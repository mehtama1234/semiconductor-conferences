# UGLMS: uncertainty-directed measurement, not just fewer samples

Assessment 2026-09-06; selected preprint evidence, independent review pending.
The [ICCAD preprint](https://arxiv.org/abs/2511.11895) matches the program title
and four authors. Its [condition ledger](../data/uglms-primary-recovery-v1.json)
preserves the PDF hash, timing table and limitations. The distinct *Advanced
Strategies* follow-up is not substituted for the conference version.

UGLMS makes measurement selection part of an estimation loop: local ADC sweeps
update a capacitor-mismatch model, whose uncertainty guides the next code edge.
Its significance for the emerging research directions is a shift in optimization
target from raw sample count to elapsed test time with useful estimates available.
That interpretation is a mechanism connection, not evidence of increasing adoption.

The evaluation uses simulated ADCs parameterized from modified measured-device
data. Timings assume acquisition/selection overlap and exclude reusable setup.
Selection cost rises with resolution; more samples can stabilize estimation but
slow progress. Small noisy sweeps can temporarily diverge, and covariance shrinkage
can produce late drift. Fixed-iteration results do not validate adaptive stopping.

Next comparisons should include setup amortization, compute resources, model
mismatch and actual tester behavior. A production claim also needs false-pass and
false-fail assessment, not only average reconstruction accuracy. These remain open.
