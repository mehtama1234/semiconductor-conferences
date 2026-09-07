# ICCAD 2025 fallback topical capability map

This page covers nine coded ICCAD fallback records (independent review pending) at the
mechanism level. ICCAD 2026 remains the target edition, but its paper corpus was
not publicly available in the collection window; therefore every observation on
this page is explicitly about the 2025 fallback sample and is not a 2026 trend
claim.

## Capability map

| Topical area | Detailed subskills | Evidence records |
|---|---|---|
| Agentic design-flow decomposition | role separation, hierarchy, retrieval, tool validation, adaptive debugging, PPA feedback | MAHL, VeriOpt |
| Verilog and HLS correctness | RL reward from compile/simulation, bug localization, bug taxonomy, correction validation | VERIRL, HLSDebugger |
| Physical integration | hierarchical chiplet partitioning, layout configuration, tool-backed exploration | MAHL |
| Thermal and bandwidth co-design | 3D stacking, thermal balancing, bandwidth sharing, LLM placement/scheduling | Tasa |
| Robust analog optimization | process-variation modeling, uncertainty-aware Bayesian search, Monte Carlo refinement | RSizing |
| Hardware telemetry security | power/thermal observation, architecture inference, substitute-model construction, transfer attacks | Energon |
| Device-algorithm co-design | stochastic computation, spin neurons, ferroelectric nonvolatile weights, PDE mapping | NeuroPDE |
| Cross-layer optimization | system/technology feedback, cell criticality, search-budget controls | Orthrus (primary-coding addition below) |

The useful unit is the chain of decisions, not the label “AI for EDA.” For
example, MAHL is about decomposing a hierarchical chiplet workflow and validating
the outputs with tools; VeriOpt is about closing a PPA loop around generated RTL;
HLSDebugger is about localizing and correcting functional HLS defects. These
should remain separate subskills even though all use language models or learned
components.

## 1. From generation to tool-grounded design loops

MAHL and VeriOpt provide two different forms of agentic design automation. MAHL
uses multiple roles across parsing, hierarchical description, RTL generation,
validation/debugging, design-space exploration, and physical configuration. Its
key capability is maintaining hierarchy and tool feedback across a chiplet design
flow. VeriOpt separates planning, programming, review, and evaluation, then feeds
synthesis reports and timing diagrams back into Verilog generation. Its key
capability is making PPA and timing closure part of the generation loop rather
than checking them only after code generation.

The shared mechanism is closed-loop tool grounding. The distinct subskills are
hierarchical physical decomposition versus multi-role PPA-aware RTL refinement.
Reported Pass@5, power, area, timing, and functional-success values are maxima or
selected results in preprints; they do not establish average-case reliability,
model/API cost, or reproducibility across design suites.

## 2. Correctness remains a separate axis

VERIRL uses reinforcement learning for Verilog generation, where compilation,
simulation, and functional feedback define the reward path. HLSDebugger instead
frames HLS debugging as a learned multi-task problem: locate the bug, classify its
type, and produce a correction, supported by a domain-specific bug dataset.

The subskills are different: generation under executable reward versus diagnosis
and repair under a bug taxonomy. A generated module that compiles is not
automatically functionally correct, and a bug-localization score is not a proof of
repair correctness. The evidence therefore requires separate fields for
compilation, simulation, correction validity, dataset construction, and coverage.

## 3. Physical constraints enter the same loop

MAHL and Tasa show two forms of physical-system coupling. MAHL applies agentic
hierarchy to 2.5D chiplet design and physical-layout configuration. Tasa combines
3D-stacked architecture, thermal behavior, bandwidth sharing, and LLM inference.
The shared capability is translating physical constraints into architecture or
workflow decisions; the mechanisms and evaluation conditions are not the same.

RSizing supplies a complementary analog-design case: robust Bayesian optimization
under process variation. Here the detailed skill is uncertainty-aware search,
including how process variation is modeled, how the surrogate is calibrated, and
how Monte Carlo refinement is used. It should not be collapsed into generic
“Bayesian optimization” without retaining the variation and signoff context.

## 4. AI is also an attack instrument

Energon forms a distinct security chain:

`GPU power/thermal telemetry → transformer architecture inference → substitute model → transfer attack`

This is not ordinary model optimization. The required subskills are telemetry
access, signal quality, architecture identifiability, attacker cost, substitute
construction, and transferability under clean/noisy conditions. The security
claim cannot be separated from its threat model or from whether telemetry access
is realistic in the target deployment.

## 5. Device physics can be the computation

NeuroPDE treats stochastic spin neurons and ferroelectric nonvolatile weights as
part of the PDE-solving algorithm rather than merely imperfect hardware. The
detailed subskill is matching a random-walk computation to device stochasticity,
then measuring variance, time, energy, precision, and process assumptions together.
This is a different question from whether an analog or neuromorphic device is
generally energy efficient.

## What this fallback supports

The 2025 sample supports a capability map in which EDA automation is becoming
more hierarchical, tool-grounded, physically constrained, and security-aware.
It also shows that “AI-assisted design” spans generation, verification, search,
thermal integration, and attack analysis rather than one technology.

It does not support ICCAD-wide prevalence, a 2025-to-2026 directional claim,
commercial adoption, or a ranking of methods. Those require the 2026 paper corpus,
full-paper extraction for all records, and independent adversarial review.
## Orthrus primary-coding addition

[Orthrus assessment](../data/orthrus-primary-recovery-v1.json) and
[review packet](../../data/review-packets/iccad-2025-437.json) extend the fallback
sample to nine coded papers. The primary branch is design methodology →
optimization and search → dual-loop system-technology co-optimization.
This is a researcher classification: learned search and physical design are
secondary relationships, not additional papers. The distinguishing question is
how design levels exchange optimization guidance. Its captured abstract is
separate from the coding summary; figure review and independent acceptance
remain pending, and numerical headlines are withheld.
