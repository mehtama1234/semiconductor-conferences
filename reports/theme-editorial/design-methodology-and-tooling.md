## Follow a design choice through its consequences

A design is chosen in stages, and a candidate that looks best early can fail a later limit.

A design process:

1. starts with required behavior and constraints;
2. builds candidate implementations;
3. evaluates them;
4. selects a result.

Each stage feeds the next. A candidate that looks good in an early representation may turn invalid or expensive once implementation exposes more costs.

> **Worked example.** An arithmetic block must return a result within 10 nanoseconds and take at most 100 area units.
>
> | Candidate | Area units | Time (ns) | Valid? |
> | --- | --- | --- | --- |
> | A | 80 | 12 | No: too slow |
> | B | 95 | 9 | Yes |
>
> A is smaller, but not a valid solution. Reporting only the smallest area would pick the wrong one.

A paper must keep three things separate:

- the **required behavior**;
- the **limits** that define acceptable candidates;
- the **objective** used to choose among acceptable candidates.

**Be careful:** the numbers in this discussion are teaching calculations, not measurements from the linked papers.

## A representation enables some decisions and hides others

How a problem is written down decides which costs a tool can see.

- A **graph** describes objects and links between pairs of them.
- A **hypergraph** lets one link connect several objects.

In a circuit, one signal can connect a driver to several receivers. Grouping objects into partitions can cut the connections that cross partition boundaries, while respecting capacity limits.

The representation does not price every implementation effect. One crossing signal driving ten distant receivers and another driving one nearby receiver may each count as one cut. Their physical load, traffic and timing can differ. A lower cut count is evidence about that objective, not proof of a faster final system.

The [optimization and search chapter](../observed-subthemes/optimization-and-search-methods.md) links this to Impart's multilevel partitioning and the other captured search methods. Their current descriptions do not establish complete downstream conditions. The useful question is which left-out costs could change the selected solution.

**Coarsening** merges several objects into fewer, larger ones before searching. It makes the problem cheaper, but temporarily hides choices about how the merged objects differ. **Refinement** restores the detail and allows adjustments. So a good coarse solution is a starting point. Its quality depends on what the grouping kept, and what refinement can recover.

## A transformation needs a validity condition before a cost estimate

Before asking whether a changed program is faster, show it still computes the right thing.

Two implementations can compute the same intended result with different operation orders or storage. Whether they are equivalent depends on the arithmetic and execution rules:

- Reordering exact integer additions, without overflow, keeps the result.
- Reordering finite-precision floating-point additions can change it, through rounding.

Likewise, a kernel built for contiguous arrays needs a valid alternative, or a rejection path, for an array whose elements are spaced further apart in memory (a larger **stride**). Matching dimensions do not make memory layouts interchangeable. A cache key for reusing an implementation must capture every condition that affects validity, not just the handiest label.

