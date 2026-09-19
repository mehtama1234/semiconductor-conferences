# Optimization and search methods

This subject has 7 records in the selected sample. This page explains where it fits, then presents all captured paper evidence without shortening the measurements or limitations.

[Definitions used in the paper records](../reading-guide-v1.md)

## Understand the parent subject first

- [Design methodology and tooling](../themes/design-methodology-and-tooling.md)

## An optimization problem needs a choice, an objective, and constraints

A design tool chooses among possible implementations. The objective states what should improve, such as area or execution time. Constraints state which candidates are acceptable, such as balance between partitions, correctness, or a resource limit. Without these definitions, a reported better score is difficult to interpret.

The search procedure decides which candidates to evaluate and how to use the results. Some procedures systematically explore a representation. Others use estimates, random variation, learned policies, or combinations of these. The useful outcome is the valid solution obtained with a stated total budget.

## Representation determines what the search can see

A graph represents objects and pairwise connections. A hypergraph permits a connection to involve more than two objects. This can represent relationships such as one signal connecting several circuit terminals. Partitioning divides the objects into groups while trying to satisfy size or resource limits and control the connections crossing between groups.

A different representation can expose useful structure, but it can also omit costs that become important in implementation. A partition with fewer crossing connections may still place too much traffic on one physical link or create a timing problem. The objective must be connected to the intended downstream use.

## Impart combines coarse and fine search

Impart's captured method combines candidates and mutates choices inside a multilevel partitioning process. A multilevel method first combines objects into a smaller representation, solves a simpler problem, and refines the solution as detail is restored. [Recorded evidence](../observed-subthemes/optimization-and-search-methods.md#paper-dac-2026-research1292)

Combining solutions can reuse favorable parts of earlier candidates. Mutation introduces alternative choices. These operations may improve solution quality, but they consume evaluation time and can make outcomes depend on random choices. The current description does not establish partition balance, cut quality, runtime, problem sizes, or comparison settings.

<span id="explanation-dac-2026-research1292"></span>

## Impart: integrated memetic search must improve partition quality within a measured total budget

Hypergraph partitioning assigns vertices to `k` parts while minimizing a stated cut objective and satisfying balance constraints. A hyperedge can connect more than two vertices, so cutting one net can affect several parts. In VLSI, the cut may approximate communication or connectivity cost; in scientific computing, it may affect exchanged boundary data. That interpretation must be preserved when comparing a partition score with downstream execution.

Impart is described as integrating memetic recombination and mutation into the uncoarsening phase of one multilevel framework. Coarsening builds a smaller hypergraph, initial partitioning solves that reduced problem, and uncoarsening restores detail while refining assignments. Recombination can combine promising parent partitions and mutation can explore alternatives at multiple granularities. Integrating them may avoid repeatedly launching standalone partitioners, but it does not establish that the resulting candidates are balanced or that the added search work is cheaper.

The first gate is a precise objective. State the cut metric, balance tolerance, part weights, fixed vertices, connectivity rules, seed, number of parents, mutation/recombination operators and acceptance policy. Verify that every output assigns each vertex exactly once, honors balance and produces the claimed cut. A lower cut under a changed imbalance tolerance or a different hyperedge convention is not an apples-to-apples improvement.

The second gate is search-cost and scalability accounting. Report input vertices and hyperedges, `k`, coarsening ratios, memory peak, candidate evaluations, refinement iterations, wall time, timeout behavior and run-to-run variation. Compare one integrated framework against a standard multilevel baseline and standalone memetic approaches with the same objective, balance, seeds, stopping rule, hardware and total time or memory budget. Show quality-versus-time curves and worst cases, not only the best partition or average claim.

The official description claims that standard benchmarks show higher-quality large-`k` partitions and better escape from local optima, but supplies no cut quality, balance, runtime, memory, `k` range, benchmark identities or baseline values. The evidence supports integrated memetic multilevel search, not demonstrated scalable partition quality or an end-to-end VLSI/scientific-computing benefit.

<span id="explanation-dac-2026-research068"></span>

## DiffPart: a learned partition must become a legal, thread-efficient simulation schedule

RTL simulation evaluates a hardware design over time. Its work can be represented as dependent tasks: a task may read state produced by another task, and tasks that are independent may run concurrently. Partitioning assigns tasks to threads or scheduling domains. A partition with equal task counts can still be slow if one thread receives a long dependency chain, if the critical path crosses threads, or if synchronization and queueing dominate the useful work.

DiffPart is described as a differentiable task-graph partitioning framework that learns partitions under real operating conditions, with RTL simulation as the case study. The key change is the partition proposal and objective: the method attempts to expose threading costs that general-purpose heuristics may omit. A differentiable relaxation does not itself produce a runnable schedule. The implementation must define the task graph, features, cost model, relaxed assignment, discrete projection, dependency handling, scheduler interface and how training data or operating conditions are collected.

### A graph partition is not yet a correct simulator execution

The partition must preserve the simulator's dependency semantics. Every task needs an owner or legal execution route; reads must observe the required state version; events must not be duplicated or lost; and concurrent updates must retain the simulator's ordering rules. If a relaxed assignment places communicating tasks on different threads, the resulting synchronization is part of the schedule cost. If it places dependent tasks together, it may reduce communication but create a long serial region.

Validate the generated partition against a trusted sequential or reference simulator on the same RTL design, inputs, reset behavior, event semantics and output traces. Check state transitions, assertions, cycle/time ordering, waveform values and termination, not only final exit status. A faster run with missing events or altered race behavior is not a simulation speedup. Report invalid-partition rate, repair/fallback rate, synchronization stalls and any design features that require special handling.

