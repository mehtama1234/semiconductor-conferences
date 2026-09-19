# Chiplet partitioning and integration

This subject has 1 record in the selected sample. This page explains where it fits, then presents all captured paper evidence without shortening the measurements or limitations.

[Definitions used in the paper records](../reading-guide-v1.md)

## Understand the parent subject first

- [Chiplets 3d and packaging](../themes/chiplets-3d-and-packaging.md)

## Dividing a design creates interfaces that must work together

A chiplet system divides functions among multiple dies connected within a package. Partitioning chooses what each die does. Integration makes those choices work together through compatible interfaces, data transfers, timing, and physical connections. A successful individual module is therefore not sufficient evidence for a successful complete system.

The selected record, [MAHL](../observed-subthemes/chiplet-partitioning-and-integration.md#paper-iccad-2025-1207), proposes a hierarchical, language-model-assisted design workflow. The evidence belongs to the 2025 fallback corpus even though the atlas's target edition is 2026. Its presence should not be counted as an independent 2026 publication or a year-over-year trend observation.

## Why hierarchy helps organize a complex design

A hierarchy describes a system as components with defined responsibilities and interfaces, then describes the internal structure of those components. This can make a large generation task more manageable: a module description can specify what must be implemented without repeating every detail of the whole design.

However, local descriptions must remain consistent. Two modules can each pass isolated tests while disagreeing about data width, transfer ordering, or when an output is valid. Hierarchical generation therefore needs checks of both module behavior and composed behavior. Dividing the work does not remove the integration problem.

MAHL's captured preprint description identifies six collaborating agents covering AI-to-hardware mapping, hierarchical descriptions, retrieval-assisted code generation, validation, debugging, and design-space exploration. These are software workflow roles, not six independent human reviews or six separate sources of evidence. Agreement among generated outputs is not a substitute for tool-based and specification-based checking.

## Generated RTL is an intermediate artifact

RTL describes circuit state updates and the logic connecting them. Producing RTL that parses or compiles establishes only an early requirement. Functional tests, synthesis, timing, physical constraints, and interface checks examine different properties.

The record describes retrieval-assisted RTL generation and Diverseflow validation with adaptive debugging. Retrieval supplies existing information to the generation process; debugging uses feedback to revise candidates. The available evidence does not specify every validation gate, so “passes validation” must remain tied to the paper's actual procedure rather than being expanded into full physical acceptance.

A debugging loop also has costs and risks. Repeated revisions consume model calls and tool execution, and a fix can satisfy a visible test without preserving behavior outside that test. A complete evaluation should retain failed attempts and assess the final candidate with checks not used merely as generation feedback.

## What Pass@5 does and does not measure

The captured record reports a best-case real-world chiplet-design comparison in which Pass@5 rises from 0 to 0.72. Pass@5 concerns obtaining a passing result within five candidates under the stated evaluation. It is not a single-attempt success rate, and the best-case comparison is not an established average across all tasks and models.

Its practical interpretation requires the definition of passing, the task set, candidate-generation procedure, and resources spent per candidate. A workflow with more extensive validation or more generation effort can differ substantially from another even when both report five attempts. The captured preprint evidence does not establish those cost and comparability details.

## Compare complete physical designs under the same objective

MAHL also reports comparable or superior power, performance, and area to CLARIE under selected objectives. These quantities can trade against one another. A lower-area design is not automatically preferable if it misses a timing requirement, and a faster design may consume more power or package resources.

The comparison therefore needs common workloads, design constraints, process assumptions, and physical-analysis settings. The record does not establish the full reproducible flow or fairness of the CLARIE comparison. It also does not provide enough information to infer fabricated chiplet operation from the generated designs.

<span id="explanation-iccad-2025-1207"></span>

## MAHL: hierarchy and validation must cover the composed chiplet system

### Partitioning creates a contract between dies

A chiplet design divides a system into dies, but the division does not eliminate the behavior that crosses the boundary. Each module has to state its inputs, outputs, data widths, timing, protocol and resource assumptions. The package then has to provide the physical connections, power delivery, clocking and thermal conditions needed for those contracts to hold.

MAHL is described as a multi-agent, language-model-guided workflow for hierarchical chiplet design. Its hierarchy is useful only if a local module specification can be composed into a system specification. A generated accelerator block may pass its own tests while using a different interface width or transaction order from the block that consumes it. The workflow therefore has to validate both local behavior and the assembled design.

### The six roles divide work, not responsibility

The captured preprint description identifies six collaborating roles: AI-to-hardware mapping, hierarchical description, retrieval-assisted RTL generation, validation, debugging, and design-space exploration. These roles form a sequence of transformations. A workload or system objective is mapped to hardware structure; the structure is expressed as module descriptions; RTL is generated using retrieved information; tools test the candidate; debugging revises it; and exploration chooses among design configurations.

The separation can make feedback more specific, but it also creates information-transfer requirements. Retrieval can provide relevant examples without proving that the new design matches the target specification. A debugger can repair a failing test without finding behaviors that the test suite never exercises. A design-space search can optimize a predicted PPA score while changing the interface or validation assumptions. The workflow must carry requirements and failure causes between roles, not merely pass text from one agent to the next.

### RTL generation is only an intermediate checkpoint

RTL is a description of state updates and combinational logic. Parsing or compiling the generated RTL establishes syntax and some tool compatibility. Functional simulation checks selected behavior. Synthesis checks whether the design can be mapped to a target library. Timing, power, area, routing and package checks examine different constraints. A passing result at one level does not imply that the next level will pass.

MAHL's retrieval-assisted generation and Diverseflow validation with adaptive debugging are therefore best read as a closed generation-and-repair loop whose exact gates need to be specified. Each repair may consume model calls, synthesis or simulation time, and additional candidate evaluations. The evaluation should preserve failed candidates, retry counts, tool versions, stopping rules, and checks withheld from generation feedback. Otherwise “validation” may measure the workflow's ability to satisfy a familiar test rather than the design's general correctness.

### Pass@5 is a budgeted success probability

Pass@5 asks whether at least one of five generated candidates passes the stated criterion. It is not the probability that the first candidate works, and it does not show that all five candidates have equal cost. A workflow can increase Pass@5 by generating more diverse candidates, using more validation per candidate, or spending more repair effort. Those choices are useful only if the added cost is included.

The captured record reports a best-case real-world comparison in which Pass@5 rises from 0 to 0.72. The task population, passing criterion, model and prompt configuration, candidate-generation cost, and whether the number is an average or selected best case are not fully exposed in the stored paper reading. The number therefore cannot be generalized to autonomous chiplet design or compared fairly with CLARIE without those conditions.

### PPA comparison needs the same physical problem

Power, performance and area are not one objective. Improving one can worsen another, and a candidate that does not meet timing or interface requirements is not comparable merely because its area is smaller. MAHL's reported comparable or superior PPA to CLARIE must remain attached to the selected objectives, design constraints, process/library assumptions, physical-flow settings and workload.

The paper is in the ICCAD 2025 fallback corpus, not the target 2026 corpus. Its evidence is a primary preprint, but exact page, section and table locations were not recorded in this atlas pass. The record therefore supports a technically meaningful workflow explanation and a bounded report of the captured claims, not a page-verified conclusion about fabricated chiplet operation or broad year-over-year change.

### What MAHL establishes and what remains open

MAHL establishes a proposed hierarchical workflow that combines LLM-generated descriptions and RTL with tool feedback, debugging and design-space exploration. It does not establish end-to-end autonomous chiplet correctness, average-case Pass@5, equal-cost comparison with conventional LLMs or CLARIE, complete physical closure, or fabricated hardware. A stronger evaluation would publish the task suite, module/system specifications, agent prompts and models, retrieval corpus, validation gates, retries and costs, OpenROAD/library/process settings, PPA denominators, held-out designs, and independent final checks.

[Primary preprint](https://arxiv.org/abs/2508.14053)

## The longer-term question

MAHL motivates organizing automated hardware design around explicit hierarchy and repeated validation. The decisive research question is whether that organization reduces total effort to obtain an integrated design meeting fixed requirements, rather than only increasing the number of generated candidates that pass a limited test suite.

Evidence would need to connect each requirement to its module and system checks, preserve generation and repair costs, and verify the final physical configuration. The current preprint record supports explaining the proposed workflow and its reported results, but not claiming autonomous end-to-end chiplet correctness, general superiority, or an established long-term adoption trend.

## Compare the results carefully

First identify the inputs and required output quality. Then identify the limited resource: time, memory, communication, energy, circuit area, or correctness coverage. Ask which part of the method reduces that cost and which new cost it adds. Compare numbers only when the experiments hold these conditions sufficiently similar.

A conference description may explain the proposal while omitting the full experiment. An author preprint link may have been coded from its abstract. The source classification does not by itself establish that every table was read. Missing locations remain visible below.

## Complete captured evidence

These are evidence records, not substitutes for the explanations above. Each record preserves its problem, proposed method, measurements, comparison conditions, and source limits. A populated record does not establish that its mechanism has been fully explained or independently verified.

<span id="paper-iccad-2025-1207"></span>

### MAHL: Multi-Agent LLM-Guided Hierarchical Chiplet Design with Adaptive Debugging

ICCAD 2025 · Record: `iccad-2025-1207`

[Read the step-by-step explanation](#explanation-iccad-2025-1207)

**Updated source-backed reading card**

Reviewed 2026-09-08. Deepens the primary-preprint reading; separates hierarchical module contracts, six software workflow roles, RTL/tool validation, Pass@5 budgeting and PPA comparison conditions.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Flat language-model-driven chiplet design has high validation cost and weak coordination between module generation, integration and physical objectives.

**Mechanism / artifact:**

Six-role hierarchical workflow combining AI-to-hardware mapping, structured module descriptions, retrieval-assisted RTL generation, tool-based validation/debugging, multi-granularity design-space exploration and physical-layout configuration.

**Workload — the work tested:**

Simple RTL and real-world AI chiplet-design tasks; exact task suite, module/system specifications and held-out designs require the primary paper reading.

**Hardware and manufacturing assumptions:**

2.5D chiplet designs with AI workloads, RTL generation, synthesis/validation and OpenROAD-like physical configuration; exact chiplet architectures, PPA flow, libraries and design constraints require full-paper review.

**Baseline — the comparison method:**

Conventional LLMs

CLARIE expert-based chiplet design framework

**Reported measurements:**

Reported best-case real-world chiplet-design Pass@5 rises from 0 to 0.72; the task population, average/best-case convention and candidate cost require verification.

Comparable or superior PPA to CLARIE is reported under selected objectives; exact denominators and physical-flow conditions are not fully recorded.

**Limits on the conclusion:**

Pass@5 is success within five candidates, not first-attempt success, equal-cost success or complete design correctness.

Local RTL compilation, functional validation, synthesis, timing, routing and package/system closure answer different questions; the captured record does not establish all gates or independent checks.

The ICCAD 2025 fallback paper is not an independent 2026 publication or year-over-year trend observation. Exact page/section/table locations were not recorded in this pass; no fabricated chiplet operation is established.

**Source and location**

Evidence tier: Primary preprint; selected reading and execution/independent acceptance not performed. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://arxiv.org/abs/2508.14053)

Primary preprint identity and selected method/evaluation reading; exact page, section and table locators require follow-up.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** high_primary_preprint

**Baselines:** conventional LLMs

CLARIE expert-based chiplet design framework

**Evidence locators:** Not established in the captured evidence.

**Evidence url:** https://arxiv.org/abs/2508.14053

**Hardware or process assumptions:** 2.5D chiplet designs with AI workloads, RTL generation, synthesis/validation, and OpenROAD-like physical configuration; exact chiplet architectures, PPA flow, and design constraints require full-paper review.

**Limits:** The preprint evidence does not establish average-case Pass@5, design-suite breadth, prompt/model costs, physical-flow reproducibility, or fairness of the CLARIE comparison; target edition remains 2026 while paper analysis uses the 2025 fallback corpus.

**Method or artifact:** Six-agent hierarchical workflow combining AI-hardware parsing, structured module descriptions, retrieval-augmented RTL generation, tool-based validation/debugging, multi-granularity design-space exploration, and physical-layout configuration.

**Metrics:** real-world chiplet-design Pass@5 from 0 to 0.72 in reported best-case comparison

comparable or superior PPA to CLARIE under selected objectives

RTL generation accuracy

**Problem:** Flat LLM-driven chiplet design has high validation cost and imprecise parameter optimization for complex hierarchical 2.5D systems.

**Workload or benchmark:** Simple RTL and real-world AI chiplet-design tasks; PPA objectives and Pass@5 generation accuracy are evaluated against conventional LLMs and CLARIE.

</details>

## What remains to establish

Resolve unspecified workloads, comparison methods, resource budgets, and source locations before generalizing a reported gain. This subject is represented by one paper and supports a case study, not evidence of recurrence or a long-term trend.

[All subthemes](../expanded-taxonomy-v1.md) · [Research directions](../directions/README.md)
