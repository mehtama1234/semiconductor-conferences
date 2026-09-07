# Where the field may be heading — mechanisms and testable hypotheses

Assessment date: 2026-09-06. Status: provisional researcher synthesis; independent
review pending. This is a reading of the collected evidence, not a measured
growth trend, adoption forecast, or prediction of commercial winners.

## The central interpretation

The selected papers suggest an important research question: **how much of a
system's constraints can be made explicit while choosing its algorithm,
architecture, mapping and runtime policy?** Optimizing arithmetic alone leaves
data movement, physical feasibility, correctness and search cost unresolved.
The six directions below are different responses to that question—not six
independent markets, and not a partition for counting papers.

The evidence base is asymmetric. All 543 DAC 2026 descriptions have initial
coding, but most lack full-paper conditions. The original cross-conference sample
began with 72 records; current coding contains 309 (272 DAC, 16 ISCA, 21 ICCAD),
none independently accepted here.
ICCAD technical evidence uses the explicit 2025 fallback. The
[source-linked direction map](../data/technology-direction-evidence-v1.json)
and [coverage queue](research-work-queue.md) identify the supporting records.

A [six-case challenge batch](direction-challenges-v1.md) now extends the reading
beyond the original anchors. It adds evaluation counterpressure, alternative
mechanisms and explicit validation boundaries; all six cases remain
description-level and independently unreviewed, not measured falsifications.
The [NotSoTiny follow-up](../dac/reports/notsotiny-primary-assessment-v1.md) now
adds selected preprint conditions without promoting the original description:
task selection, checker semantics and benchmark version must accompany any
capability comparison. Its quantitative conclusions remain pending review.
Pinned evaluator inspection also found a timeout-as-success scoring path.
This is a concrete implementation caveat, not demonstrated inflation of the
paper's scores; matched run provenance and timeout incidence are still missing.

## 1. AI-assisted design → tool-grounded generation → verified iteration

**Observed mechanisms.** HLSArchOpt supplies an author-linked partial hardware
example; the ICCAD fallback includes generation, optimization and debugging
cases (VeriOpt, VERIRL, HLSDebugger). Their common concern is how proposed changes
interact with executable design tools, not just whether generated text looks
plausible. See the [HLSArchOpt assessment](../dac/reports/hlsarchopt-primary-assessment-v1.md)
and [ICCAD capability map](../iccad/pages/topical-capability-map-2025-fallback.md).

**Directional hypothesis.** A valuable unit of progress may be a verified design
change under a fixed engineering budget, rather than a generated RTL/HLS file.
The associated subthemes are specification decomposition, tool feedback,
counterexample-guided repair, resource-aware search and reproducible execution.

**Pressure against that hypothesis.** Synthesis success is weaker than functional
equivalence. HLSArchOpt's inspected script disables simulation checks; the
Exact-T artifact's basis-state checker leaves relative-phase correctness open.
These are validation gaps, not demonstrated failures of every generated design.

