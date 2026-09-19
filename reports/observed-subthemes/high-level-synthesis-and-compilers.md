# High level synthesis and compilers

This subject has 2 records in the selected sample. This page explains where it fits, then presents all captured paper evidence without shortening the measurements or limitations.

[Definitions used in the paper records](../reading-guide-v1.md)

## Understand the parent subject first

- [Design methodology and tooling](../themes/design-methodology-and-tooling.md)

## A program does not uniquely specify a circuit

A program describes operations and the behavior required from them. Hardware construction must also decide how many execution units exist, which operations share a unit, where values are stored, and when work proceeds. Different choices can implement the same behavior with different area, timing, and energy costs.

High-level synthesis constructs hardware from a higher-level program description. A compiler transforms representations of the program and selects implementation choices. The result must preserve the required behavior and remain compatible with the target device and tool flow.

## Dependencies limit concurrent execution

An operation needs its inputs before it can start. If another operation produces an input, their dependency constrains the schedule. Independent work may run concurrently when hardware and data are available. Repeated work may be pipelined so different iterations occupy different execution stages.

Pipelining does not remove dependencies or storage limits. A stage can stall if its input is unavailable or its output buffer is full. The compiler needs enough information about communication and resource use to choose a schedule that can actually execute.

## Intermediate representations expose different choices

An intermediate representation is a structured form used between the original program and final implementation. One form may expose large computational regions, while another exposes individual operations and transfers. Transformations can be easier to express and check at the level where the relevant relationships are explicit.

Dataflowgen's captured description uses a two-level representation within MLIR, a compiler framework supporting multiple representations. It outlines computational regions and applies dataflow transformations and optimization. The record identifies a method, but does not provide target devices, benchmark identities, numerical gains, or compilation cost. [Recorded evidence](../observed-subthemes/high-level-synthesis-and-compilers.md#paper-dac-2026-research083)

The missing conditions matter because a transformation that helps one target may add buffering or unsupported operations on another. A compiler architecture alone does not establish a hardware-performance result.

<span id="explanation-dac-2026-research083"></span>

## Dataflowgen: a richer IR must still lower to correct, closable hardware

An intermediate representation (IR) is a structured description between source behavior and generated hardware. A high-level IR can preserve algorithmic regions and loops; a lower-level IR can expose operations, dependencies, buffers and transfers. The benefit of multiple levels is that each transformation can operate where its relevant information is visible. The cost is that every conversion must preserve meaning and make target constraints explicit.

Dataflowgen is described as an open-source MLIR framework with two IR levels for dataflow accelerator generation. It outlines an application kernel, applies dataflow transformations, and derives a hardware-oriented control dataflow graph (H-CDFG). This changes the compiler's representation and search space. It does not by itself establish which MLIR dialects are supported, how memory effects are modeled, how the H-CDFG is lowered, or which FPGA/ASIC backends can consume it.

### Parallel-looking graphs still have dependencies and storage costs

The compiler must preserve loop bounds, dependences, memory ordering, side effects, reductions, initialization and numerical precision. A graph may expose independent operations while their operands arrive through a shared buffer or memory port. A fused or parallelized region can increase live values, buffering, routing pressure or peak bandwidth. A transformation that removes an apparent dependency must prove that the removed ordering was not required by the source program.

Check generated behavior against a trusted software or reference implementation on corner cases, including empty or short inputs, aliasing where supported, boundary iterations, reductions, overflow/rounding, variable latency operations and reset/state behavior. Compare intermediate and final values, not only whether synthesis completes. Report rejected or repaired transformations and unsupported operations.

### Compiler IR quality is separate from hardware quality

An H-CDFG can be a concise planning representation, but the implementation still needs scheduling, resource binding, memory allocation, buffering, interface generation and backend lowering. The target device determines whether the proposed parallelism fits available compute units, memory ports, interconnect, clock period and routing. Resource reduction can coexist with lower frequency or more buffering; higher kernel parallelism can be hidden by memory or initiation-interval limits.

For each named target, report initiation interval, latency, throughput, frequency, LUT/FF/DSP/BRAM or ASIC area, memory traffic, buffer occupancy, routing/timing closure, power and energy. Include synthesis and place-and-route failures, timing violations, unsupported operations, compiler time, peak memory and manual intervention. Separate time to compile from time for the generated accelerator to execute.

### “State-of-the-art HLS” needs a reproducible boundary

