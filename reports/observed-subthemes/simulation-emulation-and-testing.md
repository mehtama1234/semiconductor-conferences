# Simulation emulation and testing

This subject has 20 records in the selected sample. This page explains where it fits, then presents all captured paper evidence without shortening the measurements or limitations.

[Definitions used in the paper records](../reading-guide-v1.md)

## Understand the parent subject first

- [Verification and validation](../themes/verification-and-validation.md)

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

## Compare the results carefully

First identify the inputs and required output quality. Then identify the limited resource: time, memory, communication, energy, circuit area, or correctness coverage. Ask which part of the method reduces that cost and which new cost it adds. Compare numbers only when the experiments hold these conditions sufficiently similar.

A conference description may explain the proposal while omitting the full experiment. An author preprint link may have been coded from its abstract. The source classification does not by itself establish that every table was read. Missing locations remain visible below.

## Complete captured evidence

These are evidence records, not substitutes for the explanations above. Each record preserves its problem, proposed method, measurements, comparison conditions, and source limits. A populated record does not establish that its mechanism has been fully explained or independently verified.

<span id="paper-dac-2026-research2056"></span>

### GPU-Fuzz: Finding Memory Errors in Deep Learning Frameworks

DAC 2026 · Record: `dac-2026-research2056`

[Read the step-by-step explanation](#explanation-dac-2026-research2056)

**Updated source-backed reading card**

Reviewed 2026-09-08. Deepens the existing GPU-Fuzz treatment into a paper-level reading; separates constraint-guided input generation from execution oracles and bug confirmation, defines campaign denominators and deduplication, preserves the 13-bug claim, and makes framework, GPU, sanitizer and security-impact boundaries explicit.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

GPU memory errors in deep-learning frameworks can cause crashes or security-relevant behavior, while ordinary input sampling may miss shape, stride, type and parameter boundaries in operator kernels.

**Mechanism / artifact:**

Constraint-guided GPU-kernel fuzzer that models operator parameters and uses a solver to generate boundary-focused cases; constraint encoding, executor, oracle, minimization and triage flow are unspecified.

**Workload — the work tested:**

GPU operators in PyTorch, TensorFlow and PaddlePaddle; operator inventory, kernel paths, framework commits, input validity rules, campaign duration, seeds, concurrency and bug-severity criteria are unspecified.

**Hardware and manufacturing assumptions:**

GPU kernels executed through deep-learning frameworks with drivers, compilers, runtimes and memory-safety instrumentation; GPU architectures, CUDA/runtime versions, sanitizer, reset behavior and host platform are unspecified.

**Baseline — the comparison method:**

Existing GPU/framework fuzzers

Random or ordinary boundary fuzzing with the same operator inventory and time budget

Constraint-guided flow without solver-guided boundary selection

Same framework commits, drivers, GPUs, sanitizer, seeds, concurrency, warmup, campaign duration, minimization and triage boundary are unspecified

**Reported measurements:**

The official description reports 13 previously unknown bugs across three frameworks; it provides no denominator, unique-confirmed definition, operator/kernel coverage, time to bug, duplicate or false-positive rate, failure-class distribution, baseline count, or end-to-end campaign cost.

**Limits on the conclusion:**

Generated cases must be separated into valid execution, expected rejection, framework error, timeout, nondeterministic failure and memory-safety signal. A solver-generated boundary input does not prove semantic validity or exhaustive boundary coverage.

Unknown-bug counts depend on version, disclosure, deduplication and confirmation policy. Reproduce on a clean environment, deduplicate by root cause, and report crashes, invalid accesses, leaks, denial of service and other classes separately; a sanitizer signal is not automatically a security vulnerability.

The official description omits operator inventory, software/hardware versions, campaign duration, baselines, sanitizer setup and confirmation/severity evidence. The evidence supports structured GPU-memory fuzzing, not a general detection rate, framework-safety guarantee or demonstrated security impact.

**Source and location**

Evidence tier: Primary captured official DAC description plus existing chapter level gpu fuzz discussion; no full paper extraction, reproduced fuzzing campaign, bug confirmation trace or independent review. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH2056&sess=sess152)

DAC 2026 official description; existing chapter-level GPU-Fuzz discussion; captured Problem, Mechanism / artifact, Workload, Hardware, Baseline, Measurements and Limits fields; no manuscript pages or campaign logs.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** existing GPU/framework fuzzers

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH2056&sess=sess152

**Hardware or process assumptions:** GPU kernels executed through major deep-learning frameworks; GPU models, drivers, compiler versions, and sanitizer configuration are unspecified.

**Limits:** The description omits fuzzing duration, operator coverage, deduplication, bug confirmation process, and baseline discovery counts.

Unknown-bug counts are sensitive to framework versions and disclosure/triage policies.

Official description only; reproducibility and security impact require paper-level verification.

**Method or artifact:** Constraint-based GPU-kernel fuzzer that formalizes operator parameters and systematically generates boundary-condition test cases.

**Metrics:** 13 previously unknown bugs discovered

**Problem:** GPU memory errors in deep-learning frameworks can cause crashes and security issues, while ordinary fuzzing may miss structured boundary conditions in operators.

**Workload or benchmark:** PyTorch, TensorFlow, and PaddlePaddle GPU operators; tested operator inventory, GPU architectures, execution budget, and bug-severity criteria are unspecified.

</details>

<span id="paper-dac-2026-research2348"></span>

### Vten: Tensor-Centric Verification Framework for Domain-Specific Accelerators

DAC 2026 · Record: `dac-2026-research2348`

[Read the step-by-step explanation](#explanation-dac-2026-research2348)

**Updated source-backed reading card**

Reviewed 2026-09-08. Deepens the existing vTen treatment into a paper-level reading; separates tensor-centric intent, kernel-granular batching and host-simulator synchronization from verification correctness, coverage, debug observability and end-to-end simulation cost, preserves the 2x and 60.3% claims, and makes oracle and baseline boundaries explicit.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Tensor-centric accelerator models must be verified against signal-level RTL, while fine-grained UVM/Cocotb host-simulator interactions impose synchronization overhead.

**Mechanism / artifact:**

Declarative tensor-centric verification DSL with kernel-granular batching and decoupled execution; tensor-to-transaction mapping, dependency/ordering semantics, oracle, failure localization and trace policy are unspecified.

**Workload — the work tested:**

Production-scale 3D U-Net domain-specific accelerator; RTL design, tensor shapes/types, test count, reference model, coverage target, simulator, batch sizes, test set and correctness criteria are unspecified.

**Hardware and manufacturing assumptions:**

Host-driven RTL simulation with a tensor-level reference and signal-level accelerator testbench; RTL language, simulator/compiler, host hardware, runtime, waveform settings, parallelism and compilation-cache assumptions are unspecified.

**Baseline — the comparison method:**

Cocotb

UVM-style fine-grained verification

Tensor-centric harness without kernel-granular batching

Same accelerator, RTL commit, simulator, compiler, host, tests, reference model, coverage target, waveform policy, batch budget, correctness oracle and end-to-end timing boundary are unspecified

**Reported measurements:**

The official description reports 2x simulation-latency improvement and 60.3% lower code complexity versus Cocotb; it supplies no latency boundary, throughput, tail latency, test coverage, debug cost, code-complexity denominator, simulator setting or correctness result.

**Limits on the conclusion:**

Batching can reduce synchronization while weakening failure localization or changing observability. Validate tensor outputs and protocol/state behavior under fixed shapes, types, quantization, reset, memory ordering, backpressure, overflow and boundary cases; separate parse, execution, checker, timeout and debug failures.

Measure DSL preparation, compilation, host transport, synchronization, simulator scheduling, RTL execution, checking, trace collection and teardown. Define code complexity and compare equivalent coverage, oracle strength, learning, adapter, maintenance and debugging effort.

The 2x and 60.3% claims lack simulator, test, coverage, batching, latency, code-counting, baseline and correctness conditions. The evidence supports a tensor-centric verification interface and synchronization-reduction direction, not demonstrated verification completeness, debugging superiority or general simulation-speed improvement.

**Source and location**

Evidence tier: Primary captured DAC official description plus existing chapter level conceptual discussion; no full paper extraction, coverage report, debug trace or independent review. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH2348&sess=sess163)

DAC 2026 official description; existing chapter-level vTen discussion; captured Problem, Mechanism / artifact, Workload, Hardware, Baseline, Measurements and Limits fields; no manuscript pages or reproduced simulation campaign.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** Cocotb

UVM-style fine-grained verification

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH2348&sess=sess163

**Hardware or process assumptions:** Domain-specific accelerator simulation with host/simulator interaction; RTL language, simulator, hardware scale, and test environment are unspecified.

**Limits:** The description omits test coverage, simulator settings, latency measurement, code-complexity definition, and baseline implementation.

Batching can improve throughput while changing debug granularity and failure localization.

Official description only; verification completeness and usability require paper-level verification.

**Method or artifact:** Declarative tensor-centric verification DSL with kernel-granular batching and decoupled execution.

**Metrics:** 2x simulation-latency improvement

60.3% lower code complexity versus Cocotb

**Problem:** Tensor-centric software models and signal-level hardware testbenches create a semantic gap, while fine-grained UVM/Cocotb interaction imposes synchronization overhead.

**Workload or benchmark:** Production-scale 3D U-Net domain-specific accelerator; testbench size, simulator, coverage, correctness criteria, and UVM baseline are unspecified.

</details>

<span id="paper-dac-2026-research1417"></span>

### Scalable Reliability Assessment of DNNs Through Simultaneous Fault Injection

DAC 2026 · Record: `dac-2026-research1417`

