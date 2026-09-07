# P2 recovery routing batch 74 — 2026-09-07

This closing DAC inventory tranche covers CXL near-memory ANN processing,
multi-fidelity microarchitecture search, LLM-driven technology mapping, LLM HLS
design-space exploration, zkSNARK NTT acceleration, sparse-streaming
multi-tenancy, MPC nonlinear inference, and diffusion-transformer video
generation.

| Priority | Paper ID | Title | Evidence needed before quantitative use |
|---:|---|---|---|
| 1 | `dac-2026-research108` | CANNON: A CXL-Based Near-Memory Processing Architecture for Approximate Nearest Neighbor Search on Real Hardware | CXL hardware/topology, ANN index and query corpus, recall target, memory baseline, end-to-end latency/throughput/energy, and measured-vs-modeled boundary |
| 2 | `dac-2026-research1186` | Xsearch: Exploring Microarchitecture Design Space Through Bayesian Optimization and Cross Evaluation on Multi-Fidelity Simulators | Simulator fidelity levels, architecture space, Bayesian policy, cross-evaluation protocol, search budget, QoR metrics, and exhaustive/optimizer baselines |
| 3 | `dac-2026-research535` | Mappingevolve: LLM-Driven Code Evolution for Technology Mapping | Circuit corpus, LLM/model/version, evolution prompts and budget, ABC/tool settings, area-delay objective, correctness, and mapping baseline |
| 4 | `dac-2026-research865` | Paretopilot: Global Optimization Reasoning on HLS Design Space Exploration with LLMs | HLS benchmark/device/tool suite, prompt/model, search budget, Pareto objective, synthesis timeout, correctness, and optimizer baseline |
| 5 | `dac-2026-research983` | ATTINA: Spatial Acceleration of Additive Number Theoretic Transform for Energy-Efficient zkSNARKs at the Edge | zkSNARK/NTT parameter sets, precision, edge hardware, proof correctness, throughput/latency/energy/area, and software baseline |
| 6 | `dac-2026-research986` | Procyon: Promoting Fine-Grained Multi-Tenancy to Optimize Sparse Streaming Accelerators | Accelerator architecture, tenant/workload mix, sparsity model, isolation policy, QoS/throughput/energy/area, and single-tenant baseline |
| 7 | `dac-2026-research989` | TAMI-MPC: Trusted Acceleration of Minimal-Interaction MPC for Efficient Nonlinear Inference | MPC protocol/security model, nonlinear workload, trust assumptions, hardware/software platform, communication/latency/energy, and protocol baseline |
| 8 | `dac-2026-research999` | Galaxydit: Efficient Video Generation with Guidance Alignment and Adaptive Proxy in Diffusion Transformers | Video/model suite, guidance and proxy policy, quality metrics, sampling steps, hardware, latency/energy, and standard diffusion baseline |

These routes close the titled DAC inventory. They remain routing artifacts, not
technical rankings or evidence that a paper is quantitatively comparable.
