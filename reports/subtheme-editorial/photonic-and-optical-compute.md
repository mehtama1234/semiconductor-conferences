## Start with the operation, not the light source

A matrix–vector multiplication takes a list of input numbers and produces several weighted sums. Each output multiplies the inputs by a different set of weights and adds the products. Neural networks repeat this operation, together with other transformations. An optical implementation must encode those numbers in light, produce the intended weighted combination, and deliver a result that the next operation can use.

Light has amplitude and phase: amplitude describes the size of the electromagnetic field; phase describes its position within an oscillation. Optical power is related to the squared field amplitude. These quantities are not interchangeable. An implementation needs a specified encoding and detector response before its physical behavior can be interpreted as arithmetic.

The four papers address different parts of this process. Two change how a calculation uses imperfect optical hardware. Two change how designers find a physical structure that performs a desired transformation. Shorter design time is not shorter inference time. A measured component is not automatically a measured complete application.

Three manuscripts were recovered for this discussion. LightningFNO remains supported by its official description. The source-specific findings below supersede conflicting omissions in the original captured cards; full reconciliation of those cards remains open.

<span id="explanation-dac-2026-research160"></span>

## ROSA: reduce conversions while controlling mapping error

A microring resonator is a small closed optical path coupled to another path. Its transmission depends on wavelength and device settings. Using that transmission to represent a weight requires setting it accurately and keeping it sufficiently stable during use. Temperature changes and imperfect control voltages can change the represented value.

