# Evidence dossier — Reliability Security Upstream

This dossier combines the canonical direction atlas, historical adjudicated records, and dated editorial corrections. It is a source-backed reading aid, not an independent review or a claim that the records are comparable.

- Direction page: [Reliability Security Upstream](../04-reliability-security-upstream.md)
- Source direction IDs: `reliability-security-design-loop`
- Direction status: `provisional_mechanism_hypothesis`
- Independent reviews recorded: `0`

## Reading rule

`UNKNOWN` means a field is not recorded, not that the paper lacks the condition. Corrections supersede the current displayed fields while historical fields remain expandable. A historical condition-complete label does not establish that a correction has passed condition or independent review.

## Strix: Re-Thinking NPU Reliability from a System Perspective

- Paper ID: `dac-2026-research043`
- Conference/edition: `dac` / `2026`
- Evidence tier: `Primary arXiv v1 preprint plus page-level assessment and table check; no independent execution, silicon validation or safety acceptance`
- Ledger record: `dac/data/adjudicated-2026-batch.jsonl`

**Current evidence correction — 2026-09-08**

Reconciles the Strix card with the recovered arXiv v1 assessment and visual Table 1 check; separates full-stack targeted safeguards from monolithic replication, detection from correction, FPGA/simulation conditions, synthesized overhead from silicon, and fault-injection coverage from safety acceptance.

Condition review of this correction and independent acceptance remain pending. The direction mapping is inherited, not revalidated by this update.

[Dated correction register](../../../data/editorial-paper-corrections-v1.json)

