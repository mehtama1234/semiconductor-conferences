## Faster inference requires more than faster multiplication

An accelerator's microarchitecture is its internal arrangement of arithmetic units, storage, connections, and control. A language model can keep these units busy only if the required data arrive in time and the next operation is ready to execute. Faster arithmetic cannot remove a wait for memory or a dependency on an unfinished operation.

Four papers here change different constraints. AMBER changes how bits are stored and processed. MBA changes how much data can remain close to computation. AHASD changes when two cooperating models execute. OASIS changes how low-precision numbers are represented and multiplied. These distinctions explain the mechanisms; the reported improvement factors do not form a common ranking.

Weights are learned model parameters. Activations are intermediate values produced while processing an input. The key/value cache stores attention information from earlier tokens so that generation need not recompute it each time. A token is one unit of the model's text representation, which can be a word fragment rather than a complete word.

## AMBER: preserve the numbers while changing their encoding

Lossless compression preserves every encoded value after decompression. Quantization instead replaces values with a smaller set of representable choices and can introduce numerical error. A lossless compressor applied to an already quantized model preserves that model's values; it does not reverse the earlier quantization error.

[AMBER](../observed-subthemes/ai-accelerator-microarchitecture.md#paper-dac-2026-research640) combines bit-transposed compression with a reconfigurable, pipelined bit-serial processing element. The official description covers integer, floating-point, and microscaling formats and reports evaluation on eight models and ten formats. It gives 1.17× memory-efficiency and 3.16× compute improvements, naming Olive and Tender, without exposing the exact definitions or per-baseline comparisons. Process, clock, area, format-specific costs, and model-quality conditions remain missing. [Official AMBER description](https://63dac.conference-program.com/presentation/?id=RESEARCH640&sess=sess156).

<span id="explanation-dac-2026-research640"></span>

### AMBER: lossless bit storage and bit-serial arithmetic address different costs

### What lossless bit compression preserves

An LLM value is represented by bits. Integer values use a signed or unsigned encoding; floating-point values separate sign, exponent and significand fields; microscaling formats add a shared scale or group-level representation. These formats place useful information in different bit positions. A compressor must preserve the exact encoded value if decompression is called lossless. It does not restore accuracy already lost when a higher-precision value was quantized into a smaller format.

Bit-transposed encoding changes how bits are grouped before compression. Instead of storing each complete number as one sequence, the representation can group corresponding bit positions or fields across values. If a group of values has statistical concentration in particular bit positions, a bit-level compressor can encode that concentration more efficiently. The operation is a representation change: after decoding, the original integer, floating-point or microscaling bits must be recovered exactly.

The potential benefit applies to weights and key/value (KV) cache data, but the two objects have different lifetimes. Weights are reused across many requests and can justify offline encoding. KV data is produced and consumed during serving, so encode/decode latency, memory bandwidth and access granularity affect the result more directly. A compressed byte count alone does not establish lower serving latency unless the accelerator can decode the needed values at the rate computation consumes them.

### What the bit-serial processing element changes

A bit-serial processing element performs arithmetic over successive bit portions rather than requiring a separate full-width datapath for every precision. A precision-agnostic design can reuse the same bit-level hardware for INT, floating-point and microscaling formats while changing the sequence of operations and control. A stage-pipelined structure overlaps different inputs or bit stages, which can raise steady-state throughput.

The trade-off is that bit-serial work takes multiple steps for one arithmetic result. Accumulation, field decoding, sign and exponent handling, scale management, control, and movement of compressed data still consume cycles and energy. A pipeline's output rate after it is full is not the same as the latency of one request. The useful comparison must therefore include format-dependent bit counts, pipeline fill and drain, decode overhead, memory traffic and accumulation behavior.

### What the reported evaluation establishes

The official description reports evaluation on eight LLMs and ten formats, with 1.17× memory-efficiency improvement and 3.16× compute improvement, and says AMBER surpasses Olive and Tender in throughput and energy. The description does not define memory efficiency or compute improvement, identify each baseline configuration, report compression ratio by format, or state model-quality constraints. It also supplies no area, clock, bandwidth, power or format-specific latency.

The evidence supports a unified multi-precision representation and compute direction. It does not show that every format gets the same gain, that lossless storage preserves end-to-end model quality under the surrounding quantization choices, or that compute improvement becomes the same inference-throughput improvement. Cloud and edge suitability additionally require different memory, thermal and area constraints.

### The evaluation that would establish end-to-end value

Report encoded and decoded size for weights and KV data by format, decode bandwidth, arithmetic latency, pipeline utilization, area, power, clock, memory traffic and control overhead. Compare each model and format with matched Olive and Tender configurations. Measure accuracy or task quality before and after any quantization, and separate lossless AMBER effects from quantization effects. Report prefill and decode latency, batch size, sequence length, cache residency and total energy per generated token on a stated hardware implementation or a fully specified simulator.

The [AMBER](../observed-subthemes/ai-accelerator-microarchitecture.md#paper-dac-2026-research640) record describes bit-transposed lossless weight/KV compression and precision-agnostic pipelined bit-serial processing for INT, FP and MX formats. The detailed explanation above separates exact bit preservation from quantization, storage compression from decode cost, bit-serial throughput from request latency, and reported compute/memory factors from end-to-end serving evidence; this card is the compact evidence record.

The [AMBER](../observed-subthemes/ai-accelerator-microarchitecture.md#paper-dac-2026-research640) record therefore concerns both representation and execution: bit-serial computation can share circuitry across widths, but decoding, transfers, accumulation and pipeline latency remain part of the full cost. The detailed explanation above is the paper-level account; this sentence keeps the chapter's cross-paper summary compact.

## MBA: retain data close to the arithmetic

Storage capacity and transfer bandwidth answer different questions. Capacity determines how much can stay resident; bandwidth determines how quickly data can move. Increasing capacity helps when it prevents repeated transfers of useful data. It helps less when the working data still exceed capacity or when another part of execution dominates.

[MBA](../observed-subthemes/ai-accelerator-microarchitecture.md#paper-dac-2026-research509) proposes gigabyte-scale embedded dynamic memory with priority for the key/value cache, double buffering, and iteration-aware eviction. Double buffering separates data being consumed from data being prepared for later use. Eviction chooses what to remove when space is needed.

The official description reports 5.99× speedup and 8.86× energy efficiency against a GPU baseline, versus 3.63× and 4.93× against an accelerator baseline. It does not identify the compared configurations or establish a fabricated gigabyte-buffer chip. Technology retention, refresh costs, area, sequence lengths, and complete energy accounting require the manuscript. [Official MBA description](https://63dac.conference-program.com/presentation/?id=RESEARCH509&sess=sess157).

<span id="explanation-dac-2026-research509"></span>

### MBA: a large local buffer helps only when mapping, overlap and eviction preserve useful data

### Why capacity and bandwidth are different limits

LLM inference repeatedly reads model weights and, during autoregressive decoding, the key/value cache built from earlier tokens. High-bandwidth memory (HBM) can supply data quickly, but transferring data between HBM and the compute die still consumes time and energy. A larger local buffer can reduce those transfers if the working set fits or if the most repeatedly used data remain resident.

Capacity answers how much data can stay close to computation. Bandwidth answers how quickly data can cross a connection. A gigabyte-scale buffer improves neither automatically: if the active weights and KV state exceed its capacity, the system still transfers data; if arithmetic or another network link dominates, reducing HBM traffic may not change end-to-end latency.

### What MBA changes in the memory and execution path

MBA uses embedded DRAM (eDRAM) as a large on-chip buffer. Its KV-cache-prioritized mapping (KVP) gives the cache priority when deciding which information should occupy the local buffer. The mapping policy is important because KV entries have different reuse and lifetime depending on sequence length, layer, token position and batching. Prioritizing KV data can reduce repeated HBM reads, but it can also displace weights or other state that the next operation needs.

The architecture co-designs three mechanisms. Double buffering keeps one region available to the compute pipeline while another region is being filled or prepared. This can overlap data movement with arithmetic, but only when transfer time, compute time, buffer capacity and synchronization are balanced. If the next data are not ready, the compute units still wait; if production outruns consumption, a buffer fills and backpressure is required.

Iteration-aware eviction chooses what to remove based on expected future use across iterations. An eviction policy is a prediction about reuse. Removing data that will be needed soon creates another HBM transfer; retaining data with little future use consumes capacity that could protect a high-reuse KV or weight block. The policy therefore affects traffic, cache residency, overlap and energy together rather than being an independent memory feature.

### What the reported comparisons establish

The official description reports 5.99× and 3.63× end-to-end speedup and 8.86× and 4.93× energy-efficiency improvement against GPU and LLM-accelerator baselines, respectively. The two baseline pairs must remain separate. Speedup is a latency or throughput ratio; energy efficiency is useful work per energy under a defined task. Neither number establishes the other, and neither identifies how much came from eDRAM capacity, KVP mapping, double buffering or eviction.

The description does not identify the LLMs, sequence lengths, batch sizes, memory capacity, HBM traffic, eDRAM refresh or retention behavior, area, power boundary, accuracy effects or exact baseline configurations. It describes 1T1C IGZO eDRAM integration, but an architectural description is not proof of a fabricated gigabyte-scale buffer. Density, retention, endurance, access time, refresh energy, process integration and area must all be evaluated together.

### The evaluation that would establish end-to-end benefit

Report model, sequence and batch conditions; weight and KV-cache sizes; local-buffer capacity; HBM traffic before and after KVP; hit/residency rates; transfer overlap; eviction events; refresh and retention assumptions; area; power; and control overhead. Compare no-buffer, ordinary-buffer and MBA policies under equal compute and memory constraints. Report prefill and decode latency, throughput, energy per token, tail behavior and model quality separately, and distinguish modeled eDRAM from synthesized or measured hardware.

The [MBA](../observed-subthemes/ai-accelerator-microarchitecture.md#paper-dac-2026-research509) record describes gigabyte-scale eDRAM buffering with KV-prioritized mapping, double buffering and iteration-aware eviction. The detailed explanation above separates capacity from bandwidth, residency from transfer, overlap from guaranteed utilization, eviction prediction from free reuse, and reported baseline ratios from the missing memory and implementation conditions; this card is the compact evidence record.

The title's 1T1C means one transistor and one capacitor per memory cell. Its IGZO label identifies the indium-gallium-zinc-oxide material system. A cell technology's potential density is not sufficient evidence that a complete buffer meets an accelerator's capacity, access-time, power, and manufacturing requirements simultaneously.

## AHASD: overlap useful work without accumulating rejected work

Speculative decoding uses a smaller model to propose tokens and a target model to check them. Only accepted progress should count toward useful output. Doing more drafting can waste work when proposals are rejected. Doing less can leave the verifier waiting. The acceptance rule also matters to whether the generated-output distribution is preserved.

[AHASD](../observed-subthemes/ai-accelerator-microarchitecture.md#paper-dac-2026-research384) separates drafting on processing-in-memory hardware from verification on a neural processing unit. Its official description uses confidence-history and available-time controls to manage drafting and pre-verification, plus attention and task-scheduling hardware within LPDDR5-PIM.

It reports up to 4.2× throughput and 5.6× energy efficiency against GPU-only execution, and 1.5× and 1.24× against a GPU-plus-PIM baseline. Reported added hardware occupies under 3% of DRAM area, not necessarily under 3% of total system area or power. Model pairs, acceptance distributions, absolute latency, correctness conditions, and implementation methodology remain unspecified in this source. [Official AHASD description](https://63dac.conference-program.com/presentation/?id=RESEARCH384&sess=sess157).

<span id="explanation-dac-2026-research384"></span>

### AHASD: speculative decoding needs a policy for deciding which draft work is worth doing

### What speculative decoding computes

Speculative decoding uses a small draft language model (DLM) to propose several next tokens, then asks a larger target language model (TLM) to verify them in a batch. Accepted draft tokens can reduce the number of expensive TLM steps. Rejected tokens are not useful output, although their generation and verification still consumed compute and energy. The useful quantity is accepted progress per unit time and energy, not the raw number of draft tokens produced.

Adaptive drafting changes the number of proposed tokens as confidence or workload conditions change. A synchronous implementation can leave the NPU idle while the PIM side drafts, or leave the PIM side idle while verification completes. A fully asynchronous implementation can instead produce drafts faster than verification can consume them, causing invalid or unnecessary drafts to accumulate. The control problem is to overlap useful DLM and TLM work without turning uncertainty into wasted work.

### What AHASD changes

AHASD decouples DLM drafting on processing-in-memory hardware from TLM verification on a single NPU at task level. This lets drafting and verification proceed in parallel rather than forcing every operator to wait for the other side. The task boundary matters: the system can schedule a complete drafting or verification unit, but it must still synchronize the token state and acceptance result between them.

Entropy-history-aware drafting control uses recent model uncertainty as a signal for how aggressively to draft. Lower confidence can make longer drafts less useful because more tokens may be rejected. Time-aware pre-verification control considers available time before starting verification, with the stated goal of suppressing invalid drafting. These controls are policies, not guarantees: their value depends on the entropy distribution, acceptance rule, model pair, request length and thermal state.

The architecture adds attention algorithm units and gated task scheduling units inside LPDDR5-PIM. Localized attention keeps relevant attention computation near the PIM data, while gated scheduling controls when task execution is allowed to proceed. The reported sub-microsecond task switching concerns switching overhead; it does not establish total draft/verify latency, accepted-token rate or end-to-end serving performance by itself.

### What the reported numbers establish

The official description reports up to 4.2× throughput and 5.6× energy-efficiency improvement over GPU-only execution, and 1.5× throughput and 1.24× energy-efficiency improvement over the GPU+PIM baseline. The “up to” values are best cases. Throughput must be tied to accepted output tokens and request conditions; energy efficiency must state whether energy includes both DLM and TLM, rejected work, memory traffic, control and idle periods.

The source reports hardware overhead below 3% of DRAM area. That denominator is not total system area, total power, thermal density, or mobile-device cost. It also does not establish LPDDR5-PIM fabrication or the area/energy of the NPU-side additions. The description omits model sizes, acceptance rates, adaptive-draft distributions, absolute latency, correctness conditions, thermal methodology and cross-device generalization.

### The evaluation that would establish useful speculative execution

Report DLM/TLM pairs, draft-length distributions, token acceptance rate, rejected-token work, output-quality equivalence, request lengths, batch and arrival conditions, and control decisions over time. Measure end-to-end time to first token, time per accepted token, tail latency, throughput, energy, memory traffic, PIM/NPU utilization, synchronization, task-switching and queueing overhead. Compare synchronous, asynchronous and AHASD policies under the same models, quality rule and hardware budget. Give area and power for the complete system, not only DRAM-area overhead, and test temperature or mobile power limits.

The [AHASD](../observed-subthemes/ai-accelerator-microarchitecture.md#paper-dac-2026-research384) record describes task-level asynchronous DLM drafting on PIM and TLM verification on an NPU with entropy-history and time-aware controls. The detailed explanation above separates proposed tokens from accepted work, overlap from useful progress, policy signals from guarantees, switching overhead from end-to-end latency, and DRAM-area overhead from complete-system cost; this card is the compact evidence record.

The [AHASD](../observed-subthemes/ai-accelerator-microarchitecture.md#paper-dac-2026-research384) record should therefore be read through accepted tokens, rejected work, synchronization time and both models' energy over the same output task; peak drafting rate alone cannot establish shorter user-visible latency.

## OASIS: compute using a small set of representative values

Non-uniform quantization assigns short codes to representative values that need not be equally spaced. Multiplying the codes as integers would generally give the wrong result: code numbers identify values rather than express their magnitudes. One alternative is to precompute the possible products and retrieve the appropriate product using the two codes.

For example, two sets of sixteen representative values have 256 possible pairs. This bounds the number of distinct pair products, but not the work of reading input codes, combining repeated contributions, or handling values outside the compact representation. A small lookup table is not itself an end-to-end speedup.

[OASIS](../observed-subthemes/ai-accelerator-microarchitecture.md#paper-isca-2026-program-020) combines product tables with outlier detection and concurrent error compensation. Use version 4; version 1 was KLLM with different comparisons. Section V-A, PDF page 9, models hardware through cycle simulation, 28-nm logic synthesis, and memory models—not measured accelerator silicon. Figure 11, page 10, reports 3.00× speed and 1.44× energy efficiency against FIGLUT for four-bit weights/activations in single-batch decoding; FIGLUT uses sixteen-bit activations.

Accuracy needs reconciliation: the arXiv abstract says 1.98%, the downloaded version-4 PDF abstract says 1.94%, and Section V-B says 2.05%. Table IV, page 11, gives LLaMA-2-7B averages of 70.49 for FP16 and 68.55 for four-bit OASIS: a 1.94-percentage-point difference for that model, not a universal relative loss. [Version-4 PDF, pages 1 and 9–11](https://arxiv.org/pdf/2507.23035v4), [arXiv record](https://arxiv.org/abs/2507.23035v4).

<span id="explanation-isca-2026-program-020"></span>

### OASIS: lookup multiplication must preserve quantization meaning and control outlier error

### Why non-uniform quantization does not fit ordinary integer MACs

Quantization replaces a continuous numerical value with a code that refers to a representative value. Uniform quantization spaces representatives at regular intervals. Non-uniform quantization places them where the model's weights or activations are concentrated, which can represent a skewed or heavy-tailed distribution more efficiently. The code is an index, not necessarily the numerical magnitude.

This creates a hardware problem. If a weight code and activation code are multiplied as ordinary integers, the result is generally not the product of their represented values. Dequantizing before multiplication restores the numerical meaning but adds conversion, storage and data-movement work. OASIS instead precomputes products for pairs of representative values and uses the two codes to select the corresponding product from a lookup table (LUT).

### What the Cartesian-product LUT changes

If there are (N_w) weight representatives and (N_a) activation representatives, a direct product table has (N_wN_a) possible pairs. The table can replace a general multiplier with code decoding and a lookup. OASIS uses Cartesian-product LUT organization to reduce LUT size relative to earlier LUT-based GEMM methods and reports 64× lower LUT size and 1024× higher computational parallelism than those methods.

The table count does not equal total GEMM cost. The accelerator must read codes, select products, accumulate products across the reduction dimension, move partial sums and handle values that are not represented well by the common codebook. Lookup parallelism can also increase table bandwidth, read ports, routing and accumulation demand. The reported ratio is therefore a microarchitecture comparison whose usefulness depends on the complete memory and accumulation path.

### How outlier handling changes the numerical path

Aggressive activation quantization can represent common values compactly while poorly representing rare large values. Those outliers can contribute disproportionately to a dot product. OASIS identifies activation outliers with the Orizuru top-k detection engine, computes the regular values through LUT-based GEMM, and applies concurrent error compensation for the outlier contribution.

The top-k engine must decide which values are exceptional under a threshold or ranking rule, then route their correction without stalling the common path. The correction is useful only if the outlier representation, location, sign, scale and accumulation order are preserved. Detecting an outlier is not itself a proof that the compensated product matches FP16; the remaining quantization error and the hardware cost of detection and correction must be measured.

### What the reported results establish

The recovered version-4 evaluation models hardware with cycle simulation, 28-nm logic synthesis and memory models. Figure 11 reports 3.00× speed and 1.44× energy efficiency against FIGLUT for four-bit weights and activations in single-batch decoding; FIGLUT uses sixteen-bit activations. This is not a measurement of fabricated accelerator silicon, and the precision mismatch is part of the comparison condition.

The accuracy claim also has source-version and metric differences: the arXiv abstract reports 1.98%, the version-4 PDF abstract reports 1.94%, and Section V-B reports 2.05%. Table IV's LLaMA-2-7B values of 70.49 for FP16 and 68.55 for four-bit OASIS imply a 1.94-percentage-point difference for that model, not a universal relative loss. These values should not be collapsed into one unqualified accuracy number.

### The evaluation that would establish end-to-end value

Report representative-value tables, code distributions, outlier rate and threshold, LUT size and bandwidth, detection/compensation cost, accumulation precision, area, frequency, memory traffic and power. Compare OASIS and FIGLUT under matched weight/activation precision, batch, sequence length, model suite and output-quality metric, and separate lookup, outlier, accumulation and memory time. Give per-model accuracy and tail error, not only an average, and distinguish cycle simulation, synthesis estimates and measured silicon.

The [OASIS](../observed-subthemes/ai-accelerator-microarchitecture.md#paper-isca-2026-program-020) record describes Cartesian-product LUT GEMM for dual-side non-uniform quantization with outlier-aware compensation and Orizuru detection. The detailed explanation above separates code indices from values, LUT size from total GEMM cost, common quantization error from outlier correction, source-version accuracy discrepancies and modeled hardware from silicon evidence; this card is the compact evidence record.

## What the group suggests—and does not establish

The shared technical direction is to reduce wasted representation, transfer, or execution work while accounting for the cost introduced by doing so. This is a synthesis of mechanisms, not evidence of a measured long-term adoption trend across conferences.

Combining these methods would require compatibility checks. A compressed representation needs a compatible arithmetic path. A larger buffer changes the value of compression. Speculative execution changes the pattern of data reuse and useful output. Their individual gains cannot simply be multiplied.

An end-to-end comparison should hold output-quality requirements, model, input/output lengths, and batch size explicit, then report completed useful work, latency, energy, memory traffic, and area under a stated implementation method. The three DAC manuscripts remain missing. OASIS's recovered conditions supersede omissions in its historical card below, but source discrepancies and independent reproduction remain open.
