# Adversarial LLM/human judge protocol v1

This protocol is the required next review layer for the 71 current adjudicated
records. `scripts/audit_adjudications.py` is only a deterministic preflight; its
71/71 pass result must not be described as an adversarial LLM judgment.

## Judge input

Give the judge exactly one record, its cited evidence span/abstract/description,
the relevant taxonomy branch from `reports/taxonomy-coding-guide-v1.md`, and
the source-quality label. Do not provide the cross-conference conclusion first;
that would bias the classification.

## Hostile judge prompt

> Act as an adversarial semiconductor-research reviewer. Treat every field as
> unproven until the cited evidence entails it. For each of problem, method,
> artifact, workload, hardware/process assumptions, baseline, metric, taxonomy
> level, confidence, and limit: return `supported`, `partially_supported`, or
> `unsupported`, with the shortest evidence quote or paraphrase that justifies
> the decision. Identify one plausible neighboring sub-subtheme and explain why
> it should win or lose. Check every number for a named baseline and condition.
> Penalize application-level labels that hide the mechanism. Reject claims of
> superiority, generality, adoption, or trend direction unless the evidence
> directly supports them. End with one of `accept`, `revise`, or `reject` and a
> concrete revision list.

## Required judge output

```json
{
  "paper_id": "...",
  "field_verdicts": {
    "problem": "supported|partially_supported|unsupported",
    "method_or_artifact": "supported|partially_supported|unsupported",
    "workload_or_benchmark": "supported|partially_supported|unsupported",
    "hardware_or_process_assumptions": "supported|partially_supported|unsupported",
    "baselines": "supported|partially_supported|unsupported",
    "metrics": "supported|partially_supported|unsupported",
    "taxonomy": "supported|partially_supported|unsupported",
    "limits": "supported|partially_supported|unsupported"
  },
  "neighboring_taxonomy_candidate": "...",
  "unsupported_claims": ["..."],
  "revision_actions": ["..."],
  "decision": "accept|revise|reject",
  "judge_confidence": "low|medium|high"
}
```

## Acceptance rules

- `accept`: no unsupported technical field, no ungrounded number, and taxonomy
  mechanism is more specific than a generic application label.
- `revise`: evidence is useful but one or more fields need narrowing, a missing
  limit, or a lower confidence label.
- `reject`: the row is mostly title inference, merges distinct papers, or makes
  a claim not entailed by the cited source.

Two independent judges should review records marked `accept` before they feed a
cross-conference conclusion. Disagreements become explicit review artifacts;
they are not averaged away. The protocol also requires a human check for source
license/access conditions and for claims involving security, safety, or
fabrication assumptions.
