# Confidential and trusted computing

This subject has 1 record in the selected sample. This page explains where it fits, then presents all captured paper evidence without shortening the measurements or limitations.

[Definitions used in the paper records](../reading-guide-v1.md)

## Understand the parent subject first

- [Systems applications and workloads](../themes/systems-applications-and-workloads.md)

## Moving a running computation without weakening its protection

A virtual machine is a software-visible computer whose processor time, memory, and devices are supplied by a physical host. Migration transfers its running state to another host. That state includes more than program files: memory contents, processor registers, and the information needed to continue outstanding work must agree at the point of resumption.

A confidential virtual machine adds a protection requirement: some host-controlled components must not be able to read or alter protected guest state. Which components and which alterations are excluded depend on the particular hardware and security model. The word “confidential” alone does not promise integrity, availability, or protection against every indirect observation.

This subject's single paper concerns migration across different confidential-computing implementations. The first-principles discussion below develops the requirements such a system should satisfy; it is not a reconstruction of an unavailable protocol or a claim that the paper implements every check described.

## Compatibility has both a functional and a security meaning

Functional compatibility means the destination can represent and resume the computation. It must interpret transferred state correctly and provide the processor and device behavior the guest expects. Sharing an instruction-set family does not by itself establish that every processor feature, virtual device, or protected-state format matches.

Security compatibility asks a different question: does the destination enforce the protections the workload owner requires? Copying protected bytes successfully is insufficient if the new host allows an actor to read or modify information that was previously protected.

A trusted execution environment, abbreviated TEE, is the hardware-and-software environment on which specified execution protections depend. A trusted computing base is the set of components whose correct behavior is necessary for a security claim. Calling a migration helper trusted therefore identifies a dependency to examine, not a demonstration that the helper is correct.

For review, write the required properties separately: who may read state, who may change it, who may authorize a destination, and whether an old state may be resumed. Then ask whether each property holds before transfer, during transfer, and after resumption. This exposes a weaker destination or a less protected intermediate step that a simple “migration succeeded” test would miss.

## What the DAC paper actually establishes in the available description

