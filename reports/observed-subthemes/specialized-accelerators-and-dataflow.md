# Specialized accelerators and dataflow

This subject has 35 records in the selected sample. This page explains where it fits, then presents all captured paper evidence without shortening the measurements or limitations.

[Definitions used in the paper records](../reading-guide-v1.md)

## Understand the parent subject first

- [Architecture and accelerators](../themes/architecture-and-accelerators.md)

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

## Compare the results carefully

First identify the inputs and required output quality. Then identify the limited resource: time, memory, communication, energy, circuit area, or correctness coverage. Ask which part of the method reduces that cost and which new cost it adds. Compare numbers only when the experiments hold these conditions sufficiently similar.

A conference description may explain the proposal while omitting the full experiment. An author preprint link may have been coded from its abstract. The source classification does not by itself establish that every table was read. Missing locations remain visible below.

## Complete captured evidence

These are evidence records, not substitutes for the explanations above. Each record preserves its problem, proposed method, measurements, comparison conditions, and source limits. A populated record does not establish that its mechanism has been fully explained or independently verified.

<span id="paper-dac-2026-research1822"></span>

### Leveraging AI-Inspired Hardware Architecture to Enhance LPN Acceleration in Post-Quantum Cryptography

DAC 2026 · Record: `dac-2026-research1822`

[Read the step-by-step explanation](#explanation-dac-2026-research1822)

**Updated source-backed reading card**

Reviewed 2026-09-08. Reconciles the LPN accelerator card with the captured official description; explains LPN workload/security parameters, heterogeneous FPGA engines, pipeline/bandwidth behavior and the boundary between performance and cryptographic claims from first principles.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Existing LPN accelerators may optimize an isolated computation while leaving execution-flow, buffering and data-transfer bottlenecks in post-quantum cryptography workloads.

**Mechanism / artifact:**

AI-inspired heterogeneous FPGA architecture with configurable LPN engines, stage-level scheduling and bandwidth-oriented performance modeling.

**Workload — the work tested:**

LPN acceleration workloads on FPGAs; LPN variant, dimension, sample count, noise rate, security level, success condition, FPGA family and baseline are unspecified.

**Hardware and manufacturing assumptions:**

FPGA-based post-quantum accelerator with heterogeneous engines and bandwidth-limited data movement; device, clock, memory interface, LUT/DSP/BRAM, power and buffer assumptions are unspecified.

**Baseline — the comparison method:**

State-of-the-art LPN architecture

LPN parameters, security, FPGA, clock, resource, correctness, throughput and measurement-boundary parity are unspecified

**Reported measurements:**

The official description reports 52.80x performance gain over a state-of-the-art LPN architecture; throughput definition, parameter set, security condition, baseline implementation and resource/energy boundary are unspecified.

**Limits on the conclusion:**

LPN parameters define both the work and the security meaning; a speed result at an unspecified parameter set cannot establish support for a target security level.

Configurable engines and stage scheduling can improve pipeline balance, but producer/consumer rates, buffers and memory bandwidth can still limit complete throughput.

A large relative gain may reflect baseline data-transfer bottlenecks, different conditions or baseline maturity; it does not establish cryptographic superiority or security.

The official description supplies no parameter set, FPGA device, clock, resource, energy, correctness, throughput definition or independent reproduction; the reported performance remains unestablished beyond its qualitative record.

**Source and location**

Evidence tier: Primary captured official DAC description only; no full paper extraction, lpn accelerator reproduction or independent cryptographic parameter, FPGA resource, power and throughput validation. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH1822&sess=sess108)

DAC 2026 official description and data/review-packets/dac-2026-research1822.json: LPN post-quantum acceleration; heterogeneous configurable engines; stage scheduling; bandwidth model; 52.80x over state-of-the-art LPN architecture; parameter/security/hardware conditions unspecified.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** state-of-the-art LPN architecture

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH1822&sess=sess108

**Hardware or process assumptions:** FPGA-based post-quantum cryptography accelerator with heterogeneous engines and bandwidth-limited data movement; device and memory-interface details are unspecified.

**Limits:** The description omits LPN parameters, security assumptions, FPGA resource/clock results, energy, throughput definition, and baseline implementation details.

A large relative gain may depend on data-transfer bottlenecks or baseline maturity and does not establish cryptographic superiority.

Official description only; performance and security claims require paper-level verification.

**Method or artifact:** AI-inspired heterogeneous FPGA architecture with configurable engines, stage-level scheduling, and bandwidth-oriented performance modeling for LPN.

**Metrics:** 52.80x performance gain over the state-of-the-art LPN architecture

**Problem:** Existing LPN accelerators optimize isolated computation while overlooking execution flow and data-transfer bottlenecks in post-quantum cryptography.

**Workload or benchmark:** LPN acceleration workloads on FPGAs; parameter sets, security level, FPGA family, clock, resource use, and state-of-the-art baseline are unspecified.

</details>

<span id="paper-dac-2026-research727"></span>

### A Correlation-Aware GKP Decoder for Fault-Tolerant Continuous-Variable Photonic Quantum Computers

DAC 2026 · Record: `dac-2026-research727`

[Read the step-by-step explanation](#explanation-dac-2026-research727)

**Updated source-backed reading card**

Reviewed 2026-09-08. Reconciles the correlation-aware GKP decoder card with the captured official description; explains continuous-variable syndrome inference, correlated noise, decoder correctness, 7-nm synthesis latency and complete photonic feedback-loop boundaries from first principles.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Correlation-aware GKP decoding can improve error correction but straightforward hardware may not meet the optical-clock timing needed for fault-tolerant continuous-variable photonic quantum computing.

**Mechanism / artifact:**

Low-latency hardware accelerator for correlation-aware GKP decoding with synthesis-based design-space exploration; noise model, decoder state and implementation details are unspecified.

**Workload — the work tested:**

Correlation-aware GKP decoding workloads; code parameters, measurement precision, covariance/correlation structure, logical-error target and comparison architecture are unspecified.

**Hardware and manufacturing assumptions:**

7-nm FinFET synthesized decoder intended for photonic optical-clock timing; process library, frequency constraint, area, power, memory, post-layout status and photonic integration are unspecified.

**Baseline — the comparison method:**

Straightforward correlation-aware hardware implementation

Uncorrelated or prior GKP decoding methods

Noise, code, accuracy, latency, area, power, process and complete-loop boundary parity are unspecified

**Reported measurements:**

The official description reports 12.96 ns decoding latency in 7-nm FinFET synthesis and qualitative accuracy/latency/area tradeoffs; logical-error rate, initiation interval, area, power and complete-loop conditions are unspecified.

**Limits on the conclusion:**

A GKP decoder infers a grid displacement from continuous noisy measurements; correlated noise changes the probability model and a mismatched model can increase logical errors even when the circuit is fast.

Synthesis timing estimates a modeled circuit under library and constraint assumptions; it does not establish post-layout timing, power, yield or measured photonic-system behavior.

Decoder decision latency, initiation interval and complete feedback-loop timing are different quantities; sensor, buffering, correction output and actuator costs must be included for an optical-clock claim.

The official description supplies no code/noise parameters, logical accuracy, area, power, post-layout or integration results; fault-tolerant-system benefit remains unestablished.

**Source and location**

Evidence tier: Primary captured official DAC description only; no full paper extraction, decoder reproduction or independent logical error, post layout, power and photonic loop validation. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH727&sess=sess134)

DAC 2026 official description and data/review-packets/dac-2026-research727.json: correlation-aware GKP decoder; 7-nm FinFET synthesis; 12.96 ns latency; qualitative accuracy/latency/area tradeoff; omitted code/noise/area/power and integrated-system conditions.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** straightforward hardware implementation of correlation-aware decoding

uncorrelated or prior GKP decoding methods

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH727&sess=sess134

**Hardware or process assumptions:** 7-nm FinFET synthesized decoder intended to meet photonic optical-clock timing; process libraries, frequency assumptions, area, power, and interconnect are unspecified.

**Limits:** The description omits decoding accuracy, area, power, throughput, noise assumptions, and baseline latency.

Synthesis timing does not establish post-layout or integrated photonic-system performance.

Official description only; quantum-error-correction and hardware claims require paper-level verification.

**Method or artifact:** Low-latency hardware accelerator optimized for correlation-aware GKP decoding with synthesis-based design-space exploration.

**Metrics:** 12.96 ns decoding latency in 7-nm FinFET synthesis

Accuracy/latency/area tradeoffs explored qualitatively

**Problem:** Correlation-aware GKP decoding improves error correction but straightforward hardware implementations are too computationally slow for optical-clock operation in tens of nanoseconds.

**Workload or benchmark:** Correlation-aware GKP decoding workloads for fault-tolerant continuous-variable photonic quantum computers; decoder sizes, noise model, accuracy target, and comparison architecture are unspecified.

</details>

<span id="paper-dac-2026-research1499"></span>

### KCD-CAM: A K-Nearest-Neighbor Accelerator Based on Charge-Domain Content-Addressable-Memory for Point Cloud Processing

DAC 2026 · Record: `dac-2026-research1499`

[Read the step-by-step explanation](#explanation-dac-2026-research1499)

**Updated source-backed reading card**

Reviewed 2026-09-08. Reconciles the KCD-CAM card with the captured official description; explains KNN distance/selection, charge-domain CAM, range filtering, iterative top-k, voxel hashing, recall and complete point-cloud cost from first principles.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Euclidean-distance top-k KNN search can dominate point-cloud processing and prevent real-time edge execution because distance computation, candidate selection and data movement are repeated for many queries.

**Mechanism / artifact:**

4T2R ReRAM charge-domain CAM KNN accelerator with in-situ range search, iterative top-k selection and dual-granularity voxel hashing; array/sensing and exact pruning behavior are unspecified.

**Workload — the work tested:**

Real-world 3D point-cloud datasets and KNN processing; dataset names, point counts, query count, K, distance metric, radius, recall/downstream quality and preprocessing are unspecified.

**Hardware and manufacturing assumptions:**

4T2R ReRAM CAM with charge-domain computation for edge point-cloud processing; array size, ADC/sensing, process, voltage, calibration, peripheral, memory and data-movement boundaries are unspecified.

**Baseline — the comparison method:**

GPU implementations

State-of-the-art KNN accelerators

Point cloud, K, recall, precision, preprocessing, device, peripheral and energy-boundary parity are unspecified

**Reported measurements:**

The official description reports 279.79x speed and 3282x energy-efficiency improvement over GPU implementations, plus 8.51x speed and 4.76x energy-efficiency improvement over state-of-the-art KNN accelerators; recall, datasets, technology and measurement boundaries are unspecified.

**Limits on the conclusion:**

KNN distance computation and top-k neighbor selection are separate costs; range filtering or hashing can reduce candidates only if omitted points cannot change the required neighbors or recall loss is measured.

Charge-domain CAM computation still requires sensing, ADC/reference circuitry, calibration, storage, voxel/hash construction and data movement; array arithmetic is not complete point-cloud cost.

Voxel hashing and dual granularity can reduce search work while adding preprocessing, collisions, boundary handling and density-dependent behavior; downstream point-cloud quality must be measured.

The official description supplies no datasets, point counts, recall, preprocessing, ADC/peripheral, technology, absolute latency or energy boundary; the large ratios remain baseline- and condition-dependent.

**Source and location**

Evidence tier: Primary captured official DAC description only; no full paper extraction, kcd cam reproduction or independent recall, preprocessing, peripheral, device and end to end validation. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH1499&sess=sess107)

DAC 2026 official description and data/review-packets/dac-2026-research1499.json: 4T2R ReRAM charge-domain CAM; in-situ range search; iterative top-k; dual-granularity voxel hashing; GPU/state-of-the-art KNN baselines; 279.79x/3282x and 8.51x/4.76x ratios; omitted recall and system conditions.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** GPU implementations

state-of-the-art KNN accelerators

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH1499&sess=sess123

**Hardware or process assumptions:** 4T2R ReRAM CAM with charge-domain computation and edge point-cloud processing; array size, ADC/sensing, process, voltage, and data-movement boundaries are unspecified.

**Limits:** The description omits accuracy/recall tradeoffs, end-to-end preprocessing, ADC/peripheral costs, technology details, and measurement boundaries.

Large relative gains may depend on GPU and accelerator baseline configurations and whether data movement is included.

Official description only; performance and energy claims require paper-level hardware verification.

**Method or artifact:** ReRAM charge-domain CAM KNN accelerator with in-situ range search, iterative top-k selection, and dual-granularity voxel hashing.

**Metrics:** 279.79x higher speed than GPU implementations

3282x greater energy efficiency than GPU implementations

8.51x speed improvement over state-of-the-art KNN accelerators

4.76x energy-efficiency improvement over state-of-the-art KNN accelerators

**Problem:** Euclidean-distance top-k KNN search dominates point-cloud processing cost and prevents real-time efficient edge execution.

**Workload or benchmark:** Real-world 3D point-cloud datasets and KNN processing; dataset names, point counts, accuracy criteria, device parameters, and GPU baselines are unspecified.

</details>

<span id="paper-dac-2026-research2128"></span>

### Enabling Robust On-Device Personalization via Pulse-Based Mapping and Noise Suppression for Non-Ideal CIM Architecture

DAC 2026 · Record: `dac-2026-research2128`

[Read the step-by-step explanation](#explanation-dac-2026-research2128)

**Updated source-backed reading card**

Reviewed 2026-09-08. Reconciles the CIM-MP on-device personalization card with the captured official DAC description; explains the separation between analog CIM storage, in-situ learning, pulse-based weight updates, forward feature variation, backward gradient error and the evidence boundary around the reported accuracy improvement.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

On-device personalization changes model parameters where they are stored. In analog CIM, the stored conductance is also part of the multiply-accumulate path, so device variation and update noise can alter both the forward prediction and the gradient used for the next update.

**Mechanism / artifact:**

CIM-MP hardware/software co-design using pulse-based weight mapping for in-situ updates, Feature Variation Elimination during forward propagation and Gradient Adaptive Purification during backpropagation; exact mapping, suppression and purification equations are unavailable in the captured description.

**Workload — the work tested:**

Deep-model personalization under non-ideal CIM conditions; model and task suite, number and type of personalization samples, training steps, device-noise distribution, accuracy denominator and baseline implementations are unspecified.

**Hardware and manufacturing assumptions:**

Analog CIM arrays that support in-situ weight updates and noisy forward/backward computation; device technology, conductance states, pulse amplitude/width, ADC/DAC, peripheral circuits, calibration, write endurance, retention and energy are unspecified.

**Baseline — the comparison method:**

State-of-the-art CIM personalization approaches

Model/task, personalization data, noise model, training budget, precision, hardware boundary and accuracy denominator are unspecified

**Reported measurements:**

The official description reports up to 35.1% accuracy improvement over state-of-the-art approaches; absolute accuracy, task/model, baseline value, convergence cost, energy and device conditions are unspecified.

**Limits on the conclusion:**

A pulse-based mapping defines how a desired signed weight change becomes physical programming pulses; its benefit depends on pulse granularity, conductance nonlinearity, stochastic update error, saturation, retention and write endurance, none of which are reported in the captured description.

Forward feature variation and backward gradient error are different failure locations. Suppressing activation variation does not by itself recover the correct gradient, and purifying a gradient does not by itself make the forward model faithful; the combined training rule must be evaluated against clean-digital and noisy-device references.

On-device personalization is a training process, not only an inference measurement. Accuracy improvement must be tied to the same task, adaptation data, number of updates, initialization, convergence criterion and final model state as the baseline; a relative improvement without these denominators cannot be interpreted as a general hardware advantage.

The official description supplies no absolute accuracy, model/task, noise distribution, update count, energy, endurance, ADC/DAC or silicon measurement. The 35.1% value remains a source-reported upper result under unknown conditions and does not establish robust physical CIM personalization.

**Source and location**

Evidence tier: Primary captured official DAC description only; no full paper extraction, device aware reproduction or independent validation of the training algorithm, accuracy, energy, endurance and non ideality model. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH2128&sess=sess139)

DAC 2026 official description and data/review-packets/dac-2026-research2128.json: CIM-MP co-optimization; pulse-based weight mapping; Feature Variation Elimination in forward propagation; Gradient Adaptive Purification in backpropagation; up to 35.1% accuracy improvement; omitted model, task, device, noise and training conditions.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** state-of-the-art CIM personalization approaches

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH2128&sess=sess139

**Hardware or process assumptions:** Analog CIM arrays supporting in-situ weight updates and noisy forward/backward computation; device technology, ADC/DAC, pulse programming, endurance, and peripheral overhead are unspecified.

**Limits:** The description omits absolute accuracy, task/model, convergence cost, energy, update endurance, and noise distributions.

Accuracy improvement may depend on the selected baseline and simulated rather than measured device behavior.

Official description only; learning and hardware claims require paper-level device-aware verification.

**Method or artifact:** Pulse-based in-memory update mapping with feature-noise suppression and gradient purification for robust CIM fine-tuning.

**Metrics:** Up to 35.1% accuracy improvement over state-of-the-art approaches

**Problem:** Analog CIM weights are expensive to read and transfer for external fine-tuning, while non-ideal device noise makes direct on-device personalization unstable.

**Workload or benchmark:** On-device deep-model personalization under non-ideal CIM conditions; model/task suite, device noise model, training budget, and state-of-the-art baselines are unspecified.

</details>

<span id="paper-dac-2026-research2713"></span>

### Raise the Shields: A Modular RISC-V Extension for Post Quantum Cryptography

DAC 2026 · Record: `dac-2026-research2713`

