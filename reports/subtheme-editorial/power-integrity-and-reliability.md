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
