# Physical design and manufacturing

This article explains the subject and then connects it to 42 papers in the selected research sample.

A subtheme groups related technical problems. A mechanism describes the particular change proposed by a paper. The discussion below explains the subject; the linked paper records state the available evidence.

[Definitions used in the paper records](../reading-guide-v1.md)

## From circuit connections to geometry

A circuit description identifies components and their connections. Manufacturing requires actual shapes in specified material layers. Placement chooses component locations. Routing chooses wire paths and layers. Wires occupy space, resist current, and store electric charge. Their length and surroundings affect how quickly a signal changes, so a correct logical connection can still arrive too late.

## Why the decisions interact

Moving two communicating components closer can shorten a wire but make another region crowded. Adding a buffer can improve signal timing while increasing area and power. Manufacturing rules restrict widths, spacing, and overlaps. Changes in fabrication can also change transistor or wire behavior. An optimizer must satisfy these conditions together, rather than improving one score while silently violating another.

## What separates the subthemes

Placement and routing methods construct geometry. Timing analysis estimates whether signal transitions meet required times. Process models estimate how fabricated devices behave. Manufacturing and yield methods study defects and variation; yield means the fraction of manufactured devices that meet requirements. A faster estimator and a better final layout are different contributions and need different evidence.

## A comparison that answers the question

Use the same circuit set, manufacturing rules, timing requirements, and implementation tools. Record violations as well as successful outputs. Check the selected designs with a sufficiently accurate final evaluation and include all search time. If a method uses a cheaper approximation, measure whether its errors change which design is selected.

## Follow a logical connection into a physical implementation

A logical circuit specifies which outputs depend on which inputs. A physical implementation assigns dimensions and locations to transistors, cells, wires, and connections between material layers. The logical statement that two terminals are connected does not specify the resistance, capacitance, or travel time of the implemented connection.

Consider two placed cells connected by a wire. Moving them closer can reduce one connection's length. But each cell may also connect to other cells, and the shorter route may pass through a region already occupied by other wires. The task is not to minimize one distance independently. It is to construct a legal geometry that implements the required circuit and meets timing, power, and other stated limits.

The examples below are teaching constructions, not measurements from the linked papers. The current physical-design branches largely retain incomplete source conditions. A connected explanation of their mechanisms does not substitute for missing manuscripts or final implementation results.

## Placement creates demand; routing must find space for it

Placement assigns locations to components. Routing assigns actual wire paths and layers, including connections between layers. An early placement objective may estimate wire length using a simplified distance. Final routing may require detours around obstacles or congested areas, making that estimate optimistic.

Imagine a corridor with room for eight parallel tracks while ten connections need to cross it under a simplified one-track-per-connection model. At least two cannot use that corridor simultaneously as assigned. They need another route, another layer if available, or a placement change. A low average wire length does not remove this local capacity violation.

Adding layers or changing spacing is not automatically available: the technology and design rules constrain both. A route that looks short in a drawing can violate minimum spacing, width, enclosure, or permitted layer-transition rules. The final result must satisfy the applicable rule set, not merely the optimizer's simplified geometry.

The [placement and routing chapter](../observed-subthemes/placement-routing-and-floorplanning.md) and [routing chapter](../observed-subthemes/physical-design-and-routing.md) organize proposals addressing these decisions. Their labels identify the stage being changed. They do not establish final routability or manufacturing acceptance for every proposed placement.

## Timing depends on both data and clock arrival

A synchronous circuit stores values at clock events. For a simplified maximum-delay check, data must arrive early enough before the receiving clock event. Slack is the allowed arrival time minus the actual or estimated arrival time. A requirement of 100 picoseconds and arrival of 103 gives slack of −3 picoseconds, a violation under this simplified setup.

Clock signals also travel through real wires and buffers. Their arrival times differ between locations. That difference changes the time available for data to travel between storage elements. A change helping one maximum-delay condition can affect a minimum-delay condition, so improving a single path is not equivalent to complete timing closure.