[Read the step-by-step explanation](#explanation-dac-2026-research2713)

**Updated source-backed reading card**

Reviewed 2026-09-08. Reconciles the modular RISC-V post-quantum cryptography extension card with the captured official DAC description; explains the cryptographic kernel diversity, instruction-extension boundary, modular PQ-ALU, reuse versus specialization tradeoff and synthesis-only evidence boundary.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Post-quantum cryptography schemes use different dominant operations, so a fixed scheme-specific accelerator can be fast for one algorithm while being difficult to reuse in a constrained RISC-V system.

**Mechanism / artifact:**

Open RISC-V extension exposing scalar CV-X-IF instructions and a modular PQ-ALU for Keccak, sampling, modular and polynomial arithmetic, finite-field operations and compression across ML-KEM, ML-DSA, SLH-DSA and HQC; exact instruction set, datapaths and software mapping are not available in the captured description.

**Workload — the work tested:**

ML-KEM, ML-DSA, SLH-DSA and HQC standardized algorithms plus candidates under evaluation; parameter sets, security levels, message sizes, implementation language, compiler and end-to-end protocol throughput are unspecified.

**Hardware and manufacturing assumptions:**

RISC-V core with CV-X-IF and modular PQ-ALU synthesized in 65-nm CMOS; clock, voltage, memory hierarchy, area accounting, timing constraints, standard-cell library, placement/routing, post-layout status and power methodology are unspecified.

**Baseline — the comparison method:**

Software-only RISC-V execution

Scheme-specific PQC accelerators

Algorithm parameters, compiler, core configuration, clock, security, throughput, area and energy boundaries are unspecified

**Reported measurements:**

Approximately 48 kGE area

Post-synthesis instruction-cycle counts

Power and energy estimates per custom operation

Open-source hardware/software release; absolute throughput and comparable end-to-end protocol results are unspecified

**Limits on the conclusion:**

A post-quantum scheme is a protocol built from kernels such as hashing, sampling, modular arithmetic, polynomial arithmetic, finite-field operations and compression. Sharing a modular ALU across these kernels can improve reuse, but each operation still needs defined width, latency, throughput, memory access and software instruction mapping.

CV-X-IF custom instructions reduce the instruction and control path only when the core can issue them, supply operands and consume results without hidden stalls. Instruction-cycle counts do not by themselves establish complete algorithm latency because loads, stores, register movement, synchronization and software control remain in the boundary.

A unified extension can trade peak performance for one scheme against area reuse and crypto agility. Fair comparison requires the same algorithm parameters, security level, RISC-V core, compiler, memory system, clock, precision, protocol boundary and treatment of key generation, encapsulation/signing, verification and hashing.

The official description supplies approximately 48 kGE and post-synthesis cycle/power/energy claims but no area breakdown, timing, voltage, post-layout status, absolute throughput, security validation or artifact reproduction. These values establish a modular hardware proposal, not a demonstrated secure and universally faster PQC processor.

**Source and location**

Evidence tier: Primary captured official DAC description only; no full paper extraction, RTL/FPGA/asic artifact reproduction or independent security, timing, area, power and end to end protocol validation. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH2713&sess=sess108)

DAC 2026 official description and data/review-packets/dac-2026-research2713.json: scalar CV-X-IF instructions; modular PQ-ALU; Keccak, sampling, modular/polynomial arithmetic, finite-field operations and compression; ML-KEM/ML-DSA/SLH-DSA/HQC; 65-nm post-synthesis characterization; approximately 48 kGE; omitted security and comparison conditions.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** software-only RISC-V execution

scheme-specific PQC accelerators

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH2713&sess=sess108

**Hardware or process assumptions:** RISC-V core with CV-X-IF and modular PQ-ALU synthesized in 65-nm CMOS; core configuration, clock, memory, compiler, and post-layout conditions are unspecified.

**Limits:** The description omits absolute throughput, energy, security validation, area breakdown, timing, and comparison conditions.

A unified extension may trade peak scheme-specific performance for reuse and software compatibility.

Official description only; ASIC and cryptographic claims require paper-level and artifact verification.

**Method or artifact:** Unified modular RISC-V extension and PQ-ALU spanning hash-, lattice-, and code-based cryptographic kernels, with open hardware/software stack.

**Metrics:** Approximately 48 kGE area

Post-synthesis instruction-cycle counts

Power and energy estimates per custom operation

Open-source hardware/software release

**Problem:** Post-quantum schemes have diverse dominant kernels, making fixed accelerators difficult to reuse while constrained RISC-V systems need practical crypto agility.

**Workload or benchmark:** ML-KEM, ML-DSA, SLH-DSA, and HQC standardized algorithms plus candidates under evaluation; cycle, power, energy, and area methodology details are unspecified.

</details>

<span id="paper-dac-2026-research2824"></span>

### ISA-PM: A Unified ISA Extension and Microarchitecture Enabling Efficient ECPM in IoT Devices

DAC 2026 · Record: `dac-2026-research2824`

[Read the step-by-step explanation](#explanation-dac-2026-research2824)

**Updated source-backed reading card**

Reviewed 2026-09-08. Reconciles the ISA-PM card with the captured official DAC description; explains elliptic-curve point multiplication, curve-form flexibility, bit-width decomposition, ISA/microarchitecture boundaries and the area-time comparison limits.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Curve-specific elliptic-curve point-multiplication accelerators must be redesigned when field parameters or curve forms change, which is undesirable for area-constrained IoT cryptography.

**Mechanism / artifact:**

Unified ISA extension and microarchitecture supporting ECPM across Montgomery and short-Weierstrass curves through three-phase small-bit-width modular computation and design-space exploration over resource parallelism; exact instruction semantics and datapath are unavailable in the captured description.

**Workload — the work tested:**

Elliptic-curve point multiplication for multiple curves on an AMD Virtex-7 FPGA; curve set, field sizes, scalar lengths, coordinate system, operation count, frequency, FPGA resource use and security checks are unspecified.

**Hardware and manufacturing assumptions:**

Area-constrained IoT cryptographic accelerator with flexible modular arithmetic, unified RISC-V-style ISA integration and FPGA implementation; device configuration, clock, memory, compiler, interface and energy measurement boundary are unspecified.

**Baseline — the comparison method:**

State-of-the-art lightweight ECPM hardware accelerators

Curve-specific ECPM designs

Curve, field, scalar, FPGA, clock, resource, software, security and area-time boundary parity are unspecified

**Reported measurements:**

The official description reports up to 8.37x area-time-product improvement on an AMD Virtex-7 FPGA; absolute area, latency, frequency, energy and curve-by-curve values are unspecified.

**Limits on the conclusion:**

Elliptic-curve point multiplication repeatedly combines a public curve point according to a secret scalar. The field arithmetic, point representation, addition/doubling formulas, coordinate system and scalar-processing schedule determine both correctness and cost; supporting a curve name alone does not establish support for its complete secure implementation.

Montgomery and short-Weierstrass curves use different curve forms and can require different formulas, field parameters and exceptional-case handling. A unified datapath must define how those differences are selected and how invalid points, identity cases, scalar width and modular reduction are handled.

Bit-width decomposition can replace a wide modular operation with several smaller operations and can expose parallelism choices. It also adds partial-result accumulation, carries, reductions, control and memory traffic. An ISA instruction count for a modular primitive must be distinguished from complete scalar multiplication and from software overhead at the core interface.

The 8.37x area-time-product value is an upper relative result under an unspecified Virtex-7 configuration and baseline. The description omits absolute area, latency, energy, frequency, curve coverage, software overhead, timing closure, constant-time analysis and side-channel validation; flexibility may reduce peak performance compared with a dedicated curve accelerator.

**Source and location**

Evidence tier: Primary captured official DAC description only; no full paper extraction, RTL/FPGA artifact reproduction or independent cryptographic, timing, area, energy and side channel validation. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH2824&sess=sess174)

DAC 2026 official description and data/review-packets/dac-2026-research2824.json: unified ISA/microarchitecture; Montgomery and short-Weierstrass curves; three-phase small-bit-width modular computation; resource-parallelism design-space exploration; AMD Virtex-7; up to 8.37x area-time-product improvement; omitted curve, timing, energy and security conditions.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** state-of-the-art lightweight ECPM hardware accelerators

curve-specific ECPM designs

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH2824&sess=sess174

**Hardware or process assumptions:** Area-constrained IoT cryptographic accelerator with flexible modular arithmetic; FPGA implementation and ISA integration details are unspecified.

**Limits:** The description omits absolute area, latency, energy, frequency, curve coverage, and software overhead.

Flexibility may trade peak performance against dedicated curve accelerators.

Official description only; cryptographic hardware claims require paper-level verification.

**Method or artifact:** Unified ISA extension and microarchitecture with bit-width decomposition and design-space exploration over resource parallelism.

**Metrics:** Up to 8.37x area-time-product improvement on AMD Virtex-7

**Problem:** Curve-specific ECPM accelerators do not scale across field parameters and force redesigns for multi-curve IoT cryptography.

**Workload or benchmark:** ECPM for multiple elliptic curves on AMD Virtex-7 FPGA; curve set, frequency, resource use, security checks, and baseline implementations are unspecified.

</details>

<span id="paper-dac-2026-research1409"></span>

### CODA: A Computation-Data Decoupled Dataflow Paradigm for DNN Computing on NPUs

DAC 2026 · Record: `dac-2026-research1409`

[Read the step-by-step explanation](#explanation-dac-2026-research1409)

**Updated source-backed reading card**

Reviewed 2026-09-08. Reconciles the CODA card with the captured official DAC description; explains the difference between an operator's computation schedule and tensor data movement, non-uniform loop-space mapping, memory-hierarchy constraints and the gap between mapping expressiveness and measured NPU performance.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

When computation and tensor movement are forced to use coupled loop and storage choices, an NPU may be unable to exploit a memory hierarchy whose buffers, bandwidth and reuse opportunities differ across tensors and operators.

**Mechanism / artifact:**

CODA computation-data decoupled dataflow representation with tensor-wise mapping and non-uniform loop-space modeling; exact mapping grammar, compiler search procedure, legality constraints and generated hardware schedule are unavailable in the captured description.

**Workload — the work tested:**

DNN operators mapped to NPUs; operator set, tensor shapes, batch, precision, memory hierarchy, data reuse, search cost, baselines and end-to-end model coverage are unspecified.

**Hardware and manufacturing assumptions:**

NPU with hierarchical on-chip memory and configurable tensor movement; buffer capacities, bandwidth, number of processing elements, interconnect, execution model, clock, area and energy boundary are unspecified.

**Baseline — the comparison method:**

Computation-data coupled dataflow models

Operator shapes, memory hierarchy, precision, mapping legality, compiler/search budget and performance boundary are unspecified

**Reported measurements:**

The official description qualitatively claims expanded mapping expressiveness; latency, energy, area, search time, compile time and benchmark results are not reported.

**Limits on the conclusion:**

A DNN operator has an iteration space over dimensions such as batch, channels, spatial positions and reduction indices. A dataflow chooses which dimensions are tiled, parallelized, reused and stored at each memory level; this schedule determines both arithmetic work and tensor traffic.

Computation and data movement are related but not identical. The operation schedule determines when partial sums and operands are needed, while the storage/movement schedule determines where each tensor tile resides and how it reaches the processing elements. Decoupling can represent choices that a coupled model cannot, but the two schedules must still satisfy dependencies, capacity, bandwidth and ordering constraints.

Non-uniform loop-space modeling can allow different tensors or loop dimensions to use different tiling, placement and movement choices. That larger legal space can expose better mappings, but it also increases compiler search, legality checking, cost-model accuracy and schedule representation requirements.

The official description reports no latency, energy, area, search cost, compile time or benchmark coverage. Expanded mapping expressiveness is therefore a modeling capability, not evidence of an NPU speedup or energy reduction; any benefit remains dependent on operator shapes, hardware hierarchy, cost model and generated schedule.

**Source and location**

Evidence tier: Primary captured official DAC description only; no full paper extraction, compiler/artifact reproduction or independent schedule legality, search cost, npu performance and energy validation. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH1409&sess=sess110)

DAC 2026 official description and data/review-packets/dac-2026-research1409.json: computation-data decoupled representation; tensor-wise mapping; non-uniform loop-space modeling; NPU hierarchical memory; qualitative mapping-expressiveness claim; omitted latency, energy, area, search and benchmark conditions.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** computation-data coupled dataflow models

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH1409&sess=sess110

**Hardware or process assumptions:** NPU with hierarchical on-chip memory and configurable tensor movement; buffer sizes, bandwidth, and execution model are unspecified.

**Limits:** The description omits latency, energy, area, search cost, and benchmark coverage.

A larger mapping space may increase compiler/search complexity.

Official description only; accelerator claims require paper-level evaluation.

**Method or artifact:** Computation-data decoupled dataflow representation with tensor-wise mapping and non-uniform loop-space modeling.

**Metrics:** Expanded mapping expressiveness claimed qualitatively

**Problem:** Coupled computation-data dataflows force tensors to share storage structures and paths, limiting mappings as NPU memory hierarchies become complex.

**Workload or benchmark:** DNN operators mapped to NPUs; workloads, hardware hierarchy, search method, and performance baselines are unspecified.

</details>

<span id="paper-dac-2026-research1837"></span>

### Factored Floating-Point MAC: Eliminating Redundant Normalization for Energy-Efficient Systolic Arrays

DAC 2026 · Record: `dac-2026-research1837`

[Read the step-by-step explanation](#explanation-dac-2026-research1837)

**Updated source-backed reading card**

Reviewed 2026-09-08. Reconciles the Factored-FPMAC card with the captured official DAC description; explains floating-point normalization, rounding, carry-save accumulation, deferred post-processing and the numerical/PPA evidence boundary.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

A conventional floating-point FMA in a long GEMM or systolic accumulation repeatedly aligns, normalizes and rounds intermediate results, adding delay, energy and opportunities for rounding error.

**Mechanism / artifact:**

Factored floating-point MAC using 4:2 carry-save adders and a redundant floating-point representation inside the systolic array, with normalization deferred to unified post-processing; exact exponent/significand representation and post-processing pipeline are unavailable in the captured description.

**Workload — the work tested:**

Floating-point systolic-array GEMM and related scientific/ML workloads; precision, matrix dimensions, accumulation length, numerical-error metric, sparsity, workload mix and baseline implementation are unspecified.

**Hardware and manufacturing assumptions:**

Systolic array with 4:2 CSAs, redundant floating-point accumulation and unified normalization; process, frequency, pipeline depth, array size, buffer/memory system, rounding mode, overflow handling and post-processing hardware are unspecified.

**Baseline — the comparison method:**

IEEE-754 floating-point FMA systolic arrays

Precision, dimensions, accumulation order, rounding mode, process, frequency, memory boundary and PPA accounting are unspecified

**Reported measurements:**

The official description qualitatively claims removal of redundant normalization and wide carry-propagate adders, with qualitative numerical and energy benefits; no numerical accuracy, latency, area, power, frequency or workload result is reported.

**Limits on the conclusion:**

A floating-point value separates sign, exponent and significand. Before values can be added, their exponents must be aligned; after addition, the significand may need shifting and the exponent adjusted. Rounding then discards information according to a defined mode. Repeating this process inside every MAC can add hardware and change the accumulation path.

A carry-save representation keeps multiple partial-sum components instead of propagating every carry after each addition. A 4:2 carry-save adder can compress several operand rows into fewer rows without immediately resolving all carries. This can shorten the local critical path, but the saved carry state still requires storage, routing and a final carry resolution.

Deferred normalization changes when exponent alignment, significand normalization, rounding, overflow and exceptional-value handling occur. It can remove repeated work only if the redundant representation has enough range and precision to preserve every required intermediate, and if the unified post-processing step does not become the new bottleneck.

The official description reports no precision, error metric, rounding mode, overflow behavior, array dimensions, timing, area, power, process or workload results. The qualitative removal claim is therefore not evidence of numerical equivalence or energy/PPA improvement; bit-accurate comparison against IEEE-754 FMA and complete post-processing measurement are required.

**Source and location**

Evidence tier: Primary captured official DAC description only; no full paper extraction, bit accurate model, RTL/FPGA/asic artifact reproduction or independent numerical, timing, area and energy validation. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH1837&sess=sess130)

DAC 2026 official description and data/review-packets/dac-2026-research1837.json: 4:2 CSAs; redundant floating-point representation; deferred unified normalization; IEEE-754 FMA systolic baseline; qualitative removal and numerical/energy claims; omitted precision, error, PPA and workload conditions.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** IEEE-754 floating-point FMA systolic arrays

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH1837&sess=sess130

**Hardware or process assumptions:** Systolic array using 4:2 CSAs and floating-point redundant representation; process, frequency, pipeline, and normalization hardware are unspecified.

**Limits:** The description omits precision/error, PPA, timing, area, and workload results.

Deferred normalization may affect overflow, rounding, and numerical reproducibility.

Official description only; arithmetic claims require bit-accurate and hardware verification.

**Method or artifact:** Factored floating-point MAC with carry-save accumulation and deferred unified normalization.

**Metrics:** Redundant normalization and CPA removal claimed qualitatively

Numerical and energy benefits claimed qualitatively

**Problem:** Conventional floating-point FMA in long GEMM chains repeats normalization and rounding, causing numerical error, delay, and energy overhead.

**Workload or benchmark:** Floating-point systolic-array GEMM and related scientific/ML workloads; precision, numerical error, area, power, and baselines are unspecified.

</details>

<span id="paper-dac-2026-research1374"></span>

### SpArC: Sparse Tensor Accelerator Compilation with Scheduling and Mapping

DAC 2026 · Record: `dac-2026-research1374`

