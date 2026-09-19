# Chiplets, 3D integration, and packaging

This article explains the subject and then connects it to 25 papers in the selected research sample.

A subtheme groups related technical problems. A mechanism describes the particular change proposed by a paper. The discussion below explains the subject; the linked paper records state the available evidence.

[Definitions used in the paper records](../reading-guide-v1.md)

## Why a system can contain several dies

A die is a piece of semiconductor containing circuits. A package can connect several dies, often called chiplets when designed as components of a larger system. A three-dimensional design places active layers or dies above one another. Partitioning can let different functions use different manufacturing processes, but communication must cross additional physical boundaries.

## The costs introduced by partitioning

A connection between dies consumes physical area, energy, and time. The package must deliver current and remove heat from every active part. Stacked parts can place heat sources farther from an effective cooling path. Moving computation between dies therefore changes communication and temperature together. A system-level choice cannot be evaluated solely from the speed of an individual die.

## What separates the subthemes

Partitioning methods decide which functions belong together. Interconnect methods design communication between the parts. Thermal methods estimate temperatures and choose placement or operation to stay within limits. Package co-design studies these decisions jointly with power delivery and physical assembly. Each branch concerns a different variable, although a single paper may address several.

## A comparison that answers the question

State die dimensions, link rates, cooling conditions, power assumptions, workload placement, and the manufacturing assumptions used for cost. Compare the full system while respecting the same temperature and performance limits. Thermal simulation supports a temperature prediction under its model; manufactured reliability and yield need their own evidence.

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

## Subthemes and how to study them

Each link opens the subtheme discussion and its captured paper records. Explanatory depth varies: some papers have expanded individual explanations; others still have only brief discussion or evidence cards. Source locations and unresolved conditions remain visible.

### [3d stacking and thermal management](../observed-subthemes/3d-stacking-and-thermal-management.md)

7 selected records in this theme. Start with [COOL: A Cooling-Aware Point Transformer Framework for Thermal Prediction in Advanced 3D/3.5D IC Packaging](../observed-subthemes/3d-stacking-and-thermal-management.md).

### [3d integration and thermal management](../observed-subthemes/3d-integration-and-thermal-management.md)

6 selected records in this theme. Start with [Thermal Stability Strategy for a 12nm/28nm Hybrid-Bonding Wafer-on-Wafer 3D-Integrated Eflash In-Memory Computing SoC](../observed-subthemes/3d-integration-and-thermal-management.md).

### [Chiplet system architecture](../observed-subthemes/chiplet-system-architecture.md)

3 selected records in this theme. Start with [DUET: Disaggregated Hybrid Mamba-Transformer LLMs with Prefill and Decode-Specific Packages](../observed-subthemes/chiplet-system-architecture.md).

### [Advanced packaging and interconnect](../observed-subthemes/advanced-packaging-and-interconnect.md)

2 selected records in this theme. Start with [Mixed-Structure Double-Sided Redistribution Layer Routing for Glass Interposer-Based 5.5D ICs](../observed-subthemes/advanced-packaging-and-interconnect.md).

### [Chiplet interconnects](../observed-subthemes/chiplet-interconnects.md)

2 selected records in this theme. Start with [LEXI: Lossless Exponent Coding for Efficient Inter-Chiplet Communication in Hybrid LLMs](../observed-subthemes/chiplet-interconnects.md).

### [Wafer scale and heterogeneous integration](../observed-subthemes/wafer-scale-and-heterogeneous-integration.md)

2 selected records in this theme. Start with [Hyperwafer: Communication-Aware Sparse Matrix Multiplication on Wafer-Scale Chips](../observed-subthemes/wafer-scale-and-heterogeneous-integration.md).

### [Chiplet partitioning and integration](../observed-subthemes/chiplet-partitioning-and-integration.md)

1 selected records in this theme. Start with [MAHL: Multi-Agent LLM-Guided Hierarchical Chiplet Design with Adaptive Debugging](../observed-subthemes/chiplet-partitioning-and-integration.md).

### [Chiplets and heterogeneous integration](../observed-subthemes/chiplets-and-heterogeneous-integration.md)

