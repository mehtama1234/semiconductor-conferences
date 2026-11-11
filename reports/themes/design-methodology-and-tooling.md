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

A design process starts with required behavior and constraints, constructs candidate implementations, evaluates them, and selects a result. Each stage produces information another stage uses. A candidate that looks favorable in an early representation may become invalid or expensive once implementation exposes additional costs.

Consider an arithmetic block that must return a result within ten nanoseconds and occupy at most 100 area units. Candidate A occupies 80 units but takes twelve nanoseconds. Candidate B occupies 95 units and takes nine. A is smaller, but it is not a valid solution to this problem. Reporting only minimum area would select the wrong outcome.

This simple example separates three things that a paper must preserve: the required behavior, the limits that define acceptable candidates, and the objective used to choose among acceptable candidates. The numerical examples in this discussion are teaching calculations, not measurements from the linked papers.

## A representation enables some decisions and hides others

A graph describes objects and pairwise relationships. A hypergraph allows one relationship to connect several objects. In a circuit, one signal can connect a driver to several receivers. Grouping these objects into partitions may reduce connections that cross partition boundaries while respecting capacity limits.

The representation does not automatically price every implementation effect. One crossing signal driving ten distant receivers and another driving one nearby receiver may each contribute one unit to a simple cut-count objective. Their physical loading, communication traffic, and timing can differ. A lower cut count is evidence about that objective, not proof of a faster final system.

The [optimization and search chapter](../observed-subthemes/optimization-and-search-methods.md) connects this issue to Impart's multilevel partitioning and the other captured search methods. Those current descriptions do not establish complete downstream implementation conditions. The useful question is which omitted costs can change the selected solution, not whether the representation is universally good or bad.

Coarsening combines several objects into fewer larger objects before searching. This can make a problem cheaper to solve, but temporarily removes choices about how the combined objects differ. Refinement restores detail and permits adjustments. A successful coarse solution is therefore a starting point whose quality depends on what the grouping retained and what refinement can recover.

## A transformation needs a validity condition before a cost estimate

Two implementations can compute the same intended result while using different operation orders or storage. That equivalence depends on the arithmetic and execution rules. Reordering exact integer additions without overflow is not the same claim as reordering finite-precision floating-point additions, where rounding can change the result.

Similarly, a kernel specialized for contiguous arrays needs a valid alternative or rejection path for an array whose elements are separated by a larger address stride. Identical dimensions alone do not establish interchangeable memory layouts. A cache key identifying a reusable implementation must capture the conditions that affect validity, not merely the most convenient label.

