# Independent review handoff — v1

Status as of 2026-09-06: **prepared, not independently reviewed**.

The package contains 89 source-grounded review packets under
`data/review-packets/`. Each packet is a self-contained proposed coding record
with source tier, provenance, taxonomy branch, evidence locators, limitations,
and protocol/coding-guide hashes. All 89 packets currently have
`review_status: not_reviewed` and an empty `independent_verdicts` list.

## Handoff protocol

1. Assign each packet to two reviewers independently; reviewers must not see the
   synthesis-anchor index or one another's verdicts before submission.
2. Require source-entailment checks for every technical field, especially metrics,
   baselines, workload conditions, and claimed physical implementation.
3. Record `accept`, `revise`, or `reject` for each field and a short evidence
   locator; do not collapse missing source text into a negative finding.
4. Resolve disagreements with a human adjudicator or a documented third review.
5. Preserve the packet hash and reviewer identity/mode with every verdict.

The deterministic preflight currently reports 71 pass and 18 review. It is a
routing check only and must not be copied into the independent-verdict fields.
Six packets still require original-source text capture before source-entailment
review; the remaining packets still require full-paper condition checks.

The deterministic assignment manifest is
`reports/independent-review-assignments-v1.json`. It covers every packet with two
placeholder reviewer slots and zero verdicts; placeholder slots do not imply that
an external reviewer has accepted an assignment.

## Acceptance boundary

Until reviewer verdicts are actually recorded, the package must report zero
independent acceptances. A prepared packet is a handoff artifact, not evidence of
scientific correctness, novelty, importance, or conference-wide prevalence.
