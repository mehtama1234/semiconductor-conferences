## An optimization is valid only under its assumptions

A compiler prepares a computation for execution; a runtime manages choices made while it executes. Both can specialize work to known conditions or reuse earlier results. These savings depend on recognizing when the earlier assumptions still hold. If the input size or electrical context changes, blindly reusing a previous choice can be slow or incorrect.

This group contains dynamic-shape neural-network tuning and reuse in timing analysis. They are different applications of a shared question: which work can be avoided safely, and how much does detecting that opportunity cost?

<span id="explanation-dac-2026-research127"></span>

## DyTuner: when is a faster implementation worth preparing?

### Start with the computation and its shape

A tensor is an array of values with one or more dimensions. Its shape specifies the length of each dimension. A batch of 8 sequences, each with 128 positions and 64 values per position, has shape 8 × 128 × 64 and contains 65,536 values. If sequence length becomes 256, this array contains 131,072 values. The program still performs the same kind of operation, but the amount and organization of work have changed.

An operator is a computation such as matrix multiplication. A kernel is executable code implementing that computation on a device. Compilation prepares executable code; tuning chooses among ways to implement the operation, often by measuring candidates. Here, tuning concerns execution, not retraining the neural network's learned weights.

Shape can change more than the number of values. In ordinary dense attention, comparing every sequence position with every other position produces a length-by-length score array. Increasing length from 128 to 256 doubles the sequence length but increases that score array from 16,384 to 65,536 entries. This is a worked example of shape-dependent work, not a DyTuner benchmark or a claim that all attention implementations materialize that array.

### Why the same kernel may not remain the best choice

Hardware usually processes work in groups. A tiled matrix kernel divides a larger operation into smaller rectangular blocks so values can be reused locally. A large tile can increase reuse, but also requires storage and enough work to keep its execution resources busy. A small input can leave much of that capacity unused.

For an illustrative one-dimensional boundary, a 128-element tile needs two tiles to cover 129 elements. The two tiles contain 256 positions, only 129 of which correspond to actual elements. A 32-element tile needs five tiles, with 160 positions. These counts alone do not predict runtime: the smaller-tile kernel can have more scheduling overhead or less reuse. They explain why the fastest implementation need not change smoothly with input length.

Shape is also not the whole execution context. Two arrays can have identical dimensions but different strides—the address increments used to move between elements. An implementation assuming contiguous values cannot necessarily process a strided view correctly without additional logic. Data type, alignment, supported operations, and device capabilities can likewise constrain reuse. A valid specialization must state the conditions under which it is applicable, not merely remember a shape label.

### What is actually known about DyTuner

