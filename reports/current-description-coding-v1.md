# DAC 2026 description coding expansion — 2026-09-06

The first four previously uncoded records, selected by paper-ID order, have
[technical drafts](../data/current-description-coding-v1.jsonl): research1000
(asymmetric tile buffering), research1011 (SatSFL), research1095 (STEM-CAM) and
research1138 (ARTEMIS). Exact official source URLs and row locators accompany
each record. All are pending independent review and retain description-level
evidence status. They are not added to the 49-record selected adjudication sample.
With eleven batches, 61 additional drafts are available;
433 of the 543 current DAC descriptions still need initial technical coding.

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

## Fifth batch

| Paper | Mechanism | Evidence boundary |
|---|---|---|
| 1267 MATCHA | Constraint-programmed memory allocation and heterogeneous schedules | Up-to-35% latency reduction versus MATCH is scoped to MLPerf Tiny and a two-accelerator SoC |
| 1268 Bident | Topology-aware optical loss modeling and combiner optimization | Schematic simulation and model-bound optimality are not fabricated optical validation or universal optimality |
| 127 DyTuner | Adaptive dynamic-shape operator tuning | Up-to-1.41×/1.64× versus BladeDISC/TorchInductor lacks shape distribution and tuning-time boundaries |
| 1275 TRAC | ACT-triggered in-subarray row counting | Qualitative monitoring claims do not establish a complete RowHammer mitigation policy |
| 1282 CPW-SMO | Set-attention common-source/mask generation | Nearly-2× process window and approximately-200× runtime gains omit training/amortization and physical validation |
| 1284 WFH-BFs | Functional weight tiers, core hardening and adaptive pruning | Attack-cost and random-error results are separate; GFLOPs reductions are not measured energy savings |

## Sixth batch

| Paper | Mechanism | Evidence boundary |
|---|---|---|
| 1286 SlideFormer | Sliding GPU window with CPU updates and tiered I/O | Single GPU does not mean GPU-only memory or compute; 1.40–6.27× throughput lacks named baseline conditions |
| 1287 MDP-ILT | Differentiable shot-level EBL/optical co-optimization | Exact model gradients are not physical accuracy or global optimality; results are qualitative |
| 1290 Hybrid net/pin weighting | Analytical TNS/WNS placement objectives | Average 39%/6% gains omit signed-slack normalization and do not establish routed timing closure |
| 1291 NASiC | CAM-selected 3D NAND multibit CIM | Result sentence calls the architecture V-ASIC; naming conflict and all numerical conditions remain unresolved |
| 1292 IMPart | Integrate memetic operations into uncoarsening | Broad superiority is qualitative; seeds, balance constraints and budgets are missing |
| 1298 FreqSEM | Frequency-guided SAM2 contour extraction | 0.334 nm mean/0.661 nm standard deviation are not maximum-error guarantees; 81 nm linewidth is not a process node |

## Seventh batch

| Paper | Mechanism | Evidence boundary |
|---|---|---|
| 130 C2C-Explorer | Prototype-calibrated interconnect simulation and Bayesian DSE | Simulator capacity, FPGA validation and 32-XPU workload study differ; 98.4% memory reduction has an unspecified memory category |
| 1300 ComPart | Community-guided post-coarsening partition search | Solution quality claims omit objective, balance constraints and budgets |
| 1302 AILFM | Oracle-imitation thermal/kernel-aware scheduling | Near-optimality, thermal safety and generalization are qualitative |
| 1307 MASQ | Mask/stage-aware precision and diffusion acceleration | A100 and Orin NX gains retain separate baselines; quality and hardware-resource parity are unspecified |
| 1308 SDM | FeFET sigmoid computation for soft decisions | 93.2% MNIST accuracy under 40 mV variation is not universal variation tolerance or demonstrated silicon robustness |
| 1312 QAgent | Per-qubit multi-agent RL placement | Up-to-53.9% cost reduction lacks cost definition and training budget; not demonstrated fault-tolerant hardware |

## Eighth batch

