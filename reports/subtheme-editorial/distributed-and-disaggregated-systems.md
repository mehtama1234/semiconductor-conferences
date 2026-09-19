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
