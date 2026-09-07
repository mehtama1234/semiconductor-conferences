# P2 recovery routing batch 68 — 2026-09-07

This DAC-specific tranche covers early-stage thermal prediction, Monte Carlo
analog placement, probabilistically safe neural control, correlation-aware GKP
decoding, multilayer PCB rail/signal co-design, physics-informed power integrity,
serverless elastic MoE inference, stochastic diffusion transistor sizing,
hardware-aware CiM retrieval, and SAT-based delay-constrained area optimization.

| Priority | Paper ID | Title | Evidence needed before quantitative use |
|---:|---|---|---|
| 1 | `dac-2026-research706` | Early Design Stage Thermal Prediction and Optimization: Machine-Learning Driven Approach | Thermal/process/design corpus, ML model, boundary conditions, temperature error, optimization objective/runtime, and numerical baseline |
| 2 | `dac-2026-research713` | Alphaplacer: Analog Placement Enhanced by Monte Carlo Tree Search | Analog/PDK corpus, MCTS policy/budget, placement constraints, wirelength/congestion/timing/DRC, and placer baseline |
| 3 | `dac-2026-research720` | Provably Probabilistic Safe Controller Synthesis for Vision-Based Neural Network Control Systems | Vision/control tasks, plant model, safety probability definition, proof/verification conditions, runtime, and controller baseline |
| 4 | `dac-2026-research727` | A Correlation-Aware GKP Decoder for Fault-Tolerant Continuous-Variable Photonic Quantum Computers | Photonic hardware/noise, GKP code/circuit suite, correlation model, logical error rate, decoder latency/energy, and decoder baseline |
| 5 | `dac-2026-research732` | Unified Rail-Signal Co-Design for Multilayer PCBs: Resource Allocation, IR-Drop, and Routability | PCB/process corpus, rail/signal constraints, IR-drop/routability metrics, timing/area/runtime, and conventional flow baseline |
| 6 | `dac-2026-research733` | PIANO: Physics-Informed Admittance Neural Operator for Fast Power Integrity Analysis | PDN/design corpus, physics constraints, operator model, voltage/error/runtime, and SPICE/numerical baseline |
| 7 | `dac-2026-research734` | Smoe: Elastic MoE-Based Inference with Serverless Computing via Fine-Grained Expert Scaling | MoE models, serverless platform, expert-scaling policy, quality, tail latency/throughput/cost/energy, and static baseline |
| 8 | `dac-2026-research739` | Stochastic Diffusion Prior: Knowledge Elicitation and Local Adaptation for Transistor Sizing | Device/process/circuit corpus, diffusion prior, adaptation policy, PPA/constraint quality, search budget, and sizing baseline |
| 9 | `dac-2026-research752` | CQ-CiM: Hardware-Aware Embedding Shaping for Robust CiM-Based Retrieval | CiM device/variation, retrieval models/corpus, embedding shaping, recall/accuracy, throughput/energy, and unshaped baseline |
| 10 | `dac-2026-research754` | Delay-Constrained Area Optimisation Using SAT-Based Local Improvement | Cell/design corpus, delay constraints, SAT/local-search budget, area/timing/DRC, correctness, and optimizer baseline |

These are DAC-specific source-recovery priorities and condition checklists, not
technical rankings or temporal trend evidence.
