# Sparse and irregular compute

This subject has 11 records in the selected sample. This page explains where it fits, then presents all captured paper evidence without shortening the measurements or limitations.

[Definitions used in the paper records](../reading-guide-v1.md)

## Understand the parent subject first

- [Architecture and accelerators](../themes/architecture-and-accelerators.md)

## Why a zero can be cheap mathematically and expensive computationally

This chapter contains eleven paper records, each now linked to an expanded individual explanation. SPADE has a recovered manuscript; the other ten records still lack theirs. Acc-SpMV additionally has selected pinned-code inspection, and LTMiner links separately identified related-paper background. This is writing coverage, not independent acceptance. Full-paper evidence and independent comprehension review remain open.

In a sum of products, a product involving zero contributes nothing. Skipping it preserves the mathematical result under the applicable arithmetic rules. But the machine must first know which values are zero and locate the useful values that remain. A sparse representation stores useful entries with information identifying their positions.

That position information occupies memory and must be read. The program may also need to gather values from scattered locations, combine partial results, and coordinate workers. Sparse computation is beneficial when avoided work exceeds these added costs. The fraction of zero entries alone is insufficient to decide that question.

## Irregularity concerns how work is distributed

Two matrices can have the same number of nonzero entries and different execution behavior. One may distribute entries evenly across rows; another may concentrate most entries in a few rows. If one worker receives a long row while others receive short rows, the shorter workers finish first and wait.

Connections in a graph can create a similar imbalance. Some objects have many neighbors and others have few. Accessing their data can also produce different memory behavior. A hardware method must therefore account for both the amount of work and its arrangement.

## Three design choices recur in the collected records

The first is how to represent useful entries. A representation can make it easy to find the next entry or reuse an input, while making another operation harder. Converting to that representation has a cost, which may be repaid only if the input is reused many times.

The second is how to assign work. Fixed assignments are simple but can leave workers idle. Dynamic scheduling can move ready work toward available resources, but needs queues, dependency checks, and control. Scheduling overhead can dominate when useful tasks are very small.

The third is where partial results remain. Several input combinations can contribute to the same output entry. Combining them requires either exclusive ownership, ordered updates, or a correct reduction procedure. An implementation must preserve the required numerical behavior while avoiding excessive synchronization and transfers.

## What the selected examples contribute

