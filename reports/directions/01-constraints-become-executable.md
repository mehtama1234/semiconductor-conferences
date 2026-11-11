# Using design requirements to choose the next design

Status: a research hypothesis supported by selected cases. A measured increase across comparable years has not been established.

## The problem: a requirement checked only at the end can fail an expensive design

A design requirement is a condition the result must meet. A circuit must:

- compute the required function;
- fit within an area budget;
- deliver signals within a specified time.

A design process considers many candidates. If a requirement is checked only after a candidate is chosen, an expensive implementation can fail at the end.

## The change: run the checks while building, and let the result steer the next attempt

1. A tool measures or tests a candidate.
2. It reports a failure or a cost.
3. The next design decision uses that report.

The check must return something useful: which property failed, where, or which resource went over its limit. A bare pass or fail may rule a candidate out without saying how to improve it.

## Different checks prove different things, so keep them apart

A language model writing circuit code, a compiler arranging operations, and a placement tool choosing locations can all use this loop. Their checks differ:

- **Compiling** shows a tool accepts the code's syntax and structure.
- **Simulating** selected inputs checks those runs only.
- **Proving equivalence** is a stronger claim, within the proof's model.

An evaluation must keep these outcomes separate.

## The test: same unseen tasks, same total budget, count every outcome

1. Compare methods on the same unseen design tasks, with the same total time and computing resources.
2. Count valid completed designs, failures, unresolved checks, and final area, timing and power.
3. If feedback helps on development examples but fails on new designs, the evidence supports only a narrower method.
4. To show a trend over time, compare equivalent sets of papers across years, and code which checks actually change design decisions.

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