[ROSA](../observed-subthemes/photonic-and-optical-compute.md#paper-dac-2026-research160) combines time-encoded inputs, analog weights, delay lines and splitters, and layer-specific input- or weight-stationary mapping. Section 3.1, PDF pages 2–3, places scaling and timing alignment in optics but describes final addition through photodetection and amplification; “optical shift-and-add” should not imply an entirely optical application.

Section 4, pages 5–6, uses extended Timeloop/CiMLoop architecture modeling and PyTorch behavioral simulation, with 45 nm component assumptions, 5 GHz operation, and eight-bit inputs, weights, and outputs. Figure 8 reports a 29% energy–delay-product reduction from adding the module to its baseline. This is not a measured fabricated-chip speedup.

Table 4 on page 6 needs correction: the extracted ResNet18 values, 1.531 to 1.493 J·s, imply about 2.48% reduction, not the annotated 24.7%. MobileNet V3 accuracy rises from 74.8% to 76.5%, a 1.7-percentage-point change, not the annotated 2.6%. The reported aggregate mapping improvements should not be accepted without reconciling these entries. [Version-1 manuscript, Sections 3–4 and Table 4](https://arxiv.org/pdf/2605.00032v1#page=2).

Keeping weights stationary means reusing a programmed weight while changing inputs. Keeping inputs stationary means reusing an input while changing the relevant weights. Reuse can reduce transfers, but a setting that reduces one transfer can increase another. The right choice depends on layer dimensions, programming costs, and how errors affect that layer's output.

Energy–delay product multiplies energy by execution time. Its reduction does not identify how much each factor changed. A complete comparison should show both separately, then explain whether the application has an energy limit, a deadline, or both. Calibration also belongs in that accounting: a delay line that needs adjustment is not a cost-free replacement for storage.

ROSA's robustness claim has two separate boundaries. The noise-aware voltage-to-weight model must describe how DAC quantization, thermal drift, wavelength detuning, insertion loss, crosstalk and fabrication variation perturb the microring transmission, and how calibration observes and corrects those changes. Then the resulting optical error must be propagated through every layer and checked against task accuracy. A mapping that is robust in a behavioral model is not yet robust on a fabricated, thermally varying array.

The recovered evaluation is a modeled 45-nm, 5-GHz study with 8-bit inputs, weights and outputs, extended Timeloop/CiMLoop modeling and PyTorch behavior. The source reports 64% and 26% aggregated EDP reductions against DEAP-CNNs and a general compact array, 29% from OSA, an 8.3% CIFAR-10 accuracy improvement over weight-stationary mapping and 54.7% lower average EDP than DEAP-CNNs. Those numbers require the energy and delay components, calibration, array dimensions, wavelength count and complete optical/electronic boundary.

The recovered Table 4 values also require arithmetic reconciliation: ResNet18 values of 1.531 and 1.493 J·s imply approximately 2.48% reduction, while MobileNet V3 accuracy from 74.8% to 76.5% is a 1.7-percentage-point increase. The annotated percentages should not be promoted to validated results until the source table and denominators are resolved. The evidence supports noise-aware microring mapping and optical shift-and-add co-design, not demonstrated process-robust, calibration-complete or whole-system optical-NN superiority.

<span id="explanation-dac-2026-research2358"></span>

## LightningFNO: learn both design generation and response prediction

Forward modeling starts with a physical structure and predicts its response. Inverse design starts with a desired response and searches for a structure. For optical devices, a detailed electromagnetic solver computes fields subject to material and boundary conditions. Repeating that computation for many candidate geometries can dominate design time.

[LightningFNO](../observed-subthemes/photonic-and-optical-compute.md#paper-dac-2026-research2358) uses two Fourier neural operators: one proposes a structure, and another predicts its optical response. The official description reports 1,245,550× faster design than adjoint-based optimization for 4×4 units, fabricated 3×3 prototypes with root-mean-square error 0.043, and 97.69% MNIST accuracy using metasurface-deployed kernels. The old card's statement that no numerical or measured-device results are reported is therefore outdated.

The description does not establish training-data generation cost, whether model training is included in the speed ratio, error normalization, device sample count, or the division between optical and electronic execution. The 4×4 design comparison and 3×3 fabrication experiment are separate evidence. A full manuscript and page-backed conditions remain missing. [Official DAC description](https://63dac.conference-program.com/presentation/?id=RESEARCH2358&sess=sess169).

A Fourier representation describes a spatial pattern through frequency components. A neural operator learns relationships between input and output fields or arrays. That can reduce repeated numerical solving within the range learned from its data. It does not remove the need to verify unfamiliar shapes, materials, wavelengths, or manufacturing variations.

Two learned models can also share a blind spot. A generated structure may look accurate to the learned response predictor but fail in an independent solver or device measurement. The strongest validation therefore checks proposed designs with evidence outside the model pair. Root-mean-square error summarizes squared deviations; without the reference quantity and its scale, 0.043 is not automatically 4.3% error.

The first gate is independent optical fidelity. Compare fields, phase/amplitude, transmission, loss and relevant MVM error against a full-wave Maxwell solver for held-out geometries, wavelengths, materials, angles, polarization and fabrication perturbations. Then compare the fabricated prototype's measured response. RMSE 0.043 needs its target, normalization, spatial/frequency domain and whether it is simulated or measured; it is not automatically a percentage or a wafer result.

Inverse generation also needs a manufacturability gate. Check minimum feature and spacing, layer constraints, connectivity, fabrication bias, alignment, optical loss, thermal behavior and detector dynamic range. A candidate can score well against the learned forward FNO while exploiting a surrogate error or violating the process. Count rejected candidates, repair and independent re-simulation, not only the time to produce a topology.

Keep the 1,245,550× 4×4 design comparison separate from the fabricated 3×3 RMSE and the 97.69% MNIST deployment. Include training-data generation, FNO training/inference, adjoint/Maxwell evaluations, fabrication, calibration, optical setup, electronic conversion and neural-network execution in the relevant time and energy boundaries. The evidence supports a dual-FNO photonic inverse-design direction with a fabricated prototype result, not demonstrated scalable process transfer, full-system optical efficiency or universal design-speed superiority.

<span id="explanation-dac-2026-research3237"></span>

## Light-Bound Transformers: train for the hardware's uncertainty

Attention assigns relative importance to pieces of an input. Its scores are numerical quantities, so noise can reverse their ordering when two scores are close. Training for ideal arithmetic can therefore produce a model that behaves differently when the same operations execute with physical errors.

[Light-Bound Transformers](../observed-subthemes/photonic-and-optical-compute.md#paper-dac-2026-research3237) characterizes bank-level microring-resonator noise, then uses Chance-Constrained Training to impose noise-normalized attention margins and a noise-aware LayerNorm using an estimated noise variance (Section 4, PDF page 4). The probability argument assumes a Gaussian noise model and selected score comparisons; a soft training penalty does not itself prove every desired inequality is satisfied.

Section 5, page 5, describes noise injection and ten noisy inference runs. It distinguishes the indicated measured fabrication-noise range, 0.05–0.1, from larger stress settings. Table 2's strongest listed Tiny-ImageNet noise case improves from 65.89% to 79.50% mean accuracy, still below the 86.14% clean result.

These are hardware-in-the-loop and noise-injection results with a calibration and optical loss boundary, not automatically execution of the complete Transformer on a population of fabricated photonic devices.

Page 6's efficiency claims need reconciliation. Figure 8 presents 70.7×/116.7× efficiency ratios, while Table 4 reports much smaller energy ratios; Tiny consumes 61.4 µJ versus FPGA's 54.86 µJ. The prose also applies an additional tenfold scaling to electronic latency. Without aligned accounting, these are not established whole-system energy gains or direct measured latency comparisons. Device-informed noise should not be conflated with execution of the entire model on fabricated hardware. [Version-1 manuscript, Sections 4–5, Figure 8 and Table 4](https://arxiv.org/pdf/2604.04330v1#page=4).

There are two separate questions here: whether a model resists the specified noise, and whether the platform executes it efficiently. Better noisy accuracy answers the first. It does not answer the second. Conversely, an energy estimate is useful only at an acceptable output quality.

The captured evidence supports noise-aware training for photonic vision, not demonstrated full-system optical efficiency or process-robust Transformer deployment.

Frames per second per watt reduces dimensionally to frames per joule. It measures energy efficiency, not speed alone. If each frame consumes a stated energy, the two quantities should agree after accounting for batching, utilization, and measurement scope. A disagreement requires those conditions to be explained, not a choice of the larger headline.

<span id="explanation-dac-2026-research760"></span>

## SP2RINT: repeatedly bring learned responses back to physical designs

A metasurface is a patterned layer whose small structures modify light. Neighboring structures can interact, so selecting each structure from an isolated lookup table can miss the response of the complete arrangement. Training an unrestricted numerical transformation also does not guarantee that any allowed structure can implement it.

[SP2RINT](../observed-subthemes/photonic-and-optical-compute.md#paper-dac-2026-research760) treats training as a PDE-constrained process, first using banded transfer matrices and then alternating a numerical response with adjoint inverse design and local patches to reduce field-solving work. The recovered version-2 preprint predates the DAC edition; identical camera-ready content is not established. Sections IV-B–D, PDF pages 9–10, acknowledge projection and response-approximation errors and use 17-element patches. Table II reports simulated physical-response testing: 88.44% Fashion-MNIST and 81.61% SVHN accuracy, plus a separate Darcy-flow error metric.

The simulation-in-the-loop baseline is not completed: page 10 estimates about 178 hours per Fashion-MNIST epoch at batch size 32 and omits its results. The 1825× headline is therefore not a ratio between completed equivalent training runs. Table II's 63.88% aggregate also combines classification and regression improvements; it is not an absolute accuracy increase. [Version-2 manuscript, Sections IV-B–D and Table II](https://arxiv.org/pdf/2505.18377v2#page=9).

The authors provide an [implementation repository](https://github.com/ScopeX-ASU/SP2RINT). Its availability is established, but its experiments have not been independently reproduced here.

The captured evidence supports progressive physics-constrained diffractive training, not demonstrated reproducible training superiority, fabricated optical deployment or process-robust physical-response accuracy.

The general design tradeoff is how often to check physical feasibility. Checking only after training can leave a large mismatch that cannot be corrected without losing useful behavior. Checking after every update can consume excessive computation or restrict exploration too early. Intermediate checks allow adaptation, but their frequency and approximation error need testing together.

Feasibility in an electromagnetic model is also narrower than manufacturing yield. A design can satisfy the modeled equations and still fail under dimensional variation, surface roughness, alignment error, or temperature changes. Fabrication-ready geometry and a measured population of reliable devices are different achievements.

## What these papers suggest, and what would establish a trend

The useful connection is the need to preserve the intended numerical operation across design, hardware, and application evaluation. Faster physical design helps only if the resulting response remains accurate. Noise-aware training helps only within a sufficiently representative error model. Fewer conversions help only if their replacements preserve quality and reduce total cost.

This is a synthesis of mechanisms in the selected sample, not evidence that optical computing is replacing electronic computing or that adoption is increasing. A long-term study should follow comparable tasks across editions and record design cost, fabricated scale, output quality, calibration frequency, and complete execution energy separately.

Three tests would materially strengthen the direction: independently solve and fabricate learned candidate structures; test trained models across multiple devices and changing operating conditions; and compare complete input-to-output execution with electronic alternatives at matched quality. Failure at any of these stages would narrow the proposed benefit even if a component-level result remains valid.
