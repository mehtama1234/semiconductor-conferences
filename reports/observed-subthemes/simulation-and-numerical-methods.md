# Simulation and numerical methods

This subject has 1 record in the selected sample. This page explains where it fits, then presents all captured paper evidence without shortening the measurements or limitations.

[Definitions used in the paper records](../reading-guide-v1.md)

## Understand the parent subject first

- [Design methodology and tooling](../themes/design-methodology-and-tooling.md)

## Circuit simulation includes solving equations

Electrical models relate unknown quantities, such as voltages, through equations. A linear solve seeks values satisfying a system written as `A x = b`: `A` describes the relationships, `x` contains the unknowns, and `b` contains the specified contributions. A simulator may solve many such systems as conditions change or as part of a larger nonlinear calculation.

A sparse matrix stores relatively few nonzero relationships. This can reduce storage and arithmetic, but sparsity alone does not establish that a system is easy to solve. Numerical sensitivity and the relationships among the equations affect how reliably and quickly a method approaches an answer.

## What preconditioning changes

An iterative solver improves an estimated solution through repeated updates. A preconditioner is an auxiliary transformation intended to make those updates more effective. It has its own construction and application costs. A more expensive preconditioner can be worthwhile if it saves enough iterations; a cheap one may leave the overall solve slow.

