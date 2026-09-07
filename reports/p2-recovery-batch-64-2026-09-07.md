# P2 recovery routing batch 64 — 2026-09-07

This DAC-specific tranche covers semantic in-vehicle intrusion detection,
operator-aware LLM-training swap optimization, IGZO eDRAM LLM buffers,
asymmetric LLM checkpointing, PCIe peripheral-trace safety, 3D bonded clock
trees, superconducting retiming, model-checking lemma generation, prototype
processing-in-memory transactions, and runtime LLM tensor parallelism.

| Priority | Paper ID | Title | Evidence needed before quantitative use |
|---:|---|---|---|
| 1 | `dac-2026-research462` | SCIMI: Semantic-Aware Collaborative Intrusion Detection for Multi-Domain In-Vehicle Networks | Vehicle/network domains, threat model, collaboration protocol, detection/false-positive metrics, latency/energy, and IDS baseline |
| 2 | `dac-2026-research484` | Smartswap: Swap-Based Memory Optimization for LLM Training Under Varying Operator Sequences | LLM/training suite, memory hierarchy, operator-aware swap policy, convergence, throughput/memory/energy, and standard swap baseline |
| 3 | `dac-2026-research509` | MBA: Mega-Buffer Architecture Based on 1T1C IGZO eDRAM for Efficient LLM Inference | IGZO eDRAM process, LLM workloads, buffer policy, accuracy, latency/energy/area/retention, and SRAM/DRAM baseline |
| 4 | `dac-2026-research513` | Asymcheck: Asymmetric Partitioned Checkpointing for Efficient Large Language Model Training | Distributed platform, LLM/training traces, partition policy, recovery correctness, checkpoint time/storage/energy, and standard checkpoint baseline |
| 5 | `dac-2026-research514` | The Phantom of PCIe: Constraining Generative Artificial Intelligences for Practical Peripherals Trace Synthesizing | PCIe/peripheral corpus, threat model, generative model, trace correctness/safety, coverage/runtime, and unconstrained baseline |
| 6 | `dac-2026-research518` | Flexicts: CPPR-Aware 3D Clock Tree Synthesis for Face-to-Face Bonded ICs | 3D process/clock corpus, CPPR model, timing/CTS constraints, skew/power/area/DRC, runtime, and CTS baseline |
| 7 | `dac-2026-research520` | Duplication-Aware Retiming and Cell Interface Redesign for Superconductor Circuit Minimization | Superconductor process/library, circuit corpus, retiming/duplication rules, correctness/timing/area, and conventional synthesis baseline |
| 8 | `dac-2026-research523` | Legend: A Data-Driven Framework for Lemma Generation in Hardware Model Checking | Proof corpus, lemma model, solver/version, proof correctness/coverage/runtime, and hand-crafted baseline |
| 9 | `dac-2026-research529` | Onyx: Efficient Transaction Processing with Real Processing-in-Memory Prototypes | PIM prototype/device, transaction workloads, consistency model, correctness, throughput/latency/energy, and CPU baseline |
| 10 | `dac-2026-research538` | Amoeba: Runtime Tensor Parallel Transformation for LLM Inference Services | LLM/service suite, runtime transformation policy, quality, tail latency/throughput/energy, and static parallel baseline |

These are DAC-specific source-recovery priorities and condition checklists, not
technical rankings or temporal trend evidence.
