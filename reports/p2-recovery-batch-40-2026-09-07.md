# P2 recovery routing batch 40 — 2026-09-07

This tranche continues the DAC frontier across DRAM-PIM interference, in-vehicle
attack tracing, personalized edge MoE, federated-learning energy, multi-GPU
translation, circuit graph learning, FPGA prefill/decode swapping, safety
assertions, side-channel leakage estimation, and hyperdimensional LiDAR.

| Priority | Paper ID | Title | Evidence needed before quantitative use |
|---:|---|---|---|
| 1 | `dac-2026-research1909` | Pimony: A DRAM-PIM Design for Harmonizing PIM and Memory Accesses with Minimal Interference | DRAM/PIM device, workload/interference traces, scheduling/dataflow, throughput/energy, correctness, and baseline |
| 2 | `dac-2026-research1920` | Graph-Based Attack-Chain Traceback Across Multiple In-Vehicle Network Domains | Vehicle/network topology, attack corpus, graph construction, traceback accuracy/latency, threat assumptions, and IDS baseline |
| 3 | `dac-2026-research1922` | Pegasus: Personalized and Communication-Efficient Mixture-of-Experts System for Distributed Edge LLM Inference | Edge devices/models, personalization objective, expert placement, communication traces, quality/latency/energy, and baseline |
| 4 | `dac-2026-research1936` | RTFL: Energy-Aware Federated Learning for AIoT Design Via Adaptive Quantization-Based Multi-Agent Scheduling | AIoT devices/traces, quantization policy, multi-agent schedule, convergence/accuracy, energy/latency, and FL baseline |
| 5 | `dac-2026-research1938` | Phantom Walk: Reducing the Post-Migration Translation Path via Proactive Translation Dissemination in Multi-GPU Systems | GPU/OS/interconnect, migration traces, translation protocol, hit/latency/overhead, and standard migration baseline |
| 6 | `dac-2026-research194` | TRACE: Learning to Compute on Circuit Graphs | Circuit corpus, graph task, model/split, accuracy/transfer, runtime/memory, and graph-learning baseline |
| 7 | `dac-2026-research1942` | PD-Swap: Prefill–decode Logic Swapping for End-to-End LLM Inference on Edge FPGAs via Dynamic Partial Reconfiguration | FPGA/device, LLM models, reconfiguration time, workload/SLO, throughput/energy, and static design baseline |
| 8 | `dac-2026-research1945` | Safegen: LLM-Driven Assertion Generation and Fault Criticality Evaluation for Functional Safety | Safety/RTL corpus, LLM/version, assertion correctness, fault model, coverage/runtime, and human/tool baseline |
| 9 | `dac-2026-research1949` | Athena: Analytical Timing-Aware Pre-Silicon Estimation of Side-Channel Leakage | Process/circuit corpus, leakage/threat model, timing analytical model, calibration/accuracy, runtime, and post-silicon baseline |
| 10 | `dac-2026-research1960` | Hyperlidar: Adaptive Post-Deployment LiDAR Segmentation via Hyperdimensional Computing | LiDAR datasets/drift, HDC representation, adaptation protocol, segmentation quality/latency/energy, and fixed-model baseline |

These are source-recovery priorities and condition checklists, not technical
rankings or temporal trend evidence.
