# Physical design and manufacturing

This article explains the subject and then connects it to 42 papers in the selected research sample.

A subtheme groups related technical problems. A mechanism describes the particular change proposed by a paper. The discussion below explains the subject; the linked paper records state the available evidence.

[Definitions used in the paper records](../reading-guide-v1.md)

## A correct connection can still arrive too late once it becomes a wire

A circuit description lists components and their connections. Manufacturing needs real shapes in specified material layers.

1. **Placement** chooses where each component sits.
2. **Routing** chooses each wire's path and layer.

Wires take up space, resist current and store electric charge. Their length and surroundings change how fast a signal switches. So a logically correct connection can still arrive too late.

## Every physical fix pushes on another part of the design

- Moving two communicating components closer shortens a wire, but can crowd another region.
- Adding a buffer can improve signal timing, but adds area and power.
- Manufacturing rules limit widths, spacing and overlaps.
- Changes in fabrication can change how transistors and wires behave.

An optimizer must meet all these conditions together. Improving one score while quietly breaking another does not count.

## The subthemes build geometry, estimate timing, or model manufacturing

- **Placement and routing** methods build the geometry.
- **Timing analysis** estimates whether signals switch in time.
- **Process models** estimate how fabricated devices behave.
- **Manufacturing and yield** methods study defects and variation. Yield is the fraction of manufactured chips that meet requirements.

A faster estimator and a better final layout are different contributions. They need different evidence.

## A fair test uses the same circuits and rules, and counts violations

1. Use the same circuit set, manufacturing rules, timing requirements and implementation tools.
2. Record violations as well as successful outputs.
3. Check the chosen designs with an accurate enough final evaluation, and count all search time.
4. If a method uses a cheaper approximation, check whether its errors change which design is chosen.

## Follow a logical connection into a physical implementation

A logical connection says what links to what; the physical version decides how fast and how well it works.

A **logical circuit** says which outputs depend on which inputs. A **physical implementation** gives sizes and locations to transistors, cells, wires, and connections between material layers. "These two terminals are connected" says nothing about the resistance, capacitance or travel time of the real connection.

> **Example.** Two placed cells are joined by a wire.
>
> - Moving them closer shortens that connection.
> - But each cell also connects to others.
> - The shorter route may pass through a region already full of other wires.

So the task is not to shorten one distance on its own. It is to build legal geometry that implements the circuit and meets timing, power and other stated limits.

**Be careful:** the examples below are teaching constructions, not measurements from the linked papers. Most physical-design branches still have incomplete source conditions. Connecting their mechanisms does not replace missing manuscripts or final implementation results.

## Placement creates demand; routing must find space for it

Where parts are placed decides how many wires must squeeze through each region.

- **Placement** gives each component a location.
- **Routing** gives each wire a real path and layer, including jumps between layers.

Early placement may estimate wire length with a simple distance. Final routing may need detours around obstacles or crowded areas, so that estimate is optimistic.

> **Worked example (simplified: one track per connection).** A corridor has room for 8 parallel tracks. 10 connections need to cross it.
>
> - At least 10 − 8 = **2** cannot use the corridor as assigned.
> - They need another route, another layer if one exists, or a placement change.
> - A low average wire length does not remove this local shortage.

Extra layers or different spacing are not always available. The technology and design rules limit both. A route that looks short in a drawing can break rules on minimum spacing, width, enclosure or allowed layer changes. The final result must meet the real rule set, not the optimizer's simplified geometry.

The [placement and routing chapter](../observed-subthemes/placement-routing-and-floorplanning.md) and [routing chapter](../observed-subthemes/physical-design-and-routing.md) group proposals for these decisions. Their labels name the stage being changed.

**Be careful:** they do not show that every proposed placement can be fully routed, or accepted for manufacturing.

## Timing depends on both data and clock arrival

A signal is on time only relative to when the clock arrives, and the clock travels too.

