# Accelerator reliability

This subject has 10 records in the selected sample. This page explains where it fits, then presents all captured paper evidence without shortening the measurements or limitations.

[Definitions used in the paper records](../reading-guide-v1.md)

## Understand the parent subject first

- [Power reliability and security](../themes/power-reliability-and-security.md)

## Define failure in terms of useful output

An accelerator performs work for an application. A physical fault matters because it can change an output, delay completion, or stop the device. The consequence depends on where the fault occurs, how long it lasts, and how the application uses the affected value.

A reliability experiment needs both a fault model and a result criterion. The fault model states which errors can occur and how they are introduced or observed. The result criterion states what counts as a correct or acceptable application outcome. Counting faulty components alone does not determine application reliability.

## Different faults require different responses

A transient error changes state temporarily. A persistent defect can repeatedly affect a component. Wear can change the probability of failure as operation continues. Detection, recomputation, replacement, and avoidance address these conditions differently.

Avoiding a known faulty resource may preserve correctness while reducing available parallelism. Repeating an operation may detect disagreement but consume time and energy. Correcting an error requires enough additional information to determine a valid result. The evaluation must charge the work required by the chosen response.

<span id="explanation-dac-2026-research2057"></span>

## AccShield changes where operations execute

AccShield's captured method uses operator sensitivity and dependency information to assign work across reliable and faulty arrays. An operator is one unit of application computation, such as a matrix operation or another stage in a neural-network graph. A multi-array accelerator has several places where an operator could run. Those places are not equivalent: one array may be more reliable than another, and assigning an operator to an array consumes that array's time and capacity.

