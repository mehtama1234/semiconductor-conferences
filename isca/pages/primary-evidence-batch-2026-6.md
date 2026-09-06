# ISCA 2026 primary evidence batch 6

## PLENA: long-context agentic inference as a two-wall memory problem

PLENA distinguishes agentic inference from short-context chatbot serving. Web or
computer-use agents accumulate large DOMs, tool-call trajectories, and prolonged
interaction histories. The resulting workload is constrained by both memory
bandwidth and memory capacity, leaving on-chip compute underutilized.

The proposed response is a full hardware/software stack rather than one kernel:
asymmetric-quantization compute and memory units, a flattened systolic array with
native FlashAttention support, a custom ISA, compiler, cycle-emulated simulator,
and automated design-space exploration. The preprint reports up to 8.5x higher
utilization than existing accelerators, 2.24x throughput over an A100, and 3.85x
over a TPU v6e under matched multiplier and memory settings. [Primary preprint](https://arxiv.org/abs/2509.09505)

The detailed subskill is recognizing agentic context as a hardware workload
constraint and carrying that constraint through the ISA, compiler, array, memory
units, and search flow. The reported evaluation is simulated; area, energy,
context-length distributions, simulator validation, and open-source artifact
status still require full-paper verification.

## Near-Shannon lossless LLM weight compression

The weight-compression paper studies entropy across models from 1.5B to 405B
parameters and numeric formats from bf16 to int4, AWQ, and SQ8. It reports that
effective entropy is 2–10x lower than stored bitwidth, suggesting large lossless
footprint reductions without changing weight values.

Its mechanism is tile-level on-the-fly Asymmetric Numeral Systems decompression
aligned with GPU GEMM tiling. Integrated with SGLang and multi-GPU serving, the
system reaches within 0.01–0.1 bits of the Shannon limit, raises Qwen-14B maximum
batch size from 47 to 75, raises Mixtral-176B batch size from 20 to 95, and reports
up to 1.2x and 1.6x throughput gains respectively. The abstract also reports up
to 11x over NeuZip and DFloat11. [Primary preprint](https://arxiv.org/abs/2606.15789)

The detailed subskill is not just compression. It is compression whose decode
granularity, entropy code, GEMM tile schedule, serving runtime, and GPU memory
capacity are co-designed. The current evidence does not establish decompression
latency, bandwidth overhead, energy, quality invariance across all workloads, or
whether the mechanism requires dedicated hardware.

## Combined interpretation

PLENA attacks the memory wall by changing the accelerator stack for long-context
agentic execution. The compression work attacks it by reducing the representation
footprint while aligning decode with existing GPU computation. They are related
through memory capacity and movement, but they are not interchangeable solutions
and should not be collapsed into a single “memory optimization” score.
