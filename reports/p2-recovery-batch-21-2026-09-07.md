# P2 recovery routing batch 21 — 2026-09-07

This tranche routes ten ISCA records across neural prefetching, quantum
compilation/simulation/photonic architectures, Ising/SAT compilation, cluster
power and thermal management, and distributed LLM synthesis.

| Priority | Paper ID | Title | Evidence needed before quantitative use |
|---:|---|---|---|
| 1 | `isca-2026-program-145` | From Memorization to Generalization: A Practical Neural Network Prefetching Framework | Training/test traces, model architecture, prefetch target, generalization split, accuracy/coverage, bandwidth/latency, and heuristic baseline |
| 2 | `isca-2026-program-146` | Unifying Qubit Routing Across Diverse Quantum ISAs via Canonical Representation | Quantum ISA set, circuits, canonical representation, routing constraints, fidelity/depth/runtime, and compiler baselines |
| 3 | `isca-2026-program-147` | TUSQ: Tracking, Uncomputation, and Sampling for Noisy Quantum Simulation | Noise model, circuits, tracking/uncomputation policy, sampling budget, estimator error/runtime, and simulator baseline |
| 4 | `isca-2026-program-148` | Photonic Quantum Computing on Spin Memory Architecture with Tree-Encoded Fusion | Photonic/spin device assumptions, fusion protocol, loss/error model, memory/optical resources, fidelity/throughput, and prior architecture |
| 5 | `isca-2026-program-149` | SATIC: An Optimizing Ising Compiler for SAT(isfiability) | SAT benchmark suite, Ising encoding, compiler transformations, solver/hardware target, solution quality/time, and encoding baseline |
| 6 | `isca-2026-program-150` | PowerGrad: Hierarchical Power Management for Power-Limited ML Inference Clusters | Cluster hardware, power cap/workload traces, controller hierarchy, SLO/throughput, transition overhead, and static power policy baseline |
| 7 | `isca-2026-program-151` | Power Sloshing in Compound Servers for Large-Scale AI Inference Workloads | Server composition, workload phase traces, power transients, thermal/electrical model, reliability/SLO effects, and mitigation baseline |
| 8 | `isca-2026-program-152` | PowerWeave: Unlocking Energy-Efficient ML on GPUs with OS-Level Spatial Power Management | GPU model, spatial partitioning, OS controls, ML workloads, quality/throughput/energy, and device-wide DVFS baseline |
| 9 | `isca-2026-program-153` | Lit Silicon: A Case Where Thermal Imbalance Couples Concurrent Execution in Multiple GPUs | GPU topology, thermal sensors/model, concurrent workloads, coupling mechanism, frequency/throughput impact, and thermal-management baseline |
| 10 | `isca-2026-program-154` | Scalable Synthesis of Distributed LLM Workloads Through Symbolic Tensor Graphs | Model/workload graph, symbolic representation, cluster topology, synthesis constraints, scaling/communication metrics, and hand-tuned baseline |

These are source-recovery priorities and condition checklists, not technical
rankings or temporal trend evidence.
