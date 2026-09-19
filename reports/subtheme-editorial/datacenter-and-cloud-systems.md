## A service must finish useful work, not merely keep hardware busy

A cloud service receives requests, assigns resources, performs computation, and returns results. Requests differ in size and arrival time. When resources are occupied, new work waits. The time experienced by a user therefore includes queueing, data transfers, and scheduling decisions as well as arithmetic.

These five papers change different decisions: how memory is shared, which model handles a request, how many expert instances run, what frequency a GPU uses, and where cloud tasks execute. Their common problem is allocating finite resources under changing demand. Their reported improvements are not interchangeable.

A service-level objective, or SLO, defines a target such as a response-time limit for a specified fraction of requests. Throughput counts completed work per unit time. SLO attainment counts the fraction meeting the target. A system can improve one while worsening the other, especially when it serves more work in larger batches or changes which model produces the answers.

Three manuscripts were recovered for this article. sMoE remains description-backed; GREEN also has an author implementation repository, but no recovered full manuscript here. The findings below supersede conflicting omissions in the original captured cards. Full source-record reconciliation and independent reproduction remain open.

<span id="explanation-dac-2026-research1351"></span>

## eLLM: make activation memory and KV-cache memory share one physical pool

### The resource problem is separate logical lifetimes competing for the same bytes

During transformer inference, model weights remain mostly fixed, while two other objects change over time. Activations are temporary intermediate tensors used during a computation. The key–value (KV) cache stores attention keys and values from earlier tokens so later autoregressive steps do not recompute the entire prefix. Activation size depends strongly on the current phase and batch; KV-cache size grows with the retained sequence and request count. Their lifetimes and access patterns differ, but both consume GPU memory.

The serving system must therefore answer two different questions: which logical tensors are live, and which physical memory blocks back them at this moment. Traditional frameworks allocate activations through a static tensor interface. vLLM virtualizes the KV cache with page-like blocks, but keeps the activation and KV spaces separate. If activation capacity is idle while the KV pool is full, the idle bytes cannot immediately serve a new request. The paper calls this space-wise internal fragmentation. It is not fragmentation inside one allocator; it is unused capacity trapped behind two incompatible allocation abstractions.

The scale of the problem depends on the workload distribution. In the manuscript's example, increasing the maximum context of MTP-30B from 2K to 200K changes the reserved activation space from 0.3% to 30.8% of GPU memory, while the cited ShareGPT distribution has 99% of prompts within 2K tokens. During decoding, activation utilization can be about 1% because each step produces only a small number of tokens. A reservation sized for the maximum context can therefore remain mostly unused while the KV cache is the limiting resource.

### eTensor separates logical type from physical ownership

