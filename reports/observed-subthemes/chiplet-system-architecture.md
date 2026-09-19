# Chiplet system architecture

This subject has 3 records in the selected sample. This page explains where it fits, then presents all captured paper evidence without shortening the measurements or limitations.

[Definitions used in the paper records](../reading-guide-v1.md)

## Understand the parent subject first

- [Chiplets 3d and packaging](../themes/chiplets-3d-and-packaging.md)

## Splitting a system changes both computation and communication

A chiplet is a separately manufactured die that participates in a larger system. A package connects dies to one another and to the rest of the machine. In a 2.5D arrangement, dies sit alongside one another on an interconnection structure rather than all computation being fabricated on one continuous die.

The design question is not simply how many chiplets to use. It is which work belongs on each die, what information must cross die boundaries, and whether the resulting connections meet timing and capacity requirements. Moving a function can reduce its local cost while increasing transfer time or creating a new bottleneck elsewhere.

The three papers in this group operate at different decision levels. DUET chooses phase-specific packages for language-model inference. ChiPlanner joins circuit partitioning with early physical and timing estimates. ChiSER accelerates the search among neural-network accelerator designs. They illustrate related design dependencies, not interchangeable tools or a controlled comparison.

## DUET: give different inference phases different hardware

Prefill processes the supplied prompt. Decode then generates additional tokens, with each new step depending on earlier output. A token is a unit of the model's text representation. Processing many prompt positions together can expose more parallel arithmetic and reuse than processing one new position at a time. Whether computation or memory limits performance still depends on model, batch size, and hardware; the phase name alone does not prove the bottleneck.

A hybrid Mamba–Transformer model contains both attention operations and state updates. A state update carries a numerical summary forward through the sequence. Attention instead uses information associated with earlier positions. Hardware intended for a hybrid model must accommodate these different operations without making the less convenient ones dominate execution time.

