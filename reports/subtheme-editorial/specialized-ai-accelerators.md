## Specialization starts by identifying which work can change

An accelerator is useful when it makes a particular computation cheaper while preserving the output conditions that matter. It can do this by moving less data, reusing previous work, changing numerical precision, or expressing the computation in a form that existing hardware executes efficiently. These are different interventions. They require different correctness checks and should not be ranked using one headline number.

The nine papers in this subject cover graph learning, language-model arithmetic, image generation, distance computation, and scene rendering. Four full manuscripts were recovered in this pass. Five papers remain description-backed; missing experiments are not supplied from their titles. Source locations below refer to the inspected versions, whose equality with final publisher versions has not been established.

| Intervention | Papers | Main condition to test |
|---|---|---|
| Reuse or reorganize graph work | DIA-CIM, TDH-GNN, HDGAS | Dependencies, graph changes, and prediction quality |
| Reduce arithmetic cost | FuseDot, DSPE | Effective numerical values, rounding, and approximation error |
| Assign precision by region | MASQ | Image quality across masks and denoising steps |
| Change distance representation | STEM-CAM | Supported precision, metric order, and device variation |
| Reformulate rendering | GEMM-GS, geometry-guided CODA | Visibility, image quality, and the complete rendering path |

A hardware operation count is not a completed application count. Removing multiplications can add sorting, indexing, or decoding. Keeping partial results close to arithmetic can save transfers but consume storage. A method that skips work must also pay to determine what can be skipped. These costs belong in the comparison.

## Graph learning: dependencies determine what can run together

A graph represents entities as nodes and relationships as edges. Each node can hold a feature vector: a list of numerical attributes. Graph learning combines information along edges to update those features or make predictions. The edges determine which values are needed, so memory access is usually less regular than reading a dense rectangular array.

There are two different meanings of “dynamic” here. A graph can change between observations, or an algorithm can update node states sequentially during one computation. The first creates opportunities to reuse unaffected results. The second creates dependencies on newly computed values. Treating them as the same problem hides the reason an architecture helps.

<span id="explanation-dac-2026-research1194"></span>

### DIA-CIM: dynamic graph aggregation must preserve dependencies while exploiting sparse work

#### What dynamic iterative aggregation computes

A graph neural network updates a node by combining information from connected nodes. In a dynamic iterative model, the update may use newly computed states during the same broader computation, extending the receptive field without materializing every full dense layer. This changes the hardware problem: the accelerator must follow data dependencies while handling irregular edge addresses and uneven numbers of active neighbors.

The operation count is therefore not determined only by the number of graph edges. It depends on the update rule, iteration order, stopping condition, feature precision and whether the algorithm reuses or recomputes partial results. A hardware comparison must hold those algorithmic conditions fixed before attributing a gain to the accelerator.

#### What the dataflow contributes

Compressed sparse row (CSR) storage records nonzero edge values and the start of each row. Streaming CSR edges can avoid reading explicit zeros and can provide a regular sequence of metadata for the hardware. It cannot remove a dependency on a newly updated neighbor. If the next update needs that value, the scheduler must wait, buffer the partial state, or use a mathematically equivalent approximation.

Output-stationary processing keeps an unfinished node result near the arithmetic while contributing edges are consumed. This can reduce repeated writes and transfers, but local storage must hold partial sums and the accumulation order can affect numerical results. Sparse traffic can also leave compute units idle when rows have different lengths.

#### What BF16 bit/value sparsity means

The reported BF16 pipeline exploits zero values and bit patterns. Exact zero skipping can remove work without changing the result. Bit-pattern shortcuts may change how arithmetic is performed and therefore require a numerical error analysis. The evaluation must state whether values are rounded, approximated or skipped, and must report the resulting GNN accuracy under the same graph and stopping rule.

#### How to interpret the efficiency claims

The official description reports an author-reported fabricated 28 nm CMOS macro, 60.01 TFLOPS/W, more than 3.56× lower energy and more than 2.32× lower latency. Those figures are meaningful only with the graph suite, feature dimensions, iteration count, operation-count convention, macro area, ADC/DAC and peripheral power, clock, process conditions and baseline normalization. TFLOPS/W can increase when the counted operation definition changes; it is not by itself application energy.

The complete comparison must include graph preparation, CSR construction, indexing, data movement, partial-sum storage, control, convergence checks and the work performed by the baseline. It must also show that the same output quality is reached. A fabricated macro supports stronger evidence than a simulation, but it does not remove the need to state the measurement boundary.

#### What the evidence establishes and where it stops

The captured record supports a dynamic iterative GNN co-design with CSR streaming, output-stationary accumulation and BF16 sparsity-aware processing, plus the reported fabricated-macro efficiency claims. It does not expose the graph suite, accuracy, operation accounting, area, peripheral power or full application boundary. The evidence supports a silicon direction, not a general GNN efficiency or accuracy result.

