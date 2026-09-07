#!/usr/bin/env python3
"""Route every inventory title to reviewable theme candidates.

This is deliberately metadata-only: title matches are routing hints, not
technical classifications, prevalence estimates, or trend evidence.
"""
from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from pathlib import Path


RULES = {
    "architecture-and-accelerators": ("ai-accelerator-microarchitecture", ["accelerator", "npu", "gpu", "cpu", "inference"]),
    "memory-interconnect-and-storage": ("memory-hierarchy-and-persistence", ["memory", "cache", "dram", "hbm", "cxl", "storage", "interconnect"]),
    "ai-assisted-eda": ("llm-assisted-design-flows", ["llm", "language model", "generative", "eda", "synthesis"]),
    "physical-design-and-manufacturing": ("placement-routing-and-timing", ["placement", "routing", "timing", "floorplan", "layout", "lithography"]),
    "verification-and-validation": ("formal-and-functional-verification", ["verification", "formal", "validation", "testing", "assertion", "fuzzing", "debugging"]),
    "chiplets-3d-and-packaging": ("chiplet-partitioning-and-integration", ["chiplet", "3d", "2.5d", "packaging", "stacked", "interposer"]),
    "power-reliability-and-security": ("energy-and-thermal-efficiency", ["power", "energy", "reliability", "fault", "security", "trojan", "side-channel", "thermal"]),
    "analog-mixed-signal-and-emerging-devices": ("neuromorphic-quantum-and-non-von-neumann", ["analog", "mixed-signal", "quantum", "neuromorphic", "photonic", "in-memory"]),
    "design-methodology-and-tooling": ("optimization-and-search-methods", ["compiler", "optimization", "design space", "search", "benchmark", "tool"]),
    "systems-applications-and-workloads": ("edge-embedded-and-mobile-systems", ["edge", "mobile", "cloud", "datacenter", "automotive", "robotics", "workload", "system"]),
}


def read_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def route(row: dict) -> dict:
    title = row.get("title", "")
    text = title.lower()
    candidates = []
    for theme_id, (subtheme_id, terms) in RULES.items():
        matched = [term for term in terms if re.search(r"(?<![a-z0-9])" + re.escape(term) + r"(?![a-z0-9])", text)]
        if matched:
            candidates.append({"theme_id": theme_id, "subtheme_id": subtheme_id, "matched_terms": matched, "score": len(matched)})
    candidates.sort(key=lambda item: (-item["score"], item["theme_id"]))
    return {
        "paper_id": row["paper_id"],
        "conference_id": row["conference_id"],
        "analysis_edition": row.get("analysis_edition"),
        "title": title,
        "theme_candidates": candidates[:3],
        "routing_status": "keyword_routing_only",
        "evidence_basis": "title_metadata_only",
        "limit": "Title matches route review and do not establish the primary contribution, technical subtheme, importance, prevalence, or trend direction.",
    }


def build(root: Path) -> dict:
    inventory = [row for path in sorted(root.glob("*/data/papers-*-program.jsonl")) for row in read_jsonl(path)]
    routed = [route(row) for row in inventory]
    output = root / "data/inventory-theme-routing-v1.jsonl"
    output.write_text("".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in routed), encoding="utf-8")
    top = Counter(row["theme_candidates"][0]["theme_id"] for row in routed if row["theme_candidates"])
    summary = {"schema": "inventory-theme-routing.v1", "status": "metadata_only_review_routing", "inventory_count": len(routed), "routed_count": sum(bool(row["theme_candidates"]) for row in routed), "unrouted_count": sum(not row["theme_candidates"] for row in routed), "top_candidate_counts": dict(sorted(top.items())), "limits": ["This does not replace abstract/full-text thematic coding.", "Candidate counts are not prevalence or directional trend evidence."]}
    (root / "reports/inventory-theme-routing-v1.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    lines = ["# Full-inventory theme routing v1", "", f"The inventory contains {len(routed)} papers; {summary['routed_count']} have at least one title-based candidate and {summary['unrouted_count']} do not.", "", "This is a metadata-only routing layer. It is not technical thematic analysis, prevalence, or a trend claim.", "", "| Candidate theme | Routed titles |", "|---|---:|"]
    lines.extend(f"| {theme} | {count} |" for theme, count in sorted(top.items(), key=lambda item: (-item[1], item[0])))
    lines += ["", "## Required next step", "", "Use these candidates to prioritize abstract/full-text collection, then adjudicate the shared problem, mechanism, conditions, metrics, limits, and provenance fields. Only independently reviewed evidence may enter the substantive synthesis.", ""]
    (root / "reports/inventory-theme-routing-v1.md").write_text("\n".join(lines), encoding="utf-8")
    return summary


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    print(json.dumps(build(parser.parse_args().root), indent=2, sort_keys=True))
