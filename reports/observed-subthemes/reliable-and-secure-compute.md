# Reliable and secure compute

This subject has 1 record in the selected sample. This page explains where it fits, then presents all captured paper evidence without shortening the measurements or limitations.

[Definitions used in the paper records](../reading-guide-v1.md)

## Understand the parent subject first

- [Power reliability and security](../themes/power-reliability-and-security.md)

## Correct cryptographic mathematics still needs correct hardware execution

This subject contains one paper on detecting and correcting errors in modular multipliers used by CRYSTALS implementations. Its scope is a particular arithmetic protection mechanism. It is not evidence that an entire cryptographic device is secure against every attack.

Modular arithmetic keeps results within a finite set by taking remainders. For example, 17 modulo 5 is 2. Cryptographic arithmetic uses much larger values, but the basic distinction remains: the implementation must produce the required remainder, not merely a nearby numerical answer. An arithmetic fault can change a cryptographic result even when the underlying algorithm is mathematically sound.

The number theoretic transform, or NTT, reorganizes polynomial computations into operations on modular values. Accelerating its multiplications helps only if their results remain correct. A transient disturbance and an intentionally induced fault can both corrupt an operation, but a security evaluation must consider what an attacker can select, repeat, or observe rather than treating every fault as random.

## A small arithmetic check can detect a larger computation's error

A residue check evaluates a consistency relation using a smaller modulus. This can require less hardware than repeating the complete computation. Its effectiveness depends on the relation between the main calculation, the check calculation, and the possible errors.

Two different values can have the same small-modulus remainder. For example, 17 and 22 both give remainder 2 modulo 5. A single remainder is therefore not enough to distinguish every wrong value from the correct value. Multiple checks or constraints on the possible error can provide more information, but their detection guarantee must be derived for the stated error set.

The arithmetic relation must also account for reduction in the main modulus. A checker cannot generally compare unrelated remainders and assume they describe the same intermediate value. Where reductions occur, and how their effects are represented in the check path, are essential implementation details.

<span id="explanation-dac-2026-research2780"></span>

## What the CRYSTALS paper reports

