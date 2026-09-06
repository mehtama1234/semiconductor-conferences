# DAC 2026: evidence-backed AI-for-design and accelerator batch

This page analyzes eight DAC 2026 research manuscripts whose official program
pages expose substantive descriptions. It is a bounded adjudication batch, not a
claim about the full DAC distribution. The machine-readable records are in
`dac/data/adjudicated-2026-batch.jsonl`; raw page captures are locally produced
by `scripts/collect_dac_paper_evidence.py` and are excluded from Git by the raw
data policy.

## What these eight records show

The batch contains several distinct technical moves:

1. **Replace an expensive EDA kernel with specialized parallel execution.**
   Warp-STAR targets GPU static timing analysis and reports speedups in both the
   timing-analysis kernel and a timing-driven placement flow.
2. **Use learned models to express design intent.** ModuPlace applies LLM
   fine-tuning and preference optimization to modular PCB placement, making user
   constraints part of the placement representation.
3. **Exploit physical signals to reduce characterization cost.** Powerpath uses
   supply-current signatures and statistical calibration to reduce sequential
   constraint search without extra SPICE simulations.
4. **Make the objective exact where proxy objectives fail.** The quantum-synthesis
   paper replaces AND-count proxy optimization with exact T-cost reasoning under
   Clifford equivalence.
5. **Co-design graph algorithms and hardware.** TDH-GNN and HDGAS both reduce
   graph-learning cost through algorithm/architecture specialization, but they
   target different graph structure and sparsity mechanisms.
6. **Put reliability into the system stack.** Strix treats NPU reliability as a
   microarchitecture/ISA/programming problem, while GEMIR treats power integrity
   as a coupled, physics-constrained prediction problem.

## Theme map

| Theme | Subtheme | Records |
|---|---|---|
| Physical design and manufacturing | Timing analysis and optimization | Warp-STAR, Powerpath |
| AI-assisted EDA | LLM-assisted design flows | ModuPlace |
| Design methodology and tooling | Synthesis and compilation | Exact T synthesis |
| Architecture and accelerators | Specialized AI accelerators | TDH-GNN, HDGAS |
| Power, reliability and security | Accelerator reliability | Strix |
| Power, reliability and security | Power integrity and reliability | GEMIR |

## Limits and next adjudication step

The official descriptions provide evidence for each record’s stated problem,
method, evaluation context, and selected metrics. They do not provide complete
benchmark tables, all baselines, resource costs, accuracy/quality tradeoffs, or
generalization boundaries. The next pass must verify these fields against the
paper or an authorized full-text copy before using the records for conference-wide
comparisons.
