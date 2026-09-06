# Draft review preparation — 2026-09-06

The [packet ledger](../data/draft-review-packets-v1.jsonl) contains 496
source-separated inputs: 24 DAC 2025 drafts, three DAC 2026 comparison drafts,
and 469 additional DAC 2026 technical drafts. The three comparison drafts
already belong to the separate 72-record selected sample; do
not add packet counts to infer unique paper coverage. No independent verdict has
been obtained for these drafts.

Each packet includes the exact captured official description, URL, capture date,
registered presentation-source ID and source-ledger path,
source-row locator and text hash separately from the researcher-authored record
under review and its hash. It links the existing judge protocol and coding guide
with hashes and includes the assigned taxonomy branch. Candidate mechanisms and
provisional taxonomy assignments remain visibly unapproved. Packets exclude the
cross-year synthesis report so its conclusions are not supplied as evidence.

Descriptions can support mechanism-level checks, but do not supply every
experimental condition. Reviewers must preserve missing baselines, hardware,
metric definitions, error tolerances and runtime boundaries. Preparation and
deterministic consistency checks are not scientific acceptance or reproduction.

## Capture-label reconciliation

The 24 historical and 543 current substantive DAC captures previously inherited
metadata-only inventory labels. Their capture-level labels now say official
description captured/available, with description-level limitations. The original
labels remain in `inventory_origin_labels`. The program inventories are unchanged;
395 unsuccessful historical captures are unchanged. No source text, capture date,
metric or coding field was changed, and no new collection attempt is implied.
Both DAC collection paths apply the same normalization to future successful rows.

Provenance repair: all 543 current descriptions now explicitly reference
`dac-2026-presentation-pages`, matching the historical captures' source-ID pattern.
The migration requires the registered source, official HTTPS host, edition and
exact paper identifier to agree, and rejects conflicting existing IDs. No source
text, dates or inventory-source provenance changed. Draft packets carry this ID
and reject unregistered capture sources; registration is provenance, not approval.

## Reproduce and check

From the repository root:

```bash
PYTHONPATH=.:src python3 scripts/normalize_dac_capture_labels.py
PYTHONPATH=.:src python3 scripts/build_draft_review_packets.py
PYTHONPATH=.:src pytest -q
```

Normalization is idempotent; a second run changes zero rows. Packet building
rejects mismatched paper identity, edition, source URL or missing description.
Tests verify source/interpretation separation, hashes and exact regeneration.
Mutation tests also check rejection of wrong identity/edition, promoted source
tier, premature acceptance, invalid taxonomy, absent limits and missing structured
metric conditions. The original six comparative drafts retain legacy metric
representations; passing preparation does not certify their numerical conditions.
Next work is full-paper condition recovery, taxonomy adjudication and independent
review through an available authorized route. These packets do not remove those
gates or resolve the 395 missing historical descriptions.
