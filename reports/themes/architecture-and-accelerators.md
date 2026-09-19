# Architecture and accelerators

This article explains the subject and then connects it to 103 papers in the selected research sample.

A subtheme groups related technical problems. A mechanism describes the particular change proposed by a paper. The discussion below explains the subject; the linked paper records state the available evidence.

[Definitions used in the paper records](../reading-guide-v1.md)

## Start with the computation

A program performs operations on stored values. A processor must obtain those values, execute each operation, and store or forward its result. Operations that depend on earlier results must wait. Independent operations can run at the same time if enough hardware and data are available. An accelerator is hardware arranged for a particular kind of computation. Its benefit comes from reducing work, reducing data transfers, or executing more useful operations at once.

## Why more arithmetic units may not help

If an operation needs two inputs and those inputs have not arrived, an arithmetic unit waits. Adding units increases the possible rate of computation but also increases the rate at which inputs must arrive. The time to finish a job is therefore constrained by both computation and data supply. A design must also account for operations that cannot run in parallel. Performance on one large matrix calculation does not establish performance on an entire application.

## What separates the subthemes

Precision methods change how many bits represent a number and how much numerical error the application accepts. Sparse computation skips values or operations known to be unnecessary; it must also locate the remaining values and distribute uneven work. Dataflow methods choose when operations run and where intermediate results remain. Hardware and software co-design changes the machine and the program together, so the evaluation must identify which change caused the improvement.

## A comparison that answers the question

Hold the application, required answer quality, and input sizes fixed. Compare completion time, energy per completed job, memory use, and hardware cost. Then vary inputs that affect reuse or parallelism. If a specialized design wins only when all inputs fit in a small memory, that capacity condition is part of the result. The evidence cards below preserve the reported conditions; they should be read before transferring a result to a different application.

## Follow one result through the machine

Start with a dot product: multiply corresponding entries of two lists and add the products. For `[2, 3]` and `[5, 7]`, the answer is `2·5 + 3·7 = 31`. A hardware implementation must represent four inputs, locate them, transfer them to arithmetic units, perform the multiplications, and combine the results. If a later operation uses 31, that operation must receive the completed sum rather than just the first product, 10.

This short computation exposes four distinct design choices. Representation determines how many bits and what decoding rules describe each value. Data placement determines where those bits reside. Scheduling determines when each operation runs. Arithmetic determines how the represented inputs become a represented output. A paper can improve one choice while making another more expensive.

The explanations below connect recovered paper evidence through those choices. They do not establish a historical trend or a ranking across unrelated applications. The numerical examples in this theme discussion are teaching calculations, not additional paper measurements.

## Separate three limits before selecting an accelerator

Suppose a job needs 100 million arithmetic operations and transfers 200 million bytes through its limiting memory interface. A machine capable of ten billion useful operations per second needs at least ten milliseconds for the arithmetic. At ten billion transferred bytes per second, the traffic needs at least twenty milliseconds. If the two activities overlap perfectly, twenty milliseconds is a lower bound, not a prediction. Without overlap they could take thirty milliseconds before other costs.

Now suppose a chain of dependent operations takes thirty milliseconds. Even unlimited independent arithmetic capacity cannot finish that chain sooner without changing the operations or their individual latency. The job has a third limit: the time along its longest required dependency sequence.

These bounds explain why adding multipliers, widening memory interfaces, and improving task activation address different problems. A useful evaluation measures actual work, actual traffic at a named interface, and actual waiting. Counting source-program operations or stored model bytes alone does not provide those quantities.

### Representation can save transfers while adding execution work

Four 8-bit integer weights require four bytes before metadata. Encoding them with four bits each would require two bytes, but only if the chosen representation can express the required values or accepts approximation. A group descriptor occupying two additional bytes would remove the storage saving for this tiny group. Larger groups can spread descriptor cost across more values, while making it harder to select a good representation for every value.

Decoding also consumes hardware and time. A compact representation is valuable when its storage or traffic saving exceeds the cost of decoding and any additional coordination. The relevant evidence is bytes actually stored and transferred, not merely the nominal bits assigned to a weight.

