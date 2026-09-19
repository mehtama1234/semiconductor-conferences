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
