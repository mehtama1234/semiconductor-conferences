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

**Be careful:** this overview is not the end of the work. The paper write-ups below, the search for full sources, the label clean-up and independent review are still open.
