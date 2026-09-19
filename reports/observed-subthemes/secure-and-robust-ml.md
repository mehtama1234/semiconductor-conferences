# Secure and robust ml

This subject has 4 records in the selected sample. This page explains where it fits, then presents all captured paper evidence without shortening the measurements or limitations.

[Definitions used in the paper records](../reading-guide-v1.md)

## Understand the parent subject first

- [Power reliability and security](../themes/power-reliability-and-security.md)

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

## Compare the results carefully

First identify the inputs and required output quality. Then identify the limited resource: time, memory, communication, energy, circuit area, or correctness coverage. Ask which part of the method reduces that cost and which new cost it adds. Compare numbers only when the experiments hold these conditions sufficiently similar.

A conference description may explain the proposal while omitting the full experiment. An author preprint link may have been coded from its abstract. The source classification does not by itself establish that every table was read. Missing locations remain visible below.

## Complete captured evidence

These are evidence records, not substitutes for the explanations above. Each record preserves its problem, proposed method, measurements, comparison conditions, and source limits. A populated record does not establish that its mechanism has been fully explained or independently verified.

<span id="paper-dac-2026-research1613"></span>

### STRAP-ViT: Segregated Tokens with Randomized Transformations for Defense Against Adversarial Patches in ViTs

DAC 2026 · Record: `dac-2026-research1613`