### Differentiable objectives must match discrete thread costs

A continuous objective can estimate load balance, cut edges or communication, but the simulator pays discrete costs: barriers, locks, queues, cache coherence, task granularity, thread wakeups, affinity and the longest dependency-constrained path. The surrogate may rank two relaxed partitions correctly while their projected schedules reverse that ranking. Measure the correlation between objective values and actual simulator runtime on held-out designs, and report how often projection or repair changes the learned choice.

The comparison should hold the number of threads, CPU affinity, runtime, compiler, simulator version, input trace, design build, warm-up and correctness checks constant. Report task count, dependency edges, partition sizes, critical-path length, cross-thread edges, synchronization events, queueing, utilization, cache or memory effects, compile time, partition-generation time and run-to-run variance. Compare per-design results and worst cases, not only the maximum speedup.

### The wide runtime range needs its denominator and boundary

The official description reports up to 1.22×–55.25× faster simulation across diverse designs than Verilator's partitioning. The description does not map the range to individual designs, thread counts or input traces, and it does not state whether graph extraction, DiffPart training or inference, partition materialization, compilation, initialization, output handling and retries are included. “Up to” is therefore a maximum claim, not a typical improvement.

A complete end-to-end measurement should include the cost to obtain and apply the partition as well as the steady-state simulation. It should report absolute runtime and p50/p95/p99 behavior across design sizes, dependency densities, event rates and thread counts. If training is amortized, state the number of designs and runs needed to amortize it; if the model adapts online, include adaptation and instability costs.

The evidence supports learned task-graph partitioning for RTL simulation, not demonstrated reproducible general RTL-simulation acceleration or verification throughput. The design/thread mapping, host/runtime conditions, correctness checks, training cost and per-design speedup distribution remain unresolved.

<span id="explanation-dac-2026-research1042"></span>

## Gearls: zero-shot logic optimization must transfer timing behavior, not just policy features

Logic optimization rewrites a Boolean network or circuit representation before technology mapping. The desired result is usually a tradeoff among timing, area, power, and sometimes buffering or routability. A reinforcement-learning (RL) agent selects transformations and receives a reward from the resulting circuit or a proxy. If the reward or state representation omits a physical effect, the agent can learn a policy that looks successful while worsening the final mapped design.

Gearls is described as a generalizable RL framework with three relevant mechanisms: logic-cone extraction reduces the state and reward-estimation problem; cut weighting attempts to represent global timing effects using local subgraphs; and a Policy Similarity Metric (PSM) enriches the state representation to support zero-shot transfer to unseen circuits. These mechanisms change what the agent observes and how it compares states. The captured description does not specify the action library, synthesis flow, cut definition, PSM construction, reward, training corpus, policy architecture, or transfer boundary.

### Local cones are not the whole timing graph

A logic cone contains the logic contributing to a selected node or cut under a stated direction. It can make a large circuit manageable, but timing also depends on reconvergent paths, fanout, wire/load effects, buffering, mapping choices, sequential boundaries and constraints elsewhere in the design. Cut weighting may approximate those effects; it must be calibrated against the downstream timing engine rather than assumed to encode them.

Validate each selected rewrite after the same synthesis, technology mapping, buffering and timing-analysis flow. Check Boolean or sequential equivalence, fanout and library legality, then measure slack on critical and near-critical paths, not only the local reward. Report cases where the local metric and mapped WNS/TNS disagree, invalid-action or repair rates, and whether policy decisions depend on circuit names or leaked design-family features.

### “Zero-shot” has a precise boundary

Zero-shot transfer means that the policy is applied without circuit-specific retraining, but it does not mean that the new circuits, libraries, constraints, scale, representation or synthesis flow are unrelated to training data. State the circuit-family split, preprocessing, technology library, clock and I/O constraints, action vocabulary, number of optimization steps, stopping rule and whether any calibration or search occurs at test time. Hold out designs and, where claimed, technology libraries or synthesis conditions.

The PSM needs an ablation and a failure analysis. Compare the full state with logic-cone features alone, cut weighting alone, conventional RL state, supervised or heuristic policies, and per-circuit retraining. Report policy similarity distributions, action coverage, convergence, seed variation, invalid transformations and the cost of generating features and rewards. A similarity score can improve transfer while also causing two circuits with different timing sensitivities to receive overly similar actions.

### WNS, TNS, and runtime are separate measurements

The official description reports 31.7% lower worst negative slack (WNS), 32.5% lower total negative slack (TNS), and runtime equal to 13% of prior approaches on unseen benchmark circuits. It does not identify the circuit suite, absolute slack units, PPA tradeoffs, technology library, synthesis conditions, per-circuit distribution, timing-analysis boundary or whether training and feature/reward construction are included in runtime. WNS and TNS are not interchangeable: one captures the worst violation, while the other aggregates negative slack across violating endpoints.

Report absolute WNS/TNS, area, power, leakage, clock period, endpoint counts, mapped netlist validity, compile/inference/search time, and timeout or regression cases. Include synthesis, mapping, timing analysis, reward generation and final verification under the same wall-clock boundary for every baseline. The evidence supports a policy-similarity-guided RL direction for logic optimization, not demonstrated technology-independent zero-shot PPA improvement or universal timing benefit.

<span id="explanation-dac-2026-research1052"></span>

## Quantum template matching: locality can accelerate search without proving a better circuit

The quantum-template-matching record represents circuit relationships with a hypergraph and updates matches locally after changes. A template describes a structure for which a valid transformation is known. Finding a match can allow a compiler to replace part of a circuit while preserving the intended behavior under the transformation's assumptions. [Recorded evidence](../observed-subthemes/optimization-and-search-methods.md#paper-dac-2026-research1052)

