# Privacy preserving computing

This subject has 3 records in the selected sample. This page explains where it fits, then presents all captured paper evidence without shortening the measurements or limitations.

[Definitions used in the paper records](../reading-guide-v1.md)

## Understand the parent subject first

- [Power reliability and security](../themes/power-reliability-and-security.md)

## Start with the information being protected

Private computation is not one mechanism. A system may try to hide a user's input from a server, hide a model from a client, restrict what a collaborator learns, or prevent reconstruction of training data. Each goal requires a statement about the parties, their observations, and the information they are allowed to learn. Good prediction accuracy or a transformed input image does not establish any of these protections by itself.

This group contains encrypted inference, optical-electronic encoding for training, and multi-GPU execution. Their common setting is computation performed with a privacy requirement. Their captured descriptions do not establish a common threat model, so their benefits cannot be compared as equivalent security guarantees.

## Encrypted arithmetic changes the computation

Homomorphic encryption permits specified operations on encrypted values, producing an encrypted result that an authorized party can decrypt. CKKS supports approximate real or complex arithmetic: the decrypted result need not equal an exact plaintext calculation. That distinction is explicit in [Microsoft SEAL's documentation](https://github.com/microsoft/SEAL). Numerical error and cryptographic security are different requirements; satisfying one does not establish the other.

[FBS](../observed-subthemes/privacy-preserving-computing.md#paper-dac-2026-research1187) proposes sparsity-aware convolutional-network inference using RNS-CKKS with fewer bootstrapping operations. RNS refers to representing large arithmetic quantities through residues under several smaller moduli. Bootstrapping refreshes a ciphertext for further computation; its configuration can trade performance against precision, as the [OpenFHE implementation notes](https://github.com/openfheorg/openfhe-development/blob/main/src/pke/examples/CKKS_BOOTSTRAPPING.md) explain.

The important claim is therefore not simply that some network values are zero. It is that the encrypted computation can exploit that structure to reduce expensive work while preserving required accuracy and security. The captured record does not explain the sparsity transformation or supply bootstrap counts, cryptographic parameters, latency, or inference accuracy. It would be unjustified to infer that pruning ordinary operations reduces encrypted work proportionally.

A useful comparison must keep the task, acceptable prediction error, and security requirements fixed. It should count any retraining, data rearrangement, additional ciphertext storage, and client-side processing required by the method. Fewer refresh operations would be an intermediate measurement, not the entire performance result.

<span id="explanation-dac-2026-research1187"></span>

### FBS: sparsity can reduce encrypted work only if the ciphertext representation and error budget permit it

#### What encrypted CNN inference is doing

A convolutional neural network applies learned weights to encrypted input values. In RNS-CKKS, a plaintext number is encoded approximately and encrypted into a ciphertext. The server performs supported additions and multiplications on ciphertexts without seeing the underlying input. The client or another authorized party decrypts the result and accepts a numerical approximation of the intended inference.

The computation carries more than the model's values. Ciphertexts have a modulus chain, scale, packing layout and accumulated numerical error. Multiplication can increase the scale and consume levels in the chain. Bootstrapping refreshes a ciphertext so that more computation can continue, but it is expensive and introduces its own precision and parameter requirements.

#### What sparsity changes—and what it does not

Sparsity means that selected weights, activations or connections are zero or treated as negligible under a defined rule. In ordinary arithmetic, skipping a zero multiplication is straightforward. In encrypted arithmetic, the zero pattern must be known at the right stage, represented in a way the evaluator can use, and compatible with ciphertext packing and rotations. If the server must discover the pattern from encrypted data, that discovery itself may require encrypted work and may reveal information through control flow or access patterns.

Reducing the number of ordinary operations does not automatically reduce bootstrapping. A sparse schedule may still require level alignment, rotations, ciphertext packing, masking, rescaling and refreshes. Conversely, aggressive pruning or approximation can change the network's prediction error. The method must state whether sparsity is in weights, activations or structure, whether it is fixed or input-dependent, and whether it changes the security or leakage model.

#### What a complete result must establish

Fix the CNN, dataset, accuracy target, CKKS parameters, security level, modulus chain, scale, packing, sparsity pattern and hardware. Compare dense RNS-CKKS, the standard bootstrap schedule and the proposed schedule. Report bootstrap count and time, ciphertext multiplications, rotations, memory, communication, latency, throughput, energy, decrypted numerical error and task accuracy. State whether client-side preprocessing, pruning, retraining, mask generation or ciphertext rearrangement is included.

Security must be evaluated at the selected parameters, not inferred from fewer bootstraps. Test different sparsity levels, input-dependent patterns, approximation error, packing layouts, noise margins, adversarial inputs and parameter choices that meet or fail the claimed security level. The captured official description reports no latency, throughput, security, accuracy, memory or bootstrap count. The evidence supports a sparsity-aware encrypted-inference direction, not a demonstrated proportional speedup or preserved privacy/accuracy guarantee.

## Encoding data is not automatically encryption

[Holocode](../observed-subthemes/privacy-preserving-computing.md#paper-dac-2026-research2996) proposes hybrid optical-electronic encoding at the edge for cloud training. The conceptual task is to transform locally collected information so that training remains useful while unwanted information is harder to obtain. The available description does not specify what the cloud receives, what secrets exist, or which party can reverse the transformation.

A visually unfamiliar representation is not enough to prove privacy. Evaluation must identify what an observer knows about the encoder, whether they can obtain examples of original and encoded data, and what sensitive attributes or reconstructions they attempt to recover. Optical noise and calibration also affect whether useful training behavior survives repeated operation. The source provides no leakage, training-accuracy, device-noise, latency, or energy measurements. It supports describing the proposal, not labeling it cryptographically equivalent to encrypted inference.

<span id="explanation-dac-2026-research2996"></span>

### Holocode: an encoded training input is private only against a defined observer and reconstruction task

#### What the edge transformation changes

An edge device can transform locally collected data before sending it to a cloud trainer. The transformation may change pixels, features, amplitudes, timing or representation while trying to preserve the information needed for model training. An optical stage can perform part of this transformation through light propagation, modulation, interference or sensing; an electronic stage can calibrate, digitize, package or further encode the result.

The transformed data is not automatically encrypted. Encryption is defined by a key-based security model in which an unauthorized party should not recover protected information under a stated attack model. An encoder may instead be a lossy transform, a secret-key transform, a learned representation or an obfuscation layer. The privacy claim depends on which of these it is, what the cloud knows, and whether the cloud can collect paired examples, gradients, model outputs or repeated observations.

#### What privacy must specify

Name the protected attributes and the observer. The cloud may be honest-but-curious, may alter the training procedure, or may collude with a device or another observer. It may know the encoder design, obtain calibration data, query the encoder, observe many samples, inspect timing and power, or train an inverse model. A transformed image can hide one attribute while preserving another, and training gradients or model outputs can reveal information even when the input representation looks unfamiliar.

The analysis must state whether privacy means low reconstruction quality, low sensitive-attribute inference, a formal leakage bound, resistance to a known attack, or something else. It must also state what utility is preserved: training loss, accuracy, calibration, robustness, convergence, downstream fairness or class performance. Privacy and utility should be measured on separate held-out data and against an observer who knows the published method.

#### What the optical channel adds

Optical noise, drift, alignment, saturation, temperature and calibration affect the encoded representation. Noise may reduce an attacker's reconstruction while also reducing training utility. A changing device can create distribution shift between edge encoders and cloud training. The evaluation must separate deliberate privacy transformation from accidental channel degradation and include the cost of calibration, retraining, device replacement and repeated operation.

Compare plaintext cloud training, ordinary digital encryption or encoding, and the proposed optical-electronic method under the same data, model, communication budget and training target. Report attack reconstruction and sensitive-attribute inference, training accuracy and convergence, latency, bandwidth, energy, calibration, device-to-device variation and failure behavior. Test known-encoder attacks, paired samples, chosen inputs, repeated observations, gradient or output attacks, optical noise and an untrusted cloud.

The captured official description identifies hybrid optical-electronic edge encoding for privacy-preserving cloud training. It reports no threat model, privacy leakage, reconstruction attack, training accuracy, latency, energy, optical-noise, calibration or key result. The evidence supports a privacy-aware representation direction; it does not establish cryptographic confidentiality or an end-to-end privacy guarantee.

## Multiple GPUs add an execution problem

The [multi-GPU tensor-fusion paper](../observed-subthemes/privacy-preserving-computing.md#paper-dac-2026-research574) combines operations and manages memory for private inference. A tensor is a multidimensional collection of values. Fusion combines processing steps so intermediate results may require less storage or movement. Whether that helps depends on how the privacy mechanism represents those values and permits them to move.

The record does not identify that mechanism. It must not be assumed to use CKKS, secure multiparty computation, or protected hardware merely because neighboring records do. The evaluation needs to state which memories and inter-device links can expose information, then measure execution under those protections. GPU count, interconnect, model, latency, and privacy results are all unspecified in the captured source.

<span id="explanation-dac-2026-research574"></span>

### Multi-GPU tensor fusion: fewer intermediate transfers do not automatically create private inference

#### What tensor fusion changes

Inference applies a sequence of operations to tensors: multidimensional arrays containing inputs, weights, activations or intermediate results. In a multi-GPU system, tensors may be split, copied between GPUs, stored in device memory, moved through an interconnect, or temporarily written to host memory. Tensor fusion combines compatible operations or their data movement so that an intermediate value can stay in a fused execution path instead of being materialized and transferred separately.

This can reduce memory traffic, kernel launches or synchronization. It can also increase the size and lifetime of a fused buffer, make scheduling harder, or force a different representation of protected values. A fusion transformation is valid only if it preserves the inference result under the selected numerical or privacy mechanism.

#### Where privacy can fail

Private inference has parties and observation points. The client may want to hide input data, the model owner may want to hide weights, and the service may be allowed to see only an encrypted or secret-shared representation. GPU memory, host memory, DMA paths, interconnect packets, logs, allocator metadata, timing and failed operations may each reveal information. Whether fusion helps depends on which of these are trusted and whether the privacy mechanism protects values during every movement.

The source does not identify whether privacy uses encryption, secret sharing, trusted hardware or another protocol. A fused operation can change the number and timing of messages, the location of plaintext or shares, the lifetime of intermediate tensors and the amount of information exposed by memory reuse. Adaptive memory management must therefore be evaluated as part of the threat model, not only as a capacity optimization.

#### What a complete evaluation needs

Define the protected inputs and model, trusted parties, colluding parties, observation points, allowed leakage and failure behavior. Compare single-GPU private inference, unfused multi-GPU execution and fused execution with the same model, privacy parameters, numerical error, batch, GPU count and interconnect. Report latency, throughput, memory peak, communication volume, synchronization time, energy, kernel count, allocator overhead, model accuracy and privacy leakage or security proof.

Test GPU failure, communication loss, out-of-order or repeated messages, memory reuse, host spill, concurrent tenants, different batch sizes and attacks that observe timing, traffic size or allocator behavior. State whether the result is an optimization under an existing privacy protocol or a new privacy protocol. The captured official description reports no privacy leakage, latency, throughput, energy, memory or model result. The evidence supports a multi-GPU execution direction for private inference, not established privacy preservation or system-level efficiency.

## A shared research question, not a shared guarantee

These papers motivate coordinating privacy mechanisms with numerical representation and execution. That is an inference from their proposed tasks, not evidence that one protection model is replacing another over time. A meaningful end-to-end study would state the permitted disclosures first, validate them, then compare complete latency, memory, communication, energy, and task accuracy under the same requirements. Performance obtained by revealing more information or trusting an additional party must be identified as a different operating point.

## Compare the results carefully

First identify the inputs and required output quality. Then identify the limited resource: time, memory, communication, energy, circuit area, or correctness coverage. Ask which part of the method reduces that cost and which new cost it adds. Compare numbers only when the experiments hold these conditions sufficiently similar.

A conference description may explain the proposal while omitting the full experiment. An author preprint link may have been coded from its abstract. The source classification does not by itself establish that every table was read. Missing locations remain visible below.

## Complete captured evidence

These are evidence records, not substitutes for the explanations above. Each record preserves its problem, proposed method, measurements, comparison conditions, and source limits. A populated record does not establish that its mechanism has been fully explained or independently verified.

<span id="paper-dac-2026-research1187"></span>

### FBS: Accelerating CNN Inference over RNS-CKKS with Fewer Bootstrapping Sparsity

DAC 2026 · Record: `dac-2026-research1187`

[Read the step-by-step explanation](#explanation-dac-2026-research1187)

**Updated source-backed reading card**

Reviewed 2026-09-08. Deepens the existing FBS treatment into a paper-level reading; defines RNS-CKKS ciphertext arithmetic and bootstrapping, separates ordinary sparsity from encrypted-work reduction, and makes numerical error, security parameters, packing and end-to-end latency explicit.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Fully homomorphic CNN inference is dominated by bootstrapping cost and encrypted tensor operations.

**Mechanism / artifact:**

Sparsity-aware RNS-CKKS inference strategy with fewer bootstrapping operations; sparsity location, representation, packing, schedule, parameter set, pruning/retraining and security assumptions are unspecified.

**Workload — the work tested:**

Encrypted CNN inference; network, dataset, weight/activation sparsity, accuracy target, ciphertext layout, input-dependent behavior and inference protocol are unspecified.

**Hardware and manufacturing assumptions:**

FHE accelerator or software stack for RNS-CKKS; modulus chain, scale, security level, memory, processor, communication and energy assumptions are unspecified.

**Baseline — the comparison method:**

Dense RNS-CKKS inference

Standard bootstrapping schedule

CNN, parameters, hardware, accuracy, security, packing and end-to-end accounting conditions are unspecified

**Reported measurements:**

Encrypted inference efficiency is claimed qualitatively; no bootstrap count/time, latency, throughput, security level, numerical error, task accuracy, memory, communication or energy result is reported.

**Limits on the conclusion:**

RNS-CKKS represents approximate encrypted values with scale, modulus levels, packing and accumulated error. Bootstrapping refreshes a ciphertext for more computation but its cost and precision depend on the parameter set. Fewer refreshes are not by themselves a security or performance result.

Sparsity can skip work only if the zero pattern, ciphertext layout, rotations, rescaling and control flow permit it. Weight sparsity, activation sparsity and input-dependent sparsity have different privacy, packing and computation consequences; ordinary zero counts do not imply proportional encrypted-work reduction.

The official description reports no latency, throughput, security, accuracy, memory or bootstrap count. The record supports a sparsity-aware encrypted-inference direction, not demonstrated proportional speedup or preserved privacy and accuracy.

**Source and location**

Evidence tier: Primary captured official DAC description plus existing chapter level fbs/rns ckks discussion and cited implementation documentation; no full paper extraction, parameterized security evaluation or end to end reproduction. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH1187)

DAC 2026 official description; captured Problem, Mechanism / artifact, Workload, Hardware, Baseline, Measurements and Limits fields; record RESEARCH1187; no manuscript pages.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** dense RNS-CKKS inference

standard bootstrapping schedule

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH1187

**Hardware or process assumptions:** FHE accelerator or software stack for RNS-CKKS; modulus chain, memory, and security assumptions are unspecified.

**Limits:** No latency, throughput, security, accuracy, memory, or bootstrapping counts are reported.

Sparsity may interact with ciphertext noise and packing.

Official description only; parameterized security evaluation is required.

**Method or artifact:** Sparsity-aware RNS-CKKS inference strategy with fewer bootstrapping operations.

**Metrics:** Encrypted inference efficiency is claimed qualitatively

**Problem:** Fully homomorphic CNN inference is dominated by bootstrapping cost and encrypted tensor operations.

**Workload or benchmark:** Encrypted CNN inference; scheme parameters, sparsity, security level, and baselines are unspecified.

</details>

<span id="paper-dac-2026-research2996"></span>

### Holocode: Hybrid Optical-Electronic Edge Encoding for Privacy-Preserving Cloud Training

DAC 2026 · Record: `dac-2026-research2996`

[Read the step-by-step explanation](#explanation-dac-2026-research2996)

**Updated source-backed reading card**

Reviewed 2026-09-08. Deepens the existing Holocode treatment into a paper-level reading; separates representation obfuscation from encryption, defines observer and leakage tasks, and makes optical-channel, utility, calibration, reconstruction and end-to-end privacy conditions explicit.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Edge data owners need to protect information while offloading model training to the cloud.

**Mechanism / artifact:**

Hybrid optical-electronic encoding scheme for privacy-preserving training data; transform, secret/key model, cloud observations, decoder, optical channel and training protocol are unspecified.

**Workload — the work tested:**

Cloud training with encoded edge data; data types, protected attributes, models, datasets, training outputs/gradients, repeated observations and utility targets are unspecified.

**Hardware and manufacturing assumptions:**

Optical/electronic edge encoder and cloud decoder; optics, sensor, channel, noise, drift, alignment, calibration, temperature, energy, bandwidth and key assumptions are unspecified.

**Baseline — the comparison method:**

Plaintext cloud training

Digital data encryption/encoding

Cloud threat model, observer knowledge, attack budget, model, data and communication conditions are unspecified

**Reported measurements:**

Privacy and training efficiency are claimed qualitatively; no privacy leakage, reconstruction or attribute-inference result, training accuracy, convergence, latency, energy, optical-noise, calibration, key or device-variation result is reported.

**Limits on the conclusion:**

A transformed representation is not automatically encryption. Privacy depends on the protected attributes, observer, key or training model, and whether the observer can use the known encoder, paired samples, repeated inputs, gradients, outputs, timing or power to reconstruct information.

Optical noise, drift, alignment and calibration can reduce an attack while also reducing training utility. Privacy must be measured against a defined reconstruction or attribute-inference task and a method-aware observer, while utility must include accuracy, convergence, robustness and relevant task behavior.

The official description reports no threat model, privacy leakage, reconstruction attack, training accuracy, latency, energy, optical-noise, calibration or key result. The record supports a privacy-aware representation direction, not cryptographic confidentiality or an end-to-end privacy guarantee.

**Source and location**

Evidence tier: Primary captured official DAC description plus existing chapter level holocode discussion; no full paper extraction, privacy attack evaluation or optical device validation. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH2996)

DAC 2026 official description; captured Problem, Mechanism / artifact, Workload, Hardware, Baseline, Measurements and Limits fields; record RESEARCH2996; no manuscript pages.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** plaintext cloud training

digital data encryption/encoding

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH2996

**Hardware or process assumptions:** Optical/electronic edge encoder and cloud decoder; channel, noise, and key assumptions are unspecified.

**Limits:** No privacy leakage, accuracy, latency, energy, optical noise, or key results are reported.

Encoding may leak through side channels or reconstruction errors.

Official description only; threat-model and channel validation are required.

**Method or artifact:** Hybrid optical-electronic encoding scheme for privacy-preserving training data.

**Metrics:** Privacy and training efficiency are claimed qualitatively

**Problem:** Edge data owners need to protect information while offloading model training to the cloud.

**Workload or benchmark:** Cloud training with encoded edge data; threat model, optical device, and baselines are unspecified.

</details>

<span id="paper-dac-2026-research574"></span>

### Multi‑GPU Tensor‑Level Fusion and Adaptive Memory Management for Private Inference

DAC 2026 · Record: `dac-2026-research574`

[Read the step-by-step explanation](#explanation-dac-2026-research574)

**Updated source-backed reading card**

Reviewed 2026-09-08. Deepens the existing multi-GPU tensor-fusion treatment into a paper-level reading; defines tensor movement and fusion, separates execution optimization from privacy protection, and makes GPU/interconnect observation points, memory lifecycle and end-to-end validation explicit.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Private inference workloads need efficient multi-GPU execution while protecting data and intermediate tensors.

**Mechanism / artifact:**

Tensor fusion and adaptive memory-management system for multi-GPU private inference; privacy mechanism, trusted parties, tensor representation, fusion transformation, memory lifecycle and leakage model are unspecified.

**Workload — the work tested:**

Private inference workloads; models, inputs, weights, batches, numerical error, GPU count, interconnect, failure cases and privacy parameters are unspecified.

**Hardware and manufacturing assumptions:**

Multi-GPU system with secure or isolated memory; GPU memory, host memory, DMA, interconnect, allocator, synchronization, tenant and threat assumptions are unspecified.

**Baseline — the comparison method:**

Single-GPU private inference

Unfused multi-GPU execution

Privacy mechanism, model, batch, GPU, interconnect, security and performance conditions are unspecified

**Reported measurements:**

Private-inference efficiency is claimed qualitatively; no privacy leakage or proof, latency, throughput, energy, peak memory, communication, synchronization, kernel, allocator or model result is reported.

**Limits on the conclusion:**

Tensor fusion can reduce intermediate materialization, transfers, launches or synchronization, but may change buffer lifetime, memory location, message timing and protected-value representation. An execution optimization is not automatically a privacy mechanism.

Privacy depends on which party can observe GPU memory, host memory, DMA, interconnect traffic, logs, allocator metadata, timing and failures. The source does not identify encryption, secret sharing, trusted hardware or another protocol, so no specific privacy guarantee can be inferred.

The official description reports no privacy leakage, latency, throughput, energy, memory or model result. The record supports a multi-GPU execution direction for private inference, not established privacy preservation or system-level efficiency.

**Source and location**

Evidence tier: Primary captured official DAC description plus existing chapter level multi gpu privacy discussion; no full paper extraction, threat model validation or multi gpu reproduction. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH574)

DAC 2026 official description; captured Problem, Mechanism / artifact, Workload, Hardware, Baseline, Measurements and Limits fields; record RESEARCH574; no manuscript pages.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** single-GPU private inference

unfused multi-GPU execution

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH574

**Hardware or process assumptions:** Multi-GPU system with secure or isolated memory; interconnect and threat assumptions are unspecified.

**Limits:** No privacy leakage, latency, throughput, energy, memory, or model results are reported.

Fusion may increase isolation and synchronization complexity.

Official description only; threat-model and performance validation are required.

**Method or artifact:** Tensor fusion and adaptive memory-management system for multi-GPU private inference.

**Metrics:** Private-inference efficiency is claimed qualitatively

**Problem:** Private inference workloads need efficient multi-GPU execution while protecting data and intermediate tensors.

**Workload or benchmark:** Private/inference workloads; privacy model, models, GPUs, and baselines are unspecified.

</details>

## What remains to establish

Resolve unspecified workloads, comparison methods, resource budgets, and source locations before generalizing a reported gain. Multiple papers in this selected sample permit comparison of mechanisms, but do not by themselves establish recurrence across years or a long-term trend.

[All subthemes](../expanded-taxonomy-v1.md) · [Research directions](../directions/README.md)
