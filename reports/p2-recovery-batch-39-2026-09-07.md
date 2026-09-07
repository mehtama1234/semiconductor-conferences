# P2 recovery routing batch 39 — 2026-09-07

This tranche continues the DAC frontier across CIM security, agentic testbench
generation, chip-layout pretraining, hybrid-bonded 3D eFlash thermal stability,
SSD aging, BEV detection NAS, compressed GEMM, SNN co-design, embodied VLA
speculative decoding, and silicon thermal reconstruction.

| Priority | Paper ID | Title | Evidence needed before quantitative use |
|---:|---|---|---|
| 1 | `dac-2026-research1853` | Signing Crossbar Columns Instead of Neural Network Weights in Compute-in-Memory Accelerators | CIM device/threat model, signing scheme, model suite, accuracy/security, PPA/energy, and weight-signing baseline |
| 2 | `dac-2026-research1858` | Reflectbench: An Agentic Framework for Generating System-Level Design Testbench via Consensus and Reflection | Design/testbench corpus, agent/model/version, consensus/reflection loop, coverage/bug detection, cost/runtime, and human baseline |
| 3 | `dac-2026-research1859` | iPCL-M: Pre-Training of Chip Layout for Metrics Evaluation and Optimization | Layout corpus/PDK, pretraining split, metric targets, transfer/generalization, PPA/runtime, and supervised baseline |
| 4 | `dac-2026-research1862` | Thermal Stability Strategy for a 12nm/28nm Hybrid-Bonding Wafer-on-Wafer 3D-Integrated Eflash In-Memory Computing SoC | Process/package, thermal workload, stability metric, measured/simulated conditions, power/performance, and thermal baseline |
| 5 | `dac-2026-research1872` | SSD Reforge: Dynamic Parity Management to Extend SSD Lifetime Under Aging | NAND/SSD generation, aging/endurance model, parity policy, workload traces, lifetime/performance/energy, and static parity baseline |
| 6 | `dac-2026-research1878` | Hardware-Aware Neural Architecture Search for Real-Time BEV-Based 3D Object Detection | BEV datasets/models, hardware constraints, NAS budget, detection quality/latency/energy, and conventional detector baseline |
| 7 | `dac-2026-research1885` | PEACE: Algorithm–hardware Co-Design for PE-Granular Energy-Aware Compressed GEMM Acceleration | Matrix/model suite, compression/precision, PE architecture, energy/throughput/quality, and dense/compressed baseline |
| 8 | `dac-2026-research1899` | ACE-NAS: A Zero-Cost NAS Framework for Co-Design of Architecture and Encoding in Spiking Neural Networks | SNN datasets, encoding/search space, zero-cost score, hardware target, accuracy/latency/energy, and NAS baseline |
| 9 | `dac-2026-research1900` | KERV: Kinematic-Rectified Speculative Decoding for Embodied VLA Models | VLA models/tasks, action/kinematic traces, speculation acceptance, quality/latency, hardware/runtime, and non-speculative baseline |
| 10 | `dac-2026-research1907` | Seeing Through Silicon: Multimodal Thermal Reconstruction via Physics-Informed Diffusion | Silicon/package thermal corpus, sensors/physics, diffusion model, reconstruction error, transfer/runtime, and numerical baseline |

These are source-recovery priorities and condition checklists, not technical
rankings or temporal trend evidence.
