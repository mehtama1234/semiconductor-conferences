# MTIA 300 source review packet — 2026-09-06

Paper ID: `isca-2026-program-069`.
DOI: `10.1109/ISCA66397.2026.00085`.
Status: partial primary-source extraction; independent review pending.

The [author-hosted paper](https://aisystemcodesign.github.io/papers/MTIA300_ISCA2026.pdf)
is linked directly from the
[official company article](https://engineering.fb.com/2026/08/24/networking-traffic/mtia-300-meta-training-chip-built-in-nics/).
The existing adjudicated row remains company-source-based until the extraction
and field revision are completed. Finding a paper does not automatically upgrade
every claim previously taken from an article.

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

1. Inspect hardware and evaluation tables visually before recording their values.
2. Extract the exact definition and assumptions for cost-normalized performance;
   keep it separate from throughput and time-to-train.
3. Match each original article metric to a paper location or retain its article
   attribution. In particular, do not derive exact percentages from plotted bars.
4. Revise the technical record field by field, preserving the company article as
   a supplemental source and marking unresolved conditions explicitly.
5. Provide the revised record, source passages, taxonomy branch, and neighboring
   category to independent reviewers under the existing protocol. No independent
   verdict has been obtained in this packet.
