# Privacy preserving compute

This subject has 3 records in the selected sample. This page explains where it fits, then presents all captured paper evidence without shortening the measurements or limitations.

[Definitions used in the paper records](../reading-guide-v1.md)

## Understand the parent subject first

- [Power reliability and security](../themes/power-reliability-and-security.md)

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

## Compare the results carefully

First identify the inputs and required output quality. Then identify the limited resource: time, memory, communication, energy, circuit area, or correctness coverage. Ask which part of the method reduces that cost and which new cost it adds. Compare numbers only when the experiments hold these conditions sufficiently similar.

A conference description may explain the proposal while omitting the full experiment. An author preprint link may have been coded from its abstract. The source classification does not by itself establish that every table was read. Missing locations remain visible below.

## Complete captured evidence

These are evidence records, not substitutes for the explanations above. Each record preserves its problem, proposed method, measurements, comparison conditions, and source limits. A populated record does not establish that its mechanism has been fully explained or independently verified.

<span id="paper-dac-2026-research2265"></span>

### Sparsee: Unlocking Sparsities in Encrypted Sparse Matrix Multiplication via Hardware-Software Co-Design

DAC 2026 · Record: `dac-2026-research2265`

[Read the step-by-step explanation](#explanation-dac-2026-research2265)

**Updated source-backed reading card**

Reviewed 2026-09-09. Deepens the Sparsee treatment into a paper-level reading; separates secure Scatter-Gather-Apply, encrypted-index homomorphic permutation, Benes/Radix-k permutation hardware and selector-ciphertext expansion from FHE security, ciphertext correctness, sparsity leakage, parameter/noise growth, memory and full encrypted-SpMM cost, while preserving the 401.8x and 2594.3x source claims.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Fully homomorphic encryption hides sparse-matrix structure in ciphertexts, causing sparse matrix multiplication to resemble dense computation and making ciphertext arithmetic, movement and storage expensive.

**Mechanism / artifact:**

Sparsee recasts encrypted SpMM as secure Scatter-Gather-Apply, uses a homomorphic permutation network to gather using encrypted indices, maps that network to a hardware-friendly Benes topology with a pipelined Radix-k MDC Homomorphic Permutation Engine, and expands compressed selector ciphertexts on the fly in a Homomorphic Expansion Engine; FHE scheme, packing, selector format, security parameters, permutation proof and hardware precision are unspecified.

**Workload — the work tested:**

Encrypted sparse matrix multiplication with hidden sparsity pattern; matrix dimensions, nonzero distribution, density, index/value confidentiality, operand packing, ciphertext modulus/level, rotations/multiplications, batch/RHS count, datasets, correctness/error tolerance and compared software/hardware systems are unspecified.

**Hardware and manufacturing assumptions:**

Dedicated encrypted-compute accelerator with Benes permutation network, Radix-k multi-dimensional circular pipeline and on-the-fly selector-ciphertext expansion; technology, clock, memory capacity/bandwidth, on-chip storage, host link, area, power, security implementation, noise/precision and FPGA/ASIC status are unspecified.

**Baseline — the comparison method:**

Dense encrypted matrix multiplication

Software encrypted SpMM

State-of-the-art encrypted sparse-compute solution

Same FHE scheme/security level, matrix, packing, ciphertext parameters, correctness/privacy contract, hardware, preprocessing, data transfer and end-to-end timing/energy boundary are unspecified

**Reported measurements:**

The official description reports 401.8x average speedup and 2594.3x average energy reduction versus state-of-the-art solutions; it does not report absolute latency, throughput, energy, memory, ciphertext expansion, FHE operation count, security parameters, correctness/noise margin, leakage analysis or per-workload results.

**Limits on the conclusion:**

Encrypted indices and a homomorphic permutation can preserve sparsity without revealing the pattern only under a stated FHE scheme, security parameter, key/ciphertext handling and leakage model. Define which values, indices, access patterns, lengths, timing and metadata are public; prove or measure that selector compression, permutation routing and output behavior do not expose the sparse structure to the allowed adversary.

FHE correctness requires tracking ciphertext noise/modulus levels, rotations, key switching, multiplication depth, packing and decryption error. Compare decrypted outputs with plaintext SpMM and a dense encrypted reference, report failure/noise margin and parameter sets, and include selector expansion, permutation, accumulation and unsupported operations. A faster encrypted kernel is not valid if it changes the computation or exhausts the noise budget.

Speed and energy must include key generation/management where relevant, encryption/decryption, packing, selector compression/expansion, host-device transfers, memory, control, preprocessing and final output materialization. Hold security, correctness, matrix density, hardware and baseline optimization constant. The evidence supports privacy-aware encrypted sparse-SpMM co-design, not demonstrated security preservation, leakage resistance, FHE correctness across workloads or universal 401.8x/2594.3x end-to-end benefit.

**Source and location**

Evidence tier: Primary captured official DAC description plus existing authored privacy preserving compute discussion; no full paper extraction, independent fhe security/correctness validation, hardware implementation report or complete latency/energy accounting. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH2265&sess=sess108)

