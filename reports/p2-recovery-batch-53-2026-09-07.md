# P2 recovery routing batch 53 — 2026-09-07

This tranche continues the DAC frontier across RL placement, timing-arc reuse,
speculative MoE decoding, hierarchical video precision, lattice-surgery
compilation, decomposed-LLM inference, fault-tolerant circuit compilation,
local-address SRAM, ZNS filesystem units, and multi-agent SDC generation.

| Priority | Paper ID | Title | Evidence needed before quantitative use |
|---:|---|---|---|
| 1 | `dac-2026-research2560` | How Can Reinforcement Learning Achieve Expert-Level Placement? | Placement corpus/PDK, RL state/action/reward, expert comparator, wirelength/congestion/timing/DRC, training/search budget, and placer baseline |
| 2 | `dac-2026-research2566` | Path-Based Timing Analysis Acceleration via Segment-Level Timing Arc Reuse | Circuit/timing corpus, arc-reuse conditions, setup/corner, slack correctness, runtime/memory, and STA baseline |
| 3 | `dac-2026-research257` | Specmoe: A Fast and Efficient Mixture-of-Experts Inference via Self-Assisted Speculative Decoding | MoE models, draft/verification policy, acceptance rate, quality, latency/throughput/energy, and ordinary decoding baseline |
| 4 | `dac-2026-research259` | HierPAS: Accelerating Video Generation Models with Hierarchical Precision and Adaptive Sparsity | Video-generation models/tasks, precision/sparsity policy, quality, hardware/runtime/energy, and dense/full-precision baseline |
| 5 | `dac-2026-research2596` | Exploiting Movable Logical Qubits for Lattice Surgery Compilation | Qubit/code/topology model, movement policy, circuit corpus, logical error/depth, compiler runtime, and fixed-layout baseline |
| 6 | `dac-2026-research2620` | Deinfer: Efficient Parallel Inferencing for Decomposed Large Language Models | Decomposition scheme, LLM suite, parallel runtime, quality, latency/throughput/energy, and monolithic baseline |
| 7 | `dac-2026-research2621` | Minimizing the Number of Code Switching Operations in Fault-Tolerant Quantum Circuits | FTQC code/circuit model, switching definition, compiler objective, logical correctness/error, depth/runtime, and prior compiler baseline |
| 8 | `dac-2026-research2631` | ARC-SRAM: A Memory Subarray with Local Addressing and Reduced Access Energy | SRAM process/array, access workload, local-address circuit, timing/retention/yield, area/energy, and conventional SRAM baseline |
| 9 | `dac-2026-research2637` | From Block to Range: Rethinking the Fundamental Unit of Log-Structured File Systems for ZNS SSDs | ZNS SSD/device, filesystem workloads, range-unit policy, correctness, latency/throughput/endurance, and block baseline |
| 10 | `dac-2026-research2642` | LLM4SDC: Leveraging Multi-Agent System for Automated SDC Generation and Benchmarking | SDC/RTL corpus, agents/models, constraint correctness, coverage/PPA, tool budget, and human/EDA baseline |

These are source-recovery priorities and condition checklists, not technical
rankings or temporal trend evidence.
