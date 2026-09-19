# Emerging and nonvon neumann compute

This subject has 3 records in the selected sample. This page explains where it fits, then presents all captured paper evidence without shortening the measurements or limitations.

[Definitions used in the paper records](../reading-guide-v1.md)

## Understand the parent subject first

- [Analog mixed signal and emerging devices](../themes/analog-mixed-signal-and-emerging-devices.md)
- [Architecture and accelerators](../themes/architecture-and-accelerators.md)

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

## Compare the results carefully

First identify the inputs and required output quality. Then identify the limited resource: time, memory, communication, energy, circuit area, or correctness coverage. Ask which part of the method reduces that cost and which new cost it adds. Compare numbers only when the experiments hold these conditions sufficiently similar.

A conference description may explain the proposal while omitting the full experiment. An author preprint link may have been coded from its abstract. The source classification does not by itself establish that every table was read. Missing locations remain visible below.

## Complete captured evidence

These are evidence records, not substitutes for the explanations above. Each record preserves its problem, proposed method, measurements, comparison conditions, and source limits. A populated record does not establish that its mechanism has been fully explained or independently verified.

<span id="paper-dac-2026-research2159"></span>

### PMTPA: An Ising Model-Based Parallel-Momentum Tempering Processing Architecture for Combinatorial Optimization

DAC 2026 · Record: `dac-2026-research2159`

[Read the step-by-step explanation](#explanation-dac-2026-research2159)

**Updated source-backed reading card**

Reviewed 2026-09-09. Deepens the PMTPA treatment into a paper-level reading; separates elastic replica time-division, momentum-tempering search, similarity-based local fields, adaptive sizing and random-controlled nonlinear updates from Ising objective correctness, success probability, convergence, replica correlation, FPGA resource/precision limits and the CPU speedup boundary, while preserving the 2,048-spin, 2–32-replica, 99%+ and 17,000x claims as source-reported.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Combinatorial optimization searches rugged discrete energy landscapes; parallel replicas and specialized local-field arithmetic may improve exploration, but a useful result requires a defined objective, constraint contract, solution-quality target and probability of reaching it.

**Mechanism / artifact:**

PMTPA is an FPGA processing architecture with elastic replicas, time-division multiplexing and a system-level parallel pipeline for parallel-momentum tempering; it uses similarity-driven local-field computation to halve local-field storage, adaptive processing for varying spin-network sizes and random-number-controlled shifts for nonlinear functions; exchange/update equations, precision, replica scheduling and random source are unspecified.

**Workload — the work tested:**

Fully connected Ising networks up to 2,048 spins, with 2–32 configurable replicas, evaluated on large-scale Max-Cut and image-segmentation benchmarks; problem mappings, sizes, constraints/penalties, objective normalization, target-quality threshold, run count, iteration budget, success probability and CPU baseline configuration are unspecified.

**Hardware and manufacturing assumptions:**

Prototype FPGA implementation with time-shared processing and configurable replicas; FPGA model, clock, resource utilization, BRAM/URAM, DSP/LUT use, precision, bandwidth, power, random-number generator, host transfer and measured-versus-modeled status are unspecified.

**Baseline — the comparison method:**

CPU-based implementation

Simulated annealing

CPU or GPU optimizer

Same Ising encoding, penalties, quality target, initialization, random seeds, run/iteration budget, parallelism, precision, host overhead and time-to-solution boundary are unspecified

**Reported measurements:**

The official description reports accuracy exceeding 99% on large-scale Max-Cut and image-segmentation benchmarks, support for up to 2,048 fully connected spins and 2–32 replicas, and 17,000x speedup over a CPU implementation; it does not define accuracy, optimum/approximation gap, success probability, convergence, time-to-solution, energy, FPGA resources, precision or per-instance results.

**Limits on the conclusion:**

An Ising energy or an 'accuracy' percentage must map to the original optimization problem. Define variables, objective sign, penalty weights, feasibility, optimum/reference, approximation gap and tie/constraint handling; validate returned assignments and objective values independently. A state with low encoded energy can still violate a constraint if penalties are mis-scaled, and 99% is not automatically a 99% probability of finding the optimum.

Tempering and momentum need explicit update and exchange equations, temperature/parameter schedule, replica correlation, acceptance rule and stopping condition. Measure success probability and time-to-target over repeated seeds, not only best energy or one run. Include local-field storage, random generation, nonlinear approximation, time-division scheduling, synchronization and host transfer in FPGA area, power and time; supporting more replicas is not the same as updating them concurrently.

Compare CPU, GPU and simulated-annealing baselines with identical problem encoding, quality target, initialization, run budget and reliability requirement. Test spin counts, graph density, constraint regimes, Max-Cut and segmentation distributions, and larger or unseen instances. The evidence supports an FPGA parallel-tempering architecture, not demonstrated optimum-finding probability, universal 17,000x time-to-solution, energy efficiency or scalable solution quality.

**Source and location**

Evidence tier: Primary captured official DAC description plus existing authored probabilistic optimization discussion; no full paper extraction, independent ising quality reproduction, FPGA resource/power validation or matched time to solution campaign. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH2159&sess=sess130)

