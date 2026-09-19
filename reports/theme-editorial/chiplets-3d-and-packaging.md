## Follow the information crossing a die boundary

Partitioning a computation assigns operations and storage to different physical components. A producer on one die may need to send its result to a consumer on another. The consumer cannot use that result until the required bytes arrive. The connection also occupies physical space and consumes energy, while both endpoints require power delivery and cooling.

Suppose two sequential computation stages take three milliseconds each on one implementation. A partitioned design reduces each stage to two milliseconds but adds a three-millisecond transfer between them. Completion takes seven milliseconds rather than six. Overlapping different requests may improve throughput, but it does not erase the dependency within this request. These are illustrative numbers, not a result attributed to a paper.

This is the starting point for evaluating chiplets: which costs are reduced inside each part, and which costs appear at the boundaries? The examples below explain that question. Linked articles retain their source-specific conditions and gaps; this parent synthesis does not establish a manufactured system.

## A physical boundary needs more than a logical connection

A circuit connection describes the intended relationship between signals. Its implementation needs transmitters, receivers, wiring, timing rules, and a way to match requests with responses where appropriate. A package may connect dies side by side through an interconnection structure, or place active dies or layers above one another. These arrangements expose different distances, connection densities, assembly requirements, and heat paths.

Shorter distance alone does not establish lower application latency. A link can require buffering, conversion between interfaces, or coordination across clock domains. More available bandwidth helps only when the workload exposes sufficient independent transfers and the endpoints can supply and consume them.

The [interconnect chapter](../observed-subthemes/chiplet-interconnects.md) groups representation and network-design proposals. The [advanced-packaging chapter](../observed-subthemes/advanced-packaging-and-interconnect.md) addresses physical connection structures. Their results concern different parts of the path and cannot be ranked by a shared word such as bandwidth without matching the transferred work and measurement boundary.

## Partition according to communication, not component count alone

Two partitions can cut the same number of logical connections while transferring different amounts of data. One cut may carry a control bit infrequently; another may carry a large tensor every step. They also may lie on different dependency paths. Counting crossings can guide design, but traffic volume, burst timing, and criticality determine additional costs.

For a simple lower bound, transferring 100 million bytes over an interface sustaining 50 billion bytes per second requires two milliseconds. That excludes request setup, contention, protocol overhead not included in the stated useful bandwidth, and any waiting before the transfer starts. A peak physical signaling rate is not automatically the sustained useful byte rate.

