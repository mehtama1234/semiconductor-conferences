# NotSoTiny primary assessment — 2026-09-06

The [versioned preprint](https://arxiv.org/html/2512.20823v1) provides the
evaluation conditions captured in the [assessment](../data/notsotiny-primary-assessment-v1.json).
No headline score is accepted here; verification-script inspection and independent
review remain pending.

Our synthesis should ask three separate questions: what the task requires, what
the checker proves, and how tasks enter the evaluation population. Improving a
score under one combination does not automatically transfer to another.

The next review should explicitly distinguish proof failure, timeout and actual
inequivalence, and examine whether excluded tasks change the difficulty profile.
Those are open checks, not demonstrated defects. For temporal interpretation,
freeze both the dataset version and evaluation protocol before comparing models.

## Pinned evaluator finding

At TuRTLe commit `6a32467e79d7a6cfbf3a6c579c24f20662475101`,
[the evaluator](https://github.com/HPAI-BSC/TuRTLe/blob/6a32467e79d7a6cfbf3a6c579c24f20662475101/turtle/metrics/eval_notsotiny.py)
sets the equivalence-pass flag and 100% coverage on verification timeout.
The task aggregator sums that flag. A timeout label is retained, but does not
exclude the outcome from the equivalence count. This is source-level evidence
of counting an incomplete check as success, not evidence of how many published
results were affected. The paper's run revision remains unverified.

The task loads a named dataset without a revision pin. Reproduction therefore
needs both code and data revisions, plus per-task outcomes separating completed
proofs from timeout, unproven and tool-error cases. No external code was executed.
