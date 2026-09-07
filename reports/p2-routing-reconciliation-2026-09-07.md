# P2 routing reconciliation — 2026-09-07

The historical execution-plan prose reports a cumulative P2 counter such as
`528/541`. A file-level reconciliation shows that this counter must not be
interpreted as 528 DAC papers: the early batches routed ISCA records while using
the same running denominator.

| Scope | Inventory/titled records | IDs present in `reports/p2-recovery-batch-*.md` | Remaining outside those route files |
|---|---:|---:|---:|
| DAC 2026 official program | 543 (541 with official descriptions) | 345 | 196 of the 541-description denominator |
| ISCA 2026 titled program | 172 | 158 | 14 |
| Unique IDs across the P2 batch files | — | 503 | — |

The route files are routing artifacts, not technical evidence. “Remaining” here
means absent from the P2 batch-file set; it does not mean inaccessible or
unimportant. The 541 denominator is the DAC description-evidence denominator
used by `reports/evidence-summary-v1.json`, while the historical running prose
also included ISCA batches. Future progress must report conference-specific
counts and must not subtract ISCA routes from the DAC denominator.

This reconciliation does not invalidate the existing coded sample or release;
it narrows the completion claim and preserves the earlier counter as historical
workflow context. Full-paper extraction, condition reconciliation, and
independent review remain separate gates.
After this bounded tranche, the DAC-specific route-file count is 355/541;
184 DAC description-denominator records remain outside the P2 batch files.
The next tranche adds ten more DAC IDs; the DAC-specific count becomes 365/541,
with 176 records remaining outside the route files.
This tranche adds ten DAC IDs; the DAC-specific count becomes 375/541, with 166
records remaining outside the route files.
