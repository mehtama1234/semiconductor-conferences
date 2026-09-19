# Physical verification

This subject has 1 record in the selected sample. This page explains where it fits, then presents all captured paper evidence without shortening the measurements or limitations.

[Definitions used in the paper records](../reading-guide-v1.md)

## Understand the parent subject first

- [Verification and validation](../themes/verification-and-validation.md)

## Checking the geometry, then checking the checker

Design-rule checking, or DRC, evaluates layout geometry against a specified rule set. Rules can constrain the minimum width of a shape, separation between shapes, or enclosure of one layer by another. [KLayout's DRC documentation](https://www.klayout.de/doc/manual/drc_basic.html) describes these basic geometric checks. Passing them does not by itself prove correct circuit function, timing, or successful fabrication under every condition.

A rule deck is the executable collection of checks applied by a tool. Both the deck and the engine interpreting it can contain mistakes. Testing their behavior therefore requires layouts whose expected outcomes are known independently. This is the subject of [DRCGen](../observed-subthemes/physical-verification.md#paper-dac-2026-research907), the single selected record in this group.

<span id="explanation-dac-2026-research907"></span>

## DRCGen: generating diverse violations is useful only when each case has an independently defined meaning

### What a DRC test case has to establish

Design-rule checking evaluates geometric relationships in a layout. A rule can constrain width, spacing, enclosure, overlap, density or another property of shapes on specified layers. A test case is useful when its geometry, intended rule condition and expected result are all known.

A negative case should violate the requested rule. A positive case should satisfy it. Boundary cases matter because a spacing just below a limit, exactly at a limit and just above a limit can expose different interpretations of units, tolerances and inclusive or exclusive comparisons. A shape that looks unusual is not automatically a meaningful violation case; the rule exercised and expected checker behavior must be recorded.

### What controllable generation changes

DRCGen is described as a conditional diffusion model. A diffusion generator produces a pattern through iterative denoising, guided by conditions that constrain the output. Here, structured control hints encode spatial and semantic information about the requested violation, and a natural-language prompt identifies the desired type and target region.

The control promise has two parts. The requested violation must appear in the target region, and the rest of the layout must remain DRC-compliant under the declared rules. The second part is important because an unintended spacing, enclosure, connectivity or density violation can make it unclear which condition caused the checker result. Evaluation must report request success, target localization and unintended-violation rate separately.

### Why diversity is not coverage

Topological diversity concerns differences in how shapes are connected or arranged. Geometric diversity concerns differences in dimensions, positions or other geometric properties. Both can help create varied tests, but neither proves that the generator exercises all rule categories or interactions.

Thousands of distinct patterns can repeat the same rule behavior. Conversely, a small set can reveal a rare interaction if the cases are selected from a declared coverage model. A validation study should map each generated case to the rule, layer combination, boundary condition and interaction it is intended to test, then independently verify the expected outcome.

### What cross-PDK transfer must preserve

A process design kit defines layer names, dimensions, spacing limits, exceptions and interactions for a technology. Few-shot transfer means adapting the generator with a small amount of information from a new PDK. It does not mean that a geometry or prompt has the same meaning across kits.

A transfer evaluation should state whether the new PDK contributes examples, rule definitions, control hints or labels; which rules and layouts are unseen; and whether the generator is tested on a PDK whose structure differs from the training kits. The labels should not be produced only by the same checker whose rule-deck behavior is being evaluated, because that makes the validation circular.

### How to interpret the reported diversity results

The captured description reports 2.27× higher topological diversity and 1.02× higher geometric diversity than state-of-the-art methods, and 3.31× topological and 1.15× geometric improvements over Calibre LSG. These ratios need the dataset, diversity definitions, sample counts, rule mix and normalization method.

They do not establish violation validity, coverage, transfer accuracy, generation runtime or the discovery of tool or rule-deck errors. A generator can produce diverse shapes that violate unintended rules, or produce valid cases that cover only a narrow part of a deck.

### What the record establishes and where it stops

The official description establishes a controllable DRC-violation generation proposal using conditional diffusion, structured spatial and semantic controls, target-region requests, DRC-compliant surroundings and few-shot PDK transfer. It reports topological and geometric diversity improvements. It does not expose rule coverage, independent labels, transfer protocol, runtime, rare-rule interaction coverage or discovered checker errors.

The [DRCGen](../observed-subthemes/physical-verification.md#paper-dac-2026-research907) record is evidence of a controllable test-pattern generator, not proof that a production rule deck or DRC tool is correct. The explanation separates case meaning, conditional generation, isolation, diversity, cross-PDK transfer and independent validation.

## Why deliberately generate violations?

A correct checker should flag a layout that violates a rule and accept a layout that satisfies it, within that rule's defined scope. Deliberately constructed cases can test these boundaries more directly than an ordinary design that happens to contain some errors.

For a hypothetical minimum-spacing rule, useful cases include spacing slightly below the limit, exactly at it, and slightly above it, with the expected treatment defined by the specification. This is an illustrative testing requirement, not a reported DRCGen experiment. Different shape orientations and neighboring structures can exercise additional aspects of the same rule.

A large case count is not necessarily broad coverage. Thousands of near-identical violations can leave another rule or interaction completely untested. Meaningful coverage needs a declared set of rule behaviors and a mapping from cases to those behaviors.

## What DRCGen proposes and what remains unspecified

The official description identifies a controllable violation-case generator with transfer across process design kits. Control would be useful if it lets a reviewer request cases for a particular condition rather than relying only on whatever errors a generator happens to produce.

The captured source does not specify the controls, generation algorithm, supported rules, selected kits, or validation tools. It must not be assumed to use a language model, a geometric solver, or a particular learning method. Nor does the description establish that generated cases isolate exactly one violation or cover combinations of rules.

The source supplies no generation-validity, coverage, runtime, transfer-accuracy, or discovered-tool-error results. It supports identifying the proposal and its intended use, not concluding that it has validated a complete production deck.

## Cross-process transfer must preserve meaning

A process design kit supplies technology-specific design information. Moving a test-generation method between kits can require more than changing numerical dimensions: layer meanings, rule conditions, exceptions, and interactions may differ.

A transfer evaluation should state what is reused unchanged and what is supplied or adapted for the new kit. Testing new layouts under a familiar deck is a different claim from handling a previously unseen rule structure. The captured description does not expose a split or adaptation protocol that distinguishes those cases.

Similarly, comparing against handwritten tests requires accounting for expert preparation. Automated generation may reduce the cost of producing variants while still depending on substantial manual interpretation of the rules. That effort belongs in an end-to-end comparison.

## Avoid circular validation

If the tested checker supplies every expected label, agreement with those labels cannot independently establish that the checker is correct. Useful evidence can include directly reviewed specification-based cases, a separately implemented check, or disagreements reduced to small geometries and adjudicated against the rule definition. Each has its own limitations and should be documented.

Known-valid cases matter as well as violations. A checker that rejects everything finds every bad case but is unusable. Evaluation should therefore report missed violations and incorrect rejections separately, along with the rule categories and conditions involved.

## What would support a stronger conclusion?

A reproducible validation package would preserve the geometry, intended rule condition, expected markers, tool and deck versions, execution settings, and reviewed resolution of disagreements. Regression tests could then check that a confirmed fix remains effective after later changes.

DRCGen motivates systematic testing of physical-verification infrastructure. This is a narrower and more defensible direction than treating generated tests as proof of manufacturability. The present official description does not establish exhaustive rule coverage, cross-kit correctness, or measured fabrication improvements; those remain separate evidence requirements.

## Compare the results carefully

First identify the inputs and required output quality. Then identify the limited resource: time, memory, communication, energy, circuit area, or correctness coverage. Ask which part of the method reduces that cost and which new cost it adds. Compare numbers only when the experiments hold these conditions sufficiently similar.

A conference description may explain the proposal while omitting the full experiment. An author preprint link may have been coded from its abstract. The source classification does not by itself establish that every table was read. Missing locations remain visible below.

## Complete captured evidence

These are evidence records, not substitutes for the explanations above. Each record preserves its problem, proposed method, measurements, comparison conditions, and source limits. A populated record does not establish that its mechanism has been fully explained or independently verified.

<span id="paper-dac-2026-research907"></span>

### DRCGen: A Controllable DRC Violation Case Generator with Cross-PDK Transferability for Rule-Deck and Tool Validation

DAC 2026 · Record: `dac-2026-research907`

[Read the step-by-step explanation](#explanation-dac-2026-research907)

**Updated source-backed reading card**

Reviewed 2026-09-08. Reconciles the DRCGen card with the captured official DAC description; explains rule-deck test-case generation, conditional diffusion control, region-limited violations, DRC-clean surroundings, few-shot cross-PDK transfer and the difference between diversity metrics and checker-validation coverage.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Design-rule checking infrastructure needs known and diverse violation cases to validate rule decks and tools, while most layout-generation work emphasizes DRC-clean layouts rather than controllable negative cases.

**Mechanism / artifact:**

DRCGen: a conditional diffusion-based generator that uses structured control hints to encode spatial and semantic violation information, generates user-specified violation types in a target region from a natural-language prompt, maintains DRC compliance outside that region, and uses few-shot learning for transfer across PDKs.

**Workload — the work tested:**

VLSI layout patterns and DRC rule decks across PDKs; rule categories, layer geometries, target regions, PDK split, checker versions and expected labels are unspecified.

**Hardware and manufacturing assumptions:**

Physical-design verification flow using layout geometry, PDK rule decks and DRC tools; process layers, geometric tolerances, tool versions, generation runtime and compute platform are unspecified.

**Baseline — the comparison method:**

State-of-the-art DRC-violation generation methods

Calibre LSG

Handwritten DRC cases

Single-PDK generators

Rule coverage, validity labels, tool/deck versions, PDK split, runtime and diversity definitions are unspecified

**Reported measurements:**

The captured official description reports 2.27× higher topological diversity and 1.02× higher geometric diversity than state-of-the-art methods, and 3.31× topological and 1.15× geometric improvements over Calibre LSG; it does not report violation coverage, validity, transfer accuracy, runtime or discovered checker errors.

**Limits on the conclusion:**

A DRC rule defines a geometric condition such as minimum width, spacing or enclosure. A useful negative case must violate the intended condition, while a positive case must satisfy it under the same rule interpretation. Generating a visually unusual pattern does not establish which rule it exercises or whether the expected checker result is correct.

Conditional generation can accept a requested violation type, target region and natural-language description and produce structured geometry. Maintaining compliance outside the target region is a stronger isolation requirement: the generator must prevent unintended spacing, enclosure, connectivity or density violations elsewhere in the layout. The source does not expose the control representation or validation procedure.

A diffusion model generates a sample through a sequence of denoising steps guided by conditions. Structured control hints can constrain spatial and semantic properties, but controllability must be measured as the fraction of requests that produce the requested rule violation in the requested region while preserving all declared non-target rules.

Few-shot cross-PDK transfer means adapting from a small number of examples from another process design kit. PDKs can change layer meanings, dimensional limits, exceptions and rule interactions. A valid transfer test must separate unseen layouts, unseen rules and unseen PDKs, and must independently label the generated cases rather than using the same checker as both generator evaluator and oracle.

The description reports topological and geometric diversity ratios, but diversity is not coverage or correctness. A generator can produce many different invalid shapes that exercise few rules, or diverse shapes that violate unintended rules. No violation coverage, false-positive/false-negative validity, transfer accuracy, runtime, rare-rule interaction or tool-error discovery result is reported; the record establishes a controllable generation proposal and diversity claims only.

**Source and location**

Evidence tier: Primary captured official DAC description only; no full paper extraction, generator artifact reproduction or independent geometry labeling, rule coverage, cross pdk, runtime and drc tool validation. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH907)

DAC 2026 official description and data/review-packets/dac-2026-research907.json: DFM/DRC case-generation motivation; conditional diffusion model; structured spatial/semantic control hints; natural-language request; target-region violation with outside-region compliance; few-shot PDK transfer; 2.27×/1.02× diversity over state-of-the-art and 3.31×/1.15× over Calibre LSG; omitted rule coverage, validity, transfer protocol, runtime and tool-validation conditions.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** handwritten DRC cases

single-PDK generator

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH907

**Hardware or process assumptions:** Physical-design verification flow; process and layout assumptions are unspecified.

**Limits:** No violation coverage, validity, transfer accuracy, runtime, or tool results are reported.

Generated cases may miss rare rule interactions.

Official description only; multi-PDK validation is required.

**Method or artifact:** Controllable DRC violation case generator.

**Metrics:** DRC validation coverage is claimed qualitatively

**Problem:** DRC tools and rule decks need diverse violation cases for validation across process design kits.

**Workload or benchmark:** Layout geometries and DRC rule decks; PDKs, tools, and transfer protocol are unspecified.

</details>

## What remains to establish

Resolve unspecified workloads, comparison methods, resource budgets, and source locations before generalizing a reported gain. This subject is represented by one paper and supports a case study, not evidence of recurrence or a long-term trend.

[All subthemes](../expanded-taxonomy-v1.md) · [Research directions](../directions/README.md)