[ChiPlanner's discussion](../observed-subthemes/chiplet-system-architecture.md#chiplanner-partition-with-an-estimate-of-the-physical-consequences) connects partitioning to approximate placement and timing. Its description-level evidence leaves absolute timing and cost-model conditions unresolved. The question is whether early estimates choose partitions that remain favorable after physical implementation, not merely whether the partitioner produces a better internal score.

This connects directly to the [physical-design theme](physical-design-and-manufacturing.md): geometric legality, extracted effects, clock behavior, and power delivery must survive the partition decision. A favorable early partition remains a candidate until those checks apply to the resulting assembly.

## Phase-specific hardware adds a scheduling obligation

Language-model prompt processing and subsequent token generation can expose different amounts of parallel work and data reuse. Specializing different resources for those phases may improve their local efficiency. The design then needs to transfer the necessary state and balance demand between the resources.

Imagine one phase can supply 100 requests per second while the next can complete only 60 under the same request distribution. Sustainable end-to-end throughput cannot exceed 60 without changing that distribution or adding capacity. The first phase's idle time or growing intermediate queue is part of the system behavior. Different prompt and output lengths can change which phase is limiting.

The manuscript-backed [DUET explanation](../observed-subthemes/chiplet-system-architecture.md#duet-give-different-inference-phases-different-hardware) preserves that boundary: the study assumes matched phase throughput without an explicit multi-request scheduler, uses simulation and synthesis, and models its baseline rather than measuring a complete baseline service. Its chiplet area scaling is not fabricated-package evidence.

This DUET is the phase-specific hybrid-model architecture, not the bit-sparsity Duet in the architecture chapter. Similar names must not merge their mechanisms or results. The [systems theme](systems-applications-and-workloads.md) supplies the further requirement to evaluate queueing, admission, initial response, and generation pace together.

## Thermal feasibility is spatial and time-dependent

Power describes the rate at which energy is used; temperature depends on where heat is produced and how it moves through materials to the surroundings. Two designs with the same total power can have different hottest locations. Placing power-dense components together can change local temperature even when total power stays fixed.

In a simplified steady-state model, temperature rise equals power multiplied by thermal resistance. Twenty watts through a two-kelvin-per-watt path gives a 40-kelvin rise. This calculation does not describe a complete stacked package: real temperature fields depend on multiple interacting paths, geometry, materials, and boundary conditions. A temperature difference of one kelvin has the same magnitude as one degree Celsius; absolute temperature scales differ.

Steady-state analysis describes settled conditions. A changing workload additionally requires a transient model describing how temperatures evolve. A predictor accurate for one cooling arrangement or power map is not thereby validated for a different stack or sudden power change.

The [thermal chapter](../observed-subthemes/3d-stacking-and-thermal-management.md) explicitly separates prediction, reconstruction from observations, and control. LegoTherm's reduced models, learned predictors, and analytical solvers there have different recorded scopes and error definitions. A low average temperature error does not bound the error at the hottest location, and a faster prediction does not prove safe control.

## Cooling and throttling belong in performance accounting

A design may reduce operating frequency to keep temperatures within a limit. This can preserve operation while reducing sustained work per second. Reporting performance before the thermal response settles can conceal that tradeoff.

For an illustrative ten-second run, suppose execution completes 100 work units per second for two seconds, then 50 for the remaining eight. Total work is 600 units, or 60 per second on average, not the initial rate of 100. A fair comparison states startup conditions, cooling, workload duration, and the temperature rule that changes operation.

Moving work to a cooler region can also move its data, disrupt reuse, or overload another connection. The thermal benefit must be evaluated with those costs. Temperature simulation supports a prediction under its model; it does not alone establish long-term manufactured reliability.

## Assembly and testing change the cost denominator

Smaller separately manufactured parts can be tested and selected before assembly, but the package introduces its own cost and possible failures. Cost per attempted package differs from cost per accepted working package. A useful model must state die cost, screening, assembly, rework where supported, and final acceptance criteria.

As a deliberately simplified example, if an attempt consumes 100 cost units and final acceptance is 80%, long-run cost per accepted output is 125 units when failed attempts are unrecoverable and all attempts cost the same. This is not a chiplet cost forecast. Recovery, correlated failures, different die populations, and test coverage alter the calculation.

Do not multiply generic die-yield numbers to predict package yield without justified independence and assembly assumptions. Passing a test also establishes only the properties covered under its conditions. Connectivity testing, functional testing, thermal behavior, and lifetime qualification address different failure mechanisms.

## Keep the comparison at the complete-system boundary

| Local claim | Additional condition needed |
| --- | --- |
| A specialized die executes faster | Transfer and phase scheduling preserve the end-to-end benefit |
| A package offers more link bandwidth | Useful traffic can exploit it without endpoint or queue limits |
| An early partition has better timing | Physical implementation and extracted analysis retain the result |
| A thermal estimator is faster | Critical-location and transient errors are acceptable for its use |
| Smaller parts reduce one manufacturing cost | Assembly, testing, failures, and accepted-system cost remain favorable |

These conditions connect the papers without pretending they are already integrated. The [tooling theme](design-methodology-and-tooling.md) explains preparation and search budgets; the [memory theme](memory-interconnect-and-storage.md) explains data availability and progress. Both remain relevant when resources are reorganized inside a package rather than across servers.

## Long-term hypotheses with explicit tests

One hypothesis is that partitioning increasingly needs workload and physical estimates together. Compare early joint planning with staged planning under the same final implementation checks. It weakens when estimate errors cause extra repair or staged methods reach equivalent outcomes more cheaply.

A second hypothesis is that phase specialization helps only when communication and phase demand remain compatible with resource allocation. Vary request distributions, handoff sizes, and concurrency, including imbalance. It weakens when idle capacity, transfers, or scheduling consume the local gain.

A third hypothesis is that thermal constraints change the ranking of high-density designs. Compare sustained useful work under equal declared cooling and temperature limits, not only initial performance. It weakens as a distinguishing factor where candidate rankings remain unchanged over realistic power maps and durations.

These are bounded interpretations, not established ISCA–DAC–ICCAD time trends or evidence of commercial adoption. Matched editions, workloads, technology assumptions, cooling, cost models, and source depth remain needed. This expanded parent discussion does not complete individual-paper source recovery, deeper writing, manufactured validation, or independent scientific and comprehension review.
