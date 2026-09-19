# Analog, mixed-signal, and emerging devices

This article explains the subject and then connects it to 38 papers in the selected research sample.

A subtheme groups related technical problems. A mechanism describes the particular change proposed by a paper. The discussion below explains the subject; the linked paper records state the available evidence.

[Definitions used in the paper records](../reading-guide-v1.md)

## What changes when physics performs part of the computation

Digital circuits represent values with discrete bit patterns. Analog computation uses continuously varying quantities such as voltage or current. Optical computation uses properties of light. Quantum computation uses quantum states and operations. These approaches differ substantially, but each requires a precise account of how the physical state represents the input and how the output is read.

## Why device behavior is only part of the system

Inputs may require conversion from digital values, and outputs may require measurement and conversion back. Noise, temperature, variation between devices, and measurement precision can change the result. Calibration adjusts operation using measured device behavior and also consumes time or hardware. Any claimed saving must include the surrounding conversion, control, and correction work.

## What separates the subthemes

Analog circuit automation designs continuous-signal circuits. Compute-in-memory methods perform operations in or near storage structures. Photonic work uses optical components. Quantum hardware and control work concerns preparing, manipulating, and measuring quantum states. Emerging-memory work studies storage technologies with different physical properties. The umbrella grouping does not imply these methods have interchangeable accuracy or performance measures.

## A comparison that answers the question

Identify whether the evidence comes from equations, simulation, a fabricated device, or a complete system. Report precision, error, calibration, conversion cost, temperature, and device variation under the intended workload. A device operation with low energy establishes one component cost; an application claim requires the full path from inputs to usable outputs.

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

## Subthemes and how to study them

Each link opens the subtheme discussion and its captured paper records. Explanatory depth varies: some papers have expanded individual explanations; others still have only brief discussion or evidence cards. Source locations and unresolved conditions remain visible.

### [Neuromorphic quantum and non von neumann](../observed-subthemes/neuromorphic-quantum-and-non-von-neumann.md)

8 selected records in this theme. Start with [Photomt : Accelerating Zero-Knowledge Proofs with a Photonic-Electronic Merkle Tree Engine](../observed-subthemes/neuromorphic-quantum-and-non-von-neumann.md).

### [Analog compute in memory](../observed-subthemes/analog-compute-in-memory.md)

4 selected records in this theme. Start with [RM-CIMA: An Analog Computing-in-Memory Accelerator for a Robust UAV Trajectory Tracking Framework](../observed-subthemes/analog-compute-in-memory.md).

### [Photonic and optical compute](../observed-subthemes/photonic-and-optical-compute.md)

4 selected records in this theme. Start with [ROSA: Robust and Energy-Efficient Microring-Based Optical Neural Networks via Optical Shift–and–Add and Layer-Wise Hybrid Mapping](../observed-subthemes/photonic-and-optical-compute.md).

### [Quantum hardware and control](../observed-subthemes/quantum-hardware-and-control.md)

4 selected records in this theme. Start with [NIAQ: Adaptive Non-Ideality-Aware Qubit Readout for Long-Term Accuracy](../observed-subthemes/quantum-hardware-and-control.md).

### [Analog layout and circuit automation](../observed-subthemes/analog-layout-and-circuit-automation.md)

3 selected records in this theme. Start with [AMS Layout Automation Using Circuit-Level Analog Standard Cells and Self-Biasing Techniques in Digital PnR Tools](../observed-subthemes/analog-layout-and-circuit-automation.md).

### [Analog and mixed signal design](../observed-subthemes/analog-and-mixed-signal-design.md)

2 selected records in this theme. Start with [Floquet-Based Subspace Projection Method for Time-Domain PPV Computation](../observed-subthemes/analog-and-mixed-signal-design.md).

### [Analog calibration and modeling](../observed-subthemes/analog-calibration-and-modeling.md)

2 selected records in this theme. Start with [Train Once, Calibrate Always: Machine-Learning-Assisted Blind Calibration for Analog-to-Digital Converters](../observed-subthemes/analog-calibration-and-modeling.md).

### [Device modeling and simulation](../observed-subthemes/device-modeling-and-simulation.md)

2 selected records in this theme. Start with [Weak-Form Physics-Informed Neural Network for Self-Supervised Learning in Semiconductor Device Simulation](../observed-subthemes/device-modeling-and-simulation.md).

### [Emerging device design](../observed-subthemes/emerging-device-design.md)

2 selected records in this theme. Start with [Duplication-Aware Retiming and Cell Interface Redesign for Superconductor Circuit Minimization](../observed-subthemes/emerging-device-design.md).

### [Emerging memory and devices](../observed-subthemes/emerging-memory-and-devices.md)

2 selected records in this theme. Start with [M²CAM: A Multi-Level Memristor-Based Self-Adaptive CAM Architecture for Genome Processing Acceleration](../observed-subthemes/emerging-memory-and-devices.md).

### [Analog and mixed signal synthesis](../observed-subthemes/analog-and-mixed-signal-synthesis.md)

1 selected records in this theme. Start with [Noisexplore: A Device-Aware Hierarchical Noise Modeling and DTCO Framework for Analog In-Pixel Computing Architectures](../observed-subthemes/analog-and-mixed-signal-synthesis.md).

