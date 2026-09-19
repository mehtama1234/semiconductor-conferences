# Partitioning and placement

This subject has 3 records in the selected sample. This page explains where it fits, then presents all captured paper evidence without shortening the measurements or limitations.

[Definitions used in the paper records](../reading-guide-v1.md)

## Understand the parent subject first

- [Design methodology and tooling](../themes/design-methodology-and-tooling.md)
- [Physical design and manufacturing](../themes/physical-design-and-manufacturing.md)

## Start with the decisions, not the tool names

Partitioning decides which group each circuit element belongs to. Placement decides where each element sits. These are different decisions: grouping two elements together does not determine the distance between their terminals, and placing them nearby does not guarantee that a legal wire can connect them.

A connection can involve more than two elements. A **hypergraph** represents that directly: vertices represent elements, and a hyperedge represents one connection involving a set of elements. A partition boundary cuts a connection when its elements belong to different groups. Reducing such crossings can be useful, but putting everything in one group is not a useful solution when each group has a capacity limit. The optimization must account for both connectivity and capacity.

Physical placement introduces additional constraints. Elements occupy area and cannot overlap in a finished layout. Their terminals have particular positions. Rotating a large block changes those positions even if its center remains fixed. In a stacked design, choosing a layer also changes which connections must cross between layers. A useful early estimate must retain enough of these facts to guide the next design decision.

## iHyperG: update the existing partition

