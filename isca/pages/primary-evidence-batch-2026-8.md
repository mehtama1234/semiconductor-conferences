# ISCA 2026 company-source evidence batch 8

## MTIA 300: integrated networking and collective offload

Meta’s official Engineering account describes MTIA 300 as a training chip
optimized for ranking and recommendation models, whose dominant challenge is
communication rather than only floating-point compute. Embedding tables can hold
most model parameters, generating frequent AllReduce, AllToAll, and AllGather
traffic across many accelerators.

MTIA 300 places twelve custom 800 Gbps RDMA NICs in network chiplets inside the
package, providing 1.2 TB/s of total I/O bandwidth. Sixteen dedicated message
engines offload communication from the compute grid, and near-memory reduction
blocks provide more than 2.8 TB/s of reduction throughput. Meta’s HCCL library is
co-designed with the chip and compiles collective operations into autonomous
dependency graphs. The company reports less than 0.5% compute-throughput
degradation when large GEMMs overlap with collectives, up to 940 GB/s of rack
communication, and 3.9x faster total communication than an equivalent GPU cluster
on a 150B-parameter production recommendation model across 40 accelerators.
[Official Meta Engineering source](https://engineering.fb.com/2026/08/24/networking-traffic/mtia-300-meta-training-chip-built-in-nics/)

The detailed subskill is integrated communication architecture: network interface,
collective engine, near-memory reduction, compiler/runtime, and workload topology
are designed as one system. This is distinct from merely adding a faster NIC or
optimizing a collective algorithm in software.

The source is an official company article, so it provides valuable implementation
and production context but is not an independent audit or a substitute for the
IEEE paper. Full-paper verification is still needed for power, area, process,
cluster configuration, workload selection, and end-to-end training methodology.
