# P2 recovery routing batch 15 — 2026-09-07

This tranche routes ten ISCA records across MoE prefetching, vector/low-bit
inference, near-data processing, ANN search, VLM quantization, compression, and
multi-GPU memory systems.

| Priority | Paper ID | Title | Evidence needed before quantitative use |
|---:|---|---|---|
| 1 | `isca-2026-program-085` | STEP: Adaptive Spatio-Temporal Expert Prefetching for Low-Latency and Memory-Efficient MoE Inference | Models, routing traces, prefetch horizon/accuracy, GPU memory/interconnect, latency/P99, and no-prefetch baseline |
| 2 | `isca-2026-program-086` | EVA: Accelerating LLM Decoding via an Efficient Vector Quantization Architecture | Model/task suite, codebook/bit width, decode batch/sequence lengths, hardware, quality impact, and dense baseline |
| 3 | `isca-2026-program-087` | LoKA: Low-precision Kernel Applications for Recommendation Models At Scale | Recommendation models/datasets, precision, embedding tables, accelerator, accuracy/throughput/energy, and production baseline |
| 4 | `isca-2026-program-088` | Bringing Near Data Processing into the Low-Bit Floating-Point Era | NDP technology, FP formats, kernels, memory bandwidth, numerical error, area/energy, and host baseline |
| 5 | `isca-2026-program-089` | NasZip: Software and Hardware Co-design to Accelerate Approximate Nearest Neighbor Search with DIMM-based Near-Data Processing | ANN datasets/indexes, DIMM/NDP hardware, recall target, query batch, latency/energy, and CPU/GPU baseline |
| 6 | `isca-2026-program-090` | AQuant: Repurposing CODEC for VLM Acceleration via Adaptive Quantization | VLM models/tasks, codec mapping, bit allocation, quality metric, accelerator, latency/energy, and uniform-quantization baseline |
| 7 | `isca-2026-program-091` | Random-Access Hardware Sequence Compression | Data/trace classes, random-access guarantee, compression ratio, hardware/storage, decode latency/energy, and software baseline |
| 8 | `isca-2026-program-092` | Observability-aided GPU Memory Oversubscription | GPU/runtime, observability signals, workload traces, oversubscription ratio, page/migration overhead, and oblivious policy baseline |
| 9 | `isca-2026-program-093` | Coarse-Grained Duplication First, Fine-Grained Deduplication Later: Duplication-Centric Multi-GPU Memory Management | GPU topology, duplication/dedup policy, workloads, memory pressure, migration/communication cost, and conventional dedup baseline |
| 10 | `isca-2026-program-094` | Reducing Page Faults via Invalidation-based Mapping Propagation in Multi-GPU Systems | Address-space model, GPU count/interconnect, fault traces, invalidation protocol, overhead, and standard mapping propagation baseline |

These routes prioritize source recovery and condition extraction; they do not
establish performance rankings or temporal trends.
