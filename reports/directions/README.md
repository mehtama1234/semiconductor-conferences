# Canonical long-term directions

These pages are the durable direction layer of the research atlas. They are
not forecasts and they are not paper-count rankings. Each page turns a
recurring mechanism into a testable research proposition.

The machine-readable registry is [`data/long-term-direction-atlas-v1.json`](../../data/long-term-direction-atlas-v1.json), generated from the existing direction evidence and challenge ledgers by [`scripts/build_direction_atlas.py`](../../scripts/build_direction_atlas.py).

## Reading contract

For each direction, read in this order:

1. first-principles pressure;
2. theme → subtheme → mechanism map;
3. supporting page-backed evidence;
4. counterpressure and boundary conditions;
5. falsifier and next evidence action.

The current evidence is asymmetric: DAC has broad official-description
coverage, ISCA contributes selected systems and architecture evidence, and ICCAD
uses a 2025 fallback with deeper design-method cases. None of these pages should
be read as a prevalence estimate or accepted temporal trend.

| Direction | Canonical page | Core question |
|---|---|---|
| Constraints become executable | [01](01-constraints-become-executable.md) | Can design constraints govern generation and search rather than only check outputs? |
| Data movement becomes an algorithmic contract | [02](02-data-movement-as-contract.md) | Does workload-aware placement survive matched capacity, bandwidth, and quality controls? |
| Closed loops become the unit of innovation | [03](03-closed-loop-design.md) | Which feedback loops remain useful under cost, shift, and failure? |
| Reliability and security move upstream | [04](04-reliability-security-upstream.md) | Can failure and threat models shape design without hiding protection costs? |
| Physical reality re-enters abstraction layers | [05](05-physical-reality-in-the-loop.md) | Do fast physical models improve real feasible decisions, not just simulation speed? |
| Evaluation becomes a research frontier | [06](06-evaluation-as-research.md) | Can benchmarks and artifacts make capability claims independently comparable? |

The source-level synthesis remains in [field directions and hypotheses](../field-directions-and-hypotheses-v1.md), while the machine-readable evidence map is
[`data/technology-direction-evidence-v1.json`](../../data/technology-direction-evidence-v1.json).
