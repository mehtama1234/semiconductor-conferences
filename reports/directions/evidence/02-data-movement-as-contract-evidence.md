# Evidence dossier — Data Movement As Contract

This dossier combines the canonical direction atlas, historical adjudicated records, and dated editorial corrections. It is a source-backed reading aid, not an independent review or a claim that the records are comparable.

- Direction page: [Data Movement As Contract](../02-data-movement-as-contract.md)
- Source direction IDs: `data-movement-as-contract, workload-specialized-accelerators`
- Direction status: `provisional_mechanism_hypothesis`
- Independent reviews recorded: `0`

## Reading rule

`UNKNOWN` means a field is not recorded, not that the paper lacks the condition. Corrections supersede the current displayed fields while historical fields remain expandable. A historical condition-complete label does not establish that a correction has passed condition or independent review.

## CANNON: A CXL-Based Near-Memory Processing Architecture for Approximate Nearest Neighbor Search on Real Hardware

- Paper ID: `dac-2026-research108`
- Conference/edition: `dac` / `2026`
- Evidence tier: `Primary captured official DAC description plus existing authored CXL/ANN explanation; real-hardware claim is source-reported, but no full-paper extraction, reproduced query benchmark, recall validation or complete power/accounting trace`
- Ledger record: `dac/data/adjudicated-2026-batch.jsonl`

**Current evidence correction — 2026-09-09**

Deepens the CANNON treatment into a paper-level reading; separates real-CXL-hardware implementation, fully offloaded pipelining, asynchronous hashing and speculation from ANN recall semantics, CXL configuration, index/capacity conditions, full query-path accounting and RAG benefit, while preserving the up-to-two-orders claim.

Condition review of this correction and independent acceptance remain pending. The direction mapping is inherited, not revalidated by this update.

[Dated correction register](../../../data/editorial-paper-corrections-v1.json)

- Source: [https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH108](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH108)

| Field | Current record |
|---|---|
| Problem | CPU/GPU ANN systems face local-memory scaling limits, while SSD-backed tiers impose coarse-grained I/O latency on fine-grained vector accesses. |
| Mechanism / artifact | CXL-based near-memory processing architecture with fully offloaded, deeply pipelined ANN search, asynchronous hashing and speculative execution on real CXL hardware; index structure, distance path, hash policy, host/device partition and speculation recovery are unspecified. |
| Workload / benchmark | ANN search on large-scale vector datasets for AI/RAG-like retrieval; dataset identities, vector dimensions/distribution, distance metric, query load, top-k, recall target, index algorithm, batch/concurrency and update workload are unspecified. |
| Hardware / process | Real CXL near-memory hardware with an offloaded ANN pipeline; CXL generation/protocol, link width/speed, host CPU, device memory/capacity, NMP compute, storage format, controller, power/thermal setup, software stack and measurement boundary are unspecified. |
| Baselines | State-of-the-art CPU ANN systems; State-of-the-art GPU ANN systems; SSD-backed multi-tier architectures; Same dataset, index, metric, top-k/recall target, batch, concurrency, capacity, software, warm-up, power boundary and end-to-end retrieval path are unspecified |
| Metrics | The source reports up to two orders of magnitude performance improvement over CPU and GPU baselines on large-scale vector datasets, but does not report absolute throughput/latency, recall or accuracy tradeoffs, dataset-level results, QPS, p50/p95/p99 tails, memory footprint, bandwidth, power/energy, index-build/update cost or CXL configuration. |
| Evidence locator / span | DAC 2026 official description, first and final paragraphs; existing CXL/ANN data-movement explanation; captured Problem, Mechanism / artifact, Workload, Hardware, Baseline, Measurements and Limits fields; no full manuscript, dataset table, recall trace, CXL configuration or independent reproduction. |
| Limits | Asynchronous hashing and speculative execution must preserve the ANN retrieval contract. Compare returned IDs and distances with an exact or trusted reference; report recall@k, precision, ties, distance error, false omissions, candidate counts, discarded speculative work and tail-query behavior. Pipeline throughput without recall conditions is not an end-to-end retrieval result.; Real hardware does not make the configuration self-describing. Identify the CXL protocol, link, host/device memory, index placement, batching, concurrency, software and power/thermal boundary; measure query encoding, traversal, hashing, filtering, distance computation, synchronization, result transfer and reranking under matched CPU/GPU baselines.; The official description supports a real-CXL-hardware CXL/NMP ANN architecture and an up-to-two-orders performance claim, not demonstrated recall-preserving end-to-end ANN/RAG acceleration across workloads. Dataset identities, absolute latency/throughput, recall tradeoffs, capacity, updates and complete query-path accounting remain unresolved. |

<details markdown="1">
<summary>Historical captured record — superseded in the current table</summary>

Historical atlas evidence tier: `official_description`.

| Field | Historical record |
|---|---|
| problem | CPU/GPU ANN systems are constrained by local memory, while SSD-backed tiers impose coarse-grained I/O latency on fine-grained vector access. |
| mechanism | CXL-based near-memory processing with fully offloaded pipelined ANN search, asynchronous hashing, and speculative execution. |
| workload | Approximate nearest-neighbor search on large-scale vector datasets for AI/RAG-like retrieval. |
| hardware | UNKNOWN — not present in the current adjudicated record |
| baselines | state-of-the-art CPU ANN systems; state-of-the-art GPU ANN systems; SSD-backed multi-tier architectures |
| metrics | up to two orders of magnitude performance improvement |
| limits | The description does not provide recall/accuracy tradeoffs, CXL configuration, dataset identities, or absolute throughput/latency. |
| locator | CANNON implements a CXL near-memory-processing architecture on real hardware, uses a deeply pipelined ANN dataflow with asynchronous hashing and speculative execution, and reports up to two orders of magnitude improvement over CPU and GPU baselines on large-scale vector datasets. |

[Historical source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH108&sess=sess156)

</details>


Mapping review status: `not_recorded`; independent review status: `pending`.

## Ctxmem: OS-Hardware Co-Designed Tiered Memory with DRAM-SSD Hybrid CXL Devices

- Paper ID: `dac-2026-research1028`
- Conference/edition: `dac` / `2026`
- Evidence tier: `Primary captured official DAC description plus existing authored Ctxmem explanation; no full-paper extraction, reproduced GEM5 run, hardware measurement or persistence validation`
- Ledger record: `dac/data/adjudicated-2026-batch.jsonl`

**Current evidence correction — 2026-09-09**

Deepens the existing Ctxmem treatment into a paper-level reading; separates OS-hardware CXL tiering and DRAM/flash placement from page-fault migration policy, latency tails, persistence semantics and end-to-end workload benefit, while preserving the source's 1.4x execution-time and 2x throughput claims.

Condition review of this correction and independent acceptance remain pending. The direction mapping is inherited, not revalidated by this update.

[Dated correction register](../../../data/editorial-paper-corrections-v1.json)

- Source: [https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH1028](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH1028)

| Field | Current record |
|---|---|
| Problem | DRAM-flash hybrid CXL memory expansion addresses capacity but can suffer inefficient access and page-migration handling. |
| Mechanism / artifact | OS-hardware co-designed tiered memory with asynchronous page-fault handling, a dynamic direct-mapped DRAM cache, hardware hot/cold page profiling, and CXL-device offload of page-fault data movement. |
| Workload / benchmark | Large-scale memory expansion evaluated in GEM5 over DRAM/SSD hybrid CXL devices against conventional CXL-SSD; benchmark suite, working-set population, concurrency, fault mix and simulator configuration are unspecified. |
| Hardware / process | Byte-addressable CXL interconnect, DRAM cache, inexpensive flash/SSD storage and a CXL device with hardware profiling and migration support; link, queue, capacity, timing, flash behavior, OS implementation and hardware prototype assumptions are unspecified. |
| Baselines | Conventional CXL-SSD; Same workload, DRAM/SSD capacity, CXL link, simulator model, queueing, page size, OS path and measurement boundary are unspecified |
| Metrics | The source reports 1.4x execution-time improvement and doubled system throughput in GEM5, but does not report the benchmark distribution, p50/p95/p99 latency, page-fault rate, migration volume, bandwidth, CPU/OS overhead, energy, flash endurance, persistence behavior or hardware validation. |
| Evidence locator / span | DAC 2026 official description, first and final paragraphs; existing Ctxmem chapter explanation; captured Problem, Mechanism / artifact, Workload, Hardware, Baseline, Measurements and Limits fields; no full manuscript, benchmark matrix, simulator trace or hardware validation. |
| Limits | Asynchronous page-fault handling and device-side data movement do not by themselves establish lower application latency. Separate fault detection, host work, queueing, flash service, transfer, mapping publication and resumed execution; report page-fault latency distributions and tail behavior under concurrent faults, working-set changes and dirty-page eviction.; DRAM/flash tiering and an SSD-backed CXL path are capacity and placement mechanisms, not a persistence contract. Define clean versus dirty migration, writeback ordering, failure points, completion semantics, recovery and flash write amplification before making durability or endurance claims; none is reported here.; The GEM5 description supports OS-hardware co-designed CXL tiered-memory evaluation against conventional CXL-SSD, with 1.4x execution-time and 2x throughput claims. It does not establish general end-to-end memory-system improvement, real-hardware performance, tail-latency behavior, workload transfer, energy, endurance or durable-memory semantics because the conditions and validation are unspecified. |

