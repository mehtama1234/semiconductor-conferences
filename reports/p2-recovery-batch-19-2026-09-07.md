# P2 recovery routing batch 19 — 2026-09-07

This tranche routes ten ISCA records across GPU/FHE memory optimization,
ray-tracing and Gaussian-splatting accelerators, instruction/memory prefetching,
speculative translation, and quantum compilation/layout.

| Priority | Paper ID | Title | Evidence needed before quantitative use |
|---:|---|---|---|
| 1 | `isca-2026-program-125` | MNEMOS: A GPU-based TFHE Acceleration Framework with Memory Access Optimization | TFHE parameters/circuits, GPU model, memory layout, bootstrapping workload, correctness, latency/energy, and baseline |
| 2 | `isca-2026-program-126` | GauTracer: Extending Ray Tracing Accelerator for Gaussian-based Scene Representation | Scene/dataset suite, Gaussian representation, RT hardware changes, image quality, rays/s, power, and RT baseline |
| 3 | `isca-2026-program-127` | TTP: A Hardware-Efficient Design for Precise Prefetching in Ray Tracing | Ray-tracing workloads, locality predictor, metadata/storage, coverage/accuracy, bandwidth/latency, and prefetch baseline |
| 4 | `isca-2026-program-128` | Optimizing 3D Gaussian Splatting with Axis-Shared Rasterization and Order-independent Transmittance | Scenes, quality metric, rasterization assumptions, hardware/software target, frame rate/energy, and standard splatting baseline |
| 5 | `isca-2026-program-129` | Bumper: Hinting Instruction Usefulness for Robust Unified Caches | ISA/cache hierarchy, hint semantics, workloads, hit/miss/MPKI, area/energy, and replacement-policy baseline |
| 6 | `isca-2026-program-130` | ICP: Exploiting Instruction Correlation for Prefetching Irregular Memory Accesses | CPU/cache, irregular workload suite, correlation detector, storage/accuracy, latency/bandwidth, and prefetch baselines |
| 7 | `isca-2026-program-131` | Revelator: Rapid Data Fetching via OS-Guided Hash-based Speculative Address Translation | OS/MMU/translation model, hash structure, workloads, mis-speculation/recovery, latency/area, and conventional translation baseline |
| 8 | `isca-2026-program-132` | Distilling Magic States in the Bicycle Architecture | Code/architecture, distillation protocol, physical-error model, resource counts, fidelity/throughput, and prior distillation baseline |
| 9 | `isca-2026-program-133` | O3LS: Optimizing Lattice Surgery via Automatic Layout Searching and Loose Scheduling | Quantum circuits, layout/search space, scheduling constraints, code/noise model, qubit/time/resource metrics, and compiler baseline |
| 10 | `isca-2026-program-134` | Leveraging Phase Polynomials for Quantum Circuit Optimization | Circuit suite, phase-polynomial transformation, gate/error model, correctness, depth/count/runtime, and optimizer baseline |

These are source-recovery priorities and condition checklists, not technical
rankings or temporal trend evidence.
