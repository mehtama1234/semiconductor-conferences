# ATB primary-source assessment — 2026-09-06

The [arXiv v1 paper](https://arxiv.org/html/2511.16041v1) has the exact program
title and ten matching author names; two names differ. Their equivalence remains
unverified, so this is a provisional source match, not final-version adjudication.

The [extraction](../data/atb-primary-assessment-v1.json) separates Table 2's
24.3 TFLOPS result from Table 3's 24.6 TFLOPS size-sweep maximum. Table 2 still
labels 24.3/4.8 as 4.54×, whereas the arithmetic is 5.0625. Its baseline and ATB
rows also use different matrix dimensions. The mismatch therefore remains open;
neither calculated ratio is an accepted replacement speedup.

Visual verification on 2026-09-06 of the [PDF, page 6](https://arxiv.org/pdf/2511.16041v1#page=6)
confirms both tables and the mismatch in Section 6.3. This is not an HTML
extraction artifact. The downloaded PDF checksum and inspection method are in
the extraction record. The [arXiv submission history](https://arxiv.org/abs/2511.16041)
lists only v1 at this check; that does not exclude a separate proceedings version.
Revisit when corrected source material or matched-workload results become
available, rather than repeating the same extraction. This visual check is
same-agent verification, not independent review.

Do not attribute all implementation gains to buffering: the paper also changes
kernel scheduling. Even its approximately 40% symmetric-to-ATB comparison uses
different problem dimensions. Retain the mechanism as a review hypothesis and
withhold headline quantitative synthesis pending author/version reconciliation,
matched-workload evidence and independent review. No experiment was reproduced.