[HAP's individual explanation](../observed-subthemes/approximate-and-precision-aware-compute.md#explanation-dac-2026-research1999) separates exact recovery of an already quantized activation from preservation of the original floating-point computation. Its recovered evaluation uses synthesis and simulation, not measured fabricated silicon. That source boundary matters when connecting arithmetic ideas to hardware claims.

[Duet](../observed-subthemes/sparse-and-irregular-compute.md#explanation-dac-2026-research1419) raises the related question at bit level: which digits are redundant, how are signs and positions recovered, and what work remains after skipping? Its manuscript is still missing. HAP and Duet therefore motivate a common representation question without supplying equally complete evidence or interchangeable results.

### Sparse values require addresses and completed reductions

In the dot product above, replacing 3 with zero removes the second useful multiplication. But a sparse format must identify which position remains so that 2 is still multiplied by 5 rather than 7. If locating one retained value costs more than the arithmetic avoided, sparsity can increase runtime.

Matrix operations add a second issue: several retained products may contribute to one output. Producing those products concurrently requires correct accumulation. Reordering independent products does not authorize dropping a contribution or reading an incomplete result.

[PFGEMM](../observed-subthemes/sparse-and-irregular-compute.md#explanation-dac-2026-research138) addresses compressed positions and execution order. [TRIDENT](../observed-subthemes/sparse-and-irregular-compute.md#explanation-dac-2026-research149) raises the related problem of retaining intermediate sparse products near later consumers. Both currently rely on descriptions rather than recovered manuscripts. Their connection is a question to investigate: can saved addressing or intermediate traffic pay for the added control and retained state?

### Ready work and nearby data are not always the same work

An idle worker can execute a ready task only after obtaining its operands. Assigning the task elsewhere may improve worker occupancy but cause extra transfers. Keeping it near its operands may improve reuse but leave another worker idle. Neither occupancy nor cache reuse alone is the application objective; completing the required job within time, energy, and correctness limits is.

[SALUT](../observed-subthemes/sparse-and-irregular-compute.md#explanation-dac-2026-research935) makes dependency readiness explicit in sparse factorization. [BSGCN](../observed-subthemes/sparse-and-irregular-compute.md#explanation-dac-2026-research1242) and [LTMiner](../observed-subthemes/sparse-and-irregular-compute.md#explanation-dac-2026-research240) make request order and retained data explicit. These papers do not prove one common optimal scheduler. They identify competing costs a scheduler must account for, under different computations and presently incomplete source evidence.

## Do not merge exact compression and approximation into one claim

There are at least three different meanings of preserving an answer. A codec may recover exactly the bits it received. An arithmetic implementation may preserve the result defined for those bits. An application may preserve an acceptable quality score despite changing many outputs. Proving one does not prove the others.

For example, compressing and exactly recovering the integer 7 says nothing about whether rounding an original real value to that integer was acceptable. Likewise, two generated videos can both receive good quality scores while showing different content. A benchmark's definition of quality must therefore accompany a speed claim.

[SPADE's manuscript-backed explanation](../observed-subthemes/sparse-and-irregular-compute.md#explanation-dac-2026-research680) provides a concrete reason to keep these distinctions. Its standard and Turbo configurations use different sparse-step schedules; the recovered table separates their timing and output-fidelity results. A higher perceptual-quality score does not establish greater similarity to the dense reference. That evidence cannot be collapsed into a single claim of faster, unchanged inference.

This is also why a taxonomy needs secondary relationships. Sparse attention may omit selected interactions approximately; bit-level sparsity may remove redundant digits exactly within an integer representation. Both can appear under sparsity, but their correctness obligations differ. Current navigation preserves historical classifications; these conceptual connections do not silently reclassify records or count them twice.

## Three long-term hypotheses worth testing

These are bounded interpretations of the linked mechanisms, not accepted longitudinal findings. Their purpose is to specify what further evidence could strengthen or reject them.

| Hypothesis | Why the mechanism could matter | Evidence that would weaken it |
| --- | --- | --- |
| Representation and scheduling increasingly need joint evaluation when arithmetic becomes a smaller cost | Fewer stored bits or indices can alter decoding, task size, and available parallelism | Matched workloads where decoding and coordination outweigh transfer savings, or where traffic was already insignificant |
| Fine-grained readiness helps primarily when broad synchronization hides substantial independent work | A task can start after its own inputs finish without waiting for unrelated tasks | Dependency chains that dominate runtime, too few ready tasks, or completion-notification cost exceeding removed waiting |
| Quality-constrained performance is more transferable than unconstrained peak speed for approximate methods | An application needs a usable result, not simply fewer executed operations | Gains disappearing at the required quality threshold or under shifted inputs, longer contexts, or different models |

Testing these hypotheses requires more than finding additional papers with matching titles. Within each application, compare equivalent input sets, numerical requirements, hardware budgets, and complete-job measurement boundaries. Report distributions and regressions, not only favorable averages. Across editions, use the same collection rules and distinguish missing manuscripts from measured negative results.

For ISCA, DAC, and ICCAD, the current selected sample cannot establish that one conference leads a trend or that a mechanism is growing. Conference identity is not an experimental control. A useful cross-conference connection instead asks whether separately evaluated components can satisfy one compatible set of requirements. A compiler result, an accelerator result, and a physical implementation result remain separate evidence until their interfaces, formats, capacities, and measurement conditions align.

## What an end-to-end comparison must retain

Take an illustrative baseline job lasting 100 milliseconds: 20 for preparation, 50 for accelerated computation, and 30 for everything else. A fivefold improvement in the middle stage gives `20 + 10 + 30 = 60` milliseconds, or about 1.67× overall. If the proposed format adds 15 milliseconds of conversion, the result becomes 75 milliseconds, or about 1.33×. Reusing preparation changes the comparison again and must be reported explicitly.

A connected account should therefore follow one input through preparation, conversion, execution, output handling, and quality checking. It should state which steps are timed, which costs are reused, where bytes cross an interface, and which failure conditions remain. Faster arithmetic is a component result until this accounting supports an application result.

The [precision-aware chapter](../observed-subthemes/approximate-and-precision-aware-compute.md) and [sparse/irregular chapter](../observed-subthemes/sparse-and-irregular-compute.md) now supply expanded individual explanations for their recorded papers. Other architecture branches below remain uneven in depth. This theme synthesis does not complete their rewrites, source recovery, classification reconciliation, or independent review.

## Subthemes and how to study them

Each link opens the subtheme discussion and its captured paper records. Explanatory depth varies: some papers have expanded individual explanations; others still have only brief discussion or evidence cards. Source locations and unresolved conditions remain visible.

### [Specialized accelerators and dataflow](../observed-subthemes/specialized-accelerators-and-dataflow.md)

35 selected records in this theme. Start with [Leveraging AI-Inspired Hardware Architecture to Enhance LPN Acceleration in Post-Quantum Cryptography](../observed-subthemes/specialized-accelerators-and-dataflow.md).

### [Approximate and precision aware compute](../observed-subthemes/approximate-and-precision-aware-compute.md)

14 selected records in this theme. Start with [Algorithm and Hardware Co-Design for Efficient Complex-Valued Uncertainty Estimation](../observed-subthemes/approximate-and-precision-aware-compute.md).

### [Architecture software co design](../observed-subthemes/architecture-software-co-design.md)

13 selected records in this theme. Start with [UniNL: Unifying Fragmented Non-Linear Operators for Efficient Edge LLM Inference](../observed-subthemes/architecture-software-co-design.md).

### [Sparse and irregular compute](../observed-subthemes/sparse-and-irregular-compute.md)

11 selected records in this theme. Start with [BSGCN: Taming Diverse Sparsities in GCNs via Adaptive Band-Segmentation and Tailored Caching](../observed-subthemes/sparse-and-irregular-compute.md).

### [Quantum architectures and control](../observed-subthemes/quantum-architectures-and-control.md)

9 selected records in this theme. Start with [Compiler Framework for Directional Transport in Zoned Neutral-Atom Systems with AOD Assistance: A Hybrid Remote CZ Approach](../observed-subthemes/quantum-architectures-and-control.md).

### [Specialized AI accelerators](../observed-subthemes/specialized-ai-accelerators.md)

9 selected records in this theme. Start with [DIA-CIM: A Dynamic Iterative Aggregation Graph Neural Network and Its Hardware Co-Design for Energy-Efficient Graph Processing](../observed-subthemes/specialized-ai-accelerators.md).

### [AI accelerator microarchitecture](../observed-subthemes/ai-accelerator-microarchitecture.md)

4 selected records in this theme. Start with [AMBER: A Unified Accelerator for Multi-Precision LLM Inference Exploiting Bit-Level Redundancy and Reconfigurability](../observed-subthemes/ai-accelerator-microarchitecture.md).

### [Memory and data movement](../observed-subthemes/memory-and-data-movement.md)

3 selected records in this theme. Start with [REACT: Rapid Error-Tolerant Activation Compressor for Efficient Transformer Training](../observed-subthemes/memory-and-data-movement.md).

### [Emerging and nonvon neumann compute](../observed-subthemes/emerging-and-nonvon-neumann-compute.md)

2 selected records in this theme. Start with [PMTPA: An Ising Model-Based Parallel-Momentum Tempering Processing Architecture for Combinatorial Optimization](../observed-subthemes/emerging-and-nonvon-neumann-compute.md).

### [Distributed and wafer scale inference](../observed-subthemes/distributed-and-wafer-scale-inference.md)

1 selected records in this theme. Start with [Mapping and Communication Optimizations with Fault Tolerance for Wafer-Scale LLM Inference](../observed-subthemes/distributed-and-wafer-scale-inference.md).

### [Edge AI and deployment](../observed-subthemes/edge-ai-and-deployment.md)

1 selected records in this theme. Start with [Tsetlinwisard: On-Chip Training of Weightless Neural Networks Using Tsetlin Automata on FPGAs](../observed-subthemes/edge-ai-and-deployment.md).

### [Neuromorphic and emerging architectures](../observed-subthemes/neuromorphic-and-emerging-architectures.md)

1 selected records in this theme. Start with [Unispike: Accelerating Spiking Neural Networks on Neuromorphic Systems via Eliminating Address Redundancy](../observed-subthemes/neuromorphic-and-emerging-architectures.md).

## Representative source-backed records

The following reading set spans the available conferences and uses dated corrections where registered. These corrections improve the current reading view but do not change historical adjudication or establish independent acceptance. Each paper link opens its exact evidence card.

## Paper cards: what changes and where it stops

- [MTIA 300: Meta’s First Training Chip Featuring Built-in NICs and Collective Offloading Engines](../observed-subthemes/architecture-software-co-design.md#paper-isca-2026-program-069) — ISCA 2026.
- [Mapping and Communication Optimizations with Fault Tolerance for Wafer-Scale LLM Inference](../observed-subthemes/distributed-and-wafer-scale-inference.md#paper-isca-2026-program-060) — ISCA 2026.
- [Accelerating MoE with Dynamic In-Switch Computing on Multi-GPUs](../observed-subthemes/architecture-software-co-design.md#paper-isca-2026-program-058) — ISCA 2026.
- [OASIS: Outlier-Aware LUT-Based GEMM with Dual-Side Quantization for LLM Inference Acceleration](../observed-subthemes/ai-accelerator-microarchitecture.md#paper-isca-2026-program-020) — ISCA 2026.
- [ATTINA: Spatial Acceleration of Additive Number Theoretic Transform for Energy-Efficient zkSNARKs at the Edge](../observed-subthemes/specialized-accelerators-and-dataflow.md#paper-dac-2026-research983) — DAC 2026.
- [UNICON: A Unified Reconfigurable Nonlinear Architecture for Efficient Neural Network Inference](../observed-subthemes/specialized-accelerators-and-dataflow.md#paper-dac-2026-research946) — DAC 2026.
- [SALUT: Efficient Sparse LU Factorization via Asynchronous Task Triggering on HBM FPGAs](../observed-subthemes/sparse-and-irregular-compute.md#paper-dac-2026-research935) — DAC 2026.
- [Chimera: A Unified FHE Accelerator with Enhanced Compatibility for TFHE](../observed-subthemes/specialized-accelerators-and-dataflow.md#paper-dac-2026-research885) — DAC 2026.
- [Squat: Quant Small Language Models on the Edge](../observed-subthemes/architecture-software-co-design.md#paper-iccad-2025-105) — ICCAD 2025.
- [Combating the Memory Walls: Optimization Pathways for Long-Context Agentic LLM Inference](../observed-subthemes/architecture-software-co-design.md#paper-isca-2026-program-007) — ISCA 2026.
- [Cassandra: Enabling Reasoning LLMs at Edge via Self-Speculative Decoding](../observed-subthemes/architecture-software-co-design.md#paper-isca-2026-program-006) — ISCA 2026.
- [Patterns Behind Chaos: Forecasting Data Movement for Efficient Large-Scale MoE LLM Inference](../observed-subthemes/architecture-software-co-design.md#paper-isca-2026-program-005) — ISCA 2026.

## What the evidence supports

These records identify proposed methods and the conditions recorded for them. A reported improvement should be interpreted with its comparison method, input size, hardware, and result-quality requirement. Missing fields are evidence gaps; a populated field can also state that a detail is unspecified.

## Limits and next evidence

The selected sample is uneven across conferences and source types. It cannot establish how fast a subject is growing. Repeated observations across comparable years, with the same inclusion rules and source depth, are needed for a time trend.

Every linked evidence article preserves the Problem: and Mechanism / artifact: fields, baseline, unshortened limitations, source URL, and recorded location. Primary text and independent review remain necessary where the record says those checks are open.

[Research directions](../directions/README.md) · [All observed subthemes](../expanded-taxonomy-v1.md)
