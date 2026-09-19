# Package system co design

This subject has 1 record in the selected sample. This page explains where it fits, then presents all captured paper evidence without shortening the measurements or limitations.

[Definitions used in the paper records](../reading-guide-v1.md)

## Understand the parent subject first

- [Chiplets 3d and packaging](../themes/chiplets-3d-and-packaging.md)

## A package power plane has several requirements at once

A system-in-package combines components within a shared package structure. Conductive power and ground planes distribute electrical current to those components. Their geometry affects voltage loss, but it must also satisfy the package's manufacturing constraints. A design that performs well in an electrical model can still be unsuitable for fabrication.

The selected paper, [BLADE](../observed-subthemes/package-system-co-design.md#paper-dac-2026-research073), addresses this conflict through metal-density-constrained power/ground-plane synthesis. Its scope is specific: package plane generation. The record does not establish optimization of an entire computing system, even though the taxonomy places it under package–system co-design.

## Why more metal is not a complete objective

Metal density describes how much of a specified region is occupied by metal. The region and measurement rule are important: a package-wide average can conceal local imbalance. The official description associates uniform density constraints with controlling warpage and accommodating degassing holes. Warpage is deformation of the package; degassing holes are openings required by the process considered in the paper.

Those openings and density limits restrict the shapes available for current distribution. Electrical evaluation then asks whether the remaining conductive structure supplies acceptable voltage at its loads. IR drop is the voltage loss associated with current flowing through resistance. A low-resistance path in one region does not prove adequate voltage everywhere in the package.

The source does not specify the density windows, allowed density range, hole rules, material stack, or load conditions. These must remain unknown rather than being replaced with assumed industry-wide values. The degree of conflict between electrical and manufacturing objectives depends on those details.

## What BLADE proposes

The official description says BLADE expands planes from skeletons while enforcing metal-density and degassing constraints. A skeleton here is the starting geometric structure identified by the source, not a complete final plane. The exact construction and expansion rules are not exposed, so the explanation cannot claim a particular connectivity guarantee or geometric algorithm.

The method combines a fast IR-drop evaluator with bi-level Bayesian optimization. Bayesian optimization uses accumulated evaluations to guide which candidates to examine next when evaluating every choice is expensive. “Bi-level” indicates two levels of optimization in the proposed method. The short description does not identify the variables assigned to each level or their coordination procedure.

The important relationship is that candidate selection depends on an electrical estimate. If that estimate misranks geometries, the search can efficiently select a poor design. Search efficiency and evaluator accuracy therefore require separate validation, followed by a check of the final chosen plane.

## Six cases are an evaluation scope, not a performance number

BLADE is evaluated on six system-in-package cases. The captured description does not name the baseline methods or report numerical IR-drop improvements, absolute runtime, or package geometry. Six cases do not establish six independent technologies or broad transfer to other fabrication processes.

A meaningful comparison would use the same source and load locations, current demands, layer stack, manufacturing rules, and acceptance limits. It would report whether all constraints are satisfied, how voltage loss is distributed across the package, and how much time is spent generating and evaluating candidates.

Search results also need their total budget. Comparing a long optimized run with a short baseline run can confuse additional effort with a better method. Preparation of the fast evaluator, failed candidates, and any final repair should be counted separately and included where they belong in the intended workflow.

## From synthesis to physical confidence

Passing the encoded metal-density rules establishes compliance with those rules, not measured absence of warpage. Likewise, a predicted low IR drop is not a physical voltage measurement. Stronger evidence would validate the electrical evaluator against a trusted reference and assess the manufacturing assumptions with the appropriate process evidence.

The paper motivates treating electrical and fabrication requirements together while generating package structures. That is the defensible cross-level insight: package geometry constrains useful power delivery, so optimization cannot consider either requirement in isolation. The current record does not establish a complete system performance gain, improved production yield, or a general deployment recommendation. Those conclusions would require additional measured or calibrated evidence beyond the reported six-case scope.

<span id="explanation-dac-2026-research073"></span>

## BLADE: package-plane search must satisfy geometry, electrical, and manufacturing contracts together

A package power/ground plane is a conductive network that distributes supply and return current across package layers. Its shape changes path resistance and therefore voltage loss, but the package process may impose a metal-density window to reduce warpage and require degassing holes. Those holes remove or interrupt candidate metal regions. A plane that is electrically favorable under an unconstrained model can therefore be illegal or mechanically unsuitable.

BLADE is described as expanding a power/ground-plane skeleton while enforcing metal density and degassing constraints. The skeleton is a starting geometry, not evidence that the final candidate is connected, routable, manufacturable, or free of current bottlenecks. The captured description does not specify the representation, layer stack, expansion moves, connectivity checks, hole placement rules, density window, material model, or boundary conditions.

### The evaluator and the search can fail independently

The method combines a fast IR-drop evaluator with bi-level Bayesian optimization. Bayesian optimization uses previous candidate evaluations to choose where to sample next; bi-level means that the search has two coordinated levels, but the source does not identify their variables, acquisition functions, nesting, constraints, or stopping rule. A fast evaluator is useful only if its ranking agrees with a trusted electrical analysis over the relevant geometry and load range.

Validate both stages separately. Compare evaluator voltage fields, worst drops, current density and constraint violations against a trusted package solver on held-out planes. Then compare the optimizer's selected candidate with the best candidate found under a fixed evaluation budget, including failed or infeasible proposals, surrogate fitting, acquisition optimization, constraint handling, initialization, retries and final repair. A lower surrogate objective is not proof of lower physical IR drop.

### Density compliance is not warpage measurement

Metal density must be defined over a region and window: a package-wide average can hide local windows that violate process rules. Satisfying an encoded density constraint shows only that the candidate meets that encoded rule. It does not establish mechanical warpage, laminate behavior, thermal expansion, fabrication yield, or the manufacturability of contacts, vias and degassing openings. Those claims require the process stack, mechanical model or measured package evidence.

### IR-drop comparisons need the complete electrical boundary

Report source and sink locations, current waveforms, layer resistances, vias, return paths, temperature, frequency, allowable voltage limits, solver tolerances and whether coupling or transient behavior is modeled. Measure spatial distributions and worst-case percentiles, not only an average. Include plane generation, evaluator time, constraint checking, repair and any downstream extraction in the search budget. Compare against named prior synthesis methods with the same geometry, loads, rules, solver and evaluation budget.

The six SiP cases establish an evaluation scope, not broad process transfer. The source reports that BLADE satisfies the metal-density constraint and achieves superior IR-drop performance, but provides no numerical IR-drop gain, baseline identity, geometry, runtime, mechanical result, fabricated-package measurement or yield. The evidence supports constrained package P/G-plane synthesis, not demonstrated production-ready power integrity, warpage control, or general package-system improvement.

## Compare the results carefully

First identify the inputs and required output quality. Then identify the limited resource: time, memory, communication, energy, circuit area, or correctness coverage. Ask which part of the method reduces that cost and which new cost it adds. Compare numbers only when the experiments hold these conditions sufficiently similar.

A conference description may explain the proposal while omitting the full experiment. An author preprint link may have been coded from its abstract. The source classification does not by itself establish that every table was read. Missing locations remain visible below.

## Complete captured evidence

These are evidence records, not substitutes for the explanations above. Each record preserves its problem, proposed method, measurements, comparison conditions, and source limits. A populated record does not establish that its mechanism has been fully explained or independently verified.

<span id="paper-dac-2026-research073"></span>

### BLADE: Bi-Level Bayesian Optimization for Metal-Density-Constrained Multi-Layer Package Power/ground Plane Synthesis

DAC 2026 · Record: `dac-2026-research073`

[Read the step-by-step explanation](#explanation-dac-2026-research073)

**Updated source-backed reading card**

Reviewed 2026-09-09. Deepens the BLADE package-plane treatment into a paper-level reading; separates metal-density and degassing-constrained geometry generation, fast IR-drop evaluation and bi-level Bayesian search from evaluator validity, mechanical/process evidence, numerical IR-drop gain and package-system generalization, while preserving the six-SiP-case source scope.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Advanced-package power/ground planes must preserve power integrity while satisfying metal-density and degassing-hole constraints intended to limit warpage.

**Mechanism / artifact:**

Metal-density-aware power/ground-plane synthesis that expands plane skeletons under density and degassing constraints, uses a fast IR-drop evaluator, and applies bi-level Bayesian optimization; geometry representation, layer/process model, optimizer levels and constraint handling are unspecified.

**Workload — the work tested:**

Six system-in-package power/ground-plane cases with metal-density and degassing constraints; package geometry, layer count, source/load map, current waveforms, density windows, hole rules, design split and solver conditions are unspecified.

**Hardware and manufacturing assumptions:**

Multi-layer package P/G planes with process-driven metal-density, degassing and warpage concerns; materials, stackup, vias, package dimensions, mechanical model, electrical solver, thermal/transient conditions, fabrication and measurement status are unspecified.

**Baseline — the comparison method:**

Prior package P/G-plane synthesis approaches

Same skeletons, geometry, layer stack, source/load locations, current demand, density and degassing rules, IR-drop solver, evaluation budget and acceptance thresholds are unspecified

**Reported measurements:**

The source reports satisfaction of the metal-density constraint and superior IR-drop performance on six SiP cases, plus search efficiency, but gives no numerical IR-drop gain, absolute voltage values, worst-case distribution, baseline identity, runtime, candidate count, evaluator error, warpage, yield or fabricated-package measurement.

**Limits on the conclusion:**

Encoded metal-density and degassing checks are geometric constraints, not measurements of warpage or fabrication yield. Define local density windows, material and layer stack, hole/via rules, mechanical boundary conditions and process tolerances; validate accepted candidates with appropriate mechanical or package-process evidence.

A fast IR-drop evaluator can misrank plane geometries. Compare voltage fields, worst drops, current density and constraint violations with a trusted package solver on held-out geometries and loads; include surrogate fitting, infeasible candidates, constraint repair, extraction and final verification in the bi-level Bayesian-optimization budget.

The six-case description supports constrained package power/ground-plane synthesis, not demonstrated production-ready power integrity, warpage control or general package-system improvement. No numerical IR-drop gain, named baseline, geometry/process matrix, runtime, fabricated-package result or yield evidence is reported.

**Source and location**

Evidence tier: Primary captured official DAC description plus existing authored blade/package plane explanation; no full paper extraction, reproduced bayesian search, trusted solver comparison or fabricated package measurement. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH073)

DAC 2026 official description, first and final paragraphs; existing package-system-co-design explanation; captured Problem, Mechanism / artifact, Workload, Hardware, Baseline, Measurements and Limits fields; no full manuscript, solver trace, package geometry or fabrication validation.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** prior package P/G-plane synthesis approaches

**Evidence locators:** Not established in the captured evidence.

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH073&sess=sess155

**Hardware or process assumptions:** Not established in the captured evidence.

**Limits:** The description does not expose numerical IR-drop gains, baseline names, or package geometry/process assumptions.

**Method or artifact:** Metal-density-aware P/G-plane synthesis with a fast IR-drop evaluator and bi-level Bayesian optimization.

**Metrics:** metal-density constraint satisfaction

IR-drop performance

design-space search efficiency

**Problem:** Package power/ground planes must maintain power integrity while meeting uniform metal-density constraints that prevent warpage and accommodate degassing holes.

**Workload or benchmark:** Six system-in-package power/ground-plane cases with metal-density and degassing constraints.

</details>

## What remains to establish

Resolve unspecified workloads, comparison methods, resource budgets, and source locations before generalizing a reported gain. This subject is represented by one paper and supports a case study, not evidence of recurrence or a long-term trend.

[All subthemes](../expanded-taxonomy-v1.md) · [Research directions](../directions/README.md)
