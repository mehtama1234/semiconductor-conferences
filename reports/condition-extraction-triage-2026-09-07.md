# Triage condition extraction — 2026-09-07

This note upgrades the Triage ISCA 2026 route from an abstract-only lead to a
source-located evaluation record. It does not constitute independent review or
acceptance.

## Evidence and setup

- **Primary source:** author preprint, [arXiv:2605.04459](https://arxiv.org/abs/2605.04459),
  sections IV–V (15-page PDF captured 2026-09-07).
- **System modeled:** a classical control pipeline in which a compiler emits
  low-level instructions, a static analyzer builds an annotated timeline, and a
  discrete-event simulator schedules syndrome decoding on arrivals and task
  completions (Section IV).
- **Decoder model:** PyMatching profiling fit to `t_decode = A·volume^alpha`,
  with `alpha = 1.17`; task volume is tied to window-buffer size and unresolved
  constraint-graph degree. Pattern-dependent variation is separately modeled as
  calibrated heavy-tail jitter (Section IV).
- **Noise and code:** rotated surface code, distance 9 simulation with
  circuit-level depolarizing noise `p = 3×10^-3`, then logical-error-rate
  extrapolation to distance 21. Stim Monte Carlo uses at least `10^5` runs per
  point (Section IV).
- **Benchmark suite:** 15 QASMBench-derived FTQC workloads spanning state
  injection, rotation, magic-state distillation, Bell preparation, arithmetic,
  variational, QFT, Trotterization, and Ising circuits; both Compact Layout and
  Standard Layout variants are included where applicable.
- **Baselines:** serial sliding-window, time-parallel window, FIFO
  time-space-parallel, and SWIPER with 10% misprediction and 10% speculation
  time. The comparison metrics are inserted idle layers and aggregate logical
  error rate.
- **Fixed controls:** heuristic weights `w_u = w_c = 0.5`, trigger replan scope
  threshold `0.3`, and minimum planning interval `2` (Section V).
- **Representative regimes:** Bell4 sweeps decoder count and relative decoder
  speed; the benchmark-wide comparison uses a parallelism-rich regime
  (decoder count `2×` logical qubits, speed `0.9`) and a latency-rich regime
  (count `1×` logical qubits, speed `1.8`).

## What the paper supports

Within this simulation, Triage reports a **52.6% average logical-error-rate
reduction versus the time-parallel baseline** across the listed benchmark suite.
The paper also reports that Triage occupies the resource-constrained frontier,
while SWIPER can win when decoder resources are abundant. These are author
simulation results under the conditions above, not silicon measurements,
independent replications, or a field-level trend.

## Remaining gaps

The preprint does not yet provide an independently reproduced run, released
trace bundle, matched per-benchmark confidence intervals, or a demonstrated
hardware decoder implementation. The distance-21 result is an extrapolation,
and the cross-decoder latency law and heavy-tail calibration require sensitivity
checks before generalizing beyond this simulator. Keep the result provisional
until those checks and adversarial review are complete.

## Thematic interpretation

Triage is a concrete instance of a broader cross-layer theme already visible in
the corpus: resource availability and scheduling policy are treated as part of
correctness (here, avoiding causal-cone backlog and inserted idle layers), not
as a post-hoc optimization. It strengthens the mechanism-level synthesis, but
does not establish temporal growth or prevalence.
