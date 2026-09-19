# Real time and networked systems

This subject has 3 records in the selected sample. This page explains where it fits, then presents all captured paper evidence without shortening the measurements or limitations.

[Definitions used in the paper records](../reading-guide-v1.md)

## Understand the parent subject first

- [Systems applications and workloads](../themes/systems-applications-and-workloads.md)

## A deadline is about a complete response

A system can compute correct values and still respond too late. Real-time analysis therefore asks when the result becomes available, not only whether the computation is correct. The interval of interest may start with a sensor event and end with an actuator command, passing through several tasks and network transfers.

Execution time is the time a task spends running. Response time can also include waiting for a processor, input, or resource. End-to-end latency includes the relevant stages between the selected starting event and final response. Adding isolated execution times can miss these waits and the effects of how tasks exchange data.

A mean describes an average. A percentile describes a threshold in an observed or modeled distribution. A worst-case bound claims that the delay cannot exceed a value under stated assumptions. Jitter describes variation in delay, but its definition must also be specified. None of these measures can replace the others without additional reasoning.

## PFATS: separate traffic before shared queues create interference

A network flow is a stream of related packets. Traffic shaping delays transmission when necessary to control that stream's output pattern. Although it can add waiting locally, it can reduce bursts that would otherwise create larger queues downstream. The result depends on the permitted input traffic and the service available along the path.

