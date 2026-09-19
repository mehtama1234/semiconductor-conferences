## Begin with an expected behavior

A test needs an input, a way to execute the design, and a rule for deciding whether its behavior is acceptable. Running many inputs without a reliable expected result does not establish correctness. A wrong expected result can reject a working design or accept a faulty one.

Simulation executes a model of a system. Emulation uses other hardware to execute a representation of that system. Both can make behavior observable before the final hardware is available, but their conclusions depend on which features and timing effects the representation includes.

## Faster execution and better tests are separate contributions

A faster simulator can run more cases in the available time. A better test generator can reach behaviors that earlier inputs did not exercise. A better checker can recognize failures that earlier checks missed. A paper can combine these improvements, but its evaluation should identify which one explains the result.

Coverage describes some set of exercised behaviors or structures. It might count code branches, states, requirements, or fault classes. Those definitions are not interchangeable. Reaching a branch does not establish that every input taking that branch behaves correctly. Detecting a known fault does not establish detection of faults that were absent from the experiment.

<span id="explanation-dac-2026-research1180"></span>

## ESCAPE: activity shaping can lower LBIST power only if fault excitation survives

Logic built-in self-test (LBIST) applies pseudo-random or structured patterns through scan chains and observes whether the circuit responds as expected. More transitions can improve the chance of sensitizing some faults, but they also raise instantaneous supply demand during shift or capture. The design problem is therefore not simply “toggle less”: it is to control activity while preserving the fault classes and observation paths that make the test effective.

ESCAPE is described as a programmable low-power LBIST architecture. A probability generator periodically emits user-configurable sequences that drive hold registers; two groups of hold registers feed a two-dimensional AND-gate array, and the resulting control signals modulate the enable probability of lockups before the phase shifter. The mechanism changes per-chain activity control and its temporal pattern. It does not itself establish which faults remain sensitized, how phase-shifter timing changes the pattern distribution, or how much control logic switches and costs area.

The first gate is fault-excitation validity. Define the scan architecture, shift and capture clocks, fault model, observability, pattern length, seeds, compression and coverage denominator. Compare detected, undetected, redundant and masked faults against uncontrolled and conventional low-power patterns at equal test length and diagnosis rules. A lower activity probability can reduce peak power while making rare transition or sensitization sequences less likely; aggregate coverage can conceal a lost critical fault class.

The second gate is the physical power boundary. Measure peak and average power separately at the actual voltage, frequency, tester timing and scan mode. Include the probability generator, hold registers, 2D array, phase shifter, configuration storage and their clock/control activity. Report IR-drop or supply disturbance where relevant, thermal behavior, pattern-generation area, timing, seed/configuration bandwidth and test-time overhead. A control circuit that reduces scan-chain switching but adds substantial clock or capture activity has not necessarily reduced system peak power.

Industrial-scale evaluation needs repeated seeds, per-design and per-fault-class results, power distributions and worst cases. Hold compression, pattern budget, ATE conditions, clocking, voltage, fault simulator, process and coverage accounting constant against uncontrolled and conventional low-power generation. Test different scan architectures, chain counts, process corners and manufacturing conditions; silicon or tester evidence is required before treating simulated activity shaping as a production-test benefit.

The official description claims high coverage, reduced peak power and lower hardware overhead on industrial-scale designs, but provides no numerical coverage, power, pattern-count, test-time, area or timing results, fault distribution, measurement method or silicon validation. The evidence supports programmable low-power LBIST activity shaping, not demonstrated quantitative fault-coverage preservation, peak-power reduction or production-test benefit.

<span id="explanation-dac-2026-research1348"></span>

## TOB-Sched: a balanced topological order is not yet cycle-accurate emulation throughput

Processor-based emulation executes a representation of a hardware computation graph on a set of processors. The graph's dependencies determine which nodes are ready, while inter-processor communication and synchronization determine when their results can be consumed. A static schedule can reduce idle time by distributing ready nodes, but a graph-order score is only useful if it predicts the timed execution of the emulation platform.

TOB-Sched is described as a topological-order balancing-driven static scheduler. It prioritizes nodes by mobility, uses forward and backward propagation, and presents a theorem that reduces gain calculation to O(1). These choices change candidate ordering and scheduling cost. They do not establish that dependencies, communication, memory, instruction execution and state updates are modeled faithfully, or that a schedule with better TOB completes an emulation faster on the target hardware.

The first gate is schedule semantics. Define topological order, mobility, gain, time step, dependency readiness, node allocation, communication latency, synchronization, resource capacity and tie-breaking. Replay schedules with a cycle-accurate or hardware-backed emulator and check functional equivalence, deadlock, ordering, state updates, stalls and communication. A theorem about gain-computation complexity does not by itself establish schedule construction plus execution complexity or emulation correctness.

The second gate is physical and workload transfer. Report makespan, processor utilization, idle time, critical path, communication bytes/stalls, memory use, schedule-construction time and emulation throughput per benchmark and graph scale. Hold netlists, mapping, processor count, interconnect, memory, clock, resource limits, seeds and runtime constant against list scheduling and unbalanced topological baselines. Test different processor counts, communication delays, fanout, graph structures and workload phases; static schedules may be brittle when those conditions change.

The official description reports 72% improvement in the TOB metric, 22.5% fewer time steps and 55% faster runtime than the state-of-the-art scheduler on public/open-source chip benchmarks. It provides no metric definitions, absolute makespan, emulation throughput, utilization, communication or memory results, processor/interconnect settings, functional validation or hardware-emulation evidence. The evidence supports topological-order-balanced static scheduling, not demonstrated cycle-accurate PBE throughput or transferable emulation efficiency.

<span id="explanation-dac-2026-research2085"></span>

## Prelude: replayed state is useful only when the invisible machine state is reconstructed faithfully

An FPGA processor prototype can run much faster and closer to deployment conditions than a software model, but internal signals are expensive to observe. Continuous tracing consumes on-chip bandwidth, storage and host-link capacity; snapshots reduce capture volume but omit transient pipeline and control state. Debugging then becomes a reconstruction problem: restore enough architectural state and memory, replay the same inputs, and observe the internal state needed to explain the failure without changing the behavior being debugged.

Prelude is described as a lightweight snapshot-based framework for FPGA processor debugging. It records essential architectural state and the processor memory footprint, then uses a short visibility warm-up during replay to reconstruct internal microarchitectural state for cycle-accurate analysis. This moves observation from continuous capture toward selective replay and priming. It does not establish that the captured state is sufficient, that replay sees the same external events, or that a plausible reconstructed trace localizes the original bug.

