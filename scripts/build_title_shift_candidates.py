#!/usr/bin/env python3
"""Find title-term shift candidates without presenting them as technical trends."""
from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from pathlib import Path

from scripts.inventory_scope import partition_titles


STOP = {
    "a", "an", "and", "based", "for", "from", "in", "of", "on", "or", "the", "to", "with",
    "using", "via", "towards", "toward", "efficient", "efficiency", "design", "system", "systems",
    "framework", "frameworks", "accelerating", "acceleration", "analysis", "architecture", "architectures",
    "hardware", "method", "methods", "model", "models", "network", "networks", "high", "low", "new",
    "based", "aware", "aware", "driven", "generation", "optimization", "optimization", "computing",
}
TOKEN = re.compile(r"[a-z][a-z0-9]{2,}")


def rows(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def counts(records: list[dict]) -> Counter:
    return Counter({term: sum(term in set(TOKEN.findall(row["title"].lower())) for row in records) for term in set(TOKEN.findall(" ".join(row["title"] for row in records).lower())) if term not in STOP})


def compare(old: list[dict], new: list[dict]) -> dict:
    old_inventory_count, new_inventory_count = len(old), len(new)
    old, old_excluded = partition_titles(old)
    new, new_excluded = partition_titles(new)
    exclusions = {
        "old_inventory_count": old_inventory_count,
        "new_inventory_count": new_inventory_count,
        "old_excluded_ids": [r["paper_id"] for r in old_excluded],
        "new_excluded_ids": [r["paper_id"] for r in new_excluded],
        "denominator_policy": "nonempty_titles_excluding_unresolved_slots",
    }
    if not old or not new:
        return {**exclusions, "old_record_count": len(old), "new_record_count": len(new),
                "comparison_status": "insufficient_titles", "candidate_terms": []}
    old_counts, new_counts = counts(old), counts(new)
    terms = sorted(set(old_counts) | set(new_counts))
    candidates = []
    for term in terms:
        old_n, new_n = old_counts[term], new_counts[term]
        if old_n + new_n < 3:
            continue
        old_share, new_share = old_n / len(old), new_n / len(new)
        candidates.append({"term": term, "old_count": old_n, "new_count": new_n, "old_share": round(old_share, 6), "new_share": round(new_share, 6), "share_delta": round(new_share - old_share, 6), "candidate_direction": "up" if new_share > old_share else "down" if new_share < old_share else "flat"})
    candidates.sort(key=lambda row: (-abs(row["share_delta"]), row["term"]))
    return {**exclusions, "old_record_count": len(old), "new_record_count": len(new),
            "comparison_status": "exploratory_metadata_only", "candidate_terms": candidates}


def build(root: Path) -> dict:
    comparisons = {
        "isca_2025_to_2026": compare(rows(root / "isca/data/papers-2025-program.jsonl"), rows(root / "isca/data/papers-2026-program.jsonl")),
        "dac_2025_to_2026": compare(rows(root / "dac/data/papers-2025-program.jsonl"), rows(root / "dac/data/papers-2026-program.jsonl")),
    }
    payload = {"schema": "title-shift-candidates.v1", "status": "exploratory_metadata_only", "comparisons": comparisons, "limits": ["Title occurrence is not paper prevalence or technical evidence.", "Program composition and naming conventions can change between editions.", "Every candidate requires abstract/full-text review with the shared taxonomy before a rising/declining claim." ]}
    (root / "reports/title-shift-candidates-v1.json").write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    lines = ["# Title-shift candidates v1", "", "This report is an exploratory screen over official program titles. It is not a", "technical trend report, prevalence estimate, or claim that a capability is", "rising or declining.", ""]
    for name, comparison in comparisons.items():
        lines += [f"## {name}", "", f"Captured inventory: {comparison['old_inventory_count']} → {comparison['new_inventory_count']} records.",
                  f"Eligible title denominators: {comparison['old_record_count']} → {comparison['new_record_count']}.",
                  f"Excluded earlier IDs: {', '.join(comparison['old_excluded_ids']) or 'none'}; later IDs: {', '.join(comparison['new_excluded_ids']) or 'none'}.",
                  "", "| Term | Earlier share | Later share | Candidate direction |", "|---|---:|---:|---|"]
        for row in comparison["candidate_terms"][:15]:
            lines.append(f"| {row['term']} | {row['old_share']:.2%} | {row['new_share']:.2%} | {row['candidate_direction']} |")
        lines += ["", "These rows route review. They do not establish that the underlying technical", "topic, method, or importance changed.", ""]
    lines += ["## Next evidence step", "", "Use the candidate terms to select comparable paper subsets, collect equivalent", "abstract/full-text evidence, adjudicate the same technical fields in both editions,", "and run independent adversarial review before writing directional conclusions.", ""]
    (root / "reports/title-shift-candidates-v1.md").write_text("\n".join(lines), encoding="utf-8")
    return {"comparisons": {name: {"old": value["old_record_count"], "new": value["new_record_count"], "candidate_count": len(value["candidate_terms"])} for name, value in comparisons.items()}}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    print(json.dumps(build(args.root), indent=2, sort_keys=True))
