# Semiconductor technology direction synthesis — v1 provisional

This is the root-level synthesis of the current ISCA, DAC, and ICCAD workspaces.
It asks what detailed capabilities are appearing across the selected evidence,
how the conferences complement one another, and what is required before calling
any direction a measured trend.

The machine-readable evidence map is [`data/technology-direction-evidence-v1.json`](../data/technology-direction-evidence-v1.json).

For deeper mechanisms, counterpressures and explicit forward-looking hypotheses,
read [Where the field may be heading](field-directions-and-hypotheses-v1.md).
It separates suggested research directions from measured temporal trends.

The evidence is intentionally asymmetric:

- DAC: 543 official 2026 research descriptions plus one technically coded 2025
  recovery record; the selected DAC sample is 88 records and independent acceptance
  remains pending.
- ISCA: 173 official 2026 program slots (172 titled); 16 technically coded
  records; 4 secondary-only papers pending primary verification.
- ICCAD: 2026 scope evidence and a 319-entry 2025 fallback inventory; 21 technically
  coded fallback papers. The inventory includes 43 invited papers and ten student
  presentations, not 319 regular papers; see the [scope audit](../iccad/reports/program-scope-audit-v1.md).

The 371-record technical coding sample is selected for recoverable evidence and
technical diversity. It is not a prevalence estimate, market forecast, conference
ranking, or proof that a direction is rising.
For a mechanism-level follow-up, see [scheduling versus physical surrogates](../iccad/reports/scheduling-versus-surrogates-v1.md): two analysis accelerators with different correctness and generalization requirements.
All 371 remain independently unaccepted. The original synthesis-anchor set is
distinct from the expanded coded sample and is not enlarged by metadata recovery.

## Executive interpretation

The selected evidence contains multiple examples of coupled engineering.
These papers optimize a loop spanning model or algorithm, architecture,
compiler/runtime, memory/interconnect, physical constraints, and reliability—rather
than treating each layer as an isolated design problem. This is a pattern within
the selected sample, not a measured increase over time.

The most defensible conclusion is therefore a capability statement:

> Semiconductor and computer-system research is developing methods that make
> cross-layer constraints executable inside design, mapping, scheduling, and
> verification loops.

“AI” is part of this picture, but it is not the complete explanation. Mechanisms
include learned search, tool-grounded generation, data-movement-aware
architecture, physical modeling, ECC coordination, fault mitigation, and
security-aware evaluation.

The expanded sample also includes SatSFL, which extends this cross-layer pattern
to intermittent satellite links: gradient approximation and adaptive compression
are coupled to the communication regime. Its official description provides no
numeric convergence, accuracy, trace, or deployment conditions, so it is a
capability example rather than a measured trend or accepted synthesis anchor.

The latest DAC systems batch makes the data-movement and workload co-design branch
more concrete: C2C-Explorer uses workload-derived chip-to-chip traffic in Bayesian
design-space exploration; Marlin treats prefix-KV retrieval as an I/O and overlap
problem; eLLM unifies GPU/CPU tensor memory under SLO-aware scheduling; PIMGRAG
co-designs graph-RAG retrieval across PIM and GPUs; and Pegasus places MoE experts
for personalized edge execution. These records suggest a shared pressure to make
placement, locality, interconnect, and scheduling workload-aware, while their
official-description evidence still does not establish comparable generality or
independent numerical validity.

The next DAC batch extends the same map across distinct constraints: AgenticDSE
uses multi-agent, phase-wise Bayesian exploration for chiplet designs; adaptive
KV prefetching makes token prediction and transfer overlap explicit; semi-virtual
addressing couples deterministic translation to microcontroller memory safety;
PhotoMT splits zero-knowledge Merkle computation across photonic and digital
engines; and Rememtier co-designs CXL tiering with burst-resistant replacement.
Together these are evidence of cross-layer specialization, not evidence that one
mechanism dominates the field.

The underrepresented-branch additions show that the same cross-layer pattern is
not limited to LLM accelerators: PRO-V-R1 makes verification-tool feedback part of
agent training; RISC-Q makes quantum-control timing and generator structure
executable; COOL inserts package boundary conditions into a thermal surrogate;
S²CIM couples cryptographic protection to FeFET circuit operation; and TierANNS
co-designs CXL placement with graph-search queues. Their descriptions support
mechanism-level thematic links, but not yet comparable end-to-end evidence.

