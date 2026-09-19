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
