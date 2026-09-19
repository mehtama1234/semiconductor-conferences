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
