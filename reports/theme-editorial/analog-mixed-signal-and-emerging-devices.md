## Follow a number through its physical representation

When physics does arithmetic, the way a number is stored as a voltage sets its precision.

A computation must represent its inputs, transform them, and make its output available.

- In a **digital** interface, a value may be a bit pattern.
- In an **analog** operation, a continuously varying quantity, such as voltage or current, stands for a value within a defined range.

**Conversion** links the two. It is part of the computation's cost and error, not a detail to ignore.

> **Worked example.** Voltages from 0 to 1 volt stand for numbers from 0 to 1.
>
> - A measured 0.6 volt means 0.6 under this mapping.
> - An unintended shift of 0.01 volt changes the number by 0.01.
> - A different mapping would change that sensitivity.

So precision comes from the mapping, the device behavior and the measurement together, not just the number of nominal output bits.

**Be careful:** these examples are independent teaching constructions. The linked chapters keep their manuscript, description, simulation and measured-device boundaries. Grouping analog, photonic, quantum and emerging-memory systems under one theme does not make them interchangeable.

## Conversion establishes both a range and a resolution

A converter fixes which values can be told apart, and which cannot be recovered at all.

- A **digital-to-analog converter** turns a code into a physical signal.
- An **analog-to-digital converter** assigns a code to a measured signal.

> **Worked example (ideal converter).** A 1-volt range split into 256 equal intervals:
>
> 1,000 millivolts ÷ 256 ≈ **3.906 millivolts** per interval.

More codes can tell smaller intervals apart in the ideal model. They do not remove noise, distortion, or uncertainty in the input.

An input outside the supported range can **saturate**: different physical values all give the same limiting code. From that code alone, no later arithmetic can tell which original value it was, without extra information or assumptions. Inside the range, random error and systematic distortion are separate problems.

The range is a trade-off at a fixed number of codes:

- A wider range prevents saturation, but makes intervals wider.
- A narrower range improves nominal resolution, but excludes valid inputs.

So report the input distribution and the required error, not just the converter width.

## Physical arithmetic needs a stated operating model

Devices can multiply and add for free in principle, but only under a stated model and with an encoding for every value.

Under a simple linear model, applying a voltage to a **conductance** (how easily a device passes current) gives a current equal to their product. Adding currents together gives a sum of products. The opportunity is to let device physics do part of a numerical operation, instead of running every multiplication in digital logic.

The implementation must still handle:

- signed values;
- finite operating ranges;
- wiring effects;
- how the output is sensed.

A conductance cannot represent any signed real number without an encoding method. Large arrays can also behave differently from one isolated device, because their wiring changes the applied and observed signals.

The [analog compute-in-memory chapter](../observed-subthemes/analog-compute-in-memory.md) lists relevant proposals. Judge them after counting input preparation, output conversion, corrections and data movement. An efficient internal operation does not mean an equally efficient complete application.

> **Worked example (illustrative energy budget, not a measurement).**
>
> | Step | Energy units |
> | --- | --- |
> | Input conversion | 4 |
> | Physical arithmetic | 1 |
> | Output conversion | 3 |
> | Control | 2 |
> | **Total** | **10** |
>
> Halving arithmetic energy saves 0.5 unit: **5%** of the total.

Where you draw the accounting boundary can change how a large device-level gain should be read.

## Calibration cannot recover information that was never observed

Correction can undo a known, stable distortion, but not noise or clipping it never saw.

**Calibration** uses observations to estimate and compensate for departures from intended behavior.

> **Worked example.** Over a validated range, a device follows `measured = 1.1 × input + 0.02`.
>
> - Correction: subtract 0.02, then divide by 1.1.
> - This works only while those two parameters still apply.
> - If they drift with temperature or time, the correction becomes inaccurate.

This simple formula does not remove unobserved random noise, or undo arbitrary clipping. Two different inputs giving the same saturated output cannot be told apart from that output. A learned correction may use extra structure in the signal, but then it works only when that structure is present.

