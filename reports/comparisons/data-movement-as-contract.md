# Data Movement As Contract: cross-conference comparison

This dossier asks what the three venues contribute to the same conceptual pressure. It is a layer comparison, not a ranking, prevalence estimate, or temporal trend claim.

**Relation type:** `same_pressure_different_layer`  
**Current gate:** `blocked_pending_independent_review_and_condition_reconciliation`

## Comparative proposition

The shared pressure is movement and contention; mechanisms and quality targets remain heterogeneous.

## Venue roles

| Venue | Current role | Evidence references |
|---|---|---:|
| ISCA | Systems and architecture cases expose expert traffic, collectives, KV locality, PIM scheduling, and deployed memory context. | 10 |
| DAC | Memory and accelerator cases expose CXL, near-memory, PIM, buffering, and movement-aware execution mechanisms. | 4 |
| ICCAD | Physical-integration cases connect bandwidth and placement to 3D thermal and package constraints. | 1 |

## Paper-level comparison set

These are the source-backed references currently attached to the direction. Different source tiers and condition completeness are preserved rather than normalized away. Dated corrections use current source links, but do not inherit a historical complete-condition label. The direction promotion gate above is historical and is not newly satisfied by a correction.

### ISCA

| Paper | Edition | Evidence tier | Conditions | Source |
|---|---:|---|---|---|
| `isca-2026-program-003` — COSM: A Cooperative Scheduling Framework for Concurrent PIM and CPU Execution on Mobile Devices | 2026 | `primary_or_author_copy` | `complete` | [source](https://arxiv.org/abs/2606.30553) |
| `isca-2026-program-005` — Patterns Behind Chaos: Forecasting Data Movement for Efficient Large-Scale MoE LLM Inference | 2026 | `Primary author preprint plus released trace-dataset reference; no independent trace/insight check, wafer-scale reproduction or cross-topology placement validation` | `correction_pending_condition_review` | [source](https://arxiv.org/abs/2510.05497) |
| `isca-2026-program-006` — Cassandra: Enabling Reasoning LLMs at Edge via Self-Speculative Decoding | 2026 | `Primary author preprint abstract only; no full-paper extraction, Cassandra reproduction or independent acceptance, reasoning-quality, latency, format-converter and edge-hardware validation` | `correction_pending_condition_review` | [source](https://arxiv.org/abs/2605.26558) |
| `isca-2026-program-007` — Combating the Memory Walls: Optimization Pathways for Long-Context Agentic LLM Inference | 2026 | `Primary author preprint abstract only; no full-paper extraction, simulator/prototype reproduction or independent memory, quality, latency, energy and hardware validation` | `correction_pending_condition_review` | [source](https://arxiv.org/abs/2509.09505) |
| `isca-2026-program-008` — Approaching Shannon Bound with Lossless LLM Weight Compression | 2026 | `Author preprint v1; selected method/results inspected; source discrepancy retained` | `correction_pending_condition_review` | [source](https://arxiv.org/pdf/2606.15789v1) |
| `isca-2026-program-020` — OASIS: Outlier-Aware LUT-Based GEMM with Dual-Side Quantization for LLM Inference Acceleration | 2026 | `Primary author version-4 preprint and captured abstract; no fabricated OASIS silicon or independent full-paper reproduction` | `correction_pending_condition_review` | [source](https://arxiv.org/pdf/2507.23035v4) |
| `isca-2026-program-044` — A Silicon-Proven Unified Low-Latency CXL Controller and Port-Based Routing Switch for Memory-Centric Fabrics | 2026 | `Official company author source; paper manuscript and independent reproduction not performed` | `correction_pending_condition_review` | [source](https://panmnesia.com/news/en/2026-06-24-panmnesia-isca2026-eng/) |
| `isca-2026-program-045` — Vistara: Making CXL Real—Full Path from ASIC Design and OS Support to Hyperscale Deployment | 2026 | `Author-hosted manuscript; selected platform, method, and evaluation sections inspected` | `correction_pending_condition_review` | [source](https://aisystemcodesign.github.io/papers/isca26/vistara_camera_ready.pdf) |
| `isca-2026-program-069` — MTIA 300: Meta’s First Training Chip Featuring Built-in NICs and Collective Offloading Engines | 2026 | `Primary author PDF with selected sections/tables inspected; no independent replication, full cost-accounting reconstruction or deployment validation` | `correction_pending_condition_review` | [source](https://aisystemcodesign.github.io/papers/MTIA300_ISCA2026.pdf) |
| `isca-2026-program-155` — DisDP: Disaggregating Compute, Network, and Storage for Model-Sharded Data-Parallel Training | 2026 | `primary_or_author_copy` | `complete` | [source](https://arxiv.org/abs/2409.00918) |

- [isca-2026-program-005: current correction and original evidence](../observed-subthemes/architecture-software-co-design.md#paper-isca-2026-program-005) — corrected 2026-09-08; historical condition status `complete` is not carried forward as approval.
- [isca-2026-program-006: current correction and original evidence](../observed-subthemes/architecture-software-co-design.md#paper-isca-2026-program-006) — corrected 2026-09-08; historical condition status `complete` is not carried forward as approval.
- [isca-2026-program-007: current correction and original evidence](../observed-subthemes/architecture-software-co-design.md#paper-isca-2026-program-007) — corrected 2026-09-08; historical condition status `complete` is not carried forward as approval.
- [isca-2026-program-008: current correction and original evidence](../observed-subthemes/memory-hierarchy-and-persistence.md#paper-isca-2026-program-008) — corrected 2026-09-07; historical condition status `complete` is not carried forward as approval.
- [isca-2026-program-020: current correction and original evidence](../observed-subthemes/ai-accelerator-microarchitecture.md#paper-isca-2026-program-020) — corrected 2026-09-08; historical condition status `complete` is not carried forward as approval.
- [isca-2026-program-044: current correction and original evidence](../observed-subthemes/chiplet-and-on-chip-interconnect.md#paper-isca-2026-program-044) — corrected 2026-09-08; historical condition status `complete` is not carried forward as approval.
- [isca-2026-program-045: current correction and original evidence](../observed-subthemes/memory-hierarchy-and-persistence.md#paper-isca-2026-program-045) — corrected 2026-09-07; historical condition status `complete` is not carried forward as approval.
- [isca-2026-program-069: current correction and original evidence](../observed-subthemes/architecture-software-co-design.md#paper-isca-2026-program-069) — corrected 2026-09-08; historical condition status `complete` is not carried forward as approval.

### DAC

| Paper | Edition | Evidence tier | Conditions | Source |
|---|---:|---|---|---|
| `dac-2026-research1028` — Ctxmem: OS-Hardware Co-Designed Tiered Memory with DRAM-SSD Hybrid CXL Devices | 2026 | `Primary captured official DAC description plus existing authored Ctxmem explanation; no full-paper extraction, reproduced GEM5 run, hardware measurement or persistence validation` | `correction_pending_condition_review` | [source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH1028) |
| `dac-2026-research108` — CANNON: A CXL-Based Near-Memory Processing Architecture for Approximate Nearest Neighbor Search on Real Hardware | 2026 | `Primary captured official DAC description plus existing authored CXL/ANN explanation; real-hardware claim is source-reported, but no full-paper extraction, reproduced query benchmark, recall validation or complete power/accounting trace` | `correction_pending_condition_review` | [source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH108) |
| `dac-2026-research1113` — Achieving Intra- and Inter-Operator Communication Lower Bounds in Near-Memory Processing | 2026 | `Primary captured official DAC description plus existing authored RAF explanation; no full-paper extraction, reproduced dataflow analysis, compiler/runtime trace or measured hardware result` | `correction_pending_condition_review` | [source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH1113) |
| `dac-2026-research1182` — Fusedot: A Multiplication-Fused Dot Product Accelerator for Efficient LLM Inference | 2026 | `Primary captured official DAC description plus source-recovery assessment; no full-paper extraction, FuseDot artifact reproduction or independent accuracy, PPA, memory and energy validation` | `correction_pending_condition_review` | [source](https://63dac.conference-program.com/presentation/?id=RESEARCH1182&sess=sess156) |
| `dac-2026-research2268` — TierANNS: Scalable Graph-Based ANNS with CXL-Enabled Tiered Data Placement | 2026 | `Primary captured official DAC description plus existing chapter-level TierANNS discussion; no full-paper extraction, numeric CXL trace, recall validation or independent review` | `correction_pending_condition_review` | [source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH2268&sess=sess169) |

- [dac-2026-research1028: current correction and original evidence](../observed-subthemes/memory-hierarchy-and-persistence.md#paper-dac-2026-research1028) — corrected 2026-09-09; historical condition status `partial` is not carried forward as approval.
- [dac-2026-research108: current correction and original evidence](../observed-subthemes/data-movement-and-locality.md#paper-dac-2026-research108) — corrected 2026-09-09; historical condition status `partial` is not carried forward as approval.
- [dac-2026-research1113: current correction and original evidence](../observed-subthemes/data-movement-and-locality.md#paper-dac-2026-research1113) — corrected 2026-09-09; historical condition status `partial` is not carried forward as approval.
- [dac-2026-research1182: current correction and original evidence](../observed-subthemes/specialized-ai-accelerators.md#paper-dac-2026-research1182) — corrected 2026-09-08; historical condition status `complete` is not carried forward as approval.
- [dac-2026-research2268: current correction and original evidence](../observed-subthemes/data-movement-and-locality.md#paper-dac-2026-research2268) — corrected 2026-09-08; historical condition status `complete` is not carried forward as approval.

### ICCAD

| Paper | Edition | Evidence tier | Conditions | Source |
|---|---:|---|---|---|
| `iccad-2025-1103` — Tasa: Thermal-aware 3D-Stacked Architecture Design with Bandwidth Sharing for LLM Inference | 2025 | `Primary arXiv preprint v3 and official ICCAD record; selected manuscript reading, simulator execution and independent acceptance not performed` | `correction_pending_condition_review` | [source](https://arxiv.org/pdf/2508.07252v3) |

- [iccad-2025-1103: current correction and original evidence](../observed-subthemes/3d-stacking-and-thermal-management.md#paper-iccad-2025-1103) — corrected 2026-09-08; historical condition status `complete` is not carried forward as approval.

## What is actually comparable

The comparison should be made at the mechanism and constraint level first. A valid matched comparison must hold constant the relevant workload or design suite, hardware/process or simulator assumptions, baseline, metric definition, evaluation budget, and failure/validity boundary.

### Required matched fields

| Field | Why it matters |
|---|---|
| Workload / design population | Determines whether the mechanism addresses the same pressure. |
| Hardware / process / tool version | Separates a mechanism from a platform advantage. |
| Baseline and budget | Prevents unequal search, retries, tuning, or evaluator effort. |
| Metric and end-to-end boundary | Prevents proxy improvement from being reported as system benefit. |
| Failure model and limits | Defines what counts as valid, safe, feasible, or transferable. |

## Next matched comparison

Match workload, recall/accuracy, resident set, capacity, bandwidth, topology, migration cost, and tail latency.

## Current conclusion boundary

The evidence supports a provisional cross-conference mechanism relation. It does not establish that the direction is increasing, dominant, superior, or independently validated. The [direction review gate](../direction-review-gate-v1.md) records the remaining promotion work.
