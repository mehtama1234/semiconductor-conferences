# Constraints Become Executable: cross-conference comparison

This dossier asks what the three venues contribute to the same conceptual pressure. It is a layer comparison, not a ranking, prevalence estimate, or temporal trend claim.

**Relation type:** `complementary_layering`  
**Current gate:** `blocked_pending_independent_review_and_condition_reconciliation`

## Comparative proposition

The venues support a shared mechanism of constraint-driven iteration, not one common benchmark or growth rate.

## Venue roles

| Venue | Current role | Evidence references |
|---|---|---:|
| ISCA | Architecture/compiler cases expose executable dataflow and system constraints. | 1 |
| DAC | Design-automation cases provide broad tool-grounded generation, search, and mapping candidates. | 3 |
| ICCAD | Fallback cases expose verification, physical-flow, and design-method consequences. | 4 |

## Paper-level comparison set

These are the source-backed references currently attached to the direction. Different source tiers and condition completeness are preserved rather than normalized away. Dated corrections use current source links, but do not inherit a historical complete-condition label. The direction promotion gate above is historical and is not newly satisfied by a correction.

### ISCA

| Paper | Edition | Evidence tier | Conditions | Source |
|---|---:|---|---|---|
| `isca-2026-program-002` — CODO: An Automated Compiler for Comprehensive Dataflow Optimization | 2026 | `primary_or_author_copy` | `complete` | [source](https://arxiv.org/abs/2604.12618) |


### DAC

| Paper | Edition | Evidence tier | Conditions | Source |
|---|---:|---|---|---|
| `dac-2026-research1110` — LLM-Based Automatic Architecture Optimization for AI Model HLS Implementation on FPGA | 2026 | `Primary captured official DAC description plus author-linked partial artifact assessment and existing authored explanation; full paper and complete optimization framework not recovered, no execution, post-route timing, board run or independent functional validation` | `correction_pending_condition_review` | [source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH1110) |
| `dac-2026-research2760` — Notsotiny: A Large, Living Benchmark for RTL Code Generation | 2026 | `Primary arXiv preprint v1, official DAC description and read-only pinned evaluator inspection; no artifact execution or independent acceptance` | `correction_pending_condition_review` | [source](https://arxiv.org/pdf/2512.20823v1) |
| `dac-2026-research535` — Mappingevolve: LLM-Driven Code Evolution for Technology Mapping | 2026 | `Primary arXiv preprint v1, PDF table crosscheck, public artifact inspection and official DAC description; no experiment execution or independent acceptance` | `correction_pending_condition_review` | [source](https://arxiv.org/pdf/2604.26591v1) |
| `dac-2026-research865` — Paretopilot: Global Optimization Reasoning on HLS Design Space Exploration with LLMs | 2026 | `Official description and selected pinned artifact inspection; manuscript and reproduction missing` | `correction_pending_condition_review` | [source](https://github.com/GEAR-SEU/ParetoPilot-DAC-26/blob/d08173f66903ed466537c9327b63addac223ee95/src/DSE_LLM.py) |

- [dac-2026-research1110: current correction and original evidence](../observed-subthemes/llm-assisted-design-flows.md#paper-dac-2026-research1110) — corrected 2026-09-09; historical condition status `partial` is not carried forward as approval.
- [dac-2026-research2760: current correction and original evidence](../observed-subthemes/simulation-emulation-and-testing.md#paper-dac-2026-research2760) — corrected 2026-09-08; historical condition status `complete` is not carried forward as approval.
- [dac-2026-research535: current correction and original evidence](../observed-subthemes/llm-assisted-design-flows.md#paper-dac-2026-research535) — corrected 2026-09-08; historical condition status `partial` is not carried forward as approval.
- [dac-2026-research865: current correction and original evidence](../observed-subthemes/llm-assisted-design-flows.md#paper-dac-2026-research865) — corrected 2026-09-08; historical condition status `partial` is not carried forward as approval.

### ICCAD

| Paper | Edition | Evidence tier | Conditions | Source |
|---|---:|---|---|---|
| `iccad-2025-1027` — HLSDebugger: Identification and Correction of Logic Bugs in HLS Code with LLM Solutions | 2025 | `Primary arXiv preprint v1 and open-source artifact link; selected manuscript reading, artifact execution and independent acceptance not performed` | `correction_pending_condition_review` | [source](https://arxiv.org/pdf/2507.21485v1) |
| `iccad-2025-110` — VERIRL: Boosting the LLM -based Verilog Code Generation via Reinforcement Learning | 2025 | `Primary preprint v1; selected method/evaluation reading, not reproduction` | `correction_pending_condition_review` | [source](https://arxiv.org/pdf/2508.18462v1) |
| `iccad-2025-1207` — MAHL: Multi -Agent LLM -Guided Hierarchical Chiplet Design with Adaptive Debugging | 2025 | `Primary preprint; selected reading and execution/independent acceptance not performed` | `correction_pending_condition_review` | [source](https://arxiv.org/abs/2508.14053) |
| `iccad-2025-1222` — VeriOpt: PPA-Aware High-Quality Verilog Generation via Multi-Role LLMs | 2025 | `Primary preprint v1; selected method/evaluation reading, not reproduction` | `correction_pending_condition_review` | [source](https://arxiv.org/pdf/2507.14776v1) |

- [iccad-2025-1027: current correction and original evidence](../observed-subthemes/simulation-emulation-and-testing.md#paper-iccad-2025-1027) — corrected 2026-09-08; historical condition status `partial` is not carried forward as approval.
- [iccad-2025-110: current correction and original evidence](../observed-subthemes/llm-assisted-design-flows.md#paper-iccad-2025-110) — corrected 2026-09-08; historical condition status `complete` is not carried forward as approval.
- [iccad-2025-1207: current correction and original evidence](../observed-subthemes/chiplet-partitioning-and-integration.md#paper-iccad-2025-1207) — corrected 2026-09-08; historical condition status `complete` is not carried forward as approval.
- [iccad-2025-1222: current correction and original evidence](../observed-subthemes/llm-assisted-design-flows.md#paper-iccad-2025-1222) — corrected 2026-09-08; historical condition status `complete` is not carried forward as approval.

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

Match design suites, correctness oracle, synthesis budget, model/API cost, retries, and held-out transfer.

## Current conclusion boundary

The evidence supports a provisional cross-conference mechanism relation. It does not establish that the direction is increasing, dominant, superior, or independently validated. The [direction review gate](../direction-review-gate-v1.md) records the remaining promotion work.
