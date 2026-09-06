# DAC 2026 description coding expansion — 2026-09-06

The first four previously uncoded records, selected by paper-ID order, have
[technical drafts](../data/current-description-coding-v1.jsonl): research1000
(asymmetric tile buffering), research1011 (SatSFL), research1095 (STEM-CAM) and
research1138 (ARTEMIS). Exact official source URLs and row locators accompany
each record. All are pending independent review and retain description-level
evidence status. They are not added to the 49-record selected adjudication sample.
With the second six-paper batch below, ten additional drafts are available;
484 of the 543 current DAC descriptions still need initial technical coding.

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

All ten records have source-separated review packets. Next: resolve the ATB
numeric comparison from primary evidence and continue uncoded descriptions in
stable order, preserving gaps and possible counterexamples.
