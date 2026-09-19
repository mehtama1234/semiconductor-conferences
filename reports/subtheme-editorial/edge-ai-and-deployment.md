## Deployment begins with the device's actual limits

An edge application runs near its user or data source. Its device may have limited memory, power, cooling, and network access. The model must meet an output-quality requirement while sharing those resources with the rest of the application.

The useful measurement is therefore the complete application response under the intended conditions. A fast internal operation can coexist with a slow response if loading, preprocessing, transfers, or scheduling dominate. A short benchmark can also miss the effect of sustained temperature and power limits.

## Memory and response time constrain different choices

Model parameters, intermediate values, and stored execution state all consume memory. Reducing one of these can make a model fit, but may add conversion, recomputation, or transfers. The minimum-memory configuration need not provide the fastest response.

Concurrent applications complicate the choice. Memory available during an isolated test may be unavailable during ordinary use. A deployment result should state what else runs on the device and whether its resource limits remain satisfied as requests or tasks change.

## On-demand sparsity changes which work is performed

The multi-task sparsity record proposes selecting sparse work according to the requested task. Sparsity permits some values or operations to be omitted under the method's rules. Dynamic selection can avoid unnecessary computation, but must identify the required work and distribute it efficiently. [Recorded evidence](../observed-subthemes/edge-ai-and-deployment.md#paper-dac-2026-research2030)

The comparison needs task accuracy, memory, latency, energy, and the overhead of changing tasks or sparse patterns. The captured description provides none of those measurements. It identifies a design approach while leaving its practical deployment benefit unresolved.

<span id="explanation-dac-2026-research2030"></span>

## On-demand multi-task sparsity: a smaller differential set must still produce the same useful task result

An edge platform may serve several models or tasks while sharing limited memory, compute and power. Sparsity can omit weights or operations under a defined approximation, but multi-task serving adds a second problem: the next task may need a different sparse structure. The system then pays for identifying the task, finding reusable state, loading missing blocks and reconfiguring execution before the first useful output.

The source proposes decomposing weights into reusable block-granular units, aligning sparse structures across tasks to maximize overlap, and dynamically loading only the differential blocks required by the next task. This changes the representation and switching policy. It does not by itself establish that each task retains its accuracy, that the sparse blocks map efficiently to the accelerator, or that the reported switch speed includes storage, DMA, metadata, cache and runtime work.

The first gate is task and sparsity correctness. State the models, tasks, data, quality target, pruning/training method, block size, sparsity ratio, overlap, metadata and unsupported patterns. Compare per-task outputs with a dense or trusted reference, report quality by task and input condition, and measure block reuse, differential-block size, load balance, dropped work and memory capacity. A small differential set can still produce a poor result if alignment forces irregular kernels or removes task-critical weights.

The second gate is complete switching cost. Measure task identification, metadata lookup, eviction, storage read, DMA, decompression or format conversion, cache fill, synchronization, kernel reconfiguration and time to first useful output. Separate cold and warm switches, p50/p95/p99 latency, throughput, energy, peak memory and irregular-kernel utilization. Hold task sequences, inter-arrival times, concurrency, hardware, power mode, runtime and warm-up policy fixed against dense multi-task, static task-specific pruning, monolithic sparsity and existing methods. Include the cost of constructing and storing aligned sparse representations.

The official description reports over 6.6× average task-switch acceleration on a real-world autonomous-driving platform, but provides no task accuracy, model/task set, sparsity or block conditions, latency distribution, memory traffic, energy, hardware/runtime settings or complete cold-start accounting. The evidence supports reusable block-granular multi-task sparsity, not demonstrated quality-preserving end-to-end edge efficiency or universal switching benefit.

## Speculative decoding changes the sequence of work

Speculative decoding proposes candidate model outputs and then checks whether they can be accepted by a validation procedure. Its potential saving depends on how much useful output is accepted relative to the work spent proposing and checking candidates.

SpecMoE's captured record proposes a self-assisted method for mixture-of-experts models. The description does not establish acceptance rate, the verification rule, output quality, batch size, or complete response time. Those conditions are necessary before treating the method as a faster way to produce equivalent useful outputs. [Recorded evidence](../observed-subthemes/edge-ai-and-deployment.md#paper-dac-2026-research257)

An input that causes many proposals to be rejected can have a different execution cost from an input whose proposals are accepted. A deployment experiment should include both the distribution of that behavior and its effect on slow requests.

<span id="explanation-dac-2026-research257"></span>

## SpecMoE: self-assisted speculation is useful only when accepted tokens preserve the target model

Speculative decoding proposes several future tokens with a cheaper draft path, then uses the target model to verify them. Accepted tokens can reduce the number of sequential target steps, but rejected proposals still consume draft and verification work and may require rollback. For an MoE target, expert routing and memory movement are part of both paths, so a proposal count is not the same as useful throughput.

SpecMoE is described as a memory-efficient MoE inference system using self-assisted speculative decoding without additional model training. The captured description does not specify whether the draft is a reduced expert path, a previous-layer/self model, a tree or a different token schedule, nor how target verification, acceptance, rollback, sampling and MoE routing are implemented. The claimed mechanism changes how candidate tokens are generated and checked; it does not by itself establish exact target-model semantics or quality preservation.

