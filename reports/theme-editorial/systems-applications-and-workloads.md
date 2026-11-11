## Follow a request from arrival to a usable result

A request spends time in several stages, so speeding up one stage speeds up the whole far less.

A request:

1. arrives;
2. waits for resources;
3. gets its inputs;
4. runs its computation;
5. produces an output.

Some applications need one more step. A robot must apply the command. A database must make an update recoverable. A user must receive the answer over a network. Measuring only the arithmetic leaves out part of what the application needs done.

> **Worked example (illustrative fixed wait).** A request waits 20 milliseconds, transfers data for 10, computes for 30 and returns its result in 5.
>
> - Total, if the stages run one after another: 20 + 10 + 30 + 5 = **65 milliseconds**.
> - Make computation three times faster: 20 + 10 + 10 + 5 = **45 milliseconds**.
> - That is about **1.44×** faster overall, not 3×.

Queueing may also change once service gets faster. So this is a teaching example, not a prediction under any load.

**Be careful:** this theme's coded records are all DAC records. Links below to ISCA-backed explanations in neighboring themes give cross-theme context. They do not turn the sample into a balanced three-conference comparison. Numerical examples not marked as paper results are teaching calculations.

## Define the unit of useful work

Requests differ in size, so every rate must say what it counts.

Requests are not equal units:

- One language-model request may have a short prompt and a long answer; another the reverse.
- One image may need different processing from another.

So two queues of ten requests each can hold very different amounts of work.

A rate must name its unit. Possible units include:

- requests per second;
- input tokens per second;
- output tokens per second;
- processed frames per second;
- successfully completed tasks.

None can stand in for another without the workload and a conversion rule. Even equal output counts can hide unequal output quality.

**Offline processing** starts with all the work available, and usually aims for the shortest total completion time. **Online service** also faces arrival times, waiting and response limits. A fast offline batch does not show good online service when requests arrive irregularly or need different amounts of work.

## Throughput and response time can move in opposite directions

Finishing more requests per second can still make each request wait longer.

> **Worked example.** A machine finishes a batch of four requests every 40 milliseconds.
>
> - Steady rate: 4 ÷ 0.04 s = **100 requests per second**, or 10 milliseconds per request on average.
> - But a request that starts with the batch waits **40 milliseconds** for its result.
> - That is before counting the wait for the batch to form.
>
> The reciprocal rate is not its response time.

A larger batch can make hardware more efficient, by sharing setup or reusing weights. It can also:

- need more memory;
- delay admission;
- lengthen the time until any one request finishes.

So report both completed work and the spread of request times.

Two neighboring records show this:

