# Device modeling and simulation

This subject has 2 records in the selected sample. This page explains where it fits, then presents all captured paper evidence without shortening the measurements or limitations.

[Definitions used in the paper records](../reading-guide-v1.md)

## Understand the parent subject first

- [Analog mixed signal and emerging devices](../themes/analog-mixed-signal-and-emerging-devices.md)

## Device equations and circuit behavior are different levels

A device model describes electrical behavior within or at the terminals of a component. A circuit model connects components and determines how their voltages and currents interact. This grouping contains one learned semiconductor-device solver and one learned circuit simulator. Their input variables, outputs, and acceptable errors should not be assumed identical.

Conventional numerical simulation approximates equations on a finite representation and solves them to a chosen tolerance. A learned surrogate instead represents a solution or input-output relationship with a trained model. A surrogate can be fast to evaluate, but its preparation and validation are part of the method's cost.

Accuracy also has several meanings. A small equation residual means that a candidate approximately satisfies the equations where or how they were checked. A small prediction error means agreement with selected reference outputs. Agreement with a physical device requires calibrated equations or measurements. These are related checks, not substitutes for each other.

## Weak-form learning: enforce equations through integrals

A strong-form equation states a local relationship involving a field and its derivatives. A weak form expresses the relationship through integrals against selected test functions. This can change which derivatives must be evaluated and how errors are penalized. The test functions and numerical integration determine which violations the training process can detect.

An integral constraint is not simply a claim that the average answer is correct. With appropriate mathematical conditions and a sufficiently rich set of tests, weak and strong formulations can describe the same problem. A finite trained implementation still needs checks: a small collection of integral tests can miss localized error or fail to resolve a sharp change.

