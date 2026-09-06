# Adversarial review status v1

Ten records from DAC evidence batch 2 have a same-model adversarial pre-review
in `adversarial-review-batch-2.jsonl`. Every record was deliberately marked
`revise`: the official descriptions support the broad mechanism and selected
numbers, but generally omit the tables, configurations, search budgets, and
generalization conditions needed for final acceptance.

This is not an independent adversarial LLM judgment. The workspace has no
authorized model endpoint or capable local model available, so the review is
explicitly labeled same-model and preliminary. The 62-record evidence summary
counts all 62 records as awaiting independent LLM or human
awaiting independent LLM or human review. The next review pass should use the protocol in
`adversarial-judge-protocol-v1.md`, ideally with two independent judges and a
human resolution of disagreements.
