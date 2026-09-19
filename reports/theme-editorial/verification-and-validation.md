## Follow a claim from requirement to evidence

Consider a storage unit that accepts a write of value 7 to address A. A later read of A should return 7 under a specified set of conditions: the write completed, no intervening write changed A, the read was permitted, and no failure outside the contract occurred. Without those conditions, a comparison with 7 may report an allowed behavior as a defect or accept behavior that should have been rejected.

A verification method must make five things explicit: what object is under test, what behavior is required, what inputs and starting states are allowed, what execution is represented, and what observations decide the result. These are connected obligations. Improving test generation does not repair a wrong expected result; a correct expected result cannot detect an error that the observation omits.

The examples below are independent teaching constructions. The linked paper explanations retain their manuscript locations, reported results, and unresolved discrepancies. This parent discussion connects their mechanisms without claiming a reproduced combined system or exhaustive verification.

## The object being checked determines what a failure means

A processor implementation executes instructions using a particular circuit. A reference instruction model computes the allowed software-visible behavior without necessarily representing that circuit's timing. Comparing them can reveal an architectural disagreement. It does not require their internal signals or clock-by-clock behavior to match.

Firmware testing asks a different question: does software behave correctly when interacting with devices? A peripheral model may provide input bytes, status flags, and interrupts. A software crash in that environment is not automatically a circuit defect, and a model reaching more software branches is not processor-state coverage.

