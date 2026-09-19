## Why computation is usually separated from stored values

A conventional processor reads values from memory into execution resources, performs operations, and writes results. This arrangement permits flexible computation, but repeated transfers can consume substantial time and energy. Increasing the number of arithmetic units helps only if their input values can arrive quickly enough.

Processing in memory places some computation within memory structures or close to them. The intended saving is reduced movement across an expensive connection. The method must still explain how inputs are arranged, which operations the memory-side hardware supports, and how outputs reach the rest of the application.

## The location of saved traffic must be explicit

Moving computation toward memory can reduce processor-to-memory transfers while leaving movement inside the memory system. If data must be copied into a special layout first, that preparation can be substantial. A result may also need conversion or additional processing on the host processor.

The evaluation should therefore trace the complete sequence: place inputs, execute the supported operation, extract results, and complete the unsupported operations elsewhere. The saving in one step is useful only after the costs of the full sequence are considered.

## Different memory technologies permit different operations

Memory cells, access circuits, and data converters have different electrical behavior. A computation performed by digital logic beside an array has different precision and variation concerns from one that relies on analog behavior inside the array.

An analog-to-digital converter measures an analog signal and represents it digitally. Its resolution, speed, and energy can limit the surrounding computation. A digital implementation can instead face limits in supported arithmetic, data arrangement, and communication. The name “compute in memory” by itself does not specify either implementation.

## What the four records contribute

Freebit's captured record concerns low-bit model inference using processing in memory. Fewer bits reduce stored representation size, but useful execution requires arithmetic and conversion that preserve the desired model output. The description does not establish the complete precision, performance, energy, or conversion conditions. [Recorded evidence](../observed-subthemes/processing-in-memory-and-memory-centric-compute.md#paper-dac-2026-research146)

<span id="explanation-dac-2026-research146"></span>

## FreeBit: low-bit PIM is useful only when model quality and the complete memory path survive

Quantizing an LLM weight from higher precision to 1, 2 or 4 bits can reduce storage and arithmetic, but it does not automatically reduce end-to-end inference time. A roofline limit can move the bottleneck from computation to memory bandwidth: even a large reduction in operations may produce little speedup if weights, activations, metadata, partial sums or conversions still dominate. PIM changes where some of that work occurs; it does not remove the work or the quality contract.

FreeBit is described as a hardware-software PIM co-design. Its hardware uses a LUT-centric architecture for quantized computation and a sparsity-aware memory optimization; its software uses static/dynamic decoupled scheduling to expose PIM parallelism. These mechanisms target redundant arithmetic, memory access and scheduling stalls. The captured description does not specify the memory technology, LUT precision, sparse encoding, activation/KV precision, peripheral conversion path, operator coverage, mapping or scheduler overhead.

The first gate is model fidelity. Report perplexity and task accuracy by model, sequence length and generation setting, with the quantization and calibration procedure, activation/KV precision, accumulation, dequantization, saturation, outlier handling and layer-wise error. If LUT approximation or analog PIM is used, include device variation, noise, ADC/DAC error and temperature assumptions. A smaller representation or fewer MACs is not an accuracy result.

The second gate is complete data movement. Trace weight and activation loading, LUT access, sparse metadata, partial sums, array reads, conversions, host/PIM transfers, synchronization, unsupported operators and output materialization. State whether sparsity is structural or input-dependent and include metadata cost. Evaluate static/dynamic scheduling under different sequence lengths, batches, bank contention, load skew and tail latency; average PIM utilization can hide a straggler or a saturated host link.

The source motivates FreeBit with a 6.7× computation reduction that yields limited speedup under an NVIDIA A100 roofline, and reports notable performance improvement over CPUs, GPUs and prior PIM baselines. It does not expose latency, throughput, energy, area, perplexity/accuracy, memory traffic, conversion overhead, model identities or per-workload results. Compare at the same model quality, quantization, sequence/batch workload, memory capacity, compiler/runtime and end-to-end boundary, including calibration, mapping, compilation and transfers.

