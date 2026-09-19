# Analog and mixed signal synthesis

This subject has 1 record in the selected sample. This page explains where it fits, then presents all captured paper evidence without shortening the measurements or limitations.

[Definitions used in the paper records](../reading-guide-v1.md)

## Understand the parent subject first

- [Analog mixed signal and emerging devices](../themes/analog-mixed-signal-and-emerging-devices.md)

## The actual subject: designing with noisy electrical values

The taxonomy calls this subject analog and mixed-signal synthesis, but its one captured paper concerns noise modeling and joint design exploration. That is narrower than automatically generating a complete circuit from a specification. A modeling framework can help choose a configuration without producing a manufacturable layout.

An analog computation represents a value through an electrical quantity, such as voltage, current, or charge. The intended result and unwanted electrical variation are then present in the same quantity. A later digital conversion does not recover information already lost to that variation; it assigns a digital value to what the converter actually receives.

In-pixel computing performs some computation within an image sensor's pixels. Its attraction is that information can be processed before sending every raw pixel value elsewhere. Whether this saves total energy depends on the required readout, conversion, communication, and remaining computation. Moving an operation into a pixel does not make those other costs disappear.

## Why one generic noise number is insufficient

Noise can differ in origin and behavior. Thermal noise arises from random thermal motion of charge carriers. Shot noise reflects the discreteness of charge transport in relevant current flows. Random telegraph noise involves switching between electrical states, often associated with charge trapping and release. Device mismatch is different: nominally identical devices can have different parameters, producing differences that persist rather than changing independently at every sample.

Those distinctions affect a simulation. A fixed offset repeated across many inputs is not equivalent to fresh random error on every operation. Likewise, errors shared by several pixels need not behave like independent errors of the same individual magnitude. A model must specify when errors change, where they are shared, and how their size depends on operating conditions.

Signal-to-noise ratio compares wanted signal power with noise power. It describes an electrical relationship, not directly the probability of a correct classification. The same electrical error can matter differently for different inputs or computations. Both the electrical model and its effect on the application need evaluation.

<span id="explanation-dac-2026-research1152"></span>

## NoiseXplore: how device noise becomes a system-level design variable

### The design problem crosses several abstraction levels

An in-pixel computing array performs part of a machine-learning operation in or near the image-sensor pixels. A pixel may encode a sensed value as charge or voltage, combine it with stored weights or signals, and pass the result to later circuitry. The computation is attractive because raw sensor values do not all need to travel to a separate digital processor. The same location also creates a direct failure path: device variation and electrical noise perturb the value before the neural-network decision is complete.

The design question is therefore not simply whether a transistor is fast or whether a circuit has a high nominal signal-to-noise ratio. It is whether a particular device technology, pixel circuit, array configuration, conversion path and neural model jointly meet the required application quality and rate. NoiseXplore is described as a design-technology co-optimization framework that connects those levels before a physical implementation is chosen.

### Noise sources change the meaning of an error

Thermal noise is associated with random electrical fluctuations caused by temperature. Shot noise results from the discrete nature of charge transport. Random telegraph noise can produce changes associated with a device switching between electrical states, often through charge trapping and release. Device mismatch is a difference between nominally identical devices; it can persist across repeated evaluations of the same device instead of behaving like an independently redrawn sample.

These sources cannot be represented faithfully by one undifferentiated random number. A model must specify the variable being perturbed, the time scale at which it changes, whether it is shared across pixels, and how it depends on bias, temperature, geometry or operating point. A persistent offset can be learned or calibrated differently from a fresh sample-to-sample fluctuation. A correlated array error can affect a whole feature pattern differently from independent per-pixel noise.

The official description names all four sources but does not give the equations, fitted parameters, device geometry, process corner, voltage, temperature, correlation model or calibration procedure. Those missing details are part of the physical meaning of the reported application result.

### The framework needs a path from device statistics to classification

