# Logic synthesis and optimization

This subject has 3 records in the selected sample. This page explains where it fits, then presents all captured paper evidence without shortening the measurements or limitations.

[Definitions used in the paper records](../reading-guide-v1.md)

## Understand the parent subject first

- [Design methodology and tooling](../themes/design-methodology-and-tooling.md)

## The same logical function can have many structures

A Boolean function maps input bits to output bits. It can often be implemented using different arrangements of logic operations. Logic synthesis chooses and transforms those arrangements while preserving the required input-output behavior.

The representation might count abstract operations, use cells from a hardware library, or describe transistor connections. Each level exposes different costs. A reduction at one level does not necessarily produce a smaller or faster final physical circuit.

## Sharing logic creates a tradeoff

If several outputs need the same intermediate result, one implementation can compute it once and share it. This may reduce duplicated circuitry. The shared result may then need to drive more destinations or travel farther, affecting electrical loading and delay.

Duplicating some logic can sometimes reduce those costs. The optimization therefore needs an objective that reflects the target implementation, together with timing and correctness constraints. Fewer abstract nodes alone is an incomplete hardware-quality measure.

## Local rewriting limits the search

A local method chooses a region of a circuit and searches for an equivalent replacement. Restricting the region can make the search tractable. A small region may, however, hide a larger opportunity involving several shared computations.

