# Placement routing and floorplanning

This subject has 12 records in the selected sample. This page explains where it fits, then presents all captured paper evidence without shortening the measurements or limitations.

[Definitions used in the paper records](../reading-guide-v1.md)

## Understand the parent subject first

- [Physical design and manufacturing](../themes/physical-design-and-manufacturing.md)

## A circuit needs both components and space

A logical circuit identifies components and their connections. A physical implementation assigns locations to those components and paths to the wires. Floorplanning decides the broad arrangement of major blocks. Placement assigns more detailed locations. Routing constructs the actual connections within the available layers and manufacturing rules.

These decisions interact. Moving connected components closer can shorten a wire but crowd a region needed by other connections. Reserving more space for wires can increase the distance between components. A layout must ultimately meet several conditions together, including legal geometry, connectivity, timing, and power delivery.

## Why a connection diagram is insufficient

Physical wires have resistance and capacitance. Resistance limits current flow; capacitance stores charge that must change when a signal changes. Their combination contributes delay. The exact behavior depends on wire dimensions, material, surrounding structures, and attached circuits.

A placement tool often uses an estimate of these effects before detailed routing exists. The estimate is useful if it guides the design toward a final implementation that passes the required checks. A lower estimated wirelength or delay does not itself establish that every connection can be routed or that the completed circuit meets timing.

## Standard cells make some choices in advance

A standard cell is a predesigned small circuit with a defined physical layout and interface. Building from a library of cells limits the choices a placement tool must make. A transistor-level placement method instead considers finer-grained structure and can potentially discover arrangements outside those fixed boundaries.

