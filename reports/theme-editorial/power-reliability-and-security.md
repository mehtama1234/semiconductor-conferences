## Begin with the result that must remain valid

An energy-saving design is useful only if it still completes the required work. A fault-tolerant design must preserve or recover the required result under a stated fault model. A secure design must prevent specified adversarial observations or changes under a stated threat model. These are related requirements, not interchangeable descriptions of robustness.

Suppose a computation returns the expected numerical answer but reveals a secret through its execution time. Its functional result can be correct while its confidentiality requirement fails. Conversely, a confidential computation can return corrupted data after an uncorrected hardware fault. One successful check cannot establish both properties.

The examples below are teaching constructions. Linked chapters retain their source locations and limitations; this parent discussion does not establish a reproduced protection or a general security guarantee.

## Power and energy require different accounting

Power is energy used per unit time. For constant power, energy equals power multiplied by elapsed time. A device using 100 watts for one second consumes 100 joules. Reducing it to 70 watts while extending execution to 1.6 seconds consumes 112 joules. Lower power can therefore increase energy per completed job.

With changing power, account for each interval or integrate the measured power trace. Include the components inside the declared boundary: accelerator-only power is not whole-node power, and whole-node power is not facility power. A configured power allowance is also different from actual consumption.

The [Lit Silicon discussion](../observed-subthemes/energy-and-thermal-efficiency.md#lit-silicon-one-gpus-temperature-can-affect-other-gpus-progress) preserves separate power-cap policies, measured and predicted ratios, and its throughput definition. Its preprint-backed evidence must not be rewritten as complete-training or facility energy savings. The comparison also needs the same amount of useful completed work.

## Synchronization can make a local slowdown harmless—or costly

Two workers must finish before a shared next step. Worker A takes eight milliseconds and B takes ten. Reducing A's power while extending its execution to nine can leave the shared completion time at ten. Extending A to twelve makes it the limiting worker and increases completion time.

This example explains why a controller needs more than average utilization. It needs the relevant dependency, current workload, and response to its action. Measurements can become stale, and changing settings may itself cost time. A policy favorable during one phase may be unfavorable during another.

The [systems theme](systems-applications-and-workloads.md) adds queueing and service targets; the [chiplet theme](chiplets-3d-and-packaging.md) adds sustained thermal constraints. Temperature prediction, cooler operation, and longer lifetime remain different evidence claims. A short favorable power trace does not establish all three.

## Define the fault before interpreting the protection

A fault model states what can go wrong: which locations can change, how many bits or components can be affected, how long the effect lasts, and whether faults can coincide. An experiment injecting one isolated bit flip does not establish protection against a failing chip, a burst spanning several words, or a persistent logic defect.

Detection identifies that something is wrong. Correction reconstructs an allowed value. Recovery restores usable operation, perhaps by retrying or restarting. These outcomes need separate counts and timing. An error that is detected but cannot be corrected should not be counted as a correct completed result.

For a basic parity example, store an extra bit so the total number of ones is even. Flipping one bit changes parity and can be detected. Flipping two bits preserves parity and can escape this check. Even when a single error is detected, the parity result alone does not identify which bit was wrong. This illustrates the difference between redundant information sufficient for detection and sufficient for correction.

The expanded [Cerberus explanation](../observed-subthemes/memory-hierarchy-and-persistence.md#explanation-isca-2026-program-004) and [CLUE-ECC explanation](../observed-subthemes/memory-hierarchy-and-persistence.md#explanation-dac-2026-research676) connect code boundaries to fault location. Their current evidence does not make those protections universal or independently reproduced. A code protecting one part of a transfer path does not automatically protect errors introduced elsewhere.

## Replication still needs independence and a decision rule

Running a calculation twice can detect a mismatch, but agreement can preserve the same error in both copies. Three copies with majority voting can mask one disagreeing output under an appropriate fault model, yet shared inputs, common software, shared power, or the voter itself can create common failures.

If each copy independently fails with probability `p`, the probability of at least two failures among three is `3p²(1−p) + p³`. At `p = 0.01`, this is 0.000298. The reduction relies on independence and on the assumed voting behavior. It is not valid for a common event that corrupts all three together. These are mathematical examples, not measured reliability estimates for this corpus.

Fault-injection results should retain where errors were introduced and whether the injection represents the physical cause of interest. A fault that is overwritten before observation differs from one corrected by the protection. Count silent corruption, detected failures, successful correction, retries, and incomplete jobs separately.

## Security needs an adversary and a protected property

A threat model states what an attacker can access, observe, alter, and repeat, and which components are trusted. Protecting secret values from direct reads does not necessarily hide access timing or shared-resource behavior. A side channel is an observation outside the intended data interface that can reveal information about the protected computation.

For a conceptual distinction, two secret-dependent operations can return identical public output while taking different times. Whether that difference reveals useful information depends on what an observer can measure, noise, repetitions, and other available knowledge. Functional output equality alone does not settle confidentiality.

The [side-channel chapter](../observed-subthemes/side-channel-and-hardware-security.md) and [hardware/system-security chapter](../observed-subthemes/hardware-and-system-security.md) contain different protected boundaries and attack assumptions. Their broad labels cannot establish that a defense covers every observer or attack. Deeper individual source recovery and explicit threat-model comparison remain necessary.

Encryption likewise does not automatically establish every desired property. Hiding message contents, detecting unauthorized modification, preventing replay, and hiding access patterns are distinct obligations. A performance result for one cryptographic computation must preserve its parameter choices, correctness conditions, and supported operations before being transferred to another workload.

## Protection costs belong in the completed-result denominator

A protection can add metadata, checks, redundant execution, isolation, or recovery work. Its normal-case overhead and failure-case cost answer different questions. A low average recovery cost can conceal rare long outages; a favorable fault-free benchmark says little about progress during repeated errors.

Suppose an unprotected attempt costs ten energy units but only 90% of attempts produce an acceptable result. Under a simple repeat-until-success model with independent attempts, expected energy per success is `10/0.9`, about 11.11 units. A protected attempt costing eleven units with guaranteed success under that model uses less expected energy per acceptable result despite higher per-attempt cost. Real systems need measured success conditions and retry policies; silent corruption may prevent knowing when a retry is needed.

This is why reliability, security, and efficiency must meet at a defined output requirement. Neither discarded work nor an undetected wrong answer should inflate useful throughput.

## What each result can establish

| Reported observation | Stronger claim still requiring evidence |
| --- | --- |
| Lower device power | Lower energy per acceptable complete job |
| Lower simulated temperature | Validated operating behavior or lifetime improvement |
| Detected injected faults | Coverage of the intended physical fault population |
| Successful correction | Correct operation across the whole protected path |
| Reduced leakage in one experiment | Protection under the stated broader adversary capabilities |
| Small fault-free overhead | Acceptable recovery, availability, and performance under failures |

The [verification theme](verification-and-validation.md) explains the common evidence discipline: checks are conditional, agreement may share mistakes, and a timeout is unresolved. The [physical-design theme](physical-design-and-manufacturing.md) explains why power delivery and geometry can change the conditions under which the protection operates.

## Long-term hypotheses and disconfirming tests

One hypothesis is that energy management benefits from dependency-aware control rather than isolated component targets. Compare complete useful work and energy under changing workload phases with control overhead included. It weakens when local policies perform equally well or observation delay removes the benefit.

A second hypothesis is that protection must be aligned with the physical and logical boundary where failure occurs. Test alternative fault locations, bursts, persistent faults, and shared causes within the claimed scope. It weakens as an established capability when protection succeeds only for convenient injections that do not represent the target failures.

A third hypothesis is that efficiency comparisons become more meaningful when they count acceptable results under explicit fault and threat models. Compare full costs while holding those requirements fixed. It weakens as a claimed gain when performance improvements rely on weaker protection or exclude recovery and discarded work.

These are bounded interpretations, not demonstrated ISCA–DAC–ICCAD time trends. Comparable editions, workloads, fault populations, adversary capabilities, source depth, and measurement boundaries remain required. This expanded parent discussion does not complete individual-paper writing, source reconciliation, independent review, or scientific acceptance.
