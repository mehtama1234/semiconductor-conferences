## Follow a read before comparing memory systems

A program requests a value using an address. The system determines whether the access is permitted and where the current value resides. A nearby cached copy may satisfy the request; otherwise the request travels to another memory or storage device. The returned bytes must reach the right consumer, and a dependent operation cannot use them before they are available.

That sequence contains more than a transfer. Address translation, queueing, routing, fetching, checking, and publishing completion can each consume time. Some stages overlap across independent requests; stages belonging to one dependent request cannot be overlapped arbitrarily. Changing the location of the bytes changes both the physical route and the responsibilities along it.

The following examples are teaching calculations, not measurements of the linked papers. The paper links lead to individual explanations with source locations and evidence limits. This synthesis connects mechanisms; it does not certify a combined implementation.

## Capacity, latency, and bandwidth change different decisions

Capacity answers whether the required data can remain resident. Latency answers how long a particular request waits. Bandwidth answers how much data can cross an interface over time. A system can have sufficient capacity and high sustained bandwidth yet still be slow for a chain of dependent small reads.

Suppose one request retrieves 64 bytes and takes 100 nanoseconds. If the next request cannot begin until that value arrives, at most ten million requests complete per second, or 640 million useful bytes per second. A nominal 20-billion-byte-per-second connection does not change this dependency limit. Independent requests can overlap: sustaining that nominal byte rate with these request sizes and latency would require at least 32 requests in flight under an idealized model. Protocol traffic, queueing, and implementation limits can raise the requirement or prevent reaching the rate.

This calculation explains why one sequential pointer traversal cannot establish the bandwidth available to a parallel matrix workload, and why a large transfer benchmark cannot establish small-read response time. The experiment must match both the access size and the independence of requests.

### More capacity can help even when each new access is slower

Suppose a service must retain 300 GB of data, but local memory holds 240 GB. It can add slower memory, fetch absent data from storage, compress data, recompute some values, or use more machines. These choices pay different costs. The correct comparison includes the actual alternative, not an imaginary system with unlimited fast memory.

If 180 GB is actively accessed, ideal placement could keep that active set within the 240-GB local tier. If 280 GB becomes active, at least 40 GB cannot remain local at once. No better predictor can remove this capacity inequality. The predictor can only choose which accesses pay the additional cost and when migrations occur.

