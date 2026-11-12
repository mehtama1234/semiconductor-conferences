# Design methodology and tooling

This article explains the subject and then connects it to 29 papers in the selected research sample.

A subtheme groups related technical problems. A mechanism describes the particular change proposed by a paper. The discussion below explains the subject; the linked paper records state the available evidence.

[Definitions used in the paper records](../reading-guide-v1.md)

## Design tools make many small choices that add up

- A **compiler** turns a program from one form into another while keeping its intended behavior.
- A **synthesis tool** builds a circuit implementation.
- An **optimizer** picks among implementations by a stated goal.

Together these choices decide run time, memory use, circuit size, and the effort needed to get a result.

## How a design is written down decides what a tool can see and change

A representation makes some properties visible and hides others.

- A **graph** can show which operations depend on which.
- A **schedule** assigns operations to times or resources.

Removing redundant work can also change memory traffic or available parallelism. So a tool needs two things: a rule for which changes keep the design correct, and a cost model for picking useful ones.

## The subthemes change the steps, the search, the structure, or the benchmarks

- **Compilation and synthesis** methods change the sequence of transformations.
- **Search** methods choose configurations or implementations.
- **Graph and partitioning** methods organize connected work.
- **Benchmark and artifact** methods publish inputs, expected outputs and steps so others can compare.

Their shared question: can another designer or user get the claimed benefit by following a defined process?

## A fair test separates tool time from the time the output saves

1. State inputs, versions, settings, hardware, and the total time to get a valid output.
2. Separate time spent running the tool from time saved by its output.
3. Compare correctness and output quality, not only run time.
4. Test on unfamiliar inputs. That is a stronger test than re-tuning on the development examples.

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

Likewise, a kernel built for arrays stored side by side needs a plan for spaced-out arrays. The spacing between elements is the **stride**. The kernel must handle a larger stride correctly, or refuse it. Matching dimensions do not make memory layouts interchangeable. A cache key for reusing an implementation must capture every condition that affects validity, not just the handiest label.

