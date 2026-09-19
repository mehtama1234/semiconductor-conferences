# Power integrity and reliability

This subject has 1 record in the selected sample. This page explains where it fits, then presents all captured paper evidence without shortening the measurements or limitations.

[Definitions used in the paper records](../reading-guide-v1.md)

## Understand the parent subject first

- [Power reliability and security](../themes/power-reliability-and-security.md)

## Supplying voltage and preserving wires are related problems

A chip's power grid distributes current through conductors with nonzero resistance. Current through that resistance produces a voltage difference, commonly called IR drop. The voltage available locally can therefore differ from the source voltage. A static analysis evaluates a specified load condition; it is not a complete account of every time-varying supply disturbance. [OpenROAD's IR-drop analysis documentation](https://openroad.readthedocs.io/en/latest/main/src/psm/README.html) illustrates how even the modeled locations of power sources are part of this analysis.

Electromigration concerns changes in interconnect material under electrical and other driving forces. Its modeling can involve electrical conditions, temperature, and mechanical stress. [COMSOL's electromigration explanation](https://www.comsol.com/blogs/modeling-electromigration-in-comsol-multiphysics/) describes this coupled physical problem. Predicting voltage and predicting material stress are thus related, but they remain different outputs with different units and acceptance criteria.

The single selected paper, [GEMIR](../observed-subthemes/power-integrity-and-reliability.md#paper-dac-2026-research046), learns both quantities from a power-grid graph.

## Why use one graph for two predictions?

A graph represents the grid as nodes and connections. Node quantities can describe local voltage, while connection quantities can describe properties of a conductor segment. Both depend on the same network structure and electrical loading. Learning them jointly can potentially reuse information that separate predictors would have to obtain independently.

GEMIR predicts static IR drop at nodes and electromigration stress at edges. The official description identifies attention across layers and between node and edge information. Attention is a learned weighting of available information; the short source does not expose the exact features or update equations. The proposed representation should therefore not be expanded into a specific implementation beyond those recorded details.

The important engineering question is whether shared information improves both predictions on new grids and conditions. A model can improve one task while harming another, especially when the training objectives favor different changes to shared parameters.

## Physical constraints and multitask training

The source names constraints based on Kirchhoff's current law and the Korhonen partial differential equation. Kirchhoff's current law expresses current balance at a node under the modeled conditions. The named stress equation describes spatial and temporal stress evolution under its physical assumptions. Including these relationships in training can discourage certain inconsistent predictions.

That does not automatically establish exact satisfaction of the equations or coverage of omitted physical effects. The evaluation needs to state how constraints are enforced, what boundary conditions and material parameters are used, and what violations remain after prediction.

The description also identifies conflict-gated multitask optimization. Its purpose is to manage conflicting training updates from the two prediction tasks. The exact gating rule is absent, so it should not be assumed to guarantee that every update improves both tasks. A useful comparison would isolate the effects of the graph representation, physical constraints, and training rule under matched data and budgets.

## Interpret the reported errors separately

The official description reports a 40.79% reduction in IR-drop mean absolute error and a 19.35% reduction in electromigration-stress root-mean-square error. These are relative reductions in two different error metrics. They are not reductions in actual chip voltage drop or physical stress, and they must not be averaged into a single reliability gain.

The source does not give absolute errors or detailed baseline conditions. Without them, a percentage reduction cannot establish that either prediction is accurate enough near an engineering limit. Mean error can also hide a missed high-drop node or highly stressed segment. Such cases may be more consequential than many small errors elsewhere.

Design sizes, absolute runtime, and the distribution of gains across technologies and workloads are unspecified. The record therefore does not establish faster complete analysis, cross-technology generalization, or measured lifetime improvement.

## From predictions to design decisions

A stronger study would test complete held-out grids, vary load and material assumptions, compare local extremes with trusted reference solutions, and inspect the changes a designer would make using those predictions. Any claimed lifetime result would need a validated connection from stress to failure, not merely a better stress-fitting score.

GEMIR motivates joint modeling where electrical and reliability tasks share physical structure. That is a concrete research direction, not evidence that a single predictor can replace all power-integrity and reliability checks. Its practical value remains conditional on prediction validity, full preparation and execution cost, and the correctness of the decisions made from its outputs.

<span id="explanation-dac-2026-research046"></span>

## GEMIR: joint EM/IR prediction must preserve physical boundaries and signoff-critical tails

IR drop and electromigration stress are related through the power grid but are different physical fields. Static IR drop is a node-level voltage quantity under specified loads and boundary conditions. Electromigration stress is an edge-level reliability quantity involving current, temperature, material and time-dependent behavior. A shared graph representation can reuse structure; it does not make their units, reference models or acceptance thresholds interchangeable.

GEMIR is described as a graph-based multitask predictor with cross-layer node-edge attention, physics-informed constraints for Kirchhoff's current law and the Korhonen PDE, and conflict-gated gradient fusion. The captured description does not specify features, loss weights, boundary conditions, source terms, temperature/material parameters, discretization, gate rule or inference workflow.

The first gate is physical validity. Check KCL residuals and conservation, PDE residuals, boundary conditions, source currents, temperature and material parameters on held-out grids. Compare node and edge extremes with a trusted numerical solver across current/load, geometry, process, temperature and material shifts. A lower average prediction error can still miss the single voltage hotspot or wire segment that controls signoff.

The second gate is decision validity. Report absolute units, mean and tail errors, maxima/percentiles, threshold classification, spatial localization and error correlation separately for IR drop and EM stress. Distinguish prediction quality from decisions such as widening wires or adding vias, and charge graph construction, reference-solver labels, training/inference, calibration and fallback. Test leakage across related layouts and process populations.

The source reports 40.79% lower IR-drop MAE and 19.35% lower EM-stress RMSE, plus computational efficiency and generalization, but gives no absolute errors, design/process matrix, baseline conditions, runtime, threshold violations, lifetime estimate or silicon validation. These claims do not establish signoff-quality power integrity, lifetime improvement or cross-technology transfer. The evidence supports physics-informed joint EM/IR prediction, not replacement of trusted power-integrity and reliability checks.

## Compare the results carefully

First identify the inputs and required output quality. Then identify the limited resource: time, memory, communication, energy, circuit area, or correctness coverage. Ask which part of the method reduces that cost and which new cost it adds. Compare numbers only when the experiments hold these conditions sufficiently similar.

A conference description may explain the proposal while omitting the full experiment. An author preprint link may have been coded from its abstract. The source classification does not by itself establish that every table was read. Missing locations remain visible below.

## Complete captured evidence

These are evidence records, not substitutes for the explanations above. Each record preserves its problem, proposed method, measurements, comparison conditions, and source limits. A populated record does not establish that its mechanism has been fully explained or independently verified.

<span id="paper-dac-2026-research046"></span>

### GEMIR: Graph-Based Joint Modeling of Electromigration and IR Drop for Power Grid

DAC 2026 · Record: `dac-2026-research046`

[Read the step-by-step explanation](#explanation-dac-2026-research046)

**Updated source-backed reading card**

Reviewed 2026-09-09. Deepens the GEMIR treatment into a paper-level reading; separates joint graph prediction, node-edge attention, KCL/Korhonen physics constraints and conflict-gated multitask training from physical boundary validity, tail errors, signoff thresholds, calibration and process transfer, while preserving the 40.79% IR-drop-MAE and 19.35% EM-stress-RMSE source claims as withheld pending full-paper conditions.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Power-grid reliability depends on both node-level voltage loss and edge-level electromigration stress, while numerical analysis is expensive on large designs and separate ML predictors may miss shared structure.

**Mechanism / artifact:**

GEMIR jointly predicts static IR drop at graph nodes and electromigration-induced stress at graph edges using cross-layer node-edge attention, physics-informed constraints incorporating Kirchhoff's current law and the Korhonen PDE, and conflict-gated multitask gradient fusion. Features, loss terms, boundary conditions, gradient gate, training targets and inference workflow are unspecified.

**Workload — the work tested:**

Power-grid analysis on large-scale designs for static IR drop and EM-induced stress; design sizes, technology/process, grid topology, current loads, temperature/material parameters, train/test split, leakage controls, numerical reference solver, PVT/aging conditions and workload population are unspecified.

**Hardware and manufacturing assumptions:**

Power-grid graphs with node voltage and edge stress fields; physical boundary conditions, via/resistance/capacitance models, current sources, thermal coupling, material parameters, process node, signoff tool, compute hardware and fabricated-chip validation are unspecified.

**Baseline — the comparison method:**

Existing numerical power-grid methods

Single-task ML predictors

Multitask ML baselines

Same designs, reference solver, loads, physical parameters, train/test split, error units, runtime hardware and signoff threshold are unspecified

**Reported measurements:**

The source reports 40.79% reduction in IR-drop mean absolute error and 19.35% reduction in electromigration-stress root-mean-square error, plus computational efficiency and generalization; it reports no absolute errors/units, worst-case or tail error, named baseline conditions, design/process distribution, runtime, memory, threshold violations, lifetime prediction or silicon validation.

**Limits on the conclusion:**

KCL and the Korhonen PDE are useful constraints only when boundary conditions, source terms, material parameters, temperature and discretization match the physical problem. Verify residuals and conservation on held-out grids, compare node/edge extremes with a trusted numerical solver and test current/load, temperature, geometry and material shifts; low mean error can hide a signoff-critical hotspot or stressed segment.

IR-drop MAE and EM-stress RMSE are different quantities and cannot be averaged into a reliability gain. Report absolute units, distributions, maxima/percentiles, threshold classification, spatial localization and error correlation; distinguish prediction quality from the downstream decision of widening a wire, adding vias or changing the grid. Measure graph construction, reference-solver labels, training/inference, calibration and any fallback cost.

The 40.79%/19.35% reductions and generalization claim are description-backed with full-paper conditions unresolved. They do not establish signoff-quality power integrity, lifetime improvement, cross-technology transfer or fabricated-chip validity. The evidence supports physics-informed joint EM/IR prediction, not replacement of trusted power-integrity and reliability checks.

**Source and location**

Evidence tier: Primary captured official DAC description plus bounded recovery assessment and existing authored power integrity discussion; full paper not recovered, numerical claims withheld pending conditions, no reproduced physics validation or fabricated chip result. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH046)

DAC 2026 official description; existing power-integrity-and-reliability editorial explanation; selected primary-source recovery assessment; captured Problem, Mechanism / artifact, Workload, Hardware, Baseline, Measurements and Limits fields; no full manuscript, design/process matrix, numerical trace or independent signoff validation.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** high_official_description

**Baselines:** existing numerical methods

single-task machine-learning approaches

multitask baselines

**Evidence locators:** Not established in the captured evidence.

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH046&sess=sess112

**Hardware or process assumptions:** Not established in the captured evidence.

**Limits:** The description does not disclose design sizes, absolute runtime, or the distribution of gains across technologies and workloads.

**Method or artifact:** Graph-based multitask learning with node-edge attention, physics-informed constraints, and conflict-gated gradient fusion.

**Metrics:** 40.79% reduction in IR-drop MAE

19.35% reduction in EM-stress RMSE

computational efficiency and generalization

**Problem:** Separate EM and IR-drop analysis misses their shared physical structure, while numerical methods are expensive on large designs.

**Workload or benchmark:** Power-grid analysis for node-level static IR drop and edge-level electromigration-induced stress.

</details>

#### Additional source assessment

This separately recorded check is dated 2026-09-06. It supplements the original record above and retains its own scope and uncertainty.

[Assessment record](../../dac/data/gemir-primary-recovery-v1.json)

[Assessed source](https://63dac.conference-program.com/presentation/?id=RESEARCH046&sess=sess112)

**Extraction scope**

Official description recheck and bounded primary-source discovery; no full paper recovered

**Interpretation limits**

Description supports a provisional joint-modeling mechanism, not a signoff-quality guarantee.

Reposted material and related patent discovery were not admitted as paper-level technical evidence.

Search non-recovery is not inaccessibility or proof that no full paper exists.

**Headline metric status**

withheld_pending_fullpaper_conditions

**Independent review status**

pending

## What remains to establish

Resolve unspecified workloads, comparison methods, resource budgets, and source locations before generalizing a reported gain. This subject is represented by one paper and supports a case study, not evidence of recurrence or a long-term trend.

[All subthemes](../expanded-taxonomy-v1.md) · [Research directions](../directions/README.md)
