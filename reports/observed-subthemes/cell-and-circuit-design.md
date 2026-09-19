# Cell and circuit design

This subject has 2 records in the selected sample. This page explains where it fits, then presents all captured paper evidence without shortening the measurements or limitations.

[Definitions used in the paper records](../reading-guide-v1.md)

## Understand the parent subject first

- [Design methodology and tooling](../themes/design-methodology-and-tooling.md)
- [Physical design and manufacturing](../themes/physical-design-and-manufacturing.md)

## A cell's logical behavior does not uniquely determine its implementation

A standard-cell library supplies small circuit implementations used to build larger designs. Cells must provide the intended function, but alternatives with that function can differ in area, delay, power, and physical compatibility. Designing additional cells is useful when those alternatives help complete designs meet their requirements.

The two selected records propose different search approaches. B-Flex explores flip-flop designs using finite-state models. Celle extends libraries using equality saturation. Neither captured official description supplies numerical power, performance, or area results, and neither establishes a fabricated implementation.

## B-Flex: search over stateful behavior

A flip-flop stores a value and updates it according to its input and clock behavior. Unlike purely combinational logic, its output depends on retained state. A finite-state machine describes a finite set of states and rules for moving between them in response to inputs.

[B-Flex](../observed-subthemes/cell-and-circuit-design.md#paper-dac-2026-research2394) uses exhaustive finite-state-machine search to explore a broader flip-flop design space. This can make alternatives explicit rather than starting from only a few familiar implementations. The source does not specify the state encoding, candidate-generation rules, admissible transitions, or physical realization procedure.

“Exhaustive” is meaningful only relative to the defined search space. Examining every candidate in one bounded representation does not establish examination of every possible transistor circuit. It also does not establish global physical optimality unless the representation and cost model support that stronger claim.

A useful evaluation would state which behaviors and implementations the search includes, how invalid candidates are rejected, and how the resulting circuits are characterized. Logical state-transition correctness does not alone determine electrical timing, power, or robustness under operating variation. Those properties require additional analysis.

The captured record provides no search size, runtime, area, delay, power, or technology results. It therefore supports the proposed exploration strategy, not an established improvement over a conventional flip-flop library.

<span id="explanation-dac-2026-research2394"></span>

### B-Flex: exhaustive FSM search widens the sequential design space only within its declared representation

#### What a flip-flop must implement

A flip-flop stores state and changes that state in response to a clock, inputs, reset and enable conditions. Its functional behavior can be described as a finite-state machine: a finite set of states plus rules for the next state and output under each relevant input event.

An FSM description is a useful abstraction for exploring behavior, but it does not contain all physical design information. A candidate must eventually become gates or transistors with setup and hold requirements, clock-to-Q delay, reset recovery, metastability behavior, power, area, routing and variation limits.

#### What “exhaustive” means

B-Flex uses exhaustive FSM search to explore a broader flip-flop design space. Exhaustiveness is meaningful only relative to the state encoding, transition grammar, candidate size, allowed signals, reset semantics and other bounds. Searching every candidate in that finite representation does not establish that every transistor topology or every circuit with the same function was considered.

The workflow also needs rules for rejecting invalid candidates and for proving that a candidate implements the required sequential behavior. A functionally equivalent candidate can still be unusable if it has a poor clock path, unsafe reset, excessive switching, difficult layout or a characterization corner failure.

#### What a complete cell evaluation must measure

Compare the discovered cells with the conventional library and heuristic search under the same process, load, clock, reset, input slew, output slew, voltage, temperature, placement and timing constraints. Report candidate count, search time, characterization time, area, leakage, dynamic power, setup/hold, clock-to-Q, recovery/removal, metastability or robustness checks and yield across process corners.

Then map representative larger designs with the extended library. A cell that improves isolated PPA but is rarely selected or creates routing and timing problems may not improve a complete design. Library integration, legalization, placement, routing, extraction, signoff and manufacturing assumptions must remain visible.

The captured DAC description supports exhaustive FSM-based flip-flop exploration. It reports no state-space boundary, search cost, PPA, technology, variation, signoff or silicon result. The evidence supports systematic sequential-design exploration, not a globally optimal or production-ready flip-flop library.

[Observed paper card](../observed-subthemes/cell-and-circuit-design.md#paper-dac-2026-research2394)

## Celle: retain equivalent alternatives during exploration

[Celle](../observed-subthemes/cell-and-circuit-design.md#paper-dac-2026-research278) uses equality saturation for standard-cell library extension. At a conceptual level, equality-based exploration retains alternative expressions connected by valid equivalences rather than committing immediately to one rewrite. A later selection step chooses a candidate according to a cost objective.

That separates two requirements: the transformations must preserve the relevant function, and the selected expression must lead to a useful physical implementation. A logically equivalent alternative may be expensive to implement or incompatible with the intended library constraints.

The source does not expose the equivalence rules, representation, stopping limits, or extraction cost. It would be unjustified to infer that the search reaches every equivalent expression or that the cost function includes complete physical effects. The method name identifies an approach, not a proof of unlimited search or best possible cell quality.

The record also lacks the target library, fabrication assumptions, characterization flow, and measured results. Its claimed extension capability does not establish that new cells have passed final physical and electrical acceptance checks.

<span id="explanation-dac-2026-research278"></span>

### Celle: equality saturation delays commitment, but library extension still ends in physical acceptance

#### The problem a cell-library extension is trying to solve

A standard-cell library contains legal circuit building blocks that synthesis and physical-design tools can select. The library is not just a list of Boolean formulas. Each entry has a defined function, pins, allowable input and output behavior, physical layout, timing arcs, power behavior, drive strength, area and manufacturing rules.

A library can miss a useful implementation. The missing option may compute the same function as an existing cell but use a different internal structure, transistor arrangement or pin relationship. The design question is therefore not only “which expression is logically correct?” It is also “which legal implementation has the best measured behavior for the target process, loads, wiring and design constraints?”

#### What equality saturation changes

An ordinary rewrite flow usually chooses one expression, rewrites it, and continues from that choice. If an early choice removes an alternative, later steps cannot recover it. Equality saturation keeps multiple expressions together in an equivalence structure, commonly called an e-graph. An equivalence class represents expressions that are claimed to compute the same function under the declared assumptions.

The separation is important. A rewrite rule is valid only if it preserves the function for all input conditions covered by the rule. The e-graph can then retain several valid forms instead of treating the first discovered form as the only path. Equality saturation does not mean that every possible circuit is present. The result depends on the expression language, rewrite rules, assumptions, resource limits and stopping condition.

After exploration, an extraction step selects one representative from the equivalent alternatives. That selection needs a cost model. A gate-count cost can favor a compact formula, but gate count is not the same as cell area, delay, leakage, dynamic power or routability. A physically meaningful cost may need technology mapping, transistor sizing, pin capacitance, fanout, input slew, output load, wiring estimates and timing constraints. If those terms are absent, the extracted result is optimized only for the stated abstract cost, not for complete silicon behavior.

#### What must be proved before a new library cell is usable

First, the proposed cell must be functionally correct. The Boolean or sequential behavior must be checked against the required truth table and against any assumptions used by the rewrite rules. A mathematically equivalent expression can still be wrong if the equivalence was applied outside its valid domain or if an input, reset, power or unknown-value convention was omitted.

Second, the circuit must obey the target process and library interface. Its layout must satisfy design-rule checks and layout-versus-schematic checks. Its pins, power connections, well structures, electrical limits and legal drive/load ranges must be defined. The cell then needs characterization across voltage, temperature, process corners, input slews and output loads, including timing arcs, leakage and dynamic power.

Third, the cell must help after integration. Map representative designs with the old and extended libraries under the same synthesis, placement, routing, extraction and signoff settings. Measure area, timing, power, congestion, buffering, cell-selection frequency, failure rate and runtime. A cell that is better in isolation may be rejected by the mapper, create worse wiring, or improve one path while hurting total design closure.

The captured official description identifies equality-saturation-based library extension, but it does not provide the rewrite system, e-graph representation, saturation limits, extraction objective, target library, process, characterization results or larger-design measurements. The evidence supports a search method for retaining equivalent cell candidates. It does not establish exhaustive coverage, global optimality, manufacturability, PPA improvement or production-library readiness.

## A better individual cell may not improve a complete design

Library entries compete for use during mapping and implementation. A cell can look attractive in isolation but rarely be selected, or its benefit can be offset by wiring and placement effects. Evaluating new entries therefore needs both cell-level characterization and representative larger designs using the extended library.

The comparison should preserve the same functional requirements, timing targets, technology, and implementation settings. Additional search effort, manual corrections, and characterization costs should remain visible. A larger library is not automatically better if it increases tool complexity without improving usable outcomes.

## The shared research question

B-Flex and Celle motivate widening the set of circuit candidates considered before physical implementation. Their search mechanisms differ, and the records do not demonstrate their integration. The common question is whether more systematic exploration produces independently validated cells that improve complete designs within a stated engineering budget.

Answering that requires explicit search boundaries, correctness checks, complete characterization, and downstream implementation comparisons. The current descriptions provide a clear methodological direction but no quantitative ranking, yield improvement, or demonstrated replacement for expert library design.

## Compare the results carefully

First identify the inputs and required output quality. Then identify the limited resource: time, memory, communication, energy, circuit area, or correctness coverage. Ask which part of the method reduces that cost and which new cost it adds. Compare numbers only when the experiments hold these conditions sufficiently similar.

A conference description may explain the proposal while omitting the full experiment. An author preprint link may have been coded from its abstract. The source classification does not by itself establish that every table was read. Missing locations remain visible below.

## Complete captured evidence

These are evidence records, not substitutes for the explanations above. Each record preserves its problem, proposed method, measurements, comparison conditions, and source limits. A populated record does not establish that its mechanism has been fully explained or independently verified.

<span id="paper-dac-2026-research2394"></span>

### B-Flex: Exploration of Broader Flip-Flop Design Space Based on FSM Exhaustive Search

DAC 2026 · Record: `dac-2026-research2394`

[Read the step-by-step explanation](#explanation-dac-2026-research2394)

**Updated source-backed reading card**

Reviewed 2026-09-08. Deepens the existing B-Flex treatment into a paper-level reading; defines the boundary of FSM exhaustiveness and separates sequential functional correctness from transistor implementation, PPA, timing, variation and library adoption.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Flip-flop choices affect power, performance and area, but common design flows may search only a narrow set of familiar sequential implementations.

**Mechanism / artifact:**

Exhaustive finite-state-machine search over flip-flop design alternatives; state representation, transition grammar, candidate-generation boundary, invalid-candidate rules and physical realization are unspecified.

**Workload — the work tested:**

Flip-flop circuits and sequential design cases; technology, clock/reset requirements, load, constraints, candidate count and benchmark suite are unspecified.

**Hardware and manufacturing assumptions:**

Standard-cell or custom flip-flop implementation; process, transistor models, layout, characterization corners, power measurement and signoff assumptions are unspecified.

**Baseline — the comparison method:**

Conventional flip-flop library

Heuristic flip-flop search

Functional, PPA, technology, timing, variation and library-integration conditions are unspecified

**Reported measurements:**

Flip-flop PPA exploration is claimed qualitatively; no candidate count, search time, area, delay, power, yield, variation or silicon result is reported.

**Limits on the conclusion:**

A finite-state model describes states and input/clock transitions. Exhaustively enumerating that model means every candidate in the declared representation was explored; it is not every possible transistor circuit or physical implementation. In other words, the record does not establish that every possible transistor circuit was searched.

A candidate can have correct state-transition behavior while violating setup/hold, reset recovery, clock-to-Q, metastability, slew, power or layout constraints. The mapping from an FSM candidate to a circuit and the characterization flow determine whether it can become a usable library cell.

The official description reports no state-space size, candidate-generation rule, search cost, PPA, technology, variation, signoff or silicon result. The record supports systematic sequential-design exploration, not a globally optimal or production-ready flip-flop library.

**Source and location**

Evidence tier: Primary captured official DAC description plus existing chapter level b flex discussion; no full paper extraction, cell characterization or signoff/silicon validation. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH2394)

DAC 2026 official description; captured Problem, Mechanism / artifact, Workload, Hardware, Baseline, Measurements and Limits fields; record RESEARCH2394; no manuscript pages.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** conventional flip-flop library

heuristic flip-flop search

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH2394

**Hardware or process assumptions:** Standard-cell or custom flip-flop implementation; process and signoff assumptions are unspecified.

**Limits:** No PPA, timing, search cost, yield, or silicon results are reported.

Exhaustive scope may not transfer across technologies.

Official description only; library and signoff validation is required.

**Method or artifact:** Exhaustive FSM search over flip-flop design alternatives.

**Metrics:** Flip-flop PPA exploration is claimed qualitatively

**Problem:** Flip-flop design choices affect power, performance, and area but are often narrowed prematurely.

**Workload or benchmark:** Flip-flop circuits and sequential design cases; technology, constraints, and baselines are unspecified.

</details>

<span id="paper-dac-2026-research278"></span>

### Celle: Automated Standard Cell Library Extension via Equality Saturation

DAC 2026 · Record: `dac-2026-research278`

[Read the step-by-step explanation](#explanation-dac-2026-research278)

**Updated source-backed reading card**

Reviewed 2026-09-08. Deepens the existing Celle treatment into a paper-level reading; defines equality saturation, separates equivalence preservation from extraction cost, and makes library characterization, physical signoff and larger-design integration explicit.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Standard-cell libraries may omit useful implementations for a target function, process or design constraint.

**Mechanism / artifact:**

Equality-saturation-based standard-cell library extension; the expression language, rewrite rules, equivalence assumptions, e-graph limits, extraction objective and cell-generation flow are unspecified.

**Workload — the work tested:**

Logic cells and synthesis patterns; functions, expression sizes, target designs, library coverage, task count and evaluation protocol are unspecified.

**Hardware and manufacturing assumptions:**

Standard-cell implementation and characterization; PDK, process corners, voltage, temperature, layout rules, timing/power models, routing conditions and signoff tools are unspecified.

**Baseline — the comparison method:**

Manual cell design

Existing standard-cell library

Heuristic or ordinary rewrite search

Function, library, process, mapping, placement, routing, signoff and runtime conditions are unspecified

**Reported measurements:**

Library-extension efficiency is claimed qualitatively; no equivalence-coverage, e-graph-size, search-time, extraction-cost, area, timing, power, characterization, routing, manufacturability or larger-design result is reported.

**Limits on the conclusion:**

Equality saturation retains multiple expressions connected by valid equivalences, but it does not imply that every possible expression or transistor implementation was enumerated. Coverage is bounded by the expression language, rewrite rules, assumptions, resource limits and stopping condition.

Logical equivalence is necessary but not sufficient for a usable library cell. Extraction needs a cost model, and a cost based only on abstract operators may not reflect cell area, delay, power, pin capacitance, fanout, wiring, variation or design-rule constraints.

A new cell must pass functional checking, legal layout checks, characterization across stated corners and integration in representative designs. The official description reports none of those quantitative results; the record supports a candidate-generation method, not global optimality, PPA improvement or production-library readiness.

**Source and location**

Evidence tier: Primary captured official DAC description plus existing chapter level celle discussion; no full paper extraction, independent equivalence audit, cell characterization or signoff validation. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH278)

DAC 2026 official description; captured Problem, Mechanism / artifact, Workload, Hardware, Baseline, Measurements and Limits fields; record RESEARCH278; no manuscript pages.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** manual cell design

existing standard-cell library

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH278

**Hardware or process assumptions:** Standard-cell design and signoff flow; PDK and characterization assumptions are unspecified.

**Limits:** No PPA, timing, characterization, manufacturability, or library-coverage results are reported.

Equality-saturation candidates may violate hidden design rules.

Official description only; signoff validation is required.

**Method or artifact:** Equality-saturation-driven standard-cell library extension.

**Metrics:** Library-extension efficiency is claimed qualitatively

**Problem:** Standard-cell libraries may miss useful implementations for new constraints or technologies.

**Workload or benchmark:** Logic cells and synthesis patterns; technology, rules, and library baseline are unspecified.

</details>

## What remains to establish

Resolve unspecified workloads, comparison methods, resource budgets, and source locations before generalizing a reported gain. Multiple papers in this selected sample permit comparison of mechanisms, but do not by themselves establish recurrence across years or a long-term trend.

[All subthemes](../expanded-taxonomy-v1.md) · [Research directions](../directions/README.md)
