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
