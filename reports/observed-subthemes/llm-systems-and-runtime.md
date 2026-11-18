# LLM systems and runtime

This subject has 10 records in the selected sample. This page explains where it fits, then presents all captured paper evidence without shortening the measurements or limitations.

[Definitions used in the paper records](../reading-guide-v1.md)

## Understand the parent subject first

- [Systems applications and workloads](../themes/systems-applications-and-workloads.md)

## A model needs a process that manages its execution

A trained language model specifies a computation. A running system must load its parameters, allocate memory, schedule operations, and manage requests or training steps. Runtime software performs decisions during execution rather than fixing every choice in advance.

Training, fine-tuning, and inference create different requirements. Training updates model parameters. Fine-tuning adapts an existing model using further training. Inference executes a trained model to produce outputs. A result for one phase does not automatically establish an improvement in another.

## Look at complete work and its dependencies

Execution consists of operations that read and produce values. Some operations can run together; others must wait for earlier outputs. Hardware can be idle because inputs are unavailable, memory is full, or another activity owns a shared resource.

A runtime changes when work happens and where its state resides. It can reduce idle time or memory use while adding scheduling, transfer, or bookkeeping costs. The evaluation must include the work moved elsewhere rather than measuring only the accelerated portion.

<span id="explanation-dac-2026-research1286"></span>

## Single-GPU fine-tuning can still use other resources

