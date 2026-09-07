# P2 recovery routing batch 58 — 2026-09-07

This DAC-specific tranche covers AI-assisted SoC security assertions, effective-
resistance hypergraph sampling, AI ASICs for ZKPs, expandable-register ISA
extensions, LUT qubit readout, intra-device speculative decoding, spiking-model
fine-tuning, neural-field robot control, remote ML-KEM side channels, and
in-storage Ethereum analytics.

| Priority | Paper ID | Title | Evidence needed before quantitative use |
|---:|---|---|---|
| 1 | `dac-2026-research2886` | ATLAS: AI-Assisted Threat-to-Assertion Learning for System-on-Chip Security Verification | Threat/assertion corpus, LLM/model, property correctness, coverage/formal budget, and manual baseline |
| 2 | `dac-2026-research2887` | Hyperefs: Adaptive Clique Sampling for Scalable Effective Resistance Estimation in Large Hypergraphs | Hypergraph corpus, sampling policy, estimator error, scalability/runtime/memory, and exact/sampling baseline |
| 3 | `dac-2026-research2888` | Enabling AI ASICs for Zero Knowledge Proof | ZKP protocols, ASIC/process, security/precision, proof throughput/latency/energy/area, and CPU/GPU baseline |
| 4 | `dac-2026-research2897` | EXRA: Efficient Execution of Data-Dominated Applications via ISA Extensions for Expandable Register Files | ISA/platform, application corpus, register-file design, correctness, performance/energy/area, and conventional ISA baseline |
| 5 | `dac-2026-research2914` | LUNA: LUT-Based Neural Architecture for Fast and Low-Cost Qubit Readout | Qubit/readout corpus, LUT architecture, fidelity, latency/area/energy, and classifier baseline |
| 6 | `dac-2026-research292` | Throughput-Oriented Speculative Decoding via Intra-Device Parallelism | LLM suite, draft/verification policy, acceptance/quality, throughput/latency/energy, and standard decoding baseline |
| 7 | `dac-2026-research293` | SkiST: Memory-Efficient Fine-Tuning of Spiking Neural Networks via Spatio-Temporal Adaptation | SNN/task suite, adaptation method, memory/precision, accuracy/convergence, latency/energy, and standard fine-tuning baseline |
| 8 | `dac-2026-research2959` | ENACT: Ensemble Neural Fields for Reactive Robot Control | Robot/platform/tasks, neural-field ensemble, success/safety, latency/energy, and controller baseline |
| 9 | `dac-2026-research296` | A Remote Side-Channel Attack on Post-Quantum Key Encapsulation Mechanisms: A Case Study of ML-KEM on Intel x86 | ML-KEM parameter set, Intel CPU/platform, remote threat/noise, key-recovery success, trace/query budget, and hardened baseline |
| 10 | `dac-2026-research297` | Etherssd: An In-Storage Ethereum Analytics Platform with Minimized I/O and Authentication Overhead | Blockchain/workload corpus, SSD/storage device, authentication model, correctness, throughput/latency/energy, and host baseline |

These are DAC-specific source-recovery priorities and condition checklists, not
technical rankings or temporal trend evidence.
