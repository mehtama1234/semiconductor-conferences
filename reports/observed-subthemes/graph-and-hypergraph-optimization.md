# Graph and hypergraph optimization

This subject has 3 records in the selected sample. This page explains where it fits, then presents all captured paper evidence without shortening the measurements or limitations.

[Definitions used in the paper records](../reading-guide-v1.md)

## Understand the parent subject first

- [Design methodology and tooling](../themes/design-methodology-and-tooling.md)

## What the mathematical problem represents

A graph records pairwise connections between objects. A hypergraph lets one connection include several objects at once. For a circuit, that distinction matters because one signal can connect many terminals. Replacing it with independent pairs changes the object being counted unless the conversion and its weights are chosen carefully.

Partitioning assigns every object to a group. A cut-net objective charges for each connection crossing between groups. It does not necessarily charge again when the same connection reaches a third group. A connectivity objective can count those additional groups. Before comparing two reported cut values, establish that they count the same thing.

The capacity constraint matters just as much. If each group can hold only a limited total weight, a tightly connected set may still need to split. Weights might represent area or another resource; they do not automatically represent every constraint of an actual device. Minimizing a connectivity score is therefore a mathematical subproblem, not proof that the final circuit fits, routes, or meets timing.

## ComPart: reconsider groups after simplifying the problem

Coarsening merges objects to create a smaller problem. Uncoarsening restores the separate objects and refines their assignments. A community is a set with relatively strong internal connections. Moving its members together can reveal an improvement that would be missed when each member is considered alone.