The runtime/security batch adds another recurring structure: resource constraints
are being modeled as part of correctness or safety. RTFL schedules quantization and
device participation under battery and bandwidth limits; GPU-Fuzz turns operator
constraints into memory-error tests; drcAgent closes the loop with commercial DRC
tools; M²CAM adapts matching precision to memristor variation; and MemFlow makes
contention along a disaggregated memory path explicit. These are thematic links,
not a claim that the methods share evaluation quality or deployment maturity.

The architecture/physical batch extends the same pattern from runtime policy into
implementation and verification: two-tier Verilog generation couples LLM output
to simulation and hardware checks; undocumented-instruction analysis couples
discovery to security verification; 3D-ReSAC treats refresh and communication as
first-class memory costs; PNO-Therm transfers PDE structure across thermal designs;
and the NoC DTCO study exposes backside routing and PDN assumptions in link-level
tradeoffs. These mechanisms are comparable thematically, not numerically.

The optimization/serving batch shows the same movement toward explicit feedback:
inverse lithography uses policy learning over mask distributions; quantum
calibration schedules experiments against drift and information gain; HW-Router
feeds live GPU and KV-cache signals into model routing; UniNL exposes nonlinear
operator structure to edge hardware; and DiffFill optimizes delay rather than
only density proxies. The shared theme is useful for taxonomy, but evidence
quality and evaluation boundaries remain heterogeneous.

The precision/security batch adds two related forms of adaptability: AMBER and
SAEM exploit bit- and stage-level regularity to reduce movement and compute, while
the sparse GPU and PiMM-NoC papers expose storage/mapping structure to hardware
execution. Attackonctf adds an evaluation-layer counterpart by testing whether
security benchmarks measure semantics rather than syntax. These links broaden the
taxonomy but do not make the reported gains directly comparable.

The elastic-serving/reliability batch links service objectives to physical and
architectural state: sMoE scales experts under cost and P95 constraints;
MoE-Balance overlaps CPU/GPU transfer with expert execution; GreenLLM separates
prefill/decode DVFS; IR-drop-aware placement feeds power integrity into physical
optimization; and Accshield maps operator sensitivity to unreliable arrays. This
is a coherent thematic branch, while evidence conditions still vary substantially.

The graph/verification batch reinforces that cross-layer engineering also appears
in non-LLM workloads: DIA-CIM reshapes graph dependencies around a CIM dataflow;
RISC-V cryptography verification turns invariants into reusable proof structure;
SafeGen links safety semantics to fault mapping and formal assertions; GREEN makes
cloud placement a graph optimization; and SpecANNS moves graph-search distance
work into storage. These records broaden the field map without making their
accuracy, energy, proof, or latency claims interchangeable.

The physical/security/reliability batch shows the same cross-layer constraint
handling in mature flows: HyPAS joins differentiable search to discrete signoff;
real-time GPU scheduling joins DAG dependencies to bounded response time;
Safe-IoT couples post-quantum arithmetic to memory limits; vTen turns tensor
intent into batched verification execution; and adaptive NAND retry uses retention
state to preserve capacity. These links broaden the capability map, not a common
performance ranking.

The compiler/thermal/memory batch emphasizes observability and implementation
boundaries: neutral-atom compilation trades search memory for routing overhead;
Janus uses ARM primitives to make speculation defense compiler-visible; thermal
diffusion reconstructs 3D fields from heterogeneous sensors; CLUE-ECC pools
parity across memory layers; and LOHA splits graph traversal from storage
re-ranking. These are mechanism-level connections, not a common benchmark.

The methodology/storage/reliability batch extends this pattern into infrastructure:
IMPart embeds memetic search in hypergraph uncoarsening; the AiMX compiler removes
host-side movement; HDDB uses HDC redundancy to tolerate FeNAND noise; XRel-Graph
distributes fault mitigation across abstraction layers; and REPAIR makes NVM write
endurance a CAD and runtime scheduling objective. These are capability links, not
evidence of uniform deployment maturity.

## Direction 1 — Tool-grounded AI for design and verification

The [HLSArchOpt partial-artifact assessment](../dac/reports/hlsarchopt-primary-assessment-v1.md)
identifies an author-linked Fire-module implementation, not a reproduced complete
LLM workflow. Its inspected script disables simulation checks; numerical claims
remain withheld pending benchmark and correctness conditions.

