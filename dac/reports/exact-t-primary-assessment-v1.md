# Exact T Library primary assessment — 2026-09-06

The [version-pinned preprint](https://arxiv.org/html/2605.15476v1) matches the
program title and all four authors. [Structured assessment](../data/exact-t-primary-assessment-v1.json)
records experimental conditions and the unresolved description/preprint metric
difference. Original description evidence is preserved, not overwritten.

The synthesis may retain this as a provisional resource-specific mapping case,
not an accepted numerical headline or evidence of learned search. Neither local
library optimality nor software tests establish globally optimal circuits.

## Figure and artifact follow-up

Visual inspection of [PDF page 6](https://arxiv.org/pdf/2605.15476v1#page=6)
separates the mapper variants and records a modeled space-time counterexample
in the structured assessment. Nearby prose and chart attribution differ; the
figure check does not resolve the conference-description discrepancy.

The [pinned repository](https://github.com/Nozidoali/exact-t-map/tree/60297d3dd25a0c1f3eec31a28b4df7535f44aa41)
contains implementation and benchmark files. Its verification script requires
Slurm despite the README's local-looking invocation. Inspection also shows that
the simulator does not test relative phases between basis states, leaving a
coherent-oracle correctness gap. These are same-agent observations, not an
independent verdict. Next: reconcile source claims and check both functional and
phase correctness before attempting accepted benchmark reproduction.

The pinned revision compiled with GNU C++ 11.4.0/CMake 3.22.1 on Linux x86_64.
The README's small `maj3` example exited successfully and emitted QASM; commands,
header and output checksum are recorded in the assessment. This proves build and
emission only. No simulator, equivalence check or paper benchmark was run.
