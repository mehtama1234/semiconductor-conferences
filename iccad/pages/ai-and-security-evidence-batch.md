# ICCAD 2025: AI-assisted verification and hardware security batch

This page covers two ICCAD 2025 fallback papers with primary or author-hosted
preprint evidence. It is a technical batch, not a representation of the full 276
paper fallback corpus.

## HLSDebugger: turning HLS debugging into a learned verification task

HLSDebugger targets a practical gap between high-level synthesis productivity and
the difficulty of finding functional logic bugs. The work treats debugging as a
multi-task problem: identify the bug location, predict the bug type, and produce a
correction. Its artifact is not only a model but also a roughly 300K-sample labeled
dataset designed around HLS logic bugs.

The important subskills are therefore more specific than “LLMs for hardware”:

- generating or curating domain-specific bug data;
- representing HLS code and tool feedback;
- localizing functional defects rather than syntax errors;
- producing corrections that must be checked for functional validity;
- measuring identification and correction separately.

The paper reports gains over advanced general-purpose LLMs, but the evaluation
must be read together with the dataset-generation choices and the bug taxonomy.

## Energon: GPU telemetry as a transformer side channel

Energon studies a different security boundary: a user with access to power and
thermal telemetry on a shared or virtualized GPU. The work uses CNN predictors to
infer transformer family and architectural details such as layers and attention
heads, then uses the inferred architecture to construct substitute models and
transfer attacks.

This creates a detailed security chain:

`telemetry access → architectural inference → substitute model → transfer attack`

The paper’s contribution is not simply a new classifier. It connects hardware
telemetry leakage to model confidentiality and adversarial risk. The reported
results include high model-family identification accuracy, hyperparameter
classification, and transfer-attack success in both clean and noisy settings.

## Combined direction

Together these papers show two distinct uses of AI in CAD/security:

1. AI is embedded inside the design and verification workflow to find and repair
   defects.
2. AI is also used by an attacker to extract information from the hardware
   execution environment and attack deployed models.

That dual-use relationship is a meaningful ICCAD theme, but it should not be
collapsed into a generic “AI trend.” The relevant subthemes are domain-specific
verification automation, artifact/data construction, telemetry leakage, threat
models, and attack transferability.

## Limits

Both records are from the 2025 fallback because ICCAD 2026 paper data is not yet
available here. The full fallback corpus remains metadata-only, so these papers
cannot support conference-wide prevalence claims. The evidence and extracted
fields are preserved in `iccad/data/adjudicated-2025-batch.jsonl`.
