# Graph learning for EDA

This subject has 5 records in the selected sample. This page explains where it fits, then presents all captured paper evidence without shortening the measurements or limitations.

[Definitions used in the paper records](../reading-guide-v1.md)

## Understand the parent subject first

- [AI assisted EDA](../themes/ai-assisted-eda.md)

## Why represent a circuit as a graph?

A graph records objects and their connections. For a circuit task, an object might be a cell, pin, or electrical node; a connection might represent a signal dependency or an electrical relationship. Choosing the representation is already an engineering decision. A graph of logical connectivity does not automatically contain wire geometry, resistance, operating voltage, or input activity.

A graph neural network learns how information about connected objects contributes to a prediction. In a common message-passing formulation, each node combines information from its neighbors, optionally using attributes of their connecting edges, then updates its own representation. Repeating this process allows information to travel farther through the graph. This describes a model family, not the exact implementation of each paper below. [PyTorch Geometric's message-passing documentation](https://pytorch-geometric.readthedocs.io/en/latest/tutorial/create_gnn.html) gives the underlying formulation.

The important question is not merely whether the circuit is graph-shaped. It is whether the chosen objects, connections, features, and computation preserve the information required by the target electrical or design task.

## Cell timing and whole-path timing are different targets

A cell's delay depends on its operating conditions and electrical loading. A path joins multiple timing relationships, so arrival time depends on more than one cell. The remaining time before a required arrival deadline is called slack; negative slack indicates that the modeled requirement is missed. Conventional analysis uses a circuit description, timing libraries, constraints, and wire-related electrical information. [OpenSTA's documentation](https://openroad.readthedocs.io/en/latest/main/src/sta/README.html) identifies these inputs, including Liberty libraries and SPEF parasitics.

<span id="explanation-dac-2026-research1562"></span>

### PG-GNN: reducing cell-library characterization without losing timing conditions

### What cell-library characterization produces

A standard-cell timing library records how a cell responds under specified conditions. For a timing arc, the input transition rate and output load are independent conditions: a slowly changing input is not the same as a heavily loaded output. Process, voltage and temperature (PVT) corners add further conditions. A characterization flow evaluates many combinations with circuit simulation, then stores delay and transition values for use by static-timing analysis.

The cost comes from the number of combinations and the electrical simulation required at each one. Skipping simulations is useful only if the predicted table remains accurate where the timing flow will use it, including corners and conditions near a design limit. An average error over easy points can hide a bad value at a rare but critical slew/load/corner combination.

### What PG-GNN changes

PG-GNN uses sparse **anchor PVT corners** as direct simulation points, constructs a physics-consistent reference, and trains a graph neural network to predict the residual between that reference and the remaining values. Residual learning means the model does not learn the full timing surface from zero; it learns the correction to a chosen baseline. This can reduce the complexity of the learned target, but its validity depends on the reference being appropriate across the unmeasured region.

The method then uses **uncertainty-driven active learning** to select additional points for labeling. Instead of spending the same simulation effort everywhere, it queries points where the model is uncertain. The saved effort depends on how uncertainty is computed, how new labels update the model, what stopping rule is used, and whether uncertainty is calibrated near the worst errors. A point-selection policy can lower the number of labels without guaranteeing lower total characterization time if model training, data movement, or repeated retraining is substantial.

The official description reports a 98.7% reduction in SPICE effort and 1.67% MAPE for TSMC 16 nm libraries, plus 0.74% critical-path delay mismatch on ISCAS'89 benchmarks versus foundry libraries. It does not define the effort denominator, MAPE aggregation, corner coverage, library cells, train/test split, foundry comparison conditions, or complete timing-flow boundary. “Signoff-level accuracy” is therefore a source claim that requires the missing conditions; it is not established by the description alone. [Source: official DAC description and captured record](https://63dac.conference-program.com/presentation/?id=RESEARCH1562&sess=sess155).

### The evaluation that would establish characterization usefulness

Hold out complete cells, PVT corners, slew/load regions, and circuit designs separately. Report worst-case and percentile delay/slew error, not only MAPE; count timing-limit violations; measure simulation count, simulator time, model-training time, active-learning overhead, and total wall-clock effort. Run static timing with the generated library and compare critical-path delay and slack against the same foundry or SPICE reference. The physics reference and active learner need ablations so their separate contributions are visible.

[PG-GNN](../observed-subthemes/graph-learning-for-eda.md#paper-dac-2026-research1562) targets cell-library characterization. The detailed explanation above separates PVT/slew/load conditions, residual prediction, active-learning label cost, mean error and worst-case timing risk; this card is the compact evidence record.

<span id="explanation-dac-2026-research2333"></span>

### PBA-rGAT-Edge: predicting timing quantities is not the same as proving timing

### Start with the timing objects

An **arc** is a local timing relationship, such as the delay and output transition produced by a cell when an input transition and output load are known. A **path** is a sequence of arcs connected by the circuit's signal dependencies. A path-based timing result depends on the combination of arcs, the path's start and end conditions, constraints, and the electrical information used by the timing engine. An arc predictor can be accurate on average while still making a path-level decision wrong near the required timing limit.

Path-Based Analysis (PBA) follows a particular path and can avoid some pessimism introduced by combining independently worst-case local conditions. Graph-Based Analysis (GBA) is generally cheaper because it reuses graph calculations, but its approximation can be conservative. Replacing an expensive analysis with a learned predictor is therefore a decision-risk problem, not only a regression problem: the predictor must preserve the timing ordering and the violations that affect design closure.

### What PBA-rGAT-Edge changes

The source describes a pin-level timing graph in which nodes represent timing points and edges carry timing relationships. PBA-rGAT-Edge predicts arc-level delay and slew using residual edge-aware graph attention, a lightweight fusion stage, and a dual-task output head. **Edge-aware** means the information carried by a connection can affect the update; this matters because an edge can represent a different timing relationship from another edge attached to the same pins. **Path-based features** provide context beyond the immediate neighborhood. **Residual connections** provide a direct information path across layers, which can help optimization but does not guarantee that the learned representation preserves every timing dependency.

Delay and slew are related but distinct outputs. Delay is the time shift of a signal transition. Slew describes how quickly that transition changes. They influence one another through cell and interconnect behavior, but predicting one well does not establish that the other is well predicted. A dual-task head must be evaluated for both tasks and for their effect on path construction and timing-limit decisions.

The official description reports R² values of 0.965 for slew and 0.997 for delay on million-scale industrial benchmarks and says convergence is faster than prior GNN methods, including DeepEdgeGAT. R² measures explained variation under a chosen dataset and aggregation; it is not a worst-case error, a percentage accuracy, a signoff-equivalence result, or proof of correct violation ranking. The description does not identify the designs, process corners, timing labels, split, graph-size unit, hardware, convergence measure, or path-level decision results. [Source: official DAC description and captured record](https://63dac.conference-program.com/presentation/?id=RESEARCH2333&sess=sess177).

### The evaluation that would establish timing-flow usefulness

Compare against the same PBA/GBA labeling flow and report absolute error distributions for delay and slew, especially near setup and hold limits. Measure missed violations, false violations, top-critical-path overlap, worst negative slack error, and the effect of using predictions in a complete optimization or signoff loop. Hold out complete designs and process corners to test transfer. Report training and inference time separately from the timing-engine time saved. A high R² on arc values is useful only if it leads to safe path-level decisions at the boundary that engineers actually use.

[PBA-rGAT-Edge](../observed-subthemes/graph-learning-for-eda.md#paper-dac-2026-research2333) targets timing at arc and path level, incorporating edge information and path context. The detailed explanation above separates arc regression, path composition, delay versus slew, PBA/GBA cost, and timing-limit risk; this card is the compact evidence record.

## Coupled wires need more than logical connectivity

<span id="explanation-dac-2026-research2537"></span>

### Crosstalk timing: the graph must carry electrical coupling, not only connectivity

### What the electrical problem is

When nearby wires switch, their electric fields couple through capacitance. A changing signal on one net can alter the transition of another net. The **aggressor** is the switching source of the disturbance; the **victim** is the net whose transition is affected. These terms describe an electrical relationship, not ownership in the logic design.

An RC network represents resistance and capacitance along wires and through connected structures. Crosstalk timing depends on which nets are adjacent, how strongly they couple, the direction and timing of their transitions, their driver strengths, their loads, and the surrounding network. A graph that stores only “cell A connects to cell B” omits the values and conditions that determine the disturbance. A graph model must therefore encode the relevant electrical edges, switching context, and multi-net structure or it cannot be expected to predict the reference timing quantity.

### What the graph-prompt method changes

The source describes a dual-level graph prompt architecture. **Node-level prompts** are intended to capture fine-grained coupling effects around individual graph elements. **Subgraph-level prompts** are intended to represent holistic interactions among multiple coupled nets. Prompt learning here means adapting a pretrained graph model with additional learned information or task-conditioning; the official description does not specify the prompt parameters, input features, adaptation budget, or frozen versus trainable components, so those details cannot be inferred from the name.

The two levels correspond to different failure modes. A local prompt may represent a nearby coupling value while missing an interaction that travels through a larger RC structure. A subgraph prompt may represent the larger interaction while losing a local switching condition. The method must be evaluated on both local and multi-net cases, including cases where the electrically important relationship is not the shortest graph path.

The official description says the method predicts crosstalk timing and consistently outperforms existing methods across benchmark designs. It supplies no absolute error, worst-case slack error, process condition, benchmark identity, graph construction, prompt-training cost, transfer split, or signoff correlation. The source therefore supports the proposed representation and evaluation direction, not a universal timing or process-transfer result. [Source: official DAC description and captured record](https://63dac.conference-program.com/presentation/?id=RESEARCH2537&sess=sess155).

### The evaluation that would establish usefulness

Use a reference crosstalk analysis with the same RC extraction, process corner, driver/load conditions, and transition scenarios for every method. Report delay and slew error distributions, errors near setup/hold limits, missed and false violations, critical-net ranking, inference cost, prompt-adaptation cost, and transfer to unseen designs or corners. Ablate node-level prompts and subgraph-level prompts separately. A high average correlation is insufficient if the method misses the small set of coupled nets that determines timing closure.

The [crosstalk timing paper](../observed-subthemes/graph-learning-for-eda.md#paper-dac-2026-research2537) works with aggressor-victim resistance-capacitance networks and a dual-level graph-prompt method. The detailed explanation above separates electrical coupling from logical connectivity, local from multi-net context, and prediction quality from signoff evidence; this card is the compact evidence record.

<span id="explanation-dac-2026-research194"></span>

## TRACE: learning circuit computation requires position, hierarchy, and a defined target

### What it means to compute on a circuit graph

A circuit graph is not merely a list of connected nodes. Its nodes can represent gates, registers, pins, or other circuit objects; its edges can represent signal dependencies. A useful model must preserve enough information to answer the target question: for example, which signal values depend on which earlier values, where state is stored, and how a sequence of operations combines inputs. The graph representation alone does not define the target. The output might be a node label, a signal value, a whole-circuit function, a timing quantity, or a design decision.

### Why ordinary neighborhood aggregation can lose computation order

Many graph models update a node by combining messages from neighboring nodes. If the combination is permutation-invariant, reordering the neighbors produces the same summary. That property is useful when neighbor order has no meaning. It is a problem when two inputs occupy different computational positions or when the same local pieces are combined in different stages. A summary can preserve which neighbors exist while losing the ordered and hierarchical route by which their values affect the output.

TRACE proposes a hierarchical Transformer intended to follow the step-by-step flow of computation. The conceptual claim is that the model's information path should reflect the circuit's computational structure rather than repeatedly applying a generic, order-insensitive neighborhood reduction. “Hierarchical” must be made concrete in a full paper: the graph levels, the tokens or subgraphs at each level, the direction of information flow, and the way sequential state is represented. The official description names the backbone but does not supply those implementation details.

### What function-shift learning changes

Let the desired circuit behavior be a function (F(x)) of the input (x). A direct learner tries to predict (F) in one step. TRACE instead defines a simpler local approximation (F_0(x)) that assumes input independence, then trains the model to predict the difference (F(x)-F_0(x)). This is a change in the learning target, not a proof that the difference is always easier to learn. The method can help only if the local approximation captures a useful part of the behavior and the remaining shift is represented accurately across the tested graph family.

The two claims must be evaluated separately. The hierarchical backbone concerns how graph structure is represented. Function-shift learning concerns what numerical function the model is asked to predict. An ablation that removes one while retaining the other is necessary to attribute any improvement. The evaluation must also state whether the target is Boolean behavior, a numerical circuit function, a graph property, or a downstream EDA quantity; “learning computation” is not itself a metric.

The official description says TRACE is validated on RTL graphs, And-Inverter Graphs, and post-mapping netlists and qualitatively reports that it outperforms prior architectures. It supplies no target definitions, dataset identities, accuracy values, train/test split, graph sizes, runtime, transfer test, or downstream PPA result. The source therefore supports the proposed representation and objective at a conceptual level, not a verified general-purpose circuit-function learner. [Source: official DAC description and captured record](https://63dac.conference-program.com/presentation/?id=RESEARCH194&sess=sess177).

### The evaluation that would establish the contribution

Use the same circuit families, targets, training budget, graph encoding, and metric for four comparisons: the proposed hierarchy with direct learning; the proposed hierarchy with function-shift learning; a conventional backbone with direct learning; and a conventional backbone with function-shift learning. Hold out complete designs, not only nodes from designs seen during training. Then report target error, exact or task-specific correctness, graph size, training and inference cost, and failure cases near the decision boundary. If the learned output drives synthesis, timing or optimization, run the complete downstream flow and compare the final design result against the reference tool, including harmful predictions and the cost of checking them.

## Learning circuit computation and making training practical

[TRACE](../observed-subthemes/graph-learning-for-eda.md#paper-dac-2026-research194) proposes a hierarchical Transformer and function-shift objective for learning computation on RTL graphs, And-Inverter Graphs, and post-mapping netlists. The detailed explanation above separates graph-structure representation from the learning target and preserves the missing task, metric, dataset, and generalization conditions; this card is the compact evidence record.

<span id="explanation-dac-2026-research795"></span>

### GSR-GNN: making deep circuit-graph training fit within memory

### The resource problem is created by depth

A graph neural network updates node representations through repeated layers. One layer lets information move a limited distance through the graph; many layers can expose a node to a larger structural neighborhood. During training, the system usually retains intermediate representations so it can compute gradients later. If the graph has many nodes and the network has many layers, storing those representations can dominate memory even when the final model parameters are modest.

Depth also costs time. Each layer may require graph reads, message aggregation, nonlinear transformation, and synchronization. More layers can improve the receptive field, but the additional work is useful only if the target task benefits from the extra structural information. A memory reduction that prevents deep training is not equivalent to a memory reduction that preserves the same depth and task quality.

### What GSR-GNN changes

GSR-GNN combines three mechanisms described in the source. **Reversible residual modules** allow earlier activations to be reconstructed from later values under the method’s mathematical conditions, reducing the amount that must be stored during backpropagation. Reconstruction itself consumes compute; memory saved by recomputation must therefore be compared with the added operations and runtime.

The **group-wise sparse nonlinear operator** compresses node embeddings by applying a structured sparsifying transformation to groups of values. The source says this reduces representation cost without sacrificing task-relevant information. That phrase needs a measurable definition: the task metric, acceptable degradation, group structure, sparsity pattern, and behavior on different graph sizes must be reported. Sparsity in an embedding is also not automatically a reduction in physical memory traffic unless the execution pipeline can store and process the representation in that form.

The **optimized execution pipeline** targets fragmented activation storage and data movement. This is a systems contribution in addition to the model changes. Its benefit depends on allocation behavior, graph layout, batch construction, kernel implementation, and hardware. The three mechanisms should be ablated separately; otherwise a total speedup cannot be assigned to reversibility, sparsity, or execution organization.

The official description reports up to 87.2% peak-memory reduction and over 30× training speedup on sampled circuit graphs, with negligible degradation in correlation-based quality metrics. It does not name the tasks, graph sizes, hardware, depth, baseline implementation, metric values, sampling procedure, or memory/speed measurement boundary. The source therefore supports a training-efficiency proposal and bounded reported claims, not a universal deep-GNN improvement or proof that downstream EDA decisions remain unchanged. [Source: official DAC description and captured record](https://63dac.conference-program.com/presentation/?id=RESEARCH795&sess=sess177).

### The evaluation that would establish practical benefit

Compare models at the same depth, graph, batch, optimizer, training budget, and target quality. Report peak allocated memory, persistent model memory, temporary workspace, graph-storage memory, recomputation operations, training time, throughput, and energy separately. Test shallow and deep baselines, full and sampled graphs, different graph sizes, and complete-design holdouts. If the learned result is used in an EDA flow, measure the final timing, area, power, or correctness outcome and include the cost of reference analysis.

[GSR-GNN](../observed-subthemes/graph-learning-for-eda.md#paper-dac-2026-research795) addresses training time and memory consumption for deeper graph models. The detailed explanation above separates activation storage, reversible reconstruction, embedding compression, execution movement, and downstream task quality; this card is the compact evidence record.

## Generalization must be tested at the design level

Splitting nearby nodes from the same circuit between training and evaluation can leave much of the same structure visible to the model. Success under that split is weaker evidence for use on a new circuit than withholding entire designs. Further tests can withhold a design family, cell library, or fabrication technology, but these are different transfer claims and should be reported separately.

The five records motivate graph representations that retain more of the information relevant to the task, while keeping training affordable. They do not establish a shared performance improvement or a historical growth rate. A useful end-to-end study would show both prediction quality on unseen designs and the consequences of using those predictions in a design flow, including incorrect decisions and the cost of final reference checks.

## Compare the results carefully

First identify the inputs and required output quality. Then identify the limited resource: time, memory, communication, energy, circuit area, or correctness coverage. Ask which part of the method reduces that cost and which new cost it adds. Compare numbers only when the experiments hold these conditions sufficiently similar.

A conference description may explain the proposal while omitting the full experiment. An author preprint link may have been coded from its abstract. The source classification does not by itself establish that every table was read. Missing locations remain visible below.

## Complete captured evidence

These are evidence records, not substitutes for the explanations above. Each record preserves its problem, proposed method, measurements, comparison conditions, and source limits. A populated record does not establish that its mechanism has been fully explained or independently verified.

<span id="paper-dac-2026-research194"></span>

### TRACE: Learning to Compute on Circuit Graphs

DAC 2026 · Record: `dac-2026-research194`

[Read the step-by-step explanation](#explanation-dac-2026-research194)

**Updated source-backed reading card**

Reviewed 2026-09-08. Reconciles the TRACE card with the captured official source; separates circuit-graph representation, hierarchical information flow, function-shift learning and downstream task meaning, and prevents qualitative outperformance language from being read as a verified circuit-function or EDA-flow result.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Learning circuit computation requires a graph model that preserves position-aware and hierarchical dependencies rather than only an order-insensitive neighborhood summary.

**Mechanism / artifact:**

TRACE combines a hierarchical Transformer intended to follow circuit computation flow with function-shift learning: it predicts the difference between the global circuit function and a local input-independence approximation instead of predicting the global function directly.

**Workload — the work tested:**

Circuit graphs from RTL, And-Inverter Graphs and post-mapping netlists; target tasks, datasets, graph sizes, labels and train/test split are unspecified.

**Hardware and manufacturing assumptions:**

Learned graph-computation model operating on netlist representations; graph encoding, compute platform, model size, training budget and downstream EDA integration are unspecified.

**Baseline — the comparison method:**

Prior graph architectures

Backbone and objective ablations needed to attribute the claimed gain; identities and parity are unspecified

**Reported measurements:**

The official description qualitatively claims substantial improvement over prior architectures, but supplies no accuracy, exact-correctness, runtime, transfer, generalization or downstream PPA value.

**Limits on the conclusion:**

A permutation-invariant neighborhood summary can lose computational position, but a hierarchical backbone does not automatically prove that the relevant order, state or long-range dependency has been represented correctly.

Function-shift learning changes the target to a residual relative to a local independence approximation; it can help only when that approximation and residual are defined and evaluated across the target graph family.

RTL, AIG and post-mapping netlists are different representations; performance on one representation does not establish transfer to another or to a fabricated design flow.

The official description supplies no task definition, dataset, metric, split, ablation, numerical result or independent execution; no general circuit-function, equivalence, timing, synthesis or PPA claim follows.

**Source and location**

Evidence tier: Primary captured official DAC description only; no full paper extraction, graph model execution or independent task/generalization validation. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH194&sess=sess177)

DAC 2026 official description and data/review-packets/dac-2026-research194.json: position-aware hierarchical computation problem; Hierarchical Transformer backbone; function-shift residual objective relative to input-independence approximation; RTL/AIG/post-mapping validation; qualitative outperformance claim.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** generic GNN

handcrafted circuit graph features

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH194

**Hardware or process assumptions:** Netlist/circuit graph representation; technology and downstream tool assumptions are unspecified.

**Limits:** No accuracy, transfer, scale, runtime, or downstream PPA results are reported.

Graph models may memorize design-family structure.

Official description only; cross-design validation is required.

**Method or artifact:** Learned computation framework operating directly on circuit graphs.

**Metrics:** Circuit-graph task quality is claimed qualitatively

**Problem:** Circuit graph tasks require topology-aware learned computation beyond generic graph embeddings.

**Workload or benchmark:** Circuit graph prediction or optimization tasks; targets, datasets, and baselines are unspecified.

</details>

<span id="paper-dac-2026-research2333"></span>

### PBA-rGAT-Edge: Arc-Level Path-Based Timing Prediction with Scalable Residual Edge-Aware Graph Attention

DAC 2026 · Record: `dac-2026-research2333`

[Read the step-by-step explanation](#explanation-dac-2026-research2333)

**Updated source-backed reading card**

Reviewed 2026-09-08. Reconciles the PBA-rGAT-Edge card with the captured official source; separates arc-level delay/slew regression from path-level timing decisions, edge/path context from generic graph aggregation, and R-squared from worst-case or signoff evidence.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Path-based timing analysis is accurate but expensive while graph-based analysis is faster and can be pessimistic; a learned predictor must preserve timing-critical decisions, not only average local values.

**Mechanism / artifact:**

PBA-rGAT-Edge predicts delay and slew on a pin-level timing graph using residual edge-aware graph attention, path-based features, lightweight fusion and a dual-task head.

**Workload — the work tested:**

Million-scale industrial timing benchmarks; design identities, graph-size unit, timing labels, process corners, path types and train/test split are unspecified.

**Hardware and manufacturing assumptions:**

Learned timing-prediction flow replacing or supplementing timing analysis; timing engine, library/parasitic inputs, process conditions, training hardware and inference deployment are unspecified.

**Baseline — the comparison method:**

Prior GNN-based timing predictors including DeepEdgeGAT (ASPDAC 2023)

PBA/GBA timing references and resource parity are unspecified

**Reported measurements:**

The official description reports R-squared 0.965 for slew and 0.997 for delay and qualitatively claims faster convergence; it supplies no absolute error, worst-case error, path-ranking, violation-detection or timing-flow speed result.

**Limits on the conclusion:**

R-squared measures explained variation under a dataset; it is not a percentage accuracy, a bounded timing error or proof that critical paths and violations are preserved.

Arc delay and slew predictions are not path-level timing decisions. Errors can compound or change path ordering near setup/hold limits even when average arc metrics are high.

Edge-aware attention and path features can encode useful context without proving that process corners, library conditions, parasitics and sequential constraints are represented correctly.

The official description supplies no design identities, split, timing-label flow, corner coverage, path-level decisions or independent execution; no signoff-equivalence, cross-corner transfer or safe optimization claim follows.

**Source and location**

Evidence tier: Primary captured official DAC description only; no full paper extraction, timing flow execution or independent path/signoff validation. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH2333&sess=sess177)

DAC 2026 official description and data/review-packets/dac-2026-research2333.json: PBA/GBA cost and pessimism problem; pin-level graph; residual edge-aware attention; path features; dual-task delay/slew prediction; reported R-squared values and DeepEdgeGAT comparison.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** cell-local timing model

standard GNN timing predictor

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH2333

**Hardware or process assumptions:** Static-timing analysis flow with graph features; process and timing engine assumptions are unspecified.

**Limits:** No slack error, ranking, runtime, transfer, or design-scale results are reported.

Timing labels and graph topology may be tool-specific.

Official description only; held-out design validation is required.

**Method or artifact:** Residual edge-aware graph-attention timing predictor with path-based features.

**Metrics:** Timing-prediction accuracy and scalability are claimed qualitatively

**Problem:** Timing prediction must capture path context and edge effects across large circuit graphs.

**Workload or benchmark:** ASIC timing graphs; libraries, labels, path types, and baselines are unspecified.

</details>

<span id="paper-dac-2026-research2537"></span>

### Crosstalk Timing Prediction via Graph Prompt Learning in Aggressor-Victim RC Networks

DAC 2026 · Record: `dac-2026-research2537`

[Read the step-by-step explanation](#explanation-dac-2026-research2537)

**Updated source-backed reading card**

Reviewed 2026-09-08. Reconciles the crosstalk timing card with the captured official source; separates aggressor-victim RC coupling from logical connectivity, node-level from subgraph-level prompts, and qualitative outperformance from signoff-correlated timing evidence.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Crosstalk timing depends on coupled resistance-capacitance networks, switching conditions and multi-net interactions, making repeated analysis expensive and difficult to represent with ordinary connectivity graphs.

**Mechanism / artifact:**

Dual-level graph prompt learning for aggressor-victim crosstalk timing: node-level prompts target fine-grained coupling effects and subgraph-level prompts target holistic multi-net interactions while adapting a pretrained graph model.

**Workload — the work tested:**

Crosstalk timing on aggressor-victim RC networks and benchmark designs; design identities, extracted features, process corners, switching scenarios, labels and splits are unspecified.

**Hardware and manufacturing assumptions:**

Learned crosstalk-timing prediction flow using RC graph representations; extraction tool, timing reference, model hardware, prompt-training cost and signoff integration are unspecified.

**Baseline — the comparison method:**

Traditional crosstalk analysis

Existing graph-learning timing models

Baseline identities, RC parity and timing-label conditions are unspecified

**Reported measurements:**

The official description qualitatively claims precise prediction and consistent outperformance across benchmark designs; it supplies no numeric error, worst-case slack, ranking, runtime, adaptation cost or signoff-correlation value.

**Limits on the conclusion:**

Logical connectivity does not contain coupling capacitance, resistance, switching alignment, driver strength or load; graph prediction quality depends on whether these conditions are represented.

Node-level and subgraph-level prompts can capture different scales of interaction, but the description does not define prompt inputs, adaptation budget, trainable parameters or the cases each level covers.

Average prediction quality can hide missed coupled nets near timing limits; critical-net ranking, false/missed violations and worst-case error are separate requirements.

The official description supplies no benchmark identities, process conditions, RC extraction, transfer split, numerical result or independent execution; no signoff equivalence or process-transfer claim follows.

**Source and location**

Evidence tier: Primary captured official DAC description only; no full paper extraction, rc/timing execution or independent signoff correlation validation. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH2537&sess=sess155)

DAC 2026 official description and data/review-packets/dac-2026-research2537.json: crosstalk coupling/multi-net limitation; dual-level node/subgraph graph prompts; aggressor-victim RC timing; qualitative precise-prediction and outperformance claims.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** traditional crosstalk analysis

generic graph neural predictor

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH2537

**Hardware or process assumptions:** Advanced-node interconnect timing flow; extraction and noise assumptions are unspecified.

**Limits:** No delay error, worst-case ranking, runtime, process-transfer, or scale results are reported.

Prompt behavior may depend on RC graph distribution.

Official description only; signoff-correlated validation is required.

**Method or artifact:** Graph prompt-learning model for aggressor-victim crosstalk timing.

**Metrics:** Crosstalk prediction efficiency is claimed qualitatively

**Problem:** Crosstalk timing depends on coupled RC structures and is expensive to evaluate repeatedly.

**Workload or benchmark:** RC networks and crosstalk timing cases; labels, process, and baselines are unspecified.

</details>

<span id="paper-dac-2026-research1562"></span>

### PG-GNN: Physics-Guided Graph Neural Network for Cell Timing Library Characterization

DAC 2026 · Record: `dac-2026-research1562`

[Read the step-by-step explanation](#explanation-dac-2026-research1562)

**Updated source-backed reading card**

Reviewed 2026-09-08. Reconciles the PG-GNN card with the captured official source; separates cell-library timing conditions, physics-reference residual learning, uncertainty-driven label selection, SPICE effort, MAPE and downstream critical-path mismatch, and bounds signoff language to the stated evidence.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Standard-cell timing-library characterization requires many expensive circuit simulations across input transition, output load and process/voltage/temperature conditions.

**Mechanism / artifact:**

PG-GNN samples sparse anchor PVT corners, constructs a physics-consistent reference, learns residual timing errors with a graph neural network, and uses uncertainty-driven active learning to select additional simulation points.

**Workload — the work tested:**

TSMC 16 nm standard-cell libraries and ISCAS'89 circuit benchmarks; cells, arcs, PVT ranges, slew/load grid, labels, split and critical-path aggregation are unspecified.

**Hardware and manufacturing assumptions:**

SPICE-based library characterization and learned surrogate; simulator, process/corner setup, training hardware, active-learning overhead and static-timing integration are unspecified.

**Baseline — the comparison method:**

SPICE characterization effort reference

Foundry libraries for critical-path comparison

Effort denominator and comparison conditions are unspecified

**Reported measurements:**

The official description reports 98.7% SPICE-effort reduction, 1.67% MAPE on TSMC 16 nm libraries and 0.74% critical-path delay mismatch on ISCAS'89 versus foundry libraries; aggregation and measurement boundaries are unspecified.

**Limits on the conclusion:**

MAPE is an average relative error and does not bound the worst slew/load/corner or timing-critical error; a small mean can coexist with a harmful outlier.

Residual learning depends on the physics-consistent reference remaining useful outside the anchor points; the description does not define the reference, error model or transfer range.

Active learning can reduce labeled points while adding uncertainty estimation, model updates and retraining cost; SPICE-label reduction is not automatically total characterization wall-clock reduction.

The official description supplies no cell/corner grid, split, uncertainty calibration, signoff procedure or independent execution; the source's signoff-level and orders-of-magnitude claims are not independently established.

**Source and location**

Evidence tier: Primary captured official DAC description only; no full paper extraction, spice/timing flow execution or independent signoff validation. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH1562&sess=sess155)

DAC 2026 official description and data/review-packets/dac-2026-research1562.json: standard-cell characterization bottleneck; anchor PVT simulation; physics-consistent residual reference; uncertainty-driven active learning; TSMC 16 nm 98.7% SPICE-effort/1.67% MAPE and ISCAS'89 0.74% critical-path mismatch claims.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** SPICE characterization

physics-agnostic GNN predictor

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH1562

**Hardware or process assumptions:** Cell characterization and SPICE-like simulation flow; device and parasitic assumptions are unspecified.

**Limits:** No delay/slew error, simulation reduction, transfer, or cell-library results are reported.

Physics guidance may encode node-specific assumptions.

Official description only; signoff-correlated validation is required.

**Method or artifact:** Physics-guided graph neural predictor for cell timing characterization.

**Metrics:** Timing prediction efficiency is claimed qualitatively

**Problem:** Timing-library characterization requires many expensive circuit simulations across input slews and loads.

**Workload or benchmark:** Standard-cell timing arcs; libraries, process nodes, labels, and baselines are unspecified.

</details>

<span id="paper-dac-2026-research795"></span>

### GSR-GNN: Training Acceleration and Memory-Saving Framework of Deep GNNs on Circuit Graph

DAC 2026 · Record: `dac-2026-research795`

[Read the step-by-step explanation](#explanation-dac-2026-research795)

**Updated source-backed reading card**

Reviewed 2026-09-08. Reconciles the GSR-GNN card with the captured official source; separates deep-layer activation memory, reversible reconstruction, grouped sparse embeddings and execution-pipeline movement, and bounds the reported memory/speed claims to sampled circuit-graph training.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Deep GNNs can improve structural reach on circuit graphs but incur growing activation memory and training cost.

**Mechanism / artifact:**

GSR-GNN combines reversible residual modules for activation reconstruction, a group-wise sparse nonlinear operator for structured embedding compression, and an optimized execution pipeline intended to reduce fragmented activation storage and data movement.

**Workload — the work tested:**

Deep GNN training on sampled circuit graphs; task identities, graph sizes, layer counts, sampling method, quality metric and complete-design holdout are unspecified.

**Hardware and manufacturing assumptions:**

Graph-learning training system with GPU memory and data-movement constraints; GPU, software stack, allocation, batch, kernel and execution details are unspecified.

**Baseline — the comparison method:**

Shallow GNN architectures

Prior deep-GNN training approaches

Baseline depth, implementation, graph sampling and resource parity are unspecified

**Reported measurements:**

The official description reports up to 87.2% peak-memory reduction and over 30x training speedup with negligible degradation in correlation-based quality metrics; exact values, baselines and measurement boundaries are unspecified.

**Limits on the conclusion:**

Reversible activation reconstruction trades stored memory for recomputation; its net benefit depends on added operations, memory bandwidth and the implementation of the backward pass.

Grouped sparse embeddings reduce useful representation size only if the task metric, sparsity representation and execution path preserve the needed information and realize the storage/traffic reduction.

An optimized training pipeline can improve one graph size, batch or GPU without establishing the same result for full graphs, another implementation or a downstream EDA flow.

The official description supplies no task identities, graph/depth details, hardware, exact metric values or independent execution; memory and training speed claims do not establish unchanged circuit decisions or PPA.

**Source and location**

Evidence tier: Primary captured official DAC description only; no full paper extraction, graph training execution or independent memory/quality/downstream flow validation. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH795&sess=sess177)

DAC 2026 official description and data/review-packets/dac-2026-research795.json: deep circuit-graph GNN memory/training problem; reversible residual modules; group-wise sparse nonlinear operator; optimized activation/data-movement pipeline; sampled-graph 87.2% memory and >30x speed claims.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** standard deep GNN training

shallow circuit-graph GNN

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH795

**Hardware or process assumptions:** GPU/accelerator GNN training stack; graph sizes and precision assumptions are unspecified.

**Limits:** No accuracy, convergence, memory, throughput, or design-transfer results are reported.

Memory reductions may alter long-range graph information.

Official description only; task-diverse validation is required.

**Method or artifact:** Training acceleration and memory-saving framework for circuit-graph GNNs.

**Metrics:** Training efficiency and memory are claimed qualitatively

**Problem:** Deep GNN training on circuit graphs suffers from memory growth and long propagation paths.

**Workload or benchmark:** Circuit graphs and EDA prediction tasks; datasets, hardware, and baselines are unspecified.

</details>

## What remains to establish

Resolve unspecified workloads, comparison methods, resource budgets, and source locations before generalizing a reported gain. Multiple papers in this selected sample permit comparison of mechanisms, but do not by themselves establish recurrence across years or a long-term trend.

[All subthemes](../expanded-taxonomy-v1.md) · [Research directions](../directions/README.md)
