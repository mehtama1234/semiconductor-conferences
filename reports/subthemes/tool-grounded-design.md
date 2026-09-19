# Tool-grounded design and verification

This article groups several related subjects to explain a shared design question.

## The problem

Design tools can generate code or layouts that look plausible but do not work. The central problem is deciding validity before expensive implementation.

## What changes in the design

The papers connect generated choices to synthesis, simulation, formal checking, or measured design limits.

## How to establish an improvement

The useful test reports how many proposals were tried, how many failed, what checked them, and whether the final design improved against a fixed baseline.

## What designing a chip requires

A designer specifies what a circuit must do and which limits it must satisfy. Electronic design automation, abbreviated EDA, is software that helps turn that specification into a circuit and a physical layout. There are many choices: how to represent the logic, which circuit elements to use, where to place them, and how to connect them. Each choice can affect correctness, area, timing, and power.

## Where a learned model enters

A learned model uses patterns in previous examples or evaluations to suggest a new choice. A language model may generate hardware-description code or modify a design program. Another model may predict which candidate is worth an expensive evaluation. These are different jobs. Generating code does not show that the code implements the specification; predicting a favorable timing score does not show that the implemented circuit meets timing.

## Why the checking procedure matters

Synthesis converts a behavioral or logical description into circuit elements. Simulation executes a model on selected inputs. Formal verification checks a stated property mathematically within a defined model. Each check answers a different question. The design method needs to record which check rejected a candidate, what information was returned, and how that information changed the next attempt. A weak test can accept an incorrect design and make the search appear successful.

## A comparison that answers the question

Give competing methods the same design tasks and account for the complete time and computing budget, including model calls, training, checking, and retries. Report valid completed designs and their measured quality. Test new circuits that were not used to tune the method. The long-term question is whether better choices can be made with less total engineering and evaluation effort while preserving correctness.

## The individual subjects

The grouping contains 37 selected records. Read its individual subjects below; their boundaries can overlap.

- [LLM assisted design flows](../observed-subthemes/llm-assisted-design-flows.md)
- [High level synthesis and compilers](../observed-subthemes/high-level-synthesis-and-compilers.md)
- [Simulation emulation and testing](../observed-subthemes/simulation-emulation-and-testing.md)
- [Formal and functional verification](../observed-subthemes/formal-and-functional-verification.md)

## Technical cards

Evidence tier and exact source locations are provided in each linked article. The article preserves full recorded text, including limits and baselines.

- [CODO: An Automated Compiler for Comprehensive Dataflow Optimization](../observed-subthemes/high-level-synthesis-and-compilers.md#paper-isca-2026-program-002)
- [Paretopilot: Global Optimization Reasoning on HLS Design Space Exploration with LLMs](../observed-subthemes/llm-assisted-design-flows.md#paper-dac-2026-research865)
- [Mappingevolve: LLM-Driven Code Evolution for Technology Mapping](../observed-subthemes/llm-assisted-design-flows.md#paper-dac-2026-research535)
- [Lyra: A Hardware-Accelerated RISC-V Verification Framework with Generative Model-Based Processor Fuzzing](../observed-subthemes/simulation-emulation-and-testing.md#paper-dac-2026-research358)
- [STELLAR: Structure-Guided LLM Assertion Retrieval and Generation for Formal Verification](../observed-subthemes/formal-and-functional-verification.md#paper-dac-2026-research3200)
- [VeriOpt: PPA-Aware High-Quality Verilog Generation via Multi-Role LLMs](../observed-subthemes/llm-assisted-design-flows.md#paper-iccad-2025-1222)
- [VERIRL: Boosting the LLM-based Verilog Code Generation via Reinforcement Learning](../observed-subthemes/llm-assisted-design-flows.md#paper-iccad-2025-110)
- [HLSDebugger: Identification and Correction of Logic Bugs in HLS Code with LLM Solutions](../observed-subthemes/simulation-emulation-and-testing.md#paper-iccad-2025-1027)
- [RIROS: A Parallel RTL Fault SImulation FRamework with TwO-Dimensional Parallelism and Unified Schedule](../observed-subthemes/simulation-emulation-and-testing.md#paper-iccad-2025-114)
- [Uvmarvel: an Automated LLM-Aided UVM Machine for Subsystem-Level RTL Verification](../observed-subthemes/simulation-emulation-and-testing.md#paper-dac-2026-research2880)

## Limits and next evidence

This is a cross-cutting grouping within the selected sample. Its count measures the records included by the grouping rule. Comparing methods requires the same workload, answer quality, hardware limits, and total evaluation budget. Open the individual records before treating a shared subject as a common result.

[Research directions](../directions/README.md) · [Complete subtheme index](../expanded-taxonomy-v1.md)
