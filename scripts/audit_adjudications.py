#!/usr/bin/env python3
"""Run adversarial consistency preflight checks over adjudicated records.

This is a deterministic preflight, not a claim that an LLM or human has completed
adjudication. It is intentionally hostile to unsupported labels, missing fields,
weak provenance, and evidence spans that share little vocabulary with the captured
description.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

from scripts.build_review_packets import source_matches, captured_sources


STOP = {"the", "and", "for", "with", "from", "that", "this", "into", "over", "than", "using", "via", "are", "its"}


def tokens(value: str) -> set[str]:
    return {token for token in re.findall(r"[a-z0-9]{3,}", value.lower()) if token not in STOP}


def read(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def audit(root: Path) -> dict:
    taxonomy = json.loads((root / "data/taxonomy-v1-evidence.json").read_text(encoding="utf-8"))
    valid_sub = {theme["theme_id"]: set(theme["subthemes"]) for theme in taxonomy["themes"]}
    valid_subsub = {(theme["theme_id"], sub): set(values) for theme in taxonomy["themes"] for sub, values in theme.get("subsubthemes", {}).items()}
    evidence = captured_sources(root)
    records = read(root / "dac/data/adjudicated-2025-batch.jsonl") + read(root / "dac/data/adjudicated-2026-batch.jsonl") + read(root / "dac/data/adjudicated-2026-batch-2.jsonl") + read(root / "dac/data/adjudicated-2026-batch-3.jsonl") + read(root / "dac/data/adjudicated-2026-batch-4.jsonl") + read(root / "iccad/data/adjudicated-2025-batch.jsonl") + read(root / "iccad/data/adjudicated-2025-batch-2.jsonl") + read(root / "isca/data/adjudicated-2026-batch.jsonl") + read(root / "isca/data/adjudicated-2026-batch-2.jsonl") + read(root / "isca/data/adjudicated-2026-batch-3.jsonl") + read(root / "isca/data/adjudicated-2026-batch-4.jsonl") + read(root / "isca/data/adjudicated-2026-batch-5.jsonl") + read(root / "isca/data/adjudicated-2026-batch-6.jsonl") + read(root / "isca/data/adjudicated-2026-batch-7.jsonl") + read(root / "isca/data/adjudicated-2026-batch-8.jsonl")
    records += read(root / "dac/data/adjudicated-2026-batch-5.jsonl")
    records += read(root / "dac/data/adjudicated-2026-batch-6.jsonl")
    records += read(root / "dac/data/adjudicated-2026-batch-7.jsonl")
    records += read(root / "dac/data/adjudicated-2026-batch-8.jsonl")
    records += read(root / "dac/data/adjudicated-2026-batch-9.jsonl")
    records += read(root / "isca/data/adjudicated-2026-batch-9.jsonl")
    records += read(root / "iccad/data/adjudicated-2025-batch-3.jsonl")
    records += read(root / "iccad/data/adjudicated-2025-batch-4.jsonl")
    records += read(root / "iccad/data/adjudicated-2025-batch-5.jsonl")
    records += read(root / "iccad/data/adjudicated-2025-batch-6.jsonl")
    records += read(root / "iccad/data/adjudicated-2025-batch-7.jsonl")
    records += read(root / "iccad/data/adjudicated-2025-batch-8.jsonl")
    records += read(root / "iccad/data/adjudicated-2025-batch-9.jsonl")
    records += read(root / "iccad/data/adjudicated-2025-batch-10.jsonl")
    records += read(root / "iccad/data/adjudicated-2025-batch-11.jsonl")
    checks = []
    for record in records:
        source = evidence.get(record["paper_id"])
        source_text = source.get("description", "") if source and source_matches(record, source) else ""
        overlap = len(tokens(record["evidence_span"]) & tokens(source_text)) / max(1, len(tokens(record["evidence_span"]))) if source_text else None
        theme_ok = record["theme_id"] in valid_sub and record["subtheme_id"] in valid_sub[record["theme_id"]]
        subsub_ok = record["subsubtheme_id"] in valid_subsub.get((record["theme_id"], record["subtheme_id"]), set())
        url_ok = record["evidence_url"].startswith(("https://63dac.conference-program.com/", "https://arxiv.org/", "https://zhiyaoxie.com/", "https://www.cse.cuhk.edu.hk/", "https://cris.technion.ac.il/", "https://panmnesia.com/", "https://www.linkedin.com/", "https://engineering.fb.com/", "https://aisystemcodesign.github.io/", "https://www.cpc.pku.edu.cn/", "https://pypi.org/", "https://jasonlau.io/"))
        fields_present = all(record.get(field) for field in ("problem", "method_or_artifact", "limits", "metrics"))
        checks.append({"paper_id": record["paper_id"], "evidence_overlap": round(overlap, 3) if overlap is not None else None,
                       "source_comparison_status": "captured_original_text_compared" if source_text else "original_source_text_missing_or_unmatched",
                       "taxonomy_valid": theme_ok and subsub_ok, "provenance_url_valid": url_ok,
                       "fields_present": fields_present,
                       "status": "pass" if overlap is not None and overlap >= 0.2 and theme_ok and subsub_ok and url_ok and fields_present else "review"})
    return {"audit_version": "v0-deterministic-adversarial-preflight", "judge_mode": "deterministic_preflight_not_llm", "record_count": len(checks), "pass_count": sum(item["status"] == "pass" for item in checks), "review_count": sum(item["status"] == "review" for item in checks), "checks": checks, "limits": "A passing preflight does not establish truth, novelty, importance, or full-corpus representativeness; adversarial LLM/human review remains required."}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    result = audit(args.root)
    (args.root / "reports/adversarial-preflight-v0.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({key: value for key, value in result.items() if key != "checks"}, indent=2, sort_keys=True))
