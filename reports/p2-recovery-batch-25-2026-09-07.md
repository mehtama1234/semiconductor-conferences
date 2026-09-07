# P2 recovery routing batch 25 — 2026-09-07

This tranche continues the DAC priority-3 frontier across MoE scheduling,
buffering, satellite federated learning, analog/CIM dynamics, quantum
compilation, PMU security, logic optimization, CPU DSE, and graph-based circuit
matching.

| Priority | Paper ID | Title | Evidence needed before quantitative use |
|---:|---|---|---|
| 1 | `dac-2025-research1019` | HybriMoE: Hybrid CPU-GPU Scheduling and Cache Management for Efficient MoE Inference | Model/router, CPU-GPU hardware, cache policy, traces, SLO/throughput/energy, and GPU-only baseline |
| 2 | `dac-2026-research094` | KL-MoE: A Hierarchical MoE Pruning Framework Exploiting KL Divergence | Models/tasks, pruning hierarchy, KL budget, quality/perplexity, hardware/runtime, and pruning baseline |
| 3 | `dac-2026-research1000` | Can Asymmetric Tile Buffering Be Beneficial? | Accelerator/memory target, tile shapes, workload suite, buffer sizing, bandwidth/area/energy, and symmetric baseline |
| 4 | `dac-2026-research1011` | Towards Fast and Robust Split Federated Learning over Satellite-Based Computing Networks | Satellite link traces, clients/model, split point, compression/optimization, convergence/accuracy, and conventional FL baseline |
| 5 | `dac-2026-research1016` | A Fully Analog Continuous-Time CIM Neural ODE Solver for Flow-Matching-Based Fluid Dynamics Generation | ODE/task suite, analog device/circuit, numerical precision, stability, area/energy/latency, and digital baseline |
| 6 | `dac-2026-research1036` | NEAT: A Neutral-Atom Transpiler for Joint Mapping and Scheduling of Syndrome Extraction Circuits | Neutral-atom device, QEC circuits, mapping/scheduling constraints, fidelity/depth/runtime, and transpiler baseline |
| 7 | `dac-2026-research1037` | Seeing the Unseen: Reverse Engineering Hidden PMU Events by Differential Analysis and Simulation Validation | CPU/platform, PMU events, attacker/access model, validation traces, accuracy/coverage, and disclosure limits |
| 8 | `dac-2026-research1042` | Gearls: Generalizable Reinforcement Learning Framework for Logic Optimization via Policy Similarity Metric | RTL/netlist corpus, RL training/test split, policy metric, PPA/correctness, transfer setting, and optimizer baseline |
| 9 | `dac-2026-research1047` | GenDSE: Generative CPU Design Space Exploration via Sequential Decision Making | CPU design space, generative policy, simulator/toolchain, workloads, PPA/constraint budget, and search baseline |
| 10 | `dac-2026-research1052` | Fast Template Matching for Quantum Circuits Using Hypergraph | Circuit corpus, hypergraph representation, match quality, rewrite correctness, runtime/memory, and graph baseline |

These are source-recovery priorities and condition checklists, not technical
rankings or temporal trend evidence.
