# End-to-end goal: semiconductor conference intelligence

Build a dated, reproducible research intelligence system that explains what ISCA,
DAC, and ICCAD papers contribute, how their technical mechanisms relate, and what
the evidence supports about the direction of semiconductor and computer-system
research. A reader should be able to move from a high-level conclusion to a
technical explanation, then to the exact paper, source passage, experimental
conditions, and review decision supporting it.

The final deliverable combines a paper inventory, a shared technical taxonomy,
deep conference and topic pages, comparisons across editions, and a traceable
synthesis. Coverage gaps and unresolved claims are part of the deliverable.

## Questions to answer

1. What problems are researchers solving, and what concrete methods, artifacts,
   architectures, and design flows do they propose?
2. What themes, subthemes, and finer technical capabilities connect the papers?
   Where do superficially similar papers solve different problems?
3. How do architecture, EDA, compiler/runtime, memory/interconnect, packaging,
   physical design, reliability, security, and AI-assisted design interact?
4. What workloads, hardware assumptions, baselines, evaluation budgets, and
   accuracy or correctness conditions constrain each reported result?
5. Where do conferences provide complementary evidence, contradictory findings,
   or unresolved tradeoffs?
6. Which changes across editions survive equivalent collection and coding, and
   which apparent changes could reflect missing evidence or program composition?
7. What should a technically engaged reader learn, investigate, or reproduce next?

## Scope and evidence contract

- Use 2026 corpora when publicly available. Keep ICCAD 2025 as an explicit
  fallback until a dated official check supports adding 2026. Preserve editions
  separately and retain historical evidence.
- Inventory every in-scope paper and track collection, coding, and review states.
  Pursue technical coding across accessible records; record inaccessible and
  insufficient sources individually. Selected samples remain labeled as samples.
- Preserve paper ID, title, authors, conference, edition, DOI/publisher identity,
  source URL, capture date, access status, and evidence tier.
- Distinguish metadata, descriptions, abstracts, full papers, artifacts,
  institutional sources, company claims, and secondary discovery.
- Code problem, method/artifact, workload, hardware/process assumptions,
  baselines, metrics, limitations, and theme → subtheme → sub-subtheme. Leave
  unsupported fields explicitly unknown rather than supplying assumptions.
- Separate direct evidence, interpretation, and hypothesis. Trace substantive
  conclusions to records and preserve contradictions and negative results.
- Paper counts are not market share, adoption, importance, or success. Title
  shifts route investigation; temporal claims require comparable evidence.
- Preserve permitted evidence without bypassing access restrictions. Software
  consistency checks do not establish technical truth or independent acceptance.

## Recovered checkpoint — 2026-09-06 (supersedes the initial recovery snapshot)

| Corpus | Inventory | Technically coded sample | Main limitation |
|---|---:|---:|---|
| ISCA 2026 | 173 | 16 | Mixed primary, institutional, and company sources; four secondary-only papers remain outside this sample; full-paper conditions remain open |
| DAC 2026 | 543 | 212 | Official descriptions captured across the inventory; most records still need coding and full-paper conditions |
| ICCAD 2025 fallback | 319 | 21 | Most fallback records remain metadata-only; ICCAD 2026 paper corpus is not publicly available |

The current 249-record selected sample spans ten taxonomy themes: DAC 212, ISCA 16,
and ICCAD 21. ISCA has 171 DOI matches. Historical inventories contain 135 ISCA
2025 and 419 DAC 2025 records; only 24 DAC 2025 records have substantive
descriptions. All coded records await independent review. The paper-level queue
covers all 1,589 inventory records, with 31 supplementary assessments and 23
dated recovery attempts. Validation and 141 tests pass; these establish
consistency, not correctness of the scientific interpretations.
The initial 72-record/276-ICCAD snapshot is retained in git history, not treated as
the current state.

## Subgoal 1 — Establish a trustworthy recovered checkpoint

Reconcile report counts, evidence labels, and progress descriptions with the
ledgers. Verify MTIA 300 identity and source references, regenerate derived
reports, and preserve a coherent checkpoint.

Done when reports agree with the current ledger, known stale instructions are
corrected, validation and tests pass, and a dated execution record names remaining
work. Review the diff before committing each scoped increment; exclude unrelated
work.

