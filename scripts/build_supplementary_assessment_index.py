#!/usr/bin/env python3
"""Build a dated index of supplementary source assessments without promoting them to acceptance."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from scripts.primary_supplements import load as load_supplements


def build(root: Path) -> tuple[dict, str]:
    supplements = load_supplements(root)
    rows = []
    for paper_id, items in sorted(supplements.items()):
        for item in items:
            assessment = item["assessment"]
            unresolved = assessment.get("unresolved_conditions", [])
            if not unresolved:
                unresolved = assessment.get("interpretation_limits", [])
            rows.append({
                "paper_id": paper_id,
                "path": item["path"],
                "source_url": item["source_url"],
                "capture_date": assessment.get("capture_date"),
                "source_tier": assessment.get("source_tier"),
                "recovery_status": assessment.get("recovery_status", "assessment_material_available"),
                "headline_metric_status": item["headline_metric_status"],
                "unresolved_condition_count": len(unresolved),
                "independent_review_status": assessment.get("independent_review_status"),
            })
    payload = {
        "schema": "supplementary-assessment-index.v1",
        "as_of": "2026-09-07",
        "status": "researcher_assessments_pending_independent_review",
        "assessment_count": len(rows),
        "paper_count": len({row["paper_id"] for row in rows}),
        "independent_review_count": sum(row["independent_review_status"] != "pending" for row in rows),
        "rows": rows,
        "limits": [
            "Assessments summarize permitted source inspection and are not original source text.",
            "A recovered artifact or institutional/company source does not establish manuscript-level claims.",
            "Independent review status remains pending for every indexed assessment.",
        ],
    }
    lines = [
        "# Supplementary assessment index — v1",
        "",
        "This index covers researcher-produced source assessments joined to the",
        "paper queue. It is an evidence-depth ledger, not an acceptance or ranking.",
        "",
        f"Assessments: **{payload['assessment_count']}** across **{payload['paper_count']}** papers.",
        f"Independent review count: **{payload['independent_review_count']}**.",
        "",
        "| Paper | Source tier | Recovery status | Headline status | Unresolved conditions |",
        "|---|---|---|---|---:|",
    ]
    for row in rows:
        lines.append(
            f"| `{row['paper_id']}` | {row['source_tier']} | {row['recovery_status']} | "
            f"{row['headline_metric_status']} | {row['unresolved_condition_count']} |"
        )
    lines += ["", "Every row remains pending independent review; no assessment is an acceptance verdict.", ""]
    return payload, "\n".join(lines)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    payload, report = build(args.root)
    (args.root / "data/supplementary-assessment-index-v1.json").write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (args.root / "reports/supplementary-assessment-index-v1.md").write_text(report, encoding="utf-8")
    print(json.dumps({"assessment_count": payload["assessment_count"], "paper_count": payload["paper_count"]}, indent=2, sort_keys=True))