The first gate is acceptance and output fidelity. Define draft construction, target verification, acceptance/rejection, rollback, EOS, temperature/sampling and expert routing. Compare token distributions, logits, perplexity, task quality and rare-token behavior with standard autoregressive MoE decoding. Report proposed, accepted and rejected tokens per step, target evaluations, acceptance rate by position and workload, and whether the result is exact or an explicitly bounded approximation. A throughput gain with changed sampling semantics is not an equivalent inference result.

The second gate is complete serving cost. Measure draft work, verification, expert loads, cache reuse, memory/interconnect bytes, GPU/CPU utilization, synchronization, batch/concurrency effects, p50/p95/p99 latency, energy, cold/warm behavior and time to first token. Compare standard autoregressive decoding, external draft-model speculation and CPU-offloaded MoE under the same model, top-k routing, precision, context/generation lengths, batch, quality target, hardware and memory boundary. Include proposal, rejection, rollback and runtime scheduling overhead even though no additional model training is required.

The official description claims no additional training, up to 4.30× throughput and reduced memory/interconnect bandwidth requirements on memory-constrained systems. It provides no acceptance rate, model/trace conditions, quality definition, batch scaling, latency, energy, token/byte accounting or baseline boundary. The evidence supports self-assisted speculative MoE decoding, not demonstrated exact or quality-preserving end-to-end serving or universal throughput benefit.

## Processor-specific tuning needs an explicit hardware account

Inferweave's captured description concerns an inference stack for the MT-3000 processor. A software stack can arrange operations, memory use, and data movement to suit a particular device. That is a meaningful contribution when the resulting application improvement is measured under known conditions. [Recorded evidence](../observed-subthemes/edge-ai-and-deployment.md#paper-dac-2026-research1466)

The present record does not establish model configuration, throughput, response time, energy, memory, or reproducible settings. It cannot yet show whether the benefit comes from the proposed software, a device-specific feature, or a different comparison setup.

<span id="explanation-dac-2026-research1466"></span>

## InferWeave: regulating shared memory traffic can improve HUMA inference only if the model and total serving path remain equivalent

In a heterogeneous unified-memory architecture (HUMA), host and device compute units can access shared DRAM. That removes some explicit-copy boundaries, but it also makes operators compete for the same bandwidth. LLM inference alternates between phases and operators with different compute, tensor sizes and reuse; a static placement can leave one unit idle while another saturates DRAM. The relevant result is therefore not just kernel speed, but tokens produced under a complete memory, synchronization and quality boundary.

InferWeave is described as two coordinated mechanisms. An offline planner jointly chooses operator placement and data staging while treating DRAM bandwidth as a first-class constraint. A runtime bandwidth-aware asynchronous pipeline scheduler enforces the plan by regulating access rates and allowing host/device work to overlap without blocking. This changes the placement and memory schedule; it does not automatically define how dependencies, tensor ownership, reductions, unsupported operators or plan changes are handled.

The first gate is execution equivalence. Specify supported operators, tensor layouts, precision, host/device ownership, staging lifetime, asynchronous dependencies, reduction order, synchronization and fallback paths. Compare logits, perplexity and task outputs with a trusted reference across prompt/context lengths, prefill and decode, batch/concurrency, sampling settings and model sizes. A schedule that lowers DRAM contention but changes an output or silently falls back to a different kernel is not an equivalent inference result.

The second gate is bandwidth and total-cost accounting. Instrument DRAM bytes, channel utilization, queue depth, stalled cycles, operator placement, overlap, host/device transfers, staging memory, planner cost, runtime control, synchronization and throttling. Report tokens/s, time to first token, inter-token latency, p50/p95/p99 latency, energy and peak memory separately for warm steady state and cold start. Include plan generation, compilation, model loading, warm-up and background contention when claiming deployment benefit; offline work may be amortized only over a stated number of requests.

The third gate is baseline and transfer validity. Compare FlexGen, llama2.c, GPU-centric static placement and untuned MT-3000 execution with the same LLaMA/GPT versions, precision, prompt/generation workload, batch, memory capacity, DRAM/interconnect, libraries, quality target and end-to-end boundary. Test different model sizes, sequence lengths, decode concurrency and DRAM pressure, then repeat on another HUMA processor or clearly limit the claim to MT-3000. A processor-specific schedule can be valuable without being portable.

The official description reports LLaMA/GPT evaluation on MT-3000 and up to 2.3× higher throughput than FlexGen and llama2.c. It does not expose absolute tokens/s, model/precision conditions, latency, energy, DRAM profile, memory footprint, planning cost, model quality or cross-processor transfer. The evidence supports bandwidth-aware HUMA LLM scheduling, not demonstrated universal end-to-end inference improvement.

<span id="explanation-dac-2026-research2271"></span>

## PeFoo-L: reducing optimizer state is not the same as preserving the fine-tuning trajectory

Backpropagation stores activations and computes gradients through the model, so its memory cost grows with model depth, sequence length, batch and the set of trainable parameters. A forward-only optimizer avoids the backward graph by estimating how parameter changes affect the objective through additional forward evaluations. That can fit a tighter memory budget, but it changes the estimator, query count and optimization noise.

