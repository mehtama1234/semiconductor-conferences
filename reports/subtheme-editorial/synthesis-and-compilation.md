## Compiling a quantum program means choosing a physical implementation

A quantum circuit describes operations on qubits. Executing it requires translating those operations into what a target architecture can perform. The ordering must respect dependencies and resource limits. Different targets impose different costs. Moving atoms in a neutral-atom device differs as a resource problem from supplying particular logical operations in an error-corrected architecture.

The two papers grouped here optimize those different costs. One targets compilation search and atom rearrangement; the other targets T-gate count in quantum synthesis. Their metrics should not be combined into a single compiler ranking.

## A compiler for zoned neutral-atom hardware

The [Iterative Diving Search compiler](../observed-subthemes/synthesis-and-compilation.md#paper-dac-2026-research1316) addresses zoned neutral-atom architectures. In the proposed setting, a compiler must plan operations together with atom rearrangement across the available structure. A circuit that is valid as an abstract sequence is not automatically a feasible physical schedule.

The official description identifies a goal-directed search intended to reduce memory demands and relaxed routing intended to reduce rearrangement. It reports compilation of circuits with thousands of qubits and a 28.1% average reduction in atom-rearrangement overhead. It does not specify whether that overhead is measured as movement count, duration, or another aggregate. The original wording must therefore stay attached to the reported percentage.

The description also omits the circuit suite, memory footprint, compilation time, trap geometry, movement timing, and gate model. Compiling a large circuit demonstrates a software result under assumed hardware rules. It is not evidence that the same computation was run successfully on a physical device.

A useful evaluation would preserve the same target geometry and validity constraints. It would report worst cases as well as averages. It would count both compiler resources and the final execution schedule. Reduced movement may be useful without proportionally reducing duration if another dependency dominates. Its effect on execution errors also requires an explicit physical model or measurements.

<span id="explanation-dac-2026-research1316"></span>

## IDS and relaxed routing: compiler scalability must remain tied to physical atom motion

In a zoned neutral-atom processor, qubits are carried by atoms. Traps, transport lanes and operation zones constrain the atoms' positions and allowed interactions. A compiler therefore maps an abstract circuit into gate operations, atom assignments, movements and timing. A smaller search memory footprint is a compiler property. It is not by itself a reduction in the physical work needed to execute the circuit.

The described method combines Iterative Diving Search (IDS) with relaxed routing to reduce atom rearrangement. IDS is a goal-directed search intended to avoid the memory growth of prior compilation methods. IDS changes how candidate schedules are explored. Relaxed routing changes which movement constraints or intermediate arrangements are accepted. The compiler must state the legal state representation, routing constraints, atom occupancy rules, and collision avoidance. It must also state gate compatibility, search bound and pruning rule. It must state a proof or check that the resulting schedule preserves the circuit.

The first correctness gate is logical and physical feasibility. Verify that every logical qubit remains associated with the correct atom. Verify that every gate's operands are co-located or otherwise supported. Verify that movements do not collide or violate zone capacity. Verify that the schedule respects operation and transport dependencies. Then evaluate transport duration, atom loss, motional heating, gate fidelity, calibration assumptions and measurement/readout conditions. A lower movement count can increase path length or create waits. A relaxed constraint can improve search results only by changing the permitted hardware model.

The second gate is resource and quality accounting. Report peak compiler memory, runtime, explored states, seeds, timeout behavior and whether a failed search means infeasibility or resource exhaustion. For the generated schedule report movement count, distance, duration, parallelism, and idle time. Also report circuit depth, gate count, atom loss and modeled or measured success probability. Define “rearrangement overhead” before interpreting the claimed percentage; it could mean movements, distance, time, or a weighted cost.

The official description reports compilation of circuits with thousands of qubits and a 28.1% average reduction in rearrangement overhead. It does not provide the circuit suite, qubit distribution, trap geometry, movement timing, and gate model. It also does not provide memory footprint, compilation time, baseline configuration, fidelity model or worst-case results. The evidence supports a scalable neutral-atom compilation search direction. It does not show physical-device execution, fidelity preservation or universal reduction in total quantum runtime.

## Why minimizing T gates is a distinct synthesis objective

A T gate is a particular quantum phase operation outside the Clifford gate family. Its implementation can require additional resources in fault-tolerant computation. [IBM's fault-tolerant computation lesson](https://learning.quantum.ibm.com/course/foundations-of-quantum-error-correction/fault-tolerant-quantum-computation) describes how an appropriate additional quantum state can support its implementation using Clifford operations. This motivates tracking T cost separately rather than assigning every operation the same price.

[Quantum Circuit Synthesis Using an Exact T Library](../observed-subthemes/synthesis-and-compilation.md#paper-dac-2026-research031) argues that minimizing classical AND operations misses phase cancellation. That makes AND minimization an imperfect substitute for minimizing T gates. The method groups Boolean functions under Clifford equivalence and precomputes T-optimal implementations up to seven variables. It maps larger work using that library.

Grouping equivalent cases can avoid solving redundant small problems. Precomputation moves effort out of each subsequent mapping operation, but does not eliminate that effort. The source does not provide the library construction cost or complete scalability boundary.

The official description reports up to 16% lower T count on EPFL benchmarks and improvements for selected cryptographic modules. “Up to” denotes a best reported reduction, not the average. Exact optimality of the bounded library entries also does not establish global optimality of every larger mapped circuit. The full mapping procedure and its guarantees are needed for that claim.

<span id="explanation-dac-2026-research031"></span>

## Exact-T synthesis: bounded optimality must be checked against the actual ancilla and hardware contract

T-count is a synthesis objective for fault-tolerant circuits because T gates and their magic states can dominate resource cost. It is not the complete execution cost. A lower T count can coexist with more Clifford operations, greater depth, or more ancillas. It can also coexist with harder routing, or a schedule that does not match the available magic-state factories.

The work formulates exact T synthesis and groups Boolean functions under Clifford equivalence. It precomputes T-optimal implementations for bounded small cases. It maps larger circuits with a specialized mapper. The selected author-preprint assessment records an exact-solver bound of N ≤ 7 total qubits. It also records a correctness condition involving a clean output ancilla initialized to zero. Those conditions matter. Matching a Boolean function is not automatically unrestricted unitary equivalence. Bounded library optimality is not global optimality for larger circuits.

The correctness gate should check phase convention, qubit ordering, output ancilla state, and measurement behavior. It should also check temporary resources and the exact Clifford-equivalence relation. Compare synthesized circuits with an independent statevector/formal reference on exhaustive small cases and held-out larger circuits. Report invalid, repaired, ancilla-violating and phase-mismatched outputs separately.

The source boundary also needs reconciliation. The official description reports up to 16% T-count reduction. The selected preprint assessment reports 5.3% geometric-mean reduction for six EPFL arithmetic circuits with the customized mapper. It reports about 0.5% for library-only substitution, with regressions on some circuits. It reports mapping stages up to 11.7% of reported QLUT synthesis runtime. These figures have different scopes and should not be merged without resolving the source version, circuit set and measurement boundary.

Evaluate T count, Clifford count, depth, ancillas, routing, compilation time, library construction/storage, per-circuit regressions and fault-tolerant execution cost. Include magic-state production, scheduling, code distance, qubit budget, decoder and parallelism before translating a synthesis result into physical benefit. The evidence supports exact bounded T-cost synthesis, not demonstrated globally optimal or hardware-efficient fault-tolerant compilation.

## Gate count is not complete execution cost

A lower T count can still coexist with different operation ordering, auxiliary qubit requirements, or other gate costs. The schedule determines which operations can occur concurrently. Consequently, T count alone does not quantify physical runtime or total error-correction resources.

The shared research question is how closely a compiler's objective matches the cost of useful execution on its intended architecture. These papers offer two concrete objectives but do not establish their complete physical consequences. A convincing end-to-end comparison would report semantic correctness, target-specific resource constraints, preparation and compilation costs, and a validated execution-cost model. It would preserve the distinction between compiler scalability, local synthesis optimality, and successful physical computation.