DAC 2026 official description; existing emerging-and-nonvon-neumann-compute chapter framing; captured Problem, Mechanism / artifact, Workload, Hardware, Baseline, Measurements and Limits fields; no manuscript pages, instance table, objective/penalty definition, repeated-seed trace or FPGA resource/power report.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** simulated annealing

CPU or GPU optimizer

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH2159

**Hardware or process assumptions:** Ising or stochastic optimization accelerator; device, precision, and annealing assumptions are unspecified.

**Limits:** No solution quality, time-to-solution, energy, scaling, or hardware results are reported.

Tempering behavior may be instance-specific.

Official description only; benchmark-diverse validation is required.

**Method or artifact:** Ising-model processing architecture with parallel-momentum tempering.

**Metrics:** Optimization efficiency is claimed qualitatively

**Problem:** Combinatorial optimization can require expensive search over rugged energy landscapes.

**Workload or benchmark:** Combinatorial optimization instances; problem sizes, quality criteria, and hardware are unspecified.

</details>

<span id="paper-dac-2026-research2817"></span>

### EHPC: Efficient Heterogeneous Probabilistic Computing Architecture for Combinatorial Optimization Acceleration

DAC 2026 · Record: `dac-2026-research2817`

[Read the step-by-step explanation](#explanation-dac-2026-research2817)

**Updated source-backed reading card**

Reviewed 2026-09-09. Deepens the EHPC treatment into a paper-level reading; separates volatile-RRAM probabilistic state generation, heterogeneous computation and the fabricated OxRAM-multiplexed Max-Cut circuit from hardware-simulation results, optimization quality, time-to-solution, accelerator silicon overhead and scalability, while preserving the under-1-second, 20x–1,500x and under-1.7% claims with their distinct boundaries.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Combinatorial optimization needs stochastic exploration over irregular solution spaces, but conventional deterministic or software solvers can require substantial time and energy as instance size grows.

**Mechanism / artifact:**

EHPC combines heterogeneous probabilistic computation with volatile RRAM/OxRAM devices; an OxRAM-multiplexed EHPC circuit is described as fabricated and used for a Max-Cut demonstration. The physical-to-probability mapping, update rule, heterogeneity partition, control/data movement, annealing or sampling schedule and host interface are unspecified.

**Workload — the work tested:**

A fabricated Max-Cut demonstration, separate hardware simulations of Max-Cut with better solution quality in under 1 second at equal computational resources, and floorplanning comparisons reporting 20×–1,500× speedups; graph/problem sizes, instance distributions, objective thresholds, seeds, stopping rules, floorplanning modality, number of instances and scaling protocol are unspecified.

**Hardware and manufacturing assumptions:**

Volatile RRAM/OxRAM probabilistic circuit with heterogeneous support; fabrication is claimed for the multiplexed circuit, while the Max-Cut timing and floorplanning comparisons are identified as hardware simulations. Device technology, array size, variability, retention, calibration, peripheral/control area, process, voltage, frequency, simulator, host cost and measurement boundary are unspecified.

**Baseline — the comparison method:**

Existing Max-Cut methods under the stated equal computational resources

Simulated annealing

CPU/GPU solver

Best-performing conventional floorplanning methods

Same objective encoding, instance set, solution-quality target, seeds, stopping rule, computational resources, host/control overhead and time-to-solution boundary are unspecified

**Reported measurements:**

The source reports better simulated Max-Cut solution quality in under 1 second using the same computational resources, floorplanning speedups from 20× to 1,500× versus conventional methods, and floorplan area expansion below 1.7%; the area-expansion value is a floorplanning comparison metric and is not identified as EHPC circuit silicon overhead. Solution quality definition, success probability, convergence, energy, absolute time, device yield and per-instance results are not reported.

**Limits on the conclusion:**

A volatile resistive device's physical variability and retention behavior do not automatically implement a calibrated stochastic update rule. Characterize the probability distribution, temporal correlation, device-to-device variation, temperature/voltage dependence, retention and calibration overhead, then verify that the resulting Markov or annealing process optimizes the intended objective rather than merely producing random exploration.

A fabricated OxRAM-multiplexed circuit establishes a device demonstration, not that the reported under-1-second Max-Cut result or 20×–1,500× floorplanning speedups were measured on that silicon. Separate measured hardware, hardware simulation, CPU/GPU execution and software/control time; report solution quality, optimum gap, success probability, convergence, energy, resource counts and time-to-target at matched stopping criteria and computational budgets.

Floorplan area expansion below 1.7% describes the compared solution or design outcome unless the source defines it as accelerator area. Hold problem encoding, constraints, instance distribution, seeds, precision, host transfer, peripheral/control costs and quality target constant, and test larger and unseen instances. The evidence supports a heterogeneous probabilistic-optimization direction, not demonstrated scalable end-to-end time-to-solution or device-level optimization superiority.

**Source and location**

Evidence tier: Primary captured official DAC description; fabricated proof of concept plus hardware simulation claims, with no full paper extraction, device condition matrix or independent optimization validation. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/presentation/?id=RESEARCH2817&sess=sess174)

