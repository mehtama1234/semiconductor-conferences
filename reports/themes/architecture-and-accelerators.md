# Architecture and accelerators

This article explains the subject and then connects it to 103 papers in the selected research sample.

A subtheme groups related technical problems. A mechanism describes the particular change proposed by a paper. The discussion below explains the subject; the linked paper records state the available evidence.

[Definitions used in the paper records](../reading-guide-v1.md)

## A processor fetches values, computes, and passes results on

A program performs operations on stored values. For each operation the processor must:

1. obtain the input values;
2. execute the operation;
3. store or forward the result.

An operation that depends on an earlier result must wait for it. Independent operations can run at the same time, if enough hardware and data are available.

An **accelerator** is hardware arranged for one kind of computation. Its benefit comes from one of three things: less work, fewer data transfers, or more useful operations at once.

## More arithmetic units help only if their inputs arrive in time

An operation needs its inputs. If they have not arrived, the arithmetic unit waits.

Adding units raises the possible rate of computation. It also raises the rate at which inputs must arrive. So the time to finish a job is limited by both computation and data supply.

Some operations cannot run in parallel at all. That is why good performance on one large matrix calculation does not show good performance on a whole application.

## The subthemes differ in what they change

- **Precision methods** change how many bits represent a number, and how much numerical error the application accepts.
- **Sparse computation** skips values or operations known to be unnecessary. It must still find the remaining values and share out the uneven work.
- **Dataflow methods** choose when operations run and where intermediate results stay.
- **Hardware and software co-design** changes the machine and the program together. The evaluation must then show which change caused the improvement.

## A fair test holds the job fixed and measures the whole cost

1. Hold the application, the required answer quality and the input sizes fixed.
2. Compare completion time, energy per completed job, memory use and hardware cost.
3. Vary the inputs that affect reuse or parallelism.

Suppose a specialized design wins only when all inputs fit in a small memory. Then that memory size is part of the result. The evidence cards below keep the reported conditions. Read them before applying a result to a different application.

## Follow one result through the machine

One small sum shows the four choices every accelerator makes.

A **dot product** multiplies matching entries of two lists, then adds the products.

> **Worked example.** For `[2, 3]` and `[5, 7]`: `2·5 + 3·7 = 10 + 21 = 31`.

To compute it, the hardware must hold four inputs, find them, move them to arithmetic units, multiply, and add. A later operation that uses 31 must get the finished sum, not just the first product, 10.

| Choice | What it decides |
| --- | --- |
| Representation | How many bits, and which decoding rules, describe each value |
| Data placement | Where those bits are stored |
| Scheduling | When each operation runs |
| Arithmetic | How the stored inputs become a stored output |

A paper can improve one choice while making another more expensive.

**Be careful:** the explanations below link paper evidence through these choices. They do not show a historical trend or a ranking across unrelated applications. The numbers in this theme are teaching calculations, not paper measurements.

## Separate three limits before selecting an accelerator

A job is held back by arithmetic, by data traffic, or by a chain of steps that must wait for each other.

> **Worked example.** A job needs 100 million operations and moves 200 million bytes through its slowest memory interface.
>
> - Arithmetic at ten billion useful operations per second: at least 100 million ÷ 10 billion = **10 milliseconds**.
> - Traffic at ten billion bytes per second: at least 200 million ÷ 10 billion = **20 milliseconds**.
> - If the two overlap perfectly, 20 milliseconds is a lower bound, not a prediction.
> - With no overlap, they could take 10 + 20 = **30 milliseconds**, before other costs.

Now suppose a chain of dependent operations takes thirty milliseconds. Unlimited extra arithmetic cannot finish that chain sooner. Only changing the operations, or how long each one takes, can. This is the third limit: the time along the longest chain of required steps.

So different fixes solve different problems:

- more multipliers help the arithmetic limit;
- wider memory interfaces help the traffic limit;
- faster task start-up helps the waiting limit.

A useful evaluation measures actual work, actual traffic at a named interface, and actual waiting. Counting operations in the source program, or bytes in a stored model, does not give those numbers.

### Representation can save transfers while adding execution work

Fewer bits per value save storage and traffic only if the extra description and decoding cost less.

> **Worked example.** Four 8-bit integer weights take 4 bytes, before any metadata.
>
> - At 4 bits each, they take 2 bytes. This works only if 4 bits can express the needed values, or approximation is acceptable.
> - Add a 2-byte group descriptor, and the saving for this tiny group is gone: 2 + 2 = 4 bytes.
> - Larger groups spread the descriptor cost over more values. But one representation then has to suit more values.

Decoding also uses hardware and time. A compact format pays off when its storage or traffic saving is bigger than the decoding and coordination cost. The evidence that counts is bytes actually stored and moved, not the nominal bits per weight.

Two papers show this question from different angles:

