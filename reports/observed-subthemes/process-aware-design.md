# Process aware design

This subject has 7 records in the selected sample. This page explains where it fits, then presents all captured paper evidence without shortening the measurements or limitations.

[Definitions used in the paper records](../reading-guide-v1.md)

## Understand the parent subject first

- [Physical design and manufacturing](../themes/physical-design-and-manufacturing.md)

## Manufacturing assumptions determine which designs are feasible

A circuit layout is a set of shapes that will be turned into physical structures. The manufacturing process constrains permitted dimensions, spacing, layers, materials, and device behavior. A design optimization is meaningful only within those assumptions.

Process-aware design includes those constraints while choosing circuits or geometry. The purpose is to avoid selecting a design that looks favorable under an abstract model but fails after fabrication effects are considered. The quality of the process model is therefore part of the evidence.

## Why changing technology also changes the comparison

A new layer arrangement or connection technology can shorten some paths and change resistance, capacitance, supply delivery, or heat removal. The best circuit organization under one process may not be the best under another. Comparing only one metric can miss a cost shifted to another part of the implementation.

The network-on-chip co-optimization record compares several two-dimensional, three-dimensional, and backside-interconnect schemes using technology-dependent physical modeling. A network on chip connects components within a chip. The captured record indicates that the preferred choice depends on core size, while detailed stack, routing, workload, and manufacturing assumptions remain unresolved. [Recorded evidence](../observed-subthemes/process-aware-design.md#paper-dac-2026-research2290)

This supports examining the circuit and technology jointly. It does not establish that one integration scheme is universally superior or that modeled improvements imply manufacturing yield.

<span id="explanation-dac-2026-research2290"></span>

### DTCO for 3 nm NoCs: process choice changes the link, power and traffic problem together

#### What a network-on-chip link costs

A network-on-chip transfers packets between cores, caches or other components. A long link has resistance and capacitance that affect how quickly a signal can change and how much energy is used to drive it. Repeaters and vias can restore signal quality or cross layers, but they consume area, power and routing resources.

The physical design also needs a power-delivery network. IR drop is the voltage reduction caused by current flowing through the power network. It can reduce circuit speed or operating margin. A process-aware comparison therefore needs more than a wire length: it needs the extracted interconnect, power delivery, voltage, timing, energy and layout constraints used to make the claim.

#### What the co-optimization compares

The record compares four two-dimensional, three-dimensional and backside-interconnect schemes using post-layout extraction, technology-dependent resistance/capacitance, and PDN and IR-drop-aware circuit/system simulation. This is design-technology co-optimization: the interconnect organization and the process assumptions are evaluated together.

The official description reports 53% and 68% lower delay for F3D and B2D, 32% and 63% lower EDP, 2.1× and 3.1× feasible link frequency, and 23% and 35% lower average NoC latency. Each pair remains attached to its named scheme and metric. A feasible link frequency is not CPU performance, and average NoC latency is not the latency of every packet or application.

#### Why traffic and core size change the answer

Latency depends on the number of hops, serialization, routing, queueing, contention and injection rate. A link technology can improve an unloaded path while a hotspot still dominates the application. The best physical arrangement can also change with core size because the ratio of local to global wires, endpoint count and traffic concentration changes.

EDP combines energy and delay within a specified boundary. It does not show whether the design meets thermal limits, whether the package can be assembled, or whether the CPU's application performance improves. The comparison must state whether buffers, routers, repeaters, converters, power delivery, memory traffic and idle power are included.

#### What remains necessary for a process claim

Hold the CPU tile, core count, traffic matrix, routing policy, voltage, frequency target and acceptance criteria fixed while comparing the frontside 2D baseline with F3D and B2D. Report per-flow and average/tail latency, link utilization, throughput, energy, peak power, IR drop, thermal conditions, area, routing violations, process variation, assembly assumptions and yield.

The captured DAC description supports process-aware NoC co-optimization with the reported F3D/B2D delay, EDP, frequency and average-latency results. It does not establish universal technology preference, full-system CPU benefit, manufacturability, thermal feasibility or yield.

[Observed paper card](../observed-subthemes/process-aware-design.md#paper-dac-2026-research2290)

<span id="explanation-iccad-2025-1080"></span>

### RSizing: robust analog sizing is a probability-constrained Pareto search, not a nominal best-point search

#### What analog sizing must decide

Analog circuit sizing chooses device parameters such as transistor dimensions, bias values and compensation values. Several performance measures can conflict: increasing gain can increase current, reducing offset can affect bandwidth, and a design that is best at nominal parameter values may fail when fabrication changes device parameters.

For a design (x), let (y(x)) be the vector of performance values after process variation. A yield requirement asks for the probability that all required specifications are met. RSizing seeks a Pareto set of designs that are not dominated by another design while satisfying a stated yield target. The output is therefore a set of tradeoff choices, not one point that is best on every metric.

#### What the three phases do

The recovered paper first runs nominal multi-objective optimization to find promising regions and prune the design space. It then uses heteroscedastic Gaussian-process models, which allow the variation level to depend on the design point, and Thompson sampling to select limited Monte Carlo simulations. Finally, it performs targeted Monte Carlo refinement and calibrates the model before producing the robust Pareto set.

This structure reduces expensive circuit simulations, but it also creates model-risk boundaries. A surrogate can predict the mean and variation incorrectly in an unexplored region. Process distributions can be skewed or have tails that a Gaussian assumption does not capture. The paper uses an MVaR approximation and explicitly notes that its approximation error is not fully addressed and may introduce bias, especially at lower yield requirements.

#### What the manuscript actually evaluates

The paper evaluates ITC 2017 OPAMP, OSC and PLL circuits with 36, 14 and 77 selected parameters and the listed multi-objective performance measures. Spectre simulations use a TSMC 40 nm process on a machine with an 80-core 2.70 GHz CPU and an A100 GPU. It evaluates yield targets of 97.5%, 99.0% and 99.9%; the variation-aware stage uses 50 Monte Carlo samples, refinement uses 100, 200 or 500 samples by target, and final yield is checked with 1,000 samples.

Table II reports mean, minimum and maximum verified yield. Table III reports yield, hypervolume and runtime for NSGA-II, MARS-NEI and RSizing. Table IV compares RSizing with PVTSizing at three target points. NSGA-II is omitted for PLL because its simulation cost is excessive. These conditions matter: the reported results show behavior under a specific process, circuit suite, simulator and budget, not a general analog-design law.

#### How to interpret yield and runtime

Finite Monte Carlo verification estimates a probability; it does not prove the true yield exactly. A design near a 99.9% threshold needs enough samples and uncertainty reporting to distinguish a true pass from sampling variation. A higher target can move the Pareto set toward safer but lower-performance designs. Runtime also includes different algorithm and baseline budgets, and the PLL comparison omits NSGA-II, so a speed ranking must preserve those conditions.

The page-backed manuscript supports RSizing's robust multi-objective method and its reported OPAMP/OSC/PLL simulations, yield checks, hypervolume and runtime tables. It does not establish transfer to another process node, circuit family, simulator, variation distribution or signoff flow, and it does not remove the stated MVaR approximation or independent-reproduction requirements.

[Observed paper card](../observed-subthemes/process-aware-design.md#paper-iccad-2025-1080)

## Lithography connects an intended shape to a printed shape

Lithography uses a patterned exposure process to define structures during fabrication. The resulting shape can differ from the intended design because of the physical imaging and process behavior. Inverse lithography seeks a mask pattern that will produce the desired result under a stated model.

The generative-reinforcement-learning record proposes learning and refining candidate mask distributions. A model that produces plausible patterns still needs physical evaluation of the printed result and checks on whether the mask can be manufactured. The current description does not establish pattern coverage, process conditions, mask-quality measures, or total training and search cost. [Recorded evidence](../observed-subthemes/process-aware-design.md#paper-dac-2026-research209)

The relevant comparison is the final acceptable pattern under the same process conditions and evaluation budget. Similarity to training examples is a different measurement from successful printing.

<span id="explanation-dac-2026-research209"></span>

### Generative inverse lithography: a plausible mask is not yet a verified printed pattern

#### What inverse lithography is solving

The desired layout describes shapes that should exist after fabrication. Lithography chooses a mask and exposure process that produce those shapes after imaging, resist processing and other physical effects. Inverse lithography works backward: it searches over mask patterns using a model of how a candidate mask becomes a printed pattern.

The objective must therefore be defined at the printed shape, not only at the mask. Useful quantities can include edge-placement error, contour distance, process-window behavior, hotspot count, forbidden geometry and mask complexity. The metric must state the simulator, process conditions, tolerance and whether the final mask satisfies manufacturing rules.

#### What the generative and reinforcement-learning stages do

The recorded method uses style-aware GAN pretraining on design data, followed by policy optimization and imitation-learning fine-tuning over mask distributions. GAN pretraining can produce candidate patterns resembling the training distribution. Policy optimization changes candidates according to a reward. Imitation learning can make the policy follow selected examples or trajectories.

Those stages do not define the physical result without a reward and action space. If the reward measures only image similarity, it can prefer a mask that looks plausible but prints poorly. If the lithography simulator is simplified, the policy may exploit simulator errors. If process constraints are added only after generation, the refinement cost may remove the claimed time benefit.

#### What a complete comparison must measure

Compare conventional inverse-lithography solvers, generative methods and post-generation refinement on the same pattern suite, process model, simulator, compute budget and stopping rule. Report final printed-pattern metrics, edge-placement distributions, process-window or variation behavior, mask-rule violations, hotspot results, simulator calls, training and refinement time, memory and energy.

Test patterns must include shapes and interactions not represented in the training set. The study should separate training, policy-selection and final evaluation patterns, and should test process changes rather than assuming that a policy trained for one node transfers to another. A mask that succeeds in simulation still needs mask-writing and fabrication constraints.

The captured DAC description supports a generative reinforcement-learning direction for inverse lithography. It reports no mask-quality metric, process condition, pattern suite, runtime, simulator cost, policy-training budget, refinement result or yield implication. The evidence supports a search method hypothesis, not demonstrated printed-pattern fidelity, speed or manufacturing benefit.

[Observed paper card](../observed-subthemes/process-aware-design.md#paper-dac-2026-research209)

## Fill changes both manufacturing conditions and electrical behavior

Fill insertion adds material patterns to satisfy density or other manufacturing requirements. Added structures can change electrical coupling near signal wires. Meeting a density rule can therefore affect circuit delay.

The differentiable-fill record combines fill selection with a learned capacitance estimate and an explicit delay objective. Capacitance describes how much charge changes with voltage in the modeled structure. A delay approximation uses those electrical estimates to guide the choice. [Recorded evidence](../observed-subthemes/process-aware-design.md#paper-dac-2026-research648)

The important question is whether the final layout meets both manufacturing rules and timing requirements under an adequate extraction model. The current description does not establish the accuracy of that connection across technologies or the complete final results.

<span id="explanation-dac-2026-research648"></span>

### Differentiable fill insertion: meeting density rules is not the same as preserving signoff delay

#### Why fill affects timing

Fill insertion adds shapes or material to satisfy density rules used by fabrication. Those shapes can change the electric field around signal wires. The result can change self-capacitance, coupling capacitance and the time needed for a driver to charge a wire and its load.

The design must satisfy two different conditions: the layout must meet manufacturing density rules, and the signal paths must meet timing under the declared process and operating corners. A density score or a proxy for capacitance is not a timing-signoff result.

#### What the differentiable method changes

The recorded framework learns a capacitance estimate and optimizes fill with an explicit Elmore-delay objective. Differentiability allows the optimizer to change fill choices using a gradient rather than trying every discrete pattern independently. The method must define the fill representation, density and spacing constraints, training data, reference extractor, coupling model and how discrete legal layouts are produced from the optimization variables.

A learned capacitance model is useful only if its errors do not change the selected fill or the timing decision. A model can be accurate on average while missing a high-coupling net or a layout corner that controls signoff. Elmore delay is an RC approximation; it is not automatically equivalent to a signoff timing engine with distributed wires, coupling, slew, driver resistance, corners and variation.

#### What a complete evaluation must measure

Compare state-of-the-art and proxy-objective fill insertion on the same layouts, density rules, routing, process node, timing paths, extraction corners and stopping budget. Report density compliance, capacitance error against a reference extractor, delay and slack before and after fill, runtime, memory, violations, repair rate and the fraction of paths that change signoff status.

The final selected layouts should be checked with an independent signoff extractor and timing tool. Test layer stacks, coupling patterns, path lengths, congestion, process variation and nodes not used for training. If the method claims manufacturing validity, include design-rule checks and the conditions under which the fill can actually be fabricated.

The captured DAC description supports differentiable fill insertion with learned capacitance and explicit Elmore-delay optimization. It reports no delay, density, capacitance, runtime, design-quality, extraction-error, signoff or cross-node result. The evidence supports an optimization direction, not demonstrated timing closure or manufacturing validity.

[Observed paper card](../observed-subthemes/process-aware-design.md#paper-dac-2026-research648)

<span id="explanation-dac-2026-research1282"></span>

### CPW-SMO: a larger common process window must be measured over a defined pattern set and fidelity rule

#### What source-mask optimization is choosing

Lithography uses a source of illumination and a mask pattern to print a wafer pattern. Source-mask optimization chooses both so that the printed result matches the desired layout. Conventional optimization may work on one source-mask pair at a time. CPW-SMO targets a set of patterns that must share one source while using multiple masks.

A common process window is a region of process conditions, commonly focus and exposure, where every selected pattern remains within a stated print-fidelity limit. The size of that window depends on the pattern set, the error metric, the process axes, the optical and resist model, and the acceptable failure rate. “Nearly two times” is not interpretable until those quantities are named.

#### What the proposed components change

The record describes single-shot set-based generative optimization with attention, parallel simulation, preference-penalty scalarization and SMO-aware gradients. Attention can relate features across patterns. Parallel simulation can evaluate candidates concurrently. Scalarization combines objectives such as fidelity, window size and mask constraints into one optimization signal. The weights determine which pattern or constraint is sacrificed when the objectives conflict.

The source and masks remain coupled. A source that helps one pattern can hurt another, and a mask that compensates for one focus/exposure condition may fail elsewhere. The method must define its action representation, gradient through the simulator or surrogate, mask-writability constraints, process sampling and stopping rule. A generative candidate that scores well in a surrogate still needs physical simulation and manufacturing checks.

#### How to read the reported speedup

The official description reports nearly 2× common process window and approximately 200× runtime speedup. Runtime speedup can arise from parallel hardware, fewer simulator calls, a surrogate, an early stopping rule or a changed fidelity target. The comparison must include training, candidate generation, simulation, refinement, hardware and the same convergence or acceptance criterion.

Evaluate against iterative source-mask optimization on the same pattern set, node, process model, focus/exposure grid, fidelity threshold, mask rules and compute budget. Report per-pattern fidelity, the intersection of all patterns' valid windows, failed patterns, simulator calls, total wall time, hardware, memory and mask-writing constraints. Include unseen critical patterns and process variation.

The captured DAC description supports a set-based generative source/mask optimization direction. It reports no node, pattern count, common-window definition, fidelity constraint, simulator fidelity, runtime hardware, mask-writability result or baseline stopping rule. The nearly-2× and approximately-200× claims are conditional indicators, not established general lithography or manufacturing gains.

[Observed paper card](../observed-subthemes/process-aware-design.md#paper-dac-2026-research1282)

<span id="explanation-dac-2026-research1287"></span>

### Differentiable MDP-ILT: a mask can print the right wafer pattern and still be hard to write

#### Why ILT and mask data preparation interact

Inverse lithography chooses a mask intended to produce a target wafer pattern. Mask data preparation then converts that mask into shapes and shots that a mask-writing system can expose. A curvilinear mask can improve the optical representation but may require more complex geometry, more shot fracturing or a write pattern that violates practical constraints.

The two objectives are related but different. Wafer fidelity measures the printed contour under an optical and resist process. Writability measures whether the mask can be represented, fractured, exposed, inspected and manufactured within beam, dose, geometry, time and cost limits. A disjoint workflow can improve one while damaging the other.

#### What the differentiable MDP-ILT method changes

The record describes a physics-aware differentiable EBL simulator with exact gradients, optical-lithography simulation in the loop and end-to-end shot-parameter co-optimization. The intended benefit is to let changes to mask geometry and shot parameters respond to both wafer-fidelity and mask-writing objectives during one optimization.

The gradient is exact with respect to the implemented simulator, not automatically exact with respect to a physical mask writer. Discrete shot fracturing, variable-shaped-beam constraints, geometry snapping, dose quantization and process variation may require projection or approximation after the gradient step. The final legal mask must be reevaluated through the full optical and EBL path.

#### What a complete evaluation must measure

Compare disjoint fab-ILT/MDP workflows with joint optimization on the same curvilinear pattern set, process node, optical and resist models, EBL calibration, shot constraints, compute budget and stopping rule. Report wafer contour error, edge placement, mask geometry violations, shot count, write time, dose, mask complexity, process window, simulator calls and optimization time.

Use an independent optical model and calibrated EBL model where possible. Test pattern geometries not used in training or tuning, process variation, different shot limits and layouts that make wafer fidelity and writability conflict. A simulation result is not a mask-write or fabrication result.

The captured DAC description supports differentiable joint optimization of wafer pattern fidelity and mask writability. It reports no wafer-error metric, writability metric, shot count, runtime, process window, calibration, mask-write or fabrication result. The evidence supports a co-optimization direction, not demonstrated manufacturability or preserved wafer fidelity on hardware.

[Observed paper card](../observed-subthemes/process-aware-design.md#paper-dac-2026-research1287)

<span id="explanation-dac-2026-research1298"></span>

### FreqSEM: a small edge-placement error requires a calibrated image-to-distance measurement and unseen-tool validation

#### What contour extraction is measuring

An SEM image contains pixel intensities produced by an imaging process. Contour extraction selects the boundary that represents a printed feature. The extracted contour can be compared with a reference contour using edge placement error, but the result depends on how the reference is defined, how the image is calibrated and how annotation uncertainty is handled.

FreqSEM uses frequency-aware FFT decomposition, SEM-adapted SAM2 prompting and feature injection, edge-weighted loss and Sobel-gradient loss. FFT features can expose different spatial-frequency content. A gradient loss can emphasize transitions. These mechanisms can help a model locate edges, but they do not by themselves identify the physical edge when contrast, charging, blur, noise, tool calibration or process variation changes.

#### What the reported EPE values mean

The official description reports EPE mean 0.334 nm and standard deviation 0.661 nm for an 81 nm minimum line width. These numbers must remain tied to the stated image and measurement conditions. A nanometer value requires a pixel-to-distance calibration and a reference contour. The standard deviation is larger than the mean, so the distribution and difficult cases matter; an average alone can hide systematic bias or a subset of bad contours.

The comparison should report baseline EPE values, per-pattern errors, annotation agreement, repeat-image variation, calibration uncertainty, runtime and the fraction of contours meeting a specified tolerance. It should state whether EPE is measured on centerlines, edges, line widths or another convention.

#### What generalization requires

Train and test splits should separate images or patterns in a way that prevents near-duplicate structures from leaking across the boundary. Test on a new SEM session, tool, magnification, process condition, node and line-width range. If the model is used for process control, link contour error to the downstream decision and report whether the extracted result changes that decision.

The captured DAC description supports a frequency-aware SEM contour-extraction direction with the reported EPE values. It does not provide dataset size, annotation uncertainty, baseline values, runtime, calibration, imaging conditions or cross-tool/node generalization. The evidence supports selected metrology results, not validated process-control accuracy or broad transfer.

[Observed paper card](../observed-subthemes/process-aware-design.md#paper-dac-2026-research1298)

## Distinguish prediction, physical verification, and fabrication

A model predicts behavior under assumptions. A physical design-rule check establishes compliance with the rules it implements. Measurement on fabricated devices establishes behavior of those devices under the measurement conditions. These are related steps, but they support different conclusions.

A process-aware method should state which step provides each result. If a learned model substitutes for a physical calculation, compare its errors against an appropriate reference and test whether those errors change the selected design. If the claim concerns yield or variation, include the population and operating conditions needed to assess those quantities.

## The comparison that supports a design decision

Keep input circuits or patterns, manufacturing rules, process models, and acceptance criteria explicit. Compare final valid outcomes, violations, total search cost, and sensitivity to relevant process variation. Include repair and recalibration when changing the process or design family.

The transferable lesson is which physical constraint changes the design choice and how reliably the method accounts for it. A faster approximation or favorable nominal case remains useful evidence, but its claim must retain that narrower scope until broader validation is available.

## Compare the results carefully

First identify the inputs and required output quality. Then identify the limited resource: time, memory, communication, energy, circuit area, or correctness coverage. Ask which part of the method reduces that cost and which new cost it adds. Compare numbers only when the experiments hold these conditions sufficiently similar.

A conference description may explain the proposal while omitting the full experiment. An author preprint link may have been coded from its abstract. The source classification does not by itself establish that every table was read. Missing locations remain visible below.

## Complete captured evidence

These are evidence records, not substitutes for the explanations above. Each record preserves its problem, proposed method, measurements, comparison conditions, and source limits. A populated record does not establish that its mechanism has been fully explained or independently verified.

<span id="paper-dac-2026-research2290"></span>

### Design Technology Co-Optimization for Network on Chip in High Performance CPUs at 3nm Node Using Monolithic 3D and Backside Interconnect Technologies

DAC 2026 · Record: `dac-2026-research2290`

[Read the step-by-step explanation](#explanation-dac-2026-research2290)

**Updated source-backed reading card**

Reviewed 2026-09-08. Deepens the existing process-aware NoC treatment into a paper-level reading; preserves the F3D/B2D quantitative claims and makes RC, PDN, IR drop, traffic, core-size dependence and manufacturing assumptions explicit.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Long global network-on-chip links in many-core CPUs require repeaters and vias that affect delay, energy and power delivery, so the interconnect technology and circuit organization should be chosen together.

**Mechanism / artifact:**

Design-technology co-optimization across four 2D, 3D and backside-interconnect schemes using post-layout extraction, technology-dependent resistance/capacitance, power-delivery-network and IR-drop-aware circuit/system simulation.

**Workload — the work tested:**

ARM Neoverse CSS N2 compute tile and NoC system evaluations across Cortex-A76 through Cortex-N2-sized clusters; traffic matrix, link lengths, process stack, routing rules and workload phases are incompletely specified.

**Hardware and manufacturing assumptions:**

3 nm high-performance CPU clusters with monolithic 3D integration and backside power/signal routing, extracted PDN and RC characteristics; thermal, assembly, yield and exact stack assumptions are unspecified.

**Baseline — the comparison method:**

Conventional frontside 2D NoC implementation

F3D and B2D technology schemes

Core size, traffic, link, process, extraction and system configuration must remain matched

**Reported measurements:**

Official description reports 53% and 68% lower delay for F3D and B2D, 32% and 63% lower EDP, 2.1× and 3.1× feasible link frequency, and 23% and 35% lower average NoC latency; exact measurement boundaries and traffic conditions are not fully specified.

**Limits on the conclusion:**

Resistance and capacitance determine wire delay and energy, while the power-delivery network and IR drop can change the voltage available to the circuit. A technology that shortens a signal path can add routing, thermal, assembly or power-delivery constraints. Post-layout modeling is stronger than an abstract wire estimate, but its extraction and process assumptions define the result.

Average NoC latency depends on traffic, contention, link placement, routing and injection rate. Feasible link frequency is not the same as application throughput or CPU performance, and EDP combines energy and delay only within the stated system boundary.

The official description omits exact process stack, routing rules, traffic workloads, thermal and assembly cost, extraction detail, yield and full-system validation. The reported preference varies with core size, so F3D/B2D gains are conditional technology comparisons rather than universal superiority.

**Source and location**

Evidence tier: Primary captured official DAC description plus existing chapter level process aware noc discussion; no manuscript pages, extracted layout reproduction or manufacturing/yield validation. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH2290&sess=sess169)

DAC 2026 official description; captured Problem, Mechanism / artifact, Workload, Hardware, Baseline, Measurements and Limits fields; record RESEARCH2290; reports F3D/B2D delay, EDP, frequency and average-latency factors.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** conventional frontside 2D NoC implementation

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH2290&sess=sess169

**Hardware or process assumptions:** 3 nm high-performance CPU clusters, monolithic 3D integration, backside power/signal routing, extracted PDN and RC characteristics.

**Limits:** The description omits exact process stack, routing rules, traffic workloads, thermal/assembly cost, and post-layout extraction details.

Technology preference varies by core size; results are not a universal comparison of 2D, 3D, and backside integration.

Official description only; manufacturability, yield, and full-system claims require paper-level verification.

**Method or artifact:** DTCO across four 2D/3D/backside-interconnect schemes with post-layout extraction, technology-dependent RC, PDN, and IR-drop-aware circuit/system simulation.

**Metrics:** 53% and 68% lower delay for F3D and B2D

32% and 63% lower EDP for F3D and B2D

2.1x and 3.1x feasible link frequency

23% and 35% lower average NoC latency

**Problem:** Long global NoC links in many-core CPUs require repeaters and vias that degrade delay and energy, motivating technology-aware interconnect co-design.

**Workload or benchmark:** ARM Neoverse CSS N2 compute tile and NoC system-level evaluations across Cortex-A76 through Cortex-N2-sized clusters; traffic, link lengths, and process details are only partially specified.

</details>

<span id="paper-dac-2026-research209"></span>

### Pushing the Limits of Inverse Lithography with Generative Reinforcement Learning

DAC 2026 · Record: `dac-2026-research209`

[Read the step-by-step explanation](#explanation-dac-2026-research209)

**Updated source-backed reading card**

Reviewed 2026-09-08. Deepens the existing inverse-lithography treatment into a paper-level reading; separates generated-mask distribution quality, policy optimization, printed-pattern fidelity, simulator cost and manufacturability.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Inverse lithography must choose a mask pattern whose printed result matches a desired layout under a physical process model, while the search space is large and refinement can be expensive.

**Mechanism / artifact:**

Style-aware GAN pretraining on design data followed by policy optimization and imitation-learning fine-tuning over mask distributions; reward, simulator, action representation, constraints and refinement schedule are unspecified.

**Workload — the work tested:**

Inverse-lithography mask generation; design-pattern suite, geometry, process node, optical model, resist model, simulator, mask constraints and refinement budget are unspecified.

**Hardware and manufacturing assumptions:**

Semiconductor mask-generation and lithography simulation flow; resolution, exposure, resist, process variation, mask writing, design rules, thermal and manufacturing constraints are unspecified.

**Baseline — the comparison method:**

Conventional inverse-lithography solvers

Generative ILT methods with post-ILT refinement

Pattern suite, process, simulator, compute budget and acceptance metric are unspecified

**Reported measurements:**

Mask quality and optimization/refinement reduction are claimed qualitatively; no printed-pattern metric, process condition, pattern suite, runtime, simulator cost, policy-training budget or yield result is reported.

**Limits on the conclusion:**

Inverse lithography is an optimization problem over a mask. A generated mask is useful only after the lithography and resist model predicts the printed pattern under stated process conditions. Similarity to training patterns or a plausible mask image does not establish contour fidelity, edge placement, hotspot safety or manufacturability.

GAN pretraining can provide a distribution of candidate masks, while policy optimization changes candidates according to a reward and imitation learning can copy selected behavior. The result depends on the reward, action space, simulator fidelity, exploration budget and pattern coverage. A reward that omits a process constraint can optimize the wrong physical outcome.

The official description reports no mask-quality metric, process condition, pattern suite, runtime, policy-training cost, refinement budget, simulator validation or yield implication. The record supports a generative-optimization direction, not demonstrated lithography fidelity, speed or manufacturing benefit.

**Source and location**

Evidence tier: Primary captured official DAC description plus existing chapter level inverse lithography discussion; no full paper extraction, lithography simulation reproduction or manufacturability validation. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH209&sess=sess154)

DAC 2026 official description; captured Problem, Mechanism / artifact, Workload, Hardware, Baseline, Measurements and Limits fields; record RESEARCH209; no manuscript pages.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** conventional inverse-lithography solvers

generative ILT methods with post-ILT refinement

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH209&sess=sess154

**Hardware or process assumptions:** Semiconductor mask-generation and lithography simulation flow; optical model, process conditions, resolution, and manufacturing constraints are unspecified.

**Limits:** No mask-quality metric, process condition, pattern suite, runtime, or policy-training budget is supplied.

GAN distribution quality and manufacturability may depend strongly on training-pattern coverage.

Official description only; lithography fidelity and yield implications require paper-level verification.

**Method or artifact:** Style-aware GAN pretraining on design data followed by policy-optimization and imitation-learning fine-tuning over mask distributions.

**Metrics:** Improved mask quality claimed qualitatively

Reduced optimization/refinement time claimed qualitatively

**Problem:** Inverse lithography is non-convex, and suboptimal training data plus expensive post-generation refinement can leave generative mask solutions in poor local minima.

**Workload or benchmark:** Inverse-lithography mask generation; design patterns, process node, lithography simulator, mask metrics, and refinement budget are unspecified.

</details>

<span id="paper-dac-2026-research648"></span>

### Differentiable Fill Insertion with Explicit Delay Optimization

DAC 2026 · Record: `dac-2026-research648`

[Read the step-by-step explanation](#explanation-dac-2026-research648)

**Updated source-backed reading card**

Reviewed 2026-09-08. Deepens the existing differentiable-fill treatment into a paper-level reading; separates density-rule compliance, learned capacitance prediction, Elmore delay and signoff extraction validity.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Fill insertion adds material to meet manufacturing density rules, but the added structures can change coupling and wire capacitance near signal paths and therefore change delay.

**Mechanism / artifact:**

Differentiable fill-insertion framework with learned capacitance extraction and explicit Elmore-delay optimization; fill representation, density constraints, training data, extraction reference and gradient path are unspecified.

**Workload — the work tested:**

Physical-design fill insertion; layouts, process node, layer stack, routed nets, timing paths, density targets and comparison metrics are unspecified.

**Hardware and manufacturing assumptions:**

Semiconductor interconnect capacitance and delay modeling; extraction tool, routing rules, coupling model, signoff corners, variation and manufacturing rules are unspecified.

**Baseline — the comparison method:**

State-of-the-art fill-insertion methods

Proxy-objective fill optimization

Layout, density, timing, process, extraction and signoff conditions are unspecified

**Reported measurements:**

Significant improvement over state of the art is claimed qualitatively; no delay, density, capacitance, runtime, design-quality, signoff or cross-node result is supplied.

**Limits on the conclusion:**

Fill is not electrically neutral. It changes nearby conductor geometry and dielectric environment, which can change self-capacitance and coupling capacitance. Meeting a density rule is therefore a manufacturing constraint, while meeting delay is an electrical constraint; optimizing one proxy does not establish the other.

A learned capacitance model can make the objective differentiable and reduce repeated extraction cost, but its prediction error matters only through the selected fill and final timing. Elmore delay is an approximation based on a simplified RC network; it must be compared with signoff extraction across relevant paths, layers, corners and coupling conditions.

The official description reports no delay, density, capacitance, runtime, design-quality, extraction-error, signoff or cross-node result. The record supports a differentiable fill-optimization direction, not demonstrated timing closure or manufacturing validity.

**Source and location**

Evidence tier: Primary captured official DAC description plus existing chapter level differentiable fill discussion; no full paper extraction, signoff extraction reproduction or cross node validation. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH648&sess=sess154)

DAC 2026 official description; captured Problem, Mechanism / artifact, Workload, Hardware, Baseline, Measurements and Limits fields; record RESEARCH648; no manuscript pages.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** state-of-the-art fill-insertion methods

proxy-objective fill optimization

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH648&sess=sess154

**Hardware or process assumptions:** Interconnect capacitance and delay modeled for semiconductor physical design; extraction tool, layer stack, routing rules, and signoff conditions are unspecified.

**Limits:** No delay, density, capacitance, runtime, or design-quality values are supplied.

Learned capacitance accuracy and Elmore approximation may not match signoff extraction across nodes.

Official description only; physical-design validity requires paper-level verification.

**Method or artifact:** Differentiable fill-insertion framework with learned capacitance extraction and explicit Elmore-delay optimization.

**Metrics:** Significant improvement over state of the art claimed qualitatively

**Problem:** Traditional fill insertion optimizes density and proxy objectives while remaining misaligned with actual signal delay.

**Workload or benchmark:** Physical-design fill insertion; layouts, process node, density constraints, delay paths, and comparison metrics are unspecified.

</details>

<span id="paper-dac-2026-research1282"></span>

### CPW-SMO: Generating Mask Sets and Common Source for Maximum Common Process Window

DAC 2026 · Record: `dac-2026-research1282`

[Read the step-by-step explanation](#explanation-dac-2026-research1282)

**Updated source-backed reading card**

Reviewed 2026-09-08. Deepens the existing process-aware lithography treatment into a paper-level reading; defines common process window and source/mask co-optimization, and bounds the nearly-2× and approximately-200× claims by pattern, simulator, fidelity and runtime conditions.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Source-mask optimization must choose one illumination source and masks for a set of patterns, while keeping all patterns printable across a shared range of process conditions.

**Mechanism / artifact:**

Single-shot set-based generative source/mask optimization using attention, parallel simulation, preference-penalty scalarization and SMO-aware gradients; pattern representation, simulator, reward weights and stopping rule are unspecified.

**Workload — the work tested:**

Full-chip or critical-pattern common-process-window lithography optimization; pattern count, criticality, node, pitch, process range, mask constraints and fidelity targets are unspecified.

**Hardware and manufacturing assumptions:**

Advanced-node DTCO and source-mask optimization with one common source and multiple masks; optical/resist model, focus/exposure conditions, process variation, simulator hardware and mask-writing limits are unspecified.

**Baseline — the comparison method:**

State-of-the-art source-mask optimization methods

Iterative single-pair source-mask optimization

Pattern set, simulator fidelity, stopping criteria, hardware and comparison budget are unspecified

**Reported measurements:**

Official description reports nearly 2× common process window and approximately 200× runtime speedup; process-window definition, pattern/fidelity conditions, simulator hardware and baseline stopping rule are unspecified.

**Limits on the conclusion:**

A common process window is the range of process conditions, such as focus and exposure, over which all selected patterns meet a stated print-fidelity requirement. Improving the window requires defining the patterns, acceptable error, process axes and whether the source is fixed across masks.

Source and mask are coupled: source shape affects how the mask prints, and each mask may need to compensate for the same source across different patterns. Parallel simulation can reduce wall time only if simulator work and hardware are counted consistently. Preference-penalty scalarization depends on weights and can trade one pattern or metric against another.

The official description reports no node, pattern count, process-window definition, fidelity constraint, simulator fidelity, runtime hardware, mask-writability result or baseline stopping rule. The nearly-2× and approximately-200× claims are conditional indicators, not established general lithography or manufacturing gains.

**Source and location**

Evidence tier: Primary captured official DAC description plus existing process aware lithography discussion; no manuscript pages, simulator reproduction or mask/fabrication validation. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH1282&sess=sess154)

DAC 2026 official description; captured Problem, Mechanism / artifact, Workload, Hardware, Baseline, Measurements and Limits fields; record RESEARCH1282; official page reports nearly 2× CPW and approximately 200× runtime.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** state-of-the-art source-mask optimization methods

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH1282&sess=sess154

**Hardware or process assumptions:** Advanced-node DTCO and source-mask optimization with common source and multiple masks; optical model, resist/process assumptions, and compute platform are unspecified.

**Limits:** The description omits node, pattern count, process-window definition, fidelity constraints, and runtime hardware.

Speedup and CPW comparisons may depend on simulator fidelity and baseline stopping criteria.

Official description only; reported gains require paper-level verification.

**Method or artifact:** Single-shot set-based generative source/mask optimization with attention, parallel simulation, preference-penalty scalarization, and SMO-aware gradients.

**Metrics:** Nearly 2x common process window

Approximately 200x runtime speedup

**Problem:** Conventional source-mask optimization iteratively produces a single pair and does not efficiently co-optimize critical pattern sets under a common source.

**Workload or benchmark:** Full-chip or critical-pattern common-process-window lithography optimization; pattern sets, node, simulator, and mask constraints are unspecified.

</details>

<span id="paper-dac-2026-research1287"></span>

### From Fab to Mask Shop: A Differentiable MDP-ILT Framework for Co-Optimization of Wafer Pattern Fidelity and Mask Writability

DAC 2026 · Record: `dac-2026-research1287`

[Read the step-by-step explanation](#explanation-dac-2026-research1287)

**Updated source-backed reading card**

Reviewed 2026-09-08. Deepens the existing inverse-lithography/MDP treatment into a paper-level reading; separates wafer pattern fidelity from mask writability and makes EBL shot, gradient, simulator calibration and fabrication evidence explicit.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Inverse lithography can optimize the wafer pattern while a separate mask-data-preparation flow produces a mask that is costly or difficult to write, causing the two objectives to conflict.

**Mechanism / artifact:**

Physics-aware differentiable electron-beam-lithography simulation with exact gradients, optical-lithography simulation in the loop and end-to-end shot-parameter co-optimization for curvilinear ILT and variable-shaped-beam mask preparation.

**Workload — the work tested:**

Curvilinear inverse-lithography and variable-shaped-beam mask preparation; pattern suite, process node, geometry, shot count, resist/optical conditions and acceptance targets are unspecified.

**Hardware and manufacturing assumptions:**

Optical lithography and EBL mask-writing models with shot fracturing and geometry-level mask-process correction; EBL calibration, beam settings, write time, mask rules and simulator settings are unspecified.

**Baseline — the comparison method:**

Disjoint fab ILT and mask-shop MDP workflows

Separate wafer-fidelity optimization and mask-writability optimization

Pattern, process, simulator, shot, runtime and acceptance conditions are unspecified

**Reported measurements:**

Improved mask manufacturability and preserved wafer pattern fidelity are claimed qualitatively; no wafer error, writability metric, shot count, runtime, process window, write time or calibration result is provided.

**Limits on the conclusion:**

Wafer pattern fidelity asks whether the printed wafer contour matches the target. Mask writability asks whether the mask can be fractured, written and manufactured within beam, geometry, dose and shot constraints. Optimizing one does not guarantee the other; the joint objective and its weights must be stated.

Differentiability can propagate a gradient through a simulated EBL and optical process, but exact gradients of a simulator are exact only for that simulator. Discrete shot fracturing, geometry rules and process effects may need approximations or projection steps that change the final mask.

The official description reports no wafer-error metric, writability metric, shot count, runtime, process window, physical EBL calibration, mask-write experiment or fabrication result. The record supports a joint differentiable optimization direction, not demonstrated manufacturability or preserved wafer fidelity on hardware.

**Source and location**

Evidence tier: Primary captured official DAC description plus existing process aware lithography discussion; no full paper extraction, ebl calibration, mask write or fabrication validation. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH1287&sess=sess154)

DAC 2026 official description; captured Problem, Mechanism / artifact, Workload, Hardware, Baseline, Measurements and Limits fields; record RESEARCH1287; no manuscript pages.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** disjoint fab ILT and mask-shop MDP workflows

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH1287&sess=sess154

**Hardware or process assumptions:** Optical lithography and EBL mask-writing models with shot fracturing and geometry-level mask-process correction; process calibration and simulator settings are unspecified.

**Limits:** No numeric wafer error, writability, shot count, runtime, or process-window results are provided.

Differentiable simulator fidelity and calibration to physical EBL are unresolved.

Official description only; no independent fabrication or mask-write validation.

**Method or artifact:** Physics-aware differentiable EBL simulation with exact gradients, optical-lithography simulation in the loop, and end-to-end shot-parameter co-optimization.

**Metrics:** Improved mask manufacturability and preserved wafer pattern fidelity claimed qualitatively

**Problem:** Disjoint inverse-lithography and mask-data-preparation workflows can optimize wafer fidelity and mask manufacturability inconsistently.

**Workload or benchmark:** Curvilinear inverse-lithography and variable-shaped-beam mask preparation; pattern suite, process node, and shot counts are unspecified.

</details>

<span id="paper-dac-2026-research1298"></span>

### FreqSEM: Frequency-Aware High-Precision Contour Extraction for Lithographic SEM Images

DAC 2026 · Record: `dac-2026-research1298`

[Read the step-by-step explanation](#explanation-dac-2026-research1298)

**Updated source-backed reading card**

Reviewed 2026-09-08. Deepens the existing FreqSEM treatment into a paper-level reading; separates image-feature extraction, contour annotation, EPE calibration and model generalization from the reported nanometer values.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Lithographic SEM images can have low contrast, noise and complex structures, making it difficult to locate the printed contour accurately for metrology and process control.

**Mechanism / artifact:**

Frequency-aware FFT decomposition with SEM-adapted SAM2 prompting and feature injection, edge-weighted loss and Sobel-gradient loss; model input, prompt construction, labels, calibration and training protocol are unspecified.

**Workload — the work tested:**

Lithographic SEM contour extraction with an 81 nm minimum line width and limited training data; dataset size, annotation process, imaging conditions, tool variation and cross-node test are unspecified.

**Hardware and manufacturing assumptions:**

SEM-based lithographic metrology and image-analysis pipeline; pixel scale, magnification, calibration, process node, noise, imaging settings and inference hardware are unspecified.

**Baseline — the comparison method:**

Existing contour-extraction approaches

Baseline model names, annotation protocol, image tool, calibration and runtime conditions are unspecified

**Reported measurements:**

Official description reports EPE mean 0.334 nm, EPE standard deviation 0.661 nm and an 81 nm minimum line width; dataset, annotation uncertainty, calibration and baseline values are not reported.

**Limits on the conclusion:**

Contour extraction maps image intensities to a geometric boundary. FFT decomposition can separate frequency components and Sobel loss can emphasize gradients, but these design choices do not define the physical edge or remove SEM noise and charging. SAM2 prompting and feature injection must be tied to the image scale and label convention.

Edge placement error is meaningful only relative to a calibrated pixel-to-length conversion, reference contour, annotation uncertainty and measurement repeatability. A sub-nanometer mean with a larger standard deviation may hide difficult structures or systematic bias, and the number cannot be compared across tools without matching conventions.

The official description supplies no dataset size, annotation uncertainty, baseline values, runtime, calibration, imaging conditions or cross-node/tool generalization. The record supports a frequency-aware metrology direction and selected EPE figures, not validated process-control accuracy or broad transfer.

**Source and location**

Evidence tier: Primary captured official DAC description plus existing process aware metrology discussion; no full paper extraction, calibrated sem reproduction or cross tool/node validation. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH1298&sess=sess160)

DAC 2026 official description; captured Problem, Mechanism / artifact, Workload, Hardware, Baseline, Measurements and Limits fields; record RESEARCH1298; official page reports 0.334 nm mean, 0.661 nm standard deviation and 81 nm line width.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** existing contour-extraction approaches

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH1298&sess=sess160

**Hardware or process assumptions:** SEM-based lithographic metrology and image-analysis pipeline; imaging conditions, process node, pixel scale, and inference hardware are unspecified.

**Limits:** No dataset size, annotation uncertainty, baseline values, runtime, or generalization across nodes is supplied.

Nanometer EPE depends on calibration and measurement conventions that are not described.

Official description only; metrology validity requires paper-level verification.

**Method or artifact:** Frequency-aware FFT decomposition, SEM-adapted SAM2 prompting and feature injection, edge-weighted loss, and Sobel gradient loss.

**Metrics:** EPE mean 0.334 nm

EPE standard deviation 0.661 nm

81 nm minimum line width

**Problem:** Low contrast, noise, and complex structures in lithographic SEM images make precise contour extraction difficult for metrology and process optimization.

**Workload or benchmark:** Lithographic SEM contour extraction at an 81 nm minimum line width with limited training data; dataset, annotation, and cross-tool conditions are unspecified.

</details>

<span id="paper-iccad-2025-1080"></span>

### RSizing: Robust Bayesian Optimization for Analog Circuit Sizing Under Process Variations

ICCAD 2025 · Record: `iccad-2025-1080`

[Read the step-by-step explanation](#explanation-iccad-2025-1080)

**Updated source-backed reading card**

Reviewed 2026-09-08. Adds a page-backed RSizing reading from the recovered author PDF; explains robust Pareto optimization, heteroscedastic process variation, MVaR approximation, Monte Carlo budgets and the yield/runtime tradeoff rather than retaining the shallow card.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Analog circuit sizing must choose device parameters that trade several performance objectives while meeting a probability-of-success requirement under process variation.

**Mechanism / artifact:**

Three-phase robust Bayesian optimization: nominal multi-objective pruning, heteroscedastic Gaussian-process modeling with Thompson sampling and targeted Monte Carlo refinement/calibration; the recovered paper defines a robust Pareto set using a yield constraint.

**Workload — the work tested:**

ITC 2017 OPAMP, OSC and PLL benchmark circuits with 36, 14 and 77 selected parameters and the listed circuit objectives; Spectre simulations use TSMC 40 nm. Yield targets are 97.5%, 99.0% and 99.9%.

**Hardware and manufacturing assumptions:**

Spectre analog simulation on TSMC 40 nm; 80-core 2.70 GHz CPU and A100 80 GB machine; 50 Monte Carlo samples in variation-aware optimization and 100/200/500 refinement samples for the three yield targets, with final verification by 1,000 samples.

**Baseline — the comparison method:**

NSGA-II

MARS-NEI

PVTSizing

NSGA-II is omitted for PLL because of simulation cost; baseline budgets and objective constructions are not fully symmetric

**Reported measurements:**

Manuscript-backed: Table II verifies mean/min/max yield over 1,000 Monte Carlo samples; Table III reports yield, hypervolume and runtime for OPAMP/OSC/PLL at 97.5%, 99.0% and 99.9%; Table IV compares PVTSizing and RSizing at three targets. The paper notes MVaR approximation bias for lower yield requirements and tradeoffs between target yield and performance.

**Limits on the conclusion:**

A robust Pareto solution is not one design that maximizes every metric. It is a set of non-dominated designs whose probability of meeting the performance specifications is at least the required yield. The yield estimate is itself uncertain when based on finite Monte Carlo samples, especially near a threshold.

The heteroscedastic GP models input-dependent variation and the acquisition function chooses expensive simulations, but the model can be wrong when distributions are non-Gaussian or local variation changes. The paper's refinement uses MVaR estimates and states that approximation error is not fully addressed and may bias results at lower yield.

The recovered experiment is strong page-backed evidence under TSMC 40 nm, ITC 2017 circuits, stated simulation budgets and a specific machine. It does not establish transfer to other nodes, circuits, simulators, variation distributions or commercial signoff. Runtime comparisons also need the asymmetric PLL omission and different baseline budgets kept visible.

**Source and location**

Evidence tier: Primary author hosted manuscript backed selected evaluation; page level extraction performed 2026 09 08; independent reproduction and broader technology/circuit validation remain open. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://www.cse.cuhk.edu.hk/~byu/papers/C287-ICCAD2025-RSizing.pdf)

Recovered author-hosted PDF v1, pages 1–7; Sections II–IV; Fig. 2; Table I (page 6), Tables II–IV (page 7); TSMC 40 nm, ITC 2017 OPAMP/OSC/PLL, yield targets, Monte Carlo budgets and baseline settings.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** high_primary_author_pdf

**Baselines:** existing analog circuit sizing and Bayesian-optimization methods

**Evidence locators:** Not established in the captured evidence.

**Evidence url:** https://www.cse.cuhk.edu.hk/~byu/papers/C287-ICCAD2025-RSizing.pdf

**Hardware or process assumptions:** CMOS analog circuit sizing and Monte Carlo process-variation simulation; exact technology node, circuit identities, and simulation budgets require full-paper extraction.

**Limits:** The evidence is an author-hosted conference PDF; the repository has not yet extracted numerical table values, exact baselines, technology assumptions, or all yield/quality tradeoffs.

**Method or artifact:** Three-phase robust Bayesian optimization using nominal-region pruning, heteroscedastic Gaussian-process surrogate models, Thompson sampling, targeted Monte Carlo simulations, and model calibration.

**Metrics:** yield requirement satisfaction

multiple analog performance objectives

Monte Carlo simulation/computational cost

**Problem:** Analog circuit sizing under process variation is expensive and manual; nominal optimization can produce designs with poor yield when performance distributions shift across manufacturing variation.

**Workload or benchmark:** Three analog benchmark circuits evaluated under process variation with multi-objective performance and yield requirements.

</details>

## What remains to establish

Resolve unspecified workloads, comparison methods, resource budgets, and source locations before generalizing a reported gain. Multiple papers in this selected sample permit comparison of mechanisms, but do not by themselves establish recurrence across years or a long-term trend.

[All subthemes](../expanded-taxonomy-v1.md) · [Research directions](../directions/README.md)
