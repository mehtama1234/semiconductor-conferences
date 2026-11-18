## Why represent a circuit as a graph?

A graph records objects and their connections. For a circuit task, an object might be a cell, pin, or electrical node. A connection might represent a signal dependency or an electrical relationship. Choosing the representation is already an engineering decision. A graph of logical connectivity does not automatically contain wire geometry, resistance, operating voltage, or input activity.

A graph neural network learns how information about connected objects contributes to a prediction. In a common message-passing formulation, each node combines information from its neighbors. It may use attributes of their connecting edges. It then updates its own representation. Repeating this process allows information to travel farther through the graph. This describes a model family, not the exact implementation of each paper below. [PyTorch Geometric's message-passing documentation](https://pytorch-geometric.readthedocs.io/en/latest/tutorial/create_gnn.html) gives the underlying formulation.

The important question is not merely whether the circuit is graph-shaped. It is whether the chosen objects, connections, features, and computation preserve certain information. This is the information required by the target electrical or design task.

## Cell timing and whole-path timing are different targets

A cell's delay depends on its operating conditions and electrical loading. A path joins multiple timing relationships, so arrival time depends on more than one cell. The remaining time before a required arrival deadline is called slack; negative slack indicates that the modeled requirement is missed. Conventional analysis uses a circuit description, timing libraries, constraints, and wire-related electrical information. [OpenSTA's documentation](https://openroad.readthedocs.io/en/latest/main/src/sta/README.html) identifies these inputs, including Liberty libraries and SPEF parasitics.

<span id="explanation-dac-2026-research1562"></span>

### PG-GNN: reducing cell-library characterization without losing timing conditions

### What cell-library characterization produces

A standard-cell timing library records how a cell responds under specified conditions. For a timing arc, the input transition rate and output load are independent conditions. A slowly changing input is not the same as a heavily loaded output. Process, voltage and temperature (PVT) corners add further conditions. A characterization flow evaluates many combinations with circuit simulation, then stores delay and transition values for use by static-timing analysis.

The cost comes from the number of combinations and the electrical simulation required at each one. Skipping simulations is useful only if the predicted table remains accurate where the timing flow will use it. This includes corners and conditions near a design limit. An average error over easy points can hide a bad value at a rare but critical slew/load/corner combination.

### What PG-GNN changes

PG-GNN uses sparse **anchor PVT corners** as direct simulation points and constructs a physics-consistent reference. It then trains a graph neural network to predict the residual between that reference and the remaining values. Residual learning means the model does not learn the full timing surface from zero. It learns the correction to a chosen baseline. This can reduce the complexity of the learned target. Its validity depends on the reference being appropriate across the unmeasured region.

The method then uses **uncertainty-driven active learning** to select additional points for labeling. Instead of spending the same simulation effort everywhere, it queries points where the model is uncertain. The saved effort depends on how uncertainty is computed and how new labels update the model. It also depends on what stopping rule is used. Finally, it depends on whether uncertainty is calibrated near the worst errors. A point-selection policy can lower the number of labels. It does not guarantee lower total characterization time if model training, data movement, or repeated retraining is substantial.

The official description reports a 98.7% reduction in SPICE effort and 1.67% MAPE for TSMC 16 nm libraries. It also reports 0.74% critical-path delay mismatch on ISCAS'89 benchmarks versus foundry libraries. It does not define the effort denominator, MAPE aggregation, corner coverage, or library cells. It also does not define the train/test split, foundry comparison conditions, or complete timing-flow boundary. “Signoff-level accuracy” is therefore a source claim that requires the missing conditions; it is not established by the description alone. [Source: official DAC description and captured record](https://63dac.conference-program.com/presentation/?id=RESEARCH1562&sess=sess155).

### The evaluation that would establish characterization usefulness

Hold out complete cells, PVT corners, slew/load regions, and circuit designs separately. Report worst-case and percentile delay/slew error, not only MAPE. Count timing-limit violations. Measure simulation count, simulator time, model-training time, active-learning overhead, and total wall-clock effort. Run static timing with the generated library and compare critical-path delay and slack against the same foundry or SPICE reference. The physics reference and active learner need ablations so their separate contributions are visible.

[PG-GNN](../observed-subthemes/graph-learning-for-eda.md#paper-dac-2026-research1562) targets cell-library characterization. The detailed explanation above separates PVT/slew/load conditions, residual prediction, active-learning label cost, mean error and worst-case timing risk. This card is the compact evidence record.

<span id="explanation-dac-2026-research2333"></span>

### PBA-rGAT-Edge: predicting timing quantities is not the same as proving timing

### Start with the timing objects

An **arc** is a local timing relationship. An example is the delay and output transition produced by a cell. This applies when an input transition and output load are known. A **path** is a sequence of arcs connected by the circuit's signal dependencies. A path-based timing result depends on the combination of arcs and the path's start and end conditions. It also depends on constraints and the electrical information used by the timing engine. An arc predictor can be accurate on average while still making a path-level decision wrong near the required timing limit.

Path-Based Analysis (PBA) follows a particular path and can avoid some pessimism introduced by combining independently worst-case local conditions. Graph-Based Analysis (GBA) is generally cheaper because it reuses graph calculations, but its approximation can be conservative. Replacing an expensive analysis with a learned predictor is therefore a decision-risk problem, not only a regression problem. The predictor must preserve the timing ordering and the violations that affect design closure.

### What PBA-rGAT-Edge changes

The source describes a pin-level timing graph in which nodes represent timing points and edges carry timing relationships. PBA-rGAT-Edge predicts arc-level delay and slew using residual edge-aware graph attention, a lightweight fusion stage, and a dual-task output head. The term **edge-aware** means the information carried by a connection can affect the update. This matters because an edge can represent a different timing relationship from another edge attached to the same pins. The **path-based features** provide context beyond the immediate neighborhood. The **residual connections** provide a direct information path across layers. This can help optimization but does not guarantee that the learned representation preserves every timing dependency.

Delay and slew are related but distinct outputs. Delay is the time shift of a signal transition. Slew describes how quickly that transition changes. They influence one another through cell and interconnect behavior. Predicting one well does not establish that the other is well predicted. A dual-task head must be evaluated for both tasks and for their effect on path construction and timing-limit decisions.

The official description reports R² values of 0.965 for slew and 0.997 for delay on million-scale industrial benchmarks. It also says convergence is faster than prior GNN methods, including DeepEdgeGAT. R² measures explained variation under a chosen dataset and aggregation. It is not a worst-case error, a percentage accuracy, a signoff-equivalence result, or proof of correct violation ranking. The description does not identify the designs, process corners, timing labels, or split. It also does not identify the graph-size unit, hardware, convergence measure, or path-level decision results. [Source: official DAC description and captured record](https://63dac.conference-program.com/presentation/?id=RESEARCH2333&sess=sess177).

### The evaluation that would establish timing-flow usefulness

Compare against the same PBA/GBA labeling flow. Report absolute error distributions for delay and slew, especially near setup and hold limits. Measure missed violations, false violations, top-critical-path overlap, and worst negative slack error. Also measure the effect of using predictions in a complete optimization or signoff loop. Hold out complete designs and process corners to test transfer. Report training and inference time separately from the timing-engine time saved. A high R² on arc values is useful only if it leads to safe path-level decisions. These decisions must hold at the boundary that engineers actually use.

[PBA-rGAT-Edge](../observed-subthemes/graph-learning-for-eda.md#paper-dac-2026-research2333) targets timing at arc and path level, incorporating edge information and path context. The detailed explanation above separates arc regression, path composition, delay versus slew, PBA/GBA cost, and timing-limit risk. This card is the compact evidence record.

## Coupled wires need more than logical connectivity

<span id="explanation-dac-2026-research2537"></span>

### Crosstalk timing: the graph must carry electrical coupling, not only connectivity

### What the electrical problem is

When nearby wires switch, their electric fields couple through capacitance. A changing signal on one net can alter the transition of another net. The **aggressor** is the switching source of the disturbance; the **victim** is the net whose transition is affected. These terms describe an electrical relationship, not ownership in the logic design.

An RC network represents resistance and capacitance along wires and through connected structures. Crosstalk timing depends on which nets are adjacent and how strongly they couple. It also depends on the direction and timing of their transitions, their driver strengths, their loads, and the surrounding network. A graph that stores only “cell A connects to cell B” omits the values and conditions that determine the disturbance. A graph model must therefore encode the relevant electrical edges, switching context, and multi-net structure. Otherwise it cannot be expected to predict the reference timing quantity.

### What the graph-prompt method changes

The source describes a dual-level graph prompt architecture. The **node-level prompts** are intended to capture fine-grained coupling effects around individual graph elements. The **subgraph-level prompts** are intended to represent holistic interactions among multiple coupled nets. Prompt learning here means adapting a pretrained graph model with additional learned information or task-conditioning. The official description does not specify the prompt parameters, input features, adaptation budget, or frozen versus trainable components. Those details cannot be inferred from the name.

The two levels correspond to different failure modes. A local prompt may represent a nearby coupling value while missing an interaction that travels through a larger RC structure. A subgraph prompt may represent the larger interaction while losing a local switching condition. The method must be evaluated on both local and multi-net cases. These include cases where the electrically important relationship is not the shortest graph path.

The official description says the method predicts crosstalk timing and consistently outperforms existing methods across benchmark designs. It supplies no absolute error, worst-case slack error, process condition, or benchmark identity. It also supplies no graph construction, prompt-training cost, transfer split, or signoff correlation. The source therefore supports the proposed representation and evaluation direction, not a universal timing or process-transfer result. [Source: official DAC description and captured record](https://63dac.conference-program.com/presentation/?id=RESEARCH2537&sess=sess155).

### The evaluation that would establish usefulness

Use a reference crosstalk analysis with the same RC extraction, process corner, driver/load conditions, and transition scenarios for every method. Report delay and slew error distributions, errors near setup/hold limits, and missed and false violations. Also report critical-net ranking, inference cost, prompt-adaptation cost, and transfer to unseen designs or corners. Ablate node-level prompts and subgraph-level prompts separately. A high average correlation is insufficient if the method misses the small set of coupled nets that determines timing closure.

The [crosstalk timing paper](../observed-subthemes/graph-learning-for-eda.md#paper-dac-2026-research2537) works with aggressor-victim resistance-capacitance networks and a dual-level graph-prompt method. The detailed explanation above separates electrical coupling from logical connectivity, local from multi-net context, and prediction quality from signoff evidence. This card is the compact evidence record.

<span id="explanation-dac-2026-research194"></span>

## TRACE: learning circuit computation requires position, hierarchy, and a defined target

### What it means to compute on a circuit graph

A circuit graph is not merely a list of connected nodes. Its nodes can represent gates, registers, pins, or other circuit objects; its edges can represent signal dependencies. A useful model must preserve enough information to answer the target question. Examples are which signal values depend on which earlier values and where state is stored. Another is how a sequence of operations combines inputs. The graph representation alone does not define the target. The output might be a node label, a signal value, a whole-circuit function, a timing quantity, or a design decision.

### Why ordinary neighborhood aggregation can lose computation order

Many graph models update a node by combining messages from neighboring nodes. If the combination is permutation-invariant, reordering the neighbors produces the same summary. That property is useful when neighbor order has no meaning. It is a problem when two inputs occupy different computational positions. It is also a problem when the same local pieces are combined in different stages. A summary can preserve which neighbors exist. It can still lose the ordered and hierarchical route by which their values affect the output.

TRACE proposes a hierarchical Transformer intended to follow the step-by-step flow of computation. The conceptual claim is that the model's information path should reflect the circuit's computational structure. It should not repeatedly apply a generic, order-insensitive neighborhood reduction. “Hierarchical” must be made concrete in a full paper: the graph levels, the tokens or subgraphs at each level, the direction of information flow, and the way sequential state is represented. The official description names the backbone but does not supply those implementation details.

### What function-shift learning changes

Let the desired circuit behavior be a function (F(x)) of the input (x). A direct learner tries to predict (F) in one step. TRACE instead defines a simpler local approximation (F_0(x)) that assumes input independence. It then trains the model to predict the difference (F(x)-F_0(x)). This is a change in the learning target, not a proof that the difference is always easier to learn. The method can help only if the local approximation captures a useful part of the behavior. The remaining shift must also be represented accurately across the tested graph family.

The two claims must be evaluated separately. The hierarchical backbone concerns how graph structure is represented. Function-shift learning concerns what numerical function the model is asked to predict. An ablation that removes one while retaining the other is necessary to attribute any improvement. The evaluation must also state the target. It may be Boolean behavior, a numerical circuit function, a graph property, or a downstream EDA quantity. “Learning computation” is not itself a metric.

The official description says TRACE is validated on RTL graphs, And-Inverter Graphs, and post-mapping netlists. It qualitatively reports that TRACE outperforms prior architectures. It supplies no target definitions, dataset identities, accuracy values, train/test split, graph sizes, runtime, transfer test, or downstream PPA result. The source therefore supports the proposed representation and objective at a conceptual level, not a verified general-purpose circuit-function learner. [Source: official DAC description and captured record](https://63dac.conference-program.com/presentation/?id=RESEARCH194&sess=sess177).

### The evaluation that would establish the contribution

Use the same circuit families, targets, training budget, graph encoding, and metric for four comparisons. The first is the proposed hierarchy with direct learning. The second is the proposed hierarchy with function-shift learning. The third is a conventional backbone with direct learning. The fourth is a conventional backbone with function-shift learning. Hold out complete designs, not only nodes from designs seen during training. Then report target error, exact or task-specific correctness, and graph size. Also report training and inference cost and failure cases near the decision boundary. If the learned output drives synthesis, timing or optimization, run the complete downstream flow. Compare the final design result against the reference tool. Include harmful predictions and the cost of checking them.

## Learning circuit computation and making training practical

[TRACE](../observed-subthemes/graph-learning-for-eda.md#paper-dac-2026-research194) proposes a hierarchical Transformer and function-shift objective for learning computation on RTL graphs, And-Inverter Graphs, and post-mapping netlists. The detailed explanation above separates graph-structure representation from the learning target. It preserves the missing task, metric, dataset, and generalization conditions. This card is the compact evidence record.

<span id="explanation-dac-2026-research795"></span>

### GSR-GNN: making deep circuit-graph training fit within memory

### The resource problem is created by depth

A graph neural network updates node representations through repeated layers. One layer lets information move a limited distance through the graph. Many layers can expose a node to a larger structural neighborhood. During training, the system usually retains intermediate representations so it can compute gradients later. Suppose the graph has many nodes and the network has many layers. Storing those representations can then dominate memory even when the final model parameters are modest.

Depth also costs time. Each layer may require graph reads, message aggregation, nonlinear transformation, and synchronization. More layers can improve the receptive field. The additional work is useful only if the target task benefits from the extra structural information. A memory reduction that prevents deep training is not equivalent to one that preserves the same depth and task quality.

### What GSR-GNN changes

GSR-GNN combines three mechanisms described in the source. One is **reversible residual modules**. They allow earlier activations to be reconstructed from later values under the method’s mathematical conditions. This reduces the amount that must be stored during backpropagation. Reconstruction itself consumes compute; memory saved by recomputation must therefore be compared with the added operations and runtime.

The **group-wise sparse nonlinear operator** compresses node embeddings by applying a structured sparsifying transformation to groups of values. The source says this reduces representation cost without sacrificing task-relevant information. That phrase needs a measurable definition. The task metric, acceptable degradation, group structure, sparsity pattern, and behavior on different graph sizes must be reported. Sparsity in an embedding is also not automatically a reduction in physical memory traffic. The execution pipeline must be able to store and process the representation in that form.

The **optimized execution pipeline** targets fragmented activation storage and data movement. This is a systems contribution in addition to the model changes. Its benefit depends on allocation behavior, graph layout, batch construction, kernel implementation, and hardware. The three mechanisms should be ablated separately; otherwise a total speedup cannot be assigned to reversibility, sparsity, or execution organization.

The official description reports up to 87.2% peak-memory reduction and over 30× training speedup on sampled circuit graphs. It also reports negligible degradation in correlation-based quality metrics. It does not name the tasks, graph sizes, hardware, depth, baseline implementation, metric values, sampling procedure, or memory/speed measurement boundary. The source therefore supports a training-efficiency proposal and bounded reported claims. It does not support a universal deep-GNN improvement or proof that downstream EDA decisions remain unchanged. [Source: official DAC description and captured record](https://63dac.conference-program.com/presentation/?id=RESEARCH795&sess=sess177).

### The evaluation that would establish practical benefit

Compare models at the same depth, graph, batch, optimizer, training budget, and target quality. Report peak allocated memory, persistent model memory, temporary workspace, graph-storage memory, recomputation operations, training time, throughput, and energy separately. Test shallow and deep baselines, full and sampled graphs, different graph sizes, and complete-design holdouts. If the learned result is used in an EDA flow, measure the final timing, area, power, or correctness outcome. Include the cost of reference analysis.

[GSR-GNN](../observed-subthemes/graph-learning-for-eda.md#paper-dac-2026-research795) addresses training time and memory consumption for deeper graph models. The detailed explanation above separates activation storage, reversible reconstruction, embedding compression, execution movement, and downstream task quality. This card is the compact evidence record.

## Generalization must be tested at the design level

Nearby nodes from the same circuit may be split between training and evaluation. That can leave much of the same structure visible to the model. Success under that split is weaker evidence for use on a new circuit than withholding entire designs. Further tests can withhold a design family, cell library, or fabrication technology. These are different transfer claims and should be reported separately.

The five records motivate graph representations that retain more of the information relevant to the task, while keeping training affordable. They do not establish a shared performance improvement or a historical growth rate. A useful end-to-end study would show prediction quality on unseen designs. It would also show the consequences of using those predictions in a design flow. It would include incorrect decisions and the cost of final reference checks.
