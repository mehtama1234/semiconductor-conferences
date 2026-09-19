# Reliable and secure AI systems

This subject has 1 record in the selected sample. This page explains where it fits, then presents all captured paper evidence without shortening the measurements or limitations.

[Definitions used in the paper records](../reading-guide-v1.md)

## Understand the parent subject first

- [Power reliability and security](../themes/power-reliability-and-security.md)

## A model's stored numbers are part of its behavior

A neural network computes outputs from inputs using learned numerical parameters, usually called weights. A deep neural network, or DNN, applies several stages of such computation. Inference means evaluating the trained network on a new input. If a stored weight changes, the machine can execute its instructions correctly while evaluating a different network from the one that was validated.

A bit flip changes one binary digit in that stored representation. Its numerical effect depends on the number format and the bit position. In an unsigned eight-bit example, changing the lowest bit of zero produces 1; changing its highest bit produces 128. Signed and floating-point formats assign different meanings to their bits, so the format must be specified before reasoning about a fault's magnitude.

Numerical magnitude is only part of the problem. For a multiplication y = w × x, a change Δw produces Δy = Δw × x if x is unchanged. Later computations may reduce or amplify that difference, and a final decision may change when competing output scores are close. This elementary calculation explains why equal-sized storage errors need not have equal consequences. It is not a sensitivity formula recovered from the paper below.

## Random faults and deliberate attacks require different tests

A random-fault experiment samples changes from a stated distribution. An attack experiment allows an adversary to select changes under a stated access and effort limit. A method can tolerate most randomly chosen flips while remaining vulnerable to a carefully selected small set.

The attacker model therefore needs to say whether the adversary knows the weights and defense, can choose a bit address, can repeat changes, and can observe the defender's response. Software injection at arbitrary addresses tests a different capability from a physical fault mechanism restricted to particular locations. Neither experiment should silently stand in for the other.

The objective also matters. An attack that makes many predictions wrong differs from one that changes a chosen class or causes a particular input to receive an attacker-selected output. Average accuracy alone may conceal the latter. These distinctions define what evidence would support the word “secure”; they are not additional outcomes established by this subject's single paper.

<span id="explanation-dac-2026-research1284"></span>

## WFH-BFs: selective protection changes the network; it does not automatically repair corrupted weights

