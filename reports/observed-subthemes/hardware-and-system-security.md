# Hardware and system security

This subject has 11 records in the selected sample. This page explains where it fits, then presents all captured paper evidence without shortening the measurements or limitations.

[Definitions used in the paper records](../reading-guide-v1.md)

## Understand the parent subject first

- [Power reliability and security](../themes/power-reliability-and-security.md)

## Security depends on interactions across the system

A processor, memory manager, operating system, peripheral, and application can each behave according to its local rules while their interaction exposes protected information. System security therefore requires identifying how data and control pass between components and which observations are available to another party.

The same observation can have different consequences in different deployments. A shared machine, an isolated device, and a device accessible to a physical observer provide different opportunities. The evaluation must describe the actual deployment assumptions before a claim can be interpreted.

## An information path needs several conditions

For an information leak to matter, protected activity must affect something observable, the observer must access that observation, and the observation must support a useful inference. Noise, unrelated activity, and changing software can affect each step.

An experiment should distinguish identifying the relationship from demonstrating the full inference. The number of measurements, the time needed, the observer's prior knowledge, and unsuccessful cases are part of practicality. A title describing an attack does not establish these conditions.

## Address translation can expose system behavior

Stone-Skimming's captured description concerns a page-table-walk side channel in analytics applications. Virtual-memory systems translate program-visible addresses into physical-memory locations. A page-table walk consults the translation data needed to resolve an address when that information is not already available in a faster structure. [Recorded evidence](../observed-subthemes/hardware-and-system-security.md#paper-dac-2026-research1793)

The research question is whether observable translation activity permits inference about protected application behavior. The record does not establish access requirements, leakage rate, observation time, operating-system configuration, or evaluated mitigations. Those gaps prevent interpreting the description as a generally available attack against analytics systems.

<span id="explanation-dac-2026-research1793"></span>

### Stone-Skimming: a page-table side channel is an inference path, not merely a slow memory access

#### What address translation does

An application normally uses virtual addresses. The processor must translate each virtual address into a physical location before memory can be accessed. A translation cache can hold recent mappings. When the needed mapping is absent, the processor consults page-table data through one or more memory references. That extra work is a page-table walk.

The walk is governed by the operating system's page tables, page size, permissions, process layout and memory state. It can affect latency, cache state, memory traffic, contention and other timing-visible behavior. The important security question is whether those effects depend on a protected computation in a way that an observer can measure.

#### How an inference attack would have to work

The attack needs a chain of conditions. First, the protected workload must choose addresses or execution paths that produce distinguishable translation activity. Second, the attacker must obtain an observation: for example, timing, contention or another architectural or microarchitectural signal. Third, the signal must be separated from noise caused by the attacker's own work, other tenants, interrupts, scheduling, garbage collection, input variation and unrelated system activity. Fourth, the attacker must map the remaining signal to a useful property of the analytics application.

Observing that two workloads produce different timing is weaker than recovering a secret or identifying a protected query. A complete result must define the target information, the attacker's prior knowledge, the number of measurements, the time per attempt, the success threshold and the rate of unsuccessful inferences.

#### Why big-data workloads need explicit evaluation

Analytics systems often execute long pipelines with changing data, parallel workers, task scheduling, joins, shuffles and repeated stages. These features can create both signal and noise. A page-table pattern associated with one input or software version may not remain stable when partitions, memory pressure, worker placement or operating-system decisions change.

The comparison must hold the protected workload, input, software, processor, memory size, co-location, scheduling policy and measurement procedure fixed while varying the protected condition of interest. It should then test unseen inputs, different workers, concurrent applications, process placement, page sizes, huge pages, address-space randomization and relevant mitigations. Report leakage or classification accuracy, confidence, samples, wall-clock attack time, observation bandwidth, false positives, false negatives and attacker overhead.

The captured official description identifies a page-table-walk side-channel attack against big-data analytics applications. It does not state the observation interface, co-location requirement, operating system, processor, workload configuration, leakage rate, attack time or mitigation result. The evidence supports a plausible translation-based information path and a research direction; it does not establish a generally practical attack or a security conclusion for all analytics systems.

## Physical measurements have their own access boundary

The per-core electromagnetic-monitoring record concerns signals associated with multicore execution. A physical observation can depend on the device package, measurement position, surrounding noise, and concurrent activity. Distinguishing one core's activity from another is a different result from recovering a protected application value. [Recorded evidence](../observed-subthemes/hardware-and-system-security.md#paper-dac-2026-research213)

The captured description does not supply measurement distance, trace count, inference success, or protection results. A complete evaluation must identify the measured quantity and the observer's access. The record supports a research topic, while the practical security conclusion remains open.

<span id="explanation-dac-2026-research213"></span>

### Per-core electromagnetic leakage: detecting activity is different from recovering a secret

#### Why computation can create an electromagnetic signal

Digital circuits change voltage and current as transistors switch. Those changes can produce electromagnetic fields around the die, package, board and power-delivery network. The field is not a direct copy of the program. It is a physical mixture of switching activity, clocking, memory traffic, power regulation, package coupling, nearby cores and environmental noise.

The security question is whether the mixture changes in a repeatable way when a protected computation changes. A probe or antenna can collect a time-varying trace. Signal processing or statistical learning can then test whether traces reveal a core, an instruction class, an operand property or a secret-dependent operation. Each step is an additional claim; detecting that two cores have different activity is not the same as extracting a secret value.

#### What “per-core” must establish

Multicore systems create overlapping sources. The measured field may contain activity from the target core, sibling cores, shared caches, memory controllers, interconnects, clock circuits and regulators. A per-core claim therefore needs an attribution method: spatial placement, timing, repeated execution, controlled scheduling, a reference trace or another validated separation procedure.

The physical setup is part of the threat model. Report the package and board, probe type and bandwidth, probe position and distance, shielding, grounding, sampling rate, trigger, measurement duration, environmental noise, supply conditions and whether the attacker controls or shares a core. A result requiring a probe placed directly over a known package location has a different security meaning from a remote or unmodified-device observation.

#### What a secret-recovery claim requires

The protected computation must be repeated under controlled inputs and labels, while the attacker is prevented from learning the answer through an easier channel. Training and test traces must be separated by execution, input, key or device as appropriate. Report the number of traces, preprocessing, classifier or statistical test, confidence intervals, false positives, false negatives, guessing success and time to reach the stated success level.

The experiment should vary core placement, simultaneous activity, workload, input, secret, clock frequency, voltage, temperature, device and probe position. It should compare per-core monitoring with aggregate electromagnetic and power monitoring under the same conditions. A defense must be tested against the same attack budget and must show whether it reduces leakage, lowers attribution quality, or only defeats one measurement setup.

The captured official description identifies per-core electromagnetic side-channel monitoring of multicore architectures. It reports no probe distance, trace count, leakage rate, attack success, package conditions, attribution method or mitigation result. The evidence supports a physical side-channel research direction; it does not establish remote observability, reliable per-core separation or secret recovery.

## Obscuring a protocol can affect its correct execution