Refreshed DAC 2026 official description; existing emerging-and-nonvon-Neumann-compute editorial explanation; captured Problem, Mechanism / artifact, Workload, Hardware, Baseline, Measurements and Limits fields; no full manuscript, per-instance trace, device calibration table or independent reproduction.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** simulated annealing

CPU/GPU solver

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH2817

**Hardware or process assumptions:** Probabilistic or stochastic compute elements with heterogeneous support; device and precision assumptions are unspecified.

**Limits:** No solution quality, time-to-solution, energy, area, scaling, or device results are reported.

Probabilistic behavior may be instance-specific.

Official description only; benchmark-diverse validation is required.

**Method or artifact:** Heterogeneous probabilistic-computing architecture.

**Metrics:** Optimization acceleration is claimed qualitatively

**Problem:** Combinatorial optimization can benefit from stochastic exploration but has irregular workloads and scaling demands.

**Workload or benchmark:** Combinatorial optimization instances; problem sizes, distributions, and hardware are unspecified.

</details>

<span id="paper-dac-2026-research2975"></span>

### iADS: In-Situ Adaptive Diffusion Sampling Architecture Based on Voltage-Tunable P-Bits

DAC 2026 · Record: `dac-2026-research2975`

[Read the step-by-step explanation](#explanation-dac-2026-research2975)

**Updated source-backed reading card**

Reviewed 2026-09-09. Deepens the iADS treatment into a paper-level reading; separates self-compensating voltage-tunable p-bit generation, Gaussian scaling and hardware calibration from binary-to-Gaussian fidelity, diffusion-model quality, device variation, system energy and million-unit fabrication, while preserving the 256-unit prototype, 1,048,576-unit modeled architecture, FID 9.96, 8x and 143x claims with their distinct scopes.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Diffusion sampling needs repeated noise generation with a specified distribution and scale; digital pseudorandom generation and data movement can contribute substantial energy and area.

**Mechanism / artifact:**

iADS combines self-compensating voltage-tunable p-bits with in-situ adaptive Gaussian-noise generation and scaling for diffusion sampling. A 256-p-bit circuit is fabricated for an MNIST generation demonstration; a hardware-calibrated 1,048,576-p-bit architecture is used for the reported CIFAR10 and CelebA-HQ results. The p-bit-to-Gaussian transformation, calibration loop, control, conversion, correlation management and integration with the diffusion model are unspecified.

**Workload — the work tested:**

MNIST generated with the fabricated 256-unit circuit, and CIFAR10 and CelebA-HQ evaluated with the hardware-calibrated million-p-bit architecture; model architecture, sampler, number of diffusion steps, training versus inference boundary, sample count, FID protocol, random-seed policy and CelebA-HQ metrics are unspecified.

**Hardware and manufacturing assumptions:**

Voltage-tunable probabilistic-bit hardware with a fabricated 256-unit prototype and a separately calibrated 1,048,576-unit architecture whose fabrication status is not established; device technology, voltage range, process, temperature, retention, variability, DAC/ADC or conversion circuitry, calibration storage, clocking and system integration are unspecified.

**Baseline — the comparison method:**

Pseudorandom-number generators

Digital diffusion sampling

Fixed stochastic sampler

Same diffusion model, sampler, number of steps, output quality, random-source interface, conversion, control, memory, calibration, technology and full-system energy/area boundary are unspecified

**Reported measurements:**

The source reports CIFAR10 FID 9.96 for the hardware-calibrated million-p-bit architecture, approximately 8× lower energy and roughly 143× lower area than pseudorandom-number generators; FID is not reported for the 256-unit prototype, and the source does not expose distribution error, sample latency, convergence, full diffusion-model energy, peripheral cost, device variation or million-unit fabrication.

**Limits on the conclusion:**

A p-bit is binary and probabilistic, while diffusion sampling requires a continuous-valued noise distribution with the intended mean, scale, independence or correlation structure. Establish the binary-to-Gaussian construction, voltage-to-parameter calibration, temporal/spatial correlation, tail behavior and distribution error across process, voltage and temperature; a visually plausible sample does not prove correct noise statistics.

The fabricated 256-unit MNIST circuit and the hardware-calibrated 1,048,576-unit architecture are different evidence boundaries. Calibration of a modeled or scaled architecture is not proof of million-device fabrication, yield, retention or integrated diffusion operation. Report prototype measurements, architecture extrapolation, calibration cost, device mismatch, drift, conversion/control overhead and failure behavior.

FID 9.96 is a dataset- and protocol-dependent image-distribution metric, not proof of equal task quality or sampler equivalence. Compare the same diffusion model, steps, prompts/data, seeds, sample count and quality metrics against PRNG and fixed-sampler baselines, and include denoising compute, memory, control, conversion and calibration in energy and area. The evidence supports adaptive probabilistic noise hardware, not demonstrated full-system diffusion acceleration or quality-preserving 8×/143× gains.

**Source and location**

Evidence tier: Primary captured official DAC description; fabricated 256 unit prototype plus hardware calibrated scaled architecture claims, with no full paper extraction, million unit silicon evidence or independent system validation. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/presentation/?id=RESEARCH2975&sess=sess174)

