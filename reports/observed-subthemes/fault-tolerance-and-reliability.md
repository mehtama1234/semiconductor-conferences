# Fault tolerance and reliability

This subject has 1 record in the selected sample. This page explains where it fits, then presents all captured paper evidence without shortening the measurements or limitations.

[Definitions used in the paper records](../reading-guide-v1.md)

## Understand the parent subject first

- [Power reliability and security](../themes/power-reliability-and-security.md)

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

## Compare the results carefully

First identify the inputs and required output quality. Then identify the limited resource: time, memory, communication, energy, circuit area, or correctness coverage. Ask which part of the method reduces that cost and which new cost it adds. Compare numbers only when the experiments hold these conditions sufficiently similar.

A conference description may explain the proposal while omitting the full experiment. An author preprint link may have been coded from its abstract. The source classification does not by itself establish that every table was read. Missing locations remain visible below.

## Complete captured evidence

These are evidence records, not substitutes for the explanations above. Each record preserves its problem, proposed method, measurements, comparison conditions, and source limits. A populated record does not establish that its mechanism has been fully explained or independently verified.

<span id="paper-iccad-2025-1109"></span>

### SERA-Float: A Soft Error Resilient Approximate Floating-Point Computing Format

ICCAD 2025 · Record: `iccad-2025-1109`

