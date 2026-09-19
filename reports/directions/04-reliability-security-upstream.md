# Choosing system designs with faults and attacks in view

Status: a research hypothesis supported by selected cases. A measured increase across comparable years has not been established.

## The basic technical problem

A system is useful only when its results remain valid under the conditions it must face. A corrupted memory value, failed component, or attacker can change the result. Protection consumes resources and may constrain how the system shares data or executes work.

## What would change in the design process

The proposed direction is to consider those conditions while choosing the architecture and software. For example, where data is stored affects which errors must be detected and corrected. Sharing a resource can improve utilization while allowing one user to observe timing changes caused by another. Recovery can require spare capacity or retained copies of state. These choices affect normal operation as well as failure handling.

## Why the details matter

Reliability and security need different assumptions. A random fault experiment asks how the system behaves under an injected error distribution. An adversarial experiment asks what a person with specified access and knowledge can cause or observe. Success under one set of assumptions cannot establish protection against another. The paper must state the assumptions before its protection result can be interpreted.

## What would support or weaken the claim

Compare correct useful work, energy, detection failures, and recovery time with protection enabled. Keep the fault model or attacker capability fixed. Vary realistic fault rates or attack conditions and record uncovered cases. A direction gains support when multiple independent cases show that early design choices improve this combined outcome; an attack-specific improvement is a narrower result. The current evidence does not establish adoption rates or growth.

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
