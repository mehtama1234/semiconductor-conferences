# Physical design and routing

This subject has 2 records in the selected sample. This page explains where it fits, then presents all captured paper evidence without shortening the measurements or limitations.

[Definitions used in the paper records](../reading-guide-v1.md)

## Understand the parent subject first

- [Physical design and manufacturing](../themes/physical-design-and-manufacturing.md)

## The problem: a connection needs physical space

A circuit description says which terminals must connect. A physical design must turn those connections into conductors with actual width, separation, and layer positions. Two unrelated connections cannot occupy the same conductor. A route also has to obey the manufacturing rules that determine where metal and connections between layers can be placed.

Routing therefore concerns more than finding a short path. A short path can occupy space that another connection needs. Moving a route to another layer can relieve crowding but require additional connections between layers, called vias. The resulting layout must still meet electrical requirements. In this article, **routability** means the ability to complete the required connections under the applicable physical rules, not simply to draw approximate paths.

The two captured papers address different physical objects: three-dimensional routing and a multilayer printed circuit board. They share a resource-allocation question, but their manufacturing rules and electrical checks should not be treated as interchangeable. The following explanation develops that common question; it does not reconstruct algorithms absent from the source descriptions.

## LRTA: choosing tracks and layers together

A routing track is a permitted path position on a routing layer. Assigning a connection to a track makes a more concrete space commitment than choosing a broad routing region. If too many connections need the same region, individually convenient assignments can leave later connections without legal paths.

