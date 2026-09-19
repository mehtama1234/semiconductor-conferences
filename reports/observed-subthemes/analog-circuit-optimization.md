# Analog circuit optimization

This subject has 1 record in the selected sample. This page explains where it fits, then presents all captured paper evidence without shortening the measurements or limitations.

[Definitions used in the paper records](../reading-guide-v1.md)

## Understand the parent subject first

- [Analog mixed signal and emerging devices](../themes/analog-mixed-signal-and-emerging-devices.md)

## The objective is electrical behavior under specified conditions

Analog circuit optimization selects a circuit structure or its parameters to meet electrical requirements. A candidate is useful only if it satisfies all mandatory constraints, not merely because one score improves. The relevant conditions include the intended input, operating frequency, supply, load, and fabrication model.

The selected paper, [COmPOSER](../observed-subthemes/analog-circuit-optimization.md#paper-dac-2026-research1407), proposes performance-oriented synthesis for radio-frequency and millimeter-wave circuits. The captured official description identifies this scope but does not specify the circuit families, optimization algorithm, or quantitative results.

<span id="explanation-dac-2026-research1407"></span>

## COmPOSER: why RF synthesis must include the physical layout

### The target is a post-layout circuit, not only a schematic

At radio and millimeter-wave frequencies, a wire, inductor, transmission line or power network is part of the electrical circuit. Its resistance, capacitance, inductance, coupling and substrate interaction change with geometry. A schematic-level optimizer can choose transistor sizes that satisfy equations for an idealized circuit and still miss the target after placement and routing introduce parasitics.

COmPOSER treats the design target as a connected chain:

`specification → active/passive sizing → primitive layout → placement/routing/PDN → EM and SPICE validation`

The paper evaluates low-noise amplifiers and power amplifiers in a commercial 65 nm process kit at frequencies up to 60 GHz. The central claim is narrower than “automation solves RF design”: a layout-aware flow can generate designs whose post-layout measurements meet the selected targets while reducing turnaround time relative to the reported manual baseline.

### Stage 1 combines equations with learned EM models

The first stage uses physics-based equations for active-device sizing and machine-learning models for layout-dependent passive behavior. For LNAs, the flow starts from targets such as center frequency, gain, noise figure, bandwidth, load, and input return loss. It derives candidate transistor sizes from noise–bandwidth–gain relationships, sweeps a realizable input-resistance interval of 40–60 ohms, and selects inductor and matching-network dimensions.

For PAs, it estimates the number of stages from the target gain, derives the output device width from saturation-power and load-line conditions, scales preceding stages, and constructs inter-stage matching networks. These equations constrain the search to candidates with a meaningful RF interpretation instead of treating every parameter vector as equally valid.

The passive models address the expensive part of the loop. The authors generate 80,000 spiral-inductor layouts with a Python generator and simulate them in Cadence EMX over 24 hours. A 200-estimator random forest predicts inductance, peak quality factor, frequency of peak quality factor and self-resonant frequency from geometry. An inverse k-nearest-neighbor model maps target passive responses back to geometries. The paper reports R² greater than 0.999 for the forward inductor model and says the EM optimizer is accurate within 0.4% of EM simulation with more than 1,000× speedup for that step.

These are surrogate-model measurements, not a guarantee that every unseen geometry is accurate. The model is trained on a technology-specific dataset, and the paper’s claim is bounded by the geometry range, process kit, EM solver and target passive types represented there.

### Stage 2 turns dimensions into checkable primitives

The second stage converts transistor widths, finger counts, channel lengths, inductors, transmission lines, capacitors and other passive parameters into DRC-clean layout blocks. The blocks include active-device structures and several geometry variants for passives. Variants give the later placer choices that trade area, routing access and RF behavior.

This stage matters because a numerical design vector is not yet a manufacturable layout. A candidate must have valid spacing, layers, contacts, orientations and interfaces. Primitive generation also makes the flow hierarchical: sizing is specific to an LNA or PA, while the later layout machinery can operate on a common set of blocks and constraints.

### Stage 3 makes physical choices explicit

COmPOSER formulates placement as a mixed-integer linear program. The objective combines bounding-box area and weighted half-perimeter wirelength. RF-critical nets receive higher weights, while the constraints select exactly one primitive variant and orientation, prevent overlap with routing halos, and place pads on permitted chip edges and pitches.

For typical designs with 28–30 modules, the paper reports about 2,300 variables and 3,300 constraints, solved with Gurobi at a 10^-3 mixed-integer gap in about 20 seconds. Routing then constructs a Manhattan grid around pins and blockages, builds a tree for each net, and uses A* search with resistance, via and net-priority costs. Critical nets can use upper metal layers and increased widths. The power-delivery-network generator assigns metal resources, avoids shielded passive regions and places decapacitors in legal whitespace.

These steps are not merely implementation details. Placement and routing change the parasitics that the first-stage sizing assumed. A placement objective that ignores RF-critical nets can produce a compact but electrically poor layout. Conversely, giving every net equal priority can waste routing resources. COmPOSER makes those choices explicit and then checks their electrical consequence.

### Stage 4 closes the schematic–layout loop

The final layout is analyzed with Cadence EMX to obtain frequency-dependent parasitics, including coupling, current crowding and substrate loss. Those parasitics are back-annotated into a netlist and evaluated with Cadence Spectre. If a specification is not met, the flow tightens the associated constraint and reruns synthesis from Stage 1.

This loop distinguishes a layout-aware model from a layout-oblivious optimizer. A model can predict a passive accurately and still fail if placement, routing or the power network changes the combined circuit. Post-layout EM/SPICE validation is therefore the acceptance check for the generated design, while the learned EM model is an acceleration mechanism inside the search.

### The LNA results are post-layout results under one process

The LNA study contains four designs: three single-stage LNAs at different frequencies and one two-stage LNA. The targets include gain, bandwidth, S11 and noise figure. The reported post-layout results span 22, 25, 39, 45 and 60 GHz entries in the comparison table; the COmPOSER designs use 65 nm and 1.1 V.

For the COmPOSER designs, the table reports gain/noise-figure/bandwidth/S11/DC-power/area/runtime values of 13.5 dB/2.46 dB/6.1 GHz/−10 dB/6.57 mW/0.137 mm²/2.41 minutes for LNA 1; 9.2 dB/3.62 dB/4.8 GHz/−22 dB/4.70 mW/0.115 mm²/2.43 minutes for LNA 2; 6.45 dB/3.96 dB/4.7 GHz/−20 dB/4.00 mW/0.112 mm²/2.45 minutes for LNA 3; and 9.2 dB/5.3 dB/4 GHz/−20 dB/7.35 mW/0.178 mm²/2.73 minutes for LNA 4. The table marks all as stable. The manual comparison entries are not fully matched for every design; one cited design uses bandwidth extension and trades gain and noise figure, so raw column-by-column ranking would be misleading.

The paper reports that the synthesized LNAs meet the selected specifications after EM/SPICE validation and reduce the reported manual turnaround from about 70 hours to less than 24 minutes. Table 4 separates stages: for an LNA, Stage 1 takes 52 seconds, primitive generation 35 seconds, layout synthesis 68 seconds and final SPICE/EM verification 21 minutes, for 23.58 minutes total. The one-time EM-model data generation is about 24 hours and training is under one minute. This means the headline turnaround excludes amortized model-data preparation when comparing one isolated design, unless that cost is accounted across multiple designs.

### The PA results show a different objective mix

The PA study covers Class-A designs at 20, 40 and 60 GHz. The reported post-layout results are: PA1 gain 14.7 dB, saturation power 9.5 dBm, bandwidth 10.2 GHz, DC power 51.3 mW, maximum PAE 25%, area 0.220 mm² and runtime 2.31 minutes; PA2 gain 16 dB, saturation power 6.7 dBm, bandwidth 5.1 GHz, DC power 53.0 mW, maximum PAE 7.5%, area 0.254 mm² and runtime 3.25 minutes; PA3 gain 13.6 dB, saturation power 6.8 dBm, bandwidth 8.3 GHz, DC power 63.5 mW, maximum PAE 6.4%, area 0.282 mm² and runtime 3.74 minutes. All are marked stable and the paper states that they meet their specification targets after post-layout evaluation.

The PA numbers should not be treated as a single quality score. Saturation power, gain, bandwidth, DC power, PAE and area answer different engineering questions. A design can improve one while worsening another. The paper’s useful evidence is that the flow produced complete post-layout candidates under its stated target constraints, not that PA1 dominates PA2 or PA3 in every application.

### The ablation isolates the cost of ignoring layout

The paper replaces the EM-aware first stage with schematic-only sizing. At a 60 GHz target, the layout-oblivious flow produces a 45 GHz PA and a 40 GHz LNA. The reported PA loses 4.6 dB of gain and 4 dB of output power, while the LNA loses 3.4 dB of gain and incurs a 1.75 dB noise-figure degradation. Restoring EM-aware modeling aligns the PAs and the 25 GHz LNA with their targets, with smaller systematic offsets reported for LNA-3.

This ablation supports a specific causal interpretation: unmodeled layout effects can move the realized RF behavior far enough to invalidate schematic-level sizing. It does not prove that COmPOSER’s particular surrogate is the only way to avoid that error, nor that all process nodes show the same magnitude.

### What the productivity claim includes

Table 4 compares the reported COmPOSER flow with a manual 40 GHz LNA design taking about 70 hours. COmPOSER’s total is about 23.58 minutes for the LNA and 40.10 minutes for the PA when final EM/SPICE verification is included. The paper reports approximately 178× faster for the LNA table and a 100–300× productivity gain overall. The comparison is design-turnaround time under the authors’ flow and baseline; it is not a speedup of one equal simulator invocation.

The manual baseline includes schematic optimization, layout generation and post-layout optimization. COmPOSER includes reusable EM-model preparation and automated stages, but the one-time 24-hour passive-data generation is listed separately. A deployment claim must state the number of designs over which that preparation is amortized, the amount of human intervention, failed runs, constraint revisions and whether manual designers receive the same process-kit and layout constraints.

### What COmPOSER establishes and what remains conditional

The manuscript supports a stronger claim than the original official card: an open-source, four-stage, layout-aware flow generated and post-layout-validated 65 nm CMOS LNAs and PAs up to 60 GHz, with reported performance comparable to selected manual designs and substantially shorter reported turnaround. The EM ablation shows why schematic-only optimization is insufficient for the tested high-frequency cases.

It does not establish universal topology synthesis, transfer to other process kits, fabrication measurements, equal human effort, or a guaranteed 100–300× gain for every RF design. Results depend on the 65 nm models, passive-training corpus, EM solver, circuit families, constraints, target frequencies, PDK rules, post-layout retry behavior and selected manual comparisons. The repository was inspected as a source reference but the flow, EM simulations and layouts were not executed here.

**Primary source read:** [COmPOSER arXiv version 3](https://arxiv.org/abs/2603.20486), Sections 2–6 and Tables 1–4, PDF pages 2–7, including the four-stage architecture, 80k-inductor EM dataset, analytical sizing, MILP/A* layout, post-layout EM/SPICE validation, LNA/PA tables, runtime breakdown and layout-oblivious ablation; [COmPOSER repository](https://github.com/UMN-EDA/COmPOSER); [official DAC record](https://63dac.conference-program.com/presentation/?id=RESEARCH1407&sess=sess118). The manuscript was read; the repository flow and circuit/EM runs were not reproduced here.

## Several requirements can compete

Gain describes how a circuit changes signal magnitude under stated conditions. Noise concerns unwanted fluctuations added to the signal. Linearity concerns how consistently the output follows the intended input-output relationship as the input changes. Power and area impose additional implementation costs.

An improvement in one quantity can accompany deterioration in another. A design search must therefore distinguish requirements that cannot be violated from preferences among acceptable designs. A combined numerical score can conceal a failed requirement unless feasibility is checked explicitly.

The source does not identify COmPOSER's objectives, weights, constraints, or target values. “Performance-oriented” must not be interpreted as simultaneously optimizing every listed circuit property. The evaluation needs the actual specification before its success can be judged.

## Synthesis and parameter adjustment are different scopes

Parameter optimization changes values within a selected structure. Synthesis can include choosing or constructing the structure itself. The distinction matters because a search that changes topology explores a different space from one that tunes a fixed circuit.

The captured description does not establish which structural choices COmPOSER supports or how candidates are represented. It should not be assumed to generate arbitrary circuits, use a learned model, or apply a particular search technique. Those mechanisms require the full source.

Regardless of search method, candidates must have meaningful operating conditions and valid connections. Counting generated candidates is not the same as counting realizable circuits. Failed simulations, invalid candidates, and repairs belong in the reported search effort.

## Physical implementation changes the calculation

A schematic captures intended devices and connections, while layout adds geometry-dependent electrical effects. At the frequencies targeted by the paper, the assumptions used to represent connections and surrounding structures are part of the evaluation, not incidental implementation details.

A favorable result before layout therefore needs checking after the physical implementation is represented with appropriate extracted models. The source leaves the process design kit, parasitic assumptions, devices, and simulation procedure unspecified. It supplies no measured circuit results.

That absence does not prove the method fails physically. It means the available record cannot establish that its optimized candidates survive the relevant physical effects or meet requirements on fabricated hardware.

## Expensive evaluation creates a search-budget question

If evaluating each candidate is costly, the number and type of evaluations matter. A search can save effort by prioritizing promising choices, but inaccurate guidance can also discard useful regions or favor misleading estimates.

A fair comparison with manual design or another optimizer would preserve the same specification, process, available structures, and evaluation budget. Human preparation, simulation setup, failed candidates, and final verification should be recorded rather than excluded selectively. Different stopping rules can otherwise produce apparently different quality simply by allowing different amounts of work.

The captured description provides no simulation count, runtime, gain, noise, linearity, power, area, or frequency results. It cannot support a numerical ranking against the baseline categories in the coding.

## What would demonstrate useful automation?

A stronger evaluation would provide complete specifications and reproducible candidate descriptions, verify feasibility with a consistent simulator and physical-analysis procedure, and report the final tradeoffs alongside total engineering cost. Testing changed targets or operating conditions would help establish whether the method generalizes beyond its development cases.

COmPOSER motivates directing synthesis toward the electrical behavior that matters to the application. The current record supports that research purpose, not an established performance improvement, a general replacement for expert design, or a long-term adoption claim. The decisive outcome is a physically validated circuit meeting fixed requirements with a clearly accounted reduction in design effort.

## Compare the results carefully

First identify the inputs and required output quality. Then identify the limited resource: time, memory, communication, energy, circuit area, or correctness coverage. Ask which part of the method reduces that cost and which new cost it adds. Compare numbers only when the experiments hold these conditions sufficiently similar.

A conference description may explain the proposal while omitting the full experiment. An author preprint link may have been coded from its abstract. The source classification does not by itself establish that every table was read. Missing locations remain visible below.

## Complete captured evidence

These are evidence records, not substitutes for the explanations above. Each record preserves its problem, proposed method, measurements, comparison conditions, and source limits. A populated record does not establish that its mechanism has been fully explained or independently verified.

<span id="paper-dac-2026-research1407"></span>

### COmPOSER: Circuit Optimization of mm-Wave/rf Circuits with Performance-Oriented Synthesis for Efficient Realizations

DAC 2026 · Record: `dac-2026-research1407`

[Read the step-by-step explanation](#explanation-dac-2026-research1407)

**Updated source-backed reading card**

Reviewed 2026-09-08. Reconciles the official DAC card with arXiv version 3 and the public COmPOSER repository; separates EM-surrogate accuracy, post-layout circuit performance, layout-oblivious ablation and amortized versus per-design turnaround.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

At RF/mm-wave frequencies, layout parasitics, coupling, substrate loss, routing geometry and power delivery alter circuit behavior, so schematic-only optimization can miss post-layout gain, noise, frequency and power targets while requiring expensive manual iteration.

**Mechanism / artifact:**

Four-stage COmPOSER flow: physics-based active sizing plus random-forest/k-NN EM-aware passive optimization; DRC-clean primitive generation; MILP placement, A* routing, pad and PDN synthesis; Cadence EMX/Spectre post-layout validation with targeted constraint tightening and re-synthesis.

**Workload — the work tested:**

65 nm CMOS RF/mm-wave LNAs and Class-A PAs up to 60 GHz; four LNA designs and three PA designs; 80,000 spiral inductor EM samples generated and simulated in Cadence EMX; Nangate or other non-target technologies are not used for the reported circuit tables.

**Hardware and manufacturing assumptions:**

Commercial 65 nm process kit, Cadence EMX, Calibre extraction and Spectre; 1.1 V LNA and 1.2 V PA table conditions; Gurobi MILP at 10^-3 gap; typical 28–30-module layouts with about 2.3k variables and 3.3k constraints. Passive model, PDK, routing and EM results were not reproduced here.

**Baseline — the comparison method:**

Manual RF design, including a reported approximately 70-hour 40 GHz LNA design

Layout-oblivious schematic-only sizing in the EM ablation

Selected prior/manual LNA table entries where the process, topology and objective are sufficiently visible

**Reported measurements:**

Passive model: 80k inductors generated and EM-simulated over 24 hours; 200-tree random forest reports R² > 0.999 for inductance/quality/resonance outputs; EM optimizer reports within 0.4% of EM simulation and >1000× speedup for that step.

LNA post-layout table: COmPOSER LNA1/2/3/4 gain 13.5/9.2/6.45/9.2 dB, NF 2.46/3.62/3.96/5.3 dB, bandwidth 6.1/4.8/4.7/4 GHz, S11 −10/−22/−20/−20 dB, DC power 6.57/4.70/4.00/7.35 mW, area 0.137/0.115/0.112/0.178 mm², runtime 2.41/2.43/2.45/2.73 min; all stable.

PA post-layout table: PA1/2/3 gain 14.7/16/13.6 dB, Psat 9.5/6.7/6.8 dBm, bandwidth 10.2/5.1/8.3 GHz, DC power 51.3/53.0/63.5 mW, maximum PAE 25/7.5/6.4%, area 0.220/0.254/0.282 mm², runtime 2.31/3.25/3.74 min; all stable.

Runtime: LNA total 23.58 min and PA total 40.10 min including EM/SPICE verification versus about 70 hours manual LNA; one-time passive data generation about 24 hours. Layout-oblivious 60 GHz ablation shifts PA/LNA center frequency to 45/40 GHz, loses 4.6/3.4 dB gain, loses 4 dB PA output power and worsens LNA NF by 1.75 dB.

**Limits on the conclusion:**

Post-layout results are simulation and extraction results in one commercial 65 nm process kit, not fabricated-silicon measurements or universal transfer across PDKs, frequencies, topologies and passive structures.

The manual comparison is not fully matched for every table column; one cited LNA uses bandwidth extension and trades gain/NF. Productivity includes a separately listed one-time 24-hour EM-data generation cost and differs in human intervention, stopping rules and verification boundaries.

Surrogate accuracy and runtime do not establish complete circuit correctness; constraint retries, failed candidates, post-layout convergence, repository execution and independent reproduction remain open. The 100–300× claim is a reported workflow turnaround comparison, not a universal per-simulation speedup.

**Source and location**

Evidence tier: Primary arxiv preprint v3, public repository and official DAC description; selected method/evaluation reading, execution not reproduced. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://arxiv.org/pdf/2603.20486v3)

Version 3: Sections 2–6 and Tables 1–4, PDF pages 2–7; four-stage framework Section 2.2 pages 2–3; 80k-inductor dataset and EM model Section 3 pages 3–4; MILP/A* and PDN Section 5 pages 4–5; experimental setup, LNA/PA Tables 2–4 and layout-oblivious ablation Section 6 pages 5–7. Public artifact: https://github.com/UMN-EDA/COmPOSER; official DAC record: https://63dac.conference-program.com/presentation/?id=RESEARCH1407&sess=sess118.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** manual RF design

generic circuit optimization

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH1407

**Hardware or process assumptions:** RF integrated-circuit process with frequency and matching constraints; PDK and parasitic assumptions are unspecified.

**Limits:** No gain, noise, linearity, power, area, frequency, or simulation-cost results are reported.

Optimization may depend strongly on process models.

Official description only; post-layout RF validation is required.

**Method or artifact:** Performance-oriented mm-Wave/RF circuit synthesis and optimization framework.

**Metrics:** RF circuit quality and synthesis efficiency are claimed qualitatively

**Problem:** RF circuit synthesis must optimize nonlinear performance objectives under expensive simulation and layout constraints.

**Workload or benchmark:** mm-Wave/RF circuits; devices, targets, simulation, and baselines are unspecified.

</details>

## What remains to establish

Resolve unspecified workloads, comparison methods, resource budgets, and source locations before generalizing a reported gain. This subject is represented by one paper and supports a case study, not evidence of recurrence or a long-term trend.

[All subthemes](../expanded-taxonomy-v1.md) · [Research directions](../directions/README.md)
