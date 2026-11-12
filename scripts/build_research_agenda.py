#!/usr/bin/env python3
"""Build the dependency-aware execution agenda for the living research atlas."""
from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load(path: str):
    return json.loads((ROOT / path).read_text())


def build() -> dict:
    gate = load("data/direction-review-gate-v1.json")
    condition = load("data/direction-condition-register-v1.json")
    comparisons = load("data/cross-conference-comparison-dossiers-v1.json")
    agenda = [
        {
            "task_id": "A1-condition-reconciliation",
            "workstream": "evidence",
            "title": "Reconcile anchor and challenge conditions",
            "status": "active",
            "priority": "P1",
            "depends_on": [],
            "deliverable": "Updated condition register with source locators for workload, hardware/process, baseline, metric, budget, limits, and explicit unknowns.",
            "acceptance": [
                "Every anchor and challenge paper has a condition record or an explicit source-access failure record.",
                "Unknown fields remain unknown; description-tier values are not upgraded to full-paper evidence.",
                "The direction review gate is regenerated and counts match the condition register.",
            ],
            "evidence": ["data/direction-condition-register-v1.json", "data/direction-review-gate-v1.json"],
        },
        {
            "task_id": "A2-counterpressure-audit",
            "workstream": "falsification",
            "title": "Audit counterpressure and boundary cases",
            "status": "active",
            "priority": "P1",
            "depends_on": ["A1-condition-reconciliation"],
            "deliverable": "One auditable challenge record per canonical direction, with relation type, failure condition, and what observation would weaken the hypothesis.",
            "acceptance": [
                "All six directions have a role=challenge record.",
                "Each challenge has source tier, condition status, limits, and a source locator or documented gap.",
                "No challenge is counted as independent validation of the supporting direction.",
            ],
            "evidence": ["data/long-term-direction-atlas-v1.json", "data/direction-condition-register-v1.json", "reports/comparisons/README.md"],
        },
        {
            "task_id": "A3-independent-review",
            "workstream": "review",
            "title": "Obtain independent source-entailment review",
            "status": "awaiting_external_review",
            "priority": "P1",
            "depends_on": ["A1-condition-reconciliation", "A2-counterpressure-audit"],
            "deliverable": "Two independent verdicts per selected review packet, disagreement resolution, and preserved reviewer rationale.",
            "acceptance": [
                "Reviewer judgments are independent of the researcher coding and each other until disagreement resolution.",
                "Every accepted material claim has a source-entailment verdict and unresolved objections are retained.",
                "The gate count changes only from recorded verdicts, never from deterministic preflight.",
            ],
            "evidence": ["reports/independent-review-assignments-v1.json", "reports/adversarial-judge-protocol-v1.md", "reports/direction-review-gate-v1.md"],
        },
        {
            "task_id": "A4-matched-comparisons",
            "workstream": "synthesis",
            "title": "Run matched cross-conference mechanism comparisons",
            "status": "ready_after_review",
            "priority": "P2",
            "depends_on": ["A1-condition-reconciliation", "A3-independent-review"],
            "deliverable": "Matched comparison tables for each direction using equivalent workloads/design suites, hardware/process, baselines, metrics, budgets, and validity boundaries.",
            "acceptance": [
                "Every comparison states its population and missingness denominators.",
                "Proxy metrics are not presented as end-to-end benefit without an explicit boundary argument.",
                "Contradictory or incomparable records are retained as such rather than ranked.",
            ],
            "evidence": ["data/cross-conference-comparison-dossiers-v1.json", "reports/comparisons/README.md"],
        },
        {
            "task_id": "A5-longitudinal-promotion",
            "workstream": "longitudinal",
            "title": "Promote, split, weaken, or abandon direction hypotheses",
            "status": "disabled_until_gates_pass",
            "priority": "P2",
            "depends_on": ["A3-independent-review", "A4-matched-comparisons"],
            "deliverable": "Edition-comparable snapshots and a direction verdict at capability, persistence, prevalence, or impact level.",
            "acceptance": [
                "At least two comparable editions use the same taxonomy and disclosed evidence tiers.",
                "Inventory, source-text, coded, condition-complete, and independently reviewed denominators are reported.",
                "The claim moves up only if it passes its direction's test in the protocol for comparing years. Otherwise it stays unproven, or is weakened.",
            ],
            "evidence": ["data/longitudinal-protocol-v1.json", "reports/longitudinal-protocol-v1.md", "reports/temporal-insufficiency-v1.json"],
        },
    ]
    for direction in gate["directions"]:
        partial = [p["paper_id"] for p in direction["papers"] if p["condition_status"] != "complete"]
        agenda.append({
            "task_id": f"D-{direction['direction_id']}-evidence",
            "workstream": "direction",
            "title": f"Close condition gaps for {direction['label']}",
            "direction_id": direction["direction_id"],
            "status": "active" if partial else "ready_for_review",
            "priority": "P1",
            "depends_on": ["A1-condition-reconciliation"],
            "deliverable": "Condition-complete evidence table for the direction's anchors and challenge record.",
            "acceptance": [
                f"Resolve or explicitly bound missing fields for: {', '.join(partial) if partial else 'none'}.",
                "Keep condition extraction, source entailment, and scientific correctness as separate states.",
                "Regenerate the direction page, dossier, and review gate.",
            ],
            "evidence": [direction["page"], "data/direction-condition-register-v1.json", "reports/direction-review-gate-v1.md"],
        })
    result = {
        "schema": "research-agenda.v1",
        "as_of": "2026-09-07",
        "status": "living_execution_agenda",
        "current_gate": {
            "independent_review_count": gate["independent_review_count"],
            "synthesis_anchor_count": gate["synthesis_anchor_count"],
            "condition_reference_count": sum(d["paper_count"] for d in condition["directions"]),
            "comparison_dossier_count": len(comparisons["dossiers"]),
        },
        "agenda": agenda,
        "operating_rules": [
            "A green validator proves repository consistency, not scientific acceptance.",
            "A prepared packet is not a verdict.",
            "A condition-complete record is not necessarily correct or independently reproduced.",
            "A comparison dossier is not a trend claim until populations, denominators, and editions are matched.",
        ],
    }
    (ROOT / "data/research-agenda-v1.json").write_text(json.dumps(result, indent=2) + "\n")
    lines = [
        "# Research agenda v1", "",
        "This is the execution layer for the living research atlas. It makes the path from provisional synthesis to defensible long-term insight explicit: evidence conditions → counterpressure → independent review → matched comparison → longitudinal promotion.", "",
        f"Current gate: **{result['current_gate']['independent_review_count']} independent verdicts** across **{result['current_gate']['synthesis_anchor_count']} synthesis anchors**; **{result['current_gate']['condition_reference_count']} direction references** and **{result['current_gate']['comparison_dossier_count']} comparison dossiers** are tracked.", "",
        "## Work packages", "", "| ID | Workstream | Status | Priority | Depends on | Deliverable |", "|---|---|---|---|---|---|",
    ]
    for item in agenda:
        deps = ", ".join(item["depends_on"]) or "—"
        lines.append(f"| `{item['task_id']}` | {item['workstream']} | `{item['status']}` | {item['priority']} | {deps} | {item['deliverable']} |")
    lines += ["", "## Acceptance rules", ""]
    for item in agenda:
        lines.append(f"### `{item['task_id']}` — {item['title']}")
        for criterion in item["acceptance"]:
            lines.append(f"- {criterion}")
        lines.append("")
    lines += ["## Operating boundary", "", *[f"- {rule}" for rule in result["operating_rules"]], "", "The machine-readable agenda is authoritative for task dependencies and acceptance criteria. It does not turn pending external review into completion.", ""]
    (ROOT / "reports/research-agenda-v1.md").write_text("\n".join(lines))
    return result


if __name__ == "__main__":
    print(json.dumps(build(), indent=2))
