# Research agenda v1

This is the execution layer for the living research atlas. It makes the path from provisional synthesis to defensible long-term insight explicit: evidence conditions → counterpressure → independent review → matched comparison → longitudinal promotion.

Current gate: **0 independent verdicts** across **37 synthesis anchors**; **60 direction references** and **6 comparison dossiers** are tracked.

## Work packages

| ID | Workstream | Status | Priority | Depends on | Deliverable |
|---|---|---|---|---|---|
| `A1-condition-reconciliation` | evidence | `active` | P1 | — | Updated condition register with source locators for workload, hardware/process, baseline, metric, budget, limits, and explicit unknowns. |
| `A2-counterpressure-audit` | falsification | `active` | P1 | A1-condition-reconciliation | One auditable challenge record per canonical direction, with relation type, failure condition, and what observation would weaken the hypothesis. |
| `A3-independent-review` | review | `awaiting_external_review` | P1 | A1-condition-reconciliation, A2-counterpressure-audit | Two independent verdicts per selected review packet, disagreement resolution, and preserved reviewer rationale. |
| `A4-matched-comparisons` | synthesis | `ready_after_review` | P2 | A1-condition-reconciliation, A3-independent-review | Matched comparison tables for each direction using equivalent workloads/design suites, hardware/process, baselines, metrics, budgets, and validity boundaries. |
| `A5-longitudinal-promotion` | longitudinal | `disabled_until_gates_pass` | P2 | A3-independent-review, A4-matched-comparisons | Edition-comparable snapshots and a direction verdict at capability, persistence, prevalence, or impact level. |
| `D-constraints-become-executable-evidence` | direction | `active` | P1 | A1-condition-reconciliation | Condition-complete evidence table for the direction's anchors and challenge record. |
| `D-data-movement-as-contract-evidence` | direction | `active` | P1 | A1-condition-reconciliation | Condition-complete evidence table for the direction's anchors and challenge record. |
| `D-reliability-security-upstream-evidence` | direction | `active` | P1 | A1-condition-reconciliation | Condition-complete evidence table for the direction's anchors and challenge record. |
| `D-physical-reality-in-the-loop-evidence` | direction | `active` | P1 | A1-condition-reconciliation | Condition-complete evidence table for the direction's anchors and challenge record. |
| `D-closed-loop-design-evidence` | direction | `active` | P1 | A1-condition-reconciliation | Condition-complete evidence table for the direction's anchors and challenge record. |
| `D-evaluation-as-research-evidence` | direction | `active` | P1 | A1-condition-reconciliation | Condition-complete evidence table for the direction's anchors and challenge record. |

## Acceptance rules

### `A1-condition-reconciliation` — Reconcile anchor and challenge conditions
- Every anchor and challenge paper has a condition record or an explicit source-access failure record.
- Unknown fields remain unknown; description-tier values are not upgraded to full-paper evidence.
- The direction review gate is regenerated and counts match the condition register.

### `A2-counterpressure-audit` — Audit counterpressure and boundary cases
- All six directions have a role=challenge record.
- Each challenge has source tier, condition status, limits, and a source locator or documented gap.
- No challenge is counted as independent validation of the supporting direction.

### `A3-independent-review` — Obtain independent source-entailment review
- Reviewer judgments are independent of the researcher coding and each other until disagreement resolution.
- Every accepted material claim has a source-entailment verdict and unresolved objections are retained.
- The gate count changes only from recorded verdicts, never from deterministic preflight.

### `A4-matched-comparisons` — Run matched cross-conference mechanism comparisons
- Every comparison states its population and missingness denominators.
- Proxy metrics are not presented as end-to-end benefit without an explicit boundary argument.
- Contradictory or incomparable records are retained as such rather than ranked.

### `A5-longitudinal-promotion` — Promote, split, weaken, or abandon direction hypotheses
- At least two comparable editions use the same taxonomy and disclosed evidence tiers.
- Inventory, source-text, coded, condition-complete, and independently reviewed denominators are reported.
- The claim moves up only if it passes its direction's test in the protocol for comparing years. Otherwise it stays unproven, or is weakened.

### `D-constraints-become-executable-evidence` — Close condition gaps for Constraints Become Executable
- Resolve or explicitly bound missing fields for: dac-2026-research1110, dac-2026-research535, dac-2026-research865, iccad-2025-1027.
- Keep condition extraction, source entailment, and scientific correctness as separate states.
- Regenerate the direction page, dossier, and review gate.

### `D-data-movement-as-contract-evidence` — Close condition gaps for Data Movement As Contract
- Resolve or explicitly bound missing fields for: dac-2026-research1028, dac-2026-research108, dac-2026-research1113.
- Keep condition extraction, source entailment, and scientific correctness as separate states.
- Regenerate the direction page, dossier, and review gate.

### `D-reliability-security-upstream-evidence` — Close condition gaps for Reliability Security Upstream
- Resolve or explicitly bound missing fields for: dac-2026-research043, dac-2026-research046, dac-2026-research1054, iccad-2025-1000.
- Keep condition extraction, source entailment, and scientific correctness as separate states.
- Regenerate the direction page, dossier, and review gate.

### `D-physical-reality-in-the-loop-evidence` — Close condition gaps for Physical Reality In The Loop
- Resolve or explicitly bound missing fields for: dac-2026-research1065.
- Keep condition extraction, source entailment, and scientific correctness as separate states.
- Regenerate the direction page, dossier, and review gate.

### `D-closed-loop-design-evidence` — Close condition gaps for Closed Loop Design
- Resolve or explicitly bound missing fields for: dac-2026-research031, dac-2026-research046, dac-2026-research1101.
- Keep condition extraction, source entailment, and scientific correctness as separate states.
- Regenerate the direction page, dossier, and review gate.

### `D-evaluation-as-research-evidence` — Close condition gaps for Evaluation As Research
- Resolve or explicitly bound missing fields for: dac-2026-research031, dac-2026-research046, dac-2026-research1101, dac-2026-research1110, dac-2026-research535, dac-2026-research865, iccad-2025-1027.
- Keep condition extraction, source entailment, and scientific correctness as separate states.
- Regenerate the direction page, dossier, and review gate.

## Operating boundary

- A green validator proves repository consistency, not scientific acceptance.
- A prepared packet is not a verdict.
- A condition-complete record is not necessarily correct or independently reproduced.
- A comparison dossier is not a trend claim until populations, denominators, and editions are matched.

The machine-readable agenda is authoritative for task dependencies and acceptance criteria. It does not turn pending external review into completion.
