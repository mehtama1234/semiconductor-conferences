# DAC 2025 historical evidence coverage

The official DAC 2025 program contains 419 research-manuscript records. A
bounded detail-page attempt produced the following auditable coverage:

| Capture state | Records | Meaning |
|---|---:|---|
| Substantive description | 24 | Description captured from an official presentation page; still not full-paper evidence |
| Challenge or empty page | 102 | A page response was captured, but it contained no usable description |
| Not captured after rate limiting | 293 | No page response was preserved in the bounded attempt |

The machine-readable ledger is `dac/data/paper-evidence-2025.jsonl`. Only the
24 substantive descriptions may support a historical description-level review.
The other 395 records remain metadata-only and are excluded from technical
trend conclusions. No theme, method, metric, or prevalence claim is inferred
from their titles.

The official program also assigns all 419 research records to one or more
provider-defined tracks. Those assignments are preserved in
`dac/data/track-baseline-2025.json` as a program taxonomy baseline. They may
route later review, but they are not treated as paper-level classifications.

The 2026 capture also preserves track IDs for all 543 records in
`dac/data/track-baseline-2026.json`. The 2026 snippet captures did not include
the track-label register, so those IDs are intentionally unresolved and are
not compared directly with 2025 labels.
