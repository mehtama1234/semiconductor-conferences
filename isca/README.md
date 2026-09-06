# ISCA — International Symposium on Computer Architecture

Focus: processors, memory systems, accelerators, interconnects, architecture/software co-design, security, emerging architectures, and production-scale systems.

Initial authoritative sources:

- [ISCA 2026 home](https://www.iscaconf.org/isca2026/index.php)
- [ISCA 2026 Call for Papers](https://www.iscaconf.org/isca2026/submit/callforpapers.php)
- [ISCA 2026 Industry Track](https://www.iscaconf.org/isca2026/submit/industry.php)

The official 2026 program yields 173 captured rows in `data/papers-2026-program.jsonl`: 172 nonempty titles and one unresolved blank slot. Title comparisons exclude that slot while retaining its stable ID. Program titles remain discovery evidence until technical evidence is collected.

The official 2025 program is preserved as a historical metadata-only baseline in `data/papers-2025-program.jsonl` with 135 paper records. It supports inventory and comparable-coverage checks only; it does not support technical prevalence or trend claims without separate abstract/full-text evidence.

Crossref reconciliation in `data/crossref-metadata-2026.jsonl` adds DOI, publisher, author, page, and publication-date metadata for 171 uniquely reconciled records. Two program items remain unresolved because their titles differ materially from the Crossref record or are blank. These records remain metadata-only; technical claims require abstracts, paper text, or other substantive evidence.

Subfolders: `data/raw/` for permitted source responses, `reports/` for ledgers and analyses, and `pages/` for deep topic pages.
