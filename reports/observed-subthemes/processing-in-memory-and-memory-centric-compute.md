# Processing in memory and memory centric compute

This subject has 4 records in the selected sample. This page explains where it fits, then presents all captured paper evidence without shortening the measurements or limitations.

[Definitions used in the paper records](../reading-guide-v1.md)

## Understand the parent subject first

- [Memory interconnect and storage](../themes/memory-interconnect-and-storage.md)

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

## Compare the results carefully

First identify the inputs and required output quality. Then identify the limited resource: time, memory, communication, energy, circuit area, or correctness coverage. Ask which part of the method reduces that cost and which new cost it adds. Compare numbers only when the experiments hold these conditions sufficiently similar.

A conference description may explain the proposal while omitting the full experiment. An author preprint link may have been coded from its abstract. The source classification does not by itself establish that every table was read. Missing locations remain visible below.

## Complete captured evidence

These are evidence records, not substitutes for the explanations above. Each record preserves its problem, proposed method, measurements, comparison conditions, and source limits. A populated record does not establish that its mechanism has been fully explained or independently verified.

<span id="paper-dac-2026-research146"></span>

### Freebit: Unleashing the Performance Potential of Low-Bit LLMs Through PIM

DAC 2026 · Record: `dac-2026-research146`

[Read the step-by-step explanation](#explanation-dac-2026-research146)

**Updated source-backed reading card**

Reviewed 2026-09-09. Deepens the FreeBit treatment into a paper-level reading; separates LUT-centric low-bit PIM arithmetic, sparsity-aware memory optimization and static/dynamic scheduling from quantization error, analog/digital non-idealities, memory traffic, conversion overhead and full LLM quality/serving cost, while preserving the source's 6.7x roofline context and qualitative performance claims without inventing results.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Low-bit LLM weights reduce computation and storage, but inference can remain memory-bandwidth bound; PIM must exploit the low-bit representation without changing model behavior or shifting cost into conversion and coordination.

**Mechanism / artifact:**

FreeBit is a hardware-software PIM co-design with a LUT-centric architecture for quantized computation, sparsity-aware memory optimization to reduce accesses and exploit PIM bandwidth, and static/dynamic decoupled scheduling to expose PIM parallelism; memory technology, LUT precision, sparsity format, mapping, ADC/DAC or digital peripheral path and scheduler overhead are unspecified.

**Workload — the work tested:**

Low-bit LLM inference with weights quantized to 1/2/4 bits; model families, layer/operator coverage, activation/KV precision, sequence lengths, batch/concurrency, sparsity pattern, quantization/calibration method, quality metric, context/generation workload and baseline tuning are unspecified.

**Hardware and manufacturing assumptions:**

PIM memory arrays and near-memory compute for low-bit LLM operations compared with CPUs, GPUs and prior PIM baselines; memory technology, array organization, capacity/bandwidth, compute units, LUT storage, ADC/DAC or digital arithmetic, host link, compiler/runtime, area, power, temperature and device variation are unspecified.

**Baseline — the comparison method:**

CPU low-bit LLM inference

GPU low-bit inference

Prior PIM low-bit/LLM architecture

Digital memory-centric accelerator

Same model, quantization/calibration, quality target, sequence/batch workload, memory capacity, precision, compiler/runtime, hardware and end-to-end timing/energy boundary are unspecified

**Reported measurements:**

The source motivates FreeBit with a 6.7x computation reduction that yields limited speedup under a memory-bandwidth roofline and reports notable performance improvements over CPUs, GPUs and prior PIM baselines, but gives no latency, throughput, energy, area, perplexity/accuracy, memory traffic, conversion overhead, model list or per-workload result.

**Limits on the conclusion:**

Low-bit arithmetic is useful only if model quality survives the complete inference path. Report perplexity and task accuracy by model, sequence length and generation setting, including calibration, activation/KV precision, accumulation, dequantization, saturation, outliers and layer-wise error. A smaller weight representation or fewer operations does not establish equivalent outputs, especially when LUT approximation or analog PIM non-idealities are present.

Trace data movement rather than counting only avoided MACs: weight loading, LUT access, sparse metadata, activations, partial sums, conversions, array reads, host/PIM transfers, synchronization and unsupported operators. State whether sparsity is structural or input-dependent, how it is encoded, and include metadata and skipped-work overhead. Static/dynamic scheduling must be evaluated under skew, batch variation, sequence growth, bank contention and tail latency.

Compare CPU, GPU and prior PIM systems at the same model quality, quantization method, sequence/batch workload, memory capacity, compiler/runtime and end-to-end boundary. Include calibration, mapping, compilation, initialization, transfers, rejected/unsupported layers and output materialization in performance and energy. The evidence supports a low-bit PIM co-design direction, not demonstrated accuracy-preserving LLM inference, device-validated PIM efficiency or universal end-to-end superiority.

**Source and location**

Evidence tier: Primary captured official DAC description plus existing authored PIM discussion; no full paper extraction, independent LLM quality reproduction, device/non ideality validation or complete latency/energy accounting. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH146&sess=sess138)

