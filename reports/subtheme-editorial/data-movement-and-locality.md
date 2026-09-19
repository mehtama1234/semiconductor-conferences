## Begin with the location of a value

A calculation needs its inputs before it can produce an output. If an input is already in a register next to the arithmetic unit, the hardware can use it quickly. If it is in another memory device or another machine, the system must request it, transport it, and make it available to the operation. That movement can take longer and consume more energy than the arithmetic itself.

Locality describes opportunities to avoid repeated expensive access. Reusing the same value soon after reading it is useful if the value remains in nearby storage. Processing values stored next to one another can also make a transfer more efficient. Both opportunities depend on the program's order of operations and the amount of storage available.

## Three different ways to reduce the cost

One choice is to move fewer bytes. Retaining intermediate values, combining operations, or compressing a representation can do this. Compression also requires encoding, decoding, and sometimes additional numerical checks.

A second choice is to execute an operation nearer its stored inputs. This can reduce traffic over a particular connection. It requires suitable compute resources near the data and an account of how inputs arrive and results leave.

A third choice is to schedule the same transfers more effectively. Two activities can proceed together when they use independent resources. They can delay each other when they compete for the same memory bank, command path, or data connection. Scheduling must account for those specific shared resources.

These choices explain why two papers can both discuss data movement yet propose different methods. One reduces traffic, one relocates arithmetic, and another avoids interference. Their speedups answer different experimental questions.

<span id="explanation-dac-2026-research1256"></span>

## DAP: distributed SpMM needs balanced work, communication, and dependency correctness

Sparse-dense matrix multiplication is not defined only by the number of nonzeros. A distributed implementation must place sparse entries and dense operands across chips, move metadata and values, accumulate partial sums, and respect dependencies. Irregular nonzero locations can leave one node busy while another waits; reducing arithmetic or metadata can move the bottleneck to links, memory banks, synchronization or accumulation order.

