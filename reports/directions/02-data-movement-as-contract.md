# Designing computation around the cost of moving data

Status: a research hypothesis supported by selected cases. A measured increase across comparable years has not been established.

## The problem: a job can spend most of its time waiting for data

Every operation needs its inputs where the hardware can reach them. If they are elsewhere, they must move.

Moving them uses bandwidth, takes time and costs energy. So a job can spend most of its time waiting for values, even when its arithmetic is simple.

## The change: choose the algorithm, the data placement and the schedule together

- Keep intermediate values near the operations that use them next, to cut repeated transfers.
- Move a computation near the stored data, to cut the bytes sent over a connection.
- Recompute a cheap value, sometimes, instead of storing and fetching it.

Each change brings new costs, such as local traffic and extra computation. Count them.

## Memory, architecture and scheduling overlap, so fixing one can shift the delay

- A **memory** method decides where values can live.
- An **architecture** decides where operations can run.
- A **scheduler** decides when workers compete for data.

A method that changes only one layer may just move the delay elsewhere. A full comparison includes the first loading of data and any later migration.

## The test: fixed output quality, varied data sizes, every transfer counted

1. Measure completion time and energy at fixed output quality.
2. Vary input size, memory capacity and competing requests. Include data that fits, and data that does not fit, in fast memory.
3. For approximate search, compare at the same rate of correct answers. For services, include slow requests and data migration.

The hypothesis weakens if the advantage disappears once capacity is matched or all transfer costs are counted. Seeing it recur in today's cases cannot show growth over time.

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

A trend needs the same rules applied to comparable years:

1. Select comparable editions.
2. Apply the same inclusion and coding rules.
3. Measure source coverage in each edition.
4. Tell apart how many papers discuss a method from evidence that the method improves results.

The current sample combines DAC and ISCA 2026 with ICCAD 2025 fallback material, and coverage is uneven. That supports comparing cases with stated limits.

[Read the longitudinal protocol](../longitudinal-protocol-v1.md) · [Return to research directions](README.md)