DAC 2026 official description; existing processing-in-memory-and-memory-centric-compute chapter framing; captured Problem, Mechanism / artifact, Workload, Hardware, Baseline, Measurements and Limits fields; no manuscript pages, model/quality table, memory-traffic trace, device conditions or reproduced PIM evaluation.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** GPU low-bit inference

digital memory-centric accelerator

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH146

**Hardware or process assumptions:** PIM memory array with low-bit operations; device, ADC/DAC, and host-link assumptions are unspecified.

**Limits:** No perplexity, latency, throughput, energy, area, or conversion overhead results are reported.

Analog PIM non-idealities may affect quality.

Official description only; device-aware evaluation is required.

**Method or artifact:** Processing-in-memory architecture or dataflow for low-bit LLMs.

**Metrics:** PIM performance potential is claimed qualitatively

**Problem:** Low-bit LLM inference remains constrained by memory movement and PIM support for quantized arithmetic.

**Workload or benchmark:** Low-bit LLM inference; models, sequence lengths, quantization, and PIM technology are unspecified.

</details>

<span id="paper-dac-2026-research2014"></span>

### OpenACMv2: An Accuracy-Constrained Co-Optimization Framework for Approximate DCiM

DAC 2026 · Record: `dac-2026-research2014`

[Read the step-by-step explanation](#explanation-dac-2026-research2014)

**Updated source-backed reading card**

Reviewed 2026-09-09. Deepens the OpenACMv2 treatment into a paper-level reading; separates accuracy-constrained architecture search, GNN PPA/error surrogate, compressor/SRAM choices, variation/PVT-aware Monte Carlo sizing and OpenROAD/FreePDK45 integration from accuracy definition, surrogate calibration, circuit variation, Pareto validity and full application/system cost.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Approximate digital compute-in-memory can improve PPA by accepting controlled numerical error, but architecture-level approximation and transistor-level variation are coupled and must be selected under an explicit application-quality constraint.

**Mechanism / artifact:**

OpenACMv2 operationalizes Accuracy-Constrained Co-Optimization through architecture search over compressor combinations and SRAM macro parameters using a GNN surrogate for PPA and error, followed by variation- and PVT-aware Monte Carlo transistor sizing for standard cells and SRAM bitcells; accuracy constraint, surrogate training/uncertainty, optimizer coupling, circuit models, sampling and handoff criteria are unspecified.

**Workload — the work tested:**

Approximate DCiM neural-network or matrix workloads evaluated with FreePDK45 and OpenROAD; model/task, accuracy metric and budget, DCiM array dimensions, compressor options, SRAM parameters, voltage/frequency, PVT corners, mismatch distribution, Monte Carlo count and exact/approximate baselines are unspecified.

**Hardware and manufacturing assumptions:**

Digital compute-in-memory arrays with approximate compressors and SRAM macros, standard cells and SRAM bitcells; FreePDK45/OpenROAD compatibility is claimed, but memory organization, process rules, voltage, frequency, parasitics, layout, timing/power extraction, yield and silicon status are unspecified.

**Baseline — the comparison method:**

Exact DCiM

Uncoupled approximate DCiM optimization

Architecture-only approximation search

Circuit-only sizing without accuracy-aware architecture search

Same neural task, accuracy acceptance rule, PPA definitions, compressor/SRAM choices, PVT/mismatch samples, OpenROAD flow, constraints and final verification boundary are unspecified

**Reported measurements:**

The official description claims strong PPA–accuracy tradeoffs, robust convergence and rapid what-if exploration under controlled accuracy budgets, but reports no accuracy value/distribution, latency, energy, area, timing, yield, convergence curve, surrogate error, Monte Carlo count, circuit conditions or final application result.

**Limits on the conclusion:**

An accuracy constraint must identify the task, dataset/population, metric, baseline, calibration, acceptable degradation and statistical confidence. Validate the final approximate array and sized circuits with independent inference or numerical simulation, including activation/input distributions and rare cases; a surrogate's predicted error is not the application's measured quality.

Architecture approximation and transistor/PVT/mismatch variation interact. Propagate compressor error, SRAM read/write variation, voltage/frequency, temperature, process corners, parasitics and Monte Carlo outcomes through the same network, and report PPA distributions, timing failures, yield and Pareto fronts. A nominal PPA point or mean accuracy can hide tail failures.

Separate GNN surrogate training, architecture candidates, circuit sizing, Monte Carlo, layout/extraction, rejected designs and final validation in runtime. Compare exact, uncoupled and jointly optimized flows with equal task quality, PPA definitions, process, tools, constraints and search budget. FreePDK45/OpenROAD improves reproducibility but does not establish silicon behavior or transfer to another process. The evidence supports accuracy-constrained approximate-DCiM co-optimization, not demonstrated application-safe PPA improvement or process-independent yield.

**Source and location**

Evidence tier: Primary captured official DAC description plus direction atlas challenge context; no full paper extraction, reproduced openacmv2 flow, calibrated circuit/yield study or independent application quality evaluation. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH2014&sess=sess118)

