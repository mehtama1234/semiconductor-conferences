# P2 recovery routing batch 22 — 2026-09-07

This tranche routes ten ISCA records across disaggregated training, MoE/MLLM
serving, accelerator scheduling, flexible precision, LLM/SNN/FPGA compute,
computational memory offload, PIM compilation, and near-cache locality.

| Priority | Paper ID | Title | Evidence needed before quantitative use |
|---:|---|---|---|
| 1 | `isca-2026-program-155` | DisDP: Disaggregating Compute, Network, and Storage for Model-Sharded Data-Parallel Training | Cluster topology, model/sharding, storage/network traces, overlap policy, scaling/throughput/efficiency, and monolithic baseline |
| 2 | `isca-2026-program-156` | MoE-Hub: Taming Software Complexity for Seamless MoE Overlap with Hardware-Accelerated Communication on Multi-GPU Systems | GPU/interconnect, MoE models, overlap/runtime API, expert traffic, utilization/latency, and software communication baseline |
| 3 | `isca-2026-program-157` | Symbiotic MLLM Serving: Dynamically Balancing Parallelism Across GPUs and Resources Within GPUs | MLLM models/modalities, GPU topology, parallelism policy, request traces, SLO/throughput/energy, and static serving baseline |
| 4 | `isca-2026-program-159` | Dynamic Scheduling for AI Accelerators via TISA | Accelerator ISA/microarchitecture, workload mix, scheduler state/actions, overhead, utilization/latency, and static scheduler baseline |
| 5 | `isca-2026-program-160` | MXFFP: Microscaling Flexible Floating Point Format for Large-Scale AI Model Acceleration | Format/block scale, models/tasks, accuracy, hardware support, bandwidth/energy/latency, and FP/quantization baselines |
| 6 | `isca-2026-program-161` | UniCore: A Bit-Width Scalable GEMM Unit for Unified LLM Inference | LLM models/precisions, bit-width transitions, FPGA/ASIC target, throughput/area/energy, quality, and fixed-width baseline |
| 7 | `isca-2026-program-162` | XtraMAC: An Efficient MAC Architecture for Mixed-Precision LLM Inference on FPGA | FPGA/device, mixed-precision kernels, model suite, DSP/LUT/BRAM cost, throughput/quality/energy, and conventional MAC baseline |
| 8 | `isca-2026-program-163` | ELSA: An ELastic SNN Inference Architecture for Efficient Neuromorphic Computing | SNN models/datasets, elasticity mechanism, neuromorphic target, accuracy/latency/energy, and fixed-resource baseline |
| 9 | `isca-2026-program-164` | AXLE: Coordinated Offloading with Asynchronous Back-Streaming in Computational Memory Systems | Computational-memory technology, workload/data placement, offload/back-stream protocol, bandwidth/latency/energy, and host baseline |
| 10 | `isca-2026-program-165` | DCC: Data-Centric Compilation of Machine Learning Kernels for Processing-In-Memory Architectures | PIM technology, ML kernels/models, compiler transformations, mapping constraints, accuracy/performance/energy, and hand-tuned baseline |

These are source-recovery priorities and condition checklists, not technical
rankings or temporal trend evidence.