The evidence supports a low-bit PIM co-design direction, not demonstrated accuracy-preserving LLM inference, device-validated PIM efficiency or universal end-to-end superiority.

OpenACMv2 makes accuracy an explicit condition in selecting an approximate compute-in-memory design. The key question is how application accuracy is assessed while circuit and algorithm choices change together. A valid accuracy constraint needs a defined task, input population, and acceptance rule. [Recorded evidence](../observed-subthemes/processing-in-memory-and-memory-centric-compute.md#paper-dac-2026-research2014)

<span id="explanation-dac-2026-research2014"></span>

## OpenACMv2: an accuracy budget is useful only when approximation and circuit variation are evaluated together

Approximate digital compute-in-memory trades numerical fidelity for power, performance or area. The trade is meaningful only relative to an application-quality requirement. Architecture choices such as compressors and SRAM parameters determine the nominal operation, while transistor variation, PVT, parasitics and layout can change the actual error and timing. A predicted PPA point or average task accuracy cannot stand in for the joint distribution.

OpenACMv2 is described as a two-level Accuracy-Constrained Co-Optimization flow. At the architecture level it searches compressor combinations and SRAM macro parameters using a GNN surrogate for PPA and error. At the circuit level it sizes standard cells and SRAM bitcells with variation- and PVT-aware Monte Carlo. The separation can make exploration tractable, but it also creates a handoff question: the architecture surrogate and circuit samples must represent the same error and cost that the application will experience. The captured description does not specify the accuracy metric, surrogate uncertainty, circuit models, Monte Carlo sampling or handoff rule.

The first gate is the accuracy contract. Define the task and input population, exact baseline, metric, acceptable degradation, calibration procedure and statistical confidence. Validate final approximate hardware or an independent numerical model on ordinary and rare inputs, not only surrogate-predicted error. For neural workloads, report layer-wise and end-to-end error; an average metric can conceal a small number of inputs or layers that cause a large application failure.

The second gate is variation-aware PPA. Propagate compressor error, SRAM read/write variation, voltage, frequency, temperature, process corners, mismatch, parasitics and timing through the same network. Report area, energy, delay, error and yield distributions, timing failures and Pareto fronts. Monte Carlo makes a distribution visible; it does not prove that the sampled model matches silicon variation or that the selected design is robust outside the sampled conditions.

The official description claims strong PPA–accuracy tradeoffs, robust convergence and rapid what-if exploration using FreePDK45 and OpenROAD. It does not expose accuracy values, PPA definitions, surrogate error, convergence curves, Monte Carlo count, circuit conditions, yield or final application results. Compare exact, uncoupled approximate and jointly optimized flows with equal task quality, process, tools, constraints and search budget, including GNN training, sizing, layout/extraction, rejected candidates and final validation.

The evidence supports accuracy-constrained approximate-DCiM co-optimization, not demonstrated application-safe PPA improvement or process-independent yield.

<span id="explanation-dac-2026-research401"></span>

## PAGE: co-design the DRAM operation and the GEMV schedule

PAGE targets general matrix–vector multiplication in the memory-bound decoding phase of large language models. Its four named mechanisms—mat-level parallelism, inversion-enabled sense amplifiers, AP-based source–destination row copy and adaptive adder-tree accumulation—change where the work occurs and how many DRAM-side cycles are needed. They do not by themselves define the numerical representation, operand layout, control sequence or output-quality contract.

The evidence has three boundaries. Baseline processing-using-DRAM operations are demonstrated on a COTS DRAM–FPGA platform for functionality and timing. Modified PAGE circuits are evaluated in TSMC 16 nm at circuit level. Throughput and energy are then estimated with an in-house system simulator. A COTS baseline demonstration is not fabricated PAGE silicon, and a 16 nm circuit model is not a commercial DRAM product.

DRAM-side logic must respect activation, sensing, restore, charge sharing, timing, refresh and disturbance constraints. The evaluator should report mat/bank geometry, row setup and copy cycles, sense-amplifier margins, PVT and variation, retention, refresh interference, controller legality and failure rates. It should also count data placement, layout conversion, control, output extraction and unsupported operations; saved interface traffic can be replaced by movement inside the memory system.

GEMV correctness is separate from cycle reduction. Define operand signedness and precision, accumulation width, rounding/saturation, error tolerance and exact-reference comparison. Test dimensions, weight and activation distributions, batches, sequence lengths and representative LLM layers. An approximate or simulator-only result can look fast while producing unacceptable logits or generation quality.

The captured description reports up to 14× end-to-end throughput and 3.1× energy improvement over state-of-the-art PUD designs. These are bounded system-analysis claims: absolute values, simulator calibration, baseline implementation, refresh and controller costs, FPGA/host overhead, and full LLM generation coverage remain unavailable. The evidence supports PUD GEMV architecture–circuit co-design, not demonstrated fabricated PAGE deployment, numerical equivalence or transferable end-to-end LLM efficiency.

[Recorded evidence](../observed-subthemes/processing-in-memory-and-memory-centric-compute.md#paper-dac-2026-research401)

<span id="explanation-dac-2026-research752"></span>

## CQ-CiM: shape the representation and the array together

An embedding is a vector whose distances or inner products determine which corpus items are retrieved. RAG systems usually prefer high-dimensional, higher-precision vectors, while a CiM array may expose fewer bits, a fixed row/column shape and analog computation with device-dependent error. Forcing the vector into the array after the embedding model is trained creates a representation gap: the hardware may fit while the nearest-neighbor ordering changes.

CQ-CiM is described as jointly compressing and quantizing embeddings for different CiM implementations, including SRAM, ReRAM and FeFET examples with 2-bit cells and 512×512 arrays. Joint compression and quantization can coordinate dimension, precision and array mapping, but they do not guarantee that the resulting vectors preserve retrieval semantics. The paper needs to state the shaping objective, whether the encoder is retrained or distilled, how queries and corpus vectors are transformed, and how the index is rebuilt.

Retrieval quality is the first gate. Compare distance distortion, top-k recall, precision, NDCG or MRR, and downstream RAG groundedness against unshaped embeddings, dimension-only shaping, precision-only quantization and digital retrieval. Use held-out queries, changing corpus distributions and the same index/search policy. A reconstruction error or norm preservation can look good while moving a relevant item below the top-k boundary.

Hardware validity is a second gate. Cell precision, array dimensions and nominal mapping are not enough: ADC/DAC resolution, conductance range, noise, variation, IR drop, saturation, accumulation, temperature and calibration drift can change the similarity score. Evaluate per-array and per-device behavior, query/database placement, remapping or rejection, and the energy and latency of shaping, indexing, analog conversion, host transfers and result selection.

The official description supplies no quantitative retrieval, device or system result. The evidence supports hardware-aware embedding shaping, not demonstrated robust CiM retrieval quality or end-to-end RAG improvement across device technologies.

[Recorded evidence](../observed-subthemes/processing-in-memory-and-memory-centric-compute.md#paper-dac-2026-research752)

## What would establish a transferable benefit

State the memory technology, supported operations, input and output formats, capacity, and operating conditions. Measure the complete workload at a fixed answer-quality requirement. Include loading, calibration, conversion, control, and host-side work.

Vary data size, precision, and relevant device conditions. If the evaluation uses a device model, identify how the model was calibrated and which variation or noise assumptions it includes. A low energy per array operation is one component result. A system-level energy or performance claim requires the full input-to-output path.

All four selected records currently rely on official descriptions with substantial experimental gaps. They support the classification of proposals. They do not yet provide enough common conditions to rank the methods or establish broad superiority of memory-side computation.
