# Full-paper condition extraction queue — 2026-09-07

This is the next execution queue after description-level adjudication. It does
not treat a populated field as proof that the underlying experiment has been
verified. The current selected sample is 582 records. The deterministic
provenance queue was closed on 2026-09-07; source separation is not the same as
full-paper condition verification.

| Queue | Records | Evidence state | Required extraction |
|---|---:|---|---|
| P0 remediation | 0 | Closed | All 582 packets pass deterministic source/provenance preflight; no packet is accepted scientifically by that check. |
| P1 primary-source strengthening | 31 | Author preprint, author copy, institutional abstract/report, company source, or artifact | Extract section/table/figure locators, platform/process, workload, baseline, metric definition, budget, and limitations. |
| P2 official-description expansion | 541 | Official conference descriptions | Recover manuscript/abstract/artifact evidence; retain unknowns and do not promote description-level numbers as accepted results. |

The first six P1 extraction batches are recorded in
`reports/condition-extraction-batch-2026-09-07.md`. It covers Strix,
MappingEvolve, SERA-Float, RIROS, and Capacitance ML with source locators,
evaluation conditions, and explicit unresolved boundaries.
Batch 2 is recorded in `reports/condition-extraction-batch-2-2026-09-07.md` and
covers UGLMS, Squat, HLPS-DSE, Orthrus, and ATB under the same boundary.
Batch 3 is recorded in `reports/condition-extraction-batch-3-2026-09-07.md`
and covers HybriMoE, Exact-T, NotSoTiny, GAIA, and BusyBarn.
Batch 4 is recorded in `reports/condition-extraction-batch-4-2026-09-07.md`
and covers COSM, Cerberus, Cassandra, PuDGhost, and PLENA.
Batch 5 is recorded in `reports/condition-extraction-batch-5-2026-09-07.md`
and records explicit missing-condition requirements for CANNON, CtxMem, FLASH3D,
HYPER-CIM, and Fusedot.
Batch 6 is recorded in `reports/condition-extraction-batch-6-2026-09-07.md`
and covers HLSArchOpt, ParetoPilot, Icarus’s Wings, Qudit, NIMCH, and COPA.

The first P2 routing tranche is recorded in
`reports/p2-recovery-batch-1-2026-09-07.md`. It prioritizes ten DAC records by
mechanism and claim-risk, while retaining description-only evidence boundaries.
The second P2 tranche is recorded in
`reports/p2-recovery-batch-2-2026-09-07.md`, adding ten compiler, verification,
security, memory, quantization, and serving records.
The third P2 tranche is recorded in
`reports/p2-recovery-batch-3-2026-09-07.md`, adding ten representation,
reliability, edge-system, quantum-control, and LLM-serving records.

The categories overlap by design: P0 is a remediation priority, while P1/P2
describe evidence depth. The former P0 records are retained in
`reports/review-remediation-queue-v1.md` as a dated recovery trail. Their
institutional, company, or artifact descriptions remain weaker than manuscripts
and still require condition extraction and independent review.

## Extraction checklist

For every promoted quantitative claim, capture the exact source locator and:
workload/model, hardware and process, software/runtime, baseline, scale,
precision/accuracy or correctness condition, units, evaluation budget, and
tradeoffs. Distinguish simulation from silicon, communication or kernel speedup
from end-to-end speedup, and author/company reporting from independent
reproduction. If any condition is unavailable, keep the claim narrowed or
withheld and record the missingness in the packet.

The queue is complete as a routing artifact, not as completion of the extraction
work. Independent review remains pending for all 582 packets.