DAC 2026 official description; existing privacy-preserving-compute chapter framing; captured Problem, Mechanism / artifact, Workload, Hardware, Baseline, Measurements and Limits fields; no manuscript pages, FHE parameter table, leakage/security proof, decrypted-correctness report or reproduced accelerator benchmark.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** dense encrypted multiplication

software encrypted SpMM

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH2265

**Hardware or process assumptions:** Homomorphic or encrypted-compute accelerator; ciphertext precision and memory assumptions are unspecified.

**Limits:** No security parameters, latency, throughput, memory, energy, or accuracy results are reported.

Sparsity may interact with ciphertext expansion and leakage.

Official description only; cryptographic and hardware validation is required.

**Method or artifact:** Hardware-software co-design exploiting sparsity in encrypted SpMM.

**Metrics:** Encrypted sparse-compute efficiency is claimed qualitatively

**Problem:** Encrypted sparse matrix multiplication often loses sparsity benefits because ciphertext operations and formats are costly.

**Workload or benchmark:** Encrypted sparse matrix workloads; scheme, matrices, and accelerator are unspecified.

</details>

<span id="paper-dac-2026-research897"></span>

### MACH: Memory-Aware Configuration Generation for Homomorphically Encrypted Neural Networks

DAC 2026 · Record: `dac-2026-research897`

