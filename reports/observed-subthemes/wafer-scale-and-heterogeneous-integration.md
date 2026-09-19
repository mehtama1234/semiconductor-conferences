# Wafer scale and heterogeneous integration

This subject has 2 records in the selected sample. This page explains where it fits, then presents all captured paper evidence without shortening the measurements or limitations.

[Definitions used in the paper records](../reading-guide-v1.md)

## Understand the parent subject first

- [Chiplets 3d and packaging](../themes/chiplets-3d-and-packaging.md)

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

## Compare the results carefully

First identify the inputs and required output quality. Then identify the limited resource: time, memory, communication, energy, circuit area, or correctness coverage. Ask which part of the method reduces that cost and which new cost it adds. Compare numbers only when the experiments hold these conditions sufficiently similar.

A conference description may explain the proposal while omitting the full experiment. An author preprint link may have been coded from its abstract. The source classification does not by itself establish that every table was read. Missing locations remain visible below.

## Complete captured evidence

These are evidence records, not substitutes for the explanations above. Each record preserves its problem, proposed method, measurements, comparison conditions, and source limits. A populated record does not establish that its mechanism has been fully explained or independently verified.

<span id="paper-dac-2026-research2132"></span>

### Hyperwafer: Communication-Aware Sparse Matrix Multiplication on Wafer-Scale Chips

DAC 2026 · Record: `dac-2026-research2132`

[Read the step-by-step explanation](#explanation-dac-2026-research2132)

**Updated source-backed reading card**

Reviewed 2026-09-09. Deepens the HyperWafer treatment into a paper-level reading; separates weighted-hypergraph dependency modeling, communication-centric partitioning, topology-aware mapping, sparse execution and congestion-sensitive routing from SpGEMM numerical correctness, matrix/sparsity transfer, congestion/traffic accounting, wafer faults and end-to-end system cost, while preserving the four source-reported speedups.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Sparse matrix-matrix multiplication has irregular sharing, accumulation and data movement; on a wafer-scale chip, communication contention can leave processing elements underutilized even when aggregate bandwidth is high.

**Mechanism / artifact:**

HyperWafer uses a weighted hypergraph for multiway row sharing and overlapping reduction scopes, communication-centric partitioning and topology-aware mapping aligned with wafer bandwidth, plus a sparsity-aware SpGEMM engine and lightweight congestion-sensitive runtime routing; partition objective, mapping granularity, reduction protocol, topology, buffers, routing policy and fault handling are unspecified.

**Workload — the work tested:**

Sparse matrix-matrix multiplication across diverse workloads and CPU, GPU, FPGA and wafer-scale comparisons; matrix dimensions/nonzeros/patterns, output density, format, sparsity distribution, precision, batch/reuse, PE count, wafer topology, traffic traces and preprocessing boundary are unspecified.

**Hardware and manufacturing assumptions:**

Wafer-scale chip with many processing elements, high-bandwidth on-wafer links, sparse execution support and congestion-sensitive routing; wafer size/process, PE/memory capacity, link bandwidth/latency, topology, packaging, thermal/power, defect/fault model and simulator or hardware status are unspecified.

**Baseline — the comparison method:**

CPU SpGEMM implementation

GPU SpGEMM implementation

FPGA SpGEMM implementation

Existing wafer-scale SpGEMM implementation

Same matrices, precision, output semantics, PE count, memory, topology, compiler/runtime, preprocessing, fault assumptions and end-to-end timing/energy boundary are unspecified

**Reported measurements:**

The official description reports average speedups of 979.97x over CPU, 125.23x over GPU, 12.14x over FPGA and 5.14x over a wafer-scale SpGEMM implementation; it reports no absolute throughput, communication volume, utilization, energy, area, memory, numerical error, congestion, scaling, fault tolerance or per-workload result.

**Limits on the conclusion:**

Hypergraph mapping must preserve SpGEMM semantics. Define sparse formats, duplicate products, reduction order, accumulation precision, zeros, output ordering and deterministic/nondeterministic behavior, then compare output values and residuals with a trusted reference. Reducing communication is not useful if contributions are dropped, duplicated or numerically changed.

A communication-aware partition must be evaluated with actual traffic and resource contention. Report shared-row/column reuse, messages/bytes, hops, link utilization, queueing, buffer occupancy, PE work, reduction traffic, routing overhead and p50/p95/p99 execution time by matrix pattern. Include hypergraph construction, partitioning, mapping, compilation, runtime setup and remapping; a 5.14x comparison with another wafer design needs matched topology and resource boundary.

Test matrices with different dimensions, nonzero distributions, output density, reuse and adversarial skew, plus wafer sizes, topologies, link failures, defective PEs, thermal/power limits and changing sparsity. Compare CPU/GPU/FPGA/wafer baselines with matched precision, memory and tuning. The evidence supports communication-aware wafer-scale SpGEMM, not demonstrated numerical equivalence, universal speedup, fault-tolerant scale-out or complete wafer-system benefit.

**Source and location**

Evidence tier: Primary captured official DAC description plus existing authored wafer scale discussion; no full paper extraction, reproduced spgemm outputs, communication trace, scale out/fault validation or measured wafer hardware. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH2132&sess=sess169)

DAC 2026 official description; existing wafer-scale-and-heterogeneous-integration chapter framing; captured Problem, Mechanism / artifact, Workload, Hardware, Baseline, Measurements and Limits fields; no manuscript pages, matrix/traffic table, topology specification, numerical validation or fault/thermal study.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** communication-oblivious sparse mapping

GPU sparse multiplication

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH2132