[DyTuner's expanded explanation](../observed-subthemes/compiler-and-runtime-optimization.md#explanation-dac-2026-research127) uses dynamic tensor shapes to explain this distinction. The official description supplies a proposed adaptive tuning method and named comparisons, but its exact adaptation and reuse rules remain unrecovered. The theme must not fill those gaps by treating a plausible specialization policy as the paper's implementation.

Validation is therefore not a final decorative step. It constrains candidate construction and reuse. A cost model should rank candidates only after their required behavior and applicable conditions are established, or clearly record that its rankings include candidates awaiting validation.

## A fast estimate is useful only if it supports the right decision

A cost model predicts an expensive quantity, such as execution time, area, energy, or circuit delay. Prediction error matters partly through its effect on the decision. Small errors near a hard limit can be more consequential than larger errors far from it.

Suppose a timing requirement is 100 picoseconds. A true arrival at 100.2 fails, but an estimate of 99.9 passes. The absolute error is only 0.3 picoseconds; its direction changes the accept/reject decision. For this maximum-delay requirement, an estimate that is too early is not interchangeable with one that is conservatively late.

The manuscript-backed [segment-level timing reuse explanation](../observed-subthemes/compiler-and-runtime-optimization.md#explanation-dac-2026-research2566) applies this reasoning to sharing timing calculations. Reuse must retain the appropriate electrical context, including the transition behavior that affects later stages. Its source-specific discussion preserves discrepancies between the stated checks and unresolved conditions on error propagation.

A useful general bound follows from the triangle inequality. If a stored result differs from a predicted query result by at most a tolerance `τ`, and the predictor's error is bounded by `e` over that query domain, then the stored result can differ from the true query result by up to `τ + e`. Checking only `τ` does not establish that total bound. An average prediction error is not automatically the needed worst-case bound.

This connects tooling to [verification](verification-and-validation.md): the claim must say what was checked, under which assumptions, and whether an unresolved case was rejected, re-evaluated exactly, or accepted without a guarantee.

## Tool runtime and output runtime are different costs

A compiler can take longer to produce code that runs faster. A search can evaluate more candidates and deliver a better circuit. Neither tradeoff is good or bad without knowing how often the result will be used and what budget the user has.

Suppose tuning costs ten seconds and reduces each later invocation from five to four milliseconds. The one-millisecond saving needs 10,000 compatible invocations to recover that cost. If the input or hardware changes after 100 invocations and the prepared result cannot be reused, only 0.1 second is saved. These are illustrative calculations, not DyTuner results.

The same accounting applies to a design tool used once per product versus repeatedly during exploration. Record total preparation and validation costs as well as the final result's performance. Reuse assumptions must include what changes invalidate the work: shape, layout, target hardware, constraints, library versions, or model parameters may each matter.

## Search quality must include failed and expensive attempts

An optimizer chooses which candidates to evaluate. A cheap predictor can screen many candidates before expensive implementation, while random variation or a learned policy can explore alternatives. A higher predicted score does not itself establish a better valid implementation.

Suppose method A spends one minute on each of 100 candidates and method B spends ten minutes on each of twenty. B evaluates fewer candidates but consumes twice the serial evaluation time. If B uses ten machines concurrently, its elapsed time may improve while its resource consumption does not. Compare the output quality at stated time and resource budgets rather than choosing whichever denominator favors a method.

Invalid candidates and unsuccessful runs belong in the record. If nine runs fail and one obtains a good result, reporting only that survivor hides the probability and cost of obtaining a usable output. Distinct random seeds, failures, timeout rules, and the procedure for selecting a final result are necessary to interpret variability.

Candidate selection also tests a predictor differently from random sampling. Search preferentially chooses unusually favorable predictions, which can include unusually optimistic errors. A held-out random test error does not automatically characterize the candidates the optimizer will select. Evaluate predicted winners with the intended higher-confidence method and retain cases where their ranking changes.

## Local improvements must survive the rest of the process

| Stage | What becomes available | What remains unproven |
| --- | --- | --- |
| Candidate generation | A proposed representation or implementation | Valid behavior and constraint satisfaction |
| Cheap evaluation | A ranking under a model or simplified objective | Accuracy on selected candidates and downstream costs |
| Implementation and validation | A result under stated tools, targets, and checks | Transfer to different configurations or untested conditions |
| Deployment or repeated use | Measured benefit under the chosen workload | Broader generality, future workload stability, and independent reproduction |

These stages can repeat: a failed implementation can guide a new candidate. The feedback must retain why the candidate failed. Treating a constraint violation as merely a poor score can allow the search to keep selecting invalid outputs if another score component compensates for it.

The [architecture theme](architecture-and-accelerators.md) adds the downstream requirement: a compiler's improved operator or an accelerator generator's favorable model must still fit a complete application with data movement, numerical quality, and preparation costs. Improvements at several stages cannot be multiplied when they concern different baselines or overlapping work.

## Three long-term hypotheses and their limits

One hypothesis is that conditional reuse becomes more useful as design and execution contexts vary but repeatedly revisit related cases. Test it by recording reuse frequency, invalidations, lookup cost, preparation cost, and output validity. It weakens when contexts change too often, applicability checks dominate, or reuse compromises the required result.

A second hypothesis is that earlier estimates become more valuable when their uncertainty changes later decisions explicitly. Compare exact evaluation everywhere with screening plus exact fallback, keeping the accepted-result requirements fixed. It weakens when screening mistakes reject valuable candidates, admit invalid ones, or consume the saved evaluation budget in rework.

A third hypothesis is that reusable tooling depends on preserving context across stages, not merely exchanging files. Test whether an independent user can reproduce a result with recorded versions, constraints, representations, seeds, and validation steps. It weakens where an undocumented manual correction or unavailable component remains necessary.

These are mechanism-based interpretations, not established ISCA–DAC–ICCAD trends. A cross-conference comparison needs compatible problems, objectives, input populations, source depth, and budgets. A compiler paper, partitioner paper, and physical implementation paper may contribute complementary evidence, but they do not establish an integrated process simply because their subjects are related.

The two [compiler/runtime explanations](../observed-subthemes/compiler-and-runtime-optimization.md) provide the deepest current individual reading path used here: timing reuse is manuscript-backed and DyTuner remains description-backed. The other tooling branches below still need fuller paper-level writing, evidence recovery, and independent review. This synthesis does not close those gaps or establish accepted temporal conclusions.

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
