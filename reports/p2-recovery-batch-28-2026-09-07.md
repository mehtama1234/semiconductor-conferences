# P2 recovery routing batch 28 — 2026-09-07

This tranche continues the DAC frontier across clock-tree synthesis, capacitance
extraction, analog CIM for UAVs, point-cloud sampling, graph sparsity, distributed
matrix multiplication, heterogeneous edge SoCs, optical synthesis, and dynamic
shape neural networks.

| Priority | Paper ID | Title | Evidence needed before quantitative use |
|---:|---|---|---|
| 1 | `dac-2026-research1211` | DCTS: Differentiable Clock Tree Synthesis Based on Probabilistic Graphical Model | Design corpus/PDK, clock constraints, probabilistic model, skew/power/area, convergence budget, and CTS baseline |
| 2 | `dac-2026-research1222` | Attentioncap: Transformer Based Capacitance Matrix Learning Toward Full-Chip Extraction | Layout/PDK corpus, matrix target, train/test split, extraction accuracy, runtime/memory, and extraction baseline |
| 3 | `dac-2026-research1224` | Capbench: A Multi-PDK Dataset for Machine-Learning-Based Post-Layout Capacitance Extraction | PDK/process diversity, labels/measurement method, split policy, leakage controls, benchmark metrics, and licensing |
| 4 | `dac-2026-research1233` | RM-CIMA: An Analog Computing-in-Memory Accelerator for a Robust UAV Trajectory Tracking Framework | UAV dynamics/tasks, analog CIM device, controller precision/stability, area/energy/latency, and digital baseline |
| 5 | `dac-2026-research124` | Flashfps: Efficient Farthest Point Sampling for Large-Scale Point Clouds via Pruning and Caching | Point-cloud datasets/scale, pruning error, cache/memory, hardware/software target, latency/energy, and exact FPS baseline |
| 6 | `dac-2026-research1242` | BSGCN: Taming Diverse Sparsities in GCNs via Adaptive Band-Segmentation and Tailored Caching | Graph suite/sparsity distributions, band policy, cache hardware, accuracy, throughput/energy, and sparse-GCN baseline |
| 7 | `dac-2026-research1256` | DAP: A Software/hardware Co-Design for Accelerating Multi-Chip-Based Distributed Sparse-Dense Matrix Multiplication | Matrix/workload suite, chip topology, communication model, sparsity, scaling/energy, and software baseline |
| 8 | `dac-2026-research1267` | MATCHA: Efficient Deployment of Deep Neural Networks on Multi-Accelerator Heterogeneous Edge SoCs | SoC/accelerator mix, model suite, partition/runtime policy, accuracy, latency/energy, and single-accelerator baseline |
| 9 | `dac-2026-research1268` | Bident: Optical Logic Synthesis via Optimal Configuration of Binary-Combiner Trees | Optical device/process, logic corpus, synthesis constraints, correctness, area/power/delay, and electronic baseline |
| 10 | `dac-2026-research127` | Optimizing Dynamic-Shape Neural Networks: A Unified Approach to Adaptive Tuning | Models/shape traces, tuning algorithm, hardware/runtime, accuracy, latency/energy, adaptation overhead, and static tuning baseline |

These are source-recovery priorities and condition checklists, not technical
rankings or temporal trend evidence.
