# Edge embedded and mobile systems

This subject has 6 records in the selected sample. This page explains where it fits, then presents all captured paper evidence without shortening the measurements or limitations.

[Definitions used in the paper records](../reading-guide-v1.md)

## Understand the parent subject first

- [Systems applications and workloads](../themes/systems-applications-and-workloads.md)

## Start with the work that must finish, and the resources available

An edge system computes near the place where data is collected or used. An embedded system performs a defined function inside a larger device. A mobile system also has changing location, connectivity, or power availability. These descriptions overlap, but none defines a single processor type or research method. The relevant question is which work must finish before which resources or opportunities disappear.

Inference uses an already trained model to produce an answer. Training changes the model using examples and feedback. A request deadline constrains one inference result; a training-time budget constrains a sequence of model updates. Faster inference does not establish faster learning. Finishing more training rounds does not establish a better model if the rounds use different devices, precision, or data.

For a request, account for input collection, waiting for service, transfers, computation, and output delivery. Some stages can overlap, but operations that depend on an earlier result cannot start before that result exists. A faster processor helps only the stages that use it. Moving a stage to another machine can reduce its execution time while adding transfer and queueing delay. If that machine becomes unreachable, the system needs an explicit wait, retry, local fallback, or failure rule.

The six records here are from the selected DAC 2026 sample. Three recovered version-1 manuscripts provide page-backed evidence: GPU task scheduling, MATCHA, and PHAROS. Their equivalence to final conference versions has not been established. Pegasus, RTFL, and SatSFL remain description-backed in this review. They should not inherit the evidence depth of their neighbors.

## Separate the questions before comparing results

| Paper | Unit of work | Decision being changed | Evidence needed for a stronger conclusion |
|---|---|---|---|
| Pegasus | Distributed model inference | Which experts reside locally and which requests run together | Equal answer quality, query changes, network and placement costs |
| RTFL | Federated training rounds | Device participation and numerical precision | Quality reached within time and energy budgets |
| GPU scheduling | One periodically released computation graph | Concurrent kernel sizes and execution dependencies | Valid execution-time assumptions and complete response-time bounds |
| SatSFL | Split training across satellites and ground | Approximate feedback during disconnection and compressed return traffic | Link traces, approximation error, and deployment boundary |
| MATCHA | Neural-network inference on one chip design | Operation placement, splitting, memory, and overlap | Complete model latency including communication and coordination |
| PHAROS | Repeated jobs across an accelerator pipeline | Hardware partitioning and runtime scheduling | The precise timing guarantee, arrival assumptions, and preemption cost |

<span id="explanation-dac-2026-research1922"></span>

## Pegasus: why distributed edge MoE inference is a placement and communication problem

### Start with the computation

A mixture-of-experts (MoE) language model has a shared routing step and several alternative expert networks. For one token, the router selects a small subset of experts instead of executing every expert. This reduces arithmetic for that token, but it does not make the full model small: the expert parameters still have to be stored somewhere, and the selected expert may not be on the node that received the request.

That creates three distinct costs. The first is **expert computation**: the selected expert must perform its matrix operations. The second is **expert movement**: the token representation may have to cross an edge-to-edge link, and the result may have to return. The third is **queueing**: a node can have the right expert but still be busy serving earlier requests. A latency result is meaningful only when these costs are measured over the same request and quality conditions.

### What the three Pegasus mechanisms change

Pegasus addresses different parts of this chain rather than applying one generic speedup.

1. **Similarity-based expert deployment** chooses which experts to place at which nodes using a measure of semantic relevance between queries and experts across nodes and time. This attempts to make the likely expert local. It does not guarantee that the selected expert is always local, because future queries can differ from the history used for placement. It also creates a placement-update problem: moving experts consumes memory bandwidth and communication capacity, and a placement policy can become stale.

2. **Personalized gating** fine-tunes part of the routing function separately at each node. The routing decision can therefore reflect local query patterns and local expert availability. This changes model behavior as well as execution location. A lower communication cost is not enough to call the result equivalent to the original model; the evaluation must show the task-quality measure, the amount of local fine-tuning, its training cost, and the behavior when the query distribution changes.

3. **Adaptive local batching** groups requests at a node so the hardware can use memory and compute more efficiently. Batching can improve completed requests per unit time, but it can also make an early request wait for later requests. The system must therefore report both per-request latency and throughput, including the time spent waiting to form a batch.