[Read the step-by-step explanation](#explanation-dac-2026-research1374)

**Updated source-backed reading card**

Reviewed 2026-09-08. Reconciles the SpArC card with the captured official DAC description; explains sparse tensor representation, scheduling, mapping, load balance, metadata and memory effects, and bounds the compiler claim because no quantitative or hardware-target results are exposed.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Sparse tensor accelerators need schedules and mappings that skip zero work without creating metadata overhead, irregular memory traffic, idle processing elements or incorrect reductions.

**Mechanism / artifact:**

Compiler framework for sparse-tensor scheduling and accelerator mapping on programmable sparse dataflows; exact sparse formats, intermediate representation, cost model, legality rules and generated code are unavailable in the captured description.

**Workload — the work tested:**

Sparse tensor and DNN workloads; tensor shapes, sparsity distributions, structured/unstructured format, density, accelerator targets, precision, baselines and end-to-end model coverage are unspecified.

**Hardware and manufacturing assumptions:**

Sparse accelerator with programmable dataflow and hierarchical memory; processing-element topology, supported formats, metadata storage, interconnect, buffer capacities, bandwidth, clock and execution model are unspecified.

**Baseline — the comparison method:**

Dense accelerator mapping

Existing sparse tensor compilers

Sparse format, accelerator topology, precision, correctness, compile budget, runtime boundary and energy accounting are unspecified

**Reported measurements:**

The official description qualitatively claims sparse compilation and mapping efficiency; speedup, energy, compile time, sparsity coverage and absolute execution results are not reported.

**Limits on the conclusion:**

Sparse computation stores or processes only selected tensor elements, but the accelerator must also represent where those elements occur. Index metadata, compressed rows or tiles, pointer traversal and decompression consume storage, bandwidth and control; skipping arithmetic does not imply skipping all work.

Scheduling assigns sparse work to time slots and processing elements. Mapping assigns tensors, tiles, metadata and partial sums to hardware resources and memory levels. Irregular nonzero counts can leave some resources idle or create reduction and synchronization bottlenecks even when the total arithmetic count is low.

A compiler cost model must represent the chosen sparse format, metadata traffic, load imbalance, buffer capacity, address generation, interconnect contention, reduction order and supported accelerator operations. A mapping that is legal for one topology or format may be invalid or slow for another.

The official description reports no speedup, energy, compile time, sparsity coverage, hardware topology, format, precision or correctness result. Qualitative compilation efficiency therefore establishes a compiler direction, not a demonstrated end-to-end sparse accelerator gain; benefits remain format- and accelerator-specific.

**Source and location**

Evidence tier: Primary captured official DAC description only; no full paper extraction, compiler/artifact reproduction or independent sparse format, schedule legality, performance, energy and end to end validation. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH1374&sess=sess147)

DAC 2026 official description and data/review-packets/dac-2026-research1374.json: sparse-tensor scheduling and accelerator mapping; programmable dataflow and memory hierarchy; dense mapping and existing sparse compilers as baseline categories; qualitative efficiency claim; omitted speedup, energy, compile, format and hardware conditions.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** dense accelerator mapping

existing sparse tensor compilers

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH1374&sess=sess147

**Hardware or process assumptions:** Sparse accelerator with programmable dataflow and memory hierarchy; hardware topology and supported formats are unspecified.

**Limits:** The description omits speedup, energy, compile time, sparsity coverage, and hardware details.

Results may depend on sparse format and accelerator-specific assumptions.

Official description only; compiler claims require end-to-end evaluation.

**Method or artifact:** Compiler framework for sparse-tensor scheduling and accelerator mapping.

**Metrics:** Sparse compilation and mapping efficiency are claimed qualitatively

**Problem:** Sparse tensor accelerators require coordinated scheduling and mapping to exploit irregularity without excessive load imbalance or data movement.

**Workload or benchmark:** Sparse tensor and DNN workloads; sparsity formats, accelerator targets, baselines, and measurements are unspecified.

</details>

<span id="paper-dac-2026-research1942"></span>

### PD-Swap: Prefill–decode Logic Swapping for End-to-End LLM Inference on Edge FPGAs via Dynamic Partial Reconfiguration

DAC 2026 · Record: `dac-2026-research1942`

[Read the step-by-step explanation](#explanation-dac-2026-research1942)

**Updated source-backed reading card**

Reviewed 2026-09-08. Reconciles the PD-Swap card with the captured official DAC description; explains the different resource patterns of LLM prefill and decode, dynamic partial reconfiguration, state preservation and the boundary between phase-level specialization and end-to-end inference efficiency.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

LLM prefill processes many input tokens with high parallel throughput, while decode generates one or a small number of tokens repeatedly with large key-value-cache and latency demands; a static FPGA datapath may provision resources poorly across the two phases.

**Mechanism / artifact:**

Dynamic partial reconfiguration that swaps phase-specific prefill and decode logic on an edge FPGA; bitstream partition, state-transfer method, reconfiguration controller and overlap with inference are unavailable in the captured description.

**Workload — the work tested:**

End-to-end edge-FPGA LLM inference; model, prompt lengths, generated lengths, batch/concurrency, quality target, bitstream size, reconfiguration frequency and baseline implementations are unspecified.

**Hardware and manufacturing assumptions:**

Edge FPGA supporting dynamic partial reconfiguration and phase-specific accelerator regions; FPGA family, static/reconfigurable partition, memory capacity/bandwidth, clock, host interface, power and configuration-memory behavior are unspecified.

**Baseline — the comparison method:**

Static FPGA accelerator

Single shared prefill/decode datapath

Model, sequence lengths, concurrency, memory, FPGA, reconfiguration, quality, throughput and energy boundaries are unspecified

**Reported measurements:**

The official description qualitatively claims end-to-end inference efficiency; reconfiguration latency, token latency, throughput, energy, area, resource utilization and accuracy are not reported.

**Limits on the conclusion:**

Prefill consumes the prompt in parallel and is commonly limited by matrix throughput and available parallel resources. Decode generates tokens sequentially and repeatedly reads or updates the key-value cache, so its bottleneck can be memory bandwidth, latency or cache capacity rather than the same arithmetic throughput.

Dynamic partial reconfiguration changes logic in a region while the rest of the FPGA remains available. The system must load a partial bitstream, pause or isolate affected interfaces, preserve model weights and cache state, reestablish timing and resume execution. Configuration time, bitstream storage and power belong to the phase transition cost.

The benefit depends on how often requests cross between phases and whether reconfiguration can overlap with useful work. Short prompts, short generations, interleaved requests or concurrent users can make repeated swapping more expensive than the resources saved by specialization.

The official description reports no reconfiguration overhead, latency, throughput, energy, area, utilization, model, sequence lengths or accuracy. The qualitative end-to-end efficiency claim therefore does not establish a measured FPGA advantage; runtime, bitstream and state-transfer data are required.

**Source and location**

Evidence tier: Primary captured official DAC description only; no full paper extraction, partial bitstream/runtime artifact reproduction or independent FPGA, state transfer, latency, energy and quality validation. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH1942&sess=sess175)

DAC 2026 official description and data/review-packets/dac-2026-research1942.json: prefill/decode phase-specific FPGA logic; dynamic partial reconfiguration; static/shared baselines; qualitative end-to-end efficiency claim; omitted reconfiguration, model, latency, throughput, energy, area and accuracy conditions.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** static FPGA accelerator

single shared prefill/decode datapath

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH1942&sess=sess175

**Hardware or process assumptions:** Edge FPGA supporting dynamic partial reconfiguration and phase-specific accelerator regions; device and memory details are unspecified.

**Limits:** The description omits reconfiguration overhead, latency, throughput, energy, area, and accuracy.

Frequent phase swapping may negate gains for short requests.

Official description only; FPGA claims require measured bitstream and runtime data.

**Method or artifact:** Dynamic partial reconfiguration that swaps phase-specific prefill and decode FPGA logic.

**Metrics:** End-to-end inference efficiency is claimed qualitatively

**Problem:** Prefill and decode phases have different resource and throughput needs, making static FPGA provisioning inefficient.

**Workload or benchmark:** End-to-end edge FPGA LLM inference; model, bitstream size, reconfiguration latency, and baselines are unspecified.

</details>

<span id="paper-dac-2026-research121"></span>

### Exquant: Global Expert Ranking–guided Mixed-Precision Quantization for Efficient MoE Inference

DAC 2026 · Record: `dac-2026-research121`

[Read the step-by-step explanation](#explanation-dac-2026-research121)

**Updated source-backed reading card**

Reviewed 2026-09-08. Reconciles the Exquant card with the captured official DAC description; explains MoE routing and expert usage, global ranking, layer/weight precision assignment, calibration error and the distinction between quality retention and serving-system cost.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Mixture-of-experts models activate only selected experts for each token, creating uneven expert use and a large parameter footprint; quantization must reduce storage and arithmetic cost without damaging the experts and routes that matter for the workload.

**Mechanism / artifact:**

Global expert-ranking-guided mixed-precision quantization; exact ranking statistic, calibration set, bit-width choices, layer granularity, scale/zero-point handling and deployment kernels are unavailable in the captured description.

**Workload — the work tested:**

MoE LLM inference; model family, expert count, top-k routing, bit widths, calibration and evaluation traces, sequence lengths, batch/concurrency, perplexity/task metrics and baselines are unspecified.

**Hardware and manufacturing assumptions:**

GPU or specialized MoE accelerator supporting mixed precision; weight layout, dequantization path, tensor-core/integer support, memory capacity/bandwidth, routing communication and energy boundary are unspecified.

**Baseline — the comparison method:**

Uniform quantization

Expert-oblivious mixed precision

Model, routing traces, bit budget, calibration, kernel support, quality metric, latency, memory and energy boundaries are unspecified

**Reported measurements:**

The official description qualitatively claims MoE efficiency and quality retention; no perplexity, task accuracy, latency, energy, memory, model or absolute compression result is reported.

**Limits on the conclusion:**

An MoE layer routes each token to a selected subset of experts. Expert frequency can be measured globally, but a frequently used expert is not necessarily equally sensitive in every layer, token type or task; ranking usage and ranking quantization vulnerability are different measurements.

Mixed precision assigns different bit widths to weights, activations or layers. Lower precision reduces storage and can reduce arithmetic cost, but it changes quantization error, scaling, accumulation and kernel selection. The total model bit budget and the locations receiving each precision must be stated.

A global ranking is computed from a calibration distribution. Routing distributions can shift with prompts, domains, sequence phase, batch composition and model updates. A stale ranking can allocate high precision to experts that are no longer important and low precision to experts that become sensitive.

The official description reports no model, bit widths, perplexity, task accuracy, latency, energy, memory, routing trace or kernel result. Qualitative quality retention and efficiency therefore do not establish a serving benefit; workload-diverse calibration and complete mixed-precision execution measurements are required.

**Source and location**

Evidence tier: Primary captured official DAC description only; no full paper extraction, calibration/routing trace reproduction or independent quality, kernel, memory, latency and energy validation. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH121)

DAC 2026 official description and data/review-packets/dac-2026-research121.json: global expert ranking; mixed-precision quantization; MoE inference; uniform/expert-oblivious baselines; qualitative efficiency/quality claim; omitted model, precision, accuracy, latency, memory and energy conditions.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** uniform quantization

expert-oblivious mixed precision

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH121

**Hardware or process assumptions:** GPU or specialized MoE accelerator with mixed-precision support; memory and bandwidth assumptions are unspecified.

**Limits:** No perplexity, task accuracy, latency, energy, memory, or model results are reported.

Ranking can become stale as routing distributions shift.

Official description only; workload-diverse evaluation is required.

**Method or artifact:** Global expert-ranking-guided mixed-precision quantization.

**Metrics:** MoE efficiency and quality retention are claimed qualitatively

**Problem:** Mixture-of-experts models require efficient quantization while preserving quality across unevenly used experts.

**Workload or benchmark:** MoE LLM inference; models, bit widths, routing traces, and baselines are unspecified.

</details>

<span id="paper-dac-2026-research1338"></span>

### ZK-Tracer: A High-Performance Heterogeneous Accelerator for Zero-Knowledge VM Trace Generation

DAC 2026 · Record: `dac-2026-research1338`

[Read the step-by-step explanation](#explanation-dac-2026-research1338)

**Updated source-backed reading card**

Reviewed 2026-09-08. Reconciles the ZK-Tracer card with the captured official DAC description; explains virtual-machine execution traces, their role in zero-knowledge proving, heterogeneous division of work and the boundary between trace throughput and complete proof generation.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

A zero-knowledge virtual machine must execute a program and record the state transitions or trace needed by a prover; producing and moving that trace can dominate proving time and memory traffic.

**Mechanism / artifact:**

Heterogeneous accelerator for zero-knowledge VM trace generation, described as CPU/FPGA/ASIC-like components with large memory movement; exact trace format, processor partition, scheduling, memory organization and proof-system interface are unavailable in the captured description.

**Workload — the work tested:**

Zero-knowledge VM programs and execution traces; VM instruction set, program lengths, branch behavior, witness size, proving system, trace width, hardware target, memory traffic and baseline implementations are unspecified.

**Hardware and manufacturing assumptions:**

Heterogeneous CPU/FPGA/ASIC-like accelerator with substantial trace storage and movement; device technology, interconnect, memory capacity/bandwidth, consistency protocol, clock, area and energy boundary are unspecified.

**Baseline — the comparison method:**

CPU trace generation

Homogeneous ZK accelerator

VM program, trace format, proving system, hardware, memory, correctness, throughput and end-to-end proof boundaries are unspecified

**Reported measurements:**

The official description qualitatively claims trace-generation throughput and efficiency; trace rate, proof latency, energy, area, memory use and program coverage are not reported.

**Limits on the conclusion:**

A zero-knowledge VM executes a program while recording enough information about each relevant state transition for a prover to demonstrate correct execution without exposing the private witness. Trace generation is therefore a correctness-critical producer, not merely a log-writing task.

The trace is consumed by later proving stages such as constraint construction, polynomial processing, commitments or other proof-specific work. Its layout, width, ordering and consistency determine downstream memory traffic and proving cost; a faster trace producer can simply move the bottleneck to trace storage or proof construction.

A heterogeneous design can assign regular arithmetic, control-heavy VM interpretation, trace packing and memory movement to different components. That can improve utilization only if partition boundaries, synchronization, state transfer and ordering preserve the VM semantics. Large trace movement may dominate the benefit of specialized arithmetic.

The official description reports no trace rate, proof latency, energy, area, memory, program coverage, proving system or trace distribution. The qualitative throughput claim therefore establishes an accelerator direction, not an end-to-end prover improvement or cryptographic security result.

**Source and location**

Evidence tier: Primary captured official DAC description only; no full paper extraction, trace/prover artifact reproduction or independent vm correctness, memory, performance, energy and end to end proof validation. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH1338)

DAC 2026 official description and data/review-packets/dac-2026-research1338.json: zero-knowledge VM trace generation; heterogeneous accelerator; CPU and homogeneous-ZK baselines; qualitative trace throughput/efficiency claim; omitted VM, proof, memory and hardware conditions.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** CPU trace generation

homogeneous ZK accelerator

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH1338

**Hardware or process assumptions:** Heterogeneous CPU/FPGA/ASIC-like accelerator with large memory movement; implementation assumptions are unspecified.

**Limits:** No trace rate, proof latency, energy, area, memory, or program coverage are reported.

Benefit depends on proving system and trace distribution.

Official description only; end-to-end prover validation is required.

**Method or artifact:** Heterogeneous accelerator for ZK VM trace generation.

**Metrics:** Trace-generation throughput and efficiency are claimed qualitatively

**Problem:** Trace generation is a major bottleneck in zero-knowledge virtual-machine proving.

**Workload or benchmark:** Zero-knowledge VM programs and traces; proof system, workloads, hardware, and baselines are unspecified.

</details>

<span id="paper-dac-2026-research1447"></span>

### STCG: Sparse Tensor Code Generation via Adaptive Tile Scheduling on GPUs with Tensor Cores

DAC 2026 · Record: `dac-2026-research1447`

[Read the step-by-step explanation](#explanation-dac-2026-research1447)

**Updated source-backed reading card**

Reviewed 2026-09-08. Reconciles the STCG card with the captured official DAC description; explains sparse tensor tiles, tensor-core utilization, adaptive scheduling, metadata and load imbalance, and bounds qualitative code-generation efficiency against complete GPU execution evidence.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

GPU tensor cores are optimized for regular dense tiles, while sparse tensors contain uneven nonzero patterns that can leave lanes idle, increase metadata work and create load imbalance.

**Mechanism / artifact:**

Sparse tensor code generation with adaptive tile scheduling for tensor-core GPUs; exact sparse format, tile representation, schedule selection, generated kernel and runtime adaptation mechanism are unavailable in the captured description.

**Workload — the work tested:**

Sparse tensor kernels on tensor-core GPUs; tensor dimensions, sparsity distribution and format, precision, GPU model, baseline kernels, compile budget and end-to-end model coverage are unspecified.

**Hardware and manufacturing assumptions:**

GPU with tensor cores and sparse memory access; tensor-core tile shape, warp mapping, memory hierarchy, metadata path, occupancy constraints, clock, compiler/runtime and energy boundary are unspecified.

**Baseline — the comparison method:**

Dense tensor-core kernels

Static sparse tiling

Sparse format, density, tensor shapes, precision, GPU, correctness, compile/runtime overhead and measurement boundary are unspecified

**Reported measurements:**

The official description qualitatively claims sparse-kernel efficiency; no speedup, occupancy, sparsity range, compilation time, runtime overhead, energy or model result is reported.

**Limits on the conclusion:**

A tensor core executes a fixed-shape block of matrix operations efficiently when lanes receive regular operands. Sparse tiles contain missing values and indices; the system must either pack nonzeros into supported shapes, execute masked work, or use a conversion path. The skipped arithmetic can be offset by metadata loads, packing, address generation and irregular memory access.

Tile scheduling assigns sparse tiles to warps or processing units. Adaptive scheduling can respond to nonzero counts or tile cost to reduce idle lanes, but it needs a cost estimate, queueing or runtime decisions, and a method for preserving output ownership and reductions.

Tensor-core occupancy depends on registers, shared memory, tile shape, warp count and outstanding memory operations. A schedule that improves nonzero balance can reduce occupancy or increase synchronization; a schedule that maximizes occupancy for one density pattern may fail for another format or shape.

The official description reports no speedup, occupancy, sparsity range, compilation time, runtime overhead, energy, GPU, format, precision or correctness result. Qualitative code-generation efficiency therefore does not establish a complete sparse-GPU gain; format-diverse and end-to-end measurements are required.

**Source and location**

Evidence tier: Primary captured official DAC description only; no full paper extraction, generated kernel/artifact reproduction or independent format diverse, occupancy, correctness, performance and energy validation. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH1447)

DAC 2026 official description and data/review-packets/dac-2026-research1447.json: sparse tensor code generation; adaptive tile scheduling; tensor-core GPU; dense and static sparse baselines; qualitative efficiency claim; omitted speed, occupancy, sparsity, compilation, energy and format conditions.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** dense tensor-core kernels

static sparse tiling

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH1447

**Hardware or process assumptions:** GPU with tensor cores and sparse memory access; generation/runtime assumptions are unspecified.

**Limits:** No speedup, occupancy, sparsity range, compilation time, or energy results are reported.

Adaptive schedules may add runtime or compile overhead.

Official description only; format-diverse evaluation is required.