DAC 2026 official description; existing processing-in-memory-and-memory-centric-compute chapter framing; direction-atlas evaluation-as-research challenge record; captured Problem, Mechanism / artifact, Workload, Hardware, Baseline, Measurements and Limits fields; no manuscript pages, accuracy/PPA table, Monte Carlo matrix or independent application/circuit validation.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** exact DCiM

uncoupled approximate DCiM

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH2014

**Hardware or process assumptions:** Digital compute-in-memory array; data movement, process, and error assumptions are unspecified.

**Limits:** No accuracy, latency, energy, area, yield, or technology results are reported.

Constraints may be workload-specific.

Official description only; circuit and application validation is required.

**Method or artifact:** Accuracy-constrained algorithm-circuit co-optimization framework for DCiM.

**Metrics:** Accuracy-constrained efficiency is claimed qualitatively

**Problem:** Approximate DCiM requires jointly selecting algorithms and circuits under explicit accuracy constraints.

**Workload or benchmark:** DNN or matrix workloads; accuracy targets, memory technology, and circuit baselines are unspecified.

</details>

<span id="paper-dac-2026-research401"></span>

### PAGE: Processing-Using-DRAM Architecture-Circuits Co-Optimization for Efficient Acceleration of General Matrix-Vector Multiplication

DAC 2026 · Record: `dac-2026-research401`

