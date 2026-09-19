# Storage and memory systems

This subject has 3 records in the selected sample. This page explains where it fits, then presents all captured paper evidence without shortening the measurements or limitations.

[Definitions used in the paper records](../reading-guide-v1.md)

## Understand the parent subject first

- [Memory interconnect and storage](../themes/memory-interconnect-and-storage.md)

## Follow the request through the storage system

An application reads and writes file contents. A file system translates a file offset into stored locations and maintains the metadata needed to find those contents later. An SSD controller then manages the flash operations that store or retrieve the encoded data. An improvement at one of these stages need not improve every other stage.

Flash updates also involve more than writing new application bytes. Data can be moved during space reclamation, protected by error-correction information, and read more than once when decoding fails. Write amplification compares the amount written at a specified lower layer with the application's written amount. Always name that lower layer: host-issued device writes and internal flash programming are not identical measurements.

The three papers here address different units of work. RangeLFS changes how file segments are represented and written. COLA changes the unit over which error correction operates. WILL changes how pages are grouped for programming. Their common subject is avoiding unnecessary work while preserving the required data, not a single interchangeable optimization.

<span id="explanation-dac-2026-research2637"></span>

## RangeLFS: an application update need not fill a file-system block

Suppose an application changes only part of the unit a file system normally writes. If the rest of that unit must be preserved, the system may have to obtain the unchanged data, combine it with the update, and write the combined result. This read-modify-write work can exceed what the application requested. The example explains the general alignment problem; it is not a benchmark result.

