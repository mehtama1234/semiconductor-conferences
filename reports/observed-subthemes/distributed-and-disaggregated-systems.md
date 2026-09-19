# Distributed and disaggregated systems

This subject has 7 records in the selected sample. This page explains where it fits, then presents all captured paper evidence without shortening the measurements or limitations.

[Definitions used in the paper records](../reading-guide-v1.md)

## Understand the parent subject first

- [Systems applications and workloads](../themes/systems-applications-and-workloads.md)

## Distribution adds communication and coordination

A distributed system assigns work or state to several machines or components. Each part has resources it can use locally, while cooperation requires messages or shared access. Dividing work can increase total capacity and permit concurrent execution, but it also creates dependencies across communication paths.

Disaggregation separates responsibilities or resources that might otherwise reside together. The resulting organization can allocate resources more flexibly, but the system must pay for communication and coordination between the separated parts. More available hardware does not by itself establish faster completion of one job.

## A job finishes only after its required dependencies finish

Workers can progress at different rates because of input differences, hardware differences, or shared-resource interference. A step that requires contributions from every worker may wait for the slowest required contribution. Measuring only the average worker time can conceal that delay.

The program also needs consistent rules for combining contributions and updating shared state. A scheduling or compression method must preserve the intended computation while changing where and when information moves.

## Compression reduces bytes but adds work

Adahuff-GNN's captured record uses adaptive Huffman compression guided by convergence behavior in distributed graph-neural-network training. Huffman coding represents symbols with variable-length codes based on their frequencies. Encoding, decoding, and managing the code representation all cost work. [Recorded evidence](../observed-subthemes/distributed-and-disaggregated-systems.md#paper-dac-2026-research1468)

The useful comparison measures complete training progress with and without the method, including bytes transferred and compression overhead. It must also establish whether the overall procedure preserves the required learning outcome. The current description provides no convergence, accuracy, transfer-volume, or total-time results sufficient to establish that gain.

<span id="explanation-dac-2026-research1468"></span>

### Adahuff-GNN: adaptive compression reduces distributed bytes only when codebook and synchronization costs stay below the communication saved

#### What distributed GNN training communicates

A distributed graph-neural-network trainer divides a graph, its nodes, or its training examples across workers. Each worker computes local message passing and parameter updates, but graph edges or model dependencies can cross worker boundaries. Workers must exchange values such as remote node features, intermediate states, gradients or updated parameters. A training step is complete only when the required exchanges and synchronization have completed.

The communication cost is not just the number of bytes. A transfer has serialization, encoding, network transmission, decoding, memory-copy and synchronization costs. If workers wait for one another at a barrier, the slowest required communication path can determine the step time. Reducing bytes helps only when link transmission is a significant part of that path and the compression work does not create a new bottleneck.

#### What Huffman coding changes

Huffman coding assigns shorter bit strings to symbols that occur more frequently and longer strings to rarer symbols. The code is lossless for the represented symbols when the encoder and decoder share the same codebook. The compressed message is therefore variable-length: its size depends on the observed symbol frequencies rather than only on the number of values.

An adaptive version changes the code as the distribution changes. The system must maintain frequency information, update the codebook, communicate or coordinate the codebook state, and ensure that every decoder interprets the incoming bitstream with the same code. A codebook that is stale may compress poorly; a codebook that changes at different times on different workers can make the message undecodable or require explicit versioning and synchronization.

The captured record describes convergence behavior as the signal guiding adaptation. This suggests changing the compression policy as training progresses, but the official description does not specify whether it changes the symbol alphabet, update interval, codebook, precision, lossless guarantee or message selection rule. Those details determine both the achievable bit reduction and the correctness boundary.

#### Why convergence can be a useful but risky control signal

Training does not have one stationary communication distribution. Early updates can differ from later updates, and changes in gradients or node-state distributions may correlate with convergence. A policy that compresses aggressively when updates appear stable can save communication, but an apparent convergence phase can be temporary or worker-specific. A local convergence signal may also disagree across partitions.

The method must therefore define what is measured, over which workers and over what time window. It must state how a policy change is synchronized, whether the first message after a change pays a codebook cost, and how it behaves when the training loss changes, data distribution is skewed or a worker lags. Convergence-aware compression must preserve the training computation; a lower message size with altered values is not automatically the same learning algorithm.

#### The complete cost comparison

For a message of (B) uncompressed bytes, the useful time comparison includes encoding time, compressed transfer time, decoding time, codebook maintenance, buffer copies and any barrier delay. The compressed path wins only if the saved network time exceeds those added costs on the critical path. If encoding uses a CPU while the GNN uses an accelerator, CPU contention and host-device transfers also belong in the measurement.

The baseline must include both uncompressed communication and a fixed-compression policy under the same graph partition, workers, minibatches, network topology, precision and synchronization rule. Report uncompressed and compressed byte counts, compression ratio, encode/decode time, codebook traffic, link utilization, worker idle time, per-step time, total time to the same training target and the number of training steps.

#### What correctness and scaling require

If the representation is lossless, decoded communicated values should match the baseline values exactly under the declared format. If the method is near-lossless or uses quantization, it must report the error and show that the model reaches the same accuracy or an explicitly stated alternative target. Distributed training validation must include final accuracy, convergence curves, loss variance, reproducibility across seeds and behavior under worker or partition imbalance.

Scale tests should vary worker count, graph partition quality, network bandwidth, message size, contention and the point in training at which the policy changes. A reduction on one fast link may disappear on another link, and a policy that helps average traffic may worsen the slowest worker's step time. Rare communication patterns and distribution shifts should remain visible rather than being averaged away.

The captured official description supports adaptive Huffman compression guided by convergence behavior for distributed GNN communication. It reports no convergence, accuracy, byte-volume, total-training-time, encode/decode-overhead, network, scale or power result. The evidence therefore establishes a mechanism proposal and its evaluation requirements, not demonstrated communication reduction or faster distributed training.

