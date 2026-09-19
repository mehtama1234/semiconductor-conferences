## Speculative decoding creates both parallel work and temporary state

This group contains one paper, HBSpec, about a hybrid-bonded accelerator for tree-structured speculative decoding. It is a specific intersection of packaging, memory management, and language-model execution—not a survey of all heterogeneous integration.

Ordinary autoregressive generation produces a new token using the preceding tokens. A token is a unit of the model's text representation. Speculative decoding proposes several possible future tokens and checks them with the target model. A tree can represent alternative continuations that share a prefix. Its width expresses how many alternatives are considered; its depth expresses how far those alternatives extend.

More candidates can expose parallel work, but not all that work becomes accepted output. The system must compute, store, and eventually discard information for rejected candidates. A faster candidate generator is therefore not automatically a faster text generator.

## Why packaging enters an algorithmic problem

Heterogeneous hardware contains different kinds of processing resources. Near-memory processing places computation close to the memory supplying its operands. Hybrid bonding joins surfaces through closely spaced electrical contacts and dielectric bonding, enabling dense connections between stacked components. These terms describe different design choices: where computation happens, what performs it, and how components connect.

The reason to combine them is that an operation may need many bytes transferred for relatively little arithmetic. Arithmetic intensity measures operations per byte moved at a specified memory boundary. Increasing available arithmetic does little for such an operation if the data cannot arrive faster. Conversely, adding bandwidth does little once the available arithmetic is the limiting resource.

The boundary must be stated. An operation can reuse data efficiently inside a processing unit while repeatedly fetching those same data across a more expensive connection elsewhere. Counting only local transfers can conceal that cost.

<span id="explanation-dac-2026-research2417"></span>

### HBSpec: heterogeneous speculative decoding must improve accepted-token progress under a complete package and memory budget

#### What speculative decoding actually measures

Autoregressive decoding generates one token, or output symbol, at a time with the target language model. Speculative decoding adds a draft model that proposes a sequence or tree of candidate tokens. The target model then checks those candidates. The system accepts a prefix or selected paths according to its verification rule and rejects the rest. Rejected candidates consume computation and memory but do not become output.

The useful unit is therefore accepted output tokens per elapsed time, together with output-quality and sampling conditions. A design that verifies many candidates can still be slow if the acceptance rate is low or if tree management and data movement dominate. Acceptance is not a fixed hardware property: it depends on the draft and target models, prompt distribution, generated length, tree width, sampling rule and the exact verification algorithm.

#### What the heterogeneous hardware is changing

The draft and target computations may have different arithmetic, memory and latency needs. A heterogeneous design can place different processing elements or memory resources near the data they use. Communication-aware mapping decides which data resides in which bank or die. An arithmetic-intensity-aware scheduler decides whether an operation is limited mainly by arithmetic or by moving its operands.

These decisions are conditional on a stated boundary. Data can be local to one die but remote across a bonded interface. A mapping that reduces cross-bank traffic can concentrate accesses on one bank. A scheduler that chooses a nearby compute element can increase contention for its local memory. The evaluation must include the transfers, mapping work, scheduling decisions and synchronization that occur on the critical path.

#### Why Branch-KV storage needs correctness rules

Attention uses key and value state from earlier positions. A tree of candidate continuations shares a prefix and then creates private branch state. The memory system must identify shared state, branch-private state and state that can be reclaimed after verification. It must prevent one branch from reading another branch's incompatible state and must preserve the accepted path after rejected branches are discarded.

The Branch-KV pool can reduce fragmentation only if its allocation unit, metadata, sharing rule and reclamation procedure are defined. It also needs to handle a candidate tree whose width changes over time. A claimed reduction in wasted storage must be measured against metadata, copying, synchronization and the state-transfer work needed to verify and commit a path.

#### What hybrid bonding does and does not prove

Hybrid bonding may provide closely spaced electrical connections and a dense physical arrangement. The system claim still depends on link capacity, latency, memory bandwidth, die area, power delivery, heat removal, bond yield and assembly cost. A simulated link or an abstract bandwidth assumption is not a measured package result. The comparison must identify whether the reported factor is a kernel, accelerator, decoding-loop or complete user-visible latency measurement.

