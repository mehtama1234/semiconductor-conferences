# Evidence-derived taxonomy and coding guide v1

This guide turns the taxonomy IDs in `data/taxonomy-v1-evidence.json` into
operational coding rules. It is derived from the 66 adjudicated records across
DAC 2026, ICCAD 2025 fallback, and ISCA 2026. It is provisional until the
remaining corpora are adjudicated.

## Coding unit and evidence ladder

The unit is one paper, not one keyword or one presentation session. Every
adjudicated row must answer: what technical problem is being solved, what
mechanism/artifact is proposed, what workload or design corpus is evaluated,
what hardware/process assumptions apply, what baselines are used, which metrics
are reported, and what the evidence cannot establish.

Evidence strength is recorded separately from taxonomy confidence:

1. `metadata_only` — title, author, session, DOI, or CFP scope. Discovery only;
   no technical classification.
2. `secondary_excerpt` — indexed summary or abstract not yet verified against a
   primary/authorized source. May create a review hypothesis, never a final
   trend claim.
3. `medium_official_description` — official conference description contains a
   substantive problem/mechanism/result summary, but not the full paper tables.
4. `high_primary_preprint` or `high_primary_author_pdf` — author preprint/PDF
   supports the technical fields. Numerical claims still require limits and
   should not be treated as independently reproduced.

The deepest label is earned only when the mechanism—not merely the application
area—distinguishes the paper. For example, “LLM” is a workload; “row-aligned
sparse-attention PIM” is a sub-subskill.

## Theme boundary rules

### AI-assisted EDA

Use when learning or generative models change a design-automation activity:
placement, HLS, verification, synthesis, mapping, or code generation. Do not
use for an ordinary AI accelerator unless the paper changes the design flow.

Observed sub-subskills:

- `preference-optimized-pcb-placement` — learned constraint-graph generation
  expresses user preferences in modular PCB placement; require placement
  objective and preference mechanism.
- `llm-generated-hls-architecture-optimization` — an LLM generates or changes
  synthesizable dataflow architecture; require synthesis success and hardware
  evaluation, not just generated code.
- `llm-global-reasoning-for-hls-dse` — an LLM navigates HLS directives as a
  Pareto/search controller; require search budget and Pareto-quality evidence.
- `llm-evolution-of-technology-mapping` — an agent evolves core mapping code,
  not merely scripts or prompts; require code-validity and regression checks.
- `reinforcement-learning-verilog-generation` — RL uses compilation/simulation
  feedback to generate HDL; require reward signal, testbench, and functional
  correctness evidence.

### Architecture and accelerators

Use when the primary contribution changes hardware organization, execution,
memory placement, or architecture/software coordination. Keep EDA tooling in
AI-assisted EDA or design methodology when the artifact is the design flow.

Observed sub-subskills:

- `ai-accelerator-microarchitecture` family — datapath, buffering, PIM, or
  quantization hardware whose objective is AI execution. Distinguish the
  specific mechanism below rather than collapsing every paper to “AI chip.”
- `gigabyte-embedded-dram-kv-cache-buffering` — large on-chip eDRAM buffers,
  KV-priority mapping, and eviction co-designed for LLM serving.
- `asynchronous-pim-speculative-decoding` — draft/verify model decoupling across
  PIM and NPU with adaptive scheduling and acceptance-aware control.
- `outlier-aware-lut-quantized-gemm` — non-uniform dual-side quantization,
  LUT-based GEMM, and explicit outlier detection/compensation.
- `architecture-software-co-design` family — hardware and software/runtime
  decisions are jointly optimized. Observed mechanisms include
  `kl-guided-moe-pruning-and-restoration`,
  `generative-sequential-cpu-design-space-exploration`,
  `silicon-calibrated-hierarchical-cim-exploration`, and
  `moe-data-movement-forecasting-and-placement`.
- `specialized-ai-accelerators` family — accelerator organization specialized
  to a non-generic model/data structure. Observed mechanisms include
  topology-driven heterogeneous GNN acceleration, adaptive-sparsity
  hyper-dimensional graph learning, tensor-core 3D Gaussian splatting, and
  sort-free Gaussian-splatting acceleration.

### Chiplets, 3D integration, and packaging

Use when package/interposer/stack organization or physical integration is a
first-order design variable. Do not infer manufacturing readiness from a
thermal or simulation result.

Observed sub-subskills:

- `analytical-3d-ic-thermal-simulation` — analytical acceleration of 3D-IC
  thermal evaluation.
- `modular-reduced-order-chiplet-thermal-modeling` — reusable reduced-order
  thermal modules with interface-port coupling for chiplet scenarios.
- `thermal-aware-3d-stacked-llm-inference` — heterogeneous 3D-stacked compute,
  thermal balancing, and bandwidth scheduling for LLM inference.
- `metal-density-constrained-package-power-plane-synthesis` — package power
  plane synthesis under metal-density and integrity constraints.

