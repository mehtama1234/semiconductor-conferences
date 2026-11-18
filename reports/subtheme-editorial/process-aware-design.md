## Manufacturing assumptions determine which designs are feasible

A circuit layout is a set of shapes that will be turned into physical structures. The manufacturing process constrains permitted dimensions, spacing, layers, materials, and device behavior. A design optimization is meaningful only within those assumptions.

Process-aware design includes those constraints while choosing circuits or geometry. The purpose is to avoid selecting a design that looks favorable under an abstract model. Such a design may fail after fabrication effects are considered. The quality of the process model is therefore part of the evidence.

## Why changing technology also changes the comparison

A new layer arrangement or connection technology can shorten some paths and change resistance, capacitance, supply delivery, or heat removal. The best circuit organization under one process may not be the best under another. Comparing only one metric can miss a cost shifted to another part of the implementation.

The network-on-chip co-optimization record compares several two-dimensional, three-dimensional, and backside-interconnect schemes using technology-dependent physical modeling. A network on chip connects components within a chip. The captured record indicates that the preferred choice depends on core size. Detailed stack, routing, workload, and manufacturing assumptions remain unresolved. [Recorded evidence](../observed-subthemes/process-aware-design.md#paper-dac-2026-research2290)

This supports examining the circuit and technology jointly. It does not establish that one integration scheme is universally superior or that modeled improvements imply manufacturing yield.

<span id="explanation-dac-2026-research2290"></span>

### DTCO for 3 nm NoCs: process choice changes the link, power and traffic problem together

#### What a network-on-chip link costs

A network-on-chip transfers packets between cores, caches or other components. A long link has resistance and capacitance. These affect how quickly a signal can change and how much energy is used to drive it. Repeaters and vias can restore signal quality or cross layers, but they consume area, power and routing resources.

The physical design also needs a power-delivery network. IR drop is the voltage reduction caused by current flowing through the power network. It can reduce circuit speed or operating margin. A process-aware comparison therefore needs more than a wire length. It needs the extracted interconnect, power delivery, voltage, timing, energy and layout constraints used to make the claim.

#### What the co-optimization compares

The record compares four two-dimensional, three-dimensional and backside-interconnect schemes using post-layout extraction, technology-dependent resistance/capacitance, and PDN and IR-drop-aware circuit/system simulation. This is design-technology co-optimization: the interconnect organization and the process assumptions are evaluated together.

The official description reports 53% and 68% lower delay for F3D and B2D. It reports 32% and 63% lower EDP, and 2.1× and 3.1× feasible link frequency. It also reports 23% and 35% lower average NoC latency. Each pair remains attached to its named scheme and metric. A feasible link frequency is not CPU performance. Average NoC latency is also not the latency of every packet or application.

#### Why traffic and core size change the answer

Latency depends on the number of hops, serialization, routing, queueing, contention and injection rate. A link technology can improve an unloaded path while a hotspot still dominates the application. The best physical arrangement can also change with core size. This is because the ratio of local to global wires, endpoint count and traffic concentration changes.

EDP combines energy and delay within a specified boundary. It does not show whether the design meets thermal limits. It does not show whether the package can be assembled. It also does not show whether the CPU's application performance improves. The comparison must state whether buffers, routers, repeaters, converters, power delivery, memory traffic and idle power are included.

#### What remains necessary for a process claim

Hold the CPU tile, core count, traffic matrix, routing policy, voltage, frequency target and acceptance criteria fixed. Do this while comparing the frontside 2D baseline with F3D and B2D. Report per-flow and average/tail latency, link utilization, throughput, energy, peak power, IR drop, and thermal conditions. Also report area, routing violations, process variation, assembly assumptions and yield.

The captured DAC description supports process-aware NoC co-optimization with the reported F3D/B2D delay, EDP, frequency and average-latency results. It does not establish universal technology preference, full-system CPU benefit, manufacturability, thermal feasibility or yield.

[Observed paper card](../observed-subthemes/process-aware-design.md#paper-dac-2026-research2290)

<span id="explanation-iccad-2025-1080"></span>

### RSizing: robust analog sizing is a probability-constrained Pareto search, not a nominal best-point search

#### What analog sizing must decide

Analog circuit sizing chooses device parameters such as transistor dimensions, bias values and compensation values. Several performance measures can conflict. Increasing gain can increase current, and reducing offset can affect bandwidth. A design that is best at nominal parameter values may fail when fabrication changes device parameters.

For a design (x), let (y(x)) be the vector of performance values after process variation. A yield requirement asks for the probability that all required specifications are met. RSizing seeks a Pareto set of designs that are not dominated by another design while satisfying a stated yield target. The output is therefore a set of tradeoff choices, not one point that is best on every metric.

#### What the three phases do

The recovered paper first runs nominal multi-objective optimization to find promising regions and prune the design space. It then uses heteroscedastic Gaussian-process models, which allow the variation level to depend on the design point. It also uses Thompson sampling to select limited Monte Carlo simulations. Finally, it performs targeted Monte Carlo refinement and calibrates the model before producing the robust Pareto set.

This structure reduces expensive circuit simulations, but it also creates model-risk boundaries. A surrogate can predict the mean and variation incorrectly in an unexplored region. Process distributions can be skewed or have tails that a Gaussian assumption does not capture. The paper uses an MVaR approximation. It explicitly notes that its approximation error is not fully addressed. The error may introduce bias, especially at lower yield requirements.

#### What the manuscript actually evaluates

The paper evaluates ITC 2017 OPAMP, OSC and PLL circuits with 36, 14 and 77 selected parameters. It also evaluates the listed multi-objective performance measures. Spectre simulations use a TSMC 40 nm process. They run on a machine with an 80-core 2.70 GHz CPU and an A100 GPU. It evaluates yield targets of 97.5%, 99.0% and 99.9%. The variation-aware stage uses 50 Monte Carlo samples. Refinement uses 100, 200 or 500 samples by target. Final yield is checked with 1,000 samples.

Table II reports mean, minimum and maximum verified yield. Table III reports yield, hypervolume and runtime for NSGA-II, MARS-NEI and RSizing. Table IV compares RSizing with PVTSizing at three target points. NSGA-II is omitted for PLL because its simulation cost is excessive. These conditions matter. The reported results show behavior under a specific process, circuit suite, simulator and budget, not a general analog-design law.

#### How to interpret yield and runtime

Finite Monte Carlo verification estimates a probability; it does not prove the true yield exactly. A design near a 99.9% threshold needs enough samples and uncertainty reporting to distinguish a true pass from sampling variation. A higher target can move the Pareto set toward safer but lower-performance designs. Runtime also includes different algorithm and baseline budgets. The PLL comparison omits NSGA-II. A speed ranking must therefore preserve those conditions.

The page-backed manuscript supports RSizing's robust multi-objective method and its reported OPAMP/OSC/PLL simulations, yield checks, hypervolume and runtime tables. It does not establish transfer to another process node, circuit family, simulator, variation distribution or signoff flow. It also does not remove the stated MVaR approximation or independent-reproduction requirements.

[Observed paper card](../observed-subthemes/process-aware-design.md#paper-iccad-2025-1080)

## Lithography connects an intended shape to a printed shape

Lithography uses a patterned exposure process to define structures during fabrication. The resulting shape can differ from the intended design because of the physical imaging and process behavior. Inverse lithography seeks a mask pattern that will produce the desired result under a stated model.

The generative-reinforcement-learning record proposes learning and refining candidate mask distributions. A model that produces plausible patterns still needs physical evaluation of the printed result. It also needs checks on whether the mask can be manufactured. The current description does not establish pattern coverage, process conditions, mask-quality measures, or total training and search cost. [Recorded evidence](../observed-subthemes/process-aware-design.md#paper-dac-2026-research209)

The relevant comparison is the final acceptable pattern under the same process conditions and evaluation budget. Similarity to training examples is a different measurement from successful printing.

<span id="explanation-dac-2026-research209"></span>

### Generative inverse lithography: a plausible mask is not yet a verified printed pattern

#### What inverse lithography is solving

The desired layout describes shapes that should exist after fabrication. Lithography chooses a mask and exposure process that produce those shapes after imaging, resist processing and other physical effects. Inverse lithography works backward. It searches over mask patterns using a model of how a candidate mask becomes a printed pattern.

The objective must therefore be defined at the printed shape, not only at the mask. Useful quantities can include edge-placement error, contour distance, process-window behavior, hotspot count, forbidden geometry and mask complexity. The metric must state the simulator, process conditions, tolerance and whether the final mask satisfies manufacturing rules.

#### What the generative and reinforcement-learning stages do

The recorded method uses style-aware GAN pretraining on design data, followed by policy optimization and imitation-learning fine-tuning over mask distributions. GAN pretraining can produce candidate patterns resembling the training distribution. Policy optimization changes candidates according to a reward. Imitation learning can make the policy follow selected examples or trajectories.

Those stages do not define the physical result without a reward and action space. If the reward measures only image similarity, it can prefer a mask that looks plausible but prints poorly. If the lithography simulator is simplified, the policy may exploit simulator errors. If process constraints are added only after generation, the refinement cost may remove the claimed time benefit.

#### What a complete comparison must measure

Compare conventional inverse-lithography solvers, generative methods and post-generation refinement. Use the same pattern suite, process model, simulator, compute budget and stopping rule. Report final printed-pattern metrics, edge-placement distributions, process-window or variation behavior, and mask-rule violations. Also report hotspot results, simulator calls, training and refinement time, memory and energy.

Test patterns must include shapes and interactions not represented in the training set. The study should separate training, policy-selection and final evaluation patterns. It should also test process changes. It should not assume that a policy trained for one node transfers to another. A mask that succeeds in simulation still needs mask-writing and fabrication constraints.

The captured DAC description supports a generative reinforcement-learning direction for inverse lithography. It reports no mask-quality metric, process condition, pattern suite, runtime, simulator cost, policy-training budget, refinement result or yield implication. The evidence supports a search method hypothesis, not demonstrated printed-pattern fidelity, speed or manufacturing benefit.

[Observed paper card](../observed-subthemes/process-aware-design.md#paper-dac-2026-research209)

## Fill changes both manufacturing conditions and electrical behavior

Fill insertion adds material patterns to satisfy density or other manufacturing requirements. Added structures can change electrical coupling near signal wires. Meeting a density rule can therefore affect circuit delay.

The differentiable-fill record combines fill selection with a learned capacitance estimate and an explicit delay objective. Capacitance describes how much charge changes with voltage in the modeled structure. A delay approximation uses those electrical estimates to guide the choice. [Recorded evidence](../observed-subthemes/process-aware-design.md#paper-dac-2026-research648)

The important question is whether the final layout meets both manufacturing rules and timing requirements under an adequate extraction model. The current description does not establish the accuracy of that connection across technologies or the complete final results.

<span id="explanation-dac-2026-research648"></span>

### Differentiable fill insertion: meeting density rules is not the same as preserving signoff delay

#### Why fill affects timing

Fill insertion adds shapes or material to satisfy density rules used by fabrication. Those shapes can change the electric field around signal wires. The result can change self-capacitance and coupling capacitance. It can also change the time needed for a driver to charge a wire and its load.

The design must satisfy two different conditions. The layout must meet manufacturing density rules. The signal paths must meet timing under the declared process and operating corners. A density score or a proxy for capacitance is not a timing-signoff result.

#### What the differentiable method changes

The recorded framework learns a capacitance estimate and optimizes fill with an explicit Elmore-delay objective. Differentiability allows the optimizer to change fill choices using a gradient rather than trying every discrete pattern independently. The method must define the fill representation, density and spacing constraints, training data, reference extractor and coupling model. It must also define how discrete legal layouts are produced from the optimization variables.

A learned capacitance model is useful only if its errors do not change the selected fill or the timing decision. A model can be accurate on average while missing a high-coupling net or a layout corner that controls signoff. Elmore delay is an RC approximation. It is not automatically equivalent to a signoff timing engine with distributed wires, coupling, slew, driver resistance, corners and variation.

#### What a complete evaluation must measure

Compare state-of-the-art and proxy-objective fill insertion. Use the same layouts, density rules, routing, process node, timing paths, extraction corners and stopping budget. Report density compliance, capacitance error against a reference extractor, delay and slack before and after fill. Also report runtime, memory, violations, repair rate and the fraction of paths that change signoff status.

The final selected layouts should be checked with an independent signoff extractor and timing tool. Test layer stacks, coupling patterns, path lengths, congestion, process variation and nodes not used for training. If the method claims manufacturing validity, include design-rule checks and the conditions under which the fill can actually be fabricated.

The captured DAC description supports differentiable fill insertion with learned capacitance and explicit Elmore-delay optimization. It reports no delay, density, capacitance, runtime, design-quality, extraction-error, signoff or cross-node result. The evidence supports an optimization direction, not demonstrated timing closure or manufacturing validity.

[Observed paper card](../observed-subthemes/process-aware-design.md#paper-dac-2026-research648)

<span id="explanation-dac-2026-research1282"></span>

### CPW-SMO: a larger common process window must be measured over a defined pattern set and fidelity rule

#### What source-mask optimization is choosing

Lithography uses a source of illumination and a mask pattern to print a wafer pattern. Source-mask optimization chooses both so that the printed result matches the desired layout. Conventional optimization may work on one source-mask pair at a time. CPW-SMO targets a set of patterns that must share one source while using multiple masks.

A common process window is a region of process conditions, commonly focus and exposure. In it, every selected pattern remains within a stated print-fidelity limit. The size of that window depends on the pattern set, the error metric, and the process axes. It also depends on the optical and resist model and the acceptable failure rate. “Nearly two times” is not interpretable until those quantities are named.

#### What the proposed components change

The record describes single-shot set-based generative optimization with attention, parallel simulation, preference-penalty scalarization and SMO-aware gradients. Attention can relate features across patterns. Parallel simulation can evaluate candidates concurrently. Scalarization combines objectives such as fidelity, window size and mask constraints into one optimization signal. The weights determine which pattern or constraint is sacrificed when the objectives conflict.

The source and masks remain coupled. A source that helps one pattern can hurt another. A mask that compensates for one focus/exposure condition may fail elsewhere. The method must define its action representation, gradient through the simulator or surrogate, mask-writability constraints, process sampling and stopping rule. A generative candidate that scores well in a surrogate still needs physical simulation and manufacturing checks.

#### How to read the reported speedup

The official description reports nearly 2× common process window and approximately 200× runtime speedup. Runtime speedup can arise from parallel hardware, fewer simulator calls, or a surrogate. It can also arise from an early stopping rule or a changed fidelity target. The comparison must include training, candidate generation, simulation, refinement, hardware and the same convergence or acceptance criterion.

Evaluate against iterative source-mask optimization. Use the same pattern set, node, process model, focus/exposure grid, fidelity threshold, mask rules and compute budget. Report per-pattern fidelity, the intersection of all patterns' valid windows, and failed patterns. Also report simulator calls, total wall time, hardware, memory and mask-writing constraints. Include unseen critical patterns and process variation.

The captured DAC description supports a set-based generative source/mask optimization direction. It reports no node, pattern count, common-window definition, fidelity constraint, simulator fidelity, runtime hardware, mask-writability result or baseline stopping rule. The nearly-2× and approximately-200× claims are conditional indicators, not established general lithography or manufacturing gains.

[Observed paper card](../observed-subthemes/process-aware-design.md#paper-dac-2026-research1282)

<span id="explanation-dac-2026-research1287"></span>

### Differentiable MDP-ILT: a mask can print the right wafer pattern and still be hard to write

#### Why ILT and mask data preparation interact

Inverse lithography chooses a mask intended to produce a target wafer pattern. Mask data preparation then converts that mask into shapes and shots that a mask-writing system can expose. A curvilinear mask can improve the optical representation. However, it may require more complex geometry, more shot fracturing or a write pattern that violates practical constraints.

The two objectives are related but different. Wafer fidelity measures the printed contour under an optical and resist process. Writability measures whether the mask can be represented, fractured, exposed, inspected and manufactured. This must happen within beam, dose, geometry, time and cost limits. A disjoint workflow can improve one while damaging the other.

#### What the differentiable MDP-ILT method changes

The record describes a physics-aware differentiable EBL simulator with exact gradients, optical-lithography simulation in the loop and end-to-end shot-parameter co-optimization. The intended benefit is to let changes to mask geometry and shot parameters respond to both objectives during one optimization. The objectives are wafer-fidelity and mask-writing.

The gradient is exact with respect to the implemented simulator, not automatically exact with respect to a physical mask writer. Discrete shot fracturing, variable-shaped-beam constraints, and geometry snapping may require projection or approximation after the gradient step. So may dose quantization and process variation. The final legal mask must be reevaluated through the full optical and EBL path.

#### What a complete evaluation must measure

Compare disjoint fab-ILT/MDP workflows with joint optimization. Use the same curvilinear pattern set, process node, and optical and resist models. Also use the same EBL calibration, shot constraints, compute budget and stopping rule. Report wafer contour error, edge placement, mask geometry violations, shot count, and write time. Also report dose, mask complexity, process window, simulator calls and optimization time.

Use an independent optical model and calibrated EBL model where possible. Test pattern geometries not used in training or tuning, and process variation. Also test different shot limits and layouts that make wafer fidelity and writability conflict. A simulation result is not a mask-write or fabrication result.

The captured DAC description supports differentiable joint optimization of wafer pattern fidelity and mask writability. It reports no wafer-error metric, writability metric, shot count, runtime, process window, calibration, mask-write or fabrication result. The evidence supports a co-optimization direction, not demonstrated manufacturability or preserved wafer fidelity on hardware.

[Observed paper card](../observed-subthemes/process-aware-design.md#paper-dac-2026-research1287)

<span id="explanation-dac-2026-research1298"></span>

### FreqSEM: a small edge-placement error requires a calibrated image-to-distance measurement and unseen-tool validation

#### What contour extraction is measuring

An SEM image contains pixel intensities produced by an imaging process. Contour extraction selects the boundary that represents a printed feature. The extracted contour can be compared with a reference contour using edge placement error. However, the result depends on several things. These are how the reference is defined, how the image is calibrated and how annotation uncertainty is handled.

FreqSEM uses frequency-aware FFT decomposition, SEM-adapted SAM2 prompting and feature injection, edge-weighted loss and Sobel-gradient loss. FFT features can expose different spatial-frequency content. A gradient loss can emphasize transitions. These mechanisms can help a model locate edges. However, they do not by themselves identify the physical edge. This applies when contrast, charging, blur, noise, tool calibration or process variation changes.

#### What the reported EPE values mean

The official description reports EPE mean 0.334 nm and standard deviation 0.661 nm for an 81 nm minimum line width. These numbers must remain tied to the stated image and measurement conditions. A nanometer value requires a pixel-to-distance calibration and a reference contour. The standard deviation is larger than the mean, so the distribution and difficult cases matter. An average alone can hide systematic bias or a subset of bad contours.

The comparison should report baseline EPE values, per-pattern errors, annotation agreement, and repeat-image variation. It should also report calibration uncertainty, runtime and the fraction of contours meeting a specified tolerance. It should state whether EPE is measured on centerlines, edges, line widths or another convention.

#### What generalization requires

Train and test splits should separate images or patterns. They should do so in a way that prevents near-duplicate structures from leaking across the boundary. Test on a new SEM session, tool, magnification, process condition, node and line-width range. If the model is used for process control, link contour error to the downstream decision. Report whether the extracted result changes that decision.

The captured DAC description supports a frequency-aware SEM contour-extraction direction with the reported EPE values. It does not provide dataset size, annotation uncertainty, baseline values, runtime, calibration, imaging conditions or cross-tool/node generalization. The evidence supports selected metrology results, not validated process-control accuracy or broad transfer.

[Observed paper card](../observed-subthemes/process-aware-design.md#paper-dac-2026-research1298)

## Distinguish prediction, physical verification, and fabrication

A model predicts behavior under assumptions. A physical design-rule check establishes compliance with the rules it implements. Measurement on fabricated devices establishes behavior of those devices under the measurement conditions. These are related steps, but they support different conclusions.

A process-aware method should state which step provides each result. If a learned model substitutes for a physical calculation, compare its errors against an appropriate reference. Also test whether those errors change the selected design. If the claim concerns yield or variation, include the population and operating conditions needed to assess those quantities.

## The comparison that supports a design decision

Keep input circuits or patterns, manufacturing rules, process models, and acceptance criteria explicit. Compare final valid outcomes, violations, total search cost, and sensitivity to relevant process variation. Include repair and recalibration when changing the process or design family.

The transferable lesson is which physical constraint changes the design choice and how reliably the method accounts for it. A faster approximation or favorable nominal case remains useful evidence. However, its claim must retain that narrower scope until broader validation is available.
