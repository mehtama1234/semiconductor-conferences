# P2 recovery routing batch 71 — 2026-09-07

This DAC-specific tranche covers shape-controlled single-flux-quantum placement,
trusted-domain snapshots, RTL timing prediction, unified TFHE acceleration,
parallel approximate reachability, encrypted-neural-network configuration,
hybrid-bonded 3D placement, self-supervised toggle propagation, cross-PDK DRC
generation, and application-specific FHE accelerator design.

| Priority | Paper ID | Title | Evidence needed before quantitative use |
|---:|---|---|---|
| 1 | `dac-2026-research875` | Jsplace: A Shape-Controllable and Length-Matching Placement for Rapid Single-Flux-Quantum Circuits | SFQ process/library, circuit corpus, shape/length constraints, timing/area/DRC, runtime, and placer baseline |
| 2 | `dac-2026-research876` | Tdsnap: Enabling Secure Function-as-a-Service with Trusted Domain Snapshots | TEE/platform, snapshot threat model, workload/state size, confidentiality/integrity, downtime/storage/latency, and conventional FaaS baseline |
| 3 | `dac-2026-research883` | RTL-Sequencer: Towards Scalable RTL Timing Prediction with the Sequence-Based Paradigm | RTL/design corpus, sequence model, timing labels, split/leakage controls, error/runtime, and STA/ML baseline |
| 4 | `dac-2026-research885` | Chimera: A Unified FHE Accelerator with Enhanced Compatibility for TFHE | FHE/TFHE parameters, device/process, workload suite, correctness/security, throughput/latency/energy/area, and CPU/GPU baseline |
| 5 | `dac-2026-research896` | Parallelizing Complementary Approximate Reachability | Control/PDE task corpus, approximation/error model, parallel platform, correctness/bounds, runtime/memory, and exact baseline |
| 6 | `dac-2026-research897` | MACH: Memory-Aware Configuration Generation for Homomorphically Encrypted Neural Networks | HE scheme/parameters, neural models, memory/configuration policy, accuracy, latency/memory/energy, and fixed configuration baseline |
| 7 | `dac-2026-research900` | Integrated Timing-Driven Placement for Hybrid-Bonding-Based Face-to-Face 3D ICs | Hybrid-bonding process, 3D design corpus, timing/placement constraints, wirelength/congestion/thermal/DRC, runtime, and placer baseline |
| 8 | `dac-2026-research906` | LEAP: A Self-Supervised Per-Cycle Toggle Propagation Model Supports Fast, Transferable, and Early Analysis of Layout Power | RTL/layout corpus, self-supervised split, toggle labels, power error/transfer/runtime, and power-analysis baseline |
| 9 | `dac-2026-research907` | DRCGen: A Controllable DRC Violation Case Generator with Cross-PDK Transferability for Rule-Deck and Tool Validation | PDK/rule decks, violation corpus, generator model, validity/coverage/transfer, runtime, and existing-case baseline |
| 10 | `dac-2026-research912` | Hades: Harnessing Architecture Design Automation for Application-Specific FHE Accelerators | FHE application/parameters, accelerator architecture, design-space method, correctness/security, PPA/latency/energy, and generic baseline |

These are DAC-specific source-recovery priorities and condition checklists, not
technical rankings or temporal trend evidence.