[eLLM](../observed-subthemes/datacenter-and-cloud-systems.md#paper-dac-2026-research1351) introduces eTensor, with two logical types: KV eTensor and activation eTensor. The types retain different policies because they have different behavior, but both can draw from a unified physical pool. A virtual address names a logical tensor range; a mapping table determines which physical chunks currently back that range. This decouples the tensor's logical lifetime from a permanent physical reservation.

KV eTensor reserves virtual address space for the maximum context of a request but allocates physical blocks only when the cache is written. This preserves sequential addressing while avoiding immediate allocation of the maximum. Activation eTensor uses variable-sized virtual segments because activation blocks are shorter-lived and accessed more frequently. Both types align virtual slots with physical-block granularity so a chunk can be reassigned without splitting it into incompatible units.

The allocator does not remove all mapping work. The KV pool uses best-fit selection among available mapped slots and triggers on-demand mapping when no suitable slot exists. The activation pool retains the framework's best-fit-with-coalescing policy. The system also keeps some mappings available for reuse instead of unmapping them immediately. These details matter because the benefit of sharing capacity can be lost if address translation, mapping, garbage collection, or synchronization dominates the saved allocation.

### Inflation and deflation transfer capacity inside the GPU

When a new KV allocation cannot fit, eLLM performs memory inflation. It identifies inactive activation eTensors, unmaps their physical chunks, transfers ownership of those chunks to the KV pool, and maps them into the requesting KV eTensor. Deflation reverses the ownership transfer when activation demand rises or KV capacity is no longer needed. The operation changes the mapping relation; it does not create additional GPU memory.

The useful case occurs at phase boundaries. Prefill can require substantial activation memory and produces KV data. Decode uses much smaller activation memory but retains the growing KV cache. A static split sized for both phases wastes capacity; inflation and deflation let the physical split follow the current phase. eLLM performs deflation lazily to avoid paying a transfer of ownership before the capacity is needed elsewhere.

### CPU overflow changes queueing and token-generation cost in opposite directions

GPU-internal sharing is insufficient when all GPU chunks are occupied. eLLM can proactively offload selected KV data to CPU memory during prefill and fetch it back when the request is scheduled for decoding. This can admit a request earlier and allow a larger decode batch. The paper argues that the transfer is linear in the cache size while prefill self-attention is quadratic in sequence length, and that layer-wise transformer execution can overlap transfers with computation in the tested LLaMA-3-8B case.

The overflow path has a direct cost: PCIe or interconnect traffic consumes bandwidth and can delay decoding. The paper therefore distinguishes time to first token (TTFT), which includes queueing and prefill, from time per output token (TPOT), which measures the pace of generation after output begins. More CPU buffering can reduce TTFT by admitting more prefill work while worsening TPOT if cache fetches compete with decode. A lower TTFT is not a general latency improvement unless TPOT and the request-level service objective are also preserved.

### The scheduler treats buffer size as a control variable

eLLM exposes a logical CPU-buffer size that can change within a fixed physical buffer. If TPOT violates its target repeatedly, the scheduler reduces the logical buffer to limit prefill admission and protect decoding. If TTFT violates its target, it increases the logical buffer to admit more work. A violation requires three breaches within a five-iteration scheduling window, and the default adjustment factor is two. This hysteresis avoids changing the policy after one noisy measurement, but it also makes the response dependent on the chosen window and factor.

The paper defines online SLOs as 25 times the uncontended TTFT and TPOT for the relevant workload. Goodput is the highest request rate at which at least 90% of requests meet the SLO. This is a service metric, not a raw throughput metric: a controller can increase token throughput while lowering goodput if it creates more deadline misses. The comparison must therefore keep the arrival process, input/output lengths, baseline contention and SLO construction fixed.

### What the evaluation measures

The version-2 implementation adds about 4,000 lines of C++ and Python to vLLM 0.5.5, changes KV allocation granularity from pages to physical chunks, uses GPU virtual-memory-management APIs for activation allocation, and overlaps speculative decoding pre-mapping and asynchronous unmapping. The testbed has eight NVIDIA A100 80 GB GPUs connected by NVLink, an Intel Xeon Platinum 8369B CPU, 1 TB RAM, PyTorch 2.4.0 and CUDA driver 12.4. The evaluated models are Llama3-8B-262K, Jamba and OPT-13B. Online requests use ShareGPT or fixed-length workloads with Poisson arrivals; offline requests are all available at the beginning.

Against vLLM and vLLM with chunked prefill, single-GPU Llama3-8B experiments report up to 295× and 140× lower TTFT in the plotted settings and up to 2.5× and 2.26× higher goodput. The large TTFT ratios reflect queueing conditions and the selected request rates; they are not a 295× improvement in every part of inference. In offline inference, the 128K-input/4K-output configuration reports up to 1.82× total throughput and 2.32× decode throughput. Total throughput includes prefill and decode, whereas decode throughput isolates the generation phase; the two numbers must not be substituted for each other.

The ablation exposes the cost of combining mechanisms. GPU-internal elasticity alone and GPU–CPU elasticity alone both reduce TTFT. Their combination can produce lower throughput than GPU-internal sharing alone because PCIe transfers do not always overlap decoding. The paper reports up to 1.5× throughput and 2.5× goodput from adaptive orchestration, while mapping work occupies 1–5% of online execution time. These results support a conditional systems tradeoff, not the claim that CPU overflow is always beneficial.

### What this establishes and what remains open

eLLM establishes, under its stated software, A100, model, traffic and SLO conditions, that a shared physical pool can reduce allocation waste and improve admission or batching when activation and KV demand peak at different times. It also shows why CPU overflow must be controlled by service targets: it can improve TTFT while adding transfer work to TPOT. It does not establish the same gains on other GPU generations, interconnects, allocators, model architectures, request distributions, context lengths or SLO definitions. A stronger deployment study would report full latency distributions, transfer bytes and overlap, allocator/mapping failures, warmup and thermal behavior, model-quality invariance, multi-tenant interference, and cost per accepted request. [Version-2 manuscript, Sections 1–4.6, PDF pages 1–7, Figures 5–8](https://arxiv.org/pdf/2506.15155v2#page=5)

<span id="explanation-dac-2026-research3129"></span>

## HW-Router: choose a model–GPU pair from current serving state

### Routing cost is a property of a query, model, device, and queue state

A multi-LLM service may keep several models available because different models answer different requests well. A router must choose both a model and the GPU instance hosting it. The choice has two outputs: expected response quality and expected serving cost. Model size and FLOPs provide a static cost estimate, but actual latency also depends on input length, output length, batching, KV-cache capacity, running requests, waiting requests, GPU type, and recent contention.

The same small model can therefore be a poor choice when its GPU is saturated, while a larger model on an idle GPU can finish sooner. This is not a contradiction in model speed. It is a change in the system state that determines how much work the model can receive and when that work begins.

[HW-Router](../observed-subthemes/datacenter-and-cloud-systems.md#paper-dac-2026-research3129) treats each model–GPU pair as a separate candidate. For a query `x`, it predicts quality `Q` and a cost `C`; the decision score is `(1 − λ)Q − λC`, subject to an SLO bound. The coefficient λ selects a point on the quality–latency tradeoff. A router that changes λ can produce different quality and latency results even when the serving system is unchanged.

### The monitor turns runtime state into routing features

The hardware monitor polls each model server every 200–300 ms and caches the results before a request arrives. It records active-request count, waiting-request count, KV-cache utilization, recent average time to first token (TTFT), and recent average time per output token (TPOT). These measurements describe different constraints. Active requests indicate ongoing computation; waiting requests indicate queue pressure; KV-cache utilization limits the batch and admission capacity; TTFT and TPOT summarize the recent effect of those conditions.

The polling interval creates a boundary: the router sees a recent snapshot, not the exact state at the instant the request is assigned. A burst can fill a queue between polls. The cached design avoids adding the monitor's polling work to each routing decision, but it cannot eliminate state staleness. A deployment claim therefore needs evaluation under changes faster than the monitoring interval as well as under stable load.

### The cost predictor estimates the whole response path

For each query and candidate pair, a two-layer neural network predicts TTFT, TPOT, and output-token count. Its inputs include query features, one-hot model/GPU identifiers, and the five runtime signals. The predicted cost is `TTFT + predicted_output_tokens × TPOT`. This adds queueing and generation to a single cost quantity, but it assumes that the predicted token count and average TPOT are useful summaries for the request.

The paper reports about 10 ms for the cost-predictor forward pass. Separately, the experimental section reports about 200 μs of additional routing latency over CARROT. These measurements have different boundaries and should not be combined into a claim that the full router costs only 200 μs. The 200 μs figure is an incremental comparison on the stated testbed; the predictor-forward-pass figure describes one internal operation.

Quality is predicted separately and treated as hardware-independent. The decision maker evaluates feasible pairs and rejects candidates whose predicted cost exceeds the SLO bound. This can improve latency only if the cost prediction reflects the current system and if the quality predictor remains calibrated. A model chosen for lower predicted latency is not equivalent to the original model if it produces a lower-quality answer.

### The evaluation uses a fixed two-GPU model pool

The manuscript evaluates one node with two NVIDIA H100 PCIe GPUs, each with 80 GB HBM, eight CPU cores and 64 GB system memory. Models run in vLLM, one process per GPU, with Prometheus metrics. The fixed placement is: Phi-3-mini and Qwen2.5-14B on H100-0; Qwen2.5-3B, Mistral-7B and Llama-3.1-8B on H100-1. The H100/V100 contrast motivates the problem, but the measured experiment does not use a mixed H100/V100 cluster.

The prompt set contains 8,425 examples: 6,000 MixInstruct prompts and 2,425 English LongBench prompts, split into 6,740 training and 1,685 evaluation examples. Short instructions create concurrency; LongBench supplies medium and long contexts that stress KV-cache and latency. An LLM judge, Qwen-3-Next-80B, assigns quality from 0.0 to 1.0 in 0.1 increments against golden answers. This is a judged quality proxy, not a universal correctness measurement.

Training exposes the predictor to Poisson, micro-burst and sustained-overload arrivals. Evaluation uses sustained overload with arrival rates swept from 15 to 21 requests per second. This makes queue-balancing differences visible, but it does not establish behavior for ordinary light load, arbitrary burst shapes, changing model placement, or a model pool not represented in training.

### SLO and load-balance metrics have specific meanings

TTFT SLO is fitted as a linear function of prompt length and multiplied by 1.2 slack. TPOT SLO is the 70th percentile of per-token latency in the training set. For a request with `p` input tokens and `d` output tokens, the request passes when measured latency is no greater than the fitted TTFT target plus `d` times the TPOT target. SLO attainment is the fraction of requests that pass.

The paper also measures average running requests and waiting requests per GPU. This separates work currently being processed from backlog. For two GPUs, its load-skew equation is the absolute difference between their average total queue lengths. Under that definition, a value near 13 means a difference of about 13 requests, not that one GPU processes 13 times as many requests. The manuscript's prose interprets the value as a multiplicative ratio, which conflicts with the displayed definition and should remain an evidence issue.

### Reported results and what drives them

At judged quality 0.62, the paper reports approximately 40 seconds for CARROT and IRT-Router versus 16 seconds for HW-Router. At quality 0.60, SLO attainment is approximately 97% for HW-Router, 51% for CARROT and 65% for IRT-Router. At quality 0.63, the corresponding values are 90%, 48% and 60%; at 0.65, HW-Router remains at 76% while both baselines are below 50%. These are points on the selected quality/SLO curves, not guarantees for all prompts or future traffic.

At arrival rates 15, 18 and 21, CARROT has 53–55% of its total queue waiting; IRT has 34–39%; HW-Router has 16–17%. The waiting fraction falls by roughly 3.1–3.4× in the paper's comparison. Table 4 reports load-skew values of approximately 12.9 for CARROT, 12.6–12.9 for IRT, and 1.7–2.1 for HW-Router under its absolute-difference definition. HW-Router's average total load is slightly higher, about 7.0–7.2 versus 6.3–6.5, which is consistent with keeping both GPUs active rather than concentrating requests on one. The table supports more even queue counts; it does not by itself prove equal GPU utilization, minimum energy, or model-quality equality.

### What this establishes and what remains open

The manuscript supports a bounded claim: on a fixed two-H100 model pool, with the specified prompts, judged quality, sustained-overload rates, monitoring interval, placement, and baselines, using runtime signals can improve the measured quality–latency frontier, SLO attainment, and queue balance over static-cost routers. It does not establish a hard deadline guarantee. Predictions can become stale, several requests can observe the same idle state, output length can be mispredicted, and an SLO trained from the same traffic may not transfer to another service.

Stronger evidence would hold out entire model/GPU placements, evaluate mixed GPU generations, report prediction error and stale-state effects, test fast bursts and low-load regimes, measure router and monitor cost end to end, and use independent quality judgments or task-specific correctness. [Version-1 manuscript, Sections 3–5, PDF pages 3–7, Tables 3–4](https://arxiv.org/pdf/2608.14575v1#page=4)

## sMoE: scale individual experts without ignoring the rest of the request

A mixture-of-experts model uses a learned selection rule to activate only some expert subnetworks for each token. Different requests can select different experts, and a popular expert can become overloaded while others are lightly used. Selective computation reduces arithmetic only if the system can manage the resulting storage and communication demands.

[sMoE](../observed-subthemes/datacenter-and-cloud-systems.md#paper-dac-2026-research734) represents experts and other model segments as a directed dependency graph. Its learned autoscaler uses graph features and layer-wise decisions to choose per-expert resources, replica counts, and concurrency. The official description reports 21.4–39.2% lower serving cost while meeting end-to-end P95 latency objectives.

<span id="explanation-dac-2026-research734"></span>

### sMoE: scaling one expert is useful only when the whole dependency graph can keep up

### What an MoE serving pipeline contains

A mixture-of-experts (MoE) model contains several expert subnetworks, but a routing decision activates only some experts for each token. Expert popularity is therefore uneven: a small number of experts can receive much more work than the rest, and the popular set can change with the request mix. A deployment that allocates equal resources to every expert can waste capacity while still leaving a hot expert as the bottleneck.

An inference request also passes through non-expert segments and layers. These stages create dependencies: a later expert cannot run until its input is produced, and the response cannot complete until all required stages finish. The service must scale experts without breaking the order, memory, communication and batching relationships between stages.

### What the DAG representation makes visible

sMoE represents the deployment as a directed acyclic graph (DAG) of experts and non-MoE segments. A node represents a computational segment; an edge represents a dependency or data path. The graph makes cross-layer structure explicit instead of treating each expert as an independent queue.

The autoscaler uses a DAG neural network (DAGNN) to propagate runtime features across the graph. Cross-layer propagation lets the representation include how congestion or resource changes in one stage affect downstream work. A layer-wise pointer network then selects actions for the experts in each layer. The stated actions jointly choose vertical resources, replica counts and concurrency.

These controls have different effects. Vertical scaling gives one instance more compute or memory resources. Replication creates more instances so requests can be distributed across them. Concurrency determines how many requests or token groups an instance handles at once. More of any one resource can increase utilization or service capacity, but can also increase memory pressure, queueing, cold starts, synchronization, or interference with another stage.

### Why serverless cost and latency are coupled

Serverless elasticity changes resources in response to demand and charges according to a provider-specific unit and duration. Scaling an expert can reduce queue time while adding instance startup, model loading, idle reservation or replica-churn cost. A cost model that omits those terms can favor an action that looks cheap in steady state but is expensive during a burst.

P95 latency means the 95th percentile of request latency. Meeting a P95 SLO does not mean every request meets the target, and it does not say how close the slowest five percent are to failure. The service also needs to define whether latency includes queueing, cold start, model loading, inter-stage transfer and the full end-to-end response.

### What the reported result establishes

The official description reports 21.4–39.2% lower serving cost than state-of-the-art solutions while meeting end-to-end P95 latency SLOs. The range is condition-dependent; the description does not identify the model, request traces, cloud price, SLO threshold, cold-start policy, replica churn, resource units or baseline tuning. It therefore supports a topology-aware elastic-scaling direction, not a provider-independent cost reduction.

The deep reinforcement-learning policy also depends on its training distribution and reward. If the reward does not charge for startup, migration, model loading, memory, network transfer or quality changes, the policy can move cost outside the reported objective. Generalization to a different expert-skew pattern or model graph must be measured rather than inferred from the graph representation.

### The evaluation that would establish cloud-serving value

Report expert popularity over time, model graph, request arrival and length distributions, cloud platform and price, resource units, cold-start and model-loading costs, replica lifetime, concurrency limits and SLO thresholds. Measure P50/P95/P99 end-to-end latency, queueing, throughput, cost per accepted request, resource utilization, memory/network traffic and quality. Compare vertical scaling, replication, concurrency-only and graph-aware policies under equal startup and billing assumptions, and test workload shifts that change which experts are hot.

The [sMoE](../observed-subthemes/datacenter-and-cloud-systems.md#paper-dac-2026-research734) record describes a DAGNN/pointer-network autoscaler that jointly selects expert resources, replicas and concurrency for serverless MoE inference. The detailed explanation above separates expert popularity from graph dependencies, scaling from replication and concurrency, steady-state capacity from serverless startup cost, and P95 SLO attainment from universal deadline satisfaction; this card is the compact evidence record.

The model suite, trace distribution, billing rules, startup costs, transfer costs, actual latency thresholds, and training expense are not supplied in the recovered description. This is not the separate expert-substitution paper with a similar SMoE name. Full manuscript conditions and page-backed comparisons remain missing. [Official DAC description](https://63dac.conference-program.com/presentation/?id=RESEARCH734&sess=sess124).

A directed dependency graph records which operations must finish before others can proceed. Scaling one expert does little for response time if a later required stage remains overloaded. Conversely, adding replicas to every stage can waste resources when only a small part of the graph is busy.

Vertical scaling changes the resources assigned to an instance; replication creates additional instances. Concurrency limits determine how many requests an instance handles together. These decisions interact: more concurrency may improve utilization but increase individual waiting time or memory pressure.

Serverless operation still uses servers. Its distinguishing resource and billing policies do not eliminate startup time or data loading. An expert replica that becomes available after a demand spike ends may incur cost without helping the requests that caused the spike. P95 latency means the 95th-percentile latency; it also leaves a slower fraction whose behavior should remain visible.

<span id="explanation-dac-2026-research976"></span>

## GreenLLM: choose frequency separately for prompt processing and token generation

### Power, energy, and service quality are different quantities

GPU power is the rate of energy use. Energy is the time integral of power. Lowering the clock can lower instantaneous power while extending execution long enough to consume the same or more energy. A valid energy result must therefore include the completed work, the time taken, and the requests that missed their latency target.

GreenLLM starts from a structural fact about autoregressive inference. Prefill processes the entire input prompt and largely determines time to first token (TTFT); its attention work grows approximately quadratically with prompt length. Decode generates one token at a time, has an unpredictable duration, and is commonly constrained by time between tokens (TBT). A frequency that is appropriate for compute-heavy prefill can be wasteful for decode, where KV-cache traffic can make the GPU memory-bound.

The paper measures a U-shaped energy-versus-frequency curve. At very low clocks, execution takes longer; at high clocks, power rises faster than latency improves. The minimum therefore depends on phase, load, prompt length, and the SLO deadline. A single governor that maximizes instantaneous throughput is not guaranteed to minimize energy for a service.

### The control path has three linked decisions

[GreenLLM](../observed-subthemes/datacenter-and-cloud-systems.md#paper-dac-2026-research976) first routes requests into prompt-length classes. Short and medium prompts use one prefill path, and long prompts use another. This reduces head-of-line blocking: a long prompt does not occupy the same queue position as many short prompts waiting for their first token. The separation changes queueing as well as frequency, so any energy comparison must distinguish energy saved by clock control from latency saved by queue partitioning.

For prefill, GreenLLM profiles latency and power as functions of SM frequency. It fits measured latency with a quadratic in prompt length, `t_ref ≈ aL² + bL + c`, where the quadratic term represents attention and the linear term represents projections and feed-forward work. It then scales the reference time by `f_ref/f` and chooses the lowest-energy frequency whose cumulative prefill busy time fits the SLO deadline. The energy model includes active power during busy time and idle power for the remaining interval; a frequency that misses the deadline is infeasible even if its active power is low.

For decode, a dual-loop controller measures tokens per second every 20 ms. A coarse loop selects a frequency band from a profiled TPS-to-frequency table. A fine loop changes the clock in 15 MHz steps with hysteresis and targets the 95th-percentile TBT. Hysteresis prevents a small measurement fluctuation from causing repeated up/down changes, but it also means the controller responds with a delay to sudden load or sequence-length changes.

### The measurements are device- and trace-specific

The version-1 manuscript profiles Qwen3-14B on a DGX-A100 system and evaluates Qwen3-14B and Qwen3-30B-MoE. NVML app clocks control SM frequency, memory clocks are fixed, and autoboost is disabled. The DGX node has eight A100-SXM4 40 GB GPUs, and the serving stack is identified as Dynamo 0.3.1. Trace replays use Alibaba traffic and downsampled Azure traffic. The paper also constructs microbenchmarks: prefill prompts vary from 256–1024 tokens, decode outputs from 256–1024 tokens, and frequency sweeps run from 210 MHz to 1410 MHz over stated TPS ranges.

The system profile reports an energy minimum near 0.95–1.05 GHz for many prefill loads and a lower decode knee near the point where KV-cache reads dominate. A practical Alibaba chat trace at 5 queries/second reports about 47% lower total inference energy at an approximately 0.75 GHz cap than the default performance governor. This is a measured trace result under fixed clock and workload conditions, not a universal frequency rule.

The prompt-length routing experiment raises SLO attainment from 89.9% to 96.4% in the stated setup. Table 3 reports Qwen3-14B chat energy savings declining from 27.52% at one request/second to 6.78% at ten. This decline is consistent with a controller having less slack as utilization rises, but it should not be generalized beyond the trace, model, arrival rate and energy boundary.

### The reported quality boundary needs to remain visible

The Azure_code5 trace has a first-token pass rate of 98.5% for the baseline and 94.2% for GreenLLM, a 4.3-percentage-point difference. That table entry does not sit cleanly beside the manuscript's blanket statement of less than 3.5% additional SLO violations; the two quantities may use different denominators or conditions, and the discrepancy requires source reconciliation. The 34.09% energy-saving result belongs to another trace and must not be combined with the Azure_code5 quality result.

The framework's claim is therefore not “lower frequency is free.” It is that phase-specific control can choose a lower-energy operating point while meeting the selected latency constraints often enough in the evaluated traces. A service operator must retain tail TTFT/TBT, request-level misses, queue delay, output completion, and energy measurement scope. GPU-stage energy is not automatically whole-node energy, datacenter energy, cost, or carbon emissions.

### What this establishes and what remains open

GreenLLM establishes a concrete control strategy under the stated A100, NVML, fixed-memory-clock, model, trace and SLO conditions: isolate prompt lengths, optimize prefill frequency from a fitted queueing/energy model, and adapt decode frequency from observed token rate and TBT. It does not establish transfer to other GPU generations, power governors, memory clocks, workloads, model architectures, traffic bursts, thermal states, or SLO definitions. Frequency changes can also interact with co-tenants and power caps.

Stronger evidence would report full energy accounting boundaries, transition overhead, controller settling time, tail distributions, queue fairness for long prompts, independent traces, repeated runs, and the exact denominator behind every SLO-violation summary. [Version-1 manuscript, Sections 2–5, PDF pages 2–10, Tables 1–3](https://arxiv.org/pdf/2508.16449v1#page=7)

## GREEN: place cloud work using a graph-based resource model

Cloud placement assigns tasks to machines. Scheduling decides when they run. Consolidating work can allow some machines to become idle or sleep, but can also increase interference and delay. Spreading work can improve response time while keeping more hardware powered.

[GREEN](../observed-subthemes/datacenter-and-cloud-systems.md#paper-dac-2026-research2970) combines graph neural networks and reinforcement learning for placement and scheduling. Its official description reports up to a 2.17× energy-saving ratio without worse stated SLO metrics, using COSCO simulation and CloudLab experiments. The 100–1,000-server scaling result explicitly belongs to simulation, not a demonstrated thousand-server physical deployment. The full manuscript, power accounting, workload conditions, and exact ratio definition remain unrecovered. [Official DAC description](https://63dac.conference-program.com/presentation/?id=RESEARCH2970&sess=sess141).

The [author repository](https://github.com/UIUC-ChenLab/GREEN) provides separate simulation and Docker Swarm/CloudLab implementations, with configurations that enable or disable server sleep. Its real-testbed setup requires multiple machines and privileged installation. The repository has been inspected for availability, not executed or independently reproduced here.

<span id="explanation-dac-2026-research2970"></span>

### GREEN: cloud placement is a graph decision with an energy objective and service constraints

### What scheduling and placement decide

Cloud resource management assigns workloads to servers and decides when they run. A placement changes which compute, memory, storage and network resources a workload uses. A scheduling decision changes the order or time at which work executes. Consolidating workloads can make unused servers eligible for sleep, but it can also increase contention, queueing and interference. Spreading workloads can reduce contention while leaving more servers powered on.

The decision is constrained by service-level objectives (SLOs). An SLO may limit response time, deadline misses or another service measure. An energy-efficient placement is acceptable only if the work still completes within its SLO and the energy accounting includes any migration, startup, idle and sleep-transition costs.

### What the graph formulation represents

GREEN reduces scheduling and placement to graph optimization. A graph can represent workloads, servers, resources and their relationships. Nodes can carry attributes such as demand or capacity; edges can represent communication, compatibility, dependency or interference. This representation lets the policy account for relationships that a fixed list of independent server features would omit.

The graph neural network (GNN) computes a representation by passing information along those relationships. The reinforcement-learning (RL) component chooses placement or scheduling actions and receives an objective signal from the resulting energy and service behavior. A policy can learn to consolidate work and sleep servers when that reduces energy, while avoiding placements that cause SLO violations. The reward definition determines what the learned policy treats as important; omitted costs or weak penalties can move a burden outside the reported score.

### What scalability means here

The official description says GREEN produces similarly high-quality solutions for systems with 100 to 1,000 servers in COSCO cloud simulations. This indicates that the learned representation and action process were tested at those simulated sizes. It does not establish equal decision latency, equal energy-model fidelity, or physical operation at 1,000 servers. A larger graph can require more message passing, action selection and state collection, so quality and decision time should be reported together.

The description also cites CloudLab experiments. COSCO simulation and CloudLab are different evidence boundaries: simulation supplies scale and a modeled energy/SLO environment, while a testbed can expose real scheduling and power behavior under its actual machines. The two results should not be merged unless workloads, resource constraints, power measurement and SLO definitions are matched.

### What the reported result establishes

The source reports up to 2.17× energy savings over prior state-of-the-art resource managers without compromising stated SLO metrics. “Up to” identifies the strongest reported condition. The packet does not identify workload traces, server heterogeneity, power model, SLO targets, baseline tuning, training cost, migration behavior or the exact meaning of the energy ratio.

The author repository makes the implementation boundary clearer by separating simulation and Docker Swarm/CloudLab paths and exposing server-sleep configuration, but repository availability is not an executed reproduction. The evidence supports a GNN-RL resource-management direction with simulation-scale claims and testbed evidence; it does not establish a universal energy ratio, a thousand-server physical deployment or zero SLO impact under arbitrary workloads.

### The evaluation that would establish cloud-management value

Report workload traces, server types, graph construction, action space, RL reward, training cost, inference time, migration and startup costs, sleep-transition power, idle power, network traffic and SLO definitions. Separate simulation and testbed results, and measure energy, latency distributions, throughput, violations, utilization and decision overhead. Compare against tuned heuristic and ML baselines under identical workload and server constraints. Test fast demand changes, unseen cluster sizes, heterogeneous hardware and policies that are not allowed to sleep servers.

The [GREEN](../observed-subthemes/datacenter-and-cloud-systems.md#paper-dac-2026-research2970) record describes GNN-RL scheduling and placement for energy-efficient cloud resource management. The detailed explanation above separates placement from scheduling, graph representation from policy quality, simulated scale from physical deployment, energy savings from SLO compliance, and repository availability from independent reproduction; this card is the compact evidence record.

A graph neural network computes representations using relationships between graph elements. For resource management, this can express connections and constraints more naturally than a fixed-length description of one cluster size. However, accepting a larger graph does not establish equal decision quality or acceptable decision time at that size.

Reinforcement learning selects actions using an objective accumulated over interactions. If the objective omits migration time, startup energy, deadline misses, or failed actions, a learned policy can appear efficient while shifting cost outside the measurement. Testing on larger clusters must retain those costs and include workloads unlike those used for training.

## The cross-paper insight: local resource savings can move the bottleneck

Sharing memory can admit more work and increase queue contention. Routing away from a busy GPU can change output quality or overload another device. Scaling experts can increase communication. Lowering frequency can increase waiting. Consolidating machines can increase interference. These are consequences to test, not reasons to reject the methods.

The long-term hypothesis is that resource controllers need a shared account of completed work, quality, and deadlines. This selected sample supports that research question, not a historical claim that one design is becoming dominant. Comparable multi-year evidence would preserve request distributions, model quality, hardware budgets, software versions, and energy boundaries.

A useful end-to-end experiment would combine compatible mechanisms, record their decisions over time, and compare accepted work per joule or per unit cost under fixed latency and quality targets. It should retain rejected requests, timeouts, startup events, and rare slow responses. Without those records, a favorable average can conceal the work that the system failed to deliver.
