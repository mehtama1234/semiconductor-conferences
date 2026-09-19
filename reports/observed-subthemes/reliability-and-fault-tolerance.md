# Reliability and fault tolerance

This subject has 2 records in the selected sample. This page explains where it fits, then presents all captured paper evidence without shortening the measurements or limitations.

[Definitions used in the paper records](../reading-guide-v1.md)

## Understand the parent subject first

- [Power reliability and security](../themes/power-reliability-and-security.md)

## Correct data storage does not automatically imply correct in-memory computation

Memory-centered computation moves some operations closer to stored data. This can reduce transfers, but it changes which components participate in producing a result. A reliability argument must cover that computation path, not merely the ability to read back a stored value under ordinary memory operations.

The two records in this group address different mechanisms. PuDGhost studies interference during processing-using-DRAM operations on physical chips. The ECC-enabled PIM paper proposes an architecture combining error handling with computation scheduling. Their fault models and experimental evidence are not interchangeable.

## PuDGhost: neighboring data can affect a computed result

[PuDGhost](../observed-subthemes/reliability-and-fault-tolerance.md#paper-isca-2026-program-024) examines operations based on activating multiple DRAM rows simultaneously. The assumed computation depends on the intended operands within a column. The study reports that data in adjacent non-activated rows and in other concurrently computing columns can affect that result.

This matters because a computation can be wrong even when the assumed local operands appear correct. Testing only an isolated operation or a favorable surrounding pattern would miss the relevant interaction. Evaluation must vary both the intended input and the surrounding data that the implementation assumed irrelevant.

The author abstract reports experiments on 96 DDR4 chips from 12 modules. It reports up to 10% output impact from adjacent non-activated rows and up to 48% from concurrently computing columns for random inputs. These are maximum reported effects under the abstract's conditions, not universal failure probabilities for DRAM or for all memory-compute architectures.

The proposed countermeasures include screening unreliable columns and separating computation rows with dedicated rows. Screening can restrict usable resources; row separation can consume capacity. Those consequences need measurement alongside improved computation accuracy. The captured abstract does not provide screening time, reserved capacity, detailed operating-condition sweeps, or full application results.

The study supplies real-chip evidence for its examined mechanism. It does not establish that every DRAM generation or unrelated PIM design has the same vulnerability. Exact devices, operation sequences, input distributions, voltage, and temperature remain necessary conditions for interpreting transfer.

## ECC-enabled PIM: error handling shares resources with computation

[ECC Enabled Reliable and Performant Processing-in-Memory](../observed-subthemes/reliability-and-fault-tolerance.md#paper-isca-2026-program-009) proposes tailored error-correcting codes for bank-level PIM. An error-correcting code stores additional structure that enables specified error patterns to be detected or corrected. Detection identifies a problem; correction recovers the intended information within the code's supported conditions.

The institutional abstract describes multi-bit detection and rank-level correction, a Codeword Flip method for weak-cell errors associated with variable retention time, and odd-even bank pipelining. A bank is a memory subdivision that can participate in operations; a rank groups devices operated together. Moving correction work to a broader level can affect availability and scheduling of computation resources.

The abstract reports 90% PIM-unit utilization, up to 400 times lower silent-data-corruption likelihood over five years, and potential fourfold performance improvement over rankPIM in selected microbenchmarks. Silent corruption means an incorrect result escapes detection. Its estimated likelihood depends on the assumed fault process and observation horizon; the five-year wording must not be interpreted as five years of measured operation without supporting evidence.

Likewise, utilization is not application speedup, and selected microbenchmark performance is not a universal language-model inference result. Exact code layouts, fault probabilities, correction latency, area, energy, and application configurations are absent from the captured abstract.

## What connects the findings

One paper shows why physical computation behavior must be characterized; the other shows why protection overhead belongs in the architecture and schedule. The records do not demonstrate that the proposed ECC architecture addresses PuDGhost's particular interference. That connection would require matching error patterns, where they occur, and what the checker can observe.

A useful end-to-end study would report correct useful outputs under stated fault exposure, detection failures, recovery costs, lost capacity, and sustained throughput. It would distinguish measured device phenomena from modeled long-term probabilities. These papers motivate that evaluation but do not collectively prove fault-tolerant operation across all memory-compute systems.

## Compare the results carefully

First identify the inputs and required output quality. Then identify the limited resource: time, memory, communication, energy, circuit area, or correctness coverage. Ask which part of the method reduces that cost and which new cost it adds. Compare numbers only when the experiments hold these conditions sufficiently similar.

A conference description may explain the proposal while omitting the full experiment. An author preprint link may have been coded from its abstract. The source classification does not by itself establish that every table was read. Missing locations remain visible below.

## Complete captured evidence

These are evidence records, not substitutes for the explanations above. Each record preserves its problem, proposed method, measurements, comparison conditions, and source limits. A populated record does not establish that its mechanism has been fully explained or independently verified.

<span id="paper-isca-2026-program-024"></span>

### PuDGhost: Experimental Analysis of Computation Result Corruption in Processing-using-DRAM Operations on Real DRAM Chips and Implications for Future Systems

ISCA 2026 · Record: `isca-2026-program-024`

**Problem:**

Processing-using-DRAM assumes that each column's computation depends only on its own operands, but density scaling and neighboring-cell interference may violate that isolation and corrupt results.

**Mechanism / artifact:**

Empirical characterization of PuDGhost under simultaneous multiple-row activation, followed by cross-layer countermeasures including unreliable-column screening and compute-row layouts that separate active computation rows.

**Workload — the work tested:**

Processing-using-DRAM operations on real DDR4 chips, including random-input experiments and computation-accuracy evaluation; the abstract identifies matrix-vector multiplication as a target workload context.

**Hardware and manufacturing assumptions:**

Real DDR4 DRAM using simultaneous multiple-row activation; results depend on chip organization, density, row layout, input patterns, and operating conditions.

**Baseline — the comparison method:**

ideal column-isolated processing-using-DRAM behavior

uncorrected PuD operation without PuDGhost countermeasures

**Reported measurements:**

96 real DDR4 DRAM chips

12 DRAM modules

up to 10% output impact from adjacent non-activated rows

up to 48% output impact from concurrently computing columns

computation accuracy after countermeasures

**Limits on the conclusion:**

The evidence is an author preprint abstract; exact chip part numbers, voltage and temperature sweeps, full workload accuracy tables, screening cost, row-layout capacity cost, and transfer to other DRAM generations or PIM mechanisms require full-paper verification.

**Source and location**

Evidence tier: High primary preprint. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://arxiv.org/abs/2606.19119)

An exact page, section, or table location has not been recorded. Page-level verification remains open.

<span id="paper-isca-2026-program-009"></span>

### ECC Enabled Reliable and Performant Processing-in-Memory

ISCA 2026 · Record: `isca-2026-program-009`

**Problem:**

Processing-in-memory improves data locality but introduces reliability risks from variable-retention-time scaling errors, physical faults, and multi-bit errors that can cause silent data corruption or repeated rank-level correction overhead.

**Mechanism / artifact:**

A reliable bank-PIM architecture with tailored rank-level ECC, Codeword Flip masking for VRT weak cells, and odd-even bank pipelining to preserve utilization while limiting correction interference.

**Workload — the work tested:**

PIM microbenchmarks and end-to-end LLM application evaluation; the institutional abstract reports comparisons with rankPIM and traditional bank-PIM.

**Hardware and manufacturing assumptions:**

Bank-level PIM integrated with modern DRAM, variable-retention-time weak cells, rank-level correction, and an odd-even bank pipeline; exact DRAM generation, fault distributions, and implementation cost require full-paper verification.

**Baseline — the comparison method:**

traditional bank-PIM configuration

rankPIM

**Reported measurements:**

90% PIM-unit utilization

up to 400x lower five-year silent-data-corruption likelihood

potential 4x performance enhancement over rankPIM in selected microbenchmarks

end-to-end LLM performance improvement

**Limits on the conclusion:**

The evidence is an institutional publication record containing the abstract and DOI metadata, not a captured full paper. Exact ECC layouts, fault probabilities, correction latency, area/energy overhead, LLM configurations, and the meaning of the reported likelihood horizon require full-paper verification.

**Source and location**

Evidence tier: Medium institutional abstract. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://cris.technion.ac.il/en/publications/ecc-enabled-reliable-and-performant-processing-in-memory/)

An exact page, section, or table location has not been recorded. Page-level verification remains open.

## What remains to establish

Resolve unspecified workloads, comparison methods, resource budgets, and source locations before generalizing a reported gain. Multiple papers in this selected sample permit comparison of mechanisms, but do not by themselves establish recurrence across years or a long-term trend.

[All subthemes](../expanded-taxonomy-v1.md) · [Research directions](../directions/README.md)
