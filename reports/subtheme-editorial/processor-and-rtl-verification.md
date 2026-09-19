## What must a processor test actually establish?

A processor changes stored state as it executes instructions. Some of that state is visible to software: registers hold values used by instructions, memory holds data, and a program counter identifies where execution continues. The instruction set architecture, or ISA, specifies the allowed behavior. RISC-V is an ISA; two RISC-V processors can implement its rules using different internal circuits.

Register-transfer level, or RTL, is a description of hardware state and the logic that changes it. Simulating RTL lets a test observe the proposed circuit before fabrication. An ISA reference model instead computes instruction behavior without necessarily reproducing that circuit's timing or internal organization. Comparing the two asks whether the implementation produces an allowed software-visible result, not whether every internal signal matches.

A useful test needs a starting state, an input sequence, an execution environment, and a checker. An instruction that reads memory is not fully specified by its instruction bits: the address, permissions, and existing contents affect what should happen. An exception is an architecturally specified response to a condition such as an invalid instruction or disallowed access. Raising the right exception can be the correct result of a test; reaching the end without an exception is not inherently success.

Fuzzing automates the construction or modification of tests. A campaign may retain inputs that exercise previously unseen behavior and use them to construct later inputs. This feedback can improve exploration, but its value depends on what is observed. [LLVM's libFuzzer documentation](https://llvm.org/docs/LibFuzzer.html) describes a software coverage-feedback loop; processor verification needs its own account of hardware behavior and checking.

The three papers below change different parts of that process. RISCSmith changes instruction construction and comparison. Beyond Fuzzer Islands changes how several fuzzers share work. The SystemC paper changes the environment in which embedded software interacts with devices. A better input generator cannot compensate for a checker that ignores the relevant error; a more accurate environment cannot compensate for never supplying the input that reaches it.

All three paper discussions now have manuscript-backed explanations, worked reasoning, and explicit evidence limits. This is a writing pass, not independent acceptance of their results. Independent comprehension review remains open.

<span id="explanation-dac-2026-research150"></span>

## RISCSmith: make instruction interactions observable

### What the paper changes

[RISCSmith's author-hosted manuscript](https://yzhddding.github.io/assets/pdf/DAC26_RISCSmith.pdf#page=3), Section 3, describes instruction models derived from UnifiedDB metadata, constrained operands, prepared memory addresses, and deliberate state reuse. Verilator-based logging records register writes, memory writes, and exceptions. Reconstructed instruction contexts support differential comparison and test reduction. These are recovered method details, replacing the earlier claim that construction rules were unavailable.

The following worked examples are explanatory constructions, not reported RISCSmith test cases or measurements.

### Why a valid instruction is not yet a useful test

Consider a sequence that writes a value into a register, stores it to memory, and loads it back. If the store and load use unrelated addresses, the sequence may never test whether the stored value becomes visible to the later load. If their addresses are invalid, execution may stop before reaching the behavior of interest. If a later instruction replaces the loaded value before checking, a wrong result may disappear.

Three separate decisions therefore matter: which operations to generate, which state they share, and when to observe the result. These decisions cannot be reduced to generating more random instruction bits.

A register constraint can prevent a generator from selecting an operand that an instruction cannot encode. A memory-range constraint can keep an ordinary load inside a prepared region. Such constraints make a test executable under its intended setup; they do not establish that either the generator's interpretation or the hardware's result is correct. Tests deliberately targeting illegal accesses need a different expected outcome, not the same constraint applied indiscriminately.

State reuse makes dependencies more frequent. If instruction A writes a register and instruction B reads it, B's behavior depends on A. Using a small set of registers increases the chance of this interaction. The tradeoff is concentration: repeatedly exercising a narrow region can leave other register combinations and address boundaries unexplored. A policy useful for one class of errors is not automatically a complete testing strategy.

Structured instruction metadata also moves work into the metadata and its importer. A field saying that an operand has a certain width must be translated into the generator's representation correctly. Successful assembly establishes that the assembler accepts an encoding; it does not prove that the intended operation, privilege rules, or reference-model behavior agree. Versioned inputs and preserved conflict decisions are needed to investigate that boundary.

### Why comparing only the final state can miss an error

Suppose the initial values and execution conditions are identical, and the expected arithmetic result is 5. A faulty implementation produces 6. A later instruction clears the destination register:

| Observation point | Reference register value | Tested register value | What a comparison sees |
| --- | ---: | ---: | --- |
| Before the arithmetic instruction | 0 | 0 | Agreement |
| After the arithmetic instruction | 5 | 6 | A disagreement worth investigating |
| After clearing the register | 0 | 0 | Agreement again |

A final-register check misses this particular error. An intermediate check preserves the observation before it is overwritten. This is why the location of an observation matters independently of the number of generated tests.

Registers alone are insufficient. A wrong memory write could leave the checked registers unchanged. An incorrect exception could redirect execution before the expected register update occurs. The checker needs a stated set of observable events and rules for matching those events between implementations.

Matching should follow corresponding architectural operations, not equal simulator clock counts. One circuit may take longer to complete an instruction than another. Conversely, an internally executed operation that is later discarded must not automatically be treated as a committed software-visible update. A comparison that confuses these boundaries can report differences that the ISA permits.

The first observed disagreement is a useful debugging boundary, not necessarily the first internal error. An earlier hidden-state mistake may only become visible when a later instruction uses that state. The checker, its event logger, or the reference can also be wrong. Repeating a mismatch rules out some accidental failures but does not decide which component violated the specification.

### What reducing a failing program does—and does not—prove

The manuscript describes binary-search-based reduction and labels reliably reproduced reduced failures as confirmed bugs. That is the tool's criterion, not independently checked maintainer acceptance. Section 3.3 spans [PDF pages 3–4](https://yzhddding.github.io/assets/pdf/DAC26_RISCSmith.pdf#page=3).

Reduction asks whether parts of the input can be removed while preserving the same failure. Suppose A initializes a value, B performs unrelated arithmetic, and C uses the initialized value in the failing operation. Removing B may preserve the failure; removing A may erase it or produce a different exception. Merely obtaining a shorter program is insufficient if it no longer demonstrates the original disagreement.

“Shortest” also needs qualification. Finding an earliest failing prefix differs from finding the smallest arbitrary subset of instructions. With dependencies, deleting one instruction can require deleting or repairing another. A search strategy must state what changes it allows and what predicate it preserves. The inspected description is not a mathematical guarantee of globally minimal tests.

To make a reduced example useful to someone else, its record should retain the processor revision and configuration, initial memory and register state, supported extensions, reference version, input bytes, and observed mismatch. Different reduced programs can still have one underlying cause. Counting each as a separate bug would overstate the number of distinct findings.

### What the reported results establish

The [official DAC description](https://63dac.conference-program.com/presentation/?id=RESEARCH150&sess=sess152) reports six target cores, 18 newly found bugs, and branch-coverage gains of 37% and 61% against Cascade and RISCV-DV. The manuscript's [Tables 1–3, pages 4–5](https://yzhddding.github.io/assets/pdf/DAC26_RISCSmith.pdf#page=4), give baseline counts of 4 and 5 over 24 hours. Section 4.1 specifies an i9-10900, 32 GiB RAM, Ubuntu 20.04, and ten repetitions.

The denominators matter. Eighteen is 4.5 times four and 3.6 times five. Equivalently, the increases are 350% and 260%. Saying “3.5 times more” can refer to the first increase, but saying “3.5 times as many” would describe a different total. These ratios characterize this experiment, not all processor versions or every future testing budget.

Section 4.3 measures coverage in **the Spike reference model, not RTL state coverage**. [PDF pages 5–6](https://yzhddding.github.io/assets/pdf/DAC26_RISCSmith.pdf#page=5) therefore support a reference-code exploration result. Tables 4–5 label times in milliseconds while the surrounding prose says seconds; absolute timing remains unresolved. Table 4's values are 5732.49 and 3065.91, giving a 46.5% relative reduction either way.

A software branch measures a choice in that software's control flow. It does not enumerate every circuit state that can implement the same instruction. Even a hypothetical machine with only two independent 8-bit registers has 256 × 256 = 65,536 possible register-value pairs. Visiting both outcomes of one conditional operation would not establish that those pairs were tested, much less that hidden hardware states were covered.

The timing conflict matters differently from the ratio. A ratio of values carrying the same unit cancels that unit; an absolute planning estimate does not. Until the unit is resolved, using the reported number to budget seconds or milliseconds of analysis would introduce a thousandfold uncertainty. Bug-localization time also differs from how many new test instructions a campaign can execute per second.

### What remains to be checked

The manuscript's Section 3.2 describes a custom-extension input path, but [Section 5, page 6](https://yzhddding.github.io/assets/pdf/DAC26_RISCSmith.pdf#page=6), places private/custom-extension support in future work. Implemented scope is therefore unresolved. The linked artifact and individual issue dispositions were not verified in this pass; no result was reproduced.

The defensible conceptual conclusion is narrower than “automatic verification.” Improving test construction and observing intermediate architectural effects address two different reasons a campaign can miss errors. The remaining question is how much each contributes under a fixed budget, with a validated checker and independently confirmed findings. A larger instruction catalog, higher reference coverage, and a reduced mismatch each supply different evidence; none substitutes for the other two.

<span id="explanation-dac-2026-research2533"></span>

## LiFU: choose which test to modify, how to modify it, and what to try next

### Why combining fuzzers is a technical problem

A seed is an existing test from which a tool constructs another test. A mutator changes that seed: it might change instruction bits, replace an operation, or construct a new sequence while preserving selected dependencies. Different mutation rules explore different possibilities. A seed useful to one rule may become useless when another rule changes the part that made it interesting.

Consider a constructed example, not a LiFU measurement. A test writes register A and immediately uses A in the next instruction. This can exercise logic that supplies a newly computed value before it has reached the usual storage location. Changing the second instruction to read register B removes that dependency. Both programs can execute correctly, yet the modified program no longer exercises the original interaction. A validity check alone does not preserve the reason for keeping the seed.

Combining completed coverage reports also differs from cooperation during execution. Suppose fuzzer A reaches locations {1, 2, 3} and fuzzer B reaches {3, 4}. Merging the reports yields {1, 2, 3, 4}, not five locations. It changes our record of what was exercised. It does not construct a new test that uses a discovery from A to reach location 5 through B. That latter possibility requires exchanging useful inputs or feedback while there is still time to act on them.

LiFU's method uses scored seeds, several mutation styles, a reference-model pre-run, asynchronous RTL execution, analysis, and feedback. Its score combines coverage gain, mismatch severity, novelty, and efficiency. These details come from Sections 3.1–3.5 of the [accepted manuscript, PDF pages 4–6](https://eprints.whiterose.ac.uk/id/eprint/244137/1/2533_Camera_Ready_Paper.pdf#page=4). PDF page 1 is a repository cover sheet; the printed paper page numbers are one lower.

### How feedback can change the next test

The important quantity is not just how much a seed once covered, but what additional behavior it helps reach now. If a seed covers ten locations already reached by other tests, its immediate new-coverage contribution is zero. Another seed covering only three locations may be more useful if two are new. This marginal contribution changes as the campaign progresses.

The score also has to compare unlike quantities. A coverage fraction, a mismatch-severity score, and a cost per execution cycle have different numerical scales. Making coefficient weights add to one does not by itself make those quantities comparable. For example, a severity value of 100 multiplied by 0.25 contributes 25, while a coverage fraction of 0.1 with the same coefficient contributes 0.025. Normalization and chosen priorities can change which seed wins by orders of magnitude. This is a requirement for interpreting a scoring rule, not a reported LiFU failure.

Textual novelty is another imperfect guide. Renaming registers throughout a program can make instruction text look different while preserving its dependency pattern. Changing one branch condition can leave most text unchanged while changing execution substantially. A useful scheduler needs observed outcomes as well as a structural similarity measure; otherwise it may pay for differences that do not help verification.

The purpose of retaining some less-promising seeds is exploration. A seed that has produced no immediate coverage gain might be one modification away from a rare behavior. Allocating every future trial to the current highest scorer can prevent that discovery. Allocating everything randomly wastes accumulated information. The scheduling question is how to balance these costs under the available budget, not whether a single score constitutes a correctness guarantee.

### What language-model assistance contributes

LiFU routes dependency-rich seeds to language-model-guided mutation and uses low-level mutation for broader changes. It also generates candidate temporal properties. [Sections 3.1–3.4, PDF pages 4–6](https://eprints.whiterose.ac.uk/id/eprint/244137/1/2533_Camera_Ready_Paper.pdf#page=4) describe these roles; a generated candidate is not an established hardware requirement.

A temporal property describes behavior across successive steps. For example, “after an accepted request, a response eventually arrives” relates two events rather than testing a value at one instant. To make this precise, the author must define what counts as acceptance, whether reset cancels the request, and what assumptions apply to a receiver that refuses responses. Missing one condition can turn a reasonable sentence into a false assertion.

There is also a difference between asking whether a state sequence can occur and asserting that all executions obey a rule. A cover property seeks an execution reaching the described condition. Finding one such execution establishes reachability under the model's assumptions. An assertion expresses a rule that should hold for all executions in its stated scope. Demonstrating one successful example does not prove that universal statement.

Syntax checks establish that a property is well formed. Checks against recorded simulations establish consistency with those particular traces. Neither establishes that the proposed property matches the intended specification. Human review and formal results must therefore retain their assumptions and scope. Otherwise the campaign could optimize toward a plausible but incorrectly specified target.

### Why an early progress filter can save time—and exclude useful tests

Algorithm 1 uses a bounded instruction-set-simulator pre-run and repair attempts. Algorithm 2 distinguishes constant-driven points from empirically unlikely points; the accompanying footnote withholds unlikely points from feedback. [PDF page 5](https://eprints.whiterose.ac.uk/id/eprint/244137/1/2533_Camera_Ready_Paper.pdf#page=5).

An instruction-set simulator computes architectural behavior relatively directly, whereas RTL simulation follows the circuit description. Spending a small amount of work before expensive simulation can reject a test that merely repeats a useless loop. But repeating a program-counter value does not by itself mean that nothing useful is happening. A bounded loop can change a counter each iteration and terminate normally. A device-polling loop can make progress only when an external event arrives. The environment and the definition of progress matter.

The distinction between reference non-progress and RTL-only non-progress is especially important. A test that terminates in the reference but hangs in the RTL can expose an implementation error. It should not be discarded merely because the tested processor stops making progress. Retaining the original input, pre-run outcome, timeout, and any repairs allows a reviewer to check whether filtering accidentally removed the phenomenon being sought.

Similarly, observing a signal remain zero in many runs does not establish that it is permanently zero. If it is physically tied to zero in a fixed configuration, a proof about that driver can establish the opposite value is unreachable in that configuration. If zero is only an empirical observation, a rare input may still produce one. Withholding such a target from feedback is a search policy, not proof that the target is irrelevant.

Coverage reporting must keep that distinction visible. In an illustrative example, 80 covered points out of 100 is 80%. Removing ten uncovered points from the denominator produces 80/90 = 88.9%, without exercising anything new. A transparent report separates points newly reached, points formally excluded, and points merely deprioritized. Those changes answer different questions.

### What overlapping stages can—and cannot—save

The point of asynchronous stages is to prepare or analyze another test while a slow simulation is running. It does not make the simulation itself shorter.

For a worked timing example, assume three independent stages with separate resources: preparation takes 2 ms, execution takes 10 ms, and analysis takes 3 ms. Processing three tests serially takes 3 × 15 = 45 ms. With adequate buffers and no feedback dependency between these particular tests, completions can occur at 15, 25, and 35 ms. The first test still takes 15 ms, but later completions are spaced by the slowest stage's 10 ms service time.

If analysis rises to 12 ms per test, it becomes the limiting stage. Its queue grows unless scheduling slows input production or adds analysis capacity. If every next test must wait for the previous test's analysis, the assumed overlap is unavailable. Thus “coordination is hidden behind simulation” requires adequate slack, resources, and tolerable feedback delay; it cannot be inferred solely from drawing separate stages.

### Read the evaluation as several different comparisons

The [official DAC description](https://63dac.conference-program.com/presentation/?id=RESEARCH2533&sess=sess164) reports line / finite-state-machine / condition coverage of 93.4 / 43.6 / 95.7 for BOOM and 90.1 / 75.0 / 78.3 for Rocket, plus approximately 40% fewer tests. These are reported outcomes, not a universal resource-saving factor.

The manuscript's setup uses EPYC 7763, VCS, VC Formal, GPT-4-turbo, and Spike, with a 1.5-hour per-test limit. Figure 6 includes formal-assisted coverage. Figure 7 partly uses published comparison data. Table 4 lists six bugs, five marked new. See [Section 4, PDF pages 6–7](https://eprints.whiterose.ac.uk/id/eprint/244137/1/2533_Camera_Ready_Paper.pdf#page=6).

Line coverage concerns exercised source locations. Condition coverage concerns logical conditions. Finite-state-machine coverage depends on which states or transitions the tool extracts and counts. None measures the fraction of all possible hardware states that has been verified. Formal-assisted results also need to distinguish what simulation actually exercised from what a solver established under assumptions.

Test count is not elapsed time. Sixty tests costing two seconds each take 120 seconds, whereas 100 one-second tests take 100 seconds. A timeout is an upper bound on one test, not an average test cost or the total campaign budget. Equal elapsed budgets also need equal resource accounting: simulator workers, formal-engine work, remote model calls, and human analysis can all contribute. The inspected evaluation does not establish a complete, independently reproducible accounting for these costs.

Reusing published comparison curves introduces a separate comparability question. Processor revisions, enabled features, coverage exclusions, and counting conventions must match before curve differences can be attributed solely to the new method. A direct local baseline and a historical published baseline should not silently acquire the same evidence status.

Finally, a mismatch after reset requires a specified expectation. If a particular state element is required to initialize to zero, a nonzero value can violate that rule. If its initial value is unspecified, disagreeing with a reference that happens to choose zero is not sufficient evidence of a processor bug. This is a general checking requirement, not a determination about the listed LiFU issues. Their dispositions and exact specification obligations were not independently verified here.

### What this adds to the chapter's larger question

RISCSmith emphasizes constructing meaningful instructions and retaining intermediate observations. LiFU adds decisions about which observations should change resource allocation and future input construction. Its deeper contribution is a feedback-driven testing process, not just a merged total from several runs.

The open evaluation question is how much benefit comes from scheduling, additional generation methods, formal assistance, and filtering separately. A component-removal experiment would keep the other resources and definitions fixed, remove one component, and compare time to validated findings as well as coverage. Until those effects and bug confirmations are independently checked, the manuscript supports a promising combined method rather than a settled claim that coordination alone explains every gain. No LiFU implementation was executed in this pass.

<span id="explanation-dac-2026-research616"></span>

## SystemC embedded fuzzing: preserve the device behavior around the input

### Why a device read is not an isolated number

Firmware is software that controls a device. It often interacts with a peripheral through particular addresses: reading an address obtains status or data, while writing an address changes configuration or starts an operation. This is memory-mapped input/output, or MMIO. Although instructions access these addresses similarly to memory, their effects need not resemble ordinary storage. A read can consume queued data; a write can acknowledge an event.

The useful state is therefore larger than the last value returned. A serial receiver may have an enable bit, queued bytes, a status flag, and an interrupt request. An interrupt asks the processor to execute a handler for an event. A FIFO is a queue whose oldest entry is removed first. Correct relationships between these parts determine which paths the firmware can legitimately take.

Here is a simplified receiver example constructed for explanation, not a trace from the paper. Assume a one-byte queue, a level-sensitive interrupt enabled throughout, and a read that removes the byte:

| Event | Queue contents | Data-ready flag | Interrupt request |
| --- | --- | --- | --- |
| Receiver enabled, no input yet | Empty | 0 | 0 |
| External byte 42 arrives | 42 | 1 | 1 |
| Firmware reads the byte | Empty | 0 | 0 |

These values are related by the device's rules. Returning arbitrary independent values could report an interrupt with no received byte, or keep the queue permanently empty while firmware waits for data that the test supposedly delivered. A resulting hang might be caused by the test environment rather than the firmware.

Real peripherals have more complicated rules. Interrupts can be edge-triggered rather than level-sensitive, and clearing status can require a separate write. The example explains why a state model is needed; it is not a claim that all UARTs implement the table above.

### Where this method injects data

The paper connects AFL++ to SIM-A and VCML peripheral models. Injectors deliver inputs through peripheral interfaces; an MMIO probe starts injection at configured accesses. Peer-style communication uses periodic delivery; request/response communication supplies replies. See [version 1, Section 3, PDF page 3](https://arxiv.org/pdf/2604.19824v1#page=3).

The conceptual change is the injection boundary. Supplying a byte to a receiver model allows the model to update its queue and generate its interrupt. Directly replacing a firmware-visible status read skips those causal steps. The first approach asks what software does when an external participant sends data through the modeled interface. The second asks what software does when reads return selected values. Both can explore useful cases, but they do not make the same statement about physical reachability.

Triggering after configuration solves another problem. If the test delivers its entire input while the receiver is disabled, the model may correctly discard it. Firmware then waits indefinitely despite the fuzzer having generated many bytes. Waiting for a relevant enable or polling access can ensure that the intended communication starts.

That convenience also limits the tested schedules. A bug involving data arriving before initialization or during reconfiguration may require a different trigger policy. The test configuration must therefore be treated as part of the experiment: which event starts injection, which instance receives it, how bytes are grouped, and when subsequent items arrive. “Valid device behavior” and “all relevant input timings” are separate requirements.

Request/response traffic has a different causal order from unsolicited input. A sensor-interface model can wait for a read request and then supply bytes for that transaction. A serial peer can send a byte without first receiving a firmware read request. Applying one timing policy indiscriminately to both can create deadlocks or prevent the intended behavior from occurring.

### What “stateful” and “accurate” mean here

SIM-A is a proprietary functional simulator, not a cycle-accurate implementation; the paper uses a Cortex-M0 configuration. [Section 2.1, PDF page 2, and Section 4.1, page 4](https://arxiv.org/pdf/2604.19824v1#page=2) establish that boundary.

SystemC provides a way to describe components and simulated events in C++. Transaction-level modeling, or TLM, describes exchanges between components at the level of operations such as reads, writes, or message delivery. This can preserve an operation's logical consequences without reproducing every electrical transition or every processor pipeline cycle.

Stateful here means that device behavior depends on earlier events within an execution. It does not mean that unrelated fuzzing inputs should inherit leftover device state. To replay a failure, the test must preserve the initial state and the event sequence that produces it. If one test leaves a byte in a queue and the next test consumes it accidentally, the next test's result is no longer determined by its recorded input alone.

A functional model can correctly enforce “data arrives before data-ready becomes true” while still approximating arrival timing. That supports reasoning about the causal order; it does not establish response-time bounds on fabricated hardware. Conversely, a timing-accurate CPU model would not compensate for an incorrect peripheral state machine. Accuracy must be stated for the behavior relevant to the finding.

The model also defines what an external sender can express. Allowing arbitrary payload bytes is useful for testing validation, but it is not the same as modeling every legal or illegal wire-level frame. A failure should retain the injection interface and its constraints so that a reviewer can determine whether a real sender, a faulty peripheral, or only the simulator could cause it.

### Distinguish proving the test can detect a bug from discovering a new bug

The four targets are drone and robot firmware plus two Zephyr applications. The authors injected bugs for detection experiments, then removed those injected bugs for the tool comparison. They also adapted the bare-metal firmware to nrfx. [Section 4, PDF pages 4–5](https://arxiv.org/pdf/2604.19824v1#page=4).

An injected bug provides a known failure condition. Finding it demonstrates that the input path and checker can expose that condition in this setup. It does not demonstrate the rate at which the tool will find previously unknown bugs in an untouched codebase. The comparison with other tools must not quietly include planted defects on one side and only pre-existing defects on the other.

Likewise, “no fuzzing instrumentation required in firmware” does not imply that no porting or experimental changes occurred. Instrumentation adds observations for the testing tool. Porting changes how software connects to the available platform. Deliberately inserting a bug changes the tested behavior. These three changes serve different purposes and need separate records.

Consider a generic buffer example. A destination holds 16 bytes, while an external input asks the program to receive 20. Correct validation must reject the length or constrain the operation before writing beyond the destination. Whether an unchecked write immediately crashes depends on the surrounding memory and the simulator's checks. No crash does not prove that every access stayed inside the buffer; an out-of-bounds access can hit mapped memory and remain silent.

This illustrates the checker boundary. Crash, timeout, and coverage signals are observations, not a complete inventory of incorrect behavior. Silent data corruption may require additional assertions or a reference result. A timeout requires a documented progress expectation, because a program designed to wait for input is not necessarily faulty when no input arrives.

### What the comparison supports—and what it leaves open

Section 4.2 reports approximately 2× slower execution than Fuzzware, subset-only inspection of competing crashes, and unmeasured false negatives. P2IM failed before fuzzing two targets. The paper's broad false-positive claim must be read with these limits. [PDF pages 5–6](https://arxiv.org/pdf/2604.19824v1#page=5).

A false positive is a reported defect that does not correspond to the intended target's actual fault. A false negative is a real defect the testing process misses. Reducing the first does not establish that the second is also reduced. A restrictive input model can eliminate impossible traces while accidentally excluding a real but unusual sequence.

Crash counts are also not counts of distinct causes. Many inputs can lead to the same faulty assumption. Conversely, similar-looking hangs can arise from different causes. Manual classification needs a specified procedure, not just a smaller number in the final report. The subset that was inspected cannot establish that every uninspected competing crash was spurious.

There is a numerical discrepancy worth retaining. Table 3 gives target-C edges as 1250 versus 600 and target-D edges as 1800 versus 3100, while the following discussion states 60% and 40% coverage advantages respectively. [PDF pages 5–6](https://arxiv.org/pdf/2604.19824v1#page=5).

Using the table's counts, the target-C increase over 600 is (1250 − 600)/600 = 108.3%, not 60%. For target D, 3100 exceeds 1800 by 72.2%, not 40%; the reverse-direction reduction, from 3100 to 1800, is 41.9%. Different denominators or metrics could explain some of the prose, but they are not reconciled here. The writeup retains the actual counts rather than choosing a headline percentage.

More edges are not inherently better evidence if a model reaches them through impossible events. Yet calling extra edges impossible also requires validation of the model and traces. The relevant outcome is meaningful exploration of the target under stated assumptions, together with confirmed findings—not maximizing or minimizing one count in isolation.

A slower simulator can still reduce total engineering effort if it removes enough manual investigation. That tradeoff needs both quantities. In a constructed example, doubling a one-hour run adds one hour, while avoiding twenty ten-minute investigations saves three hours twenty minutes. The net saving is two hours twenty minutes. With only two such investigations avoided, the same slower run instead costs forty additional minutes. The paper's simulation-speed comparison alone does not establish this end-to-end balance.

### What to verify before using the results as hardware evidence

The useful next check is replay against independently validated device behavior: inspect the peripheral contract, record initial state and event timing, reproduce the firmware failure, and determine whether another model or the relevant hardware exhibits it. A model with the same mistaken assumption is not independent confirmation.

The strongest supported conceptual lesson is that a fuzzer's environment determines which failures its inputs can meaningfully demonstrate. Preserving queues, status transitions, and interrupt causes can eliminate some environment-induced failures, but shifts responsibility to model correctness and configuration coverage. The manuscript was inspected; its proprietary simulator was not executed here, and physical-hardware correspondence was not independently established.

## What connects the three proposals

The papers address test construction, campaign allocation, and execution-model fidelity. These are complementary needs, not evidence that the methods have been integrated. Their shared research question is how to maximize reproducible, genuinely new findings under a fixed verification budget. Answering it requires preserving seeds, tool versions, starting states, checker assumptions, reduced failing cases, and confirmation evidence. None of the three inspected manuscripts establishes exhaustive processor correctness or the absence of unobserved bugs.

The SystemC paper also changes what is under test. RISCSmith and LiFU compare processor implementations with a reference; the SystemC framework executes firmware against peripheral models and looks for software failures. Placing them in one verification chapter is useful for comparing testing mechanisms, but must not turn firmware edge counts into processor RTL coverage or software hangs into proven circuit defects.

RISCSmith and LiFU also show why “coverage improved” is not a sufficient cross-paper comparison. RISCSmith's inspected experiment observes Spike reference-code coverage. LiFU reports RTL-tool coverage with formal assistance and target-selection decisions. Different observations, denominators, and resources prevent ranking the methods by simply comparing their percentages. A common evaluation would need the same processor configuration, recorded coverage definitions, comparable budgets, and separately confirmed findings.

A hypothesis worth tracking across later editions is that verification gains increasingly depend on preserving useful information between steps: keeping instruction dependencies during mutation, retaining intermediate mismatches, and using prior observations to guide later tests. These two manuscripts motivate that hypothesis; they do not establish a historical trend. Testing it requires comparable earlier and later papers, plus experiments separating better information use from added compute or stronger auxiliary tools.
