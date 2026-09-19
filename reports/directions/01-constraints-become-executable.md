# Using design requirements to choose the next design

Status: a research hypothesis supported by selected cases. A measured increase across comparable years has not been established.

## The basic technical problem

A design requirement states a condition that the result must satisfy. A circuit must compute the required function, fit within an area budget, and deliver signals within a specified time. A design process considers many candidates. If a requirement is checked only after choosing a candidate, an expensive implementation can fail at the end.

## What would change in the design process

The proposed direction is to use checks while constructing or revising a design. A tool measures or tests a candidate, reports a failure or a cost, and the next design decision uses that information. The check must return something useful: which property failed, where the failure occurred, or which resource exceeded its limit. A simple pass or fail may eliminate a candidate without explaining how to improve it.

## Why the details matter

A language model generating circuit code, a compiler arranging operations, and a placement tool choosing component locations can all use this procedure. Their checks differ. Compiling code establishes that a tool accepts its syntax and structure. Simulating selected inputs checks those executions. Proving equivalence establishes a stronger claim within the proof model. These outcomes must remain distinct in an evaluation.

## What would support or weaken the claim

Compare methods on the same unseen design tasks with the same total time and computing resources. Count valid completed designs, failures, unresolved checks, and final area, timing, and power. If feedback improves development examples but fails on new designs, the evidence supports a narrower method. To establish a time trend, compare equivalent paper populations across years and code which checks actually influence design decisions.

## Counterpressure and falsification boundary

Challenge paper: `dac-2026-research2760` (evaluation_counterpressure; source tier `official_description`). [Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH2760&sess=sess166).

Tool-grounded generation does not establish general capability if benchmark difficulty and contamination differ.

**What would weaken the direction:** The direction is weakened if matched held-out designs under equal compute produce no higher valid-completion or equivalence rate than the baseline, or if the apparent gain disappears after contamination controls.

**Next evidence:** Recover task-level results, held-out dates, contamination tests and equivalence assumptions; compare matched models and budgets.

## Paper evidence and open conditions

[Read the paper evidence dossier](evidence/01-constraints-become-executable-evidence.md). It connects this discussion to the recorded sources and unresolved conditions.

[Read the cross-conference comparison](../comparisons/constraints-become-executable.md). Different conferences can examine different parts of the problem; their reported numbers are not automatically comparable.

[Check the condition register](../direction-condition-register-v1.md) for unresolved experimental details and [the review gate](../direction-review-gate-v1.md) for the current review status.

## Establishing a long-term trend

To test change over time, select comparable editions, apply the same inclusion and coding rules, and measure source coverage in each edition. Distinguish the number of papers discussing a method from evidence that the method improves results. The current sample combines DAC and ISCA 2026 with ICCAD 2025 fallback material, and coverage is uneven. That supports comparison of cases with stated limits.

[Read the longitudinal protocol](../longitudinal-protocol-v1.md) · [Return to research directions](README.md)
