# P2 recovery routing batch 30 — 2026-09-07

This tranche continues the DAC frontier across hypergraph partitioning, thermal
and kernel-aware inference, diffusion quantization, variation-tolerant analog
inference, quantum placement/compilation, placement/sizing optimization, chiplet
thermal modeling, RowHammer attacks, and PIM scheduling.

| Priority | Paper ID | Title | Evidence needed before quantitative use |
|---:|---|---|---|
| 1 | `dac-2026-research1300` | Compart: Community-Guided Post-Coarsening for High-Quality Hypergraph Partitioning | Hypergraph corpus, community/coarsening method, cut/balance objective, runtime, and partitioner baselines |
| 2 | `dac-2026-research1302` | Active Imitation Learning for Thermal- and Kernel-Aware LFM Inference on 3D S-NUCA Many-Cores | Many-core/thermal model, LFM workload, expert traces, policy/active-learning budget, accuracy/latency/energy, and static baseline |
| 3 | `dac-2026-research1307` | MASQ: Accelerating Masked Diffusion via Stage-Wise Multi-Precision Quantization | Diffusion models/tasks, stages/bit widths, quality metric, hardware target, latency/energy, and uniform-precision baseline |
| 4 | `dac-2026-research1308` | SDM: A Variation-Tolerant Soft Decision Machine with In-Memory Sigmoid Computation | Device variation model, CIM circuit, datasets, accuracy/error, calibration, area/energy, and digital baseline |
| 5 | `dac-2026-research1312` | Agent-Per-Qubit: Automated Qubit Placement for Fault-Tolerant Quantum Computing | QEC code/circuits, hardware topology, placement objective, compiler/runtime, fidelity/depth, and placement baselines |
| 6 | `dac-2026-research1316` | Search Smarter, Not Harder: A Scalable, High-Quality Zoned Neutral Atom Compiler | Neutral-atom hardware, circuit suite, zone constraints, search budget, fidelity/depth/runtime, and compiler baseline |
| 7 | `dac-2026-research1317` | HyPAS: A Hybrid Optimization Framework for Placement and Sizing Co-Optimization | Circuit/PDK corpus, objective/constraints, hybrid optimizer, PPA/timing, convergence budget, and commercial/heuristic baseline |
| 8 | `dac-2026-research132` | Legotherm: Modular and Reusable Thermal Model for Chiplet-Based Heterogeneous Integration | Package/chiplet stack, thermal solver/calibration, workloads, accuracy/runtime, and detailed-model baseline |
| 9 | `dac-2026-research1320` | Shooting Falcon with One Fault: A Practical Rowhammer-Based Fault Attack Against Falcon | DRAM/platform, Falcon implementation, attacker model, fault/recovery probability, mitigations, and security disclosure boundary |
| 10 | `dac-2026-research1322` | Keeping PIM Busy: Eliminating Execution Overheads for Full Throughput | PIM technology, workload/command traces, scheduling/overhead model, utilization/energy, and conventional scheduler baseline |

These are source-recovery priorities and condition checklists, not technical
rankings or temporal trend evidence.