The multiple-node Boolean-optimization record proposes transformations across more than one node. Its current description does not establish area, delay, power, runtime, or benchmark results. The key question is whether the extra search and equivalence-checking effort produces better mapped circuits under comparable constraints. [Recorded evidence](../observed-subthemes/logic-synthesis-and-optimization.md#paper-dac-2026-research3091)

<span id="explanation-dac-2026-research3091"></span>

### Shared Logic Unleashed: coordinated multi-node rewriting can change sharing, not just individual formulas

#### Why one-node rewriting can stop too early

A Boolean network contains nodes whose outputs feed other nodes. A single-node rewrite replaces one function while holding the surrounding network mostly fixed. That restriction makes search manageable, but the best change may require several nodes to change together: one node may be simplified only if another node is reshaped, two similar computations may become a shared intermediate, or a duplicated term may be removed only after downstream logic is reorganized.

Multi-node optimization searches a larger window and considers a coordinated replacement. The replacement must preserve every affected output, not only the output of one selected node. It must also preserve constraints on constants, unused outputs, fanout, state boundaries if present and interfaces to the rest of the network.

#### Why fewer nodes is not the same as better hardware

Sharing an intermediate can reduce duplicated logic, but it can increase fanout and wire length. A shared signal may need buffers, larger drivers or longer routes. A rewrite that reduces the Boolean graph can therefore increase delay, power or congestion after technology mapping. Conversely, a duplicated expression can be better when it keeps timing-critical paths local.

The objective must state whether it optimizes abstract node count, mapped cell area, timing, power, switching, congestion or a weighted combination. The equivalence check must cover all outputs under the same input assumptions. A larger replacement can also create more solver work and more opportunities for timeout or incomplete search; failure to find a replacement is not evidence that no better replacement exists.

#### What a complete multi-node evaluation needs

Define the rewrite window, number of nodes, allowed operators, shared-boundary signals, constant and don't-care assumptions, equivalence method, timeout and cost function. Compare single-node rewriting, commercial synthesis and the multi-node method on the same combinational networks, technology library, constraints and mapping flow. Report accepted and rejected candidates, equivalence-check time, search time, timeout rate, memory, area, timing, power, fanout, buffering, congestion and downstream repair.

Test circuits with common subexpressions, reconvergent paths, high fanout, irregular structure and multiple outputs. Measure both local graph change and final mapped implementation. The captured official description identifies multiple-node Boolean optimization but reports no area, delay, power, runtime or benchmark result. The evidence supports coordinated rewriting as a search direction, not proven mapped-circuit improvement or universal advantage over local or commercial synthesis.

## Satisfiability reasoning can check a candidate

A Boolean satisfiability problem asks whether some assignment of Boolean variables satisfies a set of conditions. Circuit tools can use such reasoning to search for implementations or to detect an input on which two implementations differ. How the circuit and objective are encoded affects the difficulty of the problem.

The delay-constrained local-improvement record uses satisfiability-based search to reduce area. A valid replacement must preserve behavior and satisfy the applicable delay condition. The record does not establish solve time, memory, circuit sizes, or the timing evaluation used for acceptance. [Recorded evidence](../observed-subthemes/logic-synthesis-and-optimization.md#paper-dac-2026-research754)

An unfinished search does not prove that a better implementation does not exist. A candidate accepted by an abstract delay model still needs the downstream physical checks appropriate to the final claim.

<span id="explanation-dac-2026-research754"></span>

### Delay-constrained SAT local improvement: area reduction is a constrained search, not a free rewrite

#### What the optimizer is trying to change

The method starts with a logic or mapped circuit and selects a local region for replacement. It searches for a smaller implementation that produces the same required outputs and does not violate a delay constraint. The local boundary limits the number of signals and nodes under consideration, which makes the search more manageable but prevents the method from seeing improvements that require distant or coordinated changes.

SAT can encode the original and candidate functions and ask whether an input exists that makes them differ. If no satisfying counterexample exists under the model, the candidate is functionally equivalent for the encoded assumptions. The optimizer can combine this correctness condition with candidate-shape and area constraints, then search for a feasible replacement.

#### What the delay constraint actually means

Delay is not a Boolean property. A synthesis tool may estimate it from cell timing tables, logic depth, fanout, wire assumptions or a simplified timing graph. The candidate can satisfy that estimate while failing after mapping, placement, routing, parasitic extraction, voltage/temperature corners or input-slew and output-load changes.

The acceptance rule must state whether delay is a hard limit, a worst-path limit, a slack constraint or a weighted objective. It must identify the timing model and whether area counts cells, gate equivalents, transistor area or a later physical result. A smaller circuit that increases a non-critical path may be acceptable; one that slightly changes the critical path may violate the actual design target.

#### Why local SAT search has a resource boundary

The search has at least three costs: generating candidates, proving equivalence and evaluating the area/timing model. SAT difficulty depends on the region, logic structure and encoding. A timeout means the solver did not establish feasibility or infeasibility within the budget; it does not prove that no better replacement exists. The system should record accepted, rejected, timed-out and unresolved regions separately.

Compare heuristic area optimization and SAT-free local search on the same mapped circuits, library, timing constraints and compute budget. Report area change, delay/slack change, power, solver time, total runtime, memory, timeout rate, number of regions, equivalence failures and downstream repair. Then run placement, routing, extraction and signoff checks. The captured official description reports no area, delay, solve-time, memory or circuit-suite results. The evidence supports a delay-constrained local-search direction, not proven PPA improvement or timing closure.

## Transistor-network synthesis changes the implementation level

Transsyn's captured description maps circuit regions into transistor networks and refines them using satisfiability-based reasoning. Transistors are the physical switching devices from which logic circuits are constructed. Selecting their arrangement can expose choices beyond a fixed logic-gate representation. [Recorded evidence](../observed-subthemes/logic-synthesis-and-optimization.md#paper-dac-2026-research2007)

Electrical behavior and layout constraints still matter. A transistor-count improvement can coexist with worse delay or a difficult physical arrangement. The current description leaves area, timing, power, search cost, and final electrical validation unresolved.

<span id="explanation-dac-2026-research2007"></span>

### Transsyn: cut-based mapping narrows a transistor search, while SAT refinement checks the chosen function

#### What is being mapped

Logic synthesis starts with a Boolean network and must produce a physical switching network. A cut divides a network region from the signals entering and leaving it. A mapper can enumerate or select candidate implementations for a cut, then connect those local choices into a larger circuit. A transistor network describes how transistors connect to realize the pull-up and pull-down behavior of CMOS logic rather than treating a gate as an indivisible library object.

This representation can expose transistor arrangements that ordinary gate mapping cannot see. It also introduces more physical constraints. Series and parallel devices affect resistance, capacitance, signal rise and fall, leakage, input dependence and layout. A smaller transistor count is only one possible cost and may not predict final area or timing after sizing, buffering and routing.

#### What SAT-based refinement contributes

SAT reasoning encodes Boolean conditions and asks whether an assignment exists that satisfies them. For a candidate replacement, an equivalence check can ask whether there is an input on which the original and candidate produce different outputs. If no such input exists under the encoded model, the functions are equivalent for that model. A refinement step can use this reasoning to search around a mapped candidate or reject a functionally wrong one.

The result depends on the encoding. Sequential state, unknown values, input constraints, timing assumptions, power behavior and analog transistor effects are not automatically captured by a Boolean formula. A SAT proof of combinational equivalence does not prove setup/hold behavior, delay, power, reliability, layout legality or manufacturability. The mapper must also state how it handles unresolved searches and candidates that pass logic checking but fail electrical checks.

#### What a complete transistor-synthesis evaluation needs

Fix the input networks, transistor or cell library, process assumptions, voltage, loads, timing constraints and output requirements. Compare conventional logic synthesis, non-refined transistor mapping and SAT-refined mapping with the same equivalence rule and implementation flow. Report mapped area, transistor count, delay, slew, power, leakage, congestion, search time, SAT time, memory, unresolved cases and downstream repair cost.

Then perform electrical and physical validation: device sizing, parasitic extraction, layout checks, timing across corners, power across workloads, reliability limits and representative larger designs. Test sharing, reconvergent logic, high fanout, irregular cuts and circuits that make the search difficult. The captured official description claims area-oriented transistor synthesis but reports no area, delay, power, SAT cost or benchmark result. The evidence supports a cut-based mapping and refinement direction, not proven area improvement, global optimality or post-layout readiness.

## How to compare synthesis methods

Use the same input circuits, functional requirements, technology library or device assumptions, and output constraints. Report whether equivalence was established, which instances remained unresolved, and how much total computation the search required.

Measure final area together with timing and power where relevant. State whether costs come from an abstract graph, mapped cells, or extracted physical implementation. Include later repair and optimization steps because they can change the apparent benefit.

Test circuits with different amounts of sharing and structural regularity. A strong explanation identifies why the replacement is useful, what additional cost it introduces, and which implementation conditions preserve the benefit. That supports reuse beyond a single favorable benchmark.

## Compare the results carefully

First identify the inputs and required output quality. Then identify the limited resource: time, memory, communication, energy, circuit area, or correctness coverage. Ask which part of the method reduces that cost and which new cost it adds. Compare numbers only when the experiments hold these conditions sufficiently similar.

A conference description may explain the proposal while omitting the full experiment. An author preprint link may have been coded from its abstract. The source classification does not by itself establish that every table was read. Missing locations remain visible below.

## Complete captured evidence

These are evidence records, not substitutes for the explanations above. Each record preserves its problem, proposed method, measurements, comparison conditions, and source limits. A populated record does not establish that its mechanism has been fully explained or independently verified.

<span id="paper-dac-2026-research2007"></span>

### Transsyn: Scalable, Area-Oriented Transistor Network Synthesis via Cut-Based Mapper with SAT-Based Refinement

DAC 2026 · Record: `dac-2026-research2007`

[Read the step-by-step explanation](#explanation-dac-2026-research2007)

**Updated source-backed reading card**

Reviewed 2026-09-08. Deepens the existing Transsyn treatment into a paper-level reading; defines cut-based transistor mapping and SAT equivalence refinement, separates Boolean correctness from electrical and layout correctness, and makes search cost and post-layout validation explicit.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Transistor-level synthesis must optimize area while preserving logic correctness at scale.

**Mechanism / artifact:**

Cut-based transistor-network mapper with SAT-based refinement; cut enumeration, transistor library, SAT encoding, state/unknown-value model, cost function and electrical validation are unspecified.

**Workload — the work tested:**

Boolean logic and transistor-network synthesis benchmarks; circuit sizes, sharing, fanout, reconvergence, process, constraints and benchmark suite are unspecified.

**Hardware and manufacturing assumptions:**

Transistor-level CMOS synthesis flow; device library, sizing, parasitics, voltage, loads, timing corners, layout and power assumptions are unspecified.

**Baseline — the comparison method:**

Conventional logic synthesis

Non-refined transistor mapping

Equivalence rule, technology, implementation flow, resource budget and output constraints are unspecified

**Reported measurements:**

Area-oriented synthesis quality is claimed qualitatively; no area, transistor count, delay, power, SAT time, memory, unresolved-case, congestion or post-layout result is reported.

**Limits on the conclusion:**

A cut-based mapper searches a bounded region and connects local transistor-network candidates. This can expose structures beyond fixed gate mapping, but the bound and cost model determine what was considered. Fewer transistors do not automatically mean lower final area, delay or power after sizing, buffering and routing.

SAT equivalence can establish that two Boolean models agree for the encoded inputs and assumptions. It does not automatically model sequential state, unknown values, analog delay, power, variation, parasitics, layout rules or manufacturability. A logically correct candidate can fail electrical acceptance.

The official description reports no area, delay, power, SAT cost or benchmark result. The record supports cut-based transistor mapping and refinement, not proven area improvement, global optimality or post-layout readiness.

**Source and location**

Evidence tier: Primary captured official DAC description plus existing chapter level transsyn discussion; no full paper extraction, sat cost reconstruction or post layout electrical validation. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH2007)

DAC 2026 official description; captured Problem, Mechanism / artifact, Workload, Hardware, Baseline, Measurements and Limits fields; record RESEARCH2007; no manuscript pages.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** conventional logic synthesis

non-refined transistor mapping

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH2007

**Hardware or process assumptions:** Transistor-level CMOS synthesis flow; device library and electrical constraints are unspecified.

**Limits:** No area, delay, power, SAT cost, or benchmark results are reported.

Area optimization may degrade electrical timing.

Official description only; post-layout electrical validation is required.

**Method or artifact:** Cut-based transistor-network mapper with SAT-based refinement.

**Metrics:** Area-oriented synthesis quality is claimed qualitatively

**Problem:** Transistor-level synthesis must optimize area while preserving logic correctness at scale.

**Workload or benchmark:** Boolean logic and transistor-network synthesis benchmarks; libraries and baselines are unspecified.

</details>

<span id="paper-dac-2026-research3091"></span>

### Shared Logic Unleashed: Multiple-Node Boolean Optimization for Next-Gen Synthesis

DAC 2026 · Record: `dac-2026-research3091`

[Read the step-by-step explanation](#explanation-dac-2026-research3091)

**Updated source-backed reading card**

Reviewed 2026-09-08. Deepens the existing Shared Logic Unleashed treatment into a paper-level reading; defines coordinated multi-node rewriting, separates graph simplification from mapped hardware quality, and makes sharing/fanout, equivalence, solver cost and timeout boundaries explicit.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Local Boolean rewrites can miss improvements that require coordinated multi-node transformations.

**Mechanism / artifact:**

Multiple-node Boolean optimization for logic synthesis; rewrite window, allowed operators, shared boundaries, equivalence method, timeout, cost function and mapping flow are unspecified.

**Workload — the work tested:**

Combinational logic and synthesis benchmarks; circuit size, sharing, reconvergence, fanout, outputs, technology, constraints and benchmark suite are unspecified.

**Hardware and manufacturing assumptions:**

Digital synthesis flow with Boolean rewriting; technology, cell library, mapping, timing, power, congestion and physical assumptions are unspecified.

**Baseline — the comparison method:**

Single-node rewriting

Commercial logic synthesis

Circuit, mapping, constraint, resource-budget, equivalence and comparison conditions are unspecified

**Reported measurements:**

Synthesis quality is claimed qualitatively; no area, delay, power, runtime, equivalence-check cost, timeout rate, memory, fanout, buffering, congestion or benchmark result is reported.

**Limits on the conclusion:**

A multi-node rewrite can expose coordinated simplification or sharing that a one-node window cannot see, but it searches a larger bounded region and must preserve every affected output. The rewrite boundary, operators, assumptions and timeout determine what was considered.

Fewer graph nodes do not automatically mean better mapped hardware. Sharing can increase fanout, buffering, wire length, delay, power or congestion; duplication can sometimes improve timing. The objective must distinguish abstract graph cost from mapped-cell and physical cost.

The official description reports no area, delay, power, runtime or benchmark result. The record supports coordinated Boolean rewriting as a search direction, not proven mapped-circuit improvement or universal advantage over local or commercial synthesis.

**Source and location**

Evidence tier: Primary captured official DAC description plus existing chapter level multi node boolean optimization discussion; no full paper extraction, solver cost reconstruction or mapped cell validation. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH3091)

DAC 2026 official description; captured Problem, Mechanism / artifact, Workload, Hardware, Baseline, Measurements and Limits fields; record RESEARCH3091; no manuscript pages.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** single-node rewriting

commercial logic synthesis

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH3091

**Hardware or process assumptions:** Digital synthesis flow with Boolean rewriting; technology and mapping assumptions are unspecified.

**Limits:** No area, delay, power, runtime, or benchmark results are reported.

Larger rewrites may increase search and verification cost.

Official description only; mapped-cell validation is required.

**Method or artifact:** Multiple-node Boolean optimization for logic synthesis.

**Metrics:** Synthesis quality is claimed qualitatively

**Problem:** Local Boolean rewrites can miss improvements that require coordinated multi-node transformations.

**Workload or benchmark:** Combinational logic and synthesis benchmarks; libraries, constraints, and baselines are unspecified.

</details>

<span id="paper-dac-2026-research754"></span>

### Delay-Constrained Area Optimisation Using SAT-Based Local Improvement

DAC 2026 · Record: `dac-2026-research754`

[Read the step-by-step explanation](#explanation-dac-2026-research754)

**Updated source-backed reading card**

Reviewed 2026-09-08. Deepens the existing delay-constrained SAT local-improvement treatment into a paper-level reading; separates Boolean equivalence from timing-model validity and signoff timing, and makes local search bounds, solver budgets and unresolved cases explicit.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Logic optimization must reduce area while preserving delay constraints.

**Mechanism / artifact:**

SAT-based local-improvement area optimizer; local region, candidate grammar, equivalence encoding, area definition, timing model, solver budget and downstream validation are unspecified.

**Workload — the work tested:**

Logic synthesis or mapped circuits; circuit sizes, libraries, critical paths, timing constraints, workloads, suite and region count are unspecified.

**Hardware and manufacturing assumptions:**

Standard-cell synthesis flow; PDK, cell timing, slew/load, wire, placement, routing, parasitic and corner assumptions are unspecified.

**Baseline — the comparison method:**

Heuristic area optimization

SAT-free local search

Circuit, library, timing model, compute budget, area definition and signoff conditions are unspecified

**Reported measurements:**

Delay-constrained PPA improvement is claimed qualitatively; no area, delay/slack, power, solve time, total runtime, memory, timeout, equivalence-failure or circuit-suite result is reported.

**Limits on the conclusion:**

SAT can prove functional equivalence for the encoded model, but delay is an electrical or timing-model property. A candidate can satisfy logic and an abstract delay estimate while failing after mapping, placement, routing, parasitic extraction or operating corners.

Local region bounds and solver budgets limit what is searched. A timeout or unresolved region does not prove that no better implementation exists. The result must distinguish accepted, rejected, timed-out and unproven candidates and state the area and timing definitions.

The official description reports no area, delay, solve-time, memory or circuit-suite result. The record supports a delay-constrained local-search direction, not proven PPA improvement or timing closure.

**Source and location**

Evidence tier: Primary captured official DAC description plus existing chapter level sat/local improvement discussion; no full paper extraction, solver cost reconstruction or signoff validation. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH754)

DAC 2026 official description; captured Problem, Mechanism / artifact, Workload, Hardware, Baseline, Measurements and Limits fields; record RESEARCH754; no manuscript pages.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** heuristic area optimization

SAT-free local search

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH754

**Hardware or process assumptions:** Standard-cell synthesis flow; PDK and timing model assumptions are unspecified.

**Limits:** No area, delay, solve time, memory, or circuit-suite results are reported.

SAT search may scale poorly with design size.

Official description only; signoff and benchmark validation is required.

**Method or artifact:** SAT-based local-improvement area optimizer.

**Metrics:** Delay-constrained PPA improvement is claimed qualitatively

**Problem:** Logic optimization must reduce area while preserving delay constraints.

**Workload or benchmark:** Logic synthesis or mapped circuits; libraries, timing constraints, and solver are unspecified.

</details>

## What remains to establish

Resolve unspecified workloads, comparison methods, resource budgets, and source locations before generalizing a reported gain. Multiple papers in this selected sample permit comparison of mechanisms, but do not by themselves establish recurrence across years or a long-term trend.

[All subthemes](../expanded-taxonomy-v1.md) · [Research directions](../directions/README.md)
