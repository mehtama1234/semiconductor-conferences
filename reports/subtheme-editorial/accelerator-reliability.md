## Define failure in terms of useful output

An accelerator performs work for an application. A physical fault matters because it can change an output, delay completion, or stop the device. The consequence depends on where the fault occurs, how long it lasts, and how the application uses the affected value.

A reliability experiment needs both a fault model and a result criterion. The fault model states which errors can occur and how they are introduced or observed. The result criterion states what counts as a correct or acceptable application outcome. Counting faulty components alone does not determine application reliability.

## Different faults require different responses

A transient error changes state temporarily. A persistent defect can repeatedly affect a component. Wear can change the probability of failure as operation continues. Detection, recomputation, replacement, and avoidance address these conditions differently.

Avoiding a known faulty resource may preserve correctness while reducing available parallelism. Repeating an operation may detect disagreement but consume time and energy. Correcting an error requires enough additional information to determine a valid result. The evaluation must charge the work required by the chosen response.

<span id="explanation-dac-2026-research2057"></span>

## AccShield changes where operations execute

AccShield's captured method uses operator sensitivity and dependency information to assign work across reliable and faulty arrays. An operator is one unit of application computation, such as a matrix operation or another stage in a neural-network graph. A multi-array accelerator has several places where an operator could run. Those places are not equivalent. One array may be more reliable than another. Assigning an operator to an array consumes that array's time and capacity.

