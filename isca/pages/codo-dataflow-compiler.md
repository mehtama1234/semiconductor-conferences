# CODO: automated dataflow-compilation as an ISCA 2026 direction

## What the paper addresses

CODO targets a recurring bottleneck in FPGA accelerator construction: high-level
synthesis makes hardware generation more accessible, but large streaming
designs still require difficult manual choices about legal dataflow, movement
between memory levels, and scheduling under resource limits. The paper frames
these as coupled compiler problems rather than isolated kernel optimizations.

## Technical mechanism

The reported compiler detects both coarse-grained and fine-grained dataflow
violations, repairs the resulting streams, optimizes on-chip and off-chip data
movement, and automatically schedules the generated accelerator. Its artifact
is described as an MLIR-based implementation with examples and experiment
scripts. The primary evidence is the [author preprint](https://arxiv.org/abs/2604.12618)
and the associated [public artifact](https://github.com/sjtu-zhao-lab/codo-artifact).

## Evidence-backed results

The preprint reports 1.45x–4.52x latency speedups on computation kernels and
3.7x–33.8x speedups on DNN models relative to state-of-the-art frameworks. In
on-board evaluation it reports 7.3x average speedup on CNN models and 2.07x on
GPT-2. These are reported paper results, not repository reproductions.

## Taxonomy

- Theme: design methodology and tooling
- Subtheme: high-level synthesis and compilers
- Sub-subtheme: MLIR two-level dataflow accelerator generation

## Limits and adversarial questions

The public evidence does not by itself show how the compiler behaves across
FPGA families, larger application graphs, different HLS tool versions, or ASIC
flows. The headline speedups also need baseline identity, absolute latency,
resource utilization, synthesis-time, and quality-of-result tables before they
can support a broader claim about compiler superiority. A primary-paper or
artifact-reproduction review should verify those conditions.