At the circuit level, signal-to-noise ratio compares wanted signal power with noise power. That quantity is useful for characterizing an electrical path, but it is not the same as classification accuracy. A neural network may tolerate some perturbations and be sensitive to others depending on where they enter, their distribution, and the input class.

NoiseXplore is described as connecting physics-grounded noise models to device-aware SNR estimation and neural-network co-simulation. In a complete flow, the device model produces a noise realization or distribution, the circuit model maps that disturbance through sensing and in-pixel computation, and the neural model consumes the resulting values. The final accuracy then reflects the interaction between electrical error and learned decision boundaries rather than a generic SNR threshold.

That connection also creates evaluation obligations. Training with one noise distribution and testing with the same distribution can measure adaptation to a model rather than robustness to the physical device. The test must state whether noise is applied during training, which device instances are held out, whether errors are correlated, and whether the classification result includes ADC, readout and remaining digital computation.

### NeuroSim supplies a circuit-level performance model

The official description places the circuit model inside NeuroSim. A circuit-level model can estimate effects such as operation cost, array behavior and interface activity without requiring every design-space point to be fabricated. Its role in this framework is to connect a candidate device and pixel configuration to larger-array and neural-network consequences.

This is a modeling boundary, not a silicon measurement. A NeuroSim estimate is only as faithful as its cell model, peripheral model, technology parameters, array assumptions and treatment of nonidealities. In-pixel computing can reduce movement of raw data while still paying for conversion, accumulation, buffering, control, calibration and output communication. A framework that reports frames per second must define which of these operations are inside the time boundary.

### Bayesian exploration chooses which configurations to evaluate

The design space contains several coupled choices: device and process parameters, pixel-circuit choices, array-level settings, noise conditions and neural-network operating choices. Exhaustively evaluating every combination may be expensive. Bayesian design-space exploration uses previous evaluated configurations to select the next configuration expected to improve or clarify the objective.

This search method changes the allocation of simulation effort; it does not make the objective or physical model correct. The acquisition rule, initial samples, number of evaluations, constraints, random seeds and stopping condition determine what the search can discover. A reported optimum is conditional on the modeled design space and the search budget. It is not evidence that no better physical configuration exists outside the explored variables.

### What the official case study reports

NoiseXplore is demonstrated on a noise-sensitive one-transistor fully depleted silicon-on-insulator in-pixel-computing architecture. The description reports an optimized configuration reaching 50 frames per second and 86.8% classification accuracy on a three-class subset of CIFAR-10: airplane, car and ship.

The denominator matters. CIFAR-10 has ten classes, while this reported result uses three. The accuracy cannot be read as a full-CIFAR-10 result, and frames per second cannot be compared with another pipeline until image size, clock or simulation boundary, preprocessing, output conversion, model size and hardware implementation are matched. The description supplies no baseline accuracy, energy per frame, area, SNR margin, classification model, array dimensions or number of Bayesian evaluations.

### What NoiseXplore establishes and what remains conditional

The official record supports a mechanism-level claim: device-specific noise sources can be carried into circuit and neural-network evaluation, and Bayesian DTCO can search configurations using those cross-layer estimates. It supports the narrower case-study claim that one reported 1T FDSOI in-pixel configuration reached 50 fps and 86.8% accuracy on the stated three-class subset.

It does not establish a fabricated-chip result, a full ten-class accuracy result, an energy advantage, a general noise model, or a universally optimal device/circuit configuration. The conclusion remains conditional on noise equations and parameters, process and operating conditions, NeuroSim fidelity, network training and test protocol, conversion and peripheral costs, and Bayesian search coverage. A serious follow-up needs held-out device conditions, explicit noise correlations, absolute energy/area/latency, matched baselines, a complete-frame boundary, and silicon or independently calibrated circuit validation.