### [Analog circuit learning](../observed-subthemes/analog-circuit-learning.md)

1 selected records in this theme. Start with [Hyperanalog: Domain-Aware Hypergraph Transformer for Analog Circuit Representation Learning](../observed-subthemes/analog-circuit-learning.md).

### [Analog circuit optimization](../observed-subthemes/analog-circuit-optimization.md)

1 selected records in this theme. Start with [COmPOSER: Circuit Optimization of mm-Wave/rf Circuits with Performance-Oriented Synthesis for Efficient Realizations](../observed-subthemes/analog-circuit-optimization.md).

### [Emerging and nonvon neumann compute](../observed-subthemes/emerging-and-nonvon-neumann-compute.md)

1 selected records in this theme. Start with [iADS: In-Situ Adaptive Diffusion Sampling Architecture Based on Voltage-Tunable P-Bits](../observed-subthemes/emerging-and-nonvon-neumann-compute.md).

### [RF and mixed signal design](../observed-subthemes/rf-and-mixed-signal-design.md)

1 selected records in this theme. Start with [ASG-MOENN: Adaptive Sparsely-Gated Mixture of Experts Neural Network for Digital Predistortion in Quadrature Switched-Capacitor Power Amplifiers](../observed-subthemes/rf-and-mixed-signal-design.md).

## Representative source-backed records

The following reading set spans the available conferences and uses dated corrections where registered. These corrections improve the current reading view but do not change historical adjudication or establish independent acceptance. Each paper link opens its exact evidence card.

## Paper cards: what changes and where it stops

- [Jsplace: A Shape-Controllable and Length-Matching Placement for Rapid Single-Flux-Quantum Circuits](../observed-subthemes/emerging-device-design.md#paper-dac-2026-research875) — DAC 2026.
- [Diffsp: Differentiable Sequence Pair-Based Analog Placement](../observed-subthemes/analog-layout-and-circuit-automation.md#paper-dac-2026-research776) — DAC 2026.
- [SP2RINT: Spatially-Decoupled Physics-Constrained Progressive Inverse Optimization for Diffractive Optical Neural Network Training](../observed-subthemes/photonic-and-optical-compute.md#paper-dac-2026-research760) — DAC 2026.
- [Alphaplacer: Analog Placement Enhanced by Monte Carlo Tree Search](../observed-subthemes/analog-layout-and-circuit-automation.md#paper-dac-2026-research713) — DAC 2026.
- [NeuroPDE: A Neuromorphic PDE Solver Based on Spintronic and Ferroelectric Devices](../observed-subthemes/neuromorphic-quantum-and-non-von-neumann.md#paper-iccad-2025-130) — ICCAD 2025.
- [Adder-DCIM: A Parallel Bit-Flexible Digital CIM Joint Model Compression Framework for AdderNet Inference](../observed-subthemes/emerging-memory-and-devices.md#paper-iccad-2025-1) — ICCAD 2025.
- [Simulation Framework and Optimization of Superconducting Transmon-Tunable Coupler-Transmon System for Qudit Gates](../observed-subthemes/neuromorphic-quantum-and-non-von-neumann.md#paper-iccad-2025-1094) — ICCAD 2025.
- [ASG-MOENN: Adaptive Sparsely-Gated Mixture of Experts Neural Network for Digital Predistortion in Quadrature Switched-Capacitor Power Amplifiers](../observed-subthemes/rf-and-mixed-signal-design.md#paper-dac-2026-research656) — DAC 2026.
- [Duplication-Aware Retiming and Cell Interface Redesign for Superconductor Circuit Minimization](../observed-subthemes/emerging-device-design.md#paper-dac-2026-research520) — DAC 2026.
- [Hyperanalog: Domain-Aware Hypergraph Transformer for Analog Circuit Representation Learning](../observed-subthemes/analog-circuit-learning.md#paper-dac-2026-research445) — DAC 2026.
- [AMS Layout Automation Using Circuit-Level Analog Standard Cells and Self-Biasing Techniques in Digital PnR Tools](../observed-subthemes/analog-layout-and-circuit-automation.md#paper-dac-2026-research407) — DAC 2026.
- [Light-Bound Transformers: Hardware-Anchored Robustness for Silicon-Photonic Computer Vision Systems](../observed-subthemes/photonic-and-optical-compute.md#paper-dac-2026-research3237) — DAC 2026.

## What the evidence supports

These records identify proposed methods and the conditions recorded for them. A reported improvement should be interpreted with its comparison method, input size, hardware, and result-quality requirement. Missing fields are evidence gaps; a populated field can also state that a detail is unspecified.

## Limits and next evidence

The selected sample is uneven across conferences and source types. It cannot establish how fast a subject is growing. Repeated observations across comparable years, with the same inclusion rules and source depth, are needed for a time trend.

Every linked evidence article preserves the Problem: and Mechanism / artifact: fields, baseline, unshortened limitations, source URL, and recorded location. Primary text and independent review remain necessary where the record says those checks are open.

[Research directions](../directions/README.md) · [All observed subthemes](../expanded-taxonomy-v1.md)
