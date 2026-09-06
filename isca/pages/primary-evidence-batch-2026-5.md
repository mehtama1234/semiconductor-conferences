# ISCA 2026 primary evidence batch 5

## ECC-enabled reliable and performant processing-in-memory

This record adds an institutional abstract for a paper that makes reliability a
first-class part of PIM design. The target failure modes are variable-retention-
time scaling errors, physical faults, and multi-bit errors in modern DRAM. The
authors describe a reliable bank-PIM architecture that detects multi-bit errors
and corrects at rank level without paying the full cost of repeated rank-level
corrections.

The proposed mechanism combines a Codeword Flip method for masking errors from
VRT weak cells with odd-even bank pipelining. The abstract reports 90% PIM-unit
utilization, up to 400x lower silent-data-corruption likelihood than traditional
bank-PIM over a five-year operating period, and potential 4x performance over
rankPIM in selected microbenchmarks, along with end-to-end LLM improvements.
[Institutional publication record](https://cris.technion.ac.il/en/publications/ecc-enabled-reliable-and-performant-processing-in-memory)

The detailed subskill is ECC-aware PIM architecture: reliability coding,
correction scheduling, and bank-level computation are designed together so
protection does not simply serialize or stall the accelerator. This complements
Cerberus’s cross-layer ECC coordination and PuDGhost’s physical interference
characterization, but it is not interchangeable with either.

Confidence is lower than the arXiv-backed records because the current evidence is
an institutional abstract rather than a captured full paper. Fault distributions,
ECC layouts, correction latency, area/energy overhead, and the exact LLM results
remain open extraction tasks.
