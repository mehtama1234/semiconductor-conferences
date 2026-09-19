## Design automation must connect the specification to a usable artifact

A design task can begin with written requirements and end with a schematic, a physical model, or a corrected protocol implementation. Generative automation proposes some part of that artifact. The essential question is whether the generated result preserves the required relationships and passes the checks appropriate to its intended use.

A visually plausible model, a syntactically valid file, and an electrically correct design are different outcomes. The evaluation must identify which outcome it measures and which later steps remain necessary.

<span id="explanation-dac-2026-research561"></span>

## Cupilot: CUDA-kernel evolution is a measured program-and-hardware search

### What a CUDA optimization changes

A CUDA kernel is a program executed by many GPU threads. Its performance depends on the algorithm, memory addresses, thread and block mapping, synchronization, atomics, numerical precision, input shape, compiler decisions and the GPU's memory and execution resources. Changing one of these can improve throughput while changing the result or making another input shape slower.

The optimization target must therefore include a correctness rule. A kernel is not accepted because it compiles or because one output looks plausible. The required output comparison, numerical tolerance, supported shapes and error behavior must be defined before performance is compared.

### What strategy coordination contributes

The captured Cupilot framework uses multiple agents coordinated by search strategies to evolve CUDA kernels. Different roles can propose algorithm changes, tune launch and memory parameters, inspect profiler evidence, or reject candidates that fail correctness. Coordination is useful only when these roles exchange measured evidence and operate under one shared acceptance boundary. Several agents repeating an unsupported guess do not create independent evidence.

The search state should retain the source kernel, input shape, compiler configuration, GPU, measured result, correctness result and change made. Without that state, the system cannot distinguish a real improvement from a measurement artifact or a candidate that succeeded only because a test was weakened.

### What a valid evaluation must include

Compilation and profiling are part of the optimization cost. A candidate can appear faster because of cache state, GPU clock behavior, warm-up, input shape, compiler version or an incomplete timing interval. Use a fixed measurement protocol with warm-up and repetitions, report variance, include compilation and search cost, and record failed candidates. Test unseen inputs and, if portability is claimed, other GPU architectures and toolchain versions.

The comparison must use the same functional workload and acceptance rule for manual tuning, single-agent generation and Cupilot. It should report accepted-kernel rate, end-to-end latency or throughput, compile and search time, resource use, and the number of candidates evaluated. A benchmark-only speedup does not establish transfer to another kernel or GPU.

### What the record establishes and where it stops

The captured description names manual kernel tuning and single-agent code generation as comparisons and claims kernel-evolution efficiency qualitatively. It does not expose the kernels, inputs, correctness oracle, search budget, GPU models, compiler settings, speedups, compile time, cost, failures or cross-GPU results.

The evidence supports a coordinated multi-agent CUDA-evolution proposal. It does not establish general kernel correctness, transferable speedup or cost-effective optimization without reproducible functional and performance evaluation.

