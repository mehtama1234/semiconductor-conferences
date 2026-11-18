## Start with the question, not the inherited category name

This page contains ten captured paper records. The inherited subtheme name does not mean that every paper proves a formal property. Some construct proof tasks, some accelerate checking, some generate code or assertions, and others help locate faults. The earlier overview discussed only three records. The map below now exposes all ten; all ten papers have received an individual comprehension pass in this chapter.

This is a reading map based on the captured records, not a new source assessment or an accepted taxonomy reassignment. Original classifications remain unchanged pending mechanism-level review. The paper cards retain their evidence limits.

| Start with this question | Captured papers to inspect | Distinction that controls the conclusion |
|---|---|---|
| Do two combinational implementations agree? | [Factored-form sharing](#paper-dac-2026-research1388); [sweeping-based task scheduling](#paper-dac-2026-research285) | Faster search is useful only for the same equivalence obligation |
| What property should be checked? | [ATLAS](#paper-dac-2026-research2886); [Svacoder](#paper-dac-2026-research2361) | Generating an assertion is not proving that it captures the intended requirement |
| Can training produce better RTL candidates? | [Insights from Verification](#paper-dac-2026-research2737); [EARL](#paper-dac-2026-research1612) | Training feedback is not independent acceptance of the generated circuit |
| What structure or fault should be examined? | [Hierarchical Boundary Recovery](#paper-dac-2026-research1638); [Debug Like a Human](#paper-dac-2026-research1355) | Recovered structure and suspected causes need validation against behavior |
| What execution or safety bound holds? | [Beyond Exact](#paper-dac-2026-research1552); [probabilistic safe controller synthesis](#paper-dac-2026-research720) | The bound depends on the modeled machine, environment and uncertainty |

### A useful property can still be too weak

Consider an illustrative interface that must acknowledge every accepted request within two cycles. A property saying that every acknowledgment has a preceding request checks a different direction. It forbids unsolicited acknowledgments. It does not require any acknowledgment to occur. A circuit that never acknowledges can satisfy that property while failing the intended service requirement.

Even the right implication can pass for an unhelpful reason. If the model assumes requests never occur, a request-to-acknowledgment property has no triggering case. This is vacuity: the condition is satisfied without exercising the behavior the reader intended to examine. The check needs both a valid requirement and an environment that permits relevant events.

That is why assertion generation belongs next to proof methods but is not interchangeable with them. Read [formal and functional verification](../observed-subthemes/formal-and-functional-verification.md) for adjacent assertion and verification records. Neither category label establishes that the generated properties are sufficient, nonvacuous or independently reviewed.

### A reduced representation must preserve the relevant behavior

Synthesis can combine or remove logic that was separate in the source description. Recovering recognizable modules can make inspection easier, but the recovered boundary need not be the unique original design boundary. Multiple decompositions can represent the same function. Matching an expected label is therefore different from proving a valid correspondence.

Similarly, a debugging slice keeps selected parts of a trace or design for inspection. Suppose a wrong output is produced in block B. An earlier control signal from block A selected the wrong operand. A slice containing only B's arithmetic may omit the cause even if it includes the visibly incorrect result. The important evaluation is whether the reduced context preserves evidence needed to identify and confirm the fault.

These are independent examples, not observed failures of the named papers. They explain why structure-recovery accuracy, fault-localization accuracy and proof validity need separate measures. A ranked suspect is not a confirmed bug. Confirmation requires a reproducible failing behavior and an explanation tied to the intended requirement.

### Bounds need a stated population of behaviors

The longest runtime observed in a finite test set is a measurement. It is not automatically an upper bound over all allowed executions. A worst-case argument must cover the allowed branches, data-dependent work and machine behavior within its scope. Excluding interference can yield a valid bound for an isolated kernel without establishing the same bound under shared execution.

A probabilistic safety statement has another boundary: it describes risk under a model and distribution. A one-step violation bound does not automatically become an unchanged bound over an arbitrarily long run. Take an illustrative sequence of one hundred events. Each has violation probability at most 0.001 under the relevant model. The union bound then permits a total violation probability as large as 0.1. Independence is not needed for that upper bound. Stronger conclusions require additional evidence or assumptions.

### Follow the connection without collapsing the tasks

For proof representation, generalization and parallel solver work, continue to [formal and equivalence verification](../observed-subthemes/formal-and-equivalence-verification.md). For training reward versus functional acceptance, the expanded [VERIRL explanation](../observed-subthemes/llm-assisted-design-flows.md#explanation-iccad-2025-110) supplies a conceptual connection. It is not evidence about EARL or Insights from Verification. Related papers must not fill missing target-specific methods or results.

Beyond Exact, ATLAS, the factored-form sharing paper, Insights from Verification and EARL now have individual paper explanations in this chapter. So do Hierarchical Boundary Recovery, Debug Like a Human, Svacoder, HydraCEC, and probabilistic safe controller synthesis. All ten records have received the same paper-level pass. The explanations are based on accepted manuscripts, preprints, or—where explicitly marked—the official conference description. The cards retain their evidence limits. This is still not a longitudinal trend: the records span different verification questions and are not a matched time series.

<span id="explanation-dac-2026-research1552"></span>

## Beyond Exact: what the bound means and how it is constructed

### The question is an upper bound over allowed GPU executions

The paper asks for the worst-case execution time (WCET) of one GPU thread block. WCET is not the longest runtime seen in a test run. It is an upper bound over every execution that the timing model permits. The distinction matters because a GPU can make different timing choices even when the source kernel is unchanged. Threads inside one warp can take different branch outcomes. Warps can contend for the same execution resources in different orders.

The target is a thread block made of (M) warps running on one sub-core. A sub-core contains functional units such as floating-point and special-function units. An instruction may need one of these resources for a period of time. While that resource is occupied, another instruction needing the same resource cannot start. The model also assumes one instruction issue per cycle, program-order issue within a warp, dependency-respecting issue, and no memory-related contention. Loop bounds are assumed to have already been obtained by static analysis or supplied by an engineer. These are not incidental implementation details: the resulting bound is only a bound for executions inside this model.

### Why branch divergence defeats the obvious longest-path argument

GPU warps execute threads in a lockstep-style SIMT model. When all threads take the same branch, the warp executes one branch path. When different threads take different branches, the paths are executed serially with lane masks. The warp executes the work for one group of lanes and then the work for the other group. Thus a warp may execute more basic blocks than any one thread's individual path suggests.

The paper's small control-flow example makes the issue concrete. If every thread takes the first branch, the warp executes three unit-time blocks. Suppose some threads take the first branch and the rest take the second. Both branch bodies are then executed and the warp takes four units. That extra work alone is not the difficult part. The difficult part is interaction between warps. A shorter warp can release or request a shared resource at a different time, changing which warp blocks another warp. Therefore “make every warp follow its longest individual path” does not necessarily produce the longest thread-block completion time.

The paper calls this a timing anomaly. A scenario containing shorter warp paths can finish later than the scenario in which every warp follows the longest path. The reason is global scheduling, not a claim that a shorter path is locally slower. A local reduction in work can change resource contention and increase idle or blocked time elsewhere. This is why a finite set of measured executions cannot establish the WCET claimed by the paper. Nor can a single assumed path per warp.

### The paper's first model: instructions become resource intervals

The method starts from a control-flow graph and an instruction model. For each instruction, static analysis identifies data dependencies and the resource it needs. The model separates three events: issue, resource start, and completion. An instruction can be issued only after its dependencies complete. It starts when its resource is available. It holds that resource for the modeled access duration while continuing for its modeled execution duration.

The paper then abstracts a warp's instruction sequence into alternating intervals:

- A critical section is an interval in which the warp exclusively occupies a modeled execution resource.
- A non-critical section is an interval in which the warp occupies none of those modeled resources.

For each possible branch-divergence path, the paper constructs a sequence of these intervals. The set of all possible sequences is written as (Lambda). A concrete scenario chooses one path from (Lambda) for each of the (M) warps. It also chooses an admissible interleaving under the scheduler. The block response time is the finish time of the last warp.

This reduction is useful because it exposes the two quantities that determine the bound. Critical intervals consume mutually exclusive resource time. Non-critical intervals can overlap across warps. There can also be a period in which all unfinished warps are simultaneously non-critical. The paper calls this latter quantity the global non-critical time.

### The exact bound under a deliberately weak scheduler model

For any concrete scenario, the response time is exactly the sum of its critical-section duration and its global non-critical-section duration. The paper then bounds those two parts separately. The critical contribution is bounded by the longest critical duration of any possible warp path multiplied by (M). The global non-critical contribution is bounded by the largest non-critical duration of any possible path. It cannot exceed the non-critical time of the warp that finishes last.

This gives the paper's work-conserving bound:

\[
R = C(Z^*_{\lambda^\dagger}) \times M + C(Z_{\lambda^\dagger})
\]

Here (\lambda^\dagger) is the path with the largest critical and non-critical totals under the paper's model. (C(Z^*)) is total critical duration. (C(Z)) is total non-critical duration. The important point is not merely the equation. The paper proves exactness under its scheduling assumption. If the scheduler is only required to be work-conserving, there exists an admissible execution scenario that reaches this bound. “Exact” therefore means exact relative to the modeled instruction/resource behavior and the set of work-conserving schedules. It does not mean that every GPU scheduler will realize the scenario or that the model includes every hardware effect.

The proof constructs one warp using the longest path. It arranges the other warps so that they keep the longest-path warp blocked while preserving equal critical duration. This is possible because the work-conserving assumption leaves many execution orders admissible. The same freedom permits the exact worst-case construction. It also makes the result conservative for a real implementation whose scheduler follows more structure than the model records.

### The tighter bound adds a scheduling constraint, then solves a longest path

The second contribution narrows the set of allowed execution orders. The paper represents critical and non-critical sections as graph nodes. Edges preserve the order inside each warp. Between different warps, the work-conserving model permits many relative orders of critical sections, represented by bidirectional edges. The paper replaces those choices with directed edges that impose a topological order. This produces a directed acyclic graph (DAG).

The tighter bound is the sum of node durations on the longest path of that DAG:

\[
\widetilde{R} = \sum_{v \in V} C(v)
\]

This works in the paper's model because warps can execute in parallel. Each node's finish time is determined by its predecessors and its own duration. The longest path therefore bounds the makespan. The imposed ordering removes schedules that were technically allowed by the weak work-conserving model. These are not intended to occur under the proposed constrained execution policy.

The constraint is a substantive assumption, not a free mathematical improvement. The paper discusses realizing it through scheduler support, semaphores, synchronization, or compiler/code instrumentation. Such mechanisms can add overhead and may not be available on a given GPU. The manuscript does not implement them or measure that overhead; it evaluates the benefit analytically. Consequently, the tighter number is useful as a design target for a predictable execution policy. It is not by itself evidence that an unmodified commercial GPU will obey the required order.

### What the evaluation actually establishes

The authors evaluate the two bounds with a lightweight synthetic simulator and a static model of 22 Rodinia kernels. The hardware parameters for the benchmark study come from an NVIDIA Quadro K620 with Maxwell GM107 architecture at 1072 MHz. Arithmetic and memory latencies are measured with microbenchmarks. Each kernel is modeled as one block on a sub-core. The synthetic study generates 1,000 thread blocks per configuration and fixes the longest path's total duration at 1,000. It reports the relative reduction ((R-\widetilde{R})/R).

The synthetic results show why the constraint helps most when non-critical sections are substantial. More of that work can overlap under the DAG ordering. With more warps, the gap first grows and can then shrink when critical sections dominate and reduce parallelism. Increasing the number of path nodes increases the gap in the tested low-critical-section setting. These are trends in the paper's generated model, not universal laws for all GPU kernels.

In the Rodinia study, the critical-section share averages 7.60%. The constrained analysis is lower than the work-conserving exact bound for all 22 listed kernels. The average reduction is 19.13% and the maximum is 39.39% for `particle_kernel`. The table also reports large variation: `kmeans_kernel_c` improves by 2.45%, while `particle_kernel` improves by 39.39%. The paper reports bound values, not measured end-to-end deadlines, energy, area, or a deployed safety case.

### Acceptance conditions and unresolved boundary

To accept the result for a real system, a reader must establish at least four links. The paper itself does not complete them. First, the instruction and resource abstraction must cover the target GPU's relevant timing behavior. This includes any omitted memory or interference effects. Second, the branch-path and loop-bound inputs must be sound for the actual kernel inputs. Third, the proposed warp-order constraint must be enforced by the hardware, compiler, or inserted synchronization. This must not invalidate the timing model through its own overhead. Fourth, the thread-block bound must be composed with other blocks, sub-cores, memory traffic, preemption, and the system deadline. This applies if the intended claim is system-level predictability.

The paper is therefore a rigorous model-level result with a clear trade. Removing path assumptions requires considering divergent scenarios. Tightening the bound requires adding an execution-order assumption. Its central contribution is not simply the reported 19.13% reduction. It is the explicit separation between two bounds. One is exact under a broad scheduler model. The other is smaller and becomes available only after the admissible scheduler behavior is restricted.

**Primary source read:** [accepted manuscript at White Rose Research Online](https://eprints.whiterose.ac.uk/id/eprint/242555/1/DAC26_GPU_Kernel_WCET_2_.pdf), especially the abstract and Sections 1–5 (PDF pages 2–7). It includes Figure 1, Lemmas 1–2, Theorem 1, Figure 4, and Table 1. The paper record is [White Rose record 242555](https://eprints.whiterose.ac.uk/id/eprint/242555/), DOI `10.1145/3770743.3804186`.

<span id="explanation-dac-2026-research2886"></span>

## ATLAS: how a security concern becomes a checkable property

### The paper addresses a missing translation step

Security verification has a different starting problem from ordinary functional verification. For a functional feature, the design team can often state an expected input/output behavior. It can then write a test or property against it. For security, the question begins earlier. What must be protected? Who may interact with it, through which interface, and under what privilege? What sequence would constitute a violation? If those decisions are not made explicitly, a formal tool can prove a property that is precise but irrelevant.

ATLAS is a framework for making that translation more systematic. Its input is not only RTL. It combines vulnerability knowledge, an SoC-specific asset inventory, a threat model, and three kinds of design context. Its output is a set of design-specific SystemVerilog Assertions and a JasperGold script that runs those properties on the RTL. The paper's claimed contribution is therefore a pipeline from a known weakness category to a candidate formal obligation. It is not a new formal decision procedure for proving arbitrary security requirements.

### The basic security terms must remain separate

ATLAS uses five distinct elements in its threat-model template:

- An adversary describes who can act and what access or capability that actor has.
- An asset is the data, state, control, or logic whose confidentiality, integrity, or correct operation must be protected.
- An attack surface is the interface through which the adversary can reach or influence the asset.
- A vulnerability is a weakness in the design, such as an incorrect access-control condition or an invalid state transition.
- A threat is the harmful exploitation of that weakness by an adversary.

The separation is operational. A debug register is not itself a threat. It may be an asset or attack surface. An improper privilege check is a vulnerability. An unauthorized debug operation is a threat outcome. If these are collapsed into one label, the generated assertion can lose the condition that makes the security claim meaningful.

The paper illustrates the template with CWE-1245, improper finite-state-machine logic. Its example records a simple hardware adversary. It records hardware state and logic integrity as the asset, and interfaces and state-machine logic as attack surfaces. It records an insecure FSM as the vulnerability. It records exploitation of undefined or insecure transitions as the threat. This template gives the LLM a fixed place to state each part. It does not ask the LLM to infer an entire security argument from a short RTL fragment.

### The threat-model database turns general weakness knowledge into reusable structure

CWE describes classes of weaknesses, CVE records concrete vulnerability instances, and CAPEC describes attack patterns. These sources are useful. But they do not directly tell a checker what must be constrained in a particular SoC. That means which signal, state, privilege mode, or reset condition. ATLAS builds a threat-model database (TMDB) to supply that missing intermediate representation.

The authors first manually create high-quality examples using the template. GPT-5 then generates additional hardware-CWE threat models using the examples, CWE entries, related CVEs and CAPEC links. Human feedback reviews and refines the outputs. The resulting JSON dataset stores the template fields, adversary descriptions, instructions, and example input/output mappings. The paper says the database covers the known hardware-design CWE set and makes it available through a public repository.

This construction has two separate quality dependencies. The database can improve consistency only if its CWE-to-threat interpretations are correct. It can improve coverage only if the mapping from a CWE to an SoC asset and attack surface is appropriate. A large database is not evidence that every stored threat model is complete. A generated threat model is not yet a proof obligation.

### Asset-centric analysis narrows the search before property generation

ATLAS defines seven broad asset types. They are sensitive data, boot integrity, and attestation data and measurements. They also include parametric data, privileged system resources, shared resources, and runtime integrity and state resources. It associates definitions and signal-name cues with each type. For example, `key_`, `secret_`, and `protected_` can suggest sensitive data. In contrast, `debug_`, `mode`, `valid_`, `dma_`, `grant_`, and `crossbar_` can suggest privileged or shared resources.

The LLM examines the buggy RTL with the generic definitions and the TMDB. It identifies concrete signals, explains their role, and then searches the threat models for relevant weaknesses. In the DMA example, the output identifies control-state registers, progress vectors, physical-memory-protection gates, and handshake or abort controls. It then maps the relevant asset and keywords to candidate CWEs. Examples are improper FSM logic, incorrect defaults, or improper access control on aliased regions.

This is a pruning and hypothesis-building step. It reduces the set of properties worth attempting. It does not prove that an asset was found. It does not prove that no asset was missed. It also does not prove that every matched CWE applies. A keyword match can be useful evidence for a review queue while still being an insufficient security argument.

### Three context sources provide different facts

ATLAS then generates properties using three complementary views of the SoC:

1. Design documents state intended architecture, register maps, interface semantics, privilege rules, trust boundaries, modes, and lifecycle behavior. They supply facts that may not appear in RTL. Examples are why a signal is security-sensitive or which actor is allowed to drive it.
2. An abstract syntax tree (AST) extracted with Yosys or PyVerilog/Slang exposes the implemented structure. This covers signals, drivers, dependencies, state encodings, fan-in, fan-out, and control/data paths. It helps bind a general weakness to actual RTL objects.
3. A security-focused RTL summary describes assets, guards, policies, critical registers, and code-level conditions. It is itself LLM-generated, so it is a useful additional view but not an independent human specification.

The paper's central claim is that these views answer different questions. The AST helps identify where a state or control path exists. Documentation helps determine what the path is supposed to mean and who may use it. The RTL summary highlights security-relevant implementation details that a general document may omit. The framework intersects these cues to form a concrete property hypothesis. It does not ask an LLM to guess from raw code alone.

The Figure 5 DMA example shows the failure mode without this context. Given RTL and a threat model alone, the LLM produces a property. That property does not correctly represent the FSM security condition. With AST, design documentation, and RTL summary, it recognizes the relevant states and the abort signal. It also recognizes the intended escape behavior and the trust boundary. It then produces an assertion checking that an abort state does not persist when `done_i` is low. The example demonstrates contextual improvement for that case; it does not show that every generated property is correct.

### Assertion generation and formal checking are different gates

ATLAS emits SystemVerilog Assertions bound to real signal names, state values, reset behavior, and interface conditions. It also emits a Tcl harness for Cadence JasperGold. The harness compiles the design, applies assumptions and constraints, and runs formal checks. The result may be a proof, a counterexample, or an inconclusive outcome. The framework allows up to three refinement iterations for a bug; persistent inconclusive cases are sent for manual review.

The paper adds non-vacuity cover properties as guideposts for assertion generation. This matters because an implication can pass without checking the intended behavior if its antecedent never occurs. A cover demonstrates that the triggering situation can be exercised in the formal model. It does not by itself prove that the antecedent represents every relevant attack condition. Likewise, a counterexample shows that the generated property is violated. It still requires interpretation to decide whether the violation is the intended security bug or an invalid assumption.

The acceptance chain is therefore:

1. The threat model must identify the correct asset, adversary, attack surface, and weakness.
2. The generated assertion must express the intended security condition without omitting required modes, resets, privileges, or temporal behavior.
3. The formal environment must permit the relevant attack sequence and constrain only behavior that is genuinely unavailable.
4. A proof, counterexample, or inconclusive result must be interpreted against the intended design contract.

Formal completion at step four cannot repair an incorrect decision at step one. This is the central limit on reading the paper's accuracy numbers.

### What the evaluation measures

The evaluation uses three OpenTitan-based HACK@DAC benchmark suites from 2018, 2019, and 2021. The paper describes 48 relevant CWEs across the suites. ATLAS identifies 39 of them. For those detected cases, it generates correct security properties for 33. That is more than 82% of the 39 detected cases. The denominator is not all possible SoC vulnerabilities. “Correct property” is the paper's benchmark assessment rather than an independently reproduced judgment here.

The paper also reports that ATLAS can identify multiple relevant CWEs for one bug. This is not automatically an error: access control and privilege enforcement can describe overlapping aspects of one weakness. But it means that CWE count, bug count, property count, and successful proof count are different quantities. They should not be added together.

The ablation study separates the TMDB from the three SoC contexts. Without the TMDB, the LLM detects 6/20, 3/11, and 4/17 cases on the three benchmarks. With the TMDB, ATLAS detects 17/20, 11/11, and 11/17. The paper then reports that using only one context yields at most five accurate properties. The full context combination adds 10, 4, and 6 correct properties for the three benchmarks. These are described as roughly 3×, 2.3×, and 2.5× improvements. These comparisons support the paper's claim that structured threat knowledge and combined context both matter. They do not isolate every prompt, model, token, review, or formal-runtime cost.

### Boundary of the result

The paper's strongest evidence is an end-to-end benchmark demonstration. It uses known benchmark bugs, a structured threat database, contextual property generation, and JasperGold checking. Its weakest implied interpretation would be that ATLAS has solved SoC security verification. It has not established that the TMDB is complete. It has not established that asset detection has high recall on unseen designs. It has not established that generated properties are free of false positives or vacuity. It has also not established that the reported benchmark properties transfer to proprietary SoCs.

The use of GPT-5 and human feedback in TMDB construction also creates a provenance question. The evaluation tests the resulting pipeline, but it does not make every knowledge-base entry independently auditable from the benchmark table. The three benchmark suites are valuable because they contain real design bugs and golden references. They are not a representative sample of all SoC architectures, adversary capabilities, or security requirements.

ATLAS is best understood as a structured front end to formal security verification. It addresses the costly translation from general vulnerability knowledge to candidate design-specific properties. It improves that translation by forcing explicit security roles and by combining specification context with implemented structure. The formal tool still proves only the resulting property under its assumptions. The paper's durable idea is this separation of responsibilities. Threat knowledge chooses what to ask. Design context determines how to state it. Formal analysis checks the stated question.

**Primary source read:** [ATLAS arXiv version 2](https://arxiv.org/pdf/2603.01170), especially Sections 1–5 (PDF pages 1–6), Tables 1–4 and Figures 2–6. The DAC DOI is `10.1145/3770743.3804400`; the source record is [arXiv:2603.01170](https://arxiv.org/abs/2603.01170). The public TMDB is linked by the paper as [Threat-Model-Database-for-Hardware-Security](https://github.com/KimiaTasnia/Threat-Model-Database-for-Hardware-Security); it was not independently executed or audited here.

<span id="explanation-dac-2026-research1388"></span>

## Factored-form sharing: what is being parallelized in equivalence checking

### The obligation comes before the speedup

Combinational equivalence checking asks whether two combinational logic networks produce the same outputs for every allowed input assignment. “Combinational” means that the output at a time depends on the current inputs and internal logic, not on stored state from an earlier clock cycle. The two networks may have very different internal structure after synthesis or technology mapping. But the acceptance question remains behavioral. For each input vector, do the corresponding outputs agree?

A common way to turn that question into a satisfiability problem is to build a miter. Corresponding outputs are compared. The comparisons are combined into a condition that is true when at least one output differs. The checker asks whether there exists an input assignment that makes the miter true. If the formula is satisfiable, the assignment is a counterexample to equivalence. If the formula is unsatisfiable, the modeled circuits agree for the outputs and input assumptions encoded in that formula.

This logical direction is important. A faster solver does not establish a stronger equivalence property. The result is useful only if several things are preserved. These are the same two networks, output correspondence, input constraints, black-box treatment, and timeout interpretation. The paper's contribution is about reducing the time needed to solve the equivalence workload. The official description does not establish a change to the equivalence semantics.

### Why a large equivalence problem has two different costs

SAT-based checking represents logic as a Boolean formula, commonly in conjunctive normal form (CNF). A formula has two separate sources of cost. First, encoding a circuit into clauses creates literals and relationships that consume memory and construction time. Second, the SAT solver must choose variable assignments and propagate consequences. Some choices quickly force a contradiction. Others create a large search tree before the solver can decide whether a counterexample exists.

Parallelizing this workload is not just a matter of splitting the gates evenly. Two partitions with the same number of gates can have different numbers of repeated signals, clauses, and difficult branching points. If each worker independently rebuilds the same logic encoding, parallel workers may duplicate the largest cost. Suppose a partition contains an unusually hard SAT subproblem. Other workers can then finish early while one worker determines the total runtime.

The paper proposes factored form literal count (FFLC) as a structural estimate of both shareable literal/CNF encoding and branching complexity. A factored representation expresses Boolean logic while retaining common subexpressions instead of expanding every repeated term separately. The official description says FFLC is combined with a lightweight branching-complexity proxy. Together, these estimates guide partitioning so that the method seeks two goals at once. These are to reuse repeated encoding work and to balance estimated SAT difficulty.

The exact FFLC definition and the branching proxy formula are not available in the public conference description. Nor are the conditions under which the estimate tracks solver time, or the encoding-reuse implementation. They must not be reconstructed as if they were established by the paper record. What is established is the design intent: the partitioner uses a representation-sensitive cost rather than only circuit size.

### Seed-and-grow partitioning has a specific role

The method uses a sharing-aware seed-and-grow algorithm. A seed is an initial unit of logic assigned to a partition. The algorithm then grows that partition by adding related logic. It chooses additions according to the estimated benefit of sharing and the estimated effect on SAT difficulty. The goal is not merely to make contiguous chunks. It is to preserve common factored structure where reuse is valuable. It must also prevent one worker from accumulating a disproportionate branching burden.

This creates a three-way constraint. A partition must contain enough related logic to make reuse worthwhile. It must remain small enough to execute concurrently with other partitions. It must also preserve the global equivalence obligation. A local check must be connected to the original miter. The connection must make all local results sufficient for the full result. The official description names the partitioning strategy and its cost signals. It does not provide the formal condition proving that every partitioned result is equivalent to checking the original problem.

The phrase “sharing” therefore needs careful reading. It can refer to sharing factored literals, reusing CNF encoding, or avoiding repeated derivation across parallel tasks. It does not mean that the circuits being compared are allowed to share behaviorally unequal outputs. Any implementation that changes the formula without preserving the miter's satisfiability result would be a different verification problem.

### What a correct parallel decomposition must preserve

For a partitioned CEC flow to be sound, the decomposition needs at least these properties:

- Every output-difference condition in the original miter must remain represented.
- Shared intermediate logic must retain the same Boolean meaning in every worker that uses it.
- A local satisfiable result must map back to a valid global counterexample. Otherwise the method must explain how local counterexamples are combined.
- An unsatisfiable collection of local checks must imply unsatisfiability of the original miter, rather than only prove several weakened formulas.
- Input assumptions and treatment of unmatched or cut signals must be identical across the compared methods.

These are acceptance conditions for the task, not claims that the available description proves each one. The current source record does not expose the paper's formal soundness argument. It also does not expose handling of cross-partition dependencies or behavior when a partition times out. Those gaps matter more than a headline speedup because equivalence checking is a correctness gate. An acceleration that silently weakens the obligation is not an equivalent improvement.

### How to read the reported comparisons

The official DAC description reports an implementation in ABC evaluated on large-scale benchmarks using 40 physical CPU cores. It reports geometric-mean speedups of 45.57× over single-threaded ABC, with a maximum of 6,595×. It reports 1.53× over a state-of-the-art CPU-parallel method, with a maximum of 17×. It reports 5.52× over a state-of-the-art GPU-parallel method, with a maximum of 382×.

Geometric-mean speedup summarizes multiplicative ratios across cases. It is not the same as an arithmetic average. It does not reveal whether every case improved. The maximum values identify the most favorable case, not a typical case. The description does not report absolute runtimes, solved and timed-out counts, memory consumption, benchmark names, core utilization, or GPU hardware. It also does not say whether all baselines used equivalent preprocessing and resource budgets. Therefore the strongest supported statement is that the authors report substantial benchmark speedups under their stated comparison setup. It is not that the method universally reduces verification time by 45.57×.

The CPU comparison also needs resource accounting. “40 physical CPU cores” identifies the proposed implementation's CPU capacity, but the public description does not give the exact core count, memory, or parallel settings for each baseline. A fair comparison requires matched circuit instances, preprocessing, timeout, number of workers, and memory limit. It also requires stating whether a baseline's encoding cost is included. Without those details, the result is a promising performance claim with unresolved reproducibility conditions.

### The paper's place in the formal-verification map

Factored-form sharing addresses solver throughput after the equivalence obligation has been formed. It does not replace miter construction, output correspondence, input modeling, or proof interpretation. It is complementary to the other equivalence paper in this chapter, which targets sweeping-task scheduling. That paper and this one should not be combined into one speedup. They may alter different stages of the checking flow.

The paper's conceptual contribution is to treat structural representation as part of parallel scheduling. Circuit size alone is too weak a predictor of SAT work. Repeated structure and branching behavior affect both encoding and search. A useful implementation must exploit that structure without changing the Boolean question. The central unresolved evidence is exactly the bridge between those two claims. The public description reports the cost model and benchmark speedups. It does not report the formal decomposition proof or enough experimental detail to reproduce the comparison.

**Primary source read:** [official DAC 2026 paper description](https://63dac.conference-program.com/presentation/?id=RESEARCH1388&sess=sess163). It states the CEC problem, FFLC and branching proxy, and sharing-aware seed-and-grow partitioning. It also states the ABC implementation, 40 physical CPU cores, and the reported geometric-mean and maximum speedups. No public manuscript, equation-level method description, benchmark list, absolute runtime table, or reproducible artifact was recovered in this pass. The explanation therefore keeps those boundaries explicit. The DAC session places the paper in the “From SAT to IC3: Modern Proof Techniques for Hardware Correctness” session.

<span id="explanation-dac-2026-research2737"></span>

## Insights from Verification: how testbench evidence changes RTL generation

### The target is executable behavior, not token similarity

The paper starts from a mismatch in ordinary language-model training. Supervised fine-tuning (SFT) teaches a model to predict the next Verilog token from a specification and previous tokens. That objective rewards similarity to the training code. It does not directly ask whether the complete generated module compiles or responds correctly over time. It also does not ask whether it handles reset and control sequencing, or satisfies the testbench's expected outputs.

For hardware, those distinctions matter. Two Verilog descriptions can use different names, structures, and coding styles while implementing the same behavior. Conversely, a generated description can look close to a reference and still fail. One state transition, width, reset value, or clock relationship may be wrong. The paper therefore uses executable testbench outcomes as a training signal. Its system is called VeriPrefer. It first trains a model to generate Verilog. It then uses testbench feedback to construct preference pairs. Finally it applies direct preference optimization (DPO).

The goal is not to prove generated RTL equivalent to the reference design. The goal is to increase the probability that generated RTL passes the available functional tests. That is a meaningful engineering objective, but its scope is bounded by the testbench and its assumptions.

### Stage one creates the initial generator

The first training stage uses specifications paired with Verilog code. The specification format is deliberately more detailed than a short one-line prompt. It includes module purpose, ports and widths, and internal working principles. It also includes timing behavior, signal relationships, implementation logic, and important internal signals. The paper constructs this dataset from PyraNet and filters out empty descriptions. It retains the top two quality levels, leaving 86,672 entries from an original 692,238.

The model minimizes token-level maximum-likelihood loss. In plain terms, it is rewarded for assigning high probability to the reference code token by token. This stage is necessary because the later preference stage assumes the model can already produce compilable and reasonably structured candidates. It is not sufficient for functional correctness, because no complete behavior score appears in the SFT objective.

### The paper's main artifact is the testbench-generation pipeline

The authors identify a data problem: public Verilog datasets often contain specifications and code without a usable testbench. Without testbenches, there is no executable signal for ranking generated candidates. They therefore generate testbenches in four stages: Analyze, Draft, Improve, and Rectify.

In Analyze, an LLM reads the specification and extracts the most important functional points and test cases. The pipeline limits the output to the top three functional points and top five test cases to avoid repetitive generation. In Draft, another prompt creates a testbench. The testbench instantiates the design, applies clocks, resets and stimuli, and prints expected and actual values for every case. Compilation is checked with Synopsys VCS; compiler errors are returned to the generator for another attempt.

In Improve, VCS coverage reports identify lines not exercised by the draft. The testbench generator adds cases aimed at uncovered lines. It continues until the coverage threshold is met or the attempt limit is reached. The paper's example uses a 90% line-coverage threshold. Line coverage is a structural measure. It indicates that statements executed. It does not show that all input combinations, temporal sequences, protocol interleavings, or security conditions were checked.

In Rectify, the generated testbench is run against the original Verilog implementation. The pipeline compares the expected values written by the LLM with the actual simulation outputs. If they disagree, the mismatch is sent back to the LLM so it can correct the testbench. The loop ends when all test cases pass against the original code. It also ends after three failed correction iterations, in which case the instance is discarded.

This last step prevents obvious self-inconsistent testbenches from becoming training data, but it creates a precise boundary. The original code is treated as the reference while the testbench is corrected. A testbench can therefore be internally consistent with the original code. It can still omit an untested requirement, encode a mistaken specification, or fail to exercise a rare behavior. Passing Rectify means the generated testbench agrees with the selected reference executions. It does not establish that the reference implementation is fully correct.

### Preference pairs convert test results into a training signal

After testbench generation, the SFT model produces two candidate Verilog programs for the same specification. Both candidates are compiled and run under the generated testbench. If one passes more test cases, it becomes the preferred output (y^+); the other becomes the less-preferred output (y^-). Pairs in which either candidate fails to compile are discarded. The resulting record contains one specification and an ordered pair of generated programs.

DPO trains the model to increase the relative probability of (y^+) against (y^-). It keeps the updated model near a fixed reference model. It does not require a separate reward model. This matters because a numeric reward such as “fraction of test cases passed” can be optimized through shortcuts. These shortcuts do not improve the intended behavior. The paper compares DPO with explicit-reward approaches and argues that pairwise preference avoids some reward-hacking pressure.

The preference signal still inherits the testbench's blind spots. If both candidates pass the same incomplete tests, the pair contains little information about the omitted behavior. Suppose a testbench is biased toward the reference code's structure. The model may then learn implementation-specific patterns rather than the general specification. If a candidate passes more tests because it exploits an unmodeled assumption, DPO can reinforce that behavior. The paper's method improves alignment to the measured executable signal. It does not turn that signal into a complete correctness specification.

### The paper measures syntax and function separately

The evaluation uses pass@k with 20 sampled programs per specification. Syntax pass means the generated code compiles. Function pass means it passes the benchmark testbench. The metric pass@1 estimates the fraction of tasks solved by the first sample. The metric pass@5 estimates whether at least one of five samples succeeds. A higher pass@5 can coexist with a lower pass@1 because the metric rewards the chance of finding one successful sample.

The paper evaluates VerilogEval-Machine (143 GPT-created tasks) and VerilogEval-Human (156 manually crafted tasks). It also evaluates RTLLM v1.1 (29 designs). It evaluates RTLLM v2 (50 designs across arithmetic, memory, control and miscellaneous categories) and VerilogEval v2. It trains several foundation families, including CodeLlama, DeepSeek-Coder, CodeQwen, Mistral and Qwen2.5-Coder.

For a concrete result, on RTLLM v2 the Qwen2.5-Coder-14B VeriPreferRL model reaches function pass@1/pass@5 of 55.2/67.5. The figure is 53.8/67.5 for its VeriPreferSFT version. On VerilogEval v2, the same model reaches 58.6/72.1 versus 57.9/71.1 after SFT. The gains are not uniform across every model and benchmark. Some syntax or pass@5 values decrease. The paper itself notes weaker performance on VerilogEval-Machine because the preference-training specifications are more human-like than that benchmark's prompts.

The broader headline is therefore not the claim “DPO always improves every number”. It is that testbench-based preference training often improves functional pass rates across model families and benchmark formats. The largest reported gains depend on the model and task distribution.

### Dataset and compute conditions determine what transfers

The RL-stage source pool filters SFT examples longer than 50 lines, leaving 8,291 instances. The automatic pipeline produces 6,704 valid testbenches. The final preference-pair counts range from 1,782 for the Mistral variant to 2,267 for Qwen2.5-Coder-14B. Training uses eight NVIDIA A100 80 GB GPUs. Fine-tuning runs for three epochs at a learning rate of (10^{-5}); DPO runs for ten epochs at (5\times10^{-6}), with (eta=0.1).

These conditions separate data generation from model inference. At inference time, only the natural-language specification is provided. The testbench is used during training and evaluation. It is not an additional input to the deployed generator. The reported improvements therefore test whether the model has absorbed a relation. That relation is between specification patterns and behavior measured by the training testbenches. They do not measure the cost of generating a testbench for each future user request. They also do not guarantee that a new design's unseen behavior will be covered.

### The ablations test the source of the improvement

The paper compares several ways of constructing preference pairs. BLEU measures token overlap with reference code. AST and data-flow-graph similarity measure structural similarity. A testbench-based pair instead uses the number of functional cases passed. In Table VII, the Qwen2.5-Coder experiment obtains RTLLM v2 function pass@1/pass@5/pass@10 of 52.4/66.4/69.0 with VeriPreferRL. The figures are 49.3/58.4/62.1 for a DPO variant using testbench rewards. They are 49.2/60.5/63.1 for AST-based preferences. On VerilogEval v2, VeriPreferRL obtains 49.3/64.7/69.5, while the testbench-reward DPO variant obtains 45.4/59.4/62.1.

The table also shows that SFT on verified data alone does not reproduce the full result. Its RTLLM v2 function pass@1/pass@5/pass@10 is 49.7/61.9/65.4. This is close to the 49.8/62.5/66.1 VeriPreferSFT baseline. This supports the paper's claim that the preference objective, not just filtering or adding successful samples, changes the training signal.

The ablation is informative but not a complete causal isolation. The pair-construction methods have different numbers of usable pairs, different failure handling, and potentially different data distributions. The authors report that dataset size alone does not explain the result. Independent reproduction would need the released data, exact sampling, training settings, testbench versions and evaluator behavior.

### Why lower perplexity is not the same as better RTL

The paper compares language-model perplexity with testbench performance. It finds that only 52.3% of code pairs have the expected ordering. In the expected ordering, the candidate that passes more tests also has lower perplexity. This is a direct demonstration of the objective mismatch. Perplexity evaluates token likelihood under a distribution; functional testing evaluates selected executions of a hardware module. Neither metric subsumes the other.

The result should not be overextended. A low testbench pass rate does not prove that a module is wrong under every input. A high pass rate does not prove full correctness. A strong evaluation needs held-out specifications, independently constructed testbenches, coverage beyond lines, and multiple seeds or sampling budgets. When the design is safety-critical, it also needs formal properties or equivalence checks. These must not be generated solely from the same candidate and testbench loop.

### What this paper establishes

The paper establishes a concrete way to feed executable verification outcomes into RTL-generator training. It contributes a decomposed testbench-generation pipeline and a filtered preference-pair construction procedure. It also contributes DPO alignment, and benchmark results showing improved functional pass rates in many settings. It also supplies a public implementation and data/model release for reproduction.

It does not establish that the generated Verilog is formally correct. It does not establish that the generated testbenches are complete. It also does not establish that line-coverage thresholds imply behavioral coverage. Nor does it establish that the model understands hardware intent independently of the training distribution. Its first-principles lesson is narrower and useful. If the desired output property is behavioral correctness, token imitation is an indirect objective. Executable feedback can make the training signal closer to that property. But the feedback mechanism becomes part of the correctness boundary.

**Primary source read:** [arXiv:2504.15804 v1](https://arxiv.org/pdf/2504.15804), especially Sections I–V and VII (PDF pages 1–9), Figures 1–7 and Tables I–VII. The official implementation is [CatIIIIIIII/VeriPrefer](https://github.com/CatIIIIIIII/VeriPrefer). The paper's DAC 2026 record is listed by [CityUHK Scholars](https://scholars.cityu.edu.hk/en/publications/insights-from-verification-training-a-verilog-generation-llm-usin/). The source was read but the released training pipeline was not executed here.

<span id="explanation-dac-2026-research1612"></span>

## EARL: why update only the uncertain parts of an RTL sequence

### The training problem is credit assignment in structured code

An RTL generator produces a long sequence of tokens, but those tokens do not all make equally important decisions. Module declarations, punctuation, repeated keywords and fixed port syntax are often predictable once the surrounding specification is known. A sensitivity list, conditional guard, state transition or data-path operation can determine how the circuit reacts over time. Suppose a generated module fails a compiler or functional check. A reward attached to the complete sequence does not directly say which positions caused the failure.

Standard reinforcement learning with verifiable rewards can propagate the same sequence-level learning signal through every generated token. EARL argues that this spends update capacity on predictable tokens and weakens credit assignment at structural decisions. Its proposed answer is to measure the model's uncertainty at each generation position and selectively update the high-uncertainty positions.

This is a claim about training efficiency and where the gradient is applied. It is not a claim that high entropy is itself a correctness proof. It is also not a claim that every high-entropy token is functionally important.

### Entropy is measured at a position, not assigned to a word

For generation position `t`, the paper defines entropy as the sum below. `p[t,v]` is the probability assigned to vocabulary item `v` at position `t`.

```text
H[t] = - sum over v of p[t,v] * log(p[t,v])
```

The value describes how spread out the model's next-token distribution is in that particular context. The same lexical token can have low entropy in one context and high entropy in another. For example, the word begin may be nearly forced after one syntax pattern but ambiguous at a structural junction.

The paper studies entropy with a fine-tuned DeepSeek-Coder model at temperature 1.0. Across more than 210,000 generated tokens, over 80% have entropy below 0.15 and only a small tail exceeds 0.6. The high-entropy positions in the examples cluster around sensitivity triggers, conditional branches and data-path operations. Module headers, port lists, whitespace and closing syntax tend to be low entropy. The paper interprets this as evidence that uncertainty is concentrated near choices that can alter control flow or module structure.

The observation is descriptive. It shows correlation between model uncertainty and certain RTL locations in the studied corpus. It does not by itself establish that changing those positions causes the measured functional improvement. The training experiment is needed to test that hypothesis.

### EARL has four connected stages

First, the authors construct synthetic specification–Verilog–testbench triples. GPT-4 generates problems across arithmetic operators, sequential logic, control modules and algorithmic circuits, varying difficulty, circuit type and specification style. Each sample is filtered by three checks. These are compilation with iverilog, functional execution of the paired testbench, and an additional grading-LLM assessment of functional behavior. Only samples that pass all three are retained.

Second, a pre-trained code model receives supervised fine-tuning on those verified triples. This supplies syntax and interface structure before reinforcement learning begins. In the reported experiment, the base model is DeepSeek-Coder-7B. SFT runs for three epochs with a peak learning rate of 0.00005.

Third, the model generates RTL rollouts and receives a cascaded verifiable reward. Candidates that fail syntax receive zero reward. Candidates that compile are checked for interface consistency, including module name and port declarations. Candidates with aligned interfaces proceed to functional equivalence checking using the Yosys eqy engine against a reference implementation. Passing candidates receive the highest reward; near-misses receive lower graded credit.

Fourth, EARL applies the entropy mask inside policy optimization. For each response, it computes the entropy of every generated position and chooses a response-level quantile threshold. A token receives a policy-gradient update only when its entropy is at or above that threshold. Low-entropy tokens are left at zero update weight, preserving the stable distributions learned during SFT. The method is optimizer-agnostic in formulation; the paper instantiates it with PPO and DAPO, and the main experiment uses DAPO.

The threshold is relative to each response rather than a single global entropy number. This controls for different prompts having different entropy scales. The paper also imposes a group condition requiring both positive and non-positive rewards so group-normalized advantages remain meaningful. EARL is therefore not simply “train on tokens with a fixed entropy greater than X”. It is a response-relative selective policy update combined with multi-stage verification rewards.

### Why the reward hierarchy matters

Syntax, interface and functional equivalence are different gates. Syntax validity says the candidate can be parsed and compiled. Interface consistency says it exposes the expected module and ports. Functional equivalence says its outputs match a reference under the equivalence engine's modeling assumptions. A candidate can pass the first two and fail the third. The cascade prevents the system from spending expensive functional-checking work on malformed candidates. It also gives the optimizer intermediate information when a candidate is close.

The hierarchy also defines the reliability boundary. The eqy result is only as strong as the reference design, equivalence setup, black-box treatment, input assumptions and tool semantics. A passing check is not automatically a synthesis-quality, timing, power or security result. The dataset filtering has a similar limitation. A sample passes the paired testbench and grading step, not every possible input sequence.

### What the benchmark numbers mean

EARL evaluates VerilogEval-Machine (143 machine-generated prompts), VerilogEval-Human (156 expert-written prompts), and RTLLM v1.1 (29 diverse RTL prompts). It reports pass@1 and pass@5, with five completions per prompt in this paper's evaluation formula. “Functional” means the benchmark's functional checker accepts the output; “syntax” means it compiles. A pass@5 increase does not mean every generated module is correct. It asks whether at least one of up to five samples succeeds.

Table 1 reports EARL with a 7B model at 72.9/83.9 pass@1/pass@5 on VerilogEval-Machine and 49.6/60.2 on VerilogEval-Human. It reports 68.9 functional pass@5 on RTLLM. On RTLLM, the paper compares 68.9 with 54.2 for the best listed RL baseline. The same comparison lists 51.7 for the best listed SFT baseline. It describes the corresponding differences as 14.7 and 17.2 percentage points. It also reports 100% syntax pass@5 on RTLLM.

The paper reports improvements across its listed table. But the comparison is not a single model-versus-model experiment for every baseline. Some baselines have different parameter counts, training data, prompting procedures, and evaluation provenance. The numbers support a benchmark improvement under the paper's setup. They do not establish a universal 14.7-point gain for all RTL generators or a guarantee of one-pass correctness.

### The entropy ablations test whether selection is doing work

The paper compares plain PPO and DAPO, entropy weighting, and EARL's binary entropy mask. It reports that DAPO is stronger than PPO without entropy masking, and that entropy-aware variants improve over their unmasked counterparts. The best DAPO-EARL configuration improves pass@1 over the SFT baseline by 5.2 percentage points in the cited analysis.

The quantile study is more direct. At quantile 0.0, the model obtains VerilogEval-Machine pass@1/pass@5 of 72.7/83.2 and RTLLM functional pass@5 of 62.0. At 0.8, the corresponding values are 72.9/83.9 and 68.9. At 0.9, they fall to 71.0/79.7 and 65.5. The authors interpret the peak near 0.8 as a balance. Lower thresholds admit too many low-value updates. Higher thresholds exclude useful decision positions.

This ablation supports the value of choosing a minority of positions in the tested setting. It does not prove that 80% is a universal threshold. The optimal quantile can depend on tokenizer, model size, prompt style, code length, reward sparsity and training stage. Entropy is also model-dependent: a well-calibrated model and an overconfident model can assign different entropy to the same structural uncertainty.

### Acceptance conditions and unresolved questions

To accept EARL as a reliable RTL-generation method for a new flow, a reader must verify several boundaries. The synthetic triples must represent the target design styles and must not leak reference implementations or evaluator-specific patterns into training. The reward's equivalence check must use an independent and correctly configured reference. The entropy mask must improve learning rather than merely change sampling or preserve syntax at the cost of diversity. Benchmark prompts and testbenches must be held out from data generation. Finally, generated RTL must pass downstream synthesis, timing, power, lint, formal properties and human design review. This applies if those are part of the intended acceptance process.

The paper does not establish all of those conditions. It reports functional benchmark results and training stability, not physical implementation quality or independent formal acceptance of every output. Its central conceptual contribution is narrower. In structured RTL sequences, applying the same policy-gradient update to every token may waste learning signal. Uncertainty-guided selection can focus optimization on structural choices. This holds provided the verifiable reward is itself sound and the selective update does not hide errors in low-entropy regions.

**Primary source read:** [EARL arXiv version 2](https://arxiv.org/pdf/2511.12033), especially Sections 1–5 (PDF pages 1–6), Figures 1–5 and Tables 1–2. The source gives the entropy definition, quantile mask, reward cascade and dataset checks. It also gives the 4× NVIDIA A100 80GB setup, benchmark tasks and ablations. The anonymized implementation link in the preprint was not executed here. The DAC page and later author materials identify the work as a DAC 2026 paper.

<span id="explanation-dac-2026-research1638"></span>

## Hierarchical Boundary Recovery: what synthesis removes and what recovery must reconstruct

### The problem is lost organization, not missing logic

An RTL design usually has named modules and explicit instance boundaries. Synthesis transforms that description into a gate-level netlist to optimize area, timing, power or other implementation objectives. During this process, it can flatten module instances, merge equivalent signals and duplicate logic. It can also remove buffers, propagate constants and rewrite Boolean expressions. The resulting netlist can implement the same input/output function while no longer containing the signal that marked the original boundary.

This creates a practical problem. A flat netlist still contains the logic. But it no longer tells an engineer which gates belong to a high-level component. Debugging becomes harder because a failing signal cannot be mapped cleanly to a specification block. Engineering-change-order work becomes harder because a local change has no obvious implementation region. Cross-abstraction training and verification also lose the correspondence between the specification and its synthesized implementation.

Hierarchical Boundary Recovery addresses this organizational loss. It attempts to recover a boundary for a high-level component in a gate-level netlist. This includes cases where synthesis has completely removed the original boundary signals. The target is not to recreate the exact historical RTL text. It is to find implementation nodes. Their external behavior and position in the surrounding logic must correspond to the specification component's boundary.

### A boundary has inputs, outputs and a behavioral cut

A useful boundary separates the logic inside a component from the logic around it. Boundary inputs are signals entering the component; boundary outputs are signals leaving it. Suppose the component is replaced or inspected independently. The boundary must then expose enough information for the outside logic to continue behaving as before.

The important word is enough. A recovered set of gates that merely looks spatially compact is not necessarily a valid boundary. It must form a cut through the relevant logic cones. Paths from primary inputs toward the component should cross the proposed boundary in a controlled way. So should paths from the component toward its outputs. The recovered implementation boundary may contain nodes that never existed as named signals in the original hierarchy.

This is why the task is different from naming or graph clustering. Naming can suggest that two signals correspond. Structural clustering can group nearby nodes. Boundary recovery needs a relation between the specification boundary and the implementation's Boolean behavior. It must also cope with optimization that changes the shape of the logic. Exact graph isomorphism is therefore too strong a requirement.

### SAT sweeping supplies behavioral correspondences

SAT sweeping is a method for finding nodes in a Boolean network that compute equivalent functions. The tool represents the networks as logic graphs and proposes candidate pairs using structural information. For a candidate pair, it asks a SAT solver a question. The question is whether there exists an input assignment that makes the two node values differ. If no such assignment exists under the modeled inputs, the nodes are equivalent. If a satisfying assignment exists, the pair is rejected and the assignment is a counterexample to that node equivalence.

Boundary recovery uses these equivalent-node pairs as correspondence evidence. It can compare nodes in the hierarchical specification netlist with nodes in the flattened implementation. This works even when the nodes have different names or occur at different structural locations. A node may have more than one equivalent counterpart, for example after logic sharing or duplication. That ambiguity is part of the recovery problem; selecting one match does not make the mapping unique.

The method then combines the behavioral correspondence with structural analysis. For each specification boundary output, it searches for implementation nodes that form an appropriate cut through the relevant fanout cone. It performs an analogous analysis for boundary inputs. The candidate implementation nodes whose corresponding specification nodes create the required cut become the extended recovered boundary.

The phrase “extended boundary” matters. Synthesis may remove the exact original signal. The method can then move the boundary toward surrounding logic. It continues until it finds a set of nodes for which the required cut and equivalence relationships are available. That can produce a usable region for debugging or ECO work. This holds even when the result is not the smallest or most historically faithful boundary.

### Why equivalence alone is not enough

Suppose a specification boundary signal and an implementation node are functionally equivalent at one point in the design. That correspondence does not automatically define a valid component boundary. The node may be downstream of logic that should belong outside the component. Or it may fail to separate all paths entering and leaving the intended region. Conversely, a structurally plausible cut may contain nodes whose Boolean functions do not match the specification boundary.

The method therefore has two obligations:

- Behavioral correspondence: matched nodes must agree for all modeled input assignments.
- Cut validity: the selected nodes must separate the target component's relevant transitive fan-in and fan-out paths.

The first obligation is a SAT question. The second is a graph and cone-structure question. Passing one does not imply passing the other. This separation explains why a method can recover a useful boundary. It does so without claiming that the recovered gates are an exact copy of the source module.

### What the method can and cannot preserve

The method is strongest when the logic outside the target instance remains equivalent between the specification and implementation. In that case, a change or replacement inside the recovered boundary can be related to the original hierarchical component. The relation goes through the surrounding logic. The method becomes more difficult when synthesis uses transformations that rely on the component's context.

Two important cases are logic sharing and satisfiability don't-cares. Logic sharing can cause one implementation node to correspond to several specification nodes. Replacing one region may then affect another use of the shared logic. A satisfiability don't-care can let the synthesis tool change a function. This applies on input assignments that never occur at a boundary output. A local comparison may appear valid under the reachable context. A proposed replacement may still change behavior under assignments that the original context excluded. These cases require the boundary to be extended or the surrounding assumptions to be analyzed.

The practical consequence is that “recovered boundary” is not synonymous with “original module recovered”. It is a behavioral and structural interface candidate. This holds under the equivalence and reachability assumptions used by the method. A downstream ECO or debug tool must recheck the modified netlist. This matters especially when logic is shared or the synthesis flow exploits don't-care conditions.

### Why this helps downstream work

Debugging needs a way to move from a failing gate-level signal back to a meaningful specification block. A recovered boundary can limit the search region and restore the unit of reasoning that synthesis removed. ECO flows can use it to identify which implementation nodes correspond to a requested high-level change. Cross-abstraction model training can use recovered pairs to associate specification-level concepts with gate-level structures. Verification can use the boundary to define a smaller region while retaining connections to the surrounding netlist.

These are applications of the recovered correspondence, not evaluations of the recovery itself. A boundary that is useful for debugging may be too broad for a low-cost ECO. A boundary that is behaviorally valid may not match the labels expected by a training dataset. Each application needs its own acceptance criterion.

### Evidence and evaluation boundary

The DAC description states that the approach is automated and handles cases where synthesis removes original boundary signals. It states that the approach is implemented as an open-source tool. It also states that it shows robust experimental recovery of hierarchical boundaries. The authors' Berkeley publication page identifies the work as a DAC 2026 paper. Those sources establish the problem, intended mechanism and existence of an implementation.

The accessible record does not provide the target paper's benchmark names, synthesis scripts, or recovered-boundary precision or recall. It also does not provide SAT runtime, timeout policy, scale limits, number of ambiguous matches, or cross-tool validation. It also does not establish whether “robust” means high recovery accuracy, stability across synthesis settings, runtime scalability, or all three. The numerical quality of the target paper therefore remains unverified in this reading pass.

The related boundary-recovery problem has a natural evaluation structure. Compare recovered implementation boundaries with known specification boundaries. Measure behavioral equivalence of matched cuts. Report failures under increasingly aggressive synthesis. Measure SAT and structural-analysis cost. The target paper must be judged by its own experiments and definitions. These are the conditions a reader should look for. They are not results attributed to this paper without its manuscript.

### What this paper establishes at the current evidence level

Hierarchical Boundary Recovery addresses a real gap created by synthesis: behavior can survive while design organization disappears. Its method combines SAT-based functional correspondence with structural cut analysis to infer an implementation boundary. This includes one whose original signal was removed. That is a technically coherent bridge between equivalence checking and hierarchy recovery.

The current evidence does not establish that every recovered boundary is unique, minimal, semantically complete, or safe for an ECO. It does not establish the target's recovery accuracy or runtime from the available pages. The correct reading is therefore as follows. The paper presents an automated boundary-recovery approach and an open-source implementation with claimed robust experiments. The mechanism is plausible and well-defined at the conceptual level. Quantitative acceptance and corner-case behavior require the manuscript, artifact and independent checks.

**Primary sources read:** [DAC 2026 official description](https://63dac.conference-program.com/presentation/?id=RESEARCH1638&sess=sess312), which states the synthesis-obscurity problem, removed-boundary case, automation, open-source implementation and robustness claim. Also [Alan Mishchenko's publication list](https://people.eecs.berkeley.edu/~alanmi/publications/), which identifies the paper and authors. The target manuscript, benchmark tables and artifact execution were not recovered in this pass. The related prior boundary-recovery literature was not substituted for target-paper measurements.

<span id="explanation-dac-2026-research1355"></span>

## Debug Like a Human: why processor fault localization needs an instruction-time slice

### The task is to rank code blocks, not to prove the bug

Fault localization starts after a verification run has found a failure. The result is a failed instruction and a signal whose architectural value is wrong. It also includes a simulation time and an expected value or behavior. The task is to rank source regions that may contain the cause. An engineer can then inspect and repair them. This is different from bug detection. The failing test establishes that some observed behavior disagrees with the reference. It does not identify which source statement caused the disagreement.

The distinction matters in a processor because one instruction is implemented across multiple modules and clock cycles. A wrong committed value may be produced by a combinational expression or selected by a control signal from another block. It may also be held in a register because a write-enable was wrong one cycle earlier. A source-only search sees code text but not which values were active for the failing instruction. A waveform-only search sees values but not a compact, semantically grouped source context. BluesFL is designed to connect these two views.

### Why ordinary slicing and full-file prompting lose information

Static slicing follows data dependencies from a suspicious signal and returns statements that could influence it. This can be useful for a small module. But a processor contains many connected modules. The resulting set can remain too large for careful inspection. Transition-based methods can remove statements that were not active in a cycle, but a pipelined instruction spans cycles and modules. A range-based coverage interval can therefore mix the failing instruction with other instructions that are in flight.

The other failure mode is excessive context. Giving an LLM a whole processor project or a long module file does not make the model understand the design. It increases the number of unrelated declarations and possible causes it must consider. The relevant signal may be separated from the failure by both module boundaries and clock cycles. The paper's design response is to restrict the model's view. It uses two kinds of information. These are local dataflow and the dynamic path of the failing instruction.

### Code blockization preserves local dataflow

BluesFL first partitions the SystemVerilog project into disjoint code blocks. A block is a set of source lines, and a line belongs to one block. The method records an input-signal set and an output-signal set for each block. This gives the later analysis a concrete rule for moving from a signal to the source block that computes it.

The block types reflect synthesizable SystemVerilog structure:

- A module-input block represents an input port and the connected signals at its instantiation.
- A module-output block represents the signals connected to an output port.
- An `always` block groups the signals assigned on its left-hand sides and the signals used on right-hand sides or conditions.
- An assignment block begins with one continuous assignment. Assignment blocks are merged when their input and output sets have a dataflow dependency.

The merge rule is important. Arbitrarily splitting every assignment would produce small pieces that omit the local expression needed to interpret a value. Grouping dependent assignments keeps related computation together while retaining a mapping from signals to source regions. It does not claim that each block is a hardware module or a true bug boundary. It is an analysis unit chosen for context control.

### Blues reconstructs an instruction execution path

The central object is a directed graph whose node is `(block, time)`. The timestamp is a clock-cycle count from the simulation start. A block may occur more than once at different times because a sequential block can be covered repeatedly. The graph is therefore not just a static dependency graph. It records when a value for the failing instruction can have been produced.

The algorithm starts with the failing signal and its time. It finds the block that drives that signal. It identifies the signals inside that block that drive the current value. It then finds the blocks that produce those signals and adds predecessor nodes. It repeats this backward traversal until no earlier state can be added. The edges represent data dependence for the particular instruction and time under analysis.

The time rule distinguishes combinational and sequential behavior. For combinational logic, a signal at time `t` is driven by its inputs at `t`. For a clocked block, the value at `t` is normally computed from inputs at `t-1`. This holds when the assignment was active at the preceding edge. If the assignment was not active, the register retains its earlier value. The prior value of the register becomes the predecessor rather than an unrelated input. This retained-value case is necessary because “no write” is itself a state transition rule.

### The LLM receives a constrained debugging interface

At each `(block, time)` state, the model receives the current code block and the failing test report. It also receives the driven signals identified by the slice. It can mark a block as suspicious or request the blocks that drive selected signals. It can also read waveform values at relevant times. The allowed signal queries are restricted to the execution path. The model therefore cannot expand arbitrarily through every signal in the project. The final output is a ranked list of suspicious blocks with confidence scores.

This arrangement separates deterministic preprocessing from probabilistic reasoning. The parser, blockizer and slice decide which source and runtime states are eligible for inspection. The LLM decides which eligible signals deserve attention and whether a block appears causally suspicious. The ranked result is a localization hypothesis, not a proof that the highest-ranked block is defective. Confirmation still requires inspecting the source, reproducing the failure, and checking the repair against the intended processor behavior.

### What the experiment measures

The evaluation uses the open-source Ibex RISC-V core, approximately 19 thousand lines of SystemVerilog. The authors inject 119 bugs using mutation rules and run CoreMark in a co-simulation flow. A failing architectural-state comparison supplies the instruction, signal and time used by the localization process. The paper evaluates how many injected bugs have at least one buggy block. The block must be within the top 1, top 5 or top 10 ranked positions.

BluesFL localizes 24 bugs at Top-1, 28 at Top-5 and 28 at Top-10. The comparison table reports 7, 7 and 7 for LiK, the strongest listed LLM-specific baseline. It reports 13, 16 and 16 for the adapted Agentless baseline. The reported Top-1 improvement over LiK is 242.9 percent relative to the baseline count. It is not a 242.9-percentage-point accuracy guarantee. The table also reports 0 Top-1 for Cirfix, Strider and Tarsel-Jaccard, 3 for Tarsel-Tarantula, and 2 Top-10 for Tarsel-Ochiai.

The ablations test the two dynamic inputs separately. Removing waveform signal values reduces the result to 13 Top-1, 24 Top-5 and 26 Top-10. Removing the instruction execution path reduces it to 5, 6 and 6. The paper also reports that 99 percent of the generated Ibex blocks contain no more than 200 lines. It also reports that the default setup checks an average of 15.4 blocks per bug. Without signal values it checks 88.3 blocks, raising reported average cost from $0.257 to $1.821, a 609 percent increase.

The backend comparison changes the result and cost. GPT-4o-mini reports 17/25/26 at Top-1/5/10 for $0.015 per bug. GPT-4o reports 24/28/28 for $0.257. Claude-3.5-Sonnet reports 30/33/33 for $0.263. These figures are conditional on the paper's injected-bug set, prompt/tool protocol, model versions and scoring rule. They do not establish performance on naturally occurring processor bugs or on another ISA.

### Limits that control the conclusion

The benchmark is mutation-based and concentrated on one RISC-V implementation. Mutation rules determine which bug mechanisms are represented; 119 injected failures are not a sample of all processor defects. The comparison also uses block-level ranking conventions. Slicing methods receive an expected rank derived from set size. LiK emits a single line. Those conversions affect cross-method comparability and should be reproduced with the released artifact.

The method depends on a test report, a co-simulation reference, signal coverage and waveform values. It also depends on a parser that correctly maps SystemVerilog dataflow. If the reference model or test does not expose the failure, the method has no initial state to trace. A bug may depend on a signal omitted from the recorded waveform, a wrong path classification, or a cross-instruction interaction. The slice can then exclude relevant evidence. The paper reports a finding about bugs not localized within Top-10. For approximately 70 percent of them, the buggy block was never checked because the LLM terminated too early. That is a limitation of the search policy, not evidence that the bug was absent from the execution path.

The paper also identifies possible data exposure to pretrained models. It injects bugs to reduce the chance that the model has memorized the exact test cases. This does not prove no training contamination. Finally, cost is an API/model-use estimate under the reported setup. It is not a complete engineering cost including waveform generation, parser construction, simulation, human confirmation or repair.

### What this paper establishes

Debug Like a Human gives an LLM a structured, time-indexed view of a processor failure. Its technical contribution is the combination of dataflow-based source blocks, instruction-oriented backward slicing, waveform values and tool-constrained LLM reasoning. The reported Ibex experiment supports a narrower conclusion. This combination improved the paper's injected-bug Top-N localization counts. It also reduced reported model-query cost relative to its listed baselines under the stated setup.

It does not establish a general fault-localization guarantee or causal correctness of the top-ranked block. It also does not establish superiority on natural bugs. Nor does it establish independence from the quality of the co-simulation trace and mutation benchmark. A strong follow-up evaluation would need naturally occurring bugs and multiple processor designs or ISAs. It would need matched model and budget settings and per-bug failure analysis. It would also need independent confirmation that the proposed block is the repair-relevant cause.

**Primary source read:** [arXiv:2605.17290](https://arxiv.org/abs/2605.17290), version 1 PDF, Sections 1–6 and Tables 1–2. It includes the blockization definitions, Blues algorithm, Ibex benchmark, ablations, model comparison, limitations and threat-to-validity discussion. The public artifact is linked by the paper at [github.com/pointerliu/bluesfl](https://github.com/pointerliu/bluesfl); it was not executed in this pass.

<span id="explanation-dac-2026-research2361"></span>

## Svacoder: why assertion generation needs both RTL grounding and semantic filtering

### An assertion is a temporal requirement, not just legal syntax

SystemVerilog Assertions describe conditions over signals and clock cycles. An assertion can require a relationship in the same cycle or a relationship on a later cycle. It can require a response after a request or a reset condition. It can also require a value to remain stable while an enable is inactive. Small changes in implication direction, delay, grouping or operator precedence can change the property being checked.

The NL2SVA task takes a natural-language property and RTL context and produces an SVA. A generated assertion may compile. It may even pass formal verification against the design. It can still fail to express the requested property. The simplest example is a tautology such as `assert property (1'b1)`: it passes for every RTL implementation but checks nothing useful. A second failure is a weaker property that the RTL happens to satisfy. Thus three questions must be separated. Is the SVA syntactically valid? Does it hold for the design under the tool's model? Does it mean what the natural-language requirement says?

Svacoder, named CodeV-SVA in the manuscript, addresses the data problem behind this translation. The paper does not propose a new SVA logic. It constructs training pairs and fine-tunes open models. The models then have more exposure to RTL structure, temporal properties and the syntax needed to express them.

### RTL provides a large source of candidate verification situations

Human-written SVA corpora are small. The paper starts instead with open-source RTL and specifications from the CodeV dataset. It uses Yosys to retain designs with clock and reset signals. These signals create temporal behavior that can support nontrivial assertions. From 165,000 RTL examples, 42,000 are retained after this filtering.

DeepSeek-V3.1 decomposes each design specification into independent natural-language verification properties. This produces 324,000 candidate properties. The same model receives each candidate property and its RTL implementation and generates an SVA. Cadence JasperGold then checks whether the generated assertion holds under the RTL. The first formal screen leaves 159,000 SVA instances.

That screen answers only one question: whether the RTL satisfies the candidate assertion. It does not prove that the SVA is the intended translation of the natural-language property. A design can satisfy an assertion that is too weak, vacuous or unrelated. The paper's central data-quality contribution is therefore a second semantic-alignment check.

### Bidirectional translation tests whether meaning survives two conversions

For a screened SVA, the pipeline asks an LLM to translate SVA back into natural language. It then asks the LLM to translate that natural-language description back into a new SVA. The original and regenerated SVAs are compared with formal equivalence under the same RTL context. Only pairs whose assertions are logically equivalent are retained. This produces 105,000 NL-SVA pairs with corresponding RTL code before later refinement.

The logic is conditional. If the round trip changes the assertion, some information was likely lost in one of the translations. Suppose it preserves the assertion. The natural-language intermediate was then at least sufficient for the LLM to reconstruct an equivalent property under the checked model. That is stronger than checking only that the first SVA passes. It is not a proof that the natural-language sentence is complete for every human interpretation. Equivalence is checked between formal assertions, not between the sentence and an independently formalized specification.

The paper's precedence example shows why this filter matters. An original SVA can appear to express two conditional requirements. Operator precedence may make the conjunction bind differently. This produces a tautology that passes formal verification. The back-translated SVA expresses the intended grouped conditions; formal equivalence fails, so the pair is rejected. The filter detects a mismatch between the original assertion and its recovered meaning. It does not by itself repair the original assertion or establish which wording a domain expert intended.

### Refinement removes easy or ambiguous training examples

After bidirectional selection, the pipeline applies three further operations. First, DeepSeek-V3.1 uses expert-derived error categories to select cleaner pairs. The categories are logical misalignment, signal inconsistency, RTL misunderstanding and mapping a property to the wrong SVA object. Second, Qwen3-8B generates five candidate SVAs for each natural-language property. Examples for which all candidates are equivalent to the reference are removed as too easy. Third, DeepSeek-R1 generates a reasoning trajectory and a final SVA. It retains cases whose final SVA is equivalent to the selected assertion.

The resulting 83,000 examples contain RTL, a natural-language property, reasoning text and an SVA. Qwen3-8B and Qwen3-14B are fine-tuned for two epochs, with a learning rate of 2e-5, batch size 128 and 32,768-token context. Training is reported as 8 and 12 hours on eight H800 80GB GPUs for the two model sizes. The deployed model is still a generator: formal tools remain necessary to test each assertion against its design context.

### What Func.@k measures

The paper evaluates on FVEval's NL2SVA-Human and NL2SVA-Machine sets. The Human set contains expert-written ground-truth SVAs and natural-language descriptions. The Machine set starts from randomly generated SVAs and uses LLMs to create descriptions. Human experts recheck, correct or remove erroneous cases. The paper applies 13-gram decontamination to reduce training/test overlap.

The metric is functional pass@k. For each problem, the model produces samples. A sample is counted correct only when the generated SVA is formally equivalent to the ground-truth SVA. This holds under the benchmark setup. Func.@1 is the probability that one attempt is correct. Func.@16 and Func.@32 measure the chance that at least one correct assertion appears. The sample sizes are 16 or 32. A high pass@32 can therefore coexist with a lower first-attempt reliability. It does not mean that every generated assertion is correct.

CodeV-SVA-14B reports NL2SVA-Human Func.@1/16/32 of 75.8/89.4/90.4 and NL2SVA-Machine of 84.0/94.9/95.8. CodeV-SVA-8B reports 72.0/88.8/90.4 and 83.5/96.3/97.2. The table compares these results with GPT-5, DeepSeek-R1, GPT-4o, specialized RTL-generation models and Qwen3 base models. The reported numbers use temperature 0.8, top-p 0.95 and 32 samples for pass@k estimation. They measure formal equivalence to benchmark assertions, not coverage of all design requirements.

The data ablations support the pipeline's internal claims. With 5,000 examples, the paper reports synthesized data at 55.4 Func.@1 on Human and 75.7 on Machine. Under the same comparison, the figures are 22.3 and 39.2 for DeepCircuitX data. They are 1.9 and 6.4 for VERT data. Removing reasoning trajectories lowers CodeV-SVA-8B Human Func.@1 from 72.0 to 63.9. Removing bidirectional selection as well as later refinement gives 51.2, while removing formal verification too gives 44.1. These are ablations of a single training pipeline. They do not isolate every source of data quality from model or prompt effects.

### End-to-end results add a different denominator

The paper also modifies AssertionForge for five RTL designs. A specification-analysis stage produces natural-language properties, and the NL2SVA stage generates assertions. Table 5 reports the number generated, the number syntactically correct and the number that pass formal verification. On OPENMSP430 with GPT-4o as the specification stage, GPT-4o NL2SVA produces 1,013 generated, 777 syntax-correct and 196 proven assertions. CodeV-SVA-8B produces 1,044, 859 and 484. With DeepSeek-R1 as the specification stage, the corresponding CodeV-SVA-8B row is 1,215 generated, 917 syntax-correct and 502 proven.

These counts should not be read as a percentage of all required properties. The specification stage may omit requirements. Syntactic validity does not imply semantic alignment. “Proven” means the assertion passes the formal check used by the framework. The table is evidence that the specialized generator produced more accepted assertions under that pipeline. It is not evidence that the five designs' full verification plans were covered.

### Limits that determine the conclusion

The synthetic data inherits the source RTL, generated specifications and teacher-model judgments. The initial formal screen can admit weak assertions. Bidirectional equivalence can preserve a wrong but internally consistent assertion if the round-trip translation reproduces it. LLM-as-a-judge and difficulty filtering introduce additional model decisions. The benchmark's ground-truth SVA is the acceptance reference. The metric therefore does not independently judge whether that reference is complete. It also does not judge whether a different correct assertion should also be accepted.

The RTL context also constrains what is visible. A property about an external protocol or an environment assumption may not be expressible from the selected code and prompt. The same holds for reset sequencing or an unmodeled interaction. Passing JasperGold depends on clock, reset, assumptions, property syntax and tool semantics. The paper reports models and aggregate benchmark results. It does not establish hardware implementation quality, synthesis impact, assertion runtime at deployment scale, or the cost of expert review.

### What this paper establishes

Svacoder shows that RTL-grounded synthetic data plus round-trip assertion equivalence can train smaller open models. These models perform strongly on the paper's NL2SVA benchmarks. The strongest technical point is a separation. It separates “the design satisfies this SVA” from “this SVA remains equivalent after its meaning is translated out and back”. The method reduces a particular class of weak or misaligned training pairs. The ablations show that this filtering is associated with better benchmark scores.

It does not establish that generated assertions cover the full design intent. It does not establish that a formally passing assertion is nonvacuous. It also does not establish that the model can replace verification engineers. The appropriate acceptance test for deployment remains as follows. Review the requirement and inspect the generated temporal semantics. Check assumptions and vacuity. Run the formal tool on the intended RTL. Measure whether the assertion suite detects relevant injected and real bugs.

**Primary sources read:** [arXiv:2603.14239](https://arxiv.org/abs/2603.14239), version 1 PDF, Sections 1–5 and Tables 1–5. Also read: [DAC 2026 official description](https://63dac.conference-program.com/presentation/?id=RESEARCH2361&sess=sess166) and [public CodeV-SVA artifact and evaluation instructions](https://github.com/wyt2000/CodeV-SVA). The repository was inspected through its public README but the JasperGold evaluation and model training were not executed here.

<span id="explanation-dac-2026-research285"></span>

## HydraCEC: why parallel equivalence checking must parallelize the sweep itself

### The proof obligation is unchanged; the work schedule changes

Combinational equivalence checking asks whether two combinational circuits produce the same outputs for every allowed input valuation. A solver can encode the comparison as a miter. Corresponding outputs are compared, and a SAT solver searches for an input that makes any comparison differ. If the miter is unsatisfiable, the circuits are equivalent under the modeled inputs. If it is satisfiable, the assignment is a counterexample.

Modern equivalence tools often simplify this problem through SAT sweeping. The circuits are represented as Boolean graphs. The tool proposes pairs of nodes that may compute the same function. It asks a SAT query to distinguish them. It merges or records equivalent nodes when the query proves no difference. Every successful merge can simplify later queries. The order in which tasks run therefore changes the structure and cost of the remaining work.

This creates a distinction between two forms of parallelism. A solver may run several SAT searches for one candidate pair in parallel, while the outer sweep remains serial. HydraCEC targets the outer sweep: it executes multiple verification tasks concurrently and lets completed tasks share equivalence information asynchronously. The equivalence requirement remains the same; only the order and concurrency of proof work change.

### A sweep task has benefit as well as cost

Not every available candidate pair is equally valuable. A task can be cheap but produce little simplification. Another can be expensive but merge nodes that remove a large amount of later work. A useful scheduler therefore needs to estimate the benefit of completing a task, not only its local runtime.

The paper introduces a Task Benefit Graph (TBG) to guide dynamic scheduling. At a conceptual level, the graph represents candidate verification tasks, their dependencies and the simplification benefit expected from their results. The scheduler chooses tasks whose predicted equivalence information is likely to reduce downstream work while respecting dependencies and available workers. The accessible conference description does not provide the graph's exact vertex/edge definition, benefit estimator, update equations or dependency rules. Those implementation details must therefore not be inferred from the name alone.

The benefit estimate is important because sweeping is state-changing search. Running tasks in parallel can consume resources on pairs that would have become unnecessary after another merge. A scheduler that ignores this interaction can increase contention or duplicate work. A benefit-aware scheduler attempts to spend concurrency where the result will simplify the shared problem.

### Asynchronous sharing removes a global barrier

Suppose workers wait for every task in a round to finish before sharing equivalences. Fast workers then sit idle. Newly discovered simplifications cannot affect tasks already waiting in the next round. A global barrier also makes the schedule sensitive to the slowest task in each batch.

HydraCEC uses asynchronous equivalence sharing. A worker can publish a newly established equivalence without waiting for all other workers. Other workers can incorporate that information while continuing their own tasks. The intended effect is cooperative simplification without global synchronization at every step.

Asynchronous sharing has a correctness condition. A shared equivalence must be sound under the same Boolean model and must be applied consistently. It also has a scheduling condition. Tasks that were generated before a merge may become stale. The implementation must decide whether to cancel, revalidate or tolerate them. The official description establishes the presence of asynchronous sharing but does not expose these stale-task policies or their overhead.

### What the paper claims to improve

The reported framework is HydraCEC, described as a general-purpose parallel CEC framework for SAT-sweeping flows. Its stated contribution is to parallelize the sweeping process itself, add dynamic benefit-aware scheduling through TBG, and share equivalences asynchronously. The intended target is larger circuits where a serial sweep is the bottleneck. Sharing can also make later proof tasks easier there.

The official DAC description reports experiments on ISCAS/ITC, Datapath and Large-Scale benchmark groups. It says HydraCEC consistently outperforms existing parallel CEC solvers. It reports a 10.5× speedup over the best competitor on large-scale instances. It also reports scalability reaching 72.3× speedup with 128 cores. These are reported speedup claims, not proof-strength changes. The accessible description does not give the circuits, solved/timeout counts or baseline configurations. It also does not give the core model, wall-clock definition, preprocessing, memory use or per-benchmark distribution.

The 72.3× figure also needs its denominator before it can be interpreted. It could be relative to a serial baseline, a particular parallel solver or another reference defined by the full paper. The description says the framework reaches that scalability with 128 cores. It does not provide the exact reference or whether all benchmark instances contribute equally. A reader should preserve the number as a bounded conference claim rather than convert it into a universal 72.3× improvement.

### Correctness and performance are separate obligations

Parallel scheduling does not change what it means for two circuits to be equivalent. Each node-equivalence result must still be justified by a valid SAT outcome under the modeled inputs. The framework also needs to preserve completeness of the sweep. A task skipped, canceled or made stale must not remove a necessary candidate without a sound reason.

Performance evaluation must therefore report more than a single speedup. It should show whether all instances reached the same equivalence or counterexample outcome. It should show how many timed out and whether preprocessing is included. It should also show how memory and core count scale. It should show whether the scheduler's extra bookkeeping offsets its savings on small cases. A solver that completes faster by changing timeouts or stopping before unresolved tasks is not a faster equivalent checker.

### Limits at the current evidence level

The accessible source establishes the problem, HydraCEC's named components, benchmark families, and headline speedup claims. It does not establish the exact TBG construction, the equivalence-sharing data structure, or the SAT solver and circuit representation. It also does not establish timeout policy, hardware platform, competitor settings or individual benchmark results. Nor does it establish memory scaling, counterexample handling or artifact reproducibility.

The framework's likely benefit is largest when successful merges expose substantial downstream simplification. It is also largest when enough independent tasks exist to occupy workers. Small circuits, highly dependent task graphs or memory pressure can reduce or reverse the benefit. So can weak benefit estimates or few useful equivalences. These are mechanism-derived evaluation conditions, not results attributed to the target paper.

### What this paper establishes

HydraCEC presents a coherent way to attack the serial portion of SAT sweeping. It schedules candidate equivalence tasks concurrently and prioritizes tasks by expected simplification benefit. It also shares results without a global barrier. The DAC description reports large-scale benchmark speedups and 128-core scalability for this design.

From the accessible pages, it does not establish the detailed correctness argument or task-benefit model. It also does not establish runtime distribution, memory cost or reproducible comparison. These are needed to accept the headline as a general CEC performance law. A complete reading requires the manuscript and artifact. It then requires matched runs that preserve the same equivalence obligations, solver limits and outcome accounting.

**Primary source read:** [DAC 2026 official description](https://63dac.conference-program.com/presentation/?id=RESEARCH285&sess=sess163), which states the SAT-sweeping bottleneck, HydraCEC and Task Benefit Graph scheduling. It also states asynchronous equivalence sharing, benchmark families, 10.5× competitor comparison and 72.3×/128-core claim. No target manuscript, benchmark tables or artifact execution was recovered in this pass.

<span id="explanation-dac-2026-research720"></span>

## Probabilistic safe controller synthesis: what a stochastic safety certificate actually covers

### The controller acts on a model, not directly on an image

A vision-based controller receives an image or other visual observation. But the physical system evolves through hidden or partially observed state. The state may include position, velocity, orientation and other variables that determine whether the next action is safe. An image is a measurement of that state, not the state itself. Camera noise, lighting, environmental changes and observation-model error can make similar states produce different images. They can also make different states look similar.

The paper's target is a closed-loop controller whose neural policy uses visual observations. The safety claim is stated over the underlying dynamical system. The key verification question is therefore not merely whether the neural network chooses a reasonable action on sampled images. It is whether the closed loop remains inside a safe state set. This holds under a stated uncertainty model, with a stated probability bound over the modeled horizon.

### A probability statement needs a horizon and a distribution

Let the system state evolve from an initial set through dynamics affected by environmental perturbations. A finite-horizon safety claim has the following form. Start from the allowed initial states and apply the controller. Then a specified lower bound applies to one probability. That probability is that the state remains in the safe set for every step up to horizon `N`. This probability is taken over the uncertainty model, not over arbitrary disturbances outside that model.

That scope is essential. A certificate for one time step is not automatically a certificate for a hundred-step trajectory. A bound for a finite horizon is not automatically an infinite-horizon claim. A high probability under the data distribution is not a worst-case guarantee for every possible image or environmental change. The paper's use of “probabilistic” should therefore be read as a quantitative guarantee under explicit stochastic assumptions. It is not deterministic safety against all disturbances.

### The cGAN supplies a verifiable observation model

The first component uses a conditional generative adversarial network to approximate the mapping from system states to visual observations. The condition is the system state; the generated image represents what the controller may observe at that state. This provides a closed-loop model in which the physical dynamics, observation generation and visual policy can be analyzed together.

The cGAN is not itself a proof that the real camera or environment follows the learned mapping. It is a learned approximation. Its uncertainty model may omit lighting, occlusion, sensor corruption or state regions absent from training data. The certificate then applies to the approximated observation process. It does not automatically apply to the real deployment process. The safety result therefore depends on how uncertainty is quantified and how the learned observation model is validated.

### Reinforcement learning supplies a starting controller, not the certificate

The method combines the visual model with reinforcement-learning pretraining to construct an initial controller. Pretraining can provide task behavior and a useful policy before formal refinement. Reward optimization does not by itself establish safety. A policy can achieve high task reward while entering a low-probability unsafe region. This is especially likely when the training distribution does not expose the relevant perturbation.

The formal stage adds a stochastic barrier certificate. A stochastic barrier certificate is a learned function. Its values and expected evolution constrain the probability of reaching an unsafe set. The training objective seeks a function and controller satisfying conditions that imply a safety bound. The certificate is the proof object. The neural policy is safe only to the extent that the certificate inequalities hold. They must hold for the modeled dynamics, observation process, action limits and uncertainty.

### Martingale reasoning connects local inequalities to a trajectory bound

The method uses martingale theory to turn a one-step conditional expectation condition into a bound. The bound is on the probability of violating safety over the chosen horizon. In outline, the certificate process is constructed so that its conditional evolution does not grow in the forbidden way. A maximal-inequality argument then limits the probability that the process reaches the unsafe threshold.

The important conceptual step is the bridge from local dynamics to a multi-step statement. The certificate does not enumerate every image and trajectory. It establishes an inequality that must hold at every modeled state and action. The martingale argument aggregates those inequalities over time. Suppose the inequality is checked only on sampled points. Or suppose the learned dynamics do not cover the actual state distribution. The mathematical implication is then weakened. A reader must distinguish a theorem conditioned on certificate conditions from empirical agreement on simulation traces.

### Counterexamples close the loop between learning and verification

The method alternates controller and certificate refinement. A verification procedure searches for states or observations that violate the certificate or safety condition. These counterexamples are added to the training process. The controller and certificate networks are then updated on failures found by the verifier. The process repeats until the resulting pair satisfies the verification checks or the procedure stops without a certificate.

This is a counterexample-guided synthesis loop. A discovered counterexample is evidence that the current candidate is unsafe or that its certificate is insufficient at that point. It is not evidence that the updated candidate is safe everywhere. The final probabilistic claim requires the certificate conditions to be verified over the relevant domain. Approximation and solver tolerances must be accounted for. If the verification search is incomplete, the result may be an empirical refinement process rather than a complete certificate.

### What the official evaluation establishes

The DAC description states that the method was tested on widely studied benchmarks and reports efficiency and effectiveness. It identifies the architecture-level components. These are cGAN observation modeling, RL pretraining and data-driven uncertainty quantification. They also include stochastic barrier certificates guided by martingale theory, and alternating counterexample refinement. It does not expose benchmark names, dynamics, controller architectures or horizon lengths. It also does not expose probability thresholds, baselines, safety-violation counts, computation times or certificate margins.

Those missing quantities control interpretation. “Safe” could mean a high empirical success rate, a formal probability lower bound, or both; “efficient” could refer to training, verification, inference or the number of refinement rounds. Without the manuscript, the official description cannot establish the numerical safety probability or the size of the uncertainty set. It also cannot establish the independent test distribution. Nor can it establish whether the reported certificates transfer from the learned observation model to a physical camera.

### Limits that determine the certificate's scope

The guarantee is conditional on the closed-loop model. It depends on the system dynamics, observation generator, uncertainty distribution and initial-state set. It also depends on the safe set, action constraints, time horizon and certificate inequalities. Changing any of these can change the probability bound. A model trained on environmental perturbations cannot automatically cover perturbations outside its data or support.

The controller may also exploit visual features that are not stable under deployment changes. A cGAN can make the formal problem tractable while introducing model bias. Counterexample refinement can improve the sampled or searched regions but does not alone prove that unsearched regions are safe. The paper's use of a neural certificate also raises numerical and optimization questions. Failure to find a certificate may mean the controller is unsafe. It may mean the parameterization is insufficient. It may also mean the optimization stopped early.

### What this paper establishes at the current evidence level

The paper presents a technically coherent synthesis architecture for visual control under modeled uncertainty. It learns an observation model and pretrains a policy. It learns a stochastic barrier certificate. It uses martingale reasoning for a finite-horizon probability statement. It then refines both networks with verification counterexamples. The official description supports that mechanism-level reading and claims formal probabilistic safety guarantees.

The accessible record does not establish the actual probability numbers, benchmark conditions or completeness of verification. It also does not establish physical-camera transfer, long-horizon behavior or computational cost. The correct acceptance standard is to inspect the theorem assumptions and certificate checks. Then reproduce the stated benchmarks with independent perturbations. Compare empirical trajectories with the certified bound.

**Primary source read:** [DAC 2026 official description](https://63dac.conference-program.com/presentation/?id=RESEARCH720&sess=sess158), which states the cGAN observation model, RL pretraining and data-driven uncertainty. It also states the stochastic barrier certificate, martingale reasoning, counterexample refinement and benchmark claim. No target manuscript, quantitative tables or artifact execution was recovered in this pass.

## What a formal result establishes

Formal analysis represents a design, its environment, and a requirement mathematically. A procedure then reasons about the behaviors allowed by that model. A successful result applies to the stated model and assumptions. If an important behavior was excluded, the proof does not establish anything about that omitted behavior.

The requirement itself must be explicit. Two circuits may be required to produce the same outputs. A state may be required to remain unreachable. Or execution may need to finish before a deadline. These are different properties and can require different representations and proof procedures.

## Why a proof can become expensive

A stateful circuit stores information. Each allowed combination of stored values contributes to its possible states, and inputs determine how those states change. Directly enumerating all behavior can become impractical. Formal methods use structure, simplification, decomposition, and mathematical reasoning to avoid unnecessary enumeration.

Simplification needs a justification. If a design is split into parts, the assumptions used for each part must hold when the parts interact. A smaller proof task is useful when solving it contributes to the original requirement. It must not silently replace that requirement with an easier one.

## Equivalence checking compares behavior

The factored-form-sharing paper concerns checking that two combinational circuits implement equivalent behavior. A combinational circuit's outputs depend on its current inputs rather than a sequence of stored states. Its captured method partitions work using shared structure and estimates of proof difficulty. [Recorded evidence](../observed-subthemes/formal-analysis-and-verification.md#paper-dac-2026-research1388)

Sharing repeated expressions can reduce redundant reasoning. Splitting the task can permit parallel execution, but partition sizes and overhead determine whether this helps. The comparison needs the same circuit pairs, proof obligation, computing resources, and timeout policy. Solved cases, unfinished cases, memory, and absolute runtime matter alongside a speedup. Those details remain unresolved in the current description.

## A timing bound depends on execution assumptions

The worst-case-execution-time paper concerns an upper bound on GPU-kernel duration when threads take different branches. An upper bound must cover every execution allowed by its assumptions. It differs from the longest time observed in a finite experiment, which may miss a slower execution. [Recorded evidence](../observed-subthemes/formal-analysis-and-verification.md#paper-dac-2026-research1552)

The captured method combines analysis with a constraint on thread-group execution. A tighter bound can be useful, but the constraint must be enforceable on the intended machine. Memory behavior, scheduling, and interference also need an explicit scope. The current record does not establish the full proof boundary or enforcement cost.

## Generating a property is different from proving it

ATLAS's captured description maps security concerns to assertion properties and verification scripts. An assertion is a condition the checker evaluates. A generated assertion can be valid syntax yet omit the intended security requirement. Even a completed proof of that assertion would then answer an incomplete question. [Recorded evidence](../observed-subthemes/formal-analysis-and-verification.md#paper-dac-2026-research2886)

Evaluate the quality of the generated requirement separately from the checker's result. Record missing threat cases, unsound assumptions, script failures, unfinished proofs, and human review. The description does not establish those quantities across unseen designs.

## Reading proof outcomes honestly

A completed proof, a counterexample, an unsupported property, and a timeout are distinct outcomes. A counterexample is a behavior that violates the stated property; it still needs interpretation against the intended design and environment. A timeout leaves the property unresolved.

Compare methods on matched obligations and resource budgets. Preserve assumptions with each result and check whether a claimed improvement changes those assumptions. For deployment, connect the mathematical model to the implemented hardware and software. That connection is part of establishing usefulness, not a consequence of the proof procedure finishing successfully.
