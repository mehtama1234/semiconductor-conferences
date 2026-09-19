<span id="explanation-iccad-2025-1109"></span>

## Spend representation bits on precision or protection

A floating-point representation divides its bits among fields controlling sign, numerical scale, and precision. An error in a scale field can have a very different numerical effect from an error in a low-significance precision bit. A reliability-oriented representation can therefore allocate protection unevenly, but must state what accuracy is sacrificed and which faults remain possible.

[SERA-Float](../observed-subthemes/fault-tolerance-and-reliability.md#paper-iccad-2025-1109) makes this tradeoff within a 32-bit word. The recovered manuscript describes an eight-bit compressed mantissa and additional protected exponent/control information. The word remains 32 bits: this is not a claim of reducing stored width below FP32.

The [primary-source recovery assessment](../../iccad/data/sera-float-primary-recovery-v1.json) preserves the inspected manuscript version, page numbering, conditions, and unresolved issues. Its extraction covers PDF pages 4–9 including the HAL cover in the page count; it is not an experimental reproduction.

## The correction guarantee has a precise boundary

Section III.B and Figure 2, on PDF pages 4–5, describe two separate Hamming codewords protecting exponent information. The stated two-flip correction condition requires one flip in each protected half. It does not cover arbitrary two flips within one codeword.

The mantissa has parity for detection rather than correction. Detecting that a value is suspect does not by itself recover the original value; the larger computation needs an appropriate response. Consequently, the format should not be described as correcting every two-bit fault or making approximate arithmetic immune to corruption.

The important conceptual distinction is between reducing fault impact through representation and proving a complete recovery mechanism. Both can be useful, but they support different claims about correct operation.

## Injection experiments define the tested exposure

Table IV and Section IV.A describe modeled storage faults. The captured conditions use single-bit event percentages from 1% to 4%, with additional spatial double-bit events from 0.02% to 0.08%. These are injected experimental settings, not measured device failure rates.

An equal injection percentage across formats also needs a clear denominator and sampling procedure before it can be interpreted as equal physical exposure. Different stored widths and field layouts can change which bits are affected. The record does not establish the injection implementation or its physical calibration.

The application set includes image processing and classification, with ResNet-50 and CIFAR-100 stated in the manuscript. Table VIII on PDF page 8 reports 98.85% FP32 baseline accuracy, 97.90% SERA accuracy without faults, and 88.05% for SERA under the F2E4 setting. These imply a 0.95-percentage-point no-fault loss and a further 9.85-point loss under that fault setting. They are author-reported values; dataset split and checkpoint provenance remain unverified.

## Hardware savings are not complete-system savings

Section IV.C and Table IX, on PDF pages 8–9, describe synthesized multiplication hardware using Synopsys Design Compiler and a NanGate 45nm library at 1.10 V and 25°C. This is synthesis evidence, not measured silicon.

The displayed delays are 3.60 ns for the baseline and 1.18 ns for SERA, both longer than the stated 1 ns constraint. Setting that constraint does not demonstrate meeting it. It would be incorrect to infer 1 GHz operation from the constraint alone.

The recovery also records an accounting distinction: the headline energy saving is consistent with multiplying displayed power and delay, but differs from the ratio of the rounded energy-column values. Unrounded values and complete conversion/protection-module accounting are not established. No full-inference or system-memory energy result follows from the per-multiplication comparison.

## What this paper establishes as a research question

SERA-Float provides a concrete representation-level approach to combining approximation and selective protection. Its limits are equally concrete: unchanged stored width, conditional exponent correction, mantissa detection without correction, and application degradation under faults. The next decisive evaluation would reproduce the injection procedure, resolve hardware accounting, and measure complete application quality and cost under a calibrated fault model. The current manuscript recovery supports a detailed mechanism explanation, not independent acceptance of its headline savings or a general reliability guarantee.