The proposal therefore treats scheduling as a reliability decision, not only a load-balancing decision. It maps less-sensitive operators to faulty arrays and reserves reliable arrays for critical operations. The [recorded paper evidence](../observed-subthemes/accelerator-reliability.md#paper-dac-2026-research2057) says that the scheduler also respects inter-operator dependencies.

## What operator sensitivity means

An operator is sensitive when an error in its result is likely to cause an unacceptable final result. This cannot be determined from the operator name alone. The effect depends on the values being processed and the later operations that consume the result. It also depends on whether the model has redundancy and on the output rule used by the application. For classification, a small numerical change may leave the predicted class unchanged in one input and change it in another. The same hardware error can therefore have different application consequences.

To use sensitivity in a scheduler, the system needs a defined measurement or estimate. It must specify the output-quality rule, the inputs used to estimate sensitivity, and the fault inserted into the operator. It must also specify the unit of sensitivity: numerical error, wrong class, missed deadline, or another criterion. Without these definitions, “insensitive” means only that the source labels an operator that way. It does not establish a measured probability of acceptable output.

## Why dependency information changes the schedule

Operators form a dependency graph. A consumer cannot use a producer's value until the producer has completed and the value has been made visible. Moving one operator to a faulty or slower array can therefore affect later operators. This can happen even when the moved operator itself is insensitive. The schedule must preserve dependency order and transfer data between arrays when needed. It must also avoid assigning two operations to the same resource at the same time.

This creates three separate constraints:

1. The selected array must have the required reliability condition.
2. The array must have enough execution capacity at the required time.
3. Every input to the operator must arrive before the operator executes, and every output must remain available to its consumers.

A schedule that satisfies only the first condition can still miss a deadline or create communication and queueing costs. A schedule that balances array occupancy can still place a high-consequence operator on a resource. That resource's fault probability may be too high. The useful result must report all three constraints together.

## The comparison that would establish benefit

The natural comparison is not merely “AccShield versus no scheduler”. It needs at least a reliability target, a fault model, and a common performance budget. The baseline might use a single-array fault-tolerance mechanism on a multi-array design, as the captured card states. The comparison must also say whether both methods have the same number of arrays and reliable resources. It must also say whether they have the same recovery options and available execution time.

For each fault condition, the evaluation should measure final-output failures, output-quality loss, detected faults, and recovery or avoidance time. It should also measure completed work, array utilization, communication traffic, scheduling time, energy, and area or resource cost. If AccShield avoids faulty arrays rather than correcting errors, the loss of usable capacity must be included. If it permits faults in low-sensitivity operators, the application-level quality threshold must be stated. “Improved reliability with minimal performance loss” is not interpretable without these denominators and conditions.

## What the available source establishes and leaves open

The official DAC description establishes the intended mechanism. The mechanism combines hardware reliability variation, operator-level error sensitivity, and inter-operator dependencies. It places less-sensitive work on faulty arrays. It reserves reliable arrays for critical work. It does not provide the fault distribution, number and type of arrays, sensitivity calculation, and model or operator set. It also does not provide reliability metric, output-quality rule, scheduling overhead, utilization loss, energy result, or numeric baseline comparison.

The available evidence therefore supports a precise research question. Can application-level criticality guide multi-array scheduling so that a fixed reliability target is met? The cost in performance or hardware should be lower than when the same protection policy is applied uniformly. It does not yet support a numerical reliability improvement or a general claim about AI accelerators. It also does not support a conclusion that faulty arrays are safe for all operators or inputs.

<span id="explanation-dac-2026-research2424"></span>

## XRel-Graph distributes protection across layers

XRel-Graph addresses mixed-criticality embedded systems. In such a system, tasks do not all have the same consequence when they fail or miss a deadline. A safety-relevant task may need a stronger guarantee than a task whose result can be delayed or discarded. Fault tolerance therefore has two linked outputs. It must reduce incorrect behavior. It must also preserve the timing requirements of the tasks that matter.

The captured source describes a design-time method that selects and distributes fault-tolerance mechanisms across hardware and software layers. A layer is a place where protection can be added, such as hardware detection, a runtime response, or application-level recovery. The source says that XRel-Graph uses machine learning to choose efficient methods across those layers. It also says it reduces the amount of mitigation placed in hardware while meeting real-time and reliability requirements. [Recorded paper evidence](../observed-subthemes/accelerator-reliability.md#paper-dac-2026-research2424)

## Why layer placement changes the cost

Protection at different layers observes different information and pays different costs. Hardware can detect an error close to the failing operation. Hardware protection consumes area, power and timing margin on every execution. Software can use application meaning to decide whether a result is acceptable or can be recomputed. Software recovery adds execution time and may discover the fault later. A cross-layer policy can choose a different response for different tasks. Then the interfaces between layers become part of the correctness mechanism.

For example, a hardware detector may report an error to software. Software then needs a defined status signal, a recovery action, and a bound on the recovery time. It also needs a rule for what happens if recovery itself fails. Moving protection out of hardware is not automatically a reduction in total cost. It can move work into software, increase delay variation, or make the timing proof more difficult. The result must count those costs at system level.

## Why mixed criticality changes the objective

An average result can hide a failure in the task with the strongest requirement. A meaningful evaluation must identify each task's criticality, allowed execution time, acceptable output error, and consequence of failure. It must then show that the cross-layer choice preserves the requirement for every relevant task. It is not enough to show that the average energy or peak power is lower.

The phrase “meeting real-time requirements” also needs a defined timing condition. It could mean average latency, a maximum response time, a deadline-miss probability, or a worst-case bound. These are different claims. A recovery policy that improves average energy while occasionally delaying a critical task does not satisfy a hard deadline requirement.

## What the learning problem must represent

The graph model needs nodes and edges with a clear meaning. Nodes might represent tasks, hardware blocks, software handlers or protection mechanisms. Edges might represent data dependence, timing dependence, shared resources or recovery control flow. The training target must say whether the model selects a mechanism, or assigns it to a layer. It must also say whether the model predicts overhead, or optimizes a combined objective.

The training and validation data must also include the conditions under which a choice remains valid. If the fault distribution, task set, processor load or timing requirement changes, a learned choice may fail. It may no longer meet the requirement. A training/test split can show predictive performance on the chosen data. It does not by itself establish reliability under unseen faults or certification-level coverage.

## The comparison that would establish benefit

The comparison should hold the application, hardware, task deadlines, fault exposure and output requirements fixed. It should compare isolated layer-specific mitigation with XRel-Graph's cross-layer allocation. It should report hardware area, peak power, energy, average and worst-case timing, and deadline misses. It should also report fault coverage, undetected errors, recovery time and design-time computation.

The evaluation also needs an accounting rule for protection that is not active on every execution. A software recovery path may have low average cost but high tail latency. A hardware detector may add constant cost but provide a bounded response. These cannot be ranked with one average number. The paper must show which requirement each metric represents and whether the same protection coverage is preserved.

## What the available source establishes and leaves open

The official DAC description establishes the intended direction. The direction is to use graph learning at design time to select application-specific fault-tolerance across multiple hardware/software layers. It also aims to reduce hardware-layer mitigation overhead. It targets real-time and reliability requirements in mixed-criticality systems. It does not provide task definitions, criticality levels, fault probabilities, and layer options. It also does not provide graph features, training data, timing bounds, numeric overheads, fault coverage, or validation results.

The evidence therefore supports a precise question. Can cross-layer allocation preserve the strongest task-level reliability and timing requirements? Its total cost should be lower than that of applying protection independently at each layer. It does not support a numerical overhead reduction or a general safety claim. It also does not support an inference that the learned choice remains valid. This holds when task sets, faults, hardware or deadlines change.

<span id="explanation-dac-2026-research2976"></span>

## REPAIR addresses repeated reconfiguration and wear

REPAIR concerns nonvolatile-memory-based FPGAs. An FPGA's configuration stores the choices that determine which logic and connections are active. Partial reconfiguration changes only part of that configuration while the rest of the device continues to exist. In an NVM FPGA, the configuration cells retain their state without power. However, each write consumes part of the cell's write endurance and may take longer than an SRAM configuration write.

The reliability problem is therefore cumulative. A single partial reconfiguration may work correctly. A long sequence of reconfigurations can cause some configuration cells to reach their endurance limit earlier than others. Lifetime depends on the maximum stress on the most heavily written cell. It does not depend only on the average number of changed bits. [Recorded paper evidence](../observed-subthemes/accelerator-reliability.md#paper-dac-2026-research2976)

## The three mechanisms operate at different times

REPAIR's first mechanism is lifetime-aware fixed placement during preprocessing. Placement determines which logical functions occupy which physical LUT configuration cells. If the placement is chosen with future reconfiguration behavior in mind, frequently changing functions can be assigned in two ways. They can be assigned so that writes are spread more evenly. They can also be concentrated away from cells that would otherwise become the bottleneck. This decision is made before runtime, so it can affect every later configuration. It cannot react to an update pattern that was not represented during placement.

The second mechanism generates differential partial bitstreams. Instead of writing a complete partial configuration, the tool compares consecutive configurations and writes only the changed LUT configuration bits. This can reduce the number of writes when consecutive configurations are similar. It does not imply that every cell receives fewer writes. A small set of bits may still change repeatedly. The write count alone does not specify how stress is distributed across cells.

The third mechanism schedules LUT updates during the reconfiguration path. Scheduling can control the order or timing of updates and may reduce conflicts or runtime overhead. It cannot restore endurance already consumed by a previous write. A lifetime claim must therefore distinguish fewer physical writes, better distribution of writes, shorter reconfiguration time, and lower scheduler overhead. These are related but different outcomes.

## What a lifetime claim must define

“Operational lifetime” needs an endpoint. It could be the first cell that exceeds its endurance, or the first configuration that cannot be loaded. It could also be a specified probability of configuration failure, or another device-level condition. The endurance model must state whether all cells have the same limit, and whether writes have identical cost. It must also state whether temperature, voltage, retention, or write timing changes that limit.

The update trace is equally important. A policy that performs well for alternating configurations may behave differently for a workload that repeatedly changes one region. The evaluation should report the number of configurations, changed bits per transition, and per-cell write distribution. It should also report maximum cell stress, reconfiguration latency, and any configuration failures. It should also show that the placed design remains functionally equivalent after each update.

## The comparison that would establish the 7× result

The captured source compares REPAIR with baseline partial reconfiguration using commercial tools. It reports at least a 7× extension of operational lifetime. To interpret that factor, several items must be held or explicitly compared. These are the baseline tool and its placement, bitstream generation, update schedule, and endurance model. They also include the update trace, lifetime endpoint and measurement modality. A simulated 7× ratio, an accelerated endurance test, and a field lifetime estimate are different kinds of evidence.

The comparison must also account for the cost of preserving performance and flexibility. Placement restrictions can reduce the set of legal mappings. Differential generation adds preprocessing work and may change bitstream storage or transfer cost. Runtime scheduling adds control logic and possibly reconfiguration delay. A useful result reports lifetime together with timing, resource use, bitstream size, update latency and any loss of feasible configurations.

## What the available source establishes and leaves open

The official DAC description establishes the proposed chain. The chain has lifetime-aware fixed placement, differential partial-bitstream generation, and a low-overhead runtime scheduler. It states an at-least-7× operational-lifetime result versus commercial-tool partial reconfiguration. It does not provide the NVM technology, endurance distribution, circuits, update sequences, and per-cell stress. It also does not provide lifetime endpoint, physical-versus-modeled measurement, performance overhead, or bitstream details.

The evidence therefore supports a precise question. Can placement, changed-bit reduction and update scheduling jointly lower the maximum NVM write stress? This should happen without breaking the normal CAD flow or runtime performance. It does not support a universal 7× lifetime claim. This covers NVM FPGA technologies, reconfiguration traces, temperatures, endurance models and commercial flows.

<span id="explanation-dac-2026-research1585"></span>

## DFA-DRIVE connects circuit delay faults to driving-task output

DFA-DRIVE starts from a fault that occurs below the application. A circuit path may not settle before the clock samples it. Temperature, voltage droop and device aging can increase that delay. If the sampled value is wrong, the error can enter a neural-network layer. It can eventually change object detection, drivable-area segmentation or lane-line segmentation. The important question is therefore not only whether a circuit violates timing. It is whether that violation changes the driving task's accepted output or deadline.

The paper describes two linked parts. DFA-DRIVE propagates timing failures from circuit-level analysis into multi-task perception. DFA-OPT then remaps work across systolic-array resources using layer-level and application-level thermal sensitivity. The source states that this is evaluated against automotive temperature envelopes. They are called AEC-Q100 Grade 0, −40 °C to 150 °C, and Grade 1, −40 °C to 125 °C. [Recorded evidence](../observed-subthemes/accelerator-reliability.md#paper-dac-2026-research1585)

## Why delay faults become task-level faults

A timing fault is conditional on a path, clock period, voltage, temperature, aging state and input-dependent activity. A larger systolic array may provide more parallel arithmetic. It can also create longer or more heavily loaded paths and a larger region exposed to thermal stress. The source reports a motivating case. A 256×256 array loses up to 4% accuracy at 150 °C. A smaller 4×4 array is treated as a high-reliability reference.

That number needs a defined accuracy metric and task denominator. A multi-task model has separate outputs and losses. A change in object detection quality is not interchangeable with a change in lane-line segmentation or drivable-area segmentation. A single combined accuracy value can hide a large degradation in one safety-relevant output. The evaluation must preserve task-specific results and state whether “4%” is a relative percentage or percentage-point change.

## What thermal sensitivity controls

DFA-OPT uses thermal sensitivity to choose where DNN layers execute. A layer with high sensitivity is one for which a temperature-induced timing error produces a large task-level consequence. This is judged under the defined evaluation. Mapping it to a smaller or more reliable array may reduce the probability of an error. It can also reduce parallelism and increase the number of computation cycles.

This is a resource allocation problem with a reliability constraint. The mapping must preserve layer dependencies and fit the layer's dimensions. It must provide enough memory and bandwidth. It must finish within the driving system's timing requirement. If the method reports fewer computation cycles, the comparison still needs several things held the same. These are the clock, array resources, data movement, thermal state, precision and output-quality target. Fewer cycles are not automatically lower vehicle latency, energy, or risk.

## The comparison that would establish the claim

The baseline should identify the array size and mapping policy used without DFA-OPT. The fault analysis should expose the same temperature, voltage and aging conditions to both mappings. It should report per-task quality, timing, fault count, and missed deadlines. It should also report energy, array utilization and remapping cost. If a small array preserves accuracy by doing more work, the extra cycles must be counted. Any change in thermal behavior must be counted too.

The source reports comparable accuracy with up to 92% fewer computation cycles using adaptive mapping. “Comparable” needs a tolerance and a per-task table. “Computation cycles” needs a boundary: accelerator arithmetic only, memory and synchronization included, or complete perception latency. A result can be valid under one boundary and misleading under another.

## What the available source establishes and leaves open

The official DAC description establishes the cross-layer direction. It propagates temperature-induced timing failures into three driving-perception tasks. It then adapts systolic-array mapping using layer and application thermal sensitivity. It reports the 256×256/150 °C motivating accuracy drop and a qualitative comparable-accuracy result with up to 92% fewer computation cycles. It does not provide the model, data set, timing-fault distribution, and voltage and aging conditions. It also does not provide task-specific accuracy, clock and memory assumptions, vehicle-level timing target, energy result, or safety validation.

The evidence supports a precise question. Can thermal-aware mapping preserve each required perception task under a defined automotive fault envelope? Its execution cost should be lower than that of a fixed mapping. It does not establish automotive qualification, functional safety, or robust operation across vehicles. It also does not establish a universal interpretation of the 4% and 92% figures.

<span id="explanation-dac-2026-research3059"></span>

## EPAR connects electromagnetic layout to quantum execution

EPAR concerns superconducting quantum processors. A quantum processor is not defined only by its logical circuit and calibrated gate-error table. The physical layout determines where qubits and control structures sit. It also determines how electromagnetic fields couple them, and how signals reach each qubit. As the processor grows, those physical interactions can change the behavior of a two-qubit operation. This can happen even when two edges have similar calibrated error rates.

The captured source describes an electromagnetic-to-architecture framework. It reconstructs how layout distortion changes the effective Hamiltonian, alters mediated connectivity, and affects control-pulse response. It then derives structural scores intended to guide architecture and compilation decisions earlier than a final execution measurement. [Recorded evidence](../observed-subthemes/accelerator-reliability.md#paper-dac-2026-research3059)

## Why a calibrated error rate is not the whole physical explanation

A calibrated two-qubit error rate summarizes behavior observed under a particular calibration and test procedure. It is useful for selecting or ranking operations. It does not necessarily identify why one edge is more vulnerable than another. It also does not identify how the edge will behave after layout, frequency, pulse, temperature or neighboring-qubit conditions change.

EPAR's proposed structural score adds a physical intermediate layer. Layout geometry affects electromagnetic fields. Those fields affect the effective interaction Hamiltonian and the response to a control pulse. The resulting interaction can change the reliability of a gate or the usefulness of a compiler-selected path. This is a chain of modeled causes. Each link must be defined before a score can be treated as a predictor.

The phrase “mediated connectivity” also needs a precise meaning. If an intended interaction travels through another coupling path, the effective connection depends on the physical network and operating conditions. A compiler can use that information to avoid fragile edges or select alternate paths. Doing so may increase circuit depth, routing operations, or calibration work. A more robust edge is not automatically a faster or lower-error program once the routing cost is included.

## What the structural score can and cannot prove

The source reports 100% agreement with two-qubit error trends across tested layouts. Agreement with a trend means the score and the reference change in the same direction under the tested cases. It does not by itself establish absolute error prediction, calibrated probability estimates, or performance on unseen layouts. The sample count, agreement rule, and reference measurement or simulation are not supplied in the available description.

The source also reports more than 10× robustness differences among edges with identical calibrated error rates. This means the score distinguishes edges that the conventional rate treats as equal under the stated condition. It does not mean the processor has obtained a 10× execution speedup. It also does not mean it has obtained 10× longer lifetime, or a 10× reduction in application failure. The robustness definition, physical units, edge selection, calibration procedure and statistical spread are needed to interpret the factor.

## The compiler-level comparison that would establish value

To show architectural usefulness, the evaluation should run the same quantum workloads with and without EPAR-guided edge or path selection. It should report logical success probability, physical two-qubit error, circuit depth, and added routing operations. It should also report calibration time, compilation time and the number of usable edges. If EPAR changes the selected layout rather than only the compiler path, the physical design cost must also be included. The electromagnetic model error must be included too.

The comparison must preserve the error-correction and execution assumptions. A structural score may improve the choice of a physical edge. The full logical circuit can still be limited by other gates, measurement errors, readout, leakage or decoder behavior. A local edge ranking cannot be presented as an end-to-end logical reliability result without a circuit-level evaluation.

## What the available source establishes and leaves open

The official DAC description establishes the intended contribution. The contribution is to use physical electromagnetic layout information to derive architecture-level robustness scores. It does so by modeling Hamiltonian distortion, mediated connectivity and pulse response. It reports trend agreement on tested layouts and variation among edges with equal calibrated error rates. It does not provide layout count, electromagnetic solver, Hamiltonian parameters, and pulse model. It also does not provide measured-versus-simulated reference, compiler experiments, logical circuit results, or physical fabrication validation.

The evidence supports a precise question. Can a layout-derived physical score improve compiler and architecture decisions beyond calibrated two-qubit error rates? Circuit cost should be preserved. It does not establish absolute gate-error prediction, unseen-layout generalization, a universal robustness factor, or an end-to-end quantum-application reliability gain.

<span id="explanation-dac-2026-research1664"></span>

## Probabilistic memory makes sampling a memory operation

Probabilistic computation uses random values as part of an algorithm. A Gaussian sample is normally produced by a random-number generator and then moved through the processor and memory hierarchy. For a Bayesian neural network, uncertainty may require many samples or distributions over weights and activations. If the generator produces values much more slowly than the rest of the computation, the processor waits for randomness. The instruction stream then spends work moving and transforming samples.

The p-MEM proposal stores distribution parameters in a memory primitive and produces samples at the memory interface. A deterministic value is represented as a distribution with zero variance. The same primitive is therefore intended to cover both ordinary stored data and sampled data. The source describes a layout-validated simulator that explores device choices, memory specifications and technology nodes. It then integrates p-MEM into CPU and GPU systems for BNN workloads. [Recorded evidence](../observed-subthemes/accelerator-reliability.md#paper-dac-2026-research1664)

## What changes when samples are generated in memory

In a conventional path, the system must define a random distribution, generate random bits, and transform them into samples. It must also store or forward the samples, and execute the BNN operation. Here p-MEM moves the sampling step into the memory primitive. That can reduce instructions and data movement. It also changes the memory's required behavior. The memory must represent distribution parameters, produce statistically valid samples, and provide the required precision. It must maintain that behavior across devices, cells, voltage, temperature and time.

The key reliability question is not only whether the memory returns a value. It is whether the returned values have the intended distribution. It is also whether deviations change the BNN's output uncertainty or decision quality. A deterministic memory error and a random-sampling error have different structures. The evaluation must report distribution quality, correlation between samples, repeatability, bias, tails and failure behavior. It must report these in addition to ordinary read correctness.

## Throughput, latency and energy are different claims

The source reports greater than 1000 GSa/s/mm² GRNG throughput, including memory arrays. This is a sampling-density metric, not a complete BNN throughput result. The denominator is memory-array area. The source does not establish the peripheral, controller, conversion, interconnect or system-area boundary in the available description.

The integrated CPU/GPU results report instruction-count reductions up to 2.19× and 4.37×. They report sampling-latency reductions of 562× and 3.45×. They report energy reductions of 295.5× and 3.53×. These are for CPU and GPU BNN integration respectively. These are separate platform and metric pairs. They must not be averaged or combined into one universal improvement. Sampling latency can fall substantially. Total BNN inference latency can still remain dominated by matrix operations, memory access, synchronization or repeated samples.

Energy also requires a boundary. A memory-array energy number may exclude host instructions, data transfers, random-bit conditioning, and peripheral circuits. It may also exclude cooling and the energy of the BNN operations that consume the samples. The CPU and GPU results must therefore state whether the reported energy covers sampling only or the complete integrated workload.

## What “trustworthy” must mean here

Trustworthiness can refer to several different properties. One is uncertainty that reflects prediction error. Others are robustness under input or device variation, privacy from randomized computation, or correct operation under memory faults. A probabilistic memory can help one property while harming another. For example, an incorrect variance can make a model appear confident when it is not. A biased random source can make repeated samples insufficiently independent.

The evaluation should define the target distribution and compare generated samples against it using a stated statistical test. It should measure BNN task quality and calibration, not only random-number throughput. It should also show how device variation, retention, read noise, stuck cells, temperature and supply changes affect the sample distribution. It should show their effect on the final decision as well. Fault correction, retraining, refresh and security assumptions need separate treatment.

## What the available source establishes and leaves open

The captured source establishes the p-MEM mechanism. The mechanism is to store distribution parameters and sample at native memory bandwidth. Deterministic data is the zero-variance case. It reports a layout-validated simulator. It reports greater than 1000 GSa/s/mm² GRNG throughput including memory arrays. It reports platform-integrated CPU/GPU BNN reductions in instruction count, sampling latency and energy under the stated source conditions.

It does not establish fabricated hardware, complete BNN inference speed or energy, or statistical sample quality. It also does not establish fault rates, calibration, privacy, uncertainty calibration, device variation, or generalization beyond the explored simulator configurations. The evidence supports a question about reducing the cost of probabilistic data generation. It does not by itself prove trustworthy edge intelligence in deployment.

<span id="explanation-dac-2026-research2245"></span>

## TRAM trains the multiplier and the model together

An exact multiplier returns the mathematical product represented by its input format. An approximate multiplier changes that computation to save circuit power, area, delay, or switching activity. The change introduces an arithmetic error that is then propagated through the neural network. The useful design question is not “how much error can the multiplier tolerate?” in isolation. It is which circuit errors the trained model can tolerate while still meeting a specified task-quality requirement.

TRAM addresses this coupling by jointly optimizing the approximate multiplier structure and the AI model. The source contrasts this with multiplier designs selected without model context. In the joint procedure, the multiplier is a hardware object and the model parameters are a software object. Both are changed so that the resulting arithmetic error and model response are evaluated together. [Recorded evidence](../observed-subthemes/accelerator-reliability.md#paper-dac-2026-research2245)

## Why multiplier error is not one number

An approximate multiplier can make different errors for different operand pairs. The error may be biased, input-dependent, sign-dependent, concentrated in low-order bits, or correlated across many operations. A mean absolute error over random operands does not determine the error in a neural layer. The layer's values have a particular distribution, and the same weights and activations are reused many times.

The circuit also has several distinct costs. Dynamic power depends on switching activity. Leakage depends on the implementation and operating condition. Area and delay depend on the synthesized structure. The approximation may also change the model's output quality. A lower multiplier power number does not prove lower accelerator energy. Additional control, larger accumulators, retraining, memory traffic or repeated inference work may change the rest of the system.

## What joint training changes

If only the model is trained, the hardware error pattern is fixed and the model adapts to that pattern. If only the multiplier is optimized, the circuit may reduce power. It does so without knowing whether the resulting error is concentrated in an important layer or input region. Joint optimization allows the two choices to respond to one another. It also creates a larger search problem and a risk of fitting the selected training distribution.

The training protocol must state what is differentiable or approximated, and how discrete circuit structures are selected. It must also state how synthesis or power estimation feeds back into training. It must state whether the final model is retrained after the hardware structure is fixed. It must also test an untouched evaluation set. A model that recovers accuracy on training or tuning inputs does not establish generalization. This holds for new inputs, models, or hardware operating points.

## The comparison that would establish the power-quality tradeoff

The source reports up to 25.05% AxM power reduction on CNNs with CIFAR-10 compared with state-of-the-art approximate multipliers. It reports 27.09% power reduction on vision transformers with ImageNet. These are different workload families and should not be combined into one average. The source does not state whether the second value uses exactly the same AxM-only boundary. The boundary must therefore remain explicit.

The evaluation should report task accuracy or loss before and after approximation, and per-layer and per-operand error. It should also report synthesized area and delay, and multiplier and complete-accelerator power. It should report training cost, inference cost, precision, voltage, process/library, and the comparator structures. The power operating point should be matched. If the model is changed for each multiplier, the baseline must receive an equivalent training or calibration opportunity.

## What the available source establishes and leaves open

The captured DAC description establishes TRAM's core idea. The idea is to jointly optimize approximate multiplier structures and AI models. This reduces power while keeping accuracy loss small. It names CNNs on CIFAR-10 and vision transformers on ImageNet and reports the two power-reduction values above. It does not provide the multiplier topology, training objective, model accuracy, and error distribution. It also does not provide power-estimation method, synthesis conditions, complete-accelerator accounting, training overhead, process assumptions or silicon evidence.

The evidence supports a precise question. Can model-aware training make a particular approximate multiplier useful at a stated task-quality target? Matched hardware power should also be reduced. It does not establish a universal approximation tolerance, full-system energy reduction, silicon reliability, or transfer across models and operating conditions.

<span id="explanation-dac-2026-research2347"></span>

## METRIC protects analog in-memory computation at the layer level

Analog compute-in-memory (CIM) uses physical memory cells and circuits to perform parts of a computation. The stored conductance and applied signals produce an analog result. Device defects and circuit noise can perturb that result. A neural network may tolerate small perturbations. A large outlier can change a layer output enough to affect later layers or the final prediction.

An error-correcting code (ECC) adds information that lets a system detect or reconstruct a corrupted result. In analog CIM, the correction path must operate on noisy analog values. It must also fit the array, sensing, conversion and timing budget. METRIC is described in the source packet as MECA-CIM. It is a Maximum Distance Separable (MDS) analog ECC using two redundancy columns. It uses Hessian-trace sensitivity to allocate protection across layers. It also uses an analog-domain syndrome decoder. [Recorded evidence](../observed-subthemes/accelerator-reliability.md#paper-dac-2026-research2347)

## Why two redundancy columns are not a universal guarantee

“Two redundancy columns” describes a storage or computation layout choice, not a complete correction theorem by itself. Correction capability depends on the code length, symbol definition, redundancy placement, and decoder assumptions. It also depends on the number and structure of corrupted values. It also depends on whether the analog errors fall within the code's correctable model.

An MDS code is designed to use redundancy efficiently under its mathematical assumptions. An analog crossbar adds non-ideal effects that may violate those assumptions. These include correlated device variation, drift, saturation, read noise, stuck cells, and non-linear conductance. They also include conversion error and a fault that affects several columns together. The evaluation must state which errors are detected and which are corrected. It must state how many symbols can be corrupted. It must also state what happens when the error exceeds coverage.

## Why layer-aware protection changes the allocation problem

Protecting every layer equally can waste redundancy on computations whose errors have little effect while leaving high-sensitivity layers under-protected. METRIC uses Hessian trace as a sensitivity signal. At a high level, a Hessian measures how the loss changes when model parameters or intermediate values are perturbed. Its trace summarizes curvature across selected directions. A larger signal can indicate that a perturbation deserves more protection under the paper's defined model.

That signal is not itself a fault probability or a proof of output importance. It depends on the loss, model state, data distribution, perturbation location and approximation used to compute it. Layer allocation must also account for the number of redundancy columns, decoder capacity, latency, and energy. It must account for area and calibration. It must also account for the possibility that errors are correlated across layers or time.

## What analog syndrome decoding must establish

The decoder computes a syndrome from the observed analog values and uses it to identify or correct an error. In a digital ECC, the arithmetic is often defined over a discrete symbol set. In analog CIM, the decoder must tolerate measurement noise. It must also determine whether a deviation is a correctable code error or ordinary analog variation.

The evaluation should report the distribution of syndrome values, detection and correction rates, false alarms, and residual error after correction. It should also report decoder latency, ADC/DAC or comparator use, and behavior under multiple simultaneous defects. It should distinguish a numerical error reduction from exact recovery of the intended analog result. A neural-network output that remains acceptable is not the same as a reconstructed codeword.

## The comparison that would establish the claim

The baseline should have the same array dimensions, precision, workload, fault exposure, technology, sensing path and output-quality target. “Conventional ECC” must identify its code, redundancy, decoder and peripheral cost. The comparison should report area, energy, delay, array utilization, accuracy, and residual error. It should also report correction coverage and the cost of sensitivity estimation and layer allocation.

AEDP combines area, energy and delay into one product. A lower AEDP does not identify which component improved. It also does not establish that area, energy and delay each fell. The source's “large AEDP reduction” remains qualitative in the available evidence.

## Identity and evidence boundary

The selected record is titled METRIC, while the captured source text calls the framework MECA-CIM. This naming difference must be reconciled against the full paper before treating them as independently named artifacts. The official description establishes the problem, two-redundancy-column MDS approach, Hessian-trace layer allocation and analog syndrome-decoder direction. It does not provide the exact code, correction radius, array size, and fault/noise distributions. It also does not provide model results, AEDP values, process conditions or physical measurement.

The evidence supports a precise question. Can layer-aware analog ECC use limited redundancy where neural sensitivity is highest? It should also preserve correction coverage and reduce total area-energy-delay cost. It does not establish a universal two-column correction guarantee, robust accuracy across CNNs and Transformers, or a fabricated CIM result.

<span id="explanation-dac-2026-research043"></span>

## Strix treats NPU reliability as a system contract

An NPU is not only an array of multiply-accumulate units. An inference request passes through storage, local memories, and instruction and control logic. It also passes through arithmetic arrays, and normalization and nonlinear stages. It passes through software that programs those pieces. A fault in one part can be detected by a local mechanism. It can also change an intermediate tensor, or make the final output wrong. The protection needed depends on the fault's location, duration, propagation path, and consequence for the running workload.

Strix is described as a full-stack framework spanning microarchitecture, the instruction-set interface, and programming methods. It re-partitions the NPU along the inference pipeline and identifies dominant failure modes. It attaches targeted safeguards instead of replicating the entire NPU at a coarse granularity. The recovered assessment identifies the comparison as area-matched partial TMR, triple-instruction redundancy, and ReaLM with a rollback limit of one. [Recorded evidence](../observed-subthemes/accelerator-reliability.md#paper-dac-2026-research043)

## Why full replication is expensive and targeted protection is difficult

Replicating an entire NPU can detect disagreement by running redundant copies. It also repeats computation and requires extra storage, interconnect, control, and comparison logic. It also protects every block equally. This holds even when some blocks dominate failure risk. It also holds when an error in one stage is masked by later computation.

Targeted protection can lower cost by matching a safeguard to a failure mode. The safeguard might detect a corrupted register, check an instruction or tensor, roll back a state, or correct a result. That approach requires a map from fault location to response. A response that works for a transient bit flip may not work for a permanent stuck-at fault. A check that detects an error does not automatically identify the correct value. Rollback requires a valid checkpoint and a bound on repeated failure.

## The recovered fault model and evaluation boundary

The assessment records transient bit flips and permanent stuck-at faults at a default rate of 10⁻⁷. The rate denominator is defined as the original-input bit count. The selected evaluation uses the first 1,000 dataset samples and 10 runs. This makes the result conditional on both the fault model and the sampling budget. It is not a proof over all faults or all inputs.

The recorded platform is Gemmini with an AMD VU19P FPGA and 20 cluster nodes. BF16-I is an exception. The assessment records PyTorch following Spike behavior for LLM performance analysis. It does not record the same hardware configuration. Mixing that simulated condition with FPGA results would produce an invalid universal hardware conclusion.

## What the measurements mean

The recovered assessment records a 1.04× geometric-mean slowdown, with a 1.02×–1.07× range, under the stated Section 5 conditions. It also records a worst-case detection-latency bound below 1 microsecond at 500 MHz for INT8-D, INT8-I, and FP32-D. The assessment explicitly marks this as a detection bound. It is not a measured correction-latency bound. BF16-I is absent from the latency table.

The hardware overhead values are synthesis estimates using Design Compiler 2019.12 and a TSMC 28 nm library. The recorded area/power percentage pairs are 10.2/21.3 for FP32-D, 20.7/23.2 for INT8-D, and 8.7/16.8 for INT8-I. The available evidence does not establish fabricated-silicon measurements. The pair ordering and exact metric labels must remain tied to the assessment. They must not be interpreted as a single generic overhead number.

## Reliability needs an application-level acceptance rule

Fault localization, detection, correction and useful inference are separate outcomes. A system may locate a fault quickly but still spend time recovering. It may detect a wrong value but have no information to reconstruct it. It may correct an internal state while changing the model output for a particular input. The evaluation must state whether success means no silent error or restored tensor values. It must state whether it means preserved classification, bounded degradation, or completion before a deadline.

The source's “minimal hardware overhead” and 1.04× slowdown are meaningful only in one case. The protection coverage and workload must be the same as the baselines'. An area-matched comparison does not automatically mean equal energy, memory, timing, software effort, or fault coverage. A fault-injection campaign can demonstrate behavior for its sampled faults. It cannot establish safety certification or coverage of every physical fault mode.

## What the evidence establishes and leaves open

The recovered evidence supports Strix as a full-stack, failure-mode-specific reliability design. It records transient and permanent fault injections, baseline comparisons, and a conditional slowdown. It also records a detection-latency boundary and synthesis-based overhead estimates. It does not establish universal reliability, complete correction latency, fabricated hardware, all-workload behavior, all-precision coverage, or safety certification.

The precise research question concerns pipeline-specific safeguards across NPU hardware, ISA and programming. Can they meet a defined application-level reliability target? The total cost should be lower than that of monolithic replication. The fault model and workload must be the same. The current assessment is strong enough to explain that question and its conditions. It is not strong enough to independently accept the headline reliability claim.

<span id="explanation-dac-2026-research1139"></span>

## BFP changes how a fault propagates through an NPU

Block floating point (BFP) represents a group of values with shared scale information and separate fixed-point mantissas. The shared exponent gives the block a wider usable range than a small fixed-point number. It avoids a full exponent for every element. This saves hardware work, but it creates a dependency: one exponent participates in the interpretation of many mantissas.

That dependency changes reliability. A bit flip in one mantissa may affect one value or one path. A fault in a shared exponent can rescale many values at once. The final effect also depends on later nonlinear operations, such as activation or normalization. There, a small change before a threshold or division can produce a much larger change after it. The source describes pronounced heterogeneous vulnerabilities at bit and path level. It reports that a conventional end-to-end check becomes largely ineffective under nonlinear block scaling. [Recorded evidence](../observed-subthemes/accelerator-reliability.md#paper-dac-2026-research1139)

## Why an end-to-end check can miss the important fault

An end-to-end check compares a final output with a reference. It can miss an internal error when later operations mask the difference. It can also make localization difficult when many earlier errors produce similar final deviations. Under BFP, the same final mismatch can originate from several places. These are a mantissa, a shared exponent, a conversion, a memory path, or a control signal. A final check alone does not identify which component failed or which protection mechanism is needed.

The correct analysis needs at least three levels. At the bit level, it identifies which fields are vulnerable. At the path level, it follows a corrupted value through arithmetic, memory and nonlinear stages. At the application level, it defines whether the final result is wrong, degraded, or late. These levels answer different questions and should not be collapsed into one “reliability” number.

## What the row and column blocking is intended to do

The source describes row/column-wise blocking that decouples fixed-point mantissa computation from the scalar exponent path. The purpose is to keep the two kinds of information separable enough that each can receive a lightweight protection mechanism. Mantissa protection addresses errors in the repeated fixed-point computation; exponent protection addresses the shared scale that can affect many values.

Decoupling is not the same as removing the dependency. The block still needs a correct exponent and a correct association between an exponent and its mantissas. The design must preserve that association through storage, transfer, arithmetic and nonlinear operations. A protection mechanism that detects an exponent error may allow the block to continue with the wrong scale. It may then still produce a large application error.

## Interpreting the reported overhead and reliability

The captured source reports near-dual-modular-redundancy reliability with 3.55% geometric-mean performance overhead and less than 2% hardware cost. “Near-DMR reliability” requires a defined fault population, failure criterion and DMR comparison. It could refer to output-error rate under injected faults, detection coverage, corrected results, or another measure. Those are not interchangeable.

The geometric mean summarizes ratios across the evaluated cases. It does not show the worst case or the distribution of overhead. Hardware cost also needs a boundary: NPU compute arrays, protection logic, memory, control, interconnect, or complete accelerator. A percentage from one boundary cannot be compared with a percentage from another.

## The evaluation needed for a reliable BFP claim

The fault campaign should report transient and permanent fault types, bit and path locations, and injection rate and denominator. It should also report correlations, workload inputs, BFP block dimensions, exponent/mantissa format, and the number of runs. It should measure detection, correction, silent output error, accuracy or loss, timing impact, energy, area and recovery behavior separately.

The baselines should receive the same fault population and output-quality rule. If the comparison is against dual modular redundancy, the evaluation must state whether DMR duplicates all BFP state. It must also state whether Strix-like targeted protection uses the same available area or power budget. A near-DMR output result does not establish identical coverage of physical faults.

## What the available source establishes and leaves open

The official DAC description establishes an RTL-level fault-injection study and bit- and path-level vulnerability analysis. It also establishes a BFP NPU microarchitecture using row/column blocking with lightweight mantissa and exponent protection. It reports near-DMR reliability, 3.55% geometric-mean performance overhead, and less than 2% hardware cost.

It does not provide the fault distribution, BFP format, workloads, and exact reliability probability. It also does not provide accuracy criterion, technology implementation, area boundary, correction latency, energy, or independent reproduction. The evidence supports the question of whether BFP-specific protection can approach DMR reliability at lower cost. It does not establish a universal reliability guarantee or safety qualification.

## How to measure the combined outcome

Specify fault locations, rates, duration, and any correlations. Preserve the application input distribution and output-quality requirement. Measure incorrect outputs that escape detection, false alarms, recovery time, completion time, and energy with protection enabled.

If a method uses sensitivity estimates, test unfamiliar inputs and models. If it manages aging, evaluate sustained update patterns and changing device conditions. Explain whether faults are measured, injected into hardware, or introduced into a simulation.

The transferable result is a relationship between a stated fault condition and a protection decision. It also includes the useful correct work that remains after paying the protection cost. A faster fault-free run or an isolated successful recovery establishes only part of that relationship.
