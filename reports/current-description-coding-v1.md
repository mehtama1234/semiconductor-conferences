# DAC 2026 description coding expansion — 2026-09-06

The first four previously uncoded records, selected by paper-ID order, have
[technical drafts](../data/current-description-coding-v1.jsonl): research1000
(asymmetric tile buffering), research1011 (SatSFL), research1095 (STEM-CAM) and
research1138 (ARTEMIS). Exact official source URLs and row locators accompany
each record. All are pending independent review and retain description-level
evidence status. They are not added to the 49-record selected adjudication sample.
With four batches, nineteen additional drafts are available;
475 of the 543 current DAC descriptions still need initial technical coding.

## Evidence requiring care

The asymmetric-buffering description gives both a 4.54× maximum speedup and
4.8→24.6 TFLOPS endpoints. Their arithmetic ratio is 5.125×, so a common comparison
configuration is not established. Preserve both claims; obtain the source table
before attributing the discrepancy to rounding, different workloads or a typo.
No claimed performance record is accepted from this description.

The [primary-source assessment](../dac/reports/atb-primary-assessment-v1.md)
found the mismatch also in arXiv v1, distinct matrix sizes in the compared rows,
and two unresolved author-name differences. Headline metrics remain withheld;
arithmetic checks are not substituted as corrected experimental results.

SatSFL describes interpolation and compression for intermittent satellite links,
but names no platform, dataset or numerical result. STEM-CAM supplies a FeFET CAM
encoding mechanism without measured device, energy, throughput or precision data.
ARTEMIS describes learned commercial-SSD stress tests, but no quantitative event
rates or demonstrated correctness bugs. Do not convert qualitative benefits into
invented numbers, deployment claims or validation results.

ARTEMIS's learned-search taxonomy placement remains provisional: generating
stress tests is distinct from optimizing a chip design. Verification/testing is
a secondary relationship. The candidate mechanism labels do not create approved
sub-subtheme IDs.

## Second batch

| Paper | Mechanism | Evidence boundary |
|---|---|---|
| 1152 NoiseXplore | Physics-grounded noise co-simulation and Bayesian in-pixel DTCO | 86.8% accuracy is only the airplane/car/ship subset of CIFAR-10; 50 fps is not independently verified silicon performance |
| 1180 ESCAPE | Programmable probability-driven per-chain LBIST controls | Coverage, peak-power and overhead benefits are qualitative |
| 1183 FLUT area recovery | Predict packing merges and use dynamic mapping costs | At-most-10.3% FLUT count reduction is not silicon area; timing parity needs the full evaluation |
| 1185 CPA-BNN | Encrypted RRAM BNN execution and intrinsic PUF keys | Approximately 100% reliability is not perfect reliability or universal attack prevention |
| 1187 FBS | Prune encrypted CNNs to reduce bootstrapping | ImageNet is motivation, not a confirmed evaluated dataset; negligible accuracy loss is unquantified |
| 1194 DIA-CIM | Co-design asynchronous graph aggregation and sparse BF16 CIM | Description claims fabricated 28-nm CMOS; 60.01 TFLOPS/W lacks operation-counting and measurement boundaries |

## Third batch

| Paper | Mechanism | Evidence boundary |
|---|---|---|
| 1196 GPU LU | Balance dependency levels and adapt resource allocation/indexing | 2.1× versus GLU3.0 and 5.2× versus 16-thread PARDISO are factorization results, not quantified whole-SPICE gains |
| 1200 NIAQ | Kalman drift tracking plus MLP qubit discrimination | 88% versus 61% readout accuracy uses day-equivalent data; 148 mW/5 ns are post-synthesis, not measured silicon |
| 1206 DSPE | Pruning, approximate multiplication and adaptive posit execution | 91.7 TFLOPS/W lacks operation counting, accuracy and power boundaries |
| 121 ExQuant | Globally rank experts and allocate/schedule mixed precision | Reported 2.87–5.93% accuracy gain does not specify relative percent versus percentage points |
| 1222 AttentionCap | Symmetric attention and process embeddings for capacitance learning | Unseen-node transfer uses 5000 samples/4000 fine-tuning steps; 192× inference gain is not whole-chip extraction speed |
| 1233 RM-CIMA | Co-design RL/MPC control and analog CIM | Recovery, latency and energy comparisons have different baselines; hardware-only attribution and physical-flight validation remain unknown |

## Fourth batch

FlashFPS (124) removes sampling redundancy through pruning and inter-layer reuse;
its 5.16× GPU and 2.69× accelerator figures are not established whole-network
speedups. BSGCN (1242) tailors graph bands, traversal and caching to degree/reuse
patterns; its average 1.41× and maximum 4.80× gains remain distinct. DAP (1256)
co-designs distributed SpMM partitioning, CSC communication and dependency buffers;
its 2.69× geometric-mean comparison against A100 is simulation-based at 500 MHz.
The description's ambiguous 0.067× penalty notation is not converted into a
percentage loss or remaining-throughput claim without a definition.

All nineteen records have source-separated review packets. Next: resolve the ATB
numeric comparison from primary evidence and continue uncoded descriptions in
stable order, preserving gaps and possible counterexamples.
