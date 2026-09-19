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
