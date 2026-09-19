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