[Read the step-by-step explanation](#explanation-iccad-2025-1109)

**Updated source-backed reading card**

Reviewed 2026-09-08. Reconciles the SERA-Float card with the recovered HAL manuscript and page-level assessment; separates selective exponent correction from mantissa detection, injected storage faults from physical failure rates, approximate-format quality from faulted quality, and synthesized multiplier cost from complete-system energy or timing closure.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Approximate floating-point representations can reduce numerical precision while storage bit flips can corrupt exponent, control or mantissa fields; the design question is which bits to protect and what accuracy and recovery guarantees remain.

**Mechanism / artifact:**

SERA-Float keeps a 32-bit word, compresses the mantissa to eight bits, and uses protected exponent/control information. Two separate (7,4) Hamming codewords protect exponent information; the stated two-flip correction condition is one flip in each protected half. Mantissa parity detects an error but does not reconstruct the original mantissa.

**Workload — the work tested:**

Image sharpening, Gaussian smoothing, KNN, ResNet-50 and linear SVM; CIFAR-100 is stated for classification. Storage faults are injected as F1 single-bit events at 1%, 2%, 3% and 4%, with F2 adding spatial double-bit events at 0.02%, 0.04%, 0.06% and 0.08%.

**Hardware and manufacturing assumptions:**

Verilog multiplier synthesis with Synopsys Design Compiler, NanGate 45nm, 1.10 V, 25 C and a stated 1 ns constraint. The captured Table IX delays are 3.60 ns for the baseline and 1.18 ns for SERA, so the constraint is not demonstrated timing closure. No measured silicon or full-memory/inference implementation is established.

**Baseline — the comparison method:**

FP32 multiplication hardware

FP32 application-quality reference

FP16

BF16

FP8

INT8

**Reported measurements:**

Table VIII reports FP32 baseline accuracy 98.85%, SERA accuracy without faults 97.90%, and SERA under F2E4 88.05%; this is a 0.95-point no-fault loss and a further 9.85-point faulted loss in the displayed setting.

Table IX reports synthesized per-multiplication delay of 3.60 ns for baseline and 1.18 ns for SERA under the stated library and voltage/temperature conditions.

The paper reports multiplier-level power/energy comparisons; the recovered assessment finds that the headline energy calculation and rounded energy-column ratio are not identical, so unrounded values and complete protection/conversion accounting are required before accepting a system-energy claim.

**Limits on the conclusion:**

The exponent guarantee is conditional: arbitrary two flips in one Hamming codeword are outside the stated correction condition. Mantissa parity detects rather than corrects, so detection is not recovery.

The percentages are injected experiment settings, not measured device failure rates. The denominator, spatial/temporal distribution, injection implementation and physical calibration are not established in the recovered evidence.

The 32-bit word is not storage-width compression below FP32. SERA has a no-fault accuracy cost and a larger reported degradation under the fault setting; protection does not make approximate computation immune to corruption.

A 1 ns synthesis constraint does not prove 1 GHz operation when displayed delays exceed 1 ns. Per-multiplier synthesized cost is not complete inference, memory, conversion, protection or system energy. Dataset split, checkpoint provenance, raw unrounded tables and independent execution remain open.

**Source and location**

Evidence tier: Recovered primary hal manuscript and page level assessment; selected source reading, not experimental reproduction or independent silicon validation. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://hal.science/hal-05333255/document)

Recovered HAL manuscript, Sections III.B and Figure 2 PDF pages 4–5 for the 32-bit fields, two Hamming codewords and mantissa parity; Table IV PDF page 4 and Section IV.A PDF page 6 for injected F1/F2 settings; Table VIII PDF page 8 for FP32/SERA/F2E4 accuracy; Section IV.C and Table IX PDF pages 8–9 for synthesis conditions, delay and energy accounting; saved assessment iccad/data/sera-float-primary-recovery-v1.json records page numbering, hash and unresolved issues.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_primary_full_text

**Baselines:** FP32 multiplication hardware baseline

FP32 application-quality reference; FP16, BF16, FP8 and INT8 format comparisons, with FP8 configuration labeling unresolved

**Evidence locators:** **Fields:** problem

method_or_artifact

limits

**Location:** Section III.B and Figure 2, PDF pages 4–5 including HAL cover

**Fields:** workload_or_benchmark

hardware_or_process_assumptions

baselines

limits

**Location:** Table IV PDF page 4; Sections IV.A–C PDF pages 6–9; visually checked Tables VIII and IX PDF pages 8–9; iccad/data/sera-float-primary-recovery-v1.json preserves values and hash

**Evidence url:** https://hal.science/hal-05333255/document

**Hardware or process assumptions:** Verilog synthesis with Synopsys Design Compiler and NanGate 45nm library at 1.10 V and 25 C; stated 1 ns constraint is not demonstrated timing closure. No measured silicon.

**Limits:** Two exponent flips are corrected only across separate protected halves; mantissa parity detects rather than corrects. Stored word remains 32 bits. Accuracy degrades under faults. Headline metrics withheld pending unrounded energy/per-module accounting, injection and evaluation provenance, and independent review. Synthesized per-multiplication energy is not full-inference energy.

**Method or artifact:** 32-bit approximate floating-point format reallocating mantissa bits to protected exponent/control fields, eight-bit compressed mantissa, parity and number-type identifiers.

**Metrics:** Not established in the captured evidence.

**Problem:** Approximation error and storage bit flips jointly threaten floating-point accuracy and exception behavior.

**Workload or benchmark:** Image sharpening, Gaussian smoothing, KNN, ResNet-50 DNN and linear SVM; CIFAR-100 stated for classification; modeled single-bit and spatial double-bit storage faults.

</details>

#### Additional source assessment

This separately recorded check is dated 2026-09-06. It supplements the original record above and retains its own scope and uncertainty.

[Assessment record](../../iccad/data/sera-float-primary-recovery-v1.json)

[Assessed source](https://hal.science/hal-05333255/document)

**Extraction scope**

HAL manuscript PDF pages 4–9: format, split-code correction condition, injected faults, applications and synthesized hardware; Tables VIII and IX visually checked. Not experimental reproduction.

**Conditions**

**Format:** **Storage bits:** 32

**Exponent encoded bits:** 14

**Control bits:** 7

**Mantissa bits:** 8

**Identifier bits:** 2

**Mantissa parity bits:** 1

**Locator:** Section III.B, PDF pages 4–5

**Limit:** Mantissa compression frees protection bits inside a 32-bit representation; not a reduction of stored word width below FP32.

**Correction:** **Exponent code:** Two separate (7,4) Hamming codewords

**Two bit condition:** One flip in each protected half; arbitrary two flips in one codeword are not covered by the stated correction guarantee.

**Mantissa:** Single-bit parity detection, not mantissa error correction

**Locator:** Section III.B and Figure 2, PDF pages 4–5

**Faults:** **Single bit percent:** 1

2

3

4

**Additional spatial double bit percent:** 0.02

0.04

0.06

0.08

**Scope:** F1 single-bit events; F2 adds spatial double-bit events. Section IV.A injects storage faults at any location across the representation.

**Locator:** Table IV PDF page 4; Section IV.A PDF page 6

**Limit:** Injected model; not a measured device fault distribution or proof for arbitrary spatial/temporal faults. Equal injection percentages do not by themselves establish equal physical failure exposure across word widths.

**Dnn:** **Model:** ResNet-50

**Dataset as stated:** CIFAR-100

**Locator:** Section IV.B and Table VIII, PDF page 8

**Accuracy percent:** **Fp32 baseline:** 98.85

**Sera no fault:** 97.9

**Sera f2e4:** 88.05

**Fp16 f2e4:** 72.9

**Bf16 f2e4:** 57.68

**Calculated no fault loss percentage points:** 0.95

**Calculated f2e4 loss from sera no fault percentage points:** 9.85

**Limit:** Author-reported accuracy, not reproduced; held-out split, training/checkpoint provenance and injection implementation require verification. Text's 0.9% loss does not specify the percentage-point convention.

**Hardware:** **Locator:** Section IV.C PDF pages 8–9; Figure 4(c) PDF page 6; Table IX PDF page 9

**Evidence type:** Verilog synthesis, not measured silicon

**Tool:** Synopsys Design Compiler

**Library:** NanGate 45nm Open Cell Library

**Clock constraint ns:** 1.0

**Voltage v:** 1.1

**Temperature c:** 25.0

**Baseline:** Conventional FP32 multiplier

**Candidate:** Multiplication framework enabled by SERA-Float conversion, Figure 4(c)

**Table ix:** **Baseline:** **Area um2:** 7690

**Power mw:** 0.15

**Delay ns:** 3.6

**Energy pj:** 0.54

**Sera:** **Area um2:** 7386

**Power mw:** 0.09

**Delay ns:** 1.18

**Energy pj:** 0.1

**Calculated saving from displayed energy percent:** 81.48

**Calculated saving from displayed power times delay percent:** 80.33

**Limit:** Headline 80.3% is consistent with displayed power-times-delay arithmetic, not the rounded energy-column ratio. Unrounded values and per-module conversion/inverse/ECC accounting are not established. Reported delays exceed the stated 1 ns synthesis constraint; do not infer timing closure or 1 GHz throughput. No system-memory or whole-inference energy result.

**Headline metric status**

withheld_pending_accounting_and_independent_review

**Independent review status**

pending

## What remains to establish

Resolve unspecified workloads, comparison methods, resource budgets, and source locations before generalizing a reported gain. This subject is represented by one paper and supports a case study, not evidence of recurrence or a long-term trend.

[All subthemes](../expanded-taxonomy-v1.md) · [Research directions](../directions/README.md)
