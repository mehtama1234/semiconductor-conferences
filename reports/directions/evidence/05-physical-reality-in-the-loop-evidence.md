# Evidence dossier — Physical Reality In The Loop

This dossier combines the canonical direction atlas, historical adjudicated records, and dated editorial corrections. It is a source-backed reading aid, not an independent review or a claim that the records are comparable.

- Direction page: [Physical Reality In The Loop](../05-physical-reality-in-the-loop.md)
- Source direction IDs: `physical-integration-optimization-variable`
- Direction status: `provisional_mechanism_hypothesis`
- Independent reviews recorded: `0`

## Reading rule

`UNKNOWN` means a field is not recorded, not that the paper lacks the condition. Corrections supersede the current displayed fields while historical fields remain expandable. A historical condition-complete label does not establish that a correction has passed condition or independent review.

## FLASH3D: A Fast Layered Analytical Solver for High-Accuracy Steady-State Thermal Simulation of 3D ICs

- Paper ID: `dac-2026-research1065`
- Conference/edition: `dac` / `2026`
- Evidence tier: `Primary captured official DAC description only; no full-paper extraction, numerical-solver reproduction or independent transient/transfer validation`
- Ledger record: `dac/data/adjudicated-2026-batch.jsonl`

**Current evidence correction — 2026-09-08**

Reconciles the FLASH3D card with the captured official source; explains steady-state analytical thermal simulation from first principles and separates modal decomposition, transfer matrices, power-map resolution, maximum error, transient scope and speedup comparison boundaries.

Condition review of this correction and independent acceptance remain pending. The direction mapping is inherited, not revalidated by this update.

[Dated correction register](../../../data/editorial-paper-corrections-v1.json)

- Source: [https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH1065&sess=sess156](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH1065&sess=sess156)

| Field | Current record |
|---|---|
| Problem | High-fidelity 3D-IC thermal simulation is too slow for early thermal-aware design exploration. |
| Mechanism / artifact | Layered analytical steady-state thermal solver combining spectral modal decomposition, transfer matrix propagation and accelerated power decomposition for fine-grained 3D power maps and complex boundaries. |
| Workload / benchmark | 3D-IC steady-state temperature distributions with curved-edge boundaries and standard-cell-level power maps; designs, layer counts, resolutions, power cases and reference discretization are unspecified. |
| Hardware / process | Layered 3D-IC thermal structures with material and cooling boundaries; geometry/material parameters, solver hardware, numerical precision, reference mesh and preprocessing are unspecified. |
| Baselines | COMSOL; DeepOHeat machine-learning thermal simulator; Hardware, discretization, preprocessing, accuracy target and timing boundaries are unspecified |
| Metrics | The official description reports more than four orders of magnitude speedup versus COMSOL, computation reduced from minutes to milliseconds, maximum absolute error below 0.5 K, and approximately 10x lower error than DeepOHeat while processing roughly 2000 slices per inference; per-case runtimes, error aggregation and setup boundaries are unspecified. |
| Evidence locator / span | DAC 2026 official description and data/review-packets/dac-2026-research1065.json: steady-state scope; spectral modal decomposition; transfer matrix method; accelerated power decomposition; curved-edge and standard-cell-level maps; COMSOL speed/error claims and DeepOHeat 2000-slice/10x-error claim. |
| Limits | The method is described for steady-state temperature fields; these results do not establish transient accuracy, heating/cooling response or workload-switching behavior.; A maximum absolute error below 0.5 K is conditioned on the tested reference, points, geometry, materials and boundaries; it does not establish accuracy for unseen stacks or local interfaces without those conditions.; The COMSOL speedup and DeepOHeat slice-throughput comparison use different baselines and should not be combined; preprocessing, hardware, batch size and solver convergence are not reported.; The official description supplies no complete geometry/material assumptions, absolute per-case runtimes, discretization, memory use or independent reproduction; early-design usefulness remains to be tested through a decision-level thermal flow. |

<details markdown="1">
<summary>Historical captured record — superseded in the current table</summary>

Historical atlas evidence tier: `official_description`.

| Field | Historical record |
|---|---|
| problem | High-fidelity 3D-IC thermal simulation is too slow for early thermal-aware design. |
| mechanism | Layered analytical steady-state thermal solver with spectral decomposition, transfer matrices, and accelerated power decomposition. |
| workload | 3D-IC temperature distributions with complex boundaries, curved edges, fine-grained power maps, and standard-cell-level distributions. |
| hardware | UNKNOWN — not present in the current adjudicated record |
| baselines | COMSOL; DeepOHeat machine-learning thermal simulator |
| metrics | over four orders of magnitude speedup over COMSOL; below 0.5 K maximum absolute error; roughly 10X lower error than DeepOHeat; approximately 2000 slices per inference |
| limits | The description does not expose all geometry/material assumptions, absolute runtimes, or accuracy under transient rather than steady-state conditions. |
| locator | FLASH3D combines spectral modal decomposition, transfer matrices, and accelerated power decomposition; compared with COMSOL it reports over four orders of magnitude speedup, below 0.5 K maximum absolute error, and roughly 10X lower error than DeepOHeat while processing about 2000 slices per inference. |