The [official DAC description](https://63dac.conference-program.com/presentation/?id=RESEARCH127&sess=sess140) identifies **DyTuner** as an adaptive, operator-level tuning framework with a system-compatible interface. It reports up to 1.41× and 1.64× speedups over BladeDISC and TorchInductor, respectively, and claims reduced redundant compilation. The earlier reading card incorrectly said no numerical results or named baselines were available.

The description does not expose the adaptation rule, candidate-generation procedure, precise integration interface, hardware, or measured shape sequences. A matching full manuscript was not recovered in this pass. Therefore, the discussion below explains the decisions such a method must handle; it does not invent DyTuner's internal algorithm. The similarly titled ASPLOS 2024 MikPoly work is a different paper with different authors and is not substituted for this DAC paper.

### Count preparation as well as execution

Suppose a general kernel takes 2 ms per invocation. Preparing a specialized kernel costs 100 ms, after which execution takes 1 ms per invocation. For n invocations, the general implementation costs 2n ms and the specialized choice costs 100 + n ms. The choices tie at n = 100; specialization saves total time only beyond 100 uses. These are constructed numbers, not reported measurements.

If choosing the specialization also costs 0.1 ms per invocation, the comparison becomes 2n versus 100 + 1.1n. The first integer count at which specialization wins is 112. If the shape appears only ten times, preparing the faster kernel increases total work despite making each prepared execution faster.

This is why a dynamic-shape workload must be a sequence, not just a list of sizes. A size that appears repeatedly can repay preparation. A stream of unique sizes may not. A rare size can also cause a long individual delay even if the average is good. Reporting only performance after every specialization has already been prepared hides the first-use cost.

An implementation can avoid some repeated preparation by reusing compiled code or sharing implementations across shape ranges. Those are possible design choices, not verified DyTuner mechanisms. Their tradeoff is explicit: more specialized versions can improve execution but consume compilation effort and storage; broader versions can reduce that effort while doing extra work on individual inputs.

### Separate validity from predicted performance

A guard is a check that a prepared implementation's assumptions still hold. If a kernel requires a dimension divisible by 16, accepting a dimension of 17 without a correct boundary path can produce wrong results. That is a validity failure. Selecting a slower but correct kernel for dimension 17 is a performance failure. A tuning framework needs both a correctness boundary and a policy for choosing among valid candidates.

Benchmark noise complicates that policy. A candidate measured while a device is busy may look intrinsically slow. Measurements can also change with clock state, available memory, or interference from other work. Repeated, controlled comparisons help separate the candidate's behavior from the conditions of the trial. A system adapting to changed conditions needs a way to distinguish persistent changes from a single noisy observation.

Faster individual operators do not guarantee faster whole-network execution. In a constructed example, one kernel saves 0.5 ms but requires an additional 0.8 ms layout conversion before the next operator. The complete sequence is 0.3 ms slower. A useful interface must preserve compatibility with surrounding operations, and the evaluation must include any conversion, dispatch, and synchronization work it introduces.

Numerical requirements must also stay fixed. Changing arithmetic order can change floating-point rounding even when the mathematical expression is unchanged. A comparison should specify whether outputs must be bit-identical or agree within a stated tolerance. A speed gain obtained by silently weakening that requirement is not solely a compiler improvement.

### Interpret the reported speedups without losing their conditions

A speedup is baseline time divided by proposed time. A 1.41× speedup corresponds to about 29.1% less time; 1.64× corresponds to about 39.0% less time. Neither means 41% or 64% less time. The two reported maxima use different baselines and should not be multiplied together or treated as a guaranteed result on every shape.

To establish an end-to-end benefit, the missing evaluation needs total elapsed time from first use, the ordered shape distribution, compilation and tuning cost, peak storage, fallback behavior, model accuracy requirements, and hardware/software versions. Steady-state kernel timing is useful, but it answers a narrower question. The official description supports a reported performance claim, not a reproduced explanation of when its adaptation policy wins.

The conceptual lesson is that specialization is an investment whose return depends on valid future reuse. The open paper-specific question is how DyTuner estimates that opportunity and controls its cost. Independent comprehension review and manuscript recovery remain open.

<span id="explanation-dac-2026-research2566"></span>

## Segment-level timing reuse: share calculations without hiding a late signal

### What timing analysis calculates

A digital circuit must produce values in time for the components that consume them. For a simplified setup-time check, a path has an arrival time and a required arrival time. Slack is required time minus arrival time. If the requirement is 100 ps and the signal arrives at 98 ps, slack is +2 ps. Arrival at 103 ps gives −3 ps, indicating a violation under these assumptions. A picosecond, abbreviated ps, is one trillionth of a second.

Static timing analysis computes such relationships from circuit structure and timing models rather than requiring a simulation of every input sequence. A timing arc describes one local dependency: for example, from a logic cell's input to its output, or along the wire connecting cells. A path chains these dependencies from a starting point to an endpoint.

Delay and slew are different quantities. Delay describes how much later a corresponding output transition occurs. Slew describes how long a transition takes to change between specified voltage thresholds. A slowly changing input can make the next cell respond differently from a sharply changing one. Load capacitance, the electrical load charged or discharged by an output, also affects its response.

Therefore a path calculation must propagate both accumulated delay and the transition shape summarized by slew. Reusing only a delay number while losing the appropriate output slew can change the input condition for every later calculation.

### Why overlapping paths still create repeated work

Graph-based analysis combines timing information at shared nodes. Path-based analysis retains individual path context and can avoid combining worst cases that do not belong to the same path. This accuracy comes with repeated calculations when many paths traverse the same circuit section.

Consider three paths with distinct prefixes followed by the same ten-arc suffix. Evaluating each suffix separately performs thirty arc calculations. If the three suffix-entry conditions are equivalent for the required accuracy, ten calculations plus reuse can suffice. If their entry slews differ enough to change the suffix response, sharing circuit objects alone is insufficient.

This is why reuse changes the amount of work rather than merely distributing the original work across more processors. The saving depends on the workload's overlap and on which contexts can safely share results. A set of unrelated paths can offer little reuse even on a very large circuit.

### How the paper locates reusable work

The manuscript splits paths into single-fanin chains bounded by multi-fanin nodes. SegHashMap indexes a segment by its ending arc and stores representative slew/polarity keys in a red-black tree. See [Sections 3.1–3.2, PDF page 3](https://changmg.github.io/papers/Ye_Hu_Tian_Meng_He_Shi_Path-Based-Timing-Analysis-Acceleration-via-Segment-Level-Timing-Arc-Reuse.pdf#page=3).

A fanin is an incoming dependency. Inside a chain with one incoming arc per internal node, the predecessor sequence is unambiguous. At a node with multiple incoming arcs, different paths can bring different conditions. Stopping there gives the method a boundary at which those conditions must be handled explicitly.

The two indexes answer different questions. The segment index asks which chain is being evaluated. The ordered slew index asks which previously calculated condition is suitable for the current query. A red-black tree is a balanced search tree: it keeps lookup depth proportional to the logarithm of the number of entries rather than scanning all stored values. Fast lookup helps only if the stored result is applicable.

Imagine stored rising-transition slews of 10, 20, and 40 ps, and a query at 18 ps. The nearest stored larger value is 20 ps. A falling-transition entry with the same numerical slew is not automatically interchangeable. Similarly, reusing entries after a library, load, or circuit change would require checking that the associated context is still valid. These examples explain the data-structure requirements; they are not reproduced paper traces.

### How the learned model participates in reuse

The predictor uses delay-table patches and circuit metadata, with training on delay values, local derivatives, and perturbation consistency. Algorithm 1 compares an exact cached delay with a predicted query delay, reusing the cache entry when their difference meets the segment tolerance. [PDF pages 4–5](https://changmg.github.io/papers/Ye_Hu_Tian_Meng_He_Shi_Path-Based-Timing-Analysis-Acceleration-via-Segment-Level-Timing-Arc-Reuse.pdf#page=4).

A derivative measures how much one quantity changes when another changes slightly. In this case, it is delay sensitivity to input slew. Two predictors can agree on the delay at 20 ps yet disagree about the effect of moving to 19 ps. Training only the value at 20 ps would not distinguish them. Training nearby changes encourages a model suitable for deciding whether two conditions are close enough to share a calculation. This is the meaning of the paper's Sobolev-style supervision; it does not require the reader to treat the name as an explanation.

For a constructed example, a cached exact delay is 50 ps and the predicted query delay is 49.98 ps. A tolerance of 0.05 ps accepts their 0.02 ps difference. But if the true query delay is 50.20 ps, reuse underestimates it by 0.20 ps. The comparison against a prediction alone has not bounded the true error.

More formally, the true difference is at most the checked difference plus the predictor's error, by the triangle inequality. If the checked difference is at most τ and a validated predictor bound is e, the resulting bound is τ + e, not τ alone. A small average training error does not establish a uniform bound e over every deployment query. This is a mathematical condition needed to interpret the guarantee, not an observed failure of the implementation.

The same distinction applies to output slew. Even when one segment's delay error is small, an inaccurate outgoing slew may increase downstream error. A complete argument must account for that propagation rather than adding local delay errors as though later inputs were unaffected.

### What preserving pessimism means

For the simplified maximum-delay check above, a pessimistic estimate is late rather than early: it may report a violation that exact analysis would remove, but it should not hide a real late arrival. Reusing the response to a larger slew can be conservative only when the relevant delay response and propagated context justify that direction. This statement is specific to the checking objective; minimum-delay checks require their own reasoning.

The direction of error matters as well as its magnitude. With a 100 ps requirement and true arrival at 100.2 ps, estimating 99.9 ps changes a failing path into an apparent pass. The absolute error is only 0.3 ps, but its consequence is important. Reporting maximum absolute error without signed errors does not itself establish one-sided conservatism.

The paper's Section 3.3 compares two predicted delays, whereas Algorithm 1 compares an exact cached delay against a prediction. [PDF pages 4–5](https://changmg.github.io/papers/Ye_Hu_Tian_Meng_He_Shi_Path-Based-Timing-Analysis-Acceleration-via-Segment-Level-Timing-Arc-Reuse.pdf#page=4). These checks need not accept the same queries. The implementation choice and associated guarantee remain to be reconciled.

### Check the path budget rather than assuming it adds up

Equation 11 assigns each segment `τsegment = τtotal × N(segment)/N`, where N counts analyzed paths and N(segment) counts paths through that segment. [PDF pages 4–5](https://changmg.github.io/papers/Ye_Hu_Tian_Meng_He_Shi_Path-Based-Timing-Analysis-Acceleration-via-Segment-Level-Timing-Arc-Reuse.pdf#page=4).

That rule gives frequently reused segments more tolerance. It does not by itself ensure that the tolerances on any one path sum to τtotal. Suppose two consecutive segments are present in every analyzed path. Each receives τtotal, so the sum on a path is 2τtotal. This counterexample concerns the stated allocation formula, not a reproduced timing error.

To claim a per-path total bound, the method needs an additional constraint, normalization, or validated accumulation argument. It must also include predictor error and propagated slew effects. Empirically small errors are useful evidence, but are not a substitute for that argument.

### What the performance figures actually measure

The evaluation uses TAU15 circuits and OpenTimer v2. Table 3 uses 64 threads and reports average speedups of 13.25× at 1,000 paths and 195× at five million. The latter column includes a 2.36 ps maximum error for pci_bridge32_ispd. [PDF pages 5–6](https://changmg.github.io/papers/Ye_Hu_Tian_Meng_He_Shi_Path-Based-Timing-Analysis-Acceleration-via-Segment-Level-Timing-Arc-Reuse.pdf#page=5).

Thus 195× is not the average over every query size, and sub-picosecond error is not universal across the table. The table labels the metric maximum absolute error; a later reference to mean absolute error should not silently change its interpretation. The average of several circuit maxima is also not the single worst error across all circuits.

The setup chooses `τtotal = 0.1 × N`. The GPU comparison is indirect and uses published speedups. [Section 4, PDF pages 5–6](https://changmg.github.io/papers/Ye_Hu_Tian_Meng_He_Shi_Path-Based-Timing-Analysis-Acceleration-via-Segment-Level-Timing-Arc-Reuse.pdf#page=5).

Substituting that experimental budget into Equation 11 yields `τsegment = 0.1 × N(segment)`. Consequently, as the number of paths through a segment grows, its allowed reuse tolerance grows too. Greater overlap and a looser reuse tolerance can both influence speed. A fixed-error-budget experiment would be needed to isolate how much improvement comes from overlap alone.

An indirect GPU comparison divides speedups measured relative to a supposedly comparable baseline. It requires matching baseline configuration and workload conditions; it is not an execution of both methods on the same machine. Training cost, model inference placement, preparation, cache memory, and repeated-query behavior also need explicit accounting before interpreting the headline as complete workflow savings.

Reducing evaluated arcs is not identical to reducing total runtime. Reuse adds indexing, prediction, and path reconstruction. In an illustrative calculation, eliminating 90 of 100 equal-cost arc evaluations saves 90 units, but adding 30 units of reuse overhead leaves a 40-unit total: 2.5× faster, not 10×. Actual gains depend on these relative costs.

### What connects this result to compiler/runtime optimization

Both papers ask whether previously prepared work can be reused under a new context. DyTuner concerns choosing executable implementations for new tensor shapes; this paper concerns reusing numerical timing responses for new signal conditions. The shared idea is conditional reuse, not a shared algorithm or application.

The timing paper also belongs conceptually in timing-analysis tooling. Its current placement in this compiler/runtime group is a taxonomy boundary to reconcile, not evidence that it compiles neural-network kernels. Both records retain their original IDs and classification pending that review.

The manuscript supports a concrete and promising mechanism for avoiding repeated timing work. Its error guarantees require stronger interpretation than the earlier card provided. No implementation was executed here; predictor bounds, signed-error conservatism, path-budget composition, and independent signoff equivalence remain unverified. Independent comprehension review remains open.

## Measure complete savings under changing conditions

These papers motivate optimization that is explicit about when a specialized choice or cached result remains applicable. They do not demonstrate a common algorithm or integration. For neural execution, the output must retain its required numerical behavior. For timing analysis, the conclusions about whether paths meet constraints must remain trustworthy.

A strong comparison would report preparation cost, reuse opportunities, invalidations, fallback work, peak memory, and final valid outputs on previously unseen sequences. It should separate steady repeated operation from first use and change-heavy operation. The long-term question is whether adaptation and reuse reduce total work robustly, rather than improving a narrowly warmed-up case. DyTuner remains description-backed; the timing manuscript now provides a method and quantified results with the conditions and unresolved guarantees explained above. These two examples motivate a hypothesis about conditional reuse, not a measured historical trend.
