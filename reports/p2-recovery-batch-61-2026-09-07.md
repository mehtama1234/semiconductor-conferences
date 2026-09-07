# P2 recovery routing batch 61 — 2026-09-07

This DAC-specific tranche covers ML datapath power prediction, spatial netlist
partitioning, LLM assertion retrieval, distributed-training preemption, robust
silicon-photonic vision, backside-PDN optimization, GNN acceleration, RISC-V
processor fuzzing, wafer-on-wafer network design, and RL macro placement.

| Priority | Paper ID | Title | Evidence needed before quantitative use |
|---:|---|---|---|
| 1 | `dac-2026-research3154` | Unlocking Automated Datapath Gating via Machine Learning Power Prediction | Datapath/process corpus, power labels, model split, gating policy, prediction error/PPA, and power-analysis baseline |
| 2 | `dac-2026-research320` | SAAP: An Efficient Spatial-Aware Analytic Partitioning Algorithm of VLSI Netlists for Parallel Routing | Netlist/PDK corpus, partition objective, parallel router, wirelength/congestion/runtime, and partitioner baseline |
| 3 | `dac-2026-research3200` | STELLAR: Structure-Guided LLM Assertion Retrieval and Generation for Formal Verification | RTL/assertion corpus, retrieval/generation model, property correctness/coverage, formal budget, and generic-LLM baseline |
| 4 | `dac-2026-research3208` | Making Sense of Job Preemption for Distributed Deep Learning Acceleration | Cluster/workload traces, preemption policy, convergence/throughput, recovery cost, energy, and non-preemptive baseline |
| 5 | `dac-2026-research3237` | Light-Bound Transformers: Hardware-Anchored Robustness for Silicon-Photonic Computer Vision Systems | Photonic device/noise model, vision suite, robustness method, accuracy, optical/electronic energy and latency, and baseline model |
| 6 | `dac-2026-research335` | BSPDN-Elite: A Comprehensive Framework for Optimizing Timing, Power and Routing Resources in BSPDN Designs | BSPDN/3D process, design corpus, timing/power/routing constraints, PPA/DRC, runtime, and conventional flow baseline |
| 7 | `dac-2026-research341` | TAG: A Topology-Aware Architecture for Configurable and Memory-Efficient GNN Acceleration | GNN/model suite, topology/dataflow, accelerator target, accuracy, throughput/memory/energy, and GPU baseline |
| 8 | `dac-2026-research358` | Lyra: A Hardware-Accelerated RISC-V Verification Framework with Generative Model-Based Processor Fuzzing | RISC-V cores/ISA, generator model, fault oracle, coverage/validated bugs, runtime, and software fuzzer baseline |
| 9 | `dac-2026-research363` | Network Design for Wafer-Scale Systems with Wafer-on-Wafer Hybrid Bonding | Wafer stack/process, topology/workloads, link model, bandwidth/latency/energy/area, and conventional wafer-scale baseline |
| 10 | `dac-2026-research365` | Advancing Macro Placement: Integrating Proven Design Practices with Reinforcement Learning | PDK/design corpus, RL state/reward, expert priors, placement quality/timing/DRC, search budget, and placer baseline |

These are DAC-specific source-recovery priorities and condition checklists, not
technical rankings or temporal trend evidence.
