# Emerging memory and devices

This subject has 2 records in the selected sample. This page explains where it fits, then presents all captured paper evidence without shortening the measurements or limitations.

[Definitions used in the paper records](../reading-guide-v1.md)

## Understand the parent subject first

- [Analog mixed signal and emerging devices](../themes/analog-mixed-signal-and-emerging-devices.md)

## Two ways to compute where values are stored

This grouping contains an analog sequence-matching architecture and a digital neural-network accelerator. They both place computation near stored values, but they do not demonstrate the same device technology or execute the same task. In particular, digital compute-in-memory does not by itself imply a new memory material.

Ordinary addressed memory returns the contents of a selected location. Content-addressable memory, or CAM, instead compares a supplied value with stored entries and reports matches. Comparing many entries in parallel can reduce a search's sequence of accesses. The surrounding system still has to encode the query, load the stored entries, interpret match results, and handle cases the array cannot resolve.

Compute-in-memory, or CIM, is a broader term for performing operations within or closely integrated with memory structures. Digital implementations manipulate discrete bit values using logic. Analog implementations use electrical quantities whose magnitude carries information. These choices lead to different precision limits, circuit costs, and validation requirements.

<span id="explanation-dac-2026-research2708"></span>

## M²CAM: represent sequence symbols with conductance levels

A conductance describes how readily current flows through a device. A multi-level storage device uses distinguishable conductance ranges to represent more than two states. Greater information per device can reduce the number of storage elements needed for an encoding, but only if the states remain distinguishable under programming variation, noise, and drift.

