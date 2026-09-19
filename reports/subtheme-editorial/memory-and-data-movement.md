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
