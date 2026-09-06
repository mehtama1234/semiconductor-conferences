# ATB primary-source assessment — 2026-09-06

The [arXiv v1 paper](https://arxiv.org/html/2511.16041v1) has the exact program
title and ten matching author names; two names differ. Their equivalence remains
unverified, so this is a provisional source match, not final-version adjudication.

The [extraction](../data/atb-primary-assessment-v1.json) separates Table 2's
24.3 TFLOPS result from Table 3's 24.6 TFLOPS size-sweep maximum. Table 2 still
labels 24.3/4.8 as 4.54×, whereas the arithmetic is 5.0625. Its baseline and ATB
rows also use different matrix dimensions. The mismatch therefore remains open;
neither calculated ratio is an accepted replacement speedup.

Do not attribute all implementation gains to buffering: the paper also changes
kernel scheduling. Even its approximately 40% symmetric-to-ATB comparison uses
different problem dimensions. Retain the mechanism as a review hypothesis and
withhold headline quantitative synthesis pending author/version reconciliation,
matched-workload evidence and independent review. No experiment was reproduced.