The [DCTS discussion](../observed-subthemes/placement-routing-and-timing.md#the-clock-also-has-to-arrive-on-time) connects clock topology and buffer sizing. The available record still lacks complete final wiring and comparison conditions. The [manuscript-backed timing-reuse explanation](../observed-subthemes/compiler-and-runtime-optimization.md#explanation-dac-2026-research2566), in the tooling theme, further shows why arrival estimates must retain electrical context and error direction. A faster timing calculation and a faster implemented circuit are different contributions.

## Cell sizing moves costs between connected components

A stronger driver may charge a given load more quickly. It can also occupy more area, consume more energy, and present a larger input load to its own predecessor. Replacing a small cell with a larger one therefore changes more than that cell's isolated delay.

In an illustrative chain, suppose strengthening the second cell reduces its delay by four time units but increases the first cell's delay by three because of added load. The chain saves one unit, not four. If placement displacement adds two more units of wiring delay, the total becomes one unit worse. These numbers explain the dependency; they are not a device model or a measured paper result.

[HyPAS's recorded method](../observed-subthemes/placement-routing-and-timing.md#paper-dac-2026-research1317) motivates considering placement and sizing together. Its current evidence does not establish complete prediction error, repair cost, or final gain. Joint optimization enlarges the set of decisions, but it also makes attribution harder: an evaluation needs to distinguish the combined result from each component's contribution.

## Power delivery changes the conditions used for timing

The supply network has electrical resistance. In a simple resistive model, a current of 0.1 ampere through 0.2 ohm produces a voltage drop of 0.02 volt. A nominal 0.8-volt source then supplies 0.78 volt after that element, ignoring other effects. Real networks distribute current over many paths and change with switching activity; this calculation is only a basic illustration.

Placing many simultaneously active cells in one area can concentrate demand. Enlarging drivers to improve timing can increase that demand. If delay analysis assumes a supply condition the network cannot provide, the apparent timing improvement may not survive the actual operating case.

The [IR-drop-aware placement record](../observed-subthemes/placement-routing-and-timing.md#paper-dac-2026-research2297) links placement, supply-network changes, and voltage analysis. The current description does not establish all activity assumptions or final power-integrity checks. A useful comparison states which switching patterns and operating conditions were tested and which remain outside the model.

## Extraction connects geometry back to electrical analysis

Extraction estimates electrical properties associated with the physical geometry, such as wire resistance and capacitance. These properties influence signal delay, coupling, and energy. Two geometries with the same logical connectivity need not have the same extracted behavior.

A fast learned or simplified extractor can help evaluate more candidates. Its error should be judged where it changes decisions: selecting a different route, accepting an apparently valid path, or missing an interaction. Small average error does not establish that the critical region is sufficiently accurate.

This links physical design to the [AI-assisted EDA theme](ai-assisted-eda.md) and [tooling theme](design-methodology-and-tooling.md). Prediction, search, and final checking need compatible definitions. A design selected using a cheap model still needs the appropriate higher-confidence evaluation; otherwise the process can preferentially select the model's optimistic mistakes.

## Manufacturing checks and yield answer different questions

A design-rule check determines whether geometry satisfies specified rules. Pattern matching searches for arrangements represented by its query definitions. Lithography simulation estimates aspects of how a pattern transfers through the modeled process. Inspection looks for observable deviations in manufactured material. Functional testing evaluates specified behavior of produced devices. These stages are related, but none alone establishes every later outcome.

[G-Matcher's explanation](../observed-subthemes/manufacturing-and-yield.md#searching-for-known-problematic-geometry) separates faster pattern search from evidence that unknown patterns are safe. The [clip-wise optimization discussion](../observed-subthemes/manufacturing-and-yield.md#scheduling-the-computation-that-produces-a-mask) distinguishes allocating computation among regions from increasing simulator accuracy. Improvements within separate regions must also survive their boundaries when assembled.

Yield is the fraction of manufactured devices meeting the specified acceptance requirements. A higher inspection-classifier score is not automatically higher yield. A subsequent process or design change needs evidence that more acceptable devices result, under comparable production conditions.

Rare defects also change the meaning of a classifier result. Imagine 100 defective items among 10,000 inspected items. Finding 90 defects gives 90% recall. If 99 good items are falsely flagged, only 90 of 189 flags concern real defects, about 47.6% precision. A high defect-detection rate can therefore coexist with a substantial investigation burden. These are illustrative counts, not results for a captured inspection paper.

The [inspection discussion](../observed-subthemes/manufacturing-and-yield.md#rare-defects-and-incomplete-labels) retains the difference between synthetic training examples and real evaluation defects, and between incomplete labels and established ground truth. Test splits need to reflect transfer across wafers, periods, or conditions rather than only nearby images from the same source.

## What a complete physical result must preserve

| Claimed improvement | Necessary companion evidence |
| --- | --- |
| Shorter estimated wires | Legal detailed routes, congestion, and extracted effects |
| Faster critical paths | Other timing checks, clock assumptions, area, and power |
| Lower predicted voltage drop | Activity assumptions and final supply-network conditions |
| Faster physical estimation | Decision-relevant errors and validation of selected candidates |
| Better inspection scores | Real defect ground truth, false alarms, and separate yield evidence |

The total flow also includes unsuccessful candidates and repair. An optimizer taking ten minutes but requiring ninety minutes of cleanup is not a ten-minute path to an accepted layout. Fixing geometry can alter electrical behavior, and improving electrical behavior can require new geometry. Completion means the selected result meets all applicable requirements together under stated conditions.

## Long-term hypotheses and disconfirming evidence

One hypothesis is that earlier joint consideration of placement, wiring, timing, and supply demand reduces downstream repair. Compare it with staged optimization using the same final checks and total budget. It weakens when early models are inaccurate enough to cause additional rework or when staged methods reach equally good results more cheaply.

A second hypothesis is that faster estimation is most useful when paired with decision-aware validation. Test ranking changes, false feasibility decisions, and final accepted outputs, not only average numerical error. It weakens if the cheap model cannot safely filter candidates or exact fallback consumes the expected saving.

A third hypothesis is that manufacturing learning requires evidence across the design-to-production boundary. Test whether predicted or detected patterns correspond to verified physical or electrical consequences under independent conditions. It weakens as an established capability when gains remain confined to simulation or image scores without the claimed production outcome.

These are bounded interpretations, not established ISCA–DAC–ICCAD time trends. Comparable processes, rule sets, circuits, operating assumptions, tool budgets, source depth, and editions remain necessary. This parent synthesis does not complete the deeper individual-paper writing, manufacturing validation, source recovery, or independent review still needed below.

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
