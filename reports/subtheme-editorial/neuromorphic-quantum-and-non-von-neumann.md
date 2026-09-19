## Different physical systems require different definitions of a correct answer

This grouping combines eight papers, but it does not describe one computing architecture. Some propose circuits whose electrical or optical behavior performs part of a calculation. Others generate classical control hardware, maintain a quantum device, compile error-correction circuits, or simulate superconducting gates. Their common concern is the relationship between an abstract operation and a physical implementation. Their correctness requirements are not interchangeable.

A numerical solver can permit a stated approximation error. A cryptographic hash must implement its specified discrete function. A quantum controller must issue the right signal at the right time. An error-correction schedule must preserve the intended checks while respecting device constraints. A simulator must predict relevant physical behavior well enough to support its claimed use. Calling all of these systems “non-von Neumann” does not explain those differences.

Three full manuscripts were inspected for this pass: RISC-Q, NeuroPDE, and the NEAT PDF linked by an author's publication list. NEAT's PDF still has anonymous-author and placeholder publisher metadata; the author-hosted association supports its identity, not equivalence to a final published version. Four other DAC papers remain description-backed. The ICCAD qudit paper remains supported by institutional and author abstracts. The two ICCAD records are explicitly from the 2025 fallback edition, not DAC 2026.

| Technical branch | Papers | What the evidence must establish |
|---|---|---|
| Physical numerical computation | NeuroPDE; analog flow-generation solver | Error, sampling or training cost, circuit assumptions |
| Optical arithmetic and logic | PhotoMT; Bident | Exact arithmetic or valid logic, optical loss, total supporting cost |
| Classical quantum control | RISC-Q; active calibration | Signal timing, feedback delay, drift and maintenance cost |
| Quantum compilation and device modeling | NEAT; qudit simulation | Valid schedules or accurate models under stated noise |

The explanations below distinguish reported observations from conceptual reasoning and proposed tests. Hardware simulation, a generated design, a public repository, and a measured device are separate evidence states.

### Start with the computation, before choosing the hardware

A computing system accepts an input, represents it internally, changes that representation through a sequence of operations, and produces an output. To judge a proposed design, we must specify all four parts. Saying that a circuit is analog, optical, or quantum does not yet tell us what input it accepts or what answer it must produce.

Consider the difference between estimating a numerical value and calculating a hash. For an estimate, an output of 0.499 might be acceptable when the reference is 0.500, if the application permits an absolute error of 0.001. For a hash, the requirement is equality with the specified discrete output; closeness of the underlying voltage is not the definition of correctness. These are illustrative requirements, not measurements from the papers. They explain why the same physical noise can be tolerable in one computation and unacceptable in another.

Next ask what physical quantity carries the value. In a digital circuit, allowed voltage ranges encode discrete states. In an analog circuit, the voltage or current itself can represent a numerical magnitude. A stochastic circuit can represent a transition probability through how frequently a device produces an outcome across repeated trials. None of these choices eliminates representation: each defines a different relationship between physical behavior and the value the algorithm uses.

Then identify the operation that the device performs. A resistance can weight a current, but a complete numerical algorithm may also need to select inputs, accumulate values, apply a nonlinear rule, repeat a step, and decide when to stop. If only the weighting operation moves into a new circuit, the other operations remain part of the system. Their cost can determine whether the complete calculation becomes faster.

Finally, follow the output back to the requirement. A numerical result needs an error measurement. An exact discrete calculation needs a reference-output check. A controller needs a correctly timed signal, not merely the correct instruction in memory. A device model needs agreement with the physical quantities it claims to predict. This sequence—input, representation, operation, output check—is the basis for comparing the branches below. It is conceptual analysis, not a claim that all eight papers implement the same process.

### Why a faster component may not produce a faster application

Suppose an illustrative computation spends 30 milliseconds preparing input, 60 milliseconds in the operation being accelerated, and 10 milliseconds reading and checking the result. Its total is 100 milliseconds. Making the middle operation ten times faster reduces it to 6 milliseconds, so the new total is 46 milliseconds: the application improves by about 2.17 times, not ten times. If the new hardware also requires 20 milliseconds of additional conversion, the total becomes 66 milliseconds and the improvement falls to about 1.52 times. These numbers are a worked example, not a paper result.

The same accounting applies when the extra cost is repeated sampling, device programming, signal conversion, calibration, or schedule compilation. Preparation performed once can be shared across many uses, but only if the prepared state remains valid. A comparison therefore needs both the cost per use and how often preparation must be repeated. This is why the individual paper discussions separate an internal operation from the complete task.

## Physical numerical computation: use device behavior, then account for its error

A differential equation describes how a quantity changes. A partial differential equation can involve changes across several independent variables, such as position and time. To obtain a numerical answer, a solver also needs an initial state, boundary conditions, and a rule for representing the unknown values. The same equation with different boundaries is a different computational problem.

Digital arithmetic approximates these quantities using finite numerical representations and finite operations. Analog circuits instead allow a continuously varying electrical quantity to represent part of the state. That does not make the answer exact. Device variation, noise, finite settling time, limited dynamic range, and input/output conversion can all affect it. A faster internal circuit is useful only if the complete output still meets the required error level.

<span id="explanation-iccad-2025-130"></span>

### NeuroPDE: perform probabilistic transitions with stochastic devices

#### The missing connection: how can random choices calculate an answer?

A numerical solver starts with a rule relating unknown values, together with enough specified values or other conditions to determine a solution. Random choices are useful only when their average produces the quantity required by that rule. Randomness is not a replacement for formulating the problem.

Here is a deliberately small mathematical example, not a NeuroPDE experiment. Consider five equally spaced positions numbered 0 through 4. The values at the ends are fixed: position 0 has value 0, and position 4 has value 100. At each interior position, require the unknown value to equal the average of its two neighbors. Writing `u1` for the value at position 1 gives:

```text
u1 = (0 + u2) / 2
u2 = (u1 + u3) / 2
u3 = (u2 + 100) / 2
```

The solution is 25, 50, and 75 at positions 1, 2, and 3. Substitution checks it: for example, `(25 + 75) / 2 = 50`. This is the discrete steady diffusion equation with fixed end values and no internal source. “Discrete” means we represent the domain by these selected positions; “steady” means the required values are no longer changing with time.

Now start a sampled path at position 1. At each interior position, choose left or right with equal probability. Stop when the path reaches either end and record that end's value. One path returns either 0 or 100, which is usually not the answer 25. The estimate comes from averaging the values returned by many paths starting at the same position.

Why should that average solve the equations? Let `m1`, `m2`, and `m3` be the expected final values from the three interior starting positions. “Expected” means the probability-weighted average over possible outcomes. From position 1, half the first steps go straight to value 0; half go to position 2, whose expected final value is `m2`. Therefore `m1 = (0 + m2) / 2`. The same first-step reasoning gives the other two equations above. The expected endpoint values satisfy exactly the required equations. That is the connection between random paths and this numerical answer.

This finite, unbiased walk eventually reaches an endpoint with probability one. Solving the equations also shows that a path starting at position 1 reaches the 100-valued end with probability one quarter. If a particular set of 100 paths reaches that end 27 times, its estimate is `27 × 100 / 100 = 27`, an absolute error of 2 from the reference 25. The 27 outcomes are illustrative, not observations or a guaranteed count.

Changing the equation can require different transition probabilities, accumulated contributions along the path, or different stopping rules. The example explains the basic connection; it is not the paper's complete formulation and does not show that every partial differential equation has this simple endpoint estimator.

#### What changes when a circuit makes the random choice?

An ordinary implementation can store the current position, generate a pseudorandom number, select a transition, update the position, and record a contribution. Pseudorandom numbers come from a deterministic algorithm with a changing internal state. Their suitability depends on the statistical requirements of the computation, not on whether they are physically random.

