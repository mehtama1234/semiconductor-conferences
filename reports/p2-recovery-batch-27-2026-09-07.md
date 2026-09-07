# P2 recovery routing batch 27 — 2026-09-07

This tranche continues the DAC frontier across TCAD surrogates, low-power test,
FPGA area recovery, secure CIM/PUF, encrypted inference, graph CIM, GPU circuit
simulation, robust quantum readout, edge DeepSeek inference, and MoE quantization.

| Priority | Paper ID | Title | Evidence needed before quantitative use |
|---:|---|---|---|
| 1 | `dac-2026-research1156` | FUSE-TCAD: A Diffusion-Based Multi-Field Surrogate for High-Fidelity TCAD Device Simulation | Device/PDK corpus, PDE fields, train/test split, diffusion model, fidelity/error, runtime, and conventional TCAD baseline |
| 2 | `dac-2026-research1180` | ESCAPE: Elegant Scan Chain Activity Probability Establishment for Programmable Low-Power LBIST | Scan/ATPG setup, activity model, fault coverage, power metric, process/tool, and LBIST baseline |
| 3 | `dac-2026-research1183` | Dynamic-Cost Area Recovery for Fracturable LUT-Based FPGAs | FPGA architecture, cost model, benchmark suite, timing/area constraints, recovery quality/runtime, and placer baseline |
| 4 | `dac-2026-research1185` | CPA-BNN: A Secure and Efficient CIM and PUF Architecture for BNN Accelerator | CIM/PUF device, threat model, BNN suite, security/accuracy, area/energy, and insecure/digital baseline |
| 5 | `dac-2026-research1187` | FBS: Accelerating CNN Inference over RNS-CKKS with Fewer Bootstrapping Sparsity | RNS-CKKS parameters, CNN models, sparsity/bootstrapping policy, accuracy/security, latency/energy, and dense FHE baseline |
| 6 | `dac-2026-research1194` | DIA-CIM: A Dynamic Iterative Aggregation Graph Neural Network and Its Hardware Co-Design for Energy-Efficient Graph Processing | Graph datasets, iterative aggregation, CIM technology, accuracy, throughput/energy, and GNN baseline |
| 7 | `dac-2026-research1196` | A Levelized Load-Balanced and Structure-Adaptive GPU LU Factorization Method for Circuit Simulation | Matrix/circuit suite, GPU model, pivoting/precision, load-balance method, accuracy/runtime/energy, and library baseline |
| 8 | `dac-2026-research1200` | NIAQ: Adaptive Non-Ideality-Aware Qubit Readout for Long-Term Accuracy | Qubit/device drift, non-ideality model, calibration interval, readout fidelity, hardware/runtime, and static calibration baseline |
| 9 | `dac-2026-research1206` | DSPE: An Energy-Efficient Edge Processor for Deepseek Inference with Merkletree-Based Incremental Pruning, Multi-Stage Boothing Lookup and Dynamic Adaptive Posit Processing | DeepSeek model/task, pruning/lookup/posit settings, edge process, accuracy/latency/energy, and full-precision baseline |
| 10 | `dac-2026-research121` | Exquant: Global Expert Ranking–guided Mixed-Precision Quantization for Efficient MoE Inference | MoE models/tasks, ranking/bit allocation, quality/perplexity, hardware/runtime, memory/latency, and uniform quantization baseline |

These are source-recovery priorities and condition checklists, not technical
rankings or temporal trend evidence.
