# P2 recovery routing batch 41 — 2026-09-07

This tranche continues the DAC frontier across quantum power-system solvers,
Hamiltonian pretraining, ATPG-free test insertion, diffusion acceleration,
row-aligned PIM attention, PCB 3D generation, adaptive quantization, ternary
LLM inference, transistor placement/routing, and transistor-network synthesis.

| Priority | Paper ID | Title | Evidence needed before quantitative use |
|---:|---|---|---|
| 1 | `dac-2026-research1963` | Optimized Time-Dependent Hamiltonian Evolution Quantum Solver for Power System Transient Computations | Power-system/PDE corpus, Hamiltonian discretization, quantum/noise model, error/runtime/resource metrics, and classical solver baseline |
| 2 | `dac-2026-research1966` | A Hamiltonian-Guided Pre-Trainer for Variational Quantum Algorithms | VQA tasks/ansatz, training corpus, Hamiltonian guidance, noise/fidelity/convergence, compute budget, and pretraining baseline |
| 3 | `dac-2026-research1971` | Test Point Insertion with ATPG-Free Self-Supervised Learning | Circuit/fault corpus, self-supervised labels, test-point constraints, coverage/area/timing/power, and ATPG baseline |
| 4 | `dac-2026-research1976` | Cacheparallel: Comprehensively Exploring Multi-Level Acceleration for Diffusion Models | Diffusion models/tasks, cache levels, reuse policy, quality, latency/energy/memory, and uncached baseline |
| 5 | `dac-2026-research1986` | REFLEX: Rewrite-Free Row-Aligned Sparse Attention for Efficient LLM Execution on PIM | PIM technology, LLM/workload suite, row alignment, accuracy, bandwidth/latency/energy, and conventional attention baseline |
| 6 | `dac-2026-research1991` | PCBgen3D: A Self-Correcting Graph-Based MLLM Framework for Automated PCB 3D Models Generation | PCB corpus, MLLM/version, graph/3D representation, geometric correctness, correction budget, and CAD baseline |
| 7 | `dac-2026-research1999` | HAP: Efficient Quantization Harnessing Adaptive Precision for DNN Hardware Acceleration | Models/tasks, adaptive-precision policy, quality metric, hardware target, latency/energy/area, and fixed-precision baseline |
| 8 | `dac-2026-research200` | Ternainfer: Pushing the Compression Boundary of Ternary LLMs Towards 1.58-Bit GPU Inference | LLM models/tasks, ternary training/quantization, GPU/kernel, perplexity/quality, throughput/energy, and higher-bit baseline |
| 9 | `dac-2026-research2006` | Cell-Structure-Independent Transistor-Level Placement and MOL-Aware Routing Framework Beyond the Standard-Cell Paradigm | Device/PDK corpus, transistor/MOL rules, objective/PPA, DRC correctness, runtime, and standard-cell baseline |
| 10 | `dac-2026-research2007` | Transsyn: Scalable, Area-Oriented Transistor Network Synthesis via Cut-Based Mapper with SAT-Based Refinement | Logic/cell corpus, synthesis semantics, cut/SAT search, area/timing/power, correctness, and synthesis baseline |

These are source-recovery priorities and condition checklists, not technical
rankings or temporal trend evidence.
