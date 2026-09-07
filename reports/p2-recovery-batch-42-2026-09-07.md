# P2 recovery routing batch 42 — 2026-09-07

This tranche continues the DAC frontier across RTL simulation, approximate DCiM,
floorplanning, 4D/3D Gaussian splatting, edge sparsity, routability/track
assignment, multi-die FPGA HLS, GPU fuzzing, and fault-tolerant AI scheduling.

| Priority | Paper ID | Title | Evidence needed before quantitative use |
|---:|---|---|---|
| 1 | `dac-2026-research2011` | Dart: Towards Redundancy-Free RTL Simulation via DAG-Driven Execution | RTL/workload suite, DAG construction, redundancy definition, correctness/determinism, runtime/memory, and simulator baseline |
| 2 | `dac-2026-research2014` | OpenACMv2: An Accuracy-Constrained Co-Optimization Framework for Approximate DCiM | DCiM device/process, model/task suite, accuracy constraint, mapping/optimization, PPA/energy, and exact baseline |
| 3 | `dac-2026-research2024` | Rectilinear Soft Module Floorplanning via Differentiable Polygon Shaping Model and Flow-Based Legalization | Floorplan/PDK corpus, polygon model, constraints, wirelength/congestion/timing, runtime, and floorplanner baseline |
| 4 | `dac-2026-research2027` | Relay-GS: Reusing Temporal Sort Information for 4D Gaussian Splatting Acceleration | 4D scene/video suite, temporal-sort reuse, quality metric, GPU/hardware target, frame rate/energy, and standard renderer |
| 5 | `dac-2026-research2030` | On-Demand Multi-Task Sparsity for Efficient Large-Model Deployment on Edge Devices | Models/tasks, dynamic sparsity policy, edge hardware, quality/latency/energy, adaptation overhead, and static sparsity baseline |
| 6 | `dac-2026-research2036` | PipeGS: Unlocking 3DGS Pipeline Parallelism via Hierarchical Reuse and Dynamic Partitioning | Scenes, pipeline topology, reuse/partition policy, image quality, throughput/memory/energy, and serial baseline |
| 7 | `dac-2026-research2037` | LRTA: Routability-Driven 3D-Aware Track Assignment with Layer Reassignment | 3D/PDK corpus, track/layer constraints, routability metric, timing/congestion/DRC, runtime, and router baseline |
| 8 | `dac-2026-research2048` | Efficient HLS Accelerator Floorplan on Multi-Die FPGA Aided by Graph Neural Networks | Multi-die FPGA architecture, HLS/design corpus, GNN training split, PPA/routability, runtime, and heuristic baseline |
| 9 | `dac-2026-research2056` | GPU-Fuzz: Finding Memory Errors in Deep Learning Frameworks | Framework/GPU versions, operator corpus, fault/oracle model, bug validation, coverage/runtime, and fuzzing baseline |
| 10 | `dac-2026-research2057` | Accshield: Operator-Aware Robust Scheduling for Fault-Tolerant AI Accelerators | Accelerator/fault model, operators/workloads, scheduling policy, correctness/SLO, overhead/energy, and non-fault-tolerant baseline |

These are source-recovery priorities and condition checklists, not technical
rankings or temporal trend evidence.
