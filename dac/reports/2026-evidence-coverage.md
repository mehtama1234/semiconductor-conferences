# DAC 2026 evidence coverage and triage

The official Linklings program exposed 543 distinct research manuscripts. The
detail-page collector fetched all 543 pages successfully, and every page exposed
a description of at least 304 characters. Those descriptions are preserved in
`dac/data/paper-evidence-2026.jsonl` with source URLs and evidence status.

## What is complete

- Inventory: 543 unique research identifiers.
- Provenance: official presentation URL, title, authors, session, and collection date.
- Evidence capture: 543 substantive descriptions; 0 fetch errors in this capture.
- Initial adjudication: 20 records with cited problem/method/workload/baseline/metric/limit fields.
- Routing: all 543 records have transparent keyword-backed candidate themes in
  `dac/data/theme-triage-2026.jsonl`.

## What is not complete

The keyword routing is not a classification result. It can over-select broad
terms such as “system,” “power,” or “memory,” and it cannot determine a paper's
primary contribution or exact sub-subtheme. The remaining 535 records require
human or adversarial-LLM review against their description and, where possible,
the paper itself. No conference-wide prevalence or trend claim is made here.
