# Evidence dossier — Closed Loop Design

This dossier combines the canonical direction atlas, historical adjudicated records, and dated editorial corrections. It is a source-backed reading aid, not an independent review or a claim that the records are comparable.

- Direction page: [Closed Loop Design](../03-closed-loop-design.md)
- Source direction IDs: `multifidelity-physics-aware-search`
- Direction status: `provisional_mechanism_hypothesis`
- Independent reviews recorded: `0`

## Reading rule

`UNKNOWN` means a field is not recorded, not that the paper lacks the condition. Corrections supersede the current displayed fields while historical fields remain expandable. A historical condition-complete label does not establish that a correction has passed condition or independent review.

## GEMIR: Graph-Based Joint Modeling of Electromigration and IR Drop for Power Grid

- Paper ID: `dac-2026-research046`
- Conference/edition: `dac` / `2026`
- Evidence tier: `Primary captured official DAC description plus bounded recovery assessment and existing authored power-integrity discussion; full paper not recovered, numerical claims withheld pending conditions, no reproduced physics validation or fabricated-chip result`
- Ledger record: `dac/data/adjudicated-2026-batch.jsonl`

**Current evidence correction — 2026-09-09**

Deepens the GEMIR treatment into a paper-level reading; separates joint graph prediction, node-edge attention, KCL/Korhonen physics constraints and conflict-gated multitask training from physical boundary validity, tail errors, signoff thresholds, calibration and process transfer, while preserving the 40.79% IR-drop-MAE and 19.35% EM-stress-RMSE source claims as withheld pending full-paper conditions.

Condition review of this correction and independent acceptance remain pending. The direction mapping is inherited, not revalidated by this update.

[Dated correction register](../../../data/editorial-paper-corrections-v1.json)

- Source: [https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH046](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH046)

| Field | Current record |
|---|---|
| Problem | Power-grid reliability depends on both node-level voltage loss and edge-level electromigration stress, while numerical analysis is expensive on large designs and separate ML predictors may miss shared structure. |
| Mechanism / artifact | GEMIR jointly predicts static IR drop at graph nodes and electromigration-induced stress at graph edges using cross-layer node-edge attention, physics-informed constraints incorporating Kirchhoff's current law and the Korhonen PDE, and conflict-gated multitask gradient fusion. Features, loss terms, boundary conditions, gradient gate, training targets and inference workflow are unspecified. |
| Workload / benchmark | Power-grid analysis on large-scale designs for static IR drop and EM-induced stress; design sizes, technology/process, grid topology, current loads, temperature/material parameters, train/test split, leakage controls, numerical reference solver, PVT/aging conditions and workload population are unspecified. |
| Hardware / process | Power-grid graphs with node voltage and edge stress fields; physical boundary conditions, via/resistance/capacitance models, current sources, thermal coupling, material parameters, process node, signoff tool, compute hardware and fabricated-chip validation are unspecified. |
| Baselines | Existing numerical power-grid methods; Single-task ML predictors; Multitask ML baselines; Same designs, reference solver, loads, physical parameters, train/test split, error units, runtime hardware and signoff threshold are unspecified |
| Metrics | The source reports 40.79% reduction in IR-drop mean absolute error and 19.35% reduction in electromigration-stress root-mean-square error, plus computational efficiency and generalization; it reports no absolute errors/units, worst-case or tail error, named baseline conditions, design/process distribution, runtime, memory, threshold violations, lifetime prediction or silicon validation. |
| Evidence locator / span | DAC 2026 official description; existing power-integrity-and-reliability editorial explanation; selected primary-source recovery assessment; captured Problem, Mechanism / artifact, Workload, Hardware, Baseline, Measurements and Limits fields; no full manuscript, design/process matrix, numerical trace or independent signoff validation. |
| Limits | KCL and the Korhonen PDE are useful constraints only when boundary conditions, source terms, material parameters, temperature and discretization match the physical problem. Verify residuals and conservation on held-out grids, compare node/edge extremes with a trusted numerical solver and test current/load, temperature, geometry and material shifts; low mean error can hide a signoff-critical hotspot or stressed segment.; IR-drop MAE and EM-stress RMSE are different quantities and cannot be averaged into a reliability gain. Report absolute units, distributions, maxima/percentiles, threshold classification, spatial localization and error correlation; distinguish prediction quality from the downstream decision of widening a wire, adding vias or changing the grid. Measure graph construction, reference-solver labels, training/inference, calibration and any fallback cost.; The 40.79%/19.35% reductions and generalization claim are description-backed with full-paper conditions unresolved. They do not establish signoff-quality power integrity, lifetime improvement, cross-technology transfer or fabricated-chip validity. The evidence supports physics-informed joint EM/IR prediction, not replacement of trusted power-integrity and reliability checks. |

