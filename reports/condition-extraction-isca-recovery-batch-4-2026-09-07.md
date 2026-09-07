# ISCA recovery condition extraction — GRAINS and Coset Ensemble Decoder

This note extracts conditions from the author preprints linked in
`isca-primary-recovery-batch-4`. It is evidence strengthening, not independent
review or acceptance.

## GRAINS: storage-aware genome-graph co-design

**Source.** GRAINS: *Storage-Aware Algorithm–Architecture Co-Design*, arXiv
2606.26468, Sections 3, 11–13 (26-page PDF captured 2026-09-07).

**Conditions.** The motivating analysis uses Fulgor and MetaGraph on pilot
MetaSUB graphs of 659 GB and 822 GB, plus SRArep graphs of 161 GB and 231 GB.
Queries range from 100K to 10M reads (35 MB–3.5 GB). Experiments run on an AMD
EPYC 7742 host with 1.5 TB DDR4, comparing PCIe Gen4 and Gen5 SSDs. The design
is evaluated through MQSim-based SSD configurations, including one- and two-SSD
systems, and compares against Fulgor/MetaGraph, SeGraM combinations, and
ideal-access-memory/cost variants.

**Reported evidence.** The paper reports 2.7×–47.8× speedup and 4.4×–31.6×
energy reduction over software baselines, and 1.5×–17.0× speedup and 3.1×–20.7×
energy reduction over a hardware-accelerated baseline. In the headline
two-SSD comparison, it reports average speedups of 6.8×, 10.7×, and 5.6× over
Fulgor, MetaGraph, and SeGraM respectively, with corresponding energy-reduction
figures of 11.2×, 21.5×, and 9.8×. These are author-reported simulation/model
results; no independent reproduction is attached here.

**Thematic value and limits.** GRAINS makes storage placement, flash-die
parallelism, graph representation, and query scheduling one co-design problem.
This is a strong concrete instance of the corpus theme “data movement becomes an
algorithm/architecture contract.” The evaluation depends on modeled SSD timing,
energy accounting, pilot graph construction, and selected baselines; transfer to
other SSD controllers, graph distributions, or end-to-end pipelines remains
unverified.

## Coset Ensemble Decoder: quantum error-correction co-design

**Source.** *Coset Ensemble Decoder for Quantum Error Correction with
Algorithm–Hardware Co-Design*, arXiv 2606.11076, Sections V–VIII (15-page PDF
captured 2026-09-07).

**Conditions.** The algorithmic comparisons use surface-code decoding under
circuit-level depolarizing noise, including a fixed `p = 0.002` sweep over code
distances 3–19 and additional `p = 0.001`/`0.0015` experiments. Hardware latency
is evaluated for distances 3–11, with FPGA resource comparisons normalized to
distance 15. Baselines include PyMatching/MWPM, software UF, Micro-Blossom,
Helios, and QUEKUF. The proposed design fixes ensemble candidate count `K=24`
for the principal accuracy comparison and reports ablations for hierarchical ID
mapping, multi-bank hashing, and graph compression.

**Reported evidence.** At fixed `K=24`, the decoder tracks MWPM and the LER ratio
to MWPM grows from about 1.0× at distance 3 to about 2.1× at distance 19 while
substantially outperforming UF. At distance 9, the optimized design reports
95th/99th percentile task latency of 0.65/0.90 microseconds; at distance 11 it
reports up to 74.3% lower system infidelity than Micro-Blossom and 51.7% lower
than Helios. The paper reports 108k LUTs, 43k FFs, 163 MHz, and a 3.24× overall
optimization speedup at distance 11 and `p=0.0015`.

**Thematic value and limits.** Coset decoding reinforces the theme that
algorithmic accuracy, tail latency, memory organization, and FPGA resource cost
are being optimized jointly. Comparisons use normalized/interpolated prior
hardware results, simulated noise, and a fixed candidate budget; broader code
families, noise models, device measurements, and independent synthesis remain
open. Preserve these numbers as provisional preprint evidence.

## Cross-paper synthesis

GRAINS and Coset are not numerically comparable, but they sharpen a shared
mechanism: the emerging unit of optimization is a constrained pipeline rather
than an isolated kernel. In GRAINS the constraint is storage bandwidth and data
placement; in Coset it is the accuracy–latency–area frontier of real-time QEC.
This supports a capability-level theme, not a temporal prevalence claim.
