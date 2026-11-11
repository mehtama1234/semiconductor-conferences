# Verification and validation

This article explains the subject and then connects it to 52 papers in the selected research sample.

A subtheme groups related technical problems. A mechanism describes the particular change proposed by a paper. The discussion below explains the subject; the linked paper records state the available evidence.

[Definitions used in the paper records](../reading-guide-v1.md)

## A design is correct only relative to a written requirement

A requirement can describe an output, a sequence of states, a timing limit, or information that must stay private.

- **Verification** checks whether the design meets those statements.
- **Validation** asks whether the statements and the design meet the intended use.

The two questions can need different experiments.

## Tests try some behaviors; proofs cover only what they assume

A circuit can have very many input combinations and internal states.

- **Simulation** tries selected runs and compares them with the expected result. A test that never reaches a faulty state cannot expose that fault.
- **Formal verification** reasons about a specified set of behaviors. Its conclusion depends on the model, the assumptions and the property proved.

A timeout is an unresolved check, not a pass.

## The subthemes run tests faster, prove properties, or choose better inputs

- **Simulation** methods run a model faster.
- **Emulation** builds a version of the design on other hardware to run tests.
- **Formal** methods search for violations or prove properties.
- **Test generation** picks inputs likely to expose errors.
- **Coverage** measures say which behaviors were exercised. They need a definition to mean anything.

## A fair test uses known faults and reports what was missed

1. Use known faults, or independently established reference behavior, to judge detection.
2. State design sizes, properties, test budget, unresolved checks, false alarms and missed faults.
3. When a generated test raises a score, check whether it finds new errors on designs outside the development set.

More tests help only if they improve the relevant coverage or detection.

## Follow a claim from requirement to evidence

A check can only be judged against conditions that say what the right answer is.

> **Example.** A storage unit accepts a write of value 7 to address A. A later read of A should return 7, but only if:
>
> - the write completed;
> - no later write changed A;
> - the read was allowed;
> - no failure outside the contract occurred.
>
> Without those conditions, comparing with 7 may call allowed behavior a defect, or accept behavior that should be rejected.

A verification method must make five things explicit:

1. what object is under test;
2. what behavior is required;
3. which inputs and starting states are allowed;
4. what execution is represented;
5. which observations decide the result.

These depend on each other. Better test generation does not fix a wrong expected result. A correct expected result cannot catch an error the observation leaves out.

**Be careful:** the examples below are independent teaching constructions. The linked paper explanations keep their manuscript locations, reported results and unresolved discrepancies. This discussion connects their mechanisms without claiming a reproduced combined system or exhaustive verification.

## The object being checked determines what a failure means

A failure means different things for a processor circuit and for firmware running on device models.

| What is checked | Compared against | What a mismatch means |
| --- | --- | --- |
| A processor implementation (a particular circuit) | A reference instruction model of allowed software-visible behavior | An architectural disagreement. Internal signals and clock-by-clock timing need not match. |
| Firmware talking to devices | Peripheral models that supply input bytes, status flags and interrupts | A software problem in that environment, not automatically a circuit defect |

Reaching more software branches in a device model is not processor-state coverage.

