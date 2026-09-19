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
