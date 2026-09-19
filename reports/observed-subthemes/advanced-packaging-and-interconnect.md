# Advanced packaging and interconnect

This subject has 2 records in the selected sample. This page explains where it fits, then presents all captured paper evidence without shortening the measurements or limitations.

[Definitions used in the paper records](../reading-guide-v1.md)

## Understand the parent subject first

- [Chiplets 3d and packaging](../themes/chiplets-3d-and-packaging.md)

## A route must be electrically usable as well as connected

Package and board routing place conductive paths between circuit connections. A geometric route can satisfy connectivity while still producing unacceptable electrical behavior. The surrounding conductors and materials affect how signals propagate and how return current flows. Ground-plane design is therefore part of the interconnect problem, not just unused space around signal wires. [Analog Devices' mixed-signal layout guidance](https://www.analog.com/en/resources/analog-dialogue/articles/what-are-the-basic-guidelines-for-layout-design-of-mixed-signal-pcbs.html) explains why layer choices and allowable return paths should be considered before routing.

The two records here concern different physical structures: double-sided redistribution wiring on a glass interposer, and joint ground-plane generation with rerouting. Neither captured description supplies numerical fabrication or signal-quality results.

## Routing both sides of a glass interposer

The [mixed-structure redistribution-layer paper](../observed-subthemes/advanced-packaging-and-interconnect.md#paper-dac-2026-research799) addresses a glass interposer with wiring on both sides. An interposer provides an intermediate connection structure between components. Redistribution layers route connections from their original locations to the locations required by the package assembly.

Using both sides adds routing choices, but connections between sides still require defined structures and locations. A routing algorithm must honor the actual layer arrangement, spacing rules, connection capacities, and obstacles. The title's “5.5D” label does not itself specify those details or provide a universal dimensional definition. The captured record leaves the layer stack and mixed-structure constraints unspecified.

The appropriate quality measurements include whether every required connection can be routed under the rules, wire lengths, use of inter-layer connections, and the electrical behavior of completed routes. Routing density alone is insufficient: denser paths may interact electrically or require different fabrication constraints. Mechanical deformation and process tolerances also need their own models and evidence rather than being inferred from geometric success.

The description contains no routability, signal-integrity, thermal, warpage, or yield results. It therefore cannot establish that a generated layout was fabricated successfully or that the glass structure outperforms another material in a comparable package.

## GRACE: choose the plane and signal routes together

[GRACE](../observed-subthemes/advanced-packaging-and-interconnect.md#paper-dac-2026-research1473) jointly considers ground-plane generation and rerouting. A ground plane provides a reference conductor and current-return paths. Changing its shape can alter the environment of a signal route; changing the route can in turn alter the plane structure needed for acceptable behavior.

This interaction explains why optimizing the two separately can require later correction. It does not identify GRACE's particular optimization algorithm. The captured source does not specify how candidate plane shapes are represented, how electrical behavior is estimated, or when rerouting is triggered. Those mechanisms should not be invented from the co-design label.

A useful comparison would keep the same connections, stackup, materials, and electrical constraints. It would then count complete routing and analysis time, including failed candidates and subsequent repairs. Signal integrity means preserving signals sufficiently for the receiving circuitry's requirements; its evaluation needs stated frequencies, impedances, coupling conditions, and acceptance limits. A visually continuous plane or shorter route is not by itself that evaluation.

The source provides no impedance, crosstalk, electromagnetic-interference, route-length, or runtime measurements. These remain open evidence requirements, not confirmed deficiencies of the proposed tool.

<span id="explanation-dac-2026-research799"></span>

## Mixed-structure double-sided RDL routing: connectivity must survive the package process

### The object being routed is not a flat board

Redistribution-layer routing changes where a die's connection points appear in the package. A glass interposer can contain conductive layers on more than one side, and a 5.5D package can combine the interposer with other structures and dies. A route therefore has to connect the right endpoints through the allowed layers, cross between sides where permitted, and respect spacing, obstacles, and connection capacity.

The paper's problem is not simply to maximize the number of wires. A path that is geometrically connected but violates a layer, spacing, or process rule is not a usable package connection. A path that meets geometry but creates excessive coupling or an unreliable inter-layer transition is also not a completed result. The routing representation must retain the physical distinctions that the package manufacturer and signal receiver will see.

### Double-sided routing adds choices and constraints

With one redistribution side, the router chooses paths within one layer arrangement. With two sides, a connection may have more available routing area, but it also needs a legal transition between sides and must coordinate the two sides' obstacles and capacities. A router can reduce local congestion on one side by moving a path to the other, while creating a crossing, return-path, assembly, or inspection problem elsewhere.

The captured record identifies a double-sided mixed-structure redistribution-layer routing method for glass-interposer-based 5.5D ICs. It does not state the layer stack, transition structure, design rules, net classes, or routing objective. The title's “5.5D” label is therefore not treated as a universal geometric definition, and no specific algorithm is attributed beyond the stated routing task.

### What a convincing result would measure

First establish legality: all required nets should be connected without spacing, layer, obstruction, or transition violations. Then report wire length, congestion, transition count, and the time and memory required to find the routes. If the design claims package feasibility, the evaluation must also connect the routing output to signal integrity, thermal behavior, mechanical deformation, process tolerance, and inspection or yield constraints.

The recorded baselines are single-sided RDL routing and homogeneous interposer routing. They identify useful comparison questions, but no quantitative routability, length, signal-integrity, thermal, warpage, or yield results are supplied. Routing density cannot be read as fabrication success or as a signal-quality improvement.

### What the paper establishes and what remains open

The accessible description establishes a routing problem involving both redistribution-layer sides and mixed package structures. It does not establish a completed legal layout, superior density, fabricated glass interposer, or better electrical behavior. A stronger evaluation would publish the package stack and design rules, exact transition and obstacle model, complete-net success rate, route-length and congestion distributions, reference router settings, electrical validation, mechanical/process analysis, and fabrication evidence.

[Official DAC description, record RESEARCH799](https://63dac.conference-program.com/presentation/?id=RESEARCH799&sess=sess109)

<span id="explanation-dac-2026-research1473"></span>

## GRACE: ground-plane and signal-route choices are coupled electrical decisions

### A signal needs a return path

A high-speed signal is a changing electrical field and current, not only a line drawn between two pins. The return current follows an impedance path shaped by the reference conductor, layer transitions, nearby conductors, and material properties. If a ground plane is cut, narrowed, or moved away from a route, the return path can change and the signal can experience altered impedance, coupling, or radiation.

This creates a dependency between two design objects. Ground-plane generation chooses the reference conductor and its openings or boundaries. Signal routing chooses the path that travels through that environment. Changing one after optimizing the other can invalidate the earlier electrical estimate, which is the reason a co-design engine can be useful.

### Co-design is not the same as adding two optimizers

GRACE is described as a ground-plane generation and rerouting-aware co-design engine. The important architectural question is when a plane change triggers rerouting, how candidate planes and routes are represented, and which electrical calculation decides whether a candidate is acceptable. The captured description does not expose those algorithmic details, so the writeup does not infer a particular optimizer or field solver.

The baseline boundary is separate ground-plane design and routing-oblivious plane generation. A fair comparison must use the same stackup, materials, nets, frequencies, termination conditions, electrical constraints, and total search budget. It must include failed candidates and repair or rerouting work. Otherwise a shorter route or visually larger plane may simply have been evaluated under a different physical model.

### Electrical quality needs defined tests

Signal integrity is a requirement on the received waveform or timing margin. It cannot be inferred from route length alone. Relevant tests may include characteristic impedance, insertion loss, crosstalk, electromagnetic interference, eye opening, or another receiver-specific limit. The chosen test must state frequency, source/load, material parameters, layer stack, and acceptance threshold.

The source reports no impedance, crosstalk, EMI, route-length, runtime, or fabrication measurements. Those are evidence gaps in the accessible record, not proof that GRACE fails them. A field-solver result would establish behavior under its model; a manufactured-board or package measurement would be needed to establish process and physical transfer.

### What GRACE establishes and what remains open

GRACE establishes the co-design problem of generating a ground plane while remaining aware of signal rerouting. It does not establish a numeric signal-integrity gain, a faster design flow, or a fabricated high-speed package. A stronger evaluation would publish the plane and route representation, electrical model, rerouting trigger, optimization budget, complete-route rate, impedance/crosstalk/EMI results, comparison settings, and measured or calibrated physical validation.

[Official DAC description, record RESEARCH1473](https://63dac.conference-program.com/presentation/?id=RESEARCH1473&sess=sess109)

## From package geometry to system conclusions

Both papers motivate expressing physical and electrical requirements together during automated routing. The connection is conceptual; the records do not show an integrated glass-interposer and ground-plane tool. A convincing end-to-end experiment would first verify routing legality, then correlate electrical models with trusted reference analysis or measurements, and finally assess the operating link under specified conditions.

Such evidence could support conclusions about useful connection density or reduced design effort. The present descriptions support neither a numerical ranking nor a long-term adoption forecast. The research opportunity is to make packaging automation accountable to completed, electrically acceptable connections rather than geometric objectives alone.

## Compare the results carefully

First identify the inputs and required output quality. Then identify the limited resource: time, memory, communication, energy, circuit area, or correctness coverage. Ask which part of the method reduces that cost and which new cost it adds. Compare numbers only when the experiments hold these conditions sufficiently similar.

A conference description may explain the proposal while omitting the full experiment. An author preprint link may have been coded from its abstract. The source classification does not by itself establish that every table was read. Missing locations remain visible below.

## Complete captured evidence

These are evidence records, not substitutes for the explanations above. Each record preserves its problem, proposed method, measurements, comparison conditions, and source limits. A populated record does not establish that its mechanism has been fully explained or independently verified.

<span id="paper-dac-2026-research799"></span>

### Mixed-Structure Double-Sided Redistribution Layer Routing for Glass Interposer-Based 5.5D ICs

DAC 2026 · Record: `dac-2026-research799`

[Read the step-by-step explanation](#explanation-dac-2026-research799)

**Updated source-backed reading card**

Reviewed 2026-09-08. Deepens the official-description reading; explains mixed-structure double-sided redistribution routing while keeping package legality, electrical behavior and fabrication evidence separate.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Glass-interposer 5.5D packages require routing across mixed structures and both redistribution-layer sides while preserving legal, electrically usable connections.

**Mechanism / artifact:**

Double-sided mixed-structure redistribution-layer routing method for glass-interposer-based 5.5D ICs.

**Workload — the work tested:**

Glass-interposer 5.5D package layouts; layer stack, net classes, transition rules, signal constraints and layout sizes are unspecified.

**Hardware and manufacturing assumptions:**

Glass interposer with double-sided RDL and heterogeneous dies; process, spacing, transition, warpage, signal-integrity and yield assumptions are unspecified.

**Baseline — the comparison method:**

Single-sided RDL routing

Homogeneous interposer routing

**Reported measurements:**

Routing density and package feasibility are claimed qualitatively; no complete-net rate, wire length, congestion, signal-integrity, thermal, warpage or yield result is reported.

**Limits on the conclusion:**

Double-sided geometric connectivity does not establish legal transitions, signal quality, mechanical reliability, fabrication success or yield.

The captured description does not expose a layer stack, exact routing algorithm, design rules, obstacles, transition structure or numeric comparison.

Official description only; package fabrication-aware and electrical validation were not performed.

**Source and location**

Evidence tier: Official DAC description; full manuscript and reproduction not performed. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH799&sess=sess109)

DAC official description, Captured Description and Authors fields; record RESEARCH799; no manuscript pages.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** single-sided RDL routing

homogeneous interposer routing

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH799

**Hardware or process assumptions:** Glass interposer with double-sided RDL and heterogeneous dies; process, warpage, and SI assumptions are unspecified.

**Limits:** No routability, length, signal integrity, thermal, warpage, or yield results are reported.

Mixed structures may complicate fabrication and inspection.

Official description only; package fabrication-aware validation is required.

**Method or artifact:** Double-sided mixed-structure redistribution-layer routing method.

**Metrics:** Routing density and package feasibility are claimed qualitatively

**Problem:** 5.5D glass-interposer packages require routing across mixed structures and both redistribution-layer sides.

**Workload or benchmark:** Glass-interposer 5.5D package layouts; layer stack, signal constraints, and baselines are unspecified.

</details>

<span id="paper-dac-2026-research1473"></span>

### GRACE: A Ground Plane Generation and Re-Routing Aware Co-Design Engine

DAC 2026 · Record: `dac-2026-research1473`

[Read the step-by-step explanation](#explanation-dac-2026-research1473)

**Updated source-backed reading card**

Reviewed 2026-09-08. Deepens the official-description reading; explains why ground-plane generation and rerouting are coupled electrical decisions while preserving the missing model and measurement conditions.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Ground-plane design and high-speed signal routing interact, but separate optimization can make later electrical correction necessary.

**Mechanism / artifact:**

Ground-plane generation and rerouting-aware co-design engine.

**Workload — the work tested:**

High-speed PCB/package layouts; stackup, nets, frequencies, materials, electromagnetic model and layout population are unspecified.

**Hardware and manufacturing assumptions:**

PCB/package substrate with ground-plane and routing constraints; impedance, termination, field-solver, frequency and manufacturing assumptions are unspecified.

**Baseline — the comparison method:**

Separate ground-plane design

Routing-oblivious plane generation

**Reported measurements:**

Signal-integrity and routing quality are claimed qualitatively; no impedance, crosstalk, EMI, route-length, runtime or fabrication measurement is reported.

**Limits on the conclusion:**

The source does not identify how planes are represented, when rerouting is triggered, what electrical model is used, or how total search and repair cost is measured.

A continuous plane or shorter route does not establish receiver-level signal integrity or fabricated-board behavior.

Official description only; field-solver calibration and physical validation were not performed.

**Source and location**

Evidence tier: Official DAC description; full manuscript and reproduction not performed. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH1473&sess=sess109)

DAC official description, Captured Description and Authors fields; record RESEARCH1473; no manuscript pages.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** separate ground-plane design

routing-oblivious plane generation

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH1473

**Hardware or process assumptions:** PCB/package substrate with ground-plane and routing constraints; frequency and material assumptions are unspecified.

**Limits:** No impedance, crosstalk, EMI, route length, runtime, or fabrication results are reported.

EM-aware co-design depends on accurate substrate models.

Official description only; field-solver validation is required.

**Method or artifact:** Ground-plane generation and re-routing-aware co-design engine.

**Metrics:** Signal-integrity and routing quality are claimed qualitatively

**Problem:** Ground-plane design and signal routing interact in high-speed layouts, but are often optimized separately.

**Workload or benchmark:** High-speed PCB/package layouts; stackup, nets, electromagnetic model, and baselines are unspecified.

</details>

## What remains to establish

Resolve unspecified workloads, comparison methods, resource budgets, and source locations before generalizing a reported gain. Multiple papers in this selected sample permit comparison of mechanisms, but do not by themselves establish recurrence across years or a long-term trend.

[All subthemes](../expanded-taxonomy-v1.md) · [Research directions](../directions/README.md)
