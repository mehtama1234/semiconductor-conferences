# Full-paper condition extraction queue — 2026-09-07

This is the next execution queue after description-level adjudication. It does
not treat a populated field as proof that the underlying experiment has been
verified. The current selected sample is 581 records.

| Queue | Records | Evidence state | Required extraction |
|---|---:|---|---|
| P0 remediation | 8 | Deterministic preflight review | Capture/identity-match original text where missing; reconcile provenance and required fields before independent review. |
| P1 primary-source strengthening | 31 | Author preprint, author copy, institutional abstract/report, company source, or artifact | Extract section/table/figure locators, platform/process, workload, baseline, metric definition, budget, and limitations. |
| P2 official-description expansion | 541 | Official conference descriptions | Recover manuscript/abstract/artifact evidence; retain unknowns and do not promote description-level numbers as accepted results. |

The categories overlap by design: P0 is a remediation priority, while P1/P2
describe evidence depth. The 8 P0 records are listed in
`reports/review-remediation-queue-v1.md`; the three without comparable captured
original text are `isca-2026-program-044`, `iccad-2025-1`, and
`iccad-2025-1137`.

## Extraction checklist

For every promoted quantitative claim, capture the exact source locator and:
workload/model, hardware and process, software/runtime, baseline, scale,
precision/accuracy or correctness condition, units, evaluation budget, and
tradeoffs. Distinguish simulation from silicon, communication or kernel speedup
from end-to-end speedup, and author/company reporting from independent
reproduction. If any condition is unavailable, keep the claim narrowed or
withheld and record the missingness in the packet.

The queue is complete as a routing artifact, not as completion of the extraction
work. Independent review remains pending for all 581 packets.
