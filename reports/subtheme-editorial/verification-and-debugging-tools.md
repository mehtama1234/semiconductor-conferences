## Organizing observations and changing code are different tasks

Debugging starts with evidence about a mismatch between intended and actual behavior. Tools can help organize that evidence or propose a change, but these are separate steps. A well-parsed log does not establish the cause of a failure. A patch that compiles does not establish that the intended behavior has been restored.

The two records in this subject cover log-schema extraction and language-model-assisted Rust repair. They are retained together as debugging tools, not presented as two implementations of the same method. The captured descriptions provide no quantitative evaluation for either.

## Schemacoder: recover structure from heterogeneous logs

[Schemacoder](../observed-subthemes/verification-and-debugging-tools.md#paper-dac-2026-research1841) automatically extracts log schemas using a method named residual Q-tree boosting. A schema identifies the structure of a record: which parts are fields, how they are represented, and which records share a format. This can make otherwise inconsistent messages searchable and comparable.

The difficult distinction is between variation in data and variation in meaning. Two messages may differ only in a timestamp or identifier and belong to one schema. Two superficially similar messages may describe different events and need different treatment. Merging them incorrectly can hide evidence; separating every minor textual variation can make the extracted structure unusable.

The source does not explain the Q-tree construction or residual update rule. Those mathematical details should not be inferred from the name. The available evidence supports the task and proposed model family, but not a claim about how it handles nested records, multiline messages, or streaming input.

Evaluation would need independently labeled schemas and explicit scoring of incorrect merges, incorrect splits, and field extraction. Testing later software versions matters because log formats change. It should also preserve the original messages so that a derived schema does not erase the evidence needed to audit a diagnosis. Accuracy, memory, latency, datasets, and robustness to format changes are all unspecified in the captured record.

<span id="explanation-dac-2026-research1841"></span>

### Schemacoder: schema extraction must preserve event meaning while compressing textual variation

#### What a log schema represents

A log record is a text or structured message emitted by a system. Some parts describe the event type and fixed wording; other parts are fields whose values change, such as timestamps, identifiers, addresses, counts or error details. A schema groups records that share the same structural meaning and identifies the fields and their representations.

The task is not simple text matching. A timestamp can vary while the record remains one event type. A number can instead be part of a message variant whose meaning changes. Two messages can have similar punctuation but represent different events, while one event can be printed in multiple formats across software versions. A useful extractor must distinguish variation in value from variation in structure and meaning.

#### What residual Q-tree boosting establishes—and does not establish

The captured description names residual Q-tree boosting as the extraction method. “Residual,” “Q-tree” and “boosting” identify a method label, but they do not specify the tree representation, feature construction, residual update, objective, stopping rule or handling of nested and multiline records. Those details determine whether the method merges equivalent records, splits distinct records and extracts fields correctly.

An incorrect merge hides meaningful differences by assigning different events to one schema. An incorrect split fragments one event into many schemas, increasing maintenance and reducing searchability. Field errors can also alter the evidence: a value classified as a fixed token may be discarded, or a fixed event marker classified as a variable field may make unrelated records appear similar. The raw log must remain available beside the derived schema.

#### What a complete evaluation needs

Create independently labeled logs with known schemas, field boundaries, nested records, multiline messages, malformed entries, missing fields and version changes. Compare residual Q-tree boosting with regular-expression extraction and generic tree boosting under the same data and compute budget. Report schema precision and recall, merge and split error, field-boundary accuracy, unknown-format detection, memory, latency, streaming behavior and maintenance cost after a software update.

Split by system, version and time rather than randomly splitting near-duplicate messages. Test whether the extractor preserves the raw record, explains its assignment and flags uncertainty. Then measure downstream value: can an investigator search and correlate events more accurately, and does a schema error change a diagnosis? The captured official description reports no schema accuracy, drift robustness, latency, memory or dataset result. The evidence supports automated log-structure extraction, not demonstrated cross-system diagnostic reliability.

## Akirarust: feedback guides a proposed repair

[Akirarust](../observed-subthemes/verification-and-debugging-tools.md#paper-dac-2026-research2871) uses a feedback-guided switch in a language-model-assisted Rust repair process. Its proposed control decision is how the repair process responds to compiler or test feedback. The source does not identify the language model, switching rule, repositories, or repair benchmark, so no particular reasoning strategy can be attributed to it beyond that description.

Compiler feedback checks properties enforced by the language and compilation process. Tests check the behaviors they actually exercise and assert; the [Rust book's testing chapter](https://doc.rust-lang.org/stable/book/ch11-01-writing-tests.html) describes tests as functions checking expected behavior. Neither compilation nor a finite test suite alone establishes that an arbitrary patch satisfies the full intended specification.

A repair might remove an error while accidentally changing valid behavior elsewhere. Evaluation therefore needs tests or review independent of the feedback used to generate the patch. It should distinguish compilation success, visible-test success, additional-test success, and independently assessed correctness. A single aggregated “repair rate” would hide those different evidentiary levels.

The complete cost includes failed candidates, model calls, compilation, test execution, and any human review. Repeated trials may also matter when generation is variable. The captured description supplies no patch-correctness, test-pass, runtime, or cost results, so it does not establish that adaptive feedback yields better repairs than a fixed process.

<span id="explanation-dac-2026-research2871"></span>

### Akirarust: feedback can steer repair search, but passing feedback is not the full specification

#### What the repair loop is doing

An automated Rust repair loop proposes a patch, compiles it and runs some tests. The compiler can report syntax, type, borrow, trait or build errors. Tests can report failures for the input cases and assertions they cover. The loop uses that feedback to decide what to do next, such as change its reasoning mode, generate another patch or stop.

The “thinking switch” is therefore a control policy for search. It does not itself define what a correct patch is. The source does not specify the language model, switch condition, modes, prompts, context retained between attempts, candidate limit or stopping rule. Those details determine whether the switch reduces wasted attempts or simply changes how the same incomplete search behaves.

#### What compiler and test feedback can prove

Compilation success establishes that the submitted code satisfies the compiler's checked rules for that build configuration. A visible-test pass establishes only that those tests passed. It does not prove behavior for untested inputs, error paths, concurrency, performance, security properties, public API compatibility or the intended behavior that was never encoded in a test.

A patch can fix the reported failure while changing valid behavior elsewhere. The evaluation must separate compiler success, visible-test success, additional hidden or held-out-test success, differential behavior against a reference and independent human or formal correctness assessment. The repair benchmark must prevent the model from seeing the target patch or tests in a way that makes the score incomparable; otherwise benchmark leakage can make the measured repair rate meaningless.

#### What a complete repair evaluation needs

Define repositories, bug classes, initial failures, compiler versions, test suites, time and model budgets, patch acceptance rule and baseline. Compare the feedback-guided switch with unguided LLM repair and traditional program repair under the same starting state. Report plausible patches, compile rate, visible-test pass, held-out-test pass, independently judged correctness, regression rate, attempts, model calls, compile/test time, total wall-clock time and cost.

Run repeat trials because generation can vary. Include bugs where compiler feedback is weak, tests are incomplete, failures are flaky and a patch can overfit the visible test. Preserve every candidate and feedback trace so that a result can be audited. The captured official description reports no patch correctness, test-pass rate, runtime, cost or repository result. The evidence supports feedback-guided repair as a search direction, not demonstrated better repair correctness or lower end-to-end repair cost.

## A useful connection without claiming an integration

Structured logs could help present failure evidence to a repair process, but these records do not demonstrate that combination. Incorrect schema extraction could also distort the very feedback used to choose a patch. A combined study would need to retain raw observations, trace the derived diagnosis to those observations, and independently validate the resulting code change.

The longer-term question is whether automation can reduce time from a reproducible failure to a validated repair without weakening the evidence at either end. That is a proposed research direction inferred from these tasks. Faster parsing or more passing patches would be intermediate results, not proof that the entire debugging process became more reliable.
