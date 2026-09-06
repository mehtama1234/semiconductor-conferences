# ISCA 2026 primary evidence batch 3

## Cassandra: self-speculative decoding for edge reasoning LLMs

Cassandra targets the decode-stage cost of reasoning LLMs in low-batch edge
scenarios. The central design choice is to make self-speculation practical without
additional training: a compact draft representation is built by fine-grained data
selection, while pruning and mantissa truncation retain salient information in
weights and the KV cache. Full-precision parallel verification then checks the
candidate tokens.

The paper also treats representation conversion as a hardware problem. A
lightweight encoder-decoder module is proposed so Cassandra’s representation can
interoperate with standard floating-point formats on commercial GPUs and NPUs.
The author preprint reports up to 2.41x speedup over BF16 and 1.81x more tokens
than Eagle-3 under the same memory budget for Llama 3 8B on an NVIDIA GeForce
RTX 4090. [Primary preprint](https://arxiv.org/abs/2605.26558)

The detailed capability here is not simply “LLM quantization.” It is the joint
optimization of draft-model construction, KV-cache representation, verification
behavior, and the hardware path that converts representations. This makes
speculation a system contract spanning model values, memory footprint, token
acceptance, and accelerator interfaces.

The current evidence does not establish accuracy or acceptance-rate behavior
across a broad reasoning benchmark, nor does it establish the conversion unit’s
area or energy. Those details must be extracted from the full paper before the
reported speedups are generalized beyond the stated Llama 3 8B / RTX 4090 case.
