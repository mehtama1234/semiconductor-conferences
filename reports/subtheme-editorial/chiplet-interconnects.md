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
