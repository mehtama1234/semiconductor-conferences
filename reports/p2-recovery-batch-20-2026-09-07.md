# P2 recovery routing batch 20 — 2026-09-07

This tranche routes ten ISCA records across sparse-matrix scheduling, collective
communication, RDMA atomics, hardware verification/fuzzing, memory consistency
and formal methods, and CPU/GPU prefetching.

| Priority | Paper ID | Title | Evidence needed before quantitative use |
|---:|---|---|---|
| 1 | `isca-2026-program-135` | Harmonia: A Unified Hierarchical Scheduling Framework for Sparse Matrix Multiplication | Matrix distributions, scheduler hierarchy, hardware target, load balance/utilization, performance/energy, and sparse baselines |
| 2 | `isca-2026-program-136` | PipeComm: Maximizing Link Utilization through Pipeline-Aware Collective Communication Synthesis | Network topology, collective suite/message sizes, synthesis constraints, link utilization/latency, and NCCL/hand-tuned baseline |
| 3 | `isca-2026-program-137` | Breaking Barriers in Atomic Scaling: A Hardware–Software-Collaborated Framework to Deconstruct RDMA Atomic | RDMA NIC/network, atomic semantics, workload/traffic, ordering correctness, throughput/latency, and standard atomic baseline |
| 4 | `isca-2026-program-138` | Democratizing and Accelerating Hardware Verification with Software-Native Optimization | Verification workload/RTL suite, software optimization, proof/simulation correctness, runtime/resource cost, and commercial-tool baseline |
| 5 | `isca-2026-program-139` | HartBreaker: Deterministic Fuzzing of Multi-Hart RISC-V CPUs with Non-Deterministic Programs | CPU/ISA targets, fuzz-generation constraints, determinism mechanism, bug corpus, coverage/time, and existing fuzzers |
| 6 | `isca-2026-program-140` | QED: Scalable Consistency Verification of Memory Instruction Reordering in Hardware | Memory model, reorderings, proof/test method, litmus/workload suite, completeness/correctness, and baseline verifier |
| 7 | `isca-2026-program-141` | täkōFormal: Enabling Robust Software for Programmable Memory Hierarchies | Memory hierarchy/API, formal properties, software/toolchain, target systems, proof/runtime overhead, and conventional software baseline |
| 8 | `isca-2026-program-142` | LIBRA: A High-Accuracy, Cost-Aware, and Coordinated Multi-GPU Page Prefetcher | GPU topology, page traces, coordination policy, prefetch accuracy/coverage, migration cost, latency, and baseline prefetchers |
| 9 | `isca-2026-program-143` | Enhancing Instruction Prefetching via Cache and TLB Management | CPU/cache/TLB, benchmark suite, prefetch metadata, accuracy/MPKI, bandwidth/latency, and conventional instruction prefetcher |
| 10 | `isca-2026-program-144` | R-Max: Extending Bélády’s MIN with Prefetching to Bound Realistic Cache Performance | Trace source, future-knowledge bound, prefetch assumptions, cache sizes, metric definition, and practical-policy comparisons |

These are source-recovery priorities and condition checklists, not technical
rankings or temporal trend evidence.
