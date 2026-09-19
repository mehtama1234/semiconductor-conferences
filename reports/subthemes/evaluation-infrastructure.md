# Evaluation infrastructure

This article groups several related subjects to explain a shared design question.

## The problem

A number is not meaningful unless the task, input set, correctness rule, time limit, and comparison are known.

## What changes in the design

The papers improve benchmarks, test systems, emulators, proof procedures, artifacts, or measurement rules.

## How to establish an improvement

The useful test makes the evaluation repeatable and shows what was tested, what was not tested, and how much the evaluation cost.

## Correctness needs an explicit statement

A design is correct relative to a requirement. The requirement can describe an output, a sequence of states, a timing limit, or information that must remain private. Verification checks whether a design satisfies those statements. Validation asks whether those statements and the design meet the intended use. The two questions can require different experiments.

## Why testing does not cover every behavior

A circuit can have many input combinations and internal states. Simulation tries selected executions and compares their behavior with an expected result. A test that never reaches a faulty state cannot expose that fault. Formal verification reasons about a specified set of behaviors, but its conclusion depends on the model, assumptions, and the property being proved. A timeout is an unresolved check.

## What separates the subthemes

Simulation methods accelerate execution of a model. Emulation implements a representation of the design on other hardware to run tests. Formal methods search for violations or prove properties. Test-generation methods choose inputs likely to expose errors. Coverage measures describe which behaviors were exercised; they need a definition to be interpretable.

## A comparison that answers the question

Use known faults or independently established reference behavior to assess detection. State the design sizes, properties, test budget, unresolved checks, false alarms, and missed faults. When a generated test improves a score, examine whether it finds new errors on designs outside the development set. More tests are useful only to the extent that they improve the relevant coverage or detection.

## The individual subjects

The grouping contains 31 selected records. Read its individual subjects below; their boundaries can overlap.

- [Reproducibility artifacts and benchmarks](../observed-subthemes/reproducibility-artifacts-and-benchmarks.md)
- [Simulation emulation and testing](../observed-subthemes/simulation-emulation-and-testing.md)
- [Formal and functional verification](../observed-subthemes/formal-and-functional-verification.md)
- [Hardware security validation](../observed-subthemes/hardware-security-validation.md)

## Technical cards

Evidence tier and exact source locations are provided in each linked article. The article preserves full recorded text, including limits and baselines.

- [Lyra: A Hardware-Accelerated RISC-V Verification Framework with Generative Model-Based Processor Fuzzing](../observed-subthemes/simulation-emulation-and-testing.md#paper-dac-2026-research358)
- [STELLAR: Structure-Guided LLM Assertion Retrieval and Generation for Formal Verification](../observed-subthemes/formal-and-functional-verification.md#paper-dac-2026-research3200)
- [Uvmarvel: an Automated LLM-Aided UVM Machine for Subsystem-Level RTL Verification](../observed-subthemes/simulation-emulation-and-testing.md#paper-dac-2026-research2880)
- [Automated Discovery, Classification, and Systematic Security Verification Methodology for Undocumented Instructions](../observed-subthemes/hardware-security-validation.md#paper-dac-2026-research2804)
- [HLSDebugger: Identification and Correction of Logic Bugs in HLS Code with LLM Solutions](../observed-subthemes/simulation-emulation-and-testing.md#paper-iccad-2025-1027)
- [RIROS: A Parallel RTL Fault SImulation FRamework with TwO-Dimensional Parallelism and Unified Schedule](../observed-subthemes/simulation-emulation-and-testing.md#paper-iccad-2025-114)
- [Software-Style Hardware Debugging: A Hardware Generation, Simulation and Debugging Framework](../observed-subthemes/simulation-emulation-and-testing.md#paper-iccad-2025-1137)
- [Uncertainty-Guided Live Measurement Sequencing for Fast SAR ADC Linearity Testing](../observed-subthemes/simulation-emulation-and-testing.md#paper-iccad-2025-1117)
- [Notsotiny: A Large, Living Benchmark for RTL Code Generation](../observed-subthemes/simulation-emulation-and-testing.md#paper-dac-2026-research2760)
- [Vten: Tensor-Centric Verification Framework for Domain-Specific Accelerators](../observed-subthemes/simulation-emulation-and-testing.md#paper-dac-2026-research2348)

## Limits and next evidence

This is a cross-cutting grouping within the selected sample. Its count measures the records included by the grouping rule. Comparing methods requires the same workload, answer quality, hardware limits, and total evaluation budget. Open the individual records before treating a shared subject as a common result.

[Research directions](../directions/README.md) · [Complete subtheme index](../expanded-taxonomy-v1.md)
