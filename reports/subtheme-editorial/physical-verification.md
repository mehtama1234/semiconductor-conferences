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
