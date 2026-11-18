## Start with the decisions, not the tool names

Partitioning decides which group each circuit element belongs to. Placement decides where each element sits. These are different decisions. Grouping two elements together does not determine the distance between their terminals. Placing them nearby does not guarantee that a legal wire can connect them.

A connection can involve more than two elements. A **hypergraph** represents that directly: vertices represent elements, and a hyperedge represents one connection involving a set of elements. A partition boundary cuts a connection when its elements belong to different groups. Reducing such crossings can be useful. Putting everything in one group is not a useful solution when each group has a capacity limit. The optimization must account for both connectivity and capacity.

Physical placement introduces additional constraints. Elements occupy area and cannot overlap in a finished layout. Their terminals have particular positions. Rotating a large block changes those positions even if its center remains fixed. In a stacked design, choosing a layer also changes which connections must cross between layers. A useful early estimate must retain enough of these facts to guide the next design decision.

## iHyperG: update the existing partition

[iHyperG's captured record](../observed-subthemes/partitioning-and-placement.md#paper-dac-2026-research223) is supplemented here by the recovered manuscript. Sections 4–5, PDF pages 2–5, describe separate storage for changed connections. They also describe refinement focused on vertices whose movement can reduce partition crossings. The method first removes excess weight from overloaded partitions into a temporary group, then assigns its vertices to feasible partitions. This temporary group is not an extra final partition.

Section 6, PDF page 5, specifies 18 ISPD98-derived circuits enlarged 100–1000 times through random insertions. It specifies an A6000 with 48 GB memory, 3% allowed imbalance, and ten-run averages. Table 1, PDF page 6, uses two partitions and 100 iterations of 25 modifications each. It reports average speedups of 190.17× for modification and 82.82× for partitioning against HyperG rebuilding and repartitioning. These are separate timings, not factors to multiply. The baseline extension is acknowledged as potentially unoptimized.

The evidence supports fast updates under this constructed workload. It does not support equivalent speedups for complete chip design or all real modification sequences. The implementation has not been reproduced here. [Author manuscript, Sections 4–6 and Table 1](https://tsung-wei-huang.github.io/papers/2026-DAC-iHyperG.pdf#page=5).

<span id="explanation-dac-2026-research223"></span>

### iHyperG: incremental partitioning is useful only when the update representation preserves the partitioning problem

#### Start with what partitioning must maintain

A hypergraph has vertices representing objects and hyperedges representing connections that can contain more than two objects. A k-way partition assigns every vertex to one of k groups. The partitioner normally tries to keep groups within a balance limit. It also tries to reduce the number or weight of hyperedges that cross group boundaries. A crossing hyperedge can increase communication, cut size, or a later physical-design cost, depending on the application.

In an optimization loop, the hypergraph does not stay fixed. A circuit transformation may add or remove a vertex. It may add or remove a pin from a hyperedge. It may change a weight or change the balance requirement. Rebuilding the entire graph representation and recomputing a partition after every edit repeats work that the edit did not invalidate. Incremental partitioning tries to update only the changed representation and the part of the solution that may have become wrong.

The central correctness requirement is therefore not merely speed. The incremental state must remain equivalent to the current hypergraph. The selective refinement must examine every vertex whose movement could matter under the chosen objective and balance constraint. The update structure may omit a changed incidence. The refinement scope may omit a newly critical vertex. In either case, a fast result can be a partition of an incomplete problem.

#### What the delta structure changes

The recovered manuscript describes a delta-based GPU hypergraph data structure. The base structure stores the unchanged graph, while a separate representation records changed connections. This can avoid rewriting large adjacency structures when an edit touches only a small portion of the hypergraph. The implementation still needs defined rules for additions, deletions, weight changes, duplicate pins, and empty or singleton hyperedges. It also needs a defined point at which accumulated deltas are merged into the base structure.

The update cost depends on edit locality and representation size. A small number of edits concentrated in a few connections may fit the intended fast path. A long sequence of edits may make the delta structure large, reduce locality, increase memory use, or require a rebuild. Report both per-update cost and amortized cost over a sequence, including compaction or reconstruction. A single small modification is not a complete dynamic-workload evaluation.

#### Rebalancing and refinement are different operations

The described algorithm first removes excess weight from overloaded partitions into a temporary group. It then assigns those vertices to feasible partitions. This is the rebalancing step. The temporary group is an intermediate holding area, not an additional final partition. This step addresses feasibility: every final partition must satisfy the allowed imbalance. It does not by itself minimize cut cost.

After feasibility is restored, the algorithm refines vertices identified as cut-critical. A vertex is relevant when moving it could reduce a crossing hyperedge or improve the objective without violating balance. Restricting refinement can reduce work. The method must define how criticality is detected and how ties are resolved. It must define how moves are ordered and whether moves are accepted greedily. It must also define how the process stops. A one-pass procedure may be appropriate for the intended update regime. It can differ from a full iterative partitioner when several moves interact.

This creates two separate quality checks. First, the final assignment must satisfy balance and cover every vertex exactly once. Second, its cut quality must be compared with a specified reference. The comparison must use the same partition count, weights, imbalance allowance and stopping rule. “Comparable quality” cannot be assessed from runtime alone.

#### GPU execution adds consistency and memory questions

GPU parallelism can process changed connections and candidate moves concurrently. Concurrent updates may conflict when several vertices affect the same partition weights or hyperedge state. The implementation needs a defined synchronization or atomic-update rule and a deterministic or statistically characterized result under different execution orders. It must also state whether the base graph, delta graph, partition labels, weights and temporary group fit in device memory.

The relevant hardware cost includes host-to-device transfer, allocation, synchronization and kernel launch. It also includes temporary storage, compaction, and any CPU work around the GPU kernels. A modification speedup measured only after data is resident on an A6000 is different from end-to-end speedup. The end-to-end case is a CAD loop that creates edits on the host and consumes the updated partition elsewhere.

#### Read the reported experiment at its actual boundary

The recovered Sections 4–6 and Table 1 describe 18 ISPD98-derived circuits enlarged by random insertions from 100× to 1000×. They describe an NVIDIA A6000 with 48 GB memory and a 3% allowed imbalance. They also describe ten-run averages, two partitions, and 100 iterations of 25 modifications each. These conditions make the result more concrete than the official card, but they also define the tested boundary. Random insertions may not represent edits produced by real synthesis, placement, timing or optimization loops. Two-way partitioning does not establish behavior for arbitrary k. Ten-run averages do not show tail latency or variance unless those are reported.

The reported 190.17× modification speedup and 82.82× partitioning speedup are separate stages. They must not be multiplied into a claimed end-to-end speedup. The comparison is against HyperG rebuilding and repartitioning, and the manuscript notes that the baseline extension may not be optimized. A fair comparison should use equivalent graph representations, update semantics, and quality targets. It should use the same device-resident or end-to-end timing boundaries. It should also use the same edit sequence. Report cut metrics, balance violations, memory, throughput, per-update latency and rebuild frequency alongside the two stage timings.

#### What remains open

The evidence supports the mechanism and the reported constructed experiment, not universal incremental partitioning performance. Reproduction is still pending. The important open tests are real edit traces and larger and different k-way settings. They also include adversarial or nonlocal edits, long delta sequences and compaction behavior. The remaining tests are multiple GPUs, end-to-end host/device timing, and quality distributions rather than only average speedups. The 190.17× and 82.82× numbers are evidence for reduced work under the stated conditions. They are not evidence that a complete CAD optimization loop is 190× or 83× faster.

<span id="explanation-dac-2026-research934"></span>

### ATOM-3D: orientation-aware placement must preserve the physical meaning of pins, layers, and connections

#### Why three-dimensional placement changes the problem

Placement assigns coordinates to circuit objects subject to non-overlap, area, design-rule, timing and routing constraints. In a heterogeneous three-dimensional chip, objects may occupy different dies or layers. They may communicate through vertical terminals or other interconnect structures. Partitioning decides which objects belong to which layer or region. Placement decides their positions. Orientation decides how each macro’s local coordinate system is rotated or reflected. These choices interact. A layer assignment changes which connections cross vertically. An orientation changes where the connection pins appear.

A macro cannot be represented adequately by its center alone. Two macros with the same center and outline can expose their pins on different sides after rotation. A wire-length model using only center-to-center distance can therefore prefer a placement that looks geometrically close. Actual terminals may then be harder to connect. ATOM-3D is described as an analytical, differentiable, orientation-aware mixed-size placer. It combines partition, position and orientation decisions. It then adjusts the partition to compensate for wire-length estimation deviations.

#### What the objective must contain

An analytical placer optimizes a mathematical objective rather than directly running detailed routing at every step. The objective should state how it represents net or hyperedge wire length, pin locations, macro overlap and density. It should also state how it represents layer transitions, vertical terminals and congestion. It should state how it represents timing-critical connections and orientation constraints. A differentiable relaxation may permit continuous coordinates or orientation variables. The method must then explain how those variables are converted into legal discrete placements. It must also explain how the conversion changes the objective.

“Differentiable” means that the optimizer can calculate how a small modeled change affects the objective. It does not mean that the final layout is legal, routed, or timing-clean. A smooth wire-length estimate can guide search. It can still miss discrete blockages, routing tracks, via limits and pin access. It can also miss clock structures, power delivery, thermal constraints or design-rule checks. The post-placement adjustment is therefore part of the method’s correctness boundary, not an optional presentation detail.

#### Partition and orientation are coupled decisions

If a macro is assigned to a die, the locations and cost of its connections depend on two things. These are the destination layer and its orientation. Optimizing layer assignment first and orientation later can trap the search in a poor local arrangement. A joint method can evaluate these variables together. It must show how it avoids illegal overlaps, impossible terminal access and inconsistent layer capacity during the optimization.

The partition-adjustment step needs a precise trigger and objective. It may move a macro between layers when the estimated wire cost differs from a more accurate calculation. Such a move can change density, vertical interconnect demand, thermal load, and timing. It can also change the orientation choices of neighboring macros. Report whether the adjustment is one pass or iterative. Report whether it can undo earlier decisions. Also report whether the final coordinates are re-optimized after reassignment.

#### Separate modeled quality from physical signoff

Wire length is not the same as routed delay. A shorter geometric connection can be slower. This can happen if it is congested, requires extra vias, uses a poor layer, or has limited pin access. It can also happen if it crosses a timing-critical path with unfavorable buffering. In 3D, vertical connections also have capacity, alignment, reliability, thermal and manufacturing constraints. The evaluation should therefore distinguish the analytical objective from routed wire length, congestion, timing and power. It should also distinguish it from via count, thermal behavior, design-rule violations and yield.

The claimed “8% higher quality” and “2% over the best published method” require the quality metric and direction. They also require the aggregation, benchmark set and statistical treatment. They must not be rewritten as 8% shorter wires or 2% better timing. The 1.6× runtime speedup requires the same hardware, stopping criterion, legalization, partition adjustment, initialization and post-processing boundary for each baseline.

#### The comparison must expose the 3D conditions

A 2D analytical placer and an orientation-oblivious 3D placer are useful conceptual baselines. A complete comparison must still identify the stack topology, number of dies, face-to-face bonding assumptions, terminal pitch and layer capacities. It must also identify macro dimensions, cell mix, netlist, pin locations and allowed orientations. It must identify routing resources, via rules and timing constraints. It should include a placement with fixed orientation, a placement with independent orientation, and a joint placement. This isolates the value of orientation awareness.

Report legality rate, overlap, wire-length components, congestion, and via or vertical-terminal demand. Also report timing slack, power or thermal measures, runtime and memory. Report convergence failures, DRC violations and post-route correlation. Test different stack sizes, macro proportions, pin distributions, critical-path weights and design-rule constraints. A method that improves a relaxed objective but produces more failed legalizations has not shown a physical-design improvement.

#### What the captured evidence establishes

The official description supports an orientation-aware analytical 3D mixed-size placement direction for face-to-face heterogeneous chips. It reports author-claimed quality and runtime comparisons. It does not define the quality measure. It also does not provide paper-page evidence for wire length, congestion, timing or via behavior. It gives none for design-rule checking, manufacturing conditions or signoff correlation. The evidence supports joint modeling of partition, position and orientation, not demonstrated routable or manufacturable 3D placement improvement.

## ATOM-3D: orientation changes the placement problem

A large predesigned circuit block is commonly called a macro; mixed-size placement handles such blocks together with smaller cells. Orientation matters because connections terminate at pins, not at block centers. A placement estimate that ignores pin movement under rotation can prefer an arrangement whose real connection distances are worse.

[ATOM-3D](../observed-subthemes/partitioning-and-placement.md#paper-dac-2026-research934) targets heterogeneous chips bonded face-to-face through terminals. Its official description combines partition assignment, position, and macro orientation in one analytical global-placement framework. A partition adjustment then compensates for wire-length estimation deviations. Here, analytical means optimizing a mathematical description of placement cost. Differentiable means that small changes to the modeled variables have computable effects on that cost.

The description reports 8% higher quality than the ICCAD 2023 contest winner. It reports 2% over the best published method. It also reports 1.6× runtime speedup. It does not define the quality measure or expose the detailed comparison conditions. Those percentages must therefore remain author claims about an unspecified quality measure, not be rewritten as wire-length or timing reductions. This source establishes more mechanism than the older captured card, but does not supply paper-page evidence or final manufacturing validation. [Official ATOM-3D description](https://63dac.conference-program.com/presentation/?id=RESEARCH934&sess=sess132).

<span id="explanation-dac-2026-research954"></span>

### Module-level placement: deformation is useful only if the abstraction preserves the decisions that matter later

#### What module-level placement simplifies

A physical design may contain millions of cells, but an early planning stage often groups related cells into modules. A module can be treated as one object. The object has an area, a shape, pins or boundary terminals, and connections to other modules. This reduces the number of positions and shapes that the optimizer must consider. It also removes information. The module abstraction does not tell the early placer where every internal cell will eventually be placed. It gives the same lack of information for every internal wire or internal pin.

The reported method uses force-based deformation. A force-based placer represents attraction or repulsion between connected objects and uses those forces to move them. Deformation allows a module’s width and height, or aspect ratio, to change while preserving a stated area or other constraint. This is more expressive than moving fixed rectangles. It still optimizes a model of the module, not the final standard-cell placement and routed layout.

#### Area preservation is not shape or routability preservation

Area is the product of width and height. Two modules can have the same area. They can still have very different aspect ratios, pin distributions, boundary congestion and internal routing difficulty. A wide, short module may connect well to horizontal neighbors and poorly to vertical ones. A tall, narrow version may reverse that behavior. The model may preserve area but not terminal locations, pin access, internal hierarchy or blockages. The resulting estimate can then be systematically wrong. This can happen even when its area constraint is exact.

The method must define what can deform and which dimensions are bounded. It must define how pins move with the shape. It must also define whether orientation is allowed and whether a module can overlap another during the optimization. It must also state when shapes are legalized and whether the final legal shape is re-evaluated. A smooth deformation path can find a useful early arrangement. It can still produce a shape that cannot be implemented under placement rows, routing tracks, macro halos or power-grid constraints.

#### Understand the reported wire-length metric

The inter-module half-perimeter wire length (HPWL) of a connection is the width plus height of a rectangle. The rectangle is the smallest axis-aligned one containing its pins. HPWL is fast and useful for ranking candidate placements. It is not the length of a routed wire, and it is not a timing measurement. It omits routing detours, congestion, layer assignment, via cost, buffering, resistance, capacitance, coupling and pin-access failures.

The reported approximately 3% error therefore needs a reference and denominator. Error is relative to which detailed placement or wire-length calculation? Over which designs and nets? With what mean or percentile aggregation? A low average HPWL error can hide large errors on critical or congested nets. The evaluation should report per-design and per-net distributions, critical-net error, rank correlation and congestion correlation. It should also report whether the abstraction selects the same candidate that survives detailed implementation.

#### Interpret longest-net recovery correctly

Recovering 93% of the longest 10% of nets is a ranking or recall result for a selected subset. It does not mean that 93% of all nets are placed correctly, nor that all timing-critical connections are found. The result depends on the cutoff, ties, number of nets, target definition and baseline ranking. It also depends on whether “longest” is measured by HPWL or routed length.

Use precision, recall, false-negative rate, rank correlation and top-k overlap for several k values. Separate geometric longest nets from timing-critical nets and high-congestion nets. A method may identify long connections. It may still miss a shorter connection with high delay because of layer resistance, fanout, buffering or electrical coupling.

#### Compare early estimation against the decision it is meant to support

The 56× average speedup over conventional placers is meaningful only after defining the optimized task and timing boundary. Does it include shape initialization, force iterations, legalization, constraint checks, data loading, output conversion and memory transfers? Is the conventional placer solving the same module-level problem, or a more detailed problem? A faster abstraction is not a fair comparison if it performs less work.

The useful end-to-end test is decision preservation. Run the early placer and take its selected designs into a detailed placement and routing flow. Then compare whether it chooses good candidates under timing, congestion, area, power and design-rule constraints. Include analytic placement, manual floorplanning and any detailed placer with equal input information and stopping criteria. Report runtime, memory, convergence failures, legalization rate, HPWL, routed metrics and correlation with signoff results.

#### What remains outside the captured evidence

The official description reports a 56× average speedup and about 3% inter-module HPWL error. It also reports recovery of 93% of the longest 10% of nets. It does not name the designs, constraints, comparison tools, hardware, per-design errors, routing checks, timing correlation or signoff flow. The evidence supports a force-based deformable module-estimation direction, not demonstrated detailed routability, timing prediction, or signoff-quality selection.

## Module-level placement: estimate less detail, then test what was lost

A module groups circuit elements by function. Treating it as one object reduces the number of positions an early estimator must choose. That simplification also removes internal detail. For example, a module's total area does not determine where every internal terminal will eventually lie.

[The force-based deformation study](../observed-subthemes/partitioning-and-placement.md#paper-dac-2026-research954) uses deformable module shapes that change aspect ratio while preserving area. Aspect ratio is width divided by height: a module can become wider and shorter without reducing its modeled area. The official description reports a 56× average speedup over conventional placers. It reports about 3% error in inter-module half-perimeter wire length. It also reports recovery of 93% of the longest 10% of nets. [Official description, results paragraph](https://63dac.conference-program.com/presentation/?id=RESEARCH954&sess=sess129).

Half-perimeter wire length adds the width and height of the smallest axis-aligned rectangle enclosing a connection's pins. It is a geometric estimate, not the length of an actual routed wire. Accordingly, the 3% result must not be described as 3% timing error. The longest-net result concerns identifying a selected subset, not 93% accuracy for every connection. The abstract does not name the comparison tools. It does not provide the per-design errors, hardware, or detailed routing checks needed to judge deployment.

## The shared insight and the unresolved comparison

These papers reduce different kinds of work. They reduce repeating unchanged calculations, separating coupled placement decisions, and representing every cell during early estimation. Their speedups measure different tasks and cannot form a ranking.

My synthesis is that a useful reduction in design effort must preserve the information needed for the next decision. Test an incremental method on realistic sequences of edits. Test a joint placer through the subsequent physical checks. Test an early estimator on whether it selects good designs after detailed implementation. Those are proposed evaluation requirements, not experiments claimed for all three papers.

The evidence cards below preserve the earlier capture, including its missing-result statements. This dated editorial recovery on 2026-09-07 supersedes those statements where explicitly cited above. Only iHyperG now has recovered manuscript locations here; the other two remain official-description evidence. Comparable editions and broader sampling are still needed before calling the shared idea a long-term trend.
