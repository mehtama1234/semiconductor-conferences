# P2 recovery routing batch 48 — 2026-09-07

This tranche continues the DAC frontier across resilient LLM inference,
memory-constrained MoE scheduling, sub-bit compression, LLM reference-model
verification, generative circuit design, ReRAM CIM, graph timing prediction,
physics-prior compact modeling, KV-cache offload, and semiconductor-device
simulation.

| Priority | Paper ID | Title | Evidence needed before quantitative use |
|---:|---|---|---|
| 1 | `dac-2026-research2307` | STAC: Spatial-Temporal Activation Contextualization for Resilient LLM Inference | Fault model, LLM/model suite, spatial-temporal context mechanism, quality/recovery, latency/energy overhead, and unprotected baseline |
| 2 | `dac-2026-research2313` | Weaver: Stratified Expert Scheduling for Memory-Constrained MoE Inference | MoE models, memory limit, stratification/scheduler policy, quality, latency/throughput/energy, and standard scheduler baseline |
| 3 | `dac-2026-research2317` | Ultrasketchllm: Sub-1-Bit LLM Compression via Sketch and Hardware-Friendly Operators | LLMs/tasks, sketch/compression error, bit budget, hardware mapping, accuracy/latency/energy, and standard quantization baseline |
| 4 | `dac-2026-research2319` | Chipmodeler: LLM-Aided Reference Model Design for Agile Hardware Verification | Hardware-model corpus, LLM/version, reference-model correctness, coverage/runtime, toolchain, and human/EDA baseline |
| 5 | `dac-2026-research2329` | Shortcircuit: Alphazero-Driven Generative Circuit Design | Circuit objective/library, AlphaZero state/action/reward, design corpus, functional/PPA quality, search budget, and synthesis baseline |
| 6 | `dac-2026-research2330` | HP-CIM: A Computing-in-Memory Transformer Accelerator with ReRAM-Based Hash Predictor for Attention Sparsity Exploitation | ReRAM/device model, transformer suite, hash/sparsity policy, accuracy, throughput/energy/area, and dense/digital baseline |
| 7 | `dac-2026-research2333` | PBA-rGAT-Edge: Arc-Level Path-Based Timing Prediction with Scalable Residual Edge-Aware Graph Attention | Circuit/graph corpus, timing labels, model split, prediction error, scalability/runtime, and STA/ML baseline |
| 8 | `dac-2026-research2336` | A Physics-Prior Intelligent Compact Modeling Framework for BEOL-Compatible DTCO: EKAN-Based Distillation from Neural to Symbolic Models | Device/process data, physics priors, neural/symbolic models, prediction error, transfer scope, and compact-model baseline |
| 9 | `dac-2026-research2345` | Scoutattention: Efficient KV Cache Offloading via Layer-Ahead CPU Pre-Computation for LLM Inference | LLM/context suite, KV-cache policy, CPU/GPU platform, quality, latency/memory/energy, and ordinary offload baseline |
| 10 | `dac-2026-research2346` | Weak-Form Physics-Informed Neural Network for Self-Supervised Learning in Semiconductor Device Simulation | Device/PDE corpus, weak-form loss, boundary conditions, solver settings, error/runtime, and supervised/numerical baseline |

These are source-recovery priorities and condition checklists, not technical
rankings or temporal trend evidence.
