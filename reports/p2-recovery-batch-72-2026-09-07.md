# P2 recovery routing batch 72 — 2026-09-07

This DAC-specific tranche covers adaptive spiking detection, QLC write
invalidation, orientation-aware 3D placement, asynchronous sparse LU on HBM
FPGAs, reconfigurable nonlinear inference, function-family analog optimization,
cross-stage video redundancy, force-based module placement, pressure-aware
biochip scheduling, and intermittent hyperdimensional IoT inference.

| Priority | Paper ID | Title | Evidence needed before quantitative use |
|---:|---|---|---|
| 1 | `dac-2026-research920` | Adaptive Spiking Neural Networks for Real-Time Multi-Object Detection Tasks | SNN/detection suite, adaptation policy, hardware target, accuracy/latency/energy, and static-SNN baseline |
| 2 | `dac-2026-research931` | WILL: Write Invalidation Skipping for QLC NAND by Leveraging Data Lifespan and Latency Awareness | QLC generation, workload/lifespan traces, invalidation policy, latency/endurance/error, and standard FTL baseline |
| 3 | `dac-2026-research934` | ATOM-3D: Analytical Three-Dimensional Orientation-Aware Mixed-Size Placer | 3D process/design corpus, orientation model, placement constraints, wirelength/congestion/timing/DRC, and placer baseline |
| 4 | `dac-2026-research935` | SALUT: Efficient Sparse LU Factorization via Asynchronous Task Triggering on HBM FPGAs | HBM FPGA platform, sparse matrices, task policy, numerical correctness, throughput/memory/energy, and CPU/GPU baseline |
| 5 | `dac-2026-research946` | UNICON: A Unified Reconfigurable Nonlinear Architecture for Efficient Neural Network Inference | Operator/model suite, reconfigurable hardware, approximation/precision, accuracy, throughput/energy/area, and fixed architecture baseline |
| 6 | `dac-2026-research951` | Exploiting Function-Family Structure in Analog Circuit Optimization | Analog/PDK corpus, function-family model, optimization/search budget, PPA/constraint quality, and optimizer baseline |
| 7 | `dac-2026-research952` | Deltasight: Architecting Efficient Video AIoT Systems via Cross-Stage Consistent Redundancy Elimination | Video AIoT platform/traces, redundancy policy, quality, latency/energy/bandwidth, and uncompressed baseline |
| 8 | `dac-2026-research954` | Module-Level Placement Using Force-Based Deformation for Efficient Early Design Estimation | PDK/design corpus, force/deformation model, placement metrics, runtime, and early-placement baseline |
| 9 | `dac-2026-research959` | Timing-Driven Scheduling and Placement Under Pressure-Path Interference for Fully Programmable Valve Array Biochips | Biochip platform/protocol corpus, pressure/timing model, schedule correctness, latency/area, and scheduler baseline |
| 10 | `dac-2026-research962` | Energyhdc: Intermittent Hyperdimensional Inference on Energy-Harvesting IoT | HDC/task suite, harvester/device traces, intermittent policy, accuracy/availability, latency/energy, and conventional baseline |

These are DAC-specific source-recovery priorities and condition checklists, not
technical rankings or temporal trend evidence.
