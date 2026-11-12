# Evaluation As Research: cross-conference comparison

This dossier asks what the three venues contribute to the same conceptual pressure. It is a layer comparison, not a ranking, prevalence estimate, or temporal trend claim.

**Relation type:** `measurement_contract`  
**Current gate:** `blocked_pending_independent_review_and_condition_reconciliation`

## Comparative proposition

Evaluation is a cross-venue enabling layer; field direction cannot be inferred until evaluator populations and semantics are matched.

## Venue roles

| Venue | Current role | Evidence references |
|---|---|---:|
| ISCA | Artifact and system cases expose execution, workload, and reproducibility boundaries. | 1 |
| DAC | Tool-grounded and benchmark cases expose task selection, search budget, and evaluator semantics. | 7 |
| ICCAD | Verification and physical-design cases expose proof state, simulator fidelity, and implementation boundaries. | 6 |

## Paper-level comparison set

These are the source-backed references currently attached to the direction. Different source tiers and condition completeness are preserved rather than normalized away. Dated corrections use current source links, but do not inherit a historical complete-condition label. The direction promotion gate above is historical and is not newly satisfied by a correction.

### ISCA

| Paper | Edition | Evidence tier | Conditions | Source |
|---|---:|---|---|---|
| `isca-2026-program-002` — CODO: An Automated Compiler for Comprehensive Dataflow Optimization | 2026 | `primary_or_author_copy` | `complete` | [source](https://arxiv.org/abs/2604.12618) |


### DAC

| Paper | Edition | Evidence tier | Conditions | Source |
|---|---:|---|---|---|
| `dac-2026-research031` — Quantum Circuit Synthesis Using an Exact T Library | 2026 | `Primary captured official DAC description plus selected author-preprint reading; source-version discrepancy remains open, and no independent exactness proof, benchmark reproduction or fault-tolerant hardware validation` | `correction_pending_condition_review` | [source](https://arxiv.org/html/2605.15476v1) |
| `dac-2026-research046` — GEMIR: Graph-Based Joint Modeling of Electromigration and IR Drop for Power Grid | 2026 | `Primary captured official DAC description plus bounded recovery assessment and existing authored power-integrity discussion; full paper not recovered, numerical claims withheld pending conditions, no reproduced physics validation or fabricated-chip result` | `correction_pending_condition_review` | [source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH046) |
| `dac-2026-research1101` — HYPER-CIM: Hierarchical Predictive Exploration and Realizable Design Flow for High-Efficient Digital CIM | 2026 | `Primary captured official DAC description plus supplementary official/institutional assessment; no recovered full paper or independent surrogate, design-flow and silicon reproduction` | `correction_pending_condition_review` | [source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH1101&sess=sess156) |
| `dac-2026-research1110` — LLM-Based Automatic Architecture Optimization for AI Model HLS Implementation on FPGA | 2026 | `Primary captured official DAC description plus author-linked partial artifact assessment and existing authored explanation; full paper and complete optimization framework not recovered, no execution, post-route timing, board run or independent functional validation` | `correction_pending_condition_review` | [source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH1110) |
| `dac-2026-research1186` — Xsearch: Exploring Microarchitecture Design Space Through Bayesian Optimization and Cross Evaluation on Multi-Fidelity Simulators | 2026 | `Primary captured official DAC description plus existing authored learned-DSE discussion; no full-paper extraction, numerical result, simulator-condition matrix or independent high-fidelity validation` | `correction_pending_condition_review` | [source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH1186&sess=sess167) |
| `dac-2026-research2014` — OpenACMv2: An Accuracy-Constrained Co-Optimization Framework for Approximate DCiM | 2026 | `Primary captured official DAC description plus direction-atlas challenge context; no full-paper extraction, reproduced OpenACMv2 flow, calibrated circuit/yield study or independent application-quality evaluation` | `correction_pending_condition_review` | [source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH2014&sess=sess118) |
| `dac-2026-research535` — Mappingevolve: LLM-Driven Code Evolution for Technology Mapping | 2026 | `Primary arXiv preprint v1, PDF table crosscheck, public artifact inspection and official DAC description; no experiment execution or independent acceptance` | `correction_pending_condition_review` | [source](https://arxiv.org/pdf/2604.26591v1) |
| `dac-2026-research865` — Paretopilot: Global Optimization Reasoning on HLS Design Space Exploration with LLMs | 2026 | `Official description and selected pinned artifact inspection; manuscript and reproduction missing` | `correction_pending_condition_review` | [source](https://github.com/GEAR-SEU/ParetoPilot-DAC-26/blob/d08173f66903ed466537c9327b63addac223ee95/src/DSE_LLM.py) |

- [dac-2026-research031: current correction and original evidence](../observed-subthemes/synthesis-and-compilation.md#paper-dac-2026-research031) — corrected 2026-09-09; historical condition status `partial` is not carried forward as approval.
- [dac-2026-research046: current correction and original evidence](../observed-subthemes/power-integrity-and-reliability.md#paper-dac-2026-research046) — corrected 2026-09-09; historical condition status `partial` is not carried forward as approval.
- [dac-2026-research1101: current correction and original evidence](../observed-subthemes/architecture-software-co-design.md#paper-dac-2026-research1101) — corrected 2026-09-08; historical condition status `partial` is not carried forward as approval.
- [dac-2026-research1110: current correction and original evidence](../observed-subthemes/llm-assisted-design-flows.md#paper-dac-2026-research1110) — corrected 2026-09-09; historical condition status `partial` is not carried forward as approval.
- [dac-2026-research1186: current correction and original evidence](../observed-subthemes/learned-design-space-exploration.md#paper-dac-2026-research1186) — corrected 2026-09-09; historical condition status `complete` is not carried forward as approval.
- [dac-2026-research2014: current correction and original evidence](../observed-subthemes/processing-in-memory-and-memory-centric-compute.md#paper-dac-2026-research2014) — corrected 2026-09-09; historical condition status `complete` is not carried forward as approval.
- [dac-2026-research535: current correction and original evidence](../observed-subthemes/llm-assisted-design-flows.md#paper-dac-2026-research535) — corrected 2026-09-08; historical condition status `partial` is not carried forward as approval.
- [dac-2026-research865: current correction and original evidence](../observed-subthemes/llm-assisted-design-flows.md#paper-dac-2026-research865) — corrected 2026-09-08; historical condition status `partial` is not carried forward as approval.

### ICCAD

| Paper | Edition | Evidence tier | Conditions | Source |
|---|---:|---|---|---|
| `iccad-2025-1027` — HLSDebugger: Identification and Correction of Logic Bugs in HLS Code with LLM Solutions | 2025 | `Primary arXiv preprint v1 and open-source artifact link; selected manuscript reading, artifact execution and independent acceptance not performed` | `correction_pending_condition_review` | [source](https://arxiv.org/pdf/2507.21485v1) |
| `iccad-2025-1080` — RSizing: Robust Bayesian Optimization for Analog Circuit Sizing Under Process Variations | 2025 | `Primary author-hosted manuscript-backed selected evaluation; page-level extraction performed 2026-09-08; independent reproduction and broader technology/circuit validation remain open` | `correction_pending_condition_review` | [source](https://www.cse.cuhk.edu.hk/~byu/papers/C287-ICCAD2025-RSizing.pdf) |
| `iccad-2025-110` — VERIRL: Boosting the LLM -based Verilog Code Generation via Reinforcement Learning | 2025 | `Primary preprint v1; selected method/evaluation reading, not reproduction` | `correction_pending_condition_review` | [source](https://arxiv.org/pdf/2508.18462v1) |
| `iccad-2025-1207` — MAHL: Multi -Agent LLM -Guided Hierarchical Chiplet Design with Adaptive Debugging | 2025 | `Primary preprint; selected reading and execution/independent acceptance not performed` | `correction_pending_condition_review` | [source](https://arxiv.org/abs/2508.14053) |
| `iccad-2025-1222` — VeriOpt: PPA-Aware High-Quality Verilog Generation via Multi-Role LLMs | 2025 | `Primary preprint v1; selected method/evaluation reading, not reproduction` | `correction_pending_condition_review` | [source](https://arxiv.org/pdf/2507.14776v1) |
| `iccad-2025-130` — NeuroPDE: A Neuromorphic PDE Solver Based on Spintronic and Ferroelectric Devices | 2025 | `Recovered version-1 manuscript; cited sections inspected` | `correction_pending_condition_review` | [source](https://arxiv.org/pdf/2507.04677v1) |

- [iccad-2025-1027: current correction and original evidence](../observed-subthemes/simulation-emulation-and-testing.md#paper-iccad-2025-1027) — corrected 2026-09-08; historical condition status `partial` is not carried forward as approval.
- [iccad-2025-1080: current correction and original evidence](../observed-subthemes/process-aware-design.md#paper-iccad-2025-1080) — corrected 2026-09-08; historical condition status `complete` is not carried forward as approval.
- [iccad-2025-110: current correction and original evidence](../observed-subthemes/llm-assisted-design-flows.md#paper-iccad-2025-110) — corrected 2026-09-08; historical condition status `complete` is not carried forward as approval.
- [iccad-2025-1207: current correction and original evidence](../observed-subthemes/chiplet-partitioning-and-integration.md#paper-iccad-2025-1207) — corrected 2026-09-08; historical condition status `complete` is not carried forward as approval.
- [iccad-2025-1222: current correction and original evidence](../observed-subthemes/llm-assisted-design-flows.md#paper-iccad-2025-1222) — corrected 2026-09-08; historical condition status `complete` is not carried forward as approval.
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

Require task population, evaluator/tool version, timeout/error semantics, baseline, budget, and independent rerun status.

## Current conclusion boundary

The evidence supports a provisional cross-conference mechanism relation. It does not establish that the direction is increasing, dominant, superior, or independently validated. The [direction review gate](../direction-review-gate-v1.md) records the remaining promotion work.
