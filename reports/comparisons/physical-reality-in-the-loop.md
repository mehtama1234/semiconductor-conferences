# Physical Reality In The Loop: cross-conference comparison

This dossier asks what the three venues contribute to the same conceptual pressure. It is a layer comparison, not a ranking, prevalence estimate, or temporal trend claim.

**Relation type:** `upstream_physical_feedback`  
**Current gate:** `blocked_pending_independent_review_and_condition_reconciliation`

## Comparative proposition

The layering suggests physical models are becoming decision inputs, but model transfer and manufacturability remain open.

## Venue roles

| Venue | Current role | Evidence references |
|---|---|---:|
| ISCA | Selected runtime/system cases expose thermal imbalance and physical effects after mapping. | 1 |
| DAC | Design-automation cases expose fast thermal, package, process, and physical models for search. | 1 |
| ICCAD | Physical-design fallback cases provide the deepest placement, process, device, and signoff-oriented evidence. | 2 |

## Paper-level comparison set

These are the source-backed references currently attached to the direction. Different source tiers and condition completeness are preserved rather than normalized away. Dated corrections use current source links, but do not inherit a historical complete-condition label. The direction promotion gate above is historical and is not newly satisfied by a correction.

### ISCA

| Paper | Edition | Evidence tier | Conditions | Source |
|---|---:|---|---|---|
| `isca-2026-program-153` — Lit Silicon: A Case Where Thermal Imbalance Couples Concurrent Execution in Multiple GPUs | 2026 | `primary_or_author_copy` | `complete` | [source](https://arxiv.org/abs/2511.09861) |


### DAC

| Paper | Edition | Evidence tier | Conditions | Source |
|---|---:|---|---|---|
| `dac-2026-research1065` — FLASH3D: A Fast Layered Analytical Solver for High-Accuracy Steady-State Thermal Simulation of 3D ICs | 2026 | `Primary captured official DAC description only; no full-paper extraction, numerical-solver reproduction or independent transient/transfer validation` | `correction_pending_condition_review` | [source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH1065&sess=sess156) |
| `dac-2026-research1862` — Thermal Stability Strategy for a 12nm/28nm Hybrid-Bonding Wafer-on-Wafer 3D-Integrated Eflash In-Memory Computing SoC | 2026 | `Primary captured official DAC description only; no full-paper extraction, thermal/silicon execution or independent endurance/qualification validation` | `correction_pending_condition_review` | [source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH1862&sess=sess139) |

- [dac-2026-research1065: current correction and original evidence](../observed-subthemes/3d-stacking-and-thermal-management.md#paper-dac-2026-research1065) — corrected 2026-09-08; historical condition status `partial` is not carried forward as approval.
- [dac-2026-research1862: current correction and original evidence](../observed-subthemes/3d-integration-and-thermal-management.md#paper-dac-2026-research1862) — corrected 2026-09-08; historical condition status `complete` is not carried forward as approval.

### ICCAD

| Paper | Edition | Evidence tier | Conditions | Source |
|---|---:|---|---|---|
| `iccad-2025-1103` — Tasa: Thermal-aware 3D-Stacked Architecture Design with Bandwidth Sharing for LLM Inference | 2025 | `Primary arXiv preprint v3 and official ICCAD record; selected manuscript reading, simulator execution and independent acceptance not performed` | `correction_pending_condition_review` | [source](https://arxiv.org/pdf/2508.07252v3) |
| `iccad-2025-1207` — MAHL: Multi -Agent LLM -Guided Hierarchical Chiplet Design with Adaptive Debugging | 2025 | `Primary preprint; selected reading and execution/independent acceptance not performed` | `correction_pending_condition_review` | [source](https://arxiv.org/abs/2508.14053) |

- [iccad-2025-1103: current correction and original evidence](../observed-subthemes/3d-stacking-and-thermal-management.md#paper-iccad-2025-1103) — corrected 2026-09-08; historical condition status `complete` is not carried forward as approval.
- [iccad-2025-1207: current correction and original evidence](../observed-subthemes/chiplet-partitioning-and-integration.md#paper-iccad-2025-1207) — corrected 2026-09-08; historical condition status `complete` is not carried forward as approval.

## What is actually comparable

The comparison should be made at the mechanism and constraint level first. A fair comparison holds six things fixed: the workload or design set, the hardware or simulator assumptions, the baseline, the metric, the test budget, and what counts as a failure.

### Required matched fields

| Field | Why it matters |
|---|---|
| Workload / design population | Determines whether the mechanism addresses the same pressure. |
| Hardware / process / tool version | Separates a mechanism from a platform advantage. |
| Baseline and budget | Prevents unequal search, retries, tuning, or evaluator effort. |
| Metric and end-to-end boundary | Prevents proxy improvement from being reported as system benefit. |
| Failure model and limits | Defines what counts as valid, safe, feasible, or transferable. |

## Next matched comparison

Compare candidate ranking, constraint violations, held-out high-fidelity evaluation, and search cost across geometry/process changes.

## Current conclusion boundary

The evidence supports a provisional cross-conference mechanism relation. It does not establish that the direction is increasing, dominant, superior, or independently validated. The [direction review gate](../direction-review-gate-v1.md) records the remaining promotion work.