[ComPart](../observed-subthemes/graph-and-hypergraph-optimization.md#paper-dac-2026-research1300) applies community guidance during initial partitioning and uncoarsening. Section 3.1 describes reassignment of community fragments using integer optimization for smaller problems and a KaHyPar refinement cycle for larger ones. Thus, it does not establish globally optimal partitions at every scale. Section 3.2's convergence claim concerns a density-decomposition calculation, not the full partitioning problem.

Section 4.1 compares best results under equal total time for ComPart, hMETIS, and KaHyPar; some other baseline results come from earlier publications. Table 1 reports a 0.943 geometric-mean cut ratio relative to KaHyPar for three-way Titan23 partitioning. This is an aggregate ratio, not a reduction achieved on every design. The balance wording also needs care: the setup calls its allowance 2% per partition but specifies epsilon as 0.02 times the partition count. Evaluate that against the Section 2 formula before reproducing the comparison. [ComPart manuscript, Sections 2–4 and Table 1](https://arxiv.org/html/2606.18131v1).

<span id="explanation-dac-2026-research1300"></span>

## ComPart: community guidance can change the search basin, but a better cut ratio is conditional on the hypergraph objective and balance contract

Hypergraph partitioning assigns vertices to parts while preserving the relationships represented by hyperedges. A net can connect more than two vertices, so the cost of cutting it depends on the chosen objective—such as connectivity or cut-net cost—and on how the resulting communication is interpreted by the downstream MPSoC or multi-FPGA system. Balance constrains the part weights; a low cut with an infeasible part is not a valid partition.

Coarsening merges vertices or structures to create a smaller problem. Initial partitioning chooses a solution on that reduced representation, and uncoarsening expands it while refinement moves individual vertices or groups. ComPart changes where community information enters this loop: detected clusterings guide the initial partition and reappear during post-coarsening uncoarsening/refinement. The manuscript also generalizes locally-dense decomposition from graphs to hypergraphs to construct a better starting point. This can expose a promising solution region that a purely local move sequence would miss, but it does not make the search exhaustive or globally optimal.

The first gate is objective and feasibility equivalence. Define hyperedge cut/net connectivity, vertex and net weights, number of parts, balance epsilon, allowed imbalance, fixed vertices, constraints and any communication interpretation. Check the formal balance formula against the implementation and verify every output partition independently. Community density is only a heuristic signal: a dense group may contain vertices that should be separated because a large hyperedge connects it to other parts, or it may hide an imbalance when weights are heterogeneous.

The second gate is search and time accounting. State which community detectors are used, how many clusterings are generated, how fragments are reassigned, when integer optimization is used, when the KaHyPar refinement cycle is used, and what happens when a guide conflicts with a lower cut. Report detector and initialization cost, refinement iterations, accepted/rejected moves, memory, parallelism, timeout and per-instance outcomes. Equal total time is meaningful only when preprocessing, initialization, community detection, refinement and result selection all share the same boundary. A convergence result for the locally-dense decomposition is not convergence of the entire partitioning algorithm.

The manuscript compares best results under equal total time with hMETIS and KaHyPar and reports a 0.943 geometric-mean cut ratio relative to KaHyPar for three-way Titan23 partitioning. That is an aggregate relative result, not a 5.7% improvement on every design, and some comparison values come from earlier publications rather than one reproduced run. Recheck the balance allowance against the formal epsilon definition, report per-instance cut and balance distributions, and test benchmark families beyond Titan23. Then map the selected partitions to the intended heterogeneous MPSoC or multi-FPGA workload to establish whether a cut improvement reduces actual communication, area, congestion or execution time.

The evidence supports community-guided post-coarsening hypergraph search with manuscript-backed objective and benchmark discussion. It does not establish globally optimal partitions, universal quality superiority, reproducible equal-time dominance under all implementations, or downstream physical/system benefit.

## HySpecPro: search over numerical coordinates

A spectral representation assigns numerical coordinates derived from a matrix describing connections. Those coordinates summarize structure; they are not physical locations on a chip. A projection combines them into scores used to choose groups. Reducing the number of search variables can save work, but the resulting family of possible assignments may exclude a better partition.

[HySpecPro](../observed-subthemes/graph-and-hypergraph-optimization.md#paper-dac-2026-research2694) builds coordinates from a bipartite Laplacian: one node type represents vertices, the other hyperedges. Sections 3.1–3.2 optimize projection scores using an evolutionary search and penalize balance violations. Section 2.1 limits the study to two groups and unit weights; nonuniform weights remain future work.

Section 3.4's linear scaling holds when embedding size, solver iterations, population, and generations remain fixed. Section 4 uses an A100 with 80 GB, 32 eigenvectors, 50 Lanczos iterations, up to 3000 candidates per generation, and 50 generations. Table 2 imports several baseline columns from an earlier paper. These conditions do not establish equal-hardware speedups against every listed tool.

Its balance formula allows deviation of epsilon times total weight from the group average. That is not automatically the same as epsilon times average group weight. A numeric tolerance label alone cannot establish comparability. [HySpecPro manuscript, Sections 2.1, 3.1–3.4, and 4](https://arxiv.org/html/2607.00055v1).

<span id="explanation-dac-2026-research2694"></span>

## HySpecPro: spectral projection can reduce search cost only if the discrete partition and balance contract survive

A hypergraph represents relationships in which one hyperedge can connect many vertices. In VLSI, those relationships may encode nets or other coupled objects whose cut cost differs from an ordinary pairwise graph edge. Partitioning assigns vertices to groups while trying to keep connected hyperedges from being cut and to keep group weights balanced. The partition is useful only if its discrete objective and constraints match the downstream parallel, placement or hierarchical flow.

HySpecPro constructs a bipartite Laplacian with separate vertex and hyperedge nodes, embeds the structure into numerical coordinates, and searches projection scores in that spectral space. The captured manuscript describes evolutionary search with balance penalties and a fully GPU-accelerated implementation; it documents 32 eigenvectors, 50 Lanczos iterations, up to 3000 candidates per generation and 50 generations for the A100 evaluation. This is a way to reduce the search representation and expose parallel candidate evaluation. It does not make the continuous embedding the final partition, and it does not prove that the selected projection is globally optimal.

The first gate is discrete partition validity. Define the cut objective, partition count, vertex/hyperedge weights, balance tolerance, projection-to-group rule, repair and penalty. Report infeasible candidates, balance measured under the exact weight convention, cut quality, seed variance and per-benchmark results. The captured balance formula allows deviation proportional to total weight from the group average; that is not automatically equivalent to a tolerance proportional to average group weight. The study's two-group unit-weight scope should not be generalized to weighted or multiway partitioning without new evidence.

The second gate is genuine scaling. “Linear in total hyperedge degree” is conditional when embedding dimension, eigensolver iterations, population and generations remain fixed. Count Laplacian construction, sparse storage, Lanczos/eigensolve, projection, candidate evaluation, GPU/host transfers, preprocessing, memory capacity and search time. Scale vertices, hyperedges, total degree, high-degree distributions and target cut quality separately, and report whether the fixed search budget still reaches the same quality as graphs grow.

Compare state-of-the-art multilevel methods, graph spectral partitioning and earlier projection methods under the same hypergraphs, cut definition, partition count, weights, balance convention, preprocessing, hardware and search budget. Some captured table columns are imported from an earlier paper, so they are not automatically equal-hardware measurements. Finally, pass the partitions into the intended VLSI or parallel flow and measure communication, congestion, timing, area or downstream cut-induced cost; a good partition metric is not automatically a good physical implementation.

The official description claims cut quality comparable to state-of-the-art multilevel methods and linear scaling with total hyperedge degree. The captured manuscript context bounds that claim to the A100/32-eigenvector/50-Lanczos/3000-candidate/50-generation setting and two-group unit-weight scope; the record does not provide a complete normalized cut/balance/runtime/memory distribution, equal-condition baseline reconstruction or downstream placement/routing result. The evidence supports constrained GPU-accelerated spectral hypergraph partitioning, not demonstrated universally scalable, weighted/multiway or downstream-optimal VLSI partitioning.

## HyperEFs: estimate connection structure without materializing every pair

A clique connects every pair in a set. For a hyperedge containing 100 vertices, full clique expansion creates 4950 pairs. A star representation instead uses a central node connected to each member. These representations have different costs and can give different numerical properties; using fewer edges is useful only if it preserves what the later computation needs.

Effective resistance is defined for an electrical network as the voltage difference produced by unit current injected at one node and removed at another. Graph algorithms use the corresponding mathematical quantity to assess connections across multiple paths. This is a definition, not evidence that the paper measures resistance in manufactured wiring. For hypergraphs, the exact construction must be specified before interpreting a distance value.

[HyperEFs](../observed-subthemes/graph-and-hypergraph-optimization.md#paper-dac-2026-research2887) describes adaptive sampling between star and clique expansions to improve its numerical representation. The official abstract claims up to 100× speedup over HyperEF 2.0, lower memory use, and improved partition cuts. It does not expose the selected case, hardware, sampling budget, error tolerance, or complete timing boundary. The maximum must not become an average or a whole-design speedup. [Official HyperEFs description](https://63dac.conference-program.com/presentation/?id=RESEARCH2887&sess=sess129).

An exact-title [research-group repository](https://github.com/Feng-Research/HyperEFs) is available, with a CUDA source directory. Repository discovery is not successful reproduction: the build, inputs, numerical agreement, and benchmark outputs have not been verified here.

<span id="explanation-dac-2026-research2887"></span>

## HyperEFs: adaptive expansion can make resistance estimation cheaper only if the hypergraph and error contract remain intact

Effective resistance is a graph quantity that summarizes how strongly two vertices are connected through all available paths. For a hyperedge containing many vertices, a full clique expansion connects every pair, while a star expansion introduces an auxiliary center connected to each member. A degree-100 clique creates 4,950 pair relationships; a star uses 100 member links plus its center. The two representations have different storage and numerical behavior, so reducing the number of explicit pairs changes the estimator's obligations rather than simply deleting redundant work.

HyperEFs is described as adaptively sampling between star and clique expansions to estimate pairwise effective-resistance distances in large hypergraphs and improve Krylov-subspace embeddings. The resulting information is fed into multilevel hypergraph partitioning. This is an estimator and representation choice: it does not establish that every sampled Laplacian preserves the intended hypergraph resistance, that the embedding error is bounded, or that a better resistance estimate necessarily produces a better discrete partition. Sampling probabilities, estimator weights, transition rule, solver tolerance, variance control, stopping and partition handoff must be explicit.

The first gate is estimator fidelity. Define the hypergraph-to-Laplacian construction and compare pairwise resistance estimates with an exact or high-accuracy reference. Report additive/relative error, bias, variance, confidence bounds and error by hyperedge degree, bottleneck structure, component, bridge-like net and query pair. Test disconnected graphs, skewed degree, repeated nets, communities and high-degree hyperedges; an average embedding score can hide errors precisely on the relationships that determine a partition.

The second gate is real scaling. Count parsing, adaptive sampling, expansion metadata, sparse construction, Krylov/eigensolver work, query evaluation, synchronization, GPU/host transfer, memory peak and retries. “Nearly linear” depends on sample count, solver iterations, embedding dimension, query count, precision and target error. Scale vertices, hyperedges, total hyperedge degree, maximum degree and requested accuracy independently, and report wall time and memory at equal error budgets. The cited CUDA repository is a discovery lead, not a reproduced result until it builds, runs on stated inputs and agrees numerically.

The downstream partition test must hold the rest of the flow fixed. Use the same multilevel partitioner, balance convention, cut objective, refinement budget, seeds and hardware, then report cut size, balance, runtime and per-instance failures. Compare HyperEF 2.0, uniform clique sampling, graph resistance approximation and star expansion. A better cut can result from changed refinement or budget rather than the resistance estimator, and a maximum 100× case cannot be treated as an average or universal speedup.

The official description claims nearly-linear-time estimation, improved Krylov embeddings, lower memory use, improved partition cuts and up to 100× speedup over HyperEF 2.0, including superior cut sizes on large datasets such as Titan23. It does not expose approximation guarantees, sample/error conditions, absolute timing, memory, hardware, partition settings or verified repository execution. The evidence supports adaptive hypergraph effective-resistance estimation, not demonstrated unbiased, universally scalable estimation or downstream partitioning improvement across graph families.

## What can be concluded across the three studies

The shared question is which information must survive a cheaper representation or a restricted search. That is my synthesis of the approaches, not a measured field trend. ComPart revisits groups, HySpecPro searches numerical projections, and HyperEFs samples an expanded representation. They do not perform identical jobs.

A meaningful joint evaluation would fix the objective and actual capacity bounds, include representation construction and refinement in runtime, report memory, and check the final assignments on the original hypergraph. For sampled methods, repeat the experiment to reveal variability. For deployment, also measure the downstream physical result. None of these requirements can be replaced by a headline speedup.

This recovery was checked on 2026-09-07. The two manuscript links provide section- and table-backed detail beyond the older evidence cards below. Their missing-result statements describe the earlier capture, not the new recovery. HyperEFs remains abstract-and-repository evidence here; no full-paper approximation guarantee or reproduced result is asserted.

## Compare the results carefully

First identify the inputs and required output quality. Then identify the limited resource: time, memory, communication, energy, circuit area, or correctness coverage. Ask which part of the method reduces that cost and which new cost it adds. Compare numbers only when the experiments hold these conditions sufficiently similar.

A conference description may explain the proposal while omitting the full experiment. An author preprint link may have been coded from its abstract. The source classification does not by itself establish that every table was read. Missing locations remain visible below.

## Complete captured evidence

These are evidence records, not substitutes for the explanations above. Each record preserves its problem, proposed method, measurements, comparison conditions, and source limits. A populated record does not establish that its mechanism has been fully explained or independently verified.

<span id="paper-dac-2026-research1300"></span>

### Compart: Community-Guided Post-Coarsening for High-Quality Hypergraph Partitioning

DAC 2026 · Record: `dac-2026-research1300`

[Read the step-by-step explanation](#explanation-dac-2026-research1300)

**Updated source-backed reading card**

Reviewed 2026-09-09. Deepens the ComPart treatment into a paper-level reading; separates community guidance in initial partitioning/uncoarsening and locally-dense hypergraph decomposition from cut-net semantics, balance feasibility, local-optimum escape, runtime budgets and downstream mapping benefit, while preserving the manuscript-backed 0.943 Titan23 cut-ratio result and equal-time comparison boundary.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Hypergraph partitioning maps connected workload or circuit objects to parts while trading cut communication against balance; standard community-guided methods often use structure only during coarsening and can leave later refinement trapped in a local solution.

**Mechanism / artifact:**

ComPart: a generalized community-guided framework that uses detected clusterings during initial partitioning and post-coarsening uncoarsening/refinement, and extends locally-dense decomposition with a formal hypergraph treatment; the community detector interface, fragment reassignment, cut objective, balance formula, refinement budget and parallel implementation are condition-dependent and must be read from the manuscript.

**Workload — the work tested:**

Standard hypergraph partitioning benchmarks including Titan23, with three-way partitioning reported in the manuscript; hypergraph sizes, net-size distribution, k, vertex weights, balance allowance, objective variant, benchmark subset, seeds and downstream MPSoC/multi-FPGA mapping workload are otherwise unspecified in the captured official description.

**Hardware and manufacturing assumptions:**

Software multilevel hypergraph partitioner using community detection, integer optimization for smaller refinement problems and KaHyPar-style refinement for larger ones; CPU/GPU, threads, memory, compiler, parallel schedule, time budget and reproducibility environment are unspecified in the captured record.

**Baseline — the comparison method:**

KaHyPar

hMETIS

Standard multilevel hypergraph partitioning with community-oblivious refinement

Equal total-time comparison for the manuscript-reported hMETIS/KaHyPar results; benchmark subset, implementation versions, initialization, threads, seeds, balance formula and objective accounting must remain matched

**Reported measurements:**

The manuscript reports a 0.943 geometric-mean cut ratio relative to KaHyPar for three-way Titan23 partitioning under an equal-total-time comparison, while the official description claims consistent state-of-the-art solution-quality improvement; the record does not provide per-instance cut values, balance violations, runtime distribution, memory, scaling or downstream mapping quality in this card.

**Limits on the conclusion:**

Community density is a search guide, not a proof that vertices in a community belong in the same partition. Define hyperedge cut/net connectivity, vertex/net weights, k, balance epsilon, allowed imbalance, fragment reassignment and feasibility; verify every reported partition satisfies the same balance and cut objective. A graph-style dense decomposition may not preserve heterogeneous hypergraph connectivity or communication cost.

Post-coarsening guidance can help escape a local refinement basin, but the integer optimization and KaHyPar refinement stages remain heuristic or budget-limited at scale. Report initialization, detector cost, number of clusterings, refinement iterations, equal-time accounting, convergence/failure cases, per-instance wins/losses and scaling; convergence of the locally-dense decomposition is not convergence or global optimality of the full partitioning problem.

The manuscript-backed 0.943 geometric-mean Titan23 cut ratio is aggregate and relative to KaHyPar; some baseline results are inherited from earlier publications, and the balance wording requires checking against the formal epsilon definition. The evidence supports community-guided hypergraph search, not demonstrated globally optimal partitioning, universal quality superiority or downstream MPSoC/multi-FPGA benefit.

**Source and location**

Evidence tier: Primary captured DAC description plus recovered author manuscript with section/table reading; balance formula interpretation, benchmark results and baseline provenance remain pending independent review. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://arxiv.org/html/2606.18131v1)

DAC 2026 official description; ComPart manuscript Sections 2–4 and Table 1 as linked in the existing graph-and-hypergraph-optimization chapter; captured Problem, Mechanism / artifact, Workload, Hardware, Baseline, Measurements and Limits fields; no independent reproduction or downstream mapping study.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** multilevel hypergraph partitioning

community-oblivious refinement

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH1300

**Hardware or process assumptions:** CPU/GPU partitioning runtime; graph representation and parallel assumptions are unspecified.

**Limits:** No cut, balance, runtime, memory, or graph-scale results are reported.

Community detection can mislead on heterogeneous hypergraphs.

Official description only; dataset-diverse validation is required.

**Method or artifact:** Community-guided post-coarsening refinement for hypergraph partitioning.

**Metrics:** Partition quality and runtime are claimed qualitatively

**Problem:** Hypergraph partitioning must preserve community structure while optimizing cut and balance at scale.

**Workload or benchmark:** Large hypergraphs from VLSI or applications; partition counts, balance, and baselines are unspecified.

</details>

<span id="paper-dac-2026-research2694"></span>

### Hyspecpro: Scalable Hypergraph Partitioning via Spectral Projection Optimization

DAC 2026 · Record: `dac-2026-research2694`

[Read the step-by-step explanation](#explanation-dac-2026-research2694)

**Updated source-backed reading card**

Reviewed 2026-09-09. Deepens the HySpecPro treatment into a paper-level reading; separates bipartite-Laplacian spectral embedding and GPU projection/evolutionary search from discrete cut quality, balance semantics, partition-count/weight scope, solver/search costs, baseline comparability and downstream VLSI placement validity, while preserving the linear-scaling and state-of-the-art-quality claims with their documented conditions.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Very large VLSI hypergraphs make partitioning central to parallel or hierarchical optimization, but multilevel coarsening can distort high-degree hyperedge structure and leave expensive refinement work; a scalable method must reduce search cost without losing cut quality or balance feasibility.

**Mechanism / artifact:**

HySpecPro is described as a single-level hypergraph partitioner that constructs vertex/hyperedge coordinates from a bipartite Laplacian and performs end-to-end projection-based search with a GPU-accelerated implementation; the manuscript records evolutionary search over projection scores with balance penalties, 32 eigenvectors, 50 Lanczos iterations, up to 3000 candidates per generation and 50 generations, and a two-group unit-weight scope. Partition encoding, projection objective, repair, stopping, multiway/weighted extension and downstream integration remain bounded by the captured evidence.

**Workload — the work tested:**

Large VLSI/application hypergraphs with two-way unit-weight partitioning in the documented study; hyperedge-degree distributions, vertex/hyperedge counts, partition balance tolerance, benchmark identities, weighted/multiway cases, partition reuse and downstream placement/routing workload are partly unspecified.

**Hardware and manufacturing assumptions:**

GPU-accelerated numerical partitioning evaluated with an NVIDIA A100 80-GB configuration in the documented manuscript context; embedding storage, sparse-matrix format, eigensolver implementation, memory traffic, precision, GPU utilization, host transfer, software versions and equivalent baseline hardware are not fully specified.

**Baseline — the comparison method:**

State-of-the-art multilevel hypergraph partitioners

Graph spectral partitioning

Earlier spectral or projection-based methods

Same hypergraphs, partition count, vertex/hyperedge weights, balance definition, cut objective, preprocessing, hardware, solver/search budget and downstream use are required for a fair comparison; some table columns are imported from an earlier paper

**Reported measurements:**

The official description claims cut quality comparable to state-of-the-art multilevel methods and linear scaling with total hyperedge degree; the captured manuscript context documents the A100/32-eigenvector/50-Lanczos/3000-candidate/50-generation setting and a two-group unit-weight scope, but does not provide a complete normalized cut/balance/runtime/memory distribution, equal-hardware comparison or downstream VLSI quality result in this record.

**Limits on the conclusion:**

A spectral embedding is a continuous relaxation and projection search must produce a legal discrete partition. Report cut metric definition, balance by vertex/hyperedge weight, infeasible candidates, repair/penalty behavior, partition count, weighted cases, seed variance and per-benchmark quality. A coordinate that captures connectivity can still discard a discrete partition needed by the actual cut objective or downstream placement.

The reported linear scaling is conditional on fixed embedding dimension, eigensolver iterations, population and generations; those costs can grow with graph size or required quality. Include Laplacian construction, eigensolve/Lanczos, projection, candidate evaluation, GPU/host transfers, memory capacity, preprocessing and search time, and report scaling separately for vertices, hyperedges, total hyperedge degree, high-degree distribution and target cut quality.

Balance tolerances must be defined precisely: the captured formula allows deviation proportional to total weight from the average group weight, which is not automatically the same convention as a tolerance proportional to average group weight. Hold objective, weights, partition count, tolerance, preprocessing and hardware constant across multilevel and spectral baselines; imported baseline columns are not by themselves an equal-condition comparison.

Partition quality is not downstream VLSI quality. Validate selected partitions in the intended parallel, placement, routing or hierarchical flow and measure communication, congestion, timing, area or cut-induced cost as appropriate. The evidence supports a constrained GPU-accelerated spectral hypergraph-partitioning direction, not demonstrated universally scalable, weighted/multiway or downstream-optimal VLSI partitioning.

**Source and location**

Evidence tier: Primary captured official DAC description plus captured manuscript backed chapter extraction; source conditions include a two group unit weight scope and fixed a100 search settings, while weighted/multiway and downstream validation remain open. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH2694&sess=sess129)

DAC 2026 official description plus captured HySpecPro manuscript context (Sections 2.1, 3.1–3.4 and 4); existing graph-and-hypergraph-optimization chapter; no complete normalized result table, equal-hardware baseline reconstruction or downstream placement/routing validation.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** multilevel hypergraph partitioner

graph spectral partitioning

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH2694

**Hardware or process assumptions:** Parallel numerical graph-processing platform; matrix construction and memory assumptions are unspecified.

**Limits:** No cut, balance, runtime, memory, or graph-scale results are reported.

Spectral relaxations may lose discrete partition quality.

Official description only; benchmark-diverse validation is required.

**Method or artifact:** Spectral-projection-based scalable hypergraph partitioner.

**Metrics:** Partition quality and scalability are claimed qualitatively

**Problem:** Large hypergraph partitioning must balance cut quality, balance, and scalability.

**Workload or benchmark:** VLSI or application hypergraphs; partition constraints, scale, and baselines are unspecified.

</details>

<span id="paper-dac-2026-research2887"></span>

### Hyperefs: Adaptive Clique Sampling for Scalable Effective Resistance Estimation in Large Hypergraphs

DAC 2026 · Record: `dac-2026-research2887`

[Read the step-by-step explanation](#explanation-dac-2026-research2887)

**Updated source-backed reading card**

Reviewed 2026-09-09. Deepens the HyperEFs treatment into a paper-level reading; separates adaptive interpolation between star and clique hyperedge expansions from effective-resistance estimator fidelity, sampling bias/variance, Krylov embedding quality, memory/timing boundaries and downstream partition-cut outcomes, while preserving the HyperEF 2.0, 100x, Titan23 and multilevel-integration claims with their evidence limits.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Effective-resistance information can guide sampling, embeddings and hypergraph partitioning, but explicitly expanding large hyperedges into pairwise cliques can make numerical construction and storage expensive; a scalable estimator must reduce that cost without distorting the hypergraph relationships used downstream.

**Mechanism / artifact:**

HyperEFs adaptively samples between star and clique expansions of hyperedges to estimate pairwise effective-resistance distances and improve Krylov-subspace embeddings, with a claimed nearly-linear-time framework integrated into multilevel hypergraph partitioning; sampling probabilities, star/clique transition rule, estimator weights, solver/embedding tolerance, variance control, stopping rule, GPU/CPU implementation and partition handoff are unspecified.

**Workload — the work tested:**

Large VLSI/application hypergraphs including the cited Titan23 dataset, effective-resistance estimation and multilevel hypergraph partitioning; hyperedge-degree distribution, vertex/hyperedge count, pair-query set, sample count, approximation tolerance, partition count/balance, benchmark suite and downstream partition settings are unspecified.

**Hardware and manufacturing assumptions:**

Graph sampling and sparse numerical-linear-algebra runtime with memory and parallel resources; the captured record mentions a CUDA repository but does not establish a verified build or run, and does not specify GPU/CPU, memory capacity/bandwidth, precision, sparse format, eigensolver/Krylov implementation, host transfer or power assumptions.

**Baseline — the comparison method:**

HyperEF 2.0

Uniform clique sampling

Graph-based resistance approximation

Star expansion

Same hypergraphs, queries, sample/memory budget, approximation tolerance, solver precision, hardware, preprocessing, partitioner, balance/cut objective and end-to-end timing boundary are unspecified

**Reported measurements:**

The official description claims nearly-linear-time effective-resistance estimation, improved Krylov-subspace embeddings, lower memory use, improved hypergraph-partitioning solution quality and up to 100x speedup over HyperEF 2.0; it cites superior cut sizes on large datasets such as Titan23, but reports no approximation error, estimator variance/bias, sample count, absolute runtime, memory, graph-scale distribution or downstream per-instance results.

**Limits on the conclusion:**

Star and clique expansions are different numerical representations: a clique for a hyperedge of degree d creates d(d-1)/2 pair relationships, while a star uses an auxiliary center and d links. Adaptive interpolation must define the induced Laplacian/weighting and show that the estimated effective resistance corresponds to the intended hypergraph model. Report pairwise relative/additive error, bias, variance, confidence bounds and error by hyperedge degree/topology against an exact or high-accuracy reference; a smoother Krylov embedding is not automatically a faithful resistance estimate.

Nearly-linear scaling is conditional on sample count, solver iterations, embedding dimension, query count, memory traffic and precision. Count hypergraph parsing, sampling, expansion metadata, sparse construction, Krylov/eigensolver work, synchronization, GPU/host transfer, memory peak and retries. Scale vertices, hyperedges, total hyperedge degree, maximum degree and requested accuracy separately, and compare wall time at equal error and memory budgets rather than only reporting a best speedup.

Adaptive sampling can bias unusual topologies or underrepresent high-degree, bridge-like or low-probability hyperedges. Test graph families with skewed degree, disconnected components, bottlenecks, repeated nets, communities and distributions not used to tune the sampler. Hold the downstream multilevel partitioner, balance, cut objective, random seeds and refinement budget fixed; improved cut size can come from a changed partitioner or budget rather than the resistance estimator.

The official description claims up to 100x over HyperEF 2.0, lower memory and better cuts including Titan23, while repository discovery is not successful reproduction. The captured record does not expose approximation guarantees, sample/error conditions, absolute timing, memory, hardware, partition settings or build/run validation. The evidence supports adaptive hypergraph effective-resistance estimation, not demonstrated unbiased, universally scalable estimation or downstream partitioning improvement across graph families.

**Source and location**

Evidence tier: Primary captured official DAC description plus existing authored hypergraph/effective resistance discussion and repository discovery; no reproduced cuda execution, formal approximation validation or independent downstream partitioning study. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH2887&sess=sess129)

DAC 2026 official description; existing graph-and-hypergraph-optimization chapter framing; exact-title repository discovery recorded in the chapter; no verified build/run, manuscript extraction, approximation-error table or complete partition comparison.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** uniform clique sampling

graph resistance approximation

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH2887

**Hardware or process assumptions:** Graph sampling and numerical linear-algebra runtime; memory and parallel assumptions are unspecified.

**Limits:** No approximation error, sample count, runtime, memory, or graph-scale results are reported.

Adaptive sampling may be biased under unusual topology.

Official description only; graph-family validation is required.

**Method or artifact:** Adaptive clique-sampling estimator for hypergraph effective resistance.

**Metrics:** Estimation scalability and accuracy are claimed qualitatively

**Problem:** Effective-resistance estimation is costly on large hypergraphs and impacts network optimization tasks.

**Workload or benchmark:** Large hypergraphs; approximation tolerance, graph scale, and baselines are unspecified.

</details>

## What remains to establish

Resolve unspecified workloads, comparison methods, resource budgets, and source locations before generalizing a reported gain. Multiple papers in this selected sample permit comparison of mechanisms, but do not by themselves establish recurrence across years or a long-term trend.

[All subthemes](../expanded-taxonomy-v1.md) · [Research directions](../directions/README.md)