[Towards Practical Live Migration for Heterogeneous Confidential Virtual Machines](../observed-subthemes/confidential-and-trusted-computing.md#paper-dac-2026-research2079) proposes a framework for heterogeneous x86 TEEs. Its prototype migrates between AMD SEV and Hygon CSV using a trusted helper that emulates required firmware migration commands and handles compatibility differences. The description claims security comparable to homogeneous migration and acceptable overhead, but supplies no numerical measurements or detailed security argument. [Official DAC description](https://63dac.conference-program.com/presentation/?id=RESEARCH2079&sess=sess108).

This is evidence of the stated prototype and approach, not demonstrated support for every x86 TEE. The description does not identify precise processor generations, firmware versions, permitted migration directions, or security-feature variants. In particular, its use of the SEV name must not be silently expanded into a claim about SEV-SNP or Intel TDX. The author's [publication list](https://yinqian.org/pubs.html) confirms the title but provides no linked manuscript for this entry. No paper pages or tables were recovered in this pass.

<span id="explanation-dac-2026-research2079"></span>

## Heterogeneous confidential-VM migration: translate state without changing the trust claim

### Migration has a functional state problem and a security state problem

To migrate a running virtual machine, the source must transfer enough state for the destination to continue execution. That includes memory pages, processor registers, virtual-device state, interrupt state, and the bookkeeping needed to resume outstanding operations. If the destination interprets any of these differently, the guest may fail even when the bytes were copied exactly.

A confidential VM adds a second requirement. The bytes and execution state must remain protected from host components that the source TEE excluded from the trusted computing base. A destination that resumes the program but changes who can inspect memory has functional continuity without security continuity. A migration result therefore needs separate claims for state completeness, execution behavior, confidentiality, integrity, authorization and failure handling.

### Heterogeneous TEEs expose representation and policy differences

The DAC description proposes migration between AMD SEV and Hygon CSV through a trusted helper that emulates required firmware migration commands and handles compatibility differences. The helper is a translation boundary: it must understand the source's protected-state representation and produce a destination state that the other TEE accepts. It may also need to translate device or firmware operations that are not identical across vendors.

The translation boundary changes the trust question. The helper now participates in the migration protocol and may see, transform, authorize or reject sensitive state. The system must specify which operations it can perform, how its code and configuration are authenticated, which host components can influence it, and how the destination proves that it is the intended environment. Calling it trusted identifies a requirement; it does not prove that the requirement is satisfied.

The source uses SEV and CSV names, but the captured description does not identify processor generations, firmware versions, migration directions or security-feature variants. The result is not expanded to SEV-SNP, Intel TDX or every x86 TEE. Compatibility across an instruction-set family is also insufficient evidence because protected-state formats, virtual devices and attestation procedures can differ.

### Authorization must be connected to the state transfer

Attestation provides evidence about a platform's measured or configured execution environment. Authorization is the policy decision that the workload owner permits that environment to receive the VM. A secure channel protects bytes in transit but does not decide whether the endpoint is authorized. A migration framework must connect destination identity, attestation evidence, policy evaluation, key release and state restoration.

The review questions are concrete: who validates the destination, which measurement changes cause rejection, where transfer keys are generated, whether the helper handles plaintext or decrypted state, and how the source knows which destination completed restoration. The available description does not provide this protocol or a detailed threat argument, so “security comparable to homogeneous migration” remains an author claim rather than a verified equivalence result.

### Live migration has a moving-state and failure problem

While memory is being copied, the guest can continue writing pages. The system may copy dirty pages again, pause the guest briefly for a final state transfer, and then resume at the destination. The write rate, effective network bandwidth, guest size, and pause policy determine whether the remaining dirty state shrinks and whether the user-visible interruption is acceptable.

Total transfer time, downtime, application response time and total transferred bytes are different measurements. The description reports no numeric values for them. A complete evaluation should also cover interrupted migration, destination rejection, source failure, duplicate resumption, stale-state rollback and external effects that cannot safely be repeated. These are required evaluation dimensions, not claims that the paper's prototype fails them.

### What the paper establishes and what remains open

The accessible description establishes a proposed heterogeneous live-migration framework and an AMD SEV-to-Hygon CSV prototype using a trusted migration helper. It does not establish a formal security equivalence, complete attestation/key protocol, broad TEE portability, measured downtime or bandwidth overhead, failure-state semantics, or independent cloud deployment. A stronger evaluation would publish the protocol and threat model, helper privileges and code boundary, platform/firmware versions, migration directions, cryptographic operations, workload write rates, pause and total-time distributions, failure tests, and independent implementation checks.

[Official DAC description](https://63dac.conference-program.com/presentation/?id=RESEARCH2079&sess=sess108) · [Author publication list](https://yinqian.org/pubs.html)

## The transfer protocol must connect destination identity to permission

Consider a workload owner who permits migration only to machines satisfying a stated policy. A destination needs more than a reachable network address. The review must determine how evidence about its identity and configuration is checked and how that evidence is connected to the recipient of the protected state. Attestation is evidence used to assess an execution environment; it is not, by itself, the owner's permission to transfer a workload there.

These are evaluation questions, not assertions about this prototype: who verifies the destination, which configuration changes cause rejection, where transfer keys are created, and whether the helper ever handles unprotected guest data. A secure network channel cannot compensate for sending data to an unauthorized endpoint. Similarly, encrypting transferred memory does not establish that the restored state is complete, current, or internally consistent.

Failure behavior matters as much as the successful path. If the source stops but the destination fails before resuming, the system needs a defined recovery outcome. If both resume, two copies may make conflicting externally visible decisions. If an older captured state can be resumed, the application may repeat work it already completed. A review should check these cases against the promised security and application semantics, without assuming this paper claims to prevent every form of duplication or rollback.

## Live migration does not mean zero interruption

Total migration time measures the complete transfer process. Downtime measures the interval during which the guest cannot provide its normal service. Application response time measures what a client experiences. These quantities can move differently: a longer background transfer may reduce the final pause while consuming resources that slow ordinary requests.

As an independent simplifying model, suppose migration repeatedly copies memory while the guest continues modifying it. Let B be the effective copy rate and D the rate at which bytes become modified again, in the same units. If D stays at or above B, repeated copying alone does not guarantee that the remaining state shrinks. This model is not a claim about the paper's migration algorithm. It explains why workload write behavior and effective bandwidth are necessary experimental conditions, rather than optional implementation details.

An adequate comparison would keep guest size, workload, processor allocation, network, and required protection comparable. It should report the pause, total transferred bytes, completion time, application performance, and failed or interrupted transfers. Separate helper processing from network and host differences where possible. “Acceptable” overhead cannot answer whether an application with a particular interruption limit can use the system.

## What this case suggests, and what remains unproven

The conceptual connection to cloud scheduling is direct: migration adds placement choices only when the destination can both execute the workload and satisfy its protection policy. The resulting research question is how much operational flexibility can be gained without adding unacceptable trusted components, interruption, or weaker guarantees. One case does not establish a long-term trend or general vendor independence.

The historical card below suggests dependence on undocumented vendor behavior. The recovered description does not establish that dependence; treat it as an unverified concern, not a finding. The helper's exact privileges, protection, and contribution to the trusted computing base require the full protocol. Page-backed threat assumptions, failure-state analysis, workload conditions, and independent implementation checks remain open. This article does not substitute a qualitative abstract for those missing results.

## Compare the results carefully

First identify the inputs and required output quality. Then identify the limited resource: time, memory, communication, energy, circuit area, or correctness coverage. Ask which part of the method reduces that cost and which new cost it adds. Compare numbers only when the experiments hold these conditions sufficiently similar.

A conference description may explain the proposal while omitting the full experiment. An author preprint link may have been coded from its abstract. The source classification does not by itself establish that every table was read. Missing locations remain visible below.

## Complete captured evidence

These are evidence records, not substitutes for the explanations above. Each record preserves its problem, proposed method, measurements, comparison conditions, and source limits. A populated record does not establish that its mechanism has been fully explained or independently verified.

<span id="paper-dac-2026-research2079"></span>

### Towards Practical Live Migration for Heterogeneous Confidential Virtual Machines

DAC 2026 · Record: `dac-2026-research2079`

[Read the step-by-step explanation](#explanation-dac-2026-research2079)

**Updated source-backed reading card**

Reviewed 2026-09-08. Deepens the official-description reading; separates functional state transfer, cross-TEE translation, destination authorization, attestation, live-migration cost and security-equivalence limits.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

TEE-vendor-specific confidential VMs support migration mainly within homogeneous stacks, limiting cloud placement across heterogeneous confidential hardware.

**Mechanism / artifact:**

Generic heterogeneous-migration framework and trusted migration helper bridging AMD SEV and Hygon CSV command semantics and compatibility differences.

**Workload — the work tested:**

Live migration between AMD SEV and Hygon CSV confidential VMs; VM workloads, guest write rates, downtime, bandwidth, migration directions and failure cases are unspecified.

**Hardware and manufacturing assumptions:**

x86 confidential VMs, vendor TEE firmware, trusted migration helper and cloud migration path; CPU generations, firmware versions, attestation, key handling and protected-state formats are unspecified.

**Baseline — the comparison method:**

Homogeneous CVM migration

Vendor-specific migration support

**Reported measurements:**

Comparable security guarantees and acceptable performance overhead are claimed qualitatively; an AMD SEV-to-Hygon CSV prototype is described, with no numeric downtime, bandwidth, cryptographic or application-overhead measurements.

**Limits on the conclusion:**

Functional resume does not establish security continuity; attestation is not authorization, and a trusted helper expands the protocol's trust boundary until its privileges, protection and code are specified.

The use of SEV is not expanded to SEV-SNP or Intel TDX; processor generations, firmware, migration direction and feature variants are missing.

No detailed threat model, security-equivalence argument, key-release protocol, state-completeness check, failure/rollback/duplicate-resume analysis or independent implementation check is available.

Official description only; cloud deployment and performance claims require paper-level verification.

**Source and location**

Evidence tier: Official DAC description plus author identity source; full manuscript and reproduction not performed. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH2079&sess=sess108)

DAC official description, Captured Description and Authors fields; author publication list confirms identity; no manuscript pages or tables recovered.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** homogeneous CVM migration

vendor-specific migration support

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH2079&sess=sess108

**Hardware or process assumptions:** x86 confidential VMs, vendor TEE firmware, trusted migration agent, and cloud migration path; CPU generations, firmware versions, and attestation details are unspecified.

**Limits:** The description omits downtime, bandwidth, cryptographic cost, failure behavior, and formal security equivalence.

Firmware emulation may expand the trusted computing base and depend on vendor-specific undocumented behavior.

Official description only; cloud security and performance claims require paper-level verification.

**Method or artifact:** Generic heterogeneous-migration framework and trusted migration agent bridging AMD SEV and Hygon CSV command semantics.

**Metrics:** Comparable security guarantees claimed

Acceptable performance overhead claimed qualitatively

AMD SEV-to-Hygon CSV prototype

**Problem:** TEE-vendor-specific CVM implementations support migration mainly within homogeneous stacks, blocking cloud mobility across heterogeneous confidential hardware.

**Workload or benchmark:** Live migration between AMD SEV and Hygon CSV confidential VMs; VM workloads, downtime, bandwidth, threat model, and overhead values are unspecified.

</details>

## What remains to establish

Resolve unspecified workloads, comparison methods, resource budgets, and source locations before generalizing a reported gain. This subject is represented by one paper and supports a case study, not evidence of recurrence or a long-term trend.

[All subthemes](../expanded-taxonomy-v1.md) · [Research directions](../directions/README.md)
