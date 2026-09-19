# 3d integration and thermal management

This subject has 6 records in the selected sample. This page explains where it fits, then presents all captured paper evidence without shortening the measurements or limitations.

[Definitions used in the paper records](../reading-guide-v1.md)

## Understand the parent subject first

- [Chiplets 3d and packaging](../themes/chiplets-3d-and-packaging.md)

## Building a usable stack, not just a compact arrangement

A three-dimensional chip divides circuitry among layers and connects those layers vertically. This adds choices that do not exist in a single-layer placement: which layer owns each function, where a signal crosses layers, and whether the connection locations fit the bonding structure. A shorter geometric distance is only useful if the resulting circuit can be connected, clocked, powered, cooled, and manufactured.

This subject's six records mainly concern construction of that physical implementation. The neighboring [stacking and thermal-management article](../observed-subthemes/3d-stacking-and-thermal-management.md) mainly concerns temperature prediction and operating policies. These labels overlap; they are retained to make the existing classification reviewable, not to assert that they are separate established fields.

## Early partitioning and detailed placement make different commitments

Partitioning chooses which circuitry belongs on each layer. Placement assigns locations within those layers. An early decision sees a less detailed design but can avoid expensive changes later. A late decision sees more realistic wire and cell information, but much of the structure is already fixed.

