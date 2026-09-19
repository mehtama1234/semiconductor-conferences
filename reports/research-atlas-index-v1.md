# Semiconductor research atlas v1

## What this is

This is the reading and operating entrypoint for the ISCA, DAC, and ICCAD
research project. It connects first principles, themes, paper mechanisms,
source-backed conditions, cross-conference relationships, and longitudinal
research questions.

The project’s central question is:

> How do choices about algorithms, hardware, memory, physical design, and checking
> affect one another—and which proposed improvements still help when the complete
> job, its required answer, and its real operating conditions are measured?

This atlas is a bounded research intelligence product, not a market forecast,
conference ranking, or accepted scientific review. Its uncertainty boundaries
are part of the result.

## Read the connected explanation first

The ten [theme articles](themes/README.md) now contain expanded first-principles discussions. They are connected by one practical question: when a paper removes one cost, what new cost or correctness obligation appears elsewhere? This section explains three recurring relationships. They are interpretations of selected evidence, not measured historical trends or proof that the proposed systems have been integrated.

### 1. A smaller representation changes more than storage

Start with values needed by a computation. A compact encoding can reduce their stored size, but an execution unit must still obtain usable operands. It may need decoding, position information, or a conversion step. If an encoding is approximate, the output-quality requirement changes the comparison too.

This creates a chain of consequences: smaller stored values can free memory; free memory can admit more concurrent work; concurrent work can improve total throughput while increasing each request's wait. A storage saving is therefore not automatically a response-time improvement.

