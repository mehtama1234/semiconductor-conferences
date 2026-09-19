# Generative design and synthesis

This subject has 7 records in the selected sample. This page explains where it fits, then presents all captured paper evidence without shortening the measurements or limitations.

[Definitions used in the paper records](../reading-guide-v1.md)

## Understand the parent subject first

- [AI assisted EDA](../themes/ai-assisted-eda.md)

## Generating a circuit means choosing a structure

A circuit's required behavior can have many implementations. A generator selects components, connections, or a program representation intended to realize that behavior. A synthesis process then maps the representation toward an implementation using available hardware elements and constraints.

The number of choices grows quickly with circuit size. Learning and search can help propose candidates, but each candidate still needs a correctness check and a meaningful cost evaluation. A small graph is not automatically a small or fast physical circuit after mapping and wiring.

## Separate the generated representation from the final implementation

A logic representation can hide details that become important later. For example, it may count operations without representing wire lengths, electrical drive strength, or the available cell library. A reduction in representation size can be useful while leaving final timing or energy unchanged.

The evaluation should identify each transformation between generated output and measured implementation. If a later optimizer contributes much of the improvement, the result should retain that contribution rather than attributing all gains to generation.

## Shortcircuit searches for logic structure

Shortcircuit's captured method generates an AND-inverter graph using pretraining and search. An AND-inverter graph represents Boolean computation using AND operations and inversions. Search explores different graph structures while a learned component guides which choices appear promising. [Recorded evidence](../observed-subthemes/generative-design-and-synthesis.md#paper-dac-2026-research2329)

The stored description leaves circuit-size results, search cost, wider input coverage, and mapped hardware tradeoffs unresolved. Correctly implementing small Boolean functions is an important capability, but it does not establish improved physical-design quality or transfer to much larger circuits.

<span id="explanation-dac-2026-research2329"></span>

## Shortcircuit: a search-generated Boolean graph must be correct, efficiently found, and still good after technology mapping

An AND-inverter graph (AIG) represents Boolean logic with two kinds of nodes: AND operations and inverted edges. A truth table specifies the required output for every input assignment. Generating an AIG from a truth table means choosing a graph whose evaluated Boolean function matches that table. Many different graphs can implement the same function, so correctness is a constraint while graph size, depth, switching behavior and later mapped hardware are possible objectives.

Shortcircuit is described as a transformer that generates AIGs directly from truth tables. It uses supervised pretraining to learn useful graph-generation behavior and an AlphaZero variant to search candidate structures. Greedy rollout accelerates the search. These parts solve different problems: pretraining supplies a proposal distribution, search explores alternatives using an objective, and rollout estimates or completes decisions quickly. The paper must state the graph state, allowed actions, terminal condition, reward, search budget, correctness check and how invalid partial graphs are handled.

The first invariant is functional equivalence. Every generated graph must be evaluated on all input assignments for the stated input width, or checked with a formally equivalent method. “Guaranteed correctness” is meaningful only if the guarantee covers the generator's output space, not merely the 500 test functions. Report invalid-candidate rate, equivalence-check cost, timeout behavior, duplicate graphs, and whether the search can return no candidate under its resource budget. For larger input counts, exhaustive truth-table checking itself changes cost, so the verification method must be stated.

Circuit size is not one universal quantity. It may mean number of AIG nodes, AND nodes, graph depth, literal count, mapped standard-cell area, or another representation measure. A smaller AIG can map to a larger or slower circuit because technology mapping depends on the cell library, fanout, buffering, wire estimates, timing constraints and optimization passes. Evaluate the generated graph through the same technology mapper and report area, delay, power, depth, node count and mapping runtime under named constraints. If only AIG size is measured, do not call it a physical PPA improvement.

The AlphaZero search has a total-cost boundary. Training data creation, transformer inference, search expansions, rollout evaluation, equivalence checking and postprocessing all consume time and hardware. The reported 31× greedy-rollout speedup needs the reference rollout, hardware, batch size, number of candidates, search quality and whether preprocessing or model loading is included. A faster rollout that chooses worse graphs is not an end-to-end search improvement. Report quality at equal search budgets and search time, not only speed at an unspecified operating point.

Generalization is constrained by the truth-table size and source distribution. The captured evaluation uses 500 eight-input truth tables derived from real circuits. State the train/validation/test split, whether functions from the same source circuit cross splits, input permutations, function difficulty, output count, structural distribution and test leakage. Evaluate larger input widths, unseen functions, multi-output logic, highly unbalanced functions, parity-like functions and functions with different minimal graph structures. A result on eight-input truth tables does not establish synthesis of large RTL or full designs.

The baselines should include ABC with a named version and options, prior deep-learning generators, random or heuristic AIG search, and an oracle or exhaustive result on small functions where feasible. Hold the truth tables, equivalence requirement, search time, candidate budget, hardware, mapper, library and PPA constraints constant. Include ablations for supervised pretraining, AlphaZero search and greedy rollout. Report the fraction of cases where the method wins, ties or loses, not only the mean circuit size.

The captured description supports transformer-plus-search AIG generation, claims functional correctness, says it outperforms ABC in circuit size, and reports a 31× greedy-rollout speedup on 500 eight-input truth tables. It does not expose exact size values, timing/area/power tradeoffs, training or search cost, ABC configuration, mapping results or generalization beyond eight inputs. Functional correctness does not imply PPA superiority after technology mapping. The evidence supports a learned Boolean-graph search direction, not demonstrated scalable physical circuit improvement.

<span id="explanation-dac-2026-research2476"></span>

## FlowPlace: a generated placement is useful only after it is legal, routable and evaluated under the same physical-design constraints

Chip placement assigns cells or larger design objects to physical locations on a die. Placement influences wirelength, congestion, timing, power, area and the difficulty of later routing. A placement is not useful merely because its coordinates look plausible. Cells must obey non-overlap, boundary, orientation, density, keepout and site rules, and the result must remain valid when detailed placement, routing and timing analysis are applied.

FlowPlace is described as a flow-matching generative placement method with mask-guided synthetic data generation, flow-based training with flexible prior injection, and hard-constraint sampling for overlap-free layouts. These components address different parts of the pipeline. Synthetic data affects the training distribution; the flow model learns a distribution or transformation for placements; prior injection changes the starting or conditioning information; hard constraints restrict samples during generation. The paper must state which constraints are enforced during sampling, which are repaired afterward, and which are checked only by the physical-design tools.

Placement quality is a vector. Total or routed wirelength, congestion, worst negative slack, total negative slack, timing violations, power, area, density, routing completion, design-rule violations and runtime can trade off. “Better PPA” is not interpretable without the exact objective, technology library, clock constraints, placement/routing flow and reporting tools. A shorter wirelength can worsen timing if critical nets are mishandled; zero overlaps can coexist with severe congestion or unroutable channels.

Hard-constraint sampling needs a correctness boundary. Explain how the model represents cell locations, masks occupied sites, handles variable cell sizes, respects die boundaries and keeps constraints valid during every generation step. If a repair or legalization stage removes overlaps, report its runtime, movement, failure rate and effect on quality. Zero overlaps after a repair pass is different from a sampler that produces legal layouts directly. Check legality with an independent placer or verifier, not only the generation code that created the constraint.

