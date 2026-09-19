# Analog compute in memory

This subject has 4 records in the selected sample. This page explains where it fits, then presents all captured paper evidence without shortening the measurements or limitations.

[Definitions used in the paper records](../reading-guide-v1.md)

## Understand the parent subject first

- [Analog mixed signal and emerging devices](../themes/analog-mixed-signal-and-emerging-devices.md)

## Computing where values are stored does not specify how arithmetic works

Compute-in-memory places some calculation within or immediately around a memory structure. Its purpose is to reduce repeated movement of stored values to a separate arithmetic unit. The calculation can be analog, digital, or a mixture. A memory technology alone does not determine which of these descriptions is correct.

This selected subject contains four records, including a digital lookup-table architecture that does not fit a strictly analog label. It remains here to preserve the existing coding and its review links, but its mechanism is identified correctly below. The grouping should not be treated as proof that all four papers use analog multiplication or share the same sources of numerical error.

## How conductance can implement a weighted sum

In an ideal resistive element, current equals conductance multiplied by applied voltage: I = G × V. If voltages represent inputs and conductances represent weights, currents collected from several elements can represent a sum of products. This is an elementary circuit model, not an assertion that every paper below implements this exact arrangement.

The useful output is still a number with a required accuracy. The system must encode the inputs as physical signals, allow the circuit to settle, and interpret the output. A digital-to-analog converter creates a signal from a digital value; an analog-to-digital converter turns a measured signal into a digital value. Their work, along with sensing and control, belongs in the system cost.

If actual conductance is G + ΔG, the idealized product changes by ΔG × V. Across an array, errors may accumulate or partly cancel depending on their signs and correlations. Wire resistance, noise, nonlinear response, and finite sensing range add other effects. Quantization introduces a different error by restricting numbers to a finite set. Neither device variation nor quantization should be described merely as a universal percentage loss independent of the workload.

<span id="explanation-dac-2026-research1233"></span>

## RM-CIMA: analog control speed matters only if the closed loop remains stable and safe

