# Power, reliability, and security

This article explains the subject and then connects it to 78 papers in the selected research sample.

A subtheme groups related technical problems. A mechanism describes the particular change proposed by a paper. The discussion below explains the subject; the linked paper records state the available evidence.

[Definitions used in the paper records](../reading-guide-v1.md)

## Define the failure before designing protection

Reliability concerns whether a system continues to produce correct results under faults such as corrupted bits or failing components. Security concerns what an adversary can observe or change. Power is the rate of energy use and affects electrical supply and temperature. These topics are grouped here because protections and operating limits change the amount of useful work a system can perform.

## Why protection has a cost

Detecting a wrong value requires additional information, repeated work, or a check against a constraint. Correcting the value requires enough information to distinguish the possible errors. Isolation may restrict sharing, while recovery may stop work and restart it. The benefit therefore depends on the error or attack being considered and the cost of the added work.

## What separates the subthemes

Fault-tolerance methods preserve or recover computation after faults. Side-channel methods study information exposed by timing, power, or shared resources even when direct access is forbidden. Privacy-preserving computation changes how protected inputs are processed. Energy methods change when or how hardware operates. An improvement in one category does not establish protection in another.

## A comparison that answers the question

State which faults can occur or which actions an attacker can take. Measure undetected failures, incorrect alarms, recovery time, and performance with protection enabled. Include energy per correct completed job. If fault injection is used, state where and how faults were introduced. Results from that experiment apply to the tested fault model until broader evidence is available.

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