A synchronous circuit stores values at clock events. In a simplified maximum-delay check, data must arrive early enough before the receiving clock event.

**Slack** = allowed arrival time − actual (or estimated) arrival time.

> **Worked example.** Required: 100 picoseconds. Arrival: 103.
>
> - Slack = 100 − 103 = **−3 picoseconds**.
> - Negative slack is a violation, under this simplified setup.

Clock signals also travel through real wires and buffers, so they arrive at different places at different times. That difference changes how much time data has to travel between storage elements. A change that helps one maximum-delay check can hurt a minimum-delay check. So fixing one path is not complete **timing closure** (meeting every timing check at once).

- The [DCTS discussion](../observed-subthemes/placement-routing-and-timing.md#the-clock-also-has-to-arrive-on-time) links clock layout and buffer sizing. Its record still lacks complete final wiring and comparison conditions.
- The [manuscript-backed timing-reuse explanation](../observed-subthemes/compiler-and-runtime-optimization.md#explanation-dac-2026-research2566), in the tooling theme, shows why arrival estimates must keep their electrical context and error direction.

A faster timing calculation and a faster built circuit are different contributions.

## Cell sizing moves costs between connected components

Making one cell stronger can slow the cell that drives it.

A stronger driver may charge its load faster. It can also take more area, use more energy, and present a bigger load to the cell before it. So swapping a small cell for a larger one changes more than that cell's own delay.

> **Worked example (illustrative chain, not a device model).**
>
> - Strengthening the second cell cuts its delay by **4** time units.
> - The extra load adds **3** units to the first cell's delay. Net saving: 4 − 3 = **1** unit, not 4.
> - If the new size shifts placement and adds **2** units of wiring delay: −4 + 3 + 2 = **1 unit worse**.

[HyPAS's recorded method](../observed-subthemes/placement-routing-and-timing.md#paper-dac-2026-research1317) argues for choosing placement and sizing together. Its current evidence does not establish complete prediction error, repair cost or final gain. Optimizing jointly opens up more choices, but makes credit harder to assign. An evaluation must separate the combined result from each part's contribution.

## Power delivery changes the conditions used for timing

Timing analysis assumes a supply voltage that the power network may not actually deliver.

The supply network has electrical resistance.

> **Worked example (simple resistive model).**
>
> - Current 0.1 ampere through 0.2 ohm: voltage drop = 0.1 × 0.2 = **0.02 volt**.
> - A nominal 0.8-volt source then supplies 0.8 − 0.02 = **0.78 volt** past that element, ignoring other effects.
>
> Real networks spread current over many paths, and change with switching activity. This is only a basic illustration.

Placing many cells that switch at once in one area concentrates demand. Enlarging drivers to fix timing can raise it further. If delay analysis assumes a supply the network cannot provide, the timing gain may not survive real operation.

The [IR-drop-aware placement record](../observed-subthemes/placement-routing-and-timing.md#paper-dac-2026-research2297) links placement, supply-network changes and voltage analysis. Its description does not establish all activity assumptions or final power-integrity checks. A useful comparison says which switching patterns and operating conditions were tested, and which lie outside the model.

## Extraction connects geometry back to electrical analysis

Two layouts with the same connections can behave differently, so geometry must be turned back into electrical numbers.

**Extraction** estimates electrical properties of the physical geometry, such as wire resistance and capacitance. These affect signal delay, coupling between wires, and energy.

A fast learned or simplified extractor lets you evaluate more candidates. Judge its error where it changes decisions:

- choosing a different route;
- accepting a path that only looks valid;
- missing an interaction.

A small average error does not show the critical region is accurate enough.

This links physical design to the [AI-assisted EDA theme](ai-assisted-eda.md) and [tooling theme](design-methodology-and-tooling.md). Prediction, search and final checking need compatible definitions. A design chosen with a cheap model still needs a more trustworthy evaluation. Otherwise the process tends to select the model's optimistic mistakes.

## Manufacturing checks and yield answer different questions

Each manufacturing check answers its own question, and none alone predicts yield.

| Check | What it determines |
| --- | --- |
| Design-rule check | Whether geometry meets the specified rules |
| Pattern matching | Whether arrangements matching its query definitions are present |
| Lithography simulation | How a pattern is likely to print through the modeled process |
| Inspection | Whether manufactured material shows observable deviations |
| Functional testing | Whether produced devices show the specified behavior |

- [G-Matcher's explanation](../observed-subthemes/manufacturing-and-yield.md#searching-for-known-problematic-geometry) separates faster pattern search from evidence that unknown patterns are safe.
- The [clip-wise optimization discussion](../observed-subthemes/manufacturing-and-yield.md#scheduling-the-computation-that-produces-a-mask) separates sharing computation among regions from making the simulator more accurate. Improvements in separate regions must also hold at their boundaries when joined.

**Yield** is the fraction of manufactured devices that meet the acceptance requirements. A higher inspection-classifier score is not automatically higher yield. A process or design change needs evidence that more acceptable devices result, under comparable production conditions.

Rare defects also change what a classifier result means.

> **Worked example (illustrative counts, not from a captured paper).** 10,000 items are inspected; 100 are defective.
>
> - The classifier finds 90 defects: **recall** = 90 ÷ 100 = **90%**.
> - It also flags 99 good items. Flags total 90 + 99 = 189.
> - **Precision** = 90 ÷ 189 ≈ **47.6%** of flags are real defects.
>
> A high detection rate can still leave a large investigation burden.

The [inspection discussion](../observed-subthemes/manufacturing-and-yield.md#rare-defects-and-incomplete-labels) keeps two differences visible:

- synthetic training examples versus real evaluation defects;
- incomplete labels versus established ground truth.

Test splits should reflect transfer across wafers, time periods or conditions, not just nearby images from the same source.

## What a complete physical result must preserve

Each claimed gain needs companion evidence before it counts as a finished result.

| Claimed improvement | Necessary companion evidence |
| --- | --- |
| Shorter estimated wires | Legal detailed routes, congestion, and extracted effects |
| Faster critical paths | Other timing checks, clock assumptions, area, and power |
| Lower predicted voltage drop | Activity assumptions and final supply-network conditions |
| Faster physical estimation | Decision-relevant errors and validation of selected candidates |
| Better inspection scores | Real defect ground truth, false alarms, and separate yield evidence |

The full flow also includes failed candidates and repair. An optimizer that runs for ten minutes but needs ninety minutes of clean-up is not a ten-minute route to a finished layout. Fixing geometry can change electrical behavior, and fixing electrical behavior can need new geometry. Done means the chosen result meets every applicable requirement together, under stated conditions.

## Long-term hypotheses and disconfirming evidence

Three readings are worth testing; each names what would weaken it.

| Hypothesis | Test | What would weaken it |
| --- | --- | --- |
| Considering placement, wiring, timing and supply demand together, early, reduces later repair | Compare with step-by-step optimization, using the same final checks and total budget | Early models are inaccurate enough to cause extra rework, or staged methods do as well more cheaply |
| Faster estimation helps most when paired with decision-aware validation | Measure ranking changes, false feasibility calls and final accepted outputs, not just average error | The cheap model cannot safely filter candidates, or exact fallback eats the saving |
| Manufacturing learning needs evidence across the design-to-production boundary | Do predicted or detected patterns match verified physical or electrical effects, under independent conditions? | Gains stay inside simulation or image scores, without the claimed production outcome |

These are bounded interpretations, not established ISCA–DAC–ICCAD time trends. Comparable processes, rule sets, circuits, operating assumptions, tool budgets, source depth and editions are still needed.

**Be careful:** this parent synthesis does not complete the deeper individual-paper writing, manufacturing validation, source recovery, or independent review still needed below.

## Subthemes and how to study them

Each link opens the subtheme discussion and its captured paper records. Explanatory depth varies: some papers have expanded individual explanations; others still have only brief discussion or evidence cards. Source locations and unresolved conditions remain visible.

### [Placement routing and floorplanning](../observed-subthemes/placement-routing-and-floorplanning.md)

12 selected records in this theme. Start with [Cell-Structure-Independent Transistor-Level Placement and MOL-Aware Routing Framework Beyond the Standard-Cell Paradigm](../observed-subthemes/placement-routing-and-floorplanning.md).

### [Process aware design](../observed-subthemes/process-aware-design.md)

7 selected records in this theme. Start with [Design Technology Co-Optimization for Network on Chip in High Performance CPUs at 3nm Node Using Monolithic 3D and Backside Interconnect Technologies](../observed-subthemes/process-aware-design.md).

### [Placement routing and timing](../observed-subthemes/placement-routing-and-timing.md)

6 selected records in this theme. Start with [IR-Drop Aware Global Placement with PDN Optimization and GPU-Accelerated Analysis for Mitigating Global and Local IR-Drop](../observed-subthemes/placement-routing-and-timing.md).

### [Manufacturing and yield](../observed-subthemes/manufacturing-and-yield.md)

4 selected records in this theme. Start with [G-Matcher: GPU-Accelerated Multi-Level, Multi-Stage Framework for Large-Scale Layout Pattern Matching](../observed-subthemes/manufacturing-and-yield.md).

### [Manufacturing and lithography](../observed-subthemes/manufacturing-and-lithography.md)

2 selected records in this theme. Start with [N3Litho: A GPU-Native Numerical-Neural Framework for 3D Mask Modeling, 3D Propagation, and 3D Aerial Image Simulation](../observed-subthemes/manufacturing-and-lithography.md).

### [Partitioning and placement](../observed-subthemes/partitioning-and-placement.md)

2 selected records in this theme. Start with [ATOM-3D: Analytical Three-Dimensional Orientation-Aware Mixed-Size Placer](../observed-subthemes/partitioning-and-placement.md).

### [Physical design and routing](../observed-subthemes/physical-design-and-routing.md)

2 selected records in this theme. Start with [LRTA: Routability-Driven 3D-Aware Track Assignment with Layer Reassignment](../observed-subthemes/physical-design-and-routing.md).

### [Timing analysis and optimization](../observed-subthemes/timing-analysis-and-optimization.md)

2 selected records in this theme. Start with [Warp-STAR: High-Performance, Differentiable GPU-Accelerated Static Timing Analysis Through Warp-Oriented Parallel Orchestration](../observed-subthemes/timing-analysis-and-optimization.md).

### [Cell and circuit design](../observed-subthemes/cell-and-circuit-design.md)

1 selected records in this theme. Start with [B-Flex: Exploration of Broader Flip-Flop Design Space Based on FSM Exhaustive Search](../observed-subthemes/cell-and-circuit-design.md).

### [Device and process modeling](../observed-subthemes/device-and-process-modeling.md)

1 selected records in this theme. Start with [A Physics-Prior Intelligent Compact Modeling Framework for BEOL-Compatible DTCO: EKAN-Based Distillation from Neural to Symbolic Models](../observed-subthemes/device-and-process-modeling.md).

### [FPGA and reconfigurable design](../observed-subthemes/fpga-and-reconfigurable-design.md)

1 selected records in this theme. Start with [Dynamic-Cost Area Recovery for Fracturable LUT-Based FPGAs](../observed-subthemes/fpga-and-reconfigurable-design.md).

### [Manufacturing monitoring and yield](../observed-subthemes/manufacturing-monitoring-and-yield.md)

1 selected records in this theme. Start with [STAMP: Semiconductor Tool-Chain Attestation Through Wafer-Level Machine Learning-Based Process Monitoring](../observed-subthemes/manufacturing-monitoring-and-yield.md).

### [Parasitic extraction and modeling](../observed-subthemes/parasitic-extraction-and-modeling.md)

1 selected records in this theme. Start with [Capacitance Extraction via Machine Learning with Application to Interconnect Geometry Exploration](../observed-subthemes/parasitic-extraction-and-modeling.md).

## Representative source-backed records

The following reading set spans the available conferences and uses dated corrections where registered. These corrections improve the current reading view but do not change historical adjudication or establish independent acceptance. Each paper link opens its exact evidence card.

## Paper cards: what changes and where it stops

- [Module-Level Placement Using Force-Based Deformation for Efficient Early Design Estimation](../observed-subthemes/partitioning-and-placement.md#paper-dac-2026-research954) — DAC 2026.
- [ATOM-3D: Analytical Three-Dimensional Orientation-Aware Mixed-Size Placer](../observed-subthemes/partitioning-and-placement.md#paper-dac-2026-research934) — DAC 2026.
- [Disentangled Differentiable Timing-Power Co-Optimization with Quad-Gradient Gate Sizing](../observed-subthemes/placement-routing-and-floorplanning.md#paper-dac-2026-research843) — DAC 2026.
- [Separate: Segmenting Patterns from Defects in Wafer Manufacturing Using Weak Supervision](../observed-subthemes/manufacturing-and-yield.md#paper-dac-2026-research838) — DAC 2026.
- [COPA: A Congestion-Oriented Pin Assignment Framework for Intra-Block Physical Design Optimization](../observed-subthemes/placement-routing-and-timing.md#paper-iccad-2025-1155) — ICCAD 2025.
- [RSizing: Robust Bayesian Optimization for Analog Circuit Sizing Under Process Variations](../observed-subthemes/process-aware-design.md#paper-iccad-2025-1080) — ICCAD 2025.
- [Capacitance Extraction via Machine Learning with Application to Interconnect Geometry Exploration](../observed-subthemes/parasitic-extraction-and-modeling.md#paper-iccad-2025-1142) — ICCAD 2025.
- [Parallel Non-Integer Multiple-Cell-Height Node Remapping](../observed-subthemes/placement-routing-and-timing.md#paper-iccad-2025-1111) — ICCAD 2025.
- [DR. OPC: Differentiable Rasterization for Advanced Optical Proximity Correction](../observed-subthemes/manufacturing-and-lithography.md#paper-dac-2026-research827) — DAC 2026.
- [Unified Rail-Signal Co-Design for Multilayer PCBs: Resource Allocation, IR-Drop, and Routability](../observed-subthemes/physical-design-and-routing.md#paper-dac-2026-research732) — DAC 2026.
- [Mask-Guided Diffusion with Process-Aware Metric Optimization for Long-Tailed Wafer Defect Analysis](../observed-subthemes/manufacturing-and-yield.md#paper-dac-2026-research649) — DAC 2026.
- [Differentiable Fill Insertion with Explicit Delay Optimization](../observed-subthemes/process-aware-design.md#paper-dac-2026-research648) — DAC 2026.

## What the evidence supports

These records identify proposed methods and the conditions recorded for them. A reported improvement should be interpreted with its comparison method, input size, hardware, and result-quality requirement. Missing fields are evidence gaps; a populated field can also state that a detail is unspecified.

## Limits and next evidence

The selected sample is uneven across conferences and source types. It cannot establish how fast a subject is growing. Repeated observations across comparable years, with the same inclusion rules and source depth, are needed for a time trend.

Every linked evidence article preserves the Problem: and Mechanism / artifact: fields, baseline, unshortened limitations, source URL, and recorded location. Primary text and independent review remain necessary where the record says those checks are open.

[Research directions](../directions/README.md) · [All observed subthemes](../expanded-taxonomy-v1.md)
