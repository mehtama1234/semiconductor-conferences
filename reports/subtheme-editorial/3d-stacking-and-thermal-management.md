## What stacking changes

Placing active silicon layers above one another changes both communication and heat removal. Nearby layers can exchange data through vertical connections, but their heat must still reach the package's cooling surfaces. Power generated in one layer can raise the temperature of another. A design cannot therefore be evaluated from memory bandwidth alone: the useful question is how much computation it sustains without exceeding its temperature limits.

There are three different tasks in this paper group. Prediction calculates temperatures from a proposed structure and power distribution. Reconstruction estimates temperatures from incomplete observations of a running chip. Control changes where and how fast computation runs. An accurate predictor does not by itself establish a safe controller, and a reconstruction result does not establish that a new package can remove more heat.

## Predicting temperatures: what is being simplified?

A detailed numerical solver divides the package into small regions and solves their heat-transfer relationships. Faster methods reduce the number of quantities solved, reuse earlier calculations, or learn an approximation from examples. Their usefulness depends on which details they preserve when materials, cooling, and power distributions change.

[LegoTherm](../observed-subthemes/3d-stacking-and-thermal-management.md#paper-dac-2026-research132) makes reusable reduced-order components: each retains fewer internal quantities than a detailed model and exchanges thermal information at its interfaces. The important question is whether reconnecting those components preserves temperatures near small, strongly coupled structures. The official description reports up to 10.39 times faster analysis than COMSOL and mean relative error below 0.40%. It does not provide the mesh sizes or full error distribution. A small mean error need not bound the error at the hottest location.

<span id="explanation-dac-2026-research132"></span>

### LegoTherm: reduce a stack into reusable thermal modules without losing interface behavior

### Why repeated full simulations are expensive

A detailed finite-element thermal model divides a package into many small elements and solves for temperatures and heat flows throughout the mesh. It can represent small interconnects and material boundaries, but a new power distribution, cooling condition or stack arrangement may require another large solve. Chiplet systems make this cost harder because the design contains structures at several scales: chiplets, interposers, bonding or micro-interconnects, interface materials and cooling paths.

A compact thermal model reduces this cost by replacing many internal variables with a smaller set of states. The reduction is useful only if the remaining variables still describe how heat enters and leaves each reusable part. If the interface state is too small, reassembling modules can produce a plausible average temperature while missing a local hotspot near a dense interconnect or a material boundary.

### What the modular reduction represents

The captured description says LegoTherm first constructs high-fidelity 3D meshes with micro-interconnection detail through modular discretization. It then generates reduced-order modules by aggregating thermally coupled interface ports. A port is an interface quantity through which one module communicates with another, such as temperature or heat flow over a boundary. Aggregating ports reduces the number of coupled variables while attempting to preserve the thermal response seen by neighboring modules.

The modules are reusable because the internal solution is summarized at the boundaries rather than recomputed for every complete package scenario. Reassembly can then change power distributions, cooling conditions or structural combinations by reconnecting the reduced modules. This only works when the module's internal behavior remains valid for the new boundary conditions and power range. A module calibrated for one interface regime may not preserve accuracy when a neighboring chiplet, heat spreader or cooling path changes the heat-flow pattern.

The description reports up to 10.39× speedup over COMSOL, mean relative error below 0.40%, and a reduction in thermal design iteration time from weeks to half a day. These measures have different boundaries. Speedup compares solver time; iteration time may also include geometry preparation, module generation, reassembly, inspection and design changes. Mean relative error summarizes an average; it does not establish the maximum error or hotspot error. “Up to” identifies the strongest reported case, not the typical improvement across all scenarios.

### The evaluation that would establish reusable-module validity

Report mesh resolution, module boundaries, port definitions, aggregation rules, calibration cases and the cost of creating each reduced module. Test reassembly on unseen combinations of chiplets, power maps, cooling conditions and stack structures. Give mean, percentile, maximum and hotspot errors, including errors at micro-interconnects and material interfaces. Compare total design-loop time—not only one solve—against COMSOL and compact thermal models with the same geometry-construction and convergence requirements. Measure whether reduced modules remain accurate when power and boundary conditions fall outside the calibration range.

The [LegoTherm](../observed-subthemes/3d-stacking-and-thermal-management.md#paper-dac-2026-research132) record describes modular discretization and interface-port aggregation for reusable reduced-order thermal models. The detailed explanation above separates detailed mesh construction from reduced representation, interface preservation from reassembly, solver speed from total design-loop time, and mean error from hotspot accuracy; this card is the compact evidence record.

[COOL](../observed-subthemes/3d-stacking-and-thermal-management.md#paper-dac-2026-research1846) instead represents package geometry, material, and power as annotated points and trains a predictor with constraints at material and cooling boundaries. Its reported 2.4% normalized mean absolute error depends on the normalization and test distribution. Neither is specified in the captured description. Testing new cooling structures matters because interpolation among familiar power maps is a different task from predicting a structurally different package.

<span id="explanation-dac-2026-research1846"></span>

### COOL: thermal prediction must represent both the package and its boundaries

### What the thermal prediction problem contains

A package thermal model maps a physical structure and a power distribution to temperatures. The structure includes regions such as dies, interposers, thermal-interface materials (TIMs), heat spreaders and cooling elements. Each region has geometry and thermal properties. Heat crosses interfaces according to those properties and the boundary conditions imposed by cooling surfaces. A predictor that sees only the power placed in a fixed grid can miss the effect of changing a material boundary, adding a heat spreader or moving the cooling path.

The output is a temperature field, not one universal temperature. A mean error can be small while the hottest point, a die-to-die interface or a thin TIM boundary is wrong. That distinction matters because reliability and frequency control often depend on a maximum or local temperature. NMAE must therefore be read with its normalization, spatial weighting and error distribution; the percentage alone does not state the worst hotspot error.

### What COOL changes in the representation and loss

The captured description represents heterogeneous 3D packages as annotated point clouds. Each point carries geometric, material and power attributes. This representation lets the model describe different package components and their locations rather than assuming one fixed rectangular arrangement. The point representation still needs a rule for resolution: a thin interface or narrow cooling channel can disappear if sampling is too coarse, while a finer cloud increases input and preprocessing cost.

COOL uses a cooling-aware point transformer. A transformer combines information across points so the prediction at one location can depend on other parts of the package. The method explicitly encodes geometric boundaries and adds a physics-informed boundary-condition (PI-BC) loss. The loss penalizes predictions that violate the stated thermal behavior at material interfaces and cooling boundaries. This constraint can make the learned output more consistent with the modeled problem, but it does not guarantee correct temperatures when material parameters, boundary conditions or cooling structures differ from training data.

The official description reports 2.4% normalized mean absolute error on a constructed benchmark of multi-package thermal designs and more than 15.7× speedup over commercial finite-element-method solvers. These measurements answer different questions: NMAE describes prediction discrepancy under the benchmark's normalization, while speedup describes elapsed computation under a solver and hardware setup. A surrogate can be faster because it replaces iterative numerical convergence with one learned inference; the comparison must include point-cloud construction, model loading, preprocessing and any solver setup that is excluded from the reported timing.

### The evaluation that would establish a useful package surrogate

Specify package geometries, point resolution, material properties, power maps, cooling boundaries, train/test split and solver convergence tolerances. Report mean, percentile and maximum temperature errors, especially at hotspots and interfaces, instead of only one global NMAE. Test unseen package topologies, materials, cooling structures and power distributions. Measure total time from design description to temperature field, including preprocessing and model execution, and compare against FEM on the same hardware and accuracy target. Finally, test whether errors change design decisions such as hotspot detection, frequency throttling or cooling selection.

The [COOL](../observed-subthemes/3d-stacking-and-thermal-management.md#paper-dac-2026-research1846) record describes a cooling-aware point-transformer surrogate with explicit package boundaries and a physics-informed boundary-condition loss. The detailed explanation above separates temperature-field prediction from hotspot safety, point-cloud representation from resolution cost, physics-informed training from physical validation, and NMAE/speedup from the missing benchmark and timing conditions; this card is the compact evidence record.

<span id="explanation-dac-2026-research553"></span>

### PNO-Therm: transfer a PDE operator before fine-tuning a chip-specific thermal model

### Why thermal data are expensive

A thermal solver maps material structure, power generation and cooling conditions to a temperature field. A separate model trained for each chip needs examples of that mapping for the target geometry and power patterns. Those examples usually come from numerical simulation, so reducing the number of training examples does not remove the cost of generating them; it changes how much of that cost is required for a new design.

Heat conduction and diffusion-type equations share mathematical structure: a quantity spreads through a medium according to local material and boundary relationships. That shared structure motivates pretraining a neural operator on multiple PDE families. A neural operator learns a mapping between fields or functions rather than only memorizing a fixed-size vector-to-vector task. The useful transfer claim is that the pretrained representation already contains features for propagation and boundary-driven change, so thermal fine-tuning needs fewer target-chip examples.

### What PNO-Therm changes

The source describes a foundation neural operator pretrained on diverse PDE families and then targeted fine-tuning for 3D-IC thermal simulation. Fine-tuning adapts the shared model to the target thermal inputs, geometry and output temperature fields. This is different from training a thermal predictor from random initialization for every chip. It is also different from proving that every PDE in pretraining is physically equivalent to a specific 3D-IC package: transfer depends on the overlap between the pretraining equations and the target materials, boundary conditions, geometry and power distributions.

The reported comparisons keep dataset size equal when claiming 6–10× lower mean absolute error, 3.5× lower GPU memory consumption and more than 3× faster training than the previous state-of-the-art learned model. The source separately reports use of less than 20% of the prior training data and approximately 940× speedup relative to FEM. These comparisons must stay separate. Equal-data accuracy compares model quality at one data budget; the less-than-20% result concerns data efficiency; GPU memory and training time are training-resource measures; FEM speedup is inference or analysis-time comparison whose exact boundary is not stated.

A small target dataset can also hide large preparation cost if each example requires a high-fidelity FEM solve. The relevant end-to-end data-efficiency question is the cost of pretraining, target-data generation, fine-tuning, validation and inference for a new package. A fast model can be useful for design-space exploration while still failing on an unseen stack, a new cooling boundary or a power map outside the training distribution.

### The evaluation that would establish transferable thermal modeling

Describe the pretraining PDE families, target thermal equations, input/output fields, mesh or discretization, material and boundary distributions, and exact fine-tuning protocol. Separate designs used for pretraining, adaptation and testing. Report absolute and normalized errors, hotspot errors, error by design, extrapolation to unseen geometries and cooling structures, GPU memory, training time, data-generation time and inference time. Compare from the same target-data budget and from the same end-to-end preparation budget. Compare against FEM at a stated accuracy and convergence target, not only an unspecified solver runtime.

The [PNO-Therm](../observed-subthemes/3d-stacking-and-thermal-management.md#paper-dac-2026-research553) record describes PDE foundation-model pretraining followed by thermal fine-tuning. The detailed explanation above separates shared PDE structure from physical transfer, target-data percentage from total preparation cost, equal-data accuracy from training-resource measures, and learned inference speed from FEM fidelity; this card is the compact evidence record.

The [PNO-Therm](../observed-subthemes/3d-stacking-and-thermal-management.md#paper-dac-2026-research553) record describes a PDE foundation operator adapted to 3D-IC thermal prediction. The detailed explanation above separates shared PDE structure from physical transfer, target-data percentage from total preparation cost, equal-data accuracy from training-resource measures, and learned inference speed from FEM fidelity; this card is the compact evidence record.

[FLASH3D](../observed-subthemes/3d-stacking-and-thermal-management.md#paper-dac-2026-research1065) uses a layered analytical formulation rather than a learned predictor. Its reported maximum absolute error below 0.5 K is a different metric from COOL's normalized average error. Its steady-state scope concerns the settled temperature field; it does not establish accuracy during a changing workload. These reported errors and speedups should not be ranked as if they came from one benchmark.

<span id="explanation-dac-2026-research1065"></span>

### FLASH3D: an analytical steady-state solver reduces repeated numerical work without becoming a transient model

### What steady-state thermal analysis computes

A steady-state thermal problem asks for the temperature field after the modeled heat generation and boundary conditions have settled. It does not describe how quickly the package reaches that state or how temperature changes when power switches between workloads. A transient problem adds time and heat-storage effects, so a method designed for steady state cannot be called a transient simulator without separate evidence.

The input includes the package layers, material properties, cooling boundaries and power distribution. Fine-grained power matters because two designs with the same total power can produce different local hotspots. Curved boundaries and standard-cell-level power maps are harder for simple formulas that assume uniform layers or coarse rectangular sources.

### What the analytical components do

FLASH3D combines three stated components. Spectral modal decomposition represents the spatial temperature field as a combination of basis modes; this can replace a very large set of local unknowns with coefficients for modes that capture the field. The transfer matrix method propagates the relationship between temperature and heat flow across layers. An accelerated power decomposition algorithm breaks a detailed power map into components that can be evaluated and combined efficiently.

These components reduce computation by using the layered structure of the thermal equations. They do not remove the need to specify material interfaces and boundary conditions. The method's advantage depends on how accurately the chosen modes, layer model and power decomposition represent curved edges, thin materials, vertical coupling and fine local sources.

The official description reports more than four orders of magnitude speedup over COMSOL, reducing computation from minutes to milliseconds while keeping maximum absolute error below 0.5 K. Maximum absolute error is the largest pointwise temperature difference under the tested cases. It is stricter than a mean error for that set, but it still depends on the reference solver, mesh or discretization, material parameters, boundary conditions and the points included in the comparison. The description does not provide those conditions or matched per-case runtimes.

The source also reports that, within one DeepOHeat inference time, FLASH3D computes roughly 2,000 slices and reaches approximately 10× lower error. This is a throughput-and-error comparison against a learned method, not a direct comparison with the COMSOL result. “One inference time” must be tied to preprocessing, batch size, hardware and whether FLASH3D's setup time is included before the claim can be reproduced.

### The evaluation that would establish a reliable early-design simulator

Report the layer geometry, material and boundary parameters, power-map resolution, curved-boundary treatment, standard-cell aggregation rule and reference discretization. Separate steady-state error from transient response and test local hotspots, interfaces and cooling boundaries. Give per-case runtimes, hardware, preprocessing, memory use and solver tolerances for COMSOL, DeepOHeat and FLASH3D. Test changes in geometry, material and power maps rather than only repeated cases from one design family, and show whether the temperature errors change a floorplan, cooling decision or thermal-throttling decision.

The [FLASH3D](../observed-subthemes/3d-stacking-and-thermal-management.md#paper-dac-2026-research1065) record describes spectral decomposition, transfer matrices and accelerated power decomposition for 3D steady-state thermal analysis. The detailed explanation above separates settled temperature from transient behavior, analytical speed from reference fidelity, maximum error from average error, and DeepOHeat slice throughput from the COMSOL comparison; this card is the compact evidence record.

## Reconstructing and controlling a running system

[Seeing Through Silicon](../observed-subthemes/3d-stacking-and-thermal-management.md#paper-dac-2026-research1907) combines sparse temperature sensors with activity counters. Sensors measure only selected locations; counters provide indirect information about heat generation. Combining them may reduce ambiguity about unobserved temperatures. The description reports 0.48°C reconstruction RMSE and 0.95-second inference, but does not specify sensor layout or spatial resolution. Whether that delay suits control depends on how quickly the system heats, how often control runs, and the cost of a missed hotspot.

<span id="explanation-dac-2026-research1907"></span>

### Seeing Through Silicon: reconstructing hidden temperatures is an observability problem

### Why neither input modality is enough

A 3D-IC temperature field has a value at many locations across several layers. On-chip thermal sensors observe temperature only at their physical locations. They provide local state but leave the regions between sensors and other tiers unmeasured. Performance counters provide indirect evidence about activity and heat generation, but they do not directly say how heat spreads through materials, interfaces, cooling paths or neighboring layers.

The reconstruction task therefore has two parts: infer where heat is being generated, and infer how that heat is transported through the 3D structure. A model trained only on counters can miss transport and boundary effects. A model trained only on sparse sensors can miss a hotspot outside the sensor layout. Combining the signals can reduce ambiguity, but only if the model learns the relation between observations, power and the thermal field under the relevant physical conditions.

### What the physics-informed conditional diffusion model does

The captured description treats reconstruction as constrained inference over the heat equation. The heat equation relates temperature change to heat generation, material-dependent transport and boundary conditions. A physics-informed model adds a penalty or constraint so that a proposed temperature field is not only statistically plausible from the observations but also consistent with the stated thermal relationships.

The method uses a conditional diffusion framework. In this setting, diffusion sampling generates a field conditioned on the available sensor readings and performance-counter signals. The conditioning supplies evidence about the particular running state; the heat-equation constraint limits physically inconsistent completions of the unobserved volume. The architecture explicitly models vertical inter-layer coupling, which is necessary because heat from one tier can affect temperatures in another tier.

The source reports deterministic sampling. This matters for runtime because repeatedly sampling many possible fields would increase inference cost. Deterministic sampling can produce one repeatable reconstruction path, but repeatability is not the same as uncertainty estimation. A monitoring controller also needs to know when the observations are insufficient and the reconstructed hotspot is uncertain.

### What the reported numbers establish

The official description reports 0.48°C RMSE versus 13.08°C for single-source baselines, described as more than 94% lower estimation error, and reports an inference time of 0.95 seconds versus 147 seconds for finite-element simulation. It also reports R² above 0.99 against the FEM reference. RMSE measures an aggregate discrepancy over the evaluated field and cases; it does not identify the maximum local error or whether the error is concentrated near a safety-critical hotspot. R² indicates explained variance relative to the reference distribution; it does not guarantee correct absolute temperature at every location.

The 0.95-second reconstruction time can support control only relative to the system's thermal time scale and control period. A controller needs enough time to observe, reconstruct, decide, and apply an action before a temperature limit is crossed. The source does not report sensor layout, spatial resolution, sensor drift, unseen power traces, FEM configuration, controller period, actuation delay, or closed-loop temperature violations. The evidence therefore supports multimodal reconstruction, not a demonstrated safe dynamic thermal-management loop.

### The evaluation that would establish observability and control value

Report sensor count and placement, counter semantics, tier geometry, power traces, thermal parameters, reconstruction resolution and train/test split. Test unseen power maps, sensor failures or drift, changing cooling conditions and hotspots between sensors and across tiers. Report per-location and per-tier errors, maximum error, hotspot detection recall, false alarms, uncertainty calibration and inference latency on the target controller hardware. Then close the loop: measure decision latency, actuation cost, temperature-limit violations, performance loss and energy under matched baselines.

The [Seeing Through Silicon](../observed-subthemes/3d-stacking-and-thermal-management.md#paper-dac-2026-research1907) record describes physics-informed conditional-diffusion reconstruction from sparse sensors and activity counters. The detailed explanation above separates heat generation from transport, local observation from volumetric inference, aggregate RMSE/R² from hotspot safety, and reconstruction speed from closed-loop control evidence; this card is the compact evidence record.

[AILFM](../observed-subthemes/3d-stacking-and-thermal-management.md#paper-dac-2026-research1302) learns thread-migration and voltage/frequency choices from reference policies. Moving work can change temperature and cache access time simultaneously. A useful evaluation must charge for migration, data movement, and policy execution, and check temperature violations rather than only average performance. Those numerical results are absent from the captured description.

<span id="explanation-dac-2026-research1302"></span>

### AILFM: scheduling LFM inference requires a joint thermal, locality and kernel policy

### What the scheduler controls

Large foundation-model inference is a sequence of different kernels. Some kernels perform substantial arithmetic; others repeatedly read weights, activations or key/value state. On a many-core system, a thread's location affects which cache and network path it uses. In a 3D static non-uniform cache architecture (S-NUCA), cache access latency depends on the source and destination locations and on the 3D network-on-chip path.

The scheduler has at least two physical controls. Thread migration changes where work executes and can improve access locality or load balance, but it moves execution state and may cause additional cache or network traffic. Voltage/frequency (V/f) scaling changes performance and power: a higher operating point can complete work sooner while increasing heat generation, and a lower point can reduce power while extending the time the system remains active. These controls interact because migration changes both access latency and where power is generated.

The thermal state is also delayed. Heat accumulates and propagates through the stack rather than changing only at the instant a scheduling action occurs. A policy that reacts to current temperature alone can miss a future hotspot; a policy that lowers frequency too aggressively can preserve temperature headroom while harming inference latency. The useful decision must account for current observations, kernel behavior, core variation, cache locality and the thermal consequence of the action.

### What active imitation learning contributes

The captured description presents AILFM as an active-imitation-learning scheduler trained from Oracle demonstrations. An Oracle is a reference policy that selects actions using information or computation not available to the deployed lightweight scheduler. Imitation learning trains the deployed policy to reproduce those decisions from observable features. “Active” indicates that the learner selects or emphasizes informative examples rather than treating every demonstration as equally useful; the source does not specify the query rule or Oracle construction.

AILFM is described as using core-level performance variation and kernel-specific behavior as policy inputs. This matters because one fixed action can have different effects on different cores and kernels. A policy that copies only average system behavior may migrate a memory-heavy kernel onto a path with poor cache latency or raise frequency on a thermally constrained tier. The source's qualitative claim is that the learned policy generalizes across diverse LFM workloads, but no workload list, trace split, Oracle gap or unseen-kernel test is supplied.

### What the captured evidence does and does not show

The official description says AILFM outperforms state-of-the-art scheduling baselines and maintains thermal safety, but it provides no numeric latency, throughput, energy, temperature, migration overhead, policy overhead or generalization values. “Thermal safety” needs a temperature threshold, sampling period, spatial scope, duration and violation rule. “Performance” needs a defined end-to-end inference metric and must include any migration, cache warm-up, network traffic, policy execution and V/f transition cost.

Because the result is a policy learned from an Oracle, the Oracle's quality and information access are part of the experiment. A policy can appear near-optimal if its demonstrations use future information, exact simulator state or a workload distribution unavailable at deployment. The comparison must therefore separate Oracle generation, training traces, held-out traces and truly unseen kernels, and report the cost of the policy itself.

### The evaluation that would establish a safe scheduling result

Report the 3D stack, core and cache topology, NoC latency, V/f states, thermal model, temperature limits and control interval. Give workload and kernel traces, Oracle objective and information, train/test split, migration and transition costs, policy latency, throughput or tail-latency, energy, peak and per-tier temperature, and the number and duration of thermal violations. Test workload phase changes, unseen kernels, heterogeneous core speeds, cache contention and sensor/model error. Compare thermal-only, locality-only, static V/f and non-learned policies under equal action costs.

The [AILFM](../observed-subthemes/3d-stacking-and-thermal-management.md#paper-dac-2026-research1302) record describes active imitation learning for kernel- and core-aware thread migration and V/f control on 3D S-NUCA many-cores. The detailed explanation above separates migration from V/f effects, cache locality from thermal transport, Oracle imitation from independent optimality, and qualitative safety claims from the missing end-to-end policy measurements; this card is the compact evidence record.

[Tasa](../observed-subthemes/3d-stacking-and-thermal-management.md#paper-iccad-2025-1103) combines different core types, thermal balancing, and bandwidth sharing for language-model inference. Its abstract reports temperature reductions separately for three core counts. Those conditions must stay attached to the numbers; they do not establish a package-independent benefit or measured silicon operation.

<span id="explanation-iccad-2025-1103"></span>

## Tasa: treat thermal headroom and memory bandwidth as one architecture problem

### The workload creates two different bottlenecks

LLM inference has a prompt-processing stage and an autoregressive decoding stage. During prompt processing, many tokens can be handled together. During decoding, each new token depends on the previously generated sequence and the stored key/value cache. This makes decoding sequential at the request level and repeatedly reads a large amount of data.

Tasa starts from the claim that 3D stacking can supply more memory bandwidth by placing several DRAM dies above a logic die. That solves a data-supply problem but changes the thermal problem. The logic die sits farther from the heat sink and concentrates compute power beneath the memory stack. Adding cores can therefore increase bandwidth and arithmetic capacity while raising local temperature, thermal gradients and frequency throttling.

The method has two coupled parts. It places high-performance P-cores, with systolic arrays for compute-intensive GEMM/fully connected layers, beside high-efficiency E-cores, with MAC-tree arrays for memory-intensive GEMV/attention layers. It then shares unused P-core bandwidth with E-cores by moving part of the KV cache and scheduling cache placement according to batch size and current bandwidth use. The thermal design changes where power is generated; the dataflow design changes which memory channels carry the work.

### The thermal analysis establishes why placement matters

The paper simulates a four-layer memory stack with 8 TB/s bandwidth and a 48-core GPU-like logic die delivering 196 TFLOPS. It uses HotSpot 6.0 for GPT-3 66B inference with batch size 32. Under the stated model, the logic die reaches a simulated peak of 361.79 °C while the DRAM layers are reported between 355.66 and 359.11 °C. These are simulator outputs under the paper's thermal parameters, not measured temperatures of a fabricated stack.

The important result is spatial, not only absolute. The 3D design has a reported hotspot gap of 11.1 °C versus 2.5 °C for the comparable 2D distribution. When the number of processing-element cores grows from 24 to 72, the simulated peak rises by 23.3 °C in 3D and 15.3 °C in 2D. Increasing the distance between cores lowers the simulated peak by 10.32 °C, but increases area to 2.25 times. This exposes the design tradeoff: spacing can reduce heat concentration, but it consumes the area that makes high parallelism useful.

Thermal temperature, gradient and scalability are different conditions. A design can have an acceptable average temperature while containing a local hotspot, or remain below a limit at one core count while becoming infeasible when scaled. Tasa therefore evaluates floorplan and core-ratio choices instead of applying one global temperature correction after the architecture is fixed.

### Heterogeneous cores create a controlled tradeoff

The 48-core configuration uses four 12-GB DRAM dies, 48 GB per stack, 768 banks per die and 16 banks per core. Each logic core has 128 KB of SRAM, and the base frequency is 1 GHz. The P-core contains two 32×32 systolic arrays and targets GEMM. The E-core contains twelve 32×1 MAC trees and targets GEMV-like attention. The E-core can read from local DRAM or bypass parts of the local buffer, which reduces redundant movement for attention's memory-heavy operation.

The core ratio is not a cosmetic configuration. More P-cores can raise peak compute throughput and power density. More E-cores can spread heat and serve attention efficiently, but may reduce peak GEMM throughput. Tasa explores 3:1 and 5:1 P:E ratios and varies E-core placement, including increased central clustering. The selected floorplan changes the heat sources themselves; it is not equivalent to migrating a fixed workload after a hotspot appears.

The architecture uses a hierarchy of communication. P-cores connect directly to a root E-core inside a group; E-cores connect groups through a router-based global network. This lets an E-core coordinate local bandwidth sharing while the global mesh handles inter-group communication. The paper's claim depends on this topology because the cache and bandwidth path must exist before the scheduler can exploit it.

### Bandwidth sharing is a cache-allocation problem

The dataflow maps fully connected layers to P-cores and attention layers to E-cores. The QKV/projection work is pipelined with attention at head granularity, and tensor parallelism spans multiple devices. Parameters are partitioned to avoid remote memory access; the KV cache is initially held in E-cores.

During a fully connected operation, P-cores may not use all of their local DRAM bandwidth because batching creates reuse. During the attention phase, E-cores need KV-cache bandwidth. Tasa uses the otherwise unused P-core bandwidth through the local fat-tree network. For one attention head, the paper models latency as `max(KV_P / BW_shared, KV_E / BW_core)`. The cache split should therefore balance the two terms rather than place all KV data in one core type.

`BW_shared` changes with P-core activity and batch size. Tasa maintains a batch-size-indexed lookup table, records current cache allocation, and migrates KV data as the batch changes. The allocation is not free in the abstract: it must preserve the next iteration's useful cache, hide migration latency where possible, and handle both increasing and decreasing batch sizes. This is why the scheduling mechanism is part of the architecture result rather than a separate software optimization.

### Read the reported measurements with their denominators

The evaluation uses LLaMA-65B and GPT-3 66B in FP16/BF16, conversational requests sampled from ShareGPT, dynamic request addition for stable batch sizes, and Poisson arrivals for QPS experiments. The temperature threshold is 85 °C in the model; DVFS triggers when the maximum exceeds that threshold. Baselines are eight A100 40 GB GPUs, eight A100 GPUs plus AttAcc PIM, and an eight-device homogeneous 3D-stacked accelerator with the same overall Tasa configuration.

The simulator combines Timeloop, Accelergy, Ramulator 2.0, HotSpot 6.0 and an AttAcc-derived framework. Operator performance uses Timeloop and DRAM accesses use Ramulator; energy and area use extended Accelergy/FinCACTI assumptions, including ASAP7 logic and modeled stacked DRAM. The result is a multi-tool simulation study. It is not a chip measurement or a demonstrated package with the stated thermal materials.

For batch size 32 and input/output lengths 512/512, Tasa's average peak-temperature reduction versus Homo-3D is 3.96 °C, 6.10 °C and 5.99 °C for 48, 60 and 72 cores. Across frequency comparisons, the paper reports ranges of 3.63–5.55 °C, 5.73–9.37 °C and 5.12–7.91 °C for those core counts. The range and average answer different questions; the abstract's 5.55/9.37/7.91 values are maxima within the explored settings.

For the 48-core performance comparison, the paper reports average throughput speedups of 2.85× over A100-only, 2.12× over A100+AttAcc and 1.33× over Homo-3D. It reports average energy-efficiency improvements of 2.07× and 1.61× over A100-only and A100+AttAcc, and up to 3.35× performance in a stated comparison. Without bandwidth sharing, Tasa's latency is worse than Homo-3D at increasing QPS; with sharing it outperforms Homo-3D. The results therefore do not support attributing the performance to thermal heterogeneity alone. The P/E design, cache placement, bandwidth sharing, frequency response and simulation baselines jointly produce the reported result.

### What the paper establishes and what remains open

Tasa provides a coherent architecture-level mechanism: allocate compute-heavy and memory-heavy operators to different core structures, place those structures to flatten heat flow, and use temporarily unused bandwidth to serve KV-cache reads. Under its modeled 3D stack, thermal parameters, 85 °C policy, selected core ratios, workloads, traffic and simulator stack, it reports lower peak temperature and higher simulated throughput than its baselines.

It does not establish fabricated-silicon temperature, package-level cooling feasibility, area/cost including manufacturing, controller and migration overhead under all request patterns, or transfer to other memory stacks and thermal interface materials. It also does not show that the 85 °C DVFS policy exactly matches a physical device's reliability limit. The 361.79 °C simulated value illustrates the need to understand the model and threshold conventions; it should not be repeated as a physical operating claim.

The long-term question is whether 3D architecture should be optimized on a joint thermal-throughput frontier rather than by maximizing memory bandwidth first and fixing heat later. Tasa supports that hypothesis for a specific simulated design space. A stronger result would require a reproducible stack model, calibrated thermal parameters, explicit migration cost, matched end-to-end baselines, and eventually package or silicon measurements.

[Recorded paper evidence](../observed-subthemes/3d-stacking-and-thermal-management.md#paper-iccad-2025-1103)

## The cross-paper question

The research opportunity is to connect fast estimation to decisions that remain safe when the estimator is wrong. That is a hypothesis motivated by this group, not a demonstrated historical trend. A convincing comparison would use common package structures, calibrated references, unseen power maps, hotspot errors, total analysis cost, and sustained throughput under the same temperature limit.