### Specific subskills

- hierarchical multi-agent decomposition of chiplet design;
- multi-role RTL generation with synthesis/timing/PPA feedback;
- RL generation whose reward comes from compilation or simulation;
- HLS bug localization, classification, and correction;
- LLM-controlled HLS design-space exploration;
- executable technology-map evolution with regression checks.

### Evidence distribution

DAC supplies the largest description-level set of AI-for-EDA mechanisms. ICCAD’s
2025 fallback supplies primary-preprint cases for MAHL, VeriOpt, VERIRL, and
HLSDebugger, allowing detailed inspection of hierarchy, PPA feedback, and
correctness. ISCA contributes CODO as a primary-preprint-backed compiler case,
where dataflow legality and accelerator execution are co-optimized.

### Interpretation and limit

The shared capability is tool-grounded iteration, not generic text generation.
The evidence does not establish average-case correctness, API/model cost,
transfer across design suites, or production adoption. Read the [DAC capability
map](../dac/pages/topical-capability-map-2026.md) and [ICCAD capability
map](../iccad/pages/topical-capability-map-2025-fallback.md).

NotSoTiny adds a benchmark-design mechanism to this direction: contextual task
selection, formal/simulation gates, and living updates are themselves part of the
measurement system. Its pinned evaluator inspection counts a timeout as an
equivalence success, so benchmark quality depends on preserving proof-state
semantics and versioned task/run logs—not only on increasing task count.

## Direction 2 — Data movement as an algorithm/architecture contract

### Specific subskills

- expert-selection forecasting and placement for MoE inference;
- disaggregated compute/network/storage coordination;
- CXL near-memory ANN search and OS/hardware tiering;
- row-aligned sparse-attention PIM;
- KV-cache contiguity, recomputation, and memory management;
- cooperative CPU/PIM scheduling under bank and bus interference.

### Evidence distribution

ISCA provides primary cases for MoE movement, disaggregated training, COSM, and
LLM memory/quantization, plus company-source evidence from Panmnesia’s
silicon-proven CXL controller/switch and Meta’s Vistara deployment path. DAC
provides CANNON, CtxMem, RAF, REFLEX, MBA, and KEEP
as official-description cases spanning CXL, near-memory processing, and KV-cache
management. ICCAD’s Tasa connects bandwidth and memory placement to 3D-stacked
thermal constraints in the 2025 fallback.

RAF's [communication-bound assessment](../dac/reports/raf-primary-recovery-v1.md)
preserves baseline pairing but leaves proof assumptions and evaluation conditions
unresolved. Remote-access elimination is not zero local traffic, and claimed
communication optimality does not establish universal latency/energy optimality.

BusyBarn provides an additional artifact-only follow-up for this direction. Its
author-linked package exposes hierarchical mapping and BALD fault-tolerant routing;
one normalized 16KB AllGather case completed at 80 artifact simulation time units
under a 4x6, 256-bandwidth configuration. That result is a reproducibility check,
not a paper metric: no complete figure, matched baseline, end-to-end workload, or
independent reproduction was obtained. It remains outside the 371-record selected
coding sample and cannot support a comparative performance claim.

CANNON's [recovery assessment](../dac/reports/cannon-primary-recovery-v1.md)
records differing official and institutional performance headlines. Numerical
synthesis is withheld pending reconciliation with recall-matched baselines and
memory-capacity conditions; reported hardware implementation alone is insufficient.

The newly coded ATB case adds a related but distinct mechanism: asymmetric GEMM
tile buffering trades higher arithmetic intensity against kernel-switching cost
on XDNA2. Its preprint preserves a printed 4.54x claim alongside endpoint ratios
of 5.06x/5.13x under different matrix dimensions, so it supports the mechanism
and the need for matched-workload accounting—not a corrected speedup estimate.

### Interpretation and limit

Movement is being treated as part of the computation contract: placement,
migration, locality, topology, and contention affect the algorithm’s outcome. The
company-source records add a productionization subskill: CXL must be carried from
controller and switch silicon through firmware, OS tiering, fleet operations, and
workload-specific capacity planning.
The samples use different workloads, topologies, memory technologies, and metrics;
they do not justify ranking CXL, PIM, HBM, or a particular scheduling strategy.
Company-reported deployment metrics remain claims requiring paper-level and
independent deployment verification.
The [CtxMem recovery assessment](../dac/reports/ctxmem-primary-recovery-v1.md)
keeps its description-level simulation results distinct from the company deployment
cases; missing experimental conditions prevent accepted numerical comparisons.

