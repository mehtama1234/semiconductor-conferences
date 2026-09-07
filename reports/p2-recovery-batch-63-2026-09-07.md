# P2 recovery routing batch 63 — 2026-09-07

This DAC-specific tranche covers surrogate-guided chiplet accelerator
exploration, processing-using-DRAM GMV, point-cloud CAM search, analog layout
automation, activity-aware RTL simulation, temporal/spatial cache partitioning,
in-storage version search, disaggregated-memory replication, analog graph
representation learning, and CPU-GPU MoE balance.

| Priority | Paper ID | Title | Evidence needed before quantitative use |
|---:|---|---|---|
| 1 | `dac-2026-research399` | ChiSER: Surrogate-Enhanced Resource-Aware Exploration of Chiplet-Based Deep Neural Network Accelerators | Chiplet/package/process, DNN suite, surrogate calibration, resource constraints, PPA/thermal/runtime, and search baseline |
| 2 | `dac-2026-research401` | PAGE: Processing-Using-DRAM Architecture-Circuits Co-Optimization for Efficient Acceleration of General Matrix-Vector Multiplication | DRAM device/process, GMV workloads, circuit/architecture co-design, numerical correctness, throughput/energy/area, and CPU/GPU baseline |
| 3 | `dac-2026-research406` | PS-CAM: An Efficient Content-Addressable Memory Based Accelerator for Point Search in Point Clouds | CAM device, point-cloud corpus, search semantics, recall/latency/energy/area, and software/CAM baseline |
| 4 | `dac-2026-research407` | AMS Layout Automation Using Circuit-Level Analog Standard Cells and Self-Biasing Techniques in Digital PnR Tools. | Analog cell/process, layout corpus, self-biasing/PnR constraints, DRC/PPA/yield, runtime, and manual/analog flow baseline |
| 5 | `dac-2026-research440` | Activity-Aware Partitioning for Effective Multi-Threaded Event-Driven RTL Simulation | RTL/workload corpus, activity model, partition policy, simulation correctness, speedup/memory, and simulator baseline |
| 6 | `dac-2026-research441` | Cachence: Fine-Grained Cache Partitioning in Both Time and Space | Cache/microarchitecture, workload traces, temporal/spatial policy, QoS/latency/energy, and static partition baseline |
| 7 | `dac-2026-research442` | VALVE: Accelerating Visible Version Searching in HTAP Systems via In-Storage Computing | HTAP/version workload, storage device, visibility semantics, correctness, throughput/latency/energy, and host baseline |
| 8 | `dac-2026-research444` | Gwrite: Offloading Replication in Disaggregated Memory Systems | Disaggregated topology, replication workloads, consistency model, bandwidth/latency/energy, and software replication baseline |
| 9 | `dac-2026-research445` | Hyperanalog: Domain-Aware Hypergraph Transformer for Analog Circuit Representation Learning | Analog circuit corpus, hypergraph construction, model split, prediction error/runtime, and prior ML baseline |
| 10 | `dac-2026-research461` | MoE-Balance: Unleashing the Full Potential of CPU-GPU Heterogeneity for Efficient MoE Inference | MoE models, CPU/GPU platform, balance/scheduling policy, quality, latency/throughput/energy, and CPU-only/GPU-only baseline |

These are DAC-specific source-recovery priorities and condition checklists, not
technical rankings or temporal trend evidence.
