# Condition extraction batch 7 — 2026-09-07

This batch promotes the final eight DAC anchor routes into a condition-aware
evidence ledger. The evidence tiers remain separate: four have author/artifact
material, while four remain official-description-only or have no quantitative
source result. No headline is treated as independently verified.

| Paper | Evidence and conditions captured | Boundary retained |
|---|---|---|
| DAC-108 CANNON | Official description/recovery assessment; reported real-CXL implementation, pipelined ANN dataflow, asynchronous hashing, CPU/GPU labels, and up-to-two-orders claim | CXL version/topology, device, dataset, recall, batching, latency distribution, and matched baselines unresolved; headline withheld |
| DAC-1186 XSearch | Official description and bounded source search; Bayesian optimization over microarchitecture configurations with multi-fidelity simulation and cross-evaluation | Acquisition/fidelity policy, simulator validity, budget, workload, baselines, and high-fidelity results unavailable; no quantitative result admitted |
| DAC-535 MappingEvolve | Author preprint plus pinned artifact; EPFL/ASAP7 after `ABC compress2`, six stored average ratios cross-checked, 30×3 search iterations, ABC/mockturtle baselines, area-delay objective | Logs and PDF transcription were not rerun; model/seed/timeout/held-out protocol and equivalence remain unresolved; composite QoR is not speedup |
| DAC-865 ParetoPilot | Pinned public artifact; AES HLS Tcl targets `xczu7ev-ffvc1156-2-e` at 10 ns and reads csynth XML latency/resource estimates | No execution or paper identity reconciliation; benchmark split, model revision, seeds, comparator, and physical-board relevance unresolved |
| DAC-983 ATTINA | Official program route for spatial additive-NTT acceleration for edge zkSNARKs | Parameter sets, proof correctness, precision, hardware, metrics, and software baseline unavailable; mechanism only |
| DAC-986 Procyon | Official program route for fine-grained multi-tenancy in sparse streaming accelerators | Tenant mix, sparsity, isolation/QoS policy, hardware, throughput/energy/area, and single-tenant baseline unavailable |
| DAC-989 TAMI-MPC | Official program route for trusted minimal-interaction MPC acceleration of nonlinear inference | Protocol/security assumptions, nonlinear workload, trust boundary, communication, latency/energy, and baseline unavailable |
| DAC-999 GalaxyDiT | Official program route for guidance alignment and adaptive proxy in diffusion-transformer video generation | Video/model suite, quality metric, sampling budget, proxy error, hardware, latency/energy, and standard diffusion baseline unavailable |

This batch resolves evidence depth and missingness for the routed anchors; it does
not convert official descriptions into full-paper evidence or independent review.
