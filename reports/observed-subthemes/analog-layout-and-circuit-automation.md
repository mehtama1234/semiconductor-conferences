# Analog layout and circuit automation

This subject has 3 records in the selected sample. This page explains where it fits, then presents all captured paper evidence without shortening the measurements or limitations.

[Definitions used in the paper records](../reading-guide-v1.md)

## Understand the parent subject first

- [Analog mixed signal and emerging devices](../themes/analog-mixed-signal-and-emerging-devices.md)

## A compact layout is not necessarily a good analog circuit

Analog circuits process continuously varying electrical quantities. Their behavior depends on device properties and physical connections, not only on whether a connection exists. Placement can affect how closely two devices experience similar surroundings, while routing introduces resistance and capacitance that alter circuit response.

Analog automation therefore uses constraints such as symmetry, grouping, and proximity to express design intent. These are explicit inputs in practical tools such as [ALIGN's constraint system](https://align-analoglayout.github.io/ALIGN-public/notes/const.html). A constraint is a means of obtaining acceptable electrical behavior, not a substitute for checking that behavior after the physical implementation is complete.

The three records here propose reusable circuit abstractions and two placement-search methods. Their evidence levels differ: the AMS standard-cell work reports fabricated-chip and jitter results, while the captured AlphaPlacer and Diffsp descriptions do not expose comparable numerical placement results.

<span id="explanation-dac-2026-research776"></span>

## DiffSP: a smooth placement objective still has to become legal geometry before it can affect an analog circuit

### Why sequence-pair placement is difficult to differentiate

A sequence pair represents relative block ordering with two discrete permutations. The permutations can be decoded into non-overlapping coordinates, but a small change in the ordering can move several blocks or change their relative relationships. The original choice therefore has no ordinary continuous gradient.

Analog placement also has coupled objectives. Area and wirelength are geometric; symmetry, matching, proximity and routing constraints express circuit intent; parasitics determine whether the placed and routed circuit meets electrical targets. Improving one objective can worsen another.

### What the Gumbel–Sinkhorn relaxation changes

DiffSP uses Gumbel–Sinkhorn relaxation to turn a hard permutation or sequence-pair constraint graph into a smooth approximation. A smooth representation permits automatic gradients to update the placement according to the selected objective.

The relaxed representation is not necessarily a valid permutation. It can contain fractional assignments or relationships that cannot coexist in a legal placement. The temperature used in the relaxation, the transition to a discrete sequence pair and the difference between relaxed and discrete objective values determine whether the optimization result survives conversion.

### Why the objective weights matter

The description names area, wirelength and symmetry as jointly optimized objectives. A weighted objective still encodes a choice: a larger weight on wirelength can favor compact connections even when it increases matching or coupling risk; a larger symmetry weight can consume area or increase route length.

The evaluation should state the weights, normalization, constraint handling and whether parasitic or circuit-performance terms enter the differentiable objective. A geometric score cannot stand in for gain, bandwidth, noise, jitter or yield unless its relationship to those properties has been established for the circuit family.

### What MILP legalization contributes

Mixed-integer linear programming can enforce exact discrete and geometric constraints after the relaxed optimization. It can impose non-overlap, alignment, symmetry, spacing or other linearized relations and return a legal arrangement when the constraints are feasible.

Legalization can also move blocks far from the relaxed solution, fail for an overconstrained instance or take substantial time. The final placement must be scored after legalization, not only before it. The runtime of the MILP stage, infeasibility rate, repair distance and resulting objective values belong in the comparison.

Legal geometry is still not final circuit evidence. Routing, parasitic extraction and post-layout simulation are needed to determine whether the analog circuit satisfies its specifications under the relevant process, voltage and temperature conditions.

### How to interpret the reported claims

The captured description says DiffSP improves placement quality and post-layout performance on industrial-level OTA benchmarks while reducing runtime relative to state-of-the-art analog placers. It does not report numeric placement quality, constraint-satisfaction rate, legalization failures, solver budget, extraction setup, parasitic results or circuit-performance values.

“Reduced runtime” requires the same hardware, initialization, number of restarts, simulator calls and post-processing boundary. “Better post-layout performance” requires the circuit metric, extraction flow, process corners and baseline layouts. Without those conditions, the source supports a method claim but not a reproducible general advantage.

### What the record establishes and where it stops

The official description establishes a differentiable sequence-pair analog-placement method using Gumbel–Sinkhorn relaxation, gradient optimization of area/wirelength/symmetry objectives and MILP legalization for exact constraints. It names industrial OTA benchmarks and qualitative placement, post-layout and runtime benefits. It does not expose the relaxation schedule, objective weights, legalization outcomes, solver cost or circuit-validation conditions.

The [DiffSP](../observed-subthemes/analog-layout-and-circuit-automation.md#paper-dac-2026-research776) record is evidence of a discrete-to-continuous placement method, not proof that the relaxed objective produces better legalized analog circuits. The explanation separates differentiable representation, objective choice, exact legalization, runtime and post-layout electrical validation.

<span id="explanation-dac-2026-research713"></span>

## AlphaPlacer: Monte Carlo search can guide analog placement only when its reward reflects electrical constraints

### What analog placement is deciding

Placement assigns circuit blocks or devices to physical locations before routing. The placement must avoid overlap and fit the available region, but analog requirements add relationships between objects. Matched devices may need similar surroundings, differential pairs may need symmetry, sensitive blocks may need proximity, and high-current or noisy structures may need isolation.

A compact placement or short total wirelength is not sufficient. Routing adds resistance and capacitance, and those parasitics can change gain, bandwidth, delay, noise, matching and stability. The placement objective must therefore be connected to the electrical behavior that the final circuit must satisfy.

### What a sequence pair represents

A sequence pair describes relative ordering between rectangular blocks using two permutations. The pair can be decoded into non-overlapping coordinates and is useful for expressing a large discrete placement space compactly. It does not, by itself, encode every analog requirement.

The decoded arrangement still needs spacing, symmetry, alignment, grouping, blockages, legal orientations and routing feasibility. A candidate can be valid as a sequence pair and invalid after analog constraints or power and well rules are applied. Search quality must be judged after the final placement is legalized and, where relevant, routed and extracted.

### How Monte Carlo tree search allocates effort

Monte Carlo tree search represents partial design decisions as nodes. It selects a promising partial choice, expands it, evaluates a completed or partially completed candidate, and uses the result to decide which branch to explore next. Exploration prevents the search from repeatedly following only the first apparently good arrangement.

A two-level search can separate coarse structural decisions from detailed sequence-pair choices. The exact benefit depends on the actions at each level, the reward function, the number of simulations, failed-candidate handling, random seed, simulation cost and stopping rule. If the reward is only geometric, it may favor placements that later fail routing or electrical simulation. If the reward uses detailed circuit extraction, the search may be more accurate but much slower.

### What expert-layout pretraining changes

Pretraining on historical layouts can learn which sequence-pair patterns occurred in expert designs. The learned distribution can guide the search toward regions that are plausible for similar circuits and reduce exploration of obviously poor orderings.

The same prior can be harmful when the new circuit has a different topology, constraint set, technology or objective. It can reproduce historical design habits without proving they are required. A valid evaluation must keep test circuits separate from the training layouts and include cases with unseen combinations of symmetry, proximity, device sizes and routing pressure.

### How to interpret the reported improvement

The captured description says AlphaPlacer significantly outperforms existing baselines across area, wirelength and post-layout performance. It does not report numeric values, matching statistics, parasitic metrics, runtime, search budget, yield, legalization failures or extracted-circuit conditions.

Area and wirelength are geometric measures. Post-layout performance is an electrical result only when the extraction, simulator, process corners, input conditions and circuit specifications are defined. A fair comparison must use the same constraints, technology, extraction flow and total search computation, and must include failed or unrouteable candidates rather than only successful outputs.

### What the record establishes and where it stops

The official description establishes a Monte Carlo tree-search analog-placement proposal using hierarchical sequence-pair search and expert-layout pretraining. It qualitatively claims improvements in area, wirelength and post-layout performance. It does not expose the reward, search budget, benchmark split, constraint satisfaction, routing success, extraction settings or numeric results.

The [AlphaPlacer](../observed-subthemes/analog-layout-and-circuit-automation.md#paper-dac-2026-research713) record is evidence of a guided placement-search method, not proof of improved analog circuits or practical deployment. The explanation separates representation, search allocation, learned priors, geometric objectives and extracted electrical validation.

<span id="explanation-dac-2026-research407"></span>

## AMS analog standard cells: digital PnR can automate placement only if the abstraction preserves electrical constraints

### What analog layout must preserve

Analog layout places and connects devices whose electrical behavior depends on geometry and surroundings. Matching requires paired or grouped devices to experience similar process variation, temperature, routing and neighborhood effects. Bias circuits must operate at valid voltages and currents. Routing adds resistance and capacitance, which can change gain, bandwidth, delay, noise and stability.

Digital place-and-route tools normally reason about cell legality, timing, congestion and connectivity. Those abstractions are useful only when the analog cell interface exposes the constraints that affect circuit behavior. A DRC-clean layout can still have poor matching, excessive coupling or an invalid bias point.

### What a circuit-level analog standard cell provides

A circuit-level analog standard cell is a reusable physical block with an internal circuit, geometry, pins, power connections and placement rules. The description names self-biased amplifiers, current mirrors and delay cells. The block can hide transistor-level construction from the digital PnR engine while presenting a known interface and fixed physical behavior.

This abstraction can reduce repeated manual layout work, but it moves responsibility into library creation and validation. The library must encode dimensions, legal orientations, symmetry or matching relationships, blockages, well and guard-ring requirements, power routing and allowed connections. If an important analog constraint is omitted, the automation can produce a physically legal but electrically unsuitable arrangement.

### What self-biasing changes

Self-biasing circuitry generates or stabilizes the operating condition needed by an analog block. Its valid behavior depends on supply voltage, process, temperature, load, startup, feedback and interaction with neighboring circuitry. Placing the block in a digital PnR flow does not remove those conditions.

The generated layout therefore needs post-layout extraction and circuit simulation. The check must compare the intended operating point and performance before and after parasitic extraction, then compare measured silicon where available. DRC and LVS establish geometric-rule and connectivity properties; they do not establish gain, jitter, noise, matching or stability.

### What the reported validation covers

The captured description reports fully automated DRC/LVS-clean layouts for a current source, an adaptive-bandwidth PLL and a probabilistic computer in fabricated 180 nm and 65 nm CMOS. It reports strong pre-/post-layout and silicon correlation, 0.98–1.50 ps simulated and 4.1 ps measured PLL jitter, at least 96% area utilization, 14.4–69.5% DCAP density and less-than-1-minute to 1-hour runtime.

These are materially stronger than a purely geometric demonstration, but their interpretation still needs the circuit specifications, process corners, supply conditions, extracted-netlist setup, jitter definition, area boundary, DCAP definition, library-development effort and manual corrections. Runtime for generating a layout is different from the total effort to create and validate the reusable analog library.

### What the record establishes and where it stops

The official description establishes a circuit-level analog-standard-cell and self-biasing workflow integrated with digital PnR and reports fabricated 180 nm and 65 nm examples with DRC/LVS, simulation and silicon evidence. It does not establish that the abstraction covers all analog constraints, all circuits or all PDKs, and it does not expose a full manual-effort, matching, area, power or corner comparison.

The [AMS analog standard-cell](../observed-subthemes/analog-layout-and-circuit-automation.md#paper-dac-2026-research407) record is evidence of a silicon-validated automation workflow for named circuits, not proof that digital PnR can replace analog design judgment generally. The explanation separates library abstraction, self-biasing, physical legality, extracted electrical behavior and silicon correlation.

## Reusing digital placement tools with analog building blocks

The [analog standard-cell layout paper](../observed-subthemes/analog-layout-and-circuit-automation.md#paper-dac-2026-research407) uses circuit-level analog standard cells and self-biasing techniques within digital place-and-route tools. A reusable cell gives the automation a defined physical object and connection interface. Biasing establishes the electrical operating conditions of a circuit; the title indicates that the proposed cells incorporate techniques related to that requirement.

The potential benefit is reuse of an existing placement and routing infrastructure. The essential question is which analog requirements the abstractions preserve. A legal placement can still have unsuitable coupling, poor matching, or excessive electrical loading. The source does not describe the self-biasing circuitry or establish which requirements are handled automatically, so those details should not be inferred.

Evaluation should separate library-development effort from the time to generate each subsequent layout. It should also count manual corrections and check the completed circuit with extracted interconnect effects. The captured record provides no area, electrical performance, matching, or human-time results. It supports a proposed workflow, not a demonstrated replacement for all manual analog layout.

## Alphaplacer: allocating search among placement choices

[Alphaplacer](../observed-subthemes/analog-layout-and-circuit-automation.md#paper-dac-2026-research713) uses Monte Carlo tree search for analog placement. In this general search family, partial choices form a branching structure, and evaluations guide which alternatives receive more exploration. The exact moves, evaluation policy, and circuit objective in this paper are not exposed in the captured description.

The conceptual tradeoff is search effort versus the quality of the chosen placement. A detailed electrical evaluation may be expensive; a cheap geometric score may omit important circuit behavior. The paper's benefit therefore depends on what the search measures and how well that measure predicts the completed circuit's performance.

A comparison should use the same constraints and total computation budget, and repeat variable search runs. It should report failed or unrouteable candidates rather than considering only successful outputs. No such counts, runtime, placement-quality metrics, or extracted-circuit results are supplied here.

## Diffsp: connecting discrete placement to gradient optimization

[Diffsp](../observed-subthemes/analog-layout-and-circuit-automation.md#paper-dac-2026-research776) makes a sequence-pair placement representation differentiable. A sequence pair encodes relative placement relationships using two orderings of blocks. Those orderings are discrete choices, whereas a gradient describes sensitivity to a continuous change.

The proposed approach must therefore connect an optimizable representation to a final valid arrangement. The captured record does not specify its relaxation or conversion procedure. It would be unjustified to assume that every intermediate candidate is legal, or that converting the final result necessarily preserves all of its predicted benefits.

Evaluation should check constraint satisfaction after conversion, then routing and electrical performance. The time and quality cost of any repair belongs in the comparison. The source provides none of these quantitative results, so the differentiable formulation is a proposed capability rather than proof of better analog circuits.

## The useful cross-paper question

These proposals address different parts of automation: what reusable objects to provide, how to explore arrangements, and how to make arrangement choices amenable to numerical optimization. They motivate studying complete, electrically validated layout generation under a fixed engineering budget. They do not establish an integrated flow or a historical rate of adoption. The decisive outcome is the time and effort required to obtain circuits meeting the same specifications, including all manual intervention and post-layout checks.

## Compare the results carefully

First identify the inputs and required output quality. Then identify the limited resource: time, memory, communication, energy, circuit area, or correctness coverage. Ask which part of the method reduces that cost and which new cost it adds. Compare numbers only when the experiments hold these conditions sufficiently similar.

A conference description may explain the proposal while omitting the full experiment. An author preprint link may have been coded from its abstract. The source classification does not by itself establish that every table was read. Missing locations remain visible below.

## Complete captured evidence

These are evidence records, not substitutes for the explanations above. Each record preserves its problem, proposed method, measurements, comparison conditions, and source limits. A populated record does not establish that its mechanism has been fully explained or independently verified.

<span id="paper-dac-2026-research407"></span>

### AMS Layout Automation Using Circuit-Level Analog Standard Cells and Self-Biasing Techniques in Digital PnR Tools

DAC 2026 · Record: `dac-2026-research407`

[Read the step-by-step explanation](#explanation-dac-2026-research407)

**Updated source-backed reading card**

Reviewed 2026-09-08. Reconciles the AMS layout card with the captured official DAC description; explains circuit-level analog standard-cell abstraction, self-biasing, digital PnR integration, extracted/silicon validation and the exact reported jitter, density, utilization and runtime claims.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Analog and mixed-signal layout requires electrical matching, biasing, parasitic control and physical constraints that ordinary digital place-and-route abstractions do not directly represent.

**Mechanism / artifact:**

Circuit-level analog standard-cell library integrated with a digital PnR environment, including self-biased amplifiers, current mirrors and delay cells, with automation validated on fabricated 180 nm and 65 nm CMOS chips.

**Workload — the work tested:**

Current source, adaptive-bandwidth PLL and probabilistic computer layouts; exact circuit specifications, constraints, PDK rules, library contents, manual baselines and comparison flow are unspecified.

**Hardware and manufacturing assumptions:**

180 nm and 65 nm CMOS fabrication, analog circuit-level standard cells and digital PnR tools; matching constraints, parasitic extraction, bias conditions, supply, corners, chip area boundary and silicon measurement setup are not fully exposed.

**Baseline — the comparison method:**

Manual analog layout

Digital PnR without analog abstractions

Transistor-level stem-cell approaches

Circuit specifications, effort accounting, extraction settings and baseline implementation conditions are unspecified

**Reported measurements:**

The captured official description reports DRC/LVS-clean fabricated layouts, strong pre-/post-layout and silicon correlation, 0.98–1.50 ps simulated and 4.1 ps measured PLL jitter, at least 96% area utilization, 14.4–69.5% DCAP density and less-than-1-minute to 1-hour runtime; exact definitions and conditions are not exposed.

**Limits on the conclusion:**

An analog standard cell is a reusable circuit-level physical block with a defined interface and layout geometry. It can preserve relationships that would be difficult for a digital tool to create from individual transistors, but it can also hide internal matching, routing, well, guard-ring, substrate, noise and parasitic constraints from the placement engine.

Self-biasing establishes operating conditions through circuitry rather than relying only on external bias inputs. The cell must remain within its valid voltage, current, process and temperature range after placement and routing. A legal connection does not prove that the bias point, gain, bandwidth, noise or matching target survives extracted parasitics.

Using digital PnR requires an abstraction boundary: the tool must know cell dimensions, pins, blockages, legal orientations, power connections, analog keep-outs and constraints. The evaluation must show which analog constraints are encoded, which are enforced by the library and which still require manual repair. Reusing a digital flow does not mean analog behavior has become digital.

The description reports current-source, adaptive-bandwidth-PLL and probabilistic-computer layouts in fabricated 180 nm and 65 nm CMOS, DRC/LVS cleanliness, pre-/post-layout and silicon correlation, 0.98–1.50 ps simulated and 4.1 ps measured PLL jitter, at least 96% area utilization, 14.4–69.5% DCAP density and less-than-1-minute to 1-hour runtime. It does not expose circuit specifications, corners, matching statistics, area boundary, manual effort, extraction setup, power or baseline parity; the claims therefore establish a silicon-validated workflow for named examples, not universal analog-layout automation.

**Source and location**

Evidence tier: Primary captured official DAC description only; no full paper extraction, pnr/library artifact reproduction or independent extracted circuit, matching, runtime, area, power and silicon validation. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH407)

DAC 2026 official description and data/review-packets/dac-2026-research407.json: circuit-level analog standard cells; self-biased amplifiers/current mirrors/delay cells; digital PnR; fabricated 180 nm and 65 nm CMOS; current source, adaptive-bandwidth PLL and probabilistic computer; DRC/LVS-clean; pre/post-layout and silicon correlation; 0.98–1.50 ps simulated and 4.1 ps measured jitter; ≥96% utilization; 14.4–69.5% DCAP density; <1 min–1 hr runtime; omitted circuit, corner, matching and baseline conditions.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** manual analog layout

digital PnR without analog abstractions

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH407

**Hardware or process assumptions:** Digital PnR tools extended for analog cells in a mixed-signal process; matching, parasitic, and bias assumptions are unspecified.

**Limits:** No area, matching, parasitic, circuit-performance, or human-time results are reported.

Standard-cell abstractions may omit analog-specific constraints.

Official description only; layout claims require extracted simulation evidence.

**Method or artifact:** Analog standard-cell abstractions and self-biasing techniques embedded in digital PnR automation.

**Metrics:** AMS layout automation is claimed qualitatively

**Problem:** Analog/mixed-signal layout remains manual and difficult to integrate with digital automation flows.

**Workload or benchmark:** AMS circuit layouts; technologies, circuits, PDK constraints, and quality baselines are unspecified.

</details>

<span id="paper-dac-2026-research713"></span>

### Alphaplacer: Analog Placement Enhanced by Monte Carlo Tree Search

DAC 2026 · Record: `dac-2026-research713`

[Read the step-by-step explanation](#explanation-dac-2026-research713)

**Updated source-backed reading card**

Reviewed 2026-09-08. Reconciles the AlphaPlacer card with the captured official DAC description; explains hierarchical sequence-pair placement, Monte Carlo tree search, expert-layout pretraining, reward selection and the distinction between geometric placement quality and extracted analog performance.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Analog placement must satisfy discrete relative-position choices together with symmetry, matching, proximity, routing and parasitic objectives. The search space grows rapidly and expert placement practice is difficult to encode in generic heuristics.

**Mechanism / artifact:**

AlphaPlacer: a Monte Carlo tree-search analog placement framework using hierarchical sequence-pair search and a two-level MCTS structure, with pretraining on historical expert layouts to guide the distribution of sequence-pair choices.

**Workload — the work tested:**

Analog placement instances; circuit sizes, device groups, symmetry/proximity constraints, technology, legalization, routing, extraction and benchmark split are unspecified.

**Hardware and manufacturing assumptions:**

Analog IC placement flow with constraint and parasitic-aware objectives; simulator, extractor, compute platform, search budget, process and layout technology are unspecified.

**Baseline — the comparison method:**

Existing analog placement methods

Heuristic analog placement

Manual placement

Constraint set, search budget, legalization, extraction, simulator and quality boundary are unspecified

**Reported measurements:**

The captured official description qualitatively claims improvement across area, wirelength and post-layout performance; it reports no numeric matching, area, wirelength, parasitic, runtime or yield results.

**Limits on the conclusion:**

A placement assigns blocks or devices to coordinates while preserving constraints. In analog circuits, a short wire or compact bounding box can be harmful if it breaks matching, increases coupling or creates a parasitic that changes the circuit response. The objective must therefore connect placement decisions to the electrical requirements they are meant to protect.

A sequence pair represents relative ordering between rectangular blocks using two permutations. It gives a compact discrete description of non-overlapping placement, but a valid sequence pair still needs coordinate decoding, spacing, symmetry, alignment, legalization and later routing. Relaxing or searching the representation does not guarantee that the final layout satisfies all analog constraints.

Monte Carlo tree search builds a partial decision tree, selects a promising branch, expands it, evaluates a candidate and uses the result to guide later exploration. A two-level search can allocate one level to coarse structural choices and another to detailed sequence-pair choices. The outcome depends on the reward function, simulation cost, exploration policy, random seed, search budget and handling of failed or unrouteable candidates.

Pretraining on expert layouts can bias the search toward sequence-pair distributions observed in historical designs. That can reduce wasted exploration when the new circuit resembles the training set, but it can also encode the biases and technology assumptions of those layouts. Evaluation must separate training and test circuits and show behavior on constraint combinations or topologies not represented in the examples.

The official description says area, wirelength and post-layout performance improve over baselines, but no numeric result, matching statistic, parasitic metric, runtime, search budget, yield or extracted-circuit setup is reported. Geometric improvement therefore does not establish better analog behavior or practical deployment; final placement, routing, extraction and circuit simulation remain required.

**Source and location**

Evidence tier: Primary captured official DAC description only; no full paper extraction, placement search artifact reproduction or independent constraint, routing, parasitic, post layout, runtime and yield validation. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH713)

DAC 2026 official description and data/review-packets/dac-2026-research713.json: MCTS analog placement; hierarchical sequence-pair search; two-level MCTS; pretraining from expert layouts; qualitative area, wirelength and post-layout performance improvement; omitted constraints, numeric metrics, search budget, extraction and validation conditions.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** heuristic analog placement

manual placement

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH713

**Hardware or process assumptions:** Analog IC layout with matching and parasitic-aware objectives; technology and extraction assumptions are unspecified.

**Limits:** No matching, area, wirelength, parasitic, runtime, or yield results are reported.

Search cost may grow rapidly with circuit size.

Official description only; placement claims require extracted-circuit validation.

**Method or artifact:** Monte Carlo tree search enhanced analog placement optimizer.

**Metrics:** Placement quality and search efficiency are claimed qualitatively

**Problem:** Analog placement must satisfy symmetry, matching, proximity, and parasitic constraints in a combinatorial space.

**Workload or benchmark:** Analog layout placement instances; constraints, legalization, and baselines are unspecified.

</details>

<span id="paper-dac-2026-research776"></span>

### Diffsp: Differentiable Sequence Pair-Based Analog Placement

DAC 2026 · Record: `dac-2026-research776`

[Read the step-by-step explanation](#explanation-dac-2026-research776)

**Updated source-backed reading card**

Reviewed 2026-09-08. Reconciles the DiffSP card with the captured official DAC description; explains discrete sequence-pair placement, Gumbel–Sinkhorn relaxation, gradient objectives, MILP legalization and the distinction between relaxed optimization, legal geometry and post-layout circuit behavior.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Sequence-pair placement is discrete, which makes direct gradient optimization difficult, while analog placement needs area, wirelength, symmetry, matching and electrical objectives to be optimized together.

**Mechanism / artifact:**

DiffSP: differentiable sequence-pair analog placement using a smooth relaxation of the sequence-pair constraint graph through Gumbel–Sinkhorn, automatic gradients for area, wirelength and symmetry objectives, followed by MILP-based legalization for exact geometric and symmetry constraints.

**Workload — the work tested:**

Industrial-level OTA placement benchmarks; circuit sizes, topology, constraints, technology, routing, extraction, process corners and train/test split are unspecified.

**Hardware and manufacturing assumptions:**

Analog placement optimization with differentiable geometric/circuit objectives and MILP legalization; simulator, extractor, compute platform, search budget, process, parasitic and solver settings are unspecified.

**Baseline — the comparison method:**

State-of-the-art analog placers

Discrete sequence-pair search

Heuristic or simulated-annealing placement

Constraint, legalization, extraction, runtime and post-layout comparison boundaries are unspecified

**Reported measurements:**

The captured official description qualitatively claims better placement quality and post-layout performance than state-of-the-art analog placers with significantly reduced runtime; no numeric placement, constraint, runtime or circuit-performance results are reported.

**Limits on the conclusion:**

A sequence pair uses two orderings to encode relative positions of blocks. The ordering is discrete: changing one item can change several geometric relationships, so a small numerical gradient is not directly defined on the original representation.

Gumbel–Sinkhorn relaxation replaces a hard permutation or ordering with a smooth approximation that can be differentiated. During optimization the relaxed object may not correspond to a legal discrete placement. The temperature, rounding rule and gap between relaxed and discrete objectives determine whether the optimized result survives conversion.

Area, wirelength and symmetry can be placed in one differentiable objective, but their weights determine the search outcome. A short wirelength can conflict with matching, routing resources or parasitic limits. The optimization must expose objective weights and evaluate the final legalized layout under the actual analog constraints.

MILP legalization enforces exact geometric and symmetry constraints after the relaxed optimization. It can move blocks away from the relaxed solution, make the problem infeasible or consume substantial runtime. The post-legalization objective and any repair cost must be included; legalization is not evidence that the relaxed candidate was already valid.

The description names industrial OTA benchmarks and claims better placement quality, post-layout performance and runtime than state-of-the-art placers, but reports no numeric result, constraint-satisfaction rate, legalization failures, solver budget, extraction setup, parasitic metric or circuit-quality condition. The record establishes a differentiable-placement method, not a demonstrated general analog-circuit advantage.

**Source and location**

Evidence tier: Primary captured official DAC description only; no full paper extraction, differentiable placement or milp artifact reproduction and no independent legalization, post layout, runtime, parasitic or circuit quality validation. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH776)

DAC 2026 official description and data/review-packets/dac-2026-research776.json: discrete sequence-pair limitation; Gumbel–Sinkhorn smooth relaxation of constraint graph; area/wirelength/symmetry gradients; MILP legalization for exact geometry and symmetry; industrial OTA benchmarks; qualitative placement/post-layout/runtime claims; omitted numeric, solver, extraction and constraint conditions.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** discrete sequence-pair search

heuristic analog placement

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH776

**Hardware or process assumptions:** Analog layout optimization with differentiable geometric and circuit objectives; process and extraction assumptions are unspecified.

**Limits:** No placement quality, constraint satisfaction, runtime, or circuit-performance results are reported.

Continuous relaxations may produce hard-to-legalize layouts.

Official description only; claims require post-layout simulation.

**Method or artifact:** Differentiable sequence-pair representation for analog placement optimization.

**Metrics:** Differentiable placement optimization is claimed qualitatively

**Problem:** Discrete sequence-pair placement representations hinder gradient-based optimization of analog layout objectives.

**Workload or benchmark:** Analog placement benchmarks; relaxation, constraint handling, and baselines are unspecified.

</details>

## What remains to establish

Resolve unspecified workloads, comparison methods, resource budgets, and source locations before generalizing a reported gain. Multiple papers in this selected sample permit comparison of mechanisms, but do not by themselves establish recurrence across years or a long-term trend.

[All subthemes](../expanded-taxonomy-v1.md) · [Research directions](../directions/README.md)
