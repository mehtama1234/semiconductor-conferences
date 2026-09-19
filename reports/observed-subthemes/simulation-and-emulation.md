# Simulation and emulation

This subject has 3 records in the selected sample. This page explains where it fits, then presents all captured paper evidence without shortening the measurements or limitations.

[Definitions used in the paper records](../reading-guide-v1.md)

## Understand the parent subject first

- [Verification and validation](../themes/verification-and-validation.md)

## A simulation result is conditional on a model and an input

Simulation executes a description of behavior. Its result depends on the model, the supplied inputs, and the rules used to order events. Faster execution lets a project examine more cases, but it does not correct an incomplete model or a weak test. Emulation uses an implementation platform to execute represented behavior; the selected records do not establish that their methods run on a hardware emulator.

This group spans three different parts of a verification workflow: parallel simulation, generated peripheral traces, and maintenance of hardware-generation benchmarks. The common need is preserving the meaning of a test while increasing the amount or usefulness of testing. None of the captured descriptions supplies quantitative evaluation.

## Partitioning simulation according to activity

[Activity-aware RTL partitioning](../observed-subthemes/simulation-and-emulation.md#paper-dac-2026-research440) divides event-driven simulation work among threads. RTL describes updates to hardware state and the logic between those updates. An event-driven simulator processes changes that require further evaluation rather than assuming that every modeled object performs equal work at every step.

Equal-sized partitions can therefore have unequal execution cost. A region with many objects but little activity can require less work than a smaller, frequently changing region. Accounting for activity is a plausible way to balance work. However, partition boundaries also create communication and synchronization costs when one region affects another.

The source does not specify how activity is estimated or whether partitions change during execution. A workload used to estimate activity may differ from a later test, so evaluation should include changes in stimulus and operating phase. The relevant result is reduced complete simulation time on the same design and tests, including preparation and synchronization.

Correct event semantics are equally important. Parallel scheduling must preserve the behavior required by the language and simulation model. Agreement on a few final values would not necessarily expose an incorrectly ordered intermediate event. The record provides no determinism, trace-equivalence, memory, or thread-scaling results, so correctness and scalability remain unverified claims.

<span id="explanation-dac-2026-research440"></span>

### Activity-aware RTL partitioning: balancing event work must preserve event-causality semantics

#### What event-driven RTL simulation does

RTL describes hardware state and the logic that updates it. An event-driven simulator schedules evaluation when a signal or state changes and propagates resulting changes to dependent logic. It does not perform equal work for every modeled object at every simulated time.

A large quiet region can generate little work, while a small region with a clock, reset, handshake or feedback activity can generate many events. Static equal-size partitions can therefore give one thread a much larger queue than another. Activity-aware partitioning tries to use observed or predicted event work when assigning regions to threads.

#### What partitioning adds

When a dependency crosses a partition boundary, a thread must communicate the event or state update to another thread. The simulator needs a rule for timestamps, causality, event ownership, synchronization and simultaneous updates. Repartitioning can also move state, rebuild queues or invalidate an activity estimate.

The useful balance is complete simulation time, not only equal event counts or thread utilization. Work that is moved across a boundary can reduce local imbalance while increasing synchronization and memory traffic. Activity from one stimulus or phase may also fail to predict a later phase, creating imbalance or excessive repartition overhead.

#### Correctness and scalability are separate

A parallel simulator must preserve the RTL language and simulator semantics, including ordering of dependent events and the handling of same-time updates. Matching a few final register values does not prove trace equivalence or determinism. Repeated runs should expose whether event order, random seeds, scheduling and floating-point behavior produce the same declared result.

Compare serial simulation, static partitioning and activity-aware partitioning on the same designs, traces, simulator settings, cores and stopping condition. Report complete wall time, speedup by thread count, event count, synchronization and communication time, repartition time, memory, utilization, determinism and mismatches in event or state traces. Include stimulus and operating phases not used to estimate activity.

The captured DAC description supports activity-aware partitioning for multi-threaded event-driven RTL simulation. It reports no activity estimator, event protocol, deterministic-trace result, speedup, memory, overhead or design-suite measurement. The evidence supports a load-balancing direction, not demonstrated faster or semantically equivalent simulation.

[Observed paper card](../observed-subthemes/simulation-and-emulation.md#paper-dac-2026-research440)

## Generating a trace that a peripheral could produce

[The Phantom of PCIe](../observed-subthemes/simulation-and-emulation.md#paper-dac-2026-research514) constrains generative models used to synthesize peripheral traces. A trace records a sequence of interactions. Generating individually plausible entries is not enough: their ordering and state dependencies must also be valid for the modeled device and protocol.

The captured description does not identify the constraints, protocol version, peripheral classes, or validity checker. It would be inappropriate to infer coverage of particular PCIe rules. The evaluation needs to state which properties are enforced by construction and which are checked afterward.

Validity and usefulness are separate outcomes. Repeating a small set of valid sequences can produce a high validity rate with little new test coverage. A diverse collection of invalid traces can exercise error handling without representing normal operation. A useful study should identify its intended testing purpose and report validated diversity, execution cost, and replay results under that purpose. Those measurements are absent here.

<span id="explanation-dac-2026-research514"></span>

### The Phantom of PCIe: a plausible transaction is not a valid stateful peripheral trace

#### What a peripheral trace represents

A trace is an ordered record of interactions between a host and a peripheral. It can include configuration reads and writes, memory transactions, completions, data movement, interrupts, errors and timing or ordering information. The legality of one event can depend on earlier events: a device may need to be configured before a DMA request, and a completion must correspond to a request with the right tag and state.

Generative AI can produce entries that look like examples while violating protocol ordering, credit rules, link timing, device state, payload constraints or completion dependencies. A constraint system must state which of these properties it enforces during generation and which are checked afterward.

#### What constrained generation must preserve

The method needs a device-state model, protocol version, transaction grammar, legal state transitions, timing rules, error behavior and a validation oracle. It should distinguish constraints enforced by construction from post-generation filtering. If a trace is rejected, the system should record why; otherwise a high acceptance rate can hide that the generator avoids difficult but valuable cases.

Validity and coverage are different. Repeating a short sequence that always succeeds can produce high validity with little new state or protocol coverage. Generating many rare or invalid sequences can increase diversity without testing normal operation. The target should define coverage of states, transaction types, ordering combinations, error paths and device behaviors.

#### What the evaluation must measure

Compare unconstrained generation, constrained generation and record-and-replay under the same device classes, protocol, trace budget and hardware or software oracle. Report protocol-validity rate, state-transition validity, coverage, diversity, novelty, generation time, rejection cost, replay success, error handling and resource use. Replay on a model is different from replay on a real or cycle-accurate peripheral.

Test unseen device configurations and protocol sequences, including configuration changes, DMA, backpressure, completion reordering, malformed inputs and recovery. A constraint learned only from known device classes may not transfer to a new peripheral or protocol version.

The captured DAC description supports constrained generative synthesis of PCIe peripheral traces. It reports no protocol version, state model, validity oracle, coverage, diversity, runtime, replay or hardware result. The evidence supports a test-input generation direction, not demonstrated PCIe coverage or real-device usefulness.

[Observed paper card](../observed-subthemes/simulation-and-emulation.md#paper-dac-2026-research514)

## Updating a benchmark without losing comparability

[RTL-Benchmt](../observed-subthemes/simulation-and-emulation.md#paper-dac-2026-research874) uses agents to analyze and revise RTL-generation benchmarks. A benchmark defines both the tasks and the procedure used to judge generated hardware. Revising either can change apparent model performance even when the model itself is unchanged.

Maintenance can be useful when tasks contain errors or tools change. To support comparisons, however, each revision needs a recorded reason, versioned inputs and checkers, and reruns of relevant baselines. A test added after seeing a candidate failure is valuable for future checks but changes the basis of the score. It should not silently replace the original evaluation protocol.

The source supplies no benchmark-validity, contamination-control, coverage, revision-cost, or model-comparison results. An agent's successful edit is not independently established benchmark correctness. Review should verify that generated implementations cannot pass by exploiting weak tests and that revised tasks retain their intended difficulty and meaning.

<span id="explanation-dac-2026-research874"></span>

### RTL-Benchmt: changing a benchmark changes the measurement unless tasks, checkers and versions remain comparable

#### What a benchmark measures

An RTL-generation benchmark is not only a list of prompts. It includes task descriptions, reference intent, input/output behavior, testbenches or checkers, tool versions, resource limits, compilation rules and the procedure that turns an implementation into a score. A model can score higher because the task became easier or the checker became weaker, even when the model did not improve.

RTL tasks are especially sensitive to checker design. A generated module may pass a narrow simulation while violating an untested protocol condition, using an unintended latency, relying on an unsupported language feature or exploiting a mismatch between the prompt and the test. Synthesis and timing checks may reveal failures that a functional test misses.

#### What agent-assisted maintenance changes

An agent can inspect failures, revise task text, add tests, update reference designs or identify stale tool assumptions. That can improve a benchmark, but each revision is a change to the instrument. The workflow needs a recorded reason, versioned task and checker files, an approval decision, contamination controls and reruns of relevant baselines before and after the change.

A test added after seeing a candidate failure may be an important regression test. It can also leak a solution detail or make the new benchmark harder in a way that invalidates historical score comparisons. The governance process must distinguish bug repair, scope expansion, difficulty calibration and security hardening.

#### What the evaluation must expose

Compare static and revised benchmarks with the same model versions, prompts, toolchain, time/memory limits and random seeds where relevant. Report task validity, checker false acceptance/rejection, language and tool coverage, functional and synthesis coverage, contamination or solution leakage, revision time, task difficulty, baseline score changes and the reasons for every revision.

Review tasks with independent humans or models that did not author the revision. Run generated RTL through simulation, synthesis, timing and intended design-rule checks, and include hidden tests that cover protocol, reset, corner and adversarial behavior. Preserve old benchmark versions so that a model can be evaluated on both historical and current instruments.

The captured DAC description supports agent-assisted RTL-benchmark maintenance. It reports no validity audit, contamination control, coverage, revision cost, difficulty analysis, checker-strength result or baseline rerun. The evidence supports a benchmark-governance direction, not evidence that agent maintenance improves RTL-generation measurement.

[Observed paper card](../observed-subthemes/simulation-and-emulation.md#paper-dac-2026-research874)

## The end-to-end implication

The three proposals motivate improving execution capacity, test inputs, and evaluation maintenance together. That connection is a research hypothesis, not an integration demonstrated by the papers. A stronger workflow would preserve reproducible versions, validate model and trace semantics, and report new confirmed findings per total verification cost. More simulation steps or a higher benchmark score alone cannot establish that real hardware is better verified.

## Compare the results carefully

First identify the inputs and required output quality. Then identify the limited resource: time, memory, communication, energy, circuit area, or correctness coverage. Ask which part of the method reduces that cost and which new cost it adds. Compare numbers only when the experiments hold these conditions sufficiently similar.

A conference description may explain the proposal while omitting the full experiment. An author preprint link may have been coded from its abstract. The source classification does not by itself establish that every table was read. Missing locations remain visible below.

## Complete captured evidence

These are evidence records, not substitutes for the explanations above. Each record preserves its problem, proposed method, measurements, comparison conditions, and source limits. A populated record does not establish that its mechanism has been fully explained or independently verified.

<span id="paper-dac-2026-research440"></span>

### Activity-Aware Partitioning for Effective Multi-Threaded Event-Driven RTL Simulation

DAC 2026 · Record: `dac-2026-research440`

[Read the step-by-step explanation](#explanation-dac-2026-research440)

**Updated source-backed reading card**

Reviewed 2026-09-08. Deepens the existing activity-aware RTL simulation treatment into a paper-level reading; separates activity-based load balancing from event causality, cross-partition synchronization, determinism and complete simulation-time evidence.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Event-driven RTL simulation has uneven work because some modeled regions change frequently while others remain idle, and cross-region dependencies can limit thread scalability.

**Mechanism / artifact:**

Activity-aware partitioning for parallel RTL simulation; activity estimator, partition granularity, repartition policy, event ownership, synchronization protocol and simulator integration are unspecified.

**Workload — the work tested:**

Event-driven RTL designs and stimulus traces; simulator, design suite, activity phases, thread counts and trace split are unspecified.

**Hardware and manufacturing assumptions:**

Multicore host running an event-driven RTL simulator; core topology, memory, synchronization, event queue and inter-thread communication assumptions are unspecified.

**Baseline — the comparison method:**

Serial RTL simulation

Static partitioning

Simulator, design, stimulus, thread, correctness and timing conditions are unspecified

**Reported measurements:**

Simulation scalability is claimed qualitatively; no complete simulation time, speedup, determinism, memory, partitioning overhead, synchronization cost or design-suite result is reported.

**Limits on the conclusion:**

Event-driven simulation processes updates and propagates changes through dependent RTL logic. Equal object counts do not imply equal work: a small active region can generate more events than a large quiet region. Activity-aware partitioning can balance work only when the estimate represents the later stimulus and operating phase.

Partition boundaries create communication and synchronization. A parallel simulator must preserve event ordering or the defined semantics when one region affects another; matching final values on a few tests may miss an incorrectly ordered intermediate event or nondeterministic race.

The official description reports no activity estimator, repartition cost, event protocol, deterministic-trace check, memory, thread scaling, complete time or design-suite result. It supports a load-balancing direction, not demonstrated faster or semantically equivalent RTL simulation.

**Source and location**

Evidence tier: Primary captured official DAC description plus existing chapter level RTL simulation discussion; no full paper extraction, simulator reproduction or determinism/scaling validation. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH440)

DAC 2026 official description; captured Problem, Mechanism / artifact, Workload, Hardware, Baseline, Measurements and Limits fields; record RESEARCH440; no manuscript pages.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** serial RTL simulation

static partitioning

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH440

**Hardware or process assumptions:** Multicore host and event-driven simulator; synchronization and memory assumptions are unspecified.

**Limits:** No simulation speed, determinism, memory, overhead, or design-suite results are reported.

Activity estimates may be workload-specific.

Official description only; simulator and design validation is required.

**Method or artifact:** Activity-aware partitioning for parallel RTL simulation.

**Metrics:** Simulation scalability is claimed qualitatively

**Problem:** Event-driven RTL simulation has uneven activity and synchronization that limit thread scalability.

**Workload or benchmark:** Event-driven RTL designs; simulators, traces, and thread counts are unspecified.

</details>

<span id="paper-dac-2026-research514"></span>

### The Phantom of PCIe: Constraining Generative Artificial Intelligences for Practical Peripherals Trace Synthesizing

DAC 2026 · Record: `dac-2026-research514`

[Read the step-by-step explanation](#explanation-dac-2026-research514)

**Updated source-backed reading card**

Reviewed 2026-09-08. Deepens the existing Phantom of PCIe treatment into a paper-level reading; separates syntactic trace plausibility, protocol validity, stateful device behavior, coverage diversity and hardware replay.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Generative models can produce PCIe peripheral traces whose individual transactions look plausible but whose ordering, state dependencies or timing cannot occur for a real device and protocol.

**Mechanism / artifact:**

Constraint mechanism for generative AI peripheral-trace synthesis; protocol constraints, device state model, timing rules, validation oracle and generation/rejection process are unspecified.

**Workload — the work tested:**

PCIe peripheral traces; device classes, protocol version, transaction mix, error cases, trace length, capture source and coverage target are unspecified.

**Hardware and manufacturing assumptions:**

PCIe host/peripheral system with trace capture and replay; link generation, timing, configuration state, DMA, memory model and hardware oracle are unspecified.

**Baseline — the comparison method:**

Unconstrained trace generation

Record-and-replay traces

Device class, protocol, validity checker, replay hardware and coverage conditions are unspecified

**Reported measurements:**

Trace synthesis utility is claimed qualitatively; no protocol-validity rate, coverage, diversity, runtime, replay success, error-handling or hardware result is reported.

**Limits on the conclusion:**

A trace is a time-ordered sequence of requests, completions, configuration changes, data transfers and errors. A transaction can be valid in isolation but invalid after the device state, ordering rule, credit, tag, link timing or completion dependency is considered.

Constraints can enforce known syntax or state transitions, but they may encode only the device classes and scenarios represented in their specification. A high validity rate can come from repeating a small safe sequence, while a diverse set can contain invalid traces; validity and useful coverage must be measured separately.

The official description reports no protocol version, state model, validity oracle, coverage definition, diversity metric, runtime, replay result or hardware trace validation. The record supports constrained generation as a test-input direction, not demonstrated PCIe coverage or real-device usefulness.

**Source and location**

Evidence tier: Primary captured official DAC description plus existing chapter level pcie trace discussion; no full paper extraction, protocol oracle or hardware replay validation. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH514)

DAC 2026 official description; captured Problem, Mechanism / artifact, Workload, Hardware, Baseline, Measurements and Limits fields; record RESEARCH514; no manuscript pages.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** unconstrained trace generation

record-and-replay traces

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH514

**Hardware or process assumptions:** PCIe host/peripheral systems and trace capture; protocol and timing assumptions are unspecified.

**Limits:** No protocol validity, coverage, diversity, runtime, or hardware-replay results are reported.

Constraints may encode only known device classes.

Official description only; hardware trace validation is required.

**Method or artifact:** Constraint mechanism for generative AI trace synthesis.

**Metrics:** Trace synthesis utility is claimed qualitatively

**Problem:** Generative models may produce unrealistic PCIe peripheral traces without hardware and protocol constraints.

**Workload or benchmark:** PCIe peripheral traces; devices, protocols, and validation oracles are unspecified.

</details>

<span id="paper-dac-2026-research874"></span>

### RTL-Benchmt: Dynamic Maintenance of RTL Generation Benchmark Through Agent-Assisted Analysis and Revision

DAC 2026 · Record: `dac-2026-research874`

[Read the step-by-step explanation](#explanation-dac-2026-research874)

**Updated source-backed reading card**

Reviewed 2026-09-08. Deepens the existing RTL-Benchmt treatment into a paper-level reading; separates benchmark maintenance from model improvement and makes task validity, checker strength, leakage, versioning, difficulty and baseline comparability explicit.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

RTL-generation benchmarks can become stale or contain flawed tasks as design patterns, tools and evaluation requirements change, which can make model comparisons unreliable.

**Mechanism / artifact:**

Agent-assisted benchmark analysis and revision workflow; revision policy, agent permissions, task/checker changes, acceptance review and version-control procedure are unspecified.

**Workload — the work tested:**

RTL-generation tasks and test suites; designs, languages, tool versions, licenses, synthesis flow, hidden tests and evaluation protocol are unspecified.

**Hardware and manufacturing assumptions:**

RTL simulation and synthesis environment; simulator, synthesizer, target technology, timing/signoff rules, resource limits and tool versions are unspecified.

**Baseline — the comparison method:**

Static RTL benchmark

Manual benchmark maintenance

Model comparisons require the same task, checker, tool, version, budget and contamination controls

**Reported measurements:**

Benchmark maintenance efficiency is claimed qualitatively; no benchmark-validity, leakage, coverage, revision cost, task-difficulty, checker-strength or model-comparison result is reported.

**Limits on the conclusion:**

A benchmark is both a set of tasks and a measurement procedure. Changing a prompt, reference design, hidden test, checker or synthesis setting can change model scores even when the model is unchanged. A revision must record what changed, why it changed and which prior scores remain comparable.

An agent can identify a broken task or propose a stronger test, but the revision needs independent review. Tests added after seeing a model output can fix a real weakness while also changing the evaluation basis or leaking information about the target solution. Checkers must reject implementations that exploit underspecified behavior rather than implement the intended hardware.

The official description reports no validity audit, contamination control, coverage, revision cost, difficulty analysis, baseline rerun or model-comparison result. The record supports benchmark governance as a research direction, not evidence that agent maintenance improves RTL-generation measurement.

**Source and location**

Evidence tier: Primary captured official DAC description plus existing chapter level benchmark maintenance discussion; no full paper extraction, independent governance review or baseline rerun. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH874)

DAC 2026 official description; captured Problem, Mechanism / artifact, Workload, Hardware, Baseline, Measurements and Limits fields; record RESEARCH874; no manuscript pages.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** static RTL benchmark

manual benchmark maintenance

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH874

**Hardware or process assumptions:** RTL simulation/synthesis environment; tool versions and signoff assumptions are unspecified.

**Limits:** No benchmark validity, leakage, coverage, revision cost, or model-comparison results are reported.

Agent revisions may change task difficulty.

Official description only; independent benchmark governance is required.

**Method or artifact:** Agent-assisted benchmark analysis and revision workflow.

**Metrics:** Benchmark maintenance efficiency is claimed qualitatively

**Problem:** RTL-generation benchmarks become stale as tools and design patterns change.

**Workload or benchmark:** RTL-generation tasks and test suites; designs, licenses, and evaluation protocol are unspecified.

</details>

## What remains to establish

Resolve unspecified workloads, comparison methods, resource budgets, and source locations before generalizing a reported gain. Multiple papers in this selected sample permit comparison of mechanisms, but do not by themselves establish recurrence across years or a long-term trend.

[All subthemes](../expanded-taxonomy-v1.md) · [Research directions](../directions/README.md)
