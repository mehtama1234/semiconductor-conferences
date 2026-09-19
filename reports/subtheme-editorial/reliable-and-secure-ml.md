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
