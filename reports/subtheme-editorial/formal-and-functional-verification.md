## Begin with what the design is supposed to do

A functional requirement describes intended behavior. For a stateful circuit, that behavior includes how stored values change across clock cycles. It also includes how outputs respond to sequences of inputs. Verification needs a representation of that requirement that can be compared with the implementation.

Functional simulation checks selected executions. Formal verification reasons about a specified set of behaviors mathematically. The methods can support one another. A simulation failure can identify a concrete problem. A formal property can address cases that would be difficult to enumerate. The scope of each check must remain visible.

## A specification can itself be wrong or incomplete

Correctness depends on the expected behavior. If a requirement omits an exceptional input or permits an unintended state transition, an implementation may satisfy that requirement. It may still fail the real use case. Automating the conversion of prose requirements into checks makes the translation faster, but does not eliminate this risk.

The evaluation therefore needs to examine both the generated checks and the circuit's response. A check that always passes is not useful if it never expresses a condition that could fail. A check that rejects valid behavior also needs correction before its results can support a design decision.

PRO-V-R1, the RISC-V cryptography invariant paper, SafeGen and STELLAR now have individual paper-level explanations in this chapter. So do Seeing the Unseen, ChatSVA, and Beyond Flat Netlist. These explanations are source-backed reading coverage, not independent scientific acceptance or a completed taxonomy reassignment.

## PRO-V-R1 connects generation to simulation feedback

