# Initial collection status

Status: **repository scaffold and authoritative source register**.

The project now has separate conference workspaces for ISCA, DAC, and ICCAD, a shared provisional taxonomy, and dated source ledgers. The collection policy is 2026-first. For any conference whose 2026 paper corpus is not publicly available, the latest complete accessible edition is used as a labeled fallback; ICCAD currently uses 2025 paper data while retaining 2026 scope metadata. The initial DAC seed papers and program inventories are collection inputs—not trend evidence.

Current inventory checkpoint:

- ISCA 2026: 173 official program records normalized with titles, authors, sessions, times, identifiers, and metadata-only status; Crossref reconciliation adds DOI/publisher metadata for 171 records, two remain unresolved, and five records also have secondary indexed excerpts pending primary verification.
- ISCA evidence: one paper (CODO) now has author-preprint and public-artifact-backed adjudication; five additional papers have substantive secondary-index excerpts with DOI metadata and remain low-confidence pending primary-source verification.
- DAC 2026: 543 distinct official research-manuscript records normalized in `dac/data/papers-2026-program.jsonl`, plus 75 other program items; all technical fields remain unclassified.
- DAC evidence: all 543 research pages returned substantive official descriptions; twenty-nine records have evidence-cited adjudications across EDA, accelerators, memory, packaging, verification, security, quantum, and reliability.
- DAC triage: all 543 descriptions now have keyword-backed routing candidates, explicitly marked non-adjudicated; the routing is for review queue construction only.
- Taxonomy/audit: `data/taxonomy-v1-evidence.json` reconciles adjudicated subtheme and sub-subtheme IDs across all three conferences; `reports/adversarial-preflight-v0.json` passes 32/32 deterministic consistency checks. This is a preflight, not a substitute for adversarial LLM or human review.
- ICCAD: 276 distinct 2025 program-paper records normalized as the explicitly labeled fallback for the 2026 target; two records now have primary/preprint evidence-cited adjudications, while the remaining fallback rows remain metadata-only.

DAC’s seven day-by-day program fragments are collected by `scripts/collect_dac_program.py`. The generated raw captures are locally reproducible evidence inputs and remain ignored by the repository’s raw-data policy; the normalized metadata ledgers are tracked.

Next collection batch:

1. extract paper titles, authors, identifiers, abstracts, tracks, and sessions from authoritative programs/proceedings;
2. resolve duplicate publisher, DOI, ACM, and IEEE records;
3. preserve permitted metadata and abstracts with capture dates and access status;
4. code problem, method, artifact, workload, assumptions, baselines, and metrics;
5. adjudicate theme → subtheme → sub-subtheme assignments;
6. publish one deep page per conference and per major research direction before cross-conference synthesis.

Program pages alone do not establish paper conclusions. Access restrictions, missing abstracts, title changes, and publisher-index inconsistencies will remain explicit.
