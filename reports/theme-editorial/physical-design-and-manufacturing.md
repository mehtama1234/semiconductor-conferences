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

The full flow also includes failed candidates and repair. An optimizer that takes ten minutes but needs ninety minutes of cleanup is not a ten-minute path to an accepted layout. Fixing geometry can change electrical behavior, and fixing electrical behavior can need new geometry. Done means the chosen result meets every applicable requirement together, under stated conditions.

## Long-term hypotheses and disconfirming evidence

Three readings are worth testing; each names what would weaken it.

| Hypothesis | Test | What would weaken it |
| --- | --- | --- |
| Considering placement, wiring, timing and supply demand together, early, reduces later repair | Compare with step-by-step optimization, using the same final checks and total budget | Early models are inaccurate enough to cause extra rework, or staged methods do as well more cheaply |
| Faster estimation helps most when paired with decision-aware validation | Measure ranking changes, false feasibility calls and final accepted outputs, not just average error | The cheap model cannot safely filter candidates, or exact fallback eats the saving |
| Manufacturing learning needs evidence across the design-to-production boundary | Do predicted or detected patterns match verified physical or electrical effects, under independent conditions? | Gains stay inside simulation or image scores, without the claimed production outcome |

These are bounded interpretations, not established ISCA–DAC–ICCAD time trends. Comparable processes, rule sets, circuits, operating assumptions, tool budgets, source depth and editions are still needed.

**Be careful:** this parent synthesis does not complete the deeper individual-paper writing, manufacturing validation, source recovery, or independent review still needed below.
