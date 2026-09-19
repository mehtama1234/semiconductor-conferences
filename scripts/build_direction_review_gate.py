#!/usr/bin/env python3
"""Build the paper-level promotion gate for the canonical research directions."""
from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read_json(path: str):
    return json.loads((ROOT / path).read_text())


def read_jsonl(path: str):
    return [json.loads(line) for line in (ROOT / path).read_text().splitlines() if line.strip()]


def build() -> dict:
    atlas = read_json("data/long-term-direction-atlas-v1.json")
    conditions = {row["paper_id"]: row for direction in read_json("data/direction-condition-register-v1.json")["directions"] for row in direction["papers"]}
    primary = {row["paper_id"]: row for row in read_jsonl("data/primary-condition-assessments-v1.jsonl")}
    supplementary = {}
    supplementary_paths = [ROOT / "data/direction-condition-extractions-v1.jsonl"]
    supplementary_paths.extend(sorted(ROOT.glob("**/data/source-condition-extractions-v1.jsonl")))
    for path in supplementary_paths:
        for row in (json.loads(line) for line in path.read_text().splitlines() if line.strip()):
            if row["paper_id"] in supplementary:
                raise ValueError(f"Duplicate supplementary extraction: {row['paper_id']}")
            supplementary[row["paper_id"]] = row
    queue = {row["paper_id"]: row for row in read_jsonl("data/research-work-queue.jsonl")}
    coverage = read_json("reports/review-packet-coverage.json")
    assignments = {row["paper_id"]: row for row in read_json("reports/independent-review-assignments-v1.json")["assignments"]}
    anchors = set(coverage["synthesis_anchor_ids"])

    directions = []
    for direction in atlas["directions"]:
        source_ids = set(direction.get("source_direction_ids", []))
        paper_ids = {row["paper_id"] for row in direction.get("evidence", [])}
        if direction.get("challenge", {}).get("paper_id"):
            paper_ids.add(direction["challenge"]["paper_id"])
        paper_ids.update(
            paper_id for paper_id, row in queue.items() if source_ids.intersection(row.get("synthesis_directions", []))
        )
        papers = []
        for paper_id in sorted(paper_ids):
            row = queue.get(paper_id, {})
            condition = conditions.get(paper_id, {})
            assignment = assignments.get(paper_id)
            papers.append({
                "paper_id": paper_id,
                "title": row.get("title"),
                "conference_id": row.get("conference_id") or next((e["conference_id"] for e in direction.get("evidence", []) if e["paper_id"] == paper_id), None),
                "edition": row.get("analysis_edition") or next((e["edition"] for e in direction.get("evidence", []) if e["paper_id"] == paper_id), None),
                "evidence_tier": row.get("evidence_tier") or next((e["evidence_tier"] for e in direction.get("evidence", []) if e["paper_id"] == paper_id), None),
                "is_synthesis_anchor": paper_id in anchors,
                "packet_path": assignment.get("packet_path") if assignment else None,
                "review_status": assignment.get("review_status") if assignment else row.get("independent_review_status"),
                "independent_verdict_count": len(assignment.get("verdicts", [])) if assignment else 0,
                "condition_status": condition.get("condition_status", "not_registered"),
                "missing_conditions": condition.get("missing_conditions", []),
                "combined_condition_status": condition.get("combined_condition_status", condition.get("condition_status", "not_registered")),
                "combined_missing_conditions": condition.get("combined_missing_conditions", condition.get("missing_conditions", [])),
                "primary_assessment": primary.get(paper_id, {}).get("assessment_path"),
                "primary_assessment_review_status": primary.get(paper_id, {}).get("independent_review_status"),
                "supplementary_extraction": supplementary.get(paper_id, {}).get("schema"),
                "supplementary_evidence_tier": supplementary.get(paper_id, {}).get("evidence_tier"),
                "supplementary_review_status": supplementary.get(paper_id, {}).get("independent_review_status"),
                "source_direction_ids": sorted(set(row.get("synthesis_directions", [])) & source_ids),
            })
        complete = sum(p["condition_status"] == "complete" for p in papers)
        partial = sum(p["condition_status"] == "partial" for p in papers)
        combined_complete = sum(p["combined_condition_status"] == "complete" for p in papers)
        combined_partial = sum(p["combined_condition_status"] == "partial" for p in papers)
        packet_count = sum(bool(p["packet_path"]) for p in papers)
        verdict_count = sum(p["independent_verdict_count"] for p in papers)
        directions.append({
            "direction_id": direction["direction_id"],
            "label": direction["label"],
            "page": direction["page"],
            "paper_count": len(papers),
            "anchor_paper_count": sum(p["is_synthesis_anchor"] for p in papers),
            "packet_count": packet_count,
            "condition_complete_count": complete,
            "condition_partial_count": partial,
            "combined_condition_complete_count": combined_complete,
            "combined_condition_partial_count": combined_partial,
            "primary_assessment_count": sum(bool(p["primary_assessment"]) for p in papers),
            "independent_verdict_count": verdict_count,
            "promotion_gate": "blocked_pending_independent_review_and_condition_reconciliation",
            "required_actions": [
                "Reconcile adjudicated-row gaps with supplementary source-condition fields for anchor papers; preserve source tiers and explicitly bind any remaining workload, hardware/process, baseline, metric, and limit gaps.",
                "Obtain two independent source-entailment verdicts per review packet and resolve disagreements.",
                "Re-run the longitudinal protocol only after direction mapping and condition fields survive review.",
            ],
            "papers": papers,
        })
    return {
        "schema": "direction-review-gate.v1",
        "as_of": "2026-09-07",
        "status": "promotion_blocked_pending_review",
        "source_policy": "A direction is a research hypothesis until paper-level conditions and independent source-entailment review are complete.",
        "independent_review_count": coverage["independent_review_count"],
        "synthesis_anchor_count": coverage["synthesis_anchor_count"],
        "directions": directions,
        "interpretation_limits": [
        "Review packet presence means prepared, not accepted.",
        "Condition completeness is an extraction property, not proof that the reported result is correct.",
        "Combined condition completeness includes explicitly tiered supplementary extractions; it does not rewrite the adjudicated ledger or count as independent review.",
        "Primary assessments remain researcher-authored until independent review.",
            "No direction may be promoted to a longitudinal trend claim from this gate alone.",
        ],
    }


