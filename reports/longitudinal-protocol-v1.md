# Longitudinal direction protocol v1

This protocol defines how the project will distinguish a recurring capability,
mechanism persistence, directional prevalence, and comparative impact. It is the
guardrail between the current evidence-backed snapshot and future long-term
claims.

## Unit of analysis

The unit is a paper–mechanism–condition record, not a title, keyword, session,
or conference count. A record is comparable only when its mechanism and the
conditions under which it was evaluated are coded.

The required comparison tuple is:

```text
conference + edition + population + taxonomy path + mechanism + evidence tier
+ workload/design corpus + hardware/process + baseline + metric + budget
+ limits + independent review status
```

## Claim ladder

| Claim level | What it can say | Gate |
|---|---|---|
| Capability | A mechanism is present in a source-backed record | One or more permitted source-backed records |
| Mechanism persistence | A mechanism recurs across editions | Same taxonomy, at least two editions, evidence tiers disclosed |
| Directional prevalence | A mechanism becomes more/less common | Complete denominators, equivalent populations, matched tiers, missingness analysis, independent review |
| Comparative impact | One mechanism performs better | Matched workload, hardware, baseline, metric, budget, extracted conditions, independent review |

Title frequency can route investigation but cannot satisfy the last three levels.

## Missingness and denominators

For every comparison, report five denominators separately:

1. inventory records;
2. records with permitted source text;
3. technically coded records;
4. condition-complete records;
5. independently reviewed records.

Unavailable historical descriptions are not negative evidence. If a claim changes
under plausible assignments of missing records, publish the sensitivity range or
an insufficient-evidence result.

## Direction-specific promotion tests

| Direction | Promotion test |
|---|---|
| Constraints become executable | Held-out design improvement at equal correctness, synthesis, model-call, retry, and wall-clock budgets |
| Data movement as contract | Benefit survives matched workload, quality target, capacity, bandwidth, topology, and migration cost |
| Reliability/security upstream | Useful throughput or correctness remains improved after protection, recovery, and residual-risk costs |
| Physical reality in the loop | Fast physical feedback improves feasible decisions against held-out higher-fidelity simulation or measurement |
| Closed-loop design | Adaptive feedback beats a static baseline at equal sensing, calibration, and evaluation budget |
| Evaluation as research | Independent reruns preserve the result or ranking under versioned evaluator semantics |

The full machine-readable gates, required fields, and current boundary are in
[`data/longitudinal-protocol-v1.json`](../data/longitudinal-protocol-v1.json).

## Current verdict

The current repository supports capability-level and mechanism-level synthesis.
It cannot yet support claims about how common a direction is, or which matters more. Sources differ in depth, many DAC 2025 records are missing, the samples differ, and there are no independent verdicts yet. This is a
result of the protocol, not an invitation to fill gaps with assumptions.