[Read the step-by-step explanation](#explanation-dac-2026-research1417)

**Updated source-backed reading card**

Reviewed 2026-09-08. Deepens the existing simultaneous-fault-injection treatment into a paper-level reading; separates interaction-aware simultaneous injection and input pruning from fault-model coverage, masking, oracle validity, SW/RTL abstraction, campaign cost and reliability conclusions, preserves the nearly-42-million, false-negative, 3.82x and 5.29x claims, and defines the assessment boundary.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

DNN fault campaigns scale poorly, while simultaneous fault injection can create interactions and artificial masking that misclassify critical faults as non-critical.

**Mechanism / artifact:**

Interaction-aware simultaneous DNN fault-injection assessment with mitigation of artificial masking and pruning of non-critical inputs for acceleration at software and RTL levels; interaction model, pruning rule, oracle and fault mapping are unspecified.

**Workload — the work tested:**

DNN transient-fault campaigns at SW and RTL abstraction levels totaling nearly 42 million injections; model architectures, layers, inputs, fault multiplicity/location/timing, target implementation, abstraction correspondence and campaign split are unspecified.

**Hardware and manufacturing assumptions:**

Software and RTL DNN implementations with fault injection; processor/accelerator, RTL design, simulator, memory/compute fault sites, timing, reset, precision, tool versions and campaign hardware are unspecified.

**Baseline — the comparison method:**

Existing DNN fault-injection approaches

Single-fault or non-simultaneous assessment

Same DNNs, fault distribution, input set, oracle, abstraction, simulator, pruning budget, seeds, trace/comparison process and end-to-end campaign boundary are unspecified

**Reported measurements:**

The official description reports nearly 42 million injections, false negatives as low as 0% with 0.2% average, and 3.82x RTL and 5.29x SW average injection-time gains; it supplies no interaction rate, fault-class distribution, oracle definition, per-model variance, pruning threshold or campaign-cost breakdown.

**Limits on the conclusion:**

Specify transient fault location, duration, bit/signal distribution, multiplicity, timing, layer, memory/compute target and data conditions. Compare simultaneous samples with independent single-fault references and classify masked, interacting, detected, silent and output-changing faults by critical class.

Define criticality by output, logits, numerical tolerance, application loss, safety decision or RTL behavior. Reconcile SW and RTL fault sites/timing, validate input pruning against unpruned reliability outcomes, and include setup, reset, trace, comparison, failed-run and deduplication costs.

The nearly-42-million, false-negative, 3.82x and 5.29x claims lack model, fault, interaction, oracle, pruning, abstraction and campaign-cost conditions. The evidence supports interaction-aware DNN fault assessment, not demonstrated broad reliability coverage or safety assurance.

**Source and location**

Evidence tier: Primary captured DAC official description plus existing chapter level conceptual discussion; no full paper extraction, fault trace, oracle validation or independent review. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH1417&sess=sess127)

DAC 2026 official description; existing chapter-level simultaneous fault-injection discussion; captured Problem, Mechanism / artifact, Workload, Hardware, Baseline, Measurements and Limits fields; no manuscript pages or reproduced SW/RTL campaign.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** existing DNN fault-injection approaches

single-fault or non-simultaneous assessment

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH1417&sess=sess127

**Hardware or process assumptions:** DNN implementations evaluated at SW and RTL levels with transient-fault injection; target accelerator/processor, RTL design, and fault model are unspecified.

**Limits:** The description omits model architectures, fault distributions, accuracy criteria, campaign cost, and per-model variance.

Low false-negative rates may depend on the interaction model and selected pruning threshold; other fault classes may behave differently.

Official description only; reliability conclusions require paper-level campaign and oracle verification.

**Method or artifact:** Interaction-aware simultaneous fault-injection assessment with mitigation of artificial masking and input-batch pruning for further acceleration.

**Metrics:** Nearly 42 million injections

False negatives as low as 0%, average 0.2%

3.82x average RTL injection-time gain

5.29x average SW injection-time gain

**Problem:** Conventional DNN fault injection does not scale to large models, while simultaneous injection can interact and create false negatives that misclassify critical faults.

**Workload or benchmark:** DNN fault campaigns at software and RTL abstraction levels totaling nearly 42 million injections; models, fault distributions, hardware, and baseline tool details are unspecified.

</details>

<span id="paper-dac-2026-research177"></span>

### Finding Behavior Bugs in IoT Messaging Protocols with Automated Oracle Generation and Monitoring

DAC 2026 · Record: `dac-2026-research177`

[Read the step-by-step explanation](#explanation-dac-2026-research177)

**Updated source-backed reading card**

Reviewed 2026-09-08. Deepens the existing ARES treatment into a paper-level reading; separates executable oracle extraction and LLM behavior filtering from specification fidelity, oracle coverage, bug confirmation, monitoring overhead and security conclusions, preserves the six-implementation, 25-bug, 87.5%, 18-confirmed/fixed and 10-CVE claims, and defines the evidence boundary.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

IoT messaging implementations can violate protocol behavior specifications in ways that enable unauthorized access or device compromise, while manual or incomplete oracle construction misses behavior bugs.

**Mechanism / artifact:**

Automated specification-to-executable-oracle extraction with LLM-assisted behavior filtering and real-time compliance monitoring; source representation, oracle coverage, filtering rule, test generation and confirmation process are unspecified.

**Workload — the work tested:**

Six widely used IoT messaging protocol implementations; protocol names, versions, specification formats, test sequences, state/transition coverage, precision denominator and independent confirmation set are unspecified.

**Hardware and manufacturing assumptions:**

IoT protocol implementations and a runtime network-monitoring environment; device platforms, network conditions, reset/state control, implementation versions, monitor placement, compute and LLM model/configuration are unspecified.

**Baseline — the comparison method:**

Manual or existing protocol bug-detection workflows

Specification-derived oracle without LLM filtering

Same protocols, implementations, test generator, environment, oracle, seed, sequence budget, deduplication and confirmation process are unspecified

**Reported measurements:**

The official description reports 25 new bugs at 87.5% precision across six implementations, including 21 behavior bugs, with 18 confirmed or fixed and 10 CVEs assigned; it supplies no recall, false-negative rate, oracle coverage, test budget, monitoring overhead, precision denominator or per-protocol breakdown.

**Limits on the conclusion:**

Translate protocol prose, grammar, state transitions, roles, permissions, timing, error behavior and optional extensions into executable checks, and report uncovered or ambiguous requirements and filtering failures. LLM filtering can suppress security-relevant violations as well as noise.

Define bug classes, sequence generation, state/reset control, timing, observation boundary and confirmation protocol. Separate unique reproduced findings from duplicates, triage labels, fixes and CVE assignments; measure missed bugs with seeded faults, a trusted reference or an independently constructed oracle.

The six-implementation, 25-bug, 87.5%, 18-confirmed/fixed and 10-CVE claims lack protocol, oracle, recall, test-budget and confirmation conditions. The evidence supports automated protocol-oracle generation and runtime monitoring, not demonstrated oracle completeness, broad IoT prevalence or security assurance.

**Source and location**

Evidence tier: Primary captured DAC official description plus existing chapter level ares discussion; no full paper extraction, oracle artifact, protocol trace or independent security review. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH177&sess=sess146)

DAC 2026 official description; existing chapter-level ARES discussion; captured Problem, Mechanism / artifact, Workload, Hardware, Baseline, Measurements and Limits fields; no manuscript pages or reproduced protocol campaign.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** manual or existing protocol bug-detection workflows

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH177&sess=sess146

**Hardware or process assumptions:** IoT protocol implementations and monitoring environment; device platforms, network conditions, specification formats, and LLM model/configuration are unspecified.

**Limits:** The description omits recall, oracle completeness, false negatives, test budget, protocol distribution, and independent confirmation criteria.

CVE assignment and fixes indicate impact for a subset, not prevalence across IoT deployments.

Official description only; security findings require reproducible disclosure and paper-level verification.

**Method or artifact:** Automated specification-to-executable-oracle extraction with LLM-assisted behavior filtering and runtime monitoring.

**Metrics:** 25 new bugs identified

87.5% precision

21 behavior bugs

18 findings confirmed or fixed

10 CVEs assigned

**Problem:** IoT messaging implementations can violate protocol behavior specifications in ways that enable unauthorized access or device compromise, while manual oracle construction is incomplete.

**Workload or benchmark:** Six widely used IoT messaging protocol implementations; protocol names, test volume, oracle coverage, and precision denominator are unspecified.

</details>

<span id="paper-dac-2026-research2179"></span>

### Detrojan: Detecting Trojan Circuits Using a Purpose-Built Graph Neural Network with Community-Enhanced Classification

DAC 2026 · Record: `dac-2026-research2179`

[Read the step-by-step explanation](#explanation-dac-2026-research2179)

**Updated source-backed reading card**

Reviewed 2026-09-08. Deepens the existing DeTrojan treatment into a paper-level reading; separates functionality-aware features, edge-aware GNN context and community refinement from threat-model coverage, dataset leakage, false-positive cost, localization validity and adversarial generalization, preserves the ICCAD-contest, 16.7%, 47.3%, 16.6% and 2x claims, and defines the security evidence boundary.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Structure-only GNN features and fragmented node predictions can limit gate-level hardware-Trojan detection and localization, while false alarms and missed or unseen Trojans carry different security costs.

**Mechanism / artifact:**

Functionality-aware feature engineering, edge-aware GNN with jumping knowledge and global context aggregation, and community-aware classification refinement for circuit-level detection and gate-level localization; graph construction, features and refinement labels are unspecified.

**Workload — the work tested:**

2025 ICCAD CAD Contest hardware-Trojan benchmarks; circuit provenance, synthesis/library settings, sizes, Trojan families, trigger/payload types, insertion process, class balance, design/Trojan splits and unseen/adaptive test set are unspecified.

**Hardware and manufacturing assumptions:**

Gate-level netlist graphs for hardware-Trojan detection; HDL-to-netlist flow, libraries, synthesis transformations, graph extraction, compute hardware, inference budget and analyst-validation process are unspecified.

**Baseline — the comparison method:**

State-of-the-art machine-learning hardware-Trojan detectors

Existing GNN approaches

Structure-only features

Same design/Trojan split, graph extraction, seeds, training budget, threshold selection, class weighting and evaluation cost are unspecified

**Reported measurements:**

The official description reports 16.7% improvement in circuit-level accuracy and 47.3% relative gate-level F1 improvement over state-of-the-art ML methods; adding features/refinement to existing approaches reportedly gives up to 16.6% accuracy and 2x F1 gains. It supplies no absolute scores, confusion matrices, false-positive rate, localization error, runtime, memory or per-family breakdown.

**Limits on the conclusion:**

Split by design and Trojan family, not correlated gates. Hold out unseen designs, mechanisms, obfuscated and adaptive variants; report circuit confusion, gate precision/recall/F1, localization distance, false-positive rate per clean circuit and asymmetric missed-versus-review cost.

Ablate functionality features, edge-aware message passing, jumping knowledge, global context and community refinement under matched graphs, seeds, training and thresholds. Check graph preprocessing and community labels for annotation leakage, and validate alerts with independent simulation, formal reasoning or reverse engineering.

The ICCAD-contest, 16.7%, 47.3%, 16.6% and 2x claims lack absolute scores, splits, Trojan families, false-positive cost, leakage controls, adaptive generalization and runtime. The evidence supports functionality- and community-aware Trojan classification, not demonstrated security coverage across proprietary or adversarial netlists.

**Source and location**

Evidence tier: Primary captured DAC official description plus existing chapter level conceptual discussion; no full paper extraction, dataset split audit, adversarial validation or independent security review. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH2179&sess=sess111)

DAC 2026 official description; existing chapter-level simulation/testing discussion; captured Problem, Mechanism / artifact, Workload, Hardware, Baseline, Measurements and Limits fields; no manuscript pages or reproduced Trojan benchmark.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** state-of-the-art machine-learning hardware-Trojan detectors

existing GNN approaches

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH2179&sess=sess111

**Hardware or process assumptions:** Gate-level netlist graphs for hardware-Trojan detection; synthesis/library provenance, design scale, and deployment context are unspecified.

**Limits:** The description omits absolute scores, false-positive cost, unseen-Trojan generalization, dataset leakage controls, and runtime.

