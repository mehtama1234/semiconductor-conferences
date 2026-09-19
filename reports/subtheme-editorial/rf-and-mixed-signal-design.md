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
