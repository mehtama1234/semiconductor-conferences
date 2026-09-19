"""Normalize existing primary/preprint/artifact assessments for direction anchors."""
from __future__ import annotations

import json
from pathlib import Path


ASSESSMENTS = [
    "dac/data/strix-primary-assessment-v1.json",
    "dac/data/mappingevolve-primary-assessment-v1.json",
    "dac/data/exact-t-primary-assessment-v1.json",
    "dac/data/notsotiny-primary-assessment-v1.json",
    "dac/data/hlsarchopt-primary-assessment-v1.json",
]


def build(root: Path) -> dict:
    rows = []
    for relative in ASSESSMENTS:
        path = root / relative
        assessment = json.loads(path.read_text(encoding="utf-8"))
        if "conditions" in assessment:
            condition_payload = assessment["conditions"]
        elif "platform" in assessment or "artifact" in assessment:
            condition_payload = {"platform": assessment.get("platform"), "artifact": assessment.get("artifact")}
        else:
            condition_payload = {}
        rows.append(
            {
                "schema": "primary-condition-assessment.v1",
                "paper_id": assessment["paper_id"],
                "title": assessment["title"],
                "assessment_path": relative,
                "source_url": assessment.get("source_url"),
                "source_tier": assessment.get("source_tier", "not_recorded"),
                "capture_date": assessment.get("capture_date"),
                "condition_payload": condition_payload,
                "pdf_verification": assessment.get("pdf_verification"),
                "artifact_inspection": assessment.get("artifact_inspection") or assessment.get("artifact"),
                "unresolved_conditions": assessment.get("unresolved_conditions", assessment.get("remaining_unknowns", [])),
                "interpretation_limits": assessment.get("interpretation_limits", []),
                "headline_metric_status": assessment.get("headline_metric_status"),
                "independent_review_status": assessment.get("independent_review_status", "pending"),
            }
        )
    output = root / "data/primary-condition-assessments-v1.jsonl"
    output.write_text("\n".join(json.dumps(row, sort_keys=True) for row in rows) + "\n", encoding="utf-8")
    lines = [
        "# Primary condition assessment register v1", "",
        "This register surfaces existing author-preprint and artifact assessments for direction-adjacent anchors. It is not an independent review and does not convert a source assessment into an accepted result.", "",
        "| Paper | Source tier | Conditions | Review | Headline status |", "|---|---|---|---|---|",
    ]
    for row in rows:
        conditions = ", ".join(row["condition_payload"]) if isinstance(row["condition_payload"], dict) else "recorded"
        lines.append(f"| `{row['paper_id']}` — {row['title']} | `{row['source_tier']}` | {conditions or 'none'} | `{row['independent_review_status']}` | `{row['headline_metric_status']}` |")
    lines += ["", "## Use boundary", "", "Use these records to deepen condition extraction and direct review. Preserve each source tier, unresolved-condition list, and interpretation limit. Primary or artifact evidence is not independent validation.", ""]
    (root / "reports/primary-condition-assessment-register-v1.md").write_text("\n".join(lines), encoding="utf-8")
    return {"schema": "primary-condition-assessment-register.v1", "status": "source_assessments_pending_independent_review", "record_count": len(rows), "output": "data/primary-condition-assessments-v1.jsonl"}


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    print(json.dumps(build(args.root), indent=2))