[DAP](../observed-subthemes/data-movement-and-locality.md#paper-dac-2026-research1256) combines a two-level partitioner for a 2-D multi-chip array with an SPU that uses CSC instead of COO, reduces redundant data replication, and handles floating-point RAW dependencies with a reservation buffer. The captured description does not specify the partition objective, CSC layout, routing, arbitration, replication policy, buffer size, precision or interconnect microarchitecture.

The first gate is work and communication balance. Report per-node nonzeros and operations, dense-operand reuse, bytes, messages, link utilization, queueing, memory occupancy, replication, critical-path dependencies and partition/conversion time across matrix shapes and sparsity distributions. A balanced nonzero count can still produce an imbalanced communication or memory schedule. Define the denominator and comparison boundary for the reported 1.43× partitioning improvement.

The second gate is numerical and dependency correctness. Compare outputs with a high-precision reference for duplicate indices, empty rows/columns, arbitrary sparsity, cancellation, accumulation order, precision and rounding. Exercise reservation-buffer overflow, backpressure, dependency races and partial-sum ordering; report conflict stalls, storage, control traffic and any preprocessing or fallback. CSC conversion and reduced replication must preserve the intended sparse-dense result rather than merely improve a trace statistic.

The source reports a 0.067× performance penalty attributed to memory-access conflicts and 2.69× geometric-mean throughput relative to an NVIDIA A100 at 500 MHz, both from simulation. It does not clarify whether the penalty is a relative loss or remaining fraction, or expose the matrix suite, absolute throughput, communication, utilization, numerical error, area, power, energy, chip scaling or complete A100 normalization. Include format conversion, preprocessing, transfers and inter-chip communication in the same end-to-end boundary before interpreting the comparison.

The evidence supports multi-chip sparse-matrix communication co-design, not demonstrated portable end-to-end SpMM superiority, ASIC efficiency or numerical equivalence across workloads.

<span id="explanation-dac-2026-research1113"></span>

## RAF: a communication lower bound is useful only after the access model is fixed

Near-memory processing places some computation close to distributed memory. In a vault/channel organization, a tensor element may be available in the local memory region for an operator or may need to cross a channel or vault boundary. That distinction matters because a design can reduce arithmetic while still spending time and energy on remote requests, synchronization, and partial-result movement.

RAF, or Remote-Access-Free, is described as a tensor-rotation dataflow for LLM operators. The rotation abstracts the distributed organization so that intra-operator remote access can be eliminated; analytical optimization then minimizes the remaining intra-operator local access. Data partitioning targets inter-operator remote access, and operator fusion targets inter-operator local access. These are four different costs. Removing one does not prove that the others vanish, and the captured description does not expose the exact tensor layout, partition constraints, fusion legality, or compiler schedule.

### “Lower bound” depends on the feasible design space

A communication lower bound is a statement about the minimum traffic under a specified model. The model must define tensor dimensions, operator graph, data layout, replication, memory capacity, number of vaults/channels, allowed recomputation, precision, reduction order, and what counts as local or remote. If replication is free, the bound differs from a model that counts storage and initialization traffic. If recomputation is allowed, less communication may require more arithmetic. If a local access contends for one bank, it may be slower than an uncongested remote access.

The appropriate check is therefore not only “does RAF report zero remote accesses?” Measure bytes, requests, hops, local-bank conflicts, queueing, synchronization, barriers, metadata, partial reductions, initialization, eviction and output movement. State whether the bound covers one operator, a fused graph, or the complete model execution. A proof for an idealized operator is not automatically a bound for the deployed schedule.

### Tensor rotation changes placement, not model semantics

Rotating a tensor changes which physical location supplies each logical element. The transformation must preserve indexing, broadcasting, reductions, layout conversions, padding, masking and the order or precision of accumulated results. Partitioning must also preserve ownership and visibility when one operator produces data consumed by another. Fusion can save an intermediate write and read, but it can increase the live working set, register or local-memory pressure, and the amount of synchronization required inside the fused region.

Validate each transformed operator and fused sequence against a trusted unfused reference. Test different tensor shapes, batch and sequence lengths, attention or reduction patterns, sparsity, precision and numerical tolerances. Report accuracy or output error separately from communication. A communication reduction is not an LLM-quality result, and a numerically plausible output on one shape does not establish correctness across the graph.

### Energy and speedup need a common boundary

The official description reports energy reductions of 50.4%, 39.0% and 37.8%, and speedups of 3.98×, 1.72× and 1.57× over IANUS, H^2LLM and OptiPIM respectively. It does not identify which workload produces each pair, the memory technology, model and precision, capacity pressure, simulator or hardware boundary, or whether compiler transformation, data movement, loading, synchronization and output handling are included. The superscript form H^2LLM is retained from the source; the packet's baseline label uses H2LLM.

An energy result should identify dynamic and static components, memory and compute contributions, link/controller energy, idle energy, refresh or storage work, and the measurement or modeling method. A speedup should include the same model execution and preprocessing boundary for every baseline. Report per-model and per-operator traffic, latency distributions, utilization, peak storage, area, thermal behavior and failures rather than only aggregate ratios.

The evidence supports RAF as a constrained near-memory dataflow direction with reported source-level energy and speedup claims, not demonstrated universal LLM/NMP efficiency or communication optimality. The metric-to-workload mapping, lower-bound assumptions, accuracy, capacity, hardware implementation and complete compiler/runtime cost remain unresolved.

<span id="explanation-dac-2026-research108"></span>

## CANNON: real CXL hardware strengthens the evidence, but ANN quality and the full query path still matter

Approximate nearest-neighbor (ANN) search returns vectors or IDs close to a query under a chosen distance metric without exhaustively comparing every stored vector. A useful system must balance three outcomes: retrieval quality, latency/throughput, and the capacity and energy cost of storing and moving the index. A faster pipeline that returns different neighbors may be unacceptable to a retrieval or RAG application.

CANNON is described as a fully offloaded CXL near-memory-processing architecture implemented on real CXL hardware. It transforms ANN search into a fine-grained, deeply pipelined dataflow, adds asynchronous hashing, and uses speculative execution to hide hash-check latency. These mechanisms target access and pipeline stalls, but the description does not disclose the ANN index, distance computation, candidate policy, hash function, false-positive/negative handling, CXL configuration, or what work remains on the host.

### Speculation must preserve the retrieval contract

Asynchronous hashing can overlap hash generation or checking with other stages. Speculative execution can begin work before a hash check or candidate decision is final. The system must then define what happens when speculation is wrong: discard cost, duplicate work, queue pressure, stale candidates, ordering, and any effect on returned top-k results. Validate IDs and distances against an exact or high-quality reference, and report recall@k, precision, distance error, candidate counts, false omissions, ties and tail queries alongside performance.

### “Real hardware” still needs a reproducible configuration

The source says CANNON runs on real CXL hardware, but the captured description does not identify the CXL generation/protocol, device memory, capacity, link width and speed, host CPU, accelerator logic, vector storage format, index placement, batching, concurrency, software stack, power measurement, or thermal conditions. State whether the design uses CXL.mem, CXL.io, or another path, and separate host, link, device-memory, NMP, controller and storage costs.

Measure query encoding, index traversal, hashing, candidate filtering, distance computation, synchronization, result transfer and any reranking. Report p50/p95/p99 latency, QPS, bandwidth, queueing, memory footprint, preprocessing/index-build time, update cost, power and energy per query. Compare CPU and GPU baselines at matched dataset, dimension, metric, top-k, recall target, batch, concurrency, index algorithm, memory capacity, software version and end-to-end boundary. A comparison that places the baseline index in slow storage but gives CANNON a resident index is not a hardware-only improvement.

The official description reports up to two orders of magnitude performance improvement over state-of-the-art CPU and GPU baselines on large-scale vector datasets. It does not expose dataset identities, absolute throughput or latency, recall/accuracy tradeoffs, or the CXL configuration. The real-hardware statement raises the evidence tier for implementation existence, but the evidence still supports a CXL/NMP ANN architecture direction, not demonstrated recall-preserving end-to-end ANN/RAG acceleration across workloads.

<span id="explanation-dac-2026-research2294"></span>

## PIMA-SecDB: moving FHE SQL into memory is useful only when query semantics and cryptographic validity survive

Fully homomorphic encryption allows computation on ciphertexts, but database queries can require scanning, comparing, rotating, multiplying and moving expanded ciphertext representations. A PIM architecture can reduce movement over a host-memory boundary, yet the query still has to return the same result under the declared privacy, security and correctness contract. The memory hierarchy is part of the FHE execution, not a substitute for its cryptographic semantics.

[PIMA-SecDB](../observed-subthemes/data-movement-and-locality.md#paper-dac-2026-research2294) is described as a hardware/algorithm co-design with multi-level, multi-channel PIM, a bootstrapping-reduced FHE SQL path, and quantitative selection of encryption parameters for PIM suitability. The captured description does not identify the FHE scheme, query circuit, parameter constraints, noise management, memory technology or PIM operation semantics.

The first gate is cryptographic and query correctness. State the SQL/query subset, schema, predicates, joins, aggregations, selectivity and result encoding. Report scheme, security level, modulus/levels, packing, multiplicative depth, rotations, key switching, ciphertext noise, bootstrapping and decryption error. Compare decrypted results with a plaintext/database reference and establish that removing bootstrapping does not merely defer refresh or output work outside the measured boundary.

The second gate is complete data-movement accounting. Measure encrypted bytes, ciphertext expansion, PIM operations, channel utilization, memory bandwidth, queueing, host/controller transfers, key management, preprocessing, encryption/decryption, retained bootstrapping, control and result materialization. Test dataset scale, query mix, selectivity, concurrency and parameter choices; a scan-friendly query can hide costs that dominate joins or selective predicates.

The source reports 1.98×–7.93× speedup over existing FHE accelerators, but supplies no per-query latency, absolute throughput, cryptographic parameter table, noise margin, correctness/failure rate, security analysis, energy, area, memory technology or implementation result. The range may mix query and parameter conditions, so it cannot be treated as a universal end-to-end gain.

The evidence supports FHE/PIM database co-design, not demonstrated end-to-end secure query acceleration across workloads, equivalent SQL semantics or deployable PIM efficiency.

<span id="explanation-dac-2026-research1629"></span>

## AQR-HNSW: compression and re-ranking help only when ANN recall and the full query path remain intact

HNSW search navigates a graph of vectors to find approximate nearest neighbors without comparing a query with every stored vector. At billion-vector scale, graph memory and distance computation can dominate. Quantization reduces stored representation size, while re-ranking can spend more accurate distance work only on selected candidates. Both changes alter the search approximation, so a speed result is useful only with a defined recall contract.

AQR-HNSW is described as combining density-aware adaptive quantization, multi-state re-ranking and quantization-optimized SIMD implementations. The quantizer is intended to preserve distance relationships across heterogeneous density; the re-ranking stages remove unnecessary distance computations; the SIMD path exposes 16–64 operations per cycle across architectures. The captured description does not specify density estimation, bit allocation/codebooks, candidate bounds, re-ranking states, update behavior, vector ISA or whether final distances are exact.

The first gate is retrieval correctness. Define the distance metric, top-k and tie handling, exact reference, recall denominator and query set. Compare returned IDs and scores with exact search and report recall/precision tails by density, distance, dimension and query difficulty. A quantized distance can preserve average relationships while changing the nearest-neighbor boundary, and “98%+ recall” is uninterpretable without its reference and distribution.

The second gate is complete query accounting. Measure graph traversal, quantized vector reads, codebook/metadata access, SIMD work, re-ranking states, candidate count, cache misses, memory bytes, synchronization and p50/p95/p99 latency. Include index construction, compression, allocation, warm-up, updates and rebuilds. A 35% reduction in unnecessary computations is not automatically a 35% query-speed improvement if memory or graph traversal dominates.

The source reports 4× quantization compression, 35% fewer unnecessary computations, 16–64 operations per cycle, 2.5–3.3× higher QPS than state-of-the-art HNSW, 98%+ recall, 75% index-graph memory reduction and 5× faster index construction. It does not expose absolute latency or tails, recall distribution, distance error, update cost, energy, hardware, dataset conditions or per-workload results. Hold out datasets, dimensions, density mixtures, query classes, graph sizes, top-k and update phases; compare HNSW and product quantization at equal recall, memory, ef settings and hardware.

The evidence supports adaptive quantized HNSW, not demonstrated recall-preserving universal QPS, durable update efficiency or complete system superiority.

<span id="explanation-dac-2026-research1357"></span>

## 3D-DuRA: sparse attention reduces movement only when visual quality and 3D cost remain intact

Visual autoregressive generation predicts an image in successive resolutions. At each step the token map can grow, so attention repeatedly reads and combines a larger set of representations. The arithmetic may be sparse, yet the memory traffic, token movement and synchronization needed to discover and reduce those interactions can dominate. An architecture is useful only if it reduces that path while preserving the interactions required for the generated image.

3D-DuRA is described as an algorithm–architecture co-design with a hybrid 3D near-memory and in-memory computing stack and dual-ring sparse attention. Near-memory logic places computation close to stored data; in-memory operations further reduce movement for suitable primitives; the two rings organize sparse token interactions and reductions. These choices change placement and communication, but the captured description does not specify the sparsity rule, token mapping, ring schedule, data layout, reduction semantics, precision, sensing path, compiler or thermal policy.

The first gate is generation fidelity. Define which attention interactions are removed, how candidates are selected, the threshold or budget, resolution transition, positional behavior and reduction order. Compare attention outputs, logits and final images with dense reference generation under matched seeds or decoding, and report image-quality metrics, diversity, long-range/high-resolution failure cases, sparsity, false omissions and quality versus speed. A lower operation count is not equivalent generation if the sparse pattern loses a visually important dependency.

The second gate is dataflow accounting. Measure token and metadata bytes, ring hops, broadcasts, partial reductions, barriers, bank/array utilization, queueing, buffer occupancy, mapping overhead, precision conversion, idle time and output movement. Report p50/p95/p99 generation latency by resolution and include sparse-index construction, model loading, warm-up and resolution changes. Account for shared-link bandwidth explicitly: a dual-ring design can move the bottleneck from memory reads to synchronization or a saturated link.

The physical boundary must include the complete 3D stack: memory arrays, near-memory logic, in-memory compute, interconnect/bonding, buffers, controllers, sensing/ADC/DAC, cooling and thermal throttling. State whether area and energy are modeled, post-layout or measured, and test sustained generation and hotspot behavior. Compare with the RTX 6000 Ada and dense in-memory baselines at the same model, precision, resolution, quality target, batch, memory capacity, frequency, thermal limit and software/runtime boundary.

The official description reports 4.1× area-efficiency improvement versus an RTX 6000 Ada GPU, 3.5× and 9.1× speedups, and 10.1× and 13.1× energy-efficiency improvements on Infinity2B and VAR-d36 respectively. It does not expose absolute latency or energy, image quality, sparsity/recall, area definition, traffic, utilization, thermal conditions or fabrication status. The evidence supports a hybrid 3D sparse-attention architecture direction, not demonstrated quality-preserving, thermally sustainable or portable end-to-end generation efficiency.

<span id="explanation-dac-2026-research1976"></span>

## CacheParallel: reusing diffusion intermediates is useful only if the denoising trajectory and output quality remain valid

Diffusion generation repeatedly transforms a noisy sample across timesteps. Each step may reuse parts of a network’s computation, but the current timestep, conditioning, noise state and solver history can change what an activation means. The system must therefore distinguish a cache hit that reuses a mathematically valid value from a stale approximation that merely reduces arithmetic.

CacheParallel is described as a training-free scheme spanning two levels. A fusion node abstracts a network into pre-fusion and post-fusion computational streams. The pre-fusion stream uses CPS for intra-step caching; the post-fusion stream uses correlations between outputs at different steps to expose parallel work and increase computational density. An error-correction mechanism uses observed linear correlations to mitigate accumulated errors and non-orthogonality when methods are combined. These mechanisms change reuse and scheduling, but do not by themselves define the legal dependency graph or establish that the generated sample follows the uncached sampler.

The first gate is trajectory and sampler fidelity. Define the sampler/solver, timestep schedule, noise and random-seed handling, conditioning, cached tensors, reuse horizon, solver state, parallel ordering and correction coefficients. Compare fixed-seed outputs and intermediate score/noise predictions with uncached inference, then report image-quality or task metrics, score/reconstruction error, diversity, failure cases and quality versus acceleration. A throughput improvement that changes the sampling distribution or collapses diversity is not equivalent acceleration.

The second gate is cache and parallel accounting. Measure hit/reuse rate, stale or invalid entries, cache occupancy and capacity, bytes moved, recomputation, correction work, synchronization, memory bandwidth, parallel utilization, queueing, energy, warm-up and cold-start behavior. Separate reusable precomputation from per-request work and report p50/p95/p99 latency and throughput. Test model architectures, samplers, timestep counts, prompts, resolutions, batch sizes and cache budgets that were not used to tune the correlation policy; correlations can disappear when the workload or denoising phase changes.

The baselines should include uncached inference, a single-level cache and structure-specific caching methods under the same model, sampler, quality target, hardware, memory budget and end-to-end boundary. Include all unsupported or recomputed operators, output handling and any correction/fallback path. Peak improvement is not an average result, and improvements from separate components cannot be multiplied when they share memory or synchronization resources.

The official description presents a training-free method and reports comparative gains across various diffusion models, with a peak improvement exceeding 100%. It does not expose absolute latency or throughput, sample quality, sampler conditions, cache trace, memory/energy accounting, correction error or hardware configuration. The evidence supports multi-level diffusion caching and parallelism, not demonstrated quality-preserving universal diffusion acceleration.

<span id="explanation-dac-2026-research2235"></span>

## CoX-MoE: coalescing expert work raises operational intensity only if routing, transfer, and decode tails remain correct

Mixture-of-Experts inference activates a small subset of experts for each token, but the selected tokens may be fragmented across experts and requests. Micro-batches can reduce padding and memory pressure while leaving each expert with too little work to use the hardware efficiently. Moving some work to an AMX CPU can use otherwise idle compute, but every offloaded tensor pays for placement, transfer, synchronization and the CPU/GPU critical path.

CoX-MoE is described as an AMX-enabled CPU-GPU collaborative system with two main scheduling choices. It uses ordinary batches for expert computation through a coalescing-aware orchestration policy, and selectively offloads attention rather than assuming every stage belongs on the CPU. A static expert-aware stratification pre-assigns frequently activated experts to the GPU, leaving other work to be balanced between CPU and GPU. These choices target operational intensity and PCIe traffic; they do not by themselves define token dispatch/combination, capacity overflow, routing changes, or how decode dependencies are synchronized.

The first gate is MoE correctness. Define top-k routing, expert capacity, token dropping or fallback, padding, dispatch, expert execution, combination, precision and attention state. Compare expert assignments, logits, perplexity and task quality with a GPU-only reference across prompt/prefill and decode, sequence lengths, batch/concurrency and routing skew. Ordinary-batch coalescing must not reorder tokens or silently change which expert receives them; an apparent throughput gain with altered routing or dropped tokens is not equivalent inference.

The second gate is heterogeneous critical-path accounting. Measure CPU, AMX and GPU utilization, expert load balance, GPU residency, PCIe/interconnect bytes, DRAM/cache traffic, queueing, synchronization, transfer overlap, padding, staging, attention-offload work, scheduling overhead and p50/p95/p99 latency. Separate time to first token from inter-token latency and include model loading, warm-up, stratification/planning and fallback. Test phase changes, prompt distributions, expert popularity shifts, concurrent requests, memory pressure and link contention; static GPU residency can become a hotspot when routing changes.

Compare FlexGen, MoE-Lightning, GPU-only serving and uncoupled CPU/GPU offload with the same model, routing, precision, batch, prompt/decode workload, memory capacity, CPU/GPU/link, kernels, quality target and end-to-end boundary. A fair result must disclose whether baseline tuning includes micro-batch size, CPU kernels, PCIe overlap and expert placement; component gains cannot be added when they share the same transfer and synchronization path.

The official description reports AMX CPU-GPU collaboration and up to 7.1× higher throughput than FlexGen and 2.4× higher throughput than MoE-Lightning. It does not expose absolute tokens/s, model/precision, routing, utilization, bandwidth, latency tails, energy, quality, scaling or baseline tuning. The evidence supports coalesced heterogeneous MoE execution, not demonstrated quality-preserving universal throughput improvement or portable CPU-GPU co-execution.

<span id="explanation-dac-2026-research368"></span>

## TriMoE: three-way expert placement helps only when routing, migration and the new bottleneck remain controlled

Mixture-of-Experts inference activates only some experts for each token. A GPU can execute hot experts efficiently, but cold experts may exceed GPU memory and CPU offload can be limited by host-memory bandwidth. Warm experts are a separate case: they may be requested often enough to suffer GPU I/O latency while also generating enough arithmetic to saturate a near-memory engine. Treating every non-hot expert as one class can therefore move the bottleneck rather than remove it.

TriMoE is described as a GPU–AMX-enabled CPU–DIMM-NDP architecture that maps hot, warm and cold experts to different compute resources. It adds bottleneck-aware expert scheduling and prediction-driven dynamic relayout/rebalancing. These mechanisms change placement and timing, but the captured description does not specify routing traces, class thresholds, placement granularity, migration protocol, tensor ownership, coherence, synchronization, prediction horizon, NDP kernels or fallback. A relayout is useful only if its cost and consistency are included in the serving path.

The first gate is MoE correctness. Define top-k routing, capacity limits, token dropping/overflow, dispatch and combination, precision, expert state and attention/KV dependencies. Compare expert assignments, logits, perplexity or task quality with an exact GPU reference across prompt/prefill and decode, sequence lengths, batch/concurrency, routing skew and distribution shifts. Report stale placement, migration failures, dropped tokens, fallback and numerical error; a throughput gain with altered routing is not equivalent inference.

The second gate is heterogeneous critical-path accounting. Measure expert bytes, GPU I/O, CPU/AMX and DIMM-NDP work, DRAM/channel/NDP/link utilization, queueing, synchronization, coherence, migration and relayout bytes, metadata, prediction work, p50/p95/p99 time to first token and inter-token latency, throughput, energy and warm-up. The three resources have different ceilings: moving a warm expert can reduce GPU I/O while saturating NDP compute, or increase traffic and tail latency through repeated rebalancing.

Prediction-driven adaptation needs a held-out routing trace and a defined horizon, misprediction penalty, stability policy and migration budget. Test phase changes, bursty requests, concurrent tenants, memory pressure, link contention and cold starts. Report prediction precision/recall, stale placement, oscillation, relayout frequency and per-expert tail behavior. Compare GPU-only, CPU/GPU offload, GPU-NDP and static tri-level placement with the same model, precision, hardware, quality target, tuning, warm-up and end-to-end boundary.

The official description reports up to 2.83× speedup over state-of-the-art solutions. It does not expose model/precision, routing, absolute latency, utilization, bandwidth, energy, migration cost, quality, scale or topology. The evidence supports tri-level heterogeneous MoE offload and adaptive placement, not demonstrated quality-preserving universal throughput improvement or portable GPU–CPU–NDP deployment efficiency.

<span id="explanation-dac-2026-research375"></span>

## Crystal-KV: answer-aware eviction helps only when later reasoning, cache semantics and response quality remain intact

Chain-of-thought (CoT) generation can produce a long sequence of intermediate tokens before the final answer. Autoregressive attention normally retains key/value (KV) state for those tokens, so cache capacity and movement grow with the thinking sequence. But “intermediate” does not mean disposable: a later step may revisit an earlier fact, and a token that looks weakly related to the answer can still be necessary for the reasoning path.

Crystal-KV is described as applying an answer-first principle to attention maps from the answer back into the think stage. It distinguishes SlipKV entries that mainly preserve reasoning flow from CrystalKV entries that contribute to final-answer correctness, evicts SlipKV with an attention-based Least Recently Frequently Used policy when utility expires, and reallocates cache budget across layers and heads according to the dynamic CrystalKV proportion. These mechanisms change retention and budget decisions; the captured description does not define answer extraction or verification, utility thresholds, token labels, recomputation/offload, position handling, precision or synchronization.

The first gate is reasoning fidelity. Define the answer/quality criterion and compare full-cache generation with Crystal-KV under matched model, prompt, decoding, seeds or sampling conditions, and think budget. Report final answer accuracy and task metrics, output/logit agreement, reasoning-step or intermediate-state error, failures after eviction, and behavior for long thinking, self-correction, evidence revisits and changed answer position. An attention preference is not by itself a causal proof that removing a KV entry cannot change a later decision.

The second gate is cache correctness and critical-path accounting. Preserve layer/head indices, sequence positions, rotary or other position semantics, attention dependencies and precision. Measure hits, evictions, stale entries, recomputation, offload/prefetch bytes, metadata, budget reallocations, queueing, memory occupancy, GPU utilization, p50/p95/p99 time to first and inter-token response, throughput and energy. Include attention analysis, eviction decisions, cache movement, warm-up and fallback; a smaller cache can increase recompute or transfer enough to erase the apparent latency gain.

Adaptive budgets need distributional validation. Test short and long think traces, answer-position changes, self-correction, branching/tool-use patterns, diverse tasks and model families, batch/concurrency, memory pressure and cold starts. Compare full retention, naive eviction, uniform compression and existing importance-aware policies at equal capacity, precision, answer-quality tolerance, hardware and total-time boundary. Report policy-analysis overhead, calibration/training cost, budget oscillation and per-task failures.

The official description claims state-of-the-art KV-cache compression, improved throughput and faster response time while maintaining or improving answer accuracy for CoT reasoning. It does not expose absolute memory/latency, answer or reasoning metrics, eviction error, recomputation/traffic, model/task conditions, cache budget, hardware or tails. The evidence supports answer-aware CoT KV management, not demonstrated reasoning-faithful, universally efficient or quality-preserving KV compression.

<span id="explanation-dac-2026-research2199"></span>

## Expertflow: predictive expert loading helps only when routing, cache state, and token latency are measured together

Sparse MoE inference activates only a few experts for each token, but the complete expert pool can exceed GPU memory. Offloading inactive experts to CPU memory makes the model fit while adding transfer and synchronization. A cache predictor can reduce those transfers when its forecast is correct; a wrong forecast can evict useful state, increase misses, or delay the critical path. Token scheduling adds another dependency because requests for different experts compete for memory bandwidth, compute slots and the interconnect.

Expertflow is described as combining a routing-path predictor, a routing-aware token scheduler and a predictive expert cache. The predictor anticipates future expert use, the cache loads likely-needed experts, and the scheduler orders tokens to make those loads and executions overlap. This changes the placement and timing of expert data. It does not establish routing correctness, prediction accuracy under a changing workload, or that overlap survives queueing, synchronization and tail requests.

The first gate is model and routing fidelity. State the MoE model, top-k routing, precision, capacity factor, token dropping/fallback behavior and cache hierarchy. Compare selected experts, output logits, perplexity or task quality with an uncached exact reference under diverse prompts, sequence lengths, batch/concurrency levels, expert-skew patterns and distribution shifts. Report predictor precision/recall, cache hit rate, stale or mispredicted loads, evictions, dropped tokens and fallback work; a high hit rate does not prove that the right expert outputs arrive on time.

The second gate is the complete serving path. Measure CPU/GPU memory, interconnect bandwidth, expert-load bytes, queueing, prefetch lead time, synchronization, scheduler overhead, cache metadata, initialization, p50/p95/p99 token latency, throughput, energy and quality. Separate cold and warm starts and include prompt/prefill and decode phases. Compare uncached serving, reactive scheduling, static caching and predictive caching under the same model, capacity, request trace, quality target, hardware, software and end-to-end boundary. Include the cost of collecting routing history and running the predictor.

The official description claims 93.72% lower GPU memory use and up to 10× higher throughput on a single GPU, but provides no model/trace conditions, cache hit rate, bandwidth, latency distribution, energy, quality result, predictor cost or baseline accounting. The evidence supports predictive expert caching with routing-aware scheduling, not demonstrated quality-preserving end-to-end MoE serving or universal throughput benefit.

<span id="explanation-dac-2026-research1582"></span>

## SliceMoE: bit-slice caching trades off offload traffic, precision, and miss behavior

Mixture-of-Experts (MoE) inference activates only a subset of experts for each token, but the full expert pool can exceed on-device memory. A cache must decide which expert data to retain and when to fetch the rest. A cache miss adds transfer and decode work to a token's critical path; a lower-bit representation saves capacity and bandwidth but can change the expert's numerical output. Miss rate, memory footprint, latency, energy and model quality therefore form one coupled measurement problem.

SliceMoE is described as Dynamic Bit-Sliced Caching (DBSC), which stores expert slices at different precision and assigns precision on demand; Calibration-Free Asymmetric Matryoshka Quantization (AMAT), which makes truncated low- and high-bit slices compatible without calibration; and Predictive Cache Warmup (PCW), which reshapes cache contents during prefill to reduce early-decode cold misses. The mechanism changes both what is cached and what numerical representation is fetched. It must preserve expert routing, slice assembly, token ordering and precision semantics while accounting for prefill work and later decode traffic.

The first gate is quality and miss-model validity. Fix tokenizer, prompts, routing policy, batch, sequence length, context, sampling and high-bit reference. Report perplexity or task accuracy, output agreement, expert-selection stability, miss rate by phase and expert popularity, precision assigned per slice, and worst-case degradation rather than only “near-high-bit” average quality. Test changing prompts, long contexts, bursty routing, cold starts and distributions not used to tune the predictor; a miss-rate constraint is useful only if it is measured under the deployment workload.

The second gate is complete deployment accounting. State device memory hierarchy, accelerator, host link, bandwidth, storage, precision kernels and energy instrumentation. Include expert metadata, slice assembly, quantization/dequantization, prefill warmup, cache eviction, transfers, synchronization, idle power and all decode tokens in latency and energy. Compare high-bit caching, expert prefetching, clustering and a fixed-capacity policy at equal model quality, memory budget, batch/sequence workload and end-to-end measurement boundary. Report p50/p95/p99 token latency, throughput, memory occupancy, traffic, energy/token and warmup overhead.

The official description reports DeepSeek-V2-Lite and Qwen1.5-MoE-A2.7B results: up to 2.37× and 2.85× lower decode energy, and 1.81× and 1.64× lower decode latency, while preserving near-high-bit accuracy. It does not provide absolute quality, miss rates, memory capacity, device, bandwidth, quantization settings, sequence workload, tail latency, prefill cost or energy boundary. The evidence supports slice-level MoE caching and precision adaptation, not demonstrated universal end-to-end on-device efficiency or quality preservation.

<span id="explanation-dac-2026-research2313"></span>

## Weaver: score-stratified MoE offload helps only when approximation and overlap preserve serving quality

Mixture-of-Experts (MoE) inference routes each token to a small subset of expert networks, but the full expert pool can exceed accelerator memory. Offloading experts to the CPU makes more models fit, at the cost of transfers and CPU/GPU scheduling. The useful overlap window is real only when CPU work, GPU attention, memory copies and the interconnect have independent capacity; otherwise prefetching simply moves contention earlier.

Weaver is described as ranking or stratifying experts by score. Low-score experts are executed on the CPU during GPU attention using prior-layer inputs, high-score experts remain accuracy-critical, and the framework combines proactive stratified prefetching with reactive balancing of remaining work. This can use otherwise idle CPU cycles and prioritize scarce transfer capacity. It does not establish what the score means, how low-score expert inputs are approximated, how routing changes are handled or whether the scheduler remains valid when expert popularity shifts.

The first gate is model correctness. Define the approximation operator and compare exact versus scheduled expert outputs, routing decisions, perplexity and task metrics across prompts, context lengths, long sequences, bursty routing and distribution shifts. Report worst-case degradation, failed requests, numerical error and any fallback to exact execution. “Maintaining model quality” requires a stated metric and tolerance, not only a speed ratio.

The second gate is complete serving accounting. Fix model, top-k routing, precision, device memory, CPU/GPU hardware, interconnect, concurrency and quality target. Measure CPU/GPU utilization, transferred bytes, prefetch accuracy, memory pressure, queueing, synchronization, p50/p95/p99 latency, throughput, energy and the cost of score computation and scheduling. Compare GPU-only execution, unstratified offload and prefetching with the same end-to-end latency boundary. A higher average speed can coexist with worse tail latency or lower utilization under a different request mix.

The official description reports 1.47–3.58× speedup over state-of-the-art offloading systems on three MoE models while maintaining model quality. The captured evidence does not identify the models, approximation, quality metric, hardware, bandwidth, memory, absolute or tail latency, CPU utilization or workload conditions. It supports stratified MoE offload scheduling, not demonstrated robust quality-preserving speedup across workloads or devices.

<span id="explanation-dac-2026-research1449"></span>

## Maple: data-transfer-aware NDP mapping must survive bank, queue, and model-execution constraints

Near-DRAM processing (NDP) places some computation close to memory so that an edge accelerator does not move every operand through the same interface. That shifts the mapping problem: performance depends not only on where an operator executes, but on how tensor partitions are assigned to banks or NDP resources, which transfers are bound to which paths, and whether those transfers overlap without queueing. A mapping that minimizes an abstract byte count can still overload one bank or serialize on a shared controller.

Maple is described as an address-mapping-based exploration framework that jointly searches resource grouping, tensor partitioning and transfer binding for a specified workload and xPU-NDP architecture. The joint search can expose interactions that a compute-centric mapper misses. It does not establish the address semantics, legal partition constraints, synchronization, DMA/coherence behavior, NDP kernel support, search budget or whether the objective is a measured hardware result or a model estimate.

The first gate is mapping legality and functional correctness. Check ownership and alignment of every tensor partition, bank/resource capacity, ordering, synchronization, remote accesses, reductions, NDP instruction support and reconstruction of the original operator. Compare mapped outputs with a reference under the stated precision and report unsupported operators, invalid mappings, retries, compiler failures and model-quality changes. Transfer reduction is not useful if it changes the computation or requires uncounted repair.

The second gate is complete movement accounting. Measure bytes and reuse, bank and interconnect utilization, contention, queueing, stall time, DMA and synchronization overhead, NDP/xPU utilization, memory energy, preprocessing, kernel launch, compilation and mapping-search cost. Compare compute-centric NDP and conventional edge mappings with the same model, tensor shapes, precision, memory capacity, bandwidth, architecture, runtime and latency/energy boundary, including tail latency and per-workload results.

The official description reports up to 3.34× performance improvement and 1.49× energy improvement over existing approaches on mainstream NDP architectures. The captured evidence does not expose model/operator details, NDP organization, bandwidth, absolute latency or energy, traffic accounting, search cost, quality conditions or per-workload distributions. It supports data-transfer-aware NDP mapping exploration, not demonstrated portable end-to-end edge-LLM improvement across NDP architectures.

<span id="explanation-dac-2026-research1938"></span>

## Phantom Walk: disseminating translations trades page-walk latency for metadata traffic and coherence work

Unified virtual memory lets multiple GPUs address a shared allocation, but a page migration changes which GPU owns or maps a page. The migration can invalidate translation lookaside buffer and page-table state on other GPUs. A later access then pays a migration-induced translation miss (M-miss), including a local fault, page-table walk or interconnect request before the data access can proceed. Reducing that post-migration path is different from reducing migrations themselves.

Phantom Walk is described as proactively disseminating translation information after migration so that a GPU can resolve an M-miss through a shorter path instead of repeating a full local fault and page-table walk. The mechanism must define which PTEs or translation entries are sent, when dissemination occurs, how ownership and permissions are represented, and how invalidation and races are handled. A translation that arrives early can save a walk; a stale or unnecessary translation can consume metadata bandwidth, cache capacity and coherence work.

The first gate is translation correctness. Fix page size, address-space and protection semantics, migration ownership, invalidation ordering, concurrent faults, retries, prefetch races and process isolation. Verify that every served translation maps to the current physical page and permissions, and that no stale entry can expose or corrupt data. Measure M-miss rate, TLB/page-walk components, dissemination hits, stale/duplicate messages and migration-induced data traffic separately.

The second gate is complete multi-GPU accounting. State GPU count and models, TLB/page-table hierarchy, interconnect, driver/runtime, page-migration policy, memory capacity, page size and workload. Include dissemination messages, invalidations, synchronization, queueing, contention, data movement and energy, and report average and tail latency plus application throughput. Compare advanced migration policies with and without Phantom Walk under matched mappings, workloads, warmup, concurrency and platform configuration; an average speedup can hide regressions when several GPUs contend for translation bandwidth.

The official description reports a 44.37% average overall performance improvement. It does not provide GPU configurations, application suite, M-miss breakdown, translation hit rate, migration traffic, metadata overhead, stale-state handling, tail latency or energy. The evidence supports proactive post-migration translation dissemination, not demonstrated universal multi-GPU performance improvement or bounded coherence cost.

<span id="explanation-dac-2026-research1322"></span>

## Keeping PIM Busy: removing host and bank stalls must survive the complete request path

Processing-in-memory (PIM) places arithmetic near memory arrays, but useful throughput depends on feeding the PIM cores with operands, scheduling requests across channels and banks, and draining results. A low core-activity fraction can indicate that execution units are starved by host communication or request generation; it does not by itself identify which bottleneck dominates every workload or prove that adding parallelism will scale.

The described co-design uses Channel-Level Burst (CL) for autonomous per-channel operand generation, PDMA for PIM-oriented request scheduling, and an integrated PIM core for multi-batch execution. These mechanisms target different gaps: host/device serialization, insufficient DMA request production and per-bank batch serialization. They must preserve address ordering, operand placement, synchronization, visibility and numerical semantics while avoiding a new bottleneck in PCIe, command queues, bank conflicts, buffers or host coordination.

The first gate is request correctness and utilization accounting. Define the PIM programming model, GEMM tiling, operands, address mapping, bank/channel conflicts, batch dependencies, ordering, precision and completion semantics. Break execution into host preparation, communication, request generation, queueing, bank service, PIM arithmetic, synchronization and result transfer. Report channel/bank utilization, queue occupancy, stalls, traffic, overlap and core activity; component speedups are not additive or necessarily multiplicative when they share the same path.

The second gate is complete system comparison. State memory technology, channels, banks, bandwidth, PCIe/interconnect, PIM frequency, host CPU, emulator fidelity and energy measurement. Compare baseline multi-channel PIM, conventional DMA, serialized bank execution, CPU and GPU under matched GEMM/LLM shapes, batch, sequence length, precision, memory capacity, software and thermal/power conditions. Include setup, data movement, idle power, synchronization, compiler/runtime and multi-tenant contention in throughput and energy results, and validate emulator timing against an implementation or calibrated model.

The official description reports 6.55% baseline PIM-core activity, component speedups of 9.10×, 29.6× and 102.4×, and a 145.8× combined improvement over baseline across GEMM microbenchmarks and four LLMs; it says PIM surpasses CPU throughput and approaches GPU efficiency for memory-bound decode. It does not provide absolute throughput, traffic, energy, emulator validation, shapes, channel/bank configuration or component interaction conditions. The evidence supports a PIM request-generation and execution-overlap direction, not demonstrated hardware-level full-throughput or GPU-comparable efficiency.

<span id="explanation-dac-2026-research1909"></span>

## PIMony: concurrent PIM and host access needs a correctness-preserving memory schedule

Edge LLM inference can use PIM to perform matrix operations near DRAM, but the same DRAM must also serve ordinary host loads, stores and runtime traffic. If PIM holds a bank or channel too long, a host request waits; if the controller interleaves work too aggressively, row conflicts, queueing and synchronization can erase the benefit. Stable token latency is therefore a scheduling and memory-timing claim, not simply a property of placing MACs in DRAM.

PIMony is described as combining interrupt-based asynchronous PIM, which makes MAC execution preemptible, with Dual-Path Subarray Access (DPSA), which uses dual-row activation to permit PIM and conventional memory access within one bank. The design aims to avoid channel-wide stalls while allowing co-execution. It must define preemption points, partial-MAC state, priority and fairness, row activation/timing constraints, data hazards, visibility and recovery; dual-row activation must also be checked for circuit feasibility, disturbance, retention and standard compatibility.

The first gate is memory correctness. Fix address mapping, row/bank ownership, atomicity, ordering, coherence, refresh, ECC, read/write hazards and PIM result visibility. Test concurrent PIM and host accesses with adversarial bank conflicts, preemption at every legal point, interrupts, resets and dependent loads. Report lost/duplicated operations, stale data, retries, ECC events and correctness against a CPU or non-PIM reference.

The second gate is interference accounting. State DRAM organization, timing parameters, channel/bank count, PIM frequency, host processor, interconnect, controller policy, LLM model and decode workload. Measure PIM and host throughput, token latency distribution, queue occupancy, bank conflicts, preemption frequency, channel utilization, bandwidth, energy, area and timing closure. Compare blocking PIM, host-only memory access and any conventional overlap mechanism under matched memory traffic, batch/sequence, power mode and measurement boundary; average latency can hide host-tail or PIM-tail regressions.

The official description claims improved co-execution efficiency and stable LLM decoding latency under concurrent PIM and memory accesses through asynchronous preemptible MACs and DPSA. It supplies no numerical throughput, latency, energy, area, timing, interference, DRAM configuration, reliability, or silicon/simulation evidence. The evidence supports concurrent DRAM-PIM access as a design direction, not demonstrated minimal interference or deployable hardware benefit.

<span id="explanation-dac-2026-research1560"></span>

## LOHA: splitting graph traversal from re-ranking only helps when recall and the full I/O path are preserved

Graph-based approximate nearest-neighbor search (ANNS) follows links among candidate vectors. A query repeatedly chooses candidates, reads graph or vector data, computes distances, and decides which nodes to visit next. At billion-scale, random SSD reads can dominate the critical path. Product quantization (PQ) reduces vector storage and distance-work cost, but it also introduces decoding and approximation choices that must remain part of the quality measurement.

LOHA is described as a CPU-storage hybrid. The CPU performs graph traversal, an in-storage accelerator performs PQ re-ranking using SSD-level parallelism, and speculative re-ranking pipelines the stages. Decoupling can expose parallel work, but the next traversal decision depends on the re-ranking result. A speculative result that arrives late, is unnecessary, or changes candidate ordering can add reads and buffering without reducing query latency or preserving the same search quality.

The first correctness gate is retrieval equivalence. Hold the graph, PQ codebook, distance metric, candidate queue, visited set, search parameters, termination rule and top-k output definition fixed. Report recall@k, result agreement, distance error and failures on queries with different graph traversal patterns. If LOHA changes pruning or accepts an approximate ranking to gain throughput, that is an algorithmic quality tradeoff and must be measured separately from the storage architecture.

The second gate is complete-path accounting. Include CPU traversal, SSD command setup, flash reads, controller and accelerator work, PQ decode, re-ranking, result transfer, speculation, queueing, synchronization and host scheduling. Report useful and speculative reads, read amplification, bytes moved, SSD-channel utilization, buffer occupancy, cache state, tail latency, throughput and energy/query. SSD parallelism can raise internal bandwidth while host-device transfers or dependent traversal still determine end-to-end latency.

The official description claims up to 9.6×, 6.2× and 4.0× throughput improvements over CPU, GPU and in-storage architectures. It does not provide datasets, recall targets, query distributions, SSD or accelerator configuration, I/O volume, latency, energy, speculation accuracy, or baseline tuning. The evidence supports a CPU-storage ANNS co-design direction, not demonstrated recall-preserving end-to-end latency or universal throughput improvement.

<span id="explanation-dac-2026-research1365"></span>

## AiMX graph compilation: removing host movement matters only when kernel coverage and model behavior remain intact

In a hybrid PIM system, the graph describes operators and the tensors flowing between them, while the hardware determines which operators can execute near memory. A tensor layout that is convenient for one AiMX kernel may require a reorder before another kernel or before the CPU consumes the result. The useful quantity is therefore not just PIM arithmetic time but the complete sequence of layout changes, transfers, synchronization and execution.

The described compiler simplifies the graph to increase AiMX-kernel coverage, uses DMA-assisted tensor reordering and layout redefinition to move preprocessing away from the CPU, and fuses operators to suppress redundant transfers. Integrated with ONNX Runtime, it targets both LLM prefill and decode. These transformations can reduce host work, but each must preserve tensor shapes, layouts, data types, quantization, ordering and numerical semantics. An operator that is unsupported or fused under a different precision can shift work back to the CPU or change model output.

The first gate is graph and kernel correctness. Enumerate supported operators and fallback paths, validate layout transformations and fusion boundaries against a reference execution, and test dynamic shapes, sequence lengths, batch sizes and numerical tolerances. “Kernel coverage” should identify the fraction of operations, bytes or execution time covered; a higher operation count does not necessarily remove the dominant transfer.

The second gate is end-to-end movement accounting. Include graph compilation and specialization, layout planning, DMA setup, CPU reorder work, CPU–AiMX transfers, AiMX execution, synchronization, output conversion, fallback kernels, queueing and cache effects. Separate prefill from decode, report transfer bytes and reorder time, and include compiler overhead and model-loading costs when claiming user-visible latency or throughput.

The official description profiles SK hynix AiMX and attributes 50.07% of prefill and 78.36% of decode time to CPU–AiMX communication and CPU-side reordering; it reports 2.00–2.73× prefill and 18.50–38.29× decode speedups, comparable to hand-tuned AiMX execution. It does not provide models, sequence lengths, operator coverage, AiMX configuration, transfer accounting, compiler cost, baseline tuning or numerical correctness results. The evidence supports graph-level PIM data-movement co-optimization, not a general LLM speedup or hardware-independent result.

<span id="explanation-dac-2026-research2432"></span>

## Hybrid PIM architecture/dataflow: Pareto search is useful only if the heterogeneous path remains correct and fully accounted

LLM inference repeatedly applies matrix and attention operations to weights, activations and state. A conventional NPU can provide substantial arithmetic throughput, but moving operands between compute and memory can dominate when models or intermediate tensors do not fit close to the arithmetic units. Processing in memory (PIM) changes that balance by placing some computation near stored data. DRAM contributes capacity, while the described SOT-MRAM-PIM component contributes a different compute/bandwidth point. The central design question is therefore not simply whether PIM is faster; it is which operation and tensor should use each resource, and what transfers, reductions and synchronization that choice creates.

The paper is described as a hybrid architecture/dataflow co-design. It combines SOT-MRAM-based PIM with DRAM capacity and existing NPU-PIM resources, then searches adaptive compute schedules and dataflow configurations with NSGA-II multi-objective exploration. That search changes the placement and scheduling proposal mechanism. It does not by itself establish that every supported operator has a legal PIM implementation, that partial results are reduced in the right order, or that the selected point preserves the original LLM outputs. The implementation must specify operator coverage, tensor partitioning, address mapping, precision and accumulation, ownership and visibility, fallback execution, and how NPU, DRAM-PIM and SOT-MRAM-PIM queues synchronize.

The first gate is numerical and functional fidelity. Define the model, tokenizer, precision, quantization, attention/KV-cache handling, layer partition, reduction semantics and allowable approximation. Compare logits, perplexity or task quality with a conventional NPU reference across prefill and decode, sequence lengths, batch/concurrency and model sizes. Record unsupported operators, data conversions, retries, dropped work, partial-result errors and fallback time. A dataflow that lowers modeled traffic while changing the output or silently omitting a layer is not an equivalent inference result.

The second gate is movement and contention accounting. Separate weight and activation transfers, KV-cache traffic, staging, bank/channel service, interconnect, queueing, launch, synchronization, reduction, idle/leakage power and thermal limits. Report NPU, DRAM-PIM and SOT-MRAM-PIM utilization, memory capacity pressure, bytes per token, p50/p95/p99 latency, throughput, energy/token and power. Include model loading, mapping compilation, runtime scheduling and any data-layout conversion in the claimed boundary. Capacity, bandwidth, density, endurance and control overhead can make a nominally powerful SOT-MRAM-PIM resource a poor choice for a particular layer.

NSGA-II also needs a reproducible search boundary. State the dataflow representation, feasible hardware-resource budget, objectives and normalization, constraint penalties, population, generations, mutation/crossover, random seeds, simulator fidelity, stopping rule and search time. Report the Pareto front and per-workload choices rather than only the best point. Compare against a compute-centric NPU, NPU-PIM, fixed-dataflow DRAM-PIM and a tuned search or exhaustive baseline under the same model, precision, memory capacity, hardware budget, quality target and end-to-end time boundary. Validate selected mappings with a detailed timing/energy model or hardware; a fast search is not an end-to-end speedup unless its search and validation costs are included.

The official description reports up to 8.72× lower inference latency and 11.74× lower power consumption than NPUs, plus 6.24× lower latency and 7.76× higher power efficiency than NPU-PIM baselines. The captured record does not expose absolute values, model or layer conditions, traffic, area, quality, memory organization, search budget, simulator calibration, per-workload variation or hardware evidence. The evidence supports hybrid PIM architecture/dataflow exploration, not demonstrated quality-preserving, hardware-validated end-to-end LLM efficiency or universal superiority over NPU-PIM.

<span id="explanation-dac-2026-research2489"></span>

## Nash: neighbor-aware shared memory helps only when provenance, synchronization and metadata cost are correct

GPU AI kernels often stage values in shared memory so threads in a block can reuse them instead of fetching each value from global memory. The benefit depends on the access trace: a later request may reuse a value already loaded by the same block, or a value may be available through a neighboring SM only if the architecture provides a legal and timely path. A repeated address is not automatically a safe reuse opportunity because the value may have been overwritten, may not yet be visible, or may belong to a different synchronization phase.

Nash is described as a lightweight neighbor-aware shared-memory design. Its Source Location Table (SLT) tracks where data came from, detects subsequent requests that can reuse that data, and redirects redundant requests within or across neighboring SMs. This changes the lookup and placement path; it does not by itself define address identity, lifetime, ownership, barriers, atomic ordering, invalidation, bank mapping or the behavior of a miss/stale entry. The implementation must also define the neighbor communication path and how the SLT is updated when a thread writes or evicts a value.

The first gate is GPU memory-model correctness. Check that every redirected request receives the value written by the correct producer at the correct synchronization point. Test divergent control flow, partial tiles, writes, reductions, atomics, barriers, dynamic shapes and concurrent blocks. Compare outputs and numerical tolerances with an unmodified kernel, and report false hits, stale entries, duplicate or lost updates, retries and fallback accesses. Lower global-memory traffic is not useful if the kernel's computation changes.

The second gate is metadata and resource accounting. The SLT consumes storage, lookup energy, update bandwidth and timing; a neighbor path can add arbitration and synchronization. Measure SLT hit/redirection rate, false hits, metadata bytes, lookup latency, invalidations, extra barriers, shared-memory bank conflicts, SM/interconnect utilization, occupancy, register/shared-memory pressure, global/shared bytes, energy and p50/p95/p99 kernel latency. Include initialization, table maintenance and fallback work. A reduction in global traffic can be offset by lower occupancy or a serialized neighbor lookup.

Reuse is workload-dependent. Evaluate GEMM, convolution, attention, reductions and irregular AI kernels across tensor shapes, block sizes, reuse distances, batch/sequence lengths, contention and access distributions not used to tune the policy. Compare default shared-memory layout, optimized tiling/caching and global-memory execution with the same GPU, compiler, launch resources, synchronization, precision and output-quality target. Report per-kernel and application-level results; a peak kernel speedup does not establish end-to-end acceleration.

The official description observes that up to 60.2% of subsequent memory requests reaccess data already loaded into shared memory and reports cycle-accurate simulation results of up to 18.3% performance improvement, 9.8% energy savings and 25.3% lower global-memory traffic. It does not expose absolute latency, bandwidth, occupancy, SLT overhead, kernel diversity, GPU configuration, simulator validation or hardware results. The evidence supports neighbor-aware shared-memory redirection, not demonstrated cross-GPU, kernel-general or end-to-end AI acceleration.

## COSM: coordinating memory use inside a device

COSM addresses concurrent CPU and processing-in-memory work. Its controller estimates available time at memory banks and the memory bus, then admits compatible work. Sections 5–6 describe interruptible execution and scheduling of computation with transfers. The causal idea is to use available resources without extending the wait for the CPU's next memory access. [COSM, sections 5–6](https://arxiv.org/html/2606.30553v2#S5)

Section 8.1 identifies Ramulator2 simulation and modeled LPDDR5 memory. Mobile application traces are collected from a phone, but those traces do not make the proposed controller a measured phone implementation. The comparison includes All-Bank Command, Chopim, and AsyncDIMM-Bank. The abstract reports up to 2.8× throughput with less than 2.0% CPU loss; the introduction separately states 2.6× and less than 2.2%. Those statements require their experiment contexts before being combined. [COSM, sections 1 and 8.1](https://arxiv.org/html/2606.30553v2#S8.SS1)

## DisDP: separating communication from training computation

DisDP moves training communication to programmable network devices and optimizer-state storage to a parameter server. This changes which resources perform the work. Section IV-C ties the 3.98× result to ZeRO-Infinity on a 175-billion-parameter model, reporting up to 134 tokens per second. [DisDP, section IV-C and Figure 16](https://arxiv.org/html/2409.00918v2#S4.SS3)

The paper's larger scaling study uses simulation in section IV-F. Its 32-GPU cost comparison also uses simulated throughput in section IV-H. Some ablations in section IV-E are simulated because the authors could not run the isolated variants. Section IV-D reports a case favoring the comparison system: with two GPUs and no concurrent matrix computation, NCCL has 28% higher communication bandwidth, attributed to the tested network device's transfer capability. [DisDP, sections IV-D–IV-H](https://arxiv.org/html/2409.00918v2#S4.SS4)

<span id="explanation-dac-2026-research1331"></span>

## Marlin reduces the amount and timing of prefix KV retrieval

During autoregressive LLM inference, the model processes a prompt and produces tokens one at a time. Attention for a new token needs key and value tensors from earlier tokens. These tensors form the KV cache. A long shared prefix can make the cache larger than GPU memory, so part of it is placed in host memory or storage. The resulting delay is not only the time to compute attention; the system must locate the needed KV data, transfer it, and make it available before the dependent attention work can finish.

Marlin is described as an I/O-efficient prefix KV-cache retrieval system. It uses three linked ideas: a dispersion-based token selector precomputes a compact, query-agnostic subset of important prefix tokens; a sensitivity-guided head classifier assigns different retrieval policies to prefix-sensitive and query-sensitive attention heads; and an overlap-optimized pipeline transfers head-specific KV data while attention computation proceeds. [Recorded evidence](../observed-subthemes/data-movement-and-locality.md#paper-dac-2026-research1331)

## Why token selection changes the retrieval problem

Retrieving every prefix token preserves the full cache but can exceed memory and I/O budgets. Selecting fewer tokens reduces transferred data, but the selector must preserve the information that matters for the next query. A query-agnostic subset is computed before the new query is known, so it cannot optimize for every future query. The method therefore needs a stated criterion for token importance and a bound or measured effect on attention output and model quality.

Dispersion is a selection signal, not correctness by itself. Tokens that are spread out in a representation space may cover different prefix content, but a compact subset can still omit a token that matters for a particular query. The evaluation must compare selected-cache attention with full-prefix attention and then compare the resulting model task quality, not only retrieval volume.

## Why heads need different policies

An attention head computes weights between the current query and stored keys, then combines the corresponding values. Different heads can use the prefix differently. A prefix-sensitive head may need information from the shared prefix regardless of the current query. A query-sensitive head may need to retrieve a smaller or more targeted set based on the new query.

The classifier assigns retrieval policies based on that sensitivity. The classification itself has a cost and can become invalid when the model, prefix distribution, context length, or request type changes. A policy that saves I/O for one head can also change the timing of its attention computation; the system must account for head scheduling, buffer capacity, transfer granularity, and synchronization.

## Why overlap is a scheduling claim, not free latency

Overlapping KV transfer with attention is useful only when the two activities use independent resources and the computation has enough ready work. If attention waits for a particular head's KV data, or if transfers share a bus, storage queue, memory controller, or buffer, the operations still serialize. The system also needs a fallback for a cache miss or a selected subset that arrives late.

The causal latency question is therefore: how much TTFT is spent waiting for offloaded KV data, how much of that wait can be hidden behind useful attention work, and what extra work is introduced by selection, classification, scheduling and reconstruction? A reduced I/O volume and an overlapped pipeline are separate mechanisms and should be measured separately.

## What the available source establishes and leaves open

The official DAC description establishes the long-prefix capacity problem and Marlin's three-part direction: dispersion-based compact token selection, sensitivity-guided head policies, and overlap of head-specific KV transfers with attention. It claims lower TTFT than state-of-the-art methods while maintaining comparable model accuracy.

The available source does not provide model or prefix identities, context lengths, cache size, storage/link hardware, selector cost, head-classification cost, overlap schedule, TTFT values, accuracy metric, concurrency, cache reuse, or a full end-to-end energy result. The evidence supports a precise question: can a query-agnostic compact prefix representation and head-specific retrieval hide enough offload cost to reduce TTFT without unacceptable model-quality loss? It does not support a universal TTFT or accuracy claim.

<span id="explanation-dac-2026-research2345"></span>

## Scoutattention: layer-ahead CPU work helps only when KV dependencies and overlap remain correct

Long-context inference stores keys and values from previous tokens so each new token can perform attention. When the KV cache exceeds GPU memory, moving it to CPU/DRAM saves capacity but adds transfers and can leave the GPU waiting for data or CPU computation. The useful system result is therefore the complete per-token path, not only the amount of cache moved or the speed of one CPU kernel.

ScoutAttention is described as combining GPU--CPU collaborative block-wise sparse attention, a layer-ahead CPU pre-computation algorithm that starts attention one layer early, and asynchronous periodic recall to keep CPU work small. These mechanisms change where KV attention is computed and when its result is prepared. They require a precise dependency/version protocol: the CPU must use the correct KV and intermediate state for the corresponding layer and token, and a late or stale result must trigger a defined fallback rather than silently changing the model computation.

The first gate is attention and quality fidelity. Define block sparsity, recall period, layer ordering, freshness checks, missed/late blocks, fallback, precision and synchronization. Compare logits and final model quality with exact GPU-resident attention across context and generation lengths, token positions, prompts, batch/concurrency and distribution shifts. Report attention/output error, task quality, rare failures and whether the stated 2.4% accuracy difference is relative or absolute and which metric it uses.

The second gate is overlap and total serving cost. Measure CPU sparse-attention time, GPU idle time, transferred bytes, link occupancy, queueing, synchronization, precompute lead time, recall stalls, peak memory, first-token latency and per-token p50/p95/p99 latency for cold and warm cache states. Separate prefill and decode, include CPU/GPU/link power and the cost of block selection, recall, scheduling and fallback, and compare GPU-resident KV, naive offloading and existing offload methods with the same model, precision, context, hardware, link, memory capacity and quality boundary.

The official description reports accuracy within 2.4% of baseline and 2.1× speedup over existing offloading methods. It does not expose model/context conditions, accuracy definition, memory reduction, transfer trace, CPU/GPU/link settings, tail latency, energy or complete prefill/decode accounting. The evidence supports collaborative KV offloading with layer-ahead CPU pre-computation, not demonstrated quality-preserving long-context serving or universal speedup.

<span id="explanation-dac-2026-research1632"></span>

## ECPrefix: erasure coding can spread hot KV state only if reconstruction and queueing stay within the serving path

Prefix KV caching stores the key and value tensors produced for a shared prompt prefix so that later requests do not recompute them. Replication makes several copies available, but hot prefixes can still overload the few nodes holding those copies. Erasure coding instead divides the cache into encoded blocks distributed across nodes; a reader reconstructs the needed object after obtaining enough blocks. That can spread storage and reads, but it also introduces coding, metadata, network and reconstruction work.

ECPrefix is described as organizing hot prefixes as profile-guided objects, distributing erasure-coded blocks with adaptive striping, and pipelining reads. These mechanisms change placement and retrieval scheduling. They do not establish the code rate, block size, reconstruction threshold, consistency rules, failure behavior or whether reconstructed KV tensors are exactly the intended cache. A cache that is structurally available but stale, incomplete or numerically altered can change model output.

The first gate is cache correctness. Define the object version, block layout, code parameters, placement, read quorum, reconstruction path and behavior when blocks are missing or stale. Compare reconstructed KV tensors and model outputs with the replicated or recomputed reference across long prefixes, attention heads, numerical precision and cache updates. Report reconstruction failures, retries, dropped requests and output-quality differences.

The second gate is serving-system accounting. Measure per-node compute, memory, network and storage load; encoded bytes and read amplification; encoding/decoding cost; queue depth; throughput; p50/p95/p99 TTFT; inter-token latency; and recovery time. Vary prefix skew, context length, concurrency, cache hit rate, node count, link capacity and failures. Compare replication and existing serving systems with the same model, prompts, cache state, cluster, scheduler and complete latency boundary. A lower average TTFT can coexist with worse tail latency or higher total resource use.

The official description reports up to 52.3% lower time-to-first-token than existing systems. The captured evidence does not expose absolute or tail latency, workload traces, coding parameters, cluster conditions, overhead, load distribution, failure recovery or model-output correctness. It supports an erasure-coded prefix-cache load-balancing direction, not demonstrated robust end-to-end LLM serving improvement across clusters or failures.

<span id="explanation-dac-2026-research1441"></span>

## Adaptive token-fluctuation prediction: a small KV cache helps only if recovery and prefetch preserve the dependency path

During autoregressive decoding, a language model produces one output token at
a time. Attention for the next token reads keys and values produced for earlier
tokens. The collection of those tensors is the key-value (KV) cache. A long
context can make the full cache too large or too expensive to read from the
fastest memory, so a system may retain only a small resident portion and fetch
other entries when needed.

Evicting a KV entry is not equivalent to forgetting an irrelevant token. Its
importance depends on the future query, attention head, layer, numerical
representation and task. A static predictor can therefore make a locally
reasonable choice that becomes wrong after token demand changes. If eviction is
irreversible, the system may preserve the wrong subset and permanently change
the attention result. A predictor that scores every request synchronously has a
different failure mode: its decision work can sit directly in front of the
attention operation it is meant to accelerate.

The described method combines three ideas. Adaptive Prediction models changes
in token demand rather than assuming a fixed access pattern. Reuse-based
recovery attempts to make previously evicted KV entries useful again instead of
treating an eviction as permanent loss. Decoupled Prefetching separates the
prediction/transfer path from attention so that data movement can proceed while
ready attention work executes. These are related but distinct mechanisms: a
better prediction can reduce misses, recovery can limit the damage of a miss,
and overlap can hide a transfer only when the required data arrives before its
dependent computation.

The cache contract must be explicit. Define what “256 tokens” means: tokens per
layer, per request, per sequence, or a shared system budget; state whether keys
and values, metadata, and temporary buffers are included; and specify precision
and eviction granularity. “Matches full-KV accuracy” also needs an accuracy
quantity, task set, tolerance, decoding settings and whether the comparison is
exact output, likelihood, retrieval quality or downstream task score. A compact
cache can match one aggregate score while changing rare but important requests.

Prefetching is a deadline problem. If a KV transfer takes `t_transfer` and the
attention work that can safely overlap it takes `t_overlap`, the exposed wait is
at least `max(0, t_transfer - t_overlap)` in a simple isolated model. The
actual path adds predictor time, queueing, memory contention, synchronization,
reconstruction and late or incorrect prefetches. A “decoupled” implementation
does not prove zero latency; it changes where the wait may be hidden. Measure
transfer completion relative to the exact attention dependency, not merely
average link utilization.

The comparison must separate full-KV execution, static token prediction,
on-the-fly scoring and the proposed adaptive/recovery/prefetch combination.
Hold model, context length, prompt distribution, decoding parameters, memory
capacity, transfer path, batch and concurrency constant. Ablate adaptive
prediction, recovery and decoupled prefetching individually. Report predictor
accuracy or miss quality, recovered-entry usefulness, transferred bytes,
prefetch precision/recall, cache occupancy, exposed transfer time, TTFT,
time-between-tokens, tail latency, output quality and energy. Count predictor
and recovery overhead in end-to-end time.

The official description reports that a 256-token cache matches full-KV
accuracy and an average 2.50× end-to-end speedup on long-context decoding.
Those are bounded description claims. The captured source does not identify the
models, context lengths, cache hierarchy, processor, bandwidth, predictor
overhead, accuracy tolerance, concurrency, transfer implementation or averaging
weights. The evidence supports an adaptive KV-cache/prefetching direction, not
demonstrated accuracy preservation or universal long-context speedup across
models and memory systems.

The decisive follow-up is a held-out request and context-length evaluation with
an independent full-KV reference. Include demand shifts that defeat static
prediction, late-transfer cases, cache-pressure sweeps and concurrent requests.
Publish per-request quality and latency distributions, not only averages, and
show whether the predictor/recovery work repays the bytes and waiting time it
adds.

<span id="explanation-dac-2026-research2268"></span>

## TierANNS: CXL tiering helps graph search only if placement follows the search dependency

Approximate nearest-neighbor (ANNS) search returns vectors close to a query without examining every vector. A graph-based index stores links between candidate vectors. Search follows those links, evaluates distances, and maintains a priority queue of candidates to visit or return. The graph makes search selective, but it also creates irregular, query-dependent memory accesses. A large index may therefore exceed local memory even when the arithmetic for each distance calculation is modest.

TierANNS, also described as COGA, targets that capacity and movement problem with CXL-extended memory. The proposed CXL-tailored priority queue is intended to keep useful candidate work moving while tolerating the higher latency of the extended tier. Queue hints then guide tiered placement and speculative access to graph-index data. This changes the location and timing of index reads; it does not make a remote read local, and it does not guarantee that a prefetched graph node will be useful for the eventual query.

The search semantics remain the first gate. The implementation must preserve the graph construction, distance function, candidate ordering, visited-set behavior, termination rule, and returned top-k result. A queue policy that favors requests that fill CXL bandwidth can still hurt recall if it delays a high-value candidate. Speculation can hide latency when its prediction is useful, but it can also consume bandwidth, cache space, and queue capacity on data that the traversal never needs. Report recall@k and result agreement against the same graph-search reference, not only link utilization.

Tier placement is a workload-distribution hypothesis. Nodes that are frequently visited across a query population may belong in the fast tier, while less likely nodes can use expanded memory. But graph locality can vary by query region, time, tenant, and index update. A static hot/cold classification can become wrong, and moving or duplicating index pages has construction, migration, metadata, and capacity costs. The evaluation should measure local and CXL traffic, speculative-hit and wasted-read rates, queue occupancy, page migrations, index-build overhead, and the effect of changing query distributions.

The decisive comparison is against conventional graph ANNS in local memory, a naive CXL memory extension, and static tiering, with the same graph, vectors, query set, recall target, software search parameters, memory capacity, and termination rule. Report QPS, mean and tail latency, recall@k, CXL bytes and requests, capacity scale, energy, and end-to-end cost. Include queue-management, hint-generation, page-placement, warmup, migration, and result-transfer time; proposal time alone is not search time.

The official description establishes the CXL-oriented priority queue, queue-hint-driven tiered placement, and speculative access direction. It supplies no numeric throughput, latency, recall, capacity, CXL bandwidth, or queue-overhead result, and it leaves the CXL generation, device latency, CPU platform, dataset, graph construction, query rate, and memory split unspecified. The evidence supports a promising CXL-aware graph-ANNS mechanism, not demonstrated scalable or high-speed ANNS performance under reproducible conditions.

<span id="explanation-dac-2026-research343"></span>

## SpecANNS: speculative in-storage search must preserve recall while reducing random I/O

Disk-based approximate nearest-neighbor (ANNS) search stores a graph index on flash or another storage medium. A query visits a candidate node, reads its neighbors or associated vectors, ranks them, and chooses the next candidates. Because the next hop depends on the current distances, graph traversal creates random page requests. If random I/O dominates the search, reducing arithmetic time alone leaves the critical path unchanged.

SpecANNS is described as an in-storage-computing design using an FPGA inside a computational-storage device (CSD) for distance computation. It also predicts pages likely to be needed in later graph-search hops and uses NAND parallelism to issue or service accesses together. The simple CSD interface may reduce host involvement, but it does not remove the dependency between a distance result and the next graph decision. A speculative page that arrives early is useful only if it is needed soon enough; an incorrect prediction consumes flash bandwidth, buffering, energy, and potentially endurance without advancing the query.

The first correctness gate is search equivalence. Hold the graph, vector representation, distance function, candidate queue, visited set, termination rule, and top-k output fixed. Compare recall@k and result agreement against a reference disk-based search, including queries whose traversals defeat the predictor. If the system changes the search order, prunes candidates, or accepts approximate distance results to gain speed, that is an algorithmic tradeoff and must be measured separately from the storage optimization.

The second gate is page-prediction usefulness. Classify each predicted read as useful and timely, useful but late, unused, duplicated, or harmful because it evicted or delayed a demanded page. Measure prediction precision and recall at the page/request level, extra reads, queue occupancy, page reuse, flash-channel utilization, read amplification, host/device traffic, and tail latency. A high NAND utilization number can coexist with worse query latency if the device is busy serving speculative work while a critical page waits.

In-storage distance computation also has a complete-path cost. The FPGA needs the query and vector data in a supported representation, performs arithmetic at a stated precision, and returns distances or candidate decisions through a device controller. Include query transfer, command setup, flash read, flash-to-FPGA movement, FPGA execution, result return, host scheduling, queueing, device reset, and CSD firmware work. Report FPGA resource use, clock, arithmetic precision, storage bandwidth, parallel channels, energy per query, and whether preprocessing or index construction is included.

The appropriate baselines include state-of-the-art disk-based ANNS on the same CSD or host, a conventional storage path without in-storage distance computation, a non-speculative in-storage design, and a predictor ablation with the same flash device. Hold dataset, graph construction, vector dimension, query distribution, recall target, search parameters, page layout, cache state, queue depth, concurrency, warmup, flash geometry, firmware, host, and measurement boundary constant. The official description reports that random-node I/O exceeds 90% of search time and qualitatively claims lower query latency and better energy efficiency on real CSD hardware, but provides no numeric latency, energy, recall, dataset, flash, FPGA, prediction, or wear result. The evidence supports speculative in-storage ANNS as a testable direction, not demonstrated end-to-end search improvement or recall preservation.

<span id="explanation-dac-2026-research2550"></span>

## MemFlow: a detailed contention model is useful only when its path and timing are validated

Disaggregated memory lets processors access memory that is pooled outside the processor package or local socket. The programming model may look like ordinary loads and stores, but a request can pass through a load-store queue, translation and cache hierarchy, coherence or ordering logic, a network interface, a scale-up fabric, a remote memory controller, and the return path. Several processors can compete for each queue, link, bank, controller, or buffer. The observed latency is therefore a property of the whole path, not just the remote DRAM access time.

MemFlow is described as a flow-centric simulator with modular, fine-grained abstractions for that path. A flow represents the progress and resource occupancy of a request as it moves through the system. This can expose interference that a model treating a remote access as one fixed delay would hide: queue buildup, cache misses, link arbitration, memory-bank conflicts, backpressure, and overlap between independent requests. The model can then support design-space exploration for changes intended to reduce contention.

The abstraction boundary must be explicit. A simulator can model an idealized protocol, a trace-driven implementation, or a cycle-level approximation of a particular hardware platform. “Complete path” does not establish that protocol ordering, coherence, retries, packetization, virtual channels, address mapping, cache replacement, prefetching, translation, interrupts, or software service time are represented. Each omitted mechanism can either create or remove contention. The simulator should expose which event consumes which resource, what causes a request to wait, and whether timing is deterministic, sampled, or calibrated from a trace.

Validation has at least three separate targets. First, component checks should compare queue, cache, link, controller, and arbitration behavior with analytical expectations or controlled microbenchmarks. Second, path checks should compare request latency, throughput, occupancy, and traffic distributions against a trace or measured platform under isolated and contended accesses. Third, workload checks should test whether the model reproduces application-level slowdown and interference across changing processor counts, locality, read/write mix, concurrency, and memory placement. Agreement on one average latency is not validation of a full contention model.

Design-space exploration adds another potential error source. An optimizer may favor a mitigation that improves the simulator's objective while exploiting an unmodeled cost, such as extra buffering, control traffic, fairness loss, coherence work, or tail latency. Every candidate must be evaluated with the same workload traces, warmup, cache state, topology, capacity, and timing boundary. Report simulation time and model complexity separately from predicted system performance, and include sensitivity to link bandwidth, remote-memory latency, queue depth, address interleaving, traffic burstiness, and arbitration policy.

The appropriate baselines include existing disaggregated-memory simulators with simplified access paths, a reduced MemFlow model with each added component ablated, and—where possible—hardware or trace references. Report validation error, rank correlation for design choices, p50/p95/p99 latency, throughput, queue occupancy, link utilization, memory-controller utilization, fairness, slowdown and energy assumptions. The official description reports fine-grained characterization and automatic mitigation exploration qualitatively, but no validation error, simulation speed, workload suite, contention result, mitigation gain, protocol detail, or hardware trace. The evidence supports a modeling direction, not demonstrated simulator fidelity or a hardware design improvement.

<span id="explanation-dac-2026-research701"></span>

## RAGNMP: near-memory elimination trees help only when retrieval recall and RAG evidence remain intact

Retrieval-augmented generation has two linked stages. A query is encoded and used to search a knowledge corpus; the selected passages then condition a language model. Vector search can be memory-bound because the system moves large embeddings and index structures before returning only a small candidate set. A retrieval accelerator therefore has to preserve which evidence is returned, not merely reduce the number of memory operations.

RAGNMP is described as a general-purpose near-memory processing accelerator for RAG. Its enhanced, quantified elimination tree jointly explores data placement, task parallelism and pipelining, while a flexible processing unit supports diverse memory-bound RAG operations and adapts to changes in RAG algorithms. These mechanisms change index traversal and where work executes. The captured description does not specify the tree construction, pruning/elimination bound, distance metric, top-k behavior, placement, synchronization, index updates or NMP technology.

The first gate is retrieval fidelity. Define embedding representation and precision, distance, tree construction, pruning threshold, tie behavior, top-k and recall target. Compare returned IDs, scores, recall/precision and tail queries against an exact or trusted ANN reference, then measure reranked evidence and downstream answer correctness/factuality. A faster candidate filter can remove the passage needed to answer correctly even when average search latency improves.

The second gate is the complete movement path. Include query encoding, index lookup, tree traversal, memory reads, near-memory computation, bank/processing-unit contention, interconnect, synchronization, candidate transfer, reranking, result formatting and generator input. Measure bytes, bandwidth, utilization, queueing, memory footprint, p50/p95/p99 retrieval latency and energy. Retrieval speed is not end-to-end RAG speed if reranking, transfers or LLM generation dominate.

Dynamic corpora need an update contract. Test insertions, deletions, rebalancing, placement changes, index freshness, concurrent queries/updates, corpus growth, distribution shift, hot/cold keys, failures and changing RAG algorithms. Include rebuild and update cost, stale-index behavior and consistency. Compare CPU/GPU vector search and memory-centric ANN accelerators with the same corpus, query set, recall/top-k, reranker/generator, hardware, batch, index freshness and retrieval-to-generation boundary.

The official description states that RAGNMP outperforms state-of-the-art RAG systems and accelerators, but reports no recall/precision, retrieval latency, throughput, energy, memory traffic, index-update cost, answer quality, factuality, absolute comparison or per-workload result. The evidence supports general-purpose near-memory RAG retrieval and elimination-tree exploration, not demonstrated ANN recall, dynamic-corpus robustness or end-to-end RAG improvement.

<span id="explanation-dac-2026-research1596"></span>

## PIMGRAG moves graph retrieval toward the data

Graph-based retrieval-augmented generation uses a knowledge graph and vector representations to find information before an LLM generates an answer. Retrieval may traverse graph relationships, compare vectors, rank candidates, gather associated text, and pass the selected context to later generation. These steps often perform relatively little arithmetic per byte moved: the system repeatedly fetches irregular graph links, vector elements, metadata, and candidate results.

PIMGRAG is described as a heterogeneous hardware/software design for this retrieval stage. Its PIM architecture executes bandwidth-intensive operations near memory to reduce off-chip transfers. Its software scheduler orchestrates PIM and GPU stages to reduce idle time. [Recorded evidence](../observed-subthemes/data-movement-and-locality.md#paper-dac-2026-research1596)

## Why graph retrieval is different from dense neural computation

Dense matrix operations can reuse regular blocks of data and keep arithmetic units busy. Graph retrieval often follows data-dependent neighbors and accesses vectors or metadata at locations that are not adjacent. The processor may spend time waiting for memory rather than multiplying values. Moving computation into memory can reduce the distance traveled by data, but it does not remove the need to read the graph, select neighbors, maintain intermediate candidates, or return the result.

The PIM operation must therefore match the retrieval algorithm. If it filters neighbors, computes partial similarity, or ranks candidates, the design must preserve the same graph traversal and ranking semantics as the baseline. A reduction in off-chip bytes is not automatically a reduction in retrieval latency if the PIM array has lower internal bandwidth, limited parallelism, or extra setup and result-transfer work.

## Why the heterogeneous schedule matters

PIM and GPU resources have different strengths. PIM can process data near memory, while the GPU may perform dense vector operations, aggregation, or later stages more efficiently. A scheduler decides which stage runs where and when its outputs become available. It must account for graph partitions, data dependencies, memory-bank contention, PIM/GPU transfer, queueing, synchronization, and the capacity of intermediate buffers.

Reducing GPU idle time is meaningful only if the PIM stage can supply work at the needed rate. If the GPU waits for candidate data, or if PIM waits for a graph update or a result buffer, the stages are not effectively overlapped. The schedule also needs a policy for skew: high-degree graph nodes can produce more work and create a straggler even when average bandwidth looks sufficient.

## Retrieval quality is separate from generation quality

Graph-RAG motivation often mentions factual consistency or interpretability. A retrieval architecture can preserve or accelerate a retrieval algorithm without proving that it retrieves the right evidence, improves answer factuality, or reduces hallucination. Those properties need separate measures: recall or ranking quality at the retrieval stage, context relevance, answer accuracy, citation correctness, and end-to-end generation latency.

Approximate filtering or partial ranking can reduce movement but change which context reaches the LLM. The evaluation must compare the retrieved nodes, vectors, and final answers against a reference system under the same graph, embedding model, query set, and generation settings.

## What the available source establishes and leaves open

The official DAC description establishes the problem of large vector and graph-data movement in graph-based RAG and the proposed division of labor: PIM performs bandwidth-intensive retrieval near memory, while a lightweight software scheduler coordinates PIM and GPU stages. It reports qualitative improvements in throughput, latency, and energy efficiency over CPU/GPU and existing PIM-based baselines.

It does not provide graph or model identities, graph scale, retrieval algorithm, PIM technology, GPU, memory capacity/bandwidth, partition policy, schedule, numeric throughput/latency/energy, retrieval quality, answer quality, or hardware implementation status. The evidence supports a precise question: can near-memory graph retrieval and heterogeneous scheduling reduce data movement without changing retrieval semantics or shifting the bottleneck to PIM/GPU coordination? It does not support a quantitative system-wide or factuality claim.

## What connects the cases

My synthesis is that resource ownership and timing matter alongside the quantity of data. COSM tries to share resources without harmful overlap. DisDP moves responsibilities to different resources so computation and communication can proceed together. Neither implies that data movement disappears. Both require identifying which activity waits, why it waits, and what changes that wait.

This interpretation is a comparison of mechanisms. It is not a comparison of their headline speedups: the workloads, machines, baselines, and measurements differ.

## The experiment needed for a broader conclusion

Measure complete job time and energy while varying data size, available memory, and competing work. Record bytes moved on each relevant path and time spent waiting for each resource. Include initial loading, format conversion, communication control, and collection of results.

Then remove the proposed change while holding the other conditions fixed. If the gain disappears, that supports the proposed causal explanation. If it persists because one system has more capacity or a different comparison configuration, the improvement needs a narrower explanation. This is the distinction the paper records below help investigate.

The source sections above were inspected for this editorial update on 7 September 2026. The older captured records below are retained as research history; these added source checks qualify their abstract-only descriptions.
