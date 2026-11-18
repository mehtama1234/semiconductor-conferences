## A model answers a question under assumptions

Architecture exploration compares organizations of computation, storage, and communication before committing to an implementation. A model makes that comparison affordable by representing selected behavior and omitting other details. Its usefulness depends on whether the omitted details could change the decision being made.

An upper-bound model and a candidate-design estimator answer different questions. The first asks how much performance might remain if specified constraints were removed. The second asks how a particular implementable design is expected to behave. An optimistic limit is not a forecast of an actual processor. A favorable design estimate is also not a measured result.

The two records here cover ideal processor modeling and automated design of encrypted-computation accelerators. Neither captured description contains quantitative validation.

## IdealSim: identify the remaining opportunity

[IdealSim](../observed-subthemes/architecture-modeling-and-exploration.md#paper-dac-2026-research690) proposes ideal-scenario modeling for processor upper-bound analysis. Idealization might remove or relax a resource constraint, allowing an architect to ask whether that constraint is worth addressing. The source does not identify its particular idealizations. Unlimited memory bandwidth, perfect prediction, or any other specific assumption must therefore not be attributed to it.

The word “bound” needs a defined scope. A model that omits a delay may produce an optimistic estimate under its remaining assumptions. Establishing a mathematical upper bound on achievable performance requires showing why no allowed implementation can exceed it. The short record does not expose such an argument or the class of implementations to which it would apply.

Bound tightness matters even when validity is established. A very loose limit can rule out little and provide weak guidance among designs. A useful evaluation would compare ideal estimates with progressively more detailed models on common workloads. It would explain which constraints account for the gap.

The architect also needs to know whether a resource improvement is practical. Removing a modeled bottleneck can shift work elsewhere. It can also require area, power, and communication that the ideal scenario does not charge. IdealSim's captured description supplies no bound-tightness, runtime, workload, or calibration results. It supports identifying the analysis purpose, not accepting its estimates as realizable performance.

## Hades: search for an application-specific encrypted-compute design

[Hades](../observed-subthemes/architecture-modeling-and-exploration.md#paper-dac-2026-research912) automates architecture design for fully homomorphic encryption, or FHE, accelerators. FHE permits supported computation on encrypted values. Its implementation has arithmetic and memory requirements determined by the encryption scheme, parameters, and application computation.

Application specialization can focus resources on frequently used operations and their data movement. That also narrows the conditions under which the resulting architecture is useful. A design chosen for one computation or parameter set may behave differently. This can happen when intermediate representations, operation frequencies, or memory requirements change.

The captured source does not expose the search space, cost model, encryption scheme, security parameters, or generated hardware. It should not be assumed to synthesize a complete chip, use a particular optimization algorithm, or support every FHE application. The phrase “design automation” identifies the task, not the completeness of the delivered implementation.

A fair comparison must hold the required computation, numerical accuracy, and cryptographic protection fixed. Only then should it compare latency, area, power, or throughput. Otherwise an apparently cheaper architecture may simply perform a different task or meet weaker requirements. The source supplies none of those numerical results or the conditions needed to interpret them.

<span id="explanation-dac-2026-research690"></span>

## IdealSim: an upper-bound model is useful only when its idealization is named

### What an upper-bound question asks

A processor executes a workload through a sequence of dependent operations. Some operations wait for data, and some wait for a shared resource. Some cannot be overlapped because a later result depends on an earlier one. An upper-bound model removes or relaxes selected constraints. It asks how much performance could remain if those constraints were no longer limiting. This is a diagnostic question: it can indicate where further design effort might help.

It is not the same as predicting a processor that can be built. A prediction must include finite storage, finite bandwidth, arbitration, pipeline state, and control work. It must also include the physical cost of the chosen resources. If an ideal model removes one of these, its result can exceed every design that obeys the omitted constraint. The result is meaningful only after the model states what was removed and what remained.

### The comparison has two layers

IdealSim is described as a methodology for efficient ideal-scenario processor upper-bound analysis. The first layer is the ideal scenario: alter a resource or execution assumption and measure the resulting limit. The second layer is the comparison method: the captured card names cycle-accurate simulation and an analytical roofline model as baselines. These baselines do not answer the same question. Cycle-accurate simulation represents a particular modeled machine over time. A roofline model relates arithmetic work and data movement to resource ceilings. An ideal-scenario result must state which of those details it changes before their numbers can be compared.

For example, suppose the idealization changes memory supply. The result can then reveal whether the modeled workload is limited by data movement under the remaining assumptions. It does not show that supplying that memory bandwidth is affordable. It does not show that the interface can sustain it for all requests. It also does not show that computation and transfer can overlap as assumed. The specific idealizations are not exposed in the captured source, so no particular resource can be attributed to IdealSim.

### A limit must be checked for usefulness and tightness

An upper bound can be valid but too loose to guide a decision. If the limit is far above all feasible designs, it does not distinguish the next useful target. That target could be memory, execution width, control, or communication. A useful evaluation would compare the ideal result with progressively more detailed models. It would show how each restored constraint reduces the gap. It would also test whether the ranking of candidate interventions changes when omitted costs are restored.

The reported record supplies no workload traces, runtime, bound-tightness result, error measure, or calibrated comparison. Its evidence supports the purpose of ideal-scenario analysis, not a numeric claim about processor performance. The phrase “upper-bound performance” must therefore remain a scoped modeling claim until the resource assumptions and validation procedure are available.

### What IdealSim establishes and what remains open

IdealSim establishes an intended analysis function: use idealized processor scenarios to identify remaining performance opportunity before detailed design. It does not establish a mathematical upper bound over all implementations. It does not establish a realizable processor forecast. It also does not establish a measured improvement in a completed workload. A stronger paper-level evaluation would list each relaxed constraint and define the workload and output metric. It would compare against cycle-accurate and analytical references under matched inputs. It would also report the cost of the modeling procedure. Finally, it would test whether its recommendations survive detailed simulation or implementation.

[Official DAC description, record RESEARCH690](https://63dac.conference-program.com/presentation/?id=RESEARCH690&sess=sess109)

<span id="explanation-dac-2026-research912"></span>

## Hades: application-specific FHE hardware must preserve the cryptographic task

### Encrypted computation changes the cost of an operation

Fully homomorphic encryption, or FHE, lets a computation operate on encrypted values. An untrusted executor then need not receive the plaintext inputs. The ciphertext is not usually a compact copy of the plaintext. Its operations carry extra algebraic structure and may produce intermediate state that grows or becomes noisier as the circuit proceeds. Some schemes require a refresh or bootstrapping operation to continue computation within the allowed error conditions.

An FHE accelerator therefore handles more than the application’s visible arithmetic. It must represent ciphertext components and move them through memory. It must perform scheme-specific polynomial or modular operations and manage intermediate storage. It must also preserve the cryptographic parameters that define the security and correctness target. A hardware design that reduces one arithmetic kernel can still lose at memory movement, bootstrapping, control, or result recovery.

### The design flow begins with the application circuit

Hades is described as architecture design automation for application-specific FHE accelerators. The natural decision sequence is as follows. Identify the application circuit. Determine the encryption scheme and parameters. Count the resulting operation types and intermediate values. Choose arithmetic units and storage. Then check whether the generated organization meets the required computation and protection level. Specialization can remove hardware for operations that never occur or allocate more resources to operations that dominate the selected circuit.

That specialization creates a validity boundary. A design optimized for one circuit, ciphertext size, modulus, security parameter, or bootstrapping frequency may not remain efficient. This applies when any of those change. The search must therefore expose which application and cryptographic parameter set it used. The evaluation must also include the cost of generating and checking the design. The captured source does not identify the search space, cost model, scheme, security parameters, or generated hardware.

### Security is a fixed constraint, not a quality score to trade away silently

Latency, area, power, and throughput can be compared only under certain conditions. The encrypted computation must first have the same required output and security conditions. Lowering a modulus, reducing ciphertext precision, or changing the number of operations may reduce hardware work. Using a weaker parameter set may do the same. Each of these may change the cryptographic task. Such a result cannot be called a faster implementation of the original task. This requires showing equivalence of the protection and correctness requirements.

The source names general-purpose FHE accelerators and CPU/GPU FHE as comparison categories. However, it supplies no numeric PPA, latency, throughput, circuit, security-parameter, or application results. These baselines therefore identify the intended comparison boundary, not measured reference values.

### What Hades establishes and what remains open

Hades establishes the design-automation problem of specializing an accelerator around an FHE application and its encrypted arithmetic. It does not establish a completed chip, a universal FHE architecture, a specific search algorithm, or a performance/security improvement. A stronger evaluation would publish the scheme and parameters, application circuits, and generated architecture. It would publish memory and bootstrapping accounting, search budget, and baseline implementations. It would also publish cryptographic correctness checks and PPA and latency measurements. Finally, it would publish transfer results on circuits not used to specialize the design.

[Official DAC description, record RESEARCH912](https://63dac.conference-program.com/presentation/?id=RESEARCH912&sess=sess109)

## Validate the decision, not only the prediction

For IdealSim, validation should establish what the claimed limit means and whether it helps identify worthwhile design changes. For Hades, validation should show that selected designs remain preferable when checked with a more detailed implementation model. Low average prediction error alone would not prove good design selection if errors reverse the ranking of the best candidates.

Both evaluations should count model construction, search, failed candidates, and final checking. Reuse can spread preparation cost over many decisions, but that reuse must be demonstrated for the intended workloads. These records motivate a shared research question: how can inexpensive models guide decisions whose benefits survive physical and application constraints? They do not yet establish that either modeling approach yields better completed hardware. They also do not establish that the two approaches have been integrated.
