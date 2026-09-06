# DAC 2026 evidence batch 2: deeper technical directions

These ten analyses use substantive official DAC presentation descriptions. They
are stronger than title-only signals but remain below full-paper evidence where
the public description omits experiment tables or implementation details.

## Physical design and thermal modeling

**DCTS** turns discrete clock-tree topology and buffer sizing into a continuous
probabilistic-graphical-model optimization. On ISCAS'89 and OpenCores under
ASAP7, the description reports 2.78x speedup on large circuits and minimum
improvements in delay, skew, power, and area over academic solutions. The
important mechanism is joint topology/buffer optimization rather than a
sequential CTS pipeline; commercial-tool configurations remain unknown.

**LegoTherm** decomposes chiplet thermal systems into reusable reduced-order
modules with thermally coupled interface ports. It reports up to 10.39x speedup
over COMSOL, below 0.40% mean relative error, and reducing design iteration
from weeks to half a day on industrial-scale 2.5D/3D benchmarks. This suggests
thermal analysis is becoming a reusable design-flow primitive, but mesh and
calibration details are not exposed.

**Early Design Stage Thermal Prediction** combines ML power-density prediction,
physics-guided temperature interpolation, and placement optimization. The
description reports 49.0% and 34.9% prediction-accuracy improvements and a
9.97°C maximum-temperature reduction with timing and area maintained. The
critical open question is whether the learned predictor transfers across
designs, nodes, and placement distributions.

## LLMs inside the design loop

**ParetoPilot** uses an LLM for global-optimization reasoning over HLS
directives, combining directive scheduling with Pareto-front quality awareness.
It reports 49.5% DSE improvement and 1.8x efficiency over a heuristic baseline.
This is distinct from code generation: the LLM is used as a search controller,
so search budget, reproducibility, and Pareto-quality definition are central
adversarial checks.

**STELLAR** retrieves structurally similar RTL/SVA pairs using AST fingerprints
and uses them to guide LLM SystemVerilog Assertion generation. The reported
evaluation improves syntax correctness, stylistic alignment, and functional
correctness. Numerical values, property coverage, and proof-validity details
are not in the public description, so this remains medium-confidence evidence.

**MappingEvolve** uses a Planner/Evolver/Evaluator hierarchy to evolve the core
technology-mapping implementation rather than merely generating optimization
scripts. It reports 10.04% area reduction versus ABC, 7.93% versus mockturtle,
and 46.6%–96.0% S_overall improvement on EPFL benchmarks. The main risk is
regression and code-validity control across evolved implementations.

## LLM memory and execution architecture

**MBA** places gigabyte-scale 1T1C IGZO eDRAM buffers near the accelerator and
co-designs KV-cache mapping, double buffering, and iteration-aware eviction.
It reports up to 5.99x/3.63x end-to-end speedup and 8.86x/4.93x energy
efficiency over GPU and accelerator baselines. The field direction is moving
KV-cache placement into memory-technology/architecture co-design; density,
retention, area, and fabrication assumptions need verification.

**AHASD** decouples draft-model execution on mobile PIM from target-model
verification on an NPU. Entropy-history-aware control and time-aware
pre-verification address fluctuating draft lengths; the description reports
up to 4.2x throughput and 5.6x energy-efficiency gains over GPU-only with less
than 3% DRAM-area overhead. Acceptance-rate distributions and model details are
not public in the description.

**REFLEX** aligns sparse-attention KV entries to one DRAM row and schedules PIM
execution without cache rewrites or hardware changes. It reports up to 1.64x
PIM throughput and 1.36x energy efficiency, plus 1.37x throughput in GPU-PIM.
The key design issue is preserving sparse-attention irregularity while making
DRAM activation locality explicit.

## Security and reliability

The remote ML-KEM side-channel study reports up to 99.5% secret-key recovery
from PQClean on Intel x86, treating remote power traces as a plaintext-checking
oracle. It challenges the assumption that speculative execution and dynamic
power management remove exploitable leakage. Network distance, trace budget,
attack time, and mitigations must be extracted before judging deployment risk.

## Cross-paper interpretation

This batch links three layers that are often analyzed separately: design-flow
search (DCTS, ParetoPilot, STELLAR, MappingEvolve), physical constraints
(LegoTherm and early thermal prediction), and execution architecture (MBA,
AHASD, REFLEX). The recurring direction is explicit optimization under hidden
state—topology, structure, thermal behavior, memory traffic, and security
leakage—rather than optimizing a single static PPA number.

These are evidence-backed directions within ten official descriptions, not
conference-wide rankings or claims about industrial adoption.