1 selected records in this theme. Start with [Hbspec: A Hybrid-Bonding-Based Heterogeneous Accelerator for Efficient Tree-Structured Speculative Decoding](../observed-subthemes/chiplets-and-heterogeneous-integration.md).

### [Package system co design](../observed-subthemes/package-system-co-design.md)

1 selected records in this theme. Start with [BLADE: Bi-Level Bayesian Optimization for Metal-Density-Constrained Multi-Layer Package Power/ground Plane Synthesis](../observed-subthemes/package-system-co-design.md).

## Representative source-backed records

The following reading set spans the available conferences and uses dated corrections where registered. These corrections improve the current reading view but do not change historical adjudication or establish independent acceptance. Each paper link opens its exact evidence card.

## Paper cards: what changes and where it stops

- [Integrated Timing-Driven Placement for Hybrid-Bonding-Based Face-to-Face 3D ICs](../observed-subthemes/3d-integration-and-thermal-management.md#paper-dac-2026-research900) — DAC 2026.
- [Mixed-Structure Double-Sided Redistribution Layer Routing for Glass Interposer-Based 5.5D ICs](../observed-subthemes/advanced-packaging-and-interconnect.md#paper-dac-2026-research799) — DAC 2026.
- [RTL-3D: Timing-Aware Tier Partitioning for 3D ICs Using Pre-Synthesis Timing Analysis](../observed-subthemes/3d-integration-and-thermal-management.md#paper-dac-2026-research793) — DAC 2026.
- [From Fluid Dynamics to Chip Design: PDE Foundation Model Address Data Bottleneck in 3D-ICs Thermal Simulation](../observed-subthemes/3d-stacking-and-thermal-management.md#paper-dac-2026-research553) — DAC 2026.
- [MAHL: Multi-Agent LLM-Guided Hierarchical Chiplet Design with Adaptive Debugging](../observed-subthemes/chiplet-partitioning-and-integration.md#paper-iccad-2025-1207) — ICCAD 2025.
- [Tasa: Thermal-aware 3D-Stacked Architecture Design with Bandwidth Sharing for LLM Inference](../observed-subthemes/3d-stacking-and-thermal-management.md#paper-iccad-2025-1103) — ICCAD 2025.
- [Flexicts: CPPR-Aware 3D Clock Tree Synthesis for Face-to-Face Bonded ICs](../observed-subthemes/3d-integration-and-thermal-management.md#paper-dac-2026-research518) — DAC 2026.
- [ChiSER: Surrogate-Enhanced Resource-Aware Exploration of Chiplet-Based Deep Neural Network Accelerators](../observed-subthemes/chiplet-system-architecture.md#paper-dac-2026-research399) — DAC 2026.
- [Chiplanner: Physically-Aware and Timing-Driven Design Planner for 2.5D Multi-Chiplet Systems](../observed-subthemes/chiplet-system-architecture.md#paper-dac-2026-research380) — DAC 2026.
- [Network Design for Wafer-Scale Systems with Wafer-on-Wafer Hybrid Bonding](../observed-subthemes/chiplet-interconnects.md#paper-dac-2026-research363) — DAC 2026.
- [LEXI: Lossless Exponent Coding for Efficient Inter-Chiplet Communication in Hybrid LLMs](../observed-subthemes/chiplet-interconnects.md#paper-dac-2026-research3121) — DAC 2026.
- [DUET: Disaggregated Hybrid Mamba-Transformer LLMs with Prefill and Decode-Specific Packages](../observed-subthemes/chiplet-system-architecture.md#paper-dac-2026-research3120) — DAC 2026.

## What the evidence supports

These records identify proposed methods and the conditions recorded for them. A reported improvement should be interpreted with its comparison method, input size, hardware, and result-quality requirement. Missing fields are evidence gaps; a populated field can also state that a detail is unspecified.

## Limits and next evidence

The selected sample is uneven across conferences and source types. It cannot establish how fast a subject is growing. Repeated observations across comparable years, with the same inclusion rules and source depth, are needed for a time trend.

Every linked evidence article preserves the Problem: and Mechanism / artifact: fields, baseline, unshortened limitations, source URL, and recorded location. Primary text and independent review remain necessary where the record says those checks are open.

[Research directions](../directions/README.md) · [All observed subthemes](../expanded-taxonomy-v1.md)
