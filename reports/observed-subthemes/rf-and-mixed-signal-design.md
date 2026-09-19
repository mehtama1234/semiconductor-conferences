# RF and mixed signal design

This subject has 1 record in the selected sample. This page explains where it fits, then presents all captured paper evidence without shortening the measurements or limitations.

[Definitions used in the paper records](../reading-guide-v1.md)

## Understand the parent subject first

- [Analog mixed signal and emerging devices](../themes/analog-mixed-signal-and-emerging-devices.md)

## Correcting the signal before amplification

A power amplifier increases a signal's power for transmission. Its output may not remain an exact scaled version of its input: the input-output relationship can change with signal level and operating conditions. Digital predistortion modifies the signal before amplification so that the combined digital and amplifier behavior more closely matches the desired output.

The selected paper, [ASG-MOENN](../observed-subthemes/rf-and-mixed-signal-design.md#paper-dac-2026-research656), proposes an adaptive, sparsely gated mixture-of-experts neural predistorter for quadrature switched-capacitor power amplifiers. The captured official description gives no measured RF linearity or implementation results.

## The correction must match the actual operating conditions

A correction learned for one condition may not remain appropriate after the input distribution, output level, or operating environment changes. Adaptive predistortion seeks to respond to such variation. However, adaptation requires some information about the change and a procedure for selecting or updating the correction.

The source does not specify the feedback signal, training procedure, adaptation interval, or supported operating range. It should not be assumed to perform continuous online retraining or to track every possible amplifier change. Those are separate implementation capabilities requiring evidence.

The named amplifier architecture defines the paper's target. Its inclusion does not establish equivalent behavior on every power-amplifier family. The exact device, bandwidth, sampling rate, and operating conditions remain unspecified in the captured record.

## Sparse experts allocate computation selectively

A mixture-of-experts model contains several component models and a mechanism deciding which contribute to an output. Sparse gating selects a subset rather than evaluating all experts in the same way for every input. This offers a way to concentrate computation, but introduces selection and coordination costs.

The potential advantage depends on whether different experts capture useful differences in the signal or operating regime. Selection mistakes can choose an inappropriate correction. Switching among experts can also need evaluation for consistency across a continuous signal stream. These are validation questions, not reported failures of ASG-MOENN.

The description does not identify the expert count, gating features, activation pattern, or combination rule. A reduced number of active experts therefore cannot be translated into a numerical energy or latency saving from the available evidence.

## Signal quality is not a generic model-accuracy score

A predistorter must be judged on the resulting transmitted signal, not only its internal prediction loss. Error-vector magnitude compares a measured signal representation with its intended reference under a specified procedure. Adjacent-channel leakage concerns unwanted power outside the intended channel relative to the defined channel measurements.

These metrics examine different consequences of distortion. Improving one does not automatically establish compliance with every communication requirement or comparable performance across bandwidths. Their measurement settings and reference conditions must accompany the numbers.

The record lists EVM and ACLR among missing evidence and reports neither. It also supplies no output-power conditions, spectral results, or measured comparison against the single-model and dense-expert baseline categories in the coding.

## Real-time implementation adds another requirement

The digital correction must produce samples quickly enough for its intended stream. Mean model-evaluation time alone may not establish sustained throughput or acceptable worst-case latency, particularly if selected experts have different costs.

The complete implementation includes gating, expert computation, data movement, and any feedback or adaptation. Memory and power needed by inactive experts can also remain relevant even when they are not evaluated on a particular input. The source provides no hardware, energy, latency, or adaptation measurements.

A fair efficiency comparison would hold signal quality, input waveform, amplifier conditions, and throughput requirements fixed. Otherwise an apparently cheaper predistorter may simply deliver a weaker correction or process an easier workload.

<span id="explanation-dac-2026-research656"></span>

## ASG-MOENN: sparse adaptive predistortion helps only when RF quality and worst-case timing survive

A power amplifier is nonlinear: its output is not always a scaled copy of its input, and the distortion can change with output power, frequency, temperature, memory effects and device state. Digital predistortion applies a learned inverse-like correction before the PA so that the combined input–PA path is closer to the desired transmitted waveform. The correction must be evaluated at the RF output, not only by the neural network's internal loss.

ASG-MOENN is described as a mixture-of-experts digital predistorter for quadrature switched-capacitor power amplifiers. Its first adaptation conditions the input using SCPA physical principles; a sparse gate then selects both which experts to activate and how many are needed using a cumulative-confidence criterion. This can scale average computation with operating state. It does not specify expert count, gate features, confidence calibration, combination rule, hysteresis, update procedure, feedback path or hardware mapping.

The first gate is RF linearity. Define the waveform, bandwidth, modulation, sample rate, output-power range, EVM/ACLR/NMSE procedures, reference signal and spectral mask. Measure the PA output by power level, bandwidth, temperature, device instance and memory condition against a single neural model and dense MoE at matched quality. A lower expert count is not a benefit if it worsens EVM, increases adjacent-channel leakage or changes the accepted output power.

The second gate is adaptive selection and stream continuity. Report expert-selection error, confidence calibration, fallback, active-count distribution, switching transients, hysteresis, worst-case active count and behavior on unseen power levels, drift, memory effects and device variation. A gate can select an appropriate expert on average while making occasional discontinuities in a continuous RF stream. Adaptation also needs a defined feedback signal, update interval, calibration/retraining cost and convergence criterion.

The real-time boundary includes conditioning, gating, expert memory, expert evaluation, data movement, DAC/ADC and feedback/adaptation. Measure sustained sample throughput, p50/p95/p99 and worst-case latency, energy, memory, hardware utilization and deadline misses. Compare single, dense and sparse predistorters with the same SCPA, waveform, RF quality target, sample rate and worst-case deadline; average computational load is not a real-time guarantee.

The official description claims superior linearization versus a SOTA baseline and up to 50% lower average computational load across a 30-dB dynamic power range. It does not expose EVM, ACLR, NMSE, output power, spectral regrowth, absolute latency, throughput, energy, expert traces, adaptation time or hardware conditions. The evidence supports SCPA-aware adaptive sparse DPD, not demonstrated measured RF linearity, safe out-of-distribution adaptation or a quantified real-time efficiency gain.

## The longer-term research question

ASG-MOENN motivates matching correction complexity to changing amplifier behavior rather than applying identical computation to every case. A convincing evaluation would show measured output quality across declared operating changes, the time and cost of adaptation, and complete real-time resource use.

The current official description supports explaining that proposed approach. It does not establish a measured linearity improvement, a quantified efficiency gain, or transfer beyond the specified amplifier class. Those conclusions remain dependent on RF measurements and implementation conditions not exposed in the captured source.

## Compare the results carefully

First identify the inputs and required output quality. Then identify the limited resource: time, memory, communication, energy, circuit area, or correctness coverage. Ask which part of the method reduces that cost and which new cost it adds. Compare numbers only when the experiments hold these conditions sufficiently similar.

A conference description may explain the proposal while omitting the full experiment. An author preprint link may have been coded from its abstract. The source classification does not by itself establish that every table was read. Missing locations remain visible below.

## Complete captured evidence

These are evidence records, not substitutes for the explanations above. Each record preserves its problem, proposed method, measurements, comparison conditions, and source limits. A populated record does not establish that its mechanism has been fully explained or independently verified.

<span id="paper-dac-2026-research656"></span>

### ASG-MOENN: Adaptive Sparsely-Gated Mixture of Experts Neural Network for Digital Predistortion in Quadrature Switched-Capacitor Power Amplifiers

DAC 2026 · Record: `dac-2026-research656`

[Read the step-by-step explanation](#explanation-dac-2026-research656)

**Updated source-backed reading card**

Reviewed 2026-09-09. Deepens the ASG-MOENN treatment into a paper-level reading; separates SCPA-aware conditioning, adaptive sparse expert selection and cumulative-confidence compute scaling from RF linearity, expert-selection errors, adaptation stability, real-time worst-case cost and measured PA validation, while preserving the 30-dB and 50% computational-load claims.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Quadrature switched-capacitor power amplifiers exhibit nonlinear behavior that changes across output-power levels; a fixed-complexity digital predistorter can waste computation at lower power while a sparse adaptive model can select an unsuitable correction under changing RF conditions.

**Mechanism / artifact:**

ASG-MOENN is described as a sparsely gated mixture-of-experts digital predistorter with dual adaptation: conditioning the input using SCPA physical principles, then selecting both expert identity and expert count using a cumulative-confidence criterion; expert architecture, gate inputs, confidence calibration, combination rule, adaptation/update procedure and hardware mapping are unspecified.

**Workload — the work tested:**

Wide dynamic-power-range quadrature switched-capacitor PA signals across a claimed 30-dB range; carrier/bandwidth, modulation, sampling rate, output power, memory effects, temperature/voltage, device instances, train/test operating points, expert count and baseline tuning are unspecified.

**Hardware and manufacturing assumptions:**

Real-time digital predistortion coupled to a quadrature SCPA; PA process/device, RF front end, DAC/ADC, sample rate, FPGA/ASIC/CPU implementation, memory, clock, feedback observation, latency budget, power and instrumentation are unspecified.

**Baseline — the comparison method:**

SOTA single neural predistorter

Dense mixture-of-experts predistorter

Fixed-complexity digital predistortion

Same SCPA, waveform, bandwidth, output-power range, RF metrics, training/adaptation budget, sample rate, hardware, quality target and worst-case timing boundary are unspecified

**Reported measurements:**

The official description claims superior linearization versus a SOTA baseline while reducing average computational load by up to 50% across a 30-dB dynamic power range; it does not report EVM, ACLR, NMSE, output power, spectral regrowth, absolute latency, throughput, energy, expert-selection error, adaptation time or per-operating-point results.

**Limits on the conclusion:**

The predistorter must be judged at the PA output, not only by neural prediction loss. Define EVM/ACLR/NMSE procedures, channel bandwidth, reference waveform, output power and spectral mask, then report linearity and quality by power level, bandwidth, modulation, temperature and device. A gate can reduce computation while selecting an expert that worsens the transmitted signal or violates an adjacent-channel limit.

Cumulative-confidence gating has two costs: selection can be wrong, and the number of active experts can vary over a continuous stream. Report expert precision/recall or fallback, switching transients, confidence calibration, hysteresis, sequence continuity, worst-case active count and adaptation behavior under unseen power levels, memory effects, drift and device variation. Average load is not a real-time guarantee.

Include gating, expert memory, feature conditioning, expert evaluation, data movement, feedback/adaptation, retraining and calibration in latency, energy and hardware cost. Compare single, dense and sparse models at matched RF quality, sample rate and worst-case deadline. The evidence supports SCPA-aware adaptive sparse DPD, not demonstrated measured RF linearity, safe out-of-distribution adaptation or a quantified real-time efficiency gain.

**Source and location**

Evidence tier: Primary captured official DAC description plus existing authored dpd discussion; no full paper extraction, measured RF validation, hardware timing/power study or independent dynamic range adaptation evaluation. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH656)

DAC 2026 official description; existing RF-and-mixed-signal-design chapter framing; captured Problem, Mechanism / artifact, Workload, Hardware, Baseline, Measurements and Limits fields; no manuscript pages, RF spectrum/EVM/ACLR table, expert trace or reproduced SCPA measurement.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** single neural predistorter

dense MoE predistorter

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH656

**Hardware or process assumptions:** Digital predistortion system coupled to RF PA; bandwidth, sampling, and implementation assumptions are unspecified.

**Limits:** No EVM, ACLR, power, latency, energy, or adaptation results are reported.

Sparse experts may fail under out-of-distribution RF conditions.

Official description only; measured RF validation is required.

**Method or artifact:** Adaptive sparsely gated MoE neural predistorter.

**Metrics:** Predistortion efficiency and linearity are claimed qualitatively

**Problem:** Power-amplifier nonlinearities vary with operating conditions and require efficient digital predistortion.

**Workload or benchmark:** Quadrature switched-capacitor PA signals; RF conditions, hardware, and baselines are unspecified.

</details>

## What remains to establish

Resolve unspecified workloads, comparison methods, resource budgets, and source locations before generalizing a reported gain. This subject is represented by one paper and supports a case study, not evidence of recurrence or a long-term trend.

[All subthemes](../expanded-taxonomy-v1.md) · [Research directions](../directions/README.md)
