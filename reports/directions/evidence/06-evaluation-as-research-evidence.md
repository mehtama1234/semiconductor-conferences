# Evidence dossier — Evaluation As Research

This dossier combines the canonical direction atlas, historical adjudicated records, and dated editorial corrections. It is a source-backed reading aid, not an independent review or a claim that the records are comparable.

- Direction page: [Evaluation As Research](../06-evaluation-as-research.md)
- Source direction IDs: `tool-grounded-ai-design-verification, multifidelity-physics-aware-search`
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

## GEMIR: Graph-Based Joint Modeling of Electromigration and IR Drop for Power Grid

- Paper ID: `dac-2026-research046`
- Conference/edition: `dac` / `2026`
- Evidence tier: `Primary captured official DAC description plus bounded recovery assessment and existing authored power-integrity discussion; full paper not recovered, numerical claims withheld pending conditions, no reproduced physics validation or fabricated-chip result`
- Ledger record: `dac/data/adjudicated-2026-batch.jsonl`

**Current evidence correction — 2026-09-09**

Deepens the GEMIR treatment into a paper-level reading; separates joint graph prediction, node-edge attention, KCL/Korhonen physics constraints and conflict-gated multitask training from physical boundary validity, tail errors, signoff thresholds, calibration and process transfer, while preserving the 40.79% IR-drop-MAE and 19.35% EM-stress-RMSE source claims as withheld pending full-paper conditions.

Condition review of this correction and independent acceptance remain pending. The direction mapping is inherited, not revalidated by this update.

[Dated correction register](../../../data/editorial-paper-corrections-v1.json)

- Source: [https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH046](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH046)

| Field | Current record |
|---|---|
| Problem | Power-grid reliability depends on both node-level voltage loss and edge-level electromigration stress, while numerical analysis is expensive on large designs and separate ML predictors may miss shared structure. |
| Mechanism / artifact | GEMIR jointly predicts static IR drop at graph nodes and electromigration-induced stress at graph edges using cross-layer node-edge attention, physics-informed constraints incorporating Kirchhoff's current law and the Korhonen PDE, and conflict-gated multitask gradient fusion. Features, loss terms, boundary conditions, gradient gate, training targets and inference workflow are unspecified. |
| Workload / benchmark | Power-grid analysis on large-scale designs for static IR drop and EM-induced stress; design sizes, technology/process, grid topology, current loads, temperature/material parameters, train/test split, leakage controls, numerical reference solver, PVT/aging conditions and workload population are unspecified. |
| Hardware / process | Power-grid graphs with node voltage and edge stress fields; physical boundary conditions, via/resistance/capacitance models, current sources, thermal coupling, material parameters, process node, signoff tool, compute hardware and fabricated-chip validation are unspecified. |
| Baselines | Existing numerical power-grid methods; Single-task ML predictors; Multitask ML baselines; Same designs, reference solver, loads, physical parameters, train/test split, error units, runtime hardware and signoff threshold are unspecified |
| Metrics | The source reports 40.79% reduction in IR-drop mean absolute error and 19.35% reduction in electromigration-stress root-mean-square error, plus computational efficiency and generalization; it reports no absolute errors/units, worst-case or tail error, named baseline conditions, design/process distribution, runtime, memory, threshold violations, lifetime prediction or silicon validation. |
| Evidence locator / span | DAC 2026 official description; existing power-integrity-and-reliability editorial explanation; selected primary-source recovery assessment; captured Problem, Mechanism / artifact, Workload, Hardware, Baseline, Measurements and Limits fields; no full manuscript, design/process matrix, numerical trace or independent signoff validation. |
| Limits | KCL and the Korhonen PDE are useful constraints only when boundary conditions, source terms, material parameters, temperature and discretization match the physical problem. Verify residuals and conservation on held-out grids, compare node/edge extremes with a trusted numerical solver and test current/load, temperature, geometry and material shifts; low mean error can hide a signoff-critical hotspot or stressed segment.; IR-drop MAE and EM-stress RMSE are different quantities and cannot be averaged into a reliability gain. Report absolute units, distributions, maxima/percentiles, threshold classification, spatial localization and error correlation; distinguish prediction quality from the downstream decision of widening a wire, adding vias or changing the grid. Measure graph construction, reference-solver labels, training/inference, calibration and any fallback cost.; The 40.79%/19.35% reductions and generalization claim are description-backed with full-paper conditions unresolved. They do not establish signoff-quality power integrity, lifetime improvement, cross-technology transfer or fabricated-chip validity. The evidence supports physics-informed joint EM/IR prediction, not replacement of trusted power-integrity and reliability checks. |

