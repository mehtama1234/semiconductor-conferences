# Cross-conference direction atlas v1

This is a structured comparison of what ISCA, DAC, and ICCAD contribute to each canonical direction. It distinguishes complementary layering, shared pressure, methodological bridges, and measurement contracts. It is not a venue ranking or temporal trend report.

| Direction | Relation | ISCA | DAC | ICCAD | Reviews |
|---|---|---:|---:|---:|---:|
| [Constraints Become Executable](directions/01-constraints-become-executable.md) | `complementary_layering` | 1 | 3 | 4 | 0 |
| [Data Movement As Contract](directions/02-data-movement-as-contract.md) | `same_pressure_different_layer` | 10 | 4 | 1 | 0 |
| [Reliability Security Upstream](directions/04-reliability-security-upstream.md) | `cross_layer_contract` | 3 | 3 | 1 | 0 |
| [Physical Reality In The Loop](directions/05-physical-reality-in-the-loop.md) | `upstream_physical_feedback` | 1 | 1 | 2 | 0 |
| [Closed Loop Design](directions/03-closed-loop-design.md) | `methodological_bridge` | 0 | 4 | 2 | 0 |
| [Evaluation As Research](directions/06-evaluation-as-research.md) | `measurement_contract` | 1 | 7 | 6 | 0 |

## Constraints Become Executable

Relation type: `complementary_layering`.

| Conference | Contribution in the current evidence |
|---|---|
| ISCA | Architecture/compiler cases expose executable dataflow and system constraints. |
| DAC | Design-automation cases provide broad tool-grounded generation, search, and mapping candidates. |
| ICCAD | Fallback cases expose verification, physical-flow, and design-method consequences. |

Interpretation: The venues support a shared mechanism of constraint-driven iteration, not one common benchmark or growth rate.

Next matched comparison: Match design suites, correctness oracle, synthesis budget, model/API cost, retries, and held-out transfer.


## Data Movement As Contract

Relation type: `same_pressure_different_layer`.

| Conference | Contribution in the current evidence |
|---|---|
| ISCA | Systems and architecture cases expose expert traffic, collectives, KV locality, PIM scheduling, and deployed memory context. |
| DAC | Memory and accelerator cases expose CXL, near-memory, PIM, buffering, and movement-aware execution mechanisms. |
| ICCAD | Physical-integration cases connect bandwidth and placement to 3D thermal and package constraints. |

Interpretation: The shared pressure is movement and contention; mechanisms and quality targets remain heterogeneous.

Next matched comparison: Match workload, recall/accuracy, resident set, capacity, bandwidth, topology, migration cost, and tail latency.


## Reliability Security Upstream

Relation type: `cross_layer_contract`.

| Conference | Contribution in the current evidence |
|---|---|
| ISCA | Architecture and memory cases expose correction, interference, and thermal behavior during execution. |
| DAC | Accelerator and design-flow cases expose fault mitigation, physical integrity, attacks, and protection overhead. |
| ICCAD | Security and fallback design cases expose threat-model and validation boundaries, with broader physical-reliability scope. |

Interpretation: The venues converge on explicit operating envelopes, but fault, thermal, and threat models cannot be collapsed into one robustness score.

Next matched comparison: Match threat/fault model, coverage, false negatives, recovery cost, useful throughput, and availability impact.


## Physical Reality In The Loop

Relation type: `upstream_physical_feedback`.

| Conference | Contribution in the current evidence |
|---|---|
| ISCA | Selected runtime/system cases expose thermal imbalance and physical effects after mapping. |
| DAC | Design-automation cases expose fast thermal, package, process, and physical models for search. |
| ICCAD | Physical-design fallback cases provide the deepest placement, process, device, and signoff-oriented evidence. |

Interpretation: The layering suggests physical models are becoming decision inputs, but model transfer and manufacturability remain open.

Next matched comparison: Compare candidate ranking, constraint violations, held-out high-fidelity evaluation, and search cost across geometry/process changes.


## Closed Loop Design

Relation type: `methodological_bridge`.

| Conference | Contribution in the current evidence |
|---|---|
| ISCA | The current selected source map has no direct ISCA evidence reference for this direction; compiler/system cases remain adjacent evidence. |
| DAC | Search, surrogate, Bayesian, and tool-feedback cases provide the broadest loop inventory. |
| ICCAD | Design-space and physical-model cases expose fidelity, calibration, and downstream feasibility boundaries. |

Interpretation: This is a methodological bridge across venues, not evidence that the same adaptive loop dominates any venue.

Next matched comparison: Match total wall-clock/evaluation budget, calibration cost, rejected candidates, misranking, and out-of-distribution error.


## Evaluation As Research

Relation type: `measurement_contract`.

| Conference | Contribution in the current evidence |
|---|---|
| ISCA | Artifact and system cases expose execution, workload, and reproducibility boundaries. |
| DAC | Tool-grounded and benchmark cases expose task selection, search budget, and evaluator semantics. |
| ICCAD | Verification and physical-design cases expose proof state, simulator fidelity, and implementation boundaries. |

Interpretation: Evaluation is a cross-venue enabling layer; field direction cannot be inferred until evaluator populations and semantics are matched.

Next matched comparison: Require task population, evaluator/tool version, timeout/error semantics, baseline, budget, and independent rerun status.

## Reading boundary

The counts are selected evidence references, not venue prevalence. Evidence tiers are asymmetric, independent reviews are pending, and missing historical descriptions are not negative evidence.
