# Initial collection status

Status: **repository scaffold and authoritative source register**.

The project now has separate conference workspaces for ISCA, DAC, and ICCAD, a shared provisional taxonomy, and dated source ledgers. The collection policy is 2026-first. For any conference whose 2026 paper corpus is not publicly available, the latest complete accessible edition is used as a labeled fallback; ICCAD currently uses 2025 paper data while retaining 2026 scope metadata. The initial DAC seed papers and program inventories are collection inputs—not trend evidence.

Current inventory checkpoint:

- ISCA 2026: 7 official program-title records normalized as metadata-only and hypothesis-only.
- DAC 2026: 543 distinct official research-manuscript records normalized in `dac/data/papers-2026-program.jsonl`, plus 75 other program items; all technical fields remain unclassified.
- ICCAD: 2026 scope signals captured; 2025 remains the explicitly labeled paper-analysis fallback.

DAC’s seven day-by-day program fragments are collected by `scripts/collect_dac_program.py`. The generated raw captures are locally reproducible evidence inputs and remain ignored by the repository’s raw-data policy; the normalized metadata ledgers are tracked.

Next collection batch:

1. extract paper titles, authors, identifiers, abstracts, tracks, and sessions from authoritative programs/proceedings;
2. resolve duplicate publisher, DOI, ACM, and IEEE records;
3. preserve permitted metadata and abstracts with capture dates and access status;
4. code problem, method, artifact, workload, assumptions, baselines, and metrics;
5. adjudicate theme → subtheme → sub-subtheme assignments;
6. publish one deep page per conference and per major research direction before cross-conference synthesis.

Program pages alone do not establish paper conclusions. Access restrictions, missing abstracts, title changes, and publisher-index inconsistencies will remain explicit.
