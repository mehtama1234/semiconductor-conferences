# ISCA 2026 Crossref metadata coverage

Capture date: 2026-09-06

The captured ISCA 2026 program contains 173 slots, including 172 nonempty titles
and one unresolved blank slot excluded from title denominators. A bounded
Crossref query for 2026 IEEE proceedings articles was reconciled against those
titles. The reconciliation produced 171 unique DOI matches, each with a DOI,
publisher URL, author metadata, and publication-date or page metadata in
`data/crossref-metadata-2026.jsonl`.

Two program items remain unresolved:

- `isca-2026-program-128`: the program title is “Optimizing 3D Gaussian
  Splatting with Axis-Shared Rasterization and Order-independent Transmittance”
  while the Crossref title begins “Efficient 3D Gaussian Splatting”; this is
  not merged automatically because the title change is material.
- `isca-2026-program-158`: the program contains an empty title/author block and
  is retained as a parse anomaly rather than assigned a DOI by inference.

The matching methods are recorded per row. Exact normalized title matches are
preferred; a unique paper-name prefix is used only when it identifies one
Crossref result. Crossref metadata is bibliographic evidence, not evidence for
the paper’s technical problem, method, workload, baseline, metric, or result.
Those fields remain unclassified until an abstract, paper, or other substantive
source is collected and adjudicated.

Source: [Crossref works API](https://api.crossref.org/works), queried with the
2026 publication window, IEEE prefix, and proceedings-article type.