[DUET](../observed-subthemes/chiplet-system-architecture.md#paper-dac-2026-research3120) assigns configurable systolic arrays and off-package memory to prefill, and vector arrays with in-package high-bandwidth memory to decode. Section 4.1, PDF page 4, uses simulation and 28-nm synthesis. Section 4.3, page 5, models the B200 baseline as two homogeneous GPUs with assumed internal compute geometry, not measured B200 serving. Table 3 gives different memory resources across configurations.

Section 4.4 and Table 4, pages 5–6, report about 4× lower time to first token, 1.4× higher throughput, and 1.5× lower time between tokens against that baseline. The study assumes matched phase throughput without explicit multi-request scheduling. Section 4.5 estimates chiplet area by scaling components to 7 nm; it does not demonstrate a manufactured package. Table 4's 1.2× token-interval ratio against the decode-friendly design also differs from the nearby prose's 1.1×. [DUET version-1 manuscript, Sections 4.1–4.5](https://arxiv.org/pdf/2603.15530v1).

The authors provide an architecture simulator and a numerical-comparison path. Its documented performance counters include architectural steps and configurable estimates of clock cycles. Those counters require validation before being treated as measured processor time; the repository has not been executed in this audit. [Author simulator and metric definitions](https://github.com/AlishKanani/DUET).

Splitting phases adds a handoff: state produced by prefill must reach the decode resources before it can be used. For a real serving assessment, count that transfer, queueing, and idle capacity under changing request lengths. Faster token generation and shorter initial response time are separate outcomes; neither establishes the other.

<span id="explanation-dac-2026-research3120"></span>

### DUET: phase-specific packages must be evaluated across the full prefill-to-decode handoff

### Why one accelerator sees two different workloads

LLM serving has a prompt-processing phase called prefill and a token-generation phase called decode. Prefill processes many prompt positions together, so matrix multiplication and long-sequence operations can expose substantial parallel work. Decode produces one or a small number of new tokens at a time. It repeatedly reads model weights and the accumulated key/value state, so memory bandwidth, data reuse and access latency can dominate.

Hybrid Mamba–Transformer models add two different operator patterns. Mamba-style state-space layers update a recurrent state and include element-wise operations; attention layers use information associated with earlier positions and often stress key/value memory. A hardware organization that is efficient for large matrix multiplication can be poorly matched to vector–matrix or state-update work. DUET treats this mismatch as an architecture problem rather than assuming one homogeneous package is equally efficient in both phases.

### What the two packages do

The Prefill package uses systolic-array chiplets and off-package memory. A systolic array reuses data across a regular grid of multiply-accumulate units, which matches large matrix multiplications and the long-sequence work described for prefill. The Decode package uses vector-unit arrays with high-bandwidth in-package memory. Vector units support element-wise and vector–matrix operations, while nearby high-bandwidth memory reduces the distance and transfer cost for repeatedly accessed decode state.

Both packages are described as runtime-configurable so that a hybrid model can mix Mamba and attention layers. Runtime configurability changes the mapping of work to available units; it does not eliminate the need to move state between packages or resolve contention when several requests enter different phases at once. The system must also decide how much memory capacity and bandwidth each phase receives under changing sequence lengths and batch sizes.

### What the reported evaluation means

The manuscript evaluation uses Nemotron-H-56B, Zamba2-7B and Llama3-8B across four workloads. It reports approximately 4× faster time to first token, 1.4× higher throughput and 1.5× lower time between tokens than the modeled B200 baseline. Time to first token mainly reflects prompt processing and startup; time between tokens reflects decode cadence; throughput depends on request mix and scheduling. These metrics are related but cannot be multiplied into one overall speedup.

The B200 comparison is a modeled baseline using assumed internal compute geometry, not a measurement of B200 serving. The study uses simulation and 28-nm synthesis, while one area estimate scales components to 7 nm. Those results can support architectural projections under the stated assumptions, but they do not establish a fabricated chiplet package, production power, or measured B200 parity. The source also reports a nearby discrepancy: Table 4 gives a 1.2× token-interval ratio against the decode-friendly design while nearby prose says 1.1×. That should remain visible until reconciled.

### The evaluation that would establish system-level value

Report package topology, die-to-die bandwidth and latency, memory capacity, precision, power, area, process assumptions and the cost of transferring prefill state into decode memory. Evaluate dynamic multi-request scheduling with varying prompt lengths, generated lengths, batch sizes, phase imbalance and queueing. Report time to first token, time between tokens, end-to-end latency, throughput, energy per token, utilization and transfer overhead separately. Compare against measured or fully specified matched baselines, and publish the simulator configuration and counter definitions so architectural cycle estimates can be checked.

The [DUET](../observed-subthemes/chiplet-system-architecture.md#paper-dac-2026-research3120) record describes phase-specific systolic/off-package-memory and vector/in-package-memory packages for hybrid Mamba–Transformer inference. The detailed explanation above separates prefill from decode, operator type from memory placement, phase metrics from one combined speedup, simulator estimates from measured hardware, and package specialization from the required state handoff; this card is the compact evidence record.

## ChiPlanner: partition with an estimate of the physical consequences

Partitioning decides which circuit elements belong on each die. Placement decides where those elements and dies go. A connection crossing a die boundary needs a different physical path and interface from a short local wire. If partitioning ignores that distinction, a low connection count can still produce unacceptable delays on important paths.

[ChiPlanner](../observed-subthemes/chiplet-system-architecture.md#paper-dac-2026-research380) uses approximate placement before partitioning to estimate later timing, models inter-chiplet delay, and applies parallel connection weighting during timing-driven planning. It also uses Bayesian optimization to explore manufacturing-cost and timing trade-offs. This search method builds a predictive model to select further candidates; it is not a proof that the entire design space has been optimized.

The official description reports average improvements of 42.4% in total negative slack and 16.8% in worst negative slack for downstream design tools. It does not expose benchmark configurations, absolute timing, cost-model calibration, or the normalization used for those percentages. [Official ChiPlanner description](https://63dac.conference-program.com/presentation/?id=RESEARCH380&sess=sess114).

Slack is the required arrival time minus the actual arrival time. Negative slack means a timing requirement is violated. Worst negative slack describes the most severe violation; total negative slack aggregates violations under the tool's reporting rules. Improving either does not establish that all requirements are met. For example, changing worst slack from −100 ps to −80 ps improves the violation but leaves a failing path.

The decisive comparison should therefore report both early predictions and final routed timing, including new interface and routing costs. It should also show whether fewer design iterations were actually needed, rather than inferring that outcome from an improved timing score.

<span id="explanation-dac-2026-research380"></span>

### ChiPlanner: partitioning is only useful when its early physical estimate survives implementation

### What the planning problem is

Chiplet planning assigns circuit logic to dies, chooses relationships among dies, and anticipates the physical paths that will connect them. A connection that crosses a chiplet boundary is not equivalent to a local wire: it uses an interface, travels through package-level structures and may have different delay, power and capacity. A partition with fewer crossing nets can still be worse if those crossings lie on timing-critical paths or are concentrated in one constrained region.

Timing closure means that required paths meet their arrival limits after synthesis, placement, routing and parasitic analysis. Early planning occurs before all of those details exist. ChiPlanner therefore uses approximate placement before partitioning to estimate the timing consequences of possible chiplet arrangements. The estimate is meant to improve the starting point for later tools and reduce the amount of correction required through engineering-change orders (ECOs) and architectural iterations.

### What ChiPlanner adds

The captured description identifies three connected mechanisms. First, approximate placement predicts post-chiplet-placement timing before the partition is finalized. Second, the planner models inter-chiplet delay and uses parallel net weighting during timing-driven physical planning. Net weighting changes the importance assigned to connections during optimization; the parallel strategy is intended to account for several related connections rather than treating each in isolation.

Third, Bayesian optimization explores the trade-off between chiplet manufacturing cost and system timing. Bayesian optimization builds a model of the objective from previously evaluated candidates and uses that model to choose promising next candidates. It can reduce the number of expensive evaluations, but it does not prove that the best design was found. Its result depends on the candidate space, objective normalization, initial samples, evaluation noise and stopping budget.

The mechanism is therefore a flow-level feedback loop: approximate physical information influences partitioning, inter-chiplet delay influences timing-driven planning, and a search procedure explores cost/timing choices. Each estimate can still be wrong. The final design must be routed and timed with the actual package, interface capacity, parasitics, congestion and manufacturing constraints.

### How to read the reported slack changes

The official description reports average improvements of 42.4% in total negative slack and 16.8% in worst negative slack for downstream chiplet design tools. TNS aggregates timing violations; WNS records the most severe violation. A percentage reduction needs the absolute baseline values, sign convention, endpoint set, timing corners and aggregation rule. An improvement can reduce a violation while leaving the design failing, and TNS and WNS can move differently when one path improves but many smaller violations remain.

The description does not provide benchmark configurations, absolute timing, package or process parameters, wirelength, congestion, thermal behavior, yield, runtime or ECO counts. The reported slack improvements therefore support the direction of physically aware early planning under the authors' conditions, not a universal timing-closure or manufacturing-cost result.

### The evaluation that would establish planning value

Report netlists, chiplet counts and boundaries, package/interposer geometry, interface capacity, delay and parasitic models, timing corners, manufacturing-cost model, Bayesian search budget and downstream tool settings. Compare early predicted timing with post-route timing for each candidate. Give absolute WNS/TNS, violating endpoints, wirelength, congestion, power, thermal limits, yield assumptions, runtime and ECO/repair count. Show the cost/timing Pareto frontier and test whether the planner reduces total design effort rather than only improving a selected timing score.

The [ChiPlanner](../observed-subthemes/chiplet-system-architecture.md#paper-dac-2026-research380) record describes approximate-placement-guided partitioning, inter-chiplet delay modeling, parallel net weighting and Bayesian cost/timing exploration. The detailed explanation above separates early prediction from final physical timing, connection count from critical-path cost, Bayesian search from global optimality, and TNS/WNS changes from timing closure and ECO evidence; this card is the compact evidence record.

## ChiSER: search quickly, then check promising designs more carefully

A detailed evaluator can make a large design search prohibitively slow. A surrogate is a cheaper model trained or fitted to approximate an expensive evaluation. Its usefulness depends not only on average prediction error but also on whether it orders promising candidates correctly and respects the constraints used to select them.

[ChiSER](../observed-subthemes/chiplet-system-architecture.md#paper-dac-2026-research399) uses a compact architecture-aware predictor of intra-core cost to guide global exploration, then rechecks top candidates with a reference model. Its official description emphasizes energy-related features for convolutional and matrix-multiplication-like workloads. It reports up to 62% and 44% reductions in a manufacturing-weighted energy–delay objective on ResNet-50 and a Transformer, respectively. The objective's exact formula, reference configurations, search cost, held-out errors, and manufacturing assumptions are not supplied. [Official ChiSER description](https://63dac.conference-program.com/presentation/?id=RESEARCH399&sess=sess318).

A reduction in a combined objective does not establish the same reduction in every component. Energy can decrease while delay increases, depending on the formula and constraints. Manufacturing weights can also change which candidate is preferred. Report energy, latency, cost, and feasibility separately so the reader can see the actual trade-off.

<span id="explanation-dac-2026-research399"></span>

### ChiSER: a surrogate can accelerate search only if it preserves the ordering of useful designs

### Why accelerator exploration has two fidelity levels

Chiplet-based DNN accelerator design chooses several coupled variables: which operations or data belong on each chiplet, how resources are divided, how data moves between chiplets, and how each chiplet's internal compute structures are configured. A detailed evaluator can estimate energy and delay for a candidate but may be too slow to run for every point in the search space. A fast system-level estimator can evaluate more candidates but may blur intra-core effects that dominate energy.

ChiSER addresses this speed–fidelity gap with a coarse-to-fine flow. A compact architecture-aware surrogate predicts an intra-core cost from a candidate's features during global exploration. The most promising candidates are then evaluated again with a reference model. The surrogate is therefore a search guide, not the final measurement authority.

### What the surrogate must preserve

The search does not require the surrogate to predict every energy or delay value exactly if it reliably ranks candidates: designs predicted to be better should usually remain better under the reference model. This ranking property can fail even when average prediction error is small. An error concentrated near a design constraint or near the best candidates can cause the search to discard the actual best design.

The source describes an energy-focused feature space and a lightweight predictor for convolutional and GEMM-like workloads. The features must represent enough of the architecture to capture intra-core cost while remaining cheap to compute. If the feature space omits chiplet communication, memory behavior, data reuse, sparsity, precision or resource contention, the predictor can rank a design well in one regime and incorrectly in another. The official description does not expose the feature list, training split, error distribution or search policy.

Rechecking only the top candidates is efficient but creates selection bias. A candidate never selected by the surrogate is never corrected by the reference model, so a systematic surrogate error can remove an entire region of the design space before the expensive evaluator sees it. A robust audit needs held-out candidates, repeated searches, reference checks outside the selected set and an accounting of all surrogate and reference evaluations.

### What the reported objective means

The captured description reports reductions of up to 62% on ResNet-50 and 44% on a Transformer in a manufacturing-weighted energy–delay objective. This is a combined score, not a claim that energy, delay and manufacturing cost each fall by the same percentage. The weight assigned to manufacturing cost can change which design wins, and a lower weighted objective can contain an increase in one component that the weighting accepts.

The source does not provide the objective formula, weights, reference configurations, search budget, communication measurements, PPA values, held-out surrogate error or generalization conditions. The “up to” values identify selected best cases, not typical improvements. The result supports a surrogate-guided exploration direction under the stated workload and objective, not a general accelerator or chiplet efficiency result.

### The evaluation that would establish exploration value

Report the full design variables, feature construction cost, surrogate training data and split, search policy, reference-evaluation budget, candidate count and random seeds. Measure value prediction error and ranking quality separately, including top-k recall and regret against exhaustive or large-budget reference search. Report energy, latency, communication, area, manufacturing cost and feasibility separately for selected and rejected candidates. Test unseen architectures, chiplet counts, mappings, dataflows, workloads and precision settings, and include the cost of retraining or updating the surrogate.

The [ChiSER](../observed-subthemes/chiplet-system-architecture.md#paper-dac-2026-research399) record describes a compact architecture-aware intra-core-cost surrogate followed by reference-model checks for chiplet DNN accelerator exploration. The detailed explanation above separates search guidance from final evaluation, value error from ranking quality, selected-candidate validation from search coverage, and the weighted objective from its individual energy/delay/cost components; this card is the compact evidence record.

Rechecking selected candidates catches some prediction failures but cannot reveal every good design excluded earlier by a poor prediction. A useful search audit includes the final reference-checked result, total evaluation budget, and comparisons over repeated searches. It should test unfamiliar architectures and workloads, not only small variations of training examples.

## What can be inferred across the three papers

The common methodological lesson is that system partitioning cannot be assessed independently of physical timing, memory, and workload mapping. This is an inference from the mechanisms, not evidence that the tools compose into a validated flow or that chiplets always reduce cost.

A joint experiment would hold the workload and service requirements explicit, use a shared package and technology model, and carry each selected design through detailed evaluation. Manufacturing yield, interface power, thermal constraints, and runtime scheduling must remain visible rather than disappearing into a single score.

The refreshed sources were inspected on 2026-09-07. DUET's page-backed evaluation and the newly recovered ChiPlanner/ChiSER numerical descriptions supersede missing-result statements in the historical cards below. Full ChiPlanner and ChiSER manuscripts, DUET final-version reconciliation, and independent experimental verification remain open. These cases do not establish a longitudinal adoption trend.

## Compare the results carefully

First identify the inputs and required output quality. Then identify the limited resource: time, memory, communication, energy, circuit area, or correctness coverage. Ask which part of the method reduces that cost and which new cost it adds. Compare numbers only when the experiments hold these conditions sufficiently similar.

A conference description may explain the proposal while omitting the full experiment. An author preprint link may have been coded from its abstract. The source classification does not by itself establish that every table was read. Missing locations remain visible below.

## Complete captured evidence

These are evidence records, not substitutes for the explanations above. Each record preserves its problem, proposed method, measurements, comparison conditions, and source limits. A populated record does not establish that its mechanism has been fully explained or independently verified.

<span id="paper-dac-2026-research3120"></span>

### DUET: Disaggregated Hybrid Mamba-Transformer LLMs with Prefill and Decode-Specific Packages

DAC 2026 · Record: `dac-2026-research3120`

[Read the step-by-step explanation](#explanation-dac-2026-research3120)

**Updated source-backed reading card**

Reviewed 2026-09-08. Reconciles the DUET card with the captured official description and inspected manuscript; explains phase-specific LLM packaging from first principles and separates prefill/decode behavior, memory placement, handoff cost, phase metrics, modeled B200 assumptions and simulator evidence.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Hybrid Mamba–Transformer inference has compute-heavy prefill and memory/latency-sensitive decode phases, while SSM recurrences and element-wise operations do not map uniformly to a homogeneous accelerator.

**Mechanism / artifact:**

Disaggregated accelerator with systolic-array chiplets and off-package memory for prefill, vector-unit arrays with high-bandwidth in-package memory for decode, and runtime configurability for mixed Mamba and attention layers.

**Workload — the work tested:**

Nemotron-H-56B, Zamba2-7B and Llama3-8B across four workloads; request lengths, batch/scheduling policy, phase imbalance, precision and transfer traces are incompletely specified.

**Hardware and manufacturing assumptions:**

Multi-package/chiplet accelerator; evaluation uses simulation and 28-nm synthesis with a 7-nm-scaled area estimate, modeled memory resources and assumed B200 internal geometry; package topology, die-to-die links, cooling, power and fabricated status are unspecified.

**Baseline — the comparison method:**

Modeled B200 GPU baseline

Decode-friendly design comparison

Baseline internal geometry, memory resources, scheduling and transfer accounting are not fully matched

**Reported measurements:**

The inspected manuscript/official record reports approximately 4x lower time to first token, 1.4x higher throughput and 1.5x lower time between tokens versus the modeled B200 baseline; Table 4 also reports a 1.2x token-interval ratio against a decode-friendly design while nearby prose says 1.1x. Metric boundaries, aggregation and discrepancy reconciliation remain explicit.

**Limits on the conclusion:**

Time to first token, time between tokens and throughput are distinct serving measures; they cannot be multiplied into one overall gain and depend on request mix and scheduling.

Phase specialization adds a handoff for state from prefill to decode and can create queueing, idle capacity or memory-capacity imbalance; the reported headline ratios do not expose those costs.

Simulation, 28-nm synthesis and 7-nm area scaling support architectural projection but do not establish a fabricated package, measured B200 parity, production power or thermal behavior.

The source supplies no complete package topology, link costs, multi-request scheduling, transfer accounting or independent execution; the author simulator's cycle estimates remain unvalidated in this audit.

**Source and location**

Evidence tier: Primary manuscript plus captured official DAC description; no fabricated package measurement, b200 serving measurement or independent simulator execution. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://arxiv.org/pdf/2603.15530v1)

DUET version-1 manuscript Sections 4.1–4.5, PDF pages 4–6, plus DAC 2026 official record and data/review-packets/dac-2026-research3120.json: phase asymmetry; Prefill systolic/off-package-memory package; Decode vector/in-package-HBM package; runtime configurability; Nemotron-H/Zamba2/Llama3 evaluation; modeled B200 comparison; Table 4 ratios and 1.1x/1.2x discrepancy.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** monolithic Transformer accelerator

shared prefill/decode package

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH3120

**Hardware or process assumptions:** Multi-package accelerator or chiplet system; bandwidth, memory, thermal, and process assumptions are unspecified.

**Limits:** No latency, throughput, energy, area, package, or model results are reported.

Disaggregation can add communication and scheduling overhead.

Official description only; package claims require system measurements.

**Method or artifact:** Disaggregated hybrid Mamba-Transformer design with phase-specific packages.

**Metrics:** Phase-specific LLM efficiency is claimed qualitatively

**Problem:** Prefill and decode have different memory and compute behavior, while hybrid sequence models complicate efficient packaging.

**Workload or benchmark:** LLM prefill/decode workloads; model mix, package topology, and baselines are unspecified.

</details>

<span id="paper-dac-2026-research380"></span>

### Chiplanner: Physically-Aware and Timing-Driven Design Planner for 2.5D Multi-Chiplet Systems

DAC 2026 · Record: `dac-2026-research380`

[Read the step-by-step explanation](#explanation-dac-2026-research380)

**Updated source-backed reading card**

Reviewed 2026-09-08. Reconciles the ChiPlanner card with the captured official description; explains physically aware chiplet planning from first principles and separates early placement estimates, inter-chiplet delay, Bayesian search, TNS/WNS interpretation, final timing closure and missing package evidence.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

2.5D multi-chiplet planning must jointly handle partitioning, physical placement, inter-chiplet delay, package constraints and timing closure before detailed implementation is available.

**Mechanism / artifact:**

Early-stage planner using approximate placement before partitioning, inter-chiplet delay modeling, parallel net weighting in timing-driven physical planning and Bayesian optimization over manufacturing-cost/timing trade-offs.

**Workload — the work tested:**

2.5D multi-chiplet designs; netlists, chiplet counts, package geometry, interface topology, timing corners, benchmark identities and downstream-tool settings are unspecified.

**Hardware and manufacturing assumptions:**

Interposer-based 2.5D package with chiplet links; process, interconnect capacity, parasitic extraction, routing, thermal model, manufacturing-cost model and yield assumptions are unspecified.

**Baseline — the comparison method:**

Geometry-oblivious chiplet planning

Single-die physical planning

Downstream chiplet design tools

Resource, constraint, timing-flow and search-budget parity are unspecified

**Reported measurements:**

The official description reports average 42.4% TNS improvement and 16.8% WNS improvement for downstream chiplet design tools; absolute slack, sign convention, endpoint set, timing corners, aggregation and ECO count are unspecified.

**Limits on the conclusion:**

Approximate placement can guide partitioning without accurately predicting post-route timing if inter-chiplet parasitics, congestion, interface capacity or later synthesis changes are missing.

Bayesian optimization selects candidates using a learned search model; it reduces evaluated candidates only under the stated objective, candidate space and budget and does not prove global optimality.

TNS/WNS improvements can reduce violations without achieving timing closure; absolute slack, violating endpoints and signoff corners are required.

The official description supplies no benchmark configurations, wirelength, congestion, thermal, yield, runtime, cost calibration or ECO values; no universal physical-planning or manufacturing-cost result follows.

**Source and location**

Evidence tier: Primary captured official DAC description only; no full paper extraction, package flow reproduction or independent routed/signoff/eco validation. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH380&sess=sess114)

DAC 2026 official description and data/review-packets/dac-2026-research380.json: early approximate placement before partitioning; post-chiplet-placement timing estimate; inter-chiplet delay; parallel net weighting; Bayesian manufacturing-cost/timing exploration; reported average 42.4% TNS and 16.8% WNS improvements.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** geometry-oblivious chiplet planning

single-die physical planning

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH380

**Hardware or process assumptions:** Interposer-based 2.5D package with chiplet links; process, thermal, and routing assumptions are unspecified.

**Limits:** No timing, wirelength, congestion, thermal, yield, or runtime values are reported.

Planner results may depend on package-specific models.

Official description only; cross-layer planning requires reproducible benchmarks.

**Method or artifact:** Physical and timing-aware 2.5D chiplet design planner.

**Metrics:** Timing and physical-planning quality are claimed qualitatively

**Problem:** Multi-chiplet planning must jointly address placement, timing, package geometry, and inter-chiplet links.

**Workload or benchmark:** 2.5D multi-chiplet designs; package constraints, netlists, timing model, and baselines are unspecified.

</details>

<span id="paper-dac-2026-research399"></span>

### ChiSER: Surrogate-Enhanced Resource-Aware Exploration of Chiplet-Based Deep Neural Network Accelerators

DAC 2026 · Record: `dac-2026-research399`

[Read the step-by-step explanation](#explanation-dac-2026-research399)

**Updated source-backed reading card**

Reviewed 2026-09-08. Reconciles the ChiSER card with the captured official description; explains surrogate-guided accelerator exploration from first principles and separates intra-core prediction, ranking quality, selected-candidate validation, search coverage and the manufacturing-weighted energy–delay objective.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Chiplet DNN accelerator exploration jointly spans partitioning, placement, dataflow and microarchitecture, while detailed intra-core energy/delay evaluation is too slow for exhaustive search.

**Mechanism / artifact:**

Coarse-to-fine flow using a compact architecture-aware surrogate of intra-core cost to guide global exploration, followed by reference-model checks on top candidates and an energy-focused feature space for convolutional and GEMM-like workloads.

**Workload — the work tested:**

ResNet-50 and a Transformer; architecture designs, chiplet counts, mappings, dataflows, precision, candidate space, reference split and search budget are unspecified.

**Hardware and manufacturing assumptions:**

Chiplet-based DNN accelerator with inter-chiplet communication and resource constraints; package, process, memory, network, PPA, manufacturing-cost and thermal assumptions are unspecified.

**Baseline — the comparison method:**

Exhaustive design-space search

Non-surrogate heuristic exploration

Reference-model budget, objective weights and comparison parity are unspecified

**Reported measurements:**

The official description reports up to 62% reduction in a manufacturing-weighted energy–delay objective on ResNet-50 and up to 44% on a Transformer; objective formula, weights, component values, aggregation and selected-case mapping are unspecified.

**Limits on the conclusion:**

A surrogate can have low average value error while mis-ranking the best candidates; top-k recall, regret and search coverage are needed to establish exploration quality.

Rechecking only selected candidates cannot recover a good design discarded by surrogate error, so reference checks on the selected set are not exhaustive validation.

A weighted energy–delay objective can improve while one component worsens; manufacturing weights can change the preferred design and do not establish separate energy, latency, area or cost reductions.

The official description supplies no feature list, held-out error, search cost, communication/PPA values, candidate count, unseen-architecture test or independent execution; no general chiplet-accelerator efficiency claim follows.

**Source and location**

Evidence tier: Primary captured official DAC description only; no full paper extraction, surrogate reproduction or independent exhaustive/reference search validation. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH399&sess=sess110)

DAC 2026 official description and data/review-packets/dac-2026-research399.json: chiplet DNN exploration speed/fidelity gap; intra-core-cost surrogate; energy-focused features; convolutional/GEMM-like workloads; top-candidate reference checks; up-to-62% ResNet-50 and 44% Transformer manufacturing-weighted energy–delay reductions.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** exhaustive design-space search

non-surrogate heuristic exploration

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH399

**Hardware or process assumptions:** Chiplet-based DNN accelerator with inter-chiplet communication and resource constraints; package and process assumptions are unspecified.

**Limits:** No search cost, PPA, communication, generalization, or workload results are reported.

Surrogate error can mis-rank designs under distribution shift.

Official description only; exploration claims require held-out validation.

**Method or artifact:** Surrogate-enhanced resource-aware design-space exploration for chiplet DNN accelerators.

**Metrics:** Exploration efficiency and accelerator quality are claimed qualitatively

**Problem:** Chiplet accelerator design spaces combine partitioning, resources, communication, and workload mapping, making exhaustive exploration expensive.

**Workload or benchmark:** Chiplet DNN accelerator designs; surrogate features, search policy, workloads, and baselines are unspecified.

</details>

## What remains to establish

Resolve unspecified workloads, comparison methods, resource budgets, and source locations before generalizing a reported gain. Multiple papers in this selected sample permit comparison of mechanisms, but do not by themselves establish recurrence across years or a long-term trend.

[All subthemes](../expanded-taxonomy-v1.md) · [Research directions](../directions/README.md)
