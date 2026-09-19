## A large compute surface still has local limits

Wafer-scale computing connects computation across a much larger silicon surface than a conventional individual die. That increases the resources available to a workload, but does not make every resource equally close to every other resource. Each connection still has a finite transfer rate, and each compute region still has finite storage and arithmetic capacity.

The two papers here ask different questions. HyperWafer asks how sparse matrix multiplication should distribute work and communication. WSC-Cost asks how manufacturing and assembly should enter a cost model. A fast mapping does not establish low manufacturing cost; a plausible cost estimate does not establish useful application throughput.

## Sparse multiplication: missing entries reduce arithmetic, not every other cost

A sparse matrix has many zero entries. A sparse representation stores selected nonzero values and their positions instead of explicitly storing every zero. For matrix multiplication, an output entry is a sum of products: C(i,j) = sum over k of A(i,k) × B(k,j). Products involving zero can often be omitted, but the implementation must still locate matching positions and combine contributions to the same output.

This creates several distinct costs. Input positions must be read. Shared data may need to reach multiple compute regions. Intermediate products must be accumulated without losing contributions. Different regions may receive very different amounts of work. Even matrices with identical dimensions and nonzero counts can produce different communication patterns because the positions of their nonzeros differ.

Balancing the count of stored input entries is therefore not necessarily sufficient to balance multiplication work. Nor does minimizing total transferred bytes necessarily minimize execution time: many transfers can compete for the same narrow set of links while other links remain idle.

<span id="explanation-dac-2026-research2132"></span>

## HyperWafer: make shared dependencies part of the mapping