[Vistara's manuscript-backed explanation](../observed-subthemes/memory-hierarchy-and-persistence.md#explanation-isca-2026-program-045) separates adding capacity from replacing local memory at fixed total capacity. The latter exposes access-cost regressions that a capacity-relief experiment can hide. Its linked discussion also retains a reported throughput regression and unresolved table inconsistencies. This is stronger evidence than a claim that all addressable memory behaves like local memory, but it is not a universal service result.

## Placement is a decision with an upfront cost

A placement policy chooses where data should reside. Migration is the work of changing that location while preserving the intended contents and accesses. Copying bytes is only part of it: readers and writers must not observe a partially moved page or update a copy that will be discarded.

For an illustrative decision, moving a page costs ten microseconds and saves 100 nanoseconds on each subsequent access. One hundred qualifying accesses recover the movement cost. Fewer accesses lose time under this simple accounting. Additional contention, tracking, displaced useful data, or a later move back can make the result worse. The saving must count accesses that would really have reached the slower tier, not accesses already satisfied by a processor cache.

A policy based on past accesses predicts future benefit; it does not know it. An abrupt change in active data can produce repeated moves. Measure both correct and incorrect placement decisions, migration traffic, and the time until the policy adapts.

[Ctxmem](../observed-subthemes/memory-hierarchy-and-persistence.md#explanation-dac-2026-research1028) addresses a related boundary between software handling and device-side movement. Its description does not establish the full implementation. Asynchronous handling can free the processor for other tasks while the original consumer still waits. It must not be interpreted as permission to read unavailable data or bypass access checks.

## Compression changes capacity and the path to a usable value

Compressed storage can reduce the bytes needed for a value, but the next computation may need a decoded representation. A decoder therefore becomes part of the dependency path. Random access may require metadata identifying a valid decoding start; storing independently decodable blocks can sacrifice some compression to shorten that path.

Consider an 80-GB device with 30 GB of weights, 10 GB of fixed workspace, and one GB of state per admitted request. A simplified capacity bound permits 40 requests. Reducing weights to 20 GB permits 50, a 25% increase in admitted requests rather than the one-third reduction in weight bytes. Longer requests, additional workspace, or allocator overhead alter the bound.

That capacity gain does not determine response time. More simultaneous requests can improve aggregate work per second while increasing each request's wait. [The lossless-weight-compression explanation](../observed-subthemes/memory-hierarchy-and-persistence.md#explanation-isca-2026-program-008) retains precisely this distinction in its recovered serving results, along with a conflicting batch count in the manuscript. It also separates whole-model serving from a single-projection comparison.

This connects memory design to [architecture and accelerators](architecture-and-accelerators.md): a smaller representation is useful only if the machine can deliver usable operands fast enough, within the required numerical behavior. Exact decoding proves recovery of the encoded values, not correctness of an earlier quantization step or improvement in every application metric.

## An interconnect must make progress, not just move bits quickly

An interconnect carries requests and responses among components. Finite buffers hold work awaiting its next stage. If responses cannot obtain space because requests occupy all available resources, simply generating requests faster can make the problem worse.

An abstract dependency cycle illustrates the obligation: operation A holds resource X while waiting for Y, and operation B holds Y while waiting for X. Neither can finish and release its resource. Increasing link bandwidth does not remove this cycle. A design needs rules that prevent the cycle or guarantee an escape; the rule must cover supported combinations of traffic, not just an isolated one-way transfer.

[OpenSUN's explanation](../observed-subthemes/memory-hierarchy-and-persistence.md#explanation-dac-2026-research1061) records a specific artifact-documentation warning about high-throughput mutual host-memory access. That warning is not a locally reproduced failure, and the abstract cycle above is not its reconstructed internal cause. It is nevertheless a reason to retain the supported traffic boundary when interpreting the platform.

Addressability also does not establish coherence or ordering. Coherence concerns consistent handling of cached copies of a location. Ordering concerns which observations across operations are allowed. A writer storing data and then setting a ready flag needs the appropriate synchronization contract before a reader can safely use that flag as proof of completed data. Physical connectivity alone does not provide that proof.

## Recovery changes what completion means

A successful read means that the consumer received the required value under the access contract. A successful durable update has a stronger obligation: after a specified failure, recovery must produce an allowed state. Data residing in a volatile cache may be visible now and disappear after power loss.

Imagine updating a stored record and an index pointing to it. If the index becomes durable first but the record does not, recovery may find a pointer to incomplete data. If the record survives but the index does not, recovery needs a defined way to handle the unreferenced record. The system must specify ordering, atomicity, and recovery rules; faster writes alone cannot establish them. This is a conceptual failure example, not an extracted algorithm from a paper in this sample.

Error correction answers another question: can damaged encoded data be detected or reconstructed within a stated fault model? [Cerberus](../observed-subthemes/memory-hierarchy-and-persistence.md#explanation-isca-2026-program-004) and [CLUE-ECC](../observed-subthemes/memory-hierarchy-and-persistence.md#explanation-dac-2026-research676) explain why code boundaries and fault location matter. Correcting some bit errors does not by itself make a multi-write transaction atomic or durable. Conversely, a recoverable update protocol does not prove protection against every physical fault.

The chapter historically named memory hierarchy and persistence includes several mechanisms outside crash durability. Its current title is a navigation label, not evidence that every included paper addresses persistence. Classification reconciliation remains open.

## Connect the mechanisms through explicit tradeoffs

| Proposed change | Possible benefit | Cost or obligation that must remain visible |
| --- | --- | --- |
| Add a slower memory tier | Keep more data resident and avoid storage accesses or additional machines | Active-set capacity, placement mistakes, migration, response-time limits |
| Compress stored values | Free capacity and reduce selected transfers | Decoding, metadata, access granularity, quality boundary |
| Move computation or fault handling toward data | Reduce host work or traffic over one interface | Remaining consumer wait, permissions, completion visibility, new device bottlenecks |
| Increase concurrent communication | Overlap independent waits | Buffer capacity, congestion, fairness, and guaranteed progress |
| Add recovery or correction mechanisms | Survive specified failures | Protected boundary, redundancy, update ordering, unsupported faults |

These are not independent optimizations whose reported ratios can be multiplied. Compression can alter page hotness and migration cost. Migration consumes the same links used by application requests. Additional concurrent requests can hide latency until queues become congested. Recovery metadata can add writes and ordering constraints that an isolated bandwidth benchmark excludes.

## Long-term hypotheses and how to challenge them

One bounded hypothesis is that usable capacity becomes a joint property of devices and system software as memory locations diversify. A device can expose bytes that an application cannot use safely or efficiently under its allocation and service constraints. Evidence would strengthen this hypothesis if matched systems repeatedly require placement, migration, and admission changes to realize device capacity. It would weaken where simple static placement achieves comparable results without meaningful restrictions.

A second hypothesis is that representation and placement should be evaluated together for capacity-constrained services. The test must compare compression alone, placement alone, and their combination, including decoding and movement. It would weaken if one intervention already removes the relevant limit or their coordination costs erase the combined benefit.

A third hypothesis is that average transfer efficiency becomes insufficient when systems share memory resources. Measure per-application completed work and slow-request latency under competing traffic, not only aggregate bandwidth. It would weaken as a distinguishing design concern where realistic sharing produces no material interference or where existing isolation already satisfies every service requirement.

These are interpretations to test, not demonstrated ISCA–DAC–ICCAD trends. A cross-conference account must match workloads, source depth, comparison conditions, and edition coverage before inferring change over time. The current selected sample and missing sources do not support a conference ranking or a claim of historical growth.

The expanded [memory hierarchy chapter](../observed-subthemes/memory-hierarchy-and-persistence.md) provides a deeper reading path for fourteen records. Other memory, storage, and interconnect branches below still need fuller individual explanations and source recovery. This parent discussion does not replace that work or independent scientific and comprehension review.
