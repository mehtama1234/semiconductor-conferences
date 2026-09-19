## Follow a request from arrival to a usable result

A request arrives, waits for resources, obtains its inputs, runs computation, and produces an output. Some applications then need another step: a robot must apply the command, a database must make an update recoverable, or a user must receive the answer over a network. Measuring only the arithmetic omits part of what the application needs completed.

Suppose a request waits 20 milliseconds, transfers data for 10, computes for 30, and returns its result in 5. Its elapsed time is 65 milliseconds if these stages are sequential. Making computation three times faster reduces that total to 45 milliseconds, about 1.44× faster rather than 3×. Queueing may also change when service becomes faster, so the calculation is an illustrative fixed-wait example, not a prediction under arbitrary load.

The theme's current coded records are DAC records. Links to ISCA-backed explanations in neighboring themes below provide explicit cross-theme context; they do not change that sample into a balanced three-conference comparison. All numerical examples not identified as paper results are teaching calculations.

## Define the unit of useful work

Requests are not necessarily equal-sized units. One language-model request may contain a short prompt and long answer; another may contain a long prompt and short answer. One image can require different processing from another. Two queues containing ten requests each can therefore contain very different amounts of remaining work.

A rate must name its unit: requests per second, input tokens per second, output tokens per second, processed frames per second, or successfully completed tasks. None can be substituted for another without the workload and conversion rule. Even equal output counts can conceal unequal output quality.

Offline processing begins with work available and often seeks minimum total completion time. Online service additionally faces arrival times, waiting, and response constraints. A fast offline batch does not establish good online service when requests arrive irregularly or require different amounts of work.

## Throughput and response time can move in opposite directions

Imagine a machine completes a batch of four requests every 40 milliseconds. Its steady completion rate is 100 requests per second, giving ten milliseconds per request when dividing total time by count. But a request that begins processing with the batch waits 40 milliseconds for its result, even before counting time spent waiting for the batch to form. The reciprocal rate is not its response time.

A larger batch can make hardware more efficient by sharing setup or reusing weights. It can also require more memory, delay admission, or lengthen the time until any one request completes. Report both completed work and the distribution of request elapsed times.

The neighboring memory chapter's [lossless-weight-compression explanation](../observed-subthemes/memory-hierarchy-and-persistence.md#explanation-isca-2026-program-008) preserves a concrete manuscript case where throughput improves while median time per output token increases. The [robotics discussion of ActionFlow](../observed-subthemes/robotics-and-edge-ai.md#pipelining-throughput-is-not-a-timestamp) likewise separates a frame rate from an observation-to-command timestamp and retains a source timing-unit discrepancy. These records motivate a shared measurement obligation, not a directly comparable speed ranking.

## A deadline claim needs a population and a failure rule

A service-level objective specifies a target for a defined population, such as at least 99% of admitted requests completing within 100 milliseconds. It should state whether rejected requests, canceled requests, retries, and requests remaining unfinished at the end of measurement are counted. Excluding difficult work can improve reported latency without improving the service.

If 980 of 1,000 admitted requests finish within the target, attainment is 98%. That fails the illustrative 99% requirement even if the average response is fast. Reporting only completed requests can hide those still waiting. A percentile also needs a documented calculation and sufficient observations; a short run cannot establish behavior over every future burst.

