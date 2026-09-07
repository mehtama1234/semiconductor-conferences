#!/usr/bin/env python3
"""Build a dated manifest for the reproducible intelligence package."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


COMMANDS = [
    "PYTHONPATH=.:src python3 scripts/build_evidence_summary.py",
    "PYTHONPATH=.:src python3 scripts/build_taxonomy_v1.py",
    "PYTHONPATH=.:src python3 scripts/audit_adjudications.py",
    "PYTHONPATH=.:src python3 scripts/build_work_queue.py",
    "PYTHONPATH=.:src python3 scripts/build_review_packets.py",
    "PYTHONPATH=.:src python3 scripts/build_review_assignments.py",
    "PYTHONPATH=.:src python3 scripts/build_draft_review_packets.py",
    "PYTHONPATH=.:src python3 scripts/build_title_shift_candidates.py",
    "PYTHONPATH=.:src python3 scripts/validate_project.py",
    "PYTHONPATH=.:src pytest -q",
]

ARTIFACTS = [
    "GOAL.md",
    "data/conference-register.json",
    "data/taxonomy-v1-evidence.json",
    "data/research-work-queue.jsonl",
    "reports/evidence-summary-v1.json",
    "reports/research-work-queue-summary.json",
    "reports/review-packet-coverage.json",
    "reports/adversarial-preflight-v0.json",
    "reports/temporal-insufficiency-v1.json",
    "reports/title-shift-candidates-v1.json",
    "reports/collection-status.md",
    "reports/field-directions-and-hypotheses-v1.md",
    "reports/technology-direction-synthesis-v1.md",
    "data/theme-evidence-matrix-v1.json",
    "reports/theme-evidence-matrix-v1.md",
    "scripts/build_theme_evidence_matrix.py",
    "reports/execution-plan.md",
    "reports/adversarial-judge-protocol-v1.md",
    "reports/adversarial-review-status-v1.md",
    "reports/draft-review-packets-v1.md",
    "reports/historical-description-coding-v1.md",
    "reports/temporal-mechanism-comparison-v1.md",
    "reports/completion-audit-v1.json",
    "reports/independent-review-handoff-v1.md",
    "reports/review-remediation-queue-v1.md",
    "reports/package-release-v1.md",
    "reports/evidence-gap-register-v1.md",
    "reports/condition-extraction-queue-v1.md",
    "reports/release-readiness-v1.md",
    "reports/independent-review-response-template-v1.json",
    "reports/independent-review-assignments-v1.json",
    "scripts/validate_project.py",
    "tests/test_work_queue.py",
    "tests/test_review_packets.py",
    "isca/data/busybarn-artifact-primary-recovery-v1.json",
    "isca/data/rearchitecting-primary-recovery-v1.json",
    "isca/data/capa-artifact-reproduction-v1.json",
    "reports/isca-recovery-batch-2-2026-09-07.md",
    "reports/p2-recovery-batch-9-2026-09-07.md",
    "reports/p2-recovery-batch-10-2026-09-07.md",
    "reports/p2-recovery-batch-11-2026-09-07.md",
    "reports/isca-primary-recovery-batch-3-2026-09-07.md",
    "reports/isca-primary-recovery-batch-4-2026-09-07.md",
    "reports/condition-extraction-triage-2026-09-07.md",
    "reports/condition-extraction-isca-recovery-batch-4-2026-09-07.md",
    "isca/data/source-recovery-attempts.jsonl",
    "iccad/data/source-recovery-attempts.jsonl",
    "iccad/data/nimch-thesis-primary-recovery-v1.json",
]


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def build(root: Path) -> dict:
    generated_paths = set(ARTIFACTS)
    generated_paths.update(str(path.relative_to(root)) for path in root.glob("*/data/papers-*program.jsonl"))
    generated_paths.update(str(path.relative_to(root)) for path in root.glob("*/data/sources.jsonl"))
    generated_paths.update(str(path.relative_to(root)) for path in root.glob("*/data/adjudicated-*.jsonl"))
    artifacts = []
    for relative in sorted(generated_paths):
        path = root / relative
        artifacts.append({"path": relative, "sha256": digest(path), "bytes": path.stat().st_size})
    return {
        "schema": "reproducibility-manifest.v1",
        "as_of": "2026-09-07",
        "status": "dated_package_checkpoint",
        "commands": COMMANDS,
        "artifact_hashes": artifacts,
        "source_policy": "Permitted metadata, abstracts, descriptions and author/company sources are retained with evidence tiers; access restrictions are not bypassed.",
        "interpretation_gates": [
            "Selected coding is not venue-wide prevalence.",
            "Deterministic preflight is not independent review.",
            "Temporal title shifts and six pilot pairs do not establish rising or declining trends.",
            "Missing source text is recorded as a gap, not treated as negative evidence.",
        ],
        "raw_data_policy": "Raw downloaded captures may be ignored by repository policy; tracked ledgers preserve URLs, dates, status and hashes where permitted.",
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    output = args.root / "reports/reproducibility-manifest-v1.json"
    manifest = build(args.root)
    output.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"path": str(output), "artifact_count": len(manifest["artifact_hashes"])}, indent=2))
