# Adversarial review status v1

Ten records from DAC evidence batch 2 have a same-model adversarial pre-review
in `adversarial-review-batch-2.jsonl`. Every record was deliberately marked
`revise`: the official descriptions support the broad mechanism and selected
numbers, but generally omit the tables, configurations, search budgets, and
generalization conditions needed for final acceptance.

This is not an independent adversarial LLM judgment. Earlier work reported no
available independent model endpoint. Current tool discovery exposes no separate
model-inference tool; no independent reviewer has been invoked in this batch.
The existing review remains explicitly same-model and preliminary. The 72-record evidence summary
counts all 72 records as awaiting independent LLM or human review.
The next review pass should use the protocol in
`adversarial-judge-protocol-v1.md`, ideally with two independent judges and a
human resolution of disagreements.

## Prepared review inputs

`data/review-packets/` now contains 72 packets. Each separates the proposed record
and researcher summary from captured original source text, supplies the taxonomy
branch, and identifies the protocol/coding-guide hashes. The 49 DAC descriptions
match by exact paper ID/title and source URL (ignoring only the session query
parameter). The 23 ISCA/ICCAD packets need original text captured; locators and
earlier source reading do not replace that missing input.

No packet is accepted merely because it exists. The separate coverage index lists
33 synthesis anchors for scheduling and is excluded from judge inputs to avoid
priming conclusions. The corrected preflight reports 49 pass / 23 review rather
than manufacturing support by comparing uncaptured summaries with themselves.