The manuscript-backed [eLLM discussion](../observed-subthemes/datacenter-and-cloud-systems.md#ellm-let-temporary-activations-and-saved-attention-data-share-capacity) explicitly records how its latency thresholds and goodput are defined. Its goodput uses a particular attainment criterion, not a universal definition applicable to every service. The same discussion separates online service from offline decode and total-throughput results.

## Load changes the value of an optimization

Suppose a server can sustain 100 equal requests per second. At a continuing arrival rate of 110, pending work grows by roughly ten requests per second once sustained operation reaches capacity, assuming no rejection or cancellation. A tenfold faster routing decision cannot remove this service-capacity deficit if routing was not the limiting work.

Average arrivals below capacity do not prevent temporary queues. If 100 requests arrive together and each takes ten milliseconds on a serial server, their completion times range from ten to 1,000 milliseconds. The same 100 requests spread far enough apart can avoid that queue entirely. Arrival timing belongs in the workload definition alongside input size.

Routing and scaling act on this changing state. A router chooses a destination; a scaler changes available resources. Measurements can become stale before a decision takes effect. Starting a replica may involve allocation, loading, and initialization. The method must explain what happens during that delay and when no available choice can meet the target.

The [HW-Router discussion](../observed-subthemes/datacenter-and-cloud-systems.md#hw-router-choose-using-current-queues-as-well-as-model-capability) preserves its overload evaluation, quality definition, and differing timing boundaries. The [sMoE discussion](../observed-subthemes/datacenter-and-cloud-systems.md#smoe-scale-individual-experts-without-ignoring-the-rest-of-the-request) retains missing full-paper conditions. They address related allocation decisions without providing equivalent source depth or interchangeable service guarantees.

## Changing the model changes the comparison

A system may reduce cost by choosing a smaller model, omitting selected work, returning an answer early, or reducing numerical precision. These actions can change output quality as well as runtime. Faster execution of a fixed computation and cheaper execution of a modified computation are different claims.

If a benchmark score stays similar, examine what that score measures and which cases it averages. A small overall difference can coexist with a substantial regression on a difficult or important subset. A model-based judge supplies evidence under its judging procedure; it is not a universal correctness oracle.

The [SPADE explanation](../observed-subthemes/sparse-and-irregular-compute.md#explanation-dac-2026-research680) distinguishes similarity to a dense-generated output from perceptual quality. The [architecture theme](architecture-and-accelerators.md) explains the corresponding distinction between exact representation recovery and acceptable approximation. A systems result must attach its latency and cost to the output requirement actually evaluated.

## In a control system, the age of information matters

A robot's command depends on an observation made earlier. Even if a computation returns exactly the same numerical answer as a reference, additional delay can make that answer less appropriate for the current physical state. The relevant interval can include sensing, admission, processing, communication, and actuation.

For an illustrative constant-speed calculation, an object moving at one meter per second changes position by ten centimeters during a 100-millisecond delay. That does not establish a general safe deadline: acceleration, uncertainty, obstacles, and the controller's compensation all matter. It shows why equivalent numerical outputs at different times are not automatically equivalent physical behavior.

The [robotics chapter](../observed-subthemes/robotics-and-edge-ai.md) separates numerical behavior, information timing, and physical outcome. It also distinguishes training experiments from deployed robot decisions. Its reported simulations, hardware measurements, and missing physical conditions remain separate evidence tiers; this synthesis does not turn them into validated robot safety claims.

## Resource efficiency requires an explicit denominator

Power is energy consumed per unit time. Energy per completed task also depends on how long the task takes and what system components are included. A 100-watt device running for one second consumes 100 joules. A 60-watt device running for two seconds consumes 120 joules. Lower power does not necessarily mean less task energy.

Similarly, fewer servers can reduce cost while increasing interference between tenants. Better aggregate utilization can conceal worse response time for one application. The neighboring [Vistara explanation](../observed-subthemes/memory-hierarchy-and-persistence.md#explanation-isca-2026-program-045) links capacity-driven consolidation to per-container placement and service conditions. Additional capacity is valuable only if the resulting configuration still satisfies the required work and failure tolerance.

Count preparation, transfers, retries, idle capacity retained for bursts, and any externally performed computation within the declared accounting boundary. If billing units differ from physical resource use, report both definitions rather than calling them the same efficiency metric.

## Connect component evidence to application evidence

| Component observation | Application question still unanswered |
| --- | --- |
| A kernel finishes sooner | Does total request time improve after waiting, transfer, and return costs? |
| More requests fit in memory | Can the additional requests still meet their response and quality targets? |
| A router predicts lower latency | Does the prediction remain accurate after concurrent decisions and changing queues? |
| A batch produces more outputs per second | How old is each input when its output becomes usable? |
| A device draws fewer watts | What energy and complete-system cost are paid per acceptable result? |

These questions connect to the [memory theme](memory-interconnect-and-storage.md), [tooling theme](design-methodology-and-tooling.md), and [verification theme](verification-and-validation.md). The system inherits capacity limits, preparation costs, and correctness assumptions from those components. The relationship is a checklist for compatible evidence, not proof that independently proposed methods have been integrated.

## Long-term hypotheses and disconfirming tests

One hypothesis is that workload-aware allocation becomes more useful when request sizes, arrival rates, or model choices vary substantially. Compare adaptive and fixed policies at equal hardware and output requirements, including transition periods and observation overhead. It weakens where a fixed policy already meets the targets or adaptation costs more than it saves.

A second hypothesis is that capacity-saving methods increasingly trade individual response pace for aggregate service capacity. Test across input lengths, admission policies, and latency thresholds, retaining cases where no tradeoff appears. It weakens as a broad claim if matched systems consistently improve both without shifting quality or excluding difficult requests.

A third hypothesis is that acceleration for interactive and physical applications must optimize the time at which useful information becomes available, not merely execution rate. Test timestamped inputs and outputs together with task outcomes. It weakens as a distinguishing concern where timing changes do not affect usefulness under the application's actual constraints.

These are bounded interpretations, not demonstrated cross-edition trends. Equivalent collection across ISCA, DAC, and ICCAD, matched evidence depth, and clearly defined workload populations remain necessary. This theme's DAC-only coded sample cannot establish conference-wide prevalence or a three-conference direction by itself.

The cloud and robotics chapters provide substantive source-specific discussions, but many individual records and other systems branches remain shallow or condition-incomplete. This parent writeup does not complete their rewriting, source reconciliation, independent comprehension review, or scientific acceptance.
