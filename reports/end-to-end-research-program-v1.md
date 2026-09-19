# End-to-end research program: from first principles to long-term semiconductor insight

## North-star question

How is the design of computing systems changing as algorithms, models,
architectures, memories, interconnects, compilers, physical implementation,
reliability, security, and manufacturing become one coupled optimization
problem—and which changes are durable enough to matter beyond one paper,
conference, or product cycle?

This project is not a paper-counting exercise. It is a mechanism-first research
program. The unit of analysis is a constrained design decision, supported by a
paper, a page-level explanation, and the conditions under which the decision
works or fails.

## What the finished product must let a reader do

A technically engaged reader should be able to:

1. Start with a first-principles concept such as computation, movement,
   information, uncertainty, physical feasibility, or failure cost.
2. Follow that concept into a field-level theme and then into subthemes and
   concrete mechanisms.
3. Read an explanatory page that says what problem is being solved, what is
   actually changed, why it should work, and what it costs.
4. Open the exact paper record and source passage behind each material claim.
5. Compare how ISCA, DAC, and ICCAD attack related constraints at different
   layers of the stack.
6. Separate a recurring capability from a measured temporal trend, and a
   promising hypothesis from an established result.
7. See what evidence would falsify or strengthen each long-term insight.

The deliverable is therefore a connected research atlas, not a flat literature
list.

## First-principles model of the field

Every paper should be explainable as a transformation of a constrained system.
The common schema is:

```text
workload / objective
        ↓
representation and algorithm
        ↓
mapping and execution
        ↓
data movement and coordination
        ↓
physical realization
        ↓
observed result under limits, uncertainty, and failure modes
```

The core questions are:

| First-principles object | Question to ask of every paper | Typical evidence |
|---|---|---|
| Objective | What is being optimized or protected? | latency, energy, area, yield, accuracy, security, cost |
| Workload | What real or synthetic demand creates the pressure? | model, trace, graph, benchmark, traffic, design suite |
| Representation | What structure is exposed, compressed, predicted, or searched? | tensors, graphs, RTL, layouts, memory regions, faults |
| Mechanism | What new operation changes the feasible design space? | scheduler, compiler, accelerator, surrogate, verifier, ECC |
| Constraint | What cannot be ignored? | bandwidth, capacity, timing, thermal, process, threat model |
| Boundary | Where does the method stop being valid? | scale, precision, drift, baseline, simulator, fabrication |
| Feedback | What observes the result and updates the next decision? | profiling, simulation, formal proof, silicon, retraining |
| Transfer | Does the result survive a new workload, platform, or edition? | held-out tests, cross-platform data, artifact reproduction |

This model is deliberately deeper than an “AI / hardware / EDA” split. It
allows a compiler paper, a chiplet paper, a security paper, and a placement
paper to be compared by the constraint they make executable and the feedback
loop they close.

## Theme architecture

The taxonomy is a navigation system, not the conclusion. Each record should
carry one primary path and any meaningful secondary paths:

```text
first-principles pressure
  → field theme
    → subtheme
      → mechanism / capability
        → paper evidence
          → condition-aware result
            → cross-conference relation
              → long-term insight or unresolved question
```

The current ten-theme map is the working spine:

| Theme | What it explains | Page-backed entry points |
|---|---|---|
| AI-assisted EDA | learned search, generation, and tool-grounded design loops | [DAC AI/EDA and accelerator evidence](../dac/pages/ai-eda-and-accelerator-evidence-batch.md); [ICCAD AI and security evidence](../iccad/pages/ai-and-security-evidence-batch.md) |
| Architecture and accelerators | specialized execution and algorithm–hardware co-design | [DAC topical capability map](../dac/pages/topical-capability-map-2026.md); [ISCA CODO](../isca/pages/codo-dataflow-compiler.md) |
| Memory, interconnect, and storage | movement, locality, capacity, contention, and placement as computation | [DAC data movement and integration](../dac/pages/data-movement-memory-and-integration.md); [ISCA LLM memory and wafer-scale](../isca/pages/llm-memory-and-wafer-scale-v0.md) |
| Chiplets, 3D, and packaging | partitioning, thermal coupling, package boundaries, and integration | [DAC data movement and integration](../dac/pages/data-movement-memory-and-integration.md); [ICCAD topical capability map](../iccad/pages/topical-capability-map-2025-fallback.md) |
| Physical design and manufacturing | timing, placement, process variation, power delivery, and signoff | [ICCAD topical capability map](../iccad/pages/topical-capability-map-2025-fallback.md) |
| Power, reliability, and security | energy, faults, attacks, protection, and recovery as design constraints | [DAC reliability, security, and verification](../dac/pages/reliability-security-and-verification.md); [ISCA memory ECC/PIM reliability](../isca/pages/memory-ecc-pim-reliability.md) |
| Verification and validation | proving, testing, emulating, and measuring correctness | [ICCAD AI and security evidence](../iccad/pages/ai-and-security-evidence-batch.md); [DAC reliability, security, and verification](../dac/pages/reliability-security-and-verification.md) |
| Design methodology and tooling | compilers, synthesis, search, benchmarks, and reproducibility | [ISCA CODO](../isca/pages/codo-dataflow-compiler.md); [DAC AI/EDA and accelerator evidence](../dac/pages/ai-eda-and-accelerator-evidence-batch.md) |
| Systems, applications, and workloads | datacenter, edge, scientific, robotics, and domain-specific pressure | [DAC topical capability map](../dac/pages/topical-capability-map-2026.md); [ISCA primary evidence pages](../isca/pages/primary-evidence-llm-systems.md) |
| Analog, mixed-signal, and emerging devices | non-von-Neumann, analog, photonic, quantum, and emerging-memory tradeoffs | [DAC evidence batch 3](../dac/pages/evidence-batch-3.md); [ICCAD topical capability map](../iccad/pages/topical-capability-map-2025-fallback.md) |

