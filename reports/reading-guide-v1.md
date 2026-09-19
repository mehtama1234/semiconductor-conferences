# Reading the semiconductor research articles

Start with a [theme](themes/README.md) for the underlying technical explanation. Follow a subtheme link to the papers that address that narrower problem. Open the source for the experiment and its recorded page, section, or table location. An unrecorded location is an unfinished evidence check.

## The questions a paper needs to answer

1. What work must the system complete, and what makes that difficult?
2. What exactly does the proposed method change?
3. Why should that change reduce time, energy, space, errors, or design effort?
4. What extra cost does it introduce?
5. What was compared, and were the inputs and required answer quality held constant?
6. Which conditions make the result stop applying?

## Terms used in the evidence records

**Workload:** the work executed in an experiment, including the program, input sizes, and request pattern.

**Baseline:** the comparison method or system. A speedup has meaning only relative to this choice and its settings.

**Latency:** elapsed time for an operation or request. **Throughput:** work completed per unit time. Increasing throughput can increase how long an individual request waits.

**Bandwidth:** data transferred per unit time. **Capacity:** data that can be stored. **Locality:** how closely the location and timing of data access allow values to be reused without expensive transfers.

**Energy and power:** energy is consumed while doing work; power is the rate of energy use. A power rating is not a measurement of energy per completed workload.

**Precision and quantization:** precision concerns how finely numbers are represented. Quantization maps values onto a limited set of representations. Using fewer bits can reduce storage and arithmetic cost while changing numerical error.

**EDA:** electronic design automation, software used to construct and check circuits. **RTL:** register-transfer level, a description of stored circuit state and the operations that update it. **HLS:** high-level synthesis, which constructs hardware from a higher-level program description.

**FPGA:** a field-programmable gate array, hardware with configurable logic and connections. **ASIC:** an application-specific integrated circuit, fabricated for a particular design. **GPU:** a graphics processing unit, also used to execute many computation tasks in parallel.

**PIM:** processing in memory, methods that perform computation in or close to memory structures. **CXL:** Compute Express Link, a connection standard used in some processor, device, and memory systems. The particular version and implementation matter to a performance claim.

**LLM:** a large language model. **Inference:** executing a trained model to produce outputs. **KV cache:** stored attention keys and values used when a language model generates further output. **MoE:** mixture of experts, a model organization that chooses among parts of the model for particular inputs.

**GEMM:** general matrix multiplication. **LUT:** a lookup table, which stores results or values to retrieve later. **ECC:** an error-correcting code, which adds information that can detect or correct specified data errors.

**PPA:** power, performance, and area. These are separate objectives. A paper should state how each changes and how any combined score is calculated.

## What an evidence label does and does not establish

The articles retain the source classifications from the research records. An official conference description can explain a proposal but omit experimental details. A link to a full preprint can still accompany a record extracted only from its abstract. Read the location and limitations with the label.

The paper evidence text is preserved in full and can use specialist terminology beyond these definitions. The theme explanations introduce the subjects; they do not substitute for a complete technical reading of every source.

## Reading a proposed trend

The [research directions](directions/README.md) explain hypotheses that connect several papers. The sample is uneven: it includes DAC and ISCA 2026 and ICCAD 2025 fallback material. Recurrence in this sample helps identify questions to investigate. Establishing change across years requires comparable populations and the same evidence rules in each year.
