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

[ChiPlanner's discussion](../observed-subthemes/chiplet-system-architecture.md#chiplanner-partition-with-an-estimate-of-the-physical-consequences) ties partitioning to rough placement and timing. Its description-level evidence leaves absolute timing and cost-model conditions open. The real question: do early estimates pick partitions that stay good after physical implementation, not just score better inside the partitioner?

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

A predictor accurate for one cooling setup or power map is not validated for a different stack or a sudden power change.

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

**Be careful:** this parent discussion does not complete individual-paper source recovery, deeper writing, manufactured validation, or independent scientific and comprehension review.