**Method or artifact:** Sparse tensor code generation with adaptive tile scheduling.

**Metrics:** Sparse-kernel efficiency is claimed qualitatively

**Problem:** GPU tensor cores favor dense tiles while sparse tensors create irregular work and load imbalance.

**Workload or benchmark:** Sparse tensor kernels on tensor-core GPUs; formats, sparsity, and baselines are unspecified.

</details>

<span id="paper-dac-2026-research2504"></span>

### EASY-ZKP: An End-to-End FPGA-Accelerated System for Zero Knowledge Proofs

DAC 2026 · Record: `dac-2026-research2504`

[Read the step-by-step explanation](#explanation-dac-2026-research2504)

**Updated source-backed reading card**

Reviewed 2026-09-08. Reconciles the EASY-ZKP card with the captured official DAC description; explains the stages of zero-knowledge proof generation, finite-field and memory bottlenecks, FPGA host/device boundaries and what end-to-end evidence must include.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Zero-knowledge proof generation combines large finite-field and cryptographic computations with substantial intermediate data movement, making practical latency and energy difficult on general-purpose processors.

**Mechanism / artifact:**

End-to-end FPGA acceleration system for zero-knowledge proofs with finite-field arithmetic and a memory hierarchy; exact proving system, kernels, host interface, dataflow, memory organization and FPGA implementation are unavailable in the captured description.

**Workload — the work tested:**

Zero-knowledge proof workloads and circuits; proof system, curve/field, circuit size, witness size, FPGA device, precision, proof phases and baselines are unspecified.

**Hardware and manufacturing assumptions:**

FPGA accelerator for finite-field arithmetic and proof-related memory movement; device family, clock, voltage, resource budget, external memory, host link, bitstream, power and configuration conditions are unspecified.

**Baseline — the comparison method:**

CPU/GPU zero-knowledge proving

Partial FPGA acceleration

Proof system, curve, circuit, host/device boundary, software version, correctness and resource/energy accounting are unspecified

**Reported measurements:**

The official description qualitatively claims proof-generation efficiency; proof latency, throughput, energy, area, memory use, circuit coverage and absolute results are not reported.

**Limits on the conclusion:**

A zero-knowledge prover transforms a circuit and witness into a proof through several stages. Depending on the proving system, these can include witness/trace processing, polynomial construction, finite-field transforms, commitments, group arithmetic, hashing, proof assembly and verification-related preparation. FPGA acceleration of one stage does not establish end-to-end proof speed.

Finite-field arithmetic is only one part of the data path. Large polynomials and intermediate vectors must be stored, reordered, streamed and sometimes transferred between FPGA memory, external memory and the host. Memory capacity, bandwidth, access pattern and synchronization can dominate even when arithmetic units are busy.

An end-to-end FPGA system must define which work remains on the CPU/GPU, how data crosses the host/device boundary, when buffers are copied, and whether transfers overlap computation. A partial accelerator comparison can look favorable while excluding the software, DMA, initialization, bitstream and proof-assembly costs that a complete prover pays.

The official description reports no proof latency, throughput, energy, area, memory, circuit coverage, curve, field, proof system, FPGA or host boundary. The qualitative efficiency claim therefore establishes a system direction, not a measured universal ZK-proving advantage or reproducible end-to-end result.

**Source and location**

Evidence tier: Primary captured official DAC description only; no full paper extraction, FPGA/prover artifact reproduction or independent correctness, performance, memory, energy and end to end validation. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH2504)

DAC 2026 official description and data/review-packets/dac-2026-research2504.json: end-to-end FPGA zero-knowledge-proof acceleration; finite-field arithmetic and memory hierarchy; CPU/GPU and partial-FPGA baselines; qualitative proof-generation efficiency claim; omitted proof, circuit, device and resource conditions.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** CPU/GPU ZK proving

partial FPGA acceleration

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH2504

**Hardware or process assumptions:** FPGA accelerator with finite-field arithmetic and memory hierarchy; device and clock assumptions are unspecified.

**Limits:** No proof latency, throughput, energy, area, memory, or circuit coverage are reported.

Results depend strongly on curve and proof system.

Official description only; end-to-end reproducibility is required.

**Method or artifact:** End-to-end FPGA acceleration system for zero-knowledge proofs.

**Metrics:** Proof-generation efficiency is claimed qualitatively

**Problem:** ZK proof generation requires substantial arithmetic and memory bandwidth for practical applications.

**Workload or benchmark:** ZK proof workloads and circuits; proof system, FPGA, and baselines are unspecified.

</details>

<span id="paper-dac-2026-research1438"></span>

### PiHG: A Redundancy-Free Heterogeneous Graph Neural Network Accelerator via a Pivot-Centric Approach

DAC 2026 · Record: `dac-2026-research1438`

[Read the step-by-step explanation](#explanation-dac-2026-research1438)

**Updated source-backed reading card**

Reviewed 2026-09-08. Reconciles the PiHG card with the captured official DAC description; explains heterogeneous graph aggregation, pivot-centric reuse, relation types, irregular graph memory access and the need to preserve aggregation semantics when removing redundant work.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Heterogeneous GNNs aggregate messages across typed nodes and relations, creating repeated work and irregular feature/edge movement; redundant aggregation can waste compute while graph structure makes memory access difficult to regularize.

**Mechanism / artifact:**

Pivot-centric redundancy-free heterogeneous GNN accelerator; exact pivot definition, relation scheduling, aggregation transformation, memory hierarchy, processing elements and correctness conditions are unavailable in the captured description.

**Workload — the work tested:**

Heterogeneous graph workloads; node/edge types, relation count, graph size, degree distribution, GNN layers, aggregation semantics, datasets, feature dimension, precision and baselines are unspecified.

**Hardware and manufacturing assumptions:**

GNN accelerator with graph memory and irregular-access support; processing-element topology, feature/edge storage, interconnect, cache/buffer capacity, precision, clock and energy boundary are unspecified.

**Baseline — the comparison method:**

General-purpose GNN accelerator

Redundant heterogeneous aggregation

Graph datasets, relation semantics, precision, hardware, memory, correctness, latency and energy boundaries are unspecified

**Reported measurements:**

The official description qualitatively claims GNN efficiency; no speedup, energy, accuracy, memory, graph-scale, utilization or absolute result is reported.

**Limits on the conclusion:**

A heterogeneous GNN represents different node and edge types or relation semantics. A layer aggregates neighbor features according to those types and then applies learned transformations. Removing repeated work is valid only when two computations have the same inputs, relation semantics, weights, normalization and update timing.

A pivot-centric method can choose a shared node, feature, relation or intermediate as a reuse point, but the pivot must preserve which neighbors contribute to which destination and how typed messages are combined. Reusing a partial result across relations that only look similar can change the model function.

Graph execution is irregular: adjacency lists, feature vectors and relation metadata are often accessed in different orders, and high-degree nodes can create hotspots or reduction conflicts. A redundancy-free arithmetic path can still be limited by graph memory bandwidth, address generation, synchronization and partial-sum storage.

The official description reports no speedup, energy, accuracy, memory, graph scale, relation set, dataset, hardware or aggregation proof. The qualitative efficiency claim therefore establishes a proposed reuse strategy, not a demonstrated heterogeneous-GNN improvement; dataset-diverse and semantic-equivalence validation are required.

**Source and location**

Evidence tier: Primary captured official DAC description only; no full paper extraction, accelerator/artifact reproduction or independent aggregation equivalence, dataset diverse, performance, memory and energy validation. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH1438)

DAC 2026 official description and data/review-packets/dac-2026-research1438.json: pivot-centric redundancy-free heterogeneous GNN accelerator; general-purpose and redundant-aggregation baselines; qualitative GNN efficiency claim; omitted graph, relation, hardware, accuracy, speed and energy conditions.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** general-purpose GNN accelerator

redundant heterogeneous aggregation

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH1438

**Hardware or process assumptions:** GNN accelerator with graph memory and irregular access support; precision and interconnect assumptions are unspecified.

**Limits:** No speedup, energy, accuracy, memory, or graph-scale results are reported.

Removing redundancy may alter aggregation semantics.

Official description only; dataset-diverse validation is required.

**Method or artifact:** Pivot-centric redundancy-free heterogeneous GNN accelerator.

**Metrics:** GNN efficiency is claimed qualitatively

**Problem:** Heterogeneous GNNs incur redundant aggregation and irregular data movement.

**Workload or benchmark:** Heterogeneous graph workloads; datasets, aggregation semantics, hardware, and baselines are unspecified.

</details>

<span id="paper-dac-2026-research200"></span>

### Ternainfer: Pushing the Compression Boundary of Ternary LLMs Towards 1.58-Bit GPU Inference

DAC 2026 · Record: `dac-2026-research200`

[Read the step-by-step explanation](#explanation-dac-2026-research200)

**Updated source-backed reading card**

Reviewed 2026-09-08. Reconciles the Ternainfer card with the captured official DAC description; explains ternary weight representation, why 1.58 bits is an information-theoretic average, packing and GPU kernel requirements, and the separation between compression, accuracy and serving throughput.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

LLM weight storage and matrix arithmetic remain expensive after 8-bit or 4-bit quantization; ternary weights can reduce the number of representable states and stored bits but require appropriate training, packing and execution support.

**Mechanism / artifact:**

GPU inference stack for ternary approximately 1.58-bit LLM weights, including custom low-bit arithmetic and packing; exact ternary encoding, scaling, kernels, accumulation precision and supported GPU instructions are unavailable in the captured description.

**Workload — the work tested:**

Ternary LLM inference; model family, parameter count, layer coverage, calibration/retraining method, sequence lengths, batch/concurrency, kernels, output quality metrics and baselines are unspecified.

**Hardware and manufacturing assumptions:**

GPU with custom low-bit arithmetic and packed ternary weights; tensor-core or SIMD path, unpack/decode overhead, memory hierarchy, instruction support, clock, energy and activation/KV-cache precision are unspecified.

**Baseline — the comparison method:**

8-bit/4-bit GPU inference

Dense floating-point inference

Model, quality target, weight/activation/KV precision, kernel, GPU, batch, sequence length, memory and energy boundaries are unspecified

**Reported measurements:**

The official description qualitatively claims compression and inference efficiency; no perplexity, task accuracy, throughput, energy, memory, compression ratio or kernel result is reported.

**Limits on the conclusion:**

A ternary weight takes one of three values, often represented as negative, zero or positive, with a scale or group scale restoring magnitude. Three states require log2(3), approximately 1.585, bits per weight in an ideal entropy-balanced representation; practical packing adds code boundaries, scales, alignment and metadata.

Low-bit storage does not automatically produce low-cost GPU arithmetic. The kernel must unpack or decode ternary codes, apply scales, handle zeros, accumulate products at sufficient precision and feed the GPU's supported execution units. Unpacking and irregular bit operations can consume the memory and arithmetic savings.

Ternary quantization changes the model's weight values and may require quantization-aware training, retraining or a model specifically optimized for ternary weights. Quality must be measured against the same model, data, task, generation settings and precision treatment; compression alone does not establish useful LLM behavior.

The official description reports no model, encoding, bit budget, perplexity, task accuracy, throughput, energy, memory, GPU, kernel or activation/KV-cache conditions. The qualitative efficiency claim therefore establishes a ternary-inference direction, not a measured universal GPU speedup or quality-preserving compression result.

**Source and location**

Evidence tier: Primary captured official DAC description only; no full paper extraction, ternary training/kernel artifact reproduction or independent model diverse quality, packing, throughput, memory and energy validation. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH200)

DAC 2026 official description and data/review-packets/dac-2026-research200.json: ternary approximately 1.58-bit GPU LLM inference; custom low-bit arithmetic and packing; 8/4-bit and dense baselines; qualitative compression/efficiency claim; omitted model, quality, kernel, throughput and memory conditions.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** 8-bit/4-bit GPU inference

dense floating-point inference

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH200

**Hardware or process assumptions:** GPU with custom low-bit arithmetic and packing; supported instructions and memory assumptions are unspecified.

**Limits:** No perplexity, task accuracy, throughput, energy, memory, or kernel results are reported.

Ternary quantization may require retraining or limit model quality.

Official description only; model-diverse benchmarking is required.

**Method or artifact:** GPU inference stack for ternary approximately 1.58-bit LLM weights.

**Metrics:** Compression and inference efficiency are claimed qualitatively

**Problem:** LLM memory and arithmetic cost remain high even after conventional low-bit quantization.

**Workload or benchmark:** Ternary LLM inference; models, kernels, packing, and baselines are unspecified.

</details>

<span id="paper-dac-2026-research2125"></span>

### Overmind NSA: A Unified Neuro-Symbolic Computing Architecture with Approximate Nonlinear Activations and Preemptive Memory Bypass

DAC 2026 · Record: `dac-2026-research2125`

[Read the step-by-step explanation](#explanation-dac-2026-research2125)

**Updated source-backed reading card**

Reviewed 2026-09-08. Reconciles the Overmind NSA card with the captured official DAC description; explains neural versus symbolic computation, approximate nonlinear activation error, preemptive memory bypass and the correctness/quality boundary of a unified accelerator.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Neuro-symbolic workloads combine learned numerical computation with rule, search or discrete symbolic operations, creating different control, precision and memory behavior that separate accelerators may handle inefficiently.

**Mechanism / artifact:**

Unified neuro-symbolic architecture with approximate nonlinear activations and preemptive memory bypass; exact neural/symbolic interfaces, approximation functions, bypass trigger, state handling and microarchitecture are unavailable in the captured description.

**Workload — the work tested:**

Neuro-symbolic applications; neural models, symbolic operators, data/control dependencies, tasks, precision, approximation-error metric, memory traces, hardware target and baselines are unspecified.

**Hardware and manufacturing assumptions:**

Heterogeneous neural/symbolic accelerator with approximate arithmetic and memory-bypass paths; processing elements, interconnect, buffers, bypass protocol, clock, area, energy and consistency assumptions are unspecified.

**Baseline — the comparison method:**

Separate neural and symbolic accelerators

Exact nonlinear execution

Application, symbolic semantics, model, approximation, memory, correctness, latency and energy boundaries are unspecified

**Reported measurements:**

The official description qualitatively claims neuro-symbolic efficiency; no task accuracy, latency, energy, area, approximation error, memory traffic or system result is reported.

**Limits on the conclusion:**

Neural computation usually tolerates bounded numerical error because the model is evaluated by a continuous quality metric. Symbolic computation often relies on exact comparisons, predicates, indices, discrete states or proof-like rules. An approximation acceptable in an activation may change a symbolic branch or invalidate a discrete result.

A unified architecture must define the boundary between neural tensors and symbolic state: representation, precision, conversion, synchronization, control and error policy. Without that interface, combining the units does not show that data or control can flow efficiently or correctly.

Preemptive memory bypass can route a value around a normal buffer or memory level when the system predicts that storing and rereading it is more expensive than forwarding it. The bypass needs a trigger, capacity, ordering rule, arbitration and fallback; otherwise it can create contention, starvation, state inconsistency or extra control work.

The official description reports no task accuracy, latency, energy, area, approximation error, memory trace, symbolic correctness or application coverage. The qualitative efficiency claim therefore establishes a unified architecture direction, not a demonstrated neuro-symbolic benefit; application-diverse exactness and quality evaluation are required.

**Source and location**

Evidence tier: Primary captured official DAC description only; no full paper extraction, hardware/artifact reproduction or independent neural quality, symbolic correctness, memory, performance and energy validation. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH2125)

DAC 2026 official description and data/review-packets/dac-2026-research2125.json: unified neuro-symbolic architecture; approximate nonlinear activations; preemptive memory bypass; separate neural/symbolic and exact baselines; qualitative efficiency claim; omitted task, correctness, approximation, latency and energy conditions.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** separate neural and symbolic accelerators

exact nonlinear execution

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH2125

**Hardware or process assumptions:** Heterogeneous neural/symbolic accelerator with approximate arithmetic and bypass paths; assumptions are unspecified.

**Limits:** No task accuracy, latency, energy, area, or approximation-error results are reported.

Approximation may affect symbolic correctness.

Official description only; application-diverse validation is required.

**Method or artifact:** Unified neuro-symbolic architecture with approximate activations and memory bypass.

**Metrics:** Neuro-symbolic efficiency is claimed qualitatively

**Problem:** Neuro-symbolic workloads combine irregular symbolic operations with neural compute and memory bottlenecks.

**Workload or benchmark:** Neuro-symbolic applications; symbolic operators, models, hardware, and baselines are unspecified.

</details>

<span id="paper-dac-2026-research2698"></span>

### BiBNN: 88.6% Computation Reduction in Bayesian Neural Networks via Post-Training Bernoullization

DAC 2026 · Record: `dac-2026-research2698`

[Read the step-by-step explanation](#explanation-dac-2026-research2698)

**Updated source-backed reading card**

Reviewed 2026-09-08. Reconciles the BiBNN card with the captured official DAC description; explains Bayesian predictive uncertainty, Bernoulli sampling/representation, post-training conversion, computation-count boundaries and uncertainty calibration requirements.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Bayesian neural networks represent uncertainty over model parameters or predictions, but estimating that uncertainty can require multiple stochastic samples and repeated neural computation.

**Mechanism / artifact:**

Post-training Bernoullization for lower-cost Bayesian inference; exact conversion rule, Bernoulli variables, sampling schedule, hardware mapping and whether weights/activations or masks are randomized are unavailable in the captured description.

**Workload — the work tested:**

Bayesian neural-network inference; models, datasets, posterior approximation, number of samples, uncertainty metrics, calibration method, hardware and deterministic/Bayesian baselines are unspecified.

**Hardware and manufacturing assumptions:**

Binary or probabilistic inference accelerator or GPU; bit precision, random-number generation, sample reuse, memory layout, kernel support, clock, energy and hardware boundary are unspecified.

**Baseline — the comparison method:**

Full Bayesian inference

Deterministic neural approximation

Model, posterior, sample count, accuracy/uncertainty target, hardware, random source and computation-count boundary are unspecified

**Reported measurements:**

The title claims 88.6% computation reduction; the official record does not expose the counted operations, model, sample count, hardware, accuracy or uncertainty conditions.

**Limits on the conclusion:**

A Bayesian neural network can represent a distribution over parameters or predictions. Predictive uncertainty is estimated by combining outputs from multiple parameter samples or stochastic forward passes; the mean prediction and the spread of those outputs are different quantities.

Bernoullization maps a quantity or stochastic choice to Bernoulli behavior, but the exact conversion determines whether the method preserves the intended posterior, expectation, variance and correlations. Independent binary samples can have the right mean while losing dependencies that affect uncertainty.

Post-training conversion avoids retraining cost but may introduce approximation error relative to the original Bayesian model. Fewer or cheaper samples can reduce computation while changing accuracy, calibration, aleatoric/epistemic uncertainty separation and out-of-distribution behavior.

The 88.6% headline lacks the operation definition, model, posterior, sample count, hardware, random-number cost, accuracy, calibration, uncertainty metric and baseline conditions. It therefore establishes a claimed computation reduction, not preserved Bayesian uncertainty or a measured inference-system benefit; task and calibration evaluation are required.

**Source and location**

Evidence tier: Primary captured official DAC description only; no full paper extraction, bernoulli conversion/reproduction or independent accuracy, calibration, uncertainty, random generation, hardware and computation boundary validation. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH2698)

