# Designing computation around the cost of moving data

Status: a research hypothesis supported by selected cases. A measured increase across comparable years has not been established.

## The basic technical problem

Every operation needs inputs in a place the executing hardware can access. If those inputs are elsewhere, they must move. The transfer uses bandwidth, takes time, and consumes energy. A job can therefore spend most of its time waiting for values even when its arithmetic is simple.

## What would change in the design process

The proposed direction is to choose the algorithm, placement of data, and execution schedule together. Keeping intermediate values near later operations can reduce repeated transfers. Moving a computation near stored data can reduce the bytes sent over a connection. Recomputing a cheap value can sometimes avoid storing and retrieving it. Each change needs an account of its new costs, including local traffic and extra computation.

## Why the details matter

These choices explain why memory systems, accelerator designs, and distributed applications overlap. A memory method determines where values can reside; an architecture determines where operations can run; a scheduler determines when workers compete for data. A method that changes only one layer may shift the delay elsewhere. A full comparison must include the initial loading of data and any later migration.

## What would support or weaken the claim

Measure completion time and energy at fixed output quality while varying input size, memory capacity, and competing requests. Include cases where data fits and does not fit in fast memory. For approximate search, compare at the same rate of correct answers. For services, include slow requests and data migration. The hypothesis weakens if an advantage disappears after matching capacity or including all transfer costs. Recurrence across the current cases alone cannot establish growth over time.

## Counterpressure and falsification boundary

Challenge paper: `dac-2026-research2268` (alternative_mechanism; source tier `official_description`). [Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH2268&sess=sess169).

Memory-centric progress can come from host-side layout and access scheduling, not necessarily compute offload. The title/body system-name discrepancy remains unresolved.

**What would weaken the direction:** The direction is weakened if a matched-recall comparison shows that host-side placement and scheduling provide the same end-to-end result after including CXL traffic, speculation, capacity and host overhead, without a distinct near-memory benefit.

**Next evidence:** Resolve TierANNS/COGA identity and compare recall, working-set capacity, speculation traffic and host overhead against near-memory alternatives.

## Paper evidence and open conditions

[Read the paper evidence dossier](evidence/02-data-movement-as-contract-evidence.md). It connects this discussion to the recorded sources and unresolved conditions.

[Read the cross-conference comparison](../comparisons/data-movement-as-contract.md). Different conferences can examine different parts of the problem; their reported numbers are not automatically comparable.

[Check the condition register](../direction-condition-register-v1.md) for unresolved experimental details and [the review gate](../direction-review-gate-v1.md) for the current review status.

## Establishing a long-term trend

To test change over time, select comparable editions, apply the same inclusion and coding rules, and measure source coverage in each edition. Distinguish the number of papers discussing a method from evidence that the method improves results. The current sample combines DAC and ISCA 2026 with ICCAD 2025 fallback material, and coverage is uneven. That supports comparison of cases with stated limits.

[Read the longitudinal protocol](../longitudinal-protocol-v1.md) · [Return to research directions](README.md)
