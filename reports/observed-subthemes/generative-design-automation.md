# Generative design automation

This subject has 6 records in the selected sample. This page explains where it fits, then presents all captured paper evidence without shortening the measurements or limitations.

[Definitions used in the paper records](../reading-guide-v1.md)

## Understand the parent subject first

- [AI assisted EDA](../themes/ai-assisted-eda.md)

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

## Compare the results carefully

First identify the inputs and required output quality. Then identify the limited resource: time, memory, communication, energy, circuit area, or correctness coverage. Ask which part of the method reduces that cost and which new cost it adds. Compare numbers only when the experiments hold these conditions sufficiently similar.

A conference description may explain the proposal while omitting the full experiment. An author preprint link may have been coded from its abstract. The source classification does not by itself establish that every table was read. Missing locations remain visible below.

## Complete captured evidence

These are evidence records, not substitutes for the explanations above. Each record preserves its problem, proposed method, measurements, comparison conditions, and source limits. A populated record does not establish that its mechanism has been fully explained or independently verified.

<span id="paper-dac-2026-research1991"></span>

### PCBgen3D: A Self-Correcting Graph-Based MLLM Framework for Automated PCB 3D Models Generation

DAC 2026 · Record: `dac-2026-research1991`

[Read the step-by-step explanation](#explanation-dac-2026-research1991)

**Updated source-backed reading card**

Reviewed 2026-09-08. Reconciles the PCBgen3D card with the captured official DAC description; explains datasheet-to-CAD extraction, graph representation, multimodal task decomposition, dynamic task graphs, self-correction and the distinction between visually plausible geometry and validated PCB/CAD artifacts.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Creating a usable three-dimensional PCB component model from manufacturer datasheets requires extracting dimensions, views, text and relationships and converting them into consistent geometry. Manual interpretation is slow and can introduce geometric or connectivity errors.

**Mechanism / artifact:**

PCBgen3D: self-correcting graph-based multimodal LLM framework with modules for data extraction, task planning and process refinement, an adaptive dynamic task graph that decomposes modeling into subtasks, and an iterative self-correction loop.

**Workload — the work tested:**

Datasheet-driven PCB components across package types and manufacturers; dataset size, CAD formats, package standards, geometric tolerances, pin/connectivity rules and manufacturing checks are unspecified.

**Hardware and manufacturing assumptions:**

EDA/CAD and multimodal-LLM generation workflow; model versions, context inputs, compute, CAD kernel, file formats, geometry checker, connectivity validator and manufacturing rules are unspecified.

**Baseline — the comparison method:**

Manual PCB 3D modeling

Direct generative model

State-of-the-art general-purpose multimodal LLM

Component families, CAD representation, human review, geometric tolerance, connectivity and runtime boundaries are unspecified

**Reported measurements:**

The captured official description reports that PCBgen3D outperforms a state-of-the-art general-purpose MLLM on industrial-grade PCB 3D-modeling tasks across components and manufacturers, but provides no geometric accuracy, connectivity validity, repair rate, runtime or human-effort numbers.

**Limits on the conclusion:**

A datasheet may contain orthographic drawings, dimensions, text descriptions, tables and images that refer to the same component. A usable 3D model must reconcile those sources into a coordinate system, solid geometry, pin locations, orientation and package identity. A model that looks plausible can still have a wrong dimension, missing feature or incorrect pin association.

A graph can represent components, geometric parts, pins and relationships such as adjacency, alignment, containment or electrical correspondence. A graph representation makes dependencies explicit, but its usefulness depends on how nodes and edges are extracted and checked against the authoritative datasheet. An incorrect graph can make later generation consistently wrong.

The dynamic task graph decomposes modeling into subtasks such as extracting dimensions, planning geometry, generating parts, placing features and refining errors. Dynamic decomposition can adapt when a package has unusual structure, but it adds scheduling, state and dependency management. The framework must define when a task is complete and how changes propagate to dependent geometry and connectivity.

Self-correction requires an error signal. A model's own textual judgment can repeat the same mistake; an independent CAD geometry checker, dimensional comparison, pin-rule validator or manufacturing constraint checker supplies a separate source of evidence. After a repair, the entire artifact must be checked again because changing one feature can break clearance, alignment or connectivity elsewhere.

The source reports better performance than a general-purpose MLLM on industrial-grade tasks across package types and manufacturers, but does not expose geometric tolerances, connectivity validity, repair success, unresolved cases, runtime, human effort, CAD formats or manufacturing validation. The record establishes a reported graph/MLLM generation proposal and qualitative comparison, not proof of usable production CAD output.

**Source and location**

Evidence tier: Primary captured official DAC description only; no full paper extraction, pcbgen3d/model/cad artifact reproduction or independent geometry, connectivity, repair, runtime, human effort and manufacturing validation. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH1991)

