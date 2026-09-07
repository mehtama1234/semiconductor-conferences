# P2 recovery routing batch 18 — 2026-09-07

This tranche routes ten ISCA records across sparse embeddings, spatial audio,
event-driven sensing, video super-resolution, programmable IPUs, private
inference, and fully homomorphic-encryption accelerators.

| Priority | Paper ID | Title | Evidence needed before quantitative use |
|---:|---|---|---|
| 1 | `isca-2026-program-115` | ParetoES: Hardware-Accelerated Sparse Embedding Similarity via Pareto-Optimal Pruning | Embedding models/datasets, pruning objective, recall/quality, hardware target, latency/energy, and dense/sparse baselines |
| 2 | `isca-2026-program-116` | ECHO: Efficient Head-Orientation-Guided Real-Time Sound Spatialization for Virtual Reality | Audio/VR traces, head-motion latency, spatialization quality, DSP/accelerator target, power, and software baseline |
| 3 | `isca-2026-program-117` | DESSCam: An Event-Driven Architecture with In-Sensor Epitopological Sparse Sampling to Break the Latency-Power Tradeoff in Eye Tracking | Sensor/process, eye-tracking dataset, event/sampling policy, accuracy/latency/power, and frame-based baseline |
| 4 | `isca-2026-program-118` | SLICE: A Selective Local Inference Framework with Codec Exploitation for Accelerating Video Super-Resolution | Video dataset/quality metric, selection policy, codec reuse, hardware/runtime, latency/energy, and full-inference baseline |
| 5 | `isca-2026-program-119` | Enabling Continuous, In-Field Introspection: The Programmable IPU Architecture | IPU architecture, observability probes, production workload, overhead/coverage, programmability, and static-monitor baseline |
| 6 | `isca-2026-program-120` | FEnc2: Unifying Data Packing for Efficient Private Inference via Convolution and Architecture-Aware Fragment Encoding | Cryptosystem/threat model, model/task suite, packing/encoding, accelerator, accuracy/security, latency/communication, and prior private-inference baseline |
| 7 | `isca-2026-program-121` | FlashTFHE: A Scalable Architecture for Efficient Multi-bit Fully Homomorphic Encryption | TFHE parameters, multi-bit scheme, workload circuits, flash/memory target, bootstrapping latency/energy, and CPU/GPU/ASIC baselines |
| 8 | `isca-2026-program-122` | Unlocking Pipeline Parallelism for Bootstrapping: A Pipelined Multi-Chiplet TFHE Accelerator | Chiplet topology, TFHE parameters, pipeline schedule, interconnect, throughput/latency/area, and monolithic baseline |
| 9 | `isca-2026-program-123` | HE²: A Communication-Light Heterogeneous Architecture for Efficient Fully Homomorphic Encryption | FHE scheme/parameters, CPU/accelerator split, communication model, circuit suite, security/correctness, and homogeneous baseline |
| 10 | `isca-2026-program-124` | HyperDrive: Hierarchical Exploitation of Memory Efficiency for GPU-Based FHE Acceleration | GPU/memory hierarchy, FHE workload, tiling/compression, capacity and bandwidth, latency/energy, and unoptimized GPU baseline |

These are source-recovery priorities and condition checklists, not technical
rankings or temporal trend evidence.
