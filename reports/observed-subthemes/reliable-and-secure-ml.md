# Reliable and secure ml

This subject has 4 records in the selected sample. This page explains where it fits, then presents all captured paper evidence without shortening the measurements or limitations.

[Definitions used in the paper records](../reading-guide-v1.md)

## Understand the parent subject first

- [Power reliability and security](../themes/power-reliability-and-security.md)

## Reliability starts with a fault and an acceptable outcome

A neural network stores weights and computes intermediate values called activations. A hardware fault can change either. The numerical effect depends on which bit changes, where the value is used, and how later operations transform it. A changed bit need not change the final prediction, but an unchanged average accuracy does not mean every execution was correct.

This grouping contains four reliability proposals. The available evidence concerns accidental computational or storage faults, not demonstrated resistance to a deliberate attacker. Its existing “secure” label should not extend those conclusions to confidentiality, maliciously chosen faults, or unauthorized model changes.

Three distinctions organize the subject. Detection identifies a possible error. Exact correction restores the intended value within a stated fault model. Approximate recovery instead seeks an acceptable application result, which can differ from the fault-free result. A useful comparison must state which of these is required before measuring its cost.

The explanations below use refreshed official descriptions and a recovered DRIFT manuscript. They supersede conflicting omissions in the original cards, which still need source-record reconciliation. Missing manuscripts and experiments remain explicit rather than being filled from titles.

<span id="explanation-dac-2026-research2307"></span>

## STAC: an unusual activation is not necessarily an error

Language-model inference normally begins by processing the supplied prompt, a phase called prefill. It then produces additional tokens through repeated decoding steps. These phases have different execution shapes: prefill processes the known sequence, while decoding repeatedly extends it. A rule for expected intermediate values need not behave equally well in both phases.

