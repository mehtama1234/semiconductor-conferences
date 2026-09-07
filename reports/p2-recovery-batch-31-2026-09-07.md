# P2 recovery routing batch 31 — 2026-09-07

This tranche continues the DAC frontier across prefix-KV retrieval, video
enhancement, zero-knowledge tracing, emulation scheduling, elastic LLM memory,
processor fault localization, LLM-generated assertions, 3D near-memory video
generation, graph PIM, and Apple-SoC cache side channels.

| Priority | Paper ID | Title | Evidence needed before quantitative use |
|---:|---|---|---|
| 1 | `dac-2026-research1331` | Marlin: I/O-Efficient Prefix KV Cache Retrieval for Long-Prefix LLM Serving | Models/prefix traces, storage/cache hierarchy, retrieval policy, SLO/throughput/latency, and baseline |
| 2 | `dac-2026-research1334` | PEL: A 4K@120FPS Palette-Based Enhancement Layer Validated with JPEG XS Achieving 18.13% Bdrate Reduction | Video corpus/codec settings, quality metric, hardware pipeline, bitrate/frame-rate/power, and JPEG XS baseline |
| 3 | `dac-2026-research1338` | ZK-Tracer: A High-Performance Heterogeneous Accelerator for Zero-Knowledge VM Trace Generation | ZK VM/protocol, workloads/field parameters, CPU/accelerator split, proof correctness, throughput/latency/area, and software baseline |
| 4 | `dac-2026-research1348` | TOB-Sched: Topological Order Balancing-Driven Static Scheduling for Processor-Based Emulation | RTL/workload suite, emulation platform, topology/balance objective, timing/throughput, and scheduler baseline |
| 5 | `dac-2026-research1351` | eLLM: Elastic Memory Management Framework for Efficient LLM Serving | Models/request traces, memory tiers, elasticity policy, fragmentation/migration, throughput/SLO/energy, and allocator baseline |
| 6 | `dac-2026-research1355` | Debug Like a Human: Scaling LLM-Based Fault Localization to Processor Design via Block-Level Instruction-Oriented Slicing | Processor RTL/bug corpus, LLM/model/version, slicing method, localization metric, reproducibility, and existing debugger baseline |
| 7 | `dac-2026-research1356` | ChatSVA: Bridging SVA Generation for Hardware Verification via Task-Specific LLMs | RTL/assertion corpus, LLM/task prompts, syntax/formal correctness, coverage, cost/runtime, and human/tool baseline |
| 8 | `dac-2026-research1357` | 3D-DuRA: Accelerating Next-Resolution Generation via 3D Near/in-Memory Architecture with Dual-Ring Sparse Attention | Video/diffusion models, quality metric, memory technology, sparse attention, area/energy/latency, and GPU baseline |
| 9 | `dac-2026-research1365` | Bringing Graphs Closer to Memory: Compiler-Driven Data Transfer Reduction in the PIM Accelerator | Graph suite, PIM device, compiler transformations, data movement metric, accuracy/performance/energy, and hand-tuned baseline |
| 10 | `dac-2026-research1373` | Slcross: Cross-Component System-Level Cache Side-Channel Attacks on Apple M2 SoC | M2 hardware/OS, attacker model, cross-component channel, leakage metric, reproducibility, and mitigations |

These are source-recovery priorities and condition checklists, not technical
rankings or temporal trend evidence.
