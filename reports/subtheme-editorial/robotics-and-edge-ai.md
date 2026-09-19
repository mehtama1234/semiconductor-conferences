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
