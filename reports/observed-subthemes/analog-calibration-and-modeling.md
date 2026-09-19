# Analog calibration and modeling

This subject has 2 records in the selected sample. This page explains where it fits, then presents all captured paper evidence without shortening the measurements or limitations.

[Definitions used in the paper records](../reading-guide-v1.md)

## Understand the parent subject first

- [Analog mixed signal and emerging devices](../themes/analog-mixed-signal-and-emerging-devices.md)

## Calibration corrects behavior under stated conditions

An analog device can differ from its intended model because of fabrication variation, operating conditions, or changes over time. Calibration uses observations or previously learned relationships to compensate for those differences. Its usefulness depends on what can be observed, which errors are correctable, and the cost of applying the correction.

The two records in this group target different outputs. One improves analog-to-digital conversion. The other preserves neural-network prediction quality as memory-device behavior changes. Their accuracy metrics and measurement durations must remain separate.

## Blind ADC calibration: what the output metrics mean

An analog-to-digital converter, or ADC, turns an electrical input into numerical samples. Errors can add noise or unwanted signal components. Signal-to-noise-and-distortion ratio measures the desired signal relative to combined noise and distortion. Spurious-free dynamic range measures separation from the largest unwanted spectral component under the stated convention. These are distinct measures, as explained in [Analog Devices' ADC testing guide](https://www.analog.com/en/resources/app-notes/an-835.html).

[Train Once, Calibrate Always](../observed-subthemes/analog-calibration-and-modeling.md#paper-dac-2026-research3087) uses convolutional-recurrent and residual convolutional models for blind calibration. The source describes these as not requiring prior knowledge of the input statistics or error mechanism. That is a methodological claim about required knowledge, not a guarantee that every possible input and unforeseen defect can be corrected.

The official description reports more than 20 dB improvement in both SNDR and SFDR on 65-nm and 28-nm converter test chips of different architectures. An improvement in decibels is a change in a logarithmic ratio, not a percentage-point increase in conversion accuracy. Without the initial and final values, input conditions, and measurement bandwidth, the reported improvements do not fully characterize the calibrated converter.

The evidence includes test-chip measurements, but does not specify the calibration model's integrated hardware implementation, memory, power, latency, or sustained sampling throughput. Correcting stored samples after collection and correcting a live stream at its required rate are different deployment achievements. The title's “train once” wording also needs a held-out evaluation across devices, inputs, and errors before it can support broad reuse without retraining.

<span id="explanation-dac-2026-research3087"></span>

### Train Once, Calibrate Always: blind ADC calibration is an inference problem under missing circuit information

### What ADC calibration is correcting

An ADC maps an analog input to digital samples. Its output can contain static errors, which remain similar for the same input conditions, and dynamic errors, which depend on frequency, signal history, switching behavior or operating state. Calibration applies a correction so the digital output better represents the intended signal.

SNDR compares desired signal power with combined noise and distortion. SFDR compares the desired signal with the largest unwanted spectral component. Both are logarithmic ratios in decibels, and improving them does not directly mean a percentage increase in sample accuracy. A calibration result needs the input signal, bandwidth, sampling condition, initial values and final values attached to the dB change.

### What “blind” means in this method

Traditional algorithmic calibration can use a known error mechanism, circuit model or measured input statistics. A blind learned calibrator attempts to infer the correction from observed ADC samples without being given those specific descriptions. The method uses two model families: ConvRec, a convolutional-recurrent model, and ResConv, a residual convolutional model. Their comparison is an accuracy-versus-hardware-cost tradeoff, not evidence that one architecture is universally better.

The model still needs training data that relate observed outputs to desired behavior. “Input-agnostic” and “error-agnostic” describe information not explicitly supplied at calibration time; they do not mean that the model has seen no distribution, that every unforeseen defect is correctable, or that no adaptation data or compute are required. A defect outside the learned relationship can produce an incorrect correction.

### What the test-chip evidence shows

The captured description demonstrates the framework on two different converter test chips: a 65-nm oversampled time-interleaved band-pass delta-sigma ADC and a 28-nm Nyquist SAR ADC. This is useful evidence that the method was exercised across architectures and process nodes. It is not a controlled comparison of one ADC before and after a single calibration model unless the input, sampling, bandwidth, and error conditions are held equal.

The source reports more than 20 dB improvement in both SNDR and SFDR. Because these are logarithmic ratios, the improvement is not a 20-percentage-point accuracy gain. The source does not provide absolute starting and ending SNDR/SFDR, model size, calibration latency, power, memory, convergence, sampling throughput or the split between offline training and live correction. Measured test-chip output therefore supports analog calibration behavior, not necessarily an integrated real-time production calibrator.

### The evaluation that would establish blind calibration value

Report the model input and target data, calibration sequence length, sampling rate, bandwidth, process/voltage/temperature conditions, static and dynamic error classes, train/test split and held-out chips. Give absolute and dB SNDR/SFDR before and after correction, residual spurs, model memory, compute, latency, energy and sustained sample rate. Test unseen input spectra and error mechanisms, compare ConvRec and ResConv at equal hardware budgets, and distinguish stored-sample post-processing from live streaming correction.

The [Train Once, Calibrate Always](../observed-subthemes/analog-calibration-and-modeling.md#paper-dac-2026-research3087) record describes ConvRec and ResConv blind ML calibration on 65-nm TI-BPADC and 28-nm SAR test chips. The detailed explanation above separates static/dynamic ADC error, SNDR/SFDR meaning, missing-information claims from training dependence, test-chip measurement from integrated deployment, and dB improvement from sample accuracy; this card is the compact evidence record.

## VeRA+: correcting memory drift without retraining on the chip

[VeRA+](../observed-subthemes/analog-calibration-and-modeling.md#paper-dac-2026-research2298) addresses resistance-based memory used for computation. A programmed conductance represents information used in an electrical calculation. If that conductance changes with time, the calculation can change even when the intended stored value has not.

The method reuses shared projection matrices and two drift-specific vectors per drift level, selecting parameters trained offline. The claimed economy is a smaller correction representation and no on-chip retraining or replay. That does not mean no training occurred: the offline preparation remains part of the method. The selection mechanism must also obtain enough information to choose a suitable drift level; its operational details are not exposed here.

The description reports preserving up to 99.77% of drift-free accuracy after ten years of simulated drift. This is relative to the drift-free result, not necessarily 99.77% absolute task accuracy. It also reports over three orders of magnitude lower storage overhead than batch-normalization calibration. That storage comparison does not by itself establish an equivalent energy or latency reduction.

<span id="explanation-dac-2026-research2298"></span>

## VeRA+: a compact drift compensator is useful only when the drift model and IMC boundary are credible

RRAM in-memory computing stores neural weights as conductance and uses array currents to perform multiply-accumulate operations. Conductance drift changes the effective weights after programming, so an inference result can degrade even if the digital model and inputs are unchanged. Compensation must be judged against the drift distribution, readout circuitry, device variation and workload—not only against a software perturbation applied to ideal weights.

VeRA+ is described as reusing shared projection matrices and adding two compact drift-specific vectors per drift level. A drift-aware scheduler trains a small parameter set offline and selects the appropriate set over time without on-chip retraining or data replay. This can reduce storage and adaptation work, but it assumes that the vector correction family captures the device/model error and that the drift level can be identified without an expensive or disruptive measurement. The method must define how vectors compose with positive/negative conductances, ADC/DAC quantization, nonlinearity, noise, stuck devices and spatially correlated variation.

The first gate is device-grounded accuracy. Specify device count, 1T1R array, conductance range, programming distribution, temperature, read voltage, retention, cycle age, drift law and cross-device/chip variation. Fit drift parameters on one population and validate on held-out devices, arrays and time intervals. Report absolute baseline accuracy, task/model, layer-wise and worst-case degradation, calibration/scheduling error, inference energy/latency and accuracy under combined drift, noise, write variation, stuck-at faults and ADC/DAC effects.

The second gate is lifecycle and overhead accounting. Compare retraining, noise-aware training and BN calibration with matched accuracy targets, storage precision, data/replay access, rewriting, calibration time and on-chip resources. Count vector storage, selector metadata, sensing/monitoring, controller logic, periodic reads, programming wear and any array reconfiguration. A small digital compensation vector does not by itself establish lower total energy or endurance cost if the array must be repeatedly observed or rewritten.

The source reports up to 99.77% of drift-free accuracy after ten years of simulated drift, more than three orders of magnitude lower storage overhead than BN calibration, and one-week drift statistics measured on fabricated 1T1R RRAM devices. It does not provide absolute accuracy, device count, temperature, cross-chip variation, extrapolation law, energy, latency, endurance, ADC/DAC conditions or full-array validation. The evidence supports a lightweight vector-based drift-compensation direction, not demonstrated ten-year device retention or complete RRAM-IMC system resilience.

## One week measured and ten years simulated are different evidence

VeRA+ uses one-week drift measurements from fabricated one-transistor/one-resistor devices. Its ten-year result depends on extrapolating a model beyond that measured interval. The simulation is evidence about the model's consequences, not a ten-year device observation.

Temperature, device count, array scale, cross-chip variation, and absolute task accuracy are not supplied in the captured description. Evaluating long-term operation would require checking the extrapolation and the compensation under the conditions the intended system will encounter. The correction's memory traffic, arithmetic, and update policy also need measurement.

## The research question shared by these methods

Both proposals suggest replacing some device-specific correction work with reusable learned compensation. That is a connection inferred from their methods, not a demonstrated universal calibration strategy. A useful comparison would measure residual error on unfamiliar devices and conditions alongside the complete correction cost. It would keep measured duration, simulated duration, offline training, and real-time execution distinct, so that improved accuracy does not conceal an impractical operating requirement.

## Compare the results carefully

First identify the inputs and required output quality. Then identify the limited resource: time, memory, communication, energy, circuit area, or correctness coverage. Ask which part of the method reduces that cost and which new cost it adds. Compare numbers only when the experiments hold these conditions sufficiently similar.

A conference description may explain the proposal while omitting the full experiment. An author preprint link may have been coded from its abstract. The source classification does not by itself establish that every table was read. Missing locations remain visible below.

## Complete captured evidence

These are evidence records, not substitutes for the explanations above. Each record preserves its problem, proposed method, measurements, comparison conditions, and source limits. A populated record does not establish that its mechanism has been fully explained or independently verified.

<span id="paper-dac-2026-research3087"></span>

### Train Once, Calibrate Always: Machine-Learning-Assisted Blind Calibration for Analog-to-Digital Converters

DAC 2026 · Record: `dac-2026-research3087`

[Read the step-by-step explanation](#explanation-dac-2026-research3087)

**Updated source-backed reading card**

Reviewed 2026-09-08. Reconciles the Train Once, Calibrate Always card with the captured official source; explains blind ADC calibration from first principles and separates static/dynamic error, SNDR/SFDR dB metrics, missing-information claims, test-chip evidence, live deployment and generalization limits.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Existing ADC calibration can require known circuit errors or input statistics, limiting correction of unforeseen static and dynamic errors.

**Mechanism / artifact:**

Hybrid convolutional-recurrent ConvRec and residual convolutional ResConv models for blind ADC calibration, with an accuracy-versus-hardware-cost trade-off.

**Workload — the work tested:**

Measured 65-nm oversampled time-interleaved band-pass delta-sigma ADC and 28-nm Nyquist SAR ADC test chips; sampling conditions, input spectra, error injections, model size, split and calibration latency are unspecified.

**Hardware and manufacturing assumptions:**

ADC test chips with ML calibration hardware/software; power, memory, compute, integration, throughput, process/voltage/temperature conditions and live-stream boundary are unspecified.

**Baseline — the comparison method:**

Algorithmic calibration requiring error knowledge

Prior ML calibration requiring input statistics

Baseline SNDR/SFDR, model and hardware parity are unspecified

**Reported measurements:**

The official description reports more than 20 dB improvement in both SNDR and SFDR on the two test chips; absolute values, bandwidth, input conditions, aggregation and logarithmic-ratio reference are unspecified.

**Limits on the conclusion:**

SNDR and SFDR are logarithmic signal-quality ratios, not percentage-point accuracy; without absolute start/end values the dB headline does not fully characterize the converter.

Input/error-agnostic wording describes information supplied to calibration, not a guarantee for every unseen input or defect; training distribution and measurement coverage still determine generalization.

Test-chip output correction does not establish an integrated real-time stream calibrator; model memory, latency, power, convergence and sustained sample rate are not reported.

The official description supplies no held-out-chip protocol, absolute metrics, operating conditions, model cost or independent deployment validation; unforeseen-error correction remains a claim to test.

**Source and location**

Evidence tier: Primary captured official DAC description only; no full paper extraction, calibration model reproduction or independent live stream/generalization validation. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH3087&sess=sess130)

DAC 2026 official description and data/review-packets/dac-2026-research3087.json: ConvRec/ResConv blind calibration; static/dynamic errors; 65-nm TI-BPADC and 28-nm SAR test chips; input/error-agnostic claim; >20 dB SNDR and SFDR improvement.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** algorithmic calibration requiring error knowledge

prior ML calibration requiring input statistics

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH3087&sess=sess130

**Hardware or process assumptions:** Analog-to-digital converter test chips in 65-nm and 28-nm processes with ML calibration hardware/software; power, memory, throughput, and integration details are unspecified.

**Limits:** The description omits absolute SNDR/SFDR, area, power, latency, convergence data, and test-chip operating conditions.

Input/error agnosticism may depend on training distribution and measurement coverage; unforeseen errors are not automatically guaranteed to be corrected.

Official description only; silicon calibration claims require paper-level measurement and generalization checks.

**Method or artifact:** Hybrid convolutional-recurrent and residual convolutional blind calibration models with accuracy-versus-hardware-cost tradeoffs.

**Metrics:** More than 20 dB SNDR improvement

More than 20 dB SFDR improvement

Demonstrated on 65-nm and 28-nm test chips

**Problem:** Existing ADC calibration requires known error mechanisms or input statistics, limiting correction of unforeseen static and dynamic errors.

**Workload or benchmark:** Measured 65-nm TI-BPADC and 28-nm SAR ADC test chips; sampling conditions, error injections, model size, calibration latency, and baselines are unspecified.

</details>

<span id="paper-dac-2026-research2298"></span>

### VeRA+: Vector-Based Lightweight Compensation for Drift-Resilient RRAM In-Memory Computing

DAC 2026 · Record: `dac-2026-research2298`

[Read the step-by-step explanation](#explanation-dac-2026-research2298)

**Updated source-backed reading card**

Reviewed 2026-09-08. Deepens the existing VeRA+ treatment into a paper-level reading; separates shared projection/vector compensation and drift-aware scheduling from device-grounded drift calibration, analog/array nonidealities, lifecycle overhead, extrapolation and ten-year RRAM-IMC conclusions, preserves the 99.77%, three-orders and one-week-measurement claims, and defines the evidence boundary.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

RRAM conductance drift degrades long-term CIM accuracy, while retraining, rewriting and batch-normalization calibration impose storage, energy and adaptation costs.

**Mechanism / artifact:**

Lightweight vector compensation reusing shared projection matrices with two drift-specific vectors per level and offline drift-aware scheduling without on-chip retraining or replay; vector composition, drift sensing, analog nonidealities and selector implementation are unspecified.

**Workload — the work tested:**

RRAM-IMC neural inference under ten-year simulated drift and one-week fabricated 1T1R measurements; model/task, device count, array scale, drift distribution, retention conditions, baseline accuracy and validation split are unspecified.

**Hardware and manufacturing assumptions:**

Fabricated 1T1R RRAM CIM array with conductance drift and offline parameter storage; conductance range, programming/read voltage, temperature, ADC/DAC, noise, endurance, cross-device/chip variation, controller and measurement hardware are unspecified.

**Baseline — the comparison method:**

Retraining

Noise-aware training

Batch-Normalization-based calibration

Same model/task, drift distribution, accuracy target, storage precision, data/replay, rewriting, calibration time, sensing and on-chip resource boundary are unspecified

**Reported measurements:**

The official description reports up to 99.77% of drift-free accuracy after ten years of simulated drift, over three orders of magnitude lower storage overhead than BN calibration, and one-week drift statistics from fabricated 1T1R RRAM; it supplies no absolute accuracy, device count, extrapolation error, energy, latency, endurance, ADC/DAC or full-array result.

**Limits on the conclusion:**

Specify device/array population, conductance, programming, temperature, read voltage, retention, cycle age, drift law and cross-device/chip variation. Fit on one population and validate on held-out devices, arrays and time intervals; report accuracy under drift, noise, write variation, stuck faults and ADC/DAC effects.

Compare retraining, noise-aware training and BN calibration at matched quality, storage, data/replay, rewriting, calibration and on-chip costs. Count vectors, metadata, sensing, monitoring, controller, reads, wear and reconfiguration; digital compensation can shift rather than remove total energy/endurance cost.

The 99.77%, three-orders and one-week-measurement claims lack absolute accuracy, device, temperature, variation, extrapolation, energy, latency, endurance, ADC/DAC and full-array conditions. The evidence supports vector drift compensation, not demonstrated ten-year device retention or complete RRAM-IMC resilience.

**Source and location**

Evidence tier: Primary captured DAC official description plus existing chapter level conceptual discussion; no full paper extraction, held out device validation, long term retention measurement or independent rram imc reproduction. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH2298&sess=sess160)

DAC 2026 official description; existing chapter-level VeRA+ discussion; captured Problem, Mechanism / artifact, Workload, Hardware, Baseline, Measurements and Limits fields; no manuscript pages or reproduced device/IMC campaign.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** retraining

noise-aware training

batch-normalization calibration

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH2298&sess=sess160

**Hardware or process assumptions:** Fabricated 1T1R RRAM CIM array with conductance drift and offline parameter storage; array scale, ADC/DAC, temperature, and endurance are unspecified.

**Limits:** The description omits absolute accuracy, energy, latency, temperature, device count, and cross-chip variation.

Ten-year simulation depends on drift extrapolation from one-week measurements.

Official description only; endurance and accuracy claims require device-level verification.

**Method or artifact:** Lightweight vector compensation with drift-aware scheduling and measured-device drift statistics.

**Metrics:** Up to 99.77% of drift-free accuracy after ten years simulated drift

Over three orders of magnitude lower storage overhead than BN calibration

One-week measured-device drift statistics

**Problem:** RRAM conductance drift degrades long-term CIM accuracy, while retraining, rewriting, and batch-normalization calibration impose storage and energy costs.

**Workload or benchmark:** RRAM IMC neural inference under ten-year simulated drift and one-week fabricated 1T1R measurements; model, task, drift distribution, and baseline details are unspecified.

</details>

## What remains to establish

Resolve unspecified workloads, comparison methods, resource budgets, and source locations before generalizing a reported gain. Multiple papers in this selected sample permit comparison of mechanisms, but do not by themselves establish recurrence across years or a long-term trend.

[All subthemes](../expanded-taxonomy-v1.md) · [Research directions](../directions/README.md)
