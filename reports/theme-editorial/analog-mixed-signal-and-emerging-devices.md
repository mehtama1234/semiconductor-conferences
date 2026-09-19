## Follow a number through its physical representation

A computation must represent its inputs, transform them, and make its output available. In a digital interface, a value may be encoded by a bit pattern. In an analog operation, a continuously varying quantity such as voltage or current represents a value within a defined range. Conversion connects these representations; it is part of the computation's cost and error, not an external detail that can always be ignored.

Suppose voltages from zero to one volt represent numbers from zero to one. A measured voltage of 0.6 volt represents 0.6 under that mapping. An unintended shift of 0.01 volt changes the represented number by 0.01. Another mapping can change that numerical sensitivity. Precision is therefore a property of the mapping, device behavior, and measurement together—not simply the number of nominal output bits.

These examples are independent teaching constructions. The linked chapters retain their manuscript, description, simulation, and measured-device boundaries. The umbrella theme does not make analog, photonic, quantum, and emerging-memory systems interchangeable.

## Conversion establishes both a range and a resolution

A digital-to-analog converter produces a physical signal from a code. An analog-to-digital converter assigns a code to a measured signal. A simple ideal quantizer covering a one-volt range with 256 equal intervals has interval width about 3.906 millivolts. More output codes can distinguish smaller intervals in the ideal model, but they do not eliminate noise, distortion, or uncertainty in the input.

Inputs outside the supported range can saturate: different physical values then produce the same limiting code. No later arithmetic can reconstruct which original value was present from that code alone without additional information or assumptions. Within range, random error and systematic distortion remain different problems.

Increasing range can prevent saturation while making intervals wider at fixed code count. Reducing range can improve nominal resolution while excluding valid inputs. Report the input distribution and the required error, not just converter width.

## Physical arithmetic needs a stated operating model

Under a simple linear model, applying voltage to a conductance produces current equal to their product. Combining currents can implement a sum of such products. The mathematical opportunity is to let device relationships perform part of a numerical operation rather than explicitly executing every multiplication in digital logic.

The implementation must still address signed values, finite operating ranges, wiring effects, and how the output is sensed. A conductance cannot simply represent any signed real number without an encoding method. Large arrays can also behave differently from an isolated device because their interconnections affect the applied and observed signals.

The [analog compute-in-memory chapter](../observed-subthemes/analog-compute-in-memory.md) identifies relevant proposals. Their usefulness must be judged after input preparation, output conversion, corrections, and data movement. An efficient internal operation does not establish an equally efficient complete application.

As an illustrative energy budget, let input conversion cost four units, physical arithmetic one, output conversion three, and control two. Total cost is ten. Halving arithmetic energy saves only half a unit, or 5% overall. This is not a measurement; it shows why the accounting boundary can change the interpretation of a large device-level gain.

## Calibration cannot recover information that was never observed

Calibration uses observations to estimate and compensate for departures from intended behavior. Suppose a device follows `measured = 1.1 × input + 0.02` over a validated range. A correction can subtract 0.02 and divide by 1.1 if those parameters remain applicable. If they change with temperature or time, the correction can become inaccurate.

The simple formula also does not remove unobserved random noise or undo arbitrary clipping. Two different inputs producing the same saturated output are indistinguishable through that output alone. A learned correction may exploit additional signal structure, but its success then depends on that structure being present.

