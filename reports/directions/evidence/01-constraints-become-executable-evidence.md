# Evidence dossier — Constraints Become Executable

This dossier combines the canonical direction atlas, historical adjudicated records, and dated editorial corrections. It is a source-backed reading aid, not an independent review or a claim that the records are comparable.

- Direction page: [Constraints Become Executable](../01-constraints-become-executable.md)
- Source direction IDs: `tool-grounded-ai-design-verification`
- Direction status: `provisional_mechanism_hypothesis`
- Independent reviews recorded: `0`

## Reading rule

`UNKNOWN` means a field is not recorded, not that the paper lacks the condition. Corrections supersede the current displayed fields while historical fields remain expandable. A historical condition-complete label does not establish that a correction has passed condition or independent review.

## LLM-Based Automatic Architecture Optimization for AI Model HLS Implementation on FPGA

- Paper ID: `dac-2026-research1110`
- Conference/edition: `dac` / `2026`
- Evidence tier: `Primary captured official DAC description plus author-linked partial artifact assessment and existing authored explanation; full paper and complete optimization framework not recovered, no execution, post-route timing, board run or independent functional validation`
- Ledger record: `dac/data/adjudicated-2026-batch.jsonl`

**Current evidence correction — 2026-09-09**

Deepens the LLM-based FPGA HLS architecture treatment into a paper-level reading; separates generated modular dataflow architectures and pattern optimization from functional correctness, HLS/post-route closure, resource fit, model-level throughput and prompt/search cost, while preserving the official 11.78x claim and the partial Fire-module artifact boundary.

Condition review of this correction and independent acceptance remain pending. The direction mapping is inherited, not revalidated by this update.

[Dated correction register](../../../data/editorial-paper-corrections-v1.json)

- Source: [https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH1110](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH1110)

| Field | Current record |
|---|---|
| Problem | AI-model HLS implementation requires coordinated module partitioning, dataflow orchestration and throughput optimization, while compiler and LLM approaches may not jointly optimize the system architecture. |
| Mechanism / artifact | LLM-based generation and optimization of modular dataflow HLS architectures with pattern-based transformations and synthesizable FPGA output; model identity, prompts, retries, architecture representation, legality checks, feedback loop and lowering flow are unspecified. |
| Workload / benchmark | AI model implementations through HLS on FPGA; model suite, kernels, tensor shapes, precision, dataflow partition, baseline designs, accuracy tolerance, device split and aggregation behind the average claim are unspecified. A pinned partial Fire-module artifact uses Vivado HLS/Vivado 2019.2, ZCU102 and a 100 MHz target, but does not establish the paper benchmark suite. |
| Hardware / process | FPGA dataflow architectures with connected streaming stages, buffering and HLS-generated hardware; device/resource budget, clock, memory/interconnect, place-and-route, post-route timing, board execution, power and full-model integration are unspecified. The inspected artifact reports stored HLS estimates only and no executed simulation or co-simulation. |
| Baselines | Current state-of-the-art compiler-based HLS approaches; Current LLM-assisted HLS approaches; Same AI models, source kernels, precision, accuracy, FPGA device, clock/resource constraints, backend versions, optimization budget, correctness checks and end-to-end boundary are unspecified |
| Metrics | The official description reports an average 11.78x performance improvement over current state-of-the-art approaches, but does not define the performance quantity or aggregation, benchmark/model distribution, resource tradeoff, synthesis success rate, compile/LLM cost, post-route timing, board measurement or model-quality result. The selected Fire artifact assessment records 335,494-cycle top-level latency, 229,703-cycle interval, estimated 8.419 ns clock and resource totals, but these are stored HLS estimates for a partial example, not a reproduction of 11.78x or end-to-end model performance. |
| Evidence locator / span | DAC 2026 official description, first and final paragraphs; pinned HLSArchOpt artifact assessment at commit 999043ab132f984b5b88b26ab9e415221e1198f1; README, Fire top-level kernel, HLS script and stored synthesis reports; existing LLM-assisted-design-flows explanation; no full manuscript or executed reproduction. |
| Limits | Generated dataflow stages must preserve values, tensor order, stream progress, backpressure, deadlock freedom, numerical tolerance and end-of-output behavior. Check generated designs against a trusted software/reference implementation and exercise empty, boundary, variable-rate, reset, branching and concatenation cases; synthesizability alone is not functional equivalence.; HLS estimates and requested clock periods are not post-route timing or board execution. Report initiation interval versus top-level latency, resource use, buffering, frequency, timing closure, power, host/device transfers, full-model integration and accuracy on named FPGA devices; include failed synthesis, place-and-route, simulation and manual repair costs.; The official description supports LLM-assisted modular HLS architecture generation and reports an average 11.78x claim, while the pinned artifact is a partial Fire-module release with Vivado 2019.2/ZCU102 conditions and future full integration. The evidence does not establish production-ready FPGA acceleration or a reproducible end-to-end 11.78x gain because prompts/search cost, benchmark aggregation, matched baselines, correctness, post-route/board evidence and resource/quality constraints remain unresolved. |

