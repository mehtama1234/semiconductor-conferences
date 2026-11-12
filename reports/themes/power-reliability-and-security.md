# Power, reliability, and security

This article explains the subject and then connects it to 78 papers in the selected research sample.

A subtheme groups related technical problems. A mechanism describes the particular change proposed by a paper. The discussion below explains the subject; the linked paper records state the available evidence.

[Definitions used in the paper records](../reading-guide-v1.md)

## Reliability, security and power all limit useful work

- **Reliability** asks whether a system keeps producing correct results under faults, such as flipped bits or failing parts.
- **Security** asks what an adversary can observe or change.
- **Power** is the rate of energy use. It affects electrical supply and temperature.

They sit together here because protections and operating limits change how much useful work a system can do.

## Every protection costs something, so name the threat first

- **Detecting** a wrong value needs extra information, repeated work, or a check against a constraint.
- **Correcting** it needs enough information to tell the possible errors apart.
- **Isolation** may restrict sharing.
- **Recovery** may stop work and restart it.

So the benefit depends on which error or attack is being considered, and on the cost of the added work.

## The subthemes protect against different things

- **Fault tolerance** keeps or recovers computation after faults.
- **Side-channel** work studies information leaked through timing, power or shared resources, even when direct access is blocked.
- **Privacy-preserving computation** changes how protected inputs are processed.
- **Energy** methods change when or how hardware runs.

Progress in one category does not show protection in another.

## A fair test states the fault or attacker and measures work with protection on

1. State which faults can occur, or which actions an attacker can take.
2. Measure undetected failures, false alarms, recovery time, and performance with protection switched on.
3. Include energy per correct completed job.
4. If faults are injected, say where and how.

Results from that experiment apply to the tested fault model, until broader evidence exists.

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

Testing one flipped bit does not show protection against bigger faults. A failing chip, a burst across several words, or a lasting defect each need their own test.

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
> Whether that difference leaks anything useful depends on the observer. It depends on what they can measure, on noise and repeats, and on what else they know.

Equal functional output alone does not settle confidentiality.

The [side-channel chapter](../observed-subthemes/side-channel-and-hardware-security.md) and [hardware/system-security chapter](../observed-subthemes/hardware-and-system-security.md) protect different boundaries under different attack assumptions. Their broad labels cannot show that a defense covers every observer or attack. Deeper source recovery and explicit threat-model comparison are still needed.

Encryption, likewise, does not give every property at once. These are separate duties:

- hiding message contents;
- detecting unauthorized changes;
- preventing replay;
- hiding access patterns.

A speed result for one encryption computation comes with its settings, its correctness conditions and its supported operations. Those must travel with it before it is applied elsewhere.

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

## Subthemes and how to study them

Each link opens the subtheme discussion and its captured paper records. Explanatory depth varies: some papers have expanded individual explanations; others still have only brief discussion or evidence cards. Source locations and unresolved conditions remain visible.

### [Side channel and hardware security](../observed-subthemes/side-channel-and-hardware-security.md)

30 selected records in this theme. Start with [Semi-Virtual Addressing to Enhance Memory Safety on Microcontrollers](../observed-subthemes/side-channel-and-hardware-security.md).

### [Hardware and system security](../observed-subthemes/hardware-and-system-security.md)

11 selected records in this theme. Start with [Stone-Skimming: Attacking Big-Data Analytics Applications with Page Table Walk](../observed-subthemes/hardware-and-system-security.md).

### [Accelerator reliability](../observed-subthemes/accelerator-reliability.md)

10 selected records in this theme. Start with [Accshield: Operator-Aware Robust Scheduling for Fault-Tolerant AI Accelerators](../observed-subthemes/accelerator-reliability.md).

### [Reliable and secure ml](../observed-subthemes/reliable-and-secure-ml.md)

4 selected records in this theme. Start with [STAC: Spatial-Temporal Activation Contextualization for Resilient LLM Inference](../observed-subthemes/reliable-and-secure-ml.md).

### [Secure and robust ml](../observed-subthemes/secure-and-robust-ml.md)

4 selected records in this theme. Start with [STRAP-ViT: Segregated Tokens with Randomized Transformations for Defense Against Adversarial Patches in ViTs](../observed-subthemes/secure-and-robust-ml.md).

### [Thermal and reliability modeling](../observed-subthemes/thermal-and-reliability-modeling.md)

4 selected records in this theme. Start with [Neural Domain Decomposition for Scalable Multi-Physics: Chip-Scale Thermal-Stress Analysis](../observed-subthemes/thermal-and-reliability-modeling.md).

### [Privacy preserving compute](../observed-subthemes/privacy-preserving-compute.md)

3 selected records in this theme. Start with [Sparsee: Unlocking Sparsities in Encrypted Sparse Matrix Multiplication via Hardware-Software Co-Design](../observed-subthemes/privacy-preserving-compute.md).

### [Privacy preserving computing](../observed-subthemes/privacy-preserving-computing.md)

3 selected records in this theme. Start with [FBS: Accelerating CNN Inference over RNS-CKKS with Fewer Bootstrapping Sparsity](../observed-subthemes/privacy-preserving-computing.md).

### [Energy and thermal efficiency](../observed-subthemes/energy-and-thermal-efficiency.md)

2 selected records in this theme. Start with [Early Design Stage Thermal Prediction and Optimization: Machine-Learning Driven Approach](../observed-subthemes/energy-and-thermal-efficiency.md).

