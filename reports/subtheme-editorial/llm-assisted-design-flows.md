## A language model proposes an action in a larger design process

All eight paper records in this chapter now have expanded individual explanations. This is writing coverage, not independent comprehension acceptance: source depth varies, original-ledger and artifact reconciliation remain open, and the broader collection still needs rewriting. The comparison below connects the contributions without ranking incompatible measurements.

## Read the eight contributions by the decision they change

| Paper explanation | Decision being changed | What must be checked separately |
|---|---|---|
| [drcAgent](#explanation-dac-2026-research2145) | A repair to physical geometry | Applicable rules, connectivity and newly introduced violations |
| [Two-tier Verilog generation](#explanation-dac-2026-research2545) | RTL describing the requested behavior | State transitions, output timing and implemented hardware quality |
| [ParetoPilot](#explanation-dac-2026-research865) | Synthesis configurations | Feasibility, complete search cost and tradeoffs among candidates |
| [MappingEvolve](#explanation-dac-2026-research535) | Code inside a technology mapper | Produced netlist equivalence, held-out circuits and a validated fallback |
| [ModuPlace](#explanation-dac-2026-research012) | Component grouping and placement relationships | Realizable geometry, routing and electrical behavior |
| [FPGA architecture optimization](#explanation-dac-2026-research1110) | Connected compute stages and data streams | Values, ordering, progress, resource fit and integrated throughput |
| [VeriOpt](#explanation-iccad-2025-1222) | RTL implementation choices informed by cost reports | Unchanged behavior and matched power, timing and area conditions |
| [VERIRL](#explanation-iccad-2025-110) | The trained generator's output distribution | Independent functional tests and separation of reward from acceptance |

These are not eight interchangeable ways to measure whether a language model is good at chip design. They act on different objects. A configuration search chooses within an existing tool interface; changing the tool itself can affect future designs that were never in the search. Generating a learned reward changes training incentives; repairing a routed design changes a physical artifact directly. Their failure modes and verification costs therefore differ.

The common design question is where to place a machine-generated proposal relative to a trusted check. A proposal can narrow the next search or suggest a revision without being accepted as correct. The check needs to assess the resulting object under the original requirements. If the requirements, testbench, reward and generated candidate all inherit the same mistaken assumption, agreement among them is weak evidence.

Three long-term hypotheses follow from this comparison, not from a measured historical increase. First, structured proposals may make failures easier to locate when their fields have explicit meanings and independent validity checks. This would weaken if structure merely relocates errors into unchecked relationships. Second, implementation feedback may improve practical choices when the report belongs to the exact candidate and its constraints remain fixed. This would weaken if apparent gains disappear after integration or matched evaluation. Third, learned guidance may reduce repeated search work when training cost is reused across sufficiently many unfamiliar tasks. This would weaken if gains depend on benchmark familiarity or expensive per-task repairs.

Testing those hypotheses over time requires comparable task families, source access, tool and model versions, budgets and acceptance rules across editions. This chapter combines ICCAD 2025 fallback records with DAC 2026 records; that difference alone cannot establish a shift from one approach to another. Unavailable manuscripts and the selected-paper sample also prevent treating these eight records as field-wide proportions.

A language model produces text or structured output from its input context. In chip design, that output might be hardware-description code, a tool command, a suggested layout change, or a set of compiler settings. The output becomes useful only when the surrounding process can interpret it, execute it, and check the resulting design.

The design flow therefore includes more than the model. It includes the specification, the information supplied to the model, the permitted actions, the design tools, and the rule for accepting an output. Changing any of these can change the measured success rate.

## Information supplied to the model affects the claim

Retrieval-augmented generation supplies selected reference material with a request. In a design application, that material could include design rules, examples, or tool documentation. Retrieval can make relevant information available, but it does not establish that the material is complete, current, or correctly applied.

An evaluation must identify which references the model could access and how they were selected. A method with task-specific examples or manually prepared rules has different preparation costs and transfer assumptions from one evaluated with only a general specification.

## Drcagent proposes physical-design repairs

Drcagent's captured description combines design-rule information, a language model, and feedback from electronic-design tools to repair violations. A design-rule check evaluates whether physical geometry satisfies specified manufacturing constraints. Repairing one violation can change nearby geometry and create another. [Recorded evidence](../observed-subthemes/llm-assisted-design-flows.md#paper-dac-2026-research2145)

The useful outcome is a valid repaired design under the full relevant checks, with the original circuit intent preserved. The record does not establish violation coverage, closure rate, runtime, final layout quality, or transfer across processes. A multi-turn repair loop by itself does not establish any of those outcomes.

## Generated code needs several kinds of checking

The two-tier Verilog-generation record combines retrieved information, classification, prompting, simulation, review, and hardware-performance checks. Verilog describes circuit behavior and structure. A valid text representation can still implement the wrong function, and a functionally correct description can produce an unsuitable circuit after synthesis. [Recorded evidence](../observed-subthemes/llm-assisted-design-flows.md#paper-dac-2026-research2545)

Separate syntax acceptance, simulated correctness, synthesis completion, and implemented hardware quality. Report how many outputs fail each step. A system that accepts fewer but better designs may have a different useful result from a system optimized for generating many syntactically valid candidates.

## Paretopilot chooses synthesis settings

High-level synthesis constructs hardware from a higher-level program and settings that influence parallelism, resource use, and scheduling. Paretopilot's captured method uses a language model to guide exploration of these choices. [Recorded evidence](../observed-subthemes/llm-assisted-design-flows.md#paper-dac-2026-research865)

Several objectives can conflict. A candidate may be faster but larger. A Pareto set contains candidates for which no other evaluated candidate is at least as good on every objective and better on one. The quality of that set depends on the objectives, evaluated candidates, and budget. The current description does not establish enough of those conditions to interpret its reported improvement as a generally better search.

## Count the work needed to obtain an accepted design

A complete budget includes preparing references, model calls, tool execution, failed attempts, repairs, and human intervention. If training or task-specific tuning is required, state whether that cost is included and how often the resulting method is reused.

Compare the same tasks and acceptance rules. Preserve model and tool versions, prompts or interfaces, and failure records. Test unfamiliar designs and conditions. The strongest conclusion identifies which part of the design process improved, what feedback caused the improvement, and what work still requires a separate correctness or physical check.

<span id="explanation-iccad-2025-110"></span>

## VERIRL: improve a generator without confusing its reward with circuit correctness

### What the inspected preprint establishes

Selected method and evaluation sections of version 1 were read on 2026-09-08. No training, repository code or generated RTL was executed; conference-version and artifact reconciliation remain open. The current reading card below includes this extraction; the original captured fields remain available in its disclosure.

VERIRL trains a policy with a learned reward model. Its trace-back procedure replaces an internal candidate's score with the mean of its children's scores; sample balancing adjusts learning contributions using probability and reward. [Sections III, V–VI; trace-back on PDF page 5](https://arxiv.org/pdf/2508.18462v1#page=5)

Evaluation uses twenty samples per task and pass@1/pass@5. Table II reports CodeQwen2.5-based VERIRL at 69.3/78.1 on VerilogEval-human and 58.2/66.0 on RTLLM v1.1. Inference selects the best results across three temperatures. [Sections VII-D–F and Table II, PDF pages 7–8](https://arxiv.org/pdf/2508.18462v1#page=7)

These are functional benchmark results, not measured circuit power, area or timing. The independent examples below explain why training scores, repair success and final acceptance need separate meanings.

### The trained object is a probability distribution over outputs

A language model generates a sequence by assigning probabilities to possible next tokens. For a hardware task, the sequence includes a proposed implementation. Training changes which implementations are likely to be generated; it does not directly change the circuit already produced on a previous attempt.

A policy is the model used to choose outputs. A reward is a score used to guide learning. A reward model is a learned function that predicts a score from the task and candidate. Executing a testbench is a different operation: it runs selected input sequences and checks the circuit's responses. Predicted quality and observed test outcome can disagree.

Suppose a generator produces two candidates. A receives predicted reward 0.9 but fails a required reset test. B receives 0.7 but passes all the available checks. The reward ranking prefers A; the observed test outcome favors B. Training can improve prediction quality, but calling the score a reward does not make it an authoritative correctness decision.

### Sparse feedback can hide useful distinctions

An all-or-nothing test outcome may assign zero to both a program that does not parse and one that computes nearly every tested case correctly. Their next repairs may be very different. More detailed observations can help distinguish missing syntax, incorrect output width, wrong state transitions and output-cycle errors.

However, counting passed tests does not automatically measure how close a circuit is to correct. Consider ten tests: nine exercise ordinary addition and one checks overflow. A circuit passing nine receives 90% test success but still violates a required case. Duplicating the ordinary tests could increase the percentage without improving the implementation. Coverage and severity do not arise from the denominator alone.

The original specification must therefore remain visible when test results become training labels. Multiple generated testbenches can share the same omission. Agreement across tests is more useful when they exercise genuinely different requirements than when they restate one easy case in different code.

### Repair potential and present correctness answer different questions

For an independent tree example, candidate A initially passes none of its tests. Two revised children pass all tests and 80% of tests respectively. Averaging the children's scores gives 0.9. That can express usefulness as a starting point for the particular repair process; it is not A's own measured pass rate.

The distinction matters when constructing preferred and disfavored training pairs. A high score inherited from repairs may encourage outputs that lead to good repairs, rather than outputs that already pass. Whether that helps one-shot generation depends on the data representation and the learning procedure. It cannot be settled by changing the score's name.

To evaluate this boundary, retain candidate identities, original test outcomes, repair histories and inherited scores as separate fields. Test final sampled outputs independently of the scorer used in training. These are proposed checks, not claims that the released implementation mislabels its results or that its reported benchmark gains are invalid.

### Probability and reward are not the same kind of confidence

Generation probability says how likely the current model is to emit an output under the sampling process. Reward says how desirable a scorer judges it. A common output may be consistently wrong, while an uncommon output may implement an unusual requirement correctly.

An adaptive weighting scheme changes how much particular examples influence an update. Increasing attention to promising rare cases may help the model learn beyond frequent patterns. Reducing the influence of persistently uninformative cases may reduce noise. But unusual valid behavior can also look rare, and scorer mistakes can make invalid behavior look promising.

For a simple illustration, suppose a batch has ninety routine cases and ten unusual cases. Optimizing only the overall mean can improve ninety answers while degrading all ten unusual ones. A weighted objective can expose that imbalance, but it still needs trustworthy labels and evaluation on the relevant task categories. A balanced numerical objective is not itself a guarantee of generalization.

### Understand what multiple-attempt success measures

Pass@1 concerns one sampled solution; pass@5 concerns whether at least one of five sampled solutions succeeds. A higher multiple-attempt score can be useful when the user can afford to generate and test alternatives. It does not say the system can identify the successful candidate without those checks.

For an independent finite-sample calculation, suppose twenty generated candidates contain four passes. A uniformly chosen single candidate succeeds with probability `4/20 = 0.2`. Choosing five distinct candidates from that set has success probability `1 − C(16,5)/C(20,5)`, approximately 0.718. Here `C(n,k)` counts the ways to select k objects from n without regard to order. The difference reflects additional chances, not a change in any candidate's correctness.

Do not replace that finite-sample calculation with an assumption that every attempt is independent and has identical success probability unless the measurement supports it. Models can repeat the same wrong structure. Record sampling settings, candidate count, testing cost and selection procedure when comparing methods.

Choosing the best setting using the evaluation results adds another selection step. A transferable deployment claim should distinguish a setting chosen on separate validation tasks from a best-of-settings result on the reported benchmark. Neither is inherently meaningless; they estimate different procedures and require different budgets.

### Dataset filtering does not prove independence from evaluation

Removing near-identical text helps reduce one form of duplication. It does not ensure two differently worded problems require different circuits. Conversely, similar text can specify importantly different behavior, such as a different reset polarity or output cycle.

An independence check should follow problem provenance and semantic overlap as far as the evidence allows. It should also distinguish training examples, reward-training pairs, repaired descendants and evaluation tasks. A large count of pairs can contain repeated information from a much smaller number of underlying problems.

Training and evaluation costs also serve different purposes. Preparing testbenches, exploring repair branches and training a scorer are preparation work. Generating a new candidate and checking it are per-task work. Any claimed engineering saving needs both, with the intended number and variety of future tasks stated.

### Connect training improvements to implementation requirements

[VeriOpt](#explanation-iccad-2025-1222) discusses using implementation feedback to improve RTL costs. VERIRL's inspected evaluation concerns functional generation. Better functional sampling can supply more usable starting candidates to a later implementation flow, but does not establish that those candidates satisfy area, power or clock constraints.

The bounded hypothesis is that informative, correctly interpreted training feedback can increase the chance of obtaining usable RTL on unfamiliar tasks. It weakens if rewards mainly predict benchmark-specific test behavior, if repair-derived labels do not transfer to final outputs, or if gains vanish under matched sampling budgets. Source-to-artifact consistency, broader test coverage, dataset independence, reproduced measurements and independent comprehension review remain open.

<span id="explanation-iccad-2025-1222"></span>

## VeriOpt: improve implementation cost without changing the required behavior

### What the manuscript actually supports

The version-1 preprint was inspected on 2026-09-08, including method, evaluation tables and limitations. This is manuscript reading, not execution or verification of a conference camera-ready version. The current reading card below includes the inspected conditions and preserves the original abstract-backed fields in its disclosure.

VeriOpt assigns planning, programming, reviewing and evaluating roles, then supplies optimization context and synthesis reports. Section V-C explicitly describes manual external synthesis feedback. [Sections III and V-C; limitations on PDF page 8](https://arxiv.org/pdf/2507.14776v1#page=8)

Evaluation uses GPT-4o, Icarus Verilog, Design Compiler and RTLLM; Table II reports 25/29 testbench passes. PPA baselines are the flow's functionally passing pre-optimization designs. [Section IV-A and Table II, PDF pages 6–7](https://arxiv.org/pdf/2507.14776v1#page=6)

Table III's 73.23% is critical-path reduction for the 16-bit divider. Some leakage and slack entries worsen. Its 90% slack improvement for the four-bit pipelined multiplier also exceeds the prose's stated 39.44% maximum. Preserve that discrepancy rather than silently harmonizing it. [Table III and Section IV-C, PDF pages 7–8](https://arxiv.org/pdf/2507.14776v1#page=7)

The independently constructed examples below explain how to read those boundaries. They are not recreated VeriOpt circuits, simulations, or measurements.

### Define behavior before optimizing its implementation

Register-transfer-level code, or RTL, describes how stored state and combinational logic determine a circuit's outputs. Combinational logic calculates from its current inputs. Registers preserve values between specified clock events. For a sequential circuit, correctness concerns a sequence of states and outputs, not just a final arithmetic answer.

Suppose a request accepted at clock edge 0 must produce its sum at edge 1. An implementation that produces the same sum at edge 2 violates that timing contract unless the interface explicitly permits the extra cycle. A faster clock does not automatically make it interchangeable with the original circuit: connected components may still expect the result on a particular edge.

Width also matters. Adding unsigned eight-bit values 255 and 1 gives 256 mathematically. An eight-bit output wraps to zero if that is the specified behavior; a nine-bit output can retain 256. An optimization that drops the carry is correct for one contract and incorrect for the other. Natural-language requests and checking code must agree on which result is required.

### Roles organize work; checks establish what passed

A planner can state the intended registers, operations and state transitions. A programmer can implement them. A reviewer can compare implementation with plan. An evaluator can use tool outcomes to identify revisions. This separation can make a proposed change easier to inspect, but it does not make the plan correct merely because another role followed it.

For example, a plan might wrongly give enable priority over reset. Every later role could agree with the implementation, while the required simultaneous-reset-and-enable case remains wrong. The useful external check comes from the specification, not from agreement among generated descriptions.

Simulation applies selected input sequences and compares observed behavior with expected behavior. A passing testbench establishes agreement on those checks, not on every possible sequence. Formal equivalence can answer a broader comparison under explicitly modeled assumptions, but should not be inferred from the existence of a reviewer or a successful simulation. A robust account must name the actual check used.

### Timing slack is a margin, not a pass percentage

For a simplified setup check, slack is the required arrival time minus the actual arrival time. If data is required by 2.0ns but arrives at 2.4ns, slack is −0.4ns: the path is late. Reducing arrival to 2.2ns improves slack to −0.2ns, yet the requirement still fails. Halving the lateness is not timing closure.

The critical path is the path that limits the relevant timing objective under the chosen constraints. Shortening it can improve achievable speed, but another path may then become limiting. Clock definitions, input arrival assumptions, output requirements and cell-library conditions affect the result. A percentage alone cannot say whether the final design meets its deadline.

Small starting margins also make percentages unstable. Changing slack from −0.02ns to −0.03ns worsens the magnitude of lateness by 50%, but the absolute change is 0.01ns. Neither number should be hidden: the percentage conveys relative change, while the absolute value and required margin determine acceptance. This is a teaching calculation, not a recovered optimized report.

### Pipelining and sharing change different costs

Pipelining places storage between portions of a computation so less logic must finish between adjacent clock events. Consider two serial combinational blocks taking 1.1ns each. With 0.2ns of aggregate register overhead, a single-stage timing estimate is 2.4ns. Splitting evenly can give approximately 1.3ns per stage, but now an item crosses two stages and extra registers consume area and clock activity. These estimates omit routing and other implementation costs.

Resource sharing instead lets several operations use one hardware unit at different times. Replacing two adders with one can reduce arithmetic hardware, but adds operand selection, scheduling and possibly storage. If both results are required simultaneously, sequential reuse cannot meet that requirement without changing some other part of the architecture.

The design objective must therefore say which quantities may move. Minimizing area subject to a fixed output schedule is different from minimizing area while allowing arbitrary extra cycles. A comparison that changes the functional or timing contract has changed the task, not merely found a cheaper implementation.

### Power, energy and activity are different measurements

Power is energy per unit time. Energy for one task depends on power during the task and the duration of execution. A circuit averaging 8W for two seconds uses 16J; a 10W implementation finishing in one second uses 10J. Lower power can accompany higher energy when work takes longer.

Dynamic power concerns switching activity. Leakage concerns current that can persist even when useful switching stops. Suppressing unnecessary register updates may reduce some activity while leaving clock distribution and other logic active. Clock gating controls clock activity; it is not equivalent to disconnecting a region's power supply. Neither should be credited with a particular leakage reduction without the corresponding implementation evidence.

A power estimate also depends on how often signals change. Comparing one design under mostly idle inputs with another under active inputs is not a matched workload comparison. The relevant evidence includes activity assumptions, operating conditions, included circuitry and how power was calculated. A synthesis report supplies estimates under a model, not a physical measurement of fabricated hardware.

### Keep each candidate's results together

Suppose candidate A has power 4, area 10 and delay 3, while candidate B has power 7, area 6 and delay 2, in fixed arbitrary units. Neither dominates the other: A uses less power, B is smaller and faster. Reporting power 4, area 6 and delay 2 as one design would invent an implementation that neither candidate provides.

Every result row should therefore identify the exact RTL revision and its correctness outcome, synthesis settings and complete metric set. If separate power-, area- and timing-oriented candidates are generated, retain them separately. The best improvement in each column does not establish one candidate achieving all of those improvements simultaneously.

Failed generation tasks also remain part of the overall outcome even if they cannot enter a PPA comparison. In an illustrative ten-task study, finding correct implementations for six tasks and improving all six does not mean ten tasks were solved. Report generation coverage and conditional implementation improvements with their own denominators and search budgets.

### What this contributes to the larger subject

The connection to [two-tier Verilog generation](#explanation-dac-2026-research2545) is the separation of behavior generation from implementation quality. The connection to [MappingEvolve](#explanation-dac-2026-research535) is that a favorable optimization score still needs a valid accepted result. The edited objects differ: RTL in one case, mapping software in the other.

The bounded hypothesis is that structured proposals plus implementation feedback can improve design choices when the original contract and acceptance checks remain fixed. It would weaken if gains depended on looser output timing, unmatched activity assumptions, manual work excluded from the budget, or selecting incompatible metrics from different candidates.

Target-library and operating conditions, complete prompt/retry cost, exact post-optimization checking, per-candidate RTL/report pairing and artifact reproduction remain unresolved in this assessment. Independent review is still required; the new explanation does not establish production readiness or a historical trend.

<span id="explanation-dac-2026-research1110"></span>

## FPGA HLS architecture optimization: make connected stages work at compatible rates

### What is available, and what is still missing

The official description proposes language-model-driven generation and optimization of system-level HLS architectures and reports an average 11.78× performance improvement. It does not supply the benchmark conditions needed to interpret that average. [Official description](https://63dac.conference-program.com/presentation/?id=RESEARCH1110&sess=sess173)

A fresh title search on 2026-09-08 did not recover the manuscript. The [author's publication entry](https://csee.hnu.edu.cn/people/hexu) links HLSArchOpt. Its pinned README and top-level source were reread for this explanation. The [saved primary assessment](../../dac/data/hlsarchopt-primary-assessment-v1.json) additionally records selected script and stored synthesis-report inspection; those observations are attributed to that earlier assessment, not to a newly executed experiment. No manuscript page citations are available.

The release contains a Fire-module example, not the full optimization framework. Its README names Vivado HLS/Vivado 2019.2, ZCU102 and a 100MHz target, while listing full-model integration and automation as future work. These conditions describe the released example, not every paper benchmark. [Pinned README](https://github.com/Szzer1/HLSArchOpt/blob/999043ab132f984b5b88b26ab9e415221e1198f1/README.md)

### Start with a computation, not a generated file

An FPGA is a device whose configurable logic, arithmetic resources, memory blocks and connections can implement a chosen digital circuit. High-level synthesis, or HLS, translates a program and implementation directives into a hardware design. The same computation can be implemented with different amounts of parallel arithmetic, buffering and resource sharing.

A convolution computes weighted sums over selected input values. An activation such as ReLU replaces a negative result with zero and retains a nonnegative result. These operations define values that must be produced. Their implementation additionally determines when values are available, how they are stored and how subsequent operations receive them.

For a simple independent example, four products can use one multiplier over several cycles or four multipliers concurrently. The second choice needs enough input delivery capacity and a way to add the products. If operands arrive one pair per cycle, installing four multipliers alone cannot sustain four useful products per cycle. Architecture optimization must consider the connected computation rather than count arithmetic units in isolation.

### The inspected example branches and rejoins

The top-level source unpacks 32-bit stream payloads as floating-point values, applies a squeeze convolution and ReLU, duplicates the resulting stream, processes two expand convolution/ReLU branches, concatenates their outputs and packs the result. The function requests HLS dataflow execution. [Pinned `pipeline_top` and `duplicate_stream`](https://github.com/Szzer1/HLSArchOpt/blob/999043ab132f984b5b88b26ab9e415221e1198f1/fire/sys/top.cpp)

Dataflow execution allows connected stages to overlap when dependencies and resources permit. It does not make all operations independent. A consumer still needs the correct input values in the expected order. Duplication means each branch receives the required values; it does not mean the branches receive alternating halves of the input.

Concatenation joins outputs along a specified dimension. It is not addition. If one branch produces channels `[a,b]` and the other `[c,d]`, an intended output might be `[a,b,c,d]`. Returning `[a+c,b+d]` has different shape and meaning. Returning `[a,c,b,d]` preserves four values but can still violate the required channel order. A test must check layout and ordering as well as arithmetic.

### Throughput depends on the slowest sustained rate

Latency is the time from starting a particular work item until its output is ready. Initiation interval is the spacing between accepted work items in a repeated schedule. The two can differ because several items can be in progress together.

For an idealized example, a pipeline has latency ten cycles and accepts another item every five cycles. Four items finish by cycle `10 + 3×5 = 25`, assuming the first starts at cycle zero and no stalls occur. Processing them without overlap would take forty cycles. The first item's latency remains ten; overlap improves repeated-work throughput, not necessarily individual response time.

Now consider a producer able to supply one value per cycle and a consumer able to process one every two cycles. A finite queue temporarily absorbs the difference. Its occupancy grows until it is full, after which the producer must slow down. More buffer space delays this event but cannot remove a permanent rate mismatch.

A duplicated stream has two consumers. If both must receive every input value, the slower branch can limit the source's sustained rate even while the faster branch is idle. Replicating work at a branch point can therefore create a capacity requirement rather than a free speedup. The relevant optimization may involve balancing branches, changing their parallelism, or reconsidering how intermediate values are stored.

### A complete stream protocol is part of correctness

Backpressure means a receiving stage temporarily prevents its sender from delivering another value, usually because storage is full. This is ordinary flow control, not automatically a deadlock. Deadlock requires a set of waits from which the system cannot advance under the allowed actions.

For an independent construction, suppose two tasks each insist on reading an empty input queue before writing the value the other task needs. Neither can begin. A different schedule or an initial value could change the outcome. This does not show that the released Fire module deadlocks; it shows why testing arithmetic functions separately is insufficient to establish progress of a connected streaming system.

A useful functional check also needs the expected number of inputs and outputs, tensor dimensions, channel order, end-of-output signaling and numerical tolerance. Floating-point sums can change slightly when their addition order changes. A tolerance should express an allowed numerical difference, not silently excuse an incorrect channel permutation or missing output.

### Read the saved synthesis estimates without turning them into board measurements

The saved assessment records top-level latency of 335,494 cycles and interval of 229,703 cycles at a requested 10ns period. Multiplication gives approximately 3.355ms latency and 2.297ms interval. The same assessment records an estimated 8.419ns clock period. These are stored HLS estimates, not a fresh synthesis run, achieved post-route frequency, or measured full-model performance. [Selected text/XML report assessment](../../dac/data/hlsarchopt-primary-assessment-v1.json)

At a fixed clock, fewer cycles reduce the corresponding scheduled time. But a design with more parallel logic can become harder to connect physically and fail the requested clock after placement and routing. One cannot replace the requested clock with a favorable estimate and call the product an observed speedup.

Resource fit is another separate question. FPGA lookup-table logic, registers, dedicated arithmetic blocks and memory blocks have distinct capacities. Spare registers cannot necessarily replace exhausted memory or arithmetic resources without changing the implementation. Integrating the kernel with data transfer and control logic can consume capacity not represented by an isolated kernel estimate.

The saved script inspection found synthesis and export enabled, with C simulation and co-simulation commented out. That limits what that script demonstrates; it does not establish that the authors never ran correctness tests elsewhere. Generating hardware files is not itself evidence of functional equivalence, timing closure, or successful execution on a board.

### A faster module does not establish the headline system gain

Suppose a complete workload spends forty time units in an optimized module and sixty elsewhere. Making the module ten times faster changes total time from one hundred to sixty-four, for a speedup of `100/64 = 1.5625`, not ten. Transfers, other layers and control work can dominate after the improvement. This is an illustrative calculation, not a decomposition of the reported 11.78× result.

An average speedup also needs its aggregation rule and per-model results. The ratio of summed runtimes, the arithmetic mean of individual speedups and their geometric mean answer different questions. A paper-level claim needs matched baselines, resource constraints, accepted numerical quality and complete costs before those numbers can be compared across methods.

Compared with [ParetoPilot](#explanation-dac-2026-research865), which selects synthesis configurations, this record concerns generation and optimization of a connected hardware architecture. The available example helps explain the resulting data path but does not reveal the complete language-model search process. Prompts, retries, model versions, rejected designs and the mechanism connecting feedback to architectural edits remain unresolved.

The bounded insight is that useful automation must jointly preserve values, stream order, progress and feasible rates. Evidence would strengthen with complete model-level comparisons and reproducible optimization histories; it would weaken if local gains disappear after integration or depend on unequal resource budgets. The inspected sources do not yet establish that broader result.

The evidence therefore supports LLM-assisted modular HLS architecture generation and a partial artifact-backed dataflow example, not demonstrated production-ready FPGA acceleration or a reproducible end-to-end 11.78× gain. Prompts/search cost, benchmark aggregation, matched baselines, correctness, post-route/board evidence and resource/quality constraints remain unresolved.

<span id="explanation-dac-2026-research012"></span>

## ModuPlace: turn placement preferences into relationships that a placer can evaluate

### What the recovered manuscript establishes

An author-hosted seven-page manuscript was recovered on 2026-09-08; its title, authors and DOI `10.1145/3770743.3803892` identify this paper. Text was inspected, including method and evaluation sections; no model, placer or router was executed. The current reading card below includes this recovery and preserves the original description-only fields in its disclosure.

The method partitions components hierarchically, generates weighted relative-position/rotation graphs, and places modules then components. Training combines expert examples and preference optimization. [Sections 3.2–3.4, PDF pages 2–5](https://yhhan.com/PDFs/ModuPlace_paper.pdf#page=2)

The evaluation uses Qwen-2.5 7B, 426 training graphs, four 80GB A100s, eleven boards, routing with PcbRouter/Freerouting, and ADS electromagnetic simulation. Table 2 reports mean wirelength 1266.5 versus SA-PCB's 1528.5, and vias 48.6 versus 81.7. P8 instead has wirelength 816.2 versus 688.6 and vias 23 versus 12. [Section 4.1 and Tables 1–2, PDF pages 5–6](https://yhhan.com/PDFs/ModuPlace_paper.pdf#page=5)

Thus the reported average advantage is not improvement on every board. The explanation below develops independent examples; none is a reconstructed benchmark. Manuscript recovery does not establish reproducibility or independent acceptance.

### Start with what placement must produce

A printed circuit board, or PCB, supports electronic components and conductive connections between their terminals. A schematic states which terminals must connect electrically. Placement decides where components sit and how they are oriented. Routing then chooses actual conductive paths, subject to available layers, clearances and obstacles.

A net is a set of terminals that must be electrically connected. A via connects conductive layers through the board. Moving a component can shorten one net while making another harder to route. A geometrically compact placement can therefore require longer routes or more layer changes than a less compact one.

Consider two terminals at `(0,0)` and `(10,0)`, in arbitrary length units. Their direct horizontal separation is ten. If a blocked region requires a route to rise to `y=3`, cross, and descend, that route has length sixteen. Both placements can have the same terminal separation while differing in the available paths. This is why an estimate made before routing is not a measurement of completed wiring.

Half-perimeter wirelength, abbreviated HPWL, sums the horizontal and vertical spans of a net's terminals. For terminals at `(0,0)`, `(10,0)` and `(0,4)`, it is fourteen. It summarizes spatial spread; it does not construct legal copper paths, determine layer changes, or certify electrical behavior. The relevant question is whether optimizing the estimate improves the completed board under the same router and rules.

### Represent a relationship before choosing every coordinate

An intermediate representation is an explicit description passed between stages of a design process. Here the important conceptual distinction is between asking for final coordinates and describing relationships that constrain their choice. A graph has objects as nodes and relationships as edges. Its usefulness depends on what each relationship means, not on the fact that it is called a graph.

For an independent example, suppose A should be left of B with a preferred horizontal displacement of four, while C should be above B by three. A coordinate optimizer can compare candidate positions with those requests. Translating all three components together preserves the relative displacements. The board boundary and any fixed connector still determine whether the translated arrangement is legal.

Relative relationships can conflict. Asking for `xB−xA=4`, `xC−xB=4`, and `xA−xC=4` is impossible: adding the left sides gives zero, but adding the requested right sides gives twelve. Valid graph syntax would not detect the geometric impossibility unless a further check examines the relationships. A model can produce a well-formed intermediate representation that has no exact realization.

### A preference weight is not a hard requirement

A hard requirement rejects a candidate when violated. A preference contributes a cost that an optimizer may trade against other costs. These roles must be explicit. A very large penalty can discourage overlap, but its numerical size alone is not a proof that overlap is impossible in every returned result.

Suppose the desired displacement is four but a candidate provides six. An absolute-error penalty is two. Giving that relationship weight five makes its contribution ten. A solver could still accept the discrepancy if another term decreases by more than ten. This reasoning is illustrative, not a claim about the paper's exact penalty coefficients or solver behavior.

Distance and angle also have different units. Adding a one-millimeter error to a one-degree error requires a defined scaling choice. Otherwise a unit conversion changes the apparent preference. A useful explanation of an optimization result must distinguish user requirements, learned preferences, implementation penalties, and final acceptance checks.

### Hierarchy reduces a search problem but can restrict its answers

Treating related components as a module lets the placer choose a region for a group before resolving every member's location. This reduces the number of details considered simultaneously. It can also prevent a globally useful arrangement if the chosen grouping or boundary is too restrictive.

For example, two components in one group might each connect strongly to different external connectors. Keeping the group compact can shorten its internal connection while lengthening both external connections. The best grouping depends on more than connectivity within the group. Fixed positions, mechanical limits and the intended electrical role can change the decision.

The question is therefore not simply whether hierarchy is present. It is whether the process can revise an unsuitable partition or allocated region, and how that revision is charged to the total search budget. A successful demonstration on one set of boards does not by itself answer how confidently the same grouping procedure transfers to a different class of board.

### Learning an expert preference does not replace checking the result

Training on examples changes which outputs a model tends to generate. Training on pairwise preferences changes which of two candidate outputs it tends to favor. Neither operation turns the learned preference into a manufacturing rule or an electrical proof.

If a reviewer prefers candidate A to B, that comparison need not mean A is acceptable. Both can violate a required clearance, and A can merely violate it less. Similarly, three pairwise judgments can be inconsistent: A preferred to B, B to C, and C to A. A practical evaluation needs to describe how incomplete or conflicting preference information affects the selected result.

Preparation costs also matter. Expert examples, preference labels, training and inference are different expenses from placing and routing a new board. A reusable trained model can spread preparation cost across many tasks, but the number and similarity of those tasks determine whether the total effort falls. A placement-quality comparison alone does not establish a shorter end-to-end engineering process.

### Read the measurements at the right boundary

Wirelength and via count concern the routed geometry. Electrical simulation evaluates a model of that geometry under specified materials, frequencies, ports and other conditions. Physical measurement evaluates a fabricated object with instruments. These are different evidence stages, and one must not be silently presented as another.

A mean can also hide failures or regressions on individual boards. In an illustrative two-board comparison, costs changing from `100,100` to `50,130` improve the mean from 100 to 90 while worsening the second board by 30%. Report per-board behavior and complete-routing success alongside aggregate quality. Failed or unfinished routes must not disappear from the denominator.

The bounded cross-paper idea is that a language model can propose a structured design decision while a separate tool evaluates its physical consequences. [drcAgent](#explanation-dac-2026-research2145) concerns repairs to existing geometry; [ParetoPilot](#explanation-dac-2026-research865) chooses synthesis settings. These are different actions with different acceptance rules. Their shared use of a language model does not make their success percentages comparable.

The next evidence work is to reconcile this manuscript into the paper record, inspect result-producing artifacts if available, and establish training/test separation, routing configurations, electrical test conditions and total cost. None of those missing checks should be filled in from the explanatory examples above.

<span id="explanation-dac-2026-research535"></span>

## MappingEvolve: change the mapper while checking the circuits it produces

### Evidence and scope

MappingEvolve edits technology-mapping code using Planner, Evolver, and Evaluator roles. The manuscript describes bounded operators, compilation, logical equivalence checking, and area/delay evaluation. [Version-1 manuscript, Sections 2–3](https://arxiv.org/html/2604.26591v1#S2)

The existing [primary assessment](../../dac/data/mappingevolve-primary-assessment-v1.json) preserves selected method/evaluation inspection, a visual check of PDF Table 2, pinned control-flow inspection, and selected author logs. The manuscript was reopened for this explanation; no mapping experiment or repository code was executed. Examples below are independently constructed reasoning, not reproduced paper cases. Source-to-result reconciliation and independent review remain open.

### What technology mapping chooses

A Boolean network specifies logical relationships independently of a particular cell library. A cell library supplies circuit implementations of functions with characterized costs and behavior. Mapping chooses how to cover the network with compatible cells. The mapped netlist records chosen cells and their connections.

For example, `y = NOT(a AND b)` can be implemented by an AND followed by an inverter, or by one NAND cell if the library provides it. Both compute the same Boolean function. Their area, delay, input load, and available drive strengths can differ. A mapper must preserve the function while choosing among implementations appropriate to the objective.

The mapping program is therefore not the mapped circuit. Changing a heuristic inside that program can alter the circuits produced for many future inputs. A successful output on one benchmark does not prove that every possible output of the changed program remains correct or good.

### A cut identifies a replaceable region

A cut at a node identifies boundary inputs through which the node's relevant upstream dependencies pass. The logic between those inputs and the node computes a function that may match a library cell. Different cuts expose different candidate groupings of the same underlying computation.

Consider `y = (a AND b) OR c`. One implementation uses separate AND and OR cells. A library might contain a compound cell matching the whole three-input function. Selecting that larger grouping can remove an intermediate connection, but it does not automatically minimize delay under every input arrival and load condition.

If `a` arrives late while `b` and `c` arrive early, the path from `a` can determine completion. A cell's relevant pin delay and the prior arrival time must be combined; gate count alone is insufficient. Matching an inverted output can also require an inverter elsewhere. Local savings need evaluation in the surrounding network.

### Shared logic makes area accounting nonlocal

Suppose two outputs use a shared subexpression `a AND b`. Counting the subexpression's area once for each output overstates the implementation area if it remains physically shared. Removing its use from one output does not free that area while the second still needs it.

An approximate accounting scheme can divide a shared cost among its users. A reference-count-based calculation instead asks whether a proposed change removes the last required use. These answer different questions: a useful local estimate need not equal the actual incremental area of the final selected network.

The paper's operator decomposition concerns delay-oriented selection, area accounting, and output phase choices. The exact mutation must preserve their shared assumptions. A locally attractive edit that mishandles references or signal inversion can produce a wrong netlist even if the mapping program compiles.

### There are two different correctness checks

Compilation checks whether the edited mapping program can be built under its programming-language and dependency rules. Logical equivalence checking compares the produced circuit's Boolean behavior with its reference. Passing the former does not establish the latter.

For an illustrative combinational comparison, form a signal that is one whenever any corresponding output differs. Proving that this signal cannot become one over the permitted inputs establishes equivalence for that compared pair under the check's model. It does not prove the mapping algorithm correct for all future circuits.

The [verification theme](../themes/verification-and-validation.md) explains the same boundary: assumptions, compared outputs, and unresolved outcomes matter. A timeout must not silently become an equivalence pass. A regression on a benchmark omitted from validation can remain unseen while the selected suite improves.

### A combined score can reward a tradeoff

The assessed objective weights normalized area and delay reductions equally. Evolution uses eleven ISCAS85 circuits; evaluation uses EPFL and ASAP7 after ABC preprocessing. The recorded budgets are thirty outer rounds with three inner rounds, versus ninety direct-evolution rounds. [Manuscript Sections 3.1 and 4.1](https://arxiv.org/html/2604.26591v1#S3.SS1)

For an independent example, let area change from 100 to 90 and delay from 100 to 104. The equal-weight score is `0.5×0.10 + 0.5×(−0.04) = 0.03`. A positive score coexists with a slower circuit. A hard delay limit might reject this candidate despite the improved score.

The saved Table 2 transcription reports average area ratio 0.8996 versus ABC for two configurations, with delay ratios 1.0571 and 1.0369 and mapper-runtime ratios 1.755 and 1.6557. [PDF page 6, Table 2](https://arxiv.org/pdf/2604.26591v1#page=6). Thus area reduction coexists with larger average delay and longer mapping runtime; it is not dominance across all dimensions.

Mapper runtime is time spent producing a netlist. Circuit delay concerns the produced design. Evolution time additionally includes model calls, evaluation, failed candidates, and orchestration. These are three distinct budgets. Equal iteration counts do not establish equal wall-clock cost or equal search opportunity.

### Preserve a validated fallback separately from the highest score

The saved pinned-code assessment identifies an ordering concern: best-state update precedes candidate acceptance, and rejection can restore that best state. It gives a source-level counterexample with initial best reward −1, failed candidate reward −0.45, and acceptance threshold −0.1. The candidate improves the stored reward but fails the acceptance threshold.

If that candidate becomes the stored best state before rejection, restoring best does not necessarily restore a separately validated state. This illustrates why best score and known-valid fallback are different properties. It is not evidence that a published circuit was invalid.

The same assessment inspected three selected released outer-loop logs and found no outer reversion in them. Those logs therefore do not demonstrate the modeled failure path. They are author-provided histories, not independently reproduced runs. This distinction prevents a control-flow concern from becoming an unsupported accusation about reported experiments.

### Connect the contribution without overstating it

Unlike [ParetoPilot](#explanation-dac-2026-research865), which chooses synthesis configurations, MappingEvolve changes code inside the optimization tool. Unlike [two-tier RTL generation](#explanation-dac-2026-research2545), its direct output is not the final user circuit. That increases the importance of generalization: a useful evolved mapper should preserve behavior and improve tradeoffs on inputs beyond those that guided evolution.

The bounded hypothesis is that structured edits and explicit checks can improve reusable optimization software within a controlled budget. It weakens if gains disappear on held-out circuits, violate required delay constraints, or require disproportionate evolution and mapping time. The inspected evidence does not establish universal improvement, post-route gains, or a historical trend.

Full result-producing artifact reconciliation, per-netlist checks, broader held-out evaluation, failure handling, model costs, and independent comprehension review remain open.

<span id="explanation-dac-2026-research865"></span>

## ParetoPilot: choose synthesis configurations without confusing a search score with a faster circuit

### What evidence is available

The official description proposes a dedicated language model for HLS exploration, combining directive scheduling and quality-aware optimization. It reports 49.5% better DSE performance, 1.8× efficiency, and 81.4% improvement against an auxiliary DeepSeek-R1 configuration, without defining the metric denominators or full comparison budget. [Official Description and Authors](https://63dac.conference-program.com/presentation/?id=RESEARCH865&sess=sess168)

No target manuscript was recovered in the 2026-09-08 search. The differently titled ParetoPilot diffusion-optimization paper is not this HLS paper. A [saved artifact assessment](../../dac/data/paretopilot-primary-assessment-v1.json) records selected inspection at revision `d08173f66903ed466537c9327b63addac223ee95`. The entry point was reread for this explanation; no code was executed. Artifact-to-headline experiment correspondence remains unresolved. No manuscript page citations are available.

### Begin with one computation and several implementations

High-level synthesis, or HLS, constructs hardware from a higher-level program and implementation settings. A directive instructs the tool about choices such as loop scheduling or array organization. Different settings can produce circuits with different resource use and execution schedules while aiming to preserve the program's specified result.

Consider summing sixteen independent products. Reusing one multiplier across iterations can save multiplier resources but require multiple cycles. Replicating multipliers can expose parallel work, but inputs must arrive fast enough and partial results still need a correct reduction. More parallel arithmetic does not establish a proportional speedup.

Loop unrolling exposes several iterations together. Pipelining overlaps work from successive iterations. A pipeline with latency eight cycles and initiation interval two can ideally accept new work every two cycles once started; an individual input still takes eight cycles to emerge. Dependences and available resources can prevent the requested schedule. These are teaching examples, not ParetoPilot benchmark configurations.

Memory organization can become limiting. If four multipliers each need two operands in a cycle while a memory supplies only two operands per cycle, arithmetic capacity alone cannot sustain all four. Splitting storage into independently accessible banks may help, but access conflicts, extra resources, and supported mapping determine whether it does. Directives interact rather than contributing independent speed factors.

### The search space is a set of allowed choices

If each of five loops has four candidate settings and three arrays each have three, the Cartesian product contains `4⁵ × 3³ = 27,648` combinations. Some may be invalid, redundant, or produce identical hardware. The number is an upper count for this constructed search space, not the paper's evaluated population.

A search method chooses which combinations to spend evaluation time on. A language model can use program structure and prior information to propose candidates, but fluent reasoning is not evidence that a candidate is feasible or globally optimal. The evaluation tool and acceptance rules determine its measured properties.

### Pareto quality describes tradeoffs among evaluated candidates

Suppose both area and latency should be minimized. Candidate A has `(area, latency) = (2,8)`, B has `(5,4)`, and C has `(8,2)`. None is at least as good as another in both dimensions. They form a nondominated set within this evaluated sample. Candidate D at `(6,6)` is dominated by B because B is smaller and faster.

A Pareto set does not specify which candidate the user should choose. A hard area limit of four makes only A feasible among A, B, and C. It also does not prove no unseen candidate dominates them. The word global in a method's name is not a proof of exhaustive search.

One possible quality metric is dominated hypervolume: the area covered between the nondominated points and a fixed worse reference point. With reference `(10,10)`, the example's covered area is `3×2 + 3×6 + 2×8 = 40`. B alone covers `5×6 = 30`. That metric improves by one third, but no circuit became one third faster. Changing reference point, units, normalization, or feasibility filtering changes the comparison.

This is an explanation of a possible metric, not an assertion that the paper uses this exact formula. The description does not establish how its 49.5% figure is calculated. Its headline must not be translated into latency, physical area, or hypervolume without recovering the definition.

### What the inspected entry point actually does

At the pinned revision, `DSEWorkflow.perform_dse` calls `llm_sampling_with_metadata` once, obtains a set of combinations, and evaluates at most `init_samples` of them. The declared default for that count is three. Each iteration modifies a synthesis script, runs HLS, extracts results, and persists a result record. [Pinned entry point](https://github.com/GEAR-SEU/ParetoPilot-DAC-26/blob/d08173f66903ed466537c9327b63addac223ee95/src/DSE_LLM.py)

Measured results are not passed into a second sampling call in this function. That observation limits what this entry point demonstrates; it does not establish that the complete training procedure or claimed experiments lack other feedback. The relationship between the released path and the reported search results still needs reconciliation.

The saved assessment identifies latency and FPGA-resource fractions extracted from synthesis reports, plus an AES example targeting a specific FPGA part with a ten-nanosecond requested clock. Those are selected artifact conditions, not proof that every headline experiment uses that target. Synthesis estimates are not measured board performance, and resource fractions are not physical chip area.

### Failure records must not become plausible measurements

The entry point substitutes `1e8` for missing latency or utilization and calls a cleanup routine for each trial. A sentinel is a marker for an unavailable result, not a measured design latency or a valid resource estimate. Downstream analysis needs an explicit failure status before ranking, averaging, or plotting the values.

The saved assessment also records trial/log deletion in the inspected utility. Reproduction would need preserved raw reports, tool exits, configurations, and seeds so failed or surprising results can be checked. Merely retaining the final JSON is insufficient if the evidence producing its numbers has been removed.

This audit did not install dependencies, load model code, invoke an API, run synthesis, or exercise cleanup. The saved assessment identifies external-code loading and broad process-name timeout cleanup as execution cautions. Source inspection must not be described as a successful benchmark run.

### Compare effort and valid output together

Evaluating twenty candidates at ten minutes each costs more serial evaluation time than evaluating one hundred at one minute each. Model preparation, sampling, rejected configurations, synthesis, and result checking belong in the complete budget. Parallel workers can shorten elapsed time while consuming more resources.

Use matched programs, input semantics, tool versions, target parts, clock constraints, resource limits, stopping rules, and feasible-output checks. Separate performance of the selected circuit from speed of the search producing it. Also test unfamiliar programs and disclose training overlap: memorized directive patterns answer a narrower question than generalization to new computation structures.

ParetoPilot connects to [two-tier generation](#explanation-dac-2026-research2545) through evaluated hardware quality and to [drcAgent](#explanation-dac-2026-research2145) through candidate/checker boundaries. Its bounded research question is whether learned proposals reach better valid tradeoffs within a complete fixed budget. Current evidence does not settle that question or establish a historical trend.

Full-paper recovery, metric definitions, author/artifact linkage, experiment correspondence, functional validation, raw trial preservation, and independent comprehension review remain open.

<span id="explanation-dac-2026-research2545"></span>

## Two-tier Verilog generation: connect intended behavior to a checked implementation

### What the source establishes

The official description combines language models, retrieval, classifiers, heuristics, simulation, and reasoning. It connects top-down generation with bottom-up functional and performance evaluation, including parallelism, critical paths, and resource sharing. Comparisons with existing generation methods are stated without numerical results. [Official Description and Authors](https://63dac.conference-program.com/presentation/?id=RESEARCH2545&sess=sess173)

Title/author searches on 2026-09-07 did not recover the manuscript. An author's indexed publication listing corroborated the title, but opening the site returned a JavaScript-only page rather than a readable paper. No manuscript page citations are available. Tier interfaces, classifier labels, prompts, tools, benchmarks, and acceptance rules remain unknown. The examples below are teaching constructions, not recovered paper experiments.

### Specify a state transition before generating code

Consider the request: make a four-bit counter with reset and enable. Four unsigned bits represent zero through fifteen. But does reset act only at a clock event? Does reset override enable? Does incrementing fifteen wrap to zero or remain at fifteen? When is the output valid?

An illustrative precise contract could say: at each rising clock edge, reset takes priority and sets state to zero; otherwise enable increments state modulo sixteen; otherwise state remains unchanged. This is one chosen contract, not a universal counter definition.

Starting at fourteen, enabled events produce fifteen and then zero. With reset and enable both asserted, the next state must be zero. A design that increments instead is wrong even if it compiles. A test that never asserts both inputs cannot reveal that priority error.

RTL, or register-transfer level, describes stored state and the logic determining its updates. It is not simply a sequential software script. Distinct blocks can operate concurrently, and clock events govern when particular state updates become visible. A generator needs these semantics, not merely plausible syntax.

### Width and output timing belong to the function

Keeping four unsigned bits of `15 + 1` gives zero; producing a five-bit value sixteen expresses different behavior. Signed interpretation creates further differences: the same four-bit pattern can represent fifteen unsigned or minus one in two's-complement interpretation. Width and signedness must remain consistent through intermediate expressions and interfaces.

A pipeline can also return the right numerical answer one clock later than required. That can be valid when the interface permits the latency and identifies valid outputs, but wrong for a consumer expecting an earlier result. Adding a register to shorten a propagation path is therefore not automatically a valid transformation.

The required record includes clock/reset behavior, widths, parameter ranges, input-valid conditions, output timing, and exceptional cases. These also determine useful tests. The source does not establish how the proposed method captures them.

### Connect generation and evaluation without changing the requirement

Top-down work starts from requested behavior and proposes structure or code. Retrieval can supply examples; a classifier can choose a prompting path; heuristics can guide selection. The description names these components without exposing their decisions. It would be unsupported to invent a module hierarchy or classifier taxonomy.

Bottom-up work examines the candidate: whether tools accept it, which behavior it exhibits, and what hardware results. A useful feedback message distinguishes syntax failure from reset-priority failure or excessive delay because each needs a different repair.

Both directions must retain a stable requirement. Editing the test to accept incorrect code can create apparent success without solving the task. Code and tests generated from the same mistaken interpretation can agree; that agreement is not independent confirmation.

### Keep the acceptance stages separate

| Stage | What success establishes | What remains open |
| --- | --- | --- |
| Parsing and elaboration | The tool can interpret the code and construct the configured model | Intended behavior |
| Simulation | Selected executions satisfy selected checks | Untested behaviors |
| Formal checking, if used | A property holds in its model under assumptions | Unstated requirements and model correspondence |
| Synthesis and implementation | A circuit can be constructed under the flow | Timing, area, and power unless separately checked |

Formal checking is included as a conceptual distinction, not a verified component of this paper. Code review can expose mistakes but is not interchangeable with exhaustive checking. Preserve failures at every stage rather than treating accepted text as completed hardware.

### Parallelism and sharing change the implementation

Suppose two independent products are needed. Two multipliers can compute them concurrently; one shared multiplier can compute them in separate cycles. Sharing may save arithmetic hardware while adding scheduling, selection logic, and storage. Validity depends on the required output rate and latency.

In an illustrative combinational design, one-nanosecond multipliers operating in parallel followed by a half-nanosecond adder give a 1.5-nanosecond arithmetic path, before other delays. Sharing a registered multiplier across cycles changes the schedule. Adding isolated gate delays is not sufficient to infer its request latency: clock periods, registers, and handshakes matter.

The critical path is the relevant longest constrained propagation path, not the longest line of source code. Wiring and loading can change it after physical implementation. The description's mention of these properties identifies evaluation dimensions, not measured hardware gains or target-device conditions.

### Count accepted designs and complete effort

If 100 attempts yield 80 parsable candidates, 50 passing functional checks, and 30 satisfying all declared requirements, final acceptance is 30%, not 80%. Whether those 30 are genuinely correct still depends on the checks. Repeated attempts on one task differ from success across independent tasks.

Report task-level outcomes, attempt limits, model/tool versions, supplied references, test preparation, failed attempts, and human intervention. Compare the same requirements, information access, checking strength, and total budget. Stronger task-specific tests can improve acceptance without establishing that code generation alone improved.

This paper and [drcAgent](#explanation-dac-2026-research2145) concern different outputs—RTL and layout edits—but both need requirements preserved through generation and feedback. The bounded hypothesis is that structured evaluation helps repair the actual failure with fewer complete attempts. It weakens if gains depend on relaxed requirements, privileged references, or omitted checking costs.

No target model, generated RTL, simulator, synthesis flow, or benchmark was executed. Full-paper recovery, precise tier behavior, evaluation conditions, independent checking, and comprehension review remain open.

<span id="explanation-dac-2026-research2145"></span>

## drcAgent: repair geometry without changing the circuit's required meaning

### What the available source establishes

The official description proposes a multimodal language-model agent using retrieved information from a design-rule knowledge graph. Generator and Fixer agents improve through adversarial, multi-turn reinforcement learning with commercial EDA-tool interaction. The evaluation is described qualitatively as industrial-scale violation correction. It gives no numerical closure rate, runtime, or final-layout quality. [Official Description and Authors, checked 2026-09-07](https://63dac.conference-program.com/presentation/?id=RESEARCH2145&sess=sess166)

Title and author searches did not recover the target manuscript or implementation. The reference to 7 nm and below motivates the problem; it does not establish the exact evaluated process. Model inputs, action syntax, graph schema, rewards, benchmarks, and checks remain unknown. No manuscript page citations are available. The explanations below are independently constructed examples and required conditions, not recovered drcAgent algorithms.

### Start with the geometry a checker sees

A layout contains shapes assigned to manufacturing layers. A wire may be represented by connected metal polygons; a connection between layers needs the permitted connecting structure. Design rules constrain properties such as minimum width, spacing, or enclosure. A rule checker reports geometry that violates the rules it was configured to check.

For a deliberately simplified one-dimensional cross-section, let three parallel wires occupy horizontal intervals `[0,2]`, `[5,7]`, and `[11,13]`. Assume neighboring wires must be separated by at least four units. The first gap is `5−2 = 3`, so it fails. The second is `11−7 = 4`, so it passes.

Moving the middle wire to `[6,8]` makes the first gap four, but the second becomes three. The selected violation disappears while a new one appears. If the two outer wires cannot move, their inner edges leave a nine-unit region. Two required gaps of four plus middle-wire width two require ten units. No position for that middle wire can satisfy this simplified constraint set.

That infeasibility matters. Trying more horizontal moves cannot solve it. A valid alternative would need some other permitted change, such as moving an outer wire or choosing a different route. Whether those changes are allowed depends on the actual layout, connections, layers, and rules. The example does not imply drcAgent uses interval geometry or these actions.

### A clean rule report is not complete circuit correctness

Deleting the middle wire removes the two spacing relationships, but may disconnect terminals that must remain connected. Shortening it can likewise detach an endpoint. Adding metal can create an unintended connection. The intended circuit therefore has to survive the repair, not just the selected geometric check.

Other requirements can change too. A longer detour can add resistance and capacitance; a new connection between layers can add delay and require its own legal surrounding geometry. A repair accepted by a local spacing check can still fail connectivity, timing, or another manufacturing rule.

A defensible completion condition identifies the required checks, their scope, and any accepted exceptions. It distinguishes a local violation count from acceptance of the whole relevant layout. The official description does not expose enough information to establish drcAgent's complete acceptance predicate.

### A knowledge graph must connect the rule to its applicability

A knowledge graph represents entities and relationships. In this task, useful entities could include rule identifiers, layer types, geometric predicates, and exceptions. Useful relationships could indicate which conditions activate a rule or which neighboring rules an edit can affect. These are possible requirements, not the recovered contents of drcAgent's graph.

Retrieval selects information for the agent's current decision. A spacing rule from a different layer or process revision can be textually relevant yet inapplicable. A retrieved threshold without its exception conditions can also lead to a wrong edit. The retrieval result needs enough identity and context to apply the actual rule correctly.

Multimodal input means more than one kind of representation can be supplied, such as visual and textual information. It does not establish that a model's view contains exact coordinates, connectivity, or every nearby constraint. A screenshot can help describe a violation while still omitting information needed for a legal geometry edit. The target's exact input and coordinate interface remain unrecovered.

### Separate an attempted edit from a checked new state

An agent can propose an action, a tool can attempt it, and a checker can evaluate the resulting layout. Those are three different events. A tool rejecting an edit must not be recorded as a successfully changed layout. A checker result for the previous layout must not be attached to the new one.

For a reproducible iteration, retain the starting layout revision, selected violation, retrieved rule revision, proposed edit, tool outcome, resulting layout revision, and relevant check results. This is an evidence checklist, not a claim that the paper logs these fields.

Repeated repairs can oscillate. In the interval example, moving the middle wire right fixes one gap; moving it left fixes the other. Without detecting the incompatible constraints or changing the available action, the process can alternate forever. A termination limit prevents unlimited work but does not turn the last candidate into a valid result. Unresolved cases need an explicit failed or incomplete status.

### What adversarial training must demonstrate

The description names a Generator and a Fixer in self-play. Conceptually, one can supply challenging cases while the other learns correction actions. That can expose cases missing from a static collection. However, the source does not specify how cases are generated, what they must preserve, or how rewards are computed.

If generated cases are infeasible under permitted edits, penalizing the Fixer for not solving them measures something different from poor correction. If rewards count only disappearing markers, deleting required geometry could appear favorable to an inadequate objective. These are possible failure modes to test, not observed behavior of drcAgent.

Training and evaluation also need separation. Success on cases produced by the same Generator can reflect shared patterns rather than general repair ability. Test unfamiliar layouts, rule classes, and declared process-transfer conditions, while retaining failed cases and any manual preparation. A new process node in the motivation does not establish demonstrated portability.

### Evaluate closure and effort with stable denominators

Suppose an initial layout has 100 violation markers. A sequence removes 90 but creates 20 elsewhere. Counting removed original markers gives 90%, while the final layout still contains 30 markers under this simplified accounting. Neither number establishes full closure. Real checkers can also split or merge markers, so marker identity and rule class matter when interpreting count changes.

Across designs, report how many reach all required acceptance conditions, not only an average marker reduction. Include tool failures, infeasible cases, timeouts, retries, and invalid repairs. Separate per-iteration time from complete repair time and model inference from commercial-tool execution. Training, knowledge preparation, licenses, and human intervention affect reproducibility and total effort.

Baselines need the same starting layouts, rule decks, permitted edits, checks, and budgets. A stronger checker or more permissive edit set can change results independently of the model. The official description's qualitative result is insufficient to attribute a numerical benefit to retrieval, adversarial training, or the combined workflow.

### What this adds to the cross-paper story

drcAgent connects the [AI-assisted EDA theme](../themes/ai-assisted-eda.md) to [physical design](../themes/physical-design-and-manufacturing.md): learning proposes changes, but geometry and circuit requirements determine whether those changes are usable. It also connects to [verification](../themes/verification-and-validation.md), because the checker defines which failures are observable and which properties remain untested.

The bounded hypothesis is that rule-aware feedback can reduce the effort required to reach a valid repaired layout. It would be weakened if graph preparation, rejected edits, repeated violations, or final cleanup consume the apparent saving. The present evidence motivates that test; it does not establish a historical trend, autonomous closure, or superiority over matched baselines.

No drcAgent model, commercial EDA tool, training loop, layout repair, or benchmark was executed. Full-paper recovery, exact rule/action/reward semantics, complete acceptance checks, quantitative conditions, and independent comprehension review remain open.
