## A usable biochip needs both the right shape and the right sequence

A microfluidic device moves small amounts of liquid through channels and chambers. A biochemical assay is a sequence of operations used to measure or test a sample. Designing such a device therefore requires more than drawing connected channels. The fabricated openings must have suitable dimensions. Liquids must also reach the intended locations at suitable times.

The two papers here address different parts of that problem. LiPCon changes a design before printing to reduce fabrication error. The valve-array paper chooses where operations occur and when they run, accounting for interference associated with pressure paths. These are not two implementations of the same experiment, and their outcomes cannot be ranked using one percentage.

## LiPCon: compensate the geometry before fabrication

Fabrication can change a feature's dimensions. The design supplied to the machine may then need to differ from the desired final shape. The correction must be tested on the manufactured object. A model that predicts an error accurately is useful. Prediction alone does not show that applying its correction produces the intended result.

[LiPCon](../observed-subthemes/biochips-and-specialized-systems.md#paper-dac-2026-research397) uses local geometry and weighted printing slices to predict a height correction. It uses a convolutional neural network, a model that learns spatial patterns. Section 3, PDF pages 2–4, describes this design correction, not illumination control during a biological assay.

Sections 4–5, pages 4–5, report 622 retained measurements from 1,037 raw points, augmented to 2,488. The stated training/validation/test counts total 2,476: twelve cases need reconciliation. The description does not establish whether all transformed copies and points from each chip stay in one split. Independence needs checking.

Section 5.2 and Table 4, pages 5–6, compare fabricated heights. Cases 1–6 use Anycubic Photon D2 and Miicraft BV-007a: proposed errors are 1.25–5.50%, versus 34.39–78.75% for the prior compensation method. Cases 7–9 use Elegoo Mars 4 and Anycubic Plant Based Resin + Clear without retraining: errors are 5.75–17.00%, versus 13.50–34.75%. Transfer helps these cases but does not preserve the original accuracy. [LiPCon manuscript, Sections 3–5 and Table 4](https://mediatum.ub.tum.de/doc/1846798/kj9r2ins2ujnez4dxlwcjehvo.DAC26_LPC_CamReady.pdf).

A height error percentage needs a denominator. Here it is the intended height, not the previous method's error. For example, reducing a 40% dimensional error to 4% means a 36-percentage-point change in dimensional error. It also means a 90% reduction relative to the old error. Neither statement means a 90% improvement in assay accuracy.

Removing damaged measurements can help isolate the mechanism being modeled. It also changes the population being evaluated. Accuracy on retained measurements cannot, by itself, establish the fraction of all manufacturing attempts that produce usable devices. A manufacturing assessment should separately count failures, define exclusions, and report variation across repeated prints.

<span id="explanation-dac-2026-research397"></span>

### LiPCon: a geometry correction model must survive the printer, resin and assay—not only the held-out measurements

#### What the physical problem is

A light-based 3D printer builds a microfluidic structure layer by layer. The intended geometry describes channel and opening dimensions. The cured material can differ from that geometry. Light penetrates through the resin and spreads beyond the intended region. It also interacts with exposure, layer thickness, material and printer settings. A height or width error can change fluid resistance, mixing, pressure response and whether an assay reaches the required state.

LiPCon uses local geometry and weighted printing slices as inputs to a convolutional neural network that predicts a height correction. The correction changes what is sent to the printer so that the fabricated feature is closer to the intended feature. This is a pre-fabrication geometry problem. It is not, by itself, a model of biological assay illumination. It is also not a proof that every corrected chip performs the intended biochemical protocol.

#### What the reported measurements establish

The recovered manuscript reports 1,037 raw points, 622 retained measurements and augmentation to 2,488 cases. The stated training, validation and test counts total 2,476, leaving twelve cases that need reconciliation. Augmentation and points from the same printed chip can also create dependence between splits. This happens if related examples appear in both training and test data. A test error is interpretable only after the unit of independence is clear: point, feature, print, chip, printer or material.

Sections 4–5 and Table 4 report fabricated-height comparisons. Cases 1–6 use Anycubic Photon D2 and Miicraft BV-007a. The proposed errors are 1.25–5.50% compared with 34.39–78.75% for the prior compensation method. Cases 7–9 use Elegoo Mars 4 and Anycubic Plant Based Resin + Clear without retraining. The proposed errors are 5.75–17.00% compared with 13.50–34.75%. These numbers support lower measured height error in the stated cases. They do not mean the same percentage improvement in assay accuracy, flow rate or manufacturing yield.

#### What must be validated next

The error denominator must remain visible: here it is intended height. Report failed prints and exclusions separately. Also report repeat prints, feature sizes, channel dimensions, resin batches, exposure settings, printer calibration, temperature, orientation and measurement uncertainty. Test a printer/material combination held out from training. Also test a new chip rather than only new points from a familiar chip.

Then run the fluidic and biochemical consequences. Measure pressure-flow behavior, leakage, channel connectivity, mixing, reaction timing, assay yield and repeatability. A geometry predictor can be accurate while a correction increases another dimension. The correction can also create roughness or introduce a defect that affects operation. The captured evidence supports the manuscript's page-backed height-error results and transfer cases. The count discrepancy, split independence, failed-print population, assay results and reproduction remain unresolved.

## Scheduling a valve array: timing depends on physical control

A schedule assigns start times and durations to operations. Placement assigns locations. These choices interact. An operation's location determines where its liquid must travel. The schedule determines which other operations may be active during that travel. A plan can satisfy the logical order of a protocol yet still rely on incompatible physical actions.

[Timing-Driven Scheduling and Placement Under Pressure-Path Interference](../observed-subthemes/biochips-and-specialized-systems.md#paper-dac-2026-research959) explicitly includes pressure-path interference in scheduling and placement for fully programmable valve arrays. The official description reports reductions in assay completion time, fluid-path length, and delay. It provides no numerical results, named comparison algorithms, pressure settings, assay list, or detailed validation method. It therefore supports the proposed design concern, but not a quantified performance or reliability conclusion. [Official DAC description](https://63dac.conference-program.com/presentation/?id=RESEARCH959&sess=sess121).

The missing interference model matters. To assess a schedule, a reader needs to know which simultaneous actions are forbidden and which merely slow one another. The reader also needs to know how the algorithm represents those effects. A shorter geometric route is not sufficient evidence of shorter completion time. Pressure availability or operation dependencies may require additional waiting.

The evaluation should also separate computation time—the time the design algorithm takes—from execution time—the time the resulting assay takes. A method may improve one while increasing the other. Biological correctness requires its own checks rather than being inferred from either runtime.

<span id="explanation-dac-2026-research959"></span>

### Pressure-path-aware valve scheduling: a legal operation order must also be physically executable

#### What scheduling and placement control

A programmable valve-array biochip routes liquids by opening and closing valves. An assay protocol specifies operations such as loading, moving, mixing, washing and reacting. It also specifies dependencies. An operation may start only after the required liquid is present and a previous step is complete. Placement assigns those operations or fluid sources to locations in the array. Scheduling assigns start times and durations.

These decisions are coupled. The location determines the path through which pressure moves liquid. The time determines which other valves are open along that path. Two operations that are independent in the protocol can still interfere. This happens if they share a pressure path, valve, channel or control resource. Interference may block an operation, change its flow rate or add a delay rather than simply make the schedule illegal.

#### What a pressure model must say

The scheduler needs a physical model that distinguishes forbidden simultaneous actions from actions that can run together with changed timing. It should state how pressure propagates and how valves and fluid resistance affect flow. It should also state how long transients last and how the model is calibrated. A geometric path length is only a proxy. A shorter path can still be slower if it needs waiting, has higher resistance or conflicts with another operation.

The schedule must preserve fluid identity and assay semantics. A plan can satisfy precedence constraints while causing cross-contamination, incomplete transfer or wrong mixing ratio. It can also cause insufficient reaction time or an unsafe valve state. The objective may combine completion time, path length, delay, valve use and resource constraints. A weighted score does not replace a pass/fail check for fluidic correctness and assay correctness.

#### What a complete evaluation needs

Define the assay protocols, valve array, fluids, pressure sources, timing limits, interference rules, placement space and baseline schedulers. Compare timing-oblivious scheduling and manual placement under the same protocol and hardware assumptions. Report algorithm runtime separately from assay completion time, fluid-path length, waiting time and pressure violations. Also report valve count, resource use, throughput, failed operations and successful assay outputs.

Validate the pressure model with measurements or a fluid simulator. Then test fabricated chips across pressure settings, fluid properties, manufacturing variation and valve faults. Also test concurrent operations and protocols not used to design the scheduler. The captured official description claims reductions in assay completion time, fluid-path length and delay. It reports no numerical results, named algorithms, pressure settings, assay list or validation method. The evidence supports pressure-aware scheduling and placement, not demonstrated fluidic reliability or a quantified performance gain.

## What connects these papers, and what remains unproved

The conceptual connection is that physical effects should enter design decisions before fabrication or execution. For printing, the relevant decision is the supplied geometry. For valve arrays, it is the joint choice of locations and times. This is an interpretation of the two mechanisms. It is not evidence that they share a compatible device platform or have been combined.

A future end-to-end study could ask whether measured fabrication variation changes operation timing enough to alter scheduling decisions. It would need a common device, measured geometry, calibrated timing assumptions, and repeated execution. It should report unsuccessful runs as well as successful ones. The present pair does not establish that result or a long-term cross-conference trend.

## Evidence status

The LiPCon manuscript was recovered and read on 2026-09-07; its page-backed conditions supersede missing-result statements in the historical card below. The dataset-count discrepancy and split independence remain unresolved, and the experiments were not reproduced. The valve-array manuscript remains missing. Clear prose and a working page do not remove these evidence gaps.
