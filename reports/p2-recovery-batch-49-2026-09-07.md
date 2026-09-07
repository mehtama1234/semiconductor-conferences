# P2 recovery routing batch 49 — 2026-09-07

This tranche continues the DAC frontier across layer-aware IMC error correction,
tensor-centric accelerator verification, hot-switched CPU LLM serving, photonic
inverse design, real-time DAG scheduling, RTL assertion generation, voltage-
underscaled MACs, secret tracking, FPGA weightless learning, and posit-like
microscaling.

| Priority | Paper ID | Title | Evidence needed before quantitative use |
|---:|---|---|---|
| 1 | `dac-2026-research2347` | METRIC: An MDS-Analog ECC with Minimum Two-Column Redundancy for Fault-Tolerant, Layer-Aware IMC Architecture | IMC device/fault model, layer workloads, code construction, correction guarantee, accuracy/PPA/energy, and ECC baseline |
| 2 | `dac-2026-research2348` | Vten: Tensor-Centric Verification Framework for Domain-Specific Accelerators | Accelerator/tensor IR corpus, verification properties, batching method, coverage/proof/runtime, and conventional verifier baseline |
| 3 | `dac-2026-research235` | Sandwich: Joint Configuration Search and Hot-Switching for Efficient CPU LLM Serving | CPU/model suite, configuration space, hot-switch policy, quality, latency/throughput/energy, and static configuration baseline |
| 4 | `dac-2026-research2358` | Lightningfno: Ultra-Fast Modeling and Inverse Design for Photonic Matrix-Vector Multiplication Computing Units | Photonic device/process, design corpus, FNO model, electromagnetic error, inverse-design quality/runtime, and numerical solver baseline |
| 5 | `dac-2026-research2360` | Hierarchical Pareto-Prompted Optimization for Probabilistic DAG Scheduling on Real-Time Systems | DAG/task suite, probability and deadline model, prompt/search budget, schedulability/makespan/energy, and scheduler baseline |
| 6 | `dac-2026-research2361` | Svacoder: Training Specialized LLMs for Hardware Assertion Generation via RTL-Grounded Bidirectional Data Synthesis | RTL/assertion corpus, model/training split, property correctness/coverage, synthesis/formal runtime, and generic-LLM baseline |
| 7 | `dac-2026-research2364` | Adaptive Multiply-Accumulate Unit with Scalable Critical Path for Aggressive Voltage Underscaling DNN Accelerators | Process/voltage range, DNN workloads, adaptive MAC design, error/fault behavior, PPA/energy, and nominal-voltage baseline |
| 8 | `dac-2026-research2369` | Reconnaissance: Correctly Tracking Multiple Secrets Using Reveal/conceal Paradigms | Threat/model semantics, secret corpus, reveal/conceal mechanism, tracking correctness, overhead, and prior information-flow baseline |
| 9 | `dac-2026-research2372` | Tsetlinwisard: On-Chip Training of Weightless Neural Networks Using Tsetlin Automata on FPGAs | FPGA/device, task and data suite, automata/weightless training, accuracy/convergence, resource/energy, and conventional NN baseline |
| 10 | `dac-2026-research2374` | MXP: A Posit-Inspired Microscaling Format for Vision-Language Tasks | VLM/model suite, format/scale policy, accuracy, hardware implementation, latency/energy/memory, and FP/other microscaling baseline |

These are source-recovery priorities and condition checklists, not technical
rankings or temporal trend evidence.
