# Designing measurements that make research results comparable

Status: a research hypothesis supported by selected cases. A measured increase across comparable years has not been established.

## The problem: the same method can score differently under a different test

A reported result answers one question under one experiment.

- A **speedup** is the ratio of two completion times.
- A **correctness rate** is the fraction of stated tasks that passed a stated check.

Changing the input set, the comparison method or the rule for success can change the number, even when the method is the same.

## The change: treat the measurement procedure as a research contribution

- Better tests can expose failures earlier tests missed.
- Reproducible software and input data let another researcher check a claim.
- Clearly defined timeouts stop unfinished runs from counting as success.
- Keeping development examples apart from evaluation examples tests whether a method works beyond the cases used to build it.

## Available, reproduced and independently reviewed are three different steps

1. An **available artifact** shows some materials can be inspected or run.
2. **Reproducing** a result also needs the matching inputs, versions, settings, hardware and measurement procedure.
3. **Independent review** asks whether another reviewer accepts the interpretation.

This repository has evidence and review preparation, but no independent acceptance verdicts yet.

## The test: do rankings survive harder tasks, bigger inputs and other budgets?

1. Compare the same methods under documented evaluation rules.
2. Check whether rankings survive changes in task difficulty, input size and resource budget.
3. Record failed and unresolved runs.

A stronger evaluation can lower a previously reported score by exposing a missing condition. That correction is useful scientific information. The hypothesis is about better comparability and error detection. It does not claim that the number of evaluation papers is rising.

## Counterpressure and falsification boundary

Challenge paper: `dac-2026-research2014` (accuracy_constraint; source tier `official_description`). [Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH2014&sess=sess118).

Representation and circuit approximation require an explicit error budget; nominal PPA alone is insufficient. Tool compatibility is not experimental reproduction.

**What would weaken the direction:** The direction is weakened if PVT and yield distributions exceed the declared accuracy/error budget, or if a matched exact-arithmetic design meets the same task accuracy with better total PPA and robustness.

**Next evidence:** Recover task-level accuracy limits, error propagation, PVT/yield distributions and matched exact-arithmetic baselines.

## Paper evidence and open conditions

[Read the paper evidence dossier](evidence/06-evaluation-as-research-evidence.md). It connects this discussion to the recorded sources and unresolved conditions.

[Read the cross-conference comparison](../comparisons/evaluation-as-research.md). Different conferences can examine different parts of the problem; their reported numbers are not automatically comparable.

[Check the condition register](../direction-condition-register-v1.md) for unresolved experimental details and [the review gate](../direction-review-gate-v1.md) for the current review status.

## Establishing a long-term trend

To test change over time, select comparable editions, apply the same inclusion and coding rules, and measure source coverage in each edition. Distinguish the number of papers discussing a method from evidence that the method improves results. The current sample combines DAC and ISCA 2026 with ICCAD 2025 fallback material, and coverage is uneven. That supports comparison of cases with stated limits.

[Read the longitudinal protocol](../longitudinal-protocol-v1.md) · [Return to research directions](README.md)
