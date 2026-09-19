# Synthesis and compilation

This subject has 2 records in the selected sample. This page explains where it fits, then presents all captured paper evidence without shortening the measurements or limitations.

[Definitions used in the paper records](../reading-guide-v1.md)

## Understand the parent subject first

- [Design methodology and tooling](../themes/design-methodology-and-tooling.md)

## Compiling a quantum program means choosing a physical implementation

A quantum circuit describes operations on qubits. Executing it requires translating those operations into what a target architecture can perform, with an ordering that respects dependencies and resource limits. Different targets impose different costs. Moving atoms in a neutral-atom device and supplying particular logical operations in an error-corrected architecture are not the same resource problem.

The two papers grouped here optimize those different costs. One targets compilation search and atom rearrangement; the other targets T-gate count in quantum synthesis. Their metrics should not be combined into a single compiler ranking.

## A compiler for zoned neutral-atom hardware

The [Iterative Diving Search compiler](../observed-subthemes/synthesis-and-compilation.md#paper-dac-2026-research1316) addresses zoned neutral-atom architectures. In the proposed setting, a compiler must plan operations together with atom rearrangement across the available structure. A circuit that is valid as an abstract sequence is not automatically a feasible physical schedule.

The official description identifies a goal-directed search intended to reduce memory demands and relaxed routing intended to reduce rearrangement. It reports compilation of circuits with thousands of qubits and a 28.1% average reduction in atom-rearrangement overhead. It does not specify whether that overhead is measured as movement count, duration, or another aggregate. The original wording must therefore stay attached to the reported percentage.

The description also omits the circuit suite, memory footprint, compilation time, trap geometry, movement timing, and gate model. Compiling a large circuit demonstrates a software result under assumed hardware rules; it is not evidence that the same computation was run successfully on a physical device.

A useful evaluation would preserve the same target geometry and validity constraints, report worst cases as well as averages, and count both compiler resources and the final execution schedule. Reduced movement may be useful without proportionally reducing duration if another dependency dominates. Its effect on execution errors also requires an explicit physical model or measurements.

<span id="explanation-dac-2026-research1316"></span>

## IDS and relaxed routing: compiler scalability must remain tied to physical atom motion

In a zoned neutral-atom processor, qubits are carried by atoms whose positions and allowed interactions are constrained by traps, transport lanes and operation zones. A compiler therefore maps an abstract circuit into gate operations, atom assignments, movements and timing. A smaller search memory footprint is a compiler property; it is not by itself a reduction in the physical work needed to execute the circuit.

The described method combines Iterative Diving Search (IDS), a goal-directed search intended to avoid the memory growth of prior compilation methods, with relaxed routing to reduce atom rearrangement. IDS changes how candidate schedules are explored. Relaxed routing changes which movement constraints or intermediate arrangements are accepted. The compiler must state the legal state representation, routing constraints, atom occupancy rules, collision avoidance, gate compatibility, search bound, pruning rule and proof or check that the resulting schedule preserves the circuit.

The first correctness gate is logical and physical feasibility. Verify that every logical qubit remains associated with the correct atom, every gate's operands are co-located or otherwise supported, movements do not collide or violate zone capacity, and the schedule respects operation and transport dependencies. Then evaluate transport duration, atom loss, motional heating, gate fidelity, calibration assumptions and measurement/readout conditions. A lower movement count can increase path length or create waits, and a relaxed constraint can improve search results only by changing the permitted hardware model.

The second gate is resource and quality accounting. Report peak compiler memory, runtime, explored states, seeds, timeout behavior and whether a failed search means infeasibility or resource exhaustion. For the generated schedule report movement count, distance, duration, parallelism, idle time, circuit depth, gate count, atom loss and modeled or measured success probability. Define “rearrangement overhead” before interpreting the claimed percentage; it could mean movements, distance, time, or a weighted cost.

The official description reports compilation of circuits with thousands of qubits and a 28.1% average reduction in rearrangement overhead. It does not provide the circuit suite, qubit distribution, trap geometry, movement timing, gate model, memory footprint, compilation time, baseline configuration, fidelity model or worst-case results. The evidence supports a scalable neutral-atom compilation search direction, not demonstrated physical-device execution, fidelity preservation or universal reduction in total quantum runtime.

## Why minimizing T gates is a distinct synthesis objective

A T gate is a particular quantum phase operation outside the Clifford gate family. Its implementation can require additional resources in fault-tolerant computation; [IBM's fault-tolerant computation lesson](https://learning.quantum.ibm.com/course/foundations-of-quantum-error-correction/fault-tolerant-quantum-computation) describes how an appropriate additional quantum state can support its implementation using Clifford operations. This motivates tracking T cost separately rather than assigning every operation the same price.

[Quantum Circuit Synthesis Using an Exact T Library](../observed-subthemes/synthesis-and-compilation.md#paper-dac-2026-research031) argues that minimizing classical AND operations is an imperfect substitute for minimizing T gates because it misses phase cancellation. The method groups Boolean functions under Clifford equivalence, precomputes T-optimal implementations up to seven variables, and maps larger work using that library.

Grouping equivalent cases can avoid solving redundant small problems. Precomputation moves effort out of each subsequent mapping operation, but does not eliminate that effort. The source does not provide the library construction cost or complete scalability boundary.

The official description reports up to 16% lower T count on EPFL benchmarks and improvements for selected cryptographic modules. “Up to” denotes a best reported reduction, not the average. Exact optimality of the bounded library entries also does not establish global optimality of every larger mapped circuit. The full mapping procedure and its guarantees are needed for that claim.

<span id="explanation-dac-2026-research031"></span>

## Exact-T synthesis: bounded optimality must be checked against the actual ancilla and hardware contract

T-count is a synthesis objective for fault-tolerant circuits because T gates and their magic states can dominate resource cost, but it is not the complete execution cost. A lower T count can coexist with more Clifford operations, greater depth, more ancillas, harder routing, or a schedule that does not match the available magic-state factories.

The work formulates exact T synthesis, groups Boolean functions under Clifford equivalence, precomputes T-optimal implementations for bounded small cases, and maps larger circuits with a specialized mapper. The selected author-preprint assessment records an exact-solver bound of N ≤ 7 total qubits and a correctness condition involving a clean output ancilla initialized to zero. Those conditions matter: matching a Boolean function is not automatically unrestricted unitary equivalence, and bounded library optimality is not global optimality for larger circuits.

The correctness gate should check phase convention, qubit ordering, output ancilla state, measurement behavior, temporary resources and the exact Clifford-equivalence relation. Compare synthesized circuits with an independent statevector/formal reference on exhaustive small cases and held-out larger circuits. Report invalid, repaired, ancilla-violating and phase-mismatched outputs separately.

The source boundary also needs reconciliation. The official description reports up to 16% T-count reduction. The selected preprint assessment reports 5.3% geometric-mean reduction for six EPFL arithmetic circuits with the customized mapper, about 0.5% for library-only substitution with regressions on some circuits, and mapping stages up to 11.7% of reported QLUT synthesis runtime. These figures have different scopes and should not be merged without resolving the source version, circuit set and measurement boundary.

Evaluate T count, Clifford count, depth, ancillas, routing, compilation time, library construction/storage, per-circuit regressions and fault-tolerant execution cost. Include magic-state production, scheduling, code distance, qubit budget, decoder and parallelism before translating a synthesis result into physical benefit. The evidence supports exact bounded T-cost synthesis, not demonstrated globally optimal or hardware-efficient fault-tolerant compilation.

## Gate count is not complete execution cost

A lower T count can still coexist with different operation ordering, auxiliary qubit requirements, or other gate costs. The schedule determines which operations can occur concurrently. Consequently, T count alone does not quantify physical runtime or total error-correction resources.

The shared research question is how closely a compiler's objective matches the cost of useful execution on its intended architecture. These papers offer two concrete objectives but do not establish their complete physical consequences. A convincing end-to-end comparison would report semantic correctness, target-specific resource constraints, preparation and compilation costs, and a validated execution-cost model. It would preserve the distinction between compiler scalability, local synthesis optimality, and successful physical computation.

## Compare the results carefully

First identify the inputs and required output quality. Then identify the limited resource: time, memory, communication, energy, circuit area, or correctness coverage. Ask which part of the method reduces that cost and which new cost it adds. Compare numbers only when the experiments hold these conditions sufficiently similar.

A conference description may explain the proposal while omitting the full experiment. An author preprint link may have been coded from its abstract. The source classification does not by itself establish that every table was read. Missing locations remain visible below.

## Complete captured evidence

These are evidence records, not substitutes for the explanations above. Each record preserves its problem, proposed method, measurements, comparison conditions, and source limits. A populated record does not establish that its mechanism has been fully explained or independently verified.

<span id="paper-dac-2026-research1316"></span>

### Search Smarter, Not Harder: A Scalable, High-Quality Zoned Neutral Atom Compiler

DAC 2026 · Record: `dac-2026-research1316`

[Read the step-by-step explanation](#explanation-dac-2026-research1316)

**Updated source-backed reading card**

Reviewed 2026-09-08. Deepens the existing zoned neutral-atom compiler treatment into a paper-level reading; separates Iterative Diving Search memory/scalability and relaxed routing from legal atom schedules, transport duration, fidelity, atom loss, compiler cost and physical-device execution, preserves the thousands-qubit and 28.1% claims, and defines the rearrangement-overhead boundary.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Zoned neutral-atom architectures require compilation across a large qubit and atom-movement search space, while existing methods have memory demands that limit them to small circuits.

**Mechanism / artifact:**

Goal-directed Iterative Diving Search compiler plus relaxed atom-routing optimization; state representation, legal movement constraints, pruning, search bounds, occupancy and schedule validation are unspecified.

**Workload — the work tested:**

Quantum circuits with thousands of qubits targeting zoned neutral-atom hardware; circuit suite, qubit distribution, gate set, zone layout, movement demand, compilation time, memory footprint and quality metrics are unspecified.

**Hardware and manufacturing assumptions:**

Zoned neutral-atom quantum computer with traps, transport lanes, operation zones and atom rearrangement; geometry, zone capacity, movement timing, collision model, gate fidelity, atom loss, heating, calibration and readout assumptions are unspecified.

**Baseline — the comparison method:**

State-of-the-art neutral-atom compilers

Same circuits, logical mapping, hardware geometry, routing legality, gate model, search timeout, compiler hardware, fidelity model and end-to-end schedule-cost boundary are unspecified

**Reported measurements:**

The official description reports compilation of circuits with thousands of qubits and a 28.1% average reduction in atom-rearrangement overhead; it does not define whether overhead is movement count, distance, duration or weighted cost, and supplies no memory, compile-time, depth, fidelity, loss or worst-case result.

**Limits on the conclusion:**

Verify logical-to-physical identity, gate compatibility, zone capacity, collision avoidance and movement dependencies, then measure transport duration, idle time, atom loss, heating, gate fidelity, calibration and readout. Fewer rearrangements do not necessarily mean a shorter or more reliable execution.

Expose IDS state, pruning, bounds, initialization, explored states, peak memory, timeout behavior and relaxed-routing constraints. Report movement count, distance, duration, parallelism, circuit depth, gate count and modeled/measured success probability under the same hardware model.

The thousands-qubit and 28.1% claims lack circuit, geometry, timing, gate, baseline, memory, compile-time, fidelity and overhead-definition conditions. The evidence supports a scalable neutral-atom compilation search direction, not demonstrated physical-device execution, fidelity preservation or universal reduction in total quantum runtime.

**Source and location**

Evidence tier: Primary captured DAC official description plus existing chapter level conceptual discussion; no full paper extraction, schedule trace, hardware execution or independent review. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH1316&sess=sess133)

DAC 2026 official description; existing chapter-level zoned neutral-atom compiler discussion; captured Problem, Mechanism / artifact, Workload, Hardware, Baseline, Measurements and Limits fields; no manuscript pages or reproduced compiler run.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** state-of-the-art neutral-atom compilers

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH1316&sess=sess133

**Hardware or process assumptions:** Zoned neutral-atom quantum computer with atom rearrangement and routing operations; trap geometry, movement timing, and gate model are unspecified.

**Limits:** The description omits circuit suite, memory footprint, compilation time, fidelity, routing constraints, and baseline configurations.

Rearrangement overhead reduction may trade off circuit depth, fidelity, or search optimality.

Official description only; compiler scalability and quantum-system validity require paper-level verification.

**Method or artifact:** Goal-directed Iterative Diving Search compiler and relaxed atom-routing optimization.

**Metrics:** Thousands-qubit circuits compiled

28.1% average reduction in atom-rearrangement overhead

**Problem:** Zoned neutral-atom architectures may scale to thousands of qubits, but existing compilers require excessive memory and fail to scale beyond small circuits.

**Workload or benchmark:** Quantum circuits with thousands of qubits on zoned neutral-atom architectures; circuit suite, qubit counts, runtime, and compilation-quality metrics are unspecified.

</details>

<span id="paper-dac-2026-research031"></span>

### Quantum Circuit Synthesis Using an Exact T Library

DAC 2026 · Record: `dac-2026-research031`

[Read the step-by-step explanation](#explanation-dac-2026-research031)

**Updated source-backed reading card**

Reviewed 2026-09-09. Deepens the exact-T synthesis treatment using the captured official description and selected author-preprint assessment; separates Clifford-equivalence canonicalization, bounded exact library construction and mapping from clean-ancilla correctness, global optimality, runtime and hardware cost, and preserves the official up-to-16% claim alongside the assessed 5.3% six-EPFL-circuit geomean and 0.5% library-only result with their source/version boundary.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

In fault-tolerant quantum synthesis, T resources dominate relevant space-time cost while minimizing classical AND count can miss phase cancellation and therefore misestimate T cost.

**Mechanism / artifact:**

The work formulates exact T synthesis, canonicalizes Boolean functions under Clifford equivalence, precomputes T-optimal implementations for bounded small instances and uses a specialized mapper for larger circuits. The selected assessment identifies an exact-solver bound of N ≤ 7 total qubits and correctness under a clean output ancilla initialized to zero; phase-equivalence, ancilla, synthesis and mapper details remain bounded by the inspected sections.

**Workload — the work tested:**

EPFL arithmetic circuits and selected cryptographic modules; the selected assessment reports six EPFL circuits, comparison against exact-MC mapping, library-only substitution, and a QLUT mapping evaluation. Circuit dimensions, gate basis, ancilla limits, decomposition conventions, target fault-tolerant architecture, runtime corpus and source-version relationship to the official 16% headline are not fully reconciled.

**Hardware and manufacturing assumptions:**

Fault-tolerant quantum compilation where T gates/magic states are costly; selected mapping assessment ran on an Apple M4 Max with 36 GB RAM, but physical architecture, magic-state factory cost, scheduling, parallelism, error-correction code, qubit budget, decoder and hardware execution are unspecified.

**Baseline — the comparison method:**

Conventional XOR/AND/NOT-basis AND-count minimization

Exact-MC mapping

Library-only substitution

Previous best-known T counts

Same Boolean/unitary convention, clean-ancilla assumption, circuit set, gate basis, decomposition, mapper, target constraints, runtime boundary and source version are unspecified

**Reported measurements:**

The official description reports up to 16% T-count reduction on EPFL benchmarks and improved best-known T counts for selected cryptographic modules. The selected author-preprint assessment reports 5.3% geometric-mean T-count reduction for six EPFL arithmetic circuits with the customized mapper, about 0.5% geometric-mean reduction for library-only substitution with regressions on some circuits, and mapping stages up to 11.7% of reported QLUT synthesis runtime; these are not reconciled into one universal result and no hardware speedup is reported.

**Limits on the conclusion:**

Exactness is conditional. Verify the synthesized operation under the stated Clifford-equivalence and clean-zero-ancilla assumptions, including global phase, output ancilla state, qubit ordering, measurement behavior and allowed temporary resources. A circuit can match a Boolean function while violating the intended unitary or ancilla contract.

Exact optimality for N ≤ 7 total qubits does not establish global optimality for larger mapped circuits. Report library construction/storage, mapper search, decomposition, ancilla, depth, Clifford count, routing and compilation runtime; test held-out circuits and compare per-circuit regressions rather than only a best or geometric mean.

The official up-to-16% headline and selected 5.3%/0.5% preprint findings have different scopes and require source-version reconciliation. T-count reduction is not hardware speedup or universal space-time reduction; magic-state production, scheduling, parallelism, code distance, qubit count, error rates and physical execution remain unvalidated. The evidence supports exact bounded T-cost synthesis, not demonstrated globally optimal or hardware-efficient fault-tolerant compilation.

**Source and location**

Evidence tier: Primary captured official DAC description plus selected author preprint reading; source version discrepancy remains open, and no independent exactness proof, benchmark reproduction or fault tolerant hardware validation. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://arxiv.org/html/2605.15476v1)

DAC 2026 official description; selected author-preprint assessment exact-t-primary-assessment-v1; sections 4.2–4.3 and 6, S4.SS2/S4.SS3/S6.SS1/S6.SS2/S6.SS4, Table 2 and Figures 8–11; no independent reproduction or hardware execution.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** high_official_description

**Baselines:** conventional XOR/AND/NOT-basis AND-count minimization

previous best-known T counts

**Evidence locators:** Not established in the captured evidence.

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH031&sess=sess133

**Hardware or process assumptions:** Not established in the captured evidence.

**Limits:** The public description does not enumerate all circuits, runtime costs, or the scalability boundary of exact precomputation.

**Method or artifact:** Exact T-synthesis formulation with Clifford-equivalence canonicalization, precomputed small-function libraries, and a specialized mapper.

**Metrics:** up to 16% T-count reduction

improved best-known T counts for selected cryptographic modules

**Problem:** AND-count minimization is an imperfect proxy for T cost in fault-tolerant quantum synthesis because it misses phase cancellation.

**Workload or benchmark:** EPFL benchmarks and cryptographic circuit modules in fault-tolerant quantum synthesis.

</details>

#### Additional source assessment

This separately recorded check is dated 2026-09-06. It supplements the original record above and retains its own scope and uncertainty.

[Assessment record](../../dac/data/exact-t-primary-assessment-v1.json)

[Assessed source](https://arxiv.org/html/2605.15476v1)

**Extraction scope**

Selected HTML sections 4.2–4.3 and 6; PDF page 6 Figures 8–11 visually inspected

**Conditions**

**Locator:** S6.SS2; Table 2

**Finding:** Six EPFL arithmetic circuits; comparison against exact-MC mapping; customized mapper reports 5.3 percent geomean T-count reduction.

**Locator:** S6.SS2

**Finding:** Library-only substitution reports about 0.5 percent geomean reduction and regressions on some circuits.

**Locator:** S4.SS3

**Finding:** Exact solver bound is N <= 7 total qubits, not seven arbitrary logical inputs; larger instances use suboptimal solutions.

**Locator:** S4.SS2

**Finding:** Correctness assumes clean output ancilla initialized to zero; not unrestricted unitary equivalence.

**Locator:** S6.SS4

**Finding:** Mapping stages account for at most 11.7 percent of total synthesis runtime in the reported QLUT evaluation.

**Platform**

**Name:** Apple M4 Max

**Ram gb:** 36

**Locator:** S6.SS1

**Interpretation limits**

T-count savings are not measured hardware speedup or universal space-time savings.

Do not promote small-library exactness into whole-circuit global optimality.

Resolve source-version discrepancy before retaining a headline; chart labels are source claims, not reproduced measurements.

Pinned code availability does not establish benchmark reproduction, phase-correctness, proof validity or independent acceptance.

**Headline metric status**

withheld_pending_source_reconciliation

**Independent review status**

pending

## What remains to establish

Resolve unspecified workloads, comparison methods, resource budgets, and source locations before generalizing a reported gain. Multiple papers in this selected sample permit comparison of mechanisms, but do not by themselves establish recurrence across years or a long-term trend.

[All subthemes](../expanded-taxonomy-v1.md) · [Research directions](../directions/README.md)
