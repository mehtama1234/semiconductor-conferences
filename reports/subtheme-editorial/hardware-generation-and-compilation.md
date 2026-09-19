## A generator must produce a usable implementation

A hardware generator turns a description and configuration choices into a circuit implementation. Its value is not only that it emits code: the output must compute the intended result, fit the target's resources, and satisfy its operating requirements. Compilation and physical implementation introduce further choices and checks before the circuit's area, speed, or power can be assessed.

The selected paper, [FSGen](../observed-subthemes/hardware-generation-and-compilation.md#paper-dac-2026-research868), proposes a generator for fused, sparse language-model accelerators with a power model. The captured official description identifies the purpose but gives no generated-design measurements or detailed implementation procedure.

<span id="explanation-dac-2026-research868"></span>

## FSGen: how a generator makes fusion and sparsity searchable hardware choices

### The search space is part of the hardware method

An accelerator generator does not merely print RTL from a fixed template. It defines which dataflows, buffers, processing-element arrays, sparse networks, memory paths and control choices can be expressed. If a useful choice is absent from that representation, the design-space search cannot find it. If the representation permits an invalid combination, the search can spend effort on designs that cannot execute the workload correctly.

FSGen targets attention-based LLM accelerators. Its high-level input specifies the attention type, fused operator dataflow, loop order, tilings, intermediate-tensor cache sizes and sparsity mappings. The generator maps those choices to Chisel RTL, a compiler converts LLM layers into executable kernels, and testbenches support kernel and multi-kernel simulation. The paper evaluates the generated designs under fixed implementation conditions rather than treating a high-level score as the final result.

### Fusion changes the lifetime of intermediate tensors

Attention contains a sequence of dependent operations. In multi-head attention, the score calculation forms a product of queries and keys, softmax transforms the score, and a later product combines the result with values. In notation used by the paper:

`S1: S = Q × K;  S2: P = softmax(S);  S3: O = V × P + x`

When these operations are executed separately, an intermediate tensor may be written to memory and read back. A fused dataflow passes an intermediate directly between processing arrays or keeps it in a local buffer. This can reduce memory traffic, but the producer and consumer must agree on tile shapes, rates, ordering and completion. A larger fused unit can also require more local storage and more complicated control.

FSGen represents fused operators as multiple loop nests sharing iterators. It supports attention, feed-forward networks, KV-cache generation and normalization. It distinguishes prefill, where many input tokens are processed, from decode, where one new token reads prior keys and values from the KV cache. The generated design can reconfigure between these modes. Its softmax path uses online softmax to reduce the need for a large input cache.

The paper adds heterogeneous tiling: downstream arrays can use smaller tiles when their required bandwidth remains below the upstream bandwidth. It also uses multi-tensor caching so that hits for queries and keys can allow upstream work to be skipped. These are not universal fusion benefits; they depend on cache capacity, tile alignment, token length and whether the next operation can consume data at the produced rate.

### Sparsity has a condition, a location and a mapping

Sparse computation is not defined only by a percentage of zeros. A sparse rule identifies which tensor elements or groups are absent, and the hardware must implement that rule at a particular point. FSGen represents a sparse set as mappings from tensor iterators to Boolean conditions. A mapping can be value-based when individual iterator points decide whether work is skipped, or group-based when a group of points is selected together.

The framework separates three locations. Compute-based sparsity selects values before they enter a processing-element array. Memory-based sparsity changes what the DMA or memory system stores and transfers. Group-based sparsity selects a coarser unit and can reduce metadata or routing complexity at the cost of skipping less precisely. The same sparsity condition can lead to different hardware depending on where it is applied.

FSGen’s sparse hardware has a two-level network. A group-level network selects a coarse tensor group, and a value-level network selects fine-grained values within that group. Tilings describe the physical sub-tile, physical tile, virtual tile and virtual group tile. The mapping is then translated into crossbar or multicast parameters such as copy, group count, fan-in, fan-out and port counts.

This explicit mapping is the important design step. A sparse algorithm can reduce arithmetic while increasing selection logic, crossbar power, metadata movement or load imbalance. The generated accelerator must therefore be evaluated on the complete dataflow, not on the nominal number of nonzero operations.

### Hardware generation exposes the consequences of the choices

The generator determines processing-element arrays from the dataflow, inserts queues between arrays and pipelines for fused operation, sizes memory arrays to hold a virtual tile per cycle, and creates sparse networks from the selected mappings. Memory-based sparsity modifies the DMA finite-state-machine controller. The top-level module exposes an AXI programming interface.

The software side reads an LLM model, loads weights and converts each layer into executable kernels. Kernel-level simulation can test attention or feed-forward operations, while full-layer simulation runs multiple kernels. The paper reports generation of attention-based LLM accelerator core RTL rather than a fabricated accelerator. RTL generation and gate-level analysis are therefore separate evidence stages: a generated module can be structurally valid while still failing timing, power or workload correctness checks.

### Early power estimation is built from primitives

Full synthesis and power analysis for every design in a large space is too slow for early exploration. FSGen models power from primitives: processing elements, arithmetic units, exponent units, sparse networks, systolic pipelines, SRAM banks and registers. For each primitive, an XGBoost model predicts power from the primitive type, parameters, signal toggle activity and zero-bit count.

The activity features are produced by an early cycle-accurate architectural simulator. The simulator samples the executed dataflow and counts bit-level toggles and zero values per cycle. This is more informative than assigning one constant power per operation because a sparse network, a switching pattern and an all-zero path can have different costs.

The primitive model is trained from post-synthesis power labels. Each primitive has about 256 training points; collecting one primitive training set takes about 30 minutes and training takes seconds. Validation uses about 20 dense and 200 sparse FSGen designs with varied dataflows, sparsity sets and tilings. The paper reports 12.8% power error and correlation R = 0.97 for its model, compared with MAPE values of 61.6% for a Maestro-like model, 45.5% for an Accelergy-like model and 56.2% for a top-level ML regressor in the plotted comparison.

The model’s accuracy is conditional on the primitive inventory, post-synthesis labels, activity simulator and hardware implementation assumptions. A good power estimate does not establish that a generated design is functionally correct or that its full-chip power is captured outside the modeled primitives.

### The evaluation fixes a concrete comparison boundary

The experiments use Bert-Large and Llama models with multi-head attention, and Mistral and Qwen3-small with group-query attention. Both prefill and decode stages are evaluated across token lengths. Chisel generates Verilog RTL. Synopsys Design Compiler performs synthesis and area estimation for TSMC 40 nm; PrimeTime and PTPX provide power and timing analysis; VCS performs gate simulation.

The design-space sweep combines three loop orders, eight tilings, two compute-value, two compute-group and four memory-based sparsity mappings, for 768 FSGen designs. BinaryLLM and Stellar are configured by their dataflow representations and yield 12 and 20 distinct dataflows respectively. The comparison fixes INT8 inference, 8 GB/s off-chip memory, at most 16 KB per tensor, at most 8 TOPS and a 1 GHz clock. These conditions define what the reported PPA numbers mean.

### The reported designs show different tradeoffs

Table 1 reports tokens per second, area, power, clock frequency, utilization and a figure of merit defined as tokens/s divided by power and area. Prior BinaryLLM is listed at 1.9 tokens/s, 19.3 mm² and 2,120 mW, with FoM 0.05. Stellar is listed at 1.8 tokens/s, 10.4 mm² and 1,130 mW, with FoM 0.15. FSGen designs D1–D4 report:

- D1: 2.3 tokens/s, 3.58 mm², 374 mW, 812 MHz, 93% utilization, FoM 1.7.
- D2: 10 tokens/s, 3.60 mm², 377 mW, 712 MHz, 71% utilization, FoM 7.3.
- D3: 22 tokens/s, 4.79 mm², 509 mW, 823 MHz, 39% utilization, FoM 9.0.
- D4: 23 tokens/s, 7.08 mm², 763 mW, 811 MHz, 39% utilization, FoM 4.2.

The designs illustrate why a single metric is inadequate. D3 has the highest listed FoM, while D4 is slightly faster but uses more area and power. D1 has the highest utilization and the lowest power among FSGen designs but much lower throughput. The paper reports up to 120k tokens/s in prefill and up to 110 tokens/s in decode for selected configurations; these are different workload stages and should not be compared as one throughput number.

### The DSE comparisons support conditional claims

At a 700 mW constraint, FSGen reports up to 10× better performance than the comparison designs. At the same 8×10^7-cycle count, it reports 1.4× better power. The paper attributes the improvement to a larger fused/sparse design space, including compute-group and memory-based sparsity mappings that earlier generators support less broadly.

The comparison is meaningful under the fixed memory, precision, clock, area and workload rules. It does not establish that FSGen always beats a hand-optimized accelerator, because the baselines have different supported spaces and the selected design points may not share identical operator coverage. The figure of merit also combines throughput, power and area; a deployment decision still needs separate constraints for each resource.

### What the generator establishes and what remains conditional

FSGen provides a concrete end-to-end accelerator-generation method: represent fused loop chains and sparse conditions, map them to configurable hardware networks, emit RTL and compiler support, estimate power from primitive activity features, and search a 768-design space under fixed implementation constraints. The manuscript supports the reported improvements in selected throughput, PPA, FoM and early-stage power-model error over the listed baselines.

It does not establish silicon results, unrestricted support for arbitrary LLM operators, correctness of every sparse/fused configuration, or universal speedup independent of token length, sparsity distribution, memory bandwidth, precision and technology. The 12.8% power error is a model error on the paper’s validation set, not an error bound for every generated accelerator. The repository was not executed here, and the RTL, compiler, synthesis, gate simulation and PTPX runs were not independently reproduced.

**Primary source read:** [FSGen arXiv version 1](https://arxiv.org/abs/2608.09252), Sections 3–7 and Figures 2–10/Table 1, PDF pages 2–7, including fused-operator and sparsity representations, hardware mapping, Chisel generation, primitive XGBoost power models, 768-design sweep, fixed 40 nm/INT8 evaluation conditions and PPA/DSE results; [official DAC record](https://63dac.conference-program.com/presentation/?id=RESEARCH868&sess=sess156). The manuscript was read; the RTL generation, synthesis, gate simulation and power runs were not reproduced here.

## Fusion changes where intermediate results live

A computation often contains several dependent operations. Executing them separately can require writing an intermediate result to memory and reading it again. Fusion combines processing so that some intermediate values may be consumed closer to where they are produced.

The possible saving is reduced movement and storage of those values. The cost can include more complicated scheduling, additional local buffering, or a mismatch between the rates at which operations produce and consume data. Fusion is therefore not automatically beneficial for every operation pair or input size.

FSGen's description does not specify which operations can be fused, the buffering scheme, or the generated interfaces. It would be unjustified to assume that every supported fusion avoids all external-memory traffic or preserves performance across arbitrary language-model configurations. Those capabilities require explicit generator rules and evaluated outputs.

## Sparsity changes the representation as well as arithmetic

Sparse data contains many zero values. Skipping work associated with those zeros can reduce arithmetic, but the implementation also needs to identify and locate the retained values. Their positions can require metadata, and uneven distributions can leave some processing resources idle while others remain busy.

A generator must match these properties to a supported data format and execution schedule. Structured sparsity and irregular sparsity create different implementation choices. The captured record does not identify the format, sparsity patterns, workloads, or accuracy conditions used by FSGen, so no particular skipping mechanism can be attributed to it.

Fusion and sparsity can interact. A fused consumer may need values in an order that the sparse producer does not naturally supply. Any rearrangement and buffering belongs in the complete cost, rather than disappearing from an arithmetic-operation count. This is a design question raised by the proposal, not a demonstrated failure of its implementation.

## A power model helps only if its estimates support the decision

The title describes an accurate power model. Such a model estimates power for candidate implementations under specified activity and technology assumptions. Its usefulness depends on what it includes: arithmetic units, memory, control, communication, and any other components inside the stated measurement boundary.

Power and energy are different quantities. Power is the rate of energy use; completing a task's energy accounting also requires its duration. A candidate with lower estimated power can consume more energy if it takes sufficiently longer. Conversely, a faster design may require a higher instantaneous power budget.

The source supplies no calibration method, power error, technology, activity traces, or complete generated-system measurements. “Accurate” must therefore remain an author claim rather than an independently established error bound. Evaluation should inspect both prediction error and whether the model correctly ranks candidates near the design decision.

## What an end-to-end generator evaluation requires

A useful experiment would fix the language-model task, numerical requirements, hardware target, and memory assumptions. It would then generate several configurations, check their functionality, carry them through the stated implementation flow, and report area, timing, power, and complete execution performance.

Generation time and manual intervention also matter. A reusable generator may require substantial setup, while an individual output may still need repairs. Those costs should be separated and recorded. Failed or unsupported configurations should remain visible rather than being omitted from the apparent coverage of the tool.

FSGen motivates jointly selecting fusion, sparse execution, and resource costs during hardware generation. The present description does not establish a complete language-model accelerator result, a silicon measurement, or a validated replacement for hand design. Its longer-term research question is whether automated choices remain advantageous after all data movement, correctness checks, and physical implementation costs are included.
