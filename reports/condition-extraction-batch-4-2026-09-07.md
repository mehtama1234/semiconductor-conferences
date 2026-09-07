# Condition extraction batch 4 — 2026-09-07

This fourth P1 batch adds five ISCA preprint-backed records. The source pages
preserve the reported setup and the limits on generalization; no metric is
treated as independently accepted.

| Paper | Source and locator | Conditions extracted | Boundary retained |
|---|---|---|---|
| ISCA COSM | [primary evidence page](../isca/pages/primary-evidence-batch-2026-2.md), linked preprint | Mobile CPU/PIM shared-memory setting; concurrent LLM, mobile-application, and compute-kernel workloads; idleness-aware insertion into CPU access windows; author-reported up to 2.8× PIM throughput and <2.0% CPU loss | Energy, SoC diversity, scheduler parity, and full platform tables remain unresolved |
| ISCA Cerberus | [primary evidence page](../isca/pages/primary-evidence-batch-2026-2.md), linked preprint | HBM-oriented dense DRAM; clustered/peripheral fault emphasis; Encode-Once/Decode-Many organization across on-die, link, and system ECC; decoder ordering and correction budget | Fault probabilities, decoder latency, exact HBM configuration, and overhead are not yet extracted |
| ISCA Cassandra | [primary evidence page](../isca/pages/primary-evidence-batch-2026-3.md), linked preprint | Llama 3 8B on NVIDIA RTX 4090; low-batch edge reasoning decode; draft representation, KV-cache pruning/truncation, full-precision verification, and representation conversion; reported 2.41× over BF16 and 1.81× tokens over Eagle-3 at the same memory budget | Accuracy/acceptance behavior, broad reasoning benchmarks, conversion-unit area/energy, and full memory-budget tables remain open |
| ISCA PuDGhost | [primary evidence page](../isca/pages/primary-evidence-batch-2026-4.md), linked preprint | 96 real DDR4 chips from 12 modules; random-input interference experiments; adjacent-row and concurrent-column interference; screening and dedicated compute-row layout countermeasures; reported output impacts up to 10% and 48% | DRAM-generation transfer, screening overhead, capacity loss, environmental sweeps, and end-to-end workloads remain unresolved |
| ISCA PLENA | [primary evidence page](../isca/pages/primary-evidence-batch-2026-6.md), linked preprint | Long-context web/computer-use agent workloads; asymmetric quantization, flattened systolic array with FlashAttention, custom ISA/compiler, cycle-emulated simulator, and design-space exploration; reported 8.5× utilization, 2.24× A100 throughput, and 3.85× TPU v6e throughput under matched multiplier/memory settings | Simulation rather than silicon; area, energy, context distributions, simulator validation, and artifact status remain unresolved |

## Next extraction action

Finish the remaining P1 records that are currently institutional, company, or
artifact-only, then begin a second pass over the 541 official-description
records for manuscript recovery and condition upgrades.