The cell-structure-independent placement record proposes this finer-grained choice together with routing that accounts for middle-of-line connections near the devices. The current description does not establish its technology rules, final routing legality, or measured timing and power. Increased freedom therefore needs to be evaluated alongside implementation and verification costs. [Recorded evidence](../observed-subthemes/placement-routing-and-floorplanning.md#paper-dac-2026-research2006)

<span id="explanation-dac-2026-research2006"></span>

### Cell-structure-independent placement: removing cell boundaries moves the hard problem into physical legality

#### What standard-cell boundaries normally provide

A standard-cell flow places predesigned cells with known dimensions, pins, power connections and routing abstractions. This limits the search space and gives later tools characterized timing, power and legal interfaces. The boundary can also waste space or make pins and low-level connections difficult to access at an advanced node.

A transistor-level method places individual devices or smaller structures without treating the standard cell as the fixed unit. It can change device sharing, local geometry, pin access and the distance between transistor terminals. The added freedom can reduce abstract wirelength or area, but it also removes assumptions that made mapping, routing, extraction and signoff predictable.

#### What MOL-aware routing adds

Middle-of-line and M0 connections are local interconnect structures close to transistor and device contacts. They have limited tracks, spacing rules, contact options and access directions. A placement that looks good at a higher metal layer can be impossible to connect in these lower-level resources. An MOL-aware router must therefore reason about device adjacency, terminal access, local congestion, design rules and how lower-level choices constrain later wires.

The objective is not simply to minimize distance. A legal route must connect every required terminal, obey spacing and enclosure rules, avoid shorts, meet manufacturing rules and leave enough resources for power and signal connections. Transistor-level placement can also create more unique structures that need extraction and characterization instead of reusing a standard cell's known models.

#### What a complete evaluation needs

Fix the technology node, PDK, device rules, voltage, design size, input netlist and signoff flow. Compare the commercial standard-cell flow and prior transistor-level work with the same placement, routing, extraction, timing, power and verification requirements. Report wirelength, area, congestion, unrouted nets, design-rule violations, pin-access failures, timing, slew, power, leakage, runtime, memory, repair iterations and signoff yield.

Test high pin density, shared devices, long wires, irregular structures, high fanout, power-grid interaction and designs of different sizes. A useful result must show that a placement improvement survives MOL/M0 routing, extraction, corner analysis and final checks. The captured official description claims qualitative wirelength and area improvement but reports no numeric PPA, timing, power, routability, design-rule or technology-node result. The evidence supports a broader physical-design search direction, not proven signoff-ready improvement.

## Three-dimensional placement adds another physical relationship

Placing circuits on more than one active layer changes which components can be near one another and which connections cross layers. It also introduces constraints from alignment, connection structures, and thermal behavior. A short abstract three-dimensional distance does not automatically describe an available physical wire path.

The true-3D placement record combines timing-driven choices with treatment of large-block boundaries during initial placement. Its description names a search approach but leaves routing, timing, thermal, and runtime results unresolved. The relevant question is whether the resulting physical implementation improves under the same stack and evaluation assumptions. [Recorded evidence](../observed-subthemes/placement-routing-and-floorplanning.md#paper-dac-2026-research2133)

<span id="explanation-dac-2026-research2133"></span>

### True-3D timing-driven placement: vertical distance is useful only when bonding, routing and timing models agree

#### What analytical 3D placement is choosing

Placement assigns coordinates to cells and larger blocks before detailed routing. An analytical method represents those coordinates as variables and optimizes a mathematical objective, often using smooth approximations so that gradients can guide movement. A mixed-size placement must handle small standard cells together with large macros whose shape, orientation, keep-out region and legal location constrain nearby cells.

In a face-to-face 3D design, circuit regions can occupy multiple dies or active layers. A signal may cross between dies through hybrid bonds or micro-bumps and then continue through local wiring. The distance between two coordinates is therefore not the complete wire path. A vertical connection has limited sites, alignment and electrical properties, and may compete with thermal, power-delivery and mechanical constraints.

#### What timing-driven weighting and macro boundaries mean

Timing-driven placement gives more influence to connections whose delay affects a critical path. That weight must reflect resistance, capacitance, fanout, driver strength, wire layers, vertical crossings and the current timing slack. If the estimate is wrong, the optimizer may move the wrong objects or improve a proxy without improving final timing.

Macro-boundary-aware initialization tries to prevent large blocks from occupying positions that make the rest of the placement impossible or congested. A differentiable boundary penalty can guide continuous optimization, but it is still an approximation to discrete legal placement, orientation, blockage, power, thermal and bonding rules. A smooth objective can produce an attractive intermediate position that must later be snapped, legalized or moved substantially.

#### What a complete 3D evaluation needs

Define die stack, bonding technology, vertical-interconnect sites, macro dimensions and orientations, keep-outs, thermal model, power grid, routing layers, RC model, STA version and timing constraints. Compare timing-oblivious analytical placement and prior 3D placement under the same netlist, dies, routing, legalization, extraction and signoff flow. Report wirelength, vertical crossings, timing/slack, congestion, macro displacement, thermal distribution, power, runtime, memory, legalization changes, unrouted connections and signoff failures.

Test different die assignments, macro sizes, bond densities, temperature conditions, critical-path structures, multi-die 2D cases and designs not used to tune the weights. Separate the result of initial placement from detailed routing, extraction and final STA. The captured official description identifies timing-driven net weighting and differentiable macro-boundary-aware true-3D initialization but reports no wirelength, timing, congestion, thermal or runtime result. The evidence supports a 3D analytical-placement direction, not demonstrated timing closure or manufacturing-ready 3D quality.

## Weighting expresses which connections matter more

A placement objective can assign different importance to connections. A net is a group of electrically connected terminals; a pin is an individual connection point. A timing-driven method can give greater weight to connections whose delay affects whether a requirement is met.

The hybrid net–pin weighting paper proposes an analytical way to assign those weights. The benefit depends on how accurately the weights represent the completed circuit's timing needs. The captured record lacks the benchmark and final timing conditions needed to establish that relationship. [Recorded evidence](../observed-subthemes/placement-routing-and-floorplanning.md#paper-dac-2026-research1290)

<span id="explanation-dac-2026-research1290"></span>

### Hybrid net–pin weighting: a placement weight is useful only when it points toward the actual critical delay

#### Why a net-level weight is not enough

A net connects one driver to one or more receiving pins. A net-level weight gives the whole connection one importance value. That can miss an important difference between pins: one sink may lie on a critical path while another sink on the same net has slack, a short local route or a different load. The placement objective may need both the importance of the net and the importance of each pin or sink.

Placement usually balances a geometric term such as estimated wirelength with timing terms. The weight determines how strongly moving a connection changes the objective. An analytical weight tries to derive that value from measurable circuit quantities rather than repeatedly choosing it by a hand-tuned heuristic. The derivation still depends on the timing model, slack, fanout, capacitance, estimated route and how the placement tool represents congestion.

#### What the hybrid objective can and cannot prove

The weighting can guide cells that affect critical paths closer together or reduce the estimated cost of important sinks. It cannot guarantee that the same paths remain critical after legalization, detailed routing, buffering, layer assignment, parasitic extraction and timing analysis at operating corners. Moving one pin can improve one sink while increasing another sink's load or creating congestion that harms several paths.

Timing also changes as the design changes. A path that is critical at one placement can become non-critical after an improvement, while another path becomes the limiting path. A stable analytical rule should therefore be evaluated across iterations and designs rather than assumed to remain correct because it produced a lower objective value.

#### What a complete evaluation needs

Define the wirelength estimate, timing engine, slack and criticality calculation, net/pin weighting formula, congestion model, update frequency and optimization objective. Compare wirelength-driven placement, heuristic timing-weighted placement and the analytical hybrid method on the same netlists, technology, constraints and compute budget. Report wirelength, worst negative slack, total negative slack, critical-path delay, congestion, overflow, runtime, memory, convergence and legalization changes.

Then route and extract the placements and rerun timing. Report how often the ranking predicted by the placement objective survives final STA, how many timing repairs are required and whether wirelength or congestion worsens. The captured official description claims qualitative timing and placement improvements but reports no wirelength, worst negative slack, congestion, runtime or benchmark details. The evidence supports analytical net–pin weighting, not established timing closure or universal superiority over heuristic weighting.

## FPGA placement is a discrete resource-assignment problem

An FPGA is not an empty rectangle where any logic block can be placed at any coordinate. Its fabric contains discrete site types: lookup-table and register resources, arithmetic blocks, memories, input/output sites and clocking resources. A netlist node must be assigned to a compatible site, and its connections must later use available routing tracks and switch resources. A placement can therefore have short geometric distances and still be illegal, unroutable or slow.

The heterogeneous-FPGA placement record adds a learning-based, slack-aware timing signal to global placement. Slack is the remaining time margin on a timing requirement. If a path is required to arrive at time 10 and is estimated to arrive at time 8, it has slack 2. If it arrives at 11, it has slack −1 and violates the requirement. A timing-aware placer gives more attention to paths with small or negative margin, but that margin remains an estimate until the design has a concrete route and extracted delay.

<span id="explanation-dac-2026-research1404"></span>

### Learning-based slack-aware FPGA placement: a learned priority is useful only if it survives legal placement and routing

#### What the placement problem contains

Global placement chooses approximate locations for many logic elements before exact sites and routing paths are finalized. In a heterogeneous FPGA, the element must fit one of the fabric's discrete site types, nearby elements must be reachable through the routing fabric, and the resulting paths must satisfy clock and input/output requirements.

These constraints are not interchangeable. Moving a lookup-table cluster toward a memory block may shorten one data path but consume sites needed by another region. Moving logic away from a congested channel may improve routability while making a critical path longer. Carry chains, hard arithmetic blocks, clock regions, fixed package pins and placement exclusions can make a geometrically attractive location illegal or expensive to repair.

#### What slack-aware timing changes

Wirelength-driven placement treats distance or estimated routing cost as the main signal. Timing-driven placement adds information about which paths currently limit the design. Slack-aware placement tries to distinguish a path with only a small margin from one with abundant margin, so movement on the first path receives greater priority.

The timing signal must be recomputed as placement changes. Fanout changes the load seen by a driver. Congestion can force a longer or higher-layer route. A different site type can change local delay. Buffering, clock skew, routing detours and the final FPGA timing model can all change the slack estimated during global placement. A learned model is therefore a policy for deciding which placement changes to try under an approximate state, not a replacement for timing analysis.

#### What “learning-based” must specify

A reproducible account must state what the model observes, what action it selects, what objective supplies the training signal and how illegal actions are handled. The state may include cell locations, net connectivity, estimated slack, fanout, site types and congestion. The action may move a block, adjust a region weight or choose which critical group to place next. The training objective may reward lower wirelength, improved slack, reduced overflow or a weighted combination. Without these definitions, “learning-based” does not identify a reproducible algorithm.

Training data creates a generalization question. If the model sees circuits from one architecture, device size or design family, it may learn that distribution rather than a rule that transfers to another FPGA. A fair test separates training and evaluation circuits, reports FPGA families and resource mixes, fixes placement and routing budgets, and measures seed-to-seed variation. A model that improves only on designs used to tune it has a narrower result than one that transfers to unseen netlists and devices.

#### What a complete evaluation needs

Define the FPGA architecture, site capacities, clock regions, routing graph, timing constraints, congestion model, legalization procedure, learning model, training set, held-out set and compute cost. Compare against wirelength-driven placement and heuristic timing-driven placement with the same netlists, seeds, placement time, routing tool and device constraints.

Report wirelength or the exact proxy, legal-placement failures, routing overflow, unrouted nets, worst negative slack, total negative slack, critical-path delay, power if available, runtime, memory, training cost and seed variance. Then run the complete placement-to-route-to-timing flow. A lower global-placement objective or better predicted slack is not enough if legalization moves critical logic, routing fails or final timing degrades.

The captured official description claims qualitative timing and placement improvement for large heterogeneous FPGA netlists. It reports no slack, wirelength, congestion, runtime, training cost, held-out-device result or cross-architecture generalization result. The evidence supports a learning-based slack-aware placement direction, not proven FPGA timing closure or a general advantage over heuristic placement. [Recorded evidence](../observed-subthemes/placement-routing-and-floorplanning.md#paper-dac-2026-research1404)

## Detailed routing turns connection intent into legal geometry

Placement says which objects should be near one another. Detailed routing must choose the actual path through a discrete grid of tracks, layers, vias and programmable or physical connections. A path is useful only if it connects the required terminals, does not collide with other paths, obeys spacing and width rules, and leaves enough resources for the rest of the design.

The routing record describes a versatile maze-routing algorithm. Maze routing explores a connection graph from a source toward a target. Each graph edge represents a possible movement along a routing track, through a layer change, or through a permitted connection. The router assigns costs to edges and to congestion so that a path is not merely short but also feasible in the shared routing graph.

<span id="explanation-dac-2026-research1534"></span>

### DRΛMA maze routing: a pathfinding method must be judged on legal completion, not only on search behavior

#### What detailed routing is solving

After placement, each net has terminals at fixed locations. The router has to connect them using available routing resources. A two-terminal connection can be viewed as a path through a graph. Multi-terminal nets require a tree or a sequence of connected paths, and each selected edge consumes capacity that other nets may need.

The simplest path cost is geometric length. That is not enough in a real layout. A short path through a nearly full channel can block several remaining nets. A path with an extra via may be easier to find but add resistance, capacitance, manufacturing risk or timing delay. A path on a preferred layer may be lower cost than the same distance on a layer with difficult rules. The router therefore needs a cost model that combines length, congestion, vias, layer preferences, design rules and, where relevant, timing sensitivity.

#### What maze routing means

A maze router expands candidate locations from a source until it reaches a target, then backtracks through the lowest-cost predecessor chain to recover a path. In a congested design, the first route can reserve resources needed by later nets. Modern routers therefore use negotiated congestion, rip-up and reroute, path-history penalties, net ordering, Steiner-tree construction or other mechanisms to revise earlier decisions.

“Versatile” must be made concrete. It may mean that the algorithm handles different net shapes, layer rules, congestion conditions, routing objectives or technology constraints. Each added rule changes the graph and the cost function. An algorithm that works on a simple uniform grid may fail when tracks have direction restrictions, blockages, nonuniform capacities, via arrays, multi-patterning limits, cut layers, antenna rules or advanced-node spacing constraints.

#### Why legal routing is different from finding a path

Finding a graph path does not by itself prove physical legality. The graph must faithfully encode which tracks, vias and layer transitions are allowed. After routing, design-rule checking must inspect spacing, width, enclosure, end-of-line, minimum-area, shorts, opens, antenna and other technology-specific conditions. The parasitic extraction step then determines whether the legal geometry meets timing and signal-integrity requirements; that extracted result is part of the routing claim, not an optional later detail.

Routing choices also interact across nets. Rip-up and reroute can improve one connection while making another unroutable. A lower total wirelength can come with more vias, greater congestion concentration or a worse critical path. A router that reports a complete connection set but needs extensive post-route repair has a different practical result from one that reaches signoff with fewer iterations.

#### What a complete evaluation needs

Define the routing graph, number and direction of layers, track capacities, via rules, blockages, design rules, net ordering, cost terms, rip-up policy, stopping rule, technology node and signoff tools. Compare classical maze routing and any commercial or open router under the same netlists, constraints, layer stack, design rules, hardware and runtime budget.

Report routed-net completion, opens, shorts, design-rule violations by type, total wirelength, via count, layer usage, peak and average congestion, overflow, timing slack, signal integrity, runtime, memory, rip-up count and convergence. Test sparse and highly congested designs, high-fanout nets, blockages, irregular rules, long nets, critical nets and designs from more than one technology or rule set. Report whether the result remains valid after extraction, timing analysis and signoff checks.

The captured official description claims qualitative routing quality and runtime improvement. It reports no design-rule count, wirelength, via count, timing, congestion, runtime or signoff result. Algorithm behavior may depend strongly on the encoded rule complexity. The evidence supports a versatile maze-routing direction, not demonstrated signoff-scale superiority or universal robustness. [Recorded evidence](../observed-subthemes/placement-routing-and-floorplanning.md#paper-dac-2026-research1534)

## Soft rectilinear modules require both continuous shaping and discrete legality

A floorplan assigns each large block a position, width, height and sometimes a non-rectangular outline before detailed placement and routing. A soft module has a required area but can change its aspect ratio. A rectilinear module may contain horizontal and vertical edges and may have notches or stepped boundaries. That flexibility can make it easier to pack modules around fixed blocks and routing channels, but it also makes overlap and boundary checks more complex.

The floorplanning record combines a differentiable polygon-shaping model with flow-based legalization. The two parts solve different problems. Differentiable shaping supplies a smooth signal that can move a continuous representation toward lower area, wirelength or constraint cost. Legalization converts that representation into non-overlapping modules with discrete positions, permitted edges and any required boundary or blockage constraints. A good relaxed solution can require substantial movement before it becomes legal.

<span id="explanation-dac-2026-research2024"></span>

### Differentiable rectilinear floorplanning: a smooth polygon objective must survive discrete legalization

#### What a soft rectilinear module represents

For each module, the floorplanner must preserve a target area while choosing a shape. A rectangle can vary its width and height subject to an aspect-ratio range. A rectilinear polygon adds more possible outlines, but every edge must remain horizontal or vertical and the boundary must form a valid connected region. Notches can help one module fit around another, but they can also create narrow channels that are difficult to route or impossible to manufacture under minimum-width rules.

The floorplan must satisfy non-overlap, outline, fixed-block, keep-out, power and routing constraints. Wirelength depends on the locations of module terminals, not only on the module centers. If a module changes shape, its pins may move or become harder to access even when its area is unchanged. The objective therefore has to represent both module geometry and the connections between modules.

#### Why differentiability is introduced

Many floorplanning decisions are discrete: two blocks are either left/right or above/below, a boundary is either inside or outside a region, and two polygons either overlap or do not. Discrete changes make direct gradient optimization difficult. A differentiable polygon model replaces hard decisions with continuous parameters or smooth penalties. Gradients can then indicate which shape or position change would reduce an objective.

The smooth objective is a proxy. A small overlap penalty may allow modules to intersect during optimization; a smooth boundary may permit a corner or edge that is not legal; a wirelength approximation may not match the route produced after legalization. The result is useful only if the representation can be converted without large area, wirelength, congestion or timing damage.

#### What flow-based legalization contributes

Legalization takes the proposed shapes and positions and assigns them to a valid arrangement. A flow formulation can model movement or assignment through a network whose capacities and costs encode available space, ordering or displacement. It must still preserve polygon boundaries, module areas, fixed objects, non-overlap and the floorplan outline. If legalization moves modules far from their relaxed locations, the differentiable optimization was solving a different problem than the final one.

The cost of legalization is part of the method. It includes displacement, shape changes, new overlaps that must be repaired, routing-channel loss and any iterations needed to recover timing or congestion. Reporting only the continuous objective hides the central question: whether the relaxed solution is a good starting point for a legal physical design.

#### What a complete evaluation needs

Define the polygon representation, area and aspect-ratio constraints, minimum edge widths, allowed notches, outline, fixed blocks, keep-outs, overlap penalty, wirelength model, routing model, flow network, legalization objective and stopping rule. Compare sequence-pair floorplanning and discrete rectilinear legalization using the same module sets, constraints, seeds and compute budget.

Report total area, outline utilization, wirelength, overlap before and after legalization, displacement, shape distortion, channel width, congestion, routing failures, timing, runtime and memory. Separate the relaxed result from the legalized result and then evaluate detailed routing, extraction and timing. Test fixed macros, narrow channels, high terminal density, irregular module shapes, different module counts and cases where the relaxed optimum is near a hard boundary.

The captured official description claims qualitative floorplan quality and legalization efficiency. It reports no area, wirelength, overlap, congestion, timing or runtime result. The relaxation-to-legalization gap may be substantial. The evidence supports a differentiable polygon-shaping and flow-legalization direction, not demonstrated physical-flow improvement or universal superiority over sequence-pair and discrete methods. [Recorded evidence](../observed-subthemes/placement-routing-and-floorplanning.md#paper-dac-2026-research2024)

## Dual-side routing adds resources only when the two sides can be connected and manufactured

Conventional routing usually treats most signal paths as belonging to one primary side of the device or wafer. A dual-side process permits selected connections to use resources on both sides of the active device structure. That can increase the available routing space and shorten some paths, but it also adds interfaces between sides. Those interfaces may have limited locations, resistance, capacitance, alignment tolerances and manufacturing rules.

The Flip-FET record proposes a congestion-aware dual-side routing framework. The central problem is not simply to move a wire from the front side to the back side. The router must decide which nets benefit from the second side, where a net crosses between sides, how the two side-specific routing graphs share capacity, and whether the resulting device and interconnect geometry can be fabricated and verified.

<span id="explanation-dac-2026-research2139"></span>

### Flip-FET dual-side routing: a second routing side is useful only if side changes, rules and yield are modeled

#### What dual-side routing changes

A single-side router assigns a net's path to tracks, layers and vias in one routing domain. A dual-side router has at least two routing domains. Each domain can have its own layer directions, track density, blockages, preferred materials and design rules. A connection between domains needs a permitted transition through a contact, via, backside connection or other process-defined structure. The exact transition is process-specific and is not established by the captured description.

This creates a choice for every suitable net. Staying on one side may avoid transition cost but encounter congestion. Crossing sides may open a shorter or less crowded path but consume a scarce transition site and add electrical or manufacturing cost. A congestion-aware objective therefore needs more than total wirelength: it needs side-specific occupancy, transition count and location, local capacity, delay, power and rule penalties.

#### Why congestion is coupled across the sides

The two routing surfaces are not independent parallel grids. A dense region on one side may force many nets through the same crossing area, creating a bottleneck even if the other side has open tracks. A crossing site can also block device contacts, power delivery or neighboring signal paths. Routing decisions must account for both the local capacity on each side and the capacity of the interfaces between them.

The router may need to reserve crossing resources before all nets are known. If it assigns them greedily to early nets, later critical or high-fanout nets may be left with no legal transition. Rip-up and reroute can recover from that decision, but the cost and convergence behavior become part of the framework. A lower two-side wirelength score does not prove lower delay if extra transitions add resistance or capacitance, or if congestion causes detours.

#### Why Flip-FET process assumptions matter

The device process determines which side can host which wires and contacts, how a signal crosses the device, what alignment and enclosure rules apply, and how heat, power and mechanical stress are handled. Manufacturing may impose minimum widths, spacing, overlay tolerance, contact redundancy, defect sensitivity and yield limits. These are not details that can be inferred from a routing graph after the fact. They determine whether the graph's edges represent realizable structures.

The framework therefore needs a process-aware mapping from routing decisions to physical shapes. It must distinguish an abstract route, a design-rule-clean route, an extracted route with delay and a fabrication-ready layout. A route that is legal under a simplified two-side model may fail when contacts, backside access, power rails or yield constraints are included.

#### What a complete evaluation needs

Define the Flip-FET device structure, front- and back-side layers, track directions and capacities, transition structures, contact and via rules, blockages, power network, thermal assumptions, design-rule checker, extraction flow and yield model. Compare single-side routing and the conventional FET flow on the same netlists, constraints, layer budgets and compute hardware.

Report routed-net completion, wirelength, side-specific utilization, transition count, congestion and overflow, design-rule violations, timing slack, power, area, runtime, memory, rip-up iterations and yield or defect sensitivity. Test critical and high-fanout nets, dense interface regions, asymmetric side capacities, power-grid interaction, process variation, overlay error and designs of different sizes. Validate the result through extraction, timing, power, design-rule checking and, where claimed, fabrication or silicon data.

The captured official description claims qualitative routing and manufacturability benefits. It reports no congestion, timing, area, yield, design-rule or process result. Emerging-device assumptions may not transfer to mature flows. The evidence supports a congestion-aware dual-side routing direction for Flip-FET structures, not demonstrated fabrication-ready quality or universal superiority over single-side routing. [Recorded evidence](../observed-subthemes/placement-routing-and-floorplanning.md#paper-dac-2026-research2139)

## Multi-row complementary-FET cells couple device geometry to pin access

A standard cell is a reusable layout unit with defined height, power interfaces and signal pins. A complementary-FET cell contains complementary transistor networks that implement the logic function. In a multi-row cell, those devices and their routing resources span more than one row or organized device band. This can create more room for devices or allow a more compact arrangement, but it changes which diffusion regions, gates, contacts and wires can be shared or reached.

Cell synthesis must satisfy two different contracts. The internal geometry must obey device and manufacturing rules. The cell boundary must expose pins and power connections in positions that the chip-level placer and router can use. A cell can be area-efficient inside its boundary and still be a poor library element if its pins are blocked, its pin-access directions are restrictive, or its timing and extraction models are not characterized.

<span id="explanation-dac-2026-research2416"></span>

### Multi-row complementary-FET layout synthesis: compact device geometry is useful only when the cell remains routable and reusable

#### What layout synthesis is choosing

The standard cell synthesis process maps a logic function into transistors, diffusion or active regions, gates, contacts, local interconnect and higher-level wires. It chooses device positions, orientations, shared regions, contact locations, pin shapes, power rails and the cell boundary. In a multi-row arrangement, a signal may need to cross between rows or between device regions, so row alignment and available access tracks become part of the logic implementation.

Area is not just the rectangle around the cell. A smaller cell may reduce the footprint of every instance, but it can also reduce the space around pins and power rails. If a pin is reachable only from one direction, neighboring cells may block it when abutted. If a shared diffusion or contact saves area, it may couple devices that require different electrical or layout conditions. The synthesis objective must therefore include access and reuse constraints, not only cell width or transistor count.

#### Why complementary-FET and multi-row structure matters

Complementary device networks have distinct pull-up and pull-down structures and may need different diffusion, well, gate and contact relationships. A multi-row organization changes their relative placement and the path by which local interconnect reaches the cell boundary. The legal arrangement depends on the process design rules: minimum dimensions, spacing, enclosure, contact cuts, well or isolation requirements, layer directions, density and permitted device orientations.

These rules also affect routability. A layout with the right Boolean connectivity can still fail because a contact cannot be placed, a wire cannot leave a pin, a local track is blocked, or a neighboring cell creates a spacing violation. A routability-driven synthesizer should model the actual access geometry or a validated proxy for it. A generic count of open terminals is not enough if all terminals compete for the same track or direction.

#### Area optimality and routability can conflict

Sharing diffusion or aligning devices can lower area and reduce local parasitic length. The same sharing can force pins into a narrow region or make a critical internal connection longer. Adding a track or widening a boundary may improve access while increasing cell area. The relevant comparison is therefore multi-objective: area, pin accessibility, internal and external wirelength, congestion, parasitic delay, power and manufacturability must be evaluated together.

An “area-optimal” result is meaningful only after the constraints and denominator are fixed. State whether area means cell bounding-box area, active area, routing-inclusive area or a library-level footprint including spacing. State whether routability is measured by a pin-access checker, a detailed router, estimated overflow or completed chip-level placement and routing. These measurements answer different questions and must not be substituted for one another.

#### Why library integration is a separate test

A synthesized cell becomes useful only if it can be characterized and instantiated repeatedly. Characterization needs extracted parasitics, timing arcs, power behavior, signal slew and load ranges. Integration needs compatible height or row structure, power rails, abutment rules, pin naming, legal orientations and a router that understands the cell's access points. A cell that works in isolation may fail when placed beside another cell or when many instances create a repeated congestion pattern.

#### What a complete evaluation needs

Define the complementary-FET process, device and routing layers, row organization, cell boundary, power rails, allowed orientations, sharing rules, design-rule checker, extraction tool, characterization flow and library interface. Compare single-row synthesis and area-only synthesis with the same Boolean cells, constraints, process rules and compute budget.

Report cell area under a stated definition, transistor and contact count, pin-access failures, internal wirelength, external routability, congestion, design-rule violations, extracted delay, slew, power, leakage, runtime and yield or manufacturability checks. Include extracted parasitics, not only geometric distance. Test simple and high-fanout cells, dense pin patterns, shared-device opportunities, different drive strengths, abutted neighbors and repeated instances in a placed-and-routed design.

The captured official description claims qualitative area and routability benefits. It reports no area, pin-access, routing, timing, yield or process result. Area-optimal solutions may be difficult to integrate into a library. The evidence supports area- and routability-driven multi-row complementary-FET layout synthesis, not demonstrated signoff-ready library quality or universal superiority over single-row and area-only synthesis. [Recorded evidence](../observed-subthemes/placement-routing-and-floorplanning.md#paper-dac-2026-research2416)

## Detailed placement must improve timing without breaking legal cell geometry

Global placement chooses broad locations; detailed placement makes local changes such as moving a cell to a neighboring site, swapping cells, changing orientation, or compacting whitespace. These changes can improve a critical connection, but they must preserve row alignment, legal orientations, site occupancy, cell overlap rules, density limits and access to power and routing resources.

The LATTE record combines differentiable timing-driven optimization with a legality guarantee. The two words describe different obligations. Differentiability supplies a continuous direction for improving an objective. Legality means that the resulting cell arrangement satisfies discrete placement constraints. A smooth optimizer can guide movement, but the method needs a mechanism that prevents or repairs overlaps and density violations rather than assuming that a low objective is automatically legal.

<span id="explanation-dac-2026-research373"></span>

### LATTE detailed placement: a timing gradient matters only when the final cell arrangement remains legal

#### What detailed placement is changing

A standard-cell row provides discrete legal sites with fixed or restricted heights, orientations and power-rail relationships. Detailed placement operates within that structure. It may reorder neighboring cells, shift cells within whitespace, or exchange positions so that important pins and drivers become closer. The change must maintain non-overlap, row membership, placement blockages, density limits, well or implant requirements and legal cell orientations.

Timing is affected by more than center-to-center distance. A cell's drive strength, input capacitance, fanout, pin location, wire layer, buffering and local congestion influence delay. Moving one cell can improve one net while crowding another region or changing the load of a neighboring path. A timing-driven objective therefore needs a timing model and a clear definition of what is estimated during placement.

#### What differentiability contributes

Many placement variables are discrete, but gradients are easier to use on continuous coordinates or smooth approximations of density, wirelength and timing. A differentiable method can calculate how a small movement is expected to change the objective and repeatedly update cell positions. This can make timing optimization more systematic than a sequence of hand-designed swaps.

The gradient is still a proxy. It may be computed from estimated wirelength and approximate RC rather than the final routed parasitics. It may also point through an overlap or into a region that violates a site or density constraint. The method is meaningful only if the legality mechanism is part of the optimization or if any repair step is measured as part of the result.

#### What legality assurance must mean

“Legality-assured” should identify the invariant being preserved and the point at which it is checked. Possible conditions include no cell overlap, legal row and site assignment, allowed orientation, density bounds, blockage compliance, pin accessibility and design-rule constraints. A penalty that makes violations expensive is not the same as a proof that violations cannot occur. A post-optimization legalizer can produce a legal result, but if it moves cells substantially, the timing objective was evaluated on a different arrangement.

The evaluation must therefore separate three states: the differentiable intermediate placement, the legal detailed placement, and the routed and extracted design. Timing should be measured at each relevant state, with the final claim based on static timing analysis after routing rather than on the smooth objective alone.

#### What a complete evaluation needs

Define the cell rows and sites, legal orientations, blockages, density limits, overlap representation, timing engine, RC model, slack calculation, gradient objective, legality mechanism, legalizer, routing flow and stopping rule. Compare analytic detailed placement and timing-oblivious differentiable placement with the same netlists, libraries, timing constraints, seeds and compute budget.

Report worst and total negative slack, critical-path delay, wirelength, density and overflow, overlap count, illegal-site count, legalization displacement, pin-access failures, congestion, runtime, memory, convergence and timing-repair iterations. Then route and extract every comparison, rerun STA at stated corners and report whether the ranking survives final timing. Test high-density regions, macros and blockages, high-fanout nets, short-path and long-path timing limits, and designs with different cell distributions.

The captured official description claims qualitative timing and legality benefits. It reports no slack, wirelength, density, legality, runtime or signoff result. Differentiable relaxations may miss discrete legal constraints. The evidence supports a legality-aware differentiable detailed-placement direction, not demonstrated final timing closure or universal superiority over analytic and timing-oblivious placement. [Recorded evidence](../observed-subthemes/placement-routing-and-floorplanning.md#paper-dac-2026-research373)

## Gate sizing changes timing and power through the same electrical variables

Gate sizing chooses the strength or drive option of a logic cell. A larger cell can charge and discharge a downstream load faster because it can supply more current, but it usually presents more input capacitance and may consume more area, leakage power or dynamic power. A smaller cell can save power and area while increasing delay. The choice also changes the load seen by the previous stage, so a local improvement can move the cost to another part of the path.

The timing-power co-optimization record uses a differentiable method and calls its sizing mechanism “quad-gradient.” The captured description does not define the four gradients or the way they are combined. That name is therefore not treated as a specific mathematical guarantee. The important conceptual question is whether the gradient signals represent timing, power and their interactions accurately enough to choose discrete library cells and still improve the extracted, signoff-checked design.

<span id="explanation-dac-2026-research843"></span>

### Differentiable timing–power gate sizing: a continuous gradient must end in a valid discrete cell choice

#### What gate sizing changes in a circuit

Each logic instance usually selects one cell from a library family. The variants implement the same Boolean function with different transistor sizes or drive strengths. Selecting a stronger variant can reduce the delay of a heavily loaded transition, but it can increase the input capacitance that the previous cell must drive. It can also increase switching energy, leakage, area and local power density.

Sizing is therefore a network problem, not an independent choice per cell. The delay of a path depends on gate delay, wire resistance and capacitance, input slew, output load, fanout, buffering and operating corner. Power depends on switching activity, capacitance, voltage, frequency, leakage state and the selected cells. A sizing change can improve one critical path, make another path critical, or violate a power budget elsewhere.

#### Why a differentiable sizing model is difficult

The library choice is discrete. A cell may have drive options such as X1, X2 and X4, but there is no physical X2.7 cell simply because a continuous optimizer requests it. A differentiable method can represent a relaxed mixture, a continuous strength variable or a smooth surrogate for library choices. That representation provides a direction for optimization, but it must eventually be projected or rounded to an actual cell.

Rounding can change timing and power discontinuously. A relaxed point between two sizes may look attractive because it averages their costs, while either legal cell produces a different slew, load, leakage and path delay. The method should therefore report both relaxed optimization and the discrete mapped netlist, including any repair iterations required after mapping.

#### What timing and power gradients must capture

A timing gradient should identify how a cell-size change affects path delay and slack through its own output and through the loads it presents upstream. A power gradient should distinguish dynamic switching from leakage and should state the activity, voltage, frequency and corner assumptions. If the objective combines them, the weighting or constraint must be explicit: reducing power by a fixed amount is not equivalent to recovering one unit of slack.

The term “quad-gradient” does not, from the captured source alone, tell us whether the four signals refer to rise/fall timing, setup/hold timing, timing/power components or another decomposition. A reproducible paper-level account must define each gradient, its units, its update schedule, its normalization and how conflicting directions are resolved. Without that information, the mechanism can be understood as differentiable timing-power co-optimization, but not independently reconstructed from the title.

#### Why signoff validation is required

The optimization may use approximate cell models, wireload estimates or differentiable surrogates. Legal library mapping, buffering, routing and parasitic extraction change the electrical network. Final static timing analysis can expose setup or hold violations that the relaxed objective missed. Power analysis can change after real switching activity, clock-tree effects, glitches, leakage corners and routed capacitance are included.

#### What a complete evaluation needs

Define the cell library and drive options, timing and power models, activity assumptions, voltage and frequency, corners, setup/hold constraints, gradient decomposition, objective weights or constraints, discrete mapping rule, repair policy, routing flow and extraction tool. Compare heuristic gate sizing and single-objective differentiable sizing with the same netlists, initial cells, constraints, seeds and compute budget.

Report worst and total negative slack, setup and hold violations, critical-path delay, dynamic and leakage power, area, cell-count changes, slew, capacitance, convergence, runtime, memory, discrete-rounding loss and repair iterations. Route and extract all final netlists, rerun multi-corner STA and power analysis, and report whether the timing-power tradeoff survives. Test low- and high-activity designs, fanout-heavy paths, multiple voltage corners, hold-limited paths and designs not used to tune the model.

The captured official description claims a qualitative timing-power tradeoff. It reports no slack, power, area, convergence, runtime or signoff result, and it does not define the four gradients. Continuous gradients may misrepresent discrete library behavior. The evidence supports a differentiable timing-power sizing direction, not demonstrated signoff improvement or universal superiority over heuristic and single-objective sizing. [Recorded evidence](../observed-subthemes/placement-routing-and-floorplanning.md#paper-dac-2026-research843)

## Parallel routing depends on how the netlist is divided

A netlist records which circuit pins must be connected. A parallel router divides the work among workers or regions so that multiple routing tasks can proceed at the same time. The division changes the problem: a net whose terminals fall in different partitions becomes a boundary or cut net, and workers must coordinate to route it without conflicting over shared tracks.

Partition quality therefore has at least two dimensions. Work must be balanced so that one worker does not become the serial bottleneck. Connectivity should remain local so that fewer nets cross partition boundaries and less synchronization is needed. These goals can conflict. A balanced partition can cut many long or high-fanout nets; a locality-preserving partition can place most difficult routing work in one region.

<span id="explanation-dac-2026-research320"></span>

### SAAP spatial-aware partitioning: a partition is useful only when locality, balance and boundary routing improve together

#### What a VLSI netlist partition represents

A partition assigns cells or netlist objects to groups. A graph model treats cells as vertices and connections as edges. A hypergraph model represents a multi-terminal net directly, because cutting one net can affect several partitions at once. A spatial-aware model adds physical information such as cell coordinates, estimated bounding boxes, routing demand and region capacity.

The partitioner typically tries to minimize cut cost while keeping group sizes or estimated work within bounds. Cut size alone is not enough. Cutting a short low-fanout net may be cheap, while cutting a long timing-critical or high-fanout net may create many boundary connections. A spatial partition should account for the location and routing demand of the cut nets, not merely the number of graph edges.

#### Why parallel routing needs both locality and balance

If each worker owns a compact physical region, most local nets can be routed without communication. That reduces shared-state contention and makes memory access more predictable. Boundary nets still require coordination: the workers need compatible entry points, reserved tracks, layer assignments and a rule for resolving conflicts.

If one worker receives a dense region, many high-fanout nets or the most difficult blockages, total runtime is determined by that worker even when other workers finish early. A partitioning objective can therefore include estimated routing work, congestion, net degree, cut penalties and region capacity. The weights must be measured against actual routing time; a proxy that balances cell counts may not balance route search or rip-up work.

#### What spatial awareness can and cannot do

Spatial coordinates can expose locality that an abstract graph misses. Two cells connected by a net may be adjacent in the layout, while another graph connection may span a large region and require multiple routing resources. Spatial information can guide partition boundaries away from dense channels or keep strongly connected nearby objects together.

It cannot remove the physical coupling at a boundary. A partition line can cut a narrow routing corridor, concentrate crossings at a few pins, or separate a net's terminals even when the cells themselves are balanced. Independent local routers can also choose paths that look valid within each region but conflict at the shared boundary. The partitioner must therefore be evaluated with the parallel router and its boundary protocol, not as an isolated graph score.

#### What a complete evaluation needs

Define the graph or hypergraph representation, spatial features, partition count, balance constraint, cut-net cost, routing-work estimate, boundary ownership, shared-resource protocol, synchronization method and router. Compare graph partitioning without spatial awareness and serial routing under the same netlists, technology, routing rules, hardware, worker count and termination criteria.

Report cut size by net class, partition imbalance, boundary crossings, congestion, routing overflow, unrouted nets, design-rule violations, wirelength, timing, parallel speedup, total runtime, worker idle time, memory, communication volume and reproducibility across seeds. Separate algorithm time from data preparation and final verification. Test sparse and dense layouts, high-fanout nets, irregular blockages, different partition counts, uneven routing demand and designs larger than the tuning set.

The captured official description claims qualitative routing scalability and partition quality. It reports no cut size, congestion, routing success, runtime or scale result. Partitions may create boundary congestion. The evidence supports a spatial-aware analytic partitioning direction for parallel routing, not demonstrated end-to-end speedup, routing completion or signoff-routing superiority. [Recorded evidence](../observed-subthemes/placement-routing-and-floorplanning.md#paper-dac-2026-research320)

## Backside power delivery moves the power network, not the verification burden

Power delivery supplies current to transistors and returns it through a network of metal layers, contacts and sources. The resistance of that network causes voltage loss when current flows. This loss is IR drop. A larger local drop reduces the voltage available to a cell and can slow it down or make its behavior less reliable. Current density can also create electromigration risk, and the power network interacts with heat and signal routing.

Backside power delivery places selected power-distribution resources on the side of the die opposite the main signal-routing surface. The intended benefit is to free frontside routing space or shorten parts of the power path. The change introduces process-specific connections between the backside network and the device layer, plus constraints from alignment, resistance, thermal flow, mechanical structure and manufacturing yield.

<span id="explanation-dac-2026-research335"></span>

### BSPDN-Elite: a backside power network is useful only when IR drop, timing, routing and process rules are solved together

#### What a BSPDN design is changing

In a conventional frontside power-delivery arrangement, signal interconnect and power rails compete for some of the same routing layers and area. A backside power-distribution network can move selected power paths away from those signal resources. This changes the optimization problem: the framework must choose power-network geometry, connections through the device stack, signal-routing resources, placement or cell assumptions and operating conditions together.

The power network is a spatial electrical network. Each segment has resistance, and each load draws current that varies with activity and time. The voltage at a load is the source voltage minus the drops along the current path. If nearby loads share a narrow or resistive path, their drops can interact. A design with lower average resistance may still have a local worst-case drop at a high-current region.

#### Why power, timing and routing are coupled

IR drop changes the voltage seen by cells, which changes delay and possibly slew. Timing repair may add or resize cells, increasing current and changing the power network's load. Moving signal routes to free space for power can increase wirelength, capacitance or congestion. Moving power resources to the backside can require special vias or contacts that consume area and have their own resistance and reliability limits.

These effects create feedback rather than independent objectives. A framework that minimizes power-network resistance without checking signal routing can create frontside congestion elsewhere. A framework that minimizes congestion without solving the current distribution can leave a timing-critical region under-supplied. Combining scores is not enough unless each score is calibrated, constrained and recomputed after the physical design changes.

#### What process assumptions control the result

Backside power delivery depends on the process stack: available backside metals, connection structures, contact resistance, alignment tolerance, thermal path, mechanical support, design rules and yield model. The allowed path from the backside network to device power pins determines whether an abstract edge in the optimization graph corresponds to a manufacturable structure. Process variation can change both resistance and current distribution.

The framework must distinguish an estimated power network from a routed and extracted network. It must also state whether the reported timing uses voltage-aware cell models, whether IR drop is static or dynamic, how temperature is modeled, and which corners or workloads are checked. Without these conditions, a claimed improvement may be specific to a simplified stack or a particular node.

#### What a complete evaluation needs

Define the frontside and backside layer stacks, power sources, load currents, backside-to-device connection structures, resistance and capacitance models, IR-drop analysis, electromigration rules, thermal model, signal-routing constraints, timing corners, extraction tools and process-yield assumptions. Compare frontside power delivery and single-objective BSPDN optimization with the same netlists, placement, activity, voltage, frequency, routing flow and compute budget.

Report worst and distributional IR drop, current density, electromigration margin, timing slack, setup and hold violations, dynamic and leakage power, area, signal congestion, transition count, thermal distribution, runtime, memory, yield sensitivity and repair iterations. Re-run extraction, voltage-aware timing, power integrity, thermal and design-rule checks on the final routed design. Test high-current blocks, uneven activity, dense signal regions, voltage corners, temperature variation and more than one process or stack when transfer is claimed.

The captured official description claims qualitative timing, power and routing benefits. It reports no IR drop, timing, power, congestion, thermal, yield or runtime result. Backside process assumptions may not transfer across nodes. The evidence supports a multi-objective BSPDN design direction, not demonstrated signoff integrity, process portability or universal superiority over frontside delivery and single-objective optimization. [Recorded evidence](../observed-subthemes/placement-routing-and-floorplanning.md#paper-dac-2026-research335)

## Compare completed designs under the same rules

Use the same circuit, cell library, physical constraints, and routing flow. State which results come from initial placement, legal placement, detailed routing, and final checks. Report unrouted connections, rule violations, timing failures, and repair effort as well as favorable scores.

Measure total runtime and resources, including final evaluation and repair. Vary design size and structural difficulty. The useful conclusion is that a particular choice improves completed valid designs under stated conditions. A faster intermediate optimization step remains a narrower result until its effect on completion is established.

## Compare the results carefully

First identify the inputs and required output quality. Then identify the limited resource: time, memory, communication, energy, circuit area, or correctness coverage. Ask which part of the method reduces that cost and which new cost it adds. Compare numbers only when the experiments hold these conditions sufficiently similar.

A conference description may explain the proposal while omitting the full experiment. An author preprint link may have been coded from its abstract. The source classification does not by itself establish that every table was read. Missing locations remain visible below.

## Complete captured evidence

These are evidence records, not substitutes for the explanations above. Each record preserves its problem, proposed method, measurements, comparison conditions, and source limits. A populated record does not establish that its mechanism has been fully explained or independently verified.

<span id="paper-dac-2026-research2006"></span>

### Cell-Structure-Independent Transistor-Level Placement and MOL-Aware Routing Framework Beyond the Standard-Cell Paradigm

DAC 2026 · Record: `dac-2026-research2006`

[Read the step-by-step explanation](#explanation-dac-2026-research2006)

**Updated source-backed reading card**

Reviewed 2026-09-08. Deepens the existing cell-structure-independent placement treatment into a paper-level reading; defines the standard-cell boundary, transistor-level freedom and MOL/M0 routing constraint, and separates abstract wirelength/area from legal routed and signoff-ready design quality.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Fixed standard-cell boundaries constrain pin access, M0/MOL routing, wirelength and area optimization at advanced technology nodes.

**Mechanism / artifact:**

Transistor-level placement independent of fixed cell structure coupled to an MOL-aware routing engine; device representation, placement objective, lower-level routing rules, extraction and signoff flow are unspecified.

**Workload — the work tested:**

VLSI designs evaluated against a commercial standard-cell flow and prior transistor-level work; circuit suite, design size, netlist structure, technology node, timing/power constraints and metrics are unspecified.

**Hardware and manufacturing assumptions:**

Advanced-node transistor-level physical design with dense pin access and MOL/M0 routing resources; PDK, design rules, device models, extraction, corners, power grid and signoff assumptions are unspecified.

**Baseline — the comparison method:**

Commercial standard-cell-based design tool

State-of-the-art transistor-level work

Netlist, technology, routing, extraction, timing, power, resource and signoff conditions are unspecified

**Reported measurements:**

Wirelength and design-area improvement are claimed qualitatively; no numeric wirelength, area, timing, power, leakage, congestion, unrouted-net, design-rule, runtime, memory or signoff result is reported.

**Limits on the conclusion:**

Removing standard-cell boundaries expands device placement choices but also removes characterized interfaces and predictable routing abstractions. Lower abstract wirelength or transistor area does not guarantee legal MOL/M0 access, lower delay, lower power or final area after routing, extraction and repair.

MOL-aware routing must handle terminal access, local tracks, contacts, spacing, enclosure, shorts, power connections and later-layer interactions. A higher-level placement score cannot establish that every required transistor connection can be manufactured.

The official description reports no numeric PPA, timing, power, routability, design-rule or technology-node result. The record supports a broader transistor-level physical-design direction, not proven signoff-ready improvement.

**Source and location**

Evidence tier: Primary captured official DAC description plus existing chapter level cell structure independent placement discussion; no full paper extraction, mol/m0 reproduction or signoff validation. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH2006&sess=sess132)

DAC 2026 official description; captured Problem, Mechanism / artifact, Workload, Hardware, Baseline, Measurements and Limits fields; record RESEARCH2006; no manuscript pages.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** commercial standard-cell-based design tool

state-of-the-art transistor-level work

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH2006&sess=sess132

**Hardware or process assumptions:** Advanced-node transistor-level physical design with dense pin access and MOL/M0 routing resources; PDK, design rules, extraction, and signoff assumptions are unspecified.

**Limits:** The description omits numeric PPA results, timing/power impacts, routability, design-rule compliance, and technology-node details.

Relaxing cell structure may increase design complexity, variability, and verification/signoff cost.

Official description only; physical-design claims require paper-level and signoff-condition verification.

**Method or artifact:** Transistor-level placement independent of fixed cell structure coupled to an MOL-aware routing engine.

**Metrics:** Wirelength improvement claimed qualitatively

Design-area improvement claimed qualitatively

**Problem:** Fixed standard-cell boundaries constrain pin access, M0/MOL routing, wirelength, and area optimization at advanced technology nodes.

**Workload or benchmark:** VLSI designs evaluated against a commercial standard-cell flow and prior transistor-level work; circuit suite, technology node, timing/power constraints, and metrics are unspecified.

</details>

<span id="paper-dac-2026-research2133"></span>

### Toward True-3D Timing-Driven Analytical Global Placement for Mixed-Size Face-to-Face 3D ICs

DAC 2026 · Record: `dac-2026-research2133`

[Read the step-by-step explanation](#explanation-dac-2026-research2133)

**Updated source-backed reading card**

Reviewed 2026-09-08. Deepens the existing true-3D placement treatment into a paper-level reading; defines mixed-size analytical placement and vertical interconnect, separates timing proxies and differentiable boundaries from legal routed 3D implementation, and makes bonding, thermal, STA and signoff conditions explicit.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Timing optimization remains underdeveloped in analytical placement for mixed-size face-to-face 3D ICs with vertical interconnects and hybrid bonding.

**Mechanism / artifact:**

Timing-driven net weighting and differentiable macro-boundary-aware true-3D initialization adaptable to 3D and multi-die 2D placement; weighting, boundary penalty, die assignment, bonding, routing and signoff models are unspecified.

**Workload — the work tested:**

Mixed-size face-to-face 3D IC placement with STA and RC timing; designs, die assignments, macro sizes, bond density, timing paths, technology, metrics and baselines are unspecified.

**Hardware and manufacturing assumptions:**

Hybrid-bonded or micro-bump 3D ICs with multi-die placement and vertical interconnect; process, thermal, power, bonding, alignment, routing, extraction, RC and STA assumptions are unspecified.

**Baseline — the comparison method:**

Timing-oblivious analytical placement

Prior 3D global-placement methods

Netlist, die stack, routing, legalization, extraction, timing, thermal and signoff conditions are unspecified

**Reported measurements:**

Timing-aware placement capability is claimed qualitatively; no wirelength, vertical-crossing, timing/slack, congestion, thermal, power, runtime, memory, legalization or signoff result is reported.

**Limits on the conclusion:**

In face-to-face 3D placement, coordinate distance is not the full wire path. Hybrid bonds or micro-bumps have sites, alignment, electrical, thermal and mechanical constraints; a smooth analytical position can change during legalization and routing.

Timing weights depend on RC, fanout, driver, layers, vertical crossings and slack. A differentiable macro-boundary penalty is an approximation to discrete legal placement, blockage, power, thermal and bonding rules; improving the proxy does not establish timing closure.

The official description reports no wirelength, timing, congestion, thermal or runtime result. The record supports a 3D analytical-placement direction, not demonstrated timing closure or manufacturing-ready 3D quality.

**Source and location**

Evidence tier: Primary captured official DAC description plus existing chapter level true 3d placement discussion; no full paper extraction, 3d routing/thermal validation or signoff experiment. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH2133&sess=sess132)

DAC 2026 official description; captured Problem, Mechanism / artifact, Workload, Hardware, Baseline, Measurements and Limits fields; record RESEARCH2133; no manuscript pages.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** timing-oblivious analytical placement

prior 3D global-placement methods

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH2133&sess=sess132

**Hardware or process assumptions:** Hybrid-bonded or micro-bump 3D ICs with multi-die placement and vertical interconnect; process, thermal, power, and bonding constraints are unspecified.

**Limits:** The description omits wirelength, timing, congestion, thermal, and runtime results.

RC and STA approximations may not capture bonding, thermal, or signoff effects.

Official description only; physical-design claims require paper-level signoff validation.

**Method or artifact:** Timing-driven net weighting and differentiable macro-boundary-aware true-3D initialization adaptable to 3D and multi-die 2D placement.

**Metrics:** Timing-aware placement capability claimed qualitatively

**Problem:** Timing optimization remains underdeveloped in analytical placement for mixed-size face-to-face 3D ICs with vertical interconnects and hybrid bonding.

**Workload or benchmark:** Mixed-size face-to-face 3D IC placement with STA and RC timing; designs, technology, timing metrics, and baselines are unspecified.

</details>

<span id="paper-dac-2026-research1290"></span>

### Analytically-Derived Hybrid Net–pin Weighting for Timing-Driven Global Placement

DAC 2026 · Record: `dac-2026-research1290`

[Read the step-by-step explanation](#explanation-dac-2026-research1290)

**Updated source-backed reading card**

Reviewed 2026-09-08. Deepens the existing hybrid net–pin weighting treatment into a paper-level reading; defines net/sink criticality, separates analytical placement objective values from post-route timing, and makes timing-model, congestion, convergence and final-STA requirements explicit.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Timing-driven placement must balance wirelength and critical-path delay while avoiding unstable heuristic weighting.

**Mechanism / artifact:**

Analytical hybrid weighting of nets and pins integrated into global placement optimization; weighting derivation, slack/criticality inputs, timing model, congestion model, update rule and objective are unspecified.

**Workload — the work tested:**

Timing-driven circuit placement benchmarks; netlist size, fanout, critical paths, technology, timing engine, congestion, constraints, convergence and benchmark suite are unspecified.

**Hardware and manufacturing assumptions:**

ASIC global placement with timing constraints and interconnect delay estimation; technology node, cell library, RC model, legalization, routing, extraction and timing corners are unspecified.

**Baseline — the comparison method:**

Wirelength-driven placement

Heuristic timing-weighted placement

Netlist, timing model, congestion, compute budget, routing and final-STA conditions are unspecified

**Reported measurements:**

Timing and placement quality improvements are claimed qualitatively; no wirelength, worst negative slack, total negative slack, critical-path delay, congestion, runtime, memory, convergence or benchmark result is reported.

**Limits on the conclusion:**

A net-level weight treats all sinks alike, while one pin may be critical and another may have slack or a different load. Hybrid net–pin weights can guide an estimated objective, but their value depends on slack, fanout, RC, congestion and timing-model assumptions.

A lower placement objective does not guarantee lower final delay. Legalization, buffering, detailed routing, layer assignment, parasitic extraction and operating corners can change the critical path; improving one sink can increase another sink's load or create congestion.

The official description reports no wirelength, worst negative slack, congestion, runtime or benchmark details. The record supports analytical net–pin weighting, not established timing closure or universal superiority over heuristic weighting.

**Source and location**

Evidence tier: Primary captured official DAC description plus existing chapter level hybrid net–pin weighting discussion; no full paper extraction, routed timing validation or reproducible benchmark comparison. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH1290&sess=sess132)

DAC 2026 official description; captured Problem, Mechanism / artifact, Workload, Hardware, Baseline, Measurements and Limits fields; record RESEARCH1290; no manuscript pages.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** wirelength-driven placement

heuristic timing-weighted placement

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH1290&sess=sess132

**Hardware or process assumptions:** ASIC global placement with timing constraints and interconnect delay estimation; technology node and congestion model are unspecified.

**Limits:** The description omits wirelength, worst negative slack, congestion, runtime, and benchmark details.

Analytical weighting may depend on timing-model assumptions.

Official description only; placement claims require reproducible benchmark comparisons.

**Method or artifact:** Analytical hybrid weighting of nets and pins integrated into global placement optimization.

**Metrics:** Timing and placement quality improvements are claimed qualitatively

**Problem:** Timing-driven placement must balance wirelength and critical-path delay while avoiding unstable heuristic weighting.

**Workload or benchmark:** Timing-driven circuit placement benchmarks; designs, timing engine, convergence, and comparison flow are unspecified.

</details>

<span id="paper-dac-2026-research1404"></span>

### Learning-Based Slack-Aware Timing-Driven Global Placement for Large-Scale Heterogeneous FPGAs

DAC 2026 · Record: `dac-2026-research1404`

[Read the step-by-step explanation](#explanation-dac-2026-research1404)

**Updated source-backed reading card**

Reviewed 2026-09-08. Deepens the existing learning-based slack-aware FPGA placement treatment into a paper-level reading; defines heterogeneous site assignment, slack, learned placement policy, legality, routing and generalization, and separates predicted timing from final routed timing closure.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Large heterogeneous FPGA placement must balance legal resource assignment, timing slack and routability at scale.

**Mechanism / artifact:**

Learning-based slack-aware timing-driven global placement; model inputs, action space, training objective, legality handling, timing model and update rule are unspecified.

**Workload — the work tested:**

Large heterogeneous FPGA netlists; FPGA family, resource mix, device size, timing constraints, training/evaluation split, routing tool and benchmark details are unspecified.

**Hardware and manufacturing assumptions:**

Heterogeneous FPGA fabric containing multiple site types, routing tracks and clocking constraints; architecture, site capacities, routing graph and timing model are unspecified.

**Baseline — the comparison method:**

Wirelength-driven FPGA placement

Heuristic timing-driven placement

Netlists, FPGA architectures, seeds, placement/routing budgets and final timing flow are unspecified

**Reported measurements:**

Timing and placement quality improvements are claimed qualitatively; no slack, wirelength, congestion, overflow, unrouted-net, runtime, memory, training-cost, seed-variance or cross-device result is reported.

**Limits on the conclusion:**

FPGA placement assigns logic to discrete heterogeneous site types and must preserve carry, memory, arithmetic, clock, pin and routing constraints. A geometric or predicted timing improvement can be lost during legalization or routing.

Slack is a timing margin estimated from a timing and routing model. Fanout, congestion, detours, buffering, clock effects and final routed delay can change it; a learned policy guides placement decisions but does not replace final timing analysis.

A learned policy may encode the architectures and circuits used for training. The official description reports no training split, held-out-device result, slack, wirelength, congestion, runtime or generalization measurement. The record supports a learning-based slack-aware placement direction, not proven timing closure or universal superiority over heuristic placement.

**Source and location**

Evidence tier: Primary captured official DAC description plus existing chapter level FPGA placement discussion; no full paper extraction, routed timing validation or cross device experiment. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH1404)

DAC 2026 official description; captured Problem, Mechanism / artifact, Workload, Hardware, Baseline, Measurements and Limits fields; record RESEARCH1404; no manuscript pages.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** wirelength-driven FPGA placement

heuristic timing-driven placement

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH1404

**Hardware or process assumptions:** Heterogeneous FPGA fabric with timing and routing constraints; architecture and process are unspecified.

**Limits:** No slack, wirelength, congestion, runtime, or generalization results are reported.

Learned policies may be architecture-specific.

Official description only; cross-device validation is required.

**Method or artifact:** Learning-based slack-aware timing-driven global placement.

**Metrics:** Timing and placement quality are claimed qualitatively

**Problem:** FPGA placement must balance timing slack, heterogeneity, and routability at scale.

**Workload or benchmark:** Large heterogeneous FPGA netlists; device architecture, timing engine, and baselines are unspecified.

</details>

<span id="paper-dac-2026-research1534"></span>

### DRΛMA: Detailed Routing by a Versatile Maze Routing Algorithm

DAC 2026 · Record: `dac-2026-research1534`

[Read the step-by-step explanation](#explanation-dac-2026-research1534)

**Updated source-backed reading card**

Reviewed 2026-09-08. Deepens the existing DRΛMA routing treatment into a paper-level reading; defines the routing graph, maze expansion, shared capacity, negotiated congestion, physical legality, extraction and signoff, and separates a found path from a completed valid route.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Detailed routing must find legal, low-cost paths under congestion and design-rule constraints.

**Mechanism / artifact:**

Versatile maze-routing algorithm for detailed physical design routing; graph construction, cost terms, net ordering, rip-up policy, technology-rule encoding and stopping condition are unspecified.

**Workload — the work tested:**

ASIC detailed-routing benchmarks; netlists, technology node, layer stack, congestion, blockages, design rules, baselines and signoff flow are unspecified.

**Hardware and manufacturing assumptions:**

Advanced-node multi-layer physical routing with layer, track, via, spacing and manufacturing rules; exact process, routing graph and signoff assumptions are unspecified.

**Baseline — the comparison method:**

Classical maze routing

Commercial detailed router

Netlists, rule complexity, hardware, runtime budget, extraction and signoff conditions are unspecified

**Reported measurements:**

Routing quality and runtime are claimed qualitatively; no routed-net completion, design-rule count, wirelength, via count, timing, congestion, overflow, runtime, memory or signoff result is reported.

**Limits on the conclusion:**

A graph path is not automatically a legal physical route. The graph must encode track direction, capacity, layer transitions, via and spacing rules; final design-rule checking and extraction can expose failures not visible in path search.

Routes consume shared resources. A short route can create channel overflow or block later nets, while rip-up and reroute can trade one net's improvement for another net's failure. Wirelength alone does not establish routability, timing or signal integrity.

The official description reports no design-rule count, wirelength, via count, timing, congestion, runtime or signoff result. Behavior may depend on rule complexity and graph fidelity. The record supports a versatile maze-routing direction, not demonstrated signoff-scale superiority or universal robustness.

**Source and location**

Evidence tier: Primary captured official DAC description plus existing chapter level detailed routing discussion; no full paper extraction, signoff validation or reproducible benchmark comparison. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH1534)

DAC 2026 official description; captured Problem, Mechanism / artifact, Workload, Hardware, Baseline, Measurements and Limits fields; record RESEARCH1534; no manuscript pages.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** classical maze routing

commercial detailed router

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH1534

**Hardware or process assumptions:** Advanced-node routing with multi-layer design rules; layer stack and signoff assumptions are unspecified.

**Limits:** No DRC count, wirelength, vias, timing, congestion, or runtime results are reported.

Algorithm behavior may depend on rule complexity.

Official description only; signoff-scale reproducibility is required.

**Method or artifact:** Versatile maze-routing algorithm for detailed physical design routing.

**Metrics:** Routing quality and runtime are claimed qualitatively

**Problem:** Detailed routing must find legal, low-cost paths under congestion and design-rule constraints.

**Workload or benchmark:** ASIC detailed-routing benchmarks; technology, rules, congestion, and baselines are unspecified.

</details>

<span id="paper-dac-2026-research2024"></span>

### Rectilinear Soft Module Floorplanning via Differentiable Polygon Shaping Model and Flow-Based Legalization

DAC 2026 · Record: `dac-2026-research2024`

[Read the step-by-step explanation](#explanation-dac-2026-research2024)

**Updated source-backed reading card**

Reviewed 2026-09-08. Deepens the existing rectilinear soft-module floorplanning treatment into a paper-level reading; defines soft polygon shaping, differentiable proxy objectives, flow-based legalization and the gap between relaxed and legal physical designs.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Rectilinear soft modules are difficult to optimize continuously while maintaining legal, non-overlapping floorplans.

**Mechanism / artifact:**

Differentiable polygon-shaping model with flow-based legalization; polygon representation, smooth penalties, flow network, constraints and legalization objective are unspecified.

**Workload — the work tested:**

Rectilinear floorplanning instances; module counts, fixed blocks, aspect-ratio and polygon constraints, terminal locations, routing model and benchmark details are unspecified.

**Hardware and manufacturing assumptions:**

ASIC floorplanning with rectilinear soft modules and routing constraints; technology, minimum-width rules, blockages, power and signoff assumptions are unspecified.

**Baseline — the comparison method:**

Sequence-pair floorplanning

Discrete rectilinear legalization

Module sets, constraints, seeds, compute budget, routing, extraction and timing flow are unspecified

**Reported measurements:**

Floorplan quality and legalization efficiency are claimed qualitatively; no area, wirelength, overlap, displacement, congestion, timing, runtime, memory or post-route result is reported.

**Limits on the conclusion:**

A differentiable polygon model optimizes a continuous proxy for discrete geometry. A low relaxed objective can still contain overlap, invalid edges, narrow channels or inaccessible terminals, and legalization may move or reshape modules substantially.

Flow-based legalization solves a separate feasibility and movement problem. Its cost must include displacement, shape distortion, lost routing space and later timing or congestion repair; a good pre-legalization score does not establish a good legal floorplan.

The official description reports no area, wirelength, overlap, congestion, timing or runtime result. The relaxation-to-legalization gap may be substantial. The record supports a differentiable polygon-shaping and flow-legalization direction, not demonstrated physical-flow improvement or universal superiority over sequence-pair and discrete methods.

**Source and location**

Evidence tier: Primary captured official DAC description plus existing chapter level soft module floorplanning discussion; no full paper extraction, physical flow validation or reproducible benchmark comparison. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH2024)

DAC 2026 official description; captured Problem, Mechanism / artifact, Workload, Hardware, Baseline, Measurements and Limits fields; record RESEARCH2024; no manuscript pages.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** sequence-pair floorplanning

discrete rectilinear legalization

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH2024

**Hardware or process assumptions:** ASIC floorplanning with rectilinear modules and routing constraints; technology assumptions are unspecified.

**Limits:** No area, wirelength, overlap, congestion, timing, or runtime results are reported.

Relaxation-to-legalization gaps may be substantial.

Official description only; full physical-flow validation is required.

**Method or artifact:** Differentiable polygon-shaping model with flow-based legalization.

**Metrics:** Floorplan quality and legalization efficiency are claimed qualitatively

**Problem:** Rectilinear soft modules are difficult to optimize continuously while maintaining legal, non-overlapping floorplans.

**Workload or benchmark:** Rectilinear floorplanning instances; module counts, constraints, and baselines are unspecified.

</details>

<span id="paper-dac-2026-research2139"></span>

### Flip-FET-Based VLSI Design Framework with Congestion-Aware Dual-Side Routing

DAC 2026 · Record: `dac-2026-research2139`

[Read the step-by-step explanation](#explanation-dac-2026-research2139)

**Updated source-backed reading card**

Reviewed 2026-09-08. Deepens the existing Flip-FET dual-side-routing treatment into a paper-level reading; defines side-specific routing resources, inter-side transitions, shared congestion, process-dependent legality, extraction and fabrication/yield boundaries.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Emerging Flip-FET structures require routing methods that exploit both sides without creating congestion or manufacturing violations.

**Mechanism / artifact:**

Congestion-aware dual-side routing framework for Flip-FET VLSI; side-specific graph, transition structures, cost terms, process rules, extraction and yield model are unspecified.

**Workload — the work tested:**

Flip-FET layouts and routing benchmarks; device structure, front/back layers, track capacities, contacts, blockages, power network, baselines and validation flow are unspecified.

**Hardware and manufacturing assumptions:**

Flip-FET process with dual-side routing; design rules, side transitions, contacts, alignment, thermal, defect and yield assumptions are unspecified.

**Baseline — the comparison method:**

Single-side routing

Conventional FET routing flow

Netlists, layer budgets, device rules, extraction, compute budget and fabrication conditions are unspecified

**Reported measurements:**

Routing and manufacturability are claimed qualitatively; no congestion, timing, area, transition count, design-rule, yield, runtime, power or process result is reported.

**Limits on the conclusion:**

The two routing sides are coupled by scarce inter-side transitions. A second side can reduce local congestion while creating a bottleneck at contacts or transition sites; side-specific occupancy and interface capacity must be modeled together.

A dual-side graph path does not establish a realizable Flip-FET structure. Device contacts, backside access, alignment, spacing, power, thermal and defect rules determine whether transitions and routes can be fabricated; extraction can change timing after routing.

The official description reports no congestion, timing, area, yield, design-rule or process result. Emerging-device assumptions may not transfer to mature flows. The record supports a congestion-aware dual-side routing direction, not demonstrated fabrication-ready quality or universal superiority over single-side routing.

**Source and location**

Evidence tier: Primary captured official DAC description plus existing chapter level dual side routing discussion; no full paper extraction, fabrication aware validation or reproducible benchmark comparison. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH2139)

DAC 2026 official description; captured Problem, Mechanism / artifact, Workload, Hardware, Baseline, Measurements and Limits fields; record RESEARCH2139; no manuscript pages.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** single-side routing

conventional FET routing flow

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH2139

**Hardware or process assumptions:** Flip-FET process with dual-side routing; design rules, contacts, and yield assumptions are unspecified.

**Limits:** No congestion, timing, area, yield, DRC, or process results are reported.

Emerging-device assumptions may not transfer to mature flows.

Official description only; fabrication-aware validation is required.

**Method or artifact:** Congestion-aware dual-side routing framework for Flip-FET VLSI.

**Metrics:** Routing and manufacturability are claimed qualitatively

**Problem:** Emerging Flip-FET structures require routing methods that exploit both sides without creating congestion or manufacturing violations.

**Workload or benchmark:** Flip-FET layouts and routing benchmarks; device rules, layers, and baselines are unspecified.

</details>

<span id="paper-dac-2026-research2416"></span>

### Area-Optimal and Routability-Driven Layout Synthesis for Multi-Row Complementary-FET Standard Cells

DAC 2026 · Record: `dac-2026-research2416`

[Read the step-by-step explanation](#explanation-dac-2026-research2416)

**Updated source-backed reading card**

Reviewed 2026-09-08. Deepens the existing multi-row complementary-FET layout-synthesis treatment into a paper-level reading; defines device geometry, cell-boundary and pin-access contracts, area/routability tradeoffs, extraction, characterization and library-integration limits.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Multi-row complementary-FET cells need compact layouts that remain routable and manufacturable.

**Mechanism / artifact:**

Area-optimal, routability-driven standard-cell layout synthesis; device mapping, row organization, sharing rules, pin-access model, process rules and characterization flow are unspecified.

**Workload — the work tested:**

Multi-row complementary-FET standard cells; logic functions, drive strengths, device rules, libraries, neighbors, routing flow and benchmark details are unspecified.

**Hardware and manufacturing assumptions:**

Complementary-FET standard-cell process with multi-row placement; diffusion, gate, contact, well/isolation, routing, extraction and manufacturability assumptions are unspecified.

**Baseline — the comparison method:**

Single-row standard-cell synthesis

Area-only layout synthesis

Cell definitions, process rules, pin-access checker, extraction, characterization and chip-level routing conditions are unspecified

**Reported measurements:**

Area and routability are claimed qualitatively; no area definition, pin-access, routing, timing, yield, design-rule, power, extraction or process result is reported.

**Limits on the conclusion:**

A compact cell can reduce its footprint while blocking pins, power rails or neighboring access. Device sharing, row alignment and contact placement affect both area and the routes that can leave the cell boundary.

Boolean connectivity is not physical legality. Complementary-FET diffusion, gate, contact, well/isolation, spacing, enclosure and layer rules must be checked; an area or open-pin proxy does not establish a design-rule-clean, extracted cell.

A cell that routes in isolation may not integrate when abutted, characterized or instantiated repeatedly. The official description reports no area definition, pin-access, routing, timing, yield or process result. The record supports multi-row area/routability-driven synthesis, not demonstrated signoff-ready library quality or universal superiority over single-row and area-only methods.

**Source and location**

Evidence tier: Primary captured official DAC description plus existing chapter level multi row complementary fet discussion; no full paper extraction, library characterization or chip level routing validation. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH2416)

DAC 2026 official description; captured Problem, Mechanism / artifact, Workload, Hardware, Baseline, Measurements and Limits fields; record RESEARCH2416; no manuscript pages.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** single-row standard-cell synthesis

area-only layout synthesis

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH2416

**Hardware or process assumptions:** Complementary-FET standard-cell process with multi-row placement; rules and extraction assumptions are unspecified.

**Limits:** No area, pin access, routing, timing, yield, or process results are reported.

Area-optimal solutions may be difficult to integrate into libraries.

Official description only; signoff and fabrication-aware checks are required.

**Method or artifact:** Area-optimal, routability-driven standard-cell layout synthesis.

**Metrics:** Area and routability are claimed qualitatively

**Problem:** Multi-row complementary-FET cells need compact layouts that remain routable and manufacturable.

**Workload or benchmark:** Multi-row complementary-FET standard cells; device rules, libraries, and baselines are unspecified.

</details>

<span id="paper-dac-2026-research373"></span>

### LATTE: Legality-Assured Differentiable Timing-Driven Detailed Placement

DAC 2026 · Record: `dac-2026-research373`

[Read the step-by-step explanation](#explanation-dac-2026-research373)

**Updated source-backed reading card**

Reviewed 2026-09-08. Deepens the existing LATTE detailed-placement treatment into a paper-level reading; defines timing-driven local movement, differentiable proxy objectives, legality invariants, legalization displacement and the distinction between placement timing and final routed STA.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Detailed placement optimization must improve timing without producing illegal overlaps or density violations.

**Mechanism / artifact:**

Legality-assured differentiable timing-driven detailed placement; differentiable variables, timing/RC model, legality invariant, repair mechanism and routing/signoff flow are unspecified.

**Workload — the work tested:**

ASIC detailed-placement benchmarks; standard-cell rows, libraries, density, blockages, timing constraints, legalization, routing and baseline details are unspecified.

**Hardware and manufacturing assumptions:**

Standard-cell placement with timing and design-rule constraints; technology node, cell sites, orientations, RC extraction, timing corners and signoff flow are unspecified.

**Baseline — the comparison method:**

Analytic detailed placement

Timing-oblivious differentiable placement

Netlists, libraries, timing engine, seeds, compute budget, routing, extraction and signoff conditions are unspecified

**Reported measurements:**

Timing and legality are claimed qualitatively; no worst or total negative slack, wirelength, density, overlap, illegal-site, legalization-displacement, runtime, memory or signoff result is reported.

**Limits on the conclusion:**

Differentiable coordinates and smooth density or timing penalties are proxies for discrete row sites, legal orientations, blockages and overlaps. A low smooth objective can still be illegal or require substantial movement during legalization.

A legality penalty is not automatically a guarantee. The invariant, enforcement mechanism and check point must be specified; timing measured before legalization can differ from timing after legal placement, routing and extraction.

The official description reports no slack, wirelength, density, legality, runtime or signoff result. The record supports a legality-aware differentiable detailed-placement direction, not demonstrated final timing closure or universal superiority over analytic and timing-oblivious placement.

**Source and location**

Evidence tier: Primary captured official DAC description plus existing chapter level differentiable placement discussion; no full paper extraction, routed timing validation or reproducible signoff comparison. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH373)

DAC 2026 official description; captured Problem, Mechanism / artifact, Workload, Hardware, Baseline, Measurements and Limits fields; record RESEARCH373; no manuscript pages.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** analytic detailed placement

timing-oblivious differentiable placement

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH373

**Hardware or process assumptions:** Standard-cell placement with timing and design-rule constraints; node and signoff flow are unspecified.

**Limits:** No slack, wirelength, density, legality, runtime, or signoff results are reported.

Differentiable relaxations may miss discrete legal constraints.

Official description only; full-flow placement validation is required.

**Method or artifact:** Legality-assured differentiable timing-driven detailed placement.

**Metrics:** Timing and legality are claimed qualitatively

**Problem:** Detailed placement optimization must improve timing without producing illegal overlaps or density violations.

**Workload or benchmark:** ASIC detailed-placement benchmarks; cells, timing model, legalization, and baselines are unspecified.

</details>

<span id="paper-dac-2026-research843"></span>

### Disentangled Differentiable Timing-Power Co-Optimization with Quad-Gradient Gate Sizing

DAC 2026 · Record: `dac-2026-research843`

[Read the step-by-step explanation](#explanation-dac-2026-research843)

**Updated source-backed reading card**

Reviewed 2026-09-08. Deepens the existing differentiable timing-power gate-sizing treatment into a paper-level reading; defines discrete library choices, drive strength/load coupling, timing and power gradients, relaxation-to-cell mapping, extraction and signoff limits, and does not infer the meaning of quad-gradient beyond the captured source.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Gate sizing must improve timing and power simultaneously despite discrete cell choices and nonlinear interactions.

**Mechanism / artifact:**

Differentiable timing-power co-optimization with quad-gradient gate sizing; the four gradients, continuous representation, objective combination, discrete mapping and repair policy are unspecified.

**Workload — the work tested:**

ASIC gate-sizing instances; standard-cell libraries, netlists, activity, timing constraints, corners, routing, extraction and baseline details are unspecified.

**Hardware and manufacturing assumptions:**

Standard-cell ASIC flow with timing and power models; technology node, cell variants, voltage/frequency, parasitics, activity, corners and signoff assumptions are unspecified.

**Baseline — the comparison method:**

Heuristic gate sizing

Single-objective differentiable sizing

Libraries, netlists, timing/power models, constraints, seeds, compute budget, routing and signoff conditions are unspecified

**Reported measurements:**

Timing-power tradeoff is claimed qualitatively; no slack, setup/hold violation, power split, area, slew, convergence, runtime, discrete-rounding loss or signoff result is reported.

**Limits on the conclusion:**

Gate-size choices are discrete library cells. A continuous strength, mixture or surrogate can produce a good relaxed point whose rounded cell has different input capacitance, slew, leakage, dynamic power and path delay.

Sizing is coupled across a path: a stronger cell can improve its output transition while increasing the upstream load, changing another path's criticality or violating power and area limits. Timing and power gradients must state models, units, normalization and objective constraints.

The captured description does not define the four gradients, and reports no slack, power, area, convergence, runtime or signoff result. Continuous gradients may misrepresent discrete library behavior. The record supports a differentiable timing-power sizing direction, not demonstrated signoff improvement or universal superiority over heuristic and single-objective sizing.

**Source and location**

Evidence tier: Primary captured official DAC description plus existing chapter level timing power sizing discussion; no full paper extraction, discrete mapping validation or reproducible signoff comparison. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH843)

DAC 2026 official description; captured Problem, Mechanism / artifact, Workload, Hardware, Baseline, Measurements and Limits fields; record RESEARCH843; no manuscript pages.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** heuristic gate sizing

single-objective differentiable sizing

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH843

**Hardware or process assumptions:** Standard-cell ASIC flow with timing/power models; node and signoff assumptions are unspecified.

**Limits:** No slack, power, area, convergence, runtime, or signoff results are reported.

Continuous gradients may misrepresent discrete library behavior.

Official description only; full-flow validation is required.

**Method or artifact:** Differentiable timing-power co-optimization with quad-gradient gate sizing.

**Metrics:** Timing-power tradeoff is claimed qualitatively

**Problem:** Gate sizing must improve timing and power simultaneously despite discrete cell choices and nonlinear interactions.

**Workload or benchmark:** ASIC gate-sizing instances; libraries, timing, power, and baselines are unspecified.

</details>

<span id="paper-dac-2026-research320"></span>

### SAAP: An Efficient Spatial-Aware Analytic Partitioning Algorithm of VLSI Netlists for Parallel Routing

DAC 2026 · Record: `dac-2026-research320`

[Read the step-by-step explanation](#explanation-dac-2026-research320)

**Updated source-backed reading card**

Reviewed 2026-09-08. Deepens the existing SAAP partitioning treatment into a paper-level reading; defines graph/hypergraph partitioning, spatial locality, cut nets, work balance, boundary coordination and the distinction between partition quality and end-to-end parallel routing.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Parallel routing needs partitions that preserve locality while balancing work and cut nets.

**Mechanism / artifact:**

Spatial-aware analytic VLSI netlist partitioning for parallel routing; graph or hypergraph representation, spatial features, balance objective, cut cost, boundary protocol and router are unspecified.

**Workload — the work tested:**

VLSI netlists and routing tasks; netlists, geometry, congestion, partition counts, routers, worker counts, hardware, baselines and benchmark scale are unspecified.

**Hardware and manufacturing assumptions:**

Parallel routing infrastructure with spatial netlist representation; technology, routing layers, shared-resource protocol, synchronization and design-rule assumptions are unspecified.

**Baseline — the comparison method:**

Graph partitioning without spatial awareness

Serial routing

Netlists, technology, routing rules, worker count, hardware, termination and final verification conditions are unspecified

**Reported measurements:**

Routing scalability and partition quality are claimed qualitatively; no cut size, imbalance, boundary crossing, congestion, routing success, runtime, speedup, communication, memory or scale result is reported.

**Limits on the conclusion:**

Cut size is not the same as routing difficulty. A long, high-fanout or timing-critical cut net can create more boundary work than several short nets, and balanced cell counts may leave one worker with the hardest congestion.

Spatial partitions remain coupled at boundaries. Local routers can compete for tracks, vias and entry points or create boundary congestion; partition quality must be measured with the actual router and coordination protocol.

The official description reports no cut size, congestion, routing success, runtime or scale result. The record supports a spatial-aware analytic partitioning direction, not demonstrated end-to-end parallel speedup, routing completion or signoff-routing superiority.

**Source and location**

Evidence tier: Primary captured official DAC description plus existing chapter level parallel routing partitioning discussion; no full paper extraction, end to end routing validation or reproducible scale comparison. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH320)

DAC 2026 official description; captured Problem, Mechanism / artifact, Workload, Hardware, Baseline, Measurements and Limits fields; record RESEARCH320; no manuscript pages.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** graph partitioning without spatial awareness

serial routing

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH320

**Hardware or process assumptions:** Parallel routing infrastructure with spatial netlist representation; technology and routing assumptions are unspecified.

**Limits:** No cut size, congestion, routing success, runtime, or scale results are reported.

Partitions may create boundary congestion.

Official description only; signoff-routing validation is required.

**Method or artifact:** Spatial-aware analytic VLSI netlist partitioning for parallel routing.

**Metrics:** Routing scalability and partition quality are claimed qualitatively

**Problem:** Parallel routing needs partitions that preserve locality while balancing work and cut nets.

**Workload or benchmark:** VLSI netlists and routing tasks; partition constraints, routers, and baselines are unspecified.

</details>

<span id="paper-dac-2026-research335"></span>

### BSPDN-Elite: A Comprehensive Framework for Optimizing Timing, Power and Routing Resources in BSPDN Designs

DAC 2026 · Record: `dac-2026-research335`

[Read the step-by-step explanation](#explanation-dac-2026-research335)

**Updated source-backed reading card**

Reviewed 2026-09-08. Deepens the existing BSPDN-Elite treatment into a paper-level reading; defines backside power delivery, IR drop, current-density and timing coupling, signal-routing tradeoffs, process-stack assumptions and final integrity-validation requirements.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Backside power delivery creates coupled timing, power, routing and manufacturability constraints.

**Mechanism / artifact:**

Comprehensive multi-objective BSPDN design framework; backside stack, connection structures, power model, IR-drop analysis, timing coupling, thermal model, objective constraints and process validation are unspecified.

**Workload — the work tested:**

BSPDN physical-design cases; netlists, placement, load activity, power network, current distribution, process stack, routing, baselines and benchmark details are unspecified.

**Hardware and manufacturing assumptions:**

Backside power distribution and advanced-node ASIC flow; backside metals, vias or contacts, resistance, IR drop, electromigration, thermal, alignment, yield and timing assumptions are unspecified.

**Baseline — the comparison method:**

Frontside power delivery

Single-objective BSPDN optimization

Netlists, activity, voltage/frequency, placement, routing, extraction, thermal, compute budget and process conditions are unspecified

**Reported measurements:**

Timing-power-routing quality is claimed qualitatively; no IR drop, current density, timing slack, power, congestion, thermal, yield, runtime, area or integrity result is reported.

**Limits on the conclusion:**

Moving power resources to the backside can free signal-routing space but introduces process-specific connections, resistance, alignment, thermal and yield constraints. An abstract backside edge is not automatically a manufacturable connection.

IR drop changes cell voltage and timing; timing repair changes current and power demand, while routing and placement changes alter both signal congestion and the power network. Separate or uncalibrated objective scores do not establish a valid coupled solution.

The official description reports no IR drop, timing, power, congestion, thermal, yield or runtime result. Backside process assumptions may not transfer across nodes. The record supports a multi-objective BSPDN design direction, not demonstrated signoff integrity, process portability or universal superiority.

**Source and location**

Evidence tier: Primary captured official DAC description plus existing chapter level bspdn discussion; no full paper extraction, power integrity validation or cross process comparison. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH335)

DAC 2026 official description; captured Problem, Mechanism / artifact, Workload, Hardware, Baseline, Measurements and Limits fields; record RESEARCH335; no manuscript pages.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** frontside power delivery

single-objective BSPDN optimization

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH335

**Hardware or process assumptions:** Backside power distribution and advanced-node ASIC flow; via, IR-drop, and thermal assumptions are unspecified.

**Limits:** No IR drop, timing, power, congestion, thermal, yield, or runtime results are reported.

Backside process assumptions may not transfer across nodes.

Official description only; signoff and process validation are required.

**Method or artifact:** Comprehensive multi-objective BSPDN design framework.

**Metrics:** Timing-power-routing quality is claimed qualitatively

**Problem:** Backside power delivery creates coupled timing, power, routing, and manufacturability constraints.

**Workload or benchmark:** BSPDN physical-design cases; process, power network, and baselines are unspecified.

</details>

## What remains to establish

Resolve unspecified workloads, comparison methods, resource budgets, and source locations before generalizing a reported gain. Multiple papers in this selected sample permit comparison of mechanisms, but do not by themselves establish recurrence across years or a long-term trend.

[All subthemes](../expanded-taxonomy-v1.md) · [Research directions](../directions/README.md)
