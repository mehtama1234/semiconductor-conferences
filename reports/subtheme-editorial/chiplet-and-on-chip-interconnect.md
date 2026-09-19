## A connection is more than its transfer rate

An interconnect carries information between components. Its links transfer bits; its routing rules choose paths; its buffers hold data waiting for a resource. A receiver also needs a way to know which transaction a value belongs to and whether the required ordering or consistency rules have been satisfied.

Bandwidth describes how much data can be transferred per unit time. Latency describes how long a particular transfer takes. More bandwidth can reduce queueing under load, but it does not necessarily remove delays from routing, buffering, synchronization, or protocol processing.

## Why the communication pattern matters

Some computations send data evenly among components. Others concentrate traffic at one destination, repeatedly exchange small messages, or distribute a large value to many receivers. The same physical network can handle these patterns very differently.

A topology specifies which components are directly connected. Routing chooses the path for a transfer through that topology. Scheduling decides which pending transfer uses a shared link next. Improving any one of them can shift contention elsewhere. Evaluating only a link in isolation cannot reveal that system effect.

## The two selected records answer different questions

C2C-Explorer studies how to compare candidate chip-to-chip interconnect designs. Its official description combines workload-driven traffic generation, a simulator, and an adaptive search procedure. The generated traffic is part of the research assumption: a search can select the best candidate for the wrong traffic and still fail on the intended application. [Official description](https://63dac.conference-program.com/presentation/?id=RESEARCH130&sess=sess109)

The Panmnesia record concerns a controller and routing switch. Its company announcement describes shared buffers across protocol layers to reduce synchronization overhead, plus routing using port identifiers. This is a concrete proposal to change internal processing and connectivity. The announcement provides author/company evidence; it does not provide the full paper's latency distributions, power, area, process, and workload measurements. [Company technical announcement, Technical Highlights](https://panmnesia.com/news/en/2026-06-24-panmnesia-isca2026-eng/)

These records can inform each other conceptually. A design explorer needs realistic controller and switch costs. A controller evaluation needs realistic traffic and topology. Their evidence does not support comparing a search-efficiency result directly with a controller-latency result.

<span id="explanation-dac-2026-research130"></span>

## C2C-Explorer: make the interconnect search answer the workload question

### The design problem is a large conditional search

An interconnect design is not one number. It includes the topology, the number of chips, link connections, routing behavior, and the way requests are injected into the network. A candidate can have high link capacity but still deliver poor application performance if its paths contend, if buffers fill, or if its traffic pattern creates an uneven load. The number of possible combinations grows quickly as chips and links are added.

C2C-Explorer addresses this search problem for chip-to-chip systems used by large language models. Its artifact has three distinct responsibilities: generate traffic that represents the target workload, simulate the candidate interconnect, and choose additional candidates for evaluation through adaptive Bayesian design-space exploration. These responsibilities should not be merged into one speedup claim. A traffic generator defines what the simulator is asked to reproduce; the simulator defines the measured behavior; the search policy defines how much of the candidate space is examined.

### Traffic is part of the evidence, not merely an input file

The recorded workload includes DeepSeek-R1-671B inference on 32 XPUs and additional LLM traffic patterns. Such a workload produces communication between chips because model state, activations, or collective operations are distributed. The useful traffic pattern depends on message size, destination concentration, synchronization, and the order in which transfers become ready. A search optimized for one pattern can select a different topology from a search optimized for another.

This is why the paper's traffic-generation method matters. If generated traffic does not preserve the relevant burstiness, fan-out, synchronization, or request dependencies, a low simulator error against that generated trace can coexist with poor prediction of the deployed workload. The reported 2.46–8.23% timing error is evidence about the stated comparison with FPGA C2C prototypes across traffic patterns; it is not an error bound for every possible LLM deployment.

### Hybrid simulation trades detail against evaluation cost

A cycle-accurate simulator advances hardware events with fine timing detail. It can represent queueing and arbitration precisely, but each event costs computation. An event-oriented model can process larger time intervals or aggregated behavior more cheaply, but it must approximate the timing interactions that matter. A hybrid cycle/event simulator therefore needs a defined boundary: which components or phases receive detailed treatment, which are aggregated, and how the approximation is calibrated.

The paper reports up to 7.8× simulation speedup over a pure cycle-accurate simulator. That comparison is useful only with the same candidate, traffic, output metrics, and accuracy criterion. Simulation speed is not LLM inference speed: the result says that the model evaluates interconnect candidates faster, not that the deployed model generates tokens 7.8× faster. The 44.1% goodput improvement and 98.4% memory reduction belong to the 32-XPU DeepSeek-R1-671B study, but the recorded description does not identify the baseline configuration or define which memory is counted. They must not be read as the consequence of simulator speed alone.

### Bayesian exploration changes the evaluation schedule

Design-space exploration is expensive because each candidate requires a simulation or prototype measurement. Bayesian exploration uses results from earlier candidates to choose where to sample next. The benefit depends on whether the model guides the search toward useful regions without excluding a better region, and whether the cost of generating features, fitting or updating the model, and evaluating failed candidates is included.

The recorded evidence establishes the presence of an adaptive Bayesian search, but not its surrogate model, acquisition rule, initialization budget, stopping criterion, or sensitivity to random seeds. The description also says the framework supports switch/full-mesh simulation up to 512 chips and mentions FPGA-based validation. That supports a simulation capability and a validation path; it does not establish a physical 512-chip deployment or a particular production link technology.

### What C2C-Explorer establishes and what remains open

C2C-Explorer establishes a workload-driven exploration framework with a hybrid simulator and adaptive search, plus the reported timing agreement, simulation-speed comparison, goodput result, and memory result under the recorded conditions. It does not establish that one topology is best for LLM cloud systems in general, that the traffic generator represents all deployed workloads, or that the goodput and memory numbers include the full system cost. A stronger evaluation would publish traffic traces and generation rules, identify FPGA and simulation configurations, report search preparation and candidate budgets, define goodput and memory, and test held-out traffic patterns.

[Official DAC description, record RESEARCH130](https://63dac.conference-program.com/presentation/?id=RESEARCH130&sess=sess109)

<span id="explanation-isca-2026-program-044"></span>

## The CXL controller: unify the protocol path before scaling the fabric

### A CXL transfer crosses several responsibilities

CXL is a communication interface for attaching devices and memory. The physical layer moves electrical signals. The link layer manages reliable transfer between directly connected endpoints. The transaction layer describes the requested operation and its ordering or completion requirements. A conventional separation can make each layer easier to define, but it can also require data and control state to pass between layer-specific buffers and synchronization points.

The Panmnesia record describes a unified CXL controller that shares buffers across the physical, link, and transaction layers. The proposed mechanism is not simply a larger buffer. It changes where data and control state are held so that intermediate layers can coordinate without repeatedly copying or synchronizing the same transaction. The claimed benefit is lower controller overhead and a more direct path through the protocol stack; exact latency, bandwidth, area, power, and process values are not present in the captured company source.

### Routing determines whether added memory remains usable

Connecting more memory nodes increases available capacity only if requests can reach the correct node without excessive contention. A hierarchy-based fabric fixes routes around a predefined tree or level structure. A port-based switch instead uses identifiers associated with ports to select paths, allowing the fabric topology to be changed without requiring the same fixed hierarchy. The routing rule must still preserve reachability, ordering, flow control, and progress for concurrent requests.

The source describes a switch that supports port-based routing alongside hierarchy-based routing. This is an architectural compatibility claim: an existing hierarchical organization can remain available while a more flexible topology is introduced. It does not by itself show that every topology has equal latency or that routing state scales without added storage and control time. Those properties require a workload matrix and measurements at different node counts and traffic concentrations.

### Read the silicon wording narrowly

The company article identifies the exact ISCA paper and describes larger memory expansion at a similar latency, improved total system bandwidth, and stable performance up to 64 nodes. It also uses silicon-proven and pre-release product language. The source is valuable evidence that an implementation and product context were claimed, but it is not the captured IEEE paper and does not provide the paper's complete evaluation conditions. “Silicon-proven” should therefore not be expanded into a claim about a measured 64-node system, a particular process node, or a universal latency bound.

### What this record establishes and what remains open

The accessible evidence establishes a unified cross-layer CXL controller, a switch with port-based and hierarchical routing options, and an author/company report of scaling to 64 nodes while maintaining a similar latency range and increasing system bandwidth. It does not establish the numerical size of those changes, the power and area cost, the exact CXL generation and protocol features, the node-to-node traffic distribution, or independent operation of the complete fabric. A stronger reading needs the paper's controller microarchitecture, buffer sizes, routing and flow-control rules, silicon test setup, latency distributions, bandwidth denominators, power/area, and comparison baseline.

[Official company technical highlights](https://panmnesia.com/news/en/2026-06-24-panmnesia-isca2026-eng/)

## Buffers solve one problem and introduce another

A buffer permits a sender and receiver to operate at different times. It can absorb a short burst and allow independent work to continue. However, queued data still waits, buffer space consumes hardware resources, and several traffic classes may compete for that space.

Sharing buffers can reduce duplication or synchronization, but requires rules for allocation and progress. A valid design must ensure that one class of traffic does not indefinitely prevent another from advancing. The details of that requirement depend on the protocol; a general buffer-capacity number does not establish it.

## The experiment needed to interpret a result

Measure isolated latency and performance as offered load increases. Include small and large transfers, concentrated traffic, and concurrent applications. Record useful delivered data, time spent waiting, buffer occupancy, energy, and the application completion time.

State which portions are measured in silicon, emulated, or simulated. For simulation, compare the modeled component behavior with an appropriate reference and show how model errors affect the selected design. For search, include traffic preparation and all evaluation costs.

This subject has only two selected records, one from DAC and one from ISCA. They establish two useful cases for reading. Broader conclusions about interconnect research or adoption require a larger and consistently examined population.