## Direction 3 — Reliability and security move into the main design loop

### Specific subskills

- cross-layer ECC and Encode-Once/Decode-Many recovery;
- ECC-aware bank-PIM correction scheduling;
- physical PuD interference measurement and layout mitigation;
- NPU fault localization and correction across microarchitecture, ISA, and code;
- joint EM/IR physical-integrity modeling;
- telemetry-based model confidentiality attacks;
- adversarial disruption of MoE caching and prefetching.

### Evidence distribution

ISCA’s detailed memory cluster covers runtime contention, coordinated ECC, physical
interference, and correction-aware PIM. DAC contributes Strix, BFP reliability,
GEMIR, and adversarial/security cases. ICCAD contributes Energon and its 2025
fallback security/reliability cases, while the 2026 scope confirms that security,
reliability, and advanced integration remain in scope.

### Interpretation and limit

The common capability is explicit modeling of failure, threat, or physical
integrity conditions during design. Threat models, fault models, and correctness
guarantees remain distinct; they cannot be combined into one “robustness” score.
See the [ISCA memory/ECC/PIM analysis](../isca/pages/memory-ecc-pim-reliability.md).

The expanded DAC sample sharpens this direction into distinct threat and
recovery mechanisms: a one-bit Rowhammer path against Falcon, cross-component
Apple M2 cache leakage, LLM-assisted FPGA toolchain vulnerability discovery,
and layer-adaptive analog-CIM ECC. These are not one common security score:
attack feasibility, disclosure, fault correction, and model reliability require
different threat and fault models. Their official descriptions omit enough
platform and experiment detail that no numeric security or reliability ranking
is accepted.
The [Strix primary assessment](../dac/reports/strix-primary-assessment-v1.md)
adds configuration-specific evidence limits; its timing and reliability claims
must not be broadened into safety certification or universal fault coverage.
For GEMIR, [primary recovery remains incomplete](../dac/reports/gemir-primary-recovery-v1.md).
Its description-level error-reduction figures lack resolved comparison conditions
and are excluded from accepted quantitative synthesis.

## Direction 4 — Physical integration becomes an optimization variable

### Specific subskills

- reduced-order chiplet thermal modeling with coupled interface ports;
- fast 3D-IC thermal solving for repeated design exploration;
- thermal-aware 3D-stacked LLM placement and bandwidth sharing;
- package power-plane synthesis under metal-density constraints;
- physical-layout configuration inside hierarchical agentic design flows.

### Evidence distribution

DAC supplies FLASH3D, LegoTherm, package/power-plane, and related physical-design
records. ICCAD’s Tasa and MAHL provide primary fallback cases linking thermal,
bandwidth, chiplets, and layout. ISCA’s Lit Silicon adds a runtime view in which
thermal imbalance creates multi-GPU stragglers.

FLASH3D remains description-level, steady-state evidence. Its
[source-depth assessment](../dac/reports/flash3d-primary-recovery-v1.md) withholds
quantitative synthesis until matched solver and workload conditions are known;
the university announcement is not independent validation, and the slice count
uses a baseline inference-time budget rather than seconds.

### Interpretation and limit

The evidence supports earlier coupling of thermal, packaging, bandwidth, and
workload decisions. It does not establish manufacturing readiness, a winning
packaging technology, or generalization beyond the evaluated geometry, materials,
devices, and workloads.

The new process-focused records add a second physical-design pattern: CPW-SMO
generates a common source and mask set, differentiable MDP-ILT couples wafer
fidelity to mask writability, and FreqSEM uses frequency-aware segmentation for
sub-nanometer contour extraction. They support a capability hypothesis that
manufacturing objectives are being pulled earlier into differentiable or
learned loops, but the descriptions do not establish calibrated fab transfer or
metrology generalization.

## Direction 5 — Search and modeling become multi-fidelity and physics-aware

### Specific subskills

