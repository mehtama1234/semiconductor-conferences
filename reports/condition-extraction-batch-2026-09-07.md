# Condition extraction batch — 2026-09-07

This is the first bounded P1 condition-extraction batch after deterministic
source recovery. It consolidates source-grounded conditions already captured in
the linked assessment records. It is not an independent review and does not
turn author-reported numbers into accepted comparisons.

| Paper | Source and locator | Conditions extracted | Boundary retained |
|---|---|---|---|
| DAC-043 Strix | [assessment](../dac/data/strix-primary-assessment-v1.json); Sections 5.1–5.2, PDF Table 1 | Gemmini on AMD VU19P; 20-node cluster; first 1,000 dataset samples and 10 runs; transient bit-flip and permanent stuck-at faults at 1e-7 per original-input bit; area-matched partial TMR, triple-instruction redundancy, and ReaLM baselines; 500 MHz and 28 nm synthesis assumptions | Synthesis is not silicon; BF16-I is absent from the latency table; fault injection is not safety certification |
| DAC-535 MappingEvolve | [assessment](../dac/data/mappingevolve-primary-assessment-v1.json); Sections 3.1, 3.2.3, 4.1, Table 2 | 11 ISCAS85 evolution circuits; EPFL/ASAP7 evaluation after `ABC compress2`; 30 outer × 3 inner iterations (90 direct iterations); ABC `&nf` and mockturtle baselines; Ubuntu 22.04, Xeon Gold 6226R, 256 GB; objective is equal-weight normalized area/delay | Table averages were visually cross-checked, not reproduced; model-version, seed, timeout, and held-out protocol remain unresolved |
| ICCAD-1109 SERA-Float | [assessment](../iccad/data/sera-float-primary-recovery-v1.json); Sections III.B, IV.A–C, Tables VIII–IX | 32-bit representation with 14 exponent, 8 mantissa, and split Hamming protection; ResNet-50/CIFAR-100 fault injections; 1.0 ns, 1.10 V, 25 °C, Synopsys Design Compiler, NanGate 45 nm; conventional FP32 multiplier baseline | Injected faults are not measured device faults; accuracy and energy claims are author-reported; displayed energy arithmetic and timing constraint require reconciliation |
| ICCAD-114 RIROS | [assessment](../iccad/data/riros-primary-recovery-v1.json); Sections IV–V, Table II | C++/Taskflow with gcc-11 `-O2`; reported i7, 16 cores at 3.80 GHz; seven designs; stuck-at wire/register faults with no fault dropping; ERASER one core, VCS and RIROS 16 cores | JPEG Table II runtimes and reported ratios disagree beyond displayed rounding; cross-tool speedup is not equal-core scaling or safety certification |
| ICCAD-1142 Capacitance ML | [assessment](../iccad/data/capacitance-ml-primary-recovery-v1.json); Sections V–VI, Table IV, Figures 14–16 | 94 imec N2 predictive-PDK cells; M0 thickness training 22–58 nm in 6 nm steps and testing 18–62 nm in 2 nm steps; dual Intel 6454S with 89 training threads; 0.082 s pattern and 0.803 s inference per cell; database/training setup recorded separately | 38 nm is used for hyperparameter-selection loss and is not demonstrated as an untouched test; predictive-PDK results are not silicon or cross-library validation; amortization remains open |

## Next extraction action

Audit the remaining P1 assessments in descending claim-risk order, starting with
records whose metrics are withheld pending table, baseline, or split
reconciliation. Preserve source locators and do not merge unlike units such as
kernel, communication, synthesis, and end-to-end speedups.
