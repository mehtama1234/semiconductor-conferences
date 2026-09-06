# Cross-conference direction report — evidence-tiered v0

This is the first synthesis across the project’s three conference workspaces. It
is deliberately provisional because the evidence is asymmetric:

- DAC has 543 official descriptions and 20 evidence-cited adjudications.
- ISCA has 2026 program metadata plus five substantive secondary-index excerpts;
  those five remain pending primary-source verification.
- ICCAD has official 2026 CFP scope and a 276-paper 2025 fallback inventory, but
  the fallback records are still metadata-only.

The machine-readable matrix is `data/cross-conference-matrix-v0.json`.

## What can responsibly be said now

### 1. The field is joining algorithm, architecture, and design-flow decisions

The clearest shared direction is not simply “more AI.” The collected records show
research moving across boundaries: LLMs and RL are being used inside design tools;
accelerator architecture is being shaped around workload structure; and compiler,
memory, packaging, timing, and reliability decisions are being optimized together.
DAC provides the strongest paper-level evidence for this claim. ISCA’s indexed
excerpts and ICCAD’s CFP independently expose compatible scope, but do not yet
provide equivalent adjudicated counts.

### 2. Data movement is becoming a first-class design object

The evidence repeatedly treats movement—not only arithmetic—as the bottleneck:
KV-cache address locality, MoE inter-GPU traffic, wafer-scale mapping, CXL
near-memory ANN search, CIM hierarchy, and package power integrity all make data
placement and communication part of the algorithm/architecture contract.

### 3. Optimization is becoming multi-level and constraint-aware

The adjudicated DAC records include exact cost objectives, differentiable graph
partitioning, Bayesian optimization, reinforcement learning, hierarchical
surrogates, and LLM-generated HLS. These methods are paired with real constraints:
timing, PPA, metal density, thermal behavior, fault models, or silicon
realizability. This suggests a more specific research direction than generic
“AI for EDA”: learned or generative methods are being embedded inside constrained
engineering loops.

### 4. Reliability and security are being pulled earlier into design

NPU fault handling, EM/IR prediction, adversarial MoE offloading, formal circuit
analysis, and ICCAD’s security/reliability scope show that the system is being
optimized together with its failure and attack surfaces. The records are not yet
comparable enough to claim a field-wide trend, but they support reliability and
security as first-class analysis dimensions rather than after-the-fact checks.

## What remains unproven

This report does not rank conferences, count research prevalence across unequal
corpora, establish industry adoption, or claim that any direction is rising or
declining. The next required work is primary-source verification for ISCA,
abstract/full-text extraction and adjudication for ICCAD 2025, and expansion of
DAC adjudication beyond the first 20 records. Historical comparable editions are
also required before temporal claims are allowed.
