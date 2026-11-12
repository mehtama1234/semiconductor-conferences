# Reliability and security loops

This article groups several related subjects to explain a shared design question.

## The problem

Systems can fail because of defects, environmental conditions, or attacks. Protection changes cost and may also change useful work or speed.

## What changes in the design

The papers detect, prevent, correct, isolate, or recover from a stated fault or threat.

## How to establish an improvement

The useful test names the fault or threat, measures protection cost and remaining risk, and states what cases are not covered.

## Reliability, security and power all limit useful work

- **Reliability** asks whether a system keeps producing correct results under faults, such as flipped bits or failing parts.
- **Security** asks what an adversary can observe or change.
- **Power** is the rate of energy use. It affects electrical supply and temperature.

They sit together here because protections and operating limits change how much useful work a system can do.

## Every protection costs something, so name the threat first

- **Detecting** a wrong value needs extra information, repeated work, or a check against a constraint.
- **Correcting** it needs enough information to tell the possible errors apart.
- **Isolation** may restrict sharing.
- **Recovery** may stop work and restart it.

So the benefit depends on which error or attack is being considered, and on the cost of the added work.

## The subthemes protect against different things

- **Fault tolerance** keeps or recovers computation after faults.
- **Side-channel** work studies information leaked through timing, power or shared resources, even when direct access is blocked.
- **Privacy-preserving computation** changes how protected inputs are processed.
- **Energy** methods change when or how hardware runs.

Progress in one category does not show protection in another.

## A fair test states the fault or attacker and measures work with protection on

1. State which faults can occur, or which actions an attacker can take.
2. Measure undetected failures, false alarms, recovery time, and performance with protection switched on.
3. Include energy per correct completed job.
4. If faults are injected, say where and how.

Results from that experiment apply to the tested fault model, until broader evidence exists.

## The individual subjects

The grouping contains 37 selected records. Read its individual subjects below; their boundaries can overlap.

- [Fault tolerance and reliability](../observed-subthemes/fault-tolerance-and-reliability.md)
- [Reliability and fault tolerance](../observed-subthemes/reliability-and-fault-tolerance.md)
- [Side channel and hardware security](../observed-subthemes/side-channel-and-hardware-security.md)
- [Power integrity and reliability](../observed-subthemes/power-integrity-and-reliability.md)
- [Hardware security validation](../observed-subthemes/hardware-security-validation.md)

## Technical cards

Evidence tier and exact source locations are provided in each linked article. The article preserves full recorded text, including limits and baselines.

- [PuDGhost: Experimental Analysis of Computation Result Corruption in Processing-using-DRAM Operations on Real DRAM Chips and Implications for Future Systems](../observed-subthemes/reliability-and-fault-tolerance.md#paper-isca-2026-program-024)
- [ECC Enabled Reliable and Performant Processing-in-Memory](../observed-subthemes/reliability-and-fault-tolerance.md#paper-isca-2026-program-009)
- [TT-SEAL: TTD-Aware Selective Encryption for Adversarially-Robust and Low-Latency Edge AI](../observed-subthemes/side-channel-and-hardware-security.md#paper-dac-2026-research848)
- [Securerouter: Encrypted Routing for Efficient Secure Inference](../observed-subthemes/side-channel-and-hardware-security.md#paper-dac-2026-research3092)
- [BREW-RC: Bit-Exact Recovery of ECCs from Write Timing in ReRAM Crossbars](../observed-subthemes/side-channel-and-hardware-security.md#paper-dac-2026-research3042)
- [A Remote Side-Channel Attack on Post-Quantum Key Encapsulation Mechanisms: A Case Study of ML-KEM on Intel x86](../observed-subthemes/side-channel-and-hardware-security.md#paper-dac-2026-research296)
- [SERA-Float: A Soft Error Resilient Approximate Floating-Point Computing Format](../observed-subthemes/fault-tolerance-and-reliability.md#paper-iccad-2025-1109)
- [Energon: Unveiling Transformers from GPU Power and Thermal Side-Channels](../observed-subthemes/side-channel-and-hardware-security.md#paper-iccad-2025-1000)
- [Nothing Left to Learn: Isomorphic Graph Transformations for Hardware IP Protection](../observed-subthemes/side-channel-and-hardware-security.md#paper-dac-2026-research2832)
- [Automated Discovery, Classification, and Systematic Security Verification Methodology for Undocumented Instructions](../observed-subthemes/hardware-security-validation.md#paper-dac-2026-research2804)

## Limits and next evidence

This is a cross-cutting grouping within the selected sample. Its count measures the records included by the grouping rule. Comparing methods requires the same workload, answer quality, hardware limits, and total evaluation budget. Open the individual records before treating a shared subject as a common result.

[Research directions](../directions/README.md) · [Complete subtheme index](../expanded-taxonomy-v1.md)