[Observed paper card](../observed-subthemes/generative-design-automation.md#paper-dac-2026-research561)

<span id="explanation-dac-2026-research2829"></span>

## LLM-assisted Signal Temporal Logic transformation must preserve meaning across time semantics

### What is being transformed

Signal Temporal Logic (STL) describes conditions over signals and time. A formula can constrain a numerical predicate, require it to remain true over an interval, require it to become true within an interval, or relate events with an until condition. The meaning depends on the signal names, units, operator nesting, interval endpoints, strictness, sampling model and numerical comparison rules.

This is why transformation is not ordinary text translation. The target formula is correct only if it accepts and rejects the same traces under the declared semantics. A formula can parse successfully while changing an interval boundary, moving an operator over a predicate, or applying a condition to the wrong signal.

### What the structured intermediate representation contributes

The captured workflow uses two LLM-assisted stages with a structured intermediate representation (IR) between source and target forms. The IR can make the semantic structure explicit: predicates, signals, units, temporal operators, interval bounds, nesting and connections between subformulas. It gives the system a place to check types and boundaries before producing target syntax.

The IR is not automatically a proof. If its schema omits a strict inequality, unit conversion, boundary convention or numerical robustness rule, both stages can agree on an incomplete meaning. The parser and serializer must preserve the full structure, and malformed or unsupported constructs must be rejected rather than silently approximated.

### What the two stages should be checked against

Separating semantic decomposition from target rendering can make failures easier to locate. The source formula should be parsed and normalized, the IR should be validated, and the target should be parsed back into a comparable form. Checks should include operator scope, interval endpoints, signal identity, units, sampling and numerical semantics.

Semantic validation then needs more than a few passing examples. Use formal equivalence where the representation and signal model permit it; otherwise use trace-based testing that targets boundaries, nested operators, violations, long holds, missing samples and numerical tolerances. The test must report cases that cannot be decided and transformations that need human review.

### What the record establishes and where it stops

The captured description names manual transformation and single-stage LLM transformation as comparisons and claims transformation efficiency qualitatively. It does not expose the formula set, source and target representations, temporal semantics, parser or solver settings, semantic-equivalence procedure, coverage, runtime, failure cases or expert review.

The evidence supports a two-stage LLM-assisted transformation proposal and identifies the structured IR as the key semantic boundary. It does not establish that the generated formulas are equivalent or suitable as verification artifacts without independent formal or simulation validation.

[Observed paper card](../observed-subthemes/generative-design-automation.md#paper-dac-2026-research2829)

<span id="explanation-dac-2026-research2642"></span>

## LLM4SDC: generated timing constraints must be checked as design intent, not just parsed as text

### What an SDC file actually specifies

Static timing analysis computes whether signal paths can meet required arrival times. An SDC file supplies assumptions for that computation: clocks and their relationships, input and output timing, uncertainty, operating conditions, and exceptions such as false or multicycle paths. Those commands define which paths are analyzed and what limits are applied.

This makes SDC generation a semantic task. A file can be syntactically valid and accepted by the timing tool while describing the wrong clock, interface delay or path exception. Under-constraint can hide a real violation. Over-constraint can reject a design that is actually valid or distort optimization. A text comparison is therefore insufficient; the effect on the timing graph must be compared.

### What the multi-agent workflow is intended to do

The captured LLM4SDC method uses multiple language-model agents for SDC generation and benchmarking. A useful decomposition could assign one agent to translate the design specification, another to challenge clock and interface assumptions, and a checker to evaluate the resulting constraints. The value comes from the evidence each role introduces, not from the number of agents. If all agents repeat the same incomplete description, the workflow can produce a more confident version of the same error.

The generated file must remain linked to its inputs: the RTL or netlist, clocks, interfaces, library and process assumptions, timing corners, and the intended signoff rules. Without those inputs, the workflow cannot determine whether a command expresses the design or merely makes the timing report easier to satisfy.

### How benchmarking must distinguish a good constraint from a convenient one

A benchmark should compare generated constraints with an authoritative reference or a formally justified specification. It should evaluate semantic differences, not only exact text. For the same netlist, libraries and corners, it should measure analyzed-path coverage, preserved and missing violations, timing correlation, and whether the generated exceptions correspond to documented behavior.

The benchmark must test both failure directions. An under-constrained file leaves paths unchecked. An over-constrained file adds relationships or limits that are not real. Both can produce a report that looks orderly. Expert review is needed for assumptions that cannot be inferred from the netlist, especially external interface timing and intentional protocol exceptions.

### What the reported result can and cannot establish

The captured description names manual SDC authoring and single-agent generation as comparisons and claims constraint-generation efficiency qualitatively. It does not provide the design set, clock and interface specifications, reference constraints, timing tools, process corners, semantic equivalence method, path coverage, timing correlation, runtime, failed cases or expert review.

The record therefore supports a proposal for using multiple LLM roles in constraint generation and benchmarking. It does not establish that the generated files preserve design intent, produce trustworthy timing analysis, or are ready for signoff. Those claims require reproducible timing runs and review of the assumptions that the timing tool cannot infer automatically.

[Observed paper card](../observed-subthemes/generative-design-automation.md#paper-dac-2026-research2642)

<span id="explanation-dac-2026-research2443"></span>

## Stitch: assertion-guided repair is only as complete as the protocol requirements being checked

### What the repair problem is

An on-chip protocol is a set of rules for how hardware blocks exchange requests, data, responses, credits, resets and errors over time. An implementation bug is not merely a wrong line of RTL. The change must restore the intended sequence while preserving behavior that was already correct. That includes ordering, back-pressure, repeated transactions, reset entry and exit, and interactions with other blocks when those are part of the protocol.

### What an assertion contributes

An assertion is an executable condition over signals and time. It can state, for example, that a response follows a request under a permitted condition, that a response is not produced without a request, or that a valid transfer is held until acceptance. The assertion gives the patching system a machine-checkable failure signal. This is more useful than asking a language model to judge its own patch from text alone because the checker evaluates an observed execution or formal state space.

The assertion is still only a projection of the full requirement. Passing one assertion proves that the checked condition held in the checked scope. It does not prove that unasserted ordering, reset, liveness, illegal-input handling, cross-block interaction or implementation timing is correct. Assertion coverage is therefore part of the result, not a background detail.

### What the LLM patch loop changes

The captured Stitch workflow uses an LLM to propose a code change, runs assertion-guided checking, and uses the resulting failure or pass information to guide another patch. The loop can search edits faster than manual trial and error when the failure is localized and the available assertions describe the relevant contract. It can also produce a patch that satisfies the visible counterexample while changing behavior outside the checked conditions.

The workflow must retain the complete failure context: the failing trace or formal obligation, the affected signals, the original requirement, the patch diff and the checks run after the patch. Without that record, it is not possible to tell whether the model repaired the cause, masked the symptom, weakened the assertion or introduced a new violation.

### What acceptance requires after a patch

Patch acceptance needs a regression boundary. Rerun all relevant assertions and tests, including reset and repeated-transaction cases, then check for deadlock, ordering, liveness and illegal-input failures. For deployable RTL, synthesis, timing, clock-domain and integration checks are separate gates. A patch that passes simulation can still fail formal exploration, synthesis or timing; a patch that passes assertions can still violate an unencoded system requirement.

### What the record establishes and where it stops

The captured description establishes an assertion-guided LLM repair proposal with manual patching and unguided LLM repair as named comparison points. It reports protocol-repair efficiency qualitatively. It does not expose the protocol designs, assertion completeness, checker settings, accepted and rejected patches, regression results, synthesis or timing impact, runtime, or human-review effort. The evidence therefore supports the mechanism and its evaluation question, not a general claim that LLM-generated protocol patches are correct or ready for implementation.

[Observed paper card](../observed-subthemes/generative-design-automation.md#paper-dac-2026-research2443)

<span id="explanation-dac-2026-research241"></span>

## PCBgen: specification-to-schematic search needs external electrical evaluation, not only language-model plausibility

### What a power-supply specification becomes

A power-supply specification defines electrical targets and constraints such as input and output ranges, current, ripple, efficiency, transient behavior, stability and component limits. A schematic must choose a topology, components, connections and parameter values that jointly satisfy those requirements.

The decisions are coupled. Changing an inductor or compensation value can change stability and transient response. Changing a topology changes the available operating range and component relationships. A syntactically valid netlist is therefore not an accepted design until the required electrical behavior is checked.

### How the framework reduces the search

PCBgen is described as combining PCB knowledge-graph retrieval, constraint-aware pre-filtering, a multimodal intermediate representation and SPICE-in-the-loop training-free Group Relative Policy Optimization. The knowledge graph can retrieve known component, topology and design relationships. Pre-filtering can reject candidates that violate explicit constraints before simulation.

The source says the pipeline compresses a space of up to 10^20 candidates to roughly 10^3 simulatable designs. Such compression is useful only if the filters preserve valid candidates and if the denominator describes the same design decisions. A filter that silently removes hard or failed cases can make the remaining search look efficient while changing the task.

### What the intermediate representation must preserve

A multimodal intermediate representation connects the specification, retrieved knowledge, schematic, parameters and simulation results. It must preserve component identity, net names, pin direction, units, parameter values, operating conditions, constraints and the reason a candidate passed or failed.

If it loses a unit, connection or sign, later steps can reason consistently over an incorrect circuit. The representation also needs to carry failed simulation state, convergence diagnostics and unresolved constraints so the next action addresses a real problem rather than generating another plausible variant.

### What SPICE-in-the-loop and TF-GRPO change

SPICE evaluates the electrical behavior of a candidate circuit under a defined model and operating condition. It can provide objective signals for output voltage, current, ripple, transient response, stability or other requirements. It can also fail to converge, making “no result” different from “design fails the specification.”

Training-free GRPO can compare groups of candidate actions using simulation-derived rewards without updating model parameters. The reward must include all required constraints and define how failed simulations, invalid netlists, out-of-range components and tradeoffs are ranked. Optimizing one reward score does not prove that every specification requirement passes.

### How to interpret the reported evaluation

The captured description reports a 336-case benchmark across six topology families and three design regimes, up to 57% improvement in topology adaptation, Pass@5 rising from 41% to 74%, more than 50% reductions in token use and wall-clock time versus LLM-only baselines, and a 24-case comparison with human designers using vendor tools. It reports 3.70× and 4.74× speedups for topology selection and schematic verification, comparable Pass@1 and overall ROI of 4.39×.

These metrics need definitions. Pass@k must state what counts as a pass and whether candidates are electrically simulated. Topology adaptation must specify the source and target regimes. ROI must include simulator, model, compute, tool, human review and correction costs. A human comparison needs matched specifications, libraries, vendor-tool settings and acceptance criteria.

### What the record establishes and where it stops

The official description establishes a closed-loop specification-to-schematic framework using retrieval, constraints, structured state, SPICE evaluation and training-free policy comparison. It reports detailed benchmark and human-comparison numbers. It does not expose circuit models, convergence treatment, electrical pass criteria, failed candidates, library transfer, human-effort accounting or hardware validation.

The [PCBgen](../observed-subthemes/generative-design-automation.md#paper-dac-2026-research241) record is evidence of a reported agentic PCB-design workflow, not proof of general electrical correctness or manufacturing readiness. The explanation separates specification semantics, search reduction, structured state, external simulation, policy reward and end-to-end design acceptance.

<span id="explanation-dac-2026-research1991"></span>

## PCBgen3D: generating a 3D PCB model requires reconciling datasheet evidence with geometry and connectivity checks

### What the input actually contains

A manufacturer datasheet can describe one component through orthographic drawings, dimension tables, text, symbols and images. These views are different representations of the same physical object. A usable CAD model must determine which dimensions refer to the same feature, establish a coordinate system, place the body and pins, and preserve package identity and orientation.

The task is not image copying. A dimension table may be authoritative for a height while a drawing shows the feature's location. Text may describe a pin numbering convention that is not obvious from the image. Conflicting or incomplete views require a rule for selecting evidence or marking the result uncertain.

### What a graph representation contributes

A graph can represent package parts, pins, dimensions and relationships such as containment, alignment, adjacency and electrical correspondence. The graph makes dependencies explicit: changing the body height may affect clearances, while changing pin numbering affects the component's connectivity representation.

The graph is only as reliable as its extraction. A missing edge can produce a geometrically correct body with incorrect pin relationships. An incorrectly linked dimension can make every downstream module consistent with the wrong value. The framework needs checks against the source datasheet and a record of unresolved ambiguity.

### What the dynamic task graph changes

PCBgen3D is described as decomposing modeling into adaptive subtasks for extraction, planning and refinement. A task graph can schedule dimension extraction, geometry generation, pin placement, format conversion and validation according to the dependencies of a particular package.

Dynamic decomposition can handle unusual package types by adding or changing subtasks. It also introduces state and dependency problems. If a corrected dimension changes a solid, dependent pin positions, clearances and output files must be recomputed. The system needs completion criteria for each task and a rule for propagating changes rather than accepting an outdated downstream result.

### What self-correction must observe

An iterative loop is useful only when it receives an error signal that can distinguish a valid artifact from a plausible one. A model's own description of its output may reproduce the same assumption. Independent checks can include dimensional comparison against the datasheet, CAD solid validity, pin-count and pin-position rules, clearance checks, coordinate consistency and manufacturing or assembly constraints.

The loop must say which failure triggered a repair, what change was made and whether the complete artifact was rechecked afterward. Fixing a pin location can break a clearance; changing a body dimension can invalidate a mounting surface. Repair rate and unresolved cases belong in the denominator, not only successfully repaired examples.

### What the reported evaluation establishes

The captured description says PCBgen3D is evaluated on components from varied package types and manufacturers and outperforms a state-of-the-art general-purpose MLLM on industrial-grade PCB 3D-modeling tasks. It does not provide geometric accuracy, dimensional tolerance, connectivity validity, repair success, unresolved-case rate, runtime, human effort, CAD format, checker or manufacturing validation results.

The comparison needs the same datasheets, component families, output format, geometric tolerance, review policy and accepted-output definition. Manual effort should include interpreting ambiguous tables and correcting generated files. A direct generative model may also differ in prompting, tool access and validation, so those conditions must be held constant.

### What the record establishes and where it stops

The official description establishes a graph-based multimodal-LLM workflow with extraction, task planning, dynamic subtask decomposition, refinement and iterative self-correction for datasheet-driven PCB 3D models. It reports a qualitative industrial-task comparison across package types and manufacturers. It does not establish geometry or connectivity acceptance, manufacturing readiness, repair reliability, runtime or reduced human effort.

The [PCBgen3D](../observed-subthemes/generative-design-automation.md#paper-dac-2026-research1991) record is evidence of a reported CAD-generation framework, not proof that its outputs are production-usable. The explanation separates source interpretation, graph dependencies, task scheduling, independent correction signals and complete artifact validation.

## A design contains several representations of the same intent

A schematic describes components and electrical connections. A board layout assigns physical locations and conductive paths. A three-dimensional model adds geometry used for checking fit, clearances, and assembly. These representations need to agree where they describe the same objects and relationships.

Generating one representation from another can save manual work. It can also introduce missing components, incorrect dimensions, or broken associations. The generation process needs checks against the authoritative inputs rather than relying only on the appearance of its output.

## PCBgen3D generates a physical model

PCBgen3D's captured method uses a graph-based multimodal model with self-correction to generate board models. A multimodal model accepts or produces more than one information form, such as text and images. A graph can represent components and their relationships. [Recorded evidence](../observed-subthemes/generative-design-automation.md#paper-dac-2026-research1991)

The important questions are what geometric and connectivity requirements are checked, which errors trigger correction, and whether the repaired model agrees with the board data. The description does not establish geometric accuracy, repair rate, runtime, or reduced human effort. A self-correction procedure needs its own evaluated acceptance rule.

## Pcbgen produces schematics and parameter choices

Pcbgen's captured record concerns converting a specification into a schematic and tuning parameters. Parameter choices can change whether a circuit operates correctly over its required range. Selecting familiar components or generating a well-formed schematic does not establish that behavior. [Recorded evidence](../observed-subthemes/generative-design-automation.md#paper-dac-2026-research241)

Evaluation should state the requirements, component-library assumptions, electrical checks, and manual changes required before the result is usable. The current record leaves electrical correctness, iterations, runtime, and board diversity unresolved. Transfer to another specification or library remains a separate question.

## Stitch repairs behavior under assertion guidance

Stitch's captured method uses assertions to guide language-model patches for on-chip protocols. A protocol defines permitted interactions, including request ordering and responses. An assertion expresses a condition used to check those interactions. [Recorded evidence](../observed-subthemes/generative-design-automation.md#paper-dac-2026-research2443)

A patch may satisfy one assertion while breaking behavior that the assertion does not cover. The test must therefore preserve the complete relevant requirement set and include checks for regression. Patch acceptance, synthesis impact, runtime, and human review remain unreported in the captured description.

## Correction requires a trustworthy source of error information

An automated loop can revise an output many times. Its usefulness depends on what identifies the error and how that information reaches the next decision. Repeating a model's own judgment can reproduce the same mistaken assumption. A separate geometry, electrical, simulation, or formal check can provide a different source of evidence, within that check's scope.

Record each failed requirement and the action taken to address it. Check the entire artifact again after a change. Count cases that remain unresolved or require a human correction instead of excluding them from the denominator.

## The outcome that should be compared

Use the same input specifications, libraries, tool settings, and acceptance criteria. Measure accepted usable outputs, complete elapsed time, computing cost, and human effort. Separate preparation of reusable knowledge from per-task execution, and state how many tasks reuse that preparation.

These papers concern different artifacts, so their scores are not directly interchangeable. Their shared question is whether generation plus checking reduces the total effort of producing a correct design under the stated requirements. That outcome needs a complete evaluation of the generated artifact and its remaining work.