[Read the step-by-step explanation](#explanation-dac-2026-research401)

**Updated source-backed reading card**

Reviewed 2026-09-09. Deepens the PAGE treatment into a paper-level reading; separates mat-level PUD parallelism, inversion-enabled sense amplifiers, AP row copy and adaptive adder-tree accumulation from DRAM timing, numerical fidelity, refresh/reliability, fabricated-modification status and system-level GEMV accounting, while preserving the COTS, TSMC 16 nm and simulator evidence boundaries and the 14x/3.1x claims.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

LLM decoding is memory-bound and performs general matrix-vector multiplication, while conventional processing-using-DRAM has limited sense-amplifier compute capability and can spend many cycles on row activation, copying and accumulation.

**Mechanism / artifact:**

PAGE co-optimizes a processing-using-DRAM architecture and circuits with mat-level parallelism across sense amplifiers, inversion-enabled sense amplifiers for NOT operations, AP-based simultaneous source–destination row copy, and adaptive adder-tree accumulation to reduce GEMV cycles. The supported bit/precision representation, operand layout, control sequence, peripheral interface, refresh interaction and circuit margins are unspecified.

**Workload — the work tested:**

GEMV workloads motivated by memory-bound LLM decoding; matrix dimensions, sparsity/density, weight/activation precision, batching, sequence length, data layout, output accuracy and end-to-end LLM generation coverage are unspecified.

**Hardware and manufacturing assumptions:**

Baseline PUD operations verified on a commercial-off-the-shelf DRAM–FPGA platform; modified PAGE circuits evaluated at circuit level in TSMC 16 nm; system throughput and energy analyzed with an in-house simulator. DRAM generation, bank/mat geometry, timing parameters, voltage/frequency, process corners, sense-amplifier variation, refresh, controller, FPGA overhead, fabrication status of PAGE modifications and simulator calibration are unspecified.

**Baseline — the comparison method:**

State-of-the-art processing-using-DRAM GEMV designs

CPU/GPU GEMV

Digital PIM GEMV

Same matrix dimensions, precision, layout, DRAM capacity, controller, clock, data preparation, refresh, output extraction, simulator assumptions and end-to-end workload boundary are unspecified

**Reported measurements:**

The source reports up to 14× end-to-end throughput improvement and 3.1× energy improvement for GEMV over state-of-the-art PUD designs; the COTS DRAM–FPGA platform verifies baseline PUD functionality and timing, TSMC 16 nm evaluates modified circuits, and an in-house simulator supplies system-level analysis. Numerical error, absolute throughput/energy, area, refresh cost, timing margins, FPGA/control overhead and full-LLM generation results are not reported.

**Limits on the conclusion:**

PUD logic operations and PAGE's added row/sense-amplifier behavior must obey DRAM activation, restore, timing, charge-sharing and refresh constraints. A COTS demonstration of baseline PUD does not establish that modified PAGE circuits are fabricated or deployable in unmodified commercial DRAM; report circuit margins, PVT/variation, retention, refresh interference, row disturbance, controller legality and failure rates.

GEMV throughput is useful only if the numerical representation and output meet the workload's quality requirement. Define bit widths, signedness, accumulation, saturation/rounding, error distribution and comparison against exact GEMV; test matrix/activation distributions, dimensions, batches and LLM layers. Include layout/conversion, data placement, row setup, control, refresh, output extraction and unsupported operations in the timing and energy boundary.

The 14× throughput and 3.1× energy claims combine architecture/circuit ideas with simulator and baseline assumptions; they are not automatically measured silicon results or full LLM decoding gains. Reconcile state-of-the-art PUD baselines, absolute values, simulator calibration, FPGA/host costs, DRAM capacity and controller behavior. The evidence supports PUD GEMV co-design, not demonstrated fabricated PAGE deployment, numerical equivalence or transferable end-to-end LLM efficiency.

**Source and location**

Evidence tier: Primary captured official DAC description; cots baseline pud demonstration, tsmc 16 nm circuit evaluation and in house system simulation, without fabricated page evidence or independent reproduction. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/presentation/?id=RESEARCH401&sess=sess116)

Refreshed DAC 2026 official description; existing processing-in-memory-and-memory-centric-compute editorial explanation; captured Problem, Mechanism / artifact, Workload, Hardware, Baseline, Measurements and Limits fields; no full manuscript, circuit margin table, numerical-error trace or fabricated PAGE validation.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** CPU/GPU GEMV

digital PIM GEMV

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH401

**Hardware or process assumptions:** DRAM processing elements and sensing circuits; analog error and process assumptions are unspecified.

**Limits:** No numerical error, throughput, energy, area, or DRAM measurements are reported.

Analog and refresh behavior may dominate results.

Official description only; device-calibrated validation is required.

**Method or artifact:** Processing-using-DRAM architecture-circuit co-optimization for GEMV.

**Metrics:** PIM GEMV efficiency is claimed qualitatively

**Problem:** General GEMV is limited by memory movement and DRAM interface cost.

**Workload or benchmark:** General matrix-vector multiplication; matrices, DRAM technology, and baselines are unspecified.

</details>

<span id="paper-dac-2026-research752"></span>

### CQ-CiM: Hardware-Aware Embedding Shaping for Robust CiM-Based Retrieval

DAC 2026 · Record: `dac-2026-research752`