[RISCSmith](../observed-subthemes/processor-and-rtl-verification.md#explanation-dac-2026-research150) and [LiFU](../observed-subthemes/processor-and-rtl-verification.md#explanation-dac-2026-research2533) examine processor testing. The [SystemC embedded-fuzzing explanation](../observed-subthemes/processor-and-rtl-verification.md#explanation-dac-2026-research616) concerns firmware interacting with peripheral models. Their placement in one chapter permits a comparison of testing mechanisms, not a merger of their bug counts or coverage denominators.

## A test needs both a path to the error and a way to observe it

Suppose an arithmetic operation should write 5 to a register but writes 6. A subsequent instruction clears the register to zero. Comparing only the final register value sees agreement. Comparing after the arithmetic operation sees a disagreement. More runs of the same final-state-only checker need not reveal this error.

Observation must also occur at the right semantic boundary. A processor can execute work internally and later discard it. Treating every temporary internal write as a committed instruction result can create false alarms. Conversely, observing only registers can miss an incorrect memory write or exception.

RISCSmith's recovered method explains why instruction dependencies and intermediate observations belong together: meaningful construction makes interactions reachable, and logging retains effects before later instructions erase them. Its [individual discussion](../observed-subthemes/processor-and-rtl-verification.md#explanation-dac-2026-research150) links the construction and logging method to manuscript Section 3 and distinguishes observed disagreement from confirmed responsibility for a defect.

The broader lesson is conditional. More observation can expose errors, but it can also increase execution overhead and produce more traces to analyze. Compare the number of distinct, independently supported findings per complete campaign budget, not merely the number of logged events.

## A reference is a checker, not unquestionable truth

Differential testing runs related inputs through two implementations and compares their observable behavior. A mismatch establishes that they differ under the comparison rule. It does not by itself identify which implementation is wrong. The reference, event matching, initial state, supported features, or test generator may contain the mistake.

Agreement is also limited evidence. Two implementations can share a mistaken interpretation or omit the same behavior. A third implementation helps only to the extent that its relevant assumptions and implementation are sufficiently independent. Counting agreeing tools cannot replace checking the requirement.

A useful failure report therefore records input bytes, initial state, configurations, revisions, permitted behaviors, the first relevant difference, and a replay procedure. Reduction removes unnecessary input while preserving the same failure condition. A shorter program that instead raises an unrelated exception has not preserved the finding.

Several reduced programs may expose one underlying cause. Suppose 100 failing inputs reduce to three distinct causes, of which two are confirmed against the specification and one remains disputed. The supported summary is two confirmed causes and one unresolved cause, not 100 newly discovered bugs. These counts are illustrative, not a result attributed to the linked papers.

## Coverage measures exploration within a definition

Line coverage counts whether selected source lines executed. Branch coverage concerns selected alternatives through control flow. State or transition coverage concerns defined states or changes between them. Each requires a denominator: what was counted, which points were excluded, and which points can actually be reached under the setup.

Reaching 90 of 100 recorded points gives 90% coverage. Reaching 950 of a different 1,000-point set gives 95%. Neither number alone says which campaign checked more meaningful behavior, whether either detected a fault, or whether their remaining points include the same critical case. A score becomes comparable only after matching its definition and target.

The manuscript-backed processor chapter gives a concrete boundary: RISCSmith's inspected coverage experiment measures the Spike reference model, whereas LiFU reports RTL-tool coverage with formal assistance. Their percentages cannot be ranked as measurements of one common state space. The [cross-paper discussion](../observed-subthemes/processor-and-rtl-verification.md#what-connects-the-three-proposals) preserves that distinction.

Coverage can still guide testing. A newly reached branch may justify retaining an input because it exposes behavior earlier tests missed. But treating every unreachable point as a failure of the generator wastes resources, while removing merely difficult points can inflate the score. Exclusion rules need evidence and must remain visible.

## Formal proof is conditional on a model and assumptions

A formal check can reason about all behaviors represented by a stated model under stated assumptions. The result concerns the property actually expressed, not every intended property of the eventual system. If the model excludes a relevant input or simplifies away a relevant interaction, a proof within that model does not cover the excluded case.

For a simple implication, consider: whenever a request is accepted, a response arrives within four cycles. If assumptions accidentally prohibit every accepted request, the implication can hold without exercising the intended obligation. A separate reachability check asking whether acceptance can occur helps expose this problem. It does not by itself establish that the remaining assumptions are realistic.

A bounded search that finds no violation in ten cycles establishes less than an unbounded proof. A failure appearing at cycle eleven remains outside that search. A solver timeout establishes neither correctness nor a counterexample; it is an unresolved check. The report must distinguish these outcomes rather than grouping them under a single success count.

Formal and simulation evidence can complement each other. Simulation can exercise a concrete environment and produce an executable trace. Formal reasoning can cover combinations within its model that random testing may miss. Their benefits depend on the relationship between models, assumptions, and properties, not on simply adding their coverage scores.

## The environment can create or conceal a failure

Suppose firmware reads a ready flag and then receives bytes from a device queue. A simulator that changes the flag independently of the queue may permit a state that the intended peripheral cannot produce. A reported crash from that state may indict the model rather than the firmware. A model that excludes a real unusual event can create the opposite problem: missed faults.

The SystemC study's [expanded explanation](../observed-subthemes/processor-and-rtl-verification.md#explanation-dac-2026-research616) separates functional peripheral behavior from cycle-accurate hardware timing. It also preserves the difference between detecting deliberately inserted bugs and discovering new bugs in unchanged software. Neither kind of experiment should silently substitute for the other.

False positives are reports that do not correspond to the relevant real fault; false negatives are faults the method misses. Fewer crash reports do not prove improvement in both. Determining either rate requires appropriate ground truth, including investigation beyond a favorable subset of outputs.

## Optimize the full investigation, not only test production

A campaign spends resources generating inputs, executing them, checking outputs, reducing failures, and resolving their causes. Faster generation can fill a queue without improving findings if execution or investigation is limiting. Remote model calls, parallel simulator workers, and human review remain costs even when one headline reports only test count.

As an illustrative comparison, 100 tests at one second each require 100 seconds of execution. Sixty tests at two seconds each require 120 seconds. Forty percent fewer tests is therefore not automatically less elapsed time. Parallelism changes elapsed time but also changes resource use; both need reporting.

LiFU's [individual explanation](../observed-subthemes/processor-and-rtl-verification.md#explanation-dac-2026-research2533) discusses selection, mutation, feedback, and execution overlap. A shared campaign can allocate effort more effectively, but an evaluation must separate the effect of coordination from extra methods, formal assistance, and additional compute.

## What each observation can support

| Observation | Supported statement | Additional evidence needed for a stronger claim |
| --- | --- | --- |
| A repeatable mismatch | The compared executions disagree under the recorded setup | Requirement-based diagnosis identifying the faulty component |
| More covered points | More of a defined observation set was reached | Matched definitions, meaningful behavior, and independently confirmed findings |
| No violation within a bound | The specified search found none within that scope | Coverage beyond the bound or an appropriate unbounded proof |
| A formal proof | The stated property holds in the stated model under its assumptions | Assumption validation and correspondence to the implemented system |
| Fewer reports to inspect | The investigation queue is smaller | Evidence about missed faults and the validity of removed reports |

## Long-term hypotheses that remain open

One hypothesis is that preserving useful information between verification stages can matter more than producing additional independent tests. Dependency-preserving mutation, intermediate observations, and feedback-directed allocation motivate it. A matched evaluation should remove each information path while keeping tools and resources fixed. The hypothesis weakens if apparent gains disappear after equalizing compute or checker strength.

A second hypothesis is that improved execution-environment fidelity can lower total investigation cost despite slower simulation. Test this using both simulator time and independently classified investigation effort. It weakens if modeling costs dominate or if the more restrictive environment hides meaningful failures.

A third hypothesis is that claims become more transferable when they report a resolved failure and its assumptions rather than only a coverage percentage. Test whether independent users can replay, diagnose, and classify the reported finding under the declared setup. A packet that omits necessary state, depends on unavailable components, or changes meaning under replay weakens the claim of transferability.

These are testable interpretations, not observed ISCA–DAC–ICCAD time trends. Comparable editions, target classes, budgets, source depth, and confirmation rules are still needed. Conference labels alone do not establish that tools are converging or that one venue's verification methods outperform another's.

The [processor and RTL chapter](../observed-subthemes/processor-and-rtl-verification.md) now contains three expanded manuscript-backed discussions. Other verification branches below still need deeper individual writing and source recovery. This parent synthesis does not resolve their evidence gaps, model-to-hardware correspondence, or independent scientific and comprehension review.
