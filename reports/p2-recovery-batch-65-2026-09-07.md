# P2 recovery routing batch 65 — 2026-09-07

This DAC-specific tranche covers dual-rail DRAM logic, electro-physical cell
PPA modeling, configurable CPU matrix extensions, PDE foundation models for
3D-IC thermal simulation, coordinated CUDA kernel evolution, private multi-GPU
inference, hardware-calibrated quantum NAS, graph reduction accelerators,
flash-SSD code-length adaptation, and knowledge-driven SSD management.

| Priority | Paper ID | Title | Evidence needed before quantitative use |
|---:|---|---|---|
| 1 | `dac-2026-research544` | DRCA: Reliable Bitwise Logic in DRAM via Dual-Rail Compute and Access | DRAM process/fault model, logic workload, dual-rail circuit, correctness/reliability, latency/energy/area, and standard DRAM baseline |
| 2 | `dac-2026-research550` | Epicell: Electro-Physical Co-Modeling for Standard Cell PPA Prediction | Cell library/process, electro-physical data, model split, PPA prediction error, transfer scope, and conventional predictor baseline |
| 3 | `dac-2026-research552` | UCME: Unified and Configurable Matrix Extension for Diverse CPU Architectures with Minimal Design Overhead | CPU ISA/platforms, matrix workload suite, extension design, correctness, throughput/area/energy, and fixed-ISA baseline |
| 4 | `dac-2026-research553` | From Fluid Dynamics to Chip Design: PDE Foundation Model Address Data Bottleneck in 3D-ICs Thermal Simulation | 3D-IC/PDE corpus, foundation-model training, boundary conditions, temperature error/runtime, and numerical solver baseline |
| 5 | `dac-2026-research561` | Cupilot: A Strategy-Coordinated Multi-Agent Framework for CUDA Kernel Evolution | CUDA/kernel corpus, agents/models, strategy/search budget, correctness, performance/energy, and single-agent baseline |
| 6 | `dac-2026-research574` | Multi-GPU Tensor-Level Fusion and Adaptive Memory Management for Private Inference | Private-inference model suite, GPU platform, fusion/memory policy, quality, latency/throughput/energy, and ordinary serving baseline |
| 7 | `dac-2026-research577` | Closing the Loop: Hybrid NAS Guided by Analytical and Hardware-Calibrated Quantum Cost Modeling | Quantum workload/circuit corpus, cost model calibration, NAS/search budget, fidelity/depth/runtime, and standard NAS baseline |
| 8 | `dac-2026-research588` | Florella: Accelerating Graph Neural Networks by Sliding Reduction Convention and Flexible Architecture | GNN suite, graph/dataflow policy, accelerator target, accuracy, throughput/memory/energy, and GPU baseline |
| 9 | `dac-2026-research607` | COLA: Enabling Low-Latency Reads for Flash-Based SSDs via Code Length Adaptation | Flash generation/process, read workload, code-length policy, latency/error/endurance, and fixed-code baseline |
| 10 | `dac-2026-research609` | Knowledge-Driven Hybrid SSD Management Enhanced by Fine-Tuned LLMs | SSD/device/workload traces, fine-tuning data, management policy, correctness/latency/endurance, and conventional manager baseline |

These are DAC-specific source-recovery priorities and condition checklists, not
technical rankings or temporal trend evidence.
