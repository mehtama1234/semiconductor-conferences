# Full-paper condition extraction queue — 2026-09-07

This is the next execution queue after description-level adjudication. It does
not treat a populated field as proof that the underlying experiment has been
verified. The current selected sample is 582 records. The deterministic
provenance queue was closed on 2026-09-07; source separation is not the same as
full-paper condition verification.

| Queue | Records | Evidence state | Required extraction |
|---|---:|---|---|
| P0 remediation | 0 | Closed | All 582 packets pass deterministic source/provenance preflight; no packet is accepted scientifically by that check. |
| P1 primary-source strengthening | 31 | Author preprint, author copy, institutional abstract/report, company source, or artifact | Extract section/table/figure locators, platform/process, workload, baseline, metric definition, budget, and limitations. |
| P2 official-description expansion | 541 | Official conference descriptions | Recover manuscript/abstract/artifact evidence; retain unknowns and do not promote description-level numbers as accepted results. |

The first six P1 extraction batches are recorded in
`reports/condition-extraction-batch-2026-09-07.md`. It covers Strix,
MappingEvolve, SERA-Float, RIROS, and Capacitance ML with source locators,
evaluation conditions, and explicit unresolved boundaries.
Batch 2 is recorded in `reports/condition-extraction-batch-2-2026-09-07.md` and
covers UGLMS, Squat, HLPS-DSE, Orthrus, and ATB under the same boundary.
Batch 3 is recorded in `reports/condition-extraction-batch-3-2026-09-07.md`
and covers HybriMoE, Exact-T, NotSoTiny, GAIA, and BusyBarn.
Batch 4 is recorded in `reports/condition-extraction-batch-4-2026-09-07.md`
and covers COSM, Cerberus, Cassandra, PuDGhost, and PLENA.
Batch 5 is recorded in `reports/condition-extraction-batch-5-2026-09-07.md`
and records explicit missing-condition requirements for CANNON, CtxMem, FLASH3D,
HYPER-CIM, and Fusedot.
Batch 6 is recorded in `reports/condition-extraction-batch-6-2026-09-07.md`
and covers HLSArchOpt, ParetoPilot, Icarus’s Wings, Qudit, NIMCH, and COPA.
The first focused ISCA condition extraction is recorded in
`reports/condition-extraction-triage-2026-09-07.md`. It records the simulator,
noise/code assumptions, benchmark suite, baselines, resource regimes, and the
boundary around Triage's reported 52.6% reduction.
The companion GRAINS/Coset extraction is recorded in
`reports/condition-extraction-isca-recovery-batch-4-2026-09-07.md`; it adds
storage/SSD conditions and FPGA/QEC conditions while preserving all claims as
provisional author-preprint evidence.

