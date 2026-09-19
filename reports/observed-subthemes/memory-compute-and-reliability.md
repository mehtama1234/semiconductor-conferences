# Memory compute and reliability

This subject has 10 records in the selected sample. This page explains where it fits, then presents all captured paper evidence without shortening the measurements or limitations.

[Definitions used in the paper records](../reading-guide-v1.md)

## Understand the parent subject first

- [Memory interconnect and storage](../themes/memory-interconnect-and-storage.md)

## Storage and computation impose different demands on a device

A memory device must distinguish stored states when reading and preserve or restore the required state when writing. Using that device for computation can impose additional operations, access combinations, or timing requirements. A device that stores values adequately under ordinary use may behave differently under those operations.

The central question is how the proposed computation affects correctness under variation, noise, temperature, supply conditions, and repeated use. Performance has meaning only alongside the probability and consequence of producing an incorrect result under the stated conditions.

## Three kinds of error must remain separate

A stored bit can be corrupted. An arithmetic operation can produce an inaccurate result. A deliberately approximate representation can change a value even when the hardware operates as designed. These are different causes and may need different detection, correction, or application tolerances.

Adding protection does not remove the need to measure them separately. A code designed to correct certain storage errors may not establish the accuracy of an analog arithmetic operation. A model that tolerates some numerical approximation may still be vulnerable to particular correlated failures.

## Why the surrounding circuitry matters

A memory array requires address selection, signal generation, sensing, and transfer circuits. A compute-capable array may require additional arithmetic, conversion, and control. These circuits can determine total area and energy even when the core array operation appears inexpensive.

For this reason, compare both the array operation and the complete unit that makes its output usable. State whether input and output circuits are included. If a proposed improvement relies on a particular manufacturing process, account for that condition when comparing it with a different implementation.

<span id="explanation-dac-2026-research796"></span>

## Prism: reducing nearest-neighbor arithmetic must preserve the recall target while coordinating PIM and host work

### What approximate nearest-neighbor search computes

Nearest-neighbor search compares a query vector with database vectors using a distance or similarity function and returns the closest results. Exact search evaluates every relevant vector. Approximate search reduces work by pruning candidates, using an index or evaluating distances only partly, accepting that some true neighbors may be missed.

Recall measures how many of the reference nearest neighbors appear in the returned set. A throughput improvement without a recall target is incomplete because discarding more candidates can make the search faster while returning worse results.

### Why PIM changes the arithmetic tradeoff

Vector search moves many vector values and performs many distance operations. PIM can provide high internal bandwidth by placing computation near stored vectors, but its arithmetic resources and local storage are limited. A design that computes every distance fully can exhaust PIM arithmetic, while a design that prunes aggressively can damage recall.

Prism is described as co-optimizing vector pruning, distance evaluation and host-PIM orchestration. The relevant boundary includes index access, vector loading, partial distance computation, candidate transfer and global ranking, not only the PIM arithmetic kernel.

### What proximity-aware pruning and dual affiliations do

A proximity-aware pruner uses the query and an index relationship to exclude vectors unlikely to be close. The quality of this decision depends on the cluster geometry, distance metric, data distribution and approximation bound.

Dual-cluster affiliations associate a vector with two neighborhoods instead of forcing it into one. This can reduce false exclusion near cluster boundaries, but it adds metadata, storage, pruning checks and possibly duplicate candidate handling. The evaluation must report pruning rate, candidate overlap and recall after deduplication.

### What sensitivity-ordered distance computation changes

Distance can be accumulated in dimension segments. Prism evaluates segments in an order expected to reveal whether a candidate is promising. If a partial distance already exceeds a valid bound, the remaining segments need not be evaluated.

Early termination is safe only when the bound is valid for the metric, remaining dimensions and numerical precision. An empirical threshold can reduce work but may exclude a true neighbor. The system should report the fraction of candidates terminated at each stage, arithmetic saved, ranking changes and recall across query and dataset distributions.

### How host-PIM overlap affects throughput

The stall-free pipeline overlaps query preparation on the host, PIM execution and global ranking. This requires queues, buffers, transfer scheduling, completion signaling and backpressure. A stage can be mathematically independent and still stall because its buffer is full, a host link is busy or one PIM partition returns late.

End-to-end throughput should include query preparation, index access, host-PIM transfer, PIM computation, candidate return and global ranking. Peak stage throughput is not enough if pipeline fill, drain or tail behavior dominates short query batches.

### How to interpret the reported result

The captured description reports 2.7–19.8× higher throughput than state-of-the-art systems. It does not expose recall, dataset, vector dimension, distance metric, index construction, pruning rate, precision, PIM capacity, energy, area, latency or host-transfer boundaries.

The range may depend strongly on dataset geometry, query distribution, recall target and baseline implementation. A high-recall result needs exact-reference construction and a declared returned-neighbor count. Throughput and recall must be reported together for each configuration.

### What the record establishes and where it stops

The official description establishes a PIM-based ANNS co-design using proximity-aware pruning, dual-cluster affiliations, sensitivity-ordered distance evaluation, early termination and a host-PIM pipeline. It reports a throughput range over state-of-the-art systems. It does not expose recall, datasets, precision, capacity, absolute throughput, PPA or transfer conditions.

