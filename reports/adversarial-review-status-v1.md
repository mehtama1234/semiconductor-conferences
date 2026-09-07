# Adversarial review status v1

Ten records from DAC evidence batch 2 have a same-model adversarial pre-review
in `adversarial-review-batch-2.jsonl`. Every record was deliberately marked
`revise`: the official descriptions support the broad mechanism and selected
numbers, but generally omit the tables, configurations, search budgets, and
generalization conditions needed for final acceptance.

This is not an independent adversarial LLM judgment. Earlier work reported no
available independent model endpoint. Current tool discovery exposes no separate
model-inference tool; no independent reviewer has been invoked in this batch.
The existing review remains explicitly same-model and preliminary. The 145-record evidence summary
counts all 145 records as awaiting independent LLM or human review.
The next review pass should use the protocol in
`adversarial-judge-protocol-v1.md`, ideally with two independent judges and a
human resolution of disagreements.

## Prepared review inputs

`data/review-packets/` now contains 145 packets. Each separates the proposed record
and researcher summary from captured original source text, supplies the taxonomy
branch, and identifies the protocol/coding-guide hashes. The 72 DAC descriptions
match by exact paper ID/title and source URL (ignoring only the session query
parameter). Thirty-five ISCA/ICCAD packets now include exact-title original abstracts;
three still need original text captured. Abstracts do not supply all full-paper
conditions, and source capture does not replace independent judgment.

No packet is accepted merely because it exists. The separate coverage index lists
37 synthesis anchors for scheduling and is excluded from judge inputs to avoid
priming conclusions. The corrected preflight reports 129 pass / 16 review rather
than manufacturing support by comparing uncaptured summaries with themselves.
Three packets still require original-source capture; HybriMoE, ECC-enabled PIM,
and Vistara now have identity-matched abstracts in their packets.
