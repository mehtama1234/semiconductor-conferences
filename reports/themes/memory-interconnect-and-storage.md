# Memory, interconnect, and storage

This article explains the subject and then connects it to 85 papers in the selected research sample.

A subtheme groups related technical problems. A mechanism describes the particular change proposed by a paper. The discussion below explains the subject; the linked paper records state the available evidence.

[Definitions used in the paper records](../reading-guide-v1.md)

## Capacity, bandwidth and latency are three different limits

A computation reads inputs and writes outputs. Those values take up bytes in memory or storage.

- **Capacity** is how many bytes can be held.
- **Bandwidth** is how many bytes can be moved per second.
- **Latency** is the wait between asking for a value and getting it.

Enough capacity does not guarantee a fast transfer. High bandwidth does not guarantee a short wait for one request.

## Moving data sets a floor on how long a job takes

> **The rule.** A job must move **B** bytes. Its connection sustains **W** bytes per second. The transfers alone take at least **B ÷ W** seconds, however fast the arithmetic is.

This simple bound assumes the job gets the stated bandwidth. Shared requests, protocol work and dependencies can make it slower.

Keeping a value near its next user can cut transfers. But nearby memory is small, so keeping one value there may push out another useful one.

## The subthemes move data, move work, or change the path

- **Memory hierarchy** work decides which values sit in faster or slower memory.
- **Near-memory or processing-in-memory** work moves some computation toward the stored data.
- **Interconnect** work changes the paths between components.
- **Storage** work must also ask whether a value survives power loss and whether updates stay consistent.

Each can cut one transfer while adding scheduling, copying or coordination work somewhere else.

## A fair test measures the whole job, including moving the data

1. Measure the whole job, including placing and migrating data.
2. Vary whether the input fits in each memory, and how many other jobs share the connection.
3. For approximate search, hold answer quality fixed. For a service, measure slow requests as well as the average.

Fewer remote bytes is useful evidence about one cost. The final claim needs completion time or energy under the full conditions.

## Follow a read before comparing memory systems

A single read passes through several steps, and each one can cost time.

A program asks for a value by its **address**, the number that names a storage location. Then:

1. The system checks the access is allowed, and finds where the current value lives.
2. A nearby cached copy may answer the request. Otherwise the request travels to another memory or storage device.
3. The returned bytes must reach the right consumer.
4. A dependent operation cannot use them before they arrive.

Address translation, queueing, routing, fetching, checking and signalling completion can each take time. Steps for independent requests can overlap. Steps for one dependent request cannot be overlapped at will. Moving the bytes elsewhere changes both the physical route and the work done along it.

**Be careful:** the examples below are teaching calculations, not measurements of the linked papers. The paper links lead to individual explanations with source locations and evidence limits. This synthesis connects mechanisms; it does not certify a combined implementation.

## Capacity, latency, and bandwidth change different decisions

Each of the three limits answers a different question.

| Limit | The question it answers |
| --- | --- |
| Capacity | Can the needed data stay resident? |
| Latency | How long does one request wait? |
| Bandwidth | How much data can cross an interface per second? |

A system can have room to spare and fast links, yet still be slow. A chain of small reads, each waiting for the one before, is enough to do it.

> **Worked example.** One request fetches 64 bytes and takes 100 nanoseconds.
>
> - If each request must wait for the previous value, at most ten million requests finish per second.
> - That is 10 million × 64 = **640 million useful bytes per second**.
> - A nominal 20-billion-byte-per-second connection does not change this limit.
> - Independent requests can overlap. To sustain 20 billion bytes per second with these sizes and this latency, an idealized model needs at least **32 requests in flight**.

Protocol traffic, queueing and implementation limits can raise that number, or stop the rate being reached.

So one sequential pointer walk cannot show the bandwidth a parallel matrix workload gets. And a large-transfer benchmark cannot show small-read response time. The experiment must match both the access size and how independent the requests are.

