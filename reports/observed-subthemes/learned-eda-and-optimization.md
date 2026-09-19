# Learned EDA and optimization

This subject has 10 records in the selected sample. This page explains where it fits, then presents all captured paper evidence without shortening the measurements or limitations.

[Definitions used in the paper records](../reading-guide-v1.md)

## Understand the parent subject first

- [AI assisted EDA](../themes/ai-assisted-eda.md)

## Where learning enters a design process

Electronic design automation means using software to construct and check electronic hardware. The work includes predicting electrical behavior, choosing circuit parameters, arranging physical structures, and proving functional properties. A learned model can assist any of these tasks, but its role determines what counts as success. A predictor estimates a quantity. A search method proposes a design. A proof assistant proposes information for a checker. These outputs need different validation.

The ten records in this group are a broad collection, not ten examples of one algorithm. Their common motivation is that evaluating every possible choice with detailed tools is expensive. The central tradeoff is whether cheaper guidance reduces total effort without causing the process to accept an invalid design or overlook a useful one.

## Estimating electrical properties before expensive analysis

[Attentioncap](../observed-subthemes/learned-eda-and-optimization.md#paper-dac-2026-research1222) learns a capacitance matrix from layout-related information. Capacitance describes how charge changes with voltage; a matrix represents electrical relationships among multiple conductors. An error in an individual relationship matters through its effect on the subsequent circuit calculation. A low average extraction error would therefore need to be accompanied by evidence about the delays or noise limits the extracted model is used to check. The captured record supplies neither extraction error nor full-chip runtime conditions.

[Epicell](../observed-subthemes/learned-eda-and-optimization.md#paper-dac-2026-research550) combines electrical and physical information to predict standard-cell power, performance, and area. Standard cells are predefined small circuit implementations used to assemble larger designs. Their physical arrangement affects electrical behavior, so considering both sources of information is a plausible modeling choice. It does not establish accuracy across fabrication technologies or operating conditions. The record provides no numerical prediction errors or technology-transfer results.

[Learned-prior multi-corner analysis](../observed-subthemes/learned-eda-and-optimization.md#paper-dac-2026-research1646) addresses repeated analysis under different conditions. A corner is a specified combination of conditions, such as process assumptions, voltage, and temperature. Removing user-facing tuning does not remove assumptions learned from earlier examples. The title's zero-hyperparameter claim must therefore be separated from coverage: which conditions can the method analyze accurately, and what happens outside them? Those results are not exposed in the captured source.

## Choosing feasible designs rather than predicting isolated scores

[Perifi](../observed-subthemes/learned-eda-and-optimization.md#paper-dac-2026-research1804) addresses inverse design for radio-frequency circuits or components: start with desired behavior and seek a physical design that produces it. Its feasible-region sampling focuses on choices expected to satisfy constraints. This may save evaluations, but incorrectly excluding part of the search space can also remove good designs. Frequency bands, fabrication constraints, sample counts, and measured or simulated validation are unspecified here.

[Function-family analog optimization](../observed-subthemes/learned-eda-and-optimization.md#paper-dac-2026-research951) asks whether knowledge transfers among related circuit functions. Related circuits may share useful response patterns, but similarity of function does not establish identical parameter sensitivities. Evaluation must separate reuse on close variants from transfer to a new topology or process. The source does not provide those splits or simulation counts.

[SoberDSE](../observed-subthemes/learned-eda-and-optimization.md#paper-dac-2026-research859) learns which search algorithm to use. This adds a decision above the design search itself. Its total cost includes learning or evaluating the selector as well as running the selected method. A fair comparison would give fixed and selected algorithms the same total evaluation budget on previously unseen design spaces; the captured record does not report such results.

## Proxies, explanations, and changing designs

[ACE-NAS](../observed-subthemes/learned-eda-and-optimization.md#paper-dac-2026-research1899) jointly searches the structure of a spiking neural network and how inputs become events. An inexpensive search score is useful only if it ranks candidates in a way that predicts their eventual trained quality and hardware cost. “Zero-cost” in the title must not be read as free search, training, or execution. The source does not specify the score, target hardware, or measured costs.

[Learning the why](../observed-subthemes/learned-eda-and-optimization.md#paper-dac-2026-research271) proposes causal-aware CPU optimization. An observed association between a design parameter and performance is not enough to show what changing that parameter will do: other parameters or workload choices may have changed with it. Testing controlled design changes is necessary to evaluate a causal interpretation. The record exposes no such validation.

[DiffDEG](../observed-subthemes/learned-eda-and-optimization.md#paper-dac-2026-research692) learns from how a design evolves after layout. The relevant output is not merely a useful representation of edit history, but a better completed design after all resulting checks and repairs. Its captured description gives no final timing, power, area, or total runtime results.

## Learned proof suggestions still require proof

[Legend](../observed-subthemes/learned-eda-and-optimization.md#paper-dac-2026-research523) proposes auxiliary statements, called lemmas, to assist hardware model checking. A suggested statement must be established under the actual model and assumptions before it can support a proof. Prediction confidence is not a substitute. Success should count valid completed proofs and total checking time, including rejected suggestions; the source supplies no proof-success or soundness results.

## The long-term question supported by this group

These records motivate studying the complete chain from learned guidance to independently checked design output. That is a research hypothesis, not evidence of year-over-year adoption or a proven common benefit. The strongest comparison would preserve the same design requirements, charge for data generation and failures, test unfamiliar designs, and report final valid outcomes rather than only intermediate model scores.

<span id="explanation-dac-2026-research1222"></span>

### Attentioncap: a learned capacitance matrix must preserve electrical relationships, not only average prediction error

#### What a capacitance matrix represents

For a group of conductors, the capacitance matrix describes how voltage changes create charge on the conductors. In a simplified linear model, the charge vector is related to the voltage vector by `q = C V`. The diagonal terms describe a conductor's self relationship under the chosen convention. Off-diagonal terms describe coupling between conductors: changing one conductor's voltage can change charge associated with another.

The matrix is not just a list of independent numbers. Its entries are tied to the same three-dimensional geometry, materials, boundary conditions and extraction convention. A prediction that makes one entry accurate while violating symmetry, sign conventions or the expected physical structure can produce an invalid electrical model. The off-diagonal terms must remain tied to the geometry, not treated as unrelated labels. The useful target must therefore be defined together with units, matrix convention, conductor set, window or chip scope and reference solver.

#### What a transformer-based extractor is trying to learn

The method record names a transformer-based learned capacitance-matrix extractor. A transformer processes a set or sequence of input tokens and uses attention to relate them. For layout extraction, tokens could encode shapes, layers, coordinates, materials, neighboring conductors or graph relationships, but the captured source does not specify the representation. The model's value depends on whether its input retains the geometry needed to distinguish nearby conductors, long-range coupling, layer separation and boundary effects.

Full-chip extraction also creates a scale problem. A chip may contain many conductors and repeated local structures. The method must decide whether to process the whole layout, tiles, nets, windows or hierarchical summaries. Tiling reduces memory but can omit long-range effects or create inconsistent values at tile boundaries. Whole-chip attention can preserve broader context but may increase memory and runtime sharply. “Toward full-chip extraction” is therefore an end-to-end systems claim, not only a model-architecture claim.

#### Why average error is not enough

A small mean error can hide large errors in dense regions, high-speed nets, critical clock structures or rare layout patterns. Matrix errors also propagate into delay, noise, signal-integrity and timing calculations, so matrix error must be reported by electrically meaningful category. The assessment should report entry-wise error, row or conductor error, coupling-specific error, worst cases, symmetry or physical-validity violations, and the effect on downstream analysis.

The correct comparison is not only a learned model against labels. It includes the high-fidelity extraction flow, dataset construction, preprocessing, inference, memory and any repair or filtering needed to make the matrix usable. If the model is faster but loses accuracy on a timing-critical coupling term, the engineering conclusion depends on the downstream tolerance rather than the average speedup alone.

#### What technology transfer requires

Capacitance depends on layer stack, dielectric materials, conductor dimensions, spacing rules and boundary conditions. A model trained on one PDK can learn those relationships as fixed patterns. Testing a different node or design style requires held-out technologies or designs, not only random layout windows from the same distribution. The split must also prevent overlapping windows or repeated structures from appearing on both sides.

#### What a complete evaluation needs

Define the conductor and matrix convention, input representation, layout scope, tokenization, attention context, target units, reference extractor, PDKs, mesh or solver settings, train/validation/test split, model size, hardware and inference boundary. Compare conventional parasitic extraction and non-transformer learned extraction with the same geometry, labels, tolerances and compute budget.

Report capacitance MAE and relative error by matrix term and technology, worst-case coupling error, physical-validity violations, coverage, memory, preprocessing cost, inference runtime, full-chip scaling, tiling or batching effects and failure cases. Feed predicted matrices into timing, noise and signal-integrity analysis and report how often the downstream decision changes. Validate on unseen designs and, when transfer is claimed, unseen technology nodes.

The captured official description claims extraction efficiency for a transformer-based method. It reports no capacitance error, coverage, runtime, memory or signoff-correlation result, and the technology, mesh and solver assumptions are unspecified. Learned extraction may be technology-node specific. The evidence supports a learned capacitance-matrix extraction direction, not demonstrated full-chip signoff substitution or general transfer. [Recorded evidence](../observed-subthemes/learned-eda-and-optimization.md#paper-dac-2026-research1222)

<span id="explanation-dac-2026-research1646"></span>

### Learned-prior multi-corner analysis: removing a tuning knob does not remove the conditions that must be covered

#### What a corner means

A circuit is analyzed under a set of conditions rather than one universal operating point. A process corner represents manufacturing variation or a model of device speed. Voltage and temperature change electrical behavior. Libraries, interconnect, aging, clock assumptions and workload can add further cases. A timing or electrical result is meaningful only with the corner, constraints and analysis model named.

Multi-corner analysis repeats an expensive computation across these conditions. The outputs can differ: a fast process at one voltage may expose a hold problem, while a slow process at another voltage may expose a setup problem. A method that works at one corner can fail at another because the ranking of paths, sensitivity of parameters or numerical behavior changes.

#### What a learned prior is doing

A learned prior uses information from earlier examples to guide an analysis. It may select settings, initialize a solver, predict a useful region, approximate a response, or decide which calculations deserve more effort. The captured description calls the result zero-hyperparameter, but it does not specify the prior, its inputs, the decisions it makes, or the analysis it accelerates.

The prior still contains assumptions. Training examples encode a distribution of circuits, PDKs, corners, parameter ranges and solver behavior. If a new design or corner falls outside that distribution, the prior can guide the analysis in the wrong direction or hide an important failure. User-facing tuning and learned tuning are different interfaces for selecting behavior; neither establishes accuracy without coverage tests.

#### Why “zero hyperparameters” needs a precise denominator

A hyperparameter is a user-selected setting that affects model or solver behavior. Removing manual settings may reduce setup work, but it can also move choices into training, architecture, data selection or a fixed default. The evaluation should state which settings are eliminated, which are learned, which remain fixed, and whether data collection or retraining is required for a new design or PDK.

The cost comparison must include the full workflow. If the learned prior needs a dataset, feature extraction, training, calibration or fallback analysis, those costs belong beside the manual-tuning cost. A method can reduce per-corner analysis time while increasing preparation cost, or it can reduce tuning effort while producing more failed or inconclusive corners.

#### What a complete evaluation needs

Define the corner set, circuit and PDK distribution, analysis tool, constraints, prior inputs and outputs, learned training procedure, fixed and learned settings, fallback behavior and stopping rule. Compare manually tuned analysis and default hyperparameters on the same designs, corners, hardware and total evaluation budget. Hold out entire designs and, when claimed, PDKs or corner families; report results on unseen designs separately from familiar designs.

Report analysis error by corner and design, setup and hold or other relevant violations, corner coverage, false passes and false failures, convergence, number of solver calls, preprocessing and training cost, per-corner runtime, total runtime, memory and transfer performance. Inspect whether the prior preserves the worst-case corner rather than improving only the average. Validate final decisions with the reference analysis tool.

The captured official description claims tuning-free multi-corner analysis. It reports no analysis error, runtime, corner coverage or transfer result, and learned priors may encode design or PDK bias. The evidence supports a learned-prior analysis direction, not demonstrated zero-assumption behavior, cross-design robustness or universal replacement of manual tuning. [Recorded evidence](../observed-subthemes/learned-eda-and-optimization.md#paper-dac-2026-research1646)

<span id="explanation-dac-2026-research1804"></span>

### Perifi inverse design: feasible-region sampling saves evaluations only if it does not remove valid solutions

#### What inverse design is solving

Forward design starts with a physical structure and predicts its electrical behavior. Inverse design starts with desired behavior and searches for a structure that produces it. For an RF circuit or component, the desired behavior may include frequency response, gain, impedance, bandwidth, loss, radiation or other requirements. The design variables may describe dimensions, materials, topology or placement.

The simulator maps a candidate design to responses. The inverse problem is difficult because many candidates can produce similar behavior, the response can be nonlinear, and only some candidates satisfy physical and manufacturing constraints. A useful method must find designs that meet the specification and remain valid when checked with the authoritative electromagnetic or circuit simulator.

#### What feasible-region sampling means

The feasible region is the subset of the search space that satisfies constraints. Sampling only this region can reduce expensive simulations by avoiding candidates that are obviously invalid or far from the target. A physics-infused method may use known relationships, parameter bounds, surrogate predictions or constraint checks to guide which candidates are sampled.

The central risk is exclusion. If the feasibility model is wrong, a valid design can be discarded before the expensive simulator sees it. A region can also be feasible for one frequency band, material, process or boundary condition and infeasible for another. The method must distinguish a hard physical constraint, a conservative screening rule and a learned probability of success; they have different failure consequences.

#### Why the sampler must be evaluated as a search policy

Inverse design is judged by completed valid designs, not only by the number of samples. A sampler that uses fewer simulations but misses the best feasible region may be worse than a broader baseline. A sampler may also find a candidate that matches the simulated response while being too sensitive to fabrication variation or too difficult to manufacture.

The comparison therefore needs a fixed simulation budget and a clear accounting of rejected candidates, failed simulations, surrogate training, constraint checks and final verification. The search should be compared with simulation-based optimization and a data-only surrogate on the same design variables, target specifications and starting information. “Data-efficient” must state whether the saved count includes all data used to build the physics or feasible-region prior.

#### What physics infusion can and cannot guarantee

Physics can reduce implausible proposals when the equations, parameterization and boundary conditions are correct. It does not guarantee that the learned model captures every mode, resonance, coupling effect, material variation or fabrication defect. A surrogate trained on one geometry family can be confidently wrong on a new topology or scale.

Fabrication validity is a separate check. A design that satisfies a simulated target may violate minimum dimensions, material limits, tolerances, thermal constraints, packaging constraints or yield requirements. Robust inverse design should evaluate perturbations around the nominal design and compare the result with calibrated simulation or measurement.

#### What a complete evaluation needs

Define the RF target, frequency bands, design variables, topology, materials, simulator, physics constraints, feasible-region construction, sampling policy, surrogate, initial dataset, simulation budget and stopping rule. Compare simulation-based optimization and data-only surrogate design with matched budgets, starting data, hardware and final verification.

Report target error by frequency, constraint violations, number of valid designs, simulator calls, rejected and failed candidates, training and preprocessing cost, runtime, memory, search coverage, sensitivity to seeds and robustness under parameter perturbation. Test unseen geometries, target specifications, frequency bands and process or material conditions. Validate promising designs with high-fidelity electromagnetic simulation and, when claimed, fabrication or measurement.

The captured official description claims inverse-design efficiency through physics-infused, data-efficient feasible-region sampling. It reports no design error, sample count, runtime, yield or measurement result, and feasible-region priors may be device-specific. The evidence supports a constrained RF inverse-design direction, not demonstrated search completeness, fabrication robustness or universal advantage over simulation-based and data-only methods. [Recorded evidence](../observed-subthemes/learned-eda-and-optimization.md#paper-dac-2026-research1804)

<span id="explanation-dac-2026-research1899"></span>

### ACE-NAS: a zero-cost search score is useful only if it predicts trained spiking performance and hardware cost

#### What the joint search is choosing

A spiking neural network has at least two coupled design choices. The architecture defines layers, connections, channels, operations and state. The encoding defines how input values become spikes over time, for example through a rate, latency or event rule. The same architecture can behave differently under a different encoding because spike timing, event count, temporal length and information loss change.

Joint search is therefore not equivalent to choosing an architecture and an encoding independently. An encoding that improves task accuracy may create many events and increase memory traffic. An architecture that looks efficient under one event pattern may be slow or energy-intensive under another. Search must evaluate the combination and preserve the training and inference assumptions used to score it.

#### What “zero-cost” usually needs to distinguish

A zero-cost proxy estimates candidate quality without fully training every candidate. It may use a single forward pass, gradients at initialization, parameter counts, activation statistics, synaptic paths or another inexpensive signal. Avoiding full training can reduce search time, but it does not make the search free. The proxy still requires model construction, data passes, memory, candidate generation, ranking, selected-candidate training and final evaluation.

The proxy is a ranking device, not the task result. It is useful only if candidates ranked highly by the proxy tend to remain strong after normal training and if the ranking reflects the target hardware cost. A proxy can favor a large or expressive model while ignoring event count, temporal steps, memory movement, accelerator support or energy per inference.

#### Why encoding makes the proxy harder

Spikes are discrete events, and their timing affects both computation and information. A rate encoding may produce repeated events over many steps. A latency encoding may use fewer events but place information in timing. The search score must state how the encoding is simulated, how many time steps are used, how gradients or activity statistics are obtained, and whether the proxy sees the same input distribution as final inference.

If the proxy is evaluated at initialization but the final network is trained with a different normalization, surrogate-gradient rule, optimizer or time horizon, the ranking may change. Joint architecture and encoding search should therefore report rank correlation or search regret against fully trained candidates, not only the best proxy score.

#### What hardware-aware validation requires

Spiking hardware may exploit sparse events, but it still pays for memory accesses, routing, state updates, time steps and communication. A model with fewer arithmetic operations can use more memory or emit more events. Hardware support for the selected neuron, synapse, encoding and precision also matters. A task-accuracy result on a simulator is not an area, energy or latency result on an accelerator.

#### What a complete evaluation needs

Define the architecture search space, encoding families, data preprocessing, time horizon, training rule, surrogate gradient, proxy computation, candidate budget, ranking procedure and stopping condition. Compare manual SNN design and conventional NAS with the same search budget, data, training budget and final evaluation. Include the cost of proxy calculation, candidate training and failed candidates.

Report trained accuracy, robustness across seeds, search time, training time, inference latency, event count, memory traffic, energy, area, on-chip storage, temporal steps and hardware utilization. Measure rank correlation between proxy and trained outcomes, search regret, transfer to unseen datasets or architectures, and the effect of changing the target hardware. Validate the selected design on the intended hardware or a calibrated hardware model.

The captured official description claims zero-cost search efficiency for joint spiking architecture and encoding search. It reports no accuracy, search time, energy, area or transfer result, and the proxy, datasets, encodings, search space and target hardware are unspecified. The evidence supports a low-cost SNN search direction, not demonstrated zero-cost behavior, trained-model superiority or hardware efficiency. [Recorded evidence](../observed-subthemes/learned-eda-and-optimization.md#paper-dac-2026-research1899)

<span id="explanation-dac-2026-research271"></span>

### Learning the why: a causal claim requires controlled design changes, not only a predictive association

#### What causal optimization is trying to answer

A predictive model asks: given observed CPU design settings and measured outcomes, what outcome is likely? A causal model asks a different question: if one setting is deliberately changed while the relevant conditions are held fixed, how will the outcome change? The second question is the one needed for optimization, because an optimizer acts by changing settings.

CPU design data can contain many interacting variables: cache sizes, pipeline choices, branch structures, issue width, memory hierarchy, compiler settings, workloads and frequency targets. A setting may appear associated with better performance because it was chosen for an easier workload or a different design family. The association can be useful for prediction while giving the wrong answer about what an intervention will do.

#### What an intervention means

An intervention fixes a design variable to a chosen value and evaluates the resulting design under a specified simulator and workload. The comparison needs a baseline design, the changed design, the constraints held fixed, and the outcome measured. If changing cache size also changes compiler flags, clock target or workload, the result mixes several effects and cannot identify the effect of cache size alone.

The causal question also has a counterfactual form: what would this same design and workload have done under the other setting? Only one version may be observed directly, so the model must rely on assumptions or controlled experiments to estimate the missing outcome. Those assumptions should be stated and tested against held-out interventions.

#### Why correlation can mislead an optimizer

A confounder is a factor that influences both the design choice and the measured result. Workload difficulty can influence the chosen microarchitecture and the reported performance. Design size can influence both cache configuration and power. If the model learns these patterns without separating them, it may recommend a change that looks favorable because the data mixes different conditions.

CPU parameters also interact. A wider issue machine may help one workload and waste power on another. A cache change can alter memory traffic, timing, area and thermal behavior. The intervention must therefore be evaluated across the outcome vector and not only one aggregate score. A causal explanation is useful only if it remains stable when the workload, design family or simulator condition changes within the intended scope.

#### What causal-aware learning can and cannot establish

A causal representation or explanation can identify variables that appear to mediate an outcome, estimate an intervention effect, or guide which design changes to try. It does not automatically prove that the causal assumptions are true. A learned graph can be wrong, an unmeasured confounder can remain, and an effect estimated from one design space can fail in another.

The optimization loop must send proposed changes back through the authoritative CPU simulator or implementation flow. A surrogate score is a screening signal. The final design must be checked for performance, power, area, frequency, correctness and any thermal or architectural constraints, with the full simulation and build cost counted.

#### What a complete evaluation needs

Define the design variables, workloads, simulator, metrics, causal assumptions, intervention set, confounders, training designs, held-out designs and optimization budget. Compare causal-aware learning with a correlation-based surrogate and manual design optimization using the same observations, interventions, simulator calls and compute budget.

Report intervention-effect error, prediction error, PPA, performance by workload, power, area, frequency, robustness across seeds, sample efficiency, runtime, simulator calls and transfer to unseen CPU designs or workloads. Include ablations that remove the causal structure, controlled one-variable changes, multi-variable interactions and cases where the model's proposed intervention fails. Verify every selected design with the authoritative flow.

The captured official description claims explainable optimization efficiency through causal-aware learning. It reports no causal validity, PPA, sample-efficiency, runtime or transfer result, and causal assumptions may not hold across design spaces. The evidence supports a causal-aware CPU-optimization direction, not demonstrated intervention validity or universal advantage over correlation-based and manual optimization. [Recorded evidence](../observed-subthemes/learned-eda-and-optimization.md#paper-dac-2026-research271)

<span id="explanation-dac-2026-research523"></span>

### Legend lemma generation: a useful suggestion must be checked by the proof engine before it counts

#### What hardware model checking is proving

Hardware model checking represents a design as a transition system. The state records values such as registers and memories, the transition relation describes how the design moves from one state to the next, and the property states what must always hold or what must eventually occur. The checker searches this model for a violating execution. If it finds one, the counterexample is evidence against the property under the modeled assumptions. If it proves the property, the proof is valid only for that model, constraints and checker semantics.

A proof can become difficult because the state space is large or because the checker needs intermediate facts to reason about the design. A lemma is an auxiliary statement supplied to help divide or constrain the reasoning. It can expose an invariant, summarize a subsystem or guide a solver, but it is not itself evidence that the target property is true.

#### What data-driven lemma generation is proposing

The Legend record proposes generating lemmas from data. The data might include prior proof attempts, transition-system structure, properties, counterexamples or solver traces, but the captured source does not specify the representation or generation rule. A learned generator can suggest statements likely to help a solver, but it cannot be trusted merely because its confidence is high or because a statement resembles one that worked on another design.

Every generated lemma must be checked under the actual model. If it is an assumption, the flow must make that assumption explicit and prove that it follows from the design or environment constraints. If it is an invariant, the checker must establish the required initial-state and inductive conditions. An unverified lemma can exclude real behaviors and produce a false proof.

#### Efficiency and soundness are separate outcomes

A generator may improve solver time by proposing useful lemmas, but it may also create many rejected, redundant or expensive candidates. Counting generated lemmas is not proof success. Counting a property as solved is valid only when the underlying checker returns a sound result with all assumptions recorded.

The evaluation should separate candidate generation time, lemma-checking time, proof time, timeout, memory and the number of rejected suggestions. It should report whether the final proof result changes, whether counterexamples remain discoverable, and whether the generator helps properties outside its training designs. A faster run that relies on unverified assumptions is not a valid acceleration.

#### What a complete evaluation needs

Define the transition-system representation, property language, solver, lemma format, training data, candidate filter, validation procedure, assumptions, timeout and proof-result semantics. Compare manual lemma generation and solver heuristics with the same designs, properties, resource limits and verification flow.

Report valid completed proofs, soundness checks, counterexample preservation, proof time, total wall-clock time, generation overhead, rejected and redundant lemmas, memory, timeouts and transfer to unseen designs and properties. Include ablations for no generated lemmas, unverified suggestions and different solver backends. Preserve proof certificates or logs so another researcher can inspect what was accepted.

The captured official description claims qualitative lemma-generation efficiency. It reports no proof success, soundness, runtime, generalization or benchmark result, and generated lemmas may be design- or solver-specific. The evidence supports a data-driven proof-assistance direction, not demonstrated sound acceleration or completed-property improvement. [Recorded evidence](../observed-subthemes/learned-eda-and-optimization.md#paper-dac-2026-research523)

<span id="explanation-dac-2026-research550"></span>

### Epicell: electro-physical PPA prediction must connect a cell's geometry to characterized electrical behavior

#### What standard-cell PPA means

A standard cell is a reusable implementation of a logic function with a fixed physical boundary, pins, power connections and a set of characterized electrical views. Power, performance and area are different properties. Area describes physical footprint. Performance can include delay, transition time and timing arcs. Power can include switching power, leakage and internal power under specified input activity, voltage, frequency and temperature.

These quantities are coupled. A wider or stronger transistor can improve drive and delay while increasing capacitance, area and leakage. A compact layout can reduce distance but make pin access, parasitics or power density worse. An accurate predictor must therefore know which electrical and physical information is available and which operating conditions generated the target.

#### What electro-physical co-modeling adds

An electrical-only model may use logical function, transistor sizes or circuit parameters without seeing the layout that determines parasitic resistance and capacitance. A layout-only model may see shapes without knowing the stimulus, load, library function or operating corner. An electro-physical model combines both kinds of information so the prediction can account for the relationship between device structure and physical implementation.

The combined input is not automatically sufficient. The model must represent diffusion, gates, contacts, metal layers, pin locations, power rails, neighboring geometry and any relevant extraction features at a resolution that preserves the effects being predicted. It must also receive activity, load, slew, voltage, temperature and process information when those variables affect PPA.

#### Why PPA averages can mislead

An average error across cells can hide large errors in a timing-critical cell, a high-fanout cell or a rare layout variant. Power error can differ between leakage and switching, and delay error can differ between rise and fall or between setup and hold arcs. A model can rank cells correctly for one use while producing inaccurate absolute values needed for timing closure or power budgeting.

The predictor's intended use must be stated. Early screening tolerates a different error from library replacement, cell sizing, placement optimization or signoff estimation. If the model proposes a cell or design change, that candidate must be characterized or checked by the reference electrical and extraction flow before it is accepted.

#### What technology transfer requires

PPA depends on transistor models, process rules, layer stack, parasitics, voltage, temperature, library conventions and characterization tools. A model trained on one PDK can learn node-specific geometry and electrical patterns. Random splits among cells from the same library test interpolation; they do not establish transfer to a new node, library style, drive strength or process corner.

#### What a complete evaluation needs

Define the cell functions, layout representations, electrical features, PPA targets, units, activity and load conditions, process nodes, PDKs, characterization tool, extraction settings, corners, train/test split and intended use. Compare electrical-only and layout-only models with the same data, compute budget and target definitions.

Report error distributions for area, delay, slew, dynamic power, leakage and internal power, plus rank correlation, worst-case cells, per-corner and per-node results, runtime, memory, training cost and failure cases. Feed predictions into cell selection, timing, power and area decisions and measure downstream changes. Validate selected cells against extracted characterization and, when claimed, silicon or calibrated process data.

The captured official description claims PPA prediction efficiency from electro-physical co-modeling. It reports no PPA error, runtime, technology-transfer or silicon-correlation result, and PDK, characterization and process assumptions are unspecified. The evidence supports an electro-physical standard-cell PPA prediction direction, not demonstrated library replacement, signoff correlation or cross-technology robustness. [Recorded evidence](../observed-subthemes/learned-eda-and-optimization.md#paper-dac-2026-research550)

<span id="explanation-dac-2026-research692"></span>

### DiffDEG: a graph of design changes is useful only if it leads to a better checked post-layout result

#### What post-layout optimization is changing

After placement and routing, an implementation has physical objects, connections, parasitics, timing, power and design-rule status. Post-layout optimization proposes changes to improve one or more outcomes while preserving legality and functional behavior. A change can alter cell sizes, buffering, placement, routing, constraints or another flow-defined object, and each change can affect later checks.

The design is therefore not one static graph. Its cells, nets, geometry, timing relationships and congestion state evolve after every accepted or rejected action. The history can contain which object changed, what the prior state was, what the tool measured, whether the change was reverted and how later repairs responded.

#### What a design-evolution graph represents

A static graph describes one snapshot: nodes may represent cells or nets and edges may represent connectivity. A design-evolution graph adds time or revision information. It can represent states, actions, changed objects, measured outcomes and transitions between successive layouts. A diffusion-enhanced representation, as named by the record, may be intended to propagate information across this evolving structure, but the captured description does not specify the graph construction or diffusion operator.

The representation is not the optimizer by itself. It may predict which action is promising, rank candidate changes, summarize a trajectory or provide a state for a policy. The proposed action still has to pass the implementation flow. A representation that recognizes a common edit pattern can be useful for prediction while failing when a different PDK, netlist, congestion pattern or repair sequence changes the consequences.

#### Why history can matter and can mislead

Two layouts with similar static features can respond differently to the next change because they arrived there through different edits, have different remaining whitespace or have different unresolved timing and routing constraints. History can expose those conditions. It can also create leakage: if train and test trajectories come from the same design or repeated optimization run, the model may memorize the trajectory rather than learn a transferable rule.

An accepted change can improve timing while worsening power, area, congestion or another path. A later repair can undo part of the gain. The useful target must therefore be defined at the completed design level, not only as the immediate reward after one edit. Failed actions and rejected candidates are part of the optimization cost and should not disappear from the training or runtime accounting.

#### What a complete evaluation needs

Define the graph nodes and edges, state representation, revision and action encoding, diffusion or message-passing operation, target outcome, candidate policy, acceptance rule, rollback behavior and implementation flow. Compare static graph learning and heuristic post-layout optimization with the same starting layouts, PDKs, constraints, seeds, tool versions and compute budget.

Report final area, power, timing slack, wirelength, congestion, design-rule violations, unrouted nets, convergence, accepted and rejected actions, rollback count, simulator/tool calls, runtime, memory and total training or inference cost. Separate intermediate prediction quality from final valid design quality. Test unseen netlists, layouts, optimization histories and process conditions, then run extraction, multi-corner timing, power, routing and signoff checks on every selected result.

The captured official description claims post-layout optimization efficiency through diffusion-enhanced design-evolution graph learning. It reports no PPA, timing, convergence, runtime or cross-design result, and graph evolution may be flow-specific. The evidence supports a design-history representation direction, not demonstrated final PPA improvement, transfer or signoff-ready optimization. [Recorded evidence](../observed-subthemes/learned-eda-and-optimization.md#paper-dac-2026-research692)

<span id="explanation-dac-2026-research859"></span>

### SoberDSE: selecting a search algorithm is itself part of the design-space exploration cost

#### What design-space exploration is doing

Design-space exploration evaluates alternative configurations of a system or circuit and compares their objectives. A configuration may include architecture, microarchitecture, physical parameters or tool settings. Each evaluation can require simulation, synthesis, placement, routing or another expensive analysis. The search algorithm decides which configuration to evaluate next from the results already observed.

Different algorithms make different assumptions. Bayesian optimization builds a model of the objective and chooses points using an acquisition rule. Random search samples without learning a response model. Other methods may use evolutionary changes, local search or problem-specific structure. No one algorithm is best for every objective, dimension, noise level, constraint set or evaluation budget.

#### What learning-based algorithm selection adds

SoberDSE places a learned selector above the search algorithm. The selector observes features of a new design space, objective or early evaluations and chooses an algorithm expected to perform well. This can adapt search behavior, but it adds a second learning problem: the selector must recognize which prior spaces resemble the current one and must not consume more resources than it saves.

The selector's training data can contain information about objective shape, dimensionality, constraints, noise, simulator cost and the performance of candidate algorithms. If training and test spaces are too similar, the method may memorize known space families. A selector that chooses well on prior spaces can still fail on a new PDK, topology, objective or scale.

#### Why total budget is the central comparison

The comparison must charge for feature extraction, selector inference, selector training or calibration, pilot evaluations and the evaluations run by the selected algorithm. Giving SoberDSE a larger total budget than a fixed Bayesian optimizer or random search makes a sample-efficiency claim ambiguous. The selected algorithm also needs a fair initialization and stopping rule.

Algorithm selection can fail in two ways. It can choose a poor search method, or it can spend too much budget deciding which method to use. The evaluation should report both the selector decision and the performance of the complete selected pipeline. A good average result can hide catastrophic choices on a subset of design spaces, so worst-case and per-family results matter.

#### What a complete evaluation needs

Define the design-space features, candidate algorithms, selector training data, meta-training/test split, pilot budget, total evaluation budget, objective, constraints, simulator, stopping rule and failure handling. Compare learned selection with fixed Bayesian optimization, random search and any oracle or best-single-algorithm reference under the same total budget.

Report best objective versus evaluations, feasible-design count, constraint violations, selector overhead, pilot cost, total runtime, simulator calls, memory, regret, variance across seeds and performance by unseen design-space family. Use held-out complete design spaces, PDKs or objective families rather than only individual configurations. Include cases where the selector chooses badly and measure whether a fallback protects the search.

The captured official description claims qualitative DSE sample efficiency from learning-based algorithm selection. It reports no objective quality, sample count, runtime, transfer or design result, and algorithm selection may overfit known spaces. The evidence supports a meta-selection direction, not demonstrated total-budget advantage or robust transfer across EDA design spaces. [Recorded evidence](../observed-subthemes/learned-eda-and-optimization.md#paper-dac-2026-research859)

<span id="explanation-dac-2026-research951"></span>

### Function-family analog optimization: shared circuit purpose is not the same as shared design behavior

#### What analog circuit optimization is solving

Analog optimization searches for circuit parameters that produce required electrical behavior. Parameters may include transistor widths and lengths, bias currents, device multiplicities, resistor and capacitor values, compensation elements, matching choices and sometimes the circuit topology itself. Each candidate is normally evaluated by a circuit simulator across operating conditions. The simulator may return gain, bandwidth, phase margin, noise, linearity, output swing, power, area, startup behavior or other quantities.

The task is not simply to predict one score. A useful design must satisfy constraints at the same time. A circuit with high gain but inadequate phase margin is not a valid amplifier. A circuit with low power but poor noise or insufficient bandwidth may not meet its specification. Some candidates also fail to converge in simulation or violate layout, device, voltage or reliability constraints. The optimizer therefore has to search a space containing both feasible and infeasible candidates, while dealing with expensive and sometimes failed evaluations.

#### What a function family means

A function family is a group of circuits related by the function they perform or by a structural description supplied to the method. Examples might include related amplifier functions, current references or converter variants, but the captured source does not define the family boundary. The important question is what is actually shared:

- Two instances may use the same topology with different specifications.
- Two circuits may perform a similar function but use different topologies.
- Two topologies may share device-level structure while having different operating points and constraints.
- Two designs may appear related at the functional level but be implemented in different PDKs, voltage ranges or frequency regimes.

These cases do not provide the same transfer problem. Reusing data from the same topology is easier than proposing a useful starting point for an unseen topology. Transfer across a PDK is harder still because device models, design rules, parasitics, supply limits and available components can change the relationship between parameters and electrical behavior.

#### What the learned method is expected to reuse

The method is described as function-family-aware analog optimization. At a conceptual level, it could reuse a representation of related circuits, a prior over promising parameter regions, a surrogate model, an initialization strategy, a search policy or information about which objectives tend to trade off against each other. The source does not identify which mechanism is used, so those possibilities must not be treated as reported implementation details.

Reuse is valuable only if it reduces the number of expensive simulations without removing good designs. A prior that concentrates search near successful members of a family can reduce early exploration. It can also be wrong when the new circuit has a different topology, a different dominant pole, a different bias regime or a different feasibility boundary. A method must therefore show not only that related data helps on average, but also when the family relation is strong enough to be trusted and when the search falls back to independent exploration.

Similarity of function is not proof that a parameter has the same effect. Increasing a transistor width can improve one circuit's drive strength while worsening another circuit's parasitic capacitance, stability or power. The same parameter can affect different objectives in opposite directions. A family representation may capture correlation between designs, but correlation does not establish the response caused by changing a parameter in the target circuit. The target circuit still requires direct simulation and constraint checking.

#### The splits that distinguish reuse from transfer

An informative evaluation must name the unit that is held out. Randomly splitting individual simulations can place nearly identical circuits in training and test data and make transfer appear stronger than it is. Stronger tests hold out complete target designs, topologies, function families, PDKs or combinations of these.

At minimum, results should separate same-topology specification changes, related-topology transfer, unseen-topology transfer and unseen-process or PDK transfer. The study should also state whether the target family label, topology identifier or simulator-derived features reveal information that would not be available before optimization. If the method receives early target-circuit simulations, those simulations belong in the reported budget; otherwise the comparison is not measuring the cost of obtaining the claimed adaptation.

#### What a fair comparison must measure

The baseline should include independent optimization with no family reuse and a generic Bayesian optimization method if Bayesian optimization is claimed as a comparison. All methods need the same initial information, simulator-call budget, stopping rule, objective normalization and treatment of failed simulations. A method that uses family data should be charged for collecting, cleaning and encoding that data when the baseline does not receive it.

Report the best feasible objective value as a function of simulator calls, not only the final result. Also report the number of valid designs, constraint violations, simulation failures, wall-clock time, model-training cost and variance across random seeds. For analog multiobjective work, state whether the result is a weighted scalar score, a constraint satisfaction rate or a Pareto set. The weights and normalization matter because they can change which design is judged best.

The evaluation should include gain, bandwidth, phase margin, noise, linearity, power and area when those are part of the stated task, together with the actual constraints and operating corners. Final candidates must be rerun with the authoritative simulator and, where claimed, with parasitic extraction, process-voltage-temperature corners, mismatch or Monte Carlo analysis. A family-aware method that finds a promising schematic but fails after extracted parasitics has not demonstrated a deployable analog design.

The captured official description supports a function-family-aware analog optimization direction. It does not specify the family definition, topology relation, PDK, simulator, objective, feasibility rule, split, simulation budget, design error, runtime or transfer result. It therefore supports the hypothesis that related analog functions may provide reusable optimization information, not demonstrated transfer to unseen topologies or processes and not a measured improvement over independent or Bayesian optimization. [Recorded evidence](../observed-subthemes/learned-eda-and-optimization.md#paper-dac-2026-research951)

## Compare the results carefully

## Compare the results carefully

First identify the inputs and required output quality. Then identify the limited resource: time, memory, communication, energy, circuit area, or correctness coverage. Ask which part of the method reduces that cost and which new cost it adds. Compare numbers only when the experiments hold these conditions sufficiently similar.

A conference description may explain the proposal while omitting the full experiment. An author preprint link may have been coded from its abstract. The source classification does not by itself establish that every table was read. Missing locations remain visible below.

## Complete captured evidence

These are evidence records, not substitutes for the explanations above. Each record preserves its problem, proposed method, measurements, comparison conditions, and source limits. A populated record does not establish that its mechanism has been fully explained or independently verified.

<span id="paper-dac-2026-research1222"></span>

### Attentioncap: Transformer Based Capacitance Matrix Learning Toward Full-Chip Extraction

DAC 2026 · Record: `dac-2026-research1222`

[Read the step-by-step explanation](#explanation-dac-2026-research1222)

**Updated source-backed reading card**

Reviewed 2026-09-08. Deepens the existing Attentioncap treatment into a paper-level reading; defines capacitance-matrix relationships, transformer input/context choices, full-chip scaling, matrix and downstream error, technology transfer and signoff requirements.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Full-chip parasitic capacitance extraction is expensive for large designs.

**Mechanism / artifact:**

Transformer-based learned capacitance-matrix extraction method; layout representation, tokenization, attention context, matrix convention, reference solver, tiling, training split and physical-validity constraints are unspecified.

**Workload — the work tested:**

Full-chip layout or parasitic-extraction cases; conductor scope, technology nodes, PDKs, meshes, solvers, designs, matrix targets, split policy and signoff baselines are unspecified.

**Hardware and manufacturing assumptions:**

EDA extraction flow with layout-derived features; PDK, layer stack, materials, mesh, boundary conditions, reference solver, hardware, memory and runtime assumptions are unspecified.

**Baseline — the comparison method:**

Conventional parasitic extraction

Non-transformer learned extractor

Geometry representation, target matrix, solver settings, split, hardware, runtime boundary and downstream checks are unspecified

**Reported measurements:**

Extraction efficiency is claimed qualitatively; no capacitance error, coupling error, physical-validity, coverage, runtime, memory, full-chip scaling or signoff-correlation result is reported.

**Limits on the conclusion:**

A capacitance matrix is a coupled electrical object, not a set of independent labels. Matrix convention, symmetry or sign constraints, geometry scope and reference-solver conditions must be fixed; average entry error can hide invalid or important coupling terms.

Transformer context and full-chip strategy determine whether long-range coupling and boundary effects are represented. Tiling can reduce memory while omitting interactions or introducing boundary inconsistency; whole-chip attention can make memory and runtime the limiting cost.

The official description reports no capacitance error, coverage, runtime, memory or signoff-correlation result, and technology, mesh and solver assumptions are unspecified. Learned extraction may be technology-node specific. The record supports a learned capacitance-matrix extraction direction, not demonstrated full-chip signoff substitution or general transfer.

**Source and location**

Evidence tier: Primary captured official DAC description plus existing chapter level attentioncap discussion; no full paper extraction, reproduced model, downstream signoff validation or cross node transfer experiment. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH1222)

DAC 2026 official description; captured Problem, Mechanism / artifact, Workload, Hardware, Baseline, Measurements and Limits fields; record RESEARCH1222; no manuscript pages.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** conventional parasitic extraction

non-transformer learned extractor

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH1222

**Hardware or process assumptions:** EDA extraction flow with layout-derived features; PDK, mesh, and solver assumptions are unspecified.

**Limits:** No capacitance error, coverage, runtime, memory, or signoff correlation is reported.

Learned extraction may be technology-node specific.

Official description only; full-chip signoff comparison is required.

**Method or artifact:** Transformer-based learned capacitance-matrix extraction method.

**Metrics:** Extraction efficiency is claimed qualitatively

**Problem:** Full-chip parasitic capacitance extraction is expensive for large designs.

**Workload or benchmark:** Full-chip layout or parasitic-extraction cases; technology nodes and signoff baselines are unspecified.

</details>

<span id="paper-dac-2026-research1646"></span>

### Breaking the Tuning Barrier: Zero-Hyperparameters Yield Multi-Corner Analysis Via Learned Priors

DAC 2026 · Record: `dac-2026-research1646`

[Read the step-by-step explanation](#explanation-dac-2026-research1646)

**Updated source-backed reading card**

Reviewed 2026-09-08. Deepens the existing learned-prior multi-corner analysis treatment into a paper-level reading; defines corners, learned assumptions, hyperparameter accounting, full workflow cost, corner coverage and cross-design/PDK validation.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Multi-corner circuit analysis often requires manual tuning and repeated expensive simulations.

**Mechanism / artifact:**

Learned-prior method intended to remove analysis hyperparameter tuning; prior inputs/outputs, training distribution, learned versus fixed settings, analysis surrogate and fallback are unspecified.

**Workload — the work tested:**

Multi-corner circuit or EDA analyses; designs, process/voltage/temperature corners, PDKs, constraints, simulator, training data, splits and baselines are unspecified.

**Hardware and manufacturing assumptions:**

EDA simulation and learned-surrogate flow; PDK, cell/interconnect models, timing constraints, corner definitions, hardware, solver and signoff assumptions are unspecified.

**Baseline — the comparison method:**

Manually tuned analysis

Default hyperparameters

Designs, corner sets, total evaluation budget, preprocessing, training, simulator and reference-analysis conditions are unspecified

**Reported measurements:**

Tuning-free analysis is claimed qualitatively; no analysis error, setup/hold or other violation, corner coverage, false-pass rate, runtime, memory, solver-call count or transfer result is reported.

**Limits on the conclusion:**

A corner is a specified process, voltage, temperature and analysis condition; a learned prior trained on some corners can encode their distribution and fail on unseen designs, PDKs or corner families. Removing a user-facing knob does not remove these assumptions.

The denominator for zero hyperparameters must include training, feature extraction, calibration, fallback and retraining costs. Lower per-corner time does not establish lower total analysis cost or safe coverage.

The official description reports no analysis error, runtime, corner coverage or transfer result. The record supports a learned-prior analysis direction, not demonstrated zero-assumption behavior, cross-design robustness or universal replacement of manual tuning.

**Source and location**

Evidence tier: Primary captured official DAC description plus existing chapter level learned prior discussion; no full paper extraction, cross design/pdk validation or reproduced multi corner analysis. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH1646)

DAC 2026 official description; captured Problem, Mechanism / artifact, Workload, Hardware, Baseline, Measurements and Limits fields; record RESEARCH1646; no manuscript pages.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** manually tuned analysis

default hyperparameters

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH1646

**Hardware or process assumptions:** EDA simulation and learned surrogate flow; PDK and model assumptions are unspecified.

**Limits:** No analysis error, runtime, corner coverage, or transfer results are reported.

Learned priors may encode design or PDK bias.

Official description only; cross-design validation is required.

**Method or artifact:** Learned-prior method intended to remove analysis hyperparameter tuning.

**Metrics:** Tuning-free analysis is claimed qualitatively

**Problem:** Multi-corner circuit analysis often requires manual tuning and repeated expensive simulations.

**Workload or benchmark:** Multi-corner circuit or EDA analyses; designs, corners, and simulator baselines are unspecified.

</details>

<span id="paper-dac-2026-research1804"></span>

### Perifi: physics-Infused RF Inverse Design with Parametric Data-Efficient Feasible-Region Sampling

DAC 2026 · Record: `dac-2026-research1804`

[Read the step-by-step explanation](#explanation-dac-2026-research1804)

**Updated source-backed reading card**

Reviewed 2026-09-08. Deepens the existing Perifi inverse-design treatment into a paper-level reading; defines feasible-region screening, exclusion risk, physics assumptions, simulation-budget accounting, fabrication robustness and transfer tests.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

RF inverse design is expensive when feasible designs occupy a small, physics-constrained region.

**Mechanism / artifact:**

Physics-infused inverse design with data-efficient parametric feasible-region sampling; physics constraints, region construction, surrogate, initial data, sampling policy and final verification are unspecified.

**Workload — the work tested:**

RF components or circuits; target specifications, frequency bands, design variables, topology, materials, simulators, sample budgets, fabrication constraints and baselines are unspecified.

**Hardware and manufacturing assumptions:**

RF process and electromagnetic simulation flow; geometry, material, boundary, packaging, tolerance, thermal and yield assumptions are unspecified.

**Baseline — the comparison method:**

Simulation-based optimization

Data-only surrogate design

Design variables, initial data, simulator fidelity, sample budget, hardware and final verification conditions are unspecified

**Reported measurements:**

Inverse-design efficiency is claimed qualitatively; no design error, valid-design count, sample count, runtime, rejected/failed candidates, robustness, yield or measurement result is reported.

**Limits on the conclusion:**

A feasible-region sampler can save simulator calls only if its constraints and learned screening do not exclude valid solutions. Feasibility can depend on frequency, topology, materials, boundaries and process conditions; a confident prior can be wrong outside its training distribution.

Data efficiency must include all data used for physics or feasible-region modeling, rejected and failed simulations, surrogate training and final verification. Fewer accepted samples alone does not establish a better search if high-quality regions are missed.

The official description reports no design error, sample count, runtime, yield or measurement result, and feasible-region priors may be device-specific. The record supports a constrained RF inverse-design direction, not demonstrated search completeness, fabrication robustness or universal advantage.

**Source and location**

Evidence tier: Primary captured official DAC description plus existing chapter level perifi discussion; no full paper extraction, reproduced RF search, calibrated simulation or fabrication/measurement validation. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH1804)

DAC 2026 official description; captured Problem, Mechanism / artifact, Workload, Hardware, Baseline, Measurements and Limits fields; record RESEARCH1804; no manuscript pages.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** simulation-based optimization

data-only surrogate design

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH1804

**Hardware or process assumptions:** RF process and electromagnetic simulation flow; geometry and material assumptions are unspecified.

**Limits:** No design error, sample count, runtime, yield, or measurement results are reported.

Feasible-region priors may be device-specific.

Official description only; fabrication or calibrated simulation validation is required.

**Method or artifact:** Physics-infused inverse design with data-efficient parametric sampling.

**Metrics:** Inverse-design efficiency is claimed qualitatively

**Problem:** RF inverse design is expensive when feasible designs occupy a small, physics-constrained region.

**Workload or benchmark:** RF components or circuits; frequency bands, simulators, and fabrication constraints are unspecified.

</details>

<span id="paper-dac-2026-research1899"></span>

### ACE-NAS: A Zero-Cost NAS Framework for Co-Design of Architecture and Encoding in Spiking Neural Networks

DAC 2026 · Record: `dac-2026-research1899`

[Read the step-by-step explanation](#explanation-dac-2026-research1899)

**Updated source-backed reading card**

Reviewed 2026-09-08. Deepens the existing ACE-NAS treatment into a paper-level reading; defines joint architecture/encoding choices, zero-cost proxy accounting, spike-event and temporal effects, rank validity, trained-model evaluation and hardware-cost requirements.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Spiking-network architecture and encoding choices interact and make neural architecture search expensive.

**Mechanism / artifact:**

Zero-cost NAS for joint spiking architecture and encoding search; proxy definition, encoding simulation, time horizon, training rule, candidate budget, ranking and target hardware are unspecified.

**Workload — the work tested:**

Spiking neural tasks; datasets, input preprocessing, encoding families, architecture space, time steps, training budget, search candidates and transfer splits are unspecified.

**Hardware and manufacturing assumptions:**

Neuromorphic or event-driven accelerator; event sparsity, memory, state updates, routing, precision, neuron/synapse support, energy and hardware model are unspecified.

**Baseline — the comparison method:**

Manual SNN design

Conventional NAS

Datasets, search/training budgets, proxy cost, seeds, final training, hardware, energy and transfer conditions are unspecified

**Reported measurements:**

Zero-cost search efficiency is claimed qualitatively; no trained accuracy, rank correlation, search regret, search time, training time, event count, energy, area, latency or transfer result is reported.

**Limits on the conclusion:**

Architecture and encoding are coupled: event count, timing, temporal steps and information loss can change the behavior and cost of the same network. A proxy evaluated at initialization or under one time horizon may not rank fully trained candidates correctly.

Zero-cost is not free. Model construction, data passes, proxy computation, candidate ranking, selected-candidate training and final evaluation still consume time and memory; hardware cost also includes events, state, communication and memory traffic.

The official description reports no accuracy, search time, energy, area or transfer result, and the proxy, datasets, encodings, search space and target hardware are unspecified. The record supports a low-cost SNN search direction, not demonstrated zero-cost behavior, trained-model superiority or hardware efficiency.

**Source and location**

Evidence tier: Primary captured official DAC description plus existing chapter level ace nas discussion; no full paper extraction, reproduced search, trained candidate comparison or hardware validation. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH1899)

DAC 2026 official description; captured Problem, Mechanism / artifact, Workload, Hardware, Baseline, Measurements and Limits fields; record RESEARCH1899; no manuscript pages.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** manual SNN design

conventional NAS

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH1899

**Hardware or process assumptions:** Neuromorphic or event-driven accelerator; event and memory assumptions are unspecified.

**Limits:** No accuracy, search time, energy, area, or transfer results are reported.

Zero-cost proxies may mis-rank hardware costs.

Official description only; hardware-aware validation is required.

**Method or artifact:** Zero-cost NAS for joint spiking architecture and encoding search.

**Metrics:** Zero-cost search efficiency is claimed qualitatively

**Problem:** Spiking-network architecture and encoding choices interact and make neural architecture search expensive.

**Workload or benchmark:** Spiking neural tasks; datasets, encodings, search space, and target hardware are unspecified.

</details>

<span id="paper-dac-2026-research271"></span>

### Learning the why: Causal-Aware Learning in Explainable and Efficient CPU Design Optimization

DAC 2026 · Record: `dac-2026-research271`

[Read the step-by-step explanation](#explanation-dac-2026-research271)

**Updated source-backed reading card**

Reviewed 2026-09-08. Deepens the existing Learning the why treatment into a paper-level reading; defines prediction versus intervention, confounding, counterfactuals, CPU design-variable interactions, authoritative validation and causal-transfer tests.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

CPU design optimization needs models that explain causal effects rather than correlating design variables with outcomes.

**Mechanism / artifact:**

Causal-aware learning for explainable CPU optimization; causal representation or graph, intervention data, confounder handling, counterfactual assumptions, surrogate and authoritative validation are unspecified.

**Workload — the work tested:**

CPU microarchitectural or physical-design spaces; design variables, workloads, simulators, metrics, intervention set, training/held-out designs and constraints are unspecified.

**Hardware and manufacturing assumptions:**

CPU design flow with learned surrogate or optimizer; processor model, workload, compiler, simulator, process, frequency, power and implementation assumptions are unspecified.

**Baseline — the comparison method:**

Correlation-based surrogate

Manual design optimization

Design variables, interventions, workloads, simulator calls, PPA metrics, seeds, compute budget and transfer conditions are unspecified

**Reported measurements:**

Explainable optimization efficiency is claimed qualitatively; no intervention-effect error, causal validity, PPA, sample efficiency, runtime, simulator-call count or transfer result is reported.

**Limits on the conclusion:**

A predictive association does not identify the effect of changing a design variable. Workload, design family, compiler settings or size can confound both the selected parameter and the measured outcome; controlled interventions and stated counterfactual assumptions are required.

CPU variables interact across performance, power, area, frequency and thermal behavior. A causal explanation or surrogate must be checked through the authoritative simulator or implementation flow, and a good predicted score does not establish a valid completed design.

The official description reports no causal validity, PPA, sample-efficiency, runtime or transfer result, and causal assumptions may not hold across design spaces. The record supports a causal-aware CPU-optimization direction, not demonstrated intervention validity or universal advantage.

**Source and location**

Evidence tier: Primary captured official DAC description plus existing chapter level causal optimization discussion; no full paper extraction, controlled intervention experiment or reproduced cpu flow validation. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH271)

DAC 2026 official description; captured Problem, Mechanism / artifact, Workload, Hardware, Baseline, Measurements and Limits fields; record RESEARCH271; no manuscript pages.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** correlation-based surrogate

manual design optimization

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH271

**Hardware or process assumptions:** CPU design flow with learned surrogate or optimizer; process and simulation assumptions are unspecified.

**Limits:** No causal validity, PPA, sample efficiency, runtime, or transfer results are reported.

Causal assumptions may not hold across design spaces.

Official description only; intervention and design validation is required.

**Method or artifact:** Causal-aware learning for explainable CPU optimization.

**Metrics:** Explainable optimization efficiency is claimed qualitatively

**Problem:** CPU design optimization needs models that explain causal effects rather than correlating design variables with outcomes.

**Workload or benchmark:** CPU microarchitectural or physical-design spaces; designs, metrics, and simulators are unspecified.

</details>

<span id="paper-dac-2026-research523"></span>

### Legend: A Data-Driven Framework for Lemma Generation in Hardware Model Checking

DAC 2026 · Record: `dac-2026-research523`

[Read the step-by-step explanation](#explanation-dac-2026-research523)

**Updated source-backed reading card**

Reviewed 2026-09-08. Deepens the existing Legend treatment into a paper-level reading; defines transition systems, properties, auxiliary lemmas, soundness, rejected suggestions, proof completion and formal-evaluation requirements.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Hardware model checking can stall when useful auxiliary lemmas are difficult to construct.

**Mechanism / artifact:**

Data-driven lemma generation framework; transition-system representation, property language, lemma format, training data, candidate validation, assumptions, solver and proof semantics are unspecified.

**Workload — the work tested:**

Hardware properties and transition systems; designs, properties, solver backends, training data, proof settings, timeouts and benchmark splits are unspecified.

**Hardware and manufacturing assumptions:**

Formal model-checking flow; RTL or transition-system semantics, proof engines, environmental constraints, memory abstraction and design assumptions are unspecified.

**Baseline — the comparison method:**

Manual lemma generation

Solver heuristics

Designs, properties, resource limits, candidate validation, proof logs and soundness conditions are unspecified

**Reported measurements:**

Lemma-generation efficiency is claimed qualitatively; no valid proof success, soundness, counterexample preservation, runtime, generation overhead, memory, timeout or generalization result is reported.

**Limits on the conclusion:**

A generated lemma is an auxiliary statement, not proof of the target property. If it is unverified or incorrectly assumed, it can exclude real behaviors and produce a false proof; the checker must establish it under the actual model and constraints.

Generation cost and rejected or redundant suggestions belong in the total runtime. More generated lemmas do not imply more completed proofs, and a faster run is not a sound acceleration if assumptions or proof certificates are hidden.

The official description reports no proof success, soundness, runtime, generalization or benchmark result, and generated lemmas may be design- or solver-specific. The record supports a data-driven proof-assistance direction, not demonstrated sound acceleration or completed-property improvement.

**Source and location**

Evidence tier: Primary captured official DAC description plus existing chapter level lemma generation discussion; no full paper extraction, formal reproduction, proof log inspection or soundness validation. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH523)

DAC 2026 official description; captured Problem, Mechanism / artifact, Workload, Hardware, Baseline, Measurements and Limits fields; record RESEARCH523; no manuscript pages.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** manual lemma generation

solver heuristics

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH523

**Hardware or process assumptions:** Formal model-checking flow; proof engines and design assumptions are unspecified.

**Limits:** No proof success, soundness, runtime, generalization, or benchmark results are reported.

Generated lemmas may be design- or solver-specific.

Official description only; formal reproduction is required.

**Method or artifact:** Data-driven lemma generation framework.

**Metrics:** Lemma-generation efficiency is claimed qualitatively

**Problem:** Hardware model checking can stall when useful auxiliary lemmas are difficult to construct.

**Workload or benchmark:** Hardware properties and transition systems; solvers, training data, and proof settings are unspecified.

</details>

<span id="paper-dac-2026-research550"></span>

### Epicell: Electro-Physical Co-Modeling for Standard Cell PPA Prediction

DAC 2026 · Record: `dac-2026-research550`

[Read the step-by-step explanation](#explanation-dac-2026-research550)

**Updated source-backed reading card**

Reviewed 2026-09-08. Deepens the existing Epicell treatment into a paper-level reading; defines standard-cell PPA, electrical/physical feature coupling, target and corner scope, error aggregation, PDK transfer and downstream characterization requirements.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Standard-cell PPA prediction needs both electrical and physical effects early in design.

**Mechanism / artifact:**

Electro-physical co-model for standard-cell PPA prediction; layout representation, electrical features, target definitions, characterization, extraction, corners and transfer protocol are unspecified.

**Workload — the work tested:**

Standard cells and layout variants; cell functions, drive strengths, PDKs, nodes, process corners, loads, activities, characterization tools and benchmark splits are unspecified.

**Hardware and manufacturing assumptions:**

Physical layout and electrical simulation flow; process, transistor models, layer stack, parasitics, voltage, temperature, activity, extraction and characterization assumptions are unspecified.

**Baseline — the comparison method:**

Electrical-only model

Layout-only model

Cell libraries, target units, loads, corners, PDKs, extraction, hardware and downstream validation conditions are unspecified

**Reported measurements:**

PPA prediction efficiency is claimed qualitatively; no area, delay, slew, power, leakage, runtime, technology-transfer, worst-case, downstream or silicon-correlation result is reported.

**Limits on the conclusion:**

PPA is a set of coupled quantities, not one score. A stronger cell can improve delay while increasing capacitance, area, leakage and upstream load; average error can hide failures in timing-critical or high-fanout cells.

Electrical-only and layout-only inputs each omit part of the causal path from device and geometry to characterized behavior. The model must include operating conditions and physical features relevant to the target, and selected cells still require reference characterization before use.

The official description reports no PPA error, runtime, technology-transfer or silicon-correlation result, and PDK, characterization and process assumptions are unspecified. The record supports an electro-physical PPA prediction direction, not demonstrated library replacement, signoff correlation or cross-technology robustness.

**Source and location**

Evidence tier: Primary captured official DAC description plus existing chapter level epicell discussion; no full paper extraction, reproduced characterization, downstream timing/power validation or cross technology experiment. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH550)

DAC 2026 official description; captured Problem, Mechanism / artifact, Workload, Hardware, Baseline, Measurements and Limits fields; record RESEARCH550; no manuscript pages.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** electrical-only model

layout-only model

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH550

**Hardware or process assumptions:** Physical layout and electrical simulation flow; process and parasitic assumptions are unspecified.

**Limits:** No PPA error, runtime, technology transfer, or silicon correlation results are reported.

Models may be node-specific.

Official description only; signoff correlation is required.

**Method or artifact:** Electro-physical co-model for standard-cell PPA prediction.

**Metrics:** PPA prediction efficiency is claimed qualitatively

**Problem:** Standard-cell PPA prediction needs both electrical and physical effects early in design.

**Workload or benchmark:** Standard cells and layout variants; PDK, characterization tools, and nodes are unspecified.

</details>

<span id="paper-dac-2026-research692"></span>

### DiffDEG: Diffusion-Enhanced Design Evolution Graph Representation Learning for Post-Layout Optimization

DAC 2026 · Record: `dac-2026-research692`

[Read the step-by-step explanation](#explanation-dac-2026-research692)

**Updated source-backed reading card**

Reviewed 2026-09-08. Deepens the existing DiffDEG treatment into a paper-level reading; defines post-layout state, design-evolution graphs, action history, representation-versus-optimizer boundaries, leakage risk, rollback cost and final PPA/signoff validation.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Post-layout optimization has sequential design evolution and complex graph changes that static features miss.

**Mechanism / artifact:**

Diffusion-enhanced design-evolution graph representation learning; graph construction, diffusion operator, state/action encoding, target outcome, optimizer, acceptance rule and implementation flow are unspecified.

**Workload — the work tested:**

Post-layout circuit designs; starting layouts, netlists, PPA targets, edit trajectories, PDKs, tools, histories, baselines and cross-design splits are unspecified.

**Hardware and manufacturing assumptions:**

EDA physical-design flow; PDK, placement/routing, parasitic extraction, timing corners, power analysis, design rules and signoff assumptions are unspecified.

**Baseline — the comparison method:**

Static graph learning

Heuristic post-layout optimization

Starting layouts, tool versions, constraints, seeds, accepted/rejected actions, compute budget and final validation flow are unspecified

**Reported measurements:**

Post-layout optimization efficiency is claimed qualitatively; no final PPA, timing slack, congestion, convergence, accepted/rejected action count, runtime, memory or cross-design result is reported.

**Limits on the conclusion:**

A design-evolution graph is a representation of states and changes, not proof that a proposed edit improves the completed design. Later routing, extraction, timing repair or rollback can remove an immediate gain.

Histories from the same design or optimization run can leak into train and test, allowing memorization rather than transfer. Rejected actions and repair cost must remain in the total optimization accounting.

The official description reports no PPA, timing, convergence, runtime or cross-design result, and graph evolution may be flow-specific. The record supports a design-history representation direction, not demonstrated final PPA improvement, transfer or signoff-ready optimization.

**Source and location**

Evidence tier: Primary captured official DAC description plus existing chapter level diffdeg discussion; no full paper extraction, reproduced optimization trajectory or final signoff validation. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH692)

DAC 2026 official description; captured Problem, Mechanism / artifact, Workload, Hardware, Baseline, Measurements and Limits fields; record RESEARCH692; no manuscript pages.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** static graph learning

heuristic post-layout optimization

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH692

**Hardware or process assumptions:** EDA physical-design flow; PDK and signoff assumptions are unspecified.

**Limits:** No PPA, timing, convergence, runtime, or cross-design results are reported.

Graph evolution may be flow-specific.

Official description only; signoff validation is required.

**Method or artifact:** Diffusion-enhanced design-evolution graph representation learning.

**Metrics:** Post-layout optimization efficiency is claimed qualitatively

**Problem:** Post-layout optimization has sequential design evolution and complex graph changes that static features miss.

**Workload or benchmark:** Post-layout circuit designs; layouts, PPA targets, and tools are unspecified.

</details>

<span id="paper-dac-2026-research859"></span>

### Soberdse: Sample-Efficient Design Space Exploration via Learning-Based Algorithm Selection

DAC 2026 · Record: `dac-2026-research859`

[Read the step-by-step explanation](#explanation-dac-2026-research859)

**Updated source-backed reading card**

Reviewed 2026-09-08. Deepens the existing SoberDSE treatment into a paper-level reading; defines design-space exploration, meta-level algorithm selection, selector overhead, total-budget accounting, overfitting to known spaces and held-out-space evaluation.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Design-space exploration is expensive and different spaces favor different search algorithms.

**Mechanism / artifact:**

Learning-based selection of DSE algorithms; design-space features, candidate algorithms, selector training, pilot budget, total budget, fallback and stopping rules are unspecified.

**Workload — the work tested:**

EDA design spaces; objectives, constraints, dimensions, simulators, PDKs, design families, selector training/test spaces and evaluation budgets are unspecified.

**Hardware and manufacturing assumptions:**

EDA optimization flow; PDK, simulation/synthesis cost, hardware, objective noise, constraint handling and evaluation-cost assumptions are unspecified.

**Baseline — the comparison method:**

Fixed Bayesian optimization

Random search

Selector training, feature extraction, pilot evaluations, total budget, stopping rule, simulator and held-out design-space conditions are unspecified

**Reported measurements:**

DSE sample efficiency is claimed qualitatively; no objective quality, feasible-design count, sample count, regret, selector overhead, runtime, simulator calls, variance or transfer result is reported.

**Limits on the conclusion:**

Algorithm selection adds a meta-level cost: feature extraction, selector inference or training, calibration and pilot evaluations consume the same budget needed for design search. A selected algorithm is not an advantage unless the complete pipeline wins under equal total cost.

A selector can memorize known design-space families and fail on a new PDK, topology, objective, dimension or noise pattern. Average performance can hide catastrophic choices; held-out spaces and worst-case results are required.

The official description reports no objective quality, sample count, runtime, transfer or design result, and algorithm selection may overfit known spaces. The record supports a meta-selection direction, not demonstrated total-budget advantage or robust transfer across EDA spaces.

**Source and location**

Evidence tier: Primary captured official DAC description plus existing chapter level soberdse discussion; no full paper extraction, reproduced selector, equal budget comparison or held out space validation. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH859)

DAC 2026 official description; captured Problem, Mechanism / artifact, Workload, Hardware, Baseline, Measurements and Limits fields; record RESEARCH859; no manuscript pages.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** fixed Bayesian optimization

random search

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH859

**Hardware or process assumptions:** EDA optimization flow; PDK and evaluation-cost assumptions are unspecified.

**Limits:** No objective quality, sample count, runtime, transfer, or design results are reported.

Algorithm selection may overfit known spaces.

Official description only; cross-design validation is required.

**Method or artifact:** Learning-based selection of DSE algorithms.

**Metrics:** DSE sample efficiency is claimed qualitatively

**Problem:** Design-space exploration is expensive and different spaces favor different search algorithms.

**Workload or benchmark:** EDA design spaces; objectives, simulators, and design families are unspecified.

</details>

<span id="paper-dac-2026-research951"></span>

### Exploiting Function-Family Structure in Analog Circuit Optimization

DAC 2026 · Record: `dac-2026-research951`

[Read the step-by-step explanation](#explanation-dac-2026-research951)

**Updated source-backed reading card**

Reviewed 2026-09-08. Deepens the existing function-family analog optimization treatment into a paper-level reading; separates reuse from transfer to unseen topologies and PDKs and makes equal-budget, feasibility, corner, Monte Carlo and final-simulation requirements explicit.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Analog circuit optimization can reuse structural knowledge across related circuit functions.

**Mechanism / artifact:**

Function-family-aware analog optimization; family representation, topology relation, transfer mechanism, objective, simulator, feasibility and validation are unspecified.

**Workload — the work tested:**

Analog circuits and design objectives; functions, topologies, PDKs, simulators, operating corners and family/topology/process splits are unspecified.

**Hardware and manufacturing assumptions:**

Analog simulation flow; PDK, device models, parasitics, voltage, temperature, corners, mismatch and hardware assumptions are unspecified.

**Baseline — the comparison method:**

Independent circuit optimization

Generic Bayesian optimization

Equal initial data, simulator budgets, stopping rules, failed-simulation handling and transfer splits are unspecified

**Reported measurements:**

Analog optimization efficiency is claimed qualitatively; no design error, feasible-design count, sample count, runtime, objective/PPA result, transfer result or silicon result is reported.

**Limits on the conclusion:**

Related function families can share structure while parameter sensitivities, feasibility boundaries, operating points and topology behavior differ; family reuse does not establish correct target-circuit response.

Random splits within a family do not prove transfer to an unseen topology or PDK. Evaluation should hold out complete families, topologies and processes and report any target information used during adaptation.

The official description reports no design error, sample count, runtime, transfer or final-circuit result. The record supports a function-family-aware direction, not demonstrated transfer to unseen topologies or processes or measured advantage over independent or Bayesian optimization.

**Source and location**

Evidence tier: Primary captured official DAC description plus existing chapter level function family discussion; no full paper extraction, reproduced optimizer, equal budget comparison or held out topology/pdk validation. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH951)

DAC 2026 official description; captured Problem, Mechanism / artifact, Workload, Hardware, Baseline, Measurements and Limits fields; record RESEARCH951; no manuscript pages.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** independent circuit optimization

generic Bayesian optimization

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH951

**Hardware or process assumptions:** Analog design and simulation flow; process and constraint assumptions are unspecified.

**Limits:** No PPA, yield, simulation count, runtime, or cross-circuit results are reported.

Family structure may not transfer across topologies.

Official description only; circuit and process validation is required.

**Method or artifact:** Function-family-aware analog optimization method.

**Metrics:** Analog optimization efficiency is claimed qualitatively

**Problem:** Analog circuit optimization can reuse structural knowledge across related circuit functions.

**Workload or benchmark:** Analog circuits and design objectives; topologies, PDK, and simulators are unspecified.

</details>

## What remains to establish

Resolve unspecified workloads, comparison methods, resource budgets, and source locations before generalizing a reported gain. Multiple papers in this selected sample permit comparison of mechanisms, but do not by themselves establish recurrence across years or a long-term trend.

[All subthemes](../expanded-taxonomy-v1.md) · [Research directions](../directions/README.md)