[Observed paper card](../observed-subthemes/distributed-and-disaggregated-systems.md#paper-dac-2026-research1468)

## Scientific learning must preserve the physical question

The two-teacher scientific-learning record proposes guidance from both hardware considerations and physical information. A learning process can optimize execution efficiency while also trying to represent a physical relationship. Those objectives require separate validation. [Recorded evidence](../observed-subthemes/distributed-and-disaggregated-systems.md#paper-dac-2026-research1741)

A lower training cost is useful if the model still meets the relevant scientific accuracy requirement. Conversely, improved prediction quality does not establish that distributed execution became more efficient. The captured description leaves accuracy, convergence, communication, runtime, and energy unresolved, so the interaction of the two forms of guidance remains an open evaluation question.

<span id="explanation-dac-2026-research1741"></span>

### Two Teachers Better Than One: hardware guidance and physics guidance solve different constraints

#### What scientific machine learning is trying to satisfy

Scientific machine learning uses a learned model to approximate a physical quantity, field or evolution. The model is trained from data, but the physical problem also imposes structure such as a governing equation, boundary condition, conservation rule or relationship between inputs and outputs. A model can fit sampled data while violating that structure between samples, especially when the data are sparse or the deployment regime differs from training.

Distributed training adds another constraint. The model or data are split across workers, and the workers exchange parameters, gradients or intermediate states. Communication, synchronization, memory and accelerator utilization affect training time and energy. The physical objective and the systems objective are related through the training process, but they are not the same measurement.

#### What two teachers could mean

The captured method uses two forms of guidance: one from hardware considerations and one from physical information. A physics teacher can provide targets, residuals or constraints derived from the scientific problem. A hardware teacher can provide information about resource cost, execution suitability, communication or deployment constraints. The student model or distributed training policy must combine these signals into an optimization objective or update rule.

The exact interaction is not exposed. It is not known whether the teachers produce labels, losses, gradients, architecture choices, schedules, compression decisions or separate model outputs. That distinction matters because adding a term to a loss, selecting a smaller model and changing a distributed schedule have different costs and different correctness conditions.

#### Why the objectives can conflict

A physics constraint can require more model capacity, higher precision, more iterations or more communication. A hardware constraint can favor fewer parameters, lower precision, less synchronization or a partition that is efficient but poorly aligned with the physical dependencies. Optimizing a weighted sum can improve one objective while degrading the other, and the weight determines what tradeoff is accepted.

The system must therefore state the physical error measure, hardware cost measure, normalization, teacher update schedule and stopping rule. A teacher signal can guide optimization, but guidance is not a guarantee that the final model satisfies the equation or that the final distributed execution is efficient. The teachers may also be domain-specific: a signal useful for one PDE or hardware topology may not transfer to another.

#### What distributed validation must include

The comparison should hold the scientific task, data split, model capacity and quality target fixed while varying single-teacher, two-teacher and unguided training. It should report physical residuals, boundary-condition error, prediction error on held-out regimes, conservation or other domain constraints, convergence curves and sensitivity to teacher weights.

Systems measurements must separately report worker count, partitioning, communication volume, synchronization frequency, accelerator utilization, memory, per-step time, total time to the same physical accuracy and energy. A lower loss after more training is not a lower training cost. A smaller communication volume is not a physical-accuracy result.

Tests should include data scarcity, distribution shift, different worker counts, network bandwidth, load imbalance and cases where physical and hardware guidance disagree. Ablations should show whether the hardware teacher improves the model, the schedule, the architecture, or only the measured proxy used during optimization.

The captured official description supports a two-teacher hardware/physics-guided distributed scientific-learning proposal and the named single-teacher and unguided comparison ideas. It reports no accuracy, convergence, communication, runtime or energy result, and does not define the teacher outputs or combination rule. The evidence therefore establishes a research direction, not demonstrated scientific validity, hardware efficiency or superiority to one-teacher learning.

[Observed paper card](../observed-subthemes/distributed-and-disaggregated-systems.md#paper-dac-2026-research1741)

## Shared execution resources can create interference

Hestia's captured description schedules cloud microservices at the hardware-thread level using an attention-based policy. Hardware threads can share execution resources within a processor core. Scheduling two activities together can increase utilization or make them compete for the same limited resource. [Recorded evidence](../observed-subthemes/distributed-and-disaggregated-systems.md#paper-dac-2026-research2395)

The policy must identify which combinations interfere and whether moving work costs less than the delay avoided. Microservice requests can depend on several other requests, so a small local slowdown can affect complete service response time. The record does not establish slow-request latency, throughput, fairness, policy overhead, or transfer to different workload mixes.

<span id="explanation-dac-2026-research2395"></span>

### Hestia: hyperthread-level placement must trade shared-resource interference against migration and fairness costs

#### What hyperthread-level scheduling controls

A hardware thread is a logical execution context exposed by a processor. Two hardware threads can share parts of one physical core, including execution ports, pipeline capacity, private caches, branch-prediction structures, load/store resources or memory-system bandwidth. The exact shared resources depend on the processor. A thread that is fast when running alone can slow another thread when both demand the same resource.

Core-level scheduling treats the core as the placement unit. Hyperthread-level scheduling makes a finer decision: which workloads should occupy sibling hardware threads at the same time, and when should one be moved or left idle. Finer control can expose useful pairings, but it also requires more observations, more decisions and more opportunities for scheduling overhead.

#### What interference means for a microservice

Interference is a change in one workload's performance caused by another workload sharing a resource. A CPU-bound service may compete for execution capacity. A memory-intensive service may evict cache lines or consume memory bandwidth. A branch-heavy service may affect prediction resources. The result can be a change in service time, not only in average core utilization.

Microservice performance is usually judged at request level. A request can call several services, wait in queues and depend on downstream responses. A placement that improves average throughput can still worsen the slowest requests if it creates contention on a critical service or produces occasional long stalls. Tail latency, such as p95 or p99, must therefore be measured with the service-level objective and the complete request path stated.

#### What an attention-based policy would need to learn

The captured Hestia description identifies an attention-based policy for hardware-thread scheduling, but it does not expose the input features, action space, training data or reward. A usable policy would need observations such as current utilization, cache or memory behavior, runnable work, service identity, request urgency and recent latency. It would choose a co-location, placement, migration, preemption or idling action under a defined objective.

The policy must distinguish correlation from causation. Two services may show high cache activity because they are both busy, not because they interfere strongly. A policy trained on one processor or workload mix can also fail when the shared-resource topology, request distribution or service versions change. The attention mechanism does not by itself establish that the learned policy identifies the physical bottleneck or generalizes to another CPU.

#### The cost of moving work

Changing placement can require descheduling, migration, cache warming, synchronization, queue movement or loss of locality. A policy decision also consumes CPU time and may require monitoring counters. Moving a service to avoid a predicted conflict is beneficial only when the avoided interference exceeds the decision and transition costs.

Frequent movement can create oscillation: the scheduler observes a conflict, moves a service, observes a new conflict, and moves it back. A stable policy needs a decision interval, hysteresis or another rule that prevents reaction to noise. Those controls can delay response to a real workload change. The evaluation should expose decision rate, migration count, monitoring overhead, cold-cache cost and the cases where the policy leaves a core underutilized to protect latency.

#### What a fair comparison requires

Compare Hestia with the operating-system scheduler and core-level placement under the same CPU, hardware-thread availability, service versions, arrival process, request mix, concurrency, quality target and load. Report throughput, mean and tail latency for each service and for end-to-end requests, utilization, migrations, scheduler CPU cost and fairness. A policy that protects one service by degrading another should make that tradeoff visible.

Stress tests should vary co-runner intensity, memory pressure, cache locality, burstiness, service dependency graphs, load imbalance and CPU generations. Include isolated execution, deliberate adversarial pairings, workload changes and overload. Training and evaluation traces must be separated so that the policy is not judged only on the interference patterns it saw during training.

The captured official description supports a hyperthread-level interference-aware attention scheduler for cloud microservices. It reports no tail latency, throughput, fairness, scheduler overhead, migration cost, processor configuration or workload-diverse result. The evidence therefore establishes a scheduling direction, not demonstrated QoS improvement, generalization or lower total service cost.

[Observed paper card](../observed-subthemes/distributed-and-disaggregated-systems.md#paper-dac-2026-research2395)

<span id="explanation-dac-2026-research2531"></span>

### PRISM: primitive-aware forecasts are useful only when forecast error improves a real scheduling decision

#### What a GPU-cluster forecast must predict

A GPU-cluster scheduler receives jobs that ask for resources over time. A job may need a number of GPUs, memory, accelerator type, duration, bandwidth or a sequence of changing demands. The scheduler uses predictions to decide where to place work, when to start it, whether to reserve capacity and whether to preempt or move another job.

“Workload” is therefore not one number. A useful forecast must state the quantity being predicted, the time horizon and the unit of prediction. It could predict arrivals, running-job demand, GPU utilization, job duration, resource demand by type or the probability of a future burst. A forecast that is accurate for average utilization may still miss the short burst that causes a deadline miss. A forecast for the next five minutes also answers a different operational question from one for the next day.

#### What a workload primitive means

A workload primitive is a recurring, measurable unit used to describe demand. It could be a job class, a model family, a computation phase, a kernel pattern or a resource-demand signature. The method must define how the primitive is detected, which telemetry identifies it, and how a primitive maps to future resource use. If the same primitive has different demand on different GPU types or during different phases, the representation must retain those conditions.

This definition matters because the forecast is only as reliable as the relationship between the primitive and the future demand. Primitive frequencies can change when users, models, data, software versions or scheduling policies change. That change is concept drift. A dynamic method may update its model as new traces arrive, but it must then handle a cold-start period, noisy telemetry and the cost of updating decisions while jobs are already running.

#### Forecast error is not the same as scheduling benefit

Forecast quality and scheduling quality are separate measurements. A model can reduce average error while still missing high-cost bursts. Conversely, a forecast with modest numerical error may be useful if it correctly identifies the events that affect placement or deadlines. Evaluation should therefore report horizon-specific error, rolling time splits, calibration or prediction intervals, rare-burst detection and error by job class or resource type.

The downstream scheduler must also be evaluated. The relevant outcomes include queue time, deadline or service-level attainment, GPU utilization, fragmentation, preemption count, migration or restart cost, fairness and scheduler decision overhead. The comparison must hold the cluster, trace order, admission policy, job priorities and resource constraints fixed while varying the forecast. Otherwise an apparent scheduling gain may come from a changed policy rather than from the forecast.

#### What dynamic adaptation costs

The dynamic path needs telemetry collection, feature extraction, model updates and a rule for deciding when a new forecast is trusted. Telemetry can consume CPU, memory, network and storage capacity. Frequent updates may increase decision churn; infrequent updates may miss concept drift. If the scheduler acts on a wrong prediction, it can reserve idle GPUs, place incompatible jobs together, preempt useful work or create unfair access for long-running jobs.

The complete claim must therefore compare the cost of forecasting with the cost avoided by better decisions. It should include inference time, update time, telemetry volume, scheduler overhead and the effect of preemption or migration. It should also test changes in GPU types, cluster topology, job mix, workload phase and arrival rate. Results from one trace do not establish that the primitive remains predictive in another cluster.

The captured DAC description supports dynamic primitive-based forecasting for large-scale GPU workloads. It reports no forecast error, forecast horizon, rolling trace split, scheduling experiment, queue-time change, preemption cost, overhead or deployment result. The evidence supports a mechanism and an evaluation plan, not demonstrated end-to-end cluster improvement.

[Observed paper card](../observed-subthemes/distributed-and-disaggregated-systems.md#paper-dac-2026-research2531)

<span id="explanation-dac-2026-research3208"></span>

### Making Sense of Job Preemption: distributed training must preserve useful progress, not only fill idle accelerators

#### What preemption changes in distributed training

A distributed training job usually has several workers processing different data or model partitions. Workers exchange gradients, activations, parameters or control messages. Some steps can proceed independently, but a synchronization point may require a set of workers to reach the same logical point before the next step is valid.

Preempting one job removes some or all of its workers from the accelerators. The scheduler may use those devices for another job, which can reduce idle capacity. The interrupted training job, however, may leave peer workers waiting, lose work that has not been saved, repeat computation after restart or need to rebuild communication state. The useful question is not whether an accelerator was occupied during the interval. It is whether the cluster reached more training quality per unit time after all interruption and recovery work was included.

#### What a consistent checkpoint must contain

A checkpoint is useful only if a restarted job can continue from a valid distributed state. Depending on the training system, that state can include model parameters, optimizer state, random-number state, data position, scheduler state and the relationship between workers. A checkpoint taken while workers disagree about the completed step can produce duplicate or missing data, inconsistent optimizer updates or a different training trajectory.

Checkpointing also has a cost. Workers may pause to create a consistent snapshot, copy state from accelerator memory, compress it, transfer it across the network and write it to shared storage. A short checkpoint interval limits recomputation after preemption but increases this overhead. A long interval reduces checkpoint traffic but increases lost work when a job is interrupted. The scheduling policy must compare these costs with the capacity made available to another job.

#### Why naive preemption can waste capacity

If the scheduler stops a worker without coordinating its peers, the remaining workers can wait at a collective operation or continue until they fail to receive the expected message. If it stops the whole job, all of its currently allocated devices become available, but the restart may require model loading, communication setup, data-loader warm-up and recomputation. If the scheduler preempts too often, the job can spend a large fraction of its time saving, restarting or waiting rather than improving the model.

Preemption can also alter fairness. A short job may repeatedly displace a long job, or a job with a large checkpoint may be avoided even when its deadline is important. The policy therefore needs an explicit objective and constraints: queue delay, time to a stated quality target, deadlines, priority, fairness, maximum interruption rate, checkpoint cost and the communication topology all matter.

#### Utilization is not time-to-quality

Raw accelerator utilization measures how often devices are busy, not whether the training job is making valid progress. A cluster can report higher utilization while spending more time on checkpoint writes, model reloads, communication recovery or recomputation. The primary comparison should hold the training task and quality target fixed and report time to that target, convergence progress, useful examples processed, lost or repeated work, queue time, checkpoint time, restart time and communication overhead.

Evaluation should compare non-preemptive scheduling, naive preemption and the proposed policy under the same job arrivals, model sizes, worker counts, network, storage path, checkpoint interval and cluster load. It should vary synchronization sensitivity, job duration, burstiness, failure or eviction frequency, network bandwidth, storage throughput and fairness constraints. Trace replay must preserve arrival order and should include workloads that make checkpoint cost and collective communication visible.

The captured DAC description supports analysis or scheduling for preempting distributed deep-learning jobs. It reports no time-to-quality, utilization, convergence, checkpoint or restart overhead, useful-work loss, communication result or cluster-trace experiment. The evidence supports a scheduling direction and its measurement requirements, not demonstrated faster distributed learning.

[Observed paper card](../observed-subthemes/distributed-and-disaggregated-systems.md#paper-dac-2026-research3208)

<span id="explanation-dac-2026-research513"></span>

### Asymcheck: asymmetric checkpointing reduces write pressure only when restart state remains consistent

#### What a distributed LLM checkpoint represents

Training state is more than the model parameters. A distributed LLM run may also need optimizer state, gradient or accumulation state, random-number state, data position, learning-rate state and scheduler metadata. The exact set depends on the training method, but the restart must restore enough state to continue the declared computation rather than start a different run by accident.

Workers hold different partitions of that state. They may write to local or shared storage while exchanging metadata over a network. A full synchronous checkpoint usually makes workers coordinate around a common training step and records a complete snapshot. That coordination can pause computation and create a large burst of storage and network traffic.

#### What asymmetric partitioning changes

An asymmetric strategy can give different partitions different sizes, write frequencies, destinations or completion rules. This can match the real state: one partition may be large but change often, another may be small but essential for correctness, and another may be cheap to reconstruct. The method must state how it classifies these differences and how the partition plan changes when the model, optimizer, worker count or storage system changes.

Reducing the largest write or spreading writes over time can lower peak bandwidth demand. It does not by itself prove that the training job spends less time checkpointing. The schedule may add metadata, coordination, buffering, replication or extra reads. A partition that is delayed too long can also increase the amount of work that must be recomputed after a failure.

#### Why restart semantics are the central correctness issue

The partitions in a checkpoint need a shared version or step identity. On restart, the system must distinguish a complete set from a mixture of old, new, missing or partially durable partitions. It needs a commit rule, durable completion metadata, failure detection and a policy for incomplete writes. If workers write independently, the method must explain how it prevents the model parameters from step (t) being combined with optimizer or data-position state from step (t-1).

This is not only a storage detail. A mixed checkpoint can produce a run that appears to resume but has changed the training computation. The evaluation must therefore test exact or declared recovery semantics, not only whether files were written. If some state is intentionally reconstructed, the amount of recomputation and its effect on time to the same quality target must be measured.

#### What an adequate comparison measures

Compare full synchronous checkpointing, uniform partitioning and the asymmetric method under the same model, worker count, training data, checkpoint interval, storage, network and failure schedule. Report bytes by state and worker, write time, synchronization time, training slowdown, peak storage and network load, recovery time to useful work, recomputed steps and the number of incomplete or rejected checkpoints.

Failure injection should include a worker loss, network interruption, storage delay, partial write and restart during each checkpoint phase. Vary model size, optimizer-state size, worker count, storage bandwidth, replication policy and checkpoint interval. A system that reduces average checkpoint traffic but fails slowly or inconsistently under a partial write has not established an end-to-end training benefit.

The captured DAC description supports asymmetric partitioned checkpointing for distributed LLM training. It reports no checkpoint volume, training overhead, recovery time, consistency result or failure-injection experiment. The evidence supports a checkpointing direction and its correctness requirements, not demonstrated efficient or reliable recovery.

[Observed paper card](../observed-subthemes/distributed-and-disaggregated-systems.md#paper-dac-2026-research513)

<span id="explanation-dac-2026-research986"></span>

### Procyon: fine-grained accelerator sharing is useful only when extra occupancy does not become tenant interference

#### What a sparse streaming accelerator is trying to keep busy

A streaming accelerator moves data through a sequence of buffers and compute stages. A sparse workload does not perform every possible operation: it skips elements known to be zero or otherwise inactive. The skipped work can reduce arithmetic, but it also makes the amount and timing of work irregular. One tenant may have an empty stage while another has a burst of active elements.

With one tenant, an empty stage or a temporary lack of ready work can leave compute units or buffers unused. Multi-tenancy tries to use that capacity for another tenant. The scheduler must decide which tenant's work enters each stage, how much state is retained for each tenant, and how shared buffers and memory traffic are controlled.

#### What fine-grained sharing changes

Fine-grained scheduling can interleave work at a smaller unit than a whole request, layer or batch. This may fill short gaps and reduce the time that a stage waits for one tenant's data. It also adds arbitration decisions, tenant state, queue management and possible context changes. If the hardware cannot retain enough state, switching tenants can cause buffer drains, refills or repeated memory accesses.

The benefit depends on the resource that was idle. If compute was idle because memory bandwidth was already saturated, adding another tenant may increase contention without increasing useful work. If the tenants need the same buffer bank or execution stage, interleaving can create a new queue. A valid comparison must measure the complete path, including scheduling and state-management overhead.

#### Efficiency and service guarantees are different claims

Aggregate throughput asks how much total work the accelerator completes. Tenant isolation asks whether one tenant can change another tenant's result or service time beyond a stated bound. Fairness asks how service is divided. Tail latency asks what happens to the slowest requests, not only the average request.

A policy can improve aggregate throughput by favoring a tenant whose work is easy to schedule while delaying a tenant with irregular memory demand. That result is not a general multi-tenant improvement unless the tradeoff is explicit. The system needs a resource-allocation rule, admission policy, priority or fairness definition, and a statement of whether isolation is performance isolation, functional isolation or both.

#### What the evaluation must expose

Compare single-tenant execution, coarse multi-tenancy and fine-grained scheduling under the same sparse formats, tenant arrivals, batch sizes, request mix, quality target and hardware configuration. Report per-tenant and aggregate throughput, mean and tail latency, queue delay, resource utilization, buffer occupancy, memory traffic, arbitration and context overhead, energy and fairness.

Stress tests should vary sparsity, burstiness, tenant count, conflicting buffer access, memory bandwidth, workload size, priority and overload. Include a tenant that produces the worst interference and test whether the policy preserves the declared isolation bound. A higher utilization number without these per-tenant measurements cannot establish that the accelerator serves several tenants efficiently.

The captured DAC description supports fine-grained multi-tenant scheduling for sparse streaming accelerators. It reports no throughput, fairness, tail-latency, isolation, energy, hardware or workload-diverse result. The evidence supports a sharing direction and its evaluation requirements, not demonstrated efficiency or QoS preservation.

[Observed paper card](../observed-subthemes/distributed-and-disaggregated-systems.md#paper-dac-2026-research986)

## Compare useful system outcomes at a stated scale

Specify machine count, resource configuration, network characteristics, input distribution, and concurrency. Hold the application result or quality target constant. Measure complete job time, slow requests, resource use, and communication, including preprocessing and policy overhead.

Vary scale and contention. More workers can change the limiting resource, so a gain on one cluster size cannot be assumed to grow proportionally. Distinguish measured cluster results from simulated larger systems and preserve the simulator's assumptions.

These papers address compression, learning guidance, and scheduling. Their shared concern is efficient cooperation under distributed resource limits. Their results become comparable only after the work performed, required output, resource budget, and measurement boundary are aligned.

## Compare the results carefully

First identify the inputs and required output quality. Then identify the limited resource: time, memory, communication, energy, circuit area, or correctness coverage. Ask which part of the method reduces that cost and which new cost it adds. Compare numbers only when the experiments hold these conditions sufficiently similar.

A conference description may explain the proposal while omitting the full experiment. An author preprint link may have been coded from its abstract. The source classification does not by itself establish that every table was read. Missing locations remain visible below.

## Complete captured evidence

These are evidence records, not substitutes for the explanations above. Each record preserves its problem, proposed method, measurements, comparison conditions, and source limits. A populated record does not establish that its mechanism has been fully explained or independently verified.

<span id="paper-dac-2026-research1468"></span>

### Adahuff-GNN: A Convergency-Aware Adaptive Huffman Compression for Communication Reduction in Distributed GNN Training

DAC 2026 · Record: `dac-2026-research1468`

[Read the step-by-step explanation](#explanation-dac-2026-research1468)

**Updated source-backed reading card**

Reviewed 2026-09-08. Deepens the official-description reading; explains distributed GNN communication, adaptive Huffman codebooks, convergence-aware policy changes and the missing end-to-end measurements.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Distributed GNN training exchanges gradients, graph states or intermediate features across workers, so communication and synchronization can limit training progress.

**Mechanism / artifact:**

Adaptive Huffman compression controlled by convergence behavior for distributed GNN communication; codebook update rule, message representation, synchronization procedure and lossless/near-lossless boundary are unspecified.

**Workload — the work tested:**

Distributed GNN training; graph datasets, partitioning, worker count, minibatches and network topology are unspecified.

**Hardware and manufacturing assumptions:**

Multi-node accelerator training with variable-length communication compression; link bandwidth, encoding/decoding processor, memory path and precision are unspecified.

**Baseline — the comparison method:**

Uncompressed communication

Fixed compression

Exact network, worker, partition, synchronization and training settings are unspecified

**Reported measurements:**

Communication reduction is claimed qualitatively; no convergence, accuracy, byte-volume, training-time or compression-overhead result is reported.

**Limits on the conclusion:**

Huffman encoding is lossless only when the symbol representation and shared codebook are defined consistently. Adaptive codebooks add frequency tracking, update, coordination and versioning work that belongs on the communication critical path.

A convergence signal can change the compression policy, but the official description does not establish the signal, update interval, worker agreement, message format, or whether values remain lossless. Lower bytes do not establish the same training outcome.

Compression may add latency and CPU, memory or accelerator contention. No graph-, network-, scale- or training-diverse measurements are reported, so the source supports a mechanism proposal rather than demonstrated faster distributed training.

**Source and location**

Evidence tier: Primary captured official DAC description only; no full paper extraction, distributed training reproduction or network/scale/accuracy validation. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH1468)

DAC 2026 official description; captured Problem, Mechanism / artifact, Workload, Hardware, Baseline, Measurements and Limits fields; record RESEARCH1468; no manuscript pages.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** uncompressed communication

fixed compression

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH1468

**Hardware or process assumptions:** Multi-node accelerator training with lossless or near-lossless compression; link bandwidth and CPU cost are unspecified.

**Limits:** No convergence, accuracy, bytes, training time, or compression-overhead results are reported.

Compression may add latency and CPU work.

Official description only; graph and network-diverse validation is required.

**Method or artifact:** Adaptive Huffman compression controlled by convergence behavior.

**Metrics:** Communication reduction is claimed qualitatively

**Problem:** Distributed GNN training incurs communication overhead from exchanging gradients or graph states.

**Workload or benchmark:** Distributed GNN training; graph datasets, workers, and network topology are unspecified.

</details>

<span id="paper-dac-2026-research1741"></span>

### Two Teachers Better Than One: Hardware-Physics Co-Guided Distributed Scientific Machine Learning

DAC 2026 · Record: `dac-2026-research1741`

[Read the step-by-step explanation](#explanation-dac-2026-research1741)

**Updated source-backed reading card**

Reviewed 2026-09-08. Deepens the official-description reading; separates hardware guidance from physics guidance and preserves the absence of scientific-accuracy and distributed-system measurements.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Distributed scientific machine learning must satisfy physical constraints while operating under hardware and communication limits.

**Mechanism / artifact:**

Two-teacher hardware- and physics-guided distributed learning method; teacher outputs, combination rule, training objective and system policy are unspecified.

**Workload — the work tested:**

Scientific ML workloads; physical equations, datasets, model classes, workers, partitions and network are unspecified.

**Hardware and manufacturing assumptions:**

Distributed accelerator training with physics-informed and hardware-aware guidance; communication, precision, memory, utilization and energy assumptions are unspecified.

**Baseline — the comparison method:**

Single-teacher learning

Unguided distributed training

Scientific task, model capacity, quality target, worker and system conditions are unspecified

**Reported measurements:**

Scientific-learning efficiency is claimed qualitatively; no accuracy, physical residual, convergence, communication, runtime or energy result is reported.

**Limits on the conclusion:**

Physics guidance can constrain a learned approximation, while hardware guidance can shape resource use, but the source does not define their outputs, combination rule, weights or update schedule.

A lower training or communication cost does not establish physical correctness, and a lower physical error does not establish distributed efficiency. Teacher interactions may be domain- and hardware-specific.

The official description supplies no equation, dataset, model, worker protocol, accuracy, convergence, communication, runtime or energy measurement; the record supports a research direction rather than demonstrated scientific or systems superiority.

**Source and location**

Evidence tier: Primary captured official DAC description only; no full paper extraction, scientific learning reproduction or distributed accuracy/runtime/energy validation. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH1741)

DAC 2026 official description; captured Problem, Mechanism / artifact, Workload, Hardware, Baseline, Measurements and Limits fields; record RESEARCH1741; no manuscript pages.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** single-teacher learning

unguided distributed training

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH1741

**Hardware or process assumptions:** Distributed accelerator training with physics-informed guidance; communication and precision assumptions are unspecified.

**Limits:** No accuracy, convergence, communication, runtime, or energy results are reported.

Teacher interactions may be domain-specific.

Official description only; physical and distributed validation is required.

**Method or artifact:** Two-teacher hardware- and physics-guided distributed learning method.

**Metrics:** Scientific-learning efficiency is claimed qualitatively

**Problem:** Distributed scientific ML must reconcile learned approximations with physical and hardware constraints.

**Workload or benchmark:** Scientific ML workloads; physical equations, datasets, workers, and network are unspecified.

</details>

<span id="paper-dac-2026-research2395"></span>

### Hestia: Hyperthread-Level Scheduling for Cloud Microservices with Interference-Aware Attention

DAC 2026 · Record: `dac-2026-research2395`

[Read the step-by-step explanation](#explanation-dac-2026-research2395)

**Updated source-backed reading card**

Reviewed 2026-09-08. Deepens the official-description reading; explains hyperthread-level shared-resource interference, attention-based scheduling, migration overhead, tail latency and fairness requirements.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Co-located cloud microservices can interfere through shared CPU resources, while core-level placement may not expose the finer-grained hardware-thread pairing decisions that affect latency.

**Mechanism / artifact:**

Hyperthread-level interference-aware scheduler using an attention-based policy; observed features, action space, training data, migration rule and optimization objective are unspecified.

**Workload — the work tested:**

Cloud microservice workloads; CPU generation, service graph, request arrivals, concurrency, interference traces and QoS targets are unspecified.

**Hardware and manufacturing assumptions:**

Multithreaded CPU with shared caches, execution and memory resources; OS scheduler, hardware counters, migration, placement and monitoring assumptions are unspecified.

**Baseline — the comparison method:**

Operating-system scheduler

Core-level placement

CPU, service, request, quality, load, hardware and timing conditions are unspecified

**Reported measurements:**

Microservice scheduling efficiency is claimed qualitatively; no tail latency, throughput, fairness, scheduler overhead, migration or workload-diverse result is reported.

**Limits on the conclusion:**

Hyperthread-level placement can reduce interference only when the policy identifies the shared bottleneck and the avoided stall exceeds monitoring, decision, migration and cache-warming cost.

Average utilization or throughput does not establish service quality: a co-runner can increase p95/p99 latency or slow a dependent end-to-end request even when average throughput rises.

The attention policy may depend on processor topology, service versions and interference traces. The official description does not expose features, action space, training protocol, transition rule, CPU, workload, tail-latency, fairness or overhead measurements.

**Source and location**

Evidence tier: Primary captured official DAC description only; no full paper extraction, scheduler reproduction or independent interference, qos, fairness and overhead validation. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH2395)

DAC 2026 official description; captured Problem, Mechanism / artifact, Workload, Hardware, Baseline, Measurements and Limits fields; record RESEARCH2395; no manuscript pages.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** OS scheduler

core-level placement

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH2395

**Hardware or process assumptions:** Multithreaded CPU with shared caches and hyperthreads; OS and hardware assumptions are unspecified.

**Limits:** No tail latency, throughput, fairness, overhead, or workload results are reported.

Attention policy may overfit interference patterns.

Official description only; multi-tenant validation is required.

**Method or artifact:** Hyperthread-level interference-aware scheduler using attention.

**Metrics:** Microservice scheduling efficiency is claimed qualitatively

**Problem:** Co-located cloud microservices interfere through shared CPU resources and need fine-grained scheduling.

**Workload or benchmark:** Cloud microservice workloads; CPU, QoS targets, and interference traces are unspecified.

</details>

<span id="paper-dac-2026-research2531"></span>

### PRISM: Dynamic Primitive-Based Forecasting for Large-Scale GPU Cluster Workloads

DAC 2026 · Record: `dac-2026-research2531`

[Read the step-by-step explanation](#explanation-dac-2026-research2531)

**Updated source-backed reading card**

Reviewed 2026-09-08. Deepens the official-description reading; separates workload primitives, dynamic forecast updates, forecast quality and the downstream scheduling decision, while preserving the missing deployment measurements.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

GPU-cluster demand changes with the kinds of work running and the resources each job needs, so a fixed forecast can become stale and cause poor allocation or queueing decisions.

**Mechanism / artifact:**

Dynamic primitive-based workload forecasting method; primitive definition and extraction, model, update cadence, forecast horizon and scheduler interface are unspecified.

**Workload — the work tested:**

Large-scale GPU-cluster traces; job mix, workload phases, arrival process, resource dimensions, time horizon and cluster topology are unspecified.

**Hardware and manufacturing assumptions:**

Distributed GPU cluster and scheduler with telemetry; GPU types, topology, monitoring path, preemption, migration and allocation policy are unspecified.

**Baseline — the comparison method:**

Static workload forecast

Generic time-series model

Forecast horizon, trace split, cluster and scheduler conditions are unspecified

**Reported measurements:**

Forecasting utility is claimed qualitatively; no error by horizon, calibration, burst detection, scheduling gain, queue time, utilization, preemption cost or forecast overhead is reported.

**Limits on the conclusion:**

A workload primitive must be defined as an observable and repeatable unit such as a job class, computation phase or resource-demand pattern; without that definition, it is not possible to tell what the model predicts or whether the primitive remains stable across clusters.

Dynamic updating can respond to concept drift, but it adds telemetry, update and cold-start costs and can react too slowly to short GPU bursts. Lower forecast error does not by itself establish lower queue time or better placement: a scheduler must use the forecast, and wrong predictions can cause fragmentation, preemption, migration or fairness loss.

The official description reports no forecast error, horizon, trace split, scheduling experiment, overhead, cluster topology or deployment result. The record therefore supports a forecasting direction, not demonstrated end-to-end GPU-cluster improvement.

**Source and location**

Evidence tier: Primary captured official DAC description only; no full paper extraction, forecasting reproduction or scheduler/deployment validation. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH2531)

DAC 2026 official description; captured Problem, Mechanism / artifact, Workload, Hardware, Baseline, Measurements and Limits fields; record RESEARCH2531; no manuscript pages.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** static workload forecast

generic time-series model

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH2531

**Hardware or process assumptions:** Distributed GPU cluster and scheduler; telemetry and preemption assumptions are unspecified.

**Limits:** No forecast error, horizon, scheduling gain, overhead, or trace results are reported.

Primitive distributions may change across clusters.

Official description only; trace and deployment validation is required.

**Method or artifact:** Dynamic primitive-based workload forecasting method.

**Metrics:** Forecasting utility is claimed qualitatively

**Problem:** GPU-cluster operators need forecasts that adapt to changing workload primitives and resource demand.

**Workload or benchmark:** Large-scale GPU-cluster traces; time horizon, jobs, and cluster topology are unspecified.

</details>

<span id="paper-dac-2026-research3208"></span>

### Making Sense of Job Preemption for Distributed Deep Learning Acceleration

DAC 2026 · Record: `dac-2026-research3208`

[Read the step-by-step explanation](#explanation-dac-2026-research3208)

**Updated source-backed reading card**

Reviewed 2026-09-08. Deepens the official-description reading; separates distributed-training progress from raw utilization and makes checkpoint, synchronization, restart, fairness and trace-validation costs explicit.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Preempting distributed deep-learning jobs can fill otherwise idle accelerator capacity, but it interrupts coordinated workers and can discard or delay useful training progress.

**Mechanism / artifact:**

Preemption analysis or scheduling method for distributed deep learning; victim-selection rule, checkpoint protocol, restart rule, communication handling and objective are unspecified.

**Workload — the work tested:**

Distributed training jobs; model type, worker count, job arrivals, checkpoint interval, convergence target, job priorities and cluster traces are unspecified.

**Hardware and manufacturing assumptions:**

Multi-node accelerator cluster; accelerator types, network topology, scheduler, storage path, checkpoint bandwidth, failure/restart behavior and synchronization protocol are unspecified.

**Baseline — the comparison method:**

Non-preemptive scheduling

Naive preemption

Job mix, cluster load, checkpoint policy, fairness rule and quality target are unspecified

**Reported measurements:**

Preemption efficiency is claimed qualitatively; no time-to-quality, useful-work loss, utilization, convergence, checkpoint/restart overhead, communication or trace result is reported.

**Limits on the conclusion:**

A distributed training step may require workers to exchange gradients or model state and reach a synchronization point. Preempting one worker can stall its peers, invalidate in-flight work or require a coordinated pause; accelerator utilization during a pause is not equivalent to useful training progress.

Checkpointing bounds restart loss only if the checkpoint captures a consistent distributed state and the storage and network costs fit the scheduling interval. Frequent checkpoints add I/O and synchronization overhead; infrequent checkpoints increase recomputation after preemption. A scheduler must also account for warm-up, data-loader state, optimizer state and communication state where relevant.

Higher utilization does not establish faster completion. The comparison must report time to the same quality target, convergence progress, queue delay, checkpoint and restart time, wasted computation, communication overhead, fairness and deadline or service-level outcomes across cluster traces. The official description reports none of these measurements, so it supports a preemption direction rather than demonstrated acceleration.

**Source and location**

Evidence tier: Primary captured official DAC description only; no full paper extraction, distributed training reproduction or cluster trace validation. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH3208)

DAC 2026 official description; captured Problem, Mechanism / artifact, Workload, Hardware, Baseline, Measurements and Limits fields; record RESEARCH3208; no manuscript pages.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** non-preemptive scheduling

naive preemption

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH3208

**Hardware or process assumptions:** Multi-node accelerator cluster; network, scheduler, and checkpoint assumptions are unspecified.

**Limits:** No time-to-quality, utilization, convergence, overhead, or trace results are reported.

Benefits depend on checkpoint and communication behavior.

Official description only; cluster-trace validation is required.

**Method or artifact:** Preemption analysis or scheduling method for distributed deep learning.

**Metrics:** Preemption efficiency is claimed qualitatively

**Problem:** Preempting distributed training jobs can improve cluster utilization but disrupt synchronization and progress.

**Workload or benchmark:** Distributed training jobs; models, cluster, checkpointing, and preemption policy are unspecified.

</details>

<span id="paper-dac-2026-research513"></span>

### Asymcheck: Asymmetric Partitioned Checkpointing for Efficient Large Language Model Training

DAC 2026 · Record: `dac-2026-research513`

[Read the step-by-step explanation](#explanation-dac-2026-research513)

**Updated source-backed reading card**

Reviewed 2026-09-08. Deepens the official-description reading; explains why checkpoint state can be partitioned asymmetrically and preserves the unresolved consistency, recovery, volume and failure-injection evidence.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Distributed LLM checkpoints can be large and can stall training or consume storage and network bandwidth, especially when all workers write state synchronously.

**Mechanism / artifact:**

Asymmetric partitioned checkpointing strategy; partition rule, state classes, write schedule, consistency protocol and recovery algorithm are unspecified.

**Workload — the work tested:**

Distributed LLM training; model size, optimizer and data-loader state, worker count, checkpoint interval, failure process and recovery target are unspecified.

**Hardware and manufacturing assumptions:**

Multi-node accelerator training with distributed storage; network topology, storage system, bandwidth, replication, durability and restart assumptions are unspecified.

**Baseline — the comparison method:**

Full synchronous checkpointing

Uniform partitioning

Model, state, worker, storage, failure and consistency conditions are unspecified

**Reported measurements:**

Checkpointing efficiency is claimed qualitatively; no checkpoint volume, write time, training overhead, recovery time, consistency or failure-injection result is reported.

**Limits on the conclusion:**

Asymmetry is useful only if the system identifies which state is large, frequently changed, expensive to write or required for exact recovery. A partition that is small or written less often is not automatically safe to delay: model, optimizer, random-number, data-position and scheduler state may have different correctness roles.

Partitioning changes the consistency problem. A restart must know which versions belong to the same training step and must detect missing, stale, duplicated or partially durable partitions. Independent writes can reduce a barrier, but they require versioning, completion metadata, failure detection and a recovery rule that does not silently mix states from different steps.

Lower checkpoint volume or write time does not establish faster training recovery. Evaluation must report bytes by state and worker, write and synchronization time, training slowdown, recovery time to useful work, recomputation, storage and network load, consistency checks and outcomes under injected worker, network and storage failures. The official description reports none of these measurements.

**Source and location**

Evidence tier: Primary captured official DAC description only; no full paper extraction, checkpoint implementation reproduction or failure injection validation. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH513)

DAC 2026 official description; captured Problem, Mechanism / artifact, Workload, Hardware, Baseline, Measurements and Limits fields; record RESEARCH513; no manuscript pages.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** full synchronous checkpointing

uniform partitioning

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH513

**Hardware or process assumptions:** Multi-node accelerator training with distributed storage; network and recovery assumptions are unspecified.

**Limits:** No checkpoint volume, training overhead, recovery time, consistency, or failure results are reported.

Asymmetry may complicate restart semantics.

Official description only; failure-injection validation is required.

**Method or artifact:** Asymmetric partitioned checkpointing strategy.

**Metrics:** Checkpointing efficiency is claimed qualitatively

**Problem:** Distributed LLM checkpoints are large and can stall training or waste storage bandwidth.

**Workload or benchmark:** Distributed LLM training; models, failures, storage, and workers are unspecified.

</details>

<span id="paper-dac-2026-research986"></span>

### Procyon: Promoting Fine-Grained Multi-Tenancy to Optimize Sparse Streaming Accelerators

DAC 2026 · Record: `dac-2026-research986`

[Read the step-by-step explanation](#explanation-dac-2026-research986)

**Updated source-backed reading card**

Reviewed 2026-09-08. Deepens the official-description reading; explains the occupancy-versus-interference tradeoff in fine-grained sparse-accelerator multi-tenancy and preserves the absent throughput, fairness, isolation, tail-latency, energy and workload evidence.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

A sparse streaming accelerator may leave compute or buffer capacity unused when one tenant cannot supply enough work, while running several tenants can improve occupancy but create interference.

**Mechanism / artifact:**

Fine-grained multi-tenant scheduling for sparse streaming accelerators; scheduling unit, admission rule, arbitration, resource partition, isolation mechanism and QoS objective are unspecified.

**Workload — the work tested:**

Sparse accelerator workloads from multiple tenants; sparsity format, arrival process, request deadlines, workload mix and quality targets are unspecified.

**Hardware and manufacturing assumptions:**

Streaming accelerator with shared buffers and compute; buffer hierarchy, execution slots, memory bandwidth, interconnect, isolation support and scheduling-control path are unspecified.

**Baseline — the comparison method:**

Single-tenant execution

Coarse multi-tenancy

Tenant mix, resource limits, QoS targets, hardware configuration and admission policy are unspecified

**Reported measurements:**

Multi-tenant accelerator efficiency is claimed qualitatively; no throughput, fairness, tail latency, isolation, energy or workload-diverse result is reported.

**Limits on the conclusion:**

Sparse work creates irregular demand: a tenant may have many logical operations but few active elements, or may generate bursts that compete for the same buffer, memory path or compute stage. Fine-grained interleaving can fill bubbles, but it can also increase arbitration, context, buffering and switching work.

Higher aggregate throughput does not establish that each tenant receives an acceptable service. The scheduler needs a stated isolation and fairness rule, and evaluation must show whether one tenant's sparsity pattern, memory traffic or burst can increase another tenant's tail latency or reduce its progress. Resource sharing can also affect reproducibility and quality when execution order changes.

The official description reports no throughput, fairness, tail-latency, isolation, energy, hardware, tenant-mix or workload result. The record supports a multi-tenancy direction, not demonstrated accelerator efficiency or QoS preservation.

**Source and location**

Evidence tier: Primary captured official DAC description only; no full paper extraction, accelerator reproduction or multi tenant isolation/qos validation. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH986)

DAC 2026 official description; captured Problem, Mechanism / artifact, Workload, Hardware, Baseline, Measurements and Limits fields; record RESEARCH986; no manuscript pages.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** single-tenant execution

coarse multi-tenancy

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH986

**Hardware or process assumptions:** Streaming accelerator with shared buffers and compute; isolation and scheduling assumptions are unspecified.

**Limits:** No throughput, fairness, tail latency, isolation, energy, or workload results are reported.

Fine-grained sharing may increase interference.

Official description only; multi-tenant validation is required.

**Method or artifact:** Fine-grained multi-tenant scheduling for sparse streaming accelerators.

**Metrics:** Multi-tenant accelerator efficiency is claimed qualitatively

**Problem:** Sparse streaming accelerators may be underutilized when serving one tenant at a time.

**Workload or benchmark:** Sparse accelerator workloads; tenants, QoS, and hardware are unspecified.

</details>

## What remains to establish

Resolve unspecified workloads, comparison methods, resource budgets, and source locations before generalizing a reported gain. Multiple papers in this selected sample permit comparison of mechanisms, but do not by themselves establish recurrence across years or a long-term trend.

[All subthemes](../expanded-taxonomy-v1.md) · [Research directions](../directions/README.md)