NeuroPDE instead represents position by an active circuit neuron. Its ferroelectric tunnel-junction resistance sets a voltage that controls magnetic tunnel-junction switching probability. The activation cycle reads the current neuron, attempts neighboring activation, stops writing after a switch, and resets the original neuron. [Section III, PDF pages 3–4, Figures 3–6](https://arxiv.org/pdf/2507.04677v1#page=3).

Here “neuron” names a circuit element representing a state. It does not mean the solver learns the answer from examples. A magnetic tunnel junction has a resistance related to the relative magnetic orientation of two layers. A ferroelectric device retains an electrically programmable polarization state that can change its resistance. The computational use of these devices depends on the relationship between the stored setting and the resulting transition probabilities.

Why must the old state reset? A single walker has one current position. Leaving the old position active while also activating the new position would no longer represent that same single-walker process. Why stop competing activation? Activating both destinations would likewise change the process being simulated. These requirements follow from the representation; circuitry that enforces them is part of the computation, not optional supporting detail.

Hardware-intrinsic randomness means the physical device supplies a random outcome. It does not mean every physical setting supplies the probability the equation needs. The relevant check is the measured frequency of each valid transition under the actual programming and operating conditions, including invalid or simultaneous state activations.

#### Separate sampling error from an incorrectly implemented probability

Return to the five-position example. If the hardware moves right more often than left, it will reach the 100-valued boundary more often. More paths then make the estimate more consistent around the answer to the wrong transition rule. Repetition reduces uncertainty about that biased result; it does not restore the intended equal-probability process.

For independent paths with unchanged outcome variance, the standard deviation of their mean decreases in proportion to `1 / sqrt(N)`, where `N` is the number of paths. Consequently, halving this sampling uncertainty requires about four times as many paths. Correlation between paths can invalidate that simple calculation. Device mismatch and a fixed error in a programmed probability are different issues from independent sampling noise.

Discretization is another separate approximation. A perfectly implemented random walk on a coarse grid can accurately solve the grid equations while remaining an inadequate approximation to the continuous problem. An evaluation must identify whether it is measuring circuit behavior, error against the discrete solution, or error against the original continuous solution.

#### What was evaluated, and what do the numbers mean?

The evaluation uses SPICE circuit simulations and Python system simulation, with a 45 nm generic process kit at 300 K. The reported 10 ns and 1.451 pJ concern the paper's single-walk operation, not a complete PDE solution. Equation 10 defines squared error from the analytical result, despite calling it variance. Temperature-induced drift is outside the study. [Sections IV–V, PDF pages 4–8; Equation 10 and Figure 12 on PDF page 7](https://arxiv.org/pdf/2507.04677v1#page=7).

Squared error and statistical variance answer different questions. If a computed value is 27 and its reference is 25, its squared error is `(27 − 25)² = 4`. To estimate variance, repeat the computation and measure the spread around its own average. A method that repeatedly returns 27 can have small variance while remaining systematically wrong. The units of squared error are also squared; a threshold for it is not automatically a threshold for relative or percentage error.

A circuit simulator computes electrical behavior from component models. A system simulator then evaluates the larger algorithm under modeled behavior. Neither is a measurement of a fabricated complete solver. The model can test a design idea, but its conclusions inherit the accuracy and range of the component models and the way circuit results enter the system simulation.

#### How to compare complete solvers fairly

Start with the same equation, domain, boundary conditions, output locations, and error requirement. Count how many paths and transitions are required, not just the cost of one primitive operation. Include programming the device states, initializing paths, detecting and recording outcomes, accumulating the estimate, and checking the result. Account for concurrency explicitly; multiplying every operation by its individual latency can overestimate elapsed time when operations overlap.

Then repeat enough complete runs to distinguish bias from sampling spread. Vary the grid resolution separately from the path count. Compare with an appropriate digital solver at the same accuracy target, including a deterministic numerical method when it is suitable; a comparison only against other random-walk hardware does not establish the best way to solve the equation.

The contribution under investigation is a cheaper physical implementation of specified probabilistic transitions. Establishing a faster complete numerical solution requires the additional accounting above. [The evidence record](../observed-subthemes/neuromorphic-quantum-and-non-von-neumann.md#paper-iccad-2025-130) retains the recovered source conditions and unresolved limits. No independent execution or new hardware result is claimed here.

<span id="explanation-dac-2026-research1016"></span>

### Analog flow generation: integrating a learned model is not automatically solving the physical equations

#### First specify what is being generated

A fluid velocity field assigns a velocity to each position in a domain. In a two-dimensional representation, each sampled position may have two values: velocity along one spatial direction and velocity along the other. A sequence of such fields can represent physical evolution over time. A generator may instead produce a single field, or samples conditioned on specified inputs. Those are different tasks and need different tests.

A conventional physical solver applies governing equations together with initial conditions, boundary conditions, and material or flow parameters. A learned generator uses fitted parameters to produce outputs according to patterns learned from data. It can be designed to respect physical constraints, but that property must be established rather than inferred from a fluid-related training dataset.

The paper proposes an MLP-Mixer model, an RRAM continuous-time neural ODE circuit, and noise-aware training with decoder retraining. Its description reports three turbulent-flow datasets and energy/latency reductions of 98.24%/99.99% against an A100. Dataset identities, conditioning inputs, precision, physical realization, and complete comparison boundaries are not specified. [Official DAC description](https://63dac.conference-program.com/presentation/?id=RESEARCH1016&sess=sess139).

The input/output distinction is therefore partly unresolved for this record. The following explanation describes the relevant computational structure without inventing its dataset, circuit dimensions, or operating conditions.

#### Two meanings of flow, and three meanings of time

Flow matching learns a rule that transports samples from an initial distribution toward a target distribution. A distribution describes which sample values are likely. The learned rule tells each current sample how to change as generation progresses. Training fits that rule to target changes associated with a chosen probability path. [Flow Matching for Generative Modeling](https://arxiv.org/abs/2210.02747).

The word “velocity” in this model can mean the rate at which a vector of internal values changes. It need not mean the physical velocity of a fluid particle. The vector might eventually decode into fluid velocities, but the internal change rule and the final physical quantities are different objects.

It helps to give the three time variables separate names. Physical time describes the fluid's evolution, if that is part of the task. Generation progress, often normalized from 0 to 1, describes movement through the learned transformation. Circuit time is how long the electrical implementation runs. One generated field could describe one physical instant while requiring an entire generation trajectory and some elapsed circuit time to produce it.

Running that electrical trajectory faster does not mean that the system simulates more physical seconds per second unless the benchmark explicitly defines and measures that relationship. It first means the implementation takes less wall-clock time to execute the specified learned transformation.

#### What a neural ordinary differential equation supplies

An ordinary differential equation specifies a rate of change with respect to one independent variable. For a neural ODE, a neural network supplies that rate. In compact notation, `dz/ds = f(z, s)`: `z` is the current internal state, `s` is generation progress, and `f` gives the proposed change at the current state and progress. “Latent” means this internal representation is not necessarily the final output representation. A decoder converts it into output values.

As a minimal mathematical example, start with `z = 1` at `s = 0` and use the constant change rule `dz/ds = 2`. At `s = 1`, the answer is 3. A simple digital calculation with four steps of size 0.25 produces `1, 1.5, 2, 2.5, 3`. It happens to be exact for this constant rule; a general state-dependent rule can introduce numerical integration error. This example is neither a trained flow-matching model nor a paper experiment.

There are two distinct sources of discrepancy. The learned function may not describe the desired transformation accurately. Separately, the hardware or numerical solver may fail to follow that learned function accurately. A perfect implementation of the wrong learned function does not repair the model; a good model executed inaccurately does not preserve its software result.

#### Why a mixer architecture is relevant

An MLP, or multilayer perceptron, alternates learned weighted combinations with nonlinear transformations. The original MLP-Mixer separately mixes information across input positions and across feature channels. A channel is one component of the representation at a position. This gives two kinds of learned interaction without requiring the attention mechanism used by a Transformer. [Original MLP-Mixer paper](https://arxiv.org/abs/2105.01601).

Weighted combinations are candidates for resistive-array computation. That does not imply that the complete network consists only of matrix multiplication. Nonlinear operations, offsets, normalization if present, state feedback, and final decoding must also be implemented or accounted for. The exact mixer adaptation in this fluid-generation paper remains a full-text question.

#### How an electrical circuit can implement a changing state

Resistive memory stores a programmable conductance, the reciprocal of resistance. In an ideal linear device, applying voltage V produces current `I = G × V`, where G is conductance. Summing currents from several devices can produce a weighted sum. Real devices and interconnects depart from this ideal, so the desired numerical function and the measured electrical function must be compared.

An integrator accumulates the resulting rate into a state. For a capacitor, `dV/dt = I/C`: current changes its voltage at a rate set by capacitance. With an ideal 1 nanofarad capacitor and constant 1 microampere current, the voltage changes by one volt in one millisecond. This elementary circuit calculation illustrates integration; it is not the paper's component sizing or speed.

To implement a neural ODE, the stored state influences the network's output, and that output drives changes to the state. This feedback closes the computational loop. Scaling between numerical values and voltages, and between generation progress and circuit time, determines what electrical parameters are required. Finite voltage range and circuit bandwidth limit the scaling; it cannot be increased without considering accuracy and stability.

A related paper by overlapping authors explicitly uses resistive-array neural computation with feedback integration for score-based generation. Its task and title differ from this DAC paper. Its device realization and benchmark numbers are not transferred here. [Related circuit background, Introduction](https://www.nature.com/articles/s41467-026-72900-z).

#### Continuous operation changes the error sources; it does not eliminate error

An analog circuit can evolve without the sequence of discrete arithmetic updates used in a digital integrator. It can still have programmed-weight error, offsets, noise, limited gain, finite response speed, and imperfect initialization. These affect the trajectory being computed.

For the constant-rate example, suppose the circuit implements 2.1 rather than the intended rate 2. Starting from 1 and running to generation progress 1 then produces 3.1 instead of 3. Making the measurement more precise will reveal this difference, not remove it. For state-dependent dynamics, an early error can affect subsequent rates as well, so the final discrepancy need not equal a simple sum of independent errors.

Noise-aware training exposes the model to a chosen noise model during optimization. Decoder retraining changes how internal states are mapped to final outputs. Either can improve results under the conditions used for training. Neither establishes robustness to arbitrary temperature changes, device aging, programming errors, or a different noise distribution. Testing new devices and held-out operating conditions addresses a different question from fitting the training setup.

#### Evaluate the right kind of accuracy

For a deterministic prediction with a specified reference, pointwise velocity error can be meaningful. For a generator that intentionally produces multiple possible fields, a different sample need not be an incorrect sample. Evaluation may need distributional statistics and diversity as well as agreement with physical constraints. A visually plausible field is not enough, but insisting that every valid random sample equal one reference is not generally the right requirement either.

The benchmark should state what is conditioned on and which outputs are valid under that condition. If it claims incompressible flow, test the relevant mass-conservation constraint; if it claims boundary-conditioned generation, test those boundaries. If it claims physical time evolution, test temporal consistency and the specified dynamics. Do not require or claim properties the task never defines.

Separate software-model error from the extra error introduced by analog execution. Hold architecture and training data fixed when testing the hardware effect, then evaluate any noise-aware retraining as an additional intervention. New geometries, flow regimes, or boundary conditions require evidence of their own.

#### Read the reductions as ratios with unresolved boundaries

A 98.24% energy reduction means 1.76% of the comparison energy remains within the measured boundary. A 99.99% latency reduction means 0.01% of the comparison latency remains. Such rounded percentages cannot establish precise complete-system speedups when the reference durations and included operations are unavailable.

The comparison needs training and programming policy, input initialization, integration, conversion, decoding, and output handling. Costs paid once should be separated from costs paid for every sample, with the number of uses stated. Identical quality targets matter: a fast inaccurate sample and a slower accurate sample do not establish an accuracy-matched acceleration.

Fresh author and topic searches found related analog generation work, but not a matching full manuscript for the DAC fluid-generation record. The [paper evidence card](../observed-subthemes/neuromorphic-quantum-and-non-von-neumann.md#paper-dac-2026-research1016) remains description-backed. The related Nature Communications paper is useful technical context, not a recovered final version of this work. Dataset-level claims, actual circuit conditions, artifact execution, and complete-system accounting remain open.

## Optical computation: light transport does not remove the representation problem

Optical circuits can combine signals while they propagate. The resulting intensity or phase must still represent the desired mathematical quantity. Loss reduces signal strength, and uncertainty affects how reliably the output can be interpreted. The source, modulation, detection, conversion, control, and memory costs belong in an application comparison.

<span id="explanation-dac-2026-research2293"></span>

### PhotoMT: accelerate hash-tree construction, not every part of a proof

#### What is the required output?

A cryptographic hash maps an input to a fixed-size output according to a specified algorithm. Different inputs can share an output because the output space is finite; the security requirement is that finding useful collisions should be computationally infeasible under the stated assumptions. A Merkle tree hashes groups of values repeatedly to produce one root. An inclusion proof supplies the intermediate values needed to connect one entry to that root. The verifier must already have an authenticated or otherwise trusted root; a supplied root is not trustworthy merely because it is a hash. [A concrete tree and inclusion-proof specification: RFC 9162, Sections 2.1.1–2.1.3](https://www.rfc-editor.org/rfc/rfc9162.html#section-2.1).

The tree does not itself hide its input values or establish a general privacy guarantee. Zero knowledge is an additional property of a proof protocol: the verifier should learn that an assertion holds without learning the private information used to establish it beyond what the assertion reveals. A tree may be one component of such a protocol. Faster tree construction is consequently not the same measurement as faster complete proof generation.

#### Follow an eight-leaf construction

The following is a structural example, not PhotoMT's reported tree configuration or a cryptographic implementation. Assume eight leaf hashes L0 through L7 are already available. Let `H(left, right)` denote the specified internal-node hash, with unambiguous encoding and ordering. The required intermediate nodes are:

```text
P0 = H(L0, L1)       P1 = H(L2, L3)
P2 = H(L4, L5)       P3 = H(L6, L7)
Q0 = H(P0, P1)       Q1 = H(P2, P3)
root = H(Q0, Q1)
```

There are seven internal hashes: four at the first level, two at the next, and one at the root. The four first-level hashes do not depend on one another, so hardware can potentially calculate them concurrently. Q0 must wait for P0 and P1, and the root must wait for both Q0 and Q1. More arithmetic units do not remove these dependencies. The example excludes the cost of computing the eight leaf hashes.

To check the inclusion of L2 at its stated position, a verifier needs L3, P0, and Q1. It computes P1 from L2 and L3, then Q0 from P0 and P1, then the root from Q0 and Q1. It compares that result with the trusted root. The verifier performs three internal hashes without recomputing the whole tree. Correct left/right ordering is essential; silently sorting pairs changes the specified construction.

Real schemes also specify how leaf hashes differ from internal-node hashes, how values are encoded, and how an incomplete last level is handled. Those rules are part of correctness. The schematic above explains dependencies, not permission to substitute an arbitrary encoding into a deployed proof system.

#### What work does PhotoMT move into optics?

The official description assigns matrix-vector multiplication to photonic microring arrays and control-intensive work to digital circuits. It adds multi-subtree interleaving and an S-box bypass queue. It reports 18.8–20.5× throughput over specialized ASIC designs and energy-efficiency gains of three to five orders of magnitude over a CPU. Exact parameters and the full experimental accounting are unavailable. [Official DAC description](https://63dac.conference-program.com/presentation/?id=RESEARCH2293&sess=sess174).

A matrix-vector multiplication produces several weighted sums. For example, one output may be `2 × x + 3 × y`; another can use different coefficients with the same input values. Optical hardware can potentially perform such signal weighting and combination while electronic hardware handles sequencing and storage. Whether that division is beneficial depends on input representation, conversion, device control, and how much of the hash actually consists of the accelerated operation.

A microring resonator is a small closed optical path coupled to other optical paths. Its wavelength-dependent transfer behavior can be used in optical signal processing. [Device background: Bogaerts and colleagues, Sections 1–2, PDF pages 1–2](https://www.photonics.intec.ugent.be/download/pub_3105.pdf#page=1). The PhotoMT description does not specify enough to reconstruct its complete numerical encoding, calibration procedure, or exact-output recovery. It would be incorrect to supply a familiar optical-neural-network implementation and label it as this paper's design.

#### Why approximate arithmetic is a central verification issue

Poseidon maps sequences of elements from a specified finite field to field-element outputs. The field and security parameters help determine the required configuration. Its S-box is a nonlinear arithmetic transformation; a common supported choice is raising an element to the fifth power in the field. [Poseidon authors' parameter and reference-implementation page](https://www.poseidon-hash.info/).

For a small arithmetic illustration, use integers modulo the prime 7: the allowed values are 0 through 6, and an arithmetic result is reduced to its remainder after division by 7. With `x = 4` and `y = 5`, the weighted sum `2 × x + 3 × y` is 23, whose field value is 2. A different recovered integer, 24, has field value 3. This tiny field is not a secure Poseidon parameter choice or a PhotoMT experiment. It makes the exactness requirement explicit.

An internal analog signal need not itself be exact if a demonstrated decoding rule reliably recovers the exact discrete value. For instance, in an idealized direct-integer encoding, nearest-integer decoding tolerates an error strictly below one half of the spacing between adjacent encoded integers. That statement depends on the encoding scale, range, rounding rule, and absence of other errors. It is not a claimed error bound for the optical engine.

The complete implementation must establish the corresponding bound or correction method for its actual representation. It must also account for finite range, accumulation, field reduction, and nonlinear operations. A small average numerical error does not establish that every hash result is correct. A single wrong internal value can produce a root different from the reference and cause an otherwise valid proof to be rejected.

These are obligations of an exact arithmetic implementation, not evidence that PhotoMT fails them. The available description leaves the relevant mechanism and tests unresolved.

#### Why interleaving independent subtrees can help

In the eight-leaf example, parallelism decreases as computation approaches the root: four available hashes become two, then one. If a hardware pipeline can accept a new hash before an earlier one finishes, it still needs ready inputs for that new hash. A dependent parent cannot be submitted before its children are available.

Work from another independent subtree or another tree can fill some of the resulting gaps. Interleaving therefore changes which ready work enters the hardware next; it does not remove the original dependencies. The general tradeoff is extra live state: partial results, identifiers, and ordering information must remain available until each parent can be formed.

More interleaving is not automatically better. If storage or data transfer becomes the limiting resource, keeping more trees active can increase waiting. A throughput comparison should identify tree size, number of concurrent trees, input arrival pattern, memory capacity, and whether it includes the initial filling and final draining of the hardware pipeline.

The name “S-box bypass queue” is not a sufficient implementation description. A bypass is correct only when it avoids work that the specified algorithm does not require on that path, or implements an equivalent transformation. It cannot simply omit a required nonlinear step while claiming the same hash. Which data bypass which operation, and under which Poseidon rounds, remains a full-text question for this paper.

#### Read throughput and energy with the same boundaries

Throughput counts completed outputs per unit time under a sustained workload. Latency measures the elapsed time for a particular request. Interleaving can improve the first without improving the second by the same factor. The throughput result also needs an output definition: hashes, complete trees, and complete proofs are different units of work.

Energy per output must include the components inside the claimed comparison boundary. For a photonic-electronic system, the relevant accounting questions include optical sources, signal conversion, electronic control, memory traffic, and device stabilization. A comparison using only optical computation energy cannot be read as whole-system energy without additional evidence.

The description uses different comparators for throughput and energy efficiency. Combining those gains into a claim that one measured system simultaneously achieves both advantages over the same baseline would exceed the source. The implementation stage—modeled, synthesized, prototyped, or fabricated—also needs to be established rather than inferred from the word “experiments.”

#### What is recoverable now, and what remains to verify?

Fresh name and author searches found the official program entry but no matching full manuscript or artifact. The [paper evidence record](../observed-subthemes/neuromorphic-quantum-and-non-von-neumann.md#paper-dac-2026-research2293) therefore remains description-backed. The external Poseidon and tree specifications explain the underlying requirements; they do not document PhotoMT's implementation.

A reproduction should first match full hashes and roots against a versioned reference with identical parameters and encodings. It should then test independent subtrees and dependent parent updates, including conversion limits and any retry or correction. Finally, measure complete-tree latency, sustained throughput, and total energy at the same correctness requirement. Only a separate complete-proof experiment can establish how much this component changes proof-generation cost.

<span id="explanation-dac-2026-research1268"></span>

### Bident: optimize how optical signals are combined

#### The required logic result comes before the loss score

An optical logic circuit represents logical values through physical optical signals. To implement a specified function, the output signals must remain distinguishable under the receiver's decision rule. A smaller power loss is useful when it helps preserve that distinction or reduces the required input power. It is not, by itself, proof that the circuit computes the right Boolean function.

For example, suppose an illustrative receiver treats output power above 0.5 units as logical 1. If a valid input pattern should produce 1 but reaches the receiver at 0.49, that implementation fails the specified decision rule. Raising the result to 0.51 may fix this one nominal case, but it leaves only 0.01 units of margin. Device variation or input uncertainty can still matter. These are hypothetical values, not Bident measurements or a proposed universal optical threshold.

Logic synthesis chooses an implementation of a required logical function. For optical logic, the physical signal behavior must constrain that choice. Otherwise, a logically valid arrangement of ideal gates may not produce reliably distinguishable signals after it is implemented.

#### Why tree structure changes the loss of each input

A binary combiner accepts two incoming paths and supplies an outgoing path. Combining more inputs requires several such elements. A tree records which paths combine first and which combinations occur later. A leaf is an original input; an internal node is a combining operation; the root is the final output.

Consider four inputs. A balanced arrangement combines inputs 1 and 2, combines inputs 3 and 4, then combines the two results. Every input passes through two combining stages. An unbalanced arrangement can give one input a one-stage path, another a two-stage path, and the remaining two three-stage paths. Both arrangements contain three internal combiners. Equal component count therefore does not imply equal paths or equal loss for each input.

For a deliberately simplified single-active-input calculation, assume each traversed stage delivers 80% of the incoming power to the required output path, independent of signal level. Two stages deliver `0.8 × 0.8 = 0.64` of the initial power; three deliver `0.8³ = 0.512`; one delivers 0.8. The retained fractions multiply rather than adding. Giving an input a shorter path changes its delivered power even when no combiner is removed.

This calculation excludes simultaneous-input interference, wavelength dependence, reflections, and layout loss. When optical fields combine coherently, their relative phase can reinforce or cancel the resulting field; simply adding independently computed powers can then be wrong. The toy calculation explains cumulative path attenuation, not the complete binary aggregate model claimed by Bident.

#### What the paper says it changes

Bident's official description proposes a binary aggregate model that accounts for topology and input ordering. It uses Huffman-based optimization for Y-branch trees and greedy leaf-level directional-coupler selection, with claims about optimality, harmonic-mean efficiency, and hardware cost. It reports schematic-level optical simulation but no numerical attenuation or cost table. [Official DAC description](https://63dac.conference-program.com/presentation/?id=RESEARCH1268&sess=sess172).

A Y-branch joins or separates optical paths through a branching geometry. A directional coupler transfers optical power between nearby waveguides through their interaction. These are physical components with transfer properties, not interchangeable cost-free tree nodes. Selecting the tree and selecting its components can therefore be related but distinct decisions.

The required input to such an optimization includes the logical function, allowed component types, and the parameters used to predict their behavior. The output is a configuration that can be checked against the model. The recovered description does not provide enough detail to reconstruct all these inputs, the loss equations, or the exact allowed transformations.

#### What Huffman optimization means—and what it does not prove here

For the standard binary weighted-path problem, each leaf has a nonnegative weight and a depth. The objective is the sum of `weight × depth`. Huffman's construction repeatedly combines the two smallest remaining weights and replaces them by their sum, producing an optimal tree for that objective. Its original application minimizes average encoded message length. [Huffman's original paper, pages 1098–1101](https://web.stanford.edu/class/ee398a/handouts/papers/Huffman%20-%20Min%20Redundancy%20Codes%20-%20IRE52.pdf).

Here is a small calculation of that objective, not Bident's optical model. Give four leaves weights 8, 4, 2, and 1. Combine 1 and 2 to obtain 3, combine 3 and 4 to obtain 7, then combine 7 and 8. The original leaves have depths 1, 2, 3, and 3 respectively. Their weighted total is `8×1 + 4×2 + 2×3 + 1×3 = 25`. A balanced depth-two tree has total `2×(8+4+2+1) = 30`.

This shows why a balanced tree is not always best for a weighted objective. It does not show that assigning optical inputs those same weights minimizes physical attenuation. That requires a derivation connecting the physical model to the mathematical objective. The phrase “Huffman-based” identifies an algorithmic connection; it does not supply the missing derivation or extend its theorem to arbitrary optical layouts.

Likewise, an objective that minimizes average loss can differ from one that protects the weakest input. An input with a small weight can be placed deep in the tree while contributing little to the average cost. If every valid logical input must remain above a threshold, the worst-case constraint still matters even when an average objective improves.

#### Why an efficiency average needs a definition

For positive efficiencies, the harmonic mean is the reciprocal of the average reciprocal efficiency. With efficiencies 1 and 0.25, it is `2 / (1/1 + 1/0.25) = 0.4`; the ordinary arithmetic mean is 0.625. The two summaries weight poor efficiencies differently. Neither is automatically the correct objective for every optical system.

The description's harmonic-mean claim therefore needs the precise definition of the efficiencies being combined, their weights, and the reason that statistic matches the intended physical or resource objective. Without those details, replacing the harmonic mean with an ordinary average—or calling either one a guaranteed logic-success rate—would change the claim.

A greedy algorithm selects a locally preferred next action. It can be globally optimal when the problem has the required mathematical structure. It can also miss better combinations in a different problem. Bident's description claims optimal leaf-level selection, but the proof and its allowed choices must be inspected before extending that result beyond the stated model.

#### From a schematic to a physical implementation

A schematic-level simulation connects modeled components and evaluates their predicted behavior. It can check whether a proposed configuration is plausible within those models. It does not automatically include the exact geometry and manufacturing variation of a fabricated circuit.

Moving from the tree to a layout adds questions about path length, bends, crossings, spacing, component tolerances, source conditions, and receiver thresholds. A tree with an improved model score may require longer routing. A lower switch count may reduce one resource while leaving input-power or detection costs unchanged. These are reasons to evaluate the complete implementation, not evidence of a flaw in the proposed method.

#### What can be concluded from the available evidence?

Fresh title and author searches did not recover a matching full manuscript or artifact. The [Bident evidence record](../observed-subthemes/neuromorphic-quantum-and-non-von-neumann.md#paper-dac-2026-research1268) remains description-backed. No numerical improvement, optimality proof, or fabricated-device result is supplied from inference.

The evidence supports physically loss-aware optical combiner synthesis, not demonstrated signoff-quality logic, fabricated-device performance or scalable photonic deployment.

A useful reproduction would compare the same logical functions and input conditions across the original and optimized configurations. It should preserve the exact component model, verify all required output decisions, report per-input and worst-case behavior as well as the aggregate score, and include the cost convention used for switches or couplers. For small instances, exhaustive enumeration of allowed configurations can independently check an optimality claim. Physical measurements would then test whether the model predicts the implemented circuit adequately.

## Quantum control is classical computation with strict physical timing

A quantum device does not directly execute a line of software. Classical electronics turn commands into signals, receive measurements, interpret them, and decide what happens next. Control timing concerns both when a signal begins and how its phase evolves. Feedback delay includes the measurement, signal processing, decision, and delivery of the next command.

A processor's clock frequency describes internal cycles. It does not specify the complete feedback latency or prove that every programmed sequence meets its timing requirements. Similarly, supporting several output channels is not evidence of controlling the same number of independent qubits under every protocol.

<span id="explanation-dac-2026-research1718"></span>

### RISC-Q: generate a configurable control system

#### What is being built, and what goes in and comes out?

[RISC-Q's paper record](../observed-subthemes/neuromorphic-quantum-and-non-von-neumann.md#paper-dac-2026-research1718) concerns a generator for classical quantum-control hardware. The generator uses SpinalHDL, a language for describing hardware, and exposes a RISC-V-compatible programming interface. Its prototype uses a ZCU216 board. [Manuscript, Sections III–IV, PDF pages 3–7](https://arxiv.org/pdf/2505.14902v1#page=3).

There are two different inputs to keep separate. At design time, a hardware generator takes configuration choices and produces a hardware description. At execution time, the resulting controller takes a program, signal parameters, and measurement data and produces control signals. Generating the controller is not the same task as running a quantum algorithm, and improving the generator does not by itself improve the accuracy of a quantum operation.

A field-programmable gate array, or FPGA, contains configurable logic and storage. Loading a design configures these resources into circuits that can operate concurrently. A processor implemented within that design still executes instructions, while other circuits can generate signals or process measurements. This distinction explains why a design can combine ordinary software with dedicated timing hardware instead of asking software to perform every operation at the required instant.

#### Follow one measurement-dependent operation from start to finish

The following is a conceptual execution sequence, not a measured timing trace from the prototype. It makes the controller's responsibilities explicit.

1. Software specifies a signal and when it should be emitted. The specification must reach the signal-generation circuit before that deadline.
2. The circuit produces digital samples. A digital-to-analog converter, or DAC, converts those numbers into an electrical signal supplied to the physical system.
3. A measurement returns an electrical signal. An analog-to-digital converter, or ADC, produces samples from it. Processing those samples produces a decision value; acquiring a signal and deciding what it means are separate operations.
4. The decision selects the next operation. The selected operation must then reach the output circuit in time to be useful.

The delay of the complete feedback sequence includes acquisition, conversion, processing, decision, and output delivery. Improving only the decision step cannot remove delays in the others. When stages overlap across repeated operations, throughput—the number completed per second—can improve without an equal reduction in the delay of one operation.

#### What a timed queue changes

A queue stores commands until they can be used. A timed queue additionally associates commands with their intended execution times. Software can prepare a command early; timing circuitry releases it at the scheduled instant. This separates when software prepares work from when the physical signal must occur.

That separation does not make deadlines automatic. If the command arrives after its scheduled time, the queue cannot deliver it in the past. If preparation produces commands more slowly than the output consumes them, the queue eventually empties. If preparation is too far ahead, finite queue capacity can fill. Correct operation therefore depends on command arrival time, capacity, and consumption rate, not simply on the presence of a queue.

Memory-mapped input/output means that some processor addresses refer to hardware control registers rather than ordinary stored data. A write to one of these addresses changes a circuit setting or submits a command. A read can retrieve a measurement result. This provides a software interface; the time required for the write to reach and affect the peripheral remains a hardware question.

#### Why preparing both alternatives can shorten a decision

The paper supports preloading two candidate gates into parallel timed queues and selecting between them through a control register after measurement. It contrasts this with a processor branch and explicitly notes a possible throughput cost from preloading. [Section V-B, PDF page 8](https://arxiv.org/pdf/2505.14902v1#page=8).

The general reasoning is a dependency change. Without advance preparation, work that depends on the outcome must wait until the outcome is available. Preparing both possibilities moves some work before that point. Afterward, the remaining task is selection rather than preparation of the chosen alternative. This is useful only to the extent that selection really is cheaper on the time-critical sequence.

It also means preparing an alternative that will not be used. Storage and command-delivery capacity are finite, so the extra work can reduce how many complete operations the system sustains. There is no contradiction between shorter decision delay and lower throughput: one measures waiting along a particular dependency sequence; the other measures the continuing rate at which resources can serve repeated work.

#### What the reported measurements establish

The prototype reports 500 MHz with 16 DAC and eight ADC channels. Section V-A does not provide a fair direct feedback-latency comparison; it compares system characteristics instead. Table I reports 74,551 lookup tables for RISC-Q versus 60,996 for QubiC. The code-size comparison is not an engineering-time measurement. [Section V-A and Table I, PDF page 8](https://arxiv.org/pdf/2505.14902v1#page=8).

A 500 MHz clock has a two-nanosecond period: one second divided by 500 million cycles. This arithmetic does not imply two-nanosecond feedback. The complete path can require many cycles and physical acquisition time. Likewise, a lookup-table count measures use of configurable logic resources, not control accuracy. A smaller source program measures less source text under the counting rule, not fewer debugging hours or stronger correctness guarantees.

The useful conclusion is consequently specific: evaluate design-generation effort, implementation resources, signal timing, and feedback delay separately. They answer different questions. A system can improve one while leaving another unchanged or making it worse.

#### What would make the contribution convincing for a new use?

A reproduction should specify a complete measurement-to-output task, identify the start and end events used for timing, and run both conditional implementations with the same signals and processing requirements. It should measure delay and sustained operation rate separately, include the cost of preparing both alternatives, and record late or missing commands. Tests of physical operation quality would be additional evidence, not a substitute for these controller measurements.

The [author repository](https://github.com/Wu-Quantum-Application-System-Group/RISC-Q) was inspected in the earlier recovery pass, not built or run. Final-conference-version matching and independent execution remain open. This explanation separates the recovered manuscript's observations from the conceptual reasoning above; it does not report a new hardware experiment.

<span id="explanation-dac-2026-research2805"></span>

### Active calibration: decide what to measure and when to interrupt useful work

#### The control setting is not the physical result

A controller can issue the same command twice without causing exactly the same physical operation. The device and its surrounding electronics can change. Calibration uses experiments to estimate which control settings currently produce the intended behavior. Characterization measures properties of the device; calibration uses such information to choose or update settings. Neither is the same as merely storing the last setting that was used. [Qiskit Experiments framework paper, “Summary” and “Statement of need,” PDF pages 1–2](https://joss.theoj.org/papers/10.21105/joss.05329.pdf#page=1).

An experiment has an input setting, a procedure, measured outcomes, and an analysis that estimates a parameter or operation quality. The result should include uncertainty and the conditions under which it was obtained. Applying a fitted setting is a separate step. Checking whether that setting actually meets the operating requirement is another. Conflating these steps makes it possible to report a successful fit without establishing a successful physical operation.

The goal is not to find a permanent best number. It is to keep the device operating within its requirements while spending an acceptable amount of time on measurement and adjustment. A measurement can be useful immediately and become outdated later. Repeating every experiment constantly reduces that risk but consumes resources that could otherwise execute useful work.

#### What the available source actually proposes

The paper's description combines a parameter-dependency graph, uncertain time-dependent drift models, experiment selection by expected information per unit time, and a reinforcement-learning/integer-optimization scheduler. It names online randomized-benchmarking and cross-entropy health signals, and an implementation called Cal Orchestrator. It claims improved calibration efficiency and longer intervals between recalibrations, but supplies no numerical results or artifact URL. [Official DAC description](https://63dac.conference-program.com/presentation/?id=RESEARCH2805&sess=sess135).

The description remains the paper-specific source. A fresh title/author and implementation-name search in this continuation did not recover a matching manuscript or repository. The explanation below develops the decision problem and its tradeoffs; it does not reconstruct unreported software internals, reward functions, or experiments. There are no manuscript page references to supply for this record.

#### Why knowing a value includes knowing when it was measured

Suppose an illustrative operating requirement allows a parameter to differ from its target by at most 0.05 units. A recent measurement estimates an offset of 0.02 with an uncertainty interval extending 0.01 in either direction. Under that interval convention, its upper endpoint is 0.03, inside the allowed range. Later, a drift model predicts the same mean offset but a wider interval of 0.04 in either direction. The upper endpoint is now 0.06, outside the requirement. The estimated mean did not change, but the available evidence no longer supports the same confidence in operation.

These numbers are a teaching example, not paper measurements, and an uncertainty interval is not a hard guarantee unless the model establishes one. The example explains why a scheduler can rationally request another measurement even before it observes a bad mean value. The useful state includes the estimate, uncertainty, measurement age, and model assumptions—not just the most recent fitted value.

Gradual drift and abrupt changes require different treatment. A model fitted to slow changes may confidently miss a sudden shift. Monitoring should test whether observations remain consistent with the assumed model, rather than endlessly extending a prediction after the device changes behavior. Conversely, triggering a full calibration after every noisy measurement can waste time. The decision must account for both missed degradation and unnecessary interruption.

#### Dependencies determine whether a new estimate is still applicable

Some calibration procedures assume other settings are already valid. If experiment B was analyzed using a setting obtained from experiment A, changing A can make the result of B inapplicable. A directed edge A → B records such a prerequisite or dependence. A graph with no directed cycles provides an order in which the dependent tasks can be considered.

That representation is useful only if its edges reflect the actual experimental assumptions. Missing a dependence can allow an invalid reuse of an old result. Adding an unnecessary dependence can prevent safe parallel work. Real procedures can also require iteration between coupled parameters; forcing such a process into a one-pass acyclic order needs explicit justification or a separate iteration rule.

For example, suppose A takes four seconds, B takes six seconds and must follow A, while an independent task C takes five seconds. With independent hardware resources for C, A and C can begin together, then B can start after A. The total completion time is ten seconds rather than the fifteen seconds of running all three serially. If C uses the same exclusive resource as A or B, that schedule may be invalid. This is a hand-constructed scheduling example, not evidence of the paper's parallel speedup.

The graph answers which results must precede which tasks. Resource constraints answer which otherwise-ready tasks can actually run together. A complete scheduler needs both.

#### Choosing a measurement is different from scheduling it

An uncertain model assigns possible outcomes to an unperformed experiment. Expected information gain estimates how much the observation would reduce that uncertainty, averaged over those possible outcomes. Dividing by experiment time expresses a preference for informative measurements that are inexpensive to obtain. The expectation is model-dependent: it is not information already observed.

Bayesian updating changes the relative plausibility of possible parameter values using how likely the observed data would be under each value. For example, suppose two candidate states initially have equal probability. A particular measurement outcome has probability 0.8 under the first state and 0.2 under the second. After observing that outcome, their updated probabilities are 0.8 and 0.2: multiply each prior probability by its outcome probability, then divide by the total. This calculation depends on the assumed measurement model; it is not certainty that the first state is correct. Bayesian experiment selection asks which next observation would most help the decision before paying to obtain it.

For a simple illustration, an experiment expected to provide 0.8 bits of information in four seconds has an expected rate of 0.2 bits per second. Another expected to provide one bit in ten seconds has a rate of 0.1. The first wins this particular ratio even though the second offers more total information. These hypothetical values explain the objective; they do not measure the paper's implementation or a real calibration experiment.

Here a bit measures uncertainty reduction, not a stored measurement's file size. In the special case of equally likely possibilities, narrowing four possibilities to two removes one bit of uncertainty. With unequal probabilities or noisy observations, information gain must use the full probability distribution. The ratio above assumes those expected gains have already been estimated consistently.

Information alone is not operation quality. Resolving a harmless parameter very precisely may be less valuable than checking a poorly known parameter that determines whether a gate meets its requirement. A good selection rule must connect uncertainty reduction to the device-level objective or constraints. Comparing information measures across parameters also requires a consistent probabilistic definition, not arbitrarily comparing their numerical variances when units and scales differ.

Once an experiment is selected, scheduling determines its start time, resource assignment, and interaction with other work. Reinforcement learning can learn a decision rule from the consequences of actions; its behavior depends on what information it observes and what reward it receives. Integer optimization can enforce discrete choices and constraints for a specified model. Naming both methods does not establish how they coordinate, which has final authority, or what happens when they disagree. Those details remain unavailable in the recovered description.

#### Why fewer recalibrations can be a misleading result

The mean time between recalibrations measures an interval between maintenance events. It does not measure whether the device was healthy throughout the interval. A policy that never recalibrates can make this interval very long while producing unusable operations. The interval becomes meaningful only with an operating-quality requirement and evidence about how long that requirement was satisfied.

A health indicator can detect that performance has changed without identifying which setting caused the change. It is also an estimate obtained from finite measurements. A trigger therefore needs a rule for uncertainty, repeated evidence, and recovery. Using the same observations both to choose a change and to declare the change successful can overstate the benefit; an additional validation measurement may be needed.

The complete cost includes monitoring, the selected calibration experiments, analysis, parameter updates, verification, and work interrupted or invalidated by the update. Some of these costs can overlap with useful computation; others cannot. A claim about reduced calibration time should state exactly which costs are included.

#### What would establish a useful improvement?

Compare policies over the same operating period and with the same required quality. Include fixed-interval and simple threshold-based alternatives, with reasonable tuning budgets. Report useful work completed, total unavailable time, time spent outside the quality requirement, unnecessary triggers, missed degradation, and recovery delay. Separately report how much computation or training the scheduling policy itself requires.

A controlled simulation can expose every policy to the same drift trace, making the comparison easier to interpret. Hardware experiments must account for changing conditions across runs; running one policy during a stable period and another during a disturbed period is not an equivalent test. Both gradual changes and sudden disturbances are relevant, but neither should be claimed as tested unless the experiment actually includes it.

The present source supports the proposed combination of mechanisms, not a numerical conclusion about how much useful computation it restores. The [paper evidence record](../observed-subthemes/neuromorphic-quantum-and-non-von-neumann.md#paper-dac-2026-research2805) retains that boundary. A similarly named calibration class in another project is not evidence that this paper's artifact was recovered or executed.

## Quantum compilation and simulation: distinguish design choices from device observations

Quantum error correction stores logical information across several physical qubits. Additional measurement qubits collect checks, called syndromes, without directly reading out the logical state. A decoder uses those outcomes to infer an appropriate correction. Different gate schedules can implement the same checks while exposing the system to different error opportunities.

<span id="explanation-dac-2026-research1036"></span>

### NEAT: choose placements and check schedules together

#### What must an error-correction check reveal—and not reveal?

Quantum error correction protects information by encoding it across several physical qubits. The encoded information is called a logical qubit. A check measures a property shared by the valid encoded states, rather than directly measuring the unknown logical information. Additional qubits used to collect these checks are called ancillas. The list of check results is the syndrome; a classical decoder uses it to infer a correction. A stabilizer code specifies compatible checks that leave its valid encoded states unchanged when there is no error. [IBM's explanation of stabilizer codes](https://quantum.cloud.ibm.com/learning/en/courses/foundations-of-quantum-error-correction/stabilizer-formalism/stabilizer-codes).

Consider an actual three-qubit bit-flip code as a small mathematical example, not a NEAT benchmark. Its two encoded basis states are `000` and `111`; an unknown encoded quantum state can be a superposition of these two. The checks ask whether qubits 1 and 2 agree, and whether qubits 2 and 3 agree. Both valid basis states answer “agree” to both checks. Checking agreement therefore need not reveal which encoded basis state is present. [IBM's repetition-code explanation](https://quantum.cloud.ibm.com/learning/en/courses/foundations-of-quantum-error-correction/stabilizer-formalism/repetition-code-revisited).

For example, a flip of the middle qubit changes `000` to `010` and `111` to `101`. In either case, both adjacent pairs disagree. A flip of the first qubit changes only the first check; a flip of the third changes only the second. Under the explicit assumption of at most one bit flip and perfect checks, the two results identify which qubit needs correction. The calculation does not require learning whether the encoded state was 0, 1, or their superposition.

The assumptions matter. Two bit flips can produce the same check results as a different single flip. A decoder that assumes one flip can then make the wrong correction. This small code also does not protect arbitrary phase errors, which change the relative phase of a superposition rather than simply exchanging 0 and 1. The example explains why checks are useful, not why this code alone is sufficient for reliable general quantum computation. [IBM's bit-flip-code tutorial](https://quantum.cloud.ibm.com/docs/en/tutorials/repetition-codes).

For this example, a superposition is a weighted combination of the `000` and `111` quantum states. The weights determine more than the probabilities of reading those strings: their relative sign can affect later quantum operations. The equally weighted plus and minus combinations are different states, yet both pass the two agreement checks. Changing that relative sign is a concrete phase error that these checks cannot detect. Protecting against bit flips alone therefore leaves part of the encoded information unprotected.

#### Why the check becomes a placement and scheduling problem

A check is not an abstract question answered at no cost. Its ancilla must interact with the relevant data qubits, then be measured. Those interactions are physical operations that take time and can introduce errors. If two requested operations need the same qubit at the same time, the device generally cannot execute them as independent two-qubit gates. Operations on disjoint qubits can still conflict because they share control resources or produce unwanted interactions.

On a neutral-atom platform, individual trapped atoms carry the qubits. Moving atoms changes which pairs can interact. A compiler must therefore output more than a reordered list of gates: it needs a placement and a physically permitted sequence of movements and operations. A valid ordering in the abstract circuit can be inconvenient or impossible in a particular geometry.

NEAT jointly models placement, check ordering, and motion. Its constraints cover required interactions, exclusive use of resources, ordering needed for logical correctness, and geometric feasibility. [Sections 3–4, PDF pages 3–4](https://fangmingliu.github.io/files/dac2026.pdf#page=3).

The input is a specification of required checks plus an architecture model. The output is a schedule and mapping that satisfy the encoded constraints. The compiler is classical software; it does not execute the checks or decode experimental measurements merely by producing that output. Whether the architecture model adequately represents the device is a separate validation question.

#### A small schedule shows what parallelism can and cannot do

Use the two adjacent-pair checks from the example above. Call their ancillas A and B, and the data qubits D1, D2, and D3. The first check needs interactions A–D1 and A–D2. The second needs B–D2 and B–D3. Ignoring geometry and assuming the chosen gate ordering is logically permitted, four serial operations can fit into two layers:

| Gate layer | First interaction | Second interaction | Shared qubit within this layer? |
|---|---|---|---|
| 1 | A–D1 | B–D2 | No |
| 2 | A–D2 | B–D3 | No |

By contrast, A–D2 and B–D2 cannot occupy the same layer under the one-gate-per-qubit rule. D2 requires two interactions, giving a lower bound of two layers for this simplified interaction set. The displayed schedule reaches that bound. This is a hand-derived example, not a schedule generated by NEAT, and it omits ancilla preparation, measurement, movement, and hardware interference.

Now restore geometry. Between the displayed layers, A needs access to D2 and B needs access to D3. Whether both transfers can happen together depends on the initial positions, destination positions, and permitted transport operation. A different initial mapping might reduce those transfers. Conversely, a layout selected without knowing the gate order may force long or conflicting moves. This is the dependency that joint optimization addresses: placement changes the cost of an ordering, while ordering changes which placement is useful.

Two full checks being compatible does not mean every gate used to implement them can be moved arbitrarily. The implementation must preserve the combined measurement, not just each operation's name. A short schedule that measures a different property is not an improvement. For more general codes, the ordering rules must account for the particular check operators and overlaps; the simple two-check example does not supply those rules.

#### How constraint solving searches without turning assumptions into guarantees

A constraint solver assigns values to variables while enforcing rules. For a scheduling problem, variables can specify a gate's time slot and an atom's position. A rule can prohibit two gates from using the same qubit in one slot. Another can require a valid interaction geometry whenever a gate is scheduled. An objective selects a preferred valid assignment, such as one with fewer layers or less movement.

An optimizer's result has several possible meanings. It may find a valid solution without proving it best, prove an optimum under its model, prove that the encoded problem has no solution, or stop before deciding. These states are not interchangeable. CP-SAT explicitly distinguishes feasible, optimal, infeasible, invalid, and unknown outcomes. [OR-Tools solver documentation](https://developers.google.com/optimization/cp/cp_solver).

For the two-layer example, the independent lower bound proves depth optimality under the simplified rules. For a large instance, producing a schedule of depth six does not by itself prove that depth five is impossible. A timeout also does not establish impossibility. Any optimality claim must specify the objective, the permitted designs, and the proof or bound supporting it.

Symmetry breaking can shorten the search by removing assignments that differ only in irrelevant naming or a truly equivalent transformation. For example, if two empty initial sites are equivalent under every modeled constraint, searching both equivalent choices may be unnecessary. The equivalence must hold for the actual model: reflecting a placement is not harmless if the device's controls or boundaries differ across the reflection. Faster search concerns compilation time, not physical gate time.

#### Read each measurement against its own question

The evaluation uses OR-Tools CP-SAT with a 7,200-second timeout. Enola receives NEAT's gate schedules, holding gate depth equal for the movement comparison. Table 2 includes exceptions to blanket improvement: Steane travel is 51.901 versus 51.549 grid units, while C4 depth is five versus the device-agnostic four. [Section 5.1 and Table 2, PDF pages 5–6](https://fangmingliu.github.io/files/dac2026.pdf#page=6).

Movement count counts scheduled transfer operations. Total distance accumulates travel under the stated convention. Neither alone determines duration: one operation may move several atoms concurrently, and a long transfer may take more time than a short one. Gate depth counts sequential gate layers, not movement or readout time unless those costs are explicitly included in the definition. Compilation time is the time spent finding the schedule, before physical execution.

Supplying the same gate schedule to two motion methods isolates a useful question: how well do they realize those interactions physically? It does not independently establish that the complete pipelines, each choosing its own schedule from the original input, have the same relationship. Both comparisons can be useful, but they answer different questions.

#### Why fewer physical faults is not the same measurement as fewer logical failures

The purpose of error correction is to tolerate some physical faults while preserving the encoded information. A score that requires every physical operation to be fault-free does not measure that purpose directly. For example, under a deliberately simplified independent-failure model, 100 operations each succeeding with probability 0.99 have a probability of about 0.366 that all succeed. That number says nothing about how many of the failed cases the code can correct. This is a numerical illustration, not an estimate for the paper's device.

A logical memory experiment instead asks whether encoded information survives a specified sequence of check rounds and decoding. To compare two schedules, hold the code, noise model, experiment duration or round count, decoder, and success definition fixed. Then count logical failures across repeated trials. Measurement faults and correlated errors matter because they can change what the decoder infers from the syndrome.

NEAT uses Stim noise simulation with matched decoder configurations for the two compilers. Its reported logical-error improvements are simulated, not measured on atoms. [Section 5.2 and Figure 5, PDF pages 5–6](https://fangmingliu.github.io/files/dac2026.pdf#page=5).

A reported reduction should include the number of trials and uncertainty, especially when failures are rare. Zero observed failures is not proof of zero failure probability. Changing a motion-error assumption can also change which schedule is preferable; such sensitivity needs testing rather than being inferred from a smaller movement count.

#### What remains before using the result as a design conclusion

The recovered PDF has anonymous-author and placeholder publisher metadata despite its author-hosted association. Shot counts, uncertainty intervals, final-version matching, and independent artifact execution remain unresolved. [Author publication listing](https://fangmingliu.github.io/publications/); [paper evidence record](../observed-subthemes/neuromorphic-quantum-and-non-von-neumann.md#paper-dac-2026-research1036).

A useful reproduction would check each emitted schedule against the stated logical and motion constraints, retain solver status and bounds, measure complete execution cost, and rerun the logical experiment under documented noise assumptions. That would test both sides of the contribution: whether joint search finds a better implementation and whether the implementation preserves information more reliably. It would not turn a simulated hardware model into a fabricated-device result.

<span id="explanation-iccad-2025-1094"></span>

### Qudit simulation: predict interactions and leakage in a larger state space

#### Three levels change both representation and control

A qubit uses two selected quantum states as its computational basis, usually labeled 0 and 1. A qutrit uses three, labeled 0, 1, and 2. Two qutrits therefore have nine joint basis states: each of the first system's three labels can be paired with each of the second's. Two qubits have four. This enlarges the representable state space; it does not by itself establish faster execution of an application.

A superconducting transmon is a circuit with multiple quantum energy levels, not a physical object limited to exactly two states. Qubit operation chooses two levels for computation; qutrit operation deliberately uses a third. The spacing between transitions affects whether control can address the intended change without driving unwanted changes. [Original transmon design paper](https://arxiv.org/abs/cond-mat/0703002).

Using more levels changes what counts as an error. Occupation of level 2 is outside a two-level qubit's computational space, but inside a qutrit's. A qutrit still has higher unwanted states outside its selected three-level space. A simulator must include enough physical levels to test unwanted transfer rather than eliminating the possibility by construction.

#### The output of a gate is more than a list of populations

A controlled-phase gate changes relative phases according to the joint state. A phase affects how components of a superposition combine in later operations. A minus sign is one simple phase change. Unlike a bit flip, it need not change the probability of immediately measuring a particular basis label.

Consider a mathematical gate example that leaves all nine two-qutrit basis labels unchanged but gives the `22` component a minus sign. This is an illustrative diagonal gate, not the paper's specified CPhase matrix. Start with an equally weighted superposition of `00` and `22`. The ideal operation changes the plus combination into the minus combination. Doing nothing leaves the plus combination unchanged.

Both outputs give `00` and `22` with equal probability if measured directly in that basis. Nevertheless, the two quantum states are different: their overlap is `1/2 − 1/2 = 0`. An appropriate later operation can distinguish them. Testing only basis-state populations would therefore miss this gate error completely.

This is why a reported gate fidelity needs a definition. It might describe agreement for a particular input state, an average over inputs, or another comparison of implemented and target operations. It must also state how leakage is handled. Conditioning on runs that remain in the computational space can conceal how frequently the system leaves that space unless the survival probability is reported separately.

#### What the simulation framework claims to connect

The author abstract describes a transmon–tunable-coupler–transmon system. It predicts cross-Kerr interactions and noisy two-qutrit CPhase fidelity, compares interaction predictions with literature systems, and co-optimizes device and control settings under an adiabatic scheme. It gives no numerical fidelity, noise parameters, or optimization budget. [Author's ICCAD 2025 publication entry](https://ferrispnugraha.github.io/).

Device parameters determine the energy levels and interactions available to the controller. A control waveform specifies how adjustable quantities vary during execution. The simulator uses both to predict how the quantum state evolves, then compares that result with the desired gate. A noise model adds specified mechanisms by which the environment or imperfect control alters that evolution.

These are distinct layers of the calculation. Agreement in an energy-level calculation does not automatically imply an accurate noise model. A realistic noise model cannot correct a wrong control waveform. An optimizer can only optimize the behavior represented by the assembled model.

#### Why an interaction can produce a conditional phase

In a cross-Kerr description, one subsystem's state changes an energy contribution associated with the other. Because quantum phases accumulate according to energy and elapsed time, the joint state can acquire a phase that depends on both subsystem states. A tunable coupler changes the effective interaction, allowing control over that accumulation.

For a purely illustrative constant interaction, define an angular rate `chi` so that the conditional phase magnitude is `chi × duration`. Doubling the rate and halving the duration produces the same phase in that simplified calculation. Real devices need not permit that substitution: changing the coupling can also change unwanted transitions, sensitivity to control error, and other phase contributions. Matching one accumulated phase is not a complete gate design.

Independent phases associated with each subsystem and truly joint phases must be distinguished when specifying the target. Some unwanted phases may be correctable by additional single-system operations; those corrections must be included in the comparison convention and execution cost. The author's abstract does not specify the convention used for its fidelity result.

#### Slow control and noise can favor different choices

Adiabatic control changes parameters sufficiently slowly relative to the relevant energy separations so that the system approximately follows the intended changing energy states. “Slowly” is relative to the device spectrum and path, not an absolute duration that works for every circuit. Rapid variation can cause unwanted transitions; smaller gaps can make a particular path harder to follow.

A longer operation also leaves more time for relaxation or loss of phase coherence. Relaxation changes state populations; loss of coherence can destroy the relative phase information needed by later operations. Making the pulse longer can reduce one error source while increasing another. Optimizing that tradeoff requires both a dynamical model and a specified noise model.

Pulse shape matters as well as duration. Two pulses with the same endpoints and total time can pass through sensitive regions at different rates. A search over duration alone and a search over full waveforms are different optimization problems and require different budgets.

#### What is actually validated?

The recovered abstract reports validation of cross-Kerr predictions against literature data. That supports a particular interaction calculation under the compared conditions. It is not direct validation of the complete optimized noisy gate. [Author abstract and preserved recovery assessment](../../iccad/data/qudit-primary-recovery-v1.json).

To validate a gate prediction, check the behavior on states sensitive to both population and phase errors, include leakage, and compare the predicted noise with relevant observations. Test sensitivity to uncertain device parameters. If the optimizer selects a region far from the validation data, explain why the model remains trustworthy there or collect additional evidence.

Searching more extensively can find settings that exploit an inaccurate part of a model. Therefore, a better simulated objective can make independent validation more important, not less. The best setting found within one parameterization and search budget is also not proof of the best gate physically possible on the device.

#### Source identity and remaining evidence

The author page uses “Architecture” in its title, while the conference record uses “System.” The existing recovery assessment reconciles the records using the shared DOI and authors; it does not silently treat the titles as identical. Fresh title/author searching in this continuation did not recover a full manuscript. The prior publisher route required browser verification. [Identity assessment](../../iccad/data/qudit-primary-recovery-v1.json).

The [paper evidence card](../observed-subthemes/neuromorphic-quantum-and-non-von-neumann.md#paper-iccad-2025-1094) therefore remains abstract-backed. The exact target gate, fidelity definition, noise rates, truncation of physical levels, optimization bounds, and validation errors remain unresolved. None of the mathematical examples above is a result from this paper or an independently executed device simulation.

## Durable connections and bounded long-term hypotheses

The shared first principle is that representation determines the validation burden. A stochastic transition must have the right probability. An analog integrator must follow a sufficiently accurate trajectory. Optical hashing must recover exact discrete values. A controller must respect timing. A compiler must preserve logical meaning while accounting for motion. A simulator must predict the physical quantities used to justify decisions.

One hypothesis is that device-aware compilation and calibration will become increasingly coupled: schedules depend on device conditions, while operating schedules affect which conditions need monitoring. Evidence would require a combined experiment showing improved useful computation at a fixed error requirement after charging for sensing, recompilation, and calibration. RISC-Q, active calibration, and NEAT supply related mechanisms, not such a combined demonstration.

The dependency is concrete. A compiler needs estimates of gate duration, error, and allowed interactions to choose a schedule. Calibration updates those estimates. A controller must then execute the selected operations with the assumed timing. If calibration changes a relevant parameter, an earlier schedule's predicted quality may no longer apply. A simulator can help evaluate candidate changes, but only within its validated range. None of these four steps can establish the others merely by succeeding at its own task.

A combined test would run the same workload and required output quality under two policies: one using a fixed schedule with its specified maintenance policy, and another allowing recalibration and rescheduling. Charge both for monitoring, compilation, calibration, invalidated work, and actual execution. The adaptive policy is useful only if it improves the resulting task-level measure after those costs. It could lose when the device is stable, when recalibration is expensive, or when a changed schedule gains too little to repay its preparation cost. This is a proposed test, not a reported cross-paper experiment.

A second hypothesis is that specialized physical computation will be valuable where its native operation closely matches the required representation and the conversion cost is small. It would be weakened when exactness recovery, repeated sampling, device programming, or calibration consumes the apparent gain. NeuroPDE and PhotoMT require especially different tests here: acceptable numerical approximation cannot be transferred into a cryptographic correctness claim.

This gives a practical comparison rule across the eight papers: identify the final requirement before choosing the internal metric. For NeuroPDE, ask for a numerical solution at a specified error, not only a cheap random transition. For fluid generation, define valid conditioned outputs before measuring sampling speed. For PhotoMT, require exact reference hashes. For Bident, check all required logic decisions, not only average attenuation. For quantum control and compilation, connect timing and motion to the intended operations. For the qudit model, test the full gate behavior rather than only one interaction parameter.

The longer-term question is whether a demonstrated component benefit survives this transition to a complete task and remains useful as inputs, devices, or operating conditions change. Comparable historical evidence would need to code those conditions consistently across editions. Counting more mentions of analog, photonic, or quantum methods would not answer that question.

These are mechanism-derived research questions. Six DAC 2026 papers and two ICCAD 2025 papers in a selected group do not establish growth, adoption, or a temporal trend. See the [longitudinal protocol](../longitudinal-protocol-v1.md). Related reading paths are [quantum architectures and control](../observed-subthemes/quantum-architectures-and-control.md), [photonic and optical compute](../observed-subthemes/photonic-and-optical-compute.md), and [analog compute-in-memory](../observed-subthemes/analog-compute-in-memory.md).

## What remains unresolved

Each of the eight paper discussions now includes a more developed conceptual explanation, with illustrative calculations separated from reported observations. Only RISC-Q, NEAT, and NeuroPDE have recovered manuscripts supporting their paper-specific discussion. PhotoMT, Bident, active calibration, and analog fluid generation remain description-backed; the qudit paper remains abstract-backed. Related background papers do not fill those missing sources or establish the unavailable implementation details.

This chapter has not passed an independent comprehension or scientific review. Its broad grouping still spans different technical fields and needs taxonomy review. Reading-card corrections also need reconciliation with original coding and all dependent synthesis. Source-version discrepancies, missing experimental conditions, artifact reproduction, and comparable historical evidence remain open. The collection-wide depth rewrite is unfinished; neither the number of authored subjects nor the length of this chapter establishes completion.
