# Cross-conference direction report — evidence-tiered v0

This is the first synthesis across the project’s three conference workspaces. It
is deliberately provisional because the evidence is asymmetric:

- DAC has 543 official descriptions and 49 evidence-cited adjudications.
- ISCA has 173 official 2026 program records, DOI reconciliation for 171, fifteen
  primary, institutional-abstract, or company-source-backed adjudications, and five secondary-only papers still
  pending primary verification.
- ICCAD has official 2026 CFP scope, a 276-paper 2025 fallback inventory, and
  eight primary/preprint/author-PDF-backed fallback adjudications.

The machine-readable matrix is `data/cross-conference-matrix-v0.json`.

## What can responsibly be said now

### 1. The field is joining algorithm, architecture, and design-flow decisions

The clearest shared direction is not simply “more AI.” The collected records show
research moving across boundaries: LLMs and RL are being used inside design tools;
accelerator architecture is being shaped around workload structure; and compiler,
memory, packaging, timing, and reliability decisions are being optimized together.
DAC provides the largest official-description sample, while ISCA and ICCAD now
contribute selected primary-preprint cases. The evidence supports a
cross-conference case pattern, not a prevalence estimate.

### 2. Data movement is becoming a first-class design object

The evidence repeatedly treats movement—not only arithmetic—as the bottleneck:
KV-cache address locality, MoE inter-GPU traffic, wafer-scale mapping, CXL
near-memory ANN search, CIM hierarchy, and package power integrity all make data
placement and communication part of the algorithm/architecture contract. The
newest ISCA and DAC cases make the mechanism more specific: expert-selection
traffic, collectives, KV-cache placement, DRAM row activation, and memory
technology are being co-designed with execution.

### 3. Optimization is becoming multi-level and constraint-aware

The adjudicated DAC records include exact cost objectives, differentiable graph
partitioning, Bayesian optimization, reinforcement learning, hierarchical
surrogates, and LLM-generated HLS. These methods are paired with real constraints:
timing, PPA, metal density, thermal behavior, fault models, or silicon
realizability. This suggests a more specific research direction than generic
“AI for EDA”: learned or generative methods are being embedded inside constrained
engineering loops, where topology, proof structure, search budget, thermal
state, and PPA are part of the objective.

### 4. Reliability, security, and thermal behavior are being pulled earlier into design

NPU fault handling, EM/IR prediction, adversarial MoE offloading, formal circuit
analysis, Lit Silicon’s thermal-straggler model, remote ML-KEM leakage, and
ICCAD’s security/reliability scope show that the system is being optimized
together with its failure, thermal, and attack surfaces. These remain distinct
analytic subtrees, but they increasingly share cross-layer assumptions.

### 5. Packaging and memory are converging around thermal and bandwidth constraints

Tasa, LegoTherm, MBA, REFLEX, AHASD, and the ISCA memory cases connect physical
integration, thermal behavior, memory placement, and workload scheduling. This
does not establish that one packaging approach will win; it shows that thermal
and bandwidth constraints are being evaluated together rather than as isolated
post-layout checks.

### 6. Memory protection is becoming a cross-layer design capability

The detailed ISCA memory cluster makes this direction more precise. COSM treats
CPU/PIM concurrency as a bank- and bus-contention scheduling problem; Cerberus
coordinates ECC layers across the memory stack; PuDGhost measures interference
from unintended rows and columns on real DRAM chips; and the ECC-enabled PIM
record co-designs correction with bank utilization. HBM-CASO is retained as a
secondary-only queue item until a primary source is recovered.

DAC provides complementary accelerator-side cases: Strix spans NPU
microarchitecture, ISA, and programming for fault mitigation; the BFP reliability
record separates mantissa and exponent protection; and EM/IR and thermal records
bring physical constraints into the same design loop. ICCAD’s 2025 fallback Tasa
case connects memory bandwidth, 3D integration, thermal behavior, and LLM
inference, while its 2026 scope explicitly includes reliability and advanced
integration.

The responsible conclusion is a capability statement: memory and accelerator
systems increasingly require coordinated reasoning across physical effects,
protection mechanisms, runtime scheduling, and workload behavior. The evidence
does not establish which ECC, PIM, or packaging strategy will dominate, nor does
it establish venue-wide prevalence.

## What remains unproven

This report does not rank conferences, count research prevalence across unequal
corpora, establish industry adoption, or claim that any direction is rising or
declining. The next required work is to expand primary/full-text extraction
beyond the selected ISCA and ICCAD cases, adjudicate the remaining DAC queue,
and perform adversarial LLM/human review of every evidence-backed
classification. Historical comparable editions are also required before
temporal claims are allowed.