ODBP concerns hiding aspects of a biochemical protocol implemented in a continuous-flow microfluidic device. Such a protocol controls fluid movement and processing steps. Altering its implementation to obscure information may also change timing, reagent use, or the intended biochemical result. [Recorded evidence](../observed-subthemes/hardware-and-system-security.md#paper-dac-2026-research2107)

This case requires both a confidentiality evaluation and a functional evaluation. The current description leaves leakage, assay outcome, latency, reagent cost, and fabrication conditions unresolved. A design that is harder to interpret is useful only if it also executes the required protocol adequately under the stated conditions.

<span id="explanation-dac-2026-research2107"></span>

### ODBP: protocol obfuscation must preserve both secrecy and the biochemical result

#### What a continuous-flow protocol controls

A continuous-flow microfluidic biochip moves liquids through channels and control points. A protocol is an ordered set of operations: introduce a reagent, route or mix fluids, wait for a reaction, wash a channel, and deliver a result. The physical schedule determines which fluids meet, for how long, at what concentrations and in what order.

The schedule can reveal information even when the chip does not expose a software-level description. An observer may see valve activations, flow paths, timing, reagent order, channel use, pressure changes or power and control traffic. Those observations can identify the assay or infer sensitive intermediate steps. Obfuscation therefore tries to make different protected protocols produce less distinguishable observations.

#### What obfuscation can and cannot mean

Randomizing or adding operations does not automatically hide the protocol. The observer may learn from the added operations, from timing differences, from which channels are available, or from the total duration and reagent volume. A useful confidentiality claim must define the observer, the signals available, the set of protocols that must be confused, the observer's prior knowledge and the allowed number of observations.

There is also a functional constraint. Fluidic operations have physical meaning. Extra mixing, routing or waiting can change concentration, residence time, temperature exposure, contamination risk, reagent consumption and completion time. An obfuscated schedule that makes the protocol harder to identify but produces the wrong assay result is not a valid implementation. Correctness must be checked at the biochemical output, not only at the valve-control trace.

#### What a complete evaluation should measure

Compare the original and obfuscated schedules on the same chip architecture, reagents, input conditions and fabrication assumptions. Measure protocol success rate, assay yield or output error, latency, reagent volume, energy or control overhead, channel occupancy, fault tolerance and repeatability. Separately measure confidentiality with an explicit attack: classification or inference accuracy, mutual information or another defined leakage measure, the observations used, training and test protocols, sample count and attacker computation.

The evaluation should include unseen protocols, varied flow rates, manufacturing variation, valve faults, contamination or incomplete flow where relevant, and an attacker who knows the obfuscation procedure. It should state whether the method hides the protocol itself, only hides a selected feature, or merely reduces the success of one tested classifier.

The captured official description identifies protocol obfuscation for continuous-flow microfluidic biochips. It reports no leakage measure, attacker model, assay result, yield, latency, reagent cost, fabrication condition or fault/variation experiment. The evidence supports a security-and-function co-design problem, not a demonstrated confidentiality guarantee or a validated biochemical improvement.

## Reconnaissance: tracking several secrets without treating every observation as a leak

<span id="explanation-dac-2026-research2369"></span>

### Reconnaissance: reveal and conceal labels define what an information-flow analysis is allowed to expose

#### What the analysis is trying to preserve

An information-flow analysis follows how values move through a design. It marks a value as secret, tracks operations that depend on it, and checks whether that dependence reaches an output or observation available to an attacker. With multiple secrets, the analysis must preserve identity: a result may depend on secret A, secret B, both, or a relation between them. Combining all secrets into one undifferentiated label can lose that information.

The analysis also needs a policy for intentional release. Some systems are designed to reveal a value, a checksum, a comparison result or a protocol-approved output. A reveal operation means that a flow to that output is permitted under a stated rule. A conceal operation means that a value remains protected and must not reach an unauthorized observation. These labels are policy statements; they do not by themselves prove that an implementation obeys the policy.

#### Why reveal and conceal semantics matter

The same operation can be safe or unsafe depending on what is revealed and to whom. Revealing one secret's authorization result must not silently reveal another secret. A comparison between two secret values can disclose their equality even when neither value is printed. A function can also combine several secret inputs, so the analysis must state whether it tracks individual dependencies, sets of secrets, correlations, or only a coarse public/secret distinction.

Soundness asks whether every forbidden flow is detected under the model. Precision asks whether the analysis avoids reporting flows that are permitted or impossible. A system can be sound but produce many false alarms, or precise on tested examples while missing a flow outside its model. Multiple-secret support must therefore be evaluated against explicit programs, policies and attacker observations.

#### What a complete validation needs

Define the label state, the transfer rule for each operation, the meaning of reveal and conceal, the allowed output interface, control-flow treatment, memory and concurrency model, and the treatment of declassification or intentional release. Then test direct flows, flows through arithmetic and comparisons, aliases, arrays, control predicates, exceptions, speculative or concurrent behavior where relevant, and interactions between multiple secrets.

Compare with single-secret tracking and standard information-flow analysis using the same designs and policies. Report soundness and precision against a reference judgment, runtime, memory, number of tracked labels, scaling with secret count and analysis failures. Case studies should state whether the result is a proof, a warning, or a tool-assisted check under a restricted model.

The captured official description identifies a reveal/conceal paradigm for tracking multiple secrets. It reports no formal label semantics, soundness proof, precision study, runtime, scalability result or case study. The evidence supports a policy-aware analysis direction; it does not establish that all forbidden multi-secret flows are detected or that all reported flows are meaningful.

## SRAM aging can preserve history without preserving the original bits directly

<span id="explanation-dac-2026-research3019"></span>

### Decoding the Past: an aging imprint is a physical inference problem, not ordinary memory remanence

#### What an SRAM cell stores and what aging changes

An SRAM bit is held by a small feedback circuit that has two stable electrical states. Reading the cell normally reports which state the circuit currently occupies. A prior data pattern can also affect long-term electrical stress if one side of the cell experiences different voltage, current or switching conditions for a substantial time. Device aging mechanisms may then change transistor strength, leakage or switching margin.

An aging imprint is therefore different from simply reading charge left behind after power is removed. The proposed attack would infer earlier activity from a later change in how cells behave. The cell does not necessarily retain the original bit as a readable bit. Instead, its later readout may contain a weak, noisy statistical relationship with the earlier pattern.

The strength and direction of that relationship depend on the cell design, process variation, supply voltage, temperature, stress duration, duty cycle, refresh and intervening writes. An observed read bias can also come from manufacturing mismatch, retention effects, read disturb, supply noise or the measurement circuit. Those alternative causes must be separated from the claimed historical imprint.

#### What data recovery would require

The attacker needs a way to access the SRAM and a readout that is sensitive to the claimed aging effect. The attacker may need to know the device before and after stress, control the stress pattern, wait a specified time, or calibrate each chip. A recovery procedure then maps measurements to a prior data pattern using a model or classifier.

Recovery accuracy must be defined against a baseline. Guessing a bit more often than chance is not the same as recovering a file, key or structured record. Report bit error rate, confidence, block or message recovery rate, number of cells and reads, calibration data, time since the sensitive data was written, required prior knowledge and the probability of false recovery. Test data from new devices separately from training data and test whether the model transfers in a cross-device evaluation.

#### What can erase or weaken the imprint

The evaluation should vary stress time, temperature, voltage, write pattern, intervening writes, power cycles, idle time and read activity. It should test process and device variation, different SRAM blocks, memory controllers and the readout sensor. Mitigations might overwrite memory, randomize placement, equalize stress, power-cycle, change voltage or limit access, but each must be tested for both residual information and functional cost.

The captured official description identifies recovery of sensitive data from SRAM aging imprints. It reports no recovery accuracy, age or retention horizon, access requirement, sensor, process condition, calibration procedure or mitigation result. The evidence supports a hardware-forensics hypothesis; it does not establish that sensitive data can be recovered from ordinary SRAM across devices or after a stated sanitization procedure.

## A touchscreen trajectory can leak through the sensing process

<span id="explanation-dac-2026-research315"></span>

### Touchscreen electromagnetic emanations: reconstructing a path requires more than detecting a touch

#### How a capacitive touchscreen produces a measurable process

A capacitive touchscreen contains a grid of conductive electrodes. The controller scans parts of the grid and measures how a finger or stylus changes the electrical coupling at nearby locations. It repeats this scan over time, estimates touch coordinates and sends those estimates to the operating system or application.

The controller's repeated switching can produce electrical current changes and electromagnetic fields. The field can depend on scan timing, electrode activity, touch location, controller state, display interference, power regulation and the device enclosure. An external sensor may therefore collect a trace correlated with touch activity without receiving the touchscreen's digital coordinate messages.

Correlation is not yet trajectory recovery. A trajectory is a time-ordered sequence of positions, so the attack must determine both where each touch occurred and when it occurred. It must separate touch-dependent variation from scan schedule, display refresh, wireless radios, processor activity, hand position, orientation and environmental noise. The attacker also needs a mapping from measured traces to coordinates, gestures or handwriting symbols.

#### What the physical threat model controls

The result depends on the phone model, screen stack, case, sensor type, probe orientation and distance, shielding, sampling bandwidth, trigger and whether the attacker can control the display or induce repeated writing. A probe placed near a known edge of one unmodified phone is a different access condition from a remote sensor in a room. The evaluation must state whether the target is a trajectory, individual points, words or a secret entered through handwriting.

Training and test traces must be separated by writing session, user, device and phrase as appropriate. Otherwise a model may recognize a particular user's motion, phone placement or recording setup rather than reconstructing touch coordinates from a new target. Report coordinate error, point-detection precision and recall, temporal alignment, handwriting or phrase recovery rate, false positives, trace count, recording time and attacker computation.

#### What a complete comparison needs

Compare the electromagnetic method with direct touchscreen software logging under the same sessions, and with a noisy electromagnetic baseline that has no useful calibration. Test different users, writing speeds, screen orientations, cases, display states, phone models, probe positions, distances and background activity. Evaluate whether a defense changes the field, reduces reconstruction quality or only defeats one probe and one trained model. Include the energy, latency, usability and display or touch-performance cost of any mitigation.

The captured official description identifies electromagnetic side-channel recovery of smartphone touch trajectories. It reports no recovery accuracy, distance, equipment, user diversity, cross-device result or mitigation result. The evidence supports a physical side-channel hypothesis; it does not establish remote trajectory recovery, general handwriting reconstruction or a demonstrated protection failure.

## A vehicle IDS must reason about messages in their system context

<span id="explanation-dac-2026-research462"></span>

### SCIMI: collaborative intrusion detection needs semantic meaning, trustworthy exchange and vehicle-level validation

#### What an in-vehicle intrusion detector observes

An in-vehicle network carries messages between electronic controllers. A message has more than a payload: its sender, identifier, timing, order, rate, operating mode and relationship to other messages can determine whether it is expected. A detector must compare observed traffic with the vehicle behavior and communication rules it is meant to protect.

“Semantic-aware” means the detector uses the meaning or context of traffic rather than treating each frame as an isolated byte pattern. For example, the same value may be normal in one operating mode and suspicious in another. This requires a defined message vocabulary, signal interpretation, state or mode model and assumptions about which sources are trusted. If those meanings are wrong or incomplete, a detector can reject valid behavior or miss an attack that stays within the expected format.

#### Why collaboration can help and hurt

A local detector sees only its own traffic or sensor inputs. Nodes can share alerts, features, context or summarized evidence so that one node can identify a pattern that is visible only across domains. Collaboration may improve coverage of distributed attacks, but it adds communication delay, bandwidth, synchronization and dependency on other nodes.

The exchange itself becomes an attack surface. A compromised node may send false alerts, suppress real alerts, replay old evidence, poison a shared model or infer sensitive vehicle state from the information it receives. The system must define identity, authentication, freshness, trust, missing messages, disagreement resolution and behavior when the collaboration channel is unavailable. A global alert also needs a clear rule for converting distributed evidence into an action.

#### What a safety-relevant evaluation must measure

Evaluate local, signature-based and collaborative detectors on the same vehicle architecture, traffic traces, attack set and compute budget. Separate training from test drives, vehicles, attack instances and operating modes. Report detection rate by attack type, false-positive rate, alert latency, missed attacks, bandwidth, memory and processor cost, detection under node failure or compromise, and the effect on control or safety functions.

Test benign mode changes, rare but valid traffic, timing jitter, loss and reordering, gateway behavior, unknown attacks, replay, forged semantic context, compromised detectors and partitioned domains. Measure whether collaboration improves system-level detection rather than only an isolated classifier score. If the detector triggers a safety response, validate that response and its worst-case delay on the vehicle platform.

The captured official description identifies a semantic-aware collaborative intrusion-detection system for multi-domain in-vehicle networks. It reports no detection rate, false positives, latency, bandwidth, compromised-node test, attack set or vehicle result. The evidence supports a context-aware distributed detection direction; it does not establish safe deployment, improved system-level detection or resistance to attacks on the collaboration mechanism.

## Attestation can establish an artifact identity without proving its whole execution

<span id="explanation-dac-2026-research625"></span>

### AttestLLM: efficient model attestation must connect a trusted measurement to runtime behavior

#### What attestation is meant to establish

An on-device language model can be changed by replacing weights, modifying code, changing configuration, loading an unauthorized adapter or altering the runtime that interprets the model. Attestation is a protocol in which the device produces evidence about its state and a verifier checks that evidence against an approved reference.

The evidence normally includes a cryptographic measurement, such as a digest of an artifact, plus a signed statement from a hardware-protected key. The verifier must know which component was measured, when it was measured, what version and configuration are allowed, and which device key is trusted. A digest can show that measured bytes match an approved value; it does not by itself say that the correct bytes were loaded into every execution path or that the device is free of later changes.

#### Why billion-scale models change the engineering problem

Hashing a complete model can require reading a large amount of memory and can add latency, bandwidth and energy cost. An efficient framework may measure chunks, a tree of hashes, metadata, selected layers or a compact commitment. Each shortcut changes the security claim. If only metadata is measured, altered weights may be missed. If only selected regions are measured, the attacker may target an unchecked region. If a tree is used, the verifier must know how leaves map to model storage and how updates invalidate old proofs.

The measurement must also cover provenance and lifecycle: model version, tokenizer, preprocessing, quantization, adapters, compiler, runtime, libraries, configuration, update authorization, rollback protection and secure boot chain. Measuring a file without binding it to the code and configuration that execute it leaves an integrity gap.

#### What model integrity does not prove

A valid attestation can show that a designated image or model is present under a stated measurement procedure. It does not prove that prompts are private, that outputs are correct, that the runtime has no memory-safety flaw, that an accelerator executes every operation faithfully, or that a compromised operating system cannot observe or alter inputs and outputs. It also does not establish that an approved model is safe or that its behavior meets a task-specific policy.

The verifier therefore needs a threat model: which device components are trusted, whether the hardware root of trust is genuine, whether keys can be cloned, whether the network is authenticated, whether freshness prevents replay, and what happens when an update is revoked or a device is offline. The protocol must define nonce or freshness handling and the action taken when evidence is missing or invalid.

#### What a complete evaluation should measure

Compare full-model hashing, the proposed method and unattested deployment on the same device and model. Report attestation latency, memory traffic, energy, verifier time, proof size, startup delay, inference throughput, update cost, rollback handling and failure recovery. Test altered weights, code, runtime, adapters, tokenizer, configuration, storage, boot state and accelerator paths. Measure whether the evidence detects each change and whether an attacker can produce a valid statement for an unauthorized state.

The captured official description identifies an efficient attestation framework for billion-scale on-device LLMs. It reports no security proof, attestation latency, memory, energy, update, freshness, tamper-detection or device result. The evidence supports an integrity-and-provenance protocol direction; it does not establish runtime behavior integrity, end-to-end model trust or deployment readiness.

## An emulator detector relies on a difference in instruction behavior

<span id="explanation-dac-2026-research663"></span>

### Emudrop: reserved-opcode detection is a compatibility test with a narrow evidence boundary

#### What a reserved opcode is testing

An instruction encoding is a bit pattern that a processor or emulator interprets as an operation. Some encodings are reserved or invalid for a stated processor mode. A real processor may raise an illegal-instruction exception, while an emulator, dynamic translator or hypervisor may handle the same bytes through a different path. A program can deliberately execute the encoding, catch the resulting exception or observe the result, and classify the environment from that behavior.

This is a hardware-behavior fingerprint. It does not directly prove that an environment is virtualized. The observed result can depend on the CPU generation, execution mode, operating system, exception delivery, signal handler, hypervisor policy, binary translation, sandbox restrictions and whether the instruction is intercepted or rewritten before execution.

#### What the detector can and cannot establish

The detector can establish that the observed environment did not behave like the reference behavior under the chosen test. It may distinguish a particular emulator or hypervisor implementation from a particular class of Intel processors. It does not automatically identify all emulators, and native behavior that differs from the reference can produce a false positive.

An emulator author can implement the expected exception behavior, intercept the test, patch the instruction, or alter the visible exception state. A malware-analysis system can also recognize the detector and neutralize it. The resulting contest is about the tested behavior and attacker budget, not a permanent property of hardware and software.

#### What a complete validation needs

Run the exact test across Intel CPU generations, operating systems, privilege levels, exception mechanisms, bare metal, hypervisors, full-system emulators, user-mode emulators, sandboxes and binary translators. Record the exception type, signal or fault delivery, register and memory state, timing and any required permissions. Test benign native machines and emulated machines not used to design the rule.

Compare reserved-opcode detection with software emulator checks and CPUID-based checks under the same conditions. Report detection rate by environment, false positives, false negatives, portability, execution overhead, crash or recovery behavior, required privilege and the effect of a defender that emulates the expected response. A result useful for malware evasion analysis should also state whether the method survives common instruction rewriting, sandbox policy and detector-aware emulation.

The captured official description identifies a minimal hardware-based emulator-detection technique using Intel reserved opcodes. It reports no detection rate, false positives, CPU or emulator coverage, privilege requirement, timing, evasion test or mitigation result. The evidence supports a compatibility-fingerprint direction; it does not establish portable detection of emulation or a general malware-evasion capability.

## A TLB signal can weaken address randomization only if it yields a usable address fact

<span id="explanation-dac-2026-research681"></span>

### Mistletunnel: a TLB side channel turns translation activity into a KASLR question

#### What KASLR is protecting

Kernel address-space layout randomization, or KASLR, changes where kernel code and data are placed in memory. An attacker may know the relative arrangement of kernel components but not their actual addresses. The random offset makes it harder to use a memory-corruption bug or another pointer-based technique reliably.

The translation lookaside buffer, or TLB, is a fast cache of recent mappings from virtual addresses to physical locations. A TLB hit and a TLB miss can cause different timing or contention. Shared or indirectly observable translation state can therefore reveal whether particular address translations were recently used. A side-channel attack tries to turn that difference into information about a victim's execution or layout.

#### What must happen for KASLR to be weakened

The attacker needs an observation that depends on a kernel address or translation event. The signal must be distinguishable from the attacker's own activity, other processes, interrupts, scheduling, cache and memory traffic, and the noise of the Apple silicon implementation. The observed result must then be mapped to a candidate address, offset or layout hypothesis with a known error rate.

Finding a correlation with translation activity is weaker than recovering the randomized kernel base. A complete claim should state the address information recovered, how many observations are needed, elapsed time, confidence, false-recovery rate and whether the result enables a demonstrated follow-on action. It should also state whether the attacker needs local code execution, same-core or same-machine co-location, special privileges, a vulnerable interface or a particular victim workload.

#### Why the platform boundary matters

TLB levels, invalidation rules, page sizes, exception behavior, scheduling, privilege checks and operating-system mappings differ across processors and OS versions. Apple M-series parts may share broad architectural ideas with other systems while implementing translation state and timing differently. A result on one chip and kernel build cannot be generalized to all Apple silicon or all KASLR deployments without cross-platform tests.

Compare with cache side channels and existing KASLR attacks using the same victim, access, noise, time and success criteria. Test different M-series generations, OS versions, page sizes, core placement, concurrent workloads, process permissions, mitigations and repeated randomized layouts. Report address-recovery rate, confidence, time, samples, noise tolerance, required privilege, false positives, false negatives and whether mitigations remove the signal or only lower it.

The captured official description identifies a novel TLB side-channel attack against KASLR on Apple M-series systems. It reports no address-recovery rate, time, noise tolerance, privilege, cross-platform coverage or mitigation result. The evidence supports a platform-specific translation-leakage direction; it does not establish general KASLR defeat or a usable exploit chain.

## A secure snapshot must preserve the whole trusted execution state

<span id="explanation-dac-2026-research876"></span>

### Tdsnap: fast restoration is useful only when the snapshot keeps isolation, integrity and freshness

#### What state a FaaS snapshot represents

Function-as-a-service runs short pieces of application code on shared infrastructure. A function can have registers, stack and heap memory, runtime metadata, open connections, pending work, credentials, device state and communication with storage or other services. A snapshot is a saved representation from which execution can resume later.

A trusted-domain snapshot tries to save and restore that state while keeping one tenant's state hidden from the platform, another tenant and an attacker who can influence scheduling or reuse. The trusted domain may be a hardware-isolated execution area, but the snapshot mechanism still needs to define which state is inside the boundary, which component performs copying, and how the saved bytes are protected while stored and moved.

#### Why saving memory is not enough

Confidentiality requires encryption and key handling for the snapshot, but encryption alone does not prevent an attacker from replacing, replaying, truncating or reordering snapshots. Integrity requires authentication of the state and its metadata. Freshness requires binding the snapshot to a function instance, version, monotonic progress or accepted epoch so that an old valid snapshot cannot restore stale secrets or repeat a one-time action.

The boundary also includes external state. A function may have sent a message, charged an account, updated a database or received a secret before the snapshot was taken. Restoring the computation without coordinating those effects can duplicate an action, lose an action or create inconsistent state. A snapshot protocol must define quiescence, in-flight requests, timers, random-number state, device mappings, network connections, keys, storage writes and rollback behavior.

Snapshot metadata can itself leak information. Size, timing, page-change patterns, function identity, access frequency and restore failures may reveal workload or tenant state even when the snapshot contents are encrypted. The evaluator must state whether the platform, storage service, hypervisor, network and co-resident tenant are trusted, and what they can observe.

#### What a complete FaaS evaluation should measure

Compare process isolation, standard virtual-machine snapshots and the trusted-domain method with the same functions, state sizes, cold-start targets, storage and network conditions. Measure snapshot and restore latency, memory and storage overhead, bandwidth, energy, throughput, tail latency, concurrent tenants, failure recovery and cost. Test a malicious host, storage replacement, replay, rollback, interrupted copy, stale key, compromised co-tenant and failed trust-domain entry.

The evaluation should prove that a restored function cannot read another tenant's state, that unauthorized modification is detected, that freshness rules prevent unsafe replay, and that external side effects remain correct. It should report whether the method protects only memory contents or also code, runtime, I/O, device state and secrets.

The captured official description identifies a trusted-domain snapshot mechanism for secure FaaS. It reports no isolation proof, snapshot latency, memory overhead, rollback handling, metadata leakage, threat-model detail or workload result. The evidence supports a secure state-migration direction; it does not establish confidential, rollback-safe or production-efficient FaaS snapshots.

## Comparing attacks and protections

Use a defined attacker model, protected behavior, and success criterion. Report how much control and observation the experiment permits. Evaluate the unprotected and protected systems under comparable conditions and include resource overhead and effects on correct operation.

For defenses, examine whether protection removes the information path or merely weakens the tested procedure. For attacks, report the conditions under which inference fails. These details allow the result to inform design decisions without implying security or insecurity beyond the demonstrated case.

The selected papers address different interfaces and access assumptions. Their connection is the need to examine whole-system information paths. Their individual success measures should not be combined into a common security ranking.

## Compare the results carefully

First identify the inputs and required output quality. Then identify the limited resource: time, memory, communication, energy, circuit area, or correctness coverage. Ask which part of the method reduces that cost and which new cost it adds. Compare numbers only when the experiments hold these conditions sufficiently similar.

A conference description may explain the proposal while omitting the full experiment. An author preprint link may have been coded from its abstract. The source classification does not by itself establish that every table was read. Missing locations remain visible below.

## Complete captured evidence

These are evidence records, not substitutes for the explanations above. Each record preserves its problem, proposed method, measurements, comparison conditions, and source limits. A populated record does not establish that its mechanism has been fully explained or independently verified.

<span id="paper-dac-2026-research1793"></span>

### Stone-Skimming: Attacking Big-Data Analytics Applications with Page Table Walk

DAC 2026 · Record: `dac-2026-research1793`

[Read the step-by-step explanation](#explanation-dac-2026-research1793)

**Updated source-backed reading card**

Reviewed 2026-09-08. Deepens the existing Stone-Skimming treatment into a paper-level reading; defines the translation path, separates an observable timing relationship from useful secret inference, and makes threat-model, workload-variation and mitigation measurements explicit.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Page-table behavior may expose information about large analytics workloads.

**Mechanism / artifact:**

Page-table-walk side-channel attack against big-data analytics applications; observation interface, signal extraction, inference model and mitigation procedure are unspecified.

**Workload — the work tested:**

Big-data analytics workloads; datasets, pipeline stages, workers, inputs, software versions, operating system, co-tenancy and trace conditions are unspecified.

**Hardware and manufacturing assumptions:**

Paged virtual-memory processor with observable translation or timing behavior; processor, memory hierarchy, page size, huge-page policy, scheduler and address-space configuration are unspecified.

**Baseline — the comparison method:**

Noisy page-table observation

Existing memory side channels

Attacker access, co-location, observation interface, prior knowledge and comparison conditions are unspecified

**Reported measurements:**

Attack effectiveness is claimed qualitatively; no leakage rate, inference accuracy, sample count, attack time, observation bandwidth, false-positive/false-negative rate, attacker overhead or mitigation result is reported.

**Limits on the conclusion:**

A page-table walk can change latency, memory traffic, cache state or contention, but a measurable difference is not automatically a useful security leak. The protected workload must affect the observation, the attacker must obtain it, noise must be controlled, and the signal must support the stated inference.

Analytics pipelines change with data partitions, parallel workers, scheduling, memory pressure and software versions. A result on one controlled configuration does not establish stability on unseen inputs, other workers, different co-tenants or different operating-system and page-size settings.

The official description reports no leakage rate, attack time, co-location requirement, observation interface, operating-system or processor configuration, or mitigation result. The record supports a plausible translation-based information path, not a generally practical attack against all analytics systems.

**Source and location**

Evidence tier: Primary captured official DAC description plus existing chapter level stone skimming discussion; no full paper extraction, controlled threat model validation or mitigation experiment. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH1793)

DAC 2026 official description; captured Problem, Mechanism / artifact, Workload, Hardware, Baseline, Measurements and Limits fields; record RESEARCH1793; no manuscript pages.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** noisy page-table observation

existing memory side channels

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH1793

**Hardware or process assumptions:** Paged virtual-memory system with observable timing or translation behavior; platform is unspecified.

**Limits:** No leakage rate, attack time, co-location requirement, or mitigation results are reported.

Practicality depends on OS and hardware details.

Official description only; controlled threat-model validation is required.

**Method or artifact:** Page-table-walk side-channel attack against big-data analytics applications.

**Metrics:** Attack effectiveness is claimed qualitatively

**Problem:** Page-table behavior can expose information about large analytics workloads.

**Workload or benchmark:** Big-data analytics workloads; operating systems, co-tenancy, and trace conditions are unspecified.

</details>

<span id="paper-dac-2026-research2107"></span>

### ODBP: Obfuscation Design Approach for Biochemical Protocols in Continuous-Flow Microfluidic Biochips

DAC 2026 · Record: `dac-2026-research2107`

[Read the step-by-step explanation](#explanation-dac-2026-research2107)

**Updated source-backed reading card**

Reviewed 2026-09-08. Deepens the existing ODBP treatment into a paper-level reading; defines a fluidic protocol as an ordered physical process, separates observer confusion from assay correctness, and specifies confidentiality, biochemical, overhead and variation measurements.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Biochemical protocols on microfluidic chips can reveal sensitive operations or reagent sequences.

**Mechanism / artifact:**

Protocol-obfuscation design for continuous-flow microfluidic biochips; schedule transformation, observer model, leakage definition and biochemical validation procedure are unspecified.

**Workload — the work tested:**

Biochemical protocols and fluidic schedules; assays, reagents, flow rates, protocol set, chip architecture, attacker observations and test conditions are unspecified.

**Hardware and manufacturing assumptions:**

Continuous-flow microfluidic biochip with controllable valves and flows; channel geometry, fabrication process, pressure/flow limits, valve faults, contamination model and assay conditions are unspecified.

**Baseline — the comparison method:**

Unobfuscated protocol

Randomized scheduling

Protocol set, attacker knowledge, chip architecture, biochemical conditions and comparison procedure are unspecified

**Reported measurements:**

Protocol obfuscation is claimed qualitatively; no leakage, inference accuracy, assay yield, output error, latency, reagent cost, control overhead, fabrication or variation result is reported.

**Limits on the conclusion:**

A protocol is an ordered physical process whose timing, fluid identity, mixing, residence time and routing affect the biochemical result. Hiding a control trace is not sufficient if the observer can use duration, channel use, added operations or reagent consumption, and it is not useful if obfuscation changes the assay outcome.

Confidentiality requires a defined observer, available signals, protected protocol set, prior knowledge and success criterion. Functional validity requires biochemical output checks under the same process conditions. A method that reduces one classifier's accuracy is not automatically a general confidentiality guarantee.

The official description reports no leakage measure, attacker model, assay result, yield, latency, reagent cost, fabrication condition or fault/variation experiment. The record supports a security-and-function co-design problem, not demonstrated confidentiality or validated biochemical improvement.

**Source and location**

Evidence tier: Primary captured official DAC description plus existing chapter level odbp discussion; no full paper extraction, biochemical validation or controlled threat model experiment. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH2107)

DAC 2026 official description; captured Problem, Mechanism / artifact, Workload, Hardware, Baseline, Measurements and Limits fields; record RESEARCH2107; no manuscript pages.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** unobfuscated protocol

randomized scheduling

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH2107

**Hardware or process assumptions:** Continuous-flow microfluidic biochip with controllable valves and flows; fabrication assumptions are unspecified.

**Limits:** No leakage, assay yield, latency, reagent cost, or fabrication results are reported.

Obfuscation may change fluidic timing or correctness.

Official description only; biochemical and threat-model validation is required.

**Method or artifact:** Protocol obfuscation design for continuous-flow microfluidic biochips.

**Metrics:** Protocol obfuscation is claimed qualitatively

**Problem:** Biochemical protocols on microfluidic chips can reveal sensitive operations or reagent sequences.

**Workload or benchmark:** Biochemical protocols and fluidic schedules; chip architecture, attacker model, and assay quality are unspecified.

</details>

<span id="paper-dac-2026-research213"></span>

### Exploiting Per-Core Leakage: Electromagnetic Side-Channel Monitoring of Multicore Architectures

DAC 2026 · Record: `dac-2026-research213`

[Read the step-by-step explanation](#explanation-dac-2026-research213)

**Updated source-backed reading card**

Reviewed 2026-09-08. Deepens the existing per-core electromagnetic-leakage treatment into a paper-level reading; separates physical signal detection, source attribution and secret recovery, and makes probe access, trace, device, noise and mitigation conditions explicit.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Multicore activity can leak through electromagnetic emissions and reveal computation or secrets.

**Mechanism / artifact:**

Per-core electromagnetic side-channel monitoring or attack method; probe setup, attribution method, signal processing, secret-recovery task and mitigation procedure are unspecified.

**Workload — the work tested:**

Multicore programs and secret-dependent computation; core placement, inputs, secrets, repetitions, simultaneous workloads and trace protocol are unspecified.

**Hardware and manufacturing assumptions:**

Multicore silicon with measurable electromagnetic leakage; processor, package, board, probe, bandwidth, distance, shielding, grounding, clock, voltage and temperature conditions are unspecified.

**Baseline — the comparison method:**

Aggregate electromagnetic monitoring

Power side-channel monitoring

Per-core attribution, attacker access, trace budget and comparison conditions are unspecified

**Reported measurements:**

Per-core leakage exploitation is claimed qualitatively; no leakage rate, trace count, probe distance, attribution accuracy, attack success, secret-recovery time, false-positive/false-negative rate or mitigation result is reported.

**Limits on the conclusion:**

Switching activity can create an electromagnetic signal, but the measured field is a mixture of cores, caches, memory, interconnects, clocks, regulators, package coupling and noise. Detecting activity or distinguishing two cores is not the same as recovering a protected secret.

A per-core claim needs a validated attribution method and an explicit physical threat model. Probe position, distance, bandwidth, shielding, sampling, device access and concurrent activity determine whether the result applies to a nearby laboratory probe, a shared device or a remote observer.

The official description reports no probe conditions, trace count, leakage rate, attack success, attribution method, package setup or mitigation result. The record supports a physical side-channel research direction, not established remote observability, reliable per-core separation or secret recovery.

**Source and location**

Evidence tier: Primary captured official DAC description plus existing chapter level electromagnetic monitoring discussion; no full paper extraction, controlled hardware measurement or mitigation validation. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH213)

DAC 2026 official description; captured Problem, Mechanism / artifact, Workload, Hardware, Baseline, Measurements and Limits fields; record RESEARCH213; no manuscript pages.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** aggregate EM monitoring

power side-channel monitoring

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH213

**Hardware or process assumptions:** Multicore silicon with measurable electromagnetic leakage; package and sensor assumptions are unspecified.

**Limits:** No leakage rate, trace count, distance, attack success, or mitigation results are reported.

Practicality depends on package and probe conditions.

Official description only; controlled hardware validation is required.

**Method or artifact:** Per-core electromagnetic side-channel monitoring or attack method.

**Metrics:** Per-core leakage exploitation is claimed qualitatively

**Problem:** Multicore activity can leak through electromagnetic emissions and reveal computation or secrets.

**Workload or benchmark:** Multicore programs and secret-dependent computation; processor, probe, and co-location assumptions are unspecified.

</details>

<span id="paper-dac-2026-research2369"></span>

### Reconnaissance: Correctly Tracking Multiple Secrets Using Reveal/conceal Paradigms

DAC 2026 · Record: `dac-2026-research2369`

[Read the step-by-step explanation](#explanation-dac-2026-research2369)

**Updated source-backed reading card**

Reviewed 2026-09-08. Deepens the existing Reconnaissance treatment into a paper-level reading; defines multi-secret information-flow tracking, separates permitted reveal from protected concealment, and makes soundness, precision, semantics and scalability requirements explicit.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Security analyses must track multiple secret values while distinguishing intentional reveal from protected state.

**Mechanism / artifact:**

Reveal/conceal paradigm for multi-secret tracking or information-flow analysis; label semantics, transfer rules, declassification policy, attacker observation and proof model are unspecified.

**Workload — the work tested:**

Hardware or software designs with multiple secrets; language, control flow, memory, concurrency, policies, case studies and reference judgments are unspecified.

**Hardware and manufacturing assumptions:**

Security-analysis or information-flow tooling; execution, memory, concurrency, speculation and observation assumptions are unspecified.

**Baseline — the comparison method:**

Single-secret tracking

Standard information-flow analysis

Soundness reference, precision reference, policy model and scalability conditions are unspecified

**Reported measurements:**

Multi-secret tracking capability is claimed qualitatively; no soundness proof, precision result, runtime, memory, label-scaling, false-alarm rate, missed-flow rate or case-study result is reported.

**Limits on the conclusion:**

Multiple secrets need identity and dependency information: an output may depend on secret A, secret B, both or a relation between them. Treating all secrets as one label can lose this distinction. Reveal and conceal are policy semantics, not proof that the implementation follows the policy.

Soundness asks whether forbidden flows are detected under the stated model; precision asks whether permitted or impossible flows are avoided. Comparisons, aliases, control predicates, arrays, exceptions, concurrency and intentional declassification can change the result, so the language and observation model must be explicit.

The official description reports no formal label semantics, soundness proof, precision study, runtime, scalability result or case study. The record supports a policy-aware multi-secret analysis direction, not established complete flow detection or meaningfulness of every reported warning.

**Source and location**

Evidence tier: Primary captured official DAC description plus existing chapter level reveal/conceal discussion; no full paper extraction, formal proof or implementation validation. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH2369)

DAC 2026 official description; captured Problem, Mechanism / artifact, Workload, Hardware, Baseline, Measurements and Limits fields; record RESEARCH2369; no manuscript pages.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** single-secret tracking

standard information-flow analysis

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH2369

**Hardware or process assumptions:** Security-analysis or information-flow tooling; execution and memory assumptions are unspecified.

**Limits:** No soundness, precision, runtime, scalability, or case-study results are reported.

Reveal semantics may be domain-specific.

Official description only; formal and implementation validation is required.

**Method or artifact:** Reveal/conceal paradigm for multi-secret tracking or analysis.

**Metrics:** Multi-secret tracking capability is claimed qualitatively

**Problem:** Security analyses must track multiple secret values while distinguishing intentional reveal from protected state.

**Workload or benchmark:** Hardware or software designs with multiple secrets; language, attacker, and proof setting are unspecified.

</details>

<span id="paper-dac-2026-research3019"></span>

### Decoding the Past: Recovering Sensitive Data from SRAM Aging Imprints

DAC 2026 · Record: `dac-2026-research3019`

[Read the step-by-step explanation](#explanation-dac-2026-research3019)

**Updated source-backed reading card**

Reviewed 2026-09-08. Deepens the existing SRAM-aging treatment into a paper-level reading; separates residual charge from history-dependent aging, defines the readout and inference chain, and makes device variation, retention horizon, recovery metrics and sanitization tests explicit.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Aging-dependent SRAM patterns may retain information about previously stored sensitive data.

**Mechanism / artifact:**

Attack or forensic method recovering data from SRAM aging imprints; cell-aging mechanism, readout sensor, calibration, inference model and sanitization test are unspecified.

**Workload — the work tested:**

SRAM devices and prior data patterns; stress duration, data structure, intervening writes, power cycles, age, temperature, voltage, access procedure and attacker model are unspecified.

**Hardware and manufacturing assumptions:**

SRAM memory with measurable aging variation; cell design, process, supply, temperature, memory controller, sensor and readout assumptions are unspecified.

**Baseline — the comparison method:**

Fresh SRAM readout

Conventional remanence attacks

Recovery target, chance baseline, calibration, cross-device transfer and access conditions are unspecified

**Reported measurements:**

Sensitive-data recovery is claimed qualitatively; no bit error rate, recovery accuracy, block/message recovery, cell/read count, age, retention horizon, calibration cost, cross-device result or mitigation result is reported.

**Limits on the conclusion:**

An aging imprint is not ordinary residual charge. It would be a weak relationship between earlier electrical stress and later cell behavior, which can be confounded by process mismatch, retention, read disturb, supply noise and the sensor. The physical aging mechanism and alternative causes must be identified.

A recovery claim needs an access path, readout, calibration and inference rule. A rate above random guessing on selected bits does not establish recovery of a key, file or structured record. Accuracy must be measured across time, devices, SRAM blocks, stress patterns and unseen chips.

The official description reports no recovery accuracy, age or retention horizon, access requirement, sensor, process condition, calibration procedure or mitigation result. The record supports a hardware-forensics hypothesis, not established recovery from ordinary SRAM or a proven sanitization failure.

**Source and location**

Evidence tier: Primary captured official DAC description plus existing chapter level sram aging discussion; no full paper extraction, controlled hardware forensics experiment or mitigation validation. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH3019)

DAC 2026 official description; captured Problem, Mechanism / artifact, Workload, Hardware, Baseline, Measurements and Limits fields; record RESEARCH3019; no manuscript pages.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** fresh SRAM readout

conventional remanence attacks

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH3019

**Hardware or process assumptions:** SRAM memory with measurable aging variation; sensor and readout assumptions are unspecified.

**Limits:** No recovery accuracy, age, retention horizon, access requirements, or mitigation results are reported.

Aging signatures may vary by process and environment.

Official description only; hardware and threat-model validation is required.

**Method or artifact:** Attack or forensic method recovering data from SRAM aging imprints.

**Metrics:** Sensitive-data recovery is claimed qualitatively

**Problem:** Aging-dependent SRAM patterns may retain information about previously stored sensitive data.

**Workload or benchmark:** SRAM devices and prior data patterns; process, age, access, and attacker model are unspecified.

</details>

<span id="paper-dac-2026-research315"></span>

### Capacitive Touchscreens at Risk: Recovering Handwritten Trajectory on Smartphone via Electromagnetic Emanations

DAC 2026 · Record: `dac-2026-research315`

[Read the step-by-step explanation](#explanation-dac-2026-research315)

**Updated source-backed reading card**

Reviewed 2026-09-08. Deepens the existing touchscreen-emanation treatment into a paper-level reading; defines capacitive scanning and the signal-to-trajectory inference chain, and makes physical access, user/device generalization and reconstruction metrics explicit.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Touchscreen electromagnetic emissions may reveal sensitive user input.

**Mechanism / artifact:**

Electromagnetic side-channel recovery of touch trajectories; touchscreen scan behavior, sensor, probe, coordinate-reconstruction model and mitigation procedure are unspecified.

**Workload — the work tested:**

Smartphone handwriting and touchscreen traces; phone model, screen stack, users, phrases, writing sessions, orientations and test protocol are unspecified.

**Hardware and manufacturing assumptions:**

Capacitive touchscreen and EM sensing setup; probe, distance, orientation, bandwidth, shielding, case, display state, background activity and attacker access are unspecified.

**Baseline — the comparison method:**

Noisy EM observation

Touchscreen software logging

Device, probe, calibration, user split, cross-device and comparison conditions are unspecified

**Reported measurements:**

Trajectory recovery is claimed qualitatively; no coordinate error, point precision/recall, temporal alignment, phrase recovery, recovery accuracy, distance, equipment, user diversity, trace count or mitigation result is reported.

**Limits on the conclusion:**

A capacitive controller scans electrodes and estimates touch locations; its switching may create an electromagnetic trace. A correlation with touch activity is not trajectory recovery. A trajectory requires time-ordered position reconstruction and separation from display, processor, radio, enclosure, user and environmental effects.

Physical access is part of the security claim. Probe position, distance, orientation, bandwidth, shielding, phone model, case and attacker control determine whether the result applies to one laboratory setup, a nearby observer or a remote attacker. Training must be separated by session, user and device to establish generalization.

The official description reports no recovery accuracy, distance, equipment, user diversity, cross-device result or mitigation result. The record supports a physical side-channel hypothesis, not established remote trajectory recovery, general handwriting reconstruction or a demonstrated protection failure.

**Source and location**

Evidence tier: Primary captured official DAC description plus existing chapter level touchscreen emanation discussion; no full paper extraction, controlled hardware validation or mitigation experiment. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH315)

DAC 2026 official description; captured Problem, Mechanism / artifact, Workload, Hardware, Baseline, Measurements and Limits fields; record RESEARCH315; no manuscript pages.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** noisy EM observation

touchscreen software logging

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH315

**Hardware or process assumptions:** Capacitive touchscreen and EM sensing setup; shielding and attacker access are unspecified.

**Limits:** No recovery accuracy, distance, equipment, user diversity, or mitigation results are reported.

Practicality depends on device and probe placement.

Official description only; controlled hardware validation is required.

**Method or artifact:** Electromagnetic side-channel recovery of touch trajectories.

**Metrics:** Trajectory recovery is claimed qualitatively

**Problem:** Touchscreen electromagnetic emissions may reveal sensitive user input.

**Workload or benchmark:** Smartphone handwriting and touchscreen traces; device, probe, distance, and user set are unspecified.

</details>

<span id="paper-dac-2026-research462"></span>

### SCIMI: Semantic-Aware Collaborative Intrusion Detection for Multi-Domain In-Vehicle Networks

DAC 2026 · Record: `dac-2026-research462`

[Read the step-by-step explanation](#explanation-dac-2026-research462)

**Updated source-backed reading card**

Reviewed 2026-09-08. Deepens the existing SCIMI treatment into a paper-level reading; defines semantic vehicle context, separates local detection from collaborative evidence exchange, and makes communication attack surface, safety, latency and vehicle validation explicit.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Vehicle networks span domains with heterogeneous traffic and need collaborative intrusion detection.

**Mechanism / artifact:**

Semantic-aware collaborative intrusion-detection system; message semantics, context model, evidence exchanged, trust mechanism, fusion rule and response behavior are unspecified.

**Workload — the work tested:**

In-vehicle network traffic and attacks; vehicle architecture, domains, operating modes, benign mode changes, attack set, labels, traces and communication conditions are unspecified.

**Hardware and manufacturing assumptions:**

Automotive network controllers and collaborative detection nodes; compute, network latency, bandwidth, authentication, safety response and platform validation assumptions are unspecified.

**Baseline — the comparison method:**

Local intrusion-detection system

Signature-based intrusion-detection system

Vehicle architecture, attack set, compute budget, latency, communication and evaluation conditions are unspecified

**Reported measurements:**

Intrusion-detection effectiveness is claimed qualitatively; no detection rate, false-positive rate, missed attacks, alert latency, bandwidth, processor/memory cost, compromised-node result or vehicle result is reported.

**Limits on the conclusion:**

Semantic detection depends on a defined message vocabulary, signal meaning, operating mode, state model and trusted sources. The same traffic can be valid in one mode and suspicious in another; incomplete or wrong semantics can create false alarms or missed attacks.

Collaboration can expose cross-domain patterns, but exchanged evidence adds delay, bandwidth, synchronization and attack surface. A compromised node can forge, suppress, replay or poison evidence, so identity, freshness, trust, disagreement and channel-failure behavior must be defined.

The official description reports no detection rate, false positives, latency, bandwidth, compromised-node test, attack set or vehicle result. The record supports context-aware distributed detection, not safe deployment, improved vehicle-level detection or resistance to attacks on collaboration.

**Source and location**

Evidence tier: Primary captured official DAC description plus existing chapter level collaborative ids discussion; no full paper extraction, threat model validation or vehicle experiment. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH462)

DAC 2026 official description; captured Problem, Mechanism / artifact, Workload, Hardware, Baseline, Measurements and Limits fields; record RESEARCH462; no manuscript pages.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** local IDS

signature-based IDS

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH462

**Hardware or process assumptions:** Automotive network controllers and collaborative detection nodes; latency and safety assumptions are unspecified.

**Limits:** No detection rate, false positives, latency, bandwidth, or vehicle results are reported.

Semantic collaboration may expose additional attack surface.

Official description only; threat-model and vehicle validation is required.

**Method or artifact:** Semantic-aware collaborative intrusion-detection system.

**Metrics:** Intrusion-detection effectiveness is claimed qualitatively

**Problem:** Vehicle networks span domains with heterogeneous traffic and need collaborative intrusion detection.

**Workload or benchmark:** In-vehicle network traffic and attacks; vehicle architecture, labels, and communication are unspecified.

</details>

<span id="paper-dac-2026-research625"></span>

### Attestllm: Efficient Attestation Framework for Billion-Scale On-Device LLMs

DAC 2026 · Record: `dac-2026-research625`

[Read the step-by-step explanation](#explanation-dac-2026-research625)

**Updated source-backed reading card**

Reviewed 2026-09-08. Deepens the existing AttestLLM treatment into a paper-level reading; defines trusted measurement and evidence binding, separates model artifact integrity from runtime behavior integrity, and makes model-scale, update, freshness and tamper-validation requirements explicit.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

On-device LLM deployments need integrity and provenance attestation without large inference overhead.

**Mechanism / artifact:**

Efficient attestation framework for large on-device LLMs; measured components, commitment structure, hardware root of trust, verifier protocol, freshness and update/rollback behavior are unspecified.

**Workload — the work tested:**

Billion-scale LLM models on edge devices; model formats, quantization, adapters, tokenizer, runtime, accelerator, update flow and inference workload are unspecified.

**Hardware and manufacturing assumptions:**

Secure embedded device with model storage and attestation; root of trust, secure boot, TEE, keys, storage, accelerator, network and offline behavior are unspecified.

**Baseline — the comparison method:**

Full-model hashing

Unattested deployment

Attacker capability, device configuration, model lifecycle and comparison conditions are unspecified

**Reported measurements:**

Attestation efficiency is claimed qualitatively; no security proof, attestation latency, memory traffic, energy, proof size, verifier time, update cost, freshness, tamper-detection or device result is reported.

**Limits on the conclusion:**

Attestation evidence can bind a signed measurement to an approved artifact only if the measured component, reference, device key, freshness and execution chain are defined. A model digest does not by itself prove that the approved bytes were loaded on every path or that later runtime changes are impossible.

Efficient measurement of a billion-scale model may hash chunks, metadata, a tree or selected regions. Each choice changes what an attacker can alter without detection. Provenance also includes tokenizer, preprocessing, quantization, adapters, compiler, runtime, libraries, configuration, update authorization and rollback state.

Model integrity does not prove prompt privacy, output correctness, absence of runtime bugs, faithful accelerator execution or safety of the approved model. The official description reports no security proof, performance, freshness, update, tamper-detection or device result; the record supports an attestation direction, not end-to-end runtime trust or deployment readiness.

**Source and location**

Evidence tier: Primary captured official DAC description plus existing chapter level on device model attestation discussion; no full paper extraction, security proof or device validation. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH625)

DAC 2026 official description; captured Problem, Mechanism / artifact, Workload, Hardware, Baseline, Measurements and Limits fields; record RESEARCH625; no manuscript pages.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** full-model hashing

unattested deployment

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH625

**Hardware or process assumptions:** Secure embedded device with model storage and attestation; TEE and network assumptions are unspecified.

**Limits:** No security proof, attestation latency, memory, energy, update, or device results are reported.

Model integrity may not imply runtime behavior integrity.

Official description only; threat-model and device validation is required.

**Method or artifact:** Efficient attestation framework for large on-device LLMs.

**Metrics:** Attestation efficiency is claimed qualitatively

**Problem:** On-device LLM deployments need integrity and provenance attestation without large inference overhead.

**Workload or benchmark:** Billion-scale LLM models on edge devices; hardware root of trust, updates, and attacker are unspecified.

</details>

<span id="paper-dac-2026-research663"></span>

### Emudrop: A Minimalistic, Hardware-Based Emulation Detection Approach Through Intel Reserved Opcodes

DAC 2026 · Record: `dac-2026-research663`

[Read the step-by-step explanation](#explanation-dac-2026-research663)

**Updated source-backed reading card**

Reviewed 2026-09-08. Deepens the existing Emudrop treatment into a paper-level reading; defines reserved-opcode behavior as an environment fingerprint, separates mismatch detection from universal emulation detection, and makes CPU, OS, privilege, hypervisor, evasion and false-positive conditions explicit.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Malware and software may evade analysis by detecting virtualized or emulated environments.

**Mechanism / artifact:**

Minimal hardware-based emulator-detection technique using reserved opcodes; exact opcode, exception handling, reference behavior, privilege, timing and evasion assumptions are unspecified.

**Workload — the work tested:**

Intel-compatible systems and emulators; CPU generations, operating systems, privilege levels, hypervisors, full/user-mode emulators, sandboxes, translators and attacker-aware variants are unspecified.

**Hardware and manufacturing assumptions:**

Intel CPU supporting reserved-opcode behavior; execution mode, exception path, OS, virtualization, binary translation and sandbox assumptions are unspecified.

**Baseline — the comparison method:**

Software emulator checks

CPUID-based checks

CPU/emulator coverage, attacker budget, privilege, exception and comparison conditions are unspecified

**Reported measurements:**

Emulation-detection effectiveness is claimed qualitatively; no detection rate, false-positive rate, false-negative rate, portability, privilege, overhead, exception behavior, evasion or mitigation result is reported.

**Limits on the conclusion:**

A reserved opcode can expose a difference between native and emulated instruction handling, but the result depends on CPU generation, mode, operating system, exception delivery, hypervisor policy, translation and sandbox restrictions. It is a compatibility fingerprint, not direct proof that an environment is virtualized.

An emulator or analysis system can reproduce the expected exception, intercept or rewrite the instruction, or recognize the detector. Native machines that differ from the reference can create false positives. The security meaning therefore depends on the attacker and defender budgets and the exact environment set tested.

The official description reports no detection rate, false positives, CPU or emulator coverage, privilege requirement, timing, evasion test or mitigation result. The record supports a hardware-fingerprint direction, not portable detection of all emulation or a general malware-evasion capability.

**Source and location**

Evidence tier: Primary captured official DAC description plus existing chapter level reserved opcode discussion; no full paper extraction, cross platform validation or detector aware evasion experiment. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH663)

DAC 2026 official description; captured Problem, Mechanism / artifact, Workload, Hardware, Baseline, Measurements and Limits fields; record RESEARCH663; no manuscript pages.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** software emulator checks

CPUID-based checks

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH663

**Hardware or process assumptions:** Intel CPU supporting reserved-opcode behavior; OS and virtualization assumptions are unspecified.

**Limits:** No detection rate, false positives, portability, privilege, or mitigation results are reported.

Reserved-opcode behavior may vary across CPUs and hypervisors.

Official description only; cross-platform validation is required.

**Method or artifact:** Minimal hardware-based emulator-detection technique using reserved opcodes.

**Metrics:** Emulation-detection effectiveness is claimed qualitatively

**Problem:** Malware and software may evade analysis by detecting virtualized or emulated environments.

**Workload or benchmark:** Intel-compatible systems and emulators; versions, privileges, and attacker model are unspecified.

</details>

<span id="paper-dac-2026-research681"></span>

### Mistletunnel: Attacking KASLR on Apple M-Series Silicon with a Novel TLB Side Channel

DAC 2026 · Record: `dac-2026-research681`

[Read the step-by-step explanation](#explanation-dac-2026-research681)

**Updated source-backed reading card**

Reviewed 2026-09-08. Deepens the existing Mistletunnel treatment into a paper-level reading; defines KASLR and TLB translation leakage, separates a timing correlation from kernel-address recovery, and makes Apple silicon, OS, privilege, noise and mitigation boundaries explicit.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Address-space randomization can be weakened by microarchitectural translation leakage.

**Mechanism / artifact:**

Novel TLB side-channel attack against KASLR; observation method, translation-state sharing, address-recovery procedure, victim access and follow-on exploit condition are unspecified.

**Workload — the work tested:**

Apple M-series systems and victim software; chip generations, OS versions, randomized layouts, victim workload, co-location, permissions and noise conditions are unspecified.

**Hardware and manufacturing assumptions:**

Apple silicon TLB and memory system; TLB levels, page sizes, invalidation, scheduler, core placement, privilege, timing interface and attacker access are unspecified.

**Baseline — the comparison method:**

Cache side channels

Existing KASLR attacks

Victim, access, noise, time, success criterion and mitigation conditions are unspecified

**Reported measurements:**

KASLR recovery effectiveness is claimed qualitatively; no address-recovery rate, confidence, time, sample count, noise tolerance, privilege, false-recovery rate, cross-platform result or mitigation result is reported.

**Limits on the conclusion:**

KASLR hides the randomized placement of kernel components. A TLB hit/miss or contention signal may reveal translation activity, but a correlation with activity is weaker than recovering the kernel base or enabling a follow-on exploit. The address hypothesis, error rate and attacker observation path must be explicit.

TLB behavior depends on processor, OS, page size, invalidation, scheduling, privilege, co-location and concurrent activity. Apple M-series and OS-specific results cannot automatically be generalized to all Apple silicon or KASLR deployments.

The official description reports no address-recovery rate, time, noise tolerance, privilege, cross-platform coverage or mitigation result. The record supports a platform-specific translation-leakage direction, not general KASLR defeat or a usable exploit chain.

**Source and location**

Evidence tier: Primary captured official DAC description plus existing chapter level tlb/kaslr discussion; no full paper extraction, controlled hardware validation or mitigation experiment. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH681)

DAC 2026 official description; captured Problem, Mechanism / artifact, Workload, Hardware, Baseline, Measurements and Limits fields; record RESEARCH681; no manuscript pages.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** cache side channels

existing KASLR attacks

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH681

**Hardware or process assumptions:** Apple silicon TLB and memory system; OS version and attacker access are unspecified.

**Limits:** No address-recovery rate, time, noise tolerance, privilege, or mitigation results are reported.

Results may be OS- and silicon-specific.

Official description only; controlled hardware validation is required.

**Method or artifact:** Novel TLB side-channel attack against KASLR.

**Metrics:** KASLR recovery effectiveness is claimed qualitatively

**Problem:** Address-space randomization can be weakened by microarchitectural translation leakage.

**Workload or benchmark:** Apple M-series systems and victim software; privileges, co-location, and noise are unspecified.

</details>

<span id="paper-dac-2026-research876"></span>

### Tdsnap: Enabling Secure Function-as-a-Service with Trusted Domain Snapshots

DAC 2026 · Record: `dac-2026-research876`

[Read the step-by-step explanation](#explanation-dac-2026-research876)

**Updated source-backed reading card**

Reviewed 2026-09-08. Deepens the existing Tdsnap treatment into a paper-level reading; defines trusted FaaS snapshot state, separates confidentiality/integrity from freshness and external side effects, and makes isolation proof, metadata leakage, rollback and efficiency requirements explicit.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

FaaS systems need fast isolation and state handling while preserving confidentiality across tenants.

**Mechanism / artifact:**

Trusted-domain snapshot mechanism for secure FaaS; trusted boundary, captured state, key handling, integrity/freshness protocol, external-side-effect coordination and restore behavior are unspecified.

**Workload — the work tested:**

Function-as-a-service workloads; state sizes, runtimes, open connections, storage, device use, concurrent tenants, failures and cold-start targets are unspecified.

**Hardware and manufacturing assumptions:**

Trusted execution or hardware-isolated domain; memory, storage, hypervisor, network, key, rollback, I/O and trust-boundary assumptions are unspecified.

**Baseline — the comparison method:**

Process isolation

Standard VM snapshots

Function, state, concurrency, threat model, storage, network and performance conditions are unspecified

**Reported measurements:**

Secure FaaS efficiency is claimed qualitatively; no isolation proof, snapshot/restore latency, memory, storage, bandwidth, energy, rollback, metadata-leakage or workload result is reported.

**Limits on the conclusion:**

A FaaS snapshot includes more than memory: registers, runtime metadata, connections, pending work, credentials, device state and external effects may matter. The trusted boundary must state what is captured, who copies it and how saved state is protected.

Encryption supports confidentiality but does not prevent replacement, replay or stale restoration. Integrity and freshness must bind state and metadata to the correct instance, version or epoch. External database writes, messages, timers and one-time actions need coordination to avoid duplicate or lost effects.

The official description reports no isolation proof, snapshot latency, memory overhead, rollback handling, metadata leakage, threat-model detail or workload result. The record supports secure state migration, not established confidential, rollback-safe or production-efficient FaaS snapshots.

**Source and location**

Evidence tier: Primary captured official DAC description plus existing chapter level trusted domain snapshot discussion; no full paper extraction, isolation proof or system validation. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH876)

DAC 2026 official description; captured Problem, Mechanism / artifact, Workload, Hardware, Baseline, Measurements and Limits fields; record RESEARCH876; no manuscript pages.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** process isolation

standard VM snapshots

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH876

**Hardware or process assumptions:** Trusted execution or hardware-isolated domain; memory and rollback assumptions are unspecified.

**Limits:** No isolation proof, snapshot latency, memory, rollback, or workload results are reported.

Snapshot metadata may leak state.

Official description only; threat-model and system validation is required.

**Method or artifact:** Trusted-domain snapshot mechanism for secure FaaS.

**Metrics:** Secure FaaS efficiency is claimed qualitatively

**Problem:** FaaS systems need fast isolation and state handling while preserving confidentiality across tenants.

**Workload or benchmark:** Function-as-a-service workloads; TEE, snapshots, and attacker model are unspecified.

</details>

## What remains to establish

Resolve unspecified workloads, comparison methods, resource budgets, and source locations before generalizing a reported gain. Multiple papers in this selected sample permit comparison of mechanisms, but do not by themselves establish recurrence across years or a long-term trend.

[All subthemes](../expanded-taxonomy-v1.md) · [Research directions](../directions/README.md)
