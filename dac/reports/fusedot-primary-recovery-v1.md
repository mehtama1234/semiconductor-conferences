# FuseDot evidence-depth assessment — 2026-09-06

The [official description](https://63dac.conference-program.com/presentation/?id=RESEARCH1182&sess=sess156)
and [first-author page](https://wenjuzhao.github.io/) match title and nine authors.
Checked author pages and the five-entry public repository metadata listing did
not yield a full paper or implementation. This is bounded non-recovery, not
proof of inaccessibility.

FuseDot groups repeated-weight multiplication work and introduces reordering and
multiplier sharing. The key unresolved question is the net cost under actual
quantization and workload conditions. As a researcher inference, equal integer
codes need not represent equal effective weights across differently scaled
groups. Full-paper legality rules and finite-precision accuracy checks are needed.
Weight repetition, index/reordering overhead and contention also need accounting.

Keep reported energy-efficiency factors separate from energy-reduction
percentages. The description does not identify the baseline accelerators or
pair each range endpoint with a model/configuration. Numerical synthesis remains
withheld. The author page mentions an award. It is from a HUST annual conference, not DAC, and it is not an independent review of this assessment.

The [structured recovery record](../data/fusedot-primary-recovery-v1.json)
lists attempts, interpretation limits and revisit conditions. Review is pending.
