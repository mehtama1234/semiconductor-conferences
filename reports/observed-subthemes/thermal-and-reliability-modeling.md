# Thermal and reliability modeling

This subject has 4 records in the selected sample. This page explains where it fits, then presents all captured paper evidence without shortening the measurements or limitations.

[Definitions used in the paper records](../reading-guide-v1.md)

## Understand the parent subject first

- [Power reliability and security](../themes/power-reliability-and-security.md)

## Four different quantities, four different kinds of evidence

Temperature, mechanical stress, supply-voltage disturbance, and failure rate are related engineering concerns, but they are not interchangeable measurements. Temperature describes thermal state. Stress describes internal mechanical loading. Supply-voltage disturbance describes departure from the voltage intended to power a circuit. Failure rate summarizes failures relative to operating exposure. Predicting one accurately does not automatically validate the others.

The four records grouped here span these distinct tasks. Their shared question is how to make expensive analysis useful during design or operation. Each must still be checked against the physical quantity it predicts and the decision that will use it.

## From heating to mechanical stress

Materials expand as their temperature changes. When connected materials expand differently, or their movement is constrained, thermal expansion can create mechanical stress. A temperature field therefore becomes an input to a structural calculation; temperature alone is not the stress result. Material properties, reference temperature, and mechanical constraints matter. [COMSOL's thermal-stress explanation](https://www.comsol.com/multiphysics/thermal-expansion-and-thermal-stresses) describes this coupling between heat transfer and structural mechanics.

<span id="explanation-dac-2026-research158"></span>

## FP-DDM: neural domain decomposition must preserve the coupled thermal-mechanical solution at interfaces

[FP-DDM](../observed-subthemes/thermal-and-reliability-modeling.md#paper-dac-2026-research158) addresses coupled chip-scale thermal-stress analysis. Domain decomposition divides a large mesh or field into overlapping subdomains that must agree where they meet. This can reduce memory and expose parallel work, but an interface error can affect the assembled solution even when each subdomain looks accurate in isolation. Temperature is an input to stress; it is not itself a stress or reliability result.

The captured method uses a foundation-model architecture, overlapping subdomains, explicit optimization of overlap boundary values by automatic differentiation, and physics-guided test-time adaptation for new physics and domains. The proposal changes how subdomain fields and boundary values are predicted and aligned. It does not specify the PDE residuals, interface loss, optimizer, adaptation budget, mesh representation, material parameters or convergence criterion. A learned field can look smooth while violating flux, traction, displacement or conservation conditions at a material boundary.

The first gate is physical and numerical fidelity. Compare temperature, displacement, strain and stress with a trusted finite-element or other calibrated multi-physics solver under the same geometry, mesh, materials, heat sources, mechanical loads, reference temperature and thermal/mechanical boundary conditions. Report field error norms, interface continuity, flux/traction balance, conservation, residuals, peak stress/temperature error and convergence failures, especially at contacts, sharp gradients and material interfaces. A chip-wide average can conceal the local maximum that drives a reliability decision.

The second gate is scale and transfer accounting. Hold out geometries, materials, loads, boundary conditions and physics rather than only field samples. Separate zero-shot transfer from test-time adaptation, state all unlabeled data and iterations, and report uncertainty and worst-case failures. Include subdomain construction, communication, overlap synchronization, automatic differentiation, memory, inference and adaptation cost; compare with a finite-element solver and standard neural surrogate at matched precision and error tolerance. Layout optimization additionally requires re-solving every proposed design with an independent evaluator and a stated stress/thermal objective.

The official description claims numerical-solver-level accuracy on thermal and stress problems, scaling to 10-billion-cell domains, label-free generalization to new physics and unseen domains, and support for layout optimization. It provides no error definitions, convergence history, mesh/material conditions, runtime, memory, interface residuals or physical calibration. The evidence supports a neural physics-guided domain-decomposition direction, not demonstrated reliability-grade thermal-stress prediction or universal multi-physics transfer.


## Thermal control has timing consequences

<span id="explanation-dac-2026-research2481"></span>

## SCOUT: thermal-aware SRAM allocation must satisfy the deadline over the whole thermal trajectory

[SCOUT](../observed-subthemes/thermal-and-reliability-modeling.md#paper-dac-2026-research2481) allocates on-chip SRAM for real-time neural-network tasks on an Edge TPU. SRAM is memory implemented on the chip; deciding which task uses which memory resources can change where activity occurs, how much data moves, and which banks heat. A thermally favorable allocation can still be unsuitable if a task finishes after its deadline, and a faster allocation can violate a thermal limit later in the schedule.

SCOUT is described as coupling task-level dynamic frequency scaling (DFS) with runtime SRAM reallocation. Its thermal model includes SRAM's thermal impact, while the reallocation technique is intended to mitigate write overhead. The mechanism changes both the frequency policy and the memory state. It must therefore define allocation legality, bank capacity, migration/write protocol, control period, sensor delay, frequency transitions, thermal recovery and behavior when a task cannot be moved without disrupting execution.

The first gate is real-time feasibility. Define task periods, deadlines, execution times, precedence, criticality, arrivals, preemption and SRAM conflicts. Measure every response time and deadline miss under the evolving frequency, memory and temperature state, including DFS transition latency, reallocation, write stalls, queueing and thermal recovery. A claim that more task sets are schedulable needs the task-set generator, feasibility denominator and comparison against capacity-only, thermal-oblivious and DFS-only policies.

The second gate is thermal calibration and energy accounting. Compare predicted and measured temperature at SRAM banks, compute units and package hotspots across workload activity, frequency/voltage, ambient, cooling and task phasing. Include sensor delay, thermal time constants, control stability, SRAM movement/write energy, data traffic, idle power and frequency-transition cost. Package-level effects can invalidate an on-chip thermal model even if its average temperature appears accurate.

The official description reports that SCOUT schedules up to 46% more DNN task sets than prior approaches while adhering to thermal constraints. The captured evidence does not expose task/deadline distributions, deadline misses, temperature trajectories, energy, write overhead, Edge-TPU conditions or package-level validation. It supports joint thermal-aware DFS and SRAM scheduling, not demonstrated real-time guarantees or hardware-validated thermal efficiency.

The evaluation must therefore combine temperature with deadline outcomes, including simultaneous tasks and allocation overhead. Lower average temperature is not enough if one region exceeds its limit. Higher average throughput is not enough if time-critical requests finish late. The available description contains neither temperature results nor deadline-miss rates, and leaves the task set, memory organization, and cooling assumptions unspecified.

## A predicted failure rate needs exposure and calibration

[ATLAS](../observed-subthemes/thermal-and-reliability-modeling.md#paper-dac-2026-research1390) uses graph-based learning for failure-in-time prediction. A graph represents components and their dependencies; a learned model uses that structure along with available features. Its value depends on whether the training labels represent the operating conditions and failure mechanisms of the systems where predictions will be used.

Rare failures make this difficult. A dataset with few observed failures can produce apparently accurate predictions simply because most observations contain no failure. Evaluation should compare predicted failure frequency with observed frequency over sufficient operating exposure, distinguish new systems from reused training systems, and describe uncertainty. The record supplies no calibration, transfer, or rare-event results. It does not justify using the model's output as an established reliability guarantee.

<span id="explanation-dac-2026-research1390"></span>

## ATLAS: a fast calibrated risk estimate is not yet an ISO 26262 safety argument

Failure in time (FIT) is a rate normalized by operating exposure. In a safety-critical circuit, the useful question is not simply whether a model predicts a number close to a label: designers need to know which components or gates are risky, under which failure mechanisms and operating conditions, and whether a mitigation changes the residual risk. ASIL-D requirements make the error boundary consequential, especially when the highest-risk events are rare.

ATLAS is described as a decoupled graph neural network whose bidirectional asynchronous topological message passing mirrors forward and backward propagation in BFIT. It adds two specialized heads: RankNet uses a gap-aware pairwise loss weighted by the log difference in FIT and emphasizes high-risk samples to rank the top-k% gates; CalibNet uses losses in log and linear domains with importance weighting to calibrate the predicted FIT values. This separates two decisions that are often conflated: finding the riskiest gates and estimating how much risk they carry. The claimed O(|V|+|E|) complexity describes graph-message processing; it does not establish correct failure physics or a safe hardening decision.

The first gate is label and mechanism validity. Define the graph nodes and edges, failure modes, FIT units and exposure, operating conditions, censoring, BFIT reference, feature availability and how labels are generated. A graph can encode connectivity while omitting temperature, voltage, aging, process variation, workload activity or a failure mechanism that dominates in deployment. Hold out complete circuits, graph families, technologies and operating conditions—not merely random nodes—and compare predictions with a trusted physics or measured reference. Report error in the relevant tail, uncertainty, calibration curves, ranking precision/recall, top-k recall and missed high-risk gates.

The second gate is the design decision. Selective hardening converts a prediction into added area, timing, power or verification work. Define the risk threshold and top-k budget, hardening primitive, area accounting, false-negative cost and post-hardening reliability evaluation. Recompute or measure the hardened circuit's residual FIT; a lower predicted score or a smaller area than DeepGate2 does not prove that the physical failure probability changed. For a safety claim, document traceability, assumptions, independence of validation data and the failure modes left outside the analysis.

The baselines should include BFIT or another physics-based reference, a static or conventional GNN, and DeepGate2 under the same graphs, labels, data splits, operating conditions, feature budget, top-k risk budget, hardening policy and runtime boundary. Long-tailed data require explicit ablations of log-gap weighting, head-sample emphasis, asynchronous message passing and the dual-domain CalibNet loss. Report training/inference time separately, plus absolute runtime, memory, calibration cost and transfer behavior; a relative speedup can hide preprocessing or reference-model costs.

The official description motivates ASIL-D FIT below 10, reports O(|V|+|E|) complexity, up to 220x speedup over BFIT and 53% lower selective-hardening area overhead than DeepGate2 on ITC'99 benchmarks. It does not expose FIT error, calibration, rare-event behavior, absolute runtime, failure-mechanism coverage, operating conditions, area accounting, cross-technology transfer or hardened-circuit validation. The evidence supports a reliability-aware GNN direction, not demonstrated calibrated FIT prediction or safety-case-ready selective hardening.

## Power integrity is a separate electrical calculation

[PIANO](../observed-subthemes/thermal-and-reliability-modeling.md#paper-dac-2026-research733) proposes a physics-informed admittance neural operator for power-integrity analysis. Admittance expresses the current response to voltage in the modeled network. The engineering question is whether that network supplies acceptable voltage as loads and conditions change. A learned approximation must preserve the behavior relevant to voltage limits, not merely achieve a small average fitting error.

The source does not provide voltage-noise errors, frequency range, geometry-transfer tests, or speed measurements. In particular, the presence of physical constraints during training is a design choice, not evidence that every operating condition is covered.

<span id="explanation-dac-2026-research733"></span>

## PIANO: a learned admittance is useful only when the reduced PDN remains physically valid

DC power-integrity analysis models a power-distribution network (PDN) of resistive elements, sources and current sinks. Kirchhoff's current law produces a large linear system; in a well-formed resistive network the relevant matrix is symmetric positive definite (SPD), so a numerical solver can obtain node or port voltages. The design question is whether the lowest voltage and its margin stay within limits under the loads and geometry being considered, not merely whether a surrogate fits average voltages.

PIANO is described as extracting an equivalent resistive network from a 3D-IC PDN layout, representing it as a graph, using a graph neural network to predict the equivalent port admittance between voltage-source ports and current sinks, and forming a reduced SPD system for a lightweight numerical solve. The method moves much of repeated network evaluation into learned port behavior while retaining a numerical solve. The captured description does not specify graph extraction, port definition, SPD enforcement, physics losses, training domain, solver tolerance, conditioning or fallback.

The first gate is physical and numerical validity. Check symmetry, positive definiteness, passivity, Kirchhoff current balance, boundary conditions and residuals after the predicted matrix is assembled. Compare node/port voltages, current conservation, minimum/maximum droop and constraint violations with a trusted sparse solver. A 1.95% average voltage error can hide a worst-case droop violation, a non-SPD matrix or a large error at the port that drives a design decision.

The second gate is transfer. Hold out PDN geometries, stack/material configurations, port counts and locations, current-sink distributions, package/process corners and unseen layouts. Separate interpolation from extrapolation and report error tails, minimum/maximum voltage error, residual, conditioning, solver iterations and failure/fallback. A surrogate trained on one placement or load pattern may preserve average behavior while missing a local bottleneck or a new current return path.

Speed must include graph extraction, feature construction, GNN inference, matrix assembly and numerical solve. For PI-constrained design-space exploration, include candidate generation, rejected designs, constraints, retraining/calibration and final independent PI checks. Compare the commercial/full numerical solver, direct sparse solving and physics-agnostic surrogates at the same voltage-error tolerance, hardware, preprocessing and end-to-end boundary.

The official description reports 12.6× speedup over commercial simulators with 1.95% voltage error on industrial-scale PDNs, and 17.2× acceleration when integrated into a PI-constrained design-space exploration flow. It does not expose absolute runtime, voltage-error distribution, SPD/residual violations, geometry/load transfer, memory, energy or per-design results. The evidence supports physics-informed admittance learning for DC PI analysis, not demonstrated signoff-grade voltage integrity, broad geometry transfer or universally faster PI-constrained design.

## What a useful combined study would establish

These papers motivate a sequence of explicit checks: validate the predicted physical quantity, quantify its uncertainty, then test the design or operating decision that consumes it. That sequence is a research proposal inferred from the records, not a result they collectively demonstrate. Temperature, stress, voltage, and failure-rate results should remain separate until an experimentally supported connection explains how an error in one affects the final decision.

## Compare the results carefully

First identify the inputs and required output quality. Then identify the limited resource: time, memory, communication, energy, circuit area, or correctness coverage. Ask which part of the method reduces that cost and which new cost it adds. Compare numbers only when the experiments hold these conditions sufficiently similar.

A conference description may explain the proposal while omitting the full experiment. An author preprint link may have been coded from its abstract. The source classification does not by itself establish that every table was read. Missing locations remain visible below.

## Complete captured evidence

These are evidence records, not substitutes for the explanations above. Each record preserves its problem, proposed method, measurements, comparison conditions, and source limits. A populated record does not establish that its mechanism has been fully explained or independently verified.

<span id="paper-dac-2026-research158"></span>

### Neural Domain Decomposition for Scalable Multi-Physics: Chip-Scale Thermal-Stress Analysis

DAC 2026 · Record: `dac-2026-research158`

[Read the step-by-step explanation](#explanation-dac-2026-research158)

**Updated source-backed reading card**

Reviewed 2026-09-08. Deepens the FP-DDM thermal-stress treatment into a paper-level reading; separates neural overlapping-domain decomposition and physics-guided adaptation from PDE/interface fidelity, coupled thermal-mechanical validity, convergence, unseen-domain transfer and physical reliability decisions, while preserving the 10-billion-cell and solver-level-accuracy claims.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Chip-scale coupled thermal and mechanical fields are expensive to solve at high spatial resolution and under complex material and boundary conditions.

**Mechanism / artifact:**

Foundation-model-based physics-guided adaptation for overlapping neural domain decomposition, with explicit optimization of overlap boundary values by automatic differentiation and test-time adaptation to new physics/domains; architecture, PDE residuals, interface loss, optimizer and adaptation budget are unspecified.

**Workload — the work tested:**

Chip-scale thermal and stress problems with multi-physics layouts and domains, claimed to scale to 10-billion-cell domains and support layout design optimization; geometry, mesh, materials, loads, thermal/mechanical boundaries, solver settings, train/test domains and optimization objectives are unspecified.

**Hardware and manufacturing assumptions:**

Multi-physics chip/package analysis and System–Technology Co-Optimization workflow; material properties, process stack, geometry, reference temperature, heat sources, convection/contacts, mechanical constraints, compute hardware, memory and solver implementation are unspecified.

**Baseline — the comparison method:**

Finite-element multi-physics solver

Standard neural surrogate solver

Single-domain neural model

Same mesh, materials, boundary conditions, loads, convergence tolerance, hardware, precision, preprocessing, adaptation budget and output/error boundary are unspecified

**Reported measurements:**

The official description claims numerical-solver-level accuracy on thermal and stress problems, scalability to 10-billion-cell domains, transfer to new physics/unseen domains without labels and support for layout optimization; it supplies no error norms, interface mismatch, convergence, runtime, memory, mesh, transfer or reliability results.

**Limits on the conclusion:**

Overlapping subdomains must satisfy the coupled PDE and interface conditions. Check temperature, displacement, strain and stress continuity, flux/traction balance, conservation, boundary conditions and residuals near material interfaces, contacts and sharp gradients; a low average field error can hide a mechanically important boundary error.

Validate transfer with held-out geometries, materials, loads, physics and boundary conditions, and report adaptation steps, labels or unlabeled data, convergence failures, uncertainty and worst-case errors. Compare against a calibrated finite-element solver at matched mesh/physics/tolerance and include domain decomposition, communication, memory and automatic-differentiation cost.

The 10-billion-cell, solver-level-accuracy, unseen-domain and layout-optimization claims lack error definitions, convergence, mesh/material conditions, runtime/memory, interface residuals and physical calibration. The evidence supports a neural physics-guided domain-decomposition direction, not demonstrated reliability-grade thermal-stress prediction or universal multi-physics transfer.

**Source and location**

Evidence tier: Primary captured official DAC description plus existing authored chapter level explanation; no full paper extraction, mesh/material matrix, interface residual report or physical thermal stress calibration. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH158&sess=sess167)

DAC 2026 official description; existing chapter-level thermal-and-reliability-modeling discussion; captured Problem, Mechanism / artifact, Workload, Hardware, Baseline, Measurements and Limits fields; no manuscript pages or reproduced multi-physics solver comparison.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** finite-element multi-physics solver

standard neural surrogate solver

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH158

**Hardware or process assumptions:** Chip/package multi-physics model; materials, geometry, thermal boundary, and process assumptions are unspecified.

**Limits:** No error, convergence, runtime, mesh-size, or generalization results are reported.

Domain decomposition may fail at sharp material interfaces.

Official description only; reliability claims require calibrated solver comparisons.

**Method or artifact:** Neural domain-decomposition solver for multi-physics thermal-stress analysis.

**Metrics:** Scalability and analysis efficiency are claimed qualitatively

**Problem:** Chip-scale thermal and mechanical fields are expensive to solve at high spatial resolution and under coupled boundary conditions.

**Workload or benchmark:** Chip thermal-stress geometries and boundary conditions; solver baselines, meshes, and accuracy targets are unspecified.

</details>

<span id="paper-dac-2026-research2481"></span>

### SCOUT: Thermal-Aware SRAM Allocation for Real-Time DNN Tasks on Edge TPU

DAC 2026 · Record: `dac-2026-research2481`

[Read the step-by-step explanation](#explanation-dac-2026-research2481)

**Updated source-backed reading card**

Reviewed 2026-09-08. Deepens the SCOUT treatment into a paper-level reading; separates task-level dynamic frequency scaling and runtime SRAM reallocation from thermal-model calibration, deadline feasibility, write overhead, package effects and measured Edge-TPU operation, while preserving the up-to-46% task-set claim.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Real-time DNN accelerators need deadline guarantees, but high computation causes thermal stress; frequency scaling can reduce heat while also reducing performance, and SRAM placement affects both activity and data movement.

**Mechanism / artifact:**

SCOUT couples task-level dynamic frequency scaling with runtime on-chip SRAM reallocation, using a thermal model that includes SRAM's thermal impact and a reallocation technique intended to mitigate write overhead; thermal state estimator, allocation legality, migration protocol, control period and scheduler are unspecified.

**Workload — the work tested:**

Real-time DNN task sets scheduled on Google Edge TPU; models, execution times, periods/deadlines, task criticality, SRAM banks/capacity, thermal traces, arrival patterns, cooling and baseline schedules are unspecified.

**Hardware and manufacturing assumptions:**

Edge TPU with banked on-chip SRAM, task-level DFS and runtime memory reallocation; TPU process/package, thermal sensors, cooling, frequency/voltage states, memory controller, write bandwidth, migration support, power instrumentation and software runtime are unspecified.

**Baseline — the comparison method:**

Capacity-only SRAM allocation

Thermal-oblivious scheduling

DFS without SRAM reallocation

Same DNN task sets, deadlines, TPU frequency/power states, thermal model, SRAM capacity/banks, migration/write cost, cooling and deadline/temperature boundary are unspecified

**Reported measurements:**

The official description reports that SCOUT schedules up to 46% more DNN task sets than prior approaches while adhering to thermal constraints; it supplies no deadline-miss rate, temperature trajectory, energy, area, throughput, write overhead, reallocation count or hardware measurement.

**Limits on the conclusion:**

A task set is feasible only if every execution meets its deadline under the thermal and memory state over time. Report response-time and deadline-miss distributions, task phasing, preemption, frequency transitions, SRAM conflicts, migration/write stalls, queueing and thermal recovery; a larger schedulable-set count needs a defined task-set generator and feasibility denominator.

The thermal model must be calibrated to the Edge TPU package and workload. Compare predicted and measured temperature at SRAM banks, compute units and package hotspots across frequency/voltage, activity, cooling and ambient conditions, and include sensor delay, thermal time constants and control stability. SRAM placement can change data movement and write energy even when temperature falls.

The up-to-46% task-set claim lacks task/deadline distributions, temperature results, deadline misses, energy, write overhead, Edge-TPU conditions and package-level validation. The evidence supports joint thermal-aware DFS and SRAM scheduling, not demonstrated real-time guarantees or hardware-validated thermal efficiency.

**Source and location**

Evidence tier: Primary captured official DAC description plus existing authored chapter level explanation; no full paper extraction, thermal calibration trace, deadline feasibility matrix or independent edge tpu validation. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH2481&sess=sess171)

DAC 2026 official description; existing chapter-level thermal-and-reliability-modeling discussion; captured Problem, Mechanism / artifact, Workload, Hardware, Baseline, Measurements and Limits fields; no manuscript pages or reproduced Edge-TPU thermal/scheduling evaluation.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** capacity-only SRAM allocation

thermal-oblivious scheduling

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH2481

**Hardware or process assumptions:** Edge TPU with banked SRAM and thermal coupling; process, cooling, and workload assumptions are unspecified.

**Limits:** No deadline miss rate, temperature, energy, area, or throughput results are reported.

Thermal models may not capture package-level effects.

Official description only; hardware thermal validation is required.

**Method or artifact:** Thermal-aware SRAM allocation and scheduling strategy for Edge TPU workloads.

**Metrics:** Deadline and thermal efficiency are claimed qualitatively

**Problem:** On-chip SRAM placement affects both real-time performance and thermal hotspots in edge TPUs.

**Workload or benchmark:** Real-time DNN tasks; TPU memory hierarchy, task deadlines, thermal model, and baselines are unspecified.

</details>

<span id="paper-dac-2026-research1390"></span>

### ATLAS: Asynchronous Topological Learning for Accurate FIT Prediction via Decoupled Graph Neural Networks

DAC 2026 · Record: `dac-2026-research1390`

[Read the step-by-step explanation](#explanation-dac-2026-research1390)

**Updated source-backed reading card**

Reviewed 2026-09-09. Deepens the ATLAS treatment into a paper-level reading; separates asynchronous topological message passing, risk ranking and calibration heads from rare-event label quality, FIT calibration, reliability-mechanism coverage, selective-hardening decisions and safety-case evidence, while preserving the ASIL-D/FIT, 220x and 53% claims.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Safety-critical integrated circuits targeting ISO 26262 ASIL-D require very low failure-in-time rates, but physics-based FIT analysis is expensive and ordinary ML can collapse on long-tailed failure data; the model must represent component dependencies while ranking high-risk gates and producing calibrated failure estimates.

**Mechanism / artifact:**

ATLAS: a decoupled graph neural network with bidirectional asynchronous topological message passing aligned to forward/backward BFIT propagation, a gap-aware RankNet head with log-gap weighting and head-sample emphasis for top-k% risk ranking, and a dual-domain log/linear CalibNet head with importance weighting for calibration; graph features, failure mechanisms, label construction, loss weights, calibration protocol and hardening decision flow are unspecified.

**Workload — the work tested:**

FIT prediction and selective hardening for hardware reliability graphs, with reported ITC'99 benchmark use; gate/system graph construction, failure mechanisms, operating exposure, FIT labels, train/validation/test split, rare-event prevalence, top-k definition, hardening constraints, circuit scale and benchmark transfer conditions are unspecified.

**Hardware and manufacturing assumptions:**

Safety-critical integrated-circuit reliability analysis under an ISO 26262 ASIL-D target and graph-based gate dependencies; BFIT or equivalent physics reference, technology/process, voltage/temperature/aging conditions, failure-rate sources, circuit simulator, hardening implementation, area model and deployment workflow are unspecified.

**Baseline — the comparison method:**

BFIT physics-based FIT analysis

DeepGate2

Static or conventional GNN FIT model

Same reliability graphs, FIT labels, operating conditions, data split, top-k risk budget, hardening policy, feature availability, training budget and measurement boundary are unspecified

**Reported measurements:**

The official description states an O(|V|+|E|) design, up to 220x speedup over BFIT and 53% lower selective-hardening area overhead than DeepGate2 on ITC'99 benchmarks; it reports no FIT prediction error, calibration error, ranking precision/recall, rare-event performance, uncertainty, transfer result, absolute runtime, area definition or safety-case outcome.

**Limits on the conclusion:**

A graph prediction can rank gates or estimate FIT without proving the underlying failure mechanisms, operating exposure or safety requirement. Define failure modes, FIT label units and exposure, graph dependencies, BFIT reference, censoring and uncertainty; evaluate held-out circuits, technologies, workloads and operating conditions with calibration curves, tail/ranking metrics and rare-event sensitivity. A low average error or useful top-k ranking is not an ISO 26262 safety argument.

CalibNet's log- and linear-domain losses must be tested against the long-tailed target distribution without allowing common low-FIT samples to hide high-risk errors. Report calibration error, confidence intervals, tail exceedance, top-k recall/precision, threshold selection and the cost of false negatives and false positives; connect predictions to selective hardening and re-evaluate the hardened circuit rather than treating a predicted risk score as a physical outcome.

The official description reports ASIL-D/FIT motivation, O(|V|+|E|) complexity, up to 220x BFIT speedup and 53% lower selective-hardening area overhead than DeepGate2 on ITC'99, but omits error definitions, calibration, rare-event/transfer conditions, absolute runtime, failure-mechanism validation, area accounting and deployment evidence. The evidence supports a reliability-aware GNN direction, not demonstrated calibrated FIT prediction or safety-case-ready selective hardening.

**Source and location**

Evidence tier: Primary captured official DAC description plus existing authored reliability discussion; no full paper extraction, failure data provenance, reproduced calibration, cross technology transfer or independent safety validation. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH1390&sess=sess118)

DAC 2026 official description; existing thermal-and-reliability-modeling chapter discussion; captured Problem, Mechanism / artifact, Workload, Hardware, Baseline, Measurements and Limits fields; no manuscript pages, FIT-label audit, calibration plot, held-out reliability study or hardened-circuit validation.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** static GNN FIT model

physics-only reliability analysis

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH1390

**Hardware or process assumptions:** Hardware reliability graph with component and dependency features; failure mechanisms and data sources are unspecified.

**Limits:** No error, calibration, rare-event, transfer, or deployment results are reported.

Historical failure data may be sparse or biased.

Official description only; calibrated reliability validation is required.

**Method or artifact:** Decoupled graph neural network with asynchronous topological learning for FIT prediction.

**Metrics:** FIT prediction accuracy is claimed qualitatively

**Problem:** Failure-in-time prediction for hardware systems must capture asynchronous dependencies and topology without expensive simulation.

**Workload or benchmark:** Reliability graphs and FIT data; labels, systems, and baselines are unspecified.

</details>

<span id="paper-dac-2026-research733"></span>

### PIANO: Physics-Informed Admittance Neural Operator for Fast Power Integrity Analysis

DAC 2026 · Record: `dac-2026-research733`

[Read the step-by-step explanation](#explanation-dac-2026-research733)

**Updated source-backed reading card**

Reviewed 2026-09-09. Deepens the PIANO treatment into a paper-level reading; separates resistive-PDN graph extraction, GNN port-admittance prediction and reduced SPD solving from Kirchhoff/physical consistency, voltage-noise error, load/geometry transfer, solver cost and design-space decision validity, while preserving the 12.6x, 1.95% and 17.2x claims.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

DC power-integrity analysis solves large symmetric positive-definite systems from package/board power-distribution networks; repeated solves across loads and geometries can slow design iterations, motivating a learned reduction that still preserves voltage behavior.

**Mechanism / artifact:**

PIANO extracts an equivalent resistive network from a 3D-IC PDN layout, represents it as a graph, uses a graph neural network to predict the equivalent port admittance matrix between voltage-source ports and current sinks, then forms and solves a reduced SPD system with a lightweight numerical solver; graph extraction, port definition, SPD enforcement, loss/physics constraints, training domain, solver tolerances and fallback are unspecified.

**Workload — the work tested:**

Industrial-scale 3D-IC/package PDNs under DC loads; geometry, stack/materials, port/load locations, current distributions, via/mesh resolution, number of ports, training/test split, design-space exploration loop, voltage limits and reference solver/tool are unspecified.

**Hardware and manufacturing assumptions:**

PDN resistive/circuit models analyzed by commercial simulators and a GNN plus numerical solver; package/board stack, metal/via resistance, materials, process, solver hardware, memory, parallelism, model-inference hardware and power/thermal instrumentation are unspecified.

**Baseline — the comparison method:**

Commercial/full-field numerical PI simulator

Physics-agnostic neural surrogate

Direct sparse SPD solver

Same PDN geometry, ports, loads, boundary conditions, solver tolerance, voltage-error target, hardware, preprocessing, training and end-to-end DSE timing boundary are unspecified

**Reported measurements:**

The official description reports 12.6x speedup over commercial simulators with 1.95% voltage error on industrial-scale PDNs, and 17.2x acceleration when integrated into a PI-constrained design-space exploration flow; it does not report absolute runtime, voltage-error distribution, peak/minimum error, SPD/residual violations, geometry/load transfer, memory, energy or per-design results.

**Limits on the conclusion:**

The predicted admittance must remain a physically valid network model. Check symmetry, positive definiteness, passivity, Kirchhoff current balance, boundary conditions and residuals after forming the reduced system; compare node/port voltages and current conservation with a trusted sparse solver. A 1.95% average voltage error can hide a worst-case droop violation or an invalid matrix at an important load/port.

Validate transfer across PDN geometry, materials, port count/location, current-sink distributions, package/process corners and unseen layouts. Separate interpolation from extrapolation and report voltage error tails, minimum/maximum droop, residual, conditioning, solver iterations and failure/fallback. Include graph extraction, feature construction, GNN inference, matrix assembly and numerical solve in speed; DSE acceleration must include rejected candidates and final independent PI checks.

The 12.6x and 17.2x claims need a declared commercial-tool boundary, tolerance, hardware, training cost and design-space workflow. Compare full numerical solving and physics-agnostic surrogates at the same voltage-quality and constraint target, and re-evaluate designs with an independent solver. The evidence supports physics-informed admittance learning for DC PI analysis, not demonstrated signoff-grade voltage integrity, broad geometry transfer or universally faster PI-constrained design.

**Source and location**

Evidence tier: Primary captured official DAC description plus existing authored power integrity discussion; no full paper extraction, independent spd/passivity validation, geometry/load transfer study or signoff equivalent pi measurement. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH733)

DAC 2026 official description; existing thermal-and-reliability-modeling chapter framing; captured Problem, Mechanism / artifact, Workload, Hardware, Baseline, Measurements and Limits fields; no manuscript pages, voltage/residual table, PDN geometry matrix or reproduced DSE run.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** full-field numerical solver

physics-agnostic neural surrogate

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH733

**Hardware or process assumptions:** Package/board power-distribution network with electromagnetic or circuit models; process assumptions are unspecified.

**Limits:** No voltage-noise error, runtime, geometry transfer, frequency, or validation results are reported.

Physics-informed surrogates may miss local resonances.

Official description only; solver-correlated validation is required.

**Method or artifact:** Physics-informed neural operator based on admittance modeling.

**Metrics:** Power-integrity analysis speed and fidelity are claimed qualitatively

**Problem:** Power-integrity analysis of complex packages and boards is expensive under varying loads and geometries.

**Workload or benchmark:** Power-integrity networks; geometries, materials, excitation, and baselines are unspecified.

</details>

## What remains to establish

Resolve unspecified workloads, comparison methods, resource budgets, and source locations before generalizing a reported gain. Multiple papers in this selected sample permit comparison of mechanisms, but do not by themselves establish recurrence across years or a long-term trend.

[All subthemes](../expanded-taxonomy-v1.md) · [Research directions](../directions/README.md)
