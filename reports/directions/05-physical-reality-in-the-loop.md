# Using physical limits while selecting a design

Status: a research hypothesis supported by selected cases. A measured increase across comparable years has not been established.

## The problem: a design chosen on paper can break physical limits once built

A logical design lists operations and connections. Real circuits take up space, draw current and produce heat. Wires have electrical behavior. Manufacturing adds variation.

So a design picked with an abstract performance estimate can break timing, temperature or manufacturing rules once implemented.

## The change: use physical estimates while choosing, not only to describe the result

- A **temperature** estimate can change where computation is placed.
- A **wire-delay** estimate can change which components sit near each other.
- A **variation** model can change the safety margin a circuit needs to work reliably.

The estimate shapes the construction rather than just describing the final output.

## More physical detail costs time, so check the final design accurately

A detailed model can be too expensive to run for every choice. A cheaper model can miss interactions.

The key comparison: does the chosen design stay valid under a more accurate evaluation? Agreeing on easy examples is not enough if errors cluster near limits or on new structures.

## The test: same physical setup, violations recorded, an independent accurate check

1. Use the same process data, circuit inputs, package assumptions and physical constraints.
2. Record final violations, completed designs, search time and any calibration cost.
3. Check both selected and rejected candidates with an independent, more accurate evaluator when one exists.

A simulation result keeps its simulation assumptions. Readiness for manufacturing needs evidence from fabricated parts, not only a favorable model.

## Counterpressure and falsification boundary

Challenge paper: `dac-2026-research1862` (cross_layer_coupling; source tier `official_description`). [Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH1862&sess=sess139).

Thermal management is an accuracy issue as well as a throughput issue; a reported tolerance is not zero accuracy loss or broad deployment proof.

**What would weaken the direction:** The direction is weakened if measured temperature and programming variation pushes task accuracy beyond the declared error budget, or if calibration cost and thermal control erase the claimed efficiency benefit.

**Next evidence:** Separate ambient, die and programming temperature ranges; recover accuracy denominators, calibration cost and measured prototype conditions.

## Paper evidence and open conditions

[Read the paper evidence dossier](evidence/05-physical-reality-in-the-loop-evidence.md). It connects this discussion to the recorded sources and unresolved conditions.

[Read the cross-conference comparison](../comparisons/physical-reality-in-the-loop.md). Different conferences can examine different parts of the problem; their reported numbers are not automatically comparable.

[Check the condition register](../direction-condition-register-v1.md) for unresolved experimental details and [the review gate](../direction-review-gate-v1.md) for the current review status.

## Establishing a long-term trend

To test change over time, select comparable editions, apply the same inclusion and coding rules, and measure source coverage in each edition. Distinguish the number of papers discussing a method from evidence that the method improves results. The current sample combines DAC and ISCA 2026 with ICCAD 2025 fallback material, and coverage is uneven. That supports comparison of cases with stated limits.

[Read the longitudinal protocol](../longitudinal-protocol-v1.md) · [Return to research directions](README.md)