The first gate is state fidelity. Compare reconstructed and fully observed or independently instrumented references cycle by cycle, including pipeline registers, queues, cache/TLB state, predictors, arbitration, stalls, exceptions, interrupts, memory ordering and clock-domain crossings. Report divergence time, state-error rate, missing-state classes, replay determinism and bug-localization agreement. Architectural state and memory can match while hidden replacement, speculation or arbitration state differs and sends execution down another path.

The second gate is replay equivalence. Define snapshot consistency, restore ordering, memory initialization, external I/O, DMA, timers, interrupts, device responses, nondeterministic arbitration, multicore interactions and the stopping criterion for priming. Measure snapshot capture, storage, transfer, restore, warm-up, reconstruction and trace costs, as well as instrumentation area, timing, frequency and perturbation on the FPGA. A short warm-up is not a general convergence guarantee when the environment or microarchitectural history is not replayable.

The reported BOOM and Rocket comparison needs a matched debugging boundary. Hold core revision, workload, visibility target, trace retention, bug/replay criterion, FPGA and host resources, snapshot policy and cold/warm-start treatment constant against DESSERT, ENCORE, full tracing and snapshot-only debugging. Test long executions, phase changes, cache/memory pressure, interrupts, external devices and injected or real bugs; report absolute time, tails, storage/bandwidth and failures per case.

The official description claims comparable visibility to prior work and reports 32.88×/2191.2× speedup over DESSERT/ENCORE on BOOM and 18.09×/896.4× on Rocket. It does not expose absolute debug time, reconstruction error, trace bandwidth, storage, FPGA resource cost, workload, bug-localization accuracy, replay determinism or full baseline conditions. The evidence supports priming-guided FPGA processor debugging, not demonstrated universal cycle-accurate reconstruction, complete bug localization or portable debug-efficiency gains.

## GPU-Fuzz changes the inputs that are tried