[Observed paper card](../observed-subthemes/specialized-ai-accelerators.md#paper-dac-2026-research1194)

### DIA-CIM: retain partial results while following sequential updates

[DIA-CIM](../observed-subthemes/specialized-ai-accelerators.md#paper-dac-2026-research1194) supports sequential, asynchronous aggregation. Its description specifies compressed-sparse-row-driven processing, local partial sums, and a BF16 pipeline that exploits zero values and bit patterns. It reports fabricated 28 nm CMOS, 60.01 TFLOPS/W, and workload energy/latency improvements exceeding 3.56×/2.32×. Dataset, accuracy, operation-count convention, and power boundary remain unspecified. Fabrication is an author report here; no manuscript measurement table was recovered. [Official DAC description](https://63dac.conference-program.com/presentation/?id=RESEARCH1194&sess=sess123).

Compressed sparse row storage records nonzero entries and where each row starts. Output-stationary processing keeps an unfinished output near the arithmetic until its contributing inputs have been processed. Neither technique removes a true dependency: an update that needs a newly computed neighbor value must still wait for it. The appropriate test must hold the update rule and stopping condition fixed, or separate algorithmic quality changes from hardware savings.

<span id="explanation-dac-2026-research032"></span>

### TDH-GNN: incremental metapath reuse is valid only when all affected dependencies are tracked

#### What changes in a dynamic heterogeneous graph

A heterogeneous graph has multiple node and edge types. A metapath is a typed sequence, such as author–paper–author, and a metapath instance is one concrete sequence of connected nodes that follows those types. A graph update can add, remove or modify an edge. That change may create or invalidate many instances, including instances whose endpoints were not directly edited.

Recomputing every metapath after every update is expensive. Incremental processing tries to identify the affected instances, update only those structures, and reuse results for unaffected parts. The correctness condition is stronger than “the edge did not change”: the features, weights, type constraints and all dependencies used by a cached result must still be valid.

#### What the hyperedge structure and cache do

The recovered TDH-GNN method stores metapath instances in a hyperedge-based structure and maintains them incrementally. A hyperedge can represent a higher-order relationship among the nodes in one metapath instance rather than treating every pairwise edge as an independent result. Frequency-aware caching prioritizes relationships or instances that are reused often.

The structure must support invalidation. When an edge or feature changes, the system needs to find every stored instance that depends on it, remove or update those entries, and prevent a stale cached embedding from reaching the next layer. A concentrated update can invalidate a large fraction of the cache; the overhead of finding and repairing invalid entries can outweigh the saved recomputation.

#### What the manuscript evaluation compares

Section 4 evaluates DHNE, THINE and DyHNet with three layers and 128 hidden dimensions on Yelp, Aminer, DBLP, IMDB and OAG temporal datasets. The reported accelerator uses a U280 FPGA at 220 MHz. Average speedups of 4.3× and 2.8× are mapped to HiHGNN and GDR-HGNN; energy ratios are 5.9× and 3.7×. Table 2 assigns those comparator configurations 1 GHz and the same 4,096 MAC count, so the values are not measurements on identical hardware.

This distinction matters. A speedup can come from reusing less work, a different clock, a different memory system, a different operation count, or a combination. The comparison must also preserve the same graph updates, model outputs, training/inference task, feature values and convergence or prediction criterion.

#### What correctness and energy validation require

For each update pattern, compare incrementally maintained metapaths and embeddings with a fresh recomputation. Include random, bursty, concentrated and adversarial updates, and report the fraction of instances invalidated. Prediction-equivalence checks should state numerical tolerance and task-level accuracy.

Energy measurement must state whether it includes FPGA board power, HBM, host transfers, preprocessing, update detection, cache maintenance and baseline software. The recovered manuscript leaves the exact energy procedure and prediction-equivalence checks insufficiently specified for independent reproduction.

#### What the evidence establishes and where it stops

The institutional manuscript supports topology-driven incremental maintenance, hyperedge indexing, frequency-aware caching, the stated five-dataset evaluation and the reported comparator mappings. It does not establish that reuse remains beneficial for all update distributions, that cached predictions are equivalent under a declared tolerance, or that the energy ratios are normalized measurements on equivalent systems.

[Observed paper card](../observed-subthemes/specialized-ai-accelerators.md#paper-dac-2026-research032)

### TDH-GNN: update the affected relationships instead of rebuilding all of them

A heterogeneous graph contains different node or relationship types. A metapath specifies a sequence of types, such as author–paper–author; an instance is a concrete sequence of connected nodes matching it. One changed edge can affect many such instances, while leaving others unchanged.

[TDH-GNN](../observed-subthemes/specialized-ai-accelerators.md#paper-dac-2026-research032) stores metapath instances in a hyperedge-based structure and incrementally maintains them, with frequency-aware caching. Section 4 evaluates DHNE, THINE, and DyHNet, each with three layers and 128 hidden dimensions, on five temporal datasets. Its U280 FPGA runs at 220 MHz. Average speedups of 4.3×/2.8× correspond to HiHGNN/GDR-HGNN; energy ratios are 5.9×/3.7×. Table 2 gives those comparators 1 GHz and the same 4,096 MAC count, not identical hardware. [Institutional manuscript, Sections 3–4, PDF pages 4–6, Tables 1–2 and Figures 6–8](https://wrap.warwick.ac.uk/id/eprint/200587/1/dcs-090526-wrap-tdh-gnn_camera_ready.pdf#page=5).

Reusing a result requires more than finding an unchanged edge: the features, weights, and relevant dependencies must also permit reuse. A useful stress test varies the fraction and distribution of updates, including concentrated changes that invalidate many metapaths. The inspected evaluation leaves the exact energy-measurement procedure and prediction-equivalence checks insufficiently explained for independent reproduction.

<span id="explanation-dac-2026-research052"></span>

### HDGAS: learned feature removal saves graph work only when the discarded information is shown to be unnecessary

#### What the graph-learning computation contains

A graph-learning layer combines a feature vector with information from related nodes. If a graph has (N) nodes and each node has (F) feature values, a dense feature operation can expose roughly (N \times F) values to the next computation, before accounting for the edges and the model's weights. A sparse implementation can avoid some of those values, but it must still determine which values exist, locate their destinations, and combine them with the correct neighbors.

The HDGAS description treats feature selection and graph acceleration as one problem. The filter decides which feature components to keep, and the remaining computation is mapped to sparse matrix multiplication. This is not equivalent to running the original model faster. The filter changes the input seen by the graph model, so the resulting predictions can change even when the sparse multiplication is exact.

#### What a learned feature filter does

Let (x) be a node's feature vector and let (m) be a mask whose entries are zero or one. The filtered input is (x' = m \odot x), where (\odot) denotes element-by-element multiplication. A feature is removed when its mask entry is zero. If the mask is produced from the current data, the hardware or software also pays to compute the mask and to decide how the selected values are represented.

The claimed benefit exists only when the work avoided by using (x') exceeds the cost of producing (m), moving the selected values, storing their positions, and handling the resulting irregular pattern. If the filter is trained jointly with the graph model, the model may learn to depend on the distribution of retained features. A mask that works on training graphs can remove information needed on a new graph or under a shifted feature distribution. The filter therefore belongs inside the accuracy and latency boundary, not outside it as free preprocessing.

#### What sparse matrix multiplication adds

Sparse multiplication stores nonzero or retained values together with metadata such as column indices, row boundaries, masks or compressed offsets. The arithmetic unit can skip absent values, but the memory system must read the metadata and route each value to the right partial result. Uneven sparsity creates load imbalance: one processing unit can finish early while another still handles a long row or a dense region.

The useful quantity is not only the retained-feature fraction. It is the total work and data movement after selection. A filter that retains 25% of the feature values does not necessarily reduce total traffic to 25% if indices, masks, padding, gathers, reductions and output writes are large. The comparison must count dense baseline work, filter inference, mask transfer, sparse-format construction, sparse multiplication, accumulation and result movement.

#### What the reported comparison does and does not identify

The refreshed official description assigns 6.76× speedup and 7.58× energy efficiency to comparisons with GNN accelerators. It assigns 69.31× speedup and 80.12× energy efficiency to a GPU comparison. These are different comparator groups; they must not be combined into one universal ratio. The captured description does not identify the exact accelerator or GPU models, graph datasets, feature dimensions, retained-feature fractions, hardware implementation stage, clock, memory system, absolute latency, power boundary or prediction-quality change.

A fair result would report a curve over retained-feature fractions and graph workloads. For every point, it would show filter cost, sparse arithmetic cost, total latency, total energy, memory traffic and graph-learning quality. The baseline would use the same model, graph, feature values, training or inference task and stopping rule. Reporting only a ratio against an unnamed baseline cannot show whether the gain comes from feature removal, a different implementation boundary or a change in the task.

#### What correctness and robustness require

The first check is output quality. Compare the filtered model with the unfiltered reference using node classification, link prediction or the task actually evaluated, and state whether the mask is fixed, input-dependent, trained once or updated at runtime. Report accuracy, loss or another task metric at each sparsity level, including worst-case or distribution-shifted graphs when the filter is input-dependent.

The second check is selection correctness. The accelerator must preserve the association between each retained feature, its node, its graph neighborhood and its model weight. Index errors can produce a fast but different graph computation. The test should compare sparse outputs with a dense reference under a declared numerical tolerance before comparing final predictions.

The evidence establishes a joint feature-selection and sparse-acceleration direction and the refreshed mapping of headline ratios to comparator classes. It does not establish a particular hardware implementation, quality-preserving sparsity level, generalization under graph shift or end-to-end energy advantage. The missing conditions are part of the result, not details that can be inferred from the word “brain-like.”

[Observed paper card](../observed-subthemes/specialized-ai-accelerators.md#paper-dac-2026-research052)

### HDGAS: selecting fewer features changes the learning computation

Hyperdimensional computing represents information using long vectors and relatively simple operations over them. The word “brain-like” in a title does not establish biological fidelity, spiking execution, or a neuromorphic chip.

[HDGAS](../observed-subthemes/specialized-ai-accelerators.md#paper-dac-2026-research052) jointly optimizes a filter and graph-learning model to remove less important features at runtime, then accelerates sparse matrix multiplication. The refreshed description maps 6.76× speedup and 7.58× energy efficiency to GNN accelerators; 69.31× and 80.12× refer to a GPU. The old card's ambiguity about that mapping is corrected. Specific devices, datasets, and quality changes remain missing. [Official DAC description](https://63dac.conference-program.com/presentation/?id=RESEARCH052&sess=sess120).

Feature removal is not merely a faster schedule for an unchanged calculation. The filter can discard useful information, particularly when deployment data differ from training data. Evaluation should count filter cost and report predictive quality at each retained-feature fraction. Sparse storage also needs indices; fewer feature values do not imply an equal reduction in total bytes.

## Language-model arithmetic: equal codes, equal values, and similar values differ

A dot product multiplies corresponding entries of two vectors and adds the products. Quantization represents values with a smaller set of numerical codes, often with a scale attached to a group of codes. This reduces storage and can simplify arithmetic, but the code alone does not necessarily identify the effective value.

<span id="explanation-dac-2026-research1182"></span>

### FuseDot: multiplier sharing helps only when quantized values and reordering costs are controlled

#### What the dot product computes

A dot product multiplies corresponding entries of an activation vector and a weight vector, then adds the products. In the reported setting, activations are FP16 and weights are INT4 or another low-bit representation with scale information. The integer code is not necessarily the full numerical value: a group scale, zero point or packing rule determines how the code becomes an effective weight.

The opportunity behind multiplication fusion is simple in exact arithmetic. If the same effective weight multiplies several activations, `w×a + w×b` can be evaluated as `w×(a+b)`. One multiplication is replaced by an addition and the result can be shared. The equality must hold after dequantization and under the accumulator's precision; equal four-bit codes in differently scaled groups may not be equal weights.

#### What MFDP adds to the data path

The captured MFDP design uses index-driven generalized matrix multiplication, hierarchical dual-phase reordering and multiplier sharing across processing elements. The indices identify compatible weight work. Reordering places compatible operations together so that a multiplier can be reused instead of independently computing every product.

This changes the workload rather than making the original workload disappear for free. Indices and group metadata must be stored and read. Reordering costs control work, movement and buffering. Irregular group sizes can leave processing elements idle, while synchronizing shared products can add coordination. A valid comparison must measure these costs as part of the matrix operation.

#### Why numerical correctness needs its own test

Reassociating additions can change rounding. INT4 dequantization, FP16 products, accumulator width, saturation and truncation determine whether the fused result matches the unfused result. The evaluation should compare tensor outputs, layer error and final LLM quality under the same scales, sequence lengths and quantization rules. A multiplier-count reduction is not a correctness result.

#### How to read the reported performance range

The official description reports 1.51–1.98× speedup and 1.19–1.51× energy-efficiency improvement over unnamed accelerator baselines. The captured sources do not expose the model suite, layer shapes, sequence lengths, batch sizes, frequency, area, memory traffic, compiler mapping, absolute latency, power boundary or variance. The ranges therefore identify a reported performance claim, not a reproducible general LLM result.

The end-to-end comparison must include weight unpacking and dequantization, index construction, reordering, memory traffic, accumulation, output movement and the layers that do not benefit from shared weights. It must also state whether energy includes only the specialized datapath or the full accelerator and memory system.

#### What the evidence establishes and where it stops

The captured record supports multiplication fusion through indexed grouping, reordering and cross-processing-element sharing for low-bit LLM inference. It does not establish that equal codes are equal effective weights in all groups, that accuracy is preserved, or that the reported speed and energy ranges transfer across models and hardware.

[Observed paper card](../observed-subthemes/specialized-ai-accelerators.md#paper-dac-2026-research1182)

### FuseDot: combine repeated-weight multiplications

[FuseDot](../observed-subthemes/specialized-ai-accelerators.md#paper-dac-2026-research1182) groups identical-weight work using indexed matrix processing, reordering, and multiplier sharing. Its description reports 1.51–1.98× speedup and 1.19–1.51× energy-efficiency improvement over unnamed accelerators. The [existing recovery assessment](../../dac/data/fusedot-primary-recovery-v1.json) still applies: a full manuscript and artifact were not recovered, and headline conditions remain unresolved. [Official DAC description](https://63dac.conference-program.com/presentation/?id=RESEARCH1182&sess=sess156).

In real arithmetic, `w × a + w × b = w × (a + b)`. This exchanges one multiplication for a different addition order. It is useful only if finding and grouping repeated weights costs less than the saved work. Equal four-bit codes in groups with different scales need not be equal effective weights. Finite-precision arithmetic also makes reassociation potentially change rounding. These are verification requirements, not claims that FuseDot fails them.

<span id="explanation-dac-2026-research1206"></span>

### DSPE: reduce repeated edge inference work, while keeping approximation and security claims separate

#### The paper combines three different reductions

[DSPE](../observed-subthemes/specialized-ai-accelerators.md#paper-dac-2026-research1206) targets edge inference for DeepSeek-V3, whose attention, KV-cache access, sparse experts, and large linear layers create different costs. It combines three mechanisms that should be evaluated separately. MIPS tries to reuse results for similar vectors and KV-cache patterns. MBLM skips or shortens multiplication work when operands are near zero or have repeated bit patterns. DAPPM changes the numeric representation and multiplier path through a dynamic adaptive Posit format.

These mechanisms reduce different resources. MIPS targets memory access and repeated vector computation. MBLM targets partial products and bit transitions in Booth multiplication. DAPPM targets representation width and multiplier activity. A single energy-efficiency number combines all three, the memory system, and the synthesized datapath; it does not identify which mechanism produced the gain.

#### MIPS uses approximate similarity decisions, not a cryptographic proof

During decoding, new query vectors attend to a growing KV cache. Adjacent inputs may be similar, so MIPS incrementally reorders vectors by cosine similarity, caches scores in Cos-SRAM, projects vectors into a compact space, and builds a Merkle-like hash hierarchy using locality-sensitive hashing. At each tree level it compares the current intermediate hash with a historical reference for the same expert.

The thresholds create three paths. A very small hash difference triggers early skip and reuses a KV-cache index/result. An intermediate difference can hit a history lookup table and reuse a previously computed differential result. A large difference, or a missing lookup entry, takes the full-compute path and records a new result. The paper reports 33.5% lower DRAM access and 36.2% lower SRAM access on DeepSeek-V3/MMLU under its setup.

The term Merkle tree describes hierarchical hash construction, but the reuse decision is governed by locality-sensitive hashing and thresholds. A locality-sensitive hash is designed to map similar inputs to related values; it can intentionally collide. That is different from a cryptographic integrity check, which requires a trusted reference, collision resistance for the claimed threat model, and a defined response to mismatch. MIPS therefore needs approximation error, false-reuse, false-full-compute, and output-quality measurements before “secure” can be treated as a security result. The paper's offline root-hash recomputation interface is a proposed consistency check, not an already reported security evaluation.

#### MBLM changes the Booth path using observed bit patterns

MBLM first marks a multiplication invalid when the weight or activation is below configured near-zero thresholds. It then measures bit variation between adjacent operand requests and the length of repeated fragments. A Bayesian model produces low/high redundancy probabilities and a redundancy score. Below 0.8 it selects radix-4 Booth encoding; above 0.8 it selects an extended radix-8 path. A variation-simplified triangle removes duplicate pair counting and self-pairs, and a small Booth lookup stores prior bit-flip patterns for reuse.

This is approximate in two independent ways: near-zero products are dropped, and repeated/related encodings are reused. The thresholds determine the numerical error and depend on the input distribution. The reported 39.1% calculation reduction on DeepSeek-V3/MMLU is a reduction in the paper's operation accounting, not automatically a 39.1% latency or energy reduction. Lookup, classification, reordering, comparator, and memory costs must be included.

#### DAPPM changes the representation, not just the multiplier

Posit numbers encode sign, regime, exponent and fraction. DSPE's DA-Posit treats the lower exponent/fraction bits as a dynamic field. When low-order patterns are shared, one- or two-bit compression folds those bits while preserving scale information in the regime. Reused boundary regime codes indicate whether no, one-bit, or two-bit compression is active without adding an external mode field.

The hardware decodes sign, regime, exponent and dynamic field, chooses a 16-, 9-, or 4-PE multiplier path based on the mode, accumulates partial products, normalizes, and re-encodes. The manuscript reports 1.47× computation speed on DeepSeek-V3/MMLU with the same computational accuracy under its evaluation. “Same accuracy” needs the actual task metric, tolerance, and comparison protocol; representation restoration is not proof that the complete model output is unchanged.

#### What is actually synthesized

The DSPE implementation uses four attention cores, each with 64 processing elements, input/output buffers, a 24 KB parameter buffer, a 48 KB weight buffer, and dedicated query/key/value SRAMs. Synopsys Design Compiler and IC Compiler are used with a 28 nm CMOS target. The reported placed-and-routed area is 8.23 mm², supply range is 0.6–1.1 V, maximum frequency is 710 MHz at 1.10 V, power is 122–345 mW, and peak performance is 22.8 TFLOPS at POSIT8. The peak energy-efficiency point is 109.4 TFLOPS/W at POSIT8, 0.6 V and 200 MHz.

These are implementation and synthesis results for the processor design. They are not measurements of a fabricated chip running the full DeepSeek-V3 model. They also do not automatically include external DRAM, host orchestration, inter-core communication, model weights, KV-cache capacity, or distributed expert placement. The paper's table compares several processor entries with mismatched citation labels; its H100 reference [1] is a DeepSeek paper. The manuscript's 109.4 figure also differs from the captured description's 91.7 figure, so the manuscript value and source condition must stay explicit.

#### What the paper establishes and what remains open

DSPE establishes a synthesized 28 nm edge-oriented datapath that combines similarity-based reuse, approximate Booth processing, and adaptive Posit arithmetic, with reported local memory-access, operation-reduction, speed, area, and energy-efficiency results under the paper's conditions. It does not establish cryptographic security, exact inference equivalence, complete DeepSeek deployment, universal MMLU accuracy preservation, or measured fabricated-silicon energy. A stronger evaluation would report full-model end-to-end latency and quality, false-reuse rates, threshold sensitivity, adversarial hash inputs, model-weight/KV-cache storage and traffic, post-layout power under representative workloads, and matched baselines with corrected source labels. [Version-1 manuscript, Sections 2–4, PDF pages 3–7, Table 1](https://arxiv.org/pdf/2605.08615v1#page=6)

<span id="explanation-dac-2026-research1307"></span>

## MASQ: assign precision by spatial and semantic influence in masked diffusion

### The mask does not define the full computation boundary

Masked diffusion edits a selected image region through repeated denoising. The visible mask identifies where new content is requested, but it does not identify every feature that can affect that content. Convolution spreads influence to nearby positions through receptive fields. Self-attention can connect a masked token to a distant unmasked token. Recomputing the entire feature tensor preserves these dependencies, but it also spends high-precision work on regions that change little.

[MASQ](../observed-subthemes/specialized-ai-accelerators.md#paper-dac-2026-research1307) reduces this cost without simply dropping unmasked computation. It keeps all regions in the calculation but assigns MXINT8, MXINT4, or MXINT2 according to estimated importance. The masked region remains at high precision; nearby regions receive intermediate precision; distant or weakly related regions receive lower precision. This is an approximation scheme with dependency-aware precision, not exact region skipping.

### Spatial importance follows receptive fields

The method constructs a four-stage mask. Stage 3 is the user mask. Stage 2 dilates it according to the number of 3×3 convolution layers at the current U-Net resolution. Stage 1 accounts for influence from the next lower-resolution feature map, where downsampling changes how many tokens correspond to the same input area. Stage 0 contains the remaining positions. The dilation is statically derived from the U-Net structure, so the precision map reflects the model's convolutional path rather than an arbitrary pixel distance.

This boundary is important. A low-precision value just outside the user mask can enter a convolution window that also contains high-precision masked values. Quantization error can then cross the boundary. Increasing the high-precision region reduces that risk but reduces the amount of low-cost work. The relevant parameter is receptive-field distance, not only the percentage of pixels masked.

### Semantic importance can cross spatial distance

Self-attention creates a second dependency path. Tokens outside the spatially dilated mask may receive high attention probability from masked tokens. MASQ identifies such tokens during early denoising, averages their attention probability to masked tokens, and promotes Stage 0 tokens above a threshold to Stage 1. The paper performs this semantic refinement every five timesteps in the stated evaluation.

The refinement itself has a cost and a calibration assumption: attention probabilities computed at the beginning must identify later-important tokens well enough. A threshold that is too low promotes too many tokens and reduces savings; one that is too high allows error to enter through an important long-range dependency. Semantic promotion therefore changes both numerical quality and control overhead.

### Timestep scheduling uses the changing sensitivity of denoising

Early diffusion steps make large structural changes. Later steps make smaller corrections, so the paper lowers precision more aggressively later in the 50-step schedule. The reported transitions are from MXINT8/8/4/2 to MXINT8/4/4/2 and finally MXINT8/4/2/2 across Stages 3, 2, 1, and 0. The mask region stays MXINT8.

Precision errors are not confined to matrix multiplication. Group normalization aggregates statistics over tokens; low-precision values can perturb the mean and variance used by high-precision tokens. Softmax converts attention scores into probabilities; errors in low-precision keys can change which context a high-precision query uses. MASQ computes normalization statistics from higher-precision stages and excludes the lowest-precision Stage 0 tokens from softmax. These choices add control and data-selection work that must be included in an implementation cost.

### The hardware executes several precisions with one block-scaled format

MXINT uses blocks of 32 values sharing an 8-bit exponent, with two's-complement INT2, INT4, or INT8 mantissalike fields. MASQ's multi-precision matrix unit contains 32 block-wise processing elements. Each processing element handles 32 activation/weight pairs; INT8 is processed as four 2-bit slices, INT4 as two, and INT2 as one. Partial results are shifted by slice significance, converted through BF16 scaling and accumulated in FP32 before returning to BF16.

The mask manager encodes four stages in two bits, dilates masks, promotes semantically important Stage 0 tokens, and downsamples masks across U-Net resolutions with a 2×2 majority rule. A vector unit handles normalization and softmax; on-chip storage holds weights, activations, intermediate values and masks. The hardware therefore implements the algorithm's spatial/timestep policy rather than merely adding a low-bit multiplier.

### Quality and hardware numbers have different evidence boundaries

The version-1 evaluation uses Stable Diffusion v1 for text-guided inpainting on EditBench and LAION, and SDEdit on LSUN Church. Average mask ratios are 42.87%, 2.38%, and 13.12%, respectively. The quality table compares the original FP16 model with MASQ using inception score, CLIP, FID, PSNR and SSIM. Results are mixed: LAION FID rises from 13.60 to 14.07 and LSUN FID rises from 19.29 to 20.91, while some IS, CLIP, PSNR and SSIM entries improve or remain close. Since FID is lower-is-better, those increases are regressions under that metric; “preserving quality” must be read as a multi-metric, approximate claim rather than exact equality.

The hardware is implemented at RTL and synthesized with a 14 nm process target at 800 MHz and 0.8 V. A cycle-accurate simulator compares a server configuration with 2 TB/s HBM2E against an edge configuration with 102.4 GB/s LPDDR5. MASQ peak throughput is matched to A100 FP16 312 TFLOPS and Orin NX 3.76 TFLOPS under MXINT8×MXINT8 for the comparison. DRAM energy uses vendor-based estimates. These are modeled architecture results, not measurements from fabricated MASQ silicon.

The uniform-MXINT8 MASQ baseline separates two effects. Even without mask-aware precision, the proposed hardware reports up to 8.10×/2.94× speedup and 2.32×/2.30× energy efficiency over A100/Orin NX. With the mask-aware algorithm, the maxima become 16.06×/5.39× and 4.18×/4.93×. Relative to uniform MXINT8 on the same modeled hardware, average speedup improvement is 61.35% server and 73.58% edge; average energy-efficiency improvement is 54.88% and 71.45%. The GPU baselines are static with respect to mask size, while MASQ changes precision with the mask, so these comparisons combine hardware and algorithm differences unless the uniform-MXINT8 baseline is used.

### What the paper establishes and what remains open

MASQ establishes a co-designed way to reduce precision outside the edit region while retaining spatial and semantic dependencies, under the listed models, masks, 50-step schedule, RTL assumptions, synthesis target and cycle-accurate simulator. It does not establish zero quality loss, fabricated-chip behavior, equal power measurement, or transfer to arbitrary masks, diffusion models, resolutions, timesteps, process nodes, memory systems or GPU baselines. Stronger evidence would report per-prompt distributions, mask-size/shape sweeps, semantic-refinement overhead, numerical error by stage and timestep, full memory traffic, post-layout power/timing, and independent silicon or FPGA measurements. [Version-1 manuscript, Sections 2–5.4, PDF pages 2–10, Table 1 and Figures 8–10](https://arxiv.org/pdf/2605.23226v1#page=5)

<span id="explanation-dac-2026-research1095"></span>

## STEM-CAM: configurable distance order still requires a precise physical encoding

### What the distance computation means

For two feature vectors, a Minkowski distance of order `p` combines coordinate differences as absolute values raised to `p`, sums them and applies the `1/p` power. Different orders produce different rankings: L1 emphasizes total absolute difference, L2 gives larger differences more weight, and other orders change the geometry again. A hardware design that supports an order must preserve the ordering or numerical tolerance required by the application.

### What the CAM representation does

Content-addressable memory compares a query against stored entries in parallel. STEM-CAM uses segmented thermometer encoding for multibit values. A thermometer code represents an ordered magnitude as a run of asserted positions; segmentation organizes that representation into smaller groups. Wildcards make selected positions irrelevant to a match, allowing the cell logic to express parts of a distance comparison without reading each stored value through a serial arithmetic unit.

This is a representation tradeoff. The encoding may simplify parallel matching, but it can expand storage, require metadata and scales, and add programming and read operations. A match result is not automatically the exact real-valued distance. The mapping from encoded differences to the distance order, precision and final ranking must be specified and tested.

### What the FeFET cell changes

A FeFET stores a programmable state using a ferroelectric gate structure. An encoding-aware cell must distinguish the programmed states during a read while tolerating variation, retention drift, endurance limits, sensing margin and voltage changes. These physical effects can turn a logical match into a false match or miss. Array size, peripheral sensing, programming energy and calibration are part of the system cost.

### How to interpret “arbitrary-order”

The official description supports a configurable encoding and FeFET CAM cell for arbitrary-order Minkowski metrics, but reports no numeric throughput, precision, area, energy, variation or application result. “Arbitrary-order” identifies the intended configurability; it does not prove exact computation for every real-valued order, bit width or device condition.

A complete evaluation should compare distance values and nearest-neighbor rankings against a high-precision reference across orders, vector distributions, ties, quantization scales and device variation. It should include encoding, programming, sensing, peripheral and result-selection costs, then measure the application quality that depends on the distance.

### What the evidence establishes and where it stops

The captured record establishes a segmented thermometer/wildcard CAM proposal using an encoding-aware FeFET cell. It does not establish numeric performance, exact distance preservation, physical reliability, area/energy efficiency or application-level AI improvement.

[Observed paper card](../observed-subthemes/specialized-ai-accelerators.md#paper-dac-2026-research1095)

## STEM-CAM: a distance function needs a physical representation

A distance function converts differences between feature vectors into a numerical separation. For Minkowski order `p`, it combines absolute coordinate differences raised to `p`, followed by a `1/p` power. The familiar absolute-sum and Euclidean distances are special cases. A configurable metric still operates at finite precision in hardware.

[STEM-CAM](../observed-subthemes/specialized-ai-accelerators.md#paper-dac-2026-research1095) proposes segmented thermometer encoding with wildcard matching in a FeFET-based content-addressable memory. Its description supports the encoding and cell concept but supplies no numeric throughput, precision, area, or energy result. “Arbitrary-order” is not evidence of exact real-number computation for every possible order. [Official DAC description](https://63dac.conference-program.com/presentation/?id=RESEARCH1095&sess=sess169).

Content-addressable memory compares a query with stored entries in parallel. Thermometer encoding represents magnitude using a run of asserted positions; a wildcard makes selected comparison positions irrelevant. Such encoding can make comparison simple while expanding the representation. A FeFET uses a ferroelectric gate structure to retain a programmable state. The full cost must include encoding, programming, reading, and selecting results, along with errors caused by variation in stored device states.

## Rendering: preserve the scene calculation or deliberately replace it

Gaussian splatting represents a scene with spatially extended primitives carrying properties such as color and opacity. Rendering projects their contributions onto image pixels. Where contributions overlap, depth and transparency determine how their colors combine. This is why sorting and blending can be expensive, and why changing either requires image-quality checks.

<span id="explanation-dac-2026-research054"></span>

### GEMM-GS: turn Gaussian opacity evaluation into matrix work without removing the rendering order

#### The bottleneck is a mismatch between the calculation and the GPU datapath

3D Gaussian Splatting represents a scene with Gaussian primitives. To render one view, the system projects visible Gaussians onto the image, finds the tiles they overlap, duplicates references for those tiles, sorts each tile's references by depth, and blends the ordered contributions into pixels. For pixel `j` and Gaussian `i`, the rendered color uses opacity `alpha_ij` and accumulated transmittance `T_i`: a contribution farther behind opaque material has less effect, and changing depth order can change the result.

The opacity calculation contains a two-dimensional quadratic form. With covariance coefficients `A`, `B`, and `C`, its exponent contains `−A dx²/2 − B dx dy − C dy²/2`. This is a collection of per-Gaussian/per-pixel element-wise operations, not a conventional matrix multiplication. Modern GPUs can execute GEMM at high throughput on Tensor Cores, but vanilla 3DGS leaves much of that hardware unused. The paper profiles blending at nearly 70% of total 3DGS rendering time, so it targets that stage rather than proposing a new scene representation.

#### The coordinate transformation exposes six reusable products

[GEMM-GS](../observed-subthemes/specialized-ai-accelerators.md#paper-dac-2026-research054) selects a reference pixel for each tile and writes every pixel's coordinate as the reference coordinate plus an intra-tile offset. For a Gaussian, the offset from the Gaussian center to the reference pixel is constant for all 256 pixels in a 16×16 tile. Expanding the quadratic form with those offsets separates the terms into two vectors of length six.

The Gaussian-side vector contains terms derived from covariance and Gaussian-to-reference displacement. The pixel-side vector contains the fixed intra-tile terms: squared x offset, squared y offset, x–y product, x offset, y offset, and a constant one. Their dot product equals the original quadratic exponent. The pixel vectors are independent of the particular Gaussian and tile position, so they can be precomputed once and reused. The Gaussian vectors still have to be constructed for each Gaussian/tile pair because they depend on the scene data.

For a batch of 256 Gaussians and a 16×16 tile, the implementation forms a 256×6 Gaussian matrix and a 6×256 pixel matrix, then multiplies them to obtain all Gaussian–pixel exponent values. The paper text has a dimension inconsistency in Section 3.3: one description says the output is 256×64 even though the stated 256 Gaussian rows and 256 pixel columns imply 256×256. The numerical implementation and the underlying six-term derivation should therefore be treated as source evidence requiring reconciliation, not silently normalized.

#### Matrix conversion does not eliminate the rest of volume rendering

After the matrix product, GEMM-GS still applies the exponential, opacity threshold, transmittance update, early termination, color accumulation, and depth order. Sorting is not removed. The transformation changes how exponent/opacity values are produced; it does not make all Gaussian–pixel pairs useful or change the physical visibility rule. The comparison is therefore a kernel optimization inside the existing 3DGS pipeline, not a replacement for sorting or a new accelerator chip.

The CUDA implementation assigns 256 threads to a 16×16 tile and processes sorted Gaussians in batches of 256. Limited shared memory leads to a mini-batch implementation using 16×8 submatrices and four rounds of warp-level `mma(m16n8k8)` PTX operations. Eight warps complete the effective matrix work. Double buffers hold indices, features, and the Gaussian matrix, while Ampere asynchronous copies overlap data movement with matrix construction and Tensor-Core execution. The benefit therefore depends on batch size, tile occupancy, synchronization, and the GPU instruction path—not only on the algebraic rewrite.

#### What the evaluation measures

The manuscript evaluates 13 scenes from Tank & Temples, Deep Blending, and Mip-NeRF 360. Scene sizes range from about 1.04M to 4.74M Gaussians; examples include Truck, Train, DrJohnson, Playroom, Bicycle, Bonsai, Counter, Flowers, Garden, Kitchen, Room, Stump, and Treehill. Each scene is trained for 30K iterations with the official 3DGS pipeline. Rendering latency is measured with CUDA events over ten passes through the test views, averaged separately on A100 and H100 GPUs.

Against vanilla 3DGS, Table 2 reports average speedups of 1.42× on A100 and 1.37× on H100. For the A100 Truck scene, latency changes from 4.28 ms to 2.78 ms. When integrated with preprocessing methods, average A100/H100 speedups are reported as 1.19×/1.21× over FlashGS, 1.42×/1.33× over StopThePop, and 1.50×/1.44× over Speedy-Splat. When integrated with compression methods, the paper reports 1.73× over c3dgs and 1.58× over LightGaussian on average. These are rendering-time comparisons under the paper's implementation; they do not include scene training or the full camera-to-display path.

The sensitivity study reports 1.73× and 1.74× speedup over vanilla 3DGS at 2× and 3× resolution. Smaller Gaussian batches reduce parallel efficiency because the 256-thread tile organization cannot fill its matrix-construction work evenly. Resolution scaling and batch-size sensitivity are therefore part of the mechanism, not incidental implementation details.

#### Correctness and deployment boundaries

An algebraically equivalent reformulation can still produce different floating-point values through precision, operation order, exponential implementation, and accumulation order. The inspected evaluation reports timing but not a detailed image-quality table tied to each baseline and scene. The paper's “equivalent” claim describes the mathematical transformation; it does not by itself establish bitwise equality or equal perceptual quality after Tensor-Core execution.

The result supports a bounded claim: on the listed scenes, A100/H100 devices, CUDA kernel, tile/batch configuration and ten-pass timing protocol, reformulating the opacity exponent enables useful Tensor-Core execution and reduces measured render latency. It does not establish equal image quality under all precisions, a fabricated accelerator, lower whole-application energy, or universal real-time performance. A stronger evaluation would report PSNR/SSIM or task-quality changes for every integrated baseline, numerical error distributions, warmup and clock conditions, end-to-end application latency, power, and behavior on scenes with extreme tile occupancy. [Version-1 manuscript, Sections 2–4.3, PDF pages 3–7, Tables 1–2 and Figures 5–7](https://arxiv.org/pdf/2604.02120v1#page=4)

<span id="explanation-dac-2026-research1096"></span>

### Geometry-guided CODA: sort-free rendering is a visibility approximation unless the guidance preserves the required depth relationships

#### Why ordinary 3D Gaussian Splatting sorts

3D Gaussian Splatting represents a scene with many translucent Gaussian primitives. Each primitive has a projected footprint, an opacity and a color. For a pixel, the renderer combines the primitives that cover that pixel. If primitive (i) has opacity (\alpha_i), color (c_i), and accumulated transmittance (T_i) before it is applied, its contribution is (T_i \alpha_i c_i), and the next transmittance becomes (T_i(1-\alpha_i)).

The order matters because (T_i) depends on the primitives rendered before (i). An opaque or nearly opaque primitive reduces the contribution of primitives behind it. Sorting the covered Gaussians by depth is therefore part of the visibility computation, not an arbitrary preprocessing step. Removing the sort changes the problem unless another rule recovers enough of the same ordering information.

#### What geometry guidance is intended to do

The captured CODA description proposes a two-stage procedure. A 2D Gaussian model first provides geometry guidance, and the complete 3D model is then rendered with sort-free weighted rendering. The likely purpose of the first stage is to supply spatial or visibility information that lets the second stage combine contributions without explicitly sorting every covered 3D Gaussian. The source does not expose the guidance equations, whether it predicts order, depth, weights or visibility, or how the 2D representation is constructed.

That missing definition is important. A weighted sum can be order-independent, but the weights must encode enough depth and opacity information to approximate the ordered transmittance calculation. If the guidance assigns similar weights to primitives that have different depths, the method can brighten surfaces that should be hidden, blur thin structures, or mix foreground and background across an edge. These are consequences to test, not observed failures of CODA.

#### What is saved and what is added

The proposed saving is the work and storage used by sorting: generating sortable keys, moving references, comparing depths and maintaining ordered lists for tiles or pixels. The cost does not disappear. The renderer now has to generate the 2D guidance, read or construct its representation, derive weights, and perform the sort-free accumulation. It may also need extra passes or storage for the guidance and for the complete 3D model.

The relevant comparison is therefore total rendering cost. It must include projection, tile assignment, guidance generation, guidance-to-3D association, weighted accumulation, memory traffic, synchronization and output writes. A speedup measured only after guidance has been produced would charge the baseline and proposed method different amounts of work. The comparison must also state whether the method renders the same number of Gaussians, uses the same image resolution and includes scene loading or preprocessing.

#### Why visibility quality needs more than a final image average

A sort-free approximation can preserve average image error while failing on the regions where visibility is hardest. Evaluation should separately inspect thin objects, intersecting surfaces, semi-transparent regions, depth discontinuities, highly overlapping Gaussians, reflective or high-contrast boundaries, and views that differ from those used to build the guidance. It should report PSNR or SSIM together with depth or alpha error where those quantities are available, and compare the same trained 3DGS scene with the ordered reference.

The test should also vary scene density and camera viewpoint. A guidance structure that works for one view may not remain valid after the camera moves. If guidance is generated per view, its latency and memory traffic belong in the render time. If it is reused across views, the evaluation must state its validity range and what happens when the view leaves that range.

#### How to read the reported ratios

The official description reports 8.4–11.6× speedup over an RTX 3060M and 2.7–3.9× over an RTX 4090. The captured record does not identify the scene set, resolution, image quality, implementation technology, clock conditions, absolute latency, accelerator area, energy boundary, guidance cost or whether the ratios are kernel, rendering or end-to-end measurements. The two GPU comparisons also represent different baseline classes and should not be collapsed into one general hardware result.

The evidence establishes a proposed geometry-guided, two-stage 3DGS rendering method with sort-free weighted rendering and the reported GPU-relative ratios. It does not establish that ordered visibility is preserved, that guidance generation is included in the timing, that the design has been fabricated, or that the speedup transfers across scenes, views and quality targets. The name CODA here refers to this Gaussian-rendering proposal; it should not be merged with unrelated CODA dataflow work.

[Observed paper card](../observed-subthemes/specialized-ai-accelerators.md#paper-dac-2026-research1096)

### Geometry-guided CODA: remove sorting by changing the rendering procedure

The [geometry-guided architecture](../observed-subthemes/specialized-ai-accelerators.md#paper-dac-2026-research1096), named CODA in its description, first uses a 2D Gaussian model to obtain guidance, then performs sort-free weighted rendering of the complete 3D model. Reported speedups are 8.4–11.6× over RTX 3060M and 2.7–3.9× over RTX 4090. Scene quality, implementation technology, area, energy, and the full evaluation remain unavailable. [Official DAC description](https://63dac.conference-program.com/presentation/?id=RESEARCH1096&sess=sess157).

Removing an ordering step is not the same as accelerating the original ordered calculation. Guidance generation becomes part of the cost, and imperfect guidance may affect thin structures, overlapping surfaces, or transparency. Those are proposed stress tests, not observed failures of CODA. This rendering design is also distinct from other papers using the CODA name for unrelated hardware.

## What connects these mechanisms over the longer term

The common technical question is whether information about the workload can reduce more work than it costs to obtain and use. That information may be an unchanged graph dependency, a repeated weight, a spatial mask, or a known pixel-coordinate pattern. Hardware and software have to agree on how it is represented and when it remains valid.

The evidence does not support one universal winner. TDH-GNN needs useful temporal reuse; MASQ accepts numerical approximation; GEMM-GS depends on efficient matrix execution; DSPE still needs stronger quality and comparator evidence. These distinctions are the substance of the comparison, not qualifications to discard after quoting speedups.

A defensible longitudinal study would track these mechanisms across editions under comparable tasks, quality targets, memory budgets, and implementation stages. The present sample supports that research question, not an adoption trend. Full-paper recovery for five records, independent reproduction, and reconciliation of older source coding outside the reading-card overlay remain unfinished.
