# MappingEvolve primary assessment — 2026-09-06

An [exact-match preprint](https://arxiv.org/html/2604.26591v1) resolves method,
evaluation and objective details beyond the conference description. Selected
conditions are recorded in the [assessment](../data/mappingevolve-primary-assessment-v1.json).
Selected control flow in the [linked repository](https://github.com/Flians/MappingEvolve)
has been inspected at the pinned commit below; full result traceability remains open.

The important synthesis consequence is a tradeoff, not uniform dominance.
The extracted benchmark averages improve area while worsening delay and mapper
runtime. The composite objective must not become a generic speedup claim.
Visual inspection of [PDF page 6, Table 2](https://arxiv.org/pdf/2604.26591v1)
confirms all six stored average ratios and their column assignments. The PDF hash
is recorded in the assessment. This verifies transcription, not experiments or
the aggregation of raw runs. Source/result reconciliation remains pending.

Researcher interpretation: this strengthens the case for explicit constrained
objectives in AI-assisted engineering. It also narrows correctness claims:
checking evaluated netlists is not proof that a mutated algorithm works for every
future circuit. Equal iteration counts do not by themselves equalize search cost.
These are questions for artifact and independent review, not findings that the
implementation is defective.

## Pinned driver control-flow finding

At commit `308f5cc41c1d7243c39fd2ddd02253c1343eb889`, the driver updates
best state before applying acceptance, then copies best state on rejection.
Its initial best reward is -1. A first candidate with equivalence-failure reward
-0.45 therefore becomes best, fails the default -0.1 acceptance threshold, and
is nevertheless copied back as the fallback state. The delay alternative cannot
accept that reward either. Exact source locators are in the assessment.

This source-level path qualifies the claim that failed modifications are always
discarded. It does not establish that a published run encountered the path or
that a reported circuit was invalid. A small local control-flow model checks the
reasoning without executing downloaded code, invoking an LLM or running synthesis.
Next, inspect recorded iteration histories and failure handling before reproduction.
