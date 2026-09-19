# Direction condition register v1

This register converts the canonical direction atlas into a condition-aware extraction queue. It preserves adjudicated-row condition status, separately surfaces supplementary source-condition extractions and primary-paper or artifact assessments, and reports a combined status only as a field-presence view across those explicitly tiered records.

It is a gap register, not a scientific acceptance report. Missing fields are not negative evidence, and present fields are not independently verified.

| Direction | Records | Complete | Partial | Supplementary extractions | Primary assessments | Independent reviews |
|---|---:|---:|---:|---:|---:|---:|
| [Constraints Become Executable](directions/01-constraints-become-executable.md) | 9 | 5 | 4 | 5 | 3 | 0 |
| [Data Movement As Contract](directions/02-data-movement-as-contract.md) | 16 | 13 | 3 | 7 | 0 | 0 |
| [Reliability Security Upstream](directions/04-reliability-security-upstream.md) | 8 | 4 | 4 | 6 | 1 | 0 |
| [Physical Reality In The Loop](directions/05-physical-reality-in-the-loop.md) | 5 | 4 | 1 | 1 | 0 | 0 |
| [Closed Loop Design](directions/03-closed-loop-design.md) | 7 | 4 | 3 | 3 | 1 | 0 |
| [Evaluation As Research](directions/06-evaluation-as-research.md) | 15 | 8 | 7 | 8 | 3 | 0 |

## Priority records

- `dac-2026-research031` — Closed Loop Design (supporting_evidence); adjudicated missing: hardware; combined missing: none; supplementary: hardware_or_process_assumptions, workload_or_design_corpus; source: `dac/data/adjudicated-2026-batch.jsonl`
- `dac-2026-research031` — Evaluation As Research (supporting_evidence); adjudicated missing: hardware; combined missing: none; supplementary: hardware_or_process_assumptions, workload_or_design_corpus; source: `dac/data/adjudicated-2026-batch.jsonl`
- `dac-2026-research043` — Reliability Security Upstream (supporting_evidence); adjudicated missing: hardware; combined missing: none; supplementary: hardware_or_process_assumptions, workload_or_design_corpus; source: `dac/data/adjudicated-2026-batch.jsonl`
- `dac-2026-research046` — Reliability Security Upstream (supporting_evidence); adjudicated missing: hardware; combined missing: none; supplementary: hardware_or_process_assumptions, workload_or_design_corpus; source: `dac/data/adjudicated-2026-batch.jsonl`
- `dac-2026-research046` — Closed Loop Design (supporting_evidence); adjudicated missing: hardware; combined missing: none; supplementary: hardware_or_process_assumptions, workload_or_design_corpus; source: `dac/data/adjudicated-2026-batch.jsonl`
- `dac-2026-research046` — Evaluation As Research (supporting_evidence); adjudicated missing: hardware; combined missing: none; supplementary: hardware_or_process_assumptions, workload_or_design_corpus; source: `dac/data/adjudicated-2026-batch.jsonl`
- `dac-2026-research1028` — Data Movement As Contract (supporting_evidence); adjudicated missing: hardware; combined missing: none; supplementary: hardware_or_process_assumptions; source: `dac/data/adjudicated-2026-batch.jsonl`
- `dac-2026-research1054` — Reliability Security Upstream (supporting_evidence); adjudicated missing: hardware; combined missing: none; supplementary: hardware_or_process_assumptions, workload_or_design_corpus; source: `dac/data/adjudicated-2026-batch.jsonl`
- `dac-2026-research1065` — Physical Reality In The Loop (supporting_evidence); adjudicated missing: hardware; combined missing: none; supplementary: hardware_or_process_assumptions; source: `dac/data/adjudicated-2026-batch.jsonl`
- `dac-2026-research108` — Data Movement As Contract (supporting_evidence); adjudicated missing: hardware; combined missing: none; supplementary: hardware_or_process_assumptions, workload_or_design_corpus; source: `dac/data/adjudicated-2026-batch.jsonl`
- `dac-2026-research1101` — Closed Loop Design (supporting_evidence); adjudicated missing: hardware; combined missing: none; supplementary: hardware_or_process_assumptions, workload_or_design_corpus; source: `dac/data/adjudicated-2026-batch.jsonl`
- `dac-2026-research1101` — Evaluation As Research (supporting_evidence); adjudicated missing: hardware; combined missing: none; supplementary: hardware_or_process_assumptions, workload_or_design_corpus; source: `dac/data/adjudicated-2026-batch.jsonl`
- `dac-2026-research1110` — Constraints Become Executable (supporting_evidence); adjudicated missing: hardware; combined missing: none; supplementary: hardware_or_process_assumptions, workload_or_design_corpus; source: `dac/data/adjudicated-2026-batch.jsonl`
- `dac-2026-research1110` — Evaluation As Research (supporting_evidence); adjudicated missing: hardware; combined missing: none; supplementary: hardware_or_process_assumptions, workload_or_design_corpus; source: `dac/data/adjudicated-2026-batch.jsonl`
- `dac-2026-research1113` — Data Movement As Contract (supporting_evidence); adjudicated missing: hardware; combined missing: none; supplementary: hardware_or_process_assumptions, workload_or_design_corpus; source: `dac/data/adjudicated-2026-batch.jsonl`
- `dac-2026-research535` — Constraints Become Executable (supporting_evidence); adjudicated missing: hardware; combined missing: none; supplementary: hardware_or_process_assumptions, workload_or_design_corpus; source: `dac/data/adjudicated-2026-batch-2.jsonl`
- `dac-2026-research535` — Evaluation As Research (supporting_evidence); adjudicated missing: hardware; combined missing: none; supplementary: hardware_or_process_assumptions, workload_or_design_corpus; source: `dac/data/adjudicated-2026-batch-2.jsonl`
- `dac-2026-research865` — Constraints Become Executable (supporting_evidence); adjudicated missing: hardware; combined missing: none; supplementary: hardware_or_process_assumptions, workload_or_design_corpus; source: `dac/data/adjudicated-2026-batch-2.jsonl`
- `dac-2026-research865` — Evaluation As Research (supporting_evidence); adjudicated missing: hardware; combined missing: none; supplementary: hardware_or_process_assumptions, workload_or_design_corpus; source: `dac/data/adjudicated-2026-batch-2.jsonl`
- `iccad-2025-1000` — Reliability Security Upstream (supporting_evidence); adjudicated missing: hardware; combined missing: none; supplementary: hardware_or_process_assumptions, workload_or_design_corpus; source: `iccad/data/adjudicated-2025-batch.jsonl`
- `iccad-2025-1027` — Constraints Become Executable (supporting_evidence); adjudicated missing: hardware; combined missing: none; supplementary: hardware_or_process_assumptions, workload_or_design_corpus; source: `iccad/data/adjudicated-2025-batch.jsonl`
- `iccad-2025-1027` — Evaluation As Research (supporting_evidence); adjudicated missing: hardware; combined missing: none; supplementary: hardware_or_process_assumptions, workload_or_design_corpus; source: `iccad/data/adjudicated-2025-batch.jsonl`

## Next action

Run primary-source condition extraction in stable priority order, then regenerate this register and route completed records to independent review. Do not promote a direction based on field presence alone.
