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
