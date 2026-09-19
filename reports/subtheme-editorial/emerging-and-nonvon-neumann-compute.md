## Randomness can be part of the computation, but the required output still matters

The three papers in this subject use probabilistic computation for two different purposes. Two search for good discrete solutions. The third generates noise for diffusion-model sampling. Finding a low-cost answer and generating samples with a required distribution are not the same task, so their quality measures cannot be combined.

“Non-von Neumann” is a broad architectural label, not an explanation of a mechanism. A useful account must identify where state is stored, how it changes, what operations remain digital, and how the machine's output becomes an application result. An architecture may replace a repeated update while retaining conventional memory, control, and input/output processing.

The conceptual explanations below develop these distinctions independently. The paper-specific sections state what the available official descriptions establish. Full manuscripts were not recovered for these three records, so no page-backed algorithm or experimental details are invented.

## Representing a discrete optimization problem as an Ising objective

A combinatorial optimization problem chooses among discrete alternatives while satisfying constraints. An Ising representation assigns each variable, called a spin, one of two values, commonly −1 and +1. Pairwise coefficients specify how pairs of choices contribute to an objective; individual coefficients specify preferences for particular choices.

For example, a weighted graph cut divides vertices into two groups and sums the weights of edges crossing between them. With group labels s_i and s_j, the expression (1 − s_i × s_j) / 2 is one when the labels differ and zero when they match. Multiplying by an edge weight and summing therefore represents the cut value. This is a mathematical encoding example, not a recovered implementation detail of either optimizer.

Calling the objective “energy” does not mean it equals electrical energy consumed by the circuit. Lower objective energy can mean a better encoded solution while the hardware expends electrical energy to find it. Constraints encoded as penalties also need careful scaling: a numerically favorable state may be unusable if a constraint violation was penalized too weakly.

The local field for a spin summarizes the weighted influence of other spins and its individual coefficient. Updating many such fields is repeated work that specialized hardware can target. Dense connectivity, however, requires information about many interactions. State-update speed alone does not account for storing coefficients, supplying them to arithmetic, or moving state between processing units.

<span id="explanation-dac-2026-research2159"></span>

## PMTPA: organize multiple searches and their repeated arithmetic