[RTL-3D](../observed-subthemes/3d-integration-and-thermal-management.md#paper-dac-2026-research793) chooses layers using timing estimates before synthesis, the step that turns a behavioral hardware description into a network of implementation cells. The conceptual risk is estimation error: a path judged important early may change when logic is transformed and actual wires are introduced. The captured record gives no timing, link-count, or implementation results. The appropriate test is whether early choices remain useful after the same complete implementation flow, including any corrective work.

<span id="explanation-dac-2026-research793"></span>

### RTL-3D: early tier partitioning is a prediction problem before it is a placement result

### What tier partitioning decides

A 3D IC divides a design among physical tiers. Tier partitioning assigns selected logic or registers to those tiers and determines which signals must cross between them. This decision happens before detailed cell placement and routing, so the exact wire shapes, buffer locations, parasitics and congestion are not yet known. The partitioner must estimate whether a proposed assignment will produce acceptable timing after those later steps.

At RTL, the input describes operations and storage relationships rather than final implementation geometry. Synthesis can change the number and structure of gates, duplicate logic, choose different cells and alter the paths that dominate timing. A pre-synthesis predictor therefore does not directly measure final delay. It estimates a property of a future implementation, and its usefulness depends on whether the estimate remains informative after synthesis, placement, routing and extraction.

### What the reported method changes

The captured description combines a Transformer-based pre-synthesis timing-analysis model with differentiable register tier partitioning. The timing model predicts timing-related information from the RTL representation. The partitioning method treats register-to-tier decisions as differentiable during optimization, so timing feedback can influence the assignment instead of being used only after a discrete partition has already been chosen.

“Differentiable” means that the optimizer can use a computed change in its objective to adjust a continuous representation of a decision. A real register cannot finally occupy a fractional tier, so the method must eventually convert the relaxed decision into a discrete assignment and implement it. That conversion can change timing and cross-tier traffic. The claimed feedback loop is therefore a design strategy; it is not by itself proof that the pre-synthesis prediction is accurate or that the final partition is legal under bonding, routing and thermal constraints.

The source reports 59.3% WNS reduction and 75.4% TNS reduction against state-of-the-art methods and describes these as signoff timing improvements. WNS is the most negative timing slack under a stated convention; TNS aggregates negative slack across violating endpoints. Percentage reductions need the baseline and signed-slack convention. If the baseline values, signs, endpoint sets or timing corners are not shown, the direction and practical size of the claimed improvement cannot be independently reconstructed from the headline percentages.

### The evaluation that would establish early partitioning value

Report the RTL designs, synthesis settings, technology libraries, number of tiers, vertical-link limits and training/test split. Measure predictor error before partitioning and compare predicted timing with post-synthesis and post-route timing on designs not used to fit the model. For each partition, report absolute WNS, TNS, violating endpoints, cross-tier connection count, area, power, temperature, routing success and runtime through signoff. Compare the same designs with timing-oblivious and post-synthesis partitioners under equal implementation effort, and account for the cost of prediction, relaxation, discrete legalization and any repair after routing.

The [RTL-3D](../observed-subthemes/3d-integration-and-thermal-management.md#paper-dac-2026-research793) record describes Transformer-guided pre-synthesis timing analysis coupled to differentiable register tier partitioning. The detailed explanation above separates RTL prediction from synthesized physical timing, relaxed decisions from discrete tier assignments, WNS/TNS ratios from absolute slack, and author-reported signoff from independently reproducible evidence; this card is the compact evidence record.

<span id="explanation-dac-2026-research900"></span>

### Integrated timing-driven placement: a 3D timing estimate must include the physical connection model

### Why ordinary placement models are insufficient

Face-to-face hybrid bonding puts two dies in opposing orientations and connects them through die-to-die bonding locations. A placer must choose each cell or module's tier and in-tier position, then ensure that signals crossing tiers can reach legal bonding resources. A shorter 2D distance is not enough: a cross-tier signal also depends on alignment, bonding density, parasitic capacitance/resistance, congestion, and the receiving tier's available connections.

Timing closure means that every required path meets its arrival constraint after implementation effects are included. Total negative slack (TNS) sums timing violations under a chosen convention; worst negative slack (WNS) records the most severe violation. A reduction factor for TNS or WNS can be misleading when the baseline value is close to zero or when the signs and absolute values are not reported. Ratios must be accompanied by the underlying slack values.

### What the integrated framework changes

The source describes a true-3D static-timing-analysis engine with more accurate parasitic modeling, a sample-based 3D wirelength model with hybrid weighting for global placement, and Lagrangian-based detailed placement. The timing model is used while placement is being optimized, so timing is not only checked after the geometric arrangement is chosen. The sample-based wirelength model estimates connection cost without enumerating every final route; hybrid weighting combines placement objectives, but the description does not specify the weights or their calibration.

Lagrangian detailed placement treats constraints through penalties or multipliers while refining legal positions. This can coordinate timing, tier assignment, alignment and inter-tier connectivity, but a penalty model is not the same as a completed physical check. The final result must still be routed and analyzed with the actual bonding and parasitic rules. Thermal consequences also remain separate: moving logic to improve timing can change power density and heat paths.

The official description reports 30–1002× TNS reduction and 3–14× WNS reduction over state-of-the-art placers. It does not provide absolute slack values, benchmark identities, process and bonding conditions, corner coverage, runtime, routed timing, alignment tolerance, thermal results, or the meaning of each range endpoint. The source therefore supports an integrated timing-driven placement direction, not a verified timing-closure or universal 3D-placement result. [Source: official DAC description and captured record](https://63dac.conference-program.com/presentation/?id=RESEARCH900&sess=sess132).

### The evaluation that would establish physical usefulness

Report tier legality, bond count and capacity, alignment violations, wirelength, congestion, absolute WNS/TNS before and after, timing corners, runtime, routing success, parasitic extraction method, power density and temperature. Compare true-3D and pseudo-3D methods under equal constraints and use the same post-route timing flow. Separate global-placement, detailed-placement, routing and thermal-analysis time. A placement result is useful only if its timing estimate remains predictive after the physical connections it assumed are actually implemented.

[Integrated Timing-Driven Placement](../observed-subthemes/3d-integration-and-thermal-management.md#paper-dac-2026-research900) targets face-to-face hybrid-bonded chips. The detailed explanation above separates tier/position decisions, 3D parasitics, estimated versus routed timing, slack-ratio interpretation, bonding legality and thermal consequences; this card is the compact evidence record.

## Dense packing and programmable connections

<span id="explanation-dac-2026-research3027"></span>

### POLT: fitting hard and soft 3D modules is a geometric problem before it is a chip problem

### What a 3D floorplan must represent

A floorplan assigns each module a position and shape on one or more dies. A **hard module** has a fixed outline. A **soft module** has a target area but can change its aspect ratio or boundary. A rectilinear shape has boundaries aligned with perpendicular directions rather than arbitrary curves. A 3D floorplan adds die-to-die interfaces and alignment constraints between modules or connection regions on different dies.

The geometric objective is to place modules without overlap, satisfy target areas and alignment, and reduce estimated wirelength. A whitespace-free result means the chosen floorplan regions are packed without unused geometric regions under the model. It does not mean that all physical space is removable: routing tracks, power delivery, thermal paths, keep-out regions, bonding pads, mechanical limits, and manufacturing tolerances may require space that a geometric packing model does not include.

### What POLT changes

POLT uses a two-stage process. First, a force-directed method places hard modules and determines spatial relationships for soft modules while respecting constraints. The force calculation is a placement heuristic: it moves objects according to the selected objective and constraints; it does not itself produce a legal routed design. Second, **pressure-driven orthogonal Laguerre–Voronoi tessellation** partitions the soft-module region into rectilinear shapes. The tessellation is intended to match target areas with small error while preserving the relationships established in the first stage.

This separation matters. The first stage determines where regions belong and how they relate. The second stage determines the exact rectilinear boundaries and area allocation. A shape can satisfy its target area while creating an unfavorable boundary for routing or a poor location for a die-to-die interface. The method therefore needs downstream checks after tessellation, not only geometric area checks.

The official description reports an average 5.6% HPWL reduction on 3D floorplans with alignment constraints, 98% area-error reduction versus existing rectilinear floorplanners, and less than 0.16% area error across stated 2D and 3D stacking scenarios. HPWL is a placement estimate, not routed wirelength, delay, power or thermal behavior. The description does not identify benchmarks, runtime, routing feasibility, interface capacity, process rules, or the denominator for area-error reduction. [Source: official DAC description and captured record](https://63dac.conference-program.com/presentation/?id=RESEARCH3027&sess=sess114).

### The evaluation that would establish physical usefulness

Report overlap, target-area error, alignment violations, HPWL, routed wirelength, congestion, die-to-die connection count, timing, power-delivery feasibility, temperature, runtime, and repair cost. Compare hard/soft and alignment-constrained cases separately. Run the same placement through detailed routing and thermal analysis; a floorplan should not be called better for a physical flow if the later stages cannot legalize it or require more whitespace and repair.

The [POLT](../observed-subthemes/3d-integration-and-thermal-management.md#paper-dac-2026-research3027) record describes pressure-driven orthogonal Laguerre–Voronoi tessellation for rectilinear 3D floorplanning. The detailed explanation above separates hard/soft geometry, tessellation, area error, HPWL and downstream routability/thermal feasibility; this card is the compact evidence record.

<span id="explanation-dac-2026-research3100"></span>

### Escaping Flatland: placement in a 3D FPGA is a placement-and-routing problem

### What an FPGA placement actually chooses

An FPGA contains programmable logic blocks and a programmable network of wires and switches. Placement assigns each logic block to a legal site. Routing then selects the programmable wires and switch settings that connect the placed blocks. A placement is useful only when the later routing step can connect every required signal within the available resources.

A 3D FPGA adds a tier choice to the site choice. A logic block is assigned both an in-tier location and a layer. Signals that remain on one layer use that layer's routing fabric. Signals that cross layers use vertical connections and the horizontal resources that reach them. Those vertical connections are finite resources with their own delay, capacitance, area and congestion; they are not an unlimited shortcut between any two points.

This makes geometric distance an incomplete objective. Moving two connected blocks onto different tiers may reduce horizontal distance, but it can add a vertical crossing, consume a scarce connection, or force other nets through a congested region. The relevant cost is the delay and resource demand of the complete routed path. A placement cost that represents only 2D wirelength can therefore prefer an arrangement that later routes poorly.

### What the reported flow changes

The captured description introduces four changes aimed at this 3D-specific search: partitioning-based initialization, adaptive cost scheduling, refined delay estimation and a simulated-annealing move set designed for 3D architectures. Partitioning provides an initial layer assignment. Cost scheduling changes which placement costs dominate at different stages. Delay estimation attempts to represent the timing effect of 3D connections during placement. The move set lets the search explore layer assignments as well as ordinary site movements.

The source compares the flow with Verilog-To-Routing (VTR) on four named architecture families: 3D CB, 3D CB-O, 3D CB-I and 3D SB. It reports approximate geometric-mean and maximum reductions in critical-path delay and routed wirelength. These are different summaries: a geometric mean describes typical multiplicative behavior across the tested cases, while a maximum identifies the strongest reported case. The maximum must not be read as the expected result for every circuit.

The evidence supports a placement flow that uses 3D-aware costs and layer moves. It does not identify the benchmark circuits, tier topology, vertical-link model, routing-capacity assumptions, runtime or physical FPGA implementation. The description says the experiments include routed wirelength, but it does not provide enough detail to determine whether all comparisons used equal routing budgets, identical architecture parameters and successful routing for every case.

### The evaluation that would establish a usable 3D FPGA flow

Report the number and arrangement of tiers, the type and capacity of vertical connections, the delay model for each connection, placement and routing runtime, routing success rate, congestion, critical-path delay before and after routing, total wirelength, power and resource use. Separate layer-assignment quality from in-layer placement quality. Show whether the estimated delay used during placement predicts post-route delay, and test architecture families and benchmark circuits separately rather than combining their best cases.

The [Escaping Flatland](../observed-subthemes/3d-integration-and-thermal-management.md#paper-dac-2026-research3100) record describes a 3D-FPGA placement flow with partitioned initialization, adaptive costs, refined delay estimation and 3D simulated-annealing moves. The detailed explanation above separates tier assignment, programmable routing resources, vertical-link cost, routed evidence and the limits of geometric-mean/max comparisons; this card is the compact evidence record.

## Clock analysis is part of the physical problem

A clock network distributes the timing signal used by storage elements. Differences in arrival time affect how much time data has to travel between them. If two clock paths share a segment, independently assigning the shared segment its fastest and slowest delays can introduce an unnecessarily pessimistic comparison. Common-path pessimism removal accounts for that shared-path variation in timing analysis; it does not physically remove clock delay. [Intel's timing-analysis documentation](https://www.intel.com/content/www/us/en/docs/programmable/683243/22-1/timing-pessimism.html) explains this distinction.

[Flexicts](../observed-subthemes/3d-integration-and-thermal-management.md#paper-dac-2026-research518) incorporates that analysis into three-dimensional clock-tree synthesis. The unanswered issue is how its constructed network performs across layer crossings and variation conditions. The captured record has no clock-arrival difference, power, area, or final timing numbers.

<span id="explanation-dac-2026-research518"></span>

### FlexiCTS: clock-tree construction must preserve the timing paths that CPPR analyzes

### What a clock tree and CPPR measure

A clock tree distributes one clock source to many storage elements. The useful property is not just that every endpoint receives a clock. The clock must arrive within an acceptable time window at each endpoint and with acceptable differences between endpoints. Those arrival differences are clock skew. Clock-tree synthesis chooses buffers, branching points, wire segments and, in a 3D design, the die or tier on which each part is placed.

Static timing analysis compares a launch clock path and a capture clock path. The two paths can share a physical segment before they separate. If analysis treats the shared segment as having an independently worst delay in both comparisons, it can count the same uncertainty twice. Common-path pessimism removal (CPPR) removes that analysis over-counting for the shared portion. CPPR changes the reported timing margin; it does not shorten the shared wire, improve the buffer, or remove variation in the manufactured clock network.

Face-to-face bonding makes the construction problem discrete and resource-constrained. A clock branch may stay on one die, cross to the other die, or share part of a path before crossing. A cross-die branch consumes a hybrid-bonding terminal (HBT) or other vertical connection and adds the delay, capacitance, resistance and variation of that connection. If a flow partitions clock paths rigidly by die, it can destroy useful common paths and leave HBT locations poorly allocated. The best CPPR result therefore depends on the actual tree topology and on whether the physical bond resources can support it.

### What FlexiCTS changes

The captured description presents FlexiCTS as a CPPR-aware, correct-by-construction 3D clock-tree synthesis framework. Its adaptive cross-die buffer assignment decides where buffers are placed relative to die crossings so that path sharing can be preserved while HBT use is allocated. “Correct by construction” is a property of the method's stated constraints; it is not evidence that a fabricated clock tree meets every signoff corner.

The source contrasts the approach with 2D clock-tree synthesis and CPPR-oblivious 3D CTS, and reports a claimed 4.1× skew reduction and 88% fewer HBTs than state-of-the-art methods while matching 2D timing quality. The record does not provide absolute skew, clock latency, HBT counts, power, area, variation corners, benchmark designs, runtime or the definition of “matching.” A reduction factor without the baseline and endpoint values cannot show whether the remaining skew meets a required clock period.

### The evaluation that would establish a usable 3D clock flow

Report the complete die topology, clock sinks, buffer library, HBT capacity and placement rules. Give absolute skew, insertion delay, transition time, area, power, HBT count and timing margin before and after CPPR, with the same constraints for every baseline. Evaluate process, voltage, temperature, bonding-alignment and inter-die-variation corners. Compare the timing analysis estimate with extracted post-route timing and show whether CPPR changes only the pessimism calculation or also corresponds to a physically improved clock network.

The [FlexiCTS](../observed-subthemes/3d-integration-and-thermal-management.md#paper-dac-2026-research518) record describes CPPR-aware 3D clock-tree synthesis with adaptive cross-die buffer assignment. The detailed explanation above separates clock skew from CPPR pessimism, timing analysis from physical delay, shared-path preservation from HBT allocation, and the reported ratios from missing signoff evidence; this card is the compact evidence record.

## Temperature must be connected to useful operation

<span id="explanation-dac-2026-research1862"></span>

### 3D eFlash analog IMC: thermal stability is a chain from temperature to task output

### Start with the physical stack

The described system places a 12 nm logic die and a 28 nm eFlash die in a hybrid-bonded wafer-on-wafer stack. The eFlash die is reported to provide 36 MB for analog in-memory computing. The process nodes identify fabrication generations; they do not by themselves determine thermal resistance, maximum temperature, memory programming behavior, analog noise, or system throughput.

In analog in-memory computing, stored conductance or another physical state represents a weight, and an electrical operation in the memory array contributes to a computation. Temperature can change the stored state, the read/write response, the analog signal, and surrounding circuits. A thermal claim therefore needs a chain of evidence: temperature distribution under a power pattern, change in stored or computed values, calibration or programming response, and final task output.

### What the thermal-stability strategy changes

The source describes three cross-layer mechanisms. A **physics-guided thermal model** predicts temperature behavior using a model constrained by thermal relationships. The reported KL divergence of 0.088 is meaningful only with the reference distribution, normalization, operating points, and spatial/temporal aggregation defined.

**Temperature-insensitive differential programming (TIDP)** is intended to stabilize stored weights from −30°C to 60°C. Differential representation can reduce the effect of a common change, but it does not remove every temperature-dependent effect: the two programmed states can respond differently, read circuitry can drift, and programming itself may have temperature-dependent error. The programming range is also not the same as the later task-evaluation range.

**Adaptive temperature calibration (ATC)** adjusts the computation or its interpretation using temperature information. The reported 60.7% reduction in output-error standard deviation must be tied to the baseline calibration, sensor conditions, calibration cost, update frequency, and remaining task error. Calibration can improve output stability while consuming time, energy, memory, or control bandwidth.

The official description reports a first 3D eFlash analog-IMC prototype with hybrid bonding, less than 10% degradation in end-to-end task accuracy for ResNet-18 and DCCRN across −15°C to 75°C, and the model/error values above. It does not identify datasets, exact accuracy baseline, temperature measurement locations, power/cooling conditions, calibration overhead, endurance, retention, or silicon characterization protocol. The source supports a prototype and a cross-layer strategy claim, not commercial qualification or universal thermal resilience. [Source: official DAC description and captured record](https://63dac.conference-program.com/presentation/?id=RESEARCH1862&sess=sess139).

### The evaluation that would establish thermal stability

Measure temperature at both dies and relevant array/periphery regions under repeatable workloads and cooling. Sweep the complete operating range, including the gap between the −30°C to 60°C programming claim and the −15°C to 75°C task claim. Report raw weight drift, analog output error, calibration time/energy, task accuracy, throughput, endurance and retention before and after calibration. Compare TIDP and ATC separately against ordinary programming and calibration, and report whether the result is measured silicon, calibrated simulation, or a mixture.

The [12nm/28nm eFlash computing stack](../observed-subthemes/3d-integration-and-thermal-management.md#paper-dac-2026-research1862) introduces a thermal-stability strategy for bonded memory and computation. The detailed explanation above separates process labels from thermal behavior, temperature from stored-weight/output error, programming range from task range, and prototype evidence from qualification; this card is the compact evidence record.

Taken together, these records motivate evaluating early design choices through completed physical implementation. They do not yet show which method wins. A defensible comparison needs the same functional design, bonding limits, cooling conditions, connection resources, and timing requirements, with area and runtime counted after necessary repairs.

## Compare the results carefully

First identify the inputs and required output quality. Then identify the limited resource: time, memory, communication, energy, circuit area, or correctness coverage. Ask which part of the method reduces that cost and which new cost it adds. Compare numbers only when the experiments hold these conditions sufficiently similar.

A conference description may explain the proposal while omitting the full experiment. An author preprint link may have been coded from its abstract. The source classification does not by itself establish that every table was read. Missing locations remain visible below.

## Complete captured evidence

These are evidence records, not substitutes for the explanations above. Each record preserves its problem, proposed method, measurements, comparison conditions, and source limits. A populated record does not establish that its mechanism has been fully explained or independently verified.

<span id="paper-dac-2026-research1862"></span>

### Thermal Stability Strategy for a 12nm/28nm Hybrid-Bonding Wafer-on-Wafer 3D-Integrated Eflash In-Memory Computing SoC

DAC 2026 · Record: `dac-2026-research1862`

[Read the step-by-step explanation](#explanation-dac-2026-research1862)

**Updated source-backed reading card**

Reviewed 2026-09-08. Reconciles the 3D eFlash thermal-stability card with the captured official source; separates the 12nm/28nm stack from thermal behavior, the physics model from measured temperature, TIDP/ATC mechanisms from their costs, and programming-range evidence from task-range and qualification claims.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

A hybrid-bonded 3D eFlash analog in-memory-computing stack can experience temperature-dependent weight and computation changes that degrade analog accuracy and system throughput.

**Mechanism / artifact:**

Cross-layer thermal stability strategy combining a physics-guided thermal model, temperature-insensitive differential programming from -30°C to 60°C, and adaptive temperature calibration.

**Workload — the work tested:**

ResNet-18 and DCCRN inference on a reported 3D eFlash analog-IMC SoC; datasets, task metrics, power workloads and accuracy baseline are unspecified.

**Hardware and manufacturing assumptions:**

Reported hybrid-bonded wafer-on-wafer prototype with 12nm logic, 28nm 36MB eFlash and analog IMC; temperature sensor locations, cooling, power, measurement instruments, endurance/retention and silicon characterization procedure are unspecified.

**Baseline — the comparison method:**

Ordinary temperature-sensitive programming/calibration

2D CIM thermal design

Baseline implementation and resource parity are unspecified

**Reported measurements:**

The official description reports KL divergence 0.088 for the thermal model, 60.7% output-error-standard-deviation reduction from adaptive calibration, and less than 10% end-to-end task-accuracy degradation across -15°C to 75°C; reference distributions, baselines and percentage-point conventions are unspecified.

**Limits on the conclusion:**

The 12nm and 28nm process labels do not quantify thermal resistance or heat removal; thermal behavior requires measured temperatures under specified power and cooling.

The -30°C to 60°C programming range differs from the -15°C to 75°C task-evaluation range, so programming stability does not cover the complete claimed task range.

Calibration can reduce output-error variation while adding sensing, computation, update, time and energy cost; output-error standard deviation is not task accuracy or throughput.

The official description supplies no temperature maps, raw weight drift, calibration overhead, endurance, retention, dataset, baseline accuracy or independent thermal characterization; prototype evidence is not commercial qualification or universal resilience.

**Source and location**

Evidence tier: Primary captured official DAC description only; no full paper extraction, thermal/silicon execution or independent endurance/qualification validation. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH1862&sess=sess139)

DAC 2026 official description and data/review-packets/dac-2026-research1862.json: hybrid-bonded 12nm logic/28nm 36MB eFlash stack; physics-guided model/KL 0.088; TIDP -30°C to 60°C; ATC 60.7% output-error-standard-deviation reduction; ResNet-18/DCCRN less-than-10% task degradation across -15°C to 75°C.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** 2D CIM thermal design

3D stack without thermal stabilization

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH1862

**Hardware or process assumptions:** 12nm/28nm hybrid-bonded wafer-on-wafer eFlash CIM stack; thermal path, materials, and operating voltage are unspecified.

**Limits:** No temperature, drift, endurance, power, density, or process-corner results are reported.

Thermal mitigation may reduce density or performance.

Official description only; silicon and thermal characterization are required.

**Method or artifact:** Thermal-stability design strategy for 12nm/28nm hybrid-bonded wafer-on-wafer CIM.

**Metrics:** Thermal stability is claimed qualitatively

**Problem:** 3D eFlash CIM stacks create thermal coupling that can destabilize memory and compute behavior.

**Workload or benchmark:** 3D eFlash CIM SoC workloads and thermal operating points; measurements and baselines are unspecified.

</details>

<span id="paper-dac-2026-research3027"></span>

### Whitespace-Free Rectilinear 3D Floorplanning with Pressure-Driven Orthogonal Laguerre-Voronoi Tessellation (POLT)

DAC 2026 · Record: `dac-2026-research3027`

[Read the step-by-step explanation](#explanation-dac-2026-research3027)

**Updated source-backed reading card**

Reviewed 2026-09-08. Reconciles the POLT card with the captured official source; separates hard/soft module geometry, force-directed placement, rectilinear tessellation, HPWL and area error from routed, thermal, power-delivery and manufacturing feasibility.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

3D floorplanning must place fixed-outline hard modules and flexible soft modules while meeting die-to-die alignment and area constraints without relying on unrealistic rectangular-only assumptions.

**Mechanism / artifact:**

Two-stage whitespace-free rectilinear floorplanning: force-directed placement establishes hard-module positions and soft-module relationships, then pressure-driven orthogonal Laguerre–Voronoi tessellation shapes soft modules with low area error.

**Workload — the work tested:**

2D and 3D stacking floorplans, including alignment-constrained 3D cases; benchmark identities, module counts, interface topology and constraint distributions are unspecified.

**Hardware and manufacturing assumptions:**

Hard/soft modules and die-to-die interfaces in a 3D IC floorplan; process rules, bonding alignment tolerance, routing resources, power delivery, thermal model and physical verification flow are unspecified.

**Baseline — the comparison method:**

Existing rectilinear floorplanners

Baseline runtime, constraints, area-error definition and physical-feasibility parity are unspecified

**Reported measurements:**

The official description reports average 5.6% HPWL reduction with alignment constraints, 98% area-error reduction versus existing rectilinear floorplanners, and less than 0.16% area error across stated 2D/3D scenarios; aggregation and denominators are unspecified.

**Limits on the conclusion:**

Whitespace-free geometric packing does not establish routability, power-delivery feasibility, thermal paths, bonding keep-outs, timing closure or manufacturing tolerance.

HPWL is a placement estimate, not routed wirelength, delay, congestion, power or temperature; a lower HPWL can still create a difficult inter-die connection pattern.

Force-directed placement and tessellation solve different stages; low soft-module area error does not prove that hard-module relationships or interface constraints remain feasible after exact shaping.

The official description supplies no benchmark identities, runtime, routed/thermal results, process constraints or independent execution; area-error and HPWL claims do not establish a better physical 3D implementation.

**Source and location**

Evidence tier: Primary captured official DAC description only; no full paper extraction, routing/thermal execution or independent 3d physical feasibility validation. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH3027&sess=sess114)

DAC 2026 official description and data/review-packets/dac-2026-research3027.json: hard/soft module and D2D floorplanning problem; force-directed first stage; pressure-driven orthogonal Laguerre–Voronoi tessellation; 5.6% HPWL, 98% area-error reduction and <0.16% area-error claims.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** whitespace-permitting 3D floorplanning

rectilinear heuristic floorplanning

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH3027

**Hardware or process assumptions:** 3D IC floorplanning with stacked or bonded tiers; technology and inter-tier assumptions are unspecified.

**Limits:** No area, whitespace, thermal, timing, routing, or runtime results are reported.

Whitespace-free packing may worsen thermal and routing feasibility.

Official description only; full 3D signoff validation is required.

**Method or artifact:** Pressure-driven orthogonal Laguerre-Voronoi tessellation for 3D floorplanning.

**Metrics:** Whitespace and floorplan quality are claimed qualitatively

**Problem:** Three-dimensional floorplanning must avoid whitespace while satisfying rectilinear geometry and physical constraints.

**Workload or benchmark:** Rectilinear 3D floorplanning instances; thermal, timing, and routing models are unspecified.

</details>

<span id="paper-dac-2026-research900"></span>

### Integrated Timing-Driven Placement for Hybrid-Bonding-Based Face-to-Face 3D ICs

DAC 2026 · Record: `dac-2026-research900`

[Read the step-by-step explanation](#explanation-dac-2026-research900)

**Updated source-backed reading card**

Reviewed 2026-09-08. Reconciles the integrated 3D placement card with the captured official source; separates tier/position decisions, 3D parasitic timing, estimated versus routed connections, TNS/WNS ratios, bonding legality and thermal consequences.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Face-to-face hybrid-bonded 3D placement must jointly choose tiers and positions while accounting for timing, parasitics, bonding alignment and inter-tier connections.

**Mechanism / artifact:**

True-3D STA with parasitic modeling integrated into placement, a sample-based 3D wirelength model with hybrid weighting for global placement, and Lagrangian-based detailed placement.

**Workload — the work tested:**

Face-to-face hybrid-bonded 3D IC netlists and tier assignments; benchmark identities, design sizes, timing corners, bonding constraints and post-route flow are unspecified.

**Hardware and manufacturing assumptions:**

Hybrid-bonded 3D IC physical-design flow; process, bonding pitch/alignment tolerance, parasitic extraction, inter-tier resource capacity, routing, power delivery, cooling and thermal model are unspecified.

**Baseline — the comparison method:**

State-of-the-art 3D placers

2D/pseudo-3D placement methods

Baseline constraints, timing flow, absolute slack values and resource parity are unspecified

**Reported measurements:**

The official description reports 30–1002x TNS reduction and 3–14x WNS reduction; absolute slack values, endpoint mapping, signed-ratio convention and aggregation are unspecified.

**Limits on the conclusion:**

TNS/WNS reduction factors can be unstable near a zero baseline and do not substitute for absolute slack, timing-corner coverage or complete timing closure.

A sample-based wirelength/parasitic model guides placement but does not prove that final routed wires, bonding connections and extracted parasitics match the estimate.

Lagrangian penalties can balance timing and geometry without proving legal bonding, routing, power delivery or thermal feasibility; timing improvement can increase local power density.

The official description supplies no benchmark identities, runtime, routed timing, alignment tolerance, thermal result or independent execution; no universal 3D signoff claim follows.

**Source and location**

Evidence tier: Primary captured official DAC description only; no full paper extraction, routed 3d execution or independent timing/thermal/signoff validation. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH900&sess=sess132)

DAC 2026 official description and data/review-packets/dac-2026-research900.json: true-3D hybrid-bonded placement problem; 3D STA with parasitic modeling; sample-based 3D wirelength/hybrid weighting; Lagrangian detailed placement; reported TNS/WNS reduction ranges.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** 2D timing-driven placement

timing-oblivious 3D placement

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH900

**Hardware or process assumptions:** Face-to-face hybrid bonding with 3D tiers; thermal, alignment, and via assumptions are unspecified.

**Limits:** No timing, wirelength, thermal, alignment, yield, or runtime results are reported.

Timing improvements may increase thermal or bonding risk.

Official description only; 3D signoff validation is required.

**Method or artifact:** Integrated timing-driven placement for hybrid-bonded 3D ICs.

**Metrics:** 3D timing and placement quality are claimed qualitatively

**Problem:** Face-to-face 3D IC placement must jointly manage timing, tier assignment, bonding alignment, and inter-tier connections.

**Workload or benchmark:** 3D IC netlists and tier assignments; process, bonding constraints, and baselines are unspecified.

</details>

<span id="paper-dac-2026-research3100"></span>

### Escaping Flatland: A Placement Flow for Enabling 3D FPGAs

DAC 2026 · Record: `dac-2026-research3100`

[Read the step-by-step explanation](#explanation-dac-2026-research3100)

**Updated source-backed reading card**

Reviewed 2026-09-08. Reconciles the Escaping Flatland card with the captured official source; explains FPGA placement and routing from first principles and separates tier assignment, vertical resources, delay estimation, routed wirelength, architecture-specific comparisons and missing implementation detail.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

3D FPGA placement must assign logic to tiers and sites while accounting for vertical connectivity, programmable routing resources and 3D delay rather than relying on 2D-derived costs.

**Mechanism / artifact:**

A 3D FPGA placement flow using partitioning-based initialization, adaptive cost scheduling, refined delay estimation and a 3D-specific simulated-annealing move set to explore layer assignments and placements.

**Workload — the work tested:**

Four 3D FPGA architectures named 3D CB, 3D CB-O, 3D CB-I and 3D SB; benchmark circuits, architecture dimensions, tier topology and routing-resource distributions are unspecified.

**Hardware and manufacturing assumptions:**

Programmable 3D FPGA fabric with horizontal routing and finite vertical connections; vertical-link implementation, delay/capacitance model, capacity, power model and physical implementation status are unspecified.

**Baseline — the comparison method:**

Verilog-To-Routing (VTR)

Architecture matching, routing budgets, benchmark set and configuration parity are unspecified

**Reported measurements:**

The official description reports approximate geometric-mean and maximum critical-path-delay reductions of 3/7%, 2/4%, 3/8% and 6/18% for 3D CB, 3D CB-O, 3D CB-I and 3D SB, respectively, plus corresponding routed-wirelength reductions of approximately 1/3%, 2/8%, below 1/5% and 5/10%; endpoint mapping and aggregation details are unspecified.

**Limits on the conclusion:**

A 3D placement improvement is not a routing or silicon improvement unless vertical resources, congestion and complete routing feasibility are reported under matched architecture constraints.

Geometric means and maxima summarize different parts of the tested distribution; the maximum is not a general expected gain and the description does not provide per-circuit results.

Refined delay estimation can guide search without predicting post-route delay if the vertical-link, switch, congestion or parasitic model is incomplete; estimated timing and routed timing must be compared directly.

The official description supplies no benchmark identities, tier topology, vertical-link implementation, runtime, power, routing-success rate or independent execution; no universal advantage over 2D FPGA flows follows.

**Source and location**

Evidence tier: Primary captured official DAC description only; no full paper extraction, architecture reconstruction or independent placement/routing execution. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH3100&sess=sess175)

DAC 2026 official description and data/review-packets/dac-2026-research3100.json: 2D-derived placement limitation; partitioned initialization; adaptive cost scheduling; refined delay estimation; 3D simulated-annealing moves; four architecture families; critical-path-delay and routed-wirelength comparisons versus VTR.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** 2D FPGA placement

3D placement without vertical-awareness

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH3100

**Hardware or process assumptions:** Stacked or monolithic 3D FPGA with vertical interconnect; thermal and process assumptions are unspecified.

**Limits:** No timing, wirelength, thermal, routability, area, or runtime results are reported.

Vertical placement benefits may depend on architecture and cooling.

Official description only; full 3D routing validation is required.

**Method or artifact:** Placement flow for 3D FPGA architectures.

**Metrics:** 3D FPGA placement quality is claimed qualitatively

**Problem:** 3D FPGA placement must exploit tiers while managing vertical connectivity, timing, and thermal effects.

**Workload or benchmark:** 3D FPGA netlists; tier topology, vias, architecture, and baselines are unspecified.

</details>

<span id="paper-dac-2026-research518"></span>

### Flexicts: CPPR-Aware 3D Clock Tree Synthesis for Face-to-Face Bonded ICs

DAC 2026 · Record: `dac-2026-research518`

[Read the step-by-step explanation](#explanation-dac-2026-research518)

**Updated source-backed reading card**

Reviewed 2026-09-08. Reconciles the FlexiCTS card with the captured official source; explains clock-tree synthesis and CPPR from first principles and separates skew, common-path analysis, physical cross-die resources, HBT allocation, reported ratios and missing signoff evidence.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Face-to-face bonded 3D IC clock trees must control skew and cross-die resources without destroying common clock paths that affect CPPR analysis.

**Mechanism / artifact:**

CPPR-aware 3D clock-tree synthesis with adaptive cross-die buffer assignment intended to preserve path sharing and optimize hybrid-bonding-terminal allocation.

**Workload — the work tested:**

Face-to-face bonded 3D IC clock networks; endpoint counts, benchmark designs, tier topology, clock constraints and variation cases are unspecified.

**Hardware and manufacturing assumptions:**

3D bonded clock distribution with tier-crossing interconnects and hybrid-bonding terminals; buffer library, bond pitch, alignment tolerance, inter-die variation, process corners, power delivery and thermal conditions are unspecified.

**Baseline — the comparison method:**

2D clock-tree synthesis

CPPR-oblivious 3D CTS

State-of-the-art comparison configuration and resource parity are unspecified

**Reported measurements:**

The official description reports 4.1x skew reduction and 88% fewer HBTs than state-of-the-art methods while matching 2D timing quality; absolute skew, HBT counts, timing-quality definition and aggregation are unspecified.

**Limits on the conclusion:**

CPPR removes pessimism in timing analysis for shared clock paths; it does not physically remove clock delay, variation or skew in the manufactured network.

Adaptive buffer assignment can preserve common paths while consuming different cross-die resources; HBT reduction is not automatically lower power, area or timing risk.

A reduction factor and qualitative 2D match do not establish required absolute skew, insertion delay, timing margin or signoff closure without baseline values and corner definitions.

The official description supplies no benchmark identities, runtime, clock topology, absolute measurements, process/voltage/temperature/bonding corners or independent execution; no universal 3D CTS advantage follows.

**Source and location**

Evidence tier: Primary captured official DAC description only; no full paper extraction, clock tree reconstruction or independent signoff corner validation. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH518&sess=sess114)

DAC 2026 official description and data/review-packets/dac-2026-research518.json: face-to-face 3D clock-tree challenge; CPPR-aware construction; adaptive cross-die buffer assignment; path sharing and HBT allocation; claimed 4.1x skew reduction, 88% HBT reduction and 2D timing match.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** 2D clock-tree synthesis

CPPR-oblivious 3D CTS

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH518

**Hardware or process assumptions:** 3D bonded clock distribution with tier-crossing interconnects; thermal and bonding assumptions are unspecified.

**Limits:** No skew, latency, power, area, thermal, yield, or runtime results are reported.

Bonding and tier variation may alter clock behavior.

Official description only; signoff-corner validation is required.

**Method or artifact:** CPPR-aware 3D clock-tree synthesis flow.

**Metrics:** Clock quality and timing closure are claimed qualitatively

**Problem:** 3D bonded IC clock trees must manage common-path pessimism, tier crossings, and skew.

**Workload or benchmark:** Face-to-face bonded 3D IC clock networks; process, tiers, and baselines are unspecified.

</details>

<span id="paper-dac-2026-research793"></span>

### RTL-3D: Timing-Aware Tier Partitioning for 3D ICs Using Pre-Synthesis Timing Analysis

DAC 2026 · Record: `dac-2026-research793`

[Read the step-by-step explanation](#explanation-dac-2026-research793)

**Updated source-backed reading card**

Reviewed 2026-09-08. Reconciles the RTL-3D card with the captured official source; explains pre-synthesis tier partitioning from first principles and separates RTL prediction, differentiable relaxation, discrete implementation, WNS/TNS interpretation and missing post-route evidence.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Early 3D IC tier partitioning must anticipate cross-tier timing before synthesis, placement and routing expose the physical implementation costs.

**Mechanism / artifact:**

RTL-3D couples a Transformer-based pre-synthesis timing-analysis model with differentiable register tier partitioning and implementation feedback.

**Workload — the work tested:**

RTL designs partitioned across 3D IC tiers; benchmark identities, design sizes, register counts, tier count, synthesis settings and train/test split are unspecified.

**Hardware and manufacturing assumptions:**

3D IC with tiered logic and vertical interconnect; technology libraries, bonding limits, vertical-link capacity, parasitic extraction, routing, power delivery and thermal model are unspecified.

**Baseline — the comparison method:**

Post-synthesis tier partitioning

Timing-oblivious partitioning

State-of-the-art comparison flow, implementation effort and constraint parity are unspecified

**Reported measurements:**

The official description reports 59.3% WNS reduction and 75.4% TNS reduction in signoff timing versus state-of-the-art methods; absolute slack, signed-slack convention, endpoint set, corner coverage and aggregation are unspecified.

**Limits on the conclusion:**

A pre-synthesis timing predictor estimates a later implementation; synthesis transformations, cell selection, placement, routing, parasitics and congestion can change the critical paths it predicts.

Differentiable tier decisions are a relaxed optimization representation; discrete legalization can change tier crossings, timing and routing feasibility, so relaxation quality is not final physical quality.

WNS/TNS reduction percentages do not establish timing closure without absolute baseline and final slack, violating-endpoint counts, timing corners and a stated sign convention.

The official description supplies no benchmark identities, predictor error, runtime, area, power, thermal result, vertical-link count or independent execution; author-reported signoff claims are not independently validated.

**Source and location**

Evidence tier: Primary captured official DAC description only; no full paper extraction, predictor reproduction or independent 3d signoff validation. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH793&sess=sess155)

DAC 2026 official description and data/review-packets/dac-2026-research793.json: pre-synthesis timing problem; Transformer timing model; differentiable register tier partitioning; implementation feedback; reported 59.3% WNS and 75.4% TNS reductions.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** post-synthesis tier partitioning

timing-oblivious partitioning

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH793

**Hardware or process assumptions:** 3D IC with tiered logic and vertical interconnect; thermal and bonding assumptions are unspecified.

**Limits:** No timing, area, thermal, vertical-link, yield, or runtime results are reported.

Pre-synthesis timing may mispredict post-layout behavior.

Official description only; 3D signoff validation is required.

**Method or artifact:** Pre-synthesis timing-aware RTL tier partitioning.

**Metrics:** 3D timing and partition quality are claimed qualitatively

**Problem:** 3D IC tier partitioning must anticipate timing before detailed synthesis and physical implementation.

**Workload or benchmark:** RTL designs mapped to 3D IC tiers; technologies, vertical links, and baselines are unspecified.

</details>

## What remains to establish

Resolve unspecified workloads, comparison methods, resource budgets, and source locations before generalizing a reported gain. Multiple papers in this selected sample permit comparison of mechanisms, but do not by themselves establish recurrence across years or a long-term trend.

[All subthemes](../expanded-taxonomy-v1.md) · [Research directions](../directions/README.md)
