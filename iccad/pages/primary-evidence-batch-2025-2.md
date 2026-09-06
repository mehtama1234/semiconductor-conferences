# ICCAD 2025 fallback: primary evidence batch 2

These three records extend the primary/preprint-backed ICCAD fallback sample.
Because the project’s target edition is 2026 and the paper corpus currently
available is 2025, every conclusion below is labeled as analysis of the 2025
fallback—not a claim about the unreleased 2026 paper corpus.

## MAHL: hierarchical multi-agent chiplet design

MAHL decomposes LLM-guided 2.5D chiplet design into six cooperating roles:
AI-to-hardware parsing, hierarchical description generation,
retrieval-augmented RTL generation, tool-based validation and debugging,
multi-granularity design-space exploration, and physical-layout configuration.
The central technical idea is hierarchy: flattening the chiplet design problem
creates validation and optimization costs that are difficult for a single prompt
or agent to manage.

The preprint reports a best-case Pass@5 improvement from 0 to 0.72 on
real-world chiplet design and PPA results comparable or superior to CLARIE for
selected objectives. The evidence does not establish average-case performance,
physical-flow reproducibility, or model/API cost.

## VeriOpt: PPA-aware multi-role Verilog generation

VeriOpt separates planning, programming, review, and evaluation, then feeds
synthesis reports and timing diagrams back into the generation loop. This
directly addresses a recurring limitation in LLM-for-EDA work: functional RTL
can still be unusable when power, performance, or area is poor.

The preprint reports maximum reductions of 88% power and 76% area, a 73%
timing-closure improvement, and 86% functional-evaluation success against
baseline LLM-generated RTL. These are reported maxima; process nodes, design
suite, constraints, prompts, and leakage controls require full-paper review.

## NeuroPDE: physical stochasticity for PDE solving

NeuroPDE uses probabilistic spin neurons to emulate random walks and ferroelectric
synapses for continuous non-volatile weights. The architecture therefore treats
device stochasticity as a computational resource rather than only a source of
error. On diffusion equations, the preprint reports variance below 1e-2 against
analytical solutions, 3.48x–315x execution-time speedup, and 2.7x–29.8x energy
advantage over advanced CMOS neuromorphic chips.

The key subskill is matching an algorithmic stochastic process to device physics.
The evidence does not yet establish device-area overhead, variability handling,
precision, process assumptions, or fair normalization of the CMOS baselines.

## Cross-record interpretation

This batch links three broader directions: hierarchical agents are being placed
inside design flows, verification/PPA feedback is becoming part of code
generation, and emerging-device randomness is being used as an algorithmic
primitive. These are evidence-backed mechanisms from three primary preprints,
not prevalence or 2025-to-2026 trend estimates. Machine-readable records are in
`iccad/data/adjudicated-2025-batch-2.jsonl`.
