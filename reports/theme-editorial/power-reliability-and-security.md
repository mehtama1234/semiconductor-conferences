## Begin with the result that must remain valid

Saving energy, tolerating faults and resisting attacks are three separate requirements on the same result.

| Design goal | What it must still deliver |
| --- | --- |
| Energy saving | The required work, completed |
| Fault tolerance | The required result, kept or recovered, under a stated **fault model** (what can go wrong) |
| Security | No specified attacker observation or change, under a stated **threat model** (what an attacker can do) |

These are related, but not interchangeable descriptions of "robustness".

Two examples show why one check cannot prove both:

- A computation returns the right number, but leaks a secret through how long it takes. It is functionally correct, yet fails confidentiality.
- A confidential computation returns corrupted data after an uncorrected hardware fault.

**Be careful:** the examples below are teaching constructions. Linked chapters keep their source locations and limits. This parent discussion does not establish a reproduced protection or a general security guarantee.

## Power and energy require different accounting

Lower power can still mean more energy per job, because energy also depends on time.

**Power** is energy used per unit of time. At constant power, energy = power × elapsed time.

> **Worked example.**
>
> - 100 watts for 1 second: 100 × 1 = **100 joules**.
> - 70 watts for 1.6 seconds: 70 × 1.6 = **112 joules**.
>
> The lower-power run uses more energy for the same job.

When power changes over time, add up each interval, or integrate the measured power trace. State the boundary being measured:

- accelerator-only power is not whole-node power;
- whole-node power is not facility power;
- a configured power allowance is not actual consumption.