[The ADC-calibration discussion](../observed-subthemes/analog-calibration-and-modeling.md#blind-adc-calibration-what-the-output-metrics-mean) distinguishes converter test-chip measurements from an integrated correction engine operating at the required live sample rate. “Train once” does not by itself establish transfer to every device, input, or unforeseen error. Model storage, inference latency, power, and supported operating conditions still matter.

Different accuracy measures answer different questions. Noise-and-distortion ratios describe signal quality under a measurement convention. Application accuracy counts or scores task outcomes. A relative preservation ratio is not an absolute accuracy. For example, retaining 99% of a baseline accuracy of 80% gives 79.2%, not 99% task accuracy.

## Measured duration and extrapolated duration must remain separate

A memory device can change its electrical state over time even when the intended information remains unchanged. A compensation method may use a fitted drift model to predict future behavior. That prediction is not the same evidence as observing the device for the predicted duration.

The [VeRA+ discussion](../observed-subthemes/analog-calibration-and-modeling.md#vera-correcting-memory-drift-without-retraining-on-the-chip) preserves a one-week measured-device interval separately from ten-year simulated drift. It also distinguishes offline preparation from absence of on-chip retraining. A compact correction representation can reduce storage overhead without establishing a proportional reduction in energy or elapsed time.

To test long-term transfer, vary the device population and operating conditions, retain residual errors, and check where the extrapolation stops matching observations. A model that fits one interval well still needs evidence for the later interval and intended deployment population.

## A circuit representation needs electrical context

Connectivity describes which terminals are connected. The same connectivity can behave differently when component parameters, supply, loading, or physical layout change. A learning model predicting an electrical property therefore needs the information relevant to that property.

[Hyperanalog's explanation](../observed-subthemes/analog-circuit-learning.md#a-learned-representation-is-not-yet-a-circuit-result) preserves the captured source's missing targets, datasets, and measurements. The term hypergraph describes a representation allowing multi-object relationships; it does not establish which electrical constraints are encoded. A learned representation becomes useful engineering evidence through a defined downstream task and validated decision, not through the model name alone.

This connects to [AI-assisted EDA](ai-assisted-eda.md): prediction, generation, and checking remain separate roles. A favorable predicted circuit must still meet its requirements under the intended conditions.

## Keep different physical computing approaches distinct

Optical systems encode information in properties of light and require appropriate preparation and measurement. Quantum systems manipulate quantum states and produce measurement outcomes under their own model. Classical controllers and data movement can remain substantial parts of either system. Their shared need for input/output accounting does not imply a shared correctness metric or equivalent numerical precision.

The expanded [neuromorphic, quantum, and non-von-Neumann chapter](../observed-subthemes/neuromorphic-quantum-and-non-von-neumann.md) separates physical numerical computation, optical representation, classical quantum control, compilation, and simulation. A control processor's response time is not a quantum algorithm's end-to-end speedup. A simulation result is not measured operation of the corresponding physical device.

The taxonomy still contains broad and overlapping labels. These connections are conceptual navigation, not silent reclassification or evidence that every technology solves the same problem.

## Compare the complete path under an output requirement

| Claimed benefit | Required companion evidence |
| --- | --- |
| More nominal representable levels | Usable range, noise, distortion, and effective discrimination |
| Low-energy device arithmetic | Conversion, sensing, control, correction, and transfer costs |
| Reusable calibration | Unfamiliar-device behavior, update needs, and live execution cost |
| Long-term accuracy preservation | Measured duration, extrapolation assumptions, and absolute task quality |
| A better learned circuit model | Defined targets, appropriate data splits, and validated downstream decisions |

The [architecture theme](architecture-and-accelerators.md) explains the numerical boundary; the [systems theme](systems-applications-and-workloads.md) explains the completed-task boundary. Both apply here. Holding only the internal operation count fixed can miss changed outputs, additional preparation, or unusable response time.

## Long-term hypotheses and disconfirming tests

One hypothesis is that improvements in physical arithmetic shift more of the complete cost toward conversion and control. Measure component and total costs under matched output requirements. It weakens where those surrounding costs are already small or fall alongside the device cost.

A second hypothesis is that reusable compensation can reduce per-device engineering effort when residual errors remain predictable. Test held-out devices, changed inputs, temperature ranges, and elapsed time while charging for preparation and updates. It weakens where correction fails outside familiar conditions or consumes the expected benefit.

A third hypothesis is that representation-aware co-design is necessary to make device advantages usable. Compare the same computation with explicit encoding, range, error, and output checks. It weakens as a demonstrated capability where gains disappear after conversion or at the application's required quality.

These are bounded interpretations, not established ISCA–DAC–ICCAD time trends or claims of technological replacement. Comparable tasks, evidence depth, hardware conditions, and editions remain required. This expanded parent discussion does not complete the still-uneven individual-paper writing, full-source recovery, device validation, or independent scientific and comprehension review.
