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