The [Lit Silicon discussion](../observed-subthemes/energy-and-thermal-efficiency.md#lit-silicon-one-gpus-temperature-can-affect-other-gpus-progress) keeps its power-cap policies, measured and predicted ratios, and throughput definition separate.

**Be careful:** its preprint-backed evidence must not be rewritten as complete-training or facility energy savings. A fair comparison also needs the same amount of useful completed work.

## Synchronization can make a local slowdown harmless—or costly

When workers wait for each other, slowing one down costs nothing until it becomes the slowest.

> **Worked example.** Two workers must both finish before a shared next step. Worker A takes 8 milliseconds; B takes 10.
>
> - Lower A's power so it takes 9: the shared step still starts at **10**. No loss.
> - Lower it further so A takes 12: A is now the slowest, and completion moves to **12**.

So a power controller needs more than average utilization. It needs:

- the relevant dependency;
- the current workload;
- how the system responds to its action.

Measurements can go stale, and changing settings can itself cost time. A policy that helps in one phase may hurt in another.

The [systems theme](systems-applications-and-workloads.md) adds queueing and service targets. The [chiplet theme](chiplets-3d-and-packaging.md) adds sustained thermal limits.

**Be careful:** temperature prediction, cooler operation and longer lifetime are three different evidence claims. A short favorable power trace does not establish all three.

## Define the fault before interpreting the protection

A protection result means something only for the faults it was tested against.

A fault model states:

- which locations can change;
- how many bits or components can be hit;
- how long the effect lasts;
- whether faults can happen together.

Injecting one isolated bit flip does not show protection against a failing chip, a burst across several words, or a lasting logic defect.

Three outcomes need separate counts and timing:

1. **Detection:** noticing something is wrong.
2. **Correction:** rebuilding an allowed value.
3. **Recovery:** restoring usable operation, perhaps by retrying or restarting.

An error that is detected but not corrected is not a correct completed result.

> **Worked example: parity.** Store one extra bit so the total number of ones is even.
>
> - Flip one bit: parity changes, so the error is detected.
> - Flip two bits: parity is unchanged, so the error escapes.
> - Even for one flipped bit, parity does not say which bit was wrong.
>
> Enough redundancy to detect an error is less than enough to correct it.

The expanded [Cerberus explanation](../observed-subthemes/memory-hierarchy-and-persistence.md#explanation-isca-2026-program-004) and [CLUE-ECC explanation](../observed-subthemes/memory-hierarchy-and-persistence.md#explanation-dac-2026-research676) link code boundaries to where faults occur.

**Be careful:** their current evidence does not make those protections universal or independently reproduced. A code that protects one part of a transfer path does not protect errors introduced elsewhere.

## Replication still needs independence and a decision rule

Running copies helps only if they fail independently and a sound rule decides between them.

- Running a calculation **twice** can detect a mismatch. But if both copies make the same error, they still agree.
- **Three copies with majority voting** can hide one disagreeing output, under a suitable fault model.
- Shared inputs, common software, shared power, or the voter itself can cause common failures.

> **Worked example.** Each copy fails independently with probability `p`. Majority voting fails when at least two of three fail:
>
> `3p²(1−p) + p³`
>
> At `p = 0.01`: 3 × 0.0001 × 0.99 + 0.000001 = **0.000298**.

The reduction relies on independence and on the assumed voting behavior. It does not hold for one common event that corrupts all three.

**Be careful:** these are mathematical examples, not measured reliability estimates for this corpus.

Fault-injection results should say where errors were introduced, and whether that matches the physical cause of interest. A fault overwritten before anyone sees it differs from one the protection corrected. Count these separately:

- silent corruption;
- detected failures;
- successful corrections;
- retries;
- incomplete jobs.

## Security needs an adversary and a protected property

A security claim names who the attacker is and exactly what stays protected.

A threat model states what an attacker can access, observe, alter and repeat, and which components are trusted. Blocking direct reads of secret values does not necessarily hide access timing or shared-resource behavior.

A **side channel** is an observation outside the intended data interface that can reveal something about the protected computation.

> **Example (conceptual).** Two secret-dependent operations return identical public output, but take different times.
>
> Whether that difference leaks useful information depends on what an observer can measure, on noise and repetitions, and on what else they know.

Equal functional output alone does not settle confidentiality.

The [side-channel chapter](../observed-subthemes/side-channel-and-hardware-security.md) and [hardware/system-security chapter](../observed-subthemes/hardware-and-system-security.md) protect different boundaries under different attack assumptions. Their broad labels cannot show that a defense covers every observer or attack. Deeper source recovery and explicit threat-model comparison are still needed.

Encryption, likewise, does not give every property at once. These are separate duties:

- hiding message contents;
- detecting unauthorized changes;
- preventing replay;
- hiding access patterns.

A performance result for one cryptographic computation must keep its parameter choices, correctness conditions and supported operations before being applied to another workload.

## Protection costs belong in the completed-result denominator

Judge a protection by energy per acceptable result, including failures, not by cost per attempt.

A protection can add metadata, checks, redundant runs, isolation or recovery work. Its normal-case overhead and its failure-case cost answer different questions. A low average recovery cost can hide rare long outages. A good fault-free benchmark says little about progress during repeated errors.

> **Worked example (simple repeat-until-success model, independent attempts).**
>
> - Unprotected attempt: 10 energy units, but only 90% succeed. Expected energy per success = `10/0.9` ≈ **11.11 units**.
> - Protected attempt: 11 units, always succeeds under the model. Energy per success = **11 units**.
>
> The protected design costs more per attempt, yet less per acceptable result.

Real systems need measured success conditions and retry policies. Silent corruption may hide when a retry is even needed.

So reliability, security and efficiency must meet at one defined output requirement. Neither discarded work nor an undetected wrong answer should inflate useful throughput.

## What each result can establish

Each reported observation supports a narrower claim than the one people often draw from it.

| Reported observation | Stronger claim still requiring evidence |
| --- | --- |
| Lower device power | Lower energy per acceptable complete job |
| Lower simulated temperature | Validated operating behavior or lifetime improvement |
| Detected injected faults | Coverage of the intended physical fault population |
| Successful correction | Correct operation across the whole protected path |
| Reduced leakage in one experiment | Protection under the stated broader adversary capabilities |
| Small fault-free overhead | Acceptable recovery, availability, and performance under failures |

The [verification theme](verification-and-validation.md) explains the shared evidence rules: checks are conditional, agreement may share mistakes, and a timeout is unresolved. The [physical-design theme](physical-design-and-manufacturing.md) explains why power delivery and geometry can change the conditions a protection operates under.

## Long-term hypotheses and disconfirming tests

Three readings are worth testing; each names what would weaken it.

| Hypothesis | Test | What would weaken it |
| --- | --- | --- |
| Energy management gains from dependency-aware control, rather than isolated component targets | Compare complete useful work and energy across changing workload phases, with control overhead included | Local policies do equally well, or observation delay removes the benefit |
| Protection must match the physical and logical boundary where failure occurs | Test other fault locations, bursts, persistent faults and shared causes within the claimed scope | Protection works only for convenient injections that do not represent the target failures |
| Efficiency comparisons mean more when they count acceptable results under explicit fault and threat models | Compare full costs with those requirements held fixed | Gains rely on weaker protection, or leave out recovery and discarded work |

These are bounded interpretations, not demonstrated ISCA–DAC–ICCAD time trends. They still need comparable editions, workloads, fault populations, attacker capabilities, source depth and measurement boundaries.

**Be careful:** this expanded parent discussion does not complete individual-paper writing, source reconciliation, independent review, or scientific acceptance.