The standard preconditioned conjugate-gradient method has mathematical requirements: the system and preconditioner are symmetric positive definite. Symmetry means that the matrix agrees with its transpose; positive definiteness means `vᵀ A v > 0` for every nonzero vector `v`. These properties give the standard method its applicable mathematical setting. [Netlib's treatment of conjugate gradients](https://netlib.org/linalg/html_templates/node21.html) states these requirements. They must not be assumed for every possible circuit matrix.

## EastPCG: use a sparser graph to assist the solve

[EastPCG](../observed-subthemes/simulation-and-numerical-methods.md#paper-dac-2026-research2131) proposes self-tuning graph sparsification in a preconditioned conjugate-gradient solver for circuit simulation. A graph can represent relationships in the system. Sparsification constructs a representation with fewer retained relationships, seeking lower cost while preserving useful properties.

The captured description does not expose the sparsification rule, tuning criterion, supported matrix classes, or exact role of the reduced graph. It should not be asserted that the method discards relationships from the final physical model. A reduced representation used only to assist an iterative solve is different from replacing the original equations with an approximate physical system.

The important questions are what problem is ultimately solved, which properties the auxiliary representation preserves, and how the method detects an ineffective configuration. “Self-tuning” does not mean no setup cost or universal convergence. The description supplies no iterations, errors, runtime, memory, circuit sizes, or robustness results.

## A small residual is a defined check, not an unrestricted guarantee

The residual is `b - A x`, the mismatch obtained by substituting the estimated answer into the original equations. A stopping rule can require this mismatch to be sufficiently small. Its interpretation depends on normalization, numerical precision, and how sensitive the system is to small changes.

Evaluation should therefore specify both the stopping rule and the quantities of engineering interest. A solver-level tolerance is not automatically a bound on every reported circuit output. If the solve is part of a larger transient or nonlinear simulation, its numerical error can also affect subsequent work. These are general validation requirements; the short source does not establish how EastPCG handles them.

## Count setup, failed cases, and reuse

A fair comparison would solve the same systems to the same stated acceptance conditions, counting graph construction, tuning, preconditioner construction, all iterations, and fallback work. Comparing iteration counts alone can favor a method whose individual iteration is much more expensive. Comparing only successful systems can hide a serious robustness limitation.

Reuse across repeated solves is another important condition. A preparation cost paid once may be reasonable for many similar systems but unattractive when the system changes enough to require rebuilding. The benchmark must state that reuse pattern before its runtime result can guide a simulator design.

<span id="explanation-dac-2026-research2131"></span>

## EastPCG: sparsifying the auxiliary graph is useful only if the original circuit solve and total cost remain controlled

Circuit simulation often reduces an operating point or a step of a transient/nonlinear calculation to a linear system `A x = b`. A sparse matrix records relatively few electrical relationships, and a preconditioned conjugate-gradient (PCG) solve tries to reach an acceptable solution with repeated updates. A preconditioner can improve the conditioning seen by the iteration, but its construction and application are part of the solve. For standard PCG, the matrix and compatible preconditioner also need the applicable symmetry and positive-definiteness properties; those cannot be assumed for every circuit formulation.

EastPCG is described as combining spectral-probability graph sparsification with a neural-network-powered self-tuning PCG framework. The sparsified graph is an auxiliary representation intended to make preconditioning or related work cheaper, while the neural component chooses settings for a target of minimum total solution time across multiple right-hand sides. That is different from replacing the physical circuit equations with a smaller approximate circuit. The captured description does not specify the sparsification rule, retained graph role, neural inputs/outputs, objective, training data, tuning search, rebuild policy, matrix class, precision or fallback.

The first gate is numerical validity. State whether the circuit matrix is symmetric positive definite, transformed to that form, or solved with a different safeguarded method. Define the preconditioner, scaling, initial guess, absolute/relative residual and stopping tolerance, then compare `b - A x`, solution error and derived voltages/currents with a trusted direct or high-precision reference. Test multiple right-hand sides, operating points, ill-conditioned systems, changing matrices and nonlinear/transient outer loops. A small residual is not automatically a bound on every circuit output, and an auxiliary sparse graph must not silently alter the physical equations.

The second gate is total-cost accounting. Measure graph construction, spectral probabilities, neural inference, candidate evaluation, preconditioner construction, application, sparse matrix-vector products, synchronization, memory traffic, all iterations, failed solves, fallback and rebuilds. Separate one-time setup from reused setup and report total wall time for a stated number of right-hand sides and matrix changes. A lower iteration count can lose overall if each iteration or each tuning decision is more expensive; a benchmark of successful systems can hide breakdowns or tolerance-dependent failures.

Compare direct circuit solving, fixed-preconditioner PCG and existing sparsification methods with identical matrices, right-hand sides, residual rule, precision, initial guesses, hardware/software, reuse pattern, fallback policy and end-to-end boundary. Report circuit scale, sparsity, conditioning, convergence distributions, output error, memory and p50/p95/p99 solve time across benchmark classes and operating conditions. The “self-tuning” claim should be evaluated on held-out systems, not only on systems used to select the policy.

The official description says EastPCG improves over existing counterparts on various benchmarks, but the captured record exposes no convergence, residual/error, iteration, runtime, memory, circuit-scale, tolerance or robustness results. The evidence supports self-tuning sparsified-PCG exploration for circuit simulation, not demonstrated solver correctness, general convergence or faster end-to-end circuit simulation.

This single record motivates adapting numerical infrastructure to circuit structure. It does not yet establish a general faster circuit simulator. The decisive evidence would connect solver correctness and total cost to complete simulations across specified operating conditions, with failure cases and sensitivity to tolerances reported explicitly.

## Compare the results carefully

First identify the inputs and required output quality. Then identify the limited resource: time, memory, communication, energy, circuit area, or correctness coverage. Ask which part of the method reduces that cost and which new cost it adds. Compare numbers only when the experiments hold these conditions sufficiently similar.

A conference description may explain the proposal while omitting the full experiment. An author preprint link may have been coded from its abstract. The source classification does not by itself establish that every table was read. Missing locations remain visible below.

## Complete captured evidence

These are evidence records, not substitutes for the explanations above. Each record preserves its problem, proposed method, measurements, comparison conditions, and source limits. A populated record does not establish that its mechanism has been fully explained or independently verified.

<span id="paper-dac-2026-research2131"></span>

### EastPCG: An Efficient and Self-Tuning Graph Sparsification Based PCG Solver for Circuit Simulation

DAC 2026 · Record: `dac-2026-research2131`

[Read the step-by-step explanation](#explanation-dac-2026-research2131)

**Updated source-backed reading card**

Reviewed 2026-09-09. Deepens the EastPCG treatment into a paper-level reading; separates spectral-probability graph sparsification and neural self-tuning of PCG preconditioners from matrix-class validity, residual/error guarantees, conditioning, tuning/rebuild cost, circuit-output accuracy and total simulation time.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Circuit simulation repeatedly solves large sparse linear systems, potentially with multiple right-hand sides and changing operating points; fixed preconditioners can be expensive or ineffective across those systems, while iterative-solver setup and convergence determine total simulation time.

**Mechanism / artifact:**

EastPCG combines a spectral-probability graph-sparsification algorithm described as efficient and stable with a neural-network-powered self-tuning preconditioned conjugate-gradient framework targeting minimum total solution time for multiple right-hand sides; sparsification rule, retained-graph role, PCG matrix/preconditioner properties, neural inputs/outputs, tuning objective, rebuild policy, fallback and precision are unspecified.

**Workload — the work tested:**

Circuit-simulation linear systems across various benchmarks and multiple right-hand sides; circuit classes, matrix dimensions/sparsity, operating-point/transient/nonlinear context, right-hand-side count, tolerances, conditioning, initial guesses, reuse pattern and benchmark identities are unspecified.

**Hardware and manufacturing assumptions:**

Sparse numerical solver for circuit matrices running in a software simulation environment; CPU/GPU/parallel implementation, memory hierarchy, numerical precision, sparse format, threading, neural-inference cost, compiler/library versions and circuit-model assumptions are unspecified.

**Baseline — the comparison method:**

Direct circuit solver

Fixed-preconditioner PCG

Existing graph-sparsification preconditioner

Same matrices, right-hand sides, tolerance/residual rule, precision, initial guess, hardware/software, setup reuse, fallback policy and total-simulation boundary are unspecified

**Reported measurements:**

The official description claims advantages over existing counterparts on various benchmarks, but reports no numerical convergence, residual/error, iteration count, runtime, memory, setup/tuning cost, robustness, circuit scale, output accuracy or operating-point sweep results.

**Limits on the conclusion:**

Standard PCG requires assumptions such as a symmetric positive-definite system and compatible preconditioner; circuit linearizations, nonsymmetric formulations, indefinite systems and nonlinear/transient contexts may require different methods or safeguards. State the matrix class, symmetrization or alternative solver, preconditioner properties and breakdown handling, and compare residuals and solution error against a trusted direct or high-precision reference. A sparse auxiliary graph must not be confused with replacing the physical circuit equations.

A small residual in b - A x is a solver check, not automatically a bound on voltages, currents, timing or later nonlinear/transient outputs. Define absolute/relative residual normalization, stopping tolerance, conditioning, scaling, precision and output-level error; test multiple right-hand sides, operating points, initial guesses, tolerances and ill-conditioned cases. Report failed or stalled solves and fallback behavior rather than only completed runs.

Self-tuning can reduce iterations while adding graph construction, neural inference, candidate evaluation, preconditioner construction and rebuild costs. Measure setup, tuning, preconditioner application, sparse matrix-vector products, synchronization, memory traffic, all iterations and recovery. Separate one-time cost from reused cost and compare total wall time for a stated number of right-hand sides and changing matrices; iteration count alone is insufficient.

The official description says EastPCG improves over existing counterparts on various benchmarks but exposes no convergence, error, runtime, memory, circuit-scale, tolerance or robustness results. The evidence supports self-tuning sparsified-PCG exploration for circuit simulation, not demonstrated solver correctness, general convergence or faster end-to-end circuit simulation.

**Source and location**

Evidence tier: Primary captured official DAC description plus existing authored numerical solver discussion; no full paper extraction, reproduced eastpcg run, circuit output error validation or independent benchmark comparison. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH2131&sess=sess112)

DAC 2026 official description; existing simulation-and-numerical-methods chapter framing; captured Problem, Mechanism / artifact, Workload, Hardware, Baseline, Measurements and Limits fields; no manuscript pages, convergence trace, residual/error table or full-simulation timing matrix.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** direct circuit solver

fixed-preconditioner PCG

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH2131

**Hardware or process assumptions:** Sparse numerical solver for circuit matrices; precision and parallel hardware assumptions are unspecified.

**Limits:** No error, iterations, runtime, memory, robustness, or circuit-scale results are reported.

Sparsification can degrade conditioning.

Official description only; tolerance and operating-point sweeps are required.

**Method or artifact:** Self-tuning graph-sparsification-based PCG solver.

**Metrics:** Simulation convergence and efficiency are claimed qualitatively

**Problem:** Large circuit linear systems make iterative simulation expensive, and fixed preconditioners may fail across operating points.

**Workload or benchmark:** Circuit simulation linear systems; circuit classes, tolerances, and baselines are unspecified.

</details>

## What remains to establish

Resolve unspecified workloads, comparison methods, resource budgets, and source locations before generalizing a reported gain. This subject is represented by one paper and supports a case study, not evidence of recurrence or a long-term trend.

[All subthemes](../expanded-taxonomy-v1.md) · [Research directions](../directions/README.md)