[Read the step-by-step explanation](#explanation-dac-2026-research1613)

**Updated source-backed reading card**

Reviewed 2026-09-08. Deepens the existing manuscript-backed STRAP-ViT treatment into a paper-level reading; preserves the clean-accuracy tradeoff, adaptive-attack boundary and the impossible 100.3% extracted entry as an unresolved source correction rather than an accepted result.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

A localized adversarial patch changes image inputs so that a vision transformer predicts an incorrect class, while the defense must preserve clean-image behavior.

**Mechanism / artifact:**

Token segregation using Jensen–Shannon divergence to identify unusual token distributions, followed by randomized transformations on selected tokens; selection threshold, reference distribution, transformation distribution and runtime are incompletely specified.

**Workload — the work tested:**

ViT-base-16 and DINOv2 on ImageNet and Caltech-101 in the recovered manuscript; patch sizes, attack budget, attack knowledge, clean split, adaptive attack procedure and per-setting tables are incompletely specified.

**Hardware and manufacturing assumptions:**

Vision-transformer inference with token scoring and randomized transformation; compute, memory, latency, random source and deployment hardware are unspecified.

**Baseline — the comparison method:**

Undefended ViT

Adversarial training

Attack and clean-evaluation settings vary across tables; matched cost and threat model are required

**Reported measurements:**

Manuscript-backed: clean-performance decreases appear in Table II; one extracted defended 45×45-patch entry reports 100.3% ImageNet Top-5 accuracy and requires source correction. Section V-A reports an adaptive-attack decrease of no more than 15% from the clean baseline; Section V-C gives operation-complexity reasoning rather than measured end-to-end runtime.

**Limits on the conclusion:**

Jensen–Shannon divergence measures a difference between probability distributions. A high token-distribution difference can identify an unusual token, but natural image content can also be unusual. The defense therefore needs a reference distribution, threshold, false-positive behavior and a defined transformation for tokens selected as suspicious.

Randomized transformation is a distribution over defenses, not a guarantee against an adaptive attacker. An attacker that observes or estimates the transformation can optimize expected loss through that distribution. Increasing the number of changed tokens may reduce attack influence while removing useful clean-image information.

The extracted 100.3% Top-5 entry is impossible as an ordinary percentage and must be corrected against the source before use. Patch sizes are mixed across comparisons, clean-performance tradeoffs exist, the adaptive-attack table is incomplete and runtime is reasoned rather than measured. The evidence supports a defense direction and selected results, not universal robustness or matched-cost superiority.

**Source and location**

Evidence tier: Recovered manuscript backed selected evaluation plus official DAC description; source correction, adaptive attacker reproduction and matched cost validation remain open. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://arxiv.org/pdf/2603.12688v1)

Manuscript v1, Sections IV–V, PDF pages 5–7; official DAC record RESEARCH1613; Table II, adaptive attack Section V-A and operation-complexity Section V-C; impossible 100.3% extracted Table II entry retained as unresolved source correction.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** undefended ViT

adversarial training

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH1613

**Hardware or process assumptions:** ViT inference with token transformations; runtime and accelerator assumptions are unspecified.

**Limits:** No attack success, clean accuracy, overhead, transferability, or adaptive-attacker results are reported.

Randomization may not defeat adaptive attacks.

Official description only; threat-model validation is required.

**Method or artifact:** Token segregation and randomized transformations for ViT defense.

**Metrics:** Patch robustness is claimed qualitatively

**Problem:** Vision transformers can be manipulated by localized adversarial patches.

**Workload or benchmark:** Vision-transformer classification or perception; datasets, attack budgets, and clean-accuracy targets are unspecified.

</details>

<span id="paper-dac-2026-research1764"></span>

### Ciphershield: Safeguarding DNN Inputs from Ciphertext Side-Channels in TEE

DAC 2026 · Record: `dac-2026-research1764`

[Read the step-by-step explanation](#explanation-dac-2026-research1764)

**Updated source-backed reading card**

Reviewed 2026-09-08. Deepens the existing CipherShield treatment into a paper-level reading; separates ciphertext-pattern matching from broader leakage, attack success from legitimate accuracy, and encryption-time comparisons from security guarantees.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Encrypted DNN inputs may reveal information through repeated ciphertext or execution patterns even when a trusted execution environment prevents direct plaintext access.

**Mechanism / artifact:**

TEE protection method using block-based processing, sparsity and quantization transformations to reduce CipherSteal-style ciphertext patterns without replacing the cryptographic scheme; exact transformation and security argument are unspecified.

**Workload — the work tested:**

Encrypted DNN inference with a reported MNIST classification attack result; cryptosystem, model, input distribution, attacker observations, platform and legitimate task target are unspecified.

**Hardware and manufacturing assumptions:**

Trusted execution environment with encrypted inputs and observable execution or ciphertext behavior; enclave, memory, timing, address, cache and network observation assumptions are unspecified.

**Baseline — the comparison method:**

Unenhanced TEE inference

Plaintext TEE inference

Original trace-based method for the reported encryption-time comparison; boundaries are unspecified

**Reported measurements:**

Official description reports ciphertext hit rates falling from 50–80% to nearly zero, a MNIST classification result falling from about 68% to as low as 2%, and encryption time over 20× shorter than an original trace-based method; denominator and comparison boundaries are unspecified.

**Limits on the conclusion:**

A ciphertext hit rate counts a defined matching event. Reducing that event can obstruct one inference method, but it does not prove that timing, memory addresses, access order, ciphertext length, other ciphertext features or repeated observations reveal no information.

The reported MNIST classification decrease concerns leakage exploitation in context, not legitimate-model accuracy. Evaluation must identify whether the classifier is the attack, what information it receives, its training and test protocol, and whether the protected DNN still meets its intended task quality.

The official description does not define the cryptosystem, attacker observation model, hit-rate denominator, trace method, encryption boundary, latency, memory, energy, false positives or broader leakage test. The record supports a transformation against a named side-channel pattern, not a general confidentiality or TEE security guarantee.

**Source and location**

Evidence tier: Primary captured official DAC description plus existing chapter level ciphershield discussion; no full paper extraction, adversarial trace reproduction or broader leakage validation. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH1764)

DAC 2026 official description; captured Problem, Mechanism / artifact, Workload, Hardware, Baseline, Measurements and Limits fields; record RESEARCH1764; no manuscript pages.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** unenhanced TEE inference

plaintext TEE inference

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH1764

**Hardware or process assumptions:** TEE with encrypted inputs and side-channel observables; enclave and memory assumptions are unspecified.

**Limits:** No leakage traces, attack success, accuracy, latency, or overhead results are reported.

Protection depends on the attacker observation model.

Official description only; adversarial validation is required.

**Method or artifact:** TEE protection method for DNN-input ciphertext side channels.

**Metrics:** Ciphertext side-channel protection is claimed qualitatively

**Problem:** Encrypted DNN inputs may leak through observable ciphertext or execution behavior even inside trusted execution environments.

**Workload or benchmark:** Encrypted DNN inference; cryptosystem, model, attacker observation, and platform are unspecified.

</details>

<span id="paper-dac-2026-research797"></span>

### Targeted Bit-Flip Attacks on LLM-Based Agents

DAC 2026 · Record: `dac-2026-research797`

[Read the step-by-step explanation](#explanation-dac-2026-research797)

**Updated source-backed reading card**

Reviewed 2026-09-08. Deepens the existing Flip-Agent manuscript treatment into a paper-level reading; separates model-state integrity, trigger and invocation outcomes, output agreement, attack access and tool authorization.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Targeted changes to model bits can alter an LLM agent's decisions or tool calls while leaving some ordinary outputs apparently unchanged.

**Mechanism / artifact:**

Targeted bit-flip attack methodology for LLM agents, including internal-trigger and invocation attacks; precise fault placement, model/workflow knowledge and selected-bit changes are assumed in the manuscript threat model.

**Workload — the work tested:**

Single-agent systems on WebShop and ToolBench; eight-bit models, a 50-bit attack budget and the manuscript's task and trigger settings; model, memory path, persistence and deployment conditions are limited.

**Hardware and manufacturing assumptions:**

Accelerator or memory system vulnerable to selected bit flips; attacker has precise fault-placement capability but not direct prompt editing under the stated threat model; hardware access path and persistence are unspecified.

**Baseline — the comparison method:**

Random bit flips

Software prompt attacks

Adapted vision-oriented bit-flip baselines

Attack access, model size, bit location and task conditions differ by comparison

**Reported measurements:**

Manuscript-backed: eight-bit models with a 50-bit budget on WebShop and ToolBench; internal-trigger success ranges 22.2%–94.4%, invocation results 67.3%–100%. “Clean data accuracy” means agreement with the original agent output, not independently verified task correctness.

**Limits on the conclusion:**

A bit flip changes a stored or computed representation. Its effect depends on which bit, parameter, memory location, model quantization, persistence and later computation are affected. A targeted attack can be effective under precise placement while remaining impractical without a physical or software fault-injection path.

Internal-trigger attacks and invocation attacks measure different events. A trigger can make a later behavior change conditional on an input, while an invocation attack targets whether a tool or action is selected. Their percentages cannot be merged, and agreement with the original output is not proof that the original task was correct.

The recovered threat model assumes full model/workflow knowledge and precise selected-bit changes, studies a single agent and uses adapted baselines. It does not establish a remote attack, persistence, transfer to other agents, tool authorization failure in every task or a mitigation. Model integrity checks and independent tool authorization are separate controls.

**Source and location**

Evidence tier: Recovered manuscript backed selected evaluation plus official DAC description; no independent fault injection, remote access or mitigation validation. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://arxiv.org/pdf/2603.10042v1)

Manuscript v1, threat model and Tables 1–3, PDF pages 2–6; official DAC record RESEARCH797; eight-bit models, 50-bit budget, WebShop/ToolBench and internal-trigger/invocation ranges.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** random bit flips

software prompt attacks

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH797

**Hardware or process assumptions:** Accelerator or memory system vulnerable to bit flips; attacker access is unspecified.

**Limits:** No attack success, bit budget, persistence, task impact, or mitigation results are reported.

Practicality depends on hardware access.

Official description only; threat-model validation is required.

**Method or artifact:** Targeted bit-flip attack methodology for LLM agents.

**Metrics:** Agent attack effectiveness is claimed qualitatively

**Problem:** Bit flips in agent models or memory may alter tool use and decision behavior.

**Workload or benchmark:** LLM-based agents and tools; model, memory access, target bits, and threat model are unspecified.

</details>

<span id="paper-dac-2026-research821"></span>

### Runtime-ADAR: Runtime Anomaly Detection and Attack Recovery in Encrypted DNNs

DAC 2026 · Record: `dac-2026-research821`

[Read the step-by-step explanation](#explanation-dac-2026-research821)

**Updated source-backed reading card**

Reviewed 2026-09-08. Deepens the existing Runtime-ADAR treatment into a paper-level reading; separates homomorphic-encryption noise from malicious faults, detection from compensation, baseline-relative accuracy from absolute accuracy, and recovery from exact repair.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Encrypted DNN inference can contain legitimate scheme noise and approximation while an attack can also alter computation or outputs; a runtime system must distinguish the two and respond without invalidating decryption or task quality.

**Mechanism / artifact:**

Noise-based statistical detection using sparse projections and a gradient-field weight-compensation mechanism in the ciphertext domain; cryptosystem, detector threshold, compensation rule, attack surface and recovery semantics are unspecified.

**Workload — the work tested:**

Homomorphically encrypted neural-network acceleration; models, cryptosystem, attack set, legitimate noise distribution, output target and evaluation protocol are unspecified.

**Hardware and manufacturing assumptions:**

Encrypted accelerator or homomorphic-encryption execution with ciphertext observability and key/decryption path; noise budget, arithmetic precision, memory, latency and key-management assumptions are unspecified.

**Baseline — the comparison method:**

No runtime defense

Offline anomaly detection

Attack and legitimate-noise conditions, cryptosystem, model and measurement boundary are unspecified

**Reported measurements:**

Official description reports mitigating over 90% of attack successes and restoring up to 97% of baseline accuracy on evaluated models, with qualitative overhead claims; absolute accuracy, attack denominator, detection rate and recovery cost are unspecified.

**Limits on the conclusion:**

Homomorphic-encryption noise can arise from valid encrypted computation and can grow toward a decryption limit. A detector must distinguish acceptable noise and approximation from an attack under the same cryptosystem, scale, operation sequence and model; a threshold that catches more attacks can also reject valid executions.

Sparse projections may detect statistical deviations but can miss attacks that preserve the observed projection or may leak information through the detector itself. Gradient-field compensation changes the ciphertext-domain computation; restoring output accuracy does not prove exact weight repair or preservation of the intended encrypted computation.

“97% of baseline accuracy” is a relative recovery statement, not necessarily 97% absolute accuracy. The official description reports no cryptosystem parameters, attack set, false-alarm rate, detection latency, recovery latency, decryption validity, energy or overhead measurement. The evidence supports a detection/recovery direction, not reliable encrypted-DNN resilience.

**Source and location**

Evidence tier: Primary captured official DAC description plus existing chapter level runtime adar discussion; no full paper extraction, encrypted attack reproduction or detection/recovery validation. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH821)

DAC 2026 official description; captured Problem, Mechanism / artifact, Workload, Hardware, Baseline, Measurements and Limits fields; record RESEARCH821; official page reports over 90% mitigation and up to 97% of baseline accuracy; no manuscript pages.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** no runtime defense

offline anomaly detection

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH821

**Hardware or process assumptions:** Encrypted accelerator or TEE inference; observability and key-management assumptions are unspecified.

**Limits:** No detection, recovery, accuracy, latency, cryptographic, or energy results are reported.

Detection may leak information or miss stealthy attacks.

Official description only; adversarial validation is required.

**Method or artifact:** Runtime anomaly detection and recovery for encrypted DNN inference.

**Metrics:** Encrypted-DNN resilience is claimed qualitatively

**Problem:** Encrypted DNN inference can conceal runtime anomalies while attacks degrade output or integrity.

**Workload or benchmark:** Encrypted DNN workloads; cryptosystem, attacks, models, and recovery are unspecified.

</details>

## What remains to establish

Resolve unspecified workloads, comparison methods, resource budgets, and source locations before generalizing a reported gain. Multiple papers in this selected sample permit comparison of mechanisms, but do not by themselves establish recurrence across years or a long-term trend.

[All subthemes](../expanded-taxonomy-v1.md) · [Research directions](../directions/README.md)
