## What an accelerator must make cheaper

A program specifies operations and relationships between their inputs and outputs. Hardware must execute the operations, move the values they use, and keep enough intermediate state to finish the computation. An accelerator is a hardware organization intended to perform a particular class of work efficiently. Its useful contribution must reduce one or more of those costs under the application's requirements.

There are several possible sources of improvement. A dedicated circuit can replace a sequence of general instructions. Several units can perform independent work concurrently. A buffer can retain values that would otherwise be fetched repeatedly. A direct connection between successive operations can reduce intermediate storage. These changes have different costs and should be evaluated separately.

## Dataflow describes when values permit work to proceed

An operation can start once its required inputs are available and an execution resource is ready. Its output may enable later operations. A dataflow design organizes execution around these producer–consumer relationships. Some designs assign a fixed sequence of work to hardware stages; others choose ready operations as execution proceeds.

The assignment affects both concurrency and storage. If one stage produces outputs faster than the next stage consumes them, those outputs accumulate in a buffer. When the buffer fills, the producer must pause or the system must provide another storage path. The overall rate is therefore limited by the rates and dependencies of the connected stages, including transfers into and out of the accelerator.

## Why specialization is conditional

A dedicated operation can be efficient when the application uses it frequently and supplies suitable inputs. The same hardware may sit idle when the workload changes or when another operation becomes dominant. Supporting more cases may require extra control, larger buffers, additional arithmetic formats, or a fallback processor.

The relevant comparison is the fraction of the complete job improved. If a method accelerates one stage, the other stages still consume time. Conversion, data loading, and output collection can determine whether the local improvement produces a useful application gain. The paper must specify the beginning and end of its measurement.

<span id="explanation-dac-2026-research1822"></span>

## LPN acceleration: cryptographic parameters define the work before the FPGA can define the speed

### What LPN computation is

Learning Parity with Noise is a problem built from binary linear relations that have errors. A typical instance contains a secret, input vectors, and observed parity values that may be flipped by noise. An algorithm tests or learns candidates against those relations. The amount of work depends on the dimension, number of samples, noise rate, success requirement and security parameter.

Those parameters are not merely benchmark labels. Changing them changes the computational workload and the security meaning of the result. An accelerator that is fast for one parameter set may not support the set required for a target security level. Throughput therefore needs to be reported with the exact LPN variant, parameters, sample count and success/error condition.

### What the heterogeneous FPGA architecture is trying to coordinate

The record describes configurable engines, stage-level scheduling and bandwidth-oriented performance modeling. Configurable engines allow different parts of the LPN computation to use hardware suited to their operation. Stage scheduling decides when those engines receive work and when their outputs become available to later stages.

The stages form a producer–consumer pipeline. If an upstream engine produces samples or intermediate values faster than the next engine can consume them, buffers grow and eventually force the producer to wait. If the next stage is fast but data arrives slowly through the memory interface, the compute engine is idle. The dataflow result is therefore controlled by the slowest dependency and the transfer path, not by the peak arithmetic rate of one engine.

### What the 52.80× claim does not establish

The official description reports a 52.80× performance gain over a state-of-the-art LPN architecture. It does not identify the LPN parameters, security assumptions, FPGA family, clock, resource use, energy, throughput definition or baseline implementation. The ratio may reflect a data-transfer bottleneck in the baseline, different parameter conditions, or baseline maturity; it cannot be interpreted as a cryptographic improvement.

A valid comparison must hold the LPN function, parameter set, success probability, output correctness, FPGA device, clock and input/output measurement boundary constant. Report latency per instance, instances per second, memory traffic, buffer occupancy, LUT/DSP/BRAM use, clock frequency, power and energy. Show stage-level utilization and compare the complete accelerator against a defined baseline, not only one optimized engine.

### What the record establishes and where it stops

The official description establishes a heterogeneous FPGA/dataflow direction for LPN acceleration that targets execution flow and data-transfer bottlenecks. It reports a source-level performance ratio but does not establish the cryptographic parameters, security level, implementation parity or complete hardware conditions needed to interpret it.

