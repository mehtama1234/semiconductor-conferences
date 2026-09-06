# ICCAD 2025 fallback: three additional evidence-backed directions

These papers are part of the explicitly labeled 2025 fallback corpus for the
2026 ICCAD target. They provide technical evidence about the prior edition;
they do not establish what ICCAD 2026 will contain.

## Robust analog sizing under variation — RSizing

RSizing treats analog sizing as a multi-objective robust-optimization problem
under process variation. Its three-phase flow prunes regions using nominal
optimization, models non-uniform variation with heteroscedastic Gaussian
processes, explores with Thompson sampling, and refines with targeted Monte
Carlo simulation and calibration. The author-hosted paper reports three
benchmark circuits, yield-constrained designs, and lower computational cost,
but the repository has not extracted the numerical tables or all technology
assumptions.

Source: [author-hosted paper](https://www.cse.cuhk.edu.hk/~byu/papers/C287-ICCAD2025-RSizing.pdf).

## LLM-for-EDA with reinforcement learning — VERIRL

VERIRL builds Veribench-53K from more than 700K Verilog problems and uses
Trace-back based Rescore to improve sparse/noisy rewards. Sample-balanced
weighting is intended to limit catastrophic forgetting and overfitting during
RL fine-tuning; policy and reward models co-evolve. The preprint reports gains
in test-pass rate, functional correctness, and compilation robustness and
releases an artifact. Exact benchmark splits, leakage controls, reward
validity, and hardware cost remain review requirements.

Sources: [preprint](https://arxiv.org/abs/2508.18462), [artifact](https://github.com/omniAI-Lab/VeriRL).

## Thermal-aware 3D stacking — Tasa

Tasa combines heterogeneous high-performance and high-efficiency cores,
cross-stack thermal optimization, and bandwidth-sharing scheduling for LLM
inference on 3D-stacked memory architectures. Its preprint reports peak
temperature reductions of 5.55, 9.37, and 7.91 degrees Celsius for 48, 60,
and 72 core configurations, plus 2.85x Llama-65B and 2.21x GPT-3 66B speedups
over the stated GPU and heterogeneous-PIM baselines. The result is relevant to
the packaging/architecture boundary, but thermal calibration, area/cost, and
cooling assumptions require full-paper verification.

Source: [preprint](https://arxiv.org/abs/2508.07252).

## Evidence-derived interpretation

The three papers suggest a broad ICCAD direction in which design automation is
increasingly coupled to physical uncertainty and system-level behavior:

- Bayesian optimization incorporates process variation into analog sizing.
- Reinforcement learning incorporates execution feedback into HDL generation.
- 3D architecture exploration incorporates thermal gradients and bandwidth
  sharing into the architecture decision.

This is a cross-paper interpretation, not a conference-wide ranking. The
fallback edition is incomplete at the technical-evidence level, and these
papers cannot be used to infer market adoption or future ICCAD 2026 acceptance
patterns.
