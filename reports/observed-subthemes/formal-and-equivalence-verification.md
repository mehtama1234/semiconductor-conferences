# Formal and equivalence verification

This subject has 4 records in the selected sample. This page explains where it fits, then presents all captured paper evidence without shortening the measurements or limitations.

[Definitions used in the paper records](../reading-guide-v1.md)

## Understand the parent subject first

- [Verification and validation](../themes/verification-and-validation.md)

## A proof answers a precise question about a precise model

Formal verification reasons about all behaviors permitted by a mathematical model, rather than only the input sequences chosen for simulation. Its conclusion still depends on that model and its assumptions. Proving that two circuits compute the same function does not prove that the function is the one a customer intended. Proving a digital safety property does not establish physical timing or resistance to manufacturing faults.

The four papers here reduce the work needed to answer formal questions. They change the representation of an equivalence problem, the generalization steps of a model checker, the coordination of parallel SAT solvers, or the distribution of reachability tasks. Faster proof search can make more questions tractable, but does not silently expand what each question covers.

## Miter-aware mapping: expose structure before asking the solver

A SAT solver asks whether Boolean variables can be assigned values that satisfy a formula. For combinational equivalence, connect both circuits to the same inputs and construct a comparison circuit whose output is true when any corresponding outputs differ. This comparison circuit is called a miter. A satisfying input demonstrates a mismatch; a proof that no satisfying input exists establishes equivalence under the encoding and input assumptions. A timeout establishes neither.

A lookup table can represent a small Boolean function exactly. Using tables to organize a proof problem is not necessarily a proposal to build that circuit in FPGA hardware. The aim can be to expose relationships that a solver otherwise has difficulty recovering from a large collection of small gates.