PeFoo adds a preconditioning strategy to the forward-only paradigm to address slow or unstable convergence. PeFoo-L then restricts preconditioner storage and weight updates to one layer per iteration, reducing live state and data traffic. The restriction is a systems mechanism as well as an optimization choice: it changes which parameters are current, how often layers are updated, and what state must move between memory and compute. It does not establish that the resulting update is equivalent to backpropagation or that fewer bytes produce the same final task quality.

The first gate is objective and update fidelity. Define the forward-only perturbation/query estimator, preconditioner, randomization, layer-selection schedule, update rule, precision, objective noise and stopping condition. Compare update direction or loss response with backpropagation where measurable, and plot loss/task quality against forward queries, wall time, data passes and energy. Iteration count alone is not a fair budget when one iteration uses several forward evaluations or different amounts of data.

The second gate is layer-state accounting. Report which layers are updated, order and frequency, parameter and preconditioner residency, stale-state behavior, optimizer/checkpoint state, reload cost, bytes moved and peak memory. Test model sizes, sequence lengths, trainable subsets, batch sizes and tasks with the same quality target and query/data budget. A single-layer update can reduce traffic while starving some layers or producing a slower, less stable trajectory; measure layer coverage and sensitivity rather than assuming uniform progress.

The third gate is actual edge feasibility. State the processor/accelerator, memory capacity and bandwidth, precision, storage, thermal/power mode, runtime and data placement. Include model loading, forward queries, preconditioner construction, layer swaps, checkpointing, communication, idle power and recovery in end-to-end adaptation time and energy. Compare backpropagation, an unpreconditioned forward-only optimizer such as MeZO, PeFoo without the single-layer restriction, and PeFoo-L under matched model initialization, data, quality, hardware and query/update boundary. Evaluate whether the adapted model's downstream quality is acceptable, not only whether it fits in memory.

The official description claims that PeFoo addresses slow/unstable forward-only convergence and that PeFoo-L reduces preconditioner memory and data traffic by restricting storage and updates to one layer per iteration. It provides no convergence curves, query count, final task quality, memory footprint, bandwidth, latency, energy or edge-device result. The evidence supports preconditioned forward-only edge fine-tuning as an optimization direction, not demonstrated gradient-equivalent training, competitive task quality or feasible end-to-end edge adaptation.

<span id="explanation-dac-2026-research3067"></span>

### Scale-Gest: model-space synthesis is a search problem, and runtime selection is a control decision

### What a gesture detector has to decide

Gesture detection maps sensor observations to a gesture label or event. A detector can be made smaller or faster by changing its architecture, but a single model may not be best for every device state, input condition, or resource budget. The deployment problem is therefore not only to train one accurate model. It is to provide a set of models and decide which one should run when.

Model-space synthesis means constructing candidate detector models with different accuracy, memory, compute, or latency properties. The record does not specify whether synthesis changes layers, widths, precision, input resolution, or another model parameter. That missing detail matters because each choice changes both the measured quality and the hardware work needed to produce an answer.

### What runtime selection changes

Runtime selection adds a policy that chooses among candidate models using current context. Context could include available memory, battery or thermal state, sensor conditions, required response time, or recent classification difficulty, but the captured description does not state which signals are used. The policy is part of the deployed system: it consumes time and memory, can change behavior between requests, and must itself be evaluated.

Selecting a smaller model can reduce compute while lowering gesture accuracy. Selecting a larger model can improve quality while increasing response time or energy. A useful selector must satisfy the application's quality constraint, not merely choose the cheapest model. If the device state changes during execution, the measurement must state whether the selected model can be changed safely and whether switching requires loading weights or rebuilding execution state.

### What the record establishes and what it does not

The official description establishes a proposal combining scalable model-space synthesis with runtime model selection for on-device gesture detection. It does not provide accuracy, latency, energy, memory, switching overhead, or results across devices and gesture conditions. It therefore supports a mechanism-level explanation, not a measured claim that Scale-Gest improves deployment.

The right comparison is a fixed detector under the same model-quality target, input stream, device and thermal condition. Report the candidate set, selector inputs, selection time, model-loading cost, peak memory, energy per decision, average and tail latency, and gesture accuracy for each operating point. Test changes in gesture speed, background, sensor quality, device load, battery state and temperature. Without those conditions, “scalable” describes the design space and “runtime selection” describes the control mechanism, but neither term establishes robust deployment benefit.

