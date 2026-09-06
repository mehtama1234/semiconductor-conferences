#!/usr/bin/env python3
"""Join inventories and evidence without promoting discovery into adjudication."""
from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path

from scripts.build_evidence_summary import PATHS, read_jsonl, source_tier
from scripts.collect_isca_crossref_metadata import title_key
from scripts.inventory_scope import title_eligible


def unique_index(records: list[dict]) -> dict[str, dict]:
    result = {}
    for row in records:
        if row["paper_id"] in result:
            raise ValueError(f"Duplicate paper ID: {row['paper_id']}")
        result[row["paper_id"]] = row
    return result


def build(root: Path) -> tuple[list[dict], dict, str]:
    inventory_paths = sorted(root.glob("*/data/papers-20??-program.jsonl"))
    inventory = unique_index([row for path in inventory_paths for row in read_jsonl(path)])
    coded = unique_index([row for path in PATHS for row in read_jsonl(root / path)])
    if set(coded) - set(inventory):
        raise ValueError("Coded records outside inventory")
    metadata = unique_index(read_jsonl(root / "isca/data/crossref-metadata-2026.jsonl"))
    descriptions = unique_index([
        row for path in sorted(root.glob("*/data/paper-evidence-20??.jsonl"))
        for row in read_jsonl(path)
    ])
    if (set(metadata) | set(descriptions)) - set(inventory):
        raise ValueError("Evidence records outside inventory")
    titles = defaultdict(list)
    for row in inventory.values():
        titles[(row["conference_id"], row["analysis_edition"], title_key(row["title"]))].append(row["paper_id"])
    secondary = {}
    for row in read_jsonl(root / "isca/data/indexed-evidence.jsonl"):
        matches = titles[(row["conference_id"], row["analysis_edition"], title_key(row["title"]))]
        if len(matches) != 1 or matches[0] in secondary:
            raise ValueError(f"Non-unique secondary identity: {row['paper_id']}")
        secondary[matches[0]] = row
    directions = defaultdict(list)
    for direction in json.loads((root / "data/technology-direction-evidence-v1.json").read_text())["directions"]:
        for ref in direction["evidence"]:
            if ref["paper_id"] not in coded:
                raise ValueError(f"Uncoded synthesis reference: {ref['paper_id']}")
            directions[ref["paper_id"]].append(direction["direction_id"])
    preliminary = unique_index(read_jsonl(root / "reports/adversarial-review-batch-2.jsonl"))
    queue = []
    for paper_id, paper in inventory.items():
        record = coded.get(paper_id)
        description = descriptions.get(paper_id, {})
        indexed = secondary.get(paper_id)
        substantive = description.get("evidence_status") == "substantive_description"
        doi = metadata.get(paper_id, {}).get("doi")
        if not doi and record and str(record.get("doi_or_identifier", "")).lower().startswith("10."):
            doi = record["doi_or_identifier"]
        unresolved = paper["conference_id"] == "isca" and paper["analysis_edition"] == 2026 and not doi
        capture = description.get("capture_status", description.get("fetch_status", "no_detail_capture_recorded"))
        reasons = []
        if not paper["title"].strip():
            reasons.append("missing_program_title")
        if directions[paper_id]:
            reasons.append("synthesis_anchor")
        if indexed and not record:
            reasons.append("secondary_requires_primary")
        if unresolved:
            reasons.append("unresolved_isca_doi")
        if record:
            reasons.append("coded_requires_source_depth_and_review")
        elif substantive:
            reasons.append("description_ready_for_coding")
        else:
            reasons.append("technical_source_needed")
        priority = (0 if directions[paper_id] else 1 if indexed and not record else
                    2 if unresolved else 3 if record else 4 if substantive else 5)
        actions = []
        if unresolved:
            actions.append("Resolve exact program identity against publisher or author metadata")
        if record:
            actions += ["Extract source passages and full-paper experimental conditions",
                        "Prepare independent review packet; acceptance remains pending"]
        elif substantive:
            actions.append("Code technical fields from captured description; preserve missing conditions")
        else:
            actions.append("Recover exact primary abstract or permitted author paper and log outcome")
        queue.append({
            "paper_id": paper_id, "conference_id": paper["conference_id"],
            "analysis_edition": paper["analysis_edition"], "target_edition": paper["target_edition"],
            "title": paper["title"], "doi": doi,
            "title_denominator_included": title_eligible(paper),
            "inventory_inclusion": "included_titled_record" if title_eligible(paper) else "excluded_unresolved_slot",
            "identity_status": "missing_title_requires_inventory_review" if not paper["title"].strip() else "doi_linked" if doi else "program_identifier_only",
            "collection_status": "cited_technical_source" if record else "substantive_description" if substantive else "secondary_only" if indexed else "metadata_only",
            "detail_capture_status": capture,
            "coding_status": "coded_selected_sample" if record else "not_coded",
            "evidence_tier": source_tier(record) if record else "official_description" if substantive else "secondary_indexed_excerpt" if indexed else "program_metadata",
            "evidence_depth_status": record.get("evidence_depth_status", "requires_source_depth_review") if record else "not_assessed",
            "independent_review_status": "pending" if record else "not_ready",
            "preliminary_review": preliminary.get(paper_id, {}).get("decision"),
            "preliminary_review_mode": preliminary.get(paper_id, {}).get("judge_mode"),
            "secondary_alias_id": indexed["paper_id"] if indexed else None,
            "evidence_url": record.get("evidence_url") if record else description.get("evidence_url") if substantive else indexed.get("source_url") if indexed else None,
            "program_url": paper.get("program_url"),
            "synthesis_directions": sorted(set(directions[paper_id])),
            "priority": priority, "priority_reasons": reasons, "next_actions": actions,
        })
    queue.sort(key=lambda row: (row["priority"], row["conference_id"], row["analysis_edition"], row["paper_id"]))
    counts = Counter(f"{r['conference_id']}-{r['analysis_edition']}" for r in queue)
    summary = {
        "schema": "research-work-queue.v1", "record_count": len(queue),
        "inventory_paths": [str(p.relative_to(root)) for p in inventory_paths],
        "corpus_counts": dict(sorted(counts.items())), "coded_count": len(coded),
        "eligible_title_counts": dict(sorted(Counter(f"{r['conference_id']}-{r['analysis_edition']}" for r in queue if r["title_denominator_included"]).items())),
        "excluded_slot_ids": [r["paper_id"] for r in queue if not r["title_denominator_included"]],
        "synthesis_anchor_count": sum(bool(r["synthesis_directions"]) for r in queue),
        "secondary_pending_ids": [r["paper_id"] for r in queue if "secondary_requires_primary" in r["priority_reasons"]],
        "unresolved_isca_doi_ids": [r["paper_id"] for r in queue if "unresolved_isca_doi" in r["priority_reasons"]],
        "collection_counts": dict(sorted(Counter(r["collection_status"] for r in queue).items())),
        "limits": ["Priority is review routing, not importance or prevalence.",
                   "Source tier does not establish full-text extraction or independent acceptance.",
                   "Historical challenge/rate-limit outcomes are preserved; metadata-only does not mean inaccessible.",
                   "Independent review remains pending; same-model preliminary review is separate.",
                   "Coverage is selected for recoverability and diversity; unidentified counterexamples and thin taxonomy branches still need manual prioritization."],
    }
    lines = ["# Research coverage and work queue", "", "Generated by `PYTHONPATH=.:src python3 scripts/build_work_queue.py`.", "",
             f"{len(queue)} inventory records; {len(coded)} coded; {summary['synthesis_anchor_count']} unique synthesis anchors.", "",
             "| Corpus | Captured rows | Eligible titles | Coded |", "|---|---:|---:|---:|"]
    for corpus, count in sorted(counts.items()):
        selected = sum(f"{r['conference_id']}-{r['analysis_edition']}" == corpus and r["coding_status"] == "coded_selected_sample" for r in queue)
        lines.append(f"| {corpus} | {count} | {summary['eligible_title_counts'].get(corpus, 0)} | {selected} |")
    lines += ["", "## Identity and primary-source recovery", "", "| Paper ID | Title | Reason |", "|---|---|---|"]
    for row in queue:
        if row["paper_id"] in summary["secondary_pending_ids"] + summary["unresolved_isca_doi_ids"]:
            lines.append(f"| {row['paper_id']} | {row['title'].replace('|', '/') or '[missing program title]'} | {', '.join(row['priority_reasons'])} |")
    lines += ["", "## Priority rules", "", "Order: synthesis anchors, secondary-source recovery, unresolved ISCA identifiers, other coded records, captured descriptions, remaining metadata. Ties use conference, edition, then paper ID. Each JSONL row retains separate collection, coding, source depth, and review states.", "", "## Limits", ""]
    lines += [f"- {limit}" for limit in summary["limits"]]
    return queue, summary, "\n".join(lines) + "\n"


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    queue, summary, report = build(args.root)
    (args.root / "data/research-work-queue.jsonl").write_text("".join(json.dumps(row, sort_keys=True, ensure_ascii=False) + "\n" for row in queue))
    (args.root / "reports/research-work-queue-summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    (args.root / "reports/research-work-queue.md").write_text(report)
    print(json.dumps(summary, indent=2, sort_keys=True))