The source reports performance improvement, significant resource reduction and effective capture of kernel parallelism relative to state-of-the-art HLS tools, but supplies no numerical values, benchmark identities, target devices or compilation-time cost. A fair comparison must hold source kernels, numerical precision, device, clock/resource limits, backend versions, timeout, optimization effort and correctness checks constant. It must say whether preprocessing, kernel outlining, code generation, synthesis, place-and-route and final timing checks are included.

Test held-out kernels and targets rather than only the cases used to shape the transformations. Report per-kernel results and failures, resource-versus-frequency tradeoffs, design-space search cost, and whether generated designs were measured on hardware or only estimated by tools. The evidence supports an open-source MLIR/dataflow accelerator-generation direction, not demonstrated reusable hardware-performance improvement across targets.

## CODO connects legality, communication, and scheduling

CODO's captured evidence describes detection and repair of dataflow violations, optimization of data movement, and automatic scheduling for FPGA accelerators. An FPGA is configurable hardware whose available resources and connections constrain the generated implementation. [Recorded evidence](../observed-subthemes/high-level-synthesis-and-compilers.md#paper-isca-2026-program-002)

The conceptual connection is that an attractive schedule is insufficient if the communication structure cannot execute correctly. Repair must restore the required behavior, and the resulting communication and buffering must fit the target. A compiler should account for all these conditions while selecting the implementation.

The repository's evidence includes author preprint and artifact documentation, but does not establish independent reproduction of every synthesis or board result. Reported kernel, model, and board measurements retain their own scopes. A result on one FPGA flow does not by itself establish applicability to all programmable devices or fabricated fixed-function circuits.

## Tool speed and generated-hardware speed are separate outcomes

A compiler can take longer to produce a faster circuit. It can also compile quickly but miss useful implementation choices. The right objective depends on how often the generated circuit is used and how much design time is available.

Measure compilation time, synthesis success, hardware resource use, correctness, and application execution separately. Include failed configurations and manual intervention. State which operations or language features are unsupported rather than excluding difficult inputs without explanation.

## What would establish a reusable improvement

Use the same programs, numerical requirements, device limits, and comparison tools. Preserve tool versions and settings. Check behavior on the generated hardware or a suitable validated model, and report final resource and timing constraints.

Then test new applications and target configurations. Explain which transformations remain useful and which depend on a specific execution or memory organization. The strongest result is a defined transformation process that repeatedly produces valid, useful implementations under explicit conditions.

## Compare the results carefully

First identify the inputs and required output quality. Then identify the limited resource: time, memory, communication, energy, circuit area, or correctness coverage. Ask which part of the method reduces that cost and which new cost it adds. Compare numbers only when the experiments hold these conditions sufficiently similar.

A conference description may explain the proposal while omitting the full experiment. An author preprint link may have been coded from its abstract. The source classification does not by itself establish that every table was read. Missing locations remain visible below.

## Complete captured evidence

These are evidence records, not substitutes for the explanations above. Each record preserves its problem, proposed method, measurements, comparison conditions, and source limits. A populated record does not establish that its mechanism has been fully explained or independently verified.

<span id="paper-dac-2026-research083"></span>

### Dataflowgen: An MLIR-Based Compiler for Efficient Dataflow Accelerator Generation

DAC 2026 · Record: `dac-2026-research083`

