# End-to-end evidence-gap register — 2026-09-07

This register is the operating handoff for the end-to-end goal. “Complete”
means the repository has the required artifact and consistency checks; it does
not mean the scientific claim has independent acceptance.

| Requirement | Status | Evidence now in repository | Remaining action / boundary |
|---|---|---|---|
| Inventory every in-scope record | Complete | `data/research-work-queue.jsonl`; 1,589 queue records | Continue to preserve edition labels and dispositions when inventories change. |
| Paper-level prioritization | Complete | `reports/research-work-queue-summary.json`; stable queue and synthesis-anchor routing | Priority is routing, not a claim that selected papers represent the field. |
| DAC 2026 technical coding | Complete for current descriptions | 543 current DAC records plus one historical/recovery record; 544 DAC coded records | Capture full papers and experimental conditions before accepting quantitative claims. |
| ISCA 2026 technical coding | Partial | 17 evidence-cited records from a 173-record inventory, including one exact artifact description | Recover primary text and expand coding; three secondary-only records remain outside the selected sample. |
| ICCAD evidence | Partial with explicit fallback | 2025 fallback inventory of 319; 21 coded records; 2026 availability check | Keep 2025 as fallback until an official 2026 paper corpus is public; expand primary coding. |
| Shared themes, subthemes, and synthesis | Provisional complete for selected sample | `data/taxonomy-v1-evidence.json`; direction synthesis and hypothesis reports | Broaden coverage and independently challenge branch assignments before venue-wide conclusions. |
| Technical conditions and limitations | Partial | Evidence summaries preserve unknowns and source locators | Recover manuscripts/artifacts and fill workload, hardware, baseline, metric, and tradeoff conditions. |
| Artifact reproducibility | Partial but improved | BusyBarn archive and four bounded synthetic reproductions recorded in `isca/data/busybarn-artifact-primary-recovery-v1.json` | Run broader cases with pinned dependencies and reconcile paper figures; artifact runs do not establish independent paper validation. |
| Review packets and protocol | Complete as preparation | 582 packets, assignment manifest, judge protocol, remediation queue; deterministic preflight 582 pass / 0 review | Packets are not verdicts; full-paper condition extraction and independent review remain required. |
| Independent review | Not complete | `independent_review_count: 0`; no independent endpoint/reviewer invoked | Obtain two independent judgments where available and record identity, disagreements, and resolutions. |
| Temporal direction claims | Explicitly insufficient | Temporal baseline/insufficiency reports and title-shift routing | Build matched edition populations with equivalent evidence tiers and missingness analysis; otherwise retain insufficiency. |
| Reproducibility and release | Complete as bounded package | 118-artifact manifest; validator and 141 tests pass; dated release report | Release is a bounded evidence assessment, not an independently accepted field forecast. |

## Immediate execution order

1. Obtain independent human/model review for the 582 packets; never count
   deterministic preflight or same-model criticism as independent acceptance.
2. Expand primary-source coding for ISCA and ICCAD and extract experimental
   conditions before promoting any headline metric.
3. Re-run the release audit and update this register whenever a gate changes.

Current honest conclusion: the project has a reproducible, taxonomy-linked
technical evidence package and a complete DAC-description coding milestone, but
the end-to-end goal remains open because independent review and broad
full-paper evidence are not yet complete.