**Primary source read:** [official DAC NoiseXplore record](https://63dac.conference-program.com/presentation/?id=RESEARCH1152&sess=sess123), which supplies the four named noise sources, device-aware SNR and neural co-simulation, NeuroSim integration, Bayesian DTCO, 1T FDSOI case study, 50 fps and 86.8% three-class CIFAR-10 result. The target manuscript, equations, device parameters, search budget, artifact and silicon measurements were not recovered; no related DTCO paper was substituted.

## What NoiseXplore actually proposes

[NoiseXplore](../observed-subthemes/analog-and-mixed-signal-synthesis.md#paper-dac-2026-research1152) combines device-aware noise models, signal-to-noise estimation, neural-network co-simulation, NeuroSim circuit modeling, and Bayesian design-technology exploration. Bayesian search uses observations from evaluated configurations to decide which configuration to try next; it is a search strategy, not an assurance that the physical model is correct.

The official description names thermal, shot, random telegraph, and mismatch effects. Its example uses single-transistor, fully depleted silicon-on-insulator in-pixel computing. Fully depleted silicon-on-insulator describes a transistor technology using a thin active silicon body above an insulating layer; the description does not provide its exact device geometry.

The reported configuration reaches 50 frames per second and 86.8% classification accuracy on only the airplane, car, and ship subset of CIFAR-10. This is not a full ten-class result. The description does not establish fabricated-chip measurement, baseline accuracy, total energy, or the search budget. [Official NoiseXplore description](https://63dac.conference-program.com/presentation/?id=RESEARCH1152&sess=sess123).

## How to judge a selected configuration

First, separate model calibration from model validation. Parameters fitted to one set of device observations should be checked on other observations. Otherwise, good agreement may only show that the fitting procedure reproduced its inputs. Relevant checks include different operating voltages, temperatures, device instances, and signal levels, according to the intended deployment.

Second, preserve the path from electrical error to application output. State where modeled noise enters the computation and whether training used the same noise distribution as evaluation. A comparison should distinguish an improvement due to better hardware settings from one due to retraining the network or changing the task.

Third, account for a complete frame. Report the image dimensions, processing performed, peripheral circuits, remaining digital work, and time boundary. Frames per second alone cannot establish latency per input, energy per frame, or superiority to another sensor pipeline.

Finally, compare configurations under the same application requirement. A lower-energy design with unacceptable accuracy is not interchangeable with one that meets the requirement. Conversely, additional accuracy may have little value if it exceeds the requirement at excessive energy or area cost. These are evaluation questions for the recovered paper, not numerical outcomes asserted by the short description.

## Evidence and longer-term interpretation

The conceptual direction is to let device behavior influence design choices before committing to an implementation. This single record supports that case study, not a measured historical increase in its adoption. Exact paper pages, noise distributions, circuit conditions, independent device validation, and full cost accounting remain missing. The refreshed official source was checked on 2026-09-07; no manuscript-level or silicon-level verification is claimed here.

## Compare the results carefully

First identify the inputs and required output quality. Then identify the limited resource: time, memory, communication, energy, circuit area, or correctness coverage. Ask which part of the method reduces that cost and which new cost it adds. Compare numbers only when the experiments hold these conditions sufficiently similar.

A conference description may explain the proposal while omitting the full experiment. An author preprint link may have been coded from its abstract. The source classification does not by itself establish that every table was read. Missing locations remain visible below.

## Complete captured evidence

These are evidence records, not substitutes for the explanations above. Each record preserves its problem, proposed method, measurements, comparison conditions, and source limits. A populated record does not establish that its mechanism has been fully explained or independently verified.

<span id="paper-dac-2026-research1152"></span>

### Noisexplore: A Device-Aware Hierarchical Noise Modeling and DTCO Framework for Analog In-Pixel Computing Architectures

DAC 2026 · Record: `dac-2026-research1152`

[Read the step-by-step explanation](#explanation-dac-2026-research1152)

**Updated source-backed reading card**

Reviewed 2026-09-08. Re-reads the official DAC NoiseXplore description and expands the mechanism from device noise through SNR, neural co-simulation, NeuroSim and Bayesian DTCO; preserves the three-class CIFAR-10 denominator and missing physical conditions.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Analog in-pixel computing can reduce raw-data movement for edge AI but device and circuit noise can perturb the computed value and reduce classification accuracy; existing flows lack cross-layer device-aware optimization.

**Mechanism / artifact:**

NoiseXplore integrates physics-grounded thermal, shot, random-telegraph and device-mismatch noise models, device-aware SNR estimation, neural-network co-simulation, NeuroSim circuit-level modeling and automated Bayesian design-technology co-optimization.

**Workload — the work tested:**

Noise-sensitive one-transistor fully depleted silicon-on-insulator in-pixel computing for airplane/car/ship three-class classification using a subset of CIFAR-10.

**Hardware and manufacturing assumptions:**

1T FDSOI analog in-pixel computing; exact device geometry, array, voltage, temperature, process corner, peripheral circuits, ADC/readout path, neural model, noise correlations and NeuroSim configuration are unspecified in the accessible description.

**Baseline — the comparison method:**

Existing design flows without comprehensive device-aware noise modeling

The reported optimized configuration, although no numerical baseline accuracy, energy or area comparison is supplied

**Reported measurements:**

The official record reports 50 frames per second and 86.8% classification accuracy for the airplane/car/ship three-class CIFAR-10 subset.

The description reports integration of four noise-source models, device-aware SNR/neural co-simulation, NeuroSim and Bayesian DTCO, but supplies no noise margin, energy/frame, area, search budget or silicon measurement.

**Limits on the conclusion:**

The 86.8% result is a three-class subset, not full ten-class CIFAR-10; frames per second has no comparable boundary without image size, preprocessing, conversion, remaining digital work and hardware conditions.

Noise equations, fitted parameters, temporal and spatial correlations, process/voltage/temperature conditions, calibration, ADC/peripheral cost, neural training protocol and Bayesian acquisition/search budget are not reported in the official source.

The record supports a modeled case study, not fabricated-chip validation, general noise-model validity, energy superiority or a globally optimal device/circuit choice. The target manuscript and artifact were not recovered and no related DTCO paper was substituted.

**Source and location**

Evidence tier: Official DAC research manuscript description; mechanism level reading, target evaluation and execution unavailable. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/presentation/?id=RESEARCH1152&sess=sess123)

Official DAC research-manuscript description: four noise sources, device-aware SNR and neural co-simulation, NeuroSim circuit modeling, Bayesian DTCO, 1T FDSOI case study, 50 fps and 86.8% three-class CIFAR-10 result. No target-manuscript pagination or quantitative condition tables were available.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** existing design flows without comprehensive device-aware noise modeling

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH1152&sess=sess123

**Hardware or process assumptions:** 1T FDSOI analog in-pixel computing architecture with thermal, shot, RTN, and mismatch sources; array dimensions, voltage, process corner, and NeuroSim configuration are unspecified.

**Limits:** The three-class subset is not full CIFAR-10 and no baseline accuracy, energy, area, or noise-margin comparison is supplied.

Noise distributions, process conditions, ADC/peripheral costs, and Bayesian search budget are unspecified.

Official description only; headline metrics require paper-level verification.

**Method or artifact:** Physics-grounded hierarchical noise models, device-aware SNR and neural co-simulation, NeuroSim circuit modeling, and automated Bayesian DTCO exploration.

**Metrics:** 50 frames per second

86.8% CIFAR-10 accuracy on a three-class subset

**Problem:** Analog in-pixel computing is energy-efficient for edge AI but device and circuit noise can degrade accuracy, while existing flows lack device-aware cross-layer optimization.

**Workload or benchmark:** Noise-sensitive 1T FDSOI analog in-pixel computing for CIFAR-10 airplane/car/ship three-class classification.

</details>

## What remains to establish

Resolve unspecified workloads, comparison methods, resource budgets, and source locations before generalizing a reported gain. This subject is represented by one paper and supports a case study, not evidence of recurrence or a long-term trend.

[All subthemes](../expanded-taxonomy-v1.md) · [Research directions](../directions/README.md)
