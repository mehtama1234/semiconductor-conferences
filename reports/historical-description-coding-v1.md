# Historical DAC technical coding — 2026-09-06

Six additional DAC 2025 descriptions are coded in
[`historical-description-coding-v1.jsonl`](../data/historical-description-coding-v1.jsonl).
Selection follows paper-ID order among captured substantive descriptions not
already in the temporal pilot. This is a recoverability-biased sample, not a
representative population. Together with the pilot's three historical records,
nine of the 24 captured historical descriptions now have technical drafts;
15 remain uncoded and 395 inventory records lack substantive descriptions.

## Mechanisms and evidence limits

| Paper | Contribution | Unsupported inference |
|---|---|---|
| research002: cloud ESSDs | Characterizes two AWS/Alibaba offerings against local-SSD expectations | Four observations and five implications are not enumerated; specific storage advice cannot be extracted |
| research008: ALLMod | Balances hybrid bit-group workloads and result-fusion timing for LUT modular reduction | Up-to-1.65×/3× area-efficiency gains at 128/8192 bits are not end-to-end HE/ZKP speedups |
| research010: G-SpNN | Reformulates passivity enforcement as GPU neural-network training | Average 7.63× convergence speedup versus DAO is not complete circuit-simulation speedup |
| research021: MOSS | Combines RTL LLM embeddings, DFF-aware GNN features and sequential propagation | Reported 95.2% arrival-time accuracy has no supplied metric definition or dataset split; it is not signoff correctness |
| research023: EPICS | Uses SCC-aware loop fusion and lazy event updates for fault simulation | Reported 5.94× speedup with equal coverage lacks named tools, fault model and CPU; it is not safety certification |
| research024: PastATPG | Integrates partial-assignment SAT and structural test compaction | Speed wins in some cases do not imply universal tool superiority; no numeric result is supplied |

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

## Next work

Code the remaining 15 captured historical descriptions in the same stable order.
Recover full-paper conditions and missing historical sources. Develop comparable
2026 populations after historical coding; do not force every case into a pair.
These drafts do not increase the separate 72-record selected adjudication ledger
or grant acceptance to synthesis claims.
