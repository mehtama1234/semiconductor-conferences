## Separate proposing a design from establishing its properties

A learned model can propose a circuit, predict a measurement, select a search action, or suggest a statement for a proof. Each output has a different meaning. A proposed circuit is a candidate. A predicted delay is an estimate. A suggested proof statement is an obligation to check. None becomes a validated result simply because the model expresses confidence.

Suppose a task asks for a four-bit counter that returns to zero after fifteen and resets when requested. Generated code might compile while ignoring reset, count correctly in a short simulation while mishandling simultaneous inputs, or implement the required behavior but exceed an area limit. Syntax, behavior, and physical constraints are separate acceptance conditions.

The following calculations and examples are explanatory constructions, not paper results. This theme connects recorded proposals without upgrading their evidence. Several linked branches still have description-level sources and shallow individual treatments; those limits remain part of the reading path.

## Identify the learned decision before comparing methods

| Learned role | Output supplied to the design process | Required check |
| --- | --- | --- |
| Generator | Code, geometry, or candidate parameters | Required behavior and implementation constraints |
| Predictor | Estimated delay, power, area, or another property | Error under the relevant target conditions and decisions |
| Search controller | Which candidate or tool to try next | Final valid solution at a stated total budget |
| Proof assistant | A candidate lemma or proof step | Validity under the actual formal model and assumptions |

This separation prevents unrelated accuracy scores from appearing comparable. A predictor with lower mean error and a generator with more valid outputs do not improve the same denominator. Their effects can meet in one design process, but that requires compatible inputs, checks, and cost accounting.

The [learned EDA chapter](../observed-subthemes/learned-eda-and-optimization.md) uses this distinction across electrical prediction, inverse design, algorithm selection, and proof suggestions. Its recorded proposals identify questions worth investigating, not a shared experimentally established improvement.

## Feedback is useful only when the checker observes the requirement

A generated candidate is evaluated; the returned information influences the next attempt. Feedback may identify invalid syntax, a failed functional test, a timing violation, or a physical rule violation. These are not interchangeable error messages. A useful repair must change the cause while retaining properties that already held.

For an illustrative layout constraint, moving a wire can increase one spacing from three units to the required four while reducing another spacing from five to three. One local violation disappears and another appears. Counting the first repair as completion hides the new problem. Connectivity and circuit behavior need their own checks as well.