[RM-CIMA](../observed-subthemes/analog-compute-in-memory.md#paper-dac-2026-research1233) combines reinforcement learning with model predictive control and maps learning and optimization into analog computation. The official description reports 7.9× faster recovery from strong wind than nonlinear model predictive control, plus 2995.6× lower computational latency and 983.1× lower computational energy than unspecified traditional architectures. It does not provide absolute times, wind conditions, hardware settings, or measurement boundaries. Recovery of vehicle motion is distinct from computation time; these three factors cannot be multiplied into one gain. [Official DAC description](https://63dac.conference-program.com/presentation/?id=RESEARCH1233&sess=sess137).

Model predictive control repeatedly predicts future behavior, chooses an action over a finite planning interval, applies an action, and updates the calculation using new observations. Reinforcement learning adjusts behavior using experience and an objective. Coupling the two introduces learning costs and questions about how updates change the controller.

Faster computation can allow action on more recent state, but does not establish stability or safe behavior under every disturbance. A proper control evaluation must include sensor and actuator delays, the model's prediction error, update deadlines, and the conditions under which the controller's assumptions fail. For online learning, memory-write cost and the effect of changing parameters also matter. These are required evaluation dimensions, not recovered RM-CIMA guarantees.

The first gate is closed-loop control validity. Define the vehicle dynamics, MPC horizon, RL objective and update rule, wind disturbance, sensor and actuator delays, saturation, constraints and safety policy. Compare exact versus analog-computed controller outputs and measure trajectory error, overshoot, settling/recovery time, control effort, constraint violations and failure rate across disturbance profiles and random seeds. A shorter arithmetic latency can still produce an unsafe action if the state is stale, the model is wrong or the analog result crosses a control threshold.

The second gate is analog-system accounting. Analog CIM computation can be affected by device variation, noise, nonlinearity, drift, finite precision, array parasitics, ADC/DAC conversion, sensing, accumulation, calibration and parameter-write cost. Compare the complete state-to-actuation path with a matched digital NMPC baseline at equal tracking quality, including state acquisition, conversions, memory/programming, controller interface, idle power and safety monitoring. Computational energy is not automatically UAV energy, and recovery time is not the same metric as controller latency.

The official description reports 7.9× faster recovery from strong wind than traditional NMPC, 2995.6× lower computational latency and 983.1× lower computational energy than traditional architectures. The captured evidence does not expose absolute times, wind conditions, tracking metrics, controller details, device/peripheral conditions, calibration, closed-loop stability or complete UAV energy. It supports an analog-CIM RL/MPC control co-design direction, not demonstrated robust UAV flight performance or complete system efficiency.

## 3D-VRRAM LUT-CiM: low precision makes table-based computation practical

A lookup table stores answers or intermediate results indexed by discrete inputs. With b independent address bits, a complete table can require 2^b entries. This simple counting relation explains why reducing bit width can reduce table cost much faster than reducing it by one bit might suggest. Partitioned tables and shared intermediate results alter the implementation details, but still require a clear accounting of lookup, combination, and storage work.

The [3D-VRRAM/G-shuffle paper](../observed-subthemes/analog-compute-in-memory.md#paper-dac-2026-research1412) describes digital LUT computation with four-bit activations and channel-structured four-, two-, and one-bit weights. It combines quantization, reconfigurable computation modes, and physical remapping. The official description's maximum 8.9× area-efficiency and 9.7× energy-efficiency comparisons are not evidence that all operations use four-bit weights or that computation is analog. [Official DAC description](https://63dac.conference-program.com/presentation/?id=RESEARCH1412&sess=sess116).

The author-uploaded manuscript's Sections 4.1–4.2 and Table 2 identify SegFormer-B2: ADE20K segmentation changes from 34.4 to 43.6 mIoU versus round-to-nearest quantization, while NYUDv2 depth error changes from 0.73 to 0.51 RMSE. Full-precision results are 46.3 and 0.47. Thus the gains are over a quantized baseline, not over full precision.

Section 4.1.2 models the system at 28 nm, 0.9 V, and 400 MHz using silicon-derived VRRAM data and synthesized/simulated supporting circuits. Table 3 uses one prior result from a different language-model workload and another normalized for vision. Those comparisons are not all matched end-to-end measurements. [Author-uploaded manuscript, Sections 4.1–4.2 and Tables 1–3](https://www.researchgate.net/publication/408166556_Reconfigurable_3D-VRRAM_LUT-CiM_with_Greedy_G-shuffle_Quantization_for_End-to-End_4-bit_ViTs_in_Edge_Dense_Prediction).

<span id="explanation-dac-2026-research1412"></span>

## 3D-VRRAM LUT-CiM: a better 4-bit quantizer still has to survive the memory array and the complete edge path

Dense prediction produces a structured output at many image locations, so the useful quality constraint is task-specific: segmentation must preserve regions and classes, while depth estimation must preserve metric relationships and numerical error. A low-bit ViT can reduce storage and arithmetic, but lookup-table cost, mixed precision, activation movement and analog/memory nonidealities all determine whether the model is actually deployable.

The software side of the proposal uses Greedy G-Shuffle quantization and PCA-based channel-wise weight assignment to produce structured INT4/2/1 weights with INT4 activations. The hardware side uses a reconfigurable LUT-based CiM macro, pipeline/tensor-parallel dataflow, flexible 1TnR VRRAM read paths and channel-wise remapping so different ViT layers can use different precision and computation modes. The co-design addresses a real mismatch between heterogeneous layer workloads and a fixed LUT. It does not imply that a quantized model is full-precision equivalent or that a mode-reconfigurable macro has no switching, sensing, calibration or data-movement cost.

The first gate is model and device fidelity. Compare full precision, vanilla round-to-nearest and Greedy G-Shuffle at layer outputs and final dense-prediction outputs. Then inject VRRAM variation, drift, read noise, conductance nonlinearity, IR drop, ADC/sensing quantization, accumulation error and calibration residuals. Report per-layer error, mIoU/RMSE distributions, class or depth failure cases, temperature/voltage corners and whether INT4/2/1 remapping changes the error pattern. The manuscript's mIoU and RMSE improvements over round-to-nearest are quantization-baseline results; they do not establish equality with full precision.

The second gate is the complete macro accounting. LUT storage and lookup, remapping, read paths, ADC/DAC, accumulation, buffers, controllers, pipeline fill, tensor-parallel synchronization, mode selection, programming, calibration and reconfiguration must be included in area, energy and latency. State which values are measured silicon, silicon-derived device data, circuit simulation, synthesis or extrapolation. A normalized prior result from another workload or a vision-adjusted comparison cannot be treated as a matched end-to-end accelerator baseline.

The third gate is edge-system validity. Evaluate the entire model—including unsupported or non-LUT layers, preprocessing, feature movement, host/controller interaction, reconfiguration and output handling—on named hardware and a stated batch/latency target. Hold the dataset, resolution, model, precision, quality threshold, process, voltage, frequency and peripheral boundary constant against a digital 4-bit accelerator and fixed VRRAM-CiM design. Measure sustained latency, throughput, energy, area, memory capacity, temperature, calibration frequency, endurance and failure behavior rather than only a macro ratio.

The manuscript reports SegFormer-B2 mIoU of 43.6 versus 34.4 for vanilla round-to-nearest and 46.3 full precision on ADE20K, NYUDv2 RMSE of 0.51 versus 0.73 and 0.47 full precision, and a 28-nm/0.9-V/400-MHz modeled evaluation using silicon-derived VRRAM data and synthesized/simulated support circuits. It claims up to 8.9× area efficiency and 9.7× energy efficiency, but Table 3 includes normalized or differently scoped prior comparisons. The evidence supports low-precision reconfigurable VRRAM LUT-CiM co-design, not demonstrated universal 4-bit ViT edge deployment efficiency or fabricated endurance.

Dense prediction produces outputs across an image rather than a single image label. Mean intersection-over-union, or mIoU, compares predicted and reference regions and averages the overlap measure across classes. Root mean square error, or RMSE, summarizes numerical prediction errors, with larger errors weighted more strongly before taking the square root. Higher mIoU and lower RMSE are desirable, but they are not interchangeable accuracy percentages.

## SDM: a smooth decision changes sensitivity, not the need for validation

[SDM](../observed-subthemes/analog-compute-in-memory.md#paper-dac-2026-research1308) transforms a multivariable model into a univariate form and uses a one-ferroelectric-transistor analog content-addressable memory to compute a sigmoid. Its description reports 93.2% MNIST accuracy under 40 mV device variation, with a 0.54% drop versus 43.86% and 16.06% drops for decision-tree and random-forest comparisons. It does not define the variation distribution, percentage conventions, baseline hardware, or whether these outcomes were measured on fabricated circuits. [Official DAC description](https://63dac.conference-program.com/presentation/?id=RESEARCH1308&sess=sess120).

A hard decision switches branches when an input crosses a threshold. A sigmoid changes smoothly between low and high values. Near a hard threshold, a small perturbation can reverse the branch choice. A smooth function instead changes its output gradually, although its sensitivity still depends on slope and on how subsequent computation uses that value.

Content-addressable memory searches stored entries by their content rather than solely by an explicit address. An analog version can implement a graded matching response. A ferroelectric transistor uses a persistent polarization state to influence electrical behavior. Neither description establishes that every cell has identical response or that classification remains robust outside the tested conditions. Smoothness is a mechanism to examine, not a blanket immunity to variation.

<span id="explanation-dac-2026-research1308"></span>

## SDM: a soft decision can reduce threshold sensitivity, but variation, calibration and system cost still need measurement

A hard decision changes branches when an input crosses a threshold. That discontinuity makes a small device-induced shift capable of changing the selected branch. A sigmoid instead maps a scalar to a gradual value between low and high limits. This can make the output less abrupt near a boundary, but the slope, saturation, input scaling and later thresholding determine how much a voltage or conductance error changes the final class. Softness is therefore a circuit/algorithm co-design choice, not a proof of variation immunity.

SDM is described as transforming a multivariate interpretable model into a hardware-friendly univariate form and implementing the required sigmoid in a compact one-ferroelectric-transistor (1-FeFET) analog content-addressable memory (CAM). The CAM's analog response is used for a soft decision rather than a purely digital branch. The captured description does not specify the feature transform, stored parameters, CAM match/sense path, sigmoid transfer curve, ADC or peripheral circuitry, precision, calibration, or how multiple univariate decisions are combined. Those details determine whether the physical response corresponds to the intended model.

The first gate is device-to-model fidelity. Characterize the mapping from FeFET state and input voltage to the sensed analog output, then compare it with a numerical sigmoid over the full operating range. Report slope and saturation error, noise, quantization, input-scaling error, decision-boundary shifts, probability calibration and false-positive/false-negative behavior. Compare model outputs and MNIST predictions with a trusted digital reference. A smooth analog curve can still be systematically biased or miscalibrated.

The second gate is variation robustness. Define whether 40 mV means device-to-device threshold variation, temporal drift, spatially correlated variation or another quantity; state the distribution, number of instances, temperature/voltage conditions, aging, noise and whether parameters were retrained or calibrated for each instance. Evaluate fixed parameters on held-out device samples and report mean, worst-case and tail accuracy, accuracy confidence intervals, output error and calibration/retraining/storage cost. Separate inherent tolerance from compensation that consumes area, energy or test time.

The task comparison must also preserve its denominator. Identify the clean reference accuracy and whether the reported 0.54%, 43.86% and 16.06% values are absolute percentage-point drops or relative percentages, and inject variation at the same model/hardware boundary for SDM, decision tree and random forest. Measure feature preparation, CAM lookup, sensing, ADC/DAC, control, output transfer, latency, energy and area at matched MNIST quality and precision. A robustness percentage alone does not establish edge efficiency or preserved interpretability.

The official description reports 93.2% MNIST accuracy under 40 mV device variation, with a 0.54% drop for SDM versus reported 43.86% and 16.06% drops for decision-tree and random-forest comparisons. It does not expose absolute baseline accuracy, variation statistics, circuit conditions, calibration, sigmoid error, latency, energy, area, sample count or fabricated-silicon evidence. The evidence supports a soft-decision analog-CIM direction, not demonstrated calibrated, process-robust or end-to-end edge efficiency.

<span id="explanation-dac-2026-research2330"></span>

## HP-CIM: attention sparsity helps only when Top-K errors and ReRAM cost remain bounded

Attention compares a query with many keys, then uses normalized scores to weight the corresponding values. A sparse accelerator tries to keep only the important keys, reducing arithmetic and movement. The selection itself is part of the cost, however, and its errors are asymmetric: retaining an unimportant key wastes work, while discarding an important key changes the weighted sum and can affect every later layer.

HP-CIM is described as a hybrid ReRAM–SRAM computing-in-memory transformer accelerator. Its ReRAM-based hash predictor (ReHP) uses device variability for low-cost projections; a ReRAM content-addressable match and K-winner-take-all circuit select Top-K query-key candidates; an optimizable bias-softmax mechanism compensates information loss. These mechanisms move approximate projection and selection toward memory. They do not establish that the selected set matches dense attention, that device variability is stable, or that compensation recovers omitted information. Hash encoding, K/sparsity, thresholds, precision, calibration and controller behavior are not specified in the captured description.

The first gate is attention and model fidelity. Define the dense reference, Top-K rule, hash collisions, score threshold, K by layer/head, sequence length and precision. Report selected-edge recall and false-negative/false-positive rates, attention/logit error, perplexity or task quality, long-context behavior and per-layer failure cases against dense attention under matched prompts, seeds or decoding. A good average task score can hide a head or layer whose dropped key causes a rare but important failure; “bias-softmax compensation” is not proof of exact recovery.

The second gate is device-to-system validity. Characterize ReRAM conductance variation, noise, drift, nonlinearity, temperature, voltage, aging and read conditions through the projection, CAM match and K-WTA path. Include ADC/DAC, sensing, calibration, SRAM, buffers, digital control, hash metadata, data movement, unsupported layers and retries in latency, energy and area. Report fixed-parameter held-out devices separately from per-device calibration; exploiting variation does not make variation free.

Compare dense transformer acceleration, software sparsification and prior CIM accelerators at the same model, task, precision, sequence length, batch, quality target, technology, peripheral inclusion and end-to-end boundary. Measure Top-K selection, bias-softmax, memory transfers, setup, sustained p50/p95/p99 latency, energy/token, TOPS/W definition, area, thermal behavior and endurance. The official description reports 9.05–310.04× energy-efficiency improvement and 2.48–16.93× speedups across diverse tasks, but provides no accuracy, attention recall, absolute latency/energy, area, variation, ADC/DAC, endurance or per-model conditions. The evidence supports ReRAM-assisted attention sparsity and hybrid CIM, not demonstrated quality-preserving, variation-robust or fabricated-system transformer efficiency.

## HP-CIM: deciding what to skip must cost less than the work skipped

[HP-CIM](../observed-subthemes/analog-compute-in-memory.md#paper-dac-2026-research2330) combines ReRAM and SRAM computation with a ReRAM hash predictor. The description uses device variation for projections, content-addressable matching and a K-winner selection circuit, plus an adjustable bias-softmax mechanism to compensate information loss. It reports 9.05–310.04× energy efficiency and 2.48–16.93× speedups against prior CIM transformer accelerators. Model conditions, accuracy outcomes, comparator identities, and physical measurement scope remain unspecified. These ranges cannot be assigned to every workload or interpreted as fabricated-system measurements. [Official DAC description](https://63dac.conference-program.com/presentation/?id=RESEARCH2330&sess=sess138).

In attention, a query is compared with keys to determine how much information to use from different positions. A hash predictor replaces an expensive comparison with a compact representation intended to retain useful similarity. This is not a cryptographic guarantee. Selecting K candidates means retaining a fixed number according to the predictor's ranking, not proving that every discarded contribution is irrelevant.

Two error directions have different costs. Retaining an unimportant candidate wastes computation; discarding an important one can change the result. Softmax converts scores into normalized weights, so changing which scores are represented can affect the whole weighted combination. A compensating bias may improve task quality, but its name alone does not establish exact recovery of omitted information.

## What the four cases imply about system comparisons

These proposals target control-loop computation, discrete table arithmetic, nonlinear matching, and sparse-attention selection. Their shared question is whether performing a particular operation near stored state saves enough movement to justify encoding, sensing, selection, programming, and control costs.

A credible comparison keeps task quality and the timing boundary explicit. Circuit energy per operation cannot stand in for total vehicle energy, and peak arithmetic efficiency cannot establish application throughput. Calibration and programming may be occasional rather than per-operation costs, but should be amortized over a stated use period rather than omitted.

The author-uploaded LUT manuscript is available as extracted text with section and table locations; the separate PDF download failed, so exact PDF-page mapping remains unverified. Full manuscripts for the other three records were not recovered. The refreshed evidence supersedes historical card omissions, but device-to-task validation, taxonomy reconciliation, and independent reproduction remain open. These four mechanisms support a comparison, not a demonstrated long-term prevalence trend.

## Compare the results carefully

First identify the inputs and required output quality. Then identify the limited resource: time, memory, communication, energy, circuit area, or correctness coverage. Ask which part of the method reduces that cost and which new cost it adds. Compare numbers only when the experiments hold these conditions sufficiently similar.

A conference description may explain the proposal while omitting the full experiment. An author preprint link may have been coded from its abstract. The source classification does not by itself establish that every table was read. Missing locations remain visible below.

## Complete captured evidence

These are evidence records, not substitutes for the explanations above. Each record preserves its problem, proposed method, measurements, comparison conditions, and source limits. A populated record does not establish that its mechanism has been fully explained or independently verified.

<span id="paper-dac-2026-research1233"></span>

### RM-CIMA: An Analog Computing-in-Memory Accelerator for a Robust UAV Trajectory Tracking Framework

DAC 2026 · Record: `dac-2026-research1233`

[Read the step-by-step explanation](#explanation-dac-2026-research1233)

**Updated source-backed reading card**

Reviewed 2026-09-08. Deepens the existing RM-CIMA treatment into a paper-level reading; separates RL/MPC control co-design and analog CIM execution from closed-loop stability, tracking-error validation, analog nonidealities, conversion overhead and UAV-level energy, while preserving the 7.9x, 2995.6x and 983.1x claims.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

UAV trajectory tracking must react to disturbances with low latency and energy, while conventional architectures may respond too slowly to sudden wind or other dynamics.

**Mechanism / artifact:**

Reinforcement learning and model predictive control combined for online learning, mapped with MPC optimization onto a dedicated analog compute-in-memory accelerator RM-CIMA; controller equations, training/update policy, analog array, precision, peripherals and safety constraints are unspecified.

**Workload — the work tested:**

UAV trajectory-tracking under strong-wind disturbance compared with traditional nonlinear MPC and unspecified traditional architectures; vehicle dynamics, trajectory, wind profile, sensor/actuator delays, controller horizon, update rate, trials and tracking-error metrics are unspecified.

**Hardware and manufacturing assumptions:**

Analog CIM accelerator for edge UAV control with analog RL and MPC computation; device technology, array dimensions, ADC/DAC, sampling, precision, voltage, calibration, noise/variation, memory writes, controller interface and flight hardware are unspecified.

**Baseline — the comparison method:**

Traditional nonlinear model predictive control

Conventional digital/software trajectory-tracking architecture

Same UAV dynamics, disturbance profile, controller objective, sensor/actuator latency, numerical precision, peripherals, energy boundary and safety constraints are unspecified

**Reported measurements:**

The official description reports 7.9x faster recovery from strong wind than traditional NMPC, 2995.6x lower computational latency and 983.1x lower computational energy than traditional architectures; it supplies no absolute recovery time, tracking error, stability/safety result, analog hardware measurement, peripheral cost or complete UAV energy accounting.

**Limits on the conclusion:**

A faster controller calculation does not prove closed-loop stability or safe recovery. Define vehicle dynamics, MPC horizon, RL objective/update rule, wind disturbance, sensor and actuator delays, saturation and safety constraints; evaluate tracking error, overshoot, settling/recovery time, control effort, constraint violations, failure rate and worst-case seeds in simulation and hardware-in-the-loop or flight tests.

Analog CIM output is affected by device variation, noise, nonlinearity, finite precision, drift, ADC/DAC, sensing, accumulation, calibration and parameter-write cost. Compare the complete controller path against a matched digital baseline at equal control quality, including state acquisition, conversion, memory/programming, host interface and idle power.

The 7.9x, 2995.6x and 983.1x claims lack absolute times, wind conditions, tracking metrics, controller details, device/peripheral conditions and energy boundaries. The evidence supports an analog-CIM RL/MPC control co-design direction, not demonstrated robust UAV flight performance or complete system efficiency.

**Source and location**

Evidence tier: Primary captured official DAC description plus existing authored chapter level explanation; no full paper extraction, closed loop stability matrix, calibrated analog hardware or flight validation. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH1233&sess=sess137)

DAC 2026 official description; existing chapter-level analog-compute-in-memory RM-CIMA discussion; captured Problem, Mechanism / artifact, Workload, Hardware, Baseline, Measurements and Limits fields; no manuscript pages or reproduced analog-controller/flight evaluation.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** conventional digital accelerator

software trajectory-tracking implementation

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH1233&sess=sess137

**Hardware or process assumptions:** Analog CIM array and peripheral circuits for edge UAV inference; device technology, ADC/DAC overhead, precision, and power boundary are unspecified.

**Limits:** The description omits tracking error, latency, energy, area, precision, and noise tolerance.

Analog peripheral overhead and calibration may dominate system efficiency.

Official description only; robustness and hardware claims require paper-level evidence.

**Method or artifact:** Analog computing-in-memory accelerator coupled to a robust trajectory-tracking framework.

**Metrics:** Robust UAV tracking and accelerator efficiency are claimed qualitatively

**Problem:** UAV trajectory tracking requires low-latency, energy-efficient inference under noisy or changing conditions.

**Workload or benchmark:** UAV trajectory-tracking workloads; model, datasets, array dimensions, and controller baseline are unspecified.

</details>

<span id="paper-dac-2026-research1412"></span>

### Reconfigurable 3D-VRRAM LUT-CiM with Greedy G-Shuffle Quantization for End-to-End 4-Bit ViTs in Edge Dense Prediction

DAC 2026 · Record: `dac-2026-research1412`

[Read the step-by-step explanation](#explanation-dac-2026-research1412)

**Updated source-backed reading card**

Reviewed 2026-09-09. Deepens the 3D-VRRAM LUT-CiM treatment into a paper-level reading; separates Greedy G-Shuffle/PCA quantization, reconfigurable lookup modes and 1TnR remapping from model-quality baselines, VRRAM nonidealities, ADC/peripheral accounting, reconfiguration cost and edge-system scope, while preserving the ADE20K/NYUDv2, 28-nm/0.9-V/400-MHz and 8.9x/9.7x claims.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Edge dense-prediction ViTs need low-bit computation and compact, adaptable memory; LUT cost grows with bit width, convolution-heavy ViTs resist generic sub-8-bit quantization, and fixed LUT structures or unstructured mixed precision can waste capacity when static and dynamic layers differ.

**Mechanism / artifact:**

Software-hardware co-design combining Greedy G-Shuffle quantization, PCA-based channel-wise weight assignment and structured INT4/2/1 weights with a reconfigurable LUT-based CiM macro, pipeline/tensor-parallel dataflow, high-density 1TnR VRRAM flexible read paths and channel-wise hardware remapping; quantization error model, LUT decomposition, ADC/sensing, accumulation, reconfiguration protocol, calibration and peripheral overhead are condition-dependent.

**Workload — the work tested:**

4-bit Vision Transformers for edge dense prediction, including SegFormer-B2 evaluation on ADE20K semantic segmentation and NYUDv2 depth prediction; model layers, image resolution, training/fine-tuning recipe, calibration data, accuracy protocol, structured sparsity/weight distribution, batch/latency target and full-precision/quantized baselines require the manuscript conditions.

**Hardware and manufacturing assumptions:**

Reconfigurable 3D 1TnR VRRAM LUT-CiM macro modeled at 28 nm, 0.9 V and 400 MHz using silicon-derived VRRAM data with synthesized/simulated support circuits; array dimensions, VRRAM variation/drift, read path, ADC/DAC, peripheral area/energy, programming/reconfiguration, thermal/endurance and fabricated-silicon status are not fully established in the captured record.

**Baseline — the comparison method:**

Vanilla round-to-nearest quantization

Full-precision SegFormer-B2 reference

Digital 4-bit ViT accelerator

Fixed VRRAM-CiM architecture

State-of-the-art normalized area/energy comparisons

Same model, datasets, precision, calibration/training budget, output-quality target, process/voltage/frequency, peripheral inclusion and end-to-end measurement boundary are not uniformly matched

**Reported measurements:**

The source/manuscript reports ADE20K SegFormer-B2 mIoU 43.6 versus 34.4 for vanilla round-to-nearest quantization and 46.3 full precision, and NYUDv2 RMSE 0.51 versus 0.73 and 0.47 full precision; it claims up to 8.9x area efficiency and 9.7x energy efficiency over prior work, with 28-nm/0.9-V/400-MHz modeled conditions. It reports no complete measured macro result, variation/endurance, reconfiguration overhead, absolute latency/energy or fully matched system baseline in this card.

**Limits on the conclusion:**

Quantization gains must be separated from hardware nonidealities. Evaluate layer outputs and dense-prediction quality with VRRAM variation, drift, read noise, nonlinearity, IR drop, sensing/ADC quantization, accumulation error and calibration; compare INT4/2/1 paths with a trusted digital reference and report per-layer and task-level error. Better mIoU or RMSE than round-to-nearest does not establish equivalence to full precision.

A reconfigurable LUT-CiM macro must pay for mode selection, remapping, data movement, LUT storage, read paths, ADC/DAC, buffers, controllers, programming and calibration. Include these costs in area, energy and latency, and state whether values are measured silicon, silicon-derived models, circuit simulation or synthesis estimates. A normalized comparison from another workload or a fixed macro is not an end-to-end edge-system comparison.

The manuscript-backed results report ADE20K/NYUDv2 quality, 28-nm/0.9-V/400-MHz modeling and up to 8.9x/9.7x area/energy efficiency, but the evidence does not establish fabricated operation, endurance, variation tolerance, reconfiguration cost, complete peripheral accounting, sustained edge latency or matched full-system baselines. The evidence supports low-precision reconfigurable VRRAM LUT-CiM co-design, not demonstrated universal 4-bit ViT edge deployment efficiency.

**Source and location**

Evidence tier: Primary captured DAC description plus author uploaded manuscript section/table reading; system comparisons include modeled/synthesized support circuits and normalized prior results, with no independent reproduction or fabricated endurance validation. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://www.researchgate.net/publication/408166556_Reconfigurable_3D-VRRAM_LUT-CiM_with_Greedy_G-shuffle_Quantization_for_End-to-End_4-bit_ViTs_in_Edge_Dense_Prediction)

DAC 2026 official description; author-uploaded manuscript Sections 4.1–4.2 and Tables 1–3 as linked in the existing analog-compute-in-memory chapter; captured Problem, Mechanism / artifact, Workload, Hardware, Baseline, Measurements and Limits fields; device variation, fabricated macro, reconfiguration trace and independent end-to-end validation remain open.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** digital 4-bit ViT accelerator

fixed VRRAM CIM

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH1412

**Hardware or process assumptions:** 3D VRRAM LUT-CIM array with reconfiguration; device variation, ADC, and process assumptions are unspecified.

**Limits:** No accuracy, TOPS/W, area, endurance, variation, or reconfiguration results are reported.

Quantization and analog nonidealities may compound.

Official description only; device-to-task validation is required.

**Method or artifact:** Reconfigurable 3D-VRRAM lookup-table CIM with greedy group-shuffle quantization.

**Metrics:** Edge ViT efficiency and quality are claimed qualitatively

**Problem:** Edge vision transformers require low-bit compute and adaptable memory for dense prediction.

**Workload or benchmark:** 4-bit ViT dense-prediction workloads; device, model, accuracy, and baselines are unspecified.

</details>

<span id="paper-dac-2026-research1308"></span>

### SDM: A Variation-Tolerant Soft Decision Machine with In-Memory Sigmoid Computation

DAC 2026 · Record: `dac-2026-research1308`

[Read the step-by-step explanation](#explanation-dac-2026-research1308)

**Updated source-backed reading card**

Reviewed 2026-09-09. Deepens the SDM treatment into a paper-level reading; separates multivariate-to-univariate soft-decision transformation and 1-FeFET analog-CAM sigmoid computation from device-to-function transfer, calibration, variation distributions, probability calibration, accuracy accounting and edge-system efficiency, while preserving the 40 mV, 93.2%, 0.54%, 43.86% and 16.06% claims.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Decision trees and random forests can be costly or difficult to map to edge hardware, while analog in-memory nonlinear decisions are sensitive to device variation and a digital sigmoid implementation can require data movement and peripheral computation.

**Mechanism / artifact:**

Soft Decision Machine (SDM) hardware-algorithm co-design: transforms a multivariate interpretable model into a hardware-friendly univariate form and uses a compact one-ferroelectric-transistor (1-FeFET) analog content-addressable memory to compute the sigmoid/soft decision; feature transform, learned parameters, CAM sensing, sigmoid transfer curve, ADC/peripheral path, calibration, precision and variation-compensation procedure are unspecified.

**Workload — the work tested:**

MNIST classification at the edge; feature dimensionality, model size, train/test split, class balance, sigmoid parameterization, input scaling, accuracy definition, number of device samples, variation distribution/correlation and inference workload are unspecified.

**Hardware and manufacturing assumptions:**

Compact 1-FeFET analog CAM implementing a sigmoid response and soft decisions; FeFET process/node, array size, voltage, sensing/readout, ADC/DAC, peripheral circuits, retention/endurance, noise, temperature, device-to-device/within-device variation, calibration storage and silicon versus simulation status are unspecified.

**Baseline — the comparison method:**

Digital sigmoid computation

Variation-unaware in-memory sigmoid/CIM

Decision tree

Random forest

Same MNIST split, feature preprocessing, model quality target, device-variation samples, precision, hardware boundary and inference-time accounting are unspecified

**Reported measurements:**

The official description reports 93.2% MNIST accuracy under 40 mV device variation with a 0.54% accuracy drop for SDM, compared with reported 43.86% and 16.06% drops for decision-tree and random-forest baselines; it reports no absolute latency, energy, area, throughput, sigmoid error, calibration cost, variation distribution, sample count, confidence interval or fabricated-silicon result.

**Limits on the conclusion:**

A smooth sigmoid can reduce the discontinuity of a hard branch, but it is not automatically calibrated or variation-invariant. Define the device-to-sigmoid transfer, slope and saturation, input scaling, sensing/readout, quantization, noise and calibration; compare analog outputs with a numerical sigmoid and report approximation error, probability calibration, decision-boundary shifts, false positives/negatives and accuracy across held-out device instances. A nominal curve fit does not establish robust model behavior.

The 40 mV condition needs a distribution and physical interpretation: device-to-device versus temporal variation, spatial correlation, temperature/voltage dependence, measured versus modeled samples, worst-case/tail behavior and whether the model was retrained or recalibrated under variation. Evaluate unseen variation, aging, noise and operating corners with fixed parameters, and separate algorithmic robustness from compensation or retraining cost.

The DT/RF percentage drops must identify the clean reference, absolute accuracy, variation injection point and hardware/model boundary. Compare SDM, DT and RF at matched task quality, feature computation, memory capacity, precision, inference latency, energy and area; a robustness percentage alone does not show that SDM is more efficient or that the transformed model remains interpretable. Include feature transforms, CAM lookup, sensing, ADC/DAC, control and output transfer in edge-system measurements.

The official description supports an MNIST variation-tolerance result for a 1-FeFET analog-CAM sigmoid, but omits circuit conditions, calibration, absolute accuracy baselines, latency, energy, area, variation statistics and silicon evidence. The evidence supports a soft-decision analog-CIM direction, not demonstrated calibrated, process-robust or end-to-end edge efficiency.

**Source and location**

Evidence tier: Primary captured official DAC description plus existing authored analog cim discussion; no full paper extraction, reproduced sigmoid transfer, calibration procedure or independent variation/edge system evaluation. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH1308&sess=sess120)

DAC 2026 official description; existing analog-compute-in-memory chapter framing; captured Problem, Mechanism / artifact, Workload, Hardware, Baseline, Measurements and Limits fields; no manuscript pages, circuit schematic, measured variation matrix or fabricated-silicon validation.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** digital sigmoid computation

variation-unaware CIM

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH1308

**Hardware or process assumptions:** CIM array implementing sigmoid and soft decisions; technology, variation, and peripheral assumptions are unspecified.

**Limits:** No accuracy, variation, energy, area, latency, or silicon results are reported.

Approximate sigmoid behavior may affect calibration.

Official description only; measured variation testing is required.

**Method or artifact:** Variation-tolerant soft-decision machine with in-memory sigmoid computation.

**Metrics:** Variation tolerance and efficiency are claimed qualitatively

**Problem:** In-memory nonlinear decisions are sensitive to device variation and sigmoid implementation cost.

**Workload or benchmark:** Classification or edge inference workloads; device, precision, and baselines are unspecified.

</details>

<span id="paper-dac-2026-research2330"></span>

### HP-CIM: A Computing-in-Memory Transformer Accelerator with ReRAM-Based Hash Predictor for Attention Sparsity Exploitation

DAC 2026 · Record: `dac-2026-research2330`

[Read the step-by-step explanation](#explanation-dac-2026-research2330)

**Updated source-backed reading card**

Reviewed 2026-09-09. Deepens the HP-CIM treatment into a paper-level reading; separates ReRAM variability-based hash projection, CAM/K-WTA Top-K selection and bias-softmax compensation from attention recall, device/ADC variation, numerical quality, macro/system accounting and endurance, while preserving the reported energy-efficiency and speedup ranges with their missing task and hardware conditions.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Transformer attention compares many query-key pairs, making dense computation and memory movement expensive; sparsifying attention can save work but identifying the top keys itself costs hardware resources or can remove information needed for model quality.

**Mechanism / artifact:**

HP-CIM is described as a hybrid ReRAM–SRAM CIM transformer accelerator with a ReRAM-based hash predictor (ReHP) that uses device variability for low-cost projections, ReRAM CAM matching and a K-winner-take-all circuit for Top-K selection, plus an optimizable bias-softmax mechanism to compensate information loss; hash encoding, K/threshold, analog precision, calibration, ADC/DAC, mapping, controller and compensation training are unspecified.

**Workload — the work tested:**

Transformer inference across diverse tasks with attention sparsity exploitation; model families/sizes, sequence lengths, prompt/decode phase, heads, sparsity/K, precision, quality metrics, batch/concurrency, task suite and input distribution are unspecified.

**Hardware and manufacturing assumptions:**

Hybrid ReRAM and SRAM computing-in-memory macros with ReRAM CAM, K-WTA selection and analog/digital peripherals; ReRAM device/process, conductance variation, noise/drift, array size, ADC/DAC, sensing, calibration, endurance, frequency, thermal state, area and energy measurement boundaries are unspecified.

**Baseline — the comparison method:**

Dense transformer accelerator

Software attention sparsification

State-of-the-art CIM-based transformer accelerators

Same transformer models, precision, attention quality/recall, sequence length, batch, memory capacity, technology, peripheral inclusion, simulator/measurement method and end-to-end timing/energy boundary are unspecified

**Reported measurements:**

The official description reports 9.05–310.04x energy-efficiency improvement and 2.48–16.93x speedups over state-of-the-art CIM-based transformer accelerators across diverse tasks, but does not report accuracy/perplexity, attention recall, absolute latency/energy, TOPS/W definition, area, variation, ADC/DAC cost, endurance or per-model/task conditions.

**Limits on the conclusion:**

Top-K prediction has asymmetric errors: retaining an unimportant key wastes work, while dropping an important key changes the weighted sum and can propagate through layers. Define the exact attention reference, K/sparsity, hash collision behavior, score threshold, false-negative/false-positive rate, head/layer distribution and compare logits, perplexity/task quality and long-context tails with dense attention. Bias-softmax compensation is not proof of recovered information.

ReRAM variability is part of the predictor and also a source of drift, noise, nonlinearity and device-to-device mismatch. Characterize the projection/CAM/K-WTA path across conductance distributions, temperature, voltage, aging and read conditions; include ADC/DAC, sensing, calibration, digital control, SRAM, buffers, data movement and failure/retry in area, latency and energy. Report fixed-parameter held-out devices and calibration cost separately.

The headline ranges need model, task, sparsity, precision, batch, baseline and measurement boundaries. Compare dense and sparsified paths at matched quality, and include hash projection, Top-K selection, bias-softmax, unsupported layers, memory transfers, setup and output handling. Measure sustained inference, p50/p95/p99 latency, energy/token, area, thermal behavior and endurance. The evidence supports ReRAM-assisted attention sparsity and hybrid CIM, not demonstrated quality-preserving, variation-robust or fabricated-system transformer efficiency.

**Source and location**

Evidence tier: Primary captured official DAC description plus existing authored analog cim discussion; no full paper extraction, device to model accuracy validation, calibrated macro measurement or independent transformer reproduction. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH2330&sess=sess138)

DAC 2026 official description; existing analog-compute-in-memory chapter framing; captured Problem, Mechanism / artifact, Workload, Hardware, Baseline, Measurements and Limits fields; no manuscript pages, attention-recall table, device-variation matrix or reproduced ReRAM/SRAM macro evaluation.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** dense transformer accelerator

software attention sparsification

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH2330

**Hardware or process assumptions:** ReRAM CIM macro with hash prediction and analog/digital peripherals; variation and ADC assumptions are unspecified.

**Limits:** No accuracy, TOPS/W, area, latency, variation, or endurance results are reported.

Hash prediction errors may drop important attention edges.

Official description only; device-to-model validation is required.

**Method or artifact:** ReRAM-based hash predictor and CIM transformer dataflow.

**Metrics:** Sparse-transformer efficiency is claimed qualitatively

**Problem:** Transformer attention has irregular sparsity that is costly to detect and exploit in hardware.

**Workload or benchmark:** Transformer inference; attention patterns, ReRAM technology, and baselines are unspecified.

</details>

## What remains to establish

Resolve unspecified workloads, comparison methods, resource budgets, and source locations before generalizing a reported gain. Multiple papers in this selected sample permit comparison of mechanisms, but do not by themselves establish recurrence across years or a long-term trend.

[All subthemes](../expanded-taxonomy-v1.md) · [Research directions](../directions/README.md)
