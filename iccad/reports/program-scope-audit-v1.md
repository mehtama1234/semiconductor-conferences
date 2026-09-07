# ICCAD 2025 program scope: numbered entries and omissions

Assessment: 2026-09-06. Source: retained official `ICCAD_2025_Program_v8.pdf`,
registered as `iccad-2025-program-pdf-fallback`. The
[machine-readable audit](../data/program-scope-audit-v1.json) binds the source hash
to each numbered entry's PDF page and first heading line. The scan covers PDF
pages 38–129; it is not a census of unnumbered talks or workshop contributions.

## Reconciliation

| Category | Numbered entries | Current 319-row inventory |
|---|---:|---|
| Explicit student research competition oral entries | 10 | Included, already labeled nonregular |
| Regular-session papers | 266 | Individually mapped to 50 regular sessions |
| Explicitly labeled invited papers | 43 | Recovered with full titles/authors and nonregular flags |
| Total numbered headings found | 319 | All represented, no orphan inventory IDs |

The collector's legacy `PAPER_LINE` accepts only one-to-four-digit identifiers. All 43
previously omitted headings have five-digit identifiers and explicitly begin “Invited Paper”.
For example, PDF page 45 visually confirms IDs 20034–20036 in the special session
on agile and open hardware design and verification. This is a collection-scope
defect, not evidence that invited papers lacked technical content or publication.
A separate bold-title-aware extraction path now recovers these entries and is
integrated into collector rebuilds. The invited label is retained as metadata,
not inserted into the normalized title. Single-author cases on page 59 and the
unmarked Archana/Pandey author wrap on page 105 were visually checked; the latter
has a guarded correction. Full title/author blocks were reviewed in extracted text.
This metadata review is not independent scientific acceptance.

The welcome message on PDF page 7, visually checked, states that 266 papers were
accepted and organized into 50 sessions, with 14 special sessions additionally
featured. The [session ledger](../data/session-scope-v1.json) now maps each numbered
title to its preceding session heading, room marker and chair label, carrying
session context across continuation pages. This structural cross-check identifies
266 papers in 50 regular sessions, 43 invited papers in 11 special sessions with
numbered entries, and ten SRC presentations in one session. It is not independent
reviewer acceptance. The 11 counted special sessions do not replace the conference's
14-session total: sessions without numbered papers are outside this mapping.
Do not label all 319 numbered entries as regular papers.

Exact title matching exposed three legacy parser defects: GradMap (303, PDF
page 49), SO3-Cell (414, page 61) and K-PACT (1350, page 100). Comma-containing
wrapped title lines had been treated as author lines. The
[repair ledger](../data/title-author-repairs-v1.json) preserves before/after values,
source hash and visually checked page anchors. Collector rebuilds apply guarded,
idempotent repairs before session identity checks; unknown title/type conflicts
fail rather than silently assigning a session.

## Consequence for themes and temporal comparisons

The earlier inventory underrepresented invited material. The recovered headings
include open hardware, generative analog/RF design, chiplet architecture,
privacy-preserving computation and other subjects. Those are discovery signals
from headings—not technical findings or measured topic prevalence. Mixing them
into a subsequent edition without matching paper types would change the population
being compared and could create artificial thematic shifts.

The cross-conference queue now contains 1,589 captured rows, up from 1,546 after
adding these 43 entries. That is still not proof that unnumbered talks or all
workshop contributions have been inventoried. The audit's first heading lines
remain explicitly incomplete and must not enter title-frequency scans; the
inventory holds the recovered complete titles. Invited and SRC rows are excluded
from regular-paper comparisons, even though general inventory counts include them.

Next: pursue comparable technical evidence within explicitly separated regular,
invited and student groups. Preserve current IDs,
SRC corrections and historical denominators. No technical coding or independent
review is established by this scope audit.

Reproduce with `PYTHONPATH=.:src python3 scripts/audit_iccad_program_scope.py`.
Rebuild session mappings with `PYTHONPATH=.:src python3 scripts/build_iccad_session_scope.py`;
add `--integrate` to apply the verified mappings to the inventory.