- Source: [https://arxiv.org/html/2604.10484v1](https://arxiv.org/html/2604.10484v1)

| Field | Current record |
|---|---|
| Problem | DNN and LLM accelerators are increasingly used in safety-relevant settings while technology scaling and model complexity increase fault exposure; monolithic NPU replication can impose high overhead and remain difficult to deploy. |
| Mechanism / artifact | Strix partitions the NPU along the inference pipeline, identifies dominant failure modes, and attaches targeted safeguards across microarchitecture, ISA and programming. The recovered comparison includes area-matched partial TMR, triple-instruction redundancy and ReaLM with rollback limit one. |
| Workload / benchmark | DNN and LLM inference on an open-source SoC/NPU; selected assessment conditions use first 1,000 dataset samples and 10 runs, transient bit flips and permanent stuck-at faults at default rate 10⁻⁷ over original-input bit count. BF16-I uses PyTorch following Spike behavior for LLM performance analysis rather than the same FPGA path. |
| Hardware / process | Gemmini base, AMD VU19P FPGA and 20 cluster nodes for the recorded platform; synthesis estimates use Design Compiler 2019.12 and TSMC 28 nm. Recorded latency configurations are INT8-D, INT8-I and FP32-D at 500 MHz; BF16-I is absent from the latency table. |
| Baselines | Area-matched partial TMR; Triple-instruction redundancy; ReaLM with rollback limit one |
| Metrics | Recorded geometric-mean slowdown is 1.04× with range 1.02×–1.07× under the Section 5 conditions.; Recorded worst-case detection latency is below 1 microsecond at 500 MHz for INT8-D, INT8-I and FP32-D; the assessment explicitly says this is not a measured correction-latency bound and BF16-I is absent.; Synthesis-estimated area/power percentage pairs: FP32-D 10.2/21.3, INT8-D 20.7/23.2 and INT8-I 8.7/16.8, using the recorded Design Compiler/TSMC 28 nm conditions. |
| Evidence locator / span | Recovered arXiv v1 HTML Section 5 for fault model, platforms, baselines, slowdown, latency and synthesis conditions; visually checked PDF Table 1 page 6 for INT8-D/INT8-I/FP32-D detection-latency rows; saved assessment dac/data/strix-primary-assessment-v1.json and data/review-packets/dac-2026-research043.json preserve the source hash, scope and limits. |
| Limits | Fault localization, detection, correction and useful inference are different outcomes. A detection-latency bound does not establish correction latency or restored application output.; Transient bit flips and permanent stuck-at faults at the recorded injection rate and denominator do not cover all physical, temporal, correlated or workload-dependent fault modes.; BF16-I LLM analysis uses PyTorch following Spike behavior, while other conditions use Gemmini/FPGA or synthesis paths; these must not be combined into one hardware validation claim.; Synthesis estimates are not fabricated-silicon measurements. Fault-injection coverage does not establish functional-safety certification, universal workload behavior or coverage of every fault model; implementation revisions, figure denominators and variance remain open. |

<details markdown="1">
<summary>Historical captured record — superseded in the current table</summary>

Historical atlas evidence tier: `official_description`.

| Field | Historical record |
|---|---|
| problem | Monolithic NPU replication creates prohibitive overhead while failing to provide deployable reliability for increasingly fault-prone accelerators. |
| mechanism | Full-stack reliability framework with pipeline-level fault-mode analysis and targeted safeguards across microarchitecture, ISA, and programming. |
| workload | DNN and LLM inference on an open-source SoC NPU, including safety-oriented fault scenarios. |
| hardware | UNKNOWN — not present in the current adjudicated record |
| baselines | coarse-grained monolithic NPU replication mechanisms |
| metrics | sub-microsecond fault localization, detection, and correction; 1.04X slowdown; minimal hardware overhead |
| limits | The description does not specify fault model coverage, workload set, reliability guarantee, or exact hardware overhead. |
| locator | Strix spans NPU microarchitecture, ISA, and programming on an open-source SoC, partitions safeguards along the inference pipeline, and reports sub-microsecond fault localization/detection/correction with 1.04X slowdown and minimal hardware overhead. |

[Historical source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH043&sess=sess171)

</details>


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

## Icarus's Wings: Disabling MoE Offloading Acceleration via a Universal Hidden Prefix Attack

- Paper ID: `dac-2026-research1054`
- Conference/edition: `dac` / `2026`
- Evidence tier: `Primary captured official DAC description plus pinned repository artifact-discovery assessment; no recovered full paper, executable attack, reproduced offloading system or independent validation`
- Ledger record: `dac/data/adjudicated-2026-batch.jsonl`

**Current evidence correction — 2026-09-08**

Deepens the existing Icarus’s Wings treatment into a paper-level reading; separates prefix construction, routing/prefetch disruption, cache replacement and victim slowdown, and incorporates the artifact-discovery limit while making attacker control, baselines, universality, metrics and adaptive defense explicit.

Condition review of this correction and independent acceptance remain pending. The direction mapping is inherited, not revalidated by this update.

[Dated correction register](../../../data/editorial-paper-corrections-v1.json)

- Source: [https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH1054&sess=sess156](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH1054&sess=sess156)

| Field | Current record |
|---|---|
| Problem | MoE offloading optimizations assume temporal locality and predictable routing, creating a denial-of-service surface when wrong experts are prefetched. |
| Mechanism / artifact | Gradient-based universal hidden-prefix attack combining temporal-locality minimization, expert-prefetch misleading, and a target-balancing scheduler; prefix constraints, gradient/query access, scheduler control and offloading implementation are unspecified. |
| Workload / benchmark | Multi-user MoE inference across models and devices with GPU-centric expert offloading; model/checkpoint, expert count, router, device, memory capacity, request mix, sequence length, concurrency, output condition and split are unspecified. |
| Hardware / process | GPU-centric MoE offloading system; GPU, host memory/interconnect, cache capacity, scheduler, prefetch policy, driver/runtime, tenant isolation and attacker privileges are unspecified. |
| Baselines | MoE caching and prefetching assumptions; Unattacked MoE offloading; Random/ordinary prefixes, alternate offload policies, same model/device/memory/concurrency/output and attacker-cost boundary are unspecified |
| Metrics | 85.4% increase in cache replacements, 12.5% reduction in prefetch accuracy, 0.7X decoding speed and maximum-length outputs are reported; no absolute latency/throughput, victim tail latency, attack cost, success rate, traffic, transfer, model/device matrix or defense result is supplied. |
| Evidence locator / span | DAC 2026 official description; captured Problem, Mechanism / artifact, Workload, Hardware, Baseline, Measurements and Limits fields; record RESEARCH1054; additional assessment dac/data/icarus-source-recovery-20260906.json and pinned repository README; no full-paper page locator. |
| Limits | An MoE denial-of-service claim requires a causal link from hidden-prefix construction to routing/prefetch decisions, cache replacement and victim service degradation. Replacement and prefetch metrics are not themselves victim-impact metrics, and 0.7X needs a defined speed/latency denominator.; Universality must be tested across held-out prompts, users, sequence lengths, checkpoints, expert counts, routing policies, devices, offloaders and schedules; attacker knowledge, prefix length, gradient/query cost and scheduler control must be stated.; The description does not enumerate models/devices, attack cost, attack success rate, or defenses. The pinned repository contains README/image artifact discovery only; no full paper or demo execution was recovered. The evidence supports an MoE offloading denial-of-service direction, not demonstrated universal or deployment-general attack impact. |

<details markdown="1">
<summary>Historical captured record — superseded in the current table</summary>

Historical atlas evidence tier: `official_description`.

| Field | Historical record |
|---|---|
| problem | MoE offloading optimizations assume temporal locality and predictable routing, creating a denial-of-service surface when wrong experts are prefetched. |
| mechanism | Gradient-based universal hidden-prefix attack combining temporal-locality minimization, expert-prefetch misleading, and a target-balancing scheduler. |
| workload | Multi-user MoE inference across models and devices with GPU-centric expert offloading. |
| hardware | UNKNOWN — not present in the current adjudicated record |
| baselines | MoE caching and prefetching assumptions; unattacked MoE offloading |
| metrics | 85.4% increase in cache replacements; 12.5% reduction in prefetch accuracy; 0.7X decoding speed; maximum-length outputs |
| limits | The description does not enumerate models/devices, attack cost, attack success rate, or defenses. |
| locator | Icarus attacks GPU-centric MoE expert caching and prefetching with adversarial prefixes, increasing cache replacements by 85.4%, reducing prefetch accuracy by 12.5%, slowing decoding to 0.7X, and driving outputs to maximum length. |

[Historical source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH1054&sess=sess156)

</details>


Mapping review status: `not_recorded`; independent review status: `pending`.

## Cerberus: Cross-Layer ECC Co-Design for Robust and Efficient Memory Protection

- Paper ID: `isca-2026-program-004`
- Conference/edition: `isca` / `2026`
- Evidence tier: `Author preprint v1; selected method and evaluation sections inspected`
- Ledger record: `isca/data/adjudicated-2026-batch-2.jsonl`

**Current evidence correction — 2026-09-07**

Expanded inspection from abstract to version-pinned method and evaluation sections.

Condition review of this correction and independent acceptance remain pending. The direction mapping is inherited, not revalidated by this update.

[Dated correction register](../../../data/editorial-paper-corrections-v1.json)

- Source: [https://arxiv.org/pdf/2605.02220v1](https://arxiv.org/pdf/2605.02220v1)

| Field | Current record |
|---|---|
| Problem | Composition of memory-protection stages. |
| Mechanism / artifact | Shared encoding with bounded local correction and controller recovery. |
| Workload / benchmark | Scenario-conditioned random fault injection; simulated GPU workloads. |
| Hardware / process | V100-derived/HBM4 simulation; modeled energy, not device measurements. |
| Baselines | Unity ECC, DUO, and layered LPDDR6/HBM4 configurations. |
| Metrics | 32-bit configuration: 0.7% geometric-mean IPC improvement. Correction/detection depend on fault scenario and retry assumptions. |
| Evidence locator / span | PDF pp. 7–9 method; pp. 10–11 fault evaluation; pp. 12–13 performance/energy. |
| Limits | Link-detected failures count as recovered through retry; normal-path timing omits rare correction. Reproduction and final-proceedings equivalence unverified. |

<details markdown="1">
<summary>Historical captured record — superseded in the current table</summary>

Historical atlas evidence tier: `primary_preprint`.

| Field | Historical record |
|---|---|
| problem | Independent evolution of on-die, link, and system ECC creates duplicated redundancy, gaps, and cross-layer interference as DRAM density and I/O speed increase. |
| mechanism | A cross-layer ECC architecture using Encode-Once, Decode-Many, complementary parity and syndrome structures, ordered decoding, and a correction budget that coordinates recovery across the memory stack. |
| workload | Fault-injection and memory-protection evaluation for clustered and peripheral memory faults, with an HBM-oriented context; exact fault distributions and workloads require full-paper verification. |
| hardware | Dense high-speed DRAM and HBM-style memory stacks with on-die, link, and system ECC layers; results depend on the assumed fault model, interface organization, and controller/device cooperation. |
| baselines | independently layered on-die, link, and system ECC; conventional multi-layer memory-protection designs |
| metrics | resilience to clustered faults; resilience to peripheral faults; redundant protection overhead; mis-correction amplification control |
| limits | The evidence is an author preprint abstract; exact codeword layouts, fault-model probabilities, decoder latency, area/energy overhead, HBM generation, and quantitative baseline tables must be extracted from the full paper before making deployment or superiority claims. |
| locator | Cerberus co-designs on-die ECC, link ECC, and system ECC for dense, high-speed DRAM. Its Encode-Once, Decode-Many design reuses controller encoding for link-level write detection/retry, device repair on reads, and system-level end-to-end recovery. The paper combines complementary parity/syndrome structures, decoder ordering, and a correction budget intended to avoid miscorrection amplification and reports improved resilience to clustered and peripheral faults with reduced redundant overhead in an HBM context. |

[Historical source](https://arxiv.org/abs/2605.02220)

</details>


Mapping review status: `not_recorded`; independent review status: `pending`.

## ECC Enabled Reliable and Performant Processing-in-Memory

- Paper ID: `isca-2026-program-009`
- Conference/edition: `isca` / `2026`
- Evidence tier: `institutional_abstract`
- Ledger record: `isca/data/adjudicated-2026-batch-5.jsonl`
- Source: [https://cris.technion.ac.il/en/publications/ecc-enabled-reliable-and-performant-processing-in-memory/](https://cris.technion.ac.il/en/publications/ecc-enabled-reliable-and-performant-processing-in-memory/)

| Field | Current record |
|---|---|
| Problem | Processing-in-memory improves data locality but introduces reliability risks from variable-retention-time scaling errors, physical faults, and multi-bit errors that can cause silent data corruption or repeated rank-level correction overhead. |
| Mechanism / artifact | A reliable bank-PIM architecture with tailored rank-level ECC, Codeword Flip masking for VRT weak cells, and odd-even bank pipelining to preserve utilization while limiting correction interference. |
| Workload / benchmark | PIM microbenchmarks and end-to-end LLM application evaluation; the institutional abstract reports comparisons with rankPIM and traditional bank-PIM. |
| Hardware / process | Bank-level PIM integrated with modern DRAM, variable-retention-time weak cells, rank-level correction, and an odd-even bank pipeline; exact DRAM generation, fault distributions, and implementation cost require full-paper verification. |
| Baselines | traditional bank-PIM configuration; rankPIM |
| Metrics | 90% PIM-unit utilization; up to 400x lower five-year silent-data-corruption likelihood; potential 4x performance enhancement over rankPIM in selected microbenchmarks; end-to-end LLM performance improvement |
| Evidence locator / span | The institutional publication record describes a reliable bank-PIM architecture with tailored ECC for variable-retention-time scaling errors and multi-bit errors. It detects multi-bit errors and corrects at rank level while avoiding repetitive correction cost, uses a Codeword Flip method to mask VRT weak-cell errors, and applies odd-even bank pipelining. The abstract reports 90% PIM-unit utilization, up to 400x lower silent-data-corruption likelihood than traditional bank-PIM over five years, and potential 4x performance enhancement over rankPIM in selected microbenchmarks, with end-to-end LLM improvements. |
| Limits | The evidence is an institutional publication record containing the abstract and DOI metadata, not a captured full paper. Exact ECC layouts, fault probabilities, correction latency, area/energy overhead, LLM configurations, and the meaning of the reported likelihood horizon require full-paper verification. |

Mapping review status: `not_recorded`; independent review status: `pending`.

## PuDGhost: Experimental Analysis of Computation Result Corruption in Processing-using-DRAM Operations on Real DRAM Chips and Implications for Future Systems

- Paper ID: `isca-2026-program-024`
- Conference/edition: `isca` / `2026`
- Evidence tier: `primary_preprint`
- Ledger record: `isca/data/adjudicated-2026-batch-4.jsonl`
- Source: [https://arxiv.org/abs/2606.19119](https://arxiv.org/abs/2606.19119)

| Field | Current record |
|---|---|
| Problem | Processing-using-DRAM assumes that each column's computation depends only on its own operands, but density scaling and neighboring-cell interference may violate that isolation and corrupt results. |
| Mechanism / artifact | Empirical characterization of PuDGhost under simultaneous multiple-row activation, followed by cross-layer countermeasures including unreliable-column screening and compute-row layouts that separate active computation rows. |
| Workload / benchmark | Processing-using-DRAM operations on real DDR4 chips, including random-input experiments and computation-accuracy evaluation; the abstract identifies matrix-vector multiplication as a target workload context. |
| Hardware / process | Real DDR4 DRAM using simultaneous multiple-row activation; results depend on chip organization, density, row layout, input patterns, and operating conditions. |
| Baselines | ideal column-isolated processing-using-DRAM behavior; uncorrected PuD operation without PuDGhost countermeasures |
| Metrics | 96 real DDR4 DRAM chips; 12 DRAM modules; up to 10% output impact from adjacent non-activated rows; up to 48% output impact from concurrently computing columns; computation accuracy after countermeasures |
| Evidence locator / span | PuDGhost reveals that processing-using-DRAM operations based on simultaneous multiple-row activation can be corrupted by data in non-activated adjacent rows and by data in other columns computing concurrently. The study characterizes the phenomenon on 96 real DDR4 DRAM chips from 12 modules, finding up to 10% output impact from adjacent non-activated rows and up to 48% from concurrently computing columns for random inputs. It evaluates robust column screening and a compute-row layout with dedicated rows between compute rows as countermeasures on real chips. |
| Limits | The evidence is an author preprint abstract; exact chip part numbers, voltage and temperature sweeps, full workload accuracy tables, screening cost, row-layout capacity cost, and transfer to other DRAM generations or PIM mechanisms require full-paper verification. |

Mapping review status: `not_recorded`; independent review status: `pending`.

## Energon: Unveiling Transformers from GPU Power and Thermal Side-Channels

- Paper ID: `iccad-2025-1000`
- Conference/edition: `iccad` / `2025`
- Evidence tier: `Primary arXiv preprint v1 and official ICCAD record; selected manuscript reading, execution and independent acceptance not performed`
- Ledger record: `iccad/data/adjudicated-2025-batch.jsonl`

**Current evidence correction — 2026-09-08**

Reconciles the captured abstract card with arXiv v1; separates sensor observation, threat model, architecture classification, surrogate/transfer attack and selected GPU conditions.

Condition review of this correction and independent acceptance remain pending. The direction mapping is inherited, not revalidated by this update.

[Dated correction register](../../../data/editorial-paper-corrections-v1.json)

- Source: [https://arxiv.org/pdf/2508.01768v1](https://arxiv.org/pdf/2508.01768v1)

| Field | Current record |
|---|---|
| Problem | Shared/virtualized GPUs expose power/thermal telemetry that may leak proprietary transformer architecture without direct model access. |
| Mechanism / artifact | Energon collects nvidia-smi/pynvml power/thermal traces and trains CNN classifiers to infer transformer family, encoder/decoder layers and attention heads; it uses extracted structure to build a MarianMT substitute and ViT transfer attacks. |
| Workload / benchmark | Custom transformers (nine configurations), eight pre-trained language models across T5/Google/MarianMT/Meta, eight ViTs across Apple/Google/Meta/Microsoft, NVIDIA A40 main platform, GTX 1660 Ti Mobile gradient analysis, single and noisy multi-process settings; 100 traces/model, 120s, 7Hz, 80:20 split and stratified K-fold. |
| Hardware / process | NVIDIA GPU physical power/thermal sensors visible to an unprivileged user via nvidia-smi/pynvml under the stated MIG/VM threat model; initial 28C and cooling between laboratory traces; device/driver/sampling/virtualization details constrain transfer. |
| Baselines | Custom transformer architecture configurations; Pre-trained language-family and ViT-family classifiers; Concurrent matrix multiplication/CNN/ViT background processes |
| Metrics | Custom head ID: 100% for 8/32-head groups and 96.25% for 16-head group; language family max/average 95%/89%; T5 head and Meta E/D 100% average.; ViT root family max/average 91.25%/84.75%; family-specific Meta/Google/Microsoft head ID 100%.; Noisy: 89.25% average root family ID; Meta/T5 92%/87%; matrix-multiplication background causes 4% root-family drop.; Substitute MarianMT BLEU 44.12 and BERT 93.53 (alternative unknown dimensions BERT 93.08/93.53); ViT FGSM/PGD success rates 83.38%, 94.87%, 98.63%, 98.63%. |
| Evidence locator / span | Version 1: Sections III–V and VII; custom traces and 7Hz/28C/cooling Section III-A pages 3–4; A40 120s power/thermal traces Sections III-B–C pages 4–5; threat model Section IV-A pages 5–6; 100 traces/80:20/K-fold and classifier Section IV-B pages 6–8; noisy processes Section IV-C pages 8–9; substitute/transfer Section V pages 9–10; mitigation/conclusion Section VII pages 10–11; ICCAD DOI 10.1109/ICCAD66269.2025.11240664. |
| Limits | Architecture classification is not weight/training-data recovery; selected families/configuration catalog and prior family conditioning limit generalization.; Sensor visibility and cross-instance correlation are threat-model assumptions; results are device/driver/sampling/MIG/cloud-policy dependent.; 100 traces/model with 80:20 split and selected models does not establish performance on unseen architecture families, GPUs or continuous production traffic; cooling/stabilization protocol is laboratory-specific.; Substitute/transfer results depend on training/data/attack definitions and do not establish universal attack success. No independent reproduction performed here. |

<details markdown="1">
<summary>Historical captured record — superseded in the current table</summary>

Historical atlas evidence tier: `author_pdf`.

| Field | Historical record |
|---|---|
| problem | Shared or virtualized GPUs expose power and thermal telemetry that may leak proprietary transformer architecture information without physical access. |
| mechanism | CNN-based predictors over power and thermal traces to infer transformer family, layer, and attention-head information, followed by substitute-model construction and black-box transfer attacks. |
| workload | Eight publicly available language/vision model families, custom transformers, NVIDIA A40 data-center GPU inference, single-process and noisy multi-process settings. |
| hardware | UNKNOWN — not present in the current adjudicated record |
| baselines | model-family and hyperparameter classification scenarios; noisy multi-process inference conditions |
| metrics | over 89% average model-family identification accuracy; 100% hyperparameter classification in reported settings; over 93% average transfer-attack success in abstract; BERT score above 93 for substitute-model evaluation |
| limits | The evidence is an author preprint and the repository does not yet extract every table or repeat the experiments; telemetry access, GPU generation, co-tenancy assumptions, and mitigation effectiveness constrain generalization. |
| locator | The paper investigates GPU power and thermal fluctuations as side channels for extracting transformer architectural details. It evaluates public language and vision transformers, reports over 89% average model-family identification accuracy and 100% hyperparameter classification in the abstract, and demonstrates transfer attacks with average success above 93%; the paper also describes a user-privilege threat model and responsible disclosure to NVIDIA. |

[Historical source](https://arxiv.org/abs/2508.01768)

</details>


Mapping review status: `researcher_reconciliation_not_independent`; independent review status: `pending`.

## Direction boundary

Threat, fault, thermal, and physical-integrity models are distinct and cannot be reduced to one robustness score.

Next evidence action: Require threat/fault model, coverage, false negatives, recovery path, and useful performance after protection for each anchor.