- robust Bayesian analog sizing under process variation;
- multi-fidelity Bayesian microarchitecture exploration;
- hierarchical PPA surrogates calibrated with silicon-consistent points;
- physics-informed joint EM/IR prediction;
- exact quantum synthesis with a resource-specific objective;
- device stochasticity used as a computational primitive.

### Evidence distribution

DAC provides the broadest selected set of learned and physics-aware design-space
methods. ICCAD’s RSizing and NeuroPDE provide primary fallback cases showing
uncertainty-aware analog search and algorithm/device co-design. ISCA contributes
compiler and architecture cases where the objective includes movement, thermal
behavior, or hardware resources.

### Interpretation and limit

The important skill is not choosing a fashionable optimizer; it is preserving
legality, uncertainty, physical structure, and evaluation budget through the loop.
Reported surrogate accuracy or figure-of-merit gains require baseline budgets,
constraint-violation analysis, and independent reproduction.

The [HYPER-CIM assessment](../dac/reports/hyper-cim-primary-recovery-v1.md)
separates training design points, predicted configurations and five reported
fabricated macros. It withholds numerical synthesis until FoM normalization,
operating conditions and surrogate validation are available; the predicted space
is not a silicon-tested population.

Adder-DCIM adds a complementary representation-aware case from the ICCAD
fallback: model compression, bit flexibility, and digital CIM circuitry are
co-designed rather than evaluated as isolated kernels. Its institutional report
does not expose voltage, frequency, power boundary, or accuracy convention, so it
supports the mechanism taxonomy but not a cross-paper TOPS/W ranking.

For the exact-T example, consult the [primary assessment](../dac/reports/exact-t-primary-assessment-v1.md):
the description and preprint disagree on the maximum reduction. Keep that
numerical headline withheld; the resource-specific mapping mechanism remains a
provisional example, not evidence of learned search or global circuit optimality.
Its figure-level counterexample also prevents a uniform space-time-benefit claim;
available artifact checks do not yet establish coherent-oracle correctness.

The new QAgent and PIMA-SecDB cases extend this direction beyond conventional
EDA: multi-agent placement makes circuit execution cost part of the quantum
compilation objective, while FHE database PIM makes cryptographic parameter
selection part of the memory architecture. Both are workload- and parameter-
conditioned capabilities, not evidence that one optimizer or PIM organization
is generally superior.

## Direction 6 — Specialized accelerators encode workload structure

FuseDot's [recovery assessment](../dac/reports/fusedot-primary-recovery-v1.md)
keeps multiplication-count reduction separate from end-to-end gains. Quantization
group rules, finite-precision accuracy, reordering costs and exact baseline
configurations remain unresolved; numerical synthesis is withheld.

### Specific subskills

- outlier-aware LUT GEMM and dual-side quantization;
- multiplication sharing for low-bit LLM dot products;
- structured-sparsity spatial dataflow;
- MoE routing and expert-placement hardware/software co-design;
- graph, Gaussian-splatting, and embodied-planning specialization;
- training-free speculative decoding with hardware format conversion.

### Evidence distribution

ISCA contributes primary cases for OASIS, Patterns Behind Chaos, Cassandra, and
related LLM systems. DAC contributes a larger description-level accelerator sample
covering LUTs, low-bit arithmetic, graph structure, rendering, and PIM. ICCAD’s
fallback cases add thermal-aware stacked inference and device-specific computation.

### Interpretation and limit

The field is specializing around data representation, routing, locality, and
memory behavior rather than only adding multiply-accumulate units. Speedup claims
remain conditional on model suite, sequence length, accuracy, area, energy,
precision, and baseline hardware.

## Conference complementarity

| Conference | Strongest current contribution | Evidence boundary |
|---|---|---|
| DAC 2026 | Breadth of design-flow, accelerator, physical-design, memory, and reliability descriptions | Mostly official descriptions; selected 200 are not full-corpus prevalence |
| ISCA 2026 | Deep primary and industry-source cases for system architecture, LLM execution, memory, PIM, ECC, CXL, integrated networking, and thermal behavior | 16 primary/institutional/company records plus 4 unresolved secondary queue items; full program remains mostly metadata |
| ICCAD 2025 fallback | Design automation, verification, chiplet, analog, security, and emerging-device depth | 2026 paper corpus unavailable; 2025 evidence cannot establish 2026 change |

