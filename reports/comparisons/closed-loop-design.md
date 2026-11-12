# Closed Loop Design: cross-conference comparison

This dossier asks what the three venues contribute to the same conceptual pressure. It is a layer comparison, not a ranking, prevalence estimate, or temporal trend claim.

**Relation type:** `methodological_bridge`  
**Current gate:** `blocked_pending_independent_review_and_condition_reconciliation`

## Comparative proposition

This is a methodological bridge across venues, not evidence that the same adaptive loop dominates any venue.

## Venue roles

| Venue | Current role | Evidence references |
|---|---|---:|
| ISCA | The current selected source map has no direct ISCA evidence reference for this direction; compiler/system cases remain adjacent evidence. | 0 |
| DAC | Search, surrogate, Bayesian, and tool-feedback cases provide the broadest loop inventory. | 4 |
| ICCAD | Design-space and physical-model cases expose fidelity, calibration, and downstream feasibility boundaries. | 2 |

## Paper-level comparison set

These are the source-backed references currently attached to the direction. Different source tiers and condition completeness are preserved rather than normalized away. Dated corrections use current source links, but do not inherit a historical complete-condition label. The direction promotion gate above is historical and is not newly satisfied by a correction.

### DAC

| Paper | Edition | Evidence tier | Conditions | Source |
|---|---:|---|---|---|
| `dac-2026-research031` — Quantum Circuit Synthesis Using an Exact T Library | 2026 | `Primary captured official DAC description plus selected author-preprint reading; source-version discrepancy remains open, and no independent exactness proof, benchmark reproduction or fault-tolerant hardware validation` | `correction_pending_condition_review` | [source](https://arxiv.org/html/2605.15476v1) |
| `dac-2026-research046` — GEMIR: Graph-Based Joint Modeling of Electromigration and IR Drop for Power Grid | 2026 | `Primary captured official DAC description plus bounded recovery assessment and existing authored power-integrity discussion; full paper not recovered, numerical claims withheld pending conditions, no reproduced physics validation or fabricated-chip result` | `correction_pending_condition_review` | [source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH046) |
| `dac-2026-research1101` — HYPER-CIM: Hierarchical Predictive Exploration and Realizable Design Flow for High-Efficient Digital CIM | 2026 | `Primary captured official DAC description plus supplementary official/institutional assessment; no recovered full paper or independent surrogate, design-flow and silicon reproduction` | `correction_pending_condition_review` | [source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH1101&sess=sess156) |
| `dac-2026-research1186` — Xsearch: Exploring Microarchitecture Design Space Through Bayesian Optimization and Cross Evaluation on Multi-Fidelity Simulators | 2026 | `Primary captured official DAC description plus existing authored learned-DSE discussion; no full-paper extraction, numerical result, simulator-condition matrix or independent high-fidelity validation` | `correction_pending_condition_review` | [source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH1186&sess=sess167) |
| `dac-2026-research399` — ChiSER: Surrogate-Enhanced Resource-Aware Exploration of Chiplet-Based Deep Neural Network Accelerators | 2026 | `Primary captured official DAC description only; no full-paper extraction, surrogate reproduction or independent exhaustive/reference-search validation` | `correction_pending_condition_review` | [source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH399&sess=sess110) |

- [dac-2026-research031: current correction and original evidence](../observed-subthemes/synthesis-and-compilation.md#paper-dac-2026-research031) — corrected 2026-09-09; historical condition status `partial` is not carried forward as approval.
- [dac-2026-research046: current correction and original evidence](../observed-subthemes/power-integrity-and-reliability.md#paper-dac-2026-research046) — corrected 2026-09-09; historical condition status `partial` is not carried forward as approval.
- [dac-2026-research1101: current correction and original evidence](../observed-subthemes/architecture-software-co-design.md#paper-dac-2026-research1101) — corrected 2026-09-08; historical condition status `partial` is not carried forward as approval.
- [dac-2026-research1186: current correction and original evidence](../observed-subthemes/learned-design-space-exploration.md#paper-dac-2026-research1186) — corrected 2026-09-09; historical condition status `complete` is not carried forward as approval.
- [dac-2026-research399: current correction and original evidence](../observed-subthemes/chiplet-system-architecture.md#paper-dac-2026-research399) — corrected 2026-09-08; historical condition status `complete` is not carried forward as approval.

### ICCAD

| Paper | Edition | Evidence tier | Conditions | Source |
|---|---:|---|---|---|
| `iccad-2025-1080` — RSizing: Robust Bayesian Optimization for Analog Circuit Sizing Under Process Variations | 2025 | `Primary author-hosted manuscript-backed selected evaluation; page-level extraction performed 2026-09-08; independent reproduction and broader technology/circuit validation remain open` | `correction_pending_condition_review` | [source](https://www.cse.cuhk.edu.hk/~byu/papers/C287-ICCAD2025-RSizing.pdf) |
| `iccad-2025-130` — NeuroPDE: A Neuromorphic PDE Solver Based on Spintronic and Ferroelectric Devices | 2025 | `Recovered version-1 manuscript; cited sections inspected` | `correction_pending_condition_review` | [source](https://arxiv.org/pdf/2507.04677v1) |

- [iccad-2025-1080: current correction and original evidence](../observed-subthemes/process-aware-design.md#paper-iccad-2025-1080) — corrected 2026-09-08; historical condition status `complete` is not carried forward as approval.
- [iccad-2025-130: current correction and original evidence](../observed-subthemes/neuromorphic-quantum-and-non-von-neumann.md#paper-iccad-2025-130) — corrected 2026-09-07; historical condition status `complete` is not carried forward as approval.

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

Match total wall-clock/evaluation budget, calibration cost, rejected candidates, misranking, and out-of-distribution error.

## Current conclusion boundary

The evidence supports a provisional cross-conference mechanism relation. It does not establish that the direction is increasing, dominant, superior, or independently validated. The [direction review gate](../direction-review-gate-v1.md) records the remaining promotion work.
