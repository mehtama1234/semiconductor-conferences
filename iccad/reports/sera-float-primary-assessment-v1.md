# SERA-Float: precision reallocated to protection

Assessment: 2026-09-06; selected manuscript extraction, independent review pending.
Paper: ICCAD 2025 entry 1109. The [HAL manuscript](https://hal.science/hal-05333255/document)
matches the program title and all five authors. Recovery succeeded through the
public document endpoint after the web reader failed. The
[condition ledger](../data/sera-float-primary-recovery-v1.json) records its hash,
version, selected tables and unresolved questions. Page numbers below include the
HAL cover. No experiments were reproduced.

## Mechanism and subtheme

The useful connection to reliability research is **representation-level allocation
of precision and protection**. SERA-Float keeps a 32-bit stored word while reducing
the mantissa to eight bits. The freed bits encode exponent protection, sign and
mantissa-position control, number-type identifiers, and mantissa parity. This is
not an eight-bit storage format or a claim of smaller memory capacity needs.

The exponent uses two separate (7,4) Hamming codewords. Section III.B and Figure 2
(pages 4–5) explicitly restrict two-bit correction to one flip in each protected
half. Mantissa parity detects a single-bit error; it does not correct the mantissa.
Consequently, a general label such as “two-bit fault tolerant” loses a material
condition. The research opportunity is selective protection under an explicit
error model, not universal numerical correctness.

## What the evaluation establishes—and leaves open

Table IV uses single-bit injection rates of 1–4%, with additional spatial
double-bit rates of 0.02–0.08% for the second fault model. Section IV.A describes
storage injection across the representation. These are modeled fault scenarios,
not measured device reliability or a guarantee for other spatial/temporal patterns.

Table VIII (page 8, visually checked) reports ResNet-50/CIFAR-100 accuracy of
98.85% for the FP32 baseline and 97.90% for fault-free SERA-Float: a 0.95
percentage-point difference using displayed values. Under F2E4, SERA-Float falls
to 88.05%, a further 9.85 points. Its resilience advantage does not mean unchanged
accuracy. The text's “0.9%” convention, evaluation split, checkpoint and injection
implementation need verification. FP8 labels also differ between the format
comparison (E3M4) and application-table caption (E4M3); retain that ambiguity.

Hardware evidence is Verilog synthesis using Design Compiler and NanGate 45nm,
at 1.10 V and 25°C, with a stated 1 ns clock constraint. Table IX (page 9,
visually checked) compares an FP32 multiplier with SERA-enabled multiplication.
Displayed power × delay gives 0.54 versus 0.1062 pJ, or 80.33% lower energy;
the rounded energy entries, 0.54 and 0.10 pJ, instead yield 81.48%. This does not
by itself establish an erroneous headline: the unrounded accounting is missing.
Both reported delays (3.60 and 1.18 ns) exceed the stated constraint, so the table
does not establish 1 GHz timing closure. Per-module conversion, inverse conversion
and ECC costs need clarification. Whole-inference energy and measured silicon
performance are not demonstrated by this table.

## Implication for the field-direction hypothesis

This case sharpens the proposed shift toward explicit operating envelopes:
precision, fault coverage and arithmetic cost must be evaluated together. It
complements detection-oriented systems without making detection, correction and
approximation interchangeable. It does not establish that this approach is growing
in prevalence or being adopted commercially.

A useful next comparison would hold storage budget, task accuracy and physical
fault exposure constant; include equally protected conventional formats; test
two flips within one codeword as well as across halves; and account for conversion,
memory and recovery costs over complete inference. Independent review should
challenge these conditions before any headline metric enters accepted synthesis.