[The ADC-calibration discussion](../observed-subthemes/analog-calibration-and-modeling.md#blind-adc-calibration-what-the-output-metrics-mean) separates converter test-chip measurements from an integrated correction engine running at the required live sample rate. "Train once" does not, by itself, show transfer to every device, input or unforeseen error. Model storage, inference latency, power and supported operating conditions still matter.

Different accuracy measures answer different questions:

- **Noise-and-distortion ratios** describe signal quality under a measurement convention.
- **Application accuracy** counts or scores task outcomes.
- A **relative preservation ratio** is not an absolute accuracy.

> **Worked example.** Keeping 99% of a baseline accuracy of 80%: 0.99 × 80% = **79.2%**, not 99% task accuracy.

## Measured duration and extrapolated duration must remain separate

A week of measurements and a ten-year prediction are different kinds of evidence.

A memory device can change its electrical state over time, even when the stored information should not change. A compensation method may predict future behavior from a fitted drift model. That prediction is not the same evidence as watching the device for that long.

The [VeRA+ discussion](../observed-subthemes/analog-calibration-and-modeling.md#vera-correcting-memory-drift-without-retraining-on-the-chip) keeps a one-week measured-device interval separately from ten-year simulated drift. It also separates offline preparation from the absence of on-chip retraining. A compact correction format can cut storage overhead, without a matching cut in energy or elapsed time.

To test long-term transfer:

1. vary the device population and operating conditions;
2. keep the leftover (residual) errors;
3. check where the extrapolation stops matching observations.

A model that fits one interval well still needs evidence for the later interval, and for the intended deployment population.

## A circuit representation needs electrical context

Knowing which terminals connect is not enough to predict how a circuit behaves electrically.

**Connectivity** says which terminals are joined. The same connectivity can behave differently when component values, supply, loading or physical layout change. So a learning model that predicts an electrical property needs the information that drives that property.

[Hyperanalog's explanation](../observed-subthemes/analog-circuit-learning.md#a-learned-representation-is-not-yet-a-circuit-result) keeps the captured source's missing targets, datasets and measurements. "Hypergraph" names a representation where one relationship can join several objects. It does not say which electrical constraints are encoded. A learned representation becomes useful engineering evidence through a defined downstream task and a validated decision, not through the model's name.

This links to [AI-assisted EDA](ai-assisted-eda.md): prediction, generation and checking stay separate roles. A circuit predicted to be good must still meet its requirements under the intended conditions.

## Keep different physical computing approaches distinct

Optical, quantum and analog systems share the need to count input and output costs, but not a correctness measure.

- **Optical** systems carry information in properties of light, and need suitable preparation and measurement.
- **Quantum** systems manipulate quantum states, and produce measurement outcomes under their own model.

Classical controllers and data movement can be large parts of either. Sharing the need for input/output accounting does not mean sharing a correctness metric or equal numerical precision.

The expanded [neuromorphic, quantum, and non-von-Neumann chapter](../observed-subthemes/neuromorphic-quantum-and-non-von-neumann.md) separates physical numerical computation, optical representation, classical quantum control, compilation and simulation.

- A control processor's response time is not a quantum algorithm's end-to-end speedup.
- A simulation result is not measured operation of the real device.

**Be careful:** the taxonomy still has broad, overlapping labels. These links are conceptual navigation, not silent reclassification, and not evidence that every technology solves the same problem.

## Compare the complete path under an output requirement

Each claimed device benefit needs companion evidence about the whole path.

| Claimed benefit | Required companion evidence |
| --- | --- |
| More nominal representable levels | Usable range, noise, distortion, and effective discrimination |
| Low-energy device arithmetic | Conversion, sensing, control, correction, and transfer costs |
| Reusable calibration | Unfamiliar-device behavior, update needs, and live execution cost |
| Long-term accuracy preservation | Measured duration, extrapolation assumptions, and absolute task quality |
| A better learned circuit model | Defined targets, appropriate data splits, and validated downstream decisions |

The [architecture theme](architecture-and-accelerators.md) explains the numerical boundary. The [systems theme](systems-applications-and-workloads.md) explains the completed-task boundary. Both apply here. Holding only the internal operation count fixed can miss changed outputs, extra preparation, or unusable response time.

## Long-term hypotheses and disconfirming tests

Three readings are worth testing; each names what would weaken it.

| Hypothesis | Test | What would weaken it |
| --- | --- | --- |
| Better physical arithmetic shifts more of the total cost to conversion and control | Measure component and total costs under matched output requirements | Those surrounding costs are already small, or fall along with the device cost |
| Reusable compensation can cut per-device engineering effort when leftover errors stay predictable | Test held-out devices, changed inputs, temperature ranges and elapsed time, charging for preparation and updates | Correction fails outside familiar conditions, or eats the expected benefit |
| Device advantages become usable only with representation-aware co-design | Compare the same computation with explicit encoding, range, error and output checks | Gains disappear after conversion, or at the application's required quality |

These are bounded interpretations, not established ISCA–DAC–ICCAD time trends or claims that one technology will replace another. Comparable tasks, evidence depth, hardware conditions and editions are still needed.

**Be careful:** this parent discussion does not complete the still-uneven individual-paper writing, full-source recovery, device validation, or independent scientific and comprehension review.