The conferences should therefore be read as complementary instruments: DAC gives
breadth across the design stack, ISCA gives system/architecture mechanisms, and
ICCAD gives design-flow and physical-design depth. Combining raw counts would
discard the evidence asymmetry.

## What must happen before a final trend claim

The latest DAC batch adds five mechanism-level signals: interrupt observability
as a hardware security surface; heterogeneous, bandwidth-aware acceleration for
post-quantum LPN; graph-neural transient surrogates with inverse analog design;
topology- and workload-aware NUMA storage coordination; and interaction-aware
simultaneous DNN fault injection. Together they reinforce a cross-layer pattern
in which security, cryptography, locality, analog behavior, and reliability are
made executable inside architecture or verification loops. These are selected
official-description cases, not prevalence or directional evidence.

The next five cases extend that pattern into availability and assurance: verifiable
CPU commitments for TEEs, executable IoT protocol behavior oracles, transistor-level
placement beyond standard cells, dynamic parity for aging SSDs, and hardware
correlation-aware decoding for photonic quantum error correction. They suggest that
security, physical design, storage endurance, and quantum correctness are increasingly
being treated as runtime or design-flow constraints. The claims remain conditional
on the captured descriptions and still require independent review.

A further five cases add PMU-event timing side channels, branch-divergence-aware
GPU WCET analysis, directional transport for neutral-atom CZ gates, hardware-aware
BEV detection search, and CodeLLM-guided HLS exploration. The common signal is
constraint-aware tooling: timing, security, physical connectivity, hardware limits,
and compiler search are being represented explicitly rather than left to late-stage
manual tuning. This remains a selected-case interpretation, not a prevalence claim.

The latest batch adds hardware-aware KNN point-cloud acceleration, thermal delay-fault
mapping for driving perception, graph traceback across in-vehicle networks, noise-
robust on-device CIM personalization, and LLM threat-to-assertion SoC verification.
These cases connect representation-aware compute, automotive safety, security
operations, adaptive learning, and formal assurance into end-to-end loops. Their
headline numbers remain provisional until full conditions and independent review are
available.

The newest batch adds masked ML-DSA root-of-trust optimization, community-aware
hardware-Trojan detection, AlphaZero generative AIG synthesis, timing-based ECC
recovery in ReRAM, and wafer-level semiconductor tool-chain attestation. These
cases extend the cross-layer pattern from runtime systems into cryptographic
implementation, design synthesis, hidden-memory behavior, and manufacturing
provenance. The evidence is still selected and description-level where noted.

The ten-record acceleration batch adds hardware-aware ViT search, CPU timing-side-
channel defense and disassembly, bit-sliced MoE caching, multi-GPU translation
dissemination, heterogeneous confidential-VM migration, graph-transformer analog
parasitic extraction, flexible elliptic-curve ISA support, and electromagnetic
quantum-reliability modeling. These reinforce a field pattern of making deployment,
security, and physical constraints first-class optimization inputs.

The next nine cases add PIM execution-overhead removal, shared-form equivalence
checking, process-reward RTL synthesis, concurrent DRAM-PIM access, redundancy-free
RTL simulation, timing-driven true-3D placement, drift-compensated RRAM CIM,
Rowhammer attacks on PLONK, and end-to-end DNN accelerator generation. They further
support the interpretation that the field is moving toward explicit co-design of
verification, memory behavior, physical constraints, and deployment security.

1. Recover and adjudicate more primary/full-text records, especially the pending
   ISCA and ICCAD queues and the remaining DAC corpus.
2. Obtain comparable historical editions with equivalent collection and coding
   rules; current title-shift results are exploratory metadata only.
3. Run independent adversarial LLM or human review. The current deterministic
   preflight checks schema, provenance, taxonomy validity, and vocabulary overlap;
   it is not an independent semantic judge.
4. Extract full-paper conditions for headline metrics: workload, baseline,
   hardware/process, accuracy, energy, area, runtime, and uncertainty.
5. Add negative, failed, and inaccessible evidence to the same ledger so that
   discoverability does not become a hidden selection bias.

Until then, this report is a defensible capability map and research-reading guide,
not a forecast.
The latest eight cases broaden the map with computation-data-decoupled NPU dataflow,
knowledge-aggregated GPU power modeling, compiler-IR energy prediction, erasure-coded
LLM prefix caches, factored floating-point systolic MACs, Hamiltonian-guided VQA
initialization, GNN-assisted multi-die FPGA floorplanning, and stratified MoE expert
scheduling. The recurring direction is explicit coordination of compiler, memory,
power, and physical constraints across the stack.

