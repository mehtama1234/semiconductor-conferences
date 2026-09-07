# P2 recovery routing batch 67 — 2026-09-07

This DAC-specific tranche covers reserved-opcode emulation detection, streaming
VLM retrieval, stage-aware MoE expert management, sparse video-diffusion
attention, Apple-Silicon TLB side channels, processor upper-bound modeling,
post-layout design-evolution graphs, Versal GEMM co-optimization, zoned-storage
write reordering, and near-memory RAG.

| Priority | Paper ID | Title | Evidence needed before quantitative use |
|---:|---|---|---|
| 1 | `dac-2026-research663` | Emudrop: A Minimalistic, Hardware-Based Emulation Detection Approach Through Intel Reserved Opcodes | Intel CPU/platform, emulation threat model, opcode behavior, detection accuracy/overhead, and software baseline |
| 2 | `dac-2026-research670` | LiveVLM: Efficient Online Video Understanding via Streaming-Oriented KV Cache and Retrieval | VLM/video suite, streaming/cache/retrieval policy, quality, latency/memory/energy, and offline baseline |
| 3 | `dac-2026-research675` | SAEM: Stage-Aware Expert Management for Memory-Efficient MoE Inference in Chain-of-Thought Reasoning | CoT/MoE models, stage policy, memory limit, quality, latency/throughput/energy, and standard expert manager baseline |
| 4 | `dac-2026-research680` | SPADE: An Input-Adaptive Sparse Attention Engine for Fast Video Diffusion Models Inference | Video-diffusion suite, sparsity policy, accelerator target, quality, frame latency/energy, and dense baseline |
| 5 | `dac-2026-research681` | Mistletunnel: Attacking KASLR on Apple M-Series Silicon with a Novel TLB Side Channel | Apple CPU/platform, TLB channel/threat model, victim/key workload, success/noise/query budget, and mitigation baseline |
| 6 | `dac-2026-research690` | Idealsim: Efficient Ideal Scenario Modeling for Processor Upper-Bound Performance Analysis | Processor/microarchitecture, workload suite, idealization assumptions, bound accuracy, runtime, and detailed simulator baseline |
| 7 | `dac-2026-research692` | DiffDEG: Diffusion-Enhanced Design Evolution Graph Representation Learning for Post-Layout Optimization | Layout/design corpus, graph/diffusion model, optimization target, PPA/timing/DRC, training split, and prior optimizer baseline |
| 8 | `dac-2026-research693` | MALIWAN: Performance and Energy Efficiency Co-Optimization of GEMM on Versal ACAP Architectures | Versal device, GEMM suite, mapping/tuning policy, correctness, throughput/energy/area, and vendor/library baseline |
| 9 | `dac-2026-research698` | Freezone: An On-Device Out-of-Order Writes Reordering Scheme for Consumer Zoned Storage | Zoned-storage device, write workloads, reordering policy, correctness, latency/throughput/endurance, and ordered baseline |
| 10 | `dac-2026-research701` | RAGNMP: Leveraging Elimination Tree to Accelerate RAG with Near-Memory Processing | RAG models/corpora, near-memory device, elimination-tree policy, answer quality, latency/energy, and CPU/GPU baseline |

These are DAC-specific source-recovery priorities and condition checklists, not
technical rankings or temporal trend evidence.
