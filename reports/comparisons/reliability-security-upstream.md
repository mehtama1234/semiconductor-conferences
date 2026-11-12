# Reliability Security Upstream: cross-conference comparison

This dossier asks what the three venues contribute to the same conceptual pressure. It is a layer comparison, not a ranking, prevalence estimate, or temporal trend claim.

**Relation type:** `cross_layer_contract`  
**Current gate:** `blocked_pending_independent_review_and_condition_reconciliation`

## Comparative proposition

The venues converge on explicit operating envelopes, but fault, thermal, and threat models cannot be collapsed into one robustness score.

## Venue roles

| Venue | Current role | Evidence references |
|---|---|---:|
| ISCA | Architecture and memory cases expose correction, interference, and thermal behavior during execution. | 3 |
| DAC | Accelerator and design-flow cases expose fault mitigation, physical integrity, attacks, and protection overhead. | 3 |
| ICCAD | Security and fallback design cases expose threat-model and validation boundaries, with broader physical-reliability scope. | 1 |

## Paper-level comparison set

These are the source-backed references currently attached to the direction. Different source tiers and condition completeness are preserved rather than normalized away. Dated corrections use current source links, but do not inherit a historical complete-condition label. The direction promotion gate above is historical and is not newly satisfied by a correction.

### ISCA

| Paper | Edition | Evidence tier | Conditions | Source |
|---|---:|---|---|---|
| `isca-2026-program-004` — Cerberus: Cross-Layer ECC Co-Design for Robust and Efficient Memory Protection | 2026 | `Author preprint v1; selected method and evaluation sections inspected` | `correction_pending_condition_review` | [source](https://arxiv.org/pdf/2605.02220v1) |
| `isca-2026-program-009` — ECC Enabled Reliable and Performant Processing-in-Memory | 2026 | `institutional_abstract` | `complete` | [source](https://cris.technion.ac.il/en/publications/ecc-enabled-reliable-and-performant-processing-in-memory/) |
| `isca-2026-program-024` — PuDGhost: Experimental Analysis of Computation Result Corruption in Processing-using-DRAM Operations on Real DRAM Chips and Implications for Future Systems | 2026 | `primary_or_author_copy` | `complete` | [source](https://arxiv.org/abs/2606.19119) |

- [isca-2026-program-004: current correction and original evidence](../observed-subthemes/memory-hierarchy-and-persistence.md#paper-isca-2026-program-004) — corrected 2026-09-07; historical condition status `complete` is not carried forward as approval.

### DAC

| Paper | Edition | Evidence tier | Conditions | Source |
|---|---:|---|---|---|
| `dac-2026-research043` — Strix: Re-Thinking NPU Reliability from a System Perspective | 2026 | `Primary arXiv v1 preprint plus page-level assessment and table check; no independent execution, silicon validation or safety acceptance` | `correction_pending_condition_review` | [source](https://arxiv.org/html/2604.10484v1) |
| `dac-2026-research046` — GEMIR: Graph-Based Joint Modeling of Electromigration and IR Drop for Power Grid | 2026 | `Primary captured official DAC description plus bounded recovery assessment and existing authored power-integrity discussion; full paper not recovered, numerical claims withheld pending conditions, no reproduced physics validation or fabricated-chip result` | `correction_pending_condition_review` | [source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH046) |
| `dac-2026-research1054` — Icarus's Wings: Disabling MoE Offloading Acceleration via a Universal Hidden Prefix Attack | 2026 | `Primary captured official DAC description plus pinned repository artifact-discovery assessment; no recovered full paper, executable attack, reproduced offloading system or independent validation` | `correction_pending_condition_review` | [source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH1054&sess=sess156) |
| `dac-2026-research1494` — When Cloud TEEs Encounter Availability: A Lightweight Framework for Verifiable CPU Availability | 2026 | `Primary captured official DAC description plus existing chapter-level cloud-TEE availability discussion; no full-paper extraction, reproduced scheduler, fairness evaluation or deployed-CPU validation` | `correction_pending_condition_review` | [source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH1494&sess=sess122) |

- [dac-2026-research043: current correction and original evidence](../observed-subthemes/accelerator-reliability.md#paper-dac-2026-research043) — corrected 2026-09-08; historical condition status `partial` is not carried forward as approval.
- [dac-2026-research046: current correction and original evidence](../observed-subthemes/power-integrity-and-reliability.md#paper-dac-2026-research046) — corrected 2026-09-09; historical condition status `partial` is not carried forward as approval.
- [dac-2026-research1054: current correction and original evidence](../observed-subthemes/side-channel-and-hardware-security.md#paper-dac-2026-research1054) — corrected 2026-09-08; historical condition status `partial` is not carried forward as approval.
- [dac-2026-research1494: current correction and original evidence](../observed-subthemes/side-channel-and-hardware-security.md#paper-dac-2026-research1494) — corrected 2026-09-08; historical condition status `complete` is not carried forward as approval.

### ICCAD

| Paper | Edition | Evidence tier | Conditions | Source |
|---|---:|---|---|---|
| `iccad-2025-1000` — "Energon": Unveiling Transformers from GPU Power and Thermal Side-Channels | 2025 | `Primary arXiv preprint v1 and official ICCAD record; selected manuscript reading, execution and independent acceptance not performed` | `correction_pending_condition_review` | [source](https://arxiv.org/pdf/2508.01768v1) |

- [iccad-2025-1000: current correction and original evidence](../observed-subthemes/side-channel-and-hardware-security.md#paper-iccad-2025-1000) — corrected 2026-09-08; historical condition status `partial` is not carried forward as approval.

## What is actually comparable

The comparison should be made at the mechanism and constraint level first. A fair comparison holds six things fixed: the workload or design set, the hardware or simulator assumptions, the baseline, the metric, the test budget, and what counts as a failure.

### Required matched fields

| Field | Why it matters |
|---|---|
| Workload / design population | Determines whether the mechanism addresses the same pressure. |
| Hardware / process / tool version | Separates a mechanism from a platform advantage. |
| Baseline and budget | Prevents unequal search, retries, tuning, or evaluator effort. |
| Metric and end-to-end boundary | Prevents proxy improvement from being reported as system benefit. |
| Failure model and limits | Defines what counts as valid, safe, feasible, or transferable. |

## Next matched comparison

Match threat/fault model, coverage, false negatives, recovery cost, useful throughput, and availability impact.

## Current conclusion boundary

The evidence supports a provisional cross-conference mechanism relation. It does not establish that the direction is increasing, dominant, superior, or independently validated. The [direction review gate](../direction-review-gate-v1.md) records the remaining promotion work.