The manuscript-backed [lossless-weight-compression explanation](observed-subthemes/memory-hierarchy-and-persistence.md#explanation-isca-2026-program-008) supplies a concrete counterexample to that shortcut. Its recovered serving table reports higher throughput alongside longer median time per output token, and its conflicting batch counts remain unresolved. The [SPADE explanation](observed-subthemes/sparse-and-irregular-compute.md#explanation-dac-2026-research680) exposes a different boundary: quality-benchmark scores and similarity to a dense-generated video need not improve together. Neither record supports the broad claim that less stored or executed work preserves every desirable outcome.

For a teaching example, suppose a job transfers 100 MB and computes for ten milliseconds. Halving the transferred bytes matters greatly if transfers originally take 50 milliseconds, but little if they take one. If decoding adds five milliseconds, the latter job becomes slower under a sequential model. The bottleneck and the added work determine the result, not compression ratio alone.

Follow this relationship through [architecture](themes/architecture-and-accelerators.md), [memory](themes/memory-interconnect-and-storage.md), [analog representation and conversion](themes/analog-mixed-signal-and-emerging-devices.md), and [systems](themes/systems-applications-and-workloads.md). The long-term hypothesis is that representation and execution increasingly need joint evaluation where movement dominates. It would be weakened by matched results showing that movement is already minor or that decoding and coordination consume the saving.

### 2. Earlier decisions help only when later checks still accept the result

A tool can make design decisions cheaply by using an approximate representation or a learned estimate. It can screen more candidates, reuse a prior calculation, or propose a repair. The selected result must nevertheless satisfy the original behavior and physical requirements.

Consider a timing limit of 100 picoseconds. A prediction of 99.9 appears valid even if the actual arrival is 100.2 and therefore late. The error is numerically small but changes the acceptance decision. Likewise, a local layout edit can remove one spacing violation while introducing another. A useful model must be evaluated where its errors affect decisions, not only by its average numerical error.

The manuscript-backed [timing-reuse explanation](observed-subthemes/compiler-and-runtime-optimization.md#explanation-dac-2026-research2566) preserves the role of electrical context, prediction error, and unresolved differences between the paper's stated checks. The description-backed [Drcagent record](observed-subthemes/llm-assisted-design-flows.md#paper-dac-2026-research2145) motivates repair with design-tool feedback, but does not establish complete physical closure. Their commonality is conditional checking—not equivalent evidence depth, one shared algorithm, or a demonstrated combined workflow.

Follow this relationship through [tooling](themes/design-methodology-and-tooling.md), [AI-assisted EDA](themes/ai-assisted-eda.md), [physical design](themes/physical-design-and-manufacturing.md), and [verification](themes/verification-and-validation.md). A testable hypothesis is that cheaper early decisions reduce total design effort when exact fallback and repair remain affordable. It weakens when optimistic estimates select invalid candidates, reject useful ones, or create enough rework to erase the initial saving.

### 3. Reorganizing resources changes the operating conditions

Adding memory, splitting functions across dies, or reallocating power changes where work executes and what it must communicate. The resulting system may need different placement, scheduling, cooling, or protection rules. The local resource increase is not itself proof of a useful complete system.

The manuscript-backed [Vistara explanation](observed-subthemes/memory-hierarchy-and-persistence.md#explanation-isca-2026-program-045) distinguishes adding capacity from replacing local memory at fixed capacity; a system can benefit from the first while regressing in the second. The [phase-specific DUET explanation](observed-subthemes/chiplet-system-architecture.md#duet-give-different-inference-phases-different-hardware) preserves simulation and synthesis boundaries and an assumption of matched phase throughput. It does not establish a complete multi-request scheduler or manufactured package. [Lit Silicon](observed-subthemes/energy-and-thermal-efficiency.md#lit-silicon-one-gpus-temperature-can-affect-other-gpus-progress) supplies a further connection between synchronization and power allocation, while retaining separate policies and measurement limits.

For an illustrative dependency, two workers taking eight and ten milliseconds finish a shared stage in ten. Slowing the first to nine may leave stage time unchanged; slowing it to twelve makes the stage slower. A local power reduction must be interpreted through the shared completion requirement.

Follow this relationship through [chiplets and packaging](themes/chiplets-3d-and-packaging.md), [memory](themes/memory-interconnect-and-storage.md), [systems](themes/systems-applications-and-workloads.md), and [power, reliability, and security](themes/power-reliability-and-security.md). A hypothesis is that resource allocation needs workload and physical conditions together. Challenge it using phase changes, contention, hot regions, failures, and the total cost of moving or reconfiguring work. These are proposed evaluation conditions, not asserted failures of every linked method.

## What makes these insights durable rather than slogans

Each relationship identifies a mechanism, the conditions under which it could help, and evidence that could contradict it. A new paper can strengthen the relationship, narrow it to a workload, or show that its added costs dominate. Merely finding another title with a similar term does none of those things.

To establish a trend over time, compare equivalent populations across editions: the same paper types, collection rules, technical definitions, and evidence depth. Otherwise an apparent increase can come from more complete source recovery or changed conference scope. Cross-conference complementarity also needs explicit compatibility: a compiler result and a package result do not form a validated system unless their interfaces, workloads, numerical rules, and physical conditions align.

The older [technology direction synthesis](technology-direction-synthesis-v1.md) and [direction dossiers](directions/evidence/README.md) retain historical interpretation and traceability. They still need reconciliation with the newer manuscript-backed corrections. The connected reading above does not silently promote their claims or replace their review gates.

All ten parent discussions are written; the individual subtheme and paper explanations remain uneven. Missing full papers, unresolved source discrepancies, classification decisions, equivalent historical evidence, and independent comprehension/scientific review remain open. Passing software and link checks proves none of those requirements complete.

## The end-to-end evidence path

```text
first principles
  → theme / subtheme
    → mechanism
      → paper and source tier
        → workload / hardware / baseline / metric / limit
          → cross-conference relationship
            → long-term hypothesis
              → longitudinal promotion test
                → independent review
```

## Start here by question

| If you want to understand… | Start with | Then inspect |
|---|---|---|
| The conceptual model | [End-to-end research program](end-to-end-research-program-v1.md) | [Taxonomy and coding guide](taxonomy-coding-guide-v1.md) |
| How a theme becomes a mechanism page | [Theme atlas](themes/README.md) | [Theme-evidence matrix](theme-evidence-matrix-v1.md) |
| How much finer structure exists across the corpus | [Expanded taxonomy atlas](expanded-taxonomy-v1.md) | [Subtheme atlas](subthemes/README.md) |
| How to inspect a high-value subtheme | [Subtheme atlas](subthemes/README.md) | [Theme atlas](themes/README.md) |
| What directions are emerging | [Canonical direction index](directions/README.md) | [Long-term direction atlas](../data/long-term-direction-atlas-v1.json) |
| What exact papers support a direction | [Evidence dossiers](directions/evidence/README.md) | [Direction condition register](direction-condition-register-v1.md) |
| How venues complement one another | [Cross-conference atlas](cross-conference-direction-atlas-v1.md) | [Technology direction synthesis](technology-direction-synthesis-v1.md) |
| How to compare the same pressure across venues | [Comparison dossiers](comparisons/README.md) | [Cross-conference atlas](cross-conference-direction-atlas-v1.md) |
| Whether something is a real trend | [Longitudinal protocol](longitudinal-protocol-v1.md) | [Temporal insufficiency findings](temporal-insufficiency-v1.json) |
| What remains unresolved | [Evidence-gap register](evidence-gap-register-v1.md) | [Research work queue](research-work-queue.md) |
| How claims are challenged | [Adversarial judge protocol](adversarial-judge-protocol-v1.md) | [Independent review handoff](independent-review-handoff-v1.md) |
| Whether a direction can be promoted | [Direction review gate](direction-review-gate-v1.md) | [Longitudinal protocol](longitudinal-protocol-v1.md) |
| What work happens next | [Research agenda](research-agenda-v1.md) | [Direction review gate](direction-review-gate-v1.md) |
| How to audit a long-term claim end to end | [Claim traceability matrix](claim-traceability-v1.md) | [Research agenda](research-agenda-v1.md) |

## First-principles spine

Every paper is interpreted as a constrained transformation:

```text
objective / workload
  → representation and algorithm
    → mapping and execution
      → movement and coordination
        → physical realization
          → result under uncertainty and failure
```

The required questions are:

1. What objective is being optimized or protected?
2. What workload or design corpus creates the pressure?
3. What representation or structure is exposed?
4. What mechanism changes the feasible design space?
5. What hardware, process, threat, or physical assumptions apply?
6. What baseline, metric, and evaluation budget define the result?
7. What feedback updates the next decision?
8. Where does the method stop being valid?

## Canonical directions

The current direction layer is mechanism-first:

- [Constraints become executable](directions/01-constraints-become-executable.md)
- [Data movement becomes an algorithmic contract](directions/02-data-movement-as-contract.md)
- [Closed loops become the unit of innovation](directions/03-closed-loop-design.md)
- [Reliability and security move upstream](directions/04-reliability-security-upstream.md)
- [Physical reality re-enters abstraction layers](directions/05-physical-reality-in-the-loop.md)
- [Evaluation becomes a research frontier](directions/06-evaluation-as-research.md)

Each page has a direct link to its paper-level evidence dossier. The machine
registry preserves source-ledger direction IDs separately from these conceptual
direction IDs so synthesis does not silently collapse distinct taxonomies.

## Current evidence state

The current checkpoint contains 1,589 inventory records and a selected technical
sample of 582 records: 544 DAC, 17 ISCA, and 21 ICCAD. The direction layer is
supported by selected evidence references and condition-aware dossiers, but the
evidence is asymmetric:

- DAC provides broad official-description coverage.
- ISCA provides selected architecture, systems, memory, and artifact-backed
  records.
- ICCAD uses a 2025 fallback with deeper physical-design and methodology cases.

The condition register currently tracks 60 direction-paper references, including
explicit counterpressure records: 38 are condition-complete in the adjudicated
ledgers and 22 remain partial. Independent
review verdicts remain zero. These facts constrain the strength of every
synthesis statement.

A supplementary [source-condition extraction batch](source-condition-extraction-batch-v1.md)
now makes explicit official-description context discoverable for nine DAC
records, including CXL hardware, 28 nm silicon-verified CIM, HLS synthesis,
NPU/SoC, 3D-IC thermal, and MoE GPU settings. These remain description-tier
extractions pending full-paper reconciliation and independent review.

Existing deeper [primary-condition assessments](primary-condition-assessment-register-v1.md)
also surface author-preprint and artifact evidence for five anchors, including
Strix, MappingEvolve, Exact-T, NotSoTiny, and HLSArchOpt. Their unresolved
conditions and pending independent-review states remain attached.

The [direction review gate](direction-review-gate-v1.md) is the explicit stopping
boundary for promotion: all six canonical directions have prepared anchor packets,
but independent verdicts are currently zero, so none is yet eligible for a
longitudinal trend claim.

## What the atlas can currently support

- Capability-level claims about mechanisms present in source-backed records.
- Provisional mechanism-level connections across conferences.
- Explicit research hypotheses with counterpressure and falsifiers.
- A reproducible queue for missing conditions and primary-source recovery.
- A protocol for deciding when future editions support persistence, prevalence,
  or comparative-impact claims.

## What it cannot currently support

- Venue-wide prevalence or market share.
- Industrial adoption or commercial success.
- Rising/declining claims from title shifts or unequal editions.
- Cross-paper speedup arithmetic with unmatched workloads or hardware.
- Independent acceptance of the current selected interpretations.

## Operating loop

1. Route every inventory record and preserve its disposition.
2. Recover permitted primary evidence for high-value mechanisms and countercases.
3. Extract conditions into the [condition register](direction-condition-register-v1.md).
4. Update the relevant evidence dossier and direction page.
5. Compare venue roles through the [cross-conference atlas](cross-conference-direction-atlas-v1.md).
6. Apply the [longitudinal protocol](longitudinal-protocol-v1.md) before any trend claim.
7. Prepare and obtain independent review; preserve objections and resolutions.
8. Rebuild the dated manifest and publish remaining gaps.

The atlas is successful when a reader can move from a conceptual claim to the
exact paper and source conditions, understand what each conference contributes,
see what would falsify the interpretation, and know why the project is or is not
allowed to call the result a long-term trend.