### Design methodology and tooling

Use for compilers, synthesis, search, and reproducibility artifacts where the
design flow—not the target application—is the contribution.

Observed sub-subskills:

- `mlir-two-level-dataflow-accelerator-generation` — compiler-level repair and
  optimization of coarse/fine dataflow plus scheduling for generated FPGA
  accelerators.
- `differentiable-task-graph-partitioning` — differentiable partition decisions
  over task graphs with explicit communication/cut constraints.
- `zero-shot-reinforcement-learning-for-logic-optimization` — zero-shot RL
  policy transfer for logic optimization without per-design retraining.
- `exact-t-cost-quantum-circuit-synthesis` — exact synthesis minimizing a
  T-cost or equivalent quantum resource objective.

### Memory, interconnect, and storage

Use when data placement, communication, persistence, or memory hierarchy is the
technical bottleneck. Require a stated movement/locality mechanism, not merely
an accelerator with memory attached.

Observed sub-subskills:

- `near-memory-communication-lower-bounds` — theoretical or measured bounds on
  communication close to memory.
- `cxl-near-memory-ann-search` — CXL/near-memory placement for approximate
  nearest-neighbor search.
- `disaggregated-compute-network-storage-training` — separate compute, network,
  and optimizer-state storage planes for distributed LLM training.
- `os-hardware-cxl-tiered-memory` — OS/hardware coordination for CXL tiering.
- `row-aligned-sparse-attention-pim` — DRAM-row alignment and activation-aware
  scheduling for sparse attention without cache rewrites.

### Physical design and manufacturing

Use for placement, timing, clocking, DRC, process-aware sizing, and layout
constraints. Distinguish physical-design optimization from thermal/reliability
analysis when the latter is the main contribution.

Observed sub-subskills:

- `fpga-accelerated-design-rule-checking` — layout partitioning and sparse
  writeback mapped to FPGA DRC execution.
- `differentiable-clock-tree-synthesis` — continuous probabilistic modeling of
  discrete CTS topology and buffer sizing.
- `robust-bayesian-analog-sizing` — process-variation-aware analog sizing with
  heteroscedastic surrogates and Monte Carlo refinement.
- `gpu-accelerated-static-timing-analysis` — warp-level orchestration for
  irregular-graph STA and timing-driven placement.
- `statistical-sequential-constraint-characterization` — calibrated current or
  statistical models that reduce sequential signoff characterization cost.

### Power, reliability, and security

Keep energy/thermal efficiency, fault tolerance, integrity, and security as
separate subthemes even when a paper crosses them. A security claim requires a
threat model; a reliability claim requires a fault/variation model.

Observed sub-subskills:

- `full-stack-npu-fault-mitigation` and
  `fault-tolerant-block-floating-point-npu` — cross-layer or arithmetic-level
  detection/recovery for NPU faults.
- `ml-early-thermal-placement-optimization` — learned early power/temperature
  prediction coupled to placement changes.
- `thermal-imbalance-concurrent-gpu-execution` — thermal stragglers coupled to
  overlapped multi-GPU execution and power management.
- `physics-informed-joint-em-ir-modeling` — physics-informed joint
  electromigration/IR-drop modeling.
- `remote-power-leakage-in-post-quantum-kem` — remotely observed power leakage
  used to recover ML-KEM secrets on a real processor.
- `diffusion-model-watermarking-acceleration`,
  `adversarial-attacks-on-moe-offloading`, and
  `gpu-power-thermal-transformer-side-channel-leakage` — distinct attack or
  defense mechanisms that must retain their threat models and attack surfaces.

### Verification and validation

Use for formal properties, simulation/emulation, test generation, and bug
finding. Generated assertions are not equivalent to proven properties unless
the evidence says so.

Observed sub-subskills:

- `hierarchical-learning-for-sequential-formal-analysis` — learned hierarchy
  for sequential formal reasoning or analysis.
- `structure-guided-llm-sva-generation` — AST-fingerprint retrieval guiding
  SystemVerilog Assertion generation.
- `llm-assisted-hls-logic-debugging` — dataset/model pipeline for locating,
  classifying, and correcting HLS logic bugs.

## Adjudication boundary tests

For every row, the reviewer must answer “yes” to all applicable questions:

- Does the evidence explicitly support the selected mechanism, rather than only
  the title or application?
- Could the paper be assigned to a neighboring sub-subtheme? If yes, record the
  alternative and why the selected mechanism is more specific.
- Are every numerical metric and baseline present in the cited evidence?
- Is the workload/design corpus named, and are hardware/process assumptions
  separated from observed results?
- Does the limits field identify what is missing, rather than merely saying
  “more work is needed”?
- Is the confidence level consistent with source type and not with the reviewer’s
  enthusiasm?

The current deterministic preflight checks schema, taxonomy validity, URL
provenance, and evidence vocabulary. It does not answer these semantic
questions; the adversarial protocol below is still required.
