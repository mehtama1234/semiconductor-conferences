# DAC 2026 description coding expansion — 2026-09-06

The first four previously uncoded records, selected by paper-ID order, have
[technical drafts](../data/current-description-coding-v1.jsonl): research1000
(asymmetric tile buffering), research1011 (SatSFL), research1095 (STEM-CAM) and
research1138 (ARTEMIS). Exact official source URLs and row locators accompany
each record. All are pending independent review and retain description-level
evidence status. They are not added to the 49-record selected adjudication sample.
With twenty-five batches, 145 additional drafts are available;
349 of the 543 current DAC descriptions still need initial technical coding.
Draft coverage does not mean complete technical evidence. Research1691's extraction
has been repaired, but its energy/power boundary remains unresolved.

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

## Twelfth batch

| Paper | Mechanism | Evidence boundary |
|---|---|---|
| 1414 EXPCheck | Age-budgeted expert checkpoint selection | Up-to-5× frequency is not training speedup; recovery consistency and failure model remain unknown |
| 1417 Simultaneous DNN fault injection | Interaction mitigation and input pruning | Best 0% versus mean 0.2% false negatives; software and RTL speedups are distinct |
| 1419 Duet | Distribution-aware pruning and bit-serial execution | Effective bits are not uniform precision; lossless high-order pruning does not imply globally lossless compression |
| 142 PRO-V-R1 | Tool-feedback-trained RTL verification agent | Functional correctness and robust fault detection are separate empirical metrics, not formal guarantees |
| 1420 IGNITE | Context-conditioned neural circuit simulation | No online training does not mean no context-generation or pretraining cost; R2 is not worst-case error |
| 1430 Spike-PTSD | SNN adversarial robustness evaluation | Success rate lacks perturbation/knowledge conditions; no attack executed or clinical claim accepted |

## Thirteenth batch

| Paper | Mechanism | Evidence boundary |
|---|---|---|
| 1431 G-Power | Cross-GPU transfer and aggregated power-model knowledge | Prediction MAPE/correlation are not power savings; 22% improvement convention is unspecified |
| 1434 G-Matcher | GPU multi-stage/multi-level layout pattern matching | Industrial Calibre and public CPU comparisons differ; perfect matching is limited to evaluated data |
| 1438 PiHG | Pivot-centric HGNN feature/computation reuse | Software and hardware speed/energy ranges remain distinct; platform parity is unknown |
| 144 Syndrome extraction | Quasi-abelian-code CNOT scheduling and pipelining | Claimed depth bound is not wall-clock latency or a measured logical error rate |
| 1440 TACo | Hypervolume-guided zero-cost ViT search | GPU-days to GPU-hours lacks exact budgets; no numeric speedup inferred |
| 1441 Adaptive KV prefetch | Token-fluctuation prediction and decoupled transfers | 256 tokens need not be all retained state; decoding speedup is not whole-request latency |

## Fourteenth batch

| Paper | Mechanism | Evidence boundary |
|---|---|---|
| 1444 Janus | PA/BTI compiler defense with modifier fusion | Overhead figures do not verify threat coverage or strong security guarantees |
| 1447 STCG | Adaptive WMMA/FMA sparse-tensor code generation | SpMM geometric mean and SpTTM reported gain have distinct comparator/aggregation conditions |
| 1449 Maple | Transfer-aware xPU/NDP mapping search | Performance and energy maxima need not co-occur; measurement scope is unspecified |
| 146 FreeBit | Low-bit LUT/PIM and decoupled scheduling | Introductory 6.7× compute reduction is not FreeBit speedup; no numeric result inferred |
| 1464 Thrend | Counter sampling and counting-thread co-scheduling | Zero evaluated false negatives is not universal detection; sampling is 100 Hz |
| 1466 InferWeave | Bandwidth-planned unified-memory inference | Throughput is not request latency; MT-3000 must not be confused with MTIA 300 |

## Fifteenth batch

| Paper | Mechanism | Evidence boundary |
|---|---|---|
| 1468 AdaHuff-GNN | Loss-triggered adaptive entropy coding | Epoch time is not time-to-convergence; codec and codebook accounting is unspecified |
| 1473 GRACE | Graph/ILP-guided PCB rerouting and copper unification | Geometric continuity is not measured signal integrity; optimality is formulation-dependent |
| 1474 Compilation Tells Energy | Compiler-IR multi-task power prediction | No numeric prediction error or energy savings supplied |
| 1480 ADAPT | Token pruning and hierarchical-sparse spiking execution | Prosperity/GPU comparisons remain distinct; pruning does not remove model training |
| 149 TRIDENT | Fused triple sparse multiplication | Accelerator average and CPU/GPU maxima differ; kernel gains are not application gains |
| 1494 AvaTEE | Attested commitments and trusted CPU arbitration | 19.7× slowdown describes the vulnerable baseline, not an AvaTEE gain; evaluation is FPGA-based |

## Sixteenth batch

