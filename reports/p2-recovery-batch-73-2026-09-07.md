# P2 recovery routing batch 73 — 2026-09-07

This DAC-specific tranche covers quantum circuit synthesis, NPU reliability,
electromigration/IR-drop modeling, CXL tiered memory, MoE offload security,
3D-IC thermal simulation, digital compute-in-memory exploration, LLM-guided FPGA
HLS optimization, near-memory communication bounds, and fused dot-product
acceleration.

| Priority | Paper ID | Title | Evidence needed before quantitative use |
|---:|---|---|---|
| 1 | `dac-2026-research031` | Quantum Circuit Synthesis Using an Exact T Library | Circuit suite, exact-library construction, qubit/connectivity constraints, gate count/depth, fidelity, runtime, and synthesis baseline |
| 2 | `dac-2026-research043` | Strix: Re-Thinking NPU Reliability from a System Perspective | NPU architecture, fault model, workloads, resilience policy, accuracy/availability/latency/energy, and reliability baseline |
| 3 | `dac-2026-research046` | GEMIR: Graph-Based Joint Modeling of Electromigration and IR Drop for Power Grid | PDK/layout corpus, current/thermal conditions, graph model, EM/IR error, runtime, and signoff baseline |
| 4 | `dac-2026-research1028` | Ctxmem: OS-Hardware Co-Designed Tiered Memory with DRAM-SSD Hybrid CXL Devices | CXL topology, workloads, tiering policy, capacity/latency/bandwidth, fault behavior, and memory baseline |
| 5 | `dac-2026-research1054` | Icarus's Wings: Disabling MoE Offloading Acceleration via a Universal Hidden Prefix Attack | Model/checkpoint suite, threat access, attack success, overhead, robustness, and defended/offload baselines |
| 6 | `dac-2026-research1065` | FLASH3D: A Fast Layered Analytical Solver for High-Accuracy Steady-State Thermal Simulation of 3D ICs | 3D-IC stack/cooling conditions, solver assumptions, temperature error, runtime/memory, and numerical baseline |
| 7 | `dac-2026-research1101` | HYPER-CIM: Hierarchical Predictive Exploration and Realizable Design Flow for High-Efficient Digital CIM | CIM technology/design space, predictor training data, realizability constraints, PPA/error, search budget, and exploration baseline |
| 8 | `dac-2026-research1110` | LLM-Based Automatic Architecture Optimization for AI Model HLS Implementation on FPGA | Model/HLS corpus, LLM prompts/tools, FPGA target, synthesis constraints, QoR/correctness, and human/optimizer baseline |
| 9 | `dac-2026-research1113` | Achieving Intra- and Inter-Operator Communication Lower Bounds in Near-Memory Processing | NMP architecture, operator/workload suite, lower-bound assumptions, communication volume, performance/energy, and prior mapping baseline |
| 10 | `dac-2026-research1182` | Fusedot: A Multiplication-Fused Dot Product Accelerator for Efficient LLM Inference | LLM/operator suite, numeric format, hardware implementation, accuracy, throughput/latency/energy/area, and unfused baseline |

These are DAC-specific source-recovery priorities and condition checklists, not
technical rankings or temporal trend evidence.
