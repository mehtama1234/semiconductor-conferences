# Storage and data movement

This subject has 14 records in the selected sample. This page explains where it fits, then presents all captured paper evidence without shortening the measurements or limitations.

[Definitions used in the paper records](../reading-guide-v1.md)

## Understand the parent subject first

- [Memory interconnect and storage](../themes/memory-interconnect-and-storage.md)

## What a storage request actually requires

A program requests a value using a logical address or a higher-level query. The storage system must locate the data, transfer the relevant bytes, and deliver the result in a usable form. Software queues, caches, device controllers, and physical media all contribute time and energy.

The amount transferred can exceed the amount returned to the program. A database scan may inspect many records to produce a small answer. A storage device may read or rewrite units larger than the particular value updated. Understanding those differences is necessary before claiming that faster media or an accelerated operation will improve the whole request.

## Where coordination adds cost

A server can contain several processors, memory regions, and storage devices. Access costs can depend on which processor runs an I/O thread, where the cached data resides, and where the device attaches. NUMA means non-uniform memory access: access time depends on location within the machine.

If a thread executes far from its cached data or storage path, requests can cross shared connections unnecessarily. Placing the thread and data together can reduce this traffic, but may overload that location or limit scheduling flexibility. A placement policy therefore needs both locality and load information.

<span id="explanation-dac-2026-research2074"></span>

## Z-ParaSwap: spreading correlated graph pages can expose ZNS parallelism, but swapping remains part of GNN execution

Zoned Namespace (ZNS) SSDs expose some physical organization to the host. That visibility lets software place data across zones and exploit parallel chips, but it also imposes zone and write-order rules. A heterogeneous GNN (HetGNN) adds an irregular access pattern: feature, relation and embedding pages may be touched according to graph sampling and traversal decisions rather than a sequential scan. When those pages are missing from memory, the swap path becomes part of the GNN's latency and throughput.

Z-ParaSwap is described as finding access correlations in graph data and distributing highly correlated pages across different SSD chips. The intent is to let requests that are likely to arrive together use parallel devices instead of contending at one chip. This changes page placement and swap management; it does not change the GNN's aggregation semantics, guarantee that correlations persist across phases, or create bandwidth when all chips share a saturated controller or link.

The first gate is semantic and placement correctness. Define the page granularity, correlation window, graph sampling/traversal, placement function, zone allocation, migration and update protocol, and the consistency rules for features, edges and intermediate states. Replay the same GNN access trace under the proposed placement and verify that every page contains the intended version and that sampling, aggregation, relation types and output accuracy are unchanged. A lower page-fetch time is not useful if stale or mis-associated graph data changes the model result.

The second gate is storage-system accounting. Measure page faults, reads/writes, bytes moved, queue depth, chip/channel/controller utilization, PCIe and host-memory traffic, queueing, garbage collection, write amplification, migration cost and p50/p95/p99/p99.9 latency. Include correlation analysis, placement, zone management and synchronization in the end-to-end boundary. Test graph scale, working-set pressure, batch/concurrency, sampling policy, phase changes, unseen graphs and background storage activity; a placement learned from one traversal can become a hotspot in another.

The third gate is ZNS and device durability. State zone size and limits, SSD channels/chips, NAND generation, controller/firmware, queue policy, host kernel, link, read/write mix and garbage-collection behavior. Separate read-only swapping from writes or migration that consume NAND program/erase budget, and report endurance or write-amplification impact. Compare conventional paging, Linux ZNS swapping and ZNS-oblivious GNN execution on the same SSD, memory capacity, graph/model, queue depth, software stack and quality requirement.

The official description reports 34% lower average swapping latency and 44% lower tail swapping latency, with improved overall HetGNN execution efficiency on ZNS-based systems. It does not expose absolute latency, tail definition, graph/model and sampling conditions, SSD configuration, GNN accuracy, end-to-end runtime, background activity, write amplification or endurance. The evidence supports access-aware ZNS swapping for HetGNNs, not demonstrated general GNN speedup or durable SSD efficiency.

## Laelaps changes three connected decisions

