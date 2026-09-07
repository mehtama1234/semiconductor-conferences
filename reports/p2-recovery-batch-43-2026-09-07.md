# P2 recovery routing batch 43 — 2026-09-07

This tranche continues the DAC frontier across single-detector knowledge
distillation, robotics diffusion accelerators, ZNS graph memory, confidential-VM
migration, secure CIM, CodeLLM FPGA DSE, FPGA debugging, generative inverse
lithography, piecewise activations, and memristor-memory NoCs.

| Priority | Paper ID | Title | Evidence needed before quantitative use |
|---:|---|---|---|
| 1 | `dac-2026-research2058` | SharedKD: Gradient-Guided Dynamic Student Discovery Inside a Single 3D Object Detector | 3D detector/dataset, teacher/student policy, training budget, detection quality, latency/energy, and fixed-student baseline |
| 2 | `dac-2026-research2071` | SpRDA: An Efficient Sparse Accelerator for Robotics Diffusion Model | Robotics/diffusion tasks, sparsity pattern, accelerator target, action/image quality, latency/energy, and dense baseline |
| 3 | `dac-2026-research2074` | Z-Paraswap: Co-Optimizing ZNS Parallelism and Swapping for Heterogeneous Graph Neural Network | ZNS/storage hardware, graph workloads, swapping/parallelism policy, quality/latency/endurance, and conventional storage baseline |
| 4 | `dac-2026-research2079` | Towards Practical Live Migration for Heterogeneous Confidential Virtual Machines | TEE/VM platforms, workload/state size, migration protocol, security/availability, downtime/bandwidth, and conventional migration baseline |
| 5 | `dac-2026-research208` | S2CIM: A Secure-Computation and Secure-Storage Compute-in-Memory Architecture with Circuit-Algorithm Co-Design for Efficient and Trustworthy Edge Inference | CIM device, cryptographic/storage threat model, model suite, accuracy/security, PPA/energy, and unprotected baseline |
| 6 | `dac-2026-research2083` | CHiRM-DSE: CodeLLM-Based Hierarchical and Rule-Mining Guided DSE for FPGA Accelerators | FPGA/design corpus, CodeLLM/version, rule-mining/search budget, PPA/correctness, and DSE baseline |
| 7 | `dac-2026-research2085` | Prelude: Priming-Guided State Reconstruction for Efficient FPGA Processor Debugging | FPGA processor/bug corpus, state reconstruction method, correctness/coverage, trace/runtime overhead, and debugger baseline |
| 8 | `dac-2026-research209` | Pushing the Limits of Inverse Lithography with Generative Reinforcement Learning | Lithography process/pattern corpus, RL policy/reward, fidelity/mask metrics, runtime, and ILT baseline |
| 9 | `dac-2026-research2094` | DAPA: Distribution Aware Piecewise Activation Functions for On-Device Transformer Inference and Training | Transformer models/tasks, activation approximation, accuracy, edge hardware, latency/energy, and exact activation baseline |
| 10 | `dac-2026-research2098` | PiMM-NoC: Process-in-Memristor-Memory NoC with RL Mapping Framework for Versatile AI Models | Memristor/NoC device, model suite, RL mapping, variation/security, throughput/energy/area, and conventional NoC baseline |

These are source-recovery priorities and condition checklists, not technical
rankings or temporal trend evidence.