<details markdown="1">
<summary>Historical captured record — superseded in the current table</summary>

Historical atlas evidence tier: `official_description`.

| Field | Historical record |
|---|---|
| problem | Separate EM and IR-drop analysis misses their shared physical structure, while numerical methods are expensive on large designs. |
| mechanism | Graph-based multitask learning with node-edge attention, physics-informed constraints, and conflict-gated gradient fusion. |
| workload | Power-grid analysis for node-level static IR drop and edge-level electromigration-induced stress. |
| hardware | UNKNOWN — not present in the current adjudicated record |
| baselines | existing numerical methods; single-task machine-learning approaches; multitask baselines |
| metrics | 40.79% reduction in IR-drop MAE; 19.35% reduction in EM-stress RMSE; computational efficiency and generalization |
| limits | The description does not disclose design sizes, absolute runtime, or the distribution of gains across technologies and workloads. |
| locator | GEMIR jointly predicts node-level static IR drop and edge-level electromigration stress using cross-layer attention, physics-informed constraints for KCL and the Korhonen PDE, and conflict-gated multitask optimization; it reports 40.79% lower IR-drop MAE and 19.35% lower EM-stress RMSE. |

[Historical source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH046&sess=sess112)

</details>


Mapping review status: `not_recorded`; independent review status: `pending`.

## HYPER-CIM: Hierarchical Predictive Exploration and Realizable Design Flow for High-Efficient Digital CIM

- Paper ID: `dac-2026-research1101`
- Conference/edition: `dac` / `2026`
- Evidence tier: `Primary captured official DAC description plus supplementary official/institutional assessment; no recovered full paper or independent surrogate, design-flow and silicon reproduction`
- Ledger record: `dac/data/adjudicated-2026-batch.jsonl`

**Current evidence correction — 2026-09-08**

Reconciles the HYPER-CIM card with the captured official description and supplementary assessment; explains CIM hierarchy, surrogate prediction, Pareto tradeoffs, TOPS metrics, predicted configuration counts and silicon-verification scope from first principles.

Condition review of this correction and independent acceptance remain pending. The direction mapping is inherited, not revalidated by this update.

[Dated correction register](../../../data/editorial-paper-corrections-v1.json)

- Source: [https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH1101&sess=sess156](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH1101&sess=sess156)

