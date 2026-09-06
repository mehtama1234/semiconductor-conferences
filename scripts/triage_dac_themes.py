#!/usr/bin/env python3
"""Generate transparent, keyword-backed DAC theme triage candidates.

This is routing evidence for human/LLM adjudication, not a final classification.
Every candidate retains the matched vocabulary and is labeled triage-only.
"""
from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from pathlib import Path


RULES = {
    "architecture-and-accelerators": {
        "subtheme_id": "ai-accelerator-microarchitecture",
        "terms": ["accelerator", "npu", "gpu", "cpu", "architecture", "inference"],
    },
    "memory-interconnect-and-storage": {
        "subtheme_id": "memory-hierarchy-and-persistence",
        "terms": ["memory", "cache", "dram", "hbm", "cxl", "storage", "interconnect", "data movement"],
    },
    "ai-assisted-eda": {
        "subtheme_id": "llm-assisted-design-flows",
        "terms": ["llm", "large language", "generative", "design automation", "eda", "pcb placement", "circuit synthesis"],
    },
    "physical-design-and-manufacturing": {
        "subtheme_id": "placement-routing-and-timing",
        "terms": ["placement", "routing", "timing", "floorplan", "layout", "lithography", "power grid", "process node"],
    },
    "verification-and-validation": {
        "subtheme_id": "formal-and-functional-verification",
        "terms": ["verification", "formal", "validation", "testing", "assertion", "fuzzing", "bug detection"],
    },
    "chiplets-3d-and-packaging": {
        "subtheme_id": "chiplet-partitioning-and-integration",
        "terms": ["chiplet", "3d ic", "3d", "2.5d", "packaging", "stacked", "interposer"],
    },
    "power-reliability-and-security": {
        "subtheme_id": "energy-and-thermal-efficiency",
        "terms": ["power", "energy", "reliability", "fault", "security", "trojan", "side-channel", "thermal"],
    },
    "analog-mixed-signal-and-emerging-devices": {
        "subtheme_id": "neuromorphic-quantum-and-non-von-neumann",
        "terms": ["analog", "mixed-signal", "quantum", "neuromorphic", "photonic", "in-memory", "emerging device"],
    },
    "design-methodology-and-tooling": {
        "subtheme_id": "optimization-and-search-methods",
        "terms": ["synthesis", "compiler", "optimization", "design space", "search", "benchmark", "tool"],
    },
    "systems-applications-and-workloads": {
        "subtheme_id": "edge-embedded-and-mobile-systems",
        "terms": ["edge", "mobile", "cloud", "datacenter", "automotive", "robotics", "workload", "system"],
    },
}


def triage(row: dict) -> dict:
    corpus = f"{row['title']} {row.get('description') or ''}".lower()
    candidates = []
    for theme_id, rule in RULES.items():
        matched = [term for term in rule["terms"] if re.search(r"(?<![a-z0-9])" + re.escape(term) + r"(?![a-z0-9])", corpus)]
        if matched:
            candidates.append({"theme_id": theme_id, "subtheme_id": rule["subtheme_id"], "matched_terms": matched, "score": len(matched)})
    candidates.sort(key=lambda item: (-item["score"], item["theme_id"]))
    return {
        "paper_id": row["paper_id"],
        "conference_id": "dac",
        "analysis_edition": 2026,
        "title": row["title"],
        "evidence_url": row["evidence_url"],
        "triage_candidates": candidates[:3],
        "triage_status": "keyword_routing_only",
        "classification_confidence": "not_adjudicated",
        "limit": "Keyword matches route review and do not establish the paper's primary contribution, sub-subtheme, importance, or trend direction.",
    }


def main(root: Path) -> dict:
    rows = [json.loads(line) for line in (root / "dac/data/paper-evidence-2026.jsonl").read_text(encoding="utf-8").splitlines() if line.strip()]
    output_rows = [triage(row) for row in rows]
    output = root / "dac/data/theme-triage-2026.jsonl"
    with output.open("w", encoding="utf-8") as handle:
        for row in output_rows:
            handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")
    top = Counter(row["triage_candidates"][0]["theme_id"] for row in output_rows if row["triage_candidates"])
    return {"input_rows": len(rows), "output": str(output), "unrouted": sum(not row["triage_candidates"] for row in output_rows), "top_candidate_counts": dict(sorted(top.items()))}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    print(json.dumps(main(args.root), indent=2, sort_keys=True))