[DyTuner's expanded explanation](../observed-subthemes/compiler-and-runtime-optimization.md#explanation-dac-2026-research127) uses changing tensor shapes to explain this. The official description gives a proposed adaptive tuning method and named comparisons. Its exact adaptation and reuse rules are not recovered.

**Be careful:** this theme must not fill those gaps by treating a plausible specialization policy as the paper's implementation.

So validation is not a final decorative step. It shapes how candidates are built and reused. A cost model should rank candidates only after their behavior and conditions are established, or clearly mark rankings that include candidates still awaiting validation.

## A fast estimate is useful only if it supports the right decision

An estimate's error matters through the decision it changes, especially near a hard limit.

A **cost model** predicts an expensive quantity, such as run time, area, energy or circuit delay. Small errors near a hard limit can matter more than large errors far from it.

> **Worked example.** Timing requirement: 100 picoseconds.
>
> - True arrival: 100.2, so the design fails.
> - Estimate: 99.9, so the design passes.
> - The error is only 0.3 picoseconds, but its direction flips accept to reject.
>
> For a maximum-delay limit, an estimate that is too early is not interchangeable with one that is safely late.

The manuscript-backed [segment-level timing reuse explanation](../observed-subthemes/compiler-and-runtime-optimization.md#explanation-dac-2026-research2566) applies this to sharing timing calculations. Reuse must keep the right electrical context, including the transition behavior that affects later stages. Its discussion keeps discrepancies between the stated checks and unresolved conditions on how error spreads.

> **The general bound (triangle inequality).**
>
> - A stored result differs from a predicted query result by at most `τ`.
> - The predictor's error is at most `e` over that query domain.
> - Then the stored result can differ from the true result by up to `τ + e`.
>
> Checking only `τ` does not establish that total bound.

An average prediction error is not automatically the needed worst-case bound.

This links tooling to [verification](verification-and-validation.md). The claim must say what was checked, under which assumptions, and whether an unresolved case was rejected, re-checked exactly, or accepted without a guarantee.

## Tool runtime and output runtime are different costs

Time spent preparing a faster result pays off only if the result is reused enough.

A compiler can take longer to produce code that runs faster. A search can try more candidates and deliver a better circuit. Whether that trade is worth it depends on how often the result is used, and on the user's budget.

> **Worked example (illustrative, not DyTuner results).** Tuning costs 10 seconds. It cuts each later run from 5 to 4 milliseconds.
>
> - Break-even: 10 seconds ÷ 1 millisecond saved = **10,000 compatible runs**.
> - If the input or hardware changes after 100 runs, and the result cannot be reused: only 100 × 1 ms = **0.1 second** saved.

The same accounting applies to a design tool used once per product versus many times during exploration. Record total preparation and validation costs, as well as the final result's performance. Reuse assumptions must name what invalidates the work. Shape, layout, target hardware, constraints, library versions or model parameters may each matter.

## Search quality must include failed and expensive attempts

Compare search methods at a stated budget, counting every failed and invalid attempt.

An optimizer chooses which candidates to evaluate. A cheap predictor can screen many candidates before expensive implementation. Random variation or a learned policy can explore alternatives. A higher predicted score does not, by itself, show a better valid implementation.

> **Worked example.**
>
> - Method A: 100 candidates × 1 minute = **100 minutes** of serial evaluation.
> - Method B: 20 candidates × 10 minutes = **200 minutes**.
> - B tries fewer candidates but uses twice the serial time.
> - On ten machines at once, B finishes sooner in elapsed time, but uses the same resources.

So compare output quality at stated time and resource budgets, rather than picking whichever denominator favors a method.

Invalid candidates and failed runs belong in the record. If nine runs fail and one gives a good result, reporting only the survivor hides the odds and cost of getting a usable output. To read the variability, record:

- distinct random seeds;
- failures;
- timeout rules;
- how the final result was selected.

Search also tests a predictor differently from random sampling. Search prefers unusually good predictions, and those can include unusually optimistic errors. A random held-out test error does not describe the candidates the optimizer picks. Re-check predicted winners with the intended more trustworthy method, and keep cases where their ranking changes.

## Local improvements must survive the rest of the process

Each stage gives something new, but leaves something still unproven.

| Stage | What becomes available | What remains unproven |
| --- | --- | --- |
| Candidate generation | A proposed representation or implementation | Valid behavior and constraint satisfaction |
| Cheap evaluation | A ranking under a model or simplified objective | Accuracy on selected candidates and downstream costs |
| Implementation and validation | A result under stated tools, targets, and checks | Transfer to different configurations or untested conditions |
| Deployment or repeated use | Measured benefit under the chosen workload | Broader generality, future workload stability, and independent reproduction |

These stages can loop: a failed implementation can guide a new candidate. The feedback must keep why it failed. If a constraint violation is treated as just a poor score, the search can keep picking invalid outputs whenever another score part makes up for it.

The [architecture theme](architecture-and-accelerators.md) adds the next requirement. A compiler's improved operator, or an accelerator generator's favorable model, must still fit a complete application with data movement, numerical quality and preparation costs.

**Be careful:** gains at several stages cannot be multiplied when they use different baselines or overlapping work.

## Three long-term hypotheses and their limits

Three readings are worth testing; each names what would weaken it.

| Hypothesis | Test | What would weaken it |
| --- | --- | --- |
| Conditional reuse helps more as contexts vary but keep revisiting related cases | Record reuse frequency, invalidations, lookup cost, preparation cost and output validity | Contexts change too often, applicability checks dominate, or reuse harms the required result |
| Early estimates are worth more when their uncertainty explicitly changes later decisions | Compare exact evaluation everywhere with screening plus exact fallback, at fixed accepted-result requirements | Screening rejects valuable candidates, admits invalid ones, or spends the saved budget on rework |
| Reusable tooling depends on keeping context across stages, not just exchanging files | Can an independent user reproduce a result from recorded versions, constraints, representations, seeds and validation steps? | An undocumented manual fix or unavailable component is still needed |

These are mechanism-based interpretations, not established ISCA–DAC–ICCAD trends. A cross-conference comparison needs compatible problems, objectives, input populations, source depth and budgets.

**Be careful:** a compiler paper, a partitioner paper and a physical implementation paper may add complementary evidence. They do not form an integrated process just because their subjects are related.

The two [compiler/runtime explanations](../observed-subthemes/compiler-and-runtime-optimization.md) give the deepest current reading path used here: timing reuse is manuscript-backed and DyTuner remains description-backed. The other tooling branches below still need fuller paper-level writing, evidence recovery and independent review. This synthesis does not close those gaps or establish accepted conclusions over time.