[STAC](../observed-subthemes/reliable-and-secure-ml.md#paper-dac-2026-research2307) distinguishes these phases when protecting activations. The official description says its spatial component preserves large, useful activation outliers during prefill, while its token-predictive temporal component follows changing activation behavior during decoding. It reports qualitative improvements over static defenses, but provides no numerical fault coverage, false-alarm rate, model list, timing result, or page-backed algorithm here. Its “negligible overhead” claim remains unquantified. [Official DAC description](https://63dac.conference-program.com/presentation/?id=RESEARCH2307&sess=sess171).

An outlier is a value far from the values normally observed around it. That is a statistical description, not a fault diagnosis. Some large values carry legitimate information. A detector that simply removes every large activation can damage clean inference; one that permits every large value can miss faults that produce extreme magnitudes.

Spatial context asks whether a value is consistent with other relevant values in the current computation. Temporal context asks whether it is consistent with the execution's recent behavior. Both can improve discrimination, but both need an explicit reference and threshold. A temporal reference can also become misleading after a real change in the input or after an earlier undetected fault. The available evidence supports contextual activation protection, not a general reliable-LLM guarantee.

The important evaluation would separate clean false alarms, detected harmful errors, missed harmful errors, and harmless changes, and report clean and faulted accuracy, latency, and energy. It should test prompt lengths and decoding lengths independently, including abrupt changes in content. A detector that works well on short, familiar inputs does not thereby establish reliable long-sequence generation.

<span id="explanation-dac-2026-research374"></span>

## Selective temporal redundancy: repeat the work that needs protection

Temporal redundancy repeats a calculation at different times. In this setting, temporal redundancy is a selective protection mechanism rather than a universal repair operation. A disagreement between two executions can reveal a fault, but two disagreeing values do not by themselves identify the correct one. Recovery needs another check, another execution, or a separately justified rule. Repetition also provides weaker protection when the same persistent fault affects both executions.

[Sparsity- and Tolerance-Aware Temporally Redundant Neural Networks](../observed-subthemes/reliable-and-secure-ml.md#paper-dac-2026-research374) combines selective repetition with sparse outer-product computation. Its description uses a bound on single-bit-flip effects in residual-quantized dot products to identify vulnerable calculations. A zero-skipping unit exploits activation zeros to offset repetition cost. The reported implementation comparison gives 16.0% speedup over a non-fault-tolerant model with 0.20–1.26% area overhead.

The description does not supply the bound, network configurations, fault coverage, manufacturing process, latency, energy, or whether the reported implementation was fabricated. The low-Earth-orbit motivation is not evidence of a flight experiment. The speedup combines changed computation with protection; it does not mean repetition alone makes a fixed calculation faster. [Official DAC description](https://63dac.conference-program.com/presentation/?id=RESEARCH374&sess=sess124).

A dot product multiplies corresponding entries of two lists and adds them. An outer product instead multiplies each entry of one list by each entry of another, producing an array. Matrix multiplication can accumulate these outer products. When an operand is zero, its products are zero and suitable hardware can skip them, subject to the cost of finding and scheduling the nonzero work.

Residual quantization represents a value through a coarse approximation and further information about the remaining difference. In this paper, residual quantization determines which bit changes have large numerical effects. A bound for one bit change should not be silently extended to simultaneous changes, correlated faults, or a different representation.

To isolate the benefit, compare four configurations at matched output quality and accuracy: the original computation, sparsity optimization alone, protection alone, and their combination. Otherwise, the reader cannot tell whether a reported gain comes from fault handling or from a faster underlying execution method. The evidence supports selective redundancy, not general fault tolerance.

<span id="explanation-dac-2026-research800"></span>

## E³-CODE: use weight representation space for error protection

An error-correcting code restricts which bit patterns are valid and uses those restrictions to identify certain corrupted patterns. Check bits, often called parity bits, encode relationships among the protected bits. More protection normally requires additional representation capacity or stronger restrictions on the data that can be represented.

[E³-CODE](../observed-subthemes/reliable-and-secure-ml.md#paper-dac-2026-research800) embeds multiple parity bits across weight representations rather than using only their least-significant positions. It jointly selects weights and parity through mixed-integer linear programming, and also proposes a hybrid with conventional error correction. The official description reports ResNet, MobileNetV2, and EfficientNet-B0 evaluations on ImageNet and CIFAR-10 under burst errors, with claimed system-lifetime extensions of 4.8× without extra memory and 10× with less than 2% extra memory.

The underlying lifetime model, error process, failure threshold, code parameters, decoder behavior, decoding cost, and page-backed results are not available in the recovered description. These multipliers must not be presented as observed years of device operation. No extra memory also does not mean no accuracy, computation, or design-time cost. The description supports a representation-aware ECC direction, not observed years of operation. [Official DAC description](https://63dac.conference-program.com/presentation/?id=RESEARCH800&sess=sess158).

Embedding check information in an existing weight representation changes the allocation of its finite bit capacity. The model may tolerate some resulting numerical changes, but that tolerance must be measured. Correcting the encoded representation and preserving the original unmodified weights are different requirements.

Mixed-integer linear programming expresses numerical constraints and choices, some restricted to integers, and searches for an assignment satisfying them. A solver's output is only as appropriate as its objective and constraints. Optimizing numerical weight error, for example, would not automatically optimize every downstream application's quality.

A burst error changes a cluster of bits. Protection depends on how physical storage locations correspond to codewords, which are the groups encoded together. The same total number of changed bits can be correctable when spread across groups and uncorrectable when concentrated in one. Report fault coverage for these distributions. Lifetime comparisons therefore need the storage mapping and error clustering, not only a mean bit-error rate.

<span id="explanation-dac-2026-research816"></span>

## DRIFT: tolerate some timing errors and replace selected damaged values

Circuits need time for their outputs to settle. Lowering voltage can increase that time; increasing clock frequency reduces the time available. Either change can produce timing errors if taken beyond the circuit's safe operating conditions. Saving energy or time then requires accounting for errors and their recovery, not just changing the operating setting.

[DRIFT](../observed-subthemes/reliable-and-secure-ml.md#paper-dac-2026-research816) selectively changes voltage or frequency and replaces large-error activations with checkpointed values from earlier diffusion steps. This is approximate substitution, not exact recomputation. Sections 3 and 5, PDF pages 3–4, assume error-free memory retrieval, inject uniform random bit flips into 32-bit outputs of eight-bit operations, and treat cancelling checksum errors as statistically negligible.

Section 6, pages 5–6, uses 14 nm synthesis and SCALE-Sim, not a reported fabricated accelerator. Nominal operation is 0.9 V/2 GHz. The first two denoising steps and timestep embedding retain nominal settings. Other work uses either 0.68 V/2 GHz for energy evaluation or 0.88 V/3.5 GHz for speed evaluation, targeting a bit-error rate near 0.003. The average 36% energy reduction and 1.7× speedup therefore describe different operating points.

Table 1 covers DiT, PixArt, and Stable Diffusion configurations. Quality scores stay close but are not identical; perceptual differences remain. These results support bounded quality preservation under the tested model, not fault-free execution or general attacker resistance. [Version-1 manuscript, Sections 3, 5–6 and Table 1](https://arxiv.org/pdf/2604.09073v1#page=3).

A diffusion model repeatedly updates an image representation. Earlier and later values can be similar without being interchangeable. Substituting an old value may avoid a large corruption while discarding a useful update. The acceptable checkpoint age consequently depends on the computation and quality criterion.

Checksums summarize relationships among numerical results. They can detect many violations efficiently, but different errors can sometimes cancel in a summary. A low probability under independent random errors is not a guarantee under correlated or intentionally selected errors. The fault model is part of the result.

Image-quality metrics also answer different questions. Similarity to a fault-free image, agreement with a prompt, and aggregate quality across generated samples are distinct. An unchanged average score can coexist with rare severe failures. Reliability evaluation should retain the distribution of outcomes and the proportion of unacceptable outputs, not only a mean.

## The shared direction is selective protection, not universal fault tolerance

These cases suggest a common design question: where does additional protection prevent enough application harm to justify its cost? The answer can depend on phase, bit representation, sparsity, storage layout, and iteration. This is a conceptual connection across the selected papers, not proof of growth across years or a single interchangeable technique.

A convincing long-term study would preserve fault locations and distributions, clean and faulty output criteria, and full protection costs across comparable model generations. It would also test whether conclusions survive correlated faults, longer executions, and changes in input distribution.

The strongest next experiments would isolate each protection mechanism, measure both clean and faulty cases, and include failures in the protection machinery itself. A reliable detector, checkpoint, or decoder cannot simply be assumed because the arithmetic it protects is unreliable. Until those boundaries are established, efficiency gains should remain attached to their tested conditions.

## Compare the results carefully

First identify the inputs and required output quality. Then identify the limited resource: time, memory, communication, energy, circuit area, or correctness coverage. Ask which part of the method reduces that cost and which new cost it adds. Compare numbers only when the experiments hold these conditions sufficiently similar.

A conference description may explain the proposal while omitting the full experiment. An author preprint link may have been coded from its abstract. The source classification does not by itself establish that every table was read. Missing locations remain visible below.

## Complete captured evidence

These are evidence records, not substitutes for the explanations above. Each record preserves its problem, proposed method, measurements, comparison conditions, and source limits. A populated record does not establish that its mechanism has been fully explained or independently verified.

<span id="paper-dac-2026-research2307"></span>

### STAC: Spatial-Temporal Activation Contextualization for Resilient LLM Inference

DAC 2026 · Record: `dac-2026-research2307`

[Read the step-by-step explanation](#explanation-dac-2026-research2307)

**Updated source-backed reading card**

Reviewed 2026-09-08. Deepens the existing STAC treatment into a paper-level reading; separates spatial/temporal activation context from fault detection, false alarms, missed errors, phase-specific behavior and end-to-end inference cost, while preserving the qualitative source boundary.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

LLM inference can be sensitive to activation faults or variation across spatial and temporal execution contexts.

**Mechanism / artifact:**

Spatial-temporal activation contextualization for resilient inference, with spatial treatment of useful activation outliers and token-predictive temporal treatment during decoding; context reference, detector, thresholds, fault model and hardware path are unspecified.

**Workload — the work tested:**

LLM inference under faults or variation; models, prefill/decode lengths, activation distributions, error injection, clean/faulted criteria, prompt distribution and evaluation split are unspecified.

**Hardware and manufacturing assumptions:**

Accelerator with spatially and temporally varying activation behavior; precision, memory, timing, checker placement, fault location/persistence, latency, energy and hardware implementation assumptions are unspecified.

**Baseline — the comparison method:**

Unprotected LLM inference

Static activation protection

Phase-specific fault distributions, clean false-alarm baseline, same model/prompt/sequence lengths, detector cost and hardware boundary are unspecified

**Reported measurements:**

Inference resilience and negligible overhead are claimed qualitatively; no accuracy loss, harmful-error coverage, false-alarm/missed-error rate, fault rate, latency, energy, memory or hardware result is reported.

**Limits on the conclusion:**

An activation outlier is a statistical observation, not proof of a fault. Legitimate large values can carry information, while a fault need not always produce an extreme value. Spatial and temporal references require defined context, thresholds and behavior under abrupt prompt or phase changes.

Prefill and decoding have different execution shapes, so evaluation must separate them and test prompt length, generation length, content shifts, persistent/transient faults and false alarms. A periodic check may allow a corrupted activation to affect inference before detection.

No accuracy loss, fault rate, detection coverage, latency, energy, or hardware results are reported. Resilience depends on fault and workload distributions; the evidence supports contextual activation protection, not a general reliable-LLM guarantee.

**Source and location**

Evidence tier: Primary captured official DAC description plus existing chapter level stac discussion; no full paper extraction, reproduced detector, fault injection matrix or hardware validation. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH2307)

DAC 2026 official description; existing chapter-level STAC discussion; captured Problem, Mechanism / artifact, Workload, Hardware, Baseline, Measurements and Limits fields; no manuscript pages.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** unprotected LLM inference

static activation protection

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH2307

**Hardware or process assumptions:** Accelerator with spatially and temporally varying activation behavior; fault and precision assumptions are unspecified.

**Limits:** No accuracy loss, fault rate, latency, energy, or hardware results are reported.

Resilience depends on the fault and workload distributions.

Official description only; fault-injection validation is required.

**Method or artifact:** Spatial-temporal activation contextualization for resilient inference.

**Metrics:** Inference resilience is claimed qualitatively

**Problem:** LLM inference can be sensitive to activation faults or variation across spatial and temporal execution contexts.

**Workload or benchmark:** LLM inference under faults or variation; models, error injection, and hardware are unspecified.

</details>

<span id="paper-dac-2026-research374"></span>

### Sparsity- and Tolerance-Aware Temporally Redundant Neural Networks

DAC 2026 · Record: `dac-2026-research374`

[Read the step-by-step explanation](#explanation-dac-2026-research374)

**Updated source-backed reading card**

Reviewed 2026-09-08. Deepens the existing sparsity/tolerance-aware temporal-redundancy treatment into a paper-level reading; separates repetition, sparse outer-product execution, residual-quantization fault bounds, recovery correctness and implementation overhead, while preserving the official-description evidence limit.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Temporal redundancy can improve neural resilience but adds compute and memory cost.

**Mechanism / artifact:**

Sparsity- and tolerance-aware temporally redundant neural network design using selective repetition, residual-quantized fault sensitivity and zero-skipping outer-product computation; bound, selection rule, recovery semantics and hardware path are unspecified.

**Workload — the work tested:**

Neural inference under transient or persistent faults; models, precision/quantization, sparsity, outer-product mapping, fault locations/rates/correlation, output criterion and repeated trials are unspecified.

**Hardware and manufacturing assumptions:**

Accelerator supporting redundant temporal execution and zero-skipping; timing, memory, process, area, energy, fault injection, synchronization, persistent-fault and implementation/fabrication assumptions are unspecified.

**Baseline — the comparison method:**

Unprotected neural network

Full temporal redundancy

Sparsity-only, protection-only and combined configurations with equal model quality, fault distribution, precision, hardware, timing and output boundary are unspecified

**Reported measurements:**

16.0% speedup over a non-fault-tolerant model and 0.20–1.26% area overhead are reported; no accuracy, fault coverage, recovery correctness, latency, energy, memory, sparsity or fabrication result is supplied.

**Limits on the conclusion:**

Temporal disagreement detects a possible fault but does not identify the correct value; repeated executions can share a persistent or correlated fault. A single-bit bound for residual-quantized arithmetic cannot be extended to multiple, correlated or differently represented faults without evidence.

Zero-skipping may offset redundancy cost, but the combined speedup must be decomposed into sparsity, scheduling, repetition and recovery overhead. Compare original, sparsity-only, protection-only and combined systems at matched output quality.

No accuracy, fault coverage, latency, energy, area, or sparsity results are reported. Tolerance depends on fault timing and correlation; the low-Earth-orbit motivation is not a flight experiment and the evidence supports a selective redundancy direction, not general fault tolerance.

**Source and location**

Evidence tier: Primary captured official DAC description plus existing chapter level temporal redundancy discussion; no full paper extraction, reproduced fault bound, implementation details or independent fault injection validation. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/presentation/?id=RESEARCH374&sess=sess124)

DAC 2026 official description; existing chapter-level temporal-redundancy discussion; captured Problem, Mechanism / artifact, Workload, Hardware, Baseline, Measurements and Limits fields; no manuscript pages.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** unprotected neural network

full temporal redundancy

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH374

**Hardware or process assumptions:** Accelerator supporting redundant temporal execution; timing and fault assumptions are unspecified.

**Limits:** No accuracy, fault coverage, latency, energy, area, or sparsity results are reported.

Tolerance depends on fault timing and correlation.

Official description only; fault-injection validation is required.

**Method or artifact:** Sparsity- and tolerance-aware temporally redundant neural network design.

**Metrics:** Fault-tolerant efficiency is claimed qualitatively

**Problem:** Temporal redundancy can improve neural resilience but adds compute and memory cost.

**Workload or benchmark:** Neural inference under transient or persistent faults; models, fault rate, and hardware are unspecified.

</details>

<span id="paper-dac-2026-research800"></span>

### E³-CODE: Embedded and Efficient Error-Correcting Code for Error-Resilient Neural Networks

DAC 2026 · Record: `dac-2026-research800`

[Read the step-by-step explanation](#explanation-dac-2026-research800)

**Updated source-backed reading card**

Reviewed 2026-09-08. Deepens the existing E³-CODE treatment into a paper-level reading; separates representation-level parity embedding, correction capability, model-quality tolerance, burst-error mapping, lifetime modeling and decoding/system overhead, while preserving the official-description evidence boundary.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Neural accelerators need compact error correction that preserves inference quality under faults.

**Mechanism / artifact:**

Embedded error-correcting code for neural-network data or computation, embedding multiple parity bits across weight representations, jointly selecting weights/parity with mixed-integer linear programming and offering a conventional-ECC hybrid; code parameters, decoder, mapping and optimization constraints are unspecified.

**Workload — the work tested:**

ResNet, MobileNetV2 and EfficientNet-B0 on ImageNet and CIFAR-10 under burst errors are reported; storage layout, codeword mapping, error process, bit rate/correlation, quality criterion, fault trials and model split are unspecified.

**Hardware and manufacturing assumptions:**

Accelerator with embedded ECC; memory technology, representation width, physical bit mapping, decoder placement, process, area, energy, latency, bandwidth, design-time solver cost and fault injection boundary are unspecified.

**Baseline — the comparison method:**

Uncorrected inference

Generic ECC

Hybrid ECC and no-extra-memory comparisons; equal code strength, representation, storage map, quality, decoder/system overhead, burst process and lifetime definition are unspecified

**Reported measurements:**

Claimed system-lifetime extensions of 4.8x without extra memory and 10x with less than 2% extra memory are reported; no fault coverage, accuracy, area, energy, latency, code rate, decoder cost, lifetime model or page-backed result is supplied.

**Limits on the conclusion:**

Embedding parity into an existing weight representation reallocates finite bit capacity and may change numerical weights. Correcting a corrupted encoded representation, preserving original weights and preserving application accuracy are separate requirements.

Burst-error protection depends on physical storage-to-codeword mapping and error clustering, not only mean bit-error rate. The lifetime multipliers require an explicit error process, failure threshold, code/decoder behavior, workload, confidence interval and operating condition.

The underlying lifetime model, error process, failure threshold, code parameters, decoding cost, and page-backed results are unavailable. The evidence supports representation-aware ECC direction, not observed years of operation, zero-cost protection, or general error-resilient inference.

**Source and location**

Evidence tier: Primary captured official DAC description plus existing chapter level e³ code discussion; no full paper extraction, reproduced code/decoder, lifetime model or independent fault injection validation. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/presentation/?id=RESEARCH800&sess=sess158)

DAC 2026 official description; existing chapter-level E³-CODE discussion; captured Problem, Mechanism / artifact, Workload, Hardware, Baseline, Measurements and Limits fields; no manuscript pages.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** uncorrected inference

generic ECC

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH800

**Hardware or process assumptions:** Accelerator with embedded ECC; memory and fault assumptions are unspecified.

**Limits:** No fault coverage, accuracy, area, energy, latency, or code-rate results are reported.

ECC may trade overhead against correction strength.

Official description only; fault-injection validation is required.

**Method or artifact:** Embedded error-correcting code for neural-network data or computation.

**Metrics:** Error resilience is claimed qualitatively

**Problem:** Neural accelerators need compact error correction that preserves inference quality under faults.

**Workload or benchmark:** Neural inference under transient or persistent faults; models, code rate, and hardware are unspecified.

</details>

<span id="paper-dac-2026-research816"></span>

### DRIFT: Harnessing Inherent Fault Tolerance for Efficient and Reliable Diffusion Model Inference

DAC 2026 · Record: `dac-2026-research816`

[Read the step-by-step explanation](#explanation-dac-2026-research816)

**Updated source-backed reading card**

Reviewed 2026-09-08. Deepens the existing DRIFT treatment using the recovered version-1 manuscript; separates timing-error generation, approximate checkpoint substitution, checksum assumptions, model-quality preservation and accelerator performance, and preserves the distinct operating points and non-fabricated boundary.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Diffusion inference is expensive and may tolerate selected hardware errors without full protection.

**Mechanism / artifact:**

Fault-tolerance-aware diffusion inference method that changes voltage/frequency and replaces selected large-error activations with checkpointed values from earlier diffusion steps; recovery trigger, checksum, checkpoint policy and fault coverage are bounded by the manuscript assumptions.

**Workload — the work tested:**

DiT, PixArt and Stable Diffusion configurations; uniform random bit flips in 32-bit outputs of eight-bit operations, error-free memory retrieval, target bit-error rate near 0.003, quality metrics and tested distributions are reported only within the selected manuscript scope.

**Hardware and manufacturing assumptions:**

14 nm synthesis and SCALE-Sim, not a reported fabricated accelerator; nominal 0.9 V/2 GHz, energy point 0.68 V/2 GHz, speed point 0.88 V/3.5 GHz, first two denoising steps and timestep embedding at nominal settings, with memory and checksum assumptions as specified in the manuscript.

**Baseline — the comparison method:**

Fully protected inference

Unprotected inference

Nominal and reduced-voltage/frequency operating points; same model, quality criterion, fault process, memory, checksum, checkpoint and energy/latency boundary are required for equal comparison

**Reported measurements:**

Average 36% energy reduction at 0.68 V/2 GHz and 1.7x speedup at 0.88 V/3.5 GHz are reported at different operating points; Table 1 covers DiT, PixArt and Stable Diffusion with close but non-identical quality scores. Fabrication, fault coverage and full quality distributions are not established.

**Limits on the conclusion:**

Checkpoint substitution is approximate recovery, not exact recomputation: an earlier diffusion value may avoid a large timing error while discarding a useful update. Acceptability depends on timestep, checkpoint age, model, prompt and quality metric.

The manuscript assumes error-free memory retrieval, injects uniform random bit flips into 32-bit outputs of eight-bit operations, and treats cancelling checksum errors as statistically negligible. These assumptions do not cover correlated, persistent, adversarial or memory faults without separate evidence.

The 36% energy and 1.7x speed results use different operating points, and the evaluation uses 14 nm synthesis/SCALE-Sim rather than a reported fabricated accelerator. The evidence supports bounded approximate tolerance under the tested models and fault process, not fault-free execution or general attacker resistance.

**Source and location**

Evidence tier: Recovered version 1 arxiv manuscript with selected method/evaluation inspection plus primary official DAC description; no reproduced hardware, independent fault campaign or security review. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://arxiv.org/pdf/2604.09073v1#page=3)

Version-1 manuscript Sections 3, 5–6 and Table 1, PDF pages 3–6; existing chapter-level DRIFT discussion; official DAC description; no fabricated accelerator evidence.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** fully protected inference

unprotected inference

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH816

**Hardware or process assumptions:** Accelerator with controllable or observed faults; fault model and precision assumptions are unspecified.

**Limits:** No image quality, fault rate, latency, energy, or hardware results are reported.

Tolerance may depend on timestep and model.

Official description only; fault-injection validation is required.

**Method or artifact:** Fault-tolerance-aware diffusion inference method.

**Metrics:** Reliable diffusion efficiency is claimed qualitatively

**Problem:** Diffusion inference is expensive and may tolerate selected hardware errors without full protection.

**Workload or benchmark:** Diffusion models; tasks, fault injection, quality metrics, and hardware are unspecified.

</details>

## What remains to establish

Resolve unspecified workloads, comparison methods, resource budgets, and source locations before generalizing a reported gain. Multiple papers in this selected sample permit comparison of mechanisms, but do not by themselves establish recurrence across years or a long-term trend.

[All subthemes](../expanded-taxonomy-v1.md) · [Research directions](../directions/README.md)
