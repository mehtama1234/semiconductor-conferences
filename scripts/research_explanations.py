"""Editorial explanations; kept separate from verbatim evidence and coding labels.

Each entry explains the physical or computational cause, the design choices, and a concrete comparison.
These are conceptual explanations, not new results. Written for a newcomer: short sections, short
sentences, numbered steps where order matters, and worked numbers in a marked box."""

# Each section is (heading that states its point, Markdown body).
EXPLANATIONS = {
 'architecture-and-accelerators': [
 ('A processor fetches values, computes, and passes results on', '''A program performs operations on stored values. For each operation the processor must:

1. obtain the input values;
2. execute the operation;
3. store or forward the result.

An operation that depends on an earlier result must wait for it. Independent operations can run at the same time, if enough hardware and data are available.

An **accelerator** is hardware arranged for one kind of computation. Its benefit comes from one of three things: less work, fewer data transfers, or more useful operations at once.'''),
 ('More arithmetic units help only if their inputs arrive in time', '''An operation needs its inputs. If they have not arrived, the arithmetic unit waits.

Adding units raises the possible rate of computation. It also raises the rate at which inputs must arrive. So the time to finish a job is limited by both computation and data supply.

Some operations cannot run in parallel at all. That is why good performance on one large matrix calculation does not show good performance on a whole application.'''),
 ('The subthemes differ in what they change', '''- **Precision methods** change how many bits represent a number, and how much numerical error the application accepts.
- **Sparse computation** skips values or operations known to be unnecessary. It must still find the remaining values and share out the uneven work.
- **Dataflow methods** choose when operations run and where intermediate results stay.
- **Hardware and software co-design** changes the machine and the program together. The evaluation must then show which change caused the improvement.'''),
 ('A fair test holds the job fixed and measures the whole cost', '''1. Hold the application, the required answer quality and the input sizes fixed.
2. Compare completion time, energy per completed job, memory use and hardware cost.
3. Vary the inputs that affect reuse or parallelism.

Suppose a specialized design wins only when all inputs fit in a small memory. Then that memory size is part of the result. The evidence cards below keep the reported conditions. Read them before applying a result to a different application.''')],
 'memory-interconnect-and-storage': [
 ('Capacity, bandwidth and latency are three different limits', '''A computation reads inputs and writes outputs. Those values take up bytes in memory or storage.

- **Capacity** is how many bytes can be held.
- **Bandwidth** is how many bytes can be moved per second.
- **Latency** is the wait between asking for a value and getting it.

Enough capacity does not guarantee a fast transfer. High bandwidth does not guarantee a short wait for one request.'''),
 ('Moving data sets a floor on how long a job takes', '''> **The rule.** A job must move **B** bytes. Its connection sustains **W** bytes per second. The transfers alone take at least **B ÷ W** seconds, however fast the arithmetic is.

This simple bound assumes the job gets the stated bandwidth. Shared requests, protocol work and dependencies can make it slower.

Keeping a value near its next user can cut transfers. But nearby memory is small, so keeping one value there may push out another useful one.'''),
 ('The subthemes move data, move work, or change the path', '''- **Memory hierarchy** work decides which values sit in faster or slower memory.
- **Near-memory or processing-in-memory** work moves some computation toward the stored data.
- **Interconnect** work changes the paths between components.
- **Storage** work must also ask whether a value survives power loss and whether updates stay consistent.

Each can cut one transfer while adding scheduling, copying or coordination work somewhere else.'''),
 ('A fair test measures the whole job, including moving the data', '''1. Measure the whole job, including placing and migrating data.
2. Vary whether the input fits in each memory, and how many other jobs share the connection.
3. For approximate search, hold answer quality fixed. For a service, measure slow requests as well as the average.

Fewer remote bytes is useful evidence about one cost. The final claim needs completion time or energy under the full conditions.''')],
 'ai-assisted-eda': [
 ('Chip design is a long chain of choices that software helps make', '''A designer states what a circuit must do and which limits it must meet. **Electronic design automation (EDA)** is the software that turns that statement into a circuit and then a physical layout.

There are many choices along the way:

1. how to represent the logic;
2. which circuit elements to use;
3. where to place them;
4. how to connect them.

Each choice can affect correctness, area, timing and power.'''),
 ('A learned model can propose or predict, and these are different jobs', '''A learned model uses patterns in past examples or evaluations to suggest a new choice.

- A **language model** may write hardware-description code, or change a design program.
- A **predictor** may guess which candidate is worth an expensive evaluation.

Writing code does not show that the code meets the specification. Predicting a good timing score does not show that the built circuit meets timing.'''),
 ('Each check answers a different question, so record which one failed', '''- **Synthesis** turns a behavioral or logical description into circuit elements.
- **Simulation** runs a model on selected inputs.
- **Formal verification** checks a stated property mathematically, within a defined model.

A design method should record which check rejected a candidate, what it reported, and how that changed the next attempt. A weak test can accept a wrong design and make the search look successful.'''),
 ('A fair test counts every model call, check and retry', '''1. Give competing methods the same design tasks.
2. Count the whole time and computing budget: model calls, training, checking and retries.
3. Report valid completed designs and their measured quality.
4. Test on new circuits that were not used to tune the method.

The long-term question: can better choices be made with less total engineering and evaluation effort, while keeping the design correct?''')],
 'physical-design-and-manufacturing': [
 ('A correct connection can still arrive too late once it becomes a wire', '''A circuit description lists components and their connections. Manufacturing needs real shapes in specified material layers.

1. **Placement** chooses where each component sits.
2. **Routing** chooses each wire's path and layer.

Wires take up space, resist current and store electric charge. Their length and surroundings change how fast a signal switches. So a logically correct connection can still arrive too late.'''),
 ('Every physical fix pushes on another part of the design', '''- Moving two communicating components closer shortens a wire, but can crowd another region.
- Adding a buffer can improve signal timing, but adds area and power.
- Manufacturing rules limit widths, spacing and overlaps.
- Changes in fabrication can change how transistors and wires behave.

An optimizer must meet all these conditions together. Improving one score while quietly breaking another does not count.'''),
 ('The subthemes build geometry, estimate timing, or model manufacturing', '''- **Placement and routing** methods build the geometry.
- **Timing analysis** estimates whether signals switch in time.
- **Process models** estimate how fabricated devices behave.
- **Manufacturing and yield** methods study defects and variation. Yield is the fraction of manufactured chips that meet requirements.

A faster estimator and a better final layout are different contributions. They need different evidence.'''),
 ('A fair test uses the same circuits and rules, and counts violations', '''1. Use the same circuit set, manufacturing rules, timing requirements and implementation tools.
2. Record violations as well as successful outputs.
3. Check the chosen designs with an accurate enough final evaluation, and count all search time.
4. If a method uses a cheaper approximation, check whether its errors change which design is chosen.''')],
 'chiplets-3d-and-packaging': [
 ('Splitting a system into several dies adds boundaries data must cross', '''A **die** is a piece of semiconductor carrying circuits. A package can connect several dies. When they are designed as parts of one larger system they are often called **chiplets**. A **three-dimensional (3D)** design stacks active layers or dies on top of each other.

Splitting lets different functions use different manufacturing processes. The cost is that communication must cross extra physical boundaries.'''),
 ('Each boundary costs area, energy, time and heat', '''- A link between dies uses area, energy and time.
- The package must deliver current to, and remove heat from, every active part.
- Stacked parts can sit far from a good cooling path.

So moving computation between dies changes communication and temperature together. A system choice cannot be judged from the speed of one die alone.'''),
 ('The subthemes split, connect, cool, or design the package', '''- **Partitioning** decides which functions belong together.
- **Interconnect** designs the communication between the parts.
- **Thermal** methods estimate temperatures and choose placement or operation to stay within limits.
- **Package co-design** studies these choices together with power delivery and physical assembly.

One paper may address several of these.'''),
 ('A fair test states the physical setup and compares whole systems', '''1. State die sizes, link rates, cooling, power assumptions, workload placement and the manufacturing assumptions used for cost.
2. Compare the full system under the same temperature and performance limits.

A thermal simulation supports a temperature prediction under its model. Reliability and yield of manufactured parts need their own evidence.''')],
 'power-reliability-and-security': [
 ('Reliability, security and power all limit useful work', '''- **Reliability** asks whether a system keeps producing correct results under faults, such as flipped bits or failing parts.
- **Security** asks what an adversary can observe or change.
- **Power** is the rate of energy use. It affects electrical supply and temperature.

They sit together here because protections and operating limits change how much useful work a system can do.'''),
 ('Every protection costs something, so name the threat first', '''- **Detecting** a wrong value needs extra information, repeated work, or a check against a constraint.
- **Correcting** it needs enough information to tell the possible errors apart.
- **Isolation** may restrict sharing.
- **Recovery** may stop work and restart it.

So the benefit depends on which error or attack is being considered, and on the cost of the added work.'''),
 ('The subthemes protect against different things', '''- **Fault tolerance** keeps or recovers computation after faults.
- **Side-channel** work studies information leaked through timing, power or shared resources, even when direct access is blocked.
- **Privacy-preserving computation** changes how protected inputs are processed.
- **Energy** methods change when or how hardware runs.

Progress in one category does not show protection in another.'''),
 ('A fair test states the fault or attacker and measures work with protection on', '''1. State which faults can occur, or which actions an attacker can take.
2. Measure undetected failures, false alarms, recovery time, and performance with protection switched on.
3. Include energy per correct completed job.
4. If faults are injected, say where and how.

Results from that experiment apply to the tested fault model, until broader evidence exists.''')],
 'verification-and-validation': [
 ('A design is correct only relative to a written requirement', '''A requirement can describe an output, a sequence of states, a timing limit, or information that must stay private.

- **Verification** checks whether the design meets those statements.
- **Validation** asks whether the statements and the design meet the intended use.

The two questions can need different experiments.'''),
 ('Tests try some behaviors; proofs cover only what they assume', '''A circuit can have very many input combinations and internal states.

- **Simulation** tries selected runs and compares them with the expected result. A test that never reaches a faulty state cannot expose that fault.
- **Formal verification** reasons about a specified set of behaviors. Its conclusion depends on the model, the assumptions and the property proved.

A timeout is an unresolved check, not a pass.'''),
 ('The subthemes run tests faster, prove properties, or choose better inputs', '''- **Simulation** methods run a model faster.
- **Emulation** builds a version of the design on other hardware to run tests.
- **Formal** methods search for violations or prove properties.
- **Test generation** picks inputs likely to expose errors.
- **Coverage** measures say which behaviors were exercised. They need a definition to mean anything.'''),
 ('A fair test uses known faults and reports what was missed', '''1. Use known faults, or independently established reference behavior, to judge detection.
2. State design sizes, properties, test budget, unresolved checks, false alarms and missed faults.
3. When a generated test raises a score, check whether it finds new errors on designs outside the development set.

More tests help only if they improve the relevant coverage or detection.''')],
 'design-methodology-and-tooling': [
 ('Design tools make many small choices that add up', '''- A **compiler** turns a program from one form into another while keeping its intended behavior.
- A **synthesis tool** builds a circuit implementation.
- An **optimizer** picks among implementations by a stated goal.

Together these choices decide run time, memory use, circuit size, and the effort needed to get a result.'''),
 ('How a design is written down decides what a tool can see and change', '''A representation makes some properties visible and hides others.

- A **graph** can show which operations depend on which.
- A **schedule** assigns operations to times or resources.

Removing redundant work can also change memory traffic or available parallelism. So a tool needs two things: a rule for which changes keep the design correct, and a cost model for picking useful ones.'''),
 ('The subthemes change the steps, the search, the structure, or the benchmarks', '''- **Compilation and synthesis** methods change the sequence of transformations.
- **Search** methods choose configurations or implementations.
- **Graph and partitioning** methods organize connected work.
- **Benchmark and artifact** methods publish inputs, expected outputs and steps so others can compare.

Their shared question: can another designer or user get the claimed benefit by following a defined process?'''),
 ('A fair test separates tool time from the time the output saves', '''1. State inputs, versions, settings, hardware, and the total time to get a valid output.
2. Separate time spent running the tool from time saved by its output.
3. Compare correctness and output quality, not only run time.
4. Test on unfamiliar inputs. That is a stronger test than re-tuning on the development examples.''')],
 'systems-applications-and-workloads': [
 ('Start from the work a user needs done', '''A **workload** is the work asked of a system: its operations, input sizes, arrival times and required output quality.

A deployment adds limits such as memory size, battery energy, network access or response deadlines. The same algorithm can face very different limits when requests arrive together, or inputs change over time.'''),
 ('Average speed hides the slow requests that miss deadlines', '''Requests compete for processors, memory and communication paths. A request may wait even when its own computation is short.

- **Throughput** is work completed per unit of time.
- **Response latency** is the time one request takes.
- **Tail latency** describes the unusually slow requests. It matters when deadlines apply.

Batching can raise throughput while making each request wait longer.'''),
 ('The subthemes differ in where the system runs and what limits it', '''- **Edge** systems run near the data or the users, often short of power or memory.
- **Cloud** systems share remote resources.
- **Distributed** systems coordinate work across machines.
- **Application-specific** systems use the structure of fields such as robotics, sensing or scientific computing.

The workload decides which resource is the limit, and which output errors are acceptable.'''),
 ('A fair test states the demand and checks targets as it changes', '''1. Specify request patterns, concurrency, input sizes, quality targets, hardware and network conditions.
2. Include scheduling, loading, communication and recovery costs.
3. Measure whether the service meets its target as demand changes.

All selected records in this theme come from DAC. So they cannot show a three-conference pattern by themselves.''')],
 'analog-mixed-signal-and-emerging-devices': [
 ('Here physics itself does part of the computing', '''- **Digital** circuits hold values as discrete bit patterns.
- **Analog** computation uses continuously varying quantities such as voltage or current.
- **Optical** computation uses properties of light.
- **Quantum** computation uses quantum states and operations.

These differ greatly. But each must say exactly how a physical state stands for the input. It must also say how the output is read.'''),
 ('The device is only part of the cost: conversion and correction count too', '''Inputs may need converting from digital values. Outputs may need measuring and converting back.

Noise, temperature, differences between devices, and measurement precision can all change the result. **Calibration** adjusts operation using measured device behavior, and it also costs time or hardware.

Any claimed saving must include the conversion, control and correction work around the device.'''),
 ('The subthemes use very different physics, with different accuracy measures', '''- **Analog circuit automation** designs continuous-signal circuits.
- **Compute-in-memory** performs operations in or near storage.
- **Photonic** work uses optical components.
- **Quantum hardware and control** prepares, manipulates and measures quantum states.
- **Emerging memory** studies storage technologies with different physical properties.

Grouping them does not make their accuracy or performance measures interchangeable.'''),
 ('A fair test says where the evidence comes from and counts the full path', '''1. Say whether the evidence comes from equations, simulation, a fabricated device, or a complete system.
2. Report precision, error, calibration, conversion cost, temperature and device variation, under the intended workload.

A low-energy device operation shows one component cost. An application claim needs the full path from inputs to usable outputs.''')],
}


def explanation_sections(theme):
    lines = []
    for heading, body in EXPLANATIONS[theme]:
        lines += ['## ' + heading, '', body.strip(), '']
    return lines