| Paper | Mechanism | Evidence boundary |
|---|---|---|
| 1495 PMU-Faker | PMU event timing-risk characterization | 118 events and four demonstrations are not prevalence or success rates; no attack executed |
| 1497 Hardware interrupts | Interrupt observability and security characterization | Six vulnerable interrupts lack platform/permission coverage; demonstration count is not general exploitability |
| 1499 KCD-CAM | Charge-domain CAM range search and voxel hashing | KNN gains are not full perception gains; accuracy and peripheral accounting are unknown |
| 150 RISCSmith | Typed instruction generation and online differential fuzzing | Bug counts do not establish severity or correctness coverage; budgets and confirmations are missing |
| 1519 AgenticDSE | Agent-guided multi-phase chiplet BO | Equal exploration counts do not ensure equal compute; token reductions are not financial savings |
| 1524 GPU DAG scheduling | Kernel parallelism control and timing analysis | Worst-case bound and measured-runtime reductions remain separate; safety assumptions need full text |

## Seventeenth batch

| Paper | Mechanism | Evidence boundary |
|---|---|---|
| 1534 DRΛMA | Hybrid-grid detailed routing and adaptive search | Nine of ten designs are violation-free, not the entire benchmark |
| 155 AccelCIM | SRAM CIM macro/array dataflow exploration | Cycle-accurate and post-layout analysis are not fabricated-chip measurements; no numeric result supplied |
| 1552 Beyond Exact | Divergence-aware GPU block WCET analysis | Lower timing estimates are not faster execution; exactness depends on constraints |
| 1560 LOHA | CPU traversal and speculative in-storage re-ranking | Numeric results are throughput, not latency; recall and concurrency are unknown |
| 1562 PG-GNN | Physics-guided residual/active timing characterization | Mean errors do not bound worst corners or independently establish signoff readiness |
| 1569 FILCO | Reconfigurable accelerator composition and DSE | Joint throughput/efficiency range cannot be split into two established per-metric ranges |

## Eighteenth batch

| Paper | Mechanism | Evidence boundary |
|---|---|---|
| 1570 NVLLM | NAND-centric FFN execution and ECC-aware pipelines | External DRAM remains; CMOS overhead is not total-system area overhead |
| 158 FP-DDM | Overlap-consistent neural domain decomposition | Ten-billion-cell scale lacks runtime/resources; solver-level accuracy is unquantified |
| 1582 SliceMoE | Bit-sliced expert caching and prefill warmup | Model-specific decode gains omit warmup cost and exact high-bit accuracy differences |
| 1585 DFA-DRIVE | Thermal-delay-fault analysis and systolic remapping | Automotive temperature targets are not certification; cycle reduction is not vehicle safety proof |
| 1587 CelestialEye | CPU decoding and FPGA stream-item processing | Qualitative BitMatcher comparison; no numeric speed/accuracy result |
| 1596 PIMGRAG | Near-memory retrieval and PIM/GPU scheduling | Qualitative efficiency claims; no demonstrated factuality or whole-generation gain |

## Nineteenth batch

| Paper | Mechanism | Evidence boundary |
|---|---|---|
| 160 ROSA | Optical shift-and-add and noise-aware hybrid mapping | EDP reductions have different references and must not be compounded |
| 1605 MANTIS | Microscaled SRAM-compatible charge-domain macro | TOPS/W depends on precision; 0.15 percentage-point loss is versus a quantized baseline |
| 1608 Remote CZ compiler | Directional excitation transport with AOD assistance | Entangling-stage reduction is not total circuit speedup; fidelity and setup cost unknown |
| 1610 BayesCVNN | Complex-valued uncertainty search and FPGA generation | Less than 10% GPU power is not a 10% reduction; model-specific speedups remain separate |
| 1612 EARL | Entropy-gated RTL policy updates | Up-to-14.7% pass-rate gain has unspecified percentage convention and sampling budget |
| 1613 STRAP-ViT | Anomalous-token detection and randomized transformations | Patch coverage is a chosen target, not measured detection; adaptive attack conditions unknown |

## Twentieth batch

| Paper | Mechanism | Evidence boundary |
|---|---|---|
| 1619 HDDB | HDC-encoded FeNAND SQL operations | Random TLC-cell corruption is not arbitrary fault tolerance; operation gains are not full-database gains |
| 1622 N3Litho | GPU numerical/neural 3D field reconstruction | Fidelity and speedup are qualitative; downstream full-flow validation not demonstrated |
| 1628 Attackonctf | Semantics-preserving benchmark obfuscation | Reduced detection does not alone prove benchmark validity; percentage conventions unspecified |
| 1629 AQR-HNSW | Density-aware quantization and staged re-ranking | SIMD rate, QPS and build time differ; storage reductions must not be compounded |
| 163 PFATS | Per-flow asynchronous TSN queuing | Jitter bound depends on traffic/system assumptions; interconnect subtheme fit remains provisional |
| 1632 ECPrefix | Erasure-coded prefix-KV distribution | TTFT is not decoding or total response time; reconstruction/network costs unknown |

## Twenty-first batch