| Field | Current record |
|---|---|
| Problem | CIM exploration can optimize one level without preserving circuit-faithful visibility into macro, accelerator and architecture interactions, making predicted high-efficiency designs difficult to realize or compare. |
| Mechanism / artifact | Hierarchical predictive exploration flow with a digital 28-nm CIM template, multi-head circuit-optimization surrogate, Pareto search and selected silicon verification. |
| Workload / benchmark | Digital CIM macro and architecture design across precision, storage, channels, pipeline depth and accumulation length; workload, accuracy, operation convention, comparison set and hierarchy conditions are unspecified. |
| Hardware / process | Digital 28-nm CIM template and fabricated macro evidence; process details, frequency, power/area boundaries, yield, layout, test conditions and architecture integration are unspecified. |
| Baselines | Prior CIM designs; Single-level CIM optimization flows; Full comparison set, objective normalization, workload/accuracy, prediction fidelity and fabricated-condition parity are unspecified |
| Metrics | The official description reports 90.8 TOPS/W, 1.23 TOPS/mm², 31.12x–3.8x10^6x FoM improvement, 52.13–67.9 TOPS/W and 0.41–0.51 TOPS/mm² ranges; operation, power, area, workload, reference and aggregation boundaries are unspecified. |
| Evidence locator / span | DAC 2026 official description and data/review-packets/dac-2026-research1101.json plus data/review-packets/hyper-cim-primary-recovery-v1.json: digital 28-nm CIM template; multi-head surrogate; hierarchical/Pareto flow; silicon verification claim; 90.8 TOPS/W, 1.23 TOPS/mm² and wide FoM/range claims; 297M predicted configurations, >8k training points and five reported macros assessment boundary. |
| Limits | A circuit surrogate can reduce exploration cost only if its prediction error preserves useful candidate ordering near constraints and Pareto boundaries; average error alone is insufficient.; Pareto search yields non-dominated tradeoffs rather than one universally best design, and its result depends on objectives, normalization, constraints and precision.; 297 million predicted configurations and more than 8,000 training points are modeling/search quantities, not fabricated designs; five reported macros do not validate the full predicted space.; Silicon verification of selected macros can expose model mismatch but does not establish all predicted configurations, full architecture integration, yield or reproducibility; full paper and comparison conditions remain open. |

<details markdown="1">
<summary>Historical captured record — superseded in the current table</summary>

Historical atlas evidence tier: `official_description`.

| Field | Historical record |
|---|---|
| problem | CIM exploration often optimizes only one level and lacks circuit-faithful visibility across macro, accelerator, and architecture decisions. |
| mechanism | Hierarchical predictive exploration flow with a digital 28 nm CIM template, multi-head circuit-optimization surrogate, Pareto search, and silicon verification. |
| workload | Digital compute-in-memory macro and architecture design across tunable precision, storage, channels, pipeline depth, and accumulation length. |
| hardware | UNKNOWN — not present in the current adjudicated record |
| baselines | prior CIM designs; single-level CIM optimization flows |
| metrics | 90.8 TOPS/W; 1.23 TOPS/mm²; 31.12X–3.8×10⁶X FoM improvement; 52.13 to 67.9 TOPS/W energy-efficiency improvement; 0.41 to 0.51 TOPS/mm² area-efficiency improvement |
| limits | The description does not provide the full prior-design comparison set, accuracy/workload conditions, or yield/reproducibility details for fabricated macros. |
| locator | HYPER-CIM uses over 8k silicon-consistent points to train a hierarchical PPA surrogate over 297M configurations, fabricates and verifies 28 nm CIM macros, and reports 90.8 TOPS/W, 1.23 TOPS/mm², and cross-level energy/area improvements. |

[Historical source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH1101&sess=sess156)

</details>


Mapping review status: `not_recorded`; independent review status: `pending`.

## RSizing: Robust Bayesian Optimization for Analog Circuit Sizing Under Process Variations

- Paper ID: `iccad-2025-1080`
- Conference/edition: `iccad` / `2025`
- Evidence tier: `Primary author-hosted manuscript-backed selected evaluation; page-level extraction performed 2026-09-08; independent reproduction and broader technology/circuit validation remain open`
- Ledger record: `iccad/data/adjudicated-2025-batch.jsonl`

**Current evidence correction — 2026-09-08**

Adds a page-backed RSizing reading from the recovered author PDF; explains robust Pareto optimization, heteroscedastic process variation, MVaR approximation, Monte Carlo budgets and the yield/runtime tradeoff rather than retaining the shallow card.

Condition review of this correction and independent acceptance remain pending. The direction mapping is inherited, not revalidated by this update.

[Dated correction register](../../../data/editorial-paper-corrections-v1.json)