[PMTPA](../observed-subthemes/emerging-and-nonvon-neumann-compute.md#paper-dac-2026-research2159) combines time-shared replicas and pipelined processing. The description reports similarity-based local-field computation that halves local-field storage, adaptive network sizing, and random-controlled shifts for nonlinear functions. Its FPGA prototype supports up to 2,048 fully connected spins and 2–32 configurable replicas. Max-Cut and image-segmentation experiments reportedly exceed 99% accuracy with 17,000× speedup over a CPU implementation. The accuracy definition, CPU configuration, run budgets, and success probabilities are unspecified. The headline is not a demonstrated 99% probability of finding an exact optimum. [Official DAC description](https://63dac.conference-program.com/presentation/?id=RESEARCH2159&sess=sess130).

A replica is a separate candidate state or search instance. Tempering methods vary exploration conditions among instances; some versions exchange states according to defined rules. The word “momentum” in a title does not specify its state variable or update equation. Those details are necessary to determine how the search behaves, especially when multiple instances share hardware.

As independent reasoning, a shared arithmetic unit trades physical duplication for scheduling time. Supporting more replicas does not necessarily mean updating all of them simultaneously. Likewise, approximate nonlinear arithmetic must be assessed for its effect on solution quality, not only its circuit cost. A storage reduction for one intermediate array is not automatically the same reduction in total memory.

The first gate is the optimization contract. Define the Ising variables, objective sign, constraint penalties, feasible assignments, optimum or reference, approximation gap and the meaning of “accuracy.” Validate every returned assignment and objective independently. A low encoded energy can still represent an infeasible solution if penalty weights are mis-scaled, and an accuracy percentage is not automatically the probability of finding the optimum.

Tempering and momentum need explicit dynamics: update equations, temperature or parameter schedule, replica exchange/acceptance rule, random source, correlation, stopping condition and replica synchronization. Measure success probability and time-to-target over repeated seeds and instances. Include local-field storage, random generation, nonlinear approximation, time-division scheduling, pipeline fill/drain and host transfer in FPGA time, area and power; 2–32 configurable replicas does not mean 32 replicas update simultaneously at full throughput.

The official description reports support for up to 2,048 fully connected spins and 2–32 replicas, accuracy above 99% on large-scale Max-Cut and image-segmentation benchmarks, and 17,000× speedup over a CPU implementation. It does not define the accuracy metric, optimum gap, success probability, convergence, time-to-solution, energy, FPGA resources, precision or per-instance results. Compare CPU, GPU and simulated-annealing baselines with identical encodings, quality target, seeds, run budget and reliability requirement.

The evidence supports an FPGA parallel-tempering architecture, not demonstrated optimum-finding probability, universal 17,000× time-to-solution, energy efficiency or scalable solution quality.

<span id="explanation-dac-2026-research2817"></span>

## EHPC: separate a device demonstration from larger modeled comparisons

[EHPC](../observed-subthemes/emerging-and-nonvon-neumann-compute.md#paper-dac-2026-research2817) uses volatile RRAM/resistive memory for probabilistic optimization. The 2026 description distinguishes a fabricated oxide-memory-multiplexed circuit solving Max-Cut from hardware simulations reporting better solution quality within one second under stated equal-resource comparisons. It separately gives floorplanning speedups of 20×–1,500× with less than 1.7% area expansion against conventional methods. Benchmark identities, comparison resources, statistical variation, and measurement boundaries are not supplied. [Official DAC 2026 description](https://63dac.conference-program.com/presentation/?id=RESEARCH2817&sess=sess174).

An earlier work-in-progress poster with the same acronym focuses on floorplanning and gives a different speed range. Its 2025 results must not be substituted for the 2026 paper's broader claim. [Official DAC 2025 poster description](https://62dac.conference-program.com/presentation/?id=RESEARCH2048&sess=sess261).

EHPC has three different evidence boundaries. The fabricated OxRAM-multiplexed circuit is a device demonstration on a Max-Cut problem. The under-one-second solution-quality comparison is described as a hardware simulation. The 20×–1,500× floorplanning result is another comparison whose solver, stopping rule, and area definition are not exposed. A result from one boundary cannot be silently promoted to the others.

Resistive memory represents device state through electrical resistance. A volatile device does not retain a switched state indefinitely. A probabilistic design must connect that physical behavior to an intended update probability; physical variability alone does not establish that the resulting search follows the desired rule.

Floorplanning arranges circuit blocks subject to geometric and other constraints. The area of the resulting floorplan is different from the area of the accelerator performing the search. The reported area-expansion phrase belongs to a solution-quality comparison in the available description; it must not be relabeled as measured accelerator silicon overhead. Exact area definitions still require the manuscript.

The optimization contract must include the objective encoding, constraints, solution-quality target, random seed, sampling schedule, stopping condition and the probability of reaching the target. A short stochastic run that occasionally finds a good solution is not equivalent to a deterministic solver that reaches the same target reliably. Compare time-to-target and energy-to-target across repeated instances, and include device calibration, peripheral control, host transfers and result decoding.

The captured evidence supports a heterogeneous probabilistic-optimization direction, not demonstrated scalable end-to-end time-to-solution or device-level optimization superiority.

<span id="explanation-dac-2026-research2975"></span>

## iADS: a noise source is a component of a generative system

[iADS](../observed-subthemes/emerging-and-nonvon-neumann-compute.md#paper-dac-2026-research2975) proposes self-compensating probabilistic-bit units for Gaussian noise generation and scaling. The description reports a fabricated 256-unit circuit used for MNIST generation, then a hardware-calibrated 1,048,576-unit architecture for CIFAR10 and CelebA-HQ, with CIFAR10 FID of 9.96. It claims about 8× lower energy and 143× lower area relative to pseudorandom-number generators. It does not establish fabrication of the million-unit architecture or equivalent reductions for a complete diffusion system. Models, sampling schedules, quality comparisons, and accounting boundaries remain unspecified. [Official DAC description](https://63dac.conference-program.com/presentation/?id=RESEARCH2975&sess=sess174).

A probabilistic bit, or p-bit, produces a binary outcome with a controllable probability. A Gaussian random variable instead has a continuous-valued distribution with a specified mean and spread. Generating binary randomness is therefore not sufficient on its own: the design must explain how values are combined or transformed and how the desired distribution is maintained.

Diffusion generation applies a sequence of learned transformations to a noisy state. Where the chosen algorithm requires random noise, both its distribution and scale affect the calculation. FID is a generated-image distribution comparison based on extracted features; it is not a percentage of correct images or a proof of equivalence to another sampler. A single reported FID needs its dataset and evaluation protocol before comparison.

Temporal correlation matters as well as the distribution of individual samples. Many outputs with the right individual mean and spread can still be unsuitable if successive values are too dependent. Voltage-dependent probability, calibration cost, device variation, and correlation across units therefore belong in the validation questions. They are not established defects in this proposal.

The captured evidence supports adaptive probabilistic noise hardware, not demonstrated full-system diffusion acceleration or quality-preserving 8×/143× gains.

## Compare time to a useful result, not just update throughput

For a randomized optimizer, define a target solution quality and measure the probability p that one run reaches it. Under independent, identically configured runs, the probability of at least one success after r runs is 1 − (1 − p)^r. This basic probability relation explains why short runs with poor success probability need not yield a faster reliable answer. Correlated replicas do not automatically satisfy the independence assumption.

For a sampler, count the time and energy needed to produce outputs at the required distribution quality, including conversion, control, and the remaining model computation. A faster random source only accelerates the part of execution that depends on it. Neither optimizer success probability nor image-quality measures can be inferred from random-bit throughput.

The shared research question is where specialized state updates save enough repeated work to justify representation, calibration, and integration costs. This connects architecture to algorithms and device behavior, but does not establish a universal advantage over conventional processors. The refreshed descriptions supersede the historical cards' missing-result statements; complete source reconciliation, paper-page evidence, and independent reproduction remain unfinished.
