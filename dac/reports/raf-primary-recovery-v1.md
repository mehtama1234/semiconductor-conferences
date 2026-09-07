# RAF communication-bound assessment — 2026-09-06

The [official description](https://63dac.conference-program.com/presentation/?id=RESEARCH1113&sess=sess116)
matches the program title and seven authors. It separates remote-access removal
from local-access minimization, first within operators and then between them.
That distinction matters: remote-access-free does not mean zero data movement.

The description explicitly pairs results with baselines in order:

| Baseline | Reported energy reduction | Reported speedup |
|---|---:|---:|
| IANUS | 50.4% | 3.98× |
| H^2LLM | 39.0% | 1.72× |
| OptiPIM | 37.8% | 1.57× |

This resolves baseline attribution, not workload conditions. The communication
cost definition, allowed operations, topology, capacities and proof assumptions
are absent. Consequently, claimed communication bounds cannot be independently
verified from the description or generalized to energy/latency optimality.

No exact full paper or artifact was recovered in the recorded searches.
The [structured assessment](../data/raf-primary-recovery-v1.json) preserves
these limits and missing evaluation conditions; numerical synthesis and
independent acceptance remain pending.