The [Prism](../observed-subthemes/memory-compute-and-reliability.md#paper-dac-2026-research796) record is evidence of a reported arithmetic-reduced PIM search system, not a recall-preserving general speedup. The explanation separates nearest-neighbor correctness, pruning, partial distance bounds, pipeline overlap and the conditions needed for a fair throughput comparison.

<span id="explanation-dac-2026-research529"></span>

## Onyx: PIM transaction processing must preserve commit semantics while moving records and work close to memory

### What a transaction has to guarantee

A transaction groups reads and writes into one logical operation. Atomicity means the operation commits as a whole or has no visible partial effect. Consistency means the committed state satisfies the database and application rules. Isolation defines what concurrent transactions can observe. Durability requires committed state to survive the specified failures.

PIM changes where the reads, writes and parts of the transaction execute. It does not remove the transaction protocol. A faster memory-side operation is not a valid transaction result if a concurrent client can observe an intermediate write, if two partitions commit inconsistently or if recovery loses a committed update.

### Why transaction processing is memory-bound

Many transaction workloads perform numerous dependent reads and writes. A record lookup may determine the next lookup, and a write can change the state seen by another transaction. The arithmetic per record is often small, while address generation, data movement, synchronization, cache or memory access dominates.

PIM offers aggregate bandwidth by placing processing units near memory. Onyx is described as running on a real UPMEM prototype. The benefit depends on where records reside, how transactions are partitioned, how a DPU reaches remote data and how results return to the host or another rank.

### What local-access orchestration changes

Onyx orchestrates transaction execution to maximize local accesses while balancing work across PIM processors. A local access stays within a DPU or rank's memory and avoids an inter-DPU or host transfer. Partitioning can reduce movement, but a transaction that spans partitions needs coordination and a rule for ownership and visibility.

The system must decide whether to move a transaction to its records, replicate records, send remote requests or split the transaction. Each choice affects contention, ordering, buffer use, communication and commit latency. A local-work percentage alone does not prove end-to-end transaction efficiency.

### Why load balance is more than transaction count

Transactions differ in the number of records they touch, the probability of conflicts, the amount of index work and the number of remote accesses. A skewed key or hot record can make one DPU a bottleneck even when transaction counts are equal.

Load-aware scheduling can use expected record count, locality, contention or transaction type to distribute work. Scheduling itself consumes metadata and may move work or state. If a transaction is reassigned after it has acquired locks or read a version, the system needs a safe handoff and visibility rule.

### What rank-level asynchronous transfer changes

Asynchronous transfer can overlap communication with computation that is ready on another rank. Rank-level queues can hold requests and completions so a DPU does not wait for every transfer before doing independent work.

The system needs ordering, backpressure, completion, retry and failure handling. A transaction cannot commit until all required reads are valid and all writes are made visible according to the isolation and durability model. Overlap can reduce idle time, but queues and coordination can increase tail latency or memory use under contention.

### How YCSB and TPC-C frame the workload

YCSB commonly represents key-value access patterns with configurable read, update, insert and scan mixes. TPC-C represents a more relational transaction workload with multiple operations, dependencies and contention. They exercise different locality, conflict and coordination behavior.

A comparison must state dataset size, request distribution, transaction mix, concurrency, isolation level, persistence, indexing, warm-up, failure behavior and whether host transfers and preprocessing are included. Average throughput can hide abort rate, tail latency or correctness failures.

### What the record establishes and where it stops

The official description establishes Onyx as a full-stack transaction-processing system on a real UPMEM PIM prototype. It identifies local-access orchestration, load balancing and rank-level asynchronous data transfer and names YCSB and TPC-C evaluation. It qualitatively claims significant outperformance but reports no throughput, latency, energy, abort, consistency, isolation, recovery or configuration results.

The [Onyx](../observed-subthemes/memory-compute-and-reliability.md#paper-dac-2026-research529) record is evidence of a reported PIM transaction system, not a quantified transactional-correctness or general performance conclusion. The explanation separates ACID guarantees, data placement, load balance, asynchronous communication, workload semantics and complete transaction measurement.

<span id="explanation-dac-2026-research2631"></span>

## ARC-SRAM: local addressing saves energy only when the access pattern and complete memory boundary are explicit

### Why random-access SRAM can waste energy on regular work

An SRAM read selects a row, develops a bitline signal and uses sensing circuitry to produce the stored value. A write drives the bitlines and activates the selected row to change the cell state. Address decoding, wordline drivers, precharge, bitline charging and output circuitry all consume energy.

Conventional SRAM is designed to permit arbitrary row selection. Image processing, computer vision, deep learning and dense linear algebra often access rows in regular loop nests. Repeating predictable address and activation work can consume a large part of the access energy even when the useful data movement is unchanged.

### What local address generation changes

ARC-SRAM moves address generation toward the memory periphery or subarray so a local controller can generate a sequence of row selections. The controller can exploit consecutive or otherwise regular accesses without repeatedly activating a global address path.

The local sequence must still preserve the requested order and handle loop boundaries, stride changes, random jumps, bank conflicts, resets and external requests. Local control adds state and logic and may become less useful when the workload loses regularity. A comparison must include the address generator and its synchronization, not only the row decoder it replaces.

### How the read schemes reduce activity

The design uses one wordline pulse per row and minimizes precharge activity to suppress half-selection energy. A shorter or more selective activation schedule can reduce wordline and bitline switching, but the sense amplifier must still receive a sufficient signal within the timing limit. Unselected cells must not be disturbed.

Read energy should be partitioned into address generation, decoder, wordline driver, precharge, bitline development, sense amplifier, output transfer and control. A cell-array-level result can omit or simplify periphery that determines the energy seen by the system.

### How the write scheme reuses bitline charge

The write method reuses bitline charge across consecutive rows. Instead of rebuilding the full electrical condition for every row, the design carries useful charge from one write to the next. The mechanism must specify how the charge is isolated, refreshed or reset and how it behaves for different data patterns and row distances.

Write correctness depends on write margin, leakage, device mismatch, voltage, temperature and timing. Charge reuse can lower switching energy while increasing state dependence or requiring control circuitry. The evaluation must test consecutive and non-consecutive rows, both data polarities, worst-case patterns and retention or disturb conditions.

### How to interpret the reported instance

The captured description reports a 64 KB ARC-SRAM instance in an advanced gate-all-around nanosheet 1.4-nm research PDK. At the cell-array level, it reports 63–76% read-energy reduction and 68–72% write-energy reduction for loop-nest-dominated applications, with 4% area overhead.

The exact baseline, absolute energy, latency, density, wire model, voltage, frequency, process corners and area boundary are not exposed. The 1.4-nm research-PDK result should not be treated as a measured production-silicon result or assumed to transfer to another SRAM cell, array size or process.

### What regularity means for the conclusion

The reported benefit is conditional on access regularity. A loop nest with predictable row progression can use local sequencing. A workload with random accesses, short bursts, frequent branch changes or interleaved requesters may spend more time switching control modes or falling back to global addressing.

Evaluation should report read/write mix, stride, burst length, row reuse, bank conflicts and the fraction of accesses handled by the optimized sequence. It should compare the same capacity, data, timing and complete peripheral boundary against global and banked SRAM.

### What the record establishes and where it stops

The official description establishes a local-address SRAM subarray that combines address-generation relocation, reduced read wordline/precharge activity and write bitline-charge reuse. It reports modeled cell-array energy reductions and area overhead for a 64 KB 1.4-nm research-PDK instance. It does not expose absolute energy, latency, density, capacity scaling, variation, yield, silicon status or full-periphery accounting.

The [ARC-SRAM](../observed-subthemes/memory-compute-and-reliability.md#paper-dac-2026-research2631) record is evidence of a regular-access SRAM architecture, not proof of lower energy for arbitrary memory traffic or a production-process result. The explanation separates address locality, read activation, write charge reuse, cell correctness and the complete measurement boundary.

<span id="explanation-dac-2026-research2378"></span>

## UBFP-IMC: wide floating-point in digital CIM moves the bottleneck from memory access into alignment, reduction and bit width

### What wide floating point has to preserve

A floating-point value stores a signed significand and an exponent. The significand carries precision; the exponent sets scale. Multiplication combines significands and adds exponents. Addition is more demanding: the operands must be shifted until their exponents match, then added or subtracted, normalized and rounded.

Scientific calculations often need more precision and range than low-bit AI inference. Increasing the mantissa width reduces rounding error, but it increases storage, partial-product count, carry handling, accumulation width and switching activity. The design must state the representation and numerical error target before an efficiency comparison has meaning.

### What bit-serial mantissa MACs change

UBFP-IMC processes mantissa bits over time rather than using a full-width parallel multiplier. A smaller repeated datapath can reduce area and local movement, but the number of cycles grows with the mantissa width and the bit schedule. The system must account for bit-plane reads, sign handling, partial-product accumulation and final normalization.

Five-signal Booth encoding recodes signed input groups to reduce the number of partial products. It can lower adder activity, but the encoding must preserve sign extension, correction terms and exact product semantics. The reduced partial-product count does not remove the cost of serial control or wide final accumulation.

### What carry-save accumulation contributes

A carry-save adder represents an intermediate result with separate sum and carry vectors. It postpones carry propagation, allowing several partial products to be combined without waiting for a full-width carry chain at every step.

A two-step carry-save structure can shorten an intermediate path, but a final carry-propagate operation is still needed. The full result also needs overflow handling, normalization, rounding and possibly sign correction. An accumulation-latency claim must say whether those operations and memory transfers are included.

### Why exponent alignment is a separate bottleneck

To add floating-point products, the smaller-exponent significand is shifted relative to the larger-exponent value. The exponent difference determines that shift. Large differences can discard low-order bits or create a value too small to affect the result, while close exponents require wider accurate addition.

UBFP-IMC uses an exponent-difference generator and FIFO adder tree for exponent-aligned accumulation. The FIFO can hold values until the reduction order and alignment conditions are ready. It also introduces storage, ordering, queue occupancy and possible stalls. A MAC array can be full while the accumulation module waits for compatible values or memory access.

### What the 28-nm design claim establishes

The captured description reports a 28-nm design with 168 MAC units and one accumulation module. It reports 4.43×, 4.46×, 4.30× and 8.53× energy-efficiency-factor improvements, 27× lower accumulation latency and an area advantage.

The exact reference point for each ratio, mantissa and exponent width, frequency, voltage, memory traffic, area boundary, process library and numerical error condition are not exposed. “Energy-efficiency factor” needs its numerator and denominator; accumulation latency needs the amount of work and whether bit-serial MAC, exponent alignment, FIFO wait, normalization and output access are included.

### What scientific-kernel validation must report

Scientific workloads should be evaluated using defined numerical error, convergence or solution-quality criteria, not only a local MAC error. Matrix dimensions, conditioning, accumulation order, precision, input range, overflow behavior and comparison implementation affect the result.

A wide-FP CIM macro can have an attractive arithmetic density while losing system efficiency to data movement, alignment storage, clocking or memory capacity. The evaluation should report those costs and compare the same numerical result and precision requirement against CPU/GPU and narrow-CIM baselines.

### What the record establishes and where it stops

The official description establishes a digital CIM architecture for wide floating-point mantissa MAC and exponent-aligned accumulation, with Booth encoding, carry-save reduction, a FIFO adder tree and a reported 28-nm 168-MAC implementation. It reports relative efficiency, latency and area claims. It does not expose bit widths, numerical accuracy, absolute throughput/energy/area, frequency, memory movement, FIFO behavior or baseline parity.

The [UBFP-IMC](../observed-subthemes/memory-compute-and-reliability.md#paper-dac-2026-research2378) record is evidence of a reported wide-floating-point CIM architecture, not proof of scientific-kernel accuracy or general system advantage. The explanation separates floating-point representation, serial mantissa work, carry handling, exponent alignment, memory hierarchy and the required numerical validation.

<span id="explanation-dac-2026-research2425"></span>

## COM-BNN/RES-BNN: serial binary MRAM-CIM trades instantaneous power for time and must expose its sensing conditions

### What binary convolution still has to compute

A convolution multiplies a local input window by weights and accumulates the products before producing an output. In a binary neural network, weights and activations take two encoded values. The multiply can be reduced to a bit comparison or XNOR-like operation, followed by a count and a signed transformation.

Binary arithmetic is simpler than full-precision multiplication, but the system still moves windows, reuses weights and activations, forms partial sums and applies the network's scaling or threshold. The representation and encoding determine whether an equality count maps directly to the required signed convolution result.

### What the MRAM-CIM array changes

MRAM stores a state through magnetic device behavior and produces a read signal that a sense circuit must distinguish. An MRAM-CIM array combines stored weights and incoming input signals near the memory cells. This can reduce movement to a separate arithmetic unit, but it makes device read margin, reference generation, variation, temperature, retention, write cost and endurance part of computation correctness.

The compute cell must deliver a reliable binary result across the intended current or voltage range. A low-power read that reduces the sense margin can increase error. A write or reconfiguration operation can consume more energy than the binary computation itself. Array efficiency therefore needs separate accounting for read, write, sense, control, input loading and output transfer.

### What serial operation changes

The captured source describes serial BNN computation with a temporal reconfigurable input and an Integrate-and-Fire adder. Instead of resolving a wide accumulation in one operation, the design processes contributions across time and accumulates them in a narrower state.

Temporal input reconfiguration selects which input contribution is presented at each step. The Integrate-and-Fire accumulator integrates those contributions and emits or infers a result when a defined threshold or complete sequence condition is reached. The exact threshold, reset behavior, bit encoding and output timing are not exposed in the captured evidence.

Serial computation can reduce parallel hardware, ADC width or instantaneous switching activity. It increases the number of cycles and may increase leakage, clock energy, buffering and input movement. Latency-power tradeoffs must therefore report mode, serial length, clock, completion condition, throughput and total energy per valid convolution.

### What Exact Result Inferring needs to define

The source names an Exact Result Inferring method for binary convolution. An exact result method must specify how the encoded binary products, signed offset and accumulated contributions map to the final convolution output. It must also state whether the method avoids an ADC, narrows the accumulator, predicts a threshold crossing or changes the schedule.

“Exact” describes mathematical equivalence under declared assumptions. It does not mean the MRAM sense operation is error-free. Device variation, a wrong binary read, temporal accumulation error or an incorrect reset can still produce a wrong output. The method's hardware overhead and error sensitivity need independent measurement.

### Why the name discrepancy remains visible

The catalog record is titled COM-BNN, while the captured official source calls the proposed design RES-BNN. Until the full paper or an authoritative program record reconciles the names, the explanation preserves both labels. A name mismatch can affect citation, source retrieval and comparison with other artifacts; it should not be silently normalized.

### How to interpret the reported power claims

The captured source reports up to 85% energy reduction and 83% power reduction versus ADC-based CIM baselines, dynamic latency-power tradeoffs and serial-mode power as low as 0.03%. It does not provide absolute power, energy per inference, accuracy, area, frequency, read/write cost, endurance, variation or silicon conditions.

The 0.03% figure especially requires the mode's execution time and work completed. Instantaneous power can fall while energy or latency rises. The baseline must use the same binary model, output correctness, memory movement, precision, clock and measurement boundary. ADC-based CIM also needs a complete peripheral comparison, including whether the proposed serial design moves conversion or accumulation cost elsewhere.

### What the record establishes and where it stops

The official description establishes a reported reconfigurable MRAM-CIM direction for binary convolution using serial computation, temporal input control, an Integrate-and-Fire accumulator and Exact Result Inferring. It reports relative power and energy claims and exposes a COM-BNN/RES-BNN naming discrepancy. It does not expose accuracy, absolute PPA, sensing margin, process variation, endurance, write cost or silicon validation.

The [COM-BNN/RES-BNN](../observed-subthemes/memory-compute-and-reliability.md#paper-dac-2026-research2425) record is evidence of a reported low-power binary-CIM proposal, not proof of a complete edge-inference advantage. The explanation separates binary mathematical work, MRAM sensing, serial latency, exact-result logic, naming uncertainty and the boundary of the power comparison.

<span id="explanation-dac-2026-research2123"></span>

## DyPamear: dynamic graph mining on PIM must balance irregular work, update visibility and DPU movement

### What dynamic graph pattern mining computes

A graph contains vertices and edges. A pattern query asks whether a specified arrangement of vertices and relationships occurs in the graph, and may enumerate or count the matching subgraphs. Dynamic mining repeats this work while edges or vertices are inserted, deleted or changed.

The computation is irregular because the number of neighbors differs by vertex and because candidate matches branch differently. A high-degree vertex can create many candidate intersections while another task finishes quickly. The data is also scattered in adjacency structures, so memory access, queueing and synchronization can dominate the set-intersection arithmetic.

### Why practical PIM changes the system boundary

Processing-in-memory places computation near stored graph data. DyPamear is built on UPMEM, a practical PIM platform with many data-processing units. The benefit depends on which graph structures reside in DPU memory, how tasks reach them, how DPUs communicate and how updates become visible.

PIM does not remove movement automatically. Graph loading, partition metadata, pattern inputs, intermediate candidates and final matches may cross the host–DPU or DPU–DPU boundary. A complete latency and energy result must state whether preprocessing, partitioning, loading, update propagation and result collection are included.

### What load-aware task distribution controls

Load-aware distribution assigns graph-pattern work using a cost estimate such as vertex degree, candidate count, intersection size or update activity. The purpose is to prevent one DPU from processing a large irregular task while other DPUs are idle.

The estimate can be stale when the graph changes. Computing it also costs memory access and control. Work may need to be split, migrated or combined, which adds queues and communication. Equal numbers of assigned tasks do not imply equal time because the tasks can have different degree and intersection behavior.

### What data-driven asynchronous execution changes

In a synchronous design, workers wait for a phase or barrier before starting dependent work. Data-driven asynchronous execution starts a task when its inputs and a suitable DPU resource are ready. This can hide memory latency and keep independent work active.

The design needs dependency tracking, queues, buffer limits, completion signals and an ordering rule for graph updates. Asynchrony cannot bypass a true dependency. If a newly inserted edge changes an adjacency list while a query is reading it, the system needs a snapshot, lock, version or another consistency rule. Otherwise a result may combine states from different graph versions.

### Why degree-adaptive set intersection matters

Pattern mining often intersects neighbor sets to find vertices satisfying multiple relationships. Intersecting a small set with a large set can use a different method from intersecting two large sets. The kernel can choose scan, merge, lookup or another granularity according to degree and expected work.

The adaptive choice must preserve duplicate handling, ordering, update visibility and result completeness. A method that reduces scans for static sorted lists may need extra work when updates make the representation unsorted or when version metadata is checked. The kernel's benefit should be reported by degree distribution and update pattern, not only as one average.

### How to interpret the reported speedups and scaling

The captured description reports average speedups of 267.38×, 82.52× and 8.78× over Cheetah, PimPam and PSMiner on real UPMEM hardware, and near-linear scaling to 20,480 DPUs. It also names a public source-code repository.

These large ratios need the graph sizes, pattern queries, update traces, baseline implementations, DPU count, preprocessing, host transfers, output collection, DPU utilization and consistency conditions. Near-linear scaling requires a definition of the measured work and an explanation of how graph partitioning, communication and memory capacity scale. A result on one degree distribution may not transfer to a graph with hubs or rapid updates.

### What the record establishes and where it stops

The official description establishes a full-stack UPMEM PIM co-design for dynamic graph pattern mining using load-aware distribution, data-driven asynchronous execution and degree-adaptive intersection. It reports real-hardware speedups and scaling claims and identifies public source code. It does not expose graph/update conditions, absolute throughput, preprocessing or transfer boundaries, energy, consistency, utilization or independent code reproduction.

The [DyPamear](../observed-subthemes/memory-compute-and-reliability.md#paper-dac-2026-research2123) record is evidence of a reported dynamic-graph PIM system, not a graph-distribution-independent speedup or a complete dynamic-consistency result. The explanation separates irregular graph work, PIM placement, load balancing, asynchronous scheduling, adaptive intersection and end-to-end measurement.

<span id="explanation-dac-2026-research2282"></span>

## BS-KMQ: nonlinear ADC references must follow activation distributions without hiding outliers or conversion cost

### What ADC quantization does in an IMC array

An in-memory-computing array produces an analog signal from stored values and applied activations. An analog-to-digital converter maps that signal range to a finite set of digital codes. The number and position of the ADC levels determine the reconstruction error.

A uniform quantizer divides the input range into equal intervals. That is simple, but it can waste levels where few values occur and create large error where the distribution changes rapidly. A nonlinear quantizer places narrower or wider intervals according to the observed distribution. Its quality depends on the calibration data and on whether deployment values follow the same distribution.

### Why ReLU and clamping create boundary mass

ReLU maps negative values to zero. Clamping maps values outside a permitted range to a boundary. Both operations can produce many repeated or nearly repeated values at an edge of the activation distribution.

If those edge values dominate clustering, K-means can place centers around the boundary mass and leave fewer useful centers for the interior range. The resulting quantizer may have low average error for calibration samples while poorly representing less frequent values that matter to later layers or rare inputs.

### What BS-KMQ changes

Boundary Suppressed K-Means Quantization removes selected boundary outliers before clustering so the retained samples provide more informative quantization levels. The resulting nonlinear references are implemented in a reconfigurable in-memory nonlinear ADC.

The method needs a defined boundary rule: which values are removed, how thresholds are chosen, whether the zero or clamp code is retained separately, and how deployment values outside the calibration range are handled. Removing an outlier during calibration does not make it impossible during inference. The ADC must still map, saturate or signal that value.

### What reconfigurable references cost

An in-memory nonlinear ADC changes comparator references or another transfer-function element so the code intervals are nonuniform. Reconfiguration requires reference storage, selection, switching and possibly calibration. The cost includes conversion time, comparator activity, reference-generation energy and control.

Fewer levels can reduce ADC area, conversion work or data movement. That benefit is valid only if quantization error, analog noise, mismatch, nonlinearity and drift remain within the network's tolerance. The evaluation must measure the ADC and the reference circuitry, not only count output levels.

### How quantization error becomes model accuracy

Quantization error is a local numerical difference. Model accuracy is an end-to-end task result after many layers use the quantized values. A local error can be amplified by a later normalization, attention operation or nonlinear function, while another layer may tolerate a larger error.

Post-training quantization uses a calibration and evaluation procedure without changing the trained weights. Low-bit finetuning can adapt the model to the quantization error, so post-training and finetuned results answer different questions. A fair comparison must keep model, dataset, calibration, bit allocation, training budget and accuracy metric explicit.

### How to interpret the reported results

The captured description reports at least 3× lower quantization error than linear, Lloyd–Max, CDF and K-means methods; a 7× area improvement over two prior works; post-training accuracy gains up to 66.8%, 25.4%, 66.6% and 67.7% on ResNet-18, VGG-16, Inception-V3 and DistilBERT versus linear quantization; competitive finetuned accuracy with 3/3/4/4-bit ADC levels; and ResNet-18 6/2/3-bit simulation up to 4× speedup and 24× energy efficiency over existing IMC accelerators.

These ratios need the absolute errors, accuracy definition, layer-wise bit allocation, ADC conversion cost, calibration, model list, process and variation conditions, reference-generation overhead and complete system boundary. A simulated system-level result is not the same as a measured ADC or silicon result.

### What the record establishes and where it stops

The official description establishes BS-KMQ as a boundary-aware nonlinear quantization method coupled to a reconfigurable in-memory nonlinear ADC. It reports quantization, area, model-accuracy and simulated system-level claims across named networks and bit settings. It does not expose calibration, variation, absolute ADC/macro PPA, reference overhead, silicon status or complete energy accounting.

The [BS-KMQ](../observed-subthemes/memory-compute-and-reliability.md#paper-dac-2026-research2282) record is evidence of a reported quantizer/ADC co-design, not proof of a universal IMC efficiency or accuracy advantage. The explanation separates distribution modeling, ADC transfer levels, local quantization error, end-to-end model quality and system cost.

<span id="explanation-dac-2026-research155"></span>

## AccelCIM: SRAM-CIM dataflow must include the memory hierarchy, not only the array operation

### What a CIM dataflow decides

Compute-in-memory places part of an operation inside or next to the memory that stores operands. In an SRAM CIM accelerator, a macro contains storage cells, wordlines, bitlines and compute or sensing circuits. The macro can process many values in parallel, but it has finite capacity, precision, bandwidth and conversion resources.

A model larger than the macro must be divided into tiles. The dataflow decides which weights, activations and partial sums remain local, when they move to another macro, and when they move to a larger memory or host. This determines whether the array spends time computing or waiting for data and whether intermediate results are repeatedly converted and transferred.

### Why macro and macro-array choices are different

At the macro level, the design may choose operand stationarity, bit-plane order, precision, row and column use, accumulation mode and conversion schedule. These choices affect valid-lane utilization, ADC/DAC activity, local storage and partial-sum accuracy.

At the macro-array level, the system chooses tile placement, inter-macro communication, reduction order, buffer sizes, multicast or broadcast paths and the assignment of layers or tensor dimensions. A macro can be efficient in isolation while the array is limited by links, buffers, synchronization or an uneven tile distribution.

The two levels interact. Increasing macro parallelism can raise arithmetic capacity while increasing interconnect traffic and conversion activity. Making a tile larger can improve reuse while exceeding local storage. A dataflow result must therefore state both the macro configuration and the array organization.

### Why large models expose the movement cost

If a DNN fits completely in the available CIM storage, weights may be loaded once and reused locally. Large LLMs generally exceed one macro or one on-chip array. Weight tiles must be loaded, activations may cross memory levels, and partial sums may be reduced across macros or retained until later stages.

Sequence length, batch, layer shape and reuse determine how often those transfers occur. A dataflow selected for a small model or one layer can become poor when the same model is partitioned across macros. The total result must include weight loading, activation movement, partial-sum movement, output transfer, conversion and idle cycles.

### What systematic exploration and simulation provide

AccelCIM is described as a framework that spans macro configurations and macro-array organizations. Cycle-accurate architectural simulation can model issue timing, stalls, buffers, transfers, synchronization and operation latency for a specified architecture. It can reveal bottlenecks that a peak TOPS calculation hides.

Post-layout PPA analysis estimates physical area, timing and power after a particular implementation has been laid out. It can capture effects absent from an abstract macro model, but it remains conditional on the process library, extraction, voltage, frequency, peripheral design, ADC/DAC model and activity assumptions.

The framework's conclusions are therefore bounded by its design space and models. A search cannot find a configuration it does not represent. A simulator cannot validate a macro model whose noise, conversion cost, calibration or memory behavior has not been measured. A post-layout estimate is not a silicon measurement.

### How to interpret the LLM application claim

The captured description says AccelCIM is applied to representative LLM applications and provides practical dataflow-design insights. It does not report numerical TOPS/W, area, accuracy, search cost, peripheral overhead or a ranking of specific dataflows.

The LLM study should identify model sizes, layers, sequence lengths, precision, sparsity, memory hierarchy, tiling, calibration, dataflow, hardware configuration and baseline mapping. It should separate compute time from weight movement, activation movement, partial-sum reduction, conversion and control. Without those details, “practical insights” establishes the study's purpose, not a universal best dataflow.

### What the record establishes and where it stops

The official description establishes a systematic SRAM-CIM dataflow-exploration framework covering CIM macro configurations and macro-array organizations, with cycle-accurate simulation, post-layout PPA analysis and representative LLM applications. It does not expose numerical PPA, search cost, peripheral overhead, calibrated macro behavior or specific mapping results.

The [AccelCIM](../observed-subthemes/memory-compute-and-reliability.md#paper-dac-2026-research155) record is evidence of a design-space methodology, not proof that one dataflow is optimal across CIM technologies, models or memory capacities. The explanation separates local array work, hierarchy-level movement, simulation, post-layout modeling and the limits of unreported results.

<span id="explanation-dac-2026-research1605"></span>

## MANTIS: microscaled block floating point must carry scale information through an analog SRAM-compatible MAC

### Why reduced precision needs a scale

Floating-point values represent a magnitude with a significand and a scale. Reducing the significand width saves storage and arithmetic, but a fixed narrow integer range cannot represent values whose magnitudes vary widely. Block floating point addresses this by sharing a scale across a group of values and storing lower-precision members relative to that scale.

Microscaling applies this idea to small vectors or blocks. The integer values can be processed efficiently, while a scale value preserves part of the dynamic range. The scale is not optional metadata: the group size, scale format, rounding, saturation and accumulation width determine the numerical result.

### What MANTIS separates

MANTIS performs vector integer multiply-accumulate operations in the analog charge domain and applies per-vector FP8 scaling digitally through microscaling. The analog array handles the repeated integer accumulation; the digital path supplies the scale needed to interpret the result.

This separation can make the analog operation simpler than directly implementing floating-point arithmetic in the array. It also creates a complete data path that includes scale storage, scale alignment, zero handling, overflow or saturation, accumulation range and conversion. TOPS/W for the integer MAC is not the same boundary as energy for a correctly scaled neural-network layer.

### What charge-domain accumulation means

In a charge-domain MAC, weighted contributions affect charge on capacitive nodes before an ADC converts the accumulated signal into a digital value. This can reduce repeated movement between memory and arithmetic, but the signal is affected by capacitor mismatch, thermal noise, reference accuracy, settling, nonlinearity and input range.

The ADC's effective number of bits describes usable resolution under a measurement condition, not simply the nominal code width. Accumulation depth and precision mode change the signal range and the required separation between adjacent results. Calibration and operating voltage can change the usable result, so the evaluation must state whether the reported ENOB is measured, simulated, calibrated and representative of the full MAC sequence.

### Why reusing the SAR ADC DAC matters

A successive-approximation-register ADC uses a DAC and a comparison sequence to resolve an analog input. MANTIS reuses the DAC in that ADC as both a bit-plane charge-domain accumulator and part of the conversion path. Reuse can reduce duplicated capacitors and circuitry, but it couples accumulation timing, capacitor settling, DAC linearity, reference generation and ADC scheduling.

The macro must define when the DAC accumulates, when it is reset, when the ADC begins conversion and how the partial state is isolated from the next operation. These phases contribute to latency and energy. Reusing the circuit also means that an error affecting conversion may affect accumulation, so the error budget must cover both functions.

### What SRAM compatibility does and does not prove

The description calls the design foundry-SRAM-compatible and reports a 4 kb macro in a commercially available 12-nm process operating at 0.8 V. Compatibility means the design is intended to fit the process and memory integration constraints; it does not automatically mean equal density, yield, retention, access timing or reliability to a conventional SRAM.

The added compute cells, DAC/ADC circuitry, references, calibration, control and input/output paths can dominate area and energy. A complete comparison must state whether TOPS/W includes ADC conversion, scaling, data movement, calibration and all active peripherals, and whether the 4 kb capacity includes metadata and unused cells.

### How to interpret the model results

The captured description reports 22.5 TOPS/W for MXINT3×MXINT3 through 6.43 TOPS/W for MXINT8×MXINT3, an 8-bit ADC with 7.62 ENOB, and 0.15 percentage-point accuracy degradation across multiple open-weight LLMs on MMLU 5-shot and HellaSwag 0-shot versus an MXINT8-activation × MXINT3-weight quantized baseline. It also reports MXINT6 or MXINT3 plus an FP8 scalar within ±0.3% of quantized models.

Those results need model names, calibration data, sequence lengths, layer coverage, token counts, precision conversion, ADC and peripheral energy, and the definition of the accuracy comparison. A small average model-quality change does not establish that every layer or distribution is equally robust, and a macro efficiency result does not establish complete accelerator efficiency.

### What the record establishes and where it stops

The official description establishes a 12-nm, 4 kb, 0.8 V mixed-signal SRAM-compatible CNM/CIM macro that combines analog integer MAC, digital microscaling and SAR ADC/DAC reuse. It reports ENOB, precision-dependent efficiency and end-to-end language-model evaluation. It does not expose frequency, area, calibration, process corners, yield, total peripheral accounting, silicon status or complete system comparison.

The [MANTIS](../observed-subthemes/memory-compute-and-reliability.md#paper-dac-2026-research1605) record is evidence of a reported mixed-signal macro and model evaluation, not proof that analog computation is invisible to all reduced-precision workloads or that the macro beats a full digital accelerator. The explanation separates scale metadata, analog accumulation, conversion resolution, SRAM integration and end-to-end quality.

<span id="explanation-dac-2026-research544"></span>

## DRCA: dual-rail DRAM logic must preserve sensing margin while adding compute and access circuitry

### What a DRAM bitline pair normally does

A DRAM cell stores charge in a capacitor. During a read, the cell shares charge with a bitline, creating a small voltage change. A complementary bitline and reference condition allow a sense amplifier to detect the difference, drive the signals to full levels and restore the cell.

The bitline pair is therefore part of both storage access and signal resolution. Its capacitance, leakage, coupling, device mismatch, activation timing and supply voltage affect whether the sense amplifier makes the correct decision. Using the pair for logic changes the sequence of activations and the electrical states that must remain distinguishable.

### What dual-rail compute changes

Dual-rail logic represents complementary information on both rails of the bitline pair. DRCA is described as using the two rails for both computation and data access instead of leaving one naturally available rail underused. Full-swing signaling can provide a larger logical separation after sensing, but it requires matched paths and additional control so the rails do not load or disturb one another unevenly.

The hardware cost is not limited to the compute cell. Contacts, transistor sizing, wordline control, sense-amplifier timing, restore behavior and peripheral drivers all affect area, energy and reliability. A dual-rail result must be checked during the operation and after the cell is restored for ordinary DRAM use.

### What DRCA-OR and DRCA-XOR provide

The description names DRCA-OR and DRCA-XOR as dual-contact compute cells. An OR cell must produce a one when either encoded input is one. An XOR cell must produce a one when the encoded inputs differ. The circuit implements these truth tables through charge sharing, transistor conduction or another array-level signal operation; the captured evidence does not disclose the exact sequence.

For each cell, a complete explanation needs the input encoding, activated rows or columns, intermediate voltage, sense threshold, output restore and behavior under repeated access. The truth table describes logical intent, but it does not establish that the voltage distributions remain separated under process, voltage, temperature, coupling and disturbance conditions.

### Why concurrent operations matter

Compound bitwise logic can require several intermediate operations. If the same bitline pair can perform compatible operations concurrently, the design may reduce activation count and intermediate transfers. That benefit depends on whether the intermediate signals remain distinguishable and whether inputs needed by later operations are preserved.

The control schedule must specify which wordlines are active, when sensing occurs, when state is restored and how the next operation receives the correct operands. A concurrent sequence that saves cycles but overwrites an input or leaves a disturbed cell unrestored is not a valid computation. Throughput must include initialization, sensing, restore, row activation and output access.

### How to interpret the reliability result

The captured description reports a 2.29× reduction in failure rate versus the most robust prior PIM design and superior average performance on basic bitwise operations. The absolute failure rates, failure definition, fault-injection or physical-variation model, voltage margins, temperature, process, timing, energy, area and peripheral boundaries are not exposed.

Failure rate must be tied to a defined operation and condition. A result under a simulated voltage sweep is different from measured silicon failures under process and temperature variation. Performance on basic OR or XOR operations is different from end-to-end compound logic when intermediate restore, data movement and error accumulation are included.

### What the record establishes and where it stops

The official description establishes a dual-rail DRAM compute-and-access direction using DRCA-OR and DRCA-XOR cells, full-swing complementary signaling and concurrent bitline-pair operations. It reports a relative failure-rate reduction and average basic-bitwise performance benefit. It does not expose absolute error, voltage margin, process/temperature coverage, latency, energy, area or complete peripheral cost.

The [DRCA](../observed-subthemes/memory-compute-and-reliability.md#paper-dac-2026-research544) record is evidence of a reported DRAM-PIM circuit scheme, not proof of silicon-level reliability or complete memory-system efficiency. The explanation separates bitline sensing, dual-rail representation, cell-level logic, concurrent scheduling and the physical conditions required for a reliability claim.

## What the selected records reveal

DRCA proposes a dual-rail compute-and-access scheme for bitwise logic in DRAM. The captured description names the scheme but does not establish its detailed encoding or measured error behavior. The useful evidence would identify which failure conditions it handles and the additional activation, storage, or circuit cost. [Recorded evidence](../observed-subthemes/memory-compute-and-reliability.md#paper-dac-2026-research544)

The 12-nm SRAM-compatible macro record concerns computation near memory using a microscaled block-floating-point format. Such a format groups numerical values with scale information. Its cost and output quality depend on the grouping and on hardware used around the array. The current description does not provide measured accuracy, area, energy, or yield sufficient to establish the combined result. [Recorded evidence](../observed-subthemes/memory-compute-and-reliability.md#paper-dac-2026-research1605)

Accelcim instead examines dataflow choices for SRAM-based computation. A dataflow specifies where intermediate values remain and when operations use them. A search can select different configurations depending on which array, transfer, and surrounding-circuit costs its model includes. Those modeling assumptions need calibration before interpreting the selected design as an improvement. [Recorded evidence](../observed-subthemes/memory-compute-and-reliability.md#paper-dac-2026-research155)

The ADC-based nonlinear-activation record changes how a nonlinear output is converted and quantized. Combining operations can reduce some steps, but the comparison must still establish the transfer function, numerical error, conversion cost, and sensitivity to device conditions. [Recorded evidence](../observed-subthemes/memory-compute-and-reliability.md#paper-dac-2026-research2282)

## How to assess the complete result

Specify the intended operation and its correct output, including any explicitly allowed approximation. Test relevant input distributions and difficult values. Sweep the physical conditions identified by the design and report error distributions, rather than only average numerical accuracy.

Measure throughput and energy for valid outputs with protection or correction enabled. Include extra information, retries, calibration, conversion, and fallback computation. If some behavior is simulated and other behavior is measured, preserve those boundaries in the results.

The research connection across these records is that memory-side efficiency depends on both data organization and valid physical operation. Their shared category does not establish that one paper's protection or accuracy result applies to another device. That transfer requires a common operating model and a checked mapping between the operations.

## Compare the results carefully

First identify the inputs and required output quality. Then identify the limited resource: time, memory, communication, energy, circuit area, or correctness coverage. Ask which part of the method reduces that cost and which new cost it adds. Compare numbers only when the experiments hold these conditions sufficiently similar.

A conference description may explain the proposal while omitting the full experiment. An author preprint link may have been coded from its abstract. The source classification does not by itself establish that every table was read. Missing locations remain visible below.

## Complete captured evidence

These are evidence records, not substitutes for the explanations above. Each record preserves its problem, proposed method, measurements, comparison conditions, and source limits. A populated record does not establish that its mechanism has been fully explained or independently verified.

<span id="paper-dac-2026-research544"></span>

### DRCA: Reliable Bitwise Logic in DRAM via Dual-Rail Compute and Access

DAC 2026 · Record: `dac-2026-research544`

[Read the step-by-step explanation](#explanation-dac-2026-research544)

**Updated source-backed reading card**

Reviewed 2026-09-08. Reconciles the DRCA card with the captured official DAC description; explains DRAM bitline-pair operation, dual-rail complementary signaling, compute-and-access cells, concurrent bitwise operations and the distinction between simulated reliability claims and complete memory-system cost.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

In-DRAM bitwise logic can be sensitive to voltage variation, coupling, sensing margin and disturbance because the operation uses storage-array signals for computation rather than only reading a stored bit.

**Mechanism / artifact:**

DRCA: dual-rail compute-and-access scheme using both complementary rails of a DRAM bitline pair, with DRCA-OR and DRCA-XOR dual-contact compute cells, full-swing signaling and concurrent operations on one bitline pair.

**Workload — the work tested:**

Basic bitwise OR and XOR and complex bitwise logic processing; process, voltage, temperature, disturbance pattern, data distribution, timing and operation mix are unspecified.

**Hardware and manufacturing assumptions:**

DRAM array with dual-contact compute cells and dual-rail access; cell geometry, sense amplifiers, bitline capacitance, process node, voltage, timing, area, activation energy and peripheral circuitry are unspecified.

**Baseline — the comparison method:**

Most robust prior PIM design

Single-rail DRAM compute

Host-side bitwise logic

Cell, voltage, timing, fault-injection, peripheral-cost and measurement boundaries are unspecified

**Reported measurements:**

The captured official description reports a 2.29× reduction in failure rate versus the most robust prior PIM design and superior average performance on basic bitwise operations; it does not report absolute error rate, voltage margin, latency, energy, area or temperature results.

**Limits on the conclusion:**

A DRAM bitline pair carries complementary signals associated with a cell and its reference or sensing path. A normal access uses the pair to develop a small voltage difference that a sense amplifier resolves and restores. In-memory computation changes the activation and combination sequence so the electrical state represents a logic result, making charge sharing, leakage, coupling and timing part of logical correctness.

Dual-rail signaling uses both complementary rails instead of leaving one rail underused. Full-swing signals can create a larger sensing margin than a small analog difference under some conditions, but the two rails require matched devices, additional contacts and control. Mismatch or unequal loading can reduce the expected benefit.

DRCA-OR and DRCA-XOR are named dual-contact compute cells. The evaluation must show the input encoding, activation sequence, sense-amplifier decision, restore behavior and how the cell's physical changes affect retention and ordinary DRAM access. A logic truth table is not enough to establish operation across process, voltage, temperature and disturbance conditions.

Concurrent operations on one bitline pair can reduce the number of sequential activations needed for a compound bitwise function. Concurrency is valid only if intermediate states remain distinguishable and the sense/restore sequence does not corrupt inputs needed by later operations. The timing schedule, reset or restore policy and data dependencies determine whether the throughput benefit survives in a full array.

The source reports a 2.29× failure-rate reduction and better average basic-bitwise performance against a prior PIM design, but does not expose absolute failure rates, voltage margins, fault distribution, temperature, process variation, latency, energy, area or peripheral costs. Dual rails and extra contacts may increase array area and activation energy; the record establishes a reported DRAM-PIM scheme, not silicon-level reliability or complete system efficiency.

**Source and location**

Evidence tier: Primary captured official DAC description only; no full paper extraction, dram cell/sense amplifier artifact reproduction or independent process variation, voltage margin, temperature, silicon, energy and peripheral cost validation. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH544)

DAC 2026 official description and data/review-packets/dac-2026-research544.json: single-bitline PIM limitation; complementary bitline-pair rails; DRCA-OR and DRCA-XOR dual-contact cells; full-swing dual-rail signaling; concurrent operations; 2.29× failure-rate reduction versus most robust prior PIM; superior average basic-bitwise performance; omitted absolute error, voltage, process, energy, area and temperature conditions.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** single-rail DRAM compute

host-side bitwise logic

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH544

**Hardware or process assumptions:** DRAM array supporting compute-in-memory operations and dual-rail access; technology and timing assumptions are unspecified.

**Limits:** No error rate, voltage margin, latency, energy, area, or temperature results are reported.

Dual-rail design may increase area and activation energy.

Official description only; silicon-level variation testing is required.

**Method or artifact:** Dual-rail compute-and-access scheme for reliable DRAM logic.

**Metrics:** Bitwise reliability and efficiency are claimed qualitatively

**Problem:** In-DRAM bitwise operations can be sensitive to variation, coupling, and reduced voltage margins.

**Workload or benchmark:** DRAM bitwise operations; process, voltage, disturbance, and baseline cells are unspecified.

</details>

<span id="paper-dac-2026-research1605"></span>

### Foundry-SRAM-Compatible Compute-Near-Memory Macro for Microscaled Block-FP in 12-nm CMOS

DAC 2026 · Record: `dac-2026-research1605`

[Read the step-by-step explanation](#explanation-dac-2026-research1605)

**Updated source-backed reading card**

Reviewed 2026-09-08. Reconciles the MANTIS card with the captured official DAC description; explains microscaled block floating point, MXINT arithmetic, FP8 scale handling, analog charge-domain accumulation, SAR ADC/DAC reuse, SRAM compatibility and the reported macro efficiency and end-to-end accuracy conditions.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Reduced-precision transformer inference needs both efficient integer arithmetic and enough dynamic range. Analog compute-in/near-memory methods must handle floating-point scale information without losing the efficiency of local accumulation or requiring an incompatible memory macro.

**Mechanism / artifact:**

MANTIS: a foundry-SRAM-compatible mixed-signal 12-nm CNM/CIM macro that performs vector integer MACs in the analog charge domain and applies per-vector FP8 scaling digitally through microscaling. It reuses the SAR ADC DAC as a bit-plane charge-domain accumulator and as part of the ADC.

**Workload — the work tested:**

Reduced-precision transformer workloads and open-weight LLMs evaluated on MMLU 5-shot and HellaSwag 0-shot; exact models, sequence lengths, calibration, token counts, layer coverage and software stack are unspecified.

**Hardware and manufacturing assumptions:**

Commercially available 12-nm CMOS, 4 kb SRAM-compatible macro operating at 0.8 V, 8-bit ADC with 7.62 ENOB; frequency, area, power boundary, peripheral overhead, process corners, yield and silicon measurement conditions are unspecified.

**Baseline — the comparison method:**

MXINT8 activation × MXINT3 weight quantized baseline

Digital SRAM-near-memory compute

Floating-point accelerator

Model, calibration, precision, memory traffic, peripheral inclusion and system measurement boundaries are unspecified

**Reported measurements:**

The captured official description reports 22.5 TOPS/W for MXINT3×MXINT3 through 6.43 TOPS/W for MXINT8×MXINT3, an 8-bit ADC with 7.62 ENOB, 0.15 percentage-point accuracy degradation across multiple open-weight LLMs versus an MXINT8×MXINT3 quantized baseline, and reduced-precision MXINT6/MXINT3 plus FP8-scalar results within ±0.3% of quantized models; exact measurement and model conditions are not fully exposed.

**Limits on the conclusion:**

Block floating point stores a shared scale for a group of values and lower-precision mantissas or integers for the members. Microscaling makes the scale metadata explicit: the integer MAC produces a local result, and the digital scale factors restore the represented magnitude. The group size, scale format, rounding, saturation and accumulation range determine the numerical error.

MANTIS uses MXINT values for the analog MAC and applies FP8 scaling digitally. This separates high-throughput integer accumulation from dynamic-range adjustment, but the scale path must remain synchronized with the vector, handle zero and overflow, and account for scale storage and movement. A result for the integer MAC alone does not establish the cost of the complete scaled operation.

Charge-domain accumulation combines analog charge contributions before the ADC resolves the result. The ADC's effective number of bits, capacitor mismatch, thermal noise, nonlinearity, reference accuracy and input range determine whether the accumulated value is distinguishable. The 8-bit nominal ADC and 7.62 ENOB must be interpreted with the accumulation depth, calibration, voltage and operating conditions.

Reusing the SAR ADC DAC as both a bit-plane accumulator and part of conversion can reduce duplicated circuitry, but it couples accumulation timing, capacitor settling, DAC linearity and ADC conversion scheduling. SRAM compatibility also requires the macro to fit the foundry memory constraints while adding compute cells and mixed-signal peripherals; compatibility alone does not establish equal density, yield or reliability to a standard SRAM.

The description reports a 4 kb, 0.8 V, 12-nm macro, 22.5 to 6.43 TOPS/W across precision modes, 7.62 ENOB and end-to-end MMLU/HellaSwag accuracy deltas. It does not expose frequency, area, total peripheral energy, calibration, process corners, yield, model list, layer coverage or silicon measurement boundary. The results establish a reported mixed-signal macro and model evaluation, not a complete system-level advantage over digital or floating-point accelerators.

**Source and location**

Evidence tier: Primary captured official DAC description only; no full paper extraction, macro/adc artifact reproduction or independent mixed signal, calibration, ppa, yield, silicon and end to end model validation. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH1605)

DAC 2026 official description and data/review-packets/dac-2026-research1605.json: MANTIS; 12-nm foundry-SRAM-compatible 4 kb macro at 0.8 V; analog charge-domain vector integer MAC; digital per-vector FP8 scaling via MXFP; SAR ADC DAC reuse; 8-bit ADC and 7.62 ENOB; 22.5 to 6.43 TOPS/W precision range; MMLU/HellaSwag accuracy results; omitted frequency, area, calibration, yield, peripheral and silicon conditions.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** digital SRAM-near-memory compute

floating-point accelerator

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH1605

**Hardware or process assumptions:** 12-nm foundry SRAM-compatible macro; voltage, frequency, precision, and measured silicon conditions are unspecified.

**Limits:** No TOPS/W, area, frequency, accuracy, yield, or peripheral overhead results are reported.

Block-FP scaling may introduce accuracy variation.

Official description only; measured silicon evidence is required.

**Method or artifact:** 12-nm CMOS compute-near-memory SRAM macro supporting microscaled block-FP.

**Metrics:** Macro efficiency and compatibility are claimed qualitatively

**Problem:** Efficient block-floating-point computation near standard SRAM requires compatibility with foundry processes and manageable peripheral cost.

**Workload or benchmark:** Neural-network block-FP workloads; macro dimensions, ADC/DAC, accuracy, and baselines are unspecified.

</details>

<span id="paper-dac-2026-research155"></span>

### Accelcim: Systematic Dataflow Exploration for SRAM Compute-in-Memory Accelerator

DAC 2026 · Record: `dac-2026-research155`

[Read the step-by-step explanation](#explanation-dac-2026-research155)

**Updated source-backed reading card**

Reviewed 2026-09-08. Reconciles the AccelCIM card with the captured official DAC description; explains SRAM-CIM capacity limits, macro and macro-array dataflow choices, off/on-chip movement, cycle-accurate simulation, post-layout PPA analysis and the limits of unreported exploration results.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

SRAM CIM can execute many operations near stored weights, but macro capacity is limited. Large DNN and LLM workloads therefore require transfers between macros, larger memory and possibly the host, making dataflow and placement central to total performance and energy.

**Mechanism / artifact:**

AccelCIM: systematic SRAM-CIM dataflow exploration spanning CIM macro configurations and macro-array organizations, evaluated with cycle-accurate architectural simulation and post-layout PPA analysis, and applied to representative LLM applications.

**Workload — the work tested:**

Representative LLM applications and DNN workloads; model sizes, layers, tensor shapes, precision, sparsity, sequence lengths, memory capacity and mapping constraints are unspecified.

**Hardware and manufacturing assumptions:**

SRAM CIM macros and macro arrays with analog/digital compute, on-chip memory hierarchy and off-chip movement; macro capacity, array dimensions, process, ADC/DAC, interconnect, frequency, voltage and peripheral models are unspecified.

**Baseline — the comparison method:**

Fixed SRAM-CIM dataflow

Digital accelerator mapping

DNN/CIM macro, precision, memory, process, simulator and PPA measurement boundaries are unspecified

**Reported measurements:**

The captured official description reports systematic design-space exploration, cycle-accurate architectural simulation, post-layout PPA analysis and LLM application study, but no TOPS/W, area, accuracy, search cost, peripheral result or numerical dataflow ranking is reported.

**Limits on the conclusion:**

A CIM macro performs part of a neural operation inside or next to the memory array. The macro has finite rows, columns, precision and conversion capacity, so a model larger than the available storage must be tiled and its weights, activations and partial sums moved between macros or external memory.

A dataflow defines where weights, activations and partial sums reside and when each moves. At the macro level it can choose which operand is stationary and how bit planes are processed. At the macro-array level it can choose tiling, placement, interconnect routes, reduction order and reuse across macros. These choices change array utilization, buffer occupancy, transfer volume, conversion count and synchronization.

Systematic exploration is useful only when the search space contains the relevant hardware and mapping choices. A cycle-accurate simulator can estimate stalls and movement for a defined architecture, while post-layout PPA analysis can estimate physical area, timing and power for a defined implementation. Neither result is independent of the macro model, peripheral assumptions, calibration and technology library.

Large LLMs make off-chip movement important because weights and activations may not fit in the CIM array. An efficient mapping must include weight loading, activation movement, partial-sum accumulation, sequence or batch reuse and output transfer. A dataflow that is best for a model fitting on chip may be poor when the model is partitioned across memory levels.

The description establishes a framework and evaluation method but reports no numerical TOPS/W, area, accuracy, search cost, peripheral overhead or dataflow ranking. Results may depend on model, precision, array capacity, technology and calibrated macro behavior; the record is evidence of a systematic exploration proposal, not a universal CIM dataflow conclusion.

**Source and location**

Evidence tier: Primary captured official DAC description only; no full paper extraction, simulator/design space artifact reproduction, calibrated cim macro, post layout database or independent ppa and LLM mapping validation. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH155)

DAC 2026 official description and data/review-packets/dac-2026-research155.json: SRAM-CIM density/efficiency; limited capacity and on/off-chip movement; macro-configuration and macro-array dataflow design space; cycle-accurate architectural simulation; post-layout PPA analysis; representative LLM applications; omitted numerical PPA, search, peripheral and ranking results.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** fixed CIM dataflow

digital accelerator mapping

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH155

**Hardware or process assumptions:** SRAM CIM macro with analog/digital compute and memory hierarchy; process and peripheral models are unspecified.

**Limits:** No TOPS/W, area, accuracy, search cost, or peripheral results are reported.

Dataflow rankings may be model- and technology-specific.

Official description only; calibrated macro evaluation is required.

**Method or artifact:** Systematic dataflow design-space exploration for SRAM CIM.

**Metrics:** Dataflow quality and exploration efficiency are claimed qualitatively

**Problem:** SRAM CIM dataflow choices couple array utilization, movement, precision, and peripheral overhead.

**Workload or benchmark:** Neural workloads mapped to SRAM CIM; array, precision, and search-space assumptions are unspecified.

</details>

<span id="paper-dac-2026-research2282"></span>

### In-Memory ADC-Based Nonlinear Activation Quantization for Efficient In-Memory Computing

DAC 2026 · Record: `dac-2026-research2282`

[Read the step-by-step explanation](#explanation-dac-2026-research2282)

**Updated source-backed reading card**

Reviewed 2026-09-08. Reconciles the BS-KMQ card with the captured official DAC description; explains ReLU/clamping edge accumulation, boundary-suppressed K-means levels, nonlinear in-memory ADC references, post-training and finetuning accuracy, and the distinction between ADC-level efficiency and complete IMC-system results.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

In-memory computing produces analog values that must be quantized by an ADC. ReLU and clamping can concentrate values near distribution boundaries, making ordinary clustering spend levels poorly and increasing quantization error.

**Mechanism / artifact:**

BS-KMQ: Boundary Suppressed K-Means Quantization that removes activation outliers near distribution boundaries before clustering to derive nonlinear quantization levels, implemented in a reconfigurable in-memory nonlinear ADC.

**Workload — the work tested:**

ResNet-18, VGG-16, Inception-V3 and DistilBERT; reported post-training quantization and low-bit finetuning settings include 6/2/3-bit ResNet-18 system simulation and 3/3/4/4-bit ADC levels, but calibration, layer coverage and data conditions are unspecified.

**Hardware and manufacturing assumptions:**

CIM macro with reconfigurable nonlinear ADC references; ADC resolution, array, process, voltage, frequency, conversion latency, variation, calibration, digital control and peripheral energy are unspecified.

**Baseline — the comparison method:**

Linear quantization

Lloyd–Max quantization

CDF quantization

K-means quantization

Two prior nonlinear-ADC works

Existing IMC accelerators

Model calibration, finetuning, ADC, array, system boundary and accuracy conditions are unspecified

**Reported measurements:**

The captured official description reports at least 3× lower quantization error than linear, Lloyd–Max, CDF and K-means methods; 7× area improvement over two prior works; up to 66.8%/25.4%/66.6%/67.7% higher post-training accuracy on ResNet-18/VGG-16/Inception-V3/DistilBERT versus linear quantization; competitive low-bit-finetuned accuracy at 3/3/4/4-bit ADC levels; and ResNet-18 6/2/3-bit system simulation up to 4× speedup and 24× energy efficiency over existing IMC accelerators. Exact boundaries are not exposed.

**Limits on the conclusion:**

An ADC maps a continuous or analog signal range to discrete digital codes. With a fixed number of levels, quantization error depends on where the levels are placed and on the distribution of values. A uniform quantizer allocates equal intervals; a learned quantizer places levels according to observed values.

ReLU maps negative values to zero and clamping limits values to a range. These operations can accumulate samples near zero or a clamp boundary. If those boundary samples dominate clustering, the learned centers may describe the boundary mass while giving too few useful levels to the interior or to less frequent but important values.

BS-KMQ removes boundary outliers before K-means clustering and derives nonlinear references for the ADC. That can make the level placement more informative for the retained distribution, but the removal rule, threshold, calibration distribution and treatment of values returned at inference must be specified. An outlier removed during calibration can still occur during deployment and saturate or map to a poor code.

A reconfigurable in-memory nonlinear ADC changes its reference levels or transfer function while staying coupled to the CIM array. The implementation must account for reference storage, switching, calibration, conversion time, comparator behavior, input range, noise, mismatch and the energy of the reconfiguration. Fewer ADC levels can reduce conversion cost, but only if the quantization error and analog nonidealities remain within the model's tolerance.

The description reports large quantization-error, area, accuracy, speedup and energy-efficiency improvements across named models and bit settings, but does not expose layer-wise calibration, ADC conversion cost, process/voltage variation, absolute area or energy, reference-generation overhead, accuracy definitions or complete system boundaries. The claims establish a reported quantization and ADC co-design, not a universal IMC advantage.

**Source and location**

Evidence tier: Primary captured official DAC description only; no full paper extraction, quantizer/adc artifact reproduction or independent calibrated macro, variation, accuracy, latency, area and system energy validation. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH2282)

DAC 2026 official description and data/review-packets/dac-2026-research2282.json: BS-KMQ boundary-suppressed K-means; ReLU/clamping edge accumulation; ≥3× quantization-error reduction; reconfigurable in-memory NL-ADC; 7× area improvement; ResNet-18/VGG-16/Inception-V3/DistilBERT post-training accuracy gains; 3/3/4/4-bit finetuned levels; ResNet-18 6/2/3-bit system simulation; up to 4× speedup and 24× energy efficiency; omitted ADC, calibration, variation and system boundaries.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** digital activation computation

separate CIM activation unit

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH2282

**Hardware or process assumptions:** CIM macro with integrated ADC and nonlinear quantization; process and peripheral assumptions are unspecified.

**Limits:** No accuracy, TOPS/W, area, latency, ADC overhead, or variation results are reported.

Quantized activations may amplify analog nonidealities.

Official description only; calibrated macro evaluation is required.

**Method or artifact:** ADC-based in-memory nonlinear activation quantization.

**Metrics:** CIM activation efficiency is claimed qualitatively

**Problem:** Nonlinear activation functions and conversion overhead limit efficient in-memory computing.

**Workload or benchmark:** Neural-network activation workloads; ADC, precision, array, and baselines are unspecified.

</details>

<span id="paper-dac-2026-research2123"></span>

### Dypamear: Efficient and Scalable Dynamic Graph Pattern Mining on Practical Processing-in-Memory Architecture

DAC 2026 · Record: `dac-2026-research2123`

[Read the step-by-step explanation](#explanation-dac-2026-research2123)

**Updated source-backed reading card**

Reviewed 2026-09-08. Reconciles the DyPamear card with the captured official DAC description; explains dynamic graph pattern matching, irregular adjacency access, UPMEM DPU placement, load-aware distribution, asynchronous execution, degree-adaptive intersection and the boundaries of the reported real-hardware speedups and scaling.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Dynamic graph pattern mining repeatedly traverses irregular adjacency structures while graph edges and vertices change. The computation is often limited by memory access, synchronization and load imbalance rather than arithmetic throughput.

**Mechanism / artifact:**

DyPamear: full-stack hardware-software co-design on UPMEM PIM, combining load-aware task distribution, data-driven asynchronous execution and a degree-adaptive set-intersection kernel to use DPU bandwidth and parallelism while handling architectural constraints.

**Workload — the work tested:**

Dynamic graph streams and graph-pattern queries; graph sizes, update rates, pattern types, degree distributions, correctness/consistency rules and query mix are unspecified.

**Hardware and manufacturing assumptions:**

Commercial UPMEM PIM platform with up to 20,480 DPUs; DPU memory capacity, inter-DPU communication, update consistency, host transfers, clock, energy, endurance and platform configuration are unspecified.

**Baseline — the comparison method:**

Cheetah

PimPam

PSMiner

CPU/GPU graph mining

Static PIM graph mining

Graph size, pattern, update trace, implementation, DPU count, preprocessing and end-to-end boundary are unspecified

**Reported measurements:**

The captured official description reports average speedups of 267.38×, 82.52× and 8.78× over Cheetah, PimPam and PSMiner, respectively, on real UPMEM hardware, and nearly linear scaling to 20,480 DPUs; it does not expose absolute throughput, update latency, energy, graph scale, consistency overhead or pattern-accuracy conditions.

**Limits on the conclusion:**

A graph-pattern query searches for a specified structural relationship among vertices and edges. Dynamic mining must incorporate inserted, deleted or changed edges without treating the graph as a static adjacency structure. The work includes irregular neighbor access, candidate generation, intersection and result maintenance.

Load-aware task distribution assigns work according to graph degree, candidate count or another cost estimate. This can prevent one DPU from receiving a high-degree or high-update task while others are idle, but the estimator and redistribution work consume memory access, control and communication. A balanced task count does not guarantee balanced execution time.

Data-driven asynchronous execution allows a DPU to issue work when its data and resources are ready instead of waiting for a global phase. It needs dependency tracking, queues, buffer capacity and a defined ordering for graph updates and results. Asynchrony can hide latency, but it cannot remove a true data dependency or an inter-DPU communication bottleneck.

Set intersection is central when a pattern query combines neighbor sets. A degree-adaptive kernel can choose different algorithms or granularities for small and large sets, reducing wasted scans. The choice must preserve duplicate handling, ordering, update visibility and result correctness under changing adjacency lists.

The source reports large average speedups over Cheetah, PimPam and PSMiner on real UPMEM hardware and near-linear scaling to 20,480 DPUs, but does not expose graph sizes, update traces, absolute throughput, preprocessing, host transfer, DPU utilization, energy, consistency or pattern-validation conditions. The results establish a reported full-stack PIM system, not a general speedup independent of graph distribution and dynamic-update workload.

**Source and location**

Evidence tier: Primary captured official DAC description and named public source code url; no full paper extraction, code execution, dynamic trace reproduction or independent throughput, consistency, energy and scaling validation. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH2123)

DAC 2026 official description and data/review-packets/dac-2026-research2123.json: dynamic graph pattern mining; irregular/data-intensive memory bottleneck; UPMEM practical PIM; load-aware task distribution; data-driven asynchronous execution; degree-adaptive set intersection; real UPMEM hardware; 267.38×/82.52×/8.78× average speedups over Cheetah/PimPam/PSMiner; near-linear scaling to 20,480 DPUs; source-code URL; omitted graph, update, throughput, energy, consistency and boundary conditions.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** CPU/GPU graph mining

static PIM graph mining

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH2123

**Hardware or process assumptions:** Processing-in-memory array with graph storage and update support; technology and consistency assumptions are unspecified.

**Limits:** No throughput, update latency, energy, area, graph scale, or pattern accuracy results are reported.

PIM updates may complicate consistency and endurance.

Official description only; dynamic-trace validation is required.

**Method or artifact:** PIM architecture for scalable dynamic graph pattern mining.

**Metrics:** Graph-mining efficiency is claimed qualitatively

**Problem:** Dynamic graph pattern mining is dominated by irregular traversal and data movement.

**Workload or benchmark:** Dynamic graph streams and pattern queries; graph sizes, memory technology, and baselines are unspecified.

</details>

<span id="paper-dac-2026-research2425"></span>

### COM-BNN: A Configurable Low Power MRAM-Based Computing-in-Memory Accelerator for Binary Convolutional Computations

DAC 2026 · Record: `dac-2026-research2425`

[Read the step-by-step explanation](#explanation-dac-2026-research2425)

**Updated source-backed reading card**

Reviewed 2026-09-08. Reconciles the COM-BNN card with the captured official DAC description, which calls the artifact RES-BNN; explains binary convolution, MRAM-CIM sensing, serial computation, temporal input reconfiguration, Integrate-and-Fire accumulation, Exact Result Inferring and the limits of the reported power/energy reductions.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Tiny edge devices have limited power, memory bandwidth and compute resources, while convolutional neural networks require repeated weight and activation operations. Binary neural networks simplify values and arithmetic, but still need efficient movement and accumulation hardware.

**Mechanism / artifact:**

The captured source calls the design RES-BNN, while the catalog card title calls it COM-BNN. It describes a lightweight reconfigurable MRAM-based CIM accelerator with serial BNN computation, temporal reconfigurable input, an Integrate-and-Fire adder for serial MACs and an Exact Result Inferring method for binary convolutions.

**Workload — the work tested:**

Binary convolutional neural networks on resource-constrained edge devices; model, layer shapes, bit encoding, serial length, accuracy, MRAM array size and workload schedule are unspecified.

**Hardware and manufacturing assumptions:**

MRAM-based CIM macro with configurable dataflow and serial sensing/accumulation; MRAM technology, write/read energy, sense margin, process, voltage, frequency, area, endurance and variation conditions are unspecified.

**Baseline — the comparison method:**

ADC-based CIM

Digital binary accelerator

Fixed-function MRAM CIM

Model, precision, serial mode, peripheral inclusion, clock, power and energy boundaries are unspecified

**Reported measurements:**

The captured official description reports up to 85% energy reduction and 83% power reduction versus ADC-based CIM baselines, dynamic latency-power tradeoffs and serial-mode power as low as 0.03%; it does not expose absolute power, energy, accuracy, area, frequency, endurance or silicon conditions.

**Limits on the conclusion:**

A binary neural network represents weights and activations with two values, so a binary multiply can become an equality or XNOR-like bit operation followed by a population count or signed accumulation. The simplification reduces arithmetic complexity but does not remove convolutional data movement, partial sums, input reuse or output scaling.

MRAM stores state through a magnetic device whose read signal and write operation have distinct energy, timing, variation and endurance behavior. An MRAM-CIM design must sense the stored state and combine it with input signals without making the read margin too small. Array-level binary logic does not establish correct operation across device variation, temperature, retention or repeated writes.

Serial BNN computation processes bits or input contributions over multiple time steps instead of resolving all contributions in one wide parallel conversion. Temporal input reconfiguration selects which input information is presented at each step, while an Integrate-and-Fire adder accumulates the partial result and emits or infers a result when a threshold or complete sequence is reached.

Serial operation can lower instantaneous power and hardware width while increasing latency. A dynamic latency-power tradeoff requires a defined mode, serial length, completion condition, clock, throughput and quality target. Power falling to 0.03% in serial mode cannot be interpreted as an end-to-end energy result without the longer execution time, input/output movement, control and memory access included.

Exact Result Inferring is described as improving binary-convolution efficiency, but the captured source does not define the inference rule, operand encoding, error behavior or hardware cost. The source also names RES-BNN while the catalog title says COM-BNN, so the alias must remain visible until reconciled against the full paper. No accuracy, TOPS/W, area, endurance, variation or silicon result is reported; the record establishes a reported low-power BNN-CIM direction, not a complete edge inference advantage.

**Source and location**

Evidence tier: Primary captured official DAC description only; title/artifact alias unresolved; no full paper extraction, mram macro artifact reproduction or independent binary accuracy, sensing, variation, endurance, ppa and silicon validation. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH2425)

DAC 2026 official description and data/review-packets/dac-2026-research2425.json: source title/artifact name RES-BNN versus catalog COM-BNN; MRAM-based CIM; serial BNN; temporal reconfigurable input; Integrate-and-Fire adder; Exact Result Inferring; 85% energy and 83% power reduction versus ADC-based CIM; 0.03% serial-mode power; omitted accuracy, absolute PPA, area, endurance, variation and silicon conditions.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** digital binary accelerator

fixed-function MRAM CIM

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH2425

**Hardware or process assumptions:** MRAM CIM macro with configurable dataflow; device variation, sensing, and process assumptions are unspecified.

**Limits:** No accuracy, TOPS/W, area, endurance, variation, or silicon results are reported.

MRAM sensing and write costs may dominate.

Official description only; measured macro validation is required.

**Method or artifact:** Configurable MRAM-based binary CIM accelerator.

**Metrics:** Low-power BNN efficiency is claimed qualitatively

**Problem:** Binary neural networks need configurable, energy-efficient memory-centric convolution hardware.

**Workload or benchmark:** Binary convolutional networks; MRAM technology, models, precision, and baselines are unspecified.

</details>

<span id="paper-dac-2026-research2378"></span>

### UBFP-IMC: Ultralarge Bit-Width Digital Floating-Point In-Memory Computing Accelerator for Scientific Computing

DAC 2026 · Record: `dac-2026-research2378`

[Read the step-by-step explanation](#explanation-dac-2026-research2378)

**Updated source-backed reading card**

Reviewed 2026-09-08. Reconciles the UBFP-IMC card with the captured official DAC description; explains wide floating-point mantissa cost, bit-serial MAC structure, Booth encoding, carry-save accumulation, exponent alignment, FIFO reduction and the limits of the reported EEF, latency and area claims.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Scientific computing needs a wider numerical range and precision than low-precision AI workloads, but wide floating-point mantissas increase arithmetic area, switching and latency, while exponent alignment and accumulation add peripheral work.

**Mechanism / artifact:**

UBFP-IMC: digital SRAM-CIM accelerator using an ultralarge-bit-width bit-serial mantissa MAC with 5-signal Booth encoding and a two-step carry-save adder, plus an exponent-aligned accumulation module with an exponent-difference generator and FIFO adder tree.

**Workload — the work tested:**

Scientific computing and numerical matrix kernels; mantissa/exponent widths, numerical error target, matrix shapes, sparsity, memory hierarchy and baseline implementations are unspecified.

**Hardware and manufacturing assumptions:**

28-nm digital CIM design with 168 MAC units and one accumulation module; SRAM organization, voltage, frequency, area boundary, memory capacity, interconnect and process-library conditions are unspecified.

**Baseline — the comparison method:**

CPU/GPU floating-point compute

Narrow-precision CIM

Conventional wide floating-point MAC

Bit width, frequency, workload, memory traffic, area, energy and accuracy boundaries are unspecified

**Reported measurements:**

The captured official description reports 4.43×, 4.46×, 4.30× and 8.53× energy-efficiency-factor improvements, 27× lower accumulation latency and an area advantage for a 28-nm design with 168 MAC units and one accumulation module; exact reference points and conditions are not exposed.

**Limits on the conclusion:**

A floating-point value combines a signed significand with an exponent. Multiplication combines significands and adds exponents; addition first aligns exponents, shifts one significand, adds or subtracts, then normalizes and rounds. Increasing mantissa width improves representational precision but increases storage, partial-product and reduction work.

Bit-serial mantissa MACs process mantissa bits across cycles instead of building a full-width parallel multiplier. The approach can reuse a smaller datapath and control switching, but latency grows with bit width and the input/weight bit schedule. A 5-signal Booth encoding can reduce partial products by recoding signed groups, while the encoding, sign extension and correction terms must preserve the exact product.

A carry-save adder stores a sum and carry without propagating carries at every intermediate step. A two-step carry-save structure can shorten the critical path and defer carry propagation, but the final carry resolution, bit width, overflow, normalization and rounding remain part of the full MAC result.

Exponent-aligned accumulation needs the exponent difference to determine a shift before combining significands. A FIFO adder tree can hold values until compatible alignment and reduction occur, but it adds storage, control, ordering and possible stalls when exponents vary. Alignment traffic and queue occupancy can dominate even when the mantissa MAC is efficient.

The description reports relative EEF, accumulation-latency and area improvements for a 28-nm 168-MAC design, but does not expose bit widths, numerical accuracy, frequency, absolute throughput/energy/area, memory movement, FIFO occupancy, process/voltage conditions or baseline parity. The result establishes a reported wide-FP digital-CIM architecture, not proof of scientific-kernel accuracy or general system advantage.

**Source and location**

Evidence tier: Primary captured official DAC description only; no full paper extraction, wide fp cim artifact reproduction or independent numerical kernel, timing, ppa, memory and process validation. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH2378)

DAC 2026 official description and data/review-packets/dac-2026-research2378.json: scientific wide-FP challenge; ultralarge mantissa; bit-serial mantissa MAC; 5-signal Booth encoding; two-step carry-save adder; exponent-difference generator; FIFO adder tree; 28 nm; 168 MAC units and one accumulation module; 4.43×/4.46×/4.30×/8.53× EEF, 27× accumulation latency and area claims; omitted bit width, numerical, PPA, memory and baseline conditions.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** CPU/GPU floating-point compute

narrow-precision CIM

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH2378

**Hardware or process assumptions:** Digital CIM array supporting wide floating-point operations; area, voltage, and process assumptions are unspecified.

**Limits:** No numerical accuracy, throughput, energy, area, or bit-width results are reported.

Wide arithmetic may dominate area and switching cost.

Official description only; numerical-kernel validation is required.

**Method or artifact:** Digital floating-point in-memory accelerator with ultralarge bit widths.

**Metrics:** Scientific-computing efficiency is claimed qualitatively

**Problem:** Scientific workloads need wide precision while memory movement limits digital accelerators.

**Workload or benchmark:** Scientific matrix and numerical kernels; precision, memory, and baselines are unspecified.

</details>

<span id="paper-dac-2026-research2631"></span>

### ARC-SRAM: A Memory Subarray with Local Addressing and Reduced Access Energy

DAC 2026 · Record: `dac-2026-research2631`

[Read the step-by-step explanation](#explanation-dac-2026-research2631)

**Updated source-backed reading card**

Reviewed 2026-09-08. Reconciles the ARC-SRAM card with the captured official DAC description; explains regular-access energy waste, local address generation, one-pulse wordline reads, precharge/half-selection suppression, bitline-charge reuse for writes and the boundaries of the reported 64-KB, 1.4-nm PDK energy and area claims.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Conventional random-access SRAM can activate global address and row circuitry even when an application accesses rows in a regular loop. Decoder, wordline, precharge and bitline activity then consumes energy unrelated to the useful data transfer.

**Mechanism / artifact:**

ARC-SRAM: a local-addressing SRAM subarray combining periphery-relocated address generation, one-wordline-pulse-per-row reads, reduced precharge and half-selection activity, bitline-charge reuse across consecutive-row writes and reduced wordline activation.

**Workload — the work tested:**

Loop-nest-dominated image processing, computer vision, deep learning and dense linear algebra access patterns; array dimensions, stride, burst length, read/write mix, data retention and workload traces are unspecified.

**Hardware and manufacturing assumptions:**

64 KB SRAM instance using an advanced gate-all-around nanosheet 1.4-nm research PDK; cell array, local decoder, voltage, frequency, wire model, variation, density and peripheral boundaries are unspecified.

**Baseline — the comparison method:**

Conventional globally addressed SRAM

Banked SRAM

The same capacity, access sequence, voltage, frequency, wire, decoder, precharge, peripheral and area boundaries are unspecified

**Reported measurements:**

The captured official description reports 63–76% cell-array-level read-energy reduction, 68–72% write-energy reduction in loop-nest-dominated applications and 4% area overhead for a 64 KB 1.4-nm-PDK instance; it does not report absolute energy, latency, density, yield or silicon results.

**Limits on the conclusion:**

A conventional SRAM is designed for arbitrary row selection. A global decoder drives the selected wordline and associated precharge, sense and bitline circuits. Under a regular loop, neighboring rows may be accessed repeatedly, so decoder and activation work can be repeated even when the access pattern could be predicted.

Relocating address generation to the memory periphery or subarray can exploit locality by generating a local sequence of row selections. The control must preserve the requested order, handle loop boundaries, random jumps, bank conflicts and interactions with external addresses. Local control can reduce activity while adding state, synchronization and capacity-specific logic.

For reads, one wordline pulse per row and reduced precharge activity aim to avoid repeated activation and half-selection energy. The sense path must still develop and resolve the bitline signal within the timing budget, and unselected cells must remain undisturbed. Read energy should separate wordline, decoder, precharge, bitline, sense-amplifier, output and address-control components.

For writes, reusing bitline charge across consecutive rows can reduce the energy needed to establish the next write condition. The design must state how the charge is retained, isolated and reset, and how leakage, data pattern, row distance, write polarity and consecutive-row timing affect correctness. Minimizing wordline activation can lower energy but may change write margin and disturb behavior.

The description reports 63–76% read and 68–72% write cell-array-level energy reduction with 4% area overhead in a 64 KB 1.4-nm research-PDK instance. It does not expose absolute energy, latency, density, capacity-scaling cost, variation, yield, silicon status or complete periphery accounting. The result establishes a regular-access SRAM architecture and modeled claims, not a general random-access or production-process advantage.

**Source and location**

Evidence tier: Primary captured official DAC description only; no full paper extraction, sram circuit artifact reproduction or independent voltage, variation, timing, density, yield, silicon and complete periphery validation. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH2631)

DAC 2026 official description and data/review-packets/dac-2026-research2631.json: regular access energy waste; address generation moved to memory periphery; one wordline pulse per row; minimized precharge/half-selection; bitline charge reuse across writes; minimized wordline activation; 64 KB; 1.4-nm gate-all-around nanosheet research PDK; 63–76% read and 68–72% write cell-array energy reduction; 4% area overhead; omitted absolute, latency, density, yield and silicon conditions.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** conventional globally addressed SRAM

banked SRAM

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH2631

**Hardware or process assumptions:** SRAM subarray and local decoder; voltage, frequency, process, and variation assumptions are unspecified.

**Limits:** No access energy, area, density, latency, yield, or silicon results are reported.

Local addressing may complicate capacity scaling and control.

Official description only; measured macro validation is required.

**Method or artifact:** SRAM subarray with local addressing and reduced activation.

**Metrics:** Access-energy reduction is claimed qualitatively

**Problem:** Global wordline and decoder activity contributes substantially to SRAM access energy.

**Workload or benchmark:** SRAM read/write workloads; technology, density, and baselines are unspecified.

</details>

<span id="paper-dac-2026-research529"></span>

### Onyx: Efficient Transaction Processing with Real Processing-in-Memory Prototypes

DAC 2026 · Record: `dac-2026-research529`

[Read the step-by-step explanation](#explanation-dac-2026-research529)

**Updated source-backed reading card**

Reviewed 2026-09-08. Reconciles the Onyx card with the captured official DAC description; explains transaction atomicity, consistency, isolation and recovery concerns, UPMEM PIM placement, local-access orchestration, load balancing, rank-level asynchronous transfer and the limits of the unquantified YCSB/TPC-C comparison.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Transaction processing performs many reads and writes that must appear as an all-or-nothing operation, creating memory-bandwidth, synchronization and data-movement bottlenecks. PIM offers bandwidth but can lose the benefit through imbalance and transfers among processors.

**Mechanism / artifact:**

Onyx: a high-throughput transaction-processing system running on a real UPMEM PIM prototype, orchestrating transaction workflow for local accesses and balanced PIM-processor work, with rank-level asynchronous data transfer to reduce communication overhead.

**Workload — the work tested:**

Real-world YCSB and TPC-C transaction benchmarks; dataset size, transaction mix, contention, skew, isolation level, durability model, DPU count and result-validation method are unspecified.

**Hardware and manufacturing assumptions:**

Real UPMEM PIM prototype with memory-side transaction execution and rank-level transfer; DPU memory, interconnect, host involvement, persistence, coherence, fault recovery, clock, energy and capacity conditions are unspecified.

**Baseline — the comparison method:**

State-of-the-art transaction-processing systems

CPU database processing

Simulated PIM transaction engine

Database configuration, data set, concurrency, isolation, persistence, hardware and end-to-end measurement boundaries are unspecified

**Reported measurements:**

The captured official description qualitatively claims that Onyx significantly outperforms state-of-the-art transaction-processing systems on YCSB and TPC-C using real UPMEM hardware; no throughput, latency, energy, transaction-abort, consistency or capacity numbers are reported.

**Limits on the conclusion:**

A transaction groups reads and writes so other clients observe an allowed state transition rather than a partial update. Atomicity requires commit or rollback behavior; consistency requires application and database invariants; isolation defines what concurrent transactions can observe; durability requires recovery after failure. Moving execution into memory does not remove these requirements.

PIM transaction processing must place records and transaction work so most reads and writes remain local to a DPU or rank. Locality can reduce host and inter-DPU traffic, but partitioning creates ownership, remote-access and hot-record problems. A transaction touching multiple partitions needs an ordering, coordination or commit protocol that can become the bottleneck.

Onyx uses workflow orchestration to maximize local accesses while balancing PIM processors. Load balance is not only equal transaction counts: transaction sizes, record locality, contention, abort probability and skew determine work. Moving a hot record or transaction can improve compute balance while increasing communication and consistency coordination.

Rank-level asynchronous data transfer can overlap communication with ready computation. It requires queues, ordering, backpressure, completion and failure handling. Asynchronous transfer must not allow a transaction to commit before all required writes are visible under the stated consistency and durability model.

YCSB represents key-value transaction access patterns, while TPC-C represents a more relational, multi-operation workload with dependencies and contention. The source names both real-world benchmarks and a real UPMEM prototype but reports no throughput, latency, energy, abort rate, isolation level, persistence, recovery, capacity or configuration. The result establishes a reported PIM transaction system and qualitative comparison, not a quantified transactional correctness or general performance conclusion.

**Source and location**

Evidence tier: Primary captured official DAC description only; no full paper extraction, upmem code execution or independent transactional correctness, isolation, recovery, throughput, energy and scaling validation. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH529)

DAC 2026 official description and data/review-packets/dac-2026-research529.json: all-or-nothing transactions; read/write memory bandwidth bottleneck; PIM bandwidth; load imbalance and PIM-processor transfer cost; Onyx real UPMEM prototype; local-access workflow orchestration; load balance; rank-level asynchronous transfer; YCSB/TPC-C evaluation; qualitative outperformance claim; omitted transaction, consistency, recovery, throughput and energy conditions.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** CPU database processing

simulated PIM transaction engine

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH529

**Hardware or process assumptions:** Real PIM prototype with memory-side transaction operations; persistence and coherence assumptions are unspecified.

**Limits:** No throughput, latency, energy, consistency, capacity, or prototype details are reported.

PIM execution may complicate isolation and recovery.

Official description only; transactional correctness validation is required.

**Method or artifact:** Processing-in-memory transaction-processing prototype.

**Metrics:** Transaction efficiency is claimed qualitatively

**Problem:** Transaction processing is limited by data movement and synchronization across memory and compute.

**Workload or benchmark:** Database transaction workloads; PIM technology, consistency, and baselines are unspecified.

</details>

<span id="paper-dac-2026-research796"></span>

### Prism: Reducing Arithmetic for High-Recall Approximate Nearest Neighbor Search on Processing-in-Memory

DAC 2026 · Record: `dac-2026-research796`

[Read the step-by-step explanation](#explanation-dac-2026-research796)

**Updated source-backed reading card**

Reviewed 2026-09-08. Reconciles the Prism card with the captured official DAC description; explains approximate nearest-neighbor ranking, proximity-aware pruning, dual-cluster affiliation, sensitivity-ordered distance evaluation, early termination and host-PIM pipeline overlap while preserving the missing recall and hardware conditions.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Large-scale approximate nearest-neighbor search is limited by moving many vectors and computing distances. PIM supplies internal bandwidth but has limited arithmetic, so reducing unnecessary distance work must not remove true nearest neighbors at the target recall.

**Mechanism / artifact:**

Prism: PIM-based ANNS system co-optimizing vector pruning, distance evaluation and host-PIM orchestration, using a proximity-aware vector pruner, dual-cluster affiliations, sensitivity-ordered dimension segments, early candidate termination and a stall-free pipeline for query preparation, PIM execution and global ranking.

**Workload — the work tested:**

High-recall approximate nearest-neighbor vector search; dataset, vector dimension, distance metric, query count, cluster structure, recall target, candidate count and index construction are unspecified.

**Hardware and manufacturing assumptions:**

PIM array with host orchestration and approximate distance computation; PIM capacity, compute precision, memory bandwidth, host link, process, frequency, energy and area conditions are unspecified.

**Baseline — the comparison method:**

State-of-the-art ANN systems

GPU/CPU ANN search

Full-arithmetic PIM search

Dataset, index, distance metric, recall target, hardware, precision, preprocessing, ranking and measurement boundaries are unspecified

**Reported measurements:**

The captured official description reports 2.7–19.8× higher throughput than state-of-the-art systems; it does not report recall, latency, energy, area, capacity, dataset, precision or absolute throughput results.

**Limits on the conclusion:**

Nearest-neighbor search ranks database vectors by distance to a query and returns the closest candidates. Approximation reduces work by pruning candidates or evaluating distances incompletely, but a discarded vector can be the true neighbor. Recall must therefore be measured against an exact or declared reference at the same query and dataset.

A proximity-aware pruner uses an index or cluster relationship to remove vectors that are unlikely to be close to the query. Dual-cluster affiliations can give a vector more than one neighborhood association, reducing false exclusion when cluster boundaries are ambiguous, but they also add metadata, storage and pruning checks.

Sensitivity-ordered distance computation evaluates dimension segments in an order expected to distinguish candidates quickly. Early termination can stop a candidate when a partial distance already exceeds a valid exclusion bound or when remaining dimensions cannot change the ranking. The bound must be mathematically safe under the distance metric and precision; an empirical threshold changes recall.

A stall-free host-PIM pipeline overlaps query preparation, PIM distance work and global ranking. The stages need buffers, backpressure, completion and a consistent candidate set. If global ranking waits for data from a slow PIM partition or query preparation cannot keep up, the pipeline's peak overlap does not equal end-to-end throughput.

The source reports 2.7–19.8× throughput improvement but does not expose recall, dataset, vector dimension, metric, index construction, pruning rate, precision, capacity, energy, area, latency or host-transfer boundaries. Arithmetic reduction can alter ranking at high recall; the record establishes a reported PIM ANNS co-design and throughput claim, not a recall-preserving general speedup.

**Source and location**

Evidence tier: Primary captured official DAC description only; no full paper extraction, prism/index artifact reproduction or independent recall, dataset, precision, throughput, energy and PIM hardware validation. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH796)

DAC 2026 official description and data/review-packets/dac-2026-research796.json: ANNS memory wall; PIM bandwidth/compute tradeoff; proximity-aware vector pruning; dual-cluster affiliations; sensitivity-ordered distance segments; early termination; stall-free host-PIM pipeline; 2.7–19.8× throughput claim; omitted recall, datasets, precision, capacity, PPA and absolute throughput conditions.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** GPU/CPU ANN search

full-arithmetic PIM search

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH796

**Hardware or process assumptions:** PIM array with approximate distance computation; precision, capacity, and process assumptions are unspecified.

**Limits:** No recall, latency, energy, area, capacity, or dataset results are reported.

Arithmetic reduction can alter ranking at high recall.

Official description only; dataset and precision sweeps are required.

**Method or artifact:** Arithmetic-reduced PIM architecture for high-recall ANN search.

**Metrics:** Recall-efficiency tradeoff is claimed qualitatively

**Problem:** Approximate nearest-neighbor search is dominated by distance arithmetic and memory movement.

**Workload or benchmark:** Vector-search datasets; distance metric, PIM technology, and baselines are unspecified.

</details>

## What remains to establish

Resolve unspecified workloads, comparison methods, resource budgets, and source locations before generalizing a reported gain. Multiple papers in this selected sample permit comparison of mechanisms, but do not by themselves establish recurrence across years or a long-term trend.

[All subthemes](../expanded-taxonomy-v1.md) · [Research directions](../directions/README.md)
