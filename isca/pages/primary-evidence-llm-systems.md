# ISCA 2026: primary-evidence batch on LLM systems

This page synthesizes four author-preprint-backed papers. The claims below are
reported results from the cited preprints, not independent reproductions.

## 1. MoE inference is becoming a data-movement problem

**Patterns Behind Chaos** profiles four 200B–1000B Mixture-of-Experts models
over more than 24,000 requests. Its key move is to treat expert-selection
traffic as the object of analysis, separating temporal and spatial patterns
before proposing system changes. The paper reports six design insights, a
6.6x average speedup from lightweight changes on wafer-scale GPUs, and up to
1.25x speedup from prefill-aware expert placement on existing GPU systems. It
also releases profiling traces.

The important technical implication is narrower than “MoE is solved”: routing
behavior can become an architecture input. The unresolved questions are how
stable those patterns are across model families, request mixes, routing
policies, and interconnect topologies.

Source: [author preprint](https://arxiv.org/abs/2510.05497), [released traces](https://huggingface.co/datasets/core12345/MoE_expert_selection_trace).

## 2. Quantization is moving into the datapath

**OASIS** addresses the mismatch between useful non-uniform weight/activation
quantization and conventional low-precision compute. It uses Cartesian-product
lookup tables to avoid dequantization, outlier-aware quantization and error
compensation to protect quality, and a top-k outlier detector called Orizuru.
The preprint reports a 64x LUT-size reduction, 1024x higher parallelism than
prior LUT-based GEMM, 1.98% average accuracy drop versus FP16, 3.00x speedup,
and 1.44x energy-efficiency improvement over FIGLUT.

The deeper direction is co-design across quantization statistics, datapath
organization, and outlier handling. The reported gains still need full-paper
checks of model suite, accuracy metric, area, energy accounting, and sequence
length.

Source: [author preprint](https://arxiv.org/abs/2507.23035).

## 3. Distributed training is being decomposed into resource planes

**DisDP** argues that model-sharded data parallelism serializes compute,
network collectives, and optimizer-state storage. It proposes full
disaggregation: SmartNIC/SmartSwitch offload for collectives and a
SmartSwitch-enhanced parameter server for storage. The abstract reports a
3.98x improvement over state-of-the-art training systems on eight GPUs while
training a 175B model.

This is not merely a faster collective algorithm. It is a systems boundary
proposal that assigns compute, network, and storage to different resources.
The evidence still needs verification of the comparison systems, network
topology, parameter-server bottlenecks, fault behavior, and scaling beyond the
reported eight-GPU experiment.

Source: [author preprint](https://arxiv.org/abs/2409.00918).

## 4. Thermal management becomes a distributed-systems concern

**Lit Silicon** links thermal imbalance to concurrent computation/communication
and shows how hotter GPUs become stragglers that slow cooler GPUs. It proposes
performance/power models, detection and mitigation, and evaluates three power
management strategies on two AMD Instinct MI300X systems, two workloads, and
two LLM-training frameworks. It reports up to 6% performance and 4% power
improvements.

The field direction is a shift from “GPU power” as a local device constraint to
thermal coordination as a node-level scheduling and efficiency problem. The
current evidence does not establish generality across GPU generations,
cooling systems, cluster sizes, or workloads.

Source: [author preprint](https://arxiv.org/abs/2511.09861).

## Cross-paper interpretation

These four papers point to a common architecture pattern: performance is being
won by exposing and coordinating hidden system state. MoE routing traffic,
quantization outliers, resource-plane interference, and thermal stragglers are
all treated as dynamic conditions that hardware/software boundaries must
observe and respond to.

That is a research direction, not a market or adoption claim. The evidence is
small and selected: four preprints from a 173-item program inventory. Full
paper extraction, artifact reproduction, and adjudication across the remaining
ISCA records are required before ranking this as a conference-wide trend.