**Hardware or process assumptions:** Wafer-scale chip with high-bandwidth interconnect; process, memory, and fault assumptions are unspecified.

**Limits:** No throughput, communication volume, utilization, energy, area, or fault results are reported.

Benefits depend on wafer topology and matrix sparsity.

Official description only; scale-out validation is required.

**Method or artifact:** Communication-aware sparse matrix-multiplication mapping or architecture.

**Metrics:** Wafer-scale efficiency is claimed qualitatively

**Problem:** Wafer-scale sparse multiplication is limited by communication and irregular load balance across many compute tiles.

**Workload or benchmark:** Sparse matrix multiplication; matrices, wafer topology, and comparison systems are unspecified.

</details>

<span id="paper-dac-2026-research2230"></span>

### WSC-Cost: An Accurate Cost Modeling Framework for Wafer-Scale Chips

DAC 2026 · Record: `dac-2026-research2230`

[Read the step-by-step explanation](#explanation-dac-2026-research2230)

**Updated source-backed reading card**

Reviewed 2026-09-09. Deepens the WSC-Cost treatment into a paper-level reading; separates horizontal mask-stitching and vertical interposer/assembly cost dimensions from yield, defect/repair assumptions, volume, process/foundry time dependence, model calibration and workload-level wafer economics, while preserving the open-data/in-house-prototype validation claim without treating it as independently reproduced.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Wafer-scale chips combine large-area silicon, multi-layer mask stitching, interposer or package assembly and yield exposure, so area-only cost estimates can mislead architecture and manufacturing decisions.

**Mechanism / artifact:**

WSC-Cost is described as a unified model with a horizontal dimension for mask-stitching cost across multiple metal layers and a vertical dimension for interposer fabrication and assembly; cost equations, defect/yield model, repair/disable policy, production volume, process assumptions, calibration split and cost boundary are unspecified.

**Workload — the work tested:**

Wafer-scale chip architectures and manufacturing scenarios, with cost-driven co-optimization of wafer-scale designs; wafer area/layout, metal layers, stitching fields, interposer/package choices, production volume, wafer yield, redundant regions, performance target, workload and comparison architectures are unspecified.

**Hardware and manufacturing assumptions:**

Wafer-scale silicon with multi-layer mask stitching and interposer/assembly integration; process node, mask field/stepper, metal stack, defect density, wafer size, assembly technology, test/repair, packaging, foundry pricing, labor, equipment depreciation and operating-cost assumptions are unspecified.

**Baseline — the comparison method:**

Simple area-based cost model

Conventional chip cost estimation

Separate mask-only or package-only estimates

Same wafer area, process, mask layers, stitching rules, interposer/assembly, volume, yield/repair policy, currency/time basis and complete manufacturing-cost boundary are unspecified

**Reported measurements:**

The official description claims unified end-to-end wafer-scale cost modeling, validation with open-source cost data and an in-house WSC prototype, and cost-driven co-optimization insights; it reports no prediction error, absolute cost, sensitivity, yield, process/volume scenario, prototype measurement or design-case result.

**Limits on the conclusion:**

Define the cost boundary before comparing architectures: mask creation/stitching, wafer fabrication, defect screening, repair/disable, interposer, bonding/assembly, packaging, test, known-good yield and unusable scrap must be separated. A horizontal mask term and vertical assembly term do not by themselves establish total delivered-system cost or operating cost.

Yield is a distribution, not a fixed multiplier. State defect density, spatial correlation, wafer area, redundancy, repair policy, acceptable disabled capacity and die/wafer acceptance rule; validate predicted usable-wafer yield and cost against independent production or calibrated public data. An in-house prototype can demonstrate plausibility without proving the economic model across processes or volumes.

Economic inputs are time-, foundry- and volume-dependent. Report sensitivity to wafer price, mask/metal count, interposer/assembly, yield, test, volume, currency/year and amortization, and couple cost to usable throughput, bandwidth, power, thermal limits and workload capacity. The evidence supports a two-dimensional wafer-scale cost-modeling direction, not demonstrated accurate delivered cost, process-independent economics or a cost advantage over matched alternatives.

**Source and location**

Evidence tier: Primary captured official DAC description plus existing authored wafer scale cost discussion; no full paper extraction, independent cost reproduction, process/volume sensitivity study or delivered system economic validation. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH2230&sess=sess113)

DAC 2026 official description; existing wafer-scale-and-heterogeneous-integration chapter framing; captured Problem, Mechanism / artifact, Workload, Hardware, Baseline, Measurements and Limits fields; no manuscript pages, cost table, yield model, calibration split or prototype measurement details.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** simple area-based cost model

conventional chip cost estimation

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH2230

**Hardware or process assumptions:** Wafer-scale manufacturing and packaging; defect, yield, and economics assumptions are unspecified.

**Limits:** No cost error, yield, sensitivity, process, or design-case results are reported.

Economic assumptions are especially time- and foundry-dependent.

Official description only; calibrated manufacturing validation is required.

**Method or artifact:** Cost modeling framework for wafer-scale chip designs.

**Metrics:** Cost-model accuracy is claimed qualitatively

**Problem:** Wafer-scale chips require cost models that account for yield, area, packaging, and manufacturing complexity.

**Workload or benchmark:** Wafer-scale architectures and manufacturing scenarios; process, yield, and calibration sources are unspecified.

</details>

## What remains to establish

Resolve unspecified workloads, comparison methods, resource budgets, and source locations before generalizing a reported gain. Multiple papers in this selected sample permit comparison of mechanisms, but do not by themselves establish recurrence across years or a long-term trend.

[All subthemes](../expanded-taxonomy-v1.md) · [Research directions](../directions/README.md)