| Paper | Mechanism | Evidence boundary |
|---|---|---|
| 1316 Zoned neutral-atom compiler | Iterative Diving Search and relaxed routing | Thousand-qubit compilation is not physical execution; 28.1% rearrangement gain is not total circuit-runtime gain |
| 1317 HyPAS | Discrete repair and differentiable placement/sizing | PPA, runtime and timing-closure claims lack numerical benchmark conditions |
| 1320 Falcon fault study | Physical implementation-fault analysis | One-bit fault and 250,000 faulty signatures are distinct requirements; 800× is signature-count reduction, not attack-time reduction |
| 1322 Keeping PIM Busy | Channel-local generation, DMA and multi-batch co-design | Emulation results and component factors have unclear denominators; do not compose them arithmetically |
| 1331 Marlin | Head-sensitive prefix KV retrieval and overlap | TTFT/accuracy benefits are qualitative; this is not the similarly named quantization kernel |
| 1334 PEL | Palette enhancement with tri-core FPGA processing | 18.13% BD-rate benefit is content/configuration-specific; eight-line latency is not complete codec latency |

## Ninth batch

| Paper | Mechanism | Evidence boundary |
|---|---|---|
| 1338 ZK-Tracer | Heterogeneous zkVM frontend tracing | 1829× frontend and 963× system gains have unnamed baselines and unresolved system boundaries |
| 1348 TOB-Sched | Topological-order-balanced emulator scheduling | Scheduling runtime, TOB score and emulated time steps are separate metrics |
| 1351 eLLM | Elastic shared activation/KV memory | Up-to-2.32× throughput lacks SLO/concurrency and host-memory conditions |
| 1355 BluesFL | Instruction-oriented block slicing for LLM fault localization | 24 versus 7 localized bugs is not an accuracy percentage; historical per-bug cost is not current API pricing |
| 1357 3D-DuRA | Dual-ring sparse attention on hybrid 3D memory compute | Infinity2B/VAR-d36 gains are model-specific; quality, area and technology parity remain unknown |
| 1365 AiMX graph compiler | DMA layout conversion and graph/operator fusion | Reported 2.00–2.73× prefill and 18.50–38.29× decode gains require baseline/work-scope reconciliation; removing only profiled overhead cannot explain them |

## Tenth batch

| Paper | Mechanism | Evidence boundary |
|---|---|---|
| 1373 SLCross | Cross-component M2 shared-cache confidentiality analysis | No leakage-rate/accuracy figures or access assumptions supplied; no attack executed here |
| 1374 SpArC | Sparse-metaoperation FPGA compilation | Numerical comparisons are SuiteSparse SpMSpV, not every supported sparse operation |
| 1378 RISC-V invariant verification | Modular proofs with counter/handshake invariants | Reported 174% speedup has ambiguous convention; proof scope and specification-update claim need source verification |
| 138 PFGEMM | Prefix-index compression and out-of-order sparse execution | Traffic and speed gains omit named baselines, precision and resources |
| 1382 AI+SAR | Pseudo-transposition and FFT-aware graph splitting | 3.45× applies to SAR imaging, not the complete AI+SAR application |
| 1388 Parallel CEC | Sharing-aware factored-form partitioning | 40-core versus single-thread gains are not resource-matched; geometric means and maxima remain separate |

## Eleventh batch

| Paper | Mechanism | Evidence boundary |
|---|---|---|
| 1390 ATLAS | Decoupled GNN FIT ranking and calibration | Predicted reliability and selective-hardening results do not establish safety certification |
| 1400 ActionFlow | Cross-request VLA prefill/decode pipeline | OpenVLA-7B frame-rate gain does not establish closed-loop latency or stability |
| 1404 LS-Placer | Learned net/logic delays and slack-adaptive FPGA placement | Reported averages compare with Vivado 2021.2; benchmark identities are missing |
| 1407 COmPOSER | Physics/learned-EM-assisted RF synthesis and layout | Post-layout 65-nm results are not fabricated-chip measurements; productivity accounting is unspecified |
| 1409 CODA | Tensor-independent NPU dataflow search | Single-operator and fused-operator gains remain separate; not the ISCA CODO paper |
| 1412 VRRAM | Gshuffle low-bit ViT and reconfigurable 3D lookup compute | Mixed weight precision is not uniform four-bit quantization; accuracy and efficiency baselines differ |

All 61 records have source-separated review packets. Next: resolve the ATB
numeric comparison from primary evidence and continue uncoded descriptions in
stable order, preserving gaps and possible counterexamples.