[Read the step-by-step explanation](#explanation-dac-2026-research897)

**Updated source-backed reading card**

Reviewed 2026-09-09. Deepens the MACH treatment into a paper-level reading; separates memory-aware configuration search and its static memory/latency model from FHE security, accuracy, noise margin, bootstrapping correctness and full end-to-end cost, while preserving the 4.97x, 91.88%, 128-bit and RTX 4060 Ti/16-GB claims.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Fully homomorphic encryption makes neural-network inference privacy-preserving but expands ciphertext storage and computation; on GPU HENN inference the bottleneck can shift from arithmetic to memory transfer when live encrypted state exceeds device capacity.

**Mechanism / artifact:**

MACH is described as a memory-aware design framework with a static model for memory footprint and latency and automatic design-space exploration over cryptographic, bootstrapping and encoding configurations. The objective trades computation against reduced memory footprint under a GPU-capacity constraint; scheme, packing, parameter-search, precision and refresh details are unspecified.

**Workload — the work tested:**

Homomorphically encrypted ResNet-20 and ResNet-18 across various GPU devices, including a reported 128-bit-security deployment on an RTX 4060 Ti with 16 GB device memory; FHE scheme, datasets, model accuracy target, batch size, ciphertext parameters, GPU list, baselines, preprocessing and end-to-end timing boundary are unspecified.

**Hardware and manufacturing assumptions:**

GPU-accelerated homomorphically encrypted neural-network inference with limited device memory; the source reports an RTX 4060 Ti with 16 GB for the 128-bit deployment, but GPU architecture, host system, memory hierarchy, software stack, frequency/power, transfer path and accelerator or ASIC status are unspecified.

**Baseline — the comparison method:**

Memory-oblivious HE configuration

Plaintext neural-network inference

Same FHE scheme, security level, model, accuracy/error target, ciphertext parameters, GPU, memory capacity, preprocessing, host-device transfers, bootstrapping policy and end-to-end timing boundary are unspecified

**Reported measurements:**

The source reports up to 4.97x speedup and 91.88% memory-footprint reduction for encrypted ResNet-20/18 across various GPUs, plus a first reported full-fledged 128-bit-security deployment on an RTX 4060 Ti with 16 GB device memory; it does not expose per-model/configuration results, accuracy, latency definition, throughput, energy, peak-versus-live memory, FHE operation counts, noise margin or security validation.

**Limits on the conclusion:**

A memory-aware configuration model can choose a feasible point in a search space, but feasibility requires a stated FHE scheme, security parameter, ciphertext modulus/levels, packing, scale/precision, multiplication depth, rotations, key switching, bootstrapping and noise margin. Compare decrypted outputs with a trusted plaintext and encrypted reference and report accuracy/error and failure rates across models and inputs.

Lower peak footprint can come from recomputation or extra ciphertext operations and does not by itself imply lower memory traffic, latency or energy. Define peak/live memory, transfers, preprocessing, key generation/management, encryption/decryption, bootstrapping, host-device movement and output materialization; report Pareto tradeoffs rather than one selected configuration.

The 4.97x, 91.88%, 128-bit and RTX 4060 Ti/16-GB claims do not establish universal encrypted-inference speedup, privacy preservation, accuracy retention, security compliance or hardware efficiency. Hold security, correctness, model, GPU capacity and timing boundary constant and report per-device results. The evidence supports memory-aware HE-NN configuration generation, not demonstrated secure, accuracy-preserving end-to-end improvement across deployments.

**Source and location**

Evidence tier: Primary captured official DAC description plus existing authored privacy preserving compute discussion; no full paper extraction, reproduced fhe security/correctness validation or complete end to end accounting. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH897)

DAC 2026 official description; existing privacy-preserving-compute editorial explanation; captured Problem, Mechanism / artifact, Workload, Hardware, Baseline, Measurements and Limits fields; no manuscript pages, cryptographic parameter table, decrypted-accuracy matrix, noise/failure trace or independent reproduction.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** memory-oblivious HE configuration

plaintext neural network

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH897

**Hardware or process assumptions:** FHE accelerator or software runtime; ciphertext memory and security assumptions are unspecified.

**Limits:** No security parameters, accuracy, memory, latency, energy, or configuration results are reported.

Memory constraints may trade against precision or security.

Official description only; cryptographic and hardware validation is required.

**Method or artifact:** Memory-aware configuration generation for HE neural networks.

**Metrics:** HE-NN configuration efficiency is claimed qualitatively

**Problem:** Encrypted neural networks require configurations balancing memory expansion, precision, and computation.

**Workload or benchmark:** Homomorphically encrypted neural networks; schemes, models, and hardware are unspecified.

</details>

<span id="paper-dac-2026-research989"></span>

### TAMI-MPC: Trusted Acceleration of Minimal-Interaction MPC for Efficient Nonlinear Inference

DAC 2026 · Record: `dac-2026-research989`