- [RISCSmith](../observed-subthemes/processor-and-rtl-verification.md#explanation-dac-2026-research150) and [LiFU](../observed-subthemes/processor-and-rtl-verification.md#explanation-dac-2026-research2533) test processors.
- The [SystemC embedded-fuzzing explanation](../observed-subthemes/processor-and-rtl-verification.md#explanation-dac-2026-research616) tests firmware against peripheral models.

**Be careful:** sharing a chapter lets us compare their testing mechanisms. It does not let us merge their bug counts or coverage denominators.

## A test needs both a path to the error and a way to observe it

A test finds an error only if it reaches it and looks at the right moment.

> **Worked example.** An arithmetic operation should write 5 to a register, but writes 6. The next instruction clears the register to zero.
>
> - Checking only the final value: 0 = 0, so the error is missed.
> - Checking right after the arithmetic: 6 ≠ 5, so the error is caught.
>
> More runs of a final-state-only checker need not reveal it.

The observation must also sit at the right boundary of meaning. A processor can do work internally and later throw it away. Treating every temporary internal write as a committed result causes false alarms. Watching only registers can miss a wrong memory write or exception.

RISCSmith's recovered method shows why two things belong together:

- building programs whose instruction dependencies make interactions reachable;
- logging intermediate effects before later instructions erase them.

Its [individual discussion](../observed-subthemes/processor-and-rtl-verification.md#explanation-dac-2026-research150) ties the construction and logging method to manuscript Section 3. It separates an observed disagreement from confirmed responsibility for a defect.

More observation can expose errors, but it also adds run time and more traces to analyze. So compare distinct, independently supported findings per complete campaign budget, not the number of logged events.

## A reference is a checker, not unquestionable truth

When two implementations disagree, that shows a difference, not which one is wrong.

**Differential testing** runs related inputs through two implementations and compares what they visibly do. A mismatch shows they differ under the comparison rule. The mistake may be in either one, or in:

- the reference;
- the event matching;
- the initial state;
- the supported features;
- the test generator.

Agreement is limited evidence too. Two implementations can share a wrong interpretation, or both omit the same behavior. A third helps only if its relevant assumptions and code are independent enough. Counting agreeing tools cannot replace checking the requirement.

A useful failure report records:

- input bytes and initial state;
- configurations and revisions;
- permitted behaviors;
- the first relevant difference;
- a replay procedure.

**Reduction** cuts unneeded input while keeping the same failure. A shorter program that raises an unrelated exception has not kept the finding.

> **Worked example (illustrative counts, not from the linked papers).** 100 failing inputs reduce to 3 distinct causes. Two are confirmed against the specification; one is disputed.
>
> The supported summary is **2 confirmed causes and 1 unresolved**, not 100 new bugs.

## Coverage measures exploration within a definition

A coverage percentage means little unless you know what was being counted.

- **Line coverage:** did selected source lines run?
- **Branch coverage:** were selected alternatives in the control flow taken?
- **State or transition coverage:** were defined states, or changes between them, reached?

Each needs a denominator: what was counted, which points were excluded, and which can actually be reached in the setup.

> **Worked example.**
>
> - 90 of 100 recorded points reached: **90%**.
> - 950 of a different 1,000-point set reached: **95%**.
>
> Neither number says which campaign checked more meaningful behavior, whether either found a fault, or whether their missed points include the same critical case.

A score becomes comparable only after its definition and target are matched. The manuscript-backed processor chapter shows this: RISCSmith's inspected coverage experiment measures the Spike reference model, while LiFU reports RTL-tool coverage with formal assistance. Their percentages cannot be ranked as measurements of one shared state space. The [cross-paper discussion](../observed-subthemes/processor-and-rtl-verification.md#what-connects-the-three-proposals) keeps that distinction.

Coverage can still guide testing. A newly reached branch may justify keeping an input that exposes behavior earlier tests missed.

**Be careful:** blaming the generator for every unreachable point wastes resources, and quietly removing hard points inflates the score. Exclusion rules need evidence and must stay visible.

## Formal proof is conditional on a model and assumptions

A proof covers exactly the property it states, inside the model it assumes, and nothing more.

A formal check reasons about every behavior in a stated model, under stated assumptions. If the model leaves out a relevant input or interaction, the proof does not cover that case.

> **Example.** Property: whenever a request is accepted, a response arrives within four cycles.
>
> - If the assumptions accidentally forbid every accepted request, the property "holds" without testing anything.
> - A separate reachability check (can acceptance ever happen?) exposes this.
> - It still does not show the remaining assumptions are realistic.

Three outcomes must be reported separately:

| Outcome | What it establishes |
| --- | --- |
| Bounded search finds no violation in ten cycles | Less than an unbounded proof; a failure at cycle eleven is outside the search |
| Unbounded proof | The stated property holds in the stated model, under its assumptions |
| Solver timeout | Nothing yet: an unresolved check |

A solver timeout establishes neither correctness nor a counterexample. So these outcomes must not be grouped under one success count.

Formal and simulation evidence can work together. Simulation exercises a concrete environment and gives a trace you can run. Formal reasoning can cover combinations within its model that random testing may miss. Their joint value depends on how their models, assumptions and properties relate, not on adding their coverage scores.

## The environment can create or conceal a failure

A wrong device model can invent failures, or hide real ones.

> **Example.** Firmware reads a ready flag, then receives bytes from a device queue.
>
> - A simulator that changes the flag independently of the queue may allow a state the real peripheral cannot produce. A crash from that state may blame the model, not the firmware.
> - A model that leaves out a real unusual event can cause the opposite problem: missed faults.

The SystemC study's [expanded explanation](../observed-subthemes/processor-and-rtl-verification.md#explanation-dac-2026-research616) separates functional peripheral behavior from cycle-accurate hardware timing. It also separates finding deliberately inserted bugs from discovering new bugs in unchanged software. Neither experiment should silently stand in for the other.

- A **false positive** is a report that matches no relevant real fault.
- A **false negative** is a fault the method misses.

Fewer crash reports do not prove both improved. Measuring either rate needs proper ground truth, including investigation beyond a favorable subset of outputs.

## Optimize the full investigation, not only test production

A campaign's cost runs from generating tests to explaining each failure, not just test count.

A campaign spends resources on:

1. generating inputs;
2. running them;
3. checking outputs;
4. reducing failures;
5. finding their causes.

Faster generation just fills a queue if running or investigating is the bottleneck. Remote model calls, parallel simulator workers and human review are costs even when a headline reports only test count.

> **Worked example (illustrative).**
>
> - 100 tests × 1 second = **100 seconds** of execution.
> - 60 tests × 2 seconds = **120 seconds**.
>
> Forty percent fewer tests is not automatically less elapsed time.

Parallelism changes elapsed time, and also resource use; report both.

LiFU's [individual explanation](../observed-subthemes/processor-and-rtl-verification.md#explanation-dac-2026-research2533) covers selection, mutation, feedback and overlapping execution. A shared campaign can spend effort better. But an evaluation must separate the effect of coordination from extra methods, formal assistance and extra compute.

## What each observation can support

Each observation supports one statement; a stronger claim needs more evidence.

| Observation | Supported statement | Additional evidence needed for a stronger claim |
| --- | --- | --- |
| A repeatable mismatch | The compared executions disagree under the recorded setup | Requirement-based diagnosis identifying the faulty component |
| More covered points | More of a defined observation set was reached | Matched definitions, meaningful behavior, and independently confirmed findings |
| No violation within a bound | The specified search found none within that scope | Coverage beyond the bound or an appropriate unbounded proof |
| A formal proof | The stated property holds in the stated model under its assumptions | Assumption validation and correspondence to the implemented system |
| Fewer reports to inspect | The investigation queue is smaller | Evidence about missed faults and the validity of removed reports |

## Long-term hypotheses that remain open

Three readings are worth testing; each names what would weaken it.

| Hypothesis | Test | What would weaken it |
| --- | --- | --- |
| Passing useful information between verification stages can matter more than producing more independent tests (motivated by dependency-preserving mutation, intermediate observations and feedback-directed allocation) | Remove each information path, keeping tools and resources fixed | Gains disappear once compute or checker strength is equalized |
| A more faithful execution environment can lower total investigation cost, despite slower simulation | Measure both simulator time and independently classified investigation effort | Modeling costs dominate, or the stricter environment hides meaningful failures |
| Claims transfer better when they report a resolved failure and its assumptions, not just a coverage percentage | Can independent users replay, diagnose and classify the finding under the declared setup? | The report omits needed state, depends on unavailable parts, or changes meaning on replay |

These are testable interpretations, not observed ISCA–DAC–ICCAD time trends. Comparable editions, target classes, budgets, source depth and confirmation rules are still needed.

**Be careful:** conference labels alone do not show that tools are converging, or that one venue's verification methods beat another's.

The [processor and RTL chapter](../observed-subthemes/processor-and-rtl-verification.md) now has three expanded manuscript-backed discussions. Other verification branches below still need deeper writing and source recovery. This synthesis does not resolve their evidence gaps, model-to-hardware correspondence, or independent scientific and comprehension review.

## Subthemes and how to study them

Each link opens the subtheme discussion and its captured paper records. Explanatory depth varies: some papers have expanded individual explanations; others still have only brief discussion or evidence cards. Source locations and unresolved conditions remain visible.

### [Simulation emulation and testing](../observed-subthemes/simulation-emulation-and-testing.md)

20 selected records in this theme. Start with [GPU-Fuzz: Finding Memory Errors in Deep Learning Frameworks](../observed-subthemes/simulation-emulation-and-testing.md).

### [Formal analysis and verification](../observed-subthemes/formal-analysis-and-verification.md)

10 selected records in this theme. Start with [Beyond Exact: Tight WCET Analysis of GPU Kernels with Branch Divergence](../observed-subthemes/formal-analysis-and-verification.md).

### [Formal and functional verification](../observed-subthemes/formal-and-functional-verification.md)

7 selected records in this theme. Start with [PRO-V-R1: Reasoning Enhanced Programming Agent for RTL Verification](../observed-subthemes/formal-and-functional-verification.md).

### [Formal and equivalence verification](../observed-subthemes/formal-and-equivalence-verification.md)

4 selected records in this theme. Start with [Miter-Aware LUT Mapping: Aligning Structure and Solvability for Efficient Logic Equivalence Checking](../observed-subthemes/formal-and-equivalence-verification.md).

### [Hardware security validation](../observed-subthemes/hardware-security-validation.md)

3 selected records in this theme. Start with [Automated Discovery, Classification, and Systematic Security Verification Methodology for Undocumented Instructions](../observed-subthemes/hardware-security-validation.md).

### [Processor and RTL verification](../observed-subthemes/processor-and-rtl-verification.md)

3 selected records in this theme. Start with [RISCSmith: Finding RISC-V CPU Bugs via Rich Instruction Construction and On-the-Fly Differential Analysis](../observed-subthemes/processor-and-rtl-verification.md).

### [Simulation and emulation](../observed-subthemes/simulation-and-emulation.md)

3 selected records in this theme. Start with [Activity-Aware Partitioning for Effective Multi-Threaded Event-Driven RTL Simulation](../observed-subthemes/simulation-and-emulation.md).

### [Emulation and prototyping](../observed-subthemes/emulation-and-prototyping.md)

1 selected records in this theme. Start with [A Boolean Processor-Based Hardware Emulation System with Reconfigurable Interconnects](../observed-subthemes/emulation-and-prototyping.md).

### [Physical verification](../observed-subthemes/physical-verification.md)

1 selected records in this theme. Start with [DRCGen: A Controllable DRC Violation Case Generator with Cross-PDK Transferability for Rule-Deck and Tool Validation](../observed-subthemes/physical-verification.md).

## Representative source-backed records

The following reading set spans the available conferences and uses dated corrections where registered. These corrections improve the current reading view but do not change historical adjudication or establish independent acceptance. Each paper link opens its exact evidence card.

## Paper cards: what changes and where it stops

- [DRCGen: A Controllable DRC Violation Case Generator with Cross-PDK Transferability for Rule-Deck and Tool Validation](../observed-subthemes/physical-verification.md#paper-dac-2026-research907) — DAC 2026.
- [Parallelizing Complementary Approximate Reachability](../observed-subthemes/formal-and-equivalence-verification.md#paper-dac-2026-research896) — DAC 2026.
- [RTL-Benchmt: Dynamic Maintenance of RTL Generation Benchmark Through Agent-Assisted Analysis and Revision](../observed-subthemes/simulation-and-emulation.md#paper-dac-2026-research874) — DAC 2026.
- [Provably Probabilistic Safe Controller Synthesis for Vision-Based Neural Network Control Systems](../observed-subthemes/formal-analysis-and-verification.md#paper-dac-2026-research720) — DAC 2026.
- [HLSDebugger: Identification and Correction of Logic Bugs in HLS Code with LLM Solutions](../observed-subthemes/simulation-emulation-and-testing.md#paper-iccad-2025-1027) — ICCAD 2025.
- [RIROS: A Parallel RTL Fault SImulation FRamework with TwO-Dimensional Parallelism and Unified Schedule](../observed-subthemes/simulation-emulation-and-testing.md#paper-iccad-2025-114) — ICCAD 2025.
- [Software-Style Hardware Debugging: A Hardware Generation, Simulation and Debugging Framework](../observed-subthemes/simulation-emulation-and-testing.md#paper-iccad-2025-1137) — ICCAD 2025.
- [Uncertainty-Guided Live Measurement Sequencing for Fast SAR ADC Linearity Testing](../observed-subthemes/simulation-emulation-and-testing.md#paper-iccad-2025-1117) — ICCAD 2025.
- [Stateful Embedded Fuzzing Using Peripheral-Accurate SystemC Virtual Prototypes](../observed-subthemes/processor-and-rtl-verification.md#paper-dac-2026-research616) — DAC 2026.
- [The Phantom of PCIe: Constraining Generative Artificial Intelligences for Practical Peripherals Trace Synthesizing](../observed-subthemes/simulation-and-emulation.md#paper-dac-2026-research514) — DAC 2026.
- [Activity-Aware Partitioning for Effective Multi-Threaded Event-Driven RTL Simulation](../observed-subthemes/simulation-and-emulation.md#paper-dac-2026-research440) — DAC 2026.
- [Lyra: A Hardware-Accelerated RISC-V Verification Framework with Generative Model-Based Processor Fuzzing](../observed-subthemes/simulation-emulation-and-testing.md#paper-dac-2026-research358) — DAC 2026.

## What the evidence supports

These records identify proposed methods and the conditions recorded for them. A reported improvement should be interpreted with its comparison method, input size, hardware, and result-quality requirement. Missing fields are evidence gaps; a populated field can also state that a detail is unspecified.

## Limits and next evidence

The selected sample is uneven across conferences and source types. It cannot establish how fast a subject is growing. Repeated observations across comparable years, with the same inclusion rules and source depth, are needed for a time trend.

Every linked evidence article preserves the Problem: and Mechanism / artifact: fields, baseline, unshortened limitations, source URL, and recorded location. Primary text and independent review remain necessary where the record says those checks are open.

[Research directions](../directions/README.md) · [All observed subthemes](../expanded-taxonomy-v1.md)
