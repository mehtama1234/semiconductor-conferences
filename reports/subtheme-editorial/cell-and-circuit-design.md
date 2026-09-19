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