Flow matching is a distribution-learning method whose output depends on the training corpus, prior, conditioning features, noise or path schedule, sampling steps and guidance. The method should state whether it learns from expert placements, synthetic placements, random placements or a mixture, and how mask-guided data is created. Training-data bias can produce fast but poor placements for unseen netlists, floorplans, block sizes, utilization, macros, power domains or technology nodes. Evaluate distribution shift explicitly.

The source reports experiments on OpenROAD and ICCAD 2015 benchmarks, with better PPA metrics, 10–50× faster sampling efficiency and zero overlaps. These claims require the exact benchmark subset, netlists, constraints, hardware, sampling-step count, preprocessing, model loading, legalization, OpenROAD version, downstream flow and repeated-run variation. Compare end-to-end placement time, not only neural sampling time, and report the full PPA table and legality rate per design. A range as broad as 10–50× may reflect different baselines or instance sizes and should not be treated as one universal speedup.

The baselines should include analytic placement, the same downstream legalization and physical-design flow, reinforcement-learning placement, prior diffusion or generative placement, and a random or standard initial placement where appropriate. Hold technology, libraries, constraints, macro handling, utilization, routing settings, timing analysis, seeds and evaluation boundary constant. Ablate mask-guided data, flexible prior injection, flow matching and hard constraints independently. Include the best-of-N sampling cost if the method generates multiple candidates.

The captured evidence supports a learned placement direction and reports claims from OpenROAD and ICCAD 2015 experiments: improved PPA, 10–50× sampling efficiency and zero overlaps. It does not expose wirelength, congestion, timing, runtime boundary, generalization, legalization cost or per-design legality. Generative placement can be sensitive to training-distribution shift. The evidence supports faster constrained placement proposals under stated conditions, not demonstrated robust end-to-end PPA improvement across physical-design workloads.

<span id="explanation-dac-2026-research179"></span>

## LLMVA: a generated Verilog-A model must remain physically calibrated when it is used to choose MRAM circuits

Verilog-A is a behavioral modeling language for analog and device-level behavior. A model describes currents, voltages, switching, state and parameter dependence so that a circuit simulator can predict how a device behaves inside a larger circuit. For an emerging memory device, the model is not just code. Its equations and parameters represent physical mechanisms, measured variation and operating limits. A model can compile and fit a few curves while still giving wrong circuit-level decisions.

LLMVA is described as an LLM-assisted iterative process for modeling spin-transfer-torque magnetic-tunnel junctions (STT-MTJs) and using device characteristics and circuit indicators for design-technology co-optimization (DTCO). The iteration must be made explicit: what the LLM observes, which Verilog-A code or parameters it changes, what simulator or measurement evaluates the change, what objective or constraint guides the next step, and when a human accepts the model. Device fitting, circuit evaluation and technology decisions are different loops and should not be collapsed into one efficiency claim.

The first requirement is physical validity. Define the measured quantities, parameter extraction procedure, units, temperature, voltage, current, pulse width, magnetic state, stochastic behavior, endurance and variation. Test the model on held-out device measurements, not only the traces used to tune it. Compare switching probability, resistance states, write/read behavior, transient response, retention or other quantities relevant to the target circuit. Report error distributions by operating condition and device, not only a maximum or average number.

The source reports that the deviation between front-test and post-test results of the MTJ does not exceed 9.2%. That phrase needs a measurement definition: which quantity, which devices, which conditions, which test stages and whether the same samples or independent samples are being compared. Front-test/post-test agreement can show model or process consistency, but it does not by itself establish model accuracy against an independent calibrated reference. Preserve the 9.2% claim with its boundary rather than treating it as universal device-model error.

Circuit-level validation asks whether model error changes a design decision. Simulate the MRAM circuit with the generated model and a trusted reference under the same PDK, corners, mismatch, parasitics, sense margin, write/read timing, voltage and temperature. Report macro capacity, density, access time, energy, yield-related margins, write failure, read failure, leakage, area and power where relevant. A model that matches a device curve but changes the selected circuit topology or operating point incorrectly can still harm DTCO.

The reported macro is a 4-Mb, 28-nm MRAM design that was taped out, according to the captured description. Tape-out is a design milestone, not proof of fabricated performance. Separate pre-silicon simulation, wafer measurement, packaged-chip measurement, post-test analysis and production validation. State the PDK, foundry/process, bit-cell and peripheral assumptions, measured sample count, test conditions and whether the macro's functional, timing, energy and yield behavior matched prediction.

The claimed approximately 50% reduction in designer and time cost also needs a denominator. Count human hours, LLM calls/tokens, prompt and model preparation, debugging, simulator runs, failed iterations, review, calibration and reuse. Compare the same task, quality threshold, experience level, tools and number of design iterations against manual Verilog-A modeling and fixed technology/circuit optimization. A faster first draft is not a lower total engineering cost if validation or correction work moves to the designer.

The baselines should include a manually authored calibrated Verilog-A model, an existing device-modeling flow, fixed circuit/technology optimization, and an LLM-assisted process without iterative feedback where possible. Ablate model generation, measurement feedback, circuit indicators, retrieval or human review. Evaluate unseen device lots, temperatures, voltages, process corners, circuit sizes and design targets. Report model compile failures, physically invalid equations, convergence failures, simulator runtime and the number of human corrections.

The captured evidence supports LLM-assisted STT-MTJ Verilog-A iteration for MRAM DTCO and reports a 4-Mb 28-nm macro tape-out, a front-test/post-test deviation not exceeding 9.2%, and an approximately 50% reduction in designer/time cost. It does not expose the error metric, calibration data, convergence, PPA, device distributions, sample count, human-cost accounting or fabricated-macro validation details. Generated behavioral models can encode physically invalid assumptions. The evidence supports an LLM-assisted device-modeling direction, not demonstrated calibrated model accuracy or general MRAM co-design efficiency.

<span id="explanation-dac-2026-research2646"></span>

## TOPCELL: a transistor topology is successful only after electrical, layout, routing and signoff checks agree

A standard cell is a reusable circuit layout implementing a logic function. Its transistor topology specifies which transistors exist, how they connect, which diffusion regions are shared, where contacts and gates are placed, and how the topology can be laid out inside the cell boundary. The topology affects transistor sizing, parasitic capacitance, diffusion area, pin access, local routing, power, delay and the ability to place the cell next to other cells.

TOPCELL is described as reformulating topology exploration as a generative task for LLMs and fine-tuning with Group Relative Policy Optimization (GRPO). The model is aligned to logical and spatial constraints. This changes the search proposal mechanism; it does not remove the need to check the generated topology. The system must represent device connectivity and geometry unambiguously, define the legal action space, state how a candidate is completed, and specify which simulator, extractor, design-rule checker and router supply the reward or rejection signal.

Logical validity is the first gate. A topology must implement the intended truth table or transistor-level function under stated assumptions. Check connectivity, transistor type, well/body connections, power rails, floating nodes, shorts, opens, state behavior, sizing limits and corner-case operation. A model can generate a graph that looks structurally plausible while reversing a signal, omitting a body connection or creating an electrically invalid path. Report invalid proposal rate, repair rate, simulation failures and the cost of each check.

Physical validity is a second gate. The layout must obey design rules for the target process, including minimum widths and spacings, enclosure, implant/well rules, contacts, diffusion sharing, pin access, boundary and power-rail conventions. Routability is not equivalent to no transistor overlap. Run design-rule checking, extraction and routing with named tools and process design kits. Record violations, unroutable nets, pin-access failures, antenna or density issues, extraction convergence and the amount of post-generation repair.

