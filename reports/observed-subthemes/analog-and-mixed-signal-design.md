# Analog and mixed signal design

This subject has 2 records in the selected sample. This page explains where it fits, then presents all captured paper evidence without shortening the measurements or limitations.

[Definitions used in the paper records](../reading-guide-v1.md)

## Understand the parent subject first

- [Analog mixed signal and emerging devices](../themes/analog-mixed-signal-and-emerging-devices.md)

## Two different kinds of uncertainty

This group contains an oscillator-analysis method and an analog-to-digital converter test method. Both help characterize circuit behavior, but they answer different questions. The first computes sensitivity in a circuit model. The second selects measurements to estimate properties of a converter. A numerical solver's accuracy and a test procedure's measurement accuracy are not interchangeable.

An oscillator produces a repeating waveform. Its phase describes position within that repeating cycle. A disturbance can change the waveform's amplitude, shift when its next cycle occurs, or do both. An amplitude disturbance may decay while a timing shift remains. Phase-noise analysis studies the unwanted variation in that timing relationship.

An analog-to-digital converter, or ADC, maps a continuous input range to discrete output codes. Ideally, successive code transitions have the intended spacing. Real transitions depart from that pattern. Differential nonlinearity measures a code interval's width error relative to the ideal interval. Integral nonlinearity measures deviation from a chosen ideal transfer line, with the reference-line convention needing specification. Neither is the same as random sample noise.

## Floquet projection: separate the persistent response from slow decay

To analyze small disturbances around an oscillation, a solver can linearize the circuit around its periodic waveform. The resulting coefficients repeat over the cycle. Floquet analysis characterizes how disturbance components change from one cycle to the next. A component that decays slowly can remain numerically significant long after a faster component has disappeared.

