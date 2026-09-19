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
