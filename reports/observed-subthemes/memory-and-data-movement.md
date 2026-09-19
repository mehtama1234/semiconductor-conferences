# Memory and data movement

This subject has 6 records in the selected sample. This page explains where it fits, then presents all captured paper evidence without shortening the measurements or limitations.

[Definitions used in the paper records](../reading-guide-v1.md)

## Understand the parent subject first

- [Architecture and accelerators](../themes/architecture-and-accelerators.md)
- [Memory interconnect and storage](../themes/memory-interconnect-and-storage.md)

## Start with the lifetime of a value

A calculation produces a value, and some later calculation consumes it. Between those events, the system must keep the value somewhere, encode it in a smaller form, or discard it and calculate it again. Each choice has a cost. Keeping the value occupies storage. Moving it takes time and electrical energy. Encoding and reconstructing it require work. Recomputing it consumes arithmetic capacity and may require fetching its original inputs again.

These costs are related but not identical. **Capacity** is how many bytes fit at once. **Bandwidth** is how many bytes a path can transfer per second. **Latency** is how long an individual request takes to finish. A program can fit in memory and still wait for transfers. It can also use only a small fraction of a device's advertised bandwidth because its next address depends on a previous result. More arithmetic units do not remove either problem.

Consider an explicitly hypothetical transfer: moving one billion bytes through a path that sustains one hundred billion bytes per second requires at least 0.01 seconds of service. This calculation excludes waiting, setup, and computation. Reducing the bytes by half saves at most 0.005 seconds on that path if the rate stays fixed. Compression is not a latency improvement if its additional, non-overlapped work takes longer than that saving. The same change may still be worthwhile if it makes an otherwise impossible allocation fit.

The six papers below modify different parts of this value lifetime. All six belong to the selected DAC 2026 sample; they do not establish a comparison across conferences or years. The current review refreshed their official descriptions on 2026-09-07. It did not recover readable full manuscripts. Consequently, source locations below identify **Description** or **Abstract** sections, not invented PDF pages. The corresponding cards are corrected from those sources, with older captured fields retained separately.

## Six distinct technical questions

| Question | What changes | What must also be measured |
|---|---|---|
| Can training state occupy fewer bits without becoming too fragile? | Activation representation and fault handling: REACT | Training quality, error model, reconstruction cost |
| Can several execution groups use one stored value? | Register sharing and access selection: CODA | Shared access traffic, conflicts, circuit power |
| Which requests interfere in a real memory system? | Joint workload and host-traffic measurement: Toki | Achieved bandwidth and delays under concurrent traffic |
| Which program benefits from the next unit of cache space? | Allocation size and adjustment timing: Cachence | Prediction error, application slowdown, control cost |
| Can inference values be compressed without changing their bits? | Floating-point encoding and parallel packing: ZipFloat | Exact reconstruction, total bytes, codec and application time |
| Is keeping an intermediate value cheaper than recreating it? | Graph recomputation and operation splitting: PRICE | Peak live storage, extra operations, complete runtime |

## Representation: fewer bits is not one kind of correctness

An activation is an intermediate numerical result inside a neural network. Training often needs intermediate results again when calculating how to change the model's parameters. Those values can remain live for much longer than a single arithmetic instruction. A larger group of training examples or a longer input can therefore increase storage even when the model parameters are unchanged.

A floating-point value is represented using a sign, an exponent that controls numerical scale, and significant digits. Removing some digits changes the value. Reorganizing repeated bit patterns can instead reduce storage while allowing exact reconstruction. A third question is what happens when stored bits change accidentally. Exact decoding in fault-free operation does not guarantee useful decoding after a fault. Nor does acceptable training quality prove that the original activation values were recovered exactly.

### REACT: compression and fault sensitivity must be tested together

