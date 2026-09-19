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