The first P2 routing tranche is recorded in
`reports/p2-recovery-batch-1-2026-09-07.md`. It prioritizes ten DAC records by
mechanism and claim-risk, while retaining description-only evidence boundaries.
The second P2 tranche is recorded in
`reports/p2-recovery-batch-2-2026-09-07.md`, adding ten compiler, verification,
security, memory, quantization, and serving records.
The third P2 tranche is recorded in
`reports/p2-recovery-batch-3-2026-09-07.md`, adding ten representation,
reliability, edge-system, quantum-control, and LLM-serving records.
The fourth P2 tranche is recorded in
`reports/p2-recovery-batch-4-2026-09-07.md`, adding ten thermal, LLM-memory,
accelerator, security, memory-safety, RF, cloud, and ANN records.
The fifth P2 tranche is recorded in
`reports/p2-recovery-batch-5-2026-09-07.md`, adding ten simulation, packaging,
analog/CIM, security, quantum, safety, distributed-compute, and power-modeling
records.
The sixth P2 tranche is recorded in
`reports/p2-recovery-batch-6-2026-09-07.md`, adding ten graph-learning,
reliability, edge-inference, analog-CIM, lithography, quantum, compiler, and
point-cloud records.
The seventh P2 tranche is recorded in
`reports/p2-recovery-batch-7-2026-09-07.md`, adding ten secure-CIM,
fine-tuning, power-modeling, security, lithography, edge-trust, probabilistic,
and verification records.
The eighth P2 tranche is recorded in
`reports/p2-recovery-batch-8-2026-09-07.md`, adding ten ISCA routes covering
accelerator interfaces, sustainability, memory, storage, ANNS, photonics,
tensor acceleration, and LLM serving.
The ninth P2 tranche is recorded in
`reports/p2-recovery-batch-9-2026-09-07.md`, adding ten ISCA routes covering
tensor optimization, analytic databases, PIM, confidential computing, ORAM,
and microarchitectural side channels.
The tenth P2 tranche is recorded in
`reports/p2-recovery-batch-10-2026-09-07.md`, adding ten ISCA routes covering
coherence, issue-queue scaling, branch/value prediction, heterogeneous memory,
and LLM serving.
The eleventh P2 tranche is recorded in
`reports/p2-recovery-batch-11-2026-09-07.md`, adding ten ISCA routes covering
benchmark methodology, deployed security, agentic compilation, graph and
genome accelerators, robotics, and quantum decoding.
The twelfth P2 tranche is recorded in
`reports/p2-recovery-batch-12-2026-09-07.md`, adding ten adjacent ISCA routes
covering quantum control, MoE/network serving, memory management, edge/cloud
orchestration, low-bit compression, and memory tagging.
The thirteenth P2 tranche is recorded in
`reports/p2-recovery-batch-13-2026-09-07.md`, adding ten ISCA routes covering
storage networking, general-AI dataflow, cooling, inference scaling, deployed
training hardware, intermittent systems, and security architectures.
The fourteenth P2 tranche is recorded in
`reports/p2-recovery-batch-14-2026-09-07.md`, adding ten ISCA routes covering
streaming side channels, point-cloud acceleration, collective communication,
prefetching, emerging-memory caches, reliable DNNs, long-context serving, edge
MoE, and NPU compression.
The fifteenth P2 tranche is recorded in
`reports/p2-recovery-batch-15-2026-09-07.md`, adding ten ISCA routes covering
MoE prefetching, vector/low-bit inference, near-data processing, ANN search,
VLM quantization, compression, and multi-GPU memory systems.
The sixteenth P2 tranche is recorded in
`reports/p2-recovery-batch-16-2026-09-07.md`, adding ten ISCA routes covering
RISC-V GPU/ASIP co-design, DRAM reliability and RowHammer defenses, chiplet PHY
and package simulation, and heterogeneous chiplet execution.
The seventeenth P2 tranche is recorded in
`reports/p2-recovery-batch-17-2026-09-07.md`, adding ten ISCA routes covering
wafer-scale binning, neuromorphic and dynamical-system architectures, neural
rendering simulation, tracing, GPU modeling, CPU predictors, datacenter
networks, simulation, and sparse GEMM.
The eighteenth P2 tranche is recorded in
`reports/p2-recovery-batch-18-2026-09-07.md`, adding ten ISCA routes covering
sparse embeddings, spatial audio, event-driven sensing, video super-resolution,
programmable introspection, private inference, and FHE accelerators.
The nineteenth P2 tranche is recorded in
`reports/p2-recovery-batch-19-2026-09-07.md`, adding ten ISCA routes covering
GPU/FHE memory optimization, ray-tracing and Gaussian-splatting accelerators,
instruction and memory prefetching, speculative translation, and quantum
compilation/layout.
The twentieth P2 tranche is recorded in
`reports/p2-recovery-batch-20-2026-09-07.md`, adding ten ISCA routes covering
sparse-matrix scheduling, collective communication, RDMA atomics, verification
and fuzzing, memory consistency/formal methods, and CPU/GPU prefetching.
The twenty-first P2 tranche is recorded in
`reports/p2-recovery-batch-21-2026-09-07.md`, adding ten ISCA routes covering
neural prefetching, quantum compilation/simulation/photonic architectures,
Ising/SAT compilation, cluster power and thermal management, and distributed
LLM synthesis.
The twenty-second P2 tranche is recorded in
`reports/p2-recovery-batch-22-2026-09-07.md`, adding ten ISCA routes covering
disaggregated training, MoE/MLLM serving, accelerator scheduling, flexible
precision, LLM/SNN/FPGA compute, computational-memory offload, PIM compilation,
and near-cache locality.
The twenty-third P2 tranche is recorded in
`reports/p2-recovery-batch-23-2026-09-07.md`. It routes the eight remaining
titled ISCA records (166–173), covering near-cache, hybrid PIM/3D-DRAM,
reconfigurable SIMT, graph transformers, zero-knowledge proofs, sparse matrix
engines, and embodied-AI planning; IDs 174–175 have no titled inventory rows.
The twenty-fourth P2 tranche is recorded in
`reports/p2-recovery-batch-24-2026-09-07.md`, adding ten DAC routes covering
timing analysis, PCB placement, characterization, heterogeneous GNNs,
hyper-dimensional computing, Gaussian splatting, RTL simulation, package power,
graph learning, and dataflow generation.
The twenty-sixth P2 tranche is recorded in
`reports/p2-recovery-batch-26-2026-09-07.md`, continuing the DAC frontier across
scale-up networks, safety-critical accelerators, DRC, embodied-planning memory,
watermarking, CAMs, Gaussian splatting, SSD testing, BFP NPUs, and analog
in-pixel modeling.
The twenty-fifth P2 tranche is recorded in
`reports/p2-recovery-batch-25-2026-09-07.md`, continuing the DAC priority
frontier across MoE scheduling, buffering, satellite federated learning,
analog/CIM dynamics, quantum compilation, PMU security, logic optimization, CPU
DSE, and graph-based circuit matching.
The twenty-seventh P2 tranche is recorded in
`reports/p2-recovery-batch-27-2026-09-07.md`, continuing the DAC frontier across
TCAD surrogates, low-power test, FPGA area recovery, secure CIM/PUF, encrypted
inference, graph CIM, GPU circuit simulation, robust quantum readout, edge
inference, and MoE quantization.
The twenty-eighth P2 tranche is recorded in
`reports/p2-recovery-batch-28-2026-09-07.md`, continuing the DAC frontier across
clock-tree synthesis, capacitance extraction, analog CIM, point-cloud sampling,
graph sparsity, distributed matrix multiplication, heterogeneous edge SoCs,
optical synthesis, and dynamic-shape neural networks.
The twenty-ninth P2 tranche is recorded in
`reports/p2-recovery-batch-29-2026-09-07.md`, continuing the DAC frontier across
RowHammer monitoring, process-window optimization, DNN bit-flip defense,
single-GPU fine-tuning, inverse lithography, timing placement, NAND/CIM MoE
inference, hypergraph partitioning, SEM imaging, and chip-to-chip exploration.
The thirtieth P2 tranche is recorded in
`reports/p2-recovery-batch-30-2026-09-07.md`, continuing the DAC frontier across
hypergraph partitioning, thermal/kernel-aware inference, diffusion quantization,
variation-tolerant analog inference, quantum placement/compilation,
placement/sizing, chiplet thermal modeling, RowHammer attacks, and PIM
scheduling.
The forty-sixth P2 tranche is recorded in
`reports/p2-recovery-batch-46-2026-09-07.md`, continuing the DAC frontier across
microscaling, post-quantum edge security, GPU hypergraph partitioning, wafer-scale
cost modeling, CPU-GPU MoE execution, multi-vector retrieval, learned approximate
arithmetic, voltage side-channel analysis, stochastic computing, and encrypted
sparse multiplication.
The forty-seventh P2 tranche is recorded in
`reports/p2-recovery-batch-47-2026-09-07.md`, continuing the DAC frontier across
CXL-tiered graph search, edge LLM optimization, in-memory quantization, 3D/3nm
NoC DTCO, photonic ZKPs, encrypted databases, IR-drop-aware placement,
drift-resilient RRAM, heterogeneous mobile RAG, and FPGA-tool fault injection.
The thirty-first P2 tranche is recorded in
`reports/p2-recovery-batch-31-2026-09-07.md`, continuing the DAC frontier across
prefix-KV retrieval, video enhancement, zero-knowledge tracing, emulation
scheduling, elastic LLM memory, processor fault localization, LLM-generated
assertions, 3D near-memory generation, graph PIM, and Apple-SoC side channels.
The thirty-second P2 tranche is recorded in
`reports/p2-recovery-batch-32-2026-09-07.md`, continuing the DAC frontier across
cryptographic verification, sparse GEMM, SAR graph optimization, equivalence
checking, FIT prediction, heterogeneous FPGA placement, RF synthesis, NPU
dataflow, VRRAM/CIM vision, and MoE checkpointing.
The thirty-third P2 tranche is recorded in
`reports/p2-recovery-batch-33-2026-09-07.md`, continuing the DAC frontier across
RTL verification agents, neural circuit simulation, SNN security, layout pattern
matching, heterogeneous GNNs, quantum syndrome extraction, ViT search,
transient-execution defense, sparse tensor code generation, and NDP edge-LLM
mapping.
The thirty-fourth P2 tranche is recorded in
`reports/p2-recovery-batch-34-2026-09-07.md`, continuing the DAC frontier across
low-bit LLM PIM, CPU timing side channels, distributed-GNN compression, PCB
ground-plane co-design, spiking transformers, TriSpGEMM, cloud-TEE availability,
RISC-V fuzzing, chiplet DSE, and real-time GPU scheduling.
The thirty-fifth P2 tranche is recorded in
`reports/p2-recovery-batch-35-2026-09-07.md`, continuing the DAC frontier across
maze routing, SRAM CIM dataflow, GPU WCET, graph vector search, timing
characterization, reconfigurable DNN acceleration, 3D-NAND LLM inference,
multiphysics thermal stress, robust driving perception, and CPU-FPGA measurement.
The thirty-sixth P2 tranche is recorded in
`reports/p2-recovery-batch-36-2026-09-07.md`, continuing the DAC frontier across
graph-RAG PIM, neutral-atom compilation, complex-valued uncertainty, RL-aligned
RTL generation, ViT security, ferroelectric-NAND databases, TSN shaping,
erasure-coded KV caches, SAT sweeping, and neuromorphic SNNs.
The thirty-seventh P2 tranche is recorded in
`reports/p2-recovery-batch-37-2026-09-07.md`, continuing the DAC frontier across
learned multi-corner analysis, control-flow auditing, FP/INT GEMM, early
fault-tolerant surface-code economics, CGRA mapping, ML-DSA side-channel
reduction, physics-guided distributed ML, process-reward RTL tuning, TEE
ciphertext side channels, and standard-cell exploration.
The thirty-eighth P2 tranche is recorded in
`reports/p2-recovery-batch-38-2026-09-07.md`, continuing the DAC frontier across
IoT protocol fuzzing, self-evolved EDA, Verilog-A/MRAM co-optimization,
page-table-walk attacks, FPGA compiler testing, post-quantum LPN acceleration,
factored floating-point MACs, sparse LLM inference, log-schema extraction, and
cooling-aware package thermal prediction.
The thirty-ninth P2 tranche is recorded in
`reports/p2-recovery-batch-39-2026-09-07.md`, continuing the DAC frontier across
CIM security, agentic testbench generation, chip-layout pretraining, hybrid-bonded
3D eFlash thermal stability, SSD aging, BEV detection NAS, compressed GEMM, SNN
co-design, embodied VLA speculative decoding, and silicon thermal reconstruction.
The fortieth P2 tranche is recorded in
`reports/p2-recovery-batch-40-2026-09-07.md`, continuing the DAC frontier across
DRAM-PIM interference, in-vehicle attack tracing, personalized edge MoE,
federated-learning energy, multi-GPU translation, circuit graph learning, FPGA
prefill/decode swapping, safety assertions, leakage estimation, and HDC LiDAR.
The forty-first P2 tranche is recorded in
`reports/p2-recovery-batch-41-2026-09-07.md`, continuing the DAC frontier across
quantum power-system solvers, Hamiltonian pretraining, ATPG-free testing,
diffusion acceleration, row-aligned PIM attention, PCB 3D generation, adaptive
quantization, ternary LLM inference, transistor placement/routing, and synthesis.
The forty-second P2 tranche is recorded in
`reports/p2-recovery-batch-42-2026-09-07.md`, continuing the DAC frontier across
RTL simulation, approximate DCiM, floorplanning, 4D/3D Gaussian splatting, edge
sparsity, routability/track assignment, multi-die FPGA HLS, GPU fuzzing, and
fault-tolerant AI scheduling.
The forty-third P2 tranche is recorded in
`reports/p2-recovery-batch-43-2026-09-07.md`, continuing the DAC frontier across
knowledge distillation, robotics diffusion, ZNS graph memory, confidential-VM
migration, secure CIM, CodeLLM FPGA DSE, FPGA debugging, inverse lithography,
adaptive activations, and memristor-memory NoCs.
The forty-fourth P2 tranche is recorded in
`reports/p2-recovery-batch-44-2026-09-07.md`, continuing the DAC frontier across
quantum-error-correction hardware, sparse GPU linear algebra, secure biochips,
graph PIM, neuro-symbolic hardware, personalized CIM, side-channel monitoring,
circuit simulation, wafer-scale communication, and 3D placement.
The forty-fifth P2 tranche is recorded in
`reports/p2-recovery-batch-45-2026-09-07.md`, continuing the DAC frontier across
advanced routing, equivalence checking, LLM-assisted DRC repair, reconfigurable
systolic arrays, Ising optimization, diffusion-language-model serving, parasitic
extraction, hardware-Trojan detection, asymmetric quantization, and MoE
scheduling.
The forty-sixth P2 tranche is recorded in
`reports/p2-recovery-batch-46-2026-09-07.md`, continuing the DAC frontier across
microscaling, post-quantum edge security, GPU hypergraph partitioning, wafer-scale
cost modeling, CPU-GPU MoE execution, multi-vector retrieval, learned approximate
arithmetic, voltage side-channel analysis, stochastic computing, and encrypted
sparse multiplication.
The forty-seventh P2 tranche is recorded in
`reports/p2-recovery-batch-47-2026-09-07.md`, continuing the DAC frontier across
CXL-tiered graph search, edge LLM optimization, in-memory quantization, 3D/3nm
NoC DTCO, photonic ZKPs, encrypted databases, IR-drop-aware placement,
drift-resilient RRAM, heterogeneous mobile RAG, and FPGA-tool fault injection.
The forty-eighth P2 tranche is recorded in
`reports/p2-recovery-batch-48-2026-09-07.md`, continuing the DAC frontier across
resilient LLM inference, memory-constrained MoE scheduling, sub-bit compression,
LLM reference-model verification, generative circuit design, ReRAM CIM, graph
timing prediction, physics-prior compact modeling, KV-cache offload, and device
simulation.
The forty-ninth P2 tranche is recorded in
`reports/p2-recovery-batch-49-2026-09-07.md`, continuing the DAC frontier across
layer-aware IMC error correction, tensor-centric verification, hot-switched CPU
LLM serving, photonic inverse design, real-time DAG scheduling, RTL assertion
generation, voltage-underscaled MACs, secret tracking, FPGA weightless learning,
and posit-like microscaling.
The fiftieth P2 tranche is recorded in
`reports/p2-recovery-batch-50-2026-09-07.md`, continuing the DAC frontier across
wide-bit digital CIM, universal circuit modeling, stochastic edge detection,
flip-flop exploration, cloud microservice interference, temporal motif mining,
LLM PCB generation, mixed-precision GEMM, complementary-FET layout, and
hybrid-bonded speculative decoding.
The fifty-first P2 tranche is recorded in
`reports/p2-recovery-batch-51-2026-09-07.md`, continuing the DAC frontier across
cross-layer reliability, MRAM binary CIM, heterogeneous LLM PIM, LLM protocol
patching, sparse tensor cores, flow-matching placement, thermal-aware SRAM,
GPU shared memory, video-diffusion token reduction, and FPGA ZKPs.
The fifty-second P2 tranche is recorded in
`reports/p2-recovery-batch-52-2026-09-07.md`, continuing the DAC frontier across
SAT model checking, policy-learned full-chip ILT, GPU-cluster forecasting,
coordinated CPU fuzzing, hardware-security GNN evasion, crosstalk timing,
neutral-atom detection, LLM Verilog generation, disaggregated-memory contention,
and multi-instance GPU serving.
The fifty-third P2 tranche is recorded in
`reports/p2-recovery-batch-53-2026-09-07.md`, continuing the DAC frontier across
RL placement, timing-arc reuse, speculative MoE decoding, hierarchical video
precision, lattice-surgery compilation, decomposed-LLM inference, fault-tolerant
compilation, local-address SRAM, ZNS filesystem units, and multi-agent SDC.

The categories overlap by design: P0 is a remediation priority, while P1/P2
describe evidence depth. The former P0 records are retained in
`reports/review-remediation-queue-v1.md` as a dated recovery trail. Their
institutional, company, or artifact descriptions remain weaker than manuscripts
and still require condition extraction and independent review.

## Extraction checklist

For every promoted quantitative claim, capture the exact source locator and:
workload/model, hardware and process, software/runtime, baseline, scale,
precision/accuracy or correctness condition, units, evaluation budget, and
tradeoffs. Distinguish simulation from silicon, communication or kernel speedup
from end-to-end speedup, and author/company reporting from independent
reproduction. If any condition is unavailable, keep the claim narrowed or
withheld and record the missingness in the packet.

The queue is complete as a routing artifact, not as completion of the extraction
work. Independent review remains pending for all 582 packets.
