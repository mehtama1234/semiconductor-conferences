# P2 recovery routing batch 12 — 2026-09-07

This tranche routes ten adjacent ISCA 2026 records across quantum control,
compiler/architecture co-design, MoE serving, edge inference, memory tagging,
and low-bit compression. These remain metadata-only routes until exact primary
sources and conditions are recovered.

| Priority | Paper ID | Title | Evidence needed before quantitative use |
|---:|---|---|---|
| 1 | `isca-2026-program-055` | A Streaming Architecture for Quantum Error Syndrome Compression at 4 Kelvin | Cryogenic device assumptions, syndrome stream, compression loss, area/power/latency, and decoder baseline |
| 2 | `isca-2026-program-056` | Transpiler-Architecture Co-Design to Curb Clifford Costs in Fault-Tolerant Quantum Computing | Circuit family, transpiler transformations, hardware target, Clifford/T-count accounting, and fidelity/runtime baseline |
| 3 | `isca-2026-program-057` | Kernpiler: Compiler Optimization for Quantum Hamiltonian Simulation with Partial Trotterization | Hamiltonians, error budget, Trotter-step policy, backend, compiler baseline, and simulation/runtime conditions |
| 4 | `isca-2026-program-058` | Accelerating MoE with Dynamic In-Switch Computing on Multi-GPUs | GPU/network topology, expert-routing distribution, switch implementation, collective baseline, throughput/latency, and power |
| 5 | `isca-2026-program-059` | ConServe: Contiguity-Preserving Memory Management for Multi-Turn LLM Serving | Model/context mix, allocator policy, fragmentation definition, hardware/runtime, SLOs, and serving baseline |
| 6 | `isca-2026-program-060` | Mapping and Communication Optimizations with Fault Tolerance for Wafer-Scale LLM Inference | Wafer-scale platform, fault model, mapping/recovery overhead, model suite, utilization, and fault-free baseline |
| 7 | `isca-2026-program-061` | DynoPipe: Heterogeneous Edge-Cloud LLM Serving with Dynamically Orchestrated Pipeline Boundaries | Edge/cloud hardware, model and request traces, boundary policy, network conditions, SLO/quality metrics, and static partition baseline |
| 8 | `isca-2026-program-062` | DIAMoND: Dynamic Inference for Adaptive Edge MoE with Heterogeneous In-NAND and Near-DRAM Compute Architecture | NAND/DRAM technologies, expert placement, workload distribution, precision, latency/energy, and GPU/CPU baseline |
| 9 | `isca-2026-program-063` | SingularBit: Exploiting Synergy of Singular Value Decomposition and Low-Bit Quantization for Weight and KV Compression in LLM Inference | Models/tasks, bit widths, SVD rank, KV policy, accuracy/perplexity, latency/memory, and quantization baseline |
| 10 | `isca-2026-program-064` | Optimized Memory Tagging on AmpereOne® Processors | Processor generation, tag granularity, security coverage, workload suite, overhead, and untagged/tagging baselines |

The routing categories are thematic hypotheses for source recovery, not
adjudicated taxonomy assignments, performance claims, or evidence of field
direction.