<details markdown="1">
<summary>Historical captured record — superseded in the current table</summary>

Historical atlas evidence tier: `official_description`.

| Field | Historical record |
|---|---|
| problem | Separate EM and IR-drop analysis misses their shared physical structure, while numerical methods are expensive on large designs. |
| mechanism | Graph-based multitask learning with node-edge attention, physics-informed constraints, and conflict-gated gradient fusion. |
| workload | Power-grid analysis for node-level static IR drop and edge-level electromigration-induced stress. |
| hardware | UNKNOWN — not present in the current adjudicated record |
| baselines | existing numerical methods; single-task machine-learning approaches; multitask baselines |
| metrics | 40.79% reduction in IR-drop MAE; 19.35% reduction in EM-stress RMSE; computational efficiency and generalization |
| limits | The description does not disclose design sizes, absolute runtime, or the distribution of gains across technologies and workloads. |
| locator | GEMIR jointly predicts node-level static IR drop and edge-level electromigration stress using cross-layer attention, physics-informed constraints for KCL and the Korhonen PDE, and conflict-gated multitask optimization; it reports 40.79% lower IR-drop MAE and 19.35% lower EM-stress RMSE. |

[Historical source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH046&sess=sess112)

</details>


Mapping review status: `not_recorded`; independent review status: `pending`.

## HYPER-CIM: Hierarchical Predictive Exploration and Realizable Design Flow for High-Efficient Digital CIM

- Paper ID: `dac-2026-research1101`
- Conference/edition: `dac` / `2026`
- Evidence tier: `Primary captured official DAC description plus supplementary official/institutional assessment; no recovered full paper or independent surrogate, design-flow and silicon reproduction`
- Ledger record: `dac/data/adjudicated-2026-batch.jsonl`

**Current evidence correction — 2026-09-08**

Reconciles the HYPER-CIM card with the captured official description and supplementary assessment; explains CIM hierarchy, surrogate prediction, Pareto tradeoffs, TOPS metrics, predicted configuration counts and silicon-verification scope from first principles.

Condition review of this correction and independent acceptance remain pending. The direction mapping is inherited, not revalidated by this update.

[Dated correction register](../../../data/editorial-paper-corrections-v1.json)

- Source: [https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH1101&sess=sess156](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH1101&sess=sess156)

