# P2 recovery routing batch 57 — 2026-09-07

This DAC-specific tranche covers HB-DRAM bandwidth-aware LLM acceleration,
IoT ISA extensions, structured signal-temporal-logic transformation, graph-based
IP protection, Floquet PPV computation, parallel SAT, adaptive Gaussian
splatting, parallel equivalence checking, CGRA energy estimation, and LLM Rust
repair.

| Priority | Paper ID | Title | Evidence needed before quantitative use |
|---:|---|---|---|
| 1 | `dac-2026-research282` | Hiband: A Hierarchical Bandwidth-Aware HB-DRAM Accelerator with Array-Level Co-Execution and Reconfigurable NoC for LLM Inference | HB-DRAM stack/process, LLM suite, bandwidth/NoC policy, quality, latency/energy/area, and GPU/DRAM baseline |
| 2 | `dac-2026-research2824` | ISA-PM: A Unified ISA Extension and Microarchitecture Enabling Efficient ECPM in IoT Devices | ECPM workload/parameters, ISA/microarchitecture, security/correctness, latency/area/energy, and software baseline |
| 3 | `dac-2026-research2829` | LLM-Enhanced Two-Stage Signal Temporal Logic Automatic Transformation with Structured Intermediate Representation | STL corpus, LLM/version, intermediate representation, semantic correctness, coverage/runtime, and rule-based baseline |
| 4 | `dac-2026-research2832` | Nothing Left to Learn: Isomorphic Graph Transformations for Hardware IP Protection | IP/netlist corpus, threat model, transformation policy, functional/security metrics, overhead, and obfuscation baseline |
| 5 | `dac-2026-research2838` | Floquet-Based Subspace Projection Method for Time-Domain PPV Computation | Circuit/oscillator corpus, Floquet model, numerical settings, error/runtime, stability scope, and conventional PPV baseline |
| 6 | `dac-2026-research284` | PRS: An Efficient Parallel SAT Framework | SAT benchmark suite, solver/platform, parallel scheduling, proof correctness, runtime/memory, and SAT baseline |
| 7 | `dac-2026-research2845` | Adagscale: Viewpoint-Adaptive Gaussian Scaling in 3D Gaussian Splatting to Reduce Gaussian-Tile Pairs | 3D scenes/viewpoints, scaling policy, image-quality metric, frame rate/memory/energy, and unscaled baseline |
| 8 | `dac-2026-research285` | Parallel Combinational Equivalence Checking via Sweeping-Based Task Scheduling | RTL/netlist corpus, equivalence semantics, parallel platform, proof rate/time/memory, and sequential checker baseline |
| 9 | `dac-2026-research2851` | An Agile and Accurate Energy Estimation Methodology for CGRA-Mapped Algorithms: The Synchoros Approach | CGRA/process, mapped algorithm suite, energy model calibration, error/runtime, and simulator/measurement baseline |
| 10 | `dac-2026-research2871` | Akirarust: Re-Thinking LLM-Aided Rust Repair Using a Feedback-Guided Thinking Switch | Rust bug corpus, model/version, feedback loop, patch correctness, test budget, and standard LLM repair baseline |

These are DAC-specific source-recovery priorities and condition checklists, not
technical rankings or temporal trend evidence.
