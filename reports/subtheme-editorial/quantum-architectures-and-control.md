## A quantum result depends on more than quantum gates

A quantum computation prepares a state, changes it through a sequence of operations, and measures an output. Classical computation is needed before, during, and after that sequence: to choose the operations, arrange their execution, interpret measurements, and estimate the answer. Reducing one of these costs does not automatically reduce the time needed to obtain a sufficiently accurate answer.

A qubit has two computational-basis states, conventionally called zero and one. Its state can also contain amplitudes for both, including relative phase information that affects later operations. Measuring in that basis produces a classical outcome, not a list of all amplitudes. Repeated preparations and measurements are therefore often needed to estimate a probability or an observable, meaning a quantity that the experiment can measure.

The nine papers here address different parts of this process. Five manuscripts were recovered in this pass; four papers remain supported by conference descriptions. Manuscript versions and exact locations are given below. The reading cards incorporate the refreshed findings and preserve their superseded fields separately. Neither manuscript access nor this editorial review establishes independent reproduction.

| Part of the computation | Papers in this subject | What must not be confused |
|---|---|---|
| Arrange operations | Directional transport; Lin-Search; code switching | Compiler runtime, gate count, and device execution time |
| Detect and handle errors | Syndrome scheduling; CryoZip; SiTA | Measurement, decoding, compression, and statistical mitigation |
| Interpret a device image | Atom-detection accelerator | Image-analysis latency and the whole control cycle |
| Construct an algorithm | Hamiltonian-guided pre-training; OHQS | Initial quality, final error, and total solution cost |

These boundaries matter when combining findings across themes. A scheduler that produces measurement data faster can increase pressure on the transmission and decoding path. Compression may relieve that pressure while adding delay. An accurate image-analysis result may still arrive too late for a dependent operation. The complete system has to satisfy all these requirements together.

<span id="explanation-dac-2026-research1608"></span>

## Directional transport: the compiler trades atom motion, duration, and modeled fidelity

### What remote entanglement requires

In a neutral-atom processor, qubits are atoms held in optical traps. A remote two-qubit operation needs the processor to create the required interaction between atoms that are not already in the same interaction region. An acousto-optic deflector (AOD) changes the position of trapping light and can move atoms. Directional excitation transport uses an ancillary atom or path to carry the interaction toward the target while leaving the data atoms less exposed to repeated movement.

A controlled-Z (CZ) operation changes the joint phase only for the relevant two-qubit state. The compiler must produce the intended CZ sequence while also accounting for transport, excitation, reset, calibration and error accumulation. Reducing the movement of data atoms does not remove the physical work; it changes where that work occurs.

### What static and dynamic paths mean

The recovered manuscript distinguishes a reusable static arrangement from a dynamic arrangement whose ancillary paths change with the circuit. A static plan can amortize setup and keep routing predictable, but it may use a path that is poor for a particular sequence. A dynamic plan can adapt the path to the current gates, but it adds scheduling and control decisions and may require more movement or preparation during execution.

The compiler therefore optimizes a coupled schedule, not one scalar. A shorter duration can expose the system to fewer time-dependent errors, while a path with fewer or better-conditioned interactions may improve modeled gate fidelity at the cost of a longer schedule. These objectives must be reported together under the same circuit and device assumptions.

### How to read the reported QFT result

For the 200-qubit QFT example, the manuscript reports dynamic/static durations of 236,000/92,600 microseconds and modeled fidelities of 3.70×10⁻⁷/1.67×10⁻¹². The dynamic value is about 221,000 times the static value, but both absolute fidelities are extremely small in this model. The comparison supports a fidelity–duration tradeoff; it does not mean that one configuration simultaneously achieves the shortest duration and highest fidelity, and it is not a measured device speedup.

The result also depends on the error model, transport assumptions, ancillary preparation and reset, calibration, layout, circuit decomposition and definition of fidelity. A ratio between two modeled values should not be read as an experimentally demonstrated improvement unless those physical conditions are measured or independently validated.

### What remains open

The cited sections establish the static/dynamic distinction and the reported QFT comparison. They do not establish hardware execution, device calibration overhead, atom loss, transport error, distance scaling, compiler runtime or end-to-end algorithm success probability. A complete evaluation must measure or model every stage that the schedule adds, then compare total duration and accepted output quality under the same circuit and device constraints.