BSGCN proposes dividing graph work and tailoring caching to different sparsity conditions. Its description reports numerical benefits, but does not give the baselines and conditions needed for a fair ranking. The individual explanation below separates the proposed mechanism from what remains unverified. [Step-by-step explanation](#explanation-dac-2026-research1242)

PFGEMM combines compressed index prefixes, element-level scheduling, and frequency-aware caching. Its description reports traffic and speed ratios, but the detailed algorithms and comparison conditions remain missing. [Step-by-step explanation](#explanation-dac-2026-research138)

Duet concerns skipping work at the bit level in transformer computation. A nonzero weight can still have redundant binary digits. Removing those digits with correct decoding can preserve its integer value; additional approximation is a separate operation. The explanation below shows why sign handling, position information, and execution balance matter. Duet's exact encoding and full evaluation remain unrecovered. [Recorded evidence](../observed-subthemes/sparse-and-irregular-compute.md#paper-dac-2026-research1419)

TRIDENT connects two sparse multiplications so that intermediate results can be consumed without waiting for the entire intermediate matrix. The benefit depends on how much intermediate work is created, how it is combined, and whether finite buffers can support the resulting bursts. [Step-by-step explanation](#explanation-dac-2026-research149)

<span id="explanation-dac-2026-research1242"></span>

## BSGCN: optimize the sequence of feature accesses, not just the busiest nodes

### What the source establishes

BSGCN groups most low-degree nodes into large bands, treats remaining nodes in smaller bands, and uses band-specific traversal and caching alongside high-degree-node pinning. [DAC description](https://63dac.conference-program.com/presentation/?id=RESEARCH1242&sess=sess161). This is the accelerator paper by Shangtong Zhang and coauthors, not the unrelated sentiment-analysis models sharing the acronym.

No full manuscript was recovered. The exact band-construction algorithm, degree thresholds, traversal rules, cache replacement policy, and hardware configuration remain unknown. The following numerical examples are constructed explanations of the design problem, not BSGCN traces or recovered circuit details.

### Start with the graph operation

A graph has nodes and edges. A node stores a vector of features; an edge identifies a connection. A graph-convolution aggregation combines feature vectors from connected nodes, using the model's specified edge weights or normalization.

For a teaching example, output node u receives features [2, 4] and [6, 8] from two neighbors, with coefficients 0.25 and 0.75. Its aggregate is `[0.25×2 + 0.75×6, 0.25×4 + 0.75×8] = [5, 7]`. Computing it requires the two feature vectors, their coefficients, and the output destination.

The relevant memory accesses depend on which neighbor identifiers are present, not merely on the number of arithmetic operations. Consecutive output nodes may request the same input features, or completely different ones. The former can reuse cached data; the latter cannot.

Degree counts connections under a defined convention. For directed graphs, incoming and outgoing degree differ. A node that collects many neighbors is not automatically the node whose own feature vector is requested most often. The source needs to specify direction and traversal before a degree threshold can be interpreted as a feature-reuse predictor.

### Why low-degree nodes can collectively matter

Suppose ten nodes each cause 1,000 feature requests, while 100,000 nodes each cause two. The first group causes 10,000 requests; the second causes 200,000. Protecting only the most individually frequent nodes addresses less than 5% of requests in this constructed distribution.

Those counts are not necessarily DRAM reads: caches may absorb repeated requests. They illustrate why the frequency of each node and the number of nodes must both enter the analysis. A large population with modest individual reuse can dominate aggregate traffic.

Feature width changes the cost too. A vector with 128 four-byte elements occupies 512 bytes. Fetching it once costs more traffic than fetching a single four-byte scalar. If many aggregation edges need a full feature vector, recovering even a second use before eviction can save meaningful traffic. Actual transfers depend on cache-line size, tiling, and which feature components the operation needs.

### Reuse is useful only if data remain available until the next request

Consider a fully associative toy cache holding two feature vectors, initially empty, with least-recently-used replacement. The request sequence `A, B, C, A, B, C` misses six times: each entry is evicted before it returns. The sequence `A, A, B, B, C, C` has the same six requests and the same per-node frequencies, but only three misses.

Ordering has created temporal locality: repeated requests occur close enough together that the cache can serve them. It has not changed the amount of mathematical graph work. This explains why a traversal change can reduce traffic even without increasing cache capacity.

However, reordering cannot blindly shuffle graph contributions. The loader must retain neighbor identities and coefficients, while partial sums must reach the correct output. If the implementation needs more output accumulators or extra bookkeeping to exploit input reuse, those costs belong in the comparison.

### Why a single grouping policy can fail across graphs

Nodes with similar degree can have very different neighborhoods. Four output nodes might all request neighbors A and B, or each might request a distinct pair. Both groups have degree two per output. Only the first group has substantial shared input reuse.

Conversely, useful reuse can occur across nodes with different degrees. Degree-based grouping may therefore be a helpful heuristic without being sufficient to identify the best execution order. The description says bands group nodes by reuse characteristics, but it does not specify how those characteristics are measured or estimated.

A large band can expose more opportunities to reuse inputs across outputs. It can also require a larger active set of features and partial sums. If that set exceeds available storage, increasing the band can create additional evictions. A small band may fit well but fail to expose reuse across its boundaries. Choosing band size is a working-set decision, not simply “larger is better.”

### Pinning protects data at an opportunity cost

Pinning reserves cache space so selected entries cannot be evicted by the ordinary replacement policy. Protecting a frequently reused feature vector can prevent repeated expensive reads. But the reserved space is unavailable to other data.

For a constructed two-entry cache, pin H and alternate requests A, B, A, B. If H is not requested during this interval, only one slot remains for A and B and every request misses. Without pinning, the first A and B miss and the next two requests hit. A node can be globally frequent yet temporarily unhelpful to retain.

This does not show that BSGCN's pinning is ineffective. It identifies what its policy needs to establish: when a node is pinned, for how long, what capacity is reserved, and whether the protected reuse repays the displaced reuse. A combined policy for low- and high-degree nodes needs to handle competition between them, not optimize each in isolation.

### Cache correctness includes which layer produced a feature

The same node identifier can refer to different feature values at successive neural-network layers. Reusing a cached feature from the wrong layer can produce a wrong answer even though the graph connection is unchanged.

A system can prevent this through separate storage regions, layer-specific addressing, explicit invalidation, or another defined rule. The example highlights a correctness requirement, not a missing feature proven in BSGCN. The unrecovered manuscript must establish its actual lifetime and addressing conventions.

Parallel aggregation adds another requirement. Contributions computed by different workers must be combined exactly once. If floating-point additions are reordered, small rounding differences may arise even if every contribution is present. Exact bitwise equivalence and acceptable model-level output are different validation targets.

### Include partition preparation and changing graphs

Constructing bands can require inspecting connectivity, calculating statistics, and building reordered structures. A graph reused for many inferences can amortize that preparation. A graph that changes frequently may need repeated work or an update mechanism.

If preparation takes one second and saves one millisecond per inference, one thousand executions merely recover the preparation time. If the graph changes after one hundred executions and full preparation must repeat, the savings do not repay that cost. These are constructed numbers; the actual break-even point requires measurements.

There may also be a distinction between updating edges and updating features. New feature values may preserve the graph partition but require cache refresh. Changed connectivity can invalidate estimated reuse itself. An end-to-end evaluation should state which type of change is supported and timed.

### Read the reported improvements without inventing their conditions

The official description reports 1.41× average speedup, up to 4.80×, 24.24% less DRAM traffic, and 1.30× energy efficiency versus other accelerators. It does not identify comparison configurations, datasets, feature widths, cache capacities, process, clock, or measurement methodology. [DAC description](https://63dac.conference-program.com/presentation/?id=RESEARCH1242&sess=sess161).

A 1.41× speed ratio corresponds to about 70.9% of baseline time, a 29.1% reduction. A 4.80× maximum is not the typical result. The 24.24% traffic reduction leaves 75.76% of baseline bytes, not 75.76% of baseline execution time. Arithmetic and stalls unrelated to those transfers can remain unchanged.

For a constructed 100 ms inference with 40 ms proportional to the affected DRAM traffic and 60 ms unaffected, reducing that traffic by 24.24% gives `60 + 40×0.7576 = 90.304 ms`, about 1.11× speedup. Larger gains would require a different time breakdown or additional effects. This example is not a challenge to the reported ratio; it explains why bytes alone cannot predict latency.

Likewise, 1.30× efficiency implies about 76.9% of energy per matched unit of work if that is the metric's denominator. The average, maximum, traffic result, and efficiency figure should not be multiplied together or treated as one verified operating point without the underlying experiments.

### What this adds to sparse-computing research

PEACE emphasizes preserving indices while feeding compressed matrix work to an array. BSGCN emphasizes arranging graph requests so retained data are reused before eviction. Both show why counting nonzeros is an incomplete cost model, but they solve different scheduling and storage problems.

A testable longer-term hypothesis is that optimizing the many modest-reuse items can matter as much as protecting a few individually frequent ones. Testing it requires reuse-distance distributions, feature sizes, pinning occupancy, preparation costs, and matched-cache comparisons across graphs. This single description motivates the question; it does not establish a cross-conference temporal trend.

No BSGCN implementation, graph benchmark, simulation, or synthesis was executed. The manuscript, exact band and cache policies, complete evaluation conditions, and independent comprehension review remain open.

<span id="explanation-dac-2026-research138"></span>

## PFGEMM: compress index repetition while keeping useful work ready

### Separate representation, scheduling, and caching

PFGEMM proposes prefix-CSR to share repeated index prefixes, element-wise out-of-order scheduling, and frequency-aware cache replacement. [Official DAC description](https://63dac.conference-program.com/presentation/?id=RESEARCH138&sess=sess157). These change the stored representation, execution order, and data retention respectively.

No full manuscript was recovered. The prefix layout, scheduling window, replacement counters, and accumulation scheme remain unknown. The examples below are constructed explanations, not PFCSR encodings or PFGEMM schedules. The unrelated parallel dense-linear-algebra routine also called pfgemm is not evidence for this accelerator.

### Products generated separately must meet at the correct output

For `C = A×B`, a nonzero `A[i,k]` multiplies relevant entries of row k of B. Different k values can contribute to the same output location. Skipping zero products does not remove the need to combine those contributions.

Consider one row of A with `A[0,1]=2` and `A[0,3]=5`. Let `B[1,0]=7`, `B[1,2]=11`, and `B[3,2]=13`, with other entries zero. The products are 14 for output column zero, and 22 and 65 for output column two. The output row is [14, 0, 87].

There are three products but only two nonzero output locations. Independent products may be issued in a different order, but 22 and 65 must be added, not written over one another. The output's sparsity can differ from either input's sparsity, so the system also needs to allocate and identify result locations.

### Sparse indices are part of the bytes moved

Compressed sparse row, or CSR, stores nonzero values, column indices, and boundaries identifying each row's section of those arrays. Narrow arithmetic values can still need comparatively wide position identifiers.

Suppose four illustrative 16-bit indices are hexadecimal `1201`, `1202`, `1207`, and `120F`. Their high byte is always `12`. Storing that byte once plus four low bytes takes five bytes instead of eight, before headers. Reconstruction concatenates the portions: `(0x12 << 8) | 0x07 = 0x1207`.

With a one-byte group header, storage becomes six bytes: a 25% reduction rather than the 37.5% obtained when ignoring the header. If the high bytes differ, this simple sharing rule saves nothing and may add overhead. The actual format must describe group boundaries and unhelpful-prefix cases.

This is prefix sharing, not a prefix sum that computes cumulative totals. It also need not mean delta coding, which stores differences between consecutive indices. The official description establishes shared prefixes, but not their exact encoding.

### Compression can introduce decoding dependencies

A complete index identifies its location independently. A suffix requires the correct prefix before it can be interpreted. Accessing the middle of a compressed group may require an additional pointer, a restart marker, or decoding from an earlier boundary. Those mechanisms cost space or time.

This matters for out-of-order execution. A scheduler selecting arbitrary elements must still obtain their decoded locations. It could choose among already decoded entries or request additional decoding; those alternatives require different buffers and control. The source does not establish which PFGEMM implements.

### Ready arithmetic can bypass a wait, but cannot erase dependencies

In the example above, suppose row one of B is delayed while the operands yielding 65 are available. Issuing that product first can keep a multiplier busy. It does not make the missing row arrive sooner, and the output cannot be declared complete until all contributions are accounted for.

An operation needs both available operands and somewhere to put its result. A full result queue or conflicting accumulator update can stall an otherwise ready multiplication. The scheduler therefore needs readiness information, output identity, and completion tracking—not merely a test for whether an input is cached.

A larger look-ahead window can expose more ready work and more reuse, but it stores and compares more state. The best choice within a finite window is not necessarily the globally fastest schedule. The description's local-optimality language does not establish a universal optimum.

Reordering also needs a numerical contract. Integer additions preserve the sum when overflow is excluded; floating-point reassociation can change rounding. Identical bits, bounded numerical error, and acceptable application output are different requirements. The manuscript must specify which is tested and how accumulator conflicts are resolved.

### Scheduling and replacement policy influence each other

Frequency-aware caching aims to retain repeatedly requested data, such as a row of B used by many output rows. But past frequency need not predict future reuse.

Imagine a two-row cache. H was requested one hundred times in an earlier phase, but the next requests alternate A and B. Retaining H indefinitely leaves only one slot for A and B, causing repeated misses. Aging frequency counts or changing retention at phase boundaries could help, with additional policy state. This is a failure case to test, not the unrecovered PFGEMM policy.

Scheduling can bring repeated requests closer together and make retention more useful. Replacement can change which operands are available and therefore which operations can issue. A fair experiment should isolate these interactions where possible, holding cache capacity and arithmetic resources fixed.

### Interpret the reported ratios

The description reports geometric-mean ratios of 1.8× for off-chip traffic reduction and 2.1× for speed versus other accelerators. It does not provide baseline names or evaluation configurations. [DAC description](https://63dac.conference-program.com/presentation/?id=RESEARCH138&sess=sess157).

Interpreting traffic reduction as baseline bytes divided by new bytes gives 55.6% of baseline traffic, a 44.4% reduction—not 180% fewer bytes. A 2.1× speed ratio leaves 47.6% of baseline time. The per-workload definitions still need recovery.

A geometric mean combines ratios multiplicatively. Two speed ratios of four and one quarter have geometric mean one despite opposite outcomes. This does not establish unchanged total job time, which depends on baseline durations. An aggregate therefore does not guarantee a benefit on every matrix.

The traffic and speed ratios must not be multiplied into a 3.78× combined gain. They describe overlapping effects in different units. Less index traffic also need not reduce total traffic proportionally when values, intermediate results, and output writes dominate.

### Establish the full job cost before drawing a trend

Required comparison conditions include matrix shapes and patterns, index/value widths, cache size, scheduling-window size, arithmetic rules, process, clock, memory bandwidth, and whether format conversion is included. A matrix reused many times can repay conversion differently from a new matrix for every job.

For a constructed case, 20 ms of conversion and 0.2 ms saved per execution break even after one hundred uses. Fewer uses lose time unless another benefit compensates. A kernel-only speedup is not sufficient to evaluate that workflow.

BSGCN changes the timing of graph-feature requests; PFGEMM additionally compresses information needed to identify sparse operands. Together they motivate a testable hypothesis: metadata representation and scheduling should be evaluated jointly because decoding can constrain when useful work becomes ready. The descriptions motivate that question, not a demonstrated longitudinal trend.

No PFGEMM implementation, matrix benchmark, simulation, or synthesis was executed. Exact PFCSR decoding, scheduling and cache rules, full-paper conditions, and independent comprehension review remain open.

<span id="explanation-dac-2026-research1419"></span>

## Duet: when fewer weight bits mean less multiplication work

Duet is the DAC paper by Heng Liao and colleagues, also listed as entry C108 on [Kun Wang's publication page](https://imwangkun.github.io/fullpaper.htm). That entry has no manuscript link. The explanation uses the [official Description](https://63dac.conference-program.com/presentation/?id=RESEARCH1419&sess=sess110); no manuscript page numbers are available. All numerical examples below are constructed teaching examples, not Duet encodings or measured traces.

### Start with one output, not the accelerator's component names

A linear layer forms each output by multiplying input numbers by learned weights and adding the products. For inputs 2 and 5 and weights −3 and −2, the output is `2 × (−3) + 5 × (−2) = −16`. An input number produced by a preceding layer is often called an activation. The arithmetic is the same regardless of that name.

A conventional multiplier handles several weight bits together. A bit-serial design spreads their contributions over successive steps. Consider an unsigned weight 13, whose binary representation is `1101`. Its positions have values 8, 4, 2, and 1. Multiplying input 3 by this weight gives `3 × 8 + 3 × 4 + 0 + 3 × 1 = 39`. Hardware can form these terms by selecting the input where a weight bit is one, shifting it to the appropriate position, and accumulating the result.

If a bit position contributes zero across an entire group of weights, an implementation might skip that group's step. This is bit-column sparsity: the column consists of the same binary position across several weights. It is different from having zero weights. The weights 1, 2, and 3 are all nonzero, but their eight-bit unsigned representations all have zero in the top six positions. A controller that understands this fact need not schedule those six positions.

A zero in one weight does not necessarily remove a shared step. If another weight in the group has a one in that position, some arithmetic is still required. Which weights share control therefore affects which bit columns can be omitted. A count of zero bits alone does not determine execution time.

### Removing leading bits must preserve the sign and the position

Signed numbers require more care. In two's-complement notation, an eight-bit −3 is `11111101`. The highest bit has negative value −128; the other positions have positive powers of two. Adding their contributions gives −3. The leading ones are repeated sign information, not independent positive contributions that can simply be discarded.

The three-bit representation `101` also means −3 when decoded as signed: `−4 + 0 + 1 = −3`. Extending its sign back to eight bits restores `11111101`. Reading the same three bits as unsigned would instead give 5. Thus a shortened representation can be exact, but only if the decoder knows its width and signed interpretation. Merely zeroing the removed high bits in the original eight-bit number changes its value.

This establishes a narrow, checkable meaning of lossless: each decoded integer equals its original integer. It does not establish equality to the floating-point weight before any earlier quantization. Nor does it make a later modification of the remaining bits exact. If weight 3 becomes 2, multiplying by input 100 changes its contribution from 300 to 200. Calling the altered bit a low-order bit does not make that output error disappear.

The distinction matters when a method combines exact shortening with approximate compression. Each transformation needs its own claim: integer reconstruction, arithmetic rounding, and application quality are different checks.

### Why the distribution of weights and their grouping matter

Duet's description proposes distribution-aware weight partitioning for high-order pruning, followed by a remaining-compression search. The partition rule and search objective are unavailable. [DAC description](https://63dac.conference-program.com/presentation/?id=RESEARCH1419&sess=sess110).

The underlying opportunity can be understood without guessing that rule. A group of signed weights `[1, 2, 3]` fits in three bits per weight: one sign bit and two value bits. Adding weight 64 forces a shared signed width of at least eight bits, because seven signed bits reach only 63. One large value can therefore keep many otherwise redundant bit positions active for its companions.

Separating the large value might reduce the work for the small values. But the split introduces boundaries and information that says where each group belongs. If weights are moved, their associations with inputs and output coordinates must remain intact. Sorting weights independently of their input associations changes the calculation, even when every individual weight is preserved exactly.

A distribution concentrated near zero makes short representations plausible; it does not prove that every group is short. The tails of the distribution, the group size, the mixture of positive and negative numbers, and the controller's supported encoding determine the actual savings. These are reasons to ask for per-group width distributions rather than relying only on an average.

### Why an activation sum can help with a shared contribution

The description names an activation-sum unit, a two-level shifter, parallel weight/metadata pipelines, and modes for linear and attention layers. It does not expose enough detail to reconstruct their operation. [DAC description](https://63dac.conference-program.com/presentation/?id=RESEARCH1419&sess=sess110).

One exact algebraic example shows why an activation sum can be useful. Return to weights −3 and −2. In three-bit signed form they are `101` and `110`. Their shared sign position contributes −4 to each weight. The remaining unsigned portions are 1 and 2. With inputs 2 and 5, the result is:

```text
remaining-bit products = 2 × 1 + 5 × 2 = 12
shared sign contribution = −4 × (2 + 5) = −28
complete output = 12 − 28 = −16
```

The shared term uses the sum of the corresponding activations. This is a mathematical reason that such a unit may help a representation with common contributions; it is not a reconstruction of Duet's circuit. The actual design must establish which inputs participate, which coefficient applies, and how wide the sum must be to avoid overflow.

Position information matters independently of sign. A surviving bit originally worth eight cannot be treated as a bit worth one after compaction. The decoder must restore its numerical significance before combining it with other contributions. A shifter can perform multiplication by a power of two, but the shift amount must come from a valid encoding rule. The phrase “two-level shifter” alone does not supply that rule.

### Metadata can overlap computation without becoming free

Metadata means the extra information used to interpret the stored weights: for example, group boundaries or surviving positions. These are illustrative possibilities, not verified Duet fields. Such information must be read and decoded before dependent arithmetic can use it.

Suppose an ideal two-stage pipeline decodes one group in two cycles and computes one group in eight cycles. If the stages overlap perfectly, successive results can emerge every eight cycles once the pipeline is filled, rather than every ten. The first result still requires both stages. With these assumptions, ten groups take `2 + 8 + 9 × 8 = 82` cycles, not 80 and not the unoverlapped 100.

Now shorten computation to one cycle while decoding still takes two. Ten groups take `2 + 1 + 9 × 2 = 21` cycles. The steady-state limit is decoding, not arithmetic. This example explains why hiding metadata cost depends on stage rates, buffering, and dependencies. It also shows why more compression can expose a new bottleneck.

Variable widths introduce another issue. Four workers assigned groups requiring two, two, two, and eight steps finish a synchronized round after eight steps. They perform 14 useful worker-steps out of 32 available, about 43.8% utilization under this simplified model. An average width of 3.5 bits does not make the round take 3.5 steps. Group assignment or independent progress must address the imbalance; memory stalls and output dependencies can remain even after arithmetic work is balanced.

### Read the reported numbers at the right scope

The description reports 3.13/3.25 effective bits, 1.45–4.30× speedup, and 1.32–2.94× energy improvement on BERT and ViT versus unnamed accelerators. Exact model variants, bit accounting, quality changes, baseline conditions, and measurement boundaries remain unknown. [DAC description](https://63dac.conference-program.com/presentation/?id=RESEARCH1419&sess=sess110).

An effective-bit average is not automatically a stored-bits average including metadata, padding, and alignment. For a constructed group of sixteen weights with four payload bits each and sixteen metadata bits, storage is `(16 × 4 + 16) / 16 = 5` bits per weight. Processing four bit positions would not make the stored format four bits per weight.

Likewise, a 4.30× speed ratio would mean 23.3% of baseline time for the measured scope, not a guarantee for a complete application. If accelerated arithmetic originally took 60 ms of a 100 ms job and everything else stayed at 40 ms, that arithmetic speedup would leave about 53.95 ms overall, or 1.85× job speedup. This is an illustrative limit, not a Duet workload breakdown.

Interpreting energy improvement as baseline energy divided by new energy, 2.94× would leave approximately 34.0% of baseline energy. That interpretation still requires the paper's definition. Neither the energy ratio nor the speed ratio should be multiplied by the effective-bit reduction to invent a combined benefit.

### What this contributes to the subtheme, and what remains unproved

BSGCN addresses when graph features are reused. PFGEMM addresses sparse operand identification and scheduling. Duet addresses redundant work inside represented numbers. These mechanisms act at different levels, so a single “sparsity percentage” cannot compare them fairly.

The shared research question is more specific: after identifying work that can be removed, how much information and coordination are required to remove it correctly? A useful experiment would vary group structure while holding the number of stored values fixed, then measure decoding, arithmetic, waiting, and memory traffic separately. That would help distinguish representation savings from scheduling savings. This is a proposed comparison, not an observed long-term trend.

No Duet implementation, model benchmark, simulation, or synthesis was executed. The full manuscript is still needed for exact encoding, partition/search rules, signed arithmetic, accumulation widths, load-balancing guarantees, quality results, and matched hardware conditions. The explanation is not full-paper-backed or independently accepted.

<span id="explanation-dac-2026-research149"></span>

## TRIDENT: compute through an intermediate matrix without storing all of it

TRIDENT is the DAC paper by Yiyue Hu and colleagues. Its [official description](https://63dac.conference-program.com/presentation/?id=RESEARCH149&sess=sess147) proposes fused triple sparse matrix multiplication with hierarchical flow control, a windowed format and hybrid dataflow, and decoupled out-of-order execution. A full manuscript was not recovered; exact algorithms and page-backed evaluation conditions remain unavailable. The examples below explain the design problem, not TRIDENT's unrecovered implementation.

### What multiplying three matrices actually asks the machine to do

A matrix is a rectangular arrangement of numbers. To multiply two matrices, an output entry sums products from a row of the first and a column of the second. Positions matter: the column index of an entry in the first matrix must match the row index of its partner in the second.

For three matrices A, B, and C, one choice is to compute intermediate D = A × B, then result Y = D × C. Each entry of D can itself contain contributions from several input pairs. Each completed D entry may then contribute to several Y entries. Sparsity means many input entries are zero and can be omitted under the chosen arithmetic rules; it does not guarantee that D is equally sparse.

Consider this exact-integer example:

```text
A = [2, 3]       B = [5,  0]       C = [13]
                    [7, 11]           [17]

D = A × B = [2×5 + 3×7, 3×11] = [31, 33]
Y = D × C = 31×13 + 33×17 = 964
```

Producing D requires the contributions 10, 21, and 33. The first two share an output position and must be added to obtain 31. Storing all three contributions as if they were three distinct entries would not be a correctly combined D. A representation that deliberately retains duplicate positions needs a later operation that combines them correctly.

The second multiplication does not necessarily need the whole D before it can start. Once D's first entry is complete, its product with 13 can proceed while other independent D entries are still being formed. This removes a global barrier—the requirement that every first-stage task finish before any second-stage task starts—without removing local dependencies.

### Streaming changes the lifetime of intermediate data

A two-call implementation may finish D, write it to external memory, and read it back for the second call. A fused implementation connects the stages so that eligible intermediate data can stay in local buffers and be consumed earlier. Streaming here means producing and consuming portions progressively, not making the intermediate data cease to exist.

If D occupies S bytes and the baseline writes and then reads it exactly once, avoiding those transfers saves 2S bytes at that memory boundary. That is a conditional accounting statement. Cache residency, duplicated partial entries, spills, and extra index information can change the actual traffic. For an illustrative one-million-entry intermediate with four-byte values and four-byte column indices, the entries alone occupy eight million bytes, making the write/read pair sixteen million bytes. Row boundaries and other format information are additional.

There are also different choices about what crosses the stage boundary. One can first combine 10 and 21 into 31 and then multiply by 13. Alternatively, one can send the partial contributions onward and compute `10×13 + 21×13`. Both give 403 in this integer example. The latter performs two multiplications instead of one, and sends two contributions instead of one. Fusing operations does not by itself specify whether intermediate aggregation is preserved, delayed, or repeated.

This is the input-reuse versus output-aggregation problem in concrete form. Keeping one input available may help generate many products cheaply, but those products may update many different outputs. Keeping only a few output sums active can simplify accumulation, yet require revisiting inputs when another set of outputs is processed. The buffer capacity and traversal order determine which cost is paid.

### Sparse inputs can produce a large intermediate

Suppose A is a 1,000-by-1 column of ones and B is a 1-by-1,000 row of ones. Their product D has one million entries, all one. The inputs contain only two thousand entries. A method cannot provision its intermediate buffers solely from the number of input entries and assume that will be enough.

Now let C be another 1,000-by-1 column of ones. Computing `(A × B) × C` first creates one million products for A × B, then uses one million products for D × C. In contrast, `A × (B × C)` first computes one scalar using one thousand products, then scales A using another one thousand products. The illustrative totals are two million versus two thousand multiplications, and both produce a column whose entries are 1,000 in exact arithmetic.

This is not evidence that TRIDENT uses the worse order or changes the order. It is a reason that its evaluation must disclose the order used by both the proposed design and each baseline. Avoiding external storage and choosing a smaller intermediate are distinct improvements. A comparison that changes both cannot attribute the entire speedup to streaming alone.

For general sparse matrices, dimensions alone are insufficient to predict intermediate size. Which indices connect determines how many product pairs exist and how many share the same output position. Cancellation can further change the final number of nonzeros, depending on numerical values and zero-removal rules.

### Finite buffers need a rule for stopping producers safely

One sparse input item can generate many output items. For example, a nonzero selecting a long row in the next matrix creates more work than one selecting a short row. A pipeline can therefore receive a burst even when its long-run average input rate seems modest.

Suppose a buffer holds eight items, starts empty, and receives four items per cycle while its consumer removes one. Under this simplified simultaneous-transfer model, occupancy grows by three items per cycle: three, six, then nine. The third cycle cannot proceed as proposed without exceeding capacity. Later idle cycles do not undo an earlier overflow.

A flow-control mechanism must delay production, reserve enough space, split a task into interruptible pieces, or safely store excess work elsewhere. A credit is one possible implementation: permission to produce an item because space has been reserved for it. If a task can generate seven items, one free slot is not enough to launch it indivisibly. It may nevertheless be safe if the task can pause after each item and preserve its state. These are design alternatives, not verified TRIDENT rules.

Stopping a producer also needs a progress argument. If every stage waits for storage held by another waiting stage, no work may advance. More buffering alone does not establish freedom from such a cycle. A convincing account needs the resource dependencies, admission rules, and a reason that some pending work can always complete or release space.

### A window bounds active work, but can also restrict useful work

A window is a limited portion of work made available at one time. Restricting active output coordinates, for example, can keep their partial sums within local storage. An implementation must track which contributions belong to that portion and when all of them have arrived before writing final output values.

If there are one hundred output coordinates but space for ten sums, processing ten-coordinate groups limits the active accumulation state. It can also require rereading an input that contributes to several groups. A format that efficiently identifies those contributions may reduce the searching or revisiting cost; its indexing and conversion overhead must still be counted.

Larger windows can expose more ready work and reuse, while using more storage and more complex selection logic. Smaller windows can simplify storage but leave the machine waiting when all exposed work depends on slow memory requests. The word “windowed” does not establish the chosen size, encoding, or best operating point.

### Out-of-order execution removes one kind of waiting, not dependencies

Imagine requests for two independent tasks. The first task's data arrives at cycle 100; the second task's data arrives at cycle 10. A strict first-in-first-out execution queue may prevent the ready second task from running until the first is ready. This is head-of-line blocking: an unready entry at the front stops later ready entries.

Allowing the second task to run first can use otherwise idle arithmetic resources. It requires more than returning memory data early. The machine must retain each task's identity, its output destination, and any missing inputs, then select eligible work. It must also know when an output is complete despite contributions arriving in a different order.

If the second task consumes a value that the first task must produce, it is not independent and cannot safely bypass that dependency. If many completed products target one output accumulator, its update capacity may remain the bottleneck even when memory waiting is reduced. A scheduling improvement must be evaluated alongside these limits.

Arithmetic order also matters. In finite-precision floating-point arithmetic, rearranging additions need not preserve every output bit. For a familiar double-precision example, `(10^16 + (−10^16)) + 1` evaluates to 1, whereas `10^16 + ((−10^16) + 1)` evaluates to 0 because the inner addition rounds away the unit. An exact-integer example proves the algebra, not the numerical behavior of a reordered floating-point implementation. TRIDENT's types, accumulation order, and correctness tolerance need the full paper.

### What the performance claims do and do not establish

The official description reports an average 3.56× speedup over sparse-matrix accelerators and maxima of 49.6× over a CPU and 6.3× over a GPU. It does not give their identities, matched configurations, matrix sets, or the averaging definition. [DAC description](https://63dac.conference-program.com/presentation/?id=RESEARCH149&sess=sess147).

A maximum is a best reported case, not a typical workload result. The CPU and GPU maxima may concern different matrices, so dividing them does not establish a CPU-to-GPU performance ratio. Nor can a mean establish that every input benefits.

A fair end-to-end comparison needs the same product, permitted multiplication order, numeric requirements, and starting representation. It should include necessary conversion and transfers, distinguish arithmetic from memory and waiting time, and report buffer capacities and spill behavior. The title's “end-to-end” does not establish that the measured boundary includes a host application or data preparation.

The connection to PFGEMM is specific: scheduling within one sparse product and coordinating two dependent sparse products solve related but different problems. A plausible research hypothesis is that preserving intermediate data locally becomes more valuable as intermediate size grows, until buffer pressure, repeated work, or a better multiplication order changes the result. Testing that hypothesis requires varying those factors separately. These descriptions do not yet establish a long-term trend across conferences.

No TRIDENT implementation, matrix benchmark, simulation, or synthesis was executed. Full-paper source recovery, format and flow-control rules, aggregation semantics, numerical validation, matched baselines, and independent comprehension review remain open.

<span id="explanation-dac-2026-research2105"></span>

## Acc-SpMV: arrange sparse products so nearby workers read nearby inputs

The [DAC entry](https://63dac.conference-program.com/presentation/?id=RESEARCH2105&sess=sess127) is titled Acc-SpMV, but its description calls the library OmniSpMV. The [author-linked repository](https://github.com/APHETION/Acc-SpMV/tree/93b7138bad9f3adbfbad4d86a362515fd3e4cd93) identifies the Acc-SpMV publication and DOI 10.1145/3770743.3804276 with matching authors. This supports the repository's paper identity; it does not explain the description's alternative name or prove that the released code is the benchmark version.

No full manuscript was recovered. The code observations below refer to commit `93b7138bad9f3adbfbad4d86a362515fd3e4cd93`, not a moving branch. Selected preprocessing and execution paths were inspected without compilation or execution. The numerical examples are constructed explanations, not measured Acc-SpMV results.

### Begin with the value that must be preserved

Sparse matrix–vector multiplication computes one output number per matrix row. Each stored matrix value multiplies the input-vector entry identified by its column, and the products for the same row are added. Consider:

```text
A = [2, 0, 3]       x = [5]
    [0, 4, 0]           [7]
                        [11]

y = [2×5 + 3×11] = [43]
    [4×7]            [28]
```

Only three products are needed, but the machine also needs their positions. A compressed-row representation can store values `[2, 3, 4]`, column indices `[0, 2, 1]`, and row boundaries `[0, 2, 3]`. The boundaries say that the first row consumes positions zero through one in the value array, and the second consumes position two. The input reads are consequently x[0], x[2], and x[1], not simply the next three consecutive numbers in storage order.

This explains why the arithmetic can be cheap while supplying it is expensive. With eight-byte values and four-byte column indices, those arrays alone require twelve bytes per nonzero for two nominal arithmetic operations: one multiplication and one addition. Input-vector reads, row information, output writes, and repeated transfers add costs. Cached reuse can reduce external traffic, so twelve bytes is an illustrative array accounting figure, not a measured memory-traffic model.

### Reordering columns also requires reordering the vector

Move the original columns into order `[2, 0, 1]`. The reordered matrix becomes rows `[3, 2, 0]` and `[0, 0, 4]`. The matching vector must become `[11, 5, 7]`. The outputs remain `[3×11 + 2×5, 4×7] = [43, 28]`.

If the matrix is reordered but the vector remains `[5, 7, 11]`, the result instead becomes `[29, 44]`. This is not harmless numerical rounding; it pairs the wrong operands. A valid permutation must identify every original column exactly once and stay within the vector's bounds.

The inspected preprocessing constructs a new-column-to-old-column mapping and uses it to rebuild the matrix. Its output includes the mapping alongside tile lengths. The execution path uses each mapping entry to select the corresponding original vector element. These are complementary transformations. [Pinned preprocessing, lines 766–806](https://github.com/APHETION/Acc-SpMV/blob/93b7138bad9f3adbfbad4d86a362515fd3e4cd93/reorder.cu#L766); [vector reader, lines 162–180](https://github.com/APHETION/Acc-SpMV/blob/93b7138bad9f3adbfbad4d86a362515fd3e4cd93/Acc-SpMV.cu#L162).

The inspected reader does not check that the mapping has the expected length, unique integer entries, and valid bounds. That is a validation gap for supplied files, not evidence that files produced by the preprocessor are necessarily invalid. The complete producer/consumer contract still needs tests.

### What a tile means in this implementation

A tile here is a group of at most 32 stored entries assigned to a 32-thread group. It need not be a fully populated rectangular block of the original matrix. The inspected preprocessor first finds same-row runs of consecutive columns, capped at 32 entries. It then packs compatible runs when the next run starts immediately after a group's last column and capacity permits. [Pinned run construction and packing](https://github.com/APHETION/Acc-SpMV/blob/93b7138bad9f3adbfbad4d86a362515fd3e4cd93/reorder.cu#L347).

This layout explains an otherwise surprising instruction in the kernel: worker position `laneId` reads vector position `colBase + laneId`. The kernel does not read a separate matrix column index for each product in that tile. Consecutive-column structure lets it infer the position from the tile's starting column and the worker's position. This depends on the stored entries remaining in the intended tile order. [Pinned kernel](https://github.com/APHETION/Acc-SpMV/blob/93b7138bad9f3adbfbad4d86a362515fd3e4cd93/Acc-SpMV.cu#L301).

For a constructed tile with columns `[5, 6, 7]`, start five plus worker positions zero, one, and two gives the correct vector addresses. For columns `[5, 7, 8]`, the same rule would incorrectly read `[5, 6, 7]`. The contiguity condition is therefore a correctness requirement, not just a performance preference.

Nearby vector addresses make it possible for hardware to service several workers with fewer combined memory transactions. This is called coalesced access. Alignment, active workers, caching, and the hardware's transaction rules still determine the actual transfer count. It is not valid to equate one tile with exactly one external-memory transaction.

### Combining products reduces conflicting output updates

Workers in a tile may target different rows or the same row. Different output destinations allow independent additions. Multiple updates to one destination must not overwrite one another.

An atomic addition prevents one simultaneous update from losing another. If two workers contribute 10 and 33 to an initially zero output, the required result is 43. Uncoordinated read/add/write operations could both read zero and leave only the last writer's value. Atomic updates preserve both contributions, though floating-point update order can still change rounding.

The pinned kernel has direct atomic-update and within-group reduction paths, selected using row-pattern metadata. The reduction paths combine some products before issuing atomic additions. Atomic operations are still present; the implementation does not eliminate every output conflict. [Pinned format selection](https://github.com/APHETION/Acc-SpMV/blob/93b7138bad9f3adbfbad4d86a362515fd3e4cd93/Acc-SpMV.cu#L245); [kernel update paths](https://github.com/APHETION/Acc-SpMV/blob/93b7138bad9f3adbfbad4d86a362515fd3e4cd93/Acc-SpMV.cu#L312).

If eight products share one output row, combining them locally could reduce eight atomic additions to one. It also requires communication and addition within the worker group. If all eight products target different rows, that particular reduction offers no shared-output saving. The best execution choice consequently depends on the pattern, not just the number of nonzeros.

Packing can also reduce unused worker positions. Two four-entry runs occupying separate 32-worker groups use eight of 64 positions; a compatible combined group uses eight of 32. That doubles this simplified occupancy measure, but does not prove a twofold speedup. Reduction cost, register use, memory supply, and the number of groups available to run remain relevant.

### The released program has two execution paths

The inspected program selects its custom path for at most one million parsed nonzeros and CSR5 for larger inputs. It uses double-precision values. CSR5 is a separate sparse representation and implementation path, not evidence that the custom tile kernel handles the whole matrix collection. [Pinned type and threshold definitions](https://github.com/APHETION/Acc-SpMV/blob/93b7138bad9f3adbfbad4d86a362515fd3e4cd93/Acc-SpMV.cu#L16); [dispatch](https://github.com/APHETION/Acc-SpMV/blob/93b7138bad9f3adbfbad4d86a362515fd3e4cd93/Acc-SpMV.cu#L593).

A result averaged across matrices needs per-path accounting. Otherwise, improvements due to the fallback may be mistaken for improvements due to the custom layout. The cutoff is an implementation choice, not a universal mathematical boundary between small and large sparse problems.

### What the timing loop actually includes

The source defines 4,200 warm-up iterations and 1,000 timed iterations. Allocation, input transfers, and the custom metadata-preparation kernel precede the timed region; matrix reordering is a separate program. The measured interval is therefore not the full preparation-and-execution workflow. [Pinned constants](https://github.com/APHETION/Acc-SpMV/blob/93b7138bad9f3adbfbad4d86a362515fd3e4cd93/Acc-SpMV.cu#L24); [custom timing path](https://github.com/APHETION/Acc-SpMV/blob/93b7138bad9f3adbfbad4d86a362515fd3e4cd93/Acc-SpMV.cu#L442).

There is a further asymmetry. The custom path clears its output once before the timed loop, then launches a kernel that atomically adds products on every iteration. The fallback includes an output clear inside every timed iteration. Thus they do not time identical reset work. For exact arithmetic and an otherwise correct custom kernel, 1,000 repetitions would accumulate 1,000 times the single-call result into the final output, rather than leave one result. [Custom timed loop](https://github.com/APHETION/Acc-SpMV/blob/93b7138bad9f3adbfbad4d86a362515fd3e4cd93/Acc-SpMV.cu#L460); [fallback timed loop](https://github.com/APHETION/Acc-SpMV/blob/93b7138bad9f3adbfbad4d86a362515fd3e4cd93/Acc-SpMV.cu#L544).

Both paths copy results to the host, but the inspected functions do not compare them with a reference answer. They print the total timed interval converted from milliseconds to seconds, not explicitly the average latency per multiplication. Dividing the total seconds by 1,000 would be necessary to obtain that average for this loop. These observations identify reproduction questions; they do not establish that the published paper used these exact loops or that its numerical claims are false.

### Keep reported speedups separate from code inspection

The official description reports 2,715 matrices. Average speedups versus cuSPARSE are 2.58×, 1.91×, and 1.78× on RTX 4090, A800, and H100 respectively; versus DASP they are 1.93×, 1.70×, and 1.75×. [DAC description](https://63dac.conference-program.com/presentation/?id=RESEARCH2105&sess=sess127). Baseline versions, per-matrix results, numeric settings, and averaging definitions have not been recovered from the manuscript.

Using ordinary programmable arithmetic units rather than matrix-specialized units does not mean the hardware is universally faster. A sparse matrix–vector job can spend much of its time locating inputs, moving indices, and combining outputs. More peak multiplication capacity helps only if those other operations can supply and consume the work efficiently. The reported comparisons concern particular implementations and workloads.

Preparation also needs repayment. In a constructed scenario, a 20 ms reordering cost and a 0.02 ms saving per multiplication break even at 1,000 uses, before any recurring vector-permutation cost. If each new vector requires another 0.01 ms of extra work, the net saving becomes 0.01 ms and break-even moves to 2,000 uses. Reusing a matrix does not mean every changing vector is already in the right order.

The connection to BSGCN and PFGEMM is that representation and request order jointly determine reuse and useful execution. Acc-SpMV adds a concrete constraint: removing per-entry address lookup is possible only when the stored layout makes addresses recoverable by a simpler rule. Testing whether that benefit survives preparation, validation, and numerical requirements is more informative than treating all sparse speedups as one trend.

No Acc-SpMV preprocessing, GPU kernel, or benchmark was executed. Full-paper recovery, the Acc-SpMV/OmniSpMV naming history, complete reduction correctness, permutation validation, fair timing boundaries, and independent comprehension review remain open.

<span id="explanation-dac-2026-research240"></span>

## LTMiner: share graph-data access without losing distinct time-ordered matches

The [official DAC description](https://63dac.conference-program.com/presentation/?id=RESEARCH240&sess=sess121) calls this accelerator LTMiner. It groups search-tree expansion by graph-data chunks to improve reuse across matching tasks. The DAC manuscript was not recovered. The related [DTMiner paper](https://theqihao.github.io/files/DTMiner.pdf#page=1) is a separate PPoPP publication, with a different title, author list, and DOI. Its selected background below must not be read as LTMiner's hardware specification or evaluation.

### Define the pattern before describing the search

A temporal graph stores interactions with their times. An edge `(u, v, t)` means an interaction from node u to node v at time t. Multiple interactions can connect the same pair at different times. A temporal motif specifies a small connection pattern together with ordering and, where required, duration constraints. [Related background: DTMiner, Section 2.1, printed p. 593, PDF p. 4](https://theqihao.github.io/files/DTMiner.pdf#page=4).

For a constructed example, require three distinct nodes a, b, and c with interactions a→b, then b→c, then a→c. Require strictly increasing times and at most five time units from the first interaction to the last. These are the example's rules, not a recovered LTMiner query definition.

```text
edge 1: u→v at time 1
edge 2: v→w at time 2
edge 3: v→w at time 4
edge 4: u→w at time 5
edge 5: u→w at time 9
```

Starting with edge 1 gives two matches: edges `(1,2,4)` with times `(1,2,5)`, and `(1,3,4)` with times `(1,4,5)`. Both satisfy the node relationships, ordering, and duration. Using edge 5 would span eight time units and fail the duration limit. An interaction w→u would fail the required direction even if its time were suitable.

The two valid matches use the same three nodes but different interaction events. Counting only unique node triples would report one instead of two under this example's event-sequence semantics. The required counting convention therefore belongs in the problem definition, not in an implementation detail. Equal timestamps, repeated nodes, duplicate events, and duration endpoints also need explicit rules.

### Search-tree growth is growth in partial assignments

After selecting edge 1, the search has assigned a to u and b to v, but still needs c and the later interactions. Choosing edge 2 or edge 3 creates two different partial matches. Each partial match must then look for the closing interaction u→w after its own most recent time and within the allowed duration.

These alternatives form a search tree: each child extends one valid partial assignment by another candidate. It is a tree of computational choices, not necessarily a tree in the input graph. A node with many candidate later interactions can create many children. Most may eventually fail a direction, node-mapping, or time constraint.

If an example has ten eligible choices at each of four extension steps, it can expose ten thousand complete combinations before additional filtering. Actual branches can terminate much earlier. Graph size or average degree alone therefore does not determine search cost; query shape, event timing, and partial-match survival matter.

### Why individually sensible searches can repeatedly fetch the same data

Each matching task may need later edges in chronological order. Yet tasks can progress at different rates because their search trees differ. One task may already be examining a late region of the graph while another is still exploring many early alternatives. When they eventually request the same edges, those edges may no longer be in the fast local memory.

Consider three tasks, each requiring data chunks A, B, and C, with capacity to retain only one chunk. A task-by-task traversal requests `ABCABCABC` and needs nine chunk loads under this simplified model. A legal chunk-grouped schedule requests `AAABBBCCC` and needs three loads: keep A while all three tasks use it, then do the same for B and C.

This example saves data loads, not necessarily candidate checks. Distinct partial matches still need their own compatibility tests and counts. Sharing one fetched edge does not make two valid event sequences identical. Whether LTMiner additionally shares computation requires its full algorithm.

### Crossing a chunk boundary requires preserving the unfinished search

Put times 1–3 of the earlier example in one chunk and times 4–6 in the next. The partial match containing edges 1 and 2 must survive the boundary to find edge 4. The partial match containing only edge 1 must also survive if it still needs to consider edge 3. Discarding all unfinished work at the boundary misses valid matches.

A resumable task may need its query position, assigned nodes, selected event identities or equivalent distinguishing state, last timestamp, deadline, and a cursor identifying the next untested candidate. This is a conceptual state requirement, not a recovered LTMiner record layout. The implementation needs enough information both to resume and to avoid counting already explored alternatives twice.

Chronological processing offers a useful bound: once future candidates are beyond a task's deadline, that task cannot obtain a valid later completion under the example's rules. But determining that condition requires valid ordering and a consistent duration convention. A chunk boundary is not itself a deadline.

### The reused graph data must share storage with indices and search state

The related DTMiner software paper explicitly budgets chunk data, index data, and reserved intermediate storage against the last-level cache capacity in Section 4.2.1. Its condition is `chunk bytes + index bytes + reserved bytes ≤ cache bytes`. It also explains the opposing costs of oversized chunks and excessive suspended-task metadata. [DTMiner, printed p. 596, PDF p. 7](https://theqihao.github.io/files/DTMiner.pdf#page=7). This is background evidence for the tradeoff, not proof that LTMiner uses that cache or sizing rule.

For a constructed eight-MiB local store with one MiB of indices and two MiB reserved for task state, at most five MiB remains for chunk data. Allocating an eight-MiB chunk simply because the nominal store is eight MiB ignores other residents. Actual placement, associativity, and competing users can further reduce useful capacity.

Smaller chunks are not automatically better. If each suspended task needed 64 bytes, one million suspended tasks would occupy 64 million bytes, already much larger than the illustrative store. A hardware implementation needs an admission, spill, or scheduling policy when live search state exceeds local capacity. Restricting active tasks can reduce memory pressure but also reduce the number of tasks available to reuse the current chunk.

Thus locality and parallelism are related but not identical. Running more tasks may expose more reuse while increasing state storage and output-count contention. A useful evaluation should separate graph bytes transferred, task-state bytes transferred, candidates tested, and time spent waiting.

### Interpret the unusually wide result ranges cautiously

The DAC description reports speedup ranges of 1.1–652.6× versus software and 1.8–70.3× versus hardware, with respective energy-saving ratios of 3.9–2050.9× and 1.2–17.3×. Baseline identities and per-case conditions are absent. [DAC description](https://63dac.conference-program.com/presentation/?id=RESEARCH240&sess=sess121).

The largest ratio is not a typical result. For example, a 652.6× time ratio leaves about 0.153% of baseline time for that particular comparison, whereas 1.1× leaves about 90.9%. Such a range calls for per-graph, per-query explanations rather than one headline number.

Energy and time extrema must not be paired unless they refer to the same run and measurement boundary. Since energy equals average power multiplied by duration, a faster implementation can save energy while using more instantaneous power. The description does not establish fabrication, clock, storage capacities, host costs, or the power-measurement method.

Fair comparisons need the same graph events, motif definition, counting semantics, time window, precision of timestamps, and exactness requirements. They also need preparation and state-transfer costs. An implementation that counts different event sequences or excludes expensive setup is not directly comparable solely because both are called temporal motif mining.

### What this adds to the sparse-compute explanation

BSGCN reorders requests for graph features; LTMiner coordinates requests generated by growing graph searches. In the latter, scheduling decisions affect both reused data and the amount of unfinished state that must remain alive. This adds a useful comparison dimension: how many bytes of task state must be retained to avoid one repeated graph-data transfer?

One testable hypothesis is that chunk-grouped execution benefits queries with substantial cross-task edge reuse until retained search state or synchronization outweighs the saved transfers. Varying motif shape, duration limit, and chunk size would test that boundary. The available description and related software paper motivate the question; they do not establish a cross-conference long-term trend.

No LTMiner hardware, graph benchmark, or DTMiner implementation was executed. LTMiner's manuscript, exact search-state handling, supported motif semantics, overflow policy, baseline configurations, and independent comprehension review remain open.

<span id="explanation-dac-2026-research2468"></span>

## PillarSparse: simplify the information needed to find sparse operands

PillarSparse proposes the Pillar CSR representation for sparse–dense multiplication and sampled dense–dense multiplication. The [DAC description](https://63dac.conference-program.com/presentation/?id=RESEARCH2468&sess=sess140) describes nonzero-column units, metadata packed into two integers, one fewer dependent pointer lookup, and co-designed execution kernels. Neither the manuscript nor an implementation was recovered. The following examples explain the computation and design constraints; they are not Pillar CSR layouts.

### Sparse–dense multiplication combines vectors through sparse connections

In sparse matrix–dense matrix multiplication, abbreviated SpMM, the sparse matrix identifies which rows of the dense matrix contribute to each output row. Unlike matrix–vector multiplication, each selected input is a vector of several features.

For a constructed example:

```text
A = [2, 0, 3]       B = [1, 2]
    [0, 4, 0]           [3, 4]
                        [5, 6]

Y = A × B
first output row  = 2×[1,2] + 3×[5,6] = [17,22]
second output row = 4×[3,4]             = [12,16]
```

The three stored values of A lead to six scalar products because B has two features per row. If B had 128 features, the same three sparse positions would identify 384 scalar products. Position metadata can therefore be reused across features. The larger feature width also increases input and output traffic, so the metadata's fraction of total work changes with matrix shape.

Grouping nonzeros associated with an input column can make their shared dense input row easier to reuse. But the products may belong to different output rows, requiring correct destination tracking and accumulation. The exact scope of a Pillar unit, including row grouping and boundary information, needs the unrecovered format specification.

### Sampled dense–dense multiplication computes only requested output positions

Sampled dense–dense matrix multiplication, abbreviated SDDMM, has a different meaning. Two dense inputs define dot products, but a sparse pattern selects which output coordinates are needed. Sparsity is in the requested output positions, not necessarily in either numerical input.

Take dense rows `U[0]=[1,2]`, `U[1]=[3,4]`, and `V[0]=[5,6]`, `V[1]=[7,8]`. For the product U × V-transpose, suppose the mask requests only positions `(0,1)` and `(1,0)`. The required dot products are:

```text
output (0,1) = [1,2] · [7,8] = 1×7 + 2×8 = 23
output (1,0) = [3,4] · [5,6] = 3×5 + 4×6 = 39
```

There is no need to produce the unrequested positions merely to discard them. Some SDDMM interfaces also multiply sampled results by stored mask values; this example uses a structural mask with unit values. PillarSparse's exact interface and scaling rules remain unknown.

These two operations often interact in graph computation: selected node pairs can receive scores, and connection-weighted feature vectors can then be aggregated. That connection does not make their kernels interchangeable. One gathers and accumulates along sparse input connections; the other computes dot products at sparse output coordinates.

### Why locating operands can require several dependent reads

A pointer lookup reads information that identifies where another piece of information resides. For an illustrative nested format, the program might first read a row's group index, then that group's descriptor, then an array location for the values. If the address of each read depends on the preceding result, those reads cannot all be issued immediately for that one task.

With an assumed 100-cycle latency for each of three dependent reads, the isolated chain takes 300 cycles before the final information is ready. Removing one level would reduce that illustrative chain to 200 cycles. It would not imply a 1.5× application speedup: other tasks can overlap some waiting, caches can change latency, and arithmetic or bandwidth can dominate elsewhere.

Packing required descriptor fields together can remove an indirection and allow a wider load to retrieve several fields. But the exact savings depend on what was previously loaded, whether the data was already cached, and how the new fields are decoded.

### Two integers is not a complete encoding specification

The description's two-integer claim leaves their widths and field assignments unspecified. It must not be restated as exactly eight bytes, nor as two integers for an entire matrix. The granularity to which the claim applies needs the full paper. [DAC description](https://63dac.conference-program.com/presentation/?id=RESEARCH2468&sess=sess140).

For an independent packing example, a 32-bit word could reserve 20 bits for an offset and 12 for a count. Encoding offset 700 and count 9 as `(700 << 12) | 9` gives 2,867,209. Shifting right by 12 retrieves 700; masking the lowest 12 bits retrieves 9. The ranges would be limited to offsets below 1,048,576 and counts below 4,096.

That example shows what packing must specify: field widths, units, bounds, reserved codes, and what happens when a value exceeds the range. It does not reveal PillarSparse's fields. Bit packing can require masks and shifts while still saving dependent loads; the relevant comparison is total decoding and access cost, not whether decoding disappears.

A single vectorized load is also not necessarily a single external-memory transaction. Alignment, cache-line boundaries, and simultaneous requests from other workers affect physical transfers. Removing an instruction, an address dependency, and a memory transfer are three distinct claims.

### Separate data-moving workers from arithmetic workers

The description names a producer–consumer pipeline with specialized worker groups and a Tensor Memory Accelerator, or TMA. It also names Thrust primitives for conversion without specifying the sequence. [DAC description](https://63dac.conference-program.com/presentation/?id=RESEARCH2468&sess=sess140).

As hardware background, NVIDIA describes Hopper TMA as an asynchronous engine for moving tensor regions between memory spaces, allowing designated workers to initiate movement while others compute. Completion still needs synchronization before consumers use the data. This documents the facility, not PillarSparse's particular transfers or GPU configuration. [NVIDIA Hopper guide, Section 1.4.1.2](https://docs.nvidia.com/cuda/hopper-tuning-guide/index.html#tensor-memory-accelerator).

In a constructed pipeline, loading one tile takes six time units and computing it takes four. Sequentially processing ten tiles takes 100 units. Perfect overlap after startup gives `6 + 4 + 9×6 = 64`, not 40, because loading limits the rate. Achieving that overlap requires separate storage for data being loaded and data still being consumed, plus correct handoff and buffer-reuse rules.

Tensor arithmetic units operate on supported matrix shapes and numeric formats. Irregular sparse work must be arranged into suitable operands or handled by additional instructions. If a hypothetical 16-position arithmetic block contains only four useful entries, at most 25% of those positions are useful under that simple mapping. A faster arithmetic unit can still be worthwhile, but its peak rate alone does not prove useful sparse throughput. PillarSparse's tile shapes, padding, and precision remain unrecovered.

### Conversion changes the complete-workflow result

An efficient execution format can require sorting, grouping, indexing, or allocating new arrays before use. Mentioning a parallel-library primitive does not establish the conversion's time, temporary-memory requirement, or behavior for a changing sparsity pattern.

For an illustrative static pattern, a 5 ms conversion cost and 0.05 ms saved per execution break even after 100 uses. If each sampled graph batch creates a new pattern used once, the same numbers lose 4.95 ms per batch. Changes only to values may permit some metadata reuse, whereas changes to positions can require rebuilding it; the implementation must establish which updates it supports.

The useful comparison is therefore both kernel-only and complete workflow: starting from the application's actual input representation, preparing the format, computing required outputs, and returning them in the required order and precision. Peak temporary memory belongs in that accounting too.

### What evidence is still needed for the paper and the trend

The official description gives no numerical benchmark results or baseline names. A qualitative performance statement cannot support a specific speedup, energy saving, or universal ranking. Required evidence includes matrix dimensions, feature widths, sparsity patterns, numeric types, GPU model, software versions, conversion frequency, and output checks.

Acc-SpMV simplifies vector addressing through consecutive-column layout. PFGEMM shares index prefixes. PillarSparse targets descriptor organization and dependent metadata access. Together they motivate a sharper hypothesis than “sparse formats are improving”: the best representation depends on whether the workload is limited by bytes transferred, dependent address discovery, or arranging operands for the arithmetic unit.

That hypothesis needs controlled measurements varying pattern and feature width while separating conversion, metadata decoding, data movement, and arithmetic. The currently recovered descriptions do not establish a longitudinal trend or a common winning format.

No PillarSparse conversion, GPU kernel, or benchmark was executed. Exact Pillar CSR encoding, numerical semantics, preparation costs, evaluation conditions, and independent comprehension review remain open.

<span id="explanation-dac-2026-research2717"></span>

## Sparse 3D operator acceleration: separate less data movement from changed arithmetic

This is Hongjin Zhong and colleagues' paper, “Operator-Level Acceleration for Sparse 3D Object Detection.” The [official description](https://63dac.conference-program.com/presentation/?id=RESEARCH2717&sess=sess177) combines attention fusion, approximate convolution replacement, and selective lower precision without retraining. No full manuscript or implementation was recovered. The calculations below explain those distinct design choices; they are not reconstructions of the paper's kernels.

### What a sparse 3D detector represents

A 3D detector estimates objects' locations, sizes, directions, and categories from spatial observations. In a voxel representation, space is divided into cells, and each active cell carries coordinates and a vector of features. A feature channel is one component of that vector. It is not another spatial axis.

Sparse storage can retain only active cells instead of allocating features everywhere. For a constructed grid with one million cells, 64 four-byte features per cell would occupy 256 million bytes if stored densely. Ten thousand active cells require 2.56 million bytes for feature values, plus coordinates, indices, and other metadata. The reduction does not mean the remaining computation is 100 times faster: finding neighbors and assembling their features can introduce irregular access.

Empty space and redundant feature information are also different. Absence of a cell can justify omitting some operations under the model's sparse-convolution rules. Similarity between two nonempty cells does not make them interchangeable without an approximation argument.

### An operator is one calculation inside the complete detector

The detector executes many operations: locating or grouping cells, combining features, computing attention, transforming coordinates, predicting boxes, and filtering predictions. An operator-level optimization changes one such calculation or its implementation. Its speedup applies first to that measured component.

Attention forms weighted combinations of features. A slot-based implementation can aggregate many input features into a smaller set of intermediate feature groups. The paper's exact slot assignment, normalization, and tensor decomposition remain unavailable. A generic weighted-sum example is sufficient to expose an important fusion constraint.

Suppose three scalar features are 10, 20, and 40, with unnormalized positive weights 2, 3, and 5. Their normalized aggregate is `(2×10 + 3×20 + 5×40)/(2+3+5) = 28`. An implementation could materialize intermediate weights and weighted values in memory, then read them for reduction. A fused implementation can instead accumulate the numerator and denominator while processing smaller pieces.

Split the inputs into a first tile containing the first two features and a second containing the last. Their numerator/denominator pairs are `(80,5)` and `(200,5)`. Combining those pairs gives `280/10 = 28`. Independently normalizing each tile and adding its answer gives `16+40 = 56`, which is wrong. The normalization domain must survive the tiling transformation.

Actual attention may obtain weights through exponentials and require stable rescaling across tiles. The example does not establish the paper's algorithm, but it shows what needs proof: the same contributing elements, normalization, masks, and output accumulation, with separately specified floating-point tolerance.

### Fusion can reduce storage without deleting model information

If an intermediate holds N groups of d four-byte values, its value storage alone is `4×N×d` bytes. For illustrative N=100,000 and d=1,024, that is 409.6 million bytes. Avoiding a complete write and reread could remove 819.2 million transferred bytes at that storage boundary, assuming each would otherwise occur once.

These numbers are not the paper's tensor dimensions or traffic measurements. They explain why eliminating an intermediate can matter even if the number of arithmetic operations barely changes. Smaller tiles can keep temporary results closer to the arithmetic units, but require buffers, handoffs, and enough local storage. Oversized tiles can consume registers or shared memory and reduce concurrent work.

The right validation compares outputs as well as allocations and traffic. Successful fusion is not established merely by using fewer kernels or making a previously oversized case fit in memory.

### Spatial convolution and channel operations have different information

A spatial convolution combines features from nearby coordinates. An operation confined to channels at one coordinate combines components of that cell's feature vector. These calculations cannot generally substitute for one another on arbitrary inputs.

Consider a one-dimensional spatial slice as a constructed counterexample. A three-position sum at the center gives 10 for neighbor values `[0,10,0]` and 30 for `[10,10,10]`. Both cases have the same center value, 10. A deterministic function that sees only the center value must return the same answer for both, so it cannot reproduce both spatial sums exactly.

Earlier attention could make a cell's features carry information about its neighbors. That makes a cheaper substitute plausible for a particular trained model and input distribution; it does not establish a universal identity between spatial and channel operations. The exact preceding features, replacement weights, and measured error are necessary evidence.

The description explicitly proposes replacing 3D axial convolutions with lightweight channel operations. Its statement about preserving architecture therefore needs a precise level of interpretation: the broad network arrangement may remain, while the implemented operator changes. Likewise, no retraining means no further weight-training step is claimed, not unchanged predictions. [DAC description](https://63dac.conference-program.com/presentation/?id=RESEARCH2717&sess=sess177).

### Lower precision changes both storage and numerical resolution

FP16 uses fewer bits per value than FP32. That can reduce transfer volume and enable faster arithmetic on supporting hardware. It also changes representable values, rounding, and range. Whether an error matters depends on how the value is used downstream, not only on the number of bits saved.

In standard binary16, the spacing near 1,000 is 0.5. Values 1,000 and 1,000.1 both round to 1,000 under round-to-nearest. If their difference encodes a small geometric displacement, converting first can erase that displacement. By contrast, representing an already centered offset near zero can have different resolution. This is an illustrative reason to inspect coordinate scaling and representation before assigning precision.

The description keeps geometric encoders in FP32 and assigns FP16 selectively elsewhere. [DAC description](https://63dac.conference-program.com/presentation/?id=RESEARCH2717&sess=sess177). That is a reported policy, not a verified guarantee for every geometric calculation. Input precision, multiplication precision, accumulator precision, and stored output precision may differ within an operator and must be specified separately.

Changing one operator at a time can reveal sensitivity, but individually small errors can interact when changes are combined. Thresholds for selecting boxes can turn a small score change into a different detection set. Evaluation therefore needs the combined configuration and per-class outcomes, not only isolated operator error.

### Explain the quality numbers before calling the loss small

Mean average precision, or mAP, summarizes detection precision across recall levels and classes under a matching protocol. Precision concerns how many reported detections are correct; recall concerns how many reference objects are found. It is not simply the percentage of correctly classified input frames.

For nuScenes, detection matching uses ground-plane center distance, and NDS combines mAP with measures of location, scale, orientation, velocity, and attribute error. These are metric definitions, not confirmation of the paper's dataset split or evaluation implementation. [Official nuScenes detection metrics](https://www.nuscenes.org/object-detection?externaIData=all&mapData=all&modalities=Any).

The description reports quality within 4% mAP and 2.5% NDS, but does not resolve relative percentages versus percentage points. [DAC description](https://63dac.conference-program.com/presentation/?id=RESEARCH2717&sess=sess177). Starting from mAP 60 on a 0–100 scale, a four-point loss gives 56; a four-percent relative loss gives 57.6. Those are different outcomes. Neither statement means that at most four percent of individual objects change predictions.

Calling a loss negligible requires an application criterion. An aggregate can conceal a larger loss for a rare class or distant objects. The available description cannot establish acceptable deployment behavior from those aggregate bounds alone.

### Operator ratios must not be multiplied into a detector speedup

The description reports attention speedups up to 50.8×, convolution acceleration of 1.2–2×, precision-related speedup of 1.93–2.19×, and 2.1–2.5× end-to-end improvement. It names A100 and writes “GTX 4090”; that latter device label needs clarification rather than silent correction. Baseline models and detailed conditions remain unrecovered. [DAC description](https://63dac.conference-program.com/presentation/?id=RESEARCH2717&sess=sess177).

Different operator ratios concern different portions of execution and may overlap in their effects. For a constructed 100 ms detector spending 20 ms on attention, making only attention 50 times faster leaves `80 + 20/50 = 80.4` ms, about 1.24× overall speedup. A large component ratio is consistent with a much smaller total gain.

Nor does 2.5× inference acceleration establish 2.5× sensor-to-output acceleration if transfers and preprocessing are excluded. A fair report needs batch size, active-cell count, feature width, precision, warm-up, synchronization, and the full measurement boundary, alongside the same quality protocol for each configuration.

This paper connects sparse-compute scheduling with approximate-and-precision-aware computation. Attention fusion should be assessed as a transformation of execution and storage; convolution replacement and reduced precision additionally need quality accounting. Keeping these categories separate is essential before combining papers into a long-term claim about efficient perception.

No sparse 3D detector, approximation, precision experiment, or GPU benchmark was executed. Full-paper recovery, operator identities, normalization rules, replacement semantics, precision boundaries, metric units, device identity, and independent comprehension review remain open.

<span id="explanation-dac-2026-research588"></span>

## Florella: share arithmetic hardware across different graph operations

Florella combines a declarative representation called sliding reduction convention with an architecture centered on a Jacobian-logarithm unit. The description attributes hardware reuse to logarithmic transformations and approximation. [Official DAC description](https://63dac.conference-program.com/presentation/?id=RESEARCH588&sess=sess156). No manuscript or implementation was recovered. The explanations and numbers below are mathematical teaching examples, not Florella instructions, circuits, or measured traces.

### One graph layer can require several different kinds of calculation

A graph stores nodes and their connections. Each node can have a vector of features. A graph-neural-network layer may transform each vector, combine vectors from connected nodes, normalize the combination, and apply a nonlinear function. These steps need different arithmetic and different access patterns.

For an example, two neighbors have features `[2,4]` and `[6,8]`. Their sum is `[8,12]`; their mean is `[4,6]`; a weighted combination with coefficients 0.25 and 0.75 is `[5,7]`. Those results are not interchangeable. A hardware representation must specify the contributing inputs, the operation that combines them, and any normalization or final transformation.

A reduction combines several inputs into fewer outputs, as a sum or maximum does. A dense matrix multiplication reduces over matching feature positions; graph aggregation reduces over selected neighbors. Both contain reductions, but they traverse different sets. A uniform description could make these common elements explicit while retaining their different indexing rules.

That is the conceptual purpose of an operation-description language. It must carry enough information to preserve the computation while allowing the implementation to choose a schedule. The source does not disclose Florella's syntax or the meaning of its sliding boundaries. It would be unjustified to identify those boundaries with a conventional fixed-size moving average merely because the name includes “sliding.”

### Why one accelerator per operation can add communication

Suppose one hardware block computes feature transforms and a different block computes graph aggregation. The intermediate vectors must pass between them, along with enough information to identify their nodes and layout. If the blocks cannot directly share local storage, an implementation may write those vectors to another memory and read them back.

For a constructed intermediate of 100,000 nodes, 64 features, and four bytes per feature, values alone occupy 25.6 million bytes. One complete write and reread transfers 51.2 million bytes. A more integrated design might avoid some of that movement by keeping an intermediate near its next consumer. That does not remove transfers required by true dependencies or by limited storage.

Reusing one arithmetic unit can also avoid duplicating circuitry that is idle during other phases. It can create contention: two operations that separate units could execute concurrently may have to take turns on the shared unit. Hardware reuse is therefore a tradeoff among area, transfer cost, concurrency, and control—not automatically a speedup.

### Logarithms change which operations are simple

A logarithm represents a positive number by the exponent needed to produce it. Using natural logarithms, let `a = ln(x)` and `b = ln(y)` for positive x and y. Multiplication becomes addition in this representation: `ln(xy) = a+b`. Returning to the original number requires exponentiation.

Addition is less direct. To add x and y, the logarithmic result is `ln(exp(a)+exp(b))`. Define `m = max(a,b)`. Factoring out `exp(m)` gives the exact identity:

```text
ln(exp(a) + exp(b))
    = max(a,b) + ln(1 + exp(−abs(a−b)))
```

The correction depends only on the distance between a and b. This gives a mathematical reason for designing shared comparison, subtraction, and correction-function circuitry. It does not establish Florella's logarithm base, number format, correction approximation, or supported operators.

Take x=2 and y=3. The correct logarithmic sum is ln(5). Keeping only the larger logarithm gives ln(3), which converts back to 3 rather than 5: a 40% error in this example. When x=y=2, omitting the correction gives 2 rather than 4, a 50% error. The correction is largest for equal inputs, where it is ln(2).

If a and b differ by ten, the correction is `ln(1+exp(−10))`, approximately 0.0000454 in natural-log units. Its small size in that case explains why an approximation might depend on the input difference. It does not justify dropping it everywhere, and this omission is not asserted to be Florella's method.

### Zero, negative values, and cancellation need explicit treatment

Real logarithms of positive values do not directly encode negative numbers. Zero has no finite logarithm. Graph-network features and weights can contain both, so a general implementation needs special-value rules and a way to preserve signs or otherwise handle these cases.

For opposite-signed contributions 100 and −99, the answer is 1. Treating both magnitudes as positive gives 199, which is not an approximation of the same signed sum. Even preserving signs, small magnitude errors can dominate the result after cancellation: using 100.5 and −98.5 gives 2, a 100% relative error despite each magnitude changing by less than one percent.

This is why testing only positive sums or average operator error is insufficient. Required tests include zeros, near cancellation, extreme magnitudes, repeated reductions, and conversions between representations. The error should then be evaluated in complete graph models, where normalization and nonlinear functions can change its effect.

The term Jacobian-logarithm does not mean that the hardware necessarily computes a matrix of derivatives. The relevant question here is the arithmetic identity and how the unit approximates and composes it. Those implementation details remain missing.

### Unified mapping still has to preserve boundaries and dependencies

Even an exact pairwise arithmetic identity does not define a whole operator. A mean also needs a count; attention needs its normalization domain; a maximum over an empty set needs a specified convention. Different graph nodes can have different neighbor counts, including no neighbors. The mapping must preserve these cases.

The description uses “atomic mapping” of macro-operations. Without the manuscript, that phrase cannot be assumed to mean a memory atomic instruction, transactional execution, or an operation completed in one cycle. It is a mapping claim whose exact meaning needs recovery. [DAC description](https://63dac.conference-program.com/presentation/?id=RESEARCH588&sess=sess156).

There is also a storage question. Keeping several operators on one architecture can reduce communication between devices while still writing intermediates within that architecture. The evaluation must identify the boundary at which traffic is counted and whether all operators in the claimed workload are supported without fallback.

### Interpret the three reported ratios separately

The description reports average 2.2× speedup, 2× lower memory traffic, and 3.3× higher performance density against four unnamed accelerators. Models, precision, quality changes, process, clock, area accounting, and aggregation method are unavailable. [DAC description](https://63dac.conference-program.com/presentation/?id=RESEARCH588&sess=sess156).

Interpreting traffic reduction as baseline bytes divided by new bytes gives half the traffic. A 2.2× speed ratio leaves about 45.5% of baseline time. These ratios describe different, potentially overlapping effects and cannot be multiplied into a 4.4× combined speedup.

Performance density generally needs both useful performance and an area denominator, but the paper's definition must be checked. For a constructed pair, increasing throughput from 100 to 220 jobs per second while reducing area from three to two square millimeters raises throughput per area from 33.3 to 110, or 3.3×. This shows how the units relate; it is not a reconstruction of Florella's area. Aggregate ratios from several baselines cannot safely be inverted to infer an unreported chip size.

No Florella implementation, graph inference, arithmetic circuit, simulation, or synthesis was executed. The language definition, operator coverage, logarithmic encoding, approximation error, fallback paths, hardware conditions, and independent comprehension review remain open.

<span id="explanation-dac-2026-research680"></span>

## SPADE: decide which attention blocks to compute, then account for that decision

The recovered [SPADE manuscript](https://arxiv.org/pdf/2608.03335v1#page=1) carries the DAC publication identity and DOI 10.1145/3770743.3804015. The explanation below uses page locators rather than only the program description. Its worked examples are constructed reasoning, not reproduced model outputs. The linked implementation has not been inspected or executed in this pass.

### Start with what attention does to one video token

A video model processes feature vectors representing portions of a compressed video representation. A token identifies one such vector, not necessarily one raw pixel or one frame. Attention allows a token to combine information from other tokens, potentially across both spatial positions and time.

Each token has a query vector Q that is compared with key vectors K. Those comparisons produce scores. Softmax converts scores into nonnegative weights summing to one, and the output is the weighted sum of value vectors V. The paper states the dense and masked forms in Equations 1–2. [PDF p. 2](https://arxiv.org/pdf/2608.03335v1#page=2).

For a scalar teaching example, attention weights `[0.8,0.15,0.05]` applied to values `[1,2,100]` produce `0.8 + 0.3 + 5 = 6.1`. The smallest weight contributes most to the output because its value is large. A low attention weight alone does not guarantee a negligible output contribution.

If the final position is removed and the remaining weights renormalized, the output becomes `(0.8+0.3)/0.95`, approximately 1.158. Removing five percent of the weight mass has changed the output substantially in this example. Sparse attention therefore needs a quality argument, not only a count of omitted products.

### Why blocks make skipping work easier to execute

With N query tokens and N keys, dense attention considers N² token pairs per head. For N=4,096, that is 16,777,216 pairs. A hypothetical fully materialized two-byte score array would occupy 32 MiB per head. Streaming implementations can avoid storing that whole array while still evaluating the pairs; less storage is not automatically less arithmetic.

Partitioning those tokens into blocks of 64 yields 64 query blocks and 64 key blocks. A block mask has 4,096 possible block pairs. Keeping sixteen key blocks for each query block retains one quarter of those pairs. It can remove arithmetic in larger, more regular pieces than selecting individual tokens independently.

That example's 75% omitted pairs would imply at most a fourfold arithmetic reduction for the affected pair work. It says nothing yet about selection, rearrangement, normalization, launches, or other model operations. If the retained fraction stays fixed as N grows, pair work still grows quadratically. Linear growth requires stronger assumptions, such as a bounded number of attended keys per query, together with bounded selection costs.

### Choose blocks that preserve useful local structure

SPADE considers spatial, temporal, and mixed 3D partitions, then uses summaries and head-specific policies to choose attention masks. [PDF p. 3, Figure 3 and Section 3.1](https://arxiv.org/pdf/2608.03335v1#page=3).

Why can the partition matter when block sizes are equal? Tokens close in an image may have similar features in one scene, while tokens tracking slowly changing content across frames may be more similar in another. A summary of a coherent group can represent its members better than a summary mixing unrelated vectors. This is a rationale for input-dependent grouping, not a guarantee that nearby tokens have interchangeable effects.

A summary deliberately loses information. The mean of `[1,0]` and `[−1,0]` is `[0,0]`. Its dot product with `[10,0]` is zero, although the two original dot products are 10 and −10. Their exponentials differ greatly. Estimating attention from a mean cannot generally recover every individual attention relationship. Alternative summaries preserve different information and have different costs.

### Compute the similarity score without building every pair

SPADE's SICS score sums within-block cosine similarities; Equation 5 and Algorithm 1 compute it using running sums. [PDF p. 4](https://arxiv.org/pdf/2608.03335v1#page=4).

The arithmetic can be derived directly. Normalize each nonzero vector to unit length and call the results u₁ through uB. The sum of all pairwise dot products is also the squared length of their sum:

```text
SICS = sum over i,j of dot(ui,uj)
     = dot(u1 + ... + uB, u1 + ... + uB)
```

For two aligned vectors `[1,0]` and `[1,0]`, the sum is `[2,0]` and its squared length is four. For opposite vectors `[1,0]` and `[−1,0]`, it is zero. For perpendicular vectors `[1,0]` and `[0,1]`, it is two. The score includes each vector's similarity to itself, not only similarities between distinct vectors.

With a running sum r of preceding normalized vectors, adding a new vector u contributes `2×dot(r,u)+1` to the score. The final one is its self-dot-product. This avoids explicitly constructing the B-by-B matrix of pairwise similarities: it requires work proportional to B times feature width, rather than B² times feature width, apart from implementation details.

Exactness of that algebra does not establish the selection heuristic's accuracy. Cosine similarity ignores magnitude: `[1,0]` and `[100,0]` have identical direction, but their dot products with key `[0.1,0]` are 0.1 and 10. A highly coherent query block can still contain very different attention scores. SICS is not a proof of preserved output or generation quality.

Zero-length vectors also need an explicit implementation rule because normalization divides by their length. Finite precision can affect the equivalence of different accumulation orders. Those numerical safeguards have not been checked in code here.

### The retained mask is a union, not a sum of sparsity percentages

The paper combines selected inter-block and intra-block positions with local-window and attention-sink masks, then executes the resulting block-sparse pattern. [PDF pp. 4–5, Section 3.3](https://arxiv.org/pdf/2608.03335v1#page=4).

Top-K retains a specified number of candidates. A cumulative-threshold rule can retain a varying number depending on its score distribution. Neither establishes the true attention mass retained unless the ranking scores and their normalization have the necessary relationship to full attention.

Suppose one rule retains block identifiers `{1,2}` and another retains `{2,3}`. Their union is `{1,2,3}`, not four distinct blocks. Different rules overlap, so their individual percentages cannot simply be added. Conversely, adding a mandatory local region can prevent a nominal pruning target from being reached.

A retained block includes its full supported tile of pairs, even if only a few individual pairs drove its importance score. This trades fine-grained selectivity for regular execution. The block shape, data ordering, and retained-mask layout therefore matter to runtime as well as quality.

### Faster mask selection is not free mask selection

The remaining workflow includes evaluating candidate partitions, summarizing tokens, ranking or thresholding scores, assembling indices, arranging operands, and running attention. A good sparse kernel does not make those other steps disappear.

For a constructed case, dense attention takes 100 time units. Sparse pair computation takes 20, but selection and layout take another 15. The resulting speedup is `100/35`, about 2.86×, not the fivefold reduction suggested by pair computation alone. If shorter inputs reduce dense attention to ten units while setup still costs 15, the sparse path can lose time.

Grouping compatible heads can give each launch more work, but different heads may choose different schemes. Grouping must preserve which query, key, value, mask, and output belong together. A rearrangement also needs to restore outputs to the model's expected order. These are correctness obligations as well as execution costs.

### Separate standard SPADE from the faster Turbo policy

The evaluation uses H800 80 GB/CUDA 12.8. Standard execution retains dense attention for the first 30% of text-to-video steps or 25% of image-to-video steps; Turbo sparsifies after the first step. [PDF p. 5, Section 4.1](https://arxiv.org/pdf/2608.03335v1#page=5).

This difference changes how often approximation enters the iterative generation process. An early change can alter subsequent inputs, so its effect is not limited to one isolated attention call. Training-free means the acceleration does not require another training run; it does not mean identical generated video.

The clearest paired evidence is Hunyuan-T2V in Table 2:

| Configuration | End-to-end speedup | SSIM to dense output | LPIPS to dense output | VBench |
| --- | --- | --- | --- | --- |
| Standard SPADE | 1.49× | 0.91 | 0.08 | 0.76 |
| SPADE-Turbo | 1.80× | 0.57 | 0.43 | 0.79 |

[Manuscript p. 6, Table 2](https://arxiv.org/pdf/2608.03335v1#page=6).

The fidelity metrics worsen markedly for Turbo: higher SSIM and lower LPIPS indicate greater similarity to the dense reference. The VBench score nevertheless increases. These observations answer different questions. A generated video can score well on a quality benchmark while differing substantially from a particular dense-generated video. The row does not establish unchanged content or universal superiority.

The abstract's 1.49–1.80× headline must not be attributed wholly to standard SPADE. Across Table 2, standard end-to-end ratios span 1.32–1.49×; Turbo spans 1.49–1.80×. [PDF p. 6](https://arxiv.org/pdf/2608.03335v1#page=6). The paper also uses inconsistent ranges in introductory prose; the table keeps the variants and individual measurements distinguishable.

### What transfers to the broader research question

SPADE makes selection overhead and approximation frequency part of the same systems problem. It connects to PillarSparse through the cost of metadata and block execution, and to the precision-aware chapter through the need to account for quality changes. The transferable question is not simply how much attention can be removed, but how cheaply useful blocks can be identified and how often approximation can be applied within a complete generation run.

Evidence for a durable trend would require matched prompts, seeds, model versions, steps, resolution, precision, and measurement boundaries. Fidelity and perceptual quality should remain separate, and early dense steps must be included in sparsity and timing accounting. A single-layer sparsity percentage does not describe the full denoising schedule.

No SPADE code, attention kernel, or video-generation benchmark was executed. Exact policy configuration, zero-vector safeguards, reproducibility details, measurement boundaries, and independent comprehension review remain open. The manuscript strengthens the explanation; it does not constitute reproduction or independent acceptance.

<span id="explanation-dac-2026-research935"></span>

## SALUT: start ready factorization tasks without waiting for unrelated work

### What the available source establishes

SALUT targets sparse LU factorization on FPGAs with high-bandwidth memory. Its proposed mechanisms are precompiled dependency management, task activation separated from dependency resolution, and locality-aware balancing with two queues. The official description reports geometric-mean throughput and energy-efficiency ratios over fifteen matrices: 4.0× and 6.5× against cuDSS on RTX A6000, and 3.7× and 4.7× against cuDSS on Tesla V100. [Official DAC description and authors](https://63dac.conference-program.com/presentation/?id=RESEARCH935&sess=sess175)

The full manuscript and implementation were not recovered in the 2026-09-07 search. No manuscript page citations are available. FPGA model, precision, matrix identities, pivot policy, queue rules, preparation costs, and measurement boundaries remain unknown. The examples below are independent mathematical and scheduling explanations, not reconstructed SALUT algorithms or results.

### Begin with the equations being solved

A linear system asks for unknown values that satisfy several equations together. Consider `2x₁ + x₂ = 3` and `4x₁ + 3x₂ = 7`. The coefficients form a matrix `A`, the unknowns form a vector `x`, and the right-hand sides form a vector `b`. The compact expression is `Ax = b`.

Subtracting twice the first equation from the second gives `x₂ = 1`. Substituting that value into the first gives `x₁ = 1`. Elimination removes an unknown from a later equation using an earlier one.

LU factorization records these operations as two triangular matrices. A lower triangular matrix has zeros above its diagonal; an upper triangular matrix has zeros below it. For this example:

```text
A = [2  1]     L = [1  0]     U = [2  1]
    [4  3]         [2  1]         [0  1]

A = L U
```

Multiplying `L` and `U` reproduces `A`: the second row is twice the first row of `U` plus its second row, giving `[4, 3]`. The multiplier 2 in `L` records the elimination step.

Once these factors exist, solve `Lz = b` first. Its first equation gives `z₁ = 3`; its second gives `2·3 + z₂ = 7`, so `z₂ = 1`. Then solve `Ux = z`, starting at the bottom: `x₂ = 1`, followed by `2x₁ + 1 = 3`. This is why factorization and solving are distinct costs. If only `b` changes, the same numerical factors can serve another solve. If coefficients in `A` change, numerical factorization generally must be repeated, even if some structural preparation can be reused.

### Sparse input can produce new nonzero entries

A sparse matrix omits many zero coefficients. That reduces initial storage, but elimination can create nonzero values at positions that started as zero. These new entries are called fill-in.

For an independent example, take:

```text
A = [2  1  1]
    [1  2  0]
    [1  0  2]
```

The first elimination multiplier for both later rows is `1/2`. Subtracting half the first row from the second changes its last entry from zero to `0 − (1/2)·1 = −1/2`. The third row's middle entry changes in the same way. An implementation that reserves space only for the original nonzeros cannot simply discard these results and remain an exact factorization method.

The pattern of entries also determines which later operations need earlier results. A worker cannot divide by a diagonal entry before the updates determining that entry have finished. Nor can it use an elimination multiplier before that multiplier has been computed. The task structure depends on the elimination ordering, fill pattern, and numerical rules—not merely on how many zeros the input contains.

### Remove a broad wait, not a true dependency

Suppose independent tasks A and B begin at time zero. A takes two time units and B takes ten. Task C takes three units and needs only A's output. Assume enough workers and no communication cost.

| Task | Required predecessor | Start with a barrier after A and B | Start when its own inputs are ready |
| --- | --- | ---: | ---: |
| A | None | 0 | 0 |
| B | None | 0 | 0 |
| C | A only | 10 | 2 |

A barrier requires the whole group to finish before the next group starts. Under that rule, C finishes at time 13. With individual readiness tracking, C finishes at time 5 and the whole job finishes when B does, at time 10. The improvement comes from removing an unnecessary relationship between B and C; no arithmetic became faster.

If C actually needs B's output too, starting it at time 2 is incorrect. If every task forms one long chain, individual activation cannot create parallel work. This distinction is central to judging any dependency-aware accelerator: fewer synchronization instructions do not prove that all required ordering survives.

### What dependency preparation must preserve

One possible design—not a verified SALUT implementation—stores a count of unfinished predecessors for each task. A task with two required inputs begins with a count of two. Each distinct predecessor completion reduces that count once. Reaching zero can make the task eligible for execution.

Several conditions are necessary. Completion must mean that the output is available to its consumer, not merely that the producer has started. Two simultaneous updates to the count must not overwrite each other. A repeated notification must not make a task ready early. The task must not be activated twice. Publishing a completion flag before publishing the data can expose stale values even if the count itself is correct.

Preparing dependency lists ahead of execution can avoid rediscovering relationships repeatedly. It does not eliminate the cost of storing those lists, delivering notifications, or ensuring that the preparation still matches the numerical problem.

Pivoting illustrates the last issue. The matrix `[[0,1],[1,1]]` is nonsingular, but an elimination procedure that begins by dividing by its top-left entry encounters zero. Swapping rows supplies a usable first pivot. In larger problems, row choices can depend on numerical values, including whether a candidate is too small for stable division. A schedule prepared from a fixed pattern therefore needs a stated compatibility rule for pivoting, or a supported restriction on inputs. SALUT's available description does not resolve this issue.

### Scheduling capacity and memory locality are separate limits

High-bandwidth memory provides substantial transfer capacity through multiple channels. It cannot make an unfinished operand ready. Many workers also cannot overcome a dispatcher that releases tasks too slowly.

As an independent capacity example, suppose eight workers each complete one task per cycle, while a dispatcher supplies only one ready task per cycle. Sustained execution cannot exceed the dispatcher's rate, regardless of the workers' combined arithmetic capacity. Distributed activation may address that limit, but shared queues, completion counters, and memory channels can become new constraints.

Moving ready tasks between workers can reduce idle time while increasing transfers. Suppose one worker already holds a task's operands but remains busy for four time units. Another is idle, yet fetching those operands takes six. For an otherwise identical two-unit computation, staying local finishes in six units; moving finishes in eight. If the local wait instead becomes twenty units, moving can help. A useful balancing rule must consider both waiting and movement, not simply assign work to the first idle worker.

Two queues alone do not establish such a rule. Their membership, capacity, priority, ownership, and handling of congestion matter. A scheduler also needs a progress guarantee: continually preferring local tasks must not leave a remote ready task waiting forever.

### How to read the reported ratios

Geometric means summarize multiplicative ratios, not total application runtime. For two illustrative matrices with speed ratios 4 and 1/4, the geometric mean is `sqrt(4·1/4) = 1`. That summary includes one large gain and one large loss; it does not mean both matrices run equally fast on the two systems. Individual results and their distribution are needed alongside the mean.

Factorization throughput must also remain separate from complete-system speed. If factorization originally takes 40 milliseconds of a 100-millisecond job, making only that part four times faster gives `60 + 40/4 = 70` milliseconds overall, or about 1.43× speedup. Analysis, transfers, factorization, triangular solves, and validation need explicit timing boundaries.

Preparation can change the result further. An illustrative 20-millisecond setup cost with a one-millisecond saving per subsequent factorization requires twenty compatible repetitions to break even. A changed sparsity pattern or value-dependent ordering may invalidate that setup. Reusing the same factors for new right-hand sides is a different reuse case and should not be counted as repeated factorization savings.

Energy efficiency also requires the measured work and power boundary: accelerator-only power, memory power, and whole-system energy are not interchangeable. Numerical verification should report residuals, such as the size of `Ax − b` relative to the problem scale, together with precision and stability conditions. A small residual alone does not guarantee a small error in `x` for an ill-conditioned system, where small coefficient changes can produce large solution changes.

### What this adds to the chapter

SALUT introduces a question distinct from index compression or approximate arithmetic: can the machine expose ready work without repeatedly coordinating unrelated tasks? That connects it to TRIDENT's handling of incomplete intermediate results and PFGEMM's out-of-order execution. In each case, scheduling freedom ends where a consumer needs a value that is not yet complete. The locality tradeoff also connects to BSGCN and LTMiner: improving reuse and improving worker occupancy can demand different execution orders.

This is a mechanism-level interpretation, not evidence of growth across conference editions. A stronger long-term hypothesis would be tested with dependency depth, ready-task count, dispatch cost, data placement, and total time on comparable workloads. It would be weakened where true sequential dependence dominates or readiness tracking costs more than the unnecessary waiting it removes.

No SALUT hardware, solver, simulation, or benchmark was executed. Full-paper recovery, dependency and pivot semantics, preparation accounting, matrix-level results, numerical validation, and independent comprehension review remain open.

## How the expanded papers connect: identify what is being saved

The papers do not all save the same kind of work. Distinguishing the mechanisms makes the chapter useful beyond remembering accelerator names. The following comparison is an interpretation of the linked evidence, not a ranking or an observed historical trend.

| Design question | Papers that expose it | What must accompany a claimed saving |
| --- | --- | --- |
| Can repeated requests reuse data already nearby? | [BSGCN](#explanation-dac-2026-research1242), [LTMiner](#explanation-dac-2026-research240) | Working-set size, request order, and retained task state |
| Can positions be recovered with less indexing work? | [PFGEMM](#explanation-dac-2026-research138), [Acc-SpMV](#explanation-dac-2026-research2105), [PillarSparse](#explanation-dac-2026-research2468) | Decoding rules, layout invariants, conversion cost, and shape limits |
| Can ready work proceed without waiting for unrelated tasks? | [SALUT](#explanation-dac-2026-research935), [TRIDENT](#explanation-dac-2026-research149), [PFGEMM](#explanation-dac-2026-research138) | True dependencies, completed-output visibility, dispatch capacity, and locality costs |
| Can intermediate results remain near their consumers? | [TRIDENT](#explanation-dac-2026-research149), [3D attention fusion](#explanation-dac-2026-research2717), [Florella](#explanation-dac-2026-research588) | Buffer capacity, reduction completion, normalization, and supported operations |
| Does less arithmetic preserve represented values or change them? | [Duet](#explanation-dac-2026-research1419), [3D approximation](#explanation-dac-2026-research2717), [Florella](#explanation-dac-2026-research588), [SPADE](#explanation-dac-2026-research680) | Exactness boundary, numeric format, error distribution, and model quality |

These questions interact. A layout that reduces address decoding can constrain scheduling. A schedule that improves reuse can retain more unfinished work. Sharing arithmetic units can reduce area while limiting concurrent operations. An approximation can remove a bottleneck but move the result outside the application's acceptable error range.

A defensible long-term hypothesis is therefore conditional: as arithmetic gets cheaper relative to finding and moving operands, representation and scheduling should be evaluated together. The hypothesis would be weakened by matched experiments showing that decoding and transfers are already small, or that conversion and coordination consume more than they save. It cannot yet be presented as a measured ISCA–DAC–ICCAD trend from these description-level records.

## Why the cases cannot be ranked from their labels

Matrix–vector multiplication, matrix–matrix multiplication, graph processing, and bit-level skipping expose different reuse and dependency patterns. An improvement in one can identify a useful scheduling or representation idea without establishing a faster implementation of another.

The paper comparisons need dimensions, data types, nonzero counts, distributions of row lengths, storage format, hardware, and numerical tolerance. Report format conversion and preprocessing separately, then include them in the complete job when the application must pay them.

Measure time spent on useful arithmetic, metadata access, gathering inputs, combining outputs, and waiting for other workers. Vary both density and structural pattern. A strong result explains where the savings come from and where the extra control outweighs them. That explanation is more transferable than an isolated throughput value.

## Compare the results carefully

First identify the inputs and required output quality. Then identify the limited resource: time, memory, communication, energy, circuit area, or correctness coverage. Ask which part of the method reduces that cost and which new cost it adds. Compare numbers only when the experiments hold these conditions sufficiently similar.

A conference description may explain the proposal while omitting the full experiment. An author preprint link may have been coded from its abstract. The source classification does not by itself establish that every table was read. Missing locations remain visible below.

## Complete captured evidence

These are evidence records, not substitutes for the explanations above. Each record preserves its problem, proposed method, measurements, comparison conditions, and source limits. A populated record does not establish that its mechanism has been fully explained or independently verified.

<span id="paper-dac-2026-research1242"></span>

### BSGCN: Taming Diverse Sparsities in GCNs via Adaptive Band-Segmentation and Tailored Caching

DAC 2026 · Record: `dac-2026-research1242`

[Read the step-by-step explanation](#explanation-dac-2026-research1242)

**Updated source-backed reading card**

Reviewed 2026-09-07. Official accelerator identity checked; numerical description recovered in reading card and expanded explanation distinguishes degree, reuse distance, band size and pinning costs.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

GCN memory accesses with diverse sparsity and significant aggregate traffic from low-degree nodes.

**Mechanism / artifact:**

Band segmentation, band-specific traversal and caching, plus high-degree-node pinning; exact algorithms and thresholds unknown.

**Workload — the work tested:**

GCNs on graph workloads; datasets, models, feature widths and degree conventions unspecified.

**Hardware and manufacturing assumptions:**

Proposed accelerator/cache hierarchy; cache size, process, frequency, bandwidth and measurement methodology unavailable.

**Baseline — the comparison method:**

Unnamed state-of-the-art accelerators; matched configurations unrecovered.

**Reported measurements:**

1.41× average speedup, up to 4.80×; 24.24% DRAM traffic reduction and 1.30× energy efficiency in official description.

**Limits on the conclusion:**

Full manuscript missing; band construction, cache replacement/pinning and preprocessing costs unknown. Cache examples are illustrative, not measured BSGCN traces. No implementation or benchmark execution.

**Source and location**

Evidence tier: Official description only; manuscript and reproduction missing. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/presentation/?id=RESEARCH1242&sess=sess161)

Official Description and Authors; no manuscript page locators available.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** dense GCN execution

generic sparse GCN accelerator

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH1242

**Hardware or process assumptions:** Sparse GCN accelerator or memory hierarchy; cache size, bandwidth, and precision are unspecified.

**Limits:** No graph accuracy, latency, bandwidth, energy, or area results are reported.

Band segmentation may be graph-distribution dependent.

Official description only; graph-diverse validation is required.

**Method or artifact:** Adaptive band segmentation with sparsity-specific caching for GCN execution.

**Metrics:** GCN execution efficiency is claimed qualitatively

**Problem:** Graph-convolution sparsity patterns vary and cause irregular memory access and low utilization.

**Workload or benchmark:** Graph convolutional networks; graph suite, sparsity patterns, and hardware baseline are unspecified.

</details>

<span id="paper-dac-2026-research138"></span>

### PFGEMM: Fully Exploiting the Parallelism of SpGEMM With Element-Wise Out-of-Order Execution Flow and Prefix Decomposition

DAC 2026 · Record: `dac-2026-research138`

[Read the step-by-step explanation](#explanation-dac-2026-research138)

**Updated source-backed reading card**

Reviewed 2026-09-07. Official description inspected; explains shared index prefixes versus prefix sums and separates scheduling, caching and traffic ratios.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Sparse matrix multiplication stalls and index/data bandwidth costs limit useful parallel execution.

**Mechanism / artifact:**

PFCSR index-prefix sharing, element-wise out-of-order scheduling and frequency-aware replacement; precise layout and policies unknown.

**Workload — the work tested:**

Sparse matrix-matrix multiplication; datasets, shapes, sparsity and numeric types unspecified.

**Hardware and manufacturing assumptions:**

Proposed accelerator; process, clock, cache capacity, scheduling window and memory bandwidth unavailable.

**Baseline — the comparison method:**

Unnamed state-of-the-art accelerators; conditions unrecovered.

**Reported measurements:**

Geometric-mean 1.8× off-chip traffic reduction and 2.1× speedup; not a combined 3.78× result.

**Limits on the conclusion:**

Full manuscript missing; format decoding, output merging, numerical rules and conversion costs unknown. Examples do not reconstruct PFCSR. No implementation or benchmark execution.

**Source and location**

Evidence tier: Official description only; manuscript and reproduction missing. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/presentation/?id=RESEARCH138&sess=sess157)

Official Description and Authors; no manuscript page locators available.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** CSR SpGEMM

vendor sparse library

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH138

**Hardware or process assumptions:** Parallel sparse linear-algebra accelerator or GPU; memory and synchronization assumptions are unspecified.

**Limits:** No throughput, numerical accuracy, memory traffic, or synchronization results are reported.

Benefits may depend on sparsity structure.

Official description only; matrix-diverse validation is required.

**Method or artifact:** Element-wise out-of-order execution flow with prefix decomposition for SpGEMM.

**Metrics:** SpGEMM parallel efficiency is claimed qualitatively

**Problem:** Sparse general matrix multiplication exposes irregular dependencies and poor parallel utilization.

**Workload or benchmark:** Sparse matrix-matrix multiplication; matrices, sparsity formats, and platform are unspecified.

</details>

<span id="paper-dac-2026-research1419"></span>

### Duet: Exploiting High-Order Lossless Sparsity for Bit-Serial Transformer Acceleration via Distribution-Aware Pruning

DAC 2026 · Record: `dac-2026-research1419`

[Read the step-by-step explanation](#explanation-dac-2026-research1419)

**Updated source-backed reading card**

Reviewed 2026-09-07. Official description and author publication entry checked; separates exact signed-integer shortening from approximation and explains metadata, grouping and pipeline limits.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Redundant bit-level work in transformer multiplication; representation savings may be limited by decoding and scheduling.

**Mechanism / artifact:**

Duet distribution-aware partition/pruning, remaining-compression search and bit-serial hardware; exact encoding unavailable.

**Workload — the work tested:**

BERT and ViT; variants and evaluation tasks unrecovered.

**Hardware and manufacturing assumptions:**

Proposed accelerator; process, frequency, memory, widths and measurement methodology unavailable.

**Baseline — the comparison method:**

Unnamed accelerators; matched conditions unavailable.

**Reported measurements:**

Description reports effective bits 3.13/3.25, speed ratios 1.45–4.30× and energy improvement 1.32–2.94×; definitions and pairing need full paper.

**Limits on the conclusion:**

No manuscript recovered. Integer reconstruction is not full-model losslessness; example algebra is not Duet encoding. Metadata accounting, quality changes and load-balancing scope unknown. No execution.

**Source and location**

Evidence tier: Official description only; manuscript and reproduction missing. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/presentation/?id=RESEARCH1419&sess=sess110)

Official Description and Authors; author publication list C108 confirms identity without a manuscript link. No manuscript page locators.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** dense bit-serial transformer

unstructured pruning

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH1419

**Hardware or process assumptions:** Bit-serial accelerator with sparse dataflow; precision, memory, and process assumptions are unspecified.

**Limits:** No accuracy, sparsity, latency, energy, area, or model coverage results are reported.

Losslessness may refer to representation rather than task accuracy.

Official description only; end-to-end model validation is required.

**Method or artifact:** Distribution-aware pruning and bit-serial acceleration exploiting high-order lossless sparsity.

**Metrics:** Lossless sparsity exploitation is claimed qualitatively

**Problem:** Bit-serial transformer hardware can waste work when structured high-order sparsity is not exposed.

**Workload or benchmark:** Transformer inference or training; models, pruning targets, and quality constraints are unspecified.

</details>

<span id="paper-dac-2026-research149"></span>

### TRIDENT: An End-to-End Streaming Accelerator for TriSpGEMM

DAC 2026 · Record: `dac-2026-research149`

[Read the step-by-step explanation](#explanation-dac-2026-research149)

**Updated source-backed reading card**

Reviewed 2026-09-07. Official description inspected; separates fusion from multiplication order and explains intermediate aggregation, expansion, flow control and dependency limits.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Intermediate traffic and synchronization in triple sparse matrix multiplication; irregular expansion stresses finite buffers.

**Mechanism / artifact:**

TRIDENT fused processing with hierarchical flow control, windowed sparse format/hybrid dataflow and decoupled out-of-order execution; exact rules unrecovered.

**Workload — the work tested:**

Triple sparse matrix multiplication; input matrices, patterns, multiplication order and data types unavailable.

**Hardware and manufacturing assumptions:**

Proposed accelerator; process, clock, buffer sizes, memory and measurement methodology unknown.

**Baseline — the comparison method:**

Unnamed sparse-matrix accelerators, CPU and GPU; matched configurations unrecovered.

**Reported measurements:**

Description reports 3.56× average accelerator speedup, up to 49.6× CPU and 6.3× GPU speedup; averaging and per-case pairing unavailable.

**Limits on the conclusion:**

No full manuscript. Examples are not TRIDENT schedules. Intermediate aggregation, spill policy, deadlock freedom, numerical ordering and end-to-end boundary unknown; no execution.

**Source and location**

Evidence tier: Official description only; manuscript and reproduction missing. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/presentation/?id=RESEARCH149&sess=sess147)

Official Description and Authors; no manuscript page locators available.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** dense GEMM

generic sparse GEMM

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH149

**Hardware or process assumptions:** Streaming sparse accelerator; memory and precision assumptions are unspecified.

**Limits:** No throughput, accuracy, area, energy, or matrix-suite results are reported.

Benefits may depend on ternary sparsity patterns.

Official description only; workload validation is required.

**Method or artifact:** End-to-end streaming TriSpGEMM accelerator.

**Metrics:** TriSpGEMM efficiency is claimed qualitatively

**Problem:** Ternary sparse matrix multiplication has irregular data movement and underutilized compute.

**Workload or benchmark:** Ternary sparse matrix-matrix multiplication; matrices and platform are unspecified.

</details>

<span id="paper-dac-2026-research2105"></span>

### Acc-SpMV: Accelerating General-Purpose Sparse Matrix-Vector Multiplication with GPU CUDA Cores

DAC 2026 · Record: `dac-2026-research2105`

[Read the step-by-step explanation](#explanation-dac-2026-research2105)

**Updated source-backed reading card**

Reviewed 2026-09-07. Official description and selected pinned implementation inspected; explains column/vector pairing, contiguous tile addressing, atomic reductions and timing asymmetry.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Sparse matrix-vector input access, worker utilization and conflicting output updates.

**Mechanism / artifact:**

Acc-SpMV column permutation, consecutive-column tiles and row-pattern-dependent accumulation; description calls library OmniSpMV, naming history unresolved.

**Workload — the work tested:**

Description: 2715 matrices; released code dispatches above one million parsed nonzeros to CSR5.

**Hardware and manufacturing assumptions:**

Description evaluates RTX4090, A800 and H100; inspected code uses doubles and CUDA kernels. No execution.

**Baseline — the comparison method:**

cuSPARSE and DASP in description; versions and numeric conditions unrecovered.

**Reported measurements:**

Average ratios versus cuSPARSE 2.58/1.91/1.78× and DASP 1.93/1.70/1.75× for RTX4090/A800/H100; not reproduced.

**Limits on the conclusion:**

Full manuscript missing. Pinned custom timed loop accumulates without per-iteration output clearing, fallback includes clearing; no reference comparison in inspected runners. Preparation excluded. Mapping validation and reduction correctness remain unverified.

**Source and location**

Evidence tier: Official description and selected pinned code; manuscript and reproduction missing. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://github.com/APHETION/Acc-SpMV/tree/93b7138bad9f3adbfbad4d86a362515fd3e4cd93)

Selected Acc-SpMV.cu definitions, vector reader, kernels and timed loops; reorder.cu run packing and permutation export. Official Description linked in explanation; no manuscript pages.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** vendor sparse library

CPU SpMV

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH2105

**Hardware or process assumptions:** CUDA GPU with sparse memory access; precision and memory assumptions are unspecified.

**Limits:** No throughput, numerical error, memory traffic, energy, or matrix-diversity results are reported.

Results may depend on sparsity and format.

Official description only; matrix-suite validation is required.

**Method or artifact:** GPU CUDA-core SpMV acceleration method.

**Metrics:** SpMV acceleration is claimed qualitatively

**Problem:** Irregular sparse matrix-vector multiplication underutilizes general GPU cores.

**Workload or benchmark:** General sparse matrices; formats, dimensions, and GPU model are unspecified.

</details>

<span id="paper-dac-2026-research240"></span>

### A Locality-Aware Temporal Motif Mining Accelerator with Chunk-Based Search Tree Expansion

DAC 2026 · Record: `dac-2026-research240`

[Read the step-by-step explanation](#explanation-dac-2026-research240)

**Updated source-backed reading card**

Reviewed 2026-09-07. Official LTMiner identity checked; explains event-sequence counting, partial search state and chunk reuse; keeps separate DTMiner background explicitly attributed.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Misaligned temporal-motif searches repeatedly access graph edges and produce irregular traffic.

**Mechanism / artifact:**

LTMiner chunk-based search-tree expansion across matching tasks; exact hardware and state-management rules unavailable.

**Workload — the work tested:**

Temporal motif mining; graph sets, motif semantics, duration windows and counting conventions unrecovered.

**Hardware and manufacturing assumptions:**

Hardware accelerator; process, clock, memory sizes and energy methodology unavailable.

**Baseline — the comparison method:**

Unnamed software and hardware solutions; configurations unrecovered.

**Reported measurements:**

Description speed ratios software 1.1–652.6×, hardware 1.8–70.3×; energy-saving ratios 3.9–2050.9× and 1.2–17.3× respectively. Extrema cannot be assumed paired.

**Limits on the conclusion:**

DAC manuscript missing. DTMiner PPoPP manuscript supplies selected background only, not LTMiner implementation or results. Constructed event/cache examples are not measured traces. No execution.

**Source and location**

Evidence tier: Official description with separately identified related paper background; target manuscript missing. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/presentation/?id=RESEARCH240&sess=sess121)

Official Description and Authors; no DAC manuscript pages. Separately attributed DTMiner Section 2.1 printed p.593/PDF p.4 and Section 4.2.1 printed p.596/PDF p.7 linked in explanation.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** CPU motif mining

GPU graph search

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH240

**Hardware or process assumptions:** Graph-processing accelerator with local storage; memory and interconnect assumptions are unspecified.

**Limits:** No motif throughput, memory, energy, graph scaling, or correctness results are reported.

Chunk expansion may depend on graph temporal locality.

Official description only; graph-diverse validation is required.

**Method or artifact:** Locality-aware accelerator with chunk-based search-tree expansion.

**Metrics:** Motif-mining efficiency is claimed qualitatively

**Problem:** Temporal motif mining has irregular search and poor locality on conventional processors.

**Workload or benchmark:** Temporal graphs and motif queries; graph sizes, motif definitions, and platform are unspecified.

</details>

<span id="paper-dac-2026-research2468"></span>

### Pillarsparse: Rethinking Unstructured Sparse Formats for Tensor Cores

DAC 2026 · Record: `dac-2026-research2468`

[Read the step-by-step explanation](#explanation-dac-2026-research2468)

**Updated source-backed reading card**

Reviewed 2026-09-07. Official description inspected; distinguishes SpMM from SDDMM, packed descriptors from physical transactions, and conversion from steady-state kernel work.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Dependent metadata access and conversion costs in sparse computations targeting Tensor Cores.

**Mechanism / artifact:**

Pillar CSR nonzero-column units with packed metadata and co-designed pipelined kernels; precise fields and granularity unavailable.

**Workload — the work tested:**

SpMM and SDDMM; matrix sets, dimensions, feature widths and semantics unrecovered.

**Hardware and manufacturing assumptions:**

GPU Tensor Cores and TMA named; GPU model, numeric formats, software and tile sizes unavailable.

**Baseline — the comparison method:**

No named baselines in official description.

**Reported measurements:**

No numerical performance or energy measurements in recovered description. Two-integer metadata claim does not specify widths or exact granularity.

**Limits on the conclusion:**

No manuscript or code recovered. Packing and pipeline examples are illustrative, not Pillar CSR. NVIDIA TMA documentation is separately attributed background. No execution.

**Source and location**

Evidence tier: Official description with hardware documentation background; manuscript and reproduction missing. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/presentation/?id=RESEARCH2468&sess=sess140)

Official Description and Authors; no manuscript pages. Separate NVIDIA Hopper guide Section 1.4.1.2 linked for TMA background.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** dense tensor cores

conventional unstructured sparsity

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH2468

**Hardware or process assumptions:** Tensor-core accelerator with sparse metadata support; memory and precision assumptions are unspecified.

**Limits:** No accuracy, metadata overhead, throughput, energy, area, or model results are reported.

Format benefits may depend on sparsity distribution.

Official description only; accelerator validation is required.

**Method or artifact:** Sparse representation and execution format for tensor cores.

**Metrics:** Sparse tensor-core efficiency is claimed qualitatively

**Problem:** Unstructured sparsity formats may prevent tensor-core utilization and create metadata overhead.

**Workload or benchmark:** Sparse tensor or DNN workloads; sparsity patterns, tensor cores, and baselines are unspecified.

</details>

<span id="paper-dac-2026-research2717"></span>

### Operator-Level Acceleration for Sparse 3D Object Detection

DAC 2026 · Record: `dac-2026-research2717`

[Read the step-by-step explanation](#explanation-dac-2026-research2717)

**Updated source-backed reading card**

Reviewed 2026-09-07. Official description inspected; separates fusion equivalence, spatial-operator approximation and precision loss; flags metric units and device naming.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Inference cost of sparse voxel-based 3D detection, including attention, convolution and precision-sensitive geometry.

**Mechanism / artifact:**

Attention fusion, approximate spatial-to-channel convolution replacement and selective FP16 with FP32 geometric encoders; exact methods unrecovered.

**Workload — the work tested:**

Sparse 3D detection; models, datasets, active-voxel counts, batch sizes and quality protocol unspecified.

**Hardware and manufacturing assumptions:**

A100 and description label GTX 4090; latter needs identity clarification. Mixed precision details unavailable.

**Baseline — the comparison method:**

Unnamed state-of-the-art detector baselines; conditions unrecovered.

**Reported measurements:**

Description reports 2.1–2.5× end-to-end speedup; within 4% mAP and 2.5% NDS with relative versus percentage-point units unresolved. Operator ratios are separate, not multiplicative.

**Limits on the conclusion:**

No manuscript or execution. No retraining does not establish unchanged predictions. Slot normalization, convolution replacement, combined precision error and measurement boundary unknown; cross-subtheme classification needs reconciliation.

**Source and location**

Evidence tier: Official description with metric definition background; manuscript and reproduction missing. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/presentation/?id=RESEARCH2717&sess=sess177)

Official Description and Authors; no manuscript pages. Separately attributed official nuScenes metric background linked in explanation.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** dense 3D detector

generic sparse kernels

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH2717

**Hardware or process assumptions:** Sparse 3D accelerator or optimized kernels; memory and precision assumptions are unspecified.

**Limits:** No detection accuracy, latency, energy, memory, or operator coverage results are reported.

Benefits may depend on sensor sparsity.

Official description only; model and sensor validation is required.

**Method or artifact:** Operator-level sparse acceleration for 3D object detection.

**Metrics:** Sparse detection efficiency is claimed qualitatively

**Problem:** Sparse 3D detectors contain costly operators and irregular data movement.

**Workload or benchmark:** Sparse 3D detection; sensors, models, datasets, and accelerator are unspecified.

</details>

<span id="paper-dac-2026-research588"></span>

### Florella: Accelerating Graph Neural Networks by Sliding Reduction Convention and Flexible Architecture

DAC 2026 · Record: `dac-2026-research588`

[Read the step-by-step explanation](#explanation-dac-2026-research588)

**Updated source-backed reading card**

Reviewed 2026-09-07. Description inspected; explains graph reductions, logarithmic arithmetic, signed cancellation and reuse tradeoffs without inventing the language or approximation.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Diverse GNN operations can require separate components and costly intermediate communication.

**Mechanism / artifact:**

Sliding reduction convention and shared architecture with Jacobian-logarithm unit; syntax, encoding and approximation unrecovered.

**Workload — the work tested:**

GNN inference; model names, graph sets and quality results unavailable.

**Hardware and manufacturing assumptions:**

Proposed architecture; process, clock, area, precision and evaluation method unknown.

**Baseline — the comparison method:**

Four unnamed accelerators; comparison conditions unrecovered.

**Reported measurements:**

Description reports average 2.2× speedup, 2× traffic reduction and 3.3× performance density. Ratios must not be multiplied or inverted to infer chip area.

**Limits on the conclusion:**

No manuscript or execution. Mathematical examples do not reconstruct Florella. Signed values, zero, error, operator coverage and atomic-mapping meaning remain unresolved.

**Source and location**

Evidence tier: Official description only; manuscript and reproduction missing. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/presentation/?id=RESEARCH588&sess=sess156)

Official Description and Authors; no manuscript page locators available.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** dense GNN accelerator

generic sparse GNN execution

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH588

**Hardware or process assumptions:** Flexible sparse graph accelerator; memory and interconnect assumptions are unspecified.

**Limits:** No accuracy, throughput, memory, energy, area, or graph results are reported.

Reduction benefits may depend on graph structure.

Official description only; graph-diverse validation is required.

**Method or artifact:** Sliding-reduction convention with flexible GNN accelerator architecture.

**Metrics:** GNN acceleration is claimed qualitatively

**Problem:** GNN reduction operations are irregular and can underutilize fixed accelerator structures.

**Workload or benchmark:** Graph neural networks; graphs, models, and hardware platform are unspecified.

</details>

<span id="paper-dac-2026-research680"></span>

### SPADE: An Input-Adaptive Sparse Attention Engine for Fast Video Diffusion Models Inference

DAC 2026 · Record: `dac-2026-research680`

[Read the step-by-step explanation](#explanation-dac-2026-research680)

**Updated source-backed reading card**

Reviewed 2026-09-07. DAC-identified manuscript recovered; separates standard and Turbo schedules, fidelity and quality, and exact SICS arithmetic from heuristic selection.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Input-dependent attention selection and sparse execution overhead in video diffusion inference.

**Mechanism / artifact:**

SPADE 3D blocking, summaries, SICS-based scheme selection, head-wise masks and block-sparse execution; Turbo changes onset of sparse steps.

**Workload — the work tested:**

Hunyuan-Video and Wan 2.1/2.2 T2V/I2V; manuscript Section 4.1 gives VBench inputs and 720p configuration.

**Hardware and manufacturing assumptions:**

NVIDIA H800 80GB, CUDA12.8; no local execution.

**Baseline — the comparison method:**

FlashAttention-3 dense reference and sparse baselines; some model/baseline combinations omitted as incompatible.

**Reported measurements:**

Table2 standard E2E 1.32–1.49×; Turbo 1.49–1.80×. Hunyuan standard/Turbo SSIM .91/.57, LPIPS .08/.43, VBench .76/.79. Higher quality score does not imply dense-output fidelity.

**Limits on the conclusion:**

No reproduction or code inspection. Introductory ratios differ from table; preserve variant identity. Policy details, zero-vector normalization and full measurement boundaries require further verification.

**Source and location**

Evidence tier: DAC identified manuscript; code and experiments not reproduced. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://arxiv.org/pdf/2608.03335v1)

p.2 Equations1–2; p.3 blocking; p.4 Equations3–5 and Algorithm1; p.5 Sections3.3/4.1; p.6 Table2 and conclusion.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** dense attention

static sparse attention

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH680

**Hardware or process assumptions:** Sparse attention accelerator; memory and precision assumptions are unspecified.

**Limits:** No visual quality, temporal consistency, latency, energy, area, or sparsity results are reported.

Input-adaptive control may add overhead.

Official description only; content-diverse validation is required.

**Method or artifact:** Input-adaptive sparse attention engine.

**Metrics:** Video diffusion acceleration is claimed qualitatively

**Problem:** Video diffusion attention is expensive and has input-dependent redundancy.

**Workload or benchmark:** Video diffusion models; resolutions, frames, attention patterns, and hardware are unspecified.

</details>

<span id="paper-dac-2026-research935"></span>

### SALUT: Efficient Sparse LU Factorization via Asynchronous Task Triggering on HBM FPGAs

DAC 2026 · Record: `dac-2026-research935`

[Read the step-by-step explanation](#explanation-dac-2026-research935)

**Updated source-backed reading card**

Reviewed 2026-09-07. Description checked; distinguishes true dependencies from broad barriers, numerical factors from reusable structure, and factorization ratios from complete solves.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Irregular dependencies and work imbalance in sparse LU factorization.

**Mechanism / artifact:**

SALUT precompiled dependency management, asynchronous task activation and locality-aware dual-queue scheduling; exact algorithms unrecovered.

**Workload — the work tested:**

Fifteen sparse matrices; identities, dimensions, fill and pivot requirements unavailable.

**Hardware and manufacturing assumptions:**

HBM-equipped FPGA; board, clock, precision and power boundary unknown.

**Baseline — the comparison method:**

NVIDIA cuDSS on RTX A6000 and Tesla V100; versions and comparison conditions unavailable.

**Reported measurements:**

Official description reports geometric-mean throughput/energy-efficiency ratios 4.0×/6.5× against RTX A6000 and 3.7×/4.7× against Tesla V100. Not individual-matrix guarantees or complete-solve speedups.

**Limits on the conclusion:**

No manuscript or execution. Pivot compatibility, dependency visibility, queue rules, preparation accounting, numerical validation and matrix-level results remain open.

**Source and location**

Evidence tier: Official description only; manuscript and reproduction missing. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/presentation/?id=RESEARCH935&sess=sess175)

Official Description and Authors checked 2026-09-07; manuscript page locators unavailable.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** CPU sparse LU

synchronous FPGA LU

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH935

**Hardware or process assumptions:** FPGA with HBM and asynchronous task scheduling; memory and timing assumptions are unspecified.

**Limits:** No numerical error, throughput, memory, energy, or matrix results are reported.

Asynchrony may affect determinism and convergence.

Official description only; solver and board validation is required.

**Method or artifact:** Asynchronous task-triggering sparse LU accelerator.

**Metrics:** Sparse LU efficiency is claimed qualitatively

**Problem:** Sparse LU factorization has irregular dependencies and can underuse FPGA compute and HBM bandwidth.

**Workload or benchmark:** Sparse linear systems; matrices, precision, HBM FPGA board, and solver baselines are unspecified.

</details>

## What remains to establish

Resolve unspecified workloads, comparison methods, resource budgets, and source locations before generalizing a reported gain. Multiple papers in this selected sample permit comparison of mechanisms, but do not by themselves establish recurrence across years or a long-term trend.

[All subthemes](../expanded-taxonomy-v1.md) · [Research directions](../directions/README.md)