[From Block to Range](../observed-subthemes/storage-and-memory-systems.md#paper-dac-2026-research2637) proposes RangeLFS for zoned storage. The refreshed official description identifies two coordinated changes: ranges mapping file segments to device addresses, indexed by an enhanced B+ tree, and a page cache supporting partial-page updates and range-based writeback. A B+ tree is an ordered index for finding records without checking them all; the page cache holds file data in memory before or between device accesses.

The abstract reports up to 6.95× write bandwidth over block-based log-structured file systems on a production ZNS SSD, with comparable reads. It does not expose the winning workload, device configuration, exact permitted write sizes, or persistence conditions. Its claim about arbitrary-sized segments should not be generalized into universal byte-addressable writes on every ZNS device. [Official RangeLFS description](https://63dac.conference-program.com/presentation/?id=RESEARCH2637&sess=sess162).

Recovery needs separate evaluation. Faster ordinary writes do not prove that metadata and data remain consistent after power loss. Test interruption between the data write and the mapping update, and verify which acknowledged operations must survive. Those are proposed checks, not reported outcomes of this capture.

The captured evidence supports range-oriented ZNS filesystem design and a bounded write-bandwidth claim, not demonstrated durable end-to-end filesystem improvement across devices and workloads.

<span id="explanation-dac-2026-research607"></span>

## COLA: distinguish code length from storage overhead

Error correction stores user data together with additional check bits. A codeword is the combined protected unit. Code rate is the fraction occupied by user data; code length is the total number of bits in that unit. Holding the rate fixed while changing length is different from adding a larger fraction of check bits.

[COLA](../observed-subthemes/storage-and-memory-systems.md#paper-dac-2026-research607) selects code length per write using a read-latency model and the current raw bit-error rate (RBER). Its failure-aware read path selectively transfers and decodes failed codewords. The official description frames this as reducing read latency while retaining reliability and constant storage overhead, and explicitly identifies MQSim simulation as the evaluation method. It does not establish measured performance of a manufactured COLA controller. [Official COLA description](https://63dac.conference-program.com/presentation/?id=RESEARCH607&sess=sess171).

The authors' laboratory reports Alibaba Cloud workloads and a default 4 KiB code-length baseline, with maximum reductions of 68.69% in average read latency and 71% in the 99.9th-percentile latency. These are maximum reported reductions across the evaluated conditions, not a guarantee for every workload. [HUST laboratory report](https://stlab.wnlo.hust.edu.cn/nr.jsp?urltype=news.NewsContentUrl&wbnewsid=2024&wbtreeid=1046).

The 99.9th percentile is a threshold below which 99.9% of the observed latencies fall. It describes slow requests more directly than the mean, but depends on the workload and number of observations. Reliability comparisons additionally need the uncorrectable-error criterion, wear, retention and read-disturb conditions, and response when a page's error rate changes after writing. The recovered summaries do not resolve these conditions.

The captured evidence supports adaptive ECC code length, not demonstrated device-measured reliable low-latency SSD reads across NAND states.

<span id="explanation-dac-2026-research931"></span>

## WILL: skip obsolete QLC programming without weakening data validity or endurance

An update can make an older stored version invalid because the new version now supplies the logical contents. Invalid does not mean a corrupted live value: it means that version is no longer needed for the current mapping. Skipping work on obsolete versions must still preserve every live version and the metadata identifying it.

[WILL](../observed-subthemes/storage-and-memory-systems.md#paper-dac-2026-research931) addresses two-step programming in QLC NAND, which stores four bits per cell. It predicts page invalidation time, groups similarly short- or long-lived pages onto the same wordline, skips programming when a wordline is fully invalid, and places short-lifespan data on locations requiring expensive fine-step programming. It excludes read-hot data from the mapping to preserve read parallelism. The source does not specify predictor inputs, mapping granularity, remapping cost, controller policy or retention safeguards.

The description reports 10.0% lower programming execution time against an unnamed state-of-the-art comparator, 5.03% additional fully invalid wordlines skipped, 15.9% lower partially invalid ratio on average and a 2.59% read-performance cost. It does not define the baseline, denominator, absolute latency, NAND program count, workload trace or whether the percentage changes are relative or percentage-point changes. These outcomes must not become a claimed endurance gain or whole-application speedup.

The prediction tradeoff is important: grouping by expected lifetime is useful only if prediction errors do not erase the saved work or excessively restrict parallel access. Skipping is safe only if every live page and mapping record remain programmed and readable through remapping, garbage collection and power-loss recovery. Validate ECC margin, read-after-write correctness, retention, wear, temperature and changing update patterns.

Report host writes separately from internal NAND programming, plus write amplification, program/erase counts, GC work, p50/p95/p99 read/write latency, throughput, tail QoS, energy and controller overhead. Include prediction cost, read-hot exclusions and the full mapping/GC path. Compare under the same capacity, overprovisioning, queue depth, read/write QoS, traces and NAND states; test lifespan-distribution shift and prediction error rather than only stable workloads.

The evidence supports lifespan- and latency-aware QLC wordline mapping, not demonstrated durable end-to-end SSD improvement, retention safety, endurance gain or manufactured-device behavior.

## The longer-term question and current evidence boundary

My synthesis is that the storage stack benefits when its work units match both the request and the physical device behavior. However, reducing work at one layer can add metadata, prediction, or decoding cost elsewhere. Compare total request completion under the same durability and reliability requirements before making an end-to-end claim.

The sources were refreshed on 2026-09-07. They provide substantially more mechanism than the older cards below, whose missing-result statements refer to the earlier capture. No full manuscript was recovered in this pass. The result claims remain official-description or author-laboratory evidence, not page-backed experimental audits or independently reproduced measurements. Comparable studies across editions are also still required to establish a historical trend.

## Compare the results carefully

First identify the inputs and required output quality. Then identify the limited resource: time, memory, communication, energy, circuit area, or correctness coverage. Ask which part of the method reduces that cost and which new cost it adds. Compare numbers only when the experiments hold these conditions sufficiently similar.

A conference description may explain the proposal while omitting the full experiment. An author preprint link may have been coded from its abstract. The source classification does not by itself establish that every table was read. Missing locations remain visible below.

## Complete captured evidence

These are evidence records, not substitutes for the explanations above. Each record preserves its problem, proposed method, measurements, comparison conditions, and source limits. A populated record does not establish that its mechanism has been fully explained or independently verified.

<span id="paper-dac-2026-research2637"></span>

### From Block to Range: Rethinking the Fundamental Unit of Log-Structured File Systems for ZNS SSDs

DAC 2026 · Record: `dac-2026-research2637`

[Read the step-by-step explanation](#explanation-dac-2026-research2637)

**Updated source-backed reading card**

Reviewed 2026-09-09. Reconciles the refreshed RangeLFS description with the sparse historical card; separates range-level file mapping, B+ tree metadata and partial-page writeback from ZNS ordering, metadata consistency, durability, write amplification and end-to-end storage performance, while preserving the reported 6.95x write-bandwidth and comparable-read claims.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Block-based log-structured filesystems impose alignment on ZNS SSD writes, so an unaligned file update can trigger read-modify-write work even though the device accepts arbitrary-sized host writes.

**Mechanism / artifact:**

RangeLFS replaces fixed-size block mapping with flexible ranges that map arbitrary-sized file segments to device addresses, maintains the ranges in an enhanced B+ tree, and adds a range-augmented page cache for partial-page writes and range-based writeback; range allocation, zone sequencing, metadata update ordering and recovery protocol are unspecified.

**Workload — the work tested:**

File-system workloads on a production ZNS SSD with block-based log-structured filesystems as the comparison; workload mix, file and update-size distribution, locality, concurrency, queue depth, cache capacity, device geometry, zone utilization, read/write ratio and persistence/crash protocol are unspecified.

**Hardware and manufacturing assumptions:**

Host-managed Zoned Namespace SSD with host-visible zone/write constraints and a filesystem/page-cache stack; SSD controller and firmware, NAND generation, channels, zone size and limits, kernel/filesystem integration, interface, power-loss behavior, garbage collection and internal write accounting are unspecified.

**Baseline — the comparison method:**

Block-based log-structured filesystem on ZNS

Conventional ZNS filesystem

Same files, update trace, cache capacity, queue depth, SSD, zone allocation, kernel, durability mode and end-to-end timing boundary are unspecified

**Reported measurements:**

The refreshed description reports up to 6.95× higher write bandwidth than block-based log-structured filesystems on a production ZNS SSD and comparable read performance across diverse workloads; it does not expose absolute throughput, latency, write amplification, metadata/cache overhead, endurance, recovery time or the winning workload and device conditions.

**Limits on the conclusion:**

A range mapping can reduce alignment-induced read-modify-write work while adding range metadata, B+ tree lookup/update, fragmentation, garbage collection and cache-management costs. Measure application bytes, host writes, device writes and internal flash programming separately, and include metadata, cache, zone-management and reclamation work in the end-to-end boundary.

Arbitrary-sized host writes do not remove ZNS zone capacity, write-pointer, ordering or reset rules. Evaluate range splitting/merging, partial-page updates, zone exhaustion, hot/cold data, concurrent writers, crash interruption between data and mapping updates, replay and power-loss recovery; verify which acknowledged writes and metadata must survive.

The up-to-6.95× write-bandwidth claim and comparable reads are bounded description-level results. Report absolute throughput and latency, workload/update-size distributions, cache and queue settings, SSD geometry and firmware, read performance tails, write amplification, endurance, space utilization and recovery behavior under matched baselines. The evidence supports range-oriented ZNS filesystem design, not demonstrated durable end-to-end filesystem improvement across devices and workloads.

**Source and location**

Evidence tier: Primary captured official DAC description plus refreshed official abstract; no full paper extraction, device condition matrix, durability test or independent reproduction. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/presentation/?id=RESEARCH2637&sess=sess162)

Refreshed DAC 2026 RangeLFS description/abstract; existing storage-and-memory-systems editorial explanation; captured Problem, Mechanism / artifact, Workload, Hardware, Baseline, Measurements and Limits fields; no full manuscript, benchmark table or crash-recovery trace.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** block-based LFS

conventional ZNS filesystem

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH2637

**Hardware or process assumptions:** Zoned namespace SSD with host-managed writes; zone size, flash controller, and persistence assumptions are unspecified.

**Limits:** No throughput, write amplification, latency, endurance, recovery, or workload results are reported.

Range policies may depend on update locality.

Official description only; device and crash-consistency validation is required.

**Method or artifact:** Range-level filesystem organization for ZNS SSDs.

**Metrics:** ZNS filesystem efficiency is claimed qualitatively

**Problem:** Block-granular log-structured filesystems can create write amplification and inefficiency on zoned namespace SSDs.

**Workload or benchmark:** ZNS storage workloads; SSD geometry, durability, and filesystem baseline are unspecified.

</details>

<span id="paper-dac-2026-research607"></span>

### COLA: Enabling Low-Latency Reads for Flash-Based SSDs via Code Length Adaptation

DAC 2026 · Record: `dac-2026-research607`

[Read the step-by-step explanation](#explanation-dac-2026-research607)

**Updated source-backed reading card**

Reviewed 2026-09-09. Deepens the COLA treatment into a paper-level reading; separates per-write ECC code-length selection, failure-aware transfer/decoding and RBER-based latency modeling from code-rate/storage accounting, uncorrectable-error guarantees, NAND aging, retention, endurance and manufactured-controller validation, while preserving the 68.69% average and 71% 99.9th-percentile latency reductions with their evaluated conditions.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Flash SSD raw bit-error rate changes with device state, while longer ECC codewords can improve correction reliability and shorter codewords can reduce read latency; a fixed code length cannot optimize both as pages age or differ.

**Mechanism / artifact:**

COLA selects the ECC code length for each write using current RBER and a failure-aware read-latency model, while maintaining fixed code rate and constant storage overhead. Its failure-aware read path selectively transfers and decodes failed codewords instead of processing every codeword identically; RBER estimation, codeword metadata, decoder scheduling, retry policy and controller integration are incompletely specified.

**Workload — the work tested:**

Flash SSD reads evaluated in MQSim and an author-laboratory report using Alibaba Cloud workloads, with a default 4 KiB code-length baseline; NAND type, page/block geometry, workload mix, queue depth, read/write ratio, retention age, wear state, raw-error distribution, latency sample count and tail protocol are unspecified.

**Hardware and manufacturing assumptions:**

Flash SSD controller with configurable ECC code length and selective failed-codeword transfer/decoding; MQSim is explicitly identified for the simulation evaluation. NAND generation, SLC/MLC/TLC/QLC mode, ECC family/decoder, controller firmware, interface, voltage/temperature, program/erase history, retention, read disturb, overprovisioning, endurance and manufactured-device measurement are unspecified.

**Baseline — the comparison method:**

Default fixed-code-length ECC

Standard SSD controller/read path

Fixed 4 KiB code-length baseline in the reported laboratory comparison

Same code rate, user-visible capacity, NAND geometry, ECC correction target, workload, queue depth, wear/retention state, controller, decoder, latency percentile and background activity are unspecified

**Reported measurements:**

The author-laboratory report gives maximum reductions of 68.69% in average read latency and 71% in 99.9th-percentile read latency relative to the fixed-code-length baseline across evaluated conditions; the official description identifies MQSim simulation and reduced average/tail latency but does not expose absolute latency, error rates, throughput, energy, endurance, capacity overhead, uncorrectable-error rate or per-workload results.

**Limits on the conclusion:**

Code length and code rate are different quantities. Holding code rate constant while changing codeword length does not by itself prove constant user capacity, parity overhead, decoder work or correction margin. Report user bits, parity bits, codeword count, metadata, transfer volume, decoder cycles and the exact uncorrectable-error criterion for every selected length.

RBER is state-dependent and must be calibrated against held-out NAND measurements across wear, retention, read disturb, temperature and voltage. A latency model can choose a short code under an incorrectly estimated error tail, causing retries or uncorrectable data; measure error distributions, failed-codeword selection, recovery success, tail latency and controller/decoder overhead rather than only modeled means.

The 68.69% average and 71% 99.9th-percentile reductions are maximum reported results from simulation/laboratory evaluation, not proof of a manufactured SSD controller's reliability or endurance. Include program/erase lifetime, retention, read/write interference, throughput, energy, capacity, garbage collection and firmware cost at matched quality and workload. The evidence supports adaptive ECC code length, not demonstrated device-measured reliable low-latency SSD reads across NAND states.

**Source and location**

Evidence tier: Primary captured official DAC description plus author laboratory summary; mqsim/laboratory latency claims without full paper extraction, manufactured controller measurement or independent nand validation. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/presentation/?id=RESEARCH607&sess=sess171)

Refreshed DAC 2026 official COLA description identifying MQSim; author-laboratory report on Alibaba Cloud workloads and 4 KiB baseline; existing storage-and-memory-systems editorial explanation; no full manuscript, NAND-condition matrix, decoder trace or independent device reproduction.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** fixed-length ECC

standard SSD controller

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH607

**Hardware or process assumptions:** Flash SSD with configurable ECC; endurance and reliability assumptions are unspecified.

**Limits:** No latency, error rate, endurance, throughput, energy, or NAND results are reported.

Shorter codes may reduce reliability margin.

Official description only; device and workload validation is required.

**Method or artifact:** Adaptive code-length mechanism for flash SSD reads.

**Metrics:** Read latency efficiency is claimed qualitatively

**Problem:** Flash SSD read latency is affected by error-correction code length and device conditions.

**Workload or benchmark:** Flash SSD read workloads; NAND type, retention, error rates, and controller are unspecified.

</details>

<span id="paper-dac-2026-research931"></span>

### WILL: Write Invalidation Skipping for QLC NAND by Leveraging Data Lifespan and Latency Awareness

DAC 2026 · Record: `dac-2026-research931`

[Read the step-by-step explanation](#explanation-dac-2026-research931)

**Updated source-backed reading card**

Reviewed 2026-09-09. Deepens the WILL treatment into a paper-level reading; separates lifespan prediction, wordline grouping and latency-aware fine-step scheduling from NAND validity, retention, garbage collection, write amplification and endurance, while preserving the 10.0%, 5.03%, 15.9% and 2.59% source claims with their bounded conditions.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

QLC NAND uses a slow two-step programming process, and updating pages on a wordline between those steps can invalidate prior pages and waste programming effort. Misaligned invalidation times leave partially invalid wordlines that still incur programming work.

**Mechanism / artifact:**

WILL predicts page invalidation time, groups pages with similar lifespans into wordlines so partially invalid wordlines become fully valid or fully invalid, skips programming on fully invalid wordlines, assigns short-lifespan data to high-latency fine-step locations, and excludes read-hot data to preserve read parallelism. Predictor features, mapping granularity, remapping cost, controller policy and retention safeguards are unspecified.

**Workload — the work tested:**

3D QLC NAND programming with data-lifespan variation and read-hot data; the source reports comparison against a state-of-the-art method but does not identify the SSD/controller, NAND geometry, traces, write/read mix, queue depth, update rate, lifespan distribution, prediction accuracy, overprovisioning, garbage-collection policy or test duration.

**Hardware and manufacturing assumptions:**

QLC NAND SSD with two-step programming, wordline/page mapping, garbage collection and read parallelism; NAND generation, cell geometry, program voltage/timing, controller firmware, channel/die/plane organization, buffer capacity, wear state, retention age, temperature, interface, compute overhead and manufactured-device status are unspecified.

**Baseline — the comparison method:**

State-of-the-art QLC invalidation/programming policy

Standard invalidation or lifespan-oblivious SSD controller

Same NAND, logical capacity, overprovisioning, workload trace, queue depth, read/write QoS, garbage collection, mapping budget, simulator/device and measurement boundary are unspecified

**Reported measurements:**

The official description reports 10.0% lower programming execution time, 5.03% additional fully-invalid wordlines skipped, 15.9% lower partially-invalid ratio on average and a 2.59% read-performance cost; it does not define the baseline, denominator, absolute latency, write amplification, NAND program count, throughput, tail latency, endurance, retention/error rate, energy, controller overhead or device validation.

**Limits on the conclusion:**

Skipping programming is safe only if every live page and its mapping metadata remain programmed and readable. Validate invalidation prediction errors, remapping races, power-loss recovery, garbage-collection relocation, read-after-write correctness, ECC margin and behavior under retention, wear, temperature and changing update patterns.

A lower partially-invalid ratio or programming time does not automatically mean lower host latency, write amplification or longer endurance. Report host and internal NAND writes separately, program/erase counts, GC work, queueing, p50/p95/p99 read/write latency, throughput, tail QoS, energy and controller CPU/memory overhead, with read-hot exclusions and prediction cost included.

The 10.0%, 5.03%, 15.9% and 2.59% claims do not establish general QLC SSD performance, retention safety, endurance or manufactured-device behavior. Define whether percentage changes are relative or percentage-point, hold capacity and QoS constant, test lifespan-distribution shift and prediction error, and compare across NAND states and traces. The evidence supports lifespan- and latency-aware QLC wordline mapping, not demonstrated durable end-to-end SSD improvement.

**Source and location**

Evidence tier: Primary captured official DAC description plus existing authored storage and memory systems discussion; no full paper extraction, reproduced controller trace, manufactured device validation or endurance study. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH931)

DAC 2026 official description; existing storage-and-memory-systems editorial explanation; captured Problem, Mechanism / artifact, Workload, Hardware, Baseline, Measurements and Limits fields; no manuscript pages, prediction trace, NAND-state matrix, endurance/retention result or device reproduction.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** standard invalidation

lifespan-oblivious SSD controller

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH931

**Hardware or process assumptions:** QLC flash SSD with garbage collection and wear management; device assumptions are unspecified.

**Limits:** No latency, write amplification, endurance, throughput, energy, or NAND results are reported.

Skipping decisions may affect retention and garbage collection.

Official description only; device and trace validation is required.

**Method or artifact:** Write invalidation skipping based on data lifespan and latency.

**Metrics:** QLC efficiency is claimed qualitatively

**Problem:** QLC NAND incurs write and garbage-collection cost when invalid data is invalidated or moved unnecessarily.

**Workload or benchmark:** QLC NAND storage workloads; controller, retention, and workload locality are unspecified.

</details>

## What remains to establish

Resolve unspecified workloads, comparison methods, resource budgets, and source locations before generalizing a reported gain. Multiple papers in this selected sample permit comparison of mechanisms, but do not by themselves establish recurrence across years or a long-term trend.

[All subthemes](../expanded-taxonomy-v1.md) · [Research directions](../directions/README.md)
