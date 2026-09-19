# Chiplet interconnects

This subject has 2 records in the selected sample. This page explains where it fits, then presents all captured paper evidence without shortening the measurements or limitations.

[Definitions used in the paper records](../reading-guide-v1.md)

## Understand the parent subject first

- [Chiplets 3d and packaging](../themes/chiplets-3d-and-packaging.md)

## Communication has both a data volume and a physical path

Dividing computation across chips or regions creates transfers between them. The time for a transfer includes producing the data, preparing it for the link, waiting for access, crossing the network, and making it usable at the destination. Link bandwidth describes a transfer capacity; application latency also depends on dependencies and competition for that capacity.

The two records here attack different parts of this problem. LEXI changes the representation of transferred values. The wafer-scale network paper changes the communication structure enabled by bonded wafers. They should not be treated as competing solutions to an identical problem, nor assumed to have been combined.

## LEXI: reduce transmitted bits without changing the values

[LEXI](../observed-subthemes/chiplet-interconnects.md#paper-dac-2026-research3121) proposes lossless exponent coding for inter-chiplet communication in hybrid language models. In a floating-point representation, the exponent contributes to the numerical scale of a value. Repeated or otherwise predictable exponent information may admit a shorter representation. Whether it does depends on the actual values and format.

Lossless coding means the supported input representation can be recovered exactly. That differs from lowering numerical precision, which can alter values. The captured description does not specify the formats, coding rule, handling of exceptional values, or traffic distributions. It therefore does not establish exact coverage of all bit patterns or a particular compression ratio.

The complete path includes encoding, metadata, transmission, and decoding. Fewer transmitted bits help only when the saved communication cost outweighs the added work or when that work can overlap usefully with other execution. A small transfer may be dominated by fixed preparation costs, while a large transfer may be limited by sustained encoder or decoder throughput.

Evaluation should report the distribution of compressed sizes, not just an average over favorable transfers. Poorly compressible data needs defined behavior, potentially including a fallback representation; the source does not describe one. Area, buffering, energy, and latency of the codec also belong in the result. None of those numerical measurements is supplied in the captured record.

<span id="explanation-dac-2026-research3121"></span>

### LEXI: lossless exponent coding reduces traffic only when exact reconstruction and codec cost are measured

#### What exponent coding changes

A floating-point value contains a sign, a significand or mantissa, and an exponent that sets the numerical scale. A tensor transfer sends representations of many values between chiplets. If exponent values repeat or follow a predictable pattern, an encoder may represent them with fewer bits and send metadata that lets the decoder reconstruct the original representation.

Lossless means that the decoder recovers the same supported representation. It is not the same as lowering precision, rounding values or changing the model's numerical behavior. The method must define the formats it accepts, the exponent alphabet or coding rule, block boundaries, metadata, and how it handles zero, subnormal values, infinities, NaNs, sign and overflow.

#### Why compression ratio is workload-dependent

Exponent distributions differ across layers, tensors, models, precision modes and execution phases. A block with repeated exponents may shrink; a block with varied exponents may need nearly the original representation or an escape path. An average compression ratio can hide transfers that expand after headers or are poorly compressible.

The evaluation should report the distribution of encoded sizes by tensor and traffic phase, the fraction using a fallback representation, and exact reconstruction tests for every supported format. A ratio measured only on favorable tensors does not establish link-level benefit for a complete LLM run.

#### The codec is part of the communication path

The end-to-end path includes reading the tensor, extracting or grouping exponents, encoding, adding metadata, buffering, waiting for link access, transmitting, decoding and reconstructing the values. The saved link time must exceed the encoder and decoder work and must not create a new queue or memory bottleneck. If encoding runs on a shared processor, its contention also belongs in the measurement.

The comparison must hold the tensor values, numerical format, chiplet topology, link width, clock, traffic schedule and target-model quality fixed. Report codec throughput, latency, metadata bytes, link utilization, queueing, energy, area and any overlap with computation. Lower bytes do not establish lower application latency if the link was not the bottleneck.

The captured DAC description supports lossless exponent coding for inter-chiplet communication in hybrid LLMs. It reports no compression-ratio distribution, link latency, codec throughput, energy, area, traffic trace, fallback behavior or model-accuracy result. The evidence supports a representation-aware communication direction, not demonstrated inter-chiplet or end-to-end LLM improvement.

[Observed paper card](../observed-subthemes/chiplet-interconnects.md#paper-dac-2026-research3121)

## Bonded wafers: network structure and physical feasibility

The [wafer-scale hybrid-bonding network paper](../observed-subthemes/chiplet-interconnects.md#paper-dac-2026-research363) addresses communication across a system with wafer-on-wafer connections. The relevant design choices include which regions connect, where traffic crosses between wafers, and which routes carry long-distance transfers. The source does not expose the actual topology or routing policy.

Adding connection opportunities does not automatically improve every workload. Traffic concentrated on a few destinations can still overload shared links. A topology with fewer logical steps may use physically longer or more expensive connections. A useful evaluation must connect the network model to feasible link capacity, latency, bonding locations, and power.

Fault assumptions matter because a network must remain useful under the failures it claims to tolerate. A disconnected region, damaged link, or reduced-capacity route changes available paths. The captured description gives no fault model, bandwidth, latency, power, thermal, or yield results. It therefore supports identifying a network-design proposal, not measured wafer-scale communication performance.

<span id="explanation-dac-2026-research363"></span>

### Wafer-on-wafer network design: a short logical path must also be a feasible, powered and fault-aware physical path

#### What a wafer-scale network must provide

A wafer-scale system places many compute or memory regions across a large physical surface. A network gives those regions paths for transferring data. Its useful behavior depends on the traffic: which regions communicate, how much data they send, whether transfers are bursts or steady streams, and whether several flows share a link.

A graph can show that two endpoints are connected by a small number of hops. That does not determine application latency. Each hop has serialization, propagation, buffering, arbitration and possible contention cost. A route can also require a link with less capacity than the traffic demands. The evaluation must connect the logical graph to link width, rate, buffer capacity, routing and workload traffic.

#### What wafer-on-wafer hybrid bonding changes

Hybrid bonding can create dense electrical connections between bonded surfaces. The design question is where those connections are placed, which regions are connected, how traffic crosses between wafers and how long-distance paths are routed. More possible connections do not automatically provide more useful bandwidth: endpoint demand can be uneven, and a shared link or router can remain the bottleneck.

Physical feasibility adds constraints that a topology diagram does not show. Bond pitch, alignment, process variation, signal integrity, power delivery, heat removal, wafer warpage, repair strategy and yield affect which links can be built and operated. A network result based on ideal links cannot be treated as a fabricated-silicon result without those assumptions.

#### Faults change the available network

If the design claims fault tolerance, it must define the fault model: a missing bond, damaged region, reduced-capacity link, dead router or wafer-level defect may remove different paths. The routing policy must detect the condition, find a valid alternative and state whether bandwidth, latency or application progress remains within a bound. A connected graph after repair is not enough if the remaining path cannot carry the traffic.

#### What the evaluation must measure

Compare the proposed network with the planar or mesh baseline under the same endpoint placement, traffic matrix, link capacity, routing policy, physical resource budget and fault assumptions. Report per-flow and aggregate bandwidth, latency distribution, congestion, buffer occupancy, power, thermal conditions, area or bond count, fault recovery and yield assumptions. Include communication collectives, hotspot traffic, long-distance flows, burstiness and reduced-link cases.

The captured DAC description supports network design for wafer-scale systems with wafer-on-wafer hybrid bonding. It reports no topology, bandwidth, latency, traffic, power, fault, thermal or yield result. The evidence supports a wafer-scale network direction, not demonstrated communication performance or fabrication feasibility.

[Observed paper card](../observed-subthemes/chiplet-interconnects.md#paper-dac-2026-research363)

## Hold the computation constant before comparing costs

For LEXI, the reference should perform the same computation with the same numerical representation, differing in communication coding. For the network proposal, candidate networks should execute common traffic or workloads under comparable physical-resource constraints. Otherwise a reported improvement may come from changed model accuracy, more links, or a more favorable workload rather than the proposed mechanism.

The cross-paper research question is whether representation-aware traffic reduction and physically grounded network design can be evaluated together. That is an inference, not a demonstrated integration or a historical trend. A complete study would report application completion time and energy, along with codec cost, congestion, physical link assumptions, and failure behavior. Neither of these short records yet supports that end-to-end conclusion.

## Compare the results carefully

First identify the inputs and required output quality. Then identify the limited resource: time, memory, communication, energy, circuit area, or correctness coverage. Ask which part of the method reduces that cost and which new cost it adds. Compare numbers only when the experiments hold these conditions sufficiently similar.

A conference description may explain the proposal while omitting the full experiment. An author preprint link may have been coded from its abstract. The source classification does not by itself establish that every table was read. Missing locations remain visible below.

## Complete captured evidence

These are evidence records, not substitutes for the explanations above. Each record preserves its problem, proposed method, measurements, comparison conditions, and source limits. A populated record does not establish that its mechanism has been fully explained or independently verified.

<span id="paper-dac-2026-research3121"></span>

### LEXI: Lossless Exponent Coding for Efficient Inter-Chiplet Communication in Hybrid LLMs

DAC 2026 · Record: `dac-2026-research3121`

[Read the step-by-step explanation](#explanation-dac-2026-research3121)

**Updated source-backed reading card**

Reviewed 2026-09-08. Deepens the existing LEXI treatment into a paper-level reading; separates lossless exponent representation from precision reduction and makes traffic distribution, codec overhead, exceptional values and link-level validation explicit.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Inter-chiplet tensor traffic in distributed LLM computation consumes link bandwidth and energy, especially when numeric representations carry repeated or predictable exponent information.

**Mechanism / artifact:**

Lossless exponent coding scheme for inter-chiplet tensor communication; supported formats, coding rule, metadata, exceptional-value handling, fallback path and codec hardware are unspecified.

**Workload — the work tested:**

Hybrid LLM tensor transfers; numeric formats, tensor shapes, traffic traces, chiplet topology, compression distribution and model-quality conditions are unspecified.

**Hardware and manufacturing assumptions:**

Chiplet interconnect with encode/decode logic; link width, protocol, latency, bandwidth, buffering, clock, area, energy and process are unspecified.

**Baseline — the comparison method:**

Uncoded tensor communication

Generic lossless compression

Traffic, format, link, codec and end-to-end measurement conditions are unspecified

**Reported measurements:**

Communication efficiency is claimed qualitatively; no compression ratio distribution, latency, energy, area, codec throughput or accuracy result is reported.

**Limits on the conclusion:**

Lossless coding must recover the supported input representation exactly. It does not lower numerical precision and cannot claim benefit for values or formats outside the declared coding domain. Repeated exponents may compress well, but the distribution can change by layer, tensor, model, precision and workload.

The complete path includes exponent extraction, metadata, encoding, buffering, link transfer, decoding and reconstruction. Fewer payload bits reduce communication time only when codec work, fixed headers, queueing and link access do not become the new bottleneck. Exceptional values, sign, mantissa, zero, overflow and poorly compressible blocks need defined handling.

The official description reports no compression-ratio distribution, link latency, codec throughput, energy, area, traffic trace, fallback behavior or model-accuracy result. It supports a representation-aware communication direction, not demonstrated inter-chiplet or end-to-end LLM improvement.

**Source and location**

Evidence tier: Primary captured official DAC description plus existing chapter level lexi discussion; no full paper extraction, codec reproduction or link level traffic/hardware validation. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH3121)

DAC 2026 official description; captured Problem, Mechanism / artifact, Workload, Hardware, Baseline, Measurements and Limits fields; record RESEARCH3121; no manuscript pages.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** uncoded tensor communication

generic lossless compression

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH3121

**Hardware or process assumptions:** Chiplet interconnect supporting encode/decode logic; link width, protocol, latency, and process are unspecified.

**Limits:** No compression ratio, latency, energy, area, or accuracy data are reported.

Coding benefit depends on numeric distribution and decoder cost.

Official description only; link-level claims require traffic and hardware evidence.

**Method or artifact:** Lossless exponent coding scheme for inter-chiplet tensor communication.

**Metrics:** Communication efficiency is claimed qualitatively

**Problem:** Inter-chiplet traffic for distributed LLM computation consumes bandwidth and energy, especially for exponent-rich numeric representations.

**Workload or benchmark:** Hybrid LLM tensor transfers; numeric formats, traffic traces, chiplet topology, and baselines are unspecified.

</details>

<span id="paper-dac-2026-research363"></span>

### Network Design for Wafer-Scale Systems with Wafer-on-Wafer Hybrid Bonding

DAC 2026 · Record: `dac-2026-research363`

[Read the step-by-step explanation](#explanation-dac-2026-research363)

**Updated source-backed reading card**

Reviewed 2026-09-08. Deepens the existing wafer-network treatment into a paper-level reading; separates logical topology from physical link and bonding feasibility and makes congestion, fault, thermal and yield evidence explicit.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Wafer-scale systems span a large physical area and need communication paths that provide useful bandwidth and latency despite bonding, routing, fault, thermal and manufacturing constraints.

**Mechanism / artifact:**

Network design for wafer-scale systems with wafer-on-wafer hybrid bonding; topology, routing, link placement, traffic policy, fault handling and physical implementation are unspecified.

**Workload — the work tested:**

Wafer-scale compute traffic; traffic matrix, communication collectives, endpoint placement, burstiness, topology and workload suite are unspecified.

**Hardware and manufacturing assumptions:**

Wafer-on-wafer hybrid bonding with long-range on-wafer or inter-wafer links; bond pitch, link capacity, latency, power, thermal path, process variation, repair and yield are unspecified.

**Baseline — the comparison method:**

Planar wafer-scale network

Mesh or other interconnect baseline

Resource matching, traffic, fault, physical and routing conditions are unspecified

**Reported measurements:**

Wafer-scale communication efficiency is claimed qualitatively; no bandwidth, latency, power, fault-tolerance, thermal, yield or workload result is reported.

**Limits on the conclusion:**

A logical topology describes which endpoints can communicate; it does not establish that the required links fit on a wafer, that their capacity is available under contention or that a route has acceptable latency and power. Traffic concentrated on a few destinations can overload a shared link even when the graph has short paths.

Hybrid bonding changes where electrical connections can be placed, but long-range links still require signal integrity, power delivery, heat removal, alignment, process tolerance and repair assumptions. A network that works in an abstract model may lose capacity or yield when bonding defects, reduced links or thermal limits are included.

The official description reports no topology, bandwidth, latency, traffic, power, fault, thermal or yield result. It supports a wafer-scale network direction, not demonstrated communication performance or fabrication feasibility.

**Source and location**

Evidence tier: Primary captured official DAC description plus existing chapter level wafer network discussion; no full paper extraction, network reproduction or package/silicon validation. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH363)

DAC 2026 official description; captured Problem, Mechanism / artifact, Workload, Hardware, Baseline, Measurements and Limits fields; record RESEARCH363; no manuscript pages.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** planar wafer-scale network

mesh/interconnect baseline

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH363

**Hardware or process assumptions:** Wafer-on-wafer hybrid bonding with long-range on-wafer/inter-wafer links; process, thermal, and yield assumptions are unspecified.

**Limits:** No bandwidth, latency, power, fault tolerance, thermal, or yield results are reported.

Long-range network assumptions may not survive fabrication variation.

Official description only; package and silicon validation are required.

**Method or artifact:** Network design for wafer-scale hybrid-bonded systems.

**Metrics:** Wafer-scale communication efficiency is claimed qualitatively

**Problem:** Wafer-scale systems require scalable communication despite large physical extent, bonding constraints, and fault exposure.

**Workload or benchmark:** Wafer-scale compute traffic; topology, bonding pitch, fault model, and baselines are unspecified.

</details>

## What remains to establish

Resolve unspecified workloads, comparison methods, resource budgets, and source locations before generalizing a reported gain. Multiple papers in this selected sample permit comparison of mechanisms, but do not by themselves establish recurrence across years or a long-term trend.

[All subthemes](../expanded-taxonomy-v1.md) · [Research directions](../directions/README.md)
