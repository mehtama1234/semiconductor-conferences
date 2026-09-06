# Initial 2026 direction signals

This report is an evidence register, not the final trend analysis. It records what
the official 2026 program pages and call-for-papers materials make visible before
all paper abstracts and full texts have been normalized.

## What the sources support

- **ISCA 2026:** the public program exposes paper titles touching structured LLM
  execution, mixture-of-experts acceleration, memory management for multi-turn
  serving, and wafer-scale inference with communication and fault tolerance. These
  are program-level title signals, preserved in `isca/data/program-papers.jsonl`.
- **DAC 2026:** the official technical-program vocabulary contains multiple AI/ML
  tracks spanning hardware design, algorithms/models, architecture, and systems;
  it also separately covers in-memory/near-memory computing, SoC and 3D/2.5D
  methodology, verification, and hardware security. The normalized signal ledger
  is `dac/data/program-signals.jsonl`.
- **ICCAD 2026:** the CFP explicitly spans system-level CAD, core EDA, emerging
  computing/devices, 3D ICs, chiplets, advanced packaging, AI/hardware, and
  physical AI. ICCAD 2026 paper data is not yet treated as available in this
  repository; the 2025 program is the labeled paper-analysis fallback.

## What the sources do not support yet

These materials do not establish paper counts, technical superiority, industrial
adoption, market importance, or a rising/declining trend. A track or CFP topic is
an organizing signal. A paper title is metadata. Neither substitutes for the
problem, method, artifact, workload, baseline, metric, and limitation fields
required by the collection contract.

## Next evidence gate

The next collection pass should obtain the official accepted-paper or proceedings
metadata for each 2026 edition, then attach abstracts or permitted full-text
evidence where available. Only after deduplication, paper-level classification,
and adversarial review should these provisional signals become cross-conference
trend claims.