[Read the step-by-step explanation](#explanation-dac-2026-research083)

**Updated source-backed reading card**

Reviewed 2026-09-09. Deepens the Dataflowgen treatment into a paper-level reading; separates two-level MLIR representation, kernel outlining, H-CDFG/dataflow transformations and automated optimization from semantic preservation, target-device feasibility, resource/timing results and compiler cost, while preserving the source's qualitative performance/resource claims.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

High-level synthesis must turn algorithmic behavior and microarchitectural choices into efficient dataflow hardware despite dependencies, representation mismatches and target-specific resource constraints.

**Mechanism / artifact:**

Open-source Dataflowgen MLIR compiler with two-level intermediate representations, kernel outlining, dataflow transformations, a hardware-oriented control dataflow graph (H-CDFG) and automated optimization; dialect definitions, legality checks, lowering, scheduling and code-generation targets are unspecified.

**Workload — the work tested:**

High-level-synthesis kernels and generated dataflow accelerators; kernel identities, operation coverage, tensor/dataflow shapes, numerical precision, benchmark split, target devices and generated-design acceptance criteria are unspecified.

**Hardware and manufacturing assumptions:**

Dataflow accelerator generation through an MLIR/HLS flow; FPGA or ASIC target, device resources, clock target, memory/interconnect, synthesis/backend tools, place-and-route, timing model and hardware validation status are unspecified.

**Baseline — the comparison method:**

State-of-the-art HLS tools

Same source kernels, language/IR semantics, precision, target device, clock/resource constraints, backend versions, optimization effort, synthesis timeout and correctness checks are unspecified

**Reported measurements:**

The source reports performance improvement, significant resource reduction and effective capture of kernel parallelism versus state-of-the-art HLS tools, but provides no numerical performance/resource values, frequency, area, bandwidth, latency, energy, compile time, synthesis success rate or hardware measurement.

**Limits on the conclusion:**

An intermediate representation and H-CDFG expose choices but do not guarantee semantic preservation. Check dependence, memory ordering, loop bounds, side effects, reductions, precision and initialization against a trusted software/reference implementation and inspect generated RTL or equivalent behavior under corner cases.

Hardware benefit is target-dependent. Report initiation interval, latency, throughput, frequency, LUT/FF/DSP/BRAM or ASIC area, memory traffic, buffering, routing/timing closure, power and failed/unsupported operations on named devices with the same backend and constraints. A dataflow graph that looks parallel may be limited by buffers, ports, dependencies or physical routing.

The official description supports an open-source MLIR/dataflow accelerator-generation direction with qualitative performance and resource claims, not demonstrated reusable hardware-performance improvement. Numerical gains, benchmark identities, target devices, compiler/synthesis cost, semantic checks and measured implementation results remain unresolved.

**Source and location**

Evidence tier: Primary captured official DAC description plus existing authored dataflowgen/HLS explanation; no full paper extraction, reproduced compiler run, synthesis trace or measured accelerator result. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH083)

DAC 2026 official description, first and final paragraphs; existing high-level-synthesis-and-compilers explanation; captured Problem, Mechanism / artifact, Workload, Hardware, Baseline, Measurements and Limits fields; no full manuscript, generated RTL, synthesis report or hardware validation.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** state-of-the-art HLS tools

**Evidence locators:** Not established in the captured evidence.

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH083&sess=sess155

**Hardware or process assumptions:** Not established in the captured evidence.

**Limits:** The description does not state numerical gains, benchmark identities, target devices, or compilation-time cost.

**Method or artifact:** Open-source MLIR compiler with two-level intermediate representation, kernel outlining, dataflow transformation, and automated optimization.

**Metrics:** performance improvement

resource reduction

captured kernel parallelism

**Problem:** Existing HLS tools have difficulty mapping data-dependent applications into custom hardware because algorithm and microarchitecture concerns appear at mismatched IR levels.

**Workload or benchmark:** High-level-synthesis kernels and dataflow accelerator generation.

</details>

<span id="paper-isca-2026-program-002"></span>

### CODO: An Automated Compiler for Comprehensive Dataflow Optimization

ISCA 2026 · Record: `isca-2026-program-002`

**Problem:**

Manual construction of efficient streaming FPGA dataflow accelerators remains difficult even with high-level synthesis because dataflow legality, communication efficiency, and resource/performance tradeoffs interact.

**Mechanism / artifact:**

CODO compiler built around systematic coarse- and fine-grained dataflow-violation detection and repair, on-chip/off-chip data-movement optimization, automatic scheduling, and a public artifact implementation.

**Workload — the work tested:**

Typical computation kernels, DNN models, CNN models, and GPT-2 evaluated through synthesis and on-board FPGA experiments.

**Hardware and manufacturing assumptions:**

FPGA dataflow accelerators and high-level-synthesis tool flows; the public evidence does not establish applicability to ASIC implementation or all FPGA families.

**Baseline — the comparison method:**

state-of-the-art dataflow/HLS frameworks

**Reported measurements:**

1.45x–4.52x latency speedup on computation kernels

3.7x–33.8x speedup on DNN models

7.3x average CNN speedup in on-board evaluation

2.07x GPT-2 speedup in on-board evaluation

performance-resource tradeoff

**Limits on the conclusion:**

The evidence is an author arXiv preprint plus public artifact documentation; the repository has not independently reproduced synthesis or board results, extracted every baseline/configuration, or established generalization beyond the reported FPGA flows.

**Source and location**

Evidence tier: High primary preprint. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://arxiv.org/abs/2604.12618)

An exact page, section, or table location has not been recorded. Page-level verification remains open.

## What remains to establish

Resolve unspecified workloads, comparison methods, resource budgets, and source locations before generalizing a reported gain. Multiple papers in this selected sample permit comparison of mechanisms, but do not by themselves establish recurrence across years or a long-term trend.

[All subthemes](../expanded-taxonomy-v1.md) · [Research directions](../directions/README.md)
