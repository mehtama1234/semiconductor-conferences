## Why a system uses more than one kind of memory

This chapter's selected group contains 14 evidence records. All fourteen now have individual explanations, but source completeness varies and independent comprehension review remains open. Description-backed mechanisms are not promoted to verified implementations. HybriMoE is a DAC 2025 comparison case, not a DAC 2026 paper.

A computation needs values at different times and frequencies. Some values are reused many times within a short interval. Others occupy a large amount of space but are rarely accessed. Providing the fastest possible storage for every value is constrained by physical area, cost, power, and how storage connects to the processor.

A memory hierarchy places some data in smaller, faster storage and other data in larger or slower storage. The benefit depends on choosing the right values for the fast part. A large fast memory with poor placement can still spend time waiting for data that resides elsewhere.

### Follow a request before assigning a performance number

An operation needs a value at a particular time. If that value is already accessible where the operation executes, it can proceed once the local access completes. Otherwise, the system must obtain the value from another location or move the computation to a location that has it. Either choice has a cost. Reading memory, transferring between devices, and executing arithmetic are different stages.

Latency is the time one request takes to finish. Bandwidth is the rate at which data can be moved over an interval. A transfer can have a large fixed starting delay but a high sustained rate once moving. A useful first approximation for an isolated transfer is `start delay + bytes / transfer rate`. It omits contention and software overhead, so it is a model to check, not a universal timing guarantee.

For an illustrative 8-megabyte transfer at 16 gigabytes per second, using decimal units, the data-movement term is 0.5 milliseconds. If the operation that needs it takes 0.1 milliseconds on the destination device, transferring and then computing costs at least 0.6 milliseconds before other overheads. Faster arithmetic alone cannot remove the transfer. These numbers are not measurements of a paper's hardware.

The amount moved may exceed the amount immediately requested. A system can fetch a cache line, memory page, tensor, or entire expert weight array as its transfer unit. Larger units can reduce bookkeeping or support efficient transfers, but they also move unused data when only a small portion is needed. The transfer unit is therefore part of the policy, not a detail to omit from a comparison.

## A cache is a prediction about reuse

A cache keeps a copy of a value because the system expects to use it again. A hit means the requested value is present. A miss requires fetching it from another location. Fetching may also require choosing an existing cached value to discard, a decision called eviction.

The hit rate alone does not determine application performance. Missing a value on a dependency-critical path can matter more than missing a value whose transfer overlaps other work. A policy can also improve hit rate by fetching unnecessarily large amounts of data or by delaying another application's requests. Count the resulting movement and waiting time.

Suppose one policy has 90 hits in 100 requests, with each of its ten misses causing ten units of unavoidable waiting. Another has only 80 hits, but its twenty misses each cause one unit of waiting. Their miss-related waiting totals are 100 and 20 units respectively. This constructed example omits hit costs and overlapping work to isolate the point: the higher hit rate need not mean lower execution time. A real comparison must account for those omitted costs as well.

## Moving a value should repay its cost

Memory tiering assigns data to storage with different capacity and access costs. Moving a value to the faster tier incurs a transfer and may displace another value. Promotion helps only when later accesses save enough time or energy to justify those costs.

Prefetching starts a transfer before the application requests the value. A correct early prediction can hide the wait. A wrong or late prediction uses bandwidth and space without supplying the intended benefit. The useful question is therefore when the prediction becomes available, what it costs to act on it, and whether the value is still needed when it arrives.

If promotion costs 12 units and each later access saves two units, six accesses only recover the transfer cost. More than six are required for a strict benefit under that simplified model. Evicting another useful item or competing with foreground traffic raises the break-even point. Counting predicted future accesses without considering when they occur can also overstate the benefit: the data must arrive before those accesses to help them.

The working set is the collection of data needed during the interval being considered. A policy tuned to a working set that fits in fast storage may behave very differently just beyond that capacity. At that point, repeatedly bringing one item in can repeatedly remove another item that is about to be used. Testing only one size can conceal this change in behavior.

<span id="explanation-dac-2025-research1019"></span>

## HybriMoE connects model behavior to cache decisions

### Why selecting fewer experts does not make all their weights disappear

A mixture-of-experts layer contains several learned functions called experts. A routing function selects which ones process an input and how their outputs contribute to the result. The model can therefore use only part of its total parameters for one input. It still needs access to every expert that routing might select later.

Weights are the stored numerical parameters of these functions. Activations are the intermediate values being processed. Moving an expert's weights and moving its input activations are different operations, often with very different data sizes. A system short of GPU memory can keep some experts in CPU-accessible memory, but it must then decide what to do when they are selected.

Three decisions follow: which weights to retain on the GPU, which future weights to transfer early, and where to execute the currently selected work. They influence one another. Caching an expert changes the cost of executing it on the GPU; deciding to compute it on the CPU can eliminate the need to transfer its weights for that use.

### Compare complete routes, not processor labels

Return to the illustrative 8-megabyte expert whose transfer takes 0.5 milliseconds and GPU execution takes 0.1 milliseconds. Suppose CPU execution with the weights already available takes 0.4 milliseconds, including the required input/output handling for this example. For a single use, the CPU route finishes in 0.4 milliseconds while transfer-then-GPU takes at least 0.6. The GPU's arithmetic is faster, but that route is slower.

Now suppose the transferred weights remain cached and serve ten otherwise equivalent uses. Ignoring overlap and additional costs, the GPU route takes `0.5 + 10×0.1 = 1.5` milliseconds, while ten CPU executions take 4 milliseconds. Reuse changes the decision. Neither route is always better merely because one processor has higher peak arithmetic throughput.

Real scheduling also depends on existing queues. A nominally faster device can be busy, while a slower one can begin immediately. For independent CPU and GPU work that starts together, completion is determined by the later finishing branch, not the sum of both execution times. Transfers required by GPU work must finish before that work can begin; overlap cannot violate the dependency.

### The paper's scheduling change

