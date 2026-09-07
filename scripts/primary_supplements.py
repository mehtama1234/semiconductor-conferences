"""Join researcher assessments without treating them as original source text."""
from __future__ import annotations

import hashlib
import json
from collections import defaultdict
from pathlib import Path

from scripts.build_evidence_summary import read_jsonl
from scripts.collect_isca_crossref_metadata import title_key

SCHEMAS = {"supplementary-primary-assessment.v1", "supplementary-primary-conditions.v1",
           "primary-source-recovery-assessment.v1", "source-recovery-assessment.v1"}


def validate(assessment: dict, paper: dict, source: dict) -> None:
    if (assessment.get("paper_id") != paper.get("paper_id") or
            not assessment.get("title") or
            title_key(assessment["title"]) != title_key(paper.get("title", ""))):
        raise ValueError("Supplement inventory identity mismatch")
    if (not source or assessment.get("source_id") != source.get("source_id") or
            assessment.get("source_url") != source.get("url")):
        raise ValueError("Supplement source registration mismatch")
    if (assessment.get("independent_review_status") != "pending" or
            not assessment.get("capture_date") or not assessment.get("extraction_scope")):
        raise ValueError("Supplement evidence/review boundary violated")


def load(root: Path) -> dict[str, list[dict]]:
    inventory = {r["paper_id"]: r for p in sorted(root.glob("*/data/papers-20??-program.jsonl")) for r in read_jsonl(p)}
    supplements = defaultdict(list)
    paths = set(root.glob("*/data/*primary*.json")) | set(root.glob("*/data/*source-recovery*.json"))
    for path in sorted(paths):
        raw = path.read_bytes()
        assessment = json.loads(raw)
        if assessment.get("schema") not in SCHEMAS:
            continue
        registry = {r["source_id"]: r for r in read_jsonl(path.parent / "sources.jsonl")}
        validate(assessment, inventory.get(assessment.get("paper_id"), {}),
                 registry.get(assessment.get("source_id"), {}))
        supplements[assessment["paper_id"]].append({
            "path": str(path.relative_to(root)),
            "sha256": hashlib.sha256(raw).hexdigest(),
            "source_url": assessment["source_url"],
            "content_role": "researcher_assessment_not_original_source",
            "independent_review_status": "pending",
            "headline_metric_status": assessment.get("headline_metric_status", "not_adjudicated"),
            "assessment": assessment,
        })
    return dict(supplements)


REVIEW_ACTION = "Inspect supplementary assessments and their original sources; resolve discrepancies without using researcher interpretation to verify itself"
