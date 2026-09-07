# P2 recovery routing batch 66 — 2026-09-07

This DAC-specific tranche covers peripheral-accurate embedded fuzzing, unified
nonlinear edge operators, tree-structured mixture-of-agents serving, bit-level
redundant LLM acceleration, cache-oriented task reasoning, delay-aware fill
insertion, wafer-defect diffusion analysis, NUMA I/O coordination, sparsely
gated RF neural networks, and runtime-adaptive multimodal FPGA inference.

| Priority | Paper ID | Title | Evidence needed before quantitative use |
|---:|---|---|---|
| 1 | `dac-2026-research616` | Stateful Embedded Fuzzing Using Peripheral-Accurate Systemc Virtual Prototypes | SystemC/peripheral models, firmware corpus, state/oracle model, validated bugs/coverage, runtime, and fuzzer baseline |
| 2 | `dac-2026-research617` | UniNL: Unifying Fragmented Non-Linear Operators for Efficient Edge LLM Inference | LLM/operator suite, fusion policy, edge hardware, accuracy, latency/energy/memory, and unfused baseline |
| 3 | `dac-2026-research628` | Faster-MoA: Low-Latency Tree-Structured MoA Serving with Early Exit and Agent-Aware Prefill-Decode Overlap | MoA/LLM models, early-exit policy, prefill/decode workload, quality, tail latency/throughput/energy, and standard serving baseline |
| 4 | `dac-2026-research640` | AMBER: A Unified Accelerator for Multi-Precision LLM Inference Exploiting Bit-Level Redundancy and Reconfigurability | LLM suite, precision/redundancy model, accelerator target, accuracy, throughput/energy/area, and fixed-precision baseline |
| 5 | `dac-2026-research641` | Torr: Towards Brain-Inspired Task-Oriented Reasoning via Cache-Oriented Algorithm-Architecture Co-Design | Reasoning tasks/models, cache/memory architecture, quality, latency/energy/memory, and conventional reasoning baseline |
| 6 | `dac-2026-research648` | Differentiable Fill Insertion with Explicit Delay Optimization | PDK/design corpus, fill/process model, delay objective, timing/DRC/power, runtime, and density-only baseline |
| 7 | `dac-2026-research649` | Mask-Guided Diffusion with Process-Aware Metric Optimization for Long-Tailed Wafer Defect Analysis | Wafer/process image corpus, mask/diffusion model, class imbalance, detection quality, runtime, and classifier baseline |
| 8 | `dac-2026-research651` | Cache Where It Counts: Towards Workload-Aware I/O Coordination for NUMA Storage Systems | NUMA/storage topology, workload traces, coordination policy, tail latency/throughput/energy, and default I/O baseline |
| 9 | `dac-2026-research656` | ASG-MOENN: Adaptive Sparsely-Gated Mixture of Experts Neural Network for Digital Predistortion in Quadrature Switched-Capacitor Power Amplifiers | RF hardware/traces, MoE/DNN suite, gating policy, linearity/quality, compute/energy, and dense DPD baseline |
| 10 | `dac-2026-research660` | TRINE: A Token-Aware, Runtime-Adaptive FPGA Inference Engine for Multimodal AI | Multimodal models/tasks, FPGA/platform, token-adaptation policy, quality, latency/energy/area, and static engine baseline |

These are DAC-specific source-recovery priorities and condition checklists, not
technical rankings or temporal trend evidence.