[The Floquet-based subspace projection paper](../observed-subthemes/analog-and-mixed-signal-design.md#paper-dac-2026-research2838) targets computation of the perturbation projection vector, or PPV, used in oscillator phase-noise analysis. Its official description identifies slow-decaying modes as an obstacle to recovering the desired steady-state solution. It restricts the calculation to a smaller space containing the PPV and slow-decaying solutions, then uses a mathematical orthogonality condition to isolate the PPV through a small linear system. A subspace here means a restricted set of combinations of selected solution components.

The description claims numerical accuracy and efficiency improvements but supplies no circuit list, error values, timing results, or convergence thresholds. It therefore supports explaining the proposed separation, not a quantified speedup or universal convergence guarantee. [Official description, method paragraph](https://63dac.conference-program.com/presentation/?id=RESEARCH2838&sess=sess117).

An evaluation should include the cost of finding the periodic waveform and constructing the smaller space, not just solving its final equations. It should also check whether a close numerical PPV produces sufficiently accurate phase-noise predictions under the intended conditions. Small-disturbance analysis should not silently become a claim about arbitrary large disturbances.

## UGLMS-uSMILE: let measurements determine the next measurement

A fixed sweep measures a predetermined sequence of inputs. An adaptive test can instead update an error model after each measurement and choose where to measure next. The intended benefit is to spend effort where uncertainty remains. That benefit depends on whether the model's reported uncertainty reflects its actual errors.

[UGLMS-uSMILE](../observed-subthemes/analog-and-mixed-signal-design.md#paper-dac-2026-research3082) combines uncertainty-guided stimulus selection with segmented identification of linearity error. The indexed official description says it estimates errors at most-, intermediate-, and least-significant-bit levels during measurement, using covariance-based uncertainty. Covariance describes how estimated parameter errors vary together; it is not, by itself, proof of accurate estimates. [Official description](https://63dac.conference-program.com/presentation/?id=RESEARCH3082&sess=sess117).

The University of Stuttgart lists this as a seven-page DAC 2026 paper, separately from the authors' ICCAD 2025 work on live measurement sequencing for SAR ADC testing. That establishes an important identity boundary: results from the earlier paper must not be assigned to this combined method without checking the new manuscript. [University publication register](https://www.gs-imtr.uni-stuttgart.de/publications/).

A useful test comparison would fix converter resolution, input source quality, noise, settling requirements, and the reference measurement. Count stimulus changes, acquisition time, online computation, and any remaining reconstruction. Fewer samples do not necessarily mean a shorter test if changing and settling the stimulus dominates time.

Also inspect errors the segmented model cannot express. A confident fit within a restricted model can still miss a real defect. Test completion should therefore depend on independently checked accuracy or coverage, not only a small internal uncertainty estimate. These are proposed validation requirements; they are not reported results of the captured record.

<span id="explanation-dac-2026-research2838"></span>

## Floquet projection: reduce oscillator analysis without discarding the slow response

### The analysis starts from a periodic operating state

An oscillator is not at a fixed point. Its circuit state repeats after a period, so the nominal solution is a trajectory `x(t)` with `x(t+T) = x(t)`. To study a small disturbance, the circuit equations are linearized around that trajectory. The coefficients of the resulting linear system also repeat every period. This makes the problem different from ordinary small-signal analysis around a constant voltage or current.

The disturbance can contain components that decay at different rates. Fast components disappear after a few cycles; a slow component remains and can dominate the numerical error of an iterative solver. The phase direction is especially important because shifting an oscillator in time produces another point on the same periodic orbit. The phase perturbation projection vector, or PPV, extracts how a disturbance changes the oscillator's timing rather than only its instantaneous amplitude.

### The proposed reduction targets the slow subspace

The official description identifies slow-decaying modes as an obstacle to computing the PPV. Floquet analysis describes how perturbation components transform over one period. Floquet multipliers or related modal quantities indicate which components persist. A subspace projection then represents the perturbation using selected modes rather than the full circuit state.

The reported method restricts the computation to a space containing the PPV and the slow-decaying solutions, then uses an orthogonality condition to isolate the PPV through a smaller linear system. The computational idea is specific: preserve the directions that can still affect the desired phase response while avoiding repeated work on rapidly decaying directions. The description does not specify the exact basis construction, inner product, convergence test, or circuit equations, so those details are not inferred here.

### A smaller solve does not mean a free solve

The total cost includes finding the periodic orbit, identifying the relevant modes, constructing the reduced basis, projecting the equations, solving the reduced system, and checking the reconstructed PPV. If mode extraction or basis construction is expensive, reducing the final linear system may not reduce total runtime. The evaluation must therefore report preparation and repeated-use cost separately.

Accuracy also has two levels. The projected vector may be close to a reference PPV under a chosen numerical norm, while the resulting phase-noise prediction can still differ at the frequencies or disturbances that matter to the circuit. Small-disturbance linearization limits the claim to perturbations within its validity range; it does not establish behavior under arbitrary large disturbances or nonlinear startup transients.

### What the record establishes and what remains open

The accessible description establishes a PPV computation strategy that keeps the PPV and slow-decaying Floquet components in a smaller subspace and uses orthogonality to solve for the desired response. It does not provide circuit identities, mode counts, convergence thresholds, error values, runtime, phase-noise prediction accuracy, or fabricated measurement results. A stronger evaluation would report those conditions, compare full and projected solves, include basis-construction cost, test multiple oscillator topologies and operating points, and compare the final phase-noise output rather than only an intermediate vector.

[Official DAC description, record RESEARCH2838](https://63dac.conference-program.com/presentation/?id=RESEARCH2838&sess=sess117)

<span id="explanation-dac-2026-research3082"></span>

## UGLMS-uSMILE: adaptive ADC testing spends measurements where uncertainty matters

### An ADC's transfer curve is a set of transition decisions

An analog-to-digital converter maps an input voltage to a digital code. As the input changes, the output changes at code transitions. The width of one code interval determines local differential behavior. Differential nonlinearity, or DNL, measures how a transition interval differs from the ideal interval. Integral nonlinearity, or INL, measures how the accumulated transfer curve differs from a chosen reference line. The reference convention and code range are part of the measurement definition.

A test procedure estimates these errors by applying input stimuli and observing output codes. A fixed sweep spends measurements according to a predetermined grid. If some regions are already well characterized and others remain uncertain, an adaptive procedure can use earlier observations to select the next stimulus. That changes the measurement schedule; it does not automatically improve the converter itself.

### The method uses an uncertainty model to choose stimuli

UGLMS-uSMILE is described as combining uncertainty-guided stimulus selection with segmented identification of linearity error. The indexed description says it estimates error at most-significant-bit, intermediate-bit, and least-significant-bit levels while measuring, using covariance-based uncertainty. A segmented model represents different contributions separately so that the next measurement can target a parameter or code region whose estimate remains uncertain.

Covariance describes how estimation errors vary together. It can guide a selection rule, but a small modeled covariance is not proof that the model captures every physical error. Missing terms, source distortion, settling error, noise, reference drift, or an incorrect segmentation can make the estimate confidently wrong. The procedure therefore needs an independently checked transfer curve or reference measurement.

### Sample count is not the same as test time

An adaptive method may use fewer stimulus points and still take longer if each selected point requires a large input change, settling interval, acquisition window, or online update. The complete cost includes stimulus generation, switching, settling, conversion, code collection, covariance update, model evaluation, and final verification. The comparison must hold converter resolution, input-source quality, noise, settling requirement, and accepted error fixed.

The available source provides no sample count, acquisition time, DNL/INL error, resolution, stimulus conditions, runtime, or independent reference result. It therefore supports the mechanism and evaluation questions, not a numerical efficiency or accuracy claim. The University of Stuttgart publication register also lists an earlier ICCAD 2025 paper on live SAR-ADC measurement sequencing. That identity is useful context, but its results are not imported into UGLMS-uSMILE without the DAC manuscript.

### What the record establishes and what remains open

UGLMS-uSMILE establishes an adaptive testing direction: estimate segmented linearity behavior and use uncertainty to select subsequent ADC stimuli. It does not establish fewer total test resources, accurate uncertainty calibration, or better DNL/INL measurement than a fixed sweep. A stronger evaluation would report the adaptive policy, model terms, converter and instrument conditions, sample and wall-clock budgets, independent transfer-curve reference, error distributions, and comparison with the earlier or contemporaneous test methods under matched conditions.

[Official DAC description](https://63dac.conference-program.com/presentation/?id=RESEARCH3082&sess=sess117) · [University publication register](https://www.gs-imtr.uni-stuttgart.de/publications/)

## What is established and what still needs recovery

The common idea is selective effort: isolate the response needed by a numerical analysis, or select measurements that improve an estimate. The former depends on the validity of the circuit model and mathematical reduction; the latter also depends on instruments and the chosen error model. Their outcomes should remain separate.

The source check on 2026-09-07 recovered a fuller oscillator description and an indexed ADC description plus publication identity. Direct retrieval of the ADC presentation timed out, and neither full manuscript was recovered here. Consequently, there are no verified page-level numerical comparisons in this article yet. The older evidence cards below preserve their original capture; newly explained mechanisms above are attributed to the refreshed descriptions rather than presented as reproduced results.

## Compare the results carefully

First identify the inputs and required output quality. Then identify the limited resource: time, memory, communication, energy, circuit area, or correctness coverage. Ask which part of the method reduces that cost and which new cost it adds. Compare numbers only when the experiments hold these conditions sufficiently similar.

A conference description may explain the proposal while omitting the full experiment. An author preprint link may have been coded from its abstract. The source classification does not by itself establish that every table was read. Missing locations remain visible below.

## Complete captured evidence

These are evidence records, not substitutes for the explanations above. Each record preserves its problem, proposed method, measurements, comparison conditions, and source limits. A populated record does not establish that its mechanism has been fully explained or independently verified.

<span id="paper-dac-2026-research2838"></span>

### Floquet-Based Subspace Projection Method for Time-Domain PPV Computation

DAC 2026 · Record: `dac-2026-research2838`

[Read the step-by-step explanation](#explanation-dac-2026-research2838)

**Updated source-backed reading card**

Reviewed 2026-09-08. Deepens the refreshed official-description reading; explains periodic-orbit linearization, slow Floquet modes, PPV projection and the missing numerical conditions.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Slow-decaying perturbation modes make oscillator phase-noise PPV computation expensive or difficult to converge.

**Mechanism / artifact:**

Floquet-based subspace projection that retains the PPV and slow-decaying solutions, then isolates the PPV through an orthogonality condition and smaller linear system.

**Workload — the work tested:**

Oscillator phase-noise analysis; circuit topologies, periodic-waveform conditions, mode counts and reference solves are unspecified.

**Hardware and manufacturing assumptions:**

Numerical circuit-analysis models; solver, device/process, timestep and convergence assumptions are unspecified.

**Baseline — the comparison method:**

Full-space numerical PPV/Floquet solve

Other oscillator phase-noise analysis methods; identities unspecified

**Reported measurements:**

Numerical accuracy and efficiency improvements are claimed qualitatively; no circuit list, error, runtime, convergence threshold or phase-noise result is reported.

**Limits on the conclusion:**

The exact basis construction, inner product, mode-selection rule, convergence test and circuit equations are not exposed.

Reducing the final solve does not establish lower total cost if periodic-orbit, mode-extraction and projection preparation costs dominate.

Small-disturbance linearization and an intermediate PPV error do not establish arbitrary nonlinear transient or final phase-noise accuracy.

Refreshed official description only; full manuscript and independent reproduction were not performed.

**Source and location**

Evidence tier: Refreshed official DAC description; full manuscript and reproduction not performed. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH2838&sess=sess117)

DAC official description, method paragraph; record RESEARCH2838; no manuscript pages.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** full time-domain simulation

standard PPV solver

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH2838

**Hardware or process assumptions:** Analog simulation flow; device models and numerical integration assumptions are unspecified.

**Limits:** No numerical error, runtime, memory, convergence, or circuit results are reported.

Subspace assumptions may fail for nonlinear or multi-tone behavior.

Official description only; circuit-diverse validation is required.

**Method or artifact:** Floquet-based subspace projection for PPV computation.

**Metrics:** PPV computation efficiency is claimed qualitatively

**Problem:** Time-domain perturbation or phase-response computation can be expensive for oscillatory circuits.

**Workload or benchmark:** Oscillator or analog circuit models; circuits, tolerances, and reference solvers are unspecified.

</details>

<span id="paper-dac-2026-research3082"></span>

### UGLMS-uSMILE: Live Measurement Sequencing for Segmented Linearity Identification in ADCs

DAC 2026 · Record: `dac-2026-research3082`

[Read the step-by-step explanation](#explanation-dac-2026-research3082)

**Updated source-backed reading card**

Reviewed 2026-09-08. Deepens the refreshed indexed description; explains adaptive stimulus selection, segmented ADC linearity estimation and the difference between sample count and total test time.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

ADC linearity testing spends measurement effort over code transitions even when uncertainty is uneven across the transfer curve.

**Mechanism / artifact:**

Uncertainty-guided stimulus selection with segmented identification of ADC linearity error at most-, intermediate- and least-significant-bit levels using covariance-based uncertainty.

**Workload — the work tested:**

ADC linearity measurement; converter resolution, input source, noise, settling, stimulus count and reference measurement are unspecified.

**Hardware and manufacturing assumptions:**

ADC test instrumentation and converter under measurement; instrument accuracy, acquisition path, timing and device conditions are unspecified.

**Baseline — the comparison method:**

Fixed stimulus sweep

Earlier live SAR-ADC measurement-sequencing work is identity context, not imported quantitative evidence

**Reported measurements:**

Adaptive linearity-testing benefit is described qualitatively; no DNL/INL error, sample count, wall-clock time, resolution or uncertainty-calibration result is reported.

**Limits on the conclusion:**

Covariance is a model quantity and does not prove that unmodeled source, settling, noise, drift or segmentation errors are absent.

Fewer samples do not imply shorter testing when stimulus changes, settling, acquisition and online updates dominate.

Direct retrieval of the ADC presentation timed out and no full manuscript was recovered; the indexed description and publication identity do not provide page-level numerical comparisons.

**Source and location**

Evidence tier: Refreshed indexed description plus institutional identity source; full manuscript and reproduction not performed. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH3082&sess=sess117)

Indexed DAC official description and University of Stuttgart publication register; record RESEARCH3082; no manuscript pages.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** fixed measurement sweep

offline linearity fitting

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH3082

**Hardware or process assumptions:** Mixed-signal test setup and ADC; sampling and calibration assumptions are unspecified.

**Limits:** No INL/DNL error, measurement count, time, noise, or silicon results are reported.

Sequencing may depend on ADC architecture.

Official description only; instrumented validation is required.

**Method or artifact:** Live adaptive measurement sequencing for segmented linearity identification.

**Metrics:** Measurement efficiency is claimed qualitatively

**Problem:** ADC linearity characterization can require many measurements and may be affected by changing conditions.

**Workload or benchmark:** ADC measurements; resolution, segments, test equipment, and noise are unspecified.

</details>

## What remains to establish

Resolve unspecified workloads, comparison methods, resource budgets, and source locations before generalizing a reported gain. Multiple papers in this selected sample permit comparison of mechanisms, but do not by themselves establish recurrence across years or a long-term trend.

[All subthemes](../expanded-taxonomy-v1.md) · [Research directions](../directions/README.md)
