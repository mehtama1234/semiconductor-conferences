# P2 recovery routing batch 4 — 2026-09-07

This tranche adds ten DAC description-only records spanning thermal-aware
inference, LLM memory behavior, accelerators, security, memory safety, RF
design, and cloud scheduling.

| Priority | Paper ID | Title | Evidence needed before quantitative use |
|---:|---|---|---|
| 1 | `dac-2026-research1302` | Active Imitation Learning for Thermal- and Kernel-Aware LFM Inference on 3D S-NUCA Many-Cores | Thermal model, many-core geometry, LFM workload, imitation targets, kernel/thermal baseline, and quality/throughput metric |
| 2 | `dac-2026-research1441` | An Adaptive Prediction of Tokens Fluctuation for Decoupled Prefetching to Accelerate Long-Context LLM Decoding | Model/context distribution, predictor training, prefetch accuracy, memory system, TTFT/decode metric, and baseline |
| 3 | `dac-2026-research1466` | Inferweave: Efficient LLM Inference on the MT-3000 Processor | MT-3000 configuration, model suite, compiler/runtime, precision, baseline GPU/CPU, and throughput/latency conditions |
| 4 | `dac-2026-research1582` | Slicemoe: Bit-Sliced Expert Caching Under Miss-Rate Constraints for Efficient MoE Inference | MoE routing traces, cache capacity, miss-rate target, bit-slice policy, memory hardware, and baseline cache |
| 5 | `dac-2026-research1628` | Attackonctf: Defending Hardware Security Competition Benchmarks in the Age of LLMs | Benchmark corpus, threat model, LLM capabilities, leakage/attack metric, defenses, and contamination controls |
| 6 | `dac-2026-research1715` | Semi-Virtual Addressing to Enhance Memory Safety on Microcontrollers | MCU/ISA, memory-safety threat model, address translation overhead, benchmark software, hardware implementation, and baseline protection |
| 7 | `dac-2026-research1804` | Perifi:physics-Infused RF Inverse Design with Parametric Data-Efficient Feasible-Region Sampling | RF device/process, feasible-region constraints, simulation budget, target metrics, optimizer baselines, and fabrication/measurement status |
| 8 | `dac-2026-research2884` | Voyager: An End-to-End Framework for Design-Space Exploration and Generation of DNN Accelerators | DNN suite, accelerator generator target, search budget, synthesis/PPA flow, correctness checks, and baseline generator |
| 9 | `dac-2026-research2970` | GREEN: Towards Scalable Energy-Efficient Workload Scheduling and Placement in the Cloud | Cloud hardware/workload traces, SLO definition, energy accounting, placement policy, baseline scheduler, and tail-latency constraints |
| 10 | `dac-2026-research343` | SpecANNS: Accelerating Graph-Based Approximate Nearest Neighbor Search with Speculative In-Storage Computing | Dataset/index scale, storage device, speculation correctness, recall/latency metric, query distribution, and baseline ANN engine |

The queue is for evidence recovery and review routing, not a ranking of
technical importance or program prevalence.
