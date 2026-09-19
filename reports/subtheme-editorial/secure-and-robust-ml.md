## Four security problems require four different success conditions

This subject includes malicious image patches, information leakage from encrypted execution, deliberate changes to model-weight bits, and fault detection during encrypted arithmetic. The protected object differs in each case: prediction behavior, input confidentiality, model and action integrity, or correct execution under faults.

An attack succeeds only relative to a stated objective and access model. A defense against an altered image does not imply protection against modified weights. Encryption that hides values does not by itself establish correct execution. A final answer that looks unchanged does not establish that the system invoked only authorized tools along the way.

The discussion below separates the papers' evidence from independent conceptual reasoning. Two version-1 manuscripts were recovered. The other two records remain supported by official descriptions without paper-page experimental conditions.

## STRAP-ViT: alter suspicious image representations during inference

A vision transformer converts image regions into numerical vectors called tokens. Attention combines information across tokens. A localized adversarial patch is an intentionally chosen image modification intended to produce an incorrect prediction. Even a spatially small change can affect later computations that combine information globally.

[STRAP-ViT](../observed-subthemes/secure-and-robust-ml.md#paper-dac-2026-research1613) scores token distributions using Jensen–Shannon divergence and applies randomized transformations to selected tokens. Its version-1 manuscript evaluates ViT-base-16 and DINOv2 on ImageNet and Caltech-101 (Section IV, PDF pages 5–6). Table II includes clean-performance decreases, contrary to an unconditional reading of the no-clean-loss headline. The extracted table also reports 100.3% ImageNet Top-5 accuracy for one defended 45×45-patch case; that impossible percentage requires source correction, not acceptance.

Section V-A, pages 6–7, describes an adaptive attack attempt and reports a decrease of no more than 15% from the clean baseline, without a detailed per-setting results table there. Section V-C gives operation-complexity reasoning rather than measured end-to-end runtime. Table IV mixes patch sizes across comparisons. These limits preclude a universal robustness or matched-cost ranking. [Version-1 manuscript, Sections IV–V](https://arxiv.org/pdf/2603.12688v1#page=5).

Jensen–Shannon divergence measures a difference between probability distributions. A large difference can identify unusual behavior, but unusual does not necessarily mean malicious. Natural image content can also be statistically distinctive. The reference distribution, selection threshold, and handling of false alarms are therefore part of the defense, not incidental details.

Randomization changes the transformation applied on different executions. Its value must be tested against an attacker who accounts for that distribution, not only against an attack optimized for one fixed execution. Increasing the number of modified tokens can remove more attack influence while also discarding useful image information. Clean quality, attacked quality, and repeated-run variability should all be measured.

<span id="explanation-dac-2026-research1613"></span>

### STRAP-ViT: token randomization must reduce attack success without destroying clean classification or assuming a fixed attacker

#### What the attack and defense operate on

A vision transformer divides an image into regions and represents those regions as tokens. Later attention layers combine token information, so a small image patch can influence many downstream computations. An adversarial patch is an input change chosen to cause a wrong prediction under a stated attack goal and access model.

STRAP-ViT scores token distributions using Jensen–Shannon divergence and applies randomized transformations to selected tokens. Jensen–Shannon divergence is a bounded comparison between probability distributions; it does not itself prove that a token is malicious. Natural image edges, unusual objects or distribution shifts can also produce a large difference from the reference. The reference population, threshold, selected-token count and transformation distribution are therefore part of the defense definition.

#### Why randomization changes the threat model

If the transformation is fixed, an attacker can optimize against that fixed operation. If it is random, each execution samples a different transformation. That may make a single attack less reliable, but an adaptive attacker can optimize expected loss over the distribution if the attacker can observe or estimate it. The evaluation must state whether the attacker knows the model, token score, threshold, randomization distribution and defense output.

Changing more tokens can remove more patch influence, but it can also remove clean image information. The defense therefore needs clean accuracy, attacked accuracy, false-positive selection rate, run-to-run variability, inference overhead and behavior across patch sizes. Robustness without clean-performance and cost measurements is not a complete defense claim.

#### How to read the manuscript results

The recovered manuscript evaluates ViT-base-16 and DINOv2 on ImageNet and Caltech-101. Table II includes clean-performance decreases, so the method should not be summarized as having no clean-accuracy cost. One extracted defended 45×45-patch entry reports 100.3% ImageNet Top-5 accuracy, which is impossible as an ordinary percentage and must be corrected against the source rather than accepted as evidence.

Section V-A describes an adaptive attack attempt and reports a decrease of no more than 15% from the clean baseline, but does not provide a complete per-setting table there. Table IV mixes patch sizes across comparisons. Section V-C provides operation-complexity reasoning rather than measured end-to-end runtime. These conditions prevent a universal robustness or matched-cost ranking.

An adequate evaluation should fix the model, dataset, patch size, attack budget, attacker knowledge, clean target and randomization distribution. It should report attack success, clean accuracy, false-positive rate, selected-token fraction, repeated-run variance, latency, memory and energy, including an adaptive attacker that differentiates through or estimates the randomized defense where applicable.

The manuscript-backed evidence supports token scoring and randomized transformation as a defense direction with selected results. It does not establish universal patch robustness, zero clean cost, measured end-to-end efficiency or a corrected interpretation of the impossible 100.3% entry.

[Observed paper card](../observed-subthemes/secure-and-robust-ml.md#paper-dac-2026-research1613)

## CipherShield: encrypted values can still produce observable patterns

A trusted execution environment restricts what specified outside components can access. A side channel uses observable behavior that remains available despite that restriction. The relevant question is not simply whether an attacker can decrypt a value, but whether repeated observations reveal information about the value or its use.

[CipherShield](../observed-subthemes/secure-and-robust-ml.md#paper-dac-2026-research1764) targets CipherSteal-style ciphertext patterns through block-based processing, sparsity, and quantization transformations without replacing the cryptographic scheme. The official description reports ciphertext hit rates falling from 50–80% to nearly zero, a MNIST classification result falling from about 68% to as low as 2%, and over 20× shorter encryption time than an original trace-based method. In context, the falling classification result concerns leakage exploitation; it must not be advertised as improved legitimate-model accuracy. The exact classification protocol, hit-rate denominator, comparison boundary, and retained task quality require the missing manuscript. [Official DAC description](https://63dac.conference-program.com/presentation/?id=RESEARCH1764&sess=sess152).

A repeated ciphertext pattern may provide a relation between observations without revealing the underlying value directly. Breaking one such relation can obstruct a particular inference method. It does not establish zero information leakage through timing, addresses, other ciphertext features, or additional observations.

Likewise, a hit rate is a measurement of a defined matching event, not automatically a quantity of information in bits. An attacker may learn from patterns that the chosen counter does not record. Evaluation should distinguish the measured signal, an attack's success using that signal, and any broader security argument. All three matter, but they are different evidence.

<span id="explanation-dac-2026-research1764"></span>

### CipherShield: breaking a ciphertext pattern is narrower than proving an encrypted inference is confidential

#### What a ciphertext side channel is

Encryption transforms a value so that an observer without the key should not recover the protected value. A side channel uses other observable behavior: repeated ciphertext structure, length, timing, memory access, traffic, resource use or a relation between repeated inputs. A trusted execution environment can restrict direct access while still leaving some of these observations visible.

CipherShield targets CipherSteal-style ciphertext patterns through block processing, sparsity and quantization transformations without replacing the cryptographic scheme. The method must state which representation is transformed, whether the transformation is exact or approximate, what metadata is exposed and which observations the attacker receives.

#### What the reported hit rate means

A ciphertext hit rate is a count of a defined matching or inference event. The official description reports rates falling from 50–80% to nearly zero. That can show that the selected pattern-matching attack became less effective under the stated protocol. It does not establish zero leakage through timing, addresses, access order, ciphertext length, other statistical features or additional observations.

The evaluation must define the denominator, number of observations, input distribution, attack training data, test data, threshold and false-positive behavior. It should test attackers that use more than the one pattern being targeted and should state whether the TEE hides or exposes memory and execution behavior.

#### Why the classification number must not be misread

The description also reports a MNIST classification result falling from about 68% to as low as 2%. In context, this is the attack's ability to exploit the observed ciphertext pattern, not a claim that legitimate DNN inference accuracy improved or remained unchanged. A defense evaluation must report both attack success and the protected system's intended task accuracy under the same input and model conditions.

The description reports encryption time over 20× shorter than an original trace-based method. That comparison is meaningful only after defining whether it includes transformation, encryption, metadata, memory movement, enclave transitions and decryption, and whether both methods implement the same security and output-quality target. Faster encryption is not a security proof.

An adequate assessment should include leakage traces, attack success, legitimate accuracy, false alarms, latency, memory, energy, cryptosystem parameters, observation channels and repeated-input experiments. It should test timing, address, cache, ciphertext, length and traffic observations separately and in combination where the threat model allows them.

The captured DAC description supports a transformation against a named ciphertext-pattern attack. It reports no complete leakage trace, observation model, denominator, legitimate-task quality, latency, energy or broader adversarial result. The evidence supports a narrow side-channel defense direction, not a general confidentiality or TEE security guarantee.

[Observed paper card](../observed-subthemes/secure-and-robust-ml.md#paper-dac-2026-research1764)

## Flip-Agent: model integrity and tool authorization are separate controls

An agent uses model outputs to select subsequent computation or external actions. If a model parameter changes, an intermediate choice can change even when an eventual text answer remains plausible. Checking only the final text can therefore miss an integrity failure earlier in execution.

[Targeted Bit-Flip Attacks on LLM-Based Agents](../observed-subthemes/secure-and-robust-ml.md#paper-dac-2026-research797) presents Flip-Agent. Its threat model assumes full model/workflow knowledge and precise selected-bit changes, but not direct prompt editing; it studies single-agent systems (Section 2, PDF page 2). Sections 5.1–5.2, pages 4–6, use eight-bit models and a 50-bit budget on WebShop and ToolBench. Table 2's internal-trigger success ranges from 22.2% to 94.4%; Table 3's invocation results range from 67.3% to 100%, so prompt-level results do not describe every attack setting.

“Clean data accuracy” means agreement with the original agent's output, not independently verified task correctness. For invocation attacks, that agreement is assessed regardless of trigger presence. Precise fault placement is assumed, not established as a general remote capability. The comparison uses adapted vision-oriented bit-flip baselines; it does not establish superiority over every attack family. [Version-1 manuscript, threat model and Tables 1–3](https://arxiv.org/pdf/2603.10042v1#page=2).

This distinction motivates defense in more than one place. Protecting stored model state addresses unauthorized parameter changes. Independently checking whether a requested tool action is permitted addresses the consequences of an incorrect model decision. A tool call can be syntactically valid yet unauthorized for the user's task, so parsing alone is not an authorization check.

Such controls are independent design implications, not evaluated defenses established by this paper. A complete assessment must identify where model state is trusted, where action permission is enforced, and what evidence records the action actually performed. A model's statistical accuracy cannot substitute for those boundaries.

<span id="explanation-dac-2026-research797"></span>

### Flip-Agent: targeted model faults can change agent actions, but output agreement is not task correctness or a remote-attack claim

#### What a bit flip changes

An LLM agent uses model parameters and intermediate state to choose text, tools or later computation. A bit flip changes a binary representation in model storage, memory or computation. The effect depends on the selected bit, its numerical significance, the model's representation, when the fault occurs and whether the changed value persists.

A targeted attack therefore has two parts: reaching or controlling a fault location and choosing a change that produces a desired behavior. A result under precise bit placement is evidence about the model's sensitivity under that capability. It is not by itself evidence that an attacker can perform the same placement remotely or through an ordinary prompt.

#### The two attack outcomes are different

An internal-trigger attack makes a changed behavior occur when a condition is present. An invocation attack targets whether the agent selects a tool or action. These events occur at different points in the agent workflow and have different denominators. A high success rate for one cannot be used as the result for the other.

The manuscript's “clean data accuracy” means agreement with the original agent output. It does not mean that the original output was independently correct, that the tool call was authorized, or that the agent achieved the user's task. For tool-using agents, evaluation must record the requested action, the action selected, the arguments, the authorization decision and the final task result separately.

#### What the manuscript conditions establish

The recovered manuscript studies single-agent systems with full model/workflow knowledge and precise selected-bit changes, but not direct prompt editing. Sections 5.1–5.2 use eight-bit models and a 50-bit budget on WebShop and ToolBench. Internal-trigger success ranges from 22.2% to 94.4%, while invocation results range from 67.3% to 100%. These ranges describe multiple settings, not one universal attack rate.

The comparisons use adapted vision-oriented bit-flip baselines. The result therefore depends on the bit budget, model representation, target selection, task, trigger, tool interface and fault-placement assumption. A complete security claim would vary access path, bit persistence, model size, quantization, memory protection, task and attacker knowledge, and would include unsuccessful or harmful outcomes.

#### Integrity and authorization require separate checks

Protecting model storage or detecting parameter changes addresses model integrity. Checking whether a requested tool action is allowed addresses authorization. A model can be statistically accurate while selecting an unauthorized action, and a syntactically valid tool call can still violate the user's task or policy. These controls should be evaluated independently and connected to an audit record of the action actually performed.

The manuscript-backed evidence supports targeted bit-flip attack analysis under its stated threat model. It does not establish a remote attack, general transfer across agents, persistence, universal tool misuse or an evaluated mitigation.

[Observed paper card](../observed-subthemes/secure-and-robust-ml.md#paper-dac-2026-research797)

## Runtime-ADAR: inspect encrypted computation without equating noise with attack

Homomorphic encryption permits specified calculations on encrypted values. Depending on the scheme, internal noise and numerical approximation must remain within conditions needed for usable decryption. This differs from executing ordinary arithmetic inside an isolated environment; the two security models should not be merged under the word “encrypted.”

[Runtime-ADAR](../observed-subthemes/secure-and-robust-ml.md#paper-dac-2026-research821) targets faults in homomorphically encrypted neural-network acceleration. The description proposes noise-based statistical detection using sparse projections and a gradient-field weight-compensation mechanism in the ciphertext domain. It reports mitigating over 90% of attack successes and restoring up to 97% of baseline accuracy on evaluated models, with qualitative overhead claims. The cryptosystem, legitimate noise distribution, attack set, false-alarm rate, compensation rule, and decryption-validity conditions remain unspecified. Restoring 97% of baseline accuracy is not necessarily achieving 97% absolute accuracy or exactly repairing weights. [Official DAC description](https://63dac.conference-program.com/presentation/?id=RESEARCH821&sess=sess150).

A detector must separate acceptable execution variability from harmful deviations. A threshold that detects more deviations may also reject more legitimate work. Conversely, a low false-alarm rate may leave some harmful changes undetected. Report both rates under defined distributions, together with what happens before detection and during recovery.

Compensation changes computation to recover useful behavior; exact repair restores the intended state. Those goals can overlap, but application accuracy alone does not establish exact restoration. A recovery mechanism also needs a response when it cannot confidently recover: accepting an uncertain result and explicitly rejecting it have different security consequences.

<span id="explanation-dac-2026-research821"></span>

### Runtime-ADAR: encrypted-runtime detection must distinguish valid noise from attack and treat recovery as a separate correctness claim

#### Why encrypted execution has a special baseline

Homomorphic encryption permits computation on ciphertexts without first exposing the plaintext, but the computation can add scheme noise and numerical approximation. The noise has a budget: if it grows too far, decryption may fail or the result may lose the required accuracy. This legitimate variation is part of normal execution and cannot automatically be labeled an attack.

An attack can also alter encrypted computation, inputs, weights or intermediate behavior. A runtime detector must define what it observes, what distribution is normal, which attacks are in scope and which false alarms are acceptable. A detector that sees only a projection of the ciphertext may miss a change outside that projection or may reveal information through its own output.

#### What Runtime-ADAR proposes

The description proposes noise-based statistical detection using sparse projections and a gradient-field weight-compensation mechanism in the ciphertext domain. Detection estimates whether an observed execution deviates from an expected distribution. Compensation then changes computation to recover useful output behavior.

Those are different claims. Detection asks whether an anomaly is identified. Compensation asks whether the output improves after a response. Exact repair would require restoring the intended model or computation state, which is stronger than obtaining a similar output on one test set. The method must specify the detector threshold, projection, update rule, recovery trigger, cryptosystem noise budget and decryption-validity check.

#### How to read the reported outcomes

The official description reports mitigating over 90% of attack successes and restoring up to 97% of baseline accuracy on evaluated models, with qualitative overhead claims. “97% of baseline accuracy” is a relative recovery statement; it is not necessarily 97% absolute accuracy and does not establish exact weight repair. The attack denominator, baseline accuracy, model set, cryptosystem, false-alarm rate and recovery cost are not supplied.

A complete evaluation should report attack detection and recovery separately, including true-positive and false-positive rates, detection latency, recovery latency, decryption success, absolute and relative task accuracy, ciphertext noise growth, memory, energy and overhead. It should test attacks that change inputs, weights, intermediate values or control flow, and should include benign executions near the noise budget.

The captured DAC description supports a noise-based detector and ciphertext-domain compensation direction for encrypted DNN inference. It reports no cryptosystem parameters, attack set, false-alarm rate, detection/recovery latency, decryption validity, energy or complete overhead. The evidence supports a research direction, not reliable encrypted-DNN resilience or exact repair.

[Observed paper card](../observed-subthemes/secure-and-robust-ml.md#paper-dac-2026-research821)

## A comparison must preserve the attacker and the measurement unit

These four papers cannot be ranked by placing their percentages in one column. Classification correctness, attack success, output agreement, and ciphertext matches use different denominators. Some desired quantities increase under protection; others decrease. Every result needs its own direction, population, and tested access assumptions.

The common research question is how to preserve useful machine-learning behavior while separately checking inputs, internal state, observations, and actions. This is a conceptual connection in the selected sample, not evidence that one defense provides complete protection or that a multi-year trend is established.

The recovered evidence supersedes the historical cards' missing-results statements. STRAP-ViT's above-100% extracted table entry, unresolved experiment details, missing CipherShield/Runtime-ADAR manuscripts, and independent reproduction remain open. No attacks or hardware fault injections were executed as part of this editorial review.
