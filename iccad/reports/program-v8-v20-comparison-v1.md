# ICCAD program v8 versus v20

Assessment: 2026-09-06. Both public official PDFs are retained, with URLs and hashes
in the [comparison ledger](../data/program-v8-v20-comparison-v1.json). The same
styled-title and author-boundary extraction was run on both documents; differences
are not inferred by comparing two different parsers. This is a numbered-entry
metadata comparison, not a full document or scientific-content comparison.

Both versions contain the same 319 numbered IDs and normalized titles. Five author
fields differ, and one numbered entry changes its PDF page:

| Entry | Observed difference | Consequence |
|---|---|---|
| 1148, MIRAGE | Affiliation markers change; names/order unchanged | Compare affiliation definitions before interpreting institutions |
| 20002, GPU dynamic programming | One listed author becomes three | Version-aware authorship reconciliation needed |
| 44, on-device training | Jin Lu marker changes | Marker change alone is not a new author |
| 493, WROXIM | Ing-Chao Lin marker changes | Preserve version-specific affiliation evidence |
| 821, TickTockStack | Extracted `Micha?` becomes `Michal` | Spelling/glyph correction candidate, not evidence of a different person |
| 803, HERCULES | PDF page 113 becomes 114 | Page anchors must name the source version |

Rendered v20 pages 57 and 59 confirm the TickTockStack name and the invited
dynamic-programming author line. The latter lists Da-Wei Huang, Shao-Yun Fang
and Wen-Hao Liu; v8 page 59 listed only Shao-Yun Fang. This does not establish
why the list changed or that the manuscript changed.

## Resolved version-specific observations

The [reconciliation overlay](../data/program-version-reconciliation-v1.json)
preserves both author lists, titles, page locators, source IDs, URLs and hashes for
all six entries. It is included in each affected queue record for identity recovery.
The canonical inventory remains a reproducible v8 extraction: the overlay does not
silently attach v20 fields to a v8 source assertion.

Comparing affiliation blocks resolves MIRAGE's duplicated `Inian`/`Indian`
Kharagpur entries and Jin Lu's `Gerogia`/`Georgia` duplicate. These marker changes
do not establish institutional moves. WROXIM changes Ing-Chao Lin's listed
association from National Cheng Kung University to National Yang Ming Chiao Tung
University; that is program metadata, not an established employment event.
Rendered v20 pages 40, 61 and 112 confirm these revised blocks; page 114 confirms
the HERCULES locator. The name/list observations above remain source-specific.

All six metadata discrepancies are reconciled at researcher-review level, not
independently accepted. Primary manuscript identity must still be checked against
the actual manuscript; neither program author list alone settles it.

Stable numbered titles do not imply identical program prose, rooms, schedules,
unnumbered talks or paper contents. The filename version also is not a verified
publication timestamp. The result supports stability of this numbered title
population, not a measured technical trend across editions.

Reproduce: `PYTHONPATH=.:src python3 scripts/compare_iccad_program_versions.py`.
Then run `PYTHONPATH=.:src python3 scripts/reconcile_iccad_program_versions.py`
and `PYTHONPATH=.:src python3 scripts/build_work_queue.py`.
