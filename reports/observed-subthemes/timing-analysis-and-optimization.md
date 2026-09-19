# Timing analysis and optimization

This subject has 2 records in the selected sample. This page explains where it fits, then presents all captured paper evidence without shortening the measurements or limitations.

[Definitions used in the paper records](../reading-guide-v1.md)

## Understand the parent subject first

- [Physical design and manufacturing](../themes/physical-design-and-manufacturing.md)

## A circuit must deliver data at the right time

Both paper records now have expanded individual explanations. Warp-STAR has selected manuscript evidence; Powerpath remains description-backed. This is writing coverage, not independent comprehension acceptance. Source recovery and original-record reconciliation remain open.

Correct logic is not enough for a clocked circuit. A receiving storage element needs its input to be stable around the clock event that captures it. Setup and hold checks describe the relevant before-and-after requirements. Timing analysis compares data arrival with the required timing, accounting for the clock paths as well as the data path. [Intel's clock-analysis equations](https://www.intel.com/content/www/us/en/support/programmable/support-resources/design-examples/quartus/tq-clock.html) show why both are necessary.

Two separate computations appear in this group. Characterization determines timing constraints for individual circuit elements under specified conditions. Static timing analysis uses such models to check paths through a larger design without simulating every input sequence. A faster path analyzer still needs trustworthy input models; faster characterization does not automatically accelerate every later design step.

## Warp-STAR: organizing irregular timing work on a GPU

[Warp-STAR](../observed-subthemes/timing-analysis-and-optimization.md#paper-dac-2026-research004) addresses load imbalance in GPU timing analysis. A circuit graph is irregular: different parts have different numbers of connections and dependencies. Assigning equal numbers of graph objects to processing groups does not necessarily assign equal amounts of work.

The proposed method coordinates work at the warp level, the GPU execution grouping named by the paper. Its claimed benefit concerns how that work is organized, not a reduction in the circuit's actual signal delay. The official description reports 2.4 times faster timing analysis than prior GPU analysis and 1.7 times faster timing-driven global placement. These are separate measured scopes, not two interchangeable versions of one speedup.

Placement performs other work besides timing analysis. Consequently, accelerating the analyzer need not accelerate the entire placement process by the same factor. The [expanded manuscript discussion](#explanation-dac-2026-research004) now supplies selected absolute times, circuit conditions and a timing-quality regression that the original description omitted. A fair evaluation still needs comparable timing conclusions and designs meeting the same constraints.

The engine also supports differentiable analysis: computing information about how an analysis objective changes as adjustable quantities change. That can guide optimization, but an available gradient does not prove that every suggested physical change is legal or improves the final routed circuit. Gradient cost, optimization convergence, and completed design quality require separate measurements.

## Powerpath: reducing the search needed for cell constraints

[Powerpath](../observed-subthemes/timing-analysis-and-optimization.md#paper-dac-2026-research025) targets sequential-constraint characterization. Finding a limiting timing condition can require repeated detailed circuit simulations as a search narrows the acceptable interval. A reliable estimate that starts the search closer to the answer can reduce that work.

The method uses a supply-current signature from an already required reference-delay simulation. “Internal-probe-free” means the proposed estimate does not require the internal probes targeted by its comparison; it does not mean no simulation or measurement information is needed. The description identifies affine lookup-table calibration and online ridge regression. In plain terms, these calibrate a relationship between observed information and the search estimate, with the regression regularized to limit unstable fitting.

The reported evaluation uses post-layout TSMC 5 nm and 12 nm libraries across five process-voltage-temperature corners. A corner specifies the conditions under which the model is evaluated. The description reports 1.5-fold acceleration with affine calibration and 3.6-fold acceleration with statistical calibration. Those results should remain attached to their respective methods, not summarized as a single universal gain.

The description calls the accuracy suitable for final design checking, but does not provide error distributions. That wording is a source claim rather than an independently established accuracy bound. Evaluation should inspect cases where interval reduction might exclude the true boundary, along with the fallback and extra simulation cost when an estimate is poor.

## The end-to-end research question

These papers address complementary parts of timing work: creating constraints and propagating timing through a design. They motivate asking how much complete design turnaround improves when both costs fall while the final acceptance criteria remain unchanged. They do not demonstrate their integration. Any combined study must count calibration, data conversion, GPU transfers, repeated optimization, and final reference checks before claiming a full-flow improvement.

### Compare the changed work and the remaining responsibility

| Question | Powerpath | Warp-STAR |
|---|---|---|
| What work is reduced? | Search needed to characterize a cell constraint | Time spent analyzing a connected timing graph |
| What information is reused? | Information from a required reference simulation | Parallel work and dependencies exposed by the graph |
| What must not be inferred from speed? | That a narrowed interval contains the true boundary | That a faster run produces better timing or equivalent analysis |
| Current evidence depth | Official description; target manuscript and artifact unrecovered | Selected manuscript methods and tables; no reproduction |

The sequence is important: a faster consumer of timing models cannot repair an incorrect constraint supplied upstream. Conversely, spending more effort on accurate characterization does not ensure that a parallel analyzer combines and propagates its inputs correctly. Each stage needs its own check, and the combined flow needs a check of the final design.

For an independent budget example, suppose characterization costs forty time units and repeated analysis sixty. Halving the first and tripling the speed of the second gives a total of forty, so overall speedup is 2.5×, not 6×. Those gains act on different portions of the budget. If the library is already characterized and reused unchanged, its preparation saving contributes nothing to that particular design run. If a new library must be built, omitting preparation would understate the actual work.

The durable hypothesis is that reducing repeated estimation work is valuable when the reused information remains valid and errors are detected before acceptance. Test it with unchanged criteria, an explicit reuse lifetime and complete recovery costs. Reject a stronger claim of field-wide progress until comparable editions and task populations support it. Two selected DAC papers establish neither deployment prevalence nor a historical trend across ISCA, DAC and ICCAD.

<span id="explanation-dac-2026-research025"></span>

## Powerpath: narrow a characterization search without losing its valid boundary

### What the available source establishes

The official description uses a supply-current signature from a required reference-delay simulation to estimate sequential constraints. It names affine calibration and online ridge regression, reporting 1.5× and 3.6× acceleration respectively on post-layout TSMC 5nm/12nm libraries across five process-voltage-temperature corners. These are separate configurations, not factors to multiply. [Official Description and Authors](https://63dac.conference-program.com/presentation/?id=RESEARCH025&sess=sess155)

Title and author searches on 2026-09-08 did not recover the target manuscript or a verified target artifact. Related characterization papers are not substitutes. The source says code and data are open, but this pass did not locate and inspect that release. No manuscript page citations, estimator equations, error distributions or fallback details are available. No circuit simulation was executed. The reasoning below is explanatory, not a reconstruction of Powerpath.

### Characterization creates a model used by later analysis

A sequential cell stores state. A flip-flop, for example, captures a data value in relation to a clock event. The physical transistors do not switch instantaneously. Input transitions close to the capture event can change the output delay or prevent the intended capture under the specified observation criterion.

Characterization evaluates the cell under controlled conditions to determine values that a larger timing analyzer can use. Setup concerns how early data must become stable before capture. Hold concerns how long it must remain stable afterward. Their numerical values depend on the cell and conditions; neither is a universal fixed interval that can be inferred from its logical function alone.

For an independent example, fix a rising clock edge at time zero and vary a data transition before it. At a separation of 40 picoseconds, the output meets the chosen criterion; at 20 picoseconds, it does not. The task is to find a boundary between these outcomes to a chosen resolution. A picosecond is one trillionth of a second. The specific boundary and criterion here are illustrative, not paper measurements.

An acceptance criterion must say what counts as success. It could involve the correct output value within an observation window or a permitted increase in clock-to-output delay. These are different questions. A method that changes the criterion can change the reported constraint even if its simulator is unchanged.

### A search interval must contain the transition of interest

For a simplified monotone search, maintain one passing endpoint and one failing endpoint. Test their midpoint and retain the half containing the transition. Starting with an interval of width 128ps, seven halvings reduce the width to 1ps. Starting with a correctly bracketed interval of width 16ps takes four halvings to reach that resolution.

A predictor can save expensive tests by supplying the narrower interval. But if the true transition is at 30ps and the predicted interval is `[40,56]`, refinement inside that interval cannot recover it. The final answer can be very precise about the wrong region. Numerical convergence is not evidence that the initial interval was valid.

Before using a narrow bracket, check its endpoints under the actual criterion. If both pass or both fail, expand or revert to a trusted search procedure. This is a proposed safeguard, not a verified feature of Powerpath. More complicated or nonmonotone behavior requires a search method appropriate to that behavior; binary-search reasoning alone does not establish it.

### The current waveform supplies information, not a direct proof

Supply current changes as internal capacitances charge and discharge and transistors conduct. A waveform records current over time. Features such as timing, shape or integrated charge may correlate with the internal events that constrain capture. An estimator can exploit such correlations without reading every internal node voltage.

However, an aggregate waveform can combine contributions from several internal events. Two internal behaviors may produce similar summaries. A selected feature can also change with supply voltage, input transition shape or loading. Predictive usefulness therefore requires calibration and validation across the conditions in which the estimate will be used.

Reusing an already required simulation can avoid an extra simulator invocation. It does not make feature extraction, fitting or failed predictions free. The complete budget must include any work needed to obtain a usable estimate and to confirm or repair the search interval.

### Calibration corrects an estimate under observed conditions

An affine correction applies a scale and offset: corrected estimate equals `a×raw estimate + b`. For an illustrative raw estimate of 20ps, scale 1.1 and offset 3ps give 25ps. The correction can remove a systematic bias in the calibration data. It does not supply a guaranteed worst-case error bound for unseen cells or conditions.

Ridge regression fits a weighted combination of features while penalizing large coefficients. The penalty can make fitting less sensitive to noisy or strongly correlated features. It still relies on the relationship between the features and the target remaining useful. Online fitting updates the model as observations arrive; early samples and later samples may consequently receive different-quality predictions.

To evaluate that procedure, record the order of samples, the information available at each prediction, and the reference outcome obtained afterward. A prediction made after seeing its own target is not a prospective estimate. Separating calibration and evaluation prevents an apparently accurate interval from relying on information unavailable when the real search starts.

### Statistical accuracy needs more than a small average error

A process-voltage-temperature corner specifies a particular operating and manufacturing condition. Statistical sampling additionally varies model parameters according to a stated distribution. Results at several corners do not by themselves establish how rare variations behave inside or beyond those conditions.

Suppose 999 estimates each have absolute error 0.1ps, but one misses by 20ps. The average absolute error is only 0.1199ps. A narrow interval of ±1ps might work well for almost every sample and still miss the exceptional boundary. If that exceptional region determines a reliability decision, the average alone is inadequate.

Useful measurements include boundary error, interval coverage, fallback frequency and cost, and the distribution of failures across cell and constraint types. The reference search also needs a stated tolerance and criterion. Calling an outcome suitable for final design checking cannot replace those measurements.

### Connect characterization speed to complete design work

For an independent cost calculation, let a baseline characterization require one reference simulation and seven search simulations, each costing one time unit. A revised method uses the same reference, four search simulations and 0.2 units of estimator work. Total time falls from eight to 5.2 units, about 1.54× faster. If a fraction of cases requires fallback, those additional simulations reduce the aggregate gain.

This is a different optimization from [Warp-STAR](#explanation-dac-2026-research004), which reorganizes graph analysis using already supplied timing models. Better characterization can improve model availability or preparation time; faster graph propagation can improve repeated design evaluation. Neither paper alone establishes the performance or accuracy of a combined flow.

The bounded hypothesis is that information already produced by a required simulation can reduce later search work when the predicted bracket is checked and the original acceptance criterion is preserved. It weakens if the useful feature requires undisclosed extra work, if rare errors escape detection, or if calibration cost dominates on new libraries. Manuscript recovery, exact feature and search definitions, validated failure handling and independent review remain open.

The correction boundary is explicit: test setup, hold and removal constraints, Monte Carlo samples, PVT coverage, 5 nm and 12 nm libraries, interval bracketing, tail errors, fallback behavior and signoff criteria separately. The 1.5× and 3.6× source claims are not evidence of reliable tail-safe sequential characterization across libraries and statistical conditions.
The evidence supports search reduction, not demonstrated reliable tail-safe sequential characterization.

<span id="explanation-dac-2026-research004"></span>

## Warp-STAR: divide timing work more evenly without changing what timing means

### What was recovered

The version-1 manuscript identifies DAC DOI `10.1145/3770743.3803891`. Selected method and evaluation text was inspected on 2026-09-08; no GPU code, analyzer or placer was executed. The current reading card includes those conditions; its disclosure preserves the original description-only fields. Original-ledger and artifact reconciliation remain open.

Warp-STAR distributes pin work across a warp, reduces shared loads, and respects timing-graph levels. It retains ordinary maximum-based arrival analysis alongside a smooth differentiable calculation; CUDA events coordinate dependent streams. [Sections 3.1–3.2](https://arxiv.org/html/2603.28381v1#S3.SS1)

Experiments use a 24-core AMD 7965WX, RTX 4090 and CUDA 11.8 with contest circuits. Table 2 gives superblue1 analyzer times 57ms for GPU-Timer, 25ms pin-based and 48ms CTE. Table 3 gives Xplace/Warp-STAR placement times 60.9/35.4 seconds, but signed TNS −21.8/−23.7 in units of 100,000ns. [Section 4 and Tables 2–3, PDF pages 5–6](https://arxiv.org/pdf/2603.28381v1#page=5)

The manuscript attributes some differences to baseline synchronization and floating-point effects; INSTA-Place results are not a fully matched local rerun. [Section 4.3 and footnote 3, PDF page 6](https://arxiv.org/pdf/2603.28381v1#page=6)

The following examples are independent teaching calculations, not reproductions of these circuits.

### A timing graph propagates arrival requirements

A pin is a connection point on a circuit element. A timing arc describes how a transition at one pin affects timing at another. A net connects a driving pin to receiving pins. An analysis graph combines these relationships with delays and timing requirements.

For an illustrative late-arrival calculation, one input arrives at 2ns and crosses an arc taking 3ns. Another arrives at 4ns and crosses an arc taking 2ns. The candidate output arrivals are five and six nanoseconds. The conservative latest arrival is six, not their sum or average. If the output is required by 5.5ns, its setup slack is −0.5ns.

Backward propagation answers a complementary question. To deliver an output by 5.5ns through a 2ns arc, the corresponding input must arrive by 3.5ns under this simplified model. Multiple downstream requirements can constrain the same upstream point. A parallel implementation must preserve both the operation being computed and the dependencies that make its inputs valid.

The earliest arrival matters for other checks, including whether new data arrives too soon after capture. Replacing every operation with a maximum would therefore not constitute a general timing analyzer. Transition direction, early/late conditions, clock relationships and exceptions must retain their distinct meanings.

### Equal numbers of nets need not mean equal work

A GPU executes groups of threads that share instruction issue. When threads in such a group have different loop lengths, some can finish their useful work while others continue. The unused execution lanes do not necessarily get reassigned to unrelated work within that same instruction.

Consider a deliberately simplified four-lane group assigned nets with one, one, one and thirteen receiving pins. If each lane processes one pin per iteration, the group requires thirteen iterations. It performs sixteen useful pin operations over fifty-two lane-iteration opportunities: about 30.8% utilization in this model.

If those sixteen pin operations can instead be divided evenly among the four lanes, they need four iterations before accounting for coordination. That is an opportunity, not a guaranteed speedup. Finding each pin's net, fetching data, combining partial results and synchronizing threads all take work. Real hardware can also schedule other groups while one waits; the four-lane example does not model an entire GPU.

For very small nets, assigning a whole group to a net may leave lanes idle. For large nets, distributing its pins can expose more parallel work. The circuit's distribution of net sizes therefore matters more than a single average pin count. A scheduling policy needs evaluation on both broad shallow graphs and narrow dependency-heavy ones.

### Shared quantities require a defined combination operation

Each receiving pin contributes load that can affect a driver's delay. A reduction combines contributions into one result. For loads 1, 2, 3 and 4, a tree reduction can first form 3 and 7, then combine them into 10. Separate partial sums avoid having every thread update the same location unsafely.

Without synchronization, two threads might both read an old sum of zero, compute their additions independently and write one and two. The final value can be two rather than three. The lost contribution is a correctness error, not an acceptable numerical approximation. More concurrency is useful only when these updates have defined ordering or a correct combination scheme.

Even a race-free parallel sum can differ slightly from a sequential floating-point sum because finite-precision addition is not associative. This is different from dropping an update. Comparisons should distinguish tolerated numerical differences from invalid dependencies, and should examine their effect on the optimization decisions made from the results.

### Graph levels restrict when parallel work can start

Levelization groups work by dependency depth. If C depends on the arrivals at A and B, it cannot use unfinished values from either. A and B may be computed concurrently if neither depends on the other. The next level begins only when its required inputs are ready.

Reusing this organization is valid only while the dependency structure remains appropriate. Moving cells can change wire delays without changing which pins connect. Rewiring or inserting a new cell can change the graph itself. An incremental flow must identify which cached information is still valid after each kind of edit.

More threads cannot eliminate a long chain of dependent calculations. They mainly exploit the work that is independent within or around those levels. Kernel launch costs and memory traffic can dominate when each level contains little useful work. This is why graph shape and repeated-analysis conditions belong beside the runtime result.

### A smooth objective is guidance, not the original maximum

Optimization may need a gradient: information about how a numerical objective changes when a design variable changes. An exact maximum assigns the local derivative to the currently largest input, except where the maximum is tied. A smooth alternative gives nearby competing inputs some influence, which can make optimization guidance less abrupt.

For an illustrative smooth maximum of two equal values five, use `5 + γ log(2)` with positive smoothing parameter γ. At γ=0.1, the result is approximately 5.0693, not five. The difference is a property of the surrogate expression. It must not silently become a new measured path delay.

Overlapping gradient calculations with ordinary timing work can reduce elapsed time when dependencies permit it. But a consumer stream must wait for the exact producer result it needs. Starting a second stream does not by itself create safe overlap, and reducing synchronization too far can use stale values.

### Judge analysis runtime and placement quality separately

Total negative slack, abbreviated TNS, aggregates violations over the chosen endpoints. With signed slacks, values closer to zero indicate less total lateness. For example, endpoint slacks −2, −1 and +4 sum to TNS −3 when only negative terms contribute. The positive margin at the third endpoint does not cancel the other violations.

A smaller magnitude of TNS can coexist with a worse single endpoint, so worst slack and the number of violating endpoints are also useful. Where a table displays negative TNS, simply saying “lower is better” is ambiguous: a more negative signed value indicates greater aggregate violation. Preserve signs and explain the convention before comparing results.

Suppose analysis consumes sixty of one hundred seconds in a placement run. Making that portion 2.4 times faster gives `40 + 60/2.4 = 65` seconds if everything else stays fixed. The full-run speedup is about 1.54, not 2.4. If faster analysis also changes how often the placer requests feedback, the algorithm's trajectory and output may change too; the fixed-work calculation no longer describes the whole comparison.

The bounded insight is that reorganizing irregular work can make timing feedback cheaper, but useful end-to-end improvement requires comparable constraints and acceptable final designs. It weakens if scheduling overhead consumes the savings, timing accuracy changes materially, or faster placement worsens required outcomes. Full artifact inspection, matched correctness checks, routed-design evaluation and independent comprehension review remain open.

## Compare the results carefully

First identify the inputs and required output quality. Then identify the limited resource: time, memory, communication, energy, circuit area, or correctness coverage. Ask which part of the method reduces that cost and which new cost it adds. Compare numbers only when the experiments hold these conditions sufficiently similar.

A conference description may explain the proposal while omitting the full experiment. An author preprint link may have been coded from its abstract. The source classification does not by itself establish that every table was read. Missing locations remain visible below.

## Complete captured evidence

These are evidence records, not substitutes for the explanations above. Each record preserves its problem, proposed method, measurements, comparison conditions, and source limits. A populated record does not establish that its mechanism has been fully explained or independently verified.

<span id="paper-dac-2026-research004"></span>

### Warp-STAR: High-Performance, Differentiable GPU-Accelerated Static Timing Analysis Through Warp-Oriented Parallel Orchestration

DAC 2026 · Record: `dac-2026-research004`

[Read the step-by-step explanation](#explanation-dac-2026-research004)

**Updated source-backed reading card**

Reviewed 2026-09-08. Reconciles the original description with selected manuscript inspection; separates analyzer runtime, placement runtime and signed timing quality.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Uneven pin workloads within GPU timing analysis and added gradient-computation cost.

**Mechanism / artifact:**

Pin-based warp scheduling, shared-load reductions and dependency levels; ordinary maximum-based timing alongside smooth differentiable analysis, coordinated with CUDA events. CTE scheduling is a separate variant.

**Workload — the work tested:**

ICCAD 2015/2025 contest circuits; Table 1 lists AES and eight superblue designs. Xplace3.0-based global placement integration.

**Hardware and manufacturing assumptions:**

24-core AMD 7965WX, RTX 4090, CUDA 11.8; not measured fabricated-circuit speed.

**Baseline — the comparison method:**

OpenTimer, GPU-Timer and placement frameworks. INSTA-Place comparison is not a fully matched local rerun.

**Reported measurements:**

Superblue1: analyzer GPU-Timer/pin-based/CTE 57/25/48ms. Placement Xplace/Warp-STAR 60.9/35.4s; signed TNS -21.8/-23.7 in 100,000ns units. Faster runtime coexists with worse signed TNS.

**Limits on the conclusion:**

Selected manuscript text only; no execution. Baseline synchronization, floating-point variation, matched accuracy and routed-design quality require verification. Independent acceptance pending.

**Source and location**

Evidence tier: DAC identified manuscript v1; selected method/evaluation reading, not reproduction. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://arxiv.org/pdf/2603.28381v1)

Sections 3.1–3.2; Section 4/Table 2 PDF page 5; Table 3, Section 4.3 and footnote 3 page 6. DAC DOI 10.1145/3770743.3803891.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** previous state-of-the-art GPU-based STA

state-of-the-art timing-driven global placement frameworks

**Evidence locators:** Not established in the captured evidence.

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH004&sess=sess155

**Hardware or process assumptions:** Not established in the captured evidence.

**Limits:** The public description does not expose full circuit suites, absolute runtime, quality tradeoffs, or transfer limits.

**Method or artifact:** Warp-level parallel orchestration for a differentiable GPU-accelerated static timing analysis engine.

**Metrics:** 2.4X STA speedup

1.7X placement-flow speedup

minimal overhead for differentiable gradient analysis

**Problem:** GPU static timing analysis suffers from intra-warp load imbalance on irregular circuit graphs, limiting timing-analysis and placement-flow throughput.

**Workload or benchmark:** Static timing analysis on irregular circuit graphs; integration into timing-driven global placement; differentiable gradient analysis.

</details>

<span id="paper-dac-2026-research025"></span>

### Powerpath: Internal-Probe-Free Search Interval Reduction for Efficient Statistical Sequential Constraint Characterization

DAC 2026 · Record: `dac-2026-research025`

[Read the step-by-step explanation](#explanation-dac-2026-research025)

**Updated source-backed reading card**

Reviewed 2026-09-09. Deepens the Powerpath treatment into a paper-level reading; separates the supply-current signature, affine calibration and online ridge-regression interval reduction from bracket validity, tail error, rare-corner coverage, fallback cost and signoff acceptance, while preserving the 1.5x/3.6x, five-PVT-corner and TSMC 5/12 nm source claims.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Sequential-constraint characterization can consume most of library signoff runtime, while path-based methods depend on internal observability and extra simulations and may not handle toggle-unexpected hold/removal arcs reliably.

**Mechanism / artifact:**

Powerpath estimates constraints from a physics-grounded supply-current signature extracted from a mandatory reference-delay simulation, uses affine lookup-table calibration for nominal characterization, and uses online ridge regression to tighten search intervals across statistical Monte Carlo samples. Feature definition, regression inputs, interval policy, fallback and acceptance criterion are unspecified.

**Workload — the work tested:**

Post-layout TSMC 5 nm and 12 nm standard-cell libraries across five PVT corners for sequential constraint characterization, including setup/hold/removal/toggle-unexpected arc classes; cell count, library contents, Monte Carlo distributions/sample counts, voltage/temperature values, SPICE settings and baseline search tolerances are unspecified.

**Hardware and manufacturing assumptions:**

Post-layout standard-cell/SPICE characterization flow with supply-current waveform access and a mandatory reference-delay simulation; PDK/library versions, parasitics, simulator, waveform sampling, compute hardware, license/runtime accounting, process variation model and signoff tool are unspecified.

**Baseline — the comparison method:**

Traditional path-based sequential-constraint characterization

Same reference simulation, acceptance criterion, search resolution, SPICE settings, cells/arcs, PVT/Monte Carlo samples, fallback policy and total runtime boundary are unspecified

**Reported measurements:**

The source reports up to 80% of signoff runtime addressed, 1.5x speedup with affine calibration and 3.6x with statistical calibration across post-layout TSMC 5 nm/12 nm libraries and five PVT corners, while claiming signoff-grade accuracy; it provides no absolute runtime, boundary-error distribution, interval coverage, tail/rare-case error, fallback frequency/cost, sample counts or independent signoff comparison.

**Limits on the conclusion:**

A narrower search interval is useful only if it contains the true constraint boundary under the same acceptance criterion. Validate both endpoints, expand or fall back when they do not bracket the transition, and test nonmonotone behavior, hold/removal arcs, rare process samples, waveform noise and calibration extrapolation; average error cannot hide a missed signoff-critical tail.

Internal-probe-free means the estimator reuses information from a required reference simulation; it does not mean zero simulation, measurement or feature-extraction cost. Account for reference simulation, waveform processing, calibration/online regression, Monte Carlo updates, retries, fallback searches and model transfer to new libraries/corners.

The 1.5x/3.6x and signoff-grade claims are description-backed and do not establish universal accuracy, coverage or signoff acceptance. The evidence supports supply-current-informed search reduction, not demonstrated reliable tail-safe sequential characterization across libraries, processes and statistical conditions.

**Source and location**

Evidence tier: Primary captured official DAC description plus existing authored timing characterization discussion; no full paper extraction, reproduced spice campaign or independent signoff acceptance. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH025)

DAC 2026 official description; existing timing-analysis-and-optimization editorial explanation; captured Problem, Mechanism / artifact, Workload, Hardware, Baseline, Measurements and Limits fields; no manuscript pages, estimator equations, error distributions, fallback trace or independent signoff validation.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** high_official_description

**Baselines:** traditional path-based characterization methods

**Evidence locators:** Not established in the captured evidence.

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH025&sess=sess155

**Hardware or process assumptions:** Not established in the captured evidence.

**Limits:** The description does not expose absolute runtime, error distributions, or whether the reported libraries represent broader process technologies.

**Method or artifact:** Internal-probe-free supply-current estimation with affine calibration and online ridge-regression interval tightening.

**Metrics:** up to 80% of signoff runtime addressed

1.5X speedup with affine calibration

3.6X speedup with statistical calibration

signoff-grade accuracy

**Problem:** Sequential-constraint characterization consumes substantial signoff runtime and traditional path-based approaches fail for toggle-unexpected arcs or require extra SPICE simulations.

**Workload or benchmark:** Post-layout TSMC 5 nm and 12 nm libraries across five process-voltage-temperature corners; sequential constraint characterization.

</details>

## What remains to establish

Resolve unspecified workloads, comparison methods, resource budgets, and source locations before generalizing a reported gain. Multiple papers in this selected sample permit comparison of mechanisms, but do not by themselves establish recurrence across years or a long-term trend.

[All subthemes](../expanded-taxonomy-v1.md) · [Research directions](../directions/README.md)