DAC 2026 official description and data/review-packets/dac-2026-research1991.json: datasheet-driven 3D PCB component generation; 2D views/text/dimension tables; graph-based multimodal LLM; extraction/planning/refinement modules; dynamic task graph; iterative self-correction; package/manufacturer-diverse dataset; qualitative outperformance over general-purpose MLLM; omitted geometry, connectivity, repair, runtime, human-effort and manufacturing conditions.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** manual PCB modeling

direct generative model

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH1991

**Hardware or process assumptions:** EDA/MLLM generation workflow; CAD formats and compute assumptions are unspecified.

**Limits:** No geometric accuracy, connectivity validity, repair rate, runtime, or human-effort results are reported.

Self-correction may depend on board-specific rules.

Official description only; CAD and manufacturing validation is required.

**Method or artifact:** Graph-based MLLM generation with self-correction.

**Metrics:** Automated 3D-model generation is claimed qualitatively

**Problem:** Generating usable 3D PCB models from design specifications requires resolving geometric and connectivity errors.

**Workload or benchmark:** PCB design specifications and 3D models; board families, constraints, and evaluation are unspecified.

</details>

<span id="paper-dac-2026-research241"></span>

### Pcbgen: Self-Evolving LLM Agent for Specification-to-Schematic PCB Design with Parameter Tuning

DAC 2026 · Record: `dac-2026-research241`