The proposal therefore treats scheduling as a reliability decision, not only a load-balancing decision. It maps less-sensitive operators to faulty arrays and reserves reliable arrays for critical operations. The [recorded paper evidence](../observed-subthemes/accelerator-reliability.md#paper-dac-2026-research2057) says that the scheduler also respects inter-operator dependencies.

## What operator sensitivity means

An operator is sensitive when an error in its result is likely to cause an unacceptable final result. This cannot be determined from the operator name alone. The effect depends on the values being processed, the later operations that consume the result, whether the model has redundancy, and the output rule used by the application. For classification, a small numerical change may leave the predicted class unchanged in one input and change it in another. The same hardware error can therefore have different application consequences.

To use sensitivity in a scheduler, the system needs a defined measurement or estimate. It must specify the output-quality rule, the inputs used to estimate sensitivity, the fault inserted into the operator, and the unit of sensitivity: numerical error, wrong class, missed deadline, or another criterion. Without these definitions, “insensitive” means only that the source labels an operator that way; it does not establish a measured probability of acceptable output.

## Why dependency information changes the schedule

Operators form a dependency graph. A consumer cannot use a producer's value until the producer has completed and the value has been made visible. Moving one operator to a faulty or slower array can therefore affect later operators even when the moved operator itself is insensitive. The schedule must preserve dependency order, transfer data between arrays when needed, and avoid assigning two operations to the same resource at the same time.

This creates three separate constraints:

1. The selected array must have the required reliability condition.
2. The array must have enough execution capacity at the required time.
3. Every input to the operator must arrive before the operator executes, and every output must remain available to its consumers.

A schedule that satisfies only the first condition can still miss a deadline or create communication and queueing costs. A schedule that balances array occupancy can still place a high-consequence operator on a resource whose fault probability is too high. The useful result must report all three constraints together.

## The comparison that would establish benefit

The natural comparison is not merely “AccShield versus no scheduler.” It needs at least a reliability target, a fault model, and a common performance budget. The baseline might use a single-array fault-tolerance mechanism on a multi-array design, as the captured card states, but the comparison must also say whether both methods have the same number of arrays, reliable resources, recovery options, and available execution time.

For each fault condition, the evaluation should measure final-output failures, output-quality loss, detected faults, recovery or avoidance time, completed work, array utilization, communication traffic, scheduling time, energy, and area or resource cost. If AccShield avoids faulty arrays rather than correcting errors, the loss of usable capacity must be included. If it permits faults in low-sensitivity operators, the application-level quality threshold must be stated. “Improved reliability with minimal performance loss” is not interpretable without these denominators and conditions.

## What the available source establishes and leaves open

The official DAC description establishes the intended mechanism: combine hardware reliability variation, operator-level error sensitivity, and inter-operator dependencies; place less-sensitive work on faulty arrays; reserve reliable arrays for critical work. It does not provide the fault distribution, number and type of arrays, sensitivity calculation, model or operator set, reliability metric, output-quality rule, scheduling overhead, utilization loss, energy result, or numeric baseline comparison.

The available evidence therefore supports a precise research question: can application-level criticality guide multi-array scheduling so that a fixed reliability target is met with less performance or hardware cost than applying the same protection policy uniformly? It does not yet support a numerical reliability improvement, a general claim about AI accelerators, or a conclusion that faulty arrays are safe for all operators or inputs.

<span id="explanation-dac-2026-research2424"></span>

## XRel-Graph distributes protection across layers

XRel-Graph addresses mixed-criticality embedded systems. In such a system, tasks do not all have the same consequence when they fail or miss a deadline. A safety-relevant task may need a stronger guarantee than a task whose result can be delayed or discarded. Fault tolerance therefore has two linked outputs: it must reduce incorrect behavior and it must preserve the timing requirements of the tasks that matter.

The captured source describes a design-time method that selects and distributes fault-tolerance mechanisms across hardware and software layers. A layer is a place where protection can be added, such as hardware detection, a runtime response, or application-level recovery. The source says that XRel-Graph uses machine learning to choose efficient methods across those layers and to reduce the amount of mitigation placed in hardware while meeting real-time and reliability requirements. [Recorded paper evidence](../observed-subthemes/accelerator-reliability.md#paper-dac-2026-research2424)

## Why layer placement changes the cost

Protection at different layers observes different information and pays different costs. Hardware can detect an error close to the failing operation, but hardware protection consumes area, power and timing margin on every execution. Software can use application meaning to decide whether a result is acceptable or can be recomputed, but software recovery adds execution time and may discover the fault later. A cross-layer policy can choose a different response for different tasks, but then the interfaces between layers become part of the correctness mechanism.

For example, a hardware detector may report an error to software. Software then needs a defined status signal, a recovery action, a bound on the recovery time, and a rule for what happens if recovery itself fails. Moving protection out of hardware is not automatically a reduction in total cost: it can move work into software, increase delay variation, or make the timing proof more difficult. The result must count those costs at system level.

## Why mixed criticality changes the objective

An average result can hide a failure in the task with the strongest requirement. A meaningful evaluation must identify each task's criticality, allowed execution time, acceptable output error, and consequence of failure. It must then show that the cross-layer choice preserves the requirement for every relevant task, not only that the average energy or peak power is lower.

The phrase “meeting real-time requirements” also needs a defined timing condition. It could mean average latency, a maximum response time, a deadline-miss probability, or a worst-case bound. These are different claims. A recovery policy that improves average energy while occasionally delaying a critical task does not satisfy a hard deadline requirement.

## What the learning problem must represent

The graph model needs nodes and edges with a clear meaning. Nodes might represent tasks, hardware blocks, software handlers or protection mechanisms. Edges might represent data dependence, timing dependence, shared resources or recovery control flow. The training target must say whether the model selects a mechanism, assigns it to a layer, predicts overhead, or optimizes a combined objective.

The training and validation data must also include the conditions under which a choice remains valid. If the fault distribution, task set, processor load or timing requirement changes, a learned choice may no longer meet the requirement. A training/test split can show predictive performance on the chosen data, but it does not by itself establish reliability under unseen faults or certification-level coverage.

## The comparison that would establish benefit

The comparison should hold the application, hardware, task deadlines, fault exposure and output requirements fixed. It should compare isolated layer-specific mitigation with XRel-Graph's cross-layer allocation and report hardware area, peak power, energy, average and worst-case timing, deadline misses, fault coverage, undetected errors, recovery time and design-time computation.

The evaluation also needs an accounting rule for protection that is not active on every execution. A software recovery path may have low average cost but high tail latency. A hardware detector may add constant cost but provide a bounded response. These cannot be ranked with one average number. The paper must show which requirement each metric represents and whether the same protection coverage is preserved.

## What the available source establishes and leaves open

The official DAC description establishes the intended direction: use graph learning at design time to select application-specific fault-tolerance across multiple hardware/software layers, reduce hardware-layer mitigation overhead, and target real-time and reliability requirements in mixed-criticality systems. It does not provide task definitions, criticality levels, fault probabilities, layer options, graph features, training data, timing bounds, numeric overheads, fault coverage, or validation results.

The evidence therefore supports a precise question: can cross-layer allocation preserve the strongest task-level reliability and timing requirements with lower total cost than applying protection independently at each layer? It does not support a numerical overhead reduction, a general safety claim, or an inference that the learned choice remains valid when task sets, faults, hardware or deadlines change.

<span id="explanation-dac-2026-research2976"></span>

## REPAIR addresses repeated reconfiguration and wear

REPAIR concerns nonvolatile-memory-based FPGAs. An FPGA's configuration stores the choices that determine which logic and connections are active. Partial reconfiguration changes only part of that configuration while the rest of the device continues to exist. In an NVM FPGA, the configuration cells retain their state without power, but each write consumes part of the cell's write endurance and may take longer than an SRAM configuration write.

The reliability problem is therefore cumulative. A single partial reconfiguration may work correctly, while a long sequence of reconfigurations can cause some configuration cells to reach their endurance limit earlier than others. Lifetime depends on the maximum stress on the most heavily written cell, not only on the average number of changed bits. [Recorded paper evidence](../observed-subthemes/accelerator-reliability.md#paper-dac-2026-research2976)

## The three mechanisms operate at different times

REPAIR's first mechanism is lifetime-aware fixed placement during preprocessing. Placement determines which logical functions occupy which physical LUT configuration cells. If the placement is chosen with future reconfiguration behavior in mind, frequently changing functions can be assigned so that writes are spread more evenly or concentrated away from cells that would otherwise become the bottleneck. This decision is made before runtime, so it can affect every later configuration but cannot react to an update pattern that was not represented during placement.

The second mechanism generates differential partial bitstreams. Instead of writing a complete partial configuration, the tool compares consecutive configurations and writes only the changed LUT configuration bits. This can reduce the number of writes when consecutive configurations are similar. It does not imply that every cell receives fewer writes: a small set of bits may still change repeatedly, and the write count alone does not specify how stress is distributed across cells.

The third mechanism schedules LUT updates during the reconfiguration path. Scheduling can control the order or timing of updates and may reduce conflicts or runtime overhead. It cannot restore endurance already consumed by a previous write. A lifetime claim must therefore distinguish fewer physical writes, better distribution of writes, shorter reconfiguration time, and lower scheduler overhead; these are related but different outcomes.

## What a lifetime claim must define

“Operational lifetime” needs an endpoint. It could be the first cell that exceeds its endurance, the first configuration that cannot be loaded, a specified probability of configuration failure, or another device-level condition. The endurance model must state whether all cells have the same limit, whether writes have identical cost, and whether temperature, voltage, retention, or write timing changes that limit.

The update trace is equally important. A policy that performs well for alternating configurations may behave differently for a workload that repeatedly changes one region. The evaluation should report the number of configurations, changed bits per transition, per-cell write distribution, maximum cell stress, reconfiguration latency, and any configuration failures. It should also show that the placed design remains functionally equivalent after each update.

## The comparison that would establish the 7× result

The captured source compares REPAIR with baseline partial reconfiguration using commercial tools and reports at least a 7× extension of operational lifetime. To interpret that factor, the baseline tool and its placement, bitstream generation, update schedule, endurance model, update trace, lifetime endpoint and measurement modality must be held or explicitly compared. A simulated 7× ratio, an accelerated endurance test, and a field lifetime estimate are different kinds of evidence.

The comparison must also account for the cost of preserving performance and flexibility. Placement restrictions can reduce the set of legal mappings. Differential generation adds preprocessing work and may change bitstream storage or transfer cost. Runtime scheduling adds control logic and possibly reconfiguration delay. A useful result reports lifetime together with timing, resource use, bitstream size, update latency and any loss of feasible configurations.

## What the available source establishes and leaves open

The official DAC description establishes the proposed chain: lifetime-aware fixed placement, differential partial-bitstream generation, and a low-overhead runtime scheduler, with a stated at-least-7× operational-lifetime result versus commercial-tool partial reconfiguration. It does not provide the NVM technology, endurance distribution, circuits, update sequences, per-cell stress, lifetime endpoint, physical-versus-modeled measurement, performance overhead, or bitstream details.

The evidence therefore supports a precise question: can placement, changed-bit reduction and update scheduling jointly lower the maximum NVM write stress without breaking the normal CAD flow or runtime performance? It does not support a universal 7× lifetime claim across NVM FPGA technologies, reconfiguration traces, temperatures, endurance models or commercial flows.

<span id="explanation-dac-2026-research1585"></span>

## DFA-DRIVE connects circuit delay faults to driving-task output

DFA-DRIVE starts from a fault that occurs below the application: a circuit path may not settle before the clock samples it. Temperature, voltage droop and device aging can increase that delay. If the sampled value is wrong, the error can enter a neural-network layer and eventually change object detection, drivable-area segmentation or lane-line segmentation. The important question is therefore not only whether a circuit violates timing, but whether that violation changes the driving task's accepted output or deadline.

The paper describes two linked parts. DFA-DRIVE propagates timing failures from circuit-level analysis into multi-task perception. DFA-OPT then remaps work across systolic-array resources using layer-level and application-level thermal sensitivity. The source states that this is evaluated against automotive temperature envelopes called AEC-Q100 Grade 0, −40 °C to 150 °C, and Grade 1, −40 °C to 125 °C. [Recorded evidence](../observed-subthemes/accelerator-reliability.md#paper-dac-2026-research1585)

## Why delay faults become task-level faults

A timing fault is conditional on a path, clock period, voltage, temperature, aging state and input-dependent activity. A larger systolic array may provide more parallel arithmetic, but it can also create longer or more heavily loaded paths and a larger region exposed to thermal stress. The source reports a motivating case in which a 256×256 array loses up to 4% accuracy at 150 °C while a smaller 4×4 array is treated as a high-reliability reference.

That number needs a defined accuracy metric and task denominator. A multi-task model has separate outputs and losses. A change in object detection quality is not interchangeable with a change in lane-line segmentation or drivable-area segmentation. A single combined accuracy value can hide a large degradation in one safety-relevant output. The evaluation must preserve task-specific results and state whether “4%” is a relative percentage or percentage-point change.

## What thermal sensitivity controls

DFA-OPT uses thermal sensitivity to choose where DNN layers execute. A layer with high sensitivity is one for which a temperature-induced timing error produces a large task-level consequence under the defined evaluation. Mapping it to a smaller or more reliable array may reduce the probability of an error, but it can also reduce parallelism and increase the number of computation cycles.

This is a resource allocation problem with a reliability constraint. The mapping must preserve layer dependencies, fit the layer's dimensions, provide enough memory and bandwidth, and finish within the driving system's timing requirement. If the method reports fewer computation cycles, the comparison still needs the same clock, array resources, data movement, thermal state, precision and output-quality target. Fewer cycles are not automatically lower vehicle latency, energy, or risk.

## The comparison that would establish the claim

The baseline should identify the array size and mapping policy used without DFA-OPT. The fault analysis should expose the same temperature, voltage and aging conditions to both mappings and report per-task quality, timing, fault count, missed deadlines, energy, array utilization and remapping cost. If a small array preserves accuracy by doing more work, the extra cycles and any change in thermal behavior must be counted.

The source reports comparable accuracy with up to 92% fewer computation cycles using adaptive mapping. “Comparable” needs a tolerance and a per-task table. “Computation cycles” needs a boundary: accelerator arithmetic only, memory and synchronization included, or complete perception latency. A result can be valid under one boundary and misleading under another.

## What the available source establishes and leaves open

The official DAC description establishes the cross-layer direction: propagate temperature-induced timing failures into three driving-perception tasks, then adapt systolic-array mapping using layer and application thermal sensitivity. It reports the 256×256/150 °C motivating accuracy drop and a qualitative comparable-accuracy result with up to 92% fewer computation cycles. It does not provide the model, data set, timing-fault distribution, voltage and aging conditions, task-specific accuracy, clock and memory assumptions, vehicle-level timing target, energy result, or safety validation.

The evidence supports a precise question: can thermal-aware mapping preserve each required perception task under a defined automotive fault envelope at lower execution cost than a fixed mapping? It does not establish automotive qualification, functional safety, robust operation across vehicles, or a universal interpretation of the 4% and 92% figures.

<span id="explanation-dac-2026-research3059"></span>

## EPAR connects electromagnetic layout to quantum execution

EPAR concerns superconducting quantum processors. A quantum processor is not defined only by its logical circuit and calibrated gate-error table. The physical layout determines where qubits and control structures sit, how electromagnetic fields couple them, and how signals reach each qubit. As the processor grows, those physical interactions can change the behavior of a two-qubit operation even when two edges have similar calibrated error rates.

The captured source describes an electromagnetic-to-architecture framework. It reconstructs how layout distortion changes the effective Hamiltonian, alters mediated connectivity, and affects control-pulse response. It then derives structural scores intended to guide architecture and compilation decisions earlier than a final execution measurement. [Recorded evidence](../observed-subthemes/accelerator-reliability.md#paper-dac-2026-research3059)

## Why a calibrated error rate is not the whole physical explanation

A calibrated two-qubit error rate summarizes behavior observed under a particular calibration and test procedure. It is useful for selecting or ranking operations, but it does not necessarily identify why one edge is more vulnerable than another or how the edge will behave after layout, frequency, pulse, temperature or neighboring-qubit conditions change.

EPAR's proposed structural score adds a physical intermediate layer. Layout geometry affects electromagnetic fields. Those fields affect the effective interaction Hamiltonian and the response to a control pulse. The resulting interaction can change the reliability of a gate or the usefulness of a compiler-selected path. This is a chain of modeled causes; each link must be defined before a score can be treated as a predictor.

The phrase “mediated connectivity” also needs a precise meaning. If an intended interaction travels through another coupling path, the effective connection depends on the physical network and operating conditions. A compiler can use that information to avoid fragile edges or select alternate paths, but doing so may increase circuit depth, routing operations, or calibration work. A more robust edge is not automatically a faster or lower-error program once the routing cost is included.

## What the structural score can and cannot prove

The source reports 100% agreement with two-qubit error trends across tested layouts. Agreement with a trend means the score and the reference change in the same direction under the tested cases. It does not by itself establish absolute error prediction, calibrated probability estimates, or performance on unseen layouts. The sample count, agreement rule, and reference measurement or simulation are not supplied in the available description.

The source also reports more than 10× robustness differences among edges with identical calibrated error rates. This means the score distinguishes edges that the conventional rate treats as equal under the stated condition. It does not mean the processor has obtained a 10× execution speedup, 10× longer lifetime, or a 10× reduction in application failure. The robustness definition, physical units, edge selection, calibration procedure and statistical spread are needed to interpret the factor.

## The compiler-level comparison that would establish value

To show architectural usefulness, the evaluation should run the same quantum workloads with and without EPAR-guided edge or path selection. It should report logical success probability, physical two-qubit error, circuit depth, added routing operations, calibration time, compilation time and the number of usable edges. If EPAR changes the selected layout rather than only the compiler path, the physical design cost and electromagnetic model error must also be included.

The comparison must preserve the error-correction and execution assumptions. A structural score may improve the choice of a physical edge while the full logical circuit remains limited by other gates, measurement errors, readout, leakage or decoder behavior. A local edge ranking cannot be presented as an end-to-end logical reliability result without a circuit-level evaluation.

## What the available source establishes and leaves open

The official DAC description establishes the intended contribution: use physical electromagnetic layout information to derive architecture-level robustness scores by modeling Hamiltonian distortion, mediated connectivity and pulse response. It reports trend agreement on tested layouts and variation among edges with equal calibrated error rates. It does not provide layout count, electromagnetic solver, Hamiltonian parameters, pulse model, measured-versus-simulated reference, compiler experiments, logical circuit results, or physical fabrication validation.

The evidence supports a precise question: can a layout-derived physical score improve compiler and architecture decisions beyond calibrated two-qubit error rates while preserving circuit cost? It does not establish absolute gate-error prediction, unseen-layout generalization, a universal robustness factor, or an end-to-end quantum-application reliability gain.

<span id="explanation-dac-2026-research1664"></span>

## Probabilistic memory makes sampling a memory operation

Probabilistic computation uses random values as part of an algorithm. A Gaussian sample is normally produced by a random-number generator and then moved through the processor and memory hierarchy. For a Bayesian neural network, uncertainty may require many samples or distributions over weights and activations. If the generator produces values much more slowly than the rest of the computation, the processor waits for randomness and the instruction stream spends work moving and transforming samples.

The p-MEM proposal stores distribution parameters in a memory primitive and produces samples at the memory interface. A deterministic value is represented as a distribution with zero variance, so the same primitive is intended to cover both ordinary stored data and sampled data. The source describes a layout-validated simulator that explores device choices, memory specifications and technology nodes, then integrates p-MEM into CPU and GPU systems for BNN workloads. [Recorded evidence](../observed-subthemes/accelerator-reliability.md#paper-dac-2026-research1664)

## What changes when samples are generated in memory

In a conventional path, the system must define a random distribution, generate random bits, transform them into samples, store or forward the samples, and execute the BNN operation. p-MEM moves the sampling step into the memory primitive. That can reduce instructions and data movement, but it also changes the memory's required behavior: it must represent distribution parameters, produce statistically valid samples, provide the required precision, and maintain that behavior across devices, cells, voltage, temperature and time.

The key reliability question is not only whether the memory returns a value. It is whether the returned values have the intended distribution and whether deviations change the BNN's output uncertainty or decision quality. A deterministic memory error and a random-sampling error have different structures. The evaluation must report distribution quality, correlation between samples, repeatability, bias, tails and failure behavior in addition to ordinary read correctness.

## Throughput, latency and energy are different claims

The source reports greater than 1000 GSa/s/mm² GRNG throughput, including memory arrays. This is a sampling-density metric, not a complete BNN throughput result. The denominator is memory-array area, and the source does not establish the peripheral, controller, conversion, interconnect or system-area boundary in the available description.

The integrated CPU/GPU results report instruction-count reductions up to 2.19× and 4.37×, sampling-latency reductions of 562× and 3.45×, and energy reductions of 295.5× and 3.53× for CPU and GPU BNN integration respectively. These are separate platform and metric pairs. They must not be averaged or combined into one universal improvement. Sampling latency can fall substantially while total BNN inference latency remains dominated by matrix operations, memory access, synchronization or repeated samples.

Energy also requires a boundary. A memory-array energy number may exclude host instructions, data transfers, random-bit conditioning, peripheral circuits, cooling and the energy of the BNN operations that consume the samples. The CPU and GPU results must therefore state whether the reported energy covers sampling only or the complete integrated workload.

## What “trustworthy” must mean here

Trustworthiness can refer to several different properties: uncertainty that reflects prediction error, robustness under input or device variation, privacy from randomized computation, or correct operation under memory faults. A probabilistic memory can help one property while harming another. For example, an incorrect variance can make a model appear confident when it is not; a biased random source can make repeated samples insufficiently independent.

The evaluation should define the target distribution and compare generated samples against it using a stated statistical test. It should measure BNN task quality and calibration, not only random-number throughput. It should also show how device variation, retention, read noise, stuck cells, temperature and supply changes affect both the sample distribution and the final decision. Fault correction, retraining, refresh and security assumptions need separate treatment.

## What the available source establishes and leaves open

The captured source establishes the p-MEM mechanism: store distribution parameters and sample at native memory bandwidth, with deterministic data as the zero-variance case. It reports a layout-validated simulator, greater than 1000 GSa/s/mm² GRNG throughput including memory arrays, and platform-integrated CPU/GPU BNN reductions in instruction count, sampling latency and energy under the stated source conditions.

It does not establish fabricated hardware, complete BNN inference speed or energy, statistical sample quality, fault rates, calibration, privacy, uncertainty calibration, device variation, or generalization beyond the explored simulator configurations. The evidence supports a question about reducing the cost of probabilistic data generation; it does not by itself prove trustworthy edge intelligence in deployment.

<span id="explanation-dac-2026-research2245"></span>

## TRAM trains the multiplier and the model together

An exact multiplier returns the mathematical product represented by its input format. An approximate multiplier changes that computation to save circuit power, area, delay, or switching activity. The change introduces an arithmetic error that is then propagated through the neural network. The useful design question is not “how much error can the multiplier tolerate?” in isolation; it is which circuit errors the trained model can tolerate while still meeting a specified task-quality requirement.

TRAM addresses this coupling by jointly optimizing the approximate multiplier structure and the AI model. The source contrasts this with multiplier designs selected without model context. In the joint procedure, the multiplier is a hardware object and the model parameters are a software object; both are changed so that the resulting arithmetic error and model response are evaluated together. [Recorded evidence](../observed-subthemes/accelerator-reliability.md#paper-dac-2026-research2245)

## Why multiplier error is not one number

An approximate multiplier can make different errors for different operand pairs. The error may be biased, input-dependent, sign-dependent, concentrated in low-order bits, or correlated across many operations. A mean absolute error over random operands does not determine the error in a neural layer, because the layer's values have a particular distribution and the same weights and activations are reused many times.

The circuit also has several distinct costs. Dynamic power depends on switching activity; leakage depends on the implementation and operating condition; area and delay depend on the synthesized structure; and the approximation may change the model's output quality. A lower multiplier power number does not prove lower accelerator energy if additional control, larger accumulators, retraining, memory traffic or repeated inference work changes the rest of the system.

## What joint training changes

If only the model is trained, the hardware error pattern is fixed and the model adapts to that pattern. If only the multiplier is optimized, the circuit may reduce power without knowing whether the resulting error is concentrated in an important layer or input region. Joint optimization allows the two choices to respond to one another, but it also creates a larger search problem and a risk of fitting the selected training distribution.

The training protocol must state what is differentiable or approximated, how discrete circuit structures are selected, how synthesis or power estimation feeds back into training, and whether the final model is retrained after the hardware structure is fixed. It must also test an untouched evaluation set. A model that recovers accuracy on training or tuning inputs does not establish generalization to new inputs, models, or hardware operating points.

## The comparison that would establish the power-quality tradeoff

The source reports up to 25.05% AxM power reduction on CNNs with CIFAR-10 compared with state-of-the-art approximate multipliers, and 27.09% power reduction on vision transformers with ImageNet. These are different workload families and should not be combined into one average. The source does not state whether the second value uses exactly the same AxM-only boundary, so the boundary must remain explicit.

The evaluation should report task accuracy or loss before and after approximation, per-layer and per-operand error, synthesized area and delay, multiplier and complete-accelerator power, training cost, inference cost, precision, voltage, process/library, and the comparator structures. The power operating point should be matched. If the model is changed for each multiplier, the baseline must receive an equivalent training or calibration opportunity.

## What the available source establishes and leaves open

The captured DAC description establishes TRAM's core idea: jointly optimize approximate multiplier structures and AI models to reduce power while keeping accuracy loss small. It names CNNs on CIFAR-10 and vision transformers on ImageNet and reports the two power-reduction values above. It does not provide the multiplier topology, training objective, model accuracy, error distribution, power-estimation method, synthesis conditions, complete-accelerator accounting, training overhead, process assumptions or silicon evidence.

The evidence supports a precise question: can model-aware training make a particular approximate multiplier useful at a stated task-quality target while reducing matched hardware power? It does not establish a universal approximation tolerance, full-system energy reduction, silicon reliability, or transfer across models and operating conditions.

<span id="explanation-dac-2026-research2347"></span>

## METRIC protects analog in-memory computation at the layer level

Analog compute-in-memory (CIM) uses physical memory cells and circuits to perform parts of a computation where the stored conductance and applied signals produce an analog result. Device defects and circuit noise can perturb that result. Small perturbations may be tolerated by a neural network, but a large outlier can change a layer output enough to affect later layers or the final prediction.

An error-correcting code (ECC) adds information that lets a system detect or reconstruct a corrupted result. In analog CIM, the correction path must operate on noisy analog values and must fit the array, sensing, conversion and timing budget. METRIC is described in the source packet as MECA-CIM: a Maximum Distance Separable (MDS) analog ECC using two redundancy columns, Hessian-trace sensitivity to allocate protection across layers, and an analog-domain syndrome decoder. [Recorded evidence](../observed-subthemes/accelerator-reliability.md#paper-dac-2026-research2347)

## Why two redundancy columns are not a universal guarantee

“Two redundancy columns” describes a storage or computation layout choice, not a complete correction theorem by itself. Correction capability depends on the code length, symbol definition, redundancy placement, decoder assumptions, and the number and structure of corrupted values. It also depends on whether the analog errors fall within the code's correctable model.

An MDS code is designed to use redundancy efficiently under its mathematical assumptions. An analog crossbar adds non-ideal effects that may violate those assumptions: correlated device variation, drift, saturation, read noise, stuck cells, non-linear conductance, conversion error and a fault that affects several columns together. The evaluation must state which errors are detected, which are corrected, how many symbols can be corrupted, and what happens when the error exceeds coverage.

## Why layer-aware protection changes the allocation problem

Protecting every layer equally can waste redundancy on computations whose errors have little effect while leaving high-sensitivity layers under-protected. METRIC uses Hessian trace as a sensitivity signal. At a high level, a Hessian measures how the loss changes when model parameters or intermediate values are perturbed; its trace summarizes curvature across selected directions. A larger signal can indicate that a perturbation deserves more protection under the paper's defined model.

That signal is not itself a fault probability or a proof of output importance. It depends on the loss, model state, data distribution, perturbation location and approximation used to compute it. Layer allocation must also account for the number of redundancy columns, decoder capacity, latency, energy, area, calibration and the possibility that errors are correlated across layers or time.

## What analog syndrome decoding must establish

The decoder computes a syndrome from the observed analog values and uses it to identify or correct an error. In a digital ECC, the arithmetic is often defined over a discrete symbol set. In analog CIM, the decoder must tolerate measurement noise and determine whether a deviation is a correctable code error or ordinary analog variation.

The evaluation should report the distribution of syndrome values, detection and correction rates, false alarms, residual error after correction, decoder latency, ADC/DAC or comparator use, and behavior under multiple simultaneous defects. It should distinguish a numerical error reduction from exact recovery of the intended analog result. A neural-network output that remains acceptable is not the same as a reconstructed codeword.

## The comparison that would establish the claim

The baseline should have the same array dimensions, precision, workload, fault exposure, technology, sensing path and output-quality target. “Conventional ECC” must identify its code, redundancy, decoder and peripheral cost. The comparison should report area, energy, delay, array utilization, accuracy, residual error, correction coverage and the cost of sensitivity estimation and layer allocation.

AEDP combines area, energy and delay into one product. A lower AEDP does not identify which component improved, and it does not establish that area, energy and delay each fell. The source's “large AEDP reduction” remains qualitative in the available evidence.

## Identity and evidence boundary

The selected record is titled METRIC, while the captured source text calls the framework MECA-CIM. This naming difference must be reconciled against the full paper before treating them as independently named artifacts. The official description establishes the problem, two-redundancy-column MDS approach, Hessian-trace layer allocation and analog syndrome-decoder direction. It does not provide the exact code, correction radius, array size, fault/noise distributions, model results, AEDP values, process conditions or physical measurement.

The evidence supports a precise question: can layer-aware analog ECC use limited redundancy where neural sensitivity is highest while preserving correction coverage and reducing total area-energy-delay cost? It does not establish a universal two-column correction guarantee, robust accuracy across CNNs and Transformers, or a fabricated CIM result.

<span id="explanation-dac-2026-research043"></span>

## Strix treats NPU reliability as a system contract

An NPU is not only an array of multiply-accumulate units. An inference request passes through storage, local memories, instruction and control logic, arithmetic arrays, normalization and nonlinear stages, and software that programs those pieces. A fault in one part can be detected by a local mechanism, can change an intermediate tensor, or can make the final output wrong. The protection needed depends on the fault's location, duration, propagation path, and consequence for the running workload.

Strix is described as a full-stack framework spanning microarchitecture, the instruction-set interface, and programming methods. It re-partitions the NPU along the inference pipeline, identifies dominant failure modes, and attaches targeted safeguards instead of replicating the entire NPU at a coarse granularity. The recovered assessment identifies the comparison as area-matched partial TMR, triple-instruction redundancy, and ReaLM with a rollback limit of one. [Recorded evidence](../observed-subthemes/accelerator-reliability.md#paper-dac-2026-research043)

## Why full replication is expensive and targeted protection is difficult

Replicating an entire NPU can detect disagreement by running redundant copies, but it repeats computation and requires extra storage, interconnect, control, and comparison logic. It also protects every block equally even when some blocks dominate failure risk or when an error in one stage is masked by later computation.

Targeted protection can lower cost by matching a safeguard to a failure mode. The safeguard might detect a corrupted register, check an instruction or tensor, roll back a state, or correct a result. That approach requires a map from fault location to response. A response that works for a transient bit flip may not work for a permanent stuck-at fault. A check that detects an error does not automatically identify the correct value, and rollback requires a valid checkpoint and a bound on repeated failure.

## The recovered fault model and evaluation boundary

The assessment records transient bit flips and permanent stuck-at faults at a default rate of 10⁻⁷, with the rate denominator defined as the original-input bit count. The selected evaluation uses the first 1,000 dataset samples and 10 runs. This makes the result conditional on both the fault model and the sampling budget; it is not a proof over all faults or all inputs.

The recorded platform is Gemmini with an AMD VU19P FPGA and 20 cluster nodes. BF16-I is an exception: the assessment records PyTorch following Spike behavior for LLM performance analysis rather than the same hardware configuration. Mixing that simulated condition with FPGA results would produce an invalid universal hardware conclusion.

## What the measurements mean

The recovered assessment records a 1.04× geometric-mean slowdown, with a 1.02×–1.07× range, under the stated Section 5 conditions. It also records a worst-case detection-latency bound below 1 microsecond at 500 MHz for INT8-D, INT8-I, and FP32-D. The assessment explicitly marks this as a detection bound, not a measured correction-latency bound, and BF16-I is absent from the latency table.

The hardware overhead values are synthesis estimates using Design Compiler 2019.12 and a TSMC 28 nm library. The recorded area/power percentage pairs are 10.2/21.3 for FP32-D, 20.7/23.2 for INT8-D, and 8.7/16.8 for INT8-I. The available evidence does not establish fabricated-silicon measurements, and the pair ordering and exact metric labels must remain tied to the assessment rather than being interpreted as a single generic overhead number.

## Reliability needs an application-level acceptance rule

Fault localization, detection, correction and useful inference are separate outcomes. A system may locate a fault quickly but still spend time recovering. It may detect a wrong value but have no information to reconstruct it. It may correct an internal state while changing the model output for a particular input. The evaluation must state whether success means no silent error, restored tensor values, preserved classification, bounded degradation, or completion before a deadline.

The source's “minimal hardware overhead” and 1.04× slowdown are meaningful only with the same protection coverage and workload as the baselines. An area-matched comparison does not automatically mean equal energy, memory, timing, software effort, or fault coverage. A fault-injection campaign can demonstrate behavior for its sampled faults, but cannot establish safety certification or coverage of every physical fault mode.

## What the evidence establishes and leaves open

The recovered evidence supports Strix as a full-stack, failure-mode-specific reliability design with recorded transient and permanent fault injections, baseline comparisons, a conditional slowdown, a detection-latency boundary, and synthesis-based overhead estimates. It does not establish universal reliability, complete correction latency, fabricated hardware, all-workload behavior, all-precision coverage, or safety certification.

The precise research question is whether pipeline-specific safeguards across NPU hardware, ISA and programming can provide a defined application-level reliability target at lower total cost than monolithic replication, under the same fault model and workload. The current assessment is strong enough to explain that question and its conditions, but not to independently accept the headline reliability claim.

<span id="explanation-dac-2026-research1139"></span>

## BFP changes how a fault propagates through an NPU

Block floating point (BFP) represents a group of values with shared scale information and separate fixed-point mantissas. The shared exponent gives the block a wider usable range than a small fixed-point number, while avoiding a full exponent for every element. This saves hardware work, but it creates a dependency: one exponent participates in the interpretation of many mantissas.

That dependency changes reliability. A bit flip in one mantissa may affect one value or one path. A fault in a shared exponent can rescale many values at once. The final effect also depends on later nonlinear operations, such as activation or normalization, where a small change before a threshold or division can produce a much larger change after it. The source describes pronounced heterogeneous vulnerabilities at bit and path level and reports that a conventional end-to-end check becomes largely ineffective under nonlinear block scaling. [Recorded evidence](../observed-subthemes/accelerator-reliability.md#paper-dac-2026-research1139)

## Why an end-to-end check can miss the important fault

An end-to-end check compares a final output with a reference. It can miss an internal error when later operations mask the difference, and it can make localization difficult when many earlier errors produce similar final deviations. Under BFP, the same final mismatch can originate from a mantissa, a shared exponent, a conversion, a memory path, or a control signal. A final check alone does not identify which component failed or which protection mechanism is needed.

The correct analysis needs at least three levels. At the bit level, it identifies which fields are vulnerable. At the path level, it follows a corrupted value through arithmetic, memory and nonlinear stages. At the application level, it defines whether the final result is wrong, degraded, or late. These levels answer different questions and should not be collapsed into one “reliability” number.

## What the row and column blocking is intended to do

The source describes row/column-wise blocking that decouples fixed-point mantissa computation from the scalar exponent path. The purpose is to keep the two kinds of information separable enough that each can receive a lightweight protection mechanism. Mantissa protection addresses errors in the repeated fixed-point computation; exponent protection addresses the shared scale that can affect many values.

Decoupling is not the same as removing the dependency. The block still needs a correct exponent and a correct association between an exponent and its mantissas. The design must preserve that association through storage, transfer, arithmetic and nonlinear operations. A protection mechanism that detects an exponent error but allows the block to continue with the wrong scale may still produce a large application error.

## Interpreting the reported overhead and reliability

The captured source reports near-dual-modular-redundancy reliability with 3.55% geometric-mean performance overhead and less than 2% hardware cost. “Near-DMR reliability” requires a defined fault population, failure criterion and DMR comparison. It could refer to output-error rate under injected faults, detection coverage, corrected results, or another measure. Those are not interchangeable.

The geometric mean summarizes ratios across the evaluated cases; it does not show the worst case or the distribution of overhead. Hardware cost also needs a boundary: NPU compute arrays, protection logic, memory, control, interconnect, or complete accelerator. A percentage from one boundary cannot be compared with a percentage from another.

## The evaluation needed for a reliable BFP claim

The fault campaign should report transient and permanent fault types, bit and path locations, injection rate and denominator, correlations, workload inputs, BFP block dimensions, exponent/mantissa format, and the number of runs. It should measure detection, correction, silent output error, accuracy or loss, timing impact, energy, area and recovery behavior separately.

The baselines should receive the same fault population and output-quality rule. If the comparison is against dual modular redundancy, the evaluation must state whether DMR duplicates all BFP state and whether Strix-like targeted protection uses the same available area or power budget. A near-DMR output result does not establish identical coverage of physical faults.

## What the available source establishes and leaves open

The official DAC description establishes an RTL-level fault-injection study, bit- and path-level vulnerability analysis, and a BFP NPU microarchitecture using row/column blocking with lightweight mantissa and exponent protection. It reports near-DMR reliability, 3.55% geometric-mean performance overhead, and less than 2% hardware cost.

It does not provide the fault distribution, BFP format, workloads, exact reliability probability, accuracy criterion, technology implementation, area boundary, correction latency, energy, or independent reproduction. The evidence supports the question of whether BFP-specific protection can approach DMR reliability at lower cost; it does not establish a universal reliability guarantee or safety qualification.

## How to measure the combined outcome

Specify fault locations, rates, duration, and any correlations. Preserve the application input distribution and output-quality requirement. Measure incorrect outputs that escape detection, false alarms, recovery time, completion time, and energy with protection enabled.

If a method uses sensitivity estimates, test unfamiliar inputs and models. If it manages aging, evaluate sustained update patterns and changing device conditions. Explain whether faults are measured, injected into hardware, or introduced into a simulation.

The transferable result is a relationship between a stated fault condition, a protection decision, and useful correct work after paying the protection cost. A faster fault-free run or an isolated successful recovery establishes only part of that relationship.

## Compare the results carefully

First identify the inputs and required output quality. Then identify the limited resource: time, memory, communication, energy, circuit area, or correctness coverage. Ask which part of the method reduces that cost and which new cost it adds. Compare numbers only when the experiments hold these conditions sufficiently similar.

A conference description may explain the proposal while omitting the full experiment. An author preprint link may have been coded from its abstract. The source classification does not by itself establish that every table was read. Missing locations remain visible below.

## Complete captured evidence

These are evidence records, not substitutes for the explanations above. Each record preserves its problem, proposed method, measurements, comparison conditions, and source limits. A populated record does not establish that its mechanism has been fully explained or independently verified.

<span id="paper-dac-2026-research2057"></span>

### Accshield: Operator-Aware Robust Scheduling for Fault-Tolerant AI Accelerators

DAC 2026 · Record: `dac-2026-research2057`

[Read the step-by-step explanation](#explanation-dac-2026-research2057)

**Updated source-backed reading card**

Reviewed 2026-09-08. Reconciles the AccShield card with the official DAC description; separates operator sensitivity from a measured reliability probability, dependency-valid scheduling from end-to-end deadline satisfaction, and the qualitative reliability claim from the missing fault and performance conditions.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Multi-systolic-array accelerators can experience more complex fault propagation than single-array systems, while directly applying single-array fault-tolerance mechanisms may add substantial overhead.

**Mechanism / artifact:**

AccShield is described as a reliability-aware scheduler that combines hardware reliability variation, operator-level error sensitivity and inter-operator dependencies. It maps less-sensitive operators to faulty arrays and reserves reliable arrays for critical computations while respecting dependencies.

**Workload — the work tested:**

AI/LLM operators on multi-systolic-array accelerators; the official description does not specify models, operator graph, input distribution, fault injection workload, output-quality rule or deadline target.

**Hardware and manufacturing assumptions:**

A multi-array accelerator with heterogeneous array reliability is assumed. Array count, array capacity, fault locations and rates, process or circuit origin of the reliability variation, recovery mechanism, communication network and scheduling implementation are unspecified.

**Baseline — the comparison method:**

Directly applying single-array fault-tolerance mechanisms to a multi-array architecture

The evaluated comparator and its resource, recovery and reliability conditions are not specified

**Reported measurements:**

The official description claims improved reliability with minimal performance loss, but supplies no numeric reliability, fault coverage, output-quality, throughput, latency, utilization, energy, area or scheduling-overhead value.

**Limits on the conclusion:**

Operator sensitivity is not a universal property: it can vary with input values, model parameters, downstream dependencies and the definition of acceptable output. A label such as insensitive does not establish a probability of correct application output.

Respecting dependency order is not sufficient to prove deadline satisfaction; array contention, inter-array data movement, queueing and resource capacity must also be measured.

Mapping work onto faulty arrays may preserve useful output only under a stated fault model and quality threshold. Avoidance, detection, correction and recovery have different costs and coverage, none of which are specified here.

The official description supports mechanism comprehension and a research question, not a numerical reliability improvement, a general AI-accelerator claim, or independent validation.

**Source and location**

Evidence tier: Primary official DAC description only; no full paper extraction, artifact execution or independent acceptance. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH2057&sess=sess160)

DAC 2026 official description for AccShield's stated problem, reliability-aware scheduling mechanism, operator sensitivity, dependency constraint, faulty/reliable array assignment and qualitative reliability/performance claim; data/review-packets/dac-2026-research2057.json preserves the captured source span and unresolved fields.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** single-array fault-tolerant mechanisms applied to multi-array designs

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH2057&sess=sess160

**Hardware or process assumptions:** Multi-systolic-array accelerator with heterogeneous hardware reliability; array count, fault injection, process, and recovery mechanisms are unspecified.

**Limits:** No fault model, reliability metric, performance overhead, scheduling latency, or workload conditions are supplied.

Operator sensitivity may vary with data and model; mapping around faults may affect utilization and quality.

Official description only; reliability and performance claims require paper-level verification.

**Method or artifact:** Reliability-aware scheduler using operator sensitivity and dependency information to assign work across faulty and reliable arrays.

**Metrics:** Improved reliability claimed qualitatively

Minimal performance loss claimed qualitatively

**Problem:** Faults in multi-systolic-array accelerators propagate through dependencies and can cause more severe degradation than in single-array designs, making direct reuse of fault-tolerance mechanisms costly.

**Workload or benchmark:** Large-model operators on multi-array AI accelerators; fault models, operator set, reliability target, workloads, and performance baseline are unspecified.

</details>

<span id="paper-dac-2026-research2424"></span>

### XRel-Graph: Graph Learning-Driven Cross-Layer Reliability Management in Embedded Mixed-Criticality Systems

DAC 2026 · Record: `dac-2026-research2424`

[Read the step-by-step explanation](#explanation-dac-2026-research2424)

**Updated source-backed reading card**

Reviewed 2026-09-08. Reconciles the XRel-Graph card with the official DAC description; separates cross-layer mechanism selection from demonstrated fault coverage, mixed-criticality requirements from average metrics, and graph-learning validation from safety or real-time acceptance.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Applying fault-tolerance mechanisms independently at separate abstraction layers in mixed-criticality embedded systems can add peak-power, energy and timing overhead while real-time and safety requirements still need to be met.

**Mechanism / artifact:**

XRel-Graph is described as a design-time machine-learning approach that selects and distributes application-specific fault-tolerance mechanisms across hardware and software layers, reducing hardware-layer mitigation while targeting real-time and reliability requirements.

**Workload — the work tested:**

Mixed-criticality real-time embedded applications; task definitions, criticality levels, data/control dependencies, fault distributions, deadlines and output-acceptance rules are not supplied by the official description.

**Hardware and manufacturing assumptions:**

Cross-layer embedded system with multiple hardware/software protection locations. Processor, accelerator, interconnect, fault-injection method, layer options, timing model, power model and recovery interface are unspecified.

**Baseline — the comparison method:**

Isolated layer-specific fault mitigation

The official description does not name a complete evaluated baseline or establish equal protection coverage

**Reported measurements:**

The description claims lower hardware-layer mitigation overhead and says real-time and reliability requirements are met, but supplies no numeric power, energy, timing, deadline-miss, fault-coverage, undetected-error or design-time cost value.

**Limits on the conclusion:**

Moving protection from hardware to software can trade constant hardware cost for recovery delay, tail latency, software complexity or weaker timing bounds. Lower hardware-layer cost is not automatically lower total system cost.

Mixed-criticality acceptance must be checked per task or criticality class. Average energy or latency can conceal a missed deadline or failed safety-relevant task.

Graph-learning accuracy is not the same as reliability acceptance. Nodes, edges, targets, training/test conditions and behavior under changed faults or workloads are unspecified.

The official description supports mechanism comprehension and a bounded research question, not a numerical overhead reduction, functional-safety claim, or generalization to unseen task sets and hardware.

**Source and location**

Evidence tier: Primary official DAC description only; no full paper extraction, artifact execution or independent acceptance. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH2424&sess=sess171)

DAC 2026 official description for the mixed-criticality problem, isolated-layer overhead, design-time cross-layer distribution, machine-learning selection, hardware-layer reduction and real-time/reliability target; data/review-packets/dac-2026-research2424.json preserves the captured source text and unresolved fields.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** isolated layer-specific fault mitigation

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH2424&sess=sess171

**Hardware or process assumptions:** Embedded heterogeneous system with multiple abstraction layers and mixed-criticality timing; processors, accelerators, power model, and fault-injection environment are unspecified.

**Limits:** No reliability probability, timing bound, energy/peak-power value, task set, training data, or ML validation is supplied.

Cross-layer placement may trade implementation complexity, certification effort, and fault coverage.

Official description only; safety and reliability claims require paper-level verification.

**Method or artifact:** Graph-learning-driven design-time selection and distribution of fault-tolerance mechanisms across hardware/software layers.

**Metrics:** Lower hardware-layer mitigation overhead claimed qualitatively

Real-time and reliability requirements claimed met

**Problem:** Layer-isolated fault mitigation in mixed-criticality embedded systems can impose excessive peak-power, energy, and timing overhead.

**Workload or benchmark:** Embedded mixed-criticality applications with real-time and reliability requirements; task sets, fault models, layer options, and objective metrics are unspecified.

</details>

<span id="paper-dac-2026-research2976"></span>

### REPAIR: Reliability Enhancement of NVM FPGAs Through Lifetime-Aware Differential Partial Reconfiguration

DAC 2026 · Record: `dac-2026-research2976`

[Read the step-by-step explanation](#explanation-dac-2026-research2976)

**Updated source-backed reading card**

Reviewed 2026-09-08. Reconciles the REPAIR card with the official DAC description; separates NVM write endurance from reconfiguration latency, changed-bit reduction from per-cell wear distribution, and the reported at-least-7x lifetime factor from the missing device, trace and endpoint conditions.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

NVM FPGA configuration cells have limited write endurance and higher reconfiguration latency; frequent partial reconfiguration can therefore create a long-term reliability bottleneck, especially for LUT configuration cells.

**Mechanism / artifact:**

REPAIR combines lifetime-aware fixed placement during preprocessing, differential partial-bitstream generation that writes changed LUT configuration bits between consecutive configurations, and a low-overhead runtime scheduler for LUT updates in the reconfiguration path.

**Workload — the work tested:**

NVM FPGA partial-reconfiguration workloads; circuits, configuration sequence, number of transitions, changed-bit distribution, update frequency and functional workload are unspecified.

**Hardware and manufacturing assumptions:**

NVM-based FPGA with LUT configuration cells and partial-reconfiguration support. NVM technology, per-cell endurance distribution, write latency, temperature/voltage conditions, commercial CAD flow and physical-versus-modeled evaluation are unspecified.

**Baseline — the comparison method:**

Baseline partial reconfiguration using commercial tools

**Reported measurements:**

The official description reports at least 7× longer operational lifetime versus baseline partial reconfiguration, but does not define the lifetime endpoint, endurance model, trace, measurement modality or denominator conditions.

**Limits on the conclusion:**

Operational lifetime is undefined in the available source: first failed cell, first failed configuration, a probability threshold and a field-life estimate are different endpoints.

Writing only changed bits can reduce total writes without proving lower maximum per-cell stress. Placement and update traces must be evaluated together because lifetime is controlled by the most heavily stressed cells.

Placement restrictions, differential generation and runtime scheduling may add preprocessing, storage, control, reconfiguration-latency or flexibility costs; preserving performance is a claim that needs measurements.

The at-least-7× factor is official-description evidence, not a universal lifetime result across NVM technologies, endurance distributions, temperatures, update traces or commercial flows. No independent execution or hardware endurance test was performed.

**Source and location**

Evidence tier: Primary official DAC description only; no full paper extraction, artifact execution or independent endurance validation. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH2976&sess=sess123)

DAC 2026 official description for NVM write endurance and partial-reconfiguration problem, lifetime-aware placement, differential changed-bit bitstreams, runtime LUT-update scheduling and at-least-7× operational-lifetime claim; data/review-packets/dac-2026-research2976.json preserves the captured source text and unresolved fields.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** commercial-tool partial reconfiguration

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH2976&sess=sess123

**Hardware or process assumptions:** NVM-based FPGA with LUT configuration cells and partial-reconfiguration path; memory technology, CAD flow, controller, and thermal conditions are unspecified.

**Limits:** The description omits endurance cycles, configuration traces, area/timing overhead, bitstream sizes, and baseline tool/version.

Lifetime extension depends on workload reconfiguration patterns and cell-wear model.

Official description only; reliability and CAD-flow compatibility require paper-level verification.

**Method or artifact:** Lifetime-aware placement preprocessing, differential partial-bitstream generation, and runtime LUT-update scheduling.

**Metrics:** At least 7x longer operational lifetime

**Problem:** NVM FPGAs have limited write endurance and high reconfiguration latency, making frequent partial reconfiguration a lifetime bottleneck.

**Workload or benchmark:** NVM FPGA partial-reconfiguration workloads; FPGA technology, configuration sequences, write endurance, performance overhead, and commercial-tool baseline are unspecified.

</details>

<span id="paper-dac-2026-research1585"></span>

### DFA-DRIVE: A Cross-Layer Delay Fault Analysis and Optimization Framework for Robust Multi-Task Driving Perception

DAC 2026 · Record: `dac-2026-research1585`

[Read the step-by-step explanation](#explanation-dac-2026-research1585)

**Updated source-backed reading card**

Reviewed 2026-09-08. Reconciles the DFA-DRIVE card with the official DAC description; separates circuit timing faults from task-level perception failure, thermal sensitivity from static array size, computation cycles from end-to-end latency, and automotive temperature targets from qualification or safety evidence.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Temperature, voltage droop and aging can create delay faults in DNN accelerators; in multi-task autonomous-driving perception, those faults can degrade object detection, drivable-area segmentation and lane-line segmentation.

**Mechanism / artifact:**

DFA-DRIVE propagates circuit-level timing failures into system-level perception tasks. DFA-OPT adaptively remaps DNN layers across systolic-array resources using layer-level and application-level thermal sensitivity.

**Workload — the work tested:**

Multi-task driving perception with object detection, drivable-area segmentation and lane-line segmentation; the official description does not name the model, data set, task metrics, timing target or fault-injection workload.

**Hardware and manufacturing assumptions:**

Systolic arrays including 4×4 and 256×256 examples; temperature targets described as AEC-Q100 Grade 0 (−40 °C to 150 °C) and Grade 1 (−40 °C to 125 °C). Voltage, clock, aging model, process, memory, data movement, thermal transients and qualification status are unspecified.

**Baseline — the comparison method:**

Fixed or large-array mapping implied by the source

Small high-reliability array used as an accuracy reference in the motivating comparison

Exact mapping, resource parity and cycle-count baseline are unspecified

**Reported measurements:**

The source reports up to 4% accuracy drop for a 256×256 array at 150 °C in the motivating case; the task, metric and relative-versus-percentage-point convention are unspecified.

The source reports comparable accuracy with up to 92% fewer computation cycles using adaptive mapping; the tolerance, baseline, cycle boundary and per-task results are unspecified.

**Limits on the conclusion:**

A circuit timing error is not automatically a perception failure; propagation depends on path, clock, voltage, temperature, aging, data activity, neural layer and task-level acceptance rule.

A combined multi-task accuracy number can hide degradation in a safety-relevant output. Each task needs its own metric and requirement.

Fewer computation cycles are not necessarily lower end-to-end latency or energy; memory, synchronization, remapping, clock, thermal response and vehicle-system timing must be included.

AEC-Q100 temperature envelopes are stated targets, not certification evidence. The official description does not establish functional safety, vehicle-level robustness, physical qualification or independent reproduction.

**Source and location**

Evidence tier: Primary official DAC description only; no full paper extraction, simulation execution or independent automotive validation. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH1585&sess=sess137)

DAC 2026 official description for temperature/voltage/aging delay faults, object detection/drivable-area/lane-line tasks, AEC-Q100 Grade 0/1 ranges, 4×4 and 256×256 arrays, 4% motivating accuracy drop and up-to-92% computation-cycle reduction; data/review-packets/dac-2026-research1585.json preserves the captured source text and unresolved fields.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** large fixed systolic-array mapping

baseline accuracy under nominal conditions

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH1585&sess=sess137

**Hardware or process assumptions:** DNN systolic arrays ranging from 4x4 to 256x256 under automotive temperatures of -40C to 150C or 125C; process, thermal model, voltage, frequency, and sensor pipeline are unspecified.

**Limits:** The description omits task-specific accuracy, timing-fault distributions, thermal transients, power/area cost, and comparison mapping details.

Near-baseline accuracy under selected conditions does not establish safety certification or robustness across vehicles and workloads.

Official description only; automotive reliability claims require paper-level fault and thermal validation.

**Method or artifact:** Cross-layer delay-fault propagation analysis and adaptive thermal-sensitivity-aware DNN hardware mapping.

**Metrics:** Up to 4% accuracy drop for 256x256 arrays at 150C

Comparable accuracy with up to 92% fewer computation cycles using adaptive mapping

**Problem:** Temperature, voltage droop, and aging induce delay faults in automotive DNN accelerators, creating task-level perception degradation in safety-critical driving systems.

**Workload or benchmark:** Multi-task driving perception covering detection, drivable-area segmentation, and lane-line segmentation across AEC-Q100 Grade 0 and Grade 1 temperature envelopes; model, fault injection, and baseline mapping details are unspecified.

</details>

<span id="paper-dac-2026-research3059"></span>

### EPAR: Electromagnetic Pathways to Architectural Reliability in Quantum Processors

DAC 2026 · Record: `dac-2026-research3059`

[Read the step-by-step explanation](#explanation-dac-2026-research3059)

**Updated source-backed reading card**

Reviewed 2026-09-08. Reconciles the EPAR card with the official DAC description; separates calibrated two-qubit error rates from layout-derived physical structure, score trend agreement from absolute prediction, and edge robustness factors from end-to-end quantum execution reliability.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

As superconducting quantum processors scale, electromagnetic layout choices can alter qubit interactions and execution robustness, while conventional calibrated error rates may not expose those physical causes.

**Mechanism / artifact:**

EPAR is described as an electromagnetic-to-architecture framework that reconstructs how layout distortion changes the effective Hamiltonian, mediated connectivity and control-pulse response, then derives structural scores for architecture and compiler guidance.

**Workload — the work tested:**

Tested superconducting processor layouts and two-qubit error trends; the official description does not specify layout count, circuits, compiler workloads, operating points or reference-data provenance.

**Hardware and manufacturing assumptions:**

Scaling superconducting quantum processor with electromagnetic layout and control pulses. Qubit geometry, coupling network, electromagnetic solver, Hamiltonian parameters, pulse model, calibration procedure, temperature and measured-versus-simulated status are unspecified.

**Baseline — the comparison method:**

Conventional calibrated two-qubit error rates

The description does not provide a complete compiler or architecture evaluation baseline

**Reported measurements:**

The source reports 100% agreement with two-qubit error trends across tested layouts; sample count, trend definition and agreement rule are unspecified.

The source reports more than 10× robustness differences among edges with identical calibrated error rates; robustness definition, units, edge set and statistical spread are unspecified.

**Limits on the conclusion:**

Trend agreement does not establish absolute gate-error prediction, calibrated probabilities, causality or generalization to unseen layouts.

A robustness difference among edges is not a 10× execution speedup, lifetime extension or application-level reliability gain. Routing and calibration costs may change the circuit-level result.

A local physical score does not establish logical-circuit reliability without accounting for other gates, measurement, leakage, decoder behavior and circuit depth.

The official description supplies no solver, pulse model, compiler experiment, logical-circuit result, fabrication measurement or independent reproduction.

**Source and location**

Evidence tier: Primary official DAC description only; no full paper extraction, electromagnetic simulation execution or independent quantum hardware validation. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH3059&sess=sess135)

DAC 2026 official description for layout-driven Hamiltonian distortion, mediated connectivity, pulse response, structural-score trend agreement and over-10× edge robustness differences; data/review-packets/dac-2026-research3059.json preserves the captured source text and unresolved fields.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** conventional calibrated two-qubit error rates

layout-insensitive reliability metrics

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH3059&sess=sess135

**Hardware or process assumptions:** Superconducting qubits, electromagnetic coupling, control pulses, and physical layouts; process, frequency, packaging, and noise assumptions are unspecified.

**Limits:** The description omits absolute error rates, layout/sample count, calibration drift, solver cost, and experimental validation.

Structural agreement in tested layouts does not establish predictive generalization across devices or packaging.

Official description only; quantum reliability claims require paper-level and hardware validation.

**Method or artifact:** Electromagnetic-to-architecture framework reconstructing Hamiltonian perturbations and compiler-relevant robustness scores early from physical design.

**Metrics:** 100% agreement with two-qubit error trends across tested layouts

Over 10x robustness differences among edges with identical calibrated error rates

**Problem:** Conventional calibrated error rates do not expose how physical electromagnetic layout choices affect execution-level reliability in scaling superconducting processors.

**Workload or benchmark:** Superconducting quantum processor layouts and two-qubit error trends; layout count, calibration protocol, electromagnetic solver, and compiler tasks are unspecified.

</details>

<span id="paper-dac-2026-research1664"></span>

### Probabilistic Memory Design for Efficient Trustworthy Edge Intelligence

DAC 2026 · Record: `dac-2026-research1664`

[Read the step-by-step explanation](#explanation-dac-2026-research1664)

**Updated source-backed reading card**

Reviewed 2026-09-08. Reconciles the probabilistic-memory card with the captured official source text; separates random-sample generation from complete BNN inference, sampling-density from system throughput, CPU/GPU metric pairs from pooled claims, and simulator evidence from fabricated-memory or trustworthiness validation.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Probabilistic edge intelligence can be limited by the throughput and instruction cost of Gaussian random-number generation relative to the computation that consumes the samples.

**Mechanism / artifact:**

p-MEM stores distribution parameters and samples at native memory bandwidth. Deterministic data is represented as the zero-variance special case. The captured source describes a layout-validated simulator that explores device, memory and technology-node choices and integrates p-MEM into CPU/GPU systems for BNN workloads.

**Workload — the work tested:**

BNN workloads integrated with CPU and GPU systems; model identities, task data, sample counts, precision and end-to-end inference boundary are unspecified.

**Hardware and manufacturing assumptions:**

Probabilistic memory array and layout-validated simulator across device/memory/node choices. The captured source does not establish fabricated implementation, peripheral/controller accounting, voltage/temperature conditions, statistical-quality test or fault-correction path.

**Baseline — the comparison method:**

CPU sampling reference

GPU sampling reference

The identities, resource parity and energy boundaries of both references are unspecified

**Reported measurements:**

The source reports greater than 1000 GSa/s/mm² GRNG throughput including memory arrays; node/configuration and area boundary are unspecified.

CPU BNN integration: up to 2.19× instruction-count reduction, 562× sampling-latency reduction and 295.5× energy reduction.

GPU BNN integration: up to 4.37× instruction-count reduction, 3.45× sampling-latency reduction and 3.53× energy reduction. CPU and GPU values are separate conditions and must not be pooled.

**Limits on the conclusion:**

Sampling throughput and sampling latency are not complete BNN inference throughput or latency. Matrix operations, data movement, synchronization and repeated-sample count may dominate end-to-end execution.

Sampling-density, instruction count, latency and energy have different denominators and scopes. The CPU and GPU maxima need not occur at the same configuration or represent the same boundary.

Trustworthy probabilistic memory requires statistical distribution quality, independence/correlation, bias, variance, tail behavior and robustness under device variation; the captured source does not establish these measurements.

Layout-validated simulation is not fabricated-memory evidence. Fault rate, calibration, retention, temperature, supply variation, privacy, uncertainty calibration and deployment cost remain open; no simulator or BNN execution was independently reproduced.

**Source and location**

Evidence tier: Primary captured official DAC description only; no full paper extraction, simulator execution or fabricated memory validation. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH1664&sess=sess123)

DAC 2026 captured official description and source packet data/review-packets/dac-2026-research1664.json: p-MEM distribution-parameter storage and native-bandwidth sampling; zero-variance deterministic case; layout-validated simulator; >1000 GSa/s/mm² including memory arrays; CPU/GPU BNN instruction, sampling-latency and energy factors.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** deterministic memory design

error-corrected edge memory

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH1664

**Hardware or process assumptions:** Probabilistic or approximate memory array for edge inference; process, voltage, and correction assumptions are unspecified.

**Limits:** No error rate, accuracy, energy, area, temperature, or workload results are reported.

Probabilistic behavior may create security or reproducibility risks.

Official description only; measured fault and inference validation is required.

**Method or artifact:** Probabilistic memory design with reliability-aware edge-intelligence operation.

**Metrics:** Trustworthiness and efficiency are claimed qualitatively

**Problem:** Edge memories face variability and faults while needing low energy and trustworthy inference.

**Workload or benchmark:** Edge neural workloads and memory faults; device, error model, and baselines are unspecified.

</details>

<span id="paper-dac-2026-research2245"></span>

### TRAM: Training Approximate Multiplier Structures for Low-Power AI Accelerators

DAC 2026 · Record: `dac-2026-research2245`

[Read the step-by-step explanation](#explanation-dac-2026-research2245)

**Updated source-backed reading card**

Reviewed 2026-09-08. Reconciles the TRAM card with the captured official source text; separates model-aware approximate arithmetic from generic multiplier error, AxM power from complete-accelerator energy, and the two workload-specific power claims from a universal result.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Approximate multipliers can reduce AI-accelerator power, but approximation error can reduce model quality; multiplier structures chosen without model context may miss the useful power/accuracy tradeoff.

**Mechanism / artifact:**

TRAM jointly optimizes approximate multiplier structures and AI models. The source describes this as a model-aware alternative to manual or automatic approximate-multiplier synthesis that does not consider the AI model context.

**Workload — the work tested:**

CNNs on CIFAR-10 and vision transformers on ImageNet; model identities, training protocol, precision, evaluation split and task-quality metric are unspecified.

**Hardware and manufacturing assumptions:**

Synthesized approximate multiplier structures and AI accelerator power evaluation; multiplier topology, circuit library, process, voltage, delay/area conditions, power-estimation method, peripheral accounting and silicon status are unspecified.

**Baseline — the comparison method:**

State-of-the-art approximate multipliers

Manual or automatic multiplier synthesis approaches described as prior context

Exact multiplier and model-training parity are not specified as evaluated baselines

**Reported measurements:**

Up to 25.05% approximate-multiplier power reduction for CNNs on CIFAR-10 versus state-of-the-art AxMs.

27.09% power reduction for vision transformers on ImageNet; the available description does not explicitly establish whether this has the same AxM-only measurement boundary.

**Limits on the conclusion:**

Approximate multiplier error is operand- and layer-dependent; one average arithmetic-error number does not determine neural-network output quality.

Multiplier power is not complete-accelerator energy. Control, accumulation, memory traffic, retraining, precision and repeated inference costs may change the system result.

The two power values are workload-specific maxima/conditions and must not be pooled. Accuracy loss is described as small but not quantified in the captured source.

The official description supplies no circuit topology, training objective, held-out accuracy, error distribution, synthesis conditions, power boundary, training cost, silicon evidence or independent reproduction.

**Source and location**

Evidence tier: Primary captured official DAC description only; no full paper extraction, synthesis/power execution or independent model quality validation. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH2245&sess=sess143)

DAC 2026 captured official description and data/review-packets/dac-2026-research2245.json: joint approximate-multiplier/model optimization; CNN/CIFAR-10 and vision-transformer/ImageNet workloads; 25.05% and 27.09% reported power reductions and their stated comparison context.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** exact multipliers

hand-designed approximate multipliers

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH2245

**Hardware or process assumptions:** Approximate arithmetic accelerator with voltage/process variation; implementation assumptions are unspecified.

**Limits:** No accuracy, power, area, delay, error distribution, or silicon results are reported.

Training may overfit a narrow model set.

Official description only; workload and variation sweeps are required.

**Method or artifact:** Training-based approximate multiplier structure optimization.

**Metrics:** Power-quality tradeoff is claimed qualitatively

**Problem:** AI accelerators spend substantial power in multipliers, while approximation must preserve model quality.

**Workload or benchmark:** AI accelerator multiply workloads; models, circuit library, error budget, and baselines are unspecified.

</details>

<span id="paper-dac-2026-research2347"></span>

### METRIC: An MDS-Analog ECC with Minimum Two-Column Redundancy for Fault-Tolerant, Layer-Aware IMC Architecture

DAC 2026 · Record: `dac-2026-research2347`

[Read the step-by-step explanation](#explanation-dac-2026-research2347)

**Updated source-backed reading card**

Reviewed 2026-09-08. Reconciles the METRIC card with the captured source packet; separates two redundancy columns from a correction guarantee, Hessian-trace sensitivity from fault probability, analog syndrome decoding from exact recovery, and qualitative AEDP reduction from measured system cost. The source title/description naming discrepancy is preserved.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Memristor analog compute-in-memory crossbars suffer device defects and circuit noise; large analog outliers can exceed the small-error tolerance of neural computation and require correction.

**Mechanism / artifact:**

The record title names METRIC, while the captured source text names MECA-CIM: an MDS analog ECC with two redundancy columns, Hessian-trace sensitivity for layer-wise adaptive protection allocation, and an analog-domain syndrome decoder for error detection and correction.

**Workload — the work tested:**

CNNs and Transformers under defects and noise; model identities, array dimensions, fault multiplicity, noise distributions, accuracy metrics and operating conditions are unspecified.

**Hardware and manufacturing assumptions:**

Analog memristor CIM crossbar with two redundancy columns and analog syndrome-decoding path; device technology, conductance model, sensing/conversion circuits, process, voltage, array size, calibration and physical-versus-modeled status are unspecified.

**Baseline — the comparison method:**

Conventional ECC systems

The exact code, redundancy, decoder, resource parity and implementation baseline are unspecified

**Reported measurements:**

Two redundancy columns are stated as the design feature.

Robust outlier resistance across CNNs and Transformers and large AEDP reduction versus conventional ECC are claimed qualitatively; no numeric correction, accuracy, area, energy or delay value is supplied.

**Limits on the conclusion:**

Two redundancy columns do not by themselves define code length, symbol model, correction radius or behavior under correlated, multi-column, drift, saturation, stuck-cell or conversion errors.

Hessian trace is a model/loss/data-dependent sensitivity signal, not a fault probability or universal proof of layer criticality.

Analog syndrome decoding must separate correctable code errors from ordinary analog variation; detection, correction, residual error and acceptable neural output are different outcomes.

METRIC/MECA-CIM naming needs full-paper reconciliation. The official description supplies no exact code, fault/noise distributions, array size, model scores, AEDP values, process conditions or physical validation; no independent execution was performed.

**Source and location**

Evidence tier: Primary captured official DAC description and source packet only; no full paper extraction, analog simulation execution or independent cim validation. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH2347&sess=sess169)

DAC 2026 captured official description and data/review-packets/dac-2026-research2347.json: device-defect/noise problem; MECA-CIM MDS ECC with two redundancy columns; Hessian-trace layer allocation; analog syndrome decoder; CNN/Transformer outlier-resistance and qualitative AEDP claims; title/description naming discrepancy.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** conventional ECC systems for analog CIM

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH2347&sess=sess169

**Hardware or process assumptions:** Memristor crossbar analog CIM with layer-aware redundancy columns and analog syndrome logic; device technology, ADC/peripheral costs, and process conditions are unspecified.

**Limits:** No numeric AEDP, accuracy, fault rate, latency, area, or energy values are provided.

The outlier model, decoder precision, analog noise, and baseline ECC overhead are unspecified.

Official description only; reliability and quality claims require paper-level verification.

**Method or artifact:** Two-column MDS ECC, Hessian-trace layer sensitivity for adaptive protection allocation, and an analog-domain syndrome decoder.

**Metrics:** Large area-energy-delay-product reduction claimed qualitatively

Robust outlier resistance across CNNs and Transformers claimed qualitatively

Two redundancy columns

**Problem:** Memristor analog CIM suffers device defects and circuit noise that create large outliers beyond small-error tolerance.

**Workload or benchmark:** CNN and Transformer analog-CIM workloads with defect/noise outlier injection; models, fault distributions, and accuracy criteria are unspecified.

</details>

<span id="paper-dac-2026-research043"></span>

### Strix: Re-Thinking NPU Reliability from a System Perspective

DAC 2026 · Record: `dac-2026-research043`

[Read the step-by-step explanation](#explanation-dac-2026-research043)

**Updated source-backed reading card**

Reviewed 2026-09-08. Reconciles the Strix card with the recovered arXiv v1 assessment and visual Table 1 check; separates full-stack targeted safeguards from monolithic replication, detection from correction, FPGA/simulation conditions, synthesized overhead from silicon, and fault-injection coverage from safety acceptance.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

DNN and LLM accelerators are increasingly used in safety-relevant settings while technology scaling and model complexity increase fault exposure; monolithic NPU replication can impose high overhead and remain difficult to deploy.

**Mechanism / artifact:**

Strix partitions the NPU along the inference pipeline, identifies dominant failure modes, and attaches targeted safeguards across microarchitecture, ISA and programming. The recovered comparison includes area-matched partial TMR, triple-instruction redundancy and ReaLM with rollback limit one.

**Workload — the work tested:**

DNN and LLM inference on an open-source SoC/NPU; selected assessment conditions use first 1,000 dataset samples and 10 runs, transient bit flips and permanent stuck-at faults at default rate 10⁻⁷ over original-input bit count. BF16-I uses PyTorch following Spike behavior for LLM performance analysis rather than the same FPGA path.

**Hardware and manufacturing assumptions:**

Gemmini base, AMD VU19P FPGA and 20 cluster nodes for the recorded platform; synthesis estimates use Design Compiler 2019.12 and TSMC 28 nm. Recorded latency configurations are INT8-D, INT8-I and FP32-D at 500 MHz; BF16-I is absent from the latency table.

**Baseline — the comparison method:**

Area-matched partial TMR

Triple-instruction redundancy

ReaLM with rollback limit one

**Reported measurements:**

Recorded geometric-mean slowdown is 1.04× with range 1.02×–1.07× under the Section 5 conditions.

Recorded worst-case detection latency is below 1 microsecond at 500 MHz for INT8-D, INT8-I and FP32-D; the assessment explicitly says this is not a measured correction-latency bound and BF16-I is absent.

Synthesis-estimated area/power percentage pairs: FP32-D 10.2/21.3, INT8-D 20.7/23.2 and INT8-I 8.7/16.8, using the recorded Design Compiler/TSMC 28 nm conditions.

**Limits on the conclusion:**

Fault localization, detection, correction and useful inference are different outcomes. A detection-latency bound does not establish correction latency or restored application output.

Transient bit flips and permanent stuck-at faults at the recorded injection rate and denominator do not cover all physical, temporal, correlated or workload-dependent fault modes.

BF16-I LLM analysis uses PyTorch following Spike behavior, while other conditions use Gemmini/FPGA or synthesis paths; these must not be combined into one hardware validation claim.

Synthesis estimates are not fabricated-silicon measurements. Fault-injection coverage does not establish functional-safety certification, universal workload behavior or coverage of every fault model; implementation revisions, figure denominators and variance remain open.

**Source and location**

Evidence tier: Primary arxiv v1 preprint plus page level assessment and table check; no independent execution, silicon validation or safety acceptance. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://arxiv.org/html/2604.10484v1)

Recovered arXiv v1 HTML Section 5 for fault model, platforms, baselines, slowdown, latency and synthesis conditions; visually checked PDF Table 1 page 6 for INT8-D/INT8-I/FP32-D detection-latency rows; saved assessment dac/data/strix-primary-assessment-v1.json and data/review-packets/dac-2026-research043.json preserve the source hash, scope and limits.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** coarse-grained monolithic NPU replication mechanisms

**Evidence locators:** Not established in the captured evidence.

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH043&sess=sess171

**Hardware or process assumptions:** Not established in the captured evidence.

**Limits:** The description does not specify fault model coverage, workload set, reliability guarantee, or exact hardware overhead.

**Method or artifact:** Full-stack reliability framework with pipeline-level fault-mode analysis and targeted safeguards across microarchitecture, ISA, and programming.

**Metrics:** sub-microsecond fault localization, detection, and correction

1.04X slowdown

minimal hardware overhead

**Problem:** Monolithic NPU replication creates prohibitive overhead while failing to provide deployable reliability for increasingly fault-prone accelerators.

**Workload or benchmark:** DNN and LLM inference on an open-source SoC NPU, including safety-oriented fault scenarios.

</details>

#### Additional source assessment

This separately recorded check is dated 2026-09-06. It supplements the original record above and retains its own scope and uncertainty.

[Assessment record](../../dac/data/strix-primary-assessment-v1.json)

[Assessed source](https://arxiv.org/html/2604.10484v1)

**Extraction scope**

Selected HTML experimental prose, Section 5; PDF page 6 Table 1 visually transcribed; Table 2 and Figure 9 visually inspected without numerical extraction

**Identity status**

case_normalized_title_and_all_eleven_authors_match_program

**Conditions**

**Platform:** **Base:** Gemmini

**FPGA:** AMD VU19P

**Cluster nodes:** 20

**Locator:** S5.SS1

**Simulation exception:** **Configuration:** BF16-I

**Method:** PyTorch following Spike behavior

**Use:** LLM performance analysis only

**Locator:** S5.SS1

**Evaluation budget:** **Dataset samples:** first 1000

**Runs:** 10

**Locator:** S5.SS1

**Fault model:** **Types:** transient bit flips

permanent stuck-at

**Default rate:** 1e-07

**Rate denominator:** original-input bit count

**Locator:** S5.SS1

**Baselines:** **Names:** partial TMR

triple instruction redundancy

ReaLM

**Budget:** area-matched

**Realm rollback limit:** 1

**Locator:** S5.SS1

**Slowdown:** **Geometric mean:** 1.04

**Range:** 1.02

1.07

**Unit:** x

**Locator:** S5.SS2 item 1

**Latency:** **Metric:** worst-case detection latency

**Bound microseconds:** 1

**Bound relation:** less_than

**Clock mhz:** 500

**Configurations:** INT8-D

INT8-I

FP32-D

**Locator:** S5.SS2 item 6; PDF Table 1

**Limit:** Not a measured correction-latency bound; BF16-I absent from table.

**Hardware overhead:** **Method:** Design Compiler v2019.12; TSMC 28nm

**Area power percent:** **Int8 d:** 20.7

23.2

**Int8 i:** 8.7

16.8

**Fp32 d:** 10.2

21.3

**Locator:** S5.SS2 item 8

**Interpretation limits**

Synthesis estimates are not fabricated-silicon measurements.

Do not combine FPGA and simulated configurations into universal hardware validation.

Fault-injection coverage does not establish safety certification or coverage of every fault model.

Other figure-level denominators, Strix implementation revisions and variance remain unchecked.

**Headline metric status**

conditioned_author_claims_not_independently_accepted

**Independent review status**

pending

<span id="paper-dac-2026-research1139"></span>

### From Characterization to Microarchitecture: Designing an Elegant and Reliable BFP-Based NPU

DAC 2026 · Record: `dac-2026-research1139`

[Read the step-by-step explanation](#explanation-dac-2026-research1139)

**Updated source-backed reading card**

Reviewed 2026-09-08. Reconciles the BFP-NPU card with the captured official description; explains shared-exponent fault propagation, bit/path/application analysis, row/column decoupling, and the boundary between near-DMR, geometric-mean overhead, hardware-cost claims and a universal reliability guarantee.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

BFP-based NPUs offer dynamic range and hardware efficiency, but shared block scaling creates heterogeneous fault vulnerabilities and can make conventional final-output checks ineffective, which matters for safety-relevant deployment.

**Mechanism / artifact:**

RTL-level bit- and path-level fault-injection study plus a fault-tolerant BFP NPU microarchitecture. Row/column-wise blocking decouples fixed-point mantissa computation from the scalar exponent path, with lightweight protection mechanisms for each.

**Workload — the work tested:**

BFP-based NPU computations under injected bit- and path-level hardware faults; workload identities, BFP dimensions/format, input set, fault distribution and accuracy criterion are unspecified.

**Hardware and manufacturing assumptions:**

BFP NPU microarchitecture and RTL fault injection; technology, process, clock, implementation status, protection area boundary, memory/interconnect conditions and physical-versus-modeled evaluation are unspecified.

**Baseline — the comparison method:**

Conventional end-to-end fault checking

Near-dual-modular-redundancy reliability target

Exact DMR implementation and resource parity are not specified

**Reported measurements:**

The source reports near-DMR reliability, 3.55% geometric-mean performance overhead and less than 2% hardware cost; reliability criterion, geometric-mean cases and hardware-cost boundary are unspecified.

**Limits on the conclusion:**

A shared-exponent fault can rescale many mantissas, while a mantissa fault may affect a narrower path; nonlinear operations can change how either fault appears at the output. One final-output check cannot establish localization or coverage.

Near-DMR reliability is not a defined universal metric without fault population, failure criterion, correction behavior and equal comparison budget.

Geometric-mean performance overhead does not show worst-case overhead, and hardware cost needs an explicit boundary covering protection, memory, control and interconnect.

The official description supplies no fault-injection denominator, BFP format, workload accuracy, exact reliability probability, correction latency, energy, technology implementation or independent reproduction; no safety qualification follows.

**Source and location**

Evidence tier: Primary captured official DAC description only; no full paper extraction, RTL execution or independent hardware/reliability validation. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH1139&sess=sess158)

DAC 2026 official description and data/review-packets/dac-2026-research1139.json: BFP dynamic-range motivation; RTL bit/path fault injection; nonlinear block-scaling limitation; row/column blocking; mantissa/exponent protection; near-DMR, 3.55% geometric-mean overhead and <2% hardware-cost claims.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** high_official_description

**Baselines:** conventional end-to-end fault checking

near-dual-modular-redundancy reliability target

**Evidence locators:** Not established in the captured evidence.

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH1139

**Hardware or process assumptions:** Not established in the captured evidence.

**Limits:** The description does not specify fault-injection distribution, workload accuracy impact, technology implementation, or exact reliability probability.

**Method or artifact:** RTL fault-injection study plus fault-tolerant BFP NPU microarchitecture with row/column blocking and lightweight mantissa/exponent protection.

**Metrics:** 3.55% geometric-mean performance overhead

less than 2% hardware cost

near-DMR reliability

**Problem:** BFP NPU fault behavior is poorly characterized, and conventional end-to-end checks are ineffective when nonlinear block scaling creates heterogeneous vulnerabilities.

**Workload or benchmark:** BFP-based NPU computations under injected bit- and path-level hardware faults.

</details>

## What remains to establish

Resolve unspecified workloads, comparison methods, resource budgets, and source locations before generalizing a reported gain. Multiple papers in this selected sample permit comparison of mechanisms, but do not by themselves establish recurrence across years or a long-term trend.

[All subthemes](../expanded-taxonomy-v1.md) · [Research directions](../directions/README.md)