The official description of Cache Where It Counts names Laelaps and describes storage-aware cache placement, alignment of I/O threads with that placement, and selection of eviction policies based on access patterns. It reports a 1.41× geometric-mean throughput improvement with 3.5% runtime overhead. Those are author-reported summary values; the description does not establish per-workload results, slow-request behavior, fairness, or the full configuration. [Official description](https://63dac.conference-program.com/presentation/?id=RESEARCH651&sess=sess162)

The causal question is which unnecessary cross-location accesses disappear and what policy-management work replaces them. An average gain can coexist with regressions for some workloads, so a deployment decision requires the distribution of outcomes and the system conditions.

<span id="explanation-dac-2026-research444"></span>

## GWrite: memory-side replication removes a host bottleneck only if ordering, failure recovery and RNIC capacity remain correct

Disaggregated memory lets a compute node access memory attached to another node over a fabric. Replication adds a second requirement: a write must reach enough replica locations, in the right order and under the declared durability/consistency rule, before the system reports completion. With host-managed synchronous fan-out, the compute node's RDMA NIC can become the serialization point as the replica count grows. Moving the fan-out closer to the memory nodes may free host-side issue capacity, but it does not eliminate packets, acknowledgments, queueing or failure handling.

GWrite is described as a hardware-oriented RDMA primitive, with GWrap as the co-designed replication protocol. Together they offload replication fan-out to memory-side RNICs while preserving one-sided RDMA semantics. The key mechanism is therefore where replication requests are issued and expanded, not a relaxation of the consistency guarantee. The implementation must specify packet and descriptor format, ownership, write visibility, completion and acknowledgment, duplicate suppression, ordering across replicas, retry and timeout behavior, and how reads, atomics and recovery interact with a partially completed fan-out.

The first gate is history and failure correctness. Define the consistency and durability target, replica quorum or completion rule, fencing, failure detector, crash persistence and recovery protocol. Compare returned histories and final values with a trusted host-managed reference under concurrent writes, reordering, packet loss, duplicate packets, compute-node failure, memory-node failure and RNIC reset. A reduction in compute-node NIC traffic is not evidence that a transaction is serializable or that an acknowledged write survives the stated failures.

The second gate is complete replication-path accounting. Measure compute- and memory-side RNIC queue occupancy, packets and bytes, link utilization, memory-controller contention, CPU work, acknowledgments, retries, backpressure, batching, synchronization, p50/p95/p99 write and transaction latency, throughput and energy. Include protocol setup, metadata, background replication, recovery and tail behavior. GWrite relocates outbound work; the memory-side RNICs and shared fabric can become the new bottleneck, especially as replicas or concurrent writers increase.

Evaluate replica count, node count, object/value size, read/write mix, transaction conflicts, concurrency, topology, link contention and workload phases. Compare synchronous host fan-out, GWrite/GWrap and batching or asynchronous alternatives under the same RDMA transport, hardware, software, consistency/durability target, failure budget and end-to-end boundary. Report per-workload results and the saturation point rather than only the best replication factor.

The official description reports a software prototype that emulates GWrite on commodity RNICs, with up to 2.18× higher throughput in a distributed transaction system and replication-induced throughput degradation reduced from 46.7% to 19.7% in a replicated hash table. It does not expose absolute throughput, latency tails, consistency histories, fault recovery, RNIC utilization, bandwidth, energy, topology, scale or memory-side RNIC hardware results. The evidence supports memory-side replication offload, not demonstrated durable, low-tail-latency distributed-memory scaling or hardware-level RDMA benefit.

<span id="explanation-dac-2026-research651"></span>

## Laelaps: NUMA-aware cache placement must be evaluated as one I/O coordination path

In a NUMA server, a CPU core, memory region, PCIe root complex and NVMe device have locations and links. A page-cache hit still costs different amounts depending on which CPU accesses the page; a miss adds a request to the device attached to some path. I/O-thread affinity, cache placement and eviction therefore interact. Improving one locality decision can overload a node, increase queueing, or move misses to a slower device.

Laelaps is described as three coordinated mechanisms: it places cache pages near their backing NVMe devices, schedules I/O threads according to that cache/storage topology, and chooses eviction policies from observed workload access patterns. The combination addresses placement, execution locality and reuse. It must define page migration and invalidation behavior, cache ownership, thread affinity changes, policy-selection interval, observation window, cold-start behavior and what happens when the local node or device is full.

The first gate is request correctness and fairness. Verify that cache coherence, write ordering, durability, page ownership, eviction, readahead and direct-I/O interactions remain valid. Measure per-workload throughput, p50/p95/p99 latency, queue depth, cross-node bytes, cache hit rate, device utilization, CPU overhead, migrations and policy decisions. A geometric mean can improve while latency-sensitive or low-bandwidth tenants regress.

The second gate is overhead accounting. Include topology discovery, monitoring, policy inference, page migration, scheduler decisions, synchronization, NUMA imbalance, cache warming, background writeback and device garbage collection. Compare topology-oblivious allocation and scheduling, fixed eviction, manually tuned programmable policies and each Laelaps mechanism ablated under the same node/device placement, workload mix and time budget.

The official description reports a 1.41× geometric-mean throughput improvement with 3.5% runtime overhead. It does not provide workload identities, topology scale, device configuration, tail latency, fairness, per-workload variance, policy-selection cost or baseline tuning. The evidence supports workload-aware NUMA/storage coordination, not demonstrated universal throughput improvement or a bounded overhead across deployments.

## Moving computation toward stored data

In-storage processing executes some filtering, searching, or other computation before transferring data to the main processor. It is attractive when much of the read data can be discarded near its storage location. The storage device must still perform the work and return a correct result with sufficient throughput.

HDDB's captured description combines a representation for database values with operations on ferroelectric NAND flash. Its open questions include query correctness, false matches, device overhead, and the energy boundary. The representation and device behavior must be checked together before interpreting a database-level claim. [Recorded evidence](../observed-subthemes/storage-and-data-movement.md#paper-dac-2026-research1619)

<span id="explanation-dac-2026-research1619"></span>

## HDDB: noise-robust in-storage SQL must preserve query semantics at the complete device boundary

An SQL predicate maps rows to a Boolean decision, and aggregation combines the selected values. Hyperdimensional computing (HDC) represents data with high-dimensional distributed vectors, so similarity and bitwise operations can implement approximate or redundant versions of those decisions. That representation can be tolerant of some corrupted components, but tolerance must be measured against the exact predicate, filter cardinality, aggregate, and false-positive/false-negative rule.

HDDB is described as an HDC and ferroelectric-NAND (FeNAND) multi-level-cell co-design. It encodes standard SQL tables for in-storage predicate evaluation and analytics, using FeNAND parallelism and HDC redundancy to tolerate device noise without explicit ECC. This moves work and data reduction toward storage, but it also couples encoding, sensing, analog levels, bit errors, HDC decoding, query execution, and result transfer. “No explicit ECC” is not the same as no redundancy or no recovery cost.

The first gate is database correctness. Hold the original table, SQL semantics, NULL and type rules, predicate thresholds, aggregation, ordering and output format fixed. Compare exact rows and aggregates with a trusted CPU reference under clean and corrupted storage. Report false positives, false negatives, aggregate error, undecodable queries and whether a corrupted vector can produce a plausible but wrong answer. A correct HDC decode is not automatically a correct SQL result if the encoding or threshold operation changes the predicate.

The second gate is a real device and energy boundary. Include table encoding, programming, FeNAND sensing, MLC/TLC level discrimination, peripheral circuits, HDC operations, controllers, metadata, query setup, host transfer, decoding, result materialization, wear management and any ECC or calibration work. State cell corruption distribution, level, spatial correlation, retention and endurance conditions. A random-cell corruption experiment does not establish behavior under structured faults, drift, coupling, stuck cells or aging.

The reported TPC-DS evaluation claims up to 80.6× lower latency and 12,636× lower energy than conventional CPU/GPU SQL engines, with correct predicate and decode outcomes under up to 10% randomly corrupted TLC cells. The official description does not provide query set, table size, HDC dimension, FeNAND geometry, sensing method, corruption denominator, false-error rates, device overhead, CPU/GPU tuning or energy boundary. The evidence supports a noise-robust in-storage SQL direction, not demonstrated exact database correctness or general end-to-end latency and energy gains.

<span id="explanation-dac-2026-research1570"></span>

## NVLLM: NAND-resident inference must prove data delivery, numerical fidelity, and endurance together

NVLLM places a large part of an LLM's storage and computation path in 3D NAND. The proposal assigns FFN work to the flash array, keeps attention on lightweight CMOS logic with external DRAM, decomposes matrix operations into dot-product primitives, and uses ECC and a KV-cache-aware scheduler. The architectural idea is to reduce DRAM weight traversal for single-batch decoding. A large storage capacity does not by itself establish the access time, parallel delivery rate, numerical behavior or lifetime required for inference.

The first gate is numerical correctness. Raw NAND reads, ECC, analog or mixed-signal dot products, finite precision and accumulation must reproduce the intended GEMM/GEMV semantics. Compare layer outputs and final model outputs with a trusted digital reference across OPT and LLaMA variants, quantization, sequence lengths, KV-cache growth and exceptional values. Report perplexity, task quality, output agreement, error distributions, failed reads and unsupported operators. A storage-centric path that returns weights quickly but changes attention or FFN outputs is not an equivalent inference engine.

The second gate is the complete physical data path. State NAND generation, page/read latency, channel and plane parallelism, raw-read interface, ECC throughput, PE lanes, buffers, controller scheduling, DRAM/KV traffic, queueing, thermal conditions and power. Measure attention, FFN, transfers, decode, initialization and idle work together, including p50/p95/p99 token latency and throughput as context grows. Area must include NAND-adjacent compute, ECC, buffers, CMOS attention logic, controller and interfaces, not only the CMOS overhead selected for the headline.

Endurance is a separate deployment constraint. If inference updates metadata, KV state, calibration data or any NAND-resident state, measure program/erase activity, read disturb, retention, wear leveling and lifetime under sustained serving. If weights are read-only, state that assumption and include the controller, refresh and thermal limits that still affect availability. A speed comparison against an A800 or SSD-like design is meaningful only with matched model precision, quality target, context, cache policy, storage hierarchy, software overhead and full latency/energy boundaries.

The official description reports 16.7× speedup over A800 out-of-core inference, 1.1×–4.7× improvement over SSD-like designs and 2.7% CMOS area overhead for OPT and LLaMA models up to 30B parameters. The captured evidence does not expose absolute latency or energy, precision, model quality, NAND/process conditions, capacity, endurance, controller/peripheral costs or per-model results. It supports a 3D-NAND-centric LLM architecture direction, not demonstrated durable, quality-preserving end-to-end edge inference. [Recorded evidence](../observed-subthemes/storage-and-data-movement.md#paper-dac-2026-research1570)

<span id="explanation-dac-2026-research1291"></span>

## NASiC: dense expert storage is not yet quality-preserving on-device MoE inference

Mixture-of-Experts (MoE) models store many expert networks but activate only a small subset for each token. That sparsity can reduce arithmetic, while the inactive experts still consume capacity and must be selected, addressed and delivered. The useful system boundary therefore includes routing, expert movement, storage reads, arithmetic, combination, host control and output quality—not just the density of the memory array.

NASiC is described as an algorithm--hardware co-optimization using 3D NAND for dense storage, CAM to select experts, and multibit computing-in-memory (CIM) for the selected computation. The source names V-ASIC as the proposed architecture. CAM matching can reduce a separate expert-index traversal and multibit CIM can place more values in each cell, but the captured description does not specify the expert encoding, top-k behavior, sensing/ADC path, accumulation, precision, controller or dataflow. These choices determine whether the array's match and arithmetic correspond to the intended MoE computation.

The first gate is routing and numerical correctness. Compare selected experts, top-k ties, load balance, dropped tokens, capacity overflow, dispatch/combination and final expert outputs with a trusted digital reference across sequence length, batch size and routing distributions. Then evaluate layer and model outputs under the stated precision, multibit encoding, ADC quantization, accumulation, noise and variation. Report perplexity or task quality, error tails, unsupported cases and the cost of calibration, ECC and controller recovery.

The second gate is device and system efficiency. State NAND generation/process, cell levels, array geometry, read/program conditions, sensing and ADC/DAC, parallelism, buffers, controller, host interface, thermal state, retention, read disturb, write endurance and ECC. Measure token latency, throughput, energy per token, area, density and capacity with CMOS peripherals and data movement included; separate steady-state reads from initialization, writes, calibration, refresh and failure recovery. Compare DRAM/GPU inference, NAND storage with digital compute and other on-device MoE accelerators at the same model, top-k policy, precision, quality target, capacity and software boundary.

The official description claims improved throughput and high area- and energy-efficiency for V-ASIC, but provides no numerical results, MoE workload, model quality, precision, device/process conditions, peripheral overhead, endurance or end-to-end measurement. The evidence supports a 3D-NAND CAM-selected multibit CIM direction for dense expert storage, not demonstrated quality-preserving on-device MoE efficiency or durable device-to-system benefit.

<span id="explanation-dac-2026-research282"></span>

## HiBand: more in-situ DRAM bandwidth still requires a measured NoC schedule

Hybrid-bonding 3D DRAM can place compute and memory resources close enough to expose very high local bandwidth. That changes the bottleneck rather than removing it: many banks and arrays must share a network-on-chip (NoC), and a tensor partition that is fast at one bank can create a hotspot at a link, buffer or reduction point. The useful quantity is achieved delivery under the real schedule, not the sum of nominal bank bandwidths.

HiBand is described as co-designing grouped tensor parallelism and cross-head array-level co-execution with a four-mode reconfigurable NoC. It overlaps bandwidth-bound attention with compute-bound feed-forward layers. These mechanisms can confine traffic to short links and expose independent work, but the captured description does not specify the mapping, routing, buffers, multicast/reduction behavior, mode-switch cost or control policy. A reconfigurable NoC can also add area, state and scheduling complexity.

The first gate is movement and routing validity. Report offered and achieved bandwidth by bank, array and link, queueing, conflicts, buffer occupancy, stalls, multicast/reduction traffic, synchronization and reconfiguration overhead for each attention and FFN phase. Fix the 32-array organization, frequency, tensor partitions, sequence/batch workload and compiler/runtime. Validate that all routes are legal and that no hidden serialization or bandwidth assumption is omitted.

The second gate is LLM correctness and system accounting. Compare array-executed outputs with a trusted digital reference across precision, sequence length, KV-cache growth, tensor-parallel reductions and concurrency; report perplexity, task quality and numerical error. Include NoC, buffers, controllers, DRAM interfaces, thermal/power and area costs, and compare against HBM3 GPU-style and HB-DRAM NMP baselines under the same model, quality, capacity and latency/energy boundary.

The official description reports up to 4.28× speedup over an HBM3 GPU-style accelerator and 1.67× speedup over a state-of-the-art HB-DRAM-based NMP design on a 32-array HB-DRAM accelerator. The captured evidence does not expose absolute results, model/precision conditions, bandwidth utilization, NoC overhead, area, energy, process details or hardware validation. It supports bandwidth-aware HB-DRAM/NoC co-design, not demonstrated portable end-to-end LLM acceleration or physical 3D-DRAM efficiency.

## Reliability can create additional movement

Storage protection often retains extra information that permits detection or reconstruction of damaged data. Updating protected data can require updating that additional information. Moving valid data while reorganizing storage can create still more physical writes than the application requested.

SSD Reforge's record proposes changing parity protection as flash ages. Parity is additional information computed from stored values and used to help detect or recover certain errors. Stronger protection can extend usable operation under a stated error model, but may consume capacity, controller time, and write bandwidth. The captured record leaves those costs and the error-model calibration unresolved. [Recorded evidence](../observed-subthemes/storage-and-data-movement.md#paper-dac-2026-research1872)

<span id="explanation-dac-2026-research1872"></span>

## SSD Reforge: extra parity extends endurance only if the reliability model and protection cost are real

Flash aging increases the raw bit-error rate (RBER), so an SSD eventually reaches a controller-defined lifetime limit even when the host still has useful data to write. Parity adds information that can detect or reconstruct errors across a stripe. Dynamic parity management changes the protection level as blocks age instead of applying one fixed protection policy to the whole device. That can trade spare capacity and controller work for additional usable total bytes written (TBW), but the trade is meaningful only when the error distribution and recovery budget match the real device.

SSD Reforge is described as estimating an RBER-based error probability for heterogeneous blocks, solving parity-stripe grouping as a combinatorial optimization, and using Reliability-Aware Striping (RAS) to form groups. Stripe UPER Leveling (SUPERL) maintains the grouping as later writes change the device state. The important system boundary is therefore not just the grouping algorithm: it includes RBER estimation, parity generation and checking, allocation, migration or rewrite behavior, flash wear, controller scheduling and the definition of the lifetime limit.

The first gate is reliability-model calibration. Specify the NAND generation, page/block geometry, ECC and decoding assumptions, error correlation, retention age, read disturb, program/erase history, temperature, voltage and how RBER is measured. Compare predicted block error probabilities with held-out device measurements across aging states. A model that ranks blocks correctly on one trace can still misestimate tail failures or correlated errors, which determine whether a parity stripe actually remains recoverable.

The second gate is complete cost accounting. Report parity capacity, user-visible capacity, metadata, extra reads and writes, parity-update traffic, write amplification, garbage collection, latency tails, controller CPU, energy and bandwidth. Compare fixed protection, conventional dynamic protection and an oracle with the same NAND geometry, ECC, overprovisioning, workload, lifetime criterion and background maintenance. Include RAS construction, SUPERL updates, degraded blocks, failed stripes and recovery in the end-to-end time and endurance budget.

The official description reports FEMU experiments with real I/O traces and up to 40% average user-TBW improvement over traditional mode at the lifetime limit. It does not expose NAND/process conditions, trace diversity, parity budget, RBER calibration, ECC baseline, capacity loss, write amplification, latency, energy, tail reliability or the exact lifetime accounting. The evidence supports adaptive parity and reliability-aware striping as an SSD-endurance direction, not demonstrated device-level endurance improvement without performance, capacity or energy tradeoffs.

## How to compare complete requests

Hold the data, query or request sequence, answer requirements, and durability guarantees fixed. Report bytes read and written at both the application and device levels. Measure throughput, slow-request latency, processor overhead, energy, and capacity devoted to metadata or protection.

For a long-running storage system, state whether the measurements include background cleanup, aging, recovery, and changing request patterns. A method that wins on an empty device or one short trace may behave differently after the system has reached sustained operation. The transferable result is the identified source of saved work under those stated conditions.

<span id="explanation-dac-2026-research698"></span>

## FreeZone: SLC-backed out-of-order buffering helps only when zone ordering and durability remain intact

Zoned storage exposes an important constraint: writes within a zone must advance in logical order. Consumer workloads can generate irregular writes, so enforcing that order in the kernel may serialize requests and leave device channels idle. Moving reordering into the SSD can recover parallelism, but it also makes the device responsible for holding, ordering and safely acknowledging data that the host submitted out of order.

FreeZone is described as allowing the kernel to submit I/O requests freely and extending the on-device reorder buffer with high-performance SLC flash. Requests can remain in that buffer until they are committed in legal zone order. The mechanism changes the location and capacity of ordering state; it does not specify the zone write pointer, request identity, append/overwrite semantics, barriers, flush/FUA, zone reset, admission/backpressure, metadata persistence or flush policy.

The first gate is zone and durability correctness. Define per-zone ordering, visibility, acknowledgments, synchronization, reset and failure semantics. Check that every committed sequence is legal and that a host completion does not imply durability before reordered data and metadata are protected. Test power loss, controller reset, torn metadata, aborted or duplicate requests, replay, zone reset, full SLC and concurrent reads; a higher IOPS result is invalid if a zone becomes inconsistent or acknowledged data disappears.

The second gate is the physical buffer tradeoff. SLC capacity used for reordering consumes flash resources and can create migration, garbage-collection, metadata and endurance costs. Measure SLC occupancy, admission/backpressure, spill/fallback, migration bytes, logical-to-physical writes, write amplification, channel utilization, queueing, p50/p95/p99 latency, energy and TBW under sustained and bursty workloads. Include reorder decisions, buffer management, recovery and cleanup in the IOPS boundary.

Compare host-side ordering, strict in-order writes and prior limited-buffer device reordering with the same zone rules, host/kernel/filesystem, device capacity, SLC budget, queue depth, request trace, durability contract and recovery path. Test device aging, thermal throttling, full SLC, mixed reads and changing write phases. The official description reports up to 2.3× IOPS improvement over existing zoned-storage architectures, but provides no absolute IOPS, latency tails, write amplification, SLC cost, endurance, crash result or ordering trace. The evidence supports SLC-backed on-device zoned-write reordering, not demonstrated crash-safe consistency, durable endurance benefit or portable 2.3× end-to-end performance.

<span id="explanation-dac-2026-research609"></span>

## LLM-hybridSSD: adaptive tuning helps only when the learned controller remains safe and durable

A hybrid SSD can combine flash modes such as SLC and QLC, converting or migrating data between them to trade latency, capacity and endurance. That enlarges the controller's design space: placement, garbage collection, conversion, migration, wear leveling and queue scheduling interact with workload phases. A parameter setting that raises throughput during one phase can increase physical writes, tail latency or lifetime cost during another.

LLM-hybridSSD is described as formulating hybrid-SSD management as parameter tuning, using an LLM-based tuner for adaptive configuration and applying reinforcement-learning fine-tuning to align lightweight local models with domain-specific SSD knowledge. The LLM supplies contextual knowledge or configuration proposals; the local model supports cheaper repeated decisions. The captured description does not specify the state/action representation, reward, training data, safety constraints, update cadence, fallback, deployment path or controller integration.

The first gate is controller safety. Define legal placement, mapping, conversion, migration, garbage-collection, ECC, wear-leveling, crash-consistency and power-loss constraints. Use a guarded controller that rejects unsafe actions and test stale telemetry, invalid parameters, model failures, firmware restart, power loss and concurrent host I/O. A learned policy is not a replacement for FTL invariants; higher throughput is not a valid result if data is lost, mappings become inconsistent or latency SLOs are violated.

Write amplification needs a complete physical accounting. Separate host writes, conversion/migration writes, garbage collection, metadata/ECC, refresh and recovery. Measure logical-to-physical write ratio, bytes, migration traffic, queueing, channel utilization, p50/p95/p99 latency, energy and lifetime/TBW under sustained aging. Include profiling, LLM calls, RL or local-model inference, retraining, policy transfer, fallback and controller CPU/memory. A lower reported WA can hide extra background writes or exclude the cost of learning and adaptation.

Validate transfer and stability on complete held-out workloads, unseen read/write mixes, capacity pressure, burstiness, temperature and aging. Hold flash modes, capacity, overprovisioning, FTL/ECC, controller resources, queueing, latency target, tuning budget, warm-up and long-run boundary constant against state-of-the-art hybrid management, heuristics and LLM-free policy learning. Report per-trace results, adaptation time, unsafe-action/fallback rate and policy oscillation rather than only an average.

The official description reports average 58.92% higher throughput and 28.56% lower write amplification than state-of-the-art schemes across different real-world workloads. It does not expose absolute latency or tails, endurance/TBW, energy, conversion/migration traffic, capacity, policy/LLM cost, safety violations or per-workload variance. The evidence supports knowledge-guided adaptive hybrid-SSD management, not demonstrated safe, durable, low-tail or universally better controller behavior.

<span id="explanation-dac-2026-research442"></span>

## VALVE: in-storage visible-version search helps only when MVCC visibility survives the host–CSD boundary

Multi-Version Concurrency Control (MVCC) keeps several committed versions of a row or record so readers can use a consistent snapshot while writers continue. An analytical query must find the newest version that is visible to its transaction timestamp; under frequent HTAP updates, the version chain becomes longer and the search can cause more storage reads and host processing. Moving that search into a computational-storage device can reduce host I/O, but it also moves a transaction-correctness decision across a device boundary.

VALVE is described as offloading Visible Version Searching (VVS) to a CSD and first addressing consistency under host–CSD concurrency. It adds a frugal skip list to accelerate traversal of version chains. The skip list changes how versions are reached, while the offload changes where visibility metadata is interpreted. The captured description does not specify timestamps, snapshot semantics, version ordering, metadata ownership, update/delete protocol, skip-list maintenance, synchronization, persistence or recovery.

The first gate is visibility correctness. Define transaction timestamps, commit/abort visibility, snapshot isolation or serializability target, deletes, updates, chain ordering and result completeness. Compare host and CSD answers under concurrent commits, aborts, retries, stale metadata, long chains and changing snapshots. A lower scan latency is not valid if a query reads an uncommitted or too-new version, misses a committed version, or returns a result inconsistent with the database engine.

The second gate is skip-list and path accounting. Expose level construction, key/order, insertion/deletion, stale-index fallback, memory placement, synchronization and rebuild cost. Measure version-chain length, metadata bytes, host/CSD traffic, random reads, queueing, CPU/CSD utilization, lock/wait time and p50/p95/p99 analytical and transaction latency under read-heavy, update-heavy and mixed loads. Include query setup, CSD dispatch, result transfer, skip-list maintenance and cache warm-up; fewer host requests can leave the CSD or storage medium saturated.

The CSD creates a distributed failure boundary. Test power loss, device reset, host failure, partial metadata writes, retries, duplicate requests, firmware restart and recovery, and state which data and visibility metadata are durable. Compare host-side VVS and generic in-storage processing with equal isolation, cache, hardware, workload, batching, warm-up and recovery cost. The official description claims reduced end-to-end analytical scan latency and improved analytical throughput, but provides no absolute results, I/O/CPU reduction, consistency test, transaction impact, energy, endurance or failure evidence. The evidence supports CSD-assisted MVCC visible-version traversal, not demonstrated consistency, failure-safe persistence or portable end-to-end HTAP improvement.

<span id="explanation-dac-2026-research484"></span>

## SmartSwap: adaptive tensor swapping helps only when training semantics and overlap survive Eager Mode

LLM training can exceed GPU HBM because activations, gradients, optimizer state and temporary buffers peak at different points in the operator sequence. Swapping tensors to host memory or storage can extend capacity, but each eviction and fetch competes with forward/backward computation for bandwidth and synchronization. Eager Mode makes the schedule harder: operator sequences can vary between iterations, so a policy learned from one sequence can become stale.

SmartSwap is described as an end-to-end swap optimizer for varying Eager-Mode sequences. A lightweight online profiler monitors operator sequences, a policy generator works with limited operator information, and an optimized policy-execution module applies the policy accurately. These mechanisms target schedule adaptation and runtime overhead. The captured description does not specify tensor lifetime inference, policy representation, profiler sampling, prefetch/eviction rules, overlap scheduler, correctness barriers or whether the swap tier is CPU memory, storage or both.

The first gate is training correctness. Define tensor versions, autograd and lifetime dependencies, optimizer state, checkpoint/recomputation interaction, precision, synchronization and eviction/prefetch barriers. Compare loss curves, gradients, checkpoints and final model quality with a no-swap reference while operator sequences change. A model fitting in HBM plus swap is not equivalent training if a stale, partially transferred or incorrectly synchronized tensor enters backpropagation.

The second gate is the training critical path. Measure profiling, policy generation, CPU/GPU scheduling, pinned-memory and DMA setup, HBM eviction/fetch, host/storage transfer, synchronization, queueing, stalls, policy misses, fallback, residency and p50/p95/p99 iteration time. Include cold start, phase changes, failed transfers, model loading and policy execution. An 84.25% reduction in profiling overhead can coexist with slower training if transfer or synchronization dominates; overlap must be demonstrated at the iteration boundary, not inferred from component time.

Capacity and performance need matched baselines. Hold model, batch, sequence length, optimizer, precision, convergence target, GPU/HBM, interconnect/storage, warm-up and baseline tuning constant against static checkpointing, naive swapping, recomputation and higher-degree parallelism. Test irregular control flow, operator-sequence shifts, long runs, memory pressure and concurrent workloads. If storage is written, include write amplification, endurance and energy.

The official description reports 84.25% lower profiling overhead, support for models up to 4× larger than hardware memory, and up to 38.94% performance improvement over recomputation or high-degree parallelism while adapting to operator changes. It does not expose absolute throughput, memory occupancy, transfer volume, convergence/accuracy, energy, tails, policy overhead or long-run storage cost. The evidence supports adaptive Eager-Mode training swap management, not demonstrated accuracy-preserving, universally faster or durable out-of-HBM training.

<span id="explanation-dac-2026-research2773"></span>

## FlashHD: in-storage HDC filtering helps only when exact matches and flash cost survive

Exact DNA-sequence matching often scans a corpus much larger than host memory. The query may return only a few matches, but a conventional system still moves pages from storage, examines them in software and pays page-fault and host-memory costs. In-storage processing can reduce that movement by rejecting dissimilar sequences near the flash array. The rejection must be conservative: a fast filter that discards a true match is not an exact matcher.

FlashHD is described as executing sequence matching directly inside 3D NAND flash with a hierarchical hyperdimensional-computing (HDC) architecture. HDC encodes sequences into high-dimensional representations and compares them through staged similarity/filter operations; FlashHD uses multiple hierarchy levels to remove dissimilar candidates while claiming full recall. A hierarchy-aware architecture search tunes HDC hyperparameters for latency and energy. These mechanisms change the representation and location of filtering, but the captured description does not specify the encoding, dimension, similarity threshold, sensing path, hierarchy, candidate-verification stage or search budget.

The first gate is exactness. Define sequence encoding, match semantics, allowed mutations or edit distance, hierarchy/fanout, HDC precision, threshold and tie behavior. Compare every returned and rejected candidate with a trusted CPU exact matcher, and report false negatives, false positives and recall by sequence length, match rarity and distance. “Full recall” needs a denominator and an independent exact check; HDC collision tolerance or a visually plausible candidate set is not proof that no true sequence was filtered out.

The second gate is the complete flash path. State the 3D-NAND generation, array geometry, channels/planes, raw-read and sensing behavior, ECC, controller, peripheral HDC operations, host link, memory, temperature and queueing. Include encoding, flash reads, staged HDC filtering, candidate transfer and exact verification, query setup, result materialization and calibration in latency and energy. Report bytes read, parallelism, queue depth, device utilization and p50/p95/p99 query latency, not only array-level operation counts. A reduction in host I/O can be replaced by serial sensing, ECC or controller contention.

The architecture search also needs a reproducible boundary. Expose the HDC dimensions, thresholds, hierarchy, objective, search evaluations, training/calibration data, stopping rule and tuning cost. Test unseen sequence distributions, corpus sizes, match rates and changing databases. If data or metadata are written, measure re-encoding, garbage collection, read disturb, retention, program/erase activity and endurance; if the corpus is read-only, state that assumption and include the refresh and thermal limits that govern sustained service.

The official description claims that FlashHD significantly outperforms state-of-the-art systems and that hierarchical filtering preserves full recall for DNA sequence matching. It provides no recall/precision table, latency, throughput, energy, I/O bytes, density, area, endurance, query conditions or per-workload comparison. The evidence supports an in-storage HDC sequence-matching direction, not demonstrated exact-recall, durable flash efficiency or quantitative end-to-end superiority.

<span id="explanation-dac-2026-research2806"></span>

## LHGstore: learned adjacency layout helps only when graph semantics and distribution survive updates

An in-memory graph store has two competing paths. Updates must find and modify the right vertex and edge records, while analytics must traverse adjacency lists with predictable locality. A single layout can waste space or cause pointer chasing when degree varies widely: a low-degree vertex benefits from compact arrays, while a high-degree vertex may need an index to avoid shifting or scanning many neighbors. The useful result is therefore a complete update-and-query tradeoff, not an isolated lookup speed.

LHGstore is described as a degree-aware Learned Hierarchical Graph store. Its two-level hierarchy decouples vertex and edge access, uses lightweight arrays for low-degree vertices to preserve traversal locality, and applies learned indexes to high-degree vertices to improve update throughput. This representation changes where adjacency metadata and neighbor access are organized. It does not specify the degree threshold, key/layout encoding, model training or correction, insertion/deletion path, index rebuild policy, synchronization, allocator, migration or persistence semantics.

The first gate is graph correctness. Define vertex and edge identity, duplicate and self-loop rules, insertion/deletion visibility, adjacency ordering, snapshot or transaction semantics and crash recovery. Run analytics against a trusted graph reference while updates occur, including concurrent writes, deletes, degree changes, stale learned predictions, index rebuilds and partial failures. An update-throughput gain is not useful if a traversal observes a missing edge, a duplicate edge or an inconsistent snapshot.

The second gate is the representation cost. Report degree thresholds, array and model bytes, metadata, slack, fragmentation, cache and NUMA misses, pointer chasing, training/correction/rebuild time, synchronization, allocation and migration. Measure absolute p50/p95/p99 update and query latency, update throughput, traversal work, memory per vertex/edge and CPU utilization under read-heavy, update-heavy and mixed workloads. Include index maintenance and graph loading in the stated boundary; a fast steady-state lookup can be offset by rebuilding after a burst.

Learned indexes need a distribution-transfer test. Hold out graph snapshots, unseen graphs and temporal phases, then vary degree skew, neighbor-key distributions, insertions, deletions, bursts, adversarial keys and memory pressure. Compare hash/table and conventional in-memory graph stores with the same CPU threads, cache/NUMA placement, memory budget, batching, consistency, query semantics and warm-up. Report stale-prediction and fallback rates, convergence/rebuild cost and tail behavior rather than only an average.

The official description claims 5.9–28.2× higher throughput and significantly faster analytics than state-of-the-art in-memory graph storage systems. It does not expose absolute update/query results, graph scale, degree thresholds, memory overhead, consistency cost, tail latency, baseline tuning or persistence conditions. The evidence supports degree-aware learned in-memory graph storage, not demonstrated portable 5.9–28.2× end-to-end benefit or stable analytics under dynamic distribution shift.

<span id="explanation-dac-2026-research297"></span>

## EtherSSD: moving authenticated Ethereum queries into storage helps only if proofs, snapshots and trust boundaries remain intact

An authenticated blockchain query does more than read a value. It retrieves ledger or state data and checks auxiliary evidence—such as a Merkle proof—against a committed root for a particular snapshot or version. The proof path, page contents, ordering and query semantics must agree. Moving the work into a computational storage device (CSD) can reduce host I/O and CPU work, but it also moves part of the query and authentication boundary into firmware or device-side computation.

EtherSSD is described as bridging host and CSD semantics, flattening authenticated queries into highly concurrent in-CSD page accesses, and adding an authentication engine to offload cryptographic verification from host CPUs. These choices target page scheduling and hash computation. The captured description does not specify the query operators, proof format, root/version handling, CSD programming model, key/root storage, result materialization, update protocol, concurrency semantics or failure recovery. Lower host request count is not by itself authenticated-query correctness.

The first gate is proof and query fidelity. Define the hash/proof scheme, committed root, snapshot, page order, sibling path, range or aggregate semantics, duplicate/omitted record behavior and result-completeness rule. Compare EtherSSD with a trusted host implementation on valid, malformed, stale, reordered, replayed and adversarial pages; report false acceptance, false rejection, incomplete results and proof failures. If Ethereum reorganization or fork handling is in scope, state the version transition and confirmation assumptions rather than treating one static snapshot as the whole chain.

The second gate is the CSD trust boundary. State which code, pages, metadata, keys and roots are trusted; how device-side results are protected; and what happens under firmware compromise, DMA misuse, corrupted pages, power loss, partial writes, reset, device replacement and snapshot/update races. Test concurrent queries and updates, stale roots, retries and recovery. An authentication engine can reduce host CPU work while leaving a security gap if its inputs or proof result cannot be independently trusted.

The third gate is complete storage accounting. Measure host/CSD/media bytes and page reads, proof hashes, authentication-engine utilization, CPU cycles, queueing, cache hits, controller work, metadata, result transfer, p50/p95/p99 latency, throughput, energy, write amplification and wear. Include query flattening, proof construction, scheduling, initialization, updates and recovery. Compare host-side analytics, unaccelerated authenticated storage, CSD processing without flattening and host versus in-storage authentication under the same chain snapshot, query, proof/security policy, cache state, hardware and end-to-end boundary.

The official description reports reduced authenticated query execution time, particularly I/O and authentication overhead, on real-world workloads. It does not expose query/proof conditions, absolute results, integrity validation, trust/update assumptions, hardware configuration, wear, energy or baseline accounting. The evidence supports authenticated in-storage Ethereum analytics, not demonstrated complete blockchain-query correctness, adversarial storage security or portable end-to-end deployment efficiency.

<span id="explanation-iccad-2025-1144"></span>

## GAIA: glass-aware scheduling must model the mechanical-optical access path

Quartz-glass archival storage combines physical movement and optical focusing. A request may require moving a mechanical stage along X and Y and tuning an optical focus along Z before data can be read. The cost is therefore not determined by geometric distance alone: direction reversals, seek acceleration, focus changes, queue order, parallelism and device state can all affect latency.

GAIA is described as I/O middleware with three coordinated strategies: Zigzag Data Placement aligns data with the stage's natural motion; Z-Axis First Placement prioritizes optical traversal along depth; and Shortest Moving Time First (SMTF) schedules requests using predicted movement time rather than geometric distance. The institutional abstract does not specify the glass encoding, coordinate mapping, stage dynamics, focus model, request concurrency, placement constraints, simulator, or whether writes and failures are modeled.

### Placement and scheduling must preserve logical addresses

Data placement can reduce movement only if the address-to-location mapping remains correct and maintainable. Define object/chunk granularity, X/Y/Z coordinates, page or voxel layout, replication, updates, free space, relocation and metadata recovery. Test reads after placement, mixed reads/writes if supported, queue reordering, retries, partial movement and device restart. A lower movement estimate is not useful if the middleware returns stale, wrong or incomplete archival data.

### Predicted movement time needs calibration and tails

SMTF requires a cost model for stage travel, direction changes, acceleration/deceleration, settling, optical focus, media access and queue interference. A schedule minimizing predicted time can be worse when requests contend for the same stage or when the model omits focus or settling costs. Validate predicted versus measured/simulator service time across directions, distances, depths, queue depths, request sizes, media regions and aging or calibration variation. Report p50/p95/p99/p99.9 latency, starvation, fairness, queueing and throughput—not only an average or best reduction.

The abstract reports up to 82% lower read latency than traditional baseline schedulers using trace-driven simulations on enterprise-scale workloads and varied glass sizes. The institutional record does not identify the traces, glass dimensions, baseline scheduler implementations, movement parameters, latency distribution, simulator validation or absolute results. “Up to” is a maximum claim; it does not establish a typical or deployed-system reduction.

Compare placement and scheduling against FIFO, shortest geometric distance, seek-aware scheduling and the unnamed traditional baselines with the same traces, requests, capacity, glass geometry, media model, queue depth, warm-up and objective. Include placement construction, metadata, scheduler computation, movement, focus, data transfer and result delivery in the end-to-end boundary. This is archival glass storage, not glass substrates for chip packaging or fabricated-chip evidence; the evidence supports a glass-aware I/O scheduling direction, not demonstrated durable, deployable 82% end-to-end archival-storage improvement.

## Compare the results carefully

First identify the inputs and required output quality. Then identify the limited resource: time, memory, communication, energy, circuit area, or correctness coverage. Ask which part of the method reduces that cost and which new cost it adds. Compare numbers only when the experiments hold these conditions sufficiently similar.

A conference description may explain the proposal while omitting the full experiment. An author preprint link may have been coded from its abstract. The source classification does not by itself establish that every table was read. Missing locations remain visible below.

## Complete captured evidence

These are evidence records, not substitutes for the explanations above. Each record preserves its problem, proposed method, measurements, comparison conditions, and source limits. A populated record does not establish that its mechanism has been fully explained or independently verified.

<span id="paper-dac-2026-research1619"></span>

### HDDB: Efficient In-Storage SQL Database Search Using Hyperdimensional Computing on Ferroelectric NAND Flash

DAC 2026 · Record: `dac-2026-research1619`

[Read the step-by-step explanation](#explanation-dac-2026-research1619)

**Updated source-backed reading card**

Reviewed 2026-09-08. Deepens the existing HDDB treatment into a paper-level reading; separates HDC SQL encoding, FeNAND MLC in-storage operations and noise tolerance from predicate/aggregate correctness, false errors, sensing, device overhead, ECC/redundancy and complete latency/energy boundaries, preserves the 80.6x, 12,636x and 10% claims, and makes query semantics explicit.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

SQL scans over large fact tables move substantial data, while dense FeNAND storage and in-storage compute can suffer elevated raw bit-error rates.

**Mechanism / artifact:**

HDC encoding for standard SQL tables with in-storage predicate filtering and aggregation on FeNAND multi-level cells, relying on HDC redundancy under noise without explicit ECC; vector dimension, encoding, sensing and decode are unspecified.

**Workload — the work tested:**

TPC-DS fact-table SQL workloads; tables, queries, predicates, aggregations, data types, table size, HDC dimension, output quality, query concurrency and CPU/GPU engine configurations are unspecified.

**Hardware and manufacturing assumptions:**

Ferroelectric NAND MLC/TLC storage with in-storage compute, controller, sensing and peripheral circuits; geometry, cell levels, process, corruption distribution, retention, endurance, calibration, ECC, interface and energy boundary are unspecified.

**Baseline — the comparison method:**

Conventional CPU SQL database engine

Conventional GPU SQL database engine

Same TPC-DS data and queries, exact SQL semantics, table size, CPU/GPU tuning, device overhead, host transfer, output materialization and full energy/latency boundary are unspecified

**Reported measurements:**

The official description reports up to 80.6x lower latency and 12,636x lower energy than CPU/GPU SQL engines, with correct predicate/decode outcomes under up to 10% randomly corrupted TLC cells; it supplies no false-positive/negative rates, aggregate error, query conditions, device overhead or energy accounting.

**Limits on the conclusion:**

Validate exact predicate rows and aggregates against a trusted CPU reference under clean and corrupted storage, including NULL/type rules, thresholds, ordering and output format. Report false positives, false negatives, aggregate error, undecodable queries and plausible wrong answers; HDC decode correctness alone is not SQL correctness.

Include encoding/programming, FeNAND sensing and level discrimination, peripherals, HDC, controller, metadata, query setup, host transfer, decoding, result materialization, wear, calibration and redundancy/ECC work. Vary random and structured faults, retention, endurance and spatial correlation.

The 80.6x, 12,636x and 10% claims lack query, table, HDC, FeNAND, sensing, corruption, false-error, device-overhead, CPU/GPU and energy-boundary conditions. The evidence supports noise-robust in-storage SQL, not demonstrated exact database correctness or general end-to-end latency and energy gains.

**Source and location**

Evidence tier: Primary captured DAC official description plus existing chapter level conceptual discussion; no full paper extraction, device trace, sql correctness suite or independent review. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH1619&sess=sess120)

DAC 2026 official description; existing chapter-level HDDB discussion; captured Problem, Mechanism / artifact, Workload, Hardware, Baseline, Measurements and Limits fields; no manuscript pages or reproduced FeNAND query run.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** conventional CPU SQL engine

conventional GPU SQL engine

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH1619&sess=sess120

**Hardware or process assumptions:** Ferroelectric NAND multi-level storage with in-storage compute and up to 10% random cell corruption; device process, controller, sensing, and interface are unspecified.

**Limits:** The description omits query accuracy, HDC false-positive/negative behavior, device overhead, table size, and energy boundaries.

Noise tolerance may depend on redundancy, sensing, and data distributions and does not replace full ECC for all workloads.

Official description only; storage and database claims require paper-level verification.

**Method or artifact:** HDC encoding for SQL tables and in-storage predicate/filter/aggregation operations on FeNAND MLC/TLC cells.

**Metrics:** Up to 80.6x lower latency

Up to 12,636x lower energy

Correct predicate/decode outcomes under up to 10% random TLC corruption

**Problem:** SQL predicate scans over large fact tables require data movement, while dense FeNAND storage can have high raw bit-error rates.

**Workload or benchmark:** TPC-DS fact-table SQL workloads; table sizes, queries, FeNAND geometry, HDC dimensionality, and CPU/GPU baselines are unspecified.

</details>

<span id="paper-dac-2026-research651"></span>

### Cache Where It Counts: Towards Workload-Aware I/O Coordination for NUMA Storage Systems

DAC 2026 · Record: `dac-2026-research651`

[Read the step-by-step explanation](#explanation-dac-2026-research651)

**Updated source-backed reading card**

Reviewed 2026-09-08. Deepens the existing Laelaps treatment into a paper-level reading; separates topology-aware page placement, I/O-thread affinity and adaptive eviction from request correctness, cache migration, queueing, fairness, tail latency and complete coordination overhead, preserves the 1.41x geometric-mean and 3.5% claims, and makes NUMA/NVMe conditions explicit.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

NUMA storage stacks can place page-cache data away from its NVMe device, schedule I/O threads without storage locality, and use rigid eviction policies that ignore workload access patterns.

**Mechanism / artifact:**

Workload-aware I/O coordination with storage-topology-aware page-cache placement, topology-aware I/O-thread scheduling and adaptive eviction-policy selection from observed access patterns; migration, monitoring, policy and affinity details are unspecified.

**Workload — the work tested:**

NUMA servers with distributed NVMe and diverse application access patterns; workload identities, read/write mix, working sets, concurrency, node/device count, cache state, request distribution and baseline policies are unspecified.

**Hardware and manufacturing assumptions:**

NUMA CPU/memory topology with PCIe-attached distributed NVMe, OS page cache and I/O scheduling path; kernel, CPU, PCIe topology, NVMe models, links, memory capacity, filesystem, direct-I/O/writeback and garbage-collection conditions are unspecified.

**Baseline — the comparison method:**

Topology-oblivious page-cache allocation

Conventional I/O-thread scheduling

Rigid page-cache eviction

Programmable manually tuned cache policies

Same nodes, devices, kernel, filesystem, workload mix, cache warmup, time budget, topology, monitoring and end-to-end measurement boundary are unspecified

**Reported measurements:**

The official description reports 1.41x geometric-mean throughput improvement with 3.5% runtime overhead; it supplies no per-workload throughput, p95/p99 latency, fairness, cross-node bytes, cache hit rate, migration count, policy cost or configuration result.

**Limits on the conclusion:**

Preserve cache coherence, write ordering, durability, page ownership, eviction, readahead and direct-I/O semantics. Measure per-workload throughput and tail latency, queueing, cross-node bytes, hit rate, device utilization, CPU overhead, migrations and regressions; geometric mean can conceal harmed tenants.

Include topology discovery, monitoring, policy inference, affinity changes, page migration, synchronization, cache warming, writeback and device garbage collection. Ablate placement, scheduling and adaptive eviction under matched node/device, workload and time conditions.

The 1.41x geometric-mean and 3.5% claims lack workloads, topology, devices, tails, fairness, policy cost, migration and baseline-tuning conditions. The evidence supports workload-aware NUMA/storage coordination, not demonstrated universal throughput improvement or bounded overhead across deployments.

**Source and location**

Evidence tier: Primary captured DAC official description plus existing chapter level conceptual discussion; no full paper extraction, per workload trace, topology configuration or independent review. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH651&sess=sess162)

DAC 2026 official description; existing chapter-level Laelaps discussion; captured Problem, Mechanism / artifact, Workload, Hardware, Baseline, Measurements and Limits fields; no manuscript pages or reproduced NUMA/storage trace.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** conventional topology-oblivious page-cache allocation

conventional I/O scheduling and rigid page-cache eviction

programmable cache policies requiring manual tuning

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH651&sess=sess162

**Hardware or process assumptions:** NUMA CPU/memory topology with distributed NVMe devices and an OS page-cache/I/O scheduling path; kernel, PCIe topology, CPU, and device details are unspecified.

**Limits:** The description omits workload mix, tail latency, fairness, topology scale, policy-selection overhead, and per-workload variance.

Geometric-mean gains can conceal regressions and depend on the selected storage and NUMA configuration.

Official description only; systems results require paper-level trace and baseline verification.

**Method or artifact:** Workload-aware I/O coordination framework aligning page-cache placement and I/O-thread scheduling with NVMe topology and selecting eviction policies from observed access patterns.

**Metrics:** 1.41x geometric-mean throughput improvement

3.5% runtime overhead

**Problem:** NUMA storage stacks ignore storage topology, cache locality, and workload-specific eviction, causing cross-node accesses and poor I/O coordination.

**Workload or benchmark:** NUMA servers with distributed NVMe storage and diverse application access patterns; workloads, devices, node counts, and baseline policies are unspecified.

</details>

<span id="paper-dac-2026-research1872"></span>

### SSD Reforge: Dynamic Parity Management to Extend SSD Lifetime Under Aging

DAC 2026 · Record: `dac-2026-research1872`

[Read the step-by-step explanation](#explanation-dac-2026-research1872)

**Updated source-backed reading card**

Reviewed 2026-09-08. Deepens the existing SSD Reforge treatment into a paper-level reading; separates dynamic parity, RBER-aware stripe grouping, RAS and SUPERL from reliability-model calibration, parity overhead, write amplification, latency, capacity and device-level endurance conclusions, preserves the FEMU, real-trace and up-to-40% user-TBW claims, and defines the evidence boundary.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Flash aging raises raw bit-error rate and limits SSD lifetime by TBW or program/erase cycles, while fixed protection does not adapt to heterogeneous block reliability.

**Mechanism / artifact:**

Dynamic intra-device parity strengthening with an RBER-based error-probability model, combinatorial parity-stripe grouping, Reliability-Aware Striping (RAS) and Stripe UPER Leveling (SUPERL) for subsequent writes; NAND, ECC, calibration and controller details are unspecified.

**Workload — the work tested:**

FEMU SSD simulation evaluated with real I/O traces against traditional protection mode at the lifetime limit; trace set, NAND geometry, aging states, ECC baseline, parity budget and lifetime accounting are unspecified.

**Hardware and manufacturing assumptions:**

Aging flash SSD with controller-managed intra-device parity, RBER estimation and dynamic striping; NAND generation, channels, pages/blocks, ECC/decoder, overprovisioning, retention, temperature, voltage, controller hardware and measurement instrumentation are unspecified.

**Baseline — the comparison method:**

Traditional fixed SSD protection mode

Static parity grouping

Conventional dynamic protection

Same NAND geometry, ECC, overprovisioning, workload, aging/error process, lifetime criterion, maintenance policy and end-to-end cost boundary are unspecified

**Reported measurements:**

The official description reports up to 40% average increase in user TBW at the lifetime limit in FEMU with real I/O traces; it supplies no RBER-model error, parity/capacity overhead, write amplification, latency, energy, tail-failure rate, trace variance or device-level validation.

**Limits on the conclusion:**

Calibrate the RBER/error-probability model against held-out device measurements across program/erase age, retention, temperature, voltage, read disturb and correlated-error conditions. A block ranking that works on one trace does not establish recoverability for tail or correlated failures.

Account for parity capacity, metadata, parity reads/writes, garbage collection, migration, write amplification, controller work, latency tails, bandwidth and energy. Include RAS construction, SUPERL updates, degraded blocks, failed stripes and recovery in the lifetime and performance boundary.

The FEMU, real-trace and up-to-40% user-TBW claim lacks NAND, ECC, calibration, parity-budget, trace, capacity, performance and energy conditions. The evidence supports adaptive parity and reliability-aware striping, not demonstrated device-level endurance improvement without tradeoffs.

**Source and location**

Evidence tier: Primary captured DAC official description plus existing chapter level ssd reforge discussion; no full paper extraction, device trace, error model calibration or endurance reproduction. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH1872&sess=sess162)

DAC 2026 official description; existing chapter-level SSD Reforge discussion; captured Problem, Mechanism / artifact, Workload, Hardware, Baseline, Measurements and Limits fields; no manuscript pages or reproduced FEMU/device campaign.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** traditional SSD protection mode

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH1872&sess=sess162

**Hardware or process assumptions:** Aging flash SSD with intra-device parity, RBER estimation, and controller-managed striping; NAND generation, channels, ECC, overprovisioning, and latency/energy costs are unspecified.

**Limits:** The description omits latency, write amplification, capacity overhead, energy, trace diversity, and error-model calibration.

Lifetime gains depend on aging distribution, parity budget, workload write pattern, and controller implementation.

Official description only; endurance and performance claims require trace- and device-level verification.

**Method or artifact:** Dynamic intra-device parity strengthening with RBER-aware stripe grouping and continued leveling under subsequent writes.

**Metrics:** Up to 40% average user-TBW increase at the lifetime limit

**Problem:** Flash aging raises raw bit-error rates and limits SSD lifetime by total bytes written or program/erase cycles.

**Workload or benchmark:** FEMU SSD simulation evaluated with real I/O traces against traditional protection mode; NAND geometry, trace set, ECC baseline, and lifetime model are unspecified.

</details>

<span id="paper-dac-2026-research1570"></span>

### NVLLM: A 3D NAND-Centric Architecture Enabling Edge on-Device LLM Inference

DAC 2026 · Record: `dac-2026-research1570`

[Read the step-by-step explanation](#explanation-dac-2026-research1570)

**Updated source-backed reading card**

Reviewed 2026-09-08. Deepens the NVLLM treatment into a paper-level reading; separates 3D-NAND-resident FFN execution, CMOS attention, ECC and KV-aware scheduling from NAND latency/parallelism, endurance, numerical fidelity, controller/peripheral cost and complete edge-serving measurements, while preserving the 16.7x, 1.1x–4.7x and 2.7% claims.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

On-device LLM decoding is memory-capacity and data-movement bound, while DRAM weight traversal and coarse SSD-like access granularity limit resource-constrained edge inference.

**Mechanism / artifact:**

3D NAND-centric inference architecture that offloads FFN computation into the flash array, executes attention on lightweight CMOS logic with external DRAM, decomposes GEMM/GEMV into dot-product primitives on out-of-order PE lanes over raw NAND reads with integrated ECC, and uses a KV-cache-aware scheduler; device, controller and numerical implementation details are unspecified.

**Workload — the work tested:**

OPT and LLaMA LLM inference up to 30B parameters with growing context and single-batch decoding; model precision/quantization, sequence lengths, token throughput, prompt mix, batch/concurrency, KV-cache size, decoding quality and baseline configurations are unspecified.

**Hardware and manufacturing assumptions:**

Wafer-to-wafer-stacked multi-plane 3D NAND with compute pipelines, ECC units, buffers, CMOS attention logic and external DRAM; NAND generation, page/read latency, channels/planes, raw-read interface, controller, process, thermal, endurance, voltage, frequency and area accounting are unspecified.

**Baseline — the comparison method:**

A800 out-of-core inference

SSD-like LLM accelerators

DRAM-centric edge inference

Same OPT/LLaMA models, precision, quality target, context, KV-cache policy, storage hierarchy, controller, preprocessing, thermal/power and complete latency/energy boundary are unspecified

**Reported measurements:**

The official description reports 16.7x speedup over A800 out-of-core inference, 1.1x–4.7x improvement over SSD-like designs and 2.7% CMOS area overhead for models up to 30B parameters; it supplies no absolute latency/throughput, energy, accuracy, capacity, endurance, NAND access conditions, controller/peripheral overhead or per-model distribution.

**Limits on the conclusion:**

Raw NAND reads and in-array dot products must preserve the model's numerical semantics. Validate GEMM/GEMV accumulation, precision/quantization, ECC and error behavior against a trusted digital reference across layers, sequence lengths, KV-cache growth and edge cases; report perplexity, task quality, output agreement and unsupported operations.

NAND access is not free storage bandwidth. Measure page/read latency, channel and plane parallelism, queueing, raw-to-ECC data path, PE utilization, DRAM/KV traffic, controller scheduling, buffers, write/program activity, thermal limits and p50/p95/p99 token latency. Account for attention, FFN, transfers, decode, initialization and idle power in the same boundary.

The 16.7x, 1.1x–4.7x and 2.7% claims lack model precision, absolute results, energy, NAND/process conditions, capacity, endurance, controller/peripheral costs and quality validation. The evidence supports a 3D-NAND-centric LLM architecture direction, not demonstrated durable, quality-preserving end-to-end edge inference.

**Source and location**

Evidence tier: Primary captured official DAC description plus existing authored chapter level explanation; no full paper extraction, device level nand trace, endurance study, numerical quality validation or independent edge serving reproduction. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH1570&sess=sess116)

DAC 2026 official description; existing chapter-level storage-and-data-movement NVLLM discussion; captured Problem, Mechanism / artifact, Workload, Hardware, Baseline, Measurements and Limits fields; no manuscript pages or reproduced NAND/LLM evaluation.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** DRAM-centric edge inference

flash-offloaded LLM inference

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH1570&sess=sess116

**Hardware or process assumptions:** 3D NAND-centric memory/storage hierarchy with compute or near-storage support; endurance, latency, channel parallelism, and technology assumptions are unspecified.

**Limits:** The description omits latency, energy, capacity, endurance, accuracy, and hardware implementation details.

NAND latency and write endurance may constrain practical deployment.

Official description only; storage-centric claims require device-level evidence.

**Method or artifact:** Architecture using 3D NAND resources as a central substrate for edge LLM storage and inference.

**Metrics:** On-device feasibility and efficiency are claimed qualitatively

**Problem:** On-device LLM deployment is limited by model capacity, memory bandwidth, and energy constraints.

**Workload or benchmark:** On-device LLM inference; model quantization, NAND organization, controller, and baselines are unspecified.

</details>

<span id="paper-dac-2026-research1291"></span>

### NASiC: 3D NAND-Based CAM-Selected Multibit CIM Architecture for Efficient On-Device Mixture-of-Experts LLM Inference

DAC 2026 · Record: `dac-2026-research1291`

[Read the step-by-step explanation](#explanation-dac-2026-research1291)

**Updated source-backed reading card**

Reviewed 2026-09-09. Deepens the NASiC treatment into a paper-level reading; separates 3D-NAND CAM expert selection and multibit CIM from MoE routing quality, analog/digital numerical fidelity, peripheral movement, endurance and complete on-device system efficiency, while preserving the V-ASIC architecture claim and its official-description evidence boundary.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Mixture-of-Experts LLMs reduce active computation per token by selecting a sparse subset of experts, but storing all expert parameters creates a large memory-capacity and data-movement burden for on-device inference.

**Mechanism / artifact:**

NASiC: algorithm--hardware co-optimization using a 3D NAND-based CAM-selected multibit computing-in-memory architecture, with V-ASIC as the proposed architecture; expert-selection encoding, CAM match operation, multibit sensing/ADC, CIM arithmetic, precision, controller and dataflow are unspecified.

**Workload — the work tested:**

On-device MoE LLM inference with sparse expert activation; models, parameter size, number of experts, top-k routing, sequence length, batch/concurrency, token quality, precision, expert placement and baseline software/runtime are unspecified.

**Hardware and manufacturing assumptions:**

3D NAND array used for dense storage, CAM-based expert selection and multibit CIM with CMOS peripherals; NAND generation/process, cell levels, array geometry, ADC/DAC, sensing, variation, retention, endurance, ECC, controller, buffers, host interface, thermal conditions and power boundary are unspecified.

**Baseline — the comparison method:**

DRAM/GPU MoE inference

NAND storage with digital compute

Conventional on-device MoE accelerator or expert-cache system

Same MoE model, top-k routing, precision, quality target, storage capacity, expert placement, compiler/runtime, peripheral accounting, device conditions and end-to-end latency/energy boundary are unspecified

**Reported measurements:**

The official description claims improved throughput and high area- and energy-efficiency for the V-ASIC architecture, but reports no throughput, token latency, energy per token, model quality, area, density, capacity, ADC/peripheral overhead, endurance, variation tolerance or device/system measurement.

**Limits on the conclusion:**

CAM-selected sparse computation must preserve MoE routing semantics. Compare selected experts, top-k ties, load balance, dropped tokens, capacity overflow, dispatch/combination and expert outputs with a trusted digital reference across sequence length, batch and routing distributions; a memory-array match is not automatically correct model execution.

Multibit NAND storage and CIM arithmetic require numerical and reliability validation. State cell-level encoding, read/program conditions, ADC quantization, accumulation, noise, retention, read disturb, process variation, ECC/calibration and write endurance; report layer/output error, perplexity or task quality, error tails, temperature and aging, including CMOS peripheral, buffer and controller costs.

The source claims V-ASIC throughput and area/energy efficiency but provides no numerical result, MoE workload, precision, device/process, peripheral overhead, endurance, model-quality or end-to-end boundary. The evidence supports a 3D-NAND CAM-selected multibit CIM direction for dense expert storage, not demonstrated quality-preserving on-device MoE efficiency or durable device-to-system benefit.

**Source and location**

Evidence tier: Primary captured official DAC description plus existing authored storage/data movement discussion; no full paper extraction, device variability/endurance matrix, model quality trace or independent end to end validation. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH1291&sess=sess123)

DAC 2026 official description; existing storage-and-data-movement chapter discussion; captured Problem, Mechanism / artifact, Workload, Hardware, Baseline, Measurements and Limits fields; no manuscript pages, reproduced MoE inference, NAND device data or system measurement.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** DRAM/GPU MoE inference

NAND storage with digital compute

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH1291

**Hardware or process assumptions:** 3D NAND CIM with CAM-based expert selection; endurance, ADC, latency, and process assumptions are unspecified.

**Limits:** No throughput, energy, accuracy, endurance, density, or peripheral overhead results are reported.

NAND variability and write endurance may constrain deployment.

Official description only; device-to-system validation is required.

**Method or artifact:** 3D NAND-based CAM-selected multibit computing-in-memory architecture.

**Metrics:** On-device MoE efficiency is claimed qualitatively

**Problem:** On-device MoE inference is constrained by model capacity, expert selection, and memory movement.

**Workload or benchmark:** On-device MoE LLM inference; NAND technology, models, precision, and baselines are unspecified.

</details>

<span id="paper-dac-2026-research2074"></span>

### Z-Paraswap: Co-Optimizing ZNS Parallelism and Swapping for Heterogeneous Graph Neural Network

DAC 2026 · Record: `dac-2026-research2074`

[Read the step-by-step explanation](#explanation-dac-2026-research2074)

**Updated source-backed reading card**

Reviewed 2026-09-09. Deepens the Z-Paraswap treatment into a paper-level reading; separates graph-access correlation, ZNS chip placement and swapping from GNN semantic correctness, page lifetime, queueing, device parallelism and end-to-end execution accounting, while preserving the reported 34% average and 44% tail swapping-latency reductions.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Heterogeneous GNNs can exceed main-memory capacity and generate irregular, non-sequential page accesses; a Linux ZNS swapping mechanism can underuse SSD-chip parallelism and create congestion and long-tail latency when correlated graph data compete for storage service.

**Mechanism / artifact:**

Z-ParaSwap: ZNS-based parallelism-aware swapping that identifies access correlations in graph data and distributes correlated pages across different SSD chips to increase parallelism and reduce I/O contention; correlation window, page-placement policy, zone allocation, migration/write protocol, queue model, graph execution coordination and consistency semantics are unspecified.

**Workload — the work tested:**

Heterogeneous Graph Neural Network applications with memory pressure and ZNS-backed swapping; graph types, node/edge/features, graph scale, sampling/traversal pattern, working-set size, page size, access traces, batch/concurrency, memory capacity, swap rate, storage queue depth and model accuracy conditions are unspecified.

**Hardware and manufacturing assumptions:**

NVMe Zoned Namespace SSDs used as swap storage with CPU or accelerator HetGNN execution; SSD model, channels/chips, zones, zone size, NAND generation, controller/firmware, PCIe link, bandwidth, latency, host memory, OS/kernel, queue depth, garbage collection, wear/endurance and instrumentation are unspecified.

**Baseline — the comparison method:**

Conventional paging

ZNS-oblivious GNN execution

Linux-based ZNS swapping mechanism

Same graph/model, sampling, memory capacity, page/zone layout, SSD, queue depth, CPU/accelerator, kernel, background activity, accuracy target and end-to-end timing boundary are unspecified

**Reported measurements:**

The official description reports 34% lower average swapping latency and 44% lower tail swapping latency, with improved overall HetGNN execution efficiency on ZNS-based systems; it reports no absolute I/O latency, percentile definition, throughput, page-fault rate, I/O volume, memory reduction, GNN accuracy, end-to-end execution time, SSD utilization, write amplification or endurance result.

**Limits on the conclusion:**

Access correlation is workload- and phase-dependent. Define the observation window, graph traversal/sampling semantics, page-to-chip placement, zone constraints and update/migration consistency; evaluate unseen graphs, sampling policies, batch sizes and phase changes. A placement that reduces one trace's contention can create hotspots or destroy locality on another.

ZNS parallelism does not eliminate NAND, channel, controller, PCIe or host-memory bottlenecks. Report queue depth, chip/channel utilization, read/write mix, page faults, bytes moved, queueing, garbage-collection interference, write amplification, migration cost and p50/p95/p99/p99.9 latency. Include the placement and correlation-computation overhead in the end-to-end result.

The official description reports 34% lower average and 44% lower tail swapping latency but omits absolute conditions, tail definition, graph/model details, storage configuration, GNN accuracy, end-to-end runtime, background activity, write amplification and endurance. The evidence supports access-aware ZNS swapping for HetGNNs, not demonstrated general GNN speedup, semantic preservation under all paging behavior or durable SSD efficiency.

**Source and location**

Evidence tier: Primary captured official DAC description plus existing authored storage discussion; no full paper extraction, reproduced trace diverse evaluation, zns device characterization or independent end to end hetgnn validation. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH2074&sess=sess146)

DAC 2026 official description; existing storage-and-data-movement chapter discussion; captured Problem, Mechanism / artifact, Workload, Hardware, Baseline, Measurements and Limits fields; no manuscript pages, access trace, SSD configuration matrix, accuracy check or endurance measurement.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** conventional paging

ZNS-oblivious GNN execution

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH2074

**Hardware or process assumptions:** NVMe/ZNS storage hierarchy with accelerator or CPU GNN execution; bandwidth and queue assumptions are unspecified.

**Limits:** No I/O latency, throughput, memory reduction, GNN accuracy, or endurance results are reported.

Swap policies may be sensitive to graph access locality.

Official description only; trace-diverse storage evaluation is required.

**Method or artifact:** ZNS parallelism and swap co-optimization for heterogeneous GNN execution.

**Metrics:** Storage-aware GNN efficiency is claimed qualitatively

**Problem:** Heterogeneous GNNs can exceed memory capacity and require storage parallelism and swapping without destroying locality.

**Workload or benchmark:** Heterogeneous graph workloads and ZNS storage; device, graph scale, and baselines are unspecified.

</details>

<span id="paper-dac-2026-research444"></span>

### Gwrite: Offloading Replication in Disaggregated Memory Systems

DAC 2026 · Record: `dac-2026-research444`

[Read the step-by-step explanation](#explanation-dac-2026-research444)

**Updated source-backed reading card**

Reviewed 2026-09-09. Deepens the GWrite treatment into a paper-level reading; separates memory-side RNIC replication fan-out and GWrap protocol behavior from RDMA ordering, consistency, failure recovery, tail latency, NIC capacity and deployment scale, while preserving the 2.18x and 46.7%-to-19.7% claims.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Disaggregated memory replicates writes across memory nodes for consistency and durability, but synchronous host-managed fan-out can saturate the compute node's RDMA NIC and create a throughput bottleneck as replica count grows.

**Mechanism / artifact:**

GWrite, a hardware-oriented RDMA primitive, and GWrap, a co-designed replication protocol that offload replication fan-out to memory-side RNICs while preserving one-sided RDMA semantics; packet format, ordering, completion, acknowledgment, retry, ownership, memory-side RNIC capacity and failure behavior are unspecified.

**Workload — the work tested:**

Write-intensive disaggregated deployments including a distributed transaction system and a replicated hash table; transaction mix, object/value size, replica count, consistency/durability target, concurrency, fabric topology, workload scale, failure injection and software stack are unspecified.

**Hardware and manufacturing assumptions:**

Disaggregated memory nodes with memory-side RNICs and compute-node RDMA NICs connected by an RDMA fabric; RNIC model, memory controller, link rate, topology, transport, queue depth, CPU, host memory, clocks, power, firmware, FPGA/ASIC implementation and deployment scale are unspecified.

**Baseline — the comparison method:**

Host-managed synchronous replication

Unreplicated disaggregated memory

Same RDMA transport, replica count, object size, transaction workload, consistency/durability guarantee, NIC/link configuration, software stack, failure policy and end-to-end measurement boundary are unspecified

**Reported measurements:**

The official description reports that a software prototype emulating GWrite on commodity RNICs achieves up to 2.18x higher throughput in a distributed transaction system and reduces replication-induced throughput degradation in a replicated hash table from 46.7% to 19.7%; it does not report absolute throughput, latency/tails, CPU/RNIC utilization, bandwidth, consistency checks, failure recovery, energy, scale or hardware implementation results.

**Limits on the conclusion:**

Moving fan-out to memory-side RNICs must preserve one-sided RDMA semantics and the declared consistency/durability guarantee. Define write visibility, replica ordering, acknowledgments, completion, duplicate/retry handling, partial failure, timeout, crash recovery, fencing and interaction with reads or atomics. Compare final values and histories with a trusted host-managed reference under concurrent writes, reordering, packet loss and node/NIC failures; lower host-NIC traffic is not evidence of serializability or durability.

The outbound capacity is relocated, not made free. Measure compute- and memory-side RNIC queue occupancy, packet/byte counts, link utilization, memory-controller contention, CPU work, acknowledgments, retransmissions, backpressure, batching, p50/p95/p99 write and transaction latency, throughput and energy. Include protocol setup, metadata, recovery, background replication and the critical path; a throughput gain can hide worse tail latency or a hotspot at memory-side RNICs.

Evaluate replica count, node count, object/value size, read/write mix, transaction conflicts, concurrency, topology, link contention and workload phases. Compare synchronous host fan-out, GWrite/GWrap and any batching or asynchronous replication policy at equal consistency, durability, hardware, transport, software tuning and failure budget. Report per-workload results and the point at which memory-side outbound capacity saturates.

The captured record reports a commodity-RNIC software emulation rather than a demonstrated memory-side RNIC implementation, and does not expose consistency/failure results, latency, bandwidth, energy, topology, scale or absolute values. The evidence supports memory-side replication offload, not demonstrated durable, low-tail-latency distributed-memory scaling or hardware-level RDMA benefit.

**Source and location**

Evidence tier: Primary captured official DAC description plus existing authored storage/disaggregated memory discussion; no full paper extraction, reproduced rdma protocol, failure validation or hardware deployment. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH444&sess=sess169)

DAC 2026 official description; existing storage-and-data-movement chapter framing; captured Problem, Mechanism / artifact, Workload, Hardware, Baseline, Measurements and Limits fields; no manuscript pages, consistency history, fault-injection trace or memory-side RNIC implementation.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** host-managed replication

unreplicated disaggregated memory

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH444

**Hardware or process assumptions:** Disaggregated memory fabric with replication-capable endpoints; protocol and failure assumptions are unspecified.

**Limits:** No latency, bandwidth, consistency, failure recovery, energy, or scale results are reported.

Offload can complicate correctness and recovery ordering.

Official description only; fault-injection validation is required.

**Method or artifact:** Replication offload mechanism for disaggregated memory.

**Metrics:** Replication efficiency and system performance are claimed qualitatively

**Problem:** Replication in disaggregated memory consumes host CPU, network bandwidth, and tail latency.

**Workload or benchmark:** Distributed memory workloads; consistency model, fabric, failure mode, and baselines are unspecified.

</details>

<span id="paper-dac-2026-research297"></span>

### Etherssd: An In-Storage Ethereum Analytics Platform with Minimized I/O and Authentication Overhead

DAC 2026 · Record: `dac-2026-research297`

[Read the step-by-step explanation](#explanation-dac-2026-research297)

**Updated source-backed reading card**

Reviewed 2026-09-09. Deepens the EtherSSD treatment into a paper-level reading; separates CSD-side flattened authenticated-page access and cryptographic authentication offload from Ethereum query semantics, Merkle-proof integrity, snapshot/update consistency, trust boundaries, wear/latency and complete analytics cost.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Ethereum analytics must retrieve large ledger structures and validate auxiliary proofs such as Merkle proofs; host-side page movement and cryptographic verification can dominate authenticated query latency and CPU/I/O cost.

**Mechanism / artifact:**

EtherSSD, an in-storage Ethereum analytics platform using computational storage devices to bridge host/CSD semantics, flatten authenticated data queries into highly concurrent in-CSD page accesses, reduce host-side I/O operations and offload cryptographic authentication to an authentication engine; query language/operators, proof format, root/version handling, CSD programming model, trust boundary, update protocol, concurrency and failure behavior are unspecified.

**Workload — the work tested:**

Real-world Ethereum authenticated analytics workloads and ledger queries; query types, chain snapshot/block range, dataset size, transaction/log/state structures, proof depth, cache state, update/concurrency pattern, CSD configuration and host/storage baselines are unspecified.

**Hardware and manufacturing assumptions:**

Computational storage devices with in-storage page processing and cryptographic authentication attached to a host; flash/media/controller, CSD compute, memory, interface, parallelism, cryptographic engine, key/root-of-trust storage, firmware, power, wear, fault model and threat assumptions are unspecified.

**Baseline — the comparison method:**

Host-side Ethereum analytics

Unaccelerated authenticated storage

CSD analytics without flattened page access

Host CPU authentication without the in-storage engine

Same Ethereum snapshot, query, proof/security policy, consistency point, storage media, interface, cache state, concurrency, software and end-to-end latency/energy boundary are unspecified

**Reported measurements:**

The official description reports reduced authenticated query execution time, particularly I/O and authentication overhead, under real-world workloads; it does not report absolute latency, throughput, host I/O bytes, CPU/authentication cost, proof-verification throughput, energy, dataset/query conditions, integrity outcomes, update consistency or CSD scale.

**Limits on the conclusion:**

Flattening a Merkle-authenticated query must preserve the query's semantics and proof relation to the committed root. Define the proof type, hash function, root/version, page ordering, sibling paths, duplicate/omitted records, range/aggregate semantics and result completeness; compare returned records and proof acceptance with a trusted host reference under malformed, stale, reordered, replayed and adversarial pages. Fewer host requests do not establish authenticated correctness.

The CSD creates a new trust boundary. State which code, pages, metadata, keys and roots are trusted, how authentication-engine results are protected, how firmware compromise or DMA is handled, and how errors, retries, power loss and device replacement affect evidence. Test snapshot/update races, reorg or fork handling if relevant, concurrent queries, partial writes, corrupted pages and stale roots; report rejected invalid proofs and false acceptance, not just successful query time.

Measure page reads, bytes transferred at host/CSD/media levels, proof hashes, authentication-engine utilization, CPU cycles, queueing, parallelism, cache hits, flash reads, controller work, metadata, tail latency, energy, write amplification and wear. Include proof construction, query flattening, scheduling, result materialization, initialization, updates and recovery in the end-to-end boundary. An authentication speedup can be offset by CSD contention or media access.

The official description says EtherSSD reduces authenticated Ethereum-query execution time and I/O/authentication overhead on real-world workloads, but omits query/proof conditions, absolute results, integrity validation, trust/update assumptions, hardware configuration, wear, energy and baseline accounting. The evidence supports authenticated in-storage Ethereum analytics, not demonstrated complete blockchain-query correctness, adversarial storage security or portable end-to-end deployment efficiency.

**Source and location**

Evidence tier: Primary captured official DAC description plus existing authored in storage/query discussion; no full paper extraction, reproduced authenticated query, trust boundary analysis or independent csd validation. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH297&sess=sess161)

DAC 2026 official description; existing storage-and-data-movement chapter framing; captured Problem, Mechanism / artifact, Workload, Hardware, Baseline, Measurements and Limits fields; no manuscript pages, proof trace, adversarial validation or CSD benchmark matrix.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** host-side Ethereum analytics

unaccelerated authenticated storage

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH297

**Hardware or process assumptions:** Computational storage device with secure data path; flash/controller and threat assumptions are unspecified.

**Limits:** No query latency, throughput, energy, authentication cost, or integrity results are reported.

In-storage trust boundaries and update consistency are unspecified.

Official description only; adversarial storage validation is required.

**Method or artifact:** In-storage Ethereum analytics platform with authentication-aware data processing.

**Metrics:** I/O and authentication efficiency are claimed qualitatively

**Problem:** Blockchain analytics is storage- and I/O-heavy and must authenticate data accesses.

**Workload or benchmark:** Ethereum ledger queries; storage device, datasets, authentication scheme, and baselines are unspecified.

</details>

<span id="paper-dac-2026-research2773"></span>

### Flashhd: A Flash-Based In-Storage Hyperdimensional Computing Framework for Hierarchical Sequence Matching

DAC 2026 · Record: `dac-2026-research2773`

[Read the step-by-step explanation](#explanation-dac-2026-research2773)

**Updated source-backed reading card**

Reviewed 2026-09-09. Deepens the FlashHD treatment into a paper-level reading; separates 3D-NAND in-storage exact matching, hierarchical HDC filtering and hierarchy-aware hyperparameter search from exact-recall validation, flash sensing/variation, write/endurance cost, host/device data movement and end-to-end sequence-query performance, while preserving the qualitative superiority claim without inventing results.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Exact DNA-sequence matching scans large corpora and can become dominated by page faults and host data movement when the working set exceeds memory; filtering near flash is attractive only if it preserves exact matches and does not shift the bottleneck into sensing or device management.

**Mechanism / artifact:**

FlashHD is described as a 3D-NAND in-storage sequence-matching framework using hierarchical hyperdimensional computing to filter dissimilar sequences across stages while preserving full recall, plus hierarchy-aware hyperdimensional architecture search to tune HDC hyperparameters for latency and energy; encoding, dimension, similarity/threshold operation, NAND sensing, controller integration, hierarchy construction and search budget are unspecified.

**Workload — the work tested:**

Exact DNA-sequence matching over large stored databases with hierarchical representations; sequence length, corpus size, query count/distribution, match rate, hierarchy/fanout, HDC dimension/precision, recall definition, storage working set, update pattern and competing systems are unspecified.

**Hardware and manufacturing assumptions:**

3D-NAND flash with in-storage compute and controller/sensing support; NAND generation, array geometry, channels/planes, raw-read path, peripheral compute, ADC/sense margins, ECC, controller, host link, memory, temperature, retention, read disturb, program/erase activity and endurance model are unspecified.

**Baseline — the comparison method:**

Host-side exact sequence matching

Digital in-storage processing

Same DNA corpus, query workload, exactness/recall criterion, sequence encoding, NAND capacity, host memory, controller, parallelism, software stack and end-to-end measurement boundary are unspecified

**Reported measurements:**

The official description claims that FlashHD significantly outperforms state-of-the-art systems and states that hierarchical filtering preserves full recall, but reports no recall/precision result, latency, throughput, energy, I/O bytes, density, area, endurance, query count or per-workload comparison.

**Limits on the conclusion:**

HDC filtering can discard a true match if encoding collisions, finite dimension, thresholding, quantization or NAND sensing errors alter similarity. Define exact matching semantics, sequence encoding, hierarchy, candidate-recall stage, tie/threshold behavior and compare every returned match with a trusted CPU reference; report false negatives, false positives and recall by sequence length, mutation/edit distance and match rarity. 'Full recall' requires a denominator and independent exact check.

Moving matching into 3D NAND couples computation to raw-read latency, sensing variation, ECC, controller scheduling, channels/planes, thermal state and data movement. Include encoding, flash read, HDC operations, candidate transfer, verification, host result materialization, setup and calibration in latency/energy; report bytes read, parallelism, queueing and p50/p95/p99 behavior rather than only nominal array throughput.

The hierarchy-aware architecture search must expose its objective, HDC hyperparameters, training/search evaluations, fidelity model, stopping rule and cost. Test unseen sequence distributions, database sizes, match rates, NAND conditions and changing corpora; measure re-encoding, writes, garbage collection, read disturb, retention and program/erase endurance if data or metadata are updated. The evidence supports an in-storage HDC sequence-matching direction, not demonstrated exact-recall, durable flash efficiency or quantitative end-to-end superiority.

**Source and location**

Evidence tier: Primary captured official DAC description plus existing authored in storage compute discussion; no full paper extraction, reproduced exact match campaign, device level sensing validation or endurance study. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH2773)

DAC 2026 official description; existing storage-and-data-movement chapter framing; captured Problem, Mechanism / artifact, Workload, Hardware, Baseline, Measurements and Limits fields; no manuscript pages, sequence-query table, NAND condition matrix or reproduced recall/energy/endurance evaluation.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** host-side sequence matching

digital in-storage processing

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH2773

**Hardware or process assumptions:** Flash storage with in-storage compute and endurance constraints; controller and sensing assumptions are unspecified.

**Limits:** No accuracy, latency, energy, endurance, density, or query results are reported.

Flash variability and writes may constrain updates.

Official description only; device-level validation is required.

**Method or artifact:** Flash-based in-storage hyperdimensional computing framework.

**Metrics:** I/O and matching efficiency are claimed qualitatively

**Problem:** Sequence matching is data-movement-heavy, especially for large stored corpora and hierarchical representations.

**Workload or benchmark:** Hierarchical sequence matching; flash technology, data sizes, and baselines are unspecified.

</details>

<span id="paper-dac-2026-research2806"></span>

### Lhgstore: An In-Memory Learned Graph Storage for Fast Updates and Analytics

DAC 2026 · Record: `dac-2026-research2806`

[Read the step-by-step explanation](#explanation-dac-2026-research2806)

**Updated source-backed reading card**

Reviewed 2026-09-09. Deepens the LHGstore treatment into a paper-level reading; separates degree-aware two-level graph layout, vertex/edge decoupling, low-degree arrays and high-degree learned indexes from graph-update correctness, traversal semantics, memory overhead, concurrency, distribution shift and end-to-end analytics conditions, while preserving the 5.9–28.2x claim with its missing measurement boundary.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Dynamic in-memory graphs must absorb frequent edge/vertex updates while retaining locality for low-latency traversal and analytics; skewed degree distributions make one representation inefficient for both low- and high-degree vertices.

**Mechanism / artifact:**

LHGstore is described as a degree-aware Learned Hierarchical Graph store with a two-level hierarchy that decouples vertex and edge access, uses lightweight arrays for low-degree vertices to preserve traversal locality, and applies learned indexes to high-degree vertices to improve update throughput; degree thresholds, index training, correction/rebuild, concurrency, memory layout and recovery are unspecified.

**Workload — the work tested:**

Real-world dynamic graphs with frequent updates and analytics, including skewed degree distributions; graph identities, vertex/edge counts, degree/timestamp distributions, update mix and burstiness, query/traversal algorithms, concurrency, memory capacity, warm-up, graph mutability and scale are unspecified.

**Hardware and manufacturing assumptions:**

In-memory graph storage on a modern multi-core CPU; CPU model, cores, cache/NUMA topology, DRAM capacity/bandwidth, allocator, thread/runtime, synchronization, persistence, failure recovery and consistency model are unspecified.

**Baseline — the comparison method:**

Hash/table-based graph store

Conventional in-memory graph database

Same graph representation/semantics, memory budget, CPU/NUMA placement, update/query workload, concurrency, thread count, batching, warm-up, persistence and end-to-end timing boundary are unspecified

**Reported measurements:**

The official description reports 5.9–28.2x higher throughput and significantly faster analytics than state-of-the-art in-memory graph storage systems, but does not report absolute update/query throughput or latency, memory overhead, graph scale, consistency cost, tail behavior, per-workload results or baseline tuning.

**Limits on the conclusion:**

A learned index predicts locations or ordering; it does not replace graph semantics. Define vertex/edge identity, insertion/deletion/update visibility, duplicate/self-loop handling, adjacency ordering, traversal consistency and crash/recovery behavior. Validate analytics against a trusted graph reference during concurrent updates, including races, deletes, degree changes, stale predictions and index rebuilds; higher update throughput is not useful if a traversal sees an invalid graph.

The degree-aware split trades locality and memory layout against update and lookup cost. Report degree thresholds, array/index bytes, model metadata, slack, fragmentation, cache/NUMA misses, pointer chasing, rebuild/training time, synchronization, allocator and migration cost. Measure p50/p95/p99 update and query latency, throughput, scan/traversal work and memory per vertex/edge under read-heavy, update-heavy and mixed workloads rather than only a geometric mean.

Learned indexes can degrade when degree or neighbor-key distributions change. Hold out graph snapshots, unseen graphs and temporal phases; test skew shifts, bursts, insertions/deletions, adversarial keys and memory pressure. Compare hash/table and conventional stores with equal CPU threads, memory, consistency, batching and query semantics. The evidence supports degree-aware learned in-memory graph storage, not demonstrated portable 5.9–28.2x end-to-end benefit, stable analytics under dynamic shift or a persistence guarantee.

**Source and location**

Evidence tier: Primary captured official DAC description plus existing authored graph storage discussion; no full paper extraction, reproduced dynamic update campaign, memory accounting or independent analytics correctness validation. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH2806)

DAC 2026 official description; existing storage-and-data-movement chapter framing; captured Problem, Mechanism / artifact, Workload, Hardware, Baseline, Measurements and Limits fields; no manuscript pages, graph/workload table, consistency trace or reproduced multi-core benchmark.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** hash/table graph store

conventional in-memory graph database

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH2806

**Hardware or process assumptions:** In-memory graph storage system; consistency, persistence, and memory technology assumptions are unspecified.

**Limits:** No update latency, query throughput, memory, consistency, or graph-scale results are reported.

Learned indexes may degrade under distribution shift.

Official description only; dynamic-workload validation is required.

**Method or artifact:** Learned in-memory graph storage structure.

**Metrics:** Update and analytics efficiency are claimed qualitatively

**Problem:** Graph stores need fast updates and analytics while fitting large, irregular structures in memory.

**Workload or benchmark:** Dynamic graph updates and analytics; graph sizes, memory, and baselines are unspecified.

</details>

<span id="paper-dac-2026-research442"></span>

### VALVE: Accelerating Visible Version Searching in HTAP Systems via In-Storage Computing

DAC 2026 · Record: `dac-2026-research442`

[Read the step-by-step explanation](#explanation-dac-2026-research442)

**Updated source-backed reading card**

Reviewed 2026-09-09. Deepens the VALVE treatment into a paper-level reading; separates CSD-offloaded MVCC visible-version searching and frugal skip-list traversal from snapshot/visibility correctness, host-CSD concurrency, transaction isolation, failure recovery and complete HTAP latency/throughput cost, while preserving the qualitative end-to-end scan and analytical-throughput claims.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

HTAP systems maintain multiple versions under MVCC; frequent updates lengthen version chains, so analytical queries spend more I/O and CPU work finding the version visible to their snapshot while transactions continue concurrently.

**Mechanism / artifact:**

VALVE offloads visible-version searching from the host to a computational-storage device and first addresses consistency under host-CSD concurrency; a frugal skip list accelerates traversal of version chains. Snapshot visibility rule, metadata format, skip-list maintenance, host/device ownership, synchronization, transaction protocol, persistence and recovery are unspecified.

**Workload — the work tested:**

HTAP transactional updates and analytical scans over MVCC version chains; database engine, workload mix, transaction/update rate, chain length, snapshot age, query predicates, data size, concurrency, cache state, CSD configuration and baselines are unspecified.

**Hardware and manufacturing assumptions:**

Computational-storage device processing transaction/version metadata with host-side HTAP database; CSD processor/memory, storage medium, host link, controller, persistence, cache, queueing, firmware, power-loss and failure assumptions are unspecified.

**Baseline — the comparison method:**

Host-side visible-version search

Generic in-storage query processing

Same MVCC isolation/visibility contract, transaction and analytical workload, version-chain state, database engine, CSD/host hardware, cache, concurrency, recovery policy and end-to-end timing boundary are unspecified

**Reported measurements:**

The official description claims reduced end-to-end analytical scan latency and improved analytical throughput using CSD-offloaded visible-version search and a frugal skip list, but reports no absolute latency, throughput, I/O/CPU reduction, consistency result, transaction impact, energy, endurance, failure recovery or per-workload condition.

**Limits on the conclusion:**

Visible-version search is a correctness operation, not merely a filter. Define transaction timestamps, snapshot/commit visibility, deletes, updates, version-chain ordering, phantom/serializability or snapshot-isolation contract and result completeness. Compare host and CSD results under concurrent commits, aborts, retries, stale metadata, long chains and snapshot changes; lower scan latency is invalid if a query reads an uncommitted, too-new or missing version.

The frugal skip list trades metadata, maintenance and pointer traversal for fewer version comparisons. Specify its level construction, key/order, update/delete protocol, stale-index fallback, memory placement, synchronization and rebuild cost. Measure host/CSD bytes, metadata traffic, random reads, queueing, CPU/CSD utilization, lock/wait time, version-chain length, p50/p95/p99 analytical latency and transaction latency under read-heavy, update-heavy and mixed loads.

CSD concurrency creates a distributed state boundary. Test power loss, device reset, host failure, partial metadata writes, retries, duplicate requests, firmware restart and recovery, and state which data are durable. Compare host-side and generic in-storage processing with equal isolation, cache, hardware, workload, warm-up, batching and recovery cost. The evidence supports CSD-assisted MVCC visible-version traversal, not demonstrated serializable/consistent HTAP correctness, failure-safe persistence or portable end-to-end throughput improvement.

**Source and location**

Evidence tier: Primary captured official DAC description plus existing authored in storage/query discussion; no full paper extraction, independent concurrency validation, failure recovery study or complete htap measurement matrix. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH442)

DAC 2026 official description; existing storage-and-data-movement chapter framing; captured Problem, Mechanism / artifact, Workload, Hardware, Baseline, Measurements and Limits fields; no manuscript pages, MVCC history trace, consistency test or reproduced CSD scan benchmark.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** host-side version search

generic in-storage query processing

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH442

**Hardware or process assumptions:** Computational storage with transaction metadata processing; persistence and failure assumptions are unspecified.

**Limits:** No latency, throughput, consistency, energy, endurance, or failure results are reported.

In-storage query state may complicate transactional correctness.

Official description only; concurrency and fault validation are required.

**Method or artifact:** In-storage visible-version search accelerator.

**Metrics:** HTAP query efficiency is claimed qualitatively

**Problem:** HTAP version visibility queries incur I/O and transaction-history processing overhead.

**Workload or benchmark:** HTAP transaction/version queries; storage device, consistency model, and baselines are unspecified.

</details>

<span id="paper-dac-2026-research609"></span>

### Knowledge-Driven Hybrid SSD Management Enhanced by Fine-Tuned LLMs

DAC 2026 · Record: `dac-2026-research609`

[Read the step-by-step explanation](#explanation-dac-2026-research609)

**Updated source-backed reading card**

Reviewed 2026-09-09. Deepens the LLM-hybridSSD treatment into a paper-level reading; separates knowledge-guided parameter tuning, LLM-based adaptive configuration and RL fine-tuning of lightweight local models from SSD-policy safety, SLC/QLC conversion and migration cost, write-amplification/endurance accounting, workload transfer and controller deployment, while preserving the 58.92% throughput and 28.56% WA claims.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

A hybrid SSD combines flash modes such as SLC and QLC and may convert or migrate data between them, creating a larger management space involving placement, garbage collection, conversion and endurance; static policies can be poor when workload phases change.

**Mechanism / artifact:**

LLM-hybridSSD formulates hybrid-SSD management as parameter tuning, uses an LLM-based tuner for adaptive configuration and applies reinforcement-learning fine-tuning to align lightweight local models with domain-specific SSD knowledge; parameter/state representation, actions, safety constraints, training data, reward, deployment path, update cadence, fallback and controller integration are unspecified.

**Workload — the work tested:**

Hybrid SLC/QLC SSD management under different real-world workloads with mode conversion and data migration; traces, read/write mix, queue depth, locality, phase changes, capacity/overprovisioning, SSD geometry, workload duration, training/validation split and workload holdout are unspecified.

**Hardware and manufacturing assumptions:**

SSD controller managing heterogeneous flash modes with conversion, migration, garbage collection and wear-leveling; NAND generation, channels, firmware, controller compute/memory, host interface, FTL, ECC, thermal state, power-loss protection, program/erase limits and telemetry access are unspecified.

**Baseline — the comparison method:**

State-of-the-art hybrid-SSD management schemes

Heuristic SSD management

LLM-free policy learning

Same flash modes, capacity, overprovisioning, FTL/ECC, workload trace, queueing, latency/SLO target, controller resources, tuning budget, warm-up and long-run measurement boundary are unspecified

**Reported measurements:**

The official description reports average 58.92% higher throughput and 28.56% lower write amplification than state-of-the-art schemes across different real-world workloads; it does not report absolute latency/tails, throughput conditions, endurance/TBW, energy, conversion/migration traffic, capacity, policy/LLM cost, safety violations or per-workload variance.

**Limits on the conclusion:**

A learned tuner proposes control parameters; it does not automatically preserve FTL invariants or flash safety. Define legal placement, mapping, garbage-collection, conversion, migration, ECC, wear-leveling, crash-consistency and power-loss constraints, and use a guarded controller that rejects unsafe actions. Test stale telemetry, invalid parameters, model failures, firmware restart, power loss and concurrent host I/O; a throughput gain is not valid if data is lost or an SLO is violated.

Write amplification is an accounting boundary, not only a policy output. Separate host writes, migration/conversion writes, garbage collection, metadata/ECC and background refresh; report logical-to-physical write ratio, bytes, latency tails, queueing, channel utilization, energy and lifetime/TBW under sustained aging. Include LLM calls, profiling, RL/local-model inference, retraining, policy transfer, fallback and controller CPU/memory in the deployment cost.

The 58.92% and 28.56% averages need named traces, baselines, workload phases and matched tuning. Hold out complete workloads, unseen read/write mixes, capacity pressure, burstiness, temperature and aging; report per-trace results, policy stability and adaptation time. The evidence supports knowledge-guided adaptive hybrid-SSD management, not demonstrated safe, durable, low-tail or universally better controller behavior.

**Source and location**

Evidence tier: Primary captured official DAC description plus existing authored ssd management discussion; no full paper extraction, independent safety/convergence validation, firmware integration or endurance/aging measurement. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH609)

DAC 2026 official description; existing storage-and-data-movement chapter framing; captured Problem, Mechanism / artifact, Workload, Hardware, Baseline, Measurements and Limits fields; no manuscript pages, SSD trace table, policy-action log, endurance study or reproduced long-run controller evaluation.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** heuristic SSD management

LLM-free policy learning

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH609

**Hardware or process assumptions:** SSD controller managing heterogeneous media; endurance, firmware, and workload assumptions are unspecified.

**Limits:** No latency, throughput, endurance, energy, write amplification, or safety results are reported.

LLM policies may behave unpredictably on unseen workloads.

Official description only; long-run workload validation is required.

**Method or artifact:** Knowledge-driven SSD-management policy enhanced by fine-tuned LLMs.

**Metrics:** SSD management efficiency is claimed qualitatively

**Problem:** Hybrid SSD management must balance performance, endurance, placement, and workload changes.

**Workload or benchmark:** Hybrid SSD workloads; media types, policies, and baselines are unspecified.

</details>

<span id="paper-dac-2026-research698"></span>

### Freezone: An On-Device Out-of-Order Writes Reordering Scheme for Consumer Zoned Storage

DAC 2026 · Record: `dac-2026-research698`

[Read the step-by-step explanation](#explanation-dac-2026-research698)

**Updated source-backed reading card**

Reviewed 2026-09-09. Deepens the FreeZone treatment into a paper-level reading; separates kernel-ordering bypass, SLC-backed write-buffer extension and on-device zone reordering from zoned-write correctness, persistence/recovery, flash capacity/endurance, write amplification and complete IOPS/latency accounting, while preserving the up-to-2.3x claim.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Zoned storage requires sequential writes within each zone; kernel-side ordering of irregular consumer writes can serialize requests and reduce parallelism, while an on-device reorder buffer can run out of space as outstanding requests grow.

**Mechanism / artifact:**

FreeZone allows the kernel to submit writes without strict host-side ordering and extends the on-device reorder buffer using high-performance SLC flash, where requests are retained/reordered before being committed in zone order; zone sequence tracking, buffer admission, flush policy, metadata, persistence, recovery and SLC management are unspecified.

**Workload — the work tested:**

Consumer zoned-storage workloads with irregular/random writes and high parallelism; device capacity, zone size/count, write-size distribution, queue depth, workload phases, read/write mix, host kernel, filesystem, cache state, SLC allocation and baseline tuning are unspecified.

**Hardware and manufacturing assumptions:**

Consumer SSD/controller supporting a zone interface, on-device write buffering and an SLC flash region; NAND generation, channels, controller resources, FTL, zone-management commands, host link, power-loss protection, ECC, garbage collection, SLC-to-QLC/TLC conversion, wear and endurance are unspecified.

**Baseline — the comparison method:**

Existing zoned-storage architectures with host-side write ordering

Strict in-order zoned writes

Prior on-device request reordering with limited buffer

Same zone rules, host/kernel/filesystem, device capacity, SLC budget, queue depth, request trace, durability contract, recovery path and end-to-end measurement boundary are unspecified

**Reported measurements:**

The official description reports up to 2.3x IOPS improvement over existing zoned-storage architectures, but does not report absolute IOPS, latency/tails, queueing, write amplification, SLC capacity cost, data-movement overhead, endurance, power-loss recovery, ordering violations or per-workload results.

**Limits on the conclusion:**

Reordering must preserve the zone interface contract. Define per-zone logical write pointer, request identity/ordering, overwrite/append semantics, barriers, flush/FUA, zone reset, synchronization and visibility. Check that every committed sequence is legal and that host acknowledgments do not imply durability before the reordered data and metadata are safe; higher IOPS is invalid if zones become inconsistent.

Using SLC as a reorder buffer trades buffer capacity for flash writes, metadata, garbage collection, conversion and endurance. Measure SLC occupancy, admission/backpressure, spill/fallback, migration bytes, logical-to-physical writes, write amplification, channel utilization, latency tails, energy and TBW under sustained and bursty workloads. Include reorder decisions, buffer management, recovery and cleanup in the IOPS boundary.

Test power loss, controller reset, torn metadata, aborted requests, duplicate/replayed writes, zone reset, full SLC, device aging, thermal throttling and concurrent reads. Compare host ordering and prior device reorderers with equal zone/queue/device/durability settings. The evidence supports SLC-backed on-device zoned-write reordering, not demonstrated crash-safe consistency, durable endurance benefit or portable 2.3x end-to-end performance.

**Source and location**

Evidence tier: Primary captured official DAC description plus existing authored zoned storage discussion; no full paper extraction, independent ordering/persistence validation, slc endurance study or complete iops/latency accounting. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH698)

DAC 2026 official description; existing storage-and-data-movement chapter framing; captured Problem, Mechanism / artifact, Workload, Hardware, Baseline, Measurements and Limits fields; no manuscript pages, zone-order trace, crash-injection result or reproduced consumer-SSD benchmark.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** host-side write ordering

strict in-order zoned writes

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH698

**Hardware or process assumptions:** SSD/controller supporting zoned storage and write reordering; persistence and failure assumptions are unspecified.

**Limits:** No latency, throughput, write amplification, endurance, consistency, or crash results are reported.

Reordering may complicate recovery semantics.

Official description only; fault-injection validation is required.

**Method or artifact:** On-device out-of-order write-reordering scheme.

**Metrics:** Storage performance and write efficiency are claimed qualitatively

**Problem:** Zoned storage constrains write ordering while consumer workloads generate irregular writes.

**Workload or benchmark:** Consumer zoned-storage workloads; media, zone rules, and baselines are unspecified.

</details>

<span id="paper-iccad-2025-1144"></span>

### GAIA: Glass-Aware I/O Middleware

ICCAD 2025 · Record: `iccad-2025-1144`

[Read the step-by-step explanation](#explanation-iccad-2025-1144)

**Updated source-backed reading card**

Reviewed 2026-09-09. Deepens the GAIA institutional-abstract treatment into a paper-level reading; separates glass-aware placement and movement-time scheduling from address correctness, mechanical-optical cost-model validity, latency tails, trace/baseline conditions and deployment evidence, while preserving the up-to-82% abstract claim as withheld pending simulation conditions.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Quartz-glass archival storage combines mechanical X/Y movement and optical Z focusing, creating access costs that conventional I/O schedulers may not model.

**Mechanism / artifact:**

GAIA glass-aware I/O middleware with Zigzag Data Placement, Z-Axis First Placement and Shortest Moving Time First scheduling based on predicted movement time; coordinate mapping, cost model, queue policy, request granularity and update/recovery behavior are unspecified.

**Workload — the work tested:**

Trace-driven simulation of enterprise-scale archival-storage workloads across varied glass sizes; trace identities, request mix/size, glass dimensions, queue depth, concurrency, warm-up and latency distribution are unresolved.

**Hardware and manufacturing assumptions:**

Quartz-glass archival medium with mechanical stage motion along X/Y and optical focus along Z; encoding, media geometry, stage dynamics, acceleration/settling, focus behavior, controller, simulator validation, power, durability and implementation status are unspecified.

**Baseline — the comparison method:**

Traditional baseline schedulers (unnamed in abstract)

FIFO, geometric-distance and movement-aware schedulers under the same traces, glass geometry, request set, capacity, queue depth, warm-up, cost model and end-to-end boundary are unspecified

**Reported measurements:**

The institutional abstract reports up to 82% lower read latency in trace-driven simulation across enterprise-scale workloads and varied glass sizes, but provides no absolute latency, trace-level distribution, throughput, queueing, starvation/fairness, movement/focus breakdown, baseline implementation, simulator calibration or energy/durability result.

**Limits on the conclusion:**

Placement and scheduling must preserve logical address-to-location mapping, object/chunk boundaries, X/Y/Z coordinates, metadata, replication, updates, relocation, retries and recovery. Test stale/wrong/incomplete reads, mixed operations and restart; reducing movement is not useful if data semantics fail.

SMTF depends on a calibrated cost model for direction changes, stage dynamics, settling, focus, media access and queue interference. Compare predicted and measured/simulated service time across directions, distances, depth, queue depth and contention; report p50/p95/p99/p99.9 latency, fairness and starvation, not only an average.

The institutional abstract supports glass-aware archival I/O placement and scheduling, but the up-to-82% claim remains withheld pending trace, glass-size, simulator and baseline conditions. This is archival glass storage, not glass packaging or fabricated-chip evidence, and it does not establish durable, deployable 82% end-to-end improvement.

**Source and location**

Evidence tier: Primary captured institutional abstract plus bounded source recovery assessment and existing storage/data movement explanation; no full paper extraction, reproduced glass storage simulation or deployed media measurement. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://scholar.nycu.edu.tw/en/publications/gaia-glass-aware-io-middleware/)

NYCU institutional abstract; iccad/data/gaia-primary-recovery-v1.json; captured Problem, Mechanism / artifact, Workload, Hardware, Baseline, Measurements and Limits fields; author metadata variants retained; no full manuscript, trace table, simulator calibration or independent validation.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_institutional_abstract

**Baselines:** Traditional baseline schedulers (unnamed in abstract)

**Evidence locators:** **Fields:** problem

method_or_artifact

workload_or_benchmark

hardware_or_process_assumptions

baselines

limits

**Location:** NYCU institutional abstract; iccad/data/gaia-primary-recovery-v1.json

**Evidence url:** https://scholar.nycu.edu.tw/en/publications/gaia-glass-aware-io-middleware/

**Hardware or process assumptions:** Quartz-glass archival storage model; mechanical X/Y stage and optical Z focus; implementation and simulator details unresolved.

**Limits:** The institutional page reports up to 82% read-latency reduction, but the number is withheld pending trace, glass-size and baseline conditions. This is archival glass storage, not glass packaging or fabricated-chip evidence. Author spellings differ between institutional metadata and program/author-lab listings; DOI/title match and source variants are retained.

**Method or artifact:** Zigzag data placement, Z-axis-first placement and shortest-moving-time-first scheduling based on predicted movement time.

**Metrics:** Not established in the captured evidence.

**Problem:** Hybrid mechanical-optical glass storage has movement and depth-traversal costs that conventional I/O schedulers do not model.

**Workload or benchmark:** Trace-driven simulations with enterprise-scale workloads and varied glass sizes; trace identities and sizes unresolved.

</details>

#### Additional source assessment

This separately recorded check is dated 2026-09-06. It supplements the original record above and retains its own scope and uncertainty.

[Assessment record](../../iccad/data/gaia-primary-recovery-v1.json)

[Assessed source](https://scholar.nycu.edu.tw/en/publications/gaia-glass-aware-io-middleware/)

**Extraction scope**

Browser-readable institutional abstract and metadata; author-lab publication entry cross-check. No full text or original capture packet.

**Conditions**

Trace-driven glass-storage simulation; named traces, mechanics, baseline implementations and latency distribution not established by abstract.

**Headline metric status**

withheld_pending_identity_and_simulation_conditions

**Independent review status**

pending

## What remains to establish

Resolve unspecified workloads, comparison methods, resource budgets, and source locations before generalizing a reported gain. Multiple papers in this selected sample permit comparison of mechanisms, but do not by themselves establish recurrence across years or a long-term trend.

[All subthemes](../expanded-taxonomy-v1.md) · [Research directions](../directions/README.md)