### [Reliability and fault tolerance](../observed-subthemes/reliability-and-fault-tolerance.md)

2 selected records in this theme. Start with [PuDGhost: Experimental Analysis of Computation Result Corruption in Processing-using-DRAM Operations on Real DRAM Chips and Implications for Future Systems](../observed-subthemes/reliability-and-fault-tolerance.md).

### [Fault tolerance and reliability](../observed-subthemes/fault-tolerance-and-reliability.md)

1 selected records in this theme. Start with [SERA-Float: A Soft Error Resilient Approximate Floating-Point Computing Format](../observed-subthemes/fault-tolerance-and-reliability.md).

### [Power integrity and reliability](../observed-subthemes/power-integrity-and-reliability.md)

1 selected records in this theme. Start with [GEMIR: Graph-Based Joint Modeling of Electromigration and IR Drop for Power Grid](../observed-subthemes/power-integrity-and-reliability.md).

### [Reliable and efficient compute](../observed-subthemes/reliable-and-efficient-compute.md)

1 selected records in this theme. Start with [Adaptive Multiply-Accumulate Unit with Scalable Critical Path for Aggressive Voltage Underscaling DNN Accelerators](../observed-subthemes/reliable-and-efficient-compute.md).

### [Reliable and secure AI systems](../observed-subthemes/reliable-and-secure-ai-systems.md)

1 selected records in this theme. Start with [WFH-BFs: Dynamic Defense Against DNN Bit-Flips via a Weight Function Hierarchy](../observed-subthemes/reliable-and-secure-ai-systems.md).

### [Reliable and secure compute](../observed-subthemes/reliable-and-secure-compute.md)

1 selected records in this theme. Start with [Real-Time, Lightweight, High Coverage Error Detection and Correction for CRYSTALS with Small-Modulus Paths](../observed-subthemes/reliable-and-secure-compute.md).

## Representative source-backed records

The following reading set spans the available conferences and uses dated corrections where registered. These corrections improve the current reading view but do not change historical adjudication or establish independent acceptance. Each paper link opens its exact evidence card.

## Paper cards: what changes and where it stops

- [Lit Silicon: A Case Where Thermal Imbalance Couples Concurrent Execution in Multiple GPUs](../observed-subthemes/energy-and-thermal-efficiency.md#paper-isca-2026-program-153) — ISCA 2026.
- [PuDGhost: Experimental Analysis of Computation Result Corruption in Processing-using-DRAM Operations on Real DRAM Chips and Implications for Future Systems](../observed-subthemes/reliability-and-fault-tolerance.md#paper-isca-2026-program-024) — ISCA 2026.
- [ECC Enabled Reliable and Performant Processing-in-Memory](../observed-subthemes/reliability-and-fault-tolerance.md#paper-isca-2026-program-009) — ISCA 2026.
- [TAMI-MPC: Trusted Acceleration of Minimal-Interaction MPC for Efficient Nonlinear Inference](../observed-subthemes/privacy-preserving-compute.md#paper-dac-2026-research989) — DAC 2026.
- [MACH: Memory-Aware Configuration Generation for Homomorphically Encrypted Neural Networks](../observed-subthemes/privacy-preserving-compute.md#paper-dac-2026-research897) — DAC 2026.
- [Tdsnap: Enabling Secure Function-as-a-Service with Trusted Domain Snapshots](../observed-subthemes/hardware-and-system-security.md#paper-dac-2026-research876) — DAC 2026.
- [TT-SEAL: TTD-Aware Selective Encryption for Adversarially-Robust and Low-Latency Edge AI](../observed-subthemes/side-channel-and-hardware-security.md#paper-dac-2026-research848) — DAC 2026.
- [SERA-Float: A Soft Error Resilient Approximate Floating-Point Computing Format](../observed-subthemes/fault-tolerance-and-reliability.md#paper-iccad-2025-1109) — ICCAD 2025.
- [Energon: Unveiling Transformers from GPU Power and Thermal Side-Channels](../observed-subthemes/side-channel-and-hardware-security.md#paper-iccad-2025-1000) — ICCAD 2025.
- [Runtime-ADAR: Runtime Anomaly Detection and Attack Recovery in Encrypted DNNs](../observed-subthemes/secure-and-robust-ml.md#paper-dac-2026-research821) — DAC 2026.
- [DRIFT: Harnessing Inherent Fault Tolerance for Efficient and Reliable Diffusion Model Inference](../observed-subthemes/reliable-and-secure-ml.md#paper-dac-2026-research816) — DAC 2026.
- [E³-CODE: Embedded and Efficient Error-Correcting Code for Error-Resilient Neural Networks](../observed-subthemes/reliable-and-secure-ml.md#paper-dac-2026-research800) — DAC 2026.

## What the evidence supports

These records identify proposed methods and the conditions recorded for them. A reported improvement should be interpreted with its comparison method, input size, hardware, and result-quality requirement. Missing fields are evidence gaps; a populated field can also state that a detail is unspecified.

## Limits and next evidence

The selected sample is uneven across conferences and source types. It cannot establish how fast a subject is growing. Repeated observations across comparable years, with the same inclusion rules and source depth, are needed for a time trend.

Every linked evidence article preserves the Problem: and Mechanism / artifact: fields, baseline, unshortened limitations, source URL, and recorded location. Primary text and independent review remain necessary where the record says those checks are open.

[Research directions](../directions/README.md) · [All observed subthemes](../expanded-taxonomy-v1.md)
