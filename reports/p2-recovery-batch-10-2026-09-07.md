# P2 recovery routing batch 10 — 2026-09-07

This tranche covers ISCA 2026 coherence, issue-queue scaling, branch/value
prediction, heterogeneous memory, and LLM-serving architectures.

| Priority | Paper ID | Title | Evidence needed before quantitative use |
|---:|---|---|---|
| 1 | `isca-2026-program-033` | Dorado: Clustered Hardware Cache Coherence for 1,000+ Cores | Core count/topology, coherence protocol, traffic/workload suite, area/power, consistency guarantees, and baseline coherence system |
| 2 | `isca-2026-program-034` | Hierarchical Wakeup Logic of the Issue Queue for High Scalability | Issue-queue width/latency, wakeup algorithm, process, benchmark suite, timing/energy, and centralized/distributed baselines |
| 3 | `isca-2026-program-035` | RUNLTS: Branch Prediction with Register-Value Correlations and Hierarchical Table Orchestration | Predictor tables, training/update policy, ISA traces, storage budget, accuracy metric, and predictor baselines |
| 4 | `isca-2026-program-036` | Augmenting the Branch Predictor with a Squashed-Branch Reuse Buffer | Reuse-buffer design, speculative state, storage/latency overhead, trace suite, misprediction metric, and matched predictor baseline |
| 5 | `isca-2026-program-037` | Revisiting Global Value Prediction: A Resurgent Complement to Local Predictors | Value-prediction coverage, confidence/recovery mechanism, trace suite, storage budget, correctness, and local-predictor comparison |
| 6 | `isca-2026-program-038` | HybridSpec: Exploiting Hybrid-bonding Memory to Accelerate LLM Serving through Heterogeneous Architecture and Speculative Decoding | Bonding/memory stack, model/context suite, speculative acceptance, hardware boundary, memory bandwidth, and serving baseline |
| 7 | `isca-2026-program-039` | P3-LLM: An Integrated NPU-PIM Accelerator for Edge LLM Inference Using Hybrid Numerical Formats | NPU/PIM organization, numerical formats, model/task suite, accuracy, process/area/energy, and GPU/NPU baseline |
| 8 | `isca-2026-program-040` | CHIME: A Case for Efficient Long-Context Attention-FC Disaggregated Inference with DIMM-PIM | Context lengths, attention/FC partition, DIMM-PIM hardware, interconnect, latency/throughput, and non-disaggregated baseline |
| 9 | `isca-2026-program-041` | SMOOTH: Hardware-Assisted Fine-Grained On-Chip Memory Management for Efficient On-Device LLM Inference | On-chip memory organization, allocation granularity, model/context suite, fragmentation/latency, area/power overhead, and software-only baseline |
| 10 | `isca-2026-program-042` | SHyLA: 3D-Stacked NVM-DRAM Hybrid LLM-Inference Architecture Exploiting Data and Memory Heterogeneity | NVM/DRAM stack and process, placement policy, model suite, endurance/retention, bandwidth/energy, and homogeneous-memory baseline |

These remain official-program metadata routes pending primary sources and
condition extraction; no quantitative claim is accepted.
