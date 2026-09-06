# DAC 2026: data movement, memory, packaging, and physical constraints

This chapter synthesizes the adjudicated DAC records that treat movement of data,
physical integration, or physical constraints as part of the design problem. The
records are in `dac/data/adjudicated-2026-batch.jsonl`; each claim below is tied to
an official DAC presentation description and retains its limitations.

## 1. Memory locality is an algorithm/architecture contract

**CANNON** moves approximate-nearest-neighbor search onto real CXL near-memory
hardware. Its design is driven by the mismatch between fine-grained vector access
and coarse SSD I/O, so it combines a deeply pipelined dataflow with asynchronous
hashing and speculative execution. The specific subskills are CXL programming,
near-memory data placement, pipeline stall avoidance, and recall/performance
measurement—not merely “using near memory.”

**HYPER-CIM** addresses a different locality problem: the design space spans CIM
macro, accelerator, and architecture levels. Its hierarchical surrogate is trained
on silicon-consistent points, then checked with fabricated 28 nm macros. The
important methodological move is preserving circuit-faithful constraints while
searching architecture-level configurations.

## 2. Packaging creates coupled electrical and mechanical objectives

**BLADE** synthesizes package power/ground planes under metal-density and
degassing constraints while optimizing IR drop. This is a constrained geometric
search problem: satisfying a manufacturing-related density condition can affect
electrical integrity, and the optimizer needs a fast evaluator to explore the
trade-off.

**FLASH3D** shows the same coupling from the thermal side. It targets steady-state
3D-IC temperature simulation with fine-grained power maps and complex boundaries.
Its analytical solver is valuable because thermal-aware design needs repeated
evaluation early in the flow, before expensive detailed design decisions are
locked in.

## 3. Physical design kernels remain targets for specialization

**Powerpath** reduces sequential-constraint characterization by reusing a required
reference-delay simulation rather than adding SPICE runs. It combines a
physics-grounded signal, affine calibration, and online ridge regression. The
lesson is that a learned or statistical method becomes more defensible when it is
anchored to a signal already required by the signoff flow.

**AccDRC** uses software/hardware co-design for design-rule checking: cell-aware
partitioning, locality-preserving loading, a reconfigurable check core, and sparse
violation writeback. The subskills are layout decomposition, FPGA dataflow design,
rule-check equivalence, and resource-aware acceleration.

## Theme map

| Theme | Subtheme | Specific sub-subtheme | Evidence records |
|---|---|---|---|
| Memory/interconnect/storage | Data movement and locality | CXL near-memory ANN search | CANNON |
| Architecture/accelerators | Architecture/software co-design | Silicon-calibrated CIM exploration | HYPER-CIM |
| Chiplets/3D/packaging | Package/system co-design | Metal-density-constrained P/G synthesis | BLADE |
| Chiplets/3D/packaging | 3D stacking and thermal management | Analytical 3D-IC thermal solving | FLASH3D |
| Physical design/manufacturing | Timing analysis and optimization | Supply-current constraint characterization | Powerpath |
| Physical design/manufacturing | Placement/routing/timing | FPGA-accelerated DRC | AccDRC |

## What this does not establish

These six cases support a technical pattern: memory placement, physical
integration, and design-rule constraints are increasingly co-optimized with
architecture and algorithms. They do not establish prevalence across DAC, market
adoption, or superiority outside the reported workloads and process/platform
conditions.
