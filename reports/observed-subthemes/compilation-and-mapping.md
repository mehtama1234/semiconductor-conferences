# Compilation and mapping

This subject has 1 record in the selected sample. This page explains where it fits, then presents all captured paper evidence without shortening the measurements or limitations.

[Definitions used in the paper records](../reading-guide-v1.md)

## Understand the parent subject first

- [Design methodology and tooling](../themes/design-methodology-and-tooling.md)

## An operation needs both a processing resource and its input values

A coarse-grained reconfigurable array, or CGRA, provides processing elements connected through a configurable network. Mapping assigns a computation to those elements and determines when operations run. An assignment is incomplete if the required values cannot reach their consumers through the available connections.

The selected paper, [RAM-CGRA](../observed-subthemes/compilation-and-mapping.md#paper-dac-2026-research1712), proposes reachability-aware mapping. Reachability concerns whether a required connection can be realized under the relevant topology and timing constraints. The captured official description does not expose its algorithm, target arrays, or quantitative results.

## Placement, scheduling, and routing constrain one another

Placement chooses where an operation executes. Scheduling chooses when it executes. Routing chooses how its output reaches subsequent operations. A locally attractive choice in one of these tasks can make the others difficult or impossible.

For example, assigning a consumer to an available processing element is not enough if its input cannot arrive at the scheduled time. Moving the consumer or delaying it may resolve that dependency but consume resources needed elsewhere. This is an illustrative mapping conflict, not a reported RAM-CGRA test case.

A method that accounts for reachability earlier may avoid exploring some infeasible assignments. The benefit depends on the cost and precision of that early check. A conservative check may reject valid options; an optimistic check may allow options that fail during detailed routing. The source does not specify RAM-CGRA's treatment of this tradeoff.

## Static connectivity is not the whole feasibility test

Two resources can be connected in the hardware topology while a particular transfer remains unavailable because another transfer occupies the path at the needed time. Conversely, a longer route or additional waiting may make a dependency feasible at a different cost.

The definition of reachability therefore needs the relevant resource and timing model. It may involve link use, available storage, operation compatibility, and the schedule. The captured description does not identify which of these conditions the proposed method includes, so no complete routing guarantee can be inferred.

It also does not specify whether the mapper targets loops, straight-line kernels, or a broader computation model. Those differences affect how resource reuse and timing are represented.

## Mapping success and execution efficiency are different outcomes

A successful mapping fits the computation within the stated architecture constraints. It may still execute slowly or consume more energy than another successful mapping. Finding any valid implementation and finding a good implementation are distinct optimization goals.

For repeated loop execution, an initiation interval describes the spacing between successive iteration starts in a pipelined schedule. A shorter interval can improve sustained throughput, but it is not the same as the latency of one iteration or the total time of a finite workload. The record lists initiation interval among missing evaluation quantities; it does not provide a measured value.

Compile time is another separate cost. A more thorough search can find better mappings while requiring longer preparation. The intended use determines whether that cost can be spread across enough subsequent executions to be worthwhile.

## What a controlled comparison requires

Candidate mappers should receive the same kernels, operation definitions, array topology, resources, and timing assumptions. Otherwise a higher success rate may reflect a less constrained target rather than a better mapping method. Timeouts and unsupported kernels should remain visible in the denominator.

The evaluation should report successful mappings, search time, execution schedules, and reference-checked functional behavior. If it claims energy improvements, the complete mapped execution needs an energy model or measurements rather than an inference from routing success alone.

The captured description supplies no mapping-success rate, initiation interval, compilation time, area, or energy results. It therefore cannot establish superiority over routing-oblivious mapping or list scheduling, which appear only as comparison categories in the coding.

<span id="explanation-dac-2026-research1712"></span>

## RAM-CGRA: reachability is a constraint on the schedule, not a final route check

### A CGRA mapping must construct a timed data path

A CGRA contains processing elements and configurable connections. A computation can be represented as operations with dependencies: an operation cannot run until its inputs are available, and its result must reach the next operation before that consumer's scheduled time. Mapping therefore chooses a processing element, a time, and a route for each dependency.

RAM-CGRA is described as reachability-aware mapping. The key problem is that placement, scheduling and routing are coupled. A consumer can be placed on an idle processing element and still be infeasible if a link, switch, buffer or time slot cannot carry its input. Conversely, a placement that appears farther away may be feasible if the route and schedule provide the required transfer time.

### Reachability needs a defined state and time model

Static topology tells which resources can be connected in principle. It does not tell whether a path is available at the time a value must cross it. A complete reachability predicate may need link occupancy, routing direction, storage for intermediate values, operation compatibility, configuration changes and the schedule. If the predicate is conservative, it can reject mappings that a detailed router could realize. If it is optimistic, it can allow candidates that fail later.

The captured official description does not expose which resources RAM-CGRA models, how it updates reachability during placement or scheduling, or how it handles loops and repeated iterations. No complete routing guarantee is inferred from the name. The method's value depends on whether its early feasibility test is both cheaper than detailed routing and accurate enough to preserve useful candidates.

### A valid mapping is not automatically a fast mapping

Mapping success answers whether the computation can be placed and executed under the stated constraints. It does not answer how long one iteration takes, how often a loop can start, how much configuration or communication work is required, or how much energy the execution consumes. For a pipelined loop, initiation interval measures the spacing between iteration starts; it is different from single-iteration latency and finite-job completion time.

A reachability-aware mapper may reduce wasted search by rejecting impossible candidates early, but that saving must include the reachability analysis itself and the cost of any later routing or repair. A more thorough search can produce better schedules while increasing compile time. The useful comparison is total compilation plus execution cost for a stated reuse count, not only the quality of the selected schedule.

### The comparison must hold the architecture and kernel fixed

Routing-oblivious mapping and list scheduling are named comparison categories. To interpret their results, all methods need the same operation graph, supported operations, array dimensions, connection topology, link timing, resource counts, configuration cost and timeout policy. Unsupported kernels and timed-out searches must remain in the denominator.

Functional correctness should be checked against a software or independently specified reference. Performance should report mapping success, initiation interval, latency, compile time and execution time separately. Energy claims need a defined boundary covering configuration, transfers, active processing elements and any external memory. The source reports none of these numeric results.

### What RAM-CGRA establishes and what remains open

The accessible description establishes the proposed purpose of incorporating communication reachability into CGRA mapping instead of deferring it to final routing. It does not establish a particular reachability algorithm, universal mapping success, quantified performance or energy improvement, or coverage of physical constraints. A stronger evaluation would publish the topology and timing model, reachability predicate, kernel suite, success/timeout denominator, schedule and route outputs, compile budget, initiation intervals, functional checks, energy model and tests across different arrays and kernels.

[Official DAC description, record RESEARCH1712](https://63dac.conference-program.com/presentation/?id=RESEARCH1712&sess=sess109)

## The longer-term implication

RAM-CGRA motivates treating communication feasibility as part of mapping rather than a final afterthought. The decisive research question is whether that awareness reduces wasted search and produces better valid schedules across different kernels and architectures.

Answering it requires a reproducible definition of reachability, independent correctness checks, and complete search and execution costs. The current record supports the proposed purpose, not universal mapping success, a quantified performance gain, or evidence that all physical constraints have been addressed.

## Compare the results carefully

First identify the inputs and required output quality. Then identify the limited resource: time, memory, communication, energy, circuit area, or correctness coverage. Ask which part of the method reduces that cost and which new cost it adds. Compare numbers only when the experiments hold these conditions sufficiently similar.

A conference description may explain the proposal while omitting the full experiment. An author preprint link may have been coded from its abstract. The source classification does not by itself establish that every table was read. Missing locations remain visible below.

## Complete captured evidence

These are evidence records, not substitutes for the explanations above. Each record preserves its problem, proposed method, measurements, comparison conditions, and source limits. A populated record does not establish that its mechanism has been fully explained or independently verified.

<span id="paper-dac-2026-research1712"></span>

### RAM-CGRA: Reachability-Aware Mapping for CGRAs

DAC 2026 · Record: `dac-2026-research1712`

[Read the step-by-step explanation](#explanation-dac-2026-research1712)

**Updated source-backed reading card**

Reviewed 2026-09-08. Deepens the official-description reading; separates timed reachability, placement/scheduling/routing coupling, mapping success, execution performance and missing architecture-diverse validation.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

CGRA mapping can fail when communication reachability is ignored during placement and scheduling.

**Mechanism / artifact:**

Reachability-aware CGRA mapping algorithm.

**Workload — the work tested:**

CGRA kernels; operation graphs, loops, arrays, topologies, supported operations and reference behavior are unspecified.

**Hardware and manufacturing assumptions:**

Coarse-grained reconfigurable array with constrained interconnect; array dimensions, link timing, buffers, configuration cost and physical assumptions are unspecified.

**Baseline — the comparison method:**

Routing-oblivious CGRA mapping

List scheduling

**Reported measurements:**

Mapping success and efficiency are claimed qualitatively; no success rate, timeout denominator, initiation interval, latency, compile time, area or energy result is reported.

**Limits on the conclusion:**

Static connectivity is not a timed reachability guarantee; the source does not expose the reachability predicate, state update, loop handling or later routing/repair cost.

A valid mapping is not automatically a fast or energy-efficient execution; compile cost, configuration, transfers and external memory need separate accounting.

Official description only; kernel- and architecture-diverse functional validation and quantitative comparison were not performed.

**Source and location**

Evidence tier: Official DAC description; full manuscript and reproduction not performed. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH1712&sess=sess109)

DAC official description, Captured Description and Authors fields; record RESEARCH1712; no manuscript pages.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** routing-oblivious CGRA mapping

list scheduling

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH1712

**Hardware or process assumptions:** Coarse-grained reconfigurable array with constrained interconnect; array and timing assumptions are unspecified.

**Limits:** No mapping success, initiation interval, compile time, area, or energy results are reported.

Benefits may depend on topology.

Official description only; kernel and architecture-diverse validation is required.

**Method or artifact:** Reachability-aware CGRA mapping algorithm.

**Metrics:** Mapping success and efficiency are claimed qualitatively

**Problem:** CGRA mapping can fail when routing reachability is ignored during placement and scheduling.

**Workload or benchmark:** CGRA kernels; arrays, routing topology, and baselines are unspecified.

</details>

## What remains to establish

Resolve unspecified workloads, comparison methods, resource budgets, and source locations before generalizing a reported gain. This subject is represented by one paper and supports a case study, not evidence of recurrence or a long-term trend.

[All subthemes](../expanded-taxonomy-v1.md) · [Research directions](../directions/README.md)
