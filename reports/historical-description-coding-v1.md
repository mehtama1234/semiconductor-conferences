# Historical DAC technical coding — 2026-09-06

Twenty-one DAC 2025 descriptions are coded in
[`historical-description-coding-v1.jsonl`](../data/historical-description-coding-v1.jsonl).
Selection follows paper-ID order among captured substantive descriptions not
already in the temporal pilot. This is a recoverability-biased sample, not a
representative population. Together with the pilot's three historical records,
all 24 captured historical descriptions now have technical drafts;
395 inventory records still lack substantive descriptions. This completes a
description-level coding pass over the accessible snapshot, not historical
full-paper analysis or independent adjudication.

## Mechanisms and evidence limits

| Paper | Contribution | Unsupported inference |
|---|---|---|
| research002: cloud ESSDs | Characterizes two AWS/Alibaba offerings against local-SSD expectations | Four observations and five implications are not enumerated; specific storage advice cannot be extracted |
| research008: ALLMod | Balances hybrid bit-group workloads and result-fusion timing for LUT modular reduction | Up-to-1.65×/3× area-efficiency gains at 128/8192 bits are not end-to-end HE/ZKP speedups |
| research010: G-SpNN | Reformulates passivity enforcement as GPU neural-network training | Average 7.63× convergence speedup versus DAO is not complete circuit-simulation speedup |
| research021: MOSS | Combines RTL LLM embeddings, DFF-aware GNN features and sequential propagation | Reported 95.2% arrival-time accuracy has no supplied metric definition or dataset split; it is not signoff correctness |
| research023: EPICS | Uses SCC-aware loop fusion and lazy event updates for fault simulation | Reported 5.94× speedup with equal coverage lacks named tools, fault model and CPU; it is not safety certification |
| research024: PastATPG | Integrates partial-assignment SAT and structural test compaction | Speed wins in some cases do not imply universal tool superiority; no numeric result is supplied |
| research034: SAPO | Adds mean-variance structure and data-informed eigenvalue settings to HHL | Reported complexity/accuracy improvements use different HHL baselines; neither is demonstrated classical-to-quantum wall-clock advantage |
| research039: SSDL-ILT | Uses self-supervised learning to emit masks and controllable SRAFs | Up-to-12,000× speedup lacks training/amortization boundaries; few-shot adaptation is not zero-shot generalization or fabrication validation |
| research048: ChatLS | Uses multimodal retrieval and prompting to customize synthesis scripts | Qualitative performance lacks PPA, correctness, tool versions and search budget |
| research051: Hydra | Combines expert-popularity mapping, CAM permutation handling and softmax hardware on chiplets | 22 nm evaluation does not establish measured silicon; power reductions are not energy-per-token savings |
| research054: CAE-DFKD | Changes embedding-level data-free distillation to improve transferability | Qualitative learning results do not establish hardware acceleration, privacy guarantees or EDA benefits |
| research068: NeuralMesh | Predicts thermal distributions to guide coarse FEM mesh optimization | Up-to-45× is mesh-generation speedup; within-0.8% accuracy versus COMSOL is not measured-silicon validation |
| research085: EPOC | Combines ZX-calculus, partitioning and synthesis for pulse generation | Circuit-latency reductions of 31.74%/76.80% use different baselines; they are not compiler-runtime reductions |
| research097: EDGE | Uses database techniques for Boolean decomposition | Up-to-21× runtime improvement and at-least-15% node reduction lack named benchmarks; graph nodes are not silicon area |
| research1016: PiSPICE | Uses pre-layout adjoint sensitivity to retain essential parasitics | Maximum 17.27× speedup and less-than-0.78% error versus Spectre lack detailed conditions; introductory scale is not verified test scale |
| research1017: SDM-PEB | Models spatial/depth dependencies with a learned state-space PEB surrogate | Accuracy and efficiency improvements are qualitative; commercial-model comparison is not wafer validation |
| research103: IMR relocation | Uses deduplication reference counts to place stable data on overlapped tracks | Average 37.57% accumulated read/write latency reduction is not tail latency and depends on workload/reference behavior |
| research1034: PairGraph | Reuses frequently traversed structures for concurrent pairwise graph queries | Five baseline-specific speedup ranges cannot be pooled into a mean or assumed resource-normalized |
| research1039: Blaze | Combines value/bit sparsity with approximate orchestration and reconfigurable attention hardware | No numerical result, accuracy-loss bound or named baseline is supplied |
| research1042: LightRIM | Uses hashing and randomized CPU-budgeted integrity measurement | Less-than-0.7% overhead does not establish complete TOCTOU prevention or quantified attack coverage |
| research105: QHD community detection | Alternates multilevel QUBO formulation and quantum-inspired optimization | Up-to-5.49% modularity improvement is not demonstrated quantum hardware advantage or a global-optimum guarantee |

All statements are description-level source reports or coding interpretations.
Exact official URLs, source-ledger row locators, dates, missing conditions and
metric qualifiers accompany each record. Full papers and experiment tables have
not been extracted for this batch. Missing numbers remain empty arrays, not
zeros. Independent review remains pending.

## Taxonomy decisions

ALLMod is hardware arithmetic, not AI-assisted design merely because it uses
design-space exploration. MOSS is learned EDA representation, not an AI execution
accelerator or demonstrated autonomous RTL generator. EPICS and PastATPG share
the testing branch but address fault simulation and test generation respectively.
G-SpNN provisionally uses simulation/emulation/testing: learned macromodeling is
not well represented by existing finer branches. Mechanism labels are candidates,
not approved sub-subtheme IDs.

The second batch adds two further boundary issues. CAE-DFKD has no natural
ML-method branch in the current taxonomy: its domain-workload assignment is
explicitly provisional and should not support hardware/EDA synthesis. SSDL-ILT's
mask generation provisionally uses the learned layout-synthesis branch; neither
assignment silently creates a new approved mechanism ID. SAPO is quantum
algorithm evidence, not an investment recommendation.

LightRIM also needs a finer taxonomy boundary: runtime kernel integrity is not
physical side-channel defense despite its provisional placement in the security
branch. PairGraph handles graph queries, not necessarily GNN inference. EPOC and
the QHD community method are respectively quantum compilation and quantum-inspired
optimization; they should not be counted as equivalent hardware capabilities.

## Next work

Capture labels have been reconciled and [source-separated draft review packets](draft-review-packets-v1.md)
are prepared. Recover full-paper conditions and missing historical sources,
obtain independent review, and adjudicate provisional taxonomy branches. Develop comparable
2026 populations after historical coding; do not force every case into a pair.
These drafts do not increase the separate 72-record selected adjudication ledger
or grant acceptance to synthesis claims.
