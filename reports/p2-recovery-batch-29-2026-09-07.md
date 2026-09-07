# P2 recovery routing batch 29 — 2026-09-07

This tranche continues the DAC frontier across RowHammer monitoring, process
window optimization, DNN bit-flip defense, single-GPU fine-tuning, inverse
lithography, timing placement, NAND/CIM MoE inference, hypergraph partitioning,
SEM imaging, and chip-to-chip interconnect exploration.

| Priority | Paper ID | Title | Evidence needed before quantitative use |
|---:|---|---|---|
| 1 | `dac-2026-research1275` | TRAC: Transparent Row Activation Counting for Efficient Rowhammer Monitoring | DRAM/platform, activation-counting granularity, attack traces, detection/false-positive rate, overhead, and monitor baseline |
| 2 | `dac-2026-research1282` | CPW-SMO: Generating Mask Sets and Common Source for Maximum Common Process Window | Process/PDK, lithography model, mask/source constraints, fidelity/yield metric, optimization budget, and baseline |
| 3 | `dac-2026-research1284` | WFH-BFs: Dynamic Defense Against DNN Bit-Flips via a Weight Function Hierarchy | Fault/attack model, DNN suite, hierarchy policy, accuracy/recovery, runtime/energy, and ECC/retraining baseline |
| 4 | `dac-2026-research1286` | An Efficient Heterogeneous Co-Design for Fine-Tuning on a Single GPU | Model/dataset, GPU/CPU split, optimizer/precision, convergence, throughput/memory/energy, and GPU-only baseline |
| 5 | `dac-2026-research1287` | From Fab to Mask Shop: A Differentiable MDP-ILT Framework for Co-Optimization of Wafer Pattern Fidelity and Mask Writability | Process/lithography, pattern corpus, MDP actions/reward, fidelity/writability metrics, runtime, and ILT baseline |
| 6 | `dac-2026-research1290` | Analytically-Derived Hybrid Net–pin Weighting for Timing-Driven Global Placement | Design/PDK corpus, timing model, weighting derivation, wirelength/congestion/slack, runtime, and placer baseline |
| 7 | `dac-2026-research1291` | NASiC: 3D NAND-Based CAM-Selected Multibit CIM Architecture for Efficient On-Device Mixture-of-Experts LLM Inference | NAND/CAM/CIM device, MoE models, selection/precision, endurance, latency/energy/area, and conventional edge baseline |
| 8 | `dac-2026-research1292` | Impart: Integration of Memetic Operations into Multi-Level Framework for Large-k-Way Hypergraph Partitioning | Hypergraph corpus, partition constraints/objective, memetic budget, cut/balance/runtime, and partitioner baseline |
| 9 | `dac-2026-research1298` | FreqSEM: Frequency-Aware High-Precision Contour Extraction for Lithographic SEM Images | SEM/device corpus, frequency method, annotation/error metric, transfer split, runtime, and image-processing baseline |
| 10 | `dac-2026-research130` | C2C-Explorer: An Exploration Framework for Chip-to-Chip Interconnect Architectures in LLM Cloud Computing Systems | Model/traffic traces, topology/link/process, exploration space, latency/bandwidth/power/cost, and fixed-topology baseline |

These are source-recovery priorities and condition checklists, not technical
rankings or temporal trend evidence.