The newest ten DAC cases sharpen that direction: flow-matching and analytic
timing-driven placement push learned and closed-form optimization into physical
design; SpArC and PD-Swap make compiler scheduling and FPGA reconfiguration
phase-aware; Maple, NVLLM, and Hiband treat data movement, 3D NAND, and DRAM
bandwidth as primary LLM design variables; RM-CIMA moves robust edge control
into analog CIM; and Netdetox/Securerouter expose an arms race around secure
inference and adversarial hardware-security models. This is a thematic signal
from selected official descriptions, not a prevalence or directional claim.

The following twelve cases deepen three thinner branches of the map. Chiplet
work couples phase-specific LLM packaging, exponent coding, timing-aware 2.5D
planning, and surrogate exploration; analog work combines standard-cell AMS
automation, hypergraph representation learning, and differentiable or tree
search placement; verification work turns RL and generative models into HDL and
RISC-V test generators; and quantum work targets shallow syndrome extraction.
Together they reinforce a cross-layer shift toward learned search plus explicit
physical, communication, and verification constraints, while remaining
description-level evidence rather than a field-wide trend estimate.

The next batch extends the map into thermal and reliability-aware design,
quantum control and error mitigation, sparse robotics inference, VLA control,
and verification-oriented RTL generation. Across these cases, efficiency is
increasingly defined as a closed-loop property: thermal headroom, syndrome
bandwidth, control latency, readout noise, and testbench feedback are treated as
part of the algorithm/architecture contract. These are selected-paper themes,
not evidence that the whole field has shifted uniformly.

This batch adds a complementary deployment layer: encrypted and zero-knowledge
inference, MoE quantization/caching/speculation, dynamic-shape tuning, edge VLM
pipelines, sparse tensor code generation, near-memory macros, wafer-scale
networks, and selective edge encryption. The common theme is movement of policy
into runtime and data-movement decisions—expert choice, cache residency,
bootstrapping, precision, and protection are co-optimized with compute. These
are selected-paper signals, not a venue-wide forecast.

The latest cases add a verification-and-trust layer: balanced emulation and
parallel equivalence checking, LLM-assisted processor debugging and assertion
generation, graph-aware circuit simulation, FIT prediction, CIM signing,
traffic shaping, and ZNS-aware graph execution. Alongside new accelerator
dataflows, these suggest that practical gains increasingly depend on orchestration
and assurance around the compute kernel—not only on the kernel itself. This is
still a selected, official-description evidence signal rather than a prevalence
claim.

The newest cases extend the evidence into analog/RF design, manufacturing
inspection, safe neural control, agentic testbench generation, 3D placement,
power prediction, and reliability-aware CIM. A common pattern is co-optimization
of a learned or approximate method with a hard engineering contract—physical
constraints, safety probability, signoff power, process variation, or test
coverage. This is a selected-paper signal and does not establish venue-wide
prevalence.

This batch adds graph-centric and heterogeneous-system themes: dynamic-graph
PIM, path-aware timing prediction, hypergraph resistance and partitioning,
spiking multi-task agents, ternary/Bayesian inference, graph diffusion across
RTL and netlists, in-storage analytics, optical privacy encoding, and CPU/GPU/
NDP co-execution. The repeated direction is adaptive movement of data and
control across irregular structures, with assurance and calibration becoming
part of the architecture rather than post hoc checks.

This increment adds testability, leakage, approximate arithmetic, in-storage
analytics, learned graph storage, runtime model selection, low-power test, and
3D FPGA placement. The pattern is consistent with a field optimizing not only
steady-state throughput, but also observability, attack surface, variation,
update behavior, and deployment-time adaptation. It remains evidence from a
selected coded subset, not a complete venue-wide forecast.

This batch adds a runtime-and-assurance layer: hypergraph partitioning, adaptive
GPU and PIM dataflows, ternary and neuro-symbolic inference, MoE co-execution,
edge fine-tuning, disaggregated-memory replication, and graph-based IP
protection. The recurring design question is no longer just how to compute a
kernel, but how to schedule, cache, protect, and verify it under changing
system conditions. This remains a selected-paper signal, not a venue-wide trend
claim.
