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