def render(data: dict) -> str:
    lines = [
        "# Direction Review Gate v1", "",
        "This is the promotion boundary between a useful conceptual direction and a defensible long-term claim.",
        "A direction remains provisional until its anchor papers have source-entailment review and reconciled experimental conditions.", "",
        f"Status: **{data['status']}**  ",
        f"Synthesis anchors: **{data['synthesis_anchor_count']}**; independent verdicts: **{data['independent_review_count']}**.", "",
        "## Gate summary", "",
        "| Direction | Papers | Anchors | Packets | Adjudicated complete | Adjudicated partial | Combined complete | Combined partial | Primary assessments | Verdicts | Promotion |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|",
    ]
    for d in data["directions"]:
        lines.append(f"| [{d['label']}]({d['page'].split('reports/', 1)[-1]}) | {d['paper_count']} | {d['anchor_paper_count']} | {d['packet_count']} | {d['condition_complete_count']} | {d['condition_partial_count']} | {d['combined_condition_complete_count']} | {d['combined_condition_partial_count']} | {d['primary_assessment_count']} | {d['independent_verdict_count']} | blocked |")
    lines += ["", "## Required next actions", ""]
    for d in data["directions"]:
        lines.append(f"### {d['label']}")
        for action in d["required_actions"]:
            lines.append(f"- {action}")
        lines.append("")
    lines += ["## Paper-level audit", "", "The machine-readable JSON is authoritative for the full paper list. The following compact view identifies anchor papers that still need work:", ""]
    for d in data["directions"]:
        pending = [p for p in d["papers"] if p["is_synthesis_anchor"] and (p["independent_verdict_count"] == 0 or p["combined_condition_status"] != "complete")]
        lines.append(f"- **{d['label']}**: " + (", ".join(f"`{p['paper_id']}` (adjudicated={p['condition_status']}, combined={p['combined_condition_status']})" for p in pending) if pending else "no pending anchors") + ".")
    lines += ["", "## Interpretation boundary", "", *[f"- {item}" for item in data["interpretation_limits"]], ""]
    return "\n".join(lines)


if __name__ == "__main__":
    output = build()
    (ROOT / "data/direction-review-gate-v1.json").write_text(json.dumps(output, indent=2) + "\n")
    (ROOT / "reports/direction-review-gate-v1.md").write_text(render(output))