| Field | Current record |
|---|---|
| Problem | CIM exploration can optimize one level without preserving circuit-faithful visibility into macro, accelerator and architecture interactions, making predicted high-efficiency designs difficult to realize or compare. |
| Mechanism / artifact | Hierarchical predictive exploration flow with a digital 28-nm CIM template, multi-head circuit-optimization surrogate, Pareto search and selected silicon verification. |
| Workload / benchmark | Digital CIM macro and architecture design across precision, storage, channels, pipeline depth and accumulation length; workload, accuracy, operation convention, comparison set and hierarchy conditions are unspecified. |
| Hardware / process | Digital 28-nm CIM template and fabricated macro evidence; process details, frequency, power/area boundaries, yield, layout, test conditions and architecture integration are unspecified. |
| Baselines | Prior CIM designs; Single-level CIM optimization flows; Full comparison set, objective normalization, workload/accuracy, prediction fidelity and fabricated-condition parity are unspecified |
| Metrics | The official description reports 90.8 TOPS/W, 1.23 TOPS/mm², 31.12x–3.8x10^6x FoM improvement, 52.13–67.9 TOPS/W and 0.41–0.51 TOPS/mm² ranges; operation, power, area, workload, reference and aggregation boundaries are unspecified. |
| Evidence locator / span | DAC 2026 official description and data/review-packets/dac-2026-research1101.json plus data/review-packets/hyper-cim-primary-recovery-v1.json: digital 28-nm CIM template; multi-head surrogate; hierarchical/Pareto flow; silicon verification claim; 90.8 TOPS/W, 1.23 TOPS/mm² and wide FoM/range claims; 297M predicted configurations, >8k training points and five reported macros assessment boundary. |
| Limits | A circuit surrogate can reduce exploration cost only if its prediction error preserves useful candidate ordering near constraints and Pareto boundaries; average error alone is insufficient.; Pareto search yields non-dominated tradeoffs rather than one universally best design, and its result depends on objectives, normalization, constraints and precision.; 297 million predicted configurations and more than 8,000 training points are modeling/search quantities, not fabricated designs; five reported macros do not validate the full predicted space.; Silicon verification of selected macros can expose model mismatch but does not establish all predicted configurations, full architecture integration, yield or reproducibility; full paper and comparison conditions remain open. |

<details markdown="1">
<summary>Historical captured record — superseded in the current table</summary>

Historical atlas evidence tier: `official_description`.

| Field | Historical record |
|---|---|
| problem | CIM exploration often optimizes only one level and lacks circuit-faithful visibility across macro, accelerator, and architecture decisions. |
| mechanism | Hierarchical predictive exploration flow with a digital 28 nm CIM template, multi-head circuit-optimization surrogate, Pareto search, and silicon verification. |
| workload | Digital compute-in-memory macro and architecture design across tunable precision, storage, channels, pipeline depth, and accumulation length. |
| hardware | UNKNOWN — not present in the current adjudicated record |
| baselines | prior CIM designs; single-level CIM optimization flows |
| metrics | 90.8 TOPS/W; 1.23 TOPS/mm²; 31.12X–3.8×10⁶X FoM improvement; 52.13 to 67.9 TOPS/W energy-efficiency improvement; 0.41 to 0.51 TOPS/mm² area-efficiency improvement |
| limits | The description does not provide the full prior-design comparison set, accuracy/workload conditions, or yield/reproducibility details for fabricated macros. |
| locator | HYPER-CIM uses over 8k silicon-consistent points to train a hierarchical PPA surrogate over 297M configurations, fabricates and verifies 28 nm CIM macros, and reports 90.8 TOPS/W, 1.23 TOPS/mm², and cross-level energy/area improvements. |

[Historical source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH1101&sess=sess156)

</details>


Mapping review status: `not_recorded`; independent review status: `pending`.

## RSizing: Robust Bayesian Optimization for Analog Circuit Sizing Under Process Variations

- Paper ID: `iccad-2025-1080`
- Conference/edition: `iccad` / `2025`
- Evidence tier: `Primary author-hosted manuscript-backed selected evaluation; page-level extraction performed 2026-09-08; independent reproduction and broader technology/circuit validation remain open`
- Ledger record: `iccad/data/adjudicated-2025-batch.jsonl`

**Current evidence correction — 2026-09-08**

Adds a page-backed RSizing reading from the recovered author PDF; explains robust Pareto optimization, heteroscedastic process variation, MVaR approximation, Monte Carlo budgets and the yield/runtime tradeoff rather than retaining the shallow card.

Condition review of this correction and independent acceptance remain pending. The direction mapping is inherited, not revalidated by this update.

[Dated correction register](../../../data/editorial-paper-corrections-v1.json)

