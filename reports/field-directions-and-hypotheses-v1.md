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
contains 72 records (49 DAC, 15 ISCA, 8 ICCAD), none independently accepted here.
ICCAD technical evidence uses the explicit 2025 fallback. The
[source-linked direction map](../data/technology-direction-evidence-v1.json)
and [coverage queue](research-work-queue.md) identify the supporting records.

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
