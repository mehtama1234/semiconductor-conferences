# Semiconductor technology direction synthesis — v1 provisional

This is the root-level synthesis of the current ISCA, DAC, and ICCAD workspaces.
It asks what detailed capabilities are appearing across the selected evidence,
how the conferences complement one another, and what is required before calling
any direction a measured trend.

The machine-readable evidence map is [`data/technology-direction-evidence-v1.json`](../data/technology-direction-evidence-v1.json).

The evidence is intentionally asymmetric:

- DAC: 543 official 2026 research descriptions; 49 adjudicated records.
- ISCA: 173 official 2026 program records; 15 primary, institutional-abstract,
  or company-source-backed adjudications; 5 secondary-only papers pending primary verification.
- ICCAD: 2026 scope evidence and a 276-record 2025 fallback inventory; 8 primary
  or author-PDF-backed fallback adjudications.

The 72-record adjudication sample is selected for recoverable evidence and
technical diversity. It is not a prevalence estimate, market forecast, conference
ranking, or proof that a direction is rising.

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

## Direction 1 — Tool-grounded AI for design and verification

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

### Interpretation and limit

The evidence supports earlier coupling of thermal, packaging, bandwidth, and
workload decisions. It does not establish manufacturing readiness, a winning
packaging technology, or generalization beyond the evaluated geometry, materials,
devices, and workloads.

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

For the exact-T example, consult the [primary assessment](../dac/reports/exact-t-primary-assessment-v1.md):
the description and preprint disagree on the maximum reduction. Keep that
numerical headline withheld; the resource-specific mapping mechanism remains a
provisional example, not evidence of learned search or global circuit optimality.
Its figure-level counterexample also prevents a uniform space-time-benefit claim;
available artifact checks do not yet establish coherent-oracle correctness.

## Direction 6 — Specialized accelerators encode workload structure

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
| DAC 2026 | Breadth of design-flow, accelerator, physical-design, memory, and reliability descriptions | Mostly official descriptions; selected 49 are not full-corpus prevalence |
| ISCA 2026 | Deep primary and industry-source cases for system architecture, LLM execution, memory, PIM, ECC, CXL, integrated networking, and thermal behavior | 15 primary/institutional/company records plus 5 unresolved secondary queue items; full program remains mostly metadata |
| ICCAD 2025 fallback | Design automation, verification, chiplet, analog, security, and emerging-device depth | 2026 paper corpus unavailable; 2025 evidence cannot establish 2026 change |

The conferences should therefore be read as complementary instruments: DAC gives
breadth across the design stack, ISCA gives system/architecture mechanisms, and
ICCAD gives design-flow and physical-design depth. Combining raw counts would
discard the evidence asymmetry.

## What must happen before a final trend claim

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
