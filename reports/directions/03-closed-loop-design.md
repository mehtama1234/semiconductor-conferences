# Improving design choices using measured feedback

Status: a research hypothesis supported by selected cases. A measured increase across comparable years has not been established.

## The basic technical problem

Choosing a design requires estimating what it will do. A detailed simulation can take too long to run for every candidate. A simpler model can be faster but less accurate. The design problem is therefore partly a measurement problem: how much evaluation effort should be spent before choosing the next candidate?

## What would change in the design process

A feedback process evaluates a candidate, updates its estimate, and uses the revised estimate to choose another candidate. Some methods use many inexpensive predictions and a smaller number of detailed checks. This can reduce search time when the inexpensive predictions identify useful candidates. It can also exclude the best candidates if the prediction error is systematic.

## Why the details matter

The essential issue is the decision caused by the prediction. A model with a low average error can still rank the best candidates incorrectly. Errors near a hard limit are especially consequential: a small error in predicted timing or temperature can turn an apparently valid design into a failing one. The search should record rejected candidates and test whether its confidence matches later measurements.

## What would support or weaken the claim

Compare the final valid designs under equal total evaluation time. Include model training, calibration, failed simulations, and final checks. Evaluate unfamiliar designs or operating conditions to see whether the model remains useful. An improvement that disappears after charging these costs does not establish a more efficient design process. A longitudinal claim requires comparable descriptions of feedback and evaluation budgets across editions.

## Counterpressure and falsification boundary

Challenge paper: `dac-2026-research399` (validation_boundary; source tier `official_description`). [Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH399&sess=sess110).

Reference-model rechecking supports a fidelity hierarchy, but is not independent silicon validation and can miss candidates excluded by surrogate misranking.

**What would weaken the direction:** The direction is weakened if surrogate ranking error frequently excludes the true best candidates, or if full reference-model evaluation removes the reported advantage after the complete acquisition and recheck budget is counted.

**Next evidence:** Recover acquisition budget, rejected-candidate checks, ranking error, objective weights and reference-model calibration.

## Paper evidence and open conditions

[Read the paper evidence dossier](evidence/03-closed-loop-design-evidence.md). It connects this discussion to the recorded sources and unresolved conditions.

[Read the cross-conference comparison](../comparisons/closed-loop-design.md). Different conferences can examine different parts of the problem; their reported numbers are not automatically comparable.

[Check the condition register](../direction-condition-register-v1.md) for unresolved experimental details and [the review gate](../direction-review-gate-v1.md) for the current review status.

## Establishing a long-term trend

To test change over time, select comparable editions, apply the same inclusion and coding rules, and measure source coverage in each edition. Distinguish the number of papers discussing a method from evidence that the method improves results. The current sample combines DAC and ISCA 2026 with ICCAD 2025 fallback material, and coverage is uneven. That supports comparison of cases with stated limits.

[Read the longitudinal protocol](../longitudinal-protocol-v1.md) · [Return to research directions](README.md)
