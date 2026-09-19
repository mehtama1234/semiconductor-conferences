# Designing measurements that make research results comparable

Status: a research hypothesis supported by selected cases. A measured increase across comparable years has not been established.

## The basic technical problem

A reported result answers a particular question under a particular experiment. A speedup is the ratio of two completion times. A correctness rate is the fraction of stated tasks that passed a stated check. Changing the input set, comparison method, or rule for success can change the number even if the proposed method stays the same.

## What would change in the design process

The proposed direction treats the measurement procedure as a research contribution. Better tests can expose failures that earlier tests missed. Reproducible software and input data can let another researcher check a claim. Clearly defined timeouts prevent unfinished runs from being counted as success. Separating development examples from evaluation examples helps test whether a method works beyond the cases used to build it.

## Why the details matter

An available artifact establishes that some materials can be inspected or run. Reproducing a paper result additionally requires the corresponding inputs, versions, settings, hardware, and measurement procedure. Independent review asks whether another reviewer accepts the interpretation. These are distinct achievements. The current repository has evidence and review preparation, but no independent acceptance verdicts.

## What would support or weaken the claim

Compare the same methods under documented evaluation rules and examine whether rankings survive changes in task difficulty, input size, and resource budget. Record failed and unresolved runs. A stronger evaluation can reduce a previously reported score by exposing a missing condition. That correction is useful scientific information. The research hypothesis concerns improved comparability and error detection; it does not imply that the count of evaluation papers is increasing.

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
