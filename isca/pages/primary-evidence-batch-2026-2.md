# ISCA 2026 primary evidence batch 2

This page adds two exact-title ISCA 2026 records supported by author preprints.
The preprints provide substantive problem, mechanism, and headline-metric
evidence, but the project has not independently reproduced the experiments or
treated these two papers as a representative sample of the program.

## COSM: concurrent PIM and CPU scheduling

COSM treats processing-in-memory as a coordination problem rather than an
isolated accelerator. Its target setting is a mobile device where CPU and PIM
share memory banks and buses. Bank conflicts and bus congestion can otherwise
erase the benefit of moving computation near data.

The proposed control interface is designed to generate PIM commands with low
interference. An idleness-aware scheduler inserts PIM commands into idle windows
in the CPU access sequence, allowing PIM execution to overlap with data transfer.
The author preprint reports up to 2.8x PIM throughput and less than 2.0% CPU
performance loss across concurrent LLM, mobile-application, and compute-kernel
workloads. [Primary preprint](https://arxiv.org/abs/2606.30553)

The important subskill is cooperative scheduling under shared-memory contention:
the scheduler must understand when memory is idle, which banks are exposed to
conflict, and how much PIM work can be admitted without violating CPU service.
This is more specific than “PIM acceleration.” The evidence does not yet support
claims about energy, general mobile SoCs, or superiority over every PIM scheduler;
those require full-paper tables and platform details.

## Cerberus: cross-layer memory protection

Cerberus addresses the interaction among on-die ECC, link ECC, and system ECC in
dense, high-speed DRAM. When each layer evolves independently, redundancy can be
duplicated and recovery actions can interfere. Cerberus uses an Encode-Once,
Decode-Many organization so controller-generated protection can be reused for
link-level write detection/retry, device repair on reads, and system-level
end-to-end recovery.

The preprint further describes complementary parity/syndrome structures, decoder
ordering, and a correction budget intended to limit miscorrection amplification.
Its evaluation emphasizes clustered and peripheral faults in an HBM-oriented
setting and reports improved resilience with reduced redundant overhead. [Primary
preprint](https://arxiv.org/abs/2605.02220)

The specific subskill is cross-layer fault-recovery coordination: protection
codes, decoder sequencing, and correction budgets are designed as one memory-stack
mechanism rather than three independent safeguards. Quantitative overheads,
fault probabilities, decoder latency, and the exact HBM assumptions remain
unverified until the full paper is extracted.

## What this batch changes in the direction map

Together these records sharpen the memory direction into two distinct mechanisms:

1. Runtime scheduling coordinates CPU and PIM access to shared memory.
2. Reliability coding coordinates ECC layers across the memory stack.

Both are cross-layer designs, but they should not be collapsed into one trend:
COSM optimizes interference and utilization during execution, while Cerberus
optimizes recovery correctness and redundancy under faults. They are evidence for
the kinds of detailed capabilities appearing in the selected ISCA sample, not a
claim about ISCA-wide prevalence or product adoption.
