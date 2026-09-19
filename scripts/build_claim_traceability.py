#!/usr/bin/env python3
"""Build an end-to-end claim-to-evidence traceability registry."""
from __future__ import annotations

import json
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load(path: str):
    return json.loads((ROOT / path).read_text())


def load_queue() -> dict:
    return {json.loads(line)["paper_id"]: json.loads(line) for line in (ROOT / "data/research-work-queue.jsonl").read_text().splitlines() if line.strip()}


def load_coded_records() -> dict:
    records = {}
    for path in sorted(ROOT.glob("**/data/adjudicated-*.jsonl")):
        for line in path.read_text().splitlines():
            if line.strip():
                row = json.loads(line)
                records[row["paper_id"]] = row
    return records


def build() -> dict:
    atlas = load("data/long-term-direction-atlas-v1.json")
    conditions = load("data/direction-condition-register-v1.json")
    condition_by_direction = {d["direction_id"]: d for d in conditions["directions"]}
    gate = load("data/direction-review-gate-v1.json")
    gate_by_direction = {d["direction_id"]: d for d in gate["directions"]}
    comparisons = load("data/cross-conference-comparison-dossiers-v1.json")
    comparison_by_direction = {d["direction_id"]: d for d in comparisons["dossiers"]}
    queue = load_queue()
    coded = load_coded_records()
    trace = []
    for direction in atlas["directions"]:
        did = direction["direction_id"]
        support_ids = [e["paper_id"] for e in direction.get("evidence", [])]
        challenge = direction.get("challenge", {})
        challenge_ids = [challenge["paper_id"]] if challenge.get("paper_id") else []
        all_ids = support_ids + challenge_ids
        rows = [coded[pid] for pid in all_ids if pid in coded]
        theme_ids = sorted({row.get("theme_id") for row in rows if row.get("theme_id")})
        subthemes = sorted({row.get("subtheme_id") for row in rows if row.get("subtheme_id")})
        mechanisms = sorted({row.get("mechanism_label") or row.get("subsubtheme_id") for row in rows if row.get("mechanism_label") or row.get("subsubtheme_id")})
        cond = condition_by_direction[did]
        gate_row = gate_by_direction[did]
        trace.append({
            "direction_id": did,
            "label": direction["label"],
            "proposition": direction["first_principle"],
            "direction_page": direction["page"],
            "theme_links": [{"theme_id": theme, "page": f"reports/themes/{theme}.md"} for theme in theme_ids],
            "subtheme_ids": subthemes,
            "mechanism_ids": mechanisms,
            "supporting_paper_ids": support_ids,
            "challenge_paper_ids": challenge_ids,
            "condition_record_count": cond["paper_count"],
            "condition_complete_count": cond["complete_condition_records"],
            "condition_partial_count": cond["partial_condition_records"],
            "comparison_dossier": comparison_by_direction[did]["page"],
            "agenda_task_ids": ["A1-condition-reconciliation", "A2-counterpressure-audit", f"D-{did}-evidence", "A3-independent-review", "A4-matched-comparisons", "A5-longitudinal-promotion"],
            "promotion_gate": gate_row["promotion_gate"],
            "independent_verdict_count": gate_row["independent_verdict_count"],
            "traceability_status": "complete_chain_with_explicit_promotion_boundary" if theme_ids and subthemes and mechanisms and challenge_ids else "partial_chain_requires_reconciliation",
            "unresolved_links": [
                item for item, present in (
                    ("theme", bool(theme_ids)),
                    ("subtheme", bool(subthemes)),
                    ("mechanism", bool(mechanisms)),
                    ("challenge", bool(challenge_ids)),
                ) if not present
            ],
        })
    result = {
        "schema": "claim-traceability.v1",
        "as_of": "2026-09-07",
        "status": "traceable_provisional_synthesis",
        "directions": trace,
        "interpretation_limits": [
            "A complete chain proves that the repository can navigate the claim; it does not prove the claim is true.",
            "Source tiers, condition gaps, and independent review status remain attached at paper level.",
            "A direction with zero independent verdicts cannot be promoted to a longitudinal trend or comparative-impact claim.",
        ],
    }
    (ROOT / "data/claim-traceability-v1.json").write_text(json.dumps(result, indent=2) + "\n")
    lines = [
        "# Claim traceability matrix v1", "",
        "This matrix is the end-to-end audit of the research atlas. Each row connects a first-principles proposition to themes, subthemes, mechanisms, papers, counterpressure, conditions, cross-conference comparison, execution tasks, and the promotion gate.", "",
        "| Direction | Themes | Subthemes | Mechanisms | Support papers | Challenges | Conditions | Complete | Gate |", "|---|---:|---:|---:|---:|---:|---:|---:|---|",
    ]
    for row in trace:
        lines.append(f"| [{row['label']}]({row['direction_page'].split('reports/', 1)[-1]}) | {len(row['theme_links'])} | {len(row['subtheme_ids'])} | {len(row['mechanism_ids'])} | {len(row['supporting_paper_ids'])} | {len(row['challenge_paper_ids'])} | {row['condition_record_count']} | {row['condition_complete_count']} | `{row['promotion_gate']}` |")
    lines += ["", "## End-to-end chains", ""]
    for row in trace:
        themes = ", ".join(f"[{item['theme_id']}](../{item['page']})" for item in row["theme_links"]) or "none"
        direction_link = row["direction_page"].split("reports/", 1)[-1]
        comparison_link = row["comparison_dossier"].split("reports/", 1)[-1]
        lines += [f"### {row['label']}", "", f"> {row['proposition']}", "", f"**Chain:** {themes} → `{len(row['subtheme_ids'])}` subthemes → `{len(row['mechanism_ids'])}` mechanisms → `{len(row['supporting_paper_ids'])}` supporting records + `{len(row['challenge_paper_ids'])}` challenges → `{row['condition_record_count']}` condition records → [direction page]({direction_link}) → [comparison dossier]({comparison_link}) → [promotion gate](direction-review-gate-v1.md).", "", f"**Agenda:** {', '.join(f'`{task}`' for task in row['agenda_task_ids'])}.", ""]
    lines += ["## Interpretation boundary", "", *[f"- {item}" for item in result["interpretation_limits"]], ""]
    (ROOT / "reports/claim-traceability-v1.md").write_text("\n".join(lines))
    return result


if __name__ == "__main__":
    print(json.dumps(build(), indent=2))
