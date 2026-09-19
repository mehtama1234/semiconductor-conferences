# Reproducibility artifacts and benchmarks

This subject has 1 record in the selected sample. This page explains where it fits, then presents all captured paper evidence without shortening the measurements or limitations.

[Definitions used in the paper records](../reading-guide-v1.md)

## Understand the parent subject first

- [Design methodology and tooling](../themes/design-methodology-and-tooling.md)

## A benchmark specifies the question as well as the data

A research artifact can include input data, code, models, configuration files, and expected outputs. A benchmark additionally defines how those materials are used to compare methods. Without a fixed task and evaluation procedure, two researchers can use the same files and still measure different things.

The single selected record is [CapBench](../observed-subthemes/reproducibility-artifacts-and-benchmarks.md#paper-dac-2026-research1224), a dataset for learning post-layout capacitance extraction. Capacitance describes electrical charge response to voltage and depends on conductor geometry and surrounding materials. A predictor needs examples pairing geometry with reference values. The validity of that pairing and the independence of the evaluation set are central to the benchmark's value.

## What CapBench contains according to the source

The official description reports 61,855 three-dimensional windows from 14 OpenROAD runs across ASAP7, NanGate45, and Sky130HD. A window is a selected local region of the physical design. The runs cover single-core processors, systems-on-chip, and media accelerators, with windows in three size tiers.

The named process design kits supply technology-specific information used by the layout and extraction flows. Including several kits creates an opportunity to study transfer between technologies. It does not automatically establish such transfer: a model can train and test on examples from every kit without ever facing an unseen technology.

The description also identifies several representations and ten evaluated model architectures, including convolutional networks, point-cloud transformers, and graph neural networks. Those families organize geometry differently. Their comparison is useful only if input information, reference targets, training resources, and test conditions are sufficiently aligned to make the intended claim.

## Reference-label error and predictor error are separate

CapBench uses RWCap labels and reports validation against Raphael with 0.64% total-capacitance mean absolute error. This is a comparison between reference-generation methods under the source's conditions. It is not the same measurement as a learned model's error against those labels, and agreement between solvers is not direct measurement on fabricated silicon.

The official description reports 1.75% error for convolutional networks and 10.2% error for graph neural networks, alongside up to 41.4-fold speedup for the latter. The speedup and error belong together. Reporting only the acceleration would conceal the accompanying accuracy result. The source does not provide enough detail to identify an equivalent-accuracy winner or a complete runtime comparison.

Mean error also needs its denominator, aggregation convention, and distribution. It can conceal a small number of large errors or systematic differences between technologies and geometry sizes. Those cases can matter if a downstream design decision depends on a particular capacitance rather than an average across windows.

## Windows from the same design are not necessarily independent

Local windows may overlap or share recurring structures. Randomly splitting windows from the same layout can leave closely related examples on both sides of the evaluation. That can be appropriate for one stated task, but is weaker evidence for a new-design claim than withholding whole designs or runs.

A benchmark should therefore distinguish within-design prediction, unseen-design prediction, and unseen-technology prediction. Its split manifest should make those boundaries inspectable. The captured description does not expose leakage controls, per-technology results, or the full split procedure, so those generalization claims remain unestablished.

## What another researcher needs to reproduce the comparison

The required package includes identifiable design inputs, tool versions and settings, window-construction rules, label-generation settings, fixed splits, model configurations, training seeds, and executable scoring. Licenses and access conditions matter because a nominally described flow may depend on tools or data another group cannot obtain.

Runtime reproduction additionally needs hardware, batching, preprocessing, and the timing boundary. Training and dataset-construction costs should remain separate from prediction time but should not disappear from an end-to-end assessment. The official description leaves absolute runtimes, licensing details, and implementation availability unspecified.

CapBench provides a concrete multi-technology benchmark proposal and reported comparisons, not evidence that this atlas has reproduced them. Its longer-term research value would be demonstrated by independent reruns and clearly separated transfer tests, followed by checking how prediction errors affect electrical analysis. A larger dataset is useful material for those studies; its size alone does not establish reproducibility or a reliable replacement for reference extraction.

<span id="explanation-dac-2026-research1224"></span>

### CapBench: a capacitance dataset is useful only when labels, geometry, splits and solver conditions are independently inspectable

#### What the prediction task is

Post-layout capacitance is an electrical property of a completed physical geometry. Conductors, nearby conductors, dielectric materials, layer shapes and the local three-dimensional environment determine how charge responds when voltage changes. An ML dataset for post-layout capacitance extraction must therefore pair a precisely defined geometry window with a reference capacitance and preserve the technology and extraction conditions that produced the label.

The prediction target also needs a clear scope. It may be total capacitance, coupling capacitance, self-capacitance or several components. A model error is meaningful only when the target definition, units, aggregation and reference solver are fixed. A label produced by one extractor is not identical to measured silicon, and agreement between two extractors measures their disagreement under stated conditions rather than proving physical truth.

#### What the reported CapBench material contains

The recorded description reports 61,855 three-dimensional windows from 14 OpenROAD runs across ASAP7, NanGate45 and Sky130HD. The designs include single-core processors, systems-on-chip and media accelerators, and the windows are grouped into three size tiers. It also identifies ten evaluated model architectures, including convolutional networks, point-cloud transformers and graph neural networks.

These details establish a concrete dataset scope. They do not by themselves establish that the examples are independent, that each technology is held out in a transfer test, or that the representations receive equivalent information. A graph model and a convolutional model can be given different geometric context, preprocessing and parameter budgets. The comparison must describe those conditions before an accuracy or speed ranking is meaningful.

#### Reference error and learned prediction error are different quantities

The source reports 0.64% total-capacitance mean absolute error when RWCap is checked against Raphael under its conditions. That number describes reference-label error between reference-generation tools. It does not describe learned prediction error from the ML model against those labels, and it does not establish agreement with fabricated hardware.

The source also reports 1.75% error for convolutional networks and 10.2% error for graph neural networks, alongside up to 41.4-fold GNN speedup. The speed and error must be read together. A faster model with larger error may be useful for a screening stage, but it cannot be called equivalent to a slower model without an accuracy-at-equal-cost analysis and a definition of the downstream tolerance.

Mean absolute error requires its denominator and aggregation rule. Pooling all windows can let a technology or design family with many windows dominate the result. A mean can also hide rare large errors, systematic errors near dense wiring, or errors concentrated in one window size. Per-node, per-design, per-size and per-technology distributions are needed for transfer and engineering-use claims.

#### Why the split determines the claim

Windows from one layout can overlap or repeat local structures. If they are randomly divided, nearly identical geometry can appear in training and test sets. That split can measure interpolation within known designs, but it is weaker evidence for a new design or an unseen process. CapBench should distinguish at least within-design, unseen-design and unseen-technology evaluation, with a split manifest that identifies which runs and technologies belong to each split.

#### What reproduction requires

A reproducible rerun needs the exact OpenROAD designs and commits, PDK versions, extraction settings, window-construction rules, coordinate conventions, label-generation commands, RWCap and Raphael versions, train/validation/test manifest, preprocessing, model configurations, seeds, hardware and scoring code. It also needs licensing and access information for any proprietary tool or design.

Runtime must state the boundary being measured. Dataset construction, label generation, preprocessing, training and inference are different costs. A prediction speedup does not automatically imply an end-to-end speedup if data preparation or reference-label generation dominates. The final test should also measure whether capacitance error changes timing, signal integrity or another electrical decision.

The captured official description supports CapBench as a multi-PDK dataset proposal with reported model comparisons. It does not expose leakage controls, per-technology error distributions, absolute runtimes, license details or model implementation, and this atlas has not reproduced the reported experiments. The evidence supports a concrete benchmark artifact, not independently established transfer generalization, reproducibility or replacement of high-fidelity extraction. [Recorded evidence](../observed-subthemes/reproducibility-artifacts-and-benchmarks.md#paper-dac-2026-research1224)

## Compare the results carefully

First identify the inputs and required output quality. Then identify the limited resource: time, memory, communication, energy, circuit area, or correctness coverage. Ask which part of the method reduces that cost and which new cost it adds. Compare numbers only when the experiments hold these conditions sufficiently similar.

A conference description may explain the proposal while omitting the full experiment. An author preprint link may have been coded from its abstract. The source classification does not by itself establish that every table was read. Missing locations remain visible below.

## Complete captured evidence

These are evidence records, not substitutes for the explanations above. Each record preserves its problem, proposed method, measurements, comparison conditions, and source limits. A populated record does not establish that its mechanism has been fully explained or independently verified.

<span id="paper-dac-2026-research1224"></span>

### Capbench: A Multi-PDK Dataset for Machine-Learning-Based Post-Layout Capacitance Extraction

DAC 2026 · Record: `dac-2026-research1224`

[Read the step-by-step explanation](#explanation-dac-2026-research1224)

**Updated source-backed reading card**

Reviewed 2026-09-08. Deepens the existing CapBench benchmark treatment into a paper-level reading; separates capacitance target definition, reference-label error, learned prediction error, split leakage, transfer claims and reproduction requirements.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Post-layout capacitance extraction requires expensive high-fidelity solvers, while ML models need reproducible multi-technology data for transfer and scalability studies.

**Mechanism / artifact:**

Multi-PDK, multi-representation dataset built from placed-and-routed open-source designs, with random-walk labels, industry-tool validation and CNN, point-cloud transformer and GNN evaluations; split manifest, implementation and exact extraction conditions are not exposed in the captured description.

**Workload — the work tested:**

61,855 three-dimensional windows from 14 OpenROAD runs across ASAP7, NanGate45 and Sky130HD, covering single-core CPUs, SoCs and media accelerators in three size tiers; window overlap, design/run splits and per-node denominators are unspecified.

**Hardware and manufacturing assumptions:**

Three named technology nodes and OpenROAD physical-design flows with RWCap and Raphael extraction conditions; PDK versions, tool commits, geometry conventions, licenses, hardware and transfer conditions are unspecified.

**Baseline — the comparison method:**

RWCap random-walk solver

Raphael industry-standard solver

CNN, point-cloud transformer and GNN architectures

Input representations, target definitions, preprocessing, training resources, splits and runtime boundary are not fully specified

**Reported measurements:**

Reported values include 0.64% total-capacitance MAE for RWCap versus Raphael, 1.75% CNN error, up to 41.4x GNN speedup and 10.2% GNN error; no per-technology distributions, absolute runtimes, leakage controls or reproduced results are available.

**Limits on the conclusion:**

RWCap-versus-Raphael error is reference-label disagreement, not learned-model error or silicon validation. CNN/GNN error must be interpreted with the stated target, denominator, units and aggregation rule.

Windows from the same design can overlap or share structures. Random window splits can leak layout-specific patterns and do not establish unseen-design or unseen-technology transfer; split manifests and per-node results are required.

The official description does not expose leakage controls, per-node error distributions, absolute runtimes, license details or model implementation, and this atlas has not reproduced the experiments. The artifact supports a benchmark proposal, not independently established transfer generalization, reproducibility or replacement of high-fidelity extraction.

**Source and location**

Evidence tier: Primary captured official DAC description plus existing chapter level capbench evidence discussion; no independently rerun benchmark, full implementation or page level table verification. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH1224&sess=sess167)

DAC 2026 official description; captured Problem, Mechanism / artifact, Workload, Hardware, Baseline, Measurements and Limits fields; record RESEARCH1224; exact page/section/table locator not recorded.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** RWCap random-walk solver

Raphael industry-standard solver

CNN, point-cloud transformer, and GNN architectures

**Evidence locators:** Not established in the captured evidence.

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH1224&sess=sess167

**Hardware or process assumptions:** Three named technology nodes and OpenROAD physical-design flows; RWCap and Raphael extraction conditions, window construction, and transfer splits require detailed dataset documentation.

**Limits:** The description does not expose train/test leakage controls, per-node error distributions, absolute runtimes, license details, or model implementation; the dataset supports reproducibility claims but not automatic transfer generalization.

**Method or artifact:** Multi-PDK, multi-representation dataset built from placed-and-routed open-source designs, with high-fidelity random-walk labels, industry-tool validation, and benchmark evaluations across CNN, point-cloud transformer, and GNN models.

**Metrics:** 0.64% total-capacitance MAE for RWCap versus Raphael validation

1.75% CNN error

up to 41.4x GNN speedup

10.2% GNN error

**Problem:** Post-layout capacitance extraction requires expensive high-fidelity solvers, while ML models need reproducible multi-technology data for transfer and scalability studies.

**Workload or benchmark:** Single-core CPUs, SoCs, and media accelerators; 14 OpenROAD runs across ASAP7, NanGate45, and Sky130HD; 61,855 3D windows in three size tiers.

</details>

## What remains to establish

Resolve unspecified workloads, comparison methods, resource budgets, and source locations before generalizing a reported gain. This subject is represented by one paper and supports a case study, not evidence of recurrence or a long-term trend.

[All subthemes](../expanded-taxonomy-v1.md) · [Research directions](../directions/README.md)
