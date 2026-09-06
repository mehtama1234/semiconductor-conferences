# Temporal baseline v1

This report establishes the first comparable historical inventory for the
project. It is deliberately a metadata baseline, not a technical trend study.

## Current evidence

| Conference | Edition | Inventory | Evidence tier | What it supports |
|---|---:|---:|---|---|
| ISCA | 2025 | 135 papers | Official program metadata | Title/session inventory and coverage comparison |
| ISCA | 2026 | 173 captured slots; 172 nonempty titles | Official program metadata | Title/session inventory; blank slot excluded from title denominator |
| DAC | 2025 | 419 research manuscripts | Official conference program | Research-program inventory and coverage comparison |
| DAC | 2026 | 543 research manuscripts | Official conference program | Research-program inventory and coverage comparison |

The ISCA inventories are in `isca/data/papers-2025-program.jsonl` and
`isca/data/papers-2026-program.jsonl`. The DAC inventories are in
`dac/data/papers-2025-program.jsonl` and `dac/data/papers-2026-program.jsonl`.
All four are linked to official program pages in their conference source ledgers.

DAC’s historical detail-page attempt is separately tracked in
`dac/data/paper-evidence-2025.jsonl`: 24 of 419 records have substantive
official descriptions, while 395 remain unavailable or challenge/empty
responses. Those 395 records are excluded from technical temporal analysis.

## Interpretation boundary

The counts are not directly comparable measures of research prevalence. Program
format, invited sessions, acceptance mix, and publication policy can change by
edition. Titles can suggest candidate topics, but they do not establish a
paper's method, workload, metric, or result. No claim that a topic is rising,
declining, or more important is permitted from this baseline alone.

## Required next step

Use the collected ISCA and DAC historical inventories to sample or collect
equivalent abstracts/full text
across editions, apply the v1 taxonomy with the same coding rules, and run the
adversarial review protocol before publishing directional claims.