[WFH-BFs: Dynamic Defense Against DNN Bit-Flips via a Weight Function Hierarchy](../observed-subthemes/reliable-and-secure-ai-systems.md#paper-dac-2026-research1284) groups weights into an “Anchor Core” for representation, a class-sensitive tier for decisions, and a “Reservoir” for redundancy. Preparation strengthens the core and builds tolerance to pruning elsewhere; runtime checking protects the core while dynamic pruning changes the network in response to attacks.

The official description reports a 17.5× increase in attack cost, less than 1.4% accuracy drop under high-rate random errors, and reduced arithmetic operation count. It does not define attack cost, whether the accuracy change is relative or percentage points, the error rate, model and dataset choices, or complete execution overhead. These remain description-level claims, not page-backed measurements. [Official DAC description, Description section](https://63dac.conference-program.com/presentation/?id=RESEARCH1284&sess=sess152).

The available source does not specify the grouping algorithm, checker construction, or how pruning targets are selected. Searches for the exact title and author-associated manuscript did not recover a full paper. No particular error-correcting code, cryptographic check, or hardware memory technology should be inferred from the word “harden.”

## Why removing a damaged component can help without repairing it

Pruning removes selected weights or computation paths from use. It changes which calculation the network performs; it does not generally restore a corrupted weight's original bits. Recovery of useful predictions and exact repair of model state are different goals.

As independent reasoning, consider a damaged contribution w × x to a sum. Excluding it replaces its contribution with zero. That may be less harmful than using a badly corrupted value, but it also removes the useful contribution the original weight would have supplied. A successful removal policy therefore needs evidence about both the damage it avoids and the information it discards.

Preparation that teaches a network to tolerate removal could reduce this loss. It still needs testing across the intended inputs and across successive removal decisions. Components that appear dispensable on one evaluation set may matter for less frequent classes or for inputs outside that set. The source's functional tier names do not prove that roles are independent, fixed across workloads, or safe to remove without limit.

## Checking and response must happen before an unsafe result is used

An integrity check asks whether monitored state satisfies an expected condition. Detecting a mismatch does not necessarily identify the exact damaged location, recover the intended value, or determine which outputs were already affected. Those are separate responsibilities.

The timing relation is important. If checking is periodic, inference may use changed state before the next check. If checking precedes every use, its execution and memory-access costs must be included, including detection latency. A review must also establish what prevents damage to the checker, its reference information, and the pruning control state. These are questions for the missing implementation, not evidence of a demonstrated weakness in WFH-BFs.

Repeated adaptation needs a stopping rule. Removing more components can eventually leave insufficient computation for acceptable output quality. The system should define whether it reloads known-good state, refuses further predictions, or enters another validated operating mode. A continued numerical output is not sufficient evidence of successful recovery.

## Fewer operations do not establish lower end-to-end cost

GFLOPs denotes a count in billions of floating-point operations. A lower count can result from pruning while checking and reconfiguration add other work. Actual latency also depends on memory transfers and whether the machine efficiently executes the resulting irregular computation. Energy requires a defined measurement boundary rather than an operation-count substitution.

A meaningful comparison should include the clean, protected network before faults; the damaged network without defense; a protection method without dynamic removal; and the complete adaptive method. Match the initial model quality, number format, attack permissions, and stopping criteria. Report the time and resources required for preparation separately from per-inference cost and exceptional recovery work.

For random errors, record rates, locations, persistence, repeated trials, and variation in accuracy. For deliberate attacks, report success against the same target criterion and budget, including attacks adapted to the defense. A cost multiplier without its unit and baseline cannot show how difficult exploitation is in practice.

## The broader question is how much protection can be selective

This case connects reliability to model structure: protection might be allocated according to a component's effect on the computation rather than applied uniformly. The important test is whether the saved protection cost exceeds classification, checking, adaptation, and quality-loss costs under matched conditions. This is a bit-flip protection question as well as a model-quality question. That is a research question, not a demonstrated universal removal of the security–efficiency trade-off.

The refreshed description supersedes the historical card's statement that no numerical results are available. It does not resolve missing paper pages, threat assumptions, measured runtime and energy, or independent fault-injection validation. One selected paper supports this mechanism-level case study, not a longitudinal trend, not a general guarantee of bit-flip security, and not a general guarantee for secure AI systems.

## Compare the results carefully

First identify the inputs and required output quality. Then identify the limited resource: time, memory, communication, energy, circuit area, or correctness coverage. Ask which part of the method reduces that cost and which new cost it adds. Compare numbers only when the experiments hold these conditions sufficiently similar.

A conference description may explain the proposal while omitting the full experiment. An author preprint link may have been coded from its abstract. The source classification does not by itself establish that every table was read. Missing locations remain visible below.

## Complete captured evidence

These are evidence records, not substitutes for the explanations above. Each record preserves its problem, proposed method, measurements, comparison conditions, and source limits. A populated record does not establish that its mechanism has been fully explained or independently verified.

<span id="paper-dac-2026-research1284"></span>

### WFH-BFs: Dynamic Defense Against DNN Bit-Flips via a Weight Function Hierarchy

DAC 2026 · Record: `dac-2026-research1284`

[Read the step-by-step explanation](#explanation-dac-2026-research1284)

**Updated source-backed reading card**

Reviewed 2026-09-08. Deepens the existing WFH-BFs treatment into a paper-level reading; separates selective weight protection, fault detection, dynamic pruning, inference correctness, attack cost and end-to-end overhead, and preserves the missing paper and independent-validation boundary.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Bit-flip faults or attacks can corrupt DNN weights and degrade inference.

**Mechanism / artifact:**

Dynamic weight-function hierarchy for detecting or mitigating DNN bit flips, with Anchor Core, class-sensitive tier and Reservoir roles, preparation, runtime checking and dynamic pruning; grouping, checker, fault model and pruning policy are unspecified.

**Workload — the work tested:**

DNN inference under bit-flip faults; models, datasets, number format, fault locations/rates/persistence, random versus selected faults, target objective, repeated trials and threat model are unspecified.

**Hardware and manufacturing assumptions:**

Memory or accelerator supporting dynamic weight protection; memory technology, bit-address access, checker protection, detection timing, reconfiguration path, area, energy, latency and fault injection mechanism are unspecified.

**Baseline — the comparison method:**

Unprotected DNN

Static error mitigation

Clean/protected/damaged networks, static-only defense, equal initial accuracy, fault distribution, adaptive attacker, preparation and per-inference/recovery overhead boundaries are unspecified

**Reported measurements:**

17.5x increase in attack cost, less than 1.4% accuracy drop under high-rate random errors and reduced arithmetic operation count are reported; cost unit, accuracy denominator, attack success, detection latency, area, energy, runtime and complete overhead are not defined.

**Limits on the conclusion:**

Pruning removes a damaged contribution rather than restoring its original value. Selective protection must show that the Anchor Core, class-sensitive tier and Reservoir preserve the intended task under the stated fault distribution and do not hide failures on rare classes or adaptive inputs.

Detection timing, checker integrity, pruning control state, stopping rule, repeated faults and attacker knowledge determine whether unsafe inference occurs before response. Operation count is not end-to-end latency or energy when checking, irregular execution and reconfiguration add work.

No attack success, accuracy loss, detection latency, area, or energy results are reported. Protection may trade accuracy for overhead; the evidence supports a selective DNN fault-mitigation direction, not a general guarantee of bit-flip security or exact weight repair.

**Source and location**

Evidence tier: Primary captured official DAC description plus existing chapter level wfh bfs discussion; no full paper extraction, reproduced fault injection, checker implementation or independent adaptive validation. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/presentation/?id=RESEARCH1284&sess=sess152)

DAC 2026 official description/Description section and existing chapter-level WFH-BFs discussion; captured Problem, Mechanism / artifact, Workload, Hardware, Baseline, Measurements and Limits fields; no manuscript pages.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** unprotected DNN

static error mitigation

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH1284

**Hardware or process assumptions:** Memory or accelerator supporting dynamic weight protection; fault rate and overhead assumptions are unspecified.

**Limits:** No attack success, accuracy loss, detection latency, area, or energy results are reported.

Protection may trade accuracy for overhead.

Official description only; fault-injection validation is required.

**Method or artifact:** Dynamic weight-function hierarchy for detecting or mitigating DNN bit flips.

**Metrics:** Bit-flip resilience is claimed qualitatively

**Problem:** Bit-flip faults or attacks can corrupt DNN weights and degrade inference.

**Workload or benchmark:** DNN inference under bit-flip faults; models, fault locations, and threat model are unspecified.

</details>

## What remains to establish

Resolve unspecified workloads, comparison methods, resource budgets, and source locations before generalizing a reported gain. This subject is represented by one paper and supports a case study, not evidence of recurrence or a long-term trend.

[All subthemes](../expanded-taxonomy-v1.md) · [Research directions](../directions/README.md)
