# P2 recovery routing batch 24 — 2026-09-07

This tranche routes ten DAC 2026 records selected from the existing priority-3
queue frontier. It covers timing analysis, PCB placement, characterization,
heterogeneous GNNs, hyper-dimensional computing, Gaussian splatting, RTL
simulation, package power delivery, graph representation learning, and dataflow
generation.

| Priority | Paper ID | Title | Evidence needed before quantitative use |
|---:|---|---|---|
| 1 | `dac-2026-research004` | Warp-STAR: High-Performance, Differentiable GPU-Accelerated Static Timing Analysis Through Warp-Oriented Parallel Orchestration | Circuit/benchmark suite, GPU model, differentiability method, timing accuracy, runtime/memory, and STA baseline |
| 2 | `dac-2026-research012` | Moduplace: LLM-Assisted Modular PCB Placement via Preference-Optimized Constraint Graph Generation | Board corpus, constraints, LLM/training setup, placement quality, routability/runtime, and human/tool baseline |
| 3 | `dac-2026-research025` | Powerpath: Internal-Probe-Free Search Interval Reduction for Efficient Statistical Sequential Constraint Characterization | Process/PDK, statistical model, probe assumptions, accuracy/confidence, sample count/runtime, and characterization baseline |
| 4 | `dac-2026-research032` | TDH-GNN: An Efficient Topology-Driven Accelerator for Dynamic Heterogeneous GNN | Graph workloads, dynamic topology, hardware target, accuracy, throughput/energy, and GNN accelerator baseline |
| 5 | `dac-2026-research052` | Brain-Like Hyper-Dimensional Graph Learning System with Hardware-Efficient Adaptive Sparsity | Datasets/tasks, HDC representation, sparsity policy, hardware/device, accuracy/energy, and dense baseline |
| 6 | `dac-2026-research054` | GEMM-GS: Accelerating 3D Gaussian Splatting on Tensor Cores with GEMM-Compatible Blending | Scene suite, quality metric, tensor-core mapping, precision, frame rate/energy, and standard rasterizer baseline |
| 7 | `dac-2026-research068` | A Differentiable Approach to Task Graph Partitioning: A Case Study in RTL Simulation | RTL/workload suite, partition objective, differentiable surrogate, simulator/tool, runtime/accuracy, and heuristic baseline |
| 8 | `dac-2026-research073` | BLADE: Bi-Level Bayesian Optimization for Metal-Density-Constrained Multi-Layer Package Power/ground Plane Synthesis | Package stack/PDK, density/PDN constraints, BO budget, electrical/thermal metrics, convergence, and conventional optimizer baseline |
| 9 | `dac-2026-research080` | Beyond Flat Netlist: Hierarchical Graph Representation Learning for Scalable Analysis of Sequential Circuits | Circuit corpus, hierarchy representation, prediction task, training split, accuracy/runtime, and flat-graph baseline |
| 10 | `dac-2026-research083` | Dataflowgen: An MLIR-Based Compiler for Efficient Dataflow Accelerator Generation | MLIR/tool versions, model/kernel suite, generated targets, correctness, PPA/runtime, and hand-written/compiler baselines |

These are source-recovery priorities and condition checklists, not technical
rankings or temporal trend evidence.
