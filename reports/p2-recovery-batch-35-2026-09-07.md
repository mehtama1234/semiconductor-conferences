# P2 recovery routing batch 35 — 2026-09-07

This tranche continues the DAC frontier across maze routing, SRAM CIM dataflow,
GPU WCET, graph vector search, timing characterization, reconfigurable DNN
acceleration, 3D-NAND LLM inference, multiphysics thermal stress, robust driving
perception, and CPU-FPGA frequency measurement.

| Priority | Paper ID | Title | Evidence needed before quantitative use |
|---:|---|---|---|
| 1 | `dac-2026-research1534` | DRΛMA: Detailed Routing by a Versatile Maze Routing Algorithm | PDK/design corpus, routing rules, objective/constraints, DRC correctness, runtime/congestion, and router baseline |
| 2 | `dac-2026-research155` | AccelCIM: Systematic Dataflow Exploration for SRAM Compute-in-Memory Accelerator | SRAM-CIM device, kernel/model suite, dataflow space, accuracy, PPA/energy, and fixed-dataflow baseline |
| 3 | `dac-2026-research1552` | Beyond Exact: Tight WCET Analysis of GPU Kernels with Branch Divergence | GPU architecture, kernel suite, divergence model, WCET proof/validation, analysis cost, and prior bound |
| 4 | `dac-2026-research1560` | LOHA: A Latency-Optimized CPU-Storage Hybrid Architecture for Billion-Scale Graph-Based Vector Similarity Search | Graph/index datasets, CPU/storage hardware, query/recall target, placement/caching, latency/energy, and CPU/GPU baseline |
| 5 | `dac-2026-research1562` | PG-GNN: Physics-Guided Graph Neural Network for Cell Timing Library Characterization | Cell/PDK corpus, physics features, train/test split, timing error, transfer, runtime, and SPICE/table baseline |
| 6 | `dac-2026-research1569` | FILCO: Flexible Composing Architecture with Real-Time Reconfigurability for DNN Acceleration | FPGA/CGRA target, model suite, reconfiguration latency, precision, throughput/energy/area, and fixed-function baseline |
| 7 | `dac-2026-research1570` | NVLLM: A 3D NAND-Centric Architecture Enabling Edge On-Device LLM Inference | NAND/device stack, LLM models/quantization, endurance, dataflow, latency/energy/quality, and edge GPU/CPU baseline |
| 8 | `dac-2026-research158` | Neural Domain Decomposition for Scalable Multi-Physics: Chip-Scale Thermal-Stress Analysis | PDE/material corpus, domain decomposition, neural model, accuracy/stability, scaling/runtime, and numerical solver baseline |
| 9 | `dac-2026-research1585` | DFA-DRIVE: A Cross-Layer Delay Fault Analysis and Optimization Framework for Robust Multi-Task Driving Perception | Driving datasets/tasks, fault model, cross-layer mitigation, perception quality, latency/energy, and unprotected baseline |
| 10 | `dac-2026-research1587` | CelestialEye: A Synergistic CPU-FPGA Engine for Accurate Frequency Measurement in High-Speed Data Streams | Signal/workload traces, frequency range, CPU-FPGA design, accuracy/latency/power, and software baseline |

These are source-recovery priorities and condition checklists, not technical
rankings or temporal trend evidence.
