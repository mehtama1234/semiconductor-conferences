# P2 recovery routing batch 2 — 2026-09-07

These ten DAC description-only records extend P2 routing into compiler,
verification, security, memory, and serving mechanisms. They are not yet
paper-level technical evidence.

| Priority | Paper ID | Title | Evidence needed before quantitative use |
|---:|---|---|---|
| 1 | `dac-2026-research083` | Dataflowgen: An MLIR-Based Compiler for Efficient Dataflow Accelerator Generation | MLIR version, accelerator targets, generated-kernel correctness, synthesis flow, benchmark suite, and baseline compiler |
| 2 | `dac-2026-research1080` | AccDRC: FPGA Acceleration for VLSI DRC with Cell-Aware Layout Partitioning | DRC rule deck, layout corpus, FPGA platform, partition correctness, baseline engine, and end-to-end runtime boundary |
| 3 | `dac-2026-research1085` | DM-MARK: Software and Hardware Co-Design of Watermarking Accelerator for Authorized Diffusion Model Usage on Edge Devices | Watermark threat model, diffusion models, quality metric, accelerator process, key/security assumptions, and baseline implementation |
| 4 | `dac-2026-research121` | Exquant: Global Expert Ranking–guided Mixed-Precision Quantization for Efficient MoE Inference | MoE models, expert-ranking calibration, bit allocation, accuracy/perplexity parity, hardware/runtime, and baseline quantizers |
| 5 | `dac-2026-research1291` | NASiC: 3D NAND-Based CAM-Selected Multibit CIM Architecture for Efficient On-Device Mixture-of-Experts LLM Inference | NAND/CAM process, endurance and retention assumptions, model/workload, precision, mapping policy, and measured versus simulated PPA |
| 6 | `dac-2026-research1419` | Duet: Exploiting High-Order Lossless Sparsity for Bit-Serial Transformer Acceleration via Distribution-Aware Pruning | Transformer suite, exact losslessness criterion, sparsity distribution, accelerator implementation, accuracy parity, and baseline hardware |
| 7 | `dac-2026-research1497` | Unveiling the Security Risks Driven by the Hardware Interrupts | Interrupt threat model, privilege/isolation assumptions, platforms, leakage metric, attack success criteria, and mitigations |
| 8 | `dac-2026-research1629` | AQR-HNSW: Accelerating Approximate Nearest Neighbor Search via Density-Aware Quantization and Multi-Stage Re-Ranking | Dataset/index scale, recall target, quantization error, HNSW parameters, hardware/runtime, and baseline ANN systems |
| 9 | `dac-2026-research2945` | Rememtier: Rethinking Memory Tiering for CXL-Based SSD via Large Granularity Memory Access | CXL/SSD hardware, tier capacities, access granularity, migration policy, workloads, tail latency, and baseline tiering system |
| 10 | `dac-2026-research3129` | HW-Router: Hardware-Aware Routing for Scalable Multi-LLM Serving | Model pool, routing objective, request mix, accelerator topology, quality/SLO constraints, and baseline router |

## Routing boundary

These IDs are selected for mechanism diversity and claim risk, not prevalence.
Official descriptions remain discovery evidence until a source with conditions is
captured and identity-matched.
