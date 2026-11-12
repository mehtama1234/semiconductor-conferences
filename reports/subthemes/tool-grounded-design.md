# Tool-grounded design and verification

This article groups several related subjects to explain a shared design question.

## The problem

Design tools can generate code or layouts that look plausible but do not work. The central problem is deciding validity before expensive implementation.

## What changes in the design

The papers connect generated choices to synthesis, simulation, formal checking, or measured design limits.

## How to establish an improvement

The useful test reports how many proposals were tried, how many failed, what checked them, and whether the final design improved against a fixed baseline.

## Chip design is a long chain of choices that software helps make

A designer states what a circuit must do and which limits it must meet. **Electronic design automation (EDA)** is the software that turns that statement into a circuit and then a physical layout.

There are many choices along the way:

1. how to represent the logic;
2. which circuit elements to use;
3. where to place them;
4. how to connect them.

Each choice can affect correctness, area, timing and power.

## A learned model can propose or predict, and these are different jobs

A learned model uses patterns in past examples or evaluations to suggest a new choice.

- A **language model** may write hardware-description code, or change a design program.
- A **predictor** may guess which candidate is worth an expensive evaluation.

Writing code does not show that the code meets the specification. Predicting a good timing score does not show that the built circuit meets timing.

## Each check answers a different question, so record which one failed

- **Synthesis** turns a behavioral or logical description into circuit elements.
- **Simulation** runs a model on selected inputs.
- **Formal verification** checks a stated property mathematically, within a defined model.

A design method should record which check rejected a candidate, what it reported, and how that changed the next attempt. A weak test can accept a wrong design and make the search look successful.

## A fair test counts every model call, check and retry

1. Give competing methods the same design tasks.
2. Count the whole time and computing budget: model calls, training, checking and retries.
3. Report valid completed designs and their measured quality.
4. Test on new circuits that were not used to tune the method.

The long-term question: can better choices be made with less total engineering and evaluation effort, while keeping the design correct?

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
