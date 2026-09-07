# P2 recovery routing batch 45 — 2026-09-07

This tranche continues the DAC frontier across advanced routing, equivalence
checking, LLM-assisted DRC repair, reconfigurable systolic arrays, Ising
optimization, diffusion-language-model serving, parasitic extraction, hardware
Trojan detection, asymmetric LLM quantization, and MoE scheduling.

| Priority | Paper ID | Title | Evidence needed before quantitative use |
|---:|---|---|---|
| 1 | `dac-2026-research2139` | Flip-FET-Based VLSI Design Framework with Congestion-Aware Dual-Side Routing | Flip-FET technology/PDK, benchmark designs, dual-side routing constraints, congestion/timing/DRC, runtime, and conventional-router baseline |
| 2 | `dac-2026-research214` | Miter-Aware LUT Mapping: Aligning Structure and Solvability for Efficient Logic Equivalence Checking | FPGA LUT architecture, circuit suite, miter construction, equivalence solver, proof rate/time/memory, and mapper baseline |
| 3 | `dac-2026-research2145` | Drcagent: A Design Rule Aware LLM Agent for DRC Auto-Fix with Adversarial Reinforcement Learning | PDK/rule deck, violation corpus, LLM/version, adversarial RL budget, fix correctness/coverage/PPA, and manual/EDA baseline |
| 4 | `dac-2026-research2157` | RFIPSA: A Reconfigurable FIP-Based Systolic Array for Various Matrix-Intensive Workloads | FIP definition, matrix workload suite, target FPGA/ASIC, reconfiguration cost, throughput/energy/area, and fixed-array baseline |
| 5 | `dac-2026-research2159` | PMTPA: An Ising Model-Based Parallel-Momentum Tempering Processing Architecture for Combinatorial Optimization | Problem instances, Ising encoding, tempering/momentum policy, solution quality, convergence/runtime/energy, and classical/annealing baseline |
| 6 | `dac-2026-research2169` | Orchestrating Dual-Boundaries: An Arithmetic Intensity Inspired Acceleration Framework for Diffusion Language Models | Diffusion-LM models/tasks, arithmetic-intensity classifier, execution stages, quality, latency/energy, and standard serving baseline |
| 7 | `dac-2026-research2177` | GTX: Graph Transformer for Parasitic Extraction on Analog Circuits | Circuit/layout corpus, parasitic labels, graph-transformer architecture, extraction error, runtime/memory, and conventional extractor baseline |
| 8 | `dac-2026-research2179` | Detrojan: Detecting Trojan Circuits Using a Purpose-Built Graph Neural Network with Community-Enhanced Classification | Trojan taxonomy/corpus, graph construction, train/test split, detection/false-positive metrics, robustness, and detector baseline |
| 9 | `dac-2026-research2184` | Adana: Accelerating Large Language Models via Adaptive Nonuniform Asymmetric Quantization | LLM/model suite, quantizer calibration, bit-width/asymmetry policy, accuracy, hardware/runtime/energy, and uniform-quantization baseline |
| 10 | `dac-2026-research2199` | Expertflow: Efficient Mixture-of-Experts Inference via Predictive Expert Caching and Token Scheduling | MoE models/workloads, cache predictor, token scheduler, hit/miss and quality effects, latency/energy/memory, and uncached baseline |

These are source-recovery priorities and condition checklists, not technical
rankings or temporal trend evidence.