[Per Flow Asynchronous Traffic Shaping](../observed-subthemes/real-time-and-networked-systems.md#paper-dac-2026-research163) proposes PFATS: per-flow eligibility-time calculation, separate flow queues, and a shift-register-matrix scheduler. Eligibility time determines when a frame is allowed to proceed. The refreshed description identifies interference in grouped queues as the target, not elimination of all network contention.

The authors report an FPGA-based switch supporting 192 flows, with 7.14% additional on-chip memory over conventional asynchronous shaping. They report microsecond-scale end-to-end delay and jitter within 5 microseconds in their scenarios. The source does not expose the topology, load envelope, packet sizes, link rates, or derivation of that jitter bound. It must remain a scenario-qualified claim, not a guarantee for any network of these switches. [Official PFATS description](https://63dac.conference-program.com/presentation/?id=RESEARCH163&sess=sess171).

Separate queues still share physical links and scheduler resources. A deployment check must establish admission limits, buffer requirements, and behavior when traffic exceeds its contract. Supporting a stated number of flows does not specify how much traffic each may send.

<span id="explanation-dac-2026-research163"></span>

## PFATS: isolating queues improves a traffic-shaping mechanism, not automatically the network-wide deadline guarantee

Time-Sensitive Networking (TSN) carries flows with timing contracts over shared links and switches. A shaper may delay a frame at one point so that bursts are controlled, but the end-to-end result also includes serialization, propagation, arbitration, queueing and downstream interference. An asynchronous design avoids requiring one global clock, which makes its local eligibility rules and clock assumptions part of the timing model.

PFATS is described as a per-flow asynchronous shaper with three coupled pieces: a frame eligibility-time calculator, a separate queue for each flow, and a Synchronous Shift Register Matrix (SSRM) scheduler. Eligibility time determines when a frame becomes serviceable; the scheduler then needs a defined arbitration rule to choose among eligible frames while respecting ports, priorities and available buffer. Per-flow queues target the interference introduced when several flows share one queue. They do not create extra link bandwidth or remove contention downstream.

The first gate is protocol semantics. Define the arrival and service curves or other contracts, eligibility-time update, timestamp precision, clock domains, synchronization assumptions, priority/arbitration, frame ordering, queue admission, buffer overflow and behavior when a flow exceeds its contract. Map those rules onto the FPGA pipeline and switch fabric, including serialization, propagation, processing and downstream queues. A local scheduler trace is not a proof that every admissible flow set meets its end-to-end deadline.

The second gate is a meaningful latency bound. Define jitter—maximum-minus-minimum, deviation from a reference, percentile or worst case—and state timestamp locations and the packet population. Evaluate latency distributions and deadline misses under controlled flow periods, packet sizes, bursts, priorities, hop counts, link rates, competing traffic and clock offsets. Include queue occupancy, drops, throughput, link utilization, head-of-line behavior and overload response. Test both admissible traffic and contract violations; a design that behaves well only below an unstated load envelope cannot support a general deterministic claim.

The third gate is hardware accounting. Report FPGA family and clock, port/link rates, pipeline stages, on-chip memory organization, per-flow state, SSRM size, timestamp/eligibility precision, configuration cost and testbed instrumentation. Compare conventional grouped-queue ATS and synchronous shaping with the same traffic contracts, topology, buffers and measurement boundary. Separate added memory from total switch area, power and timing closure; “192 flows” is a state-capacity result, not a statement that 192 arbitrary-rate flows are schedulable.

The official description reports an FPGA-based switch supporting 192 flows with 7.14% additional on-chip memory versus conventional ATS, microsecond-level end-to-end delay, jitter within 5 μs in realistic TSN scenarios and high throughput. It does not expose the topology, traffic envelope, packet/link conditions, absolute latency distribution, clock/testbed details, formal schedulability proof or overload behavior. The evidence supports per-flow asynchronous TSN shaping, not demonstrated deterministic end-to-end guarantees across networks.

## Pareto-guided scheduling: choose placement and timing together

A directed acyclic graph describes tasks and their dependencies without a dependency cycle. Shared tasks can contribute to several output paths. Moving one task to a different processor or changing when it starts may improve one path while delaying another. Mapping chooses the execution resource; an offset shifts the scheduled release time relative to a reference.

[Hierarchical Pareto-Prompted Optimization](../observed-subthemes/real-time-and-networked-systems.md#paper-dac-2026-research2360) searches task mappings and then refines offsets for probabilistic automotive workloads. Pareto dominance means that one candidate is at least as good on every selected objective and better on at least one. A nondominated candidate is not beaten in that way by another candidate in the compared set; it need not be globally optimal.

The official description identifies a metaheuristic, not language-model prompting. It reports production navigation-on-autopilot workloads on NVIDIA Orin-N-based vehicles, with up to 12% lower mean latency and 15% lower 99th-percentile latency than an industrial static baseline. The actual constraints, distribution estimation, trial counts, and search cost are absent. Its statement that all constraints were met cannot be expanded into a universal deadline guarantee. [Official scheduling description](https://63dac.conference-program.com/presentation/?id=RESEARCH2360&sess=sess115).

Probabilistic evaluation requires checking the slow cases and changes in execution conditions. A distribution learned under one interference pattern may be inaccurate under another. Separate the expense of finding a schedule from the overhead of executing it, and state whether adaptation occurs before deployment or during operation.

<span id="explanation-dac-2026-research2360"></span>

## Hierarchical Pareto scheduling: a non-dominated DAG schedule is not automatically deadline-safe

An automotive sensor-to-actuator pipeline can be represented as a directed acyclic graph (DAG). Nodes are tasks, edges carry precedence or data dependencies, and shared tasks can lie on multiple end-to-end paths. Mapping chooses which processor or accelerator runs each task; an offset chooses when that task is released relative to other work. A choice that improves one path can delay another, and variable execution times make the slow tail more important than the average alone.

The paper is described as a Pareto-prompted metaheuristic with hierarchical mapping-then-offset refinement. Here “prompted” identifies the search strategy; the captured description does not establish an LLM component. Pareto dominance retains a candidate that is no worse on the selected objectives and better on at least one, but a candidate can be non-dominated only within the explored population and still miss a feasible or globally better schedule. The method must specify task/resource representation, precedence, resource and memory constraints, interference, priority, offset legality, objective normalization, repair, search budget and whether adaptation is offline or online.

The first gate is schedule feasibility. Verify every dependency, resource assignment, release/offset, synchronization point, buffer, priority and deadline on the deployed runtime. Report rejected and repaired candidates, resource conflicts, deadline misses, path completion times and whether all shared sensor-to-actuator paths—not only a selected objective—meet their constraints. “All constraints satisfied” is meaningful only when the constraints and the execution boundary are explicit and independently checked.

The second gate is probabilistic timing validity. Calibrate execution-time distributions on held-out traces and test temperature, DVFS, memory/interconnect contention, sensor load, software versions and workload shifts. State whether p99 means an empirical quantile, a confidence bound or a modeled percentile, and report p50/p95/p99/p99.9 latency, worst observed response, deadline-miss probability, calibration error and per-DAG/path results. A lower 99th percentile can coexist with rare but unacceptable misses or with a changed denominator.

Search and runtime costs must be separated. Include mapping search, offset refinement, Pareto filtering, trace collection, schedule deployment, runtime monitoring, rescheduling, synchronization and fallback. Compare the industrial static baseline, deterministic scheduling and single-objective optimization with identical DAGs, execution traces, deadlines, hardware, priority policy, interference, warm-up and end-to-end latency boundary. Report the distribution of outcomes and the cost of maintaining the schedule, not only the best improvement.

The official description reports production navigation-on-autopilot workloads on NVIDIA Orin-N-based vehicles, says the constraints were satisfied, and reports up to 12% lower mean latency and 15% lower 99th-percentile latency than an industrial static baseline. It does not expose absolute latency, deadline misses, execution-time calibration, search cost, energy, resource configuration, per-DAG results or robustness conditions. The evidence supports hierarchical Pareto scheduling exploration, not demonstrated probabilistic deadline guarantees or portable automotive real-time safety.

## Cause-effect chains: faster tasks can change which data gets used

Periodic tasks may exchange data by reading a stored value when they run. Changing a task's timing can change which producer output a consumer reads. A local speed improvement can therefore alter the sequence of task instances carrying an event through the system, rather than merely shortening an unchanged sequence.

[Scheduling Cause-Effect Chains Without Timing Anomalies](../observed-subthemes/real-time-and-networked-systems.md#paper-dac-2026-research378) has a recovered manuscript. Section 2.1 assumes periodic tasks on one core with fixed-priority scheduling and bounded execution times. Section 4 fixes producer-consumer relations using deterministic data flow: offline scheduling identifies the intended relations, modified task attributes preserve execution order, and multiple buffers preserve the intended input versions.

Section 5.3, Theorem 5.4, derives the maximum reaction time from the all-worst-case-execution schedule under this treatment. The result depends on the model and the implemented communication rules; it is not a theorem for arbitrary multicore or networked systems. Section 6 evaluates synthetic task sets and chains derived from automotive benchmark configurations, rather than establishing vehicle-level validation. [Manuscript, Sections 2.1, 4, 5.3, and 6](https://arxiv.org/html/2604.09102v1).

The implementation question is whether buffer use, task overhead, and execution-time bounds match the analyzed model. A mathematically valid bound does not survive an unmodeled cost merely because that cost is usually small.

<span id="explanation-dac-2026-research378"></span>

## Cause-effect scheduling: eliminating timing anomalies is a model-bound causality result, not a universal deadline guarantee

In a reactive system, a cause-effect chain follows a particular producer output through one or more consumers to an observed response. Periodic tasks may read whichever producer value is available when they execute. If one task becomes faster, the consumer can read a different producer instance; the measured chain has changed even if each individual execution took less time. This is a timing anomaly: local progress does not necessarily shorten the end-to-end reaction time.

The paper is described as identifying two basic causes of these anomalies and using Deterministic Data Flow (DDF) to eliminate them with small average-latency loss. The recovered manuscript describes offline scheduling that fixes intended producer-consumer relations, modified task attributes that preserve execution order, and multiple buffers that preserve the intended input versions. This is a causality and data-flow contract, not merely a priority tweak. It must define release/finish semantics, overwrites, buffer ownership, chain boundaries, preemption and what happens when a task misses a period.

The first gate is event-level correctness. Trace task instances, not only task durations, under faster and slower executions, preemption, simultaneous chains, missed periods and buffer pressure. Verify that each consumer reads the intended producer version, that DDF does not drop or duplicate events, and that the measured reaction time refers to the same cause-effect relation before and after scheduling. A shorter local task or lower average latency is not evidence if the system is answering from a different input instance.

The second gate is the timing-model boundary. The recovered manuscript assumes periodic tasks on one core with fixed-priority scheduling and bounded execution times, and derives a maximum reaction time from the all-worst-case-execution schedule under the DDF treatment. State whether bounds are WCET, measured values or estimates, and include context switches, buffer access, communication, synchronization, scheduler work and instrumentation. The result should not be generalized to arbitrary multicore or networked systems without accounting for shared resources, clock synchronization, migration and a new proof.

Evaluate synthetic and automotive-derived chains outside the design set with all-worst-case and mixed traces, priority/utilization changes, buffer sizes and deadlines. Report maximum and quantile reaction time, jitter, deadline-miss rate, utilization, average-latency cost and buffer/memory overhead. Compare priority scheduling, anomaly-oblivious chains and methods that remove anomalies by sacrificing average latency under the same causality and deadline contract; report failed and infeasible cases rather than only a derived upper bound.

The official description claims lower maximum end-to-end latency, average latency and jitter than the state-of-the-art method. The recovered manuscript provides a formal TA-free property and Theorem 5.4 under its single-core/fixed-priority/bounded-execution/DDF assumptions, with synthetic and automotive-derived evaluation, but the captured evidence does not provide complete numerical bounds, deadline-miss tables, implementation overhead, multicore/network results or vehicle-level validation. The evidence supports a model-bounded DDF cause-effect scheduling direction, not demonstrated vehicle-level real-time safety or universal deadline guarantees.

## What the three studies establish together

My synthesis is that predictable timing requires control over both competition for resources and the exact movement of data. The studies address queues, task placement and offsets, and producer-consumer relations respectively. Their results cannot be ranked by comparing the smallest reported latency percentage.

For an end-to-end assessment, define the starting event, final response, accepted inputs, resource interference, timing model, and deadline. Then distinguish observed behavior from guarantees and verify that implementation overhead is included. A long-term trend would additionally require comparable evidence across editions, not just three current proposals.

Sources were refreshed on 2026-09-07. The manuscript supplies section-backed reasoning for cause-effect chains; PFATS and Pareto scheduling remain official-description evidence. The older cards below preserve the original capture and may still state that results were missing then. The refreshed explanation supersedes those omissions where explicitly cited, without claiming independent reproduction or a complete proof audit.

## Compare the results carefully

First identify the inputs and required output quality. Then identify the limited resource: time, memory, communication, energy, circuit area, or correctness coverage. Ask which part of the method reduces that cost and which new cost it adds. Compare numbers only when the experiments hold these conditions sufficiently similar.

A conference description may explain the proposal while omitting the full experiment. An author preprint link may have been coded from its abstract. The source classification does not by itself establish that every table was read. Missing locations remain visible below.

## Complete captured evidence

These are evidence records, not substitutes for the explanations above. Each record preserves its problem, proposed method, measurements, comparison conditions, and source limits. A populated record does not establish that its mechanism has been fully explained or independently verified.

<span id="paper-dac-2026-research163"></span>

### Per Flow Asynchronous Traffic Shaping in Time Sensitive Networking

DAC 2026 · Record: `dac-2026-research163`

[Read the step-by-step explanation](#explanation-dac-2026-research163)

**Updated source-backed reading card**

Reviewed 2026-09-09. Deepens the PFATS treatment into a paper-level reading; separates per-flow eligibility, queue isolation and SSRM scheduling from admission contracts, link contention, schedulability, buffer behavior, clock assumptions and hardware/testbed guarantees, while preserving the 192-flow, 7.14%, microsecond and 5 μs claims.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Asynchronous traffic shaping can bound delay without global synchronization, but grouping flows in shared queues creates inter-flow interference and delay jitter for time-critical traffic; the design must control eligibility and service without assuming a globally synchronized clock.

**Mechanism / artifact:**

PFATS: per-flow asynchronous traffic shaping with a per-flow frame eligibility-time calculator, per-flow queues and a Synchronous Shift Register Matrix (SSRM) scheduler implemented on an FPGA-based TSN switch; eligibility semantics, queue admission, clock model, arbitration, buffer sizing, link scheduling and packet-drop behavior are unspecified.

**Workload — the work tested:**

Time-Sensitive Networking scenarios with asynchronous flows; flow count, packet sizes, periods/bursts, arrival contract, priorities, deadlines, topology/hops, link rates, competing traffic, queue occupancy, traffic traces, offered load and scenario duration are unspecified.

**Hardware and manufacturing assumptions:**

FPGA-based TSN switch with per-flow queues and SSRM scheduling; FPGA family/frequency, pipeline latency, on-chip memory organization, port count, PHY/link rates, clock domains, timestamp/eligibility precision, switch fabric, host configuration, buffering and testbed instrumentation are unspecified.

**Baseline — the comparison method:**

Conventional grouped-queue asynchronous traffic shaping (ATS)

Synchronous traffic shaping

Best-effort Ethernet

Same flow contracts, topology, packet sizes, link rates, clock assumptions, buffer budget, traffic traces, scheduler implementation and end-to-end measurement boundary are unspecified

**Reported measurements:**

The official description reports support for 192 flows with 7.14% additional on-chip memory versus conventional ATS, microsecond-level end-to-end delay, delay jitter bounded within 5 μs in realistic TSN scenarios and high throughput; it reports no absolute latency distribution, formal bound, utilization, throughput value, drops, buffer occupancy, schedulability or hardware-condition matrix.

**Limits on the conclusion:**

Per-flow queues remove one source of inter-flow interference but do not remove contention on physical links, switch resources or downstream queues. Define flow arrival/service contracts, eligibility-time computation, arbitration, priority, clock domains, synchronization assumptions, propagation and serialization delay; derive a worst-case end-to-end bound and test deadline misses under admissible and overload traffic.

A 5 μs jitter bound must define jitter, observation window, percentile versus worst case, timestamp points, packet population and traffic envelope. Report latency distributions, queue occupancy, drops, throughput, link utilization, head-of-line behavior, buffer requirements and behavior when a flow exceeds its contract; supporting 192 flows does not establish 192 arbitrary-rate flows.

The official description reports an FPGA switch, 192 flows, 7.14% additional memory, microsecond-level delay, 5 μs jitter and high throughput, but omits topology, load, packet/link conditions, absolute results, clock/testbed details, formal schedulability and overload validation. The evidence supports per-flow asynchronous TSN shaping, not demonstrated deterministic end-to-end guarantees across networks.

**Source and location**

Evidence tier: Primary captured official DAC description plus existing authored tsn discussion; no full paper extraction, schedulability proof, traffic condition matrix or independent hardware validation. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH163&sess=sess171)

DAC 2026 official description; existing real-time-and-networked-systems chapter discussion; captured Problem, Mechanism / artifact, Workload, Hardware, Baseline, Measurements and Limits fields; no manuscript pages, formal bound, traffic trace, queue trace or independent FPGA testbed report.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** synchronous traffic shaping

best-effort Ethernet

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH163

**Hardware or process assumptions:** TSN switches and links with per-flow shaping; protocol and clock assumptions are unspecified.

**Limits:** No latency bounds, jitter, utilization, drops, or hardware results are reported.

Asynchrony can complicate global guarantees.

Official description only; schedulability analysis and testbed validation are required.

**Method or artifact:** Per-flow asynchronous traffic-shaping mechanism.

**Metrics:** Latency determinism and traffic efficiency are claimed qualitatively

**Problem:** Time-sensitive networks must meet deterministic latency while handling asynchronous flows and changing traffic.

**Workload or benchmark:** Time-sensitive networking flows; topology, deadlines, traffic, and baselines are unspecified.

</details>

<span id="paper-dac-2026-research2360"></span>

### Hierarchical Pareto-Prompted Optimization for Probabilistic DAG Scheduling on Real-Time Systems

DAC 2026 · Record: `dac-2026-research2360`

[Read the step-by-step explanation](#explanation-dac-2026-research2360)

**Updated source-backed reading card**

Reviewed 2026-09-09. Deepens the hierarchical Pareto DAG-scheduling treatment into a paper-level reading; separates joint task mapping/offset refinement and Pareto metaheuristic search from execution-time calibration, deadline-miss probability, WCET/tail semantics, resource/interference constraints, search/runtime overhead and automotive deployment robustness, while preserving the Orin-N, 12% and 15% claims.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Automotive navigation-on-autopilot workloads form DAGs whose shared tasks can couple multiple sensor-to-actuator paths; probabilistic execution times make a mapping and offset that looks good on average vulnerable to tail latency and deadline violations.

**Mechanism / artifact:**

Hierarchical Pareto-prompted metaheuristic that first searches task-to-resource mappings and then refines task offsets, using Pareto dominance to retain non-dominated schedules for probabilistic real-time DAG objectives; the term prompted describes the search strategy rather than an established LLM component. Objective definitions, constraint handling, execution-time model, interference model, search budget, feasibility repair and online/offline adaptation are unspecified.

**Workload — the work tested:**

Production navigation-on-autopilot workloads modeled as real-time DAGs and evaluated on NVIDIA Orin-N-based vehicles; DAG count/structure, shared-task paths, task periods/deadlines, execution-time distributions, sensor/actuator rates, processor resources, workload traces, interference and deployment duration are unspecified.

**Hardware and manufacturing assumptions:**

Heterogeneous NVIDIA Orin-N automotive platform with mapped real-time tasks and probabilistic execution durations; CPU/GPU/accelerator partition, cores/clocks, DVFS, memory/interconnect contention, OS/runtime, scheduler, thermal state, fault model, time synchronization and timing instrumentation are unspecified.

**Baseline — the comparison method:**

Industrial static baseline

Deterministic DAG scheduling

Single-objective mapping or offset optimization

Same DAGs, execution-time traces/distributions, deadlines, resource assignment, interference, warm-up, priority policy, hardware/runtime, objective constraints and end-to-end latency boundary are unspecified

**Reported measurements:**

The official description reports that all stated constraints were satisfied and that the method reduces mean latency by up to 12% and 99th-percentile latency by up to 15% relative to an industrial static baseline on Orin-N-based vehicles; it does not report absolute latency, deadline-miss probability, worst-case response time, energy, search/runtime cost, distribution calibration, per-DAG results, robustness or deployment duration.

**Limits on the conclusion:**

A Pareto schedule is non-dominated only relative to the candidates and objectives searched; it is not automatically globally optimal or deadline-safe. Define every objective, deadline, precedence, resource, memory, priority, synchronization and interference constraint, and report feasibility repairs, rejected candidates and deadline misses. Validate the selected mapping and offsets with cycle-level or trace-based execution rather than only the optimizer's model.

Probabilistic execution times must be calibrated on held-out traces and checked under temperature, DVFS, contention, software version, sensor load and workload shifts. Report the distribution, quantile/confidence semantics, calibration error, p50/p95/p99/p99.9 latency, worst observed response, deadline-miss rate and tail across each sensor-to-actuator path. A 99th-percentile reduction can coexist with unacceptable rare misses or a changed deadline denominator.

Separate offline search cost from online scheduler overhead and execution benefit. Include hierarchical mapping search, offset refinement, Pareto filtering, model/traces collection, schedule deployment, runtime monitoring, rescheduling, synchronization and fallback. Compare static and single-objective baselines with equal hardware, task priority, interference, deadline, trace, warm-up and measurement boundaries; report per-DAG outcomes rather than only a best improvement.

The official description reports production navigation-on-autopilot workloads on Orin-N-based vehicles, all constraints satisfied, up to 12% lower mean latency and 15% lower 99th-percentile latency, but omits constraints, absolute values, deadline misses, execution-time calibration, search cost, energy, resource configuration and robustness. The evidence supports hierarchical Pareto scheduling exploration, not demonstrated probabilistic deadline guarantees or portable automotive real-time safety.

**Source and location**

Evidence tier: Primary captured official DAC description plus existing authored real time scheduling discussion; no full paper extraction, reproduced pareto search, deadline miss trace or safety case validation. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH2360&sess=sess115)

DAC 2026 official description; existing real-time-and-networked-systems chapter framing; captured Problem, Mechanism / artifact, Workload, Hardware, Baseline, Measurements and Limits fields; no manuscript pages, execution-trace distribution, schedulability proof or independent Orin-N run.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** deterministic DAG scheduling

single-objective optimization

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH2360

**Hardware or process assumptions:** Heterogeneous real-time platform with probabilistic task durations; timing and fault assumptions are unspecified.

**Limits:** No deadline miss, energy, robustness, runtime, or Pareto-front results are reported.

Probabilistic models may be miscalibrated in deployment.

Official description only; trace-based validation is required.

**Method or artifact:** Hierarchical Pareto-prompted scheduling optimization.

**Metrics:** Schedulability and Pareto quality are claimed qualitatively

**Problem:** Real-time DAG schedules must trade latency, energy, and reliability under probabilistic execution times.

**Workload or benchmark:** Probabilistic real-time task DAGs; processors, deadlines, and baselines are unspecified.

</details>

<span id="paper-dac-2026-research378"></span>

### Scheduling Cause-Effect Chains Without Timing Anomalies in End to End Latency

DAC 2026 · Record: `dac-2026-research378`

[Read the step-by-step explanation](#explanation-dac-2026-research378)

**Updated source-backed reading card**

Reviewed 2026-09-09. Deepens the cause-effect scheduling treatment into a paper-level reading; separates timing-anomaly causes, deterministic data flow, buffer/order preservation and the worst-case reaction-time theorem from single-core/fixed-priority assumptions, execution-time validity, multicore/network generalization, implementation overhead and vehicle-level validation.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Reactive systems must preserve producer-consumer causality while meeting end-to-end timing constraints; a local reduction in task execution time can change which periodic producer instance a consumer reads and paradoxically increase the observed cause-effect latency or its upper bound.

**Mechanism / artifact:**

Timing-anomaly-aware cause-effect chain scheduling using two identified anomaly causes and Deterministic Data Flow (DDF); the recovered manuscript describes offline scheduling that fixes producer-consumer relations, modified task attributes that preserve execution order and multiple buffers that preserve intended input versions, with a formal timing-anomaly-free property and worst-case reaction-time derivation. Platform, communication, implementation overhead and extensions beyond the stated model are bounded by the manuscript assumptions.

**Workload — the work tested:**

Periodic cause-effect task chains evaluated on synthetic task sets and chains derived from automotive benchmark configurations; task periods/priorities, chain topology, core/platform, execution-time bounds/distributions, deadlines, buffer sizes, workload scale, communication and baseline configurations are partly unspecified in the captured record.

**Hardware and manufacturing assumptions:**

Recovered manuscript Section 2.1 assumes periodic tasks on one core with fixed-priority scheduling and bounded execution times; communication is implemented with deterministic data-flow rules and multiple buffers. Multicore, network, cache, clock, preemption, OS/runtime, synchronization, buffer-memory and instrumentation assumptions are not established by the captured evidence.

**Baseline — the comparison method:**

Priority scheduling

Timing-anomaly-oblivious cause-effect chain scheduling

Methods that eliminate anomalies by sacrificing average latency

Same task sets, producer-consumer relations, execution-time bounds, priorities, core/platform, buffer/memory budget, deadline definition, implementation overhead and measurement boundary are unspecified

**Reported measurements:**

The official description claims lower maximum end-to-end latency, average latency and latency jitter than the state-of-the-art method, and the recovered manuscript's Theorem 5.4 derives a maximum reaction time from an all-worst-case-execution schedule under the stated DDF treatment; the record does not report numerical bounds, deadline misses, utilization, jitter distribution, overhead, multicore/network results or vehicle-level validation.

**Limits on the conclusion:**

A cause-effect latency is a relation between task instances, not merely the sum of task runtimes. Define which producer version each consumer may read, release/finish semantics, periodic sampling, buffers, overwrites, priorities and chain boundaries. Verify DDF with traces under faster/slower tasks, preemption, missed periods, buffer pressure and simultaneous chains; a local speedup must not silently change the event being measured.

The formal upper-bound result is conditional on the recovered model: periodic tasks, one core, fixed priorities, bounded execution times and the implemented deterministic communication/buffer rules. State whether execution times are WCET bounds, measured values or estimates, and include scheduling, buffer access, context-switch, communication, synchronization and instrumentation costs. The theorem should not be generalized to arbitrary multicore, networked or dynamic systems without a new proof.

Validate anomaly elimination on task sets and chains outside the design set, with all-worst-case and mixed execution traces, priority/utilization changes, buffer sizes and deadlines. Report maximum/quantile/average reaction time, jitter, deadline-miss rate, utilization and the cost in average latency or memory. Compare anomaly-oblivious and anomaly-sacrificing baselines at the same causality and deadline contract.

The evidence supports a formally reasoned DDF treatment under stated single-core timing assumptions and synthetic/automotive-derived experiments, not demonstrated vehicle-level real-time safety, multicore/network portability or independently measured deadline guarantees. The official record provides no numerical latency bounds or schedulability table.

**Source and location**

Evidence tier: Primary captured official DAC description plus recovered manuscript backed chapter extraction; theorem and experiments are bounded to the stated single core/fixed priority/ddf model, with no independent multicore/network or vehicle validation. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH378&sess=sess171)

DAC 2026 official description plus recovered manuscript Sections 2.1, 4, 5.3/Theorem 5.4 and 6; existing real-time-and-networked-systems chapter; no independent trace run, vehicle deployment or complete numerical schedulability table.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** priority scheduling

timing-anomaly-oblivious chain scheduling

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH378

**Hardware or process assumptions:** Networked or embedded real-time system; clocks, priorities, and execution-time assumptions are unspecified.

**Limits:** No latency bounds, jitter, deadline misses, utilization, or platform results are reported.

Guarantees depend on timing-model assumptions.

Official description only; trace-based real-time validation is required.

**Method or artifact:** Timing-anomaly-aware cause-effect chain scheduler.

**Metrics:** End-to-end latency predictability is claimed qualitatively

**Problem:** Reactive systems must schedule cause-effect chains without hidden timing anomalies that violate end-to-end deadlines.

**Workload or benchmark:** Real-time cause-effect chains; platform, deadlines, and baselines are unspecified.

</details>

## What remains to establish

Resolve unspecified workloads, comparison methods, resource budgets, and source locations before generalizing a reported gain. Multiple papers in this selected sample permit comparison of mechanisms, but do not by themselves establish recurrence across years or a long-term trend.

[All subthemes](../expanded-taxonomy-v1.md) · [Research directions](../directions/README.md)
