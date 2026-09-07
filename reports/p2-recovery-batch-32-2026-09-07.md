# P2 recovery routing batch 32 — 2026-09-07

This tranche continues the DAC frontier across cryptographic verification,
sparse GEMM, SAR graph optimization, equivalence checking, FIT prediction,
heterogeneous FPGA placement, RF synthesis, NPU dataflow, VRRAM/CIM vision,
and MoE checkpointing.

| Priority | Paper ID | Title | Evidence needed before quantitative use |
|---:|---|---|---|
| 1 | `dac-2026-research1378` | Leveraging Invariants for Scalable Verification of RISC-V Cryptography Extensions | ISA/crypto extensions, invariant/proof method, RTL corpus, completeness/correctness, runtime, and verifier baseline |
| 2 | `dac-2026-research138` | PFGEMM: Fully Exploiting the Parallelism of SpGEMM With Element-Wise Out-of-Order Execution Flow and Prefix Decomposition of Indices | Sparse matrix suite, format/distribution, hardware target, out-of-order method, throughput/energy, and SpGEMM baseline |
| 3 | `dac-2026-research1382` | Accelerating AI+SAR Applications Through Enhanced Graph Optimization | SAR/AI workloads, graph transformations, datasets, accelerator/runtime, quality/latency/energy, and baseline |
| 4 | `dac-2026-research1388` | Parallel Combinational Equivalence Checking Through Factored Form Sharing | RTL/netlist corpus, equivalence semantics, factoring method, proof completeness, parallel hardware/runtime, and checker baseline |
| 5 | `dac-2026-research1390` | ATLAS: Asynchronous Topological Learning for Accurate FIT Prediction via Decoupled Graph Neural Networks | FIT/soft-error corpus, graph construction, asynchronous training, accuracy/calibration, transfer split, and predictor baseline |
| 6 | `dac-2026-research1404` | Learning-Based Slack-Aware Timing-Driven Global Placement for Large-Scale Heterogeneous FPGAs | FPGA architecture/design corpus, slack/timing model, learning split, wirelength/congestion/PPA, runtime, and placer baseline |
| 7 | `dac-2026-research1407` | COmPOSER: Circuit Optimization of mm-Wave/rf Circuits with Performance-Oriented Synthesis for Efficient Realizations | RF process/circuit corpus, synthesis constraints, frequency/power/gain metrics, convergence budget, and RF CAD baseline |
| 8 | `dac-2026-research1409` | CODA: A Computation-Data Decoupled Dataflow Paradigm for DNN Computing on NPUs | NPU architecture, DNN suite, dataflow mapping, precision, throughput/energy/area, and conventional NPU baseline |
| 9 | `dac-2026-research1412` | Reconfigurable 3D-VRRAM LUT-CiM with Greedy G-Shuffle Quantization for End-to-End 4-Bit ViTs in Edge Dense Prediction | VRRAM/CIM device, ViT/dense-prediction suite, quantization quality, reconfiguration/endurance, PPA, and digital baseline |
| 10 | `dac-2026-research1414` | Expcheck: Dynamic Expert-Aware Checkpointing for Mixture-of-Experts Based Models | MoE models/traces, checkpoint policy, failure/recovery model, memory/I/O overhead, training quality/time, and static checkpoint baseline |

These are source-recovery priorities and condition checklists, not technical
rankings or temporal trend evidence.