The [Scale-Gest](../observed-subthemes/edge-ai-and-deployment.md#paper-dac-2026-research3067) record describes model-space synthesis and runtime selection for on-device gesture detection. The detailed explanation above separates candidate construction from runtime policy, states the resource/quality tradeoff, identifies switching and selector costs, and preserves the official-description evidence boundary.

<span id="explanation-dac-2026-research293"></span>

### SkiST: memory-efficient SNN fine-tuning must preserve time-dependent state

### Why spiking-network fine-tuning has a different memory problem

A spiking neural network processes an input over time. A neuron does not usually produce its output from only the current input; it maintains a state that changes with incoming spikes and may emit a spike when the state satisfies a rule. Fine-tuning changes parameters so the network adapts to a task while this temporal behavior remains useful.

Backpropagation-through-time stores or reconstructs information from multiple time steps so that a later loss can influence earlier parameter updates. The memory cost is therefore related to the number of time steps, layers, stored activations and temporal state, not only to the number of parameters. Removing stored state can reduce memory but can also change the gradient calculation or the network's temporal behavior.

### What spatio-temporal adaptation is trying to change

The captured record describes SkiST as a memory-efficient fine-tuning method using spatio-temporal adaptation. “Spatial” concerns the network's units or connections at a given time; “temporal” concerns how state and activity evolve across time. A method with both components is attempting to reduce the information retained or processed during adaptation while preserving the information needed to learn from sequences.

The official description does not specify which state is stored, which state is recomputed, whether time steps are skipped or grouped, how gradients are approximated, or whether the method changes the forward inference path. Those details decide whether the method reduces peak memory, total memory traffic, update cost, or only the bookkeeping used by the training algorithm.

### What must remain equal in the comparison

Comparing SkiST with ordinary backpropagation-through-time requires the same SNN architecture, time horizon, input encoding, task, precision, optimizer budget and target quality. Report peak memory during forward and update phases separately, because a method can lower one peak while increasing total traffic or storing another form of state. Also report convergence steps, wall-clock training time, energy, final accuracy and any change in inference latency or spike activity.

The card's phrase “static SNN adaptation” is not enough to establish what baseline was used. A static model may mean fixed parameters, a non-temporal update rule, or a fixed sparse structure; these are different comparisons. The evaluation must define the baseline and show whether the adapted network retains temporal accuracy on sequences that differ from the fine-tuning data.

### What the record establishes and where it stops

The official description establishes a proposal for memory-efficient SNN fine-tuning using spatio-temporal adaptation. It does not report accuracy, memory, energy, convergence, latency or task results. It also does not establish whether reduced training memory transfers to an edge device, whether temporal state remains stable, or whether the method changes the deployed detector.

The [SkiST](../observed-subthemes/edge-ai-and-deployment.md#paper-dac-2026-research293) record is therefore evidence of a named method and intended problem, not a measured edge-training result. The detailed explanation above defines the temporal memory source, separates stored state from parameter count, identifies the missing algorithmic details, and states the conditions required for a fair comparison.

<span id="explanation-dac-2026-research239"></span>

### Edgesc: stochastic arithmetic trades deterministic precision for a statistical representation

### What edge detection computes

An edge detector identifies locations where image intensity changes. A conventional detector represents each pixel and intermediate value with a fixed numerical format, applies filters or comparisons, and produces an edge map. The output is useful only if the detector preserves the boundaries that matter for the image task.

Stochastic computing represents a numerical value through a bitstream. The value is encoded by a property such as the fraction of bits that are one. Arithmetic can then be implemented with simple logic, but the result is an estimate whose error depends on bitstream length, correlation and the encoding scheme. A longer stream can reduce random estimation error while increasing time, switching and storage cost.

### What a universal stochastic architecture must cover

Edgesc is described as a universal stochastic-computing architecture for edge detection. “Universal” means the same architecture is intended to support more than one edge-detection situation; it does not by itself establish support for every sensor, image distribution, precision or filter. The architecture must define how pixels become stochastic streams, how streams are combined, how intermediate values are represented, and how the final stream becomes a binary edge decision.

The main design tension is direct. Simple stochastic logic can reduce circuit complexity or make approximate arithmetic easier to implement, but the detector then pays for stream generation, stream length, correlation control and statistical variation. If two input streams are correlated, an operation that assumes independence can produce a biased result. If the stream is too short, the edge decision can move because of representation noise rather than an image change.

### What must be measured

Compare the same edge detector and image set at matched output quality. Report precision-recall or another defined edge-quality metric, false positives and false negatives, bitstream length, input correlation, thresholding rule, latency, area, energy and power. State whether the comparison includes random-number generation, stream conversion, buffering and output decision logic. Test different image noise levels, contrast levels, sensor sources and operating temperatures if the claim concerns edge deployment.

The fixed-point baseline must use the same filter, threshold and quality target. A stochastic design that uses less arithmetic area but needs longer streams can have lower area and higher latency; a design that lowers power per operation can still consume more total energy per image. These quantities cannot be collapsed into a single “efficient” claim without their denominators and measurement boundary.

### What the record establishes and where it stops

The official description establishes a proposed universal stochastic-computing architecture for efficient edge detection. It does not report detection quality, bitstream length, area, power, latency or sensor results. It therefore does not establish that stochastic variability is controlled, that the architecture is universal in the strong sense, or that it improves a complete embedded vision workload.

The [Edgesc](../observed-subthemes/edge-ai-and-deployment.md#paper-dac-2026-research239) record is evidence of a named architecture and target application. The detailed explanation above defines stochastic numerical representation, identifies stream length and correlation as correctness conditions, separates per-operation cost from per-image cost, and preserves the official-description evidence boundary.

<span id="explanation-dac-2026-research124"></span>

### FlashFPS: farthest-point sampling keeps a coverage rule while trying to remove repeated distance work

### What farthest-point sampling does

Given a point cloud and a requested sample count, farthest-point sampling chooses a smaller set of points intended to cover the geometry. A basic procedure chooses an initial point, computes each unselected point's distance to the selected set, and repeatedly chooses the point whose distance is largest. After a point is selected, each remaining point only needs its distance to the new point compared with its previous distance to the selected set. Its maintained value is the minimum distance to any selected point.

The max-min rule matters. A point is preferred when it is far from the points already selected, so the sample tends to spread over the cloud rather than follow local density alone. It is not the same objective as random sampling. Random sampling may be useful as a baseline, but it does not preserve the same coverage rule and can miss small or sparse regions.

### Where the cost comes from

For (N) input points and (K) selected points, a direct implementation performs distance updates across many of the (N) points for each selection. It also stores coordinates and a current minimum-distance value for each candidate. Large point clouds make both distance arithmetic and memory traffic expensive, especially when the sample is consumed by a later 3D detector or registration stage.

FlashFPS is described as using pruning and caching. Caching can reuse distances or intermediate candidate information rather than recomputing it. Pruning can avoid evaluating candidates that cannot become the farthest point under a bound. Both mechanisms are safe only when their reuse or bound preserves the required selection rule, or when the method explicitly accepts an approximation. A stale cached distance or an unsafe bound can change which point is selected and therefore change the geometric coverage.

### What an efficiency claim must preserve

The comparison must state the point-cloud size, dimension, sample count, initial-point rule, distance metric, pruning rule, cache size and whether the result is exact or approximate. Report total runtime, distance evaluations, peak memory, bandwidth, energy and the effect of parallel execution. If pruning changes the selected points, report geometric coverage or distance-to-sample error, not only runtime.

Downstream accuracy must be measured with the same sampled points supplied to the same 3D model, preprocessing and training or inference condition. A sampler can run faster while losing a thin object, a distant cluster or a low-density region that matters to detection. Conversely, a small sampling error may have no task effect for one workload and a large effect for another. The sampling metric and downstream metric answer different questions.

### What the record establishes and where it stops

The official description establishes a pruning-and-caching proposal for efficient farthest-point sampling on large point clouds. It does not report runtime, memory, distance error or downstream accuracy, and it does not establish whether the method is exact, approximate, or validated across nonuniform clouds.

The [FlashFPS](../observed-subthemes/edge-ai-and-deployment.md#paper-dac-2026-research124) record is therefore evidence of a named sampling mechanism, not a measured point-cloud deployment result. The detailed explanation above defines the max-min state, explains where direct cost comes from, identifies correctness risks in pruning and caching, and separates sampler efficiency from downstream perception quality.

<span id="explanation-dac-2026-research1691"></span>

### Always-on visual wakeup: the detector must spend almost no power before an interaction exists

### What a visual wakeup subsystem does

An always-on interaction system cannot keep the full vision pipeline running at its ordinary power cost while waiting for an event. A wakeup subsystem observes a sensor stream, extracts enough information to detect a target event, and activates a larger processor when the event is likely. The subsystem is a gate before the main computation, not the complete visual application.

Its decision has two main error types. A false negative misses a real interaction and leaves the main system asleep. A false positive wakes the larger system when no useful interaction exists, consuming extra energy and possibly interrupting the user. The acceptable balance depends on event frequency, response-time requirement and the energy cost after wakeup.

### Why the sub-milliwatt boundary is not a complete system result

The title reports a sub-mW target for the visual wakeup accelerator, but the captured record does not state whether this is sensor power, accelerator power, average power, active power or total always-on subsystem power. It also does not state the duty cycle, frame rate, sensor interface, memory, clock, process or whether wakeup and downstream processing are included.

Average energy per hour depends on more than the detector's active power. If the detector runs continuously, its power is paid continuously. If it wakes periodically, the sampling interval changes miss probability and latency. If it wakes a larger vision pipeline, the event rate and false-positive rate determine the downstream energy. A low-power front end can therefore increase total energy if it generates too many false wakeups.

### What must be measured for an always-on claim

Report sensor input rate, resolution, detector active and idle power, duty cycle, memory and process, along with true-positive rate, false-positive rate, false-negative rate and detection latency. Measure energy per unit time at several event rates and scene conditions, including long idle periods. Include the sensor interface, clocking, buffering, wakeup signal and the powered system that runs after a positive decision.

Compare against always-on CPU vision and sensor-triggered wakeup at the same event-detection quality and response-time target. A sensor trigger is not an equivalent baseline if it has less visual information or a different miss rate. Report the operating point rather than only a thresholded accuracy number, because moving the threshold changes both missed interactions and unnecessary wakeups.

### What the record establishes and where it stops

The official description establishes a visual wakeup accelerator subsystem intended for sub-milliwatt smart-glasses operation. It does not establish the measured power boundary, detection quality, latency, duty cycle, scene distribution or end-to-end energy. It therefore supports the design target, not a verified always-on deployment result.

The [Towards Always-on Interaction](../observed-subthemes/edge-ai-and-deployment.md#paper-dac-2026-research1691) record is evidence of a named wakeup subsystem and application. The detailed explanation above separates front-end power from complete-system energy, defines false-wakeup consequences, and states the measurements required to evaluate an always-on claim.

<span id="explanation-dac-2026-research1900"></span>

### KERV: speculative decoding for an embodied controller must preserve action validity, not only token throughput

### What a VLA control loop produces

An embodied vision-language-action model receives observations and instructions and produces actions or an action sequence for a robot. The action output is consumed by a control loop with a timing budget. A result that arrives after the robot has moved, or after the observation is stale, can be less useful even if the model produced the same textual or numerical action.

Speculative decoding uses a faster draft process to propose several next outputs and a target process to verify them. Accepted proposals can reduce the number of expensive target-model steps. Rejected proposals still consume draft work and verification work, and the system must preserve the target model's defined output rule if it claims equivalent generation.

### What kinematic rectification can mean

Kinematics describes how a robot's configuration and motion variables constrain feasible movement. A kinematic-rectification method may modify, filter or rank proposed action sequences using those constraints before they are used or verified. The captured description does not state whether rectification occurs in the draft model, the verifier, a post-processing stage, or the controller.

That location changes the claim. Rectifying a proposal can reject physically inconsistent actions, but it can also add computation, alter the proposal distribution, or cause the accepted action to differ from the target model's unrectified output. A valid evaluation must define whether the objective is exact model-output preservation, higher task success, lower control latency, or some combination.

### Why language-model acceptance is not enough

Token acceptance rate measures how much draft output the target process accepts under a specified verification rule. It does not by itself measure action quality, control-loop delay, trajectory smoothness, collision avoidance, task completion or energy. A sequence can have high acceptance while arriving too slowly, or low acceptance while still completing a task if the rectifier produces useful actions.

Measure observation-to-action latency, action age at execution, accepted action rate, target and draft compute, rectification cost, control frequency, task success and failure modes. Test changing scenes, instruction lengths, robot configurations, motion speeds and disturbances. If the robot is physical, report the simulator or robot boundary and do not treat an offline trajectory score as robot-in-loop validation.

### What the record establishes and where it stops

The official description establishes a kinematic-rectified speculative-decoding proposal for embodied VLA models. It does not report token acceptance, control latency, task success, safety or energy, and it does not define where rectification occurs or how physical constraints are enforced.

The [KERV](../observed-subthemes/edge-ai-and-deployment.md#paper-dac-2026-research1900) record is therefore evidence of a named inference approach, not a verified real-time robot result. The detailed explanation above separates draft/target computation, kinematic feasibility, control-loop timing and task outcomes, and preserves the official-description evidence boundary.

<span id="explanation-dac-2026-research1960"></span>

### HyperLiDAR: post-deployment adaptation must identify what changed and what evidence updates the segmenter

### What LiDAR segmentation produces

LiDAR segmentation assigns a class or label to points or regions in a three-dimensional scan. The scan distribution can change after deployment because of weather, lighting interactions with surfaces, sensor calibration, mounting, traffic, geography, object frequency or the operating device. A model that worked on its training distribution can become less accurate when the relationship between scan features and labels changes.

Post-deployment adaptation is an update made after the system is operating. It may change a classifier, a representation, a threshold or a small set of stored prototypes. The update requires some evidence about the new environment. That evidence can be labeled examples, weak signals, repeated observations, confidence statistics or an assumption that the environment has a particular structure. “Adaptive” does not mean that labels, memory or compute are unnecessary.

### What hyperdimensional computing represents

Hyperdimensional computing represents information with high-dimensional vectors and combines those vectors using defined operations. A class can be represented by a prototype built from encoded features; a new point or local pattern can be compared with prototypes, and the closest or most compatible prototype determines the label. The exact encoding, dimension, similarity measure, update rule and hardware representation determine the memory, arithmetic and adaptation behavior.

The representation can make some updates simple, such as adding evidence to a prototype, but simple updates do not establish correct adaptation. If new observations are unlabeled, an update needs a rule for deciding which class or prototype they support. If observations are mislabeled or the environment contains a new class, online updates can reinforce an error or erase useful earlier information. Adaptation therefore needs a drift trigger, update scope, protection against forgetting, and a way to measure whether performance improved.

### What the comparison must hold constant

Compare HyperLiDAR with a fixed segmentation model and a conventional online-adaptation method on the same sequence of environmental changes. Report labeled and unlabeled data available after deployment, update frequency, adaptation time, memory written, energy, point throughput and the time between drift and recovery. Measure segmentation quality before adaptation, during drift, after adaptation and on a held-out environment.

Separate the cost of inference from the cost of updating. A method can use little arithmetic per point while spending substantial energy collecting evidence or rebuilding prototypes. Report class-wise quality and rare-object performance, because an aggregate score can hide degradation on classes that determine safety or utility. State whether the sensor and calibration remain fixed; otherwise sensor change and model adaptation are confounded.

### What the record establishes and where it stops

The official description establishes an adaptive hyperdimensional-computing approach for post-deployment LiDAR segmentation. It does not report segmentation accuracy, adaptation time, energy, memory or drift results, and it does not specify the evidence or labels used for adaptation. It therefore supports a mechanism proposal, not a demonstrated post-deployment improvement.

The [HyperLiDAR](../observed-subthemes/edge-ai-and-deployment.md#paper-dac-2026-research1960) record is evidence of a named adaptive segmentation direction. The detailed explanation above defines the deployment-shift problem, states what hyperdimensional representation contributes, identifies online-update failure modes, and preserves the official-description evidence boundary.

<span id="explanation-dac-2026-research2058"></span>

### SharedKD: dynamic student discovery chooses a detector capacity during training, but the choice must still be validated on the target distribution

### What knowledge distillation changes

A large 3D detector can serve as a teacher and a smaller detector can serve as a student. The student is trained not only against ground-truth labels but also to reproduce information from the teacher, such as class scores, box predictions or intermediate features. This can transfer useful behavior while reducing the computation or memory needed by the deployed model.

The teacher and student have different roles. A teacher may be expensive but provide a training signal; the student is the model that must meet the deployment budget. A smaller student is not automatically better: removing capacity can reduce localization or rare-object quality, while keeping extra branches can preserve training cost or inference cost.

### What dynamic student discovery is deciding

SharedKD is described as gradient-guided dynamic student discovery inside a single 3D object detector. The phrase suggests that gradient information is used to choose or adjust a student configuration rather than committing to one fixed student before training. The captured description does not specify whether the choice changes depth, width, resolution, precision, branches, features, or another structural property.

A gradient measures how a selected loss changes locally when a parameter or choice changes. It can identify which direction reduces that loss under the current batch and training state. It does not by itself prove that a discovered student will perform well on future scenes, different sensors, rare objects, or a different compute budget. A dynamic choice can also add search, memory and control overhead during training.

### What must be kept separate in the evaluation

Measure student discovery cost separately from the final student's inference cost. Report the candidate space, gradient signal, selection frequency, training memory, training time, number of evaluated students and whether discarded candidates require computation. For the deployed student, report parameter and activation memory, latency, energy, throughput and detector quality at matched hardware settings.

Use the same point-cloud preprocessing, sensor configuration, coordinate system, training data and evaluation split when comparing fixed distillation, dynamic discovery and the full-size detector. Then test held-out sensors, weather, density, range, object sizes and class imbalance. Report class-wise detection and localization quality, because a lower average cost can hide loss on small or rare objects.

### What the record establishes and where it stops

The official description establishes a gradient-guided dynamic student-discovery proposal for 3D detection distillation. It does not report detection accuracy, latency, memory, energy, discovery overhead or the selected-student behavior, and it does not establish whether the discovered student remains effective under sensor or training-distribution changes.

The [SharedKD](../observed-subthemes/edge-ai-and-deployment.md#paper-dac-2026-research2058) record is evidence of a named distillation mechanism, not a measured deployment result. The detailed explanation above separates teacher signals from deployed computation, local gradient guidance from generalization, discovery overhead from inference cost, and average detector quality from rare-object behavior.

<span id="explanation-dac-2026-research2372"></span>

### TsetlinWiSARD: on-chip learning changes stored discrete state in response to feedback

### What a weightless neural network stores

A conventional neural network stores numeric weights and updates those weights during training. A weightless or rule-based network can instead store discrete states, Boolean decisions, lookup contents or clause configurations. Its computation may be built from input literals and logical combinations rather than multiply-accumulate operations.

The absence of numeric weights does not mean the model has no state. The state determines which input conditions contribute to a class decision and how strongly or often those conditions are selected. Training changes that state based on examples and feedback. The memory representation, update rate and initialization therefore determine both learning behavior and hardware cost.

### What Tsetlin automata contribute

A Tsetlin automaton is a finite-state decision process that chooses between actions such as including or excluding a literal in a rule. Feedback moves its state toward one choice or the other. A collection of automata can form clauses, and clauses can vote for classes. This provides a hardware-friendly learning rule using discrete state transitions, but the result depends on feedback probabilities, state depth, clause count, input encoding and task structure.

The captured record calls the artifact TsetlinWiSARD and describes on-chip Tsetlin-automata training on an FPGA. It does not specify how the WiSARD and Tsetlin components are combined, whether updates are supervised, how state is initialized, or how the training schedule maps to FPGA memory and logic. Those details are necessary to understand what is learned and what the FPGA actually executes.

### What “on-chip training” includes

On-chip training means that some learning update occurs using hardware resources on the FPGA while the device is operating. It does not automatically mean that the entire training pipeline is self-contained. Data acquisition, labels, loss or feedback generation, update storage, host transfers, reconfiguration, initialization and checkpointing may still occur outside the chip.

A valid comparison must state whether it compares the same model after offline training, a conventional FPGA training engine, or the complete training-and-deployment workflow. Report accuracy over time, convergence examples, update throughput, logic and memory use, clock frequency, latency, energy per update, initialization cost and the effect of limited precision or discrete state. Test both stationary and changing data, because a rule system can fit one task while adapting poorly to another.

### What the record establishes and where it stops

The official description establishes an FPGA implementation of on-chip Tsetlin-automata training for a weightless neural network. It does not report accuracy, convergence, FPGA resources, latency, energy or datasets, and it does not define the TsetlinWiSARD state or update path in the captured evidence.

The [TsetlinWiSARD](../observed-subthemes/edge-ai-and-deployment.md#paper-dac-2026-research2372) record is therefore evidence of a hardware-learning direction, not a demonstrated on-device training result. The detailed explanation above separates discrete model state from “no weights,” automaton feedback from general learning quality, and on-chip updates from a complete self-contained training workflow.

<span id="explanation-dac-2026-research920"></span>

### Adaptive spiking detection: event-driven execution and adaptation are separate sources of behavior

### What a spiking detector processes

A frame-based detector receives an image at a defined frame rate and runs a fixed computation for that frame. A spiking detector receives events or spike trains over time. A neuron accumulates state and emits a spike when its state meets a threshold or another firing rule. Later layers process those spikes, so work and timing depend on event arrivals rather than only on a fixed frame count.

Event-driven execution can avoid work when little changes in the scene, but it can also produce more events when motion, sensor noise or illumination changes. Its latency is tied to the information needed for a decision and the time over which events arrive. “Real-time” therefore requires a deadline and an input timing condition; it is not established by saying that the model uses spikes.

### What adaptive means in this detector

Adaptation changes a model or its neuron behavior as scene conditions change. Possible targets include firing thresholds, membrane time constants, synaptic state, routing, precision or a learned classifier, but the captured description does not identify the target or the update signal. The update may occur during inference, between sequences, or during a separate training phase; these have different memory, latency and stability costs.

An adaptive threshold can reduce unnecessary spikes under one event rate and miss weak signals under another. An adaptive state can respond to a new scene while retaining stale information from the old scene. The method therefore needs a defined adaptation trigger, update time, protected state, reset behavior and evaluation sequence. Adaptation is not automatically generalization.

### How to compare frame and spike systems fairly

Use the same camera or event-sensor information, target classes, annotation timing and detection quality requirement. Report event rate, frame rate if a frame conversion is used, observation-to-decision latency, deadline attainment, energy per decision, peak memory, spike count and accelerator utilization. Separate sensor and conversion cost from detector cost.

Compare a static SNN and a frame-based detector at matched quality and response deadline. Test static scenes, fast motion, changing illumination, sensor noise, crowded scenes and event-rate bursts. Report missed and duplicate detections, small-object quality and tail latency; average latency can hide frames or events that miss the control deadline.

### What the record establishes and where it stops

The official description establishes an adaptive spiking-neural-network direction for real-time multi-object detection. It does not report detection accuracy, latency, energy, event rate or hardware results, and it does not specify the adaptive state or update schedule. It therefore supports a mechanism proposal, not a verified real-time or energy advantage.

The [Adaptive Spiking Neural Networks](../observed-subthemes/edge-ai-and-deployment.md#paper-dac-2026-research920) record is evidence of a named detector direction. The detailed explanation above separates event-driven execution from adaptation, defines the timing and event-rate dependencies, and states the measurements needed to compare it with frame-based and static-spiking baselines.

<span id="explanation-dac-2026-research952"></span>

### DeltaSight: redundancy elimination is safe only when later stages retain the information they need

### What a video AIoT pipeline does

A video AIoT system moves camera data through several stages. A stage may decode or resize frames, detect objects, track them, classify regions, estimate motion, or make a final decision. Each stage consumes data and produces an intermediate representation. The system pays for sensor input, memory movement, communication, computation and storage at each boundary.

Redundancy can appear across time, such as nearly unchanged regions in adjacent frames, and across stages, such as one stage recomputing information another stage already produced. Removing repeated work can lower bandwidth or energy, but only if the information removed is not needed by a later stage and the remaining representation preserves the final task's required quality.

### What “cross-stage consistent” has to mean

Independent stage processing lets each stage choose its own input and compression rule. Cross-stage consistency means that a decision to omit, reuse or transform data is coordinated with the stages that consume it. The system must know what representation a later stage receives, how long it remains valid, and what happens when a later stage needs a detail that was omitted earlier.

For example, reusing a previous region can reduce transfer and inference work while an object remains stable. It can also miss a small motion, an occlusion or a new object if the reuse condition is too permissive. A stage-local similarity score is not sufficient if the downstream classifier is sensitive to a feature that the upstream stage discarded. The elimination rule therefore needs a validity condition, a refresh trigger and a fallback path.

### Why stage-local savings do not establish end-to-end benefit

Report the complete camera-to-decision path. A method can reduce transmitted pixels while increasing metadata, consistency checks, cache storage, refresh traffic or synchronization. It can reduce one model's inference while increasing the next model's input preparation. The energy boundary must include the camera, sensor interface, memory, links, accelerators and control logic that enforce reuse.

Measure task accuracy and missed-event behavior under static scenes, camera motion, object motion, occlusion, lighting change, scene cuts and bursty activity. Report bandwidth, bytes transferred, stage latency, end-to-end latency, peak memory, energy per frame or decision, refresh rate and the fraction of data reused. Compare with independent stage processing and full-frame processing under the same quality and deadline target.

### What the record establishes and where it stops

The official description establishes a cross-stage consistent redundancy-elimination architecture for video AIoT systems. It does not report accuracy, bandwidth, latency, energy, memory or deployment results, and it does not specify the validity condition or fallback behavior for discarded data. It therefore supports a systems direction, not a measured end-to-end efficiency claim.

The [DeltaSight](../observed-subthemes/edge-ai-and-deployment.md#paper-dac-2026-research952) record is evidence of a named pipeline-optimization approach. The detailed explanation above defines cross-stage information dependencies, identifies refresh and fallback requirements, separates stage-local savings from complete-path cost, and preserves the official-description evidence boundary.

## How to measure a deployable improvement

State the device, software versions, input distribution, model, precision, and output-quality target. Measure the complete request from input arrival to usable output. Report model loading and setup separately, then include them when the application must pay them for each run.

Test sustained operation, competing tasks, and changing input sizes. Include peak memory, energy per request, average response time, and unusually slow requests. A method that meets the requirement only under isolated or short-run conditions needs that boundary retained.

The research connection is adaptation to constrained devices. The papers change different parts of the computation, so they require separate comparisons before their results can be combined into a deployment recommendation or a long-term claim.