| Paper | Mechanism | Evidence boundary |
|---|---|---|
| 1638 Boundary recovery | SAT-sweeping hierarchical reconstruction | Algorithm attribution is title-level; no quantitative recovery/runtime evidence |
| 1640 UniSpike | Destination-aggregated spike packets | Initial redundant traffic share differs from achieved gains; timing/accuracy costs unknown |
| 1646 Learned-prior yield analysis | In-context cross-corner regression | Best mean error is not rare-tail yield validation; zero tuning omits pretraining costs |
| 1664 p-MEM | Distribution-parameter storage and sampling | Layout-validated simulation, not silicon; CPU/GPU sampling figures remain distinct |
| 1665 CARAMEL | Nonblocking protected audit-log transmission | No numeric utilization/delivery bounds; buffering and threat assumptions unresolved |
| 1691 Visual wakeup | Compact quantized CNN and accelerator | Extraction repaired from saved HTML; 64 nJ/frame at 30 FPS gives 1.92 µW, whereas the source reports 11 µW; accounting boundary unresolved |

## Twenty-second batch

| Paper | Mechanism | Evidence boundary |
|---|---|---|
| 1692 CORE | Power-of-two BCQ scales and FP-INT GEMM | Perplexity decrease is not percent; area/energy gains are not end-to-end LLM gains |
| 1709 QAOA break-even compilation | Surface-code lattice surgery and proxy simulation | Two resource points have distinct error rates; algorithmic break-even is not classical quantum advantage |
| 1712 RAM-CGRA | Reachability-table-guided mapping | Qualitative success/runtime evidence; preprocessing costs unknown |
| 1715 Semi-virtual addressing | Deterministic LATM translation | Effective address space is not physical RAM; protection guarantees remain conditional |
| 1718 RISC-Q | Parameterized quantum-controller generator | Introductory timing requirements are not measured results; release availability unverified |
| 1732 Masked reduction | First-order masked ML-DSA arithmetic | 12.1× reduction versus 1.32× signing gain; TVLA non-detection is not leakage-proof security |

## Twenty-third batch

| Paper | Mechanism | Evidence boundary |
|---|---|---|
| 1741 EPIC | Edge latent encoding and physics-coupled decoding | Fidelity improves on eight of ten datasets; energy claim is communication-only |
| 1742 StepPRM-RTL | Stepwise reward and trajectory-guided fine-tuning | Combined correctness/fidelity threshold lacks per-metric breakdown and budgets |
| 1764 CipherShield | Ciphertext-pattern decorrelation | Lower classification concerns leakage, not legitimate utility; encryption comparator scope unresolved |
| 1765 L2L | Logic/transistor/layout library co-optimization | Separate PPA maxima and averages; maxima need not co-occur |
| 177 ARES | Specification-derived IoT behavior oracles | Bug/CVE counts are author-reported; no independent disclosure verification |
| 1784 Self-evolved ABC | Correctness/QoR-guided source evolution | No quantitative gain or validation scope; repository-wide autonomy unverified |

## Twenty-fourth batch

| Paper | Mechanism | Evidence boundary |
|---|---|---|
| 179 LLMVA | Iterative Verilog-A MTJ modeling and DTCO | Tape-out is not measured macro performance; Front-test/Post-test denominator unspecified |
| 1793 Stone-Skimming | Correlated PTW side-channel characterization | No numeric leakage results or affected-platform scope; no attacks executed |
| 1804 PeRIFi | Geometry-aware RF parameterization and search | DC connectivity does not establish all physical feasibility; training budgets differ |
| 1813 RL4HDL | Diversity-guided synthesis compiler testing | Defect confirmations are author-reported; no comparable testing budget |
| 1822 LHPA | Heterogeneous FPGA LPN pipeline | 52.80× lacks parameter/resource parity and protocol scope |
| 1837 F-FPMAC | Carry-save accumulation and deferred normalization | Fewer overflows is not zero overflow; lower numerical error is not IEEE equivalence |

## Twenty-fifth batch

| Paper | Mechanism | Evidence boundary |
|---|---|---|
| 1839 Moderate-sparsity GPU inference | Three-layer sparse storage and mixed GPU execution | SpInfer kernel and FlashLLM end-to-end gains are not numeric dense-baseline gains |
| 1841 SchemaCoder | Residual Q-Tree parser synthesis | Nine of fourteen applications outperform; pass@1 and score conventions unspecified |
| 1846 COOL | Cooling-aware 3D point thermal surrogate | NMAE is not hotspot-error bound; no measured package validation |
| 1853 SATM | Common-sign column training/mapping | Area/energy gains omit retraining, accuracy and peripheral scope |
| 1858 ReflectBench | Consensus/reflection testbench generation | Internal consensus is not independent validation; two benchmark comparisons remain separate |
| 1859 iPCL-M | Generate/evaluate/optimize routing | 336× evaluator gain is not routing-flow speedup; zero test errors do not establish signoff |

All 145 records have source-separated review packets. Next: resolve the ATB
numeric comparison from primary evidence and continue uncoded descriptions in
stable order, preserving gaps and possible counterexamples.
