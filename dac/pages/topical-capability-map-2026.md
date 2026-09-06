# DAC 2026 topical capability map

DAC has the largest current evidence base in this project: 543 official research
descriptions are captured and 49 records have been adjudicated. The 49 are a
selected, evidence-recoverable sample, not a conference-wide frequency estimate.
Most DAC evidence is official presentation-description text rather than full-paper
extraction, so headline metrics remain bounded by the public description and its
explicit limits.

## Capability map

| Topical area | Detailed subskills | Representative evidence |
|---|---|---|
| AI-assisted design automation | LLM-generated HLS, global-reasoning DSE, technology-map evolution, RL Verilog generation, preference-constrained placement | DAC AI/EDA batch; ICCAD cross-comparison is separate |
| Constraint-aware search | differentiable partitioning, Bayesian analog sizing, multi-fidelity surrogates, hierarchical CIM exploration | DSE and methodology batches |
| Memory/data movement | CXL near-memory ANN, tiered CXL memory, near-memory communication bounds, sparse-attention PIM, KV-cache management | CANNON, CtxMem, RAF, REFLEX, MBA, KEEP |
| Accelerator specialization | low-bit GEMM, LUT quantization, graph/GNN acceleration, Gaussian splatting, mixed-precision datapaths | DAC accelerator batches |
| Physical integration | 3D-IC thermal solving, chiplet thermal reduction, package power-plane synthesis, metal-density constraints | FLASH3D, LegoTherm, package/integration records |
| Reliability and security | NPU fault mitigation, BFP protection, EM/IR coupling, side channels, adversarial MoE offloading | Strix, BFP reliability, GEMIR, Energon-adjacent/security records, Icarus |
| Verification and correctness | HLS assertion generation, formal analysis, FPGA DRC, SVA retrieval and synthesis | verification and security batch |

## 1. AI-assisted EDA is becoming tool-grounded

The relevant capability is not “an LLM writes RTL.” The adjudicated records
separate several loops:

- LLM-generated HLS architecture optimization must produce synthesizable designs
  and hardware results.
- Global-reasoning HLS DSE uses a model as a search controller over directives,
  with a budget and Pareto objective.
- Technology-map evolution requires executable mapping code and regression checks.
- RL Verilog generation requires a reward path through compilation or simulation,
  not only text similarity.
- Preference-optimized placement adds user constraints to a learned placement
  representation.

The shared subskill is tool-grounded iteration; the evaluation obligations differ
between synthesis success, functional correctness, PPA, search efficiency, and
user-objective satisfaction. These records therefore should not be summarized as
one generic “AI improves EDA” result.

## 2. Search is becoming multi-level and constraint-aware

DAC’s design-space records combine learned or generative search with engineering
constraints. Examples include differentiable task-graph partitioning, robust
Bayesian analog sizing under process variation, multi-fidelity microarchitecture
exploration, and HYPER-CIM’s hierarchical surrogate trained on silicon-consistent
points and followed by macro verification.

The detailed skills are:

1. defining the design variables and legal region;
2. choosing a surrogate or policy that preserves useful structure;
3. incorporating timing, PPA, thermal, process, or physical constraints;
4. allocating evaluation budget across cheap and expensive fidelity levels; and
5. verifying that a promising point is realizable rather than only predicted.

A reported speedup or figure of merit is not enough to establish search quality;
baseline search budgets, constraint violations, model error, and silicon or
post-layout validation must remain explicit.

## 3. Movement is an architectural objective

CANNON places approximate-nearest-neighbor search on real CXL near-memory
hardware. CtxMem co-designs OS page migration with DRAM/SSD hybrid CXL memory.
RAF targets communication lower bounds in distributed near-memory processing, and
REFLEX aligns sparse-attention KV entries to DRAM rows for PIM. MBA and KEEP add
memory-placement and KV-recomputation mechanisms for LLM-style workloads.

The shared subskill is movement-aware execution: data placement, migration,
locality, access granularity, and communication are treated as part of the
algorithm/architecture contract. The records still represent different
workloads, memory technologies, and metrics; no single CXL or PIM mechanism can
be declared dominant from this sample.

## 4. Accelerator specialization is mechanism-specific

The accelerator records show why “AI accelerator” is too broad a label. FuseDot
shares multipliers around identical low-bit weights; OASIS uses outlier-aware
dual-side quantization and LUT-based GEMM; graph and Gaussian-splatting records
reshape dataflow around topology or rendering structure; and other records
co-design precision, sparsity, memory, and processing elements.

The subskills that must be retained are representation choice, dataflow, memory
traffic, precision/error behavior, hardware sharing, and workload structure. A
speedup without accuracy, sequence-length, area, or energy conditions is a
mechanism signal, not a general accelerator ranking.

## 5. Physical integration is an early design variable

FLASH3D and LegoTherm make thermal modeling faster and more reusable for 3D-IC
and chiplet exploration. Package power-plane and metal-density records add
integrity and manufacturability constraints. The important shift is methodological:
thermal and physical effects are being brought into repeated architecture/design
loops rather than reserved for a final signoff check.

The detailed skills are reduced-order model construction, interface-port coupling,
steady-state versus transient assumptions, power-map fidelity, package geometry,
and validation against numerical or silicon references. A fast thermal surrogate
does not by itself establish accuracy outside its geometry/material distribution.

## 6. Reliability, security, and verification are distinct but connected

Strix spans NPU microarchitecture, ISA, and programming for fault mitigation;
the BFP reliability work separates mantissa and exponent protection; GEMIR jointly
models EM and IR behavior; Icarus attacks MoE caching and prefetch assumptions;
and verification records use learning to generate assertions, debug HLS, or
accelerate DRC. These mechanisms share a demand for explicit failure, threat, or
correctness models, but they are not one category of evidence.

The required fields differ:

- reliability: fault model, detection/correction path, overhead, guarantee;
- security: attacker capability, leakage/attack surface, success metric, defense;
- verification: property or equivalence target, coverage, false positives, proof;
- physical integrity: coupled fields, process assumptions, prediction error.

## What DAC supports—and what it does not

The DAC evidence supports a detailed map of engineering capabilities: tool-grounded
AI, constrained search, movement-aware architecture, workload-specialized
accelerators, earlier physical integration, and explicit reliability/security
loops. It does not establish conference-wide prevalence, product adoption,
industry winners, or causal year-over-year change. Those require full-corpus
adjudication, comparable historical editions, and independent adversarial review.