[Drcagent's captured record](../observed-subthemes/llm-assisted-design-flows.md#paper-dac-2026-research2145) motivates this issue through rule-informed repair. Its current explanation does not establish full closure, process transfer, or final layout quality. The [Verilog-generation discussion](../observed-subthemes/llm-assisted-design-flows.md#generated-code-needs-several-kinds-of-checking) similarly distinguishes accepted text, simulated behavior, synthesis completion, and hardware quality.

Feedback also changes the search population. Repeatedly optimizing against one visible test can exploit gaps in that test. Hold back independently designed checks and investigate what happens on unfamiliar requirements. Passing the same tests used to guide every edit is useful but weaker than independent confirmation of the intended behavior.

## Hard constraints must not disappear inside a reward

A search can assign a numerical reward to promising candidates. If invalid behavior merely receives a small penalty, another attractive score can outweigh it. A faster incorrect circuit is not a valid substitute for a slower correct one when correctness is mandatory. The process must explicitly reject invalid candidates or retain their unresolved status.

Power, performance, and area also trade off. Candidate A might occupy 80 area units with delay 12; candidate B might occupy 100 with delay 8. Neither is better on both dimensions. If delay must be at most 10, only B is feasible among these two. A Pareto comparison identifies tradeoffs among evaluated candidates; it does not determine the user's constraints or prove global optimality.

[Paretopilot's recorded proposal](../observed-subthemes/llm-assisted-design-flows.md#paper-dac-2026-research865) guides high-level synthesis choices. Its current source conditions do not establish a universally better search. Compare feasible outcomes using the same objectives, evaluated inputs, and complete budget, not merely a favorable summary of the candidate set.

## Prediction quality must survive selection and transfer

A model trained on examples from one circuit family can exploit similarities within that family. Testing close variants may establish interpolation within that population while saying little about a new topology, technology, or operating condition. State which changes the evaluation actually tests.

The separation between training and evaluation must follow the claimed transfer. Splitting near-duplicate variants across both sets can make the test easier than deployment on a genuinely new design. Conversely, a deliberately harder split answers a different question and should not be compared silently with an easier one.

Search also selects unusual predictions. A candidate predicted to have exceptionally low delay may owe part of that advantage to an optimistic error. Evaluating random candidates accurately does not by itself establish accurate ranking of the selected winners. Re-evaluate winners with the appropriate higher-confidence method and record when their rankings or feasibility change.

The [tooling theme](design-methodology-and-tooling.md) explains why a small delay error near a constraint can change acceptance. Learned prediction belongs within that decision accounting, including exact fallback and rejected candidates, rather than replacing it with a single average-error score.

## Retrieval and multiple roles do not create independent evidence

Retrieval supplies selected references to a model. It can make rules or examples accessible, but those references may be incomplete, outdated for the target, or incorrectly applied. Record what was retrieved, its applicable version, and whether the evaluation supplied task-specific information that would require effort in a new deployment.

Dividing work among named model roles can organize generation, criticism, and repair. It does not make their judgments independent if they share a mistaken reference, checker, or underlying assumption. A second fluent explanation of the same candidate is not equivalent to a separate functional or physical check.

The [verification theme](verification-and-validation.md) provides the necessary boundary: disagreement requires diagnosis, agreement can share a common error, and a proof depends on its model and assumptions. For [Legend's learned lemma proposal](../observed-subthemes/learned-eda-and-optimization.md#paper-dac-2026-research523), a suggested statement must be established before it supports a proof. The captured record does not independently establish the method's soundness or success rate.

## Count accepted designs and the effort needed to obtain them

Suppose 100 generated candidates yield 80 syntax successes, 50 functional-test successes, and 20 candidates satisfying the implemented constraints. Final acceptance is 20% of attempts, not 80%. Reporting only survivors conceals where work was spent and which stage remains limiting.

Total cost includes preparing data and references, training or tuning where applicable, model calls, tool executions, retries, and human investigation. A model call taking one second followed by a 100-second physical evaluation does not make the full attempt a one-second process. Parallel execution changes elapsed time and resource consumption differently.

Repeated use can amortize preparation, but only while the prepared model and references remain applicable. Record how many new tasks share that cost, what invalidates reuse, and what happens when a tool or process changes. A reusable method is stronger evidence than a manually repaired demonstration, but it still needs stated boundaries.

## Long-term hypotheses to test rather than assume

One hypothesis is that learned guidance becomes more useful when it reduces expensive evaluations while preserving final acceptance. Compare against non-learned search with equal checking and preparation budgets. It weakens if saved evaluations are offset by data generation, rejected candidates, or lower valid-output quality.

A second hypothesis is that structured feedback improves transfer more than additional unconstrained generation. Remove or alter feedback components while retaining model access, tools, and compute. It weakens if apparent gains come from stronger checkers or privileged task examples rather than better use of feedback.

A third hypothesis is that trustworthy automation requires explicit boundaries between proposing, checking, and accepting. Test replay by an independent user with the same declared requirements and tools. It weakens as a demonstrated capability when acceptance still depends on hidden intervention or a checker that misses the claimed property.

These are bounded interpretations, not measured ISCA–DAC–ICCAD growth trends or evidence of autonomous design closure. Comparable editions, tasks, data access, budgets, and review standards remain needed. This expanded parent discussion does not complete the individual-paper rewrites, source recovery, classification reconciliation, or independent comprehension and scientific review below.
