# Chiplets, 3D integration, and packaging

This article explains the subject and then connects it to 25 papers in the selected research sample.

A subtheme groups related technical problems. A mechanism describes the particular change proposed by a paper. The discussion below explains the subject; the linked paper records state the available evidence.

[Definitions used in the paper records](../reading-guide-v1.md)

## Splitting a system into several dies adds boundaries data must cross

A **die** is a piece of semiconductor carrying circuits. A package can connect several dies. When they are designed as parts of one larger system they are often called **chiplets**. A **three-dimensional (3D)** design stacks active layers or dies on top of each other.

Splitting lets different functions use different manufacturing processes. The cost is that communication must cross extra physical boundaries.

## Each boundary costs area, energy, time and heat

- A link between dies uses area, energy and time.
- The package must deliver current to, and remove heat from, every active part.
- Stacked parts can sit far from a good cooling path.

So moving computation between dies changes communication and temperature together. A system choice cannot be judged from the speed of one die alone.

## The subthemes split, connect, cool, or design the package

- **Partitioning** decides which functions belong together.
- **Interconnect** designs the communication between the parts.
- **Thermal** methods estimate temperatures and choose placement or operation to stay within limits.
- **Package co-design** studies these choices together with power delivery and physical assembly.

One paper may address several of these.

## A fair test states the physical setup and compares whole systems

1. State die sizes, link rates, cooling, power assumptions, workload placement and the manufacturing assumptions used for cost.
2. Compare the full system under the same temperature and performance limits.

A thermal simulation supports a temperature prediction under its model. Reliability and yield of manufactured parts need their own evidence.

## Follow the information crossing a die boundary

Splitting work across dies makes each part cheaper or faster, but adds a cost wherever data crosses between them.

**Partitioning** a computation assigns operations and storage to different physical parts. A producer on one die may need to send its result to a consumer on another. The consumer cannot use it until the bytes arrive. The connection also takes space and energy, and both ends need power and cooling.

> **Worked example (illustrative, not from a paper).** Two stages run one after the other.
>
> - One implementation: 3 + 3 = **6 milliseconds**.
> - Partitioned: each stage drops to 2 milliseconds, but a 3-millisecond transfer sits between them: 2 + 3 + 2 = **7 milliseconds**.
>
> Overlapping different requests may raise throughput. It does not remove the dependency inside this request.

So the starting question for chiplets is: which costs shrink inside each part, and which appear at the boundaries?

**Be careful:** linked articles keep their source-specific conditions and gaps. This parent synthesis does not establish a manufactured system.

## A physical boundary needs more than a logical connection

A link between dies needs real hardware and rules, and a shorter link is not automatically faster for the application.

A circuit connection describes how signals should relate. Building it needs transmitters, receivers, wiring, timing rules, and a way to match requests with responses where needed.

A package can:

- connect dies side by side through an interconnection structure; or
- stack active dies or layers on top of each other.

These differ in distance, connection density, assembly needs and heat paths.

Shorter distance alone does not mean lower application latency. A link may need buffering, conversion between interfaces, or coordination across different clocks. More bandwidth helps only when the workload offers enough independent transfers, and both ends can keep up.

- The [interconnect chapter](../observed-subthemes/chiplet-interconnects.md) groups representation and network-design proposals.
- The [advanced-packaging chapter](../observed-subthemes/advanced-packaging-and-interconnect.md) covers physical connection structures.

**Be careful:** their results concern different parts of the path. A shared word such as "bandwidth" cannot rank them unless the transferred work and measurement boundary match.

## Partition according to communication, not component count alone

What matters at a cut is how much data crosses it and when, not how many wires it cuts.

Two partitions can cut the same number of logical connections, yet move very different amounts of data:

- one cut may carry a control bit now and then;
- another may carry a large tensor every step.

They may also sit on different dependency paths. Counting crossings can guide design, but traffic volume, burst timing and criticality decide the extra cost.

> **Worked example (lower bound).** Move 100 million bytes over an interface sustaining 50 billion bytes per second.
>
> 100,000,000 ÷ 50,000,000,000 = 0.002 seconds = **2 milliseconds**.

That excludes request setup, contention, protocol overhead outside the stated useful bandwidth, and any wait before the transfer starts. A peak physical signaling rate is not automatically the sustained useful byte rate.

