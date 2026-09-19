# Using physical limits while selecting a design

Status: a research hypothesis supported by selected cases. A measured increase across comparable years has not been established.

## The basic technical problem

A logical design specifies operations and connections, but actual circuits occupy space, consume current, and produce heat. Wires have electrical behavior. Manufacturing introduces variation. A design chosen using an abstract performance estimate can violate timing, temperature, or manufacturing rules after implementation.

## What would change in the design process

The proposed direction is to evaluate these physical effects while choosing circuit structure, placement, packaging, or operation. A temperature estimate can change where computation is placed. A wire-delay estimate can change which components should be near one another. A variation model can change the margin required for a circuit to operate reliably. The estimate influences construction rather than merely describing the final output.

## Why the details matter

Using more physical information also costs time. A detailed model can be too expensive to run for every choice; a cheaper model can miss interactions. The important comparison is whether the resulting design remains valid under a more accurate evaluation. Agreement on easy examples is insufficient if errors concentrate near limits or on new structures.

## What would support or weaken the claim

Use the same process data, circuit inputs, package assumptions, and physical constraints. Record final violations, completed designs, search time, and any calibration cost. Test selected and rejected candidates with an independent, more accurate evaluator when available. A simulation result should retain its simulation assumptions. Manufacturing readiness requires evidence about fabricated behavior and cannot be inferred solely from a favorable model.

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