The proposed representation collapses commuting gates into a super-node while retaining local connectivity. This changes what the matcher must revisit after a circuit edit: a local replacement can update the immediate neighborhood instead of searching the rest of a DAG. That is a plausible mechanism for reducing matching work. It is not itself a proof that the replacement is valid, that all relevant commutation cases are represented, or that the resulting circuit is cheaper on a physical processor.

The correctness gate is circuit equivalence. For each proposed template replacement, define the gate semantics, qubit order, parameter ranges, boundary wires, ancilla behavior and whether equality is exact up to global phase. Check small instances exhaustively or with a formal/statevector method, then test held-out larger circuits. Report unmatched, invalid and repaired candidates. A graph-level match can still be wrong if a parameterized gate, directional operation, nonlocal dependency or boundary condition was omitted.

The performance gate is broader than matcher time. Compare gate count by type, circuit depth, two-qubit operations, mapped and routed operations, compilation memory and total time including representation construction, matching, replacement, equivalence checking and routing. Keep the template library, circuit distribution, machine, parallelism, target coupling graph and native gate set fixed. A faster matcher can leave the executable circuit unchanged; conversely, a replacement can reduce abstract gates while increasing routing or noise exposure.

The official description reports 11–606x speedup over the Qiskit DAG implementation on random and arithmetic benchmarks while maintaining the same optimization quality, with acceleration increasing with circuit size. The captured evidence does not expose absolute runtimes, memory, circuit counts, gate/template conditions, equivalence failures, final depth or gate-type distributions, mapping overhead, or hardware execution. The evidence supports a locality-preserving quantum template-matching direction, not demonstrated hardware-aware compilation or end-to-end quantum execution improvement.

The method's matching time is separate from the quality of the resulting executable circuit. Faster recognition can reduce compilation cost without changing the final operation count or device execution. The record lacks the circuit population, gate set, memory use, and hardware-compilation effects needed to connect those results.

## Learned placement policies need a validated reward