[M²CAM](../observed-subthemes/emerging-memory-and-devices.md#paper-dac-2026-research2708) proposes multi-level memristor CAM encoding for nucleotides and hierarchical matching-precision adaptation under device variation. Its official description uses single-cell RNA-sequencing data as a genome-classification application. It reports 50–75% fewer devices, energy improvements of 131.2–3088.9×, and latency improvements of 161.2–269.6× against CPU/GPU implementations and tools including STAR. The ranges lack a case-by-case mapping to datasets and comparators. They must not be paired arbitrarily or treated as measured full-system gains. [Official M²CAM description](https://63dac.conference-program.com/presentation/?id=RESEARCH2708&sess=sess139).

The phrase error correction also needs a precise interpretation. Adjusting a matching threshold or selecting a more precise mode is not automatically equivalent to correcting arbitrary stored-bit errors with a coding guarantee. The description does not expose a guaranteed error pattern, correction radius, or recovery procedure.

For sequence analysis, success requires more than a fast comparison. Establish which parts of the software workflow the array replaces, which remain on a host, and whether the outputs have equivalent meaning. Report incorrect matches and missed matches under the same input conditions. Using a biological dataset does not alone establish biological accuracy, clinical usefulness, or equivalence to the complete reference tool.

### What the CAM is actually matching

In a CAM, a query pattern is applied to many stored entries and each row produces a match or mismatch signal. For nucleotide processing, the representation must define how A, C, G, T, ambiguity symbols, gaps, quality scores, and sequence positions map onto conductance states and sensing conditions. A compact multi-level encoding can reduce cells per symbol, but the number of physical devices is not the same as the number of complete matching lanes. Row drivers, word lines, sense amplifiers, reference cells, selectors, buffers, ADCs or comparators, and interconnect can dominate area and energy.

The self-adaptive mechanism is a control policy around an analog decision. If device variation makes two conductance levels overlap, the system can use a wider margin, a more precise sensing mode, repeated evaluation, or a hierarchical fallback. That may improve match reliability at the cost of latency, energy, array utilization, or throughput. “Error correction” should therefore be tied to an explicit error model: state drift, write variation, read noise, stuck devices, temperature, line resistance, or an incorrect sequence symbol. A mode switch or threshold adjustment is not automatically an error-correcting code or a guarantee of recovered sequence correctness.

### Genome classification has an application-level oracle

Single-cell RNA sequencing is a pipeline rather than one CAM operation. Reads may be base-called, filtered, aligned or pseudo-aligned, counted, normalized, and assigned to genes or cell types. M²CAM's evaluation must state which stage is accelerated and whether the array receives preprocessed sequences or replaces part of alignment and classification. A matching result that is equivalent at the row level can still change downstream counts if approximate matching admits false positives or rejects low-quality reads.

Report exact-match and approximate-match recall and precision, alignment or classification agreement with the reference tool, reads processed per second, rejected or retried reads, and the cost of moving reads and results between the array and host. Use the same reference genome, read lengths, sequencing error model, quality filtering, cell count, dataset split, and output definition. Real scRNA-seq data establishes workload relevance; it does not by itself establish biological accuracy or clinical utility.

### The improvement ratios need matched accounting

The reported 50–75% device reduction is a structural claim whose denominator must say whether it includes only memristor cells or the complete array and peripheral circuitry. The 131.2–3088.9× energy and 161.2–269.6× latency ranges must be mapped to individual datasets, stages, baselines, and measurement boundaries. CPU, GPU, and STAR are different comparators: a CPU/GPU implementation may measure an accelerated kernel, while STAR is a complete software workflow with different algorithms and I/O behavior. The ranges cannot be paired to create a single best-case speedup.

The required baselines include a digital CAM or digital IMC genome accelerator, a conventional CPU/GPU implementation, and the same bioinformatics tool configuration with identical output requirements. Report array energy and latency separately from ADC/DAC, sensing, programming, calibration, error recovery, host orchestration, memory transfers, preprocessing, postprocessing, and idle power. Also sweep device variation, temperature, endurance state, conductance distributions, array size, sequence length, and adaptive-mode activation. Without those conditions, the description supports a compact analog-CAM direction, not demonstrated end-to-end genome-processing efficiency.

<span id="explanation-iccad-2025-1"></span>

## Adder-DCIM: compressed models still need a faithful digital-CIM execution path

[Adder-DCIM](../observed-subthemes/emerging-memory-and-devices.md#paper-iccad-2025-1) addresses AdderNet inference, where replacing multiplication with adder-style operations does not by itself solve storage, bit-width, movement or parallel-utilization costs. The institutional report describes a joint design: model compression produces lower or mixed average widths, synchronous parallel digital compute-in-memory executes the resulting operations, and bit-flexible minimum-selector circuitry adapts the hardware to those widths. This is a co-design claim. It does not mean that a compressed model, an array implementation and a complete inference pipeline have automatically been shown equivalent.

Compression and execution are separate validation layers. First, the compressed ResNet20 or ResNet50 must preserve the intended task behavior against a named full-precision or uncompressed reference on a specified dataset and split. “Average width” is a distribution over layers, weights, activations or operands; it must be accompanied by the per-layer policy, encoding, scale handling and accuracy definition. Second, the mapped digital-CIM datapath must implement the same AdderNet operation: verify sign and bit ordering, minimum selection, accumulation, carry propagation, overflow or saturation, zero padding, partial sums and output reconstruction. A model-level accuracy number cannot expose a hardware mapping error that changes intermediate values.

The synchronous parallel organization also needs an explicit data path. State how operands and weights are laid out, how bit-flexible words are selected, how many rows or columns participate per cycle, where partial sums live, and how arrays are tiled for layers that exceed capacity. Report utilization, idle lanes, padding, reconfiguration or selection overhead, memory traffic, inter-array movement and host orchestration. A short average representation can reduce storage while failing to reduce latency if the array, accumulator or peripheral remains sized for the widest case.

The source reports a 28-nm design with 134 TOPS/W INT8 peak energy efficiency and 6.49 TOPS/mm² throughput density. It separately reports 255 TOPS/W for ResNet20 at 4.2 average bits and 243 TOPS/W for ResNet50 at 4.4 average bits, plus an accuracy loss below 0.4%. These are distinct source claims: the model-specific reduced-width results must not be merged with the INT8 peak, and the accuracy statement is not interpretable without the dataset, reference accuracy and percentage-point convention. The report does not resolve voltage, frequency, operation-count convention, power boundary or measured-versus-modeled status. [PKU report, item 10 under AI scheduling, mapping, and accelerator design](https://www.cpc.pku.edu.cn/info/1015/2796.htm).

TOPS/W is a ratio, not a complete inference result. Define whether an operation is an AdderNet distance, a bit-level primitive, a full layer operation or another unit. Identify whether power includes the memory array, sensing and write/read circuitry, minimum selectors, accumulators, clocking, interconnect, control, data movement, model loading and host work. Report area, latency, throughput, energy per complete inference, accuracy, utilization and layer-level distributions under the same process, voltage, frequency, model, batch size and quality target. Compare against a named conventional digital accelerator, an uncompressed or fixed-width AdderNet implementation and a compression-only flow, with identical mapping and accounting boundaries.

The captured evidence supports bit-flexible digital-CIM/model-compression co-design. It does not establish accuracy-preserving end-to-end CIM acceleration: the institutional report is not a manuscript or independent validation, and the baseline, dataset, mapped computation, operation count, power boundary, silicon status and complete inference accounting remain unresolved.

## Compare useful work, not unlike headline numbers

M²CAM's match decisions and Adder-DCIM's numerical operations are different units. A device-count reduction, an application latency ratio, and operations per watt cannot form a common ranking. Even within one architecture, the smallest array can require extra sensing or calibration circuitry that changes total area and energy.

A controlled evaluation should first fix the output requirement. It should then separate device behavior, circuit simulation or measurement, array execution, and full application execution. Include programming, calibration, error handling, and host processing where they are required. For an adaptive design, also report how often expensive modes activate and how they affect the slowest cases. These are evaluation requirements derived from the architectural differences, not measurements claimed for either paper.

The conceptual connection is that representation and circuit organization should be designed together. That is a cross-paper interpretation, not proof that analog computation is replacing digital computation. The sample combines a DAC 2026 proposal with an ICCAD 2025 fallback record, so it cannot establish year-over-year growth.

The exact-title source check on 2026-09-07 did not recover either full manuscript. M²CAM remains official-description evidence; Adder-DCIM remains institutional-report evidence with unresolved measured-versus-modeled status. Page-backed device conditions and complete application comparisons are still required. Related CIM publications must not supply missing facts for these specific papers.

## Compare the results carefully

First identify the inputs and required output quality. Then identify the limited resource: time, memory, communication, energy, circuit area, or correctness coverage. Ask which part of the method reduces that cost and which new cost it adds. Compare numbers only when the experiments hold these conditions sufficiently similar.

A conference description may explain the proposal while omitting the full experiment. An author preprint link may have been coded from its abstract. The source classification does not by itself establish that every table was read. Missing locations remain visible below.

## Complete captured evidence

These are evidence records, not substitutes for the explanations above. Each record preserves its problem, proposed method, measurements, comparison conditions, and source limits. A populated record does not establish that its mechanism has been fully explained or independently verified.

<span id="paper-dac-2026-research2708"></span>

### M²CAM: A Multi-Level Memristor-Based Self-Adaptive CAM Architecture for Genome Processing Acceleration

DAC 2026 · Record: `dac-2026-research2708`

[Read the step-by-step explanation](#explanation-dac-2026-research2708)

**Updated source-backed reading card**

Reviewed 2026-09-08. Deepens the existing M²CAM treatment into a paper-level reading; separates multi-level analog CAM representation from peripheral and application costs, defines adaptive matching and genome-level correctness, preserves the device, energy and latency ranges, and makes variation, calibration and comparator boundaries explicit.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Genome sequence matching and classification move large amounts of data, while digital encoding in in-memory genome accelerators can impose device and parallelism overhead.

**Mechanism / artifact:**

Multi-level memristor analog CAM encoding for nucleotide matching, hierarchical self-adaptive matching precision/error handling under device variation, and a parallel genome-classification framework; conductance mapping, sensing, control, correction model and host partition are unspecified.

**Workload — the work tested:**

Real single-cell RNA-sequencing datasets used for genome sequence matching/classification; reference genome, read lengths, quality filtering, cell count, dataset sizes/splits, output definition, sequence-error model and accuracy metrics are unspecified.

**Hardware and manufacturing assumptions:**

Multi-level memristor conductance states and analog CAM arrays with sensing and peripheral circuitry; device technology, conductance distributions, variation/noise/drift, temperature, ADC/DAC or comparator precision, programming, calibration, endurance, array size, process and measurement boundary are unspecified.

**Baseline — the comparison method:**

CPU implementation

GPU implementation

STAR or comparable traditional bioinformatics workflow

Digital-encoding in-memory genome accelerator

Same reference genome, reads, filtering, output requirement, preprocessing/postprocessing, host transfers, device variation, calibration, and complete energy/latency accounting are unspecified

**Reported measurements:**

The official description reports 50–75% lower device usage, 131.2–3088.9× energy improvement, and 161.2–269.6× latency improvement; it does not map ranges to cases or disclose matching accuracy, recall/precision, absolute energy/latency, peripheral cost, adaptive-mode frequency, throughput or biological output agreement.

**Limits on the conclusion:**

A conductance-level representation must define nucleotide/ambiguity encoding, sensing margins and the physical denominator for device count. ADC/DAC, sense amplifiers, references, drivers, buffers, interconnect, calibration and host transfers can change array-level and system-level cost.

Self-adaptive precision is not automatically error correction. Define whether variation means write error, read noise, drift, temperature, line resistance or stuck devices, and report false matches, missed matches, retries, mode activation and downstream sequence/classification agreement.

CPU/GPU kernels and STAR are not interchangeable baselines, and wide energy/latency ranges cannot be paired arbitrarily. The official description omits matched conditions and full-paper device/application validation. The evidence supports an analog-CAM genome-processing direction, not demonstrated end-to-end biological accuracy or system efficiency.

**Source and location**

Evidence tier: Primary captured official DAC description plus existing chapter level m²cam discussion; no full paper extraction, device variation matrix, biological accuracy validation or independent review. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH2708&sess=sess139)

DAC 2026 official description; existing chapter-level M²CAM discussion; captured Problem, Mechanism / artifact, Workload, Hardware, Baseline, Measurements and Limits fields; no manuscript pages or measured-device/application trace.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** CPU/GPU implementations

traditional bioinformatics tool STAR

digital-encoding IMC genome accelerators

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH2708&sess=sess139

**Hardware or process assumptions:** Multi-level memristor conductance states and analog CAM arrays; device technology, ADC/DAC, precision, endurance, and peripheral overhead are unspecified.

**Limits:** The wide improvement ranges lack matched hardware, tool, dataset, and accuracy conditions.

Analog peripheral, calibration, endurance, and variation costs may materially change system-level results.

Official description only; biological accuracy and measured-device claims require paper-level verification.

**Method or artifact:** Multi-level memristor analog CAM, hierarchical precision adaptation for variation tolerance, and parallel genome-classification framework.

**Metrics:** 50–75% reduction in device usage

131.2–3088.9x energy improvement

161.2–269.6x latency improvement

**Problem:** Genome sequence matching and classification are limited by data movement and bandwidth, while digital encodings impose area and parallelism overhead in in-memory genome accelerators.

**Workload or benchmark:** Single-cell RNA sequencing datasets and genome sequence matching/classification; dataset sizes, sequence lengths, accuracy/recall, and device-variation distributions are unspecified.

</details>

<span id="paper-iccad-2025-1"></span>

### Adder-DCIM: A Parallel Bit-Flexible Digital CIM Joint Model Compression Framework for AdderNet Inference

ICCAD 2025 · Record: `iccad-2025-1`

[Read the step-by-step explanation](#explanation-iccad-2025-1)

**Updated source-backed reading card**

Reviewed 2026-09-09. Deepens the Adder-DCIM institutional-report treatment into a paper-level reading; separates model compression and bit-flexible representation from digital-CIM execution and full-inference efficiency, preserves the reported 28-nm and TOPS claims with their conditions, and makes accuracy, operation-count, power-boundary and baseline gaps explicit.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

AdderNet inference still faces multiplication cost, fine-grained sparsity and mixed-precision utilization constraints in digital compute-in-memory deployments.

**Mechanism / artifact:**

Joint model compression and parallel bit-flexible digital CIM framework using synchronous parallel DCIM and minimum-selector circuitry for AdderNet; the compression policy, bit encoding, array mapping, accumulator behavior and validity checks are unspecified.

**Workload — the work tested:**

AdderNet inference with ResNet20 and ResNet50 cases and reported average widths of 4.2 and 4.4 bits; dataset, model checkpoints, reference accuracy, layer mix, batch size and evaluation split are unspecified.

**Hardware and manufacturing assumptions:**

28-nm digital-CIM design with reported INT8 peak efficiency and throughput density; memory organization, array dimensions, voltage, frequency, clocking, interconnect, peripheral circuits, operation-count convention, power boundary and measured-versus-modeled status are unresolved.

**Baseline — the comparison method:**

Not named in the institutional report

A valid comparison would hold model, dataset, accuracy target, bit policy, process, array capacity, compiler/mapping, voltage/frequency, operation definition and complete inference boundary constant; the required baseline implementation and conditions are unspecified

**Reported measurements:**

The institutional report states 134 TOPS/W INT8 peak energy efficiency and 6.49 TOPS/mm² throughput density, plus 255 TOPS/W for ResNet20 at 4.2 average bits and 243 TOPS/W for ResNet50 at 4.4 average bits; it also states loss below 0.4%, but does not define the accuracy reference, dataset or percentage-point convention.

**Limits on the conclusion:**

Compression accuracy and hardware fidelity are separate checks. Reproduce the compressed AdderNet outputs against a full-precision or named reference model, then check the mapped digital-CIM datapath for sign, carry, accumulation, overflow, saturation, bit ordering and minimum-selection behavior across layers and corner cases. A low reported accuracy loss does not prove that the physical array executes the same computation.

TOPS/W and TOPS/mm² depend on the operation definition and boundary. State whether the result is array-only, includes memory, control, interconnect and peripherals, and includes model loading, mapping, transfers and host work; report utilization, latency, throughput, area, energy per complete inference and variation across layers rather than only a peak ratio.

The institutional report supports a bit-flexible digital-CIM and model-compression direction, with the stated 28-nm, 134/6.49, 255/243 and below-0.4% claims retained as source claims. It does not establish accuracy-preserving end-to-end CIM acceleration because baselines, datasets, voltage/frequency, operation count, power boundary, measured-silicon status and manuscript-level validation remain unresolved.

**Source and location**

Evidence tier: Primary captured institutional technical report plus bounded source recovery assessment and existing digital cim explanation; no full paper extraction, reproduced model accuracy run, mapped array trace or measured silicon validation. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://www.cpc.pku.edu.cn/info/1015/2796.htm)

PKU institutional report section 10: Adder-DCIM; author publication page; publisher document 11240916; captured Problem, Mechanism / artifact, Workload, Hardware, Baseline, Measurements and Limits fields; no full manuscript or artifact recovered.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_institutional_technical_report

**Baselines:** Not named in the institutional report

**Evidence locators:** PKU report section 10: Adder-DCIM

author publication page

publisher document 11240916

**Evidence url:** https://www.cpc.pku.edu.cn/info/1015/2796.htm

**Hardware or process assumptions:** 28 nm process; source reports INT8 peak energy efficiency of 134 TOPS/W and throughput density of 6.49 TOPS/mm2, with voltage, frequency, power boundary, and measured-versus-modeled status unresolved.

**Limits:** Institutional report claims are not a manuscript or independent validation.

Voltage, frequency, operation-count convention, macro/full-system power boundary, named baselines, and measured-silicon details are unresolved.

Accuracy loss below 0.4% lacks dataset, reference accuracy, and percentage-point convention.

Do not substitute AdapCIM or SEGA-DCIM papers for this exact title; manuscript recovery remains required.

**Method or artifact:** Joint model compression and parallel bit-flexible digital CIM framework using synchronous parallel DCIM and minimum-selector circuitry for AdderNet.

**Metrics:** 134 TOPS/W INT8 peak energy efficiency

6.49 TOPS/mm2 throughput density

255 TOPS/W for ResNet20 at 4.2 average bits

243 TOPS/W for ResNet50 at 4.4 average bits

loss below 0.4% (source convention unresolved)

**Problem:** AdderNet inference still faces multiplication cost, fine-grained sparsity, and mixed-precision utilization constraints in digital compute-in-memory deployments.

**Workload or benchmark:** AdderNet inference with ResNet20 and ResNet50 cases; average bit widths reported as 4.2 and 4.4, while dataset and reference accuracy are not established in the source.

</details>

#### Additional source assessment

This separately recorded check is dated 2026-09-06. It supplements the original record above and retains its own scope and uncertainty.

[Assessment record](../../iccad/data/adder-dcim-primary-recovery-v1.json)

[Assessed source](https://www.cpc.pku.edu.cn/info/1015/2796.htm)

**Extraction scope**

Institutional report section 10, Adder-DCIM; author-page identity and publisher access check. No manuscript or artifact recovered.

**Headline metric status**

institutional_claims_only_not_accepted

**Independent review status**

pending

## What remains to establish

Resolve unspecified workloads, comparison methods, resource budgets, and source locations before generalizing a reported gain. Multiple papers in this selected sample permit comparison of mechanisms, but do not by themselves establish recurrence across years or a long-term trend.

[All subthemes](../expanded-taxonomy-v1.md) · [Research directions](../directions/README.md)