Contest benchmarks may not represent proprietary netlists or adaptive attackers.

Official description only; security-detection claims require dataset and adversarial validation.

**Method or artifact:** Functionality-aware feature engineering, edge-aware GNN with global context, and community-aware classification refinement.

**Metrics:** 16.7% improvement in circuit-level prediction accuracy

47.3% relative increase in gate-level F1-score

Up to 16.6% accuracy gain and 2x F1 gain when modules augment existing approaches

**Problem:** Structure-only GNN features and fragmented node predictions limit gate-level hardware-Trojan detection accuracy and localization.

**Workload or benchmark:** 2025 ICCAD CAD Contest hardware-Trojan benchmarks; circuit counts, Trojan families, splits, class imbalance, and baseline implementations are unspecified.

</details>

<span id="paper-dac-2026-research2319"></span>

### Chipmodeler: LLM-Aided Reference Model Design for Agile Hardware Verification

DAC 2026 · Record: `dac-2026-research2319`

[Read the step-by-step explanation](#explanation-dac-2026-research2319)

**Updated source-backed reading card**

Reviewed 2026-09-08. Deepens the existing ChipModeler treatment into a paper-level reading; separates standardized hierarchical LLM reference-model generation from behavioral fidelity, protocol coverage, independent oracle checking, defect escape and human maintenance cost, preserves the 300-design, 58.99%, 9.18x and 7.11x claims, and defines the evidence boundary.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Reference-model development for functional IC verification becomes a bottleneck as designs grow complex and requires repeated expert authoring and validation effort.

**Mechanism / artifact:**

LLM-assisted hierarchical reference-model generation using standardized design representations, agile modeling and reusable building blocks; behavioral contract, composition, state/reset semantics, model/tool versions and independent checks are unspecified.

**Workload — the work tested:**

300 diverse hardware designs compared with manual reference-model development; design languages, interfaces, protocols, sequential behavior, corner cases, model correctness criteria, design distribution and split are unspecified.

**Hardware and manufacturing assumptions:**

Functional hardware-verification flow with generated reference models and RTL comparison; RTL language/tool, simulator, formal checker, compute environment, reviewer expertise, interface protocols and maintenance conditions are unspecified.

**Baseline — the comparison method:**

Manual reference-model design and validation

Same designs, RTL revisions, correctness target, directed/random/formal tests, reviewers, tools, compute, time budget and maintenance boundary are unspecified

**Reported measurements:**

The official description reports 300 evaluated designs, up to 58.99% performance improvement, 9.18x generation-capacity increase and 7.11x faster design/validation cycles versus manual methods; it supplies no functional-equivalence rate, escaped defects, protocol coverage, compile failures, repair effort, metric definition or per-design distribution.

**Limits on the conclusion:**

Freeze RTL revision, interfaces, protocols, types, signedness, latency, reset and exception semantics. Check generated models with an independent behavioral/formal oracle, directed corner cases, constrained-random sequences, assertions and differential simulation; report mismatches, coverage, repairs, escapes and omitted behavior.

Separate generation, decomposition, integration, debugging, review, validation, simulator and maintenance costs. Compare manual and LLM flows with matched designs, correctness targets, reviewers, tools and budgets; more generated models do not imply more correct models.

The 300-design, 58.99%, 9.18x and 7.11x claims lack metric, model, protocol, defect, human-effort and distribution conditions. The evidence supports hierarchical LLM-assisted reference-model authoring, not demonstrated trusted-oracle quality or verification completeness.

**Source and location**

Evidence tier: Primary captured DAC official description plus existing chapter level conceptual discussion; no full paper extraction, generated model corpus, equivalence trace or independent review. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH2319&sess=sess166)

DAC 2026 official description; existing chapter-level simulation/testing discussion; captured Problem, Mechanism / artifact, Workload, Hardware, Baseline, Measurements and Limits fields; no manuscript pages or reproduced model-verification campaign.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** manual reference-model design and validation

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH2319&sess=sess166

**Hardware or process assumptions:** Functional hardware-verification flow with LLM generation and validation; RTL complexity, simulator, model checker, and compute environment are unspecified.

**Limits:** The description omits functional-equivalence rate, defect escape rate, human correction effort, prompt/model versions, and design distribution.

Generation speed does not establish verification adequacy or correctness without independent oracle checks.

Official description only; LLM verification claims require artifact and failure-case review.

**Method or artifact:** LLM-assisted hierarchical reference-model generation with standardized design representations and reusable building blocks.

**Metrics:** Up to 58.99% performance improvement

9.18x generation capacity increase

7.11x acceleration of design and validation cycles

300 evaluated designs

**Problem:** Reference-model development for functional IC verification becomes a major bottleneck as designs grow more complex and requires repeated expert effort.

**Workload or benchmark:** 300 diverse hardware designs compared with manual reference-model development; design languages, model correctness criteria, hardware platforms, and human baseline process are unspecified.

</details>

<span id="paper-dac-2026-research2880"></span>

### Uvmarvel: an Automated LLM-Aided UVM Machine for Subsystem-Level RTL Verification

DAC 2026 · Record: `dac-2026-research2880`

[Read the step-by-step explanation](#explanation-dac-2026-research2880)

**Updated source-backed reading card**

Reviewed 2026-09-08. Deepens the existing UVMarvel treatment into a paper-level reading; separates IR/protocol-library UVM construction, signal tracking and Verilog patching from stimulus quality, functional coverage, oracle validity, escaped bugs and human-cost accounting, preserves the 95.65% code-coverage and 4.5-hour claims, and defines the verification evidence boundary.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Subsystem-level UVM testbench construction and high-quality stimulus generation require manual coding, repeated EDA runs and deep protocol/micro-architectural expertise.

**Mechanism / artifact:**

LLM-aided UVM generation using an intermediate representation, bus-protocol library, signal tracker and Verilog patching loop for stimulus refinement; transaction constraints, scoreboards, assertions, coverage bins, patch acceptance and oracle are unspecified.

**Workload — the work tested:**

Subsystem RTL across mainstream bus protocols; designs, protocol versions, legal/illegal sequences, state/concurrency cases, coverage denominators, simulator settings, design split and manual baseline process are unspecified.

**Hardware and manufacturing assumptions:**

RTL/UVM verification environment with protocol specifications and EDA simulation; target subsystem scale, RTL language, simulator/tools/licenses, compute, waveform policy, reference model and reviewer assumptions are unspecified.

**Baseline — the comparison method:**

Manual UVM testbench construction and stimulus refinement

Same RTL, protocol specification, simulator, seeds, licenses, compute, coverage targets, correctness oracle, review standard and end-to-end time boundary are unspecified

**Reported measurements:**

The official description reports 95.65% average code coverage and 4.5-hour automated execution instead of several human working days; it supplies no functional/assertion/toggle/branch coverage, unique bugs, seeded-fault detection, escaped defects, false alarms, triage time, protocol breakdown or cost accounting.

**Limits on the conclusion:**

Specify protocols, legal/illegal transactions, backpressure, ordering, bursts, reset/error behavior, concurrency and state coverage. Separate code, toggle, branch, assertion, functional and scenario coverage, and report unique bugs, seeded-fault detection, escapes, false alarms, duplicates and triage time.

Compare manual and automated flows with matched RTL, specifications, simulators, seeds, licenses, compute, coverage and review. Include normalization, prompts/model execution, compilation, simulation, traces, patching, debugging, scoreboard repair and expert review in the 4.5-hour boundary; test unseen subsystem structures and protocols.

The 95.65% code-coverage and 4.5-hour claims lack coverage denominators, functional results, bug yield, escaped defects, protocol/state distribution, resources and baseline accounting. The evidence supports automated subsystem-UVM construction and stimulus refinement, not demonstrated verification completeness or reduced escaped-bug risk.

**Source and location**

Evidence tier: Primary captured DAC official description plus existing chapter level conceptual discussion; no full paper extraction, generated testbench corpus, coverage trace or independent verification review. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH2880&sess=sess164)

DAC 2026 official description; existing chapter-level simulation/testing discussion; captured Problem, Mechanism / artifact, Workload, Hardware, Baseline, Measurements and Limits fields; no manuscript pages or reproduced UVM campaign.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** manual UVM testbench construction and stimulus refinement

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH2880&sess=sess164

**Hardware or process assumptions:** RTL/UVM verification environment with protocol specifications and EDA simulation; target subsystems, testbench scale, and compute resources are unspecified.

**Limits:** Code coverage is not functional coverage or bug detection; the description omits escaped defects, coverage closure, and generated-test quality.

Execution time depends on design size, simulator/license resources, and human review assumptions.

Official description only; verification claims require reproducible benchmark and oracle analysis.

**Method or artifact:** LLM-aided UVM generation using an intermediate representation, bus-protocol library, signal tracker, and Verilog patching loop.

**Metrics:** 95.65% average code coverage

4.5-hour automated execution

Several human working days for comparable manual effort

**Problem:** Subsystem-level UVM testbench construction and stimulus generation require extensive manual coding, repeated EDA runs, and protocol expertise.

**Workload or benchmark:** Subsystem RTL across mainstream bus protocols; designs, coverage methodology, functional coverage, simulator/tool versions, and manual baseline effort are unspecified.

</details>

<span id="paper-dac-2026-research2011"></span>

### Dart: Towards Redundancy-Free RTL Simulation via DAG-Driven Execution

DAC 2026 · Record: `dac-2026-research2011`

[Read the step-by-step explanation](#explanation-dac-2026-research2011)

**Updated source-backed reading card**

Reviewed 2026-09-08. Deepens the existing Dart treatment into a paper-level reading; separates DAG construction, sub-DAG merging, shared execution and state reconstruction from event-semantic correctness, waveform/debug observability, stimulus-diversity scaling and resource accounting, preserves the 136.7x and 4.1x claims, and defines the evidence boundary.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

RTL simulation redundantly recomputes identical internal states across stimuli, limiting scalability as SoC complexity grows.

**Mechanism / artifact:**

DAG-driven RTL intermediate representation, cross-stimulus sub-DAG merging, shared computation execution and per-stimulus state reconstruction; event semantics, supported RTL constructs, merge conditions and debug representation are unspecified.

**Workload — the work tested:**

Multiple-stimulus RTL simulation across industrial designs; design identities, stimulus count/similarity/divergence, clocks/resets, assertions, waveform policy, semantic coverage and correctness checks are unspecified.

**Hardware and manufacturing assumptions:**

Pre-silicon RTL simulation on CPU/GPU or custom execution engine; simulator semantics, event scheduler, memory, trace storage, compile cache, parallelism and hardware are unspecified.

**Baseline — the comparison method:**

Conventional per-stimulus CPU simulation

GPU batch-parallel RTL simulators

RTLflow

Same RTL, stimuli, seeds, resets, waveform policy, compile cache, hardware, assertions, trace and correctness boundary are unspecified

**Reported measurements:**

The official description reports up to 136.7x speedup over Verilator and 4.1x over RTLflow on industrial RTL, with per-stimulus correctness claimed; it supplies no runtime baseline, design/stimulus counts, sharing ratio, memory, trace/debug cost, unsupported constructs, mismatch rate or semantic coverage.

**Limits on the conclusion:**

Compare outputs and relevant internal state cycle by cycle against a trusted event-accurate reference with identical stimuli, clocks, resets, unknown-value and assertion rules. Test delta cycles, nonblocking assignments, X/Z, memories, interrupts, backpressure, asynchronous events and divergence; report mismatches, unsupported constructs and reconstruction failures.

Measure DAG construction/merge, sharing, memory, scheduling, synchronization, trace storage and debug localization. Vary stimulus similarity, count, order and divergence; compare CPU, GPU and RTLflow with matched RTL, waveforms, cache, hardware and checks.

The 136.7x and 4.1x claims lack design/stimulus, semantic, memory, trace/debug and feature-support conditions. The evidence supports cross-stimulus redundancy elimination, not demonstrated event-semantic equivalence or universal RTL simulation acceleration.

**Source and location**

Evidence tier: Primary captured DAC official description plus existing chapter level conceptual discussion; no full paper extraction, event semantic trace, waveform equivalence or independent simulator reproduction. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH2011&sess=sess164)