[Read the step-by-step explanation](#explanation-dac-2026-research241)

**Updated source-backed reading card**

Reviewed 2026-09-08. Reconciles the PCBgen card with the captured official DAC description; explains specification-to-schematic search, PCB knowledge-graph retrieval, constraint pre-filtering, multimodal intermediate representation, SPICE-in-the-loop training-free GRPO, closed-loop tuning and the exact benchmark, Pass@5, speedup and ROI claims.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Turning PCB power-supply specifications into a valid schematic requires selecting a topology, components and parameter values that satisfy electrical constraints. The combinations form a large search space, and a syntactically valid schematic can still fail simulation or operating requirements.

**Mechanism / artifact:**

PCBgen: a closed-loop specification-to-schematic framework using PCB knowledge-graph retrieval, constraint-aware pre-filtering, a multimodal intermediate representation and SPICE-in-the-loop training-free Group Relative Policy Optimization (TF-GRPO) for topology and parameter decisions.

**Workload — the work tested:**

Power-supply designs across six topology families and three design regimes in a 336-case benchmark, plus a 24-case comparison with human designers using vendor tools; exact specifications, component libraries, SPICE models, pass criteria and task split are not fully exposed.

**Hardware and manufacturing assumptions:**

EDA schematic and SPICE simulation flow with PCB knowledge graph and component library; simulator version, model fidelity, convergence policy, hardware, token budget, human review and manufacturing constraints are unspecified.

**Baseline — the comparison method:**

LLM-only static generation

Manual schematic design with existing vendor tools

Static LLM generation

Case split, simulator, component library, electrical pass criteria, human effort and runtime boundaries are unspecified

**Reported measurements:**

The captured official description reports search-space compression from up to 10^20 candidates to roughly 10^3 simulatable designs, up to 57% improvement in topology adaptation, Pass@5 increase from 41% to 74%, over 50% reductions in token usage and wall-clock time versus LLM-only baselines, 3.70× and 4.74× speedups for topology selection and schematic verification in a 24-case human comparison with comparable Pass@1, and overall ROI of 4.39×; exact metric definitions and conditions are not exposed.

**Limits on the conclusion:**

A PCB specification states electrical targets and constraints, but a schematic must choose a topology, components, connections and parameter values before SPICE can evaluate it. The choices are coupled: changing a component can change operating points, stability, ripple, current stress and the feasible range of other values.

PCB-KG retrieval can restrict generation to known components, topologies or design relationships. Constraint-aware pre-filtering can remove candidates that violate explicit requirements before expensive simulation. These steps reduce search only if the graph and constraints are complete; an incorrect or overly restrictive filter can exclude the best valid design.

A multimodal intermediate representation gives the agent a structured state between specification, schematic, simulation result and next action. It must preserve component identity, nets, parameter values, units, constraints and failure information. If the representation loses a unit or connection, later reasoning can be internally consistent but electrically wrong.

SPICE-in-the-loop supplies an external electrical signal for the closed loop. Training-free GRPO can compare groups of candidate actions using simulation-derived rewards without parameter training, but the reward must reflect all required constraints and handle convergence failures, unstable circuits, invalid models and simulation cost. A high reward on one metric can hide a failure on another.

The description reports strong benchmark and human-comparison results, including Pass@5, topology adaptation, token/time, speedup and ROI figures, but does not expose case specifications, simulator models, pass criteria, failed/invalid candidates, human effort accounting, component-library transfer or hardware validation. The results establish a reported agentic simulation workflow, not general electrical correctness or manufacturing readiness.

**Source and location**

Evidence tier: Primary captured official DAC description only; no full paper extraction, pcbgen code/simulation artifact reproduction or independent electrical, convergence, transfer, human effort and hardware validation. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH241)

DAC 2026 official description and data/review-packets/dac-2026-research241.json: spec-to-schematic power-supply design; PCB-KG retrieval; constraint-aware pre-filtering; multimodal IR; SPICE-in-the-loop TF-GRPO; 10^20 to ~10^3 search compression; 336 cases, six topology families, three regimes; 57% TA; Pass@5 41% to 74%; >50% token/time reduction; 24-case human comparison; 3.70×/4.74× speedups; 4.39× ROI; omitted simulator, pass, human, transfer and hardware conditions.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** manual schematic design

static LLM generation

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH241

**Hardware or process assumptions:** EDA schematic and simulation flow; component libraries and electrical constraints are unspecified.

**Limits:** No electrical correctness, iterations, runtime, human effort, or board-diversity results are reported.

Agent self-evolution may encode library or task bias.

Official description only; simulation and hardware review are required.

**Method or artifact:** Self-evolving LLM agent for schematic generation and parameter tuning.

**Metrics:** Automated PCB design efficiency is claimed qualitatively

**Problem:** Translating PCB specifications into valid schematics requires iterative component and parameter decisions.

**Workload or benchmark:** PCB specifications and schematic designs; board types, rules, and evaluation are unspecified.

</details>

<span id="paper-dac-2026-research2443"></span>

### Stitch: Assertion-Guided Patching of On-Chip Protocol Implementations Using LLMs

DAC 2026 · Record: `dac-2026-research2443`

