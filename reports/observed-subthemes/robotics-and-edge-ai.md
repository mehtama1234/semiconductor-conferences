# Robotics and edge AI

This subject has 7 records in the selected sample. This page explains where it fits, then presents all captured paper evidence without shortening the measurements or limitations.

[Definitions used in the paper records](../reading-guide-v1.md)

## Understand the parent subject first

- [Systems applications and workloads](../themes/systems-applications-and-workloads.md)

## Start with the observation that causes an action

A robot receives incomplete measurements of its surroundings and its own state. Software interprets those measurements, selects an action, and sends a command to actuators. The resulting motion changes the next observation. This feedback distinguishes robot control from processing a fixed collection of images: a small decision error can change every later input.

The useful output is therefore not merely a fast prediction. It is an action that remains appropriate when executed. Record when the sensor captured the information, when computation began, when the command became available, and when motion began. A camera frame can wait in a queue even when the model itself runs quickly. A command can also wait for an actuator or for an earlier command to finish.

Two timing quantities must remain separate. **Output rate** counts completed actions per second. **Observation-to-action delay** measures how old the supporting observation is when an action becomes available or takes effect. A pipeline can improve the first without reducing the second. Hypothetically, a system could finish twenty actions each second while each action still depends on a measurement captured two hundred milliseconds earlier. Whether that delay is acceptable depends on motion, sensing, actuation, and the control law; there is no universal safe frequency for all robots.

These seven selected DAC 2026 papers intervene at different places: numerical inference, planning, reactive control, learning schedules, and geometric search. Three recovered manuscripts support page-level checks: DySL-VLA and ActionFlow version 1, and SwitchMT version 3. Four other records remain supported by refreshed official descriptions. Neither category constitutes independent reproduction or evidence of a change across years.

## Match each result to the part of the system it measures

| Paper | What it changes | What its result cannot establish alone |
|---|---|---|
| SpRDA | Repeated diffusion computation and its accelerator | Complete robot success or battery lifetime |
| HIP-MaN | Spatial representation and path generation | Shortest executed trajectory or collision-free physical motion |
| DySL-VLA | Which model layers execute for an action prediction | A universal safety rule for skipping computation |
| ENACT | Interacting reactive-control fields | General-purpose reasoning or calibrated uncertainty estimates |
| ActionFlow | Overlap between action-inference requests | Lower observation age merely from higher output rate |
| SwitchMT | When training moves between tasks | A deployed robot's task-switching reliability or chip energy |
| PS-CAM | Neighbor search within a point cloud | Full perception accuracy or navigation performance |

## Repeated inference: avoiding calculations still needs a quality test

A diffusion policy constructs an action prediction through repeated refinement. A sparse implementation avoids selected calculations, often because values are zero or changes between iterations are small. The saved arithmetic is useful only if identifying and representing the skipped work costs less than executing it. Irregular work can also leave some hardware units waiting while others remain busy.

