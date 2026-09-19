## Identifying a manufacturing route is not the same as measuring yield

The single record in this group concerns whether wafers were produced using an approved sequence of manufacturing tools. That is a process-origin question. A wafer can meet electrical requirements yet have an unapproved production history; an approved production route can also produce a defective wafer. Approval and product quality must therefore remain separate outputs.

The existing taxonomy places this record under manufacturing monitoring and yield, but one paper does not establish a broad yield-improvement result. Its specific contribution belongs to tool-chain attestation: evidence supporting a claim about which manufacturing route was used.

## What STAMP observes

[STAMP](../observed-subthemes/manufacturing-monitoring-and-yield.md#paper-dac-2026-research3145) uses measurements of physical dimensions and electrical characteristics to distinguish sanctioned from unsanctioned tool chains. The captured official description reports a demonstration using 7,000 wafers, multiple tool-chain variants, and GlobalFoundries 12LP FinFET manufacturing.

Inline measurements are taken during production. Electrical tests measure selected device or circuit properties. A monitoring model can use systematic differences in these observations as evidence about process history. The description refers to relationships between tool exchanges and the resulting silicon characteristics, but does not identify the measurement features, sampling schedule, or experimental controls in enough detail to verify a causal interpretation.

The wafer count describes the size of the demonstration. It is not a classification-accuracy result, and it does not state how many independently varied tools, production periods, or manufacturing routes were tested. The captured source supplies no false-accept or false-reject rates.

## Two errors have different operational consequences

A false acceptance occurs when an unapproved route is classified as approved. A false rejection occurs when an approved route is classified as unapproved. The former weakens the origin claim; the latter may trigger unnecessary investigation or interrupt production. Overall accuracy can hide either problem when the two categories have very different frequencies.

An operational evaluation should therefore report both errors under specified class frequencies and decision thresholds. It should also distinguish a model declining to decide from confidently accepting a route. These are requirements for interpreting deployment value, not capabilities established by the available description.

## Separating route information from production drift

If one route was used earlier and another later, a classifier might learn a time-related change rather than the tool substitution of interest. Likewise, wafers processed together can share conditions that make random train/test splits easier than predicting a later production batch. Testing on held-out production periods and controlled route changes would provide stronger evidence about what the model has learned.

Normal process drift also matters after deployment. A changed measurement distribution could indicate an unapproved tool change, an approved maintenance event, or another process change. A classification result needs an investigation procedure and contextual records before it becomes an operational conclusion. The source leaves temporal holdouts, drift behavior, and transfer to other factories or technologies unspecified.

## Measurement-based evidence needs trustworthy measurements

The attestation claim also depends on how observations are collected and associated with wafers. If measurement provenance or wafer identity is unreliable, a good classifier cannot repair that missing link by itself. The captured description does not specify chain-of-custody controls or an adversarial threat model, so resistance to manipulated measurements must remain unestablished.

The longer-term research question is whether process measurements can supplement manufacturing records with independently useful origin evidence. Answering it requires controlled substitutions, trustworthy data collection, temporal evaluation, and explicit error costs. STAMP's reported industrial-scale dataset makes that question concrete, but the available official description does not establish a general manufacturing-security guarantee or improved yield.

<span id="explanation-dac-2026-research3145"></span>

### STAMP: wafer measurements can support tool-chain attestation only when process history is separated from ordinary manufacturing variation

#### What attestation is trying to establish

Manufacturing attestation is a claim about origin or process history: a specified sequence of tools, recipes, and process steps produced a wafer or device. This is different from a yield claim. Yield asks how many manufactured units meet electrical or physical specifications. Attestation asks whether the units came through an approved route. An approved route can produce defective wafers, and an unapproved route can sometimes produce wafers that pass ordinary acceptance tests.

STAMP is described as a machine-learning process-monitoring model that uses wafer-level metrology and wafer-acceptance-test measurements to distinguish sanctioned from unsanctioned semiconductor tool chains. The model is inferring a hidden process-history label from physical observations. The security value depends on whether the observed differences are caused by the tool-chain change, rather than by time, lot, operator, wafer position, maintenance, recipe drift, measurement equipment or another correlated factor.

#### Classify the measurements and labels

Inline metrology measures physical properties during production. Electrical testing measures selected device or circuit behavior after some process steps. Each measurement has a location, time, instrument, calibration state, wafer coordinate and association with a lot or process history. A model needs reliable labels linking those observations to the actual tool chain used.

The evaluation should list the measured dimensions and electrical features, sampling cadence, wafer regions, measurement noise, missing values, instrument calibration, normalization, and the exact label assigned to each wafer. It should state which tool exchange is controlled, which tools remain fixed, and whether the changed tool affects a physical step that can plausibly leave the measured signature. A classifier can separate two datasets without proving that it has learned the intended process cause.

#### False acceptance and false rejection have different costs

False acceptance means an unapproved tool chain is accepted as sanctioned. That weakens the attestation boundary. False rejection means an approved wafer or route is rejected as unsanctioned. That can trigger investigation, delay shipment, or interrupt production. The two rates must be reported separately by route, lot, production period, and decision threshold.

The system may also abstain when evidence is ambiguous. Abstention is different from acceptance and rejection and may be operationally valuable if suspicious wafers receive additional testing. Report the confusion matrix, class frequencies, calibration, confidence intervals, threshold selection procedure, and cost-weighted operating points. The number 7,000 describes the demonstration population; it is not a classification accuracy or a guarantee that 7,000 independent process substitutions were observed.

#### Prevent the model from learning the wrong cause

Randomly splitting wafers can leak information. Wafers from the same lot or production period may share conditions, and near-duplicate measurements can appear in training and test sets. A stronger evaluation uses held-out complete lots, production periods, tool instances, maintenance events, and, where possible, factories. It should test a controlled tool substitution while keeping time and other process variables balanced.

Process drift after deployment can change the measurement distribution. A model might label an approved maintenance change as an unauthorized tool exchange, or fail to detect a new unsanctioned route because it has not seen that type of variation. Use temporal monitoring, drift alarms, recalibration rules, and an investigation path. Report performance before and after recalibration rather than silently retraining on future labels.

#### Chain of custody is part of the security claim

Wafer-level measurements are useful only if the association between a wafer, its process records, its measurement files, and its label is trustworthy. This chain of custody is part of the security boundary. An attacker or accidental data error could replace a measurement, alter a label, replay a prior wafer’s record, or disconnect the sample from its production history. Machine learning cannot repair an untrusted measurement-to-wafer link.

The operational design should define signed or access-controlled records, time synchronization, instrument identity, calibration history, sample identity, audit logs, retention, replay detection and the response to missing or conflicting records. It should state whether the adversary can alter tool logs, measurement data, model files, thresholds or the wafer itself. Without that boundary, the result is process classification, not a complete supply-chain attestation system.

#### Generalization and deployment evidence

The captured description identifies GlobalFoundries 12LP FinFET manufacturing, multiple tool-chain variants, inline measurements and electrical tests, and a 7,000-wafer demonstration. That is meaningful industrial scale, but it remains one foundry, node and measurement environment unless other settings are shown. A cross-fab transfer to another fab, node, tool family, recipe, instrument or product requires new evidence.

The baselines should include ordinary process monitoring, a classifier using only time or lot metadata, and sanctioned-versus-unsanctioned classification with matched class balance and temporal splits. Report accuracy only alongside false acceptance, false rejection, abstention, drift, calibration, inference latency, labeling cost and investigation workload. The evidence supports a concrete wafer-level tool-chain attestation direction, not a general manufacturing-security guarantee or improved yield result.
