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
