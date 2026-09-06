# DAC initial paper analysis

Status: **provisional seed analysis**. This report covers three normalized records, not the DAC corpus. It is useful for designing the coding scheme, not for ranking DAC themes.

## Paper-level observations

### LLMs and digital design automation

The paper treats LLMs as a possible interface and automation layer for silicon-design tasks. The important analytical distinction is between naming a possible application and demonstrating a reliable design flow. The next extraction must record which tasks have executable artifacts, quantitative baselines, or only qualitative readiness discussion.

- Theme: AI-assisted EDA
- Subtheme: LLM-assisted design flows
- Sub-subtheme: language models for silicon tasks
- Key question: where do language models provide useful design representations, and where do they fail to preserve correctness constraints?

### EVA

EVA moves beyond textual assistance toward generative analog-circuit topology discovery. Its interesting substructure is the combination of a generative model, circuit-validity constraints, and preference optimization. The analysis must separate topology validity, novelty, electrical performance, and search efficiency rather than collapsing them into one “AI-designed circuit” claim.

- Theme: AI-assisted EDA
- Subtheme: generative circuit and layout synthesis
- Sub-subtheme: PPO/DPO for circuit search
- Key question: can generative search produce novel circuits while preserving simulation validity and measurable design quality?

### Automated Accelerator Optimization with GNNs

This paper represents an earlier generation of AI-for-EDA: a learned surrogate replaces repeated expensive HLS evaluations during design-space exploration. The central tradeoff is search speed versus prediction fidelity. A complete analysis must extract error distributions, workloads, design variables, transfer tests, and whether the final selected design is as good as the baseline’s selected design.

- Theme: AI-assisted EDA
- Subtheme: learned design-space exploration
- Sub-subtheme: surrogate modeling
- Key question: when does a learned predictor accelerate search without steering the optimizer toward a wrong design?

## Provisional cross-paper theme

These three seeds suggest a possible progression from learned prediction of design quality, to generative topology search, to language-model interfaces for broader design tasks. That is a research hypothesis only. It cannot become a DAC trend conclusion until the full 2026 program/paper set and a comparable historical edition are coded.