[Historical source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH1065&sess=sess156)

</details>


Mapping review status: `not_recorded`; independent review status: `pending`.

## Tasa: Thermal-aware 3D-Stacked Architecture Design with Bandwidth Sharing for LLM Inference

- Paper ID: `iccad-2025-1103`
- Conference/edition: `iccad` / `2025`
- Evidence tier: `Primary arXiv preprint v3 and official ICCAD record; selected manuscript reading, simulator execution and independent acceptance not performed`
- Ledger record: `iccad/data/adjudicated-2025-batch.jsonl`

**Current evidence correction — 2026-09-08**

Reconciles the abstract card with arXiv version 3; separates simulated thermal analysis, heterogeneous core/floorplan choices, KV-cache bandwidth sharing, and end-to-end modeled speedups, preserving the simulator and threshold conditions.

Condition review of this correction and independent acceptance remain pending. The direction mapping is inherited, not revalidated by this update.

[Dated correction register](../../../data/editorial-paper-corrections-v1.json)

- Source: [https://arxiv.org/pdf/2508.07252v3](https://arxiv.org/pdf/2508.07252v3)

| Field | Current record |
|---|---|
| Problem | 3D-stacked DRAM over a logic die can increase memory bandwidth for autoregressive LLM decoding while increasing power density, thermal gradients, hotspot risk and scalability limits. |
| Mechanism / artifact | Tasa combines thermal-aware heterogeneous P-cores for GEMM/fully connected work and E-cores for memory-intensive GEMV/attention work with a hierarchical NoC, E-core placement exploration, adaptive KV-cache partitioning and bandwidth-sharing scheduling based on P-core utilization and batch size. |
| Workload / benchmark | LLaMA-65B and GPT-3 66B in FP16/BF16; ShareGPT conversational requests, dynamic stable batches and Poisson request arrivals for QPS tests; 48/60/72-core stacks, 3:1 and 5:1 P:E ratios, input/output length 512/512 and batch size 32 for thermal comparisons. |
| Hardware / process | Four DRAM dies over one logic die; 48 GB/stack, 768 banks/die, 16 banks/core, 128 KB SRAM/core, 1 GHz, 6 TB/s stack data rate, 32×32 systolic arrays in P-cores and 32×1 MAC-tree arrays in E-cores. Thermal threshold 85 °C with DVFS; modeled TIM/TSV, silicon, heat-sink and DRAM parameters; Timeloop, Accelergy/FinCACTI, Ramulator 2.0, HotSpot 6.0 and AttAcc-derived simulation, including ASAP7 logic estimates. |
| Baselines | Eight NVIDIA A100 40 GB GPUs; Eight A100 GPUs plus AttAcc PIM; Eight homogeneous 3D-stacked accelerators with the same overall Tasa configuration (Homo-3D) |
| Metrics | Thermal reduction versus Homo-3D at batch 32 and 512/512 input/output: average peak-temperature reduction 3.96 °C, 6.10 °C and 5.99 °C for 48, 60 and 72 cores; frequency-comparison ranges 3.63–5.55 °C, 5.73–9.37 °C and 5.12–7.91 °C.; Average throughput speedup in the 48-core evaluation: 2.85× over A100-only, 2.12× over A100+AttAcc and 1.33× over Homo-3D; up to 3.35× in a stated comparison. Average energy-efficiency improvement: 2.07× over A100-only and 1.61× over A100+AttAcc.; Thermal analysis baseline: 3D peak rises 23.3 °C from 24 to 72 cores versus 15.3 °C for 2D; increasing core spacing lowers peak by 10.32 °C at 2.25× area in the stated simulation. |
| Evidence locator / span | Version 3: Sections III–V pages 3–7 for thermal analysis, P/E cores and bandwidth sharing; Tables I–II pages 7–8 for hardware and thermal parameters; Sections VI-A–C pages 8–10 and Figures 11–14 for ShareGPT/Poisson evaluation, thermal reductions, throughput, energy efficiency and QPS latency; official ICCAD DOI 10.1109/ICCAD66269.2025.11240805. |
| Limits | All temperature, area, energy and throughput results are modeled with the stated HotSpot/Timeloop/Accelergy/Ramulator/AttAcc flow and thermal parameters; they are not fabricated-silicon or package measurements.; The 85 °C threshold and DVFS response, memory-stack cooling, thermal calibration, controller/migration overhead, process/library assumptions and manufacturing cost require independent verification. The simulated 361.79 °C logic-die peak should not be presented as a physical operating temperature.; The 2.85×/2.12×/1.33× comparisons combine heterogeneous cores, 3D bandwidth, thermal response, cache placement and bandwidth sharing; they do not isolate one mechanism or establish transfer to other models, traffic, stacks, cooling systems or baselines.; No simulator execution or independent reproduction was performed here; package feasibility and silicon validation remain open. |

<details markdown="1">
<summary>Historical captured record — superseded in the current table</summary>

Historical atlas evidence tier: `primary_preprint`.

| Field | Historical record |
|---|---|
| problem | 3D stacking increases memory bandwidth for autoregressive LLM decoding but creates more severe temperature, thermal-gradient, and scalability constraints than 2D designs. |
| mechanism | Heterogeneous 3D-stacked architecture with high-performance cores for compute-intensive operators, high-efficiency cores for memory-intensive attention operators, cross-stack thermal balancing, and bandwidth-sharing scheduling. |
| workload | Llama-65B and GPT-3 66B inference with 48-, 60-, and 72-core configurations; comparisons include GPU and heterogeneous PIM-based accelerators. |
| hardware | 3D-stacked multi-DRAM-die-over-logic architecture with thermal constraints and heterogeneous cores; technology, cooling, and memory-stack assumptions require full-paper verification. |
| baselines | homogeneous 3D-stacked architecture; GPU baselines; state-of-the-art heterogeneous PIM-based LLM accelerator |
| metrics | 5.55, 9.37, and 7.91 degree Celsius peak-temperature reductions; 2.85x Llama-65B inference speedup; 2.21x GPT-3 66B inference speedup; thermal scalability and bandwidth utilization |
| limits | The evidence is an author preprint abstract; full-paper verification is needed for thermal-model calibration, area/cost overhead, memory bandwidth assumptions, and comparison fairness. |
| locator | Tasa addresses the thermal limits of 3D-stacked architectures by combining heterogeneous high-performance and high-efficiency cores with cross-stack thermal optimization and bandwidth-sharing scheduling. The abstract reports peak-temperature reductions of 5.55, 9.37, and 7.91 degrees Celsius for 48, 60, and 72 core configurations, plus 2.85x and 2.21x speedups for Llama-65B and GPT-3 66B inference over GPU baselines and a heterogeneous PIM accelerator. |

[Historical source](https://arxiv.org/abs/2508.07252)

</details>


Mapping review status: `not_recorded`; independent review status: `pending`.

## Lit Silicon: A Case Where Thermal Imbalance Couples Concurrent Execution in Multiple GPUs

- Paper ID: `isca-2026-program-153`
- Conference/edition: `isca` / `2026`
- Evidence tier: `primary_preprint`
- Ledger record: `isca/data/adjudicated-2026-batch.jsonl`
- Source: [https://arxiv.org/abs/2511.09861](https://arxiv.org/abs/2511.09861)

| Field | Current record |
|---|---|
| Problem | Thermal imbalance across GPUs can create hotter, slower stragglers that slow cooler leader GPUs during overlapped computation and communication, reducing node-level efficiency. |
| Mechanism / artifact | Lit Silicon performance/power models, detection and mitigation techniques, and evaluation of TDP-constrained power optimization, node-level GPU power capping, and CPU power sloshing. |
| Workload / benchmark | Two workloads on two AMD Instinct MI300X GPU systems using two LLM training frameworks. |
| Hardware / process | Single-node multi-GPU LLM training with concurrent computation and communication; evidence is specific to evaluated AMD MI300X systems and management policies. |
| Baselines | unmitigated concurrent execution; alternative power-management strategies |
| Metrics | up to 6% performance improvement; up to 4% power improvement; thermal and node-level performance variation |
| Evidence locator / span | Lit Silicon identifies thermally induced straggling coupled with concurrent computation and communication as a source of multi-GPU performance variation. The study proposes analytical performance and power models, detection and mitigation techniques, and evaluates three power-management strategies on two AMD Instinct MI300X systems, two workloads, and two LLM-training frameworks. It reports up to 6% performance and 4% power improvements. |
| Limits | The evidence is an author preprint abstract; workload details, thermal traces, statistical variance, absolute energy, and the claimed datacenter cost implications require full-paper verification and broader hardware replication. |

Mapping review status: `not_recorded`; independent review status: `pending`.

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


Mapping review status: `researcher_reconciliation_not_independent`; independent review status: `pending`.

## Direction boundary

The evidence does not establish manufacturing readiness, a winning packaging technology, or generalization beyond evaluated geometry, materials, devices, and workloads.

Next evidence action: Compare selected and rejected candidates with held-out higher-fidelity solvers or measurements; report ranking error, violations, and search cost.
