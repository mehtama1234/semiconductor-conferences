# DAC 2025–2026 mechanism comparison — selected descriptions

This is the first technically coded historical comparison. It uses six official
descriptions, grouped into three purposeful pairs. The coding ledger is
[`temporal-comparative-coding-v1.jsonl`](../data/temporal-comparative-coding-v1.jsonl).
These records are comparative coding drafts, separate from the 72-record
adjudication sample, and await independent review. Mechanism labels for new
historical cases are descriptive candidates, not silently added taxonomy IDs.

## Selection and comparability

The historical accessible set contains 24 substantive descriptions from 419 DAC
2025 inventory records; 395 descriptions remain missing. DAC 2026 has 543
substantive descriptions. This pilot selected three 2025 cases with clear
mechanisms and related 2026 cases. It controls source tier (official description)
and broad technical question, but not workload, hardware, baseline, or evaluation
protocol. It is a retrospective exploratory sample, not a preregistered study.

| Question | 2025 case | 2026 case | Supported comparison | Not established |
|---|---|---|---|---|
| How is vector-search movement reduced? | UPVSS: operation placement on UPMEM | CANNON: pipelined full offload to CXL NMP | Both make memory-system capabilities part of search execution; mechanisms and platforms differ | CXL replacing UPMEM, superior accuracy/latency, or increasing NMP prevalence |
| How is speculative decoding coordinated? | AASD: multimodal KV projection and target/draft alignment | AHASD: asynchronous NPU/PIM execution with adaptive drafting controls | Draft usefulness and execution coordination are distinct parts of speculative inference | A chronological replacement, like-for-like speedup, or a common energy benefit |
| What assumptions support MoE offloading? | HybriMoE: scheduling, prefetching, and caching | Icarus: adversarial disruption of locality/prefetch assumptions | Performance techniques and threats can concern the same system assumptions | An attack on HybriMoE specifically, widespread exploitability, or worsening security over time |

## How to interpret reported numbers

AASD's up-to-2× figure and AHASD's GPU/PIM comparisons use different workloads and
platforms. Subtracting or dividing those figures would not measure year-over-year
progress. UPVSS's captured description has no numerical result; missing data is
not zero improvement. HybriMoE's prefill/decode improvements and Icarus's decoding
degradation answer different experimental questions and cannot form a performance
ranking. The ledger preserves named baselines, missing assumptions, and conditional
metrics for subsequent full-paper extraction.

## Temporal conclusion

The sample establishes related technical mechanisms in both editions and exposes
concrete differences worth investigating. It does not establish that any topic
is rising or declining. A historical absence cannot be inferred from the 395
uncaptured descriptions. No independent review has been performed on this pilot.

After the [historical coding batches](historical-description-coding-v1.md),
all 24 accessible historical descriptions have drafts. Next, recover missing
historical sources, and select comparison populations using documented rules.
For each intended temporal claim, align taxonomy, evidence tier, paper types,
workloads and evaluation conditions where relevant; report exclusion counts and
test sensitivity to missingness. If that cannot be achieved, retain an explicit
insufficient-evidence conclusion rather than extrapolating from these pairs.

## Source links

- [AASD, DAC 2025](https://62dac.conference-program.com/?post_type=page&p=15&id=RESEARCH005&sess=sess104)
- [HybriMoE, DAC 2025](https://62dac.conference-program.com/?post_type=page&p=15&id=RESEARCH1019&sess=sess113)
- [UPVSS, DAC 2025](https://62dac.conference-program.com/?post_type=page&p=15&id=RESEARCH1048&sess=sess163)
- [AHASD, DAC 2026](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH384)
- [Icarus, DAC 2026](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH1054)
- [CANNON, DAC 2026](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH108)
