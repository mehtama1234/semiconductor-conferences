# Reliable and efficient compute

This subject has 1 record in the selected sample. This page explains where it fits, then presents all captured paper evidence without shortening the measurements or limitations.

[Definitions used in the paper records](../reading-guide-v1.md)

## Understand the parent subject first

- [Power reliability and security](../themes/power-reliability-and-security.md)

## Lower voltage changes when a result becomes valid

A multiply-accumulate unit computes a product and adds it to a running sum. Neural-network accelerators repeat this operation across many processing elements. Reducing their supply voltage can reduce switching power, but it generally makes transistor transitions slower. If the clock captures a result before the required signals have settled, the captured value can be wrong even though the Boolean circuit is logically correct.

The critical path is the path whose delay limits the time available between relevant clock events. Its practical behavior depends on input transitions as well as the implemented gates and wires. A design that works for many values at low voltage may still fail for another transition pattern. Average delay is therefore not a guarantee that every operation meets timing.

This subject contains one paper on adaptive arithmetic width. Its reliability concern is timing under reduced voltage, not all hardware faults. It does not, by its title or taxonomy label, establish protection against permanent defects, memory corruption, malicious inputs, or aging.

## Shortening active arithmetic is different from lowering numerical precision

In signed binary arithmetic, a small-magnitude value can have repeated high-order sign bits. If the result can be represented using fewer active arithmetic stages, those upper positions may be reconstructed from the sign instead of waiting for a long propagation through every stage. This is a range-preservation problem, not necessarily a decision to discard meaningful low-order bits.

For example, a signed value representable in eight bits can also be represented in a wider signed word by repeating its sign bit in the added positions. Removing redundant sign-extension work can preserve the value. Removing a bit needed to represent its magnitude cannot. A valid adaptive design must determine which case applies before its output is used.

The control circuit is part of the timing problem too. Detecting the required width, selecting a result, and reconstructing the upper bits consume time and power. A shorter adder path is useful only if the complete controlled path meets the intended clock requirement.

<span id="explanation-dac-2026-research2364"></span>

## What ADA and ADA-Plus demonstrate

The complete controlled critical path includes width detection, result selection and upper-bit reconstruction; shortening the arithmetic portion alone does not establish timing correctness.

