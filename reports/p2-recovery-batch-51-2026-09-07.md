# P2 recovery routing batch 51 — 2026-09-07

This tranche continues the DAC frontier across cross-layer reliability, MRAM
binary CIM, heterogeneous LLM PIM, LLM protocol patching, sparse tensor cores,
flow-matching placement, thermal-aware SRAM allocation, GPU shared memory,
video-diffusion token reduction, and FPGA zero-knowledge proofs.

| Priority | Paper ID | Title | Evidence needed before quantitative use |
|---:|---|---|---|
| 1 | `dac-2026-research2424` | XRel-Graph: Graph Learning-Driven Cross-Layer Reliability Management in Embedded Mixed-Criticality Systems | Mixed-criticality workloads/faults, graph features, intervention policy, safety/availability, overhead/energy, and static-reliability baseline |
| 2 | `dac-2026-research2425` | COM-BNN: A Configurable Low Power MRAM-Based Computing-in-Memory Accelerator for Binary Convolutional Computations | MRAM/device/process, binary model suite, configuration policy, accuracy, area/energy/throughput, and digital/CIM baseline |
| 3 | `dac-2026-research2432` | Hybrid PIM-Oriented Architecture-Dataflow Co-Design for Heterogeneous LLM Inference | LLM suite, PIM/device and host platform, dataflow policy, quality, latency/energy/memory, and GPU-only baseline |
| 4 | `dac-2026-research2443` | Stitch: Assertion-Guided Patching of On-Chip Protocol Implementations Using LLMs | Protocol/RTL corpus, assertion semantics, LLM/version, patch correctness/coverage, formal/simulation budget, and manual baseline |
| 5 | `dac-2026-research2468` | Pillarsparse: Rethinking Unstructured Sparse Formats for Tensor Cores | Model/matrix suite, sparsity formats, tensor-core hardware, accuracy, throughput/energy, and dense/structured baseline |
| 6 | `dac-2026-research2476` | Flowplace: Flow Matching for Chip Placement | PDK/design corpus, flow-matching model, placement constraints, wirelength/congestion/timing/DRC, runtime, and placer baseline |
| 7 | `dac-2026-research2481` | SCOUT: Thermal-Aware SRAM Allocation for Real-Time DNN Tasks on Edge TPU | Edge TPU/process, task and thermal model, allocation policy, deadline/temperature/accuracy, energy, and thermal-unaware baseline |
| 8 | `dac-2026-research2489` | Nash: A Neighbor-Aware Shared Memory Design on GPU for Accelerating AI Workloads | GPU architecture, workload suite, neighbor-sharing policy, correctness, throughput/latency/energy, and standard shared-memory baseline |
| 9 | `dac-2026-research2495` | ORBIS: Output-Guided Token Reduction with Distribution-Aware Matching for Video Diffusion Acceleration | Video-diffusion models/tasks, token-reduction policy, output-quality metric, frame latency/energy, and unpruned baseline |
| 10 | `dac-2026-research2504` | EASY-ZKP: An End-to-End FPGA-Accelerated System for Zero Knowledge Proofs | ZKP protocol/workloads, FPGA/device, arithmetic precision/security, proof latency/throughput/energy/area, and CPU/GPU baseline |

These are source-recovery priorities and condition checklists, not technical
rankings or temporal trend evidence.
