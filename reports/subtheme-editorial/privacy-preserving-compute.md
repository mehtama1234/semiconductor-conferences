## Three ways to reduce the cost of private inference

This subject groups sparse encrypted matrix operations, memory-aware encrypted-network configuration, and trusted acceleration of multiparty computation. These target different costs: arithmetic that may be unnecessary, storage required by the encrypted representation, and communication needed by a privacy protocol. Reducing one cost can increase another or change who must be trusted.

The closely named [privacy-preserving computing article](../observed-subthemes/privacy-preserving-computing.md) covers another three records. The two labels are preserved from the coding, not presented as separate established fields. Read them together, while keeping each paper's actual privacy assumptions distinct.

## Sparse plaintext does not necessarily mean sparse encrypted work

A sparse matrix has many zero entries. An ordinary multiplication can sometimes avoid storing or multiplying those entries. Encrypted computation adds a question: is the position of each zero public, or is it itself sensitive? Revealing which entries are skipped could disclose structure even if the nonzero values remain hidden.

[Sparsee](../observed-subthemes/privacy-preserving-compute.md#paper-dac-2026-research2265) proposes hardware-software co-design for encrypted sparse matrix multiplication. Its potential contribution is a representation and execution strategy that turns permitted sparsity information into less work. The captured description does not identify the encryption scheme, what structure is public, or the accelerator. Consequently it cannot support a claim that the method hides the sparsity pattern, nor that it exposes it. That boundary is unresolved.

<span id="explanation-dac-2026-research2265"></span>

## Sparsee: encrypted sparsity is useful only when privacy, FHE correctness, and the full cost boundary remain intact

Fully homomorphic encryption (FHE) lets a party compute on ciphertexts without first seeing plaintext values, but ciphertext arithmetic and movement are substantially more expensive than ordinary arithmetic. Sparse matrix multiplication has a second privacy question: if the locations of zeros or nonzeros are visible, the sparsity pattern may itself reveal sensitive structure. Hiding the pattern can force the implementation toward dense work unless the encrypted representation supplies a safe way to select and move only the needed values.

Sparsee is described as a secure Scatter-Gather-Apply formulation. A homomorphic permutation network gathers data using encrypted indices; a Benes topology and pipelined Radix-k multi-dimensional circular architecture implement the Homomorphic Permutation Engine; a Homomorphic Expansion Engine expands compressed selector ciphertexts on the fly. These mechanisms target encrypted indexing, routing and storage. The captured description does not specify the FHE scheme, packing, security parameters, selector format, key-switching/rotation costs, leakage model, noise budget or hardware implementation status.

The first gate is privacy. State which values, indices, access patterns, lengths, timing, traffic and metadata are public, and define the adversary. Show that selector compression, encrypted permutation, expansion, routing and output behavior do not reveal the sparse pattern beyond the allowed leakage. A protocol can hide numerical values while exposing which positions were selected; conversely, padding or oblivious routing can preserve privacy while erasing the claimed sparsity benefit.

The second gate is FHE correctness. Track ciphertext noise/modulus levels, rotations, key switching, multiplication depth, packing and decryption error. Compare decrypted outputs with plaintext SpMM and a dense encrypted reference across density, dimensions and batches; report numerical error, failure rate and remaining noise margin. Include permutation, selector expansion, accumulation and unsupported operations. Faster encrypted execution is not equivalent if the result changes or the noise budget is exhausted.

The source reports 401.8× average speedup and 2594.3× average energy reduction versus state-of-the-art solutions. It does not expose absolute latency, throughput, energy, memory, ciphertext expansion, FHE operation counts, security parameters, correctness/noise margin, leakage analysis or per-workload results. A fair boundary includes encryption/decryption where applicable, packing, selector compression/expansion, permutation, memory, host transfers, control and output materialization.

The evidence supports privacy-aware encrypted sparse-SpMM co-design, not demonstrated security preservation, leakage resistance, FHE correctness across workloads or universal 401.8×/2594.3× end-to-end benefit.

Evaluation should state matrix dimensions and sparsity structure, the encrypted and plaintext operands, the information disclosed, and the cost of arranging data for computation. A speed comparison against dense encrypted multiplication is informative only when both methods meet the same correctness and privacy requirements. The source provides no security parameters, numerical accuracy, memory, or performance measurements.

## Memory is a constraint on the whole encrypted configuration

<span id="explanation-dac-2026-research897"></span>

## MACH: make encrypted inference fit memory without confusing configuration feasibility with privacy or accuracy

[MACH](../observed-subthemes/privacy-preserving-compute.md#paper-dac-2026-research897) is described as a memory-aware design framework for homomorphically encrypted neural-network inference. It uses a static model of memory footprint and latency and explores cryptographic, bootstrapping and encoding configurations, trading extra computation for a smaller footprint under a GPU-memory limit. Encrypted representations carry more structure than the original numeric values: a usable configuration must fit live ciphertexts, temporary values, keys and supporting state, not merely the network weights.

The precise configuration choices are absent from the captured record. It would be inappropriate to assert a particular packing strategy, parameter search, precision, modulus schedule or refresh policy. A valid configuration must state the FHE scheme and security parameter, ciphertext modulus and levels, packing, scale/precision, multiplication depth, rotations, key switching, bootstrapping and noise margin. Compare decrypted outputs with a trusted plaintext and encrypted reference, reporting accuracy/error and failure rates.

Memory capacity and memory traffic are different quantities. Recomputing or choosing a more expensive cryptographic path can lower peak footprint while increasing operations, transfers or energy. Count preprocessing, key generation/management, encryption/decryption, bootstrapping, host-device movement and output materialization, and define whether latency includes them. Report peak/live memory, bandwidth, latency, throughput and energy under the same security and accuracy contract.

The source reports up to 4.97× speedup and 91.88% memory-footprint reduction for encrypted ResNet-20 and ResNet-18 across various GPUs. It also reports a 128-bit-security full-fledged deployment on an RTX 4060 Ti with 16 GB of device memory. These are bounded source claims: the record does not expose per-model results, GPU list, accuracy, noise margin, FHE operation counts, transfer boundary, energy or independent security validation. A memory reduction is not automatically a privacy, accuracy or end-to-end performance result.

The evidence supports memory-aware HE-NN configuration generation, not demonstrated secure, accuracy-preserving end-to-end improvement across deployments.

<span id="explanation-dac-2026-research989"></span>

## TAMI-MPC: fewer rounds can move the security boundary into the TEE

[TAMI-MPC](../observed-subthemes/privacy-preserving-compute.md#paper-dac-2026-research989) is described as a trusted-execution-environment (TEE)-accelerated framework for nonlinear secure multiparty computation. It redesigns leaf-comparison and merge primitives so each completes in one interaction round in the stated setting, uses synchronized seeds inside the TEE to avoid oblivious transfer for most designs, reuses correlated randomness, and maps the dataflow to a streaming, highly parallel accelerator. These are protocol and system mechanisms; they do not by themselves define the security guarantee.

Nonlinear operations do not simply preserve addition and scaling, so comparison semantics, approximation, fixed-point representation, truncation and failure behavior must be specified. Reducing rounds can matter on a high-latency link, but it does not necessarily reduce bytes, local cryptographic work, preprocessing or setup. Report per-primitive and end-to-end rounds, messages, bytes, seed generation/distribution, cryptographic operations, network conditions, input sharing, output reconstruction and model loading under the same MPC baseline.

The source reports a reduction from log(n) to 1 round per described operation, OT elimination for the vast majority of designs, up to 4.86× speedup on ResNet-50 and up to 7.44× on bert-base. It does not identify the MPC protocol, adversary, model/dataset, accuracy, sequence or batch size, communication trace, setup boundary, TEE technology, area, power or security proof. “Minimal-interaction” must not be expanded into “no communication,” and a TEE must not be presented as removing trust.

The changed trust boundary needs its own evaluation: define host and TEE compromise assumptions, remote attestation, key/seed lifecycle, freshness and replay protection, memory disclosure, rollback, side channels and behavior under TEE compromise. Validate privacy and integrity for nonlinear comparison and correlated-randomness reuse in both the claimed and stronger adversary models. Then compare secure accuracy and complete end-to-end cost, including accelerator overhead.

The evidence supports TEE-assisted low-interaction MPC acceleration, not demonstrated security-preserving deployment across networks and models.

## What would make the cross-paper comparison useful?

First state the same computation, acceptable error, private information, and adversary capabilities. Then identify whether each candidate actually meets those requirements. Only the candidates that do should be ranked by complete resource costs. The three records suggest useful optimization targets, but contain no quantitative evidence sufficient for that ranking. Their long-term implication is a question to investigate: which resource savings remain when privacy assumptions and final output quality are held fixed?
