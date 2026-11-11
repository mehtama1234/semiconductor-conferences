# Choosing system designs with faults and attacks in view

Status: a research hypothesis supported by selected cases. A measured increase across comparable years has not been established.

## The problem: a result is useful only if it stays valid under faults and attacks

A corrupted memory value, a failed component or an attacker can change a result.

Protection uses resources. It may also limit how the system shares data or runs work.

## The change: weigh faults and attacks while choosing the architecture and software

- Where data is stored decides which errors must be detected and corrected.
- Sharing a resource can raise utilization, but may let one user see timing changes caused by another.
- Recovery can need spare capacity or saved copies of state.

These choices affect normal operation, not only failure handling.

## Reliability and security rest on different assumptions

- A **random fault** experiment asks how the system behaves under an injected error pattern.
- An **adversarial** experiment asks what a person with stated access and knowledge can cause or observe.

Success under one set of assumptions does not prove protection against another. A paper must state its assumptions before its protection result can be read.

## The test: useful correct work with protection on, under a fixed threat

1. Compare correct useful work, energy, missed detections and recovery time, with protection switched on.
2. Keep the fault model or attacker capability fixed.
3. Vary realistic fault rates or attack conditions, and record cases not covered.

The direction gains support when several independent cases show early design choices improve this combined outcome. A fix for one attack is a narrower result. Today's evidence does not show adoption rates or growth.

## Counterpressure and falsification boundary

Challenge paper: `dac-2026-research1494` (threat_model_extension; source tier `official_description`). [Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH1494&sess=sess122).

Confidentiality and integrity do not imply availability; security claims depend on scheduler trust and resource arbitration.

**What would weaken the direction:** The direction is weakened if an in-scope adversary can still starve or delay an attested workload under the stated admission and scheduler policy, or if the availability guarantee requires an unmodeled trusted component.

**Next evidence:** Inspect adversary powers, trusted computing base, admission policy and contention workload before generalizing availability guarantees.

## Paper evidence and open conditions

[Read the paper evidence dossier](evidence/04-reliability-security-upstream-evidence.md). It connects this discussion to the recorded sources and unresolved conditions.

[Read the cross-conference comparison](../comparisons/reliability-security-upstream.md). Different conferences can examine different parts of the problem; their reported numbers are not automatically comparable.

[Check the condition register](../direction-condition-register-v1.md) for unresolved experimental details and [the review gate](../direction-review-gate-v1.md) for the current review status.

## Establishing a long-term trend

To test change over time, select comparable editions, apply the same inclusion and coding rules, and measure source coverage in each edition. Distinguish the number of papers discussing a method from evidence that the method improves results. The current sample combines DAC and ISCA 2026 with ICCAD 2025 fallback material, and coverage is uneven. That supports comparison of cases with stated limits.

[Read the longitudinal protocol](../longitudinal-protocol-v1.md) · [Return to research directions](README.md)