[ChiPlanner's discussion](../observed-subthemes/chiplet-system-architecture.md#chiplanner-partition-with-an-estimate-of-the-physical-consequences) ties partitioning to rough placement and timing. Its description-level evidence leaves absolute timing and cost-model conditions open. The real question: do early estimates pick splits that stay good once the chip is laid out? Scoring well inside the splitting tool is not enough.

This links to the [physical-design theme](physical-design-and-manufacturing.md). Legal geometry, extracted effects, clock behavior and power delivery must all survive the partition. A good early partition stays a candidate until those checks are applied to the assembled result.

## Phase-specific hardware adds a scheduling obligation

Giving each phase its own hardware only pays if the phases stay balanced and the hand-off is counted.

Language-model prompt processing and later token generation can offer different amounts of parallel work and data reuse. Specializing hardware for each phase may make each more efficient on its own. The design must then pass the needed state between them, and balance demand.

> **Worked example.** Under the same request mix:
>
> - phase one can supply **100** requests per second;
> - phase two can complete only **60**.
>
> End-to-end throughput cannot exceed **60** without changing the mix or adding capacity.

The first phase's idle time, or its growing queue of waiting work, is part of the system's behavior. Different prompt and output lengths can change which phase is the limit.

The manuscript-backed [DUET explanation](../observed-subthemes/chiplet-system-architecture.md#duet-give-different-inference-phases-different-hardware) keeps that boundary:

- the study assumes matched phase throughput, without an explicit multi-request scheduler;
- it uses simulation and synthesis;
- it models its baseline rather than measuring a complete baseline service.

Its chiplet area scaling is not evidence from a fabricated package.

**Be careful:** this DUET is the phase-specific hybrid-model architecture, not the bit-sparsity Duet in the architecture chapter. Similar names must not merge their mechanisms or results.

The [systems theme](systems-applications-and-workloads.md) adds a further duty: judge queueing, admission, first response and generation pace together.

## Thermal feasibility is spatial and time-dependent

Temperature depends on where heat is made and how it escapes, not only on total power.

**Power** is the rate of energy use. **Temperature** depends on where heat is produced and how it flows through materials to the surroundings. Two designs with the same total power can have different hot spots. Grouping power-dense parts together can raise local temperature, even at fixed total power.

> **Worked example (simplified steady state).** Temperature rise = power × thermal resistance.
>
> 20 watts through a path of 2 kelvin per watt: 20 × 2 = **40 kelvin** rise.

This does not describe a full stacked package. Real temperature fields depend on many interacting paths, geometry, materials and boundary conditions. A difference of one kelvin is the same size as one degree Celsius, though the absolute scales differ.

- **Steady-state** analysis describes settled conditions.
- A changing workload also needs a **transient** model of how temperatures evolve.

A predictor tested on one cooling setup or power map is not tested on another. A different stack or a sudden power change needs its own check.

The [thermal chapter](../observed-subthemes/3d-stacking-and-thermal-management.md) separates prediction, reconstruction from observations, and control. LegoTherm's reduced models, learned predictors and analytical solvers there have different recorded scopes and error definitions.

**Be careful:** a low average temperature error does not bound the error at the hottest spot. A faster prediction does not prove safe control.

## Cooling and throttling belong in performance accounting

If heat forces a slowdown, the slower rate is the real performance.

A design may lower its clock frequency to stay within a temperature limit. That keeps it running, but cuts sustained work per second. Reporting performance before the thermal response settles hides this trade-off.

> **Worked example (illustrative ten-second run).**
>
> - 100 work units per second for 2 seconds: 200 units.
> - 50 per second for the remaining 8 seconds: 400 units.
> - Total 600 units, so the average is 600 ÷ 10 = **60 per second**, not the starting 100.

A fair comparison states start-up conditions, cooling, workload length, and the temperature rule that changes operation.

Moving work to a cooler region can also move its data, break reuse, or overload another connection. The thermal benefit must be weighed with those costs.

**Be careful:** temperature simulation supports a prediction under its model. It does not, alone, establish long-term reliability of manufactured parts.

## Assembly and testing change the cost denominator

Count the cost per working package delivered, not per package attempted.

Smaller, separately made parts can be tested and selected before assembly. But the package brings its own cost and failures. A useful cost model states:

- die cost;
- screening;
- assembly;
- rework, where possible;
- final acceptance criteria.

> **Worked example (deliberately simplified, not a chiplet cost forecast).** Each attempt costs 100 units, and 80% are accepted. If failed attempts cannot be recovered and every attempt costs the same:
>
> Cost per accepted output = 100 ÷ 0.8 = **125 units**.

Recovery, linked failures, different die populations and test coverage all change this.

**Be careful:** do not multiply generic die-yield numbers to predict package yield without justified independence and assembly assumptions. A passed test covers only the properties it checks, under its conditions. Connectivity testing, functional testing, thermal behavior and lifetime qualification each address different failure mechanisms.

## Keep the comparison at the complete-system boundary

Each local gain needs one more condition before it counts for the whole system.

| Local claim | Additional condition needed |
| --- | --- |
| A specialized die executes faster | Transfer and phase scheduling preserve the end-to-end benefit |
| A package offers more link bandwidth | Useful traffic can exploit it without endpoint or queue limits |
| An early partition has better timing | Physical implementation and extracted analysis retain the result |
| A thermal estimator is faster | Critical-location and transient errors are acceptable for its use |
| Smaller parts reduce one manufacturing cost | Assembly, testing, failures, and accepted-system cost remain favorable |

These conditions link the papers without pretending they are already integrated. The [tooling theme](design-methodology-and-tooling.md) covers preparation and search budgets. The [memory theme](memory-interconnect-and-storage.md) covers data availability and progress. Both still apply when resources are reorganized inside a package instead of across servers.

## Long-term hypotheses with explicit tests

Three readings are worth testing; each names what would weaken it.

| Hypothesis | Test | What would weaken it |
| --- | --- | --- |
| Partitioning increasingly needs workload and physical estimates together | Compare early joint planning with step-by-step planning, under the same final implementation checks | Estimate errors cause extra repair, or staged methods reach the same outcome more cheaply |
| Phase specialization helps only when communication and phase demand fit the resource split | Vary request mixes, hand-off sizes and concurrency, including imbalance | Idle capacity, transfers or scheduling use up the local gain |
| Thermal limits change the ranking of high-density designs | Compare sustained useful work under equal declared cooling and temperature limits, not just initial performance | Rankings stay the same across realistic power maps and durations |

These are bounded interpretations, not established ISCA–DAC–ICCAD time trends or evidence of commercial adoption. Matched editions, workloads, technology assumptions, cooling, cost models and source depth are still needed.

**Be careful:** this overview is not the end of the work. Full sources, deeper write-ups, checks on made chips and independent review are still open.

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
