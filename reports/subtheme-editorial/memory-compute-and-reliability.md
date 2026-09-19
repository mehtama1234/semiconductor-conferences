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