The heterogeneous fine-tuning record proposes coordinated algorithm and hardware choices around one GPU. “Single GPU” specifies the number of those accelerators; it does not establish the total CPU, memory, storage, or communication resources used. [Recorded evidence](../observed-subthemes/llm-systems-and-runtime.md#paper-dac-2026-research1286)

Moving state or computation away from the GPU can make a larger task possible but also add transfers. The meaningful comparison includes time to achieve the required model quality and all resource consumption. It also includes the conditions of the comparison method. The captured description leaves those quantities unresolved.

Fine-tuning changes model parameters using examples. A training step usually reads parameters, computes activations, stores or recomputes intermediate values, computes gradients, and updates parameters. Depending on the optimizer, the system may also keep optimizer states such as momentum or second-moment estimates. These objects can consume more memory than the model weights alone. A “single-GPU” method may therefore place some state in CPU memory, another device, storage, or a custom processing path. It may still retain one GPU for the main computation.

The first design question is which state moves across which boundary. In a single GPU system, moving a layer’s weights before every use has a different cost. That cost differs from moving optimizer states once per update or checkpointing activations for later recomputation. The evaluation should identify the bytes transferred, transfer direction, frequency and link bandwidth. It should identify overlap with computation, synchronization points, and pinned-memory or storage requirements. It should also say whether page faults or allocation overhead are included. A method can fit the model in nominal capacity. It can still fail to meet useful throughput because transfers serialize the critical path.

Algorithm and hardware co-design can also change the amount of work, not merely where it runs. Parameter-efficient fine-tuning may update adapters or low-rank components instead of all weights. Quantization, activation recomputation, optimizer changes, layer scheduling, microbatching and offload policy can each alter memory and computation. A comparison must state which of these changes are part of the proposed method. It must also state whether the baseline reaches the same final quality with the same trainable parameter set.

Memory capacity is not the same as trainable-task feasibility. The method must preserve the optimizer state, gradient precision and numerical stability. It must also preserve checkpoint/restart state, data pipeline and validation behavior required by the training objective. If some tensors are compressed or recomputed, report the numerical effect and the extra computation. If state is evicted to host memory, report CPU contention and memory pressure. If storage is used, report I/O bandwidth, endurance assumptions and failure behavior.

The correct performance denominator is time-to-quality, not only tokens per second or one kernel’s latency. Define the target loss, evaluation metric, dataset, and number of epochs or update steps. Also define the convergence rule, random seeds and acceptable quality variance. A method that processes tokens faster but converges more slowly has not shown a training improvement. Neither has one that reaches a lower final quality. Report preparation, loading, transfers, validation, checkpointing, failures and recovery when they are required for a fair run.

The baselines should include standard single-GPU fine-tuning using the same model and quality target. They should also include a named multi-GPU configuration, and relevant offload or parameter-efficient methods. “Multi-GPU” is not automatically a fair lower-bound comparison: it may use a different parallelism strategy, memory capacity, interconnect, batch size or quality target. Report GPU memory, host memory, storage, CPU utilization and interconnect traffic. Also report total energy, wall-clock time, throughput, time-to-quality and cost per completed run.

The captured description supports a heterogeneous algorithm-hardware direction for making large-model fine-tuning possible around one GPU. It does not specify models, datasets, parameter-efficient versus full fine-tuning, quality criteria, GPU/interconnect, time-to-quality, memory, throughput, energy or accuracy. The evidence supports a capacity-and-runtime co-design direction, not demonstrated single-GPU training efficiency across model families.

<span id="explanation-dac-2026-research2300"></span>

## Hero: mobile RAG orchestration must preserve retrieval and answer quality while respecting device limits

Retrieval-augmented generation (RAG) combines two stages. In a retrieval-augmented generation pipeline, a retriever selects documents or passages from an index using a query. A generator uses the query and retrieved context to produce an answer. The system can improve factual grounding, but retrieval errors and generation errors are different. A runtime that reduces latency by retrieving fewer or less relevant passages may lower answer quality. This can happen even if the language model runs faster.

Hero is described as adaptive orchestration across a heterogeneous mobile system-on-chip (SoC). A mobile SoC may contain CPU, GPU and NPU resources with different throughput, memory access, power, thermal and software characteristics. The orchestration policy may decide where retrieval, embedding, reranking, prompt construction and generation run. It may decide how data moves between memories. It may also decide when to use local or cloud resources. Each decision changes both performance and the evidence available for judging the answer.

The first requirement is to define the query path. Record query encoding, index access, candidate count, reranking and context length. Also record prompt assembly, generation model, output length, cache state, and any network round trip. Report retrieval recall or precision, context relevance and answer correctness. Also report citation or grounding quality, refusal behavior, and hallucination or unsupported-answer rate. Report these separately from latency. End-to-end answer quality cannot be inferred from retrieval speed or token throughput alone.

Adaptive placement needs an observable state and a decision cost. The policy may use query length, expected retrieval difficulty, model confidence, battery level and temperature. It may also use queue state, memory pressure, network quality or historical workload. It must state how these signals are measured and how often the policy changes placement. It must also state how much computation and data movement the decision adds. A policy trained or tuned on one query distribution may choose poorly for something different. That could be a different language, topic, index size, user mix or connectivity condition.

Heterogeneous execution has multiple boundaries. Moving an embedding or retrieved context between CPU, GPU, NPU and shared memory consumes bandwidth. It may also require format conversion or synchronization. Sending a query or context to the cloud adds network latency, energy, privacy exposure and availability dependence. A local-versus-cloud comparison must use the same quality target, privacy policy, network condition, model version and output length. Cloud latency alone is not a complete baseline.

Mobile constraints are dynamic. Battery state, thermal throttling, background applications, memory pressure and user-visible latency can change during one session. Report cold and warm cache behavior, sustained execution, thermal steady state and battery energy. Also report peak and average power, memory footprint, throttling and queueing. Also report first-token latency, total response latency and tail percentiles. An average speedup under a short benchmark does not establish sustained mobile efficiency.

The comparison should include static local placement, a fixed heterogeneous placement, cloud RAG, and the adaptive policy. Hold the index, retriever, generator, prompt, output quality, context limit, quantization and query set constant. Use workload splits that hold out queries, topics, index updates, devices and network states. Report policy errors. These are cases where the chosen placement misses a quality target or exceeds a latency service-level objective. They also include cases where it consumes more energy than the available budget.

The captured description identifies adaptive RAG orchestration on a heterogeneous mobile SoC. It reports no answer quality, retrieval quality, latency, energy, memory, thermal or workload-diverse results. Adaptive choices may depend on query distribution. The evidence supports a mobile RAG runtime direction, not demonstrated quality-preserving orchestration across devices and workloads.

<span id="explanation-dac-2026-research235"></span>

## Sandwich: hot-switching can adapt CPU serving only if switch cost and tail behavior remain inside the service objective

CPU LLM serving is a sequence of requests competing for cores, memory bandwidth, caches, power and thermal headroom. A serving configuration may include thread count, core affinity, vectorization, batch size and quantization. It may also include kernel choice, frequency policy, context handling, KV-cache policy and request admission. A configuration that is best for one request mix can be poor for another. Long prompts, short prompts, concurrent requests and output lengths stress different resources.

Sandwich is described as joint configuration search and runtime hot-switching. Configuration search chooses candidate settings and measures or predicts their behavior. Hot-switching changes the active setting while the service is running. These are separate mechanisms. Offline search can find a good configuration under its training workload. Runtime switching must decide when the workload has changed enough to justify a switch. It must also pay the cost of changing state.

The switching path must be defined. A change may drain requests, alter thread placement, rebuild kernels or resize a batch. It may invalidate or reduce cache locality, change KV-cache layout, adjust frequency, or wait for an in-flight operation. Measure switch duration, requests stalled, tokens lost, cache warm-up, queue growth, temporary memory, frequency transition and the configuration’s first-request behavior. A lower steady-state latency does not compensate for repeated switch penalties unless the workload intervals are long enough.

Serving quality is usually expressed through service-level objectives (SLOs), not only average throughput. Define time to first token, inter-token latency, total response latency and deadline violation. Also define throughput, admission behavior and tail percentiles such as p95 or p99. A configuration may improve average tokens per second. If it creates deadline misses or long pauses during switching, it may be worse for the service. Report quality or output-equivalence changes from quantization, batching, truncation and other configuration choices separately from runtime metrics.

Joint search also has an exploration cost. Testing configurations consumes requests, warm-up time, CPU cycles and possibly user-visible capacity. The search should state whether it uses an offline trace, a simulator, a model, safe canary traffic or live exploration. If it learns from observed workload, separate search requests from production requests. Report how quickly it adapts and how often it selects a poor configuration. Also report what prevents oscillation between configurations.

The workload must include changing conditions. These are request arrival rate, prompt length, generated length, concurrency, model and quantization. They also include cache state, background CPU activity, thermal state and power limit. Configuration quality can be workload-specific. A policy trained on a stable trace may fail under a burst or a mixture of long and short requests. Evaluate held-out traces and workload transitions, not only stationary averages.

The baselines should include a static configuration selected offline and the best fixed configuration for each known workload. They should also include offline tuning without runtime switching. Compare equal model quality, request distribution, CPU platform, thread/core budget, memory limit, frequency policy, warm-up, cache state and measurement boundary. Report switch frequency, switch cost, SLO attainment, tail latency, throughput, energy, CPU utilization, memory, configuration-search time and quality.

The captured record identifies joint configuration search and runtime hot-switching for CPU LLM serving. It reports no latency, throughput, quality, switch time, energy or workload results. Switching may disrupt cache state and tail latency. The evidence supports an adaptive CPU-serving direction, not demonstrated SLO-safe hot-switching across models and workload changes.

<span id="explanation-dac-2026-research256"></span>

## PREBA: multi-instance GPU serving must control interference, memory pressure and tail latency across tenants

Multi-instance GPU inference means that more than one inference workload uses one physical GPU at the same time. The instances may receive separate partitions, streams, memory regions, scheduling shares or combinations of these. The physical GPU still has shared resources. These are execution units, on-chip caches, memory bandwidth, memory capacity and copy engines. They also include power, thermal headroom, driver state and sometimes scheduling queues. A tenant can therefore affect another tenant even when the software presents the instances as separate services.

PREBA is described as hardware/software co-design for multi-instance GPU-based AI inference servers. “Co-design” should identify the hardware mechanism, the software policy, the control loop between them, and the resource that each mechanism changes. A hardware partition, a memory controller, a request scheduler, a model-placement policy and a batching policy solve different problems. Combining them in one system does not by itself show that their interaction is necessary. It also does not show that the combined design is better than well-tuned software on the same GPU.

The first system question is the isolation boundary. State whether an instance receives a fixed slice of compute, memory, cache, bandwidth, power or time. State whether it can borrow unused capacity. Also state what happens when it exceeds its allocation. A logical partition is not the same as performance isolation. If two instances share memory bandwidth or cache, measure how the other's latency changes. Vary one tenant's request rate, model, sequence length or batch size. If the design claims security or fault isolation, define the information or failure channel. Test it separately from performance interference.

Inference serving has more than one resource demand. A request may need model weights, activations, key-value cache, temporary workspace, input processing, output sampling and host-device transfers. Large or long-context requests can consume memory for a long time. Admission control must say what happens when the memory budget is full. A request may be rejected, queued, preempted, migrated or allowed to cause eviction. A throughput result without memory occupancy and request-level behavior can hide failures caused by cache growth or allocation stalls.

The serving objective must be stated per tenant and for the system as a whole. Measure time to first token, inter-token latency, complete response latency, throughput and queueing delay. Also measure deadline or service-level-objective violations, and p95/p99 or worse tail percentiles. Report each tenant's result, not only the aggregate. A policy that raises total throughput by starving a small tenant is not a fair multi-instance result. Neither is one that improves the mean while producing long pauses for one model. Define fairness explicitly, such as minimum guaranteed throughput, weighted service share, slowdown relative to isolation, or a bounded latency increase.

Scheduling decisions also have costs. The policy may choose instance size, core share, memory placement, batch formation and request order. It may also choose preemption, model migration, precision, clock state or power allocation. Each decision can require synchronization, context changes, kernel completion, cache effects, data movement or model reload. Measure decision frequency, reconfiguration time, work lost, queue growth, memory fragmentation, warm-up and the effect on in-flight requests. A hardware/software policy that is effective only after long stable intervals may not handle bursty tenants. A policy that changes too often may spend its gain on control overhead.

The workload must represent the sharing problem. Include multiple models, model sizes, input and output lengths, batch sizes and arrival rates. Also include concurrency, burst patterns, memory footprints, accelerator kernels and tenant priorities. Evaluate balanced tenants, a heavy tenant beside light tenants, synchronized bursts, long-context requests, changing mixes and failures or restarts. A single model at a fixed rate tests GPU execution, not multi-tenant interference. If the method targets a particular GPU-generation feature, state the supported partition sizes, driver/runtime versions and portability boundary.

Energy and cost need the same boundary as performance. Report total server energy, energy per request or token, power limit and clock state. Also report cooling or thermal condition, host CPU and memory use, and the cost of reserved versus borrowed capacity. A design can improve GPU utilization while increasing host work, memory traffic, cooling demand or failed requests. Compare the same model quality, precision, output length, request mix, admission policy and end-to-end measurement boundary.

The baselines should include one instance per GPU, conventional multi-instance GPU partitioning, and default multi-instance scheduling. Add an oracle or offline allocation when possible to show the gap between the policy and a workload-specific upper bound. Hold the physical GPU, driver, model versions, quantization and request traces constant. Also hold tenant priorities, memory limit, power limit, warm-up, cache state and quality target constant. Report an ablation for hardware changes and for software policy so the source of each gain is visible.

The captured record identifies hardware/software co-design for multi-instance GPU inference and qualitatively claims server efficiency. It reports no GPU generation, partition mechanism, tenant mix, tail latency, throughput, fairness, energy, isolation, memory behavior or workload-diverse result. The evidence supports a multi-tenant GPU serving direction, not demonstrated QoS-safe, fair or portable inference-server efficiency.

<span id="explanation-dac-2026-research2620"></span>

## Deinfer: decomposed-model parallelism is useful only when dependency and communication costs stay below the saved inference time

A decomposed language model is a model whose computation or parameters have been split into parts. These parts can be placed or executed separately. Decomposition can expose parallel work, allow a model larger than one device, or map different components to different resources. It also creates boundaries. Values must cross those boundaries and workers must synchronize. The system must preserve the order and numerical meaning required by the model.

Deinfer is described as an inference system for parallel inference of decomposed large language models. It has multiple optimizations intended to improve performance and remain compatible with other inference optimizations. The description does not identify the decomposition. It could separate layers, tensor dimensions, experts, attention and feed-forward parts, pipeline stages, or another model representation. Those choices have different dependency graphs, communication volumes, memory needs and failure behavior. So the system must state the exact graph and placement before its speed claim can be interpreted.

The first principle is to expose the critical path. For each generated token or batch, identify which operations can run concurrently. Identify which values they read and which values they produce. Also identify which operations must wait. Measure compute time, communication time, synchronization time and queueing. Also measure scheduling overhead, memory movement, kernel launch or runtime overhead, and idle time at every device. Parallelism helps only when useful work overlaps. The saved computation must also be greater than the cost of moving data and coordinating workers.

Autoregressive generation makes this especially important. A new token often depends on the state produced for the previous token. Some work can be batched across requests or split across model components. A fine-grained cross-device boundary may add a synchronization to every token. Report prefill and decode separately, because long prompt processing and one-token-at-a-time generation stress the system differently. Include time to first token, inter-token latency, complete response latency, throughput, batch/concurrency and tail percentiles.

Communication must be described in bytes and timing, not only as an implementation detail. State what crosses each boundary: activations, weights, key-value cache, logits, metadata or control messages. Report message size, frequency, direction, link, bandwidth, latency, serialization, overlap with compute, synchronization points and copies through host memory. A topology that works for a large batch may fail for small requests if fixed message latency dominates. A method that fits model weights across devices may still be limited by activation or KV-cache traffic during decoding.

Compatibility with existing optimizations is a claim that needs a defined composition. Quantization changes bytes and numerical error. Batching changes available parallel work and queueing. Kernel fusion changes boundaries. Speculative decoding changes the number of tokens proposed and verified. Caching changes reuse and memory occupancy. The evaluation should show whether each optimization is applied before or after decomposition. It should show whether it changes the dependency graph. It should also show whether the proposed scheduler still preserves output quality and acceptance behavior.

Model quality must remain comparable. Parallel execution should produce the same result within a stated numerical tolerance. Otherwise the paper must report the quality change from quantization, approximation, partitioning, or reordered operations. Compare perplexity or task accuracy for the same model and decoding rule, and report output differences if floating-point order changes. A faster system that silently changes the model or stopping rule is not an isolated systems improvement.

The baselines should include monolithic inference on the largest feasible device and sequential execution of the same decomposition. They should also include a standard distributed or tensor/pipeline-parallel implementation when applicable. Hold model weights, decomposition, precision, prompt/output lengths and decoding parameters constant. Also hold batch, concurrency, warm-up, cache state, device count, interconnect and end-to-end timing boundary constant. Include a scaling study as devices increase and an ablation of communication overlap, scheduling, memory placement and other claimed optimizations.

Small requests and low concurrency are a critical boundary condition. Their compute is short, so fixed coordination and transfer costs can dominate. Large batches may hide those costs while increasing queueing and latency. Evaluate short and long prompts, short and long generations, and low and high concurrency. Also evaluate balanced and imbalanced partitions, cold and warm state, and changing request mixes. Report scaling efficiency, device utilization, communication fraction, memory use, energy per token or response and cost per completed request.

The captured record says that DeInfer targets parallel inference of decomposed LLMs and claims extensive experiments. However, the captured evidence reports no model decomposition, device topology, quality, latency, throughput, communication, energy or scaling result. Decomposition overhead may dominate small requests. The evidence supports a distributed LLM inference-system direction. It does not demonstrate efficient and quality-preserving parallel inference across model sizes, request regimes and hardware topologies.

<span id="explanation-dac-2026-research292"></span>

## SmoothSpec: speculative decoding gains throughput only when draft quality, verification work and asymmetric resource allocation are measured together

Autoregressive language-model decoding normally generates one next token, appends it to the sequence, and repeats. Speculative decoding adds a draft model or draft procedure. The draft proposes several tokens. A target model verifies them in parallel. Accepted tokens advance the sequence and rejected tokens require a correction. The method can reduce the number of expensive target-model steps. Its benefit depends on how many proposed tokens are accepted. It also depends on how much draft and verification work is added.

The paper record describes SmoothSpec as an intra-device parallel speculative-decoding system. It uses the same parallelism configurations for draft and target models. It allocates compute asymmetrically at runtime. It also adjusts draft parameters and the resource-allocation ratio using draft-token generation quality. These are separate mechanisms. The draft parameter policy changes proposal quality and cost. The resource policy changes contention between draft and target work. The scheduler decides when and how those choices change. A fair reading must measure each mechanism and their interaction.

The basic accounting is accepted useful tokens per unit of end-to-end time. Let the draft produce a proposal and let the target verify it. Count accepted tokens plus the corrected token that advances generation under the exact algorithm. Report proposal length, acceptance rate by position, rejected-token frequency, target evaluations, draft evaluations and generated tokens. Also report time for draft, verification, synchronization, scheduling and output handling. A higher acceptance rate is not sufficient if the draft becomes expensive. It is also not sufficient if target verification occupies the device while the draft is being prepared.

Intra-device parallelism means the draft and target share one accelerator's compute units, memory system, caches, queues, power and thermal limit. Asymmetric allocation can improve overlap, but changing the ratio can also create starvation, preemption, cache disruption or memory pressure. Define the allocation unit and whether resources are partitioned or time-shared. Also define how in-flight kernels are handled, and the cost and frequency of changing the ratio. Measure achieved utilization for each model, contention, memory traffic, queueing, clock state and reconfiguration overhead. Do not infer utilization from an allocation percentage.

The control signal needs a precise definition. “Generation quality of draft tokens” could mean acceptance probability, accepted-prefix length, target-model score, confidence, entropy, a learned predictor or a recent moving average. State the observation window, warm-up, decision interval, parameters changed, exploration rule, hysteresis and protection against oscillation. A controller trained on one model or request mix may react too slowly to bursts or overreact to noise. Evaluate transitions between low and high acceptance, changing prompt domains, concurrency and request lengths.

Quality and speed are coupled. Draft parameters may change sampling temperature, number of draft steps, vocabulary filtering, quantization, layer usage or another approximation. The target verification algorithm must preserve the intended output distribution if exact speculative decoding is claimed. If the system changes the distribution, compare perplexity, task quality and output agreement. Also compare acceptance behavior and stopping semantics under the same decoding settings. Do not treat accepted-token count as model quality.

Serving evaluation must separate prefill from decode. It must report time to first token, inter-token latency, total response latency, and throughput in useful output tokens per second. It must also report p50/p95/p99 tails, batch size, concurrency, queueing and deadline violations. Include cold and warm starts, model loading, memory allocation, KV-cache behavior, output streaming and scheduler overhead. Throughput improvements at high batch size can coexist with worse interactive latency; both are relevant for a serving claim.

The baselines should include ordinary autoregressive decoding. They should include standard speculative decoding with a fixed draft and fixed resource split. They should also include an oracle or offline resource split when feasible. Hold target model, draft model or draft quality, precision, decoding rule and prompt/output distributions constant. Also hold batch, concurrency, device, clock/power state, warm-up and measurement boundary constant. Ablate dynamic draft-parameter selection and dynamic resource allocation independently. Report memory, energy per generated token, device generation, software stack and scaling across models or model pairs.

The captured description identifies a single-node system that dynamically adjusts draft parameters and the resource allocation ratio. However, the stored evidence reports no acceptance rate, latency, throughput, memory, energy or model result. Parallelism may be device-generation specific. The evidence supports adaptive intra-device speculative decoding, not demonstrated quality-preserving throughput or tail-latency improvement across model pairs and serving workloads.

<span id="explanation-dac-2026-research538"></span>

## Amoeba: changing tensor parallelism at runtime requires state migration and SLO-safe reconfiguration

Tensor parallelism splits a model operation across multiple devices. Each device holds or computes part of a tensor. The devices exchange partial results so that the next operation sees the complete value. The degree of tensor parallelism is the number of participating devices or partitions. A larger degree can provide more aggregate memory and compute for a large request. It also adds communication. It may also reduce the number of independent instances that can run concurrently.

Amoeba is described as a runtime transformation that changes tensor parallelism for running LLM inference instances. It does so as incoming request context lengths change. The underlying tension is concrete. Long-context requests need memory for a growing key-value (KV) cache and may benefit from more parallel resources. Short-context requests may use fewer resources and allow more concurrent instances. Changing the layout while a service is running is not the same as selecting a layout at startup. The system must preserve model state, request state and numerical correctness while moving from one execution arrangement to another.

The transformation protocol is the central artifact. State whether the system drains requests or pauses them. State also whether it migrates them at a safe boundary, or transforms an active instance in place. Identify what moves: model weights, activations, KV-cache blocks, scheduler metadata, sequence position, requests, communication groups and allocator state. Report bytes moved, links used, synchronization, temporary capacity and memory fragmentation. Also report kernel rebuilding, cache warm-up, failed or retried requests, and the time during which the instance cannot make progress. A higher-throughput steady state does not justify a policy if repeated transformations create queueing or deadline violations.

KV-cache behavior needs separate accounting. During autoregressive generation, the cache stores key and value tensors for prior tokens. The model then does not recompute the complete prefix. Its size grows with context length, layers, heads, precision and batch or sequence count. A change in tensor-parallel degree may require repartitioning those tensors or changing their layout. It may require copying them between devices, or temporarily keeping both old and new representations. Measure cache bytes, partitioning cost, reuse after migration, fragmentation, eviction and recomputation. Also measure the effect on time to first token and inter-token latency.

The policy needs an observable state and a decision rule. It may use incoming context length, expected output length, queue length and current KV-cache occupancy. It may also use arrival rate, device availability, model size or predicted service-level-objective risk. Define how far ahead the system predicts and what threshold triggers a change. Also define how it avoids oscillation, and how it behaves when a long request arrives during migration. A request’s context length is not the whole workload. Generated length, concurrency, prompt reuse, cache state and other tenants affect the required capacity.

Serving quality must be measured end to end. Report time to first token, inter-token latency, total response latency, throughput, queueing delay and p50/p95/p99 tail latency. Include SLO or deadline violations during and after transformation. Separate prefill from decode and include short-context and long-context requests. Report per-request and aggregate results because a throughput average can hide long pauses for the request being migrated. Include cold and warm cache behavior, model loading, admission, cancellation, failures and recovery.

The comparison should include static tensor parallelism at each relevant degree and data-parallel serving. It should also include a policy that routes new requests without transforming running instances. The static configurations should be measured on the same model, precision, devices, interconnect and request traces. They should also use the same context/output lengths, concurrency, power state and quality target. Add an oracle or offline assignment where possible. Report the claimed throughput range only with the exact workloads, baseline, timing boundary and confidence or variation. The captured description states a 1.75×–6.57× throughput improvement over state-of-the-art solutions. It does not expose the conditions needed to reproduce or interpret that range.

Resource accounting must include the devices used by idle and active instances and communication traffic. It must also include host CPU, memory, storage, energy and cooling or power limits. More tensor-parallel resources per long request can increase single-request capacity while reducing system-wide concurrency. The objective must say whether it optimizes aggregate throughput, latency, tail SLO attainment, cost, energy, or a constrained combination. Model quality and output behavior must remain constant across transformations.

The captured description supports runtime tensor-parallel transformation for context-varying LLM inference. It reports a claimed 1.75×–6.57× throughput range on real-world traces. It does not report migration time, latency, KV-cache movement, quality, energy, SLO behavior or model/device-diverse validation. The evidence supports adaptive parallelism as a serving direction, not demonstrated SLO-safe reconfiguration or general throughput improvement.

<span id="explanation-dac-2026-research628"></span>

## Faster-MoA: reducing agent connections changes both the computation graph and the answer evidence

Mixture-of-Agents (MoA) serving runs several language-model agents and combines their outputs. The agents may propose answers, critique one another, specialize by task, or feed results into later agents. An all-to-all design allows many agent-to-agent connections, but those connections create communication, scheduling and inference work. A tree structure, early exit and overlapping prefill with decode can reduce work. Each change also changes which agents contribute and when.

Faster-MoA is described as a unified algorithm-system co-design with three parts. The first is a hierarchical tree instead of all-to-all connectivity. The second is runtime early exit based on output semantic similarity and answer confidence. The third is agent-dependency-aware incremental prefilling that overlaps prefill and decode. These are not interchangeable optimizations. The tree changes the dependency graph; early exit removes computation and evidence; overlap changes scheduling without necessarily removing model work. The evaluation must isolate them and explain how the resulting system still implements the intended MoA behavior.

The tree needs a precise execution graph. Define the agents, edges, parent/child dependencies, message contents, ordering, fan-in/fan-out, synchronization and failure behavior. An all-to-all graph may produce multiple independent views before aggregation. A tree can make early decisions influence later agents and can amplify one weak intermediate answer. Report messages, bytes, communication time, agent idle time, and the critical path for each stage. A lower edge count is not automatically lower latency if the tree creates serial depth or load imbalance.

Early exit is a quality-changing decision. Semantic similarity can indicate that two outputs are close without showing that either is correct. Confidence can be poorly calibrated, task-dependent or correlated with agreement rather than truth. Define the similarity representation, confidence estimator, threshold, calibration data, exit point, minimum agent coverage and fallback behavior. Measure exit rate by task and input difficulty, agents skipped, answer changes and uncertainty. Also measure correctness, factuality, groundedness, refusal/safety behavior and disagreement cases. Compare to running all agents under the same prompt and decoding settings.

Prefill and decode have different dependencies. Prefill processes the prompt and creates attention state; decode generates tokens sequentially while reading the key-value (KV) cache. Overlap is valid only when the consumer does not read a value before its producer has completed. It is also valid only when KV-cache updates are consistent. Specify which agent phases overlap and what data is ready at each boundary. Also specify how partial outputs are represented, and how cancellation or a late parent result is handled. Measure overlap achieved, synchronization stalls, KV-cache memory, queueing, speculative or discarded work, and output equivalence.

“Similar accuracy” must identify the task metric and denominator. The captured description claims up to 90% lower end-to-end serving latency relative to all-to-all MoA baselines. It claims similar accuracy, described as only ±1% variation, or sometimes higher task accuracy. That claim does not establish equal answer quality across tasks, seeds, prompts, agent models, output lengths or exit rates. Report per-task results, confidence intervals or repeated trials, answer correctness and calibration. Also report latency percentiles, throughput and the full distribution of quality changes.

End-to-end latency must include all agent inference, prompt construction, communication, scheduling and synchronization. It must also include prefill, decode, early-exit decisions, output aggregation, model loading and queuing. Report time to first token, total response latency, p50/p95/p99, throughput, concurrency, token counts and resource use. The user may see a final answer only after all agents complete. In that case, measure streaming or internal overlap up to the final answer boundary. It must not be measured only to an intermediate token.

The baselines should include all-to-all MoA and the same MoA with tree connectivity only. They should include tree plus early exit only, tree plus overlap only, and sequential agent execution. They should also include a strong single-model or standard serving baseline where the quality target permits. Hold agent models, prompts, task set, output budget, decoding, hardware, interconnect, batch/concurrency, warm-up and measurement boundary constant. Ablations are necessary. A claimed co-design gain may come mainly from skipping agents, changing the answer procedure, or changing the hardware allocation.

The captured description supports a tree-structured, early-exit and overlap-aware MoA serving runtime. It reports a claimed up-to-90% latency reduction with approximately ±1% accuracy variation in the described comparison. It does not report task-level quality, exit behavior, communication, throughput, energy, tail latency, agent models or hardware conditions. Early exit may alter agent consensus and answer evidence. The evidence supports a conditional low-latency MoA direction, not demonstrated quality-preserving serving across tasks, models and workloads.

<span id="explanation-dac-2026-research1414"></span>

## Checkpointing trades ordinary execution cost against recovery

A checkpoint preserves enough state to resume work after a failure. Producing it consumes transfer and storage resources. An incomplete or inconsistent saved state can fail to reproduce the intended continuation, even if writing the checkpoint was fast.

Expcheck's captured method adapts checkpointing to expert activity in mixture-of-experts models. Experts are model components selected for particular inputs. The design question is which state must be saved to preserve a valid recovery point when activity differs among components. [Recorded evidence](../observed-subthemes/llm-systems-and-runtime.md#paper-dac-2026-research1414)

The record does not establish saved-state volume, normal-execution overhead, failure timing, or recovery behavior. A smaller checkpoint is useful only after the required recovery semantics are established. Tests should interrupt execution at relevant points and compare the resumed state with the intended behavior.

In mixture-of-experts (MoE) training, a router selects a subset of expert networks for each token. Expert activity is therefore uneven across batches and time. A checkpoint must preserve enough state to resume the same training computation. Preserving merely the experts that were active in the most recent batch is not enough. That may include shared parameters, expert parameters, optimizer states, and gradients or accumulation state. It may include router state, random-number state, data position, scheduler state and loss-scaling state. It may also include expert placement, communication state, and metadata that determines which values are valid.

An activity-aware checkpoint can reduce storage or transfer. It does so by exploiting the fact that some experts did not change. It also exploits that some experts were not used in a given interval. The safety question is whether an omitted value is guaranteed to be reconstructible or unchanged. This matters when it is needed after restart. “Inactive” is not the same as “irrelevant”: a previously inactive expert may be selected by the next batch, and an optimizer state can matter even when a parameter received no current gradient. The method must define its dependency rule and the point at which a state becomes safe to omit.

Checkpoint consistency is a distributed-systems problem as well as a storage problem. All workers need a compatible view of shared parameters, expert parameters, optimizer updates, router decisions, data ordering and communication progress. A checkpoint can be taken while some workers have advanced and others have not. It can then produce a state that cannot be resumed deterministically. The design should specify barriers, version numbers, write ordering, metadata, partial-write handling, replicas and checksums. It should also specify how a failed checkpoint is detected and discarded.

The recovery point is the exact training state represented by the checkpoint. Test failures during forward computation, backward computation, optimizer update, expert communication, checkpoint writing, storage transfer and data loading. After restart, compare the resumed state and subsequent update against an uninterrupted reference under deterministic conditions. If nondeterminism is allowed, report an acceptable divergence in loss, parameters, router decisions and final quality. Do not treat any completed run as recovery success.

Storage reduction and training speed are separate outcomes. A smaller checkpoint may reduce write time and storage capacity. It may also require reconstruction, extra metadata, more frequent checkpoints, or a longer recovery path. Report checkpoint interval, bytes written, write bandwidth, normal-training slowdown and memory pressure. Also report storage cost, recovery time, lost work after a failure, failure-detection time and final quality. Include the cost of saving inactive-state metadata and any replication or erasure coding.

The baseline should include periodic full checkpointing and an expert-agnostic policy. Use the same MoE model, expert count, optimizer, batch schedule, failure distribution and recovery target. Compare activity-aware storage with an explicitly defined exact-recovery baseline. If the method provides approximate recovery, state the divergence criterion and do not call it exact restoration. Activity distributions can depend on the dataset and router training, so evaluate balanced, skewed and changing workloads.

The captured record supports activity-aware checkpointing as a way to reduce the cost of MoE training recovery. It does not report saved-state volume, normal-execution overhead, failure timing, recovery point, restart correctness, storage system, or recovery results. The evidence supports a checkpoint-policy direction, not demonstrated exact recovery or general checkpoint efficiency across MoE systems.

<span id="explanation-dac-2026-research2169"></span>

## Arithmetic intensity can help identify a limiting resource

Arithmetic intensity is the amount of computation performed per quantity of data moved across a specified boundary. Low intensity can indicate that transfers limit progress; higher intensity can shift the limit toward arithmetic capacity. The value depends on the operation, input, representation, and memory boundary being measured.

The diffusion-language-model record uses this idea to organize execution stages. Diffusion-style generation has its own sequence of iterative computation. So a scheduling improvement must be evaluated on the actual model procedure. The description does not establish stage definitions, output quality, timing, or memory results. [Recorded evidence](../observed-subthemes/llm-systems-and-runtime.md#paper-dac-2026-research2169)

Arithmetic intensity is a ratio. It is the number of arithmetic operations performed divided by the bytes moved across a named memory boundary. The boundary matters. Operations per byte moved from high-bandwidth memory to a compute unit is a different quantity. It is not the same as operations per byte moved from host memory to an accelerator. It is also not the same as operations per byte moved from storage into host memory. A runtime can improve one ratio while leaving the actual bottleneck unchanged.

Diffusion language models generate a result through repeated refinement steps. Each step may read a current token or latent representation and apply model layers. It may update an intermediate state, and decide how much uncertainty remains. The cost and data reuse can change across early and late steps and sequence lengths. They can also change across batch sizes, denoising iterations, and model configurations. A framework that chooses different execution or scheduling policies by arithmetic intensity must define the stage and its operation count. It must also define its byte count, the memory boundary, and the policy transition condition.

Operation counts also require a definition. A multiply-add may count as one operation or two. Sparse operations, attention, routing, normalization, sampling, communication and control work may be included or excluded. Byte counts must state whether a value is counted once per transfer, once per request, or once per cache level. They must also state whether reads, writes, metadata, intermediate materialization and recomputation are included. Without those conventions, arithmetic intensity cannot be compared across stages or systems.

The ratio is a diagnostic, not a performance result. Low intensity may indicate that data movement limits progress. Latency can also be limited by synchronization, kernel launch, network communication or memory contention. It can also be limited by insufficient parallelism, serial decoding or an irregular access pattern. High intensity does not guarantee that a processor reaches its peak arithmetic rate. Measure achieved operations per second, bandwidth, utilization, queueing, synchronization, memory traffic, latency and energy in addition to the modeled ratio.

Stage orchestration can introduce transition costs. Moving a stage between devices may require copying weights or activations or changing precision. It may require rebuilding a kernel plan, synchronizing workers or waiting for a queue. If the policy changes frequently, the decision and movement overhead can exceed the saved compute time. Report steady-state and transition costs separately. Also test workloads whose stage characteristics change during one request rather than only using a fixed average.

The baseline must preserve the generation task. Compare against standard diffusion decoding using the same model and number of refinement steps. Also use the same input/output lengths, numerical representation, batch/concurrency, sampling procedure and quality target. The autoregressive comparison needs its own model, token budget, stopping rule and quality criterion. A difference in generation procedure is not a pure runtime improvement. Report time to first useful output, total response latency, tokens or sequences per second, quality, memory, energy and variance.

Generalization requires multiple models and sequences. Arithmetic intensity changes with hidden size, sequence length, attention pattern, vocabulary, batch size, number of refinement steps and hardware. A stage boundary tuned for one model or sequence distribution may be wrong for another. Evaluate short and long sequences, low and high concurrency, changing batch sizes, cache states, memory pressure and device configurations. The captured description does not provide these conditions or numerical results.

The evidence supports using arithmetic intensity to organize stage-aware scheduling for diffusion language models. It does not establish the stage definitions, quality preservation, latency, throughput or memory. It also does not establish the energy, transition overhead, or model-diverse acceleration needed to claim a general acceleration framework.

## What the comparison must hold constant

Specify the model, input and output lengths, numerical representation, batch or concurrency settings, hardware, and output-quality requirement. For training, report progress toward the same quality target. For inference, report complete response behavior and useful output rate. For recovery, report the preserved state and resumed execution.

Include preparation, transfers, allocation, coordination, and failures relevant to the proposed method. Measure where time and memory are spent before and after the change. This establishes whether the runtime removed a cost, overlapped independent work, or merely moved the cost outside the reported measurement.

## Compare the results carefully

First identify the inputs and required output quality. Then identify the limited resource: time, memory, communication, energy, circuit area, or correctness coverage. Ask which part of the method reduces that cost and which new cost it adds. Compare numbers only when the experiments hold these conditions sufficiently similar.

A conference description may explain the proposal while omitting the full experiment. An author preprint link may have been coded from its abstract. The source classification does not by itself establish that every table was read. Missing locations remain visible below.

## Complete captured evidence

These are evidence records, not substitutes for the explanations above. Each record preserves its problem, proposed method, measurements, comparison conditions, and source limits. A populated record does not establish that its mechanism has been fully explained or independently verified.

<span id="paper-dac-2026-research1286"></span>

### An Efficient Heterogeneous Co-Design for Fine-Tuning on a Single GPU

DAC 2026 · Record: `dac-2026-research1286`

[Read the step-by-step explanation](#explanation-dac-2026-research1286)

**Updated source-backed reading card**

Reviewed 2026-09-08. Deepens the existing heterogeneous fine-tuning treatment into a paper-level reading; separates model/gradient/optimizer memory, offload and transfer boundaries, algorithmic changes, time-to-quality, baseline fairness and total resource accounting.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Fine-tuning large models on one GPU is constrained by memory capacity and throughput.

**Mechanism / artifact:**

Heterogeneous algorithm-hardware co-design for single-GPU fine-tuning; parameter state, optimizer/gradient placement, offload boundary, numerical transformations, scheduler and hardware path are unspecified.

**Workload — the work tested:**

Parameter-efficient or full-model fine-tuning; models, datasets, trainable parameter set, optimizer, quality target, steps/epochs, batch/microbatch, convergence rule and random seeds are unspecified.

**Hardware and manufacturing assumptions:**

Single GPU plus host or heterogeneous memory/compute; GPU model, CPU/host memory, storage, interconnect, bandwidth, overlap, precision, allocation, I/O, energy and failure/recovery assumptions are unspecified.

**Baseline — the comparison method:**

Standard single-GPU fine-tuning

Multi-GPU fine-tuning

Same model, trainable parameters, quality target, batch, precision, hardware/resource accounting, preparation/transfer boundary and time-to-quality condition are unspecified

**Reported measurements:**

Fine-tuning efficiency is claimed qualitatively; no time-to-quality, wall-clock time, memory, throughput, energy, accuracy/loss, transfer volume, CPU/storage cost, convergence or complete-run result is reported.

**Limits on the conclusion:**

A single GPU does not imply a single-resource system. Weights, gradients, activations and optimizer states may use host memory, storage or other compute, and transfer/synchronization can dominate the critical path.

Time-to-quality must use the same model, trainable parameter set, quality target, data, optimizer semantics and convergence rule. Faster token processing, lower GPU memory or parameter-efficient training alone does not establish an equal fine-tuning result.

No time-to-quality, memory, throughput, energy, or accuracy results are reported. Heterogeneous offload may add transfer overhead; the evidence supports a capacity-and-runtime co-design direction, not demonstrated single-GPU training efficiency across model families.

**Source and location**

Evidence tier: Primary captured official DAC description plus existing chapter level fine tuning discussion; no full paper extraction, reproduced runtime, model diverse benchmark or end to end resource accounting. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH1286)

DAC 2026 official description; existing chapter-level heterogeneous fine-tuning discussion; captured Problem, Mechanism / artifact, Workload, Hardware, Baseline, Measurements and Limits fields; no manuscript pages.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** standard single-GPU fine-tuning

multi-GPU fine-tuning

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH1286

**Hardware or process assumptions:** Single GPU plus host or heterogeneous memory/compute; GPU model and interconnect are unspecified.

**Limits:** No time-to-quality, memory, throughput, energy, or accuracy results are reported.

Heterogeneous offload may add transfer overhead.

Official description only; model-diverse training validation is required.

**Method or artifact:** Heterogeneous algorithm-hardware co-design for single-GPU fine-tuning.

**Metrics:** Fine-tuning efficiency is claimed qualitatively

**Problem:** Fine-tuning large models on one GPU is constrained by memory capacity and throughput.

**Workload or benchmark:** Parameter-efficient or full-model fine-tuning; models, datasets, and quality criteria are unspecified.

</details>

<span id="paper-dac-2026-research1414"></span>

### Expcheck: Dynamic Expert-Aware Checkpointing for Mixture-of-Experts Based Models

DAC 2026 · Record: `dac-2026-research1414`

[Read the step-by-step explanation](#explanation-dac-2026-research1414)

**Updated source-backed reading card**

Reviewed 2026-09-08. Deepens the existing Expcheck treatment into a paper-level reading; separates activity-aware state selection from exact recovery, defines MoE/router/optimizer dependencies and distributed consistency, and makes failure injection, storage, training overhead and baseline requirements explicit.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Mixture-of-experts training has uneven expert activity and expensive checkpoint storage or recovery.

**Mechanism / artifact:**

Checkpointing policy that adapts to expert activity; dependency rule, omitted-state reconstruction, optimizer/router/data state, consistency protocol, storage format and recovery semantics are unspecified.

**Workload — the work tested:**

MoE model training; expert count, router, dataset/activity distribution, optimizer, checkpoint interval, failure locations/timing, storage system, recovery target and repeated trials are unspecified.

**Hardware and manufacturing assumptions:**

Distributed accelerator training with checkpoint storage; worker synchronization, network, filesystem, storage bandwidth/replication, memory, failure detection and restart environment are unspecified.

**Baseline — the comparison method:**

Periodic full checkpointing

Expert-agnostic checkpointing

Same MoE model, expert count, optimizer, batch schedule, failure distribution, exact/approximate recovery criterion, storage and timing boundary are unspecified

**Reported measurements:**

Checkpoint efficiency is claimed qualitatively; no recovery point, saved-state volume, bytes written, normal-training overhead, storage cost, failure-recovery time, lost work, restart correctness or final-quality result is reported.

**Limits on the conclusion:**

Inactive expert state is not automatically irrelevant: future routing, optimizer state, router state, data position and distributed updates may depend on it. An activity-aware checkpoint must prove omitted values are unchanged or reconstructible at restart.

Exact recovery requires a consistent distributed state across parameters, optimizer, router, RNG, data and communication progress. Failure-injection tests must interrupt checkpointing and training at relevant points and compare resumed state and subsequent behavior with an uninterrupted reference.

No recovery point, storage volume, training overhead, or failure-recovery results are reported. Activity-aware state may complicate exact recovery; the evidence supports a checkpoint-policy direction, not demonstrated exact recovery or general MoE checkpoint efficiency.

**Source and location**

Evidence tier: Primary captured official DAC description plus existing chapter level expcheck discussion; no full paper extraction, reproduced checkpoint format, failure campaign or restart validation. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH1414)

DAC 2026 official description; existing chapter-level Expcheck discussion; captured Problem, Mechanism / artifact, Workload, Hardware, Baseline, Measurements and Limits fields; no manuscript pages.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** periodic full checkpointing

expert-agnostic checkpointing

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH1414

**Hardware or process assumptions:** Distributed accelerator training with checkpoint storage; network and filesystem assumptions are unspecified.

**Limits:** No recovery point, storage volume, training overhead, or failure-recovery results are reported.

Activity-aware state may complicate exact recovery.

Official description only; failure-injection validation is required.

**Method or artifact:** Checkpointing policy that adapts to expert activity.

**Metrics:** Checkpoint efficiency is claimed qualitatively

**Problem:** Mixture-of-experts training has uneven expert activity and expensive checkpoint storage or recovery.

**Workload or benchmark:** MoE model training; expert counts, failure model, and storage system are unspecified.

</details>

<span id="paper-dac-2026-research2169"></span>

### Orchestrating Dual-Boundaries: An Arithmetic Intensity Inspired Acceleration Framework for Diffusion Language Models

DAC 2026 · Record: `dac-2026-research2169`

[Read the step-by-step explanation](#explanation-dac-2026-research2169)

**Updated source-backed reading card**

Reviewed 2026-09-08. Deepens the existing arithmetic-intensity treatment into a paper-level reading; defines operation/byte boundaries, diffusion-stage behavior, transition overhead, baseline fairness, achieved performance and model/sequence generalization requirements.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Diffusion language models have changing compute and memory bottlenecks across generation stages.

**Mechanism / artifact:**

Acceleration framework orchestrating arithmetic-intensity-driven stage boundaries; operation/byte definitions, memory boundary, stage policy, transition mechanism and hardware mapping are unspecified.

**Workload — the work tested:**

Diffusion language-model inference; models, refinement steps, input/output lengths, batch/concurrency, sampling procedure, quality target, stage definitions and workload distribution are unspecified.

**Hardware and manufacturing assumptions:**

AI accelerator or heterogeneous inference system; processor, memory hierarchy, interconnect, bandwidth, cache, synchronization, kernel/runtime, precision and energy measurement boundary are unspecified.

**Baseline — the comparison method:**

Standard diffusion decoding

Autoregressive language-model serving

Same model/procedure, steps, token or sequence budget, quality target, batch/concurrency, precision, transition/preparation and end-to-end timing boundaries are unspecified

**Reported measurements:**

Diffusion-model efficiency is claimed qualitatively; no quality, latency, throughput, memory, energy, stage-boundary, transition, achieved-arithmetic or model-diverse result is reported.

**Limits on the conclusion:**

Arithmetic intensity is operations per bytes moved across a specified boundary, not a universal speed score. Operation counting, byte counting, cache level, reads/writes, metadata, recomputation and communication must be defined before stages can be compared.

Stage policy can incur transfer, synchronization, kernel, precision and planning costs. Low intensity does not prove bandwidth limitation and high intensity does not prove peak compute; report achieved performance, latency, bandwidth, queueing, memory traffic and energy.

No quality, latency, throughput, memory, energy, or stage-boundary results are reported. Arithmetic intensity may vary by model and sequence; the evidence supports a stage-aware scheduling direction, not demonstrated model-diverse acceleration.

**Source and location**

Evidence tier: Primary captured official DAC description plus existing chapter level arithmetic intensity discussion; no full paper extraction, reproduced scheduler, stage measurements or model diverse validation. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH2169)

DAC 2026 official description; existing chapter-level arithmetic-intensity discussion; captured Problem, Mechanism / artifact, Workload, Hardware, Baseline, Measurements and Limits fields; no manuscript pages.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** standard diffusion decoding

autoregressive language-model serving

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH2169

**Hardware or process assumptions:** AI accelerator or heterogeneous inference system; memory and interconnect assumptions are unspecified.

**Limits:** No quality, latency, throughput, memory, energy, or stage-boundary results are reported.

Arithmetic intensity may vary by model and sequence.

Official description only; model-diverse validation is required.

**Method or artifact:** Acceleration framework orchestrating arithmetic-intensity-driven stage boundaries.

**Metrics:** Diffusion-model efficiency is claimed qualitatively

**Problem:** Diffusion language models have changing compute and memory bottlenecks across generation stages.

**Workload or benchmark:** Diffusion language-model inference; models, steps, quality, and hardware are unspecified.

</details>

<span id="paper-dac-2026-research2300"></span>

### Hero: Adaptive Orchestration of Retrieval-Augmented Generation on Heterogeneous Mobile SoC

DAC 2026 · Record: `dac-2026-research2300`

[Read the step-by-step explanation](#explanation-dac-2026-research2300)

**Updated source-backed reading card**

Reviewed 2026-09-08. Deepens the existing Hero treatment into a paper-level reading; separates retrieval quality, generation quality, adaptive placement, CPU/GPU/NPU transfer, local/cloud privacy and mobile thermal/energy behavior, and makes workload-diverse validation explicit.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Mobile RAG systems must coordinate retrieval and generation across heterogeneous compute and memory under tight energy budgets.

**Mechanism / artifact:**

Adaptive RAG orchestration across a heterogeneous mobile SoC; retrieval/generation placement, policy signals, decision cost, transfer path, local/cloud boundary and adaptation rule are unspecified.

**Workload — the work tested:**

Retrieval-augmented generation queries; models, indexes, languages/topics, query distribution, candidate/context lengths, output quality, cache state, network state, devices and workload split are unspecified.

**Hardware and manufacturing assumptions:**

Mobile CPU/GPU/NPU and memory hierarchy; SoC/device, thermal and battery conditions, shared memory, accelerators, network, model precision, OS scheduling and privacy assumptions are unspecified.

**Baseline — the comparison method:**

Static RAG placement

Cloud RAG

Fixed heterogeneous placement, same index/retriever/generator/query/output quality/context/precision, network, thermal, privacy and end-to-end timing boundary are unspecified

**Reported measurements:**

Mobile RAG efficiency is claimed qualitatively; no retrieval quality, answer quality, grounding, latency, throughput, energy, memory, thermal, throttling, tail latency, policy error or workload-diverse result is reported.

**Limits on the conclusion:**

RAG has separate retrieval and generation quality requirements. Faster retrieval or generation does not establish answer correctness, grounding or hallucination behavior, and adaptive placement can trade quality for latency or energy.

CPU/GPU/NPU and local/cloud movement adds transfer, conversion, synchronization, network, privacy, battery and thermal costs. The policy state, decision overhead, query distribution and sustained mobile conditions must be measured.

No answer quality, latency, energy, memory, thermal, or workload results are reported. Adaptive choices may depend on query distribution; the evidence supports a mobile RAG orchestration direction, not demonstrated quality-preserving orchestration across devices and workloads.

**Source and location**

Evidence tier: Primary captured official DAC description plus existing chapter level hero discussion; no full paper extraction, reproduced policy, device/workload matrix or sustained thermal validation. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH2300)

DAC 2026 official description; existing chapter-level Hero/RAG discussion; captured Problem, Mechanism / artifact, Workload, Hardware, Baseline, Measurements and Limits fields; no manuscript pages.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** static RAG placement

cloud RAG

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH2300

**Hardware or process assumptions:** Mobile CPU/GPU/NPU and memory hierarchy; thermal and battery assumptions are unspecified.

**Limits:** No answer quality, latency, energy, memory, thermal, or workload results are reported.

Adaptive choices may depend on query distribution.

Official description only; device and workload-diverse validation is required.

**Method or artifact:** Adaptive RAG orchestration across a heterogeneous mobile SoC.

**Metrics:** Mobile RAG efficiency is claimed qualitatively

**Problem:** Mobile RAG systems must coordinate retrieval and generation across heterogeneous compute and memory under tight energy budgets.

**Workload or benchmark:** Retrieval-augmented generation queries; models, indexes, devices, and quality metrics are unspecified.

</details>

<span id="paper-dac-2026-research235"></span>

### Sandwich: Joint Configuration Search and Hot-Switching for Efficient CPU LLM Serving

DAC 2026 · Record: `dac-2026-research235`

[Read the step-by-step explanation](#explanation-dac-2026-research235)

**Updated source-backed reading card**

Reviewed 2026-09-08. Deepens the existing Sandwich treatment into a paper-level reading; separates offline configuration search from runtime hot-switching and makes switch cost, cache disruption, SLO/tail latency, exploration, workload drift and CPU resource accounting explicit.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

CPU LLM services need to adapt configurations as workload and latency demand change.

**Mechanism / artifact:**

Joint configuration search and runtime hot-switching for CPU serving; configuration dimensions, search source, switch protocol, state/cache effects, policy trigger and oscillation control are unspecified.

**Workload — the work tested:**

CPU LLM serving workloads; models, request arrival/prompt/output lengths, concurrency, SLOs, quality, CPU platform, thermal/power states, workload traces and transitions are unspecified.

**Hardware and manufacturing assumptions:**

Multi-configuration CPU inference runtime; cores/threads, affinity, caches, memory bandwidth, quantization, kernels, frequency, KV cache, OS scheduling and switch implementation are unspecified.

**Baseline — the comparison method:**

Static serving configuration

Offline tuning

Best fixed per-workload configuration, same model/quality, warm-up/cache state, CPU/thread/memory/frequency budget, request mix and end-to-end timing boundary are unspecified

**Reported measurements:**

Serving efficiency is claimed qualitatively; no latency, throughput, quality, switch time, energy, SLO attainment, tail latency, search cost, switch frequency, cache warm-up or workload-transition result is reported.

**Limits on the conclusion:**

Offline configuration search and runtime hot-switching are distinct. A switch can drain requests, disrupt caches/KV state, rebuild kernels, change thread placement or create queue growth; steady-state speed does not establish safe service behavior.

Serving evaluation must report TTFT, inter-token/total latency, p95/p99, deadline violations, throughput, quality, switch duration, warm-up, oscillation, exploration cost and changing workload conditions on held-out traces.

No latency, throughput, quality, switch time, energy, or workload results are reported. Switching may disrupt cache state and tail latency; the evidence supports an adaptive CPU-serving direction, not demonstrated SLO-safe hot-switching across models and workload changes.

**Source and location**

Evidence tier: Primary captured official DAC description plus existing chapter level sandwich discussion; no full paper extraction, reproduced search policy, switch trace or model/workload diverse slo validation. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH235)

DAC 2026 official description; existing chapter-level Sandwich discussion; captured Problem, Mechanism / artifact, Workload, Hardware, Baseline, Measurements and Limits fields; no manuscript pages.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** static serving configuration

offline tuning

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH235

**Hardware or process assumptions:** Multi-configuration CPU inference runtime; memory and thread assumptions are unspecified.

**Limits:** No latency, throughput, quality, switch time, energy, or workload results are reported.

Switching may disrupt cache state and tail latency.

Official description only; SLO and model-diverse validation is required.

**Method or artifact:** Joint configuration search and runtime hot-switching for CPU serving.

**Metrics:** Serving efficiency is claimed qualitatively

**Problem:** CPU LLM services need to adapt configurations as workload and latency demand change.

**Workload or benchmark:** CPU LLM serving workloads; models, requests, SLOs, and CPU platform are unspecified.

</details>

<span id="paper-dac-2026-research256"></span>

### PREBA: A Hardware/software Co-Design for Multi-Instance GPU Based AI Inference Servers

DAC 2026 · Record: `dac-2026-research256`

[Read the step-by-step explanation](#explanation-dac-2026-research256)

**Updated source-backed reading card**

Reviewed 2026-09-08. Deepens the existing PREBA treatment into a paper-level reading; separates hardware/software co-design from ordinary multi-instance scheduling and makes partitioning, tenant interference, memory pressure, QoS, fairness, isolation, energy, workload diversity and component ablations explicit.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Multi-instance GPU inference servers must share one physical GPU across tenants while meeting per-tenant latency, throughput and resource objectives.

**Mechanism / artifact:**

Hardware/software co-design for multi-instance GPU inference serving; partition mechanism, shared-resource controls, scheduler, memory policy, admission/reconfiguration path and hardware-generation boundary are unspecified.

**Workload — the work tested:**

Multi-tenant AI inference; models, model sizes, input/output lengths, arrival rates, concurrency, burst patterns, tenant priorities, memory footprints, quality targets, GPU generation and workload splits are unspecified.

**Hardware and manufacturing assumptions:**

One physical multi-instance GPU with shared compute, cache, memory bandwidth/capacity, copy engines, power, thermal, driver and scheduling resources; partition sizes, interconnect, host resources, driver/runtime and isolation mechanism are unspecified.

**Baseline — the comparison method:**

One instance per GPU

Conventional multi-instance GPU partitioning

Default multi-instance scheduling

Same physical GPU, driver, models, precision, request traces, tenant priorities, memory/power limits, warm-up/cache state, quality and end-to-end timing boundary are unspecified

**Reported measurements:**

Server efficiency is claimed qualitatively; no per-tenant or aggregate latency, TTFT, inter-token latency, throughput, p95/p99, SLO violations, fairness, isolation, memory occupancy, energy, power, thermal, reconfiguration, migration or workload-diverse result is reported.

**Limits on the conclusion:**

Logical instance separation does not establish performance isolation: tenants can contend for execution units, caches, memory bandwidth/capacity, copy engines, power, thermal headroom and queues. The design must state fixed versus borrowed resources and measure cross-tenant slowdown and tail behavior.

QoS requires per-tenant objectives, admission behavior, memory/KV-cache accounting, scheduling and reconfiguration cost. Aggregate throughput can improve while one tenant is starved or tail latency violates its service objective.

No tail latency, throughput, fairness, energy, isolation, memory or tenant results are reported. The evidence supports a multi-tenant GPU serving direction, not demonstrated QoS-safe, fair or portable inference-server efficiency.

**Source and location**

Evidence tier: Primary captured official DAC description plus existing chapter level preba discussion; no full paper extraction, reproduced partition/scheduling design or multi tenant qos validation. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH256)

DAC 2026 official description; existing chapter-level PREBA discussion; captured Problem, Mechanism / artifact, Workload, Hardware, Baseline, Measurements and Limits fields; no manuscript pages.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** single-tenant GPU

default multi-instance scheduling

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH256

**Hardware or process assumptions:** Multi-instance GPU with shared memory and scheduling; isolation and interconnect assumptions are unspecified.

**Limits:** No tail latency, throughput, fairness, energy, isolation, or tenant results are reported.

Co-design may be GPU-generation specific.

Official description only; multi-tenant validation is required.

**Method or artifact:** Hardware-software co-design for multi-instance GPU inference serving.

**Metrics:** Server efficiency is claimed qualitatively

**Problem:** Multi-instance GPU inference must share resources while meeting latency and throughput targets.

**Workload or benchmark:** AI inference services; models, tenant mixes, SLOs, and GPU partitioning are unspecified.

</details>

<span id="paper-dac-2026-research2620"></span>

### Deinfer: Efficient Parallel Inferencing for Decomposed Large Language Models

DAC 2026 · Record: `dac-2026-research2620`

[Read the step-by-step explanation](#explanation-dac-2026-research2620)

**Updated source-backed reading card**

Reviewed 2026-09-08. Deepens the existing DeInfer treatment into a paper-level reading; makes decomposition choice, dependency graph, communication boundaries, autoregressive prefill/decode behavior, optimization compatibility, quality preservation, scaling and small-request overhead explicit.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Decomposed LLMs can expose parallel subcomputations but incur dependency, scheduling, communication and synchronization overhead during inference.

**Mechanism / artifact:**

Parallel inference system for decomposed LLMs with multiple performance optimizations; decomposition type, graph partition, placement, scheduler, communication path and optimization composition are unspecified.

**Workload — the work tested:**

Decomposed LLM inference; models, decomposition, prompt/output lengths, prefill/decode split, batch/concurrency, decoding rule, quality criterion, device count/topology and scaling conditions are unspecified.

**Hardware and manufacturing assumptions:**

Multi-device or heterogeneous inference system; device types, interconnect, host-memory path, bandwidth/latency, memory hierarchy, precision, runtime, synchronization and energy boundary are unspecified.

**Baseline — the comparison method:**

Monolithic LLM inference

Sequential execution of the same decomposition

Standard distributed/tensor/pipeline parallel inference where applicable

Same model, decomposition, precision, prompt/output lengths, decoding, batch/concurrency, devices, interconnect, warm-up/cache state and end-to-end timing boundary are unspecified

**Reported measurements:**

Parallel inference efficiency is claimed qualitatively; no model quality, TTFT, inter-token or total latency, throughput, tail latency, communication volume/time, synchronization, scaling efficiency, utilization, memory, energy or cost result is reported.

**Limits on the conclusion:**

Decomposition exposes parallel work only when dependencies permit overlap. Activation, weight, KV-cache and control traffic, synchronization, scheduling and host copies can dominate, especially for one-token-at-a-time decode and small requests.

Compatibility with quantization, batching, fusion, caching or speculative decoding must preserve the dependency graph, numerical behavior and model-quality target; a faster result with changed precision or decoding is not a controlled systems comparison.

No quality, latency, throughput, communication, energy or scaling results are reported. Decomposition overhead may dominate small requests; the evidence supports a distributed LLM inference-system direction, not demonstrated efficient and quality-preserving parallel inference across model sizes, request regimes and hardware topologies.

**Source and location**

Evidence tier: Primary captured official DAC description plus existing chapter level deinfer discussion; no full paper extraction, reproduced decomposition graph, communication trace or model/topology diverse validation. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH2620)

DAC 2026 official description; existing chapter-level DeInfer discussion; captured Problem, Mechanism / artifact, Workload, Hardware, Baseline, Measurements and Limits fields; no manuscript pages.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** monolithic LLM inference

sequential decomposed inference

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH2620

**Hardware or process assumptions:** Multi-device or heterogeneous inference system; interconnect and memory assumptions are unspecified.

**Limits:** No quality, latency, throughput, communication, energy, or scaling results are reported.

Decomposition overhead may dominate for small requests.

Official description only; model and system validation is required.

**Method or artifact:** Parallel inference method for decomposed language models.

**Metrics:** Parallel inference efficiency is claimed qualitatively

**Problem:** Decomposed LLMs can expose parallel subcomputations but incur scheduling and communication overhead.

**Workload or benchmark:** Decomposed LLM inference; models, decomposition, devices, and quality targets are unspecified.

</details>

<span id="paper-dac-2026-research292"></span>

### Throughput-Oriented Speculative Decoding via Intra-Device Parallelism

DAC 2026 · Record: `dac-2026-research292`

[Read the step-by-step explanation](#explanation-dac-2026-research292)

**Updated source-backed reading card**

Reviewed 2026-09-08. Deepens the existing SmoothSpec treatment into a paper-level reading; explains speculative decoding accounting, draft acceptance, asymmetric intra-device allocation, controller behavior, quality preservation, latency/tail metrics, baselines and device-specific limits.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Speculative decoding can leave intra-device compute underused while draft and target models compete for shared accelerator resources.

**Mechanism / artifact:**

Intra-device speculative-decoding schedule that dynamically adjusts draft parameters and the resource-allocation ratio between draft and target models; allocation unit, control signal, update interval and reconfiguration mechanism are unspecified.

**Workload — the work tested:**

LLM generation on a single-node serving system; target/draft models, prompt/output lengths, acceptance distribution, batch/concurrency, decoding rule, workload transitions and model/device coverage are unspecified.

**Hardware and manufacturing assumptions:**

Single-device accelerator with shared compute, memory, cache, queues, power and thermal resources; device generation, parallelism configuration, precision, clock/power state, runtime and memory/KV-cache assumptions are unspecified.

**Baseline — the comparison method:**

Autoregressive decoding

Standard speculative decoding

Fixed draft and resource split

Same target/draft models, decoding rule, precision, prompts, output lengths, batch/concurrency, device, warm-up/cache state, power state and end-to-end timing boundary are unspecified

**Reported measurements:**

Generation throughput is claimed qualitatively; no acceptance rate, accepted tokens, target/draft work, TTFT, inter-token or total latency, p95/p99, memory, energy, utilization, reconfiguration cost, model quality or workload-transition result is reported.

**Limits on the conclusion:**

Speculative decoding trades draft cost and target verification against accepted useful tokens. Acceptance rate alone is insufficient; proposal length, accepted-prefix distribution, target evaluations, synchronization and end-to-end time must be reported.

Asymmetric intra-device allocation can contend for compute, memory, cache, queues, power and thermal headroom. Dynamic draft parameters and allocation ratio need a defined control signal, decision cost, hysteresis and ablations to show which mechanism creates the gain.

No acceptance rate, latency, throughput, memory, energy or model results are reported. Parallelism may be device-generation specific; the evidence supports adaptive intra-device speculative decoding, not demonstrated quality-preserving throughput or tail-latency improvement across model pairs and serving workloads.

**Source and location**

Evidence tier: Primary captured official DAC description plus existing chapter level speculative decoding discussion; no full paper extraction, reproduced controller, acceptance trace or model/device diverse validation. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH292)

DAC 2026 official description; existing chapter-level SmoothSpec discussion; captured Problem, Mechanism / artifact, Workload, Hardware, Baseline, Measurements and Limits fields; no manuscript pages.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** autoregressive decoding

standard speculative decoding

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH292

**Hardware or process assumptions:** Single-device accelerator with parallel compute and memory; scheduling assumptions are unspecified.

**Limits:** No acceptance rate, latency, throughput, memory, energy, or model results are reported.

Parallelism may be device-generation specific.

Official description only; model and hardware validation is required.

**Method or artifact:** Intra-device parallel speculative-decoding schedule.

**Metrics:** Generation throughput is claimed qualitatively

**Problem:** Speculative decoding can leave intra-device compute underutilized during draft and verification phases.

**Workload or benchmark:** LLM generation; models, draft strategy, acceptance rates, and device are unspecified.

</details>

<span id="paper-dac-2026-research538"></span>

### Amoeba: Runtime Tensor Parallel Transformation for LLM Inference Services

DAC 2026 · Record: `dac-2026-research538`

[Read the step-by-step explanation](#explanation-dac-2026-research538)

**Updated source-backed reading card**

Reviewed 2026-09-08. Deepens the existing Amoeba treatment into a paper-level reading; defines tensor-parallel state and KV-cache migration, transformation protocol, runtime policy, SLO/tail behavior, comparison fairness, resource accounting and the bounded meaning of the reported throughput range.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Changing LLM request context lengths make a fixed tensor-parallel layout inefficient: long contexts need KV-cache capacity while short contexts benefit from lower parallelism and higher concurrency.

**Mechanism / artifact:**

Runtime transformation of tensor parallelism for running LLM inference services; transformation protocol, state migration, tensor/KV-cache layout, trigger policy, synchronization and rollback behavior are unspecified.

**Workload — the work tested:**

LLM inference requests with variable context lengths; models, prompt/output lengths, concurrency, arrival patterns, KV-cache state, SLOs, real-world traces and device/model diversity are unspecified.

**Hardware and manufacturing assumptions:**

Multi-device accelerator serving with tensor-parallel communication; devices, interconnect, bandwidth/latency, memory capacity, host path, precision, allocator, runtime, power state and migration support are unspecified.

**Baseline — the comparison method:**

Static tensor parallelism

Data-parallel serving

Routing new requests without transforming running instances

Same model, precision, devices, interconnect, request traces, context/output lengths, concurrency, warm-up/cache state, quality target and end-to-end timing boundary are unspecified

**Reported measurements:**

Runtime serving efficiency is claimed qualitatively; the description states a 1.75×–6.57× throughput range, but no migration time, latency, TTFT, inter-token latency, tail/SLO result, KV-cache movement, quality, energy, memory or model/device-diverse condition is reported.

**Limits on the conclusion:**

A tensor-parallel transformation must preserve active model/request state while changing device groups and layouts. Weights, activations, KV cache, scheduler metadata and allocator state may move or be duplicated; migration bytes, synchronization, temporary capacity and progress loss must be measured.

Long-context capacity and short-context concurrency are distinct objectives. Aggregate throughput can improve while migration creates tail latency, queueing or SLO violations; report per-request TTFT, inter-token/total latency and p95/p99 during workload transitions.

The captured description reports 1.75×–6.57× throughput over state-of-the-art solutions but gives no migration time, latency, KV-cache movement, quality, energy or SLO conditions. The evidence supports adaptive parallelism as a serving direction, not demonstrated SLO-safe reconfiguration or general throughput improvement.

**Source and location**

Evidence tier: Primary captured official DAC description plus existing chapter level amoeba discussion; no full paper extraction, reproduced migration protocol, kv cache trace or model/device diverse slo validation. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH538)

DAC 2026 official description; existing chapter-level Amoeba discussion; captured Problem, Mechanism / artifact, Workload, Hardware, Baseline, Measurements and Limits fields; no manuscript pages.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** static tensor parallelism

data parallel serving

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH538

**Hardware or process assumptions:** Multi-device accelerator serving; interconnect and state-migration assumptions are unspecified.

**Limits:** No latency, throughput, migration time, quality, energy, or workload results are reported.

Transformation may disrupt cached state.

Official description only; SLO and model-diverse validation is required.

**Method or artifact:** Runtime transformation of tensor parallelism for inference services.

**Metrics:** Runtime serving efficiency is claimed qualitatively

**Problem:** LLM serving demand changes over time, making fixed tensor-parallel layouts inefficient.

**Workload or benchmark:** LLM inference requests; models, devices, SLOs, and reconfiguration costs are unspecified.

</details>

<span id="paper-dac-2026-research628"></span>

### Faster-MoA: Low-Latency Tree-Structured MoA Serving with Early Exit and Agent-Aware Prefill-Decode Overlap

DAC 2026 · Record: `dac-2026-research628`

[Read the step-by-step explanation](#explanation-dac-2026-research628)

**Updated source-backed reading card**

Reviewed 2026-09-08. Deepens the existing Faster-MoA treatment into a paper-level reading; separates tree topology, early-exit quality decisions and prefill/decode overlap, and makes dependency correctness, task-level quality, tail latency, ablations and the bounded reported claims explicit.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Mixture-of-Agents serving incurs agent-to-agent communication, routing and prefill/decode latency under an all-to-all connectivity pattern.

**Mechanism / artifact:**

Early-exit and overlap-aware MoA serving runtime with hierarchical tree connectivity, dynamic agent early exit using semantic similarity/confidence, and dependency-aware incremental prefill/decode overlap; graph, thresholds, scheduler and synchronization are unspecified.

**Workload — the work tested:**

MoA agent workloads; agent models, tasks, prompts, output budgets, quality metrics, exit distributions, concurrency, hardware, interconnect and workload diversity are unspecified.

**Hardware and manufacturing assumptions:**

Multi-device or heterogeneous LLM serving system; devices, accelerator/memory, interconnect, batching, model placement, precision, runtime, power and energy boundary are unspecified.

**Baseline — the comparison method:**

All-to-all MoA

Sequential agent execution

Tree-only, early-exit-only and overlap-only ablations

Standard/single-model serving where quality permits

Same agents, prompts, tasks, decoding, output budget, hardware, interconnect, warm-up, concurrency and end-to-end timing boundary are unspecified

**Reported measurements:**

MoA serving latency is claimed qualitatively; the captured description claims up to 90% lower end-to-end latency and approximately ±1% accuracy variation, but no task-level quality distribution, exit rate, communication, throughput, energy, TTFT, p95/p99, memory or hardware condition is reported.

**Limits on the conclusion:**

A tree changes the MoA dependency graph and may add serial depth or amplify an early error. Early exit removes agents and evidence; semantic similarity or confidence does not establish correctness, calibration, factuality or safety. Both need task-level quality and exit-case analysis.

Prefill/decode overlap is valid only when producer-consumer dependencies and KV-cache updates remain consistent. Measure synchronization, discarded work, cache state, queueing, communication, agent idle time and the final-answer timing boundary.

The captured description claims up to 90% lower latency with approximately ±1% accuracy variation, but gives no task-level quality, exit, communication, throughput, energy or tail results. The evidence supports a conditional low-latency MoA direction, not demonstrated quality-preserving serving across tasks, models and workloads.

**Source and location**

Evidence tier: Primary captured official DAC description plus existing chapter level faster moa discussion; no full paper extraction, reproduced dependency graph, exit calibration, task level quality distribution or hardware diverse validation. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH628)

DAC 2026 official description; existing chapter-level Faster-MoA discussion; captured Problem, Mechanism / artifact, Workload, Hardware, Baseline, Measurements and Limits fields; no manuscript pages.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** sequential MoA serving

standard LLM serving

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH628

**Hardware or process assumptions:** Multi-device or heterogeneous inference system; interconnect and memory assumptions are unspecified.

**Limits:** No answer quality, latency, throughput, energy, communication, or model results are reported.

Early exit may alter agent consensus.

Official description only; task and system validation is required.

**Method or artifact:** Early-exit and overlap-aware MoA serving runtime.

**Metrics:** MoA serving latency is claimed qualitatively

**Problem:** Mixture-of-agents serving incurs tree traversal, agent routing, and prefill/decode latency.

**Workload or benchmark:** LLM or agent workloads; agents, models, acceptance criteria, and hardware are unspecified.

</details>

## What remains to establish

Resolve unspecified workloads, comparison methods, resource budgets, and source locations before generalizing a reported gain. Multiple papers in this selected sample permit comparison of mechanisms, but do not by themselves establish recurrence across years or a long-term trend.

[All subthemes](../expanded-taxonomy-v1.md) · [Research directions](../directions/README.md)