[LRTA](../observed-subthemes/physical-design-and-routing.md#paper-dac-2026-research2037) is described as routability-driven, three-dimensional-aware track assignment with layer reassignment. The specific conceptual contribution supported by the captured description is that a layer choice need not remain fixed while tracks are assigned. Reconsidering layers supplies another way to resolve competing space requirements.

That freedom has costs to check. Changing layers can change route length, the number and placement of vias, and the electrical properties of a connection. These are evaluation concerns, not reported LRTA results. The available description does not identify the search procedure, the exact meaning of its three-dimensional routing model, or the conditions under which reassignment is allowed. It would be premature to assume a particular stacked-chip technology.

A useful comparison would hold the circuits, available layers, manufacturing rules, and starting routing problem fixed. It would report completed connections and remaining rule violations alongside wire length, via count, timing, and runtime. An improvement in a congestion estimate alone would not establish that the final detailed layout can be completed. None of those numerical results is available in the captured official description.

<span id="explanation-dac-2026-research2037"></span>

### LRTA: layer reassignment can resolve a routing conflict only when vias, electrical cost and final legality remain visible

#### What track assignment decides

A routed net needs a path through allowed positions on routing layers. Track assignment chooses those positions before or during detailed routing. It consumes physical capacity: two nets that need the same track segment cannot both use it unless the design provides another legal route or a different layer.

Routability means that all required connections can be completed under the design rules. It is not the same as a low congestion score or a drawing with approximate paths. An assignment that looks balanced can still leave one long net, via transition or spacing rule impossible to satisfy.

#### What layer reassignment changes

LRTA is described as 3D-aware, routability-driven track assignment with layer reassignment. The conceptual change is that a net's layer choice can be revisited as track conflicts appear. Moving a net can free a crowded layer and make another connection possible.

The move also has costs. A layer change can add a via, increase route length, cross a layer with a different direction or width, and change resistance, capacitance, coupling and timing. The method must define when reassignment is allowed, how it prices these costs, and how its output is handed to detailed routing and signoff checks.

#### Why the physical technology must be stated

“3D-aware” does not identify one implementation. A monolithic 3D process, stacked dies and chiplet integration differ in vertical connections, layer rules, alignment, thermal conditions and manufacturing checks. The track capacity, via model, layer direction, spacing, timing corners and connectivity must be explicit before a result can transfer to a technology.

An adequate comparison holds the netlist, stack, layers, tracks, design rules, starting route, timing constraints and detailed-router settings fixed. It reports completed connections, remaining violations, wire length, via count, congestion, timing, power, runtime and DRC results. A final legal route should be checked by the same signoff flow used for the baseline.

The captured DAC description supports routability-driven 3D-aware track assignment with layer reassignment. It reports no benchmark, algorithm details, completed routes, wire/via/timing/runtime values or signoff result. The evidence supports a routing-direction hypothesis, not demonstrated routability, electrical validity or manufacturing feasibility.

[Observed paper card](../observed-subthemes/physical-design-and-routing.md#paper-dac-2026-research2037)

## Rail-signal co-design: power delivery uses routing resources too

A printed circuit board contains conductors for both signals and electrical power. A power rail distributes a supply voltage to components. Its conductors have resistance, so carrying current produces a voltage difference along the supply path. For a fixed resistance, a larger current produces a larger drop; this is the basic relationship expressed by voltage drop equals current multiplied by resistance.

Wider conductors or additional connected metal can reduce resistance, but they also use physical space. Signal connections need their own paths and electrical conditions. Decisions about power and signals are consequently coupled through the board's available layers and geometry.

[Unified Rail-Signal Co-Design for Multilayer PCBs](../observed-subthemes/physical-design-and-routing.md#paper-dac-2026-research732) explicitly connects resource allocation, resistive voltage drop, and routability. Its stated scope supports discussing power and signal decisions together. It does not establish which optimization method is used or demonstrate a measured advantage in the captured record.

A controlled evaluation would specify the layer arrangement, conductor properties, component locations, supply connections, and current demands. It would then compare completed signal routes and supply voltages under the same requirements. A board that routes more signals but supplies an unacceptable voltage is not an acceptable replacement. Conversely, improved power delivery does not excuse incomplete signal connections. Crosstalk, timing, fabrication checks, and tests on a manufactured board remain separate evidence questions; the record reports no results for them.

<span id="explanation-dac-2026-research732"></span>

### Unified rail-signal co-design: a routable board is not acceptable if its supply voltage or signal integrity fails

#### Why power and signals compete

A multilayer PCB uses conductors for signals and for power rails. A rail distributes current to components; its resistance causes a voltage drop along the path. In the simplest case, the drop is current multiplied by resistance. Wider conductors or additional copper can reduce resistance, but those structures consume layers and area that signal routes need.

Signal routes have their own electrical requirements. Layer choice, conductor geometry, dielectric, reference plane, via transitions and neighboring traces affect impedance, delay, return current and crosstalk. A power decision can therefore change signal behavior, and a signal route can change the available power path.

#### What unified allocation must decide

The proposed co-design connects rail allocation, signal routing, IR drop and routability. It must choose where conductors go, which layers and vias they use, how current is distributed, and which signal constraints are preserved. The objective must state voltage limits, timing, crosstalk, impedance, current peaks, thermal conditions and manufacturing rules.

Sequentially routing power and then signals can leave the second stage with no legal space or can produce a supply path that is electrically inadequate. Joint optimization can expose the tradeoff earlier, but it adds coupled constraints and requires an electrical solver or model that captures the relevant geometry and frequency behavior.

#### What the evaluation must measure

Compare unified co-design with sequential power-then-signal design and manual routing on the same board, stackup, materials, component placement, current demand, signal frequencies, layer budget and acceptance criteria. Report completed signal connections, IR-drop distribution and worst case, voltage margins, impedance, crosstalk, timing, vias, layer usage, runtime and violations.

The final board should be checked with an independent electrical signoff flow and fabrication rules. Test current hotspots, simultaneous switching, return-path discontinuities, long routes, dense vias, temperature and component tolerance. A fabricated-board measurement is needed for claims about production behavior.

The captured DAC description supports unified resource allocation for rails, signals, IR drop and routing. It reports no IR-drop, routability, crosstalk, timing, runtime, stackup, current, solver or fabricated-board result. The evidence supports a joint-design direction, not demonstrated electrical or manufacturing improvement.

[Observed paper card](../observed-subthemes/physical-design-and-routing.md#paper-dac-2026-research732)

## What these cases support—and what remains unproven

Both cases identify a reason to reconsider decisions across coupled physical resources: tracks and layers in LRTA, power and signal allocation in the board study. This is a defensible conceptual connection. It is not evidence that one method applies to both domains, that joint optimization always wins, or that this approach has become more common over time.

The source boundary is important: both records currently cite official DAC descriptions, not recovered paper pages, tables, or full experimental sections. They support the named problems and proposed approaches. Page-backed algorithm explanations and quantitative comparisons remain unfinished research work and must not be replaced with invented detail.

## Compare the results carefully

First identify the inputs and required output quality. Then identify the limited resource: time, memory, communication, energy, circuit area, or correctness coverage. Ask which part of the method reduces that cost and which new cost it adds. Compare numbers only when the experiments hold these conditions sufficiently similar.

A conference description may explain the proposal while omitting the full experiment. An author preprint link may have been coded from its abstract. The source classification does not by itself establish that every table was read. Missing locations remain visible below.

## Complete captured evidence

These are evidence records, not substitutes for the explanations above. Each record preserves its problem, proposed method, measurements, comparison conditions, and source limits. A populated record does not establish that its mechanism has been fully explained or independently verified.

<span id="paper-dac-2026-research2037"></span>

### LRTA: Routability-Driven 3D-Aware Track Assignment with Layer Reassignment

DAC 2026 · Record: `dac-2026-research2037`

[Read the step-by-step explanation](#explanation-dac-2026-research2037)

**Updated source-backed reading card**

Reviewed 2026-09-08. Deepens the existing LRTA treatment into a paper-level reading; separates track assignment, layer reassignment, via and electrical costs, and preserves the description-only boundary against assuming a specific 3D technology or signoff result.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Three-dimensional routing must assign nets to track positions and layers while avoiding congestion and preserving the possibility of completing all required connections under physical rules.

**Mechanism / artifact:**

Routability-driven 3D-aware track assignment with layer reassignment; search procedure, reassignment constraints, cost function, 3D technology and detailed-routing handoff are unspecified.

**Workload — the work tested:**

3D interconnect or chiplet layouts; netlist, net classes, layer count, track capacity, congestion, route lengths and benchmark suite are unspecified.

**Hardware and manufacturing assumptions:**

Multi-layer 3D physical-design stack; design rules, via types, layer direction, spacing, connectivity, timing and manufacturing assumptions are unspecified.

**Baseline — the comparison method:**

2D track assignment

Static 3D routing

Stack, netlist, layer, via, timing, congestion and signoff conditions are unspecified

**Reported measurements:**

Routability improvement is claimed qualitatively; no completed-connection count, wire length, congestion, timing, via count, runtime or design-rule-check result is reported.

**Limits on the conclusion:**

A track assignment reserves a concrete position on a routing layer. Reassigning a net to another layer can free a crowded region, but it can add vias, length, resistance, capacitance and timing delay. A lower congestion estimate is not the same as a legal completed route.

The meaning of 3D-aware depends on the stack, layer directions, vertical connections, spacing rules and whether the design is a monolithic 3D, stacked-die or chiplet system. Those technologies have different physical constraints and should not be inferred from the title.

The official description reports no benchmark, algorithm details, completed routes, wire/via/timing/runtime values or signoff DRC result. The record supports a routing-direction hypothesis, not demonstrated routability, electrical validity or manufacturing feasibility.

**Source and location**

Evidence tier: Primary captured official DAC description plus existing chapter level lrta discussion; no full paper extraction, detailed routing reproduction or signoff validation. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH2037)

DAC 2026 official description; captured Problem, Mechanism / artifact, Workload, Hardware, Baseline, Measurements and Limits fields; record RESEARCH2037; no manuscript pages.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** 2D track assignment

static 3D routing

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH2037

**Hardware or process assumptions:** 3D physical-design stack with multiple routing layers; design rules and via assumptions are unspecified.

**Limits:** No wirelength, congestion, timing, via count, runtime, or DRC results are reported.

Benefits depend on stack and routing rules.

Official description only; signoff-flow validation is required.

**Method or artifact:** 3D-aware routability-driven track assignment with layer reassignment.

**Metrics:** Routability improvement is claimed qualitatively

**Problem:** Three-dimensional routing needs track assignment that accounts for routability and layer choices.

**Workload or benchmark:** 3D interconnect or chiplet layouts; technology, nets, and routing baseline are unspecified.

</details>

<span id="paper-dac-2026-research732"></span>

### Unified Rail-Signal Co-Design for Multilayer PCBs: Resource Allocation, IR-Drop, and Routability

DAC 2026 · Record: `dac-2026-research732`

[Read the step-by-step explanation](#explanation-dac-2026-research732)

**Updated source-backed reading card**

Reviewed 2026-09-08. Deepens the existing rail-signal discussion into a paper-level reading; makes the shared PCB resource, IR-drop, signal-integrity, routing and fabrication boundaries explicit while preserving the description-only evidence.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Power-rail and signal-routing choices compete for multilayer PCB space and affect both supply voltage and signal connectivity.

**Mechanism / artifact:**

Unified resource-allocation co-design for rails, signals, IR drop and routing; optimization method, electrical solver, objective weights and repair/signoff loop are unspecified.

**Workload — the work tested:**

Multilayer PCB layouts with signal nets, power rails and current demands; stackup, materials, component locations, currents, frequencies and tools are unspecified.

**Hardware and manufacturing assumptions:**

PCB fabrication and electrical-signoff flow; layer count, conductor geometry, dielectric, via, return-path, thermal and manufacturing assumptions are unspecified.

**Baseline — the comparison method:**

Sequential power then signal design

Manual PCB routing

Stackup, current distribution, timing, crosstalk, electrical and fabrication conditions are unspecified

**Reported measurements:**

PCB co-design quality is claimed qualitatively; no IR-drop, routability, crosstalk, timing, runtime, power-integrity or fabricated-board result is reported.

**Limits on the conclusion:**

A power rail has resistance, so current creates voltage drop along the supply path. Lower resistance can require wider conductors or more copper, which consumes routing space. Signal routes share layers, vias and return-path constraints; changing them can alter impedance, coupling, crosstalk and timing.

A board that routes more signals can still fail if a component receives an unacceptable supply voltage or if signal integrity fails. The useful co-design objective must define current distribution, voltage limits, signal timing, crosstalk, layer/material rules and whether peak or average conditions are evaluated.

The official description reports no IR-drop, routability, crosstalk, timing, runtime, stackup, current, solver or fabricated-board result. The record supports joint resource allocation as a design direction, not demonstrated electrical or manufacturing improvement.

**Source and location**

Evidence tier: Primary captured official DAC description plus existing chapter level rail signal discussion; no full paper extraction, electrical signoff reproduction or fabricated board validation. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH732)

DAC 2026 official description; captured Problem, Mechanism / artifact, Workload, Hardware, Baseline, Measurements and Limits fields; record RESEARCH732; no manuscript pages.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** sequential power then signal design

manual PCB routing

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH732

**Hardware or process assumptions:** PCB fabrication and electrical-signoff flow; layer and material assumptions are unspecified.

**Limits:** No IR-drop, routability, crosstalk, timing, runtime, or fabricated-board results are reported.

Results depend on stackup and current distribution.

Official description only; electrical and fabrication validation is required.

**Method or artifact:** Unified resource-allocation co-design for rails, signals, IR drop, and routing.

**Metrics:** PCB co-design quality is claimed qualitatively

**Problem:** Power-rail and signal-routing decisions interact in multilayer PCB design.

**Workload or benchmark:** Multilayer PCB layouts; stackups, nets, currents, and tools are unspecified.

</details>

## What remains to establish

Resolve unspecified workloads, comparison methods, resource budgets, and source locations before generalizing a reported gain. Multiple papers in this selected sample permit comparison of mechanisms, but do not by themselves establish recurrence across years or a long-term trend.

[All subthemes](../expanded-taxonomy-v1.md) · [Research directions](../directions/README.md)