The official description reports 11.8× lower inference latency than unnamed distributed MoE frameworks. It does not identify the models, node count, expert count, link, batch policy, request distribution, quality metric, or baseline resource parity. The source therefore supports understanding the proposed mechanism and the question it targets; it does not establish a universal 11.8× result, communication reduction, or quality-preserving substitution. [Source: official DAC description and captured record](https://63dac.conference-program.com/presentation/?id=RESEARCH1922&sess=sess176).

### The evaluation that would establish the claim

Use the same model, prompts, quality criterion, node resources, network conditions, and arrival trace for every baseline. Report at least: expert-local versus remote dispatches; bytes transferred; placement-update traffic; routing fine-tuning time; batch-formation wait; service time; tail latency; throughput; energy; and task quality. Evaluate both a stable query distribution and a distribution shift. The first tests whether locality helps when the workload is predictable. The second tests whether the placement and personalized gates remain useful when the assumptions that produced them no longer hold.

The central conceptual boundary is simple: **placing the selected computation nearer to the request can reduce movement, but changing the router can also change which computation is selected**. Those effects must be measured separately. Otherwise a latency reduction could come from doing less work, sending less data, waiting differently, or changing the answer-quality tradeoff, and the result would not identify which mechanism produced it.

## Distributed inference: the work selected can change the answer

A mixture-of-experts model contains alternative computational components called experts. A routing function chooses which components process each input. Activating only some experts reduces the arithmetic used for that input, but the complete collection can still exceed one device's memory. Distributing the experts therefore creates a second decision: where the chosen computation happens and how its inputs and outputs get there.

[Pegasus](../observed-subthemes/edge-embedded-and-mobile-systems.md#paper-dac-2026-research1922) combines similarity-based expert placement, partial fine-tuning of each node's routing function, and adaptive local batching. The detailed explanation above separates placement, routing, movement, and queueing; this card is the compact evidence record. [Source: official Description, mechanisms and final result](https://63dac.conference-program.com/presentation/?id=RESEARCH1922&sess=sess176).

The general evaluation problem is to distinguish avoiding communication from avoiding computation that was necessary for the original answer. Hold a quality criterion fixed, then count expert placement, routing training, request transfers, and ongoing updates. Test what happens when a node's input distribution changes after placement. Keeping frequently useful experts nearby can help a stable workload while performing poorly when requests become unfamiliar. Batching also has two effects: it can make processing more efficient, but waiting to collect a batch increases latency for its earliest request. Report both individual-request delay and completed requests per second.

<span id="explanation-dac-2026-research1936"></span>

## RTFL: what energy-aware federated scheduling must optimize

### Start with one federated-learning round

Federated learning keeps training examples on separate devices. In one round, a coordinator selects devices, each selected device computes local model updates, the updates travel to an aggregation point, and the resulting global model is sent back for the next round. A device can be slow because of its processor, its radio, its available bandwidth, or its remaining battery. The round is therefore limited by both computation and communication, and the next round cannot use an update that has not arrived.

The objective is not simply to select more devices or complete more rounds. A useful comparison fixes a model-quality measure and asks how much quality is reached within the same elapsed-time and energy budgets. A scheduler can increase the number of aggregation rounds while using lower-precision updates, selecting less representative data, or spending more energy. Those outcomes can move in opposite directions.

### What RTFL changes

RTFL describes an energy-aware real-time federated-learning framework using multi-agent reinforcement learning. Its adaptive-quantization multi-agent scheduling strategy chooses both **which devices participate** and **which model quantization level each selected device uses** for a local-training round.

Device selection changes the population that contributes data and updates. Quantization changes the numerical representation used during local computation or communication. Fewer bits can reduce storage, arithmetic, or transmitted data, but it also changes the update before aggregation. The useful question is not whether a quantized update is cheaper in isolation; it is whether its lower cost produces enough learning progress to justify the numerical error and any change in data participation.

The multiple agents are a control mechanism for making these choices under state constraints such as remaining battery, compute capability, and communication bandwidth. The source does not establish that the agents solve a globally optimal scheduling problem. It establishes the intended decision variables and reports qualitative claims of faster convergence, more participation in aggregation, and better training performance. No numeric convergence curve, accuracy value, energy budget, communication volume, agent count, device population, or baseline configuration is supplied. [Source: official DAC description and captured record](https://63dac.conference-program.com/presentation/?id=RESEARCH1936&sess=sess158).

### The tradeoffs that must be measured separately

There are at least five separate quantities. **Round time** includes local computation, upload, aggregation, and model download. **Energy per round** includes processor and radio activity, not only arithmetic. **Learning progress** requires a defined validation or test measure at a fixed data and model condition. **Participation** must identify which devices and data groups contributed, because a high total count can still exclude slow or rare-data devices. **Scheduler overhead** includes training and running the agents; it cannot be silently assigned to zero cost.

Compare RTFL with conventional scheduling and fixed-quantization selection at equal model, device population, data partition, network trace, deadline, and energy budget. Report quality versus wall-clock time, quality versus consumed energy, time to a fixed quality, and per-device participation. Test battery depletion, intermittent connectivity, non-identically distributed data, and a change in device or traffic conditions. “Real-time” is a training-time constraint in this description; it is not evidence of a hard deadline guarantee for each inference request or each federated round.

The central boundary is: **more frequent aggregation is a scheduling outcome, not a learning-quality outcome**. The claim becomes meaningful only when the extra rounds, precision choices, device coverage, scheduler cost, and final quality are reported together.

## Distributed training: participation is not a quality measure

Federated learning trains across devices while keeping their original examples local. Devices perform local updates, and an aggregation step combines their contributions. Devices may differ in compute speed, stored data, radio cost, or remaining battery. A policy that always selects the fastest devices can produce updates quickly while systematically excluding other data.

[RTFL](../observed-subthemes/edge-embedded-and-mobile-systems.md#paper-dac-2026-research1936) uses multiple learned scheduling agents to select devices and quantization levels under a training-time constraint. The detailed explanation above separates round time, energy, data participation, numerical precision, learning progress, and scheduler cost; this card is the compact evidence record. [Source: official Description, framework, scheduling, and experimental-summary sentences](https://63dac.conference-program.com/presentation/?id=RESEARCH1936&sess=sess158).

To evaluate this kind of policy, ask how much useful learning happens before the time or energy budget is exhausted. Compare final quality at the same elapsed time, and time to reach the same quality. Count scheduler training and inference costs separately from device training. Report participation by device or data group rather than only the total number of rounds. More rounds with heavily reduced precision can be less useful than fewer accurate updates; more selected devices can also spend more energy without improving the final model.

<span id="explanation-dac-2026-research1011"></span>

### SatSFL: split learning must continue when the satellite link disappears

### Start with the split-federated path

In split federated learning, a satellite-side device keeps its training examples locally and computes the first part of a model. It sends an intermediate activation to a ground-side service, which computes the remaining part and returns gradient information. The satellite uses that gradient to update its local part. A training step therefore depends on a sequence of forward values and backward feedback; keeping raw examples onboard does not remove the dependency on the link.

Satellite links add two constraints. Contact is intermittent, so a satellite may complete local work while the ground-side feedback is unavailable. The link can also be asymmetric, so the amount of data that can travel toward the satellite may differ from the amount that can travel in the opposite direction. A method must therefore specify what happens during the outage, what state is retained, and how the system reconciles provisional updates with real feedback later.

### What SatSFL changes

SatSFL describes two mechanisms. **Interpolated gradient approximation** produces an estimated gradient during a disconnection so local training can continue without waiting for the ground service. This is a numerical substitution: the update being applied is not the gradient computed from the current remote forward/backward path. The approximation can reduce idle time, but its error can accumulate across multiple local steps or become biased when the data distribution changes.

**Adaptive uplink compression** reduces the bytes sent over the constrained direction of the link while attempting to preserve gradients judged important. Compression introduces a representation error and a selection rule. “Critical” must be defined by a measurable criterion, and the result must report the error after decompression, not only the number of bytes removed. The system also needs a recovery rule for gradients delayed, dropped, or made stale by the contact schedule.

The official description claims evaluation on real-world low-Earth-orbit satellite systems and datasets and reports superior accuracy and convergence speed against unnamed state-of-the-art methods. It does not identify the satellites, processors, contact traces, model partition, dataset, compression ratio, approximation error, numerical accuracy, or boundary between flight operation, ground execution, replay and simulation. The description therefore establishes a constrained-system problem and a proposed pair of mechanisms, not a verified deployment or quantified robustness result. [Source: official DAC description and captured record](https://63dac.conference-program.com/presentation/?id=RESEARCH1011&sess=sess110).

### The evaluation that would establish disconnection tolerance

Replay complete orbit-scale contact traces, including outage duration, direction-specific bandwidth, delay, packet loss, and stale-feedback intervals. Compare waiting, local-only updates, exact delayed feedback, gradient approximation, and compression as separate ablations. Hold the model partition, data distribution, optimizer, local-step count, and total training wall-clock budget fixed. Report final quality, quality over wall-clock time, convergence to a fixed quality, bytes in each direction, approximation and compression error, energy, and the number of updates later corrected or discarded.

The central boundary is: **continuing to compute during a disconnection is not the same as continuing with the correct gradient**. A strong result must show both progress during the outage and controlled error after genuine ground feedback returns.

### SatSFL: local data does not remove the need for intermediate feedback

Split learning divides a model between machines. The first machine computes intermediate activations; another processes them and returns gradients, numerical feedback used to update the earlier computation. Keeping the original examples on the first machine does not eliminate these transfers. Nor does it, by itself, prove that intermediate activations or gradients reveal no private information.

[SatSFL](../observed-subthemes/edge-embedded-and-mobile-systems.md#paper-dac-2026-research1011) proposes interpolated gradient approximation during satellite–ground disconnections and adaptive compression for asymmetric links. The detailed explanation above separates dependency, approximation error, compression error, link asymmetry, and deployment evidence; this card is the compact evidence record. [Source: official Description, system mechanisms and evaluation sentence](https://63dac.conference-program.com/presentation/?id=RESEARCH1011&sess=sess110).

The technical tradeoff is between waiting for correct feedback and continuing with an approximation. A link can carry data quickly while available and still deliver little over an entire orbit because contact is brief. Measure service over that full interval, not only the connected interval. Approximation must be tested under changing data and long outages, including how the method corrects accumulated error when real feedback returns. Separate progress measured in update count from progress measured in wall-clock time and final task quality.

## Concurrency: more simultaneous work can increase contention

A computation graph records operations and their dependencies. A directed acyclic graph, or DAG, has no dependency cycle: a later operation cannot be required to produce its own earlier input. Independent operations can run together, but independence of their data does not imply independence of their resources. Two operations can compete for the same arithmetic units, registers, or memory path.

[The GPU scheduling paper](../observed-subthemes/edge-embedded-and-mobile-systems.md#paper-dac-2026-research1524) scales kernel parallelism and adds ordering between balanced groups. Its model covers one periodic DAG and assumes a particular execution-time scaling relation. Tests use RTX 3060 and Jetson Orin Nano GPUs, with a repeated kernel emulating different node workloads. Table 1 includes a counterexample: Stencil on 30 multiprocessors averages 11.37 ms versus Greedy's 11.09 ms. A sampled maximum is not a proven worst case. [Source: Sections 2 and 5, PDF pages 2 and 5–6; Tables 1–2, page 7](https://arxiv.org/pdf/2602.20826v1).

A kernel is a function executed across many GPU threads. Changing how many execution resources it requests can allow another kernel to make progress at the same time. Adding an ordering constraint can also prevent an unfavorable competition. The cost is that some work deliberately waits. Thus a tighter upper bound and a lower observed mean are different outcomes: the former can improve predictability even when some runs become slower.

To apply a scheduling proof, verify its assumptions rather than treating the use of a standard programming interface as sufficient. Are execution costs valid across input values and memory behavior? Does the graph include transfers and host work? Can unrelated processes interfere? Does numerical computation remain correct after a kernel is split or resized? Those are requirements for extending a model-based result to a deployment, not failures established by this paper.

### MATCHA: keeping two accelerators busy requires a complete memory schedule

A heterogeneous chip contains execution units suited to different work. Assigning every operation to its individually fastest unit can leave other units idle. Splitting an operation may expose more parallel work, but it also needs input partitioning, output assembly, memory space, and synchronization. Intermediate buffers cannot be reused until all consumers of their previous contents have finished.

[MATCHA](../observed-subthemes/edge-embedded-and-mobile-systems.md#paper-dac-2026-research1267) jointly plans concurrent work and memory. Evaluation uses Carfield on a VCU118 FPGA at 50 MHz, with PULP and Spatz clusters and FP16 data. Against MATCH, Table 2 reduces AutoEncoder latency from 20.1 to 13.4 ms but leaves DS-CNN and MobileNet unchanged. The 35.02% reduction concerns a ResNet-50 block, not every complete model. [Source: Section 4, PDF page 5; Table 2 and overhead discussion, page 6](https://arxiv.org/pdf/2604.09124v1).

The important comparison is complete execution with the same supported operations and numerical format. Faster arithmetic does not help if splitting and joining the data costs more than the saved time. A compiler's optimized schedule must also be feasible with actual storage capacities and communication paths. Report compile-time search cost separately from runtime dispatch. An FPGA implementation provides hardware execution evidence, but its timing is not automatically the timing of a fabricated chip at another frequency.

## Timing guarantees: finite delay is different from meeting every deadline

A task describes repeated work; a job is one released instance. A period describes how often jobs arrive. A response time runs from release to completion, including waiting. A hard deadline requires every covered job to finish by its specified deadline. A bound that allows completion after that deadline can be useful, but it proves a different property. An average latency or a high percentile proves neither property for all jobs.

For a simple hypothetical resource, jobs requiring 2 ms of service every 10 ms consume 20% of its time. Another stream needing 3 ms every 10 ms consumes 30%. Their combined 50% utilization leaves nominal capacity, but does not alone settle deadline correctness: release alignment, blocking, dependencies, and interruption costs still matter. A utilization test becomes sufficient only under the conditions of its associated scheduling theory.

[PHAROS](../observed-subthemes/edge-embedded-and-mobile-systems.md#paper-dac-2026-research1074) explicitly allows deadline misses in its soft-real-time model while requiring bounded response times. Its accelerator mapping cannot return to an earlier pipeline stage. The VCK5000 prototype and CHARM-based modeling use PointNet and truncated workloads. Crucially, Section 5.2 does not give EDF the same schedulability guarantee as FIFO once preemption overhead is included. This qualifies the earlier zero-overhead formulation. [Source: Sections 3.3–3.4, PDF page 3; Sections 5.1–5.3 and 5.5, pages 5–6](https://arxiv.org/pdf/2604.05308v1).

FIFO serves work in arrival order. EDF prioritizes the earliest deadline. Preemption interrupts current work to serve another job, but interruption requires a safe stopping point and preservation of unfinished state. Resuming may require additional transfers. A priority policy that is attractive when switching costs nothing may lose that advantage on hardware. A design-space search must therefore select hardware and schedules using costs that agree with the proof, rather than optimize throughput first and assume the result is timely.

## Combined interpretation and the next evidence

These papers support a useful organizing distinction: some systems change **which work is performed**, while others change **when and where the same work executes**. Routing personalization, quantization, and gradient approximation can affect numerical or learned behavior. Scheduling and placement primarily target execution, but still require correctness checks for transformations. Mixing the two categories under a single speedup hides the condition that makes the result meaningful.

A testable long-term hypothesis is that joint decisions about computation, storage, communication, and timing will help when workloads and resource availability change. It is not a temporal finding from this one-edition group. Test the hypothesis against stable workloads where fixed schedules avoid control overhead, weak links where communication dominates, and workloads too small to repay splitting costs. MATCHA's unchanged cases and the GPU scheduling counterexample already show why universal improvement is the wrong criterion.

This review was performed on 2026-09-07. Pegasus's author publication list confirmed its identity but did not expose an active paper link; RTFL's title search yielded its official description without a recovered manuscript. A SatSFL preprint was discovered through TechRxiv metadata and an indexed PDF, but the PDF host failed DNS resolution, including a retry, and the DOI route did not produce readable full text. Its experimental pages were not inspected. The three recovered manuscripts still need final-version matching and independent challenge. No artifacts were executed, no safety certification was established, and no full-system deadline guarantee was reproduced.

## Compare the results carefully

First identify the inputs and required output quality. Then identify the limited resource: time, memory, communication, energy, circuit area, or correctness coverage. Ask which part of the method reduces that cost and which new cost it adds. Compare numbers only when the experiments hold these conditions sufficiently similar.

A conference description may explain the proposal while omitting the full experiment. An author preprint link may have been coded from its abstract. The source classification does not by itself establish that every table was read. Missing locations remain visible below.

## Complete captured evidence

These are evidence records, not substitutes for the explanations above. Each record preserves its problem, proposed method, measurements, comparison conditions, and source limits. A populated record does not establish that its mechanism has been fully explained or independently verified.

<span id="paper-dac-2026-research1922"></span>

### Pegasus: Personalized and Communication-Efficient Mixture-of-Experts System for Distributed Edge LLM Inference

DAC 2026 · Record: `dac-2026-research1922`

[Read the step-by-step explanation](#explanation-dac-2026-research1922)

**Updated source-backed reading card**

Reviewed 2026-09-08. Reconciles the Pegasus card with the captured official source; separates expert placement, personalized routing, communication movement and adaptive batching, and prevents the reported 11.8x latency claim from being read as a quality-preserving or universally reproducible result.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Edge nodes can host only a subset of MoE experts, so query-dependent routing may select experts that are remote while memory, compute and communication are constrained.

**Mechanism / artifact:**

Pegasus combines similarity-based expert deployment across edge nodes, selective local fine-tuning of gating parameters, and adaptive intra-node batching. Placement targets locality; gating changes the routing policy; batching changes queueing and resource use.

**Workload — the work tested:**

Distributed edge MoE LLM inference; model identities, expert count, node count, query distribution, batch policy, quality metric and arrival trace are unspecified.

**Hardware and manufacturing assumptions:**

Constrained multi-edge nodes with inter-node communication; hardware, memory budgets, link capacity, placement-update cost, implementation status and measurement modality are unspecified.

**Baseline — the comparison method:**

Unnamed state-of-the-art distributed MoE frameworks

Baseline model quality, node resources, network conditions and batching parity are unspecified

**Reported measurements:**

The official description reports 11.8x lower inference latency, but supplies no numeric throughput, communication volume, energy, tail latency or model-quality result.

**Limits on the conclusion:**

Expert placement can reduce movement only when the query distribution matches the placement history; distribution shift can make the selected expert remote or make placement stale.

Personalized gating can change which experts process a token and therefore may change model quality; latency alone does not establish equivalence to the unmodified router.

Adaptive batching can improve resource use while adding formation wait to early requests; throughput and individual/tail latency must be reported separately.

The official description supplies no model identities, expert/node counts, link conditions, quality metric, baseline details or independent execution; the 11.8x claim is not a universal or quality-preserving result.

**Source and location**

Evidence tier: Primary captured official DAC description only; no full paper extraction, edge execution or independent latency/quality validation. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH1922&sess=sess176)

DAC 2026 official description and data/review-packets/dac-2026-research1922.json: edge MoE capacity mismatch; similarity-based expert deployment; selective local gate fine-tuning; adaptive local batching; reported 11.8x latency claim.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** state-of-the-art distributed MoE frameworks

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH1922&sess=sess176

**Hardware or process assumptions:** Multiple resource-constrained edge nodes communicating for MoE inference; network, memory, accelerator, and fine-tuning costs are unspecified.

**Limits:** The description omits model quality, communication volume, node heterogeneity, trace characteristics, and baseline configurations.

Latency claim may depend on expert-cache capacity and query correlation assumptions.

Official description only; system-level claim requires paper-level verification.

**Method or artifact:** Similarity-based expert placement, personalized local gating, and adaptive-batching online scheduling across multi-edge nodes.

**Metrics:** 11.8x lower inference latency

**Problem:** Edge nodes cannot host all MoE experts, causing query-dependent expert mismatches under memory, compute, and communication constraints.

**Workload or benchmark:** Distributed edge LLM inference with spatiotemporal query correlations; models, node count, expert capacity, traces, and quality metrics are unspecified.

</details>

<span id="paper-dac-2026-research1936"></span>

### RTFL: Energy-Aware Federated Learning for AIoT Design Via Adaptive Quantization-Based Multi-Agent Scheduling

DAC 2026 · Record: `dac-2026-research1936`

[Read the step-by-step explanation](#explanation-dac-2026-research1936)

**Updated source-backed reading card**

Reviewed 2026-09-08. Reconciles the RTFL card with the captured official source; separates device participation, quantization, round time, energy, learning progress and scheduler cost, and prevents qualitative convergence language from being read as a measured deadline or quality guarantee.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Battery-powered AIoT federated learning has heterogeneous compute, communication and residual-energy constraints that can slow useful global-model improvement.

**Mechanism / artifact:**

RTFL uses multi-agent reinforcement learning with adaptive quantization-based scheduling. The agents select participating devices and quantization levels for each local-training round using battery, compute and bandwidth state.

**Workload — the work tested:**

Federated learning across resource-constrained AIoT devices; model, dataset, device population, data partition, round count, deadline and convergence metric are unspecified.

**Hardware and manufacturing assumptions:**

Heterogeneous battery-powered devices with processors and radios; compute, communication, battery, network trace, aggregation service and scheduler execution cost are unspecified.

**Baseline — the comparison method:**

Conventional federated-learning scheduling

Fixed-quantization device selection

Baseline device population, data partition, network trace and energy parity are unspecified

**Reported measurements:**

The official description qualitatively claims faster convergence, more rounds of knowledge aggregation and improved training performance; it supplies no numeric accuracy, time, energy, communication-volume or participation value.

**Limits on the conclusion:**

More aggregation rounds do not by themselves establish more useful learning; quantization can reduce cost while changing update error, and device selection can change which data contributes.

Participation must be reported by device and data group, not only as a total count; selecting fast devices can exclude slow devices or rare data.

Energy must include local computation, communication, waiting and the multi-agent scheduler. A training-time constraint is not a hard per-round or per-inference deadline proof.

The official description supplies no convergence curves, quality criterion, device configuration, agent cost, numerical precision settings or independent execution; no universal energy, accuracy or real-time claim follows.

**Source and location**

Evidence tier: Primary captured official DAC description only; no full paper extraction, federated training execution or independent energy/quality validation. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH1936&sess=sess158)

DAC 2026 official description and data/review-packets/dac-2026-research1936.json: heterogeneous battery-powered AIoT devices; real-time training-time constraint; AQMAS device and quantization selection; battery, compute and bandwidth state; qualitative convergence and participation claims.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** conventional federated-learning scheduling

fixed-quantization device selection

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH1936&sess=sess158

**Hardware or process assumptions:** Heterogeneous battery-powered devices with varying compute, residual energy, and communication bandwidth; radio and processor details are unspecified.

**Limits:** No convergence curves, accuracy, energy budget, communication volume, agent count, or baseline configuration are supplied.

More participation may trade off energy, fairness, and model quality across devices.

Official description only; training and scheduling claims require paper-level verification.

**Method or artifact:** Multi-agent reinforcement-learning scheduler with adaptive quantization and device selection under a training-time constraint.

**Metrics:** Faster convergence claimed qualitatively

More knowledge-aggregation participation claimed qualitatively

**Problem:** Battery-powered AIoT federated learning suffers from slow convergence and poor training performance under heterogeneous compute and communication resources.

**Workload or benchmark:** Federated learning across resource-constrained AIoT devices; dataset, model, device population, rounds, and convergence metric are unspecified.

</details>

<span id="paper-dac-2026-research1524"></span>

### Exploiting Dependency and Parallelism: Real-Time Scheduling and Analysis for GPU Tasks

DAC 2026 · Record: `dac-2026-research1524`

**Updated source-backed reading card**

Reviewed 2026-09-07. Recovered manuscript distinguishes single-DAG timing analysis from measured, emulated workload behavior.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Concurrent GPU kernels can compete for execution capacity.

**Mechanism / artifact:**

Parallelism scaling, kernel segmentation, and added group dependencies through CUDA Graphs.

**Workload — the work tested:**

Synthetic DAGs; Laplace, Gaussian, Stencil structures with emulated node loads; 100 executions per case.

**Hardware and manufacturing assumptions:**

RTX 3060 and Jetson Orin Nano; single periodic DAG and modeled kernel scaling.

**Baseline — the comparison method:**

Greedy; Graham_para for analytical comparisons.

**Reported measurements:**

Synthetic analytical bound: up to 32.8% reduction versus Greedy. Table 1, 8-SM Gaussian mean: 65.07 to 51.23 ms, about 21.3% lower.

Table 1, 30-SM Stencil: proposed 11.37 ms average versus Greedy 11.09 ms.

**Limits on the conclusion:**

Some cases are slower. Sample maxima do not prove worst-case bounds or multi-task deployment guarantees.

**Source and location**

Evidence tier: Recovered manuscript; cited sections inspected. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://arxiv.org/pdf/2602.20826v1)

Section 2, PDF page 2; Section 5, pages 5–6; Tables 1–2, page 7.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** existing GPU real-time scheduling and analysis methods

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH1524&sess=sess146

**Hardware or process assumptions:** CUDA-capable GPU with no additional hardware/software support; kernel preemption, streams, memory transfers, and driver version are unspecified.

**Limits:** The description omits graph sizes, utilization, timing deadlines, GPU/driver settings, and baseline tuning.

Measured execution time and safe makespan bounds are distinct metrics with different assumptions.

Official description only; schedulability and safety claims require paper-level verification.

**Method or artifact:** DAG-based GPU scheduler and safe, non-pessimistic makespan analysis implemented through standard CUDA APIs.

**Metrics:** Up to 32.8% lower worst-case makespan

Up to 21.3% lower measured execution time

**Problem:** GPU kernel dependencies and resource contention create unpredictable delays for safety-critical real-time applications.

**Workload or benchmark:** Synthetic and real-world DAG-structured GPU tasks; GPU model, task graphs, utilization, timing constraints, and baseline methods are unspecified.

</details>

<span id="paper-dac-2026-research1011"></span>

### Towards Fast and Robust Split Federated Learning over Satellite-Based Computing Networks

DAC 2026 · Record: `dac-2026-research1011`

[Read the step-by-step explanation](#explanation-dac-2026-research1011)

**Updated source-backed reading card**

Reviewed 2026-09-08. Reconciles the SatSFL card with the captured official source; separates split-learning dependencies, disconnection-time gradient approximation, asymmetric-link compression and deployment evidence, and prevents qualitative accuracy/convergence language from being read as a quantified satellite deployment result.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Intermittent and asymmetric satellite-ground links interrupt the feedback path required by split federated learning while onboard resources and data-download latency constrain training.

**Mechanism / artifact:**

SatSFL combines interpolated gradient approximation during link outages with adaptive uplink compression intended to retain important gradient information under asymmetric bandwidth.

**Workload — the work tested:**

Split federated learning over satellite-based computing networks; the source claims real-world LEO systems and datasets but does not identify models, tasks, data partitions, contact traces or training configuration.

**Hardware and manufacturing assumptions:**

Satellite-ground split-learning deployment with constrained onboard compute and asymmetric intermittent links; satellite, ground processor, radio, bandwidth, contact schedule and flight-versus-simulation boundary are unspecified.

**Baseline — the comparison method:**

Unnamed state-of-the-art split/federated-learning methods

Baseline link traces, model partition, optimizer and resource parity are unspecified

**Reported measurements:**

The official description qualitatively claims superior accuracy and convergence speed; it supplies no numeric accuracy, convergence time, bytes, compression ratio, approximation error, energy or deployment result.

**Limits on the conclusion:**

An interpolated gradient is not the feedback that would have been computed by the remote model path; its error can accumulate or become biased under heterogeneous or changing data.

Compression can reduce link bytes while changing the gradient; critical-gradient selection needs a defined criterion and error measurement after decompression.

A real-world LEO-system claim does not identify whether computation, links and results were flight, ground, replay or simulation; deployment status cannot be inferred from the description.

The official description supplies no link trace, outage distribution, model partition, numerical result or independent execution; no convergence, robustness, privacy or satellite-deployment guarantee follows.

**Source and location**

Evidence tier: Primary captured official DAC description only; no full paper extraction, orbit scale trace replay or independent accuracy/convergence validation. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH1011&sess=sess110)

DAC 2026 official description and data/review-packets/dac-2026-research1011.json: intermittent/asymmetric satellite-ground link problem; interpolated gradient approximation during disconnection; adaptive uplink compression; qualitative real-world LEO evaluation, accuracy and convergence claims.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** state-of-the-art split federated learning methods; names and configurations unspecified

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH1011&sess=sess110

**Hardware or process assumptions:** Satellite-edge and ground split-learning deployment with intermittent asymmetric links; onboard/ground processors, link rates, outage model, and compression costs are unspecified.

**Limits:** The official description supplies no numeric accuracy, convergence, link-trace, heterogeneity, or compression-overhead results.

Real-world LEO wording does not establish flight deployment, trace provenance, or simulation boundaries.

Official description only; no full-text extraction or independent reproduction.

**Method or artifact:** SatSFL combines interpolated gradient approximation to emulate ground feedback during disconnections with adaptive uplink compression that preserves critical gradients under asymmetric bandwidth.

**Metrics:** Not established in the captured evidence.

**Problem:** Intermittent and asymmetric satellite–ground links compromise convergence and robustness in split federated learning under constrained onboard resources and high data-download latency.

**Workload or benchmark:** Split federated learning over real-world low-Earth-orbit satellite systems and datasets; task names, traces, data partitions, and evaluation protocol are unspecified.

</details>

<span id="paper-dac-2026-research1267"></span>

### MATCHA: Efficient Deployment of Deep Neural Networks on Multi-Accelerator Heterogeneous Edge SoCs

DAC 2026 · Record: `dac-2026-research1267`

**Updated source-backed reading card**

Reviewed 2026-09-07. Recovered experimental pages identify the FPGA configuration and workloads without improvement.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Sequential layer placement leaves heterogeneous compute capacity idle.

**Mechanism / artifact:**

Concurrent scheduling, tiling, and constraint-based memory planning.

**Workload — the work tested:**

MLPerf Tiny models and separate network-block microbenchmarks.

**Hardware and manufacturing assumptions:**

Carfield on VCU118 FPGA, 50 MHz, FP16; PULP and Spatz clusters; 1 MiB shared L2.

**Baseline — the comparison method:**

MATCH; TVM host-only comparison is separate.

**Reported measurements:**

AutoEncoder: 20.1 to 13.4 ms. DS-CNN and MobileNet: no improvement over MATCH.

**Limits on the conclusion:**

35.02% reduction is a ResNet-50 block result. Slicing/concatenation can offset computation savings; no general deadline guarantee.

**Source and location**

Evidence tier: Recovered manuscript; cited sections inspected. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://arxiv.org/pdf/2604.09124v1)

Section 4, PDF page 5; Table 2 and discussion, page 6.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** MATCH compiler

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH1267&sess=sess146

**Hardware or process assumptions:** Multi-accelerator heterogeneous edge SoC with L3/L2 memory hierarchy; accelerator types, memory capacities, clocking, and compiler versions are unspecified.

**Limits:** The description does not give model-by-model latency, utilization, energy, memory traffic, or schedule overhead.

The exact MATCH configuration and hardware platform are not stated.

Official description only; comparative claim requires paper-level verification.

**Method or artifact:** Unified deployment framework combining constraint-programmed memory/schedule optimization with pattern matching, tiling, and per-unit mapping.

**Metrics:** Up to 35% inference-latency reduction relative to MATCH

Improved accelerator utilization (numeric value unspecified)

**Problem:** Existing DNN deployment frameworks do not exploit heterogeneous accelerator engines effectively on edge SoCs.

**Workload or benchmark:** MLPerf Tiny on an SoC containing two heterogeneous accelerators; model suite, SoC details, and latency measurement conditions are unspecified.

</details>

<span id="paper-dac-2026-research1074"></span>

### PHAROS: Pipelined Heterogeneous Accelerators for Real-Time Safety-Critical Systems With Deadline Compliance

DAC 2026 · Record: `dac-2026-research1074`

**Updated source-backed reading card**

Reviewed 2026-09-07. The manuscript's soft-real-time definition allows missed deadlines and its EDF evaluation qualifies the zero-overhead guarantee.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Throughput-oriented accelerator search need not ensure bounded response times.

**Mechanism / artifact:**

Pipeline-constrained search with FIFO/EDF scheduling and tile-boundary preemption.

**Workload — the work tested:**

PointNet and truncated Point Transformer, MLP-Mixer, Res-MLP, DeiT-T workloads.

**Hardware and manufacturing assumptions:**

VCK5000 prototype plus CHARM modeling; no return to an earlier pipeline stage.

**Baseline — the comparison method:**

Throughput-guided CHARM search.

**Reported measurements:**

Reported 1.44–2.28× feasible configurations across six workload combinations.

**Limits on the conclusion:**

Bounded response is not hard-deadline compliance. Section 5.2 excludes an equivalent EDF guarantee once preemption costs apply; finite simulations are not universal proofs.

**Source and location**

Evidence tier: Recovered manuscript; cited sections inspected. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://arxiv.org/pdf/2604.05308v1)

Sections 3.3–3.4, PDF page 3; Sections 5.1–5.3 and 5.5, pages 5–6.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** throughput-oriented design-space exploration

**Evidence locators:** Not established in the captured evidence.

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH1074

**Hardware or process assumptions:** Not established in the captured evidence.

**Limits:** The description does not provide numerical gains, application identities, timing models, or hardware overhead for preemption.

**Method or artifact:** Real-time-centric accelerator framework with preemption, FIFO/EDF scheduling, schedulability analysis, and deadline-constrained DSE.

**Metrics:** number of feasible configurations

real-time performance

deadline/schedulability correctness

**Problem:** Heterogeneous-accelerator design frameworks optimize throughput or QoS while neglecting predictable execution, schedulability, and deadline correctness in safety-critical systems.

**Workload or benchmark:** Diverse embedded and safety-critical applications such as smart transportation task sets.

</details>

## What remains to establish

Resolve unspecified workloads, comparison methods, resource budgets, and source locations before generalizing a reported gain. Multiple papers in this selected sample permit comparison of mechanisms, but do not by themselves establish recurrence across years or a long-term trend.

[All subthemes](../expanded-taxonomy-v1.md) · [Research directions](../directions/README.md)
