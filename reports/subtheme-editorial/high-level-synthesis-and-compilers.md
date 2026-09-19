## A program does not uniquely specify a circuit

A program describes operations and the behavior required from them. Hardware construction must also decide how many execution units exist, which operations share a unit, where values are stored, and when work proceeds. Different choices can implement the same behavior with different area, timing, and energy costs.

High-level synthesis constructs hardware from a higher-level program description. A compiler transforms representations of the program and selects implementation choices. The result must preserve the required behavior and remain compatible with the target device and tool flow.

## Dependencies limit concurrent execution

An operation needs its inputs before it can start. If another operation produces an input, their dependency constrains the schedule. Independent work may run concurrently when hardware and data are available. Repeated work may be pipelined so different iterations occupy different execution stages.

Pipelining does not remove dependencies or storage limits. A stage can stall if its input is unavailable or its output buffer is full. The compiler needs enough information about communication and resource use to choose a schedule that can actually execute.

## Intermediate representations expose different choices

An intermediate representation is a structured form used between the original program and final implementation. One form may expose large computational regions, while another exposes individual operations and transfers. Transformations can be easier to express and check at the level where the relevant relationships are explicit.

Dataflowgen's captured description uses a two-level representation within MLIR, a compiler framework supporting multiple representations. It outlines computational regions and applies dataflow transformations and optimization. The record identifies a method, but does not provide target devices, benchmark identities, numerical gains, or compilation cost. [Recorded evidence](../observed-subthemes/high-level-synthesis-and-compilers.md#paper-dac-2026-research083)

The missing conditions matter because a transformation that helps one target may add buffering or unsupported operations on another. A compiler architecture alone does not establish a hardware-performance result.

<span id="explanation-dac-2026-research083"></span>

## Dataflowgen: a richer IR must still lower to correct, closable hardware

An intermediate representation (IR) is a structured description between source behavior and generated hardware. A high-level IR can preserve algorithmic regions and loops; a lower-level IR can expose operations, dependencies, buffers and transfers. The benefit of multiple levels is that each transformation can operate where its relevant information is visible. The cost is that every conversion must preserve meaning and make target constraints explicit.

Dataflowgen is described as an open-source MLIR framework with two IR levels for dataflow accelerator generation. It outlines an application kernel, applies dataflow transformations, and derives a hardware-oriented control dataflow graph (H-CDFG). This changes the compiler's representation and search space. It does not by itself establish which MLIR dialects are supported, how memory effects are modeled, how the H-CDFG is lowered, or which FPGA/ASIC backends can consume it.

### Parallel-looking graphs still have dependencies and storage costs

The compiler must preserve loop bounds, dependences, memory ordering, side effects, reductions, initialization and numerical precision. A graph may expose independent operations while their operands arrive through a shared buffer or memory port. A fused or parallelized region can increase live values, buffering, routing pressure or peak bandwidth. A transformation that removes an apparent dependency must prove that the removed ordering was not required by the source program.

Check generated behavior against a trusted software or reference implementation on corner cases, including empty or short inputs, aliasing where supported, boundary iterations, reductions, overflow/rounding, variable latency operations and reset/state behavior. Compare intermediate and final values, not only whether synthesis completes. Report rejected or repaired transformations and unsupported operations.

### Compiler IR quality is separate from hardware quality

An H-CDFG can be a concise planning representation, but the implementation still needs scheduling, resource binding, memory allocation, buffering, interface generation and backend lowering. The target device determines whether the proposed parallelism fits available compute units, memory ports, interconnect, clock period and routing. Resource reduction can coexist with lower frequency or more buffering; higher kernel parallelism can be hidden by memory or initiation-interval limits.

For each named target, report initiation interval, latency, throughput, frequency, LUT/FF/DSP/BRAM or ASIC area, memory traffic, buffer occupancy, routing/timing closure, power and energy. Include synthesis and place-and-route failures, timing violations, unsupported operations, compiler time, peak memory and manual intervention. Separate time to compile from time for the generated accelerator to execute.

### “State-of-the-art HLS” needs a reproducible boundary

The source reports performance improvement, significant resource reduction and effective capture of kernel parallelism relative to state-of-the-art HLS tools, but supplies no numerical values, benchmark identities, target devices or compilation-time cost. A fair comparison must hold source kernels, numerical precision, device, clock/resource limits, backend versions, timeout, optimization effort and correctness checks constant. It must say whether preprocessing, kernel outlining, code generation, synthesis, place-and-route and final timing checks are included.

Test held-out kernels and targets rather than only the cases used to shape the transformations. Report per-kernel results and failures, resource-versus-frequency tradeoffs, design-space search cost, and whether generated designs were measured on hardware or only estimated by tools. The evidence supports an open-source MLIR/dataflow accelerator-generation direction, not demonstrated reusable hardware-performance improvement across targets.

## CODO connects legality, communication, and scheduling

CODO's captured evidence describes detection and repair of dataflow violations, optimization of data movement, and automatic scheduling for FPGA accelerators. An FPGA is configurable hardware whose available resources and connections constrain the generated implementation. [Recorded evidence](../observed-subthemes/high-level-synthesis-and-compilers.md#paper-isca-2026-program-002)

The conceptual connection is that an attractive schedule is insufficient if the communication structure cannot execute correctly. Repair must restore the required behavior, and the resulting communication and buffering must fit the target. A compiler should account for all these conditions while selecting the implementation.

The repository's evidence includes author preprint and artifact documentation, but does not establish independent reproduction of every synthesis or board result. Reported kernel, model, and board measurements retain their own scopes. A result on one FPGA flow does not by itself establish applicability to all programmable devices or fabricated fixed-function circuits.

## Tool speed and generated-hardware speed are separate outcomes

A compiler can take longer to produce a faster circuit. It can also compile quickly but miss useful implementation choices. The right objective depends on how often the generated circuit is used and how much design time is available.

Measure compilation time, synthesis success, hardware resource use, correctness, and application execution separately. Include failed configurations and manual intervention. State which operations or language features are unsupported rather than excluding difficult inputs without explanation.

## What would establish a reusable improvement

Use the same programs, numerical requirements, device limits, and comparison tools. Preserve tool versions and settings. Check behavior on the generated hardware or a suitable validated model, and report final resource and timing constraints.

Then test new applications and target configurations. Explain which transformations remain useful and which depend on a specific execution or memory organization. The strongest result is a defined transformation process that repeatedly produces valid, useful implementations under explicit conditions.
