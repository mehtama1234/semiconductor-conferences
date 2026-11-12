# AI-assisted EDA

This article explains the subject and then connects it to 59 papers in the selected research sample.

A subtheme groups related technical problems. A mechanism describes the particular change proposed by a paper. The discussion below explains the subject; the linked paper records state the available evidence.

[Definitions used in the paper records](../reading-guide-v1.md)

## Chip design is a long chain of choices that software helps make

A designer states what a circuit must do and which limits it must meet. **Electronic design automation (EDA)** is the software that turns that statement into a circuit and then a physical layout.

There are many choices along the way:

1. how to represent the logic;
2. which circuit elements to use;
3. where to place them;
4. how to connect them.

Each choice can affect correctness, area, timing and power.

## A learned model can propose or predict, and these are different jobs

A learned model uses patterns in past examples or evaluations to suggest a new choice.

- A **language model** may write hardware-description code, or change a design program.
- A **predictor** may guess which candidate is worth an expensive evaluation.

Writing code does not show that the code meets the specification. Predicting a good timing score does not show that the built circuit meets timing.

## Each check answers a different question, so record which one failed

- **Synthesis** turns a behavioral or logical description into circuit elements.
- **Simulation** runs a model on selected inputs.
- **Formal verification** checks a stated property mathematically, within a defined model.

A design method should record which check rejected a candidate, what it reported, and how that changed the next attempt. A weak test can accept a wrong design and make the search look successful.

## A fair test counts every model call, check and retry

1. Give competing methods the same design tasks.
2. Count the whole time and computing budget: model calls, training, checking and retries.
3. Report valid completed designs and their measured quality.
4. Test on new circuits that were not used to tune the method.

The long-term question: can better choices be made with less total engineering and evaluation effort, while keeping the design correct?

## Separate proposing a design from establishing its properties

What a model outputs is a proposal; only a check turns it into a result.

A learned model can produce four kinds of output, each with a different meaning:

| Model output | What it really is |
| --- | --- |
| A proposed circuit | A candidate |
| A predicted delay | An estimate |
| A chosen search action | A suggestion of what to try next |
| A suggested proof statement | An obligation to check |

None becomes a validated result just because the model sounds confident.

> **Worked example.** A task asks for a four-bit counter that returns to zero after fifteen and resets when asked. Generated code might:
>
> - compile, but ignore reset;
> - count correctly in a short simulation, but mishandle simultaneous inputs;
> - behave correctly, but exceed an area limit.
>
> Syntax, behavior and physical limits are separate conditions for acceptance.

**Be careful:** the calculations and examples here are explanatory constructions, not paper results. This theme links recorded proposals without upgrading their evidence. Several linked branches still have only description-level sources and shallow treatments; those limits stay part of the reading path.

## Identify the learned decision before comparing methods

Name the job the model does first, because each job needs its own check.

| Learned role | Output supplied to the design process | Required check |
| --- | --- | --- |
| Generator | Code, geometry, or candidate parameters | Required behavior and implementation constraints |
| Predictor | Estimated delay, power, area, or another property | Error under the relevant target conditions and decisions |
| Search controller | Which candidate or tool to try next | Final valid solution at a stated total budget |
| Proof assistant | A candidate lemma or proof step | Validity under the actual formal model and assumptions |

This stops unrelated accuracy scores from looking comparable. A predictor with lower average error and a generator with more valid outputs do not improve the same quantity. Their effects can meet in one design process, but only with compatible inputs, checks and cost accounting.

The [learned EDA chapter](../observed-subthemes/learned-eda-and-optimization.md) applies this split across electrical prediction, inverse design, algorithm selection and proof suggestions.

**Be careful:** its recorded proposals raise questions worth investigating. They are not a shared, experimentally established improvement.

## Feedback is useful only when the checker observes the requirement

Feedback helps only if the check actually looks at the property that matters.

A generated candidate is checked, and the result shapes the next attempt. Feedback can report:

- invalid syntax;
- a failed functional test;
- a timing violation;
- a physical rule violation.

These are not interchangeable error messages. A useful repair fixes the cause while keeping properties that already held.

