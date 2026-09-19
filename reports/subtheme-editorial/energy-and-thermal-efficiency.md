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
