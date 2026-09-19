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