> **Worked example (illustrative layout rule: spacing must be at least four units).**
>
> - Moving a wire raises one spacing from three units to the required four.
> - The same move cuts another spacing from five to three.
> - One violation disappears; another appears. Counting the first repair as "done" hides the new problem.
>
> Connectivity and circuit behavior need their own checks too.

[Drcagent's captured record](../observed-subthemes/llm-assisted-design-flows.md#paper-dac-2026-research2145) raises this through rule-informed repair. Its current explanation does not establish full closure, transfer to other processes, or final layout quality. The [Verilog-generation discussion](../observed-subthemes/llm-assisted-design-flows.md#generated-code-needs-several-kinds-of-checking) likewise separates accepted text, simulated behavior, finished synthesis and hardware quality.

Feedback also changes which candidates survive. Optimizing again and again against one visible test can exploit gaps in that test. So:

1. hold back independently designed checks;
2. try unfamiliar requirements.

Passing the same tests that guided every edit is useful, but weaker than independent confirmation of the intended behavior.

## Hard constraints must not disappear inside a reward

A requirement that must hold has to reject a candidate outright, not just lower its score.

A search can give promising candidates a numerical **reward**. If invalid behavior only gets a small penalty, an attractive score elsewhere can outweigh it. When correctness is required, a faster wrong circuit is no substitute for a slower correct one. The process must reject invalid candidates, or keep them marked unresolved.

Power, performance and area also trade off against each other.

> **Worked example.**
>
> | Candidate | Area units | Delay |
> | --- | --- | --- |
> | A | 80 | 12 |
> | B | 100 | 8 |
>
> - Neither is better on both measures.
> - If delay must be at most 10, only B is feasible of the two.

A **Pareto comparison** lists the trade-offs among the candidates evaluated. It does not set the user's constraints, or prove that no better design exists.

[Paretopilot's recorded proposal](../observed-subthemes/llm-assisted-design-flows.md#paper-dac-2026-research865) guides high-level synthesis choices. Its current source conditions do not show a universally better search. Compare feasible outcomes with the same objectives, evaluated inputs and full budget, not a favorable summary of the candidates.

## Prediction quality must survive selection and transfer

A predictor must be tested on the kind of new design it will meet, and on the winners it picks.

A model trained on one circuit family can exploit similarities within that family. Testing close variants shows it can fill gaps inside that family. It says little about a new topology, technology or operating condition. So state which changes the evaluation actually tests.

The split between training and test data must match the claimed transfer:

- Putting near-duplicate variants in both sets makes the test easier than real use on a new design.
- A deliberately harder split answers a different question. Do not compare it silently with an easier one.

Search also picks out unusual predictions. A candidate predicted to have very low delay may owe part of that to an optimistic error. Accurate predictions on random candidates do not show accurate ranking of the chosen winners. Re-check winners with a more trustworthy method, and record when their ranking or feasibility changes.

The [tooling theme](design-methodology-and-tooling.md) explains why a small delay error near a limit can change acceptance. Learned prediction belongs inside that decision accounting, with exact fallback and rejected candidates, not replaced by one average-error score.

## Retrieval and multiple roles do not create independent evidence

Several model roles that share the same sources can share the same mistake.

**Retrieval** gives a model selected reference material. It can make rules or examples available. But the references may be incomplete, out of date for the target, or wrongly applied. Record:

- what was retrieved;
- which version applies;
- whether the evaluation supplied task-specific help that a new deployment would have to recreate.

Splitting work among named model roles can organize generation, criticism and repair. It does not make their judgments independent if they share a mistaken reference, checker or assumption. A second fluent explanation of the same candidate is not a separate functional or physical check.

The [verification theme](verification-and-validation.md) sets the boundary:

- disagreement needs diagnosis;
- agreement can share a common error;
- a proof depends on its model and assumptions.

For [Legend's learned lemma proposal](../observed-subthemes/learned-eda-and-optimization.md#paper-dac-2026-research523), a suggested statement must be proved before it supports a proof.

**Be careful:** the captured record does not independently establish the method's soundness or success rate.

## Count accepted designs and the effort needed to obtain them

Report how many attempts end as accepted designs, and everything spent to get there.

> **Worked example.** 100 generated candidates:
>
> | Stage passed | Candidates |
> | --- | --- |
> | Syntax | 80 |
> | Functional tests | 50 |
> | Implemented constraints | 20 |
>
> Final acceptance is 20% of attempts, not 80%.

Reporting only the survivors hides where the work went, and which stage is still the bottleneck.

Total cost includes:

- preparing data and references;
- training or tuning, where used;
- model calls and tool runs;
- retries and human investigation.

A one-second model call followed by a 100-second physical evaluation is not a one-second attempt. Running in parallel changes elapsed time and resource use in different ways.

Repeated use can spread the preparation cost, but only while the prepared model and references still apply. Record how many new tasks share that cost, what breaks reuse, and what happens when a tool or process changes. A reusable method is stronger evidence than a hand-repaired demonstration, but it still needs stated limits.

## Long-term hypotheses to test rather than assume

Three readings are worth testing; each names what would weaken it.

| Hypothesis | Test | What would weaken it |
| --- | --- | --- |
| Learned guidance helps most when it cuts expensive evaluations while keeping final acceptance | Compare with non-learned search, at equal checking and preparation budgets | Saved evaluations are offset by data generation, rejected candidates, or lower valid-output quality |
| Structured feedback improves transfer more than extra unconstrained generation | Remove or change feedback parts, keeping model access, tools and compute | Gains come from stronger checkers or privileged task examples, not better use of feedback |
| Trustworthy automation needs clear boundaries between proposing, checking and accepting | An independent user replays it with the same declared requirements and tools | Acceptance still depends on hidden intervention, or a checker misses the claimed property |

These are bounded interpretations, not measured ISCA–DAC–ICCAD growth trends or evidence of autonomous design closure. Comparable editions, tasks, data access, budgets and review standards are still needed.

**Be careful:** this expanded parent discussion does not complete the individual-paper rewrites, source recovery, classification reconciliation, or independent comprehension and scientific review below.

## Subthemes and how to study them

Each link opens the subtheme discussion and its captured paper records. Explanatory depth varies: some papers have expanded individual explanations; others still have only brief discussion or evidence cards. Source locations and unresolved conditions remain visible.

### [Learned design space exploration](../observed-subthemes/learned-design-space-exploration.md)

21 selected records in this theme. Start with [Agenticdse: A Multi-Agent Design Space Exploration Framework with Multi-Phase Bayesian Optimization for Chiplet Accelerators](../observed-subthemes/learned-design-space-exploration.md).

### [Learned EDA and optimization](../observed-subthemes/learned-eda-and-optimization.md)

10 selected records in this theme. Start with [Attentioncap: Transformer Based Capacitance Matrix Learning Toward Full-Chip Extraction](../observed-subthemes/learned-eda-and-optimization.md).

### [LLM assisted design flows](../observed-subthemes/llm-assisted-design-flows.md)

8 selected records in this theme. Start with [Drcagent: A Design Rule Aware LLM Agent for DRC Auto-Fix with Adversarial Reinforcement Learning](../observed-subthemes/llm-assisted-design-flows.md).

### [Generative design and synthesis](../observed-subthemes/generative-design-and-synthesis.md)

7 selected records in this theme. Start with [Shortcircuit: Alphazero-Driven Generative Circuit Design](../observed-subthemes/generative-design-and-synthesis.md).

### [Generative design automation](../observed-subthemes/generative-design-automation.md)

6 selected records in this theme. Start with [PCBgen3D: A Self-Correcting Graph-Based MLLM Framework for Automated PCB 3D Models Generation](../observed-subthemes/generative-design-automation.md).

### [Graph learning for EDA](../observed-subthemes/graph-learning-for-eda.md)

5 selected records in this theme. Start with [TRACE: Learning to Compute on Circuit Graphs](../observed-subthemes/graph-learning-for-eda.md).

### [Architecture modeling and exploration](../observed-subthemes/architecture-modeling-and-exploration.md)

1 selected records in this theme. Start with [Hades: Harnessing Architecture Design Automation for Application-Specific FHE Accelerators](../observed-subthemes/architecture-modeling-and-exploration.md).

### [Verification and debugging tools](../observed-subthemes/verification-and-debugging-tools.md)

1 selected records in this theme. Start with [Akirarust: Re-Thinking LLM-Aided Rust Repair Using a Feedback-Guided Thinking Switch](../observed-subthemes/verification-and-debugging-tools.md).

## Representative source-backed records

The following reading set spans the available conferences and uses dated corrections where registered. These corrections improve the current reading view but do not change historical adjudication or establish independent acceptance. Each paper link opens its exact evidence card.

## Paper cards: what changes and where it stops

- [Exploiting Function-Family Structure in Analog Circuit Optimization](../observed-subthemes/learned-eda-and-optimization.md#paper-dac-2026-research951) — DAC 2026.
- [Hades: Harnessing Architecture Design Automation for Application-Specific FHE Accelerators](../observed-subthemes/architecture-modeling-and-exploration.md#paper-dac-2026-research912) — DAC 2026.
- [LEAP: A Self-Supervised Per-Cycle Toggle Propagation Model Supports Fast, Transferable, and Early Analysis of Layout Power](../observed-subthemes/learned-design-space-exploration.md#paper-dac-2026-research906) — DAC 2026.
- [RTL-Sequencer: Towards Scalable RTL Timing Prediction with the Sequence-Based Paradigm](../observed-subthemes/learned-design-space-exploration.md#paper-dac-2026-research883) — DAC 2026.
- [VeriOpt: PPA-Aware High-Quality Verilog Generation via Multi-Role LLMs](../observed-subthemes/llm-assisted-design-flows.md#paper-iccad-2025-1222) — ICCAD 2025.
- [VERIRL: Boosting the LLM-based Verilog Code Generation via Reinforcement Learning](../observed-subthemes/llm-assisted-design-flows.md#paper-iccad-2025-110) — ICCAD 2025.
- [Paretopilot: Global Optimization Reasoning on HLS Design Space Exploration with LLMs](../observed-subthemes/llm-assisted-design-flows.md#paper-dac-2026-research865) — DAC 2026.
- [Soberdse: Sample-Efficient Design Space Exploration via Learning-Based Algorithm Selection](../observed-subthemes/learned-eda-and-optimization.md#paper-dac-2026-research859) — DAC 2026.
- [GSR-GNN: Training Acceleration and Memory-Saving Framework of Deep GNNs on Circuit Graph](../observed-subthemes/graph-learning-for-eda.md#paper-dac-2026-research795) — DAC 2026.
- [Stochastic Diffusion Prior: Knowledge Elicitation and Local Adaptation for Transistor Sizing](../observed-subthemes/learned-design-space-exploration.md#paper-dac-2026-research739) — DAC 2026.
- [DiffDEG: Diffusion-Enhanced Design Evolution Graph Representation Learning for Post-Layout Optimization](../observed-subthemes/learned-eda-and-optimization.md#paper-dac-2026-research692) — DAC 2026.
- [Closing the Loop: Hybrid NAS Guided by Analytical and Hardware-Calibrated Quantum Cost Modeling](../observed-subthemes/learned-design-space-exploration.md#paper-dac-2026-research577) — DAC 2026.

## What the evidence supports

These records identify proposed methods and the conditions recorded for them. A reported improvement should be interpreted with its comparison method, input size, hardware, and result-quality requirement. Missing fields are evidence gaps; a populated field can also state that a detail is unspecified.

## Limits and next evidence

The selected sample is uneven across conferences and source types. It cannot establish how fast a subject is growing. Repeated observations across comparable years, with the same inclusion rules and source depth, are needed for a time trend.

Every linked evidence article preserves the Problem: and Mechanism / artifact: fields, baseline, unshortened limitations, source URL, and recorded location. Primary text and independent review remain necessary where the record says those checks are open.

[Research directions](../directions/README.md) · [All observed subthemes](../expanded-taxonomy-v1.md)