The [LPN acceleration](../observed-subthemes/specialized-accelerators-and-dataflow.md#paper-dac-2026-research1822) record is evidence of a named accelerator proposal, not a cryptographic security result or independently validated FPGA speedup. The detailed explanation above separates LPN problem conditions, pipeline throughput, data movement, FPGA resource use and security claims.

<span id="explanation-dac-2026-research727"></span>

## Correlation-aware GKP decoding: the decoder must infer a correction from a noisy continuous measurement

### What a GKP decoder is deciding

A Gottesman–Kitaev–Preskill code represents a logical qubit in an oscillator using a regular grid of allowed states. Noise shifts the oscillator away from that grid. A measurement produces a continuous-valued syndrome related to the shift. The decoder estimates which grid displacement occurred and chooses a correction so the state returns to the logical code space.

The decoder is an inference circuit, not only a lookup table. It receives measured values, applies a noise model and computes a correction or confidence. A wrong correction can turn a correctable physical error into a logical error. Decoder quality therefore requires a specified noise distribution, correlation structure, logical-error metric and decision rule.

### Why correlation changes the computation

If measurement errors are independent, the decoder can factor the probability into separate contributions. Correlated errors do not permit that simplification: an error in one variable or time step changes the probability of another. The decoder must use joint information, which can improve inference under the correct model but requires more state, arithmetic or memory access.

Correlation-aware decoding can fail in two different ways. The circuit may be too slow for the arrival rate of optical-clock measurements, or the assumed correlation model may not match the physical noise. A low-latency circuit with a mismatched model can produce more logical errors; a highly accurate inference rule that misses the timing window is also not a usable decoder.

### What the 7-nm synthesis result means

The official description reports 12.96 ns decoding latency from a 7-nm FinFET synthesis and describes accuracy/latency/area tradeoffs qualitatively. Synthesis timing estimates the delay of the modeled RTL or netlist under a library, clock and constraint setup. It does not establish post-layout timing, power, yield, optical-clock integration, memory-interface cost or the logical error rate of the complete quantum system.

The comparison must state whether 12.96 ns is one decoder decision, a pipeline initiation interval, a worst-case or typical path, and whether input measurement, buffering, correction output and reset are included. Compare against the straightforward correlation-aware decoder at the same noise model, code parameters, accuracy target, process library, clock constraint and area/power boundary.

### What a complete validation must report

Give the GKP code parameters, measurement precision, correlated-noise distribution, correlation length or covariance, decoder output rule and logical-error probability. Report latency, initiation interval, throughput, area, power, memory, process/voltage/temperature conditions and post-layout or measured status. Test model mismatch and noise conditions not used to tune the decoder.

Keep decoder circuit latency separate from the optical source, detector, measurement electronics, feedback actuator and physical oscillator timing. A synthesized decoder can meet a nominal tens-of-nanoseconds target while the complete correction loop has a different deadline.

### What the record establishes and where it stops

The official description establishes a correlation-aware GKP decoder accelerator intended for fault-tolerant continuous-variable photonic quantum computers and reports a 12.96 ns 7-nm synthesis result. It does not report decoding accuracy, logical error rate, area, power, noise conditions, post-layout status or integrated photonic-system timing.

The [correlation-aware GKP decoder](../observed-subthemes/specialized-accelerators-and-dataflow.md#paper-dac-2026-research727) record is evidence of a decoder hardware proposal, not a demonstrated fault-tolerant quantum system. The detailed explanation above separates continuous-syndrome inference, correlated-noise modeling, synthesized delay, logical correctness and complete feedback-loop timing.

<span id="explanation-dac-2026-research2753"></span>

## MoE token-stationary dataflow: removing padded expert work is only the first part of the energy argument

### Why expert inputs have different sizes

Mixture-of-Experts inference contains multiple expert networks. A router examines each token and sends it to one or more experts. Because the router decisions depend on the input, an expert may receive many tokens for one batch and only a few for another. The matrix multiplication performed by that expert therefore has a variable token dimension.

A conventional GPU implementation often groups an expert's tokens into a fixed tensor shape. If the expert receives fewer tokens than that shape allows, the unused positions are filled with padding. The fixed matrix operation then performs arithmetic for padded positions even though those positions have no corresponding token output. The wasted work is proportional to the gap between the allocated shape and the number of valid tokens; it is not a property of the expert's mathematical function.

### What token-stationary execution changes

The paper describes a token-stationary dataflow. The central question is which value remains associated with an execution position while the other operand moves. In this setting, a valid routed token is kept as the unit of work while the selected expert's parameters are streamed or reused around it. The array can therefore represent the number of real tokens rather than treating every expert as if it had the same fixed batch size.

That change can remove multiply-accumulate operations whose inputs are only padding. It does not remove the rest of MoE inference. The system must still compute router decisions, move each token to its expert, fetch or retain expert parameters, accumulate the result, and restore the original token order for the next layer. A design that reduces arithmetic but increases routing or memory traffic may not reduce total energy.

### What a reconfigurable systolic array must control

A systolic array passes values through a regular grid of processing elements. To handle variable expert token counts, the array must make its valid work boundary depend on the current routed group. Reconfiguration might alter active rows or columns, valid-lane masks, tile dimensions, operand movement or the schedule used to load expert parameters.

The implementation must specify how a token group is counted, when a configuration is selected, how a short group is drained, and how the next expert starts. If expert weights are reused across many tokens, the array may amortize weight loading. If expert groups are small or interleaved, loading and switching can dominate. Partial sums also need a defined path: they must remain associated with the correct token and expert until the output is complete.

The array cannot assume that all experts have the same work. It needs a policy for groups that are too small to fill the hardware, groups that exceed one tile, and batches in which many experts become active simultaneously. The policy determines whether the claimed removal of padding is preserved or replaced by idle lanes, extra buffering, serialization or repeated configuration.

### Why padding reduction is not yet an energy result

Arithmetic energy is only one part of MoE inference energy. Routing, token permutation, interconnect transfers, expert-weight reads, activation storage, control, clocking and output reordering also consume energy. A token-stationary design can lower arithmetic count while increasing data movement if expert tokens are scattered or expert parameters do not remain local.

A fair result must report the routed token-count distribution, top-k routing rule, padding fraction in the baseline, valid operations in the proposed array, routing traffic, weight traffic, buffer traffic and the full measurement boundary. It must hold model outputs and quality conditions constant. GPU comparison also needs the GPU type, software framework, kernel implementation, precision, batch and sequence conditions, because a framework may fuse routing or use a different padding policy.

### What the record establishes and where it stops

The official description establishes a token-stationary dataflow and reconfigurable systolic-array proposal aimed at avoiding padding-induced redundant computation for MoE inference. It qualitatively claims a significant improvement over state-of-the-art GPU-based MoE inference frameworks. It does not report token distributions, padding fraction, routing cost, memory traffic, throughput, latency, energy, area, accuracy or the GPU and software conditions.

The [MoE token-stationary dataflow](../observed-subthemes/specialized-accelerators-and-dataflow.md#paper-dac-2026-research2753) record is evidence of a dataflow proposal, not proof of an end-to-end energy advantage. The explanation separates valid-computation reduction, routing and memory cost, reconfiguration overhead, systolic-array utilization and the conditions needed for a reproducible GPU comparison.

<span id="explanation-dac-2026-research946"></span>

## UNICON: a unified nonlinear unit must preserve activation accuracy while sharing arithmetic hardware

### What a nonlinear activation computes

A neural-network layer first accumulates weighted inputs and then applies an activation function to each resulting value. The activation changes the value before it enters later layers. Some activations clamp negative values, some approximate a probability-like curve, and others use exponentials, divisions, gates or piecewise rules.

These functions have different ranges, slopes and numerical sensitivity. Their implementation may require comparisons, table reads, multiplication, division, exponentiation or iterative approximation. The cost is affected by input distribution and precision. A hardware unit that is efficient for one function may not use the same operations or accuracy range for another.

### What logarithmic-domain computation changes

Logarithmic-domain computation represents a nonzero magnitude using a logarithm. Operations related to multiplication can then be expressed using addition, and powers of two can be represented by shifts. A shift-add datapath can implement parts of these operations with simpler arithmetic than a general multiplier or divider.

The transformation does not make the activation free. The input must be converted into the logarithmic representation, and the result must be converted back. Zero, sign, negative inputs, saturation, range limits, rounding and exceptional values need explicit handling. Finite precision in the logarithm and inverse transformation contributes to activation error.

### What shift-add decomposition must preserve

A shift-add approximation expresses a coefficient or operation as a sequence of shifts and additions or subtractions. It can reduce multiplier complexity when the coefficient representation is suitable. The number of terms, shift positions, intermediate width and rounding rule determine the error and latency.

The relevant error is not only the difference between an exact and approximate activation at one input. Later layers receive the approximate value, so errors can accumulate or alter classification, detection or generation decisions. The evaluation must report the input range, function approximation error, precision, worst-case and distributional error, and network-level quality on the same model and data.

### What unified reconfigurable hardware has to control

Supporting several activations with one architecture requires a shared representation and a function-specific sequence of operations. The hardware may select coefficients, branches, shift-add paths, ranges or correction steps based on the requested activation. A modular design can avoid duplicating all arithmetic units, but it needs routing, control, configuration storage and timing rules.

Dynamic dataflow reconfiguration changes which modules receive values and in what order. A change between layers must preserve valid data, pipeline state and output ordering. If the architecture reconfigures while another operation runs, the independent paths and shared memories must be isolated or scheduled safely. Configuration time and control energy belong in the end-to-end activation cost.

### How to interpret the reported efficiency ratios

The captured description reports average 1.55× speedup, 2.56× energy efficiency and 2.74× area efficiency over state-of-the-art nonlinear-activation architectures. The activation set, approximation method, precision, conversion cost, frequency, area boundary, power and reconfiguration overhead are not exposed.

An average ratio needs the functions and weighting method. Speedup must state whether it is one activation evaluation or a complete layer. Energy efficiency must state whether input conversion, output conversion, memory and control are included. Area efficiency must define whether conversion tables, configuration storage, routing and all supported modes are counted. A design that shares hardware may look smaller per function while requiring additional control to support the full set.

### What the record establishes and where it stops

The official description establishes a unified reconfigurable nonlinear-activation architecture based on logarithmic-domain computation and shift-add decomposition. It reports average speed, energy-efficiency and area-efficiency improvements over state-of-the-art NAF architectures. It does not expose the activation set, approximation/error conditions, network-level accuracy, conversion overhead, reconfiguration cost, clock or complete PPA accounting.

The [UNICON](../observed-subthemes/specialized-accelerators-and-dataflow.md#paper-dac-2026-research946) record is evidence of a reported activation-hardware proposal, not proof of equal-quality improvement for every nonlinear function or DNN. The explanation separates mathematical approximation, representation conversion, shared hardware, dynamic dataflow and the boundaries needed for a fair efficiency comparison.

<span id="explanation-dac-2026-research885"></span>

## Chimera: a unified FHE accelerator must share transform hardware without pretending CKKS and TFHE are the same computation

### What the two schemes require

Fully homomorphic encryption allows a system to evaluate a function on encrypted data. The evaluator performs arithmetic on ciphertexts and should obtain an encryption of the result without learning the plaintext. The cost and correctness conditions depend on the encryption scheme, its parameters and the sequence of operations.

CKKS is intended for approximate arithmetic. It represents values with scale and allows controlled numerical error. TFHE is designed for fast Boolean or integer-like operations and uses bootstrapping to refresh ciphertexts during computation. These schemes have different ciphertext behavior, transform domains, precision requirements, key material and memory traffic. A unified accelerator cannot compare them only by counting multiply operations.

### What a shared FFT/NTT flow can and cannot share

An NTT computes a polynomial transform using modular arithmetic. An FFT computes a related transform over a numerical domain used by TFHE operations. Both can contain butterfly-like stages and regular data movement, so a hardware design may share arithmetic structure, routing and storage.

The shared structure still needs mode-specific controls. Modulus handling, twiddle factors, scaling, rounding, precision, coefficient representation and error behavior must be correct for the selected scheme. A mode switch must select the right constants, memory layout and output interpretation. Sharing hardware can reduce duplication, but it can also add multiplexers, control state, mode storage and timing constraints.

### Why bootstrapping-key unrolling changes utilization and storage

Bootstrapping refreshes an FHE ciphertext so accumulated noise does not make later computation invalid. The operation can use a large bootstrapping key and many transform steps. The description proposes aggressive key unrolling to expose more independent key work to the accelerator.

More exposed parallel work can keep functional units busy, but it also increases the amount of key data that must be stored or streamed. If the key is not on chip, memory bandwidth can become the bottleneck. If it is on chip, area and leakage increase. The evaluation must state key size, placement, reuse, compression, bandwidth and whether key movement is included in performance and energy.

### What Shrinking KeySwitch is supposed to address

KeySwitch changes a ciphertext from one key representation to another. It can become expensive because it involves large key material and polynomial operations. Chimera describes hardware-oriented FFT Shrinking KeySwitch support to reduce this bottleneck.

The term “shrinking” needs an exact definition. It may reduce an intermediate representation, transform work, stored coefficients or the active dimension, but every reduction must preserve the required decryption correctness and error bound. The design must report the input and output representation, transform schedule, memory traffic, approximation or rounding conditions and the security parameters under which it is valid.

### Why constrained auto-tuning is part of correctness

TFHE configuration choices affect error, memory use and bandwidth as well as latency. An auto-tuner can search tile sizes, parallelism, buffering, transform scheduling or key placement under stated constraints. The selected configuration is acceptable only if ciphertext correctness, security parameters, memory capacity and bandwidth limits remain satisfied.

The tuner must distinguish a measured result from a model prediction and report how it handles configurations that violate error or resource limits. A configuration that is fast because it permits too much numerical error is not a valid FHE result. The search space, constraints and workload parameters determine which “optimal” configuration is being claimed.

### How to interpret the reported comparison

The captured description reports an average 14.84× performance improvement across TFHE workloads, comparable performance on CKKS workloads and a 9.6% area increase over state-of-the-art unified FHE designs. The exact FHE parameters, security level, workload circuits, transform implementation, clock, key traffic, power and area boundary are not exposed.

The TFHE average must identify whether it is latency, throughput or bootstrapping rate and how workloads are weighted. “Comparable” CKKS performance needs a numerical range and the same CKKS shapes and parameters. The 9.6% area increase needs a baseline, process, frequency target and inclusion rule for memories, key storage, control and interfaces.

### What the record establishes and where it stops

The official description establishes a unified FHE accelerator direction that gives TFHE first-class transform, key and memory support while retaining CKKS operation. It identifies dual-mode FFT/NTT computation, bootstrapping-key unrolling, Shrinking KeySwitch and constrained auto-tuning, and reports the performance and area claims above. It does not expose cryptographic parameters, security conditions, exact hardware organization, key traffic, power or reproducibility artifacts.

The [Chimera](../observed-subthemes/specialized-accelerators-and-dataflow.md#paper-dac-2026-research885) record is evidence of a reported unified FHE accelerator, not proof of scheme-independent performance or preserved cryptographic correctness under every configuration. The explanation separates scheme semantics, shared transform structure, key movement, KeySwitch correctness and measured accelerator claims.

<span id="explanation-dac-2026-research693"></span>

## MALIWAN: GEMM mapping on a heterogeneous ACAP is a measured search over competing resources and objectives

### What GEMM mapping decides

General Matrix Multiplication computes an output matrix from two input matrices and an accumulation. The computation can be divided into tiles, but the division is not free. A mapping chooses which tile dimensions are processed in parallel, where operands and partial sums are stored, how data is reused, and when results move between memory and compute units.

Versal ACAPs contain different execution resources. The AI Engines, programmable logic and processing system have different instruction models, local storage, bandwidth and control costs. Assigning more work to one component can improve arithmetic throughput while increasing transfers or leaving another component idle. The best mapping therefore depends on matrix dimensions, precision, layout, memory placement, clock and the objective being optimized.

### Why throughput and energy conflict

Throughput measures how quickly completed GEMM work is produced. Energy efficiency measures work per unit energy. Increasing parallel units or clock frequency can raise throughput but also increase active power, memory traffic and synchronization. A lower-power mapping may use fewer units and take longer while consuming less energy per result.

A mapping search must make these objectives explicit. A configuration is Pareto-optimal when no other allowed configuration is at least as good in every selected objective and strictly better in one. The frontier changes if the search adds constraints for power, thermal behavior, area, memory capacity, latency or required throughput. “Optimal” without the objective and allowed configuration set is incomplete.

### What MALIWAN’s search loop contributes

MALIWAN is described as combining three activities. Analytical-model sampling estimates useful regions of the design space without measuring every point. On-board experiments measure actual Versal behavior, including effects that a simplified model may miss. A data-driven surrogate learns from those measurements and predicts promising unmeasured mappings so the search can spend later experiments on configurations likely to improve the frontier.

The surrogate is not the result itself. Its predictions can be wrong outside the measured region or when a mapping activates a different bottleneck. A sound loop must retain held-out measurements, quantify prediction error, add measurements where uncertainty is high, and measure the final selected configurations directly. The search can only claim coverage of the tested design space; it cannot establish the best mapping among configurations it never represents.

### What the approximately 6,000 experiments mean

The description reports about 6,000 on-board experiments and an evaluation on the Versal VCK190. This indicates hardware-based sampling rather than a purely simulated result. It does not by itself reveal whether an experiment is one matrix shape, one mapping, one repeated measurement or a configuration sweep. Repeated measurements, warm-up behavior and board conditions affect how the results should be interpreted.

For each point, the evaluation should identify matrix dimensions, precision, layout, mapping, clock, input/output transfers, throughput, power, energy and resource use. It should separate accelerator energy from board or complete application energy and state whether memory initialization, host transfers and setup are included. The search should also report surrogate error and whether the comparison uses the same shape and quality conditions for every baseline.

### How to read the reported improvements

The captured description reports geometric-mean throughput improvement of 1.23×, up to 2.5×, and geometric-mean energy-efficiency improvement of 1.25×, up to 2.7× over state-of-the-art works. It also begins a comparison with NVIDIA GPUs, claiming up to 2.5× energy efficiency, but the captured source ends before that comparison is complete.

Geometric means summarize ratios across a set of workloads and can hide the distribution of individual results. The maximum and geometric-mean numbers need the workload set, shapes, precision and baseline implementations. The incomplete GPU sentence cannot support a complete GPU conclusion; its missing remainder, platform, power boundary and workload conditions remain unresolved.

### What the record establishes and where it stops

The official description establishes a measured, surrogate-guided design-space exploration framework for GEMM mappings on heterogeneous Versal hardware. It reports approximately 6,000 on-board experiments, VCK190 evaluation and throughput/energy-efficiency improvements over named comparison categories. The source capture is truncated during the GPU comparison and does not expose the search variables, GEMM conditions, clocks, power boundary, surrogate validation or complete GPU result.

The [MALIWAN](../observed-subthemes/specialized-accelerators-and-dataflow.md#paper-dac-2026-research693) record is evidence of a reported device-specific mapping-search framework, not proof of a globally optimal mapping or a general GPU energy advantage. The explanation separates GEMM placement, Pareto objectives, model-guided search, board measurement and the limits created by the incomplete source capture.

<span id="explanation-dac-2026-research660"></span>

## TRINE: one FPGA bitstream must support different multimodal operators without hiding switching and pruning costs

### Why multimodal inference stresses one accelerator

A multimodal model can combine image, graph, language and attention-related components. A vision transformer, convolutional network, graph neural network and transformer language block do not present the same tensor dimensions, sparsity pattern or reduction. They also do not reuse operands in the same direction.

An accelerator built for one operator can leave lanes idle on another. A static FPGA implementation can support several operators by reserving separate resources, but that can increase area and reduce utilization. Reconfiguring the FPGA between layers can change the hardware shape, but configuration transfer and state movement add latency and interrupt execution.

### What the single-bitstream design is trying to provide

TRINE is described as a single-bitstream FPGA accelerator and compiler. The bitstream contains the available hardware; runtime execution selects modes and routes work without loading a new full bitstream for each layer. This reduces the cost of switching the entire fabric, but it does not eliminate mode-selection, pipeline-drain, buffer, synchronization or control work.

The design supports DDMM, SDDMM and SpMM. These operations differ in which operands are dense or sparse and in how valid entries are found and reduced. A common processing-element array therefore needs mode-specific operand paths, valid-entry handling, partial-sum movement and output ordering. The compiler must map each layer's tensors and dependencies to those modes while preserving numerical behavior.

### What the processing-element modes change

Weight-stationary execution keeps weights near the arithmetic units while activations move. Output-stationary execution keeps partial outputs local while the operands arrive. A 1×CS SIMD mode and a routable adder tree provide other ways to process or reduce values. These modes trade storage, movement, lane utilization and reduction cost differently.

The array must define when a mode changes and what happens to work already in flight. A mode switch may require draining a pipeline, changing valid masks, resetting or preserving partial sums, and changing the route through the adder tree. If the switch occurs between layers, the layer boundary includes this control and buffer work. If it overlaps execution, the design needs independent resources and a dependency-safe schedule.

### What top-k token pruning removes and what it adds

In-stream top-k pruning selects the highest-scoring tokens while the data is moving through the accelerator. Later layers then process fewer tokens. This can reduce arithmetic and memory traffic when the selected tokens preserve the information required by the task.

The selector itself performs scoring, comparison, storage and ordering. It may need to retain candidates before the final top-k set is known. The design must state which score is used, where the selection occurs, whether token order is preserved, how tokens re-enter later attention or graph operations, and whether a token can be restored. A less-than-2.5% accuracy-loss claim requires a defined dataset, model, pruning rate and quality metric; it cannot be converted into a general accuracy guarantee.

### How dependency-aware offload can overlap kernels

A model graph contains dependencies: a kernel can start only after its input is ready. Independent kernels can run on different reconfigurable processing units when they do not require the same data or a conflicting resource. Dependency-aware offload schedules these kernels to overlap.

The achievable overlap is limited by graph parallelism, buffer capacity, memory bandwidth, synchronization and load balance. Two kernels may be mathematically independent but still compete for the same memory channel or interconnect. The schedule must identify the RPU boundary, queueing time, transfer time and completion rule. Reported latency should distinguish arithmetic time from graph scheduling and tensor movement.

### How to interpret the reported comparison

The captured description reports up to 22.57× lower latency than an RTX 4090 and 6.86× lower latency than a Jetson Orin Nano on Alveo U50 and ZCU104, at 20–21 W, with less than 2.5% accuracy loss and state-of-the-art efficiency.

The exact workload, model, precision, token distribution, pruning threshold, clocks, preprocessing, GPU libraries, batch, latency boundary and power boundary are not exposed. “At 20–21 W” must distinguish board power, FPGA accelerator power and complete system power. A latency ratio also needs the same output quality, warm-up policy, host transfer treatment and end-to-end boundary on every platform.

### What the record establishes and where it stops

The official description establishes a runtime-adaptive, single-bitstream FPGA direction for multimodal inference. It identifies operator unification, mode-switchable systolic/SIMD/reduction paths, in-stream top-k pruning and dependency-aware RPU offload, and reports platform-specific latency, power and accuracy claims. It does not expose the full model graphs, compiler artifact, resource use, mode-transition cost, pruning policy, clock or complete energy accounting.

The [TRINE](../observed-subthemes/specialized-accelerators-and-dataflow.md#paper-dac-2026-research660) record is evidence of a reported FPGA/compiler co-design, not independent proof of a general multimodal speedup or preserved quality under all token and modality distributions. The explanation separates operator support, mode switching, pruning quality, graph overlap and platform-comparison boundaries.

<span id="explanation-dac-2026-research641"></span>

## Torr: cache-oriented reasoning must define what remains valid before it can reduce repeated work

### What the baseline computation is doing

Open-vocabulary detection lets a system detect categories that are not fixed in advance. A visual encoder produces representations from an image, and a text or query representation describes the requested concept. The system compares those representations and uses the resulting scores to make detection decisions.

Dense matching can be expensive because many visual positions, queries and intermediate features participate in the comparison. The cost is not only multiplication. Feature tensors must be read, moved, stored and compared, and later reasoning stages may repeatedly access related state. On an edge device, memory traffic and storage capacity can matter as much as arithmetic throughput.

### What the Torr co-design changes

Torr is described as replacing CLIP-style dense matching with hyperdimensional associative reasoning. Hyperdimensional computing represents an item or relation with a high-dimensional code and performs operations such as similarity, binding or association to retrieve related information. The representation changes the computation: the accelerator is no longer merely executing the original dense CLIP kernel faster. It is implementing a different reasoning path whose detection quality must be measured directly.

The co-design has two coupled parts. The algorithm decides which information can be represented, reused or updated. The hardware supplies storage, lanes, arithmetic, precision control and movement paths that match those decisions. A cache policy that looks efficient in an algorithm description is useful in hardware only if cached state is addressable, fits in the available memory, can be updated cheaply and can be invalidated when its assumptions no longer hold.

### Why temporal coherence permits caching

Consecutive frames or successive reasoning steps often share some objects, queries or graph relationships. Temporal coherence is useful when the next computation can reuse a previous result and when the unchanged portion can be identified without scanning everything again.

Query caching stores information that remains valid across a sequence. Delta updates process only the difference between the previous and current state. The system needs a precise validity rule: what event marks a query, object, relation or feature as changed; how the change is detected; how dependent cached entries are found; and when a full recomputation is required.

Cache hits reduce recomputation, but cache misses and invalidation are part of the workload. A scene with rapid motion, new objects or changing prompts can produce few hits and many updates. Storage for keys, dependencies, timestamps or confidence also consumes area and energy. A reported cache benefit must therefore include hit rate, update volume, lookup traffic and the workload's temporal distribution.

### What precision-gated item memory controls

The description names a lane-scalable, precision-gated item memory. A memory entry can be stored or processed at different precision levels when the decision tolerates different error. Gating requires a rule that identifies sensitivity and selects the precision, along with a representation for converting values and a policy for later refinement.

Lower precision can reduce storage, movement and arithmetic cost. It can also change similarity scores and graph decisions. The evaluation must measure detection quality and cache behavior at each precision policy, not only report a memory or energy reduction. Lane scalability also needs a definition: it may mean adding parallel item lanes, changing active lanes with workload size, or another organization. Each choice changes utilization, routing and memory bandwidth.

### How to interpret the reported claims

The captured description reports a 28 nm Torr accelerator, real-time detection, millijoule energy, competitive average precision and orders-of-magnitude lower energy. These claims need the dataset, image resolution, prompt set, AP definition, frame rate, latency boundary, cache hit rate, precision policy, memory traffic, clock, voltage, area and power boundary.

“Competitive AP” is not a complete quality statement without the reference model, vocabulary, confidence threshold and evaluation split. “Millijoule energy” needs the number of frames or detections, preprocessing and output transfer included, and whether static power is counted. An orders-of-magnitude comparison is meaningful only when the baseline performs the same task with the same quality target and measurement boundary.

### What the record establishes and where it stops

The official description establishes a cache-oriented algorithm–architecture co-design for task-oriented open-vocabulary detection. It identifies hyperdimensional associative reasoning, temporal query caching with delta updates, precision-gated item memory and a 28 nm accelerator, and it reports qualitative real-time, energy and accuracy claims. It does not expose the model, dataset, cache protocol, hit rate, precision levels, latency, area, power or exact comparison conditions.

The [Torr](../observed-subthemes/specialized-accelerators-and-dataflow.md#paper-dac-2026-research641) record is evidence of a reported reasoning and memory co-design, not independent proof of orders-of-magnitude energy reduction at preserved detection quality. The explanation separates representation change, cache validity, temporal reuse, precision gating and end-to-end task measurement.

<span id="explanation-dac-2026-research552"></span>

## UCME: a CPU matrix extension must separate matrix execution from the CPU pipeline without losing ordering or memory control

### What a matrix extension adds to a CPU

A CPU executes instructions through a pipeline that fetches, decodes, schedules and retires work. A matrix extension adds operations that process tiles of values together rather than treating every scalar or vector operation as an independent instruction. The extension needs arithmetic units, storage for matrix tiles, paths for loading and storing values, and an interface through which software describes the operation.

Matrix operations are not all the same size. A tile may be smaller than the hardware array at a boundary, and different models use different precisions, dimensions and reduction patterns. The extension must handle valid elements, partial tiles, accumulation order and the layout used by the CPU memory system. High arithmetic throughput is useful only if operands arrive and results leave at a matching rate.

### Why tight pipeline coupling limits reuse

When the matrix unit is tightly coupled to a CPU pipeline, its issue timing, register dependencies, execution ports, retirement rules and exception model become part of the matrix instruction design. A matrix operation may hold pipeline resources for a long interval, or the instruction set may need special rules for a particular CPU's register file and hazard logic.

That coupling makes integration harder across CPU architectures. A design that assumes one pipeline width, register arrangement or completion model may need a different implementation for another CPU. Software also has to expose the operation through an ISA and compiler interface that matches the hardware's tile shapes and data movement rules.

### What decoupling changes

UCME is described as decoupling the matrix unit from the CPU pipeline. In a decoupled design, the CPU submits a matrix command or descriptor and the matrix unit executes it through its own control and datapath. The CPU can continue with independent work while the matrix unit processes the tile, subject to dependencies and shared-resource contention.

This requires more than an independent arithmetic block. The system needs a submission interface, operand and result locations, dependency tracking, completion signaling, memory-order rules, exception behavior and a way to prevent a consumer from reading a result before the matrix operation is complete. If matrix work accesses memory shared with the CPU, cache coherence, ownership and bandwidth arbitration affect both correctness and performance.

The phrase “reuse existing compute and memory resources” also has a precise limit. Reuse can avoid duplicating storage or interfaces, but shared resources can become the bottleneck. A matrix unit may have enough multiply capacity while waiting for cache fills, or a vector unit may lose throughput because matrix transfers consume the same memory bandwidth.

### How matrix-vector overlap produces a gain

Matrix-vector overlap means that matrix work and vector work are active at the same time. It helps only when the two streams have independent dependencies and use resources that can operate concurrently. If both streams need the same cache ports, memory channels, execution units or interconnect, overlap changes scheduling but does not create additional capacity.

The maximum possible gain is bounded by the time that can be covered by useful independent vector work. The measured gain also depends on command submission, synchronization, tile boundaries, memory contention and the time spent with only one stream active. A 30% overlap gain therefore needs a defined baseline, workload schedule, overlap window, resource partition and measurement boundary.

### How to read the reported results

The captured description reports integration into four open-source RTL CPUs, over 90% utilization, up to 2.31× speedup on ResNet50, BERT and Llama3 over Intel AMX, a 30% gain from matrix-vector overlap, and a 4 TFLOPS-at-14-nm implementation occupying 0.53 mm².

Utilization must be defined: it could mean active matrix arithmetic cycles, occupied lanes, issued operations or another denominator. The speedup requires the exact CPU configurations, compiler and kernels, precision, tensor shapes, batch or sequence conditions, memory system and Intel AMX settings. The 4 TFLOPS and 0.53 mm² values require a frequency, arithmetic definition, process-library and voltage condition, and an area boundary that says whether memory, interconnect, control and CPU integration are included.

### What the record establishes and where it stops

The official description establishes a configurable matrix-extension direction that separates matrix execution from the CPU pipeline, supports asynchronous operations and targets matrix-vector overlap across four open-source RTL CPUs. It reports the numerical utilization, workload speedup, overlap and area/throughput claims above. It does not expose the ISA, compiler implementation, precision, frequency, energy, power, exact CPU configurations, workload mappings or reproducibility artifacts.

The [UCME](../observed-subthemes/specialized-accelerators-and-dataflow.md#paper-dac-2026-research552) record is evidence of a reported CPU-matrix-extension design, not proof that one implementation transfers unchanged across diverse CPUs or that the reported speedup is an end-to-end energy improvement. The explanation separates pipeline decoupling, asynchronous correctness, shared-resource contention, overlap opportunity and the conditions needed to interpret utilization and PPA.

<span id="explanation-dac-2026-research2157"></span>

## RFIPSA: a reconfigurable systolic array must show which dataflow changes and what the undefined FIP boundary contains

### What a systolic array is optimizing

A systolic array is a grid of processing elements that passes operands and partial sums through regular paths. A matrix operation is divided into tiles, and each processing element performs repeated multiply-accumulate work as data moves across the grid.

The regular movement reduces control and can reuse operands locally. It also imposes shape constraints. Matrix dimensions that do not fill the grid create idle cycles or boundary work. Different operators may need different operand reuse, reduction direction, precision, sparsity handling or output layout. A fixed dataflow can therefore be efficient for one kernel and poorly utilized for another.

### What reconfiguration can change

RFIPSA is described as a reconfigurable FIP-based systolic array. The official record does not define “FIP,” so its arithmetic, architectural or configuration meaning must remain unresolved. The record does establish the broader idea of selecting a configuration for various matrix-intensive workloads.

In general, reconfiguration might change array partitioning, operand flow, processing-element roles, precision, tile sizes, reduction paths or interconnect routes. Each change must preserve the mathematical operator and tensor layout. Partial sums cannot be lost when the mode changes, and memory interfaces must deliver data at the rate required by the selected array.

The transition path may include finishing the current tile, draining or resetting pipeline state, loading configuration, initializing buffers and restarting the next operation. If reconfiguration overlaps useful work, the design needs spare resources and a stated overlap schedule. If it does not, the transition time is part of kernel or layer latency.

### Why workload shape determines utilization

Utilization is not simply the number of processing elements divided by the array size. It depends on active cycles, valid lanes, tile boundaries, memory stalls, synchronization and producer/consumer balance. A small matrix may occupy only part of the array. A rectangular matrix may require padding or a different mapping. A reduction-heavy kernel may be limited by partial-sum movement rather than multiplication.

A matrix workload mix can include GEMM, convolution lowered to matrix operations, attention projections, batched products and scientific kernels. They may use different dimensions, precision, reuse and batch. A configuration that maximizes one kernel's steady-state rate can be poor for another or costly to switch between.

### What a fair comparison requires

The fixed systolic-array and GPU matrix-engine baselines must use the same operators, dimensions, precision, data layouts, correctness target and memory boundary. A complete result should report per-kernel throughput, utilization, latency, reconfiguration count and time, memory traffic, area, energy, frequency and the effect of incomplete tiles.

The evaluation should show both isolated kernels and a realistic sequence of layers or requests. It should say whether configuration is amortized per workload, layer, batch or request. A cross-workload average can conceal a large transition cost or a workload that receives no useful configuration.

### What the unresolved FIP term means for interpretation

The official record uses FIP in the title and method description but does not define it in the captured evidence. It could identify an arithmetic representation, processing structure, instruction interface or another design element, but no expansion should be inferred. Any claim about FIP-specific efficiency, precision or dataflow requires the source definition and paper-level details.

### What the record establishes and where it stops

The official description establishes RFIPSA as a reconfigurable systolic-array direction for varied matrix-intensive workloads and qualitatively claims cross-workload matrix efficiency. It names a fixed systolic array and GPU matrix engine as comparison categories. It does not define FIP or report throughput, utilization, reconfiguration time, area, energy, precision, workload coverage, process or silicon results.

The [RFIPSA](../observed-subthemes/specialized-accelerators-and-dataflow.md#paper-dac-2026-research2157) record is evidence of a reconfigurable matrix-dataflow proposal, not proof of a better general matrix engine. The explanation separates steady-state array throughput from transition cost, utilization from array size, cross-workload flexibility from a defined FIP mechanism, and qualitative architecture intent from silicon evidence.

<span id="explanation-dac-2026-research1569"></span>

## FILCO: composable DNN hardware is useful only when composition and reconfiguration cost less than the utilization they recover

### Why DNN layers need different hardware shapes

A DNN model is a sequence of operators. Convolution, matrix multiplication, attention, normalization and elementwise functions use different tensor dimensions, reuse patterns, reductions, precision and memory traffic. A fixed accelerator can be highly efficient for one shape while leaving resources idle or requiring inefficient tiling for another.

A general FPGA can implement many operators, but it pays for programmable routing, configuration, control, memory interfaces and a software toolchain. FILCO describes a composable architecture intended to assemble or configure resources for changing DNN workloads.

### What composition means at the dataflow boundary

Composable hardware divides the fabric into units that can be connected or assigned to an operator. A useful composition must define the data interfaces, buffer ownership, precision, tile shape, reduction path, synchronization and output layout. The units must exchange tensors at a rate that matches producer and consumer computation.

Composition is more than connecting arithmetic blocks. If a producer emits tiles faster than a consumer can accept them, queues grow or backpressure stalls the pipeline. If adjacent layers use different layouts, a transformation or buffer is needed. If a reduction crosses units, partial sums need ordering and storage. The interface and movement cost can erase the benefit of reusing the fabric.

### What real-time reconfiguration changes

Real-time reconfiguration changes the active datapath between workload segments or while other fabric remains active. The system needs configuration storage, a controller, a switching protocol, isolation or quiescing, state preservation and a resume rule.

The transition path includes detecting the next operator, selecting a configuration, loading or applying it, draining the old pipeline, preserving weights and intermediate tensors, initializing the new dataflow and restarting execution. Configuration time, bitstream bandwidth, control energy and buffer movement are part of inference cost. If reconfiguration overlaps useful computation, the overlap requires spare resources and a stated schedule.

### Why utilization recovery is workload-dependent

A composable fabric can recover utilization when operator shapes change slowly enough to amortize configuration and when the selected resources match the layer's arithmetic and memory demands. It may not help when layers are short, requests interleave, shapes change every step or the fabric must repeatedly switch modes.

Configuration can also leave part of the fabric unused. A layer may need many multipliers but little memory, while another needs memory bandwidth and reduction capacity. The best configuration is not necessarily the one with the most arithmetic units. It must balance compute, buffer capacity, interconnect, memory bandwidth, tile boundaries and synchronization.

### What a complete comparison must measure

The fixed-function DNN accelerator and general FPGA baselines must use the same models, operators, tensor shapes, precision, batch, quality target and memory boundary. The evaluation should report per-layer and full-model latency, utilization, configuration count and time, bitstream/configuration size, energy, area, memory traffic, stalls and accuracy.

It should include short and long layers, operator transitions, concurrent requests, changing batch, unsupported operators and reconfiguration overlap. A kernel result measured after configuration is not the same as end-to-end inference that includes configuration and switching. A model average can hide a few expensive transitions that dominate tail latency.

### What the record establishes and where it stops

The official description establishes FILCO as a composable, real-time-reconfigurable DNN-acceleration direction. It qualitatively claims reconfigurable acceleration and names a fixed-function DNN accelerator and general FPGA accelerator as comparison categories. It does not report latency, utilization, reconfiguration time, area, energy, accuracy, operator coverage, configuration size or hardware conditions.

The [FILCO](../observed-subthemes/specialized-accelerators-and-dataflow.md#paper-dac-2026-research1569) record is evidence of a flexible-fabric proposal, not proof of better complete DNN inference. The explanation separates composition from dataflow correctness, reconfiguration from steady-state kernel time, recovered utilization from control cost, and qualitative flexibility from layer- and transition-inclusive measurements.

<span id="explanation-dac-2026-research1480"></span>

## ADAPT: training-free token pruning must preserve temporal event and attention state, not only reduce the number of tokens processed

### What a spiking transformer processes

A spiking model represents activity as events over time. A neuron can emit a spike when its state crosses a threshold, and its internal state can carry information to later time steps. A spiking transformer combines this temporal event processing with attention or transformer-style token interactions.

The same token can be inactive at one time step and important at another. Its current event activity is not the whole information state. The model may also need an accumulated membrane value, attention context, position, mask or other temporal state. A pruning rule must define whether it removes a token for one step, for a time interval or for the rest of an inference sequence.

### What token pruning changes

Token pruning removes tokens or token-state updates judged unlikely to affect the output. This can reduce attention interactions, feature movement, event routing and downstream arithmetic. It also changes which tokens participate in normalization, attention scores, aggregation and temporal state updates.

The pruning decision needs a score or rule, a decision time, a threshold or budget, and a recovery policy. If a removed token can return, its state must be preserved or reconstructed. If it cannot return, the method must show that its future contribution is bounded under the workload. A rule that is safe for dense spatial tokens may not be safe for temporally sparse events.

### What training-free means here

Training-free pruning does not adapt model weights to the pruning errors through retraining or fine-tuning. That reduces preparation cost and makes deployment simpler, but it leaves the original model exposed to the distribution change created by pruning.

The method must choose its signal from the existing model and current execution state, such as event count, attention score, accumulated state or a structural priority. The signal can be cheap and still be misleading. A token with few current events may carry a persistent state or become important after another token changes the attention context.

### What hierarchical pruning changes

A hierarchy can make a coarse decision first and spend more computation only on candidates that pass. For example, a cheap stage can group or filter tokens before a finer stage evaluates attention or temporal importance. This can reduce expensive work when the coarse signal is predictive.

The hierarchy also introduces additional state and control. The accelerator must store candidate identity, preserve temporal state, coordinate decisions across layers or time steps, and handle tokens that cross hierarchy boundaries. An incorrect coarse decision can discard information before the fine stage has a chance to inspect it. The evaluation must report the cost of scoring, buffering, routing and synchronization.

### Why event reduction is not automatically hardware speedup

An event-driven accelerator can skip inactive operations, but it still pays for event detection, addresses, routing, queueing, synchronization, memory reads and state updates. The benefit depends on event rate, burstiness, spatial/temporal locality, queue capacity and the balance between active and inactive tokens.

Pruning may reduce attention arithmetic while creating irregular memory access or load imbalance. If different processing elements receive different token counts, some remain idle. If the hierarchy changes the active set frequently, configuration and data movement can dominate. Latency, energy and area must include the control and memory path, not only the removed operations.

### What quality evaluation must show

The dense spiking-transformer and static-token-pruning baselines must use the same model, event encoding, number of time steps, task, quality target and output protocol. Evaluation should report accuracy or task quality, token/event retention, temporal error, attention changes, latency, energy, area, memory traffic, utilization and sensitivity to event rate.

The work should also test cases where importance changes over time, events are bursty, tokens are near the pruning threshold, and the sequence is long enough for state errors to accumulate. A single average sparsity number does not establish that temporal information is preserved.

### Source boundary

The official title is truncated in the captured record. It identifies ADAPT as algorithm-hardware co-design for a spiking transformer with training-free adaptive token pruning and a hierarchy, but does not expose the full title or method details. That missing source information is itself part of the evidence boundary.

### What the record establishes and where it stops

The official description establishes ADAPT as a training-free adaptive-token-pruning and hierarchical hardware co-design direction for spiking-transformer workloads. It qualitatively claims pruning efficiency and names dense spiking-transformer execution and static pruning as comparison categories. It does not report accuracy, sparsity, latency, energy, area, event rate, time steps, model or hardware results, and the title is truncated.

The [ADAPT](../observed-subthemes/specialized-accelerators-and-dataflow.md#paper-dac-2026-research1480) record is evidence of an event-driven pruning direction, not proof of preserved temporal quality or faster spiking-transformer inference. The explanation separates current events from temporal state, token removal from safe model semantics, event sparsity from hardware speedup, and qualitative co-design from validated deployment.

<span id="explanation-dac-2026-research2888"></span>

## Enabling AI ASICs for zero-knowledge proof: dense approximate-tensor assumptions do not transfer to exact proof arithmetic automatically

### What an AI ASIC usually optimizes

An AI ASIC commonly targets regular tensor operations such as matrix multiplication and convolution. It uses fixed data types, repeated tiles, predictable reuse and parallel arithmetic units. Many AI workloads can tolerate bounded numerical approximation because task accuracy, rather than exact equality of every intermediate, is the final criterion.

Zero-knowledge proof generation has a different contract. The prover must produce a proof that satisfies exact algebraic relations for a specified circuit and witness. Its operations may include finite-field addition and multiplication, modular reduction, polynomial transforms, commitments, elliptic-curve or group arithmetic, hashing and phase-specific memory movement.

The difference is not only the arithmetic operator. Operand widths, modulus, reduction rules, data layout, control dependencies, intermediate lifetime and correctness checks all come from the proof system. A dense AI dataflow can be useful for some regular kernels, but its suitability must be demonstrated per proof stage.

### What exact finite-field arithmetic requires

A finite field contains a fixed set of values with addition, subtraction and multiplication performed modulo a field modulus. Hardware must represent field elements at the required width, perform the operation without losing information, and reduce the result according to the field definition. Approximate rounding or a numerically close result is not acceptable if it changes the proof relation.

The modulus, curve, polynomial degree and proof system determine datapath width and reduction cost. Intermediate values may need wider storage before reduction. Different phases can use different layouts or access orders. A datapath that is efficient for ordinary integer or floating-point matrix multiplication does not establish exact field behavior.

### Where AI dataflow ideas can and cannot transfer

AI-ASIC techniques such as tiled computation, local buffers, data reuse, spatial arrays, compression and configurable scheduling may help when a proof kernel has regular repeated work. But proof workloads also contain permutations, irregular memory access, phase transitions, large intermediate arrays and operations whose operand widths or dependencies change.

The memory system must move polynomials, trace data, witness values, commitments and intermediate results. A high arithmetic rate is unhelpful if the next stage needs a different ordering or if local storage cannot hold the working set. Reordering, buffering, synchronization and host/device transfer belong in the proof-system measurement boundary.

### Why programmability changes the hardware tradeoff

An ASIC specialized for one curve and field can hardwire reduction constants, widths, schedules and buffers. This can reduce control and improve peak area, latency and energy. A programmable or configurable design can support more proof systems, but it needs instruction decoding, parameter storage, routing choices, general arithmetic, configuration checks and fallback paths.

Flexibility can also mean emulating an operation that lacks a native datapath. The evaluation must state which proof systems are native, which are configured, which are software-assisted, and how performance changes across them. A qualitative claim that AI-ASIC ideas “enable” ZK does not identify this boundary.

### What correctness and end-to-end evaluation require

The accelerator must be compared with a reference implementation for field arithmetic, polynomial operations and every proof phase. The generated proof must be accepted by the intended verifier for the same circuit, witness, curve, field and security level. The evaluation should include circuit sizes, proof phases, memory traffic, host work, configuration, initialization, proof assembly and any unsupported operations.

GPU/FPGA proving and a general-purpose AI ASIC are different baselines. They must use the same proof system, correctness condition, circuit, host boundary, software and output. Measurements should report proof latency, throughput, area, energy, memory capacity and bandwidth, flexibility, utilization and quality of the proof result. A kernel-level arithmetic result is not a complete prover result.

### What the record establishes and where it stops

The official description establishes an exploration of AI-ASIC techniques for zero-knowledge proofs, involving large finite-field arithmetic and memory. It qualitatively claims ZK acceleration and names GPU/FPGA proving and a general-purpose AI ASIC as comparison categories. It does not report architecture, proof throughput, latency, area, energy, flexibility, circuit coverage, exactness, process or host boundary.

The [AI ASIC for ZK](../observed-subthemes/specialized-accelerators-and-dataflow.md#paper-dac-2026-research2888) record is evidence of a hardware-methodology direction, not proof that AI-ASIC structures preserve exact proof semantics or improve complete proving. The explanation separates dense approximate tensor execution from exact field arithmetic, arithmetic rate from memory/dataflow cost, flexibility from specialization, and qualitative exploration from end-to-end validation.

<span id="explanation-dac-2026-research272"></span>

## ZK-Flex: reusable proof hardware must expose enough of each proof system without losing the efficiency of specialization

### Why zero-knowledge proof systems differ in hardware work

A zero-knowledge proof system turns a computation and witness into a proof that a verifier can check without learning the private witness. Different systems make different algebraic choices. They can use different finite fields, elliptic curves, polynomial representations, commitment schemes, hashing, transforms and proof phases.

Those choices affect operand width, reduction, memory layout, data movement, intermediate size, access order and the balance between arithmetic and memory. A fixed accelerator can hardwire one set of choices and optimize its datapath, but the hardware may not transfer well to another proof system.

### What a flexible framework must abstract

ZK-Flex describes a flexible scalable acceleration framework. For flexibility to be useful, it must define which parts are common interfaces and which parts are configurable. Possible common interfaces include field addition/multiplication, modular reduction, polynomial transforms, group operations, hashing, memory movement and synchronization. The exact abstraction is not exposed in the captured description.

An abstraction that is too narrow forces software to emulate unsupported operations and loses performance. One that is too broad adds programmable routing, control, parameter loading and storage that a fixed accelerator would not need. The framework must also preserve exact arithmetic, proof-phase ordering and the layout expected by downstream stages.

### What reconfigurability and heterogeneity cost

A reconfigurable or heterogeneous accelerator can select different arithmetic units, memory paths or schedules for different proof systems. The transition may require loading configuration, initializing parameters, flushing or preserving state, changing buffer layouts and rebuilding a dataflow schedule.

The static resources remain present even when a mode is not active. Flexible routing, control storage, multiplexers, configuration memory, unused arithmetic capacity and interface logic contribute to area and power. A fixed accelerator can use narrower paths, simpler control and more specialized buffering for one proof system.

The comparison therefore has two dimensions: reuse across proof systems and peak efficiency for each system. A framework can be valuable because it avoids a separate chip for each scheme while still having lower peak throughput than a dedicated design. The area, energy and performance tradeoff must be reported rather than reduced to a single speed claim.

### What scalability can mean

“Scalable” can refer to increasing circuit size, proof size, arithmetic units, memory capacity, number of accelerator tiles or number of devices. These cases have different limits. Larger circuits may exceed local memory and require streaming. More arithmetic units may increase memory pressure or synchronization. Multiple devices add partitioning, communication and consistency.

The framework must state what is scaled and how the proof remains identical. A larger system can lower per-proof latency while increasing energy or configuration time. A batch of proofs can amortize setup that matters for one proof. Host preparation, transfers, proof assembly and verification-related work must remain in the defined measurement boundary.

### What a proof-system-diverse evaluation requires

The CPU/GPU and fixed-ZK-accelerator baselines need the same proof system, curve/field, circuit, witness, security level, correctness target and software boundary. The evaluation should cover systems with different arithmetic and memory behavior, circuits of different sizes, configuration changes, memory spills, single and batched proofs, and all supported proof phases.

It should report proof latency, throughput, configuration time, memory capacity and traffic, area, power, energy, host work, utilization and proof correctness. If flexibility lowers peak performance, the tradeoff should be visible per proof system. A framework-level claim without these comparisons establishes an interface concept, not a measured general accelerator benefit.

### What the record establishes and where it stops

The official description establishes ZK-Flex as a flexible scalable framework for zero-knowledge-proof acceleration. It qualitatively claims proof acceleration and flexibility and names CPU/GPU proving and a fixed ZK accelerator as comparison categories. It does not report proof latency, throughput, area, energy, memory, configuration cost, proof-system coverage, curve, circuit or hardware results.

The [ZK-Flex](../observed-subthemes/specialized-accelerators-and-dataflow.md#paper-dac-2026-research272) record is evidence of a reusable proof-acceleration direction, not proof of faster, smaller or equally correct proving across systems. The explanation separates proof-system abstraction from hidden work, configurability from specialization, resource scaling from proof throughput, and qualitative flexibility from proof-system-diverse evidence.

<span id="explanation-dac-2026-research2256"></span>

## ALOHA: a stochastic bitstream is an arithmetic representation whose correlations and finite length are part of the result

### What stochastic computing represents

Stochastic computing represents a numerical value by a stream of bits. In a simple unipolar representation, the fraction of ones over a stream of length (N) estimates a value between zero and one. A stream with 250 ones in 1000 positions represents approximately 0.25. Signed and scaled representations use additional encoding rules.

The representation trades arithmetic hardware for time and statistical error. A simple bitwise operation can estimate an arithmetic operation, but the estimate is not exact for a finite stream. Longer streams reduce sampling error while increasing latency, switching activity and storage or generation work.

### Why correlation changes the arithmetic

For two stochastic streams (A) and (B), an AND operation counts positions where both bits are one. It estimates the product of the probabilities only under appropriate independence or correlation conditions. If ones in the two streams occur at related positions, the joint probability can be larger or smaller than the product of the individual probabilities.

This means that the sequence generator and the wiring between streams are part of the arithmetic definition. Reusing one sequence, delaying a stream, feeding outputs into later operators or sharing a generator can create correlation. The individual streams can still have the correct number of ones while the computed product is biased.

Correlation can accumulate across a neural or signal-processing pipeline. A nonlinear operation, feedback path, multiplexing choice or conversion can change the relationship between streams. A sequence property measured at the input does not automatically hold after several operators.

### What Hammersley sequences are intended to provide

A Hammersley sequence is a low-discrepancy point construction intended to distribute samples more evenly through a multidimensional space than a simple random sequence. A hardware design can map sequence coordinates to thresholds, bitstreams or multiple operands. The goal is often to reduce uneven sampling error with fewer samples.

The benefit depends on the mapping. The design must specify dimensions, sequence length, generation circuit, scrambling or randomization, threshold encoding, stream reuse and how outputs are fed into nonlinear operations. Low discrepancy is a property of a point set; it does not by itself guarantee independent arithmetic streams, unbiased products or lower application error.

### What the hardware path includes

The stochastic datapath includes sequence generation, probability encoding, bitwise operators, counters or accumulators, scaling, signed-value handling and conversion back to a conventional number. It may also need decorrelation, delay, buffering or separate generators for operands.

Area and power can fall when a wide multiplier is replaced with small logic, but sequence generation and long execution time can add cost. A comparison must include the number of cycles needed for the target error, clock frequency, generator logic, counters, buffers, conversion, memory and control. A logic-gate count for the operator is not complete system area or energy.

### What numerical evaluation must show

The evaluation should report stream length, representation, input distribution, correlation measure, arithmetic error, bias, variance, worst-case and distributional behavior, and the effect of nonlinear pipeline stages. Neural workloads also need task accuracy; signal-processing workloads need the relevant signal error or quality metric.

The conventional stochastic-sequence and binary fixed-point baselines must use equal output precision or error targets. A shorter Hammersley stream may look efficient if it is allowed a larger error. A fixed-point design may use more gates but finish in fewer cycles. Area, power, latency and quality must be measured over the same complete kernel boundary.

### What the record establishes and where it stops

The official description establishes ALOHA as a Hammersley-sequence stochastic-computing architecture intended for area and power efficiency. It qualitatively claims area and power benefits and names conventional stochastic sequences and binary fixed-point arithmetic as comparison categories. It does not report accuracy, stream length, area, power, latency, workloads, sequence generator, correlation or conversion conditions.

The [ALOHA](../observed-subthemes/specialized-accelerators-and-dataflow.md#paper-dac-2026-research2256) record is evidence of a low-discrepancy stochastic-computing direction, not proof of unbiased arithmetic or lower complete-system energy. The explanation separates bit probability from joint correlation, sequence structure from hardware arithmetic, operator area from stream latency, and qualitative efficiency from numerical validation.

<span id="explanation-dac-2026-research341"></span>

## TAG: topology-aware GNN hardware must adapt its dataflow without making configuration the new bottleneck

### Why graph topology changes accelerator behavior

A GNN layer reads node features and graph structure, combines information from neighbors, and produces updated features. The graph determines how many neighbors each node has, which nodes are reused, how adjacency entries are laid out, and where partial sums must be reduced.

Two graphs with the same number of nodes and edges can produce different hardware behavior. A graph with local communities may reuse nearby features and fit a partition well. A graph with high-degree hubs may require many feature reads and create reduction hotspots. A graph with scattered edges may produce irregular addresses and poor memory locality. A fixed accelerator dataflow cannot be optimal for all of these patterns.

### What topology-aware configuration can change

TAG describes a configurable topology-aware GNN accelerator. The configuration can select how the graph is traversed, how features and adjacency data are placed in the memory hierarchy, how processing elements receive work, how tiles are formed, and where aggregation occurs. The exact modes and topology classifier are not exposed in the captured description.

The configuration must preserve the GNN operation. It must respect edge direction, relation type when present, aggregation function, normalization, feature precision and dependency order. Choosing a traversal because it has good memory locality is not enough if it changes which messages are combined or when a partial result becomes visible.

Topology analysis itself has a cost. The system may inspect degree distributions, locality, partition boundaries or reuse before selecting a mode. If the graph changes frequently, analysis and reconfiguration can occur often. If the graph is static, the cost may be amortized, but the configuration must remain valid for every layer and feature layout that uses it.

### Why a memory hierarchy matters

The accelerator may keep frequently reused node features in a local buffer, stream adjacency entries from another level, and store partial sums near the processing elements. The right placement depends on feature size, degree, reuse distance, buffer capacity and access order.

Irregular graph access can defeat a simple cache. High-degree nodes can turn one feature into a hot item, while low-degree regions may have little reuse. A memory-efficient dataflow must account for address generation, metadata traffic, bank conflicts, interconnect contention, synchronization and output writes. Reducing feature reads at one level can increase traffic at another if data is replicated or repacked.

### What configurability costs

Configurable hardware needs control storage, multiplexers, routing choices, mode-specific buffers, configuration interfaces and verification of each mode. Flexible processing elements may have lower peak efficiency than a fixed unit. Configuration decisions can add pipeline stages, stalls or reinitialization work.

The correct comparison is not only area of the arithmetic units. It includes control and configuration logic, memory capacity, ports, interconnect, clock power, reconfiguration time and the cost of detecting or encoding topology. A GPU baseline may use more general hardware but amortize its programming and scheduling system differently from a dedicated configurable accelerator.

### What a complete evaluation must compare

The fixed GNN accelerator and GPU baselines must use the same graph datasets, model layers, feature dimension, precision and output correctness. The evaluation should sweep graph size, degree skew, locality, community structure, edge cut, feature reuse, layer type and topology mode. It should report configuration time, memory traffic by level, utilization, reduction stalls, latency, throughput, area, energy, accuracy and sensitivity to graph changes.

A topology-aware best case does not establish broad benefit. The system should show when the selected mode changes, what analysis it uses, how often it is wrong or suboptimal, and whether reconfiguration cost is included. Memory efficiency also must be separated from compute efficiency; fewer feature bytes do not guarantee faster execution if reductions or control dominate.

### What the record establishes and where it stops

The official description establishes TAG as a configurable topology-aware GNN accelerator with a graph memory hierarchy. It qualitatively claims memory and compute efficiency and names fixed GNN acceleration and GPU GNN execution as comparison categories. It does not report speed, energy, area, memory, accuracy, graph diversity, topology analysis, configuration overhead or hardware conditions.

The [TAG](../observed-subthemes/specialized-accelerators-and-dataflow.md#paper-dac-2026-research341) record is evidence of a topology-aware accelerator direction, not proof of better GNN execution across graph families. The explanation separates topology analysis from execution, memory reuse from compute throughput, configurable flexibility from control/area cost, and qualitative efficiency from topology-diverse results.

<span id="explanation-dac-2026-research3050"></span>

## Adaptive graph-transformer training: partitioning must balance attention data, communication, memory, and convergence

### What a graph transformer adds to graph training

A graph neural network updates node representations using graph relationships. A graph transformer applies attention-like operations to node features, using learned projections and scores to determine how information is combined. The exact attention scope may be local to graph neighborhoods or broader, but in either case the computation needs feature data, graph structure and intermediate attention state.

Large graphs create two scaling problems. The feature and parameter tensors may exceed one device's memory, and the graph's edges or attention relationships may cross device boundaries. A device may need remote node features, edge metadata or partial results before it can complete a layer. Training adds gradients, optimizer state and parameter synchronization to the forward-pass traffic.

### What partitioning decides

A distributed system partitions nodes, edges, features, attention work or combinations of these across devices. A node partition can keep local features near the computation but creates boundary traffic for edges that connect partitions. Replicating boundary features can reduce repeated communication while increasing memory and update consistency work. Partitioning attention work can balance arithmetic but require more feature exchange.

The partition must preserve the graph-transformer computation. It must identify all required neighbors or attention inputs, fetch the correct features, combine partial scores and outputs, and synchronize gradients and parameters according to the training algorithm. Cutting or approximating relationships can change the model unless the method defines and evaluates that approximation.

### Why graph structure controls scaling

Graph degree and topology determine communication and load balance. A high-degree node can require many remote features or create a reduction hotspot. A partition with equal node counts can still have unequal edge cuts, attention work or memory use. Community structure may reduce communication for one graph and fail for another.

The system also stores more than node features: adjacency or edge attributes, attention intermediates, gradients, optimizer state and possibly replicated boundary data. Device memory and interconnect bandwidth can become the limits before arithmetic capacity. A layer throughput result must therefore state graph size, degree distribution, partition, feature dimension, batch, precision, memory use and communication volume.

### What adaptive scaling changes

An adaptive framework can change partitioning, replication or resource allocation as graph load and device state change. It needs a signal: measured memory pressure, communication volume, queue length, degree imbalance, straggler time or another estimate. It then needs to compute a new decision, migrate or rebuild partition state, synchronize parameters, and resume training.

Adaptation has a cost. Repartitioning can move features and edge metadata, invalidate caches, recreate communication plans and temporarily stop the training step. If the graph or workload changes slowly, adaptation may be worthwhile. If it changes rapidly or the batches are short, the controller and migration cost can exceed the saved time. Dynamic behavior can also make runs less reproducible unless the policy and state are recorded.

### Why throughput is not convergence

Distributed training must be measured at two levels. Systems performance includes step time, samples or edges per second, communication, memory and energy. Learning behavior includes loss trajectory, final accuracy, number of optimizer steps, effective batch, gradient synchronization, random seeds and convergence time.

A method can reduce step time while changing the effective optimization process through stale parameters, altered sampling, partition-dependent attention or approximate communication. Comparing elapsed time without equal final quality can misstate the benefit. The single-device and static-distributed baselines need the same model, data, precision, training schedule, quality target and stopping rule.

### What a complete evaluation must include

The evaluation should sweep graph size, topology, degree skew, edge-cut fraction, feature dimension, attention scope, GPU count, memory capacity, interconnect, batch and precision. It should report local and remote bytes, synchronization time, straggler time, repartition/migration time, peak memory, step throughput, energy, loss and final quality.

The adaptive policy should be compared with no adaptation and static partitioning under the same workload. The measurement must show whether gains come from better partitioning, replication, more devices, reduced communication or a changed training workload. A large graph best case cannot establish general scaling.

### What the record establishes and where it stops

The official description establishes a scalable adaptive parallel-training direction for graph transformers on large graphs. It qualitatively claims training scalability and efficiency and names single-device training and static distributed partitioning as comparison categories. It does not report throughput, convergence, accuracy, memory, communication, energy, graph scale, topology or hardware results.

The [adaptive graph-transformer training](../observed-subthemes/specialized-accelerators-and-dataflow.md#paper-dac-2026-research3050) record is evidence of a distributed-training proposal, not proof of faster or equally converged graph-transformer training. The explanation separates partitioning from communication, step throughput from convergence, adaptive decisions from migration cost, and arithmetic scaling from graph-topology behavior.

<span id="explanation-dac-2026-research2897"></span>

## EXRA: an expandable register file helps only when the ISA and compiler can keep the right data live without making the processor expensive

### What register pressure means

An instruction stream uses values that remain live between their definition and their last use. The register allocator tries to keep those values in a small, fast register file. When too many values are live at once, some must be spilled to a cache or memory and reloaded later.

Spills add instructions and address calculations. They consume cache and memory bandwidth, increase latency and energy, and can interfere with unrelated data. Data-dominated applications are especially sensitive when the computation performs little arithmetic per byte moved or when a working set is repeatedly reused.

Register pressure depends on the loop schedule, unrolling, vector width, dependency chain, calling convention, register-file port count and cache behavior. It is not determined only by the total amount of data in the program.

### What an expandable register file changes

EXRA describes ISA extensions and a register file that can expand beyond a conventional capacity. The intended effect is to keep more live values close to the execution units and reduce spills. The expansion could be additional banks, an attached register storage level or another architectural mechanism; the captured description does not specify which.

The processor must define how an instruction names an expanded register, how many operands can be read and written, when the data is available, and how dependencies and bypasses work. If expanded registers have a different latency from ordinary registers, the pipeline and scheduler must model that difference. If they are banked, conflicts can serialize accesses. If expansion is dynamically enabled, the hardware needs allocation, power and state-management rules.

The architectural state also includes the expanded values. Context switches, interrupts, exceptions, function calls and thread migration must preserve them or explicitly invalidate and reconstruct them. A larger register state can reduce application spills while increasing save/restore traffic and operating-system complexity.

### Why ISA and compiler design are one problem here

An ISA extension is useful only when software can select it reliably. The compiler must identify values worth placing in the expanded file, estimate their lifetime and access frequency, allocate them without conflicts, generate the required instructions, and fall back to ordinary registers or memory when the feature is unavailable.

The allocation decision can change the schedule. Keeping one value live may avoid repeated loads but increase the lifetime of other values and create register or bank conflicts. Loop transformations, function boundaries, alias analysis, calling conventions and register spilling all interact with the feature. A microbenchmark written to exploit the extension does not establish that a general compiler finds the same benefit.

### What the complete data path costs

The benefit should be measured against the conventional register file and memory-resident movement with the same processor and compiler. The measurement must include instruction count, spill/reload traffic, register-file accesses, cache/memory accesses, pipeline stalls, frequency, area, power and context-switch behavior.

An expandable file may reduce off-chip or cache traffic while increasing on-chip wire length, ports, banking, clock power and access latency. If the workload has few live values, the extra hardware may provide no benefit. If it has many threads or frequent context switches, the larger architectural state may become a cost.

### What the record establishes and where it stops

The official description establishes EXRA as an ISA and expandable-register-file direction for data-heavy execution. It qualitatively claims execution efficiency and names a conventional ISA/register file and memory-resident movement as comparison categories. It does not report performance, energy, area, compiler complexity, register configuration, context-switch cost or workload results.

The [EXRA](../observed-subthemes/specialized-accelerators-and-dataflow.md#paper-dac-2026-research2897) record is evidence of a register-locality architecture proposal, not proof of better compiled application performance. The explanation separates register capacity from register access cost, spill reduction from complete memory behavior, ISA capability from compiler exploitation, and local efficiency from processor-wide PPA.

<span id="explanation-dac-2026-research2698"></span>

## BiBNN: reducing Bayesian computation is useful only if predictive uncertainty and its calibration survive the conversion

### What Bayesian neural inference is estimating

A deterministic neural network uses one set of parameter values and produces one output for an input. A Bayesian neural network represents uncertainty about parameters or predictions. It uses a distribution or an approximation to a distribution, then combines results from stochastic parameter samples or forward passes.

The mean of several predictions can be used as a central estimate. The variation across predictions can indicate uncertainty, but only if the sampling distribution represents the intended sources of uncertainty. Accuracy and uncertainty are different outputs. A model can preserve average accuracy while becoming overconfident, or have useful uncertainty while slightly changing its mean prediction.

Multiple Bayesian samples are expensive because each sample may require a neural forward pass. The cost includes weight or mask generation, loading sample-specific values, arithmetic, activation, accumulation, output storage and aggregation. The cost of random-number generation and sample coordination belongs in the computation boundary.

### What Bernoullization changes

Bernoulli behavior takes one of two outcomes according to a probability. Bernoullization can represent a stochastic quantity using binary random choices, potentially allowing bit-level operations or simpler hardware. The exact meaning matters: it may convert a parameter, a mask, an activation, a probability or a sampling decision.

A conversion can preserve an expected value without preserving variance or correlations. For example, independent binary choices can have the correct average but produce a different joint distribution from the original Bayesian parameter sample. Those dependencies can affect the prediction spread and the model's behavior on uncertain or out-of-distribution inputs.

The method therefore needs to specify the variable being Bernoullized, its probability, scale, sampling frequency, correlation structure, accumulation rule and how many samples are used. The captured description names post-training Bernoullization but does not expose these details.

### Why post-training conversion has a different risk

Post-training conversion operates on a model already trained or calibrated under another representation. It avoids retraining, but the converted model may not have learned to compensate for the new sampling noise, binary representation or lost correlations. A conversion applied to weights, activations or masks can affect different parts of the predictive distribution.

The comparison must state the original Bayesian approximation, the converted representation, initialization, number of samples, random seed policy, aggregation rule and deterministic baseline. It must measure both the mean task output and uncertainty behavior. A lower operation count is not a substitute for evidence that the posterior or predictive distribution remains useful.

### What an inference accelerator must account for

Binary or probabilistic computation can reduce multiplier complexity, but it may add random-number generation, bit packing, unpacking, popcount or repeated sample accumulation. If samples are processed serially, the system may trade per-sample cost for more passes. If samples are processed in parallel, memory and bandwidth can increase.

The hardware boundary should include random generation, sample-specific weight/mask access, activation storage, accumulation across samples, calibration outputs, control, memory traffic and any conversion between binary and higher-precision values. A count of multiply operations saved is not the same as latency or energy saved.

### What uncertainty evaluation must show

Task accuracy should be reported alongside calibration and uncertainty metrics. Useful tests include confidence calibration, selective prediction or risk-coverage, out-of-distribution detection, uncertainty under distribution shift, variance of repeated outputs and the separation of parameter/model uncertainty from data noise when the method claims to preserve it.

The comparison must use the same dataset, task, model, sample budget and evaluation protocol for full Bayesian inference, Bernoullized inference and deterministic approximation. The 88.6% number must identify what operations were counted and whether random generation, memory, sample aggregation, nonlinear functions and unsupported layers were included.

### What the record establishes and where it stops

The official description establishes BiBNN as a post-training Bernoullization direction for reducing Bayesian neural-network inference computation. Its title claims an 88.6% computation reduction and the card names full Bayesian inference and deterministic approximation as comparison categories. It does not report the model, conversion rule, samples, operation boundary, accuracy, calibration, uncertainty, hardware or energy conditions.

The [BiBNN](../observed-subthemes/specialized-accelerators-and-dataflow.md#paper-dac-2026-research2698) record is evidence of a stochastic low-cost Bayesian-inference proposal, not proof that Bayesian uncertainty is preserved or that a deployed system is faster and more efficient. The explanation separates mean prediction from uncertainty, expected value from distributional fidelity, operation count from system cost, and post-training conversion from calibrated task behavior.

<span id="explanation-dac-2026-research2125"></span>

## Overmind NSA: a unified neuro-symbolic accelerator must preserve exact symbolic decisions while controlling neural approximation and memory state

### What neuro-symbolic computation combines

Neural computation represents patterns with numerical values and learned functions. It commonly uses matrix operations, nonlinear activations and approximate numerical representations. Symbolic computation manipulates discrete entities, rules, predicates, relations or search states. It often depends on exact equality, ordering, indices, masks or control decisions.

A neuro-symbolic application connects these forms of work. A neural module may propose candidates or scores, while a symbolic module applies rules, constraints or search. The interface may pass tensors, token IDs, relation tables, masks, states or control signals. The different semantics create different requirements for precision, control flow, storage and correctness.

### What approximate nonlinear activations change

A neural activation maps an input value to an output value. Functions such as ReLU, sigmoid, tanh or a learned approximation can be expensive because they require comparisons, exponentials, divisions or lookup/interpolation. An accelerator can replace an exact function with a cheaper approximation.

The effect of approximation depends on the input range, slope, error distribution and how many layers compose the function. A small pointwise error can be amplified by later weights or can move a value across a threshold. If the activation output feeds a symbolic predicate, even a small numerical change can change a discrete branch. Therefore neural task accuracy and symbolic decision correctness must be measured separately.

The approximation contract needs a defined function, input range, maximum or distributional error, precision, saturation behavior, exceptional values and hardware cost. The captured description names approximate nonlinear activations but does not expose that contract.

### What preemptive memory bypass means

Accelerators normally place data into a buffer or memory level before a later unit reads it. A memory bypass forwards a value directly around one level when storing and rereading it would add latency, traffic or energy. “Preemptive” suggests that the system decides before the normal access occurs, based on predicted reuse, urgency, dependency or data class.

The bypass is not free routing. It needs a trigger, a path, arbitration, buffering, ordering and a fallback when the bypass path is busy. The system must know whether a value has been stored, forwarded, invalidated or consumed. Neural streams may tolerate some buffering flexibility; symbolic state and control dependencies may require precise ordering. A bypass that improves one stream can contend with another or starve normal memory traffic.

### What a unified architecture must define

Combining neural and symbolic units requires an explicit interface:

1. how numerical tensors become symbolic values or predicates;
2. how symbolic state and control return to neural execution;
3. which values use approximate precision and which require exact representation;
4. how dependencies and memory ordering are enforced; and
5. how errors, exceptions and unsupported operations are handled.

The hardware must also decide which work is assigned to the neural path, which to the symbolic path, and how data moves between them. A unified physical design may reduce transfers and duplicate buffers, but it can add control complexity, shared-resource contention and isolation requirements.

### Why separate efficiency and correctness measurements are necessary

The separate-neural and symbolic-accelerator baseline answers whether integration reduces movement or control overhead. The exact-nonlinear baseline answers what quality or correctness is lost when the activation is approximated. These are different comparisons.

Evaluation should report neural task accuracy, symbolic exactness or decision agreement, end-to-end application output, activation approximation error, memory traffic, bypass hit/use rate, stalls, latency, energy and area. It should cover applications where symbolic decisions are frequent, approximate outputs are near thresholds, and neural and symbolic phases contend for memory. A single average accuracy result can hide a rare but critical symbolic failure.

### What the record establishes and where it stops

The official description establishes Overmind NSA as a unified neuro-symbolic architecture combining approximate nonlinear activations and preemptive memory bypass. It qualitatively claims neuro-symbolic efficiency and names separate neural/symbolic accelerators and exact nonlinear execution as comparison categories. It does not report task accuracy, symbolic correctness, approximation error, latency, energy, area, memory traffic or application coverage.

The [Overmind NSA](../observed-subthemes/specialized-accelerators-and-dataflow.md#paper-dac-2026-research2125) record is evidence of a unified neuro-symbolic architecture direction, not proof of preserved symbolic behavior or better system performance. The explanation separates neural approximation from symbolic exactness, bypass intent from memory consistency, physical integration from useful dataflow, and qualitative efficiency from application-diverse validation.

<span id="explanation-dac-2026-research200"></span>

## Ternainfer: 1.58 bits describes an ideal ternary code, not automatically a 1.58-bit GPU computation

### What ternary weights are

A ternary weight can take three values, commonly a negative value, zero, or a positive value. A group scale can give those symbols a useful numerical magnitude. This differs from ordinary 8-bit or 4-bit quantization, which uses more representable levels and usually stores a fixed-width code for each weight.

Three equally represented states contain (log_2(3)), approximately 1.585, bits of information per weight in an ideal variable-length or entropy-balanced representation. The phrase “1.58-bit” describes this average information content. A real model also stores group scales, code alignment, headers, padding and possibly metadata. Its physical bits per weight can therefore be higher than 1.58.

### What ternary arithmetic requires

For a matrix product, multiplying an activation by a ternary weight can be simplified: a positive symbol selects a scaled activation, a negative symbol selects its negation, and zero skips the contribution. This can reduce multiplier complexity. The GPU still needs to read packed codes, identify symbols, apply scales, handle zero positions and accumulate results.

Packed ternary codes do not necessarily align with the GPU's native word, SIMD lane or tensor-core tile. A kernel may need bit extraction, lookup, unpacking, sign handling and data rearrangement before the arithmetic unit can consume the values. If scales are stored per group, they require separate loads and broadcast operations. The cost of this decode path belongs in the inference measurement.

Activation and accumulation precision also matter. Low-bit weights can be multiplied by higher-precision activations and accumulated into a wider result. The output may then be converted for the next layer. The weight bit count alone does not define the arithmetic precision, bandwidth or energy of the layer.

### Why model quality is a separate problem

Replacing a floating-point or higher-bit weight with one of three symbols changes the model function. A model may be trained with ternary weights from the beginning, retrained with a quantization-aware objective, or converted after training. These processes have different quality and cost implications.

Quality must be measured with the same model architecture, training or calibration budget, evaluation data, tokenizer, sequence length, generation settings and activation/KV-cache precision. Perplexity does not fully describe instruction-following, reasoning, code or safety behavior. A compression result without task-level evaluation cannot establish useful LLM inference.

### What a GPU inference stack must provide

The stack must define the storage layout, packing rule, scale granularity, decode instructions, kernel tiling, accumulation precision and supported GPU. It must decide whether ternary decoding happens in registers, shared memory, a tensor-core path, a lookup table or a custom unit. The compiler or runtime must launch kernels that handle each layer's dimensions and boundary tiles.

The end-to-end path includes weight loading, code unpacking, scale loading, matrix computation, accumulation, output conversion and movement to the next layer. For autoregressive generation it also includes KV-cache reads and writes, sampling and per-token scheduling. A smaller weight file can reduce storage traffic while leaving activation or KV-cache traffic dominant.

### What a complete comparison must report

The 8-bit/4-bit GPU and dense floating-point baselines must use the same model and quality target. The comparison should state physical bits per weight including scales and padding, weight and activation precision, KV-cache precision, GPU model, kernel implementation, batch, prompt/generation lengths, throughput, time to first token, per-token latency, memory use, energy and quality.

Compression ratio is not arithmetic speedup. A packed representation may save memory but require more decoding. A custom kernel may be fast at one matrix shape and inefficient at another. A best-case layer or model does not establish broad GPU benefit without model-diverse and shape-diverse results.

### What the record establishes and where it stops

The official description establishes Ternainfer as a GPU inference-stack direction for ternary approximately 1.58-bit LLM weights, with custom low-bit arithmetic and packing. It qualitatively claims compression and inference efficiency and names 8-bit/4-bit GPU and dense floating-point inference as comparison categories. It does not report model, encoding, physical bits per weight, perplexity, task accuracy, throughput, energy, memory, GPU or kernel results.

The [Ternainfer](../observed-subthemes/specialized-accelerators-and-dataflow.md#paper-dac-2026-research200) record is evidence of ternary LLM inference work, not proof of 1.58-bit physical storage, quality preservation or faster GPU serving. The explanation separates information content from packed storage, weight precision from activation/KV precision, code compression from decode cost, and arithmetic reduction from complete inference performance.

<span id="explanation-dac-2026-research1438"></span>

## PiHG: removing redundant graph work is valid only when typed aggregation semantics are preserved

### What a heterogeneous GNN computes

A graph neural network updates each node using its own features and messages from neighboring nodes. A heterogeneous graph has more than one node or edge type. The message sent along one relation may use different weights, normalization or transformation from a message sent along another relation.

A typical layer therefore performs several steps: identify the neighbors of a destination node, read their features and relation labels, transform the features according to relation semantics, aggregate the messages, and apply an output transformation or activation. The graph structure is irregular, so the neighbors are not laid out like a dense matrix and different nodes can have very different degrees.

### What redundant aggregation can mean

Redundancy can occur when the same feature, transformed message or partial aggregation is read or computed repeatedly for multiple destinations, relations or paths. Reusing an intermediate can reduce arithmetic and memory traffic, but only if the reused value represents exactly the same mathematical quantity.

For two computations to be merged, they must agree on the source features, relation type, learned weights, normalization factor, destination context and update time. Similar graph structure is not enough. A message transformed for one relation cannot be reused for another relation if their parameters differ. A partial sum cannot be shared if the participating neighbors or normalization differ.

### What a pivot-centric approach changes

PiHG describes a pivot-centric approach. A pivot can be a shared node, feature, relation, intermediate message or other graph object around which related computations are organized. The hardware can load or transform the pivot once and reuse it across compatible edges or destinations.

The pivot choice must be accompanied by a relation-aware schedule. The system must track which destinations consume the pivot, which transformation applies, where each partial result is stored, and when the result is complete. The pivot is a reuse point, not permission to collapse distinct typed computations.

The execution sequence includes:

1. locating the pivot and its graph metadata;
2. loading the pivot feature or intermediate;
3. identifying compatible edges, relations and destinations;
4. applying the correct typed transformations;
5. accumulating messages with the required normalization; and
6. writing updated node features while preserving dependencies.

Any mismatch in relation labels, edge direction, degree normalization or update ordering can change the GNN function even if the accelerator uses fewer operations.

### Why irregular memory can dominate

Graph features, adjacency lists, edge types and relation parameters are often stored in different structures. A destination may read neighbors from scattered locations, while a high-degree node may require a long reduction. Processing elements can become idle when graph degree and relation counts vary. Shared features can reduce traffic in one region but create a hot memory location or reduction conflict in another.

The hardware boundary must include address generation, graph metadata reads, feature movement, relation selection, local buffering, interconnect contention, synchronization, partial-sum storage and output writes. A redundancy-free arithmetic count does not establish lower latency or energy if the graph memory path remains the bottleneck.

### What a complete comparison must prove

The comparison must use the same graph, relation semantics, model weights, feature dimension, precision and accuracy target. It should test graphs with different node/edge types, degree distributions, sizes, relation imbalance and feature reuse. The redundant-aggregation baseline must be defined mathematically, not only by a name, and the output of PiHG must be checked against a reference implementation.

Measurements should include layer and full-model latency, throughput, energy, memory traffic, buffer use, processing-element utilization, reduction stalls and preprocessing. A graph-specific best case does not establish broad heterogeneous-GNN efficiency. Accuracy or exact output agreement is required when the method removes or combines operations.

### What the record establishes and where it stops

The official description establishes PiHG as a pivot-centric heterogeneous GNN accelerator intended to remove redundant aggregation. It qualitatively claims GNN efficiency and names a general-purpose GNN accelerator and redundant heterogeneous aggregation as comparison categories. It does not report speedup, energy, accuracy, memory, graph scale, datasets, relation semantics or hardware conditions.

The [PiHG](../observed-subthemes/specialized-accelerators-and-dataflow.md#paper-dac-2026-research1438) record is evidence of a graph-reuse accelerator direction, not proof of semantically equivalent or faster heterogeneous-GNN execution. The explanation separates typed message semantics from structural reuse, arithmetic reduction from memory reduction, pivot selection from correctness, and kernel efficiency from dataset-diverse end-to-end performance.

<span id="explanation-dac-2026-research2504"></span>

## EASY-ZKP: an end-to-end FPGA claim must include every proof stage and every host/device transfer

### What a zero-knowledge prover has to compute

A zero-knowledge proof lets a prover demonstrate that a computation satisfies a specified relation without revealing private inputs. The prover receives a circuit or constraint system, public inputs and a private witness, then produces a proof that a verifier can check. The proof is valid only when the witness satisfies the circuit and every transformation preserves the required algebra.

The proving pipeline depends on the proof system, but it commonly includes witness or trace processing, polynomial construction, finite-field arithmetic, transforms, commitments, group operations, hashing, proof assembly and output serialization. Some systems also need large intermediate vectors or multiple passes over them. An FPGA can accelerate a selected kernel or a complete pipeline, but those are different claims.

### Why arithmetic and memory are coupled

Finite-field elements are represented using fixed-width integers modulo a field modulus. Addition, multiplication and reduction produce exact field results, but each operation needs data from somewhere and may produce an intermediate that must be stored for later stages. Polynomial and commitment operations can create arrays much larger than the FPGA's local memory.

The hardware path therefore includes arithmetic units, local buffers, external memory, address generation, permutation or reordering, DMA, interconnect and synchronization. A design with enough multipliers can still stall when data cannot be supplied or when the next stage needs a different layout. Memory bandwidth and capacity are part of proof-generation throughput.

### What “end-to-end FPGA acceleration” should mean

An end-to-end system must state the boundary between the host and FPGA. The host may parse the circuit, prepare the witness, allocate buffers, launch kernels, handle unsupported operations, coordinate stages and assemble the final proof. The FPGA may execute arithmetic, transforms, hashing, memory movement or a subset of these tasks.

The complete path includes:

1. circuit and witness preparation;
2. transfer of inputs and parameters to the FPGA;
3. execution of the accelerated proof stages;
4. intermediate storage, reordering and transfers between stages;
5. return of results to the host or the next FPGA stage; and
6. proof assembly, output and any required verification preparation.

If transfers overlap arithmetic, the overlap schedule and buffer requirements must be measured. If they do not, transfer time must be included. Bitstream loading, initialization, memory allocation and host control may be amortized for a batch or may matter for a single proof. The word “end-to-end” has no fixed meaning without this boundary.

### Why the proving system and circuit define the result

Different proof systems use different fields, curves, polynomial degrees, commitment schemes and arithmetic kernels. Circuit size and witness size change the number and size of intermediate values. A proof result for one curve and circuit cannot be transferred to another without preserving the same security level and proving semantics.

The evaluation must state the proving system, curve/field, circuit, public/private input sizes, witness generation method, proof size, correctness check, FPGA device, clock, external memory and software version. CPU/GPU and partial-FPGA baselines must include the same proof stages, or the excluded stages must be named. A kernel speedup with the proof assembly and host transfers omitted is not a proof-generation speedup.

### What correctness and reproducibility require

Finite-field arithmetic must be bit-accurate, including reduction, overflow handling and representation conversion. The accelerator must produce the same valid proof as the reference or a proof accepted by the intended verifier. Intermediate comparisons should cover boundary values, large circuits, memory spills, repeated passes and all supported proof phases.

Reproduction requires the FPGA bitstream or source, synthesis constraints, device and clock, memory configuration, host software, input circuits, witness generation and timing boundary. Resource and energy results need an inclusion rule for FPGA fabric, external memory, host, configuration and data movement. The captured description contains none of these conditions.

### What the record establishes and where it stops

The official description establishes EASY-ZKP as an end-to-end FPGA-acceleration direction for zero-knowledge proofs, involving finite-field arithmetic and a memory hierarchy. It qualitatively claims proof-generation efficiency and names CPU/GPU proving and partial FPGA acceleration as comparison categories. It does not report proof latency, throughput, energy, area, memory, circuit coverage, proof system, curve, FPGA or host boundary.

The [EASY-ZKP](../observed-subthemes/specialized-accelerators-and-dataflow.md#paper-dac-2026-research2504) record is evidence of a proposed proof-system accelerator, not proof of faster or reproducible end-to-end proving. The explanation separates field arithmetic from the complete prover, FPGA kernels from host/device work, trace or polynomial movement from compute, and qualitative system intent from measured proof results.

<span id="explanation-dac-2026-research1447"></span>

## STCG: adaptive sparse tiling must keep tensor-core lanes, metadata, and reductions productive together

### Why tensor cores expose a sparse-tensor problem

A tensor core is a fixed-function or tightly specialized unit that performs a small matrix operation on a regular tile. Its high throughput comes from feeding many lanes with values in a predictable layout. A dense matrix multiplication can divide the iteration space into tiles that match this shape.

A sparse tensor stores only some values, commonly because other values are zero or deliberately pruned. The nonzero positions are represented by metadata. A sparse tile may contain a different number of nonzeros from its neighbors, and the positions may not line up with the tile shape expected by the tensor core.

The system has three choices: execute a dense tile and mask or skip some results, pack nonzeros into a supported dense-like tile, or use a sparse kernel that traverses values and metadata directly. Each choice trades arithmetic work against packing, index processing, memory movement, lane utilization and output reduction.

### What adaptive tile scheduling decides

Tile scheduling assigns sparse work to GPU warps, thread blocks or other execution units and chooses the order in which tiles are processed. An adaptive scheduler can use nonzero counts, estimated memory traffic or observed work to avoid assigning a heavy tile to one unit while another becomes idle.

The schedule must also preserve output ownership and reductions. Two sparse tiles may contribute to the same output region. If they are assigned to different warps, their partial results need an accumulation path, synchronization or an atomic operation. A schedule that balances input work but creates output conflicts can lose the benefit through reduction overhead.

The generated kernel must handle:

1. loading values and their indices;
2. unpacking or translating the sparse tile;
3. feeding operands into the tensor-core tile shape;
4. preserving the mapping from packed values to output coordinates;
5. combining partial outputs; and
6. writing results with the required precision.

Adaptive scheduling can change the assignment or order, but it cannot remove these semantic requirements.

### Why metadata and packing matter

Sparse storage needs indices, offsets, masks or block descriptors. Those fields consume bytes and memory transactions. Packing irregular nonzeros into a regular tensor-core tile may require a preprocessing kernel, shared-memory staging, register shuffles or a format conversion. If the density is high, the metadata and packing work can approach or exceed the cost of dense execution.

The format determines what can be known before the kernel starts. A regular block-sparse format can map blocks predictably. Unstructured sparsity may require variable-length traversal and dynamic work distribution. A format that gives high compression may make address generation and tensor-core feeding harder. The captured description does not identify the supported formats, so its efficiency claim cannot be generalized across sparse representations.

### Why occupancy is not just lane utilization

GPU occupancy depends on how many warps or blocks can reside on a streaming multiprocessor given registers, shared memory, block size and hardware limits. A tile schedule that improves nonzero balance may use more registers for metadata or more shared memory for packing, reducing the number of resident warps. A schedule that keeps tensor-core lanes busy can still be memory-bound or synchronization-bound.

The relevant performance path includes global memory reads, metadata reads, conversion, tensor-core issue, synchronization, reductions, cache behavior and output writes. Tensor-core instruction throughput is only one part. Runtime adaptation also has a cost: the scheduler must inspect work, maintain queues or select among kernels, and that control can add launch or per-tile overhead.

### What a complete evaluation must compare

The dense tensor-core and static sparse-tiling baselines must use the same GPU, precision, tensor dimensions, output correctness, sparse format and data distribution. The evaluation should report density and shape distributions, generated code, compilation time, kernel-launch and adaptation overhead, occupancy, memory traffic, tensor-core utilization, latency, energy and end-to-end model impact.

Sparse performance is often non-monotonic with density. Very low density can reduce arithmetic but increase metadata and irregularity; moderate density can be especially difficult to pack; structured blocks may behave differently from unstructured values. One best-case sparsity point cannot establish broad sparse-GPU performance.

### What the record establishes and where it stops

The official description establishes STCG as an adaptive tile-scheduling code-generation direction for sparse tensor kernels on tensor-core GPUs. It qualitatively claims sparse-kernel efficiency and names dense tensor-core kernels and static sparse tiling as comparison categories. It does not report speedup, occupancy, sparsity range, compile time, runtime overhead, energy, GPU, format, precision or correctness results.

The [STCG](../observed-subthemes/specialized-accelerators-and-dataflow.md#paper-dac-2026-research1447) record is evidence of an adaptive sparse-kernel compiler proposal, not proof of faster tensor-core execution across sparse workloads. The explanation separates skipped arithmetic from metadata work, tile balance from occupancy, generated code from runtime behavior, and kernel efficiency from complete model performance.

<span id="explanation-dac-2026-research1338"></span>

## ZK-Tracer: trace generation is a correctness-critical producer, not the whole zero-knowledge prover

### What a zero-knowledge VM trace represents

A zero-knowledge virtual machine executes a program while allowing a prover to show that the execution followed the VM rules without revealing private inputs. The execution can be represented as a trace: a sequence of states, instruction effects, memory events or other records that later proving stages constrain and check.

The trace is not an optional debug log. It must contain the information required to connect one valid VM state to the next. A missing field, incorrect ordering, inconsistent memory event or wrong arithmetic result can produce an invalid proof or an incorrect claim about the program. The exact trace contents depend on the VM and proving system, which the captured description does not specify.

### Why trace generation can become a bottleneck

Trace generation runs the VM semantics and writes the resulting records. The work can include instruction decode, arithmetic, control flow, memory address checks, witness handling, range checks, packing and synchronization. The producer may generate a large amount of data even when the final proof is compact.

The trace then has to be stored and consumed. It may be written to on-chip buffers, external memory or a distributed memory system. Later stages may read it to construct constraints, polynomials, commitments or proof-specific representations. If the producer writes faster than the consumer can read, buffers fill and the system stalls. If it writes slowly, a proof accelerator waits. Trace bandwidth and storage are therefore part of proving performance.

### What a heterogeneous accelerator changes

The record describes a heterogeneous architecture for zero-knowledge VM trace generation, with CPU/FPGA/ASIC-like components and substantial memory movement. Different components can handle different classes of work: control-heavy interpretation may remain on a CPU-like unit, regular arithmetic may use fixed hardware, and trace packing or movement may use dedicated paths.

The partition is useful only if the boundaries preserve the VM state and trace order. A component receiving a block of work needs the required registers, memory state, instruction context and witness data. Its results must return with the correct sequence position. Synchronization, queues, cache coherence or explicit data movement can consume the benefit of the specialized arithmetic.

The execution path includes:

1. fetching and decoding the VM instruction;
2. reading the relevant architectural and memory state;
3. applying the VM operation and checking its semantics;
4. producing the required trace record;
5. packing and moving the record; and
6. making it available to the next proving stage.

An accelerator that measures only step 3 or only trace-record creation does not establish the throughput of this complete path.

### Why trace throughput is not proof throughput

The proof system determines what the trace must contain and how it is transformed. A trace generator may be fast for one VM program distribution but create an output layout that is expensive for the downstream prover. Conversely, a generator that emits a wider or more redundant trace may simplify later checks while increasing memory traffic.

The relevant denominator must include the entire proof workflow: program execution, trace generation, trace storage and movement, constraint or polynomial construction, commitments, proof computation, verification setup and output serialization, according to the chosen proving system. A CPU baseline and a homogeneous ZK accelerator must use the same VM semantics, program, witness, trace format, proof target and correctness check.

Program behavior matters. Branches, memory access patterns, instruction mix, witness size and trace density change the amount of work and movement. A result from a regular arithmetic-heavy program may not apply to programs with irregular memory or control behavior.

### What correctness and security require

Functional trace generation must be checked against a reference VM for every relevant instruction, memory rule, exception and boundary condition. Matching a trace hash or aggregate is not enough if the representation can hide an ordering or field error. The proof must also be accepted by the intended verifier for the intended public and private inputs.

Security is a separate property. A fast trace generator does not establish zero-knowledge, soundness, resistance to side channels or correct witness handling. The partition must not expose private data through timing, memory traffic or debug interfaces, and faults in one component must not silently alter a proof-relevant trace.

### What the record establishes and where it stops

The official description establishes ZK-Tracer as a heterogeneous accelerator direction for zero-knowledge VM trace generation. It qualitatively claims trace-generation throughput and efficiency and compares the direction with CPU generation and a homogeneous ZK accelerator. It does not report trace rate, proof latency, energy, area, memory use, program coverage, VM, trace format or proving system.

The [ZK-Tracer](../observed-subthemes/specialized-accelerators-and-dataflow.md#paper-dac-2026-research1338) record is evidence of a trace-generation accelerator proposal, not proof of faster or secure end-to-end proving. The explanation separates VM execution from trace production, trace throughput from proof throughput, heterogeneous specialization from state-transfer cost, and functional trace agreement from cryptographic validation.

<span id="explanation-dac-2026-research121"></span>

## Exquant: expert usage can guide precision allocation, but usage frequency is not the same as quantization sensitivity

### What an MoE layer is doing

A mixture-of-experts (MoE) layer contains several expert networks and a router. For each token, the router scores the experts and selects a small number, often called top-k. The selected experts process the token, and their outputs are combined. The layer can therefore contain many parameters while using only part of them for each token.

This conditional execution creates two different resource problems. The model stores weights for all experts, even when only some are active. The runtime must route tokens, move them to the selected experts, execute different expert workloads, combine outputs and handle uneven expert demand. Quantization can reduce the stored weight size and arithmetic cost, but the serving system still pays for routing, movement, dequantization or mixed-precision kernels.

### What quantization changes

Quantization maps a higher-precision value to a smaller representation. A scale, zero point or related rule maps the stored integer-like code back to an approximate real value. Fewer bits reduce storage and may allow more operations per cycle, but the mapping introduces error. The error depends on the value distribution, outliers, layer sensitivity, accumulation precision and whether weights or activations are quantized.

Mixed precision assigns different bit widths to different model components. A sensitive component may retain more bits while a less sensitive component uses fewer. The allocation has a budget: reducing one component's precision may permit another to retain more precision, but the total storage, bandwidth, kernel support and conversion cost must be counted.

### What global expert ranking means

Exquant uses a global expert ranking to guide this allocation. A ranking can be based on how often experts are selected, how much traffic they receive, or another importance statistic. If the ranking measures global usage, the method can give more precision or protection to experts that serve many tokens and compress less-used experts more aggressively.

Usage and sensitivity are not identical. A frequently selected expert may be numerically tolerant, while a rarely selected expert may be essential for a particular domain or rare token. A ranking based on one calibration distribution can also hide layer-specific behavior. The method therefore needs a precise ranking definition, calibration data, granularity, bit-width menu and rule that maps rank to precision.

### Why routing and quantization interact

Quantization changes expert outputs. The router may use a separate representation or may depend on activations affected by quantization. A small error can change the top-k selection near a routing boundary. That sends the token to a different expert, changing both the computation and the error path. The evaluation must state whether routing is held fixed, quantized, recalculated, or measured for disagreement.

Expert load also changes the hardware cost. A popular expert may receive more tokens and become a communication or compute hotspot. Assigning it a wider precision can increase its memory traffic and execution time precisely where demand is highest. A ranking that improves quality may therefore worsen tail latency or load imbalance unless the serving kernels and routing system support the assigned precisions efficiently.

### What a valid quality comparison requires

The calibration distribution used to rank experts must be separated from the evaluation distribution. Results should cover different prompt domains, sequence lengths, token frequencies, routing distributions and generation phases. Perplexity and task accuracy measure different effects; a model-level average can hide degradation in a rare but important expert or task.

The comparison must state the model, number of experts, top-k, bit widths, weight/activation scope, calibration size, scale calculation, accumulation precision, baseline bit budget and quality metric. It should compare uniform quantization and expert-oblivious mixed precision under the same total memory or bit budget. A quality result without this denominator does not establish that expert ranking caused the improvement.

### What a valid efficiency comparison requires

Compression ratio is not serving latency. A mixed-precision model may need separate kernels for each bit width, conversion between representations, extra scale loads and irregular expert scheduling. If the hardware executes all experts at one native precision, lower-bit weights may save memory but not arithmetic time. If the router sends tokens across devices, communication and queueing can dominate the expert computation.

The complete measurement should include weight storage, scale metadata, activation storage, dequantization, arithmetic, routing, expert dispatch/combine, memory traffic, kernel launches, batch/concurrency, time to first token, per-token latency, tail latency, throughput and energy. The ranking computation and refresh policy also matter if routing distributions change over time.

### What the record establishes and where it stops

The official description establishes Exquant as a global expert-ranking-guided mixed-precision quantization approach for MoE inference. It qualitatively claims efficiency and quality retention and names uniform and expert-oblivious mixed precision as comparison categories. It does not report model, bit widths, ranking statistic, calibration traces, perplexity, accuracy, latency, energy, memory or kernel results.

The [Exquant](../observed-subthemes/specialized-accelerators-and-dataflow.md#paper-dac-2026-research121) record is evidence of an expert-aware quantization direction, not proof of robust quality or faster MoE serving. The explanation separates expert frequency from sensitivity, model compression from runtime cost, routing behavior from weight precision, and calibration results from workload-diverse deployment.

<span id="explanation-dac-2026-research1942"></span>

## PD-Swap: prefill and decode need different hardware, but swapping hardware is itself part of inference

### What changes between prefill and decode

An autoregressive language model processes a prompt before it generates new tokens. The prompt-processing phase is called prefill. It can process many prompt positions in parallel and builds the key-value (KV) cache for the model's attention layers. The generation phase is called decode. It usually produces one next token at a time, reads the existing KV cache, appends the new key and value, and repeats.

The two phases execute related model layers but have different shapes and bottlenecks. Prefill can expose large matrix-operation batches and may benefit from many active arithmetic units and high throughput. Decode has a small amount of new query work per step but repeatedly accesses a growing KV cache; it may be constrained by memory bandwidth, cache capacity, data movement or per-token latency. A datapath sized for one phase can be underused in the other.

### What dynamic partial reconfiguration does

An FPGA contains programmable logic, routing and memory resources. Dynamic partial reconfiguration changes a selected region by loading a partial bitstream while the rest of the device remains configured. PD-Swap uses that capability to replace a prefill-specific region with a decode-specific region, or the reverse.

The reconfigurable region must have a defined interface to the static region. The system needs to stop or isolate traffic, load the correct configuration, restore or preserve the required state, reconnect the interfaces, and resume the model. Weights, control state, KV-cache contents and token position cannot be lost merely because the arithmetic datapath changes. If state is copied to or from external memory, that transfer is part of the transition.

The useful abstraction is therefore not “prefill hardware plus decode hardware.” It is a state machine with at least these costs:

1. detect a phase transition;
2. quiesce or drain the current pipeline;
3. move and validate the partial bitstream;
4. preserve model and KV-cache state;
5. initialize the replacement datapath; and
6. resume execution with the correct token and cache position.

Every step can affect latency, energy and correctness. The static logic, configuration memory, reconfiguration controller and interface buffering remain present even when the specialized region is swapped.

### Why phase specialization can help

If a request has a long prefill and a long generation, a specialized region may improve resource utilization in each phase. The prefill configuration can allocate more parallel matrix resources, while the decode configuration can allocate more memory paths, cache handling or low-latency control. Reusing the same physical area across phases can provide capabilities that would not fit simultaneously in a small FPGA.

That benefit is workload-dependent. Prompt length, generated length, batch size, concurrent requests, request arrival pattern and scheduling policy determine how often the system crosses between phases. If requests are interleaved, swapping one request's phase can disrupt another's progress. If sequences are short, the transition cost can be comparable to the work saved. If multiple users require prefill and decode at the same time, one reconfigurable region may create queueing that a static design avoids.

### What an end-to-end comparison must include

End-to-end inference includes prompt ingestion, model execution, KV-cache allocation and movement, token sampling, host/device coordination, phase transitions and output delivery. A phase-specific kernel measurement cannot establish end-to-end token latency or throughput.

A fair evaluation must report prompt and generation lengths, batch and concurrency, model and precision, KV-cache size, FPGA family and clock, static/reconfigurable partition, partial-bitstream size, configuration time, state-transfer time, overlap assumptions and quality. It should separate time to first token, prefill latency, per-token decode latency, total request latency, throughput and tail latency. Energy must include configuration and memory traffic, not only arithmetic.

The static FPGA and single shared datapath baselines must use the same model, quality, memory capacity, clock and request workload. A static design may consume more area but avoid transitions; a shared design may avoid bitstream movement but have lower utilization. The relevant result is the complete workload tradeoff, not the peak rate of either specialized region.

### What the record establishes and where it stops

The official description establishes PD-Swap as a dynamic partial-reconfiguration proposal that swaps phase-specific prefill and decode logic for end-to-end LLM inference on edge FPGAs. It qualitatively claims improved inference efficiency. It does not report reconfiguration time, bitstream size, state-transfer cost, latency, throughput, energy, area, utilization, model, sequence lengths or accuracy.

The [PD-Swap](../observed-subthemes/specialized-accelerators-and-dataflow.md#paper-dac-2026-research1942) record is evidence of phase-aware FPGA specialization, not proof of better end-to-end inference. The explanation separates prefill from decode, phase specialization from transition overhead, reconfigurable logic from preserved model state, and kernel efficiency from complete request-level performance.

<span id="explanation-dac-2026-research1374"></span>

## SpArC: sparse compilation must schedule values, metadata, and reductions together

### What sparsity changes in a tensor computation

A dense tensor computation assumes that values occupy a regular coordinate grid. The hardware can generate addresses from loop indices and execute a predictable sequence of multiply-adds. A sparse tensor omits some values, commonly zeros, and stores the remaining values in a compressed representation.

The arithmetic count may decrease, but the computation becomes less regular. The system must know which coordinates are present, find matching values across tensors, generate addresses, handle rows or tiles with different numbers of nonzeros, and combine partial results. The metadata that describes positions is part of the workload. A sparse compiler is successful only when the work avoided is greater than the metadata, control, movement and imbalance introduced.

### What scheduling and mapping mean

Scheduling assigns operations to time and order. It decides when a nonzero product is created, when a reduction occurs, and when a dependent operation may consume a result. Mapping assigns those operations, values, metadata and partial sums to processing elements, local buffers, shared memory and links.

These choices are coupled by dependencies but need not be identical. A compiler may schedule nonzero work in a compressed order while mapping tiles to a regular processing-element array. It may place a frequently reused tensor in local storage while streaming another tensor. It must still ensure that coordinates match, data arrives before use, and partial sums are combined with the required semantics.

### Why sparse formats determine the hardware work

Different sparse formats expose different information. A coordinate list stores explicit positions and values. A compressed row or tile format stores pointers, indices and grouped values. Structured formats constrain nonzeros to blocks or patterns. Each format changes metadata size, address generation, possible vectorization, load balance and supported operations.

The format also determines what the compiler can know statically. A regular block pattern can be mapped predictably. Unstructured nonzeros may require runtime traversal or dynamic work assignment. A format that reduces metadata may also reduce the compiler's ability to identify reuse. The captured description does not specify which format SpArC supports, so its claimed scope cannot be generalized across sparse representations.

### Why load balance and reductions are central

Sparse rows, tiles or output channels can contain very different nonzero counts. If work is assigned statically, a processing element handling a dense region may run while another becomes idle. If work is redistributed dynamically, the system adds queues, control, metadata movement and synchronization.

Reductions create another constraint. Several sparse products may contribute to one output, and their completion times can differ. The compiler must choose where partial sums live, when they are combined, and how conflicts are avoided. Reordering additions can change floating-point results. A schedule that reduces arithmetic but increases partial-sum traffic may be slower or less accurate.

### What a sparse accelerator compiler must model

A useful cost model needs more than the number of nonzero multiplications. It should account for:

- value and metadata bytes moved at each memory level;
- address generation, decompression and format conversion;
- processing-element utilization and load imbalance;
- local-buffer capacity and tile boundary effects;
- interconnect contention and synchronization;
- partial-sum storage, conflicts and reduction ordering; and
- compiler search time and any runtime scheduling overhead.

The generated mapping must also obey the target accelerator's supported operations, topology, memory ports, bandwidth and precision. A mapping legal on one programmable dataflow is not automatically legal on another. A compiler can produce a mathematically correct schedule that is still slower than dense execution when density is high or metadata dominates.

### Why a qualitative compilation claim is not an accelerator result

The official description qualitatively claims sparse compilation and mapping efficiency. It reports no speedup, energy, compile time, sparsity coverage, hardware topology, supported formats, precision or end-to-end model result. That evidence establishes a compiler direction and a claimed mapping capability, not a measured accelerator advantage.

A meaningful evaluation must compare the same sparse tensors, format, density distribution, precision and correctness target on the same hardware. It should report compiler time, generated schedule, runtime including metadata and movement, energy, memory use, processing-element utilization and sensitivity to density and imbalance. It should include dense mapping and existing sparse compilers under the same target assumptions.

### What the record establishes and where it stops

The official description establishes SpArC as a compiler framework for sparse-tensor scheduling and accelerator mapping on programmable dataflow and hierarchical-memory hardware. It identifies sparse irregularity, scheduling and mapping as the problem boundary. It does not establish a numerical speedup, energy result, compile cost, sparsity range, format coverage, hardware target or end-to-end model result.

The [SpArC](../observed-subthemes/specialized-accelerators-and-dataflow.md#paper-dac-2026-research1374) record is evidence of a sparse compiler proposal, not proof of faster sparse execution. The explanation separates arithmetic omission from metadata work, scheduling from mapping, legal schedules from fast schedules, and compiler expressiveness from measured accelerator performance.

<span id="explanation-dac-2026-research1837"></span>

## Factored-FPMAC: deferring floating-point normalization moves work out of the MAC, but does not remove its numerical obligations

### What a floating-point MAC normally does

A floating-point value represents a signed magnitude using a sign, an exponent and a significand. The exponent records scale; the significand records precision at that scale. A fused multiply-accumulate (FMA) computes a product and adds it to an accumulated value, ideally with one final rounding for the fused operation.

To add two floating-point values, hardware first aligns their exponents. The significand of the smaller-magnitude value is shifted so both values refer to the same scale. The significands are then added or subtracted. The result may have leading zeros or a carry, so it is normalized by shifting the significand and adjusting the exponent. Finally, the value is rounded to the supported precision. Overflow, underflow, zero, NaN and infinity behavior also belong to the arithmetic definition.

In a long matrix multiplication, an output accumulates many products. A conventional systolic array can repeat alignment, normalization and rounding as partial sums move through the array. Those steps consume logic, switching activity and pipeline time, and every intermediate rounding can change the eventual result.

### What carry-save accumulation changes

Carry propagation is the step that turns several partial bit rows into one ordinary binary number. A carry-save adder postpones that propagation. It keeps a sum row and a carry row, so a new partial product can be combined without immediately sending a carry through the full width.

A 4:2 carry-save adder compresses multiple input rows into fewer output rows while retaining the same mathematical value. This can reduce the depth of the local adder path. It does not make carries disappear. The carry information must eventually be propagated, and the extra rows require storage, routing and a representation that preserves exponent and sign information.

The captured method uses 4:2 CSAs and a redundant floating-point representation inside the systolic array. “Redundant” means the intermediate is allowed to have more than one component or an unresolved form rather than being immediately converted to one normalized IEEE-like value. That representation can let the array keep accumulating without performing the full normalization operation after every product.

### What deferred unified normalization means

The method moves normalization to unified post-processing. Instead of normalizing each intermediate MAC result, the array carries a redundant representation through the accumulation and resolves it later. The potential benefit is that one post-processing path replaces repeated wide carry-propagate and normalization paths.

The move is valid only if the intermediate representation preserves the information needed for the final result. It must provide enough exponent range and significand precision for the largest and smallest terms, define how signs and cancellation work, and prevent unresolved carries from overflowing the available storage. The final stage must handle alignment, carry resolution, normalization, rounding and exceptional cases.

The timing tradeoff is also conditional. Removing work from each systolic step may improve the array's initiation interval or energy, but the unified stage can become a bottleneck if many outputs arrive at once. Its area, pipeline depth, throughput, buffering and clock frequency must be measured together with the array. A shorter local adder path does not prove a shorter complete GEMM.

### Why numerical equivalence must be demonstrated

Deferring rounding changes the accumulation order and the point at which information is discarded. That can improve accuracy by avoiding repeated rounding, or it can change overflow, cancellation and reproducibility if the redundant representation is bounded differently. The result must be compared against a clearly defined reference: IEEE-754 precision, rounding mode, fused or unfused behavior, accumulation order and treatment of exceptional values.

Useful checks include bit-accurate agreement, maximum and distributional error, relative error on cancellation-heavy inputs, overflow/underflow cases, deterministic results across array scheduling, and application-level quality for scientific or ML workloads. A claim of “numerical benefit” without precision, error metric and reference cannot establish either exactness or acceptable approximation.

### What the energy and PPA claim would need to include

The official description qualitatively claims removal of redundant normalization and wide carry-propagate adders, with numerical and energy benefits. A complete energy result must state whether it includes multipliers, carry-save stages, redundant storage, interconnect, final normalization, buffers, clocking and memory traffic. Area and timing must include the post-processing path and any additional state needed by the redundant representation.

The comparison must hold matrix dimensions, accumulation length, precision, array size, clock, process, voltage, mapping, memory traffic and output rate constant. A kernel-level adder reduction can be outweighed by extra storage or a final-stage bottleneck. The captured description provides none of these numerical or implementation conditions.

### What the record establishes and where it stops

The official description establishes a factored floating-point MAC proposal for systolic arrays using 4:2 carry-save accumulation, redundant representation and deferred unified normalization. It claims qualitative removal of repeated normalization and wide carry-propagate adders, together with qualitative numerical and energy benefits. It does not establish precision, error, overflow behavior, latency, area, power, frequency, workload coverage or complete post-processing cost.

The [Factored-FPMAC](../observed-subthemes/specialized-accelerators-and-dataflow.md#paper-dac-2026-research1837) record is evidence of an arithmetic microarchitecture direction, not proof of IEEE-754 equivalence or energy-efficient systolic execution. The explanation separates carry postponement from carry removal, local MAC delay from complete-array throughput, deferred rounding from numerical correctness, and adder reduction from complete PPA measurement.

<span id="explanation-dac-2026-research1409"></span>

## CODA: decoupling computation from data movement expands the mapping space, but a legal mapping is not yet a fast execution

### What a DNN dataflow has to decide

A DNN operator is a loop nest over tensors. A convolution, matrix multiplication or attention suboperation repeatedly reads input values and weights, performs arithmetic, and writes partial or final outputs. The same value may be reused many times. An NPU maps those loops onto processing elements and a hierarchy of memories.

The mapping decides at least four things: which loop dimensions are split across processing elements, which dimensions are processed over time, where each tensor tile is stored, and when data is moved between memory levels. These choices determine whether an operand is reused locally or fetched repeatedly, whether partial sums stay near the arithmetic, and whether the interconnect or memory bandwidth becomes the bottleneck.

A dataflow is therefore not just an order for arithmetic instructions. It is a joint schedule for computation, storage, movement, synchronization and accumulation. Two mappings can perform the same mathematical operator while having very different traffic, buffer occupancy, latency and energy.

### What coupling means

In a computation-data coupled representation, a choice about the computation loop often fixes a corresponding storage or movement choice. For example, the loop dimension used to distribute work may also determine how a tensor is tiled or which processing element owns it. Coupling reduces the number of choices and can simplify a compiler, but it can exclude mappings that fit an actual hierarchy better.

The problem becomes more visible when tensors have different reuse patterns. An input activation may be useful across one dimension, a weight across another, and a partial sum across a reduction dimension. A single shared loop/storage decision can favor one tensor while forcing extra movement for the others. Hierarchical memory makes this a constraint at every level: registers, local buffers, shared on-chip storage and external memory have different capacities and bandwidths.

### What computation-data decoupling changes

CODA represents the computation schedule and the per-tensor storage/movement schedule independently, then uses tensor-wise mapping and a non-uniform loop space. In plain terms, the arithmetic loop choices for one tensor do not automatically force the same placement and movement choices for every tensor.

The decoupling does not remove hardware constraints. The schedules must still agree on when a value is produced, where it is stored, how it reaches a consumer, and how long it remains available. A mapping is legal only if:

1. every required operand arrives before its computation;
2. each tile fits in the selected memory level;
3. movement does not exceed link or memory bandwidth;
4. partial sums are preserved with the required precision and ordering;
5. producer and consumer rates do not create unbounded queues; and
6. synchronization and reuse do not violate the NPU execution model.

Decoupling expands the set of representable schedules. It does not prove that a compiler can find a good schedule, that the schedule is legal for a particular NPU, or that its extra control and movement are affordable.

### What non-uniform loop-space modeling means

Uniform tiling applies a common structure to loop dimensions or tensors. Non-uniform modeling permits different dimensions or tensors to use different tile sizes, placements, partitioning and movement rules. This can represent an operator in which weights fit in one memory level while activations require streaming, or in which partial sums need a different ownership pattern from input tiles.

The additional freedom increases the search space. A mapper needs a cost model for arithmetic utilization, buffer occupancy, traffic, bandwidth contention, synchronization, precision effects and latency. It also needs legality checks for every candidate. If the search budget is fixed, a larger space can make the search slower or make a weak cost model more likely to choose a schedule that looks good analytically but stalls in execution.

### Why mapping expressiveness is not a performance result

The official description qualitatively claims expanded mapping expressiveness. That establishes a representation capability. It does not report latency, energy, area, search time, compile time or benchmark coverage. To establish an accelerator benefit, the same operators and tensor shapes must be compiled to the same NPU or comparable NPUs under equal precision, memory capacity, bandwidth, clock and correctness conditions.

The comparison must include schedule-generation time when that cost matters, and it must measure complete execution: data loading, on-chip movement, arithmetic, partial-sum handling, synchronization, output writeback and any remapping between layers. A kernel-level improvement can disappear when a complete model has changing shapes, boundary tiles, unsupported operators or reconfiguration overhead.

### What the record establishes and where it stops

The official description establishes CODA as a computation-data decoupled dataflow representation for DNN computing on NPUs. It identifies tensor-wise mapping and non-uniform loop-space modeling as the mechanisms that expand mapping choices. It does not establish a numerical latency, energy, area, search-cost or benchmark result, nor does it expose the compiler, legality conditions or generated schedules.

The [CODA](../observed-subthemes/specialized-accelerators-and-dataflow.md#paper-dac-2026-research1409) record is evidence of a broader NPU mapping model, not proof of faster DNN execution. The explanation separates arithmetic scheduling from tensor movement, representable mappings from legal mappings, search-space size from found schedules, and mapping expressiveness from measured system performance.

<span id="explanation-dac-2026-research2824"></span>

## ISA-PM: a reusable elliptic-curve multiplier must preserve both curve mathematics and the processor boundary

### What elliptic-curve point multiplication does

Elliptic-curve cryptography represents a public key or other value as a point on a curve over a finite field. A point-multiplication operation takes a point (P) and a scalar (k), then computes (kP) by repeated point additions and point doublings. The scalar is related to secret key material in many protocols, so the implementation must produce the correct point while controlling timing and other observable behavior.

Point addition combines two curve points. Point doubling combines a point with itself. Each operation is built from finite-field additions, subtractions, multiplications, squarings, inversions or inversion-avoiding formulas, and modular reductions. The cost is therefore determined by the field width, the chosen coordinate representation, the formulas, the reduction circuit and the scalar schedule. “ECPM acceleration” is not one fixed arithmetic operation.

### Why supporting more than one curve form is a hardware problem

The record names Montgomery and short-Weierstrass curves. These are different mathematical curve forms. They use different equation parameters and can use different point-operation formulas. They also have different exceptional cases and implementation choices. A unified accelerator must expose enough control and arithmetic to select the right formula without allowing an invalid combination of parameters or an incorrect identity/infinity case.

Curve flexibility therefore requires more than a parameter register. The design must specify the field-element width, supported modulus representation, point coordinates, scalar width, operation sequencing, reduction behavior, curve-parameter loading, and handling of invalid or exceptional inputs. The captured description names the supported curve families but does not provide those semantics, so the extent of the claimed coverage remains unverified.

### What a unified ISA and microarchitecture change

An ISA extension gives software an instruction-level entry point for a hardware operation. The core must fetch or issue the instruction, provide operands, wait for dependencies, and receive the result. The microarchitecture implements the operation using modular arithmetic and storage. This division matters because an arithmetic unit can be fast while the core interface, operand movement, or software sequencing dominates complete point multiplication.

The source describes three-phase small-bit-width modular computation. A wide field operation can be decomposed into operations on smaller chunks. The phases may represent partial multiplication, accumulation and reduction, but the captured description does not expose their exact equations. In general, decomposition replaces one wide carry/reduction path with several narrower paths plus control and partial-result handling. It can reduce the size of an individual unit and permit a design-space choice between more parallel units and fewer reused units.

The resulting schedule must account for:

1. loading the field operands and curve parameters;
2. producing partial products at the selected small width;
3. propagating or storing partial carries and accumulations;
4. reducing the result into the supported field representation;
5. applying the point-addition or point-doubling formula; and
6. returning the point state to the next scalar step or software.

If the ISA exposes only a modular primitive, its instruction count is not the point-multiplication latency. If it exposes a complete point operation, the design still needs a defined scalar schedule, memory behavior and protection against secret-dependent timing or access patterns.

### Why the area-time product needs a complete comparison boundary

Area-time product multiplies an area measure by a latency measure. It can summarize a tradeoff, but it is meaningful only when both quantities have the same definitions across designs. The area must state whether it includes the ISA interface, control, storage, arithmetic, clocking and unused FPGA resources. The time must state the curve, field, scalar, coordinate representation, frequency, initialization, key/point loading and whether software or memory time is included.

The official description reports up to 8.37x area-time-product improvement on an AMD Virtex-7 FPGA. “Up to” identifies a best reported condition, not the result for every curve. A comparison against a dedicated curve accelerator may favor ISA-PM on reuse and area while favoring the dedicated design on one curve's peak latency. A comparison against a software-only path has a different boundary from a comparison against another FPGA accelerator.

The missing security boundary is equally important. Functional point multiplication does not establish resistance to timing leakage, power analysis, fault attacks, invalid-curve inputs or secret-dependent memory behavior. A flexible curve interface may increase the number of control paths that require review. The captured description reports no constant-time analysis, side-channel evaluation or invalid-input handling.

### What the record establishes and where it stops

The official description establishes a unified ISA and microarchitecture proposal for ECPM across Montgomery and short-Weierstrass curves, using three-phase small-bit-width modular computation and resource-parallelism exploration. It reports an up-to 8.37x area-time-product improvement on AMD Virtex-7. It does not establish absolute area, latency, frequency, energy, curve-by-curve coverage, software overhead, timing closure or cryptographic security.

The [ISA-PM](../observed-subthemes/specialized-accelerators-and-dataflow.md#paper-dac-2026-research2824) record is evidence of a reusable elliptic-curve hardware interface, not proof of a secure and uniformly faster multi-curve IoT implementation. The explanation separates curve mathematics from ISA semantics, modular primitives from complete point multiplication, FPGA area-time from energy and software cost, and functional arithmetic from side-channel validation.

<span id="explanation-dac-2026-research983"></span>

## ATTINA: an NTT accelerator improves zkSNARK proving only if its field arithmetic and data movement fit the complete proof

### What a zkSNARK prover is doing

A zkSNARK lets a prover convince a verifier that a computation was performed correctly without exposing the computation's private inputs. The prover takes a circuit or constraint system, public inputs and a private witness, then constructs a proof. The verifier checks a compact set of relations. The proof is useful only if the prover produces a mathematically valid proof for the intended circuit and parameter set.

The prover is not one arithmetic kernel. Depending on the proving system, it may build and evaluate polynomials, perform finite-field additions and multiplications, compute commitments, run hashes, perform multi-scalar multiplication or other group operations, move large intermediate arrays and serialize the result. An NTT can be an important part of polynomial multiplication, but an NTT speedup is not automatically a proof-generation speedup.

### What a number-theoretic transform does

Polynomial multiplication normally combines many pairs of coefficients. A number-theoretic transform reorganizes those coefficients using arithmetic in a finite field. In a suitable field and transform length, multiplication can be converted into pointwise products in the transformed representation, followed by an inverse transform. The transform uses field additions, subtractions, multiplications by field constants and modular reduction.

The hardware cost depends on more than the number of butterflies. It includes the width of field elements, the reduction method, storage for intermediate values, the order in which coefficients are read and written, permutation or shuffle operations, synchronization and the availability of memory bandwidth. An NTT implementation can have abundant arithmetic units and still be limited by data movement or reduction latency.

The title calls the operation an additive NTT. The captured official description does not define the additive transform, its relation to a conventional NTT, the supported field, or the exact proving stage. Those details are necessary to determine what operation is accelerated and whether the baseline performs the same mathematical work.

### What “spatial acceleration” means at the hardware boundary

A spatial accelerator places multiple arithmetic and storage elements so that different pieces of a transform can operate concurrently. A transform stage can be divided among processing elements, with local data passing between them. This can reduce repeated instruction issue and expose parallel field operations.

The spatial layout must still implement the dependency graph. A later stage cannot consume a coefficient before the earlier stage has produced it. Coefficients may need to be permuted between stages, and a data set larger than the local storage must be tiled or streamed. The accelerator therefore needs a defined schedule for:

1. loading coefficients from the edge memory system;
2. applying field operations and modular reduction;
3. exchanging or permuting intermediate coefficients;
4. storing or forwarding the next-stage values; and
5. returning the completed transform to the proving software or the next proof kernel.

The arithmetic array, local buffers, interconnect, controller, external memory and host interface all affect latency and energy. A count of parallel arithmetic units or a kernel-level operation rate is insufficient without the schedule and measurement boundary.

### Why the proving-system boundary matters

Different zkSNARK proving systems use different polynomial degrees, commitment schemes, field operations and phases. The same transform can be a large fraction of one prover's runtime and a small fraction of another's. Circuit size changes the transform length and the amount of intermediate storage. The curve and field determine operand width and reduction cost.

A fair comparison must specify the curve or field, security level, circuit size, transform length, proving system, number of transforms, forward/inverse operations, memory hierarchy and proof phase being timed. It must include the work surrounding the transform when claiming proof latency or energy. CPU/GPU NTT comparison also requires equal field arithmetic, transform length, precision, memory transfers and software optimization. A generic proof accelerator is not a meaningful baseline unless its supported proving system and complete proof boundary are stated.

Security is a separate requirement. Functional correctness of the transform does not establish soundness or zero-knowledge of the full prover. The implementation must preserve exact finite-field arithmetic, required randomness, parameter generation, fault behavior and any side-channel requirements. An edge efficiency claim cannot be interpreted as a cryptographic security claim.

### What the captured result does and does not say

The official description identifies ATTINA as a spatial accelerator for an additive NTT intended to improve energy-efficient zkSNARK proving at the edge. It qualitatively claims edge zkSNARK efficiency and names CPU/GPU NTT and a generic proof accelerator as comparison categories. It reports no numerical proof latency, throughput, energy, area, circuit result, field, curve, transform length, edge device or security validation.

The [ATTINA](../observed-subthemes/specialized-accelerators-and-dataflow.md#paper-dac-2026-research983) record is evidence of a proposed spatial transform accelerator, not a measured end-to-end zkSNARK prover. The explanation separates the NTT from the full proving pipeline, field arithmetic from generic arithmetic, spatial parallelism from data movement, and functional transform correctness from proof-system and security validation.

<span id="explanation-dac-2026-research2713"></span>

## A modular RISC-V PQC extension must define what is shared, what is accelerated, and what the comparison includes

### What post-quantum cryptography requires from hardware

Post-quantum cryptography (PQC) refers to cryptographic schemes designed to remain secure against attacks that could use large quantum computers. The security claim belongs to a complete parameterized scheme and protocol, not to one arithmetic circuit. A hardware implementation must therefore preserve the scheme's required operations, parameter sizes, randomness, modular reductions, memory accesses and constant-time behavior.

The card names ML-KEM, ML-DSA, SLH-DSA and HQC. These schemes do not have one common dominant instruction. They include different combinations of hashing, sampling, polynomial or modular arithmetic, finite-field operations and compression. Even when two schemes use an operation with the same name, operand width, data layout, reduction rule and required security behavior can differ.

The design problem is thus not simply “add a crypto accelerator.” It is to choose an interface that lets software invoke useful operations without forcing a separate large datapath for every scheme, while still supplying enough specialization to beat software execution.

### What the modular extension contributes

The record describes two coupled interfaces: scalar custom instructions exposed through the RISC-V CV-X-IF interface, and a modular PQ-ALU. CV-X-IF provides a route for a RISC-V core to issue custom operations and receive results. The PQ-ALU is the hardware that performs selected cryptographic kernels. The open hardware/software stack is intended to make those operations usable across more than one PQC family.

The boundary has several steps:

1. Software represents the scheme's operands in registers or memory.
2. The compiler or hand-written code selects a custom instruction.
3. The core issues the instruction through the custom interface.
4. The PQ-ALU performs the defined arithmetic or transform.
5. The result returns to the core or a subsequent accelerator operation.

An instruction-cycle count for step 4 is not automatically the latency of the complete algorithm. Operand loads, stores, register transfers, instruction issue, result dependencies, stalls, address generation and control code can dominate when kernels are small or memory-bound. The useful measurement is the complete operation or protocol, with the boundary stated, in addition to the isolated custom-operation count.

### Why sharing and specialization are in tension

A modular unit can reuse area across algorithms. It can also reduce software changes when a new scheme uses the same primitive categories. But the shared datapath must accept the largest or most demanding operand forms, and control or conversion logic may be needed for each scheme. A unit optimized for broad reuse may have lower peak throughput than a unit built for one scheme's most frequent operation.

The comparison must therefore answer two separate questions:

- Does the extension reduce the cost of the same complete PQC operation compared with software-only RISC-V execution?
- Does the reusable unit provide a better area/performance/energy tradeoff than separate scheme-specific accelerators under the same security and implementation conditions?

The first question measures acceleration against a software baseline. The second measures the cost of reuse. A single area figure and a few custom-operation cycle counts cannot answer both.

### What must be held constant for a cryptographic comparison

PQC performance depends strongly on algorithm parameters. A larger security level can change polynomial dimensions, matrix sizes, sampling work, memory traffic and the number of repetitions. A fair comparison therefore needs the same standardized parameter set or an explicit security-equivalent mapping.

It also needs the same RISC-V core, clock, voltage, compiler, instruction scheduling, memory hierarchy, data representation and protocol boundary. Key generation, encapsulation, decapsulation, signing and verification may stress different kernels. Hashing and compression may be peripheral in one operation and dominant in another. Reporting only the custom arithmetic excludes the work that software still performs.

Security is another independent boundary. Constant-time behavior, rejection handling, random-number generation, fault response and side-channel resistance are not implied by functional arithmetic or low cycle count. A modular ALU can produce the right mathematical result while an interface, memory access or control branch leaks information. The captured description reports no security validation, so the hardware proposal must not be read as a security proof.

### What the reported hardware numbers establish

The official description reports approximately 48 kGE area, post-synthesis instruction-cycle counts, and power and energy estimates per custom operation in a 65-nm CMOS characterization. “kGE” is an area normalization based on equivalent logic gates; it is useful for a rough area statement but does not reveal memory, custom arithmetic, standard-cell utilization, clocking, I/O or layout overhead. Post-synthesis results are also earlier than placed-and-routed or measured silicon results.

Power and energy per custom operation require a stimulus, switching activity, voltage, frequency and inclusion boundary. If the estimate excludes the RISC-V core, memory, interface and software work, it cannot be compared directly with complete protocol energy. The open-source release is valuable for inspection and reproduction, but source availability alone does not establish that the reported synthesis or security result has been independently reproduced.

### What the record establishes and where it stops

The official description establishes an open modular RISC-V/PQ-ALU proposal spanning hash, sampling, modular/polynomial, finite-field and compression kernels for ML-KEM, ML-DSA, SLH-DSA and HQC. It reports approximately 48 kGE and post-synthesis cycle, power and energy estimates. It does not establish absolute end-to-end throughput, comparable area/performance against scheme-specific accelerators, post-layout timing, measured silicon, constant-time behavior or side-channel resistance.

The [modular RISC-V PQC extension](../observed-subthemes/specialized-accelerators-and-dataflow.md#paper-dac-2026-research2713) record is evidence of a reusable cryptographic hardware interface, not proof that all listed schemes are secure and faster at equal conditions. The explanation separates mathematical kernels from protocol work, custom-instruction latency from complete execution, reusable area from peak specialization, synthesis estimates from silicon, and functional acceleration from security validation.

<span id="explanation-dac-2026-research2128"></span>

## CIM-MP: on-device personalization must control both the physical update and the errors that update creates

### What on-device personalization means

Personalization changes a model using data that remains on the device. The device is not only running a fixed model; it is also applying parameter updates. A normal digital training description can treat a weight as an exact number in memory, compute a gradient, and write the new number back. An analog compute-in-memory (CIM) array does not provide that abstraction for free.

In an analog CIM array, a weight is represented by a physical quantity such as a cell conductance. An input is applied to a row, the cell response contributes a current, and currents are accumulated along a column. This can avoid repeatedly moving every weight to a separate arithmetic unit. It also means that the same physical state serves two roles: it stores the parameter and participates in the computation. Variation between cells, nonlinear programming, read noise, drift and limited conductance precision can change the computed value.

For inference, a fixed error may be tolerable if the model was trained with that error. For personalization, the device uses its own noisy output to decide how to change its own physical state. An error in the forward result changes the loss and the gradient; an error in the update changes the next physical state. The process can therefore accumulate error rather than merely add a fixed inference perturbation.

### What the captured method claims to change

The record calls the hardware/software co-design CIM-MP. It names three connected mechanisms: pulse-based weight mapping for in-situ updates, Feature Variation Elimination (FVE) during forward propagation, and Gradient Adaptive Purification (GAP) during backpropagation.

Pulse-based mapping is the interface between a numerical update and a physical memory cell. A desired change such as “increase this weight by a small signed amount” must be represented by programming pulses. The mapping must handle positive and negative changes, pulse granularity, conductance bounds, nonlinear response and random update error. A mapping can make updates more compatible with the device, but that claim requires the pulse rule, device response and saturation behavior. The captured description does not provide those details.

FVE addresses variation in the forward path. The forward pass produces activations from the current physical weights. If the same input produces materially different activations because of device non-idealities, the loss is computed from a perturbed representation of the model. “Feature variation elimination” therefore needs a precise definition of what variation is estimated, what signal is removed or corrected, and whether the correction is inside the array, in peripheral logic or in software. The record gives the mechanism name but not its equations or placement.

GAP addresses the backward path. Backpropagation uses derivatives of the loss with respect to parameters. A noisy forward result, a noisy multiply-accumulate, or a noisy gradient readout can produce a gradient that points in the wrong direction or has the wrong magnitude. Adaptive purification can reject, rescale or otherwise modify that gradient. It must be judged by the final update trajectory, not by the cleanliness of an intermediate gradient alone. Removing small gradients may suppress noise but can also remove a real personalization signal; the threshold or adaptation rule matters.

These mechanisms act at different points:

1. The mapping determines how a requested parameter change is written into the array.
2. FVE acts on variation in the forward feature computation.
3. GAP acts on the gradient before it is converted into a physical update.

The three steps are not interchangeable. Better pulse programming cannot correct an activation error that has already changed the loss. Cleaner features cannot guarantee that the backward gradient is correct. A purified gradient cannot guarantee that the array will realize the requested update. A valid end-to-end claim must measure the closed loop from current conductance, through forward and backward computation, to the next conductance state.

### Why the training comparison must be defined carefully

The reported result is “up to 35.1% accuracy improvement over state-of-the-art approaches.” This is a relative statement whose meaning depends on the denominator. It could refer to an absolute percentage-point difference, a relative percentage increase, recovery from a noisy baseline, or a selected task/model condition. The captured description does not state the task, model, clean accuracy, noisy baseline accuracy, personalization data, number of updates or convergence condition.

The comparison must keep the following variables aligned:

- the initial pretrained model and the parameters allowed to change;
- the local personalization dataset and its size;
- the number of update steps, batch size and learning-rate schedule;
- the digital, ideal-CIM and non-ideal-CIM references;
- the device-noise, conductance-variation and programming model;
- the accuracy denominator and the point at which accuracy is measured.

Otherwise a reported improvement may measure a different adaptation budget or a weaker baseline rather than a better physical learning method. Accuracy also does not establish that personalization is efficient. The full result needs update latency, energy per update, read/write traffic, peripheral energy, storage overhead, convergence steps and the effect of repeated programming on endurance and retention.

### What “robust” must mean at the device boundary

Robustness here has at least three separate meanings. The algorithm may tolerate variation across cells. It may tolerate stochastic error each time a cell is read or programmed. It may remain useful as the cell drifts or accumulates writes. A method can pass one of these tests and fail another.

The hardware boundary must include the array and the circuits that make its result usable: input and output conversion, reference generation, accumulation, calibration, update-pulse generation, digital storage and control. If only an idealized array operation is simulated, the result is a learning-algorithm study under a device model, not an energy or area result for a complete CIM system. If the array is fabricated but the personalization experiment uses a separate digital gradient or hidden calibration path, that boundary must be stated.

The source record does not specify the device technology, ADC/DAC precision, pulse amplitude or width, conductance states, endurance, retention, noise distribution, model/task suite or measurement boundary. These missing fields prevent a universal interpretation of the 35.1% value. They do not invalidate the proposed direction; they define what a paper-level review must recover before accepting the hardware or learning claim.

### What the record establishes and where it stops

The official description establishes a co-design proposal for in-situ deep-model personalization on non-ideal analog CIM. It identifies pulse-based weight mapping, forward feature-variation suppression and adaptive gradient purification, and reports up to 35.1% accuracy improvement over stated state-of-the-art approaches. It does not establish the absolute accuracy, task/model, training budget, device model, physical implementation, energy, endurance or complete update-loop cost.

The [CIM-MP](../observed-subthemes/specialized-accelerators-and-dataflow.md#paper-dac-2026-research2128) record is evidence of a noise-aware CIM personalization method, not proof of robust on-device learning across devices. The explanation separates physical weight storage from numerical parameters, forward error from backward error, gradient purification from pulse realization, accuracy from training cost, and algorithmic simulation from complete hardware validation.

<span id="explanation-dac-2026-research1499"></span>

## KCD-CAM: a nearest-neighbor accelerator must preserve which points are eligible before it can select the nearest ones

### What K-nearest-neighbor search does

For a query point, KNN computes a distance to candidate points, orders or selects the smallest distances, and returns the K nearest candidates. In point-cloud processing, this operation can be repeated for many query points and can dominate the time spent preparing local neighborhoods for a detector or geometric algorithm.

The distance result and the selected set are different parts of the computation. A method can calculate distances quickly but still spend time storing them, comparing them, maintaining the top-k set, moving coordinates, or preparing the input structure. If a range filter or hash removes candidates, its correctness and recall must be measured against the full candidate set.

### What KCD-CAM changes

The record describes a 4T2R ReRAM charge-domain content-addressable-memory accelerator with in-situ range search, iterative top-k selection and dual-granularity voxel hashing. A content-addressable memory compares a query against stored entries by content rather than reading each address in a serial order. Charge-domain computation uses stored charge or current behavior to perform an analog comparison or arithmetic operation; sensing, conversion and calibration remain part of the hardware path.

In-situ range search can reject points outside a distance threshold before they enter later selection. Iterative top-k selection maintains the current best K candidates instead of fully sorting every distance. Voxel hashing groups points by spatial regions so the accelerator can search a smaller or more relevant set, while dual granularity provides different spatial resolution for different density or range conditions. These reductions are useful only when the omitted candidates cannot change the required neighbors, or when the resulting recall loss is reported.

### Why point-cloud quality is part of the accelerator result

The nearest neighbors may be used for local features, grouping, registration or object detection. A small change in the neighbor set can have little effect for one scene and a large effect for a sparse object, boundary or distant point. “Higher speed” is therefore incomplete without recall, distance error, neighbor-set agreement or downstream task quality.

Voxel hashing also adds preprocessing and storage. Building or updating the hash, moving points into bins, handling collisions and searching boundary voxels consume time and energy. A charge-domain array adds ADC/sensing, reference generation, peripheral circuitry and data movement. An accelerator-only arithmetic result is not necessarily a complete point-cloud pipeline result.

### What the reported ratios require

The official description reports 279.79× higher speed and 3282× greater energy efficiency than GPU implementations, plus 8.51× speed and 4.76× energy-efficiency improvement over state-of-the-art KNN accelerators. The captured record does not identify datasets, point counts, K, recall, device technology, ADC/peripheral cost, preprocessing or measurement boundaries. The values are therefore source-reported ratios under unspecified conditions, not universal edge-point-cloud gains.

Compare the same point clouds, query count, K, distance metric, radius, recall target, precision and output format. Include voxelization/hash construction, point movement, sensing/conversion, top-k maintenance, host work and downstream use. Report latency per query and per complete point cloud, peak memory, recall, distance error, area, power and energy. Test density variation, outliers, sparse/dense regions and point counts that exceed local storage.

### What the record establishes and where it stops

The official description establishes a ReRAM charge-domain CAM architecture combining range filtering, iterative top-k selection and dual-granularity voxel hashing for point-cloud KNN. It reports large speed and energy-efficiency ratios but omits recall, preprocessing, peripheral, technology and measurement conditions.

The [KCD-CAM](../observed-subthemes/specialized-accelerators-and-dataflow.md#paper-dac-2026-research1499) record is evidence of a specialized KNN accelerator, not an independently validated complete point-cloud system. The detailed explanation above separates distance computation from neighbor selection, candidate pruning from recall, array arithmetic from peripheral cost, and kernel ratios from end-to-end processing.

## How the selected papers differ

The captured LPN-acceleration record organizes configurable engines and stage scheduling for a cryptographic computation. Its core question is how the hardware performs the required cryptographic work within a stated parameter set. The record lacks those parameters and several comparison conditions, so its hardware result cannot establish a stronger cryptographic guarantee. [Recorded evidence](../observed-subthemes/specialized-accelerators-and-dataflow.md#paper-dac-2026-research1822)

KCD-CAM instead concerns nearest-neighbor search on point-cloud data. Its captured description combines a memory structure that compares values, a search procedure, and data organization. That combination makes preprocessing, answer quality, and the surrounding circuit costs part of the comparison. A headline acceleration ratio alone cannot identify which change produced the benefit. [Recorded evidence](../observed-subthemes/specialized-accelerators-and-dataflow.md#paper-dac-2026-research1499)

The correlation-aware GKP decoder addresses the time required to interpret error information in a quantum-computing setting. Here the validity of decoding under a specified noise model is central. Hardware timing obtained from synthesis is an estimate for the synthesized circuit; it does not establish performance of the complete physical quantum system. [Recorded evidence](../observed-subthemes/specialized-accelerators-and-dataflow.md#paper-dac-2026-research727)

These examples share the idea of adapting hardware to a specific operation. They do not share one workload, accuracy requirement, or meaningful common speedup denominator. The connections above are a synthesis of their stored descriptions, not newly verified full-paper results.

## What the evaluation needs to separate

First compare correctness or answer quality under the same input conditions. Then measure useful completed work, total time, energy, memory, and hardware area. Include any host processor work and state which resources are charged to the accelerator.

Where several changes are combined, evaluate configurations that remove individual changes while keeping the rest comparable. This can reveal whether the gain comes from arithmetic, data organization, concurrency, or a more favorable input representation. The removed-change comparison is often called an ablation.

Finally, vary input size and structure. A result that depends on fitting all working data in local storage remains useful, but that storage condition must be explicit. Evidence of usefulness across several workloads is stronger than a single best-case ratio. Establishing growth of this research approach over time additionally requires comparable paper populations across years.