[Observed paper card](../observed-subthemes/quantum-architectures-and-control.md#paper-dac-2026-research1608)

## Directional transport: moving an excitation is not moving every data atom

Neutral-atom devices hold atoms with optical traps. An acousto-optic deflector, or AOD, steers trapping light and can move atoms. An ancillary atom is an additional atom used to perform an operation rather than retain the program's data throughout execution. A controlled-Z, or CZ, changes the phase of the joint state when both qubits are in state one; it is a two-qubit operation.

The [directional-transport compiler](../observed-subthemes/quantum-architectures-and-control.md#paper-dac-2026-research1608) uses ancillary paths for remote CZ operations, with AOD movement retained for setup and adjustments. Sections 4.2–4.3 distinguish a reusable static arrangement from changing paths for quantum Fourier transform circuits. Section 5 compares modeled execution with Enola, ZAC, and ZAP. For 200-qubit QFT, dynamic rather than static scheduling raises modeled fidelity from 1.67×10⁻¹² to 3.70×10⁻⁷, while duration rises from 92,600 to 236,000 μs. This is not a measured quantum-device speedup. [Version-1 manuscript, Sections 4–5, PDF pages 4–6, Figure 6](https://arxiv.org/pdf/2604.11000v1#page=6).

The important tradeoff is explicit: a larger fidelity ratio can coexist with a very low absolute fidelity and a longer schedule. It would be misleading to combine the shortest static duration and highest dynamic fidelity as though one configuration achieved both. Device validation must also account for preparing, resetting, and calibrating the ancillary path.

<span id="explanation-dac-2026-research2756"></span>

## Lin-Search: exact gate-count search is exact only for the stated synthesis model

### What CNOT synthesis is solving

A CNOT flips the target qubit when the control qubit is one. A sequence containing only CNOTs implements a reversible linear transformation over binary values. Many different sequences can implement the same transformation, so a compiler can search for a shorter sequence.

“Shorter” must be defined. Lin-Search searches for minimum CNOT count under its allowed operations and circuit model. That is different from minimum depth, because independent gates may execute in parallel, and different from minimum physical execution time, because connectivity, routing, calibration and hardware gate durations may differ.

### How iterative deepening proves a count

The search tests candidate sequences at increasing lengths. If it finds a sequence of length k and has exhaustively ruled out all valid sequences of length less than k under the model, k is optimal for that model. Exhaustion is difficult because the number of possible sequences grows rapidly with qubit count and allowed control-target pairs.

Lower bounds allow the search to discard a partial sequence when the remaining operations cannot possibly reach the target within the current depth. Equivalence rules identify partial or complete circuits that have the same transformation, avoiding repeated exploration. These rules are useful only if they preserve the target semantics and account for the permitted connectivity and gate set.

### What the reported limits mean

The captured description reports optimal solutions for random instances up to 15 qubits and 15 CNOTs within 600 seconds on a laptop. It also reports an average 16% CNOT reduction in a larger rewriting flow and 30% fewer timeouts than its SAT-based comparator. The first result concerns exact search within a bounded instance and time budget; the second concerns a rewriting workflow and is not a proof of global optimality for the surrounding mixed-gate circuits.

Replacing a subcircuit with fewer CNOTs can increase depth, require additional routing, change the layout of other gates or alter the cost of non-CNOT operations. A fair end-to-end comparison must preserve the implemented unitary, connectivity, gate error model and output-quality target while measuring depth, total gate cost, routing, compilation time and timeouts.

### What the evidence establishes and where it stops

The refreshed description supports iterative deepening, lower-bound pruning, equivalence pruning and the stated bounded synthesis and rewriting results. The full manuscript, precise benchmark distribution and connectivity assumptions remain unrecovered. The author tool listing is evidence that a tool is named, not an executed artifact or reproduced optimality result.

[Observed paper card](../observed-subthemes/quantum-architectures-and-control.md#paper-dac-2026-research2756)

## Lin-Search: exact gate-count search has a defined boundary

A controlled-NOT, or CNOT, replaces the target bit's basis value with its exclusive-or with the control. Sequences containing only these gates implement reversible binary linear transformations. Different sequences can implement the same transformation, so compilation can search for one using fewer gates.

[Lin-Search](../observed-subthemes/quantum-architectures-and-control.md#paper-dac-2026-research2756) searches in increasing gate count and eliminates partial sequences using lower bounds and equivalent-circuit rules. The description reports optimal solutions for random instances up to 15 qubits and 15 CNOTs within 600 seconds on a laptop. In a larger rewriting flow it reports 16% fewer CNOTs on average relative to original circuits and 30% fewer timeouts than its SAT-based comparator. The manuscript, precise benchmark distribution, and connectivity assumptions remain unrecovered. [Official DAC description](https://63dac.conference-program.com/presentation/?id=RESEARCH2756&sess=sess133).

“Exact” must describe the actual search objective and permitted operations. Minimal gate count is not necessarily minimal depth: some gates run concurrently and others cannot. A locally optimal replacement is also not a proof that the surrounding mixed-gate circuit is globally optimal. The [authors' tool page](https://www.veri-q.com/tools/qda/) lists Lin-Search, but a listing is not an executed artifact or a reproduced optimality result.

<span id="explanation-dac-2026-research2621"></span>

## Code switching: assign protection by circuit demand, then price the transition

### What code switching changes

Quantum error correction represents one logical state across several physical qubits. A code determines which checks are measured, which logical operations are native or transversal, how many physical qubits are needed, and how faults propagate. Switching codes moves the protected logical information from one code representation to another; it does not change the intended logical value.

The design problem is that different parts of a circuit may favor different codes. One code may support a needed logical operation directly while another may provide a lower cost for a different operation. Every switch adds its own fault-tolerant operations, ancilla preparation and scheduling constraints, so minimizing switches is a proxy for reducing cost only under an explicit switch-cost model.

### Why a minimum cut appears

The recovered method assigns a code choice to each relevant operation or circuit region. Connections represent transitions or dependencies between regions. A two-code assignment can be represented as dividing the graph into two sides; edges crossing the division correspond to code switches. A minimum cut finds the assignment with the lowest sum of selected edge weights.

The unweighted objective minimizes the number of transitions. Weighted extensions can assign different costs to transitions, such as preferring switches during idle periods or penalizing switches across a particular dependency. The mathematical optimum is exact for that graph and those weights. It is not automatically exact for physical execution because the graph may omit ancilla preparation, measurement, routing, code distance, logical error and hardware constraints.

### How to read the reported depth savings

The manuscript evaluates generated H, T and CNOT circuits with 2D and 3D color-code choices using Python/NetworkX. Table 1 reports 4.79–5.56% modeled depth savings when switches are preferred during idle periods, under the assumption that a switch takes more than one and at most two logical single-qubit gate times.

That result is conditional on the circuit set, code implementations, switch timing and weighting rules. It does not mean that the same percentage of physical execution time disappears. If a switch requires expensive ancilla preparation, extra measurements, routing or a larger code block, the physical cost can exceed the logical-depth estimate. A switch scheduled during an idle logical interval may still consume hardware resources or constrain neighboring operations.

### What an end-to-end comparison must include

Compare total execution to a common logical-error target, not only switch count or logical depth. Include physical-qubit count, code distance, ancilla states, measurement and reset time, routing, decoder interaction, gate error, leakage and the cost of preparing or changing code blocks. The baseline must use the same circuit decomposition and hardware connectivity.

The result should also distinguish minimizing the number of switches, minimizing modeled depth, minimizing physical time, and minimizing logical error. These objectives can disagree. A switch can reduce depth while increasing error exposure or physical resource use.

### What the evidence establishes and where it stops

The recovered manuscript supports a two-code minimum-cut assignment model, weighted extensions, and the reported 4.79–5.56% modeled depth savings under its switch-time assumptions. It does not establish lower physical cost, improved logical error, hardware execution or universal optimality outside the defined graph model.

[Observed paper card](../observed-subthemes/quantum-architectures-and-control.md#paper-dac-2026-research2621)

## Code switching: choose where the information is protected

Quantum error correction encodes logical information across multiple physical qubits. A transversal operation acts separately on corresponding physical positions in code blocks, limiting how a single fault spreads within a block. Different codes support different such operations. Switching codes means transferring the protected logical information, not changing its intended value.

The [code-switching paper](../observed-subthemes/quantum-architectures-and-control.md#paper-dac-2026-research2621) converts a two-code assignment problem into a minimum cut: divide a graph between two code choices while minimizing the cost of connections crossing the division. Sections 2–3 use 2D/3D color codes and gates available in one or both. Section 4 tests generated circuits with Python/NetworkX on a Threadripper PRO 5955WX. Table 1 reports 4.79–5.56% depth savings from preferring switches during idle periods, assuming a switch takes more than one but at most two logical single-qubit gate times. [Version-1 manuscript, Sections 2–4, PDF pages 2–6](https://arxiv.org/pdf/2512.04170v1#page=6).

Minimum switch count and minimum physical cost are separate objectives. Some switches may require expensive ancillary-state preparation; staying in a particular code may itself consume more resources. The paper's weighted extensions permit expressing such preferences, but an optimal answer to a chosen cost model does not validate that model against a device. Logical error and physical-qubit requirements remain necessary parts of an end-to-end comparison.

<span id="explanation-dac-2026-research144"></span>

## Syndrome extraction scheduling: depth is a bound, while error depends on the schedule

### What a syndrome-extraction circuit does

Quantum error correction stores one logical state across multiple physical qubits. A syndrome-extraction round measures check operators indirectly: data qubits interact with an ancillary measurement qubit, and the ancilla outcome indicates whether an error pattern is consistent with a check. The data state is not read directly, so the circuit must implement the intended checks without allowing measurement, reset or gate faults to corrupt the inference.

Scheduling assigns each required interaction to a time layer. Two interactions sharing a qubit cannot occupy the same layer under the stated gate model. If the largest number of required interactions incident on any qubit is Δ, at least Δ CNOT layers are needed for the single-ancilla-per-check setting because that qubit cannot perform all of them simultaneously. A construction with depth Δ+1 is therefore a near-bound schedule, not necessarily an optimal schedule.

### Why equal depth does not mean equal protection

Two schedules can have the same number of CNOT layers while placing different interactions next to one another in time. The order affects which errors propagate through later gates, how long an ancilla remains involved, and how measurement and reset interact with the next operation. The resulting logical error rate can therefore differ even when circuit depth is identical.

The manuscript’s 48-physical-qubit tricycle-code comparison tests 1,728 schedules and reports up to an order-of-magnitude difference in logical error under the tested noise. That result does not mean that every schedule with the same depth has that spread, nor that the selected noise model predicts a device without calibration. It establishes that depth alone is an incomplete objective for schedule selection.

### What near-optimal means here

The depth bound is tied to a particular extraction model: one round, one ancilla per check, a specified interaction graph and the permitted gate operations. Changing the ancilla layout, allowing pipelining, changing measurement time or permitting additional operations changes the feasible schedule and possibly the bound. “Near-optimal” must therefore name the model, objective and comparison set.

A complete evaluation should report the schedule-construction time, depth, measurement and reset assumptions, gate conflicts, logical error model, physical error rates, ancilla resources and the number of schedules considered. If the schedule is intended for hardware, movement, calibration, crosstalk and simultaneous-operation limits must be included as well.

### What the source establishes and where it stops

The recovered manuscript supplies the Δ+1 proof scope, the deliberately one-layer-worse construction allowance, the 1,728-schedule tricycle-code experiment and its unequal logical-error result. The repository includes examples and tests, but they were not executed in this pass. The evidence supports a scheduling method and a precise depth/error tradeoff; it does not establish hardware-level logical error, universal optimality or a complete fault-tolerant execution result.

[Observed paper card](../observed-subthemes/quantum-architectures-and-control.md#paper-dac-2026-research144)

## Syndrome scheduling: short correct circuits can still have different error rates

A syndrome is a set of check outcomes used to infer errors without directly measuring all stored quantum information. A check can involve several data qubits and an ancillary qubit. Scheduling must prevent one qubit from participating in simultaneous incompatible gates and preserve the ordering needed to measure the intended checks.

The [syndrome-extraction paper](../observed-subthemes/quantum-architectures-and-control.md#paper-dac-2026-research144) proves a CNOT-depth bound of Δ+1 for single-round, single-ancilla-per-check extraction in quasi-abelian lifted-product codes. Δ is the largest number of required interactions incident on a qubit; at least Δ layers are needed because those interactions cannot all run simultaneously. Section 4.1 explicitly allows the construction to be one layer worse than an achievable optimum. Section 6 compares 1,728 schedules of a 48-physical-qubit tricycle code: equal-depth schedules differ in logical error by up to an order of magnitude under the tested noise. [Author manuscript, Sections 3–6, PDF pages 3–7](https://github.com/adiaconu11/Macro-scheduler/blob/main/dac.pdf).

The retrieved manuscript has nine pages, although the repository's citation template says seven; locations here follow the actual PDF. The [pinned manuscript](https://github.com/adiaconu11/Macro-scheduler/blob/e4f86d30a1cd1065477c9586fa2ca89a66c1c299/dac.pdf) was downloaded and matched byte-for-byte against the inspected copy on 2026-09-07. The [author repository](https://github.com/adiaconu11/Macro-scheduler) includes examples and tests, inspected but not executed in this pass.

The conceptual lesson is stronger than “shallower is better.” Depth is a constraint on sequential work, while error propagation depends on which interactions occur in which order. A physical implementation must additionally price measurement, reset, movement, and simultaneous-operation restrictions. The paper's pipelined extension explicitly notes that slower measurement can make its overlapping schedule less attractive.

<span id="explanation-dac-2026-research210"></span>

## CryoZip: compressing syndrome traffic is not the same as decoding or correcting errors

### What is moving through the link

Quantum error correction repeatedly measures checks on physical qubits. The measurement outcomes form a syndrome stream that a decoder uses to infer which errors may have occurred. In a cryogenic system, producing the data near the quantum device and processing it at warmer electronics creates a communication path with limited bandwidth, power and latency.

CryoZip addresses the representation of that stream. It does not itself infer the correction or prove that a physical error has been removed. Keeping compression, predecoding and final decoding separate is essential: each stage has a different output contract and can change the latency and error-handling requirements of the complete loop.

### How the compressor reduces representation size

The captured method encodes gaps between active syndrome entries and then applies a fixed Huffman codebook. If active entries are sparse, representing the positions of changes as gaps can use fewer symbols than sending a full bitmap or uncompressed event sequence. Huffman coding assigns shorter bit strings to common symbols and longer strings to rare symbols under the codebook.

A sliding-window hardware design processes only part of the stream at a time. That limits storage and can support a regular pipeline, but it also creates boundary conditions: a codeword or gap may span windows, the codebook must remain synchronized, and bursts can fill buffers even when the long-run average is low. The link must be designed for a required tail or worst-case traffic condition, not only the average compression ratio.

### Why the reported numbers are separate results

The manuscript reports 5.35× compression for a surface code at distance 21 and physical error rate 10⁻³ using post-synthesis vector-based estimates in 22 nm FDSOI characterized at 4 K. The roughly 14,239× bandwidth result combines compression with a predecoder at distance 9 and physical error rate 10⁻⁴. These are not one configuration or one isolated compressor result.

Section 5.1 also contains a condition discrepancy: the tested rates extend to 10⁻⁴, while the 48.3× peak is assigned to 0.1×10⁻⁴. That condition should remain unresolved rather than silently attributed to a corrected rate. A reported maximum must be tied to its exact code distance, physical error rate, workload, predecoder policy and bandwidth boundary.

### What an end-to-end evaluation must measure

Compression must preserve the syndrome information needed by the downstream decoder. The evaluation should report losslessness or a defined distortion rule, decompression and predecoder latency, buffer occupancy, burst behavior, link utilization, decoder input quality, power and the deadline for each correction round. It should separate compressor-only savings from savings caused by dropping easy cases in a predecoder.

Post-synthesis estimates can support an implementation projection, but they are not fabricated hardware measurements. Process, voltage, temperature, clock, memory, codebook storage, interface, reset and calibration conditions must be stated before a bandwidth or energy claim is generalized.

### What the evidence establishes and where it stops

The recovered manuscript supports a gap-coded, Huffman-based sliding-window compressor and distinguishes its 5.35× surface-code compression result from the combined predecoder bandwidth result. It does not establish a fabricated compressor, a complete error-correction deadline, or a universal bandwidth or energy reduction. The condition discrepancy in the peak result remains an explicit evidence limitation.

[Observed paper card](../observed-subthemes/quantum-architectures-and-control.md#paper-dac-2026-research210)

## CryoZip: reduce transferred error data without claiming the compressor corrects it

Compression changes how a message is represented. Decoding quantum errors uses that message to infer a correction. A predecoder handles a subset of simpler cases before a more capable decoder receives the unresolved cases. These functions have different correctness requirements and consume different resources.

[CryoZip](../observed-subthemes/quantum-architectures-and-control.md#paper-dac-2026-research210) encodes gaps between active syndrome entries, then applies a fixed Huffman codebook. Its sliding-window hardware processes part of the input at a time. Sections 4–5 use post-synthesis, vector-based estimates in 22 nm FDSOI characterized at 4 K, not a demonstrated fabricated compressor. Surface-code compression at distance 21 and physical error rate 10⁻³ is reported as 5.35×. The roughly 14,239× bandwidth result instead combines compression with a predecoder at distance 9 and error rate 10⁻⁴. [Version-1 manuscript, Sections 3–5, PDF pages 3–6](https://arxiv.org/pdf/2606.30805v1#page=5).

Section 5.1 also contains an unresolved condition discrepancy: it lists tested rates down to 10⁻⁴ but assigns the 48.3× peak to 0.1×10⁻⁴. That peak should not be assigned a silently corrected rate. Average compression must also be separated from worst-case traffic: a link and its buffers must handle bursts, not only average bytes saved. The compression result alone does not establish a complete error-correction loop's deadline or energy use.

<span id="explanation-dac-2026-research2540"></span>

## Atom detection: image-analysis latency is one stage of the control loop

### What the accelerator must infer

A fluorescence image records light over pixels after atoms are illuminated. The control system needs an occupancy decision for each expected trap location: is an atom present, absent, or uncertain? The image contains signal, background, optical blur and contributions from neighboring locations. Reconstruction estimates the local signal and turns it into a decision using a threshold or another classifier.

This is both a numerical and a classification problem. A faster implementation must preserve the accepted output under the same image model, calibration and decision rule. Matching a reference implementation after rounding shows numerical agreement within that test; it does not establish the physical detection-error rate on real images.

### What the FPGA parallelism changes

The recovered implementation maps reconstruction and image-data processing onto a ZCU216 FPGA at 100 MHz. FPGA parallelism can process independent pixels, local regions or arithmetic stages concurrently, while on-chip storage and pipeline structure determine how much data can be accepted each cycle. The useful metric is the elapsed analysis time for a complete image at the required accuracy and image shape, including transfers and startup if those are part of the deployment.

The reported timing uses simulated 256×256 through 1024×1024 images, 50 timing runs per case, and comparisons with original and optimized CPU implementations on an EPYC 9374F. For 256×256 pixels, analysis is 115 μs on the FPGA versus 4,012 and 730 μs for the two CPU references; for 1024×1024, it is 1.825 ms versus 37.600 and 5.100 ms. These numbers establish an image-analysis timing comparison under the stated setup, not an end-to-end rearrangement speedup.

### What must be included in the complete control cycle

After image acquisition, data may be transferred, occupancy decisions may be used to choose which atoms to move, and actuators must perform rearrangement before the next computation. Camera exposure, readout, transfer, FPGA startup, decision latency, path planning, atom movement, verification and reset can all contribute to the deadline. Optimizing the analysis stage helps only if it is on the critical path and the other stages can consume its output at the same rate.

Constant FPGA resource use across image sizes does not imply constant latency: a fixed circuit can process a larger image over more cycles. Fifty timing runs provide a sample of execution time, not a hard worst-case deadline or a tail-latency guarantee.

### What the evidence establishes and where it stops

The recovered evaluation supports the reported FPGA and CPU analysis times on simulated images and checks outputs against the reference algorithm with small rounding differences. It does not establish physical fluorescence-model accuracy, detection error on measured images, complete rearrangement-cycle latency, worst-case timing, energy or deployment robustness.

[Observed paper card](../observed-subthemes/quantum-architectures-and-control.md#paper-dac-2026-research2540)

## Atom detection: accelerate image analysis, then measure the rest of the cycle

A fluorescence image contains detected light spread across pixels. Estimating whether an atom occupies a known trap location requires separating the local signal from background and neighboring contributions. A threshold converts the estimated brightness into a presence decision. Faster arithmetic cannot repair an incorrect optical calibration by itself.

The [atom-detection accelerator](../observed-subthemes/quantum-architectures-and-control.md#paper-dac-2026-research2540) uses parallel reconstruction on a ZCU216 FPGA at 100 MHz. Section 5 uses simulated images, with 50 timing runs per case, against original and optimized CPU implementations on an EPYC 9374F. For 256×256 pixels, analysis takes 115 μs versus 4,012 and 730 μs; at 1024×1024 it takes 1.825 ms versus 37.600 and 5.100 ms. Output checks reference the original algorithm with small rounding differences, not a newly demonstrated physical detection-error rate. [Version-1 manuscript, Section 5, PDF pages 5–6, Figure 4](https://arxiv.org/pdf/2604.00816v1#page=5).

Image acquisition, transfer, rearrangement decisions, and actuation still contribute to the complete cycle. Constant circuit-resource use across image sizes does not mean constant runtime: the same hardware can process more work by running longer. Timing variability measured over 50 runs is likewise not a proof of a hard worst-case deadline.

<span id="explanation-dac-2026-research279"></span>

## SiTA: readout mitigation estimates a distribution; it does not repair the quantum state

### What readout mitigation is correcting

A quantum device produces classical measurement bits, but the bit seen by the control system may differ from the ideal outcome because of detector and readout errors. Readout mitigation estimates the relationship between intended and observed outcomes, then uses calibration data to correct the estimated output distribution. It acts after measurement. It does not undo gate errors that occurred earlier or restore the quantum state before measurement.

The calibration matrix or equivalent error model is part of the computation. If calibration is stale, incomplete, or measured at a different operating condition, the mitigation can amplify noise or bias the corrected distribution. “Without reduced fidelity” therefore requires a defined fidelity or statistical-error measure, a calibration procedure and the same target distribution used by the baseline.

### What the tensor-product cost is

For independent readout errors, a multi-qubit correction can be represented as tensor products of per-qubit transition operators. The number of represented states and probability entries can grow exponentially with qubit count. SiTA uses parallel work across probabilities and states and skips operations associated with exact zeros in the relevant representation.

The zero condition must be distinguished from a small nonzero value. A structural zero can be skipped without changing the mathematical result. A value that is absent because of finite sampling, thresholding or an approximation is not necessarily zero; removing it changes the distribution. The speed benefit therefore depends on the workload, representation, sparsity pattern, numerical precision and threshold policy.

### What the reported speedup means

The official description reports 4.9–1605× speedups over prior readout-mitigation methods without reduced fidelity. The range may reflect different workloads or qubit sizes, but the captured record does not expose those conditions, the calibration cost, the number of qubits, the implementation platform, the timing boundary or the absolute runtime. A kernel or mitigation-stage speedup cannot be promoted to a whole-application quantum speedup without including circuit execution, measurement collection, calibration, data preparation and output use.

### What a complete evaluation must measure

Use the same measured or simulated readout data, calibration quality, correction objective and output precision for each method. Report mitigation error against an ideal or independently characterized distribution, including cases where the sparse structure disappears. Include calibration generation, memory movement, preprocessing, correction, uncertainty estimation and any fallback for dense inputs. State whether timing covers only tensor operations or the complete mitigation pipeline.

### What the evidence establishes and where it stops

The refreshed description supports a sparse tensor-product dataflow that skips zero-related computation and reports a 4.9–1605× mitigation-stage speedup range. It does not establish fault-tolerant execution, preservation of a quantum state, universal sparsity, whole-application speedup, or calibration-robust fidelity. The full manuscript and system boundaries remain missing.

[Observed paper card](../observed-subthemes/quantum-architectures-and-control.md#paper-dac-2026-research279)

## SiTA: readout mitigation is not fault-tolerant execution

Readout mitigation estimates an output distribution after accounting for measurement errors. It does not restore a quantum state that suffered errors earlier in the circuit. Calibration describes how measured outcomes differ from intended outcomes; a wrong or stale calibration can bias the corrected estimate.

[SiTA](../observed-subthemes/quantum-architectures-and-control.md#paper-dac-2026-research279) proposes sparse tensor-product processing with parallel work across probabilities and states, skipping zero-related computation rather than pruning small nonzero values. Its description reports 4.9–1605× speedups over prior mitigation methods without reduced fidelity. Qubit counts, calibration conditions, implementation platform, and exact timing boundary are not supplied. “End-to-end” in that description must not be expanded into a demonstrated whole-quantum-application speedup. [Official DAC description](https://63dac.conference-program.com/presentation/?id=RESEARCH279&sess=sess135).

Sparse means that many entries in the relevant representation are zero. It is a property to establish for the tested workload, not a universal property of quantum states. A fair experiment should distinguish structural zeros from outcomes absent merely because too few measurements were taken, and include calibration and data preparation when claiming application-level savings.

<span id="explanation-dac-2026-research1966"></span>

## Hamiltonian-guided pre-training: a better starting point must be charged for its preparation

### What the initialization problem is

A variational quantum algorithm uses a parameterized circuit. A classical optimizer changes the circuit parameters and evaluates an objective, such as the energy of a spin model, from quantum measurements. The starting parameters matter because the objective may have flat regions, local minima or measurement noise that makes later improvement difficult.

The paper’s method uses structure from the Hamiltonian, the mathematical operator that defines the modeled system and its energy, to group parameters. It then uses Fourier reconstruction of low-dimensional objectives to estimate useful parameter settings before ordinary optimization. The intended benefit is a lower starting energy error, not a proof that the full optimization has become cheaper or globally optimal.

### What blocking and reconstruction do

Blocking divides a large parameter problem into smaller groups. Each group can be explored with fewer simultaneous variables, but the groups are not automatically independent: interactions between terms in the Hamiltonian can make a setting that looks good for one group worse when all parameters are combined.

Fourier reconstruction estimates the shape of a low-dimensional objective from sampled values. It can reduce the number of direct evaluations needed to identify a promising point when the objective has a suitable structure. The result depends on the sampling pattern, assumed frequency content, noise, number of measurements and reconstruction error. It is a model of the objective, not an exact view of the full quantum landscape.

### What “nearly 30-fold lower initial energy error” means

The captured description reports nearly 30-fold lower initial energy error in a blocking ablation against the next-best named benchmark. This compares the error at the start of subsequent optimization under that experiment. It does not report a 30-fold reduction in final error, total runtime, quantum measurement count, classical computation, electrical energy or time to reach a common target quality.

The fair total-cost comparison must include the measurements and classical work used to construct the starting point, the later optimization iterations, failed or rejected reconstructions, and the quality reached at termination. It must also define energy error relative to the same ground-state or reference value and preserve the same noise and measurement conditions across methods.

### What the current evidence establishes and where it stops

The refreshed official description identifies Hamiltonian-guided blocking and Fourier reconstruction and reports the initial-error ablation. It does not expose model sizes, parameter counts, sampling budget, noise model, reconstruction settings, the exact comparator, final convergence, total evaluations or hardware execution.

The evidence supports a structured initialization method for variational optimization. It does not establish global optimization, lower end-to-end cost or a hardware advantage. Those claims require measuring the complete preparation-plus-optimization process to the same final quality.

[Observed paper card](../observed-subthemes/quantum-architectures-and-control.md#paper-dac-2026-research1966)

## Hamiltonian-guided pre-training: a better start still has a cost

A Hamiltonian is a mathematical description of a system's energy and quantum evolution. In a variational algorithm, a classical optimizer adjusts circuit parameters to improve a measured objective. The initial parameters matter because limited measurements and difficult objective shapes can hinder subsequent search.

The [Hamiltonian-guided pre-trainer](../observed-subthemes/quantum-architectures-and-control.md#paper-dac-2026-research1966) groups parameters using Hamiltonian structure and reconstructs a low-dimensional objective using Fourier analysis of quantum measurements. Its description reports nearly 30-fold lower initial energy error than the next-best benchmark in a blocking ablation on spin models. That is not a 30-fold reduction in final runtime or electrical energy. Model sizes, measurement budgets, noise, and the named comparator remain missing. [Official DAC description](https://63dac.conference-program.com/presentation/?id=RESEARCH1966&sess=sess133).

Optimizing each small parameter group globally does not prove a global optimum over all parameters together. The decisive comparison counts pre-training measurements and classical work as well as subsequent optimization. A better starting point is useful if it reduces total work to the same target quality, not merely if the first plotted point looks better.

<span id="explanation-dac-2026-research1963"></span>

## OHQS: reducing numerical error is different from reducing complete solution cost

### What transient computation requires

An electromagnetic transient model describes electrical quantities that change over time. Its equations relate the current state of a power network to its derivatives and inputs. A numerical solver replaces continuous evolution with a sequence of computable updates. The result depends on the time discretization, representation of the state, approximation of the time-varying Hamiltonian, stopping rule and treatment of changing inputs.

The solver must produce the required outputs, not only a state representation. If the task asks for voltages or currents at specified times and precision, those values must be encoded, evolved, measured and reconstructed. Preparing the input and recovering the output are part of the computation even if the paper focuses on the evolution step.

### What discretized Hamiltonian evolution changes

OHQS represents the time-dependent evolution with a sequence of discretized Hamiltonian operations. Discretization converts a continuous-time problem into finite steps. Smaller or better-chosen steps can reduce numerical error, but may increase the number of operations and measurements. A fixed-point-based optimizer can tune the solver's parameters or update sequence to reduce approximation error, but its benefit depends on convergence, arithmetic precision, measurement noise and the tested network.

The method therefore has at least two objectives: approximate the physical equations accurately and execute the full encoded computation within a useful resource budget. Improving one step's approximation does not automatically reduce circuit depth, measurement count, classical processing, wall-clock time or energy.

### How to interpret the reported numbers

The captured description reports up to 99.91% accuracy and 9.56× error reduction against classical methods. Those numbers require the exact error definition, reference solution, time interval, network, input, tolerance and cost boundary. “Accuracy” might refer to a normalized state or selected output and is not interchangeable with absolute voltage/current error or time-to-solution.

The description also claims logarithmic qubit scaling with inverse error tolerance. That describes the number of qubits needed to represent a precision target under the stated encoding assumptions. It does not establish logarithmic runtime: the number of circuit operations, repetitions, state-preparation cost, measurement cost, output reconstruction and classical post-processing can grow separately.

### What the evidence establishes and where it stops

The refreshed official description identifies the discretized time-dependent Hamiltonian method, fixed-point optimization and numerical-error claims. It does not provide network sizes, equations, encoding, time steps, noise, circuit counts, measurement budget, classical baselines, runtime, output reconstruction or hardware execution.

The evidence supports a quantum numerical-solver proposal with reported error comparisons. It does not establish end-to-end speed, energy advantage, scalable power-system simulation or a runtime advantage over classical solvers.

[Observed paper card](../observed-subthemes/quantum-architectures-and-control.md#paper-dac-2026-research1963)

## OHQS: numerical error is not computational advantage

Power-system transient computation follows changing electrical quantities over time. An ordinary differential equation relates their rates of change to the current state and inputs. A numerical method approximates that evolution, so its accuracy depends on its representation, step sizes, and treatment of changing conditions.

[OHQS](../observed-subthemes/quantum-architectures-and-control.md#paper-dac-2026-research1963) proposes discretized time-dependent Hamiltonian evolution with a fixed-point-based optimizer to reduce discretization error. The description reports up to 99.91% accuracy and 9.56× error reduction against classical methods, without enough experimental detail to establish the error convention, networks, comparator, or hardware. Its claimed logarithmic qubit scaling with inverse error tolerance is not a runtime complexity result. [Official DAC description](https://63dac.conference-program.com/presentation/?id=RESEARCH1963&sess=sess133).

A complete comparison must count preparation of the encoded input, all circuit executions, and recovery of the required outputs. Producing a quantum representation of a solution is different from returning every voltage or current value at a specified precision. The manuscript remains needed before the quantitative claims can support more than this description-level account.

## The cross-paper insight and the longer-term question

These papers suggest a testable research question: do local improvements remain beneficial after their neighboring stages are included? Shorter extraction schedules may create more data per second. More efficient transmission may add buffering delay. Fewer code switches may increase time in an expensive code. Better initialization may spend more measurements before ordinary optimization begins.

That is an interpretation of this selected sample, not a measured historical trend or evidence of quantum advantage. A longitudinal study needs comparable tasks, error targets, device assumptions, and cost boundaries across editions. It should retain negative cases, including the transport compiler's fidelity–duration tradeoff and the syndrome paper's unequal error rates at equal depth.

The reader should be able to answer four concrete questions for every proposed improvement: what work disappears, what work is added, what accuracy or correctness condition is preserved, and which part of the complete computation was actually measured. A claim that cannot yet answer them remains bounded evidence, not a system-level conclusion.
