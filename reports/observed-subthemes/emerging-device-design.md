# Emerging device design

This subject has 2 records in the selected sample. This page explains where it fits, then presents all captured paper evidence without shortening the measurements or limitations.

[Definitions used in the paper records](../reading-guide-v1.md)

## Understand the parent subject first

- [Analog mixed signal and emerging devices](../themes/analog-mixed-signal-and-emerging-devices.md)

## The device changes what a design tool must preserve

The two papers in this group concern superconducting logic, not a general survey of emerging devices. One changes circuit structure and cell interfaces; the other changes physical placement. Their shared problem is that a correct Boolean expression is only part of a usable implementation. Signals must also arrive in the right relationship, reach their intended loads, and fit within physical constraints.

Single-flux-quantum logic uses electrical pulses associated with individual magnetic flux quanta. Its circuits use Josephson junctions, superconducting elements separated by a weak link. A junction count measures one important resource, but it is not the same as layout area, energy per result, or total equipment cost. Wiring, interfaces, biasing, and cooling can matter as well.

The logic family matters. Rules for synchronizing gates in rapid single-flux-quantum logic should not be silently applied to every superconducting architecture. Conversely, removing explicit gate-level clocking does not remove the need to preserve valid signal ordering and representation.

## Retiming and interfaces: minimize the circuit actually implemented

Retiming moves storage boundaries across logic while preserving the required sequence behavior under the transformation's conditions. It can change which signals need stored copies and how much logic lies between boundaries. If the representation needs separate paths for a value and its complement, counting only the unencoded logic can miss duplication costs.

