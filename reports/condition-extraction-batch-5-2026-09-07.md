# Condition extraction batch 5 — 2026-09-07

This batch covers five P1 recovery cases where accessible evidence is limited to
official descriptions and institutional/author context. The result is an
explicit missing-condition register, not a paper-level performance extraction.

| Paper | Accessible evidence | Conditions still required before quantitative use |
|---|---|---|
| DAC-108 CANNON | Official description plus author-lab/institutional context for a CXL near-memory ANN architecture on real hardware | Hardware SKU and CXL topology, memory-resident baselines, index/data scale, query workload, recall target, end-to-end RAG boundary, and measured-vs-modeled status |
| DAC-1028 CtxMem | Official description of OS–hardware tiered memory using DRAM/SSD hybrid CXL devices | Simulator or hardware platform, page-fault/offload policy, workload traces, tier capacities, migration cost, baseline memory manager, and tail-latency accounting |
| DAC-1065 FLASH3D | Official description plus institutional announcement for a layered analytical 3D-IC thermal solver | Geometry/material stack, boundary conditions, solver tolerance, reference simulator, mesh/runtime budget, temperature error metric, and measured-silicon correlation |
| DAC-1101 HYPER-CIM | Official description plus matching institutional abstract for predictive digital-CIM exploration | Training/design-space split, model error, number and identity of realized macros, process/library, PPA measurement boundary, and whether the 297M configurations are predicted or fabricated |
| DAC-1182 Fusedot | Official description and author identity/source discovery for multiplication-fused LLM dot products | Quantization grouping/equivalence rules, finite-precision behavior, model suite, accuracy parity, hardware/compiler implementation, baseline, and end-to-end latency/energy boundary |

## Recovery decision

These five records remain technically prioritized but quantitatively withheld.
Their current evidence is sufficient for mechanism-level routing only. Repeated
searches of the same official pages would not resolve the missing conditions;
the next useful event is an author manuscript, artifact, or proceedings copy.
