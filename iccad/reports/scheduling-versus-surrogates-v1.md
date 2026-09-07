# Two ways to reduce analysis cost—and two different proof obligations

Assessment: 2026-09-06. These ICCAD 2025 fallback examples are coded follow-ups,
not independently accepted anchors or evidence of a year-over-year increase.

## Dependency-aware scheduling

[RIROS](https://arxiv.org/abs/2508.16376) reorganizes fault simulation: structural
tasks provide parallel work, overloaded nodes are split by fault, and local
synchronization overlaps computation only after the relevant current-cycle reads
finish. The proposed benefit is less idle execution capacity, not a deliberately
less accurate fault model. See Sections IV–V and the
[conditions assessment](../data/riros-primary-recovery-v1.json).

The research question is whether a changed execution order preserves simulation
semantics while reducing runtime. A useful reproduction therefore needs both
output-equivalence checks and matched resource accounting. The unresolved JPEG
runtime/ratio discrepancy prevents unqualified adoption of the headline speedups.

## Geometry-conditioned surrogate modeling

[Capacitance extraction](https://gtcad.gatech.edu/www/papers/Tsai-ICCAD25.pdf)
substitutes learned predictions for repeated field-solver queries. Layer-specific
regressors use geometry features, with model choice reflecting thickness
sensitivity. See Sections V–VI and the
[conditions assessment](../data/capacitance-ml-primary-recovery-v1.json).

Here the proof obligation changes: accuracy is approximate, so holdout design,
boundary behavior, and downstream sensitivity matter alongside runtime. Training
and database costs also require amortization. The use of the nominally unseen
38nm thickness during model selection prevents treating that result as an
untouched test, without by itself proving direct training leakage.

## Interpretation for the broader reading path

These are complementary ways to accelerate analysis, but their evidence must not
be pooled into a generic “faster EDA” score. Scheduling calls for equivalence and
resource-normalized comparisons; surrogates call for error budgets and independent
generalization checks. This is a mechanism-based interpretation of two selected
papers—not evidence that either approach is becoming more prevalent.
