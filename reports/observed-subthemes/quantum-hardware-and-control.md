# Quantum hardware and control

This subject has 4 records in the selected sample. This page explains where it fits, then presents all captured paper evidence without shortening the measurements or limitations.

[Definitions used in the paper records](../reading-guide-v1.md)

## Understand the parent subject first

- [Analog mixed signal and emerging devices](../themes/analog-mixed-signal-and-emerging-devices.md)

## Two different interfaces determine whether the computation works

A quantum processor needs classical electronics to interpret measurements and a compiler to translate intended operations into a feasible device schedule. These are different tasks. Faster measurement classification can shorten one part of the control path; a better schedule can reduce the number of sequential operations. Neither result alone establishes a more accurate complete computation.

A physical qubit is a device used to hold quantum information. A logical qubit is information encoded across physical qubits so that specified errors can be detected and corrected. Error correction consumes physical qubits, measurements, classical processing, and time. Its benefit must exceed the errors and costs introduced by those additional operations.

This subject contains two readout papers and two compilation papers. Three version-1 manuscripts were recovered; they predate the conference edition, so identical camera-ready contents are not established. NIAQ remains description-backed. The findings below supersede conflicting omissions and interpretations in the original cards, whose source records still need reconciliation.

<span id="explanation-dac-2026-research1200"></span>

### NIAQ: adaptive readout must track real drift without using unavailable labels or hiding recalibration cost

#### What qubit readout does

Readout turns an analog measurement signal into a classical label, such as the state called zero or one. The signal is noisy, so the system needs a discriminator: a threshold, statistical model or neural model that maps the observed trace to a label. The signal distribution can change because of the qubit, control electronics, temperature, calibration state or other operating conditions.

A fixed discriminator assumes that the mapping from signal to state remains suitable. An adaptive discriminator tries to estimate how that mapping changes and update its decision. The update is only valid if the information used for adaptation would be available during operation. If the method needs fresh labels, the experiment must state how those labels are obtained and what measurement or calibration cost they impose.

#### What the Kalman and neural parts do

A Kalman filter maintains an estimate of a changing hidden state using a prediction and a new observation, weighted by assumed uncertainty. It can follow gradual drift when the state-transition and noise models fit the device. It can lag a sudden change, overreact to noise or become miscalibrated when its uncertainty assumptions are wrong.

The neural discriminator then maps the observed readout features to state labels. The two parts have different roles: the filter estimates change, while the discriminator makes the classification decision. The paper-level claim must identify the signal fed to each part, the update interval, the label source, the training or calibration rule, and how the system behaves when drift is faster than the update loop.

#### How to read the reported results

The official description reports 88% accuracy versus 61% for a baseline on a multi-qubit dataset described as equivalent to one day's runtime, a 19× lower degradation rate, and post-synthesis 28 nm CMOS results of 148 mW and 5 ns delay. These numbers answer different questions. Accuracy measures classification under the stated dataset. Degradation rate describes change over time, but its absolute or relative convention must be defined. Power and delay describe a stated synthesized hardware result, not automatically a fabricated continuously operating readout chain.

An adequate long-horizon test should report accuracy over time, the worst intervals, recovery after an abrupt drift, calibration interruptions, shot noise, label availability and adaptation overhead. It should use time-ordered evaluation so that future drift information does not leak into the past, and it should compare static calibration and uncorrected readout under the same device and trace conditions.

The captured DAC description supports Kalman-assisted adaptive qubit readout with the reported accuracy, degradation and post-synthesis hardware figures. It does not fully define the drift construction, degradation convention, calibration cost, delay boundary, ADC/control path or fabricated-silicon status. The evidence supports an adaptive-readout direction and stated results, not general long-term reliability or transferable hardware superiority.

