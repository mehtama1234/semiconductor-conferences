# DAC 2026 evidence batch 4: models, artifacts, and design-space search

These five official presentation descriptions broaden the evidence sample beyond
LLM accelerator microarchitecture. They cover device simulation, mixed-precision
inference, multi-fidelity exploration, reproducible datasets, and formal
verification assistance. They remain medium-confidence description-level
adjudications.

## Diffusion surrogates for TCAD

**FUSE-TCAD** replaces expensive coupled-PDE simulation in a device-design loop
with a conditional diffusion surrogate that generates joint physical fields
rather than only scalar device metrics. Geometry and bias are controllable, and
Sobolev-edge regularization preserves gradients at junctions. On SOI-FET data,
the description reports transfer learning with 20% target-domain data, more than
30x speedup over commercial TCAD, and relative error within 0.8%.

The important subskill is field-preserving surrogate modeling: the model remains
useful for physical analysis because it retains spatially coupled fields. The
public description does not specify resolution, PDE residuals, leakage controls,
or commercial measurement conditions.

## Multiplication fusion for quantized LLMs

**FuseDot** observes that identical low-bit weights create repeated
multiplications in mixed-precision inference. Its MFDP paradigm fuses those
operations, then uses index-driven matrix multiplication, hierarchical
reordering, and cross-PE multiplier sharing. It reports 1.51–1.98x speedup and
1.19–1.51x energy-efficiency improvement over state-of-the-art accelerators.

This is a concrete example of a workload-specific arithmetic contract: the
quantization pattern changes the datapath and the sharing structure. Model
suite, accuracy impact, memory traffic, area, and baseline configurations remain
unresolved.

## Multi-fidelity microarchitecture exploration

**XSearch** uses Bayesian optimization across coarse and fine simulators. Low-
fidelity evaluations expand the candidate set; high-fidelity evaluations
calibrate the search and protect against inaccurate rankings. The method is
applied to the open-source XiangShan processor.

The contribution is not simply “Bayesian optimization.” It is an explicit
accuracy–cost management strategy for architectural search, with cross-fidelity
calibration as the critical mechanism. The description gives no search budget,
objective, simulator error, convergence curve, or quantitative baseline result.

## Reproducible post-layout capacitance data

**CapBench** is both a dataset and a measurement protocol: 14 OpenROAD runs,
three technology nodes, 61,855 3D windows, RWCap labels validated against
Raphael, and multiple input representations. CNNs achieve 1.75% error, while
GNNs are up to 41.4x faster with 10.2% error, making the accuracy–speed tradeoff
visible instead of hiding it behind a single winner.

This record is especially valuable for the broader project because it supplies a
reproducibility artifact rather than only a new model. The remaining questions
are split leakage, per-node performance, absolute runtime, licensing, and
whether the transfer-learning splits represent real foundry variation.

## Multi-agent assertion generation

**ChatSVA** decomposes SystemVerilog Assertion generation into modular data,
augmentation, validation, and verification tasks through an AgentBridge
multi-agent platform. It reports 98.66% syntax pass, 96.12% function pass,
139.5 assertions per design, and 82.50% function coverage, with a public web
service.

The technical skill is constrained generation with executable validation, not
free-form code generation. Pass rates do not establish formal proof completeness:
the design suite, oracle construction, duplicate properties, model/prompt
configuration, cost, and comparison systems are still required.

## Cross-record interpretation

Together these records show a recurring pattern in the current DAC evidence:
learned methods become useful when attached to a concrete engineering loop,
representation, simulator hierarchy, dataset, or executable checker. This is a
mechanism-level synthesis, not a claim about venue-wide prevalence or temporal
direction. Machine-readable records are in
`dac/data/adjudicated-2026-batch-4.jsonl`.
