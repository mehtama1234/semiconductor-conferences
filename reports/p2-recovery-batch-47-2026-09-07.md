# P2 recovery routing batch 47 — 2026-09-07

This tranche continues the DAC frontier across CXL-tiered graph search, edge
LLM optimization, in-memory nonlinear quantization, 3D/3nm NoC DTCO, photonic
zero-knowledge proofs, encrypted databases, IR-drop-aware placement, drift-
resilient RRAM, heterogeneous mobile RAG, and FPGA-tool fault injection.

| Priority | Paper ID | Title | Evidence needed before quantitative use |
|---:|---|---|---|
| 1 | `dac-2026-research2268` | TierANNS: Scalable Graph-Based ANNS with CXL-Enabled Tiered Data Placement | CXL topology/devices, graph/index corpus, tiering policy, recall/latency/throughput/energy, and flat-memory baseline |
| 2 | `dac-2026-research2271` | Pefoo-L: A General Framework for Preconditioned Forward-Only Optimizer Enabling LLM Fine-Tuning on the Edge | LLM/task suite, optimizer/preconditioner, edge hardware, convergence/quality, memory/latency/energy, and standard-optimizer baseline |
| 3 | `dac-2026-research2282` | In-Memory ADC-Based Nonlinear Activation Quantization for Efficient In-Memory Computing | ADC/CIM device, activation/model suite, quantization error, accuracy, PPA/energy, and digital/exact activation baseline |
| 4 | `dac-2026-research2290` | Design Technology Co-Optimization for Network on Chip in High Performance CPUs at 3nm Node Using Monolithic 3D and Backside Interconnect Technologies | 3nm/3D process stack, CPU/NoC workloads, backside constraints, bandwidth/latency/power/area, and 2D/frontside baseline |
| 5 | `dac-2026-research2293` | Photomt: Accelerating Zero-Knowledge Proofs with a Photonic-Electronic Merkle Tree Engine | ZKP protocol/workload, photonic device/process, precision/security, proof latency/energy/area, and electronic baseline |
| 6 | `dac-2026-research2294` | PIMA-SecDB: Processing-in-Memory Acceleration for Fully Homomorphic Encryption Databases | FHE scheme/database workloads, PIM device, security model, correctness, query latency/throughput/energy, and CPU/FHE baseline |
| 7 | `dac-2026-research2297` | IR-Drop Aware Global Placement with PDN Optimization and GPU-Accelerated Analysis for Mitigating Global and Local IR-Drop | Technology/PDN corpus, IR-drop solver, placement constraints, timing/congestion/IR-drop, runtime, and placement baseline |
| 8 | `dac-2026-research2298` | VeRA+: Vector-Based Lightweight Compensation for Drift-Resilient RRAM In-Memory Computing | RRAM device/drift model, workloads, compensation policy, accuracy over time, area/energy/endurance, and uncompensated baseline |
| 9 | `dac-2026-research2300` | Hero: Adaptive Orchestration of Retrieval-Augmented Generation on Heterogeneous Mobile SoC | RAG models/corpora, SoC CPU/GPU/NPU resources, orchestration policy, answer quality, latency/energy/memory, and static pipeline baseline |
| 10 | `dac-2026-research2306` | Are They All Safe? Practical Fault Injection Attacks on FPGA Logic Synthesis Tools | FPGA tools/versions, attack/fault model, design corpus, exploit success and functional impact, reproducibility, and hardened-tool baseline |

These are source-recovery priorities and condition checklists, not technical
rankings or temporal trend evidence.