### More capacity can help even when each new access is slower

Adding slower memory can beat the real alternatives, but cannot beat the arithmetic of capacity.

A service must keep 300 GB of data, but local memory holds 240 GB. Its options pay different costs:

- add slower memory;
- fetch missing data from storage;
- compress data;
- recompute some values;
- use more machines.

The fair comparison is against the real alternative, not an imaginary system with unlimited fast memory.

> **Worked example.** Local memory holds 240 GB.
>
> - If 180 GB is actively used, ideal placement keeps it all local.
> - If 280 GB becomes active, at least 280 − 240 = **40 GB** cannot be local at once.

No better predictor removes that gap. It can only choose which accesses pay the extra cost, and when data moves.

[Vistara's manuscript-backed explanation](../observed-subthemes/memory-hierarchy-and-persistence.md#explanation-isca-2026-program-045) separates two experiments:

- adding capacity;
- replacing local memory, at fixed total capacity.

The second exposes access-cost regressions that the first can hide. Its discussion also keeps a reported throughput regression and unresolved table inconsistencies.

**Be careful:** this is stronger evidence than a claim that all addressable memory acts like local memory. It is not a universal service result.

## Placement is a decision with an upfront cost

Moving data pays off only if enough later accesses benefit from the move.

A **placement policy** chooses where data should live. **Migration** is the work of moving it while keeping its contents and accesses correct. Copying bytes is only part of that. Readers and writers must never see a half-moved page, or update a copy about to be thrown away.

> **Worked example (illustrative).** Moving a page costs 10 microseconds. Each later access saves 100 nanoseconds.
>
> - Break-even: 10,000 nanoseconds ÷ 100 = **100 qualifying accesses**.
> - Fewer accesses lose time, under this simple accounting.

Contention, tracking, pushing out useful data, or a later move back can make it worse. Count only accesses that would really have reached the slower tier, not ones a processor cache already serves.

A policy based on past accesses predicts future benefit; it does not know it. A sudden change in active data can cause repeated moves. So measure:

- correct and incorrect placement decisions;
- migration traffic;
- how long the policy takes to adapt.

[Ctxmem](../observed-subthemes/memory-hierarchy-and-persistence.md#explanation-dac-2026-research1028) works on a related boundary: software handling versus device-side movement. Its description does not establish the full implementation. Handling work asynchronously can free the processor for other tasks, while the original consumer still waits.

**Be careful:** asynchronous handling is not permission to read data that is not there yet, or to skip access checks.

## Compression changes capacity and the path to a usable value

Compression frees space, but decoding joins the path to every value.

Compressed storage can shrink a value, but the next computation may need it decoded. So the decoder becomes part of the dependency path. Random access may need metadata marking where valid decoding can start. Storing blocks that decode independently shortens that path, at some cost in compression.

> **Worked example.** An 80-GB device holds 30 GB of weights and 10 GB of fixed workspace. Each admitted request needs 1 GB of state.
>
> - Room for requests: 80 − 30 − 10 = **40 requests**.
> - Shrink the weights to 20 GB: 80 − 20 − 10 = **50 requests**.
> - That is 25% more requests, not the one-third cut in weight bytes.

Longer requests, extra workspace or allocator overhead change this bound.

More capacity does not decide response time. More requests at once can raise total work per second while making each request wait longer. [The lossless-weight-compression explanation](../observed-subthemes/memory-hierarchy-and-persistence.md#explanation-isca-2026-program-008) keeps exactly this distinction in its recovered serving results. It also notes a conflicting batch count in the manuscript, and separates whole-model serving from a single-projection comparison.

This links memory design to [architecture and accelerators](architecture-and-accelerators.md). A smaller format helps only if the machine can deliver usable operands fast enough, with the required numerical behavior.

**Be careful:** exact decoding proves the encoded values are recovered. It does not prove an earlier quantization step was correct, or that every application metric improves.

## An interconnect must make progress, not just move bits quickly

Faster links cannot fix a design where requests block each other forever.

An **interconnect** carries requests and responses between components. Finite buffers hold work waiting for its next step. If requests fill every buffer, responses cannot get space. Then generating requests faster makes things worse.

> **Example of a dependency cycle (abstract).**
>
> - Operation A holds resource X and waits for Y.
> - Operation B holds Y and waits for X.
> - Neither can finish or release its resource. More link bandwidth does not help.

A design needs rules that prevent the cycle or guarantee a way out. The rules must cover every supported mix of traffic, not just one isolated one-way transfer.

[OpenSUN's explanation](../observed-subthemes/memory-hierarchy-and-persistence.md#explanation-dac-2026-research1061) records a specific warning from its artifact documentation, about high-throughput mutual host-memory access. That warning is not a locally reproduced failure, and the abstract cycle above is not its reconstructed internal cause. It is still a reason to keep the supported traffic boundary in mind when reading about the platform.

Being able to address memory does not settle two further questions:

- **Coherence:** are cached copies of one location handled consistently?
- **Ordering:** which orders of observations across operations are allowed?

A writer that stores data, then sets a ready flag, needs the right synchronization contract. Only then can a reader trust the flag as proof the data is complete. Physical connectivity alone does not give that proof.

## Recovery changes what completion means

A durable update promises more than a successful read: after a failure, recovery must give an allowed state.

A successful read means the consumer got the required value under the access rules. A durable update must also survive a specified failure. Data sitting in a volatile cache may be visible now, and gone after power loss.

> **Example (conceptual, not taken from a paper in this sample).** An update changes a stored record and an index pointing to it.
>
> - If the index survives a crash but the record does not, recovery finds a pointer to incomplete data.
> - If the record survives but the index does not, recovery needs a defined way to handle the unreferenced record.

So the system must specify ordering, all-or-nothing (atomic) updates, and recovery rules. Faster writes alone cannot provide them.

**Error correction** answers another question: can damaged encoded data be detected or rebuilt, within a stated fault model? [Cerberus](../observed-subthemes/memory-hierarchy-and-persistence.md#explanation-isca-2026-program-004) and [CLUE-ECC](../observed-subthemes/memory-hierarchy-and-persistence.md#explanation-dac-2026-research676) explain why code boundaries and fault location matter.

**Be careful:** correcting some bit errors does not make a multi-write transaction atomic or durable. And a recoverable update protocol does not prove protection against every physical fault.

The chapter historically named "memory hierarchy and persistence" includes several mechanisms outside crash durability. Its title is a navigation label, not evidence that every paper in it addresses persistence. Classification reconciliation remains open.

## Connect the mechanisms through explicit tradeoffs

Every memory fix has a benefit and a cost that must stay visible.

| Proposed change | Possible benefit | Cost or obligation that must remain visible |
| --- | --- | --- |
| Add a slower memory tier | Keep more data resident and avoid storage accesses or additional machines | Active-set capacity, placement mistakes, migration, response-time limits |
| Compress stored values | Free capacity and reduce selected transfers | Decoding, metadata, access granularity, quality boundary |
| Move computation or fault handling toward data | Reduce host work or traffic over one interface | Remaining consumer wait, permissions, completion visibility, new device bottlenecks |
| Increase concurrent communication | Overlap independent waits | Buffer capacity, congestion, fairness, and guaranteed progress |
| Add recovery or correction mechanisms | Survive specified failures | Protected boundary, redundancy, update ordering, unsupported faults |

These are not independent fixes whose reported ratios can be multiplied:

- Compression can change which pages are hot, and what migration costs.
- Migration uses the same links as application requests.
- More requests at once can hide latency, until queues clog.
- Recovery metadata can add writes and ordering rules that a bandwidth benchmark leaves out.

## Long-term hypotheses and how to challenge them

Three readings are worth testing; each names what would weaken it.

| Hypothesis | Test | What would weaken it |
| --- | --- | --- |
| Usable capacity becomes a joint property of devices and system software, as memory locations diversify | Do matched systems keep needing placement, migration and admission changes to use device capacity? | Simple static placement does as well, without real restrictions |
| Representation and placement should be judged together for capacity-limited services | Compare compression alone, placement alone, and both, counting decoding and movement | One fix already removes the limit, or coordination costs erase the combined gain |
| Average transfer efficiency is not enough when systems share memory | Measure each application's completed work and slow-request latency under competing traffic | Realistic sharing causes no material interference, or existing isolation meets every service requirement |

A device can expose bytes that an application cannot use safely or efficiently under its allocation and service rules. That is the reason behind the first row.

These are interpretations to test, not demonstrated ISCA–DAC–ICCAD trends. A cross-conference account must match workloads, source depth, comparison conditions and edition coverage before inferring change over time.

**Be careful:** the current selected sample and missing sources do not support a conference ranking or a claim of historical growth.

The expanded [memory hierarchy chapter](../observed-subthemes/memory-hierarchy-and-persistence.md) gives a deeper reading path for fourteen records. Other memory, storage and interconnect branches below still need fuller explanations and source recovery. This parent discussion does not replace that work, or independent scientific and comprehension review.

## Subthemes and how to study them

Each link opens the subtheme discussion and its captured paper records. Explanatory depth varies: some papers have expanded individual explanations; others still have only brief discussion or evidence cards. Source locations and unresolved conditions remain visible.

### [Data movement and locality](../observed-subthemes/data-movement-and-locality.md)

34 selected records in this theme. Start with [Marlin: I/O-Efficient Prefix KV Cache Retrieval for Long-Prefix LLM Serving](../observed-subthemes/data-movement-and-locality.md).

### [Memory hierarchy and persistence](../observed-subthemes/memory-hierarchy-and-persistence.md)

14 selected records in this theme. Start with [HybriMoE: Hybrid CPU-GPU Scheduling and Cache Management for Efficient MoE Inference](../observed-subthemes/memory-hierarchy-and-persistence.md).

### [Storage and data movement](../observed-subthemes/storage-and-data-movement.md)

14 selected records in this theme. Start with [HDDB: Efficient In-Storage SQL Database Search Using Hyperdimensional Computing on Ferroelectric NAND Flash](../observed-subthemes/storage-and-data-movement.md).

### [Memory compute and reliability](../observed-subthemes/memory-compute-and-reliability.md)

10 selected records in this theme. Start with [DRCA: Reliable Bitwise Logic in DRAM via Dual-Rail Compute and Access](../observed-subthemes/memory-compute-and-reliability.md).

### [Processing in memory and memory centric compute](../observed-subthemes/processing-in-memory-and-memory-centric-compute.md)

4 selected records in this theme. Start with [Freebit: Unleashing the Performance Potential of Low-Bit LLMs Through PIM](../observed-subthemes/processing-in-memory-and-memory-centric-compute.md).

### [Memory and data movement](../observed-subthemes/memory-and-data-movement.md)

3 selected records in this theme. Start with [Toki: Profiling HBM Performance on FPGA Systems with RISC-V Soft Cores and PCIe Host DMA Traffic](../observed-subthemes/memory-and-data-movement.md).

### [Storage and memory systems](../observed-subthemes/storage-and-memory-systems.md)

3 selected records in this theme. Start with [From Block to Range: Rethinking the Fundamental Unit of Log-Structured File Systems for ZNS SSDs](../observed-subthemes/storage-and-memory-systems.md).

### [Chiplet and on chip interconnect](../observed-subthemes/chiplet-and-on-chip-interconnect.md)

2 selected records in this theme. Start with [C2C-Explorer: An Exploration Framework for Chip-to-Chip Interconnect Architectures in LLM Cloud Computing Systems](../observed-subthemes/chiplet-and-on-chip-interconnect.md).

### [Interconnect and networking](../observed-subthemes/interconnect-and-networking.md)

1 selected records in this theme. Start with [Credix: A Credit-Driven Distributed Buffer Management for Large-Scale Switching Chips](../observed-subthemes/interconnect-and-networking.md).

## Representative source-backed records

The following reading set spans the available conferences and uses dated corrections where registered. These corrections improve the current reading view but do not change historical adjudication or establish independent acceptance. Each paper link opens its exact evidence card.

## Paper cards: what changes and where it stops

- [DisDP: Disaggregating Compute, Network, and Storage for Model-Sharded Data-Parallel Training](../observed-subthemes/data-movement-and-locality.md#paper-isca-2026-program-155) — ISCA 2026.
- [Vistara: Making CXL Real—Full Path from ASIC Design and OS Support to Hyperscale Deployment](../observed-subthemes/memory-hierarchy-and-persistence.md#paper-isca-2026-program-045) — ISCA 2026.
- [A Silicon-Proven Unified Low-Latency CXL Controller and Port-Based Routing Switch for Memory-Centric Fabrics](../observed-subthemes/chiplet-and-on-chip-interconnect.md#paper-isca-2026-program-044) — ISCA 2026.
- [Approaching Shannon Bound with Lossless LLM Weight Compression](../observed-subthemes/memory-hierarchy-and-persistence.md#paper-isca-2026-program-008) — ISCA 2026.
- [WILL: Write Invalidation Skipping for QLC NAND by Leveraging Data Lifespan and Latency Awareness](../observed-subthemes/storage-and-memory-systems.md#paper-dac-2026-research931) — DAC 2026.
- [Credix: A Credit-Driven Distributed Buffer Management for Large-Scale Switching Chips](../observed-subthemes/interconnect-and-networking.md#paper-dac-2026-research837) — DAC 2026.
- [Prism: Reducing Arithmetic for High-Recall Approximate Nearest Neighbor Search on Processing-in-Memory](../observed-subthemes/memory-compute-and-reliability.md#paper-dac-2026-research796) — DAC 2026.
- [CQ-CiM: Hardware-Aware Embedding Shaping for Robust CiM-Based Retrieval](../observed-subthemes/processing-in-memory-and-memory-centric-compute.md#paper-dac-2026-research752) — DAC 2026.
- [GAIA: Glass-Aware I/O Middleware](../observed-subthemes/storage-and-data-movement.md#paper-iccad-2025-1144) — ICCAD 2025.
- [Cerberus: Cross-Layer ECC Co-Design for Robust and Efficient Memory Protection](../observed-subthemes/memory-hierarchy-and-persistence.md#paper-isca-2026-program-004) — ISCA 2026.
- [COSM: A Cooperative Scheduling Framework for Concurrent PIM and CPU Execution on Mobile Devices](../observed-subthemes/data-movement-and-locality.md#paper-isca-2026-program-003) — ISCA 2026.
- [RAGNMP: Leveraging Elimination Tree to Accelerate RAG with Near-Memory Processing](../observed-subthemes/data-movement-and-locality.md#paper-dac-2026-research701) — DAC 2026.

## What the evidence supports

These records identify proposed methods and the conditions recorded for them. A reported improvement should be interpreted with its comparison method, input size, hardware, and result-quality requirement. Missing fields are evidence gaps; a populated field can also state that a detail is unspecified.

## Limits and next evidence

The selected sample is uneven across conferences and source types. It cannot establish how fast a subject is growing. Repeated observations across comparable years, with the same inclusion rules and source depth, are needed for a time trend.

Every linked evidence article preserves the Problem: and Mechanism / artifact: fields, baseline, unshortened limitations, source URL, and recorded location. Primary text and independent review remain necessary where the record says those checks are open.

[Research directions](../directions/README.md) · [All observed subthemes](../expanded-taxonomy-v1.md)