[WF-PINN](../observed-subthemes/device-modeling-and-simulation.md#paper-dac-2026-research2346) trains from physical laws and Dirichlet boundary conditions without internal labeled solution data. Dirichlet conditions prescribe the value of the solution at specified boundaries. The official description reports FinFET simulation with solution errors below 5.36×10⁻² and inference 2.16×10⁴ times faster than TCAD. It does not define the error normalization or expose training cost, solver settings, hardware, or tested geometries. The error must not be rewritten as 5.36% without that definition, and inference speed must not become total workflow speed. [Official WF-PINN description](https://63dac.conference-program.com/presentation/?id=RESEARCH2346&sess=sess312).

Self-supervision removes a particular labeling requirement; it does not remove the need for correct material parameters, boundary conditions, or independent evaluation. A useful test would compare terminal currents and relevant internal fields across operating points, including regions where the numerical solution changes rapidly. It should state whether each new geometry or bias condition requires retraining.

<span id="explanation-dac-2026-research2346"></span>

## WF-PINN: removing interior labels is not the same as validating a device solver

TCAD solves coupled semiconductor equations over a device geometry and operating condition. Depending on the device and regime, the relevant fields can include electrostatic potential, carrier concentrations, current density and temperature. A surrogate is useful only if it preserves the quantities needed for a device decision, not merely an aggregate residual or a visually plausible field.

WF-PINN is described as a self-supervised weak-form physics-informed neural network for FinFET simulation. Instead of requiring labeled solution values at interior mesh points, it trains against integral forms of the physical laws and Dirichlet boundary conditions. This removes one expensive source of training labels; it does not remove the need to specify material parameters, geometry, contacts, interface conditions, bias conditions, test functions, quadrature and solver tolerances. Weak-form averaging can also hide a localized violation near a junction, interface or high-field region.

The first gate is equation and boundary fidelity. State the coupled equations, variables, units, material and mobility models, contact conditions, fixed-value boundaries, test-function family, integration mesh and loss weights. Check residuals locally and by integral region, conservation, boundary mismatch, interface continuity and convergence against a trusted TCAD solver. Report terminal current, charge, potential, field and other decision-relevant quantities across bias, geometry, temperature and process conditions; do not translate an undefined solution error of 5.36×10⁻² into 5.36%.

The second gate is transfer and total cost. Hold out device geometries, mesh resolutions, doping/material parameters and operating regimes rather than only sampling nearby points. Report failed or unstable rollouts, training time, data preparation, retraining for a new geometry or bias range, inference hardware and precision. Compare with TCAD and strong-form PINNs under the same accuracy boundary and include the cost of independently checking selected predictions. A 2.16×10⁴ inference-speed ratio is a statement about one inference boundary versus one TCAD solve; it is not automatically end-to-end simulation speed or design-flow speedup.

The official description reports FinFET solution errors below 5.36×10⁻² and inference 2.16×10⁴ times faster than TCAD. It does not expose the error normalization, equation set, geometry and bias matrix, mesh, material/process calibration, convergence behavior, training cost, hardware or downstream device-design result. The evidence supports a weak-form self-supervised device-simulation direction that may reduce reliance on interior labels, not demonstrated calibrated device-model accuracy, universal geometry transfer or a TCAD-replacing workflow.

## IGNITE: use a few examples to condition a pretrained predictor

In-context adaptation supplies examples as inputs to an already trained model. It differs from updating the model's stored parameters through another training run. It can reduce adaptation work, but the examples still need to be obtained, and the model can still fail on unfamiliar circuits.

[IGNITE](../observed-subthemes/device-modeling-and-simulation.md#paper-dac-2026-research1420) combines a self-supervised circuit-topology encoder with a Prior-data Fitted Network decoder. Its official description uses a small context set for a forward prediction pass and an information-based strategy for selecting samples. It reports R² above 0.9 with 95 samples on average, calling this a 15.8× improvement over the comparator. It separately reports 2–30× faster transistor sizing and more than 5× faster yield optimization. These are distinct sample-efficiency and application results, not factors to multiply. [Official IGNITE description](https://63dac.conference-program.com/presentation/?id=RESEARCH1420&sess=sess117).

R² compares squared prediction error with the variation in reference outputs around their mean. A value above 0.9 is not a guarantee that every output has less than 10% error. It can coexist with a large error on a rare but important condition. For a design optimizer, those conditions can determine whether a circuit meets a specification.

The description does not identify the complete output set, pretraining data, topology split, reference simulator tolerances, or accounting for context acquisition. Its cross-topology and cross-technology claims need checks that related circuits or evaluation conditions were not already available during training. The older captured card mentions transient analysis, but the refreshed description does not establish waveform-level prediction; that scope remains unresolved.

<span id="explanation-dac-2026-research1420"></span>

## IGNITE: conditioning a pretrained circuit surrogate is not the same as replacing SPICE

Circuit simulation evaluates a circuit's equations under a topology, device model, parameter set and operating condition. A neural simulator tries to approximate some of those outputs so that an optimizer can explore more candidates per unit time. For the approximation to be useful, it must preserve the outputs and constraints that drive the design decision—not merely achieve a high average fit score.

IGNITE is described as a pretrained model with a self-supervised circuit-topology encoder and a Prior-data Fitted Network decoder. Its two-stage in-context learning supplies a small context set to a single forward pass for a new circuit, while an information-theoretic active-learning strategy chooses which simulator samples to obtain. This attacks three costs separately: topology representation, per-circuit adaptation and context-data efficiency. It does not remove the cost of generating the context, guarantee behavior outside the topology families seen in pretraining, or establish that the predicted waveform/operating point satisfies circuit equations.

The first gate is simulator fidelity. Define the predicted quantities, units, time or frequency domain, device/process models, parameter and bias ranges, precision, reference-solver tolerances and convergence policy. Compare voltage, current, waveform, operating-point and derived-specification errors against a trusted SPICE-like solver on held-out circuits and operating conditions. Report absolute and worst-case errors, phase/timing behavior, corner cases, unstable predictions, physical-constraint violations and uncertainty. R2 above 0.9 can coexist with a large error on a rare but specification-critical condition.

The second gate is transfer and context accounting. A new circuit may require context simulations, topology encoding, sample selection and model inference before it can be used by an optimizer. Separate pretraining and reusable preparation from per-circuit work, count every reference simulation selected by active learning, and hold out topology families and technology nodes—not merely random parameter points. Test unseen device combinations, operating regimes and circuit scales, and report where the model refuses, extrapolates or needs more context.

The third gate is design-flow validity. Transistor sizing and yield optimization consume surrogate predictions to choose candidate designs. Re-simulate selected solutions with the reference solver and report specification success, yield definition, invalid-candidate rate, constraint violations, Pareto tradeoffs and total campaign cost. A fast surrogate can accelerate the wrong search if its error changes ranking near a constraint boundary; the optimization speedup must include context construction, candidate verification and any repair or retraining.

The reported quantities must remain separate: R2 > 0.9 with 95 samples on average is a fit/sample-efficiency claim, 15.8x is reported relative sample efficiency, 2–30x is transistor-sizing speedup, and more than 5x is yield-optimization speedup. They are not factors to multiply, and none is automatically a SPICE-equivalent accuracy or end-to-end design-flow result. The official description does not expose waveform error, topology/node split, solver settings, absolute runtime, context cost, uncertainty, energy or independently re-simulated optimization quality. The evidence supports an in-context graph-aware circuit-surrogate direction, not demonstrated calibrated circuit-simulation replacement or universally valid design optimization.

## Check the decision made with the model

A predictor used for optimization should be judged on the resulting design as well as its average fit. An optimizer may select a point precisely because the model is overly optimistic there. Re-evaluate selected candidates with the reference method and compare both successful and rejected designs. For yield optimization, inspect how uncertainty and rare failures are represented, rather than treating high average prediction quality as sufficient.

Runtime comparisons need a common start and finish. Include required data generation, training or pretraining, context selection, adaptation, model evaluation, and independent final checks. Reusable preparation can be amortized over many queries, but the number of queries must be stated. One fast prediction and a complete device or circuit design campaign are different workloads.

## Shared direction and source limits

My synthesis is that the two studies reduce different dependencies: WF-PINN reduces reliance on interior labeled solutions, while IGNITE reduces per-circuit online retraining. Neither establishes a universal replacement for calibrated device or circuit simulation.

The official descriptions were refreshed on 2026-09-07 and provide results absent from the older cards below. No full manuscript was recovered here, so equation choices, per-case errors, and complete cost comparisons still lack page-level verification. The explanations identify those missing conditions rather than supplying imagined ones. Broader adoption over time also remains a hypothesis until comparable editions are analyzed.

## Compare the results carefully

First identify the inputs and required output quality. Then identify the limited resource: time, memory, communication, energy, circuit area, or correctness coverage. Ask which part of the method reduces that cost and which new cost it adds. Compare numbers only when the experiments hold these conditions sufficiently similar.

A conference description may explain the proposal while omitting the full experiment. An author preprint link may have been coded from its abstract. The source classification does not by itself establish that every table was read. Missing locations remain visible below.

## Complete captured evidence

These are evidence records, not substitutes for the explanations above. Each record preserves its problem, proposed method, measurements, comparison conditions, and source limits. A populated record does not establish that its mechanism has been fully explained or independently verified.

<span id="paper-dac-2026-research2346"></span>

### Weak-Form Physics-Informed Neural Network for Self-Supervised Learning in Semiconductor Device Simulation

DAC 2026 · Record: `dac-2026-research2346`

[Read the step-by-step explanation](#explanation-dac-2026-research2346)

**Updated source-backed reading card**

Reviewed 2026-09-09. Deepens the WF-PINN treatment into a paper-level reading; separates weak-form self-supervised residual fitting from equation and boundary fidelity, local solution error, TCAD calibration, geometry/regime transfer and total simulation cost, while preserving the reported FinFET error and inference-speed claims without converting an undefined error into a percentage.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

TCAD simulation of semiconductor devices is expensive, and supervised surrogate models require many labeled interior solution fields from those slow numerical solves.

**Mechanism / artifact:**

Weak-form PINN with self-supervised physical residual training for FinFET simulation, using integral-form equations and Dirichlet boundary conditions rather than internal labeled solution data; equation set, test functions, quadrature, loss weights, material models and training procedure are unspecified.

**Workload — the work tested:**

FinFET semiconductor-device simulations and physical characteristics; geometry, mesh, contacts, doping/material parameters, bias and temperature ranges, outputs, TCAD solver, train/test conditions and held-out geometries are unspecified.

**Hardware and manufacturing assumptions:**

Technology computer-aided design flow for semiconductor devices with process- and material-dependent equations; device node, PDK/material calibration, mobility/recombination models, numerical solver, mesh, compute hardware, precision and operating conditions are unspecified.

**Baseline — the comparison method:**

TCAD numerical solver

Strong-form PINN

Labeled neural surrogate

Same device geometries, equations, material/process parameters, mesh, boundary/bias conditions, tolerances, hardware, precision and total training/inference/checking boundary are unspecified

**Reported measurements:**

The official description reports all solution errors below 5.36×10^(−2) for FinFET simulation and inference 2.16×10^4 times faster than TCAD; it does not define the error normalization, error locations/fields, convergence, training cost, geometry/regime split or end-to-end workflow boundary.

**Limits on the conclusion:**

Weak-form integral agreement can hide local violations near junctions, interfaces, contacts or high-field regions. State the coupled equations, variables, units, material and mobility models, Dirichlet conditions, test functions, integration mesh and loss weights; check local and regional residuals, conservation, boundary mismatch, interface continuity and convergence against trusted TCAD.

Validate terminal current, charge, potential, electric field and other decision-relevant outputs across bias, temperature, geometry, mesh, doping/material and process conditions. Hold out geometries and operating regimes, report unstable or failed cases, and state whether each new device or bias range requires retraining. An undefined solution error of 5.36×10^(−2) must not be rewritten as 5.36%.

The official description reports FinFET errors below 5.36×10^(−2) and 2.16×10^4 inference speedup, but omits error definition, equation/material calibration, geometry and bias matrix, convergence, training cost, hardware and downstream design result. The evidence supports weak-form self-supervised device simulation that may reduce reliance on interior labels, not demonstrated calibrated device-model accuracy, universal geometry transfer or a TCAD-replacing workflow.

**Source and location**

Evidence tier: Primary captured official DAC description plus existing authored chapter discussion; no full paper extraction, calibrated equation audit, held out geometry/regime matrix or reproduced tcad workflow. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH2346&sess=sess167)

DAC 2026 official description; existing device-modeling-and-simulation chapter discussion; captured Problem, Mechanism / artifact, Workload, Hardware, Baseline, Measurements and Limits fields; no manuscript pages, mesh/material matrix, reproduced TCAD comparison or independent device validation.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** TCAD numerical solver

strong-form PINN

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH2346

**Hardware or process assumptions:** Semiconductor device simulation with material and boundary models; device types and process parameters are unspecified.

**Limits:** No residual error, runtime, convergence, geometry transfer, or device results are reported.

Weak-form choices can hide local violations.

Official description only; calibrated TCAD comparison is required.

**Method or artifact:** Weak-form PINN with self-supervised physical residual training.

**Metrics:** Simulation speed and physical fidelity are claimed qualitatively

**Problem:** Device simulation requires costly labeled solutions and can be difficult across geometries and operating regimes.

**Workload or benchmark:** Semiconductor device equations and geometries; solver, mesh, and calibration baselines are unspecified.

</details>

<span id="paper-dac-2026-research1420"></span>

### IGNITE: An Inquisitive and Graph-Aware Neural Circuit Simulator with Two-Stage Enhanced In-Context Learning

DAC 2026 · Record: `dac-2026-research1420`

[Read the step-by-step explanation](#explanation-dac-2026-research1420)

**Updated source-backed reading card**

Reviewed 2026-09-09. Deepens the IGNITE treatment into a paper-level reading; separates topology encoding, prior-data fitted decoding, in-context adaptation and active sampling from SPICE-equivalent waveform correctness, extrapolation, numerical stability, context cost and optimizer/design validity, while preserving the R2, 95-sample, 15.8x, 2-30x and >5x claims.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Neural circuit simulators seek to reduce the cost of repeated SPICE analyses, but per-circuit tuning, cold starts across circuit topologies and online retraining can erase the benefit; a useful surrogate must represent graph structure and adapt to a new circuit from a small, informative context set.

**Mechanism / artifact:**

IGNITE: a pretrained neural circuit simulator with a self-supervised circuit-topology encoder and Prior-data Fitted Network decoder; two-stage in-context learning conditions a single forward pass on a small context set, and information-theoretic active learning selects samples. Output representation, circuit equations, context/adaptation protocol, uncertainty, numerical constraints, solver coupling and optimizer interface are unspecified.

**Workload — the work tested:**

Analog circuit simulation and optimization across circuit topologies and technology nodes, including transistor sizing and yield optimization; device types, topology families, netlist/parameter distributions, waveform or operating-point outputs, SPICE settings, sample budgets, train/context/test split, yield definition and optimization objectives are unspecified.

**Hardware and manufacturing assumptions:**

Neural circuit-simulation workflow coupled to a SPICE-like reference and analog design optimization; process technology, device models, simulator/version/tolerances, numerical precision, inference hardware, data-generation cost, context acquisition and design-rule/yield evaluation flow are unspecified.

**Baseline — the comparison method:**

SPICE-like numerical simulation

Per-circuit tuned neural surrogate

Topology-agnostic neural surrogate

Existing state-of-the-art context/sample-efficient method

Same circuits, technology nodes, reference-solver tolerances, output targets, context/sample budget, optimization objective, hardware and end-to-end timing boundary are unspecified

**Reported measurements:**

The official description reports R2 > 0.9 with 95 samples on average, described as a 15.8x improvement over SOTA, 2–30x speedup for transistor sizing and more than 5x speedup for yield optimization; it reports no voltage/current/waveform error, convergence, worst-case error, uncertainty, topology/node-transfer result, absolute runtime, context cost, energy or yield-quality outcome.

**Limits on the conclusion:**

R2 is an aggregate fit statistic and does not establish SPICE-equivalent behavior for every voltage, current, transient, corner or topology. Define the predicted outputs and units, compare waveforms/operating points and derived specifications with a trusted solver, report absolute and worst-case error, convergence failures, physical constraints, uncertainty and rare operating conditions. A fast forward pass can still produce a wrong design decision.

In-context learning moves adaptation into the context set rather than eliminating its cost. Count context generation, information-based selection, simulator evaluations, preprocessing, model inference and any independent verification; test unseen topology families and technology nodes with strict train/context/test separation. A cross-topology claim is not established if related circuits or process conditions were present during pretraining.

Optimization speedups require the optimizer to receive sufficiently accurate, stable and constraint-respecting predictions. Re-run selected transistor-sizing and yield-optimization solutions with the reference solver, report specification success, yield definition, invalid-candidate rate, constraint violations, Pareto tradeoffs and total campaign cost. The source reports R2 > 0.9, 95 samples, 15.8x sample efficiency, 2–30x sizing speedup and >5x yield-optimization speedup, but the evidence supports an in-context neural surrogate direction, not demonstrated calibrated circuit-simulation replacement or universally valid design optimization.

**Source and location**

Evidence tier: Primary captured official DAC description plus existing authored circuit simulation discussion; no full paper extraction, reproduced reference solver comparison, cross topology/technology audit or independent design flow validation. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH1420&sess=sess117)

DAC 2026 official description; existing device-modeling-and-simulation chapter discussion; captured Problem, Mechanism / artifact, Workload, Hardware, Baseline, Measurements and Limits fields; no manuscript pages, waveform comparison, topology/node split, context trace or independently re-simulated optimization result.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** SPICE-like numerical simulation

topology-agnostic neural surrogate

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH1420

**Hardware or process assumptions:** Circuit simulation with topology and parameter features; process and solver assumptions are unspecified.

**Limits:** No voltage/current error, convergence, runtime, transfer, or circuit-scale results are reported.

In-context adaptation may fail outside training topology families.

Official description only; calibrated circuit simulation is required.

**Method or artifact:** Graph-aware neural circuit simulator with enhanced in-context learning.

**Metrics:** Simulation speed and fidelity are claimed qualitatively

**Problem:** Circuit simulation is expensive, and learned surrogates must reason over topology and extrapolate across circuits.

**Workload or benchmark:** Analog/digital circuit graphs and transient analyses; devices, datasets, and baselines are unspecified.

</details>

## What remains to establish

Resolve unspecified workloads, comparison methods, resource budgets, and source locations before generalizing a reported gain. Multiple papers in this selected sample permit comparison of mechanisms, but do not by themselves establish recurrence across years or a long-term trend.

[All subthemes](../expanded-taxonomy-v1.md) · [Research directions](../directions/README.md)