- Source: [https://www.cse.cuhk.edu.hk/~byu/papers/C287-ICCAD2025-RSizing.pdf](https://www.cse.cuhk.edu.hk/~byu/papers/C287-ICCAD2025-RSizing.pdf)

| Field | Current record |
|---|---|
| Problem | Analog circuit sizing must choose device parameters that trade several performance objectives while meeting a probability-of-success requirement under process variation. |
| Mechanism / artifact | Three-phase robust Bayesian optimization: nominal multi-objective pruning, heteroscedastic Gaussian-process modeling with Thompson sampling and targeted Monte Carlo refinement/calibration; the recovered paper defines a robust Pareto set using a yield constraint. |
| Workload / benchmark | ITC 2017 OPAMP, OSC and PLL benchmark circuits with 36, 14 and 77 selected parameters and the listed circuit objectives; Spectre simulations use TSMC 40 nm. Yield targets are 97.5%, 99.0% and 99.9%. |
| Hardware / process | Spectre analog simulation on TSMC 40 nm; 80-core 2.70 GHz CPU and A100 80 GB machine; 50 Monte Carlo samples in variation-aware optimization and 100/200/500 refinement samples for the three yield targets, with final verification by 1,000 samples. |
| Baselines | NSGA-II; MARS-NEI; PVTSizing; NSGA-II is omitted for PLL because of simulation cost; baseline budgets and objective constructions are not fully symmetric |
| Metrics | Manuscript-backed: Table II verifies mean/min/max yield over 1,000 Monte Carlo samples; Table III reports yield, hypervolume and runtime for OPAMP/OSC/PLL at 97.5%, 99.0% and 99.9%; Table IV compares PVTSizing and RSizing at three targets. The paper notes MVaR approximation bias for lower yield requirements and tradeoffs between target yield and performance. |
| Evidence locator / span | Recovered author-hosted PDF v1, pages 1–7; Sections II–IV; Fig. 2; Table I (page 6), Tables II–IV (page 7); TSMC 40 nm, ITC 2017 OPAMP/OSC/PLL, yield targets, Monte Carlo budgets and baseline settings. |
| Limits | A robust Pareto solution is not one design that maximizes every metric. It is a set of non-dominated designs whose probability of meeting the performance specifications is at least the required yield. The yield estimate is itself uncertain when based on finite Monte Carlo samples, especially near a threshold.; The heteroscedastic GP models input-dependent variation and the acquisition function chooses expensive simulations, but the model can be wrong when distributions are non-Gaussian or local variation changes. The paper's refinement uses MVaR estimates and states that approximation error is not fully addressed and may bias results at lower yield.; The recovered experiment is strong page-backed evidence under TSMC 40 nm, ITC 2017 circuits, stated simulation budgets and a specific machine. It does not establish transfer to other nodes, circuits, simulators, variation distributions or commercial signoff. Runtime comparisons also need the asymmetric PLL omission and different baseline budgets kept visible. |

<details markdown="1">
<summary>Historical captured record — superseded in the current table</summary>

Historical atlas evidence tier: `author_pdf`.

| Field | Historical record |
|---|---|
| problem | Analog circuit sizing under process variation is expensive and manual; nominal optimization can produce designs with poor yield when performance distributions shift across manufacturing variation. |
| mechanism | Three-phase robust Bayesian optimization using nominal-region pruning, heteroscedastic Gaussian-process surrogate models, Thompson sampling, targeted Monte Carlo simulations, and model calibration. |
| workload | Three analog benchmark circuits evaluated under process variation with multi-objective performance and yield requirements. |
| hardware | CMOS analog circuit sizing and Monte Carlo process-variation simulation; exact technology node, circuit identities, and simulation budgets require full-paper extraction. |
| baselines | existing analog circuit sizing and Bayesian-optimization methods |
| metrics | yield requirement satisfaction; multiple analog performance objectives; Monte Carlo simulation/computational cost |
| limits | The evidence is an author-hosted conference PDF; the repository has not yet extracted numerical table values, exact baselines, technology assumptions, or all yield/quality tradeoffs. |
| locator | RSizing uses a three-phase strategy: nominal-condition optimization to prune promising regions, heteroscedastic Gaussian processes to model non-uniform process-variation effects, and Thompson-sampling acquisition followed by targeted Monte Carlo refinement and calibration. Experiments on three benchmark circuits report robust designs that meet yield requirements while optimizing multiple performance metrics with lower computational cost. |

[Historical source](https://www.cse.cuhk.edu.hk/~byu/papers/C287-ICCAD2025-RSizing.pdf)

</details>


Mapping review status: `not_recorded`; independent review status: `pending`.

## NeuroPDE: A Neuromorphic PDE Solver Based on Spintronic and Ferroelectric Devices

- Paper ID: `iccad-2025-130`
- Conference/edition: `iccad` / `2025`
- Evidence tier: `Recovered version-1 manuscript; cited sections inspected`
- Ledger record: `iccad/data/adjudicated-2025-batch-2.jsonl`

**Current evidence correction — 2026-09-07**

Full text establishes simulation-only evidence and single-walk accounting; squared-error definition differs from statistical variance.

Condition review of this correction and independent acceptance remain pending. The direction mapping is inherited, not revalidated by this update.

[Dated correction register](../../../data/editorial-paper-corrections-v1.json)

- Source: [https://arxiv.org/pdf/2507.04677v1](https://arxiv.org/pdf/2507.04677v1)

| Field | Current record |
|---|---|
| Problem | Efficient probabilistic transitions for PDE estimation. |
| Mechanism / artifact | Magnetic switching and ferroelectric transition weights. |
| Workload / benchmark | 1D heat and 2D diffusion examples; single-thread random walks. |
| Hardware / process | SPICE/Python simulation; GPDK045, 300 K; 50,000 activation histories. |
| Baselines | Analytical solutions; prior Loihi/TrueNorth results. |
| Metrics | Single-walk operation: 10 ns, 1.451 pJ; not complete solution cost. |
| Evidence locator / span | Sections IV–V, PDF pages 4–8; Equation 10, Figure 12. |
| Limits | Equation 10 is squared reference error; temperature drift untested; not fabricated hardware. |

<details markdown="1">
<summary>Historical captured record — superseded in the current table</summary>

Historical atlas evidence tier: `primary_preprint`.

| Field | Historical record |
|---|---|
| problem | Conventional von Neumann hardware lacks hardware-intrinsic randomness, limiting the performance of Monte Carlo and random-walk PDE solvers. |
| mechanism | Neuromorphic architecture using stochastic spin neurons for probabilistic transmission and ferroelectric synapses for continuous non-volatile weights. |
| workload | Diffusion-equation PDE solving with comparison against analytical solutions and CMOS-based neuromorphic-chip baselines. |
| hardware | Emerging spintronic and ferroelectric devices with physical stochasticity and non-volatile analog weight storage; device models, variability, conversion, and fabrication assumptions require full-paper review. |
| baselines | advanced CMOS-based neuromorphic chips; analytical diffusion-equation solutions |
| metrics | variance below 1e-2 versus analytical solutions; 3.48x–315x execution-time speedup; 2.7x–29.8x energy advantage |
| limits | The preprint abstract does not expose PDE suite breadth, device-area and conversion costs, process assumptions, precision, or how CMOS baselines are normalized; ranges require paper-level verification. |
| locator | NeuroPDE uses probabilistic spin neurons to emulate random walks and non-volatile ferroelectric synapses for continuous weights in a neuromorphic PDE solver. For diffusion equations it reports variance below 1e-2 against analytical solutions, 3.48x–315x execution-time speedup, and 2.7x–29.8x energy advantage over advanced CMOS-based neuromorphic chips. |

[Historical source](https://arxiv.org/abs/2507.04677)

</details>


Mapping review status: `not_recorded`; independent review status: `pending`.

## Quantum Circuit Synthesis Using an Exact T Library

- Paper ID: `dac-2026-research031`
- Conference/edition: `dac` / `2026`
- Evidence tier: `Primary captured official DAC description plus selected author-preprint reading; source-version discrepancy remains open, and no independent exactness proof, benchmark reproduction or fault-tolerant hardware validation`
- Ledger record: `dac/data/adjudicated-2026-batch.jsonl`

**Current evidence correction — 2026-09-09**

Deepens the exact-T synthesis treatment using the captured official description and selected author-preprint assessment; separates Clifford-equivalence canonicalization, bounded exact library construction and mapping from clean-ancilla correctness, global optimality, runtime and hardware cost, and preserves the official up-to-16% claim alongside the assessed 5.3% six-EPFL-circuit geomean and 0.5% library-only result with their source/version boundary.

Condition review of this correction and independent acceptance remain pending. The direction mapping is inherited, not revalidated by this update.

[Dated correction register](../../../data/editorial-paper-corrections-v1.json)

- Source: [https://arxiv.org/html/2605.15476v1](https://arxiv.org/html/2605.15476v1)

| Field | Current record |
|---|---|
| Problem | In fault-tolerant quantum synthesis, T resources dominate relevant space-time cost while minimizing classical AND count can miss phase cancellation and therefore misestimate T cost. |
| Mechanism / artifact | The work formulates exact T synthesis, canonicalizes Boolean functions under Clifford equivalence, precomputes T-optimal implementations for bounded small instances and uses a specialized mapper for larger circuits. The selected assessment identifies an exact-solver bound of N ≤ 7 total qubits and correctness under a clean output ancilla initialized to zero; phase-equivalence, ancilla, synthesis and mapper details remain bounded by the inspected sections. |
| Workload / benchmark | EPFL arithmetic circuits and selected cryptographic modules; the selected assessment reports six EPFL circuits, comparison against exact-MC mapping, library-only substitution, and a QLUT mapping evaluation. Circuit dimensions, gate basis, ancilla limits, decomposition conventions, target fault-tolerant architecture, runtime corpus and source-version relationship to the official 16% headline are not fully reconciled. |
| Hardware / process | Fault-tolerant quantum compilation where T gates/magic states are costly; selected mapping assessment ran on an Apple M4 Max with 36 GB RAM, but physical architecture, magic-state factory cost, scheduling, parallelism, error-correction code, qubit budget, decoder and hardware execution are unspecified. |
| Baselines | Conventional XOR/AND/NOT-basis AND-count minimization; Exact-MC mapping; Library-only substitution; Previous best-known T counts; Same Boolean/unitary convention, clean-ancilla assumption, circuit set, gate basis, decomposition, mapper, target constraints, runtime boundary and source version are unspecified |
| Metrics | The official description reports up to 16% T-count reduction on EPFL benchmarks and improved best-known T counts for selected cryptographic modules. The selected author-preprint assessment reports 5.3% geometric-mean T-count reduction for six EPFL arithmetic circuits with the customized mapper, about 0.5% geometric-mean reduction for library-only substitution with regressions on some circuits, and mapping stages up to 11.7% of reported QLUT synthesis runtime; these are not reconciled into one universal result and no hardware speedup is reported. |
| Evidence locator / span | DAC 2026 official description; selected author-preprint assessment exact-t-primary-assessment-v1; sections 4.2–4.3 and 6, S4.SS2/S4.SS3/S6.SS1/S6.SS2/S6.SS4, Table 2 and Figures 8–11; no independent reproduction or hardware execution. |
| Limits | Exactness is conditional. Verify the synthesized operation under the stated Clifford-equivalence and clean-zero-ancilla assumptions, including global phase, output ancilla state, qubit ordering, measurement behavior and allowed temporary resources. A circuit can match a Boolean function while violating the intended unitary or ancilla contract.; Exact optimality for N ≤ 7 total qubits does not establish global optimality for larger mapped circuits. Report library construction/storage, mapper search, decomposition, ancilla, depth, Clifford count, routing and compilation runtime; test held-out circuits and compare per-circuit regressions rather than only a best or geometric mean.; The official up-to-16% headline and selected 5.3%/0.5% preprint findings have different scopes and require source-version reconciliation. T-count reduction is not hardware speedup or universal space-time reduction; magic-state production, scheduling, parallelism, code distance, qubit count, error rates and physical execution remain unvalidated. The evidence supports exact bounded T-cost synthesis, not demonstrated globally optimal or hardware-efficient fault-tolerant compilation. |

<details markdown="1">
<summary>Historical captured record — superseded in the current table</summary>

Historical atlas evidence tier: `official_description`.

| Field | Historical record |
|---|---|
| problem | AND-count minimization is an imperfect proxy for T cost in fault-tolerant quantum synthesis because it misses phase cancellation. |
| mechanism | Exact T-synthesis formulation with Clifford-equivalence canonicalization, precomputed small-function libraries, and a specialized mapper. |
| workload | EPFL benchmarks and cryptographic circuit modules in fault-tolerant quantum synthesis. |
| hardware | UNKNOWN — not present in the current adjudicated record |
| baselines | conventional XOR/AND/NOT-basis AND-count minimization; previous best-known T counts |
| metrics | up to 16% T-count reduction; improved best-known T counts for selected cryptographic modules |
| limits | The public description does not enumerate all circuits, runtime costs, or the scalability boundary of exact precomputation. |
| locator | The work formulates exact T synthesis, canonicalizes Boolean functions under Clifford equivalence, precomputes T-optimal implementations up to seven variables, and reports up to 16% T-count reduction on EPFL benchmarks plus improvements for cryptographic modules. |

[Historical source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH031&sess=sess133)

</details>


Mapping review status: `researcher_reconciliation_not_independent`; independent review status: `pending`.

## Xsearch: Exploring Microarchitecture Design Space Through Bayesian Optimization and Cross Evaluation on Multi-Fidelity Simulators

- Paper ID: `dac-2026-research1186`
- Conference/edition: `dac` / `2026`
- Evidence tier: `Primary captured official DAC description plus existing authored learned-DSE discussion; no full-paper extraction, numerical result, simulator-condition matrix or independent high-fidelity validation`
- Ledger record: `dac/data/adjudicated-2026-batch-4.jsonl`

**Current evidence correction — 2026-09-09**

Deepens the Xsearch treatment into a paper-level reading; separates multi-fidelity Bayesian acquisition and high-fidelity cross-evaluation from simulator calibration error, ranking validity, feasibility, search budget and processor-design conclusions, while preserving the XiangShan application without inventing quantitative superiority.

Condition review of this correction and independent acceptance remain pending. The direction mapping is inherited, not revalidated by this update.

[Dated correction register](../../../data/editorial-paper-corrections-v1.json)

- Source: [https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH1186&sess=sess167](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH1186&sess=sess167)

| Field | Current record |
|---|---|
| Problem | Microarchitecture design-space exploration must choose among expensive accurate simulations and cheaper coarse simulations; a low-fidelity shortcut can spend more evaluations while changing the ranking of viable processor configurations. |
| Mechanism / artifact | Xsearch is described as multi-fidelity Bayesian optimization that cross-evaluates designs across simulators with different fidelity and uses high-fidelity simulation data for calibration; acquisition function, surrogate outputs and uncertainty, fidelity-selection rule, calibration model, simulator coupling and stopping criterion are unspecified. |
| Workload / benchmark | Microarchitecture-parameter exploration for the open-source XiangShan high-performance processor core; core revision, parameter dimensions/ranges, workloads, warm-up and sampling protocol, objectives, constraints, design-space size, train/validation split and held-out final evaluation are unspecified. |
| Hardware / process | Processor design flow using coarse- and fine-grained simulators with different cost and accuracy; simulator identities/versions, target implementation, architectural model, compute hardware, parallelism, licensing and timing boundary are unspecified. |
| Baselines | Low-fidelity-only Bayesian or search-based exploration; High-fidelity-only exploration; Random or conventional Bayesian optimization with one simulator; Same XiangShan configuration space, workloads, objective/constraints, seed, evaluation budget, calibration data, simulator versions and end-to-end timing boundary are unspecified |
| Metrics | The source claims an efficiency–accuracy tradeoff, broader low-fidelity exploration and high-fidelity calibration/cross-evaluation on XiangShan, but reports no numerical improvement, simulator error, convergence, final design quality, feasibility rate, evaluation count, wall-clock cost or high-fidelity held-out result. |
| Evidence locator / span | DAC 2026 official description; existing learned-design-space-exploration chapter framing; captured Problem, Mechanism / artifact, Workload, Hardware, Baseline, Measurements and Limits fields; no manuscript pages, simulator table, search trace or reproduced XiangShan evaluation. |
| Limits | Low-fidelity agreement is not automatically a useful design signal. Measure prediction error and rank agreement against high-fidelity simulation across the full parameter space, especially near constraints and Pareto boundaries; a calibrated average can still select an infeasible or inferior processor configuration. Report uncertainty, calibration residuals, false feasible/false infeasible decisions and the cost of each high-fidelity check.; Bayesian optimization needs an explicit objective, constraints, acquisition function, initial design, fidelity-selection policy, noise model, stopping rule and total budget. Count low- and high-fidelity simulations, surrogate training, failed simulations, calibration, parallelism and final confirmation under the same elapsed-time or compute boundary. More explored points is not evidence of a better design without matched-budget final evaluation.; XiangShan application does not establish transfer to another core, workload, simulator pair or implementation target. Hold out workloads, parameter regions and processor revisions; inspect repeated seeds, convergence and rejected candidates, and compare low-fidelity-only, high-fidelity-only and single-fidelity search at equal objectives and budgets. The official description supports a multi-fidelity exploration direction, not demonstrated quantitative superiority, simulator-grounded accuracy or improved processor design quality. |

<details markdown="1">
<summary>Historical captured record — superseded in the current table</summary>

Historical atlas evidence tier: `official_description`.

| Field | Historical record |
|---|---|
| problem | Microarchitecture design-space exploration must balance expensive accurate simulation against fast but less accurate coarse simulation. |
| mechanism | Multi-fidelity Bayesian optimization with cross-evaluation across simulators of different fidelity and calibration using high-fidelity data. |
| workload | Microarchitecture parameter exploration for the open-source XiangShan high-performance processor core. |
| hardware | Open-source high-performance processor and multiple simulators with differing fidelity; parameter space, simulator identities, calibration model, and hardware targets are not reported. |
| baselines | low-fidelity-only exploration; high-fidelity-only exploration (implied comparison) |
| metrics | exploration efficiency and evaluation accuracy (numeric results not reported in the description) |
| limits | The description does not report search budgets, objective functions, simulator errors, convergence, baseline results, or processor configurations; it establishes the method and application but not quantitative superiority. |
| locator | XSearch addresses the efficiency–accuracy trade-off in microarchitecture design-space exploration by using multi-fidelity Bayesian optimization. It explores more points with low-fidelity simulation and calibrates or cross-evaluates candidates with high-fidelity simulation; the method is applied to the open-source XiangShan high-performance processor core. |

[Historical source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH1186&sess=sess167)

</details>


Mapping review status: `researcher_reconciliation_not_independent`; independent review status: `pending`.

## Direction boundary

Search quality requires baseline budgets, constraint-violation analysis, model error, and independent reproduction; headline surrogate or figure-of-merit gains are conditional.

Next evidence action: Compare final feasible solutions at equal wall-clock and simulator budgets, including calibration cost, rejected candidates, and out-of-distribution error.