<details markdown="1">
<summary>Historical captured record — superseded in the current table</summary>

Historical atlas evidence tier: `official_description`.

| Field | Historical record |
|---|---|
| problem | DRAM-flash hybrid CXL memory expansion suffers from inefficient access and migration models despite solving capacity constraints. |
| mechanism | OS-hardware co-designed tiered memory with asynchronous page-fault handling, dynamic direct-mapped cache, hot/cold profiling, and CXL-device migration offload. |
| workload | Large-scale memory expansion evaluated with gem5 over DRAM/SSD hybrid CXL devices. |
| hardware | UNKNOWN — not present in the current adjudicated record |
| baselines | conventional CXL-SSD |
| metrics | 1.4X execution-time improvement; 2X system throughput |
| limits | The description does not identify workload suite, CXL hardware assumptions, endurance effects, or tail-latency behavior. |
| locator | CtxMem offloads page-fault data-plane handling to a byte-addressable CXL device using a direct-mapped DRAM cache, hot/cold profiling, and OS-hardware page migration; gem5 evaluation reports 1.4X execution-time improvement over conventional CXL-SSD and doubled throughput. |

[Historical source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH1028)

</details>


Mapping review status: `not_recorded`; independent review status: `pending`.

## Achieving Intra- and Inter-Operator Communication Lower Bounds in Near-Memory Processing

- Paper ID: `dac-2026-research1113`
- Conference/edition: `dac` / `2026`
- Evidence tier: `Primary captured official DAC description plus existing authored RAF explanation; no full-paper extraction, reproduced dataflow analysis, compiler/runtime trace or measured hardware result`
- Ledger record: `dac/data/adjudicated-2026-batch.jsonl`

**Current evidence correction — 2026-09-09**

Deepens the RAF near-memory-processing treatment into a paper-level reading; separates tensor rotation and communication-lower-bound construction from the formal lower-bound assumptions, numerical/model fidelity, hardware cost and end-to-end LLM efficiency, while preserving the source's energy-reduction and speedup claims with their baseline mapping unresolved.

Condition review of this correction and independent acceptance remain pending. The direction mapping is inherited, not revalidated by this update.

[Dated correction register](../../../data/editorial-paper-corrections-v1.json)

- Source: [https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH1113](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH1113)

| Field | Current record |
|---|---|
| Problem | Distributed vault/channel organization makes near-memory dataflow optimization difficult and creates remote communication within and between LLM operators. |
| Mechanism / artifact | Remote-Access-Free (RAF) tensor-rotation dataflow with analytical minimization of intra-operator local access, data partitioning to remove inter-operator remote access, and operator fusion to reduce inter-operator local access; tensor layout, partition constraints, fusion legality and lower-bound proof conditions are unspecified. |
| Workload / benchmark | LLM near-memory-processing dataflows; model graphs, operators, tensor shapes, batch/sequence lengths, sparsity, precision, memory capacity, vault/channel counts, mapping corpus and accuracy checks are unspecified. |
| Hardware / process | Distributed near-memory processing organized into memory vaults/channels with local and remote access; memory technology, compute placement, interconnect, bandwidth, bank conflicts, frequency, area, power model, thermal limits, compiler/runtime and fabricated or measured hardware status are unspecified. |
| Baselines | IANUS; H2LLM; OptiPIM; Same models, precision, batch/sequence lengths, memory capacity, vault/channel organization, compiler/runtime, frequency, simulator or hardware boundary and accuracy target are unspecified |
| Metrics | The source reports energy reductions of 50.4%, 39.0% and 37.8% and speedups of 3.98x, 1.72x and 1.57x over IANUS, H2LLM and OptiPIM respectively, but does not identify the workload associated with each pair or report absolute latency/energy, communication bytes, remote/local accesses, utilization, capacity pressure, accuracy, area, thermal behavior or implementation status. |
| Evidence locator / span | DAC 2026 official description, first and final paragraphs; existing RAF/data-movement discussion; captured Problem, Mechanism / artifact, Workload, Hardware, Baseline, Measurements and Limits fields; no full manuscript, bound derivation, workload table, traffic trace or hardware validation. |
| Limits | A communication lower bound is conditional on the allowed data layout, operator graph, tensor dimensions, replication, memory capacity, vault/channel topology and definition of local versus remote access. Prove that the stated bound applies to the same feasible design space, and report bytes, messages, hops, synchronization, local-bank conflicts and metadata; eliminating remote accesses can increase local traffic, storage or imbalance.; Tensor rotation, partitioning and operator fusion must preserve tensor shapes, indexing, reduction order, precision and model semantics. Validate outputs against a trusted unfused/reference implementation across operators, sequence lengths, batch sizes, sparsity and numerical tolerances; a lower communication count is not an accuracy result, and fusion can change peak live storage and scheduling constraints.; The official description supports RAF as a constrained NMP dataflow direction and reports the 50.4%/39.0%/37.8% energy and 3.98x/1.72x/1.57x speedup claims, but it does not establish universal LLM/NMP efficiency or communication optimality. The metric-to-workload mapping, memory technology, capacity, hardware boundary, accuracy and end-to-end compiler/runtime costs remain unresolved. |

<details markdown="1">
<summary>Historical captured record — superseded in the current table</summary>

Historical atlas evidence tier: `official_description`.

| Field | Historical record |
|---|---|
| problem | Distributed vault/channel organization makes near-memory dataflow optimization difficult and creates remote communication overhead within and between operators. |
| mechanism | Remote-Access-Free tensor-rotation dataflow with analytical local-access optimization, partitioning, and operator fusion. |
| workload | LLM near-memory processing dataflows. |
| hardware | UNKNOWN — not present in the current adjudicated record |
| baselines | IANUS; H2LLM; OptiPIM |
| metrics | 50.4%, 39.0%, and 37.8% energy reductions; 3.98X, 1.72X, and 1.57X speedups |
| limits | The description does not map each metric pair to a workload, specify memory technology, or expose accuracy and capacity constraints. |
| locator | RAF dataflow uses tensor rotation to eliminate intra-operator remote access in distributed NMP vaults, then applies partitioning and fusion to reduce inter-operator access; it reports 50.4%, 39.0%, and 37.8% energy reductions and 3.98X, 1.72X, and 1.57X speedups over IANUS, H2LLM, and OptiPIM. |

[Historical source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH1113)

</details>


Mapping review status: `not_recorded`; independent review status: `pending`.

## Patterns Behind Chaos: Forecasting Data Movement for Efficient Large-Scale MoE LLM Inference

- Paper ID: `isca-2026-program-005`
- Conference/edition: `isca` / `2026`
- Evidence tier: `Primary author preprint plus released trace-dataset reference; no independent trace/insight check, wafer-scale reproduction or cross-topology placement validation`
- Ledger record: `isca/data/adjudicated-2026-batch.jsonl`

**Current evidence correction — 2026-09-08**

Reconciles the Patterns Behind Chaos card with the captured primary preprint and released trace dataset; explains MoE data movement, temporal/spatial routing structure, expert placement, prefill/decode differences, forecast staleness and topology-bound speedups from first principles.

Condition review of this correction and independent acceptance remain pending. The direction mapping is inherited, not revalidated by this update.

[Dated correction register](../../../data/editorial-paper-corrections-v1.json)

