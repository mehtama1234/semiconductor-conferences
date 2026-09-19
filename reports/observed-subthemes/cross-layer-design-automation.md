# Cross layer design automation

This subject has 1 record in the selected sample. This page explains where it fits, then presents all captured paper evidence without shortening the measurements or limitations.

[Definitions used in the paper records](../reading-guide-v1.md)

## Understand the parent subject first

- [Design methodology and tooling](../themes/design-methodology-and-tooling.md)

## A logical function can have several physical implementations

A standard-cell library provides small circuit implementations from which larger digital designs are assembled. Two cells can compute the same Boolean function while differing in transistor arrangement, dimensions, connections, and physical layout. Those differences can affect area, delay, power, and how easily a larger design can use the cell.

Cross-layer exploration follows these consequences across design representations. Here “layer” means a level of design description, such as logic, circuit, or layout; it does not necessarily mean a physical metal layer. The selected paper, [L2L](../observed-subthemes/cross-layer-design-automation.md#paper-dac-2026-research1765), explores standard-cell library design from logic through layout.

The captured official description identifies that scope but supplies no numerical results or detailed search procedure. This article explains the engineering question without assigning unreported mechanisms to the framework.

## Why a logic-only score can miss the final cost

A logic representation describes what outputs depend on which inputs. A physical implementation must realize those dependencies using devices and wires that satisfy manufacturing constraints. Fewer logical operations do not necessarily imply less physical area or faster signal propagation.

Likewise, minimizing a cell's internal area can make its external connections less convenient. A larger design may then need more wiring or different placement to use it. These possibilities explain why cell quality must be evaluated at more than one representation; they are not claimed failures observed in L2L.

A useful exploration process must decide when a candidate is inexpensive enough to examine approximately and when it needs detailed construction and checking. The source does not expose whether L2L uses learned estimates, exact searches, heuristics, or some combination. Those choices remain unknown.

## From candidate cell to usable library entry

A candidate must preserve its intended function and satisfy physical rules. Its electrical behavior must also be characterized under the conditions in which tools will use it. An estimate for one load or operating condition does not describe all of those conditions.

Layout introduces connection effects that are absent from an ideal logical description. Evaluation after extraction includes modeled resistance and capacitance associated with the physical structure. A candidate that looks favorable before those effects are included may not retain that ranking afterward.

The captured record does not name the process, cells, extraction settings, characterization conditions, or final acceptance checks. It therefore does not establish that generated candidates became validated library entries. The title's logic-to-layout scope must not be expanded into measured silicon or complete production qualification.

## A library is more than a collection of individually good cells

The usefulness of a library depends on how a larger design selects and connects its entries. A cell that improves a frequently used function can have a different system impact from a highly optimized but rarely selected entry. Alternative cells may also compete for the same mapping opportunities.

Evaluation should consequently distinguish cell-level results from results obtained when representative designs are implemented with the candidate library. The larger-design comparison needs the same functional requirements, process assumptions, timing targets, and implementation flow. Otherwise improvements may reflect a different workload or relaxed constraints rather than a better library.

The source supplies no area, timing, power, yield, or design-suite results. Neither a cell-level gain nor a complete-library gain is quantitatively established by the captured description.

<span id="explanation-dac-2026-research1765"></span>

## L2L: select a cell by its downstream physical consequence

### A standard cell has several representations

A standard cell has a Boolean function, a circuit implementation, a physical layout, and characterized views used by synthesis and timing tools. The Boolean function says which output values follow from the inputs. The circuit realizes that function with transistors. The layout gives those transistors and their wires legal dimensions and positions. Characterization estimates how the resulting cell behaves under load, voltage, temperature and process conditions.

Two cells can be logically equivalent while differing in input capacitance, output drive, internal power, leakage, area, pin access, wire demand or delay. A logic-only optimizer sees the first representation and can miss costs that appear only after implementation. L2L's stated logic-to-layout scope is therefore a cross-layer decision problem: choose an early representation while charging for consequences that occur later.

### A candidate must survive a chain of checks

The useful path from candidate to library entry is sequential. First, the candidate must implement the required truth table or sequential behavior. Next, its transistor and layout realization must satisfy design rules. Parasitic extraction adds modeled resistance and capacitance from the physical geometry. Characterization then produces timing, power and other views for the larger design tools. A candidate that looks favorable before extraction can lose its ranking after wire and load effects are included.

The official description identifies L2L as a logic-to-layout exploration framework but does not state whether it uses exact search, heuristics, learned estimates, or another procedure. It also does not specify the process, cells, extraction tool, characterization corners, or final acceptance gates. These missing details are part of the result because a library-quality output requires more than a valid schematic or a low predicted area.

### Cell quality and library utility are different measurements

An individual cell is useful only when a synthesis or mapping flow selects it in a larger design. A cell with excellent delay but difficult pin access may cause extra routing elsewhere. A larger cell can improve a critical path but consume area or power when selected many times. A library can also contain several equivalent choices whose system impact depends on the workload and timing constraints.

The evaluation must therefore separate cell-level quality from design-level utility. It should report the same functions, library alternatives, process rules, timing targets and implementation tools for each baseline. It should also measure how often each candidate is selected, whether completed designs meet timing and power limits, and whether the result changes across representative circuits. A lower cell area alone is not a complete library result.

### Cross-layer search has a real evaluation budget

Each candidate may require logic checking, layout construction, extraction, characterization and a larger-design test. Search time therefore includes failed candidates and the cost of moving a candidate between representations. Approximate models can reduce this cost, but their errors matter most when they change which candidate is chosen. Reuse across similar cells can help, but it must be measured rather than assumed.

The captured source reports no area, timing, power, yield, search-cost or design-suite numbers. The named baselines—hand-designed cells and logic-only library optimization—define comparison questions, not measured results. L2L should not be read as signoff-quality validation, measured silicon, or production library qualification.

### What L2L establishes and what remains open

L2L establishes the proposed scope of exploring standard-cell libraries from logic through layout so that early decisions can be evaluated against later physical consequences. It does not establish a particular search mechanism, a quantitatively superior library, signoff completion, fabricated behavior, or general design productivity gain. A stronger evaluation would publish process and rule decks, cell/task populations, search and failed-candidate budgets, extraction/characterization conditions, cell and full-design metrics, baseline settings, yield or corner analysis, and independent signoff checks.

[Official DAC description, record RESEARCH1765](https://63dac.conference-program.com/presentation/?id=RESEARCH1765&sess=sess109)

## Count the search and validation work

Cross-layer evaluation can be expensive because each candidate may require several tool stages. Search efficiency should include candidate generation, failed layouts, electrical characterization, and any manual correction needed before the output can be used.

Reusing work across related cells can potentially reduce that cost, but the source does not identify such a reuse mechanism. A reproducible study would state the search budget, evaluated and rejected candidates, baseline preparation effort, and criteria used to select the final library. A result obtained with much more evaluation effort needs to be interpreted accordingly.

## The research direction supported by L2L

L2L motivates making early logic choices accountable to the physical and electrical behavior of the resulting cells. The strongest test would then ask whether those cells improve complete designs under fixed requirements and a stated engineering budget.

That is a concrete cross-layer question, not an established performance advantage or a historical adoption trend. The current official description supports identifying the proposed scope. Demonstrating its value still requires detailed implementation conditions, independently checked outputs, and measured or calibrated comparisons at both cell and larger-design levels.

## Compare the results carefully

First identify the inputs and required output quality. Then identify the limited resource: time, memory, communication, energy, circuit area, or correctness coverage. Ask which part of the method reduces that cost and which new cost it adds. Compare numbers only when the experiments hold these conditions sufficiently similar.

A conference description may explain the proposal while omitting the full experiment. An author preprint link may have been coded from its abstract. The source classification does not by itself establish that every table was read. Missing locations remain visible below.

## Complete captured evidence

These are evidence records, not substitutes for the explanations above. Each record preserves its problem, proposed method, measurements, comparison conditions, and source limits. A populated record does not establish that its mechanism has been fully explained or independently verified.

<span id="paper-dac-2026-research1765"></span>

### L2L: Logic to Layout Exploration of Standard Cell Library Design

DAC 2026 · Record: `dac-2026-research1765`

[Read the step-by-step explanation](#explanation-dac-2026-research1765)

**Updated source-backed reading card**

Reviewed 2026-09-08. Deepens the official-description reading; separates logic equivalence, circuit/layout realization, extraction/characterization, library utility and cross-layer search cost.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Standard-cell library design requires costly exploration from logical function choices through circuit, layout and characterized physical consequences.

**Mechanism / artifact:**

Logic-to-layout exploration framework for standard-cell library design.

**Workload — the work tested:**

Standard-cell circuits and libraries; functions, circuit populations, larger designs, timing targets and process corners are unspecified.

**Hardware and manufacturing assumptions:**

ASIC standard-cell design flow; technology node, design rules, transistor/library views, extraction, characterization, signoff tools and operating corners are unspecified.

**Baseline — the comparison method:**

Hand-designed standard cells

Logic-only library optimization

**Reported measurements:**

Library design-space efficiency and quality are claimed qualitatively; no area, timing, power, yield, search-cost or design-suite results are reported.

**Limits on the conclusion:**

Logical equivalence or pre-extraction area does not establish legal layout, parasitic-aware timing, power, library selection utility, yield or signoff completion.

The source does not expose whether search uses exact methods, heuristics, learned estimates, reuse, extraction settings or characterization gates.

Official description only; measured silicon and production-library qualification are not established.

**Source and location**

Evidence tier: Official DAC description; full manuscript and reproduction not performed. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH1765&sess=sess109)

DAC official description, Captured Description and Authors fields; record RESEARCH1765; no manuscript pages.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** hand-designed standard cells

logic-only library optimization

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH1765

**Hardware or process assumptions:** ASIC standard-cell design flow; technology node, rules, and signoff conditions are unspecified.

**Limits:** No area, timing, power, yield, search cost, or process results are reported.

Cross-layer objectives may create expensive evaluation loops.

Official description only; signoff-quality validation is required.

**Method or artifact:** Logic-to-layout exploration framework for standard-cell library design.

**Metrics:** Library design-space efficiency and quality are claimed qualitatively

**Problem:** Standard-cell libraries require costly cross-layer exploration from logic choices to physical layout.

**Workload or benchmark:** Standard-cell circuits and libraries; process, cells, extraction, and baselines are unspecified.

</details>

## What remains to establish

Resolve unspecified workloads, comparison methods, resource budgets, and source locations before generalizing a reported gain. This subject is represented by one paper and supports a case study, not evidence of recurrence or a long-term trend.

[All subthemes](../expanded-taxonomy-v1.md) · [Research directions](../directions/README.md)