[Read the step-by-step explanation](#explanation-dac-2026-research2443)

**Updated source-backed reading card**

Reviewed 2026-09-08. Reconciles the Stitch card with the captured official DAC description; explains assertion-guided protocol repair and separates assertion satisfaction from complete behavioral correctness.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Repairing an on-chip protocol implementation requires changing RTL so that the intended interaction behavior is restored without breaking legal ordering, response, reset, timing or other requirements.

**Mechanism / artifact:**

Stitch: an assertion-guided LLM patching workflow that uses protocol assertions as feedback while proposing repairs to RTL or protocol implementations.

**Workload — the work tested:**

On-chip protocol RTL implementations and assertion sets; designs, protocol families, simulators, repair set, assertion language, failure distribution and case split are unspecified.

**Hardware and manufacturing assumptions:**

RTL simulation/formal-verification flow for on-chip protocols; synthesis, timing, clock-domain, reset, implementation and downstream integration assumptions are unspecified.

**Baseline — the comparison method:**

Manual patching

Unguided LLM repair

Assertion set, simulator/formal engine, testbench, patch acceptance rule, synthesis checks and human-review boundary are unspecified

**Reported measurements:**

The captured official description claims qualitative protocol-repair efficiency; it does not report accepted-patch rate, assertion coverage, regression rate, repair time, synthesis impact or human effort.

**Limits on the conclusion:**

An assertion is an executable condition over selected signals and time points. Passing it shows only that the observed behavior satisfies that condition; it does not prove that unasserted protocol behavior, corner cases, reset sequences, illegal inputs or interactions with other blocks are correct.

The patch loop needs a trustworthy failure signal and a complete requirement boundary. If the assertion set is incomplete, an LLM can optimize for the visible checks while preserving or introducing a bug outside them. If assertions are misleading, the workflow can move the RTL away from the intended protocol.

A valid repair must be rerun against the complete regression environment, including all relevant assertions, directed tests, randomized traffic, reset and timing-sensitive cases. A patch can fix the reported counterexample while causing a new deadlock, ordering violation, liveness failure or synthesis problem.

The official description does not expose protocol designs, assertion coverage, simulator or formal settings, accepted and rejected patches, regression results, synthesis/timing impact, runtime or human review. The record establishes an assertion-guided LLM repair proposal, not general protocol correctness or deployable RTL.

**Source and location**

Evidence tier: Primary captured official DAC description only; no full paper extraction, stitch artifact reproduction or independent formal, simulation, synthesis and integration validation. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH2443)

DAC 2026 official description and data/review-packets/dac-2026-research2443.json: assertion-guided LLM patching for on-chip protocol implementations; manual and unguided-LLM baselines; qualitative efficiency claim; omitted designs, assertions, simulators, correctness, coverage, synthesis, runtime and human-review conditions.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** manual patching

unguided LLM repair

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH2443

**Hardware or process assumptions:** On-chip protocol RTL and verification flow; synthesis and timing assumptions are unspecified.

**Limits:** No patch correctness, assertion coverage, synthesis impact, runtime, or human-review results are reported.

Assertions may be incomplete or misleading.

Official description only; formal and simulation validation is required.

**Method or artifact:** Assertion-guided LLM patching workflow for on-chip protocols.

**Metrics:** Protocol repair efficiency is claimed qualitatively

**Problem:** Protocol implementation bugs require patches that preserve intended behavior and satisfy assertions.

**Workload or benchmark:** RTL or protocol implementations; designs, assertions, simulators, and repair set are unspecified.

</details>

<span id="paper-dac-2026-research2642"></span>

### LLM4SDC: Leveraging Multi-Agent System for Automated SDC Generation and Benchmarking

DAC 2026 · Record: `dac-2026-research2642`

