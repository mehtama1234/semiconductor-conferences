# P2 recovery routing batch 44 — 2026-09-07

This tranche continues the DAC frontier across quantum-error-correction
hardware, GPU sparse linear algebra, secure biochips, graph processing-in-memory,
neuro-symbolic hardware, personalized CIM, side-channel monitoring, circuit
simulation, wafer-scale communication, and 3D placement.

| Priority | Paper ID | Title | Evidence needed before quantitative use |
|---:|---|---|---|
| 1 | `dac-2026-research210` | Cryozip: An Efficient Cryogenic Compressor for Quantum Error Correction Syndromes | QEC code/syndrome workload, cryogenic device and temperature, compression mechanism, decoding fidelity, throughput/energy/area, and uncompressed baseline |
| 2 | `dac-2026-research2105` | Acc-SpMV: Accelerating General-Purpose Sparse Matrix-Vector Multiplication with GPU CUDA Cores | Matrix suite and sparsity, GPU model, kernel/data layout, correctness, throughput/energy, and optimized-library baseline |
| 3 | `dac-2026-research2107` | ODBP: Obfuscation Design Approach for Biochemical Protocols in Continuous-Flow Microfluidic Biochips | Biochip process model, threat/obfuscation model, protocol corpus, correctness/security, area/time/yield, and unobfuscated baseline |
| 4 | `dac-2026-research2123` | Dypamear: Efficient and Scalable Dynamic Graph Pattern Mining on Practical Processing-in-Memory Architecture | Dynamic graph workloads, PIM device/prototype, pattern definitions, result correctness, throughput/energy, and CPU/GPU baseline |
| 5 | `dac-2026-research2125` | Overmind NSA: A Unified Neuro-Symbolic Computing Architecture with Approximate Nonlinear Activations and Preemptive Memory Bypass | Neuro-symbolic models/tasks, approximation/error policy, architecture and memory system, accuracy, PPA/energy, and exact-arithmetic baseline |
| 6 | `dac-2026-research2128` | Enabling Robust On-Device Personalization via Pulse-Based Mapping and Noise Suppression for Non-Ideal CIM Architecture | CIM device/process, personalization tasks, pulse mapping/noise model, accuracy and convergence, endurance/energy, and ideal-device baseline |
| 7 | `dac-2026-research213` | Exploiting Per-Core Leakage: Electromagnetic Side-Channel Monitoring of Multicore Architectures | CPU/platform, leakage acquisition setup, threat model, workload/key corpus, detection/localization metrics, sample budget, and prior side-channel baseline |
| 8 | `dac-2026-research2131` | EastPCG: An Efficient and Self-Tuning Graph Sparsification Based PCG Solver for Circuit Simulation | Circuit matrices, sparsification policy, solver tolerance, convergence/error, runtime/memory/energy, and conventional PCG baseline |
| 9 | `dac-2026-research2132` | Hyperwafer: Communication-Aware Sparse Matrix Multiplication on Wafer-Scale Chips | Wafer-scale platform/topology, sparse matrix suite, communication model, numerical correctness, throughput/energy, and non-wafer baseline |
| 10 | `dac-2026-research2133` | Toward True-3D Timing-Driven Analytical Global Placement for Mixed-Size Face-to-Face 3D ICs | 3D technology/PDK and benchmark suite, timing model, face-to-face constraints, wirelength/congestion/timing/DRC, runtime, and placer baseline |

These are source-recovery priorities and condition checklists, not technical
rankings or temporal trend evidence.
