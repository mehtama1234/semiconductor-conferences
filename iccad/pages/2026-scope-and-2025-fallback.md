# ICCAD 2026 scope and the 2025 paper fallback

ICCAD is treated as a 2026-first project. The 2026 CFP and official site define
the target scope, while the captured 2025 program provides the current paper-level
fallback because the 2026 paper corpus is not yet represented in this repository.
The 319 fallback rows in `iccad/data/papers-2025-program.jsonl` are metadata-only;
they are not technical adjudications.
They include 43 invited papers and ten student presentations, explicitly excluded
from regular-paper comparisons. The remaining 266 entries are mapped to 50 regular
sessions. This establishes program type, not equivalent technical evidence for
temporal claims. See the [scope audit](../reports/program-scope-audit-v1.md).

## What the 2026 CFP says the field can contain

### System-level CAD

The CFP includes hardware/software co-design, AI and accelerators, embedded and
edge systems, security, and efficiency. These are best treated as a system-level
cross-cutting layer rather than a single method family.

### Core EDA and physical implementation

The scope covers logic synthesis, placement, routing, clock-tree synthesis,
formal verification, emulation, ATPG, post-silicon debug, timing, power, signal
integrity, design-for-manufacturing, yield, reliability, and analog/mixed-signal,
RF, and electromagnetic analysis. The analysis taxonomy therefore needs to keep
algorithmic design automation distinct from process-aware physical constraints.

### Emerging computation and devices

The CFP names post-CMOS, non-von Neumann, quantum, DNA, neuromorphic, and bio-CAD
directions. These labels indicate the intended research envelope; they do not
establish technical maturity or acceptance volume.

### Advanced integration and physical AI

3D ICs, chiplets, advanced packaging, AI/hardware, and physical AI are explicitly
included. The useful analytical question is how these areas interact with
verification, thermal behavior, yield, and system-level design—not merely whether
the keywords appear.

## Fallback corpus status

The 2025 program PDF now yields 319 unique numbered entries with titles and authors,
after recovering 43 invited papers skipped by the original identifier parser.
For every row:

- `target_edition` remains `2026`;
- `analysis_edition` is `2025`;
- access is marked `official_fallback_program_pdf_metadata_only`;
- problem, method, workload, baselines, metrics, and taxonomy assignments remain
  unfilled until abstracts or full papers are collected.

## Limits and next step

Fifteen fallback papers have separate technical coding records; these do not
promote the metadata inventory itself to technical evidence. Independent review
remains pending. Unnumbered talks and workshop contributions are not covered by
the numbered-entry completeness check.

The CFP is a scope document, not a prevalence measurement. The 2025 fallback is a
paper inventory, not evidence that any direction is dominant or increasing. The
next step is to expand authorized abstract/full-text recovery, complete paper-type
classification and technical review, and then compare the 2025 fallback with the eventual
2026 corpus using the same schema.
