# P2 recovery routing batch 70 — 2026-09-07

This DAC-specific tranche covers runtime anomaly recovery in encrypted DNNs,
differentiable optical-proximity correction, distributed switch buffering,
weakly supervised wafer-defect segmentation, differentiable gate sizing,
selective adversarial encryption, sample-efficient DSE, arithmetic-intensity
graph optimization, fused sparse LLM accelerator generation, and living RTL
benchmark maintenance.

| Priority | Paper ID | Title | Evidence needed before quantitative use |
|---:|---|---|---|
| 1 | `dac-2026-research821` | Runtime-ADAR: Runtime Anomaly Detection and Attack Recovery in Encrypted DNNs | Encryption/threat model, DNN suite, anomaly/recovery policy, detection/accuracy, latency/energy, and unprotected baseline |
| 2 | `dac-2026-research827` | DR. OPC: Differentiable Rasterization for Advanced Optical Proximity Correction | Lithography process/pattern corpus, rasterizer model, OPC objective, printability/error/runtime, and OPC baseline |
| 3 | `dac-2026-research837` | Credix: A Credit-Driven Distributed Buffer Management for Large-Scale Switching Chips | Switch topology/traffic, buffer architecture, credit policy, packet loss/latency/throughput/area, and buffer baseline |
| 4 | `dac-2026-research838` | Separate: Segmenting Patterns from Defects in Wafer Manufacturing Using Weak Supervision | Wafer/process image corpus, weak labels, segmentation metric, domain shift/runtime, and supervised baseline |
| 5 | `dac-2026-research843` | Disentangled Differentiable Timing-Power Co-Optimization with Quad-Gradient Gate Sizing | PDK/circuit corpus, timing/power gradients, sizing constraints, PPA/DRC/runtime, and sizing baseline |
| 6 | `dac-2026-research848` | TT-SEAL: TTD-Aware Selective Encryption for Adversarially-Robust and Low-Latency Edge AI | Edge hardware/model suite, threat and TTD model, selective encryption policy, accuracy/latency/energy, and full-encryption baseline |
| 7 | `dac-2026-research859` | Soberdse: Sample-Efficient Design Space Exploration via Learning-Based Algorithm Selection | Design corpus, algorithm-selection model, search budget, PPA/correctness, transfer scope, and standard DSE baseline |
| 8 | `dac-2026-research863` | PRICE: An Operator Recomputation and Fission Framework for Computation Graphs via Attainable Arithmetic Intensity | Model/operator suite, recomputation/fission policy, correctness, latency/memory/energy, and compiler baseline |
| 9 | `dac-2026-research868` | FSGen: Agile Fused and Sparse Accelerator Generator with Accurate Power Model for LLM Applications | LLM kernels/models, generator, sparsity/fusion policy, PPA/power-model error, correctness, and generator baseline |
| 10 | `dac-2026-research874` | RTL-Benchmt: Dynamic Maintenance of RTL Generation Benchmark Through Agent-Assisted Analysis and Revision | RTL task/version corpus, agent process, evaluator correctness, leakage/version controls, and benchmark baseline |

These are DAC-specific source-recovery priorities and condition checklists, not
technical rankings or temporal trend evidence.