### Required depth inside each theme

Every theme page should answer the same six questions:

1. What system pressure creates this theme?
2. What subthemes represent genuinely different mechanisms?
3. Which papers are representative, contradictory, or boundary cases?
4. What conditions make the reported result meaningful?
5. What does another conference add, remove, or assume differently?
6. What observation would show that the theme is not durable?

Subthemes must remain mechanism-specific. For example, “data movement” is too
wide by itself; its useful subthemes include near-memory execution, tiering,
expert placement, KV-cache management, CXL coordination, and PIM scheduling.
Likewise “AI for EDA” must distinguish search, generation, tool feedback,
formal verification, and benchmark/evaluator design.

## The long-term insight program

The six canonical direction pages now provide the durable navigation layer:
[constraints become executable](directions/01-constraints-become-executable.md),
[data movement as contract](directions/02-data-movement-as-contract.md),
[closed-loop design](directions/03-closed-loop-design.md),
[reliability and security upstream](directions/04-reliability-security-upstream.md),
[physical reality in the loop](directions/05-physical-reality-in-the-loop.md), and
[evaluation as research](directions/06-evaluation-as-research.md). The sections
below preserve the conceptual synthesis; those pages carry the repeatable
evidence-and-falsification template.

The machine-readable [direction atlas](../data/long-term-direction-atlas-v1.json)
and [condition register](../data/direction-condition-register-v1.json) make the
paper-to-direction links and missing workload, hardware/process, baseline,
metric, limit, and locator fields explicit. The condition register is the
active queue for the next evidence-extraction batches.

The [cross-conference direction atlas](../reports/cross-conference-direction-atlas-v1.md)
records whether an ISCA/DAC/ICCAD relationship is complementary layering, a
shared pressure at different layers, a methodological bridge, or a measurement
contract. It keeps venue roles and evidence asymmetry explicit.

The [longitudinal protocol](longitudinal-protocol-v1.md) defines the claim ladder
and promotion gates for future editions. It prevents a capability snapshot from
being silently promoted into a trend or performance conclusion.

The current corpus supports the following durable research hypotheses. They are
not declared trends; each is a claim to pursue through additional pages,
matched evidence, counterexamples, and time-separated coding.

### 1. Constraints are becoming executable

Design constraints that used to appear as late-stage checks—timing, thermal
headroom, memory traffic, fault models, security invariants, or fabrication
rules—are increasingly being placed inside search, mapping, scheduling,
generation, or training loops.

Evidence path: [DAC AI/EDA](../dac/pages/ai-eda-and-accelerator-evidence-batch.md),
[ICCAD AI/security](../iccad/pages/ai-and-security-evidence-batch.md),
[ISCA CODO](../isca/pages/codo-dataflow-compiler.md).

Long-term test: do these feedback loops improve held-out designs and real
execution, or do they optimize proxies and narrow benchmarks?

### 2. Data movement is becoming an algorithmic contract

Placement, locality, migration, topology, contention, and memory capacity are
increasingly treated as part of the algorithm rather than implementation detail.

Evidence path: [DAC data movement](../dac/pages/data-movement-memory-and-integration.md),
[ISCA LLM memory](../isca/pages/llm-memory-and-wafer-scale-v0.md).

Long-term test: do movement-aware methods retain quality and end-to-end benefit
when workload, recall/accuracy target, capacity, and bandwidth are matched?

### 3. The useful unit of innovation is the closed loop

The strongest recurring pattern is not “more AI” or “more hardware,” but a loop
that observes a system, changes a design decision, evaluates the consequence,
and feeds that result back into the next decision.