- The memory chapter's [lossless-weight-compression explanation](../observed-subthemes/memory-hierarchy-and-persistence.md#explanation-isca-2026-program-008) keeps a manuscript case where throughput improves while median time per output token rises.
- The [robotics discussion of ActionFlow](../observed-subthemes/robotics-and-edge-ai.md#pipelining-throughput-is-not-a-timestamp) separates a frame rate from an observation-to-command timestamp. It also keeps a timing-unit discrepancy in the source.

**Be careful:** these records set a shared measurement duty. They are not a directly comparable speed ranking.

## A deadline claim needs a population and a failure rule

A service target means something only if it says which requests count and what counts as missing it.

A **service-level objective** sets a target for a defined group. For example: at least 99% of admitted requests finish within 100 milliseconds. It should state whether these count:

- rejected requests;
- cancelled requests;
- retries;
- requests still unfinished when measurement ends.

Leaving out difficult work can improve reported latency without improving the service.

> **Worked example.** 980 of 1,000 admitted requests finish within the target.
>
> - Attainment: 980 ÷ 1,000 = **98%**.
> - That fails the illustrative 99% requirement, even if the average response is fast.

Reporting only completed requests can hide those still waiting. A percentile also needs a documented calculation and enough observations. A short run cannot show behavior over every future burst.

The manuscript-backed [eLLM discussion](../observed-subthemes/datacenter-and-cloud-systems.md#ellm-let-temporary-activations-and-saved-attention-data-share-capacity) records how its latency thresholds and goodput are defined. Its **goodput** (useful completed work) uses one particular attainment rule, not a universal definition. The same discussion keeps online service apart from offline decode and total-throughput results.

## Load changes the value of an optimization

When requests arrive faster than the server can handle, no speed-up elsewhere stops the queue growing.

> **Worked example.** A server can sustain 100 equal requests per second. Requests keep arriving at 110 per second.
>
> - Once the server is at capacity, waiting work grows by about 110 − 100 = **10 requests per second**, assuming no rejection or cancellation.
> - A tenfold faster routing decision cannot fix this, if routing was not the limiting work.

Average arrivals below capacity still allow temporary queues.

> **Worked example.** 100 requests arrive together. Each takes 10 milliseconds on a server that handles one at a time.
>
> - Completion times range from **10** to 100 × 10 = **1,000 milliseconds**.
> - The same 100 requests, spread far enough apart, avoid the queue entirely.

So arrival timing belongs in the workload definition, next to input size.

Routing and scaling act on this changing state:

- A **router** chooses where a request goes.
- A **scaler** changes the available resources.

Measurements can go stale before a decision takes effect. Starting a new copy of a service (a replica) may need allocation, loading and start-up. The method must say what happens during that delay, and when no available choice can meet the target.

- The [HW-Router discussion](../observed-subthemes/datacenter-and-cloud-systems.md#hw-router-choose-using-current-queues-as-well-as-model-capability) keeps its overload evaluation, quality definition and differing timing boundaries.
- The [sMoE discussion](../observed-subthemes/datacenter-and-cloud-systems.md#smoe-scale-individual-experts-without-ignoring-the-rest-of-the-request) notes the full-paper conditions still missing.

**Be careful:** they address related allocation decisions, but with different source depth. Their service guarantees are not interchangeable.

## Changing the model changes the comparison

Running a cheaper, changed computation is a different claim from running the same computation faster.

A system may cut cost by:

- choosing a smaller model;
- skipping selected work;
- returning an answer early;
- lowering numerical precision.

These can change output quality as well as run time.

If a benchmark score stays similar, check what the score measures and which cases it averages. A small overall difference can hide a large regression on a hard or important subset. A model used as a judge gives evidence under its judging procedure. It is not a universal correctness test.

The [SPADE explanation](../observed-subthemes/sparse-and-irregular-compute.md#explanation-dac-2026-research680) separates similarity to a dense-generated output from perceptual quality. The [architecture theme](architecture-and-accelerators.md) makes the matching split between exact recovery and acceptable approximation. A systems result must tie its latency and cost to the output requirement actually tested.

## In a control system, the age of information matters

For a robot, a correct answer that arrives late can still be the wrong action.

A robot's command depends on an earlier observation. Even an answer identical to a reference can suit the current physical state less if it comes later. The delay can include sensing, admission, processing, communication and actuation.

> **Worked example (illustrative, constant speed).** An object moves at 1 meter per second. During a 100-millisecond delay it moves 1 × 0.1 = **10 centimeters**.

This does not set a general safe deadline. Acceleration, uncertainty, obstacles and the controller's compensation all matter. It shows only that the same numbers at different times are not automatically the same physical behavior.

The [robotics chapter](../observed-subthemes/robotics-and-edge-ai.md) separates numerical behavior, information timing and physical outcome. It also separates training experiments from decisions on a deployed robot.

**Be careful:** its simulations, hardware measurements and missing physical conditions stay separate evidence tiers. This synthesis does not turn them into validated robot safety claims.

## Resource efficiency requires an explicit denominator

Efficiency needs a stated unit of useful work and a stated boundary of what is counted.

**Power** is energy used per unit of time. Energy per completed task also depends on how long the task takes, and which parts of the system are included.

> **Worked example.**
>
> - 100 watts for 1 second: **100 joules**.
> - 60 watts for 2 seconds: **120 joules**.
>
> Lower power does not necessarily mean less energy per task.

Likewise, fewer servers can cut cost while raising interference between tenants. Better total utilization can hide worse response time for one application. The neighboring [Vistara explanation](../observed-subthemes/memory-hierarchy-and-persistence.md#explanation-isca-2026-program-045) links capacity-driven consolidation to per-container placement and service conditions. Extra capacity is worth something only if the result still does the required work and tolerates the required failures.

Within the declared boundary, count:

- preparation;
- transfers;
- retries;
- idle capacity kept for bursts;
- any computation done elsewhere.

If billing units differ from physical resource use, report both, rather than calling them the same efficiency measure.

## Connect component evidence to application evidence

A faster component still leaves an application question open.

| Component observation | Application question still unanswered |
| --- | --- |
| A kernel finishes sooner | Does total request time improve after waiting, transfer, and return costs? |
| More requests fit in memory | Can the additional requests still meet their response and quality targets? |
| A router predicts lower latency | Does the prediction remain accurate after concurrent decisions and changing queues? |
| A batch produces more outputs per second | How old is each input when its output becomes usable? |
| A device draws fewer watts | What energy and complete-system cost are paid per acceptable result? |

These questions link to the [memory theme](memory-interconnect-and-storage.md), [tooling theme](design-methodology-and-tooling.md) and [verification theme](verification-and-validation.md). A system inherits capacity limits, preparation costs and correctness assumptions from its parts.

**Be careful:** the table is a checklist for compatible evidence. It is not proof that separately proposed methods have been integrated.

## Long-term hypotheses and disconfirming tests

Three readings are worth testing; each names what would weaken it.

| Hypothesis | Test | What would weaken it |
| --- | --- | --- |
| Workload-aware allocation helps more when request sizes, arrival rates or model choices vary a lot | Compare adaptive and fixed policies at equal hardware and output requirements, including transitions and observation overhead | A fixed policy already meets the targets, or adapting costs more than it saves |
| Capacity-saving methods increasingly trade each request's pace for total service capacity | Test across input lengths, admission policies and latency thresholds, keeping cases with no trade-off | Matched systems keep improving both, without shifting quality or excluding hard requests |
| For interactive and physical applications, speed-ups must target when useful information is ready, not just execution rate | Test timestamped inputs and outputs together with task outcomes | Timing changes do not affect usefulness under the application's real constraints |

These are bounded interpretations, not demonstrated cross-edition trends. They still need equivalent collection across ISCA, DAC and ICCAD, matched evidence depth, and clearly defined workload populations.

**Be careful:** this theme's DAC-only coded sample cannot show conference-wide prevalence, or a three-conference direction, by itself.

The cloud and robotics chapters give substantive source-specific discussions. Many individual records and other systems branches are still shallow or missing conditions. This parent writeup does not complete their rewriting, source reconciliation, independent comprehension review, or scientific acceptance.