[SpRDA](../observed-subthemes/robotics-and-edge-ai.md#paper-dac-2026-research2071) combines difference-aware caching, two-level sparsity adjustment, a sparsity-aware matrix array, and a vector unit for non-matrix operations. The description claims over 90% sparsity, 1.56–2.60× speedup, and 6.45–7.85× energy-efficiency improvement, without model, process, or named-comparator conditions. Its qualitative accuracy statement is not a quantified robot-success bound. [Source: official Description, mechanism and result sentences](https://63dac.conference-program.com/presentation/?id=RESEARCH2071&sess=sess143).

For this class of method, distinguish reuse that reconstructs the original result exactly from reuse that accepts a numerical difference. Measure a complete action prediction, including caches, indexing, non-matrix operators, and reconstruction. Then measure task success under the modified policy. Similar action vectors on a fixed dataset are not enough: a small error near contact can produce a different physical state, and subsequent errors may accumulate. Motor energy and idle waiting can also dominate whole-robot energy even when inference energy falls substantially.

### DySL-VLA: action continuity is a decision signal, not a safety proof

A vision-language-action model combines visual observations and a language instruction to predict robot commands. Layers transform intermediate numerical representations. Skipping a layer removes one such transformation; an additional adapter may approximate its effect. Deciding where to skip introduces its own computation and changes the prediction rather than merely moving unchanged work to another processor.

[DySL-VLA](../observed-subthemes/robotics-and-edge-ai.md#paper-dac-2026-research2721) retains selected layers, uses recent action continuity to guide skipping, and can recompute an action without skips. CALVIN and LIBERO evaluation is simulated. Table 2 reports 13.6 versus 51.0 ms **LLM** latency, but average successful sequence lengths are 2.89 versus 2.92. The 85.7× figure is a trainable-parameter ratio; reported training cost is 7 versus 112 GPU-hours. Table 4 instead lists the original sequence length as 2.82, an unresolved inconsistency. [Source: Section 3.3, PDF page 4; Sections 4.1–4.2, page 5; Tables 2–4, page 6](https://arxiv.org/pdf/2602.22896v1).

Smooth recent commands can suggest that the immediate computation is repetitive, but they cannot prove the next situation is unimportant. A smooth motion may approach a contact boundary or a newly visible obstacle. A useful evaluation varies those transitions and includes the cost of detecting and undoing a bad skip. An average number of completed subtasks is also not a success probability for an entire sequence. Report both, and preserve failures rather than describe nearly equal means as exact equivalence.

Action chunks add another distinction. Predicting several future commands at once can increase the command delivery rate without increasing how frequently the system uses a new observation. Evaluate the age of the last observation throughout the chunk and the rule for interrupting it. A model capable of producing many commands per second is not necessarily reacting to new information at that rate.

## Planning and reactive control solve different problems

A planner selects a route toward a goal. A reactive controller adjusts action using current measurements and internal state. A short route can take a long time to compute; a rapidly generated route can be longer or harder to execute. A controller can track its assigned target accurately while the larger navigation system chooses an unsuitable target.

[HIP-MaN](../observed-subthemes/robotics-and-edge-ai.md#paper-dac-2026-research2670) encodes location through combinations of periodic phases, computes a goal direction from phase differences, and generates detours when collision is predicted. The description reports paths 5–22% longer than optimal in a 200-by-200-metre environment, alongside faster path generation. It does not specify physical deployment, sensing, or comparison configurations. [Source: official Description, spatial encoding and evaluation sentences](https://63dac.conference-program.com/presentation/?id=RESEARCH2670&sess=sess121).

A periodic encoding repeats, so uniqueness requires an explicit supported range and sufficient numerical precision across the combined components. Position error can also alter the computed direction. To evaluate navigation, separate representation size, planning time, geometric path length, and executed motion. Include localization error, changing obstacles, clearance requirements, and cases where a local detour cannot reach the goal. Biological inspiration identifies a design motivation; it does not supply a correctness argument.

### ENACT: interacting state variables rather than several independent predictors

A dynamic neural field describes activity that changes over time according to inputs and interactions. An attractor is a state, or a pattern of states, toward which the dynamics tend to evolve. A controller can use such activity to retain a target through temporary missing observations and to change behavior when new input becomes dominant. Stability of the internal dynamics still needs to be connected to the dynamics of the controlled robot.

[ENACT](../observed-subthemes/robotics-and-edge-ai.md#paper-dac-2026-research2959) coordinates attention, gating, memory, and context fields for tracking under clutter and occlusion. The description reports simulation and Cortex-M7 benchmarking, with sub-millisecond control latency and comparisons against model predictive control. This is not the uncertainty-estimation ensemble suggested by the old card. Physical robot configuration and full experimental conditions remain unverified. [Source: official Description, field decomposition and benchmark sentence](https://63dac.conference-program.com/presentation/?id=RESEARCH2959&sess=sess177).

Model predictive control repeatedly evaluates future behavior under a model before choosing an action. Comparing it with a reactive method requires aligned constraints, prediction horizons, sensing, and tracking objectives. Root-mean-square tracking error summarizes the magnitudes of deviations over time; it can hide rare large errors. Recovery time requires a defined disturbance and a rule for deciding recovery is complete. Report those conditions, peak errors, and unsafe outcomes alongside typical latency and memory use.

## Pipelining: throughput is not a timestamp

An autoregressive action model predicts output tokens sequentially. A token is one encoded output element, not necessarily a complete physical command. Input processing and later token generation can have different resource demands. Overlapping stages from different requests may use hardware more efficiently, but each request must keep its own history and dependency ordering.

[ActionFlow](../observed-subthemes/robotics-and-edge-ai.md#paper-dac-2026-research1400) overlaps requests and packs their computation with shared-buffer management. Table 1 reports OpenVLA-7B at 3.20 FPS on AGX Orin and 19.45 FPS on RTX 5090. Its time column is labeled milliseconds, yet 0.3131 is consistent with **seconds** per output at 3.20 FPS. Table 2 gives different LIBERO success rates; the AGX comparison in the prose uses the displayed RTX baseline. Trial counts and a statistical equivalence test are not supplied there. [Source: Sections 3–4, PDF pages 3–6; Tables 1–2, page 6](https://arxiv.org/pdf/2512.20276v1).

The unit mismatch should be resolved before citing latency. Even a correctly labeled reciprocal of throughput is not automatically the elapsed time for one request from its observation to completion. Record the pipeline startup, request admission times, output timestamps, and the disposition of stale outputs. Compare success using identical seeds, task counts, hardware, and timing rules. A software transformation may aim to preserve numerical behavior while a changed execution schedule still changes the observations a moving robot receives.

## Training across tasks is not switching a deployed robot's job

Reinforcement learning updates a policy using outcomes of chosen actions. Training across several tasks can cause interference: an update useful for one task changes shared parameters used by another. A task-switching training policy chooses which environment supplies the next experience. That differs from deciding when an operating robot should abandon its current physical objective.

[SwitchMT](../observed-subthemes/robotics-and-edge-ai.md#paper-dac-2026-research2794) changes training environments when relative parameter change falls below a threshold. Version 3 evaluates Atari games in Gymnasium on RTX 4090 machines, with four million frames per environment. Table 2 improves Breakout against MTSpark_ADD but has lower Pong and Enduro scores. Table 3 gives both methods 3,300,357 trainable parameters. This is learning evidence, not physical robot or neuromorphic-chip energy evidence. [Source: Section 3.2.2 and Section 4, PDF page 4; Tables 2–3, page 6](https://arxiv.org/pdf/2504.13541v3).

A spiking network represents some communication using discrete events while maintaining numerical state between them. It can be simulated on an ordinary GPU; the model type alone does not establish event-driven hardware power savings. Equal parameter counts likewise do not mean equal memory use or energy: training also stores optimizer state, replay data, and any history used by the switching policy. Small parameter changes can indicate stalled optimization rather than task mastery. Test learning quality, forgetting, and total resource cost separately.

## Geometric search is an input operation, not the robot's decision

A point cloud contains sampled three-dimensional positions. Neighbor search finds points close to a query: a ball query uses a distance radius, while k-nearest-neighbor search requests a particular number of closest points. These are related but different output conditions. Regions with uneven point density can require very different radii to collect the same number of neighbors.

[PS-CAM](../observed-subthemes/robotics-and-edge-ai.md#paper-dac-2026-research406) uses NOR content-addressable memory for range queries, activates selected regions, and performs expanding ball queries for neighbor search. Density-aware radius estimation reduces repeated searches. The description supplies speed and energy-efficiency ranges but omits point counts, precision, exactness checks, and named baseline settings. [Source: official Description, query conversion, radius estimation, and result sentences](https://63dac.conference-program.com/presentation/?id=RESEARCH406&sess=sess119).

Content-addressable memory compares a query against stored content rather than fetching only a supplied address. Its usefulness depends on how the geometric predicate is encoded and how many cells must participate. An estimated radius is not itself proof that the returned set contains the true nearest neighbors. Evaluate exactness or recall, candidate filtering, encoding, loading, and all repeated queries. Then measure the downstream perception task with the returned neighborhoods. A faster search circuit does not establish a faster or more reliable complete robot.

## Combined interpretation and evidence still needed

The cross-paper insight is that a robotics acceleration claim has at least three boundaries: numerical behavior, timing of information, and physical outcome. A method can preserve one while changing another. Useful cross-paper comparisons must name which boundary was tested and keep sensing, actuation, task difficulty, and allowable failures explicit.

A testable long-term hypothesis is that computation allocated according to current task sensitivity can outperform uniform processing under limited resources. Challenge it with abrupt scene changes, contact transitions, irregular geometry, and situations where detecting importance costs as much as the saved work. These are proposed stress tests, not demonstrated failures of every method above. Comparable earlier-edition evidence is still required for a temporal trend.

Sources were checked on 2026-09-07. The ENACT author-lab announcement corroborated identity but did not provide a recovered manuscript. Title searches did not recover full papers for SpRDA, HIP-MaN, or PS-CAM. Their Description sections remain the available evidence locations, not PDF pages. The DySL-VLA repository was inspected for availability only; no training, inference, hardware deployment, or robot actuation was executed. Final-version matching, numerical discrepancies, broader experimental conditions, and independent scientific review remain open.

## Compare the results carefully

First identify the inputs and required output quality. Then identify the limited resource: time, memory, communication, energy, circuit area, or correctness coverage. Ask which part of the method reduces that cost and which new cost it adds. Compare numbers only when the experiments hold these conditions sufficiently similar.

A conference description may explain the proposal while omitting the full experiment. An author preprint link may have been coded from its abstract. The source classification does not by itself establish that every table was read. Missing locations remain visible below.

## Complete captured evidence

These are evidence records, not substitutes for the explanations above. Each record preserves its problem, proposed method, measurements, comparison conditions, and source limits. A populated record does not establish that its mechanism has been fully explained or independently verified.

<span id="paper-dac-2026-research2071"></span>

### SpRDA: An Efficient Sparse Accelerator for Robotics Diffusion Model

DAC 2026 · Record: `dac-2026-research2071`

**Updated source-backed reading card**

Reviewed 2026-09-07. Refreshed description supplies sparse mechanisms and conditional metrics omitted by the old card.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Repeated diffusion inference strains robot computation.

**Mechanism / artifact:**

Difference-aware caching, sparsity adjustment, matrix array, and vector processing.

**Workload — the work tested:**

Robotics diffusion models; exact tasks absent.

**Hardware and manufacturing assumptions:**

Process, precision, fabrication status, and power accounting unspecified.

**Baseline — the comparison method:**

Prior diffusion accelerators, unnamed.

**Reported measurements:**

Reports over 90% sparsity, 1.56–2.60× speedup, and 6.45–7.85× energy efficiency.

**Limits on the conclusion:**

Qualitative accuracy wording is not a task-success bound. Complete inference and robot energy boundaries require full experimental evidence.

**Source and location**

Evidence tier: Refreshed official description. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/presentation/?id=RESEARCH2071&sess=sess143)

Description, mechanism and final-result sentences; no PDF pagination.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** dense diffusion accelerator

CPU/GPU robotics inference

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH2071

**Hardware or process assumptions:** Edge robotics accelerator with sparse dataflow and memory hierarchy; precision and process assumptions are unspecified.

**Limits:** No policy quality, latency, energy, area, or sparsity results are reported.

Structured sparsity may reduce policy fidelity.

Official description only; closed-loop robot evaluation is required.

**Method or artifact:** Sparse accelerator architecture for robotics diffusion inference.

**Metrics:** Robotics inference efficiency is claimed qualitatively

**Problem:** Robotics diffusion models require repeated denoising steps and can exceed edge compute and energy budgets.

**Workload or benchmark:** Robotics diffusion policies; model sparsity, tasks, accelerator organization, and baselines are unspecified.

</details>

<span id="paper-dac-2026-research2670"></span>

### HIP-MaN: Hippocampus-Inspired Periodic Mapping and Navigation for Autonomous Mobile Robot

DAC 2026 · Record: `dac-2026-research2670`

**Updated source-backed reading card**

Reviewed 2026-09-07. Refreshed description establishes a planning-time versus path-length tradeoff.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Repeated map-based planning can be expensive.

**Mechanism / artifact:**

Periodic phase encoding, phase-difference goal direction, and collision-triggered detours.

**Workload — the work tested:**

200-by-200-metre environment; static/dynamic obstacles.

**Hardware and manufacturing assumptions:**

Processor, sensors, and physical-deployment boundary unspecified.

**Baseline — the comparison method:**

Optimal path for length; unnamed planning-time comparators.

**Reported measurements:**

Reports 5–22% longer paths; static path generation 3–50× faster, dynamic 5–346× faster.

**Limits on the conclusion:**

Path-generation time is not travel time. Localization, obstacle prediction, and encoding range require full-paper checks.

**Source and location**

Evidence tier: Refreshed official description. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/presentation/?id=RESEARCH2670&sess=sess121)

Description, encoding and final evaluation sentences; no PDF pagination.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** standard SLAM/navigation stack

neural navigation baseline

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH2670

**Hardware or process assumptions:** Not established in the captured evidence.

**Limits:** No success rate, latency, energy, map quality, or environment-diversity results are reported.

Biological inspiration does not establish robustness.

Official description only; physical-robot validation is required.

**Method or artifact:** Periodic mapping and navigation architecture inspired by hippocampal representations.

**Metrics:** Navigation robustness and efficiency are claimed qualitatively

**Problem:** Mobile robots need robust mapping and navigation under changing environments and limited edge resources.

**Workload or benchmark:** Autonomous mobile-robot navigation; environments, sensors, compute target, and baselines are unspecified.

</details>

<span id="paper-dac-2026-research2721"></span>

### DySL-VLA: Efficient Vision-Language-Action Model Inference via Dynamic-Static Layer-Skipping for Robot Manipulation

DAC 2026 · Record: `dac-2026-research2721`

**Updated source-backed reading card**

Reviewed 2026-09-07. Recovered evaluation separates model latency, trainable parameters, and simulated task quality.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

VLA inference is expensive; skipping changes the computation.

**Mechanism / artifact:**

Retain selected layers and use action continuity to guide skipping and recomputation.

**Workload — the work tested:**

CALVIN and LIBERO simulation.

**Hardware and manufacturing assumptions:**

RTX 4090, A6000, and Jetson Orin timing.

**Baseline — the comparison method:**

RoboFlamingo; OpenVLA-OFT; DeeR-VLA.

**Reported measurements:**

Table 2: 51.0 to 13.6 ms LLM latency; sequence length 2.92 to 2.89. Trainable parameters: 85.7× reduction; GPU-hours: 112 to 7.

**Limits on the conclusion:**

Not whole-loop latency or exact quality equivalence. Tables 2 and 4 disagree on baseline sequence length (2.92 versus 2.82).

**Source and location**

Evidence tier: Recovered manuscript; cited sections inspected. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://arxiv.org/pdf/2602.22896v1)

Section 3.3, PDF page 4; Sections 4.1–4.2, page 5; Tables 2–4, page 6.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** dense VLA inference

static layer skipping

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH2721

**Hardware or process assumptions:** Edge robot inference accelerator or GPU; precision, memory, and timing assumptions are unspecified.

**Limits:** No task success, latency, energy, quality degradation, or model results are reported.

Dynamic skipping can introduce control jitter.

Official description only; closed-loop manipulation tests are required.

**Method or artifact:** Dynamic-static layer-skipping inference strategy for VLA models.

**Metrics:** Manipulation efficiency and task quality are claimed qualitatively

**Problem:** Vision-language-action models are expensive for real-time robot manipulation.

**Workload or benchmark:** Robot manipulation tasks and VLA models; skipped layers, accuracy, hardware, and baselines are unspecified.

</details>

<span id="paper-dac-2026-research2959"></span>

### ENACT: Ensemble Neural Fields for Reactive Robot Control

DAC 2026 · Record: `dac-2026-research2959`

**Updated source-backed reading card**

Reviewed 2026-09-07. Refreshed source corrects the interpretation of ensemble fields and identifies MCU benchmarking.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Track targets through clutter, disturbances, and occlusion.

**Mechanism / artifact:**

Coordinate attention, gating, memory, and context dynamic neural fields.

**Workload — the work tested:**

Tracking simulation and microcontroller benchmarking.

**Hardware and manufacturing assumptions:**

Cortex-M7; exact board and robot setup absent.

**Baseline — the comparison method:**

Model predictive control, configuration unspecified.

**Reported measurements:**

Reports up to 86% lower RMS tracking error, about 2.8× faster recovery, sub-ms control latency, about 9× lower SRAM.

**Limits on the conclusion:**

Not an uncertainty-estimation ensemble. Disturbance definition, peak errors, stability conditions, and physical-robot setup require the manuscript.

**Source and location**

Evidence tier: Refreshed official description. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/presentation/?id=RESEARCH2959&sess=sess177)

Description: field modules and benchmark sentence; no PDF pagination.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** classical reactive controller

single neural-field controller

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH2959

**Hardware or process assumptions:** Real-time robot control compute; sensor, latency, and actuation assumptions are unspecified.

**Limits:** No stability, success, latency, energy, or sim-to-real results are reported.

Ensemble cost may conflict with real-time constraints.

Official description only; physical-robot evaluation is required.

**Method or artifact:** Ensemble neural-field representation for reactive robot control.

**Metrics:** Reactive control quality and uncertainty handling are claimed qualitatively

**Problem:** Reactive control needs fast spatial representations while handling uncertainty and changing scenes.

**Workload or benchmark:** Robot control and navigation tasks; sensors, dynamics, models, and baselines are unspecified.

</details>

<span id="paper-dac-2026-research1400"></span>

### Actionflow: A Pipelined Action Acceleration for Vision Language Models on Edge

DAC 2026 · Record: `dac-2026-research1400`

**Updated source-backed reading card**

Reviewed 2026-09-07. Recovered tables reveal a time-unit discrepancy and an unmatched platform comparison.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Sequential action decoding underuses GPU resources.

**Mechanism / artifact:**

Cross-request pipelining, packed computation, and unified attention-state buffers.

**Workload — the work tested:**

OpenVLA-7B; LIBERO evaluation.

**Hardware and manufacturing assumptions:**

AGX Orin 64 GB and RTX 5090; PyTorch 2.6.0.

**Baseline — the comparison method:**

Standard autoregressive baseline; naive pipeline.

**Reported measurements:**

Table 1: 3.20 versus 1.25 FPS on Orin; 19.45 versus 7.62 FPS on RTX 5090.

**Limits on the conclusion:**

Time column labeled ms is consistent with seconds per output. Table 2 lacks a displayed Orin baseline; equivalent success and observation-to-action latency are not established.

**Source and location**

Evidence tier: Recovered manuscript; cited sections inspected. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://arxiv.org/pdf/2512.20276v1)

Sections 3–4, PDF pages 3–6; Tables 1–2, page 6.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** dense edge VLM inference

non-pipelined action generation

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH1400

**Hardware or process assumptions:** Edge accelerator with pipelined VLM/action stages; precision and memory assumptions are unspecified.

**Limits:** No action latency, success, energy, memory, or model results are reported.

Pipelining may increase buffering and stale decisions.

Official description only; closed-loop task validation is required.

**Method or artifact:** Pipelined action-acceleration architecture for edge VLMs.

**Metrics:** Interactive action efficiency is claimed qualitatively

**Problem:** Edge VLM action generation must meet interactive latency and memory limits.

**Workload or benchmark:** Vision-language-action workloads; models, edge hardware, and baselines are unspecified.

</details>

<span id="paper-dac-2026-research2794"></span>

### Scalable Multi-Task Learning Through Spiking Neural Networks with Adaptive Task-Switching Policy for Intelligent Autonomous Agents

DAC 2026 · Record: `dac-2026-research2794`

**Updated source-backed reading card**

Reviewed 2026-09-07. Recovered version 3 establishes Atari/GPU training, not physical-agent energy validation.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Fixed training intervals can allocate experience poorly across tasks.

**Mechanism / artifact:**

Switch environments using relative parameter-change threshold and task-conditioned spiking network.

**Workload — the work tested:**

Pong, Breakout, Enduro; four million frames per environment.

**Hardware and manufacturing assumptions:**

Gymnasium on RTX 4090 machines.

**Baseline — the comparison method:**

MTSpark_ADD with fixed 25-episode intervals; other Q-network variants.

**Reported measurements:**

Table 2: SwitchMT/MTSpark_ADD Pong −8.8/−5.4, Breakout 5.6/0.6, Enduro 355.2/371.2.

**Limits on the conclusion:**

Not uniformly higher scores. Equal trainable-parameter counts do not prove equal total memory or energy; no robot or neuromorphic-chip deployment established.

**Source and location**

Evidence tier: Recovered manuscript; cited sections inspected. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://arxiv.org/pdf/2504.13541v3)

Section 3.2.2 and Section 4, PDF page 4; Tables 2–3, page 6.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** dense multi-task neural network

fixed task-switching SNN

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH2794

**Hardware or process assumptions:** Neuromorphic or event-driven edge hardware; spike precision and timing assumptions are unspecified.

**Limits:** No task success, latency, energy, spike count, or transfer results are reported.

Adaptive switching may cause task interference.

Official description only; physical-agent validation is required.

**Method or artifact:** Multi-task SNN with adaptive task-switching policy.

**Metrics:** Agent efficiency and task quality are claimed qualitatively

**Problem:** Autonomous agents must switch among tasks under tight energy and latency budgets.

**Workload or benchmark:** Autonomous-agent tasks; sensors, environments, hardware, and baselines are unspecified.

</details>

<span id="paper-dac-2026-research406"></span>

### PS-CAM: An Efficient Content-Addressable Memory Based Accelerator for Point Search in Point Clouds

DAC 2026 · Record: `dac-2026-research406`

**Updated source-backed reading card**

Reviewed 2026-09-07. Refreshed description distinguishes ball queries from progressive nearest-neighbor search.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Point-cloud neighbor search is costly.

**Mechanism / artifact:**

NOR-CAM range queries, selective bank activation, and density-guided expanding radii.

**Workload — the work tested:**

Ball query and k-nearest neighbors; point counts absent.

**Hardware and manufacturing assumptions:**

Memory technology details, precision, and evaluation method unspecified.

**Baseline — the comparison method:**

Prior works, unnamed.

**Reported measurements:**

Ball query: 1.25–1.33× speedup, 142× energy efficiency. KNN: 4.6–27.2× speedup, 7.1–2578× energy efficiency.

**Limits on the conclusion:**

These ranges lack matched baseline conditions. Radius estimation alone does not prove exact neighbors; no full perception or robot result established.

**Source and location**

Evidence tier: Refreshed official description. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/presentation/?id=RESEARCH406&sess=sess119)

Description, query mechanisms and result sentence; no PDF pagination.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** CPU/GPU point search

SRAM-based spatial index

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH406

**Hardware or process assumptions:** CAM-based accelerator with parallel comparisons; precision, capacity, and process assumptions are unspecified.

**Limits:** No recall, latency, energy, area, capacity, or point-density results are reported.

CAM scaling and comparison energy may dominate.

Official description only; workload-diverse hardware validation is required.

**Method or artifact:** Content-addressable-memory point-search accelerator.

**Metrics:** Point-search efficiency is claimed qualitatively

**Problem:** Point-cloud search is irregular and memory-intensive for robotics and 3D vision.

**Workload or benchmark:** Point-cloud nearest/range search; datasets, distance metric, and baselines are unspecified.

</details>

## What remains to establish

Resolve unspecified workloads, comparison methods, resource budgets, and source locations before generalizing a reported gain. Multiple papers in this selected sample permit comparison of mechanisms, but do not by themselves establish recurrence across years or a long-term trend.

[All subthemes](../expanded-taxonomy-v1.md) · [Research directions](../directions/README.md)