DAC 2026 official description and data/review-packets/dac-2026-research2698.json: post-training Bernoullization; Bayesian neural-network inference; full-Bayesian and deterministic baselines; title claim of 88.6% computation reduction; omitted model, uncertainty, hardware, sampling and operation-count conditions.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** full Bayesian inference

deterministic neural approximation

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH2698

**Hardware or process assumptions:** Binary/probabilistic inference accelerator or GPU; precision and sampling assumptions are unspecified.

**Limits:** The headline reduction lacks model, hardware, accuracy, uncertainty, and baseline conditions.

Bernoullization may distort calibrated uncertainty.

Official description only; task and calibration evaluation is required.

**Method or artifact:** Post-training Bernoullization for lower-cost Bayesian inference.

**Metrics:** 88.6% computation reduction claimed in the title

**Problem:** Bayesian neural networks provide uncertainty but incur high sampling and arithmetic cost.

**Workload or benchmark:** Bayesian neural-network inference; models, uncertainty metrics, hardware, and baselines are unspecified.

</details>

<span id="paper-dac-2026-research2897"></span>

### EXRA: Efficient Execution of Data-Dominated Applications via ISA Extensions for Expandable Register Files

DAC 2026 · Record: `dac-2026-research2897`

[Read the step-by-step explanation](#explanation-dac-2026-research2897)

**Updated source-backed reading card**

Reviewed 2026-09-08. Reconciles the EXRA card with the captured official DAC description; explains register pressure, expandable register-file state, ISA/compiler coordination, spill avoidance and the area/power/context-switch boundary.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Data-dominated applications repeatedly move values between registers, caches and memory; a conventional register file may force spills when live data exceeds available registers, increasing latency and bandwidth.

**Mechanism / artifact:**

ISA extensions and expandable register files for data-heavy execution; exact instruction semantics, register-file expansion mechanism, allocation policy, pipeline effects and compiler support are unavailable in the captured description.

**Workload — the work tested:**

Data-dominated application kernels; data footprint, live-value count, access reuse, control flow, ISA, compiler, processor, cache hierarchy, workloads and baselines are unspecified.

**Hardware and manufacturing assumptions:**

Processor with expandable register file and custom ISA; register-file ports, banks, access latency, expansion storage, pipeline, context-switch mechanism, area, power and memory hierarchy are unspecified.

**Baseline — the comparison method:**

Conventional ISA/register file

Memory-resident data movement

Processor, compiler, cache, register capacity, instruction schedule, correctness, area, power and workload boundaries are unspecified

**Reported measurements:**

The official description qualitatively claims execution efficiency; no performance, energy, area, compiler complexity, context-switch, register-use or workload result is reported.

**Limits on the conclusion:**

Register pressure occurs when the compiler must keep more live values than the physical register file can hold. It can spill values to a cache or memory and later reload them, adding instructions, address generation, bandwidth, latency and energy.

An expandable register file can keep more data close to the execution units, but larger storage may add read/write ports, banking, access latency, wakeup and bypass complexity. Expansion must preserve the architectural register state and define how instructions address the extra registers.

The ISA and compiler must agree on allocation, lifetime, calling convention, save/restore behavior, dependency tracking and fallback when the expanded file is unavailable or full. A hardware feature that reduces spills only for hand-written schedules may not improve compiled applications.

The official description reports no performance, energy, area, compiler complexity, context-switch cost, register-file configuration or workload result. Qualitative execution efficiency therefore establishes an ISA/memory-locality direction, not a demonstrated system gain; large register files may increase power and context-switch cost.

**Source and location**

Evidence tier: Primary captured official DAC description only; no full paper extraction, isa/compiler artifact reproduction or independent spill, context switch, timing, area, power and workload validation. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH2897)

DAC 2026 official description and data/review-packets/dac-2026-research2897.json: ISA extensions; expandable register files; data-dominated execution; conventional ISA/register and memory-movement baselines; qualitative efficiency claim; omitted performance, area, power, compiler and workload conditions.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** conventional ISA/register file

memory-resident data movement

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH2897

**Hardware or process assumptions:** Processor with expandable register file and custom ISA; pipeline, area, and software assumptions are unspecified.

**Limits:** No performance, energy, area, compiler complexity, or workload results are reported.

Large register files may increase context-switch and power cost.

Official description only; end-to-end compiler validation is required.

**Method or artifact:** ISA extensions and expandable register files for data-heavy execution.

**Metrics:** Execution efficiency is claimed qualitatively

**Problem:** Data-dominated applications suffer from register pressure and memory movement.

**Workload or benchmark:** Data-dominated application kernels; ISA, workloads, compiler, and baselines are unspecified.

</details>

<span id="paper-dac-2026-research3050"></span>

### Scalable and Adaptive Parallel Training of Graph Transformer on Large Graphs

DAC 2026 · Record: `dac-2026-research3050`

[Read the step-by-step explanation](#explanation-dac-2026-research3050)

**Updated source-backed reading card**

Reviewed 2026-09-08. Reconciles the adaptive graph-transformer training card with the captured official DAC description; explains graph-transformer attention, partition boundaries, feature/edge communication, adaptive scaling and the distinction between throughput scaling and converged training quality.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Graph transformers combine graph structure with attention over nodes or neighborhoods, creating large feature, attention and communication costs when training is distributed across devices.

**Mechanism / artifact:**

Scalable adaptive parallel-training framework for graph transformers with adaptive graph partitioning or scaling; exact attention scope, partition algorithm, communication schedule, consistency model and runtime controller are unavailable in the captured description.

**Workload — the work tested:**

Large graph-transformer models; graph sizes, degree/topology distributions, attention pattern, layers, feature dimensions, number of GPUs, interconnect, batch, partitioning, baselines and convergence protocol are unspecified.

**Hardware and manufacturing assumptions:**

Multi-GPU or distributed training system; device memory, interconnect bandwidth/latency, collective operations, partition storage, synchronization and consistency assumptions are unspecified.

**Baseline — the comparison method:**

Single-device graph-transformer training

Static distributed partitioning

Graph, model, GPU, interconnect, batch, precision, communication, quality and convergence boundaries are unspecified

**Reported measurements:**

The official description qualitatively claims training scalability and efficiency; throughput, convergence, accuracy, memory, communication volume, scale and energy results are not reported.

**Limits on the conclusion:**

A graph transformer applies learned attention to node or graph features while graph structure determines which data is available or relevant. Attention can require feature exchange and intermediate storage beyond ordinary message passing, especially when neighborhoods or global relationships are large.

Partitioning assigns nodes, edges, features or attention work to devices. A partition reduces local memory pressure only if cross-partition neighbors and attention inputs can be fetched or communicated within the step. Replication can reduce communication at the cost of memory and consistency; cutting edges can reduce movement only if the model semantics are preserved.

Adaptive scaling can change partitions, replication or resource allocation as graph degree, workload or device load changes. The controller must detect the condition, migrate or rebuild state, synchronize parameters and avoid spending more time adapting than it saves. Dynamic partitioning can also change communication patterns and stragglers.

The official description reports no throughput, convergence, accuracy, memory, communication, energy, graph scale, topology or hardware result. Qualitative scalability therefore establishes a distributed-training direction, not a demonstrated graph-transformer benefit; topology and size sweeps with converged-quality checks are required.

**Source and location**

Evidence tier: Primary captured official DAC description only; no full paper extraction, distributed training artifact reproduction or independent topology, communication, scaling, convergence, memory and energy validation. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH3050)

DAC 2026 official description and data/review-packets/dac-2026-research3050.json: adaptive parallel graph-transformer training; large graphs; single-device and static-distributed baselines; qualitative scalability/efficiency claim; omitted graph, communication, convergence and hardware conditions.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** single-device graph-transformer training

static distributed partitioning

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH3050

**Hardware or process assumptions:** Multi-GPU or distributed training system; interconnect, memory, and consistency assumptions are unspecified.

**Limits:** No throughput, convergence, accuracy, memory, communication, or scale results are reported.

Adaptive partitioning may add synchronization overhead.

Official description only; graph-size and topology sweeps are required.

**Method or artifact:** Scalable adaptive parallel-training framework for graph transformers.

**Metrics:** Training scalability and efficiency are claimed qualitatively

**Problem:** Graph transformers have high memory and communication cost on large graphs.

**Workload or benchmark:** Large graph transformer models; graph partitioning, hardware, and baselines are unspecified.

</details>

<span id="paper-dac-2026-research341"></span>

### TAG: A Topology-Aware Architecture for Configurable and Memory-Efficient GNN Acceleration

DAC 2026 · Record: `dac-2026-research341`

[Read the step-by-step explanation](#explanation-dac-2026-research341)

**Updated source-backed reading card**

Reviewed 2026-09-08. Reconciles the TAG card with the captured official DAC description; explains graph topology effects on GNN dataflow, configurable memory/computation paths, reuse and irregular access, and the area/control cost of flexibility.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

GNN accelerators must execute graphs with different degree distributions, locality and relation structure without wasting fixed hardware or moving features and adjacency data excessively.

**Mechanism / artifact:**

Configurable topology-aware GNN accelerator with a graph memory hierarchy; exact topology classifier, configuration controls, dataflow modes, memory organization and reconfiguration mechanism are unavailable in the captured description.

**Workload — the work tested:**

Graph neural-network workloads; datasets, graph sizes, degree distributions, topology modes, layers, feature dimensions, precision, configuration frequency and baselines are unspecified.

**Hardware and manufacturing assumptions:**

Configurable accelerator with graph memory hierarchy; processing elements, buffer levels, interconnect, topology detection, control storage, precision, clock, area and energy boundaries are unspecified.

**Baseline — the comparison method:**

Fixed GNN accelerator

GPU GNN execution

Graph topology, model, precision, memory, configuration, correctness, speed, area and energy boundaries are unspecified

**Reported measurements:**

The official description qualitatively claims GNN memory and compute efficiency; no speed, energy, area, memory, accuracy, utilization or graph-diversity result is reported.

**Limits on the conclusion:**

Graph topology determines which features are reused, how many neighbors contribute to each node, how much adjacency metadata is read and where reductions occur. A dataflow efficient for a low-degree local graph may be poor for a high-degree or globally connected graph.

Topology-aware configuration can choose memory placement, traversal order, aggregation mode, tile size or processing-element assignment based on graph structure. The configuration must preserve edge direction, relation semantics, aggregation order and feature dependencies while avoiding extra analysis and control work.

A configurable memory hierarchy can reduce repeated feature movement by retaining reused values, but graph accesses may be scattered and high-degree nodes may create hot spots. Buffer capacity, address generation, interconnect contention and partial-sum storage remain part of the execution cost.

The official description reports no speed, energy, area, memory, accuracy, graph-diversity, configuration or hardware result. Qualitative topology awareness therefore establishes a flexible accelerator direction, not a demonstrated benefit across graphs; topology-diverse evaluation and control-overhead accounting are required.

**Source and location**

Evidence tier: Primary captured official DAC description only; no full paper extraction, configurable hardware/artifact reproduction or independent topology diverse, memory, control, performance, accuracy and energy validation. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH341)

DAC 2026 official description and data/review-packets/dac-2026-research341.json: configurable topology-aware GNN accelerator; graph memory hierarchy; fixed accelerator and GPU baselines; qualitative memory/compute efficiency claim; omitted speed, area, energy, accuracy and graph-diversity conditions.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** fixed GNN accelerator

GPU GNN execution

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH341

**Hardware or process assumptions:** Configurable accelerator with graph memory hierarchy; precision and interconnect assumptions are unspecified.

**Limits:** No speed, energy, area, memory, accuracy, or graph-diversity results are reported.

Configurability may add control and area overhead.

Official description only; topology-diverse validation is required.

**Method or artifact:** Configurable topology-aware GNN accelerator.

**Metrics:** GNN memory and compute efficiency are claimed qualitatively

**Problem:** GNN accelerators must handle diverse graph topologies without excessive memory movement or fixed-function waste.

**Workload or benchmark:** Graph neural-network workloads; graph datasets, topology modes, and baselines are unspecified.

</details>

<span id="paper-dac-2026-research2256"></span>

### ALOHA: Area-Efficient and Low-Power Stochastic Computing with Hammersley Sequences

DAC 2026 · Record: `dac-2026-research2256`

[Read the step-by-step explanation](#explanation-dac-2026-research2256)

**Updated source-backed reading card**

Reviewed 2026-09-08. Reconciles the ALOHA card with the captured official DAC description; explains stochastic bitstreams, probability-to-bit encoding, correlation-sensitive arithmetic, Hammersley sequence structure, stream length and area/power measurement boundaries.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Stochastic computing can replace wide arithmetic with simple bitstream logic, but its result depends on sequence length, correlation, conversion and repeated probabilistic operations.

**Mechanism / artifact:**

Hammersley-sequence stochastic-computing architecture for area- and power-efficient kernels; exact sequence generator, encoding, arithmetic operators, correlation control and conversion hardware are unavailable in the captured description.

**Workload — the work tested:**

Stochastic neural or signal-processing kernels; values, precision, stream length, sequence dimensions, nonlinear operations, workloads, error metric and baselines are unspecified.

**Hardware and manufacturing assumptions:**

Stochastic bitstream hardware; clock, sequence generators, counters, logic, conversion, area, power, latency, correlation and process assumptions are unspecified.

**Baseline — the comparison method:**

Conventional stochastic sequences

Binary fixed-point arithmetic

Precision, stream length, error target, clock, workload, conversion, area and power boundaries are unspecified

**Reported measurements:**

The official description qualitatively claims area and power efficiency; no accuracy, bitstream length, area, power, latency, error or workload result is reported.

**Limits on the conclusion:**

A stochastic number represents a value by the fraction of ones in a bitstream. A simple AND can estimate multiplication when the two streams are appropriately independent, while addition or scaled operators require other logic and probability constraints. The finite stream creates sampling error.

Correlation changes the result because the same bit positions jointly determine the operation. Two streams with the correct individual probabilities can produce a biased product if their ones occur at related positions. Correlation can also accumulate across layers, feedback or reused streams.

Hammersley sequences are low-discrepancy point sets intended to distribute samples more evenly than a conventional pseudorandom sequence. Their benefit depends on the mapping from points to bits, dimensions, sequence length, scrambling, reuse and nonlinear pipeline operations; low discrepancy does not by itself prove unbiased hardware arithmetic.

The official description reports no accuracy, stream length, area, power, latency, workload, sequence generator, correlation or conversion result. Qualitative area/power efficiency therefore does not establish numerical quality or system benefit; bit-accurate and hardware correlation analysis are required.

**Source and location**

Evidence tier: Primary captured official DAC description only; no full paper extraction, sequence/hardware artifact reproduction or independent bit accurate, correlation, numerical error, area, power and latency validation. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH2256)

DAC 2026 official description and data/review-packets/dac-2026-research2256.json: Hammersley-sequence stochastic computing; neural/signal-processing kernels; conventional stochastic and binary fixed-point baselines; qualitative area/power claim; omitted error, stream, hardware and workload conditions.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** conventional stochastic sequences

binary fixed-point arithmetic

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH2256

**Hardware or process assumptions:** Stochastic bitstream hardware; clock, area, and correlation assumptions are unspecified.

**Limits:** No accuracy, bitstream length, area, power, latency, or workload results are reported.

Sequence properties may not hold under nonlinear pipelines.

Official description only; hardware correlation analysis is required.

**Method or artifact:** Hammersley-sequence stochastic-computing architecture.

**Metrics:** Area and power efficiency are claimed qualitatively

**Problem:** Stochastic computing can reduce arithmetic hardware but suffers correlation, sequence, and latency costs.

**Workload or benchmark:** Stochastic neural or signal-processing kernels; precision, sequences, and baselines are unspecified.

</details>

<span id="paper-dac-2026-research272"></span>

### ZK-Flex: A Flexible and Scalable Framework for Accelerating Zero-Knowledge Proofs

DAC 2026 · Record: `dac-2026-research272`