[HyperWafer](../observed-subthemes/wafer-scale-and-heterogeneous-integration.md#paper-dac-2026-research2132) uses a weighted hypergraph to represent multiway row sharing and overlapping accumulation dependencies. Its official description combines communication-centered partitioning and topology-aware placement with a sparse execution engine and congestion-sensitive runtime routing. The description reports average speedups of 979.97×, 125.23×, 12.14×, and 5.14× against CPU, GPU, FPGA, and wafer-scale implementations, respectively. It does not identify the baseline configurations, matrices, resource matching, precision, preprocessing boundary, or implementation method. These are four separate comparisons, not a universal speedup range. [Official HyperWafer description](https://63dac.conference-program.com/presentation/?id=RESEARCH2132&sess=sess169).

A hypergraph can connect several objects through one shared relationship. For example, when one input row is required by several compute regions, representing that shared requirement directly can distinguish one reusable transfer from several independent transfers. The representation alone does not prove that a runtime can realize the predicted reuse: storage capacity, arrival order, and routing rules still matter.

Topology-aware mapping means using the actual arrangement and capacities of connections when assigning work. Congestion-sensitive routing adjusts communication in response to competition for links. Those choices can interact. Changing a route might avoid a busy link while increasing distance or upsetting a reuse plan. The complete evaluation should measure both computation and the communication required to keep it supplied.

For repeated use of one matrix structure, preprocessing can be paid once and reused. For changing structures, repeated partitioning or mapping may become significant. Report both cases rather than silently excluding setup from an application-level speed claim. Correctness should also specify numerical precision and accumulation order, since changing the order of finite-precision sums can change the result.

The first gate is SpGEMM correctness. Define sparse formats, duplicate products, reduction order, accumulation precision, zero handling and output ordering, then compare values and residuals with a trusted reference. A communication-aware schedule is not valid if a shared contribution is dropped, duplicated or combined under a different numerical contract. Report deterministic versus nondeterministic reductions and their effect on downstream results.

The second gate is wafer traffic and resource balance. Measure hypergraph construction, partitioning, mapping, messages and bytes, shared-row/column reuse, hops, link utilization, queueing, buffer occupancy, reduction traffic, PE work, routing overhead and p50/p95/p99 time. Include preprocessing, compilation, runtime setup, remapping and failures. A wafer has high aggregate bandwidth but still has local bottlenecks; avoiding one link can create a longer path or overload another reduction resource.

The official description reports average speedups of 979.97× over CPU, 125.23× over GPU, 12.14× over FPGA and 5.14× over a wafer-scale SpGEMM implementation. These are separate comparisons. The source does not expose absolute throughput, communication volume, utilization, energy, area, memory, numerical error, congestion, scaling, topology, fault handling or per-workload results. Hold out matrix patterns and test wafer size, topology, link failures, defective PEs, thermal/power limits and changing sparsity before treating the result as a general wafer-scale benefit.

The evidence supports communication-aware wafer-scale SpGEMM, not demonstrated numerical equivalence, universal speedup, fault-tolerant scale-out or complete wafer-system benefit.

<span id="explanation-dac-2026-research2230"></span>

## WSC-Cost: identify what is being paid for

A cost estimate requires a boundary. Fabricating the compute surface, connecting it to memory, testing it, and assembling a working unit are different activities. An estimate that includes only silicon area cannot establish the cost of a complete usable system. Conversely, a manufacturing estimate should not be presented as a lifetime operating-cost estimate without adding its missing terms.

[WSC-Cost](../observed-subthemes/wafer-scale-and-heterogeneous-integration.md#paper-dac-2026-research2230) separates lateral mask-stitching costs across metal layers from interposer fabrication and assembly costs. Its official description states validation using public cost data and an in-house wafer-scale prototype. It supplies no prediction errors, calibration split, process details, production volume, yield assumptions, or prototype measurements. The validation claim is therefore recorded but cannot yet be independently assessed. [Official WSC-Cost description](https://63dac.conference-program.com/presentation/?id=RESEARCH2230&sess=sess113).

Mask stitching concerns joining patterned regions across exposure-field boundaries. An interposer provides connections between components. Including these terms makes the cost boundary more explicit, but accuracy still depends on how the model calculates them and where its inputs came from.

Yield is the fraction of manufactured units meeting a stated acceptance criterion. For a large system, that criterion must specify whether defective regions can be disabled and how much remaining capacity is acceptable. A partially functioning device is not automatically either a complete loss or a fully equivalent product. The model should connect its acceptance rule to the performance of the delivered system.

Fixed design and manufacturing preparation costs also need an assumed production volume. If a fixed cost F is spread across N usable units, its contribution is F/N per unit. Changing N changes the estimate even if the physical design stays identical. This arithmetic is a boundary check, not the recovered paper's undisclosed cost formula.

WSC-Cost's first gate is boundary completeness. Separate mask creation and stitching across metal layers, wafer fabrication, defect screening, repair or disabled regions, interposer, bonding/assembly, packaging, test, known-good yield and scrap. A horizontal mask-stitching term plus a vertical interposer/assembly term makes the model more structured, but does not by itself establish total delivered-system cost or operating cost.

The second gate is yield calibration. State defect density and spatial correlation, wafer area, redundancy, repair policy, acceptable disabled capacity and the wafer/unit acceptance rule. Compare predicted usable-wafer yield and cost with independent production data or a documented calibrated public source. An in-house wafer-scale prototype can validate that a design exists; it does not prove the economic model across processes, volumes or foundries.

Economic inputs are time- and volume-dependent. Report sensitivity to wafer price, mask/metal count, interposer and assembly, yield, test, volume, currency/year and amortization, then couple cost to usable throughput, bandwidth, power, thermal limits and workload capacity. The official description claims unified cost modeling, open-data/prototype validation and cost-driven co-optimization, but reports no prediction error, absolute cost, sensitivity, yield, process/volume scenario or prototype measurement details. The evidence supports a two-dimensional wafer-scale cost-modeling direction, not demonstrated accurate delivered cost, process-independent economics or a cost advantage over matched alternatives.

## Connecting performance and cost without combining incompatible claims

A useful joint question is the cost of completing a specified workload at a required speed and correctness level. That requires the same architecture, available compute regions, memory, and connection assumptions in both performance and cost evaluations. More connections might improve sparse communication while increasing manufacturing complexity. Redundant resources might improve acceptance yield while changing usable throughput.

These are dependencies to investigate, not findings that HyperWafer and WSC-Cost were evaluated together. Their current descriptions do not establish an optimal wafer-scale design, a cost advantage over matched conventional systems, or a long-term adoption trend across conferences.

## Evidence status

Official descriptions were refreshed on 2026-09-07 and supersede the historical cards' missing-result statements where cited above. Neither full manuscript was recovered in this pass, so paper-page locations, detailed conditions, and independent reproduction remain missing. These gaps cannot be filled with numbers from related wafer-scale papers, whose architectures and accounting boundaries may differ.