HybriMoE measures processing and transfer behavior during warmup. Its scheduling rules favor high-load cached experts on the GPU, low-load uncached work on the CPU, and high-load uncached experts for transfer. It simulates CPU, GPU, and transfer timelines to choose an allocation. [Version-1 manuscript, Section IV-A–B and Figures 4–5](https://arxiv.org/html/2504.05897v1#S4.SS2).

The purpose of a timeline model is to estimate when the complete layer finishes, not to maximize how busy every device appears. Keeping the CPU busy with work that delays a more useful transfer or overloads memory access can hurt the objective. Likewise, sending everything to the GPU can leave it waiting for weights.

The model's estimates are assumptions that need checking under execution. Warmup under an idle system can mispredict a loaded system. Expert size, number of inputs assigned to an expert, CPU memory behavior, and competing transfers can change timing. A scheduling heuristic that works well on measured cases is not an unrestricted proof of optimal scheduling across devices.

### Prefetching asks when a future miss would matter

The paper estimates the benefit of prospective expert prefetches through scheduling simulation and uses routing information to predict later-layer demand. Its score-aware cache retains experts using an updated priority based on routing scores rather than only past access frequency or recency. [Section IV-C–D, Figure 6 and Equation 3](https://arxiv.org/html/2504.05897v1#S4.SS3).

A routing score is a model-generated indication used in selecting an expert; it is not the same measurement as how much time loading that expert will cost. A good prediction may have little performance value if the expert could run cheaply on an idle CPU. A less frequent miss can be more important if it would delay all later work. This is why predictive accuracy, cache hit rate, and total saved time are distinct evaluation quantities.

Prefetching too early can occupy scarce GPU memory for too long. Prefetching too late leaves the transfer on the waiting path. An incorrect prediction can consume the link while urgently required data waits. The correct baseline must therefore charge for unused prefetches and any useful weights they displace.

### Prompt processing and token generation have different work patterns

Prompt processing, often called prefill, processes the supplied input tokens before the first output token is produced. A token is a unit of the model's input or output representation, often corresponding to a word fragment or punctuation. Subsequent decoding generates output incrementally, so later work can depend on earlier generated tokens.

Many prompt tokens can create a larger set of expert work than one incremental decoding step. The number of tokens assigned to each expert changes the amount of arithmetic performed for the same stored weights. Consequently, a placement decision that is efficient for one phase need not be efficient for the other.

Time to first token measures the initial wait. Time between tokens measures incremental output delay. A throughput number is another aggregation and must state the request and concurrency conditions. Combining an initial-latency speedup with a decoding-throughput gain into one universal speedup loses these distinctions.

### What was evaluated and what remains unresolved

The identified setup is an RTX A6000 and Xeon Gold 5220R using ten CPU cores. The reported averages against kTransformers are 1.33× first-token speedup and 1.70× decoding-throughput improvement. Cache-ratio variation is not a demonstration across different physical platforms. [Section VI-A–B, Figures 7–8](https://arxiv.org/html/2504.05897v1#S6).

The preserved assessment records three models and the tested input/cache configurations, while leaving repeat counts, concurrency settings, accuracy parity, aggregation weights, and exact software commits unresolved. [Primary condition assessment](../../dac/data/hybrimoe-primary-conditions-v1.json). It remains a selected-section assessment, not an independently reproduced experiment or confirmation of the final proceedings version.

A useful follow-up would hold model, numerical representation, input workload, and available memory constant while comparing the complete policies. Separate cache, prefetch, and scheduling effects; include warmup and policy-decision overhead; and measure slow requests as well as averages. Test changing expert demand and contention, not only stationary repeated inputs. The [paper evidence record](../observed-subthemes/memory-hierarchy-and-persistence.md#paper-dac-2025-research1019) preserves the source conditions without making those missing tests disappear.

<span id="explanation-dac-2026-research2945"></span>

## RememTier: protect useful residency from competing access bursts

### Why a frequently touched page may still be a poor placement choice

A page is a unit in which a system can manage address translation, placement, or transfers; its size and role must be specified for the particular implementation. A memory-tiering policy uses observations about accesses to decide which pages deserve scarce faster storage. A page that was accessed frequently in a short recent interval is not necessarily a page that will be used again.

Consider a small trace with fast storage for four pages. A main application repeatedly needs A, B, C, and D. An auxiliary task briefly accesses X, Y, Z, and W and then stops using them. If the policy replaces all four main-application pages with the four auxiliary pages, the next main-application pass must recover A through D. The newly admitted pages have displaced data with continuing reuse.

Admission means keeping a fetched page in the cache; replacement chooses which resident page to remove when space is needed. A least-recently-used policy removes the page whose last access occurred furthest in the past. With admission on every miss, the sequence `A B C D X Y Z W A B C D` produces twelve misses from an empty four-page cache. If the four known one-time auxiliary requests bypass the cache, the same sequence produces eight misses and four final hits. This is a constructed trace with perfect knowledge of which requests are one-time; it is not RememTier's algorithm or measured gain. Real policies must infer future reuse without that knowledge.

The challenge is therefore a prediction problem as well as a capacity problem. A policy that rejects every burst can harm a newly started application whose burst is the beginning of sustained work. A useful classifier must distinguish transient demand from continuing reuse early enough to avoid waste, without permanently excluding data that becomes important.

### What the recovered description proposes

DRAM, or dynamic random-access memory, holds working data while powered. Host memory here means memory belonging to the main computer. CXL, short for Compute Express Link, is a connection standard that allows processors to communicate with attached devices, including devices containing memory. These names identify components and connections, not their measured access times. The separate CXL protocols are explained below.

RememTier assigns CXL DRAM as the fast tier for main applications while isolating auxiliary tasks in host memory. It adds a sparse-burst-resistant page-replacement policy and cacheable/streamed CXL.io accesses with data reordering. The description reports up to 35% lower execution time and over 60% lower swap-in latency on mixed workloads including K-means, Radiosity, and ResNet50. [Official DAC description](https://63dac.conference-program.com/presentation/?id=RESEARCH2945&sess=sess169).

“Fast tier” is relative to the system and path being compared. This placement claim is not proof that attached CXL DRAM has lower isolated access latency than host DRAM. The proposed benefit can depend on reduced interference, allocation policy, or avoiding a still slower path. Those effects need measurement rather than inference from a tier's name.

Separating main and auxiliary allocations can protect residency, but it does not necessarily isolate every shared resource. The tasks may still share processor time, memory controllers, links, or software queues. Conversely, reserving capacity for one class of work can leave that capacity underused when the class is idle. A comparison must state both the priority policy and what happens to unused reservations.

### Large transfers trade per-request cost against unnecessary movement

A storage-backed path can pay an overhead for each request in addition to the time required to move its bytes. Combining nearby requests into a larger transfer can reduce the number of such overheads. But if most of the larger region is unused, it consumes bandwidth and memory capacity without corresponding useful work.

For an illustrative 64 KiB transfer containing only one useful 4 KiB region, 16 times as many bytes move as the immediate request requires. If all sixteen 4 KiB regions are subsequently needed before eviction, the larger transfer can instead serve all of them. The same transfer size can therefore be wasteful for sparse accesses and useful for dense reuse. This arithmetic is not a reported RememTier block size.

Data reordering may seek to make accesses easier to service together, but correctness still requires the application to receive the specified values in an allowed order. A read-only rearrangement and reordering writes with synchronization requirements are different cases. The description does not disclose enough to establish which transformations the implementation permits.

### CXL names do not specify the complete access path

CXL includes distinct protocols: CXL.io supplies PCIe-like I/O semantics, CXL.cache supports caching semantics, and CXL.mem supports memory-access semantics. They must not be treated as interchangeable labels. [CXL Consortium protocol overview](https://computeexpresslink.org/webinars/memory-challenges-and-cxl-solutions-345/).

The description specifically names CXL.io; this writeup preserves that statement. It does not silently reinterpret the design as an ordinary CXL.mem expansion device. Establishing how its cacheable and streamed accesses work requires the actual request path, host mappings, device behavior, and software implementation. Whether a particular access is served by DRAM, an SSD-backed path, or a software-managed transfer also needs to be stated.

An SSD is a solid-state storage device. Its presence is not a persistence contract: using storage that retains bits without power does not by itself guarantee that an application can recover its last completed update. A system can use that storage for paging while losing the information that maps addresses to stored pages, or leaving some writes incomplete. Durable application updates require an ordering and recovery definition separate from tier-placement performance.

### Execution time and swap-in latency are different results

Swap-in latency concerns obtaining data from a lower storage layer when needed. Application execution time also includes computation, other memory accesses, scheduling, and any overlap between them. A large reduction in one type of wait need not cause an equally large application speedup.

Suppose a hypothetical application takes 100 seconds, including 20 seconds of unhidden swap-in waiting. Reducing only that waiting by 60% saves 12 seconds, leaving 88 seconds, or about 1.14× speedup. This example is not the paper's workload decomposition. It explains why the two reported percentages cannot be substituted for one another or multiplied into a combined gain.

“Up to” also identifies a best observed case under the reported comparison, not the expected improvement for a new workload. Reported improvement for the main task must be read alongside the effect on auxiliary tasks. A policy can improve a priority task while reducing aggregate throughput; whether that is desirable depends on the declared service objective.

### What the full comparison still needs

Fresh title/name searching did not recover a matching manuscript. The [evidence record](../observed-subthemes/memory-hierarchy-and-persistence.md#paper-dac-2026-research2945) remains description-backed, with device generation, topology, capacities, page sizes, firmware, software path, and baseline tuning unresolved. No complete implementation or paper-specific classifier is reconstructed from the short description.

A useful experiment would hold device capacity and workload mix constant, then separate the effects of placement isolation, burst classification, access mode, and reordering. Include workloads with genuine sustained bursts as well as scans, and measure mistaken admissions and mistaken exclusions. Report per-task latency, total throughput, transferred bytes, migrations, and recovery after demand changes. This would test whether the policy recognizes useful reuse rather than merely favoring the benchmark's predefined main task.

<span id="explanation-dac-2026-research675"></span>

## SAEM: choose when to change expert placement

### Start with the computation, not the phrase “stage-aware”

A language model generates a sequence of tokens, the text units its tokenizer represents as numbers. During ordinary sequential decoding, the next token depends on the tokens already generated. A long answer therefore involves many successive model evaluations. Producing intermediate mathematical steps does not remove that dependency.

Within a mixture-of-experts layer, routing selects a few expert functions to process each token's numerical representation. Each selected function needs its trained weights. The function can execute where those weights reside, or the system can move the weights elsewhere. The routing decision and the placement decision answer different questions: which function must run, and where will it run? Moving an expert does not authorize replacing it with a different function.

Suppose consecutive portions of a generated answer repeatedly select similar experts. A memory policy could retain those experts across many decoding steps instead of reconsidering placement after every access. But the word “stage” needs an operational definition. A human division into derivation, checking, and conclusion is not automatically observable by the runtime, nor is it necessarily the division that best predicts memory demand.

### The recovered method and its version boundary

The recovered preprint explicitly extends DAC with additional detection detail, datasets, and an oracle analysis. [Version note, PDF p. 1](https://arxiv.org/pdf/2608.21614v1#page=1).

Its detector matches model-calibrated textual cues. At boundaries, completed-stage expert counts rank replacements within fixed per-layer GPU slots. Transfers overlap computation; CPU execution and per-layer token repacking complement placement. [Method, PDF pp. 4–6](https://arxiv.org/pdf/2608.21614v1#page=4). The [updated evidence record](../observed-subthemes/memory-hierarchy-and-persistence.md#paper-dac-2026-research675) gives the recovered setup and distinguishes the two reported throughput averages. Its previous description-only record remains available for provenance.

The following examples derive the consequences of these choices. They are not reconstructed SAEM traces, measured timings, or claims that its detector produces a faithful account of a model's internal reasoning.

### A boundary is a trigger, not knowledge of the future

Consider a hypothetical layer with four experts A, B, C, and D and room for two on the GPU. During one completed interval, 100 single-expert requests selected them 45, 35, 15, and 5 times. Retaining A and B would have served 80 of those requests locally. That is a statement about the past, not yet a prediction score.

If the next interval has counts 40, 40, 10, and 10, the same choice serves 80 of its 100 requests. If instead its counts are 5, 5, 45, and 45, it serves only ten. A perfect detector of interval boundaries cannot fix this second case: the previous interval simply predicts the next one poorly. The policy needs both useful update timing and useful demand information.

This also explains why “experts are stable within a stage” is insufficient by itself. Stability within the completed stage makes its measured counts less noisy. Successful placement for the next stage additionally requires similarity across the boundary, or another predictor of the change. A stage could be internally consistent and still be followed by a completely different demand pattern.

A text marker has its own failure modes. The same phrase can appear without a meaningful change in expert demand; a demand change can occur without that phrase. The first case may cause unnecessary updates. The second may leave an unsuitable placement unchanged. A phrase-based policy should therefore be tested against actual routing demand, not accepted because the phrase seems linguistically reasonable.

### Updating less often trades overhead for delayed adaptation

Imagine that one placement decision takes 20 microseconds of unavoidable processing time. Repeating it after each of 200 generated tokens costs four milliseconds. Doing it once for the whole interval costs 0.02 milliseconds, saving 3.98 milliseconds. This is an illustrative accounting model with no overlap.

Now suppose delaying adaptation causes eight additional misses, each adding one millisecond of unhidden waiting. That eight-millisecond penalty is larger than the decision-time saving. Fewer updates are beneficial only when the avoided bookkeeping and movement exceed the cost of stale placement. A long interval can make bookkeeping cheap per token while allowing a wrong decision to persist for longer.

Transfers introduce a further deadline. If a required transfer takes two milliseconds and can start only 0.5 milliseconds before the expert is needed, at least 1.5 milliseconds remains exposed under this isolated model. Calling a transfer asynchronous means other work may proceed while it runs; it does not guarantee that the transfer finishes soon enough. The next operation must still wait for valid weights.

### Group ready work without changing token dependencies

Repacking changes the organization of work already available at a layer. It cannot safely collect a future token from the same sequence before the preceding token has been generated. The distinction matters because a large group of independent requests offers grouping opportunities that one sequential request may not.

For a constructed batch of three ready token representations, let routing select the following expert pairs:

| Ready token | Selected experts | Where its contributions must return |
|---|---|---|
| u | A and B | Output slot u |
| v | B and C | Output slot v |
| w | A and C | Output slot w |

The runtime can form input groups `A: [u, w]`, `B: [u, v]`, and `C: [v, w]`. Each expert processes its group. The runtime must then return each result to the correct token and combine it using the prescribed routing weights. Token u still requires contributions from A and B; grouping does not reduce six required token–expert evaluations to three.

What can decrease is repeated launch and data-indexing overhead. A kernel launch starts a piece of GPU work; very small jobs can spend a substantial fraction of time getting started. Grouping can replace several small launches with fewer larger ones, but constructing groups, moving representations, and restoring output order also take time and temporary memory. The complete comparison includes all those steps.

For example, if the two contributions for u are numerical values 2 and 6 with routing weights 0.25 and 0.75, its combined value is `0.25 × 2 + 0.75 × 6 = 5`. An incorrect output mapping that substitutes v's contribution changes the model computation even if every expert ran quickly. Correct indexing and combination are part of the method's obligations, not optional postprocessing.

### CPU execution can avoid weight movement without eliminating communication

Running an expert on the CPU can leave its large weight array in host memory. The token representations and results may still have to move between devices. The comparison is the complete CPU route against the complete GPU route, including waiting and synchronization—not CPU arithmetic time against GPU arithmetic time alone.

Suppose the CPU route takes 0.6 milliseconds including input and output transfers. Suppose moving the weights and executing on the GPU takes 1.2 milliseconds for the same request. CPU execution saves 0.6 milliseconds in isolation. But if the CPU has two milliseconds of queued work, its effective completion time becomes 2.6 milliseconds, and that preference reverses. These numbers illustrate a scheduling dependency, not the paper's hardware.

A token requiring results from both devices cannot advance until both are ready. If one branch finishes in 0.2 milliseconds and another in 0.8, their combined result is unavailable before 0.8, even when the branches overlap fully. Improving a branch that already finishes early may not improve the layer's completion time.

### What a controlled comparison would establish

The first question is whether the same required work is completed. Keep model weights, routing, prompts, output limits, and quality criteria explicit. Then compare placement policies under the same available memory and device resources. A reduced expert cache is not by itself a measurement of total memory: other weights, saved attention state, temporary grouping space, and transfer buffers also occupy storage.

Next separate three questions. Does the boundary signal identify a useful time to update? Do past counts predict future demand? Does the selected placement reduce total runtime after all movement and processing costs? A good score on one question does not answer the other two. Remove or vary each mechanism while preserving the other resources to identify its actual contribution.

A diagnostic policy with advance knowledge of future requests can estimate how much a predictor might improve. It is not deployable, and it is not automatically the fastest possible system: it may retain the same update schedule and placement restrictions, while optimizing a cache statistic rather than total completion time. Comparing such policies on the same prerecorded sequence isolates placement effects; evaluating freely generated answers is separately necessary for deployment claims.

Calibration uses example workloads to choose policy settings before deployment. A comparison on similar workloads asks whether those settings are useful under matching conditions. A held-out workload asks whether that usefulness transfers. Neither setting alone establishes long-term stability across new model versions, languages, prompting styles, or traffic mixtures. Report calibration cost and its reuse period, not just steady-state tokens per second.

### How SAEM changes the question raised by HybriMoE

The comparison in this chapter suggests three separable decisions: which work must execute, where it should execute, and when placement should change. The first is part of the model's required computation; the latter two are runtime choices. This is a conceptual synthesis, not a measured ranking between papers.

A useful next experiment would hold the execution backend and model constant while exchanging the placement-update rule, then measure transfer volume, queue delays, end-to-end throughput, and answer quality. Otherwise, gains from better grouping or CPU execution could be mistaken for gains from better boundary detection. A durable research insight would identify the demand conditions under which each update rule helps—not merely conclude that using model structure is beneficial.

<span id="explanation-dac-2026-research461"></span>

## MoE-Balance: schedule for completion time, not equal task counts

### The same required expert work can finish at different times

A CPU and a GPU are different processors with different execution and memory costs. Assigning half the experts to each does not imply that they finish together. An expert's time also depends on how many token representations it processes, whether its weights are already accessible, and which earlier operations occupy the processor or transfer connection.

The immediate objective for a layer is to produce all required outputs. If several expert outputs must be combined, the next dependent operation waits for the last required contribution. An early-finishing processor can therefore be idle even though another processor still has substantial work. That waiting is a symptom to explain, not proof that moving any available task to the idle processor will help.

The official description proposes a dynamic scheduler driven by current load, together with cross-layer prefetching and chunked PCIe weight transfers. It reports Mixtral-8x7B throughput and latency improvements under memory constraints. [Official DAC description](https://63dac.conference-program.com/presentation/?id=RESEARCH461&sess=sess109). PCIe is the device connection carrying transfers here; naming that connection does not specify its achieved transfer rate.

The following schedules are constructed explanations of the design problem, not executions of MoE-Balance or reconstructions of its unspecified scheduler.

### Count time and dependencies before distributing tasks

Consider four independent, ready expert tasks, with illustrative complete-route costs in milliseconds:

| Task | CPU route | GPU route |
|---|---:|---:|
| A | 2 | 1 |
| B | 2 | 1 |
| C | 8 | 2 |
| D | 8 | 2 |

Assume each processor runs its assigned tasks sequentially, the two processors run concurrently, and all route costs are independent. These assumptions deliberately omit shared-link contention. Assigning A and B to the CPU takes four milliseconds, while C and D on the GPU also take four. All outputs are ready after four milliseconds.

Reversing the assignment still gives each processor two tasks, but now the CPU takes sixteen milliseconds and the GPU takes two. Equal task counts conceal a fourfold difference in completion time between these assignments. Running all four on the GPU would take six milliseconds: using the CPU badly can be worse than leaving it unused.

For this example, the objective is `max(CPU finish time, GPU finish time)`. Four milliseconds is the best assignment: assigning C or D to the CPU already takes at least eight; assigning neither leaves the choice among A and B, and assigning both of those to the CPU produces the four-millisecond solution. This small proof does not establish optimality for the paper's larger, shared-resource problem.

In an actual runtime, a route's finish time includes when its inputs become ready, when the processor becomes available, any necessary transfer, execution, and delivery of its output. A measurement of current utilization alone does not give those quantities. A busy processor may soon finish; an idle processor may be a poor choice for the available task. A dynamic policy needs predictions whose errors are measured as conditions change.

### Smaller scheduling units introduce their own cost

An expert task could mean all tokens assigned to an expert, a smaller token group, or a supported portion of the expert's arithmetic. Those alternatives have different dependencies. The recovered description does not specify which units its scheduler may divide or move, so this writeup does not equate fine-grained scheduling with an arbitrary split of a neural network.

Smaller units can create more opportunities to overlap work, but every decision, launch, and synchronization can cost time. If scheduling a unit adds ten microseconds and the unit performs only five microseconds of useful work, overhead is twice the useful work before any transfer is counted. If a unit instead performs 500 microseconds, the same overhead is two percent of useful work. These illustrative ratios explain why the smallest possible unit need not be the fastest choice.

Nor does “real-time load” establish a hard deadline guarantee. Reacting to current conditions and proving that every request meets a deadline are different obligations. The latter would require specified arrival limits, execution bounds, and an admission policy for work that exceeds capacity.

### What chunking can—and cannot—overlap

Moving all weights before starting all computation produces a transfer phase followed by a compute phase. Dividing a transfer into chunks can allow computation on an earlier chunk while a later chunk moves, but only if the computation can legally consume that earlier chunk independently or maintain valid partial results.

For an ideal example with three chunks, let each transfer take one millisecond and each corresponding computation take two. Assume one transfer engine, one compute engine, sufficient separate buffers, and no contention between the engines. Moving all three chunks and then computing takes `3 + 6 = 9` milliseconds. A valid overlapping schedule is:

| Chunk | Transfer interval, ms | Compute interval, ms |
|---|---|---|
| 1 | 0–1 | 1–3 |
| 2 | 1–2 | 3–5 |
| 3 | 2–3 | 5–7 |

The last result is ready after seven milliseconds. The schedule saves two milliseconds, not the entire three-millisecond transfer time: the first computation still waits for its input, and the final computation must finish. The general result for this ideal equal-chunk, two-engine case is `transfer time per chunk + compute time per chunk + (chunk count − 1) × max(transfer time per chunk, compute time per chunk)`.

This result relies on the assumptions. A buffer cannot be overwritten while computation still reads it. If the compute operation requires the whole weight array, receiving the first chunk does not make it runnable. If transfers and arithmetic compete for memory bandwidth, their concurrent times may exceed their isolated times. Smaller transfers may also pay repeated setup overhead. The paper's actual partition, buffer ownership, and synchronization rules are therefore necessary evidence, not implementation details that can be filled in from the word “chunked.”

### Prefetching across layers still needs a trustworthy prediction

A later layer can use different experts from the current layer, and its routing input depends on earlier computation. Starting a weight transfer before that later routing decision is available requires some other information about future demand. A prediction may be useful without being certain, but its benefit depends on both accuracy and lead time.

Suppose a correct early transfer avoids one millisecond of future waiting, while an incorrect transfer causes 0.5 milliseconds of extra delay by occupying a shared connection. With correctness probability `p`, the simplified expected saving is `p × 1 − (1 − p) × 0.5` milliseconds. It becomes positive only when `p > 1/3`. This is a constructed one-request model; it excludes cache eviction, scheduler overhead, late correct predictions, and interactions among transfers.

Those omissions explain why prediction accuracy alone is insufficient. A correct transfer that finishes after demand arrives hides less waiting. An incorrect transfer that displaces valuable weights can cost more than its own transfer time. A practical comparison should separate useful-and-timely, useful-but-late, and unused prefetches, then measure their effect on required work.

### Read the reported throughput and latency together

The description reports 1.6× higher throughput and 37.5% lower end-to-end latency. Its [evidence card](../observed-subthemes/memory-hierarchy-and-persistence.md#paper-dac-2026-research461) preserves the missing hardware, workload, and baseline conditions.

For fixed work processed sequentially, throughput is work divided by time. A 1.6× throughput ratio then corresponds to a new time of `1 / 1.6 = 0.625` times the old time, a 37.5% reduction. The numerical agreement means these could describe the same underlying time change; it is not evidence of two independent gains to multiply together.

Under concurrent requests, that reciprocal relationship need not hold. A system can increase total tokens per second while making one request wait longer in a batch. The source needs to specify whether latency includes queueing, prompt processing, decoding, or an entire request, and whether the two metrics use matching workloads. No particular measurement protocol is inferred here from the matching percentages.

### What remains unknown, and what would make the comparison useful

Fresh title, author, repository, and artifact searches recovered the official description and a matching [author publication listing](https://www.essex.ac.uk/people/SINGH42308), but not a full manuscript or implementation. A publication listing confirms identity; it does not reveal the scheduling rule. Related work on expert balancing is not substituted for this paper.

A useful experiment would first measure the scheduler with fixed weight placement, then add cross-layer prediction and chunked movement separately. Keep processor resources, memory budgets, model representation, inputs, and required output quality comparable. Report processor and transfer timelines, decision overhead, bytes moved, unused predictions, and complete request times. Include workloads that change routing demand and background CPU load.

The comparison with HybriMoE and SAEM is therefore a set of questions, not a speed ranking. How much of the gain comes from choosing the execution device, from deciding when to change placement, and from moving data early enough? Which choice remains useful after shared bandwidth and queueing are included? Answering those questions under matched conditions could support a lasting insight about hybrid inference; three positive headlines cannot establish it.

<span id="explanation-dac-2026-research2686"></span>

## Adaptive flash read retry: recover a readable interpretation of stored charge

### A stored bit is inferred from an electrical measurement

Flash stores information using charge that affects a cell's threshold voltage: the gate voltage needed to make its transistor conduct. Reading compares the cell against reference voltages to infer its stored state. Several states can encode multiple bits per cell. Variation and charge loss can move or broaden the ranges associated with those states, making the original read references less effective. Error-correcting codes add redundant information that can recover data despite some incorrect raw bit decisions. These are background principles, not measurements of the DAC device. [Cai et al., background and retention characterization, PDF pp. 1–4](https://users.ece.cmu.edu/~omutlu/pub/flash-memory-data-retention_hpca15.pdf#page=2).

Changing a read reference changes the interpretation of the electrical state. It does not restore lost charge or rewrite the data. This is why a failed read can sometimes be recovered without repairing the cell, and why retrying cannot guarantee recovery after arbitrarily severe information loss.

### A small threshold example explains both the opportunity and its limit

Consider eight hypothetical cells storing two possible states, L and H. Their measured threshold voltages are:

| Intended state | Four measured thresholds, volts |
|---|---|
| L | 0.8, 1.0, 1.2, 1.4 |
| H | 1.3, 1.6, 1.7, 1.9 |

For this constructed example, classify values below the chosen reference as L and values at or above it as H. At a reference of 1.8 volts, three H cells are misclassified as L. At 1.5 volts, only the H cell at 1.3 is misclassified. At 1.1 volts, two L cells become incorrect. Lowering the reference helped at first, but lowering it further did not continue to help.

No single threshold perfectly separates these observations: the H cell at 1.3 is below the L cell at 1.4. A read reference cannot simultaneously place both on their intended sides. If a hypothetical code guarantees correction of one raw error in the protected group, reducing three errors to one brings the group within that guarantee. That does not mean the threshold alone recovered every bit, or that three errors are always uncorrectable under every code.

The numbers and code condition above are educational assumptions, not the DAC experiment. In an actual controller, the original data is usually unavailable for counting errors directly. A diagnostic experiment can program known values and compare recovered data against them; a deployed decoder must rely on the code and its validation procedure. A claimed successful recovery should be checked against known written data during evaluation, including the possibility of an incorrectly accepted output.

### What extending a retry table changes

A retry table is a finite collection of candidate read settings. If a read fails, the controller can try another candidate and attempt decoding again. Exhausting the table establishes that the tested candidates failed; it does not establish that every supported read setting would fail.

The DAC description proposes extending that search using wordline-aware interpolation and multidimensional guidance. It reports up to 99% recovery of failed pages and up to 99% and 84% usable capacity at 12- and 30-month retention, respectively, versus the stated baseline's 90% or end-of-life. [Official description](https://63dac.conference-program.com/presentation/?id=RESEARCH2686&sess=sess162). The description does not supply the complete candidate-generation or stopping algorithm.

The central design question is therefore not simply whether more candidates can be tried. It is how to select promising candidates cheaply, decide when to stop, and establish that the additional successful reads are correct.

### Interpolation needs a relationship worth interpolating

A wordline is a control connection shared by a group of cells. Using its position to guide a read setting assumes that position provides useful information about the electrical behavior being corrected. That assumption needs measurement at the relevant cell organization, wear, temperature, and retention conditions.

For a purely illustrative interpolation, suppose a useful setting at position 10 is 1.2 volts and at position 12 is 1.6 volts. Linear interpolation predicts 1.4 volts at position 11. The calculation is easy; the engineering question is whether behavior changes smoothly enough for this estimate to be useful.

If position 11 instead needs 1.8 volts because of a local variation, the interpolated candidate is wrong. A useful controller might still benefit if interpolation starts a short search near the answer, but it needs a way to recognize failure and continue safely. This example does not assert that the paper uses immediate neighbors, linear interpolation, these voltages, or a particular fallback.

### Multiple settings turn retry into a constrained search

When a candidate contains several adjustable references, changing one setting may fix decisions near one state boundary while leaving another boundary poorly placed. A single shift applied identically to all references is not necessarily sufficient.

Suppose a hypothetical candidate has three independently adjustable coordinates, each with five allowed choices. Exhaustive enumeration has `5 × 5 × 5 = 125` combinations. With seven coordinates, the same five choices produce 78,125 combinations. These are search-space examples, not the paper's voltage counts or table sizes.

Guidance is useful when it reduces the number of costly reads needed to reach an acceptable combination. But a local improvement signal need not identify a globally best candidate, and a decoder's success/failure output may reveal less than an exact error count. To understand the actual method, the manuscript must identify the available feedback, valid parameter ranges, candidate order, stopping conditions, and what happens when the search budget expires.

### Recovery rate and usable capacity answer different questions

“Recovered failed pages” conditions the denominator on pages that already failed the earlier procedure. If 100 of 10,000 pages initially fail and a new procedure recovers 99 of those, failed-page recovery is 99%. Across the original population, 9,999 of 10,000 pages are now readable: 99.99%, not 99%. Neither percentage by itself specifies how much capacity the controller exposes for continued use.

Capacity can depend on the controller's treatment of larger allocation units. Consider a hypothetical device with 100 blocks of 100 pages each and a policy that retires an entire block if any page remains unreadable. One hundred unreadable pages confined to one block retire one percent of the raw blocks. The same hundred pages spread one per block retire every block. Identical page-failure counts can therefore have very different capacity effects.

If the spread-out case recovers 99 of its hundred failed pages, 99 blocks become eligible again under this toy policy. Real controllers can reserve spare space, apply different retirement rules, or require further checks before reuse. These examples explain why the paper's page-recovery and capacity statements require separate denominators, failure locations, and management policies. They do not reconstruct its capacity calculation.

### Reliability improvements can make rare reads much slower

Every additional sensing, transfer, and decoding attempt consumes time and energy. For a serial illustrative model, suppose an attempt takes 60 microseconds in total. One attempt takes 60 microseconds; an initial attempt plus twenty retries takes 1,260 microseconds. Overlap or variable decoder effort would change this model and must be measured.

If 95% of reads need one attempt and 5% need twenty-one, the mean is two attempts, or 120 microseconds. Yet the slow five percent still take 1,260 microseconds. An average alone conceals the delay experienced by requests that require recovery, as well as the queueing they may cause for later requests.

A device intended for offline recovery can reasonably accept a different retry budget from one serving interactive requests. A fair result should state the service objective, maximum retries, successful-recovery delay distribution, and residual failure rate when the budget is enforced. Comparing an unlimited search with a tightly bounded baseline would not isolate the value of better candidate selection.

### Retention age is not a complete lifetime specification

Retention concerns time since programming under specified conditions. It is distinct from the number of program/erase cycles, the amount of data written by a host, or time that a device has been in service. A month count without the temperature history, prior wear, stored patterns, and test procedure cannot determine another device's reliability.

If accelerated aging is used, the experiment must disclose how the accelerated condition is converted to an equivalent age and why the conversion applies to the failure mechanism. This is a requirement for interpreting such an experiment, not a claim that the DAC study used accelerated aging. Likewise, “end-of-life” needs a defined failure or capacity threshold; it is not a universal physical event at a particular month.

Fresh exact-title and author searches recovered the official description and an [author publication listing](https://faculty.csie.ntust.edu.tw/~jenwei/), but not the full manuscript. The earlier background paper studies a different flash generation and is not substituted for this missing experiment. The [DAC evidence card](../observed-subthemes/memory-hierarchy-and-persistence.md#paper-dac-2026-research2686) therefore remains description-backed.

The next useful comparison would hold cells, programmed data, prior wear, decoder, and total retry budget constant while comparing candidate selection. Report independently verified recovered bytes, retired blocks, remaining usable capacity, added delay, and failures at each retention condition. This would distinguish a better search from simply spending more time or changing the retirement rule.

<span id="explanation-dac-2026-research1986"></span>

## REFLEX: fewer selected tokens do not necessarily mean fewer activated rows

### Follow an attention computation to the stored values

Attention forms an output by comparing a query vector with key vectors, converting the comparison scores into weights, and summing the corresponding value vectors with those weights. A vector is an ordered list of numbers. In scaled dot-product attention, each score comes from multiplying matching query/key components, summing them, and applying a scale factor. Softmax exponentiates the scores and divides by their total so that the resulting weights sum to one. [Attention definition, Section 3.2.1](https://arxiv.org/html/1706.03762v7#S3.SS2.SSS1).

During decoding, a key-value cache retains previously computed keys and values so later steps can reuse them. This differs from the expert-weight caches discussed above: those hold trained parameters, whereas the KV cache holds representations associated with the processed sequence. Longer retained sequences can require more stored representations and more work to access them.

Sparse attention uses a selected subset rather than every available position. That can reduce arithmetic and requested data, but the memory system does not necessarily fetch or activate storage at the granularity of one selected position. The layout of the retained keys and values therefore matters alongside the number selected.

### Why a DRAM row is a meaningful unit of cost

DRAM organizes cells into rows. Opening a row makes its contents available through a row buffer, from which column accesses select data. Reusing the open row can avoid opening another one; changing rows requires additional operations and obeying memory timing constraints. [DRAM background, PDF pp. 7–10](https://faculty.cc.gatech.edu/~hyesoon/fall11/lec_dram.pdf#page=7).

Consider a constructed layout with sixteen entries, four per row, in one bank. Assume each selected entry fits wholly in one row, no row is initially open, and unrelated accesses do not intervene:

| Row | Entry positions |
|---|---|
| 0 | 0, 1, 2, 3 |
| 1 | 4, 5, 6, 7 |
| 2 | 8, 9, 10, 11 |
| 3 | 12, 13, 14, 15 |

Selecting positions 0, 1, 2, and 3 needs one row opening. Selecting 0, 4, 8, and 12 needs four. Both selections contain four entries and have the same token-level sparsity. Their row-access costs differ because one selection is concentrated and the other scattered.

This example is not a REFLEX layout or device specification. A real key or value vector can span rows, dimensions can be distributed among banks, and several attention heads can access different data. A claimed row reduction needs the actual address mapping, selected positions, vector sizes, and memory command trace—not just a percentage of tokens removed.

### What the recovered description proposes

REFLEX proposes rewrite-free row-aligned KV placement and activation-aware PIM scheduling. Its description claims unchanged hardware and preserved accuracy, with up to 1.64× PIM throughput, 1.36× energy efficiency, and 1.37× GPU-PIM throughput. [Official DAC description](https://63dac.conference-program.com/presentation/?id=RESEARCH1986&sess=sess138).

Processing-in-memory, or PIM, means that some computation is performed within or near memory rather than requiring all operands to be sent to a separate processor. It does not remove the need to access the underlying storage. If the computation repeatedly opens different rows, reducing traffic outside memory can leave substantial work inside memory.

The description does not expose the mapping algorithm, supported sparse selection rule, or exact unit covered by its single-row claim. The following constraints explain what those missing details must resolve; they do not invent an implementation.

### A fixed layout cannot place every arbitrary selection in one small row

Suppose eight entries each have one fixed location, a row holds four entries, and every possible pair may be selected. Requiring every pair to share a row would force all eight entries into the same row: whichever row contains entry 0 must also contain every entry that can be paired with it. That exceeds capacity.

This simple argument shows why the scope of a row-alignment guarantee matters. A design could restrict which entries are selected together, align only a portion of each vector, duplicate data, or use a mapping appropriate to a particular access pattern. These are possible design choices, not claims about REFLEX. Each has a different cost and correctness condition.

A stable layout can also exploit structure without guaranteeing one row for every request. The useful measurement would then be how many row activations it avoids over the evaluated workload, including cases that do not fit the favorable pattern.

### “Rewrite-free” does not mean there are no writes

As a sequence grows, new keys and values must be stored somewhere if later computation will use them. Avoiding repeated relocation of existing entries is distinct from eliminating those initial writes, metadata updates, or normal DRAM maintenance. The exact scope of the paper's rewrite-free claim remains to be established from its manuscript.

To see why relocation cost matters, imagine that repacking existing entries costs six units of work and saves two units on each later use. Three uses only repay the repacking cost; a fourth gives a strict saving in that simplified model. If the selected set changes before enough reuse occurs, repeating the repack can consume more work than it avoids.

A fixed placement avoids that particular recurring cost, but may leave less favorable future selections spread across rows. An honest comparison includes initial placement, sequence growth, address bookkeeping, unused reserved space, and any replication—not just the attention kernel after its inputs have already been organized.

### Scheduling can reduce row switches without changing placement

Placement determines addresses. Scheduling determines the order in which ready operations use them. For a one-bank illustrative request sequence `A, B, A, B`, where A and B denote different rows, servicing the sequence literally requires four activations from a closed starting state. Servicing the same independent reads as `A, A, B, B` requires two under an open-row policy.

The second order is valid only when dependencies and output association permit it. A later operation cannot move ahead of the computation that produces its input. Results must still return to their correct sequence positions. With several banks, concentrating work in one bank may also lose parallelism even while reducing row switches. Row locality and total completion time are related, but they are not identical objectives.

For PIM attention, the command sequence must additionally obey the supported operations, accumulation dependencies, and coordination with any GPU work. An activation count alone cannot establish that these constraints are met or that they fit entirely behind other work.

### Preserve a chosen sparse calculation before judging its approximation

Reordering key-value pairs consistently does not change the exact mathematical weighted sum: each score must remain paired with its value, and the normalization must cover the same selected set. Floating-point execution can still differ slightly with reduction order, so implementation equivalence needs a stated numerical tolerance.

Selecting a different set is a different matter. For an illustrative scalar-value attention calculation with four equal scores and values 0, 0, 0, and 100, dense attention returns 25. Keeping only the first three positions and renormalizing returns zero. A convenient memory layout does not make the omitted contribution irrelevant.

Consequently, “accuracy preserved” needs a reference: preservation relative to the same sparse algorithm is different from parity with dense attention. The evaluation should separately test faithful execution of the selected sparse rule and the rule's effect on model outputs across relevant tasks and sequence lengths. This example is not evidence that REFLEX drops an important token; it establishes what its accuracy claim must specify.

### Interpret efficiency with the correct system boundary

Energy efficiency usually expresses useful work per unit energy, but the actual numerator and measured components must be stated. Under fixed useful work, a 1.36× efficiency ratio corresponds to `1 / 1.36`, about 0.735, times the original energy: roughly 26.5% less, not 36% less. This conversion is conditional on a matching work definition and energy boundary.

An attention-only result and a complete decoding result are also different. If a hypothetical request spends half its time in attention, doubling only that part leaves total time at `0.5 + 0.5 / 2 = 0.75` of the original, a 1.33× speedup. The GPU, PIM, transfers, sparse selection, and synchronization must all be accounted for before converting a local gain into an end-to-end claim.

### What the next source-backed comparison needs

Fresh exact-title searches and the [author-lab publication page](https://iris.skku.edu/publication/c94_dac_2026/) recovered the same description, but no full manuscript or artifact. The record remains description-backed. Search snippets suggesting paper/code links were checked against the live author page; its REFLEX entry did not provide those links.

A useful comparison would keep the selected tokens, numeric representation, row capacity, bank organization, and supported PIM operations fixed while varying placement and scheduling separately. Count row activations, useful bytes, relocation writes, reserved space, and end-to-end time and energy. Then vary the sparse rule under explicitly checked output-quality conditions. That separates a better physical execution of the same work from a change in the work itself.

This paper therefore belongs in the chapter's data-layout and near-memory-computation branch, not its flash-recovery branch. Both concern memory, but one seeks to execute a chosen computation efficiently while the other seeks to recover correct stored information under errors. Their results cannot be pooled into a single memory-efficiency percentage.

<span id="explanation-dac-2026-research676"></span>

## CLUE-ECC: make the correction unit match the fault it must survive

### Redundancy helps only when it distinguishes possible original data

An error-correcting code stores extra information derived from the data. A decoder uses the relationships between data and redundancy to identify a valid original value after some bits change. Detecting an inconsistency and identifying the correct replacement are different tasks.

For a minimal example, encode one bit as three identical bits: zero becomes `000`, and one becomes `111`. Any single flipped bit leaves the result closer to the original than to the other codeword, so majority decoding recovers it. But changing two bits of `000` can produce `110`, which is closer to `111`. The same decoder then returns the wrong original bit. A correction guarantee always needs a limit on the allowed faults.

That example is not a memory ECC implementation. It makes a general obligation concrete: a decoder must either recover correctly within its guaranteed fault set or report that recovery is not established. Outside that set, silent miscorrection may be possible; the name “ECC” does not eliminate it.

### A symbol is a group of bits, not necessarily a transferred word

Reed–Solomon codes operate on symbols, each representing a fixed-size group of bits. One wrong bit or several wrong bits within one symbol still count as one erroneous symbol. With `r` parity symbols, conventional bounded-distance decoding guarantees correction of up to `floor(r / 2)` symbols with unknown error locations. Known-location erasures have a different budget. [Riley and Richardson, Reed–Solomon properties and decoding](https://www.cs.cmu.edu/~realworld/reedsolomon/reed_solomon_codes.html).

The distinction matters when one physical event corrupts a group of neighboring bits. Twelve wrong bits contained in one code symbol and twelve wrong bits spread across several symbols create different demands on that decoder. Counting physical fault events, wrong bits, and wrong symbols are three different measurements.

LPDDR is a family of low-power DRAM interfaces. A data beat is one transfer unit on an interface. CLUE-ECC's description identifies a 12-bit beat and a mismatch with common Reed–Solomon symbol widths. It proposes pooling on-die and system parity, including the stated 16-bit on-die budget. [Official DAC description](https://63dac.conference-program.com/presentation/?id=RESEARCH676&sess=sess130). This description is not a substitute for the normative LPDDR6 specification or a standards-compliance assessment.

### Work through the alignment problem

Assume, for a constructed example, that consecutive 12-bit beats are placed in a linear bit sequence. Four beats occupy bits 0 through 47. Now divide that sequence into fixed 8-, 12-, or 16-bit symbols, all starting at bit zero:

| Beat's bit positions | 8-bit symbols touched | 12-bit symbols touched | 16-bit symbols touched |
|---|---|---|---|
| 0–11 | 0 and 1 | 0 | 0 |
| 12–23 | 1 and 2 | 1 | 0 and 1 |
| 24–35 | 3 and 4 | 2 | 1 and 2 |
| 36–47 | 4 and 5 | 3 | 2 |

If every bit in the second beat is corrupted, it affects two 8-bit symbols and two 16-bit symbols, but only one aligned 12-bit symbol. A code guaranteed to correct one unknown symbol error is sufficient for the last mapping, but does not guarantee correction for the first two. Interleaving or a different mapping would change the table and must be specified.

For an illustrative Reed–Solomon design, guaranteeing one unknown symbol correction requires two parity symbols. That is 16 parity bits with 8-bit symbols or 24 parity bits with 12-bit symbols. Guaranteeing two unknown 8-bit-symbol corrections requires four parity symbols, or 32 bits. These are mathematical budgets for the stated examples—not recovered CLUE-ECC code parameters or a proof that a particular device must use these layouts.

This explains the tension: a narrower symbol can save parity bits per symbol while allowing one physical fault to cross more symbols. A wider aligned symbol can contain the fault but require wider parity and arithmetic. The correct design target is the required physical-fault coverage after mapping, not the smallest symbol width in isolation.

### On-die and system ECC protect different parts of the path

“On-die” means inside the memory chip. System ECC is handled at a wider system boundary, commonly involving the memory controller. To determine their actual coverage, follow a write from the controller into the chip and a read back out, marking where each check is generated and where each decoder operates.

An error introduced after a check has already been verified cannot be prevented by that earlier verification alone. Similarly, an outer decoder receives the output of the inner processing, not necessarily the original physical error pattern. The three-bit example shows why this can matter: two raw flips can cause a local majority decoder to select the wrong codeword, changing what a later checker observes.

That is a conceptual example, not a claim that CLUE-ECC uses repetition coding or suffers that exact failure. A joint scheme needs to analyze the composed path: internal faults, transfer faults, parity faults, decoder outcomes, and any error-location information passed between stages. Separate guarantees for isolated components do not automatically prove the combined guarantee.

### Pooling parity requires useful, available checks

Two stored checks need not provide two independent pieces of information. For two data bits `a` and `b`, let both check bits equal `a XOR b`, where XOR is one exactly when its inputs differ. The second check merely repeats the first. Both `a,b = 0,0` and `a,b = 1,1` satisfy two zero checks, so the checks cannot distinguish those originals.

Joint parity design must therefore specify what relationships are checked, not just their total stored bit count. The decoder must also be able to obtain the needed redundancy at the time it makes its decision. Redundancy physically present inside a chip is not automatically visible to a system decoder.

Sharing or repurposing checks can change where computation occurs and how information crosses the interface. Those changes may affect reads, writes, partial updates, and error reporting. The recovered description does not provide the code equations, parity layout, or exchange protocol, so this writeup does not claim a specific algebraic construction or implementation.

### Read the savings with their measurement boundaries

The description states “33.3% on-die parity storage,” 14.83% area savings, and 24.18% power savings, with the same bandwidth impact as its comparison. The first phrase should not silently become a 33.3% reduction: using one third of a baseline and saving one third are different claims. The [evidence record](../observed-subthemes/memory-hierarchy-and-persistence.md#paper-dac-2026-research676) retains the source's wording and unresolved boundaries.

For a hypothetical 48-bit baseline, using one third means storing 16 bits, whereas reducing storage by one third means storing 32. Neither interpretation is assigned to the paper without its full accounting. Likewise, the area of a decoder, all ECC logic, a memory die, and a complete controller are different denominators. Reduced parity storage does not imply that the whole chip shrinks by the same percentage.

Equal bandwidth overhead also does not guarantee equal read latency, energy per request, or sustained throughput. For example, ten added decoder cycles at an assumed 1 GHz are ten nanoseconds even if no additional bits cross the interface. That calculation illustrates the distinction; it is not CLUE-ECC's clock or latency. A pipelined decoder might sustain the same request rate while increasing the delay of each request.

### What would establish the claimed protection

Fresh exact-name, manuscript, and artifact searches found the official description and a matching [author-lab publication listing](https://dates.yonsei.ac.kr/publications/conference), but no full manuscript. The actual error model, code parameters, controller changes, and measurement conditions remain unresolved. No normative standard, circuit implementation, or decoder has been verified here.

A useful validation would define the fault classes first, map each class into the protected codewords, and prove or exhaustively check the claimed small-fault guarantees. Fault injection should distinguish correct recovery, detected uncorrectable data, and silently incorrect output, including corruption of the parity and multiple faults outside the guaranteed set. Random testing alone cannot prove coverage of every supported pattern.

Then compare schemes at the same required protection level, data capacity, interface timing, and implementation conditions. Include both sides of the joint decoder, parity storage, metadata transfers, update handling, and power measurement activity. Otherwise, reduced cost could come from weakening the fault guarantee or moving uncounted work outside the reported block.

CLUE-ECC and adaptive flash read retry thus address two distinct parts of reliable storage. Retry changes the measurement used to obtain raw bits; coding uses redundancy to recover from specified errors in those bits. Either can reduce visible failures, but neither result can substitute for the other's fault model or recovery proof.

<span id="explanation-dac-2026-research1061"></span>

## OpenSUN: make cross-node memory behavior experimentally accessible

### The contribution is an experimental platform

A memory-system proposal may change the processor interface, network transport, address mapping, operating-system allocation, or several of these together. Studying only one component can miss the costs and correctness requirements imposed by the others. An experimental platform is useful when researchers can change a component and observe the consequences along the complete request path.

OpenSUN's official description presents an FPGA-based platform for this purpose, spanning controllers, switches, protocols, and software. It does not present a numerical performance comparison. [DAC description](https://63dac.conference-program.com/presentation/?id=RESEARCH1061&sess=sess147). An FPGA is a chip whose digital logic can be configured after manufacture, allowing hardware designs to be changed without fabricating a new custom chip.

Public repositories have now been recovered. The root documentation describes synchronous cross-node load/store access, asynchronous DMA, and separate hardware, kernel, and userspace components. [Pinned root repository](https://github.com/memory-of-star/OpenSUN/tree/ffa257f9ec39edc86af4113b4b2721fc2f11c462). The updated evidence card records the documented platform; these are source-inspection findings, not a claim that the hardware has been built or operated here.

### Follow a remote read and its response

A load requests the value stored at an address; a store requests an update. When the address refers to memory reached through another node, the system must translate that operation into transport requests and return the result to the correct requester. A node here is one participating computer or hardware endpoint, not necessarily an entire rack or commercial server configuration.

The FPGA documentation connects host requests, network requests, and a traffic generator through an internal crossbar to local memory, host memory, or the network. A crossbar routes requests among several input and output ports. [FPGA README, Sections 2–4.1](https://github.com/memory-of-star/OpenSUN-FPGA/tree/a18c22c08606fb40e6fe1a16a48dd9c1a7babc97).

To understand such a path, consider a hypothetical read from node A to memory attached to node B. A mapping identifies the destination and address. A's controller issues a request carrying enough identity to match the eventual response. The network transports it; B accesses the target memory and returns data or an error. A completes the original operation only after the applicable response and ordering conditions are met.

This sequence is a conceptual decomposition, not a recovered packet format. It identifies what a complete measurement needs to include: request handling, network traversal, destination memory service, return traversal, and completion. Reporting only link transmission time omits most of those steps.

### Direct access does not make remote memory local in cost

Suppose an illustrative remote read spends 0.2 microseconds in request handling, 0.3 traveling outward, 0.1 at memory, 0.3 returning, and 0.1 completing. Total latency is one microsecond. If each result supplies 64 useful bytes and the program waits for that result before issuing the next request, useful bandwidth is at most 64 megabytes per second under this model.

Now allow 32 independent requests in flight. The latency-based bound becomes `32 × 64 bytes / 1 microsecond = 2.048 gigabytes per second`, before link, controller, and memory limits. The same hardware latency can therefore produce very different bandwidth depending on available concurrency. A pointer-following workload whose next address comes from the previous result cannot automatically exploit that concurrency.

These numbers are not OpenSUN results. They explain why a streaming traffic generator and an application with dependent accesses answer different questions. Both can be useful tests, but their bandwidth figures should not be presented as interchangeable.

### Address routing and response identity are different mappings

An address identifies where a request should go. A transaction identifier distinguishes outstanding requests and allows responses to return to the right source. If two sources reuse the same local identifier, the fabric must preserve enough source information to distinguish them.

The inspected crossbar declaration defaults include a 64-bit address, 12-bit identifier, and source masks `0x000`, `0x400`, `0x800`, and `0xc00`. [Selected source declarations](https://github.com/memory-of-star/OpenSUN-FPGA/blob/a18c22c08606fb40e6fe1a16a48dd9c1a7babc97/OpenSUN_IO_Controller/axicb_top_split.sv#L4). This is a header inspection, not verification of the instantiated design or all parameter overrides.

As an illustrative interpretation of separate source bits, local identifier 7 could be represented as `0x007` for one source and `0x407` for another. A correct design must preserve the distinction until the response is routed back, while avoiding identifier reuse that collides with an outstanding transaction. The example does not establish that every source can safely issue 1,024 requests; buffer limits, protocol rules, and allocation logic impose additional constraints.

### Software exposure is part of the experiment

The OS documentation describes ConfigFS-based memory-node management and distinguishes a full kernel installation from loading only the register-management module. The tools repository contains a control utility and C library. [Pinned OS documentation](https://github.com/memory-of-star/OpenSUN-OS/tree/15ef865106144e9e075c2d869da0bcc65d9aed97), [pinned tools](https://github.com/memory-of-star/OpenSUN-Tools/tree/1dd8e92a2dec3af362a114ab29789d20e72b3044).

Making a range visible to an operating system requires more than transporting a read. Software must know which physical addresses are valid, which allocation policy may use them, and whether existing allocations can be removed safely. NUMA, or non-uniform memory access, describes memory regions whose access costs depend on location; describing a range as a NUMA node does not make its physical delay disappear.

Similarly, a command successfully writing a device register is not proof that an application can allocate and use remote memory. Tests should distinguish device discovery, configuration, mapping, allocation, read/write correctness, and behavior when memory is removed. Kernel installation or memory hotplug should not be attempted on an unrelated working machine merely to check that the repository exists. No such changes were made here.

### Load/store access alone does not establish coherence or ordering

If two processors cache copies of the same value, coherence concerns how their copies are kept consistent when writes occur. Ordering concerns which observations are allowed across multiple operations. Exposing a remote address does not by itself specify either contract.

For a conceptual test, a writer stores `data = 42` and then publishes `ready = 1`. A reader waits for `ready` and then reads `data`. Whether seeing `ready = 1` guarantees seeing 42 depends on the synchronization operations, compiler rules, processor memory model, and interconnect behavior. An ordinary unsynchronized program cannot establish that guarantee by assertion.

The platform needs an explicit supported contract and tests written for that contract. Likewise, an Ethernet transport in an implementation does not imply that every listed scale-up protocol is implemented or that the system reproduces a commercial coherence domain. The current inspection does not establish those properties.

### The documented deadlock warning changes the usable experiment space

The FPGA README warns that simultaneous high-throughput mutual access to host memory can deadlock because of a CXL-IP dependency restriction. [Host-memory target warning, Section 4.1](https://github.com/memory-of-star/OpenSUN-FPGA/tree/a18c22c08606fb40e6fe1a16a48dd9c1a7babc97). This is a documented limitation, not a reproduced failure or a claim that every bidirectional operation fails.

A simple abstract deadlock has two resources: A retains resource X while waiting for Y; B retains Y while waiting for X. Neither can progress without the other releasing its resource. Adding faster links does not remove that dependency cycle. This example explains the class of failure, not the exact internal cycle of the OpenSUN design.

A stress test must therefore identify the target memory type and traffic directions. One-way access to a remote target cannot demonstrate unrestricted bidirectional host-memory progress. If an experiment avoids the warned configuration, its conclusion must retain that restriction. A timeout can reveal lack of progress but does not by itself repair the outstanding operations safely.

### What an FPGA platform can prove—and what still needs measurement

Executing a design in configurable hardware can reveal interactions between real software, finite buffers, and concurrent hardware operations. Its clock rates, resource mapping, and memory/link interfaces may differ from a custom chip. Multiplying an FPGA result by a clock ratio is not sufficient to predict a fabricated system when some delays do not scale with that clock.

A useful report would publish exact source revisions, generated hardware configuration, software build, node connections, memory types, request sizes, outstanding-request limits, and traffic patterns. It would check correctness before comparing latency and bandwidth, and separate unrestricted supported configurations from known exclusions. An injected delay can test sensitivity to that delay; it does not establish fidelity to all behavior of another network.

The recovered root revision pins FPGA `a18c22c`, OS `15ef865`, and Tools `1dd8e92`, linked above. Documentation and selected declarations were inspected; no build, kernel installation, device access, workload run, or protocol validation occurred. Correspondence to the final conference artifact remains unverified. The [current reading card](../observed-subthemes/memory-hierarchy-and-persistence.md#paper-dac-2026-research1061) preserves those limits and the earlier description-only capture.

OpenSUN's potential contribution to the broader atlas is experimental access: it may let placement, protocol, and software hypotheses be tested together. That is distinct from proving that a particular scale-up architecture is faster or that a long-term trend has been established.

<span id="explanation-dac-2026-research1081"></span>

## KEEP: reusing a model's computation when remembered facts change

### Textual memory and model state are not the same thing

An embodied planner chooses actions using a task instruction and information about its environment. Between actions, that information can change. An object may have moved, an action may have failed, or a previously unknown location may have been observed. The next decision should use the revised information.

There are two distinct things to store. One is the record itself, such as an object's location. The other is the numerical state produced when a language model processes that record. Storing the record avoids forgetting the observation. Storing the numerical state can avoid repeating computation. But the second is reusable only under conditions imposed by the computation that produced it.

In a transformer, each layer transforms the current representation of a token into a query, key, and value. A query is compared with keys to determine attention weights; those weights combine the corresponding values. A token is a unit of model input, not necessarily a complete word. A layer is one stage in the model's sequence of transformations. Later layers operate on representations already influenced by earlier attention operations.

The KV cache stores keys and values. It is not a cache of final answers, and it is not the same as the model's learned weights. Reusing KV can save prompt-processing work, called prefill. Time to first token, or TTFT, measures the wait before the model starts producing its response. It does not include all subsequent action execution.

### Why unchanged text can still have an invalid cached representation

Consider a causal model: a token can use preceding tokens but not future ones. Suppose a prompt contains record A followed by record B. In higher layers, B's representation may depend on A through attention. Changing A can therefore change B's correct representation even if B's text remains identical.

To isolate this dependency, use an illustrative calculation, not a transformer implementation: let A supply the number 2, let B supply 3, and let the contextual representation of B be their sum, 5. If A becomes 7, the correct sum becomes 10. A cache indexed only by B's unchanged value of 3 would wrongly reuse 5. The dependency changed even though the local input did not.

Exact reuse consequently needs more than a matching piece of text. Relevant preceding context, positions, attention rules, model parameters, and numerical configuration must remain compatible. Adding a suffix to an unchanged causal prefix differs from editing the middle of that prefix. Likewise, computing two blocks separately and joining their caches does not automatically reproduce computing the concatenated text together.

This is why cache validity matters separately from cache capacity. More memory can retain more states, including states that are no longer appropriate. A high hit rate does not establish correct planning.

### Smaller groups reduce the cost of an update but remove interactions

KEEP groups stable records together and computes changing records separately. A ten-step unchanged interval controls the stable classification. [Manuscript v2, PDF pp. 3–4, Section 4.1](https://arxiv.org/pdf/2602.23592v2#page=3).

The tradeoff can be understood without assuming the grouping algorithm is perfect. Imagine four records of 100 tokens each. If the first changes and the four were cached as one causally connected unit, as many as 400 token positions may need reconsideration. Separate record caches could limit rebuilding the changed record to 100 positions. These counts illustrate affected input positions, not a fourfold runtime guarantee: attention work, cache transfer, and reconstruction of interactions have their own costs.

Separation also changes what was computed. If record B needs information from record A, B's independently produced cache omits that contextual contribution. Making every group smaller can therefore reduce update work while making the cached state a poorer approximation to joint processing.

Conversely, grouping records that rarely change can preserve useful interaction within the group. The saving depends on future stability, not merely past stability. An object remaining stationary for ten steps does not prove that it will remain stationary at step eleven. A sound implementation must detect an update and change the affected state; the historical stability label is not permission to ignore new evidence.

There is also a transition cost. If rebuilding a group costs six milliseconds and avoids one millisecond on each later request, six requests only recover that cost in an otherwise unchanged toy system. Frequent changes between grouping modes could consume the benefit. These are explanatory numbers, not KEEP timings.

### Why choosing only directly relevant records can miss a dependency

Suppose the instruction is to collect an object. One record identifies its container; another identifies the container's location. The second can matter because the first matters, even if its wording has little direct similarity to the instruction. This is a dependency within the planning task, not an analogy.

KEEP repeatedly updates record-importance scores using attention from a selected relevant set, then recomputes selected records at the next layer. [PDF p. 4, Section 4.2](https://arxiv.org/pdf/2602.23592v2#page=4).

For a numerical illustration of indirect importance, let direct scores for records A, B, and C be 0.8, 0.1, and 0.1. Selecting one record initially chooses A. If A's attention to those records is 0.1, 0.8, and 0.1, the next selection chooses B. B was weakly selected directly but strongly connected to the initially relevant record. This example illustrates propagation only; it is not a recovered KEEP execution trace.

Attention-based importance remains a numerical selection rule, not a proof that the selected statements form a valid logical argument. A needed fact can receive a low score; a strongly attended record can be irrelevant or incorrect. Recomputing selected states also cannot recover an observation that was never retrieved.

A stopping rule needs scrutiny too. A selected set becoming unchanged is a fixed point of the selection procedure, not proof of planning correctness. Iteration is not automatically convergent: if A points only to B and B points only to A, a top-one update alternates forever. This constructed counterexample does not show that KEEP encountered a cycle. It identifies a reproduction question: verify iteration limits, tie handling, and cycle behavior in the implementation instead of assuming that every attention matrix stabilizes.

### Why doing less computation can expose more transfer time

Recomputing a state uses execution resources. Reusing a state stored in host memory requires loading it to the GPU. Avoiding one kind of work can increase dependence on the other.

KEEP discards a record's intermediate state once it stops recomputing that record; subsequent layers must reuse its caches. It uses early transfer slack to preload those future caches. [PDF pp. 4–5, Section 4.3](https://arxiv.org/pdf/2602.23592v2#page=4).

The consequence of discarding the intermediate state is important. Computing a new state at layer five generally requires its input from layer four. Keeping only an old key and value does not necessarily retain everything needed to reconstruct that input. Restarting computation later would require additional retained state or repeated earlier work. The restriction is a system design choice, not a theorem that the record has become permanently unimportant.

Consider a simplified schedule. An early computation takes four milliseconds; loading the immediately next layer's required data takes one. If the transfer engine would otherwise sit idle, there are three milliseconds available for data needed farther ahead. Assume a later layer needs a three-millisecond transfer and its immediate predecessor provides only one millisecond of computation to overlap it. A next-layer-only schedule exposes two milliseconds of waiting; an early preload can remove that wait if the future data is already known, buffers are available, and no other critical transfer is delayed.

None of the transfer bytes disappeared. Their timing changed. Loading future data too early can occupy scarce GPU space or delay nearer work. A complete timing analysis must include those resource constraints and the point at which the decision becomes available, not merely add nominal compute and transfer rates.

### What the reported numbers mean

The evaluation uses ALFRED/WAH-NL, Qwen-2.5 14B/32B, and one A6000; 32B uses INT4 weights. For ALFRED 32B, CacheBlend and KEEP respectively report 41.37%/45.50% success and 1.209/0.635-second TTFT. The 2.68× full-recomputation comparison is the 40-segment case. [PDF pp. 5–6, Table 1 and Figure 9](https://arxiv.org/pdf/2602.23592v2#page=5).

From the table, the success-rate difference is `45.50 − 41.37 = 4.13 percentage points`. Relative to 41.37%, that is approximately 9.98%, not 4.13%. Likewise, `1.209 / 0.635 ≈ 1.90` is a latency ratio; the corresponding reduction in waiting time is approximately 47.5%. Stating the denominator prevents superficially similar percentages from being confused.

A faster first response is not automatically a proportionally faster completed physical task. In an illustrative action cycle with one second of planning and nine seconds of execution, halving planning produces a 9.5-second cycle, only about 1.053× faster overall. Failed actions and replanning can further change the total. This example is not a reconstruction of ALFRED timing.

### The artifact still needs accuracy–latency equivalence checks

The matching title and authors connect the preprint to the [DAC program entry](https://63dac.conference-program.com/presentation/?id=RESEARCH1081&sess=sess137), but final-proceedings equivalence has not been established. The public repository, inspected at revision `493388b11e9cbbe0b323a4eb770e2b9bd0a25ed7`, explicitly separates Transformers-based accuracy evaluation from vLLM-based latency evaluation and requires different environments. [Pinned README, installation section](https://github.com/PKU-SEC-Lab/KEEP_Embodied_Memory/blob/493388b11e9cbbe0b323a4eb770e2b9bd0a25ed7/README.md#install).

Separate implementations can be useful, but combining their results requires checking that they make equivalent selections and updates. Reproduction should compare model and tokenizer revisions, prompts, retrieved records, grouping transitions, recomputation decisions, positional handling, numerical precision, and output behavior. Otherwise, the measured speed and measured success might describe different effective methods. README inspection alone neither proves nor disproves that equivalence.

No model or planner was executed here. The [current evidence card](../observed-subthemes/memory-hierarchy-and-persistence.md#paper-dac-2026-research1081) now identifies the recovered source; historical capture remains available. The broader lesson is a testable dependency between reuse, update scope, and computation placement—not an established claim that every agent should use this design.

<span id="explanation-dac-2026-research1028"></span>

## Ctxmem: who handles a memory access when the data is on flash?

### An addressable capacity is not a uniform access cost

A program issues a load to obtain a value or a store to change one. Its address identifies the requested bytes. That interface does not specify how the machine ultimately obtains them. A requested value might already be in a processor cache, be fetched from DRAM, or require a much longer operation behind a memory-expansion device.

DRAM is working memory; an SSD supplies storage through a controller and flash media. Combining the two can provide a fast resident subset backed by a larger capacity. The combined system still needs to identify which data is resident, fetch absent data, and preserve modified data before reusing its space. A byte-addressable interface does not make every physical transfer one byte long or give flash the service time of DRAM.

For example, if an eight-byte load causes a 4,096-byte page to be fetched, the transfer supplies 512 times the immediately requested bytes. If subsequent loads use the rest, that larger transfer can be worthwhile. If none do, most transferred bytes provided no immediate application benefit. These are constructed sizes, not Ctxmem's recovered page or transfer sizes.

The DAC description identifies Ctxmem as an OS–hardware design combining CXL, DRAM, and flash. Its stated components are asynchronous page-fault handling with device-side data movement, a dynamic direct-mapped cache, and hardware access profiling. [Official description, first two paragraphs](https://63dac.conference-program.com/presentation/?id=RESEARCH1028&sess=sess162). A full manuscript was not recovered, so the following explains the necessary concepts and obligations without inventing its exact implementation.

### A page fault is a request for resolution, not necessarily a program error

A virtual address belongs to the address space presented to a program. The processor uses translation information to determine the backing location and allowed operations. A page is a range managed as a unit by that translation system. If a required mapping is absent or does not allow the access, execution can enter a page-fault handler.

Some faults are legitimate parts of memory management. The system may need to obtain a valid page before allowing the instruction to continue. Other faults are invalid accesses and must not be converted into successful reads. This distinction matters when fault handling is moved partly into hardware: faster service cannot replace permission checking.

A cache miss inside a device and a processor-visible page fault are also different events. The former says that a particular internal copy is absent. The latter arises from address translation or access control. Connecting them requires a defined mechanism. The description does not expose enough detail to establish how Ctxmem creates, communicates, and resolves each kind of event.

### Asynchronous handling does not let an instruction use missing data

An operation is asynchronous when its initiation and completion are separated, allowing some other activity between them. That does not remove the dependency of a load on its result. The thread needing an absent page may still wait while another thread, the operating system, or a device performs useful work.

Imagine that serving a fault involves ten microseconds of host processing, a 100-microsecond storage operation, and ten microseconds of completion work. Serial elapsed time is 120 microseconds. If an offload reduces the host work to two microseconds at each end, elapsed time becomes 104 microseconds under this simplified model. Host processing falls from 20 to four microseconds, an 80% reduction, while elapsed time falls by only about 13.3%. These are not Ctxmem measurements.

With many independent requests, freeing host processing can improve throughput even when each request still waits substantially for storage. With only one dependent request at a time, that concurrency benefit may be unavailable. Neither behavior can be inferred from the word “asynchronous” alone.

### Moving the bytes and publishing the mapping are separate responsibilities

The data movement portion obtains the page contents and places them at their destination. Other responsibilities include deciding whether the access is allowed, reserving destination space, preventing conflicting changes, and announcing that the page is safe to use. Calling the first portion a data plane does not imply that a device independently owns all those decisions.

A conceptual fill has a dependency sequence:

| Stage | Required condition before proceeding |
| --- | --- |
| Accept the request | The requested range and permissions are valid. |
| Reserve a destination | Its old contents are no longer needed there, or have been preserved. |
| Transfer the page | Readers cannot mistake incomplete contents for a valid resident page. |
| Publish availability | Data and mapping metadata describe the same completed version. |
| Resume waiting work | The instruction can access the intended bytes under the intended permissions. |

This is a correctness checklist, not Ctxmem's recovered state machine. Two threads faulting on the same page may require shared completion handling; two competing fills must not overwrite each other's destination. If the program unmaps an address while a transfer is pending, a late completion must not publish obsolete data into a newly assigned mapping.

Linux's userfaultfd documentation gives a concrete, separate example of the publication obligation: its page-delivery operations prevent a reader from seeing a partly populated page and normally wake blocked faults after resolution. [Kernel documentation, “Resolving Userfaults”](https://docs.kernel.org/admin-guide/mm/userfaultfd.html#resolving-userfaults). This supports the explanation of atomic visibility; it is not evidence that Ctxmem uses userfaultfd or follows that API.

### Direct mapping makes lookup simple but can waste available capacity

A direct-mapped cache gives each backing item one eligible slot under the current mapping. The controller can calculate that slot and check its tag, which identifies the stored item. If two frequently used items map to the same slot, they cannot remain resident together under that mapping even when other slots are empty.

Consider four slots with the illustrative rule `slot = page number modulo 4`. Pages 0 and 4 both map to slot 0. Starting empty, the access sequence `0, 4, 0, 4, 0, 4` misses six times if each request replaces that slot. Slots 1–3 remain unused. The requested set has only two pages, smaller than the cache capacity, yet conflicts prevent reuse.

If a different placement allowed the two pages to occupy distinct slots, the same sequence could incur two initial misses followed by four hits. This is a comparison between toy placement rules, not a claim about Ctxmem's dynamic mapping algorithm. The word “dynamic” leaves important questions unanswered: what changes, how the new location is found, what metadata is needed, and how an in-flight access survives a mapping change.

Remapping also has a cost. Suppose rearranging data costs 20 microseconds and prevents a five-microsecond miss on each later reuse. Four avoided misses merely repay the move. A rapidly changing workload may not provide enough reuse before the next rearrangement. A better utilization percentage is therefore insufficient without movement and lookup costs.

### Access profiling observes the past; placement spends resources on the future

A hot page is one expected to be used enough to justify fast-memory space. Hardware profiling can count or sample accesses, but a counter is an observation over a particular interval, not direct knowledge of the next interval.

Suppose page A receives 100 accesses in one interval and none in the next, while page B goes from zero to 100. A cumulative policy may retain A too long. A short recent window adapts more quickly but can respond to brief bursts that never repeat. Comparing policies therefore requires the observation window, sampling rate, update cost, and behavior when the workload changes.

Raw access counts can be misleading too. Ten avoided misses saving two microseconds each are worth 20 microseconds of serial waiting in a toy calculation; five avoided misses saving ten each are worth 50. A frequency-only choice favors the first page even though the second offers more saved time under those assumptions. Overlap and interference can change the comparison again.

Profiling and migration need to be evaluated together. A perfectly accurate classification arriving after the relevant accesses is not useful for those accesses. A timely but noisy classification may still help, provided its unnecessary transfers do not displace more valuable work.

### Modified pages add correctness, traffic, and endurance questions

A clean cached page matches its backing copy and can potentially be discarded. A dirty page contains modifications not yet reflected in that copy. Reusing its slot without preserving those modifications loses data. Preserving them generates traffic and may require waiting for another resource.

In a constructed example, an application changes eight bytes in each of 100 otherwise separate pages. If eviction writes 4,096 bytes per page, it transfers 409,600 bytes for 800 bytes of application changes: a ratio of 512. This describes a hypothetical page-write policy, not flash's internal physical write amplification and not Ctxmem's actual policy. Flash management may add further writes; coalescing could reduce repeated writes. Neither behavior is established by the description.

Preserving dirty data during normal eviction is also distinct from guaranteeing durability after power loss. A value copied into volatile device DRAM may still disappear on failure. A persistence claim needs a completion contract, failure model, and recovery test beyond ordinary read/write correctness.

### The evaluation claim remains simulation-backed and condition-incomplete

The official description reports gem5 evaluation, a 1.4× execution-time improvement, and doubled throughput against conventional CXL-SSD. It does not specify the benchmark suite, simulator configuration, or aggregation behind those figures. [Official description, final paragraph](https://63dac.conference-program.com/presentation/?id=RESEARCH1028&sess=sess162).

The bounded conclusion is therefore OS–hardware co-designed CXL tiered-memory evaluation, not demonstrated general end-to-end memory-system improvement. The result still needs workload-level latency distributions, migration and page-fault counts, queue and bandwidth accounting, dirty-page behavior, energy, endurance, and a real-device check before the two headline ratios can be treated as portable system gains.

If “1.4×” means baseline time divided by proposed time, a 140-second baseline becomes 100 seconds: a 28.6% time reduction, not 40%. That interpretation needs the missing measurement definition. A 2× throughput result can coexist with a smaller single-job speedup if concurrency, host utilization, or workload mix differs, but those are possible explanations, not recovered experimental conditions.

A useful reproduction would separately measure fault detection, host processing, queueing, flash service, page transfer, mapping publication, and application progress. It would vary working-set size, conflict-heavy addresses, dirty-page frequency, concurrent faults, and workload changes. Device queues, DRAM capacity, link bandwidth, storage timing, and simulated operating-system paths need explicit configurations. The name of a simulator alone establishes none of those choices or their agreement with hardware.

Exact-title and author searches, including [Kan Zhong's older publication page](https://zhongkan.github.io/), did not recover the manuscript or artifact in this pass. An unrelated software package with the same name is excluded. The [evidence card](../observed-subthemes/memory-hierarchy-and-persistence.md#paper-dac-2026-research1028) therefore remains description-backed; there are no paper-page locators to supply honestly. No kernel changes, memory migration experiment, or simulator run was performed here.

Ctxmem and RememTier both concern hybrid memory capacity, but that alone does not make their gains comparable. The useful joint question is whether access granularity, placement, and ownership of migration reduce total application waiting under the same capacity and workload. Answering it requires the missing conditions and a common experiment, not combining their headline ratios.

<span id="explanation-dac-2026-research270"></span>

## 3D-ReSAC: nearby memory still needs refresh and communication

### Why a small batch changes the balance between arithmetic and movement

A linear model layer multiplies an input by a matrix of weights. For one input vector and a matrix with `M × N` entries, it performs approximately `2 × M × N` arithmetic operations when multiplication and addition are counted separately. If each weight occupies two bytes and must be fetched once, weight traffic alone is `2 × M × N` bytes. That is about one operation per byte moved, before input and output traffic.

If eight input vectors can share one fetched copy of the matrix, arithmetic rises eightfold while that weight traffic can remain the same. The idealized ratio becomes eight operations per weight byte. This assumes sufficient local storage and a schedule that actually reuses the weights; batching does not guarantee it. The example explains why a low-batch workload can demand considerable memory traffic without using all available arithmetic capacity.

Placing processing near stacked DRAM can shorten some transfers and expose more parallel memory access. It does not remove the need to maintain the stored bits or exchange results between processing regions. Those are the two overheads addressed by the official 3D-ReSAC description: sequential refresh-skip and ArrowMesh communication. [DAC description, problem and method paragraphs](https://63dac.conference-program.com/presentation/?id=RESEARCH270&sess=sess116).

### Refresh preserves a physical state, not a software copy

A DRAM cell represents data using stored electrical charge, which leaks over time. Refresh restores the state before leakage makes the stored value unreliable. Accessing a row involves sensing and restoring its cells; refresh also consumes memory resources that may otherwise serve requests. [RAIDR, PDF pp. 1–2, introduction and DRAM background](https://istc-cc.cmu.edu/publications/papers/2012/raidr-isca12.pdf#page=1). This older paper supports the physical explanation, not 3D-ReSAC's unrecovered policy or hardware assumptions.

Skipping refresh is safe only if the required data remains valid until it is restored again or is no longer needed. Several distinct arguments could support a skip: a qualifying operation has already restored the row, the data will be overwritten before it is used, or validated retention information permits a longer interval. These are possible classes of justification, not claims about which one 3D-ReSAC implements.

An ordinary processor cache hit does not establish that a DRAM row was recently restored: the request may never reach DRAM. Similarly, accessing one row says nothing about an untouched row. A correct skip decision must track the physical event that matters, at the granularity it actually protects.

### The worst gap matters more than the average access frequency

Use a deliberately simplified retention model: a row must be restored within ten milliseconds of its previous restoration. Restorations at times 0, 8, and 16 milliseconds have eight-millisecond gaps. Removing the middle event creates a sixteen-millisecond gap and violates the model. Conversely, an independent qualifying restoration at time 7 could make a separately planned event at time 8 redundant, provided the next event still meets the deadline.

These are illustrative deadlines, not a DRAM specification. The important quantity is the largest gap for each affected row. A region accessed heavily for one second and then left idle can have a high average access count while containing rows overdue for refresh.

Retention characterization itself needs margins and appropriate operating conditions. Primary retention research identifies dependence on stored data patterns and variation over time. [Authors' retrospective, abstract](https://arxiv.org/abs/2306.16037). A past successful test is therefore not automatically a permanent bound for every cell and temperature. The missing 3D-ReSAC manuscript must establish its particular correctness argument; the phrase “refresh-skip” is not that argument.

### Sequential control can save metadata only under a usable access structure

Keeping one status bit for each of one million rows takes 125,000 bytes. A single pointer into that range needs only 20 bits. That arithmetic explains why replacing per-row state with a compact sequential description could save storage—but the pointer cannot describe every possible subset of restored rows.

For example, one boundary can represent “all rows before this position have been handled.” It cannot, without extra state or restrictions, represent arbitrary holes caused by skipped, reordered, or interrupted accesses. A compact design must either exploit a real ordering property, record exceptions, or conservatively perform extra work.

This is an information-representation tradeoff, not a reconstruction of 3D-ReSAC's controller. Its title does not establish whether it uses a pointer, bitmap, counter, or another scheme. To evaluate the claimed area efficiency, the missing evidence needs actual state size, control logic, timing, and behavior when the assumed sequence is disrupted.

### Partitioning a matrix determines which results must move

Suppose two processing regions split the columns of a weight matrix. Each has different weights and the corresponding part of the input. They compute partial outputs that must be added to obtain the full result.

For a concrete dot product, let weights be `[1, 2, 3, 4]` and input be `[5, 6, 7, 8]`. The first region computes `1×5 + 2×6 = 17`; the second computes `3×7 + 4×8 = 53`. The required output is 70. Producing 17 and 53 locally is not completion: some communication and addition must combine them.

A reduction combines contributions into a result. An all-reduce additionally makes the combined result available to every participating region. Whether all regions need it depends on where the next operation runs. A row-wise matrix partition has different requirements: each region can compute complete but different output elements, while it may need the entire input. Placement can therefore exchange output-combination costs for input-distribution costs.

These are mathematical consequences of partitioning, not recovered ArrowMesh routes. The name alone does not establish its links, routing rules, collective schedule, buffering, or deadlock avoidance.

### High link utilization is useful only when it advances required work

If 64 megabytes of required data must cross a network cut whose aggregate usable bandwidth is 16 gigabytes per second, transmission across that cut takes at least four milliseconds, using decimal units. Adding links elsewhere does not change this bound. Improving routing can help if it reduces unnecessary crossings or uses available capacity at the constrained cut.

Utilization measures how busy a resource is over an interval. A link can be fully busy carrying duplicated data, retransmissions, or work that is not delaying completion. Conversely, a short critical transfer can matter even when average utilization is low. A communication comparison should measure useful completed collectives and application latency alongside link occupancy.

Numerical correctness also needs attention. Changing a reduction order can change floating-point rounding even when exact real-number sums are equal. A performance result should retain its arithmetic precision and output-quality checks instead of assuming every schedule is bit-identical.

### The two overhead reductions cannot simply be added

Consider a hypothetical 100-millisecond execution with 70 milliseconds of other work, ten of exposed refresh delay, and twenty of exposed communication delay. Eliminating the refresh delay and halving communication gives `70 + 0 + 10 = 80` milliseconds, or 1.25× speedup. It does not produce a 150% total-time reduction by adding the component percentages.

Even this calculation assumes disjoint exposed delays. If communication already overlaps refresh, independently counted savings can refer to the same waiting interval. Faster memory service can also move the limiting resource to the network. Joint evaluation must measure the new schedule, not sum isolated optimizations.

The official description reports 7–100% lower refresh overhead, 53–75% lower communication overhead, and latency ratios of 1.12–2.02× across unspecified low-batch workloads. [DAC description, results paragraph](https://63dac.conference-program.com/presentation/?id=RESEARCH270&sess=sess116). A 100% overhead reduction does not establish that refresh is physically unnecessary indefinitely; it may concern a bounded measured cost whose definition is unavailable. Nor should the largest values from separate ranges be assumed to come from one configuration.

### What remains necessary to judge the proposal

A reproducible assessment needs model names, batch and sequence sizes, numerical formats, matrix partitioning, stack organization, process assumptions, refresh deadlines, temperature conditions, and link topology. Refresh safety requires per-row timing or an equivalent proof under the supported execution model. Communication needs correctness and progress tests under the same partitioning used for latency measurement. Area and power claims need their own implementation evidence.

Fresh exact-name and author/topic searches recovered the official description, not a full manuscript or artifact. The [current evidence card](../observed-subthemes/memory-hierarchy-and-persistence.md#paper-dac-2026-research270) remains description-backed. No paper pages, controller algorithm, device test, or network simulation are claimed here.

The connection to the wider chapter is specific: moving computation closer to stored weights can expose maintenance and inter-region dependencies that were previously less visible in total runtime. That is a testable design interaction, not proof that every low-batch model benefits from this architecture or that its ratios transfer to another stack.

<span id="explanation-isca-2026-program-004"></span>

## Cerberus: making several error decoders cooperate

### Extra bits help only through a defined relationship to the data

An error-correcting code stores a constrained representation of the data. Some bit strings are valid codewords; others are not. A decoder uses these constraints to detect inconsistency and, within a specified error model, identify the original value. Redundancy is the extra stored information that makes those constraints possible.

For a simple example, store data bits `a` and `b` with `p = a XOR b`. XOR is addition modulo two: equal bits produce zero and unequal bits produce one. The valid triples are `000`, `011`, `101`, and `110`. Checking `a XOR b XOR p` yields zero for every valid triple.

If one bit flips, that check becomes one, revealing an error. But it does not identify which bit flipped: all three single-bit possibilities produce the same check result. If two bits flip, the check returns zero and the corruption can be missed. Adding a check is therefore not equivalent to obtaining arbitrary correction capability.

### A syndrome records which constraints fail

A syndrome is the collection of check results. Each possible single-bit error has a syndrome determined by the checks that include that bit. If two locations have identical syndromes, the decoder cannot distinguish their single-bit errors from those observations alone.

Consider an illustrative three-bit repetition code with valid words `000` and `111`. Use checks `x1 XOR x2` and `x2 XOR x3`. Starting from `000`, a flip in bit 1 produces syndrome `10`; bit 2 produces `11`; bit 3 produces `01`. The distinct syndromes allow single-bit correction.

Now flip bits 1 and 2, producing `110`. Its syndrome is `01`, the same as a single flip in bit 3. A decoder assuming one error flips bit 3 and produces `111`, a valid but wrong word. It has increased the distance from the original from two wrong bits to three. This is a miscorrection, not merely a failure to detect an error.

The example explains why placing two decoders in sequence does not automatically combine their correction strengths. The second receives the first decoder's output, including any new damage it introduced.

### Fault location determines which decoder can observe it

On-die protection operates inside the memory device. Link protection concerns transmission. System protection is checked at the controller. A fault introduced after an on-die decoder has finished cannot be corrected by that earlier invocation. Conversely, a write-path fault detected before storage can potentially be retried before it becomes stored corruption.

Cerberus uses shared redundancy across write-link detection/retry, on-die read correction, and controller recovery. Its 32-bit-redundancy configuration protects 256 data bits in a 288-bit codeword. [Preprint v1, PDF p. 7, Section V-B](https://arxiv.org/pdf/2605.02220v1#page=7).

The stages have different opportunities. Retransmission requires a trustworthy source copy and a recoverable transfer failure. Stored corruption may lack that source. Retrying a permanent fault can repeatedly return bad data, so a retry policy needs an eventual failure outcome rather than assuming every retry succeeds.

### Containing a local mistake can preserve system-level recoverability

Cerberus constrains on-die miscorrection for errors within one 16-bit symbol to that symbol; the controller corrects one symbol or two bit errors. [PDF pp. 7–8, Sections V-B and V-C](https://arxiv.org/pdf/2605.02220v1#page=7).

A symbol is a defined group of bits treated as one unit by a code. To see why containment matters, use three illustrative four-bit symbols initially equal to `0000 | 0000 | 0000`. A fault produces `1100 | 0000 | 0000`. If a local decoder wrongly changes another bit in the first symbol, producing `1110 | 0000 | 0000`, more bits are wrong but only one symbol is affected. A downstream code capable of correcting any one symbol still has an applicable guarantee.

If instead the local decoder changes the second symbol, producing `1100 | 1000 | 0000`, two symbols are affected. The same downstream single-symbol guarantee no longer applies. The issue is the shape of residual errors, not only their bit count.

This toy example is not a Cerberus codeword or decoder run. It also does not extend a single-region containment argument to arbitrary simultaneous faults across regions. A complete guarantee must state which input error patterns it covers and prove that earlier stages keep those patterns within the later stage's correction set.

### Sharing parity requires compatible constraints

The manuscript requires device checks to be linear combinations of system checks. [PDF p. 8, Section V-C3](https://arxiv.org/pdf/2605.02220v1#page=8).

Here is the meaning without assuming familiarity with matrix algebra. Suppose the system enforces two equations: `a XOR b XOR p = 0` and `b XOR c XOR q = 0`. XORing the equations cancels the two copies of `b`, giving `a XOR c XOR p XOR q = 0`. Every word satisfying both original equations necessarily satisfies this derived check.

An intermediate device can therefore use the derived check without requiring a new independent parity bit. But one derived check cannot distinguish every error that the two original checks distinguish. Shared encoding does not give each layer all the information available to the final decoder.

Duplicating the same parity calculation twice also does not create two independent constraints. Compatibility and independence are different properties. The co-design task is to choose checks that are compatible across layers while retaining the distinctions each decoder needs.

### Correction, detection, and retry are different outcomes

Correction returns the intended data. Detection without correction reports that the data cannot safely be supplied. Silent corruption returns wrong data without an adequate warning. A system can improve detection while correcting no more cases; that can still prevent an application from silently accepting a wrong answer, but it does not improve availability in the same way as successful recovery.

The evaluation uses ten million random injections per scenario and counts link-detected failures as corrected through retry. Performance uses Accel-Sim with a V100-derived/HBM4 configuration; normal-path timing includes detection, not rare correction. [PDF pp. 9–10 and 12, Sections V-E and VI](https://arxiv.org/pdf/2605.02220v1#page=9).

Consequently, a reported corrected fraction must be read with its retry assumption. It does not necessarily mean the decoder repaired the originally received bits without another transfer. A deployment with persistent link faults or a retry deadline needs separate measurements.

Random injection is also conditional on the sampled fault model. Even zero observed failures in ten million independent representative trials would not prove zero failure probability. Under those assumptions, an approximate 95% upper bound is `3 / 10,000,000`, or three in ten million. That calculation is illustrative statistical reasoning, not a confidence interval supplied by the paper; nonrepresentative or dependent trials weaken the interpretation further.

Similarly, a rounded percentage displayed as 100% is not automatically a mathematical guarantee. The reliable distinction is between a proved covered set, sampled outcomes within a set, and assumptions about how often real hardware enters that set.

### Storage savings are not proportional application-speed savings

The paper compares 32 versus 48 redundancy bits per 256 data bits and reports 0.7% geometric-mean IPC improvement for the 32-bit configuration. Energy is modeled using HBM2E currents and scaling assumptions. [PDF pp. 12–13, Section VI-B](https://arxiv.org/pdf/2605.02220v1#page=12).

From those bit counts, redundancy falls by one third: `(48 − 32) / 48`. Total stored bits fall from 304 to 288, only `16 / 304 ≈ 5.26%`. These denominators answer different questions. Neither percentage directly determines die-area savings, because storage layout and peripheral circuits also occupy area.

IPC means completed instructions per clock cycle. If instruction count and clock rate are fixed, a 1.007× IPC ratio corresponds to about a 0.695% runtime reduction. Other delays can dilute even a substantial reduction in an encoder's own latency. The result should not be described as a one-third application speedup.

A modeled current estimate also differs from measured energy on a fabricated device. Sensitivity to transfer widths, activity, idle time, and current-scaling assumptions needs to accompany any extrapolation. A V100-derived simulation configured with a different memory model is not a measurement of a retail V100 fitted with that memory.

### What this adds to the chapter—and what remains unverified

The [current card](../observed-subthemes/memory-hierarchy-and-persistence.md#paper-isca-2026-program-004) now points to selected method and evaluation sections rather than only the abstract. No encoder, decoder, fault-injection experiment, or hardware model was executed here; final-proceedings equivalence and independent validation remain open.

Cerberus and CLUE-ECC both raise a deeper question than how many parity bits are present: which errors remain after an earlier protection stage, and can the next stage distinguish them? Their code layouts, physical interfaces, and evidence completeness differ. A joint comparison needs matching fault locations and residual-error definitions before ranking their protection or overhead.

<span id="explanation-isca-2026-program-008"></span>

## Lossless weight compression: a smaller representation must still feed computation

### Lossless relative to which input?

A weight is a numerical parameter used by the model. Its stored representation might be a floating-point bit pattern or a quantized integer accompanied by a scale. Lossless compression changes how that representation is stored while allowing its exact reconstruction. Quantization changes the set of representable values and can change the weights themselves.

These operations can be combined without becoming equivalent. Suppose an original weight is 0.37 and quantization represents it by integer 4 with scale 0.1, reconstructing 0.4. Losslessly compressing the integer preserves 4 exactly; it does not recover the original 0.37. The scale, offsets, and other required metadata must also remain available.

Bit-identical reconstructed weights are a strong local correctness condition. They do not alone prove bit-identical model outputs if the replacement computation changes accumulation order, arithmetic precision, kernels, or nondeterministic execution. A complete test should separate codec round-trip equality from operator equality and end-to-end model behavior.

### Why unequal frequencies create an opportunity to save bits

Four equally likely symbols need two bits each under a fixed-width representation. If their probabilities are instead one half, one quarter, one eighth, and one eighth, a prefix code can assign `0`, `10`, `110`, and `111`. No codeword is the start of another, so a decoder can identify boundaries without separators.

The average length is `0.5×1 + 0.25×2 + 0.125×3 + 0.125×3 = 1.75` bits per symbol. For this distribution it equals the entropy, calculated as the sum of each probability multiplied by `−log2(probability)`. Entropy describes an average under a source model, not a promise that every individual value gets a fractional-bit codeword.

The example uses an elementary prefix code to explain compression; it is not the paper's ANS codec. The key point is that common values can receive shorter representations while rare values consume longer ones, provided decoding remains unambiguous.

### The measured histogram is not a universal limit on every possible compressor

The paper estimates per-tensor symbol entropy and weights the aggregate by tensor size. [Preprint v1, PDF p. 2, Section II-B](https://arxiv.org/pdf/2606.15789v1#page=2).

This is a useful reference for symbol-frequency coding. It does not exhaust every possible dependency in a sequence. Consider a million-bit string alternating `010101...`. Its individual-bit histogram is half zero and half one, giving one bit of marginal entropy per bit. But a representation that records the alternating pattern and its length can be much smaller. Correlation between positions supplies information that the marginal histogram ignores.

Conversely, a short payload close to its histogram bound may still need a frequency table, restart states, tile offsets, padding, and format metadata. These consume real memory. Comparing payload bits alone against the entire uncompressed allocation can overstate the usable capacity gain.

Aggregation matters too. If one tensor has 100 weights at one bit each and another has 900 at four bits each, the weighted average is `(100×1 + 900×4)/1000 = 3.7` bits per weight. Averaging the two rates directly gives 2.5 and exaggerates compression of the actual model.

### Random access requires a place to start decoding

A matrix multiplication typically consumes rectangular pieces of a weight matrix, called tiles. A compressed stream whose state depends on everything decoded before it cannot be entered at an arbitrary byte offset and decoded correctly without restoring the appropriate state.

The proposed method uses independent tile streams with a shared layer codebook, then decodes into GPU shared memory alongside matrix multiplication. [PDF pp. 5–7, Sections V-B/V-C](https://arxiv.org/pdf/2606.15789v1#page=5).

A codebook describes the symbol distribution used by the codec. A tile offset locates the encoded bytes. A decoding state identifies where the decoder is within its reversible transformation. These are distinct pieces of information. Independence at tile boundaries allows one tile to be requested without reconstructing all preceding tiles, but costs metadata and can limit the statistics available to compression.

For a toy calculation, 1,024 tiles with four-byte offsets require 4,096 offset bytes. Adding a 16,384-byte codebook gives 20,480 bytes before any other overhead. Against an eight-megabyte weight allocation using binary units, that is about 0.244%. Against a much smaller matrix the same shared table can be far more significant. These are illustrative sizes, not extracted model measurements.

ANS, or Asymmetric Numeral Systems, represents a sequence through reversible changes to an integer state and an associated stream of bits. Decoding identifies a symbol from the current state, updates the state, and draws more bits when needed. One stream has sequential dependencies; parallel work requires multiple states or independently decodable streams. Naming the codec does not automatically establish arbitrary access or unlimited parallelism.

### Fusing decompression avoids one kind of traffic, not every cost

Suppose an uncompressed weight tile occupies eight kilobytes and its compressed representation four. A separate decompression pass might read four kilobytes, write eight reconstructed kilobytes to global memory, and let multiplication read those eight again: twenty kilobytes of weight-related global traffic before caching effects. Decoding directly into a local buffer can avoid that intermediate global write and read.

The decoder still executes instructions and uses registers, local storage, and synchronization. The local buffer also occupies space that other work might need. A reduction in global bytes does not establish a proportional speedup if decoding or arithmetic becomes the limiting step.

For three tiles, let decoding take two time units per tile and multiplication three. Serial execution takes 15 units. With two buffers, decoding can run at 0–2, 2–4, and 5–7 while computation runs at 2–5, 5–8, and 8–11, completing in 11. The third decode waits until time 5 before reusing the first buffer. This assumes no additional resource interference. If decoding rises to five units, it becomes the steady-state limit despite unchanged compressed size.

Buffer ownership is part of correctness. A producer must not overwrite a tile until the consumer has finished it; the consumer must not read before all required bytes are visible. Double buffering describes two storage slots, not a proof that the matching tile indices, readiness flags, and final pipeline drain are correct.

### Capacity gains and response-time gains answer different questions

Total GPU memory includes weights, KV state, temporary workspaces, and runtime allocations. Saving weight space can allow more simultaneous requests even if the operator handling each request becomes slightly slower.

Imagine an 80-GB budget, 30 GB of weights, 10 GB of other fixed allocations, and one GB of state per request. At most 40 requests fit under that toy model. Reducing weights to 20 GB raises the bound to 50 requests: a 25% increase, not the 33.3% weight reduction. If the per-request state doubles with longer sequences, those limits become 20 and 25.

Throughput counts total completed work per unit time. Time per output token measures how long a request waits between generated tokens. Larger batches can improve the former while worsening the latter. A serving system with a response-time requirement needs both, including slow requests rather than only the median.

### The source contains a batch-count discrepancy and a visible latency tradeoff

For Qwen-14B at length 1024 on one A100, Table II reports batch 47→60, while the abstract and Section VI-C say 47→75. Table II gives throughput 1131→1217 tokens/s and median time per output token 71→81 ms. For Mixtral on four A100s, the corresponding rates are 241→391 and 110→170 ms. [PDF pp. 9–10, Table II and Section VI-C](https://arxiv.org/pdf/2606.15789v1#page=9).

The Qwen throughput ratio is approximately 1.076, while its median per-token wait grows about 14.1%. Mixtral's corresponding changes are about 1.622× throughput and 54.5% longer median wait. These are calculations from the reported pairs, not new benchmarks. Describing the result only as faster inference would hide the service-quality tradeoff.

The two Qwen batch counts cannot both describe the same maximum under identical conditions. The discrepancy remains unresolved here; the evidence card preserves the conflict rather than selecting the more favorable number. A reproduction needs exact allocator budgets, model format, framework revision, request lengths, and admission settings.

The NeuZip/DFloat11 comparison is a single-projection H200 experiment, not whole-model serving. [PDF p. 10, Section VI-D](https://arxiv.org/pdf/2606.15789v1#page=10). Its ratio must not be substituted for the end-to-end numbers above.

### What the chapter can conclude now

The [current card](../observed-subthemes/memory-hierarchy-and-persistence.md#paper-isca-2026-program-008) now records method and evaluation locators, the batch discrepancy, and the throughput/latency distinction. No codec, fused kernel, or serving workload was executed here. Final-proceedings equivalence, implementation correctness, and independent reproduction remain unverified.

The useful cross-paper connection is to placement and transfer scheduling: a compressed representation changes what must move and how much fast memory remains available, but adds reconstruction dependencies. A valid comparison with expert offloading must include reconstruction, transfers, extra batching, and response-time constraints together. Compression ratio alone cannot decide which system is preferable.

<span id="explanation-isca-2026-program-045"></span>

## Vistara: making added capacity useful in a running service

### Capacity and access speed constrain different things

A server can run out of memory while its processors still have spare execution capacity. Adding another server provides memory but also duplicates processors, networking, power delivery, and operational overhead. Memory expansion attempts to add the constrained resource without duplicating the whole machine.

Suppose a service needs 3,000 GB of resident data and each server offers 750 usable GB. Ignoring replication, imbalance, and compute limits, four servers are required. At 1,000 usable GB each, three suffice: 25% fewer servers. This illustrates capacity-driven consolidation, not Vistara's measured fleet result. The smaller fleet is useful only if it still meets traffic, response-time, and failure-tolerance requirements.

Vistara's evaluated platform combines AMD Turin, 768 GB local DDR5, and 256 GB CXL-attached DDR4 through two ASICs. [Author-hosted paper, PDF p. 5, Table VI](https://aisystemcodesign.github.io/papers/isca26/vistara_camera_ready.pdf#page=5).

An ASIC is a chip designed for a particular function. A memory expander accepts host requests through one interface and services attached memory through another. Address-based access remains available to the application, but requests cross additional controllers and links. Compatibility does not make old memory identical to local memory in latency or bandwidth.

Reused DIMMs also have costs beyond acquisition: testing, the expander board, firmware, spares, power, and cooling. Environmental benefit requires a comparison including avoided manufacturing and added operational energy, not simply a count of reused modules.

### The operating system must preserve the ability to move pages

The paper exposes CXL as a CPU-less NUMA node and uses movable-only allocations with transparent page tiering. [PDF pp. 6–8, Section IV](https://aisystemcodesign.github.io/papers/isca26/vistara_camera_ready.pdf#page=6).

NUMA describes memory locations with different access costs. A CPU-less node supplies memory without an application-executing processor of its own. Keeping tiers identifiable allows software to place data according to those costs.

Migration copies a page and changes the mapping used by its consumers. It must preserve contents, permissions, and concurrent accesses. An allocation that cannot safely move can obstruct this policy if placed in a tier intended for rearrangement. Device discovery alone therefore does not establish safe, useful capacity.

Transparent tiering means applications need not place every allocation explicitly. It does not mean tracking and migration are free. Wrong predictions leave active data in a slow tier; moving it back consumes bandwidth and may displace other useful data.

### Cold capacity helps while active data still fits locally

Consider 75 GB local memory and 25 GB expanded memory. If only 60 GB of the 100-GB allocation is actively accessed, all active data could fit locally under ideal placement. At 90 GB active, at least 15 GB must lie elsewhere. No perfect hotness detector can overcome that inequality. Past inactivity helps predict placement, but does not guarantee that a page will remain idle after a workload changes.

Slower memory can nevertheless improve application latency by preventing much slower storage accesses. In a toy workload, a memory hit costs one unit and a storage miss 100. A 90% hit rate gives an average of 10.9. If expansion raises the hit rate to 99%, while the average memory hit now costs two units, the new average is 2.98. Individual memory hits became slower, but many storage misses disappeared. These are illustrative timings, not paper measurements.

### Expansion and equal-capacity tests answer different questions

Production A/B tests use matched machines, CXL enabled or disabled, split traffic, and runs of at least a week. Separate equal-capacity tests vary tier ratios; at 1:1, DPP throughput falls 19%. [PDF p. 8, Section V-A; pp. 11–12, Section V-G](https://aisystemcodesign.github.io/papers/isca26/vistara_camera_ready.pdf#page=8).

Enabling extra capacity asks whether expansion helps the existing machine. Holding total capacity fixed asks what happens when local memory is replaced by a slower tier. A design can win the first comparison and lose the second without contradiction. Both are needed to distinguish capacity relief from access-speed improvement.

Matched traffic and longer runs are stronger evidence than isolated peak bandwidth, but do not establish universal applicability. Reproduction still needs placement history, warm-up, admission policy, replication, and service-level targets. A production report is not an independently audited fleet experiment.

### Good aggregate utilization can conceal unfairness

The paper reports colocated-container imbalance and evaluates per-container local-memory bounds. [PDF p. 12, Section V-H and Table IX](https://aisystemcodesign.github.io/papers/isca26/vistara_camera_ready.pdf#page=12).

Imagine two applications each needing 50 GB, sharing 75 GB of local memory. Giving one all 50 GB locally leaves the other only 25 GB locally. Aggregate utilization is perfect, but their access costs differ. Equal allocation is not automatically correct either: applications may have different priorities or sensitivity to delay. Fairness requires an explicit resource or service objective.

Slow requests also matter. A good mean can coexist with occasional stalls from queues or page movement. A statement about stable hardware latency does not guarantee application tails, which include software, scheduling, and network delays.

### The source's threshold numbers need reconciliation

Table X labels its baseline 273 ns but lists 258 ns; adjacent prose alternates between roughly 75% and 60% for the threshold. [PDF pp. 12–13, Section V-I](https://aisystemcodesign.github.io/papers/isca26/vistara_camera_ready.pdf#page=12).

For the reported 315-ns final row, the increase over 258 is about 22.1%; over 273 it is about 15.4%. The approximately 22% entry agrees with the former denominator, but this calculation does not authorize silently correcting the caption. The source conflict remains unresolved.

A hot-footprint threshold also depends on local capacity, competing allocations, and available bandwidth. It is not a universal CXL constant. Measure when the actual active set stops fitting and when the expanded path becomes limiting.

The [current card](../observed-subthemes/memory-hierarchy-and-persistence.md#paper-isca-2026-program-045) now uses the author-hosted manuscript instead of only the earlier social post. No device, kernel configuration, or fleet experiment was executed here. Deployment within an infrastructure containing millions of servers must not be converted into a claim that millions of servers have Vistara installed.

## What these fourteen papers jointly explain

The common question is not simply how to make memory faster. The system must retain a useful representation, keep it valid, place it where needed, transport it in time, and protect it against specified faults. Improving one part can increase demands on another.

| Question | Relevant papers | Boundary that must remain visible |
| --- | --- | --- |
| Where should computation and reused data reside? | HybriMoE, SAEM, MoE-Balance, RememTier | Prediction, transfer, migration, and competing work all cost resources. |
| Can stored information be reused or represented more compactly? | KEEP, lossless weight compression | Context validity and exact reconstruction differ from end-to-end quality. |
| What physical work remains near memory? | REFLEX, 3D-ReSAC | Row activity, refresh, and inter-region communication remain. |
| Can corrupted data be recovered? | Adaptive read retry, CLUE-ECC, Cerberus | Fault location and residual errors determine decoder guarantees. |
| Can the design operate as a complete system? | OpenSUN, Ctxmem, Vistara | Documentation, simulation, hardware, and production are different evidence tiers. |

These overlapping conceptual groups organize the reading; they do not silently replace the unreconciled taxonomy.

Three hypotheses follow from the explanations. First, placement should optimize avoidable waiting rather than only access frequency. Test this at fixed capacity while varying miss costs, concurrency, and prediction delay; added policy costs can invalidate the benefit.

Second, representation and placement should be evaluated together. Compression changes transfer bytes and available capacity but adds reconstruction. Cached state avoids reconstruction only while dependencies remain valid. Compare complete execution at fixed quality and response-time requirements, not merely at each design's largest possible batch.

Third, protection stages should be judged by what reaches the next stage. A local mistake confined to one symbol may remain recoverable; spreading it can invalidate the downstream guarantee. Test the composed error transformation rather than adding nominal correction strengths.

These are testable interpretations, not established long-term trends. Demonstrating a trend still requires comparable editions, source availability, workload conditions, and checks against selection effects. The fourteen-record sample does not supply that longitudinal proof.

## Persistence is a separate requirement

Persistent storage retains information across a specified failure such as loss of power. A value being present in a fast cache does not necessarily mean it has reached that persistent location. Software may need a defined ordering of updates so that recovery cannot observe a mixture of incompatible old and new state.

The broad taxonomy label combines hierarchy and persistence, but a cache-placement result does not establish durability. A persistence claim needs its own failure model, definition of a completed update, and recovery experiment. Keep that distinction when reading papers grouped under this label.

## The current grouping is broader than one technical problem

The selected records include expert placement, CXL tiering and deployment, near-memory execution, weight compression, flash read retry, error-correcting codes, and scale-up networking. These are distinct questions about capacity, access, computation, communication, and reliability. Their shared placement under this label comes from the current coding; it is not evidence that they solve the same problem or support a single comparative ranking.

In particular, error correction addresses recovery of data under a specified error model. Persistence addresses survival and consistency across a specified failure. Compression changes how many bits represent data. Tiering changes where data resides. Any of these can affect another, but a result in one does not establish a result in the others. The individual explanations clarify these branches; taxonomy reconciliation and independent review against primary evidence remain necessary before merging conclusions.

## The experiment that would make the result useful

Vary working-set size, reuse pattern, competing work, tier capacity, and transfer bandwidth. Include migrations, prefetches, eviction costs, and interference. Measure completion time and slow requests as well as cache hit rate. For persistent systems, also test the stated failure points and validate recovered state.

A strong conclusion explains which access behavior the policy exploits and where that behavior changes. That condition is necessary for deciding whether the method belongs in another system.