[Read the step-by-step explanation](#explanation-dac-2026-research272)

**Updated source-backed reading card**

Reviewed 2026-09-08. Reconciles the ZK-Flex card with the captured official DAC description; explains proof-system variation, reusable arithmetic/memory interfaces, reconfiguration and the tradeoff between flexibility, area and peak throughput.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Zero-knowledge proof systems use different fields, curves, polynomial operations, memory layouts and proof phases, making a fixed accelerator efficient for some systems but difficult to reuse across others.

**Mechanism / artifact:**

Flexible scalable framework for zero-knowledge-proof acceleration using reconfigurable or heterogeneous proof hardware; exact proof-system abstraction, kernels, configuration model, memory organization and scaling mechanism are unavailable in the captured description.

**Workload — the work tested:**

Zero-knowledge circuits and proof systems; curves, fields, circuit sizes, witness sizes, proof phases, hardware targets, reconfiguration, memory and baselines are unspecified.

**Hardware and manufacturing assumptions:**

Reconfigurable or heterogeneous proof accelerator with arithmetic and memory resources; device, clock, configuration time, buffer capacity, external memory, host interface, area, power and energy assumptions are unspecified.

**Baseline — the comparison method:**

CPU/GPU proving

Fixed zero-knowledge accelerator

Proof system, curve, circuit, host/device boundary, reconfiguration, correctness, throughput, area and energy conditions are unspecified

**Reported measurements:**

The official description qualitatively claims proof acceleration and flexibility; proof latency, throughput, area, energy, memory, configuration cost and system coverage are not reported.

**Limits on the conclusion:**

Proof systems differ in finite fields, curve operations, polynomial transforms, commitments, hashing, memory layouts and phase ordering. A flexible framework needs an abstraction that captures these differences without hiding the operations that determine cost or correctness.

Reusable arithmetic and memory resources can support several proof systems, but configuration, routing, control, parameter loading and data-layout conversion add overhead. A fixed accelerator can specialize its datapath and buffers for one system and achieve higher peak throughput or lower energy.

Scalability can mean more circuits, larger proofs, more accelerator resources or more devices. Each meaning has different bottlenecks: arithmetic, memory capacity, bandwidth, synchronization, reconfiguration or host coordination. The system must preserve exact field arithmetic and proof semantics across configurations.

The official description reports no proof latency, throughput, area, energy, memory, reconfiguration, proof-system coverage, curve, circuit or hardware result. Qualitative flexibility therefore establishes a reusable acceleration direction, not a measured advantage over fixed or CPU/GPU systems; proof-system-diverse evaluation is required.

**Source and location**

Evidence tier: Primary captured official DAC description only; no full paper extraction, reconfigurable framework artifact reproduction or independent proof system, correctness, scaling, performance, area and energy validation. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH272)

DAC 2026 official description and data/review-packets/dac-2026-research272.json: flexible scalable ZK-proof acceleration framework; CPU/GPU and fixed-ZK baselines; qualitative acceleration/flexibility claim; omitted proof, curve, hardware, configuration, memory and scaling conditions.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** CPU/GPU proving

fixed ZK accelerator

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH272

**Hardware or process assumptions:** Reconfigurable or heterogeneous proof accelerator; memory and arithmetic assumptions are unspecified.

**Limits:** No proof latency, throughput, area, energy, memory, or system coverage are reported.

Flexibility may reduce peak efficiency.

Official description only; proof-system-diverse evaluation is required.

**Method or artifact:** Flexible scalable zero-knowledge-proof acceleration framework.

**Metrics:** Proof acceleration and flexibility are claimed qualitatively

**Problem:** ZK proof systems vary in arithmetic and memory behavior, limiting fixed-function acceleration.

**Workload or benchmark:** ZK circuits and proof systems; curves, hardware, and baselines are unspecified.

</details>

<span id="paper-dac-2026-research2888"></span>

### Enabling AI ASICs for Zero Knowledge Proof

DAC 2026 · Record: `dac-2026-research2888`

[Read the step-by-step explanation](#explanation-dac-2026-research2888)

**Updated source-backed reading card**

Reviewed 2026-09-08. Reconciles the AI-ASIC-for-ZK card with the captured official DAC description; explains the difference between neural accelerator patterns and exact proof arithmetic, including field operations, memory/dataflow, programmability and end-to-end correctness.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Zero-knowledge proof generation needs exact finite-field and cryptographic operations plus large, irregular intermediate data movement, so a conventional AI ASIC optimized for approximate dense tensor arithmetic may not transfer directly.

**Mechanism / artifact:**

AI-ASIC-inspired architecture or methodology for zero-knowledge proofs; exact reused AI mechanisms, proof kernels, arithmetic datapaths, memory organization, programmability and process are unavailable in the captured description.

**Workload — the work tested:**

Zero-knowledge proof generation; proof systems, curves/fields, circuit sizes, polynomial operations, witness sizes, proof phases, hardware targets and baselines are unspecified.

**Hardware and manufacturing assumptions:**

ASIC accelerator with large finite-field arithmetic and memory; process, precision, programmability, clock, voltage, external memory, host interface, configuration, area and energy assumptions are unspecified.

**Baseline — the comparison method:**

GPU/FPGA zero-knowledge proving

General-purpose AI ASIC

Proof system, field, circuit, correctness, arithmetic exactness, host boundary, flexibility, area and energy conditions are unspecified

**Reported measurements:**

The official description qualitatively claims zero-knowledge acceleration; no proof throughput, latency, area, energy, flexibility, circuit coverage or architecture result is reported.

**Limits on the conclusion:**

AI ASICs often exploit regular tensor operations, bounded precision, high reuse and tolerance for numerical approximation. Zero-knowledge proving requires exact modular arithmetic, field-specific reduction, polynomial transforms, commitments, hashing and proof-preserving control; an AI-style datapath must be checked against these semantics rather than assumed reusable.

The proof workload can be data-dominated as well as arithmetic-dominated. Large polynomials and trace/intermediate arrays need permutation, streaming, buffering and synchronization. A dense compute array can be underused when access patterns, operand widths or phase boundaries differ from an AI inference workload.

Programmability can support multiple proof systems but adds instruction, routing, control, configuration and verification cost. Hardwiring one field or curve can improve peak performance and energy while losing reuse. The correct comparison must expose the supported proof-system set and the cost of switching or emulating unsupported operations.

The official description reports no proof throughput, latency, area, energy, flexibility, circuit coverage, architecture, process, field or host boundary. The qualitative acceleration claim therefore establishes an exploration direction, not an ASIC result or end-to-end proving benefit; exactness and complete prover validation are required.

**Source and location**

Evidence tier: Primary captured official DAC description only; no full paper extraction, asic/RTL artifact reproduction or independent exact arithmetic, proof correctness, flexibility, area, energy and end to end validation. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH2888)

DAC 2026 official description and data/review-packets/dac-2026-research2888.json: AI-ASIC techniques for ZK proofs; finite-field arithmetic and memory; GPU/FPGA and general AI-ASIC baselines; qualitative acceleration claim; omitted architecture, proof, exactness and hardware conditions.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** GPU/FPGA ZK proving

general-purpose AI ASIC

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH2888

**Hardware or process assumptions:** ASIC accelerator with large finite-field arithmetic and memory; process and programmability assumptions are unspecified.

**Limits:** No proof throughput, latency, area, energy, flexibility, or circuit results are reported.

AI-ASIC assumptions may not match cryptographic workloads.

Official description only; end-to-end proving validation is required.

**Method or artifact:** AI-ASIC-inspired architecture/methodology for zero-knowledge proofs.

**Metrics:** ZK acceleration is claimed qualitatively

**Problem:** ZK proof workloads require specialized arithmetic and memory systems unlike conventional AI inference.

**Workload or benchmark:** ZK proof generation; proof systems, arithmetic, and baselines are unspecified.

</details>

<span id="paper-dac-2026-research1480"></span>

### ADAPT: An Algorithm-Hardware Co-Design for Spiking Transformer with Training-Free Adaptive Token Pruning and Hierarchical

DAC 2026 · Record: `dac-2026-research1480`

[Read the step-by-step explanation](#explanation-dac-2026-research1480)

**Updated source-backed reading card**

Reviewed 2026-09-08. Reconciles the ADAPT card with the captured official DAC description; explains spiking-transformer events, token pruning, hierarchical decisions, training-free constraints and the separation between event reduction, model quality and hardware efficiency while preserving the truncated-title uncertainty.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Spiking-transformer inference can process event-driven token activity and still spend work on tokens or states that contribute little to the current output; pruning must reduce work without damaging temporal or attention semantics.

**Mechanism / artifact:**

Training-free adaptive token pruning with hierarchical spiking-transformer hardware co-design and event-driven execution; exact token score, hierarchy, temporal state, pruning rule and accelerator dataflow are unavailable in the captured description.

**Workload — the work tested:**

Spiking transformer workloads; models, event-stream encoding, time steps, token definition, pruning rates, task quality, event rates, hardware target and baselines are unspecified.

**Hardware and manufacturing assumptions:**

Event-driven accelerator with hierarchical token processing; memory for spikes and temporal state, event routing, timing, synchronization, precision, process, clock, area and energy assumptions are unspecified.

**Baseline — the comparison method:**

Dense spiking transformer

Static token pruning

Model, event stream, time steps, pruning policy, quality target, hardware, latency and energy boundaries are unspecified

**Reported measurements:**

The official description qualitatively claims adaptive pruning efficiency; no accuracy, sparsity, latency, energy, area, event rate, time-step or hardware result is reported.

**Limits on the conclusion:**

A spiking transformer represents activity as events over time rather than only dense real-valued activations. A token can be inactive at one step and important later because temporal state, attention context or accumulated membrane state persists.

Token pruning must define what is removed, when the decision is made, how temporal state and attention dependencies are handled, and whether a pruned token can return. A training-free rule cannot rely on retraining to compensate for the changed event and attention distribution.

Hierarchical pruning can make a coarse decision before a more expensive fine decision, reducing work when the hierarchy is predictive. It adds score computation, control, buffering and possible synchronization, and a mistaken early decision can remove information that later stages need.

The official title is truncated and the full method scope is unavailable. No accuracy, sparsity, latency, energy, area, event-rate, time-step, model or hardware result is reported; qualitative pruning efficiency therefore does not establish preserved spiking-transformer quality or end-to-end event-driven benefit.

**Source and location**

Evidence tier: Primary captured official DAC description only; no full paper extraction, complete title recovery, pruning/hardware artifact reproduction or independent temporal, accuracy, event rate, performance and energy validation. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH1480)

DAC 2026 official description and data/review-packets/dac-2026-research1480.json: training-free adaptive token pruning; hierarchical spiking-transformer hardware co-design; dense/static-pruning baselines; truncated title; qualitative efficiency claim; omitted model, event, quality and hardware conditions.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** dense spiking transformer

static token pruning

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH1480

**Hardware or process assumptions:** Event-driven accelerator with hierarchical token processing; timing, memory, and process assumptions are unspecified.

**Limits:** The official title is truncated; full method scope requires source recovery.

No accuracy, sparsity, latency, energy, area, or event-rate results are reported.

Official description only; task and hardware validation is required.

**Method or artifact:** Training-free adaptive token pruning with hierarchical spiking-transformer hardware co-design.

**Metrics:** Adaptive pruning efficiency is claimed qualitatively

**Problem:** Spiking-transformer inference can waste compute on redundant tokens while requiring event-driven hardware support.

**Workload or benchmark:** Spiking transformer workloads; models, event streams, quality targets, and hardware are unspecified.

</details>

<span id="paper-dac-2026-research1569"></span>

### FILCO: Flexible Composing Architecture with Real-Time Reconfigurability for DNN Acceleration

DAC 2026 · Record: `dac-2026-research1569`

[Read the step-by-step explanation](#explanation-dac-2026-research1569)

**Updated source-backed reading card**

Reviewed 2026-09-08. Reconciles the FILCO card with the captured official DAC description; explains composable DNN hardware, operator-specific dataflow, real-time reconfiguration, fabric utilization and configuration/switching overhead.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

DNN models and operators have different shapes, reuse patterns and resource needs, so a fixed accelerator can waste hardware on some workloads while a general FPGA may pay flexibility and control costs.

**Mechanism / artifact:**

Composable, real-time reconfigurable DNN accelerator architecture; exact composition units, fabric topology, configuration mechanism, operator coverage, switching protocol and runtime controller are unavailable in the captured description.

**Workload — the work tested:**

DNN inference workloads; models, operators, tensor shapes, precision, batch, reconfiguration targets, request mix, quality and baselines are unspecified.

**Hardware and manufacturing assumptions:**

Reconfigurable accelerator fabric with configuration storage and switching; device, clock, fabric resources, memory hierarchy, interconnect, bitstream/configuration size, reconfiguration latency, area and energy are unspecified.

**Baseline — the comparison method:**

Fixed-function DNN accelerator

General FPGA accelerator

Models, operators, precision, fabric, configuration, latency, utilization, quality, area and energy boundaries are unspecified

**Reported measurements:**

The official description qualitatively claims reconfigurable acceleration; no latency, utilization, reconfiguration time, area, energy, accuracy, operator coverage or runtime result is reported.

**Limits on the conclusion:**

DNN operators differ in tensor dimensions, reuse, reduction patterns, precision and memory traffic. Composable hardware can assemble resources for a particular operator or layer, but the composition must preserve data dependencies, buffering, synchronization and output layout.

Real-time reconfiguration changes the active datapath while execution is ongoing or between workload segments. It requires configuration storage, a switching protocol, quiescing or isolation, state handling and a way to resume without losing data. Configuration transfer and control time are part of inference latency.

A fabric configured for one operator may leave other resources idle, and frequent layer changes can make reconfiguration dominate. A fixed accelerator may have lower peak efficiency while avoiding transition costs; a general FPGA may offer broad support but different resource and clock behavior.

The official description reports no latency, utilization, reconfiguration time, area, energy, accuracy, operator coverage, configuration size or hardware result. Qualitative reconfigurable acceleration therefore does not establish a complete DNN-inference benefit; workload-diverse layer and transition measurements are required.

**Source and location**

Evidence tier: Primary captured official DAC description only; no full paper extraction, fabric/configuration artifact reproduction or independent operator diverse, transition, utilization, performance, area and energy validation. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH1569)

DAC 2026 official description and data/review-packets/dac-2026-research1569.json: composable real-time-reconfigurable DNN accelerator; fixed-function and general-FPGA baselines; qualitative acceleration claim; omitted operator, configuration, latency, utilization, area and energy conditions.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** fixed-function DNN accelerator

general FPGA accelerator

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH1569

**Hardware or process assumptions:** Reconfigurable accelerator fabric; configuration storage and switching overhead are unspecified.

**Limits:** No latency, utilization, reconfiguration time, area, energy, or accuracy results are reported.

Flexibility may add control and configuration overhead.

Official description only; workload-diverse validation is required.

**Method or artifact:** Composable, real-time reconfigurable DNN accelerator architecture.

**Metrics:** Reconfigurable acceleration is claimed qualitatively

**Problem:** Changing DNN workloads require accelerator flexibility without sacrificing utilization.

**Workload or benchmark:** DNN inference workloads; models, operators, and reconfiguration targets are unspecified.

</details>

<span id="paper-dac-2026-research2157"></span>

### RFIPSA: A Reconfigurable FIP-Based Systolic Array for Various Matrix-Intensive Workloads

DAC 2026 · Record: `dac-2026-research2157`

[Read the step-by-step explanation](#explanation-dac-2026-research2157)

**Updated source-backed reading card**

Reviewed 2026-09-08. Reconciles the RFIPSA card with the captured official DAC description; explains systolic-array dataflow, reconfiguration across matrix kernels, workload-shape effects and preserves the unresolved meaning of FIP rather than inventing its expansion.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

A fixed systolic array can lose utilization when matrix dimensions, operand reuse, precision or reduction patterns differ across matrix-intensive workloads.

**Mechanism / artifact:**

Reconfigurable FIP-based systolic array; the captured official record does not define FIP, array topology, configuration units, dataflow modes, memory system or reconfiguration mechanism.

**Workload — the work tested:**

Matrix-intensive workloads; operators, matrix dimensions, batch, precision, sparsity, data layouts, workload mix, platform and baseline implementations are unspecified.

**Hardware and manufacturing assumptions:**

Reconfigurable systolic array; FIP meaning, processing-element structure, memory hierarchy, interconnect, configuration storage, clock, process, area and energy conditions are unspecified.

**Baseline — the comparison method:**

Fixed systolic array

GPU matrix engine

Operators, dimensions, precision, platform, mapping, reconfiguration, utilization, correctness, area and energy boundaries are unspecified

**Reported measurements:**

The official description qualitatively claims cross-workload matrix efficiency; throughput, utilization, reconfiguration time, area, energy, silicon and workload results are not reported.

**Limits on the conclusion:**

A systolic array streams operands and partial sums through a regular processing-element grid. Its utilization depends on matrix dimensions, tile boundaries, operand reuse, reduction direction, precision and whether the producer/consumer rates match the array.

Reconfiguration can select a dataflow, array partition, precision or operator-specific path for a workload. The new mode must preserve tensor layout, partial-sum state, memory interfaces and timing; loading configuration and draining or initializing the array add transition cost.

Different matrix kernels can have different shapes and reuse. A mode that improves one workload may add routing, control or idle resources for another. A cross-workload claim needs a defined workload mix and must show whether reconfiguration is amortized per kernel, layer, request or batch.

FIP is undefined in the official record, so its arithmetic or architectural scope cannot be inferred. No throughput, utilization, reconfiguration, area, energy, workload, precision, process or silicon result is reported; qualitative efficiency therefore does not establish a reusable matrix engine benefit.

**Source and location**

Evidence tier: Primary captured official DAC description only; no full paper extraction, fip definition recovery, array/configuration artifact reproduction or independent workload, reconfiguration, utilization, silicon, area and energy validation. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH2157)

DAC 2026 official description and data/review-packets/dac-2026-research2157.json: reconfigurable FIP-based systolic array; fixed-array and GPU matrix baselines; qualitative cross-workload efficiency claim; FIP undefined; omitted matrix, configuration, throughput, silicon and PPA conditions.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** fixed systolic array

GPU matrix engine

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH2157

**Hardware or process assumptions:** Reconfigurable systolic array; FIP meaning, memory hierarchy, and process are unspecified.

**Limits:** No throughput, utilization, reconfiguration, area, energy, or workload results are reported.

FIP assumptions are undefined in the official record.

Official description only; architecture and silicon validation is required.

**Method or artifact:** Reconfigurable FIP-based systolic array.

**Metrics:** Cross-workload matrix efficiency is claimed qualitatively

**Problem:** A fixed systolic array may underperform across diverse matrix-intensive workloads.

**Workload or benchmark:** Matrix-intensive workloads; operators, dimensions, precision, and platform are unspecified.

</details>

<span id="paper-dac-2026-research2753"></span>

### An Energy-Efficient Dataflow Architecture for Efficient MoE Model Inference

DAC 2026 · Record: `dac-2026-research2753`

