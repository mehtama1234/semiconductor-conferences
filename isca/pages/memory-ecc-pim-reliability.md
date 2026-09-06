# ISCA 2026 topical analysis: memory, ECC, and PIM reliability

This page synthesizes a selected ISCA 2026 cluster around processing-in-memory,
high-bandwidth memory, and error protection. It is a mechanism map, not a count of
how common each direction is in the full program. The evidence is asymmetric:
Cerberus, COSM, and PuDGhost are supported by author preprints; the ECC-enabled
PIM paper is supported by an institutional publication abstract; HBM-CASO remains
a secondary indexed discovery record pending primary verification.

## The cluster is four different technical problems

| Problem | Mechanism | Detailed subskill | Evidence status |
|---|---|---|---|
| CPU and PIM interfere in shared memory | Idle-window admission and low-interference control | Cooperative scheduling under bank and bus contention | Primary preprint: COSM |
| ECC layers duplicate or interfere | Encode once, decode many, ordered recovery | Cross-layer ECC resource and correction-budget coordination | Primary preprint: Cerberus |
| PuD results depend on unintended data | Column screening and compute-row layout | Physical interference characterization and layout-aware mitigation | Primary preprint: PuDGhost |
| PIM protection can serialize execution | Rank-level ECC, Codeword Flip, bank pipelining | ECC-aware correction scheduling inside bank-PIM | Institutional abstract: ECC-enabled PIM |
| HBM system and on-die ECC are mismatched | Stronger on-die codeword and delayed batch verification | Coordinating processor-visible and memory-internal protection | Secondary index only: HBM-CASO |

These are related because they all reject a clean separation between “memory
hardware” and “system policy.” They should not be collapsed into one claim about
PIM adoption: their objectives differ between throughput, fault containment,
silent-data-corruption risk, correction overhead, and protection-code flexibility.

## 1. Runtime contention: COSM

COSM treats CPU/PIM concurrency as a scheduling problem. PIM is useful only when
its commands do not create enough bank conflict or bus congestion to damage CPU
service. The reported solution combines a low-interference PIM control interface
with an idleness-aware scheduler that inserts PIM work into windows in the CPU
access sequence. Its preprint reports up to 2.8x PIM throughput with less than
2.0% CPU performance loss across concurrent LLM, mobile-application, and compute
kernels.

The subskill is not merely issuing PIM commands. It is estimating and exploiting
slack in a live memory-access schedule while preserving the latency contract of a
general-purpose CPU. Open questions include the exact DRAM/PIM platform, energy
cost, scheduler overhead, and behavior under different CPU traffic distributions.
See [the detailed COSM batch page](primary-evidence-batch-2026-2.md).

## 2. Protection coordination: Cerberus

Cerberus addresses the three-layer protection stack of on-die ECC, link ECC, and
system ECC. Its Encode-Once, Decode-Many organization reuses controller encoding
for link-level detection/retry, device repair, and end-to-end recovery. Decoder
ordering, complementary parity/syndrome structures, and a correction budget are
used to avoid miscorrection amplification.

The subskill is cross-layer recovery orchestration: protection layers are
designed as a coordinated pipeline rather than independent codes whose
redundancy and correction decisions happen to interact. The current preprint
evidence supports the mechanism and fault context, but not a complete quantitative
comparison of area, latency, energy, or every HBM configuration. See [the detailed
Cerberus section](primary-evidence-batch-2026-2.md).

## 3. Physical interference: PuDGhost

PuDGhost tests whether a PuD column really sees only its intended operands. On 96
real DDR4 chips from 12 modules, the study reports output effects of up to 10%
from adjacent non-activated rows and up to 48% from concurrently computing
columns for random inputs. It evaluates robust column screening and row layouts
that insert dedicated rows between compute rows.

The subskill is empirical physical-to-architectural validation. It turns an
abstract reliability assumption into a measurable dependency on neighboring data,
column concurrency, row placement, and chip organization. The result is not a
generic “PIM is unreliable” claim: it identifies concrete interference channels
and candidate mitigations. Transfer to other DRAM generations, voltage/temperature
conditions, and the full cost of screening/layout changes remains unverified. See
[the detailed PuDGhost page](primary-evidence-batch-2026-4.md).

## 4. Correction scheduling: ECC-enabled bank-PIM

The ECC-enabled PIM record describes a reliable bank-PIM design for variable-
retention-time scaling errors and multi-bit faults. It combines rank-level ECC,
Codeword Flip masking for weak cells, and odd-even bank pipelining. The
institutional abstract reports 90% PIM-unit utilization, up to 400x lower
five-year silent-data-corruption likelihood than traditional bank-PIM, and
potential 4x performance over rankPIM in selected microbenchmarks.

The subskill is keeping correction from becoming a serialized afterthought. ECC
work, bank scheduling, and PIM utilization are co-designed. Because the current
source is an institutional abstract, the exact fault model, correction latency,
area/energy overhead, and LLM evaluation must not be inferred from the headline
claims. See [the detailed ECC-enabled PIM page](primary-evidence-batch-2026-5.md).

## 5. Pending question: HBM-CASO

The indexed HBM-CASO summary describes coordination between system-level and
on-die ECC, including a stronger on-die codeword and delayed verification over a
batch of writes. This is a plausible bridge between Cerberus-style cross-layer
protection and concrete HBM implementation constraints, but the project has not
recovered an authorized primary abstract or full paper. It remains in the
[indexed-evidence queue](indexed-evidence-queue.md) and contributes no
adjudicated record or quantitative trend conclusion.

## What this cluster supports—and what it does not

The selected evidence supports a more precise capability map for future hardware
systems:

1. Schedule near-data computation around interference budgets.
2. Coordinate protection codes across memory-stack boundaries.
3. Measure physical interference on real memory devices before trusting idealized
   PIM semantics.
4. Pipeline fault correction so reliability does not erase utilization.

This does not establish that any one ECC scheme, PIM architecture, or HBM mode
will dominate. It also does not establish program-wide prevalence, product
adoption, or a market forecast. Those claims require full-corpus adjudication,
comparable historical editions, and independent adversarial review.