[Duplication-Aware Retiming and Cell Interface Redesign](../observed-subthemes/emerging-device-design.md#paper-dac-2026-research520) co-optimizes register positions and signal polarity to reduce Josephson junction count. Its official description also targets interconnect drivers, receivers, and fanout elements with a new amplifier integrated into a characterized cell library. Fanout is the distribution of one signal to several destinations; the required supporting circuitry is not necessarily negligible.

The description reports 63–71% fewer junctions for single-cycle implementations and 41–66% fewer for multi-cycle implementations against prior work. It claims experimental verification of the amplifier but does not expose the experiment, technology conditions, or per-design comparisons. The two ranges concern different implementation classes and must remain separate. They do not establish equivalent percentages of energy or area savings. [Official retiming and interface description](https://63dac.conference-program.com/presentation/?id=RESEARCH520&sess=sess172).

A multi-cycle design can shorten its most restrictive within-cycle path while taking more cycles to produce a result. To compare it with a single-cycle design, report both cycle duration and cycles per result, plus how often new inputs can be accepted. Otherwise, a shorter critical path can be mistaken for lower end-to-end latency.

The preservation check should cover sequential behavior, initial state assumptions, signal encoding, and interface timing. A junction-count improvement is useful only after those conditions are met. The recovered description does not supply that complete validation.

<span id="explanation-dac-2026-research520"></span>

## Duplication-aware superconducting retiming: fewer junctions help only when timing and interfaces remain equivalent

Superconductor logic uses pulses and specialized cells whose cost is not captured by Boolean gate count alone. In logic families that rely on dual-rail representation, a value and its complement can require duplicated logic. Interconnect drivers, receivers and fanout elements add further Josephson junctions at cell boundaries. Retiming moves storage boundaries across logic; polarity assignment determines which rail and duplicated paths are needed. The useful objective is therefore the implemented circuit under its sequential, pulse-timing and interface contract.

The described method co-optimizes register placement and signal polarity to minimize Josephson-junction count, then redesigns an amplifier for interconnect drivers, receivers and fanout inside existing SFQ cells. The amplifier is described as experimentally verified and characterized into a new cell library. These are two coupled changes: retiming alters stage boundaries and duplication, while the cell interface changes the cost of connecting stages. The captured description does not specify the logic-family timing model, dual-rail encoding, retiming legality, amplifier parameters, library characterization, fabrication status or process corners.

The first gate is sequential and pulse correctness. Prove equivalence under initial state, reset, feedback, dual-rail polarity, pulse ordering, cycle boundaries and environment assumptions. Check pulse integrity, setup/hold or SFQ timing, hazards, fanout loading, interconnect delay and interface behavior. A lower JJ count is not useful if the transformation changes the function, loses a pulse, violates a timing contract or changes the input acceptance rate.

Single-cycle and multi-cycle results need separate throughput accounting. Report absolute JJ count, cycle duration, cycles per result, initiation interval, latency, throughput, buffering and critical path. State whether the Pareto comparison holds the Boolean/sequential function, encoding, throughput target, fanout, timing model, technology and cell library constant. A multi-cycle circuit can have a shorter critical path while taking more cycles per result; those are different benefits.

The amplifier and cell library require process-calibrated validation across bias, temperature, device variation, load, fanout, pulse amplitude/width, wiring and yield. Include drivers, receivers, fanout, bias and clock circuitry, interconnect, library characterization and cryogenic infrastructure in the declared area and energy boundary. Compare standard retiming and fixed interfaces at the same function, timing, process, library and measurement boundary.

The official description reports 63–71% fewer JJ counts for single-cycle implementations and 41–66% fewer for multi-cycle implementations versus prior state of the art, and claims the multi-cycle designs form a Pareto frontier with shorter critical paths and lower JJ counts than the best single-cycle implementations. It does not expose absolute counts, cycle/throughput results, area, energy, process conditions, yield or per-design comparisons. The evidence supports duplication-aware superconducting retiming and interface co-design, not demonstrated portable process yield, energy reduction or complete cryogenic-system benefit.

<span id="explanation-dac-2026-research875"></span>

## JSPlace: control shape without losing timing-related structure

A placement can have small area yet be too wide or too tall for the surrounding design. Aspect ratio is width divided by height. Controlling it adds a requirement beyond minimizing the total length of connections. Moving elements to improve shape may lengthen some connections or alter the available paths for clocks and data.

[JSPlace](../observed-subthemes/emerging-device-design.md#paper-dac-2026-research875) addresses RSFQ placement organized by logic stages. Its official description folds the staged placement into three segments, merges columns using mixed-integer linear programming, chooses vertical node positions with dynamic programming, and then adjusts positions using connectivity to reduce vertical wire length. The first optimization includes discrete choices; the second solves a structured sequence of subproblems. These algorithm labels do not establish global optimality for the entire layout.

The description names ISCAS85 and EPFL benchmarks and reports improved layout area and wire length with aspect-ratio control. It supplies no numerical gains, target ratios, routing results, or pulse-timing margins. The title's length-matching objective must therefore not become a claim that every final routed path meets a verified timing requirement. [Official JSPlace description](https://63dac.conference-program.com/presentation/?id=RESEARCH875&sess=sess169).

Equal geometric length alone does not prove equal electrical delay if routes differ in their structures or loads. A useful final check includes the actual routes and interface elements under the intended technology model. It should also identify any extra wiring needed after placement to satisfy timing or length requirements.

JSPlace's first gate is physical and pulse validity. Define the RSFQ stage graph, clock period, target aspect ratio, length-matching set and tolerance, then check the actual routed interconnect for pulse delay, skew, synchronization, fanout loading, crossings, vias, bias/clock effects and signal integrity across process and operating corners. A compact placement can still fail if legalization or routing changes the path lengths, or if equal geometric length does not imply equal electrical delay.

Its optimization boundary also needs to be explicit. Report the three-segment folding rule, MILP variables and optimality gap, dynamic-programming state, connectivity-repositioning objective, solver time, failed candidates and post-placement repair. Compare generic and length-oblivious placement at the same cell library, stage/clock constraints, target shape, routing flow and final timing evaluator. Include legalization, routing, timing analysis and any infeasible placement in runtime; proposal time alone is not a physical-design speedup.

The official evidence supports shape-controlled RSFQ placement on ISCAS85 and EPFL, with qualitative area and wirelength improvement. It does not expose numerical gains, absolute aspect ratios, pulse timing, routability, runtime, process conditions, yield or fabrication. The evidence supports a shape-and-length-aware placement direction, not demonstrated clock-safe routed layouts, process portability or manufacturing benefit.

## How the two approaches could interact

Cell redesign changes the sizes and interface costs that a placer sees. Retiming changes stage boundaries and connections. Placement then changes physical distances and may reveal additional interface requirements. These dependencies explain why independently good local results need a complete-flow comparison.

That interaction is an inference about design methodology, not an assertion that these papers were evaluated together. Their logic-family and timing assumptions must first be reconciled. Combining one paper's percentage improvement with another's qualitative layout result would not establish a realizable joint benefit.

An end-to-end comparison should use the same required computation, input/output timing, technology, and physical constraints. Report functional correctness, latency, input acceptance rate, junction count, routed area, and energy at clearly stated boundaries. Cryogenic operating conditions belong in the system assessment; circuit-level savings alone cannot determine facility-level energy.

## Evidence boundary

The official descriptions were refreshed on 2026-09-07. They explain substantially more mechanism than the earlier cards below, but neither full manuscript was recovered in this pass. The amplifier's verification conditions and JSPlace's final timing results remain missing. Related JPlace or J2Place publications are different works and cannot fill these gaps without explicit source reconciliation. These two cases support a technical connection, not a measured long-term adoption trend.

## Compare the results carefully

First identify the inputs and required output quality. Then identify the limited resource: time, memory, communication, energy, circuit area, or correctness coverage. Ask which part of the method reduces that cost and which new cost it adds. Compare numbers only when the experiments hold these conditions sufficiently similar.

A conference description may explain the proposal while omitting the full experiment. An author preprint link may have been coded from its abstract. The source classification does not by itself establish that every table was read. Missing locations remain visible below.

## Complete captured evidence

These are evidence records, not substitutes for the explanations above. Each record preserves its problem, proposed method, measurements, comparison conditions, and source limits. A populated record does not establish that its mechanism has been fully explained or independently verified.

<span id="paper-dac-2026-research520"></span>

### Duplication-Aware Retiming and Cell Interface Redesign for Superconductor Circuit Minimization

DAC 2026 · Record: `dac-2026-research520`

[Read the step-by-step explanation](#explanation-dac-2026-research520)

**Updated source-backed reading card**

Reviewed 2026-09-09. Deepens the duplication-aware superconducting retiming treatment into a paper-level reading; separates dual-rail duplication-aware register/polarity co-optimization and JJ cell-interface amplifier redesign from sequential equivalence, timing/throughput, interface/fanout accounting, process calibration and cryogenic-system conclusions, while preserving the single-cycle and multi-cycle JJ-count ranges.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Superconductor logic families can rely on dual-rail representations that duplicate gates, while interconnect drivers, receivers and fanout elements add substantial Josephson-junction cost; retiming and cell interfaces must be optimized together without changing sequential behavior or timing.

**Mechanism / artifact:**

Duplication-aware retiming co-optimizes register placement and polarity assignment to minimize Josephson-junction count, and a redesigned amplifier targets interconnect-driver/receiver/fanout overhead inside existing SFQ cells; the amplifier is experimentally verified and used to characterize a new SFQ cell library. Logic-family assumptions, retiming constraints, dual-rail encoding, amplifier circuit/parameters, library characterization, timing model and fabrication status are unspecified.

**Workload — the work tested:**

Superconducting logic circuits in single-cycle and multi-cycle implementations, with monotonic-circuit applicability claimed beyond SFQ; circuit suite, pipeline/latency constraints, input acceptance rate, dual-rail policy, fanout distribution, cell library, process, critical-path definition and comparison designs are unspecified.

**Hardware and manufacturing assumptions:**

Josephson-junction superconducting logic and SFQ cells with specialized drivers, receivers, fanout elements and a new amplifier; JJ technology/process, biasing, clocking or pulse timing, temperature/cryogenic environment, wiring, parasitics, fabrication yield, measurement equipment and energy boundary are unspecified.

**Baseline — the comparison method:**

Prior state-of-the-art single-cycle implementation

Prior state-of-the-art multi-cycle implementation

Standard retiming

Fixed cell interfaces

Same Boolean/sequential function, encoding, cycle/throughput contract, technology/library, timing constraints, fanout, bias/clock assumptions and junction-count boundary are unspecified

**Reported measurements:**

The official description reports 63–71% JJ-count reduction for single-cycle implementations and 41–66% reduction for multi-cycle implementations versus prior state of the art, with the multi-cycle designs claimed to form a Pareto frontier of shorter critical paths and lower JJ counts than best-to-date single-cycle implementations; it does not report absolute JJ count, cycle time, cycles/result, throughput, area, energy, yield, process conditions or per-design results.

**Limits on the conclusion:**

Retiming must preserve sequential behavior, initial-state assumptions, dual-rail polarity, pulse/order semantics, reset, feedback and interface timing. Prove equivalence and check pulse integrity, setup/hold or SFQ timing, hazards, fanout loading and cycle boundaries; a lower JJ count is not useful if the transformed circuit changes the computation or input acceptance contract.

Single-cycle and multi-cycle results are not directly interchangeable. Report cycle duration, cycles per result, initiation interval, latency, throughput and buffering, in addition to JJ count and critical path. State whether the claimed Pareto comparison uses the same function, throughput target, timing model, fanout and cell/interface assumptions; a shorter critical path may require more cycles.

The amplifier and cell-library result needs process-calibrated characterization across bias, temperature, variation, load, fanout, pulse amplitude/width, wiring and yield. Include driver/receiver/fanout, bias, clock, interconnect, library characterization and cryogenic infrastructure in area and energy boundaries. The evidence supports duplication-aware superconducting retiming and interface co-design, not demonstrated portable process yield, energy reduction or complete cryogenic-system benefit.

**Source and location**

Evidence tier: Primary captured official DAC description plus existing authored superconducting logic discussion; no full paper extraction, independent sequential/timing validation, reproduced cell library characterization or fabricated process/yield study. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH520&sess=sess172)

DAC 2026 official description; existing emerging-device-design chapter framing; captured Problem, Mechanism / artifact, Workload, Hardware, Baseline, Measurements and Limits fields; no manuscript pages, retiming equivalence trace, amplifier characterization table or process/yield validation.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** standard retiming

fixed cell interfaces

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH520

**Hardware or process assumptions:** Superconducting logic process with specialized cells and timing; fabrication assumptions are unspecified.

**Limits:** No area, latency, energy, junction count, yield, or process results are reported.

Specialized-device assumptions may not transfer.

Official description only; technology-calibrated validation is required.

**Method or artifact:** Retiming and cell-interface co-optimization for superconducting circuit minimization.

**Metrics:** Circuit minimization is claimed qualitatively

**Problem:** Superconductor circuits have costly timing and cell constraints that make duplication and interface overhead important.

**Workload or benchmark:** Superconductor logic circuits; technology, timing, and baselines are unspecified.

</details>

<span id="paper-dac-2026-research875"></span>

### Jsplace: A Shape-Controllable and Length-Matching Placement for Rapid Single-Flux-Quantum Circuits

DAC 2026 · Record: `dac-2026-research875`

[Read the step-by-step explanation](#explanation-dac-2026-research875)

**Updated source-backed reading card**

Reviewed 2026-09-09. Deepens the JSPlace treatment into a paper-level reading; separates RSFQ stage folding, MILP column merging, dynamic-programming vertical placement and connectivity refinement from pulse timing, routed-length validity, aspect-ratio feasibility, process constraints and fabrication conclusions, while preserving the qualitative ISCAS85/EPFL area and wirelength claims.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Clock-driven RSFQ gate-level pipelines can produce layouts whose width grows with logic stages while height is set by the tallest column, creating an undesirable aspect ratio and long or poorly matched interconnects.

**Mechanism / artifact:**

JSPlace folds multi-stage RSFQ placement into three segments, merges columns with mixed-integer linear programming to target a width-to-height ratio, uses dynamic programming for vertical node positions, and applies connectivity-driven repositioning to reduce vertical wirelength; timing model, length-matching tolerance, routing, legality repair and objective weights are unspecified.

**Workload — the work tested:**

RSFQ circuits from ISCAS85 and EPFL benchmarks with staged/pipelined logic; circuit sizes, stage counts, clock period, target aspect ratios, wire-length definition, benchmark preprocessing, placement constraints, train/test or held-out split and baseline tuning are unspecified.

**Hardware and manufacturing assumptions:**

Superconducting Rapid Single Flux Quantum physical-design flow with Josephson-junction cells and clocked pulse interconnects; fabrication process, cell library, wiring layers, vias, bias/clock network, parasitics, pulse model, routing tool, cryogenic operating conditions and measurement boundary are unspecified.

**Baseline — the comparison method:**

State-of-the-art RSFQ placement algorithms

Generic placement without length matching

Length-oblivious stage-column placement

Same circuit netlist, stage/clock constraints, cell library, target aspect ratio, routing/length definition, post-placement legalization and final timing/physical-validation flow are unspecified

**Reported measurements:**

The official description reports effective control of layout width-to-height ratio and qualitative outperformance in layout area and wirelength on ISCAS85 and EPFL benchmarks; it reports no numerical area/wirelength improvement, absolute aspect ratio, pulse timing, delay, routability, runtime, junction count, energy, yield or per-circuit result.

**Limits on the conclusion:**

Geometric length matching is not electrical timing matching. Define which wires must match, tolerance and reference path, then route the actual SFQ interconnect and check pulse delay, skew, setup/hold or synchronization, fanout loading, crossings, vias, bias/clock effects and signal integrity across the intended process corners. A low total wirelength or target aspect ratio can still violate a pulse-timing contract.

The staged folding, MILP and dynamic-programming subproblems need a reproducible feasibility boundary. Expose segment construction, column-merge variables, aspect-ratio constraints, length objective, dynamic-programming state, connectivity refinement, solver time/optimality gap and any repair. Compare valid final layouts at matched constraints and include legalization, routing, timing analysis and failed candidates in runtime.

ISCAS85 and EPFL are benchmark families, not evidence of fabricated RSFQ behavior. Hold out circuit sizes and stage patterns, report per-circuit area, wirelength, aspect ratio, routability, timing margin and runtime, and validate with a technology-calibrated cell/library and pulse model. The evidence supports shape-controlled RSFQ placement, not demonstrated clock-safe routed layouts, process portability, fabrication yield or complete superconducting-system benefit.

**Source and location**

Evidence tier: Primary captured official DAC description plus existing authored superconducting placement discussion; no full paper extraction, reproduced milp/dp run, pulse timing validation or fabrication/process study. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH875&sess=sess169)

DAC 2026 official description; existing emerging-device-design chapter framing; captured Problem, Mechanism / artifact, Workload, Hardware, Baseline, Measurements and Limits fields; no manuscript pages, placement table, routed timing trace or technology-calibrated validation.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** generic placement

length-oblivious SFQ placement

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH875

**Hardware or process assumptions:** Superconducting/SFQ physical-design flow with pulse-timing constraints; process assumptions are unspecified.

**Limits:** No timing, area, wiring, yield, runtime, or fabrication results are reported.

Matching constraints may reduce placement flexibility.

Official description only; technology-calibrated validation is required.

**Method or artifact:** Shape-controllable, length-matching SFQ placement.

**Metrics:** SFQ placement quality is claimed qualitatively

**Problem:** SFQ layouts need shape and length matching to preserve pulse timing and manufacturability.

**Workload or benchmark:** Single-flux-quantum circuit layouts; technology, constraints, and baselines are unspecified.

</details>

## What remains to establish

Resolve unspecified workloads, comparison methods, resource budgets, and source locations before generalizing a reported gain. Multiple papers in this selected sample permit comparison of mechanisms, but do not by themselves establish recurrence across years or a long-term trend.

[All subthemes](../expanded-taxonomy-v1.md) · [Research directions](../directions/README.md)
