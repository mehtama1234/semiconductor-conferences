# Distributed and wafer scale inference

This subject has 1 record in the selected sample. This page explains where it fits, then presents all captured paper evidence without shortening the measurements or limitations.

[Definitions used in the paper records](../reading-guide-v1.md)

## Understand the parent subject first

- [Architecture and accelerators](../themes/architecture-and-accelerators.md)

## Mapping decides where work runs; routing decides how values arrive

Distributed inference divides a model's computation among processing resources. A mapping assigns work and data to those resources. Routing determines the paths used to transfer the values required by that assignment. These decisions interact: a balanced arithmetic assignment can still create concentrated communication that delays completion.

On a wafer-scale system, physical distance and the arrangement of cores or dies matter to those transfers. A logical connection is not automatically a cheap physical path. Faults can further change which resources and routes are usable, so performance must be evaluated on the system that remains available, not only an ideal intact topology.

The selected record is [BusyBarn](../observed-subthemes/distributed-and-wafer-scale-inference.md#paper-isca-2026-program-060), an exact-title artifact for *Mapping and Communication Optimizations with Fault Tolerance for Wafer-Scale LLM Inference*. The captured evidence is its Zenodo description, not an executed reproduction or the paper manuscript.

## What the artifact describes

The description identifies hierarchical mapping using simulated annealing and load-balanced, distance-aware, fault-tolerant routing. Hierarchical mapping makes choices at multiple resource scales rather than treating every assignment as unrelated. Simulated annealing is a search method that can temporarily accept worse candidate choices to explore alternatives; its practical result depends on the search settings and evaluation budget.

The captured description does not expose the mapping objective, hierarchy boundaries, annealing schedule, or route-selection algorithm. Those details must not be reconstructed from the labels. In particular, distance-aware routing does not establish that every transfer follows the shortest possible route: load balancing may favor a different path.

The key evaluation question is whether the combined choices reduce complete inference time under the stated physical and fault constraints. Improving an intermediate traffic metric is useful evidence but does not by itself answer that question.

## Collective bandwidth and application latency are distinct

The artifact lists AllGather and AllToAll bandwidth evaluations. AllGather distributes each participant's contributed data to all participants. AllToAll exchanges potentially different data between participant pairs. Their communication patterns and congestion can differ, so one collective's bandwidth does not characterize all model traffic.

The listed studies also include end-to-end latency for six language-model architectures. Application latency depends on when required values become available, not simply aggregate link capacity. Dependencies between computation and communication can leave resources waiting even when some links are idle.

The source does not name the six models, input sizes, batching conditions, or baseline values. Consequently this article reports no numerical speedup. Neither the existence of scripts nor the listed evaluation scope supplies the missing measurements.

## Fault tolerance needs a defined fault model

The artifact description lists power/fault and multi-fault scaling studies. To interpret them, the reader needs to know what fails, whether failures occur before or during execution, how they are detected, and which state must be recovered. A routing method that avoids known unavailable links addresses a different problem from recovering data after an unexpected failure.

The captured metadata does not specify those assumptions. It should therefore not be described as tolerating arbitrary faults or guaranteeing uninterrupted inference. A complete result would report both correctness and degraded performance, along with reconfiguration or recovery costs and cases where no usable mapping remains.

## The ablations are a useful plan, not verified findings

The described scripts target Figures 8–15 and include mapping/routing ablations, die-group and core-shape sensitivity, workload heatmaps, and runtime breakdown. Ablations remove or replace a component to examine its contribution. They can help distinguish the effects of mapping from routing when the rest of the experiment remains comparable.

However, this atlas has not established those results by executing the artifact. Environment versions, simulator settings, fault distributions, baseline implementations, and hardware calibration remain unresolved in the captured description. Intended reproducibility and successful independent reproduction are separate evidentiary states.

<span id="explanation-isca-2026-program-060"></span>

## BusyBarn: judge mapping, routing and fault handling as one inference path

### Distributed inference has two coupled schedules

The computation schedule assigns model operations and data to processing resources. The communication schedule moves activations, partial results, parameters or synchronization state between those resources. A mapping can balance arithmetic work while producing a communication hotspot; a route can balance links while making a dependent operation wait. Wafer-scale distance adds another constraint because a logical hop count can correspond to different physical path lengths and link costs.

BusyBarn's artifact description combines hierarchical mapping, simulated-annealing search, and load-balanced, distance-aware, fault-tolerant routing. These labels describe different decisions. Hierarchical mapping may choose groups before individual cores. Simulated annealing is a search procedure that explores alternatives under a cost function. Routing then selects paths subject to distance, load and available resources. The description does not expose the cost function, hierarchy boundaries, annealing schedule or route algorithm, so they are not reconstructed here.

### Collective communication does not equal application latency

AllGather requires every participant to receive the combined contributions. AllToAll allows different data to move between participant pairs. Their message dependencies, volume, contention and completion conditions differ. A high bandwidth for one collective does not prove that the full LLM execution has low latency.

Application latency also includes computation, synchronization, waiting for the last required transfer, setup, and any reconfiguration. Six unnamed LLM architectures are listed in the artifact description, but model names, input sizes, batch conditions and baseline values are not supplied. The existence of scripts or a figure list is not a measured speedup and does not establish end-to-end inference behavior.

### Fault tolerance changes the feasible topology

A fault model must state what can fail, when it fails, how it is detected, and what state is lost. Avoiding a known failed link is different from recovering an in-flight activation or remapping a partially completed computation. Multiple simultaneous faults can disconnect a region even when each individual fault is tolerable.

Fault-tolerant routing therefore has two outputs: a route that remains usable and a correctness/recovery procedure for the computation that depends on it. Reconfiguration can consume bandwidth and time, and a route that avoids a fault can be longer or more congested. The artifact description names power/fault and multi-fault scaling studies but does not specify the fault distribution, detection delay, state-recovery rule, or condition under which no mapping remains.

### Artifact availability is not artifact reproduction

The Zenodo record provides a concrete artifact identity and reproduction-script scope. It does not, by itself, establish that the scripts execute in the current environment, that the environment versions are pinned, or that their output matches the paper. A reproducible evaluation should record dependencies, seeds, simulator configuration, topology, model inputs, baseline implementations, numerical outputs, and the cost of mapping and recovery.

### What BusyBarn establishes and what remains open

The accessible evidence establishes an exact-title artifact for a proposed wafer-scale LLM inference workflow combining hierarchical mapping, simulated-annealing exploration, distance/load-aware routing and fault-tolerance studies. It does not establish numerical collective bandwidth, end-to-end latency, mapping quality, fault coverage, measured wafer-scale hardware behavior, or independent reproduction. A stronger evaluation would recover the manuscript, execute the pinned artifact, define the collective and application workloads, report complete optimization/reconfiguration costs, specify fault models and correctness checks, and compare intact and degraded systems under matched conditions.

[Zenodo artifact description](https://zenodo.org/records/19430308) · [Artifact DOI](https://doi.org/10.5281/zenodo.19430308)

## The long-term question supported here

BusyBarn motivates coordinating work placement and communication with the physical resources available under faults. Its value would be established by reproducible results showing correct complete inference, full optimization and recovery costs, and performance across declared geometries and workloads.

The artifact provides a concrete path toward such evaluation. It does not yet support a numerical ranking, measured wafer-scale hardware claims, or a forecast of broad adoption. The defensible insight is that mapping quality, routing quality, and fault handling must be judged together at the application level, while their individual contributions remain inspectable.

## Compare the results carefully

First identify the inputs and required output quality. Then identify the limited resource: time, memory, communication, energy, circuit area, or correctness coverage. Ask which part of the method reduces that cost and which new cost it adds. Compare numbers only when the experiments hold these conditions sufficiently similar.

A conference description may explain the proposal while omitting the full experiment. An author preprint link may have been coded from its abstract. The source classification does not by itself establish that every table was read. Missing locations remain visible below.

## Complete captured evidence

These are evidence records, not substitutes for the explanations above. Each record preserves its problem, proposed method, measurements, comparison conditions, and source limits. A populated record does not establish that its mechanism has been fully explained or independently verified.

<span id="paper-isca-2026-program-060"></span>

### Mapping and Communication Optimizations with Fault Tolerance for Wafer-Scale LLM Inference

ISCA 2026 · Record: `isca-2026-program-060`

[Read the step-by-step explanation](#explanation-isca-2026-program-060)

**Updated source-backed reading card**

Reviewed 2026-09-08. Deepens the exact-title artifact reading; separates mapping, routing, collective bandwidth, application latency, fault models and the boundary between artifact availability and reproduction.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Wafer-scale LLM inference must map computation and communication under physical distance, irregular traffic and faults without losing end-to-end progress.

**Mechanism / artifact:**

BusyBarn artifact: hierarchical simulated-annealing mapping plus load-balanced, distance-aware, fault-tolerant routing and reproduction scripts.

**Workload — the work tested:**

Artifact description names AllGather and AllToAll, six LLM architectures, die/core-shape studies, fault-scaling studies and mapping/routing ablations; model names, input sizes, topology, seeds and baselines are not exposed.

**Hardware and manufacturing assumptions:**

Wafer-scale simulated system with die/core geometry, power/fault conditions and distance-aware routing; simulator configuration, fault model, recovery state and hardware calibration are unspecified.

**Baseline — the comparison method:**

Mapping/routing ablations are listed but baseline implementations are not named

AllGather and AllToAll are workload classes, not interchangeable baselines

**Reported measurements:**

No quantitative result is established in the captured Zenodo description; bandwidth, end-to-end latency, mapping success, fault coverage and recovery cost remain withheld pending manuscript or execution.

**Limits on the conclusion:**

Collective bandwidth does not establish application latency; computation, synchronization, waiting, setup and reconfiguration remain in the end-to-end boundary.

Fault tolerance requires a defined fault type, timing, detection, state recovery and no-mapping condition; the description does not provide them.

Zenodo artifact identity and reproduction scripts are not independent execution; environment versions, seeds, simulator settings, numerical outputs and baseline conditions remain unresolved.

No manuscript PDF or full abstract was recovered; no wafer-scale hardware measurement or independent review is established.

**Source and location**

Evidence tier: Exact title artifact description; execution and independent acceptance not performed. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://zenodo.org/records/19430308)

Zenodo description; artifact DOI 10.5281/zenodo.19430308; separate artifact assessment dated 2026-09-06; manuscript not recovered.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_exact_artifact_description

**Baselines:** Artifact description lists mapping/routing ablation scope but does not name all baseline implementations

**Evidence locators:** **Fields:** method_or_artifact

workload_or_benchmark

**Location:** Zenodo description; artifact DOI 10.5281/zenodo.19430308

**Evidence url:** https://zenodo.org/records/19430308

**Hardware or process assumptions:** Wafer-scale simulated system with die/core geometry, power/fault conditions, and distance-aware routing; simulator configuration, fault model, and hardware calibration are not exposed in the Zenodo description.

**Limits:** Zenodo artifact metadata is not the paper manuscript and does not independently verify the reported results.

No quantitative claim is promoted until the artifact is run with pinned environment metadata or the manuscript supplies exact conditions and baselines.

Artifact authorship and title match the ISCA record, but acceptance and independent review remain pending.

**Method or artifact:** BusyBarn artifact: hierarchical simulated-annealing mapping plus load-balanced, distance-aware, fault-tolerant routing and reproducibility scripts.

**Metrics:** Not established in the captured evidence.

**Problem:** Wafer-scale LLM inference must map computation and communication under irregular traffic, physical distance, and faults without losing end-to-end throughput.

**Workload or benchmark:** Artifact description names AllGather and AllToAll communication, six LLM architectures, die/core shape studies, fault-scaling studies, and mapping/routing ablations; exact model names, input sizes, topology, and baseline values require manuscript or artifact execution.

</details>

#### Additional source assessment

This separately recorded check is dated 2026-09-06. It supplements the original record above and retains its own scope and uncertainty.

[Assessment record](../../isca/data/busybarn-artifact-primary-recovery-v1.json)

[Assessed source](https://zenodo.org/records/19430308)

**Extraction scope**

Zenodo artifact description for BusyBarn and its reproduction scripts; no manuscript PDF or full abstract recovered.

**Conditions**

The artifact description names AllGather and AllToAll, six LLM architectures, fault and power sensitivity, and mapping/routing ablations; exact platforms, baselines, seeds, numerical results, and metric units remain unextracted.

**Headline metric status**

withheld_pending_primary_paper

**Independent review status**

pending

## What remains to establish

Resolve unspecified workloads, comparison methods, resource budgets, and source locations before generalizing a reported gain. This subject is represented by one paper and supports a case study, not evidence of recurrence or a long-term trend.

[All subthemes](../expanded-taxonomy-v1.md) · [Research directions](../directions/README.md)
