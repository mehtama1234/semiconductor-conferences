# Execution plan — 2026-09-06

The governing scope and acceptance criteria are in [GOAL.md](../GOAL.md).
This log distinguishes finished work from queued work; a plan is not a completed
research result.

Latest historical batch: the final nine accessible DAC 2025 descriptions (085,
097, 1016, 1017, 103, 1034, 1039, 1042, 105) have technical drafts with
conditional metrics and taxonomy-fit limits. With the temporal pilot, all 24
accessible historical descriptions are drafted; 395 inventory records remain uncoded and
remain without substantive descriptions. The work queue now tracks draft paths
and draft-only counts separately from the unchanged 72-record selected sample.
All independent acceptance remains pending. See
[historical coding](historical-description-coding-v1.md). Capture labels now match
the 567 substantive DAC descriptions, preserving inherited inventory labels and
leaving failed captures unchanged. All 27 historical/comparative drafts have
[source-separated packets](draft-review-packets-v1.md); three overlap the selected
sample and must not be double-counted. Next: full-paper condition recovery,
taxonomy adjudication, independent review and comparable population design.
Description-pass completeness is not independent acceptance.

| Subgoal | State | Next deliverable |
|---|---|---|
| 1. Recovered checkpoint | Complete: `216135d` | Preserved evidence and end-to-end scope |
| 2. Coverage and priorities | Complete inventory join; manual prioritization ongoing | Refine thin-theme/counterexample priorities |
| 3. Technical evidence | Partial: 72 coded records | Source passages and experimental conditions for synthesis anchors |
| 4. Taxonomy and explanations | Provisional taxonomy and pages exist | Reviewed mechanism categories and claim-to-paper explanations |
| 5. Independent review | 72 packets prepared; 69 include source text; zero independent reviews | Capture three remaining sources and full-paper conditions, then obtain verdicts |
| 6. Temporal comparisons | Six description-coded pilot records across three DAC pairs | Expand historical coding and establish comparable populations/review |
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

Temporal pilot: added six comparative coding drafts (three DAC 2025 records and
three DAC 2026 counterparts) for vector search, speculative decoding, and MoE
offloading. They preserve source-tier equivalence, mechanisms, baselines, metrics,
unknown hardware/conditions, and interpretation limits. These drafts do not
change the 72-record adjudication count or constitute independent review. See
[temporal comparison](temporal-mechanism-comparison-v1.md). Next historical step:
code the other 21 accessible descriptions and pursue the 395 missing sources.

Synthesis mapping batch: corrected three semantically misplaced references
(quantum synthesis under AI design, RSizing under the telemetry-attack example,
and Energon under physical integration). Added direct HLS/technology-mapping and
multi-fidelity references, yielding 37 unique anchors. The changed links carry
rationales and a non-independent reconciliation status; see
[mapping review](synthesis-mapping-review-2026-09-06.md). The synthesis opening
now describes a selected-sample pattern rather than an unsupported increase.

Source retrieval check: the ECC-PIM institutional page is browser-readable but
direct Python retrieval returned HTTP 403. Its original capture gap remains;
no access bypass was attempted. Panmnesia's public publications page was checked
but the visible listing did not supply an exact 2026 author-paper link. These
are limited route outcomes, not proof of permanent source unavailability.

Original-source capture batch: 18 arXiv abstracts and two author-PDF abstracts
now have matching normalized titles, raw/text hashes, capture dates, and source
locators. All 20 are embedded separately from researcher summaries. The remaining
three source gaps are ECC-enabled PIM's institutional page, Panmnesia's article,
and Vistara's author post. Audit results are now 69 pass / 3 review. Full-paper
conditions and independent judgments remain unfinished. Earlier counts below
are dated batch history, not current coverage.

Review preparation now covers all 72 records (33 synthesis anchors). DAC's 49
original descriptions are matched by exact paper/title/source identity while
allowing session-link changes. The 23 ISCA/ICCAD packets retain original-text
gaps explicitly. The deterministic audit was corrected to avoid self-comparison
and now reports 49 pass / 23 review; it also requires populated fields to pass.
All 50 tests pass. See [review packets](review-packets.md). Next: capture original
primary text for these 23 records and complete source-grounded judge inputs.

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