PPA and routability are coupled. Diffusion sharing can reduce area and parasitic capacitance but can constrain pin access or create a longer route. A topology with fewer transistors may have worse delay because of stack depth, series resistance or load. A compact cell can be difficult to abut or route in a library. Evaluate area, delay, power, leakage, pin accessibility, wirelength, congestion, routing completion, design-rule violations and library characterization under the same sizing, load, slew, voltage, temperature and corner conditions.

GRPO needs a reproducible reward boundary. State the groups or candidates used for relative comparison, reward terms, normalization, constraint penalties, sampling temperature, number of samples, training data, model base, prompt representation and whether failed candidates receive a score or are filtered. A reward that favors geometric compactness may sacrifice electrical behavior; a reward based on a surrogate may not predict extracted parasitics. Validate reward rankings against signoff or extraction outcomes on held-out topologies.

The source reports industrial-flow experiments targeting advanced 2-nm technology, and a 7-nm library-generation task in which TOPCELL allegedly matches the layout quality of exhaustive solvers while achieving an 85.91× speedup with zero-shot generalization. These are bounded claims. The evaluation must identify which process is used for training, which is used for testing, what “layout quality” contains, whether exhaustive-solver time includes all checks, whether TOPCELL time includes generation and validation, and how many cells and seeds are measured. Cross-node transfer is not established merely by labeling a result zero-shot.

The baselines should include manual topology design, exhaustive or search-based cell optimization, foundation LLMs without GRPO, and the same downstream extraction, routing, characterization and signoff flow. Hold logic function, drive strength, cell height/track structure, process, PDK, constraints, loads, corners, tool versions and repair budget constant. Ablate logical constraints, spatial constraints, GRPO, retrieval or repair. Report per-cell wins and failures rather than only an average or one speedup.

The captured evidence supports LLM-guided standard-cell topology search and reports 2-nm industrial-flow experiments, a 7-nm library-generation result, zero-shot language or process transfer as described, matching layout quality to exhaustive solvers, and an 85.91× speedup. It does not expose area, timing, power, routability, yield, signoff, repair, reward calibration or search conditions. LLM proposals may violate design rules or electrical constraints. The evidence supports a constrained topology-generation direction, not demonstrated signoff-quality standard-cell improvement across technologies.

<span id="explanation-dac-2026-research2793"></span>

## CircuitDiff: an RTL-conditioned netlist representation is useful only if early metrics remain valid outside the training lineage

RTL describes the intended register-transfer behavior before synthesis. A netlist describes an implementation graph after that behavior has been mapped into cells or other hardware elements. The netlist exposes structural information that can correlate with timing, area, power or other circuit metrics, but it is not automatically equivalent to the RTL and it does not by itself contain every physical effect. CircuitDiff addresses the expensive gap between early RTL decisions and later circuit analysis by learning a shared representation across RTL and netlist graphs.

The described pretraining path encodes an RTL graph as a condition for a netlist graph denoising diffusion model. During fine-tuning, learnable queries use cross-attention to draw on the pretrained representation for early circuit-metric prediction. This is a representation and prediction mechanism. It should not be described as directly synthesizing a valid netlist, recovering a unique physical implementation, or replacing downstream EDA analysis unless those outputs and checks are separately demonstrated.

The graph contract is central. Define RTL nodes, operators, signals, registers, control dependencies and hierarchy; define netlist cell types, pins, fan-in/fan-out, constants, clock/reset semantics and graph-level attributes; and state how synthesis transformations, retiming, optimization, black boxes and technology mapping affect correspondence. A denoised graph can be syntactically well formed while losing a control edge, changing polarity, merging state, or representing a circuit that no longer matches the RTL. Check graph validity and RTL/netlist equivalence independently.

Diffusion pretraining also needs a reproducible corruption and recovery boundary. State which netlist graph is noised, the noise schedule, conditioning representation, denoising target, time embedding, sampling steps, query initialization, cross-attention layers and fine-tuning objective. Compare the learned representation with a sequence-only RTL model, a graph encoder without diffusion pretraining, and simpler structural or synthesis-derived features. Report training, inference and any repeated-sampling cost separately.

“Early circuit metrics” must be named. They might be post-synthesis area, timing, power, congestion, cell counts or other proxies, but these have different labels, tools and physical meaning. Record the synthesis version, cell library, constraints, clock assumptions, process, voltage, temperature, parasitics and whether the target is pre-layout, post-route or a surrogate. Compare predicted values with held-out measurements and report error distributions, calibration, ranking quality, failures and inference latency. If a prediction guides design-space exploration, measure the quality of the designs selected by the predictor, not only its regression error.

The source claims superior early-stage circuit-metric prediction against state-of-the-art models while maintaining computational efficiency and supporting a left-shifted design workflow. Those claims need a strict split. RTL and netlists derived from the same design lineage can leak synthesis patterns, IP structure or near-duplicate templates. Split by design family, module, repository, RTL style, technology and netlist lineage where possible, and test unseen designs, synthesis settings and distribution shifts. A model that predicts labels well within one synthesis corpus may fail when the library, constraints or optimization recipe changes.

The baselines should include the named state-of-the-art predictors, sequence-only RTL models, graph encoders without diffusion pretraining, synthesis-derived heuristics and a simple feature baseline. Hold the RTL input, netlist availability, label-generation flow, design split, model size, training data, compute budget and evaluation metrics constant. Ablate RTL conditioning, netlist diffusion pretraining, learnable queries and cross-attention. Report per-design wins and failures, not only an average improvement, and include the cost of generating any required netlist or graph labels.

The captured evidence supports RTL-conditioned netlist representation learning for early circuit-metric prediction and reports qualitative superiority and computational efficiency. It does not expose metric names, errors, runtime, dataset size, split controls, synthesis conditions, physical PPA results, equivalence checks or the status of the announced code/data URL. The evidence supports a left-shifted prediction direction, not demonstrated RTL-to-netlist synthesis or robust physical-design improvement.

## Evolving a design tool changes the method itself