[Observed paper card](../observed-subthemes/quantum-hardware-and-control.md#paper-dac-2026-research1200)

## NIAQ: follow changes in the measurement signal over time

Readout converts a physical measurement into a classical label. The electronics receive a noisy signal rather than a perfectly separated zero or one. A discriminator is the rule or trained model that assigns the label. Even if that rule works initially, a slowly changing signal distribution can make yesterday's decision boundary inaccurate today.

[NIAQ](../observed-subthemes/quantum-hardware-and-control.md#paper-dac-2026-research1200) combines Kalman filtering for drift tracking with a multilayer neural discriminator. Its official description reports 88% accuracy versus 61% for a baseline on a multi-qubit dataset described as equivalent to one day's runtime, with a 19× lower degradation rate. Post-synthesis 28 nm CMOS results report 148 mW and 5 ns delay, with 7.7× power and 6.4× latency improvements against the stated prior design.

These are not evidence of a fabricated chip running continuously for a day. The description leaves the dataset's time construction, drift distribution, reference labels, calibration cost, and precise delay boundary unresolved. The degradation metric is expressed in percent per hour, but its absolute-versus-relative convention is not specified here. [Official DAC description](https://63dac.conference-program.com/presentation/?id=RESEARCH1200&sess=sess135).

A Kalman filter updates an estimate using both a prediction and a new observation, with their assumed uncertainties determining how much each contributes. It can track gradual change when its model is suitable. A sudden change or a wrong uncertainty model can instead make it lag or overreact.

The relevant experiment must separate genuine drift from ordinary shot-to-shot noise. A shot is one preparation-and-measurement trial. Adaptation should improve later predictions without using labels that would be unavailable during normal operation. The cost of obtaining any reference measurements must also be counted.

Long-term reliability needs more than a final average. Report accuracy over time, recovery after abrupt changes, the worst intervals, and how often recalibration interrupts useful work. A lower degradation slope does not guarantee acceptable accuracy if the starting value is already too low for the intended computation.

## LUNA: compress the trace before implementing the classifier in logic

A sampled readout trace contains many numbers. Passing every sample into a large classifier can require substantial hardware. Preprocessing can combine samples into fewer features, but this discards information. The useful question is which information can be removed while preserving the distinction between the prepared states.

[LUNA](../observed-subthemes/quantum-hardware-and-control.md#paper-dac-2026-research2914) sums non-overlapping signal windows and maps a quantized LogicNet classifier into FPGA lookup-table logic (Section 3, PDF pages 3–5). Table 4, page 6, reports 6,095 LUTs for its area-oriented design versus 66,600 for the baseline. Its latency-oriented design reports 22.10 ns versus 32 ns, at 95.969% versus 96.000% readout fidelity. These are different selected designs, not one configuration achieving every best value.

Sections 3.6–4, page 5, use post-placement-and-routing reports on XCZU49DR and a public superconducting-qubit dataset split into 90,000 training and 10,000 test examples. The same stated split informs architecture search; a separate untouched final evaluation set is not documented there. Reported processing latency must not be equated with the full analog acquisition and feedback loop.

Table 3 also selects pre-accumulation shift 9 despite Table 2 listing 2–7. That search-space discrepancy requires clarification. [Version-1 manuscript, Sections 3–5 and Tables 2–4](https://arxiv.org/pdf/2512.07808v1#page=3).

A lookup table implements a Boolean function of a limited number of input bits. Constraining the number of connections and bits lets a trained neuron become a manageable logic function. Without those constraints, the number of possible input combinations grows rapidly. Removing multipliers therefore transfers design pressure to representation precision, connectivity, and logic capacity.

Readout fidelity here is a balanced classification measure: one minus the average of the two state-confusion probabilities. It is not the fidelity of an entire quantum state or algorithm. Keeping these meanings distinct is necessary when connecting readout improvements to error correction.

Architecture search repeatedly chooses designs using observed performance. If the final reporting set also guided those choices, its score can be optimistic even when model training used separate examples. A new measurement session or held-out device is a stronger test of deployment behavior than repeatedly scoring the same traces.

<span id="explanation-dac-2026-research2914"></span>

### LUNA: reducing FPGA readout logic is useful only when the selected classifier preserves fidelity at the complete measurement boundary

#### What the readout pipeline receives

Qubit readout begins with an analog signal sampled over time. The classifier must distinguish the prepared states from noisy traces. LUNA sums non-overlapping signal windows before applying a quantized LogicNet classifier mapped into FPGA lookup-table logic. Windowing reduces the number of values presented to the classifier, but it can discard timing or shape information that helped separate the states.

Quantization also changes the representation. A lookup table implements a Boolean function over a finite number of input bits, so the design must choose precision, connectivity, table size and feature order. Removing multipliers transfers cost into LUT capacity, routing, input precision and the information lost by the feature transform.

#### What the selected measurements mean

The recovered manuscript reports an area-oriented design using 6,095 LUTs versus 66,600 for its baseline. A latency-oriented design reports 22.10 ns versus 32 ns, at 95.969% versus 96.000% readout fidelity. These are different selected designs; the numbers must not be combined into a claim that one configuration achieves the smallest area, lowest latency and highest fidelity simultaneously.

The fidelity is a balanced classification measure based on the two state-confusion probabilities. It is not the fidelity of an entire quantum state or algorithm. The latency is a reported processing boundary after placement and routing on an XCZU49DR FPGA, not automatically the time from analog acquisition through ADC, buffering, classification, feedback and calibration.

#### Why the evaluation boundary matters

The manuscript uses a public superconducting-qubit dataset split into 90,000 training and 10,000 test examples. The same stated split informs architecture search, so a separate untouched final session or held-out device is needed to test whether the selected design generalizes. The manuscript also lists pre-accumulation shifts 2–7 in Table 2 while selecting shift 9 in Table 3; that search-space discrepancy needs clarification before the result can be reproduced.

An adequate comparison should report the full analog-to-decision path, LUTs, registers, routing, clock, power, energy per readout, acquisition and feedback latency, calibration cost, fidelity by state and drift condition, and performance on a new measurement session or device. Area and latency optimization should be reported with the fidelity constraint and the selected architecture, not as independent best values from different designs.

The manuscript-backed evidence supports selected FPGA readout designs with the reported LUT, latency and fidelity values. It does not establish complete-loop latency, energy, robustness to drift, an untouched-device result or general hardware superiority.

[Observed paper card](../observed-subthemes/quantum-hardware-and-control.md#paper-dac-2026-research2914)

## Algorithmic break-even: error correction must improve the encoded algorithm

Surface-code computation represents logical information in regions of a two-dimensional physical-qubit layout. Lattice surgery performs logical operations by changing which joint error-checking measurements connect those regions. The compiler must schedule those measurements and allocate space while accounting for imperfect operations.

[The break-even compilation pipeline](../observed-subthemes/quantum-hardware-and-control.md#paper-dac-2026-research1709) predicts when error correction improves algorithm fidelity over unencoded execution under the same modeled hardware constraints. It does not claim advantage over a classical algorithm. Sections 4.6–5, PDF pages 5–7, simulate Clifford proxy circuits with 500,000 shots under SI1000 noise, using Stim and PyMatching. The proxies omit magic-state preparation and conditional Y-basis injection measurements; synthesis and preparation contributions are combined separately through an approximate fidelity product.

For five-logical-qubit QAOA and QPE examples, page 7 predicts break-even at 2,517 physical qubits with code distance 11 and two-qubit error probability 0.001, or 1,737 physical qubits with distance 9 and probability 0.0005. Appendix A, page 9, gives different noise rates for measurement, reset, and other operations; the quoted probability is not one uniform rate for everything. These are conditional simulations, not device demonstrations or universal qubit-count thresholds. [Version-1 manuscript, Sections 4.6–5 and Appendix A](https://arxiv.org/pdf/2511.20947v1#page=5).

Clifford operations form a restricted class of quantum operations that can be efficiently simulated in the relevant setting. A proxy using them makes larger fault studies tractable, but replacing other operations limits what is directly simulated. A magic state is a specially prepared resource used to implement operations outside that restricted class; its preparation can fail and may require repeated attempts.

Code distance describes the minimum weight of an undetectable logical error. Increasing it can improve protection under suitable noise, but also requires more physical resources and longer protection procedures. The useful choice is consequently determined by the entire algorithm and its error budget, not just the reliability of an idle encoded qubit.

The two example algorithms also answer different computational questions. QAOA alternates operations governed by adjustable parameters to seek good solutions to an optimization problem. Quantum phase estimation estimates a phase associated with an operation and a suitable input state. A result for small instances of these algorithms is valuable for testing a compiler pipeline, but does not establish performance for arbitrary scientific workloads.

<span id="explanation-dac-2026-research1709"></span>

### Algorithmic break-even: error correction helps only when its full cost improves the same algorithmic quality target

#### What “break-even” means here

An unencoded circuit uses physical qubits directly and accumulates errors as gates, measurements, resets and time proceed. A fault-tolerant circuit encodes logical information across multiple physical qubits and repeatedly measures error syndromes. It can reduce logical errors, but it also consumes more qubits, more operations, more measurements, classical decoding and time.

An algorithmic break-even point is a comparison between these two executions under a specified hardware and noise model. It asks where the encoded execution reaches a better declared algorithmic fidelity or quality target than the unencoded execution. It does not ask whether the quantum algorithm is faster or better than a classical algorithm, and it is not a universal number of qubits independent of the circuit and noise.

#### What the compiler pipeline must account for

Surface-code compilation lays out logical qubits and schedules operations such as lattice surgery. Code distance affects the number of physical qubits and the protection against certain errors, but it also changes operation time, measurement count, decoding load and the space needed for temporary regions. The pipeline must carry these changes into both the error model and the resource calculation.

The error model must state separate rates for the relevant operations. A quoted two-qubit error probability is not automatically the rate for measurement, reset, preparation or every other operation. The decoder must be included because syndrome data becomes useful only after classical processing produces corrections or a valid interpretation. Feedback and decoding delays can change the runtime and the exposure to further errors.

#### What the manuscript-backed result establishes

The recovered manuscript simulates Clifford proxy circuits with 500,000 shots under SI1000 noise using Stim and PyMatching. For five-logical-qubit QAOA and QPE examples, it predicts break-even at 2,517 physical qubits with code distance 11 and two-qubit error probability 0.001, or 1,737 physical qubits with distance 9 and probability 0.0005.

These values are conditional outputs of the stated simulation. The proxies omit magic-state preparation and conditional Y-basis injection measurements, and synthesis and preparation contributions are combined separately through an approximate fidelity product. A Clifford proxy makes larger studies tractable, but it does not directly measure the complete non-Clifford algorithm or the repeated preparation attempts that may be required.

#### What would be needed for an end-to-end claim

The comparison should hold the logical algorithm, input, output-quality target, physical noise, decoder, measurement schedule and resource budget fixed. It should report logical error, algorithmic fidelity, physical-qubit count, operation count, syndrome and decoding time, preparation success, feedback latency, total runtime and energy for encoded and unencoded executions.

Validation should vary circuit size, code distance, operation mix, correlated noise, decoder behavior and state-preparation success. A device result would additionally require calibrated noise traces and measured control, readout, reset, decoding and feedback behavior. The two reported qubit counts should remain attached to their code distances and error probabilities; they are not general thresholds.

The manuscript-backed evidence supports a compiler pipeline and conditional break-even predictions for the stated proxy circuits and noise model. It does not establish a quantum-versus-classical advantage, a universal physical-qubit requirement, a complete non-Clifford result or a device demonstration.

[Observed paper card](../observed-subthemes/quantum-hardware-and-control.md#paper-dac-2026-research1709)

## Movable logical qubits: change where information resides without moving devices

A layout can restrict which operations run together. Two operations may require overlapping temporary regions even when their logical inputs are otherwise independent. Allowing the location of logical information to change can alter later routing conflicts.

[Exploiting Movable Logical Qubits](../observed-subthemes/quantum-hardware-and-control.md#paper-dac-2026-research2596) uses teleportation during measurement-based controlled-NOT operations. Its proof-of-concept focuses on color codes, not the surface-code assumption in the old card, and does not require physical device motion. The proposed movement uses the same number of lattice-surgery operations as the corresponding standard gate; this is a specific operation-count claim, not zero total hardware cost.

Section 5, PDF pages 5–6, compares random circuits and initial placements against static shortest-first routing. Table 1 uses 120 logical qubits, eight gates per logical layer, and ten circuits per entry. For the single-patch layout at logical depth 40, routed depth falls from 47.9 to 40.2 on average. Its 3.8% residual routing-overhead ratio is distinct from the reported 15.8% total-depth reduction. These results do not establish application-level logical error rates or physical runtime. [Version-1 manuscript, Sections 3–5 and Table 1](https://arxiv.org/pdf/2512.04169v1#page=5).

Quantum teleportation transfers a state using previously established quantum correlations, measurements, and classical outcome handling. It does not copy an unknown quantum state. In compilation, the important consequence is that the logical location can change even when the physical components remain fixed.

A controlled-NOT is a two-qubit operation that flips the target's computational-basis value conditional on the control. Its measurement-based implementation uses temporary resources. A compiler can consider which temporary location should retain the outgoing logical information, then evaluate how that choice affects subsequent gates.

A shorter schedule is useful, but schedule depth is not automatically wall-clock time. Operations may take different numbers of physical cycles, and decoding or feedback can delay dependent work. Comparing layouts also requires their physical-qubit counts: lower depth obtained by reserving much more space is a tradeoff, not an unconditional improvement.

<span id="explanation-dac-2026-research2596"></span>

### Exploiting Movable Logical Qubits: changing logical location can reduce routing only when teleportation and physical costs are included

#### What “moving” a logical qubit means

A logical qubit is information encoded across several physical qubits. A compiler can change which encoded region represents that information without moving a physical device. In this work, the movement uses teleportation during a measurement-based controlled-NOT operation. Teleportation consumes previously established quantum correlations, measurements and classical outcome handling; it does not copy an unknown state.

The location change matters because later lattice-surgery operations need temporary regions and connections. A fixed placement can force operations to wait or route around occupied regions. A movable placement can choose a different destination, but the compiler must track which region owns the logical state, which corrections are pending and which temporary resources can be reused.

#### What the reported routing result means

The recovered manuscript evaluates random circuits and initial placements against static shortest-first routing. Table 1 uses 120 logical qubits, eight gates per logical layer and ten circuits per entry. For the single-patch layout at logical depth 40, routed depth falls from 47.9 to 40.2 on average. The reported 3.8% residual routing-overhead ratio is different from the 15.8% total-depth reduction; neither number is a physical-runtime or error-rate result.

The movement uses the same number of lattice-surgery operations as the corresponding standard gate. That is an operation-count comparison, not a claim of zero cost. Measurement, classical feed-forward, decoder work, temporary entanglement and correction dependencies can still affect cycle time and resource use.

#### What a fault-tolerant comparison must include

Logical schedule depth counts an abstract sequence of operations. Wall-clock time also depends on the physical cycle time of each operation, measurement and reset latency, decoder throughput, feedback, parallel resource availability and waiting caused by dependencies. A layout that reduces depth by allocating more physical qubits may be useful, but its space-time volume and error exposure must be visible.

Compare movable and fixed placement under the same code family, circuit, initial placement, physical-qubit budget, error model, decoder, connectivity and compilation limit. Report logical error, physical-qubit count, space-time volume, lattice-surgery count, routed depth, physical runtime, decoder/feedback time and compile time. Include circuits with different interaction graphs and layouts that stress temporary-region conflicts.

The manuscript-backed evidence supports a color-code proof-of-concept for reducing routed logical depth under the stated random-circuit setup. It does not establish lower application-level logical error, lower physical runtime, lower space-time volume or general benefit across code families and hardware.

[Observed paper card](../observed-subthemes/quantum-hardware-and-control.md#paper-dac-2026-research2596)

## The connection across the four papers

Readout classification, drift tracking, logical routing, and error-aware compilation all affect the path from a physical measurement to a useful algorithm result. Their measurements must remain separate until an end-to-end model explicitly connects them. Nanoseconds, LUT counts, classification accuracy, routed layers, and algorithm fidelity cannot be ranked as one quantity.

The long-term hypothesis is that classical control and compilation should be evaluated together with the quantum device's error behavior. This sample supplies mechanisms supporting that question, not a historical adoption trend. A stronger study would use comparable devices and tasks across editions, retain time-varying measurement errors, include feedback and decoding delays, and account for unsuccessful preparation attempts.

The decisive test is whether a proposed local improvement produces a better complete computation under the same resource and quality constraints. Until that test is performed, the evidence supports the narrower readout, scheduling, and modeled break-even conclusions described above.

## Compare the results carefully

First identify the inputs and required output quality. Then identify the limited resource: time, memory, communication, energy, circuit area, or correctness coverage. Ask which part of the method reduces that cost and which new cost it adds. Compare numbers only when the experiments hold these conditions sufficiently similar.

A conference description may explain the proposal while omitting the full experiment. An author preprint link may have been coded from its abstract. The source classification does not by itself establish that every table was read. Missing locations remain visible below.

## Complete captured evidence

These are evidence records, not substitutes for the explanations above. Each record preserves its problem, proposed method, measurements, comparison conditions, and source limits. A populated record does not establish that its mechanism has been fully explained or independently verified.

<span id="paper-dac-2026-research1200"></span>

### NIAQ: Adaptive Non-Ideality-Aware Qubit Readout for Long-Term Accuracy

DAC 2026 · Record: `dac-2026-research1200`

[Read the step-by-step explanation](#explanation-dac-2026-research1200)

**Updated source-backed reading card**

Reviewed 2026-09-08. Deepens the existing NIAQ treatment into a paper-level reading; preserves the reported accuracy, degradation, CMOS power and delay figures while separating drift tracking, label availability, calibration cost and measurement boundaries.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Qubit readout converts a noisy analog measurement into a classical state label, and changing device or electronics behavior can make a fixed discriminator less accurate over time.

**Mechanism / artifact:**

Adaptive readout combining Kalman filtering for drift tracking with a multilayer neural discriminator; drift model, update signal, label source, retraining rule and hardware partition are unspecified in the official record.

**Workload — the work tested:**

Multi-qubit readout traces described as equivalent to one day's runtime; device, qubit count, drift construction, label process, train/test split and baseline conditions are unspecified.

**Hardware and manufacturing assumptions:**

Quantum-control/readout electronics with post-synthesis 28 nm CMOS results; the reported 148 mW and 5 ns boundary, clock, area, calibration path, ADC and fabricated-versus-simulated status are not fully specified.

**Baseline — the comparison method:**

Static qubit readout calibration

Uncorrected readout

Baseline design for the reported 7.7× power and 6.4× latency comparisons is not fully specified

**Reported measurements:**

Official description reports 88% accuracy versus 61% for a baseline on a multi-qubit dataset described as equivalent to one day's runtime, a 19× lower degradation rate, and post-synthesis 28 nm CMOS results of 148 mW and 5 ns delay; the degradation convention and full boundaries remain unspecified.

**Limits on the conclusion:**

Readout accuracy depends on the signal distribution, state labels, discriminator threshold or model, and the time-varying noise. A Kalman filter can track gradual drift only when its state model and uncertainty assumptions fit the device; abrupt changes or an unavailable label stream can make adaptation lag or update in the wrong direction.

A one-day-equivalent dataset is not the same as a fabricated device operating continuously for one day. The evaluation must define how time was constructed, separate ordinary shot noise from drift, prevent future labels from leaking into adaptation, report accuracy over time and include abrupt changes and recalibration interruption cost.

The official description does not fully define the degradation metric, baseline hardware, delay boundary, calibration cost, area, ADC/control path or fabricated-silicon status. The record supports adaptive-readout results under the stated description, not general long-term device reliability or a directly transferable hardware advantage.

**Source and location**

Evidence tier: Primary captured official DAC description plus existing chapter level niaq discussion; no full paper extraction, long horizon hardware trace reproduction or calibration cost validation. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH1200)

DAC 2026 official description; captured Problem, Mechanism / artifact, Workload, Hardware, Baseline, Measurements and Limits fields; record RESEARCH1200; official page reports 88%/61%, 19× degradation, 28 nm, 148 mW and 5 ns; no manuscript pages.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** static qubit readout calibration

uncorrected readout

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH1200

**Hardware or process assumptions:** Quantum-control/readout electronics and qubit measurement chain; noise and calibration assumptions are unspecified.

**Limits:** No readout fidelity, drift horizon, calibration overhead, or device results are reported.

Non-ideality models may not transfer across devices.

Official description only; hardware-trace validation is required.

**Method or artifact:** Adaptive readout method that models or compensates qubit non-idealities.

**Metrics:** Long-term readout accuracy is claimed qualitatively

**Problem:** Qubit readout non-idealities and drift can degrade accuracy over time.

**Workload or benchmark:** Qubit measurement traces; device type, drift duration, and baselines are unspecified.

</details>

<span id="paper-dac-2026-research1709"></span>

### Compilation Pipeline for Predicting Algorithmic Break-Even in an Early-Fault-Tolerant Surface Code Architecture

DAC 2026 · Record: `dac-2026-research1709`

[Read the step-by-step explanation](#explanation-dac-2026-research1709)

**Updated source-backed reading card**

Reviewed 2026-09-08. Deepens the existing manuscript-backed break-even treatment into a paper-level reading; preserves the conditional simulation, proxy-circuit, noise, shot, code-distance and qubit-count conditions while separating algorithmic fidelity from classical advantage and device evidence.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Error correction adds physical qubits, operations, measurements, decoding and time; an early fault-tolerant execution is useful only if the protected algorithm reaches better fidelity or another declared quality target than the unencoded execution under matched modeled conditions.

**Mechanism / artifact:**

Compiler pipeline predicting algorithmic break-even for a surface-code architecture; layout, lattice-surgery schedule, noise model, decoder, resource accounting and treatment of magic-state preparation are specified only in the recovered manuscript scope.

**Workload — the work tested:**

Clifford proxy circuits and five-logical-qubit QAOA and QPE examples; 500,000 shots under SI1000 noise using Stim and PyMatching, with proxy omissions and approximate fidelity-product treatment stated in the manuscript.

**Hardware and manufacturing assumptions:**

Modeled early fault-tolerant surface-code architecture; page-backed examples use code distances 11 and 9 and two-qubit error probabilities 0.001 and 0.0005, with distinct measurement/reset/other noise rates in Appendix A; no device demonstration.

**Baseline — the comparison method:**

Unencoded execution

Alternative surface-code compilation

Matched algorithm, quality target, noise, decoder and resource-accounting conditions are required

**Reported measurements:**

Manuscript-backed: predicted break-even for five-logical-qubit QAOA and QPE at 2,517 physical qubits with distance 11 and two-qubit error probability 0.001, or 1,737 physical qubits with distance 9 and probability 0.0005; 500,000-shot Clifford proxy simulations use SI1000 noise, Stim and PyMatching.

**Limits on the conclusion:**

Break-even compares encoded and unencoded executions under a modeled algorithm and quality measure; it does not compare a quantum algorithm with a classical algorithm. The encoded result is meaningful only if the logical-error, physical-resource, decoding, measurement, reset, preparation and runtime costs are included consistently.

The proxy circuits are Clifford-focused and omit magic-state preparation and conditional Y-basis injection measurements; synthesis and preparation contributions are combined through an approximate fidelity product. Those omissions can change the error and resource balance for non-Clifford workloads.

The 2,517- and 1,737-qubit values are conditional simulation outputs for stated code distances and error probabilities, not universal thresholds or device results. Transfer requires calibrated device noise, decoder behavior, feedback latency, state-preparation success and an end-to-end runtime and fidelity measurement.

**Source and location**

Evidence tier: Recovered manuscript backed selected simulation plus official DAC description; no calibrated device execution, full non clifford pipeline or independent reproduction. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://arxiv.org/pdf/2511.20947v1)

Manuscript v1, Sections 4.6–5 and Appendix A, PDF pages 5–9; official DAC record RESEARCH1709; 500,000 shots, SI1000 noise, Stim, PyMatching, QAOA/QPE and conditional qubit-count results.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** non-fault-tolerant execution

alternative surface-code compilation

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH1709

**Hardware or process assumptions:** Early fault-tolerant surface-code architecture; error rates and decoder assumptions are unspecified.

**Limits:** No logical error, resource, runtime, threshold, or prediction-accuracy results are reported.

Break-even depends strongly on hardware and decoder assumptions.

Official description only; calibrated end-to-end validation is required.

**Method or artifact:** Compiler pipeline for predicting algorithmic break-even under surface-code assumptions.

**Metrics:** Break-even prediction is claimed qualitatively

**Problem:** Quantum algorithms may not benefit from early fault-tolerant hardware unless error-correction overhead is amortized.

**Workload or benchmark:** Quantum algorithms and surface-code executions; code distance, gates, and hardware model are unspecified.

</details>

<span id="paper-dac-2026-research2596"></span>

### Exploiting Movable Logical Qubits for Lattice Surgery Compilation

DAC 2026 · Record: `dac-2026-research2596`

[Read the step-by-step explanation](#explanation-dac-2026-research2596)

**Updated source-backed reading card**

Reviewed 2026-09-08. Deepens the existing manuscript-backed movable-qubit treatment into a paper-level reading; preserves the color-code, teleportation, circuit-size, routed-depth and overhead conditions while separating logical schedule depth from physical runtime and error.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Lattice-surgery compilation can create routing conflicts when logical qubits occupy fixed locations, even though changing a logical location may reduce later conflicts.

**Mechanism / artifact:**

Compiler exploiting movable logical qubits through teleportation during measurement-based controlled-NOT operations; code, measurement schedule, routing policy, decoder and physical resource accounting are only partially specified.

**Workload — the work tested:**

Random fault-tolerant circuits; manuscript Table 1 uses 120 logical qubits, eight gates per logical layer, ten circuits per entry and the reported single-patch logical-depth-40 case.

**Hardware and manufacturing assumptions:**

Color-code proof of concept with lattice-surgery resources; the old surface-code reading is not applicable to this result, and physical error, cycle time, decoder, connectivity and space-time resource assumptions are unspecified.

**Baseline — the comparison method:**

Static shortest-first routing

Standard lattice-surgery compilation

Same circuit, initial placement, code and resource conditions are required

**Reported measurements:**

Manuscript-backed: in the single-patch logical-depth-40 case, routed depth falls from 47.9 to 40.2 on average; the 3.8% residual routing-overhead ratio is distinct from the 15.8% total-depth reduction. The movement claim uses the same number of lattice-surgery operations as the corresponding standard gate.

**Limits on the conclusion:**

Teleportation changes where logical information is represented using entanglement, measurements and classical outcomes; it does not move a physical qubit or copy an unknown state. The compiler must account for measurement, feed-forward, temporary resources and correction dependencies.

A shorter logical schedule does not automatically mean lower wall-clock time. Physical operations can have different cycle counts, decoder and feedback can delay dependent operations, and a layout with more physical space may buy lower depth. Space-time volume, physical qubits, logical error and compilation time belong in the comparison.

The manuscript result is a proof-of-concept for color codes on stated random-circuit settings. It reports no application-level logical error, physical runtime, decoder cost, space-time volume or broad hardware validation; the 3.8% and 15.8% quantities must remain distinct.

**Source and location**

Evidence tier: Recovered manuscript backed selected evaluation plus official DAC description; no calibrated fault tolerant device, decoder, physical runtime or application level error validation. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://arxiv.org/pdf/2512.04169v1)

Manuscript v1, Sections 3–5 and Table 1, PDF pages 5–6; official DAC record RESEARCH2596; 120 logical qubits, eight gates per layer, ten circuits per entry, routed-depth and overhead results.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** fixed logical-qubit placement

standard lattice-surgery compiler

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH2596

**Hardware or process assumptions:** Surface-code architecture supporting logical-qubit movement; error and connectivity assumptions are unspecified.

**Limits:** No logical error, space-time volume, depth, routing, or compilation-time results are reported.

Movability depends on code and hardware assumptions.

Official description only; fault-tolerant validation is required.

**Method or artifact:** Compiler exploiting movable logical qubits for lattice surgery.

**Metrics:** Compilation efficiency is claimed qualitatively

**Problem:** Lattice-surgery compilation is constrained by logical-qubit placement and movement overhead.

**Workload or benchmark:** Fault-tolerant quantum circuits; code distance, layouts, and decoder are unspecified.

</details>

<span id="paper-dac-2026-research2914"></span>

### LUNA: LUT-Based Neural Architecture for Fast and Low-Cost Qubit Readout

DAC 2026 · Record: `dac-2026-research2914`

[Read the step-by-step explanation](#explanation-dac-2026-research2914)

**Updated source-backed reading card**

Reviewed 2026-09-08. Deepens the existing manuscript-backed LUNA treatment into a paper-level reading; preserves the selected area/latency/fidelity configurations, FPGA placement boundary, dataset split and search-space discrepancy.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Qubit readout must classify noisy measurement traces with low latency and hardware cost while preserving state-classification fidelity.

**Mechanism / artifact:**

Non-overlapping signal-window accumulation followed by a quantized LogicNet classifier mapped into FPGA LUT logic; input precision, window rule, quantization, architecture-search protocol and full analog-loop boundary are specified only in the recovered manuscript scope.

**Workload — the work tested:**

Public superconducting-qubit dataset with 90,000 training and 10,000 test examples; qubit/device session, drift, split independence, sampling and final untouched evaluation are incompletely established.

**Hardware and manufacturing assumptions:**

Post-placement-and-routing design on XCZU49DR FPGA; LUT count and processing latency boundaries are reported, but analog acquisition, ADC, feedback, clock, energy and fabricated-device conditions are not fully specified.

**Baseline — the comparison method:**

Area-oriented baseline design

Latency-oriented baseline design

Software or conventional neural readout

The selected area and latency/fidelity points are different designs

**Reported measurements:**

Manuscript-backed: area-oriented design uses 6,095 LUTs versus 66,600 for the baseline; latency-oriented design reports 22.10 ns versus 32 ns at 95.969% versus 96.000% readout fidelity. These are not one configuration achieving all best values.

**Limits on the conclusion:**

Window accumulation reduces the number of classifier inputs but can discard time information. The resulting fidelity depends on window size, quantization, signal alignment, noise and the prepared-state distribution. Balanced readout fidelity is a classification metric, not whole-state or algorithm fidelity.

Post-placement-and-routing FPGA latency is not automatically the full readout-loop latency. Analog acquisition, ADC, buffering, classifier execution, feedback, calibration and data movement can add time and energy. Area reduction can also trade against precision, connectivity, routing or robustness to drift.

The manuscript uses the same stated 90,000/10,000 split during architecture search, and Table 3 selects pre-accumulation shift 9 while Table 2 lists 2–7; these conditions require clarification and an untouched final or new-device evaluation. The evidence supports selected FPGA results, not general readout hardware superiority.

**Source and location**

Evidence tier: Recovered manuscript backed selected evaluation plus official DAC description; independent untouched device, full loop and search space reconciliation remain open. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://arxiv.org/pdf/2512.07808v1)

Manuscript v1, Sections 3–5 and Tables 2–4, PDF pages 3–6; official DAC record RESEARCH2914; XCZU49DR post-placement-and-routing, 90,000/10,000 split, LUT, latency and fidelity values.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** software classifier

conventional neural readout

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH2914

**Hardware or process assumptions:** LUT or FPGA/ASIC readout hardware; sampling and precision assumptions are unspecified.

**Limits:** No readout fidelity, latency, area, energy, calibration, or device results are reported.

Noise and drift may alter classifier behavior.

Official description only; hardware-trace validation is required.

**Method or artifact:** LUT-based neural architecture for qubit readout.

**Metrics:** Readout speed and cost are claimed qualitatively

**Problem:** Qubit readout needs low-latency, low-cost classification of noisy measurement signals.

**Workload or benchmark:** Qubit readout traces; qubit type, noise, calibration, and hardware are unspecified.

</details>

## What remains to establish

Resolve unspecified workloads, comparison methods, resource budgets, and source locations before generalizing a reported gain. Multiple papers in this selected sample permit comparison of mechanisms, but do not by themselves establish recurrence across years or a long-term trend.

[All subthemes](../expanded-taxonomy-v1.md) · [Research directions](../directions/README.md)
