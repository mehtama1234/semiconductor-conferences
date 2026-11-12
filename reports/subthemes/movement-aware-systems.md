# Movement-aware systems

This article groups several related subjects to explain a shared design question.

## The problem

Moving data takes time, capacity, bandwidth, and energy. When many workers use the same path, contention can dominate the work itself.

## What changes in the design

The papers change data placement, reuse, routing, storage, or scheduling so that movement is planned with computation.

## How to establish an improvement

The useful test reports traffic, data size, topology, contention, capacity, and end-to-end time or energy against a stated baseline.

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

## The individual subjects

The grouping contains 63 selected records. Read its individual subjects below; their boundaries can overlap.

- [Data movement and locality](../observed-subthemes/data-movement-and-locality.md)
- [Memory hierarchy and persistence](../observed-subthemes/memory-hierarchy-and-persistence.md)
- [Chiplet and on chip interconnect](../observed-subthemes/chiplet-and-on-chip-interconnect.md)
- [Architecture software co design](../observed-subthemes/architecture-software-co-design.md)

## Technical cards

Evidence tier and exact source locations are provided in each linked article. The article preserves full recorded text, including limits and baselines.

- [DisDP: Disaggregating Compute, Network, and Storage for Model-Sharded Data-Parallel Training](../observed-subthemes/data-movement-and-locality.md#paper-isca-2026-program-155)
- [MTIA 300: Meta’s First Training Chip Featuring Built-in NICs and Collective Offloading Engines](../observed-subthemes/architecture-software-co-design.md#paper-isca-2026-program-069)
- [Accelerating MoE with Dynamic In-Switch Computing on Multi-GPUs](../observed-subthemes/architecture-software-co-design.md#paper-isca-2026-program-058)
- [Vistara: Making CXL Real—Full Path from ASIC Design and OS Support to Hyperscale Deployment](../observed-subthemes/memory-hierarchy-and-persistence.md#paper-isca-2026-program-045)
- [RAGNMP: Leveraging Elimination Tree to Accelerate RAG with Near-Memory Processing](../observed-subthemes/data-movement-and-locality.md#paper-dac-2026-research701)
- [CLUE-ECC: Low-Cost LPDDR6 Reliability Enhancement by Integrating System ECC with On-Die ECC](../observed-subthemes/memory-hierarchy-and-persistence.md#paper-dac-2026-research676)
- [SAEM: Stage-Aware Expert Management for Memory-Efficient MoE Inference in Chain-of-Thought Reasoning](../observed-subthemes/memory-hierarchy-and-persistence.md#paper-dac-2026-research675)
- [UniNL: Unifying Fragmented Non-Linear Operators for Efficient Edge LLM Inference](../observed-subthemes/architecture-software-co-design.md#paper-dac-2026-research617)
- [Squat: Quant Small Language Models on the Edge](../observed-subthemes/architecture-software-co-design.md#paper-iccad-2025-105)
- [A Silicon-Proven Unified Low-Latency CXL Controller and Port-Based Routing Switch for Memory-Centric Fabrics](../observed-subthemes/chiplet-and-on-chip-interconnect.md#paper-isca-2026-program-044)

## Limits and next evidence

This is a cross-cutting grouping within the selected sample. Its count measures the records included by the grouping rule. Comparing methods requires the same workload, answer quality, hardware limits, and total evaluation budget. Open the individual records before treating a shared subject as a common result.

[Research directions](../directions/README.md) · [Complete subtheme index](../expanded-taxonomy-v1.md)
