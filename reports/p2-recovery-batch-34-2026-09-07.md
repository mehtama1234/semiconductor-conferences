# P2 recovery routing batch 34 — 2026-09-07

This tranche continues the DAC frontier across low-bit LLM PIM, CPU timing
side channels, distributed-GNN compression, PCB ground-plane co-design, spiking
transformers, TriSpGEMM, cloud-TEE availability, RISC-V fuzzing, chiplet DSE,
and real-time GPU scheduling.

| Priority | Paper ID | Title | Evidence needed before quantitative use |
|---:|---|---|---|
| 1 | `dac-2026-research146` | Freebit: Unleashing the Performance Potential of Low-Bit LLMs Through PIM | PIM device, LLM models/bit widths, quality metric, mapping/dataflow, latency/energy, and GPU baseline |
| 2 | `dac-2026-research1464` | Thrend: Mitigating Counting Thread-Based Fine-Grained Timing on Arm and Apple CPUs | CPU/OS, side-channel/threat model, counter behavior, mitigation coverage, overhead, and baseline defenses |
| 3 | `dac-2026-research1468` | Adahuff-GNN: A Convergency-Aware Adaptive Huffman Compression for Communication Reduction in Distributed GNN Training | GNN models/partitions, convergence metric, compression/error, network topology, training time/accuracy, and uncompressed baseline |
| 4 | `dac-2026-research1473` | GRACE: A Ground Plane Generation and Re-Routing Aware Co-Design Engine | PCB/PDK corpus, ground-plane/routing constraints, signal/PDN metrics, optimization budget, and CAD baseline |
| 5 | `dac-2026-research1480` | ADAPT: An Algorithm-Hardware Co-Design for Spiking Transformer with Training-Free Adaptive Token Pruning and Hierarchical Sparsity | SNN/transformer tasks, pruning/sparsity policy, device target, accuracy/latency/energy, and dense baseline |
| 6 | `dac-2026-research149` | TRIDENT: An End-to-End Streaming Accelerator for TriSpGEMM | TriSpGEMM matrix suite, sparsity patterns, streaming hardware, utilization/throughput/energy, and SpGEMM baseline |
| 7 | `dac-2026-research1494` | When Cloud TEEs Encounter Availability: A Lightweight Framework for Verifiable CPU Availability | TEE/CPU platform, threat/availability model, verifier evidence, attack coverage, overhead, and native TEE baseline |
| 8 | `dac-2026-research150` | RISCSmith: Finding RISC-V CPU Bugs via Rich Instruction Construction and On-the-Fly Differential Analysis | ISA/core corpus, instruction generator, oracle/differential setup, bug coverage, runtime, and fuzzing baseline |
| 9 | `dac-2026-research1519` | AgenticDSE: A Multi-Agent Design Space Exploration Framework with Multi-Phase Bayesian Optimization for Chiplet Accelerators | Chiplet design space, agent/model versions, BO budget, workloads, PPA/constraint metrics, and search baseline |
| 10 | `dac-2026-research1524` | Exploiting Dependency and Parallelism: Real-Time Scheduling and Analysis for GPU Tasks | GPU/task model, timing/dependency assumptions, schedulability proof, workloads, deadline/throughput, and scheduler baseline |

These are source-recovery priorities and condition checklists, not technical
rankings or temporal trend evidence.
