## Security validation needs a property, not just an unusual result

A hardware security property states what an actor must not be able to observe or change. For example, an unprivileged program may be forbidden from reading a protected register. A useful test must establish the actor's starting permissions, reach the relevant behavior, and determine whether that property was violated.

An unexpected instruction, a suspicious source-code change, and a synthesis-tool failure are three different observations. None automatically establishes the same security impact. This subject brings together three papers on those different parts of validation. Their common question is how to turn candidates into checked findings, not how to combine their counts into a single security score.

There are three distinct jobs. Discovery produces candidates. Characterization determines what those candidates do under stated conditions. Validation tests a particular security consequence against an expected rule. Automating the first job can increase the workload for the others unless the resulting evidence is reproducible and well organized.

<span id="explanation-dac-2026-research2804"></span>

## Undocumented instructions: finding an encoding is not defining its behavior

A processor interprets binary instruction encodings according to its implementation and execution mode. An undocumented instruction is one whose behavior is not described in the documentation being used. It is not necessarily malicious or exploitable. Discovery must distinguish an executed operation from an invalid encoding, an alias for an existing operation, or behavior dependent on a particular processor state.

[Automated Discovery, Classification, and Systematic Security Verification Methodology for Undocumented Instructions](../observed-subthemes/hardware-security-validation.md#paper-dac-2026-research2804) reports an automated discovery, classification, and security-verification framework. The official description gives 23 new instructions, 29 classified instructions, 99.8357% classifier accuracy, and five instructions with security implications. It does not identify the processor, privilege settings, labeled dataset, split protocol, or the five consequences. These are separate reported quantities, not a proof of complete instruction coverage. [Official DAC description](https://63dac.conference-program.com/presentation/?id=RESEARCH2804&sess=sess111).

To characterize an operation, vary its inputs and relevant initial state, then observe outputs, exceptions, and permitted state changes. A semantic class is a grouping by behavior. A classifier can suggest such a grouping, but its predicted label cannot replace the underlying observations when assessing a security property.

Classifier accuracy needs its own denominator. Multiple measurements from the same instruction or processor may be highly related. If closely related measurements appear in both training and testing, strong test accuracy may not demonstrate generalization to a new instruction family. Counts of distinct encodings, semantic operations, and individual measurements must therefore remain separate. The available description does not resolve which of these units underlies the reported percentage.

### Discovery, characterization, and security verification are separate gates

An automated campaign may vary instruction encodings, operands, privilege state, register state, memory mappings, exception masks, and surrounding instruction sequences. A candidate is useful only if it executes reproducibly and can be distinguished from an illegal encoding, an alias, undocumented but benign behavior, or an implementation artifact. The observation interface also matters: architectural registers, memory, timing, exceptions, cache state, power, and firmware-visible effects expose different parts of the behavior.

Classification should summarize an observed semantic behavior, not substitute for it. A label such as arithmetic, control-flow, privilege-changing, or memory-accessing needs a defined class ontology and annotation procedure. Report class counts, ambiguous examples, abstentions, confidence calibration, and performance on held-out instruction families or processor models. The 99.8357% figure cannot be interpreted as broad semantic generalization until the unit of prediction, split boundary, class balance, and leakage controls are known.

Security verification asks a still narrower question: does a specific instruction enable an actor to violate a stated property under stated privileges and environmental assumptions? For each of the five reported implications, identify the instruction, attacker capability, precondition, affected asset, reproducible trace, security property, and consequence. A surprising register or timing effect is evidence for investigation; it is not by itself an exploit, vulnerability severity, or cross-processor security claim. Verify the result against a documented reference model or independently reviewed trace, and test whether firmware, operating-system, virtualization, or microcode controls change the outcome.

The discovery denominator must also be explicit. “23 new instructions” could count encodings, operations, processor-specific behaviors, or findings that were not in the authors' prior corpus. “29 classified” may overlap with those 23 or may be a separate set. Report the tested encoding space, stopping rule, duplicate policy, negative cases, processor revisions, and previously known instruction inventory. Compare against constrained discovery and manual semantic analysis under the same execution budget, observation access, and confirmation process. Without these boundaries, the evidence supports an automated candidate-discovery and triage workflow, not complete instruction coverage or a measured security-detection rate.

<span id="explanation-dac-2026-research1628"></span>

## Benchmark shortcuts can obscure what a detector has learned

A benchmark often begins with a design and adds known vulnerabilities. If the original design remains available, comparing the two versions can reveal where changes were made. A text difference can be a useful investigation aid, but identifying changed lines is not the same as explaining why an attacker can violate a property.

The evaluation must specify the intended task. Finding a defect in a known modification and finding a defect in an unfamiliar standalone design require different information. Supplying a known-good version is not intrinsically invalid; it is invalid to score that task and claim the result establishes a capability that does not have such a reference.

[AttackonCTF](../observed-subthemes/hardware-security-validation.md#paper-dac-2026-research1628) rewrites benchmark code to reduce reference-comparison shortcuts while retaining behavior. Section 3.2, PDF page 4, describes Verilator syntax checking and Yosys equivalence checks. Section 4.1, pages 4–5, evaluates 50 injected vulnerabilities in three OpenTitan-based competition benchmarks using Claude Sonnet 4.5 and GPT-5, with three runs per configuration.

Crucially, Section 4.1 defines “detection accuracy” as precision: correct reports divided by all reports. Figures 5–6, pages 5–6, show full-obfuscation D1 recall changing from 83.3% to 54.3%, while precision changes from 67.2% to 15.5%. D4 recall changes from 77.1% to 48.9%, and precision from 69.2% to 15.3%. The conclusion's 55% maximum detection-rate reduction is not reconciled with these endpoints. The paper's stronger interpretation of internal reasoning is an inference, not a directly observed model process. [Version-1 manuscript, Sections 3.2–4.4 and Figures 5–6](https://arxiv.org/pdf/2606.15809v1#page=4).

## Preserving behavior does not establish equal analysis difficulty

Equivalent designs produce the same specified behavior under the equivalence check's assumptions. They can still differ in how easily a reader or detector recognizes the relevant relationships. Removing descriptive names, spreading a condition across expressions, or changing organization can increase analysis effort without changing execution.

Consequently, a detector's decline after a rewrite can support sensitivity to representation without uniquely identifying the cause. Possible contributing factors include retrieval quality, context allocation, localization difficulty, and changed false-positive behavior. Separate experiments are needed to distinguish these explanations. It is too strong to infer a complete absence of reasoning from lower performance alone.

A benchmark transformation also needs two checks that should not be confused. First, the intended vulnerability must remain reachable and demonstrable. Second, the surrounding task must remain suitable for the capability being measured. A syntax pass addresses neither by itself. An equivalence proof supports specified behavioral preservation, but does not directly measure human readability or educational usefulness.

For a concrete metric example, a detector that finds eight of ten known defects has 80% recall. If it issues twenty reports and only those eight are correct, its precision is 40%. Reporting additional incorrect findings can lower precision without changing recall. Overall classification accuracy would also require a defined set of negative cases. These are independently defined measures, not interchangeable uses of the word “accuracy.”

## Synthesis-tool security includes the software that produces hardware

A hardware description language, or HDL, specifies a circuit's behavior and structure. Logic synthesis transforms that description into an implementation representation. A defect in this tool can have several different consequences: the tool may fail, the generated circuit may behave incorrectly, or an input may affect the machine running the tool. A report must identify which boundary is crossed.

[Are They All Safe? Practical Fault Injection Attacks on FPGA Logic Synthesis Tools](../observed-subthemes/hardware-security-validation.md#paper-dac-2026-research2306) presents DefVul-Risk: a defect knowledge base, language-model-generated triggering samples, and a trained model for prioritizing risks. Its official description reports 26 submitted CVE reports and nine confirmations. It supplies neither the identifiers nor tool versions, reproduction conditions, or a measured ranking evaluation. The description emphasizes malicious HDL and toolchain defects; the title should not be interpreted as evidence of voltage or laser fault injection. [Official DAC description](https://63dac.conference-program.com/presentation/?id=RESEARCH2306&sess=sess108).

A triggering sample is useful when it can reproduce a particular failure. Security severity additionally depends on attacker control, required permissions, and consequences. A crash, incorrect synthesis, and unauthorized host access should not be assigned the same meaning simply because each can be triggered by input.

Likewise, report confirmation is not a classifier test set. Some submitted reports may still be pending or may overlap; the fraction confirmed at one time is not automatically precision. Recall requires knowing the relevant defects that were missed, not merely counting discovered cases. A risk-ranking model should be assessed against independently validated severity or reviewer effort under a specified review budget.

<span id="explanation-dac-2026-research2306"></span>

## DefVul-Risk: a triggerable HDL sample is evidence of a tool issue only after semantics and security impact are established

FPGA synthesis is a security boundary between attacker-influenced HDL and a toolchain that emits an implementation. A defect may crash the tool, reject or accept an input incorrectly, change the synthesized circuit, or expose the host running the tool. These outcomes require different oracles and have different security consequences. A generated trigger is therefore a candidate finding, not automatically an exploitable vulnerability.

DefVul-Risk is described as combining a defect knowledge base, LLM-generated triggerable vulnerability samples, and a fine-tuned model that prioritizes high-risk defects. The record does not identify the HDL subset, tool instrumentation, risk labels, model architecture, reviewer workflow, exploitability analysis or whether generated examples are minimized and independently reproduced.

The first gate is synthesis and impact validity. Name the tool and version, preserve the relevant HDL and synthesis settings, minimize the trigger, and distinguish parse/elaboration failure, crash, denial of service, synthesis miscompile, incorrect hardware behavior and host/security boundary violation. Check accepted HDL against an independent behavioral or formal reference, and state attacker access, permissions, preconditions, persistence and consequence before assigning severity.

The second gate is evaluation accounting. Define CVE/report deduplication, confirmation timing, pending and duplicate handling, negative cases and an independently labeled held-out set. Measure precision, recall, ranking quality, coverage by tool/version/vulnerability class, false positives, reviewer time, remediation time and cost under the same assessment budget as manual, fuzzing or static-analysis baselines. The 26 submitted reports and nine confirmations are discovery and coordination outcomes, not a classifier confusion matrix.

The source supplies no identifiers, tool/version matrix, trigger traces, distinct-root-cause rule, precision, recall, exploitability, severity distribution or independent review. The evidence supports LLM-assisted FPGA synthesis-tool vulnerability assessment, not demonstrated exploitability coverage, general synthesis-tool security or secure hardware-production guarantees.

## What connects these papers, and what cannot yet be concluded

All three cases make the source of the expected answer important. Instruction labels, planted benchmark defects, and confirmed tool reports are different reference standards with different blind spots. The shared research direction is to automate candidate generation while preserving a separate, checkable account of behavior and security consequence.

That connection is an analytical synthesis of this sample, not a demonstrated multi-year trend. A stronger comparison would measure validated distinct findings, false reports, reviewer time, and coverage under matched access assumptions. Raw discovery counts and benchmark percentages cannot provide that comparison.

AttackonCTF's recovered manuscript supersedes the old card's missing metric and verification details, but its tools and experiments have not been reproduced here. Manuscripts for the other two records were not recovered. Processor-level evidence, exact CVE mappings, independent review, and checked proof assumptions remain open.
