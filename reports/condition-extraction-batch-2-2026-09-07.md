# Condition extraction batch 2 — 2026-09-07

This second P1 batch consolidates five additional source-grounded assessments.
All metrics remain author-reported or analytically checked; none is an
independent acceptance verdict.

| Paper | Source and locator | Conditions extracted | Boundary retained |
|---|---|---|---|
| ICCAD-1117 UGLMS | [assessment](../iccad/data/uglms-primary-recovery-v1.json); Sections III.E–VI, Table I | 100 synthetic 16-bit ADCs; 200 iterations; 128 samples/sweep and 1.0 LSB RMS input noise; assumed 1 MS/s acquisition with concurrent selection; 12-bit reconstruction compared with ramp-histogram testing at 128 hits/code | Measured-device vectors were resampled/shifted; matrix setup is excluded; compute platform and adaptive stopping remain unresolved |
| ICCAD-105 Squat | [assessment](../iccad/data/squat-primary-recovery-v1.json); Sections IV, V-B, Tables II–IV and VIII | LLaMA-58M and GPT2-97M; OnePlus 11 Snapdragon 8 Gen 2 and Raspberry Pi 5 BCM2712; 1,000 iterations/test; sequence length 128; FP16, NIPQ, PACT, and LLM-QAT accuracy baselines; latency in ms/token | W4A4 speedup is not iso-accuracy; warmup/thermal controls and prefill/decode boundary remain unresolved |
| ICCAD-109 HLPS-DSE | [assessment](../iccad/data/hlps-dse-primary-recovery-v1.json); Sections IV, VII-C/D, Table V | Six accelerator designs across four multi-die FPGA architectures (Alveo U55C/U280/U250 and Versal VHK158); AMD EPYC 7742, 256 GB DDR4-3200; Vitis, `-O3 Explore`, and AutoBridge baselines; up to four concurrent jobs | Fmax is not application throughput; cumulative actions are not independent ablations; search populations and budgets are unequal |
| ICCAD-437 Orthrus | [assessment](../iccad/data/orthrus-primary-recovery-v1.json); Sections II-B, III, IV-A/B, Figures 9–11, Table III | 8×8 systolic MAC array; customized ASAP7; Genus/Innovus/Liberate/Spectre/Calibre/OpenBox toolchain; system-only baseline; no-fusion and no-recharacterization ablations; population 100, 20 generations, top 5, two technology-search iterations | Hypervolume is not application speedup; iso-power and iso-delay are separate operating points; total search-cost normalization remains unresolved |
| DAC-1000 ATB | [assessment](../dac/data/atb-primary-assessment-v1.json); Sections 6.3, Tables 2–3 | AMD Ryzen AI 9 HX 370 with IRON and MLIR-AIE; reported matrix dimensions are explicitly different between MLIR-AIE, symmetric, and ATB rows; 4.8/17.3/24.3 TFLOPS rows and 24.6 TFLOPS size-sweep peak | Printed 4.54× ratios fail arithmetic checks; unequal matrices prevent matched-workload comparison; two author-name mappings and final-version identity remain unresolved |

## Next extraction action

Continue with the remaining P1 assessments that have full or selected source
text, prioritizing records where split, budget, baseline, or table arithmetic
could change the interpretation of a headline metric.
