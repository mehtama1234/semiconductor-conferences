# P2 recovery routing batch 38 — 2026-09-07

This tranche continues the DAC frontier across IoT protocol fuzzing, self-evolved
EDA tools, Verilog-A/MRAM co-optimization, page-table-walk attacks, FPGA compiler
testing, post-quantum LPN acceleration, factored floating-point MACs, sparse LLM
inference, log-schema extraction, and package cooling-aware thermal prediction.

| Priority | Paper ID | Title | Evidence needed before quantitative use |
|---:|---|---|---|
| 1 | `dac-2026-research177` | Finding Behavior Bugs in IoT Messaging Protocols with Automated Oracle Generation and Monitoring | Protocol/device corpus, oracle construction, threat/test model, bug validation, coverage/runtime, and fuzzer baseline |
| 2 | `dac-2026-research1784` | Autonomous Evolution of EDA Tools: Multi-Agent Self-Evolved ABC | ABC/tool version, circuit corpus, agent/model loop, correctness/PPA, search budget, and standard ABC baseline |
| 3 | `dac-2026-research179` | LLMVA: LLMs Empowered Verilog-A Iterative for MRAM Design Technology Co-Optimization | MRAM/device/PDK corpus, LLM/version, Verilog-A correctness, device metrics, convergence budget, and manual baseline |
| 4 | `dac-2026-research1793` | Stone-Skimming: Attacking Big-Data Analytics Applications with Page Table Walk | CPU/OS/platform, attacker model, analytics workloads, leakage/impact metric, reproducibility, and mitigations |
| 5 | `dac-2026-research1813` | RL4HDL: Code Diversity Guided FPGA Logic Synthesis Compiler Testing Via Reinforcement Learning | FPGA compiler/tool, RTL corpus, diversity/reward, bug/coverage metric, training budget, and testing baseline |
| 6 | `dac-2026-research1822` | Leveraging AI-Inspired Hardware Architecture to Enhance LPN Acceleration in Post-Quantum Cryptography | LPN/PQC parameters, architecture/device, correctness/security, throughput/area/energy, and software baseline |
| 7 | `dac-2026-research1837` | Factored Floating-Point MAC: Eliminating Redundant Normalization for Energy-Efficient Systolic Arrays | Model/precision suite, numerical error, systolic architecture, PPA/throughput/energy, and conventional MAC baseline |
| 8 | `dac-2026-research1839` | Accelerating GPU Inference of Large Language Models with Moderately Unstructured Sparse Weight Matrices | LLM models/sparsity, GPU/kernel, quality metric, sparse format, throughput/energy, and dense/sparse baseline |
| 9 | `dac-2026-research1841` | Schemacoder: Automatic Log Schema Extraction Coder with Residual Q-Tree Boosting | Log corpus, schema definition, model/training split, extraction accuracy, runtime/memory, and rule/ML baseline |
| 10 | `dac-2026-research1846` | COOL: A Cooling-Aware Point Transformer Framework for Thermal Prediction in Advanced 3D/3.5D IC Packaging | Package/thermal corpus, point-transformer model, physics/measurement validation, error/runtime, and solver baseline |

These are source-recovery priorities and condition checklists, not technical
rankings or temporal trend evidence.