- [HAP's individual explanation](../observed-subthemes/approximate-and-precision-aware-compute.md#explanation-dac-2026-research1999) separates exactly recovering an already quantized activation from preserving the original floating-point result. Its evaluation uses synthesis and simulation, not measured fabricated silicon.
- [Duet](../observed-subthemes/sparse-and-irregular-compute.md#explanation-dac-2026-research1419) asks the same at bit level: which digits are redundant, how are signs and positions recovered, and what work remains after skipping? Its manuscript is still missing.

**Be careful:** HAP and Duet raise a shared question. Their evidence is not equally complete, and their results are not interchangeable.

### Sparse values require addresses and completed reductions

Skipping zeros saves arithmetic, but the hardware must still know where each kept value belongs.

In the dot product above, replace 3 with zero. The second multiplication disappears. But the sparse format must record which position remains, so 2 is still multiplied by 5, not 7. If finding one kept value costs more than the skipped arithmetic, sparsity makes the job slower.

Matrix operations add a second issue. Several kept products may feed one output, so running them at once needs correct adding-up. Reordering independent products is allowed. Dropping a contribution, or reading an unfinished result, is not.

- [PFGEMM](../observed-subthemes/sparse-and-irregular-compute.md#explanation-dac-2026-research138) handles compressed positions and execution order.
- [TRIDENT](../observed-subthemes/sparse-and-irregular-compute.md#explanation-dac-2026-research149) keeps intermediate sparse products near the operations that use them next.

Both currently rely on descriptions, not recovered manuscripts. Together they pose a question: can the saved addressing or traffic pay for the added control and stored state?

### Ready work and nearby data are not always the same work

A scheduler must trade keeping workers busy against keeping data close.

An idle worker can run a ready task only after fetching its inputs.

- Sending the task elsewhere may keep workers busier, but adds transfers.
- Keeping it near its inputs may improve reuse, but leaves another worker idle.

Neither busy workers nor cache reuse is the goal. The goal is finishing the job within time, energy and correctness limits.

- [SALUT](../observed-subthemes/sparse-and-irregular-compute.md#explanation-dac-2026-research935) makes dependency readiness explicit in sparse factorization.
- [BSGCN](../observed-subthemes/sparse-and-irregular-compute.md#explanation-dac-2026-research1242) and [LTMiner](../observed-subthemes/sparse-and-irregular-compute.md#explanation-dac-2026-research240) make request order and kept data explicit.

**Be careful:** these papers do not prove one best scheduler. They name competing costs a scheduler must count, for different computations, with source evidence still incomplete.

## Do not merge exact compression and approximation into one claim

"Preserving the answer" has at least three meanings, and proving one does not prove the others.

| Kind of preservation | What it means |
| --- | --- |
| Exact codec | Recovers exactly the bits it received |
| Exact arithmetic | Keeps the result defined for those bits |
| Application quality | Keeps an acceptable quality score, even if many outputs change |

Two examples:

- Compressing and exactly recovering the integer 7 says nothing about whether rounding the original real value to 7 was acceptable.
- Two generated videos can both score well on quality while showing different content.

So a speed claim must come with the benchmark's definition of quality.

[SPADE's manuscript-backed explanation](../observed-subthemes/sparse-and-irregular-compute.md#explanation-dac-2026-research680) shows why. Its standard and Turbo settings use different sparse-step schedules. The recovered table reports their timing and output fidelity separately. A higher perceptual-quality score does not show closer similarity to the dense reference. So this evidence cannot be squeezed into one claim of "faster, unchanged inference".

This is also why the taxonomy needs secondary links. Sparse attention may drop chosen interactions approximately. Bit-level sparsity may remove redundant digits exactly, within an integer format. Both sit under sparsity, but their correctness duties differ.

**Be careful:** navigation keeps the historical classifications. These conceptual links do not quietly reclassify records or count them twice.

## Three long-term hypotheses worth testing

These are bounded readings of the linked mechanisms, not accepted longitudinal findings. Each says what evidence would weaken it.

| Hypothesis | Why the mechanism could matter | Evidence that would weaken it |
| --- | --- | --- |
| Representation and scheduling increasingly need joint evaluation when arithmetic becomes a smaller cost | Fewer stored bits or indices can alter decoding, task size, and available parallelism | Matched workloads where decoding and coordination outweigh transfer savings, or where traffic was already insignificant |
| Fine-grained readiness helps primarily when broad synchronization hides substantial independent work | A task can start after its own inputs finish without waiting for unrelated tasks | Dependency chains that dominate runtime, too few ready tasks, or completion-notification cost exceeding removed waiting |
| Quality-constrained performance is more transferable than unconstrained peak speed for approximate methods | An application needs a usable result, not simply fewer executed operations | Gains disappearing at the required quality threshold or under shifted inputs, longer contexts, or different models |

Finding more papers with matching titles is not enough to test them. Within each application:

1. compare equivalent input sets, numerical requirements and hardware budgets;
2. measure the complete job, with the same boundaries;
3. report spreads and regressions, not only good averages;
4. across editions, use the same collection rules, and tell missing manuscripts apart from measured negative results.

**Be careful:** the current sample cannot show that ISCA, DAC or ICCAD leads a trend, or that a mechanism is growing. Conference identity is not an experimental control. A useful cross-conference link asks whether separately tested parts can meet one compatible set of requirements. A compiler result, an accelerator result and a layout result are separate evidence. They join up only when their interfaces, formats, sizes and test conditions match.

## What an end-to-end comparison must retain

A fast middle step speeds up the whole job only as much as the other steps allow.

> **Worked example.** A baseline job takes 100 milliseconds: 20 for preparation, 50 for accelerated computation, 30 for everything else.
>
> - Make the middle stage five times faster: `20 + 10 + 30 = 60` milliseconds, about **1.67×** overall.
> - Add 15 milliseconds of format conversion: 75 milliseconds, about **1.33×** overall.
> - Reusing preparation changes the comparison again, and must be reported.

So a connected account follows one input through preparation, conversion, execution, output handling and quality checking. It states:

- which steps are timed;
- which costs are reused;
- where bytes cross an interface;
- which failure conditions remain.

Faster arithmetic stays a component result until this accounting supports an application result.

The [precision-aware chapter](../observed-subthemes/approximate-and-precision-aware-compute.md) and [sparse/irregular chapter](../observed-subthemes/sparse-and-irregular-compute.md) now give expanded explanations for each of their papers. Other architecture branches below are still uneven in depth. This theme synthesis does not complete their rewrites, source recovery, classification reconciliation, or independent review.

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
