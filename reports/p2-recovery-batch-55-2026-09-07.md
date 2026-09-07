# P2 recovery routing batch 55 — 2026-09-07

This tranche resumes DAC-specific routing after the denominator reconciliation,
covering post-quantum RISC-V extensions, sparse 3D detection, flexible ZKPs,
robot VLA inference, verification-trained Verilog generation, MoE dataflow,
CNOT synthesis, RTL benchmarks, pangenome acceleration, and Rowhammer attacks
on PLONK proving systems.

| Priority | Paper ID | Title | Evidence needed before quantitative use |
|---:|---|---|---|
| 1 | `dac-2026-research2713` | Raise the Shields: A Modular RISC-V Extension for Post Quantum Cryptography | ML-DSA/KEM parameters, RISC-V target, threat model, correctness, latency/energy/area, and software baseline |
| 2 | `dac-2026-research2717` | Operator-Level Acceleration for Sparse 3D Object Detection | Detector/task suite, sparse operators, accelerator target, accuracy, latency/energy, and dense baseline |
| 3 | `dac-2026-research272` | ZK-Flex: A Flexible and Scalable Framework for Accelerating Zero-Knowledge Proofs | ZKP protocols, FPGA/ASIC target, security/precision, proof throughput/latency/energy, and CPU/GPU baseline |
| 4 | `dac-2026-research2721` | DySL-VLA: Efficient Vision-Language-Action Model Inference via Dynamic-Static Layer-Skipping for Robot Manipulation | Robot/VLA tasks, skip policy, action success/quality, latency/energy, and unskipped baseline |
| 5 | `dac-2026-research2737` | Insights from Verification: Training a Verilog Generation LLM Using Reinforcement Learning with Testbench Feedback | RTL corpus, model/training split, testbench feedback, functional/PPA success, compute budget, and supervised baseline |
| 6 | `dac-2026-research2753` | An Energy-Efficient Dataflow Architecture for Efficient MoE Model Inference | MoE models, dataflow/hardware target, quality, throughput/latency/energy, and GPU baseline |
| 7 | `dac-2026-research2756` | Lin-Search: Scaling Exact Synthesis of CNOT Circuits via Hybrid Iterative Deepening Search | CNOT circuit corpus, exactness criterion, search budget, gate count/depth/runtime, and synthesis baseline |
| 8 | `dac-2026-research2760` | Notsotiny: A Large, Living Benchmark for RTL Code Generation | Benchmark tasks/versions, evaluator correctness, leakage controls, pass/equivalence criteria, and prior benchmark baseline |
| 9 | `dac-2026-research2762` | Pangaea: A Unified Memory-Efficient Accelerator for Pangenome Chaining and Alignment | Pangenome/reference corpus, accelerator target, alignment correctness, throughput/memory/energy, and CPU/GPU baseline |
| 10 | `dac-2026-research2771` | PLONK-Hammer: Breaking Input Privacy of PLONK Proving Systems via Rowhammer | DRAM/platform, PLONK implementation, fault/threat model, exploit success, reproducibility, and hardened baseline |

These are DAC-specific source-recovery priorities and condition checklists, not
technical rankings or temporal trend evidence.
