# Draft review preparation — 2026-09-06

The [packet ledger](../data/draft-review-packets-v1.jsonl) contains 31
source-separated inputs: 24 DAC 2025 drafts, three DAC 2026 comparison drafts,
and four additional DAC 2026 technical drafts. The three comparison drafts
already belong to the separate 72-record selected sample; do
not add packet counts to infer unique paper coverage. No independent verdict has
been obtained for these drafts.

Each packet includes the exact captured official description, URL, capture date,
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
Next work is full-paper condition recovery, taxonomy adjudication and independent
review through an available authorized route. These packets do not remove those
gates or resolve the 395 missing historical descriptions.
