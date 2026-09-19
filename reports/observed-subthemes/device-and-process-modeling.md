# Device and process modeling

This subject has 1 record in the selected sample. This page explains where it fits, then presents all captured paper evidence without shortening the measurements or limitations.

[Definitions used in the paper records](../reading-guide-v1.md)

## Understand the parent subject first

- [Physical design and manufacturing](../themes/physical-design-and-manufacturing.md)

## A compact model trades detail for repeated use

A detailed physical calculation can be too expensive to repeat for every candidate circuit or process choice. A compact model represents selected behavior with a smaller set of equations or computational steps. Its purpose is to make repeated analysis practical while preserving the behavior relevant to the intended decision.

The selected paper, [Physics-Prior Neural-to-Symbolic Compact Modeling](../observed-subthemes/device-and-process-modeling.md#paper-dac-2026-research2336), proposes distilling neural models into symbolic models for back-end-of-line-compatible design–technology co-optimization. Back end of line refers to the fabrication stages forming interconnect structures after the underlying devices. Design–technology co-optimization examines circuit or design choices together with technology assumptions.

The captured record does not identify the modeled device or interconnect quantity, materials, or process range. Its broad title must not be expanded into a particular transistor model or fabrication demonstration.

## Neural and symbolic models expose different information

A neural model predicts outputs through learned numerical operations. A symbolic model expresses a relationship through explicit mathematical expressions. An explicit expression can make evaluation or inspection easier, but being readable does not make it physically correct.

Distillation transfers behavior from one model into another representation. Here the source describes a neural-to-symbolic process using EKAN. It does not explain that method's architecture, fitting objective, or expression-selection rules. The acronym should therefore remain a named method rather than receiving an invented expansion or implementation description.

There are at least two distinct fidelity questions. Does the symbolic model reproduce the neural model? And does either reproduce the relevant physical reference? Close agreement between the two models answers only the first question if the neural model itself has unverified errors.

## Physical priors limit some choices, not every error

A physical prior introduces knowledge about the expected form or behavior of a model. It can help avoid implausible predictions, particularly where observations are limited. Its scope depends on which relationships are actually encoded and how strictly they are enforced.

The source does not identify the priors or provide residual violations. It would be unjustified to claim conservation, correct limiting behavior, or reliable extrapolation simply because the title says physics-prior. Each such property needs its own specification and check.

A constrained symbolic expression can also lose detail represented by the original model. That is a possible approximation tradeoff, not evidence that this framework actually suffers a particular loss. Evaluation must show the resulting errors over the conditions that matter.

## A model's valid range belongs with its equations

Inputs can include geometry, material parameters, or operating conditions, depending on the task. A model fitted within one range may not remain useful outside it. Testing new combinations inside the fitted range is different from testing new materials or process regimes.

The captured description provides no dataset, split procedure, process range, prediction error, or extrapolation results. It therefore does not establish transfer across technologies or calibration against measured silicon. A symbolic expression that can be evaluated at an arbitrary input does not establish that the output is meaningful there.

For use in a larger simulator, further properties can matter, including smoothness and numerical behavior where the simulator evaluates or differentiates the model. The record does not specify such integration or demonstrate complete simulator execution.

## Judge the model through the decision it supports

Design–technology exploration uses predictions to choose among candidates. A small average error can still misrank close alternatives or miss a violated constraint. Validation should therefore include whether decisions selected using the compact model remain acceptable under a trusted reference analysis.

Runtime must include the relevant model-building costs as well as repeated evaluation. Neural training and symbolic distillation may be paid once and reused, but that reuse depends on the model's valid scope. The source supplies no construction time, evaluation time, or amortized exploration results.

<span id="explanation-dac-2026-research2336"></span>

## Physics-prior neural-to-symbolic modeling: readable equations still need physical validation

### A compact model replaces repeated expensive evaluation

A detailed device or interconnect calculation may solve many coupled physical quantities for one geometry and operating condition. Design–technology co-optimization needs to evaluate many candidate geometries, materials, or circuit choices. A compact model approximates the relation between inputs and outputs so that this evaluation can be repeated more cheaply.

The inputs might include geometry, material properties, temperature, voltage, frequency or process parameters, and the output might be a delay, capacitance, resistance, current or another device quantity. The paper's captured description does not identify which quantity is modeled, so no specific device equation is attributed to it. The central requirement is that the compact model preserve the part of the physical relation that changes the design decision.

### Distillation has two different fidelity targets

A neural model can represent a complicated relation through learned numerical operations. A symbolic model expresses a relation as explicit functions and parameters. Distilling one into the other can improve inspection or evaluation cost, but it creates two separate tests. The symbolic expression may reproduce the neural model, while both may still disagree with a trusted physical simulator or measurement.

The description names EKAN as the neural-to-symbolic method but does not expose its architecture, fitting objective, expression grammar, selection rule or stopping criterion. “Physics-prior” also does not identify which physical laws are encoded, how strongly they are enforced, or what residual violations remain. An expression that looks physically plausible can still have the wrong scale, wrong limiting behavior or invalid dependence on an unobserved variable.

### Validity is a region, not a property of the expression alone

Every fitted model has a domain: the geometries, materials, process conditions and operating range represented during construction and validation. Interpolation within that domain is different from extrapolation to a new material, dimension or process node. A symbolic expression can be evaluated outside its training range because the mathematics permits the input; that does not show that the prediction is physically meaningful there.

The model also has to behave well when embedded in a larger optimizer or simulator. If the downstream tool differentiates the model, discontinuities or unstable derivatives can change the search. If a design decision depends on a small difference between candidates, an average prediction error can be less informative than ranking errors near a constraint boundary.

### The downstream design decision is the strongest test

The useful question is not only whether the symbolic model has a low prediction error. It is whether designs selected using the compact model remain acceptable when evaluated with a trusted physical reference. A complete comparison should report model construction, neural training, symbolic distillation, repeated evaluation, reference simulation, failed candidates and any amortization across designs.

The stored record names a neural compact model and a traditional analytical model as comparison categories, but gives no process range, dataset, split, prediction error, extrapolation result, runtime, or silicon correlation. These are not minor omissions: they determine whether the model is a usable DTCO component or only a representation of a particular training set.

### What the paper establishes and what remains open

The accessible description establishes a proposed physics-prior neural-to-symbolic compact-model flow for BEOL-compatible DTCO using EKAN. It does not establish the modeled physical quantity, physical-law guarantees, process transfer, measured-silicon agreement, downstream design improvement, or symbolic-model superiority. A stronger evaluation would publish inputs/outputs, materials and geometry, priors, expression form, training and distillation budget, process range, train/test split, physical reference, error and ranking metrics, extrapolation tests, simulator integration and design-level outcomes.

[Official DAC description, record RESEARCH2336](https://63dac.conference-program.com/presentation/?id=RESEARCH2336&sess=sess109)
The paper motivates combining physical knowledge with explicit learned expressions for efficient design analysis. The current official description supports that methodological direction, not a verified physical model, a measured process improvement, or a general claim that symbolic models are superior. Those conclusions require calibrated references, declared validity ranges, reproducible model construction, and downstream decision checks.

## Compare the results carefully

First identify the inputs and required output quality. Then identify the limited resource: time, memory, communication, energy, circuit area, or correctness coverage. Ask which part of the method reduces that cost and which new cost it adds. Compare numbers only when the experiments hold these conditions sufficiently similar.

A conference description may explain the proposal while omitting the full experiment. An author preprint link may have been coded from its abstract. The source classification does not by itself establish that every table was read. Missing locations remain visible below.

## Complete captured evidence

These are evidence records, not substitutes for the explanations above. Each record preserves its problem, proposed method, measurements, comparison conditions, and source limits. A populated record does not establish that its mechanism has been fully explained or independently verified.

<span id="paper-dac-2026-research2336"></span>

### A Physics-Prior Intelligent Compact Modeling Framework for BEOL-Compatible DTCO: EKAN-Based Distillation from Neural to Symbolic Models

DAC 2026 · Record: `dac-2026-research2336`

[Read the step-by-step explanation](#explanation-dac-2026-research2336)

**Updated source-backed reading card**

Reviewed 2026-09-08. Deepens the official-description reading; separates neural-versus-physical fidelity, physics-prior scope, validity range, downstream decision quality and missing process validation.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Compact models for BEOL-compatible design–technology co-optimization need efficient repeated evaluation while preserving the physical behavior relevant to design decisions.

**Mechanism / artifact:**

Physics-prior neural-to-symbolic compact-model distillation using EKAN.

**Workload — the work tested:**

BEOL-compatible device or interconnect modeling; modeled quantity, inputs/outputs, materials, geometries, process range, reference simulator and dataset are unspecified.

**Hardware and manufacturing assumptions:**

Back-end-of-line process and DTCO simulation flow; technology node, rules, operating corners, calibration conditions and silicon correlation are unspecified.

**Baseline — the comparison method:**

Neural compact model

Traditional analytical model

**Reported measurements:**

Compact-model efficiency and physical plausibility are claimed qualitatively; no prediction error, ranking error, extrapolation, runtime, amortization or process-correlation result is reported.

**Limits on the conclusion:**

Agreement between symbolic and neural models does not establish agreement with a trusted physical reference.

The source does not identify the encoded priors, EKAN architecture, fitting objective, expression grammar, validity range or residual violations; a readable expression is not a physical guarantee.

Official description only; process-calibrated validation, simulator integration and design-level decision checks were not performed.

**Source and location**

Evidence tier: Official DAC description; full manuscript and reproduction not performed. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH2336&sess=sess109)

DAC official description, Captured Description and Authors fields; record RESEARCH2336; no manuscript pages.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** neural compact model

traditional analytical model

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH2336

**Hardware or process assumptions:** Back-end-of-line process and DTCO simulation flow; material and geometry assumptions are unspecified.

**Limits:** No prediction error, extrapolation, runtime, process range, or silicon correlation results are reported.

Symbolic distillation may constrain expressivity.

Official description only; process-calibrated validation is required.

**Method or artifact:** Physics-prior neural-to-symbolic compact-model distillation using EKAN.

**Metrics:** Compact-model efficiency is claimed qualitatively

**Problem:** Compact models for BEOL-compatible DTCO need physical plausibility, interpretability, and efficient evaluation.

**Workload or benchmark:** BEOL-compatible device or interconnect models; process data, nodes, and reference simulators are unspecified.

</details>

## What remains to establish

Resolve unspecified workloads, comparison methods, resource budgets, and source locations before generalizing a reported gain. This subject is represented by one paper and supports a case study, not evidence of recurrence or a long-term trend.

[All subthemes](../expanded-taxonomy-v1.md) · [Research directions](../directions/README.md)
