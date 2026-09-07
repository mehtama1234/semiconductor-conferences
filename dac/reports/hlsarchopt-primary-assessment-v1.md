# HLSArchOpt partial-artifact assessment — 2026-09-06

The [author faculty page](https://csee.hnu.edu.cn/people/hexu) links this exact
paper to [HLSArchOpt at the inspected commit](https://github.com/Szzer1/HLSArchOpt/tree/999043ab132f984b5b88b26ab9e415221e1198f1).
The release supplies a Fire-module example, not a demonstrated full optimization
workflow. README lists Vivado/HLS 2019.2, ZCU102 and a 100 MHz target.

Selected source inspection shows a dataflow pipeline with squeeze and parallel
expand branches. The HLS script selects a 10 ns clock and enables synthesis/export,
but comments out C simulation and co-simulation. This is not evidence that the
authors never tested correctness; it means this script does not reproduce those
checks. No code was executed in this assessment.

The [official description](https://63dac.conference-program.com/presentation/?id=RESEARCH1110&sess=sess173)
does not supply enough conditions to reconstruct the reported average gain.
Do not extrapolate this example's platform to all benchmarks or treat its release
as replication. Full-model coverage, LLM prompts/budgets, functional tests,
resource limits and measurement modality remain unresolved.

The [structured assessment](../data/hlsarchopt-primary-assessment-v1.json)
pins the tree and inspected paths. Review remains pending; numerical synthesis
is withheld until comparable benchmark conditions are available.