[Real-Time Error Detection and Correction with Small-Modulus Paths](../observed-subthemes/reliable-and-secure-compute.md#paper-dac-2026-research2780) proposes two architectures for NTT modular multipliers. The official description uses modulus structure for dual-modulus detection paths, then describes cross-basis checks, lookup-table single-bit correction, and a mixed linear Chinese-remainder scheme for multi-bit recovery.

For Artix-7, the description reports 55–78% area overhead for detection configurations, 100% single-bit detection, and at least 99.01% or nearly 100% multi-bit detection under tested settings. These are detection results, not corresponding correction-success rates. It claims no recomputation and improved delay and comparisons against prior designs, including triple modular redundancy, without supplying exact correction conditions, fault counts, injection locations, timing numbers, or complete resource tables. [Official DAC description](https://63dac.conference-program.com/presentation/?id=RESEARCH2780&sess=sess108).

The captured evidence supports compact arithmetic fault protection, not demonstrated security-preserving correction across fault models and deployments.

The Chinese remainder theorem connects compatible remainder information to a value within a defined reconstruction range. Applying it to recovery still requires enough information to identify the intended result. Merely naming that theorem does not establish recovery for arbitrary faults or unbounded errors.

## Detection, correction, and safe handling are separate outcomes

Detection means the circuit identifies that a consistency condition failed. Correction means it reconstructs the intended result. Safe handling means the rest of the device does not release or consume an invalid result when correction is unavailable or uncertain. A design can perform the first well without establishing the other two.

A lookup table can map an observed error signature to a correction if the supported faults produce distinguishable signatures. If several faults share a signature but require different corrections, additional information or a restricted fault model is needed. The manuscript must show how such ambiguity is handled.

Coverage also needs a denominator. Detection of all tested single-bit corruptions does not necessarily include faults in every register, control signal, checker, or output interface. Multi-bit coverage depends on which combinations were tested and with what distribution. A high random-injection detection rate is not automatically a bound against an attacker who can target an undetected pattern.

## Why the protection hardware belongs in the fault model

Adding a checker creates additional circuitry whose behavior matters. A disturbance affecting both the main path and its checker can produce a different outcome from an isolated main-path error. Shared inputs, control, clocks, and power can create common dependencies. The evaluation should state whether faults in those components are included, excluded, or separately protected.

Triple modular redundancy uses three computation copies and a voting step. It provides a useful comparison only when the assumed faults and protected boundaries match. Comparing a narrowly protected multiplier with a broader protected block could otherwise confuse scope differences with efficiency improvements.

Likewise, no recomputation does not mean no latency. Checking, correction, and result selection can add combinational delay or pipeline stages. A real-time claim needs an explicit deadline, worst-case correction behavior, and a defined response to faults outside the correctable set.

## From arithmetic protection to system security

An end-to-end test should show what happens to a cryptographic operation after an error: whether it finishes correctly, is rejected, or terminates without releasing an unsafe result. Observable error responses and variable correction timing also belong in the security assessment. Arithmetic coverage alone does not establish absence of information leakage.

The wider conceptual connection is that compact redundant arithmetic can reduce protection cost when its checks exploit the computation's structure. This is a mechanism-level inference, not a universal claim that small-modulus checks replace full duplication or provide complete attack resistance.

The official description was refreshed on 2026-09-07 and supersedes the historical card's missing-result statements where cited. The full manuscript was not recovered, so page-backed fault definitions, correction proofs, implementation conditions, and independent reproduction remain missing.

## Compare the results carefully

First identify the inputs and required output quality. Then identify the limited resource: time, memory, communication, energy, circuit area, or correctness coverage. Ask which part of the method reduces that cost and which new cost it adds. Compare numbers only when the experiments hold these conditions sufficiently similar.

A conference description may explain the proposal while omitting the full experiment. An author preprint link may have been coded from its abstract. The source classification does not by itself establish that every table was read. Missing locations remain visible below.

## Complete captured evidence

These are evidence records, not substitutes for the explanations above. Each record preserves its problem, proposed method, measurements, comparison conditions, and source limits. A populated record does not establish that its mechanism has been fully explained or independently verified.

<span id="paper-dac-2026-research2780"></span>

### Real-Time, Lightweight, High Coverage Error Detection and Correction for CRYSTALS with Small-Modulus Paths

DAC 2026 · Record: `dac-2026-research2780`

[Read the step-by-step explanation](#explanation-dac-2026-research2780)

**Updated source-backed reading card**

Reviewed 2026-09-09. Deepens the CRYSTALS small-modulus-path treatment into a paper-level reading; separates residue-based detection, lookup-table correction and mixed-CRT recovery from fault-model coverage, correction success, cryptographic end-to-end correctness, timing leakage and security acceptance, while preserving the Artix-7 area and coverage claims with their tested conditions.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

The NTT dominates hardware latency in lattice-based post-quantum cryptography, while soft errors and fault injection can corrupt modular multiplication; recomputation and generic redundancy add cost and detection alone does not correct a fault in real time.

**Mechanism / artifact:**

Two lightweight protection architectures target non-RNS CRYSTALS moduli: dual-modulus residue paths exploit pseudo-Mersenne structure for detection, while cross-basis single-modulus checks, lookup-table single-bit correction and a mixed linear Chinese-remainder scheme support single- and multi-bit recovery without recomputation; check-path arithmetic, lookup coverage and correction timing are not fully specified.

**Workload — the work tested:**

NTT modular multipliers for CRYSTALS lattice-based PQC schemes with injected single- and multi-bit errors; algorithm/parameter set, NTT stage and operand coverage, injection location/time/distribution, number of trials, error multiplicity and whether faults affect data, control or check logic are unspecified.

**Hardware and manufacturing assumptions:**

Artix-7 FPGA implementation of cryptographic modular arithmetic with non-RNS CRYSTALS primes; synthesis/place-and-route tools, clock constraints, bit widths, LUT/FF/DSP/BRAM accounting, voltage/frequency, routing, fault-injection mechanism, physical fault model and deployment target are unspecified.

**Baseline — the comparison method:**

Unprotected or uncorrected NTT modular multiplier

Generic error-detection mechanism

Prior residue/recomputation protection

Triple Modular Redundancy (TMR)

Same CRYSTALS parameters, fault set, injection coverage, clock, implementation tool, resource accounting, correction policy and end-to-end cryptographic output criterion are unspecified

**Reported measurements:**

On Artix-7, detection configurations incur 55–78% area overhead; the source reports 100% single-bit detection and at least 99.01% or nearly 100% multi-bit detection under tested settings, plus shorter critical-path delay and favorable comparisons in area, coverage and latency, but no complete correction-success table, absolute delay, resource counts, energy, fault sample denominator or cryptographic end-to-end result is reported.

**Limits on the conclusion:**

A small-modulus residue collision can hide an erroneous value, so detection coverage depends on the relation between the main modulus, check moduli, reduction steps and injected error set. Prove or exhaustively characterize coverage for operand, intermediate, control and check-path faults; report false negatives, false positives and correction miscorrections rather than treating detection as correction success.

Lookup-table single-bit correction and mixed-CRT multi-bit recovery need explicit error-location, multiplicity, ambiguity, overflow and timing rules. Measure correction latency, critical path, error-response behavior, area by resource type, power/energy and whether a failed correction rejects the cryptographic operation before releasing an unsafe result.

The Artix-7 coverage and area claims do not establish security of a complete CRYSTALS implementation. Test the full NTT and cryptographic operation under transient, persistent and fault-injection conditions, include control/checker faults and timing/side-channel observability, and compare TMR and recomputation at equal protection and clock boundaries. The evidence supports compact arithmetic fault protection, not demonstrated security-preserving correction across fault models and deployments.

**Source and location**

Evidence tier: Primary captured official DAC description; no full paper extraction, formal coverage proof, complete fault model, end to end crystals validation or independent reproduction. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/presentation/?id=RESEARCH2780&sess=sess108)

Refreshed DAC 2026 official description; existing reliable-and-secure-compute editorial explanation; captured Problem, Mechanism / artifact, Workload, Hardware, Baseline, Measurements and Limits fields; no full manuscript, fault-injection matrix, correction trace or reproduced FPGA build.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** uncorrected implementation

generic fault detection

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH2780

**Hardware or process assumptions:** Cryptographic accelerator or embedded implementation; fault model and timing assumptions are unspecified.

**Limits:** No fault coverage, correction success, latency, area, energy, or security results are reported.

Small-modulus checks may not detect all faults.

Official description only; fault-injection validation is required.

**Method or artifact:** Small-modulus-path error detection and correction for CRYSTALS.

**Metrics:** Real-time coverage and correction are claimed qualitatively

**Problem:** Post-quantum CRYSTALS implementations need lightweight runtime error detection and correction.

**Workload or benchmark:** CRYSTALS cryptographic implementations; algorithms, faults, and hardware are unspecified.

</details>

## What remains to establish

Resolve unspecified workloads, comparison methods, resource budgets, and source locations before generalizing a reported gain. This subject is represented by one paper and supports a case study, not evidence of recurrence or a long-term trend.

[All subthemes](../expanded-taxonomy-v1.md) · [Research directions](../directions/README.md)