[Read the step-by-step explanation](#explanation-dac-2026-research989)

**Updated source-backed reading card**

Reviewed 2026-09-09. Deepens the TAMI-MPC treatment into a paper-level reading; separates single-round comparison/merge primitives, TEE-synchronized seeds, correlated-randomness reuse and streaming acceleration from the changed trust model, MPC security, nonlinear correctness and end-to-end communication accounting, while preserving the log(n)-to-1, 4.86x and 7.44x claims.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Secure nonlinear inference in MPC relies on communication- and computation-intensive primitives such as secure comparison, which can be impractical on resource-constrained edge platforms.

**Mechanism / artifact:**

TAMI-MPC redesigns leaf-comparison and merge primitives so each uses one interaction round in the described setting, replaces most oblivious-transfer use with synchronized seeds inside a trusted execution environment, reuses correlated randomness, and uses a specialized streaming/high-parallelism accelerator to reduce memory overhead. Protocol, seed provisioning, TEE isolation/attestation, malicious-security handling, precision and accelerator microarchitecture are unspecified.

**Workload — the work tested:**

Secure inference for ResNet-50 and bert-base; source reports comparison with state-of-the-art CNN and LLM frameworks, but does not identify MPC protocol, model variants, datasets, batch/sequence sizes, security adversary, network latency/bandwidth, communication payloads, preprocessing, accuracy/error or whether all layers and setup are included.

**Hardware and manufacturing assumptions:**

Edge secure-inference system with a TEE and specialized streaming accelerator; TEE technology, memory hierarchy, host/network interface, clock, area, power, process, accelerator implementation status, seed storage/provisioning, side-channel protections and failure/recovery behavior are unspecified.

**Baseline — the comparison method:**

Prior interactive MPC secure inference

Software MPC or state-of-the-art CNN/LLM frameworks

Same model, accuracy, cryptographic security, threat model, network, preprocessing, setup, communication accounting, hardware resources and end-to-end timing boundary are unspecified

**Reported measurements:**

The source claims leaf-comparison and merge round complexity reduced from log(n) to 1 per operation, OT eliminated for the vast majority of designs through synchronized TEE seeds, up to 4.86x speedup on ResNet-50 and up to 7.44x on bert-base; it reports no communication bytes, total rounds, setup/preprocessing, latency, throughput, accuracy, energy, area, security proof or TEE measurement.

**Limits on the conclusion:**

Reducing interaction rounds does not by itself reduce communication bytes or computation. Report per-primitive and end-to-end rounds, bytes, messages, preprocessing, seed generation/distribution, cryptographic operations, network latency/bandwidth and whether setup, input sharing, output reconstruction and model loading are included; compare against an equivalent MPC implementation under the same threat model.

Synchronized seeds and a TEE change what must be trusted. Define the adversary, compromised host/TEE assumptions, remote attestation, key/seed lifecycle, replay/freshness, memory disclosure, side channels, rollback and behavior under TEE compromise; establish privacy and integrity for nonlinear comparisons and correlated-randomness reuse rather than treating trust as free.

The log(n)-to-1, 4.86x and 7.44x claims do not establish secure, accurate, or universally faster end-to-end inference. Verify nonlinear approximation/exactness, model accuracy, malicious and semi-honest security, leakage, setup and communication cost, and accelerator area/power/latency. The evidence supports TEE-assisted low-interaction MPC acceleration, not demonstrated security-preserving deployment across networks and models.

**Source and location**

Evidence tier: Primary captured official DAC description plus existing authored privacy preserving compute discussion; no full paper extraction, reproduced cryptographic validation, tee security assessment or complete end to end accounting. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH989)

DAC 2026 official description; existing privacy-preserving-compute editorial explanation; captured Problem, Mechanism / artifact, Workload, Hardware, Baseline, Measurements and Limits fields; no manuscript pages, protocol transcript, security proof, communication trace, TEE attestation result or hardware reproduction.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** software MPC

interactive secure inference

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH989

**Hardware or process assumptions:** Trusted hardware or accelerator for MPC; cryptographic parameters and threat model are unspecified.

**Limits:** No security proof, communication, latency, energy, area, or model results are reported.

Trusted hardware changes the threat model.

Official description only; cryptographic and hardware validation is required.

**Method or artifact:** Trusted accelerator or protocol for minimal-interaction MPC inference.

**Metrics:** Secure inference efficiency is claimed qualitatively

**Problem:** Secure nonlinear inference under MPC is communication- and computation-intensive.

**Workload or benchmark:** Nonlinear secure inference; MPC protocol, models, and trust assumptions are unspecified.

</details>

## What remains to establish

Resolve unspecified workloads, comparison methods, resource budgets, and source locations before generalizing a reported gain. Multiple papers in this selected sample permit comparison of mechanisms, but do not by themselves establish recurrence across years or a long-term trend.

[All subthemes](../expanded-taxonomy-v1.md) · [Research directions](../directions/README.md)
