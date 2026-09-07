# Condition extraction batch 6 — 2026-09-07

This sixth P1 batch records six repository/abstract-backed records where the
source is useful for mechanism routing but does not expose enough paper-level
conditions for quantitative comparison.

| Paper | Accessible evidence | Conditions still required before quantitative use |
|---|---|---|
| DAC-1110 HLSArchOpt | Pinned GitHub tree, README, HLS script, top-level kernel, and stored synthesis reports | Exact paper benchmark mapping, FPGA/device and tool versions, prompt/search budget, correctness checks, baseline, and whether stored reports are representative |
| DAC-865 ParetoPilot | Pinned GitHub README, entry point, HLS utility, sampling code, configuration, and AES Tcl | Proceedings identity/author reconciliation, benchmark suite, search budget, model/version, PPA objective, synthesis settings, and result provenance |
| DAC-1054 Icarus’s Wings | Pinned repository README and complete tree for a hidden-prefix attack against MoE offloading | Paper manuscript, attack/evaluation protocol, model and prefix construction, defenses, success metric, workload, and reproducible execution |
| ICCAD-1094 Qudit framework | Author publication abstract, CV identity, and HKUST citation metadata | Full simulation equations, device parameters, gate-fidelity metric, baselines, optimization budget, and any fabricated-device evidence |
| ICCAD-1111 NIMCH remapping | NTU institutional abstract with title, authors, DOI, and mechanism | Named baseline, circuit suite, thread/machine configuration, placement-quality tolerance, and full-flow runtime boundary |
| ICCAD-1155 COPA | NYCU institutional abstract and author-lab identity listing | Testcases, pin/capacity model, congestion baseline, timing-closure criteria, routing success, and wirelength measurement conditions |

## Recovery decision

These records remain in the P1 queue because each has a useful source route, but
none supports a matched quantitative comparison yet. Repository inspection and
abstract capture are preserved as provenance; no paper-level result is promoted.