The captured GPU-Fuzz record describes constraints on operator parameters and tests aimed at boundary conditions. An operator can accept many combinations of dimensions, types, and settings; the valid combinations determine which tests are meaningful. Values near a supported limit can expose indexing or allocation mistakes that ordinary inputs do not reach. [Recorded evidence](../observed-subthemes/simulation-emulation-and-testing.md#paper-dac-2026-research2056)

To interpret a bug-discovery result, establish how long the search ran, which versions and operators were tested, and how duplicate failures were combined into distinct bugs. Also determine whether developers confirmed the failures. The current description leaves those conditions unresolved, so a reported bug count cannot establish a general detection rate.

<span id="explanation-dac-2026-research2056"></span>

## GPU-Fuzz: boundary generation improves bug reachability only when the oracle and campaign are controlled

GPU framework testing has several layers of behavior. A high-level operator accepts tensors, shapes, data types, strides, layouts, and optional parameters. The framework validates or transforms those inputs before dispatching a GPU kernel. The kernel then performs indexing, allocation, reads, writes, and synchronization on a particular device and driver. A memory error can therefore arise from an invalid input check, a shape-dependent index calculation, a type or layout conversion, or a device-specific execution path. “The test ran” is not an adequate correctness oracle; the campaign must distinguish a normal result, an expected framework exception, an illegal memory access, a timeout, a nondeterministic failure, and a sanitizer or driver report.

GPU-Fuzz is described as modeling operator parameters as formal constraints and using a constraint solver to generate tests near error-prone boundaries. The mechanism changes how inputs are selected: instead of sampling mostly ordinary values, it can target dimensions, strides, types, and parameter combinations that satisfy the operator's interface while stressing limit conditions. The solver does not by itself prove that the generated input is semantically meaningful, that every reachable boundary was covered, or that a reported failure is a distinct confirmed bug. Those properties depend on the constraint model, executor, oracle, and triage pipeline.

The operator model must state its validity boundary. A shape can be legal for the public API but unsupported by a particular kernel specialization. A test can also be rejected before the GPU executes, fail because of an unsupported device feature, or expose a framework assertion rather than a memory safety defect. Record generated cases, rejected cases, executed kernels, sanitizer signals, framework errors, crashes, timeouts, and minimized reproductions separately. If the solver encodes only documented constraints, it may miss interactions in dispatch logic; if it relaxes them, the campaign may over-count invalid-input failures.

The discovery metric needs a denominator and a confirmation rule. “Unknown” can mean absent from a bug database, unseen by the authors before the campaign, or not previously reported for that framework version. Deduplicate reports by root cause rather than stack trace alone, reproduce each failure on a clean environment, and record whether maintainers confirmed or fixed it. Severity and security impact require separate analysis: a crash, out-of-bounds read, out-of-bounds write, information leak, and denial of service are not interchangeable outcomes. A memory sanitizer finding is evidence of a detected symptom, not automatically a remotely exploitable vulnerability.

The useful baselines are ordinary random or boundary fuzzing with the same operator inventory and time budget, existing GPU/framework fuzzers, and ablations that remove the formal constraints or solver-guided boundary selection. Hold framework commit, compiler, driver, GPU architecture, CUDA or accelerator runtime, sanitizer configuration, seed, concurrency, warmup, and campaign duration constant. Report operator and kernel coverage, valid-input execution rate, unique confirmed bugs, duplicate and false-positive rates, time to first confirmed bug, and failure distributions by error class. Include solver time, test construction, device reset, minimization, and human triage in the end-to-end cost.

The official description establishes constraint-guided boundary testing across PyTorch, TensorFlow, and PaddlePaddle and reports 13 previously unknown bugs. It does not expose the operator set, GPU models, software versions, campaign duration, baseline counts, deduplication rule, confirmation status, severity classes, sanitizer configuration, or security-impact analysis. The evidence supports a structured GPU-memory-fuzzing direction, not a general detection rate, framework-safety guarantee, or demonstrated security impact.

## Vten changes how verification work is expressed and executed

Vten's captured description proposes a tensor-oriented language for describing tests, with batching and decoupled execution. A tensor is a multidimensional collection of values. Describing a test in terms of such values can make an accelerator's intended computation easier to express than a collection of individual signal assignments. [Recorded evidence](../observed-subthemes/simulation-emulation-and-testing.md#paper-dac-2026-research2348)

Batching can reduce repeated setup and improve throughput. It can also change when a failure becomes visible and how easily the failing operation is located. A complete evaluation must therefore include test coverage, execution cost, and debugging behavior. The captured description does not establish these measurement conditions.

<span id="explanation-dac-2026-research1813"></span>

## RL4HDL: diverse compiler tests matter only when the oracle and defect counts are trustworthy

An FPGA logic-synthesis compiler translates RTL into a gate-level netlist. A compiler bug can reject legal RTL, crash, produce an invalid netlist, or silently change the implemented function while still producing a plausible-looking output. Testing therefore needs both diverse, executable HDL programs and an independent way to distinguish a real compiler defect from an invalid input, unsupported feature, simulator failure or infrastructure problem.

RL4HDL is described as using reinforcement learning and HDL code diversity to guide compiler-test generation. The learning policy changes which programs are explored and can prioritize structural or semantic regions that ordinary random tests repeatedly miss. The captured description does not specify the state/action representation, reward, HDL generation or mutation operators, compiler configuration, oracle, minimization procedure or defect-deduplication rule. Diversity is a search signal, not evidence that a test reaches a new compiler behavior.

The first gate is oracle validity. Separate parse/elaboration failures, rejected-but-validity-uncertain inputs, compiler crashes, synthesis errors, netlist invalidity, simulation mismatches, formal-equivalence failures, nondeterminism and infrastructure failures. For accepted RTL, compare the synthesized result with an independent behavioral or formal reference under the same widths, signedness, clock/reset, X/Z policy and optimization settings. A mismatch must be minimized and reproduced on a clean environment before it is counted as a defect.

The second gate is campaign accounting. Report valid-input execution rate, language-feature and compiler-path coverage, code/state coverage where meaningful, diversity, unique root causes, duplicates, false positives, time to first confirmed defect, severity, minimization effort and developer confirmation. Compare RL4HDL with random HDL fuzzing, mutation testing and the existing regression suite using the same compiler version, RTL subset, oracle, seeds and three-month or compute budget. Include policy training, test construction, synthesis, simulation/formal checking, reset, triage and repair time.

The official description reports a three-month campaign that discovered 20 unique defects, including 12 previously unreported defects, all confirmed by official developers. The captured evidence does not expose tool versions, RTL subset, baselines, coverage, oracle, deduplication, false-positive rate, severity or campaign cost. It supports RL-guided HDL compiler testing, not demonstrated synthesis correctness coverage or a general defect-detection advantage.

<span id="explanation-dac-2026-research1138"></span>

## ARTEMIS: adaptive SSD stress testing needs a trustworthy event oracle and transfer boundary

An SSD test generator explores sequences of reads, writes, idle periods and workload phases against a controller whose firmware, flash state and garbage-collection behavior evolve over time. A test that triggers a long pause is not automatically a defect: it may be normal reclamation, host interference, a timeout artifact or a firmware event that needs independent confirmation. The generator and the oracle must therefore be evaluated together.

[ARTEMIS](../observed-subthemes/simulation-emulation-and-testing.md#paper-dac-2026-research1138) formulates test-case generation as reinforcement learning and deploys directly on heterogeneous commercial SSDs without device-specific customization. At inference time it ensembles policies learned under diverse workload distributions to address non-stationary behavior. The captured record does not specify the state/action representation, reward, episode termination, policy aggregation, device feedback, safety limits or test-case minimization.

The first gate is event validity. Define Meta Garbage Collection and User Garbage Collection precisely, distinguish blocking events from ordinary latency variation, and record timeouts, firmware logs, host stalls, resets, device errors and confirmed root causes separately. Deduplicate events by root cause, reproduce them on a clean device, and report whether a developer or independent instrument confirmed the event and whether it creates user-visible reliability or performance impact.

The second gate is transfer and campaign accounting. Hold device access, firmware, NAND configuration, overprovisioning, workload, reset policy, test budget and host resources constant. Hold out SSD models, firmware versions, workload families and flash states; report event discovery per equal test budget, device-by-condition transfer, coverage, false positives, time to first confirmed event, unique events, policy disagreement and inference/training cost. Include safety controls, wear/retention state and device recovery overhead.

The source reports that the RL tester finds high-impact test cases triggering critical blocking garbage-collection events more frequently than conventional methods on Meta and User Garbage Collection stress tasks. It provides no numeric rates, confidence intervals, coverage, event-confirmation rule, false-positive rate, device matrix, campaign budget or end-to-end cost. The evidence supports RL-guided SSD stress-test generation and policy ensembling, not demonstrated device-agnostic verification coverage or general SSD reliability improvement.

<span id="explanation-dac-2026-research358"></span>

## Lyra: hardware-accelerated differential fuzzing still needs an independent processor oracle

Processor fuzzing generates instruction sequences, executes them, and checks whether the observed architectural behavior is valid. A RISC-V sequence can exercise more than arithmetic: privilege transitions, exceptions, CSRs, atomics, memory ordering, interrupts, virtual memory, cache behavior and implementation-specific extensions all affect the state that must be compared. Faster execution increases the number of trials only if the checker, trace path and reference model preserve the behavior being tested.

Lyra is described as running a DUT and reference model concurrently on an FPGA SoC, collecting hardware-level coverage, and pairing that differential engine with LyraGen, an ISA-aware generative model. The model can replace shallow random mutations with semantically structured instruction sequences, while the FPGA path can reduce software-simulation overhead. Neither mechanism proves that the reference model is complete, that the generated sequences reach rare modes, or that FPGA execution is equivalent to the intended processor environment.

The first gate is differential correctness. Fix the ISA and extensions, privilege modes, memory model, reset/boot state and nondeterminism policy. Compare architectural state, memory effects, exceptions, interrupts, CSR values, ordering and outputs against an independent oracle; report reference-model divergence, unsupported instructions, reset/debug failures, timeouts and mismatches separately. A DUT/reference agreement can reproduce a shared reference-model bug, so selected failures need a third checker, formal property or minimized software reproduction.

The second gate is coverage and campaign accounting. Report instruction, edge, state, functional, privilege, memory-system and extension coverage with denominators, plus sequence diversity, time to first confirmed failure, unique bugs, duplicates, false positives and minimized reproducers. Hold core, ISA, coverage probes, seeds, campaign duration, FPGA/host resources, trace storage and triage boundary constant against software fuzzing and mutation baselines. Include LyraGen training/inference, sequence construction, FPGA transfer, synchronization, reference execution, tracing, reset and bug triage.

The official description reports up to 1.27× higher coverage and 107×–3343× end-to-end verification acceleration versus state-of-the-art software fuzzers, with lower convergence difficulty. The captured evidence does not expose core or ISA details, coverage denominator, absolute throughput, campaign conditions, oracle quality, bug confirmation or hardware/software cost accounting. It supports FPGA-accelerated ISA-aware RISC-V fuzzing, not demonstrated verification completeness or general processor correctness coverage.

<span id="explanation-dac-2026-research2348"></span>

## vTen: batching simulation is useful only if observability and correctness remain intact

Verification of a domain-specific accelerator sits between a tensor-level reference model and signal-level RTL execution. The reference expresses an operation such as a convolution or activation over arrays; the RTL testbench drives handshakes, memory transactions, pipeline timing and reset behavior. Every abstraction boundary needs an explicit oracle. A faster exchange between host and simulator can increase the number of tests executed, but it does not by itself show that the accelerator's numerical and control behavior is correct.

vTen is described as a data-centric framework with a declarative tensor-centric DSL that decouples verification intent from execution mechanics. Kernel-granular batching reduces the frequency of host-simulator synchronization. This changes the unit of work sent to the simulator: many tensor operations can be prepared and executed as a batch rather than through fine-grained signal interactions. The design must still define how tensors become transactions, how dependencies, backpressure, interrupts and memory ordering are represented, and how a failed kernel is located inside a batch.

The first correctness gate is the reference relation. Fix the tensor shapes, data types, quantization, padding, layouts, memory initialization, reset sequence and accelerator configuration. Compare outputs and relevant state to an independently defined reference, including overflow, rounding, sparsity, exception and boundary cases. A test that completes faster or matches a few golden outputs does not establish cycle-level protocol correctness, state coverage or absence of data races.

The second gate is observability. Record whether a batch failed at DSL parsing, test construction, host transport, simulator execution, result checking or debug extraction. Measure time to isolate the failing kernel, the number of operations replayed during diagnosis, waveform or trace volume, and whether the framework can deterministically reproduce a failure. Batching can improve throughput while making a failure harder to localize; those are separate outcomes from simulation latency.

The reported 2× simulation-latency improvement needs a complete boundary. Separate DSL compilation, tensor preparation, host/runtime synchronization, simulator scheduling, RTL execution, result checking, trace collection and teardown. State whether latency is per kernel, per test, per batch or for the whole campaign, and report throughput, tail latency, batch size, synchronization count and memory use. Include warmup, simulator parallelism, compilation cache, waveform settings and hardware in the comparison.

Code complexity also needs a reproducible denominator. Define whether the 60.3% reduction counts lines, tokens, API calls, assertions, test modules, configuration or maintenance effort. Compare equivalent coverage and oracle strength against Cocotb and a UVM-style fine-grained testbench. Include the effort to learn the DSL, write adapters, debug failures and maintain tests when the RTL interface changes. Fewer lines can hide complexity in framework libraries, generated code or opaque batching semantics.

The baselines should include direct Cocotb execution, UVM-style signal-level interaction, and an otherwise identical tensor-level harness without batching. Hold the 3D U-Net accelerator, RTL commit, simulator, compiler, host, test set, reference model, coverage targets, waveform policy, batch budget and correctness oracle constant. Report functional, code, debug and performance results separately, with test coverage and rejected or nondeterministic cases.

The official description identifies a production-scale 3D U-Net accelerator and claims 2× lower simulation latency plus 60.3% lower code complexity than Cocotb. It does not expose simulator settings, test count, coverage, batching policy, latency boundary, code-complexity definition, baseline implementation, debug cost or correctness results. The evidence supports a tensor-centric verification interface and synchronization-reduction direction, not demonstrated verification completeness, debugging superiority or general simulation-speed improvement.

## Fault injection changes the system under test

Fault injection deliberately introduces an error to observe its consequences. The simultaneous-injection paper proposes evaluating multiple faults together while accounting for interactions. Two faults can sometimes hide one another's effects, so a combined experiment can miss a failure that appears when one fault is tested alone. [Recorded evidence](../observed-subthemes/simulation-emulation-and-testing.md#paper-dac-2026-research1417)

The method must identify the assumed faults, their locations, how they are combined, and the rule for judging an incorrect result. Saving test time is useful only if the changed experiment preserves the reliability question being asked. Its current record lacks enough model, fault-distribution, and campaign detail to establish broad coverage.

<span id="explanation-dac-2026-research1417"></span>

## Simultaneous DNN fault injection: speed is useful only when interacting faults remain observable

Fault injection evaluates a design by perturbing a specified state, parameter, memory bit, activation or instruction and comparing the resulting behavior with a fault-free reference. A DNN's layers are densely connected, so two injected faults can alter the same intermediate values, cancel each other, or change which later paths are exercised. A campaign that treats faults as independent must therefore detect when simultaneous injections invalidate the interpretation of a single-fault result.

The described approach mitigates artificial masking during simultaneous injection and prunes inputs judged non-critical to accelerate the campaign. It evaluates at software and RTL abstraction levels. These are separate axes: SW can run quickly but hide implementation timing and hardware state; RTL can expose more implementation detail but depends on the modeled design, simulator and oracle. Input pruning changes the exercised workload, so “negligible accuracy loss” must be defined against the unpruned fault campaign and the reliability metric, not only clean DNN accuracy.

The first gate is fault-model coverage. Specify transient duration, location, bit or signal distribution, multiplicity, timing, layer, memory/compute target, activation and data conditions. Compare simultaneous samples with an exhaustive or independently sampled single-fault reference, classify masked, interacting, detected, silent and output-changing faults, and report false negatives by fault class and model. A low aggregate false-negative rate can conceal a critical class that the interaction mitigation does not cover.

The second gate is oracle and abstraction validity. Define whether a fault is critical by top-1/top-k output, logit deviation, numerical tolerance, application loss, safety decision or RTL-visible behavior. Reconcile SW and RTL fault locations and timing, and verify that pruning preserves the input and fault distributions relevant to the claim. Include injection setup, simulation, reset, trace collection, comparison, failed runs and fault deduplication in the time budget.

The official description reports nearly 42 million SW/RTL injections, false negatives as low as 0% and average 0.2%, plus 3.82× RTL and 5.29× SW injection-time gains. It does not provide model architectures, fault distributions, interaction rates, oracle definitions, pruning thresholds, per-model variance, target hardware or campaign cost. The evidence supports interaction-aware DNN fault-assessment methodology, not demonstrated broad reliability coverage or safety assurance.

<span id="explanation-dac-2026-research177"></span>

## ARES: an executable protocol oracle is only as strong as the specification-to-monitoring chain

An IoT messaging protocol specifies more than message syntax. It defines valid sequences, state transitions, roles, permissions, timing and responses. A behavior bug occurs when an implementation accepts, rejects or processes a sequence differently from that specification in a way that can expose data or compromise a device. ARES is described as extracting executable behavior oracles from protocol specifications, then using LLM-driven behavior filtering for real-time compliance monitoring. The central change is therefore how expected behavior is generated and selected; it is not proof that the implementation, specification or monitor is complete.

The first gate is specification fidelity. The source format, protocol grammar, state-machine representation, roles, authentication assumptions, error behavior, optional extensions and version differences must be preserved when prose becomes an oracle. Record which requirements become executable checks, which remain unmonitorable, and whether the LLM may suppress a candidate behavior. A filter that removes noisy checks can also remove a security-relevant violation. Report oracle-generation failures, ambiguous requirements, monitor overhead and the coverage of states, transitions, message fields and negative cases.

The second gate is bug-oracle validity. Separate syntax violations, state-machine violations, authorization failures, malformed-input handling, resource exhaustion and implementation-defined behavior. Define the test generator, sequence length, seed, environment, network timing, device reset and observation boundary. Precision needs a denominator and a confirmation protocol: distinguish unique findings from duplicates, triage labels from reproduced bugs, and a CVE assignment from proof that the monitor found all exploitable behavior. Measure recall or missed bugs against seeded faults, differential implementations, a trusted reference or an independently constructed oracle.

The official description reports evaluation on six widely used IoT protocol implementations, 25 new bugs at 87.5% precision, including 21 behavior bugs; 18 were confirmed or fixed and 10 CVEs were assigned. It does not name the protocols, expose oracle coverage, report recall or false negatives, define the precision sample, give testing budgets or specify the independent confirmation process. The evidence supports automated protocol-oracle generation and runtime monitoring, not demonstrated oracle completeness, broad IoT prevalence or security assurance.

<span id="explanation-dac-2026-research2179"></span>

## DeTrojan: a stronger graph classifier is not the same as Trojan-detection coverage

A gate-level hardware Trojan is malicious logic embedded in a circuit that may remain dormant until a trigger and then alter behavior or leak information. Detection has two linked outputs: circuit-level classification, which asks whether a netlist contains a Trojan, and gate-level localization, which identifies suspicious gates. A model can improve one while producing costly false alarms or missing a new Trojan family. Security validity therefore depends on the attacker and circuit distribution, not only on an aggregate classifier score.

DeTrojan is described as combining functionality-aware node features, an edge-aware GNN with jumping knowledge and global context aggregation, and community-aware classification refinement for localization. These components add signal beyond structure-only features and use graph neighborhoods or communities to make fragmented node predictions more coherent. They do not guarantee that the features survive synthesis transformations, obscure Trojan construction, netlist scale changes or an attacker who adapts to the detector.

The first gate is dataset and threat-model separation. Specify design provenance, synthesis/library settings, circuit size, Trojan families, trigger and payload types, insertion process, class balance and whether multiple netlists derive from one design. Split by design and Trojan family rather than randomly splitting correlated gates. Hold out unseen designs, unseen Trojan mechanisms and obfuscated or adaptive variants. Report circuit-level confusion matrices, gate-level precision/recall/F1, localization distance, false-positive rate per clean circuit and the cost of missed versus falsely flagged gates.

The second gate is feature and refinement ablation. Compare structure-only features, functionality features, edge-aware message passing, jumping knowledge, global context and community refinement under the same graph construction, seeds, training budget and threshold selection. Check whether community labels or graph preprocessing leak Trojan annotations. Measure inference time, memory and analyst review burden, and validate suspicious gates with independent simulation, formal reasoning or reverse engineering rather than treating a classifier label as a confirmed Trojan.

The official description reports evaluation on the 2025 ICCAD CAD Contest hardware-Trojan benchmarks, with a 16.7% improvement in circuit-level accuracy and a 47.3% relative gate-level F1 increase over state-of-the-art ML methods; adding the features and refinement to existing approaches reportedly gives up to 16.6% accuracy and 2× F1 gains. It does not provide absolute scores, splits, Trojan families, false-positive cost, unseen/adaptive generalization, leakage controls or runtime. The evidence supports functionality- and community-aware Trojan classification, not demonstrated security coverage across proprietary or adversarial netlists.

<span id="explanation-dac-2026-research2319"></span>

## ChipModeler: generating a reference model faster does not make it a trusted oracle

A hardware reference model is an executable statement of intended functional behavior. Verification compares RTL or another implementation against that statement across legal transactions, corner cases, state histories, timing assumptions and reset behavior. A model can compile and produce plausible outputs while omitting protocol rules, mishandling widths or signedness, or sharing the same misunderstanding as the RTL. Generation productivity and verification adequacy are therefore separate outcomes.

ChipModeler is described as an LLM-assisted platform using standardized design representations, hierarchical agile modeling and reusable building blocks. The hierarchy can decompose a large reference model into interfaces and subfunctions, while building blocks can reduce repeated authoring. Those mechanisms must still define the behavioral contract, composition semantics, state ownership, clock/reset treatment, error handling and how generated pieces are checked against an independent specification.

The first gate is functional fidelity. Freeze the RTL revision, interface protocol, data types, signedness, latency, reset and exception semantics. Compare generated models with a trusted behavioral or formal oracle using directed corner cases, constrained-random sequences, assertions, differential RTL simulation and, where applicable, formal equivalence. Report compile failures, mismatches, coverage, escaped bugs, model repairs and the classes of behavior not represented by the standardization scheme.

The second gate is human and process cost. Separate initial prompt/model generation, design decomposition, integration, debugging, review, validation, simulator runtime and maintenance when the RTL changes. Compare manual modeling and validation with identical design inputs, correctness targets, reviewer expertise, tool versions and time budget. A larger generation capacity can simply produce more incorrect models; cycle acceleration is useful only if independent checks prevent incorrect reference behavior from becoming the new oracle.

The official description reports evaluation on 300 diverse designs, up to 58.99% performance improvement, a 9.18× increase in generation capacity and 7.11× faster design and validation cycles versus manual methods. It does not define performance, functional-equivalence rate, escaped defects, protocol coverage, human correction effort, model/ prompt versions or design distribution. The evidence supports hierarchical LLM-assisted reference-model authoring, not demonstrated trusted-oracle quality or verification completeness.

<span id="explanation-dac-2026-research2880"></span>

## UVMarvel: a generated UVM environment is valuable only when its stimulus and oracle reach the right behavior

A UVM testbench has several distinct jobs: drive legal and adversarial transactions, observe interface and internal behavior, compare results with a reference or assertions, collect coverage, and localize failures. Protocol-correct scaffolding can remove repetitive coding, but it does not guarantee that the tests reach rare state combinations, that scoreboards encode the intended behavior, or that high structural coverage detects a bug.

UVMarvel is described as an LLM-aided flow with an intermediate representation, a bus-protocol library, a signal tracker and a Verilog-patching library. The IR and protocol library translate heterogeneous specifications into subsystem-level UVM components; signal tracking and patching refine generated stimuli. The flow must still define transaction constraints, temporal sequences, reset/error behavior, scoreboards, assertions, coverage bins, patch acceptance and the independent oracle used to decide whether a test found a failure.

The first gate is functional coverage and bug detection. Specify bus protocols, legal and illegal transactions, backpressure, ordering, bursts, resets, errors, concurrency and state coverage. Report code, toggle, branch, assertion, functional and scenario coverage separately; measure unique bugs found, seeded-fault detection, escaped defects, false alarms, duplicate failures and time to triage. Code coverage can rise while the testbench repeatedly executes easy paths or uses an incorrect checker.

The second gate is automation and human-cost accounting. Compare manual UVM construction and stimulus refinement with the same RTL, protocol specification, simulator, seeds, licenses, compute, coverage targets and review standard. Include specification normalization, prompt/model execution, compilation, simulation, waveform/trace collection, patch iterations, debugging, scoreboard repair and expert review in the 4.5-hour boundary. Test across bus protocols and unseen subsystem structures, not only designs represented in the protocol library or generation examples.

The official description reports 95.65% average code coverage and a 4.5-hour automated execution compared with several human working days, and presents the flow as supporting mainstream bus protocols. It does not define coverage denominators, functional coverage, bug yield, escaped defects, protocol/state distribution, simulator resources, generated-test review or manual baseline accounting. The evidence supports automated subsystem-UVM construction and stimulus refinement, not demonstrated verification completeness or reduced escaped-bug risk.

<span id="explanation-dac-2026-research1858"></span>

## ReflectBench: consensus can improve testbench construction only when the oracle and system coverage are independent

System-level verification is not just the production of HDL stimulus. A testbench must drive legal and adversarial transactions across module boundaries, observe state and protocol behavior, compare results with an intended-behavior oracle, and report coverage and failures in a way that a reviewer can trust. An LLM-generated testbench and a generated or flawed reference design can share the same misunderstanding. They may agree on an incorrect behavior and produce a false-positive verification result.

ReflectBench is described as an agentic framework combining logic analysis, consensus-based validation, feedback self-reflection and testbench self-correction. It also uses Self-Reflective Domain Knowledge Mining to build a retrieval database aligned with hardware semantics, and ReflectVDB is described as a benchmark of 53 system-level designs. These mechanisms target candidate generation, critique and repair. They do not by themselves define the independent specification, scoreboard, assertion set, simulator semantics, agent roles, retrieval contents, repair stopping rule or how a discovered mismatch is confirmed.

The first gate is stimulus and oracle validity. Define interfaces, legal and illegal transactions, clocks, resets, ordering, backpressure, state histories, scoreboards, assertions, coverage bins and the reference-model provenance. Compare generated outputs with an independently specified behavior, not only with a reference produced from the same prompt or corpus. Report compilation failures, unsupported constructs, duplicate tests, false alarms, confirmed seeded faults, escaped violations, failure-triage effort and whether a system-level interaction was actually reached. Coverage without an independent oracle can measure activity rather than correctness.

The second gate is the agent loop and human-cost boundary. Expose prompts and roles, candidate count, consensus rule, logic-analysis representation, retrieved context, reflection and repair iterations, stochastic seeds, stopping condition and human intervention. Ablate logic analysis, consensus, self-reflection, self-correction and domain-knowledge retrieval under equal generation and simulation budgets. Include specification normalization, model calls, compilation, simulation, waveform/trace analysis, repair, review and reruns; a higher generation success rate is not an end-to-end verification gain if checking and correction work are omitted.

ReflectVDB's 53 designs and AutoBench comparison also need explicit design families, system complexity, protocols, splits, leakage controls, simulator versions, test budgets and coverage denominators. Evaluate unseen designs, protocol combinations and seeded or real bugs. Separate code, toggle, functional, assertion and scenario coverage from unique confirmed bug detection, false-positive rate and escaped-bug rate. More covered lines can reflect easier stimulus or a weaker denominator rather than better system-level verification.

The official description reports that ReflectBench improves testbench generation success rate over ConfiBench by 7.6% on ReflectVDB and 4.5% on AutoBench, and improves coverage rate by 3.8% and 1.2%, respectively. It describes ReflectBench/ReflectVDB as open-sourced, but the captured record does not expose the benchmark manifest, oracle independence, bug yield, false-positive rate, coverage definitions, compilation/runtime, human review or generalization conditions. The evidence supports agentic system-level testbench generation, not demonstrated reduction in escaped hardware bugs or independent verification completeness.

<span id="explanation-dac-2026-research2011"></span>

## Dart: shared RTL computation is valid only when the DAG preserves event semantics and per-stimulus state

RTL simulation advances signals and state through clocked and event-driven behavior. When many stimuli reach identical internal states, the simulator may be able to evaluate common logic once and reuse the result, but two stimuli that diverge later must retain separate histories. The optimization is therefore not ordinary batch parallelism: it depends on proving when states, inputs, scheduling events and outputs are equivalent.

Dart is described as constructing a DAG-based intermediate representation that exposes structural commonality and shared subexpressions across stimuli, merging sub-DAGs, evaluating shared logic once, and reconstructing per-stimulus state. The correctness contract must cover nonblocking assignments, delta cycles, clock and reset ordering, X/Z values, memory side effects, assertions, nondeterminism, timing controls and state divergence. A lightweight reconstruction mechanism is only sufficient if it restores every observable distinction required by the RTL semantics and debug flow.

The first gate is semantic equivalence. Compare Dart with a trusted reference such as Verilator or an event-accurate simulator on identical stimuli, seeds, resets, clocks, unknown-value policies and assertions. Check every output and relevant internal state cycle by cycle, including divergent branches, asynchronous events, memory writes, interrupts, backpressure and rare sequences. Report mismatches, unsupported constructs, reconstruction failures and whether waveform traces and failure localization remain equivalent.

The second gate is workload and resource accounting. Measure the amount of cross-stimulus state sharing, DAG construction time, merge cost, memory footprint, scheduling overhead, trace storage and synchronization. Vary stimulus similarity, count, ordering and divergence; high redundancy can make reuse look spectacular while diverse tests approach ordinary simulation with added DAG overhead. Compare per-stimulus CPU simulation, GPU batch simulation and RTLflow under the same design, stimulus set, waveform policy, compile cache, hardware and correctness checks.

The official description reports industrial RTL speedups of up to 136.7× over Verilator and 4.1× over RTLflow, with shared computation and state reconstruction claimed to preserve per-stimulus correctness. It does not provide design/stimulus counts, semantic coverage, memory cost, trace/debug behavior, unsupported RTL features or numerical comparison. The evidence supports cross-stimulus redundancy elimination, not demonstrated event-semantic equivalence or universal RTL simulation acceleration.

## A comparison that explains what improved

Use the same design versions, input constraints, correctness rules, and resource budget. Separate test-generation time, model execution, result checking, and human confirmation. Report confirmed failures, duplicated reports, false alarms, and unfinished runs.

For an execution-speed claim, compare the same tests and modeled behavior. For a detection claim, include designs or faults outside the development set. For a usability claim, measure the actual effort required to construct and debug a test. These experiments answer different questions and should appear as separate results.

<span id="explanation-dac-2026-research2760"></span>

## NotSoTiny: make RTL-generation evaluation measure the task, not only the model

### The paper changes the object being evaluated

RTL generation is often described as if the central question were “can a model write Verilog?” That question is too broad to be measured by one score. A model receives some specification or existing code, produces a module, and the evaluator decides whether the output is acceptable. The result depends on all three parts: the prompt, the task construction, and the acceptance test.

NotSoTiny addresses the task-construction part. It is a benchmark for contextual RTL module completion, built from hardware designs associated with the TinyTapeout community. The task is not unrestricted design from a prose requirement and it is not evidence that a model can produce a complete chip. A model is asked to complete a module in the context supplied by the benchmark. The benchmark therefore measures conditional code completion under hardware constraints. This boundary matters because a high score can mean that a model reconstructs a missing implementation from useful context; it does not by itself measure architectural invention, physical design, or silicon correctness.

The paper's claim is that earlier benchmarks can make generation appear easier than it is when they contain small or repetitive examples, weak verification, or examples that were present in model training data. NotSoTiny tries to make those failure modes visible by using structurally richer designs, removing duplicates, checking compatibility, and maintaining the collection as new community designs appear.

### Start with the dataset pipeline, because the pipeline defines the task

The benchmark begins with candidate hardware designs. Deduplication removes repeated or near-repeated examples so that many copies of one design do not make a model appear broadly capable. The captured preprint assessment records 3,062 tasks after deduplication and 1,114 tasks after compatibility filtering. The reduction is not a minor preparation detail. It changes the population on which a model can be scored.

Compatibility filtering uses a self-equivalence condition: a task must be suitable for the verification flow when the reference implementation is used in the completion setup. This protects the evaluation from tasks that the checker cannot meaningfully judge, but it also creates a selection boundary. A task that is difficult because of a parser, unsupported construct, reset convention, or solver limit may be removed before models are compared. The benchmark can therefore be rigorous within the retained population while still not representing every RTL module produced by the source community. The excluded-task distribution is needed to determine how much of the original design space remains.

The “living” property adds another boundary. A refreshed benchmark can reduce exposure to a fixed public test set, but a changing task set makes scores comparable only when the dataset revision, filtering rules, task split and evaluator version are recorded. A score on a later revision is not automatically a time-series improvement over a score on an earlier revision. The benchmark itself has changed.

### A completion task has several different correctness questions

For one task, the generated module can fail before equivalence is considered. It may be syntactically invalid, fail to compile, use a signal that is not in scope, violate the interface, or leave required behavior unspecified. A generated module can also compile and simulate on selected tests while still differing from the reference on an untested input. These outcomes should not be collapsed into one “pass” value.

NotSoTiny's reported verification flow uses simulation and Yosys formal-equivalence commands, including `equiv_simple` and `equiv_induct` with a sequence bound of 30. The preprint assessment explicitly distinguishes partition coverage from full equivalence. That distinction is necessary: proving the behavior of a selected partition or a bounded sequence is not the same as proving all reachable states and all input sequences. Reset assumptions, initialization, undriven values, black boxes, sequential depth and solver termination determine what the checker actually establishes.

The repository inspection adds an important evaluator-level condition. In the pinned `TuRTLe` path, a 900-second timeout is recorded through the same aggregation field as an equivalence success. This is a source-level finding, not evidence that the published model scores were inflated, because the paper's exact run logs and task revision were not reconciled here. It does establish the required audit action: proof completion, timeout, unproven result and tool error must be separate categories before a score is treated as a correctness rate. A timeout says that the evaluation did not finish within the allotted time; it does not say that the two designs were equivalent.

### Contamination analysis is evidence about exposure, not proof of independence

NotSoTiny uses comparative Min-K analysis across 11 models to study whether benchmark inputs resemble material in model training data. The recorded conditions include reference-only inputs and exclusion of modules above 2,000 tokens. These choices define the contamination probe. They do not prove that no training corpus contains the benchmark, that generated outputs were not influenced by related designs, or that the probe detects every form of leakage. There is no binary contamination threshold in the captured condition record.

This is why benchmark difficulty and contamination resistance must be reported separately. A task may be hard because its control structure is rich, because the context is incomplete, or because the model has not seen the pattern. A low memorization signal does not tell us which of these caused a failure. Conversely, a high memorization signal does not prove that a successful output was copied. The benchmark can expose a measurement risk without identifying its source for every task.

### What the evidence supports

The paper provides a concrete mechanism for improving RTL-generation evaluation: build from real community designs, remove duplicates, retain tasks compatible with a specified verification flow, compare models on contextual completion, inspect exposure with a stated contamination analysis, and refresh the collection. The available evidence supports the narrower conclusion that benchmark construction and evaluator semantics are part of the scientific result. It does not support a ranking of model capability from the headline description alone, because exact model prompts, per-task outcomes, dataset snapshot, split policy, solver versions, timeout handling and detailed score tables still need reconciliation.

The long-term research question is therefore not simply whether RTL models score higher. It is whether improvements survive a fixed revision boundary, strict separation of proof from timeout, held-out designs, contamination controls, and a complete accounting of compilation, verification and generation cost. Until those conditions are reported together, a benchmark score measures performance on a task-and-checker pipeline, not general hardware-design capability.

[Recorded paper evidence](../observed-subthemes/simulation-emulation-and-testing.md#paper-dac-2026-research2760)

<span id="explanation-iccad-2025-1027"></span>

## HLSDebugger: locate a logic bug before asking a model to repair it

### The debugging problem is not syntax repair

High-level synthesis translates a higher-level description such as C++ or SystemC into hardware. A compiler can reject malformed syntax, an undeclared name, or a type error. A logic bug is different: the program can compile and synthesize while producing behavior that differs from the intended function. The failure is in the relationship between the code and the required computation.

That difference changes the information available to a debugger. In ordinary software repair, a failing test often points toward the faulty behavior. HLSDebugger studies a harder case in which no additional test case or bug location is supplied. Given buggy HLS code, the system must identify the faulty region, classify the bug, and generate a replacement. The paper evaluates these as related but distinct tasks.

The manuscript identifies eight benchmark bug types: out-of-bounds array access, uninitialized-variable reads, out-of-bounds shifts, infinite loops from incorrect termination, unintended sign extension, incorrect manual loop unrolling, wrong initialization to zero, and copying from the wrong half of a split buffer. These categories are concrete transformations of known code, not a proof that they cover all HLS failure modes. They emphasize errors whose code may remain syntactically acceptable while changing the generated computation.

### The dataset creates supervision by changing known code

The paper addresses circuit-data scarcity by first collecting mostly correct HLS code from GitHub and augmenting it with HLS-like samples converted from RTL using GPT-3.5. The authors report roughly 30K crawled code samples and roughly 10K additional converted samples before supervised bug generation. GPT-3.5 is then prompted through three stages: function analysis, bug insertion, and debugging-strategy analysis.

The final labeled sample contains the buggy code, the location of the changed snippet, the bug type, and the corresponding correct snippet. The main generated dataset contains about 300K samples. A smaller auxiliary set adds a textual bug analysis and a suggested debugging strategy. This makes the training target precise: the model sees a known mutation and is asked to recover the annotated location and correction.

This construction has both strength and limitation. It supplies labels that are expensive to obtain by hand and lets the authors evaluate correction against a known target. It also makes the data distribution depend on the bug-insertion prompts, the original code collection, and the correctness of the generated labels. The converted RTL-to-HLS samples are not strictly functionally matched according to the paper's footnote. Therefore a high score establishes performance on this mutation-and-label pipeline; it does not establish robustness to arbitrary designer mistakes, synthesis-tool bugs, missing requirements, or bugs outside the eight categories.

The authors also remove approximately 2K training code samples whose Rouge-L similarity to the evaluation benchmark exceeds 0.5. This is a stated leakage-control step, not proof that all semantic or indirect overlap is absent. The final training set is reported as approximately 300K samples, but a complete generalization claim would still require the exact split, per-category denominators, and independent tests outside the generated mutation distribution.

### Why the model has an encoder and a decoder

A decoder-only repair prompt usually asks one generated sequence to name the location and then write a fix. If the location is wrong, the correction step starts from the wrong premise. The paper calls this error accumulation. HLSDebugger separates the internal functions while training them together.

The encoder reads the tokenized buggy code. One prediction head classifies the bug type. A second head assigns a binary bug indicator to each token. The token labels are highly imbalanced because most tokens are not faulty, so the training loss weights positive and negative token labels differently. The encoder output is not itself a corrected program; it is a representation that identifies where the model should concentrate.

The decoder receives the encoder's token representations through cross-attention and generates the corrected code snippet. In each decoding step it predicts the next correction token from the previous generated tokens and the encoder representation. The model is trained with three objectives: bug-type classification, token-level location classification, and maximum-likelihood generation of the correct snippet. The final loss weights the encoder and decoder objectives together, with the paper assigning a higher scale to correction loss because correction is more difficult than identification.

This design creates a measurable causal question. If the encoder is useful only for localization, it should improve identification but not necessarily correction. If its representation helps the decoder understand the reason for the bug, the combined system should improve correction beyond a separately fine-tuned generator. The paper includes an HLSEncoder-only ablation and combinations with Gemma-7B and GPT-4 to examine this boundary.

### The evaluation uses several denominators

The reported evaluation randomly selects 2,000 samples from an existing benchmark containing the eight bug types. The paper says accuracy stabilizes after more than 500 test samples, but the complete test set is still the stated 2K sample. Bug identification is measured at three granularities:

- token-wise: which tokens are marked as faulty;
- line-wise: whether the predicted faulty line matches the label; and
- code-wise: whether the correct line appears in the top-1 or top-5 predictions.

Precision and recall must be read together because faulty tokens and lines are the minority class. High recall can find most faulty material while also flagging many correct tokens. High precision can avoid false alarms while missing bugs. Code-wise top-5 accuracy answers a different operational question from token-level F1: whether a human or later tool could inspect one of five candidate lines.

Correction is measured with a strict substring match after processing spaces and special characters, with the generated length limited to three times the label length. This is reproducible, but it is not the same as compiling the corrected HLS, running a functional test, synthesizing it, or proving equivalence to a known-good implementation. A semantically correct rewrite can fail a string match; a matching snippet can still be unsuitable when placed in a larger context. The correction percentage therefore measures agreement with the labeled code under the paper's matching rule.

### What the reported results show

For bug identification, HLSDebugger reports token-level precision 54.3%, recall 83.5%, F1 0.614 and ROC area 0.935; line-level precision 57.7%, recall 78.4%, F1 0.627 and ROC area 0.923; and code-wise top-1/top-5 accuracy 79.5%/87.6%. GPT-4 reports 12.2%/37.1% token precision/recall, 13.3%/17.5% line precision/recall, and 19.7%/54.7% code-wise top-1/top-5. These are not interchangeable “accuracy” values: each uses a different prediction unit.

For correction without supplying the true location, HLSDebugger reports 37.6%, compared with 10.5% for GPT-4, 15.1% for Gemma-7B fine-tuned on the dataset, and 23.7% for HLSEncoder combined with Gemma-7B SFT. When the correct location is supplied, HLSDebugger reports 49.1% correction accuracy. The increase from 37.6% to 49.1% measures the cost of the localization problem under this benchmark; it does not mean a deployed debugger can assume the location is known.

The paper also reports a different 49.1% table for correction with the location given and shows per-bug-type results. The strongest conclusion is bounded: supervised data and the encoder–decoder design improve the selected identification and exact-snippet correction measures. The paper itself states that even the best system is not ready for practical debugging, because most cases are not corrected.

### What remains unestablished

The results do not establish that a generated correction compiles, preserves the intended algorithm, satisfies HLS synthesis constraints, or improves final hardware timing, area, and power. They do not measure human debugging time, inference cost, training cost, or performance on naturally occurring bugs. The dataset's GPT-generated mutations and the strict string metric make the benchmark useful for controlled comparison, but they also limit transfer to bugs that differ in source, context, type, or cause.

The long-term question is whether a debugger can maintain all three properties at once: identify the right region, propose a semantically valid correction, and demonstrate the correction through an independent hardware-aware check. A useful next evaluation would retain held-out projects and bug mechanisms, compile every generated repair, run functional or equivalence checks, report failures by bug type, and charge the full cost of candidate generation and verification. HLSDebugger provides a structured starting point for that loop; its current results do not close the loop.

[Recorded paper evidence](../observed-subthemes/simulation-emulation-and-testing.md#paper-iccad-2025-1027)
