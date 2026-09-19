# Energy and thermal efficiency

This subject has 2 records in the selected sample. This page explains where it fits, then presents all captured paper evidence without shortening the measurements or limitations.

[Definitions used in the paper records](../reading-guide-v1.md)

## Understand the parent subject first

- [Power reliability and security](../themes/power-reliability-and-security.md)

## Power, energy, and temperature answer different questions

Power is the rate at which a system uses energy. Energy is the accumulated use over time. Temperature depends on where heat is produced, how it spreads, and how effectively it leaves the system. A lower peak temperature does not automatically mean less energy was used, and a lower power reading does not establish lower energy for a job that now runs longer.

For a constant-power example, energy equals power multiplied by duration. If a hypothetical workload uses 10% less power but takes 20% longer, its energy becomes 0.9 times 1.2, or 1.08 times the original. That is an 8% increase. This arithmetic is illustrative, not a result from either paper.

Spatial distribution also matters. Concentrating heat production in a small region can create a hot spot even when total chip power is unchanged. Conversely, two processors receiving the same power allowance can run at different temperatures because their cooling paths or operating characteristics differ. Thermal optimization therefore needs both the amount and location of power, plus the conditions under which heat escapes.

## Early thermal placement: predict before positions are final

Placement assigns circuit elements to physical positions. A power-density map estimates how much power is produced per unit area across those positions. Turning that map into temperature requires a thermal model, including the material and cooling conditions. Steady-state temperature describes the settled result under a sustained condition; it does not describe every short burst of activity.