The multi-agent ABC record concerns modifying the code of a synthesis tool and evaluating those modifications against correctness and circuit-quality checks. Here the generated object is software that will later transform circuits. [Recorded evidence](../observed-subthemes/generative-design-and-synthesis.md#paper-dac-2026-research1784)

This creates two evaluation levels. The changed program must remain correct and maintainable, and the circuits it produces must meet their requirements. Improvements on the benchmark circuits used to select code changes can reflect specialization to those examples. Unseen circuit suites and regression checks are needed to determine whether the tool itself improved more generally.

The current record does not establish regression rates, code-review effort, search cost, or quantitative quality outcomes. Those conditions must be recovered before a broad claim about autonomous tool improvement is supported.

<span id="explanation-dac-2026-research1784"></span>

## Self-evolved ABC: changing synthesis software requires software correctness, circuit-quality validation and protection against benchmark overfitting

ABC is a logic-synthesis program. It transforms a Boolean or hardware representation through passes that simplify logic, restructure graphs, map or prepare designs, and report implementation quality. A code-evolution system changes the program itself rather than directly choosing one circuit for one input. The result must therefore be judged at two levels: the changed software must remain a valid, reproducible tool, and the circuits it produces must remain correct and improve under defined constraints.

The paper describes a multi-agent loop in which LLM agents propose and implement changes to the ABC repository. Correctness tests reject invalid changes, and standard benchmark circuits provide quality-of-result (QoR) feedback. The seed includes human-designed optimizations and external research code. The system's contribution is the search and integration process; improvements already present in the seed must not be attributed to autonomous evolution. Record the initial repository revision, seed patches, agent roles, prompts, model versions, compiler/toolchain, iteration budget, patch acceptance rule and final code revision.

Code correctness is broader than “the test suite passed.” A patch can pass functional tests while changing command behavior, nondeterministically failing, consuming excessive memory or breaking an uncommon pass combination. Validate outputs against a trusted reference, run regression and property tests, test invalid inputs and failure paths, and record flaky or timed-out tests. Review the diff for unsafe changes, dependency changes, generated code, licensing, reproducibility and maintainability. A change that improves one benchmark but destabilizes the tool is not a general synthesis improvement.

QoR is also a vector, not one score. area, delay, power, logic size, depth, memory, runtime and constraint violations can move in opposite directions. State the technology library, timing constraints, mapping flow, optimization objective, clock assumptions, effort levels and reporting tools. Compare generated ABC revisions and the seed against the same circuits and conditions. If a weighted score selects patches, publish the weights and show the individual QoR dimensions; otherwise a composite improvement can hide a serious regression.

The search loop creates selection bias. Agents propose patches based on benchmark feedback, so repeated evaluation on the same circuits can overfit the benchmark suite or its scoring function. Keep a development set for patch selection and a sealed test set that agents never see. Add structurally different circuits, larger designs, unseen RTL or Boolean networks, different constraints, random seeds and multiple tool configurations. Report per-circuit wins, ties, regressions, patch survival rate and how often a change is reverted after broader testing.

The cost boundary must include the entire evolution process. Measure LLM calls and tokens, compilation, test execution, synthesis runs, simulation, hardware time, storage, human review and failed patches. Report wall-clock time, parallel-agent resources, number of proposals, accepted changes, rejected changes, duplicate patches and the QoR gained per accepted patch. “Autonomous” should identify which steps required no human intervention and which external code or seed optimizations were supplied beforehand.

The baselines should include the unmodified ABC revision, the human-designed seed, each external research optimization separately, a conventional human or scripted search under a comparable budget, and the final evolved revision. Compare on the same held-out circuits and constraints. Ablate agent count, model, feedback signal, test strength, patch memory and iteration count. A result that depends on an unreleased prompt, hidden manual repair or an unreported seed cannot be reproduced as autonomous evolution.

The captured description supports a multi-agent LLM process that modifies ABC, validates candidate changes, and uses benchmark QoR feedback to discover improvements beyond seeded heuristics and external code. It reports no numeric QoR, regression rate, search cost, code-review burden, patch history, model versions or reproducibility detail. Autonomous code changes may overfit benchmarks or introduce latent correctness and maintainability risks. The evidence supports an automated EDA-software search direction, not demonstrated generally improved or maintainable synthesis tooling.

## StepPRM-RTL evaluates intermediate reasoning

StepPRM-RTL's captured method trains a model using stepwise trajectories and a process-reward model. A reward model scores intermediate work and can influence which reasoning path is selected. The generated hardware description still needs independent execution and synthesis checks. [Recorded evidence](../observed-subthemes/generative-design-and-synthesis.md#paper-dac-2026-research1742)

An intermediate score can encourage a reasoning style without accurately predicting correctness. The key experiment is whether using those scores yields more valid, useful implementations on new tasks within a comparable total budget. Reward calibration, failed outputs, training cost, and final synthesis quality remain unresolved in the captured record.

<span id="explanation-dac-2026-research1742"></span>

## StepPRM-RTL: rewarding intermediate RTL steps helps only if the reward predicts executable hardware and improves final synthesis outcomes

RTL is a hardware description of registers, combinational logic, interfaces and clocked behavior. Generating RTL is a sequence of dependent decisions: the model must understand the specification, choose state and data paths, write syntactically valid code, preserve timing and reset behavior, and produce a design that simulates and synthesizes correctly. A plausible explanation or locally reasonable code edit does not establish that the complete hardware behavior is correct.

StepPRM-RTL is described as combining stepwise trajectory modeling, a process-reward model (PRM), retrieval-augmented fine-tuning (RAFT), and Monte Carlo tree search (MCTS). A trajectory contains intermediate rationales and incremental code modifications. The PRM scores those intermediate steps, RAFT uses retrieved or generated training material for fine-tuning, and MCTS explores alternative paths. The proposed benefit is denser feedback than a reward given only after the final RTL is tested. Each component has a separate cost and failure mode.

The process reward must measure progress toward a valid design, not merely text quality or similarity to a canonical solution. Define what an intermediate state contains, what tests are available at that point, how the PRM is trained, how labels are obtained, how reward is calibrated, and how reward hacking is detected. A step can look like a sensible refinement while introducing an incorrect clock enable, reset polarity, width conversion, signedness change, latch, race or interface timing error. Test whether high PRM scores predict later simulation and synthesis success on designs and styles absent from PRM training.

The final correctness gate is independent execution. Compile Verilog and VHDL with stated tools and settings, run directed and randomized simulation, use assertions or formal equivalence where appropriate, and test reset, clock, stall, handshake, parameter, corner-case and invalid-input behavior. Record syntax failures, compile failures, simulation failures, assertion failures, timeouts, synthesis failures and functional mismatches. Reasoning fidelity is not a substitute for executable RTL correctness; a correct final design also needs to preserve the specified interface and cycle-level behavior.

Synthesis quality is a separate outcome. For accepted RTL, synthesize under the same technology library, clock, constraints, effort, target frequency and reset assumptions. Report area, timing, power, logic count, memory inference, fanout, critical paths, constraint violations, synthesis runtime and implementation failures. A model can improve functional pass rate while producing worse area or timing. Conversely, a small RTL text or shorter reasoning trace does not imply better hardware.

MCTS changes the total budget. Each alternative path requires model calls, state storage, code compilation, simulation or a surrogate score. Report tree branching, depth, rollout policy, pruning, duplicate paths, verification calls, parallel resources and whether cached results are reused. Compare final quality at equal wall-clock, token, simulation and hardware budgets. The claimed improvement of more than 10% in functional correctness and reasoning-fidelity metrics needs the exact metric definitions, denominators, uncertainty, task split and cost boundary.

Retrieval and canonical trajectories create leakage risks. If training or retrieval exposes a solution, module name, benchmark family, assertion or near-duplicate design from the test set, a pass rate may measure memorization. Split by design family, specification template, language, interface and source repository. Evaluate both Verilog and VHDL, unseen coding styles, larger designs, multi-module integration and specifications requiring exact cycle behavior. Report generated code length, prompt context, retrieval hits and failures.

The baselines should include standard supervised fine-tuning, outcome-based RTL generation, supervised generation with retrieval but without PRM, PRM without MCTS, MCTS with an outcome-only reward, and a strong non-LLM or human reference where feasible. Hold base model, prompts, design specifications, tools, tests, decoding, compute budget and acceptance gate constant. Ablate stepwise trajectories, PRM, RAFT and MCTS independently. Report whether gains remain after rejecting invalid outputs and after synthesizing only functionally correct designs.

The captured description reports more than 10% improvement over prior methods in functional-correctness and reasoning-fidelity metrics, with ablations supporting the combination of PRM-guided rewards and trajectory exploration. It does not expose pass rates, metric definitions, reward calibration, training cost, synthesis quality, failure cases, tool settings or artifact reproducibility. The evidence supports process-reward-guided RTL generation, not demonstrated executable, synthesizable and PPA-improving hardware generation across languages and design families.

## Compare accepted implementations and their costs

Use the same behavioral specifications and implementation constraints. Record candidate counts, correctness failures, synthesis failures, and final area, timing, and power where those are the target outcomes. Include training and search costs, or state the reuse assumptions under which they are amortized.

Test unfamiliar specifications and larger designs. Distinguish a new generator, an improved synthesis algorithm, and a better implementation of one benchmark. Their shared research problem is efficient selection among many structures, but their conclusions require different evidence about correctness, generality, and final hardware quality.

## Compare the results carefully

First identify the inputs and required output quality. Then identify the limited resource: time, memory, communication, energy, circuit area, or correctness coverage. Ask which part of the method reduces that cost and which new cost it adds. Compare numbers only when the experiments hold these conditions sufficiently similar.

A conference description may explain the proposal while omitting the full experiment. An author preprint link may have been coded from its abstract. The source classification does not by itself establish that every table was read. Missing locations remain visible below.

## Complete captured evidence

These are evidence records, not substitutes for the explanations above. Each record preserves its problem, proposed method, measurements, comparison conditions, and source limits. A populated record does not establish that its mechanism has been fully explained or independently verified.

<span id="paper-dac-2026-research2329"></span>

### Shortcircuit: Alphazero-Driven Generative Circuit Design

DAC 2026 · Record: `dac-2026-research2329`

[Read the step-by-step explanation](#explanation-dac-2026-research2329)

**Updated source-backed reading card**

Reviewed 2026-09-08. Deepens the existing Shortcircuit treatment into a paper-level reading; separates Boolean-graph correctness from technology-mapped PPA, defines AlphaZero search and rollout cost, preserves the 500 eight-input and 31x claims, and makes generalization and baseline fairness explicit.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Traditional logic-synthesis heuristics have plateaued, while direct learning over the large circuit-structure search space is difficult.

**Mechanism / artifact:**

Transformer-based AIG generator with supervised pretraining and AlphaZero search, plus greedy rollout acceleration; graph state/actions, reward, search budget, equivalence check and invalid-candidate handling are unspecified.

**Workload — the work tested:**

500 eight-input truth tables derived from real circuits; train/test split, source-circuit leakage, function difficulty, output count, input-width generalization, circuit-size definition and ABC version/options are unspecified.

**Hardware and manufacturing assumptions:**

Boolean AIG synthesis and later technology mapping; cell library, mapper, timing/area/power constraints, target technology, inference/search hardware, memory and PPA measurement boundary are unspecified.

**Baseline — the comparison method:**

ABC logic-synthesis tool

Prior deep-learning circuit-generation methods

Heuristic/random AIG search

Same truth tables, equivalence criterion, search time/candidate budget, hardware, mapper, library, constraints and preprocessing are unspecified

**Reported measurements:**

Functional correctness is claimed; circuit-size superiority over ABC and 31x greedy-rollout speedup are claimed, but exact size, timing/area/power, equivalence-check cost, training/search cost, mapping result, win/tie/loss distribution and beyond-eight-input generalization are not reported.

**Limits on the conclusion:**

Functional correctness is separate from graph size and from mapped physical PPA. A smaller AIG can map to worse area, delay or power because library, fanout, buffering, wires and optimization passes differ; evaluate the same technology-mapped implementation boundary.

AlphaZero search and greedy rollout have proposal, expansion, evaluation, equivalence-check and postprocessing costs. A 31x rollout speedup needs its reference, quality, budget, hardware and preparation boundary; faster rollout does not prove better end-to-end synthesis.

The source uses 500 eight-input truth tables and omits exact results, timing/area/power tradeoffs, training/search cost, ABC configuration and larger-input generalization. The evidence supports a learned Boolean-graph search direction, not demonstrated scalable physical circuit improvement.

**Source and location**

Evidence tier: Primary captured official DAC description plus existing chapter level shortcircuit discussion; no full paper extraction, reproduced search budget, mapped ppa results or input width diverse validation. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH2329)

DAC 2026 official description; existing chapter-level Shortcircuit discussion; captured Problem, Mechanism / artifact, Workload, Hardware, Baseline, Measurements and Limits fields; no manuscript pages.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** ABC logic-synthesis tool

prior deep-learning circuit-generation methods

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH2329&sess=sess167

**Hardware or process assumptions:** Boolean AIG synthesis from truth tables; target technology mapping, library, optimization objectives, and inference hardware are unspecified.

**Limits:** The description omits exact circuit-size results, timing/area/power tradeoffs, generalization beyond eight inputs, and search/training cost.

Functional correctness does not imply PPA superiority after technology mapping.

Official description only; synthesis and learning claims require paper-level artifact verification.

**Method or artifact:** Transformer-based AIG generator with supervised pretraining and AlphaZero search, plus greedy rollout acceleration.

**Metrics:** Functional correctness guaranteed for generated circuits claimed

Outperforms ABC in circuit size

31x greedy-rollout speedup

**Problem:** Traditional logic-synthesis heuristics have plateaued, while direct learning over the doubly exponential circuit state space is difficult.

**Workload or benchmark:** 500 eight-input truth tables derived from real circuits, compared with ABC; circuit-size definition, timing/power constraints, training/test split, and ABC version are unspecified.

</details>

<span id="paper-dac-2026-research1784"></span>

### Autonomous Evolution of EDA Tools: Multi-Agent Self-Evolved ABC

DAC 2026 · Record: `dac-2026-research1784`

[Read the step-by-step explanation](#explanation-dac-2026-research1784)

**Updated source-backed reading card**

Reviewed 2026-09-08. Deepens the existing self-evolved ABC treatment into a paper-level reading; separates code-evolution correctness from circuit QoR validation, makes benchmark overfitting, patch provenance, cost, regression and maintainability explicit, and preserves the boundary between seeded optimization and autonomous search.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Logic-synthesis heuristics plateau, while manual improvement of a complex monolithic EDA codebase is slow and difficult to scale.

**Mechanism / artifact:**

Multi-agent LLM code-evolution loop with correctness validation and benchmark QoR feedback over the ABC repository; agent roles, prompts, model versions, patch acceptance, seed provenance and toolchain are unspecified.

**Workload — the work tested:**

ABC logic-synthesis codebase and standard benchmark circuits; QoR dimensions, libraries, constraints, iterations, code changes, model versions, development/held-out split and baseline revisions are unspecified.

**Hardware and manufacturing assumptions:**

EDA software repository with synthesis tests and benchmark QoR evaluation; compiler/toolchain, compute/token budget, synthesis hardware, storage, human review, licensing and reproducibility assumptions are unspecified.

**Baseline — the comparison method:**

Unmodified ABC

Human-designed ABC heuristics

Seeded external research optimizations

Conventional human/scripted search

Same repository revision, seed, circuits, libraries, constraints, toolchain, test strength and total search/evaluation budget are unspecified

**Reported measurements:**

Correctness validation, QoR improvement and autonomous repository evolution are claimed qualitatively; no numeric area/delay/power/QoR, regression rate, patch survival, search cost, LLM cost, code-review burden, reproducibility or held-out result is reported.

**Limits on the conclusion:**

A passing benchmark test does not establish repository-wide software correctness, deterministic behavior, maintainability or safety. Validate regressions, failures, memory/runtime behavior, uncommon pass combinations, dependencies, licensing and patch provenance.

Benchmark feedback can overfit the circuits and scoring function used for patch selection. Use sealed circuits, larger/unseen designs, changed constraints and multiple seeds; report wins, ties, regressions, reverts and patch survival separately.

No numeric QoR, regression, search-cost, review or reproducibility results are reported. Seeded human/external optimizations must be separated from autonomous gains; the evidence supports automated EDA-software search, not demonstrated generally improved or maintainable synthesis tooling.

**Source and location**

Evidence tier: Primary captured official DAC description plus existing chapter level self evolved abc discussion; no full paper extraction, patch history, held out regression campaign or independent repository reproduction. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH1784)

DAC 2026 official description; existing chapter-level self-evolved ABC discussion; captured Problem, Mechanism / artifact, Workload, Hardware, Baseline, Measurements and Limits fields; no manuscript pages.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** human-designed ABC heuristics

seeded external research optimizations

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH1784&sess=sess168

**Hardware or process assumptions:** EDA software repository with synthesis correctness tests and benchmark-based QoR evaluation; target libraries, compute budget, and human review are unspecified.

**Limits:** The description omits numeric QoR, regression rate, search cost, code-review burden, and reproducibility details.

Autonomous code changes may overfit benchmark circuits or introduce latent correctness and maintainability risks.

Official description only; software-evolution claims require artifact and independent benchmark review.

**Method or artifact:** Multi-agent LLM code-evolution loop with correctness validation and benchmark QoR feedback over the ABC repository.

**Metrics:** Correctness validation claimed

QoR improvements beyond seeded heuristics claimed qualitatively

Autonomous repository evolution demonstrated

**Problem:** Logic-synthesis heuristics plateau, while manual improvement of a complex monolithic EDA codebase is slow and difficult to scale.

**Workload or benchmark:** ABC logic-synthesis codebase and standard benchmark circuits; QoR metrics, number of iterations, code changes, model versions, and baseline tool results are unspecified.

</details>

<span id="paper-dac-2026-research1742"></span>

### StepPRM-RTL: Stepwise Process-Reward Guided LLM Fine-Tuning for Enhanced RTL Synthesis

DAC 2026 · Record: `dac-2026-research1742`

[Read the step-by-step explanation](#explanation-dac-2026-research1742)

**Updated source-backed reading card**

Reviewed 2026-09-08. Deepens the existing StepPRM-RTL treatment into a paper-level reading; separates intermediate process rewards from executable RTL correctness and synthesis quality, makes PRM calibration, RAFT/MCTS cost, leakage, language generalization and PPA validation explicit, and preserves the bounded more-than-10% claim.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Long-horizon RTL generation requires multi-step reasoning and strict functional correctness that outcome-only training does not reliably provide.

**Mechanism / artifact:**

Stepwise reasoning trajectories, process-reward model, RAFT fine-tuning and MCTS path exploration for RTL synthesis; intermediate-state definition, reward labels/calibration, retrieval boundary and search budget are unspecified.

**Workload — the work tested:**

Benchmark Verilog and VHDL RTL datasets; design families, interfaces, language split, correctness tests, retrieval corpus, base model, synthesis targets, task split and comparative metric definitions are unspecified.

**Hardware and manufacturing assumptions:**

LLM-generated RTL compiled, simulated and functionally evaluated; HDL simulators/synthesizers, libraries, clock constraints, target technology, compute/token budget, MCTS verification cost and PPA boundary are unspecified.

**Baseline — the comparison method:**

Standard supervised fine-tuning

Outcome-based RTL generation

RAFT/retrieval without PRM

PRM without MCTS and MCTS with outcome-only reward

Same base model, prompts/specifications, tools, tests, decoding, design split, acceptance gate and total compute/verification budget are unspecified

**Reported measurements:**

Improved functional correctness and reasoning fidelity are claimed; the source reports more than 10% improvement over prior methods, but no pass rate, metric definition, reward calibration, synthesis area/timing/power, failure case, training/search cost or reproducibility result is reported.

**Limits on the conclusion:**

A process reward can score plausible intermediate text without predicting executable RTL. Independent compilation, simulation, assertions/formal checks, reset/clock/handshake corner cases and synthesis failure rates are required for final correctness.

RAFT retrieval and canonical trajectories can leak solutions or benchmark structure. Split by design family, interface, language, repository and near-duplicate specification; test unseen Verilog/VHDL styles and report retrieval hits and failures.

No pass rates, synthesis quality, reward calibration, training cost or failure cases are reported. The evidence supports process-reward-guided RTL generation, not demonstrated executable, synthesizable and PPA-improving hardware generation across languages and design families.

**Source and location**

Evidence tier: Primary captured official DAC description plus existing chapter level stepprm RTL discussion; no full paper extraction, reproduced prm calibration, retrieval leakage audit or synthesis/ppa validation. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH1742)

DAC 2026 official description; existing chapter-level StepPRM-RTL discussion; captured Problem, Mechanism / artifact, Workload, Hardware, Baseline, Measurements and Limits fields; no manuscript pages.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** standard supervised fine-tuning

outcome-based RTL generation

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH1742&sess=sess166

**Hardware or process assumptions:** LLM-generated RTL compiled and functionally evaluated; HDL tools, synthesis targets, prompt context, and compute budget are unspecified.

**Limits:** The description omits pass rates, synthesis quality, reward calibration, training cost, and failure cases.

Reasoning traces do not guarantee executable or synthesizable RTL correctness.

Official description only; LLM-EDA claims require artifact and independent test verification.

**Method or artifact:** Stepwise reasoning trajectories, process-reward model, RAFT fine-tuning, and MCTS path exploration for RTL synthesis.

**Metrics:** Improved functional correctness and reasoning fidelity claimed qualitatively

**Problem:** Long-horizon RTL generation requires multi-step reasoning and strict functional correctness that outcome-only LLM training does not reliably provide.

**Workload or benchmark:** Benchmark Verilog and VHDL datasets; correctness tests, design distribution, model base, and comparative metrics are unspecified.

</details>

<span id="paper-dac-2026-research2476"></span>

### Flowplace: Flow Matching for Chip Placement

DAC 2026 · Record: `dac-2026-research2476`

[Read the step-by-step explanation](#explanation-dac-2026-research2476)

**Updated source-backed reading card**

Reviewed 2026-09-08. Deepens the existing FlowPlace treatment into a paper-level reading; separates generated coordinates from legal/routable placement, defines hard constraints, PPA and legalization cost, preserves the OpenROAD/ICCAD 2015 and 10–50x claims, and makes distribution shift and end-to-end fairness explicit.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Conventional placement search is expensive and can struggle with large, multimodal placement spaces; generative methods can be slow or produce overlaps.

**Mechanism / artifact:**

Flow-matching generative model for chip placement with mask-guided synthetic data, flexible prior injection and hard-constraint sampling; representation, constraint enforcement, repair/legalization and downstream flow are unspecified.

**Workload — the work tested:**

OpenROAD and ICCAD 2015 chip-placement benchmarks; netlists, macros, utilization, constraints, training corpus, sampling steps, legalization, technology, subset, seeds and distribution-shift tests are unspecified.

**Hardware and manufacturing assumptions:**

ASIC placement flow with learned proposals and downstream physical-design evaluation; hardware, memory, OpenROAD version, libraries, routing/timing settings, process node and end-to-end runtime boundary are unspecified.

**Baseline — the comparison method:**

Analytic placement

Reinforcement-learning placement

Prior diffusion/generative placement

Same netlists, technology/library, macros, utilization, constraints, downstream legalization/routing/timing flow, seeds and best-of-N/evaluation boundary are unspecified

**Reported measurements:**

Placement quality and search efficiency are claimed; the source reports better PPA metrics, 10–50x faster sampling efficiency and zero overlaps, but no wirelength, congestion, timing, power/area table, end-to-end runtime, legalization cost, per-design legality or generalization result is reported.

**Limits on the conclusion:**

A generated coordinate set is not a valid placement until non-overlap, site, boundary, orientation, density, macro, keepout and routing constraints are independently checked. If legalization repairs samples, report its cost, movement, failure rate and PPA effect.

PPA is a vector: wirelength, congestion, timing, power, area, routing completion and runtime can trade off. Neural sampling speed is not end-to-end placement speed when preprocessing, model loading, candidate generation, legalization and downstream evaluation are excluded.

The source reports OpenROAD/ICCAD 2015 and 10–50x/zero-overlap claims but omits exact conditions, wirelength, congestion, timing, runtime boundary, distribution shift and per-design legality. The evidence supports faster constrained placement proposals, not demonstrated robust end-to-end PPA improvement.

**Source and location**

Evidence tier: Primary captured official DAC description plus existing chapter level flowplace discussion; no full paper extraction, reproduced constraint sampler, legalization trace or distribution shift validation. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH2476)

DAC 2026 official description; existing chapter-level FlowPlace discussion; captured Problem, Mechanism / artifact, Workload, Hardware, Baseline, Measurements and Limits fields; no manuscript pages.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** analytic placement

reinforcement-learning or generative placement methods

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH2476&sess=sess177

**Hardware or process assumptions:** ASIC placement flow with learned placement proposals and downstream physical-design evaluation; technology and congestion assumptions are unspecified.

**Limits:** The description omits wirelength, congestion, timing, runtime, generalization, and legality rates.

Generative models may be sensitive to training-distribution shift.

Official description only; placement claims require PPA and robustness evidence.

**Method or artifact:** Flow-matching generative model for proposing or optimizing chip placements.

**Metrics:** Placement quality and search efficiency are claimed qualitatively

**Problem:** Conventional placement search is expensive and can struggle with large, multimodal placement spaces.

**Workload or benchmark:** Chip placement instances; netlists, constraints, training corpus, legalization, and baselines are unspecified.

</details>

<span id="paper-dac-2026-research179"></span>

### LLMVA: LLMs Empowered Verilog-A Iterative for MRAM Design Technology Co-Optimization

DAC 2026 · Record: `dac-2026-research179`

[Read the step-by-step explanation](#explanation-dac-2026-research179)

**Updated source-backed reading card**

Reviewed 2026-09-08. Deepens the existing LLMVA treatment into a paper-level reading; separates generated Verilog-A from physical calibration, defines device/circuit/DTCO validation, preserves the 9.2%, 4-Mb/28-nm tape-out and 50% claims, and makes PPA, convergence and human-cost boundaries explicit.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

MRAM co-optimization requires repeated device and circuit modeling across expensive design iterations.

**Mechanism / artifact:**

LLM-assisted iterative Verilog-A generation/modeling for STT-MTJ MRAM co-design; observation/feedback loop, parameter extraction, simulator objective, human review, calibration and generated-equation constraints are unspecified.

**Workload — the work tested:**

STT-MTJ devices and MRAM circuits including a reported 4-Mb 28-nm macro; device lots, measurements, PDK, corners, temperatures/voltages, sample count, circuit metrics, convergence and independent validation are unspecified.

**Hardware and manufacturing assumptions:**

MRAM technology with Verilog-A device models, circuit simulation and reported tape-out; foundry/process, PDK, bit-cell/periphery, parasitics, test equipment, measurement conditions, compute and human-cost boundary are unspecified.

**Baseline — the comparison method:**

Manual Verilog-A modeling

Fixed technology/circuit optimization

Existing calibrated device-modeling flow

LLM-assisted process without iterative measurement feedback

Same device data, PDK, simulator, corners, design target, quality threshold, human review and end-to-end time boundary are unspecified

**Reported measurements:**

MRAM co-design efficiency is claimed; the source reports front-test/post-test MTJ deviation not exceeding 9.2%, a 4-Mb 28-nm macro tape-out and approximately 50% lower designer/time cost, but no error definition/distribution, convergence, PPA, device sample, calibration, fabricated-macro validation or cost accounting is reported.

**Limits on the conclusion:**

Verilog-A code that compiles or matches selected curves can still encode physically invalid equations and produce wrong circuit decisions. Validate held-out device measurements across voltage, temperature, process, variation and operating modes, then compare circuit behavior with a trusted calibrated model.

Front-test/post-test deviation needs a defined quantity, samples, conditions and reference; it is not automatically independent model accuracy. Tape-out is a design milestone, not proof of fabricated performance, yield, timing or energy.

No model error definition, convergence, PPA, device metrics or human-effort accounting is reported. The evidence supports LLM-assisted device modeling, not demonstrated calibrated model accuracy or general MRAM co-design efficiency.

**Source and location**

Evidence tier: Primary captured official DAC description plus existing chapter level llmva discussion; no full paper extraction, reproduced calibration data, device condition matrix or fabricated macro validation. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH179)

DAC 2026 official description; existing chapter-level LLMVA discussion; captured Problem, Mechanism / artifact, Workload, Hardware, Baseline, Measurements and Limits fields; no manuscript pages.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** manual Verilog-A modeling

fixed technology/circuit optimization

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH179

**Hardware or process assumptions:** MRAM technology with Verilog-A models and circuit simulation; device parameters and calibration are unspecified.

**Limits:** No model error, convergence, PPA, device metrics, or human effort results are reported.

Generated behavioral models can encode physically invalid assumptions.

Official description only; calibrated device validation is required.

**Method or artifact:** LLM-assisted iterative Verilog-A generation/modeling for MRAM co-design.

**Metrics:** MRAM co-design efficiency is claimed qualitatively

**Problem:** MRAM co-optimization requires repeated device and circuit modeling across expensive design iterations.

**Workload or benchmark:** MRAM devices and circuits; models, PDK, simulation, and baselines are unspecified.

</details>

<span id="paper-dac-2026-research2646"></span>

### TOPCELL: Topology Optimization of Standard Cell via LLMs

DAC 2026 · Record: `dac-2026-research2646`

[Read the step-by-step explanation](#explanation-dac-2026-research2646)

**Updated source-backed reading card**

Reviewed 2026-09-08. Deepens the existing TOPCELL treatment into a paper-level reading; separates generated topology from signoff quality, defines logical/physical constraints, GRPO reward and extraction/routing validation, preserves the 2-nm, 7-nm and 85.91x claims, and makes PPA, repair and cross-technology boundaries explicit.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Standard-cell transistor topology has a combinatorial search space and must balance logical correctness, electrical behavior, physical design and routability.

**Mechanism / artifact:**

LLM-guided standard-cell topology optimization fine-tuned with GRPO; topology representation, logical/spatial constraints, reward terms, candidate repair, extraction, routing and signoff path are unspecified.

**Workload — the work tested:**

Industrial 2-nm technology-flow experiments and a 7-nm library-generation task; cell functions, drive strengths, libraries, loads, corners, topology count, training/test split, zero-shot boundary and exhaustive-solver conditions are unspecified.

**Hardware and manufacturing assumptions:**

ASIC standard-cell design and extraction/routing flow; PDK, process, cell height/track structure, transistor model, simulators, routers, signoff tools, compute and repair assumptions are unspecified.

**Baseline — the comparison method:**

Manual topology design

Exhaustive/search-based cell optimization

Foundation LLM without GRPO

Same function, cell structure, PDK, process, loads, corners, downstream extraction/routing/characterization/signoff flow and repair budget are unspecified

**Reported measurements:**

Cell topology quality and search efficiency are claimed; the source reports matching exhaustive-solver layout quality and 85.91x speedup in a 7-nm task, with 2-nm industrial-flow evaluation, but no area, timing, power, routability, yield, signoff, repair rate or per-cell result is reported.

**Limits on the conclusion:**

A generated topology must pass logical equivalence, electrical simulation, design-rule checking, extraction, routing, pin access and signoff. Zero geometric overlap or a plausible graph does not establish valid diffusion, wells, contacts, parasitics, timing or power.

PPA and routability trade off. The reward must expose GRPO groups, constraints, penalties, sampling, repair and signoff reference; speed must include generation, checking, repair, extraction and routing rather than only proposal time.

The source reports 2-nm/7-nm and 85.91x claims but omits exact PPA, routability, signoff, reward calibration, repair, yield and cross-technology conditions. The evidence supports constrained topology generation, not demonstrated signoff-quality standard-cell improvement across technologies.

**Source and location**

Evidence tier: Primary captured official DAC description plus existing chapter level topcell discussion; no full paper extraction, reproduced grpo reward, extraction/routing trace or cross technology signoff validation. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH2646)

DAC 2026 official description; existing chapter-level TOPCELL discussion; captured Problem, Mechanism / artifact, Workload, Hardware, Baseline, Measurements and Limits fields; no manuscript pages.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** manual topology design

search-based cell optimization

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH2646

**Hardware or process assumptions:** ASIC standard-cell design and extraction flow; technology and signoff assumptions are unspecified.

**Limits:** No area, timing, power, routability, yield, or search results are reported.

LLM proposals may violate design rules or electrical constraints.

Official description only; synthesis and extraction validation is required.

**Method or artifact:** LLM-guided standard-cell topology optimization.

**Metrics:** Cell topology quality and search efficiency are claimed qualitatively

**Problem:** Standard-cell topology design has a combinatorial space and requires balancing electrical and physical objectives.

**Workload or benchmark:** Standard-cell topologies; process, constraints, evaluation, and baselines are unspecified.

</details>

<span id="paper-dac-2026-research2793"></span>

### Circuitdiff: Bridging Netlist Knowledge with RTL Based on Graph Denoising Diffusion

DAC 2026 · Record: `dac-2026-research2793`

[Read the step-by-step explanation](#explanation-dac-2026-research2793)

**Updated source-backed reading card**

Reviewed 2026-09-08. Deepens the existing CircuitDiff treatment into a paper-level reading; separates RTL-conditioned representation learning from RTL-to-netlist synthesis, defines graph diffusion and early-metric validation, preserves the qualitative superior-performance and efficiency claims, and makes split leakage, PPA and code/data availability boundaries explicit.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Early circuit-metric prediction needs physical information that is usually available only after netlist or downstream analysis, while full physical evaluation is computationally expensive.

**Mechanism / artifact:**

CircuitDiff uses RTL graphs as conditions for pretraining a netlist graph denoising diffusion model, then uses learnable queries and cross-attention during fine-tuning for early circuit-metric prediction; graph representation, diffusion target, query training, metric labels and synthesis/tool boundary are unspecified.

**Workload — the work tested:**

RTL/netlist design pairs and early-stage circuit metrics; design families, RTL language, synthesis flow, metric list, dataset size, train/test split, near-duplicate controls, scaling and distribution-shift tests are unspecified.

**Hardware and manufacturing assumptions:**

RTL-to-netlist graph learning and circuit-metric prediction flow; synthesis tools, libraries, process technology, physical-analysis labels, simulator, compute budget and whether measurements are post-layout or proxy metrics are unspecified.

**Baseline — the comparison method:**

State-of-the-art early circuit-metric prediction models

Sequence-only RTL model

Graph encoder without diffusion pretraining

Same RTL/netlist pairs, synthesis and label-generation flow, design split, metric definitions, decoding/evaluation budget and leakage controls are unspecified

**Reported measurements:**

The source claims superior early-stage circuit-metric prediction and computational efficiency relative to state-of-the-art models, supporting a left-shifted design-evaluation workflow, but reports no metric names, error values, runtime, design count, synthesis conditions, PPA table or held-out generalization result.

**Limits on the conclusion:**

A denoised netlist graph or aligned representation is not a synthesized, logically equivalent or physically implemented circuit. Validate graph validity, RTL/netlist equivalence, synthesis success and downstream timing, area, power and congestion with independent tools.

Early metric prediction is only useful if labels, split boundaries and leakage controls are explicit. Separate designs by family, RTL structure, netlist lineage, IP and near-duplicate templates; compare against a simple graph and sequence baseline under the same data and compute budget.

The official description provides qualitative superiority and efficiency claims but no error definition, metric list, runtime boundary, dataset conditions or PPA result. The evidence supports RTL-conditioned netlist representation learning for early prediction, not demonstrated RTL-to-netlist synthesis or robust physical-design improvement.

**Source and location**

Evidence tier: Primary captured official DAC description plus existing chapter level circuitdiff discussion; no full paper extraction, reproduced graph diffusion training, leakage audit or synthesis/ppa validation. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH2793)

DAC 2026 official description; existing chapter-level CircuitDiff discussion; captured Problem, Mechanism / artifact, Workload, Hardware, Baseline, Measurements and Limits fields; no manuscript pages or inspected code/data release.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** sequence-only RTL model

graph encoder without diffusion

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH2793

**Hardware or process assumptions:** RTL synthesis and graph-learning flow; technology and representation assumptions are unspecified.

**Limits:** No reconstruction, synthesis quality, transfer, runtime, or design results are reported.

Diffusion outputs may be syntactically valid but semantically wrong.

Official description only; equivalence and synthesis validation is required.

**Method or artifact:** Graph denoising diffusion model linking RTL and netlist knowledge.

**Metrics:** RTL-netlist alignment is claimed qualitatively

**Problem:** RTL and netlist representations contain complementary information that is difficult to align for design understanding or generation.

**Workload or benchmark:** RTL/netlist pairs; tasks, designs, synthesis tools, and baselines are unspecified.

</details>

## What remains to establish

Resolve unspecified workloads, comparison methods, resource budgets, and source locations before generalizing a reported gain. Multiple papers in this selected sample permit comparison of mechanisms, but do not by themselves establish recurrence across years or a long-term trend.

[All subthemes](../expanded-taxonomy-v1.md) · [Research directions](../directions/README.md)