<details markdown="1">
<summary>Historical captured record — superseded in the current table</summary>

Historical atlas evidence tier: `official_description`.

| Field | Historical record |
|---|---|
| problem | AI-model HLS still requires substantial manual work for module partitioning, dataflow orchestration, and throughput optimization. |
| mechanism | LLM-based generation and optimization of modular dataflow HLS architectures with synthesizable FPGA output. |
| workload | AI model implementations through high-level synthesis on FPGA. |
| hardware | UNKNOWN — not present in the current adjudicated record |
| baselines | current state-of-the-art compiler-based and LLM-assisted HLS approaches |
| metrics | 11.78X average performance improvement |
| limits | The description does not expose model prompts, synthesis success rate, FPGA devices, benchmark models, resource costs, or quality constraints. |
| locator | The LLM-powered framework generates modular dataflow architectures, applies pattern-based optimization, and produces synthesizable FPGA hardware, reporting an average 11.78X performance improvement over current state-of-the-art approaches. |

[Historical source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH1110&sess=sess156)

</details>


Mapping review status: `researcher_reconciliation_not_independent`; independent review status: `pending`.

## Paretopilot: Global Optimization Reasoning on HLS Design Space Exploration with LLMs

- Paper ID: `dac-2026-research865`
- Conference/edition: `dac` / `2026`
- Evidence tier: `Official description and selected pinned artifact inspection; manuscript and reproduction missing`
- Ledger record: `dac/data/adjudicated-2026-batch-2.jsonl`

**Current evidence correction — 2026-09-08**

Reconciles current reading with saved pinned-artifact assessment and reread entry point; headline definitions remain unverified.

Condition review of this correction and independent acceptance remain pending. The direction mapping is inherited, not revalidated by this update.

[Dated correction register](../../../data/editorial-paper-corrections-v1.json)