Agent-Per-Qubit's captured description assigns a learned agent to each logical qubit and uses reward shaping to guide placement. A logical qubit represents encoded quantum information at the program's chosen abstraction. Placement assigns that information to locations or resources in the target organization. [Recorded evidence](../observed-subthemes/optimization-and-search-methods.md#paper-dac-2026-research1312)

A reward tells the learning procedure which actions are favorable. It needs to correspond to the final execution objective, and constraints must prevent invalid assignments. The current description leaves processor topology, circuit sizes, error assumptions, training cost, and outcome definitions unresolved. Learning a higher reward does not alone establish a better valid placement.

<span id="explanation-dac-2026-research1312"></span>

## Agent-Per-Qubit: reward shaping must survive legal routing and fault-tolerant execution

A logical-qubit placement assigns abstract qubits to physical locations, but the assignment is only useful if the circuit can execute on the target coupling graph. Interactions between distant locations require routing, and a fault-tolerant compiler may add encoded operations, ancillas, syndrome extraction, measurements, resets and decoding. Placement quality therefore cannot be judged from layout distance or a learned reward alone.

The source describes QAgent as assigning one reinforcement-learning agent to each logical qubit and jointly learning placement policies. Its Breakthrough Return Bonus (BRB) dynamically rewards meaningful layout improvements to address sparse rewards and credit assignment. The description does not expose the state/action representation, conflict resolution, joint-action feasibility, reward terms, training curriculum or integration with routing and decoding.

The first gate is legal compilation. Verify one-to-one or otherwise permitted assignments, collision handling, coupling-graph constraints, required interactions, ancilla and code-distance requirements, routing, scheduling, measurement/reset and decoder compatibility. Compare the routed circuit and logical behavior with an independent compiler/reference; report invalid, repaired, unroutable and timeout cases separately. A placement can score well before routing and become infeasible or expensive afterward.

The second gate is objective definition. “Execution cost” should state whether it includes SWAPs, two-qubit gates, depth, idle time, measurement, calibration, classical control, decoding, retries and compiler time. “Success rate” should identify physical versus logical success, noise and error model, code, decoder, circuit duration and trial count. Hold coupling graph, gate errors, code, decoder, circuit, route policy and evaluation budget constant across baselines.

The source reports up to 53.9% lower execution cost, improved circuit success rates and an ablation identifying BRB as important for stable training and policy optimization. It does not provide absolute cost, success definition, routed-gate distribution, logical-error rate, training/inference cost, per-circuit results, topology/noise matrix or independent execution validation. Test unseen circuits, topologies, code distances, noise correlations and scale, and report seed variation and invalid/repair rates.

The evidence supports workload-aware multi-agent qubit placement, not demonstrated fault-tolerant execution improvement or universal 53.9% end-to-end benefit.

## Compare the result and the effort required to obtain it

Use the same problem instances, objective definitions, constraints, and total resource budget. Include preprocessing, training, repeated runs, and final validation. Report solution quality alongside invalid outcomes, variation across runs, memory, and elapsed time.

Separate improvements due to the search procedure from changes in representation or cost model where possible. Test unfamiliar and larger instances. A transferable conclusion explains which structure the search exploits and when the benefit exceeds its own added work.

## Compare the results carefully

First identify the inputs and required output quality. Then identify the limited resource: time, memory, communication, energy, circuit area, or correctness coverage. Ask which part of the method reduces that cost and which new cost it adds. Compare numbers only when the experiments hold these conditions sufficiently similar.

A conference description may explain the proposal while omitting the full experiment. An author preprint link may have been coded from its abstract. The source classification does not by itself establish that every table was read. Missing locations remain visible below.

## Complete captured evidence

These are evidence records, not substitutes for the explanations above. Each record preserves its problem, proposed method, measurements, comparison conditions, and source limits. A populated record does not establish that its mechanism has been fully explained or independently verified.

<span id="paper-dac-2026-research1292"></span>

### Impart: Integration of Memetic Operations into Multi-Level Framework for Large-k-Way Hypergraph Partitioning

DAC 2026 · Record: `dac-2026-research1292`

[Read the step-by-step explanation](#explanation-dac-2026-research1292)

**Updated source-backed reading card**

Reviewed 2026-09-08. Deepens the existing Impart treatment into a paper-level reading; separates integrated multilevel memetic recombination/mutation from objective definition, balance validity, cut quality, memory, runtime, random variation and downstream partitioning benefit, preserves the qualitative large-k claims, and makes total search-budget comparisons explicit.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Large-k-way hypergraph partitioning is difficult to scale, while standalone memetic recombination and mutation repeatedly invoke multilevel partitioners and make high-quality search expensive.

**Mechanism / artifact:**

Single multilevel hypergraph-partitioning framework integrating memetic recombination and mutation during uncoarsening; hypergraph representation, parent selection, operators, acceptance, refinement and stopping rules are unspecified.

**Workload — the work tested:**

Standard large-k-way hypergraph partitioning benchmarks for VLSI and scientific computing; benchmark identities, vertices, hyperedges, k range, weights, balance tolerance, cut objective, seeds and instance split are unspecified.

**Hardware and manufacturing assumptions:**

Software hypergraph partitioner running on a host processor and memory; implementation language, processor, memory limit, parallelism, compiler, threading and timing environment are unspecified.

**Baseline — the comparison method:**

Standard multilevel hypergraph partitioners

Standalone memetic partitioners

Same hypergraph, cut metric, balance, part weights, seeds, stopping rule, hardware, memory limit and total time/search budget are unspecified

**Reported measurements:**

The official description qualitatively claims higher-quality large-k partitions and improved escape from local optima; it supplies no cut values, balance violations, k, runtime, peak memory, candidate count, convergence, variance or per-instance result.

**Limits on the conclusion:**

Define the cut metric, hyperedge convention, balance tolerance, weights, fixed vertices, operators, parents, seed and acceptance rule. Verify one assignment per vertex, legal balance and the claimed cut; a lower score under changed constraints is not a fair improvement.

Account for coarsening, initial partitioning, uncoarsening, recombination, mutation, refinement, candidate evaluation and retries. Report peak memory, time, time-quality curves, timeout behavior, seeds, variance and worst cases under matched total budgets.

The qualitative large-k and local-optima claims lack benchmark, objective, balance, k, runtime, memory and baseline conditions. The evidence supports integrated memetic multilevel search, not demonstrated scalable partition quality or an end-to-end VLSI/scientific-computing benefit.

**Source and location**

Evidence tier: Primary captured DAC official description plus existing chapter level conceptual discussion; no full paper extraction, partition trace, benchmark table or independent review. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH1292&sess=sess129)

DAC 2026 official description; existing chapter-level Impart discussion; captured Problem, Mechanism / artifact, Workload, Hardware, Baseline, Measurements and Limits fields; no manuscript pages or reproduced partitioning run.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** existing multi-level hypergraph partitioners

standalone memetic partitioners

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH1292&sess=sess129

**Hardware or process assumptions:** Hypergraph partitioning for VLSI/scientific-computing design; processor, memory, and implementation details are unspecified.

**Limits:** No cut-quality, balance, runtime, k range, benchmark, or baseline values are supplied.

Integrated search may trade per-instance quality against predictability and compute cost.

Official description only; partition-quality claims require paper-level verification.

**Method or artifact:** Single multi-level framework with integrated memetic recombination and mutation during uncoarsening.

**Metrics:** Higher-quality partitions claimed qualitatively

Improved local-optima escape claimed qualitatively

**Problem:** Large-k-way hypergraph partitioning in VLSI and scientific computing is difficult to scale, while standalone memetic operations make high-quality search too slow.

**Workload or benchmark:** Standard large-k-way hypergraph partitioning benchmarks; graph sizes, k values, cut/objective metrics, runtime, and baseline identities are unspecified.

</details>

<span id="paper-dac-2026-research1052"></span>

### Fast Template Matching for Quantum Circuits Using Hypergraph

DAC 2026 · Record: `dac-2026-research1052`

[Read the step-by-step explanation](#explanation-dac-2026-research1052)

**Updated source-backed reading card**

Reviewed 2026-09-08. Deepens the existing quantum-template-matching treatment into a paper-level reading; separates hypergraph locality and matcher speed from circuit equivalence, replacement quality, hardware-aware compilation and end-to-end execution benefit, and preserves the 11–606x and same-quality claims.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

DAG-based quantum-circuit template matching handles gate commutativity but loses local connectivity, increasing the complexity of finding applicable templates.

**Mechanism / artifact:**

A commutativity-aware hypergraph representation collapses commuting gates into super-nodes while retaining local connectivity; local incremental matching updates are limited to the immediate neighborhood, with template semantics, gate rules and implementation details unspecified.

**Workload — the work tested:**

Random and arithmetic quantum-circuit benchmarks compared with the Qiskit DAG-based template matcher; circuit counts, sizes, gate sets, template library, parameterized gates, connectivity distributions and evaluation seeds are unspecified.

**Hardware and manufacturing assumptions:**

Quantum-circuit compilation and optimization; target hardware coupling constraints, native gate set, qubit mapping, routing, noise model, simulator, memory and downstream execution assumptions are unspecified.

**Baseline — the comparison method:**

Qiskit DAG-based template matcher

Manual or alternative template matching

Same circuits, templates, gate semantics, equivalence checker, hardware mapping/routing flow, machine, parallelism and total compilation boundary are unspecified

**Reported measurements:**

The official description reports 11–606x matcher speedup over the Qiskit DAG implementation on random and arithmetic benchmarks while maintaining the same optimization quality, with acceleration increasing with circuit size; it supplies no absolute runtime, memory, circuit-level distribution, equivalence failures, final gate/depth counts, routing overhead or hardware-execution result.

**Limits on the conclusion:**

A structural match is not sufficient: every replacement must preserve the circuit's unitary or declared computational behavior under parameter, commutation, qubit-order, global-phase, ancilla and boundary assumptions. Check equivalence on exhaustive small cases or formal/statevector methods and on held-out larger circuits, and report invalid and repaired matches.

Matcher speed is distinct from the quality and cost of the executable circuit. Measure gate count by type, depth, two-qubit gates, mapped/routed operations, compilation memory and total time including representation construction, matching, replacement, equivalence checking and routing under the same target constraints.

The 11–606x and same-quality claims lack circuit distributions, absolute times, memory, gate/template conditions, hardware mapping and reproducibility details. The evidence supports a locality-preserving quantum template-matching direction, not demonstrated hardware-aware compilation or end-to-end quantum execution improvement.

**Source and location**

Evidence tier: Primary captured official DAC description plus existing authored chapter level explanation; no full paper extraction, executable artifact, equivalence trace or hardware aware compilation validation. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH1052&sess=sess133)

DAC 2026 official description; existing chapter-level quantum template-matching discussion; captured Problem, Mechanism / artifact, Workload, Hardware, Baseline, Measurements and Limits fields; no manuscript pages or reproduced matcher/equivalence evaluation.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** Qiskit DAG-based template matcher

**Evidence locators:** Not established in the captured evidence.

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH1052&sess=sess133

**Hardware or process assumptions:** Quantum-circuit compilation and optimization; gate-set, circuit-size distribution, hardware coupling constraints, and downstream execution assumptions are not reported in the public description.

**Limits:** The description does not provide circuit counts, gate-set details, absolute runtimes, memory use, or hardware-aware compilation impact; the speedup range requires paper-level distribution and reproducibility checks.

**Method or artifact:** Hypergraph representation with commutativity-aware super-nodes and local incremental matching updates limited to the immediate neighborhood.

**Metrics:** 11–606x matcher speedup

same optimization quality as the baseline

scaling with circuit size

**Problem:** DAG-based quantum template matching handles gate commutativity but loses local circuit connectivity, causing high matching complexity.

**Workload or benchmark:** Random and arithmetic quantum-circuit benchmarks; comparison against the Qiskit DAG-based implementation.

</details>

<span id="paper-dac-2026-research1312"></span>

### Agent-Per-Qubit: Automated Qubit Placement for Fault-Tolerant Quantum Computing

DAC 2026 · Record: `dac-2026-research1312`

[Read the step-by-step explanation](#explanation-dac-2026-research1312)

**Updated source-backed reading card**

Reviewed 2026-09-09. Deepens the Agent-Per-Qubit treatment into a paper-level reading; separates multi-agent placement, QAgent's Breakthrough Return Bonus and workload-aware reward shaping from legal mapping, routing, fault-tolerant code behavior, noise modeling and real execution success, while preserving the up-to-53.9% execution-cost and improved-success-rate claims.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Logical-qubit placement is a combinatorial compilation problem: mapping logical qubits to processor locations affects interactions, routing, execution cost and exposure to physical errors, while sparse rewards make direct learning difficult.

**Mechanism / artifact:**

QAgent assigns one reinforcement-learning agent to each logical qubit and jointly learns placement policies. The Breakthrough Return Bonus dynamically shapes rewards to highlight meaningful layout improvements and address sparse reward/credit assignment. State/action representation, conflict resolution, joint-action feasibility, reward terms, training curriculum and routing/decoder integration are unspecified.

**Workload — the work tested:**

Diverse quantum-circuit placement benchmarks for fault-tolerant execution; circuit sizes/depths, gate distributions, logical-to-physical ratio, processor coupling graphs, code and lattice geometry, routing model, noise/error rates, seeds, train/test split and evaluation budget are unspecified.

**Hardware and manufacturing assumptions:**

Quantum processor compilation with a target coupling graph and fault-tolerant execution model; qubit connectivity, gate durations, measurement/reset, error correlations, code cycle, decoder, calibration drift, classical optimization hardware and actual device/simulator status are unspecified.

**Baseline — the comparison method:**

Leading qubit-placement approaches

Heuristic or search-based placement and routing

Same circuits, coupling graph, fault-tolerant code, routing/compiler, noise model, objective, random seeds, training/inference budget and final validation are unspecified

**Reported measurements:**

The source reports up to 53.9% reduction in execution cost, improved circuit success rates and an ablation identifying BRB as important for stable training and policy optimization; it does not define execution cost or success rate, or report absolute values, routing overhead, gate/depth distributions, logical-error rate, decoder cost, training time, inference latency or per-circuit results.

**Limits on the conclusion:**

A placement is valid only if every logical qubit is assigned consistently, physical collisions are prevented, required interactions can be routed, ancilla/code constraints are respected and the resulting circuit preserves the intended operation. Validate placement, routing, scheduling, syndrome/decoder compatibility and logical equivalence rather than treating a high RL reward as a legal compilation.

Execution cost and circuit success are different objectives. Define whether cost includes added SWAPs, two-qubit gates, depth, idle time, calibration, measurement, decoding and classical control; define success as physical or logical fidelity under a stated noise and fault-tolerant model. Hold coupling, gate errors, code, decoder, circuits and route/retry policy constant.

BRB can improve learning under the training distribution while failing on unseen circuit structures, topology, code distance, noise or scale. Report per-instance distributions, invalid/repair rates, training and inference cost, sensitivity to seeds, ablations and held-out transfer. The evidence supports workload-aware multi-agent qubit placement, not demonstrated fault-tolerant execution improvement or universal 53.9% end-to-end benefit.

**Source and location**

Evidence tier: Primary captured official DAC description plus existing authored optimization discussion; no full paper extraction, reproduced rl training, fault tolerant execution validation or hardware result. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH1312)

DAC 2026 official description; existing optimization-and-search-methods editorial explanation; captured Problem, Mechanism / artifact, Workload, Hardware, Baseline, Measurements and Limits fields; no manuscript pages, circuit/topology matrix, route validation, noise trace or independent reproduction.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** leading qubit-placement approaches

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH1312&sess=sess125

**Hardware or process assumptions:** Quantum processor layout and fault-tolerant compilation with execution-cost and success-rate objectives; coupling graph, error rates, and routing model are unspecified.

**Limits:** The description omits circuit sizes, processor topology, noise/error model, training budget, and absolute costs.

Execution-cost and success-rate definitions and baseline tuning are unspecified.

Official description only; claims require paper-level and independent review.

**Method or artifact:** Multi-agent reinforcement learning with one agent per logical qubit and dynamic Breakthrough Return Bonus reward shaping.

**Metrics:** Up to 53.9% reduction in execution cost

Improved circuit success rates

BRB identified as important in ablation

**Problem:** Logical-qubit placement is a hard compilation problem where traditional heuristics struggle to minimize execution cost on quantum processors.

**Workload or benchmark:** Diverse quantum-circuit placement benchmarks for fault-tolerant execution; processor topology, code, noise model, and circuit suite are unspecified.

</details>

<span id="paper-dac-2026-research068"></span>

### A Differentiable Approach to Task Graph Partitioning: A Case Study in RTL Simulation

DAC 2026 · Record: `dac-2026-research068`

[Read the step-by-step explanation](#explanation-dac-2026-research068)

**Updated source-backed reading card**

Reviewed 2026-09-09. Deepens the DiffPart treatment into a paper-level reading; separates differentiable partition learning and thread-aware cost modeling from discrete scheduling correctness, simulator semantics, reproducibility of the wide speedup range and end-to-end RTL verification throughput, while preserving the 1.22x–55.25x source claim with its conditions unresolved.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

RTL simulation exposes dependent task graphs whose partitioning must balance parallel work against synchronization and real threading costs; general-purpose partitioners may optimize the wrong proxy.

**Mechanism / artifact:**

DiffPart, a differentiable task-graph partitioning framework that learns partitions under operating conditions for RTL simulation; graph representation, differentiable relaxation, objective, discrete projection, scheduler and training data are unspecified.

**Workload — the work tested:**

RTL simulation of diverse designs with dependent task graphs compared with Verilator partitioning; design sizes, event/task counts, dependency structure, thread counts, simulator version, compile/warm-up policy and per-design speedups are unspecified.

**Hardware and manufacturing assumptions:**

Multithreaded host RTL simulation with a partitioned task graph; CPU model, core count, memory, operating system, compiler, thread runtime, affinity, synchronization implementation and Verilator configuration are unspecified.

**Baseline — the comparison method:**

Verilator partitioning

Same RTL designs, simulator semantics, thread count, affinity, compiler, host, input traces, compile/warm-up boundary, correctness checks and timing policy are unspecified

**Reported measurements:**

The source reports up to 1.22x–55.25x faster simulation runtime across diverse designs than Verilator's partitioning, but does not report per-design values, absolute runtime, partition quality, load balance, synchronization/communication overhead, compile/training/inference cost, correctness or variance.

**Limits on the conclusion:**

A differentiable partition objective is a proxy for a discrete simulator schedule. Define task weights, dependency legality, balance, synchronization cost, queueing, thread affinity and the projection from relaxed assignments to runnable partitions; verify every task executes exactly as required, no dependency is violated, and simulator outputs match a trusted sequential or reference run.

Runtime gains must include the complete boundary: graph extraction, feature construction, DiffPart training and inference, partition materialization, simulator compilation, initialization, scheduling, synchronization, waveform/output handling and any retries. Measure speedup, utilization, critical-path stalls, load imbalance and p50/p95/p99 behavior over designs and thread counts rather than relying on a maximum.

The official description supports learned task-graph partitioning for RTL simulation and reports a wide 1.22x–55.25x runtime range, but it does not establish reproducible general RTL-simulation acceleration or verification throughput. Design/thread mapping, host/runtime conditions, correctness checks, training cost and per-design distribution remain unresolved.

**Source and location**

Evidence tier: Primary captured official DAC description plus existing authored optimization discussion; no full paper extraction, reproduced diffpart training/inference, simulator trace or independent correctness validation. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH068)

DAC 2026 official description, first and final paragraphs; existing optimization-and-search framing; captured Problem, Mechanism / artifact, Workload, Hardware, Baseline, Measurements and Limits fields; no full manuscript, partition trace, simulator configuration or reproduced RTL run.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** Verilator partitioning

**Evidence locators:** Not established in the captured evidence.

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH068&sess=sess155

**Hardware or process assumptions:** Not established in the captured evidence.

**Limits:** The description does not specify design sizes, thread counts, quality constraints, or how the wide speedup range is distributed.

**Method or artifact:** Differentiable task-graph partitioning framework that learns partitions under operating conditions.

**Metrics:** 1.22–55.25X faster simulation runtime

**Problem:** General-purpose task-graph partitioning heuristics overlook real threading costs and produce suboptimal RTL-simulation schedules.

**Workload or benchmark:** RTL simulation of diverse designs with dependent task graphs.

</details>

<span id="paper-dac-2026-research1042"></span>

### Gearls: Generalizable Reinforcement Learning Framework for Logic Optimization via Policy Similarity Metric

DAC 2026 · Record: `dac-2026-research1042`

[Read the step-by-step explanation](#explanation-dac-2026-research1042)

**Updated source-backed reading card**

Reviewed 2026-09-09. Deepens the Gearls treatment into a paper-level reading; separates logic-cone extraction, cut weighting and Policy Similarity Metric state representation from timing/policy transfer validity, PPA tradeoffs, synthesis conditions and zero-shot boundaries, while preserving the 31.7% WNS, 32.5% TNS and 13%-runtime source claims.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

RL-based logic optimization often requires circuit-specific retraining, limiting reuse across unseen circuits while timing and PPA depend on global circuit structure and technology mapping.

**Mechanism / artifact:**

Logic-cone-aware RL framework with cut-weighted timing representation and Policy Similarity Metric (PSM) state features for zero-shot transfer; action library, reward, policy architecture, training corpus and synthesis loop are unspecified.

**Workload — the work tested:**

Unseen benchmark circuits for digital logic optimization; circuit suites, gate representations, sizes, train/test/family split, technology libraries, clock/I/O constraints, optimization steps and timing-analysis conditions are unspecified.

**Hardware and manufacturing assumptions:**

Technology-mapped digital logic evaluated through a synthesis and timing flow; library cells, wire/load model, buffering, mapper, timing engine, process, PVT, compute host and hardware implementation are unspecified.

**Baseline — the comparison method:**

State-of-the-art RL optimization methods

Circuit-specific retraining

RL without logic-cone extraction, cut weighting or PSM

Same circuits, synthesis/mapping/timing flow, library, constraints, action budget, stopping rule, runtime boundary and equivalence checks are unspecified

**Reported measurements:**

The source reports 31.7% lower worst negative slack (WNS), 32.5% lower total negative slack (TNS) and runtime equal to 13% of prior approaches on unseen benchmark circuits, but does not report absolute slack units, area, power, leakage, endpoint distributions, per-circuit results, training/feature cost, synthesis conditions or technology-transfer results.

**Limits on the conclusion:**

Logic-cone and cut-weighted state features are proxies for global timing. Validate every accepted rewrite for Boolean/sequential equivalence and library legality, then run the same mapping, buffering and timing flow; compare critical and near-critical paths, reconvergence, fanout, wire/load effects and cases where local reward disagrees with mapped WNS/TNS.

Zero-shot must specify the circuit, family, technology-library, constraint and representation split and whether test-time calibration/search counts as retraining. Ablate logic-cone extraction, cut weighting and PSM; report policy similarity, action coverage, convergence, invalid/repair rates and seed variation on held-out circuits and conditions.

The source supports a policy-similarity-guided RL direction for logic optimization and reports 31.7% WNS, 32.5% TNS and 13%-runtime claims, but does not establish technology-independent zero-shot PPA improvement or universal timing benefit. WNS/TNS definitions, PPA tradeoffs, timing flow, runtime boundary, circuit distribution and cross-library validity remain unresolved.

**Source and location**

Evidence tier: Primary captured official DAC description plus existing authored logic optimization/rl explanation; no full paper extraction, reproduced policy transfer, equivalence run or cross technology validation. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH1042)

DAC 2026 official description, first and final paragraphs; existing optimization-and-search editorial explanation; captured Problem, Mechanism / artifact, Workload, Hardware, Baseline, Measurements and Limits fields; no full manuscript, circuit table, mapped-netlist trace or independent reproduction.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** high_official_description

**Baselines:** state-of-the-art RL optimization methods

**Evidence locators:** Not established in the captured evidence.

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH1042&sess=sess156

**Hardware or process assumptions:** Not established in the captured evidence.

**Limits:** The description does not identify circuit suites, PPA tradeoffs, or whether zero-shot performance holds across technology libraries.

**Method or artifact:** Logic-cone-aware RL framework with cut-weighted timing representation and policy similarity metric for zero-shot transfer.

**Metrics:** 31.7% lower worst negative slack

32.5% lower total negative slack

13% of prior runtime

**Problem:** Circuit-specific reinforcement-learning optimization requires retraining and has weak generalization to unseen circuits.

**Workload or benchmark:** Unseen benchmark circuits in digital logic optimization.

</details>

<span id="paper-iccad-2025-437"></span>

### Orthrus: Dual -Loop Automated Framework for System -Technology Co - Optimization

ICCAD 2025 · Record: `iccad-2025-437`

**Problem:**

Cross-layer exploration is expensive and technology choices lack system-level guidance.

**Mechanism / artifact:**

Bayesian system exploration, critical-cell and Pareto-normal guidance, cell fusion/recharacterization and neural-assisted differential evolution.

**Workload — the work tested:**

8x8 systolic MAC array; compressor-tree and carry-propagate-adder alternatives.

**Hardware and manufacturing assumptions:**

Customized ASAP7; Genus/Innovus implementation with cell characterization and circuit simulation. Not fabricated-silicon measurement.

**Baseline — the comparison method:**

System-only optimization with default technology and basic cells

Without fusion

Without recharacterization

**Reported measurements:**

Not established in the captured evidence.

**Limits on the conclusion:**

Hypervolume is not application speedup. Iso-power and iso-delay points differ. Figures, normalization and total search-budget fairness remain to be checked. No independent acceptance or cross-workload generalization.

**Source and location**

Evidence tier: Medium primary preprint. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://arxiv.org/html/2509.13029v1)

**Fields:** workload_or_benchmark

hardware_or_process_assumptions

**Location:** II-B; IV-A

**Fields:** method_or_artifact

**Location:** III-A-D

**Fields:** baselines

limits

**Location:** IV-A/B; Table III; Figures 9-10

#### Additional source assessment

This separately recorded check is dated 2026-09-06. It supplements the original record above and retains its own scope and uncertainty.

[Assessment record](../../iccad/data/orthrus-primary-recovery-v1.json)

[Assessed source](https://arxiv.org/html/2509.13029v1)

**Extraction scope**

Sections II-B, III, IV-A/B; PDF page 8 Figures 9-11 and Table III visually checked against versioned source.

**Conditions**

**Scope:** 8x8 systolic MAC array; customized ASAP7; EDA evaluation, not measured fabricated silicon

**Tools:** Genus 19.12-s121_1

Innovus 21.14-s109_1

Liberate 19.2.1.215

Spectre 18.1.0

Calibre 2019.3_15.11

OpenBox 0.8.4

**Baseline:** System-only architecture/synthesis/physical optimization with default technology and basic cells

**Ablations:** Without fusion

Without recharacterization

**Table iii hv times 1e minus2:** **Baseline:** 8.055

**Without fusion:** 8.582

**Without recharacterization:** 8.679

**Orthrus:** 10.727

**Reference point:** 1

1

1

**Iso metric tolerance:** 0.001

**Technology search:** **Population:** 100

**Generations:** 20

**Top candidates:** 5

**Maximum iterations:** 2

**Headline metric status**

withheld_pending_figure_and_budget_review

**Independent review status**

pending

<span id="paper-iccad-2025-109"></span>

### Automated Design Space Exploration in High-Level Physical Synthesis

ICCAD 2025 · Record: `iccad-2025-109`

**Problem:**

Multi-die FPGA timing closure depends on interacting physical-synthesis parameters.

**Mechanism / artifact:**

Implementation-feedback-guided search over device abstraction, ILP floorplanning, routing capacity and pipeline choices.

**Workload — the work tested:**

Six designs, seven design/device cases: Sextans, Callipepla, MM 10x13 on two devices, Serpens, NTT and GPT-2 Medium.

**Hardware and manufacturing assumptions:**

Alveo U55C/U280/U250 and Versal VHK158; EPYC 7742 host with 256GB DDR4-3200; up to four concurrent Vitis jobs.

**Baseline — the comparison method:**

AMD Vitis -O3 Explore with target-frequency backoff

AutoBridge with 70-90% global resource limits

**Reported measurements:**

Reported mean Fmax: 311.06 MHz DSE versus 128.48 MHz Vitis/Vivado and 186.21 MHz AutoBridge; headline ratio remains withheld pending matched-budget and baseline-failure review

**Limits on the conclusion:**

Fmax is not throughput or faster synthesis. AutoBridge fails one case; 1.67x matches unequal-population means, versus 1.65x on shared cases. Actions and time are cumulative, not independent ablations. No equal-budget superiority or independent acceptance.

**Source and location**

Evidence tier: Medium primary author pdf. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://jasonlau.io/research-papers/10.1109-ICCAD66269.2025.11240757.pdf)

**Fields:** problem

method_or_artifact

**Location:** IV; VI

**Fields:** workload_or_benchmark

hardware_or_process_assumptions

baselines

**Location:** VII-A/C/D; Tables IV-V

**Fields:** limits

**Location:** Table V, PDF page 8; supplementary denominator and runtime analysis

#### Additional source assessment

This separately recorded check is dated 2026-09-06. It supplements the original record above and retains its own scope and uncertainty.

[Assessment record](../../iccad/data/hlps-dse-primary-recovery-v1.json)

[Assessed source](https://jasonlau.io/research-papers/10.1109-ICCAD66269.2025.11240757.pdf)

**Extraction scope**

PDF first-page identity; IV framework; VII-C/D overall timing and execution time; Table V page 8 selected columns visually verified.

**Conditions**

**Scope:** Six accelerator designs across four multi-die FPGA architectures, not necessarily a complete Cartesian product.

**Devices:** Alveo U55C

Alveo U280

Alveo U250

Versal VHK158

**Host:** AMD EPYC 7742; 256GB DDR4-3200

**Baselines:** AMD Vitis, -O3 Explore, target reduced from 300 MHz in 15 MHz steps until PnR succeeds

AutoBridge, global resource limits 70-90%

**Parallelism:** Up to four concurrent Vitis jobs per batch; search dependencies limit actual parallelism.

**Headline metric status**

withheld_pending_table_and_budget_review

**Independent review status**

pending

## What remains to establish

Resolve unspecified workloads, comparison methods, resource budgets, and source locations before generalizing a reported gain. Multiple papers in this selected sample permit comparison of mechanisms, but do not by themselves establish recurrence across years or a long-term trend.

[All subthemes](../expanded-taxonomy-v1.md) · [Research directions](../directions/README.md)