[REACT](../observed-subthemes/memory-and-data-movement.md#paper-dac-2026-research2947) combines base-delta compression with an encoding intended to limit errors in vulnerable bits. Its refreshed description reports fourfold lower activation memory and maintained accuracy at a thousandfold higher bit-error rate, but omits absolute rates, models, and the quality criterion. These are conditional author claims, not a verified reliability guarantee. [Source: official Description, mechanism and final-result sentences](https://63dac.conference-program.com/presentation/?id=RESEARCH2947&sess=sess142).

The conceptual issue is that sharing one base value among many encoded differences changes how a fault propagates. Corrupting a shared field can affect several reconstructed values; corrupting a field used once has a different reach. A useful evaluation must specify which fields receive injected faults, whether faults are independent or clustered, and how long corrupted state remains in use. Comparing only the number of stored bits cannot establish reliability. Compare complete training runs at the same target quality, including failed runs and any recovery work.

### ZipFloat: exact representation still needs a system-level test

[ZipFloat](../observed-subthemes/memory-and-data-movement.md#paper-dac-2026-research684) targets model weights and saved attention keys and values, rather than only generic intermediate activations. Its description names exponent sparsification and bit-matrix packing, with GPU-parallel compression and decompression. The reported maxima include 700 GB/s codec throughput, over 95% lower time to first output token, and over fourfold inference throughput. Hardware, input sizes, precise ratios, and the system comparison conditions remain absent. [Source: official Description, two numbered mechanisms and evaluation sentence](https://63dac.conference-program.com/presentation/?id=RESEARCH684&sess=sess109).

Saved attention keys and values are numerical summaries of earlier input positions that later output steps reuse. Compressing them can change how many requests fit simultaneously. That can improve total service throughput without making an individual arithmetic operation faster. It is therefore necessary to separate codec speed, request concurrency, and per-request latency. An exactness test should compare decoded bit patterns, including supported special values, rather than merely compare a model's final accuracy. A capacity test must count headers, indexing, temporary buffers, and incompressible cases.

## Allocation: unused capacity and blocked access are different failures

A register is small storage directly used by executing instructions. A register file contains many such locations and is often divided into banks, each with limited simultaneous access. Enough free locations do not guarantee that two requests can be served together: both may address the same bank. Conversely, a balanced request pattern does not eliminate duplicate values occupying several locations.

### CODA: share values, then handle the requests to them

[CODA](../observed-subthemes/memory-and-data-movement.md#paper-dac-2026-research387) proposes cooperative register renaming to keep a single physical copy across GPU sub-cores, plus an arbitrator that uses operand-collector identity when selecting accesses. The description reports 28.9% speedup and 15.6% lower register-file power, alongside reduced imbalance and conflicts. It does not establish a fabricated-chip result or name the tested GPU and workload suite. This is the register-sharing CODA, not the separately listed NPU dataflow paper with the same acronym. [Source: official Description, paragraphs 1–3](https://63dac.conference-program.com/presentation/?id=RESEARCH387&sess=sess143).

A general sharing design needs rules for locating a shared value, protecting it while readers still need it, and handling a write that should no longer be shared. These are evaluation questions, not mechanisms established for this paper by its short description. Sharing can reduce storage and repeated writes while increasing traffic to the remaining copy. The meaningful comparison holds the register capacity and access resources explicit. Register-file power also covers a smaller boundary than whole-GPU energy, which depends on execution time and all active components.

### Cachence: the value of cache space changes during execution

A cache keeps selected copies of data to avoid repeated accesses to a slower memory. A miss occurs when the needed copy is absent. Giving a program additional cache space helps only if it retains data that will actually be reused. Dividing cache equally can therefore be inefficient, but repeatedly changing the division can also evict useful data and create measurement overhead.

[Cachence](../observed-subthemes/memory-and-data-movement.md#paper-dac-2026-research441) combines hardware access profiling with a runtime performance model for timely, fine-grained allocation. The author-lab abstract describes roughly two kilobytes of profiling storage per core and evaluates a 16-core system. It reports average improvements of 9.5–28.2% against existing approaches, but the accessible abstract does not identify the exact benchmark mixtures or performance objective. Its accuracy guarantee concerns the profiling model; it is not a guarantee that every application gets faster. [Source: author-lab Abstract, profiling, model, and evaluation paragraphs](https://telos.top/publication/26-dac-li/).

A miss-ratio curve describes how often requests miss at different cache allocations. Turning that curve into a speed prediction needs another step: how much of the missing-data delay actually prevents progress? A processor may continue independent work while waiting. Two programs with equal miss reductions can therefore have different runtime improvements. Evaluate the allocation policy with phase changes, short runs, and competing programs, and report each program's slowdown as well as aggregate performance. Otherwise a total improvement can hide a substantial loss for one participant.

## Measurement: the traffic source changes the result

High-bandwidth memory, or HBM, offers many parallel memory connections. A field-programmable gate array, or FPGA, is a device whose logic can be configured to implement circuits, including processor cores. A soft core is such a processor implemented in configurable logic. Direct memory access, or DMA, moves data without the host processor individually copying every word; PCIe is the connection carrying that host–device traffic here.

[Toki](../observed-subthemes/memory-and-data-movement.md#paper-dac-2026-research389) combines RISC-V soft-core workloads with host DMA traffic on an AMD Alveo U55C and its HBM2 memory. The description reports configurations up to 60 cores and application/microbenchmark experiments. It describes profiling access patterns, locality, controller contention, and concurrent host traffic, rather than claiming a general application speedup. The description says the framework is open source; no repository or executable reproduction was verified in this pass. [Source: official Description, framework and experiment sentences](https://63dac.conference-program.com/presentation/?id=RESEARCH389&sess=sess147).

A traffic generator can issue requests at a prescribed rate. A running program can instead wait for one result before issuing its next request. These experiments exercise different limits. Concurrent host traffic also competes at particular shared controllers or connections, not necessarily uniformly across the entire device. To explain a measurement, record where addresses map, how much work is outstanding, the read/write mixture, and whether host and device requests overlap in time. A board's peak bandwidth is not an observed application result.

## Recomputation: lower peak storage can require more work

A computation graph lists operations and the values passed between them. A value remains live until its last required use. Peak memory is the largest simultaneous set of live values and temporary storage, not the sum of every value produced during the run. Discarding an intermediate can lower that peak, but later uses require reconstruction. Splitting an operation into smaller pieces can also lower temporary storage while adding scheduling and coordination.

[PRICE](../observed-subthemes/memory-and-data-movement.md#paper-dac-2026-research863) combines compile-time modeling with runtime decisions about recomputation and operation splitting. It uses attainable arithmetic intensity to balance storage and latency. The description reports tests on RTX 4090 and A100 GPUs and 1.08–1.31× speedup at comparable peak-memory reduction against prior work. It omits the full workload list, named competitors, and absolute peak-memory results. [Source: official Description, modeling and experiment sentences](https://63dac.conference-program.com/presentation/?id=RESEARCH863&sess=sess146).

Arithmetic intensity means arithmetic operations per byte transferred across a specified memory boundary. That boundary matters: a value kept in a register may avoid external-memory traffic while still requiring on-chip accesses. Increasing intensity by adding useless calculations is not a benefit. The useful question is whether extra computation removes enough transfers or makes a feasible execution schedule possible. Evaluate complete runtime, the number of extra operations, peak allocated bytes, and output equivalence. A theoretical throughput limit alone does not account for dependencies, insufficient parallel work, or runtime decision cost.

## The combined insight, and how to challenge it

The cross-paper interpretation is that reducing memory cost requires coordinating **representation, lifetime, placement, and access**. This is an organizing explanation, not a demonstrated integrated system. Compression changes sizes and decode costs; recomputation changes which values exist at once; allocation changes who retains them; sharing changes where requests concentrate. A combination that improves each component in isolation may still increase total runtime when their added costs coincide.

One testable long-term hypothesis is that decisions informed by current value lifetimes and access contention will outperform fixed rules under changing workloads. Challenge it with stable workloads where a fixed policy has little control overhead, incompressible tensors, rapidly changing phases, and arithmetic-saturated executions where recomputation is expensive. Those are candidate counterexamples, not failures demonstrated by these six papers. Establishing a temporal trend would additionally require equivalent earlier-edition coverage and comparable measurements.

The immediate evidence gaps are specific. Recover readable manuscripts for all six records; match versions and author identities; extract experimental sections and tables; and reconcile the headline ratios with their actual baselines. A REACT-related thesis search hit was found at the SNU repository, but the download failed certificate validation on one hostname and returned a JavaScript landing page on the other. No thesis pages are cited as inspected. Cachence's author abstract was accessible, but its DOI route did not yield readable paper content. These access outcomes do not prove the papers are unavailable elsewhere. No independent scientific review or reproduction was completed here.

## Compare the results carefully

First identify the inputs and required output quality. Then identify the limited resource: time, memory, communication, energy, circuit area, or correctness coverage. Ask which part of the method reduces that cost and which new cost it adds. Compare numbers only when the experiments hold these conditions sufficiently similar.

A conference description may explain the proposal while omitting the full experiment. An author preprint link may have been coded from its abstract. The source classification does not by itself establish that every table was read. Missing locations remain visible below.

## Complete captured evidence

These are evidence records, not substitutes for the explanations above. Each record preserves its problem, proposed method, measurements, comparison conditions, and source limits. A populated record does not establish that its mechanism has been fully explained or independently verified.

<span id="paper-dac-2026-research2947"></span>

### REACT: Rapid Error-Tolerant Activation Compressor for Efficient Transformer Training

DAC 2026 · Record: `dac-2026-research2947`

**Updated source-backed reading card**

Reviewed 2026-09-07. Refreshed official description supplies mechanisms and conditional metrics absent from the older summary.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Training activations consume storage; compressed state can be sensitive to bit faults.

**Mechanism / artifact:**

Base-delta encoding plus error-limiting treatment of remaining vulnerable bits.

**Workload — the work tested:**

Transformer training; exact models and datasets absent.

**Hardware and manufacturing assumptions:**

Platform and absolute injected bit-error rates unspecified.

**Baseline — the comparison method:**

Comparison configuration not identified in the description.

**Reported measurements:**

Claims fourfold activation-memory reduction and maintained accuracy at a thousandfold higher bit-error rate.

**Limits on the conclusion:**

Quality threshold, fault distribution, trial count, and overhead measurements remain unknown; no full manuscript inspected.

**Source and location**

Evidence tier: Refreshed official description. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/presentation/?id=RESEARCH2947&sess=sess142)

Description: mechanism and final experimental-result sentences; no PDF pagination.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** uncompressed training

generic activation compression

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH2947

**Hardware or process assumptions:** Training accelerator and memory/interconnect; decompression and error assumptions are unspecified.

**Limits:** No convergence, final quality, compression ratio, bandwidth, energy, or hardware results are reported.

Error tolerance may be model-specific.

Official description only; training and implementation validation is required.

**Method or artifact:** Rapid error-tolerant activation compression for training.

**Metrics:** Training efficiency is claimed qualitatively

**Problem:** Transformer training stores and moves large activations, while compression errors can affect convergence.

**Workload or benchmark:** Transformer training; models, compression ratio, precision, and hardware are unspecified.

</details>

<span id="paper-dac-2026-research387"></span>

### CODA: Cooperative Register Distribution and Arbitration Among Partitioned GPU Sub-Cores

DAC 2026 · Record: `dac-2026-research387`

**Updated source-backed reading card**

Reviewed 2026-09-07. Refreshed description distinguishes duplicate-value sharing from bank-conflict arbitration.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Private GPU registers duplicate values and receive imbalanced, conflicting accesses.

**Mechanism / artifact:**

Cooperative renaming retains one physical copy; arbitration considers operand-collector identity.

**Workload — the work tested:**

Deep-learning workloads; named suite absent.

**Hardware and manufacturing assumptions:**

Partitioned GPU sub-cores; exact platform and implementation method unspecified.

**Baseline — the comparison method:**

Unnamed baseline architecture.

**Reported measurements:**

Reported 28.9% speedup and 15.6% lower register-file power; 15.9% lower imbalance and 12.7% lower conflict rate.

**Limits on the conclusion:**

Register-file power is not whole-GPU energy. Not the separate NPU dataflow CODA. Full-paper evaluation remains open.

**Source and location**

Evidence tier: Refreshed official description. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/presentation/?id=RESEARCH387&sess=sess143)

Description, paragraphs 1–3; no PDF pagination.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** static register partitioning

standard GPU arbitration

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH387

**Hardware or process assumptions:** Partitioned GPU with shared or distributed register resources; cache and interconnect assumptions are unspecified.

**Limits:** No throughput, occupancy, fairness, latency, energy, or kernel results are reported.

Register demand may vary sharply across kernels.

Official description only; architecture and workload validation is required.

**Method or artifact:** Cooperative register distribution and arbitration mechanism.

**Metrics:** GPU utilization is claimed qualitatively

**Problem:** Partitioned GPU sub-cores can suffer register imbalance and arbitration overhead.

**Workload or benchmark:** GPU kernels across partitioned sub-cores; architectures, register demand, and baselines are unspecified.

</details>

<span id="paper-dac-2026-research389"></span>

### Toki: Profiling HBM Performance on FPGA Systems with RISC-V Soft Cores and PCIe Host DMA Traffic

DAC 2026 · Record: `dac-2026-research389`

**Updated source-backed reading card**

Reviewed 2026-09-07. The refreshed description names the physical board and scale omitted by the old card.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Isolated traffic tests miss interactions between running programs and host transfers.

**Mechanism / artifact:**

Joint soft-core execution and host PCIe DMA profiling.

**Workload — the work tested:**

Applications and programmable-access microbenchmarks; exact suite absent.

**Hardware and manufacturing assumptions:**

AMD Alveo U55C, HBM2, up to 60 RISC-V soft cores.

**Baseline — the comparison method:**

Description contrasts synthetic traffic generators; no numerical competitor comparison supplied.

**Reported measurements:**

Profiles locality, controller contention, and concurrent host traffic; no universal speedup claimed.

**Limits on the conclusion:**

Open-source availability is author-reported; repository, measurements, and reproduction were not verified here.

**Source and location**

Evidence tier: Refreshed official description. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/presentation/?id=RESEARCH389&sess=sess147)

Description: framework, experiment, and result sentences; no PDF pagination.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** isolated HBM access

CPU or GPU memory profiling

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH389

**Hardware or process assumptions:** FPGA with HBM, RISC-V soft cores, and PCIe; clock and memory-controller assumptions are unspecified.

**Limits:** No bandwidth, latency, contention, power, or platform-comparison results are reported.

Profiles may be board- and traffic-specific.

Official description only; measured workload validation is required.

**Method or artifact:** Profiling methodology or system for HBM and PCIe DMA interactions.

**Metrics:** HBM profiling fidelity is claimed qualitatively

**Problem:** HBM performance on FPGA systems depends on soft-core access patterns and host DMA contention.

**Workload or benchmark:** HBM access and PCIe host-DMA workloads; FPGA, HBM generation, and traffic patterns are unspecified.

</details>

<span id="paper-dac-2026-research441"></span>

### Cachence: Fine-Grained Cache Partitioning in Both Time and Space

DAC 2026 · Record: `dac-2026-research441`

**Updated source-backed reading card**

Reviewed 2026-09-07. Author-lab abstract adds profiling scope and per-core storage while leaving full experiments unresolved.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Cache allocation needs both timely adjustment and fine spatial resolution.

**Mechanism / artifact:**

Hardware miss-ratio profiling and runtime-statistics performance prediction.

**Workload — the work tested:**

Application mixtures not identified in the accessible abstract.

**Hardware and manufacturing assumptions:**

16-core evaluation; roughly 2 KB profiling storage per core.

**Baseline — the comparison method:**

Existing approaches, unnamed in the abstract.

**Reported measurements:**

Reported average gains 9.5–28.2%, maximum 48.8%; exact performance objective unresolved.

**Limits on the conclusion:**

Profiling accuracy guarantees are not universal application-speed guarantees. Full manuscript, benchmark details, and reproduction remain open.

**Source and location**

Evidence tier: Author lab abstract. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://telos.top/publication/26-dac-li/)

Abstract: profiling, performance-model, and final evaluation paragraphs; no PDF pagination.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** static cache partitioning

unpartitioned cache

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH441

**Hardware or process assumptions:** Shared cache with controllable allocation; hardware support and coherence assumptions are unspecified.

**Limits:** No miss rate, tail latency, fairness, throughput, energy, or hardware results are reported.

Partitioning overhead may affect short jobs.

Official description only; workload-diverse validation is required.

**Method or artifact:** Fine-grained time-and-space cache partitioning.

**Metrics:** Cache isolation and efficiency are claimed qualitatively

**Problem:** Shared caches need temporal and spatial partitioning to control interference among workloads.

**Workload or benchmark:** Co-located CPU or accelerator workloads; cache hierarchy, QoS, and baselines are unspecified.

</details>

<span id="paper-dac-2026-research684"></span>

### Zipfloat: An Ultra-Fast and Lossless Floating-Point Compressor for LLM Inference Systems

DAC 2026 · Record: `dac-2026-research684`

**Updated source-backed reading card**

Reviewed 2026-09-07. Refreshed description identifies software GPU-parallel encoding rather than establishing a dedicated accelerator circuit.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Weights and saved attention keys/values pressure inference memory.

**Mechanism / artifact:**

Exponent sparsification and bit-matrix packing for GPU-parallel lossless encoding.

**Workload — the work tested:**

LLM inference; named models and input sizes absent.

**Hardware and manufacturing assumptions:**

GPU model, format coverage, and temporary-buffer costs unspecified.

**Baseline — the comparison method:**

DFloat11 named for codec comparison; system baseline unresolved.

**Reported measurements:**

Claims up to 700 GB/s codec throughput, over 95% lower first-token time, over 4× inference throughput.

**Limits on the conclusion:**

Maximum codec rate is not application speedup. Exactness and complete memory accounting need manuscript and artifact checks.

**Source and location**

Evidence tier: Refreshed official description. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/presentation/?id=RESEARCH684&sess=sess109)

Description: numbered mechanisms and final evaluation sentence; no PDF pagination.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** uncompressed floating point

generic lossless compression

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH684

**Hardware or process assumptions:** Compression/decompression datapath in an inference accelerator; throughput and area assumptions are unspecified.

**Limits:** No compression ratio, throughput, latency, area, energy, or model results are reported.

Tensor distributions may vary across models and layers.

Official description only; system validation is required.

**Method or artifact:** Lossless floating-point compression for inference systems.

**Metrics:** Compression speed and ratio are claimed qualitatively

**Problem:** Floating-point LLM activations and weights create memory-bandwidth and capacity pressure.

**Workload or benchmark:** LLM inference tensors; formats, models, and memory system are unspecified.

</details>

<span id="paper-dac-2026-research863"></span>

### PRICE: An Operator Recomputation and Fission Framework for Computation Graphs via Attainable Arithmetic Intensity

DAC 2026 · Record: `dac-2026-research863`

**Updated source-backed reading card**

Reviewed 2026-09-07. Refreshed description supplies tested GPUs and narrows the speed comparison to comparable peak-memory reduction.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Reducing graph peak memory through fixed recomputation/splitting decisions can add latency.

**Mechanism / artifact:**

Compile-time arithmetic-intensity modeling with runtime decision instantiation.

**Workload — the work tested:**

GPU computation graphs; exact models and shapes absent.

**Hardware and manufacturing assumptions:**

NVIDIA RTX 4090 and A100 experiments.

**Baseline — the comparison method:**

Prior work unnamed in the description.

**Reported measurements:**

Reports 1.08–1.31× speedup with comparable peak-memory reduction.

**Limits on the conclusion:**

Absolute memory, graph correctness checks, decision overhead, and complete timing conditions require the manuscript.

**Source and location**

Evidence tier: Refreshed official description. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/presentation/?id=RESEARCH863&sess=sess146)

Description: compile/runtime modeling and final experiment sentences; no PDF pagination.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** unchanged computation graph

static recomputation

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH863

**Hardware or process assumptions:** Accelerator or CPU/GPU graph runtime; memory and scheduling assumptions are unspecified.

**Limits:** No accuracy, runtime, memory traffic, energy, or graph results are reported.

Recomputation may trade memory for compute unpredictably.

Official description only; workload and hardware validation is required.

**Method or artifact:** Operator recomputation and fission framework.

**Metrics:** Graph execution efficiency is claimed qualitatively

**Problem:** Computation graphs can be memory-bound, and recomputation or fission may improve attainable arithmetic intensity.

**Workload or benchmark:** DNN or general computation graphs; models, hardware, and memory hierarchy are unspecified.

</details>

## What remains to establish

Resolve unspecified workloads, comparison methods, resource budgets, and source locations before generalizing a reported gain. Multiple papers in this selected sample permit comparison of mechanisms, but do not by themselves establish recurrence across years or a long-term trend.

[All subthemes](../expanded-taxonomy-v1.md) · [Research directions](../directions/README.md)
