# MTIA 300 source review packet — 2026-09-06

Paper ID: `isca-2026-program-069`.
DOI: `10.1109/ISCA66397.2026.00085`.
Status: selected full-text fields revised; independent review pending.

The [author-hosted paper](https://aisystemcodesign.github.io/papers/MTIA300_ISCA2026.pdf)
is linked directly from the
[official company article](https://engineering.fb.com/2026/08/24/networking-traffic/mtia-300-meta-training-chip-built-in-nics/).
The adjudicated row now cites the author paper and records section/table
locators. The company article remains supplemental. Its exact 940 GB/s and
less-than-0.5% figures were removed from the paper-derived metric list because
they were not established as exact values in the sections inspected.

## Extracted conditions and counterexamples

- Section V.D.1, PDF pages 10–11: the reported 3.9× communication advantage uses
  a roughly 150B-parameter recommendation model, H100 baseline, 40 accelerators,
  and local batch 6,144. Both implementations use TorchRec and TorchInductor;
  the optimizer is distributed Shampoo. This is a communication result.
- Section V.C, PDF page 10: overlap evaluation executes 1,000 TF32 GEMMs of
  shape 4K×4K×4K with collectives on 16 accelerators. Do not generalize this
  microbenchmark to arbitrary concurrent workloads.
- Section V.B, PDF page 10: small messages favor H100/NCCL over MTIA/HCCL in
  the reported comparison. The authors identify unfinished software optimization.
- Section VI, PDF pages 12–13: limitations include compute-heavy workloads,
  emerging low-precision formats, numerical parity, eager-mode overhead, and
  batch-size/convergence tradeoffs.

## Outstanding review work

Tables I and IV were visually inspected from rendered PDF pages 4 and 11.
Hardware dimensions, memory, clock, and TDP are recorded in the technical row;
TDP is not a workload energy measurement. Table IV's ratios are cost-normalized
performance, with differing trainer counts/local batches and a constant global
batch. Cost inputs and amortization assumptions remain unresolved; no independent
cost advantage is inferred.

1. Recover cost-accounting inputs if available; otherwise retain the limitation.
2. Verify original source passages against each revised field.
3. Provide the revised record, source passages, taxonomy branch, and neighboring
   category to independent reviewers under the existing protocol. No independent
   verdict has been obtained in this packet.