[Read the step-by-step explanation](#explanation-dac-2026-research752)

**Updated source-backed reading card**

Reviewed 2026-09-09. Deepens the CQ-CiM treatment into a paper-level reading; separates joint hardware-aware compression/quantization and target-array shaping from embedding fidelity, analog device noise, index construction, recall/precision, calibration and end-to-end RAG cost, while preserving the description's SRAM/ReRAM/FeFET and array-constraint examples without inventing quantitative gains.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

RAG on edge devices moves and compares high-dimensional, high-precision embeddings, while compute-in-memory arrays impose lower precision, lower dimension and technology-specific shape constraints; independently reshaping dimension and precision can distort the representation and obscure whether a retrieval failure comes from data shaping or hardware.

**Mechanism / artifact:**

CQ-CiM is a hardware-aware data-shaping framework that jointly performs compression and quantization to fit embeddings to varied CiM designs, including SRAM, ReRAM and FeFET implementations with constraints such as 2-bit cells and 512×512 arrays. The objective, compression/quantization operators, calibration procedure, mapping/layout, analog error model, retraining or distillation and query/database transformation path are unspecified.

**Workload — the work tested:**

Retrieval-augmented generation with edge-device embedding search; source models, embedding dimensions/precision, corpus size, query distribution, retrieval index, top-k/recall target, CiM technology and array shape are unspecified.

**Hardware and manufacturing assumptions:**

Compute-in-memory crossbar or array with low-precision cells and analog/non-ideal computation; SRAM, ReRAM and FeFET examples, cell precision and array dimensions are named, but ADC/DAC, accumulation, noise, variation, conductance range, IR drop, temperature, process, controller, memory capacity and interface assumptions are unspecified.

**Baseline — the comparison method:**

Unshaped high-precision embeddings mapped to the target CiM constraints

Naive dimension-only shaping

Naive precision-only quantization

Digital retrieval

Same embedding model, corpus, query set, index, top-k, quality target, array mapping, calibration, ADC/DAC, storage capacity and end-to-end shaping/index-build/query boundary are unspecified

**Reported measurements:**

The source claims a unified hardware-aware shaping direction for comprehensive CiM-based RAG usage, but reports no recall, precision, NDCG, MRR, answer groundedness, embedding distortion, energy, latency, area, throughput, index-build cost, device variation or robustness value.

**Limits on the conclusion:**

Compression and quantization can preserve a norm or reconstruction error while changing nearest-neighbor ordering. Evaluate embedding cosine/distance distortion, top-k recall/precision/NDCG and downstream RAG answer quality against unshaped and separately shaped baselines; hold the corpus, query distribution, index and quality target constant.

CiM constraints differ by SRAM, ReRAM and FeFET technology, cell precision, array dimensions, ADC/DAC and analog error. A shape that fits a nominal 2-bit or 512×512 array may fail under conductance variation, noise, saturation, IR drop, calibration drift or mapping imbalance. Validate per-device and per-array behavior and report rejected or remapped embeddings.

The description supplies no quantitative retrieval or system result. Count offline shaping, retraining/distillation, encoding, index construction, storage expansion, query mapping, ADC/DAC, host transfers and RAG generation in the end-to-end boundary. The evidence supports hardware-aware embedding shaping, not demonstrated robust CiM retrieval quality or end-to-end RAG improvement across device technologies.

**Source and location**

Evidence tier: Primary captured official DAC description; no full paper extraction, quantitative retrieval result, device calibrated validation or independent reproduction. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH752)

DAC 2026 official description; existing processing-in-memory-and-memory-centric-compute editorial explanation; captured Problem, Mechanism / artifact, Workload, Hardware, Baseline, Measurements and Limits fields; no manuscript, retrieval table, device trace or calibrated array evaluation.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** unshaped embeddings

digital retrieval

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH752

**Hardware or process assumptions:** Compute-in-memory array with analog variation; ADC, noise, and process assumptions are unspecified.

**Limits:** No recall, noise tolerance, energy, latency, area, or device results are reported.

Embedding shaping may trade off digital quality.

Official description only; device-calibrated validation is required.

**Method or artifact:** Hardware-aware embedding-shaping method for CiM retrieval.

**Metrics:** Robust CiM retrieval is claimed qualitatively

**Problem:** CiM retrieval is sensitive to analog or device non-idealities in stored embeddings.

**Workload or benchmark:** Embedding retrieval workloads; models, memory technology, and robustness metric are unspecified.

</details>

## What remains to establish

Resolve unspecified workloads, comparison methods, resource budgets, and source locations before generalizing a reported gain. Multiple papers in this selected sample permit comparison of mechanisms, but do not by themselves establish recurrence across years or a long-term trend.

[All subthemes](../expanded-taxonomy-v1.md) · [Research directions](../directions/README.md)
