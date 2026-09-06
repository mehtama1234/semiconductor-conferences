# DAC 2026: reliability, security, and verification as first-class constraints

The adjudicated DAC batch includes papers where correctness, attack resistance, or
fault handling is part of the design objective. These are not one unified theme;
the useful analysis keeps threat models, fault models, and verification goals
distinct.

## Reliability and physical integrity

**Strix** treats NPU reliability across microarchitecture, ISA, and programming
instead of relying only on monolithic replication. It partitions safeguards along
the inference pipeline and reports sub-microsecond fault handling with a 1.04X
slowdown in the public description. The subskills are failure-mode isolation,
cross-layer protection, fault localization, and overhead accounting.

**GEMIR** jointly models IR drop and electromigration stress with graph attention,
physics-informed constraints, and conflict-gated multitask optimization. Its
contribution is the coupling of two physical fields that are often modeled
separately. This is a different reliability problem from Strix: prediction and
physical consistency rather than runtime fault correction.

## Security of optimized systems

**Icarus's Wings** attacks GPU-centric MoE offloading. The attack exploits the
assumptions behind expert caching and prefetching, using a universal hidden prefix
to increase cache replacement and degrade prefetch accuracy. The correct security
reading requires the threat model, attacker cost, affected models/devices, and
defenses—not only the reported slowdown.

## Verification and correctness

**DeepSeq3** uses hierarchical graph representations and state-centric pretraining
for sequential-circuit analysis, reporting an 18% reduction in bounded-model-
checking time while preserving a correctness guarantee in the description.

**AccDRC** is also a correctness-sensitive accelerator: speedup is only useful if
the FPGA checker preserves the semantics of the CPU/GPU rule checks. Its public
description reports very large speedups, but the equivalence conditions and rule
coverage remain fields for primary-paper verification.

## Detailed skill map

| Area | Subskills that must be analyzed separately |
|---|---|
| NPU reliability | failure models, localization, correction, ISA/program support, slowdown |
| Power integrity | EM/IR coupling, physics constraints, prediction error, technology assumptions |
| MoE security | attacker capability, cache/prefetch assumptions, attack transfer, defenses |
| Formal analysis | representation, state abstraction, proof/correctness guarantee, solver cost |
| DRC acceleration | layout partitioning, rule coverage, result equivalence, FPGA resources |

## Limits

The current batch has official-description evidence, not complete paper tables. It
supports detailed technical questions and defensible provisional classification;
it does not justify claims about the frequency or maturity of security and
reliability research across the entire conference.