The captured PRO-V-R1 record describes an automated programming system for register-transfer-level verification. It is trained using trajectories that include simulation results and later tool feedback. Register-transfer level describes stored circuit state and the operations that update it. [Recorded evidence](../observed-subthemes/formal-and-functional-verification.md#paper-dac-2026-research142)

Feedback can guide the next proposed test or program change. The central question is whether the feedback reflects the intended requirement and exposes failures on unfamiliar designs. A simulation-valid sequence used in training does not establish general coverage. The record leaves the design population, fault categories, training details, and statistical uncertainty unresolved.

<span id="explanation-dac-2026-research142"></span>

## PRO-V-R1: how a verification agent turns code generation into an executable check

### Verification needs an oracle and stimuli

An RTL design under test produces outputs from input signals and stored state. To check it, a verification flow needs at least two things. One is stimuli that exercise behavior. The other is an oracle that says what the outputs should be. A testbench can provide both. Writing one is difficult because values must have the right widths, bit ordering, cycle alignment and reset behavior.

PRO-V-R1 treats verification as a program-generation problem. Its agent does not ask an LLM to emit a large HDL testbench directly. It asks the model to generate executable Python artifacts that create input vectors and a Python functional reference model. The simulator runs the RTL with the same inputs, and the flow compares the RTL outputs with the reference outputs. This gives the generated artifacts an executable check. The check is only as good as the reference model and the tested input set.

### The system separates three responsibilities

The PRO-V system has a Testcase Generator, an FRM Generator and a Judge. The Testcase Generator reasons about scenarios and writes a short Python program that constructs exact input sequences. This replaces asking the LLM to type long binary strings. The FRM Generator writes a Python functional reference model and uses it to compute expected outputs for those cases. The Judge samples candidate artifacts, uses majority agreement to select a candidate, and validates it. It can edit individual testbench entries before final simulation.

This separation reduces one source of error. The model can use ordinary Python operations to calculate wide values and repeated sequences. The tool executes those operations. It does not remove semantic translation risk. Verilog bit numbering and Python indexing differ. A signed, packed or sequential signal can be represented incorrectly even when the Python code runs without an exception.

The final simulation invokes Verilator on the RTL and compares its outputs with the JSON testbench produced by the agents. A successful run establishes agreement between that RTL and that generated reference on those test cases. It does not prove the RTL's complete behavior. The reference may encode the same misunderstanding as the RTL, and the tests may omit the failing sequence.

### The training data is filtered by executable agreement

For supervised fine-tuning, the authors use a teacher model to generate testcase and functional-reference trajectories from existing RTL design datasets. A trajectory is retained only when the generated input program and reference model compile. The reference outputs must also match the golden RTL outputs for all generated cases. This creates examples in which the tools can execute the proposed verification workflow.

The filter is useful but has a precise boundary. It verifies the reference model against a golden implementation, not against an independently reviewed specification. If the golden RTL is wrong, agreement can preserve that error. The same holds if the sampled cases do not exercise a behavior. The filter is therefore a tractability and consistency condition for training. It is not a proof that the reference model captures the design's intended semantics.

### Reinforcement learning assigns rewards to separate agents

After supervised fine-tuning, PRO-V-R1 uses Group Relative Policy Optimization with rewards derived from the verification environment. The Testcase Generator receives a functional reward when the generated harness is syntactically valid, compiles and simulates. The FRM Generator receives the stronger reward only when all test cases pass the RTL/reference comparison. Both also receive a format reward for syntactically correct tool calls.

Separating rewards matters because the two agents control different failure points. A perfect input generator cannot make an incorrect reference model pass. A correct reference model is not useful if its test harness cannot run. The method normalizes rewards by agent and computes group-relative advantages, then optimizes the two sub-trajectories with a shared GRPO objective. This is a credit-assignment design: it changes which generated actions are reinforced, not the underlying definition of correctness.

### The evaluation has three distinct levels

The paper evaluates VerilogEval-v2 and RTLLM v2.0. Eval0 measures whether a generated testbench compiles and runs without simulation errors. Eval1 measures whether it compiles and passes when applied to the golden RTL. Eval2 measures robustness. The authors generate ten RTL mutants per problem. They count a testbench as robust at level 80, 90 or 100. That requires its pass/fail verdict to agree with the reference testbench on at least that fraction of mutants.

These levels answer different questions. Eval0 is viability, not functional correctness. Eval1 checks agreement with a known-good implementation, not bug detection. Eval2 asks whether the testbench distinguishes mutated implementations. This is closer to fault detection but depends on the mutation generator and the reference testbench. A testbench can score high on Eval1 by exercising only easy behavior and still score low on Eval2.

PRO-V-R1-8B with the PRO-V system reports VerilogEval-v2 Eval0/Eval1/Eval2-80/90/100 of 94.8/57.7/44.2/37.8/34.0. The same row reports RTLLM v2.0 values of 78.0/28.0/18.0/14.0/6.0. The paper compares the 57.7% functional result and 34.0% full-mutant result with CorrectBench's 25.6% and 21.8%. It also compares them with GPT-4o's 43.0% and 27.6% on the same table.

The ablation separates system design from post-training. Qwen3-8B with only the PRO-V system reports 64.7 Eval0, 39.1 Eval1 and 28.2 Eval2-100. Adding SFT raises these to 93.6, 50.6 and 27.6; adding RL produces 94.9, 57.7 and 34.0 in the ablation table. The source table and prose use slightly different Eval0 entries for the final row. The exact row should be preserved with its table locator. It should not be silently collapsed into one number.

### Speed is a workflow measurement

The paper reports mean latency of 91.2 seconds per task and median 40.5 seconds for PRO-V-R1. For the CorrectBench Qwen3-8B baseline it reports 805.4 seconds mean and 588.3 seconds median. It describes this as an 8.8× mean-latency speedup. The comparison includes different agent workflows. PRO-V samples five Python programs in parallel and usually succeeds within one or two self-consistency iterations. CorrectBench uses a more expensive self-check process with multiple RTL implementations. The timing is therefore a comparison of complete reported workflows, not the generation latency of equal model calls.

### Limits that control the conclusion

The benchmarks use generated mutants, not a complete population of naturally occurring RTL defects. Mutation operators determine which faults Eval2 can detect. The reference testbench used to judge mutant outcomes also determines the target verdict. A high mutant agreement score is evidence about the selected fault model and testbench protocol. It is not a guarantee of coverage of protocol, reset, timing, arithmetic-width, security or integration defects.

The Python FRM can be a useful executable oracle, but its agreement with the golden RTL can be circular. The method also relies on Verilator semantics, simulator settings, correct reset modeling and exact cycle alignment. Privacy and openness claims depend on which teacher APIs, training data, RTL repositories and released model artifacts are actually available. The reported task latency excludes the engineering effort needed to define the specification and inspect a reference model. It also excludes the effort to diagnose a mismatch and confirm a repair.

### What this paper establishes

PRO-V-R1 provides a coherent open agentic workflow. It generates executable stimuli and a Python reference model. It validates candidates with tools. It trains on trajectories that pass that loop. It uses structured simulation rewards to refine the agent. Its VerilogEval-v2 results support a narrower claim. Under the paper's protocol, the trained 8B agent improved golden-design pass rate and mutation-based robustness relative to the listed baselines. It also reduced the reported end-to-end latency.

It does not establish complete functional correctness or universal fault detection. It also does not establish independence from the golden RTL/reference model. It does not establish safety of a generated testbench for an unseen design. Deployment still requires specification review, independent oracle construction, and coverage analysis. It also requires real-fault validation. It further requires confirmation that the testbench detects failures not represented by the mutation set.

**Primary sources read:** [PRO-V-R1 arXiv version 4](https://arxiv.org/abs/2506.12200), Sections 1–5 and Tables 1–3. They include the agent roles, verified trajectory filter, GRPO rewards, benchmark definitions, ablations and latency comparison. The [public PRO-V repository](https://github.com/stable-lab/Pro-V) was also a primary source. The repository was inspected but the training and benchmark evaluation were not executed here.

<span id="explanation-dac-2026-research1378"></span>

## RISC-V cryptography invariants: how modular proofs make a large sequential check converge

### The property compares two implementations over time

The target is not only a combinational arithmetic function. Marian is an open-source processor implementation of the RISC-V vector cryptography extensions. Its crypto unit has state, pipelines, counters and handshakes. The reference is the official C++ Spike simulator. The main property is an instruction-level sequential equivalence statement. When both models receive the same inputs, Marian signals that the computation is complete. At that point, Marian's crypto-unit output must equal Spike's output.

This property quantifies over sequences of clocked behavior. A proof must account for the state that can be reached and the cycle at which completion is asserted. It must account for the operands and control signals that select the operation. It must also account for the mapping between the C++ reference values and RTL signals. A proof that reaches only a fixed number of cycles is bounded. An unbounded proof reasons about all allowed lengths under the model and assumptions.

### Why wide cryptography datapaths create a proof problem

Cryptographic vector instructions operate on wide values and often require several stages of control and computation. The formal engine must reason about data bits, control state and temporal sequencing together. The number of possible internal states can make a direct proof stall. This can happen even when the design is functionally simple at the instruction boundary.

When the proof stalls, adding arbitrary assumptions can make the problem appear smaller while excluding legal behavior. The paper's strategy instead has two parts. Modularization divides the equivalence obligation into units that preserve a meaningful interface. Invariants constrain reachable internal states with properties that can themselves be proved. Both steps need a sound connection back to the original whole-design property.

### Modularization changes the proof boundary

The authors first split Marian's pipeline into stages and then verify execution units per instruction. This exposes smaller proof obligations. A stage or execution unit can be checked against the corresponding portion of the reference. The check uses explicit input and handshake conditions. Modularization by itself is reported to enable unbounded proofs for Marian. It is also reported to provide a 1.28× speedup when the execution stage is divided per instruction.

The benefit is not simply that smaller files are easier for a solver. A modular proof is valid only if the assumptions at the module boundary describe every behavior that can occur. This must hold when the unit is connected to the rest of the design. If an assumption omits a legal handshake sequence, the sub-proof may pass while the integrated property remains unproved. The paper's use of the Spike model and completion condition gives the reader a concrete semantic boundary. The full assumption contracts and proof scripts are still needed for independent checking.

### Invariants constrain reachable state without changing the intended result

An invariant is a statement that is true in the initial state and remains true after every allowed transition. Examples include a counter staying within its legal range and a relationship between counters. They also include a handshake signal being consistent with an in-progress operation. They include a finite-state controller remaining in a valid state. Once an invariant is proved, it can be used as an assumption in the proof of the main property. It removes states that the design cannot reach.

The paper defines seven generic categories for finding such candidates. They are regular data, datapath control, pipeline, finite-state machine, counter, internal control and handshake. It automatically generates verification scripts for combinations of invariant groups and measures their effect on proof speed and proof bounds. This makes invariant selection an experiment rather than a claim that every plausible assertion helps.

The method has an important negative result: an invariant can slow the main proof. Proving and using an extra property adds work. A weak or poorly placed invariant can increase the solver's representation or provide little pruning. The selection procedure therefore needs to retain proof failures, timeouts and regressions instead of only reporting the fastest combination.

### What the evaluation reports

The authors manually identify 38 candidate invariants for Marian. Counter and handshake invariants have the largest reported effect. Applying effective invariants gives a further 3× speedup for modularized execution-unit proofs. The largest per-instruction speedup is reported as 6.25× for the Shang-Mi 4 instructions. Combining modularization and effective invariants yields a reported 2.7× total proof speedup for Marian. The conference card records this as an additional 174% speedup. The detailed author page gives the 3× and 2.7× figures. They should not be silently conflated.

The method is tested on VCRYPTU, a custom implementation of the SHA-256 RISC-V vector cryptography sub-extension with a different microarchitecture. VCRYPTU is not pipelined and places a crypto unit inside each vector lane. The author page reports that the proof stalls after one hour without invariants. It also stalls with most invariant groups. Counter invariants allow an unbounded proof in 43 seconds. This is useful evidence that the selected invariant category can matter more than simply adding many assertions. It is still one custom design and one verification setup.

### A proof failure can expose a specification failure

During the SM4 verification, the equivalence property failed because Marian followed one endianness interpretation while Spike used another. The initial symptom could have been treated as an RTL or simulator defect. The maintainers concluded that the ratified RISC-V specification did not define the SM4 vector-instruction endianness clearly. The specification is being updated.

This case separates implementation correctness from reference agreement. A counterexample says that the two modeled implementations differ. It does not by itself say which one violates the intended standard. The formal flow exposed a disagreement that required specification review. Correcting the proof by swapping Jasper assignments can measure the isolated endianness effect. This can support a diagnostic comparison. It does not erase the original specification ambiguity.

### What this paper establishes and what remains conditional

The paper provides a concrete verification methodology for large sequential crypto hardware. It defines the reference-equivalence property and modularizes the design. It classifies invariant candidates and evaluates combinations by proof behavior. It reuses effective invariants in the main proof. The reported Marian and VCRYPTU results support a narrower claim. Modularization and selected counter/handshake invariants made the stated proofs converge faster under the reported Jasper C2RTL setup.

They do not establish that every invariant preserves the original proof obligation. They do not establish that the proof assumptions cover all hardware environments. They do not establish that the specification is fully resolved after the SM4 finding. They do not establish that the speedup transfers to other crypto units and formal engines. The proof artifacts, exact property counts, solver settings, timeouts, assumption contracts and independent reproduction remain necessary for a security-level conclusion.

**Primary sources read:** [ETH Zurich author/project page](https://comsec.ethz.ch/research/hardware-design-security/leveraging-invariants-for-scalable-verification-of-risc-v-cryptography-extensions/). It supplies the detailed mechanism, invariant categories, Marian/VCRYPTU results and SM4 specification finding. The [DAC 2026 official description](https://63dac.conference-program.com/presentation/?id=RESEARCH1378&sess=sess163) and the [Marian public repository](https://github.com/soc-hub-fi/Marian) were also primary sources. The repository and project page were inspected; Jasper proof execution was not reproduced here.

<span id="explanation-dac-2026-research1945"></span>

## SafeGen: how specification-linked assertions turn faults into graded safety evidence

### Fault propagation is not the same as safety criticality

A fault can change an internal signal or propagate to a module output. It can alter a digital control value, or cause a system-level safety violation. These are different events. Structural fault simulation often labels a fault unsafe when its effect reaches an observable output. An output change may be masked by the control loop. It may also not cause a dangerous physical response. Conversely, a fault that looks local can alter a control decision that matters to the system.

SafeGen asks for a more semantic classification. It links a gate-level injected fault to RTL behavior. It identifies which formal safety or functional assertions the faulty design violates. It maps those assertions to extracted specifications. It combines the importance of the affected specifications into a fault-criticality score. The goal is not to maximize the number of faults detected. It is to distinguish faults that matter to the stated system functions and safety requirements. These are separated from faults that merely produce a structural difference.

### The evidence chain has four separate links

The method relies on four links that must each be correct:

1. Documents must be converted into requirements that actually describe system behavior and safety intent.
2. Requirements must be connected to RTL signals and temporal behavior so that the generated assertion checks the intended condition.
3. A gate-level fault must be represented at RTL without changing unrelated behavior or losing the fault's activation conditions.
4. A violated assertion must map back to the affected requirement with a justified importance score.

A failure in any link changes the meaning of the final criticality score. A perfectly proven assertion about the wrong requirement does not support a safety conclusion. A correct requirement mapped to the wrong RTL signal misattributes the fault. A correct mapping evaluated only on open-loop stimuli can overestimate or miss the closed-loop system consequence.

### HyperKG represents cross-document safety context

SafeGen constructs a document-level Hyper Knowledge Graph from FMEDA guidelines, safety documents and design documents. A normal graph edge connects two entities. A hyperedge can connect several entities. It can preserve a relation involving a functional role, an interface, a state condition and a safety consequence together. The paper extracts entities such as ports, finite-state machines, safe states and safety levels. It then stores descriptions and embeddings for retrieval.

The graph is used for retrieval-augmented specification extraction. The same document input is processed independently multiple times. Each run produces a candidate specification set and a self-reported completeness confidence. The candidate sets are embedded, pairwise semantic distances are computed, and agglomerative clustering identifies the most consistent group. The highest-confidence candidate in the dominant cluster becomes the selected specification set.

This procedure reduces variation between LLM responses; it does not prove that the dominant cluster is complete or correct. If every response omits the same requirement, agreement will make the omission look stable. Self-reported confidence is a selection signal, not an external safety metric. Independent requirement review remains necessary.

### RTL alignment makes a document requirement checkable

The document graph is extended with an RTL control/dataflow graph extracted using PyVerilog. RTL nodes and edges carry structural descriptions. Fuzzy string matching aligns document entities with RTL entities. This produces a unified graph that connects a safety statement to registers, reset logic, control signals and data dependencies.

For each target signal, SafeGen retrieves two kinds of context. A breadth-first search collects graph nodes and hyperedges within a hop limit; the experiment uses a limit of five. In parallel, multiple LLM summarizers condense functional and safety information from the FMEDA, safety and design documents. The combined context is supplied to an LLM that generates Functional Safety Assertions (FSAs) for individual signals. A further LLM step maps each assertion to one or more specifications. This enables a fault to affect several requirements rather than forcing a one-to-one mapping.

The alignment is useful because an assertion needs both semantic intent and concrete RTL names and relationships. It also introduces a failure mode. Fuzzy matching can connect concepts that share words but have different temporal or physical roles. The paper's quality metrics therefore need to be read separately from the existence of a graph edge.

### Gate faults are mapped to RTL effects

The method supports stuck-at and bridging faults. Stuck-at faults force a net to a constant value. Bridging faults couple two nets; the paper models wired-AND, wired-OR and dominant bridging behavior. It converts the fault into an equivalent RTL-level structure using multiplexer-based injection controlled by a Boolean-difference activation signal.

For each gate-level output, the method compares the Boolean behavior of the fault-free and faulty netlists. The difference identifies conditions under which the fault changes that output. The affected outputs are traced back to RTL signals, and the injected RTL effect is used for formal checking. The implementation extracts stuck-at faults from the netlist and collapses equivalent faults. It obtains physical layout and coupling data for bridging faults. It removes bridging faults that create combinational loops.

This mapping is a bridge between physical fault models and RTL assertions, not an exact replacement for transistor-level electrical behavior. A bridging abstraction must preserve the activation and propagation behavior relevant to the safety property. Coupling, timing, analog contention or layout-dependent effects outside the abstract model are not automatically covered.

### FPV grades a fault through violated assertions

SafeGen proves the fault-free assertions first and excludes vacuous proofs from its assertion-quality table. It then performs formal property verification on each fault-effect-injected RTL. For a fault, a previously proven assertion may become vacuously true or may acquire a counterexample. The violated assertion set is mapped to the specification set associated with each assertion. If specification `j` has importance score `I_j`, the fault score sums the importance scores for the affected specifications.

This score is not a physical probability of failure. It is a semantic importance aggregate under the extracted specifications and their assigned scores. A high score means that the fault violates requirements considered important by this workflow. It does not mean the fault occurs frequently. It does not mean that the system will fail under every environment. It does not mean the risk is acceptable under a safety standard.

### The FOC study supplies a concrete closed-loop boundary

The case study uses a field-oriented-control design for a permanent-magnet synchronous motor. The digital subsystem reads current and rotor angle and performs Clarke and Park transforms. It applies proportional-integral control. It generates three-phase PWM through space-vector PWM. A physical model contains the inverter, motor electrical and mechanical dynamics, and position sensor. The control target uses `I_D = 0` and regulates torque through the quadrature-axis current.

The authors construct functional-safety documentation using RTL-level stuck-at fault simulation. A torque deviation beyond ±10% of nominal is labeled unsafe for that documentation process. SafeGen then uses the resulting documents and RTL to extract specifications and generate assertions. The later gate-level fault criticality analysis uses FPV and is separate from the simulation used to prepare the documents.

That separation matters. A circular dependency can arise if the same simulation labels generate the safety document. It can also arise if they evaluate the proposed method. This holds without an independent check. This holds without an independent check. The paper uses closed-loop functional fault simulation as a reference for validating SafeGen's fault detection. It also uses it to show that structural simulation is pessimistic. It does not treat the closed-loop simulation as the deployable baseline. The intended grading stage precedes final physical component selection.

### Assertion quality results

On the assertion-quality comparison, SafeGen generates 976 assertions. Of these, 745 are syntactically correct and 250 are formally proven, excluding vacuous proofs. Its reported COI coverage is 83.68% statement, 83.73% branch, 83.83% functional and 84.48% toggle. AssertLLM reports 424/313/83 generated/syntax-correct/proven and 66.59/66.99/65.05/56.20 coverage across those four columns. AssertionForge reports 667/460/105 and 66.75/67.02/66.13/62.31.

Removing HyperKG reduces SafeGen to 625/459/170 and 66.55/66.96/64.53/53.25. These results support the paper's narrower ablation claim. The claim is that the retrieved semantic context improved assertion yield and coverage under the FOC setup. Assertions that were difficult to converge were removed from the evaluation set. For baselines that could not handle internal signals, the comparison was limited to module-port signals. Those filtering rules affect the denominator.

### Fault-criticality results

For fault analysis, the paper reports SafeGen detecting 2,287 of 18,869 collapsed bridging faults. It also reports SafeGen detecting 39,240 collapsed stuck-at faults in the extracted setup. The closed-loop functional simulation detects 794 of 16,495 bridging faults. It detects 4,889 of 183,346 stuck-at faults under the ±10% torque criterion. SafeGen captures 80.6% of the bridging faults detected by functional simulation. It captures 82.6% of the stuck-at faults detected by functional simulation. These figures come from the paper's comparison. Structural simulation detects 4,688 bridging faults and 39,240 stuck-at faults. Many do not cause closed-loop torque errors. The paper cites 3,894 bridging and 34,351 stuck-at cases as structurally detected without corresponding system errors.

These counts are not directly comparable as raw fault coverage. SafeGen's objective is semantic criticality, and its total fault population and collapsed-fault conventions differ across the methods. The important result is the direction of the comparison. Output propagation labels many more faults unsafe than the closed-loop torque behavior does. Specification-linked FPV seeks a middle layer that explains which requirements are affected.

### What this paper establishes and what remains conditional

SafeGen provides a traceable architecture connecting safety documents, RTL structure, generated FSAs, gate-level fault effects and formal violations. Its FOC experiment supports the claim that HyperKG context improves the reported assertion-quality measures. It also supports the claim that specification-linked FPV can separate structural propagation from closed-loop functional impact. This is under the stated fault models.

It does not establish that the extracted requirements are complete. It does not establish that LLM importance scores meet a safety standard. It does not establish that gate-to-RTL bridging abstractions cover all physical faults. It does not establish that a high criticality score equals field risk. The safety conclusion remains conditional on document quality, graph alignment, fault abstraction, and assertion nonvacuity. It also depends on formal assumptions, the ±10% torque criterion and the selected motor model. Independent safety-engineer review and reproduction on other control systems are required.

**Primary source read:** [SafeGen arXiv version 1](https://arxiv.org/abs/2606.25296), Sections 1–5 and Tables 1–2. They include HyperKG construction, RTL alignment, fault mapping, FOC setup, assertion metrics, criticality definition and fault comparisons. The [DAC 2026 official description](https://63dac.conference-program.com/presentation/?id=RESEARCH1945&sess=sess160) was also a primary source. The manuscript was read; the code, JasperGold/Xcelium flow and fault campaign were not executed here.

<span id="explanation-dac-2026-research3200"></span>

## STELLAR: how structural retrieval constrains generated assertions

### The starting problem is not only language generation

An RTL block has control structure, data movement, clock behavior and state updates. An SVA must refer to that behavior with the right signals, timing event and temporal relation. Two blocks can use different signal names while having the same control pattern. They can also use similar words while requiring different properties. A retrieval system that only compares text can therefore return an example that looks relevant. That example may have the wrong hardware behavior.

STELLAR treats assertion generation as two linked problems. First, it must retrieve examples whose RTL structure is relevant to the target block. Second, it must make the language model produce an assertion for every required execution path. It must also preserve a useful assertion style. The design is intended for cases where a verification team already has RTL blocks paired with expert-written SVAs. It reuses those pairs as a checked knowledge base instead of asking a model to invent all properties without examples.

### The unit of retrieval is a block with local context

The paper does not feed an entire hardware project into one prompt. It decomposes RTL into individual `always` blocks or finite-state-machine units. It keeps the local declarations, sensitivity list and interface signals needed to interpret cross-block behavior. This creates a retrieval unit small enough to index. It also creates a prompt unit small enough for an LLM. It retains the clock and interface information that affects an assertion.

That choice defines a scope boundary. A property about one block may depend on state or protocol behavior outside that block. Local decomposition can make retrieval tractable, but the resulting SVA still needs review against the surrounding design and its assumptions. A locally valid assertion can be incomplete if the required behavior is distributed across blocks.

### Structural fingerprints record what the RTL does

STELLAR parses each RTL unit into an abstract syntax tree. An abstract syntax tree represents the nesting and kinds of code operations. It does not treat the source as an undifferentiated string. The fingerprint records control-flow features such as `if`/`else` nesting depth and branch count. It also records assignment types such as blocking and non-blocking assignments, and data-flow structure. It also adds a context prefix derived from the sensitivity list, such as asynchronous logic or positive-edge-triggered synchronous logic.

The context prefix matters because a combinational block and a clocked block can have similar branch shapes. They can still require different temporal assertions. The fingerprint is also less dependent on arbitrary signal names than raw-code embedding. The paper compares 1,000 randomly selected VERT designs. HW2VEC embeddings had 97.7% of designs involved in at least one collision. The reported STELLAR fingerprint comparison reduced the corresponding collision figure to 1.7%. This is evidence about that sampled representation experiment, not a proof that all distinct RTL blocks are separated.

### Retrieval uses embeddings and an approximate index

The fingerprint strings are encoded with the all-MiniLM-L6-v2 Sentence Transformer and stored in a FAISS index. FAISS supports approximate nearest-neighbor search: it finds likely close vectors without comparing the query exhaustively with every stored item. The paper measures query runtime while increasing the populated data set in steps of 100 up to 3,000 samples. The reported result is that embedding retrieval with FAISS scales better in that experiment. The alternatives are raw string matching and brute-force methods.

The retrieval quality test uses 100 duplicated RTL modules. It compares exact duplicates with a second condition. In that condition 30% of variable names are changed while the logic is preserved. Raw semantic embedding retrieves the exact duplicate well when names are unchanged. Its Recall@10 falls from 1.0 to 0.2 after renaming. STELLAR reports Recall@10 of 0.99 for exact duplication and 0.99 after the 30% renaming condition. The test measures whether a known source item is retrieved under a controlled transformation. It does not show that the nearest item is the best expert example for every new design.

### The prompt contains a structural coverage obligation

Retrieval alone does not force a model to cover every branch. STELLAR traverses the target AST and counts its unique execution paths. It inserts that count into the prompt as a required number of assertions, one for each path. This targets a concrete failure mode. An LLM may describe the first and last branch in an `if`/`else if` chain. It may omit a middle branch. The omitted branch becomes a verification blind spot even though the generated assertions are syntactically valid.

The paper's path experiment compares a zero-shot GPT-4o mini baseline with STELLAR. The designs contain 2, 3, 4 and 8 paths. The baseline path coverage falls from 100% for 2-path designs to 37.9% for 8-path designs in the figure. STELLAR reports 100% for each displayed complexity group. In the larger generation table, GPT-4o mini rises from 49.84% zero-shot execution-path coverage to 100.00% with three retrieved examples. With five examples it reaches 99.92%. These numbers measure whether each structural path has a generated assertion. They do not prove that the assertion expresses the correct temporal or functional consequence of that path.

### Generation is evaluated at several different levels

STELLAR combines the target RTL, the top retrieved RTL/SVA pairs and the path-count instruction in one prompt. The raw model output is parsed into assertions. The paper evaluates three model classes: GPT-4o mini, Llama-3.1-8B-Instruct and CodeLlama-7B-Instruct. It compares zero-shot generation with three and five retrieved examples.

Syntax correctness asks whether the SVA parses. BLEU measures lexical similarity to the reference assertion, and BERTScore measures semantic similarity. Execution-path coverage counts whether the generated set contains an assertion for every path. These are not interchangeable. A syntactically valid assertion may be vacuous. A high BLEU score can reflect wording similarity without proving the property. Path coverage can be complete while the temporal relation is wrong.

For GPT-4o mini, five retrieved examples raise syntax correctness from 84.88% to 99.80%. They raise BLEU from 0.56 to 0.93. They raise BERTScore F1 from 0.904 to 0.96. They raise execution-path coverage from 49.84% to 99.92%. For Llama-3.1-8B, the corresponding changes are 33.25% to 77.29% syntax correctness and 0.33 to 0.88 BLEU. They are 0.876 to 0.95 BERTScore and 29.52% to 93.04% path coverage. For CodeLlama-7B, syntax correctness changes from 46.26% to 84.44%. BLEU changes from 0.255 to 0.84. BERTScore changes from 0.874 to 0.95. Path coverage changes from 29.49% to 73.38%. The table supports the claim that structural examples and the path instruction improve these reported measures. This holds under the selected models and data split.

### The knowledge base is filtered before retrieval

The source VERT data contains RTL/SVA pairs, but the paper first checks SVA syntax, removes failed entries and normalizes formatting. It then creates a non-overlapping knowledge base and query set. The set is stratified by execution-path count, synchronous versus asynchronous timing and primary control structure. The split is approximately 2:1, with around 10,000 items for the knowledge base and 5,000 for the query set.

This preprocessing is part of the result. It removes malformed examples before they can influence prompts. It also reduces the risk that the query set duplicates the retrieval corpus. It does not establish that the surviving assertions are functionally correct. The paper describes VERT as providing a canonical reference assertion. It uses that reference for similarity metrics. Formal proof validity still needs to be checked for the generated properties.

### The real-design case studies add formal-tool evidence

The paper evaluates UART, an I2C master controller and SHA-3/Keccak using GPT-4o mini with three retrieved examples. All syntactically valid assertions are sent to Cadence Jasper for formal coverage analysis. In the UART case, STELLAR reports 184 generated SVAs, an 89.7% syntax-pass rate, and 85.7% COI coverage. It also reports 64.1% statement coverage, 71.7% branch coverage and 90.0% toggle coverage. The zero-shot baseline has 114, 55.3%, 67.0%, 35.9%, 39.1% and 76.0%. For the I2C master, it reports 125 SVAs, 95.2% syntax-pass, and 81.3% COI. It also reports 85.9% statement, 80.7% branch and 77.8% toggle coverage. The zero-shot baseline has 111, 75.0%, 37.7%, 34.7%, 56.4% and 30.9%. For SHA-3, STELLAR reports 44 SVAs, 90.9% syntax-pass, 78.3% COI, 78.9% statement and 80.4% toggle coverage. The zero-shot baseline has 58, 67.2%, 49.5%, 40.4% and 50.8%. Branch coverage is omitted because the paper treats many SHA-3 branches as inherently unreachable.

These case studies strengthen the evidence beyond string metrics because a formal tool is used after generation. They still do not make generated assertions correct by construction. Formal coverage measures explored implementation structure under the tool's assumptions. It does not establish that the assertions encode the complete specification. It also does not establish that a high coverage score means no important behavior is missing.

### What STELLAR establishes and what remains open

STELLAR gives a precise mechanism for using design structure to improve assertion generation. It decomposes RTL into local units and builds AST fingerprints with timing context. It retrieves structurally similar RTL/SVA pairs and counts execution paths. It constrains the prompt, parses the output and checks it with syntax and formal tools. The reported results support the narrower claim that this process improved several measures over the stated baselines. These are retrieval stability under identifier renaming, generated-path coverage, syntax rates, similarity measures and selected formal-coverage results.

The paper does not establish universal assertion correctness, complete specification coverage, or nonvacuity of every generated property. It also does not establish transfer to industrial designs outside VERT and the three case studies. It does not establish equivalence between BLEU/BERTScore and verification value. The retrieved example can encode a wrong assumption. The path count can require one assertion per path without proving the assertion's meaning. Formal coverage depends on the property set, assumptions, tool configuration and reachable state space. Independent review of each assertion and reproduction on designs with known bugs remain necessary.

**Primary source read:** [STELLAR arXiv version 3](https://arxiv.org/abs/2601.19903), Sections 3–5 and Tables 2–5, PDF pages 3–7. They include fingerprint construction, collision experiment, FAISS retrieval, path-count prompting, VERT split, model comparison and UART/I2C/SHA-3 case studies. The [official DAC record](https://63dac.conference-program.com/presentation/?id=RESEARCH3200&sess=sess108) was also a primary source. The manuscript was read; the retrieval index, LLM calls and Jasper flow were not executed here.

<span id="explanation-dac-2026-research1037"></span>

## Seeing the Unseen: how hidden PMU events are turned into testable microarchitectural hypotheses

### The observable is a counter, not the hardware meaning

A processor performance-monitoring unit exposes programmable events and returns counts. The count is an observation produced by a hardware mechanism, not a direct label for the internal event. A vendor may document an event as related to branches. The documentation may not say which pipeline condition increments it, or which instruction classes qualify. It may not say whether speculative work is included. It may also not say how several event-select and unit-mask settings interact.

The paper starts from this gap. Hidden PMU events have been disclosed by earlier work, but their microarchitectural semantics remain unclear. “Semantics” here means the conditions inside the processor that cause the event to count. Without that mapping, a researcher cannot reliably use the event for performance diagnosis. A security analyst also cannot know whether the event exposes a signal that an attacker can control or observe.

### Reverse engineering requires controlled differences

The central difficulty is that a PMU count mixes two behaviors. They are the behavior of the test program and the behavior of the processor. If a workload changes several things at once, a changed count does not identify the internal cause. A useful experiment must therefore hold as much as possible fixed. It must vary one architectural or microarchitectural condition. It must observe how the hidden event responds.

The official description calls the method a differential-analysis and simulation-validation framework. The first part supplies controlled differences. It constructs workloads or instruction sequences that differ in a known feature. It measures the hidden event and compares the count patterns. A candidate explanation is stronger when the event changes when the proposed trigger changes. It is also stronger when the event remains stable when unrelated program details change. It is stronger still when it predicts the direction of change across several tests.

The result of this phase is a hypothesis about the event, not yet a proof. The same counter response can sometimes be produced by more than one internal condition. The experiment must therefore distinguish the candidate explanation from alternative explanations. It must preserve counter configuration and processor conditions. It must report noise and repeatability. The public DAC record does not provide those details for this paper.

### Simulation supplies a second observation path

The framework also uses simulation validation. A simulator represents selected processor structures and produces an internal event signal or event count when the modeled conditions occur. The measured hardware response and the simulated response can then be compared under the same or equivalent workloads.

This comparison has a precise role. If a simulator reproduces the observed change under a proposed internal condition, it supports the causal interpretation. This is stronger than a count correlation alone. It can also expose which internal state transition or pipeline condition is sufficient to produce the event. It does not establish that the simulator contains every relevant feature of a commercial processor. Agreement is conditional on the simulated microarchitecture, event model, workload construction and the mapping between simulated and physical configurations.

### UMask combinations are part of the event definition

On Intel processors, an event is selected using an event code and unit-mask settings. A single unit-mask bit may select one condition. A combination of bits may be interpreted as a set of conditions, a mode, or an undocumented internal selector. Consequently, testing only documented single settings can miss behavior created by combinations.

The paper reports discovering a hidden pattern of UMask combination for branch-related events. The important methodological point is that the combination itself becomes an object of study. The researcher must enumerate or strategically sample settings, run workloads that separate branch behaviors, and compare the resulting count signatures. A discovered pattern is useful only if its effect is repeatable and tied to a defensible microarchitectural condition. It must also not be an artifact of counter multiplexing, skid, speculative execution or another measurement detail. The official record names the pattern. It does not expose its bit values, tested processor generations, count tables or simulator configuration.

### Branch events connect the method to processor behavior

Branch-related events can reflect several different stages or outcomes. A branch may be decoded, predicted, issued, executed, resolved, retired, mispredicted or recovered. These events can have different security value. An attacker needs a signal that changes with a victim-dependent condition. The signal must remain measurable under the available privilege and noise constraints.

The framework’s branch demonstration therefore has two layers. First, it infers what hidden event behavior corresponds to which branch-related condition. Second, it asks whether that event can carry information across a security boundary. The first layer is microarchitectural characterization. The second is an attack evaluation. A successful attack does not by itself prove that the inferred semantics are complete. A semantic hypothesis does not by itself prove that an attack works in a realistic threat model.

### The security demonstrations use the recovered signal

The paper reports two demonstrations. It uses a PMU-based covert channel for Spectre-v1 in Intel Software Guard Extensions. It also enables high-precision website fingerprinting under resource-constrained conditions. In a covert channel, the sender influences a measurable hardware state. The receiver observes a signal correlated with that state. In website fingerprinting, an observer classifies a visited site from execution traces or hardware measurements. The observer does not use the page contents.

The recovered PMU event can serve as the measurement signal. This holds when it changes predictably with the microarchitectural activity induced by the attack or workload. The chain of reasoning must be kept explicit. The event must be programmable. The target activity must alter the event count. The observer must obtain the count under the stated privilege and scheduling conditions. The signal must survive noise. The inferred information must be useful for the attack objective. Breaking any link changes the security conclusion.

The official page does not report numerical fingerprinting precision, trace count, attack duration, and classification protocol. It also does not report processor models, counter settings, noise controls, SGX configuration, or mitigation comparison. “High precision” is therefore a reported qualitative claim in the current evidence set, not a number that can be compared with other attacks.

### What the paper establishes from the available source

The DAC record supports a mechanism-level description of a framework. The framework combines controlled differential experiments with simulation validation to infer the semantics of hidden PMU events. It demonstrates the method on branch-related events. It identifies an undocumented UMask-combination pattern on Intel CPUs. It uses the recovered behavior in two security demonstrations. It supports the interpretation that PMU documentation is not a complete description of the processor’s observable event space.

The available source does not establish the exact event encodings or the processor generations on which the behavior holds. It does not establish the simulator fidelity. It does not establish the size and statistical treatment of the workload set, or the numerical attack results. It does not establish whether the demonstrations transfer across CPUs and firmware configurations. It also does not establish that every hidden event can be reverse-engineered with the same method. A defensible follow-up needs the paper, event tables, experiment scripts, and simulator model. It also needs repeated measurements, threat-model details and a mitigation or disclosure analysis.

**Primary source read:** [official DAC research-manuscript record](https://63dac.conference-program.com/presentation/?id=RESEARCH1037&sess=sess107). It supplies the problem statement, differential-analysis and simulation-validation framework, and branch-event demonstration. It also supplies the hidden UMask-combination finding, Spectre-v1-in-SGX covert-channel demonstration and resource-constrained website-fingerprinting claim. The target manuscript, numerical tables, simulator details and artifact were not recovered. No results from the related 2023 hidden-PMU paper were substituted for this record.

<span id="explanation-dac-2026-research1356"></span>

## ChatSVA: how staged representations and verified data improve assertion generation

### The target is a verified behavior, not merely legal SVA syntax

An SVA can be syntactically valid and still express the wrong hardware behavior. For example, it can name valid signals but use the wrong clock. It can omit a reset condition or assert a relation in the wrong cycle. It can also cover only one of several legal operating cases. ChatSVA treats these as separate failure modes. Its evaluation reports Syntax Pass Rate, Function Pass Rate and Function Coverage. It does not use syntax as a proxy for functional correctness.

The system starts from a high-level specification of a hardware design. The specification is expected to describe functions, input and output ports, internal register mappings and temporal behavior. The method then creates intermediate representations before producing SVA. This is a response to a specific reasoning problem. Asking one model call to translate a long specification directly into assertion code requires several steps at once. The model must extract requirements and connect them to implementation signals. It must choose temporal semantics and write legal SVA.

### Four intermediate representations divide the translation

ChatSVA uses four specialized agents. SpecWiz, Agent1, extracts verification-critical information from the specification and creates a Verification Plan. The plan records functional descriptions, signal relationships and verification requirements in a standard form. Feature Generator, Agent2, refines the plan into modular Feature Lists that describe expected behavior under test scenarios. Checkpoint Generator, Agent3, expands each feature into implementation-specific Checkpoints. SVA Generator, Agent4, translates one checkpoint into an SVA that can be used by formal verification or simulation.

The representations form a directional chain:

`Spec → Verification Plan → Feature List → Checkpoint → SVA`

Each step reduces or specializes information. The plan is not the assertion; it is the structured statement of what must be checked. A feature groups related behavior. A checkpoint names a concrete verification point and its implementation conditions. The SVA is the executable property. Keeping these levels separate makes it possible to inspect where an error entered the chain. It also makes it possible to validate each stage with a different method.

This decomposition also defines a limit. If the original specification omits a requirement, later agents cannot recover it from the chain. If a plan maps a requirement to the wrong register or clock, a well-written checkpoint can preserve that wrong mapping. So can a syntactically valid SVA. The workflow improves traceability and credit assignment; it does not replace specification review.

### AgentBridge defines what training data is allowed to contain

The central data problem is not simply too few examples. A noisy example can teach a model a plausible but false relationship between a feature, checkpoint and assertion. AgentBridge constructs task-specific data under three principles.

First, the information flow is directional. An output must be a functional subset of an input. A generated checkpoint may specialize a feature, and an assertion may implement a checkpoint. The output must not invent behavior that was absent from the source. This gives each generated item a definite relation to its source. It avoids accepting a partially overlapping answer as useful training data.

Second, the input must come from a verified golden dataset. A preprocessing function adapts the golden data to a task. The starting material is not itself generated by an unverified model. This is a provenance condition. Later labels inherit the quality boundary of the golden source and the checks applied to each transformation.

Third, each output must be verifiable by a practical Boolean decision. AgentBridge allows either a direct verifier or a Bridged Agent. The Bridged Agent converts the output into a form a direct verifier can check. This is important because different stages have different checks. Expert review can validate a Verification Plan, while formal equivalence can validate an SVA recovered from a checkpoint.

### The data loop uses forward and reverse checks

AgentBridge starts from a golden input `Q0` and asks an agent to generate candidate answers `A0`. An augmentation group analyzes the input-to-answer mapping and proposes missing cases, producing an augmented set. The validation stage then applies a task-specific verifier.

For a one-to-many task, each generated item can be checked as a functional subset of the source. For a one-to-one task, such as converting a checkpoint into one SVA, AgentBridge uses reverse generation. It generates a question or checkpoint from a candidate answer, then asks independent agents to regenerate the answer. A candidate is accepted only when the reverse-generated result passes the relevant verification condition. The paper then pairs the original input with the validated answer. It records the successful validation path as reasoning data for supervised fine-tuning and retrieval.

In the ChatSVA instantiation, Agent2 starts from expert-verified Verification Plans and its Feature Lists are checked by expert review. Agent4 receives a more stringent loop because the checkpoint-to-SVA relation is one-to-one. A golden SVA is used to produce a candidate checkpoint. The checkpoint is used to generate a new SVA. The pair is retained when the new SVA is functionally equivalent to the original under formal verification. The fine-tuned Agent4 can then serve as a Bridged Agent for validating other generated data.

This is a data-quality mechanism, not a proof that every generated assertion is correct. It can reject many bad examples if the verifier is sound and the golden input is correct. It can also preserve a shared blind spot. This happens if the golden assertion, checkpoint mapping and verifier all omit the same requirement.

### Training combines specialized models with retrieval

The authors construct a 15.36 GB dataset containing examples from all pipeline stages, domain knowledge and verification guidelines. Agents 2–4 use full-parameter supervised fine-tuning of Llama 3.1 8B on an 8×A800 server. The settings are sequence length 8,192, learning rate 1e-5, batch size 64 and three epochs. Agent1 uses GPT-4o with retrieval-augmented generation for high-level reasoning. The reported temperature for all agents is 0.2.

These details matter because the result is a complete workflow, not a prompt-only comparison. Data synthesis, model specialization, retrieval and stage decomposition all contribute. A reproduction must preserve the model versions, training data construction, verifier, sampling temperature and evaluation budget. Only then can the result be attributed to the four-agent topology alone.

### The metrics answer different questions

The evaluation uses the public FIXME benchmark, described as containing diverse industrial designs such as CPUs, GPUs and IP blocks. The paper compares ChatSVA with GPT-4o, DeepSeek-R1 and AssertLLM. To make the AssertLLM comparison direct, the authors reproduce its methodology with GPT-4o as the base model. They exclude methods that require RTL input. The target task is specification-to-SVA, and additional RTL can create co-source information.

Syntax Pass Rate is the fraction of generated SVAs that parse. Function Pass Rate applies the verification function to syntactically valid SVAs and measures the fraction that pass the functional check. Function Coverage measures bug-detection capability for functionally correct assertions against predefined bug types such as protocol violations and illegal branches. The denominators therefore differ. A high syntax rate can coexist with a low functional rate. A high function coverage value is meaningful only over the stated bug set and verification protocol.

On 24 RTL designs, ChatSVA reports an average of 139.50 SVAs per design. It reports 98.66% Syntax Pass Rate, 96.12% Function Pass Rate and 82.50% Function Coverage. GPT-4o reports 4.17% Function Coverage and DeepSeek-R1 5.83%. AssertLLM reports 98.52% syntax pass, 62.84% function pass and 7.50% function coverage. The paper reports that ChatSVA generates more than 18 times the SVA volume of GPT-4o. It also reports more than 11 times the function coverage of AssertLLM under this benchmark protocol.

The ablations separate workflow structure from task-specific data. Applying the staged workflow to base GPT-4o without the fine-tuned agents raises Function Pass Rate from 43.09% to 72.88%. It raises Function Coverage from 4.17% to 20.83%. Adding the full ChatSVA training and AgentBridge data raises Function Coverage from 20.83% to 82.50%. This supports the paper's narrower attribution. Decomposition contributes a large improvement. The high-purity specialized data contributes the larger final functional-coverage result.

### Coverage distribution tests whether the average hides gaps

The authors report that ChatSVA detects 15 of 16 unique bug types in a qualitative distribution analysis. AssertLLM detects 6 of 16. This checks breadth across categories, not only the average number of detected bugs. It still depends on the benchmark's bug taxonomy and the number and construction of cases per type. It also depends on whether each bug is independently observable through the generated property set.

AgentBridge data precision is evaluated on candidate checkpoints generated from more than 500 golden SVAs with manually labeled ground truth. With one reverse-generation agent, the paper reports a 7.36% false-positive rate and 88.8% precision. With five agents, the false-positive rate falls to 0.05% and precision rises to 99.9%. This is a purity/completeness tradeoff. Stricter agreement can remove bad examples. It can also reject valid examples and reduce the diversity of the training set. The paper's reported precision does not by itself establish recall of all valid checkpoints.

### What ChatSVA establishes and what remains conditional

ChatSVA provides a coherent end-to-end method for specification-to-SVA generation. It divides the reasoning chain into inspectable representations and generates task-specific data from verified sources. It uses direct or reverse verification to filter examples. It fine-tunes specialized agents. It evaluates syntax, functional pass and bug coverage separately. The reported 24-design results support the narrower claim about this workflow and its AgentBridge data construction. The claim is that they substantially improved the paper's measured functional assertion quality over the listed baselines.

The results do not establish complete specification coverage or correctness beyond the FIXME benchmark. They do not establish independence from the golden SVAs and manually labeled data. They do not establish safety of deploying generated assertions without human review. Functional Pass Rate depends on the verification function and its assumptions. Function Coverage depends on the predefined bug types and their construction. The paper also contains an unfinished-looking benchmark name in the extracted manuscript text. The exact benchmark version and evaluation scripts should therefore be preserved in a reproduction. Full artifact execution, independent assertion review and transfer to unseen industrial designs remain open.

**Primary source read:** [ChatSVA arXiv version 1](https://arxiv.org/abs/2604.02811), Sections 3–6 and Figures 3–7, PDF pages 3–7. They include the four-stage representations, AgentBridge principles and validation loop, 15.36 GB training dataset. They also include model/training settings, benchmark definitions, Table/Figure results and reverse-generation precision study. The [official DAC record](https://63dac.conference-program.com/presentation/?id=RESEARCH1356&sess=sess166) was also a primary source. The manuscript was read; the training run, benchmark and verification flow were not reproduced here.

<span id="explanation-dac-2026-research080"></span>

## Beyond Flat Netlist: how DeepSeq3 represents state transitions without flattening the whole circuit

### A sequential circuit is not only a combinational graph

A gate-level netlist can be represented as a directed graph: gates are nodes and wires are directed connections. That representation is useful for local logic, but a sequential circuit also has memory. Flip-flops store values at one clock edge and provide those values to combinational logic during the next cycle. The important behavior is therefore not only which gates connect, but how register states change over time.

Flattening the entire netlist into one graph creates two problems. The graph can be too large for efficient graph learning. Ordinary message passing also does not automatically tell the model which relationships describe state transitions across clock cycles. DeepSeq3 addresses both by preserving the flip-flop boundary. It learns at two levels: local combinational logic and global register-level state flow.

### Stage one learns each combinational region

The preprocessing step cuts the sequential circuit at flip-flops. Each resulting subgraph starts from primary inputs or flip-flop outputs and ends at the next flip-flop inputs or primary outputs. Within that boundary, the subgraph describes a time-independent Boolean computation for the current cycle.

DeepSeq3 applies a logic-aware, layer-wise GNN to each subgraph. It maintains representations for two conditions. One is the probability that a node is logic 0. The other is the probability that it is logic 1. Gate-specific message aggregation follows the Boolean operation. For an inverter, the representation for output 0 is informed by the predecessor's output-1 representation, and vice versa. For an AND gate, predecessor information is combined according to the corresponding Boolean state. A GRU updates each node representation after aggregation.

This is different from using only a generic graph convolution. The message rule contains information about how the gate transforms logic states. The model is trained to predict logic-state probabilities. Its representation is therefore pressured to retain functional information about the local Boolean block. It does not retain only connectivity or node degree.

### Stage two replaces many gates with register-level super-nodes

After the local encoders produce embeddings, each combinational subgraph becomes one super-node. A directed edge connects two super-nodes when the output flip-flop of one region drives the input flip-flop of the other. The resulting Super-Node Graph represents the circuit at register-transfer scale. Its nodes are clock-domain data blocks. Its edges describe how stored state can influence later stored state.

This compression is structural, not an approximation that discards all internal logic. The local embedding carries the internal Boolean behavior, while the SNG carries the higher-level dependency. The paper reports that the SNG can be one to two orders of magnitude smaller than the original gate graph. This holds for a large circuit. The exact compression ratio depends on how many gates lie between registers and how the partitioning is defined.

### The pretraining target is global state behavior

A single flip-flop transition does not describe the whole sequential machine. Several registers may form a cycle, and a state that is locally possible may be globally unreachable. DeepSeq3 therefore treats the circuit as a finite-state system. The state vector contains the flip-flop values and output values. The one-step transition matrix `P` records the probability of moving from one state to another under the input-stimulus distribution.

The infinite-step reachability matrix `A∞` records whether any sequence of allowed transitions can reach state `j` from state `i`. These two targets answer different questions. `P` describes immediate behavior; `A∞` describes the longer-term structure of the state graph. Joint supervision is intended to prevent the model from learning only local register correlations while missing cycles and global constraints.

The state space grows exponentially with the number of registers and outputs. The paper computes exact or fuller transition information for small and medium circuits. Larger circuits use sampled simulation traces to construct a sparse transition matrix. It then uses transitive closure for reachability, with Floyd–Warshall for smaller cases and breadth-first search for larger sparse cases. This makes the targets practical. The large-circuit labels are approximations of the complete state graph and inherit the coverage of the sampled traces.

### State-conditioned embeddings preserve the meaning of a transition

The model maintains two embeddings for each super-node, corresponding to local state 0 and local state 1. Given a source state and target state, it selects the appropriate embedding for each node. It concatenates the source and target representations. It uses a pooling Transformer to form a global circuit representation. An MLP predicts the one-step transition probability and infinite-step reachability from that representation.

This structure gives the model a direct input for the question it must answer. Which local blocks are active in the source state? Which are active in the target state? How do their register-level dependencies relate? The model is not proving reachability by itself. It is learning a representation supervised by simulated or computed reachability labels. Downstream EDA tasks can then use it.

### Pretraining results separate local logic from temporal semantics

The paper trains on 3,568 sequential circuits from ISCAS'89, Opencore and ITC'99, converted to sequential AIG form with ABC. The circuits contain approximately 100–500 nodes after optimization. Training uses a hidden dimension of 128 and a three-layer pooling Transformer. It also uses three-layer MLPs, Adam at learning rate 1e-4, 40 epochs and two NVIDIA A100 GPUs.

For logic-1 prediction, DeepSeq3 reports R² 0.9869 and MAE 0.0193; for logic-0 prediction it reports R² 0.9916 and MAE 0.0168. At register level, it reports infinite-reachability F1 0.8429 and one-step-transition correlation 0.8413 with MAE 0.0049. DeepSeq2 reports F1 0.3048 and transition correlation 0.2922 on those corresponding tasks. The ablations show that removing the Stage1 local representation lowers reachability F1 to 0.7752. Removing infinite-reachability supervision lowers F1 to 0.0341. Removing one-step-transition supervision lowers transition correlation to 0.6442 while retaining F1 0.8249.

The ablations show that the two temporal targets are not redundant. A model can retain reachability behavior while losing immediate-transition accuracy, or retain immediate-transition correlation while losing long-range reachability classification. These metrics evaluate learned representation targets. They do not alone show that a downstream formal search is complete. They do not show that a power prediction transfers to a fabricated design.

### The representation is tested on dynamic-power prediction

For a downstream power task, the authors map circuits to the Nangate 45 nm standard-cell library. They simulate 10,000 clock cycles to obtain dynamic-power reference values. An MLP combines DeepSeq3 gate embeddings and enhanced flip-flop embeddings to predict power. DeepSeq3 reports average MAPE 4.58% with standard deviation 6.64%, compared with DeepSeq2's 7.44% average MAPE and 7.49% standard deviation.

This is a model-level prediction result under one library and one simulation procedure. It does not mean that the representation predicts total chip power across technologies, physical placements, and clock networks. It also does not mean this across leakage, voltage conditions or real activity traces. The reported improvement is evidence that register-level temporal features can help this selected dynamic-power task, not a complete physical-power validation.

### Guided BMC changes the search order but keeps a fallback

Bounded model checking unrolls a sequential circuit for a finite number of clock steps. It encodes the property violation as a SAT problem. The solver must search for an assignment to inputs and states. The assignment must satisfy the unrolled transition relation and the negated property. A learned representation can help if it identifies states likely to contain a counterexample. An incorrect restriction could hide a real counterexample.

DeepSeq3 addresses that risk by predicting a high-risk subset of flip-flop values at an unrolling depth. Guided BMC first constrains the SAT search to the predicted region. If that constrained search fails, it falls back to the original unconstrained search. The fallback preserves completeness of the original BMC search. This assumes the implementation correctly detects the failure and invokes the full search. The learned model can change the order and cost of finding a counterexample. It does not replace the SAT proof obligation.

The BMC experiment uses 40 randomly selected HWMCC instances with a 1,000-second timeout. The maximum unrolling depths are between 20 and 100. Thirty-one are classified as easy because raw BMC solves them within 10 seconds, and nine are hard. On easy instances, the paper reports an 18.6% speedup from the regression-line comparison, excluding model-inference time. On the nine hard instances, raw BMC averages 255.03 seconds. Guided BMC averages 191.11 seconds, including 5.13 seconds of inference. Guided BMC solves some instances for which raw BMC reaches the 1,000-second timeout.

These numbers must not be collapsed into one universal speedup. The easy comparison excludes inference and is based on a regression line. The hard comparison includes inference and uses a small selected set. The hard cases are the more relevant setting for the method. They are still nine instances. The guided flow uses per-circuit fine-tuning with sampled transition and reachability labels.

### What DeepSeq3 establishes and what remains conditional

DeepSeq3 provides a mechanism for learning sequential-circuit representations at a scale that a flat gate graph makes difficult. It preserves flip-flop-bounded combinational functions and compresses them into a register-level SNG. It supervises immediate transitions and long-term reachability. It uses the resulting representation for downstream prediction and guided formal search. The reported experiments support improvements in the selected representation metrics, dynamic-power prediction, and BMC timing. This holds under the stated datasets and fallback protocol.

They do not establish that sampled reachability labels are complete for very large state spaces. They do not establish that the SNG preserves every property-relevant detail for arbitrary downstream tasks. They do not establish that a model-guided solver is safe without a correctly implemented fallback. Power results remain tied to the Nangate 45 nm/10,000-cycle setup. BMC results remain tied to HWMCC instances, ABC heuristics, and timeout and depth settings. They also remain tied to per-circuit fine-tuning and the distinction between easy and hard timing measurements. Reproduction should inspect the released code and verify the partition and fallback implementation. It should compare solved properties and counterexamples rather than timing alone.

**Primary source read:** [Beyond Flat Netlist arXiv version 1](https://arxiv.org/abs/2608.28188), Sections 3–4 and Tables 1–3, PDF pages 2–7. They include subgraph partitioning, SNG construction, transition/reachability supervision, dataset and training conditions, power prediction and guided-BMC evaluation. The [public DeepSeq3 repository](https://github.com/cure-lab/DeepSeq3) was also a primary source. The manuscript was read; model training, power simulation and BMC execution were not reproduced here.

## Invariants express conditions that must remain true

An invariant is a condition that holds initially and remains true after each allowed state transition. It can help a proof avoid exploring states that the design can never reach. Useful invariants may describe counter ranges, ordering, or agreement between interacting components.

The RISC-V cryptography-extension record describes modular proofs using such invariants. RISC-V is an instruction-set architecture; an extension adds operations beyond a chosen base. Verifying an extension requires a precise statement of those operations and their interaction with the processor. The collected description identifies an approach but does not establish the property count, proof configuration, or complete specification boundary. [Recorded evidence](../observed-subthemes/formal-and-functional-verification.md#paper-dac-2026-research1378)

## SafeGen connects properties to fault consequences

SafeGen's captured method extracts specifications and generates assertions. It relates circuit faults to a higher-level representation. It grades their consequences using formal checks. Each connection needs validation. An omitted requirement can hide an important consequence. An incorrect mapping can attribute a low-level failure to the wrong behavior. [Recorded evidence](../observed-subthemes/formal-and-functional-verification.md#paper-dac-2026-research1945)

Its description does not supply assertion pass rates, fault coverage, grading agreement, or runtime conditions. Those gaps prevent interpreting the proposed process as an established functional-safety result. A process diagram alone cannot show that a system satisfies its safety requirements.

## What would show that the process is better

Start from independently reviewed requirements and known correct and faulty designs where possible. Keep the tool versions and evaluation budget fixed. Measure meaningful faults detected, correct behavior incorrectly rejected, unexpressed requirements, and unresolved checks. Report human effort needed to fix specifications or interpret failures.

For formal claims, preserve assumptions and proof outcomes. For simulation claims, preserve test inputs and coverage definitions. Then evaluate unfamiliar designs to determine whether the method transfers. The useful conclusion identifies which part of constructing and checking the requirements became more reliable or less expensive. It also identifies which work still requires review.