DAC 2026 official description; existing chapter-level simulation/testing discussion; captured Problem, Mechanism / artifact, Workload, Hardware, Baseline, Measurements and Limits fields; no manuscript pages or reproduced Dart simulator.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** conventional per-stimulus CPU simulation

GPU batch-parallel RTL simulators

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH2011&sess=sess164

**Hardware or process assumptions:** Pre-silicon RTL simulation on CPU/GPU or custom execution engine; simulator semantics, memory, and event scheduling details are unspecified.

**Limits:** The description omits runtime, memory overhead, event-semantic coverage, stimulus diversity, and numerical comparison.

DAG merging may be limited by divergent state or timing semantics.

Official description only; simulator correctness and performance require artifact verification.

**Method or artifact:** DAG-driven intermediate representation, sub-DAG merging, shared computation execution, and lightweight state reconstruction.

**Metrics:** Cross-stimulus redundancy elimination claimed

Per-stimulus correctness preservation claimed

**Problem:** RTL simulation redundantly recomputes identical internal states across stimuli, limiting scalability as SoC complexity grows.

**Workload or benchmark:** Multiple-stimulus RTL simulation; circuit suite, stimulus count, correctness checks, and speedup metrics are unspecified.

</details>

<span id="paper-dac-2026-research1813"></span>

### RL4HDL: Code Diversity Guided FPGA Logic Synthesis Compiler Testing Via Reinforcement Learning

DAC 2026 · Record: `dac-2026-research1813`

[Read the step-by-step explanation](#explanation-dac-2026-research1813)

**Updated source-backed reading card**

Reviewed 2026-09-08. Deepens the RL4HDL treatment into a paper-level reading; separates reinforcement-learning/code-diversity-guided test generation from compiler correctness, oracle quality, coverage, defect deduplication, false positives and campaign cost, while preserving the three-month, 20-defect and 12-new-defect claims.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

FPGA logic-synthesis compilers translate RTL to gate-level netlists, so compiler defects can compromise final hardware; existing tests may be redundant and fail to explore diverse defect-triggering programs.

**Mechanism / artifact:**

Reinforcement-learning generator guided by HDL code diversity for logic-synthesis compiler testing; state/action representation, reward, mutation or generation operators, compiler oracle, minimization and defect triage are unspecified.

**Workload — the work tested:**

HDL programs tested against an FPGA logic-synthesis compiler over a three-month campaign; RTL subset, language constructs, tool versions, target FPGA families, compiler configurations, seeds, test budget and baseline campaigns are unspecified.

**Hardware and manufacturing assumptions:**

FPGA synthesis compiler producing gate-level netlists with simulation, equivalence or other correctness oracles; target devices, synthesis libraries, optimization settings, simulator/formal tools, compute and campaign infrastructure are unspecified.

**Baseline — the comparison method:**

Random HDL fuzzing

Mutation-based compiler testing

Existing regression suite

Same RTL language subset, compiler version/configuration, oracle, seeds, time/compute budget, minimization, deduplication and developer-confirmation protocol are unspecified

**Reported measurements:**

The official description reports a three-month campaign that discovered 20 unique defects, including 12 previously unreported defects, all confirmed by official developers; it supplies no coverage, time-to-first-failure, baseline defect yield, false-positive/duplicate rate, defect severity, tool version or test-distribution result.

**Limits on the conclusion:**

A generated HDL program is valuable only if it reaches a meaningful compiler path and has an independent oracle. Check RTL parse/elaboration, synthesized netlist validity, simulation or formal equivalence, timing/width semantics and optimization-preserving behavior; separate compiler crashes, rejected inputs, miscompilations, nondeterminism and infrastructure failures.

Count unique root-cause defects rather than test failures or stack traces. Report valid-input execution rate, code/state/feature coverage, mutation and diversity metrics, duplicate and false-positive rates, time to first confirmed defect, minimization effort, severity and developer confirmation under a fixed campaign budget.

The three-month, 20-defect and 12-new-defect claims lack tool versions, RTL subset, baselines, coverage, oracle, deduplication, false-positive and cost conditions. The evidence supports RL-guided HDL compiler testing, not demonstrated synthesis correctness coverage or a general defect-detection advantage.

**Source and location**

Evidence tier: Primary captured official DAC description plus existing authored chapter level explanation; no full paper extraction, tool version matrix, coverage report or independent defect reproduction. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH1813)

DAC 2026 official description; existing chapter-level simulation-emulation-and-testing discussion; captured Problem, Mechanism / artifact, Workload, Hardware, Baseline, Measurements and Limits fields; no manuscript pages or reproduced compiler-testing campaign.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** random HDL fuzzing

mutation-based compiler testing

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH1813

**Hardware or process assumptions:** FPGA logic-synthesis compiler flow with simulation or equivalence oracles; target families are unspecified.

**Limits:** No coverage, unique bugs, false positives, or time-to-failure results are reported.

Reward design may bias discovered failure classes.

Official description only; testing claims require reproducible tool campaigns.

**Method or artifact:** Reinforcement-learning generator guided by HDL code diversity for FPGA synthesis testing.

**Metrics:** Test diversity and bug-finding efficiency are claimed qualitatively

**Problem:** Compiler testing needs diverse HDL programs that expose synthesis correctness and robustness failures.

**Workload or benchmark:** HDL compiler test programs; tool versions, oracles, and baselines are unspecified.

</details>

<span id="paper-dac-2026-research358"></span>

### Lyra: A Hardware-Accelerated RISC-V Verification Framework with Generative Model-Based Processor Fuzzing

DAC 2026 · Record: `dac-2026-research358`

[Read the step-by-step explanation](#explanation-dac-2026-research358)

**Updated source-backed reading card**

Reviewed 2026-09-08. Deepens the Lyra treatment into a paper-level reading; separates FPGA-SoC differential execution and LyraGen semantic instruction generation from ISA/oracle completeness, architectural coverage, bug confirmation, hardware/software comparability and campaign cost, while preserving the 1.27x, 107x–3343x and convergence claims.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Processor verification is limited by slow software simulation and shallow random instruction mutations that converge slowly on complex architectural behaviors.

**Mechanism / artifact:**

Heterogeneous RISC-V verification framework executing the DUT and reference model concurrently on an FPGA SoC for differential checking and hardware-level coverage, paired with ISA-aware generative model LyraGen for semantically rich instruction sequences; core interface, model training, coverage probes and oracle details are unspecified.

**Workload — the work tested:**

RISC-V processor cores and instruction-sequence campaigns; core implementations, ISA/extensions, privilege modes, memory model, boot/runtime environment, sequence length, seeds, coverage definitions, campaign duration and baseline fuzzer settings are unspecified.

**Hardware and manufacturing assumptions:**

FPGA-SoC hardware verification/emulation platform with DUT and reference model running concurrently; FPGA/device, clock, host interface, memory, trace storage, reset/debug infrastructure, software simulator and target-core implementation are unspecified.

**Baseline — the comparison method:**

Random instruction fuzzing

Software-only processor simulation/fuzzing

Mutation-based instruction generators

Same RISC-V core, ISA/extensions, reference oracle, coverage probes, seeds, campaign time, FPGA/host resources, tracing and triage boundary are unspecified

**Reported measurements:**

The official description reports up to 1.27x higher coverage and 107x–3343x end-to-end verification acceleration versus state-of-the-art software fuzzers, with lower convergence difficulty; it supplies no coverage denominator, absolute throughput, unique confirmed bugs, false positives, oracle failures, core distribution or hardware conditions.

**Limits on the conclusion:**

Differential checking is only as strong as the reference model and synchronization. Validate architectural state, memory ordering, exceptions, interrupts, privilege transitions, CSR behavior, atomics, MMU/cache behavior and nondeterminism against an independent oracle; report mismatches, reset/debug failures and unsupported ISA features.

Generative semantic awareness can improve common instruction sequences while missing rare privilege, concurrency, memory-system or extension interactions. Report instruction/edge/state/functional coverage, cross-core and cross-extension holdouts, sequence diversity, time to first confirmed failure, duplicate/false-positive rates and minimized reproductions.

The 1.27x, 107x–3343x and convergence claims lack core/ISA details, coverage denominator, absolute throughput, campaign conditions, oracle, bug confirmation and hardware/software cost accounting. The evidence supports FPGA-accelerated ISA-aware RISC-V fuzzing, not demonstrated verification completeness or general processor correctness coverage.

**Source and location**

Evidence tier: Primary captured official DAC description plus existing authored chapter level explanation; no full paper extraction, core/isa coverage matrix, independent oracle audit or reproduced differential fuzzing campaign. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH358&sess=sess164)

DAC 2026 official description; existing chapter-level simulation-emulation-and-testing discussion; captured Problem, Mechanism / artifact, Workload, Hardware, Baseline, Measurements and Limits fields; no manuscript pages or reproduced FPGA-SoC campaign.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** random instruction fuzzing

software-only processor simulation

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH358

**Hardware or process assumptions:** RISC-V hardware verification/emulation platform; accelerator architecture and target extensions are unspecified.

**Limits:** No coverage, bugs found, throughput, or false-positive results are reported.

Generative fuzzing may miss rare architectural corner cases.

Official description only; claims require long-run and cross-core campaigns.

**Method or artifact:** Hardware-accelerated RISC-V verification framework with generative fuzzing.

**Metrics:** Verification throughput and bug discovery are claimed qualitatively

**Problem:** Processor verification needs high-throughput, semantically diverse instruction streams that uncover architectural and implementation bugs.

**Workload or benchmark:** RISC-V cores and instruction sequences; cores, oracles, coverage, and baselines are unspecified.

</details>

