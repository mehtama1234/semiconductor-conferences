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
