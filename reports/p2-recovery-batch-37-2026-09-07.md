# P2 recovery routing batch 37 — 2026-09-07

This tranche continues the DAC frontier across learned multi-corner analysis,
control-flow auditing, FP/INT GEMM, early fault-tolerant surface-code economics,
CGRA mapping, ML-DSA side-channel reduction, physics-guided distributed ML,
process-reward RTL tuning, TEE ciphertext side channels, and standard-cell
library exploration.

| Priority | Paper ID | Title | Evidence needed before quantitative use |
|---:|---|---|---|
| 1 | `dac-2026-research1646` | Breaking the Tuning Barrier: Zero-Hyperparameters Yield Multi-Corner Analysis Via Learned Priors | PDK/corner corpus, learned-prior training split, corner metrics, generalization, runtime, and tuned baseline |
| 2 | `dac-2026-research1665` | CARAMEL: Boosting Device Utilization in Control Flow Auditing | Device/ISA, control-flow workload, audit threat model, utilization/coverage, overhead, and baseline auditor |
| 3 | `dac-2026-research1692` | CORE: Compact, Optimized, and Resource-Efficient Compute Engine for FP-INT GEMM Acceleration with Binary Coding Quantization | Models/tasks, quantization quality, FP/INT hardware, PPA/throughput/energy, and conventional GEMM baseline |
| 4 | `dac-2026-research1709` | Compilation Pipeline for Predicting Algorithmic Break-Even in an Early-Fault-Tolerant Surface Code Architecture | QEC code/noise model, architecture, break-even definition, compiler inputs, resource/fidelity estimates, and baseline |
| 5 | `dac-2026-research1712` | RAM-CGRA: Reachability-Aware Mapping for CGRAs | CGRA topology, kernel suite, reachability model, mapping objective, compile/runtime/PPA, and mapper baseline |
| 6 | `dac-2026-research1732` | Drop-In Masked Modular Reduction for ML-DSA: Cutting Side-Channel Cost in the Root-of-Trust | ML-DSA parameters, leakage/threat model, masking scheme, correctness/security, area/latency/power, and unmasked baseline |
| 7 | `dac-2026-research1741` | Two Teachers Better Than One: Hardware-Physics Co-Guided Distributed Scientific Machine Learning | Scientific workload/PDE, hardware/physics teachers, distributed topology, accuracy/convergence, communication/energy, and single-teacher baseline |
| 8 | `dac-2026-research1742` | StepPRM-RTL: Stepwise Process-Reward Guided LLM Fine-Tuning for Enhanced RTL Synthesis | RTL corpus, model/RL fine-tuning, reward/proof checks, PPA/correctness, training budget, and standard fine-tuning baseline |
| 9 | `dac-2026-research1764` | Ciphershield: Safeguarding DNN Inputs from Ciphertext Side-Channels in TEE | TEE/platform, ciphertext threat model, DNN traces, leakage metric, mitigation overhead, and unprotected baseline |
| 10 | `dac-2026-research1765` | L2L: Logic to Layout Exploration of Standard Cell Library Design | Cell/PDK corpus, logic/layout search, constraints, PPA/timing, convergence budget, and library-design baseline |

These are source-recovery priorities and condition checklists, not technical
rankings or temporal trend evidence.
