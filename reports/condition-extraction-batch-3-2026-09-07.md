# Condition extraction batch 3 — 2026-09-07

This third P1 batch records five additional evidence-bound condition sets. It
combines selected preprint text, institutional abstract evidence, and an
artifact reproduction record; those evidence tiers are kept distinct.

| Paper | Source and locator | Conditions extracted | Boundary retained |
|---|---|---|---|
| DAC-1019 HybriMoE | [assessment](../dac/data/hybrimoe-primary-conditions-v1.json); Sections 5–6 | NVIDIA RTX A6000, Intel Xeon Gold 5220R using 10 CPU cores; Mixtral-8x7B-Instruct, DeepSeek-V2-Lite-Chat, and Qwen2-57B-A14B-Instruct; MT Bench, Vicuna Bench, and ChatGPT Prompts; input lengths about 32–1024 tokens; GPU expert-cache ratios 0.25/0.5/0.75; kTransformers baseline | Average TTFT/decode aggregation weights, batch/concurrency, repeat variance, accuracy parity, and exact commits remain unknown |
| DAC-031 Exact-T | [assessment](../dac/data/exact-t-primary-assessment-v1.json); Sections 4.2–4.3, 6, Table 2, Figures 8–11 | Six EPFL arithmetic circuits; exact-MC mapping comparison; customized mapper reports 5.3% geometric-mean T-count reduction; library-only substitution about 0.5% with regressions; exact solver bound N≤7 total qubits; mapping is at most 11.7% of reported QLUT synthesis runtime | T-count is not hardware speedup; larger instances use suboptimal solutions; source-version discrepancy and proof/correctness conditions remain unresolved |
| DAC-2760 NotSoTiny | [assessment](../dac/data/notsotiny-primary-assessment-v1.json); Sections 2.4, 3, 4.2 | Contextual module completion task; self-equivalence filtering reduces 3,062 deduplicated tasks to 1,114; Yosys `equiv_simple`/`equiv_induct`; k=30; partition coverage is partial credit; Min-K comparison across 11 models with reference-only inputs and >2,000-token modules excluded | Partial partition credit is not full equivalence; contamination threshold, benchmark selection, and table-level outcomes remain unresolved |
| ICCAD-1144 GAIA | [assessment](../iccad/data/gaia-primary-recovery-v1.json); institutional abstract and author-lab cross-check | Trace-driven glass-storage simulation; zigzag placement, depth-first placement, and movement-time scheduling; abstract reports up to 82% read-latency reduction versus traditional schedulers | Trace set, glass size, mechanics, baseline implementations, latency distribution, and author spelling identity remain unresolved; headline is withheld |
| ISCA-060 BusyBarn | [assessment](../isca/data/busybarn-artifact-primary-recovery-v1.json); Zenodo description, README, and bounded runs | Python 3.9 declared artifact environment; quick/full figure scopes; seed 123; 32 GB minimum RAM; quick estimate under three hours on i9-13900K; full run under 12,000 core-hours; four bounded 4×6-mesh synthetic AllGather/AllToAll cases reproduced | Artifact simulation outputs are not paper metrics, end-to-end results, or independent reproduction; exact manuscript baselines and units remain unavailable |

## Next extraction action

The remaining P1 set is now concentrated in records with weaker evidence tiers
or unresolved identity/source recovery. Process those in risk order, keeping
institutional abstracts, company descriptions, and artifacts separate from
manuscript-level evidence.