<span id="paper-dac-2026-research1348"></span>

### TOB-Sched: Topological Order Balancing-Driven Static Scheduling for Processor-Based Emulation

DAC 2026 · Record: `dac-2026-research1348`

[Read the step-by-step explanation](#explanation-dac-2026-research1348)

**Updated source-backed reading card**

Reviewed 2026-09-09. Deepens the TOB-Sched treatment into a paper-level reading; separates topological-order balancing and O(1) gain computation from cycle-accurate emulation semantics, communication latency, resource utilization, makespan, hardware constraints and workload transfer, while preserving the reported 72%, 22.5% and 55% claims.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Processor-based emulation maps a netlist computation graph onto processors whose execution order and communication latency determine the simulated time step; poorly balanced static schedules leave resources idle and lengthen emulation.

**Mechanism / artifact:**

TOB-Sched: topological-order balancing-driven static scheduling with mobility-prioritized node selection, forward/backward propagation and a theorem reducing gain-calculation time to O(1); node allocation, dependency semantics, communication model, resource constraints, tie-breaking and schedule repair are unspecified.

**Workload — the work tested:**

Processor-based emulation of public/open-source chip netlist benchmarks; graph sizes, node types, processor count, mapping, interconnect topology/latency, memory, clock, fanout, benchmark identities and schedule baseline settings are unspecified.

**Hardware and manufacturing assumptions:**

Static processor-based emulation platform with allocated graph nodes and inter-processor communication; processor/FPGA/host hardware, network, memory, clock, synchronization, instruction model, runtime, resource capacities and emulation instrumentation are unspecified.

**Baseline — the comparison method:**

List scheduling

Unbalanced topological scheduling

SOTA scheduling algorithm

Same netlists, node allocation, processor count, interconnect latency, memory, resource constraints, clock, seeds, schedule construction and emulation measurement boundary are unspecified

**Reported measurements:**

The official description reports 72% improvement in the topological-order-balancing (TOB) metric, 22.5% fewer time steps and 55% faster runtime than the SOTA scheduling algorithm on public/open-source chip benchmarks; it reports no absolute makespan, emulation throughput, utilization, communication volume, memory, scale, hardware or functional-equivalence result.

**Limits on the conclusion:**

TOB is a graph-order metric, not automatically a cycle-accurate emulation result. Define topological order, mobility, gain, time step, dependency readiness, instruction execution, communication latency, synchronization and resource capacity; replay schedules with a cycle-accurate or hardware-backed emulator and check functional equivalence, deadlock, ordering and state-update semantics.

A static schedule can optimize the measured graph while becoming brittle under different mappings, processor counts, communication delays, memory pressure or workload phases. Report makespan, processor utilization, idle time, communication bytes/stalls, memory use, critical path, schedule-construction time, emulation throughput and per-benchmark results across graph scales and hardware configurations.

The official description reports 72% better TOB, 22.5% fewer time steps and 55% faster runtime, but omits metric definitions, absolute results, benchmark/graph conditions, processor/interconnect settings, utilization, memory, functional validation and hardware emulation evidence. The evidence supports topological-order-balanced static scheduling, not demonstrated cycle-accurate PBE throughput or transferable emulation efficiency.

**Source and location**

Evidence tier: Primary captured official DAC description plus existing authored simulation/emulation discussion; no full paper extraction, graph scale/processor matrix, reproduced schedule or independent pbe validation. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH1348&sess=sess164)

DAC 2026 official description; existing simulation-emulation-and-testing chapter discussion; captured Problem, Mechanism / artifact, Workload, Hardware, Baseline, Measurements and Limits fields; no manuscript pages, schedule trace, cycle-accurate replay or hardware-emulation validation.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** list scheduling

unbalanced topological scheduling

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH1348

**Hardware or process assumptions:** Processor-based emulation platform with static task assignment; interconnect and memory assumptions are unspecified.

**Limits:** No throughput, utilization, makespan, memory, or graph-scale results are reported.

Static schedules may be brittle under workload variation.

Official description only; hardware-emulation validation is required.

**Method or artifact:** Topological-order balancing-driven static scheduler.

**Metrics:** Emulation scheduling efficiency is claimed qualitatively

**Problem:** Processor-based emulation needs balanced schedules to avoid idle resources and long critical paths.

**Workload or benchmark:** Hardware emulation task graphs; processor array, graph scale, and baselines are unspecified.

</details>

<span id="paper-dac-2026-research1858"></span>

### Reflectbench: An Agentic Framework for Generating System-Level Design Testbench via Consensus and Reflection

DAC 2026 · Record: `dac-2026-research1858`

[Read the step-by-step explanation](#explanation-dac-2026-research1858)

**Updated source-backed reading card**

Reviewed 2026-09-09. Deepens the ReflectBench treatment into a paper-level reading; separates logic analysis, consensus validation, self-reflection, testbench correction and self-reflective domain-knowledge mining from oracle independence, bug detection, coverage semantics, correlated errors, human review and system-level generalization, while preserving the ReflectVDB/AutoBench and 7.6%/4.5%/3.8%/1.2% claims.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

System-level hardware verification requires tests that exercise interactions across modules, protocols, state and timing, but manually constructing those testbenches is labor-intensive. LLM-generated testbenches can also share misunderstandings or compensating errors with the reference design, creating false-positive verification outcomes.

**Mechanism / artifact:**

ReflectBench, an agentic system-level hardware-testbench generation framework combining logic analysis, consensus-based validation, feedback self-reflection and testbench self-correction; Self-Reflective Domain Knowledge Mining builds a retrieval database aligned with hardware semantics, and ReflectVDB provides 53 system-level hardware designs for evaluation. Agent roles, logic representation, oracle independence, correction stopping rule, retrieval contents and simulator/tool flow are unspecified.

**Workload — the work tested:**

System-level RTL/design verification evaluated on the ReflectVDB benchmark of 53 hardware designs and the AutoBench dataset; design families, interfaces, protocols, fault/bug set, specification quality, train/test split, simulator, test budget, seeds and whether designs or knowledge overlap with development data are unspecified.

**Hardware and manufacturing assumptions:**

Executable RTL/system simulation with a generated testbench and reference design or checking oracle; HDL language, simulator, compilation environment, assertions/coverage instrumentation, compute/model versions, retrieval database construction, licenses, runtime and human review process are unspecified.

**Baseline — the comparison method:**

ConfiBench

Manual testbench construction

Single-agent or non-reflective LLM testbench generation

Same designs, specification, simulator, model/tool versions, generation budget, test execution budget, coverage definition, oracle, human review and end-to-end time boundary are unspecified

**Reported measurements:**

The official description reports that ReflectBench improves testbench generation success rate over ConfiBench by 7.6% on ReflectVDB and 4.5% on AutoBench, and improves coverage rate by 3.8% and 1.2%, respectively; it does not define success/coverage denominators, confirmed bug yield, false positives, compilation rate, test execution, runtime, human effort, escaped violations or independent-oracle validation.

**Limits on the conclusion:**

A generated testbench is useful only if its stimulus reaches meaningful system interactions and its checker is independent enough to expose violations. Define legal and adversarial transactions, clocks/resets, protocol ordering, scoreboards, assertions, reference-model provenance, coverage bins and the bug/violation oracle. Compare generated and trusted outputs against an independently specified behavior, and report compilation failures, duplicate tests, false alarms, confirmed seeded faults, escaped bugs and failure-triage effort. Agreement between a generated testbench and a correlated reference can be a false positive.

Consensus and reflection can improve consistency while amplifying a shared model or specification error. Expose agent prompts/roles, candidate count, consensus rule, retrieval context, self-critique and repair loop, stopping criterion, stochastic seeds and human intervention. Ablate logic analysis, consensus, reflection, self-correction and domain-knowledge retrieval under the same generation and simulation budget; success rate without the correction cost does not establish verification value.

ReflectVDB's 53 designs and AutoBench comparison need explicit design families, splits, system complexity, protocols, simulator versions, coverage definitions and overlap controls. Test unseen designs, specifications, protocol combinations and seeded or real bugs, and separate code/toggle/functional/assertion coverage from confirmed defect detection. A higher coverage number can reflect easier stimulus or a weaker denominator rather than better system verification.

The official description reports open-source ReflectBench/ReflectVDB and the 7.6%, 4.5%, 3.8% and 1.2% improvements over ConfiBench, but omits oracle independence, bug yield, false-positive rate, coverage denominator, compilation/runtime, human review and generalization conditions. The evidence supports agentic system-level testbench generation, not demonstrated reduction in escaped hardware bugs or independent verification completeness.

**Source and location**

Evidence tier: Primary captured official DAC description plus existing authored testbench/oracle discussion; no full paper extraction, reproduced reflectvdb run, fault injection study or independent review. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH1858&sess=sess166)

DAC 2026 official description; existing simulation-emulation-and-testing chapter framing; captured Problem, Mechanism / artifact, Workload, Hardware, Baseline, Measurements and Limits fields; no manuscript pages, benchmark manifest, generated-test trace or independent bug-detection validation.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** manual testbench writing

single-agent test generation

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH1858

**Hardware or process assumptions:** RTL/system simulation environment with executable testbench oracles; design scale is unspecified.

**Limits:** No coverage, bug finds, compilation rate, runtime, or false-positive results are reported.

Consensus can amplify shared agent errors.

Official description only; independent design validation is required.

**Method or artifact:** Agentic testbench-generation framework with consensus and reflection.

**Metrics:** Testbench quality and coverage are claimed qualitatively

**Problem:** System-level testbench creation is labor-intensive and must cover interactions beyond unit-level tests.

**Workload or benchmark:** System-level hardware designs and specifications; agents, simulators, and baselines are unspecified.

</details>

<span id="paper-dac-2026-research2760"></span>

### Notsotiny: A Large, Living Benchmark for RTL Code Generation

DAC 2026 · Record: `dac-2026-research2760`

