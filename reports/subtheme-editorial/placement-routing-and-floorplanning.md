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
