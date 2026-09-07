# P2 recovery routing batch 1 — 2026-09-07

This is the first ten-record recovery tranche from the 541 DAC records that
currently have official descriptions but no supplementary primary assessment.
The rows remain description-level until a manuscript, abstract, or identity-
matched artifact is recovered.

| Priority | Paper ID | Title | Evidence needed before quantitative use |
|---:|---|---|---|
| 1 | `dac-2026-research004` | Warp-STAR: High-Performance, Differentiable GPU-Accelerated Static Timing Analysis Through Warp-Oriented Parallel Orchestration | GPU model, design corpus, timing-error metric, baseline STA tool, parallelism, and runtime measurement boundary |
| 2 | `dac-2026-research012` | Moduplace: LLM-Assisted Modular PCB Placement via Preference-Optimized Constraint Graph Generation | Board/circuit suite, preference encoding, LLM/version, placement objective, comparison flow, and constraint-validity checks |
| 3 | `dac-2026-research032` | TDH-GNN: An Efficient Topology-Driven Accelerator for Dynamic Heterogeneous GNN | Graph datasets, topology distribution, accelerator process, sparsity/precision, baseline hardware, and end-to-end versus kernel scope |
| 4 | `dac-2026-research054` | GEMM-GS: Accelerating 3D Gaussian Splatting on Tensor Cores with GEMM-Compatible Blending | Scene set, image-quality metric, tensor-core precision, rendering resolution, baseline renderer, and quality/performance tradeoff |
| 5 | `dac-2026-research1081` | KEEP: A KV-Cache-Centric Memory Management System for Efficient Embodied Planning | Agent/task traces, context length, cache policy, GPU/memory platform, baseline serving stack, and planning-quality parity |
| 6 | `dac-2026-research130` | C2C-Explorer: An Exploration Framework for Chip-to-Chip Interconnect Architectures in LLM Cloud Computing Systems | Topology/search space, traffic traces, link assumptions, objective weights, simulator calibration, and baseline interconnects |
| 7 | `dac-2026-research1331` | Marlin: I/O-Efficient Prefix KV Cache Retrieval for Long-Prefix LLM Serving | Prefix/workload distribution, storage hierarchy, retrieval metric, serving baseline, batch/concurrency, and TTFT/throughput boundary |
| 8 | `dac-2026-research676` | CLUE-ECC: Low-Cost LPDDR6 Reliability Enhancement by Integrating System ECC with On-Die ECC | LPDDR6 organization, fault model, ECC code/budget, area/power/latency overhead, correction coverage, and baseline ECC |
| 9 | `dac-2026-research684` | Zipfloat: An Ultra-Fast and Lossless Floating-Point Compressor for LLM Inference Systems | Model/weight suite, exact losslessness definition, compression ratio, decode overhead, GPU integration, and quality invariance |
| 10 | `dac-2026-research976` | Greenllm: SLO-Aware Dynamic Frequency Scaling for Energy-Efficient LLM Serving | SLO/workload distribution, hardware power model, frequency policy, quality/latency constraints, baseline governor, and energy accounting |

## Routing rule

Recover in priority order, but do not infer that title prominence or queue order
means field prevalence. If a source is not recovered, retain the official
description as metadata/route evidence and record the missingness rather than
promoting its headline numbers.