Refreshed DAC 2026 official description; existing emerging-and-non-von-Neumann-compute editorial explanation; captured Problem, Mechanism / artifact, Workload, Hardware, Baseline, Measurements and Limits fields; no full manuscript, distribution trace, calibration table or independent diffusion reproduction.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** digital diffusion sampling

fixed stochastic sampler

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH2975

**Hardware or process assumptions:** Probabilistic p-bit hardware with voltage tuning; noise, device, and conversion assumptions are unspecified.

**Limits:** No sample quality, convergence, latency, energy, area, or device-variation results are reported.

P-bit behavior may be technology-specific.

Official description only; calibrated device validation is required.

**Method or artifact:** Voltage-tunable p-bit architecture for adaptive diffusion sampling.

**Metrics:** Sampling efficiency is claimed qualitatively

**Problem:** Diffusion sampling is expensive and may benefit from adaptive stochastic hardware.

**Workload or benchmark:** Diffusion generation or optimization workloads; models, steps, and device parameters are unspecified.

</details>

## What remains to establish

Resolve unspecified workloads, comparison methods, resource budgets, and source locations before generalizing a reported gain. Multiple papers in this selected sample permit comparison of mechanisms, but do not by themselves establish recurrence across years or a long-term trend.

[All subthemes](../expanded-taxonomy-v1.md) · [Research directions](../directions/README.md)