[MappingEvolve's primary assessment](../dac/reports/mappingevolve-primary-assessment-v1.md)
adds a concrete tradeoff: its extracted average area gains coexist with delay
and mapper-runtime regressions. This supports evaluating constrained outcomes,
not interpreting a composite optimization score as improvement in every metric.

The pinned MappingEvolve driver also has a source-level fallback path that can
retain a rejected first candidate. This is not a demonstrated published-result
failure, but sharpens the hypothesis: correctness checks must govern state
transitions and fallback selection, not merely produce a score or diagnostic.
Countercheck: the three inspected released outer-loop histories log 90 accepted
steps and no reversions; they do not demonstrate that source-level fallback risk
occurring in those runs. Artifact concerns must not become unsupported claims
that published experimental results failed.

**Test next.** Compare systems on held-out designs with the same correctness
oracle, synthesis budget, model-call cost and retry limit. Count failed attempts
and regressions, not only successful outputs. Evidence of better accepted designs
per unit budget would strengthen this hypothesis; expensive retries without
transfer would weaken it. This does not establish autonomous signoff today.

NotSoTiny sharpens the measurement subtheme: a benchmark should report task
selection, dataset revision, solver proof state, timeout/tool-error outcomes, and
contamination checks separately. A living benchmark score is not comparable across
time unless those boundaries are version-matched.

## 2. Memory-centric execution → placement and locality → workload contracts

**Observed mechanisms.** CANNON moves ANN execution toward CXL memory; CtxMem
co-designs OS handling and tiered memory; RAF addresses local and remote traffic;
ISCA's COSM addresses CPU/PIM scheduling. These methods solve different parts of
movement and contention, not interchangeable versions of one accelerator.
See [CANNON](../dac/reports/cannon-primary-recovery-v1.md),
[CtxMem](../dac/reports/ctxmem-primary-recovery-v1.md),
[RAF](../dac/reports/raf-primary-recovery-v1.md), and the
[ISCA memory analysis](../isca/pages/memory-ecc-pim-reliability.md).

**Directional hypothesis.** More useful interfaces may expose workload structure
to placement and scheduling: access locality, capacity pressure, operator
boundaries and contention. Subthemes include near-memory execution, tiering,
operator fusion, KV-cache management and cooperative host/device scheduling.

**Boundary and counterpressure.** A capacity-limited baseline can make offload
appear exceptionally fast without establishing superiority when both systems
fit in memory. RAF's remote-access elimination does not eliminate local traffic.
CANNON's numerical source discrepancy is unresolved; CtxMem's description reports
simulation, not deployment. No evidence here establishes CXL replacing HBM or PIM.

The BusyBarn artifact adds a fault-aware wafer-scale communication mechanism to
the reading set, but only at artifact depth. Its one completed AllGather case is
useful for checking that the released code can execute after environment
normalization; it is not evidence that the proposed routing wins against a
matched baseline or generalizes across workloads and fault patterns.

**Test next.** Sweep resident and nonresident working sets, locality changes and
contention under equal capacity/bandwidth budgets. For ANN, hold recall constant.
Include migration and host overhead. Benefits that survive those controls support
a general interface opportunity; narrow capacity cliffs support a narrower one.

## 3. Reliability and security → explicit failure models → constrained execution

**Observed mechanisms.** Strix couples NPU reliability across system layers;
ISCA's ECC/PIM cases make correction and interference relevant to execution.
The HybriMoE/Icarus comparison raises a separate question: what happens when
locality assumptions are adversarially disrupted? See
[Strix](../dac/reports/strix-primary-assessment-v1.md),
[memory/ECC/PIM](../isca/pages/memory-ecc-pim-reliability.md), and the
[temporal mechanism comparison](temporal-mechanism-comparison-v1.md).

**Directional hypothesis.** Performance policies may increasingly need an explicit
operating envelope: which faults, interference patterns and adversarial inputs
they tolerate, at what correction or monitoring cost. Subthemes are fault
detection versus recovery, ECC-aware scheduling, physical interference and
adversarial workload robustness.

**Boundary.** This is not one combined robustness score. Strix's measured or
modeled detection scope is not universal correction coverage. Icarus has not been
shown here to attack HybriMoE specifically. Neither establishes safety certification.

The [SERA-Float manuscript follow-up](../iccad/reports/sera-float-primary-assessment-v1.md)
adds a representation-level subtheme: trading mantissa precision for selective
protection within a fixed 32-bit word. Its exponent corrects two flips only when
they occupy separate protected halves; mantissa parity detects rather than
corrects. This sharpens the need for explicit operating envelopes, but neither
establishes universal fault tolerance nor converts synthesized multiplication
energy into whole-inference savings. This supplementary case is independently
unreviewed and does not increase the original synthesis-anchor count.

**Test next.** Measure useful throughput after detection/recovery costs under
declared fault and threat models, including cases outside the nominal assumptions.
Report coverage failures separately from performance regressions. A mechanism
that only works under a narrow injected-fault model should retain that scope.

## 4. Physical integration → fast physical models → design/runtime feedback

**Observed mechanisms.** FLASH3D proposes a fast steady-state thermal solver;
LegoTherm addresses modular thermal modeling; ICCAD's Tasa links stacked inference
placement with thermal/bandwidth concerns, while ISCA's Lit Silicon links thermal
imbalance with runtime stragglers. Source paths are in
[direction 4](technology-direction-synthesis-v1.md#direction-4--physical-integration-becomes-an-optimization-variable).

**Directional hypothesis.** Fast physical models may become inner-loop inputs to
architecture search and workload placement, not just late checks. Subthemes are
reduced-order models, geometry-aware solvers, coupled interfaces and thermal-aware
scheduling. This connects EDA model-building with architecture and runtime choices.

**Boundary.** FLASH3D's current evidence is steady-state and description-level.
Faster simulation is not automatically better design, transient fidelity or
manufacturable integration. Geometry and material changes can invalidate a model.

**Test next.** Optimize designs with the fast model, then evaluate selected and
rejected candidates using a held-out higher-fidelity solver or measurements.
Count ranking errors and constraint violations. The decisive result is improved
feasible designs within a fixed search budget, not solver speed alone.

An additional coded physical-design example is
[COPA](../iccad/data/copa-primary-recovery-v1.json), an ICCAD 2025 fallback paper
supported here by its institutional abstract. It adjusts feedthrough-pin positions
using a routing-demand objective rather than treating wirelength as a sufficient
proxy. Our interpretation: choices made at block interfaces can affect internal
routing feasibility, so local geometric improvements need downstream validation.
The abstract does not establish final timing closure, detailed-route success, or
equal-budget comparison. This follow-up is not an independently accepted anchor
or evidence of increasing prevalence.

## 5. Design-space exploration → fidelity management → decision reliability

**Observed mechanisms.** HYPER-CIM connects a surrogate to design exploration and
selected fabricated macros. XSearch proposes multi-fidelity Bayesian exploration
for XiangShan; its description contains no quantitative evaluation. Exact-T is
a contrasting exact, resource-specific mapping case—not evidence of learned search.
See [HYPER-CIM](../dac/reports/hyper-cim-primary-recovery-v1.md),
[XSearch's source assessment](../dac/reports/xsearch-primary-recovery-v1.md), and
[Exact-T](../dac/reports/exact-t-primary-assessment-v1.md).

**Directional hypothesis.** Choosing when to spend expensive evaluation may matter
as much as choosing a search algorithm. Subthemes are uncertainty calibration,
multi-fidelity acquisition, feasible Pareto search and final-candidate verification.

The [UGLMS follow-up](../iccad/reports/uglms-primary-assessment-v1.md) extends this
question to adaptive measurement in ADC testing. It is a supplementary,
independently unreviewed case—not an added accepted anchor. Its distinction between
sample count and elapsed test time makes acquisition/compute overlap and setup
amortization relevant to the hypothesis; production behavior remains unverified.

**Counterexample and boundary.** Exact-T's assessed figure contains a modeled
space-time regression, illustrating that improving one objective need not improve
another. HYPER-CIM's predicted configurations are not fabricated designs.
Cross-simulator calibration is not silicon validation. XSearch's low-/high-fidelity
only comparators in the original coding are inferred ideas, not reported experiments.

[ParetoPilot's inspected entry point](../dac/reports/paretopilot-primary-assessment-v1.md)
samples a batch before synthesis rather than feeding measured results into further
sampling. Learned proposal quality and online adaptive search are distinct
mechanisms; neither a reasoning label nor synthesis estimates establish verified
Pareto improvements under equal budgets.

The [Orthrus primary follow-up](../iccad/data/orthrus-primary-recovery-v1.json)
provides another case for examining how optimization levels communicate. Its
assessment now has a coded record and prepared review packet, but is not an
independently accepted synthesis anchor. The key
comparison to investigate is the value of cross-layer guidance under a matched
total evaluation budget—not merely whether expanding the allowed design space
can produce a better frontier.

Its inspected PDF also prevents reading the direction as uniform dominance:
a selected power-saving step trades away delay, and some plotted guidance
directions have negative alignment. These are scoped counterexamples, not proof
that the overall Pareto result fails. The open question remains net search value
under comparable evaluation costs.

The [HLPS exploration follow-up](../iccad/data/hlps-dse-primary-recovery-v1.json)
adds a denominator caution: one baseline case has no successful implementation,
so the reported frequency ratio compares means over unequal case sets. Its
table also separates retained best frequency from continued search time. A
useful design-search comparison must report failures, comparable populations and
evaluation cost alongside outcome quality. This case now has technical coding
and a source-backed packet; independent review is pending, not a new accepted anchor.

**Test next.** Compare final independently evaluated feasible solutions at equal
wall-clock and simulator budgets, including calibration data costs. Report
misranked candidates and out-of-distribution errors. Small average prediction
error alone cannot prove better search decisions.

## 6. Specialized acceleration → representation-aware arithmetic → net benefit

**Observed mechanisms.** FuseDot exploits repeated low-bit weights; OASIS and
related ISCA cases explore representation-sensitive execution. The distinguishing
question is what structure makes work avoidable, and what it costs to expose
that structure. See [FuseDot](../dac/reports/fusedot-primary-recovery-v1.md) and
[ISCA primary LLM cases](../isca/pages/primary-evidence-llm-systems.md).

**Directional hypothesis.** Useful specializations may couple quantization,
data layout and scheduling with arithmetic, rather than optimizing MAC count
alone. Subthemes include repeated-value fusion, LUT computation, outlier handling,
structured sparsity and routing-aware execution.

The [ICCAD fallback follow-up](../iccad/data/adder-dcim-primary-recovery-v1.json)
adds Adder-DCIM as an institutional-evidence coded case, not a new accepted anchor.
The methodological question is whether representation changes remain beneficial
after conversion costs and system overhead are counted. Its available evidence
does not yet resolve that question. It remains inside the 309-record coded sample,
but its headline numbers remain outside accepted quantitative comparisons.

The [Squat recovery assessment](../iccad/data/squat-primary-recovery-v1.json)
adds a coded deployment-focused follow-up, with independent review pending. It sharpens the
evaluation question: does specialization improve latency at an acceptable
accuracy loss, and do published ratios reconcile with the underlying timings?
The recorded arithmetic discrepancy must be resolved before using those cells
as quantitative support. The original PDF confirms the same two mismatches,
which cannot be explained by rounding to the displayed precision under a
nearest-rounding assumption. A third, smaller arithmetic difference is compatible
with rounding and is not classified as an error. The two robust discrepancies
are not just an HTML extraction artifact. This is not a demonstrated failure
of the overall method.

The pinned Squat artifact exposes a further validation boundary: inspected QAT
uses rescaled tensors with PyTorch linear operations, while the mobile kernel
and timing harness were not located in that revision. Its selector ranks
batch-shared pre-softmax scores. These findings call for implementation/run
provenance before equating the released training path with measured deployment;
they do not demonstrate invalid published results.

**Boundary.** Reordering and metadata can consume the saved work. Equal integer
codes across different quantization groups need not denote equal weights;
finite-precision regrouping requires accuracy checks. A changed model distribution
may erase the repetition or sparsity on which a design depends.

**Test next.** Sweep structure strength and model families at matched accuracy,
including preprocessing, memory and area costs. A specialization that degrades
gracefully outside its favored distribution is stronger evidence than a peak gain.

## Cross-conference implication and temporal verdict

The research opportunity suggested by these cases is **closing constrained
engineering loops**: generation needs verification; specialization needs movement
and accuracy accounting; physical modeling needs decision validation; scheduling
needs failure and contention assumptions. These are interpretive connections,
not proof that the cited authors implemented a common integrated system.

DAC supplies broad description-level candidates; selected ISCA sources expose
system interactions; ICCAD's 2025 fallback supplies design-method depth. Those
roles describe this collection, not intrinsic rankings of the conferences.

**Temporal evidence is insufficient for all six rising/declining claims.** The
three purposeful DAC pairs control broad question and description tier, not
workloads or hardware. Only 24 of 419 historical DAC descriptions are captured;
missing historical evidence cannot be treated as absence. No independent review
has accepted these directions. The next synthesis pass must challenge them with
the remaining coded corpus, contradictory cases and matched historical subsets.

No direction above establishes adoption, market share, commercial viability, a
winning platform or a date by which it will become dominant. The practical output
is a set of technical hypotheses and experiments that can strengthen or reject
them—not a forecast disguised as a paper count.
