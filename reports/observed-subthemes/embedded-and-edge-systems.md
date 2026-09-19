# Embedded and edge systems

This subject has 4 records in the selected sample. This page explains where it fits, then presents all captured paper evidence without shortening the measurements or limitations.

[Definitions used in the paper records](../reading-guide-v1.md)

## Understand the parent subject first

- [Systems applications and workloads](../themes/systems-applications-and-workloads.md)

## Useful results must survive limited memory, communication, and power

An embedded system performs computation as part of a larger device. An edge system performs work near the source or consumer of data. Neither term specifies one processor type or application. The four papers here address stream counting, debugging under power loss, satellite-image compression, and intermittent inference.

Their shared constraint is that a computation must remain useful when resources are limited. A stream summary must retain enough information to answer a query. A debug trace must survive the failure being investigated. A compressed representation must decode consistently. A partially completed inference must resume without mixing incompatible states.

Two historical descriptions below need explicit correction. CelestialEye concerns item frequencies in data streams, not measuring an electrical signal's oscillation frequency. WINNER uses “in-vivo” for regular execution and “ex-vivo” for debug sessions; the available source does not describe a biomedical implant. These distinctions change the relevant experiments, not just the wording.

## CelestialEye: count repeated items without storing the entire stream

An item's frequency is its number of occurrences within the stream or observation window. Exact counting can require a counter for every distinct item. If many different items arrive quickly, memory capacity, memory-access rate, and counter-update conflicts become important limits.

