# Parasitic extraction and modeling

This subject has 1 record in the selected sample. This page explains where it fits, then presents all captured paper evidence without shortening the measurements or limitations.

[Definitions used in the paper records](../reading-guide-v1.md)

## Understand the parent subject first

- [Physical design and manufacturing](../themes/physical-design-and-manufacturing.md)

## Physical wires contribute electrical behavior

A logical connection says which circuit points are connected. It does not describe the full electrical effect of the wire used to connect them. Resistance and capacitance depend on physical geometry and neighboring structures. Parasitic extraction constructs electrical models of those effects from a layout. For example, [OpenRCX's documentation](https://openroad.readthedocs.io/en/latest/main/src/rcx/README.html) describes extracting resistance and capacitance using neighboring-wire and layer context.

The selected paper addresses capacitance prediction during interconnect-geometry exploration. This is narrower than replacing every part of a complete extraction flow. A fast estimate becomes useful when many proposed geometry changes would otherwise require repeating expensive reference calculations.

## What the selected paper actually models

[Capacitance Extraction via Machine Learning](../observed-subthemes/parasitic-extraction-and-modeling.md#paper-iccad-2025-1142) converts layout cross-sections into geometry features and trains layer-specific regressors against two-dimensional field-solver labels. A regressor predicts numerical values. The captured Sections V–VI describe deep neural networks for sensitive M0 cases and LightGBM, a tree-based prediction method, elsewhere.

The experiment covers 94 standard cells in an imec N2 predictive nanosheet process design kit. A predictive kit supplies modeled technology information; it is not a report of measurements from fabricated silicon. The study varies the thickness of the M0 metal layer. The evidence does not establish transfer to an unrelated cell library or fabrication process.

The [stored primary-source assessment](../../iccad/data/capacitance-ml-primary-recovery-v1.json) records training thicknesses from 22 to 58 nm in 6 nm steps and testing from 18 to 62 nm in 2 nm steps. Sections VI.A–D, Table IV, and Figures 14–16 provide the captured experimental context; Table IV and the figures were visually checked on PDF page 8 during source recovery.

## Why the test split matters

A thickness absent from model fitting is not necessarily untouched by model development. The manuscript describes 38 nm as unseen, but the recorded review finds that Section VI.A uses it in the loss for selecting hyperparameters. Hyperparameters are choices controlling how a model is built or trained. Selecting them using a case gives that case a role in development even if it was not directly used to fit the final model's parameters.

This does not establish direct training-data leakage or invalidate every reported prediction. It does mean the evidence does not demonstrate an untouched holdout at that thickness. A stronger transfer test would reserve thicknesses, geometries, or entire cells before tuning and report their results separately. The recovered figures also show increasing errors near the range boundaries, which matters when exploration moves beyond familiar configurations.

## Fast prediction and total preparation cost

The abstract contrasts approximately 25 minutes for commercial extraction after a layer-thickness change with much faster learned prediction. The recovered experiment reports per-cell pattern processing and inference times of 0.082 and 0.803 seconds. Those timings exclude database construction and tuning; they should not be substituted directly into a whole-flow speedup calculation with a different unit of work.

Table IV records 1.8 hours of database construction, two days of training, and an additional 2.3 hours of training. The evaluation uses a dual Intel 6454S workstation with 89 training threads. Whether this preparation pays off depends on how many subsequent evaluations reuse it, what each evaluation replaces, and whether new geometries require rebuilding or retraining.

The author project page describes different model and dataset counts from the manuscript. The stored assessment explicitly keeps those accounts separate because their equivalence and revision history are not established. Its additional claims must not be silently imported into the manuscript's experiment.

## What this supports as a research direction

The paper gives a concrete example of learning geometry-conditioned electrical estimates to make repeated design exploration cheaper. It does not yet establish general process transfer, measured-silicon accuracy, or amortized full-flow acceleration. The next decisive experiment would combine an untouched evaluation set, complete preparation and reuse accounting, and checks of whether prediction errors alter the selected design or its final electrical acceptance. That would connect fast modeling to useful engineering decisions rather than only fast inference.

## Compare the results carefully

First identify the inputs and required output quality. Then identify the limited resource: time, memory, communication, energy, circuit area, or correctness coverage. Ask which part of the method reduces that cost and which new cost it adds. Compare numbers only when the experiments hold these conditions sufficiently similar.

A conference description may explain the proposal while omitting the full experiment. An author preprint link may have been coded from its abstract. The source classification does not by itself establish that every table was read. Missing locations remain visible below.

## Complete captured evidence

These are evidence records, not substitutes for the explanations above. Each record preserves its problem, proposed method, measurements, comparison conditions, and source limits. A populated record does not establish that its mechanism has been fully explained or independently verified.

<span id="paper-iccad-2025-1142"></span>

### Capacitance Extraction via Machine Learning with Application to Interconnect Geometry Exploration

ICCAD 2025 · Record: `iccad-2025-1142`

**Problem:**

Repeated parasitic extraction makes standard-cell interconnect geometry exploration expensive.

**Mechanism / artifact:**

Layout cross-sections feed layer-specific capacitance regressors trained on 2D field-solver labels; DNNs handle sensitive M0 cases and LightGBM handles others.

**Workload — the work tested:**

94 standard cells in imec N2 predictive nanosheet PDK; M0-thickness sweep, not cross-library evaluation.

**Hardware and manufacturing assumptions:**

Dual Intel 6454S workstation with 89 training threads; predictive PDK, not measured silicon; inference timings exclude database construction and tuning.

**Baseline — the comparison method:**

2D field-solver capacitance labels

DNN versus LightGBM prediction comparison

**Reported measurements:**

Not established in the captured evidence.

**Limits on the conclusion:**

38nm is described as unseen but used for hyperparameter-selection loss; untouched holdout not established. Boundary errors increase. Preparation/training costs must be amortized before asserting flow acceleration. No demonstrated cross-library transfer or independent acceptance.

**Source and location**

Evidence tier: Medium primary full text. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://gtcad.gatech.edu/www/papers/Tsai-ICCAD25.pdf)

**Fields:** problem

method_or_artifact

**Location:** Abstract; Sections V–VI

**Fields:** workload_or_benchmark

hardware_or_process_assumptions

baselines

limits

**Location:** Sections VI.A–D; visually checked Table IV and Figures 14–16 PDF page 8; iccad/data/capacitance-ml-primary-recovery-v1.json

#### Additional source assessment

This separately recorded check is dated 2026-09-06. It supplements the original record above and retains its own scope and uncertainty.

[Assessment record](../../iccad/data/capacitance-ml-primary-recovery-v1.json)

[Assessed source](https://gtcad.gatech.edu/www/papers/Tsai-ICCAD25.pdf)

**Extraction scope**

Sections V–VI; Table IV and Figures 14–16 visually checked on PDF page 8.

**Conditions**

94 imec N2 predictive-PDK cells; M0 training thicknesses 22–58nm step 6; testing 18–62nm step 2. Dual Intel 6454S, 89 training threads. Per-cell pattern/inference times 0.082/0.803 seconds exclude database construction and tuning.

**Headline metric status**

withheld_pending_holdout_and_amortization_review

**Independent review status**

pending

## What remains to establish

Resolve unspecified workloads, comparison methods, resource budgets, and source locations before generalizing a reported gain. This subject is represented by one paper and supports a case study, not evidence of recurrence or a long-term trend.

[All subthemes](../expanded-taxonomy-v1.md) · [Research directions](../directions/README.md)