[Read the step-by-step explanation](#explanation-dac-2026-research2642)

**Updated source-backed reading card**

Reviewed 2026-09-08. Reconciles the LLM4SDC card with the captured official DAC description; explains SDC as executable timing intent, the multi-agent generation loop, benchmarking requirements and the risk that syntactically valid constraints silently change signoff assumptions.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Writing Synopsys Design Constraints (SDC) requires translating clock, input/output, timing exception and operating assumptions into commands that a timing tool interprets. A constraint file can parse successfully while describing the wrong design intent or hiding timing paths.

**Mechanism / artifact:**

LLM4SDC: a multi-agent LLM workflow for automated SDC generation and benchmarking, with agents responsible for generating or evaluating timing constraints.

**Workload — the work tested:**

Static-timing designs and SDC constraints; design netlists, RTL, clocks, interfaces, PDK/library data, timing tools, expert references, generated cases and train/test split are unspecified.

**Hardware and manufacturing assumptions:**

EDA static-timing flow; clock definitions, IO delays, false and multicycle paths, operating corners, libraries, synthesis state, PDK, tool versions, signoff rules and hardware implementation assumptions are unspecified.

**Baseline — the comparison method:**

Manual SDC authoring

Single-agent generation

Expert constraint set, timing tool, design state, corner set, review protocol and runtime boundary are unspecified

**Reported measurements:**

The captured official description claims qualitative constraint-generation efficiency; it does not report constraint correctness, timing correlation, path coverage, violation preservation, runtime, repair rate or expert-review effort.

**Limits on the conclusion:**

SDC is not ordinary configuration text. A clock period, generated clock, input/output delay, clock uncertainty or exception changes the set of timing relationships that the analyzer checks and the numerical limits applied to those relationships. The same syntax can be valid under a different clock or interface assumption and therefore encode the wrong design intent.

A multi-agent workflow can separate proposal, critique and checking. That separation helps only when the agents use different evidence or roles and when the final checker compares the generated constraints against an authoritative design and timing specification. Multiple language-model opinions do not by themselves establish correctness.

Benchmarking must compare the generated SDC with an expert or formally justified reference and then measure the timing consequences on the same netlist, libraries and corners. It must distinguish harmless textual differences from semantic differences, and must detect both over-constraint and under-constraint. A file that produces clean timing reports may have excluded paths that should have been analyzed.

The official description does not expose designs, clock/interface specifications, reference constraints, tool versions, corner setup, semantic comparison, coverage, timing correlation, runtime, failed cases or expert review. The record establishes an LLM-assisted constraint-generation proposal, not signoff-ready SDC or evidence that generated constraints preserve design intent.

**Source and location**

Evidence tier: Primary captured official DAC description only; no full paper extraction, llm4sdc artifact reproduction or independent timing, semantic equivalence, coverage and signoff validation. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH2642)

DAC 2026 official description and data/review-packets/dac-2026-research2642.json: laborious SDC writing and benchmarking; multi-agent LLM SDC generation; static timing designs; manual and single-agent baselines; qualitative efficiency claim; omitted correctness, timing correlation, coverage, runtime and expert-review conditions.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** manual SDC authoring

single-agent generation

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH2642

**Hardware or process assumptions:** EDA timing-analysis flow; PDK, clocks, and signoff assumptions are unspecified.

**Limits:** No constraint correctness, timing correlation, coverage, runtime, or expert-review results are reported.

Generated constraints can silently alter design intent.

Official description only; signoff and human validation are required.

**Method or artifact:** Multi-agent LLM workflow for SDC generation and benchmarking.

**Metrics:** Constraint-generation efficiency is claimed qualitatively

**Problem:** Design constraints are laborious to write and benchmark consistently across timing flows.

**Workload or benchmark:** Static timing designs and SDC constraints; tools, designs, and expert references are unspecified.

</details>

<span id="paper-dac-2026-research2829"></span>

### LLM-Enhanced Two-Stage Signal Temporal Logic Automatic Transformation with Structured Intermediate Representation

DAC 2026 · Record: `dac-2026-research2829`

