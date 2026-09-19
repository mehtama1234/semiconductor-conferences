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