Evidence path: [DAC topical map](../dac/pages/topical-capability-map-2026.md),
[ICCAD topical map](../iccad/pages/topical-capability-map-2025-fallback.md),
[DAC verification/security](../dac/pages/reliability-security-and-verification.md).

Long-term test: which loops remain stable under distribution shift, tool-version
changes, process variation, faults, attacks, and cost limits?

### 4. Reliability and security are moving upstream

Fault tolerance, side-channel exposure, memory safety, error correction, and
security validation increasingly shape architecture and mapping choices before
implementation rather than appearing only as post-design checks.

Evidence path: [DAC reliability/security](../dac/pages/reliability-security-and-verification.md),
[ISCA memory reliability](../isca/pages/memory-ecc-pim-reliability.md).

Long-term test: are protection mechanisms evaluated against realistic failure
costs and adversaries, or only against local proxy metrics?

### 5. Physical reality is re-entering abstraction layers

Thermal behavior, process variation, package boundaries, power delivery, and
device non-idealities are becoming inputs to system, compiler, architecture,
and search decisions.

Evidence path: [ICCAD topical map](../iccad/pages/topical-capability-map-2025-fallback.md),
[DAC evidence batch 3](../dac/pages/evidence-batch-3.md).

Long-term test: do physics-aware surrogates transfer to signoff and silicon,
and what error budget is acceptable for each design decision?

### 6. Evaluation infrastructure is itself a research frontier

Benchmarks, artifacts, formal gates, trace capture, and reproducibility systems
increasingly determine whether a claimed capability can be trusted or compared.

Evidence path: [DAC AI/EDA](../dac/pages/ai-eda-and-accelerator-evidence-batch.md),
[ICCAD AI/security](../iccad/pages/ai-and-security-evidence-batch.md), and the
project’s [review protocol](adversarial-judge-protocol-v1.md).

Long-term test: can an independent group reproduce the decision boundary,
conditions, and failure cases—not merely the headline score?

## How to pursue the program

### Phase A — Build the conceptual atlas

- Keep the first-principles model and taxonomy stable enough for comparison.
- Create one canonical page per theme, then one page per high-value subtheme.
- Give every page a paper table with evidence tier, mechanism, conditions,
  limits, and cross-conference role.
- Link each synthesis sentence to a page and each page claim to a record or
  source locator.

### Phase B — Deepen representative mechanisms

- Prioritize the 37 synthesis anchors and the records that could falsify them.
- Extract workload/model, hardware/process, baseline, metric, budget, and
  tradeoff conditions from primary papers or artifacts.
- Keep description-only, preprint, company, artifact-only, and full-paper
  evidence visibly separate.
- Produce a bounded mechanism page before making a long-term statement.

### Phase C — Compare across conferences

Use conferences as different observation points in the same system:

- ISCA emphasizes architecture, execution, memory, and systems behavior.
- DAC emphasizes design automation, optimization, verification, and emerging
  design flows.
- ICCAD connects algorithms and tools to physical design, devices, process,
  and implementation constraints.

For every proposed connection, state whether it is a shared mechanism, a shared
pressure, a complementary layer, or merely similar vocabulary.

### Phase D — Establish long-term evidence

- Define matched populations and evidence tiers before comparing editions.
- Track missingness instead of interpreting absent papers as negative evidence.
- Add counterexamples and negative results deliberately.
- Revisit each insight with new editions and record whether it strengthens,
  weakens, splits, or is abandoned.
- Obtain independent review for records supporting accepted synthesis claims.

### Phase E — Publish the living research package

The package should contain:

- a first-principles conceptual primer;
- theme and subtheme pages;
- paper-level evidence pages;
- cross-conference mechanism maps;
- long-term insight and challenge pages;
- temporal comparison reports;
- review and provenance ledgers;
- reproducible build and validation commands;
- an explicit “what we do not know” register.

## Current pursuit queue

The immediate work is not to add more unstructured paper summaries. It is to
turn the strongest existing evidence into linked, condition-aware explanations:

1. Convert the six long-term hypotheses above into canonical direction pages
   with supporting, opposing, and missing evidence sections.
2. Create subtheme pages for tool-grounded design, movement-aware systems,
   reliability/security loops, physical-aware optimization, and evaluation
   infrastructure.
3. Use the [condition register](direction-condition-register-v1.md) to attach
   the 37 synthesis anchors to those pages, then add at least one
   counterexample or boundary case per direction.
4. Finish primary condition extraction for the anchor records.
5. Run independent review and record verdicts separately from deterministic
   validation.
6. Only then make edition-level claims about persistence, acceleration, or
   decline.

The project is successful when it can explain not only what papers appeared,
but what constraints the field is learning to represent, which feedback loops
are becoming central, where the abstractions break, and what evidence would
change the story.
