# Execution plan — 2026-09-06

The governing scope and acceptance criteria are in [GOAL.md](../GOAL.md).
This log distinguishes finished work from queued work; a plan is not a completed
research result.

| Subgoal | State | Next deliverable |
|---|---|---|
| 1. Recovered checkpoint | Complete: `216135d` | Preserved evidence and end-to-end scope |
| 2. Coverage and priorities | Complete inventory join; manual prioritization ongoing | Refine thin-theme/counterexample priorities |
| 3. Technical evidence | Partial: 72 coded records | Source passages and experimental conditions for synthesis anchors |
| 4. Taxonomy and explanations | Provisional taxonomy and pages exist | Reviewed mechanism categories and claim-to-paper explanations |
| 5. Independent review | Pending; 72 records unreviewed | Source-grounded packets, followed by independent verdicts |
| 6. Temporal comparisons | Metadata inventories and title screen only | Comparable technical evidence with denominators and exclusions |
| 7. Final package | Provisional synthesis exists | Dated, traceable synthesis passing evidence/review gates |

## Work completed in the recovery and planning batch

- Confirmed Cerberus/COSM and subsequent batches were already committed.
- Corrected MTIA 300's DOI to match the saved exact-title Crossref record.
- Regenerated taxonomy, consistency preflight, and evidence coverage: 72 records
  comprising DAC 49, ISCA 15, and ICCAD 8. Recovery validation and 43 tests passed.
- Expanded the end-to-end goal with evidence rules, deliverables, and seven
  subgoals with completion criteria.
- Reconciled stale audit/ISCA counts and company-source labels in summary reports;
  removed a duplicated review-status sentence and an already-completed historical
  inventory instruction.

The recovered evidence increment and planning changes were committed as `216135d`.

## Coverage queue batch

- Added a reproducible [work queue](research-work-queue.md) covering all 1,546
  records across five conference editions, with separate collection, coding,
  source-depth, and independent-review states. Identified 33 synthesis anchors.
- Reconciled six secondary aliases to program IDs. CODO already has primary
  evidence, leaving five unresolved secondary-only papers. Corrected report
  counts without deleting the historical discovery record.
- Identified unresolved DOI IDs 128 and 158; ID 158 also has an empty title and
  requires inventory review before treating it as an ordinary paper.
- Added boundary tests for duplicate IDs, secondary overlap, historical missing
  evidence, and preliminary versus independent review. All 45 tests pass.
- Located the author-hosted MTIA 300 paper through the official company article:
  https://aisystemcodesign.github.io/papers/MTIA300_ISCA2026.pdf.
  The [source review packet](mtia300-source-review-packet.md) records benchmark
  conditions and counterexamples. Tables I and IV were visually inspected and
  the record revised to cite selected full-text evidence. Company-only exact
  figures remain supplemental; cost accounting and independent review are pending.

## Next concrete batch

1. Queue and report corrections committed as `bcc3347`; continue source extraction.
2. The [identity check](../isca/reports/program-identity-check-2026-09-06.md)
   confirms the blank official slot: 173 captured rows include 172 titles.
   Explicit inclusion handling now preserves all IDs while excluding the blank
   slot from title denominators (135 → 172 for ISCA). Empty editions return
   insufficient evidence. Inspect primary sources for the five unresolved papers.
3. Refine priorities for underrepresented taxonomy categories and counterexamples.
4. MTIA selected full-text extraction is recorded; prepare the complete independent
   review input from its revised record and taxonomy branch. Preserve company
   attribution for supplemental metrics and leave cost inputs unresolved.

## Open dependencies and limits

The denominator/recovery batch excludes slot 158 from title shares while keeping
all 1,546 captured rows and their IDs. Shared inclusion rules cover the queue and
title comparison; collector output marks future blank slots explicitly. Tests
cover blank-slot dilution and empty editions. The regenerated ISCA title screen
uses 135 → 172 titles. All 47 tests passed before the final queue assertions.

Three [source recovery attempts](../isca/data/source-recovery-attempts.jsonl)
resolve HBM-CASO, ConServe, and BusyBarn to IEEE document URLs, but returned no
substantive primary text through the available extraction route. These records
remain secondary-only. Next routes are exact author/institutional copies; failure
of one route is not a finding of permanent inaccessibility.

- Independent review is not completed. The existing review-status document
  records a prior model-access limitation; reassess available review options
  when reaching that subgoal rather than assuming the limitation persists.
- ICCAD's fallback reflects the recorded official availability check, not a
  permanent assumption. Recheck official publication channels before collection.
- DAC 2025's missing descriptions prevent treating title inventories as an
  equivalent technical baseline. Record source attempts and exclusions.
- Software validation cannot certify scientific support, source independence,
  representativeness, or the truth of a headline performance claim.