- Source: [https://www.cse.cuhk.edu.hk/~byu/papers/C287-ICCAD2025-RSizing.pdf](https://www.cse.cuhk.edu.hk/~byu/papers/C287-ICCAD2025-RSizing.pdf)

| Field | Current record |
|---|---|
| Problem | Analog circuit sizing must choose device parameters that trade several performance objectives while meeting a probability-of-success requirement under process variation. |
| Mechanism / artifact | Three-phase robust Bayesian optimization: nominal multi-objective pruning, heteroscedastic Gaussian-process modeling with Thompson sampling and targeted Monte Carlo refinement/calibration; the recovered paper defines a robust Pareto set using a yield constraint. |
| Workload / benchmark | ITC 2017 OPAMP, OSC and PLL benchmark circuits with 36, 14 and 77 selected parameters and the listed circuit objectives; Spectre simulations use TSMC 40 nm. Yield targets are 97.5%, 99.0% and 99.9%. |
| Hardware / process | Spectre analog simulation on TSMC 40 nm; 80-core 2.70 GHz CPU and A100 80 GB machine; 50 Monte Carlo samples in variation-aware optimization and 100/200/500 refinement samples for the three yield targets, with final verification by 1,000 samples. |
| Baselines | NSGA-II; MARS-NEI; PVTSizing; NSGA-II is omitted for PLL because of simulation cost; baseline budgets and objective constructions are not fully symmetric |
| Metrics | Manuscript-backed: Table II verifies mean/min/max yield over 1,000 Monte Carlo samples; Table III reports yield, hypervolume and runtime for OPAMP/OSC/PLL at 97.5%, 99.0% and 99.9%; Table IV compares PVTSizing and RSizing at three targets. The paper notes MVaR approximation bias for lower yield requirements and tradeoffs between target yield and performance. |
| Evidence locator / span | Recovered author-hosted PDF v1, pages 1–7; Sections II–IV; Fig. 2; Table I (page 6), Tables II–IV (page 7); TSMC 40 nm, ITC 2017 OPAMP/OSC/PLL, yield targets, Monte Carlo budgets and baseline settings. |
| Limits | A robust Pareto solution is not one design that maximizes every metric. It is a set of non-dominated designs whose probability of meeting the performance specifications is at least the required yield. The yield estimate is itself uncertain when based on finite Monte Carlo samples, especially near a threshold.; The heteroscedastic GP models input-dependent variation and the acquisition function chooses expensive simulations, but the model can be wrong when distributions are non-Gaussian or local variation changes. The paper's refinement uses MVaR estimates and states that approximation error is not fully addressed and may bias results at lower yield.; The recovered experiment is strong page-backed evidence under TSMC 40 nm, ITC 2017 circuits, stated simulation budgets and a specific machine. It does not establish transfer to other nodes, circuits, simulators, variation distributions or commercial signoff. Runtime comparisons also need the asymmetric PLL omission and different baseline budgets kept visible. |

<details markdown="1">
<summary>Historical captured record — superseded in the current table</summary>

Historical atlas evidence tier: `author_pdf`.

| Field | Historical record |
|---|---|
| problem | Analog circuit sizing under process variation is expensive and manual; nominal optimization can produce designs with poor yield when performance distributions shift across manufacturing variation. |
| mechanism | Three-phase robust Bayesian optimization using nominal-region pruning, heteroscedastic Gaussian-process surrogate models, Thompson sampling, targeted Monte Carlo simulations, and model calibration. |
| workload | Three analog benchmark circuits evaluated under process variation with multi-objective performance and yield requirements. |
| hardware | CMOS analog circuit sizing and Monte Carlo process-variation simulation; exact technology node, circuit identities, and simulation budgets require full-paper extraction. |
| baselines | existing analog circuit sizing and Bayesian-optimization methods |
| metrics | yield requirement satisfaction; multiple analog performance objectives; Monte Carlo simulation/computational cost |
| limits | The evidence is an author-hosted conference PDF; the repository has not yet extracted numerical table values, exact baselines, technology assumptions, or all yield/quality tradeoffs. |
| locator | RSizing uses a three-phase strategy: nominal-condition optimization to prune promising regions, heteroscedastic Gaussian processes to model non-uniform process-variation effects, and Thompson-sampling acquisition followed by targeted Monte Carlo refinement and calibration. Experiments on three benchmark circuits report robust designs that meet yield requirements while optimizing multiple performance metrics with lower computational cost. |

[Historical source](https://www.cse.cuhk.edu.hk/~byu/papers/C287-ICCAD2025-RSizing.pdf)

</details>


Mapping review status: `not_recorded`; independent review status: `pending`.

## NeuroPDE: A Neuromorphic PDE Solver Based on Spintronic and Ferroelectric Devices

- Paper ID: `iccad-2025-130`
- Conference/edition: `iccad` / `2025`
- Evidence tier: `Recovered version-1 manuscript; cited sections inspected`
- Ledger record: `iccad/data/adjudicated-2025-batch-2.jsonl`

**Current evidence correction — 2026-09-07**

Full text establishes simulation-only evidence and single-walk accounting; squared-error definition differs from statistical variance.

Condition review of this correction and independent acceptance remain pending. The direction mapping is inherited, not revalidated by this update.

[Dated correction register](../../../data/editorial-paper-corrections-v1.json)

- Source: [https://arxiv.org/pdf/2507.04677v1](https://arxiv.org/pdf/2507.04677v1)

| Field | Current record |
|---|---|
| Problem | Efficient probabilistic transitions for PDE estimation. |
| Mechanism / artifact | Magnetic switching and ferroelectric transition weights. |
| Workload / benchmark | 1D heat and 2D diffusion examples; single-thread random walks. |
| Hardware / process | SPICE/Python simulation; GPDK045, 300 K; 50,000 activation histories. |
| Baselines | Analytical solutions; prior Loihi/TrueNorth results. |
| Metrics | Single-walk operation: 10 ns, 1.451 pJ; not complete solution cost. |
| Evidence locator / span | Sections IV–V, PDF pages 4–8; Equation 10, Figure 12. |
| Limits | Equation 10 is squared reference error; temperature drift untested; not fabricated hardware. |

<details markdown="1">
<summary>Historical captured record — superseded in the current table</summary>

Historical atlas evidence tier: `primary_preprint`.

| Field | Historical record |
|---|---|
| problem | Conventional von Neumann hardware lacks hardware-intrinsic randomness, limiting the performance of Monte Carlo and random-walk PDE solvers. |
| mechanism | Neuromorphic architecture using stochastic spin neurons for probabilistic transmission and ferroelectric synapses for continuous non-volatile weights. |
| workload | Diffusion-equation PDE solving with comparison against analytical solutions and CMOS-based neuromorphic-chip baselines. |
| hardware | Emerging spintronic and ferroelectric devices with physical stochasticity and non-volatile analog weight storage; device models, variability, conversion, and fabrication assumptions require full-paper review. |
| baselines | advanced CMOS-based neuromorphic chips; analytical diffusion-equation solutions |
| metrics | variance below 1e-2 versus analytical solutions; 3.48x–315x execution-time speedup; 2.7x–29.8x energy advantage |
| limits | The preprint abstract does not expose PDE suite breadth, device-area and conversion costs, process assumptions, precision, or how CMOS baselines are normalized; ranges require paper-level verification. |
| locator | NeuroPDE uses probabilistic spin neurons to emulate random walks and non-volatile ferroelectric synapses for continuous weights in a neuromorphic PDE solver. For diffusion equations it reports variance below 1e-2 against analytical solutions, 3.48x–315x execution-time speedup, and 2.7x–29.8x energy advantage over advanced CMOS-based neuromorphic chips. |

[Historical source](https://arxiv.org/abs/2507.04677)

</details>


Mapping review status: `not_recorded`; independent review status: `pending`.

## Quantum Circuit Synthesis Using an Exact T Library

- Paper ID: `dac-2026-research031`
- Conference/edition: `dac` / `2026`
- Evidence tier: `Primary captured official DAC description plus selected author-preprint reading; source-version discrepancy remains open, and no independent exactness proof, benchmark reproduction or fault-tolerant hardware validation`
- Ledger record: `dac/data/adjudicated-2026-batch.jsonl`

**Current evidence correction — 2026-09-09**

Deepens the exact-T synthesis treatment using the captured official description and selected author-preprint assessment; separates Clifford-equivalence canonicalization, bounded exact library construction and mapping from clean-ancilla correctness, global optimality, runtime and hardware cost, and preserves the official up-to-16% claim alongside the assessed 5.3% six-EPFL-circuit geomean and 0.5% library-only result with their source/version boundary.

Condition review of this correction and independent acceptance remain pending. The direction mapping is inherited, not revalidated by this update.

[Dated correction register](../../../data/editorial-paper-corrections-v1.json)

- Source: [https://arxiv.org/html/2605.15476v1](https://arxiv.org/html/2605.15476v1)

| Field | Current record |
|---|---|
| Problem | In fault-tolerant quantum synthesis, T resources dominate relevant space-time cost while minimizing classical AND count can miss phase cancellation and therefore misestimate T cost. |
| Mechanism / artifact | The work formulates exact T synthesis, canonicalizes Boolean functions under Clifford equivalence, precomputes T-optimal implementations for bounded small instances and uses a specialized mapper for larger circuits. The selected assessment identifies an exact-solver bound of N ≤ 7 total qubits and correctness under a clean output ancilla initialized to zero; phase-equivalence, ancilla, synthesis and mapper details remain bounded by the inspected sections. |
| Workload / benchmark | EPFL arithmetic circuits and selected cryptographic modules; the selected assessment reports six EPFL circuits, comparison against exact-MC mapping, library-only substitution, and a QLUT mapping evaluation. Circuit dimensions, gate basis, ancilla limits, decomposition conventions, target fault-tolerant architecture, runtime corpus and source-version relationship to the official 16% headline are not fully reconciled. |
| Hardware / process | Fault-tolerant quantum compilation where T gates/magic states are costly; selected mapping assessment ran on an Apple M4 Max with 36 GB RAM, but physical architecture, magic-state factory cost, scheduling, parallelism, error-correction code, qubit budget, decoder and hardware execution are unspecified. |
| Baselines | Conventional XOR/AND/NOT-basis AND-count minimization; Exact-MC mapping; Library-only substitution; Previous best-known T counts; Same Boolean/unitary convention, clean-ancilla assumption, circuit set, gate basis, decomposition, mapper, target constraints, runtime boundary and source version are unspecified |
| Metrics | The official description reports up to 16% T-count reduction on EPFL benchmarks and improved best-known T counts for selected cryptographic modules. The selected author-preprint assessment reports 5.3% geometric-mean T-count reduction for six EPFL arithmetic circuits with the customized mapper, about 0.5% geometric-mean reduction for library-only substitution with regressions on some circuits, and mapping stages up to 11.7% of reported QLUT synthesis runtime; these are not reconciled into one universal result and no hardware speedup is reported. |
| Evidence locator / span | DAC 2026 official description; selected author-preprint assessment exact-t-primary-assessment-v1; sections 4.2–4.3 and 6, S4.SS2/S4.SS3/S6.SS1/S6.SS2/S6.SS4, Table 2 and Figures 8–11; no independent reproduction or hardware execution. |
| Limits | Exactness is conditional. Verify the synthesized operation under the stated Clifford-equivalence and clean-zero-ancilla assumptions, including global phase, output ancilla state, qubit ordering, measurement behavior and allowed temporary resources. A circuit can match a Boolean function while violating the intended unitary or ancilla contract.; Exact optimality for N ≤ 7 total qubits does not establish global optimality for larger mapped circuits. Report library construction/storage, mapper search, decomposition, ancilla, depth, Clifford count, routing and compilation runtime; test held-out circuits and compare per-circuit regressions rather than only a best or geometric mean.; The official up-to-16% headline and selected 5.3%/0.5% preprint findings have different scopes and require source-version reconciliation. T-count reduction is not hardware speedup or universal space-time reduction; magic-state production, scheduling, parallelism, code distance, qubit count, error rates and physical execution remain unvalidated. The evidence supports exact bounded T-cost synthesis, not demonstrated globally optimal or hardware-efficient fault-tolerant compilation. |

<details markdown="1">
<summary>Historical captured record — superseded in the current table</summary>

Historical atlas evidence tier: `official_description`.

| Field | Historical record |
|---|---|
| problem | AND-count minimization is an imperfect proxy for T cost in fault-tolerant quantum synthesis because it misses phase cancellation. |
| mechanism | Exact T-synthesis formulation with Clifford-equivalence canonicalization, precomputed small-function libraries, and a specialized mapper. |
| workload | EPFL benchmarks and cryptographic circuit modules in fault-tolerant quantum synthesis. |
| hardware | UNKNOWN — not present in the current adjudicated record |
| baselines | conventional XOR/AND/NOT-basis AND-count minimization; previous best-known T counts |
| metrics | up to 16% T-count reduction; improved best-known T counts for selected cryptographic modules |
| limits | The public description does not enumerate all circuits, runtime costs, or the scalability boundary of exact precomputation. |
| locator | The work formulates exact T synthesis, canonicalizes Boolean functions under Clifford equivalence, precomputes T-optimal implementations up to seven variables, and reports up to 16% T-count reduction on EPFL benchmarks plus improvements for cryptographic modules. |

[Historical source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH031&sess=sess133)

</details>


Mapping review status: `researcher_reconciliation_not_independent`; independent review status: `pending`.

## Xsearch: Exploring Microarchitecture Design Space Through Bayesian Optimization and Cross Evaluation on Multi-Fidelity Simulators

- Paper ID: `dac-2026-research1186`
- Conference/edition: `dac` / `2026`
- Evidence tier: `Primary captured official DAC description plus existing authored learned-DSE discussion; no full-paper extraction, numerical result, simulator-condition matrix or independent high-fidelity validation`
- Ledger record: `dac/data/adjudicated-2026-batch-4.jsonl`

**Current evidence correction — 2026-09-09**

Deepens the Xsearch treatment into a paper-level reading; separates multi-fidelity Bayesian acquisition and high-fidelity cross-evaluation from simulator calibration error, ranking validity, feasibility, search budget and processor-design conclusions, while preserving the XiangShan application without inventing quantitative superiority.

Condition review of this correction and independent acceptance remain pending. The direction mapping is inherited, not revalidated by this update.

[Dated correction register](../../../data/editorial-paper-corrections-v1.json)

- Source: [https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH1186&sess=sess167](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH1186&sess=sess167)

| Field | Current record |
|---|---|
| Problem | Microarchitecture design-space exploration must choose among expensive accurate simulations and cheaper coarse simulations; a low-fidelity shortcut can spend more evaluations while changing the ranking of viable processor configurations. |
| Mechanism / artifact | Xsearch is described as multi-fidelity Bayesian optimization that cross-evaluates designs across simulators with different fidelity and uses high-fidelity simulation data for calibration; acquisition function, surrogate outputs and uncertainty, fidelity-selection rule, calibration model, simulator coupling and stopping criterion are unspecified. |
| Workload / benchmark | Microarchitecture-parameter exploration for the open-source XiangShan high-performance processor core; core revision, parameter dimensions/ranges, workloads, warm-up and sampling protocol, objectives, constraints, design-space size, train/validation split and held-out final evaluation are unspecified. |
| Hardware / process | Processor design flow using coarse- and fine-grained simulators with different cost and accuracy; simulator identities/versions, target implementation, architectural model, compute hardware, parallelism, licensing and timing boundary are unspecified. |
| Baselines | Low-fidelity-only Bayesian or search-based exploration; High-fidelity-only exploration; Random or conventional Bayesian optimization with one simulator; Same XiangShan configuration space, workloads, objective/constraints, seed, evaluation budget, calibration data, simulator versions and end-to-end timing boundary are unspecified |
| Metrics | The source claims an efficiency–accuracy tradeoff, broader low-fidelity exploration and high-fidelity calibration/cross-evaluation on XiangShan, but reports no numerical improvement, simulator error, convergence, final design quality, feasibility rate, evaluation count, wall-clock cost or high-fidelity held-out result. |
| Evidence locator / span | DAC 2026 official description; existing learned-design-space-exploration chapter framing; captured Problem, Mechanism / artifact, Workload, Hardware, Baseline, Measurements and Limits fields; no manuscript pages, simulator table, search trace or reproduced XiangShan evaluation. |
| Limits | Low-fidelity agreement is not automatically a useful design signal. Measure prediction error and rank agreement against high-fidelity simulation across the full parameter space, especially near constraints and Pareto boundaries; a calibrated average can still select an infeasible or inferior processor configuration. Report uncertainty, calibration residuals, false feasible/false infeasible decisions and the cost of each high-fidelity check.; Bayesian optimization needs an explicit objective, constraints, acquisition function, initial design, fidelity-selection policy, noise model, stopping rule and total budget. Count low- and high-fidelity simulations, surrogate training, failed simulations, calibration, parallelism and final confirmation under the same elapsed-time or compute boundary. More explored points is not evidence of a better design without matched-budget final evaluation.; XiangShan application does not establish transfer to another core, workload, simulator pair or implementation target. Hold out workloads, parameter regions and processor revisions; inspect repeated seeds, convergence and rejected candidates, and compare low-fidelity-only, high-fidelity-only and single-fidelity search at equal objectives and budgets. The official description supports a multi-fidelity exploration direction, not demonstrated quantitative superiority, simulator-grounded accuracy or improved processor design quality. |

<details markdown="1">
<summary>Historical captured record — superseded in the current table</summary>

Historical atlas evidence tier: `official_description`.

| Field | Historical record |
|---|---|
| problem | Microarchitecture design-space exploration must balance expensive accurate simulation against fast but less accurate coarse simulation. |
| mechanism | Multi-fidelity Bayesian optimization with cross-evaluation across simulators of different fidelity and calibration using high-fidelity data. |
| workload | Microarchitecture parameter exploration for the open-source XiangShan high-performance processor core. |
| hardware | Open-source high-performance processor and multiple simulators with differing fidelity; parameter space, simulator identities, calibration model, and hardware targets are not reported. |
| baselines | low-fidelity-only exploration; high-fidelity-only exploration (implied comparison) |
| metrics | exploration efficiency and evaluation accuracy (numeric results not reported in the description) |
| limits | The description does not report search budgets, objective functions, simulator errors, convergence, baseline results, or processor configurations; it establishes the method and application but not quantitative superiority. |
| locator | XSearch addresses the efficiency–accuracy trade-off in microarchitecture design-space exploration by using multi-fidelity Bayesian optimization. It explores more points with low-fidelity simulation and calibrates or cross-evaluates candidates with high-fidelity simulation; the method is applied to the open-source XiangShan high-performance processor core. |

[Historical source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH1186&sess=sess167)

</details>


Mapping review status: `researcher_reconciliation_not_independent`; independent review status: `pending`.

## Direction boundary

The records support tool-grounded mechanisms, not average-case correctness, model/API cost, transfer across design suites, or production adoption. Search quality requires baseline budgets, constraint-violation analysis, model error, and independent reproduction; headline surrogate or figure-of-merit gains are conditional.

Next evidence action: Require each accepted direction claim to carry task population, evaluator version, failure semantics, baseline, budget, and independent review status.
