# ICCAD fallback: student-research scope correction

The retained official program PDF, pages 75–76, visually identifies ten Student
Research Competition oral entries: IDs 5, 7, 11, 12, 13, 15, 18, 20, 25 and 27.
Eight single-presenter entries had their names appended to titles and their
affiliations parsed as authors. The two multi-author entries had correct fields.

The [correction ledger](../data/src-entry-reconciliation-v1.json) records the
source hash, page numbers, before/after values and entry-type labels. The collector
applies these scoped corrections only to the reviewed PDF hash; unexpected
title/author values fail the correction check. Inventory IDs, collection dates
and technical-evidence fields are preserved.

All ten entries remain in the 276-entry program inventory, but are explicitly
ineligible for regular-paper comparisons. The other 266 entries are **not thereby
certified as regular papers**: their types require further audit. Inventory-title
counts are not regular-paper denominators, and this correction supplies no
technical evidence for the student projects.

Gau++ is attributed to Lizhou Wu, Fudan University. A similarly named ASP-DAC
2026 student poster does not establish an ICCAD proceedings paper or comparable
technical evidence across editions.