[CelestialEye](../observed-subthemes/embedded-and-edge-systems.md#paper-dac-2026-research1587) combines FPGA stream processing with CPU heuristic decoding. Its official description identifies hot/cold item separation, compression, encoding, and FPGA-generated frequency bounds that assist decoding. It claims better performance and accuracy than BitMatcher but supplies no numerical throughput, count-error results, memory budget, or evaluation distributions. The relevant accuracy is frequency-estimation accuracy, not clock calibration. [Official DAC description](https://63dac.conference-program.com/presentation/?id=RESEARCH1587&sess=sess175).

A frequently occurring item can justify different treatment from one seen rarely. A compact summary saves space by storing less than the full stream, but decoding must distinguish information actually retained from information estimated. Bounds can constrain a reconstruction only if their assumptions hold; a heuristic search among possible counts is not automatically an exact-count guarantee.

The CPU–FPGA split creates a system-level question: can decoding keep up with the rate at which summaries require processing? An FPGA may accept items quickly while CPU work accumulates. Measure ingestion, transfer, query completion, and loss or backpressure separately. Changing item popularity and bursts are useful stress cases because average traffic can conceal temporary overload. These are evaluation requirements, not unreported CelestialEye results.

<span id="explanation-dac-2026-research1587"></span>

### CelestialEye: a stream-frequency engine is a bounded summary-and-decoding system

#### What “frequency” means here

For a stream of items, an item's frequency is the number of times that item appears in a defined observation window. The item could be a key, event type, packet field or other identifier. This is different from the oscillation rate of an electrical signal. The system must state the item domain, window boundary, whether counts reset, and whether the required answer is exact or estimated.

Exact counting can require storage for many distinct items. At high input rates, the system must accept items, update state, retain enough information for later queries and avoid dropping or reordering data. A summary reduces storage by retaining compressed information rather than a complete counter for every item. That saves resources only if the retained summary still supports the required query with a known error rule.

#### What the FPGA and CPU each do

An FPGA can process items in a pipeline with predictable per-item work. It may classify hot and cold items, encode a compact summary and produce bounds or partial counts. A CPU can run a more flexible search or heuristic decoder over that summary. The split creates two rates: the rate at which the FPGA produces summaries and the rate at which the CPU can decode and answer queries. If production is faster than decoding, queues grow, summaries are delayed, or backpressure and loss occur.

The FPGA-generated bounds are useful only if they are valid for the information the hardware retained. A bound narrows possible counts; it does not prove the exact count unless the remaining possibilities collapse to one under stated assumptions. A heuristic that selects the most plausible count may be accurate on a distribution while still failing on an adversarial or unseen distribution.

#### What a complete result must establish

Define the stream distribution, item cardinality, hot/cold threshold, window, burst pattern, summary size, encoding, counter width, overflow behavior and decoder search budget. Compare with CPU-only counting and a fixed FPGA counter under the same input rate, memory, clock, interface and output requirement. Measure throughput, count error, exact-recovery rate, query latency, FPGA resources, CPU time, memory, power, transfer cost, dropped items and backpressure.

Test uniform streams, skewed streams, changing popularity, bursts, unseen items, high-cardinality inputs, counter overflow and windows that cross transfers. Report whether accuracy is per item, per query or aggregate, and whether reported throughput includes CPU decoding and data movement. The captured official description claims improved performance and accuracy over BitMatcher but gives no numerical throughput, count-error distribution, memory budget or input distributions. The evidence supports a CPU–FPGA summary-and-decoding architecture, not a proven exact frequency instrument or universal throughput improvement.

## WINNER: observe power-loss behavior without removing that behavior

An intermittent device loses power and later resumes from state that survived. Registers and ordinary working memory may not survive, while nonvolatile memory retains saved information. A failure can leave some effects persistent and other progress lost, making a restarted task behave differently from uninterrupted execution.

[WINNER](../observed-subthemes/embedded-and-edge-systems.md#paper-dac-2026-research2997) records execution traces in nonvolatile memory during normal operation and exposes them in debug sessions triggered by user-defined property violations. It uses software-controlled electromagnetic emissions for low-rate communication. Across six applications and five platforms, the description reports less than 1% runtime increase, 6% average binary-size growth, and up to fourfold lower transmission energy than Bluetooth Low Energy. Exact hardware, receiver conditions, bug coverage, and trace-completeness guarantees are missing. The description states that the tool is open source; no artifact execution was performed here. [Official DAC description](https://63dac.conference-program.com/presentation/?id=RESEARCH2997&sess=sess158).

Attaching a debugger can change power supply, timing, or execution. Logging also consumes energy and storage. A useful analyzer must therefore quantify how observation changes the workload and whether the recorded sequence remains interpretable after interruption. A partially written trace record must not silently appear to be a complete observation.

A property violation is a condition chosen to trigger investigation, such as an excessive number of repeated task executions. It detects behavior covered by that condition, not every possible bug. Debugging evidence should connect the triggering property to the recorded state and clearly mark missing intervals. A low runtime overhead does not by itself prove negligible energy impact or complete visibility.

<span id="explanation-dac-2026-research2997"></span>

### WINNER: intermittent debugging is a trace-integrity problem as well as a telemetry problem

#### What an intermittent execution trace must preserve

An intermittent device can lose power during an instruction sequence, memory update or trace write. Volatile registers and working memory may disappear, while a nonvolatile record survives. A useful trace must therefore identify the execution interval, record ordering, write completion and reset boundary. It must distinguish a complete record from a record interrupted halfway through a power failure.

WINNER records execution during ordinary operation and exposes the trace during a debug session triggered by a user-defined property violation. The source uses “in-vivo” and “ex-vivo” as names for execution and debug contexts; those words do not, in the captured evidence, establish a biomedical implant or medical deployment. The important engineering question is whether recording and later transmission reveal enough state to diagnose the selected property without changing the failure behavior.

#### Why observation can change the failure being studied

Writing each event consumes time, memory writes and energy. More work can change when the next power loss occurs. A software-controlled electromagnetic transmission also consumes energy and may compete with computation or interfere with other activity. If tracing makes the device survive longer, fail earlier or reach a different schedule, the trace may describe the instrumented program rather than the original failure.

The trigger has a defined scope. A property such as repeated task execution can identify one class of abnormal behavior, but it cannot prove that other bugs are absent. The trace should connect the violation to the preceding state, preserve enough context to reproduce it and mark gaps caused by overflow, reset, torn writes or failed transmission.

#### What a complete evaluation must measure

Compare tracing and transmission with offline collection and local monitoring on the same applications, platforms, energy traces and trigger conditions. Report runtime, binary size, storage writes, trace completeness, event loss, trigger latency, radio or EM energy, communication rate, receiver conditions, recovery after power loss and diagnosis accuracy. Test power failures during every trace-record stage, full storage, repeated resets, bursts, clock variation, changing harvested energy and false or missed property triggers.

If the description reports less than 1% runtime increase, 6% average binary-size growth and up to fourfold lower transmission energy than Bluetooth Low Energy, those figures still need their denominators, hardware, receiver, application set and accounting boundary. Low runtime overhead does not prove low total energy, complete visibility or safe deployment. The captured description reports no such full conditions, biomedical validation or artifact execution here.

## SemCom: consistent decoding and faithful imagery are different requirements

Image compression replaces a large image representation with fewer bits. A codebook associates compact codes with stored representations. An entropy coder further reduces bit use by assigning representations according to symbol probabilities. The encoder and decoder must agree on the coding rules to reconstruct the encoded symbols.

[SemCom](../observed-subthemes/embedded-and-edge-systems.md#paper-dac-2026-research791) partitions a codebook by semantic region and uses region-aware bit allocation. It estimates entropy-coding probabilities offline to avoid platform-dependent probability calculations between satellite and ground hardware. The official description claims bit-exact decoding and favorable results on real satellite payloads, but gives no bitrate, reconstruction metric, processor identity, or flight-test conditions. “Payload” does not by itself establish an in-orbit experiment. [Official DAC description](https://63dac.conference-program.com/presentation/?id=RESEARCH791&sess=sess145).

Bit-exact decoding means recovering the intended encoded symbols under the specified coding process. It does not necessarily mean reconstructing the original pixels without loss. An image can be quantized before entropy coding; exact recovery of those quantized symbols still leaves the earlier approximation unchanged.

Likewise, semantic regions are classes or structures used to organize representation, not a guarantee that all important content is preserved. A compression strategy adapted to common regions needs separate tests on small objects, unusual events, and class boundaries. Downstream task quality and pixel reconstruction quality can differ. The full transmitted size should include any region labels, codebook identifiers, and side information needed by the receiver.

<span id="explanation-dac-2026-research791"></span>

### SemCom: semantic compression chooses what survives a bitrate limit

#### What compression changes

An image contains more samples than a constrained satellite link can transmit. Compression converts the image into a smaller representation and the decoder reconstructs an image or an intermediate representation. At a very low bitrate, the system cannot preserve every pixel equally. It must decide which visual information receives bits and which information is approximated or discarded.

Semantic compression uses regions, object classes or task-relevant structures to make that decision. A codebook stores representative patterns, and an entropy coder assigns shorter codes to more probable symbols. Region labels, codebook identifiers, probability tables and other side information also consume bits. A claim about bitrate must count the complete transmitted representation, not only the compressed image symbols.

#### What bit-exact decoding means

The encoder and decoder may use fixed, offline probability tables so that both sides interpret a code stream identically. Bit-exact decoding means the decoder reproduces the intended encoded symbols under the specified arithmetic and tables. It does not mean that the original uncompressed pixels are recovered exactly. If quantization or semantic simplification happened before entropy coding, exact decoding reproduces the already approximated representation.

The quality question is therefore separate from decoder agreement. Pixel metrics such as distortion or structural similarity may disagree with object-detection, classification, change-detection or geolocation quality. A semantic priority can improve one downstream task while removing an unusual object, small target, boundary or event that was not represented in the training distribution.

#### What an end-to-end satellite evaluation needs

Specify sensor data, image resolution, bitrates, codebook and region overhead, onboard processor, memory, power, radiation assumptions, decoder version and link errors. Compare JPEG-like and task-agnostic learned compression at the same total bitrate and hardware budget. Report reconstruction quality, task accuracy or recall, rare-event performance, encode/decode latency, memory, energy, failure behavior and any adaptation or retraining cost.

Test ordinary scenes, small objects, unexpected content, class boundaries, seasonal and sensor changes, corrupted packets and images outside the training set. Separate ground simulation, hardware-in-the-loop and flight evidence. The captured official description claims bit-exact decoding and favorable results on real satellite payloads but reports no bitrate, reconstruction metric, processor, task metric, energy, latency or flight condition. The evidence supports a semantic, region-aware compression direction, not demonstrated ultra-low-bitrate superiority or in-orbit performance.

## EnergyHDC: preserve enough progress to finish after power returns

Hyperdimensional computing represents information using vectors with many components and compares or combines those vectors for tasks such as classification. The representation can offer tolerance to some approximation, but inference correctness under power loss is a separate issue from statistical classification quality.

[EnergyHDC](../observed-subthemes/embedded-and-edge-systems.md#paper-dac-2026-research962) combines energy-dependent checkpoint granularity, dimension-first execution, and compile-time priority pruning. On an MSP432P401R microcontroller under intermittent power, the official description reports up to 214× speedup over Mementos and 19.6× faster inference than DynBal at similar accuracy. It does not provide the datasets, exact accuracy differences, outage traces, storage sizes, or elapsed-time accounting. These are separate comparisons, not two factors to multiply. [Official DAC description](https://63dac.conference-program.com/presentation/?id=RESEARCH962&sess=sess158).

A checkpoint saves enough state to continue later. Saving too frequently consumes energy on preservation rather than new work; saving too rarely risks repeating a large amount of work after interruption. Reordering computation can change how much unfinished intermediate state must be saved, without necessarily changing the desired mathematical result.

Pruning deliberately omits selected work and can change the answer. It therefore needs its own accuracy comparison, separate from the question of whether resumed execution matches the selected pruned algorithm. A system that reliably resumes an inaccurate model has solved one problem, not both.

Average harvested power is insufficient to characterize completion. Two energy traces can provide equal total energy but different uninterrupted intervals. If each interval ends before a necessary unit of work and its preservation can finish, usable progress may remain small. Report wall-clock completion, active execution time, restart work, and successful outputs under the same energy trace.

<span id="explanation-dac-2026-research962"></span>

### EnergyHDC: intermittent inference has two correctness questions—resume the computation and preserve its answer

#### What the computation is doing

Hyperdimensional computing represents an input or class with a vector containing many components. Operations combine or compare those components, and the final similarity or score selects a class. The representation may tolerate some approximate or missing work, but that tolerance must be measured for the task; it is not a guarantee that any skipped component is harmless.

An energy-harvesting device may lose power before an inference finishes. The system must save enough intermediate state to resume without confusing a new inference with an old one. That state can include the current input, vector components, loop position, partial sums, class scores, configuration and a valid checkpoint marker. A checkpoint that is internally consistent but omits needed state can produce a plausible yet wrong answer.

#### Why checkpoint granularity and execution order matter

Frequent checkpoints reduce repeated work after an outage but consume energy, memory writes and time. Infrequent checkpoints reduce preservation cost but may force the device to repeat a large interval. The best interval depends on the energy trace, capacitor capacity, write cost, computation rate and probability of interruption.

The dimension-first execution strategy changes the order in which vector components are processed so that a useful portion can be completed or preserved within an available energy interval. Compile-time priority pruning removes selected work to reduce cost. These are different mechanisms: reordering can preserve the selected algorithm's result, while pruning may change the algorithm and its accuracy. The comparison must not treat a speedup from pruning as only a checkpointing gain.

#### What “faster inference” must mean

Accuracy compares answers with a reference model. Resumption compares whether the interrupted computation produces the same answer as an uninterrupted execution of that selected model. Completion measures whether useful outputs arrive under a real sequence of energy outages. A system can have unchanged accuracy when power is continuous but fail to complete under short outages, or complete reliably while pruning reduces accuracy.

Evaluate under identical datasets, model, memory, capacitor, harvested-energy trace and output requirement. Report accuracy, energy per inference, checkpoint count and size, write cost, restart work, wall-clock time to a valid output, active compute time, outage tolerance, latency distribution, memory, storage endurance and failure rate. Test traces with equal average energy but different burst lengths, long gaps, noisy harvest, changing input and outages during checkpoint writes.

The captured official description reports up to 214× speedup over Mementos and 19.6× faster inference than DynBal at similar accuracy on an MSP432P401R under intermittent power. It does not provide datasets, exact accuracy differences, outage traces, storage sizes or elapsed-time accounting. These figures support a claimed intermittent-inference direction, not a verified end-to-end completion or accuracy result across harvest conditions.

## Compare retained information and completed work

All four cases reduce or reorganize information: stream summaries, failure-surviving traces, compressed image symbols, or inference state. The important question is what information remains sufficient for the required output. Less storage or traffic is beneficial only if the corresponding reconstruction, diagnosis, decoding, or classification requirement still holds.

This is a mechanism-level connection across the selected papers, not proof of a multi-year trend. Strong comparisons need both resource measurements and an explicit output-quality rule. Full manuscripts were not recovered in this pass; the author publication listings and refreshed official descriptions do not supply missing page-backed experiments. The corrections above supersede the historical cards' biomedical and signal-frequency assumptions. Source-record reconciliation and independent reproduction remain open.

## Compare the results carefully

First identify the inputs and required output quality. Then identify the limited resource: time, memory, communication, energy, circuit area, or correctness coverage. Ask which part of the method reduces that cost and which new cost it adds. Compare numbers only when the experiments hold these conditions sufficiently similar.

A conference description may explain the proposal while omitting the full experiment. An author preprint link may have been coded from its abstract. The source classification does not by itself establish that every table was read. Missing locations remain visible below.

## Complete captured evidence

These are evidence records, not substitutes for the explanations above. Each record preserves its problem, proposed method, measurements, comparison conditions, and source limits. A populated record does not establish that its mechanism has been fully explained or independently verified.

<span id="paper-dac-2026-research1587"></span>

### Celestialeye: A Synergistic CPU-FPGA Engine for Accurate Frequency Measurement in High-Speed Data Streams

DAC 2026 · Record: `dac-2026-research1587`

[Read the step-by-step explanation](#explanation-dac-2026-research1587)

**Updated source-backed reading card**

Reviewed 2026-09-08. Deepens the existing CelestialEye treatment into a paper-level reading and corrects the historical frequency interpretation; defines item-frequency summaries, CPU–FPGA rate matching and bounded decoding, and makes stream distributions, count error and end-to-end throughput explicit.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

High-speed item-frequency measurement needs precise counting or estimation while sustaining stream throughput.

**Mechanism / artifact:**

Synergistic CPU–FPGA engine for item-frequency summaries and heuristic decoding; hot/cold policy, summary encoding, FPGA bounds, decoder objective and overflow behavior are incompletely specified. This is item frequency, not electrical signal-frequency measurement.

**Workload — the work tested:**

High-speed item streams; item domain, cardinality, input rate, popularity distribution, observation window, bursts, unseen items and query protocol are unspecified.

**Hardware and manufacturing assumptions:**

CPU–FPGA system with streaming I/O; FPGA pipeline, memory, interface, clock, summary size, transfer path, CPU decoder and power conditions are unspecified.

**Baseline — the comparison method:**

CPU-only item-frequency measurement

Fixed FPGA counter

BitMatcher is named in the chapter description

Input distribution, rate, memory, clock, interface and end-to-end accounting are unspecified

**Reported measurements:**

Measurement accuracy and throughput are claimed qualitatively; no count-error distribution, exact-recovery rate, maximum sustainable rate, query latency, resource, memory, power, transfer, loss or backpressure result is reported.

**Limits on the conclusion:**

Frequency means the number of occurrences of an item in a defined stream window, not an electrical oscillation frequency. The item domain, window, reset rule and exact-versus-estimated output must be defined before accuracy can be interpreted.

A compact summary and FPGA-generated bounds retain less information than full counters. A bound narrows possible counts but does not prove an exact count unless the remaining possibilities collapse under stated assumptions; heuristic decoding can work on one distribution and fail on another. CPU decoding can also lag FPGA ingestion and create queueing, backpressure or loss.

The official description claims improved performance and accuracy over BitMatcher but reports no numerical throughput, count-error distribution, memory budget or input distribution. The record supports a CPU–FPGA summary-and-decoding architecture, not a proven exact frequency instrument or universal throughput improvement.

**Source and location**

Evidence tier: Primary captured official DAC description plus existing chapter level celestialeye correction; no full paper extraction, stream distribution reconstruction or independent throughput/error validation. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH1587)

DAC 2026 official description; captured Problem, Mechanism / artifact, Workload, Hardware, Baseline, Measurements and Limits fields; record RESEARCH1587; no manuscript pages.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** CPU-only frequency measurement

fixed FPGA counter

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH1587

**Hardware or process assumptions:** CPU-FPGA system with streaming I/O; clock and interface assumptions are unspecified.

**Limits:** No frequency error, maximum rate, latency, resource, or power results are reported.

Clock and signal assumptions determine accuracy.

Official description only; instrumented stream validation is required.

**Method or artifact:** Synergistic CPU-FPGA frequency-measurement engine.

**Metrics:** Measurement accuracy and throughput are claimed qualitatively

**Problem:** High-speed frequency measurement needs precise timing while sustaining stream throughput.

**Workload or benchmark:** High-speed data streams; input rate, signal classes, and measurement windows are unspecified.

</details>

<span id="paper-dac-2026-research2997"></span>

### WINNER: A Wireless In-Vivo/ex-Vivo Runtime Analyzer for Intermittent Computing

DAC 2026 · Record: `dac-2026-research2997`

[Read the step-by-step explanation](#explanation-dac-2026-research2997)

**Updated source-backed reading card**

Reviewed 2026-09-08. Deepens the existing WINNER treatment into a paper-level reading and corrects the biomedical implication; defines intermittent trace persistence, trigger scope, observation disturbance and trace completeness, and makes telemetry energy and receiver conditions explicit.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Intermittent embedded execution needs runtime visibility despite power loss and constrained communication.

**Mechanism / artifact:**

Runtime analyzer that records execution traces in nonvolatile memory during normal execution and exposes them in debug sessions triggered by user-defined property violations; trace format, atomicity, trigger coverage and software-controlled EM communication are incompletely specified. The captured use of “in-vivo/ex-vivo” does not establish a biomedical implant.

**Workload — the work tested:**

Intermittent embedded applications; six applications and five platforms are named in the captured description, but exact applications, energy traces, trigger properties, trace volume, power-failure points and diagnosis tasks are unspecified.

**Hardware and manufacturing assumptions:**

Low-power intermittent embedded device with nonvolatile storage and software-controlled electromagnetic telemetry; hardware, energy source, receiver, storage endurance, bandwidth, safety and interference assumptions are unspecified.

**Baseline — the comparison method:**

Offline trace collection

Local runtime monitoring

Bluetooth Low Energy is named for transmission-energy comparison

Receiver, application, energy, trace-completeness and accounting conditions are unspecified

**Reported measurements:**

The captured description reports less than 1% runtime increase, 6% average binary-size growth and up to fourfold lower transmission energy than Bluetooth Low Energy; it reports no trace completeness, event loss, telemetry latency, total energy, receiver reliability, privacy or biomedical validation.

**Limits on the conclusion:**

Intermittent power can interrupt an instruction, memory update or trace write. A valid trace must preserve ordering, write completion, reset boundaries and missing intervals; a partially written record must not be interpreted as complete evidence.

Tracing and electromagnetic transmission consume time, writes and energy and can change the power-loss schedule. A property trigger covers only the behavior it defines; low runtime overhead does not establish low total energy, complete bug visibility or diagnosis correctness.

The captured description uses in-vivo/ex-vivo terminology but does not establish a biomedical implant. It reports no full telemetry conditions, receiver reliability, trace completeness, power-failure coverage, privacy, safety or artifact execution result. The record supports intermittent-debugging instrumentation, not validated biomedical deployment or complete runtime observability.

**Source and location**

Evidence tier: Primary captured official DAC description plus existing chapter level winner correction; no full paper extraction, artifact execution or deployment/safety validation. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH2997)

DAC 2026 official description; captured Problem, Mechanism / artifact, Workload, Hardware, Baseline, Measurements and Limits fields; record RESEARCH2997; no manuscript pages.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** offline trace collection

local runtime monitoring

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH2997

**Hardware or process assumptions:** Low-power intermittent embedded device with wireless telemetry; safety and bandwidth assumptions are unspecified.

**Limits:** No telemetry energy, latency, reliability, privacy, or biomedical validation results are reported.

Wireless operation may disturb intermittent execution.

Official description only; deployment and safety validation is required.

**Method or artifact:** Wireless in-vivo/ex-vivo runtime analysis system.

**Metrics:** Runtime observability is claimed qualitatively

**Problem:** Intermittent biomedical systems need runtime visibility despite power loss and wireless constraints.

**Workload or benchmark:** Intermittent biomedical applications; implant, radio, energy source, and traces are unspecified.

</details>

<span id="paper-dac-2026-research791"></span>

### Semcom: Semantic-Enhanced On-Board Satellite Image Compression at Ultra-Low Bitrates

DAC 2026 · Record: `dac-2026-research791`

[Read the step-by-step explanation](#explanation-dac-2026-research791)

**Updated source-backed reading card**

Reviewed 2026-09-08. Deepens the existing SemCom treatment into a paper-level reading; separates bit-exact symbol decoding from image and task fidelity, defines region/side-information bitrate accounting, and makes rare-content, hardware, packet and flight-validation requirements explicit.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Satellite links constrain image bandwidth while downstream tasks may need semantic content more than pixel fidelity.

**Mechanism / artifact:**

Semantic-enhanced on-board image compression; region definition, codebook, bit allocation, side information, entropy tables and task objective are incompletely specified.

**Workload — the work tested:**

Satellite imagery; sensor, resolution, scene distribution, bitrates, downstream tasks, rare content, packet errors and training/test split are unspecified.

**Hardware and manufacturing assumptions:**

Spaceborne low-power compute and communications; processor, memory, energy, radiation, link, decoder and flight conditions are unspecified.

**Baseline — the comparison method:**

JPEG-like compression

Task-agnostic learned compression

Bitrate accounting, hardware budget, task set, scene split and comparison conditions are unspecified

**Reported measurements:**

Ultra-low-bitrate efficiency is claimed qualitatively; no total bitrate, reconstruction quality, task accuracy/recall, latency, memory, energy, packet-failure or flight result is reported.

**Limits on the conclusion:**

Semantic compression allocates limited bits among regions or task-relevant structures. Region labels, codebook identifiers, probability tables and other side information also consume bits. A bitrate must include the complete representation, not only image symbols.

Bit-exact decoding means reproducing the intended encoded symbols under shared coding rules; it does not restore original pixels after quantization or semantic loss. Pixel fidelity and downstream task quality can diverge, and semantic prioritization can discard small, unusual or out-of-distribution content.

The official description claims bit-exact decoding and favorable results on real satellite payloads but reports no bitrate, reconstruction metric, processor, task metric, energy, latency or flight condition. The record supports a semantic compression direction, not demonstrated ultra-low-bitrate superiority or in-orbit performance.

**Source and location**

Evidence tier: Primary captured official DAC description plus existing chapter level semcom discussion; no full paper extraction, task quality reconstruction or flight validation. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH791)

DAC 2026 official description; captured Problem, Mechanism / artifact, Workload, Hardware, Baseline, Measurements and Limits fields; record RESEARCH791; no manuscript pages.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** JPEG-like compression

task-agnostic learned compression

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH791

**Hardware or process assumptions:** Spaceborne low-power compute and communications; radiation and power assumptions are unspecified.

**Limits:** No bitrate, image quality, task accuracy, latency, energy, or flight results are reported.

Semantic prioritization may discard unexpected content.

Official description only; task and hardware validation is required.

**Method or artifact:** Semantic-enhanced on-board image compression.

**Metrics:** Ultra-low-bitrate efficiency is claimed qualitatively

**Problem:** Satellite links constrain image bandwidth while downstream tasks may need semantic content more than pixel fidelity.

**Workload or benchmark:** Satellite imagery; sensors, bitrates, task metrics, and onboard hardware are unspecified.

</details>

<span id="paper-dac-2026-research962"></span>

### Energyhdc: Intermittent Hyperdimensional Inference on Energy-Harvesting IoT

DAC 2026 · Record: `dac-2026-research962`

[Read the step-by-step explanation](#explanation-dac-2026-research962)

**Updated source-backed reading card**

Reviewed 2026-09-08. Deepens the existing EnergyHDC treatment into a paper-level reading; separates resume correctness, model accuracy and real outage completion, and makes checkpoint cost, dimension-first ordering, pruning, harvest traces and elapsed-time accounting explicit.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Energy-harvesting IoT devices experience intermittent power and need robust low-memory inference.

**Mechanism / artifact:**

Hyperdimensional inference designed for intermittent operation, combining energy-dependent checkpoint granularity, dimension-first execution and compile-time priority pruning; state format, pruning rule and checkpoint validity are unspecified.

**Workload — the work tested:**

Energy-harvesting IoT classification or sensing; datasets, model, vector dimension, inputs, harvest traces, outage timing, output requirement and task metrics are unspecified.

**Hardware and manufacturing assumptions:**

Low-power intermittent microcontroller or accelerator; captured description names MSP432P401R, but capacitor, memory, nonvolatile storage, write cost, clock, energy source and hardware conditions are unspecified.

**Baseline — the comparison method:**

Mementos

DynBal

Continuous-power ML

Checkpointed neural inference

Dataset, accuracy, energy trace, memory, outage and elapsed-time conditions are unspecified

**Reported measurements:**

The captured description reports up to 214× speedup over Mementos and 19.6× faster inference than DynBal at similar accuracy; it reports no datasets, exact accuracy differences, checkpoint size/count, outage traces, storage cost, wall-clock completion or full energy accounting.

**Limits on the conclusion:**

Intermittent inference has separate correctness questions: whether execution resumes from a complete state, whether the selected model remains accurate, and whether a valid output completes under the actual outage trace. A checkpoint must preserve all state needed to continue and distinguish an old partial result from a new inference.

Checkpoint frequency trades write energy and time against repeated work. Dimension-first execution reorders work, while priority pruning removes work and can change accuracy; a speedup from pruning is not only a checkpointing improvement. Average harvested power does not determine completion because outage timing and uninterrupted interval length matter.

The captured description reports up to 214× speedup over Mementos and 19.6× faster inference than DynBal at similar accuracy on an MSP432P401R under intermittent power, but provides no datasets, exact accuracy differences, outage traces, storage sizes or elapsed-time accounting. The record supports an intermittent-inference direction, not verified end-to-end completion or general harvest robustness.

**Source and location**

Evidence tier: Primary captured official DAC description plus existing chapter level energyhdc discussion; no full paper extraction, outage trace reconstruction or independent hardware validation. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH962)

DAC 2026 official description; captured Problem, Mechanism / artifact, Workload, Hardware, Baseline, Measurements and Limits fields; record RESEARCH962; no manuscript pages.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** continuous-power ML

checkpointed neural inference

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH962

**Hardware or process assumptions:** Low-power intermittent microcontroller or accelerator; storage and capacitor assumptions are unspecified.

**Limits:** No accuracy, energy, outage tolerance, latency, memory, or hardware results are reported.

Harvest profiles may be environment-specific.

Official description only; deployment validation is required.

**Method or artifact:** Hyperdimensional inference designed for intermittent operation.

**Metrics:** Intermittent inference efficiency is claimed qualitatively

**Problem:** Energy-harvesting IoT devices experience intermittent power and need robust low-memory inference.

**Workload or benchmark:** Energy-harvesting IoT classification or sensing; harvest profile, tasks, and hardware are unspecified.

</details>

## What remains to establish

Resolve unspecified workloads, comparison methods, resource budgets, and source locations before generalizing a reported gain. Multiple papers in this selected sample permit comparison of mechanisms, but do not by themselves establish recurrence across years or a long-term trend.

[All subthemes](../expanded-taxonomy-v1.md) · [Research directions](../directions/README.md)