[Adaptive Multiply-Accumulate Unit with Scalable Critical Path](../observed-subthemes/reliable-and-efficient-compute.md#paper-dac-2026-research2364) introduces ADA's input-dependent width selection and ADA-Plus's output-stationary state-based control. Sections 3–4, PDF pages 3–6, use signed 8-bit multiplication and 24-bit accumulation, 28-nm synthesis, and circuit/timing simulation—not measured silicon. ADA/ADA-Plus add 16.1%/12.4% area.

Section 4.2, pages 5–6, uses an eight-image MNIST workload for circuit-level power evaluation; the separate 1-GHz CNN accuracy evaluation uses 1,000 CIFAR-10 images. Table 1 defines minimum voltage by less than 1% accuracy loss, not zero timing errors. Figure 11 reports 50.89% lower power for ADA output-stationary operation versus nominal-voltage baseline, but 19.35% versus the original design at its minimum effective voltage.

Section 3.2, page 4, assumes unchanged partial-sum sign in higher control modes and inconsistently refers to mode 4 after describing four modes. These assumptions and numbering need reconciliation before claiming unrestricted arithmetic correctness. [Manuscript, Sections 3–4, Table 1 and Figure 11](https://www.ece.ualberta.ca/~jhan8/publications/2364_Camera_Ready_Paper.pdf).

The captured evidence supports adaptive underscaled MAC operation with simulation-level power and application-accuracy claims, not demonstrated reliable end-to-end DNN quality across process and workload conditions.

Output-stationary execution retains a partial sum in the same processing element between successive operations. That can make the previous sum useful when deciding how to handle the next operation. A scheme relying on that continuity cannot automatically be applied unchanged when unrelated sums arrive from elsewhere. The supported dataflow is part of the correctness boundary.

## Three different meanings of “no loss”

Bit-exact arithmetic means every supported operation produces the intended numerical value. Timing correctness means the relevant value arrives in time for capture under stated physical conditions. Unchanged classification accuracy means the aggregate task score matches a reference on an evaluated dataset. These claims are not interchangeable.

Two systems can obtain the same number of correct classifications while disagreeing on individual examples. Internal numerical errors can also occur without changing the final selected class. Conversely, a bit-exact arithmetic transformation can still suffer physical timing failures if operated outside its validated conditions.

For this reason, an application-accuracy result should not be promoted to a guarantee of zero timing errors. A stronger assessment would separately report arithmetic mismatches, late arrivals, per-example prediction agreement, and task accuracy, including rare input transitions that are not well represented by average workload statistics.

## Power savings depend on the comparison point

Power is energy consumed per unit time. Energy per inference also depends on how long the inference takes and which components are counted. When frequency, work, and execution duration are fixed, a power reduction can translate into reduced energy for that same boundary. It does not establish the same percentage at the system boundary if memory, control, or voltage-regulation costs remain unchanged.

An unmodified design operated at nominal voltage and the same design operated at a lower acceptable voltage are different baselines. Comparing against the first measures the combined benefit of voltage reduction and the new circuit. Comparing against the second more directly asks what the added circuit enables beyond voltage scaling already available to the original implementation.

Neither comparison is inherently invalid. Both must state their voltage, clock, accuracy criterion, and included components. A large headline should not erase the smaller but more demanding comparison.

## What still needs verification

Process, voltage, and temperature conditions affect delay. Simulated corners sample specified device models; they do not by themselves establish the behavior of every manufactured device or every transient voltage disturbance. A complete reliability assessment should test control transitions, large positive-to-negative changes, overflow boundaries, and reset behavior under the intended operating envelope.

The wider conceptual insight is that data-dependent arithmetic structure can change how far voltage can be reduced while preserving a stated workload result. This is a mechanism-level inference, not a long-term adoption trend or a universal voltage policy for neural accelerators.

The manuscript was recovered on 2026-09-07 and supersedes the historical card's missing-result statements. Physical validation, the control-assumption audit, broader workload coverage, and independent reproduction remain open. The article's readable format and passing link checks are not evidence that those scientific checks are complete.

## Compare the results carefully

First identify the inputs and required output quality. Then identify the limited resource: time, memory, communication, energy, circuit area, or correctness coverage. Ask which part of the method reduces that cost and which new cost it adds. Compare numbers only when the experiments hold these conditions sufficiently similar.

A conference description may explain the proposal while omitting the full experiment. An author preprint link may have been coded from its abstract. The source classification does not by itself establish that every table was read. Missing locations remain visible below.

## Complete captured evidence

These are evidence records, not substitutes for the explanations above. Each record preserves its problem, proposed method, measurements, comparison conditions, and source limits. A populated record does not establish that its mechanism has been fully explained or independently verified.

<span id="paper-dac-2026-research2364"></span>

### Adaptive Multiply-Accumulate Unit with Scalable Critical Path for Aggressive Voltage Underscaling DNN Accelerators

DAC 2026 · Record: `dac-2026-research2364`

[Read the step-by-step explanation](#explanation-dac-2026-research2364)

**Updated source-backed reading card**

Reviewed 2026-09-09. Reconciles the recovered manuscript with the sparse official card; separates adaptive arithmetic-width control from numerical precision, timing correctness, application accuracy and silicon validation, and preserves the reported area, voltage and power claims with their stated comparison boundaries.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Aggressive supply-voltage underscaling can reduce MAC switching power but lengthen data-dependent paths and cause late or incorrect results in DNN accelerators.

**Mechanism / artifact:**

ADA is an adaptive MAC with input-dependent width selection and sign reconstruction; ADA-Plus adds state-based control for output-stationary systolic arrays. The design uses signed 8-bit multiplication and 24-bit accumulation, with a scalable active critical path; control detection, selection and reconstruction remain part of the timing and power path.

**Workload — the work tested:**

Circuit-level evaluation uses the stated signed MAC configuration, an eight-image MNIST workload for power evaluation, and a separate 1-GHz CNN accuracy evaluation on 1,000 CIFAR-10 images; model, layer coverage, voltage sweep, process corners, transition coverage and statistical treatment are limited or unspecified.

**Hardware and manufacturing assumptions:**

28-nm synthesized digital MACs and output-stationary systolic-array operation evaluated with circuit/timing simulation rather than measured silicon; voltage, frequency, process-voltage-temperature corners, clocking, implementation tools, variation, supply noise and measurement boundary are not fully specified.

**Baseline — the comparison method:**

Nominal-voltage MAC

Original/fixed-critical-path MAC at its minimum effective voltage

ADA versus ADA-Plus under the same signed arithmetic, clock, voltage, workload, synthesis and power boundary

The exact voltage, clock, accuracy criterion, components, seeds, corners and end-to-end inference boundary for each comparison are incompletely specified

**Reported measurements:**

ADA and ADA-Plus add 16.1% and 12.4% area respectively; the source defines minimum voltage using less than 1% accuracy loss, reports 50.89% lower power for ADA output-stationary operation versus a nominal-voltage baseline and 19.35% versus the original design at its minimum effective voltage; the source does not establish zero timing errors, fabricated-silicon behavior, full-system energy or broad workload accuracy.

**Limits on the conclusion:**

Shortening redundant sign-extension or active arithmetic width is not the same as discarding numerical precision. Validate bit-exact arithmetic, overflow and sign transitions, then separately measure late captures and timing-error rate across input patterns; a task-level accuracy result cannot substitute for either check.

The control path that detects width, selects the result and reconstructs upper bits consumes delay and power. Process, voltage and temperature variation, supply noise, clock assumptions, reset behavior and the output-stationary partial-sum assumption must be tested; the recovered manuscript also requires reconciliation of its higher-mode sign assumption and mode numbering before claiming unrestricted correctness.

The reported less-than-1% accuracy criterion, 50.89% and 19.35% power comparisons, and area overheads are simulation-level claims with distinct baselines. Include frequency and execution time, control and voltage-regulator costs, energy per inference, timing failures, PVT corners, workload and layer distributions, and silicon or fault-injection evidence. The evidence supports adaptive underscaled MAC operation, not demonstrated reliable end-to-end DNN quality across process and workload conditions.

**Source and location**

Evidence tier: Primary recovered manuscript plus captured official DAC description; circuit/timing simulation and synthesis evidence, not independent silicon reproduction or complete pvt/workload validation. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://www.ece.ualberta.ca/~jhan8/publications/2364_Camera_Ready_Paper.pdf)

Recovered manuscript, Sections 3–4, PDF pages 3–6; Table 1; Figure 11; existing reliable-and-efficient-compute editorial explanation; official DAC description retained in the original card.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** nominal-voltage MAC

fixed critical-path MAC

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH2364

**Hardware or process assumptions:** Near-threshold or underscaled digital accelerator; timing and variation assumptions are unspecified.

**Limits:** No voltage, timing-error rate, accuracy, energy, area, or silicon results are reported.

Error behavior depends on process and workload.

Official description only; silicon and fault-injection validation is required.

**Method or artifact:** Adaptive MAC with scalable critical path for underscaled operation.

**Metrics:** Voltage-scaled energy efficiency is claimed qualitatively

**Problem:** Aggressive voltage underscaling saves energy but increases timing errors in DNN MACs.

**Workload or benchmark:** DNN MAC workloads; models, voltage range, error policy, and process are unspecified.

</details>

## What remains to establish

Resolve unspecified workloads, comparison methods, resource budgets, and source locations before generalizing a reported gain. This subject is represented by one paper and supports a case study, not evidence of recurrence or a long-term trend.

[All subthemes](../expanded-taxonomy-v1.md) · [Research directions](../directions/README.md)
