# DAC 2026 evidence batch 3: deeper mechanisms

This page explains five additional DAC 2026 records whose official presentation
descriptions contain enough mechanism-level detail for provisional adjudication.
They are medium-confidence description-level records, not full-paper reviews.

## Analog continuous-time scientific AI

**A Fully Analog Continuous-Time CIM Neural ODE Solver for Flow-Matching-Based
Fluid Dynamics Generation** treats the numerical evolution of turbulent-flow
fields as a hardware/software co-design problem. The description combines an
MLP-Mixer flow-matching model with a continuous-time neural ODE solver mapped to
RRAM compute-in-memory. Noise-aware training and decoder retraining are part of
the design, rather than a post-hoc robustness check.

The reported comparison is unusually concrete for a program description: three
turbulent-flow datasets, comparable velocity-field accuracy to convolutional and
attention-based models, and claimed reductions of 98.24% in energy and 99.99%
in latency against an NVIDIA A100. The evidence does not expose array size,
conversion overhead, precision, device variability, or dataset-level errors, so
the result supports a mechanism hypothesis—not a general claim that analog CIM
dominates GPUs.

## Microarchitectural observability as a security surface

**Seeing the Unseen** reverse-engineers hidden performance-monitoring-unit event
semantics through differential analysis and simulation validation. It then uses
the discovered branch-related behavior and UMask combination to demonstrate a
PMU covert channel for Spectre-v1 in SGX and website fingerprinting.

The important technical connection is between verification and security: a
microarchitectural event that is undocumented is treated as an object to infer,
validate, and then exploit. The public description does not provide processor
generations, trace budgets, attack time, numerical fingerprinting precision, or
mitigation evaluation. Those omissions prevent generalizing the demonstration
to all Intel processors or to practical remote attacks.

## Locality-preserving quantum compilation

**Fast Template Matching for Quantum Circuits Using Hypergraph** replaces a DAG
representation with a commutativity-aware hypergraph. Commuting gates can be
collapsed into a super-node while local connectivity is retained, allowing
incremental matching to revisit only a neighborhood.

On random and arithmetic benchmarks, the description reports 11–606x speedup
over the Qiskit DAG implementation with the same optimization quality. The
sub-subtheme is therefore not simply “quantum optimization”: it is locality-
preserving representation design for scalable template matching. Circuit-size
distributions, gate sets, memory use, and hardware-coupling constraints remain
unreported.

## Open infrastructure for scale-up systems

**OpenSUN** addresses a research-infrastructure bottleneck. Its FPGA-based
multi-node platform exposes I/O controllers, switches, protocol stacks, and
software layers for experimentation with scale-up interconnects such as CXL,
UALink, and NVLink-like systems.

This is an artifact contribution rather than a reported optimization result.
Its significance is that it makes cross-layer experimentation possible: a
researcher can change topology, controller logic, protocol behavior, or system
software without treating a commercial scale-up machine as a black box. The
description does not establish throughput, latency, node scale, protocol
compliance, or resource cost.

## KV-cache management for embodied planning

**KEEP** treats embodied-planning memory as a dynamic KV-cache problem. Static-
Dynamic Memory Construction groups memory by update frequency; Multi-hop Memory
Re-computation restores important cross-group interactions; Layer-balanced
Memory Loading addresses imbalance between KV loading and recomputation across
layers.

The contribution is more specific than generic cache compression: it coordinates
granularity, importance propagation, and layer scheduling in the presence of
dynamic memory updates. The public description supplies no task suite, model,
latency, memory-footprint, planning-quality, or hardware results, so this record
is classified by mechanism and retained as pending deeper quantitative review.

## Cross-record interpretation

These five records reinforce three evidence-backed mechanisms in the current
DAC sample: data movement is being redesigned around workload structure; a
representation or intermediate abstraction can be the main optimization lever;
and infrastructure/verification constraints are becoming part of the research
artifact itself. They do not establish prevalence or a temporal trend. The
machine-readable records are in `dac/data/adjudicated-2026-batch-3.jsonl`.
