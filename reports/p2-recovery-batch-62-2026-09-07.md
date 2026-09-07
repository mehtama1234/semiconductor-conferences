# P2 recovery routing batch 62 — 2026-09-07

This DAC-specific tranche covers AMX/DIMM-NDP MoE offload, legality-assured
differentiable placement, tolerance-aware redundant neural networks, answer-first
KV management, cause-effect scheduling, physical chiplet planning, mobile
speculative decoding, partitioned-GPU register arbitration, FPGA HBM profiling,
and light-penetration compensation for printed microfluidics.

| Priority | Paper ID | Title | Evidence needed before quantitative use |
|---:|---|---|---|
| 1 | `dac-2026-research368` | Trimoe: Augmenting GPU with AMX-Enabled CPU and DIMM-NDP for High-Throughput MoE Inference via Offloading | MoE models, CPU/AMX/DIMM-NDP hardware, offload policy, quality, latency/throughput/energy, and GPU baseline |
| 2 | `dac-2026-research373` | LATTE: Legality-Assured Differentiable Timing-Driven Detailed Placement | PDK/design corpus, legality constraints, timing model, wirelength/congestion/timing/DRC, runtime, and placer baseline |
| 3 | `dac-2026-research374` | Sparsity- and Tolerance-Aware Temporally Redundant Neural Networks | Fault model, model/task suite, temporal redundancy policy, accuracy/recovery, overhead/energy, and nonredundant baseline |
| 4 | `dac-2026-research375` | Crystal-KV: Efficient KV Cache Management for Chain-of-Thought LLMs via Answer-First Principle | CoT models/tasks, cache policy, answer-quality preservation, memory/latency/energy, and standard KV baseline |
| 5 | `dac-2026-research378` | Scheduling Cause-Effect Chains Without Timing Anomalies in End to End Latency | Real-time workload/dependency model, anomaly definition, scheduler, deadline correctness, latency/energy, and standard scheduler baseline |
| 6 | `dac-2026-research380` | Chiplaner: Physically-Aware and Timing-Driven Design Planner for 2.5D Multi-Chiplet Systems | Chiplet/package/PDK corpus, physical/timing model, planner objective, PPA/thermal/DRC, runtime, and planner baseline |
| 7 | `dac-2026-research384` | AHASD: Asynchronous Heterogeneous Architecture for LLM Adaptive Drafting Speculative Decoding on Mobile Devices | Mobile SoC, LLM suite, draft/adaptation policy, acceptance/quality, latency/energy/memory, and ordinary decoding baseline |
| 8 | `dac-2026-research387` | CODA: Cooperative Register Distribution and Arbitration Among Partitioned GPU Sub-Cores | GPU architecture, workload suite, register policy, correctness, throughput/occupancy/energy, and standard register allocation baseline |
| 9 | `dac-2026-research389` | Toki: Profiling HBM Performance on FPGA Systems with RISC-V Soft Cores and PCIe Host DMA Traffic | FPGA/HBM/RISC-V/PCIe platform, workload traces, profiling methodology, bandwidth/latency/energy, and host baseline |
| 10 | `dac-2026-research397` | Lipcon: A Physics-Aware Spatially Resolved Light Penetration Compensation Method for Low-Cost 3D-Printed Microfluidics | Printer/material/optical setup, calibration data, physics model, print quality/error, runtime/cost, and uncorrected baseline |

These are DAC-specific source-recovery priorities and condition checklists, not
technical rankings or temporal trend evidence.