- Source: [https://arxiv.org/abs/2510.05497](https://arxiv.org/abs/2510.05497)

| Field | Current record |
|---|---|
| Problem | Large-scale MoE inference moves tokens to distributed experts, and routing-driven data movement can dominate serving latency, bandwidth and energy. |
| Mechanism / artifact | Data-movement-centric temporal/spatial profiling, distilled placement insights, lightweight wafer-scale architectural modifications and a prefill-aware expert-placement algorithm; forecasting model, horizon and fallback are unspecified. |
| Workload / benchmark | Four 200B–1000B MoE models released in 2025, more than 24,000 requests across diverse workloads, wafer-scale GPU architectures and existing GPU systems; routing traces, batch, topology and prefill/decode split conditions are not fully extracted. |
| Hardware / process | Wafer-scale GPU and multi-GPU serving systems; expert placement, memory capacity, link topology, bandwidth, congestion, software runtime, energy and architectural-modification assumptions are topology-specific. |
| Baselines | Existing GPU MoE serving systems; Existing expert-placement approaches; Model, trace, batching, topology, expert capacity, prefill/decode, software and quality parity require verification |
| Metrics | The primary preprint reports 6.6x average speedup on wafer-scale GPUs, up to 1.25x speedup on existing GPU MoE computation, more than 24,000 profiled requests and 200B–1000B model scale; exact page/table locations and aggregation conditions are not recorded. |
| Evidence locator / span | Primary arXiv preprint and released trace dataset reference in data/review-packets/isca-2026-program-005.json: temporal/spatial data-movement profiling; distilled placement insights; wafer-scale modifications; prefill-aware placement; four 200B–1000B models; >24,000 requests; 6.6x wafer-scale average and up-to-1.25x existing-GPU speedups; exact full-paper locations not recorded. |
| Limits | Routing structure can support placement decisions only when it persists long enough to act on and remains valid for the current model, request mix, batch, topology and load.; A forecast needs an error metric, horizon, refresh and fallback rule; stale or wrong predictions can create link/expert hotspots and worsen tail latency.; Prefill and decode have different token rates and movement patterns, so a placement optimized for one phase does not automatically optimize the other.; The author preprint and trace dataset have not been independently checked for the six insights, wafer-scale model or transfer to other routing distributions/interconnects; speedups remain topology and trace bounded. |

<details markdown="1">
<summary>Historical captured record — superseded in the current table</summary>

Historical atlas evidence tier: `primary_preprint`.

| Field | Historical record |
|---|---|
| problem | Random expert selection in large Mixture-of-Experts inference creates data-movement overhead that can dominate serving systems. |
| mechanism | Data-movement-centric temporal/spatial profiling, distilled placement insights, lightweight wafer-scale architectural modifications, and a prefill-aware expert-placement algorithm. |
| workload | Four 200B–1000B MoE models released in 2025, more than 24,000 requests across diverse workloads, wafer-scale GPU architectures, and existing GPU systems. |
| hardware | Wafer-scale GPU and multi-GPU serving systems; reported architectural gains depend on the evaluated expert-selection traces and target topology. |
| baselines | existing GPU MoE serving systems; existing expert-placement approaches |
| metrics | 6.6x average speedup on wafer-scale GPUs; up to 1.25x speedup on existing GPU MoE computation; more than 24,000 profiled requests; 200B–1000B model scale |
| limits | The evidence is an author preprint and released trace dataset; the repository has not independently checked the six insights, reproduced the wafer-scale model, or tested whether the placement conclusions transfer to other MoE routing distributions and interconnects. |
| locator | The study profiles data movement across four 200B–1000B MoE models using more than 24,000 requests, analyzes temporal and spatial expert-selection behavior, distills six design insights, and applies them to wafer-scale GPU modifications and a prefill-aware expert-placement algorithm. It reports 6.6x average speedup on wafer-scale GPUs and up to 1.25x speedup on existing GPU MoE computation, with profiling traces released publicly. |

[Historical source](https://arxiv.org/abs/2510.05497)

</details>


Mapping review status: `not_recorded`; independent review status: `pending`.

## DisDP: Disaggregating Compute, Network, and Storage for Model-Sharded Data-Parallel Training

- Paper ID: `isca-2026-program-155`
- Conference/edition: `isca` / `2026`
- Evidence tier: `primary_preprint`
- Ledger record: `isca/data/adjudicated-2026-batch.jsonl`
- Source: [https://arxiv.org/abs/2409.00918](https://arxiv.org/abs/2409.00918)

| Field | Current record |
|---|---|
| Problem | Model-sharded data-parallel training reduces GPU memory requirements but adds AllGather and ReduceScatter overhead and interference among compute, communication, and optimizer-state storage. |
| Mechanism / artifact | Fully disaggregated compute/network/storage architecture, SmartNIC and SmartSwitch collective offload, and a SmartSwitch-enhanced parameter server for optimizer-state storage. |
| Workload / benchmark | Model-sharded LLM training, including a reported 175B model on eight distributed GPUs; the abstract references Llama and DeepSeek-style pretraining workloads. |
| Hardware / process | Multi-GPU distributed training with programmable SmartNIC/SmartSwitch infrastructure and parameter-server storage; topology and failure assumptions require full-paper verification. |
| Baselines | state-of-the-art distributed training systems; model-sharded data parallelism with conventional GPU-managed collectives |
| Metrics | 3.98x improvement on eight GPUs for a 175B model; collective execution time increase of 41% under aggregated compute/network/storage interference; fewer than 10% of GPU SMs occupied by collectives in the motivating analysis |
| Evidence locator / span | DisDP identifies serial interference among GEMM, network collectives, and optimizer-state storage in model-sharded data parallelism. It fully disaggregates compute, network, and storage, offloads collectives to SmartNICs and SmartSwitches, and uses a SmartSwitch-enhanced parameter server. The abstract reports 3.98x improvement over state-of-the-art training systems on eight GPUs training a 175B model. |
| Limits | The evidence is an author preprint abstract; exact baseline systems, network topology, storage cost, parameter-server scaling, failure behavior, and reproduction beyond eight GPUs remain to be verified. |

Mapping review status: `not_recorded`; independent review status: `pending`.

## COSM: A Cooperative Scheduling Framework for Concurrent PIM and CPU Execution on Mobile Devices

- Paper ID: `isca-2026-program-003`
- Conference/edition: `isca` / `2026`
- Evidence tier: `primary_preprint`
- Ledger record: `isca/data/adjudicated-2026-batch-2.jsonl`
- Source: [https://arxiv.org/abs/2606.30553](https://arxiv.org/abs/2606.30553)

| Field | Current record |
|---|---|
| Problem | Mobile on-device LLM and application workloads can benefit from processing in memory, but CPU/PIM concurrency in shared memory is vulnerable to bank conflicts, bus congestion, and interference with CPU accesses. |
| Mechanism / artifact | A low-interference PIM control interface and idleness-aware cooperative scheduler that places PIM commands into idle windows in the CPU access sequence, hiding PIM latency while overlapping PIM work with data transfer. |
| Workload / benchmark | Concurrent LLM workloads, mobile applications, and compute kernels evaluated with CPU and PIM execution on a shared-memory mobile-device setting. |
| Hardware / process | Mobile CPU/PIM systems sharing DRAM banks and buses; exact memory technology, PIM substrate, platform configuration, and energy model require full-paper verification. |
| Baselines | baseline CPU/PIM scheduling approaches; CPU-only execution for the evaluated concurrent workloads |
| Metrics | up to 2.8x PIM throughput; less than 2.0% CPU performance loss; concurrent LLM, mobile-app, and compute-kernel evaluation |
| Evidence locator / span | COSM addresses concurrent processing-in-memory and CPU execution on mobile devices, where bank conflicts and shared-bus congestion can erase PIM benefits. It introduces a low-interference PIM control interface, an idleness-aware scheduler that inserts PIM commands into CPU idle windows, and overlap of PIM execution with data transfer. The abstract reports up to 2.8x PIM throughput and less than 2.0% CPU performance loss across concurrent LLM, mobile-app, and compute-kernel workloads. |
| Limits | The evidence is an author preprint abstract; exact platform details, PIM command costs, scheduler overhead, energy impact, workload mix, and comparisons against all relevant PIM schedulers require full-paper verification. |

Mapping review status: `not_recorded`; independent review status: `pending`.

## Combating the Memory Walls: Optimization Pathways for Long-Context Agentic LLM Inference

- Paper ID: `isca-2026-program-007`
- Conference/edition: `isca` / `2026`
- Evidence tier: `Primary author preprint abstract only; no full-paper extraction, simulator/prototype reproduction or independent memory, quality, latency, energy and hardware validation`
- Ledger record: `isca/data/adjudicated-2026-batch-6.jsonl`

**Current evidence correction — 2026-09-08**

Reconciles the PLENA card with the captured primary preprint abstract; explains capacity versus bandwidth walls, asymmetric quantization, flattened attention execution, custom ISA/compiler responsibilities and simulated-comparison boundaries from first principles.

Condition review of this correction and independent acceptance remain pending. The direction mapping is inherited, not revalidated by this update.

[Dated correction register](../../../data/editorial-paper-corrections-v1.json)

- Source: [https://arxiv.org/abs/2509.09505](https://arxiv.org/abs/2509.09505)

| Field | Current record |
|---|---|
| Problem | Long-context agentic LLM inference retains web, tool and interaction state that creates both memory-capacity and memory-bandwidth limits, leaving compute underutilized. |
| Mechanism / artifact | PLENA hardware/software co-design with asymmetric-quantization compute/memory units, flattened FlashAttention-capable systolic array, custom ISA, compiler, cycle-emulated simulator and automated design-space exploration. |
| Workload / benchmark | Long-context agentic LLM inference with web/computer-use inputs, tool-call trajectories and extended contexts; models, context lengths, traces, batches, quality rules and prefill/decode conditions are unspecified. |
| Hardware / process | Custom simulated accelerator with flattened systolic array, asymmetric quantization, custom ISA/compiler and modeled memory hierarchy; area, energy, bandwidth, buffer, link contention, clock and fabricated status are unspecified. |
| Baselines | Existing accelerators; NVIDIA A100; Google TPU v6e; Multiplier/memory matching, model, precision, memory, software, simulator, quality and measurement-boundary parity are unspecified |
| Metrics | The primary preprint abstract reports up to 8.5x higher utilization than existing accelerators, 2.24x throughput over A100 and 3.85x throughput over TPU v6e under matched settings; simulated boundary, aggregation and full resource accounting are unspecified. |
| Evidence locator / span | Primary arXiv preprint abstract and data/review-packets/isca-2026-program-007.json: long-context agentic memory walls; asymmetric quantization; flattened FlashAttention systolic array; custom ISA/compiler; cycle-emulated simulation; 8.5x utilization, 2.24x A100 and 3.85x TPU v6e claims; exact full-paper locations not recorded. |
| Limits | Capacity and bandwidth are different limits: fitting state in memory does not guarantee it arrives fast enough, and higher bandwidth does not eliminate capacity pressure.; Asymmetric quantization can reduce movement while changing numerical error; the exact format assignment, accumulation and quality conditions are not specified.; A cycle-emulated simulator and custom compiler can estimate a co-designed path but do not establish silicon behavior, simulator fidelity, compiler overhead or complete area/energy cost.; The captured primary evidence supplies no exact page/table location, model/context protocol, memory hierarchy validation, energy/area, fabricated status or independent reproduction; general agentic deployment benefit remains unestablished. |

<details markdown="1">
<summary>Historical captured record — superseded in the current table</summary>

Historical atlas evidence tier: `primary_preprint`.

| Field | Historical record |
|---|---|
| problem | Long-context agentic LLM inference generates large off-chip memory traffic from extended web, tool, and interaction histories, creating simultaneous bandwidth and capacity memory walls that leave compute units underutilized. |
| mechanism | PLENA hardware-software co-design with asymmetric-quantization compute/memory units, a flattened FlashAttention-capable systolic array, custom ISA, compiler, cycle-emulated simulator, and automated design-space exploration flow. |
| workload | Long-context agentic LLM inference involving web or computer-use inputs, tool-call trajectories, and extended contexts; evaluation uses simulated accelerator execution and matched multiplier/memory settings against A100 and TPU v6e references. |
| hardware | Custom accelerator with flattened systolic array, asymmetric quantization, custom ISA/compiler, and cycle-emulated simulation; reported gains are simulated and depend on matched hardware-resource assumptions. |
| baselines | existing accelerators; NVIDIA A100 GPU; Google TPU v6e |
| metrics | up to 8.5x higher utilization than existing accelerators; 2.24x throughput over A100 under matched settings; 3.85x throughput over TPU v6e under matched settings; custom ISA, compiler, simulator, and DSE stack |
| limits | The evidence is an author preprint abstract and simulated evaluation; exact models, context lengths, memory hierarchy, area/energy, simulator validation, and the status of open-source artifacts require full-paper verification. |
| locator | PLENA targets long-context agentic LLM inference, where large DOMs and tool-call trajectories create bandwidth and capacity memory walls. It combines hardware supporting asymmetric quantization, a flattened systolic array with native FlashAttention support, and a full stack with custom ISA, compiler, cycle-emulated simulator, and automated design-space exploration. Simulated results report up to 8.5x higher utilization than existing accelerators, 2.24x higher throughput than an A100, and 3.85x higher throughput than a TPU v6e under matched multiplier and memory settings; the system is intended for open-source release. |

[Historical source](https://arxiv.org/abs/2509.09505)

</details>


Mapping review status: `not_recorded`; independent review status: `pending`.

## Approaching Shannon Bound with Lossless LLM Weight Compression

- Paper ID: `isca-2026-program-008`
- Conference/edition: `isca` / `2026`
- Evidence tier: `Author preprint v1; selected method/results inspected; source discrepancy retained`
- Ledger record: `isca/data/adjudicated-2026-batch-6.jsonl`

**Current evidence correction — 2026-09-07**

Full-section inspection exposes abstract/table discrepancy and separates kernel from serving results.

Condition review of this correction and independent acceptance remain pending. The direction mapping is inherited, not revalidated by this update.

[Dated correction register](../../../data/editorial-paper-corrections-v1.json)

- Source: [https://arxiv.org/pdf/2606.15789v1](https://arxiv.org/pdf/2606.15789v1)

| Field | Current record |
|---|---|
| Problem | Weight capacity and inference-time reconstruction. |
| Mechanism / artifact | Tile-addressable ANS with fused decompression/multiplication. |
| Workload / benchmark | Qwen/Mixtral serving; separate projection microbenchmarks. |
| Hardware / process | A100 serving; H200 comparison kernels. |
| Baselines | Uncompressed serving; NeuZip/DFloat11 kernel comparisons. |
| Metrics | Qwen Table II batch 47 to 60 conflicts with 75 in prose. Throughput increases alongside longer median time per output token. |
| Evidence locator / span | PDF p. 2 entropy; pp. 5–7 method; pp. 9–10 Table II and Sections VI-C/D; p. 12 metadata. |
| Limits | Batch discrepancy unresolved; microbenchmark gains are not serving gains. Codec and operator equality not reproduced. |

<details markdown="1">
<summary>Historical captured record — superseded in the current table</summary>

Historical atlas evidence tier: `primary_preprint`.

| Field | Historical record |
|---|---|
| problem | Trillion-parameter LLM weights can exceed GPU memory capacity, while conventional stored bitwidth overstates the intrinsic randomness of weights and lossless compression has not been tightly integrated with inference execution. |
| mechanism | Entropy analysis across model sizes and numeric formats, followed by tile-level Asymmetric Numeral Systems compression and on-the-fly decompression aligned to GPU GEMM tiling, integrated with SGLang and multi-GPU serving. |
| workload | LLM serving across 1.5B–405B parameter models and bf16/int4/AWQ/SQ8 formats, including Qwen-14B and Mixtral-176B batch-size and throughput evaluation; comparisons include NeuZip and DFloat11. |
| hardware | GPU inference with tile-level decompression integrated into SGLang and multi-GPU serving; exact decompression hardware/software cost, memory bandwidth, GPU models, and quality invariance conditions require full-paper verification. |
| baselines | uncompressed stored weights; NeuZip; DFloat11; standard SGLang serving configuration |
| metrics | effective entropy 2–10x below stored bitwidth; within 0.01–0.1 bits of Shannon limit; Qwen-14B maximum batch size 47 to 75; Mixtral-176B maximum batch size 20 to 95; up to 1.2x Qwen throughput improvement; up to 1.6x Mixtral throughput improvement; up to 11x throughput improvement over NeuZip and DFloat11 |
| limits | The evidence is an author preprint abstract; exact compression/decompression latency, CPU/GPU overhead, memory-bandwidth accounting, model-quality invariance, sequence lengths, and hardware implementation details require full-paper verification. |
| locator | The study analyzes LLM weight entropy from 1.5B to 405B parameter models across bf16, int4, AWQ, and SQ8 formats, finding effective entropy 2–10x lower than stored bitwidth and theoretical footprint reduction up to 10x without changing weight values. It introduces tile-level on-the-fly lossless decompression using Asymmetric Numeral Systems aligned with GPU GEMM tiling. The system reaches within 0.01–0.1 bits of the Shannon limit, raises Qwen-14B maximum batch size from 47 to 75, improves Mixtral-176B batch size from 20 to 95, and reports up to 1.2x/1.6x throughput gains plus up to 11x over NeuZip and DFloat11. |

[Historical source](https://arxiv.org/abs/2606.15789)

</details>


Mapping review status: `not_recorded`; independent review status: `pending`.

## A Silicon-Proven Unified Low-Latency CXL Controller and Port-Based Routing Switch for Memory-Centric Fabrics

- Paper ID: `isca-2026-program-044`
- Conference/edition: `isca` / `2026`
- Evidence tier: `Official company author source; paper manuscript and independent reproduction not performed`
- Ledger record: `isca/data/adjudicated-2026-batch-7.jsonl`

**Current evidence correction — 2026-09-08**

Deepens the exact-title company-source reading; separates cross-layer controller buffering, routing flexibility, silicon wording and missing paper-level measurements.

Condition review of this correction and independent acceptance remain pending. The direction mapping is inherited, not revalidated by this update.

[Dated correction register](../../../data/editorial-paper-corrections-v1.json)

- Source: [https://panmnesia.com/news/en/2026-06-24-panmnesia-isca2026-eng/](https://panmnesia.com/news/en/2026-06-24-panmnesia-isca2026-eng/)

| Field | Current record |
|---|---|
| Problem | Layer-separated CXL control and fixed hierarchical connectivity can add synchronization overhead and constrain memory-centric fabric scaling. |
| Mechanism / artifact | A unified CXL controller with shared buffers across physical, link and transaction layers, plus a fabric switch supporting port-based routing alongside hierarchy-based routing. |
| Workload / benchmark | Memory-centric CXL fabric scaling and multi-node connectivity; the company source reports stable performance up to 64 nodes but does not expose the paper's workload matrix. |
| Hardware / process | Author/company source describes silicon-proven and pre-release product context with PCIe/CXL physical interfaces; process, link generation, controller frequency, buffer sizes and test configuration are not reported. |
| Baselines | PCIe-derived early CXL controller organization; Directly attached multi-headed device topology; Hierarchy-based routing |
| Metrics | Stable performance with as many as 64 nodes, similar latency range while expanding memory connectivity, and improved total system bandwidth are reported qualitatively by the company source. |
| Evidence locator / span | Technical Highlights sections 1–2 and availability section; exact title and paper identity; no permitted manuscript pages recovered. |
| Limits | No paper pages, numeric latency distributions, bandwidth denominators, power, area, process, traffic matrix, flow-control details or independent reproduction are available.; Silicon-proven wording does not establish measured operation of every 64-node configuration or a universal latency bound.; Port-based and hierarchical routing compatibility does not by itself prove scalability, fairness or progress under contention. |

<details markdown="1">
<summary>Historical captured record — superseded in the current table</summary>

Historical atlas evidence tier: `company_author_source`.

| Field | Historical record |
|---|---|
| problem | Early CXL designs inherited PCIe-oriented layer separation and hierarchical connectivity, creating synchronization overhead and limiting the scale of memory-centric fabrics. |
| mechanism | A unified CXL controller with shared cross-layer buffers and a port-based-routing fabric switch that supports flexible topologies while retaining hierarchy-based routing compatibility. |
| workload | Memory-centric CXL fabric scaling and multi-node connectivity; the company announcement reports stable performance with up to 64 nodes but does not expose the full paper’s workload matrix. |
| hardware | Silicon-proven CXL controller and switch, with PCIe/CXL physical interfaces, shared layer buffers, and port-based routing; exact process node, latency, bandwidth, power, and test configuration require the paper. |
| baselines | PCIe-derived early CXL controller organization; directly attached multi-headed device topology; hierarchy-based routing |
| metrics | stable performance with as many as 64 nodes; similar latency range while expanding memory connectivity; improved total system bandwidth; silicon-proven implementation and pre-release product context |
| limits | The source is an official company announcement, not the captured IEEE paper. It is subject to author/company framing and omits detailed latency distributions, bandwidth numbers, power, area, process, workloads, and independent reproduction. |
| locator | Panmnesia's official ISCA announcement describes a CXL controller that shares buffers across physical, link, and transaction layers to reduce layer-level synchronization overhead, plus a fabric switch supporting port-based routing alongside hierarchy-based routing. The announcement says the design expands memory connectivity while keeping latency in a similar range, improves total bandwidth, and shows stable performance with as many as 64 nodes. It also identifies pre-release PCIe 6.4-CXL 3.2 switch silicon and PCIe 7.0-CXL 4.0 controller IP as productization context. |

[Historical source](https://panmnesia.com/news/en/2026-06-24-panmnesia-isca2026-eng/)

</details>


Mapping review status: `not_recorded`; independent review status: `pending`.

## Vistara: Making CXL Real—Full Path from ASIC Design and OS Support to Hyperscale Deployment

- Paper ID: `isca-2026-program-045`
- Conference/edition: `isca` / `2026`
- Evidence tier: `Author-hosted manuscript; selected platform, method, and evaluation sections inspected`
- Ledger record: `isca/data/adjudicated-2026-batch-7.jsonl`

**Current evidence correction — 2026-09-07**

Recovered author-hosted manuscript beyond the social post; adverse conditions and source inconsistencies retained.

Condition review of this correction and independent acceptance remain pending. The direction mapping is inherited, not revalidated by this update.

[Dated correction register](../../../data/editorial-paper-corrections-v1.json)

- Source: [https://aisystemcodesign.github.io/papers/isca26/vistara_camera_ready.pdf](https://aisystemcodesign.github.io/papers/isca26/vistara_camera_ready.pdf)

| Field | Current record |
|---|---|
| Problem | Capacity-limited production services. |
| Mechanism / artifact | CXL expander with OS tiering and workload-specific configuration. |
| Workload / benchmark | Production A/B and separate equal-capacity sensitivity tests. |
| Hardware / process | Turin; 768 GB local DDR5 plus 256 GB expanded DDR4. |
| Baselines | CXL disabled; separate equal-capacity all-local comparison. |
| Metrics | Benefits vary by workload; DPP throughput falls 19% at a 1:1 tier ratio. |
| Evidence locator / span | PDF p. 5 Table VI; pp. 6–8 OS; p. 8 methodology; pp. 11–13 sensitivity, fairness, and threshold. |
| Limits | Table X baseline and threshold prose conflict. Production report is not an independent fleet audit; CXL-equipped server count not established here. |

<details markdown="1">
<summary>Historical captured record — superseded in the current table</summary>

Historical atlas evidence tier: `company_author_source`.

| Field | Historical record |
|---|---|
| problem | CXL’s usefulness at hyperscale depends on more than an interconnect: ASIC behavior, firmware, OS tiering, tail latency, workload diversity, and deployment operations must work together across production systems. |
| mechanism | An end-to-end CXL deployment path combining custom ASIC design, firmware, OS memory-management mechanisms, production workload integration, and operational rollout. |
| workload | Disaggregated ML inference, big-data processing, databases, distributed caches, and software build/test pipelines in Meta deployment context. |
| hardware | Hyperscale datacenter CXL deployment with custom silicon and OS memory tiering; exact server fleet, CXL generation, workload methodology, tail-latency distributions, and comparison design require the full paper. |
| baselines | conventional server fleet for disaggregated inference; non-CXL memory-capacity provisioning; production tiering alternatives (not fully specified in the post) |
| metrics | up to 25% fewer servers for disaggregated inference; tiering overhead below 0.5% in the described design; deployment across five workload classes; reuse of decommissioned DIMMs as CXL memory |
| limits | The evidence is a lead-author/company social post, not a full paper or independently audited deployment report. Claims require paper-level verification of fleet scale, baselines, workload methodology, tail latency, overhead definitions, cost, and carbon accounting. |
| locator | The lead author’s ISCA presentation post describes Vistara as Meta’s end-to-end CXL solution spanning ASIC design, firmware, OS-level memory tiering, and hyperscale rollout. It reports deployment across disaggregated ML inference, big-data processing, databases, distributed caches, and software build/test pipelines; the post claims up to 25% fewer servers for disaggregated inference, reuse of decommissioned DIMMs as CXL memory, and tiering overhead below 0.5% in the described production-minded design. |

[Historical source](https://www.linkedin.com/posts/neha-gholkar-4897b445_isca2026-activity-7477033922183458816-o8FC)

</details>


Mapping review status: `not_recorded`; independent review status: `pending`.

## MTIA 300: Meta’s First Training Chip Featuring Built-in NICs and Collective Offloading Engines

- Paper ID: `isca-2026-program-069`
- Conference/edition: `isca` / `2026`
- Evidence tier: `Primary author PDF with selected sections/tables inspected; no independent replication, full cost-accounting reconstruction or deployment validation`
- Ledger record: `isca/data/adjudicated-2026-batch-8.jsonl`

**Current evidence correction — 2026-09-08**

Reconciles the MTIA 300 card with the recovered primary paper; explains embedding/collective communication, integrated NICs, message engines, near-memory reduction, autonomous dependency graphs, communication versus Perf/TCO and power/cost boundaries from first principles.

Condition review of this correction and independent acceptance remain pending. The direction mapping is inherited, not revalidated by this update.

[Dated correction register](../../../data/editorial-paper-corrections-v1.json)

- Source: [https://aisystemcodesign.github.io/papers/MTIA300_ISCA2026.pdf](https://aisystemcodesign.github.io/papers/MTIA300_ISCA2026.pdf)

| Field | Current record |
|---|---|
| Problem | Recommendation-model training is communication-bound because large embedding tables and hybrid parallelism generate AllReduce, AllToAll and AllGather traffic that competes with computation and synchronization. |
| Mechanism / artifact | MTIA 300 compute and network-chiplet co-design with 12×800-Gbps RDMA NICs, 16 message engines, near-memory collective reduction and HCCL; collectives compile into autonomous dependency graphs rather than compute-grid kernels. |
| Workload / benchmark | Approximately 150B-parameter DLRM using TorchRec/TorchInductor and distributed Shampoo; 40 MTIA 300 versus 40 H100 at local batch 6144 for communication, plus 1,000 TF32 4K×4K×4K GEMMs with collectives across 16 accelerators for overlap; other convergence and workload conditions are bounded by paper sections V.B–D. |
| Hardware / process | MTIA 300 at 1.9 GHz, 216 GB HBM3E, 912 W TDP/667 W typical, compute and network chiplets, 12×800-Gbps RDMA NICs and 16 message engines; process node, measured workload energy and complete cost/amortization boundary are unspecified. |
| Baselines | 40 H100 with NCCL and TorchRec/TorchInductor; Table IV normalized Perf/TCO H100 reference 1.00; Communication, batch, software, numerical parity, system-cost, utilization and convergence parity are condition-specific |
| Metrics | Primary paper Section V.D reports 3.9x communication performance versus H100 for 40 accelerators/local batch 6144; Table IV reports normalized Perf/TCO 1.39 for 40 MTIA 300/local batch 6144 versus 1.00 H100 and 1.42 for 24 MTIA 300/local batch 10240 with global batch held constant. |
| Evidence locator / span | Primary MTIA 300 ISCA 2026 paper: Sections I–II for communication problem/hardware; Table I and PDF page 4 for clock/HBM/TDP/chiplets; Sections V.B–D PDF pages 10–11 and Table IV for DLRM, 40 MTIA/40 H100, 3.9x communication, normalized Perf/TCO 1.39/1.42 and batch conditions; Section VI PDF pages 12–13 for limitations. |
| Limits | Communication speedup, overlap microbenchmark performance, complete training-step throughput and normalized Perf/TCO have different denominators and must not be conflated.; Integrated NICs, message engines and near-memory reduction can reduce launch, movement or synchronization overhead but do not remove link capacity, dependency, small-message, datatype or imbalance limits.; TDP, typical platform power and chiplet dimensions are not measured energy per training step, total system area or complete TCO; amortization, cooling, networking and utilization inputs remain necessary.; The author-reported paper has not been independently replicated; other model sizes, collectives, batch/convergence tradeoffs, numerical parity and unsupported datatypes limit generalization. |

<details markdown="1">
<summary>Historical captured record — superseded in the current table</summary>

Historical atlas evidence tier: `primary_author_paper`.

| Field | Historical record |
|---|---|
| problem | Recommendation-model training is communication-bound because embedding tables contain most model parameters and hybrid parallelism generates frequent AllReduce, AllToAll, and AllGather operations that compete with computation on GPU resources. |
| mechanism | MTIA 300 co-designs compute, integrated network chiplets, dedicated message engines, near-memory collective reduction, and the HCCL communication library; collectives are compiled into autonomous dependency graphs rather than launched as compute-grid kernels. |
| workload | DLRM of approximately 150B parameters implemented with TorchRec/TorchInductor and distributed Shampoo. Communication comparison: 40 MTIA 300 versus 40 H100, local batch 6144. Overlap microbenchmark: 1000 TF32 4K x 4K x 4K GEMMs with collectives across 16 accelerators. |
| hardware | Table I: 1.9 GHz, 216 GB HBM3E, 912 W TDP (667 W typical), compute chiplet 25.6 x 31.4 mm, two network chiplets each 25.6 x 9.3 mm. Section II: 12 x 800 Gbps RDMA NICs and 16 message engines. Process node not established in extracted sections; TDP is not measured workload energy. |
| baselines | H100 with NCCL for collective operations; TorchRec/TorchInductor on both platforms for the production DLRM; Table IV reference: 40 H100 accelerators at local batch 6144, normalized Perf/TCO 1.00 |
| metrics | 3.9x communication performance relative to H100: 40 accelerators, local batch 6144, approximately 150B-parameter DLRM (V.D.1); Normalized Perf/TCO 1.39 for 40 MTIA 300 at local batch 6144 versus 1.00 for 40 H100 at the same batch (Table IV); Normalized Perf/TCO 1.42 for 24 MTIA 300 at local batch 10240 versus the Table IV H100 reference; global batch held constant |
| limits | Author-reported evaluation, not independent replication. Communication speedup and Perf/TCO are distinct; neither establishes universal end-to-end speedup. Cost-accounting inputs and amortization assumptions were not found in the extracted evaluation and remain unresolved. Small-message collectives favor H100/NCCL; compute-heavy workloads, numerical parity, unsupported datatypes, eager overhead, and convergence/batch tradeoffs limit generality. Exact article-only 940 GB/s and less-than-0.5% figures remain supplemental, not paper-verified metrics. |
| locator | Sections II and IV describe integrated RDMA NIC chiplets, dedicated message engines, near-memory reductions, and HCCL software. Section V.D.1 reports 3.9x communication performance versus H100 for a roughly 150B-parameter DLRM using 40 accelerators and local batch 6144. Table IV reports normalized Perf/TCO separately. Section V.B reports an H100/NCCL advantage for small messages; Section VI discusses numerical, datatype, runtime, and training-batch limitations. |

[Historical source](https://aisystemcodesign.github.io/papers/MTIA300_ISCA2026.pdf)

</details>


Mapping review status: `not_recorded`; independent review status: `pending`.

## Tasa: Thermal-aware 3D-Stacked Architecture Design with Bandwidth Sharing for LLM Inference

- Paper ID: `iccad-2025-1103`
- Conference/edition: `iccad` / `2025`
- Evidence tier: `Primary arXiv preprint v3 and official ICCAD record; selected manuscript reading, simulator execution and independent acceptance not performed`
- Ledger record: `iccad/data/adjudicated-2025-batch.jsonl`

**Current evidence correction — 2026-09-08**

Reconciles the abstract card with arXiv version 3; separates simulated thermal analysis, heterogeneous core/floorplan choices, KV-cache bandwidth sharing, and end-to-end modeled speedups, preserving the simulator and threshold conditions.

Condition review of this correction and independent acceptance remain pending. The direction mapping is inherited, not revalidated by this update.

[Dated correction register](../../../data/editorial-paper-corrections-v1.json)

- Source: [https://arxiv.org/pdf/2508.07252v3](https://arxiv.org/pdf/2508.07252v3)

| Field | Current record |
|---|---|
| Problem | 3D-stacked DRAM over a logic die can increase memory bandwidth for autoregressive LLM decoding while increasing power density, thermal gradients, hotspot risk and scalability limits. |
| Mechanism / artifact | Tasa combines thermal-aware heterogeneous P-cores for GEMM/fully connected work and E-cores for memory-intensive GEMV/attention work with a hierarchical NoC, E-core placement exploration, adaptive KV-cache partitioning and bandwidth-sharing scheduling based on P-core utilization and batch size. |
| Workload / benchmark | LLaMA-65B and GPT-3 66B in FP16/BF16; ShareGPT conversational requests, dynamic stable batches and Poisson request arrivals for QPS tests; 48/60/72-core stacks, 3:1 and 5:1 P:E ratios, input/output length 512/512 and batch size 32 for thermal comparisons. |
| Hardware / process | Four DRAM dies over one logic die; 48 GB/stack, 768 banks/die, 16 banks/core, 128 KB SRAM/core, 1 GHz, 6 TB/s stack data rate, 32×32 systolic arrays in P-cores and 32×1 MAC-tree arrays in E-cores. Thermal threshold 85 °C with DVFS; modeled TIM/TSV, silicon, heat-sink and DRAM parameters; Timeloop, Accelergy/FinCACTI, Ramulator 2.0, HotSpot 6.0 and AttAcc-derived simulation, including ASAP7 logic estimates. |
| Baselines | Eight NVIDIA A100 40 GB GPUs; Eight A100 GPUs plus AttAcc PIM; Eight homogeneous 3D-stacked accelerators with the same overall Tasa configuration (Homo-3D) |
| Metrics | Thermal reduction versus Homo-3D at batch 32 and 512/512 input/output: average peak-temperature reduction 3.96 °C, 6.10 °C and 5.99 °C for 48, 60 and 72 cores; frequency-comparison ranges 3.63–5.55 °C, 5.73–9.37 °C and 5.12–7.91 °C.; Average throughput speedup in the 48-core evaluation: 2.85× over A100-only, 2.12× over A100+AttAcc and 1.33× over Homo-3D; up to 3.35× in a stated comparison. Average energy-efficiency improvement: 2.07× over A100-only and 1.61× over A100+AttAcc.; Thermal analysis baseline: 3D peak rises 23.3 °C from 24 to 72 cores versus 15.3 °C for 2D; increasing core spacing lowers peak by 10.32 °C at 2.25× area in the stated simulation. |
| Evidence locator / span | Version 3: Sections III–V pages 3–7 for thermal analysis, P/E cores and bandwidth sharing; Tables I–II pages 7–8 for hardware and thermal parameters; Sections VI-A–C pages 8–10 and Figures 11–14 for ShareGPT/Poisson evaluation, thermal reductions, throughput, energy efficiency and QPS latency; official ICCAD DOI 10.1109/ICCAD66269.2025.11240805. |
| Limits | All temperature, area, energy and throughput results are modeled with the stated HotSpot/Timeloop/Accelergy/Ramulator/AttAcc flow and thermal parameters; they are not fabricated-silicon or package measurements.; The 85 °C threshold and DVFS response, memory-stack cooling, thermal calibration, controller/migration overhead, process/library assumptions and manufacturing cost require independent verification. The simulated 361.79 °C logic-die peak should not be presented as a physical operating temperature.; The 2.85×/2.12×/1.33× comparisons combine heterogeneous cores, 3D bandwidth, thermal response, cache placement and bandwidth sharing; they do not isolate one mechanism or establish transfer to other models, traffic, stacks, cooling systems or baselines.; No simulator execution or independent reproduction was performed here; package feasibility and silicon validation remain open. |

<details markdown="1">
<summary>Historical captured record — superseded in the current table</summary>

Historical atlas evidence tier: `primary_preprint`.

| Field | Historical record |
|---|---|
| problem | 3D stacking increases memory bandwidth for autoregressive LLM decoding but creates more severe temperature, thermal-gradient, and scalability constraints than 2D designs. |
| mechanism | Heterogeneous 3D-stacked architecture with high-performance cores for compute-intensive operators, high-efficiency cores for memory-intensive attention operators, cross-stack thermal balancing, and bandwidth-sharing scheduling. |
| workload | Llama-65B and GPT-3 66B inference with 48-, 60-, and 72-core configurations; comparisons include GPU and heterogeneous PIM-based accelerators. |
| hardware | 3D-stacked multi-DRAM-die-over-logic architecture with thermal constraints and heterogeneous cores; technology, cooling, and memory-stack assumptions require full-paper verification. |
| baselines | homogeneous 3D-stacked architecture; GPU baselines; state-of-the-art heterogeneous PIM-based LLM accelerator |
| metrics | 5.55, 9.37, and 7.91 degree Celsius peak-temperature reductions; 2.85x Llama-65B inference speedup; 2.21x GPT-3 66B inference speedup; thermal scalability and bandwidth utilization |
| limits | The evidence is an author preprint abstract; full-paper verification is needed for thermal-model calibration, area/cost overhead, memory bandwidth assumptions, and comparison fairness. |
| locator | Tasa addresses the thermal limits of 3D-stacked architectures by combining heterogeneous high-performance and high-efficiency cores with cross-stack thermal optimization and bandwidth-sharing scheduling. The abstract reports peak-temperature reductions of 5.55, 9.37, and 7.91 degrees Celsius for 48, 60, and 72 core configurations, plus 2.85x and 2.21x speedups for Llama-65B and GPT-3 66B inference over GPU baselines and a heterogeneous PIM accelerator. |

[Historical source](https://arxiv.org/abs/2508.07252)

</details>


Mapping review status: `not_recorded`; independent review status: `pending`.

## Fusedot: A Multiplication-Fused Dot Product Accelerator for Efficient LLM Inference

- Paper ID: `dac-2026-research1182`
- Conference/edition: `dac` / `2026`
- Evidence tier: `Primary captured official DAC description plus source-recovery assessment; no full-paper extraction, FuseDot artifact reproduction or independent accuracy, PPA, memory and energy validation`
- Ledger record: `dac/data/adjudicated-2026-batch-4.jsonl`

**Current evidence correction — 2026-09-08**

Reconciles the FuseDot card with the captured official DAC description and recovery assessment; explains multiplication-fused dot products, index/reordering overhead, multiplier sharing, quantization-scale semantics and the missing end-to-end LLM conditions.

Condition review of this correction and independent acceptance remain pending. The direction mapping is inherited, not revalidated by this update.

[Dated correction register](../../../data/editorial-paper-corrections-v1.json)

- Source: [https://63dac.conference-program.com/presentation/?id=RESEARCH1182&sess=sess156](https://63dac.conference-program.com/presentation/?id=RESEARCH1182&sess=sess156)

| Field | Current record |
|---|---|
| Problem | FP16 activations multiplied by INT4 weights make low-bit LLM dot products multiplication-heavy. Repeated or equal effective weights can create an opportunity to share multiplication work, but the accelerator must still preserve the quantized values and accumulate the correct result. |
| Mechanism / artifact | MFDP multiplication-fused dot-product architecture using index-driven generalized matrix multiplication, hierarchical dual-phase reordering and multiplier sharing across processing elements. |
| Workload / benchmark | Low-bit mixed-precision LLM inference; model suite, layer shapes, sequence lengths, batch sizes, activation/weight scales, accuracy target and exact accelerator configurations are unspecified. |
| Hardware / process | Specialized multi-processing-element accelerator with half-multiplier sharing; memory hierarchy, interconnect, frequency, area, precision datapath, compiler/mapping and power boundary are unspecified. |
| Baselines | State-of-the-art LLM inference accelerators; General-purpose processors are named as motivation, not a measured baseline; Model, software, precision, memory traffic, frequency and measurement boundaries are unspecified |
| Metrics | The captured official description reports 1.51–1.98× speedup and 1.19–1.51× energy-efficiency improvement over unnamed accelerator baselines; exact models, layers, absolute latency, power and variance are not exposed. |
| Evidence locator / span | DAC 2026 official description and data/review-packets/dac-2026-research1182.json; separately recorded recovery assessment dac/data/fusedot-primary-recovery-v1.json: FP16xINT4 LLM inference; MFDP; indexed matrix processing; hierarchical dual-phase reordering; cross-PE multiplier sharing; 1.51–1.98× speedup; 1.19–1.51× energy-efficiency claim; omitted model, accuracy, PPA, memory and baseline conditions. |
| Limits | In exact arithmetic, w×a + w×b can be reorganized as w×(a+b), replacing repeated multiplications with an addition and one multiplication. The transformation is valid only when the effective weights are equal under the quantization scales and the accumulation semantics. Equal INT4 codes from different groups can represent different real values, so code equality alone is insufficient.; Index-driven matrix processing and hierarchical reordering can expose repeated weights and place compatible work together. The search and metadata have a cost: indices must be stored, groups must be found, data may be moved or reordered, and irregular groups can leave processing elements idle. The saved multiplier work must exceed these costs.; Sharing a multiplier changes the balance among arithmetic throughput, accumulation bandwidth, local storage and synchronization. Reassociation can change rounding, saturation and overflow behavior in mixed FP16/INT4 computation. The evaluation must compare the final tensor outputs and LLM quality under identical quantization and error rules, not only count multipliers.; The official description and recovery assessment do not expose models, sequence lengths, accuracy impact, area, frequency, memory traffic, exact baseline hardware, compiler mapping or power accounting. The record supports a reported dot-product accelerator direction and bounded performance range, not a general LLM speedup or energy result. |

<details markdown="1">
<summary>Historical captured record — superseded in the current table</summary>

Historical atlas evidence tier: `official_description`.

| Field | Historical record |
|---|---|
| problem | Mixed-precision FP16xINT4 LLM inference remains multiplication-heavy on general-purpose processors and conventional dot-product accelerators. |
| mechanism | MFDP multiplication-fused dot-product paradigm with index-driven generalized matrix multiplication, hierarchical dual-phase reordering, and cross-processing-element multiplier sharing. |
| workload | Low-bit mixed-precision LLM inference; exact model suite, sequence lengths, and accelerator configurations are not stated in the description. |
| hardware | Specialized accelerator with multiple processing elements and half-multiplier sharing; quantization formats and memory/interconnect assumptions beyond FP16xINT4 are unspecified. |
| baselines | state-of-the-art LLM inference accelerators; general-purpose processors (motivation, not measured in the description) |
| metrics | 1.51–1.98x speedup; 1.19–1.51x energy-efficiency improvement |
| limits | The description omits models, sequence lengths, accuracy impact, area, frequency, memory traffic, and exact baseline hardware; reported ranges require paper-level conditions and variance. |
| locator | FuseDot exploits identical-weight multiplication opportunities in low-bit mixed-precision LLM inference through a multiplication-fused dot-product paradigm. It combines index-driven generalized matrix multiplication, hierarchical dual-phase reordering, and cross-PE multiplier sharing with a half-multiplier scheme, reporting 1.51–1.98x speedup and 1.19–1.51x energy-efficiency improvement over state-of-the-art accelerators. |

[Historical source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH1182&sess=sess156)

</details>


Mapping review status: `not_recorded`; independent review status: `pending`.

## OASIS: Outlier-Aware LUT-Based GEMM with Dual-Side Quantization for LLM Inference Acceleration

- Paper ID: `isca-2026-program-020`
- Conference/edition: `isca` / `2026`
- Evidence tier: `Primary author version-4 preprint and captured abstract; no fabricated OASIS silicon or independent full-paper reproduction`
- Ledger record: `isca/data/adjudicated-2026-batch.jsonl`

**Current evidence correction — 2026-09-08**

Reconciles the OASIS card with the recovered version-4 preprint and captured abstract; explains non-uniform quantization and Cartesian-product LUT GEMM from first principles and preserves the accuracy-version discrepancy, outlier-compensation boundary and simulation/synthesis versus silicon distinction.

Condition review of this correction and independent acceptance remain pending. The direction mapping is inherited, not revalidated by this update.

[Dated correction register](../../../data/editorial-paper-corrections-v1.json)

- Source: [https://arxiv.org/pdf/2507.23035v4](https://arxiv.org/pdf/2507.23035v4)

| Field | Current record |
|---|---|
| Problem | LLM inference needs lower memory and compute cost, but weight-only quantization adds dequantization overhead, integer weight/activation quantization can reduce quality, and non-uniform codes do not map directly to ordinary low-precision multipliers. |
| Mechanism / artifact | Dual-side non-uniform weight/activation quantization with Cartesian-product lookup-table GEMM without dequantization, outlier-aware activation handling, concurrent LUT-based error compensation and the Orizuru top-k outlier-detection engine. |
| Workload / benchmark | LLM inference including LLaMA-2-7B and the version-4 model suite; four-bit weights/activations, single-batch decoding for the FIGLUT comparison; full model list, sequence lengths, batch conditions and accuracy metric definitions are incomplete in the captured record. |
| Hardware / process | Dedicated LUT-based low-precision accelerator; version-4 hardware evaluation uses cycle simulation, 28-nm logic synthesis and memory models, with area, memory, frequency, power, process and fabricated status otherwise unspecified. |
| Baselines | FP16 baseline; Atom quantization/accelerator baseline; FIGLUT accelerator; Precision, model, batch, memory and quality parity are condition-specific and must remain attached to each result |
| Metrics | The recovered abstract reports 64x LUT-size reduction and 1024x higher computational parallelism over existing LUT-based GEMM methods, an average accuracy drop of 1.98% versus FP16, 3.00x speedup and 1.44x energy-efficiency improvement versus FIGLUT; version-4 PDF abstract reports 1.94% and Section V-B 2.05%, while LLaMA-2-7B Table IV implies 1.94 percentage points. Definitions and aggregation remain source-specific. |
| Evidence locator / span | OASIS version-4 preprint pages 1 and 9–11 plus arXiv record: NU-WAQ and LUT-GEMM problem; Cartesian-product LUT; 64x LUT-size and 1024x parallelism claims; Orizuru top-k and concurrent compensation; 1.94/1.98/2.05% accuracy discrepancy; LLaMA-2-7B Table IV; Figure 11 3.00x/1.44x versus FIGLUT under four-bit single-batch decoding. |
| Limits | Non-uniform codes identify representative values and cannot generally be multiplied as integer magnitudes; LUT lookup avoids dequantization but still requires code access, product selection, accumulation, memory bandwidth and outlier handling.; Outlier detection and compensation can reduce error for selected activation values without eliminating residual quantization error or proving quality on every model, token distribution or layer.; The 64x LUT and 1024x parallelism ratios are not automatically end-to-end speed or energy gains; table bandwidth, read ports, routing, accumulation and control costs must be included.; The accuracy headline differs across abstract/source versions and the hardware result is simulation/synthesis/modeling rather than measured silicon; full model suite, area/energy accounting, sequence conditions and independent reproduction remain open. |

<details markdown="1">
<summary>Historical captured record — superseded in the current table</summary>

Historical atlas evidence tier: `primary_preprint`.

| Field | Historical record |
|---|---|
| problem | LLM inference must reduce memory and compute cost, but weight-only quantization adds dequantization overhead and integer weight/activation quantization can degrade model quality; non-uniform quantization is difficult to map to conventional low-precision units. |
| mechanism | Outlier-aware dual-side non-uniform quantization, Cartesian-product LUT-based GEMM without dequantization, concurrent error compensation, and an Orizuru top-k outlier-detection engine. |
| workload | LLM inference with non-uniformly quantized weights and activations; comparisons against FP16 accuracy and the FIGLUT accelerator. |
| hardware | Dedicated low-precision accelerator implementing LUT-based GEMM and real-time outlier detection; area, memory, and technology assumptions require primary-paper table verification. |
| baselines | FP16 baseline; Atom quantization/accelerator baseline; FIGLUT accelerator |
| metrics | 64x LUT-size reduction; 1024x higher computational parallelism than existing LUT-based GEMM; 1.98% average accuracy drop versus FP16; 3.00x average speedup versus FIGLUT; 1.44x energy-efficiency improvement versus FIGLUT |
| limits | The evidence is an author preprint abstract; model suite, sequence lengths, area/energy accounting, accuracy metric, and hardware implementation details must be extracted from the full paper before generalizing the reported gains. |
| locator | OASIS uses Cartesian-product lookup tables to perform GEMM between non-uniformly quantized weights and activations without dequantization. It reports a 64x LUT-size reduction and 1024x higher parallelism over prior LUT-based GEMM, adds outlier-aware activation quantization with error compensation, and introduces the Orizuru top-k outlier-detection engine. The abstract reports 1.98% average accuracy drop versus FP16, 3.00x speedup, and 1.44x energy-efficiency improvement over FIGLUT. |

[Historical source](https://arxiv.org/abs/2507.23035)

</details>


Mapping review status: `not_recorded`; independent review status: `pending`.

## Cassandra: Enabling Reasoning LLMs at Edge via Self-Speculative Decoding

- Paper ID: `isca-2026-program-006`
- Conference/edition: `isca` / `2026`
- Evidence tier: `Primary author preprint abstract only; no full-paper extraction, Cassandra reproduction or independent acceptance, reasoning-quality, latency, format-converter and edge-hardware validation`
- Ledger record: `isca/data/adjudicated-2026-batch-3.jsonl`

**Current evidence correction — 2026-09-08**

Reconciles the Cassandra card with the captured primary preprint abstract; explains self-speculative decoding, accepted versus drafted tokens, pruning/truncation/KV selection, format conversion and reasoning-quality/deployment boundaries from first principles.

Condition review of this correction and independent acceptance remain pending. The direction mapping is inherited, not revalidated by this update.

[Dated correction register](../../../data/editorial-paper-corrections-v1.json)

- Source: [https://arxiv.org/abs/2605.26558](https://arxiv.org/abs/2605.26558)

| Field | Current record |
|---|---|
| Problem | Reasoning LLM decoding at the edge incurs high per-token cost, while prior self-speculative approaches can have weak low-batch behavior, training requirements or representation-conversion overhead. |
| Mechanism / artifact | Training-free self-speculative decoding pipeline using fine-grained data selection, pruning, mantissa truncation, salient-weight/KV-cache selection and a lightweight hardware encoder-decoder for format conversion. |
| Workload / benchmark | Reasoning LLM inference including Llama 3 8B on NVIDIA GeForce RTX 4090 in low-batch edge-style decoding; prompts, batch/sequence distributions, quality rule, acceptance behavior and broader models are unspecified. |
| Hardware / process | Commercial GPU/NPU integration with lightweight format conversion; exact area, frequency, power, supported formats, memory hierarchy, conversion cost and device coverage are unspecified. |
| Baselines | BF16 full-precision decoding; Eagle-3 self-speculative decoding; Prior layer-skipping and structured KV-compression methods; Model, prompt, batch, quality, acceptance, memory, hardware and latency-boundary parity are unspecified |
| Metrics | The primary preprint abstract reports up to 2.41x speedup over BF16, 1.81x more tokens than Eagle-3 at the same memory budget, Llama 3 8B on RTX 4090 and training-free operation; acceptance, quality, latency and cost definitions are unspecified. |
| Evidence locator / span | Primary arXiv preprint abstract and data/review-packets/isca-2026-program-006.json: training-free self-speculative decoding; fine-grained data selection; pruning/mantissa truncation; salient weights/KV cache; hardware encoder-decoder; 2.41x BF16 and 1.81x Eagle-3 memory-budget headline; exact full-paper locations not recorded. |
| Limits | Draft tokens are useful only when accepted enough to offset draft and verification work; generated-token count is not accepted-output latency or reasoning-task success.; Pruning, mantissa truncation and KV-cache selection reduce different representations and can change numerical behavior or remove context; format conversion makes a representation executable but adds cost.; Training-free does not mean calibration, selection, conversion or runtime overhead is absent, and a commercial GPU result does not establish an edge NPU implementation.; The captured evidence is a preprint abstract with no exact page/table location, acceptance/quality protocol, prompt distribution, hardware area/power or independent reproduction; general deployment benefit remains unestablished. |

<details markdown="1">
<summary>Historical captured record — superseded in the current table</summary>

Historical atlas evidence tier: `primary_preprint`.

| Field | Historical record |
|---|---|
| problem | Reasoning LLMs incur high decode-stage overhead at the edge, while existing self-speculative decoding methods can have weak low-batch performance or require additional training; representation-conversion overhead also limits practical deployment. |
| mechanism | A training-free self-speculative decoding pipeline using fine-grained data selection, pruning, mantissa truncation, salient weight/KV-cache selection, and a lightweight hardware encoder-decoder for format conversion. |
| workload | Reasoning LLM inference, including Llama 3 8B on an NVIDIA GeForce RTX 4090, evaluated in low-batch edge-style decoding scenarios. |
| hardware | Commercial GPU/NPU integration with a lightweight format-conversion module; exact area, frequency, power, supported formats, acceptance-rate behavior, and broader device coverage require full-paper verification. |
| baselines | BF16 full-precision decoding; Eagle-3 self-speculative decoding; prior layer-skipping and structured KV-compression methods |
| metrics | up to 2.41x speedup over BF16; 1.81x more tokens than Eagle-3 at the same memory budget; Llama 3 8B on NVIDIA GeForce RTX 4090; training-free operation |
| limits | The evidence is an author preprint abstract; exact quality/acceptance measurements, prompt and batch distributions, hardware area and power, format support, and generalization beyond Llama 3 8B and the RTX 4090 remain to be verified from the full paper. |
| locator | Cassandra is an algorithm-hardware co-designed, training-free self-speculative decoding framework for low-batch reasoning LLM inference. It constructs a draft model through fine-grained data selection, uses pruning and mantissa truncation to select salient weight and KV-cache values, and adds a lightweight encoder-decoder hardware module to reduce format-conversion overhead when integrating with commercial GPUs and NPUs. The paper reports up to 2.41x speedup over BF16 and 1.81x more tokens than Eagle-3 under the same memory budget on Llama 3 8B with an NVIDIA GeForce RTX 4090. |

[Historical source](https://arxiv.org/abs/2605.26558)

</details>


Mapping review status: `not_recorded`; independent review status: `pending`.

## Direction boundary

Workloads, topologies, memory technologies, and metrics differ; no CXL, PIM, HBM, or scheduler ranking is supported. Speedup claims remain conditional on model suite, sequence length, accuracy, area, energy, precision, and baseline hardware.

Next evidence action: Sweep resident and nonresident working sets, locality, contention, recall/accuracy, equal capacity/bandwidth, and host/migration overhead.