[Read the step-by-step explanation](#explanation-dac-2026-research2829)

**Updated source-backed reading card**

Reviewed 2026-09-08. Reconciles the LLM-assisted Signal Temporal Logic transformation card with the captured official DAC description; explains semantic preservation across representations and the role and limits of a structured intermediate representation.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Signal Temporal Logic (STL) formulas describe Boolean and numerical conditions over signals and time intervals. Transforming them between languages or representations must preserve the same accepted and rejected signal traces, not merely produce text that parses.

**Mechanism / artifact:**

Two-stage LLM-assisted STL transformation workflow with a structured intermediate representation between source and target forms.

**Workload — the work tested:**

STL formulas and target representations; source and target languages, domains, parsers, solvers, formula complexity, test traces, equivalence oracle and train/test split are unspecified.

**Hardware and manufacturing assumptions:**

Formal or simulation-based verification flow; parser, solver, numerical semantics, time discretization, floating-point handling, runtime and tool versions are unspecified.

**Baseline — the comparison method:**

Manual transformation

Single-stage LLM transformation

Formula set, target syntax, semantic oracle, test traces and review boundary are unspecified

**Reported measurements:**

The captured official description claims transformation efficiency qualitatively; it does not report semantic-equivalence rate, coverage, runtime, failure modes, solver outcomes or expert-review effort.

**Limits on the conclusion:**

An STL formula defines a condition over signal values and time. Operators such as always, eventually and until depend on interval endpoints, nesting and the signal semantics. Changing an endpoint, strictness, sampling convention or operator scope can change which traces satisfy the formula even when the transformed text looks structurally similar.

A structured intermediate representation can make temporal operators, intervals, predicates, signal names, units and nesting explicit before a target-language rendering. It can reduce syntax errors only if the representation preserves every semantic detail and has a validated parser and serializer. A clean intermediate object can still encode the wrong meaning if its schema omits a boundary or numerical convention.

Two stages can separate semantic decomposition from target rendering and provide an intermediate point for checking. The stages do not by themselves prove equivalence. The source formula, intermediate form and target formula need parser checks, type and unit checks, boundary-condition tests, and formal or exhaustive semantic comparison over an appropriate trace model.

The official description does not expose formula sets, representations, temporal semantics, parsers, solvers, equivalence procedure, coverage, runtime, failed transformations or expert review. The record establishes an LLM-assisted transformation proposal, not semantic equivalence or a reliable verification artifact.

**Source and location**

Evidence tier: Primary captured official DAC description only; no full paper extraction, transformation artifact reproduction or independent parser, formal equivalence and simulation validation. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH2829)

DAC 2026 official description and data/review-packets/dac-2026-research2829.json: complex/error-prone STL transformation; two-stage LLM-assisted workflow; structured IR; manual and single-stage baselines; qualitative efficiency claim; omitted semantic equivalence, coverage, runtime, failures and expert-review conditions.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** manual transformation

single-stage LLM transformation

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH2829

**Hardware or process assumptions:** Formal or simulation verification flow; parser, solver, and runtime assumptions are unspecified.

**Limits:** No semantic-equivalence, coverage, runtime, failure, or expert-review results are reported.

LLM outputs can introduce subtle temporal errors.

Official description only; formal equivalence validation is required.

**Method or artifact:** Two-stage LLM-assisted transformation with structured IR.

**Metrics:** Transformation efficiency is claimed qualitatively

**Problem:** Signal temporal logic transformations are complex and error-prone across representations.

**Workload or benchmark:** Signal temporal-logic formulas and target representations; domains, tools, and tests are unspecified.

</details>

<span id="paper-dac-2026-research561"></span>

### Cupilot: A Strategy-Coordinated Multi-Agent Framework for CUDA Kernel Evolution

DAC 2026 · Record: `dac-2026-research561`

