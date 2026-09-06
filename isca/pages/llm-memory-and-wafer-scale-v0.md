# ISCA 2026: LLM systems, memory locality, and wafer-scale execution

This page is a provisional technical reading of five ISCA 2026 papers for which
the repository has substantive indexed excerpts. The excerpts are secondary
index evidence, not official full-text captures. Every record remains marked
`pending_primary_verification` in `isca/data/indexed-evidence.jsonl`.

## Evidence-backed technical picture

### Structured execution rather than dense scaling

MLX is described as an algorithm–architecture co-design for structured sparse
LLM inference. Its indexed excerpt names semantic-aware FFT compression,
hierarchical sparse projections, spatial dataflow execution, and Closed
Dependency Components for folding deterministic forward-only regions across
layers. The technical implication is a move from “accelerate dense operators”
toward matching structured sparsity and execution topology, but the benchmark
and measured claims still require primary verification.

### Communication is part of MoE architecture

The DySHARP excerpt identifies redundant inter-GPU transfers in expert
parallelism and describes dynamic multimem addressing, ISA/architecture/runtime
co-design, and token-centric kernel fusion. This makes the communication fabric
and collective primitives part of the MoE performance model rather than an
implementation detail.

### Virtual memory layout becomes a serving optimization

ConServe focuses on multi-turn LLM KV-cache growth and the translation locality
cost introduced by paged layouts. Its proposed contiguity-aware allocator keeps a
contiguous virtual-address slice per conversation, maps physical pages on demand,
and resizes lazily. The important subskill is not simply “memory management”; it
is preserving the locality properties that the serving software and hardware
translation path depend on.

### Wafer-scale mapping must include failures

BusyBarn combines hierarchical mapping for Transformer blocks and die arrays with
load/distance-aware communication allocation and fault tolerance. This joins
placement, topology-aware communication, and failure handling in one inference
mapping problem. It is a useful example of reliability becoming a first-class
constraint in a large accelerator system.

### Compiler automation connects architecture to implementation

CODO is described as an automated FPGA dataflow compiler that removes coarse- and
fine-grained dataflow violations, optimizes on- and off-chip movement, and
automatically schedules designs. The indexed excerpt reports speedups for kernels,
DNNs, CNNs, and GPT-2 and names an open-source artifact, but all quantitative
claims remain pending primary verification.

## Theme → subtheme → sub-subtheme map

| Theme | Subtheme | Specific technique | Evidence status |
|---|---|---|---|
| Architecture and accelerators | LLM workload acceleration | structured sparse spatial dataflow | indexed excerpt |
| Architecture and accelerators | LLM workload acceleration | dynamic in-switch MoE communication | indexed excerpt |
| Memory, interconnect, and storage | Memory hierarchy and persistence | contiguous KV-cache virtual allocation | indexed excerpt |
| Architecture and accelerators | Distributed and wafer-scale inference | fault-tolerant wafer-scale mapping | indexed excerpt |
| Design methodology and tooling | HLS and compilers | automated FPGA dataflow optimization | indexed excerpt |

## Limits

This page does not establish ISCA-wide prevalence, performance superiority,
industrial adoption, or a temporal trend. The next evidence gate is to attach
IEEE or author-authorized primary papers, recover full benchmark conditions, and
adjudicate the five records against the shared paper contract.
