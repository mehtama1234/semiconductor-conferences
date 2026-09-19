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
