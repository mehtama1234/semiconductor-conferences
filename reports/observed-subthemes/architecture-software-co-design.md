# Architecture software co design

This subject has 13 records in the selected sample. This page explains where it fits, then presents all captured paper evidence without shortening the measurements or limitations.

[Definitions used in the paper records](../reading-guide-v1.md)

## Understand the parent subject first

- [Architecture and accelerators](../themes/architecture-and-accelerators.md)

## Hardware and software jointly determine the executed work

A hardware design exposes operations, storage, connections, and ways to control execution. Software chooses how the application uses those resources. A hardware feature produces little benefit if software cannot express or schedule useful work for it. A software optimization can likewise fail when the hardware lacks the storage, precision, or control it assumes.

Co-design means changing these choices together. The research question is whether the combined arrangement improves a stated application objective while preserving required behavior. The combined result alone does not show how much benefit came from each change.

## Start with the boundary between the two

An instruction set describes operations software can request. A memory layout determines where values are stored and how the program addresses them. A compiler translates a program into operations and a schedule. Runtime software makes decisions while the program executes, such as assigning work or selecting a representation.

Changing one of these boundaries changes both opportunity and responsibility. A new operation may reduce instruction count while requiring specialized hardware and compiler support. A new memory format can reduce transfers while requiring conversion and a new execution routine. Those supporting costs belong in the system result.

## Buffering shows why lifetime matters

A buffer is storage reserved for values needed during execution. The required capacity depends on when each value arrives and when its last use occurs. Values that are no longer needed can release space even if other parts of the computation are unfinished.

Matrix multiplication is often divided into smaller blocks, called tiles, so that inputs can be reused in limited nearby memory. Choosing tile dimensions affects input reuse, partial-output storage, and the number of times small execution routines must start. A larger reuse opportunity can therefore come with more control or switching work.

## Asymmetric tile buffering: mechanism and evidence boundary