[Read the step-by-step explanation](#explanation-dac-2026-research2753)

**Updated source-backed reading card**

Reviewed 2026-09-08. Reconciles the MoE dataflow card with the captured official DAC description; explains expert-dependent token counts, padding waste, token-stationary execution, reconfigurable systolic-array requirements and the difference between eliminating redundant multiply work and proving end-to-end energy improvement.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

MoE inference routes each token to a subset of experts, so each expert receives a variable number of tokens. Fixed tensor dimensions can pad smaller expert batches and execute multiplication on invalid entries.

**Mechanism / artifact:**

Token-stationary dataflow and a reconfigurable systolic array intended to represent varying expert input token counts without padding; exact array topology, routing implementation, memory system, reconfiguration mechanism and controller are unavailable in the captured description.

**Workload — the work tested:**

MoE inference; model architecture, expert count, top-k routing, token-count distribution, sequence and batch sizes, precision, quality target and platform are unspecified.

**Hardware and manufacturing assumptions:**

Reconfigurable systolic array for expert matrix operations; input staging, expert-parameter storage, interconnect, configuration storage, clock, process, area, power and energy boundaries are unspecified.

**Baseline — the comparison method:**

State-of-the-art GPU-based MoE inference frameworks

Fixed-size expert tensors with padding

Model, routing, token distribution, precision, GPU, software version, quality, latency, energy and measurement-boundary conditions are unspecified

**Reported measurements:**

The official description qualitatively claims significant improvement over state-of-the-art GPU-based MoE inference frameworks; no numerical throughput, latency, energy, area, padding fraction, accuracy or routing result is reported.

**Limits on the conclusion:**

MoE routing sends different tokens to different experts. The number of tokens assigned to an expert varies with the router output, so a fixed expert-input shape pads the smaller groups and performs work on entries that do not represent real tokens.

A token-stationary dataflow keeps a token as the unit of work while expert parameters are supplied to it, or otherwise organizes the array so valid token counts determine useful computation. Eliminating padding removes invalid multiply-accumulate operations, but it still requires routing, token grouping, expert-weight access, partial-sum movement and output restoration.

A reconfigurable systolic array must change its active dimensions, valid lanes, data movement or scheduling as expert token counts change. The design must define how configuration is selected, how a short expert group is drained, how weights are reused, how idle lanes are avoided and whether configuration or routing state adds latency and energy.

The official description reports no expert-count distribution, padding fraction, routing traffic, memory traffic, throughput, latency, energy, area, accuracy or GPU/software conditions. Removing padding work therefore does not by itself establish an end-to-end energy advantage or a fair comparison with GPU MoE frameworks; the captured evidence establishes a dataflow proposal and qualitative claim only.

**Source and location**

Evidence tier: Primary captured official DAC description only; no full paper extraction, array/configuration artifact reproduction or independent routing, padding, memory, performance, energy, area and quality validation. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH2753)

DAC 2026 official description and data/review-packets/dac-2026-research2753.json: variable expert token counts; fixed expert tensors and padding; token-stationary dataflow; reconfigurable systolic array; qualitative GPU-framework comparison; omitted routing, token distribution, padding fraction, performance, energy, area and quality conditions.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** dense model inference

conventional MoE dataflow

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH2753

**Hardware or process assumptions:** Accelerator or heterogeneous memory system for MoE; interconnect and precision assumptions are unspecified.

**Limits:** No accuracy, throughput, energy, area, communication, or routing results are reported.

Dataflow benefits may depend on expert locality.

Official description only; model and system validation is required.

**Method or artifact:** Energy-aware MoE inference dataflow architecture.

**Metrics:** MoE energy efficiency is claimed qualitatively

**Problem:** Mixture-of-experts inference incurs routing, memory, and communication energy overhead.

**Workload or benchmark:** MoE language or vision models; expert counts, routing, and platform are unspecified.

</details>

<span id="paper-dac-2026-research552"></span>

### UCME: Unified and Configurable Matrix Extension for Diverse CPU Architectures with Minimal Design Overhead

DAC 2026 · Record: `dac-2026-research552`

[Read the step-by-step explanation](#explanation-dac-2026-research552)

**Updated source-backed reading card**

Reviewed 2026-09-08. Reconciles the UCME card with the captured official DAC description; explains matrix-extension coupling to a CPU pipeline, decoupled/asynchronous execution, matrix-vector overlap, cross-CPU integration and the conditions required to interpret the reported utilization, speedup and area claims.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Tightly coupled matrix instructions can make a matrix extension difficult to integrate across different CPU pipelines and can prevent matrix work from overlapping scalar or vector work efficiently.

**Mechanism / artifact:**

UCME: an adaptable, unified and configurable matrix extension that decouples the matrix unit from the CPU pipeline, reuses existing compute and memory resources, supports asynchronous operations and enables matrix-vector overlap; exact ISA, interface, control, compiler and configuration details are unavailable in the captured description.

**Workload — the work tested:**

ResNet50, BERT and Llama3 are named; matrix dimensions, batch, sequence length, precision, kernels, software mappings, CPU implementations, quality conditions and measurement boundaries are unspecified.

**Hardware and manufacturing assumptions:**

Integration into four open-source RTL CPUs; a 4 TFLOPS at 14 nm implementation is reported at 0.53 mm²; CPU pipeline, matrix-unit, memory hierarchy, clock, voltage, SRAM, process-library and power conditions are otherwise unspecified.

**Baseline — the comparison method:**

Intel AMX

Fixed or tightly coupled matrix extension

SIMD CPU execution

CPU microarchitecture, compiler, ISA mapping, precision, frequency, memory system, workload and end-to-end measurement boundaries are unspecified

**Reported measurements:**

The captured official description reports over 90% utilization, up to 2.31× speedup on ResNet50, BERT and Llama3 over Intel AMX, 30% gains from matrix-vector overlap, and a 4 TFLOPS at 14 nm implementation occupying 0.53 mm²; the exact definitions and conditions are not exposed.

**Limits on the conclusion:**

A matrix extension performs tiled matrix operations using dedicated or shared arithmetic and storage. Tight pipeline coupling makes the CPU's instruction issue, dependency, register and retirement rules part of the matrix operation's control path; different CPU pipelines then require different integration logic or software interfaces.

Decoupling the matrix unit lets the CPU submit work and lets the matrix unit progress independently. Asynchronous execution requires a command or descriptor interface, dependency tracking, completion signaling, storage for operands and results, and a defined rule for exceptions, ordering and memory consistency. Reusing CPU compute or memory resources can reduce duplicated hardware, but it also creates contention that must be measured.

Matrix-vector overlap means matrix work and vector work execute concurrently when their resources, data dependencies and memory traffic permit. The gain depends on the fraction of time both streams have independent work and on whether shared memory bandwidth, cache capacity or execution ports become the bottleneck; it is not guaranteed by asynchronous issue alone.

The description reports over 90% utilization, up to 2.31× speedup on named workloads over Intel AMX, 30% overlap gains and a 4 TFLOPS-at-14-nm 0.53 mm² implementation. It does not expose precision, frequency, compiler mapping, CPU configurations, AMX settings, workload shapes, accuracy, energy, power, area boundary or whether the numbers are measured, synthesized or modeled. The claims therefore establish a promising integration direction and reported results, not a fully reproducible cross-CPU advantage.

**Source and location**

Evidence tier: Primary captured official DAC description only; no full paper extraction, RTL/compiler artifact reproduction or independent cross cpu, overlap, utilization, throughput, ppa and energy validation. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH552)

DAC 2026 official description and data/review-packets/dac-2026-research552.json: tight pipeline coupling; adaptable matrix extension decoupled from CPU pipeline; unified software support; reuse of compute and memory resources; asynchronous operations; matrix-vector overlap; four open-source RTL CPUs; over 90% utilization; up to 2.31× speedup on ResNet50, BERT and Llama3 over Intel AMX; 30% overlap gain; 4 TFLOPS at 14 nm and 0.53 mm²; omitted ISA, compiler, precision, frequency, energy and measurement conditions.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** fixed matrix extension

SIMD CPU execution

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH552

**Hardware or process assumptions:** Configurable CPU execution units and compiler support; timing and area assumptions are unspecified.

**Limits:** No performance, area, energy, compiler, compatibility, or silicon results are reported.

Configuration overhead may vary across ISAs.

Official description only; architecture and workload validation is required.

**Method or artifact:** Unified configurable CPU matrix extension.

**Metrics:** Cross-CPU matrix efficiency is claimed qualitatively

**Problem:** CPU matrix extensions must support diverse architectures without large implementation or software costs.

**Workload or benchmark:** Matrix-intensive CPU workloads; ISA, precisions, and implementations are unspecified.

</details>

<span id="paper-dac-2026-research641"></span>

### Torr: Towards Brain-Inspired Task-Oriented Reasoning via Cache-Oriented Algorithm-Architecture Co-Design

DAC 2026 · Record: `dac-2026-research641`

[Read the step-by-step explanation](#explanation-dac-2026-research641)

**Updated source-backed reading card**

Reviewed 2026-09-08. Reconciles the Torr card with the captured official DAC description; explains dense CLIP matching, hyperdimensional associative reasoning, temporal coherence, cached graph updates, precision-gated memory and the limits of the reported real-time, energy and accuracy claims.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Open-vocabulary task-oriented detection can spend substantial computation on dense alignment and repeated intermediate-state movement, making real-time edge execution difficult.

**Mechanism / artifact:**

Torr: a brain-inspired algorithm-architecture co-design using hyperdimensional computing similarity, graph reasoning with query caching and delta updates, and a lane-scalable precision-gated item memory with RT-30/RT-60 control; exact encoding, cache protocol, memory organization and accelerator schedule are unavailable in the captured description.

**Workload — the work tested:**

Task-oriented object detection on CLIP with open-vocabulary, prompt-driven semantics; dataset, image resolution, prompt set, model quality, frame rate, temporal sequence and workload distribution are unspecified.

**Hardware and manufacturing assumptions:**

A 28 nm Torr accelerator with item memory and cache-oriented execution; clock, voltage, memory capacity, interconnect, precision levels, area, power boundary and post-layout or silicon status are unspecified.

**Baseline — the comparison method:**

CLIP-style dense matching

Standard reasoning model

Cache-oblivious execution

Dataset, prompt, resolution, accuracy target, precision, clock, memory, software and end-to-end measurement boundaries are unspecified

**Reported measurements:**

The captured official description claims real-time detection, millijoule energy, competitive average precision and orders-of-magnitude lower energy; exact AP, latency, energy, area, frequency and baseline conditions are not exposed.

**Limits on the conclusion:**

Dense CLIP-style matching compares visual features with text or query representations across many positions or candidates. The work grows with the number of features and queries and can repeatedly move intermediate state through memory. A cache-oriented algorithm must identify which state is stable, which state changes, and when a cached result remains valid.

Hyperdimensional associative reasoning represents items or relations in high-dimensional codes and uses similarity or binding operations for retrieval and reasoning. Replacing dense matching changes the representation and decision rule; competitive detection quality must therefore be measured at the same task, vocabulary, prompt, resolution and confidence conditions rather than inferred from lower arithmetic cost.

Temporal coherence means that adjacent frames or successive reasoning steps share information. Query caching and delta updates can avoid recomputing unchanged graph or query state, but they need a validity rule, storage for cached state, update detection and a fallback when the scene or query changes. Cache hits, misses and invalidation work determine the actual benefit.

Precision-gated item memory can reduce movement or arithmetic for low-sensitivity values and use more precision when the decision requires it. The gate must be defined and its quality effect measured; lower precision or stale cached state can alter similarity, graph updates and detection decisions.

The description reports a 28 nm accelerator with real-time detection, millijoule energy, competitive AP and orders-of-magnitude lower energy, but does not expose dataset, AP, latency, frame rate, cache hit rate, precision, memory traffic, area, power, clock or baseline implementation. The record establishes a reported co-design direction, not independently reproducible task quality or energy superiority.

**Source and location**

Evidence tier: Primary captured official DAC description only; no full paper extraction, model/cache/memory artifact reproduction or independent task quality, temporal, latency, area, power and energy validation. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH641)

DAC 2026 official description and data/review-packets/dac-2026-research641.json: task-oriented object detection on CLIP; dense alignment and memory traffic; hyperdimensional associative reasoning; temporal coherence; graph reasoning with query caching and delta updates; lane-scalable precision-gated item memory; RT-30/RT-60 control; 28 nm accelerator; real-time, millijoule, competitive AP and orders-of-magnitude energy claims; omitted task, quality, cache, memory and hardware conditions.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** standard reasoning model

cache-oblivious execution

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH641

**Hardware or process assumptions:** Processor or accelerator with explicit cache management; memory and precision assumptions are unspecified.

**Limits:** No task accuracy, cache traffic, latency, energy, area, or model results are reported.

Brain-inspired abstractions may be task-specific.

Official description only; model and hardware validation is required.

**Method or artifact:** Cache-oriented algorithm-architecture co-design for brain-inspired reasoning.

**Metrics:** Reasoning efficiency is claimed qualitatively

**Problem:** Task-oriented reasoning can incur repeated memory accesses and intermediate-state movement.

**Workload or benchmark:** Reasoning or agent tasks; models, cache hierarchy, and quality metrics are unspecified.

</details>

<span id="paper-dac-2026-research660"></span>

### TRINE: A Token-Aware, Runtime-Adaptive FPGA Inference Engine for Multimodal AI

DAC 2026 · Record: `dac-2026-research660`

[Read the step-by-step explanation](#explanation-dac-2026-research660)

**Updated source-backed reading card**

Reviewed 2026-09-08. Reconciles the TRINE card with the captured official DAC description; explains heterogeneous multimodal kernels, single-bitstream FPGA execution, mode-switchable processing elements, top-k token pruning, dependency-aware offload and the conditions needed to interpret latency, power and accuracy claims.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

A multimodal model can combine ViT, CNN, GNN and transformer-NLP layers with different tensor sparsity, dimensions and operator requirements. A static FPGA mapping can underuse its resources or require costly reconfiguration when the active modality or layer changes.

**Mechanism / artifact:**

TRINE: a single-bitstream FPGA accelerator and compiler for end-to-end multimodal inference, using a mode-switchable processing-element array for DDMM, SDDMM and SpMM, weight/output-stationary systolic modes, 1×CS SIMD, a routable adder tree, in-stream top-k token pruning and dependency-aware offload across RPUs; exact compiler and runtime protocols are unavailable in the captured description.

**Workload — the work tested:**

Multimodal stacks mixing ViTs, CNNs, GNNs and transformer NLP; model graphs, token distributions, modalities, sequence lengths, pruning thresholds, accuracy metric and software preprocessing are unspecified.

**Hardware and manufacturing assumptions:**

Alveo U50 and ZCU104 FPGA platforms with reconfigurable processing resources and RPUs; bitstream size, clock, memory hierarchy, board power boundary, resource use, compiler mapping and runtime control conditions are unspecified.

**Baseline — the comparison method:**

RTX 4090

Jetson Orin Nano

Static FPGA engine

Multimodal model, precision, batch, token sequence, preprocessing, GPU software, clock and latency/power boundary are unspecified

**Reported measurements:**

The captured official description reports up to 22.57× lower latency than RTX 4090 and 6.86× lower latency than Jetson Orin Nano at 20–21 W, with less than 2.5% accuracy loss and state-of-the-art efficiency; exact workload, accuracy, latency and power conditions are not exposed.

**Limits on the conclusion:**

Multimodal layers have different operations and data movement. Dense-dense matrix multiplication, sampled or sparse-dense multiplication and sparse matrix multiplication need different operand paths, valid-lane rules, reduction behavior and storage. One fixed datapath can support all of them only by adding modes, routing and control.

A single bitstream avoids full FPGA reconfiguration between layers, but it does not mean that every resource is useful for every mode. A mode-switchable processing-element array must change operand flow, storage roles and reduction paths while preserving in-flight state, tensor layout and completion ordering. The transition and control cost need measurement.

In-stream top-k token pruning can reduce later work by retaining only selected tokens before they reach subsequent operators. The selection consumes comparisons, buffering and control, and pruning can remove information needed by later layers. Accuracy loss must be measured against the same model, dataset, token policy and quality metric, with the cost of selection included.

Dependency-aware offload can overlap independent kernels across reconfigurable processing units when their inputs are ready and their memory traffic does not conflict. The benefit depends on graph parallelism, buffer capacity, synchronization, load balance and the definition of the RPU boundary; independent kernels can still serialize on memory or shared interconnect.

The description reports U50 and ZCU104 latency ratios, 20–21 W operation, less than 2.5% accuracy loss and state-of-the-art efficiency, but it does not expose model graphs, precision, token distributions, pruning threshold, clocks, resource use, preprocessing, GPU software, energy accounting or whether power is board, accelerator or system power. The claims establish a reported design direction, not a fully reproducible end-to-end comparison.

**Source and location**

Evidence tier: Primary captured official DAC description only; no full paper extraction, compiler/bitstream artifact reproduction or independent multimodal accuracy, latency, power, resource and reconfiguration validation. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH660)

DAC 2026 official description and data/review-packets/dac-2026-research660.json: ViT/CNN/GNN/transformer-NLP multimodal stack; single-bitstream FPGA; DDMM/SDDMM/SpMM; mode-switchable PE array; weight/output-stationary systolic, 1×CS SIMD, routable adder tree; in-stream top-k pruning; dependency-aware RPU offload; Alveo U50 and ZCU104; 22.57× and 6.86× latency claims; 20–21 W; <2.5% accuracy loss; omitted model, precision, pruning, clock, resource, power and measurement conditions.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** static FPGA engine

GPU multimodal inference

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH660

**Hardware or process assumptions:** FPGA accelerator with runtime adaptation; reconfiguration and memory assumptions are unspecified.

**Limits:** No accuracy, latency, throughput, reconfiguration, energy, or area results are reported.

Adaptation may depend on token and modality distributions.

Official description only; workload and hardware validation is required.

**Method or artifact:** Token-aware runtime-adaptive FPGA inference engine.

**Metrics:** Multimodal inference efficiency is claimed qualitatively

**Problem:** Multimodal token streams vary in length and modality, causing FPGA utilization and latency variation.

**Workload or benchmark:** Multimodal AI models; modalities, token distributions, and FPGA are unspecified.

</details>

<span id="paper-dac-2026-research693"></span>

### MALIWAN: Performance and Energy Efficiency Co-Optimization of GEMM on Versal ACAP Architectures

DAC 2026 · Record: `dac-2026-research693`