[iHyperG's captured record](../observed-subthemes/partitioning-and-placement.md#paper-dac-2026-research223) is supplemented here by the recovered manuscript. Sections 4–5, PDF pages 2–5, describe separate storage for changed connections and refinement focused on vertices whose movement can reduce partition crossings. The method first removes excess weight from overloaded partitions into a temporary group, then assigns its vertices to feasible partitions. This temporary group is not an extra final partition.

Section 6, PDF page 5, specifies 18 ISPD98-derived circuits enlarged 100–1000 times through random insertions, an A6000 with 48 GB memory, 3% allowed imbalance, and ten-run averages. Table 1, PDF page 6, uses two partitions and 100 iterations of 25 modifications each. It reports average speedups of 190.17× for modification and 82.82× for partitioning against HyperG rebuilding and repartitioning. These are separate timings, not factors to multiply. The baseline extension is acknowledged as potentially unoptimized.

The evidence supports fast updates under this constructed workload, not equivalent speedups for complete chip design or all real modification sequences. The implementation has not been reproduced here. [Author manuscript, Sections 4–6 and Table 1](https://tsung-wei-huang.github.io/papers/2026-DAC-iHyperG.pdf#page=5).

<span id="explanation-dac-2026-research223"></span>

### iHyperG: incremental partitioning is useful only when the update representation preserves the partitioning problem

#### Start with what partitioning must maintain

A hypergraph has vertices representing objects and hyperedges representing connections that can contain more than two objects. A k-way partition assigns every vertex to one of k groups. The partitioner normally tries to keep groups within a balance limit while reducing the number or weight of hyperedges that cross group boundaries. A crossing hyperedge can increase communication, cut size, or a later physical-design cost, depending on the application.

In an optimization loop, the hypergraph does not stay fixed. A circuit transformation may add or remove a vertex, add or remove a pin from a hyperedge, change a weight, or change the balance requirement. Rebuilding the entire graph representation and recomputing a partition after every edit repeats work that the edit did not invalidate. Incremental partitioning tries to update only the changed representation and the part of the solution that may have become wrong.

The central correctness requirement is therefore not merely speed. The incremental state must remain equivalent to the current hypergraph, and the selective refinement must examine every vertex whose movement could matter under the chosen objective and balance constraint. If the update structure omits a changed incidence or the refinement scope omits a newly critical vertex, a fast result can be a partition of an incomplete problem.

#### What the delta structure changes

The recovered manuscript describes a delta-based GPU hypergraph data structure. The base structure stores the unchanged graph, while a separate representation records changed connections. This can avoid rewriting large adjacency structures when an edit touches only a small portion of the hypergraph. The implementation still needs defined rules for additions, deletions, weight changes, duplicate pins, empty or singleton hyperedges, and the point at which accumulated deltas are merged into the base structure.

The update cost depends on edit locality and representation size. A small number of edits concentrated in a few connections may fit the intended fast path. A long sequence of edits may make the delta structure large, reduce locality, increase memory use, or require a rebuild. Report both per-update cost and amortized cost over a sequence, including compaction or reconstruction. A single small modification is not a complete dynamic-workload evaluation.

#### Rebalancing and refinement are different operations

The described algorithm first removes excess weight from overloaded partitions into a temporary group, then assigns those vertices to feasible partitions. This is the rebalancing step. The temporary group is an intermediate holding area, not an additional final partition. This step addresses feasibility: every final partition must satisfy the allowed imbalance. It does not by itself minimize cut cost.

After feasibility is restored, the algorithm refines vertices identified as cut-critical. A vertex is relevant when moving it could reduce a crossing hyperedge or improve the objective without violating balance. Restricting refinement can reduce work, but the method must define how criticality is detected, how ties are resolved, how moves are ordered, whether moves are accepted greedily, and how the process stops. A one-pass procedure may be appropriate for the intended update regime, but it can differ from a full iterative partitioner when several moves interact.

This creates two separate quality checks. First, the final assignment must satisfy balance and cover every vertex exactly once. Second, its cut quality must be compared with a specified reference under the same partition count, weights, imbalance allowance and stopping rule. “Comparable quality” cannot be assessed from runtime alone.

#### GPU execution adds consistency and memory questions

GPU parallelism can process changed connections and candidate moves concurrently, but concurrent updates may conflict when several vertices affect the same partition weights or hyperedge state. The implementation needs a defined synchronization or atomic-update rule and a deterministic or statistically characterized result under different execution orders. It must also state whether the base graph, delta graph, partition labels, weights and temporary group fit in device memory.

The relevant hardware cost includes host-to-device transfer, allocation, synchronization, kernel launch, temporary storage, compaction, and any CPU work around the GPU kernels. A modification speedup measured only after data is resident on an A6000 is different from end-to-end speedup in a CAD loop that creates edits on the host and consumes the updated partition elsewhere.

#### Read the reported experiment at its actual boundary

The recovered Sections 4–6 and Table 1 describe 18 ISPD98-derived circuits enlarged by random insertions from 100× to 1000×, an NVIDIA A6000 with 48 GB memory, a 3% allowed imbalance, ten-run averages, two partitions, and 100 iterations of 25 modifications each. These conditions make the result more concrete than the official card, but they also define the tested boundary. Random insertions may not represent edits produced by real synthesis, placement, timing or optimization loops. Two-way partitioning does not establish behavior for arbitrary k. Ten-run averages do not show tail latency or variance unless those are reported.

The reported 190.17× modification speedup and 82.82× partitioning speedup are separate stages. They must not be multiplied into a claimed end-to-end speedup. The comparison is against HyperG rebuilding and repartitioning, and the manuscript notes that the baseline extension may not be optimized. A fair comparison should use equivalent graph representations, update semantics, quality targets, device-resident or end-to-end timing boundaries, and the same edit sequence. Report cut metrics, balance violations, memory, throughput, per-update latency and rebuild frequency alongside the two stage timings.

#### What remains open

The evidence supports the mechanism and the reported constructed experiment, not universal incremental partitioning performance. Reproduction is still pending. The important open tests are real edit traces, larger and different k-way settings, adversarial or nonlocal edits, long delta sequences, compaction behavior, multiple GPUs, end-to-end host/device timing, and quality distributions rather than only average speedups. The 190.17× and 82.82× numbers are evidence for reduced work under the stated conditions, not evidence that a complete CAD optimization loop is 190× or 83× faster.

<span id="explanation-dac-2026-research934"></span>

### ATOM-3D: orientation-aware placement must preserve the physical meaning of pins, layers, and connections

#### Why three-dimensional placement changes the problem

Placement assigns coordinates to circuit objects subject to non-overlap, area, design-rule, timing and routing constraints. In a heterogeneous three-dimensional chip, objects may occupy different dies or layers and communicate through vertical terminals or other interconnect structures. Partitioning decides which objects belong to which layer or region; placement decides their positions; orientation decides how each macro’s local coordinate system is rotated or reflected. These choices interact because a layer assignment changes which connections cross vertically and an orientation changes where the connection pins appear.

A macro cannot be represented adequately by its center alone. Two macros with the same center and outline can expose their pins on different sides after rotation. A wire-length model using only center-to-center distance can therefore prefer a placement that looks geometrically close while making actual terminals harder to connect. ATOM-3D is described as an analytical, differentiable, orientation-aware mixed-size placer that combines partition, position and orientation decisions, then adjusts the partition to compensate for wire-length estimation deviations.

#### What the objective must contain

An analytical placer optimizes a mathematical objective rather than directly running detailed routing at every step. The objective should state how it represents net or hyperedge wire length, pin locations, macro overlap, density, layer transitions, vertical terminals, congestion, timing-critical connections and orientation constraints. If a differentiable relaxation permits continuous coordinates or orientation variables, the method must explain how those variables are converted into legal discrete placements and how the conversion changes the objective.

“Differentiable” means that the optimizer can calculate how a small modeled change affects the objective. It does not mean that the final layout is legal, routed, or timing-clean. A smooth wire-length estimate can guide search while missing discrete blockages, routing tracks, via limits, pin access, clock structures, power delivery, thermal constraints or design-rule checks. The post-placement adjustment is therefore part of the method’s correctness boundary, not an optional presentation detail.

#### Partition and orientation are coupled decisions

If a macro is assigned to a die, the locations and cost of its connections depend on both the destination layer and its orientation. Optimizing layer assignment first and orientation later can trap the search in a poor local arrangement. A joint method can evaluate these variables together, but it must show how it avoids illegal overlaps, impossible terminal access and inconsistent layer capacity during the optimization.

The partition-adjustment step needs a precise trigger and objective. It may move a macro between layers when the estimated wire cost differs from a more accurate calculation, but such a move can change density, vertical interconnect demand, thermal load, timing, and the orientation choices of neighboring macros. Report whether the adjustment is one pass or iterative, whether it can undo earlier decisions, and whether the final coordinates are re-optimized after reassignment.

#### Separate modeled quality from physical signoff

Wire length is not the same as routed delay. A shorter geometric connection can be slower if it is congested, requires extra vias, uses a poor layer, has limited pin access, or crosses a timing-critical path with unfavorable buffering. In 3D, vertical connections also have capacity, alignment, reliability, thermal and manufacturing constraints. The evaluation should therefore distinguish the analytical objective from routed wire length, congestion, timing, power, via count, thermal behavior, design-rule violations and yield.

The claimed “8% higher quality” and “2% over the best published method” require the quality metric, direction, aggregation, benchmark set and statistical treatment. They must not be rewritten as 8% shorter wires or 2% better timing. The 1.6× runtime speedup requires the same hardware, stopping criterion, legalization, partition adjustment, initialization and post-processing boundary for each baseline.

#### The comparison must expose the 3D conditions

A 2D analytical placer and an orientation-oblivious 3D placer are useful conceptual baselines, but a complete comparison must identify the stack topology, number of dies, face-to-face bonding assumptions, terminal pitch, layer capacities, macro dimensions, cell mix, netlist, pin locations, allowed orientations, routing resources, via rules and timing constraints. It should include a placement with fixed orientation, a placement with independent orientation, and a joint placement so the value of orientation awareness is isolated.

Report legality rate, overlap, wire-length components, congestion, via or vertical-terminal demand, timing slack, power or thermal measures, runtime, memory, convergence failures, DRC violations and post-route correlation. Test different stack sizes, macro proportions, pin distributions, critical-path weights and design-rule constraints. A method that improves a relaxed objective but produces more failed legalizations has not shown a physical-design improvement.

#### What the captured evidence establishes

The official description supports an orientation-aware analytical 3D mixed-size placement direction for face-to-face heterogeneous chips and reports author-claimed quality and runtime comparisons. It does not define the quality measure or provide paper-page evidence for wire length, congestion, timing, via behavior, design-rule checking, manufacturing conditions or signoff correlation. The evidence supports joint modeling of partition, position and orientation, not demonstrated routable or manufacturable 3D placement improvement.

## ATOM-3D: orientation changes the placement problem

A large predesigned circuit block is commonly called a macro; mixed-size placement handles such blocks together with smaller cells. Orientation matters because connections terminate at pins, not at block centers. A placement estimate that ignores pin movement under rotation can prefer an arrangement whose real connection distances are worse.

[ATOM-3D](../observed-subthemes/partitioning-and-placement.md#paper-dac-2026-research934) targets heterogeneous chips bonded face-to-face through terminals. Its official description combines partition assignment, position, and macro orientation in one analytical global-placement framework, followed by a partition adjustment to compensate for wire-length estimation deviations. Here, analytical means optimizing a mathematical description of placement cost; differentiable means that small changes to the modeled variables have computable effects on that cost.

The description reports 8% higher quality than the ICCAD 2023 contest winner, 2% over the best published method, and 1.6× runtime speedup. It does not define the quality measure or expose the detailed comparison conditions. Those percentages must therefore remain author claims about an unspecified quality measure, not be rewritten as wire-length or timing reductions. This source establishes more mechanism than the older captured card, but does not supply paper-page evidence or final manufacturing validation. [Official ATOM-3D description](https://63dac.conference-program.com/presentation/?id=RESEARCH934&sess=sess132).

<span id="explanation-dac-2026-research954"></span>

### Module-level placement: deformation is useful only if the abstraction preserves the decisions that matter later

#### What module-level placement simplifies

A physical design may contain millions of cells, but an early planning stage often groups related cells into modules. A module can be treated as one object with an area, a shape, pins or boundary terminals, and connections to other modules. This reduces the number of positions and shapes that the optimizer must consider. It also removes information: the module abstraction does not tell the early placer where every internal cell, internal wire, or internal pin will eventually be placed.

The reported method uses force-based deformation. A force-based placer represents attraction or repulsion between connected objects and uses those forces to move them. Deformation allows a module’s width and height, or aspect ratio, to change while preserving a stated area or other constraint. This is more expressive than moving fixed rectangles, but it still optimizes a model of the module, not the final standard-cell placement and routed layout.

#### Area preservation is not shape or routability preservation

Area is the product of width and height. Two modules can have the same area while having very different aspect ratios, pin distributions, boundary congestion and internal routing difficulty. A wide, short module may connect well to horizontal neighbors and poorly to vertical ones. A tall, narrow version may reverse that behavior. If the model preserves area but not terminal locations, pin access, internal hierarchy or blockages, the resulting estimate can be systematically wrong even when its area constraint is exact.

The method must define what can deform, which dimensions are bounded, how pins move with the shape, whether orientation is allowed, and whether a module can overlap another during the optimization. It must also state when shapes are legalized and whether the final legal shape is re-evaluated. A smooth deformation path can find a useful early arrangement while producing a shape that cannot be implemented under placement rows, routing tracks, macro halos or power-grid constraints.

#### Understand the reported wire-length metric

The inter-module half-perimeter wire length (HPWL) of a connection is the width plus height of the smallest axis-aligned rectangle containing its pins. HPWL is fast and useful for ranking candidate placements. It is not the length of a routed wire, and it is not a timing measurement. It omits routing detours, congestion, layer assignment, via cost, buffering, resistance, capacitance, coupling and pin-access failures.

The reported approximately 3% error therefore needs a reference and denominator: error relative to which detailed placement or wire-length calculation, over which designs and nets, with what mean or percentile aggregation? A low average HPWL error can hide large errors on critical or congested nets. The evaluation should report per-design and per-net distributions, critical-net error, rank correlation, congestion correlation and whether the abstraction selects the same candidate that survives detailed implementation.

#### Interpret longest-net recovery correctly

Recovering 93% of the longest 10% of nets is a ranking or recall result for a selected subset. It does not mean that 93% of all nets are placed correctly, nor that all timing-critical connections are found. The result depends on the cutoff, ties, number of nets, target definition, baseline ranking, and whether “longest” is measured by HPWL or routed length.

Use precision, recall, false-negative rate, rank correlation and top-k overlap for several k values. Separate geometric longest nets from timing-critical nets and high-congestion nets. A method may identify long connections while missing a shorter connection with high delay because of layer resistance, fanout, buffering or electrical coupling.

#### Compare early estimation against the decision it is meant to support

The 56× average speedup over conventional placers is meaningful only after defining the optimized task and timing boundary. Does it include shape initialization, force iterations, legalization, constraint checks, data loading, output conversion and memory transfers? Is the conventional placer solving the same module-level problem, or a more detailed problem? A faster abstraction is not a fair comparison if it performs less work.

The useful end-to-end test is decision preservation. Run the early placer, take its selected designs into a detailed placement and routing flow, and compare whether it chooses good candidates under timing, congestion, area, power and design-rule constraints. Include analytic placement, manual floorplanning and any detailed placer with equal input information and stopping criteria. Report runtime, memory, convergence failures, legalization rate, HPWL, routed metrics and correlation with signoff results.

#### What remains outside the captured evidence

The official description reports a 56× average speedup, about 3% inter-module HPWL error, and recovery of 93% of the longest 10% of nets. It does not name the designs, constraints, comparison tools, hardware, per-design errors, routing checks, timing correlation or signoff flow. The evidence supports a force-based deformable module-estimation direction, not demonstrated detailed routability, timing prediction, or signoff-quality selection.

## Module-level placement: estimate less detail, then test what was lost

A module groups circuit elements by function. Treating it as one object reduces the number of positions an early estimator must choose. That simplification also removes internal detail. For example, a module's total area does not determine where every internal terminal will eventually lie.

[The force-based deformation study](../observed-subthemes/partitioning-and-placement.md#paper-dac-2026-research954) uses deformable module shapes that change aspect ratio while preserving area. Aspect ratio is width divided by height: a module can become wider and shorter without reducing its modeled area. The official description reports a 56× average speedup over conventional placers, about 3% error in inter-module half-perimeter wire length, and recovery of 93% of the longest 10% of nets. [Official description, results paragraph](https://63dac.conference-program.com/presentation/?id=RESEARCH954&sess=sess129).

Half-perimeter wire length adds the width and height of the smallest axis-aligned rectangle enclosing a connection's pins. It is a geometric estimate, not the length of an actual routed wire. Accordingly, the 3% result must not be described as 3% timing error. The longest-net result concerns identifying a selected subset, not 93% accuracy for every connection. The abstract does not name the comparison tools or provide the per-design errors, hardware, or detailed routing checks needed to judge deployment.

## The shared insight and the unresolved comparison

These papers reduce different kinds of work: repeating unchanged calculations, separating coupled placement decisions, and representing every cell during early estimation. Their speedups measure different tasks and cannot form a ranking.

My synthesis is that a useful reduction in design effort must preserve the information needed for the next decision. Test an incremental method on realistic sequences of edits; test a joint placer through the subsequent physical checks; test an early estimator on whether it selects good designs after detailed implementation. Those are proposed evaluation requirements, not experiments claimed for all three papers.

The evidence cards below preserve the earlier capture, including its missing-result statements. This dated editorial recovery on 2026-09-07 supersedes those statements where explicitly cited above. Only iHyperG now has recovered manuscript locations here; the other two remain official-description evidence. Comparable editions and broader sampling are still needed before calling the shared idea a long-term trend.

## Compare the results carefully

First identify the inputs and required output quality. Then identify the limited resource: time, memory, communication, energy, circuit area, or correctness coverage. Ask which part of the method reduces that cost and which new cost it adds. Compare numbers only when the experiments hold these conditions sufficiently similar.

A conference description may explain the proposal while omitting the full experiment. An author preprint link may have been coded from its abstract. The source classification does not by itself establish that every table was read. Missing locations remain visible below.

## Complete captured evidence

These are evidence records, not substitutes for the explanations above. Each record preserves its problem, proposed method, measurements, comparison conditions, and source limits. A populated record does not establish that its mechanism has been fully explained or independently verified.

<span id="paper-dac-2026-research223"></span>

### Ihyperg: Incremental Hypergraph Partitioning on GPU

DAC 2026 · Record: `dac-2026-research223`

[Read the step-by-step explanation](#explanation-dac-2026-research223)

**Updated source-backed reading card**

Reviewed 2026-09-08. Deepens the existing iHyperG treatment into a paper-level reading using the recovered author manuscript; separates delta maintenance, feasibility rebalancing, cut-critical refinement, GPU consistency, stage timing and partition quality, and preserves the exact benchmark and baseline limits.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Dynamic hypergraphs require repeated partition updates without recomputing from scratch.

**Mechanism / artifact:**

GPU-parallel incremental k-way hypergraph partitioner with a delta-based hypergraph data structure, single-pass rebalancing and refinement restricted to cut-critical vertices; update semantics, synchronization, compaction and quality stopping rules remain partly unspecified.

**Workload — the work tested:**

18 ISPD98-derived circuits enlarged 100–1000x by random insertions; two partitions, 3% allowed imbalance, 100 iterations of 25 modifications and ten-run averages are reported. Real edit traces, other k, nonlocal/adversarial edits and long delta sequences are not established.

**Hardware and manufacturing assumptions:**

NVIDIA A6000 with 48 GB memory and GPU-resident incremental partitioning; host/device timing, transfer, synchronization, allocation, kernel, compaction, memory and multi-GPU assumptions are not fully established.

**Baseline — the comparison method:**

HyperG rebuilding and repartitioning

190.17x modification and 82.82x partitioning are separate stage speedups; baseline extension may be unoptimized, and equal graph representation, quality, update sequence and timing boundary are not independently reproduced

**Reported measurements:**

Average 190.17x modification speedup and 82.82x partitioning speedup over HyperG rebuilding/repartitioning are reported, with comparable quality; cut metric, balance distribution, update latency, throughput, memory, tail/variance and end-to-end CAD-loop results are not fully established.

**Limits on the conclusion:**

Incremental correctness requires the delta state to remain equivalent to the edited hypergraph and the selective refinement to cover every move that can affect the objective or balance. A temporary group is a feasibility mechanism, not a final partition, and one-pass refinement can differ from full iterative optimization.

The manuscript reports 18 randomly enlarged ISPD98-derived circuits, A6000/48 GB, 3% imbalance, two partitions, 100 iterations of 25 modifications and ten-run averages. Random insertion, two-way partitioning and device-resident timing do not establish real CAD-loop or arbitrary-k behavior.

Modification and partitioning gains are distinct stages, not multiplicative end-to-end acceleration. The baseline extension may be unoptimized and the implementation has not been reproduced; evidence supports fast updates under the constructed workload, not universal incremental partitioning performance.

**Source and location**

Evidence tier: Recovered author hosted manuscript with selected method/results inspection plus primary official DAC description; not a reproduced implementation or independent scientific acceptance. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://tsung-wei-huang.github.io/papers/2026-DAC-iHyperG.pdf#page=5)

Recovered author manuscript Sections 4–6, PDF pages 2–6, and Table 1; existing observed card and DAC official description; exact manuscript conditions recorded in reports/subtheme-editorial/partitioning-and-placement.md; no reproduction.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** full repartitioning

CPU incremental partitioner

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH223

**Hardware or process assumptions:** GPU graph-processing system; memory and synchronization assumptions are unspecified.

**Limits:** No cut quality, update latency, throughput, memory, or graph-suite results are reported.

Performance may depend on update locality.

Official description only; dynamic-workload validation is required.

**Method or artifact:** GPU-accelerated incremental hypergraph partitioning.

**Metrics:** Incremental partitioning efficiency is claimed qualitatively

**Problem:** Dynamic hypergraphs require repeated partition updates without recomputing from scratch.

**Workload or benchmark:** Dynamic hypergraphs from EDA or other applications; sizes, update rates, and baselines are unspecified.

</details>

<span id="paper-dac-2026-research934"></span>

### ATOM-3D: Analytical Three-Dimensional Orientation-Aware Mixed-Size Placer

DAC 2026 · Record: `dac-2026-research934`

[Read the step-by-step explanation](#explanation-dac-2026-research934)

**Updated source-backed reading card**

Reviewed 2026-09-08. Deepens the existing ATOM-3D treatment into a paper-level reading; separates joint partition/layer/orientation modeling from legal placement, routing, timing and manufacturability, and makes quality-metric, baseline and 3D-condition requirements explicit.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

3D placement must handle mixed cell sizes and orientation while preserving routability and timing.

**Mechanism / artifact:**

Analytical 3D orientation-aware mixed-size placer combining partition assignment, position and macro orientation with partition adjustment for wire-length estimation deviations; objective, legalization, stack and signoff boundary are unspecified.

**Workload — the work tested:**

3D heterogeneous chip or package layouts; stack topology, dies, macros/cells, pins, nets, orientations, layer capacities, constraints, benchmark set and baselines are unspecified.

**Hardware and manufacturing assumptions:**

3D physical-design stack with face-to-face terminals; bonding, terminal pitch, via/routing resources, PDK/process, timing, thermal, power, design rules and manufacturing assumptions are unspecified.

**Baseline — the comparison method:**

2D analytical placement

Orientation-oblivious 3D placement

ICCAD 2023 contest winner and best published method are mentioned contextually; quality metric, legalization, hardware, stack, constraints and post-processing boundaries are unspecified

**Reported measurements:**

8% higher quality than the ICCAD 2023 contest winner, 2% over the best published method and 1.6x runtime speedup are reported; quality definition, wire length, congestion, timing, via, DRC, yield, signoff correlation and conditions are not supplied.

**Limits on the conclusion:**

Orientation changes pin locations, so center-based or orientation-oblivious objectives can misrepresent connectivity. A differentiable analytical objective guides search but does not establish legal placement, routed timing, congestion, via feasibility, thermal behavior or manufacturing yield.

Partition, position and orientation must be evaluated under explicit stack, terminal, layer, macro, pin, routing and timing conditions, with legalization and post-route checks. The quality metric and 8%/2% comparisons must not be rewritten as wire-length or timing improvements.

No wirelength, congestion, timing, via, runtime, or DRC results are reported. Placement benefits depend on stack and constraints; the evidence supports joint orientation-aware modeling, not demonstrated routable or manufacturable 3D placement improvement.

**Source and location**

Evidence tier: Primary captured official DAC description plus existing chapter level atom 3d discussion; no full paper extraction, reproduced placer, legalizer, routed evaluation or manufacturing validation. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/presentation/?id=RESEARCH934&sess=sess132)

DAC 2026 official description; existing chapter-level ATOM-3D discussion; captured Problem, Mechanism / artifact, Workload, Hardware, Baseline, Measurements and Limits fields; no manuscript pages or signoff results.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** 2D analytical placement

orientation-oblivious 3D placement

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH934

**Hardware or process assumptions:** 3D physical-design stack; layer, via, and design-rule assumptions are unspecified.

**Limits:** No wirelength, congestion, timing, via, runtime, or DRC results are reported.

Placement benefits depend on stack and constraints.

Official description only; signoff validation is required.

**Method or artifact:** Analytical 3D orientation-aware mixed-size placer.

**Metrics:** 3D placement quality is claimed qualitatively

**Problem:** 3D placement must handle mixed cell sizes and orientation while preserving routability and timing.

**Workload or benchmark:** 3D chip or package layouts; stack, cells, nets, and baselines are unspecified.

</details>

<span id="paper-dac-2026-research954"></span>

### Module-Level Placement Using Force-Based Deformation for Efficient Early Design Estimation

DAC 2026 · Record: `dac-2026-research954`

[Read the step-by-step explanation](#explanation-dac-2026-research954)

**Updated source-backed reading card**

Reviewed 2026-09-08. Deepens the existing module-level placement treatment into a paper-level reading; separates abstraction, force-based deformation, HPWL estimation, longest-net ranking and actual detailed-placement/signoff correlation, and makes speedup and workload boundaries explicit.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Early module placement must estimate physical consequences before detailed implementation.

**Mechanism / artifact:**

Force-based deformation module-level placer; module abstraction, shape/pin deformation, legalization, force objective, routing proxy and detailed-flow boundary are unspecified.

**Workload — the work tested:**

Hierarchical module layouts; designs, module count/area, pins, constraints, aspect-ratio bounds, net distribution, longest-net denominator, baselines and train/test or design split are unspecified.

**Hardware and manufacturing assumptions:**

Physical-design flow with module abstractions; PDK, floorplan, placement rows, routing layers/tracks, macro halos, power grid, timing, congestion, signoff tools and compute hardware are unspecified.

**Baseline — the comparison method:**

Analytic placement

Manual floorplanning

Conventional placers; equal information, initialization, legalization, detailedness, stopping rule, hardware, loading/output and signoff boundary are unspecified

**Reported measurements:**

56x average speedup, approximately 3% inter-module half-perimeter wire-length error and recovery of 93% of the longest 10% of nets are reported; no per-design/net errors, routed wire, congestion, timing, runtime boundary, correlation, memory or signoff result is supplied.

**Limits on the conclusion:**

Module deformation preserves only stated abstract properties such as area; equal area does not preserve pin locations, internal routing, blockages, congestion or timing. A smooth force objective does not establish legal detailed placement or route feasibility.

HPWL is a geometric proxy, not routed wire length or timing. Recovering 93% of the longest 10% is subset recall, not accuracy for every net or proof that timing-critical and congested nets are selected.

No wirelength, congestion, timing, runtime, correlation, or design results are reported. Module abstractions may hide detailed routability; the evidence supports early estimation, not demonstrated detailed routability, timing prediction, or signoff-quality selection.

**Source and location**

Evidence tier: Primary captured official DAC description plus existing chapter level module placement discussion; no full paper extraction, reproduced placer, per design error table or detailed flow correlation. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/presentation/?id=RESEARCH954&sess=sess129)

DAC 2026 official description/results paragraph; existing chapter-level module-placement discussion; captured Problem, Mechanism / artifact, Workload, Hardware, Baseline, Measurements and Limits fields; no manuscript pages or signoff tables.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** analytic placement

manual floorplanning

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH954

**Hardware or process assumptions:** Physical-design flow with module abstractions; PDK and floorplan assumptions are unspecified.

**Limits:** No wirelength, congestion, timing, runtime, correlation, or design results are reported.

Module abstractions may hide detailed routability.

Official description only; signoff correlation is required.

**Method or artifact:** Force-based deformation module-level placer.

**Metrics:** Early placement efficiency is claimed qualitatively

**Problem:** Early module placement must estimate physical consequences before detailed implementation.

**Workload or benchmark:** Hierarchical module layouts; designs, constraints, and signoff tools are unspecified.

</details>

## What remains to establish

Resolve unspecified workloads, comparison methods, resource budgets, and source locations before generalizing a reported gain. Multiple papers in this selected sample permit comparison of mechanisms, but do not by themselves establish recurrence across years or a long-term trend.

[All subthemes](../expanded-taxonomy-v1.md) · [Research directions](../directions/README.md)
