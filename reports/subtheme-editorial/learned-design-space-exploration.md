## What is being searched

A design space is a set of possible implementations. A processor design can vary buffer sizes, execution units, and scheduling choices. A circuit design can vary component dimensions or layout choices. A model intended for particular hardware can vary its structure. Each combination is a candidate whose correctness and cost must be evaluated.

The number of combinations can grow rapidly even when each individual choice has only a few options. Exhaustive evaluation becomes impractical if a detailed simulation takes minutes or hours. The search must decide which candidate deserves the next evaluation.

## What learning adds

A learned predictor estimates a candidate's behavior using examples that have already been evaluated. It may estimate latency, energy, temperature, or another quantity needed for a decision. An optimizer uses those estimates to decide where to spend the remaining evaluation budget.

There are two distinct errors. The prediction can be numerically inaccurate, and it can lead to a poor decision. A small error is consequential when it causes the search to reject the best candidate. It is also consequential when it causes the search to accept one that violates a hard limit. Conversely, a model can tolerate some numerical error if it consistently identifies valid useful candidates.

## How the selected papers divide the problem

Xsearch addresses the choice between simulators with different costs and accuracy. Its official description names Bayesian optimization and cross-evaluation between simulation levels. Bayesian optimization uses an estimate of both outcome and uncertainty when choosing the next evaluation. The available description establishes this method but does not provide enough quantitative conditions to conclude that it outperforms other searches. [Xsearch official description](https://63dac.conference-program.com/presentation/?id=RESEARCH1186&sess=sess167)

Other records in this group predict different quantities. The captured FUSE-TCAD description concerns physical fields inside a device. G-Power concerns power estimates across GPU designs. Compilation Tells Energy uses information produced during compilation to estimate accelerator energy. TACo ranks candidate neural-network structures using a score intended to avoid training each candidate. Their complete captured records appear below.

Those targets must remain distinct. A method predicting a spatial field must preserve relevant physical behavior. A power predictor must be calibrated against the measurement boundary used for energy or power. A score that ranks model structures must predict the final trained model's quality sufficiently well to guide selection. The common subject is choosing with incomplete information, but each method needs a different reference measurement.

## Why cheaper evaluation can make the answer worse

A search tends to select candidates with favorable predicted scores. If some candidates receive systematically optimistic errors, the search can concentrate on precisely those errors. Repeating the search then does not correct the problem; it can make the problem more pronounced.

Independent final evaluation matters for this reason. Test the selected candidate using an evaluator that was not merely reused to optimize its predicted score. Also inspect some rejected candidates to determine whether the search missed better choices. A successful final check establishes validity for that candidate; broader transfer requires new designs or conditions.

## How to compare the complete process

Give each method the same design tasks and total computing or elapsed-time budget. Include training, collection of labels, failed runs, calibration, and final evaluation. Report the valid result obtained at the end, not just the number of inexpensive predictions made.

The method may reuse a trained model across many future designs. If so, state how much reuse is needed to repay the training cost. If a new technology or workload requires retraining, include that cost in the transfer comparison. A long-term research question is whether these models can provide reliable decisions across changing designs with less total evaluation effort. The current selected descriptions establish candidate approaches, while the records below identify which experimental details remain unverified.

<span id="explanation-dac-2026-research883"></span>

## RTL-Sequencer: a sequence encoding is useful only when timing-critical structure survives it

RTL timing prediction estimates implementation timing before a complete synthesis-and-static-timing flow is available. The estimate can guide early architectural or RTL changes. However, timing is not a property of source text alone. Synthesis, cell choices, constraints, fanout, reconvergent paths, wiring and operating corners all contribute. A model that is numerically close on average can still miss the endpoint that controls timing closure.

RTL-Sequencer is described as linearizing RTL logic cones with breadth-first traversal and applying modern sequence models. It adds sequence shuffling, bidirectional modeling, differentiable modeling and a hybrid graph-sequence architecture. These choices change how long structural context is represented and learned. They do not guarantee that signal direction, reconvergence, fanout or technology-dependent timing behavior remains recoverable. The captured description does not specify tokenization, cone truncation, direction encoding, model objective, synthesis coupling or timing-label generation.

The first gate is timing-label fidelity. Define the reference quantity—endpoint delay, path delay, arrival time, required time or slack. Also identify synthesis, cell library, clock constraints, parasitic/wire assumptions, operating corner and STA tool. Compare absolute and signed error, rank correlation, critical-path recall and slack tails. Also compare false-feasible/false-violation decisions and per-design results against an independent post-synthesis STA reference. A model can improve mean error while missing the path that determines whether the design closes timing.

The second gate is structural and transfer validity. Test reconvergent cones, long paths, high fanout, sequential boundaries, resets, multiple clocks and modules outside the training distribution. Hold out complete designs, RTL families, module sizes, constraints, libraries and technology conditions; distinguish interpolation from design transfer and retraining. Compare a graph model, a sequence model, the hybrid model and ablations of shuffling, bidirectionality and differentiable modeling. Use identical labels and compute. “Sequence-based” does not establish process portability or structural equivalence.

If the predictor drives early timing optimization, include RTL parsing, breadth-first traversal, sequence construction and training/inference in the timing boundary. Also include candidate generation, failed synthesis, calibration and final STA. Report whether selected RTL actually improves independently measured slack, timing-closure rate, area, power and synthesis cost. Prediction speed alone is not an end-to-end optimization result if every candidate still requires the same expensive flow. It is also not one if the surrogate changes which candidate is chosen.

The official description claims significant improvement over state-of-the-art baselines and scalable early-stage RTL timing prediction. It reports no timing error, rank or endpoint results, runtime or model size. It also reports no RTL scale, transfer result, convergence or final optimization outcome. The evidence supports a sequence-based RTL timing-prediction direction. It does not demonstrate scalable timing accuracy, robust design transfer, timing closure or end-to-end optimization benefit.

<span id="explanation-dac-2026-research739"></span>

## Stochastic Diffusion Prior: a learned expert prior is useful only when sizing decisions survive circuit validation

Analog transistor sizing chooses device dimensions and bias-related values. The aim is for a circuit to meet objectives such as gain, bandwidth, noise, linearity, power and area. Each candidate may require a DC, AC or transient simulation, and the search can waste its budget in infeasible regions. Expert knowledge can make the initial search more efficient. However, a prior is a bias over candidates. It is not a device model, a circuit proof or a guarantee that a selected design remains valid across corners.

Stochastic Diffusion Prior (SDP) is described as eliciting domain expertise through an interface based on the gm/ID methodology. It encodes that knowledge as a diffusion prior. It then refines it with new simulation data through a mutual-information-guided diffusion process. It can be integrated with an optimizer such as Vanilla Bayesian Optimization. The mechanism changes proposal and exploration behavior; it does not remove the need for trusted circuit simulation. The captured description does not specify the prior parameterization, observed variables, diffusion schedule or information objective. It also does not specify optimizer coupling, constraints or stopping rule.

The first gate is sizing validity. Define the circuit specification and every objective/constraint. Then verify each selected design with a trusted simulator. Cover DC, AC and transient behavior as applicable, process/voltage/temperature corners, mismatch and stability. Also cover the relevant gain, bandwidth, noise, linearity, power and area measures. Record infeasible proposals, repairs, rejected candidates and constraint violations. An optimizer can improve a proxy or converge quickly. It may still select a design that fails a hard specification after parasitics or a corner is included.

The second gate is prior adaptation. State what expert inputs the gm/ID interface captures and how they become a probability distribution. Also state what simulation observations update it and how uncertainty and noisy evaluations are handled. Finally, state how mutual information chooses the next evidence. Deliberately corrupt or weaken the prior. Compare static-prior, no-prior and adaptive-prior flows with the same initial samples, optimizer, seeds and simulation budget. The test is whether adaptation improves valid design decisions, not merely whether it changes the generated samples.

Speed must include knowledge elicitation, prior construction, diffusion adaptation and optimizer overhead. It must also include all SPICE simulations, failed/infeasible candidates, parallelism and final independent verification. Compare Vanilla BO with and without SDP, manual gm/ID sizing, other AI sizing methods and a static prior. Use identical circuits, PDK, corners, objectives, constraints, initial designs and end-to-end timing boundary. The prior may be reused across circuits or nodes. If so, report the break-even number of designs and the cost of retraining or calibration.

The official description reports up to 92.3× speedup and 27.9× average speedup when SDP is integrated with Vanilla BO. It reports up to 2.0× improvement in key performance metrics and 1.5× on average. It also reports robustness to imperfect prior knowledge and knowledge transfer between technology nodes. It does not define the performance metrics, absolute simulation counts or times, feasibility rate or convergence. It also does not define PPA distribution, circuit count, transfer split or independent validation. The evidence supports an adaptive expert-prior direction for analog sizing. It does not demonstrate universal sample efficiency, calibrated prior accuracy, PPA improvement or transferable end-to-end optimization.

<span id="explanation-dac-2026-research1186"></span>

## Xsearch: multi-fidelity exploration is useful only when cheap simulation preserves the decision

Microarchitecture design-space exploration chooses among processor configurations. These include cache sizes, issue width, queue capacities, pipeline choices and other architectural parameters. Each candidate must be evaluated on workloads, usually with a simulator that estimates performance, energy or another objective. A detailed simulator can be expensive. A coarse simulator can evaluate more candidates but may distort the ranking, constraints or tradeoffs that matter.

Xsearch is described as multi-fidelity Bayesian optimization across simulators with different cost and accuracy. Bayesian optimization maintains a model of the objective and its uncertainty, then selects the next candidate or fidelity to evaluate. Xsearch adds cross-evaluation: information from high-fidelity simulation calibrates or corrects the cheaper exploration signal. This changes where simulation budget is spent. It does not make the low-fidelity simulator ground truth. It also does not remove the need to confirm the selected design with an independent high-fidelity evaluation.

The first gate is decision fidelity. Define the high-fidelity reference quantity, simulator error and calibration target. Compare predicted and high-fidelity performance, energy and constraint values across the design space, including infeasible candidates and Pareto boundaries. Report absolute error, rank correlation, calibration residuals and uncertainty coverage. Also report false-feasible/false-infeasible decisions and whether the method selects the same useful candidates as a high-fidelity search. A low average error can still select a poor processor if the error is concentrated near a hard constraint.

The second gate is a reproducible search contract. State the XiangShan revision, parameter ranges, workloads, warm-up and sampling, objectives and constraints. Also state the initial design, Bayesian surrogate and acquisition function, and fidelity-selection rule. Finally, state calibration data, stopping rule, seeds and parallelism. Count low- and high-fidelity simulations, surrogate training, failed simulations, calibration and final confirmation in the same compute or elapsed-time budget. More low-fidelity points are not an efficiency result unless the final high-fidelity design quality and validity improve under matched conditions.

Transfer requires more than applying the method to one open-source core. Hold out workloads, parameter regions and processor revisions, test repeated seeds and inspect convergence and rejected candidates. Compare low-fidelity-only, high-fidelity-only and single-fidelity search with the same objective, constraints, simulator access, budget and final evaluator. Include the cost of rebuilding calibration when the workload, simulator, architecture or technology changes.

The official description establishes multi-fidelity Bayesian optimization, cross-evaluation and application to the open-source XiangShan high-performance processor core. It reports no numeric improvement, simulator identities, error distribution, convergence, final design quality, feasibility rate, evaluation count or wall-clock boundary. The evidence supports a multi-fidelity microarchitecture-search direction, not demonstrated quantitative superiority, simulator-grounded accuracy or improved processor design quality.

<span id="explanation-dac-2026-research1156"></span>

## FUSE-TCAD: a fast multi-field surrogate is useful only when the fields remain physically coupled

TCAD solves coupled partial differential equations (PDEs) over a device mesh. It obtains spatial fields such as potentials, carrier quantities and currents under geometry, material and bias conditions. Those fields are useful because they explain device behavior and support derived quantities. A scalar prediction can be numerically accurate for one metric. It can still lose the local information needed to diagnose a junction, interface or design change.

FUSE-TCAD is described as a conditional diffusion surrogate. It generates a joint distribution of physical fields while accepting continuous geometry and bias controls. A physics-aware Sobolev-edge regularization term encourages gradient consistency near junctions, and transfer learning uses 20% target-domain data. These mechanisms target field structure and conditioning. However, the captured description does not specify the PDEs, field channels, mesh, boundary conditions or diffusion schedule. It also does not specify number of samples, regularization weight, reference solver, uncertainty handling or target-domain adaptation procedure.

The first gate is physical fidelity. Define each field, unit, resolution, interface condition and reference numerical solve. Compare field values and gradients, PDE residuals, flux/charge/current conservation, boundary error, cross-field identities and derived device metrics. Test junctions, interfaces, sharp gradients, bias corners and rare conditions. A low average relative error can hide a physically invalid field where the device decision is made. A visually plausible sample can do so too.

The second gate is generative and conditioning cost. State the number of denoising samples/steps, stochastic variability, uncertainty calibration, geometry/bias encoding, preprocessing, postprocessing and failure behavior. Evaluate continuous controls between training points and extrapolation outside the training domain. Also report candidate-ranking agreement when the surrogate is used inside an optimization loop. A fast sample is not an optimization gain if it changes which device is selected. It is also not a gain if it requires repeated rejection by TCAD.

The 20% target-domain-data claim also needs a precise transfer boundary. This covers source and target process/device, held-out split, adaptation labels, retraining parameters and comparison surrogate. Include label generation, training, adaptation, diffusion inference, calibration, fallback and final TCAD validation in the time budget. Compare commercial TCAD, scalar regression and field-surrogate alternatives at the same mesh/resolution, error target, target labels and physical conditions.

The official description reports more than 30× speedup over commercial TCAD and relative error within 0.8%. It also reports robust transfer with 20% target-domain data and high-fidelity/cross-field-consistent fields on SOI-FET datasets. It does not expose PDE/error definitions, field resolution, solver or hardware conditions, or uncertainty. It also does not expose transfer baseline, extrapolation, sampling cost or downstream device-design validation. The evidence supports conditional diffusion multi-field TCAD surrogates, not demonstrated PDE-faithful, process-transferable or design-validated near-real-time TCAD.

<span id="explanation-dac-2026-research906"></span>

## LEAP: fast toggle prediction is useful only when activity fidelity and power calibration survive transfer

Dynamic or switching power depends on which signals change and when they change. It also depends on how those changes propagate through a synthesized and laid-out circuit. Per-cycle toggle propagation supplies that activity information but can be expensive when every vector is simulated through the netlist. A learned shortcut can reduce this cost, yet two different errors matter. The model may predict the wrong toggle. Or it may predict a plausible activity pattern that causes the downstream power model to make the wrong design decision.

LEAP is described as a linear-complexity graph transformer with self-supervised pre-training tasks intended to capture circuit structure and functionality. It predicts per-cycle toggle propagation. LEAP-Power integrates this predictor with other machine-learning power models and estimates per-cycle layout power directly from post-synthesis netlists. The mechanism changes how activity labels are produced and consumed. It does not specify the graph representation, clock/reset semantics, sequence window or target event. It also does not specify layout/parasitic features, power boundary, calibration, or fallback to the EDA flow.

The first gate is activity fidelity. Define whether the target is a binary node value, a transition event, a thresholded toggle or another quantity. Also specify cycle alignment, clock domains, resets, unknowns, sequential state and input vectors. Report value error, temporal alignment, precision/recall by event rarity, false negatives on high-power transitions, calibration and per-design/per-vector results. A PR-AUC can be near perfect while many rare high-impact transitions are missed, especially when most cycles are inactive.

The second gate is power-model calibration. State whether power means switching, internal, dynamic, total or energy over a window, and how MAPE handles near-zero values. Compare LEAP-Power with a trusted EDA or measured reference. Cover designs, layouts, voltage, frequency, temperature, corners, activity distributions and technology conditions. Report absolute error, bias, tail error and ranking of candidate designs. Also report whether the model preserves the decision made by the full flow. An average percentage error is not automatically signoff-quality accuracy.

“Transferable” requires a held-out boundary. Test unseen netlist structures, cell libraries, technologies, clock domains, input distributions and rare behaviors without structural or label leakage. Include self-supervised pre-training, graph/feature extraction, label generation, model inference, calibration, fallback and final power validation in the elapsed-time comparison. A speedup that excludes training and labels may be useful for repeated reuse. However, the break-even number of designs must be stated. Bypassing toggle propagation is not necessarily a full EDA-flow speedup.

The official description reports 7.6× speedup over the EDA tool for toggle propagation and PR-AUC of 0.99. It also reports LEAP-Power MAPE of 4.55% for per-cycle layout-power prediction, and 5.3× runtime improvement over a model without LEAP. It does not expose absolute conditions, toggle-value error, power boundary, design/technology split, calibration, rare-event behavior, training/label cost or signoff/silicon validation. The evidence supports learned toggle and early layout-power estimation, not demonstrated transferable signoff-quality power analysis or complete EDA-flow acceleration.

<span id="explanation-dac-2026-research3154"></span>

## Automated datapath gating: a predicted power win is useful only after ODC and post-route checks agree

Datapath gating suppresses computation or data movement when the result cannot affect an observable output. The opportunity depends on an observability don't-care (ODC). For a particular state, input constraint and time window, some internal value may be irrelevant to the output. Adding an enable condition can reduce switching. However, the condition itself adds logic and can alter timing, sequential behavior or reset semantics. A useful flow must therefore prove that the gated datapath is equivalent. It must also prove that the saved switching exceeds the new cost.

The described methodology combines a SAT-based technique for computing valid ODC conditions. It pairs this with a machine-learning power model that predicts the improvement from a gating opportunity. The SAT result proposes when an enable is logically safe. The learned model helps decide whether the opportunity is profitable early in synthesis. The two components answer different questions. Satisfiability does not predict physical power. A power prediction does not prove functional equivalence. The captured description does not specify the SAT constraints, temporal model, ML features/training data, transformation, fallback or checking flow.

The first gate is functional validity. Define outputs, state, input/environment constraints, latency, reset, clock domains, X/unknown semantics and the observation window used by the ODC proof. Prove RTL-to-gated equivalence under those assumptions and test corner cases, illegal inputs, stalls, sequential state and control races. An enable condition can be logically valid for a combinational cone. It can still be invalid after pipelining, retiming, clock gating or incomplete environment assumptions.

The second gate is power calibration. State whether the target is switching, internal, dynamic or total power. Identify the activity source, vector coverage, voltage/frequency, library, parasitics and reference tool. Report signed and absolute prediction error, tail error, post-synthesis versus post-place-and-route error, gating coverage, timing slack and area. The reported “-1%” needs a reference and sign convention. A small average change can be modeling noise. A rare high-activity datapath can dominate the decision.

Automation must include SAT solving, feature extraction, ML training/inference, candidate ranking and gating insertion. It must also include synthesis, placement, routing, timing closure, power analysis, rejected candidates, repair and human review. Compare ungated and manual gating with identical RTL, technology/library, constraints, activity traces, tool versions, seeds, signoff checks and elapsed-time boundary. Measure whether the selected gates remain beneficial after routing, not merely whether the early predictor ranked them correctly.

The official description reports industrial-flow integration, high-accuracy power prediction and fully automated data gating. It also reports an average -1% post-place-and-route dynamic-power result and negligible area/runtime overhead. It does not expose prediction error, absolute power, timing, area, gating coverage, SAT cost, per-design variance or signoff conditions. The evidence supports ODC-aware ML-guided datapath-gating automation, not demonstrated signoff-power accuracy, universal power reduction or negligible cost across designs.

<span id="explanation-dac-2026-research1431"></span>

## G-Power: cross-GPU knowledge can reduce power-model data needs only if transfer is held out and calibrated

Architecture-level GPU power modeling estimates power from a representation of a GPU's structure and activity. It does so without running a full physical power analysis for every design or workload. Such a model is useful when its prediction is accurate enough to guide architecture choices, power limits or design-space exploration. The reference boundary matters. Instantaneous chip power, averaged device power, package power, board power and energy per workload are different quantities.

G-Power is described as a three-phase flow. The first phase is pre-training on additional known GPU chips. The second is attention-inspired aggregation of knowledge across those chips. The third is fine-tuning on a target GPU. The transfer mechanism can expose common relationships between architecture features, activity and power. It can potentially reduce the number of expensive labels needed on the target. It does not by itself establish that the representation captures the target GPU's power behavior. It also does not establish that the model is calibrated under a new voltage, frequency, temperature or workload.

The first gate is measurement validity. State whether the target is instantaneous or average power, chip/package/board power or energy. Also identify the sensor or simulator, sampling interval, voltage/frequency state, temperature and idle/background subtraction. Report signed and absolute error, MAPE definition, tail error, bias and correlation by GPU, workload and operating condition. A good average can hide systematic error on high-power kernels or an offset that makes an architecture decision wrong.

The second gate is transfer validity. Hold out complete GPU designs or generations. Keep near-duplicate workloads out of train and test. Separate three cases: training only on source GPUs, zero-shot prediction on the target, and fine-tuning with a declared target-label budget. Compare against AccelWattch, microbenchmark-only training and other models with the same counters, features, workloads, calibration, sampling and hardware boundary. Report pre-training, aggregation, fine-tuning and inference cost, along with uncertainty and failed or out-of-range predictions.

The official description reports average MAPE of 14% and correlation coefficient R of 0.88 on four modern NVIDIA GPUs. These are described as 22% lower MAPE and 0.36 higher R than AccelWattch. The captured evidence does not identify the GPUs, workload distribution, split, labels or measurement boundary. It also does not identify per-GPU errors, calibration conditions or resulting energy/design decisions. It supports a knowledge-aggregated GPU power-modeling direction, not demonstrated cross-GPU generalization or reliable energy-guided architecture improvement.

<span id="explanation-dac-2026-research1474"></span>

## Compilation Tells Energy: compiler features can predict accelerator power only after physical calibration

An RTL generator produces an accelerator implementation from hardware and workload choices. Before synthesis, the compiler intermediate representation (IR) already exposes information about operators, tensor shapes, tiling, fusion and scheduling. That information can help predict power because software mapping and hardware structure jointly determine switching and data movement. It remains a proxy. The IR does not directly contain library cells, wire capacitance, clock-tree behavior, memory implementation or voltage-dependent physical activity.

Compilation Tells Energy is described as extracting compiler-IR features. It applies multi-task learning to estimate accelerator power early in an RTL-generator workflow. The push-button flow changes the feature and prediction path, potentially making feedback cheaper for designers. It does not establish that the predicted quantity matches measured power or that the model ranks design choices correctly. It also does not establish that a new generator or compiler exposes the same semantics.

The first gate is reference calibration. Define dynamic versus total power, peak versus average, accelerator versus system boundary and power versus energy per inference. Name the simulator, synthesis flow or sensor, and fix technology, clock, voltage, activity assumptions, memory conditions, sampling and thermal state. Report absolute and relative error, bias, tail error and rank correlation. Then check whether model errors change the selected design or violate a power limit.

The second gate is transfer and leakage control. Split by networks, operators, shapes, generator configurations and accelerator architectures rather than randomly splitting near-identical compiler traces. Test held-out Gemmini and hls4ml cases, new workloads, new generator/compiler versions and unfamiliar mappings. Compare architecture-level simulators, generic ML predictors and manual analysis with the same IR, reference evaluator, hardware conditions and total budget. Include IR extraction, training, inference, label collection, retraining, failed cases and final synthesis or hardware confirmation.

The official description claims practical accuracy and push-button power-aware agile design, validated on Gemmini and hls4ml. The captured evidence does not expose numerical error, synthesis correlation, model scope or technology. It also does not expose clock/voltage conditions, label cost or end-to-end energy accounting. It supports compiler-informed early power modeling, not demonstrated calibrated silicon power prediction or universally power-aware accelerator design.

<span id="explanation-dac-2026-research2048"></span>

## Multi-die FPGA floorplanning: a congestion predictor must survive the real placement-and-route flow

HLS chooses an accelerator structure and schedule. A multi-die FPGA implementation must also assign logic and memories to physical slots and route connections across dies. Cross-die links can add delay, while local concentration of resources or pins can make a candidate unroutable. A floorplan-quality predictor is therefore a search surrogate. It can reduce the number of expensive Vitis implementations. Its output is not itself a legal placed or routed design.

The described method uses a slot-level graph neural network to predict floorplan quality and congestion. It then integrates that predictor into HLS design-space exploration. The graph should expose slot capacity, resource types, connectivity, die boundaries and the accelerator's placement demand. The captured description does not specify that graph, the labels, the prediction-to-parameter policy or the constraints enforced before Vitis. A high classification score can still miss a narrow routing bottleneck or a cross-die timing failure.

The first gate is implementation validity. Check legal resource capacities, die assignments, clock and pin rules, placement and routing completion. Also check congestion maps, cross-die crossings and post-route timing with the actual Vitis flow. Report false positives, false negatives, unroutable candidates, repairs and HLS functional equivalence. Frequency should be identified as post-route closure or an estimate; the two are not interchangeable.

The second gate is total search cost and hardware tradeoff. Include feature construction, GNN inference, candidate generation, Vitis compilation, placement, routing, failed iterations and any repair. Hold FPGA family, die/interposer topology, speed grade, Vitis version, clock target, resource limits, routing settings, seeds and benchmark set fixed. Report LUT/FF/BRAM/DSP use, power, cross-die traffic, worst-case timing and per-design results, not only average frequency or predictor accuracy.

The official description reports 84.13% congestion-prediction accuracy, 0.86 F1-score and 0.58ms average inference latency. It reports an unroutable and 318.2MHz case improved to 329.2MHz and 330.3MHz. It also reports average frequency improvement of 11.2% with a 23.8% maximum, and 30.9% lower benchmark execution time. The captured evidence does not expose design splits, device/tool versions, routing status, PPA, per-design outcomes or complete timing boundaries. It supports GNN-guided multi-die FPGA floorplan exploration, not demonstrated portable routed-timing improvement across FPGA flows.

<span id="explanation-dac-2026-research1878"></span>

## Hardware-aware BEV NAS: real-time detection is a joint accuracy, sensor and deployment claim

Bird's-eye-view (BEV) 3D detection converts camera and LiDAR observations into a shared spatial representation, then predicts object classes and locations. The representation, sensor preprocessing, feature fusion, detection head and runtime implementation jointly determine accuracy and latency. A neural architecture search (NAS) method changes which model is selected. It does not make the selected model real-time under every sensor rate, resolution, power mode or deployment pipeline.

The described framework constrains the NAS space using hardware considerations. It adds a lightweight depth-estimation network plus LiDAR-camera cross-attention in the BEV conversion path. The depth estimator can improve geometric alignment, while cross-attention lets one modality use information from the other. Those additions must be evaluated together with preprocessing, voxelization or projection, feature encoding, detection, postprocessing and memory movement. A lower network FLOP count is not enough if irregular fusion or memory traffic dominates Jetson execution.

The first gate is detection validity. Fix the nuScenes split, class set, range, coordinate convention, sensor synchronization, point sampling, camera resolution and evaluation code. Report mAP by class and distance, precision/recall, missed and duplicate objects, calibration and robustness to missing or delayed modalities. Hold the training recipe and augmentation budget constant against the baseline. Separate the contribution of hardware-aware search, the depth estimator and cross-attention with ablations.

The second gate is end-to-end deployment measurement. State Jetson AGX Orin software, TensorRT or compiler versions, precision, clocks, power mode, batch size, memory use and thermal state. Measure sensor-to-decision latency, throughput and tail latency, including capture, preprocessing, transfers, inference and postprocessing. Also report power and energy per frame. Search cost, retraining, compilation, engine building and failed candidates belong in the total design cost. This holds even if they are not part of steady-state FPS.

The official description reports 70.1% mAP on nuScenes, a 2.3 percentage-point improvement over baseline. It also reports 35.6 FPS on Nvidia Jetson AGX Orin. It does not expose model configuration, input resolution, class/distance breakdown, latency distribution or power. It also does not expose memory, thermal conditions, preprocessing boundary, search cost or baseline hardware settings. The evidence supports hardware-aware multimodal BEV architecture search, not demonstrated universal real-time autonomous-driving suitability or a complete accuracy-throughput-energy improvement.

<span id="explanation-dac-2026-research2083"></span>

## CHiRM-DSE: a fast HLS evaluator helps only if it preserves the ranking that matters

HLS maps a program into hardware through choices such as loop unrolling, pipelining, tiling, array partitioning and interface directives. The pragma space can be enormous. Each candidate may require synthesis or downstream implementation to measure resource use and performance. A DSE method therefore has two linked responsibilities. It must select promising candidates. It must also estimate their quality without spending the full evaluation cost on every point.

CHiRM-DSE is described as hierarchical design-space decomposition, rule mining to guide search, and a CodeLLM evaluator for design points. Decomposition and rules prune or prioritize candidates; the CodeLLM surrogate predicts QoR faster than direct HLS. These mechanisms alter search and evaluation cost. A plausible code-level prediction is not itself a synthesized circuit, timing result or resource-feasible implementation.

The first gate is evaluator ranking. Define the HLS tool, FPGA family, clock constraint, directives, compiler, resource limits and QoR objective. Split benchmarks and pragma families so that test candidates are not near-duplicates of training examples. Report prediction error and rank correlation for latency, initiation interval, LUT/FF/BRAM/DSP use and power, plus invalid or failed synthesis cases. A surrogate can have good average error while misordering the few candidates on the Pareto frontier.

The second gate is search fairness. Hold the four benchmarks, initial observations, random seeds and total wall-clock budget constant. Also hold parallelism, tool cache, synthesis timeout and final HLS/implementation evaluator constant. Compare exhaustive search, tuned and untuned metaheuristics, prior GNN evaluators and state-of-the-art DSE methods. Include rule-mining, decomposition, CodeLLM inference, prompt/model training, candidate repair and final re-evaluation costs. Check whether public code reproduces the same tool/version behavior and whether CodeLLM training or benchmark leakage changes the result.

The official description reports better QoR than the state of the art under equal time budgets on four HLS benchmarks. It claims a CodeLLM evaluator faster than direct HLS and more accurate than prior GNN evaluators. Demo code is released. It supplies no numeric QoR, evaluator error, search time, benchmark names, FPGA/tool conditions, frontier coverage or artifact reproduction. The evidence supports rule-guided hierarchical HLS exploration with a learned evaluator. It does not demonstrate portable QoR superiority or implementation-quality prediction across FPGA flows.

<span id="explanation-dac-2026-research1971"></span>

## ATPG-free test-point insertion: learned controllability is not measured fault coverage

Test-point insertion adds control or observation access to a circuit. Scan patterns can then sensitize and observe faults more easily. The optimization is difficult because adding a point can improve one region. It can also increase area, timing, routing, scan complexity or power. Controllability describes how readily a signal can be driven to a value. Observability describes whether its effect can reach an observation point. Neither proxy is itself fault coverage or a valid production test result.

The described pipeline trains an autoencoder on bit sequences to form functional embeddings. It propagates those embeddings through reconvergent regions and infers controllability from the embeddings. It uses saliency maps to estimate observability. It aims to avoid ATPG labels and reinforcement-learning search overhead. The central question is whether those self-supervised signals rank useful insertion sites. This must hold when reconvergent logic, sequential state, scan constraints and the actual fault model are present.

The first gate is test-quality validation. Specify stuck-at, transition, bridging, delay or other fault models, and scan architecture. Also specify clock/reset assumptions, sequential depth, pattern constraints and the ATPG reference. After inserting points, run an independent ATPG flow. Report pattern count, detected faults, fault coverage, untestable faults, aliasing, pattern-generation failures and diagnosis quality. Evaluate clean and unseen circuit structures, not only bit sequences or graph regions used to train the embedding.

The second gate is implementation cost. Constrain legal insertion locations and report point count, area, timing, power, routing, scan-chain length, test-data volume and tester time. Compare traditional testability metrics, supervised learning with ATPG labels and reinforcement learning. Match the circuit suite, fault model, point budget, implementation library and computational budget. Include self-supervised training, embedding propagation, saliency computation, candidate selection, ATPG verification and any manual repair in the end-to-end cost.

The official description claims effective TPI without ATPG dependency or RL overhead. It supplies no pattern-count reduction, fault coverage, circuit suite or area/timing cost. It also supplies no training time, fault model, scan conditions or generalization result. The evidence supports an ATPG-free learned testability-ranking direction. It does not demonstrate production test improvement. It also does not demonstrate equivalence between embedding-derived controllability/observability and measured fault coverage.

<span id="explanation-dac-2026-research1440"></span>

## TACo: a zero-cost score must predict trained accuracy and real hardware, not just rank untrained networks

Vision Transformer architecture search chooses among candidate patch embeddings, depths, widths, attention structures and MLP configurations. A candidate that looks promising before training can become poor after optimization. A candidate with low operation count can be slow or energy-hungry on the target device. Multi-objective search must therefore preserve the distinction between a cheap proxy, a trained model's quality and a measured deployment result.

TACo is described as a training-free hardware-aware search using a Hypervolume-based Unified Zero-Cost Score. Its zero-cost accuracy score combines layer-wise gradient stability, weight-gradient coupling and gradient-modulated activation stability. The HV-score combines that accuracy proxy with latency, energy and activation memory. It does so through Pareto and hypervolume selection. These components can reduce candidate-training cost. They do not establish that the proxy is calibrated after training. They also do not establish that hardware estimates include the complete inference path.

The first gate is ranking validity. Define the ViT search space, initialization, batch/input resolution, data split, zero-cost calculation, training recipe and final accuracy measurement. Compare proxy rankings with fully trained accuracy on held-out architectures. Report rank correlation, top-k regret, Pareto-frontier recall and variance across seeds. Guard against weight sharing, data leakage and search-set overfitting. A score can appear strong on CIFAR-10 or ImageNet-1K while failing under a changed task or architecture family.

The second gate is hardware validity and objective accounting. Measure latency, energy and activation memory on named devices. Fix the compiler, precision, batch size, clocks, thermal state and input pipeline. Include preprocessing, transfers, operator kernels, memory allocation, synchronization and postprocessing. Report how hypervolume reference points, normalization and constraints affect selections. Compare trained multi-objective NAS, single-objective zero-cost search and random or evolutionary baselines. Use the same candidate, training and wall-clock budgets.

The official description reports CIFAR-10 and ImageNet-1K experiments that reduce search from GPU-days to GPU-hours. They also identify a balanced ViT architecture. It does not provide absolute accuracy, candidate counts, search space or proxy error. It also does not provide hardware calibration, energy boundary, reference points or final deployment measurements. The evidence supports a training-free multi-objective ViT-ranking direction, not demonstrated accuracy-preserving hardware transfer or general search superiority.

<span id="explanation-dac-2026-research2177"></span>

## GTX: fast parasitic prediction is useful only when the electrical decision survives extraction error

Parasitic extraction converts a layout's geometry, materials and connectivity into resistance, capacitance and coupling values used by post-layout simulation. In analog circuits, small errors near a pole, matching constraint, settling limit or stability boundary can change the design decision. This can happen even when an average parasitic error appears small. A predicted-parasitics netlist is therefore a surrogate for an electrical model, not merely a faster file format.

GTX is described as a customized parasitic representation combined with hierarchical graph neural networks and global attention. Local device interactions can capture nearby geometry and connectivity, while global attention can represent long interconnect dependencies. The method must still define which layout features, nets, coupling terms and process assumptions are represented. It must also define how the predicted netlist preserves units, reciprocity, sparsity, boundary conditions and simulator semantics.

The first gate is extraction fidelity. Split circuits and layouts by topology, geometry family and design, not only by randomly sampled nets. Evaluate resistance, capacitance and coupling distributions, worst-case net error and failed predictions. Also evaluate correlation of extracted-versus-predicted values across process, voltage, temperature and geometry corners. Then run an independent commercial or trusted extractor. Compare gain, bandwidth, delay, phase margin, noise, settling and other design quantities. Close waveform agreement on selected circuits does not establish signoff-grade fidelity.

The second gate is speed and deployment accounting. Separate model training, layout feature construction, graph inference, netlist writing, simulator setup, convergence failures and post-processing from commercial PEX runtime. State PDK, node, layout size, extractor settings, hardware and parallelism. Compare prior ML predictors and commercial PEX on identical layouts. Also report whether the predicted netlist changes optimization choices or only reproduces already selected designs. Include out-of-distribution layouts, new process nodes and coupling-dense cases.

The official description reports higher accuracy than prior ML-based methods and predicted-netlist simulation agreement with commercial extracted netlists. It also reports 232.7× faster parasitic inference and up to 8.4× faster simulation. It does not provide absolute error, failed circuits, PDK/process diversity, corner coverage, training cost, hardware boundary or downstream analog metrics. The evidence supports a graph-based parasitic surrogate for design iteration, not demonstrated signoff-grade extraction or universal analog-design acceleration.

<span id="explanation-dac-2026-research2884"></span>

## Voyager: configurable accelerator generation is not the same as a valid tapeout-ready design space

An end-to-end DNN accelerator flow has to connect four contracts. They are the architecture parameters, generated RTL/HLS implementation, the compiler's tensor and quantization mapping, and the measured hardware behavior. A design point is useful only if it synthesizes and meets its timing and resource constraints. It must also compute the intended model within its numerical tolerance. It must be evaluable with a comparable PPA boundary. Broad parameterization expands the search space. It does not prove that every point is legal or that the compiler and RTL agree.

Voyager is described as an HLS-based generator with configurable processing elements, on-chip buffers, external-memory bandwidth, technology nodes and clock frequencies. It supports built-in and custom datatypes, arbitrary-length floating point, posit and integer formats, and per-tensor scaling and microscaling. It also supports a PyTorch-based compiler with quantization, operation fusion and tiling. The central artifact is the connection among these layers. Datatype encoding, accumulation, saturation/rounding, tiling, buffer capacity, memory traffic and generated control must have one consistent semantics.

The first gate is functional and numerical correctness. Compare compiled accelerator outputs with a high-precision software reference. Cover models, layers, shapes, sparsity, quantization formats, overflow/rounding, fused operations and edge cases. Report unsupported operators, compiler fallbacks, failed HLS/synthesis, resource violations, deadlocks and accuracy by model and datatype. Full-dataset accuracy evaluation is meaningful only when the generated design actually executes the same model. The evaluation must also include all conversion and unsupported-operation handling.

The second gate is implementation and DSE validity. State PDK/technology node, HLS tool, clock constraint, memory interface, PE/buffer parameters and bandwidth. Also state place-and-route/signoff boundary and whether area/latency are estimated or measured. Compare prior generators, manual DSE and hand-crafted accelerators under matched models, datatypes, compiler optimization, process, clocks, workloads and resource limits. Include compiler generation, HLS, synthesis, implementation, failed candidates and search time. Report utilization, latency, throughput, area, power, energy, memory traffic and timing closure rather than only a favorable design point.

The official description claims up to 99.8% utilization. It also claims up to 61% lower latency and 56% lower area than prior generators. It also claims comparable performance to hand-crafted accelerators, broad datatype/quantization support and tapeout-oriented generation. It does not provide absolute PPA, synthesis/signoff evidence, compiler coverage, technology-node conditions, search cost or numerical failure cases. The evidence supports a configurable HLS/compiler co-design framework, not demonstrated tapeout readiness or universal accelerator superiority across design points.

<span id="explanation-dac-2026-research2385"></span>

## UNCHARTED: a transient surrogate must remain faithful when it becomes a design optimizer

Analog transient simulation solves how node voltages and currents evolve. It does so under device models, circuit topology, input waveforms, initial conditions and process parameters. A surrogate can be much faster than SPICE by learning that trajectory. However, the relevant error is not only pointwise waveform similarity. A small error near a threshold, settling time, oscillation, stability boundary or specification limit can change a sizing decision.

UNCHARTED is described as a hierarchical auto-regressive spatio-temporal graph neural network with exogenous driving inputs. Circuit components and their connections form a graph. Temporal state is advanced step by step. Low-rank adaptation represents changes in component sizing. Back-propagation then supports inverse design. These mechanisms change how simulation outputs are approximated and how gradients are obtained. They do not ensure that generated sizes are legal, stable, manufacturable or correct under the original circuit equations.

The first gate is surrogate fidelity across the intended domain. Define topology families, device models, input waveforms, time steps, initial conditions, process/voltage/temperature corners and observables. Partition training, validation and test circuits by topology and design family, not only by waveform samples. Report absolute and relative waveform error, timing/settling error and extrema. Also report failed or unstable rollouts, long-horizon drift and worst-case error near design constraints. A similarity score above 95% on a subset of circuits cannot establish robust corner or out-of-distribution behavior.

The second gate is inverse-design validity. Constrain sizes to legal ranges and quantization. Re-simulate every proposed circuit with an independent SPICE configuration. Compare delay, gain, bandwidth, power, stability, noise and area under the same specifications. Include the cost of surrogate training, adaptation, gradient iterations, rejected candidates and final SPICE verification. A fast inverse-design loop can optimize surrogate artifacts if the final evaluator is not independent.

The official description claims up to 241.9× simulation acceleration. It also claims over 95% similarity to SPICE in more than 70% of tested circuits. It also claims delay-chain and amplifier optimization examples. It does not provide circuit counts, topology split, process corners or similarity definition. It also does not provide error distribution, training cost, solver settings, design constraints or final-quality results. The evidence supports a learned analog-transient modeling and inverse-design direction, not demonstrated universal SPICE fidelity or circuit-design improvement.

<span id="explanation-dac-2026-research1519"></span>

## AgenticDSE: multi-agent search is useful only when the search space and evaluator are trustworthy

A chiplet accelerator is assembled from multiple dies or functional blocks whose
compute, memory, communication and packaging choices interact. A design-space
exploration (DSE) system proposes a candidate, evaluates its objectives, and
uses the result to choose the next candidate. The expensive step is usually
not writing down a configuration. It is obtaining a credible latency, energy,
area, bandwidth, thermal or correctness result for that configuration.

AgenticDSE is described as three cooperating large language model agents: an
exploration orchestrator, an architecture analyst and an optimization engineer.
The analyst is intended to expose domain structure. The orchestrator coordinates
the search. The engineer applies the resulting optimization process. The
description also names analysis-driven search-space refinement, phase-wise
Bayesian optimization and ensemble surrogate modeling. These components change
how candidates are represented and selected. They do not make a candidate
legal, manufacturable or correctly evaluated by themselves.

The first boundary is the design-space contract. A reproducible system must
state the chiplet templates, die count, compute and memory options, topology,
and link widths and rates. It must also state buffer sizes, placement/package constraints, process and
technology assumptions, and which combinations are forbidden. Refining the
space can remove obviously poor candidates. However, an LLM-generated constraint can
also remove the best design or admit an infeasible one. Record every refinement
and the reason for it. Record the candidate count before and after it. Also record whether a
trusted checker independently accepted the remaining candidates.

Bayesian optimization uses observations from evaluated candidates to select new
ones, often balancing predicted objective value against uncertainty. An
ensemble surrogate can represent disagreement between predictors, but the
disagreement is not automatically calibrated uncertainty. Phase-wise search
also needs a defined phase transition. It must say which observations
trigger it and which variables are still allowed to change. It must also say how surrogate state is transferred, and
whether previous candidates remain eligible. Otherwise “multi-phase” describes
an implementation label rather than a reproducible search policy.

The Pareto front is the set of candidates with a specific property. For each, no other candidate is at
least as good on every declared objective and strictly better on one. A distance
to a “real Pareto front” depends on how that front was constructed and
which objectives are normalized. It also depends on whether all candidates were exhaustively or
approximately evaluated. Diversity similarly depends on the coordinate or
objective-space definition and the sampled region. A search can move closer to
one reference front while missing an entire family of feasible designs. Report
the reference-front construction, objective units, feasibility filtering,
normalization, hyperparameters, seeds, failed evaluations and per-run results.

Token consumption is a resource of the agent interface, not a hardware-quality
metric. Fewer input or output tokens can mean shorter prompts, fewer reasoning
steps, or a different amount of domain information. They do not establish lower
simulation time, lower energy, better PPA, or lower human effort. Charge for
prompt construction, model calls, tool calls, surrogate training, candidate
evaluation, retries, invalid proposals and human review. Compare against the
same model family, context, tool access, stopping rule and total wall-clock or
compute budget.

The captured description reports up to 36.9% lower average distance to the real
Pareto front and 66% higher explored-front diversity. It also reports 46×/18× lower input and
output token consumption than prior LLM-based solutions. These are bounded
source claims, not a demonstrated universal chiplet-accelerator improvement.
The description does not identify the accelerator templates, chiplet process or
package, objective definitions or surrogate features. It also does not identify exploration budget, number
of seeds, evaluator, baseline implementation, PPA values, feasibility rate or
transfer split. Thus the evidence supports a proposed multi-agent DSE workflow,
not independently reproducible PPA or manufacturing conclusions.

A convincing follow-up would hold the candidate space, evaluator, initial
designs, total evaluations, random seeds and stopping criterion constant. It would do so across
black-box Bayesian optimization, prior LLM-DSE, single-agent analysis and
AgenticDSE. It would report valid-candidate rate, search overhead, best-so-far
PPA, hypervolume, Pareto distance and diversity per seed. It would then re-evaluate
selected designs with an independent architectural and physical flow. Test a
held-out chiplet template or technology and include the cost of correcting an
invalid or misleading agent proposal. Until those conditions are exposed, the
claim remains a promising search-orchestration direction. Evidence about transfer
and end-to-end design value remains open.

<span id="explanation-dac-2026-research577"></span>

## Hyb-HANAS: a calibrated quantum-cost proxy must survive actual device execution

Quantum machine-learning architecture search chooses a quantum circuit and a classical network together. The quantum portion is not characterized by gate count alone. Native-gate duration, two-qubit routing, repeated shots, decoherence and device noise matter too. They can make two circuits with similar abstract size have very different execution cost and output quality. A cost model therefore influences which architectures are searched, but it is not itself a quantum execution result.

The source proposes Hyb-HANAS, a multi-objective NAS procedure using NSGA-II to optimize accuracy, execution time and parameter count. Its quantum cost model uses real-device calibration data and includes gate durations, routing overhead and noise-induced inefficiency. A classical model converts FLOPs into equivalent units. The two sides can then be combined into one hybrid cost metric. This changes the search objective and candidate ranking. It does not establish that the analytical estimate remains accurate after compilation or on a new calibration snapshot. It also does not establish this for a circuit that is actually executed on hardware.

The first gate is cost-model validity. Define the native gate set, device topology, compiler/transpiler, routing policy and gate-duration table. Also define error and coherence assumptions, number of shots, queue/compilation boundary and calibration age. Compare predicted cost with independently measured wall-clock time, routed operations, fidelity or success probability and energy where relevant. Use held-out circuits, workloads and calibration conditions. A model calibrated on the same circuits it ranks can reward its own errors.

The second gate is search validity. State the hybrid architecture space, quantum embedding and ansatz, qubit count, and depth and two-qubit-gate limits. Also state datasets, train/test split, optimizer, seeds, NSGA-II population and evaluation budget. Report convergence, Pareto-front construction, candidate failures, quantum and classical training cost, shots and retraining. Compare accuracy-only NAS, hand-designed circuits and simpler gate-count/depth costs under the same compiler, device, noise, training and final-evaluation boundary. Ablate the calibration, routing, noise and classical-FLOP terms to show which term changes the selected architectures.

The official description establishes a hardware-aware hybrid quantum-NAS proposal. It provides no numerical accuracy, circuit depth or calibrated-versus-measured cost error. It also provides no hardware execution time, noise/fidelity result, Pareto quality, search overhead or held-out-device validation. Device calibration may be specific to one processor and become stale as operating conditions change. The evidence supports calibrated-cost-guided QML architecture search, not demonstrated quantum advantage, calibrated execution-cost accuracy or transferable hardware benefit.

<span id="explanation-dac-2026-research1859"></span>

## iPCL-M: a fast layout metric is useful only if the optimized result remains physically legal

ASIC physical design turns a gate-level netlist into placement, routed wires and eventually a GDS-II layout. Routing metrics such as wirelength, delay, slew, resistance and capacitance are coupled. Changing one path can alter congestion, parasitics, timing and the legality of neighboring connections. A learned metric evaluator can make search cheaper, but its prediction is not itself a routed or signoff-checked layout.

iPCL-M is described as a pre-trained chip-layout model inside a Generate--Evaluate--Optimize--Generate (GEOG) loop. A pre-routing generation model predicts routing metrics. Post-processing enforces connectivity. An evaluation model estimates the candidate. Optimization feeds the result back into generation. The claimed mechanism changes how candidates are proposed and scored. It does not establish that the layout representation transfers across netlists or process conditions. It does not establish that zero post-processing error means physical validity. It also does not establish that the selected candidate survives extraction and timing signoff.

The first gate is metric calibration. Define the movement unit, relative-error denominator, and net and cell weighting. Also define timing and slew definitions, resistance/capacitance extraction, clock treatment and congestion boundary. Report absolute error, bias, tail error and per-design results on held-out layouts, netlists, design families, technologies and routing conditions. Compare the learned evaluator with iSTA and task-specific predictors using the same input data, reference flow, constraints and hardware. A 336× evaluator speedup must state whether preprocessing, model inference, reference labels and failed cases are included.

The second gate is physical validity and optimization cost. A post-processing step that makes a predicted metric numerically exact may only reconstruct a target value. It does not prove legal geometry or correct parasitics. Run connectivity, design-rule, antenna, density, extraction, static-timing and signal-integrity checks with named PDK/tools. Report unrouted nets, repairs, violations, timing closure, area, power, wirelength and total GEOG time across every iteration. Compare against handcrafted features, task-specific learned models and commercial routers under identical netlists, placement, constraints, technology and signoff boundary. “Superior to commercial tools” needs per-design results and a defined key-metric set, not only a favorable aggregate.

The official description reports 1% mean relative error and below-one-movement-unit mean absolute error for pre-routing generation. It reports zero MRE/MAE after post-processing with connectivity. It reports evaluation comparable to iSTA with a 336× speedup. It also reports improvements of 10.49% wirelength, 13.03% delay, 14.85% slew, 10.51% resistance and 6.46% capacitance. It also claims routing results superior to commercial tools on key metrics. The captured evidence omits design splits, metric units, PDK/node/tool conditions, error tails, search cost, PPA, routing failures and signoff evidence. It supports a learned closed-loop layout-metric optimization direction, not demonstrated transferable or signoff-quality physical-design improvement.

<span id="explanation-dac-2026-research365"></span>

## Practice-informed macro placement: a useful RL action mask still needs routed timing closure

Macro placement assigns large memories, IP blocks and other fixed-shape objects before standard-cell placement and routing. Their positions determine wirelength, congestion, pin access, whitespace and power-domain legality. They also determine the timing of the routes that will later connect them. A generic RL agent can spend many actions on invalid or impractical layouts. Design practices can constrain the search. However, a constrained proposal is not automatically legal or signoff-quality.

The described framework embeds practice through an action mask. The mask covers peripheral placement, dead-space avoidance and proximal placement of macros that share design hierarchy and physical footprint. It forms macro clusters from hierarchy and footprint and uses clusters as placement units. It jointly explores cluster location and tiling pattern with a compaction method intended to reduce grid waste. These mechanisms change the action space and search granularity. They do not specify mask semantics, cluster thresholds, reward terms, legality repair, pin/keepout handling, congestion model or detailed-flow integration.

The first gate is physical validity. Check macro overlap and orientation, halos, blockages, power domains, density, pin access and high-fanout nets. Also check clock structure, routing completion, extraction and static timing after detailed placement and route. Record invalid proposals, repairs, unroutable designs, design-rule violations, timing failures and post-route WNS/TNS. An action mask can exclude known bad moves while still creating a legal-looking placement that blocks routing or worsens parasitics.

The second gate is search and cost accounting. Expose cluster formation, compaction/grid rules, action masking, and reward terms and normalization. Also expose exploration, seeds, training data, model inference, failed flow runs and stopping criterion. Count placement steps together with mask computation, clustering, compaction, repair, placement, routing, extraction, timing and human review. Compare expert heuristics, standard RL and commercial placers. Use the same netlists, floorplan, macro rules, PDK/tools, timing constraints, seeds, repair budget and post-route boundary.

Practice priors need a transfer test. Hold out complete industrial designs, hierarchy patterns, macro mixes, process/node and constraint regimes. Vary aspect ratios, blockages, high-fanout structure and congestion. Report per-design results, timing-closure/routability rate, wirelength, congestion, area, power, absolute WNS/TNS, runtime and tails rather than only an average improvement. A policy trained on one organization's floorplanning style may reproduce that style without learning a portable physical objective.

The official description claims expert-level placement quality and consistent improvement over three commercial macro placers on industrial designs. It also claims reduced turnaround time. It also claims up to 25.37% WNS and 39.51% TNS improvement over five SOTA placers on public benchmarks. It does not expose absolute WNS/TNS, wirelength, congestion, area, power, runtime, routability, timing-closure rate, design split or post-route conditions. The evidence supports practice-informed RL macro placement, not demonstrated portable expert parity, routability, timing closure or full-flow turnaround improvement.

<span id="explanation-dac-2026-research2560"></span>

## Expert-level RL placement: learning an expert endpoint is not the same as learning a transferable physical objective

Placement assigns cells and macros to physical locations before routing. A good placement must balance wirelength, density, congestion, pin access, timing, power and later routing feasibility. These objectives interact. A placement with short estimated connections can create a local congestion hotspot or a timing failure after parasitic extraction. An RL reward therefore determines which physical compromises the agent learns. However, reward quality is not the same as implementation quality.

The source proposes learning the latent reward behind expert layouts rather than hand-formalizing an intricate placement process. Starting from final expert layouts, it reconstructs step-by-step expert trajectories and trains from demonstrations or preferences. The resulting reward guides an RL placement policy. This changes the supervision and reward-design mechanism. It does not establish whether the inferred reward identifies causal constraints. It does not establish whether a single expert design is enough to cover other netlists. It also does not establish whether the policy's placements survive the downstream physical-design flow.

The first gate is reward and data validity. State the placement state and action space, trajectory extraction, and demonstration versus preference labels. Also state reward model, normalization, uncertainty, policy algorithm, initialization and repair. Compare against wirelength-only RL, handcrafted multi-objective rewards, expert heuristics and direct imitation. Use the same expert data, seeds and evaluation budget. Test whether reward rankings predict independently measured placement quality. Also ablate the expert-reward, preference and trajectory components rather than attributing every gain to RL.

The second gate is physical validity and transfer. Check legal cell and macro locations, overlaps, density, blockages, pin access, congestion and clock structure. Also check routing completion, extracted parasitics, static timing, slew, area and power with a named PDK and tool flow. Include failed placements, repairs, routing, timing closure and signoff in total cost. Hold out complete designs, netlist families, macro mixes, constraints and technology conditions. “Unseen cases” must be defined. A one-design result must report how much expert data and retraining it consumes.

The official description claims expert-quality layouts, efficient learning from even a single design and good generalization to unseen cases. It provides no design count, held-out split, reward details, wirelength, congestion, timing, PPA, runtime, routability or post-route result. The evidence supports expert-demonstration-guided RL placement, not demonstrated expert parity, transferable placement quality or post-route physical improvement.
