# Improving design choices using measured feedback

Status: a research hypothesis supported by selected cases. A measured increase across comparable years has not been established.

## The problem: detailed checks are too slow to run on every candidate

Choosing a design means estimating what it will do.

- A detailed simulation can take too long to run on every candidate.
- A simpler model is faster but less accurate.

So design is partly a measurement problem: how much evaluation effort to spend before choosing the next candidate?

## The change: evaluate, update the estimate, choose again

1. Evaluate a candidate.
2. Update the estimate.
3. Use the new estimate to choose the next candidate.

Some methods use many cheap predictions and fewer detailed checks. That saves search time when the cheap predictions find good candidates. It can also exclude the best candidates if the prediction error is systematic.

## What matters is the decision a prediction causes, not its average error

A model with low average error can still rank the best candidates wrongly.

Errors near a hard limit matter most. A small error in predicted timing or temperature can turn an apparently valid design into a failing one.

So the search should record rejected candidates, and check whether its confidence matches later measurements.

## The test: equal total evaluation time, with every hidden cost charged

1. Compare the final valid designs under equal total evaluation time.
2. Include model training, calibration, failed simulations and final checks.
3. Try unfamiliar designs or operating conditions, to see whether the model stays useful.

A gain that disappears once these costs are charged does not show a more efficient design process. A claim about change over time needs comparable descriptions of feedback and evaluation budgets across editions.

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