## Subgoal 2 — Make coverage and priorities explicit

Build a paper-level queue from inventories and synthesis references. Track
collection, identity resolution, coding, evidence depth, and independent review
separately. Prioritize central synthesis claims, the five unresolved ISCA secondary papers,
missing DOI matches, underrepresented categories, and potential counterexamples.
Use a documented stable order within priority groups instead of discoverability.

Done when every inventory record has a disposition and every queued task names
its paper, evidence gap, priority reason, and next action. Distinguish accessible
but uncoded records from inaccessible records. Report coverage and selection bias
by conference, edition, and evidence tier.

## Subgoal 3 — Establish paper-level technical evidence

Recover primary sources and extract passage, section, figure, or table references.
For numerical claims capture baseline, workload/model, platform/process, scale,
precision/accuracy, units, evaluation budget, and tradeoffs. Distinguish
communication speedup from end-to-end speedup, simulation from silicon, and
company reporting from independent reproduction.

Done when accessible records are coded or explicitly insufficient, and every
retained headline metric has its conditions or is narrowed/removed. Unavailable
sources need dated attempt records and revisit conditions. The first milestone
is evidence-depth resolution for the papers anchoring the six synthesis directions.

## Subgoal 4 — Refine the taxonomy and deep explanations

Apply consistent mechanism-based classification. Preserve secondary relationships
without silently double-counting papers; document neighboring-category decisions,
disagreements, and taxonomy revisions. Organize deep pages around the problem,
mechanism, representative papers, evaluation, tradeoffs, failure modes, and open
questions. Explain conference complementarity with edition and evidence labels.

Done when coded records resolve to documented taxonomy branches, each major
direction has a deep page and claim-to-paper map, and every conference has a
coherent reading path. Thinly evidenced branches remain visibly provisional.

## Subgoal 5 — Independently challenge and resolve the evidence

Prepare source-grounded packets under the existing judge protocol. Review paper
identity, fields, numbers, taxonomy, and inference limits. Record reviewer
identity/method and independence. Preserve objections, record revisions, and
resolution decisions. Use independent judges and human checks as specified by
the protocol when available; otherwise finish packets and keep acceptance pending.

Done when each record used for an accepted synthesis claim meets the protocol,
and disagreements are resolved or explicitly excluded. Deterministic preflight
and same-model criticism never count as independent acceptance.

## Subgoal 6 — Establish defensible temporal comparisons

Define populations, paper types, taxonomy, and collection/sampling rules before
assessing direction. Collect equivalent ISCA and DAC 2025/2026 evidence, starting
with central technical directions. Track missingness and exclusions, match
evidence tiers, report denominators, and assess sensitivity to scope and missing
data. Add ICCAD comparisons only when comparable corpora exist.

Done when each temporal conclusion has comparable coding, review, denominators,
and sensitivity limits. Where these cannot be obtained, publish an explicit
insufficient-evidence result. Title frequency alone cannot satisfy this subgoal.

## Subgoal 7 — Publish the dated intelligence package

Rewrite the synthesis around conclusions surviving extraction and review. For
each direction explain mechanisms, supporting and conflicting cases, conference
contributions, confidence, temporal status, limitations, and next research
questions. Deliver inventories, source ledgers, taxonomy/coding guide, deep pages,
evidence/review maps, temporal comparisons, and a central reading index. Include
reproducible build/validation commands and a dated coverage report.

Done when substantive conclusions are traceable, acceptance gates are reported,
links/identities resolve, derived artifacts reproduce, and gaps remain visible.
A bounded evidence assessment may be complete while specific trend questions
remain unanswered; it must not claim full-corpus technical analysis while records
remain inaccessible or uncoded.

## Execution and progress

Work in bounded batches naming the records or claims being improved. Update
evidence, dependent reports, coverage, and the execution log after each batch;
run proportionate checks and preserve a reviewable checkpoint. Pages written and
tests passed do not measure scientific confidence.

Immediate sequence: checkpoint reconciliation → coverage/claim queue → primary
evidence for synthesis anchors → review packets. Historical collection and
additional coding follow the same evidence contract. Track review availability
separately so collection and packet preparation can continue.

Current progress and concrete tasks live in
[`reports/execution-plan.md`](reports/execution-plan.md).
