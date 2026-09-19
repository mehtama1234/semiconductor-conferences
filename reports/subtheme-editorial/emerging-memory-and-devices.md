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