- Source: [https://github.com/GEAR-SEU/ParetoPilot-DAC-26/blob/d08173f66903ed466537c9327b63addac223ee95/src/DSE_LLM.py](https://github.com/GEAR-SEU/ParetoPilot-DAC-26/blob/d08173f66903ed466537c9327b63addac223ee95/src/DSE_LLM.py)

| Field | Current record |
|---|---|
| Problem | Selecting useful HLS directive configurations under limited evaluation budgets. |
| Mechanism / artifact | LLM-guided HLS directive exploration. Pinned perform_dse samples once before evaluating configurations; no measured-result resampling in that function. |
| Workload / benchmark | HLS design-space exploration; release contains benchmark configurations, but correspondence to headline program population and budgets is unresolved. |
| Hardware / process | Selected artifact assessment records AES FPGA synthesis example and report-derived latency/resource fractions; not verified headline platform or measured board results. |
| Baselines | Unnamed state-of-the-art heuristic search and an auxiliary DeepSeek-R1 configuration; matched conditions unavailable. |
| Metrics | Description reports 49.5% DSE performance, 1.8× efficiency and 81.4% versus auxiliary DeepSeek-R1; definitions and experiment correspondence unresolved, not circuit speedup or physical area claims. |
| Evidence locator / span | DSEWorkflow.perform_dse reread 2026-09-08; supplementary assessment dated 2026-09-06 records other selected artifact inspection. Official Description supplies unresolved headlines. |
| Limits | No manuscript or execution. Artifact self-identification is not full experiment validation. Missing measurements use 1e8 sentinels; raw-report preservation, functional checks, budgets, training overlap and headline definitions remain open. |

<details markdown="1">
<summary>Historical captured record — superseded in the current table</summary>

Historical atlas evidence tier: `official_description`.

| Field | Historical record |
|---|---|
| problem | The combinatorial explosion of HLS directives makes it difficult for heuristic search to find Pareto-optimal designs under tight budgets. |
| mechanism | LLM-guided HLS design-space exploration using global optimization reasoning, directive scheduling, and quality-aware Pareto-front shaping. |
| workload | HLS directive/configuration design spaces evaluated by Pareto-front quality and search efficiency. |
| hardware | UNKNOWN — not present in the current adjudicated record |
| baselines | state-of-the-art heuristic HLS DSE; DeepSeek-R1 auxiliary LLM |
| metrics | 49.5% DSE-performance improvement; 1.8x search efficiency; 81.4% improvement over DeepSeek-R1; Pareto-front quality |
| limits | The description does not disclose prompt/interface design, model size, benchmark suite, search budget, or how Pareto quality is measured; LLM claims require paper-level reproducibility review. |
| locator | ParetoPilot uses a dedicated LLM to navigate combinatorial HLS directive spaces with global-optimization reasoning, directive scheduling, and quality awareness. It reports 49.5% better DSE performance and 1.8x efficiency over a state-of-the-art heuristic method, and 81.4% improvement over DeepSeek-R1. |

[Historical source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH865&sess=sess168)

</details>


Mapping review status: `researcher_reconciliation_not_independent`; independent review status: `pending`.

## Mappingevolve: LLM-Driven Code Evolution for Technology Mapping

- Paper ID: `dac-2026-research535`
- Conference/edition: `dac` / `2026`
- Evidence tier: `Primary arXiv preprint v1, PDF table crosscheck, public artifact inspection and official DAC description; no experiment execution or independent acceptance`
- Ledger record: `dac/data/adjudicated-2026-batch-2.jsonl`

**Current evidence correction — 2026-09-08**

Reconciles the official card with arXiv version 1, the PDF Table 2 crosscheck and the pinned artifact assessment; makes the mapping objective, evaluation conditions, tradeoffs, runtime boundary and source-level fallback concern explicit without treating them as independently reproduced results.

Condition review of this correction and independent acceptance remain pending. The direction mapping is inherited, not revalidated by this update.

[Dated correction register](../../../data/editorial-paper-corrections-v1.json)

- Source: [https://arxiv.org/pdf/2604.26591v1](https://arxiv.org/pdf/2604.26591v1)

| Field | Current record |
|---|---|
| Problem | Technology mapping heuristics are hand-designed software, and improving their area/delay tradeoff through LLM-guided code evolution requires preserving output equivalence while controlling search and evaluation cost. |
| Mechanism / artifact | MappingEvolve uses Planner, Evolver and Evaluator roles to propose structured changes to technology-mapping code, compile the candidate mapper, map circuits, check logical equivalence, and score normalized area and delay. The released artifact includes a proactive evolution driver and author-provided run histories. |
| Workload / benchmark | Eleven ISCAS85 circuits form the evolution suite; EPFL circuits after ABC `compress2` and ASAP7 evaluation form the reported evaluation suite. The assessed loop uses 30 outer iterations × 3 inner iterations, compared with 90 direct-evolution iterations. |
| Hardware / process | Selected artifact conditions: Ubuntu 22.04, Xeon Gold 6226R and 256 GB memory; ABC `&nf` and mockturtle `map` are named baselines. Compilation and ABC CEC equivalence precede QoR evaluation; post-route behavior and process/library transfer are not established. |
| Baselines | ABC `&nf`; mockturtle `map`; Direct code-evolution approach; Strong technology-mapping baselines named by the official description |
| Metrics | Table 2 average ratios to ABC: DeepSeek-V3 area 0.8996, delay 1.0571, mapper runtime 1.755; GPT-5 area 0.8996, delay 1.0369, mapper runtime 1.6557.; The assessed objective is 0.5 × normalized area reduction + 0.5 × normalized delay reduction; area reduction therefore can coexist with slower mapped-circuit delay or longer mapper runtime.; The official description reports 10.04% area reduction versus ABC, 7.93% versus mockturtle, and 46.6%–96.0% S_overall improvement; these headline values remain conditioned on source-to-result reconciliation. |
| Evidence locator / span | Version 1: Sections 2–4, especially Sections 3.1, 3.2.3 and 4.1; PDF Table 2 page 6 for average area/delay/mapper-runtime ratios; pinned artifact commit 308f5cc41c1d7243c39fd2ddd02253c1343eb889, `evolve_single/proactive_single_point_evolve.py` lines 107, 378–390, 705–737 and 759–764; official DAC record https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH535&sess=sess172. |
| Limits | Table averages show a tradeoff, not dominance: the visually crosschecked ratios reduce area while increasing average delay and mapper runtime. Composite QoR is not execution speedup.; Equal iteration counts do not establish equal wall-clock time, token/API cost, stochastic search opportunity or total engineering cost. Repeated seeds, dispersion, model versions, held-out protocol and timeout/equivalence-failure handling remain unresolved.; The pinned driver updates `best_state` on reward improvement before acceptance and can restore that state after rejection; this is a source-level control-flow concern, not evidence that a published circuit was invalid. The inspected author logs show no outer-loop reversion in three selected runs, but they are not independently authenticated.; No mapping experiment or repository code was executed here. Equivalence of evaluated netlists does not prove arbitrary future outputs, post-route quality, process transfer or universal mapper improvement. |

<details markdown="1">
<summary>Historical captured record — superseded in the current table</summary>

Historical atlas evidence tier: `official_description`.

| Field | Historical record |
|---|---|
| problem | LLMs have been used to generate optimization scripts, but their ability to improve the core technology-mapping algorithm remains underused. |
| mechanism | Open-source hierarchical agent framework that plans, evolves, and evaluates technology-mapping code through structured optimization operators. |
| workload | Technology-mapping experiments on EPFL benchmark circuits with area-delay tradeoff evaluation. |
| hardware | UNKNOWN — not present in the current adjudicated record |
| baselines | ABC; mockturtle; direct code-evolution approach; strong technology-mapping baselines |
| metrics | 10.04% area reduction versus ABC; 7.93% area reduction versus mockturtle; 46.6%–96.0% S_overall improvement on EPFL benchmarks; area-delay tradeoff |
| limits | The description does not disclose model/API costs, evolution budgets, reproducibility details, benchmark split, or how code validity and regression risk are controlled. |
| locator | MappingEvolve abstracts technology mapping into optimization operators and uses a Planner/Evolver/Evaluator hierarchy to guide LLM-driven code evolution. The official description reports 10.04% area reduction versus ABC, 7.93% versus mockturtle, 46.6%–96.0% S_overall improvement on EPFL benchmarks, explicit area-delay tradeoff navigation, and an open-source framework. |

[Historical source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH535&sess=sess172)

</details>


Mapping review status: `researcher_reconciliation_not_independent`; independent review status: `pending`.

## MAHL: Multi-Agent LLM-Guided Hierarchical Chiplet Design with Adaptive Debugging

- Paper ID: `iccad-2025-1207`
- Conference/edition: `iccad` / `2025`
- Evidence tier: `Primary preprint; selected reading and execution/independent acceptance not performed`
- Ledger record: `iccad/data/adjudicated-2025-batch-2.jsonl`

**Current evidence correction — 2026-09-08**

Deepens the primary-preprint reading; separates hierarchical module contracts, six software workflow roles, RTL/tool validation, Pass@5 budgeting and PPA comparison conditions.

Condition review of this correction and independent acceptance remain pending. The direction mapping is inherited, not revalidated by this update.

[Dated correction register](../../../data/editorial-paper-corrections-v1.json)

- Source: [https://arxiv.org/abs/2508.14053](https://arxiv.org/abs/2508.14053)

| Field | Current record |
|---|---|
| Problem | Flat language-model-driven chiplet design has high validation cost and weak coordination between module generation, integration and physical objectives. |
| Mechanism / artifact | Six-role hierarchical workflow combining AI-to-hardware mapping, structured module descriptions, retrieval-assisted RTL generation, tool-based validation/debugging, multi-granularity design-space exploration and physical-layout configuration. |
| Workload / benchmark | Simple RTL and real-world AI chiplet-design tasks; exact task suite, module/system specifications and held-out designs require the primary paper reading. |
| Hardware / process | 2.5D chiplet designs with AI workloads, RTL generation, synthesis/validation and OpenROAD-like physical configuration; exact chiplet architectures, PPA flow, libraries and design constraints require full-paper review. |
| Baselines | Conventional LLMs; CLARIE expert-based chiplet design framework |
| Metrics | Reported best-case real-world chiplet-design Pass@5 rises from 0 to 0.72; the task population, average/best-case convention and candidate cost require verification.; Comparable or superior PPA to CLARIE is reported under selected objectives; exact denominators and physical-flow conditions are not fully recorded. |
| Evidence locator / span | Primary preprint identity and selected method/evaluation reading; exact page, section and table locators require follow-up. |
| Limits | Pass@5 is success within five candidates, not first-attempt success, equal-cost success or complete design correctness.; Local RTL compilation, functional validation, synthesis, timing, routing and package/system closure answer different questions; the captured record does not establish all gates or independent checks.; The ICCAD 2025 fallback paper is not an independent 2026 publication or year-over-year trend observation. Exact page/section/table locations were not recorded in this pass; no fabricated chiplet operation is established. |

<details markdown="1">
<summary>Historical captured record — superseded in the current table</summary>

Historical atlas evidence tier: `primary_preprint`.

| Field | Historical record |
|---|---|
| problem | Flat LLM-driven chiplet design has high validation cost and imprecise parameter optimization for complex hierarchical 2.5D systems. |
| mechanism | Six-agent hierarchical workflow combining AI-hardware parsing, structured module descriptions, retrieval-augmented RTL generation, tool-based validation/debugging, multi-granularity design-space exploration, and physical-layout configuration. |
| workload | Simple RTL and real-world AI chiplet-design tasks; PPA objectives and Pass@5 generation accuracy are evaluated against conventional LLMs and CLARIE. |
| hardware | 2.5D chiplet designs with AI workloads, RTL generation, synthesis/validation, and OpenROAD-like physical configuration; exact chiplet architectures, PPA flow, and design constraints require full-paper review. |
| baselines | conventional LLMs; CLARIE expert-based chiplet design framework |
| metrics | real-world chiplet-design Pass@5 from 0 to 0.72 in reported best-case comparison; comparable or superior PPA to CLARIE under selected objectives; RTL generation accuracy |
| limits | The preprint evidence does not establish average-case Pass@5, design-suite breadth, prompt/model costs, physical-flow reproducibility, or fairness of the CLARIE comparison; target edition remains 2026 while paper analysis uses the 2025 fallback corpus. |
| locator | MAHL is a hierarchical LLM-based chiplet design framework with six collaborating agents for AI-to-hardware mapping, hierarchical description generation, retrieval-augmented code generation, Diverseflow validation, adaptive debugging, and multi-granularity design-space exploration. It reports Pass@5 improvement from 0 to 0.72 for real-world chiplet design in a best-case comparison and comparable or superior PPA to CLARIE under some objectives. |

[Historical source](https://arxiv.org/abs/2508.14053)

</details>


Mapping review status: `not_recorded`; independent review status: `pending`.

## VeriOpt: PPA-Aware High-Quality Verilog Generation via Multi-Role LLMs

- Paper ID: `iccad-2025-1222`
- Conference/edition: `iccad` / `2025`
- Evidence tier: `Primary preprint v1; selected method/evaluation reading, not reproduction`
- Ledger record: `iccad/data/adjudicated-2025-batch-2.jsonl`

**Current evidence correction — 2026-09-08**

Reconciles the abstract-backed reading card with selected version-1 methods, evaluation and limitations; separates functional testing and PPA conditions.

Condition review of this correction and independent acceptance remain pending. The direction mapping is inherited, not revalidated by this update.

[Dated correction register](../../../data/editorial-paper-corrections-v1.json)

- Source: [https://arxiv.org/pdf/2507.14776v1](https://arxiv.org/pdf/2507.14776v1)

| Field | Current record |
|---|---|
| Problem | Generating functional RTL while improving its implementation costs. |
| Mechanism / artifact | Planning, programming, reviewing and evaluating roles; optimization context and synthesis reports. Section V-C specifies manual external feedback, not autonomous synthesis access. |
| Workload / benchmark | RTLLM's 29 tasks; Table II reports 25/29 testbench passes, not exhaustive correctness. |
| Hardware / process | GPT-4o, Icarus Verilog and Design Compiler; target-library, operating/activity assumptions and complete settings unresolved. |
| Baselines | PPA: functionally passing pre-optimization designs from the same flow. Functional comparisons: Table II's model/method configurations; budgets need reconciliation. |
| Metrics | Table III: 73.23% critical-path reduction for 16-bit divider, not timing-closure rate. Some leakage/slack regress. Table's 90% slack gain conflicts with prose's 39.44% maximum. |
| Evidence locator / span | Section III; IV-A and Table II PDF pages 6–7; IV-C/Table III pages 7–8; V-C page 8. |
| Limits | No execution or camera-ready reconciliation. Preserve per-candidate metric pairing, output-cycle requirements, post-optimization checks and complete manual/prompt costs; independent review pending. |

<details markdown="1">
<summary>Historical captured record — superseded in the current table</summary>

Historical atlas evidence tier: `primary_preprint`.

| Field | Historical record |
|---|---|
| problem | LLM-generated Verilog often targets functional correctness while neglecting power, performance, and area constraints required for practical hardware. |
| mechanism | Multi-role prompting and iterative PPA-aware optimization loop that combines planning, code generation, review, synthesis feedback, and evaluation. |
| workload | Synthesizable Verilog generation evaluated for functional correctness and PPA using industry-standard EDA tools; exact design suite and technology conditions require paper review. |
| hardware | RTL synthesis and timing/power/area evaluation with industry-standard EDA tools; process node, constraints, synthesis settings, and baseline prompts are not specified in the abstract. |
| baselines | baseline LLM-generated RTL |
| metrics | up to 88% power reduction; up to 76% area reduction; up to 73% timing-closure improvement; 86% functional-evaluation success |
| limits | The preprint abstract reports maximum gains without design-by-design distributions, model details, prompt cost, EDA settings, or leakage controls; PPA claims require full-paper and artifact verification. |
| locator | VeriOpt structures LLM interaction into Planner, Programmer, Reviewer, and Evaluator roles and feeds synthesis reports and timing diagrams back into PPA-aware prompting. The preprint reports up to 88% power reduction, 76% area reduction, 73% timing-closure improvement versus baseline LLM-generated RTL, and 86% functional-evaluation success. |

[Historical source](https://arxiv.org/abs/2507.14776)

</details>


Mapping review status: `not_recorded`; independent review status: `pending`.

## VERIRL: Boosting the LLM-based Verilog Code Generation via Reinforcement Learning

- Paper ID: `iccad-2025-110`
- Conference/edition: `iccad` / `2025`
- Evidence tier: `Primary preprint v1; selected method/evaluation reading, not reproduction`
- Ledger record: `iccad/data/adjudicated-2025-batch.jsonl`

**Current evidence correction — 2026-09-08**

Reconciles the preprint-backed card with selected method and evaluation sections; distinguishes inherited repair scores from original test outcomes.

Condition review of this correction and independent acceptance remain pending. The direction mapping is inherited, not revalidated by this update.

[Dated correction register](../../../data/editorial-paper-corrections-v1.json)

- Source: [https://arxiv.org/pdf/2508.18462v1](https://arxiv.org/pdf/2508.18462v1)

| Field | Current record |
|---|---|
| Problem | Learning a Verilog generator with informative training feedback. |
| Mechanism / artifact | Policy/reward-model training; trace-back replaces internal candidate scores with mean child rewards. Sample-balanced weighting uses generation probability and reward. |
| Workload / benchmark | VerilogEval-human and RTLLM v1.1; additional v2 evaluations. VeriBench-53K supports training, not a 53K held-out evaluation suite. |
| Hardware / process | CodeQwen2.5-based 7B and DeepSeek-Coder-based 6.7B configurations. No implemented-circuit power, area or timing evaluation established here. |
| Baselines | Table II's general and Verilog-specific models; matched training, sampling and selection budgets require verification. |
| Metrics | Twenty samples/task; best results across three temperatures. CodeQwen2.5 VERIRL Table II pass@1/pass@5: 69.3/78.1 VerilogEval-human; 58.2/66.0 RTLLM v1.1. |
| Evidence locator / span | Sections III, V–VI; trace-back PDF page 5; VII-D–F page 7; Table II page 8. |
| Limits | No execution. Reward is not acceptance; repaired descendants do not prove the original candidate correct. Dataset independence, artifacts, complete costs and conference version remain unverified. |

<details markdown="1">
<summary>Historical captured record — superseded in the current table</summary>

Historical atlas evidence tier: `primary_preprint`.

| Field | Historical record |
|---|---|
| problem | Verilog generation is difficult for language models because of concurrency semantics, rigid syntax, simulation complexity, and sparse or noisy correctness feedback. |
| mechanism | Reinforcement-learning framework for Verilog generation with a 53K-example dataset, Trace-back based Rescore, adaptive sample-balanced weighting, and co-evolving policy/reward models. |
| workload | Verilog code-generation tasks with diverse testbenches and complexity labels, curated from more than 700K source problems. |
| hardware | LLM-based HDL generation evaluated through compilation, simulation, and functional tests; exact model sizes, hardware, and test-suite composition require full-paper verification. |
| baselines | CraftRTL-style closed-source model distillation; DeepSeek-style approaches with sparse feedback; recent LLM-based Verilog generation methods |
| metrics | test pass rate; functional correctness; compilation robustness; 53K curated training/evaluation examples from more than 700K problems |
| limits | The evidence is an author preprint and public repository; the repository has not independently reproduced the reported gains or verified benchmark splits, leakage controls, reward validity, and hardware cost. |
| locator | VERIRL introduces Veribench-53K, curated from more than 700K Verilog problems with structured prompts, complexity labels, and testbenches. Its reinforcement-learning pipeline uses Trace-back based Rescore to improve sparse/noisy reward feedback and sample-balanced weighting to limit forgetting and overfitting; the abstract reports gains in test pass rate, functional correctness, and compilation robustness and releases the system publicly. |

[Historical source](https://arxiv.org/abs/2508.18462)

</details>


Mapping review status: `not_recorded`; independent review status: `pending`.

## HLSDebugger: Identification and Correction of Logic Bugs in HLS Code with LLM Solutions

- Paper ID: `iccad-2025-1027`
- Conference/edition: `iccad` / `2025`
- Evidence tier: `Primary arXiv preprint v1 and open-source artifact link; selected manuscript reading, artifact execution and independent acceptance not performed`
- Ledger record: `iccad/data/adjudicated-2025-batch.jsonl`

**Current evidence correction — 2026-09-08**

Reconciles the captured abstract card with the full arXiv preprint; separates HLS logic debugging from syntax repair, generated mutation supervision from natural bugs, identification granularities from exact-snippet correction, and benchmark results from hardware-level validity.

Condition review of this correction and independent acceptance remain pending. The direction mapping is inherited, not revalidated by this update.

[Dated correction register](../../../data/editorial-paper-corrections-v1.json)

- Source: [https://arxiv.org/pdf/2507.21485v1](https://arxiv.org/pdf/2507.21485v1)

| Field | Current record |
|---|---|
| Problem | HLS code can compile while implementing the wrong function. Debugging without reliable test cases requires locating the faulty code, identifying its logic-bug type and producing a correction; circuit data for training is scarce. |
| Mechanism / artifact | HLSDebugger releases an approximately 300K-sample labeled dataset and fine-tunes a CodeT5-Large encoder–decoder. The encoder predicts bug type and token locations; its representations guide a cross-attending decoder that generates the corrected snippet. A weighted joint loss trains bug type, imbalanced token location and correction generation together. |
| Workload / benchmark | A random 2,000-sample evaluation subset from an eight-bug-type HLS benchmark: out-of-bounds array access, uninitialized read, out-of-bounds shift, infinite loop, unintended sign extension, incorrect manual loop unrolling, wrong zero initialization and wrong split-buffer half. Training data starts with roughly 30K crawled HLS samples and roughly 10K GPT-3.5 RTL-to-HLS augmentations; about 2K high-Rouge-L-overlap samples are removed from training. |
| Hardware / process | CodeT5-Large with 24 encoder and 24 decoder transformer layers, 1024-dimensional embeddings and 16-dimensional heads; three-layer MLP prediction heads. Evaluation uses token, line and code-level identification plus strict processed substring matching for correction, with generated length limited to three times the label length. HLS compilation, synthesis, timing, area, power and independent functional/equivalence checking are not part of the reported correction metric. |
| Baselines | GPT-3.5; GPT-4; Gemma-7B without fine-tuning; Gemma-7B unsupervised fine-tuning; Gemma-7B supervised fine-tuning; HLSEncoder-only and encoder-plus-baseline combinations |
| Metrics | Identification: HLSDebugger token precision/recall/F1/ROC area 54.3%/83.5%/0.614/0.935; line precision/recall/F1/ROC area 57.7%/78.4%/0.627/0.923; code-wise top-1/top-5 79.5%/87.6%.; Identification baselines include GPT-4 token precision/recall 12.2%/37.1%, line precision/recall 13.3%/17.5% and code-wise top-1/top-5 19.7%/54.7%.; Correction without the true location: HLSDebugger 37.6%, GPT-4 10.5%, Gemma-7B SFT 15.1%, and HLSEncoder plus Gemma-7B SFT 23.7%. Correction with the ground-truth location supplied: HLSDebugger 49.1%. |
| Evidence locator / span | Version 1: Introduction and Figure 1 pages 1–2; dataset generation Sections IV-A and Figures 2–3 pages 3–4; encoder–decoder and joint loss Sections IV-B–C and Figures 4–6 pages 4–6; evaluation benchmark/model/metrics Sections V-A–D pages 6–7; identification Table II page 7; correction results Sections VI-A–B and Discussion VII, including Table/figures pages 7–8. Open-source artifact link in the paper: https://github.com/hkust-zhiyao/HLSDebugger; ICCAD DOI 10.1109/ICCAD66269.2025.11240664. |
| Limits | The approximately 300K labels are generated through code collection, GPT-3.5 augmentation and prompted bug insertion; the mutation distribution and eight categories do not establish coverage of naturally occurring HLS failures.; Strict substring match measures agreement with the labeled correction after preprocessing, not compilation, functional equivalence, synthesis validity, hardware quality or semantic correctness in an arbitrary surrounding design.; The 2,000-sample random evaluation subset and Rouge-L filtering constrain the reported generalization claim; exact project splits, per-category denominators and semantic contamination outside the threshold remain relevant.; The reported model is not ready for practical debugging according to the paper's own discussion: the best no-location correction rate is 37.6%. Training/inference cost, human effort, held-out projects, naturally occurring bugs and independent HLS-tool validation remain open. |

<details markdown="1">
<summary>Historical captured record — superseded in the current table</summary>

Historical atlas evidence tier: `primary_preprint`.

| Field | Historical record |
|---|---|
| problem | HLS logic debugging is labor-intensive, circuit data is scarce, logic bugs are harder than syntax bugs, and reliable test cases are often unavailable. |
| mechanism | Open labeled HLS bug dataset and customized encoder-decoder LLM that performs multi-task bug-location identification, bug-type prediction, and code correction, optionally using HLS-tool information. |
| workload | HLS code containing known logic-bug categories, without assuming additional test cases. |
| hardware | UNKNOWN — not present in the current adjudicated record |
| baselines | advanced general-purpose LLMs including GPT-4; traditional sequential LLM debugging solutions; HLS/static-analysis tool information when available |
| metrics | approximately 300K labeled training samples; bug-identification performance above GPT-4 in reported evaluation; more than 3X bug-correction performance improvement over advanced LLMs |
| limits | The evidence is an author preprint; evaluation depends on the generated bug dataset and selected bug categories, and the repository has not yet extracted all accuracy, correction-validity, and generalization tables. |
| locator | HLSDebugger addresses HLS logic debugging with a released labeled dataset of about 300K samples and an encoder-decoder model that jointly predicts bug location, bug type, and correction; the abstract reports performance above advanced LLMs such as GPT-4 for bug identification and more than 3X for bug correction. |

[Historical source](https://arxiv.org/abs/2507.21485)

</details>


Mapping review status: `not_recorded`; independent review status: `pending`.

## CODO: An Automated Compiler for Comprehensive Dataflow Optimization

- Paper ID: `isca-2026-program-002`
- Conference/edition: `isca` / `2026`
- Evidence tier: `primary_preprint`
- Ledger record: `isca/data/adjudicated-2026-batch.jsonl`
- Source: [https://arxiv.org/abs/2604.12618](https://arxiv.org/abs/2604.12618)

| Field | Current record |
|---|---|
| Problem | Manual construction of efficient streaming FPGA dataflow accelerators remains difficult even with high-level synthesis because dataflow legality, communication efficiency, and resource/performance tradeoffs interact. |
| Mechanism / artifact | CODO compiler built around systematic coarse- and fine-grained dataflow-violation detection and repair, on-chip/off-chip data-movement optimization, automatic scheduling, and a public artifact implementation. |
| Workload / benchmark | Typical computation kernels, DNN models, CNN models, and GPT-2 evaluated through synthesis and on-board FPGA experiments. |
| Hardware / process | FPGA dataflow accelerators and high-level-synthesis tool flows; the public evidence does not establish applicability to ASIC implementation or all FPGA families. |
| Baselines | state-of-the-art dataflow/HLS frameworks |
| Metrics | 1.45x–4.52x latency speedup on computation kernels; 3.7x–33.8x speedup on DNN models; 7.3x average CNN speedup in on-board evaluation; 2.07x GPT-2 speedup in on-board evaluation; performance-resource tradeoff |
| Evidence locator / span | The paper presents an automated compiler for FPGA dataflow accelerators. It detects and removes coarse- and fine-grained dataflow violations, optimizes on-chip and off-chip data movement, and automatically schedules designs to balance performance and resource use. The reported results include 1.45x–4.52x latency speedups on computation kernels, 3.7x–33.8x speedups on DNN models, 7.3x average speedup on CNNs, and 2.07x speedup on GPT-2; the artifact is publicly released. |
| Limits | The evidence is an author arXiv preprint plus public artifact documentation; the repository has not independently reproduced synthesis or board results, extracted every baseline/configuration, or established generalization beyond the reported FPGA flows. |

Mapping review status: `not_recorded`; independent review status: `pending`.

## Direction boundary

The records support tool-grounded mechanisms, not average-case correctness, model/API cost, transfer across design suites, or production adoption.

Next evidence action: Compare accepted designs, failed attempts, regressions, checker state, and transfer at equal synthesis, model-call, retry, and wall-clock budgets.
