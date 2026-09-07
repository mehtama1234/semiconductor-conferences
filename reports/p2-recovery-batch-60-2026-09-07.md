# P2 recovery routing batch 60 — 2026-09-07

This DAC-specific tranche covers on-device gesture model selection, segmented
ADC measurement, blind ADC calibration, multi-node Boolean synthesis, encrypted
secure-inference routing, 3D FPGA placement, exponent coding for chiplets,
wafer-level tool-chain attestation, touchscreen electromagnetic leakage, and
Boolean hardware emulation.

| Priority | Paper ID | Title | Evidence needed before quantitative use |
|---:|---|---|---|
| 1 | `dac-2026-research3067` | Scale-Gest: Scalable Model-Space Synthesis and Runtime Selection for On-Device Gesture Detection | Gesture tasks/data, model-space synthesis, device/runtime policy, accuracy, latency/energy/memory, and fixed-model baseline |
| 2 | `dac-2026-research3082` | UGLMS-uSMILE: Live Measurement Sequencing for Segmented Linearity Identification in ADCs | ADC resolution/device, measurement model, sequencing policy, error/coverage, acquisition time/energy, and conventional test baseline |
| 3 | `dac-2026-research3087` | Train Once, Calibrate Always: Machine-Learning-Assisted Blind Calibration for Analog-to-Digital Converters | ADC/process/mismatch, calibration data, ML model, linearity/error, sample/compute budget, and conventional calibration baseline |
| 4 | `dac-2026-research3091` | Shared Logic Unleashed: Multiple-Node Boolean Optimization for Next-Gen Synthesis | Boolean/circuit corpus, optimization semantics, synthesis tool, area/timing/power/correctness, and baseline synthesis flow |
| 5 | `dac-2026-research3092` | Securerouter: Encrypted Routing for Efficient Secure Inference | Encryption/security model, network/workload suite, routing policy, accuracy, latency/energy/area, and plaintext baseline |
| 6 | `dac-2026-research3100` | Escaping Flatland: A Placement Flow for Enabling 3D FPGAs | 3D FPGA process/architecture, benchmark suite, placement constraints, wirelength/congestion/timing/thermal, and 2D baseline |
| 7 | `dac-2026-research3121` | LEXI: Lossless Exponent Coding for Efficient Inter-Chiplet Communication in Hybrid LLMs | LLM/chiplet workloads, coding format, losslessness/precision, link traffic, latency/energy/area, and uncoded baseline |
| 8 | `dac-2026-research3145` | STAMP: Semiconductor Tool-Chain Attestation Through Wafer-Level Machine Learning-Based Process Monitoring | Wafer/process data, threat model, ML detector, attestation correctness/coverage, false positives, and conventional monitoring baseline |
| 9 | `dac-2026-research315` | Capacitive Touchscreens at Risk: Recovering Handwritten Trajectory on Smartphone via Electromagnetic Emanations | Smartphone/touchscreen hardware, EM acquisition, threat/noise model, trajectory recovery accuracy, sample/distance budget, and mitigation baseline |
| 10 | `dac-2026-research3153` | A Boolean Processor-Based Hardware Emulation System with Reconfigurable Interconnects | Boolean processor/FPGA platform, emulation workloads, interconnect configuration, correctness, throughput/latency/energy, and conventional emulator baseline |

These are DAC-specific source-recovery priorities and condition checklists, not
technical rankings or temporal trend evidence.