The correct comparison holds the target model, draft model, prompts, generated lengths, tree policy, acceptance rule and output-quality requirement fixed. It reports candidate tokens, accepted tokens, acceptance rate, verification time, data-transfer time, Branch-KV capacity and overhead, end-to-end latency, energy and the physical resource budget. Separate package feasibility requires bond pitch, process, thermal, yield and manufacturing assumptions.

The captured DAC description supports a hybrid-bonding heterogeneous accelerator for tree-structured speculative decoding. It reports no acceptance rate, accepted-token throughput, latency, energy, area, thermal, bond, yield or workload-diverse result. The evidence supports a hardware direction and its evaluation requirements, not demonstrated decoding improvement or a manufacturing conclusion.

[Observed paper card](../observed-subthemes/chiplets-and-heterogeneous-integration.md#paper-dac-2026-research2417)

## What HBSpec changes

[HBSpec](../observed-subthemes/chiplets-and-heterogeneous-integration.md#paper-dac-2026-research2417) places customized processing elements on an incorporated logic die to increase near-memory computation capacity. Its official description adds communication-aware data mapping to reduce cross-bank access, an arithmetic-intensity-aware operator scheduler, and a Branch-KV pool intended to eliminate memory fragmentation.

It reports performance factors of 15.56×, 2.36×, and 2.13× over NPU-only, NPU-plus-LPDDR, and NPU-plus-hybrid-bonding baselines, respectively. The description does not define the measured performance quantity, averaging method, model pairs, tree dimensions, acceptance rates, or baseline resource matching. Nor does it expose measured-silicon versus simulation methodology. The three factors must remain separate, and should not be relabeled as energy savings or user-visible latency reductions. [Official HBSpec description](https://63dac.conference-program.com/presentation/?id=RESEARCH2417&sess=sess142).

A memory bank is a separately managed part of a memory array. Mapping related data to suitable banks can change which accesses compete and which transfers must cross bank boundaries. But locality and balance can conflict: concentrating related data may reduce some transfers while overloading a bank. A complete assessment should measure both effects.

An operator scheduler assigns pieces of computation to available execution resources. Its decision must account for input location and transfer cost as well as arithmetic demand. Reassigning an operation is useful only if the savings exceed the cost of getting data to that resource and returning the result where it is needed.

## Branch storage needs correctness as well as capacity

The key/value cache stores attention information from earlier token positions. For a candidate tree, branches may share earlier positions and diverge later. Memory management must distinguish state that is still shared, state private to a candidate, and state no longer needed after verification.

Fragmentation means allocated or free space is divided in a way that prevents efficient use. A pool can organize allocation, but its name alone does not establish zero waste. The full method must explain allocation granularity, metadata, reclamation, and whether partial blocks can be reused. The short source does not supply those details.

Correctness checks must ensure that one branch does not use another branch's incompatible state. After accepting a path, the system must preserve its required state while safely reclaiming rejected paths. These are validation requirements for tree-state management, not claims that a particular undocumented HBSpec implementation uses reference counting, paging, or any other specific mechanism.

## What a meaningful end-to-end test would measure

Useful throughput counts accepted output tokens per elapsed second, not proposed tokens. An iteration that verifies many candidates but accepts little may consume more work without proportional progress. Report candidate count, accepted path length, verification time, state-transfer time, and discarded work alongside total throughput.

The comparison should hold the target model, output-quality requirement, sampling rules, prompt lengths, and generated lengths explicit. Different draft models or tree policies can change acceptance enough to obscure the hardware contribution. The acceptance algorithm needs its own correctness argument; hardware speed does not establish equivalence to the target model's generation distribution.

The package assessment also needs bond pitch, link capacity, memory organization, area, power, and thermal assumptions. A design that meets arithmetic and bandwidth goals still requires a feasible physical implementation. Yield and assembly cost should not be inferred from a favorable performance ratio.

## Connection to the wider theme and evidence boundary

The conceptual connection is that a branching algorithm changes memory demand and available parallelism, which can change the preferred arrangement of compute and memory. This is an inference from the design problem. One paper does not establish a long-term trend or show that hybrid bonding is necessary for every speculative-decoding workload.

The official description was refreshed on 2026-09-07 and supersedes the historical card's missing-result statement where cited above. Author publication lists confirm the work, but no full manuscript was recovered, so page-backed implementation and evaluation conditions remain missing. H2-LLM and the authors' earlier adaptive draft-length paper are related but distinct works; their numbers cannot substitute for HBSpec's missing experiments.