[Read the step-by-step explanation](#explanation-dac-2026-research693)

**Updated source-backed reading card**

Reviewed 2026-09-08. Reconciles the MALIWAN card with the captured official DAC description; explains heterogeneous Versal mapping, analytical sampling, on-board surrogate learning, Pareto tradeoffs and the limits of the reported 6,000-experiment and efficiency claims, including the truncated GPU comparison.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

GEMM performance and energy on a heterogeneous Versal ACAP depend on how work is divided among AIEs, programmable logic and the processing system. A mapping that improves throughput can increase power or leave another component underused.

**Mechanism / artifact:**

MALIWAN: automated GEMM design-space exploration that combines analytical-model sampling, on-board measurements and a data-driven surrogate model to search mapping configurations and generate Pareto-optimal choices; exact search variables, model features, training split and stopping rule are unavailable in the captured description.

**Workload — the work tested:**

GEMM on the Versal VCK190; dimensions, precision, batch, layouts, memory placement, clocks, compared state-of-the-art works and NVIDIA GPU configurations are unspecified.

**Hardware and manufacturing assumptions:**

AMD/Xilinx Versal ACAP with AIEs, PL and PS; approximately 6,000 on-board experiments and a VCK190 evaluation are reported. Board power, clock, voltage, memory, resource allocation, measurement instrumentation and system boundary are unspecified.

**Baseline — the comparison method:**

State-of-the-art GEMM mapping works

NVIDIA GPUs

Fixed or manually selected Versal mappings

GEMM shapes, precision, software, clocks, power boundary and throughput/energy definitions are unspecified

**Reported measurements:**

The captured official description reports about 6,000 on-board experiments; over state-of-the-art works, geometric-mean throughput improvement of 1.23× up to 2.5× and geometric-mean energy-efficiency improvement of 1.25× up to 2.7×; it also begins a GPU comparison claiming up to 2.5× energy efficiency, but the captured source ends before that comparison is complete.

**Limits on the conclusion:**

GEMM computes a product of two matrices and an accumulation. On a heterogeneous ACAP, the mapping decides which dimensions are partitioned across AIEs, programmable logic and the processing system, where tiles and partial sums reside, and how data moves between memories and engines. Those choices determine arithmetic utilization, transfer traffic, buffering and synchronization.

A Pareto search does not optimize one number. A configuration is Pareto-optimal when no other tested configuration improves one objective without worsening another, such as throughput and power or energy efficiency. The frontier depends on the allowed configurations, constraints, measurement noise and whether area, accuracy, memory or thermal limits are included.

Analytical sampling can cover a large design space cheaply, while on-board measurements capture device effects that a model may miss. A surrogate model then predicts unmeasured configurations and guides further experiments. Its value depends on the training coverage, feature choices, error on unseen mappings and policy for correcting bad predictions; it does not replace measurement of the final selected mapping.

The description reports approximately 6,000 board experiments on VCK190, geometric-mean and maximum throughput/energy-efficiency improvements over state-of-the-art works, and begins a GPU comparison. It does not expose GEMM shapes, precision, mapping space, clock, power boundary, measurement method, surrogate error, area or the complete NVIDIA comparison because the captured source ends mid-sentence. The results establish a reported device-specific exploration framework, not a general mapping advantage for every GEMM or accelerator.

**Source and location**

Evidence tier: Primary captured official DAC description only; source capture is truncated during the gpu comparison; no full paper extraction, search artifact reproduction or independent mapping, surrogate, throughput, power and energy validation. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH693)

DAC 2026 official description and data/review-packets/dac-2026-research693.json: GEMM on heterogeneous Versal AIE/PL/PS; analytical-model sampling; data-driven ML surrogate; ≈6,000 on-board experiments; VCK190; 1.23× geometric-mean and 2.5× maximum throughput improvement; 1.25× geometric-mean and 2.7× maximum energy-efficiency improvement; incomplete GPU comparison beginning with up to 2.5× energy efficiency; omitted shapes, precision, clocks, power boundary, search variables and surrogate validation.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** CPU/GPU GEMM

fixed ACAP mapping

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH693

**Hardware or process assumptions:** AMD/Xilinx Versal ACAP with heterogeneous engines; memory and clock assumptions are unspecified.

**Limits:** No throughput, energy, area, utilization, or workload results are reported.

Optimization may be device-specific.

Official description only; board-measured validation is required.

**Method or artifact:** Performance and energy co-optimization for GEMM mapping.

**Metrics:** Performance-energy efficiency is claimed qualitatively

**Problem:** GEMM mapping on heterogeneous ACAPs must balance performance, energy, and resource allocation.

**Workload or benchmark:** GEMM workloads; dimensions, precisions, Versal device, and baselines are unspecified.

</details>

<span id="paper-dac-2026-research885"></span>

### Chimera: A Unified FHE Accelerator with Enhanced Compatibility for TFHE

DAC 2026 · Record: `dac-2026-research885`

[Read the step-by-step explanation](#explanation-dac-2026-research885)

**Updated source-backed reading card**

Reviewed 2026-09-08. Reconciles the Chimera card with the captured official DAC description; explains CKKS and TFHE operator differences, unified FFT/NTT datapaths, bootstrapping-key unrolling, shrinking KeySwitch, constrained auto-tuning and the limits of the reported TFHE and CKKS comparisons.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

A unified FHE accelerator must support schemes with different arithmetic and memory behavior. Mapping TFHE onto hardware organized for CKKS can reduce utilization and make TFHE bootstrapping and KeySwitch operations expensive.

**Mechanism / artifact:**

Chimera: unified FHE accelerator with a dual-mode computational flow unifying FFT and NTT, aggressive TFHE bootstrapping-key unrolling, hardware-oriented FFT Shrinking KeySwitch support, redesigned functional units and memory organization, and an error-, memory- and bandwidth-constrained auto-tuning framework.

**Workload — the work tested:**

TFHE workloads and CKKS workloads are named; circuits, security parameters, polynomial dimensions, ciphertext modulus, bootstrapping settings, precision and workload mix are unspecified.

**Hardware and manufacturing assumptions:**

Unified FHE accelerator with shared transform functional units and scheme-specific memory organization; area, frequency, process, on-chip memory, bandwidth, power and configuration conditions are unspecified.

**Baseline — the comparison method:**

State-of-the-art unified FHE accelerators

CKKS-centric unified designs

TFHE mapped to CKKS-oriented operators

FHE parameters, security level, precision, hardware frequency, memory and performance boundaries are unspecified

**Reported measurements:**

The captured official description reports average 14.84× performance improvement across TFHE workloads, comparable CKKS performance and a 9.6% area increase versus state-of-the-art unified FHE designs; exact workload, parameter, frequency, area and measurement conditions are not exposed.

**Limits on the conclusion:**

Fully homomorphic encryption evaluates a function while data remains encrypted. CKKS is designed for approximate arithmetic, while TFHE supports fast Boolean or integer-like gate operations through torus-based bootstrapping. Their transforms, ciphertext representations, precision requirements and memory traffic are not interchangeable merely because both use polynomial arithmetic.

An NTT computes modular polynomial transforms used by schemes such as CKKS, while an FFT computes a related transform over a different numerical domain and is central to TFHE operations. A dual-mode datapath can share butterfly arithmetic, routing and storage structures, but it must handle different modulus, precision, scaling, twiddle-factor, rounding and correctness requirements.

Bootstrapping refreshes a ciphertext so further homomorphic operations remain possible. TFHE bootstrapping can require large key material and repeated transform operations. Key unrolling exposes or stages more bootstrapping-key work to increase parallel utilization, but it increases storage, bandwidth and possibly area. The design must state whether the key is on chip, streamed, compressed and counted in the energy result.

KeySwitch changes the ciphertext key representation and can become a bottleneck. FFT Shrinking KeySwitch is described as hardware-oriented support intended to reduce that cost, but the captured evidence does not define the shrinking transformation, error bound, memory schedule or security-preserving conditions. Auto-tuning must keep error, memory and bandwidth constraints while selecting TFHE configurations; a faster configuration is invalid if it changes the required correctness or security parameters.

The description reports 14.84× average TFHE improvement, comparable CKKS performance and 9.6% area increase, but does not expose FHE parameters, security level, precision/error target, transform implementation, memory/key traffic, clock, power or area boundary. The result establishes a reported unified accelerator design, not a scheme-independent FHE advantage.

**Source and location**

Evidence tier: Primary captured official DAC description only; no full paper extraction, fhe accelerator artifact reproduction or independent correctness, security parameter, workload, performance, area, bandwidth and energy validation. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH885)

DAC 2026 official description and data/review-packets/dac-2026-research885.json: CKKS/TFHE complementarity; CKKS-centric unified accelerators; FFT/NTT unified computation; dual-mode flow; bootstrapping-key unrolling; FFT Shrinking KeySwitch; redesigned functional units and memory; error/memory/bandwidth-constrained auto-tuning; 14.84× average TFHE improvement; comparable CKKS performance; 9.6% area increase; omitted parameters, security, transform, memory and PPA conditions.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** CPU/GPU FHE

scheme-specific accelerator

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH885

**Hardware or process assumptions:** Specialized FHE arithmetic and memory; ciphertext precision and process assumptions are unspecified.

**Limits:** No security parameters, latency, throughput, energy, area, or circuit results are reported.

Compatibility may reduce peak efficiency.

Official description only; cryptographic and hardware validation is required.

**Method or artifact:** Unified accelerator supporting TFHE-compatible FHE operations.

**Metrics:** FHE acceleration is claimed qualitatively

**Problem:** Fully homomorphic encryption accelerators face expensive bootstrapping and scheme-specific hardware.

**Workload or benchmark:** FHE workloads and TFHE circuits; parameters, schemes, and hardware are unspecified.

</details>

<span id="paper-dac-2026-research946"></span>

### UNICON: A Unified Reconfigurable Nonlinear Architecture for Efficient Neural Network Inference

DAC 2026 · Record: `dac-2026-research946`

[Read the step-by-step explanation](#explanation-dac-2026-research946)

**Updated source-backed reading card**

Reviewed 2026-09-08. Reconciles the UNICON card with the captured official DAC description; explains nonlinear activation evaluation, logarithmic-domain shift-add decomposition, shared hardware across functions, dynamic dataflow reconfiguration and the conditions needed to interpret the reported speedup, energy and area-efficiency ratios.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

DNN nonlinear activation functions have different mathematical forms and can require expensive arithmetic, memory and control. Supporting many functions with duplicated dedicated hardware increases area and can reduce utilization.

**Mechanism / artifact:**

UNICON: unified reconfigurable activation hardware using a logarithmic-domain computing paradigm, shift-add decomposition, modular organization and dynamically reconfigurable dataflows to support diverse nonlinear activation functions without hardware duplication.

**Workload — the work tested:**

DNN nonlinear activation functions; function set, input distributions, precision, approximation error, models, batch and layer shapes are unspecified.

**Hardware and manufacturing assumptions:**

Reconfigurable arithmetic architecture with logarithmic-domain conversion and shift-add units; memory, conversion tables, precision, clock, process, area, power and reconfiguration conditions are unspecified.

**Baseline — the comparison method:**

State-of-the-art nonlinear activation architectures

Dedicated hardware per activation function

Function set, approximation target, precision, model, frequency, area and energy boundaries are unspecified

**Reported measurements:**

The captured official description reports average 1.55× speedup, 2.56× energy efficiency and 2.74× area efficiency over state-of-the-art NAF architectures; exact functions, accuracy/error, frequency, area and energy conditions are not exposed.

**Limits on the conclusion:**

A nonlinear activation maps an input value to an output value after a layer's accumulation. Examples include exponential-like, sigmoid-like, rectifying and gated functions. Unlike a multiply-accumulate, the function may require range handling, comparison, exponentiation, division, table lookup or iterative approximation, so its cost depends on precision and input distribution.

A logarithmic-domain design represents magnitude through a logarithm so multiplication-like operations can become additions or shifts. The conversion into and out of that domain, sign handling, zero and saturation cases, finite precision and approximation error remain part of the activation computation. Shift-add decomposition reduces a complex operation only if the approximation meets the model's numerical requirements.

Unifying functions requires identifying a shared internal representation and the function-specific coefficients, branches or sequences that produce each output. Modular hardware can select different paths, but the controller must configure those paths, handle state and preserve timing when the activation changes. Dynamic dataflow reconfiguration can reduce duplicated units while adding control, routing, configuration storage and transition cost.

Activation quality must be evaluated at the network output, not only by local numerical error. A small error in one layer may be amplified by later layers, while an input range not represented during design can trigger saturation or large approximation error. The function set, precision, error metric, input distribution, model accuracy and comparison implementation are required.

The description reports average 1.55× speedup, 2.56× energy efficiency and 2.74× area efficiency over state-of-the-art NAF architectures, but does not expose the activation set, approximation method, precision, conversion cost, frequency, area boundary, power, reconfiguration overhead or network-level accuracy. The result establishes a reported unified architecture, not proof of equal-quality advantage across all nonlinear functions or DNNs.

**Source and location**

Evidence tier: Primary captured official DAC description only; no full paper extraction, activation approximation artifact reproduction or independent numerical accuracy, network quality, latency, area and energy validation. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH946)

DAC 2026 official description and data/review-packets/dac-2026-research946.json: diverse complex NAF forms; logarithmic-domain computing; shift-add decomposition; modular design; dynamic reconfigurable dataflows; no hardware duplication; average 1.55× speedup, 2.56× energy efficiency and 2.74× area efficiency; omitted activation set, approximation, precision, conversion and PPA conditions.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** fixed nonlinear units

software nonlinear functions

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH946

**Hardware or process assumptions:** Reconfigurable arithmetic accelerator; configuration and memory assumptions are unspecified.

**Limits:** No accuracy, latency, energy, area, reconfiguration, or model results are reported.

Reconfigurability may add control overhead.

Official description only; model and silicon validation is required.

**Method or artifact:** Unified reconfigurable nonlinear inference architecture.

**Metrics:** Neural inference efficiency is claimed qualitatively

**Problem:** Neural networks use diverse nonlinear functions that can require costly dedicated hardware.

**Workload or benchmark:** Neural-network inference; models, nonlinear operators, precision, and hardware are unspecified.

</details>

<span id="paper-dac-2026-research983"></span>

### ATTINA: Spatial Acceleration of Additive Number Theoretic Transform for Energy-Efficient zkSNARKs at the Edge

DAC 2026 · Record: `dac-2026-research983`

[Read the step-by-step explanation](#explanation-dac-2026-research983)

**Updated source-backed reading card**

Reviewed 2026-09-08. Reconciles the ATTINA card with the captured official DAC description; explains the role of finite-field transforms in zkSNARK proving, distinguishes additive NTT from a conventional NTT claim, and bounds the spatial-accelerator and edge-efficiency conclusion because no proof, circuit or hardware conditions are exposed.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

zkSNARK proving repeatedly performs finite-field polynomial operations, and transform cost can constrain latency and energy on an edge device.

**Mechanism / artifact:**

Spatial accelerator for an additive number-theoretic transform (NTT) used in zkSNARK proving; the captured description does not expose the transform definition, dataflow, arithmetic units, memory organization or proof-system integration.

**Workload — the work tested:**

zkSNARK proving; curve or field, circuit size, proving system, polynomial degree, transform length, proof-generation phase, edge processor and comparison workloads are unspecified.

**Hardware and manufacturing assumptions:**

Finite-field accelerator intended for edge devices; operand precision, modular-reduction method, memory capacity/bandwidth, array dimensions, clock, voltage, area, power and security boundary are unspecified.

**Baseline — the comparison method:**

CPU/GPU NTT

Generic proof accelerator

Curve, field, transform length, proving system, implementation, memory and end-to-end proof boundary are unspecified

**Reported measurements:**

The official description makes a qualitative claim of edge zkSNARK efficiency; proof latency, throughput, energy, area and absolute comparison values are not reported.

**Limits on the conclusion:**

A zkSNARK prover transforms a computation into a proof that a verifier can check without receiving the private witness. The transform is only one part of proving; witness processing, polynomial construction, commitments, multi-scalar multiplication, hashing, memory movement and proof serialization may also contribute materially.

An NTT evaluates or reorganizes polynomial data over a finite field so multiplication and convolution can be performed efficiently. Its cost depends on field arithmetic, transform length, roots or decomposition, modular reduction, memory layout and whether the transform is forward, inverse or part of a larger fused operation.

The title names an additive NTT, but the captured description does not define its additive operation or show how it differs from the baselines. A spatial layout may expose parallelism, yet data permutation, synchronization, field reduction and intermediate storage can determine whether that parallelism improves complete proving time.

No proof latency, throughput, energy, area, security, circuit size, curve, field, edge hardware or circuit results are reported. The qualitative efficiency statement therefore establishes a proposed transform accelerator direction, not a measured edge zkSNARK advantage or a secure proving implementation.

**Source and location**

Evidence tier: Primary captured official DAC description only; no full paper extraction, transform definition, RTL/FPGA/asic artifact reproduction or independent proving, security and edge system validation. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH983)

DAC 2026 official description and data/review-packets/dac-2026-research983.json: spatial acceleration of additive NTT for edge zkSNARKs; CPU/GPU NTT and generic proof-accelerator baselines; qualitative edge-efficiency claim; omitted curve, circuit, proof, hardware, security and quantitative conditions.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** CPU/GPU NTT

generic proof accelerator

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH983

**Hardware or process assumptions:** Finite-field accelerator for edge devices; precision, memory, and security assumptions are unspecified.

**Limits:** No proof latency, throughput, energy, area, security, or circuit results are reported.

Benefits may depend on curve and proof system.

Official description only; cryptographic and hardware validation is required.

**Method or artifact:** Spatial accelerator for additive number-theoretic transforms.

**Metrics:** Edge zkSNARK efficiency is claimed qualitatively

**Problem:** zkSNARK proving at the edge is constrained by finite-field transform cost and energy.

**Workload or benchmark:** zkSNARK proving; curves, circuits, proof systems, and edge hardware are unspecified.

</details>

## What remains to establish

Resolve unspecified workloads, comparison methods, resource budgets, and source locations before generalizing a reported gain. Multiple papers in this selected sample permit comparison of mechanisms, but do not by themselves establish recurrence across years or a long-term trend.

[All subthemes](../expanded-taxonomy-v1.md) · [Research directions](../directions/README.md)
