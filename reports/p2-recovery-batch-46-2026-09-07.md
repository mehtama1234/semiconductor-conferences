# P2 recovery routing batch 46 — 2026-09-07

This tranche continues the DAC frontier across microscaling, post-quantum edge
security, GPU hypergraph partitioning, wafer-scale cost modeling, CPU-GPU MoE
execution, multi-vector retrieval, learned approximate arithmetic, voltage-based
side-channel analysis, stochastic computing, and encrypted sparse multiplication.

| Priority | Paper ID | Title | Evidence needed before quantitative use |
|---:|---|---|---|
| 1 | `dac-2026-research2207` | PRISM: Priority Aware Shared Scale Microscaling Format for 4-Bit Quantization | Microscaling format/bit allocation, model and task suite, accuracy, hardware support, latency/energy, and fixed-scale baseline |
| 2 | `dac-2026-research2216` | Safe-IoT: A Memory-Efficient HW/SW Co-Designed ML-DSA Accelerator for IoT Edge Devices | ML-DSA parameter set, IoT platform, memory hierarchy, security/correctness, latency/energy/area, and software/hardware baseline |
| 3 | `dac-2026-research223` | Ihyperg: Incremental Hypergraph Partitioning on GPU | Hypergraph workloads/update model, GPU, partition-quality objective, update throughput, memory/energy, and static/CPU baseline |
| 4 | `dac-2026-research2230` | WSC-Cost: An Accurate Cost Modeling Framework for Wafer-Scale Chips | Wafer-scale architecture, cost components, calibration data, prediction error, design-space scope, and prior cost-model baseline |
| 5 | `dac-2026-research2235` | CoX-MoE: Coalesced Expert Execution for High-Throughput MoE Inference with AMX-Enabled CPU-GPU Co-Execution | MoE models, CPU/GPU/AMX platforms, coalescing policy, quality, throughput/latency/energy, and CPU-only/GPU-only baseline |
| 6 | `dac-2026-research2243` | MIRAGE: Runtime Scheduling for Multi-Vector Image Retrieval with Hierarchical Decomposition | Retrieval corpus/query workload, vector decomposition, runtime scheduler, recall/latency/energy, and flat-index baseline |
| 7 | `dac-2026-research2245` | TRAM: Training Approximate Multiplier Structures for Low-Power AI Accelerators | Approximate multiplier search/training objective, model suite, error/accuracy, target hardware, PPA/energy, and exact-multiplier baseline |
| 8 | `dac-2026-research2254` | Instruction-Level Side-Channel Disassembly on Modern Complex CPUs via Voltage Waveform Analysis | CPU/microarchitecture, waveform acquisition, instruction corpus, decoder accuracy, noise/sample budget, and prior side-channel baseline |
| 9 | `dac-2026-research2256` | ALOHA: Area-Efficient and Low-Power Stochastic Computing with Hammersley Sequences | Stochastic number representation, workload suite, hardware/process, numerical error, area/energy/throughput, and conventional stochastic baseline |
| 10 | `dac-2026-research2265` | Sparsee: Unlocking Sparsities in Encrypted Sparse Matrix Multiplication via Hardware-Software Co-Design | Encryption scheme/security model, sparse matrices, leakage policy, correctness, throughput/energy/area, and dense/encrypted baseline |

These are source-recovery priorities and condition checklists, not technical
rankings or temporal trend evidence.
