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
