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