The ATB preprint chooses input and output buffer dimensions independently and models both reuse and execution-switching costs. Sections 3–5 explain why storage lifetime and execution overhead must be considered together. [ATB, sections 3–5](https://arxiv.org/html/2511.16041v1#S3)

Its Table 2 compares rows with different matrix dimensions. The listed 24.3 and 4.8 TFLOPS give a ratio of 5.0625, which differs from the printed 4.54×; the 24.6 peak in Table 3 gives another ratio. Neither arithmetic ratio supplies a corrected experimental speedup because the inputs differ. The repository also retains two unresolved program/preprint author-name differences. The method can be explained while the headline remains withheld. [ATB, section 6.3, Tables 2–3](https://arxiv.org/html/2511.16041v1#S6.SS3); [recorded primary assessment](../../dac/data/atb-primary-assessment-v1.json)

<span id="explanation-dac-2026-research1000"></span>

## Asymmetric Tile Buffering: buffer shape changes which data can be reused before it changes how fast arithmetic runs

### What tiled matrix multiplication needs to store

Matrix multiplication combines blocks of an input matrix with blocks of another matrix and accumulates partial output blocks. A tiled implementation loads a block into a local buffer, reuses it across several operations, and writes an output block when its required contributions are complete. The buffer must hold data until the last operation that uses it; capacity is determined by both tile dimensions and data lifetime.

Input and output storage have different lifetimes. An input tile can be reused across multiple output tiles, while an output tile may need to remain local while partial sums from several input tiles accumulate. Making the input and output tile shapes identical is convenient, but it couples two storage decisions that serve different reuse patterns.

### What asymmetric buffering changes

Asymmetric tile buffering decouples input-tile dimensions from output-tile dimensions. This lets the implementation choose more input reuse or more output accumulation according to the matrix shape, precision and local capacity. The useful objective is not simply a larger tile. It is the amount of arithmetic performed per value loaded or stored, subject to buffer capacity and the schedule that moves between tiles.

Arithmetic intensity is the ratio of arithmetic operations to data movement. Increasing reuse can raise arithmetic intensity, but a larger or differently shaped tile can also increase partial-output storage, reduce the number of compatible execution slots, or require more frequent kernel changes. ATB's performance model explicitly includes kernel-switching cost, so the best buffer shape is a tradeoff between reuse and control overhead.

### What the preprint evidence supports

The preprint describes mixed-precision BFP16-BF16 GEMM on an AMD XDNA2 AI Engine and compares MLIR-AIE, symmetric buffering and ATB configurations. The captured values include 4.8 TFLOPS for an MLIR-AIE endpoint, 17.3 TFLOPS for a symmetric configuration, 24.3 TFLOPS for an ATB configuration and a 24.6 TFLOPS size-sweep peak. The preprint also prints a 4.54× speedup headline.

The arithmetic must remain visible. 24.3 divided by 4.8 is 5.0625, and 24.6 divided by 4.8 is 5.125; neither equals 4.54. More importantly, the compared rows use different matrix dimensions, so dividing their throughputs does not create a matched-workload speedup. The discrepancy is a reason to preserve the printed values and conditions, not to infer a corrected headline.

### What a matched evaluation must report

Hold matrix dimensions, precision, tile schedule, compiler version, clock and correctness condition constant while changing the buffering policy. Report input and output tile capacities, reuse counts, local-memory traffic, kernel-switch count, arithmetic intensity, achieved throughput, latency, power and energy. Include matrices whose dimensions do not divide the tile shape, because padding and boundary tiles change both work and storage.

The result should separate model-predicted throughput from measured device throughput and state the firmware, compiler commit, repetition protocol and thermal condition. If different rows are intentionally size sweeps, label them as such; do not use their ratios as speedups. The identity mismatch between the conference program and the author-hosted preprint also remains a source-reconciliation issue.

### What the record establishes and where it stops

The primary preprint supports the mechanism that independently chooses input and output tile buffering and models reuse against kernel-switching cost. It supports the reported BFP16-BF16/XDNA2 configurations and the printed numerical discrepancy. It does not establish a corrected matched-workload speedup, independent reproduction, final proceedings identity or generalization beyond the measured device and shapes.

The [Asymmetric Tile Buffering](../observed-subthemes/architecture-software-co-design.md#paper-dac-2026-research1000) record is therefore a manuscript-backed mechanism with provisional source identity and unresolved comparison arithmetic. The detailed explanation above separates storage lifetime, arithmetic intensity, measured throughput, model predictions and cross-row ratios.

<span id="explanation-dac-2026-research094"></span>

## KL-MoE: pruning experts changes both the stored model and the routing choices that reach it

### What a mixture-of-experts layer does

A mixture-of-experts layer contains several expert networks and a router. For each token, the router scores experts and selects one or more of them. The selected experts process the token, and their outputs are combined. This lets a model have a large total parameter set while using only part of it for each token, but deployment still pays to store the experts and to move tokens to the selected computation.

Pruning removes some experts or reduces their representation. The model then has fewer possible functions and the router must send tokens to the remaining experts. A pruning method is successful only if the retained experts cover the behaviors needed by the workload and the routing changes do not create load imbalance or a quality loss.

### What KL divergence is comparing

Kullback–Leibler divergence compares two probability distributions. For distributions (P) and (Q), (D_{KL}(P\|Q)=\sum_i P(i)\log(P(i)/Q(i))) when the terms are defined. It is directional: comparing (P) to (Q) is not generally the same as comparing (Q) to (P). In this context, a KL-based selection can compare the output or routing behavior of experts and identify representatives whose distributions are similar under the selected data.

Similarity under one calibration set does not prove functional equivalence for every token. Two experts can behave similarly on common inputs and differ on rare inputs, long-context states or a task not represented in the calibration data. The selection distribution, temperature, zero-probability handling, layer location and aggregation therefore need to be specified.

### What hierarchical clustering and Linear Restore change

Hierarchical clustering first groups experts into a structure of related candidates instead of comparing every expert as one flat set. Representative selection then keeps a smaller set intended to cover the groups. The claimed benefit depends on the clustering features and on whether group similarity predicts the downstream task behavior.

The record also names a lightweight Linear Restore mapping for pruned MoE layers. A restore mapping can transform or remap the retained experts' outputs to compensate for the removed experts, but it adds parameters, computation and a new learned approximation. It does not recreate information that was never represented in the retained experts. The storage and latency of the mapping must be counted with the pruned model.

### What the reported measurements require

The official description reports 12.89%, 7.24% and 6.14% average gains over O-Prune, MoE-I2 and HC-SMoE, plus 1.31× inference speedup. The captured record does not identify what the percentage gains measure, the accuracy metric, pruning ratios, model list or storage/latency operating points. These values cannot be read as accuracy gains, compression gains or speedups without the missing definitions.

Measure quality before and after pruning, expert count, retained parameters, router load distribution, token drop or reroute rate, restore cost, memory, latency, throughput and energy. Test common and rare tokens, long contexts, different batch sizes and all listed models. Compare at equal quality, equal retained storage and equal hardware conditions where possible; otherwise keep each comparison dimension explicit.

### What the record establishes and where it stops

The official description establishes a hierarchical MoE-pruning proposal using KL-divergence-based representative selection and a Linear Restore mapping. It reports source-level percentage and inference-speedup claims but does not define their metrics, model set, pruning ratio, hardware or exact page/table support in the captured record.

The [KL-MoE](../observed-subthemes/architecture-software-co-design.md#paper-dac-2026-research094) record is evidence of a named pruning direction, not an independently validated general MoE deployment result. The detailed explanation above separates expert storage from routed compute, KL similarity from universal functional equivalence, restore computation from free recovery, and reported ratios from undefined metric boundaries.

<span id="explanation-dac-2026-research1047"></span>

## GenDSE: CPU design-space exploration is a sequence of constrained choices followed by expensive evaluation

### What design-space exploration is evaluating

A CPU design space is a set of possible configurations. A configuration can specify choices such as pipeline structure, cache parameters, issue width, branch resources, execution units or other microarchitectural features. A simulator estimates how a configuration behaves on a workload. The goal is not merely to generate a valid configuration; it is to find configurations with a useful tradeoff among performance, area, power, cost or another stated objective.

Simulation is expensive because each candidate must be constructed, checked and run on one or more workloads. The space is combinatorial: choosing one value can affect which later choices are valid and how valuable they are. A search method therefore needs to preserve constraints and account for interactions between decisions.

### What the sequential formulation changes

Representing exploration as a Markov decision process means constructing a configuration through a sequence of actions. A state records the choices made so far; an action adds or changes a design decision; a terminal state is a complete configuration that can be simulated. The Markov assumption requires that the information retained in the state is sufficient for deciding the next action and evaluating the eventual configuration.

This formulation makes credit assignment explicit. A final score is produced after the complete configuration is simulated, but the method must learn which earlier choices contributed to that result. If the state omits a dependency or constraint, the generator can favor invalid or misleading partial configurations.

### What a GFlowNet-style generator and sketching are for

A GFlowNet is a generative policy trained to sample terminal objects according to a reward-related distribution rather than only returning one highest-scoring path. For design exploration, this can preserve multiple promising configurations and provide diversity across a Pareto-relevant region. The reward definition still controls what “promising” means; a reward that overweights simulated performance can ignore area, power, validity or robustness.

Progressive Sketching is named as the data-efficiency component, but the captured record does not define the sketch, what information it removes, or whether it changes simulation fidelity or only the learning representation. Any sketch must be checked for information loss: reducing the number of simulations is useful only if the selected designs remain competitive under the full evaluation.

### What the 90% claim needs attached to it

The official description reports 90% average simulation-cost reduction and solution quality, but does not give CPU configuration dimensions, absolute simulation budgets or numerical quality comparisons. A percentage reduction needs a defined baseline count or time, workload set, simulator fidelity, invalid-candidate handling and stopping criterion. “Solution quality” needs the objective, constraints, Pareto measure and comparison point.

Evaluate GenDSE and the surrogate-guided baseline with the same initial design set, simulation budget, validity checks, workloads, random-seed protocol and stopping rule. Report best-so-far quality against simulation count, not only final quality after unequal budgets. Show whether the method finds diverse valid designs and whether its selected candidates remain strong when re-evaluated with the full simulator or a higher-fidelity model.

### What the record establishes and where it stops

The official description establishes a sequential-decision CPU design-space exploration proposal using MDP construction, GFlowNet-based configuration generation and Progressive Sketching for data efficiency. It reports a qualitative solution-quality claim and 90% average simulation-cost reduction but does not provide the dimensions, budgets or numerical quality evidence needed to interpret them.

The [GenDSE](../observed-subthemes/architecture-software-co-design.md#paper-dac-2026-research1047) record is evidence of a named exploration method, not an independently validated CPU-search result. The detailed explanation above separates valid configuration generation, reward shaping, diversity, simulation cost and final design quality.

<span id="explanation-dac-2026-research1101"></span>

## HYPER-CIM: a predictive design flow must connect circuit choices to architecture behavior and fabrication evidence

### What a digital CIM design contains

Compute-in-memory places some computation near the storage array so data does not travel through a separate memory-to-compute path for every operation. A digital CIM design still has a macro-level organization, interfaces, control, buffering, data movement and an architecture that uses one or more macros. Choices such as precision, storage, channel count, pipeline depth and accumulation length affect different levels of that system.

Optimizing only one level can produce an attractive local result that cannot be used efficiently at the next level. A circuit choice can change cycle time, area, power or data format; an architecture choice can change how often the macro is activated, how much data is buffered and how much communication occurs. A useful design flow must pass the relevant conditions between levels.

### What the hierarchical predictive flow is doing

HYPER-CIM is described as a hierarchical exploration flow using a digital 28-nm CIM template, a multi-head circuit-optimization surrogate, Pareto search and silicon verification. A surrogate predicts one or more circuit metrics from design choices instead of simulating or implementing every candidate in full detail. “Multi-head” indicates multiple predicted objectives or outputs, but the captured record does not define the heads, training data, model error or uncertainty handling.

The hierarchy can reduce search cost by using cheaper predictions at an early level and passing selected candidates to more detailed evaluation. This is useful only if the surrogate preserves the ordering of candidates well enough for the final objective. A low average prediction error can still choose the wrong Pareto candidates if errors are concentrated near a constraint or tradeoff boundary.

### What Pareto search means here

Two designs are compared across objectives such as energy efficiency and area efficiency. A design is Pareto-dominated if another design is at least as good on every objective and better on one. The Pareto set contains non-dominated tradeoffs; it is not one universally best design. The flow must state the objectives, constraints, normalization, precision, workload and whether the set comes from predictions, detailed simulation, layout or fabricated measurements.

### How to read the reported numbers

The official description reports 90.8 TOPS/W, 1.23 TOPS/mm², a 31.12×–3.8×10⁶× FoM improvement, 52.13–67.9 TOPS/W energy efficiency and 0.41–0.51 TOPS/mm² area efficiency. TOPS/W divides an operation-rate convention by power; TOPS/mm² divides it by area. These ratios depend on what counts as an operation, the precision, activity, frequency, power boundary, area boundary and workload.

The extremely wide FoM range signals that different reference designs or normalization conditions may be involved. It cannot be interpreted as one common improvement without the full comparison table. The 297 million predicted configurations and more than 8,000 training points recorded in the supplementary assessment are search and modeling quantities, not fabricated chips. Five reported macros do not validate the full predicted space.

### What silicon verification can and cannot establish

Silicon verification can show that selected fabricated macros operate under measured conditions and can reveal mismatch between the template, surrogate and physical implementation. It does not establish that every predicted configuration was fabricated or that the complete architecture-level design space has been validated. The evidence must identify which macro was fabricated, process and test conditions, measured frequency, power, area, yield, output correctness and correspondence to the predicted point.

### What the record establishes and where it stops

The official description establishes a hierarchical digital-CIM exploration flow with a 28-nm template, circuit surrogate, Pareto search and some silicon-verification claim. The captured assessment records no recovered full paper and explicitly separates predicted configurations, training points and reported macros. Full prior-design conditions, accuracy/workload conditions and fabricated-design reproducibility remain open.

The [HYPER-CIM](../observed-subthemes/architecture-software-co-design.md#paper-dac-2026-research1101) record is evidence of a predictive co-design flow, not independent validation of the entire predicted design space. The detailed explanation above separates macro from architecture, prediction from detailed evaluation, Pareto alternatives from one optimum, and silicon samples from millions of predicted configurations.

<span id="explanation-isca-2026-program-006"></span>

## Cassandra: self-speculative decoding reduces target-model work only when proposed reasoning tokens are accepted usefully

### What speculative decoding changes

Autoregressive decoding generates one token at a time. For each next token, the model reads the current sequence and produces a probability distribution. A self-speculative system uses a cheaper version or path of the model to draft several tokens, then uses a more accurate target path to verify them. Accepted draft tokens avoid repeating the full target computation; rejected tokens still cost draft work and verification work.

The useful unit is not draft tokens produced. It is accepted output produced per unit of complete decoding work, while preserving the defined output-quality rule. Acceptance depends on the draft path, prompt, model state, draft length, verification policy and sampling/decoding rule. A high token count under one memory budget does not by itself establish lower response latency or equal reasoning quality.

### What Cassandra changes in the edge execution path

The captured record describes a training-free pipeline with fine-grained data selection, pruning, mantissa truncation, salient-weight and KV-cache selection, and a lightweight hardware encoder-decoder for format conversion. These choices target different costs. Data selection and pruning reduce what is computed or stored; mantissa truncation changes numerical representation; KV-cache selection changes which prior-token state remains available; format conversion determines whether the reduced representation can be consumed efficiently by the hardware.

Training-free means the method does not require an additional training phase for the reported use, not that it has no calibration, selection, conversion or runtime cost. A pruned or truncated draft can be faster but propose worse tokens. A smaller KV cache can reduce memory traffic while removing context information. A format converter can make representations executable while adding hardware area, latency and energy.

### Why reasoning LLMs need a stronger quality boundary

Reasoning tasks can depend on intermediate steps, not only on the final token distribution at one position. A decoder can accept many locally plausible tokens and still change a later reasoning path, answer, tool call or stopping point. Evaluation should therefore report exact-match or task success where applicable, output length, refusal/error behavior, acceptance rate by draft length, target-verification work, time to first token and time per generated token.

The card reports up to 2.41× speedup over BF16 and 1.81× more tokens than Eagle-3 at the same memory budget on Llama 3 8B with an NVIDIA GeForce RTX 4090. “Up to” identifies a best condition. The evidence does not specify prompt distribution, batch distribution, acceptance conditions, quality metric, complete latency boundary, format-conversion cost, hardware area or power, so the ratios cannot be generalized to edge devices or all reasoning workloads.

### What a co-design evaluation must report

Compare BF16 decoding, Eagle-3 and the other named baselines with identical models, prompts, output-quality rule, batch, sequence length and stopping condition. Report draft and target compute, accepted-token rate, rejected-token work, KV-cache bytes, conversion traffic, memory occupancy, throughput, tail latency, energy and quality. Measure the encoder-decoder module separately and as part of complete decoding.

The hardware claim also needs a supported-format definition and an area/frequency/power boundary. A commercial RTX 4090 result is evidence for that software/hardware setup, not evidence of a fabricated edge accelerator or an NPU implementation. The abstract's page-level evidence supports the mechanism and headline conditions, but exact tables and method details require the full paper.

### What the record establishes and where it stops

The primary preprint abstract establishes a training-free self-speculative decoding proposal for reasoning LLMs combining reduced data/weight/KV representations with lightweight format conversion. It reports bounded Llama 3 8B/RTX 4090 speed and memory-budget claims. It does not establish exact acceptance/quality behavior, complete conversion cost, hardware implementation cost or broader device generalization.

The [Cassandra](../observed-subthemes/architecture-software-co-design.md#paper-isca-2026-program-006) record is evidence of a named edge-inference co-design direction, not a full-paper or independent reproduction. The detailed explanation above separates draft production from accepted output, representation reduction from conversion cost, token count from useful latency, and one commercial-GPU condition from general edge deployment.

<span id="explanation-isca-2026-program-007"></span>

## PLENA: long-context inference is constrained by both how much state exists and how fast it can move

### What the two memory walls mean

Long-context agentic inference retains information from earlier text, web pages, tool calls and interaction steps. The retained state can exceed the capacity of a fast local memory, forcing transfers to a larger but slower memory. This creates a capacity wall: the state does not fit where the compute wants to use it.

The same state can also create a bandwidth wall. Even when the data fits somewhere in the system, the links and memory interfaces may not deliver it fast enough to keep the arithmetic units busy. Capacity asks whether the data can be stored; bandwidth asks whether it can arrive at the required rate. A design can solve one and still be limited by the other.

### What PLENA changes in the hardware/software path

The record describes asymmetric-quantization compute/memory units, a flattened systolic array capable of FlashAttention-style execution, a custom instruction set, compiler, cycle-emulated simulator and automated design-space exploration. These components form one co-design contract.

Asymmetric quantization means different operands or data roles use different numerical formats or precisions. This can reduce storage and movement for values that tolerate lower precision while preserving more precision where error matters. It requires the hardware to consume the formats directly and the compiler to schedule conversions, accumulation and memory placement correctly. The captured abstract does not specify the exact precision assignment or quality conditions.

Flattening a systolic array changes how attention-related operations are laid out across processing elements and how data moves through them. FlashAttention-style execution reduces the need to materialize large attention matrices by processing blocks and retaining required intermediates locally. It does not make the long-context state disappear: keys, values, tool history and other state still require a capacity and movement policy.

The custom ISA exposes operations the compiler must schedule. A simulator can estimate cycles for that instruction stream, but the result depends on the modeled memory hierarchy, link contention, buffer sizes, clock, precision, instruction semantics and control overhead. The compiler and design-space search are therefore part of the measured system, not optional implementation details.

### What the reported comparisons establish

The captured record reports up to 8.5× higher utilization than existing accelerators, 2.24× throughput over an A100 and 3.85× throughput over a TPU v6e under matched multiplier and memory settings. The evaluation is simulated. The exact models, context lengths, memory hierarchy, area, energy, simulator validation and artifact status are not recorded in the captured abstract.

“Matched settings” means selected resources were made comparable; it does not mean the systems are identical or that every cost is measured equally. Utilization is not throughput, and throughput is not response-time tail, energy, cost or answer quality. Agentic workloads also change the state through tools and web interaction, so context length alone does not describe memory traffic.

### What a complete evaluation must report

Give context lengths, tool-call traces, batch and arrival conditions, output-quality checks, quantization formats, KV/state placement, buffer sizes, memory bandwidth, NoC/link contention and compiler/runtime overhead. Report prefill and decode separately, because their arithmetic and state movement differ. Measure throughput, time to first token, time per token, tail latency, peak memory, bytes moved, utilization, energy and quality.

Compare against A100 and TPU v6e using matched models, precision, memory capacity, bandwidth assumptions, software effort and output conditions. Validate the cycle-emulated simulator against a lower-level model or prototype and state whether the reported result is a projected accelerator result rather than measured silicon.

### What the record establishes and where it stops

The primary preprint abstract establishes a hardware/software design for long-context agentic LLM inference that addresses capacity and bandwidth through quantized compute/memory, flattened attention-capable execution, a custom ISA/compiler and simulated design exploration. It reports bounded simulated utilization and throughput comparisons.

It does not establish fabricated hardware, simulator accuracy, complete energy/area accounting, broad model coverage, production agentic latency or quality preservation. The [PLENA](../observed-subthemes/architecture-software-co-design.md#paper-isca-2026-program-007) record is therefore evidence of a co-design direction, not an independently validated accelerator result.

<span id="explanation-isca-2026-program-069"></span>

## MTIA 300: training throughput depends on the communication path as well as the matrix engines

### Why recommendation training becomes communication-bound

Large recommendation models contain embedding tables that map identifiers to learned vectors. A training step may access different rows on different accelerators, so the system must exchange embeddings, gradients or updates. Hybrid parallelism also creates collective operations: AllReduce combines values across devices, AllGather distributes values, and AllToAll redistributes different pieces to different devices.

These transfers compete with computation when the same GPU resources, memory interfaces or software launch path handle both. A faster matrix multiplication does not solve a link or synchronization bottleneck. The relevant training time is the sequence of compute, communication, dependency waiting and overlap, not the isolated bandwidth of one interface.

### What MTIA 300 changes

The paper co-designs compute, network chiplets, 12 800-Gbps RDMA NICs, 16 message engines, near-memory collective reduction and the HCCL communication library. The message engines can execute communication operations without expressing every collective as a normal compute-grid kernel. Near-memory reduction combines data close to where it is stored, reducing some movement before the result crosses the wider system.

Collectives are compiled into autonomous dependency graphs. The graph records which communication and compute actions can start, which data they depend on and when a result is ready. This can reduce launch and synchronization overhead, but it does not remove the dependency or link capacity limits. Small messages, uneven traffic, unsupported datatypes, eager setup and poor overlap can still make a specialized path less effective.

### What the paper actually compares

The manuscript evaluates an approximately 150B-parameter DLRM using TorchRec/TorchInductor and distributed Shampoo. The communication comparison uses 40 MTIA 300 accelerators versus 40 H100 accelerators at local batch 6144. The overlap microbenchmark uses 1,000 TF32 4K×4K×4K GEMMs with collectives across 16 accelerators. These are distinct experiments with distinct denominators.

The extracted evaluation reports 3.9× communication performance relative to H100 for the 40-accelerator DLRM case. Table IV reports normalized Perf/TCO of 1.39 for 40 MTIA 300 at local batch 6144 versus 1.00 for 40 H100, and 1.42 for 24 MTIA 300 at local batch 10240 against the same H100 reference with global batch held constant. Communication performance is not end-to-end training throughput, and normalized Perf/TCO is not a direct speedup unless its cost and performance definitions are supplied.

### What the hardware numbers do and do not say

The extracted Table I gives 1.9 GHz, 216 GB HBM3E, 912 W TDP and 667 W typical power, plus chiplet dimensions. TDP and typical platform power are not the same as measured energy per training step. Chiplet area is not total system area or total cost. A normalized TCO result also requires acquisition, networking, power, cooling, utilization and amortization assumptions.

Evaluate communication-only, overlap, complete training-step time, convergence and cost separately. Report collective size distributions, message counts, link utilization, overlap, idle time, numerical parity, unsupported datatypes and the performance/quality effect of changing batch size. Reproduce the same TorchRec/TorchInductor workload on both platforms and state whether the Perf/TCO denominator includes the same system components and lifetime.

### What the record establishes and where it stops

The primary paper supports a hardware/software co-design in which integrated networking, message engines, near-memory collectives and a communication library target recommendation-training communication. It reports bounded author-evaluated communication and normalized Perf/TCO comparisons with page and table locations.

It does not establish independent replication, universal end-to-end training speedup, measured workload energy, or transferable cost for other model sizes and collectives. The [MTIA 300](../observed-subthemes/architecture-software-co-design.md#paper-isca-2026-program-069) record is evidence of a concrete training-system design, not a general accelerator ranking.

<span id="explanation-isca-2026-program-058"></span>

## Dynamic In-Switch Computing for MoE: routing traffic can be reduced only if the switch sees enough token structure to combine useful work

### Why MoE routing creates directional traffic

In a mixture-of-experts layer, a router selects several experts for each token. Tokens assigned to the same expert must reach the device that stores or computes that expert. The dispatch is therefore an all-to-all movement: each source may send tokens to many destinations, and each destination may receive tokens from many sources. The combine phase sends expert outputs back or redistributes them to the tokens' original locations.

The traffic is irregular because token assignments change with the input. Top-k routing also duplicates a token for multiple experts. A network can have enough total bandwidth and still be limited by directional imbalance, small transfers, routing metadata, synchronization or a destination whose queue fills first.

### What in-switch computing is changing

Conventional switches forward packets or collective data. In-switch computing places a permitted operation in the communication path so data can be combined before it travels farther. The operation must be defined for the data layout, packet order, numerical type and dependency state; otherwise moving the computation into the switch only moves the bottleneck or changes the result.

The record names DySHARP dynamic multimem addressing and token-centric dispatch/computation/combine fusion. Dynamic addressing is intended to follow changing token-to-expert destinations. Token-centric fusion treats routing, expert computation and output combination as a connected path rather than independent collective calls. The captured evidence does not establish the exact switch operation, buffer behavior, numerical reduction, hardware implementation or how the address is updated.

### Why layer and training results must remain separate

A layer-level dispatch result measures movement or execution for one MoE layer under a specified top-k and token distribution. Full training includes many layers, optimizer work, pipeline stages, synchronization, activation/gradient traffic, load imbalance and convergence. A local reduction can be hidden by another stage or can change the timing of the next dependency.

The card describes DeepSeek-V3-like small, medium and large configurations with top-k 8/16/32. Larger top-k settings are exploratory, and the main evaluation uses a customized Accel-Sim and BookSim2 simulation of a 32-GPU GH200-NVL32-like node with nine switches. End-to-end training uses 16-way pipeline parallelism across 16 nodes. These conditions define a modeled system, not deployed multi-GPU hardware.

### What a complete evaluation must establish

Report token-to-expert distributions, top-k, duplicate-token rate, message sizes, directional link utilization, queue occupancy, switch buffers, address-update cost, combine precision, synchronization and all layer/full-training boundaries. Compare DeepEP, NVLS, FasterMoE, Tutel, CCFuser, COMET and DualPipe under the same models, top-k, batch, pipeline, network and simulator assumptions.

Calibrate the simulator against measured network and GPU behavior. Validate that in-switch operations preserve numerical results and routing semantics. Plot performance against token skew and burstiness, not only an average workload. Report full-training time, throughput, convergence, energy and failure behavior separately from operator-level movement.

### What the record establishes and where it stops

The primary preprint supports a proposed dynamic in-switch MoE path combining address adaptation with token-centric dispatch, computation and combine. The captured card deliberately withholds numerical headline results pending figure and condition reconciliation. It records simulation and source conditions, not deployed hardware validation or independent reproduction.

The [Dynamic In-Switch Computing](../observed-subthemes/architecture-software-co-design.md#paper-isca-2026-program-058) record is therefore evidence of a network/compute co-design direction. The detailed explanation above separates routing imbalance from total bandwidth, switch computation from forwarding, layer results from training results, and simulation from hardware.

<span id="explanation-isca-2026-program-005"></span>

## Patterns Behind Chaos: expert placement is a data-movement decision before it is a compute decision

### Why expert routing moves so much data

An MoE inference request produces tokens that a router assigns to experts. When experts are distributed across GPUs or wafer-scale regions, each assigned token or activation must travel to the location of its expert and the result must return to the next model stage. The movement depends on which experts are selected, how many tokens select them, the order in which requests arrive, and the topology connecting the devices.

The router may look random from the perspective of a fixed placement, but it can still have temporal and spatial structure. Temporal structure means that expert choices or traffic patterns persist or change in related ways across successive intervals. Spatial structure means that the selected experts and their data movement interact with nearby links, memory regions or communication groups. Finding such structure can support placement and prefetch decisions, but a pattern in one trace is not a guarantee for every request.

### What the method is profiling and changing

The record describes data-movement-centric temporal and spatial profiling, distilled placement insights, lightweight wafer-scale architectural modifications and a prefill-aware expert-placement algorithm. Profiling measures the routing and movement trace rather than only counting multiply-accumulate operations. Distilling insights means converting that trace into placement rules or features that a serving system can use.

Placement assigns expert storage or execution locations. A good placement reduces the distance, congestion or repeated transfer cost for likely traffic while preserving capacity and avoiding a new hotspot. Prefill and decode have different traffic: prefill processes many input tokens and can create a broad batch, while decode produces a smaller number of tokens repeatedly and is more sensitive to per-step movement and synchronization. A placement optimized for one phase can be poor for the other.

### What forecasting can and cannot establish

The title frames the work as forecasting data movement, but the captured card does not specify the forecasting model, prediction horizon, error metric or how a wrong forecast is handled. A forecast is useful only if its prediction arrives before the placement or prefetch decision, improves the expected movement cost, and does not consume more time or bandwidth than it saves.

A forecast can also become stale when request mix, model, batch size, expert popularity, topology or system load changes. The serving system needs a refresh period, fallback placement, capacity constraint and a measurement of prediction error. A lower average transfer count can still increase tail latency if the remaining traffic concentrates on one link or expert.

### What the reported scale and speedups mean

The preprint evaluates four 200B–1000B MoE models released in 2025, more than 24,000 requests across diverse workloads, wafer-scale GPU architectures and existing GPU systems. It reports 6.6× average speedup on wafer-scale GPUs and up to 1.25× speedup on existing GPU MoE computation. These numbers are tied to the evaluated traces, placement algorithms and target topologies; “up to” is not an average across all systems.

Measure routing distributions, expert load, bytes moved, link utilization, placement changes, prediction error, prefill/decode separately, average and tail latency, energy and quality. Compare the proposed placement with the same topology, expert capacity, batching, request trace, software and model. Re-evaluate the selected placement on held-out traces and a different interconnect; otherwise a trace-backed insight can be mistaken for a general property of MoE inference.

### What the record establishes and where it stops

The primary preprint and released trace dataset establish a data-movement-focused profiling and placement direction for large-scale MoE inference, with reported model scale, request count and bounded speedups. The captured evidence does not include independent checking of the six extracted insights, reproduced wafer-scale modeling or transfer validation across routing distributions and interconnects.

The [Patterns Behind Chaos](../observed-subthemes/architecture-software-co-design.md#paper-isca-2026-program-005) record is therefore evidence of a trace-informed placement approach, not a universal forecast of MoE movement. The detailed explanation above separates routing structure from forecast accuracy, placement from topology, prefill from decode, and average speedup from tail and transfer behavior.

<span id="explanation-dac-2026-research617"></span>

## UniNL: fragmented nonlinear work needs an executable representation and a schedule

### Why nonlinear operators can leave a matrix accelerator underused

Large language-model inference contains matrix operations and nonlinear operations. Matrix operations multiply and accumulate many values with regular shapes, so an accelerator can organize them across a processing-element array. A nonlinear operator applies a function or transformation that may have different arithmetic, memory and control requirements. If the array is built mainly for matrix work, the nonlinear part can leave processing elements idle or require a separate execution path.

This is a hardware/software boundary problem. The hardware must expose a way to perform the nonlinear work, while software must express the model's operator sequence in a form that uses that hardware. If the two descriptions do not match, the accelerator may spend time moving intermediate values, starting small kernels or waiting between matrix and nonlinear stages.

### What UniNL's mechanism is intended to do

The captured record describes four connected choices: decomposing nonlinear operators into primitives, approximating some functions with polynomials, adding lightweight microarchitectural support, and fusing primitives with matrix execution. A primitive is a smaller operation with a defined input/output contract. Decomposition can expose common pieces to hardware; polynomial approximation can replace an expensive function with additions and multiplications; support can provide the needed operations; fusion can reduce intermediate storage and scheduling boundaries.

Each choice adds a condition. Approximation changes numerical results and needs an error bound or task-quality evaluation. Decomposition can increase the number of intermediate values. Fusion is useful only when dependencies, memory lifetime and resource availability permit overlap. Lightweight hardware still consumes area, control state and verification effort. A faster nonlinear kernel is not automatically a faster LLM if matrix work, data movement or unsupported operators dominate.

### What utilization and energy claims must include

Processing-element utilization is the fraction of available compute capacity doing useful work under a stated workload and time boundary. Raising it can improve throughput, but utilization alone does not define output quality, latency or energy. A fused schedule may keep arithmetic units busy while increasing buffering or causing contention with matrix operations.

The record reports 6.89× speedup and 7.26× energy-efficiency improvement over Jetson AGX Orin, plus 1.46× and 1.35× performance over state-of-the-art nonlinear-operator accelerator designs. The captured description does not identify the exact model, sequence, precision, accuracy condition, accelerator area, clock, memory traffic or energy boundary. These ratios therefore remain source-reported comparisons, not transferable end-to-end LLM results.

Evaluate the complete model with and without the proposed path, keeping model quality and output conditions fixed. Report operator coverage, polynomial approximation error, matrix/nonlinear overlap, kernel-launch and transfer cost, peak memory, area, frequency, power and energy per token. State whether Jetson is a software baseline, a complete device baseline, or both, and keep comparisons to other accelerator designs attached to their own workload and measurement boundaries.

### What the record establishes and where it stops

The official description establishes a co-design proposal that represents nonlinear operators as primitives, approximates selected functions, adds accelerator support and fuses nonlinear and matrix execution for edge LLM inference. It reports source-level speedup and energy-efficiency claims but omits the conditions needed to determine end-to-end quality and cost.

The [UniNL](../observed-subthemes/architecture-software-co-design.md#paper-dac-2026-research617) record is evidence of a named architecture/software mechanism, not an independently validated edge-LLM result. The detailed explanation above separates approximation from execution savings, operator-level from model-level performance, and hardware support from software scheduling.

<span id="explanation-dac-2026-research1839"></span>

## Moderately unstructured sparse GPU inference: fewer stored weights still require a usable execution path

### What sparsity changes

An LLM weight matrix contains numeric values used in matrix multiplication. Sparsity sets some values to zero or removes them from storage. If the zeros are known and skipped, the system can reduce stored data and arithmetic. Unstructured sparsity does not place the remaining values in a simple fixed pattern, so the hardware also needs metadata describing where each value belongs.

At roughly half sparsity, a dense GPU can still be faster if the sparse representation requires irregular address calculation, metadata reads, decoding, synchronization or poorly filled execution units. The relevant comparison is not only the number of nonzero values. It is the cost of finding them, moving them, multiplying them and assembling the output.

### What the three-layer format and hybrid kernel are doing

The record describes a three-layer sparse storage format and a hybrid SpMM kernel using sparse tensor cores and CUDA cores, with compressed on-chip decoding and residual correction. The storage format determines how nonzeros and their locations are represented. Decoding reconstructs the operands needed by the compute units. Tensor cores and CUDA cores provide different execution paths, so the kernel must decide which work is assigned to each and how their partial results are combined.

Residual correction indicates that the main sparse path does not necessarily represent or execute every contribution in the same way. The correction path must preserve numerical behavior within the required model-quality tolerance. Its storage, arithmetic and synchronization cost belongs in the result; it cannot be treated as free because the main matrix is sparse.

### Kernel speedup and inference speedup answer different questions

Kernel-level speedup measures one matrix operation under a specified shape, sparsity pattern, precision and launch condition. End-to-end inference includes weight loading, other model layers, activation movement, kernel launches, synchronization, sampling or decoding, and any host/runtime work. A 1.64× kernel improvement and a 1.41× end-to-end improvement are not contradictory; they have different denominators and boundaries.

The captured description reports up to 1.64× kernel-level speedup over SpInfer and up to 1.41× end-to-end speedup over FlashLLM. “Up to” identifies a best reported condition, not an average across all models or inputs. The source does not specify GPU models, sparsity distribution, accuracy, batch or sequence settings, memory traffic or baseline tuning, so the values cannot be generalized to all moderately sparse LLM inference.

### What a complete evaluation must preserve

State the pruning or sparsification procedure, nonzero distribution, compression ratio, metadata size, precision, matrix shapes, model quality and decoding condition. Measure decode throughput and latency, peak memory, HBM traffic, tensor-core/CUDA-core utilization, energy and the cost of residual correction. Compare dense, SpInfer and FlashLLM under the same GPU, software version, batch, sequence length, output-quality target and tuning effort.

Check numerical correctness layer by layer and at the complete model. A sparse kernel can produce a plausible output while accumulating errors differently from dense multiplication. Test prompt lengths, batch sizes, decode and prefill, weight distributions and models whose sparsity pattern differs from the one used to tune the kernel.

### What the record establishes and where it stops

The official description establishes a sparse storage and hybrid GPU-SpMM approach for moderately unstructured LLM weights and reports separate kernel-level and end-to-end speedup headlines. It does not establish the exact sparsity conditions, numerical quality, GPU coverage, baseline parity or complete cost boundary.

The [moderately unstructured sparse-weight paper](../observed-subthemes/architecture-software-co-design.md#paper-dac-2026-research1839) record is evidence of a named sparse execution path, not an independently verified general LLM-inference result. The detailed explanation above separates zero skipping from metadata/decoding cost, sparse-kernel speed from model-level speed, and sparsity storage from numerical correctness.

<span id="explanation-dac-2026-research2098"></span>

## PiMM-NoC: mapping an AI model means assigning computation, storage and communication together

### What process-in-memristor memory changes

In a conventional accelerator, weights are stored in memory and moved to compute units. Process-in-memristor-memory places computation near or inside a memristor-based storage structure, often using the physical behavior of the array to perform weighted operations. The result still needs peripheral circuits to drive inputs, sense outputs, convert signals and communicate with other units.

The location of the multiplication does not remove the rest of the computation. Precision, device variation, analog-to-digital and digital-to-analog conversion, accumulation, buffering, programming, calibration and data movement can determine the actual latency, area and energy. A mapping that looks efficient at the array level can be poor after peripheral and network costs are included.

### What the PiMM-NoC architecture is organizing

The record describes heterogeneous tiles containing weight-stationary and general processing units connected by a network-on-chip. A weight-stationary unit keeps model weights near the computation; a general unit can handle work that does not fit the specialized array. The NoC carries activations, partial results, control or other data between tiles.

Mapping assigns model operations and tensors to those tiles and decides when values move. A good mapping must respect capacity, operation compatibility, data dependencies, link bandwidth, buffer occupancy and timing. It is not only a placement problem: an assignment that reduces compute can create a communication bottleneck, and an assignment that reduces movement can exceed a tile's storage or force expensive conversion.

### What RL and MCTS are searching

The captured record couples reinforcement learning and Monte Carlo tree search with cycle-accurate architecture simulation. The search proposes mapping decisions, receives an objective from simulated execution, and explores alternatives. The objective might combine latency, throughput, energy or another cost, but the source does not specify the reward, constraints, search budget or whether the simulator includes device nonidealities and peripherals.

Simulation-guided search can find a good mapping for the modeled hardware and workload. It does not prove that the mapping is good on a fabricated device or on a model whose shapes, precision and communication pattern differ from the search set. Search results are also sensitive to the candidate space, starting policy, reward weighting and stopping rule. A large improvement against a weak or differently normalized baseline is not a general hardware claim.

### What the reported ratios need attached to them

The official description reports up to 3.45× DNN speedup, up to 3.85× LLM speedup, up to 71.6× performance over state-of-the-art accelerators, and up to 6.7× energy-efficiency improvement. These are separate best-case statements with no shared model, mapping set, baseline normalization or energy boundary in the captured record. They must not be read as one common multiplier.

Report model layers and tensor shapes, tile counts, device parameters, ADC/DAC and peripheral models, NoC topology and bandwidth, buffer capacity, precision, nonidealities, mapping time, simulator validation and baseline tuning. Break out array, peripheral, memory, NoC and control cost, and validate selected mappings on a lower-level model or hardware prototype where possible.

### What the record establishes and where it stops

The official description establishes a heterogeneous process-in-memristor-memory tile architecture with NoC connectivity and RL/MCTS mapping search evaluated with cycle-accurate simulation. It does not establish device-level validity, peripheral accounting, simulator calibration, baseline normalization or generalization across models.

The [PiMM-NoC](../observed-subthemes/architecture-software-co-design.md#paper-dac-2026-research2098) record is evidence of a hardware/mapping co-design direction, not an independently validated memristor accelerator result. The detailed explanation above separates in-array computation from peripheral cost, mapping from communication, simulation reward from physical behavior, and separate best-case ratios from one end-to-end comparison.

## Other papers change different boundaries

UniNL's captured record combines decomposition of nonlinear model operations, approximation, hardware support, and fusion. Fusion means executing operations together so intermediate work or storage can be reduced. A complete evaluation must separate approximation error from execution savings and establish which operations remain outside the combined routine. [Recorded evidence](../observed-subthemes/architecture-software-co-design.md#paper-dac-2026-research617)

The moderately unstructured sparse-weight paper combines a storage format with GPU execution routines. Its official description reports different best-case comparisons for a kernel and for complete inference. A kernel is a particular execution routine; its speedup and an application's speedup measure different boundaries and use different named comparisons here. They cannot be multiplied or treated as one common result. [Official description](https://63dac.conference-program.com/presentation/?id=RESEARCH1839&sess=sess140)

PiMM-NoC's captured record instead combines a proposed memory/compute organization with a search procedure assigning model work to its components. Its validity depends on the device assumptions, communication model, and simulator as well as the quality of the assignment. [Recorded evidence](../observed-subthemes/architecture-software-co-design.md#paper-dac-2026-research2098)

## The experiment needed to explain a combined gain

When feasible, compare four cases: the original hardware and software; changed software on the original hardware; changed hardware with the closest compatible original software; and both changes together. Explain any case that cannot run and label simulations as simulations. This prevents an unavailable comparison from becoming an implied measurement.

Keep inputs, output quality, and resource limits fixed. Include conversion, compilation or tuning, host processing, and movement between components. Then vary the workload to test how strongly the combined design depends on the assumptions used to construct it. The resulting conclusion should identify which interaction matters, what it costs, and where it stops helping.
<span id="explanation-iccad-2025-105"></span>

## Squat: make sub-8-bit quantization executable on ordinary edge SIMD

### The deployment problem is a joint numerical and instruction-format problem

Quantization replaces a value represented with more bits by a value represented with fewer bits. This can reduce storage and the amount of data moved, but it also changes the numerical values used by matrix multiplication. Quantization-aware training (QAT) inserts that reduced-precision behavior into training so the model can adjust to its own error.

Squat addresses a specific deployment boundary. Many fine-grained methods assign separate scales to channels or tokens. That can preserve accuracy, but a commodity mobile SIMD kernel may not have an instruction path that consumes those many scales efficiently. A method can therefore produce a compact numerical representation that is awkward for the target processor. Squat combines three choices: QAT losses aimed at attention distortion, token-adaptive 4/8-bit activation precision, and a SIMD multi-kernel mixed-precision multiplier (MKMP).

The contribution is not “4-bit is always better.” It is a co-design claim: the precision policy, the information used to choose precision, and the arithmetic kernel must describe the same executable format. The reported latency is meaningful only together with the model, bit arrangement, sequence length, processor, number of iterations and output-quality result.

### Why query and key quantization matter

Self-attention forms query and key vectors and uses their products to determine how strongly one token attends to another. If their distributions change, the attention scores can change even when the rest of the model is unchanged. Squat's analysis quantizes different portions of LLaMA-58M separately and reports that quantizing query and key accounts for most of the drop observed when the full attention module is quantized.

The paper links this loss to two observable differences. First, the quantized query and key distributions can have different variance from the FP16 versions. Second, the attention map's distinctive first-token column can weaken or disappear. The authors treat the first token as an importance reference because autoregressive attention exposes it to later tokens and its attention column is a measurable signal associated with the information carried by each token.

This gives the method a concrete optimization target. It is not enough to minimize an average weight error if the error changes the attention structure that the model uses. The evaluation must therefore include task quality, attention-related ablations and the target inference cost.

### The training losses preserve two different properties

The FP16 model supplies the reference behavior. The quantized student is trained with soft distillation: cross-entropy with the task labels is combined with a KL-divergence term comparing the student's soft outputs with the teacher's outputs. Squat adds an entropy loss to the query and key representations and a distribution loss comparing quantized and FP16 attention maps by cosine similarity.

The entropy term is based on the paper's Gaussian approximation. For a Gaussian variable, entropy increases with the logarithm of variance. Squat uses this relationship to encourage quantized query and key representations to retain distributional spread. This is a training regularizer, not a direct guarantee that every attention probability is preserved.

The distribution term compares the direction of the quantized attention map with the FP16 map. Two maps can have high cosine similarity while differing in magnitude, and a high similarity on an average can hide a few important heads or positions. The paper sets the entropy-loss ratio to 0.5 and distribution-loss ratio to 1 in its reported experiments. The losses address different failure modes: one targets representation distribution, the other targets the attention pattern.

### Token-adaptive precision makes the average bit count conditional

Squat assigns 8 bits to tokens ranked important and 4 bits to the remainder. Importance is computed from each token's average attention to the initial token across heads. If `rho` is the selected important-token ratio, the top `rho × N` tokens receive 8-bit treatment and the rest receive 4-bit treatment. This is a runtime policy based on the current attention map, not a fixed per-layer precision.

The distinction matters when reading “W4A4” and mixed configurations. W4A4 means a uniform 4-bit weight/activation setting in the table; mixed 4:8 columns mean 4-bit and 8-bit activation groups at stated ratios. The arithmetic workload and memory format are not the same. A mixed policy can preserve more information for selected tokens while reducing average work, but the selector, sorting, grouping and later reconstruction have costs.

The implementation uses a token-control module, concatenates tokens by precision, and uses heapsort for top-k selection. The paper calls those overheads marginal for its setup; a complete transfer claim would need to measure them across sequence lengths and processors. Token importance also depends on the current attention computation, so the policy must be evaluated in the actual autoregressive execution path rather than only on a static calibration sample.

### The MKMP kernel closes the representation-to-instruction gap

Standard mobile SIMD paths commonly operate at byte granularity. If 4-bit operands are merely zero-extended into 8-bit lanes, the model stores fewer bits but may not perform fewer useful operations. Squat's MKMP path packs two 4-bit operands into a 16-bit unit, performs the multiplication using the available SIMD structure, and separates the intermediate results for accumulation. The paper states that its INT4 multiplier can use about half the hardware resources of the INT8 multiplier in its design and that the theoretical 4-bit computation can reduce multiplication and addition work by half relative to byte-expanded execution.

The hardware claim has a precise boundary. It concerns the kernel's operation and resource structure; it does not automatically imply half the end-to-end latency. Bit shifts, result recovery, memory reads, token sorting, thread scheduling and unsupported operations can consume the saved arithmetic capacity. The paper reports compiler-level overlap of memory reads and computation as part of the deployment path, so the measured result includes more than the multiplier alone.

### Read quality and latency as separate axes

The paper evaluates LLaMA-58M and GPT2-97M. For zero-shot BLiMP, its LLaMA-58M average is 74.0 for FP16, 74.0 for W4A8 and 67.8 for W4A4; the corresponding W4A8 and W4A4 values for the baselines differ. For GPT2-97M W4A4 on BLiMP Main, the paper reports average 69.2 for Squat, versus 69.9 FP16, 49.4 NIPQ, 59.7 PACT and 69.1 LLM-QAT. On LLaMA-58M W4A4 across the listed (Super)GLUE tasks, the averages are 68.6 for Squat and 71.0 for FP16. These averages do not mean every subtask improves; the tables contain both gains and regressions.

For latency at sequence length 128, the table reports LLaMA-58M FP16 at 4.54 ms/token on the OnePlus 11 and 15.63 ms/token on Raspberry Pi 5; its uniform W4A4 values are 2.02 and 6.78 ms/token. GPT2-97M reports 6.22 and 23.04 ms/token for FP16, and 2.75 and 9.74 ms/token for uniform W4A4. The mixed columns are distinct configurations: on GPT2 mobile, the 4:8 ratios 1:3 and 1:1 show 3.06 and 3.02 ms/token; on Raspberry Pi they show 11.24 and 10.98 ms/token.

The paper's displayed speedup labels contain an evidence issue. For GPT2 mobile, dividing the displayed FP16 latency 6.22 by 3.06 gives 2.03, while the table labels that cell 2.06; dividing 6.22 by 3.02 gives 2.06, while the label is 2.03. The saved assessment classifies these two cells as incompatible under the stated rounding assumption and preserves the published values rather than silently swapping them. A third strict mismatch can be compatible with unshown rounding. The arithmetic check is a correction lead, not an independent latency reproduction.

### What the paper establishes and what it does not

The manuscript supports a bounded claim: on the selected small models, tasks, QAT baselines, processors and 1,000-iteration latency procedure, Squat combines attention-aware training, token-adaptive 4/8-bit activation precision and a compatible mixed-precision SIMD kernel to improve the reported accuracy/latency tradeoff. It does not establish the same tradeoff for larger models, other processors, different sequence lengths, other token-importance distributions or a production runtime.

The experiments use a OnePlus 11 with Snapdragon 8 Gen 2 and a Raspberry Pi 5 with BCM2712 quad-core Arm Cortex-A76, using all available cores. The paper reports 1,000 iterations, but warmup, thermal controls and the exact prefill/decode boundary remain conditions to verify. The training-feasibility motivation does not establish that training was performed on-device. The code is publicly linked, but no execution or independent reproduction was performed here.

The long-term research question is whether quantization methods should be judged by numerical accuracy alone or by a complete executable contract: scale granularity, token-selection overhead, supported SIMD instruction format, memory traffic, model quality and measured latency under a controlled runtime protocol. Squat makes that contract explicit for one edge setting; its headline speedup must not be separated from the quality tables and the unresolved table arithmetic.

[Recorded paper evidence](../observed-subthemes/architecture-software-co-design.md#paper-iccad-2025-105)

## Compare the results carefully

First identify the inputs and required output quality. Then identify the limited resource: time, memory, communication, energy, circuit area, or correctness coverage. Ask which part of the method reduces that cost and which new cost it adds. Compare numbers only when the experiments hold these conditions sufficiently similar.

A conference description may explain the proposal while omitting the full experiment. An author preprint link may have been coded from its abstract. The source classification does not by itself establish that every table was read. Missing locations remain visible below.

## Complete captured evidence

These are evidence records, not substitutes for the explanations above. Each record preserves its problem, proposed method, measurements, comparison conditions, and source limits. A populated record does not establish that its mechanism has been fully explained or independently verified.

<span id="paper-dac-2026-research617"></span>

### UniNL: Unifying Fragmented Non-Linear Operators for Efficient Edge LLM Inference

DAC 2026 · Record: `dac-2026-research617`

[Read the step-by-step explanation](#explanation-dac-2026-research617)

**Updated source-backed reading card**

Reviewed 2026-09-08. Reconciles the UniNL card with the captured official description; explains fragmented nonlinear operators, polynomial approximation, primitive-aware fusion, utilization and end-to-end measurement boundaries from first principles.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Edge LLM accelerators optimized for matrix operations can underuse processing elements when executing fragmented nonlinear operators, creating extra scheduling, storage and movement cost.

**Mechanism / artifact:**

UniNL primitive decomposition, polynomial approximation, lightweight nonlinear-operation microarchitectural support and primitive-aware fusion overlapping nonlinear and matrix execution.

**Workload — the work tested:**

Edge LLM inference with nonlinear operators; models, sequence lengths, operator coverage, precision, accuracy target, runtime and competing configurations are unspecified.

**Hardware and manufacturing assumptions:**

Custom accelerator with processing-element array and nonlinear-operation extensions, compared with Jetson AGX Orin and other nonlinear accelerators; area, clock, memory hierarchy, process and power boundary are unspecified.

**Baseline — the comparison method:**

Jetson AGX Orin

State-of-the-art nonlinear-operator accelerator designs

Model, precision, quality, operator coverage, memory, hardware and energy-boundary parity are unspecified

**Reported measurements:**

The official description reports 6.89x speedup and 7.26x energy-efficiency improvement over Jetson AGX Orin, plus 1.46x and 1.35x performance over state-of-the-art designs; metric boundary, workloads, aggregation and conditions are unspecified.

**Limits on the conclusion:**

Polynomial approximation can reduce arithmetic cost while changing numerical output; task quality and approximation error must be measured alongside speed.

Primitive decomposition and fusion can reduce intermediate movement and launch boundaries but add control, buffering and dependency constraints; operator-level gain does not establish complete-model gain.

Processing-element utilization is not itself latency, energy or quality; fused execution can increase memory pressure or contend with matrix work.

The official description supplies no model suite, precision, accuracy, area, clock, memory traffic, power boundary or independent execution; end-to-end edge-LLM benefit remains unestablished.

**Source and location**

Evidence tier: Primary captured official DAC description only; no full paper extraction, uninl reproduction or independent numerical quality, end to end latency, area and energy validation. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH617&sess=sess157)

DAC 2026 official description and data/review-packets/dac-2026-research617.json: fragmented nonlinear operators; primitive decomposition; polynomial approximation; lightweight microarchitecture; primitive-aware fusion; 6.89x/7.26x versus Jetson and 1.46x/1.35x versus accelerator designs.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** Jetson AGX Orin

state-of-the-art nonlinear-operator accelerator designs

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH617&sess=sess157

**Hardware or process assumptions:** Custom accelerator with PE array and lightweight nonlinear-operation extensions; Jetson AGX Orin baseline, process, precision, memory hierarchy, and power measurement boundary are unspecified.

**Limits:** The description omits models, precision, accuracy, accelerator area, clock, memory traffic, and energy boundary.

Polynomial approximation and fusion may trade off accuracy and hardware complexity.

Official description only; performance and quality claims require paper-level verification.

**Method or artifact:** Primitive decomposition, polynomial approximation, microarchitectural support, and primitive-aware fusion overlapping nonlinear and matrix execution.

**Metrics:** 6.89x speedup over Jetson AGX Orin

7.26x energy-efficiency improvement

1.46x and 1.35x performance over state-of-the-art designs

**Problem:** Edge LLM accelerators underutilize processing elements during fragmented nonlinear operators because matrix-centric designs lack general fusion mechanisms.

**Workload or benchmark:** Edge LLM inference with nonlinear operators; model suite, sequence lengths, accuracy impact, and competing design configurations are unspecified.

</details>

<span id="paper-dac-2026-research1839"></span>

### Accelerating GPU Inference of Large Language Models with Moderately Unstructured Sparse Weight Matrices

DAC 2026 · Record: `dac-2026-research1839`

[Read the step-by-step explanation](#explanation-dac-2026-research1839)

**Updated source-backed reading card**

Reviewed 2026-09-08. Reconciles the moderately unstructured sparse-GPU card with the captured official description; explains zero skipping, metadata, three-layer storage, hybrid tensor/CUDA execution, residual correction and kernel-versus-end-to-end boundaries from first principles.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Moderate unstructured sparsity may preserve LLM quality but existing GPU sparse matrix-multiplication kernels can fail to beat dense multiplication because irregular storage and execution add overhead.

**Mechanism / artifact:**

Three-layer sparse storage format plus hybrid sparse-tensor-core/CUDA-core SpMM kernel with compressed on-chip decoding and residual correction.

**Workload — the work tested:**

LLM GPU inference with moderately sparse weight matrices and HBM-equipped GPUs; sparsity distribution, pruning method, models, precision, accuracy, matrix shapes, batch and sequence conditions are unspecified.

**Hardware and manufacturing assumptions:**

Modern GPU with sparse tensor cores, CUDA cores and high-bandwidth memory; GPU model, software/driver, launch settings, memory traffic, clock, power and correction-path assumptions are unspecified.

**Baseline — the comparison method:**

SpInfer

FlashLLM

Dense matrix multiplication

GPU, precision, sparsity, quality, batch/sequence, tuning and kernel-versus-end-to-end boundary parity are unspecified

**Reported measurements:**

The official description reports up to 1.64x kernel-level speedup over SpInfer and up to 1.41x end-to-end speedup over FlashLLM; best-case conditions, aggregation and complete cost boundaries are unspecified.

**Limits on the conclusion:**

Unstructured zero skipping requires metadata, address calculation, decoding and result assembly; fewer nonzeros do not automatically mean lower latency or energy.

Sparse tensor cores and CUDA cores have different execution paths, and residual correction adds storage, arithmetic and synchronization that must be included in the cost.

Kernel-level speedup and end-to-end inference speedup have different denominators; the first does not establish the second, and an up-to result is not an average workload result.

The official description supplies no sparsity distribution, model quality, GPU coverage, batch/sequence settings, memory traffic, baseline tuning or independent numerical check; general LLM-inference benefit remains unestablished.

**Source and location**

Evidence tier: Primary captured official DAC description plus linked source repository reference; no full paper extraction, artifact execution or independent numerical, kernel and end to end validation. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH1839&sess=sess140)

DAC 2026 official description and data/review-packets/dac-2026-research1839.json: moderately unstructured sparse weights; three-layer format; hybrid sparse-tensor-core/CUDA SpMM; compressed on-chip decoding; residual correction; 1.64x kernel over SpInfer and 1.41x end-to-end over FlashLLM.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** SpInfer

FlashLLM

dense matrix multiplication

**Evidence locators:** DAC 2026 official description

Linked source repository in official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH1839&sess=sess140

**Hardware or process assumptions:** Modern GPU with sparse tensor cores, CUDA cores, and high-bandwidth memory; architecture, kernel launch settings, and precision are unspecified.

**Limits:** The description omits sparsity distribution, model accuracy, GPU models, batch/sequence settings, memory traffic, and baseline tuning.

Kernel-level and end-to-end gains have different boundaries and may vary with sparsity structure.

Official description and linked source require paper-level artifact and correctness verification.

**Method or artifact:** Three-layer sparse storage format and hybrid sparse-tensor-core/CUDA SpMM kernel with compressed on-chip decoding and residual correction.

**Metrics:** Up to 1.64x kernel-level speedup over SpInfer

Up to 1.41x end-to-end speedup over FlashLLM

**Problem:** Moderate unstructured sparsity can preserve LLM quality but existing GPU SpMM kernels fail to beat dense multiplication at roughly 50% sparsity.

**Workload or benchmark:** LLM GPU inference with moderately sparse weight matrices and HBM-equipped GPUs; sparsity patterns, models, accuracy, and GPU configurations are unspecified.

</details>

<span id="paper-dac-2026-research2098"></span>

### PiMM-NoC: Process-in-Memristor-Memory NoC with RL Mapping Framework for Versatile AI Models

DAC 2026 · Record: `dac-2026-research2098`

[Read the step-by-step explanation](#explanation-dac-2026-research2098)

**Updated source-backed reading card**

Reviewed 2026-09-08. Reconciles the PiMM-NoC card with the captured official description; explains process-in-memristor-memory, heterogeneous tiles, NoC mapping, RL/MCTS simulation search, peripheral costs and separate ratio boundaries from first principles.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Existing process-in-memristor-memory designs may support narrow model classes or coarse mappings that fail to use the heterogeneous architecture and communication resources efficiently.

**Mechanism / artifact:**

Heterogeneous PiMM/processing-unit tile NoC plus reinforcement-learning and Monte Carlo tree-search mapping coupled to cycle-accurate architecture simulation.

**Workload — the work tested:**

Versatile DNN and LLM workloads; models, tensor shapes, mapping objectives, search budget, process/device parameters and baseline configurations are unspecified.

**Hardware and manufacturing assumptions:**

Process-in-memristor-memory tiles with weight-stationary and general processing units connected by a NoC; memristor behavior, precision, ADC/DAC, peripheral, buffer, area, power and nonideality assumptions are unspecified.

**Baseline — the comparison method:**

Existing mapping strategies

State-of-the-art AI accelerators

Model, mapping, simulator, device, communication, energy boundary and baseline-normalization parity are unspecified

**Reported measurements:**

The official description reports up to 3.45x DNN speedup, 3.85x LLM speedup, 71.6x performance over state-of-the-art accelerators and 6.7x energy-efficiency improvement; conditions, denominators, aggregation and energy boundary are unspecified.

**Limits on the conclusion:**

In-array computation does not remove ADC/DAC, sensing, accumulation, buffering, programming, calibration, peripheral, NoC or control cost; array-level benefit is not complete-system benefit.

Mapping must jointly satisfy tile capacity, operation compatibility, dependencies, buffer occupancy and NoC bandwidth; reducing compute can create communication or conversion bottlenecks.

RL/MCTS can optimize the modeled simulator reward but does not establish simulator calibration, device-level validity or generalization to unseen models and nonidealities.

The official description supplies no model set, reward, simulator validation, device parameters, peripheral accounting, baseline normalization or independent execution; the large performance range remains condition-specific.

**Source and location**

Evidence tier: Primary captured official DAC description only; no full paper extraction, simulator execution or independent device, peripheral, mapping and energy validation. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH2098&sess=sess139)

DAC 2026 official description and data/review-packets/dac-2026-research2098.json: heterogeneous PiMM/PU tiles; NoC; RL/MCTS mapping; cycle-accurate simulation; DNN/LLM and performance/energy ratios; omitted device and baseline conditions.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** existing mapping strategies

state-of-the-art AI accelerators

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH2098&sess=sess139

**Hardware or process assumptions:** Process-in-memristor-memory tiles with weight-stationary and general processing units connected by a NoC; memristor technology, precision, ADC/DAC, area, and power assumptions are unspecified.

**Limits:** The description omits model and mapping sets, simulator validation, memristor nonidealities, peripheral costs, and baseline normalization.

Large performance ranges may reflect different baselines and workload mappings rather than one common comparison.

Official description only; architecture, device, and energy claims require paper-level verification.

**Method or artifact:** Heterogeneous PiMM/PU tile NoC and reinforcement-learning/MCTS mapping search coupled to cycle-accurate architecture simulation.

**Metrics:** Up to 3.45x DNN speedup

Up to 3.85x LLM speedup

Up to 71.6x performance over state-of-the-art accelerators

Up to 6.7x energy-efficiency improvement

**Problem:** Existing process-in-memristor-memory designs support narrow model classes and use coarse static mappings that underexploit the architecture’s design space.

**Workload or benchmark:** Versatile DNN and LLM workloads; model suite, mapping objectives, process/device parameters, and baseline accelerator configurations are unspecified.

</details>

<span id="paper-dac-2026-research1000"></span>

### Can Asymmetric Tile Buffering Be Beneficial?

DAC 2026 · Record: `dac-2026-research1000`

[Read the step-by-step explanation](#explanation-dac-2026-research1000)

**Updated source-backed reading card**

Reviewed 2026-09-08. Reconciles the Asymmetric Tile Buffering card with the author preprint and recorded primary assessment; explains input/output tile lifetimes, arithmetic intensity, switching cost, measured conditions and the unresolved headline arithmetic without inventing a corrected speedup.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Symmetric GEMM tile buffering couples input and output tile dimensions even though their reuse and storage lifetimes differ, potentially limiting arithmetic intensity or increasing control cost.

**Mechanism / artifact:**

Asymmetric tile buffering that independently chooses input and output tile dimensions and uses a performance model balancing reuse/arithmetic intensity against kernel-switching cost.

**Workload — the work tested:**

Mixed-precision BFP16-BF16 GEMM on AMD XDNA2 AI Engine; preprint configurations include 4.8 TFLOPS MLIR-AIE, 17.3 TFLOPS symmetric, 24.3 TFLOPS ATB and 24.6 TFLOPS size-sweep peak; matrix dimensions differ across rows.

**Hardware and manufacturing assumptions:**

AMD Ryzen AI 9 HX 370/XDNA2 AI Engine using IRON and MLIR-AIE; firmware, clock, compiler commit, power, thermal, correctness, memory capacity and repetition conditions are not fully exposed.

**Baseline — the comparison method:**

MLIR-AIE configuration

Symmetric tile buffering

Matrix dimensions, compiler/runtime, precision, correctness and measurement boundary are not matched across every reported row

**Reported measurements:**

The preprint reports a 4.54x speedup headline, 4.8 TFLOPS MLIR-AIE, 17.3 TFLOPS symmetric, 24.3 TFLOPS ATB and 24.6 TFLOPS size-sweep peak; 24.3/4.8=5.0625 and 24.6/4.8=5.125, not 4.54, and rows use different matrix dimensions.

**Limits on the conclusion:**

Input tiles and output partial sums have different lifetimes; decoupling their shapes can improve reuse but can also increase partial-output storage, boundary work or control overhead.

Arithmetic intensity measures arithmetic relative to data movement, not complete latency or energy; kernel-switching, padding, compiler schedule and memory traffic remain part of the result.

The printed 24.3/4.8 and 24.6/4.8 ratios disagree with the printed 4.54x headline, and differing matrix dimensions prevent treating either ratio as a matched-workload speedup.

The preprint supports a mechanism and selected device configurations but does not establish independent reproduction, final proceedings identity, exact baseline commits, power/thermal conditions or generalization beyond tested shapes.

**Source and location**

Evidence tier: Primary author preprint and captured primary assessment; no independent device reproduction and conference program/preprint identity remains unresolved. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://arxiv.org/html/2511.16041v1)

Author preprint sections 3–6.3 and Tables 2–3 plus data/review-packets/dac-2026-research1000.json and recorded primary assessment: asymmetric input/output buffers; reuse and kernel-switching model; BFP16-BF16/XDNA2 configurations; printed 4.54x and TFLOPS values; arithmetic and author-identity discrepancies.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** author_preprint_primary_conditions_provisional_identity

**Baselines:** MLIR-AIE configuration

symmetric tile buffering

**Evidence locators:** official description

arXiv S6.T2

arXiv S6.T3

arXiv S6.3

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH1000&sess=sess147

**Hardware or process assumptions:** AMD Ryzen AI 9 HX 370 / XDNA2 AI Engine using IRON and MLIR-AIE; exact firmware, clock, compiler, power, accuracy and repetition conditions are not exposed.

**Limits:** The preprint has two unresolved author-name variants against the program identity.

Printed 24.3/4.8 equals 5.0625 and 24.6/4.8 equals 5.125, not the printed 4.54x; retain the discrepancy rather than correcting it by inference.

The rows use different matrix dimensions, so they do not establish a matched-workload speedup.

Exact baseline commits, accuracy parity, repetition, and final proceedings identity remain unresolved.

This is primary-source extraction, not independent review or reproduction.

**Method or artifact:** Asymmetric tile buffering decouples input and output tile dimensions and uses a performance model to balance arithmetic-intensity gains against kernel-switching costs.

**Metrics:** author-reported up to 4.54x speedup

4.8 TFLOPS MLIR-AIE endpoint

24.3 TFLOPS ATB configuration

24.6 TFLOPS size-sweep peak

**Problem:** Symmetric GEMM tile buffering can constrain arithmetic intensity when input and output tile dimensions are coupled.

**Workload or benchmark:** Mixed-precision BFP16-BF16 GEMM on AMD XDNA2 AI Engine; the preprint reports configurations including 4.8 TFLOPS MLIR-AIE, 17.3 TFLOPS symmetric, and 24.3 TFLOPS ATB, with a 24.6 TFLOPS size-sweep peak.

</details>

#### Additional source assessment

This separately recorded check is dated 2026-09-06. It supplements the original record above and retains its own scope and uncertainty.

[Assessment record](../../dac/data/atb-primary-assessment-v1.json)

[Assessed source](https://arxiv.org/html/2511.16041v1)

**Extraction scope**

HTML evaluation sections and tables; PDF text corroborates abstract; visual inspection of PDF page 6 Tables 2 and 3

**Platform**

**Name:** AMD Ryzen AI 9 HX 370

**Toolchain:** IRON and MLIR-AIE

**Locator:** S6.SS1

**Interpretation limits**

Different matrix dimensions prevent a matched-workload speedup claim from these rows.

Do not substitute arithmetic ratios as corrected experimental speedups.

Overall implementation gains include kernel optimization, not ATB alone.

The approximately 40 percent symmetric-to-ATB throughput comparison also changes matrix dimensions.

Exact baseline commits, accuracy parity, repetition and final-version identity remain unresolved.

**Headline metric status**

withheld_pending_source_reconciliation

**Independent review status**

pending

<span id="paper-dac-2026-research094"></span>

### KL-MoE: A Hierarchical MoE Pruning Framework Exploiting KL Divergence

DAC 2026 · Record: `dac-2026-research094`

[Read the step-by-step explanation](#explanation-dac-2026-research094)

**Updated source-backed reading card**

Reviewed 2026-09-08. Reconciles the KL-MoE card with the captured official description; explains MoE routing, expert pruning, directional KL divergence, hierarchical representatives, Linear Restore cost and undefined metric boundaries from first principles.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

MoE parameter footprint limits deployment and aggressive expert pruning can damage accuracy when importance measures fail to preserve expert functionality.

**Mechanism / artifact:**

Hierarchical expert clustering, KL-divergence representative selection and lightweight Linear Restore mapping for pruned MoE layers.

**Workload — the work tested:**

Multiple MoE models and tasks under storage- and latency-constrained inference; model list, pruning ratios, calibration data, quality metric and operating points are unspecified.

**Hardware and manufacturing assumptions:**

MoE inference deployment; hardware, memory hierarchy, routing, batch, sequence, precision, restore implementation and energy boundary are unspecified.

**Baseline — the comparison method:**

O-Prune

MoE-I2

HC-SMoE

Model set, pruning ratio, quality metric, storage, latency, routing and hardware parity are unspecified

**Reported measurements:**

The official description reports 12.89%, 7.24% and 6.14% average gains over O-Prune, MoE-I2 and HC-SMoE plus 1.31x inference speedup; the percentage metric, model/condition aggregation and storage/latency boundary are unspecified.

**Limits on the conclusion:**

Pruning experts changes both the stored parameter set and the router's available choices; retained experts must cover the needed behaviors without creating load imbalance or quality loss.

KL divergence is directional and measures distributions under selected data; similarity on a calibration set does not establish functional equivalence for rare tokens, long contexts or unseen tasks.

Linear Restore can compensate for removed experts but adds parameters, computation and latency; it cannot recover information absent from the retained representation for free.

The official description supplies no metric definitions, model list, pruning ratios, hardware, page/table location, router-load results or independent validation; the reported gains remain condition-specific.

**Source and location**

Evidence tier: Primary captured official DAC description only; exact page/section/table location not recorded and no full paper extraction, moe pruning reproduction or independent quality/routing/latency validation. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH094)

DAC 2026 official description and data/review-packets/dac-2026-research094.json: hierarchical MoE pruning; KL-divergence representative selection; Linear Restore; O-Prune/MoE-I2/HC-SMoE baselines; 12.89/7.24/6.14% gains and 1.31x inference claim; exact page/table not recorded.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** high_official_description

**Baselines:** O-Prune

MoE-I2

HC-SMoE

**Evidence locators:** Not established in the captured evidence.

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH094

**Hardware or process assumptions:** Not established in the captured evidence.

**Limits:** The description does not identify accuracy metric names, pruning ratios, model list, or the storage/latency operating points.

**Method or artifact:** Hierarchical expert clustering, KL-divergence representative selection, and lightweight Linear Restore mapping for pruned MoE layers.

**Metrics:** 12.89%, 7.24%, and 6.14% average gains over named methods

1.31X inference speedup

**Problem:** MoE parameter footprint limits deployment and aggressive pruning can damage accuracy because existing importance metrics miss expert functionality.

**Workload or benchmark:** Multiple MoE models and tasks under storage- and latency-constrained inference.

</details>

<span id="paper-dac-2026-research1047"></span>

### GenDSE: Generative CPU Design Space Exploration via Sequential Decision Making

DAC 2026 · Record: `dac-2026-research1047`

[Read the step-by-step explanation](#explanation-dac-2026-research1047)

**Updated source-backed reading card**

Reviewed 2026-09-08. Reconciles the GenDSE card with the captured official description; explains sequential CPU configuration search, MDP state/action semantics, GFlowNet diversity, Progressive Sketching uncertainty and simulation-cost versus solution-quality evaluation from first principles.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Surrogate-guided CPU design-space exploration can suffer from credit-assignment difficulty and high simulation cost when microarchitectural choices interact.

**Mechanism / artifact:**

Markov-decision-process formulation with GFlowNet-based CPU-configuration generation and Progressive Sketching for data efficiency; state, reward, sketch and constraint details are unspecified.

**Workload — the work tested:**

CPU microarchitecture design-space exploration and simulation; configuration dimensions, workloads, simulator fidelity, validity rules and objective constraints are unspecified.

**Hardware and manufacturing assumptions:**

CPU design configurations; area, power, performance, process, simulator model, construction cost and high-fidelity validation assumptions are unspecified.

**Baseline — the comparison method:**

Surrogate-guided CPU design-space exploration

Initial design set, simulation budget, invalid-candidate handling, stopping rule, random seeds and quality objective parity are unspecified

**Reported measurements:**

The official description reports 90% average simulation-cost reduction and a solution-quality claim; absolute simulation count/time, budget, fidelity, objective, Pareto measure and numerical quality comparisons are unspecified.

**Limits on the conclusion:**

Sequential decisions require a state that preserves constraints and dependencies; an incomplete state can favor invalid or misleading partial configurations.

A GFlowNet-style generator can preserve diversity among high-reward configurations, but reward shaping determines which quality, cost, area, power and validity tradeoffs are actually preferred.

Progressive Sketching may reduce information or simulation use, but the captured record does not define what is sketched or whether full-fidelity reevaluation preserves the ranking.

The official description supplies no design dimensions, absolute budgets, quality values, simulator validation or independent search; 90% cost reduction cannot be interpreted as better design quality without those conditions.

**Source and location**

Evidence tier: Primary captured official DAC description only; exact page/section/table location not recorded and no full paper extraction, gendse reproduction or independent search budget/quality validation. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH1047&sess=sess156)

DAC 2026 official description and data/review-packets/dac-2026-research1047.json: CPU DSE as sequential decision process; GFlowNet configuration generation; Progressive Sketching; surrogate baseline; 90% average simulation-cost reduction and qualitative solution quality; exact page/table not recorded.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** surrogate-guided CPU design-space exploration

**Evidence locators:** Not established in the captured evidence.

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH1047&sess=sess156

**Hardware or process assumptions:** Not established in the captured evidence.

**Limits:** The description does not provide CPU configuration dimensions, absolute simulation budgets, or numerical solution-quality comparisons.

**Method or artifact:** Markov decision process with GFlowNet-based configuration generation and Progressive Sketching for data efficiency.

**Metrics:** 90% average simulation-cost reduction

solution quality

**Problem:** Surrogate-guided CPU design-space exploration suffers from credit-assignment problems and high simulation sample complexity.

**Workload or benchmark:** CPU microarchitecture design-space exploration and simulation.

</details>

<span id="paper-dac-2026-research1101"></span>

### HYPER-CIM: Hierarchical Predictive Exploration and Realizable Design Flow for High-Efficient Digital CIM

DAC 2026 · Record: `dac-2026-research1101`

[Read the step-by-step explanation](#explanation-dac-2026-research1101)

**Updated source-backed reading card**

Reviewed 2026-09-08. Reconciles the HYPER-CIM card with the captured official description and supplementary assessment; explains CIM hierarchy, surrogate prediction, Pareto tradeoffs, TOPS metrics, predicted configuration counts and silicon-verification scope from first principles.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

CIM exploration can optimize one level without preserving circuit-faithful visibility into macro, accelerator and architecture interactions, making predicted high-efficiency designs difficult to realize or compare.

**Mechanism / artifact:**

Hierarchical predictive exploration flow with a digital 28-nm CIM template, multi-head circuit-optimization surrogate, Pareto search and selected silicon verification.

**Workload — the work tested:**

Digital CIM macro and architecture design across precision, storage, channels, pipeline depth and accumulation length; workload, accuracy, operation convention, comparison set and hierarchy conditions are unspecified.

**Hardware and manufacturing assumptions:**

Digital 28-nm CIM template and fabricated macro evidence; process details, frequency, power/area boundaries, yield, layout, test conditions and architecture integration are unspecified.

**Baseline — the comparison method:**

Prior CIM designs

Single-level CIM optimization flows

Full comparison set, objective normalization, workload/accuracy, prediction fidelity and fabricated-condition parity are unspecified

**Reported measurements:**

The official description reports 90.8 TOPS/W, 1.23 TOPS/mm², 31.12x–3.8x10^6x FoM improvement, 52.13–67.9 TOPS/W and 0.41–0.51 TOPS/mm² ranges; operation, power, area, workload, reference and aggregation boundaries are unspecified.

**Limits on the conclusion:**

A circuit surrogate can reduce exploration cost only if its prediction error preserves useful candidate ordering near constraints and Pareto boundaries; average error alone is insufficient.

Pareto search yields non-dominated tradeoffs rather than one universally best design, and its result depends on objectives, normalization, constraints and precision.

297 million predicted configurations and more than 8,000 training points are modeling/search quantities, not fabricated designs; five reported macros do not validate the full predicted space.

Silicon verification of selected macros can expose model mismatch but does not establish all predicted configurations, full architecture integration, yield or reproducibility; full paper and comparison conditions remain open.

**Source and location**

Evidence tier: Primary captured official DAC description plus supplementary official/institutional assessment; no recovered full paper or independent surrogate, design flow and silicon reproduction. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH1101&sess=sess156)

DAC 2026 official description and data/review-packets/dac-2026-research1101.json plus data/review-packets/hyper-cim-primary-recovery-v1.json: digital 28-nm CIM template; multi-head surrogate; hierarchical/Pareto flow; silicon verification claim; 90.8 TOPS/W, 1.23 TOPS/mm² and wide FoM/range claims; 297M predicted configurations, >8k training points and five reported macros assessment boundary.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** high_official_description

**Baselines:** prior CIM designs

single-level CIM optimization flows

**Evidence locators:** Not established in the captured evidence.

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH1101&sess=sess156

**Hardware or process assumptions:** Not established in the captured evidence.

**Limits:** The description does not provide the full prior-design comparison set, accuracy/workload conditions, or yield/reproducibility details for fabricated macros.

**Method or artifact:** Hierarchical predictive exploration flow with a digital 28 nm CIM template, multi-head circuit-optimization surrogate, Pareto search, and silicon verification.

**Metrics:** 90.8 TOPS/W

1.23 TOPS/mm²

31.12X–3.8×10⁶X FoM improvement

52.13 to 67.9 TOPS/W energy-efficiency improvement

0.41 to 0.51 TOPS/mm² area-efficiency improvement

**Problem:** CIM exploration often optimizes only one level and lacks circuit-faithful visibility across macro, accelerator, and architecture decisions.

**Workload or benchmark:** Digital compute-in-memory macro and architecture design across tunable precision, storage, channels, pipeline depth, and accumulation length.

</details>

#### Additional source assessment

This separately recorded check is dated 2026-09-06. It supplements the original record above and retains its own scope and uncertainty.

[Assessment record](../../dac/data/hyper-cim-primary-recovery-v1.json)

[Assessed source](https://63dac.conference-program.com/presentation/?id=RESEARCH1101&sess=sess123)

**Extraction scope**

Official description and matching institutional abstract; no full paper recovered

**Interpretation limits**

297M predicted configurations are not 297M tested silicon designs.

More than 8k training points must not be described as fabricated chips.

Five reported macros do not establish silicon validation throughout the predicted design space.

Institutional abstract repetition and publication peer-review metadata are not independent acceptance of this project's extraction.

No full paper recovered in bounded checks does not mean inaccessible.

**Headline metric status**

withheld_pending_fullpaper_conditions

**Independent review status**

pending

<span id="paper-iccad-2025-105"></span>

### Squat: Quant Small Language Models on the Edge

ICCAD 2025 · Record: `iccad-2025-105`

[Read the step-by-step explanation](#explanation-iccad-2025-105)

**Updated source-backed reading card**

Reviewed 2026-09-08. Reconciles the description card with arXiv version 2 and the saved PDF arithmetic assessment; explains the precision/training/kernel co-design, separates quality from latency, and preserves the two rounding-incompatible speedup cells and unresolved runtime conditions.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Sub-8-bit quantization can reduce model storage without reducing work on commodity mobile SIMD if the kernel expands values to byte lanes or cannot handle fine-grained scales; quantization can also distort self-attention and task quality.

**Mechanism / artifact:**

Squat combines entropy-guided and distribution-aligned QAT, token-importance-based 4/8-bit activation quantization, FP16-teacher distillation and a SIMD multi-kernel mixed-precision (MKMP) multiplier with token-control and concatenation support.

**Workload — the work tested:**

LLaMA-58M and GPT2-97M; zero-shot BLiMP and fine-tuned (Super)GLUE; W8A8, W4A8 and W4A4 plus mixed 4:8 activation ratios. Deployment uses sequence length 128, 1,000 latency iterations, OnePlus 11/Snapdragon 8 Gen 2 and Raspberry Pi 5/BCM2712 quad-core Arm Cortex-A76, all available cores.

**Hardware and manufacturing assumptions:**

Mobile/edge SIMD with byte-oriented INT8 paths; MKMP concatenates sub-byte operands and recovers intermediate products. Reported latency is ms/token and includes the paper's runtime/compiler path; warmup, thermal controls and exact prefill/decode boundary remain unresolved. No on-device training measurement is established.

**Baseline — the comparison method:**

FP16

NIPQ

PACT

LLM-QAT

Uniform versus mixed 4/8-bit configurations

**Reported measurements:**

LLaMA-58M BLiMP averages: FP16 74.0, Squat W4A8 74.0 and Squat W4A4 67.8; GPT2-97M W4A4 BLiMP Main averages: FP16 69.9, NIPQ 49.4, PACT 59.7, LLM-QAT 69.1 and Squat 69.2.

LLaMA-58M W4A4 (Super)GLUE average: FP16 71.0, Squat 68.6. Latency at sequence length 128: LLaMA-58M FP16/W4A4 4.54/2.02 ms per token on OnePlus 11 and 15.63/6.78 on Raspberry Pi; GPT2-97M 6.22/2.75 and 23.04/9.74 respectively.

Mixed GPT2-97M mobile 4:8 activation ratios 1:3 and 1:1 report 3.06 and 3.02 ms/token; the table labels their speedups 2.06 and 2.03, while displayed-value division gives 2.03 and 2.06. The saved assessment classifies both as rounding-incompatible under its stated rounding assumption; no values are silently swapped.

**Limits on the conclusion:**

Speedup is not an iso-accuracy claim. The tables contain per-task regressions, and the W4A4 averages do not preserve FP16 quality uniformly across BLiMP or (Super)GLUE.

Token ranking, heapsort, concatenation, memory traffic, shifts, result recovery and thread scheduling are part of executable cost; a theoretical half-work or smaller multiplier does not establish half end-to-end latency.

The two GPT2-mobile speedup inconsistencies require raw runs and the author's rounding policy; arithmetic consistency checks are not latency reproduction. Warmup, thermal controls, prefill/decode boundary, version-matched harness and checkpoint/token-selector provenance remain open.

The result is limited to two small models, selected tasks, two edge platforms and the stated configurations. Public code was not executed here; no on-device training, silicon measurement, independent reproduction or universal deployment claim is established.

**Source and location**

Evidence tier: Primary arxiv preprint v2, pdf arithmetic assessment and official code link; selected manuscript reading, execution and independent acceptance not performed. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://arxiv.org/pdf/2402.10787v2)

Version 2: Sections III–IV and Figures 1–6 pages 3–6 for attention analysis, entropy/distribution losses, token policy and MKMP; Sections V–IX pages 6–10 for BLiMP/(Super)GLUE, deployment and ablations; Tables I–IV, especially Table IV PDF page 9 for latency and displayed speedups; saved arithmetic assessment at iccad/data/squat-primary-recovery-v1.json; official code link https://github.com/shawnricecake/squant.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_primary_preprint

**Baselines:** FP16

NIPQ

PACT

LLM-QAT

**Evidence locators:** **Fields:** problem

method_or_artifact

**Location:** III; IV-B/E

**Fields:** workload_or_benchmark

baselines

**Location:** V-A; Tables I-III

**Fields:** hardware_or_process_assumptions

limits

**Location:** V-B; Table IV, PDF page 9; supplementary PDF rounding analysis

**Evidence url:** https://arxiv.org/html/2402.10787v2

**Hardware or process assumptions:** OnePlus 11 Snapdragon 8 Gen 2, all cores; Raspberry Pi 5 BCM2712, four cores. Latency: 1000 iterations, 128 input tokens, ms/token.

**Limits:** Speedup is not iso-accuracy improvement. Two PDF ratios are rounding-incompatible; one further difference is rounding-compatible. Warmup, thermal controls and prefill/decode boundary unresolved. No measured on-device training established. See supplementary assessment; no independent acceptance.

**Method or artifact:** Entropy/distribution-guided QAT, attention-ranked 4/8-bit token precision, and mixed-precision SIMD multiplication.

**Metrics:** Not established in the captured evidence.

**Problem:** Sub-byte quantization must preserve attention information and map to commodity SIMD execution.

**Workload or benchmark:** LLaMA-58M and GPT2-97M; BLiMP and (Super)GLUE.

</details>

#### Additional source assessment

This separately recorded check is dated 2026-09-06. It supplements the original record above and retains its own scope and uncertainty.

[Assessment record](../../iccad/data/squat-primary-recovery-v1.json)

[Assessed source](https://arxiv.org/html/2402.10787v2)

**Extraction scope**

IV methodology; V-B deployment; Tables II-IV and VIII hardware efficiency. PDF page 9 Table IV visually checked.

**Conditions**

**Models:** LLaMA-58M

GPT2-97M

**Devices:** OnePlus 11 Snapdragon 8 Gen 2, all available cores

Raspberry Pi 5 BCM2712, four cores

**Iterations per test:** 1000

**Input sequence length:** 128

**Latency units:** ms/token

**Accuracy baselines:** FP16

NIPQ

PACT

LLM-QAT

**Headline metric status**

withheld_pending_table_and_accuracy_reconciliation

**Independent review status**

pending

<span id="paper-isca-2026-program-006"></span>

### Cassandra: Enabling Reasoning LLMs at Edge via Self-Speculative Decoding

ISCA 2026 · Record: `isca-2026-program-006`

[Read the step-by-step explanation](#explanation-isca-2026-program-006)

**Updated source-backed reading card**

Reviewed 2026-09-08. Reconciles the Cassandra card with the captured primary preprint abstract; explains self-speculative decoding, accepted versus drafted tokens, pruning/truncation/KV selection, format conversion and reasoning-quality/deployment boundaries from first principles.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Reasoning LLM decoding at the edge incurs high per-token cost, while prior self-speculative approaches can have weak low-batch behavior, training requirements or representation-conversion overhead.

**Mechanism / artifact:**

Training-free self-speculative decoding pipeline using fine-grained data selection, pruning, mantissa truncation, salient-weight/KV-cache selection and a lightweight hardware encoder-decoder for format conversion.

**Workload — the work tested:**

Reasoning LLM inference including Llama 3 8B on NVIDIA GeForce RTX 4090 in low-batch edge-style decoding; prompts, batch/sequence distributions, quality rule, acceptance behavior and broader models are unspecified.

**Hardware and manufacturing assumptions:**

Commercial GPU/NPU integration with lightweight format conversion; exact area, frequency, power, supported formats, memory hierarchy, conversion cost and device coverage are unspecified.

**Baseline — the comparison method:**

BF16 full-precision decoding

Eagle-3 self-speculative decoding

Prior layer-skipping and structured KV-compression methods

Model, prompt, batch, quality, acceptance, memory, hardware and latency-boundary parity are unspecified

**Reported measurements:**

The primary preprint abstract reports up to 2.41x speedup over BF16, 1.81x more tokens than Eagle-3 at the same memory budget, Llama 3 8B on RTX 4090 and training-free operation; acceptance, quality, latency and cost definitions are unspecified.

**Limits on the conclusion:**

Draft tokens are useful only when accepted enough to offset draft and verification work; generated-token count is not accepted-output latency or reasoning-task success.

Pruning, mantissa truncation and KV-cache selection reduce different representations and can change numerical behavior or remove context; format conversion makes a representation executable but adds cost.

Training-free does not mean calibration, selection, conversion or runtime overhead is absent, and a commercial GPU result does not establish an edge NPU implementation.

The captured evidence is a preprint abstract with no exact page/table location, acceptance/quality protocol, prompt distribution, hardware area/power or independent reproduction; general deployment benefit remains unestablished.

**Source and location**

Evidence tier: Primary author preprint abstract only; no full paper extraction, cassandra reproduction or independent acceptance, reasoning quality, latency, format converter and edge hardware validation. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://arxiv.org/abs/2605.26558)

Primary arXiv preprint abstract and data/review-packets/isca-2026-program-006.json: training-free self-speculative decoding; fine-grained data selection; pruning/mantissa truncation; salient weights/KV cache; hardware encoder-decoder; 2.41x BF16 and 1.81x Eagle-3 memory-budget headline; exact full-paper locations not recorded.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** high_primary_preprint

**Baselines:** BF16 full-precision decoding

Eagle-3 self-speculative decoding

prior layer-skipping and structured KV-compression methods

**Evidence locators:** Not established in the captured evidence.

**Evidence url:** https://arxiv.org/abs/2605.26558

**Hardware or process assumptions:** Commercial GPU/NPU integration with a lightweight format-conversion module; exact area, frequency, power, supported formats, acceptance-rate behavior, and broader device coverage require full-paper verification.

**Limits:** The evidence is an author preprint abstract; exact quality/acceptance measurements, prompt and batch distributions, hardware area and power, format support, and generalization beyond Llama 3 8B and the RTX 4090 remain to be verified from the full paper.

**Method or artifact:** A training-free self-speculative decoding pipeline using fine-grained data selection, pruning, mantissa truncation, salient weight/KV-cache selection, and a lightweight hardware encoder-decoder for format conversion.

**Metrics:** up to 2.41x speedup over BF16

1.81x more tokens than Eagle-3 at the same memory budget

Llama 3 8B on NVIDIA GeForce RTX 4090

training-free operation

**Problem:** Reasoning LLMs incur high decode-stage overhead at the edge, while existing self-speculative decoding methods can have weak low-batch performance or require additional training; representation-conversion overhead also limits practical deployment.

**Workload or benchmark:** Reasoning LLM inference, including Llama 3 8B on an NVIDIA GeForce RTX 4090, evaluated in low-batch edge-style decoding scenarios.

</details>

<span id="paper-isca-2026-program-007"></span>

### Combating the Memory Walls: Optimization Pathways for Long-Context Agentic LLM Inference

ISCA 2026 · Record: `isca-2026-program-007`

[Read the step-by-step explanation](#explanation-isca-2026-program-007)

**Updated source-backed reading card**

Reviewed 2026-09-08. Reconciles the PLENA card with the captured primary preprint abstract; explains capacity versus bandwidth walls, asymmetric quantization, flattened attention execution, custom ISA/compiler responsibilities and simulated-comparison boundaries from first principles.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Long-context agentic LLM inference retains web, tool and interaction state that creates both memory-capacity and memory-bandwidth limits, leaving compute underutilized.

**Mechanism / artifact:**

PLENA hardware/software co-design with asymmetric-quantization compute/memory units, flattened FlashAttention-capable systolic array, custom ISA, compiler, cycle-emulated simulator and automated design-space exploration.

**Workload — the work tested:**

Long-context agentic LLM inference with web/computer-use inputs, tool-call trajectories and extended contexts; models, context lengths, traces, batches, quality rules and prefill/decode conditions are unspecified.

**Hardware and manufacturing assumptions:**

Custom simulated accelerator with flattened systolic array, asymmetric quantization, custom ISA/compiler and modeled memory hierarchy; area, energy, bandwidth, buffer, link contention, clock and fabricated status are unspecified.

**Baseline — the comparison method:**

Existing accelerators

NVIDIA A100

Google TPU v6e

Multiplier/memory matching, model, precision, memory, software, simulator, quality and measurement-boundary parity are unspecified

**Reported measurements:**

The primary preprint abstract reports up to 8.5x higher utilization than existing accelerators, 2.24x throughput over A100 and 3.85x throughput over TPU v6e under matched settings; simulated boundary, aggregation and full resource accounting are unspecified.

**Limits on the conclusion:**

Capacity and bandwidth are different limits: fitting state in memory does not guarantee it arrives fast enough, and higher bandwidth does not eliminate capacity pressure.

Asymmetric quantization can reduce movement while changing numerical error; the exact format assignment, accumulation and quality conditions are not specified.

A cycle-emulated simulator and custom compiler can estimate a co-designed path but do not establish silicon behavior, simulator fidelity, compiler overhead or complete area/energy cost.

The captured primary evidence supplies no exact page/table location, model/context protocol, memory hierarchy validation, energy/area, fabricated status or independent reproduction; general agentic deployment benefit remains unestablished.

**Source and location**

Evidence tier: Primary author preprint abstract only; no full paper extraction, simulator/prototype reproduction or independent memory, quality, latency, energy and hardware validation. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://arxiv.org/abs/2509.09505)

Primary arXiv preprint abstract and data/review-packets/isca-2026-program-007.json: long-context agentic memory walls; asymmetric quantization; flattened FlashAttention systolic array; custom ISA/compiler; cycle-emulated simulation; 8.5x utilization, 2.24x A100 and 3.85x TPU v6e claims; exact full-paper locations not recorded.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** high_primary_preprint

**Baselines:** existing accelerators

NVIDIA A100 GPU

Google TPU v6e

**Evidence locators:** Not established in the captured evidence.

**Evidence url:** https://arxiv.org/abs/2509.09505

**Hardware or process assumptions:** Custom accelerator with flattened systolic array, asymmetric quantization, custom ISA/compiler, and cycle-emulated simulation; reported gains are simulated and depend on matched hardware-resource assumptions.

**Limits:** The evidence is an author preprint abstract and simulated evaluation; exact models, context lengths, memory hierarchy, area/energy, simulator validation, and the status of open-source artifacts require full-paper verification.

**Method or artifact:** PLENA hardware-software co-design with asymmetric-quantization compute/memory units, a flattened FlashAttention-capable systolic array, custom ISA, compiler, cycle-emulated simulator, and automated design-space exploration flow.

**Metrics:** up to 8.5x higher utilization than existing accelerators

2.24x throughput over A100 under matched settings

3.85x throughput over TPU v6e under matched settings

custom ISA, compiler, simulator, and DSE stack

**Problem:** Long-context agentic LLM inference generates large off-chip memory traffic from extended web, tool, and interaction histories, creating simultaneous bandwidth and capacity memory walls that leave compute units underutilized.

**Workload or benchmark:** Long-context agentic LLM inference involving web or computer-use inputs, tool-call trajectories, and extended contexts; evaluation uses simulated accelerator execution and matched multiplier/memory settings against A100 and TPU v6e references.

</details>

<span id="paper-isca-2026-program-069"></span>

### MTIA 300: Meta’s First Training Chip Featuring Built-in NICs and Collective Offloading Engines

ISCA 2026 · Record: `isca-2026-program-069`

[Read the step-by-step explanation](#explanation-isca-2026-program-069)

**Updated source-backed reading card**

Reviewed 2026-09-08. Reconciles the MTIA 300 card with the recovered primary paper; explains embedding/collective communication, integrated NICs, message engines, near-memory reduction, autonomous dependency graphs, communication versus Perf/TCO and power/cost boundaries from first principles.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Recommendation-model training is communication-bound because large embedding tables and hybrid parallelism generate AllReduce, AllToAll and AllGather traffic that competes with computation and synchronization.

**Mechanism / artifact:**

MTIA 300 compute and network-chiplet co-design with 12×800-Gbps RDMA NICs, 16 message engines, near-memory collective reduction and HCCL; collectives compile into autonomous dependency graphs rather than compute-grid kernels.

**Workload — the work tested:**

Approximately 150B-parameter DLRM using TorchRec/TorchInductor and distributed Shampoo; 40 MTIA 300 versus 40 H100 at local batch 6144 for communication, plus 1,000 TF32 4K×4K×4K GEMMs with collectives across 16 accelerators for overlap; other convergence and workload conditions are bounded by paper sections V.B–D.

**Hardware and manufacturing assumptions:**

MTIA 300 at 1.9 GHz, 216 GB HBM3E, 912 W TDP/667 W typical, compute and network chiplets, 12×800-Gbps RDMA NICs and 16 message engines; process node, measured workload energy and complete cost/amortization boundary are unspecified.

**Baseline — the comparison method:**

40 H100 with NCCL and TorchRec/TorchInductor

Table IV normalized Perf/TCO H100 reference 1.00

Communication, batch, software, numerical parity, system-cost, utilization and convergence parity are condition-specific

**Reported measurements:**

Primary paper Section V.D reports 3.9x communication performance versus H100 for 40 accelerators/local batch 6144; Table IV reports normalized Perf/TCO 1.39 for 40 MTIA 300/local batch 6144 versus 1.00 H100 and 1.42 for 24 MTIA 300/local batch 10240 with global batch held constant.

**Limits on the conclusion:**

Communication speedup, overlap microbenchmark performance, complete training-step throughput and normalized Perf/TCO have different denominators and must not be conflated.

Integrated NICs, message engines and near-memory reduction can reduce launch, movement or synchronization overhead but do not remove link capacity, dependency, small-message, datatype or imbalance limits.

TDP, typical platform power and chiplet dimensions are not measured energy per training step, total system area or complete TCO; amortization, cooling, networking and utilization inputs remain necessary.

The author-reported paper has not been independently replicated; other model sizes, collectives, batch/convergence tradeoffs, numerical parity and unsupported datatypes limit generalization.

**Source and location**

Evidence tier: Primary author pdf with selected sections/tables inspected; no independent replication, full cost accounting reconstruction or deployment validation. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://aisystemcodesign.github.io/papers/MTIA300_ISCA2026.pdf)

Primary MTIA 300 ISCA 2026 paper: Sections I–II for communication problem/hardware; Table I and PDF page 4 for clock/HBM/TDP/chiplets; Sections V.B–D PDF pages 10–11 and Table IV for DLRM, 40 MTIA/40 H100, 3.9x communication, normalized Perf/TCO 1.39/1.42 and batch conditions; Section VI PDF pages 12–13 for limitations.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** high_primary_author_pdf

**Baselines:** H100 with NCCL for collective operations; TorchRec/TorchInductor on both platforms for the production DLRM

Table IV reference: 40 H100 accelerators at local batch 6144, normalized Perf/TCO 1.00

**Evidence locators:** **Fields:** problem

method_or_artifact

**Location:** Sections I, II, IV

**Fields:** hardware_or_process_assumptions

**Location:** Table I, PDF page 4; Section II

**Fields:** workload_or_benchmark

baselines

metrics

**Location:** Sections V.B-D, PDF pages 10-11; Table IV visually inspected

**Fields:** limits

**Location:** Sections V.B and VI, PDF pages 10, 12-13

**Evidence url:** https://aisystemcodesign.github.io/papers/MTIA300_ISCA2026.pdf

**Hardware or process assumptions:** Table I: 1.9 GHz, 216 GB HBM3E, 912 W TDP (667 W typical), compute chiplet 25.6 x 31.4 mm, two network chiplets each 25.6 x 9.3 mm. Section II: 12 x 800 Gbps RDMA NICs and 16 message engines. Process node not established in extracted sections; TDP is not measured workload energy.

**Limits:** Author-reported evaluation, not independent replication. Communication speedup and Perf/TCO are distinct; neither establishes universal end-to-end speedup. Cost-accounting inputs and amortization assumptions were not found in the extracted evaluation and remain unresolved. Small-message collectives favor H100/NCCL; compute-heavy workloads, numerical parity, unsupported datatypes, eager overhead, and convergence/batch tradeoffs limit generality. Exact article-only 940 GB/s and less-than-0.5% figures remain supplemental, not paper-verified metrics.

**Method or artifact:** MTIA 300 co-designs compute, integrated network chiplets, dedicated message engines, near-memory collective reduction, and the HCCL communication library; collectives are compiled into autonomous dependency graphs rather than launched as compute-grid kernels.

**Metrics:** 3.9x communication performance relative to H100: 40 accelerators, local batch 6144, approximately 150B-parameter DLRM (V.D.1)

Normalized Perf/TCO 1.39 for 40 MTIA 300 at local batch 6144 versus 1.00 for 40 H100 at the same batch (Table IV)

Normalized Perf/TCO 1.42 for 24 MTIA 300 at local batch 10240 versus the Table IV H100 reference; global batch held constant

**Problem:** Recommendation-model training is communication-bound because embedding tables contain most model parameters and hybrid parallelism generates frequent AllReduce, AllToAll, and AllGather operations that compete with computation on GPU resources.

**Workload or benchmark:** DLRM of approximately 150B parameters implemented with TorchRec/TorchInductor and distributed Shampoo. Communication comparison: 40 MTIA 300 versus 40 H100, local batch 6144. Overlap microbenchmark: 1000 TF32 4K x 4K x 4K GEMMs with collectives across 16 accelerators.

</details>

<span id="paper-isca-2026-program-058"></span>

### Accelerating MoE with Dynamic In-Switch Computing on Multi-GPUs

ISCA 2026 · Record: `isca-2026-program-058`

[Read the step-by-step explanation](#explanation-isca-2026-program-058)

**Updated source-backed reading card**

Reviewed 2026-09-08. Reconciles the dynamic in-switch MoE card with the captured primary preprint; explains top-k expert routing, directional traffic, DySHARP addressing, token-centric dispatch/combine, simulator and layer/full-training boundaries from first principles while retaining withheld headline results.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Irregular MoE expert routing creates duplicated token movement, directional bandwidth imbalance, synchronization and queue pressure across multi-GPU systems.

**Mechanism / artifact:**

DySHARP dynamic multimem addressing plus token-centric dispatch/computation/combine fusion for dynamic in-switch MoE execution; switch operation, buffers, precision and address-update details are unspecified.

**Workload — the work tested:**

DeepSeek-V3-like small/medium/large configurations with top-k 8/16/32; main training evaluation and exploratory larger top-k settings; token distributions, batch, message sizes and layer/full-training conditions are bounded by the preprint but not fully extracted.

**Hardware and manufacturing assumptions:**

Customized Accel-Sim and BookSim2 simulation of 32-GPU GH200-NVL32-like node with H200-based GPUs and nine switches; 16-way pipeline parallelism across 16 nodes for end-to-end training; deployed hardware, switch implementation, buffers and calibration are unspecified.

**Baseline — the comparison method:**

DeepEP

NVLS static-collective workaround

FasterMoE

Tutel

CCFuser

COMET

DualPipe model-level comparison

Model, top-k, network, simulator, pipeline, precision and layer/full-training parity require verification

**Reported measurements:**

Numerical headline measurements are withheld in the current card pending figure/condition reconciliation; the captured evidence establishes simulation setup, top-k configurations and layer/full-training evaluation boundaries rather than a validated speedup.

**Limits on the conclusion:**

Top-k routing duplicates tokens and creates all-to-all dispatch/combine traffic whose bottleneck can be directional queue pressure rather than total bandwidth.

In-switch computation requires defined operation, data layout, ordering, precision and dependency state; moving work into a switch does not establish correct or lower-cost execution without those conditions.

Layer-level routing results do not establish full-training time, convergence, energy or pipeline behavior; simulation of a GH200-like node is not deployed hardware.

The primary preprint has no independent review or reproduction in the captured evidence, and numerical claims are withheld pending figure/condition reconciliation; simulator calibration, numerical correctness and generalization remain open.

**Source and location**

Evidence tier: Primary author preprint v1 with selected mechanism/setup extraction; no deployed hardware, simulator calibration, independent reproduction or reconciled numerical results. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://arxiv.org/html/2605.05607v1)

Primary arXiv preprint v1 and data/review-packets/isca-2026-program-058.json: DySHARP dynamic multimem addressing; token-centric dispatch/computation/combine; DeepSeek-V3-like top-k 8/16/32; Accel-Sim/BookSim2 32-GPU GH200-NVL32-like simulation; nine switches; 16-node/16-way pipeline; headline figures withheld pending reconciliation.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_primary_preprint

**Baselines:** DeepEP

NVLS static-collective workaround

FasterMoE

Tutel

CCFuser

COMET

DualPipe (model-level only)

**Evidence locators:** **Fields:** method_or_artifact

**Location:** III-IV

**Fields:** workload_or_benchmark

hardware_or_process_assumptions

baselines

**Location:** V.A-C

**Fields:** limits

**Location:** VI.A, Figures 14-16

**Evidence url:** https://arxiv.org/html/2605.05607v1

**Hardware or process assumptions:** Customized Accel-Sim plus BookSim2; simulated 32-GPU GH200 NVL32-like node, H200-based GPU configuration, nine switches. End-to-end training uses 16-way pipeline parallelism across 16 nodes.

**Limits:** Simulation is not deployed hardware. Operator calibration does not validate all proposed hardware behavior. Layer and full-training results are distinct; numerical claims withheld pending figure/condition reconciliation. No independent review or reproduction.

**Method or artifact:** DySHARP dynamic multimem addressing plus token-centric dispatch/computation/combine fusion.

**Metrics:** Not established in the captured evidence.

**Problem:** Irregular expert routing creates redundant transfers and directional bandwidth imbalance.

**Workload or benchmark:** DeepSeek-V3-like small/medium/large configurations; top-k 8/16/32. Main evaluation is training; larger top-k settings are exploratory.

</details>

<span id="paper-isca-2026-program-005"></span>

### Patterns Behind Chaos: Forecasting Data Movement for Efficient Large-Scale MoE LLM Inference

ISCA 2026 · Record: `isca-2026-program-005`

[Read the step-by-step explanation](#explanation-isca-2026-program-005)

**Updated source-backed reading card**

Reviewed 2026-09-08. Reconciles the Patterns Behind Chaos card with the captured primary preprint and released trace dataset; explains MoE data movement, temporal/spatial routing structure, expert placement, prefill/decode differences, forecast staleness and topology-bound speedups from first principles.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Large-scale MoE inference moves tokens to distributed experts, and routing-driven data movement can dominate serving latency, bandwidth and energy.

**Mechanism / artifact:**

Data-movement-centric temporal/spatial profiling, distilled placement insights, lightweight wafer-scale architectural modifications and a prefill-aware expert-placement algorithm; forecasting model, horizon and fallback are unspecified.

**Workload — the work tested:**

Four 200B–1000B MoE models released in 2025, more than 24,000 requests across diverse workloads, wafer-scale GPU architectures and existing GPU systems; routing traces, batch, topology and prefill/decode split conditions are not fully extracted.

**Hardware and manufacturing assumptions:**

Wafer-scale GPU and multi-GPU serving systems; expert placement, memory capacity, link topology, bandwidth, congestion, software runtime, energy and architectural-modification assumptions are topology-specific.

**Baseline — the comparison method:**

Existing GPU MoE serving systems

Existing expert-placement approaches

Model, trace, batching, topology, expert capacity, prefill/decode, software and quality parity require verification

**Reported measurements:**

The primary preprint reports 6.6x average speedup on wafer-scale GPUs, up to 1.25x speedup on existing GPU MoE computation, more than 24,000 profiled requests and 200B–1000B model scale; exact page/table locations and aggregation conditions are not recorded.

**Limits on the conclusion:**

Routing structure can support placement decisions only when it persists long enough to act on and remains valid for the current model, request mix, batch, topology and load.

A forecast needs an error metric, horizon, refresh and fallback rule; stale or wrong predictions can create link/expert hotspots and worsen tail latency.

Prefill and decode have different token rates and movement patterns, so a placement optimized for one phase does not automatically optimize the other.

The author preprint and trace dataset have not been independently checked for the six insights, wafer-scale model or transfer to other routing distributions/interconnects; speedups remain topology and trace bounded.

**Source and location**

Evidence tier: Primary author preprint plus released trace dataset reference; no independent trace/insight check, wafer scale reproduction or cross topology placement validation. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://arxiv.org/abs/2510.05497)

Primary arXiv preprint and released trace dataset reference in data/review-packets/isca-2026-program-005.json: temporal/spatial data-movement profiling; distilled placement insights; wafer-scale modifications; prefill-aware placement; four 200B–1000B models; >24,000 requests; 6.6x wafer-scale average and up-to-1.25x existing-GPU speedups; exact full-paper locations not recorded.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** high_primary_preprint

**Baselines:** existing GPU MoE serving systems

existing expert-placement approaches

**Evidence locators:** Not established in the captured evidence.

**Evidence url:** https://arxiv.org/abs/2510.05497

**Hardware or process assumptions:** Wafer-scale GPU and multi-GPU serving systems; reported architectural gains depend on the evaluated expert-selection traces and target topology.

**Limits:** The evidence is an author preprint and released trace dataset; the repository has not independently checked the six insights, reproduced the wafer-scale model, or tested whether the placement conclusions transfer to other MoE routing distributions and interconnects.

**Method or artifact:** Data-movement-centric temporal/spatial profiling, distilled placement insights, lightweight wafer-scale architectural modifications, and a prefill-aware expert-placement algorithm.

**Metrics:** 6.6x average speedup on wafer-scale GPUs

up to 1.25x speedup on existing GPU MoE computation

more than 24,000 profiled requests

200B–1000B model scale

**Problem:** Random expert selection in large Mixture-of-Experts inference creates data-movement overhead that can dominate serving systems.

**Workload or benchmark:** Four 200B–1000B MoE models released in 2025, more than 24,000 requests across diverse workloads, wafer-scale GPU architectures, and existing GPU systems.

</details>

## What remains to establish

Resolve unspecified workloads, comparison methods, resource budgets, and source locations before generalizing a reported gain. Multiple papers in this selected sample permit comparison of mechanisms, but do not by themselves establish recurrence across years or a long-term trend.

[All subthemes](../expanded-taxonomy-v1.md) · [Research directions](../directions/README.md)