[DyTuner's expanded explanation](../observed-subthemes/compiler-and-runtime-optimization.md#explanation-dac-2026-research127) uses changing tensor shapes to explain this. The official description gives a proposed adaptive tuning method and named comparisons. Its exact adaptation and reuse rules are not recovered.

**Be careful:** this theme must not fill those gaps by treating a plausible specialization policy as the paper's implementation.

So validation is not a final decorative step. It shapes how candidates are built and reused. A cost model should rank only candidates whose behaviour is already checked. Otherwise it must mark which ranked candidates are still unchecked.

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

This links tooling to [verification](verification-and-validation.md). The claim must say what was checked and under which assumptions. It must also say what happened to unresolved cases: rejected, re-checked exactly, or accepted without a guarantee.

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

Invalid candidates and failed runs belong in the record. Say nine runs fail and one gives a good result. Reporting only that one hides the odds, and the cost, of getting a usable output. To read the variability, record:

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

These stages can loop: a failed implementation can guide a new candidate. The feedback must keep why it failed. Treat a broken rule as just a low score, and the search can keep picking invalid outputs. Another part of the score can make up for the break.

The [architecture theme](architecture-and-accelerators.md) adds the next requirement. A faster compiled step, or a good result from an accelerator generator, must still fit the whole application. That includes data movement, numerical quality and set-up costs.

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

## Subthemes and how to study them

Each link opens the subtheme discussion and its captured paper records. Explanatory depth varies: some papers have expanded individual explanations; others still have only brief discussion or evidence cards. Source locations and unresolved conditions remain visible.

### [Optimization and search methods](../observed-subthemes/optimization-and-search-methods.md)

7 selected records in this theme. Start with [Impart: Integration of Memetic Operations into Multi-Level Framework for Large-k-Way Hypergraph Partitioning](../observed-subthemes/optimization-and-search-methods.md).

### [Graph and hypergraph optimization](../observed-subthemes/graph-and-hypergraph-optimization.md)

3 selected records in this theme. Start with [Compart: Community-Guided Post-Coarsening for High-Quality Hypergraph Partitioning](../observed-subthemes/graph-and-hypergraph-optimization.md).

### [Logic synthesis and optimization](../observed-subthemes/logic-synthesis-and-optimization.md)

3 selected records in this theme. Start with [Transsyn: Scalable, Area-Oriented Transistor Network Synthesis via Cut-Based Mapper with SAT-Based Refinement](../observed-subthemes/logic-synthesis-and-optimization.md).

### [Compiler and runtime optimization](../observed-subthemes/compiler-and-runtime-optimization.md)

2 selected records in this theme. Start with [Optimizing Dynamic-Shape Neural Networks: A Unified Approach to Adaptive Tuning](../observed-subthemes/compiler-and-runtime-optimization.md).

### [High level synthesis and compilers](../observed-subthemes/high-level-synthesis-and-compilers.md)

2 selected records in this theme. Start with [Dataflowgen: An MLIR-Based Compiler for Efficient Dataflow Accelerator Generation](../observed-subthemes/high-level-synthesis-and-compilers.md).

### [Synthesis and compilation](../observed-subthemes/synthesis-and-compilation.md)

2 selected records in this theme. Start with [Search Smarter, Not Harder: A Scalable, High-Quality Zoned Neutral Atom Compiler](../observed-subthemes/synthesis-and-compilation.md).

### [Architecture modeling and exploration](../observed-subthemes/architecture-modeling-and-exploration.md)

1 selected records in this theme. Start with [Idealsim: Efficient Ideal Scenario Modeling for Processor Upper-Bound Performance Analysis](../observed-subthemes/architecture-modeling-and-exploration.md).

### [Cell and circuit design](../observed-subthemes/cell-and-circuit-design.md)

1 selected records in this theme. Start with [Celle: Automated Standard Cell Library Extension via Equality Saturation](../observed-subthemes/cell-and-circuit-design.md).

### [Compilation and mapping](../observed-subthemes/compilation-and-mapping.md)

1 selected records in this theme. Start with [RAM-CGRA: Reachability-Aware Mapping for CGRAs](../observed-subthemes/compilation-and-mapping.md).

### [Cross layer design automation](../observed-subthemes/cross-layer-design-automation.md)

1 selected records in this theme. Start with [L2L: Logic to Layout Exploration of Standard Cell Library Design](../observed-subthemes/cross-layer-design-automation.md).

### [Hardware generation and compilation](../observed-subthemes/hardware-generation-and-compilation.md)

1 selected records in this theme. Start with [FSGen: Agile Fused and Sparse Accelerator Generator with Accurate Power Model for LLM Applications](../observed-subthemes/hardware-generation-and-compilation.md).

### [Partitioning and placement](../observed-subthemes/partitioning-and-placement.md)

1 selected records in this theme. Start with [Ihyperg: Incremental Hypergraph Partitioning on GPU](../observed-subthemes/partitioning-and-placement.md).

### [Power and thermal design](../observed-subthemes/power-and-thermal-design.md)

1 selected records in this theme. Start with [An Agile and Accurate Energy Estimation Methodology for CGRA-Mapped Algorithms: The Synchoros Approach](../observed-subthemes/power-and-thermal-design.md).

### [Reproducibility artifacts and benchmarks](../observed-subthemes/reproducibility-artifacts-and-benchmarks.md)

1 selected records in this theme. Start with [Capbench: A Multi-PDK Dataset for Machine-Learning-Based Post-Layout Capacitance Extraction](../observed-subthemes/reproducibility-artifacts-and-benchmarks.md).

### [Simulation and numerical methods](../observed-subthemes/simulation-and-numerical-methods.md)

1 selected records in this theme. Start with [EastPCG: An Efficient and Self-Tuning Graph Sparsification Based PCG Solver for Circuit Simulation](../observed-subthemes/simulation-and-numerical-methods.md).

### [Verification and debugging tools](../observed-subthemes/verification-and-debugging-tools.md)

1 selected records in this theme. Start with [Schemacoder: Automatic Log Schema Extraction Coder with Residual Q-Tree Boosting](../observed-subthemes/verification-and-debugging-tools.md).

## Representative source-backed records

The following reading set spans the available conferences and uses dated corrections where registered. These corrections improve the current reading view but do not change historical adjudication or establish independent acceptance. Each paper link opens its exact evidence card.

## Paper cards: what changes and where it stops

- [CODO: An Automated Compiler for Comprehensive Dataflow Optimization](../observed-subthemes/high-level-synthesis-and-compilers.md#paper-isca-2026-program-002) — ISCA 2026.
- [FSGen: Agile Fused and Sparse Accelerator Generator with Accurate Power Model for LLM Applications](../observed-subthemes/hardware-generation-and-compilation.md#paper-dac-2026-research868) — DAC 2026.
- [Delay-Constrained Area Optimisation Using SAT-Based Local Improvement](../observed-subthemes/logic-synthesis-and-optimization.md#paper-dac-2026-research754) — DAC 2026.
- [Idealsim: Efficient Ideal Scenario Modeling for Processor Upper-Bound Performance Analysis](../observed-subthemes/architecture-modeling-and-exploration.md#paper-dac-2026-research690) — DAC 2026.
- [Shared Logic Unleashed: Multiple-Node Boolean Optimization for Next-Gen Synthesis](../observed-subthemes/logic-synthesis-and-optimization.md#paper-dac-2026-research3091) — DAC 2026.
- [Automated Design Space Exploration in High-Level Physical Synthesis](../observed-subthemes/optimization-and-search-methods.md#paper-iccad-2025-109) — ICCAD 2025.
- [Orthrus: Dual -Loop Automated Framework for System -Technology Co - Optimization](../observed-subthemes/optimization-and-search-methods.md#paper-iccad-2025-437) — ICCAD 2025.
- [Hyperefs: Adaptive Clique Sampling for Scalable Effective Resistance Estimation in Large Hypergraphs](../observed-subthemes/graph-and-hypergraph-optimization.md#paper-dac-2026-research2887) — DAC 2026.
- [An Agile and Accurate Energy Estimation Methodology for CGRA-Mapped Algorithms: The Synchoros Approach](../observed-subthemes/power-and-thermal-design.md#paper-dac-2026-research2851) — DAC 2026.
- [Celle: Automated Standard Cell Library Extension via Equality Saturation](../observed-subthemes/cell-and-circuit-design.md#paper-dac-2026-research278) — DAC 2026.
- [Hyspecpro: Scalable Hypergraph Partitioning via Spectral Projection Optimization](../observed-subthemes/graph-and-hypergraph-optimization.md#paper-dac-2026-research2694) — DAC 2026.
- [Path-Based Timing Analysis Acceleration via Segment-Level Timing Arc Reuse](../observed-subthemes/compiler-and-runtime-optimization.md#paper-dac-2026-research2566) — DAC 2026.

## What the evidence supports

These records identify proposed methods and the conditions recorded for them. A reported improvement should be interpreted with its comparison method, input size, hardware, and result-quality requirement. Missing fields are evidence gaps; a populated field can also state that a detail is unspecified.

## Limits and next evidence

The selected sample is uneven across conferences and source types. It cannot establish how fast a subject is growing. Repeated observations across comparable years, with the same inclusion rules and source depth, are needed for a time trend.

Every linked evidence article preserves the Problem: and Mechanism / artifact: fields, baseline, unshortened limitations, source URL, and recorded location. Primary text and independent review remain necessary where the record says those checks are open.

[Research directions](../directions/README.md) · [All observed subthemes](../expanded-taxonomy-v1.md)
