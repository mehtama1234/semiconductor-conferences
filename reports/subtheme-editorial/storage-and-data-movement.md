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