[Early Design Stage Thermal Prediction and Optimization](../observed-subthemes/energy-and-thermal-efficiency.md#paper-dac-2026-research706) predicts power density during global placement, uses physics-guided interpolation for steady-state temperatures, and changes placement to reduce hot spots. The official description reports 49.0% better power-density prediction accuracy, 34.9% better thermal prediction accuracy, and a 9.97°C reduction in maximum temperature while retaining equivalent timing and area. It does not define the accuracy metrics, circuit suite, process, training split, or thermal boundary conditions. [Official thermal-placement description](https://63dac.conference-program.com/presentation/?id=RESEARCH706&sess=sess112).

Prediction improvement and physical improvement must stay separate. A better temperature estimate can reveal an existing hot spot without changing the circuit at all. A cooler predicted placement needs validation with an independent thermal calculation or measurement. Neither an undefined relative accuracy improvement nor a temperature difference supplies that validation by itself.

A useful comparison would hold the workload activity, package, ambient condition, timing target, and area budget fixed. It would check the final routed design because moving cells also changes wiring and its electrical costs. Reliability requires further evidence: a lower maximum temperature is relevant but is not a measured lifetime extension.

<span id="explanation-dac-2026-research706"></span>

## Early-stage ML thermal placement: a cooler prediction is not yet a cooler chip

Thermal behavior follows a chain from switching activity to power density, heat conduction and heat removal. Placement changes the spatial distribution of cells and therefore the location of power sources; wiring, package materials, heat spreaders, ambient conditions and cooling boundaries determine how that distribution becomes temperature. Peak steady-state temperature is only one outcome and is distinct from transient temperature, energy, electromigration and lifetime.

The described framework has three stages. It predicts a power-density map during global placement, interpolates a steady-state thermal map with physics guidance, and uses an ML optimization engine to change placement while attempting to preserve timing. This can move thermal reasoning earlier in the physical-design loop. It does not make the learned power map an activity measurement, the interpolated map a full thermal solver, or a placement objective a guarantee about the routed and packaged design.

The first gate is prediction fidelity. Define the power quantity, spatial resolution, activity and workload assumptions, thermal state, reference solver or measurement, and whether the test set contains unseen designs, placements, technologies and operating conditions. Report absolute error, bias, hotspot recall, maximum-temperature error and spatial error—not only a relative “accuracy improvement.” A model can improve an aggregate score while missing the local hotspot that controls reliability.

The second gate is closed-loop physical validity. After optimization, legalize and route the placement, update parasitics and power, and recompute thermal behavior with the same package, ambient, voltage, frequency, process and temperature assumptions. Check timing, congestion, wirelength, area, power, IR drop, electromigration and thermal cycling. If timing remains equivalent only under a surrogate or an early placement estimate, the claim is not timing closure.

The reported results claim 49.0% and 34.9% prediction-accuracy improvements over tool estimation, a 9.97°C maximum-temperature reduction, and equivalent timing and area. The official description does not define the accuracy metrics, designs, technology, training split, activity traces, thermal boundary, reference tool, timing corners or final-route validation. The evidence supports early ML-assisted thermal prediction and placement optimization, not demonstrated package- or silicon-level thermal reliability improvement.

## Lit Silicon: one GPU's temperature can affect other GPUs' progress

Parallel training divides work across processors that must exchange results. A processor arriving early at a required exchange cannot always proceed independently. Meanwhile, communication and computation can share local resources. It is therefore necessary to inspect the interaction between processors rather than optimize each one's isolated execution rate.

[Lit Silicon](../observed-subthemes/energy-and-thermal-efficiency.md#paper-isca-2026-program-153) links thermal imbalance to interference during overlapped computation and communication. Section V adjusts individual GPU power caps; Table I distinguishes reducing faster GPUs' power, reallocating GPU power, and transferring CPU power allowance to GPUs.

Section VI evaluates two nodes, each with eight MI300X GPUs and two EPYC 9684X CPUs, using Llama 3.1 8B and Mistral 7B with FSDP variants. Section VII-A's default cases report 4% lower average GPU power without throughput change, 3% higher throughput with GPU reallocation, and 4% higher throughput with 3% more GPU power under CPU reallocation. These are different policies, not simultaneous benefits to combine.

Table III's predicted throughput factors are 1.06 and 1.10 for the two reallocation cases, versus measured 1.03 and 1.04. Figure 9 defines throughput through summed kernel durations. These results do not directly establish complete-training energy savings, facility power savings, or dollar savings. [Version-1 manuscript, Tables I–III and Sections V–VII](https://arxiv.org/html/2511.09861v1).

## Why power allocation needs a system boundary

Reducing a fast participant's power can be useful if it still reaches the required synchronization point in time. If the reduction makes it the new slow participant, overall completion can worsen. A controller must therefore detect the current limiting participant and account for the time taken to change settings and observe the response.

Moving a power allowance is also not equivalent to moving consumed energy. An unused CPU budget need not represent that much actual CPU power draw. Measure the CPU, GPU, and relevant other components before claiming node-level savings. Cooling and power-conversion losses introduce another boundary when extending the claim to a facility.

The thermal condition must be stable enough for a comparison, or its evolution must be recorded. Compare warm-up periods, workload phases, and repeated runs. A brief trace can capture a favorable transition without representing sustained behavior. Conversely, a controller that needs time to settle can look ineffective if evaluation stops too early.

## Cross-paper interpretation and evidence status

The two papers act at different times: one changes a design before fabrication, while the other changes operation on existing hardware. My synthesis is that thermal behavior belongs in the decision process at both stages. They do not establish one common optimization algorithm or a universal benefit from machine learning.

The source check on 2026-09-07 recovered section- and table-backed conditions from Lit Silicon's November 2025 preprint version associated with the ISCA record. Equivalence to the final conference version remains unchecked. The placement paper remains official-description evidence. Its missing manuscript conditions, Lit Silicon's broader hardware applicability, and a comparable multi-edition trend analysis remain open; neither article count nor a successful browser render closes those gaps.

## Compare the results carefully

First identify the inputs and required output quality. Then identify the limited resource: time, memory, communication, energy, circuit area, or correctness coverage. Ask which part of the method reduces that cost and which new cost it adds. Compare numbers only when the experiments hold these conditions sufficiently similar.

A conference description may explain the proposal while omitting the full experiment. An author preprint link may have been coded from its abstract. The source classification does not by itself establish that every table was read. Missing locations remain visible below.

## Complete captured evidence

These are evidence records, not substitutes for the explanations above. Each record preserves its problem, proposed method, measurements, comparison conditions, and source limits. A populated record does not establish that its mechanism has been fully explained or independently verified.

<span id="paper-dac-2026-research706"></span>

### Early Design Stage Thermal Prediction and Optimization: Machine-Learning Driven Approach

DAC 2026 · Record: `dac-2026-research706`

[Read the step-by-step explanation](#explanation-dac-2026-research706)

**Updated source-backed reading card**

Reviewed 2026-09-08. Deepens the existing early thermal-placement treatment into a paper-level reading; separates ML power-density prediction, physics-guided thermal interpolation and placement optimization from activity modeling, thermal-boundary fidelity, routed-design timing and physical reliability, preserves the 49.0%, 34.9% and 9.97-degree claims, and makes validation boundaries explicit.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Advanced-node power density makes thermal behavior a first-order physical-design concern, while early thermal estimates can be inaccurate and late mitigation can be costly.

**Mechanism / artifact:**

ML power-density prediction during global placement, physics-guided interpolation of steady-state temperature, and ML-driven placement optimization to reduce hotspots while targeting unchanged timing; model inputs, reference solver, objective and update loop are unspecified.

**Workload — the work tested:**

Modern SoC placement and thermal prediction/optimization; circuits, netlists, technology node, activity traces, power maps, training/test split, placement constraints, timing corners and package conditions are unspecified.

**Hardware and manufacturing assumptions:**

ASIC physical-design flow with global placement, thermal modeling and timing evaluation; PDK, cell library, parasitics, package/material stack, cooling, ambient, voltage/frequency, process/temperature corners and final-route/signoff tools are unspecified.

**Baseline — the comparison method:**

Tool power/thermal estimation

Thermal-aware coarse-grained floorplanning

Post-route thermal-aware cell adjustment

Same designs, activity, package, ambient, timing target, area budget, technology, reference solver, routing/extraction flow and measurement boundary are unspecified

**Reported measurements:**

The official description reports 49.0% power-density prediction-accuracy improvement, 34.9% thermal prediction-accuracy improvement, 9.97 degrees Celsius lower maximum temperature, and equivalent timing and area; it supplies no metric definitions, absolute errors, hotspot recall, design values, corners or routed/signoff validation.

**Limits on the conclusion:**

Prediction accuracy must be defined against an independent thermal/power reference with spatial and hotspot errors, unseen designs/placements, activity, technology and operating conditions. Aggregate accuracy can improve while the reliability-critical hotspot is missed.

A placement that is cooler under an early surrogate must be legalized, routed and reevaluated with updated parasitics, power, package, ambient, voltage, frequency, process and temperature assumptions. Check timing closure, congestion, wirelength, area, power, IR drop, electromigration and thermal cycling.

The 49.0%, 34.9% and 9.97-degree claims lack designs, technology, training split, activity, accuracy definitions, thermal boundaries, reference tool, corners and final-route conditions. The evidence supports early ML-assisted thermal prediction and placement optimization, not demonstrated package- or silicon-level thermal reliability improvement.

**Source and location**

Evidence tier: Primary captured DAC official description plus existing chapter level conceptual discussion; no full paper extraction, thermal trace, routed validation or independent review. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH706&sess=sess112)

DAC 2026 official description; existing chapter-level early thermal-placement discussion; captured Problem, Mechanism / artifact, Workload, Hardware, Baseline, Measurements and Limits fields; no manuscript pages or reproduced thermal-placement run.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** tool thermal/power estimation

thermal-aware coarse floorplanning

post-route cell adjustment

**Evidence locators:** Not established in the captured evidence.

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH706&sess=sess112

**Hardware or process assumptions:** Not established in the captured evidence.

**Limits:** The description does not define accuracy metrics, circuits, technology, training data, timing constraints, or transfer across placements; claimed reliability improvements need full-paper validation.

**Method or artifact:** ML power-density prediction, physics-guided thermal-map interpolation, and ML-driven placement optimization for early thermal mitigation.

**Metrics:** 49.0% power-density prediction-accuracy improvement

34.9% thermal prediction-accuracy improvement

9.97 degree Celsius maximum-temperature reduction

equivalent timing and area

**Problem:** Advanced-node power density makes thermal effects first-order, but traditional thermal mitigation is inaccurate early or expensive after fabrication/post-route.

**Workload or benchmark:** Modern SoC physical-design placement and thermal prediction/optimization; exact circuit suites and technology nodes require paper-level extraction.

</details>

<span id="paper-isca-2026-program-153"></span>

### Lit Silicon: A Case Where Thermal Imbalance Couples Concurrent Execution in Multiple GPUs

ISCA 2026 · Record: `isca-2026-program-153`

**Problem:**

Thermal imbalance across GPUs can create hotter, slower stragglers that slow cooler leader GPUs during overlapped computation and communication, reducing node-level efficiency.

**Mechanism / artifact:**

Lit Silicon performance/power models, detection and mitigation techniques, and evaluation of TDP-constrained power optimization, node-level GPU power capping, and CPU power sloshing.

**Workload — the work tested:**

Two workloads on two AMD Instinct MI300X GPU systems using two LLM training frameworks.

**Hardware and manufacturing assumptions:**

Single-node multi-GPU LLM training with concurrent computation and communication; evidence is specific to evaluated AMD MI300X systems and management policies.

**Baseline — the comparison method:**

unmitigated concurrent execution

alternative power-management strategies

**Reported measurements:**

up to 6% performance improvement

up to 4% power improvement

thermal and node-level performance variation

**Limits on the conclusion:**

The evidence is an author preprint abstract; workload details, thermal traces, statistical variance, absolute energy, and the claimed datacenter cost implications require full-paper verification and broader hardware replication.

**Source and location**

Evidence tier: High primary preprint. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://arxiv.org/abs/2511.09861)

An exact page, section, or table location has not been recorded. Page-level verification remains open.

## What remains to establish

Resolve unspecified workloads, comparison methods, resource budgets, and source locations before generalizing a reported gain. Multiple papers in this selected sample permit comparison of mechanisms, but do not by themselves establish recurrence across years or a long-term trend.

[All subthemes](../expanded-taxonomy-v1.md) · [Research directions](../directions/README.md)
