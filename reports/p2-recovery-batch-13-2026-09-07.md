# P2 recovery routing batch 13 — 2026-09-07

This tranche routes ten ISCA 2026 records across storage networking, general-AI
dataflow, datacenter cooling, inference scaling, deployed training hardware,
intermittent systems, secure memory, FHE generation, and pointer integrity.
They remain metadata-only until primary sources and exact conditions are found.

| Priority | Paper ID | Title | Evidence needed before quantitative use |
|---:|---|---|---|
| 1 | `isca-2026-program-065` | BoostX™-NTI: Fast, Scalable and Flexible Storage Architecture with NVMe/TCP Initiator Acceleration | NVMe/TCP topology, target devices, queue depth, workload mix, CPU overhead, throughput/latency, and baseline initiator |
| 2 | `isca-2026-program-066` | M100: An Orchestrated Dataflow Architecture Powering General AI Computing | Model/workload suite, orchestration policy, accelerator/interconnect, scale, utilization, and silicon or simulator status |
| 3 | `isca-2026-program-067` | Prometheus: Toward Resilient Datacenters through Optimized Cooling Infrastructure | Datacenter thermal model, cooling hardware, workload traces, resilience events, PUE/temperature/availability metrics, and baseline |
| 4 | `isca-2026-program-068` | Understanding Inference Scaling for LLMs: Bottlenecks, Trade-offs, and Performance Principles | Models, sequence lengths, serving stack, hardware scale, bottleneck definitions, utilization/SLO metrics, and trace provenance |
| 5 | `isca-2026-program-069` | MTIA 300: Meta’s First Training Chip Featuring Built-in NICs and Collective Offloading Engines | Chip/process, model and cluster scale, NIC/collective topology, software stack, training throughput/efficiency, and comparable baseline |
| 6 | `isca-2026-program-070` | μRNG: A Framework for Assessing Randomness in Intermittent Computing Devices | Device/energy-harvesting conditions, entropy source, statistical test suite, restart model, security interpretation, and reference RNGs |
| 7 | `isca-2026-program-071` | IroKnight: Ownership-Preserving Neural Acceleration for Inference Serving | Ownership/threat model, accelerator interface, model suite, isolation mechanism, overhead, and non-protected baseline |
| 8 | `isca-2026-program-072` | Intermittence-aware Speculative Page Coloring for Secure NVM | NVM technology, intermittence/failure model, security guarantee, page-coloring policy, workloads, endurance/performance overhead, and baseline |
| 9 | `isca-2026-program-073` | AutoFHE: An Automatic Hardware Generation Framework for Domain-Specific FHE Accelerator | FHE schemes/parameters, circuit suite, generation flow, target technology, area/timing/energy, correctness, and hand-designed baseline |
| 10 | `isca-2026-program-074` | LIPPEN: A Lightweight In-Place Pointer Encryption Architecture for Pointer Integrity | ISA/memory assumptions, attack model, cryptographic primitive, protected workload suite, latency/area/energy overhead, and integrity baseline |

These priorities route source recovery and condition extraction; they are not
technical rankings, taxonomy adjudications, or trend evidence.