[Miter-Aware LUT Mapping](../observed-subthemes/formal-and-equivalence-verification.md#paper-dac-2026-research214) aligns corresponding regions, preserves useful XOR relations using Gaussian elimination, and chooses tables using solver-oriented scores. Section 4 and Table 2, PDF page 5, use 2–4-input tables, a single Xeon Platinum 8375C core, and a 3,600-second timeout. Inequivalent pairs include random functional perturbations of synthesized designs.

For CaDiCaL, the reported PAR2 score falls from 856.6 to 67.4, while solved instances rise from 1,530 to 1,723. Mapping time is included. CEC solves 1,735 instances in both configurations despite a lower score. Thus the headline 92.1% is a timeout-penalized score reduction for one solver, not 92.1% more verified circuits or a universal per-instance runtime reduction. [Manuscript, Section 4 and Table 2](https://arxiv.org/pdf/2607.07164v1).

PAR2 averages completed runtimes while charging an unfinished instance twice the timeout. It combines speed and timeout behavior. A comparison should therefore retain both the score and the solved count. The correctness of each mapping and encoding transformation also belongs in the verification chain; a faster solver cannot repair an incorrectly translated question.

<span id="explanation-dac-2026-research214"></span>

### Miter-Aware LUT Mapping: changing the circuit representation must preserve the equivalence question

#### What equivalence checking asks

For two combinational circuits, equivalence checking asks whether they produce the same outputs for every allowed input. A common construction connects both circuits to the same inputs and creates a miter whose output indicates that at least one corresponding output differs. A satisfying assignment to that miter is a counterexample. Proving the miter unsatisfiable establishes equivalence only for the encoded inputs, outputs, assumptions and bit-level semantics.

This gives the mapping method two obligations. It must create a representation that the SAT solver can search efficiently, and it must preserve the Boolean function and comparison relation. A timeout is not a proof of equivalence and is not a counterexample. A faster search is useful only if the transformed question has the same meaning.

#### What miter-aware LUT mapping changes

The method maps logic into LUTs while using the structure of the equivalence miter to guide that mapping. The recorded manuscript describes aligning corresponding regions, preserving useful XOR relations with Gaussian elimination and selecting tables using solver-oriented scores. The reported setup uses 2–4-input tables, a single Xeon Platinum 8375C core and a 3,600-second timeout; these conditions define the measured result rather than a universal hardware or solver property.

The method can help when the mapping exposes relations that the solver would otherwise have to rediscover through search. It can also add mapping time or choose a structure that helps one solver but not another. The transformation must therefore be checked for output correspondence, input assumptions, bit widths, constants, don't-care handling and any arithmetic or Boolean rewrite used by the mapper.

#### How to read the reported numbers

For CaDiCaL, the reported PAR2 score falls from 856.6 to 67.4 and the solved count rises from 1,530 to 1,723. PAR2 charges an unfinished instance twice the timeout, so a large reduction can result from avoiding timeouts as well as from faster completed cases. The solved count shows how many cases crossed the timeout boundary and must be reported beside the score.

CEC solves 1,735 instances in both configurations despite the reported CaDiCaL improvement. This is evidence that the effect depends on solver behavior and should not be described as a general 92.1% equivalence-checking speedup. The 92.1% number is a timeout-penalized PAR2 score reduction, not 92.1% more verified circuits and not a 92.1% reduction for every instance.

The comparison includes mapping time, so the complete boundary is mapper plus solver under the stated machine, suite, timeout and encoding settings. A useful extension would report per-instance solved status, completed-runtime distribution, mapping cost, memory use, proof or counterexample checks and results across solver versions, cores, circuit families and timeout values.

The manuscript-backed evidence supports a solver-aware LUT-mapping method with the reported CaDiCaL and CEC outcomes. It does not establish that every transformed miter is correctly encoded outside the inspected conditions, that another solver will improve, or that the result transfers to a different circuit suite or compute platform.

[Observed paper card](../observed-subthemes/formal-and-equivalence-verification.md#paper-dac-2026-research214)

## Multi-literal dropping: generalize a blocked region safely

A literal is a Boolean variable or its negation. A cube is an AND of literals describing a set of states. For example, x AND y selects fewer states than x alone. Dropping y enlarges the represented set. If a model checker blocks that larger set, it must justify excluding every added state, not only the original example.

IC3 constructs and strengthens state constraints while checking whether a bad state can be reached. Generalization tries to express a useful exclusion with fewer conditions. A stronger exclusion can reduce later work, but only if the required initiation and transition-related checks remain valid.

[Dropping Multiple Literals per SAT Call](../observed-subthemes/formal-and-equivalence-verification.md#paper-dac-2026-research2512) attempts several removals together and analyzes failed generalizations to identify literals that cannot be removed. The official description reports 28 uniquely solved cases and 16 additional solved cases versus vanilla ABC, and 6% faster execution in rIC3. These are different statistics and implementations; they should not be added or generalized to every IC3 engine. Benchmark lists, limits, soundness arguments, and timing aggregation are absent from the description. [Official multi-drop description](https://63dac.conference-program.com/presentation/?id=RESEARCH2512&sess=sess163).

Fewer solver calls need not mean less total time. A larger attempted generalization can be harder to check, and failed attempts may require recovery work. The useful comparison includes successful and failed attempts, elapsed time, memory, and final outcomes under the same limits.

<span id="explanation-dac-2026-research2512"></span>

### Dropping Multiple Literals per SAT Call: larger IC3 generalizations must remain inductive

#### What IC3 is trying to prove

IC3 checks whether a transition system can reach a bad state. It builds constraints, called frames or clauses, that describe states ruled out at increasing distances from the initial state. A clause or cube is useful only when the solver checks the required initial-state and transition conditions. The final conclusion depends on those checks, not on the number of literals removed.

A literal is a Boolean variable or its negation. A cube made from several literals describes states satisfying all of them. If one literal is dropped, the cube describes more states. A multi-literal drop therefore asks the solver to justify a larger generalization in one operation. The added states cannot simply be assumed safe because the original, smaller cube was safe.

#### What the multi-drop strategy changes

The method attempts several removals in one SAT call and analyzes failed generalizations to identify literals that cannot be removed. This can reduce repeated calls when the solver can evaluate the combined query efficiently. It can also create a harder query, require rollback after a failed attempt, or spend work exploring a generalization that will not become an inductive clause.

The implementation must define which assumptions are active during the query, how a failed multi-drop is decomposed or repaired, and which initiation, consecution and blocking checks are repeated. A reported reduction in SAT calls is not enough: total elapsed time, memory, solver work and the final invariant must be measured.

#### Soundness is the non-negotiable boundary

The enlarged cube may contain states that were not in the original cube. For a safety proof, the checker must establish that the generalized clause is valid for the relevant initial states and is preserved by legal transitions. If a property-specific heuristic drops a literal without those checks, a faster run can be an unsound proof rather than a better model checker.

#### How to read the reported outcomes

The official description reports 28 uniquely solved cases and 16 additional solved cases versus vanilla ABC, and 6% faster execution in rIC3. These numbers are not interchangeable: “uniquely solved” and “additional solved” describe different sets, while the 6% result is a time comparison in a named implementation. They should not be added, treated as one percentage, or generalized to every IC3 engine.

An adequate evaluation would publish the benchmark list, property types, solver and version, timeout, memory limit, solved and failed cases, total and per-instance time, SAT-call count, memory, convergence behavior, failed generalizations and proof-checking results. It should compare standard IC3 and single-literal dropping under identical conditions and include properties where multi-drop attempts fail.

The captured DAC description supports a multi-literal generalization direction for IC3. It reports no soundness proof, benchmark list, solve-time distribution, memory, convergence or failure-case result. The evidence supports a method hypothesis and separate preliminary indicators, not a generally established or independently reproduced IC3 improvement.

[Observed paper card](../observed-subthemes/formal-and-equivalence-verification.md#paper-dac-2026-research2512)

## PRS: diversify searches and share useful conclusions

Parallel SAT solving can run different search choices on the same formula. One worker may discover a useful assignment or deduction earlier than another. Sharing valid learned clauses can prevent repeated exploration, but requires communication and storage. A clause learned under local assumptions cannot be treated as globally valid unless those assumptions are handled correctly.

[PRS](../observed-subthemes/formal-and-equivalence-verification.md#paper-dac-2026-research284) combines resolution-checking preprocessing, varied initial branching orders, and local-search-derived starting values. Its official description also lists dynamic clause sharing, reproducible parallel solving, and parallel proof generation. On SAT Competition 2025 instances it reports 12 more solved cases and an 11.4% better PAR2 score than MallobSAT, plus 4.7× speedup on 64 cores. The last number's reference configuration is not specified, so it is not established as speedup from one to 64 cores. [Official PRS description](https://63dac.conference-program.com/presentation/?id=RESEARCH284&sess=sess163).

Reproducible execution and independently checkable proofs are separate properties. Reproducibility concerns repeating a run's behavior under stated settings. Proof checking concerns whether a claimed conclusion follows from the input formula. A report should identify the proof format, checker, checked cases, and failures rather than infer correctness from reproducibility alone.

<span id="explanation-dac-2026-research284"></span>

### PRS: parallel SAT search must share valid deductions without hiding proof and scaling costs

#### What SAT solving is trying to establish

SAT solving asks whether a Boolean formula has an assignment that satisfies all of its clauses. If the formula is satisfiable, the assignment is a witness. If it is unsatisfiable, the solver's result can support a formal conclusion only when the solver and its proof output are correct and the formula represents the intended question.

Parallel workers can start with different branching orders or initial values so that they explore different parts of the search space. A worker may also learn a clause that rules out a set of assignments. Sharing that clause can save another worker from repeating the search, but the clause must be valid for the same formula and assumptions. Communication and storage can cost more than the repeated search it avoids.

#### What the PRS components contribute

The captured PRS description combines resolution-checking preprocessing, varied initial branching orders and local-search-derived starting values. It also lists dynamic clause sharing, reproducible parallel solving and parallel proof generation. These components address different boundaries: preprocessing changes the formula representation or solver setup, branching changes search order, clause sharing changes coordination, and proof generation changes how the result can be checked.

The framework must state when a clause becomes shareable, how workers track formula assumptions, how stale clauses are handled, and how memory growth is bounded. More workers do not guarantee more useful search. Workers can duplicate one another, contend for memory, wait at synchronization points or spend time transmitting clauses that are not useful on another branch.

#### Reproducibility and proof checking are separate

Reproducibility means that a run can be repeated under stated software, hardware, seed, worker, formula-order and timeout conditions. It does not by itself show that an unsatisfiability result is supported by a checkable proof. Parallel proof generation requires a declared proof format, a way to combine or order worker contributions, a checker, and an account of instances whose proof output is incomplete or rejected.

#### How to read the reported outcomes

On SAT Competition 2025 instances, the official description reports 12 more solved cases and an 11.4% better PAR2 score than MallobSAT, plus 4.7× speedup on 64 cores. The first two figures compare outcome counts and a timeout-penalized score against a named baseline. The 4.7× reference configuration is not specified, so it cannot be called a one-to-64-core speedup. These figures must remain separate from proof-checking success and from claims about scaling to other formulas.

An adequate evaluation would publish the benchmark filter, formula classes, worker and core counts, topology, memory, timeout, per-instance solved status, PAR2 definition, clause traffic, synchronization time, proof format, checker results and failures. It should compare serial, portfolio and shared-clause configurations under the same formula order and limits, and report scaling with enough detail to distinguish parallel search benefit from hardware or baseline changes.

The captured DAC description supports a parallel SAT framework with diversified search and clause coordination. It reports no complete benchmark conditions, proof-checking record, clause traffic, per-instance result table or defined speedup reference. The evidence supports a framework direction and separate preliminary indicators, not general proof or scaling superiority.

[Observed paper card](../observed-subthemes/formal-and-equivalence-verification.md#paper-dac-2026-research284)

## Parallel reachability: distribute tasks without weakening conclusions

Reachability asks which states can follow from allowed initial states through legal transitions. An over-approximation includes every reachable state and may include extra states. An under-approximation includes only some reachable states. These have different uses: an over-approximation excluding every bad state can establish safety, while a concrete reachable bad state establishes a failure. An apparent bad state in an over-approximation may instead need refinement.

[Parallelizing Complementary Approximate Reachability](../observed-subthemes/formal-and-equivalence-verification.md#paper-dac-2026-research896) replaces centralized scheduling with fine-grained tasks and a distributed concurrent task repository from which workers acquire work. The official description reports qualitative speedup and scaling but gives no core counts, numerical results, task-validity rules, or termination protocol. [Official reachability description](https://63dac.conference-program.com/presentation/?id=RESEARCH896&sess=sess163).

The historical card's statement that approximation may miss relevant states is too broad: the direction of approximation and the decision rules determine what can be concluded. Approximate intermediate state sets do not inherently make a final proof unsound. Here, the missing evidence is the algorithm's preservation and termination argument, not evidence that it necessarily overlooks bugs.

<span id="explanation-dac-2026-research896"></span>

### Parallelizing Complementary Approximate Reachability: distribute state exploration without changing what a conclusion means

#### What reachability asks

A transition system has an initial-state set and rules that describe which next states are legal. Reachability analysis asks whether a state satisfying a property can be reached from an allowed initial state. A safety question often asks whether any bad state is reachable.

An exact analysis tries to represent the reachable states without losing the distinction between reachable and unreachable states. An over-approximation includes every truly reachable state and may include extra states. If the over-approximation excludes all bad states, that can support a safety conclusion. An under-approximation includes only some reachable states. If it finds a valid bad state, that can establish a counterexample, but failure to find one does not prove safety.

#### What complementary approximation changes

Complementary analyses can examine different parts or representations of the state space. The method described in the record replaces centralized scheduling with fine-grained tasks and a distributed concurrent task repository. That can expose parallel work, but it creates obligations for task ownership, state-set representation, duplicate detection, merging, dependencies and termination.

Each task must carry enough information to determine what conclusion it can support. A task that produces an over-approximation cannot be combined with an under-approximation under the same rule. If two workers update related state sets concurrently, the algorithm must define whether an update invalidates queued work, how stale tasks are recognized and when all relevant work has been processed.

#### Why approximation is not automatically unsound

The phrase “approximate reachability” does not alone determine whether bugs can be missed or false alarms can appear. The direction of approximation and the final decision rule determine the result. An over-approximation can create a false alarm by including a bad state that is not actually reachable; an under-approximation can miss a real bad state because it explored only part of the state space.

The formal claim must state which of these outcomes is allowed, how refinement or exact checking resolves ambiguity, and why task distribution preserves the same set relation as the serial algorithm. A speedup without this relation can change the proof question rather than accelerate it.

#### What the evaluation must expose

Compare serial approximate reachability, exact reachability where feasible, and the parallel method on the same transition systems, properties, abstraction, hardware, memory limit and termination rule. Report runtime, memory, core count, task count, queue contention, synchronization, convergence, precision or false-alarm behavior, soundness checks and the final decision for every benchmark.

Scale tests should vary state-space size, abstraction strength, task granularity, worker count, contention and the proportion of tasks that require refinement. Include cases where the over-approximation is inconclusive, the under-approximation finds a counterexample and the analysis terminates without one. These cases show whether the system preserves the meaning of positive and negative results.

The captured DAC description supports fine-grained parallel task distribution for complementary approximate reachability. It reports no approximation rule, soundness or precision bound, task-validity check, termination protocol, runtime, memory, convergence or benchmark result. The evidence supports a parallel formal-analysis direction, not demonstrated speed or preserved conclusions.

[Observed paper card](../observed-subthemes/formal-and-equivalence-verification.md#paper-dac-2026-research896)

## What connects the papers

The shared technical idea is to reduce redundant proof work while preserving the meaning of the original question. Representation, generalization, clause sharing, and task distribution act at different levels and can interact. Their speedups cannot simply be multiplied, nor do these four cases establish a longitudinal trend across conferences.

The sources were refreshed on 2026-09-07. The recovered LUT manuscript supplies page-backed evaluation conditions; the other three remain description-backed. This explanation supersedes the older cards' missing-result and overly broad interpretation statements where noted. Full source reconciliation, independent proof checking, and experimental reproduction remain open.

## Compare the results carefully

First identify the inputs and required output quality. Then identify the limited resource: time, memory, communication, energy, circuit area, or correctness coverage. Ask which part of the method reduces that cost and which new cost it adds. Compare numbers only when the experiments hold these conditions sufficiently similar.

A conference description may explain the proposal while omitting the full experiment. An author preprint link may have been coded from its abstract. The source classification does not by itself establish that every table was read. Missing locations remain visible below.

## Complete captured evidence

These are evidence records, not substitutes for the explanations above. Each record preserves its problem, proposed method, measurements, comparison conditions, and source limits. A populated record does not establish that its mechanism has been fully explained or independently verified.

<span id="paper-dac-2026-research214"></span>

### Miter-Aware LUT Mapping: Aligning Structure and Solvability for Efficient Logic Equivalence Checking

DAC 2026 · Record: `dac-2026-research214`

[Read the step-by-step explanation](#explanation-dac-2026-research214)

**Updated source-backed reading card**

Reviewed 2026-09-08. Deepens the existing manuscript-backed chapter treatment into a paper-level reading; preserves the page-backed PAR2, solved-count, solver, core and timeout conditions while making the miter transformation and correctness boundary explicit.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Combinational equivalence checking becomes difficult when the comparison miter created from two mapped circuits has structure that is hard for the SAT solver to search.

**Mechanism / artifact:**

Miter-aware LUT mapping that aligns corresponding regions, preserves useful XOR relations using Gaussian elimination and chooses tables with solver-oriented scores; mapping correctness and exact encoding conditions require verification.

**Workload — the work tested:**

LUT-mapped combinational designs, including synthesized designs and inequivalent pairs with random functional perturbations; the selected manuscript evaluation uses the reported circuit suite and 3,600-second timeout.

**Hardware and manufacturing assumptions:**

Formal equivalence flow evaluated on a single Xeon Platinum 8375C core; LUT size is 2–4 inputs in the reported Section 4/Table 2 setup; solver and encoding settings are part of the result boundary.

**Baseline — the comparison method:**

Standard LUT mapping

Solver-only equivalence tuning

CaDiCaL and CEC comparisons under the reported timeout and mapping-time boundary

**Reported measurements:**

Manuscript-backed: CaDiCaL PAR2 falls from 856.6 to 67.4 and solved instances rise from 1,530 to 1,723; CEC solves 1,735 in both configurations. The 92.1% figure is a timeout-penalized PAR2 reduction, not a universal per-instance runtime reduction or 92.1% more verified circuits.

**Limits on the conclusion:**

A miter is a Boolean comparison formula: a satisfying assignment is a counterexample, while an unsatisfiability result establishes equivalence only under the encoded inputs, outputs and assumptions. A timeout establishes neither. Any LUT mapping or Gaussian-elimination transformation must preserve the question being checked.

PAR2 combines completed runtimes with a penalty for unfinished cases, so its improvement can reflect fewer timeouts, shorter solved runs or both. The solved-count result and solver identity must remain visible. CEC's unchanged solved count shows that the effect is solver-dependent rather than a universal property of equivalence checking.

The manuscript evidence fixes the reported suite, 2–4-input tables, one Xeon Platinum 8375C core and 3,600-second timeout, but does not justify transfer to other solvers, circuits, cores, encodings or mapping objectives without new experiments.

**Source and location**

Evidence tier: Recovered manuscript backed selected evaluation plus official DAC description; independent formal reproduction and broader solver/circuit validation remain open. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://arxiv.org/pdf/2607.07164v1)

Manuscript v1, Section 4 and Table 2, PDF pages 5–7; official DAC record RESEARCH214; reported single-core, 3,600-second timeout, 2–4-input LUT and solver-specific PAR2/solved-count conditions.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** standard LUT mapping

solver-only equivalence tuning

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH214

**Hardware or process assumptions:** FPGA or LUT-based logic mapping and formal solver flow; device and encoding assumptions are unspecified.

**Limits:** No proof time, success rate, area, delay, or circuit-suite results are reported.

Solver behavior may be benchmark-specific.

Official description only; independent formal reproduction is required.

**Method or artifact:** Miter-aware LUT mapping method aligned with equivalence-solving structure.

**Metrics:** Equivalence-checking efficiency is claimed qualitatively

**Problem:** Logic-equivalence checking can become difficult when mapped circuits produce solver-unfriendly miters.

**Workload or benchmark:** LUT-mapped combinational designs; circuits, solvers, and proof settings are unspecified.

</details>

<span id="paper-dac-2026-research2512"></span>

### Dropping Multiple Literals per SAT Call in IC3 Model Checking

DAC 2026 · Record: `dac-2026-research2512`

[Read the step-by-step explanation](#explanation-dac-2026-research2512)

**Updated source-backed reading card**

Reviewed 2026-09-08. Deepens the existing IC3 explanation into a paper-level reading; separates clause generalization from soundness, preserves the official 28/16/6% claims as distinct statistics, and keeps missing benchmark and timing conditions visible.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

IC3 model checking can spend many SAT calls strengthening blocking clauses, and larger safe literal reductions may reduce repeated proof work.

**Mechanism / artifact:**

Multiple-literal dropping strategy within IC3 model checking; attempted-removal rule, failed-generalization analysis, safety checks, recovery rule and implementation are unspecified.

**Workload — the work tested:**

Hardware model-checking instances; properties, designs, solver versions, limits, benchmark list and proof settings are unspecified.

**Hardware and manufacturing assumptions:**

Formal model-checking software flow; host, parallelism, memory and timing boundary are unspecified.

**Baseline — the comparison method:**

Standard IC3

Single-literal dropping

Vanilla ABC and rIC3 are named in the official comparison, but instance, version and limit conditions are unspecified

**Reported measurements:**

Official description reports 28 uniquely solved cases and 16 additional solved cases versus vanilla ABC, plus 6% faster execution in rIC3; the statistics use different comparisons or implementations and are not additive.

**Limits on the conclusion:**

In IC3, a literal is a variable or its negation and a cube represents states satisfying all its literals. Dropping literals enlarges the represented state set. The larger cube is safe only after the required initiation, transition and blocking checks establish that the added states cannot invalidate the property.

Trying several removals in one SAT call can reduce call count but can make each query harder, increase failed-attempt recovery work or be effective only for particular properties. A faster or more general clause is useful only if the resulting invariant remains inductive and the proof checker validates it.

The official description does not expose a soundness argument, benchmark list, solve-time distribution, memory, convergence, timeout, solver version or failure cases. The 28, 16 and 6% figures therefore remain separate, condition-bound indicators rather than a general IC3 improvement.

**Source and location**

Evidence tier: Primary captured official DAC description plus existing chapter level ic3 explanation; no full paper extraction, soundness reproduction or benchmark/timing validation. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH2512)

DAC 2026 official description; captured Problem, Mechanism / artifact, Workload, Hardware, Baseline, Measurements and Limits fields; record RESEARCH2512; no manuscript pages.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** standard IC3

single-literal dropping

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH2512

**Hardware or process assumptions:** Not established in the captured evidence.

**Limits:** No soundness proof, solve time, memory, convergence, or benchmark results are reported.

Literal dropping may be property-specific.

Official description only; formal reproduction is required.

**Method or artifact:** Multiple-literal dropping strategy within IC3 model checking.

**Metrics:** Model-checking efficiency is claimed qualitatively

**Problem:** IC3 model checking spends many SAT calls refining clauses and may benefit from larger safe literal reductions.

**Workload or benchmark:** Hardware model-checking instances; properties, solvers, and proof settings are unspecified.

</details>

<span id="paper-dac-2026-research284"></span>

### PRS: An Efficient Parallel SAT Framework

DAC 2026 · Record: `dac-2026-research284`

[Read the step-by-step explanation](#explanation-dac-2026-research284)

**Updated source-backed reading card**

Reviewed 2026-09-08. Deepens the existing PRS discussion into a paper-level reading; separates search diversification, clause sharing, proof generation, reproducibility and solver-dependent outcome metrics.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

SAT solving can repeat search work across workers and needs a way to use parallel search choices and valid deductions without making proof checking or synchronization incorrect.

**Mechanism / artifact:**

PRS parallel SAT framework combining resolution-checking preprocessing, varied initial branching orders, local-search-derived starting values, dynamic clause sharing, reproducible parallel solving and parallel proof generation; exact worker protocol and proof format are unspecified.

**Workload — the work tested:**

SAT Competition 2025 instances; formula classes, instance counts, hardware, core allocation, timeout and benchmark filtering are unspecified in the captured description.

**Hardware and manufacturing assumptions:**

Parallel multicore SAT execution with clause storage and communication; core topology, memory, synchronization, worker count and clause-sharing bandwidth are unspecified.

**Baseline — the comparison method:**

MallobSAT

Serial or portfolio SAT references are not fully specified

Reference configuration for the 4.7× speedup is unspecified

**Reported measurements:**

Official description reports 12 more solved cases and an 11.4% better PAR2 score than MallobSAT, plus 4.7× speedup on 64 cores; the speedup reference configuration is unspecified and must not be read as a demonstrated one-to-64-core scaling result.

**Limits on the conclusion:**

Parallel SAT workers can explore different branching orders, but a learned clause is globally useful only when it is valid under the assumptions of the shared formula. Clause exchange adds communication, memory and synchronization cost and can reduce search diversity if workers become too similar.

Reproducible execution means a run can be repeated under stated settings; it does not prove that the SAT result is correct. Independently checkable proof generation requires a declared proof format, a checker, checked instances and handling for failed or incomplete proof output.

The captured description does not expose the benchmark filter, worker and core configuration, timeout, memory, clause-sharing traffic, proof format, checker, per-instance outcomes or speedup reference. The reported solved-count, PAR2 and 4.7× figures therefore remain separate, condition-bound results rather than general parallel-solver scaling.

**Source and location**

Evidence tier: Primary captured official DAC description plus existing chapter level prs discussion; no full paper extraction, proof checking reproduction or solver benchmark validation. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH284)

DAC 2026 official description; captured Problem, Mechanism / artifact, Workload, Hardware, Baseline, Measurements and Limits fields; record RESEARCH284; no manuscript pages.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** serial SAT solver

portfolio SAT solving

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH284

**Hardware or process assumptions:** Multicore or accelerator SAT execution; synchronization and memory assumptions are unspecified.

**Limits:** No solve rate, runtime, memory, scaling, or benchmark results are reported.

Parallel coordination can add overhead or affect reproducibility.

Official description only; solver-benchmark validation is required.

**Method or artifact:** Parallel SAT-solving framework.

**Metrics:** SAT-solving efficiency is claimed qualitatively

**Problem:** SAT solving requires scalable parallel search and clause coordination.

**Workload or benchmark:** SAT instances; solver configuration, hardware, and benchmark suite are unspecified.

</details>

<span id="paper-dac-2026-research896"></span>

### Parallelizing Complementary Approximate Reachability

DAC 2026 · Record: `dac-2026-research896`

[Read the step-by-step explanation](#explanation-dac-2026-research896)

**Updated source-backed reading card**

Reviewed 2026-09-08. Deepens the existing reachability treatment into a paper-level reading; distinguishes over- and under-approximation, task parallelism, conclusion preservation and the missing soundness, precision and termination evidence.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Reachability analysis can be expensive for large transition systems, and complementary approximate analyses may expose parallel work.

**Mechanism / artifact:**

Parallelizing complementary approximate-reachability algorithm with fine-grained tasks and a distributed concurrent task repository; approximation direction, task validity, refinement, termination and proof-preservation rules are unspecified.

**Workload — the work tested:**

Transition systems and formal reachability tasks; abstraction, property type, solver, benchmark suite, state representation and limits are unspecified.

**Hardware and manufacturing assumptions:**

Multicore or accelerator formal-analysis platform with concurrent workers; core count, memory, synchronization, task-transfer and failure assumptions are unspecified.

**Baseline — the comparison method:**

Serial approximate reachability

Exact reachability

Approximation direction, property, hardware, task and termination conditions are unspecified

**Reported measurements:**

Reachability-analysis efficiency is claimed qualitatively; no soundness, precision, runtime, memory, convergence, termination or benchmark result is reported.

**Limits on the conclusion:**

Reachability asks which states can follow from allowed initial states through legal transitions. An over-approximation may contain extra states and can support a safety conclusion only when it excludes every bad state; an under-approximation contains only some states and can support a concrete counterexample when it finds a valid bad state. The direction changes what a result means.

Fine-grained task distribution can reduce centralized scheduling work, but each task needs a defined state-set representation, validity rule, dependency relation and merge operation. Concurrent updates require a termination condition that detects when no unprocessed work can change the conclusion. Approximate intermediate sets do not automatically make a final proof unsound, but the preservation argument must be stated.

The official description reports no approximation rule, soundness or precision bound, task-validity check, termination protocol, runtime, memory, convergence or benchmark result. It supports a parallel analysis direction, not demonstrated faster or trustworthy reachability conclusions.

**Source and location**

Evidence tier: Primary captured official DAC description plus existing chapter level reachability discussion; no full paper extraction, formal soundness reproduction or benchmark validation. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH896)

DAC 2026 official description; captured Problem, Mechanism / artifact, Workload, Hardware, Baseline, Measurements and Limits fields; record RESEARCH896; no manuscript pages.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** serial approximate reachability

exact reachability

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH896

**Hardware or process assumptions:** Multicore or accelerator formal-analysis platform; synchronization assumptions are unspecified.

**Limits:** No soundness, precision, runtime, memory, convergence, or benchmark results are reported.

Approximation may miss relevant states.

Official description only; formal and benchmark validation is required.

**Method or artifact:** Parallel complementary approximate-reachability algorithm.

**Metrics:** Reachability-analysis efficiency is claimed qualitatively

**Problem:** Approximate reachability analysis can be computationally expensive for large transition systems.

**Workload or benchmark:** Transition systems and formal reachability tasks; abstraction, solver, and hardware are unspecified.

</details>

## What remains to establish

Resolve unspecified workloads, comparison methods, resource budgets, and source locations before generalizing a reported gain. Multiple papers in this selected sample permit comparison of mechanisms, but do not by themselves establish recurrence across years or a long-term trend.

[All subthemes](../expanded-taxonomy-v1.md) · [Research directions](../directions/README.md)
