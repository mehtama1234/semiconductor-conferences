# Placement routing and timing

This subject has 6 records in the selected sample. This page explains where it fits, then presents all captured paper evidence without shortening the measurements or limitations.

[Definitions used in the paper records](../reading-guide-v1.md)

## Understand the parent subject first

- [Physical design and manufacturing](../themes/physical-design-and-manufacturing.md)

## Timing is a requirement on signal arrival

A synchronous circuit uses clock events to coordinate when stored values may change. Data must reach the relevant storage elements within the required timing window. The delay includes logic evaluation and transmission through wires, so placement, routing, and circuit sizing all influence whether the requirement is met.

A late path can limit the operating frequency or cause incorrect behavior. Making that path faster may require larger cells, more buffers, shorter connections, or different placement. Each option can increase area, power, or congestion elsewhere. Timing optimization therefore needs a complete cost and legality check.

## Supply voltage changes the timing problem

Power reaches a circuit through physical conductors. Current flowing through their resistance causes voltage differences along the supply network, often described as IR drop. If local supply conditions differ from the assumptions used to estimate circuit delay, the predicted timing can be inaccurate.

The IR-drop-aware placement record combines placement, power-network changes, and accelerated voltage analysis. The mechanism connects where current is demanded to where the power network can deliver it. Its current description does not establish voltage thresholds, violation counts, runtime, or agreement with final power-integrity checks. [Recorded evidence](../observed-subthemes/placement-routing-and-timing.md#paper-dac-2026-research2297)

An evaluation must therefore state both the workload or switching assumptions and the network model. Improving one predicted voltage score does not establish adequate operation under all relevant activity patterns.

<span id="explanation-dac-2026-research2297"></span>

## IR-drop-aware placement: a voltage model must remain coupled to the final power network

IR drop is the reduction in supply voltage caused by current flowing through resistance in the power-delivery network (PDN). A cell's location affects the resistance and available paths between its supply pins and the source. Its switching activity affects current demand. Placement and PDN topology are therefore coupled: moving a high-current cell can change local demand, while adding a power path can change the voltage field available to many cells.

The described framework combines three mechanisms. GPU-accelerated modified nodal analysis (MNA) estimates node voltages quickly enough to participate in iterative placement. An iterative PDN strategy inserts additional delivery paths to improve global robustness. A node-specific density control limits the amount of cell power that can be placed near a PDN node according to its tolerable load, targeting local hot spots. These mechanisms address different scales; a globally stronger network does not guarantee that every local demand peak is safe, and local density limits do not repair an inadequate source, trunk, or via structure.

MNA solves a circuit model whose result depends on the conductance matrix, current vector, boundary conditions, topology, resistance extraction, and numerical tolerances. GPU execution changes how quickly the equations are solved, not whether the modeled equations represent the fabricated PDN. The placement loop must state whether current is estimated from activity, cell class, vectorless assumptions, or a prior implementation. It must also state how a changed placement updates power, parasitics, rail connections, and the next analysis. Reusing stale current maps can make an apparently fast iteration physically irrelevant.

The local density constraint needs a physical interpretation. A maximum tolerable load at a node could be a current limit, a voltage-drop threshold translated through the model, or a heuristic margin. The mapping must account for neighboring nodes, shared metal segments, via resistance, multiple voltage domains, return paths, and simultaneous switching. A cell assigned to one node may draw through several network paths, and placing fewer cells locally can shift demand to an adjacent bottleneck. Report constraint violations, binding nodes, current/voltage margins, and sensitivity to the density model rather than only total placement density.

The optimization objective also has competing terms. Adding PDN paths may lower voltage drop but consume routing resources, increase wirelength, add vias and capacitance, constrain signal routing, or increase area and power. A placement that has no extra wirelength under the reported estimator can still become harder to route or fail antenna, electromigration, thermal, or timing checks after detailed implementation. “No runtime overhead” must include GPU analysis, PDN edits, legalization, incremental extraction, convergence checks, and any extra signoff passes.

The correct validation chain is staged. First compare the GPU MNA result with a reference solver on identical matrices and current vectors. Then compare placement-loop predictions with extracted pre-route and post-route PDN analyses under identical activity, voltage, process, temperature, and metal assumptions. Finally run power-integrity signoff with realistic dynamic activity and report global and local violation counts, worst voltage, margin distributions, timing impact, routability, area, power, runtime, and convergence. A reduction in violations under one analytical model is not proof of silicon-level voltage safety.

The appropriate baselines include state-of-the-art IR-drop-aware placement, ordinary placement followed by PDN repair, and ablations of GPU acceleration, iterative path insertion, and node-specific density control. Hold netlist, library, placement constraints, voltage domains, current assumptions, process, metal stack, routing resources, legalization, extraction, signoff tool versions, and stopping criteria constant. The official description claims fewer IR-drop violations without additional wirelength, runtime, or routability overhead, but supplies no counts, thresholds, designs, GPU, process, extracted-network agreement, or signoff results. The evidence supports a coupled placement/PDN optimization direction, not demonstrated signoff-quality power-integrity closure.

<span id="explanation-dac-2026-research1317"></span>

## HyPAS: a differentiable placement proposal still needs discrete signoff closure

Standard-cell placement chooses where cells sit, while sizing chooses library
variants such as drive strength and threshold type. These decisions affect
wirelength, congestion, slew, delay, leakage, dynamic power and area together.
An incremental flow may optimize one discrete stage at a time, whereas a
differentiable flow can move through a smooth approximation of the search space.
The smooth approximation is useful for proposing changes, but legality and
timing closure remain properties of the discrete implementation.

HyPAS is described as a hybrid loop. A differentiable DREAMPlace stage uses a
GNN-based timing-power surrogate to guide placement and sizing, while an
OpenROAD stage performs discrete optimization, legalization, timing closure and
buffer-aware repair. A straight-through estimator supplies gradients through
discrete library parameters. This bridges two search representations; it does
not make the surrogate equal to extracted timing or power, nor does it prove
that every repaired candidate preserves the differentiable objective.

The first gate is representation and legality. Specify the netlist, cell
library, legal sites, orientations, rows, placement constraints, allowed
sizing actions, buffer insertion rules and timing exceptions. Check overlaps,
row alignment, fixed and blocked regions, power rails, well rules, connectivity,
slew, fanout and setup/hold timing after each accepted candidate. A continuous
coordinate or library embedding can produce a useful gradient while mapping to
an illegal cell choice or a materially different discrete circuit.

The second gate is surrogate fidelity. Hold out designs, netlists, placements,
cell sizes, loads and corners when measuring the GNN timing-power model. Report
error distributions, rank correlation, worst-case paths, calibration, and the
frequency with which surrogate decisions are overturned by OpenROAD analysis.
If the surrogate is trained on outputs from the same flow used for comparison,
separate training, tuning and test data and include the cost of generating
labels. Straight-through gradients are an optimization device, not evidence of
an exact derivative of signoff PPA.

PPA must be measured at a common physical boundary. Report area, setup and hold
slack, total and critical wirelength, congestion, buffer count, leakage,
dynamic and total power, clock metrics, violations, iterations and wall-clock
time. State whether timing and power come from a surrogate, global placement,
post-route extraction or signoff, and include legalization, repair, detailed
placement, routing, extraction and repeated evaluations in runtime. A PPA gain
before routing can disappear after parasitics, buffering or congestion repair.

The relevant baselines include conventional incremental optimization, a
discrete OpenROAD flow without differentiable refinement, differentiable
placement/sizing without discrete repair, and the cited ICCAD 2025 CAD Contest
and state-of-the-art methods under the same tools. Hold design, library,
process, clock constraints, loads, corners, routing flow, stopping criterion,
hardware and measurement boundary constant. Ablate the surrogate, the
straight-through estimator, joint sizing, repair and alternation schedule;
report per-design results and failures rather than only an average claim.

The captured official description claims superior PPA gains with competitive
runtime against ICCAD 2025 contest results and state-of-the-art methods, but
provides no numerical PPA values, design sizes, timing constraints, runtime,
surrogate error or contest configuration. The evidence supports a hybrid
placement-and-sizing search direction, not demonstrated signoff-quality PPA
improvement or runtime advantage across designs and technologies.

<span id="explanation-dac-2026-research1080"></span>

## AccDRC: DRC acceleration is useful only when partitioning and rule semantics remain exact

Design-rule checking (DRC) evaluates geometric layout against process rules such as spacing, width, enclosure, overlap and connectivity constraints. A violation is meaningful only under the rule deck, layer definitions, tolerances and layout representation used by the manufacturing flow. Accelerating a subset of geometric checks is not equivalent to accelerating or replacing a complete DRC signoff run.

AccDRC is described as a software–hardware co-design. Cell-aware partitioning reorganizes layout data into balanced task units, data preparation and task encapsulation feed an FPGA, a locality-preserving loader supplies geometry, a unified reconfigurable check core evaluates multiple rules, and sparse result writeback emits violations. These mechanisms target data movement, reuse and parallelism. The captured description does not identify the rule suite, geometric kernel, partition boundary, halo/neighbor handling, FPGA device, or how results are reconciled with a trusted DRC tool.

### Partitioning must preserve geometric context

Layout cells are not independent merely because their origins are separate. A rule may compare shapes across a partition boundary, across hierarchy, or through vias and neighboring layers. A cell-aware partition must include enough halo geometry and preserve layer, net, hierarchy, orientation, datatype and coordinate precision. Balanced task counts can still create imbalanced candidate pairs or concentrated memory traffic. Report partition sizes, boundary replication, candidate-pair counts, load balance, memory bandwidth, queueing and rejected/overflowed tasks.

### Rule equivalence is the first acceleration gate

The FPGA check core must reproduce the reference rule semantics, including inclusive versus exclusive thresholds, spacing to shapes on other layers, enclosure, notch, density, connectivity, waivers, hierarchy and error locations. Sparse writeback must not drop coincident, duplicate, overlapping or high-volume violations. Compare violation sets and coordinates against KLayout or another trusted implementation on adversarial geometries, boundary distances, dense layouts, empty results, maximal violation bursts and every supported rule. Report false positives, false negatives, ordering differences, unsupported rules and fallback behavior.

### Speedup needs a complete and fair boundary

The source reports 522.11×–1071.03× speedup over CPU-based KLayout and 9.62×–26.07× over GPU-based OpenDRC. It does not identify layout sizes, rule/deck coverage, FPGA device or resources, host preprocessing, data transfer, bitstream/configuration, result transfer, CPU post-processing, compilation, or whether both baselines execute the same checks. “DRC runtime” must state whether layout parsing, tiling, partitioning, halo exchange, checking, result compression, violation reporting and final equivalence checking are included.

Report absolute runtime, throughput, FPGA frequency, LUT/FF/BRAM/DSP use, bandwidth, power/energy, memory footprint, scaling with layout size and rule count, and p50/p95/p99 or worst-case behavior. Hold layout, rule deck, process technology, tolerance, input format, output contract, host, software versions and correctness checks constant across KLayout, OpenDRC and AccDRC. A high peak speedup on sparse-violation layouts can hide a writeback or boundary-traffic bottleneck on dense violations.

The evidence supports FPGA-accelerated, cell-aware DRC as a constrained implementation direction, not demonstrated signoff-equivalent DRC replacement or portable 522.11×–1071.03×/9.62×–26.07× acceleration across rule decks and layouts. Rule coverage, equivalence, device/resource conditions and complete runtime accounting remain unresolved.

## Placement and sizing influence each other

A larger circuit element may drive a connection faster but require more space and power. Its added size can also change nearby placement and routing. Choosing sizes after fixing locations can miss useful combinations; changing both together expands the search and complicates evaluation.

HyPAS's captured method combines placement and sizing choices, learned timing/power estimates, and legality or repair steps using design tools. A learned estimate helps choose candidates, while the final tools determine whether the selected candidate meets the actual implementation rules. The record does not supply enough prediction-error, repair-cost, and final-result detail to establish the complete gain. [Recorded evidence](../observed-subthemes/placement-routing-and-timing.md#paper-dac-2026-research1317)

## The clock also has to arrive on time

A clock distribution network carries timing events to many storage elements. Its paths have different delays and loads. The difference in clock arrival times matters because it changes the time available for data to travel between connected elements.

Clock-tree synthesis chooses a branching network and associated buffers to meet the clock requirements. DCTS's record proposes representing discrete topology choices through a differentiable model and choosing topology and buffer sizes together. A differentiable representation allows a search to use estimates of how an objective changes as its variables change. [Recorded evidence](../observed-subthemes/placement-routing-and-timing.md#paper-dac-2026-research1211)

The selected topology must still become a legal physical implementation. Clock constraints, convergence, final wiring, and the comparison tool's settings are necessary to interpret the result. Those conditions remain incompletely captured.

<span id="explanation-dac-2026-research1211"></span>

## DCTS: a continuous clock-tree search must still produce a legal, extracted clock network

Clock-tree synthesis (CTS) builds a distribution network from a clock source to sequential loads. Clustering, branching topology, buffer selection, wirelength, slew, insertion delay and skew are coupled: a change that improves one branch can worsen another, increase power, or consume routing resources. The topology is discrete, so a smooth optimization representation is a proposal mechanism rather than the final physical object.

DCTS is described as an end-to-end differentiable CTS framework using a probabilistic graphical model (PGM) to re-parameterize topology choices continuously and jointly optimize topology with buffer sizing. The PGM and gradients may let a global search coordinate choices that conventional sequential stages separate. The implementation must still map the continuous state to legal cells, legal wiring and a realizable clock tree, and must explain how branching, clustering, buffering, constraints and termination are represented.

The first correctness gate is clock-network validity. Check that every required sink is connected exactly as intended, there are no shorts or floating branches, buffer choices exist in the target library, transitions and fanout meet limits, and routing obeys placement, layer, spacing and blockage rules. Then run propagated-clock timing with extracted parasitics, including insertion delay, source latency, skew, setup and hold impact, pulse width, uncertainty and variation. A differentiable objective or pre-route estimate does not establish signoff closure.

The second gate is objective and convergence accounting. Define the PGM variables, probability parameterization, gradient estimator, constraints, initialization, optimizer, stopping rule and whether topology repair or discrete legalization occurs between iterations. Report failed or repaired candidates, convergence traces, seeds, iteration counts and total wall time. If the method uses a surrogate or approximate wire model, measure its error and identify decisions overturned by detailed CTS or extraction.

PPA and speed claims require a common boundary. Report clock power, buffer area, wirelength, total area, timing and skew distributions, violation counts, routing completion and runtime. Runtime should include graph construction, optimization, topology discretization, legalization, buffering, detailed routing, extraction, timing analysis and any failed-candidate retries. A 2.78× speedup on large circuits can mean proposal time only unless the compared commercial or academic flows include equivalent downstream work.

The source reports ISCAS'89 and OpenCores evaluations under ASAP7, competitive PPA against a leading commercial tool, 2.78× speedup on large circuits, and minimum improvements of 20% in delay, 17% in skew, 1% in power and 17% in area plus 1.98× minimum academic-flow speedup. The official description does not provide circuit-by-circuit results, sink counts, clock constraints, library and routing settings, commercial-tool configuration, convergence data, extraction conditions or numerical denominators. The evidence supports differentiable CTS search, not demonstrated signoff-quality clock improvement or general runtime advantage.

<span id="explanation-iccad-2025-1155"></span>

## COPA: pin assignment can target congestion only when legality and downstream routing remain fixed

A feedthrough pin crosses a block boundary so that a connection can enter or leave an internal region. Its boundary location influences which tracks and corridors internal routes can use. Pin assignment is therefore not only a wirelength problem: moving a pin can relieve one demand peak while creating another, alter access at neighboring pins, or change the feasibility of the detailed route.

COPA is described as a Congestion-Oriented Pin Assignment framework for hierarchical IC designs. It formulates feedthrough-pin placement as a nonlinear optimization and iteratively adjusts pin positions using a routing-demand-driven congestion metric and its gradient. The abstract does not expose the pin/legal-site representation, differentiability approximation, demand model, blockages, layer capacities, spacing rules, fixed pins, ordering constraints, or the detailed-routing handoff.

### The optimization must remain a legal pin assignment

Every output pin must lie on an allowed boundary site with the required layer, orientation, spacing, access and electrical/net identity. Feedthrough pins may have ordering, symmetry, keep-out, power-domain, hierarchy and fixed-location constraints. A continuous position update can produce coincident pins, off-grid locations, illegal spacing, swapped connectivity or a candidate that requires a repair step. Report projection/repair frequency, infeasible candidates, pin displacement, boundary overflow and whether the repaired assignment is the one being measured.

### Routing demand is a proxy for actual congestion

Routing demand can estimate how many tracks a set of nets wants in a region; overflow is demand beyond available capacity. The result depends on layer directions, capacity, blockages, via costs, net bounding boxes, timing class and whether demand is local or propagated through neighboring regions. Validate the metric against global routing and detailed-routing outcomes on held-out blocks. Measure total overflow, maximum overflow, overflow distribution, unroutable nets, detours, vias, runtime and convergence—not only the objective gradient.

The abstract reports an average 7.6% reduction in total overflow and a maximum improvement up to 9% relative to initial feedthrough-pin assignments from an unnamed commercial EDA tool. The stored evidence is an institutional abstract only; testcase identities, dimensions, routing capacity, rule deck, baseline settings, wirelength definition and detailed-route success are unresolved. A reduction in an estimated overflow score is not proof of timing closure or final route completion, and “without increasing wirelength” remains an abstract-level claim until named cases and matched constraints are inspected.

Compare COPA with the commercial initial assignment, wirelength-focused assignment, random/legalized assignment and any iterative routing-aware baseline under the same block, netlist, pin sites, layer capacities, congestion estimator, router, timing constraints and stopping/evaluation budget. Report per-case results, worst cases and the complete cost of demand construction, gradient iterations, legalization, routing and repair. Then evaluate propagated timing, slew, capacitance, crosstalk, power and final detailed-route violations with extracted parasitics where relevant.

The evidence supports congestion-oriented feedthrough-pin assignment, not demonstrated signoff-quality routing or timing improvement. The 7.6% average and up-to-9% claims remain withheld pending full-paper testcase, capacity, baseline, legality and detailed-routing conditions; no independent acceptance is recorded.

## How to evaluate a timing improvement

Hold the circuit, timing requirements, library, process assumptions, and physical flow constant. Compare final timing together with area, power, congestion, and remaining violations. State whether reported delays come from early estimates or extracted post-layout behavior.

Include all candidate evaluation and repair costs. For learned or simplified models, examine cases where prediction error changes whether a candidate appears valid. If an improvement depends on a particular activity pattern, operating voltage, or corner condition, retain that condition with the result.

The shared research question is whether earlier joint decisions reduce the cost of obtaining a circuit that meets its actual timing and physical requirements. The methods address different parts of that question and should not be ranked from isolated intermediate scores.

## Compare the results carefully

First identify the inputs and required output quality. Then identify the limited resource: time, memory, communication, energy, circuit area, or correctness coverage. Ask which part of the method reduces that cost and which new cost it adds. Compare numbers only when the experiments hold these conditions sufficiently similar.

A conference description may explain the proposal while omitting the full experiment. An author preprint link may have been coded from its abstract. The source classification does not by itself establish that every table was read. Missing locations remain visible below.

## Complete captured evidence

These are evidence records, not substitutes for the explanations above. Each record preserves its problem, proposed method, measurements, comparison conditions, and source limits. A populated record does not establish that its mechanism has been fully explained or independently verified.

<span id="paper-dac-2026-research2297"></span>

### IR-Drop Aware Global Placement with PDN Optimization and GPU-Accelerated Analysis for Mitigating Global and Local IR-Drop

DAC 2026 · Record: `dac-2026-research2297`

[Read the step-by-step explanation](#explanation-dac-2026-research2297)

**Updated source-backed reading card**

Reviewed 2026-09-08. Deepens the existing IR-drop-aware placement treatment into a paper-level reading; separates GPU-accelerated MNA estimation, PDN path insertion, and local density control from extracted/signoff power-integrity closure, preserves the qualitative violation/wirelength/runtime/routability claims, and makes activity, process, routing and thermal boundaries explicit.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Global and local IR drop interact with cell placement and power-delivery design, while repeated voltage analysis can be too slow for an iterative placement loop.

**Mechanism / artifact:**

Analytical global placement with iterative PDN power-path insertion, GPU-accelerated modified nodal analysis, and node-specific density control based on maximum tolerable load; current modeling, matrix updates, extraction, voltage domains and convergence rules are unspecified.

**Workload — the work tested:**

Standard-cell placement and PDN optimization; designs, netlists, cell powers, activity/current maps, process node, metal stack, voltage domains, IR-drop thresholds, routing constraints and benchmark suite are unspecified.

**Hardware and manufacturing assumptions:**

ASIC placement with power-delivery network and GPU-assisted analysis; resistance/via extraction, source/package model, dynamic activity, voltage/temperature/process corners, GPU model, analysis precision, routing and signoff tools are unspecified.

**Baseline — the comparison method:**

State-of-the-art IR-drop-aware placement

Ordinary placement followed by PDN repair

Ablations of GPU MNA, iterative PDN path insertion and node-specific density control

Same netlist, libraries, constraints, current assumptions, process/metal stack, legalization, extraction, signoff tools and stopping criteria are unspecified

**Reported measurements:**

The official description claims significant reduction in IR-drop violations without additional wirelength, runtime or routability overhead; it supplies no violation counts, worst voltage, thresholds, margins, absolute runtime, GPU speed, area, power, timing, extraction agreement or signoff result.

**Limits on the conclusion:**

GPU acceleration changes solver speed, not model validity. Validate MNA against a reference solver and compare placement-loop voltage estimates with extracted and signoff PDN analyses under identical activity, process, voltage, temperature and metal assumptions.

Node-specific maximum load must correspond to physical current paths, shared segments, vias, neighboring demand, domains and simultaneous switching. A local density bound can shift demand to another bottleneck and is not itself a power-integrity proof.

PDN path insertion can trade voltage margin against routing resources, area, vias, capacitance, timing, thermal and power costs. The official description omits design, current, threshold, process, routing and signoff conditions. The evidence supports coupled placement/PDN optimization, not demonstrated signoff-quality power-integrity closure.

**Source and location**

Evidence tier: Primary captured official DAC description plus existing chapter level conceptual explanation; no full paper extraction, mna validation, routed pdn trace or independent review. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH2297&sess=sess132)

DAC 2026 official description; existing chapter-level IR-drop/placement discussion; captured Problem, Mechanism / artifact, Workload, Hardware, Baseline, Measurements and Limits fields; no manuscript pages or extracted/signoff analysis.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** state-of-the-art IR-drop-aware placement techniques

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH2297&sess=sess132

**Hardware or process assumptions:** Chip placement and PDN with GPU-accelerated analysis; extraction, metal layers, voltage domains, and signoff conditions are unspecified.

**Limits:** No violation counts, voltage thresholds, design sizes, runtime, GPU, or wirelength values are supplied.

MNA accuracy and density constraints may differ from signoff power-integrity analysis.

Official description only; placement and signoff claims require paper-level verification.

**Method or artifact:** Analytical global placement with PDN optimization, GPU-accelerated MNA voltage-drop analysis, and node-specific IR-drop-aware density control.

**Metrics:** Significant reduction in IR-drop violations claimed

No additional wirelength, runtime, or routability overhead claimed

**Problem:** Global and local IR-drop interact with cell placement and power-delivery design, while accurate analysis can be too slow for iterative placement.

**Workload or benchmark:** Physical-design placement with power-delivery networks; designs, process node, current maps, IR-drop thresholds, and baseline tools are unspecified.

</details>

<span id="paper-dac-2026-research1317"></span>

### HyPAS: A Hybrid Optimization Framework for Placement and Sizing Co-Optimization

DAC 2026 · Record: `dac-2026-research1317`

[Read the step-by-step explanation](#explanation-dac-2026-research1317)

**Updated source-backed reading card**

Reviewed 2026-09-08. Deepens the existing HyPAS treatment into a paper-level reading; separates differentiable surrogate guidance, straight-through discrete sizing, and OpenROAD legality/repair from extracted timing, power, routing and signoff closure, preserves the qualitative PPA/runtime claims, and makes training, process and evaluation boundaries explicit.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Incremental placement, sizing and buffering optimize coupled PPA objectives through isolated discrete stages, while smooth differentiable placement can be fragile near legality and timing-closure boundaries.

**Mechanism / artifact:**

Hybrid differentiable/discrete placement and sizing using DREAMPlace gradients, a GNN timing-power surrogate, a straight-through estimator for discrete library parameters, and OpenROAD legality, timing-closure and buffer-aware repair; surrogate training, action space and convergence rules are unspecified.

**Workload — the work tested:**

Standard-cell placement and gate-sizing benchmarks compared with ICCAD 2025 CAD Contest results and state-of-the-art methods; designs, netlists, libraries, process node, loads, corners, timing constraints, training/test split and PPA definitions are unspecified.

**Hardware and manufacturing assumptions:**

ASIC physical-design flow using OpenROAD and DREAMPlace with standard-cell libraries and routing/extraction; process, PDK, cell rows, clock constraints, parasitics, signoff tools, compute hardware and runtime boundary are unspecified.

**Baseline — the comparison method:**

Conventional incremental discrete placement/sizing

OpenROAD without differentiable refinement

Differentiable placement/sizing without discrete repair

ICCAD 2025 CAD Contest and state-of-the-art methods

Same designs, netlist, library, process, clocks, loads, corners, routing/extraction flow, stopping criterion, hardware and end-to-end timing boundary are unspecified

**Reported measurements:**

The official description claims superior PPA gains with competitive runtime against ICCAD 2025 contest results and state-of-the-art methods; it supplies no numeric area, timing/slack, power, wirelength, congestion, violation, repair, surrogate-error or runtime result.

**Limits on the conclusion:**

A differentiable candidate must be mapped to legal discrete cells and placement, then checked for overlap, row/site rules, connectivity, slew, fanout, setup/hold, routing and extraction. Straight-through gradients do not establish exact signoff behavior.

Validate the GNN timing-power surrogate on held-out designs, placements, cell choices and corners with error, rank, calibration and overturned-decision statistics. Include label-generation, legalization, repair, routing, extraction and repeated-evaluation costs in the end-to-end runtime.

The qualitative PPA/runtime claims omit design, library, process, timing, corner, routing, surrogate and measurement conditions. The evidence supports a hybrid placement-and-sizing search direction, not demonstrated signoff-quality PPA improvement or runtime advantage across designs and technologies.

**Source and location**

Evidence tier: Primary captured official DAC description plus existing chapter level conceptual discussion; no full paper extraction, surrogate validation, routed/signoff trace or independent review. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH1317&sess=sess132)

DAC 2026 official description; existing chapter-level HyPAS discussion; captured Problem, Mechanism / artifact, Workload, Hardware, Baseline, Measurements and Limits fields; no manuscript pages or reproduced physical-design run.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** ICCAD 2025 CAD Contest results

state-of-the-art placement/sizing methods

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH1317&sess=sess132

**Hardware or process assumptions:** Standard-cell placement, timing closure, buffering, and library parameters; OpenROAD/DREAMPlace tooling, process, and signoff extraction are unspecified.

**Limits:** No PPA values, design sizes, timing constraints, runtime, surrogate error, or contest configurations are supplied.

Differentiable surrogates and signoff repair may behave differently across libraries and process nodes.

Official description only; physical-design validity requires paper-level verification.

**Method or artifact:** Hybrid discrete/differentiable placement and sizing, OpenROAD signoff legality/repair, DREAMPlace gradients, GNN timing-power surrogate, and straight-through estimator.

**Metrics:** Superior PPA gains claimed qualitatively

Competitive runtime claimed qualitatively

**Problem:** Incremental placement, sizing, and buffering flows use isolated heuristic stages and timing analyses, while differentiable placement can be fragile near legality and timing-closure boundaries.

**Workload or benchmark:** Physical-design placement and gate-sizing benchmarks compared with ICCAD 2025 CAD Contest and state-of-the-art methods; designs, process node, and PPA metrics are unspecified.

</details>

<span id="paper-dac-2026-research1211"></span>

### DCTS: Differentiable Clock Tree Synthesis Based on Probabilistic Graphical Model

DAC 2026 · Record: `dac-2026-research1211`

[Read the step-by-step explanation](#explanation-dac-2026-research1211)

**Updated source-backed reading card**

Reviewed 2026-09-08. Deepens the existing DCTS treatment into a paper-level reading; separates PGM-based continuous topology search and joint buffer sizing from legal clock construction, extracted timing, skew, routing, convergence and end-to-end runtime, preserves the reported 2.78x, 1.98x, 20%, 17%, 1% and 17% claims, and makes commercial-tool comparison boundaries explicit.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Clock-tree synthesis jointly chooses discrete clustering, topology and buffers under coupled timing, skew, power, area and routing objectives, while sequential heuristic stages can become trapped in local optima.

**Mechanism / artifact:**

End-to-end differentiable CTS using a probabilistic graphical model to continuously represent discrete topology choices and co-optimize topology with buffer sizing; parameterization, gradient estimator, legalization, repair and convergence rules are unspecified.

**Workload — the work tested:**

ISCAS'89 and OpenCores benchmark circuits under ASAP7; sink counts, clock sources, libraries, constraints, loads, corners, routing settings, circuit split and large-scale designation are unspecified.

**Hardware and manufacturing assumptions:**

ASIC CTS flow with clock routing, standard-cell buffers and extracted timing under ASAP7; PDK, parasitic extraction, metal stack, variation, commercial-tool configuration, compute hardware and downstream signoff tools are unspecified.

**Baseline — the comparison method:**

Leading commercial CTS tool

State-of-the-art academic CTS solutions

Same circuits, libraries, clock constraints, loads, corners, routing/extraction/signoff flow, hardware, stopping rule and complete runtime boundary are unspecified

**Reported measurements:**

The official description reports competitive commercial-tool PPA, 2.78x speedup on large circuits, and minimum academic-solution improvements of 20% delay, 17% skew, 1% power, 17% area and 1.98x speedup; it supplies no circuit-level values, distributions, violations, convergence, routing or extraction result.

**Limits on the conclusion:**

A continuous topology must be discretized into a legal clock network. Validate sink connectivity, buffer availability, slew, fanout, pulse width, routing rules, extracted insertion delay, skew, setup/hold, uncertainty and variation; a differentiable or pre-route objective is not signoff closure.

Expose PGM variables, probability parameterization, gradient estimator, constraints, initialization, optimizer, stopping rule, repair, seeds, iterations and candidate failures. Include topology construction, legalization, buffering, routing, extraction, timing analysis and retries in runtime, and validate any surrogate against detailed CTS.

The reported 2.78x, 1.98x, 20%, 17%, 1% and 17% claims lack circuit-level data, clock constraints, library, routing, commercial-tool, convergence, extraction and timing conditions. The evidence supports differentiable CTS search, not demonstrated signoff-quality clock improvement or general runtime advantage.

**Source and location**

Evidence tier: Primary captured DAC official description plus existing chapter level conceptual discussion; no full paper extraction, clock tree trace, commercial tool configuration or independent review. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH1211&sess=sess136)

DAC 2026 official description; existing chapter-level DCTS discussion; captured Problem, Mechanism / artifact, Workload, Hardware, Baseline, Measurements and Limits fields; no manuscript pages or reproduced CTS run.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** leading commercial CTS tool

state-of-the-art academic CTS solutions

**Evidence locators:** Not established in the captured evidence.

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH1211&sess=sess136

**Hardware or process assumptions:** ASAP7 technology-node physical-design flow and clock-tree synthesis objectives; commercial-tool comparison conditions are not fully exposed.

**Limits:** The official description does not provide circuit-by-circuit results, clock-tree constraints, convergence behavior, or commercial-tool configuration; independent paper-level verification remains required.

**Method or artifact:** End-to-end differentiable CTS using a probabilistic graphical model to represent discrete topology search continuously and co-optimize topology with buffer sizing.

**Metrics:** 2.78x speedup on large circuits

minimum 20% delay improvement

minimum 17% skew improvement

minimum 1% power improvement

minimum 17% area improvement

minimum 1.98x speedup over academic solutions

PPA

**Problem:** Traditional CTS splits clustering, topology generation, and buffering into sequential stages that can become trapped in local optima; differentiable methods struggle with dynamic topology changes.

**Workload or benchmark:** ISCAS'89 and OpenCores benchmark circuits under the ASAP7 technology node; large-scale circuit timing/power/area evaluation.

</details>

<span id="paper-dac-2026-research1080"></span>

### AccDRC: FPGA Acceleration for VLSI DRC with Cell-Aware Layout Partitioning

DAC 2026 · Record: `dac-2026-research1080`

[Read the step-by-step explanation](#explanation-dac-2026-research1080)

**Updated source-backed reading card**

Reviewed 2026-09-09. Deepens the AccDRC treatment into a paper-level reading; separates cell-aware layout partitioning, locality-preserving FPGA loading, reconfigurable checking and sparse writeback from rule/deck equivalence, geometric boundary handling, device/resource conditions and complete DRC runtime, while preserving the source's two reported speedup ranges.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

VLSI design-rule checking is computationally intensive, and existing accelerators may fail to exploit layout parallelism, structural rule commonality and sparse violation outcomes.

**Mechanism / artifact:**

Software–hardware co-designed FPGA DRC accelerator with cell-aware balanced layout partitioning, data preparation/task encapsulation, locality-preserving loading, a unified reconfigurable check core and sparse-result writeback; rule implementation, halo handling and FPGA configuration are unspecified.

**Workload — the work tested:**

VLSI layout DRC with multiple rules and sparse violation outcomes; layout sizes, layers, hierarchy, rule deck/process, rule coverage, partition boundaries, violation density, input format and correctness corpus are unspecified.

**Hardware and manufacturing assumptions:**

FPGA-based DRC dataflow with host software for layout preparation and result handling; FPGA family/device, frequency, LUT/FF/BRAM/DSP resources, memory/bandwidth, host CPU, interconnect, bitstream/configuration, power and process technology are unspecified.

**Baseline — the comparison method:**

CPU-based KLayout DRC tool

GPU-based OpenDRC tool

Same layouts, rule deck, process, tolerance, input/output format, host preprocessing, rule coverage, correctness checks, software versions and timing boundary are unspecified

**Reported measurements:**

The source reports 522.11x–1071.03x speedup over KLayout and 9.62x–26.07x speedup over OpenDRC, but does not report absolute runtime, layout/rule conditions, rule-equivalence errors, FPGA device/resource use, bandwidth, power/energy, memory, preprocessing/result costs or per-layout distribution.

**Limits on the conclusion:**

Cell-aware partitioning must preserve geometry and rule context across boundaries, hierarchy, layers, vias, nets, coordinate precision and neighbor halos. Verify balanced task units, boundary replication, candidate pairs, overflow and complete violation locations on adversarial layouts; partition balance alone does not establish DRC correctness.

An FPGA check core must match trusted rule semantics, including threshold inclusivity, spacing, width, enclosure, notch, density, connectivity, waivers and error reporting. Compare violation sets against KLayout or another trusted implementation and report false positives, false negatives, unsupported rules, duplicates, ordering differences and fallback behavior.

The source supports FPGA-accelerated, cell-aware DRC as a constrained implementation direction, not demonstrated signoff-equivalent DRC replacement or portable 522.11x–1071.03x/9.62x–26.07x acceleration across rule decks and layouts. Device/resource conditions, rule coverage, equivalence and complete preprocessing/transfer/writeback/runtime accounting remain unresolved.

**Source and location**

Evidence tier: Primary captured official DAC description plus existing authored drc/physical design explanation; no full paper extraction, reproduced FPGA run, rule deck equivalence validation or signoff replacement evidence. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH1080)

DAC 2026 official description, first and final paragraphs; existing placement/routing/timing and DRC framing; captured Problem, Mechanism / artifact, Workload, Hardware, Baseline, Measurements and Limits fields; no full manuscript, rule table, FPGA resource report or independent equivalence run.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** CPU-based KLayout DRC tool

GPU-based OpenDRC tool

**Evidence locators:** Not established in the captured evidence.

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH1080&sess=sess156

**Hardware or process assumptions:** Not established in the captured evidence.

**Limits:** The description does not state FPGA device/resource use, rule-suite coverage, layout sizes, or checking-equivalence details.

**Method or artifact:** FPGA DRC accelerator with cell-aware balanced partitioning, locality-preserving data loading, reconfigurable checking, and sparse-result writeback.

**Metrics:** 522.11–1071.03X speedup over KLayout

9.62–26.07X speedup over OpenDRC

**Problem:** Design-rule checking is increasingly compute-intensive and existing accelerators fail to exploit layout parallelism and sparse violations fully.

**Workload or benchmark:** VLSI layout design-rule checking with multiple rules and sparse violation outcomes.

</details>

<span id="paper-iccad-2025-1155"></span>

### COPA: A Congestion-Oriented Pin Assignment Framework for Intra-Block Physical Design Optimization

ICCAD 2025 · Record: `iccad-2025-1155`

[Read the step-by-step explanation](#explanation-iccad-2025-1155)

**Updated source-backed reading card**

Reviewed 2026-09-09. Deepens the COPA institutional-abstract treatment into a paper-level reading; separates gradient-based routing-demand optimization from pin legality, congestion-model validity, detailed-routing completion, wirelength/timing claims and baseline conditions, while preserving the 7.6% average and up-to-9% abstract claims as withheld pending testcase and routing evidence.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Wirelength-focused feedthrough-pin assignment can overlook congestion inside hierarchical IC blocks and make internal routing inefficient.

**Mechanism / artifact:**

COPA, a gradient-based nonlinear optimization framework that adjusts feedthrough-pin positions using a routing-demand-driven congestion metric; pin-site representation, legality projection, demand model, gradients, fixed constraints and routing handoff are unspecified.

**Workload — the work tested:**

Industrial hierarchical IC testcases with intra-block feedthrough pins; identities, block/netlist sizes, pin counts, layer capacities, blockages, process/rule deck, congestion distribution, router, timing constraints and testcase split are unspecified.

**Hardware and manufacturing assumptions:**

Physical-design flow for hierarchical IC blocks with legal boundary pin sites and multi-layer routing; process, metal stack, track capacities, via/spacing rules, compute platform, runtime budget, global/detailed router and extracted-parasitic setup are unresolved.

**Baseline — the comparison method:**

Initial feedthrough-pin assignments from an unnamed commercial EDA tool

Wirelength-focused assignment

Same block, netlist, pin sites, layer capacities, congestion estimator, router, legalization, timing constraints and evaluation budget are unspecified

**Reported measurements:**

The institutional abstract reports an average 7.6% reduction in total overflow and a maximum improvement up to 9% versus initial commercial-tool feedthrough-pin assignments, while stating no wirelength increase. The packet withholds these headline percentages pending testcase, capacity and baseline conditions; no absolute overflow, wirelength, route completion, timing, via, detour or runtime data are reported.

**Limits on the conclusion:**

A continuous pin update must become a legal assignment: allowed boundary sites, layer/orientation, spacing, access, net identity, ordering, symmetry, hierarchy and fixed-pin constraints must be preserved. Report infeasible candidates, projection/repair frequency, pin displacement and whether repaired or original assignments are measured.

Routing-demand overflow is a proxy. Validate it against global and detailed routing under the same rule deck, layer directions, capacities, blockages, via costs and router; report overflow distribution, unroutable nets, detours, vias, timing, slew and convergence. Overflow reduction is not proof of timing closure or final detailed-routing success.

The institutional abstract supports congestion-oriented feedthrough-pin assignment, but the 7.6% average and up-to-9% claims remain withheld pending testcase, capacity, baseline, legality and detailed-routing conditions. Wirelength preservation is abstract-level, and the evidence does not establish signoff-quality routing or timing improvement or independent acceptance.

**Source and location**

Evidence tier: Primary captured institutional abstract plus bounded source recovery assessment and existing placement/routing explanation; no full paper extraction, reproduced optimization, detailed route equivalence or timing validation. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://scholar.nycu.edu.tw/en/publications/copa-a-congestion-oriented-pin-assignment-framework-for-intra-blo/)

NYCU institutional abstract; iccad/data/copa-primary-recovery-v1.json; captured Problem, Mechanism / artifact, Workload, Hardware, Baseline, Measurements and Limits fields; no full manuscript, named testcases, routing trace or independent acceptance.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_institutional_abstract

**Baselines:** Initial feedthrough-pin assignments from an unnamed commercial EDA tool

**Evidence locators:** **Fields:** problem

method_or_artifact

workload_or_benchmark

baselines

limits

**Location:** NYCU Abstract; iccad/data/copa-primary-recovery-v1.json

**Evidence url:** https://scholar.nycu.edu.tw/en/publications/copa-a-congestion-oriented-pin-assignment-framework-for-intra-blo/

**Hardware or process assumptions:** Process, routing capacity, compute platform and runtime budget unresolved.

**Limits:** Overflow reduction is not proof of timing closure or final detailed-routing success. Headline percentages withheld pending testcase, capacity and baseline conditions; no full-text or independent acceptance.

**Method or artifact:** Gradient-based adjustment of feedthrough-pin positions using a routing-demand congestion objective.

**Metrics:** Not established in the captured evidence.

**Problem:** Wirelength-focused pin assignment can overlook congestion inside hierarchical design blocks.

**Workload or benchmark:** Industrial testcases; identities and design sizes unspecified in abstract.

</details>

#### Additional source assessment

This separately recorded check is dated 2026-09-06. It supplements the original record above and retains its own scope and uncertainty.

[Assessment record](../../iccad/data/copa-primary-recovery-v1.json)

[Assessed source](https://scholar.nycu.edu.tw/en/publications/copa-a-congestion-oriented-pin-assignment-framework-for-intra-blo/)

**Extraction scope**

Institutional abstract, title, seven authors and DOI; author-lab listing confirms conference identity. No full manuscript located on lab page.

**Headline metric status**

withheld_pending_testcase_and_routing_conditions

**Independent review status**

pending

<span id="paper-iccad-2025-1111"></span>

### Parallel Non-Integer Multiple-Cell-Height Node Remapping

ICCAD 2025 · Record: `iccad-2025-1111`

**Problem:**

Exhaustive node and fanin mapping enumeration makes timing-aware remapping expensive for non-integer multiple-cell-height circuits.

**Mechanism / artifact:**

Timing-critical-node prioritization through parallel longest-path-first and iterative minimum-slack-first remapping schemes.

**Workload — the work tested:**

Non-integer multiple-cell-height standard-cell designs; named benchmark circuits not established by abstract.

**Hardware and manufacturing assumptions:**

Compute platform, process library and thread count not specified in abstract.

**Baseline — the comparison method:**

Not established in the captured evidence.

**Reported measurements:**

Not established in the captured evidence.

**Limits on the conclusion:**

Reported average speedup withheld until baseline, compute budget and placement-quality criteria are known. Remapping runtime is not end-to-end implementation time or chip performance. No full-manuscript extraction or independent acceptance.

**Source and location**

Evidence tier: Medium institutional abstract. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://scholars.lib.ntu.edu.tw/entities/publication/f36a23c3-8e05-474a-b3a9-b7ff2802d0ae)

**Fields:** problem

method_or_artifact

workload_or_benchmark

limits

**Location:** NTU publication Abstract and citation metadata; iccad/data/nimch-primary-recovery-v1.json

#### Additional source assessment

This separately recorded check is dated 2026-09-06. It supplements the original record above and retains its own scope and uncertainty.

[Assessment record](../../iccad/data/nimch-primary-recovery-v1.json)

[Assessed source](https://scholars.lib.ntu.edu.tw/entities/publication/f36a23c3-8e05-474a-b3a9-b7ff2802d0ae)

**Extraction scope**

NTU publication title, four authors, DOI and abstract; not manuscript or thesis extraction.

**Headline metric status**

withheld_pending_baseline_platform_and_quality_conditions

**Independent review status**

pending

#### Additional source assessment

This separately recorded check is dated 2026-09-06. It supplements the original record above and retains its own scope and uncertainty.

[Assessment record](../../iccad/data/nimch-thesis-primary-recovery-v1.json)

[Assessed source](https://tdr.lib.ntu.edu.tw/handle/123456789/99251?mode=full)

**Extraction scope**

NTU thesis repository metadata and English abstract; no thesis PDF extraction and no conference-paper full text.

**Conditions**

The thesis abstract names timing-aware remapping, non-integer multiple-cell-height standard cells, and placement-quality preservation, but does not specify benchmark circuits, machine, thread count, baseline identity, or quality tolerance.

**Headline metric status**

withheld_pending_conference_manuscript_reconciliation

**Independent review status**

pending

## What remains to establish

Resolve unspecified workloads, comparison methods, resource budgets, and source locations before generalizing a reported gain. Multiple papers in this selected sample permit comparison of mechanisms, but do not by themselves establish recurrence across years or a long-term trend.

[All subthemes](../expanded-taxonomy-v1.md) · [Research directions](../directions/README.md)