[Read the step-by-step explanation](#explanation-dac-2026-research2760)

**Updated source-backed reading card**

Reviewed 2026-09-08. Reconciles the official benchmark card with arXiv version 1 and the pinned evaluator assessment; separates contextual RTL completion from unconstrained chip design, benchmark construction from model capability, and formal proof from timeout or partial coverage.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

RTL-generation benchmarks can overstate model capability when tasks are small or repetitive, verification is weak, contamination is not examined, and a fixed public collection becomes familiar.

**Mechanism / artifact:**

NotSoTiny builds a living contextual RTL module-completion benchmark from TinyTapeout designs, deduplicates candidates, filters for compatibility with its verification flow, checks outputs with simulation and Yosys formal-equivalence procedures, and uses comparative Min-K analysis to examine possible training exposure.

**Workload — the work tested:**

Contextual RTL module completion; 3,062 deduplicated tasks are reduced to 1,114 after compatibility filtering. Comparative contamination analysis covers 11 models; reference-only inputs are used and modules over 2,000 tokens are excluded.

**Hardware and manufacturing assumptions:**

RTL and Yosys evaluation flow; `equiv_simple` and `equiv_induct` with k=30 are reported. Exact Yosys/solver versions, reset and initialization assumptions, model prompts, dataset revision and per-task run outcomes require source reconciliation.

**Baseline — the comparison method:**

Earlier RTL-generation benchmarks

Comparative evaluation across 11 language models

Yosys simulation/formal-equivalence checking

**Reported measurements:**

3,062 deduplicated tasks before compatibility filtering

1,114 compatibility-filtered tasks

Formal-equivalence coverage under k=30, with partition coverage distinct from full equivalence

Comparative Min-K contamination analysis across 11 models

**Limits on the conclusion:**

Filtering for verifier compatibility can change the task population; excluded-task characteristics are needed before generalizing to community RTL.

A pinned evaluator path records a 900-second timeout through the equivalence-success aggregation field; this source-level finding does not measure published-score inflation, but proof, timeout, unproven and tool-error outcomes must be separated before accepting a correctness rate.

Min-K similarity is a contamination probe, not proof of training-set exclusion. A refreshed benchmark is not a comparable time series unless its revision, split, filtering rules and evaluator remain fixed or are explicitly reconciled.

Contextual module completion is not unconstrained specification-to-chip generation. No independent artifact execution, full per-task result reconciliation or independent review was performed.

**Source and location**

Evidence tier: Primary arxiv preprint v1, official DAC description and read only pinned evaluator inspection; no artifact execution or independent acceptance. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://arxiv.org/pdf/2512.20823v1)

Version 1: Section 2.4 for deduplication and compatibility filtering (3,062 to 1,114); Section 3 for comparative Min-K contamination analysis across 11 models and token-length condition; Section 4.2 for Yosys `equiv_simple`/`equiv_induct`, k=30 and partition coverage; pinned TuRTLe evaluator `run_equivalence_check` at commit 6a32467e79d7a6cfbf3a6c579c24f20662475101, including timeout aggregation; DAC official record https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH2760&sess=sess166.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** primary_author_preprint

**Baselines:** prior RTL benchmarks

comparative LLM evaluations across 11 models

**Evidence locators:** DAC 2026 official description

arXiv S2.4

arXiv S3

arXiv S4.2

pinned TuRTLe evaluator run_equivalence_check

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH2760&sess=sess166

**Hardware or process assumptions:** RTL generation and Yosys formal/simulation tooling; exact solver versions, reset assumptions, model identities, hardware, and per-task run outcomes are not exposed in the public description.

**Limits:** Compatibility filtering may select for verifier tractability; excluded-task characteristics are needed before generalizing.

A pinned evaluator path counts a 900-second timeout as equivalence success, so proof, timeout, unproven, and tool-error outcomes must be separated before accepting scores.

The dataset loads a 25-12 revision without an explicit revision argument; repository pinning does not alone pin dataset contents.

Comparative memorization signals are not proof of training-set exclusion, and live benchmark scores are not temporal progress without version matching.

No artifact execution or independent review was performed.

**Method or artifact:** Living RTL benchmark with compatibility filtering, simulation/formal-equivalence verification, structurally rich contextual tasks, and contamination-oriented dataset maintenance.

**Metrics:** 3,062 deduplicated tasks before compatibility filtering

1,114 filtered tasks

formal-equivalence coverage under k=30

comparative Min-K contamination analysis

**Problem:** RTL-generation benchmarks can be trivial, weakly verified, contaminated, and too static to measure realistic design capability.

**Workload or benchmark:** Contextual module-completion tasks; compatibility filtering reduces 3,062 deduplicated tasks to 1,114; Yosys equiv_simple and equiv_induct with k=30 are reported, but partition coverage is partial credit rather than full equivalence.

</details>

#### Additional source assessment

This separately recorded check is dated 2026-09-06. It supplements the original record above and retains its own scope and uncertainty.

[Assessment record](../../dac/data/notsotiny-primary-assessment-v1.json)

[Assessed source](https://arxiv.org/html/2512.20823v1)

**Extraction scope**

Selected preprint sections and read-only pinned evaluator/task inspection; no table transcription or artifact execution

**Conditions**

**Task:** Contextual module completion, not unconstrained specification-to-chip design

**Selection:** Section 2.4: self-equivalence compatibility filtering reduces 3062 deduplicated tasks to 1114.

**Verification:** Section 4.2: Yosys equiv_simple and equiv_induct; reported k=30. Partition coverage is partial credit, distinct from full equivalence.

**Contamination:** Section 3: comparative Min-K across 11 models; reference-only inputs, modules over 2000 tokens excluded, no binary contamination threshold.

**Headline metric status**

withheld_pending_verifier_and_evaluation_reconciliation

**Independent review status**

pending

<span id="paper-dac-2026-research1180"></span>

### ESCAPE: Elegant Scan Chain Activity Probability Establishment for Programmable Low-Power LBIST

DAC 2026 · Record: `dac-2026-research1180`

[Read the step-by-step explanation](#explanation-dac-2026-research1180)

**Updated source-backed reading card**

Reviewed 2026-09-09. Deepens the ESCAPE treatment into a paper-level reading; separates programmable per-chain scan activity control and probability generation from fault coverage, peak-power measurement, pattern quality, test-time overhead and silicon/tester validity, while preserving the qualitative industrial-scale claim without inventing numbers.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Logic built-in self-test must create enough scan activity to detect faults without exceeding peak-power limits; suppressing transitions can reduce stress while also hiding faults or changing the test distribution.

**Mechanism / artifact:**

ESCAPE is described as a programmable low-power LBIST architecture that periodically generates user-configurable probability sequences, drives hold registers, combines two hold-register groups with a 2D AND-gate array and modulates enable probability before the phase shifter for per-chain power control; pattern generation, phase-shifter timing, probability resolution, seed/repeat behavior and control overhead are unspecified.

**Workload — the work tested:**

Industrial-scale digital designs evaluated with scan chains and LBIST patterns; circuit sizes, scan architecture, number of chains, fault model, test length, pattern seeds, frequency, compression, transition constraints, coverage denominator and compared pattern generators are unspecified.

**Hardware and manufacturing assumptions:**

Scan-based production-test infrastructure with programmable pattern generation, hold registers, phase shifters and an activity-control circuit; process node, library, voltage/frequency, tester/ATE, on-chip measurement, clocking, area/timing/power instrumentation and manufacturing assumptions are unspecified.

**Baseline — the comparison method:**

Uncontrolled LBIST patterns

Conventional low-power test generation

Same scan chains, fault model, test length, clock/voltage, pattern budget, compression, tester and power/coverage accounting are unspecified

**Reported measurements:**

The official description claims high fault coverage, reduced peak power and lower hardware overhead on industrial-scale designs, but reports no fault-coverage percentage, peak/average power, pattern count or test time, area/timing overhead, per-design result, fault distribution, measurement method or silicon validation.

**Limits on the conclusion:**

Activity probability is not fault coverage. Define the transition/fault distribution, scan observability, phase-shifter and capture behavior, then compare detected, undetected, redundant and masked faults against an uncontrolled or conventional pattern set at the same test length. A lower toggle probability can reduce peak power while making rare sensitization sequences less likely.

Per-chain probability control must be evaluated at the actual shift and capture clocks, voltage/frequency and tester timing. Measure peak—not only average—power, IR-drop or supply disturbance where relevant, thermal behavior, pattern generation/control area, timing, seed storage, configuration bandwidth and test-time overhead. Include probability programming, hold-register and 2D-array switching in the power boundary.

The description's industrial-scale claim does not establish portability across scan architectures, process nodes, fault models or manufacturing test conditions. Report coverage by fault class and design, power distributions and worst cases, pattern convergence and repeated seeds; compare identical compression, test budget, ATE conditions and diagnosis rules. The evidence supports programmable low-power LBIST activity shaping, not demonstrated quantitative fault-coverage preservation, peak-power reduction or silicon production-test benefit.

**Source and location**

Evidence tier: Primary captured official DAC description plus existing authored testing discussion; no full paper extraction, reproduced lbist pattern campaign, fault model matrix or measured production test validation. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH1180)

DAC 2026 official description; existing simulation-emulation-and-testing chapter framing; captured Problem, Mechanism / artifact, Workload, Hardware, Baseline, Measurements and Limits fields; no manuscript pages, fault-coverage table, power trace or silicon/ATE validation.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** uncontrolled LBIST patterns

conventional low-power test generation

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH1180

**Hardware or process assumptions:** Scan-based test infrastructure with programmable pattern generation; process and tester assumptions are unspecified.

**Limits:** No fault coverage, peak power, test time, area, or pattern results are reported.

Activity shaping may reduce detection of some faults.

Official description only; fault-model and silicon validation are required.

**Method or artifact:** Programmable scan-chain activity-probability control for low-power LBIST.

**Metrics:** LBIST power and coverage are claimed qualitatively

**Problem:** Logic built-in self-test must balance transition activity, power, and fault coverage.

**Workload or benchmark:** Digital circuits and LBIST patterns; fault models, scan architecture, and baselines are unspecified.

</details>

<span id="paper-dac-2026-research2085"></span>

### Prelude: Priming-Guided State Reconstruction for Efficient FPGA Processor Debugging

DAC 2026 · Record: `dac-2026-research2085`

[Read the step-by-step explanation](#explanation-dac-2026-research2085)

**Updated source-backed reading card**

Reviewed 2026-09-09. Deepens the Prelude treatment into a paper-level reading; separates essential architectural-state/memory snapshots and replay visibility warm-up from microarchitectural-state fidelity, nondeterminism, external events, trace/storage cost and bug-localization validity, while preserving the BOOM/Rocket and DESSERT/ENCORE speedup claims with their missing conditions.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

FPGA prototypes expose limited internal signals, while continuous tracing consumes bandwidth and storage and heavyweight snapshots slow execution; debugging needs enough state to reconstruct a cycle-accurate explanation without perturbing the prototype excessively.

**Mechanism / artifact:**

Prelude is described as a lightweight snapshot-based debugging framework that records essential architectural state and processor memory footprint, then uses a short replay visibility warm-up or priming phase to reconstruct internal microarchitectural state for cycle-accurate analysis; snapshot schema, priming inputs, reconstruction algorithm, trace instrumentation, memory consistency, nondeterminism handling and stopping/coverage criteria are unspecified.

**Workload — the work tested:**

FPGA processor prototype executions on BOOM and Rocket with debug/replay traces; core revisions, workloads, boot/OS, memory sizes, peripherals, interrupts, external I/O, trace duration, bug set, snapshot interval, replay determinism and visibility targets are unspecified.

**Hardware and manufacturing assumptions:**

FPGA implementations of BOOM and Rocket with architectural-state/memory snapshot logic, trace visibility and replay infrastructure; FPGA board/device, clocks, memory hierarchy, host link, trace bandwidth/storage, instrumentation area/timing, reset, DMA/peripheral and clock-domain assumptions are unspecified.

**Baseline — the comparison method:**

DESSERT

ENCORE

Full continuous trace capture

Snapshot-only debugging

Same FPGA core, workload, visibility target, bug/replay criterion, snapshot storage, trace link, host resources, warm-up and end-to-end debug-time boundary are unspecified

**Reported measurements:**

The official description claims comparable visibility to prior work and reports 32.88x/2191.2x speedup over DESSERT/ENCORE on BOOM and 18.09x/896.4x on Rocket, but does not report absolute replay/debug time, reconstruction error, trace bandwidth, storage, FPGA area/timing, energy, bug-localization accuracy, workload or per-case results.

**Limits on the conclusion:**

Architectural state and memory are not automatically sufficient to reconstruct microarchitectural state. Validate cycle-by-cycle registers, queues, pipelines, caches/TLBs, predictors, arbitration, stalls, exceptions, interrupts and memory ordering against a fully observed or independently instrumented reference. Report divergence time, state-error rate, missing-state classes, replay determinism and whether a reconstructed trace localizes the same bug rather than merely producing plausible signals.

Priming assumes that replay sees the same inputs and timing. Define external I/O, DMA, interrupts, timers, nondeterministic arbitration, multicore interactions, device responses, clock domains, memory initialization and snapshot consistency. Measure snapshot capture, storage, transfer, restore, warm-up, reconstruction and trace costs, plus perturbation to prototype frequency and area; a short warm-up is not a guarantee of general state convergence.

The BOOM/Rocket speedups need a matched boundary against DESSERT and ENCORE: same visibility target, workload, bug/replay criterion, trace retention, host/FPGA resources and cold/warm-start policy. Test long executions, phase changes, cache/memory pressure, interrupts, external devices and injected/real bugs, and report per-case tails and failures. The evidence supports priming-guided FPGA processor debugging, not demonstrated universal cycle-accurate reconstruction, complete bug localization or portable debug-efficiency gains.

**Source and location**

Evidence tier: Primary captured official DAC description plus existing authored FPGA debugging discussion; no full paper extraction, independent replay determinism study, bug localization validation or complete dessert/encore timing boundary. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH2085)

DAC 2026 official description; existing simulation-emulation-and-testing chapter framing; captured Problem, Mechanism / artifact, Workload, Hardware, Baseline, Measurements and Limits fields; no manuscript pages, state-divergence trace, FPGA resource table or reproduced BOOM/Rocket debug campaign.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** full trace capture

snapshot-only debugging

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH2085

**Hardware or process assumptions:** FPGA processor with trace instrumentation and reconstruction logic; observability and timing assumptions are unspecified.

**Limits:** No state error, bug-localization, trace bandwidth, storage, or runtime results are reported.

Reconstruction may fail on unobserved nondeterminism.

Official description only; hardware-debug validation is required.

**Method or artifact:** Priming-guided processor-state reconstruction.

**Metrics:** Debug efficiency and state-reconstruction quality are claimed qualitatively

**Problem:** FPGA processor debugging is constrained by limited trace storage and incomplete state visibility.

**Workload or benchmark:** FPGA processor executions and debug traces; cores, traces, and baselines are unspecified.

</details>

<span id="paper-dac-2026-research1138"></span>

### ARTEMIS: Adaptive RL Test-Time Ensemble for Model Inference in SSD Testing

DAC 2026 · Record: `dac-2026-research1138`

[Read the step-by-step explanation](#explanation-dac-2026-research1138)

**Updated source-backed reading card**

Reviewed 2026-09-09. Deepens the ARTEMIS treatment into a paper-level reading; separates RL test-case generation and test-time policy ensembling from SSD-test oracle validity, device transfer, coverage, false positives and deployment cost, while preserving the Meta/User Garbage Collection stress-task scope and qualitative high-impact-event claim.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Modern SSD controllers have complex, dynamic behavior that makes rule-based verification difficult to scale; test generation must find workload sequences that expose blocking garbage-collection behavior across changing commercial devices.

**Mechanism / artifact:**

ARTEMIS formulates SSD test-case generation as reinforcement learning for direct deployment on heterogeneous commercial devices, and ensembles policies trained under diverse workload distributions at inference time to improve robustness in non-stationary environments. State/action representation, reward, episode termination, policy aggregation, device feedback, safety limits and test-case minimization are unspecified.

**Workload — the work tested:**

Commercial SSD stress testing on Meta Garbage Collection and User Garbage Collection tasks; firmware, SSD models, NAND configuration, workload traces, queue depth, writes/reads, test budget, event definition, device count, transfer split and campaign duration are unspecified.

**Hardware and manufacturing assumptions:**

Direct access to heterogeneous commercial SSD controllers from a host tester; host platform, interface, firmware, NAND geometry, overprovisioning, temperature/wear state, reset/isolation procedure, RL compute, device safety controls and instrumentation are unspecified.

**Baseline — the comparison method:**

Conventional rule-based verification/testing

Existing SSD test generators or workload search methods

Same devices, firmware, traces, test-case budget, reset policy, event oracle, campaign duration, host resources and triage boundary are unspecified

**Reported measurements:**

The source reports that RL-driven testing discovers high-impact test cases triggering critical blocking garbage-collection events more frequently than conventional methods across Meta and User Garbage Collection tasks; it provides no event counts/rates, confidence intervals, unique-event rule, coverage, false-positive rate, time-to-event, test throughput, device damage/safety result or inference/training cost.

**Limits on the conclusion:**

A blocking garbage-collection event is only useful as a testing outcome if the event oracle distinguishes genuine device behavior from timeout, host interference, firmware logging artifacts and workload-induced normal operation. Define event severity, confirmation, deduplication, reproducibility and the relation to user-visible failure or performance impact.

A policy ensemble can improve search under the training distributions while failing on unseen SSD models, firmware, NAND states or workload phases. Hold out devices and workload families, report transfer by device and condition, measure policy disagreement and adaptation, and compare event discovery per equal test budget with random, rule-based and existing adaptive generators.

The source provides no numeric discovery advantage, coverage, latency, endurance/safety, false-positive, campaign-cost or device-diversity results. The evidence supports RL-guided SSD stress-test generation and policy ensembling, not demonstrated device-agnostic verification coverage or general SSD reliability improvement.

**Source and location**

Evidence tier: Primary captured official DAC description plus existing authored simulation and testing discussion; no full paper extraction, reproduced commercial device campaign or independent oracle validation. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH1138)

DAC 2026 official description; existing simulation-emulation-and-testing editorial explanation; captured Problem, Mechanism / artifact, Workload, Hardware, Baseline, Measurements and Limits fields; no manuscript pages, test traces, device matrix, event confirmation log or independent reproduction.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** conventional rule-based verification/testing methods

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH1138&sess=sess164

**Hardware or process assumptions:** Heterogeneous commercial SSD controllers accessed directly by the tester; firmware versions, host platform, NAND configuration, and test duration are unspecified.

**Limits:** The official description does not provide event counts, test budgets, coverage, false-positive rates, or policy-training details.

Commercial-device diversity and transfer conditions are not exposed.

Official description only; no independent reproduction.

**Method or artifact:** Reinforcement-learning test-case generation with test-time policy ensembling across workload distributions and device-agnostic deployment.

**Metrics:** More frequent discovery of critical blocking garbage-collection events is reported qualitatively; event rates, confidence intervals, and test budgets are not provided.

**Problem:** Rule-based verification does not scale to complex SSD controllers or changing commercial-device operating environments.

**Workload or benchmark:** Commercial SSD testing with Meta Garbage Collection and User Garbage Collection stress tasks; device models, traces, test budgets, and event definitions are unspecified.

</details>

<span id="paper-iccad-2025-1137"></span>

### Software-Style Hardware Debugging: A Hardware Generation, Simulation and Debugging Framework

ICCAD 2025 · Record: `iccad-2025-1137`

**Problem:**

Hardware generation and debugging workflows need software-style iteration across generation, simulation, and diagnosis rather than disconnected tool invocations.

**Mechanism / artifact:**

Python-based ComoPy framework integrating hardware generation, Verilator simulation, cocotb interaction, and debugging utilities.

**Workload — the work tested:**

Artifact-level simulator integration; paper case studies, Sodor/database-accelerator workloads, and benchmark suite are not exposed by the package page.

**Hardware and manufacturing assumptions:**

Python 3.10+, Verilator 5.040, and Icarus Verilog v13_0 environments listed by the package; hardware targets, simulator flags, and execution costs are unspecified.

**Baseline — the comparison method:**

None exposed by artifact description

**Reported measurements:**

Not established in the captured evidence.

**Limits on the conclusion:**

The package does not assert the ICCAD title, DOI, or complete paper author list; identity correspondence remains partial.

Artifact metadata establishes availability and dependencies, not paper benchmarks, novelty, or the indexed 6% performance-loss figure.

No manuscript, benchmark logs, or independent reproduction was recovered.

**Source and location**

Evidence tier: Author attributed artifact source. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://pypi.org/project/comopy/)

PyPI ComoPy 0.7.0 description

package metadata and tested environments

DOI 10.1109/ICCAD66269.2025.11240882 from inventory/recovery assessment

#### Additional source assessment

This separately recorded check is dated 2026-09-06. It supplements the original record above and retains its own scope and uncertainty.

[Assessment record](../../iccad/data/comopy-artifact-primary-recovery-v1.json)

[Assessed source](https://pypi.org/project/comopy/)

**Extraction scope**

PyPI project description for ComoPy 0.7.0, including maintainer/organization metadata, package purpose, dependencies and tested simulator versions; no ICCAD manuscript text.

**Conditions**

PyPI lists Python 3.10+, Verilator 5.040 and Icarus Verilog v13_0 test environments; no paper benchmarks, Sodor/database-accelerator case-study conditions or baseline protocol recovered from this source.

**Headline metric status**

withheld_pending_primary_paper

**Independent review status**

pending

<span id="paper-iccad-2025-1117"></span>

### Uncertainty-Guided Live Measurement Sequencing for Fast SAR ADC Linearity Testing

ICCAD 2025 · Record: `iccad-2025-1117`

**Problem:**

Dense acquisition and offline reconstruction increase the cost of SAR ADC linearity testing.

**Mechanism / artifact:**

Closed-loop selection of code-edge measurements with an Extended Kalman Filter behavioral mismatch model and covariance inflation.

**Workload — the work tested:**

Simulated 10–18-bit SAR ADCs; statistical experiment on 100 synthetic 16-bit ADCs informed by modified measured-device mismatch data.

**Hardware and manufacturing assumptions:**

C implementation; acquisition modeled at 1 MS/s; reusable setup excluded from per-device timing; compute-platform conditions unresolved. Not a measured production tester deployment.

**Baseline — the comparison method:**

12-bit reconstruction comparison to ramp histogram testing at 128 hits per code; cross-paper model-driven timing references are not locally matched implementations

**Reported measurements:**

Not established in the captured evidence.

**Limits on the conclusion:**

Headline timings withheld pending platform/setup accounting and independent review. Fixed-iteration evaluation does not demonstrate adaptive stopping. Noisy small sweeps can diverge temporarily; covariance shrinkage can induce drift. Distinct enhanced follow-up arXiv:2511.11917 is excluded.

**Source and location**

Evidence tier: Medium primary full text. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://arxiv.org/abs/2511.11895)

**Fields:** problem

method_or_artifact

workload_or_benchmark

hardware_or_process_assumptions

baselines

limits

**Location:** arXiv:2511.11895v1, Sections III.E–VI, PDF pages 5–8; visually checked Table I page 7; iccad/data/uglms-primary-recovery-v1.json

#### Additional source assessment

This separately recorded check is dated 2026-09-06. It supplements the original record above and retains its own scope and uncertainty.

[Assessment record](../../iccad/data/uglms-primary-recovery-v1.json)

[Assessed source](https://arxiv.org/abs/2511.11895)

**Extraction scope**

Exact preprint identity; PDF Sections III.E–VI and Table I, with page 7 table visually checked. No experimental reproduction.

**Conditions**

**Evaluation:** C implementation and simulation experiments; mismatch vectors derived from measured ADC data were resampled and shifted to protect proprietary information (Section IV, page 5).

**Statistical test:** 100 synthetic 16-bit ADCs, 200 iterations, 128 samples per sweep and 1.0 LSB RMS noise (Section IV.C, page 6).

**Table i:** **Resolution bits:** 10

12

14

16

18

**Samples per sweep:** 64

64

128

128

128

**Selection per iteration us:** 88.0

89.5

141.0

300.5

1181.0

**Selection total ms:** 17.6

17.9

28.2

60.1

236.2

**Total ms:** 18.5

18.7

31.6

61.2

238.8

**Iterations:** 200

**Input noise lsb rms:** 1.0

**Timing scope:** Assumed 1 MS/s acquisition; concurrent acquisition/selection; reusable Jacobian and other matrix setup excluded from per-device totals (Section IV.D, pages 6–7). Compute-platform conditions need verification.

**Baseline:** Figure 8 compares 12-bit reconstruction against ramp histogram testing at 128 hits per code; cited cross-paper runtime comparisons are not matched local implementations.

**Termination:** Evaluation uses fixed iterations; uncertainty-based adaptive stopping is discussed as supported, not evaluated as the fixed-budget results.

**Failure modes:** Noisy small sweeps can temporarily diverge; later EKF drift from shrinking covariance is acknowledged (Section IV.B, page 6).

**Headline metric status**

withheld_pending_compute_platform_and_independent_review

**Independent review status**

pending

<span id="paper-iccad-2025-114"></span>

### RIROS: A Parallel RTL Fault SImulation FRamework with TwO-Dimensional Parallelism and Unified Schedule

ICCAD 2025 · Record: `iccad-2025-114`

**Problem:**

Dynamic fault propagation creates uneven RTL simulation tasks and idle cores.

**Mechanism / artifact:**

Taskflow scheduling combines structural work stealing with fault-wise splitting of overloaded nodes; dependency-constrained local synchronization overlaps computation.

**Workload — the work tested:**

Seven RTL designs spanning RISC-V cores, accelerators and JPEG; stuck-at wire/register faults, with fault dropping disabled.

**Hardware and manufacturing assumptions:**

Reported Intel i7, 16 cores at 3.80GHz; C++ Taskflow, gcc-11 -O2; exact CPU SKU and VCS version unresolved.

**Baseline — the comparison method:**

Single-core ERASER

16-core VCS using force/release

Single-core RIROS

Structural-only and structural-plus-fault parallelism ablations

**Reported measurements:**

Not established in the captured evidence.

**Limits on the conclusion:**

Headline metrics withheld: JPEG runtime ratios disagree with reported speedups. Cross-tool comparisons are not equal-core scaling. Correctness depends on preserving current-cycle reads before synchronization; no independent reproduction or safety certification.

**Source and location**

Evidence tier: Medium primary full text. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://arxiv.org/abs/2508.16376)

**Fields:** problem

method_or_artifact

**Location:** Abstract; Sections III–IV

**Fields:** workload_or_benchmark

hardware_or_process_assumptions

baselines

limits

**Location:** Section V; visually checked Table II PDF page 7; iccad/data/riros-primary-recovery-v1.json

#### Additional source assessment

This separately recorded check is dated 2026-09-06. It supplements the original record above and retains its own scope and uncertainty.

[Assessment record](../../iccad/data/riros-primary-recovery-v1.json)

[Assessed source](https://arxiv.org/abs/2508.16376)

**Extraction scope**

Sections IV–V; Table II visually verified on PDF page 7; no reproduction.

**Conditions**

C++/Taskflow, gcc-11 -O2; reported i7, 16 cores, 3.80GHz; seven designs, stuck-at wire/register faults, no fault dropping. ERASER uses one core; VCS force/release comparison uses 16. Exact CPU SKU and VCS version unresolved.

**Headline metric status**

withheld_pending_runtime_ratio_reconciliation

**Independent review status**

pending

<span id="paper-iccad-2025-1027"></span>

### HLSDebugger: Identification and Correction of Logic Bugs in HLS Code with LLM Solutions

ICCAD 2025 · Record: `iccad-2025-1027`

[Read the step-by-step explanation](#explanation-iccad-2025-1027)

**Updated source-backed reading card**

Reviewed 2026-09-08. Reconciles the captured abstract card with the full arXiv preprint; separates HLS logic debugging from syntax repair, generated mutation supervision from natural bugs, identification granularities from exact-snippet correction, and benchmark results from hardware-level validity.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

HLS code can compile while implementing the wrong function. Debugging without reliable test cases requires locating the faulty code, identifying its logic-bug type and producing a correction; circuit data for training is scarce.

**Mechanism / artifact:**

HLSDebugger releases an approximately 300K-sample labeled dataset and fine-tunes a CodeT5-Large encoder–decoder. The encoder predicts bug type and token locations; its representations guide a cross-attending decoder that generates the corrected snippet. A weighted joint loss trains bug type, imbalanced token location and correction generation together.

**Workload — the work tested:**

A random 2,000-sample evaluation subset from an eight-bug-type HLS benchmark: out-of-bounds array access, uninitialized read, out-of-bounds shift, infinite loop, unintended sign extension, incorrect manual loop unrolling, wrong zero initialization and wrong split-buffer half. Training data starts with roughly 30K crawled HLS samples and roughly 10K GPT-3.5 RTL-to-HLS augmentations; about 2K high-Rouge-L-overlap samples are removed from training.

**Hardware and manufacturing assumptions:**

CodeT5-Large with 24 encoder and 24 decoder transformer layers, 1024-dimensional embeddings and 16-dimensional heads; three-layer MLP prediction heads. Evaluation uses token, line and code-level identification plus strict processed substring matching for correction, with generated length limited to three times the label length. HLS compilation, synthesis, timing, area, power and independent functional/equivalence checking are not part of the reported correction metric.

**Baseline — the comparison method:**

GPT-3.5

GPT-4

Gemma-7B without fine-tuning

Gemma-7B unsupervised fine-tuning

Gemma-7B supervised fine-tuning

HLSEncoder-only and encoder-plus-baseline combinations

**Reported measurements:**

Identification: HLSDebugger token precision/recall/F1/ROC area 54.3%/83.5%/0.614/0.935; line precision/recall/F1/ROC area 57.7%/78.4%/0.627/0.923; code-wise top-1/top-5 79.5%/87.6%.

Identification baselines include GPT-4 token precision/recall 12.2%/37.1%, line precision/recall 13.3%/17.5% and code-wise top-1/top-5 19.7%/54.7%.

Correction without the true location: HLSDebugger 37.6%, GPT-4 10.5%, Gemma-7B SFT 15.1%, and HLSEncoder plus Gemma-7B SFT 23.7%. Correction with the ground-truth location supplied: HLSDebugger 49.1%.

**Limits on the conclusion:**

The approximately 300K labels are generated through code collection, GPT-3.5 augmentation and prompted bug insertion; the mutation distribution and eight categories do not establish coverage of naturally occurring HLS failures.

Strict substring match measures agreement with the labeled correction after preprocessing, not compilation, functional equivalence, synthesis validity, hardware quality or semantic correctness in an arbitrary surrounding design.

The 2,000-sample random evaluation subset and Rouge-L filtering constrain the reported generalization claim; exact project splits, per-category denominators and semantic contamination outside the threshold remain relevant.

The reported model is not ready for practical debugging according to the paper's own discussion: the best no-location correction rate is 37.6%. Training/inference cost, human effort, held-out projects, naturally occurring bugs and independent HLS-tool validation remain open.

**Source and location**

Evidence tier: Primary arxiv preprint v1 and open source artifact link; selected manuscript reading, artifact execution and independent acceptance not performed. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://arxiv.org/pdf/2507.21485v1)

Version 1: Introduction and Figure 1 pages 1–2; dataset generation Sections IV-A and Figures 2–3 pages 3–4; encoder–decoder and joint loss Sections IV-B–C and Figures 4–6 pages 4–6; evaluation benchmark/model/metrics Sections V-A–D pages 6–7; identification Table II page 7; correction results Sections VI-A–B and Discussion VII, including Table/figures pages 7–8. Open-source artifact link in the paper: https://github.com/hkust-zhiyao/HLSDebugger; ICCAD DOI 10.1109/ICCAD66269.2025.11240664.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** high_primary_preprint

**Baselines:** advanced general-purpose LLMs including GPT-4

traditional sequential LLM debugging solutions

HLS/static-analysis tool information when available

**Evidence locators:** Not established in the captured evidence.

**Evidence url:** https://arxiv.org/abs/2507.21485

**Hardware or process assumptions:** Not established in the captured evidence.

**Limits:** The evidence is an author preprint; evaluation depends on the generated bug dataset and selected bug categories, and the repository has not yet extracted all accuracy, correction-validity, and generalization tables.

**Method or artifact:** Open labeled HLS bug dataset and customized encoder-decoder LLM that performs multi-task bug-location identification, bug-type prediction, and code correction, optionally using HLS-tool information.

**Metrics:** approximately 300K labeled training samples

bug-identification performance above GPT-4 in reported evaluation

more than 3X bug-correction performance improvement over advanced LLMs

**Problem:** HLS logic debugging is labor-intensive, circuit data is scarce, logic bugs are harder than syntax bugs, and reliable test cases are often unavailable.

**Workload or benchmark:** HLS code containing known logic-bug categories, without assuming additional test cases.

</details>

## What remains to establish

Resolve unspecified workloads, comparison methods, resource budgets, and source locations before generalizing a reported gain. Multiple papers in this selected sample permit comparison of mechanisms, but do not by themselves establish recurrence across years or a long-term trend.

[All subthemes](../expanded-taxonomy-v1.md) · [Research directions](../directions/README.md)