[Read the step-by-step explanation](#explanation-dac-2026-research561)

**Updated source-backed reading card**

Reviewed 2026-09-08. Reconciles the Cupilot card with the captured official DAC description; explains CUDA-kernel search as a constrained compiler-and-hardware feedback loop and separates strategy coordination from correctness and transferable performance evidence.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Optimizing a CUDA kernel requires choosing algorithm structure, memory access, thread mapping, synchronization, launch configuration and compiler-visible code so that the kernel remains correct and runs efficiently on a particular GPU.

**Mechanism / artifact:**

Cupilot: a multi-agent, strategy-coordinated framework for iterative CUDA kernel evolution, using agents to propose and assess changes across kernel implementations.

**Workload — the work tested:**

CUDA kernels; kernel set, input distributions, numerical tolerances, GPU architectures, CUDA/compiler versions, tests, optimization objective and train/tune/test separation are unspecified.

**Hardware and manufacturing assumptions:**

NVIDIA GPU and compiler/profiling toolchain; GPU model, driver, clock state, memory hierarchy, occupancy limits, correctness oracle, compilation settings and measurement protocol are unspecified.

**Baseline — the comparison method:**

Manual kernel tuning

Single-agent code generation

Kernel implementations, optimization budget, profiler, compiler flags, correctness tests and GPU diversity are unspecified

**Reported measurements:**

The captured official description claims kernel-evolution efficiency qualitatively; it does not report correctness, speedup, latency, compile time, search cost, energy, failure rate or cross-GPU results.

**Limits on the conclusion:**

A CUDA kernel is a program executed by many threads. Its result depends on the algorithm, memory addresses, thread and block mapping, synchronization, atomic operations, numerical precision and input shape. A faster kernel is useful only if it produces an accepted result under the required numerical and functional checks.

Strategy coordination can assign agents different search roles, such as proposing algorithm changes, tuning launch and memory parameters, profiling bottlenecks or rejecting invalid candidates. Coordination is meaningful only when the roles exchange measured evidence and respect a shared correctness boundary; multiple proposals without reproducible evaluation are not an optimization result.

The compilation and profiling loop is part of the search cost. A candidate may look promising on one input or GPU because of cache state, occupancy, shape, compiler version or clock behavior. The evaluation must include compilation time, profiling overhead, failed candidates and a fixed measurement protocol, then test unseen inputs and architectures if transfer is claimed.

The official description does not expose kernels, inputs, correctness oracle, search budget, GPU models, compiler settings, speedups, compile time, cost, failures or GPU-diversity results. The record establishes a coordinated multi-agent CUDA-evolution proposal, not general kernel correctness, transferable speedup or cost-effective optimization.

**Source and location**

Evidence tier: Primary captured official DAC description only; no full paper extraction, cupilot artifact reproduction or independent functional, performance, cost and cross gpu validation. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH561)

DAC 2026 official description and data/review-packets/dac-2026-research561.json: iterative CUDA kernel search over algorithmic and low-level choices; multi-agent strategy coordination; manual and single-agent baselines; qualitative efficiency claim; omitted correctness, speedup, compile time, cost and GPU-diversity conditions.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** manual kernel tuning

single-agent code generation

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH561

**Hardware or process assumptions:** NVIDIA GPU and compiler toolchain; correctness oracle and profiling assumptions are unspecified.

**Limits:** No correctness, speedup, compile time, cost, or GPU-diversity results are reported.

Search may overfit benchmark kernels.

Official description only; reproducible kernel validation is required.

**Method or artifact:** Multi-agent, strategy-coordinated CUDA kernel evolution framework.

**Metrics:** Kernel evolution efficiency is claimed qualitatively

**Problem:** CUDA kernel optimization requires iterative search across algorithmic and low-level implementation choices.

**Workload or benchmark:** CUDA kernels; GPU architectures, tests, and optimization objectives are unspecified.

</details>

## What remains to establish

Resolve unspecified workloads, comparison methods, resource budgets, and source locations before generalizing a reported gain. Multiple papers in this selected sample permit comparison of mechanisms, but do not by themselves establish recurrence across years or a long-term trend.

[All subthemes](../expanded-taxonomy-v1.md) · [Research directions](../directions/README.md)
