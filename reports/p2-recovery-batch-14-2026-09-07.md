# P2 recovery routing batch 14 — 2026-09-07

This tranche routes ten ISCA records spanning streaming side channels, point
cloud acceleration, collective communication, prefetching, 2D-material caches,
reliable DNNs, long-context serving, edge MoE, and NPU compression.

| Priority | Paper ID | Title | Evidence needed before quantitative use |
|---:|---|---|---|
| 1 | `isca-2026-program-075` | DarkStream: Exploiting Internal Throughput Contention in Data Streaming Accelerator for Timing Attacks | Accelerator microarchitecture, contention channel, attacker capability, leakage metric, mitigations, and security baseline |
| 2 | `isca-2026-program-076` | L-PCN: A Point Cloud Accelerator Exploiting Spatial Locality through Octree-based Islandization | Point-cloud datasets, octree construction, accelerator target, accuracy preservation, throughput/energy, and prior accelerator baseline |
| 3 | `isca-2026-program-077` | NS-FPS: Accelerating Farthest Point Sampling via Neighbor Search in Large-Scale Point Clouds | Sampling quality, point-cloud scale, neighbor-search structure, hardware/process, latency/energy, and CPU/GPU baseline |
| 4 | `isca-2026-program-078` | RoCC: Harnessing Raster Operations Pipeline for Efficient Tensor Collective Communication | GPU/raster pipeline, collective patterns, topology, message sizes, correctness, throughput/latency, and NCCL baseline |
| 5 | `isca-2026-program-079` | STEP: Spatial Footprint Prefetcher with Multi-Point Temporal Triggers | Memory hierarchy, trace suite, trigger state/storage, accuracy/coverage, bandwidth/latency, and conventional prefetcher baselines |
| 6 | `isca-2026-program-080` | TDMSim: Enabling High-Density and Energy-Efficient GPU DRAM Caches with 2D-Materials for Data-Intensive Applications | 2D material/device assumptions, cache organization, GPU workloads, density/yield, energy/latency, and conventional DRAM baseline |
| 7 | `isca-2026-program-081` | RangeGuard: Efficient, Bounded Approximate Error Correction for Reliable DNNs | Fault model, error bounds, DNN suite, precision, recovery policy, accuracy/overhead, and ECC/retraining baselines |
| 8 | `isca-2026-program-082` | Tetris: Efficient Long-context LLM Serving with Chunkwise Dynamic Sequence Parallelism | Models/context lengths, GPU topology, chunk policy, communication overhead, throughput/P99 SLO, and static-parallel baseline |
| 9 | `isca-2026-program-083` | SMoE: An Algorithm-System Co-Design for Pushing MoE to the Edge via Expert Substitution | Edge device, model/router, substitution quality, memory/power budget, latency/accuracy, and full-model baseline |
| 10 | `isca-2026-program-084` | ENEC: A Lossless AI Model Compression Method Enabling Fast Inference on Ascend NPUs | Model/task suite, lossless definition, compression ratio, Ascend NPU/software, latency/energy, and uncompressed baseline |

These are source-recovery priorities, not technical rankings or evidence of
prevalence/trend direction.
