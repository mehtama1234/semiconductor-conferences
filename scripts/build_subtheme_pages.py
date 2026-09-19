#!/usr/bin/env python3
"""Build the five high-value subtheme pages named by the research program."""
from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

try:
    from scripts.build_theme_pages import clean, read_current_sample, select_representatives
except ModuleNotFoundError:  # direct execution via `python3 scripts/...`
    from build_theme_pages import clean, read_current_sample, select_representatives


ROOT = Path(__file__).resolve().parents[1]
try:
    from scripts.research_articles import subtheme_article
except ModuleNotFoundError:
    from research_articles import subtheme_article
OUT = ROOT / "reports/subthemes"

SUBTHEMES = {
    "tool-grounded-design": {
        "label": "Tool-grounded design and verification",
        "theme_ids": ["ai-assisted-eda", "design-methodology-and-tooling", "verification-and-validation"],
        "subtheme_ids": ["llm-assisted-design-flows", "high-level-synthesis-and-compilers", "simulation-emulation-and-testing", "formal-and-functional-verification"],
        "question": "When a model proposes a design change, which executable tools decide whether it is valid, useful, and worth the evaluation cost?",
        "principle": "Generation becomes engineering only when synthesis, simulation, formal checking, or measured constraints can reject, repair, or rank the proposal.",
        "plain": ("Design tools can generate code or layouts that look plausible but do not work. The central problem is deciding validity before expensive implementation.", "The papers connect generated choices to synthesis, simulation, formal checking, or measured design limits.", "The useful test reports how many proposals were tried, how many failed, what checked them, and whether the final design improved against a fixed baseline."),
        "direction_ids": ["constraints-become-executable", "closed-loop-design", "evaluation-as-research"],
    },
    "movement-aware-systems": {
        "label": "Movement-aware systems",
        "theme_ids": ["memory-interconnect-and-storage", "architecture-and-accelerators", "systems-applications-and-workloads"],
        "subtheme_ids": ["data-movement-and-locality", "memory-hierarchy-and-persistence", "chiplet-and-on-chip-interconnect", "architecture-software-co-design"],
        "question": "When movement, capacity, and contention dominate arithmetic, what contract must the algorithm, hardware, and runtime share?",
        "principle": "Placement, locality, migration, topology, and contention are algorithmically consequential, not merely implementation details.",
        "plain": ("Moving data takes time, capacity, bandwidth, and energy. When many workers use the same path, contention can dominate the work itself.", "The papers change data placement, reuse, routing, storage, or scheduling so that movement is planned with computation.", "The useful test reports traffic, data size, topology, contention, capacity, and end-to-end time or energy against a stated baseline."),
        "direction_ids": ["data-movement-as-contract", "physical-reality-in-the-loop"],
    },
    "reliability-security-loops": {
        "label": "Reliability and security loops",
        "theme_ids": ["power-reliability-and-security", "verification-and-validation"],
        "subtheme_ids": ["fault-tolerance-and-reliability", "reliability-and-fault-tolerance", "side-channel-and-hardware-security", "power-integrity-and-reliability", "hardware-security-validation"],
        "question": "How do fault, threat, and physical-integrity models change the design decision before failure or attack reaches deployment?",
        "principle": "Robustness is an operating envelope with protection, recovery, residual-risk, and useful-throughput costs—not a scalar property.",
        "plain": ("Systems can fail because of defects, environmental conditions, or attacks. Protection changes cost and may also change useful work or speed.", "The papers detect, prevent, correct, isolate, or recover from a stated fault or threat.", "The useful test names the fault or threat, measures protection cost and remaining risk, and states what cases are not covered."),
        "direction_ids": ["reliability-security-upstream", "evaluation-as-research"],
    },
    "physical-aware-optimization": {
        "label": "Physical-aware optimization",
        "theme_ids": ["physical-design-and-manufacturing", "chiplets-3d-and-packaging", "design-methodology-and-tooling"],
        "subtheme_ids": ["process-aware-design", "3d-stacking-and-thermal-management", "placement-routing-and-timing", "floorplanning-and-power-delivery", "optimization-and-search-methods"],
        "question": "When geometry, process, thermal, and power-delivery constraints enter search, do they improve feasible decisions or only make a faster proxy?",
        "principle": "A logically attractive optimum matters only if higher-fidelity physical evaluation accepts it under the relevant process and geometry boundary.",
        "plain": ("A design choice can look good in an abstract model and fail after wire length, timing, heat, power delivery, or manufacturing rules are included.", "The papers put physical measurements or models into placement, routing, search, packaging, or process decisions.", "The useful test compares final valid designs, not only proxy scores, and reports technology data, tool settings, runtime, and failed cases."),
        "direction_ids": ["physical-reality-in-the-loop", "closed-loop-design", "evaluation-as-research"],
    },
    "evaluation-infrastructure": {
        "label": "Evaluation infrastructure",
        "theme_ids": ["verification-and-validation", "design-methodology-and-tooling"],
        "subtheme_ids": ["reproducibility-artifacts-and-benchmarks", "simulation-emulation-and-testing", "formal-and-functional-verification", "hardware-security-validation"],
        "question": "What evaluator, task population, version, oracle, budget, and failure semantics make a capability claim reproducible and comparable?",
        "principle": "The evaluator is part of the result: task selection, timeout semantics, proof state, contamination, and artifact availability define what a score means.",
        "plain": ("A number is not meaningful unless the task, input set, correctness rule, time limit, and comparison are known.", "The papers improve benchmarks, test systems, emulators, proof procedures, artifacts, or measurement rules.", "The useful test makes the evaluation repeatable and shows what was tested, what was not tested, and how much the evaluation cost."),
        "direction_ids": ["evaluation-as-research", "constraints-become-executable"],
    },
}


def build() -> dict:
    rows = read_current_sample(ROOT)
    direction_pages = {item["direction_id"]: item["page"].split("reports/", 1)[-1] for item in json.loads((ROOT / "data/long-term-direction-atlas-v1.json").read_text())["directions"]}
    OUT.mkdir(exist_ok=True)
    pages = []
    for slug, spec in SUBTHEMES.items():
        items = [row for row in rows if row.get("subtheme_id") in spec["subtheme_ids"]]
        selected = select_representatives(items, limit=10)
        mechanisms = Counter(row.get("_page_mechanism", "unassigned") for row in items)
        venues = Counter(row.get("conference_id") for row in items)
        lines = [
            f"# {spec['label']}", "",
            "This is a canonical subtheme page in the selected 3-venue sample. It is a mechanism-focused reading layer, not a prevalence estimate or independent review.", "",
            "## First-principles question", "", spec["question"], "",
            "## Working principle", "", spec["principle"], "",
            "## In plain technical terms", "",
            f"**The problem.** {spec['plain'][0]}", "",
            f"**What the papers change.** {spec['plain'][1]}", "",
            f"**What must be tested.** {spec['plain'][2]}", "",
            "## How to read the evidence", "",
            "For every paper below, separate the proposed method from the reported result. Check the workload, hardware or process, baseline, metric, and stated limit before treating a result as evidence for a broader direction.", "",
            "## Contents", "",
            "- [Scope](#scope)",
            "- [Mechanisms](#mechanisms)",
            "- [Representative evidence](#representative-evidence)",
            "- [Technical cards](#technical-cards)",
            "- [Direction connection](#direction-connection)", "",
            "## Scope", "", f"This subtheme groups `{', '.join(spec['subtheme_ids'])}` across the themes `{', '.join(spec['theme_ids'])}`. It contains **{len(items)}** selected coded records: " + ", ".join(f"{venue.upper()} {count}" for venue, count in sorted(venues.items())) + ".", "",
            "## Mechanisms", "", "| Mechanism | Records |", "|---|---:|"]
        for mechanism, count in mechanisms.most_common(18):
            lines.append(f"| `{mechanism}` | {count} |")
        lines += ["", "## Representative evidence", "", "| Paper | Venue | Mechanism | Evidence tier | Conditions | Source |", "|---|---|---|---|---|---|"]
        for row in selected:
            conditions = ", ".join(field for field, value in (("workload", row.get("workload_or_benchmark")), ("hardware", row.get("hardware_or_process_assumptions")), ("baseline", row.get("baselines")), ("metrics", row.get("metrics"))) if value) or "none recorded"
            source = f"[source]({row['evidence_url']})" if row.get("evidence_url") else "source URL not captured"
            lines.append(f"| `{row['paper_id']}` — {row['title']} | {row['conference_id'].upper()} {row['analysis_edition']} | `{row.get('_page_mechanism', 'unassigned')}` | `{row.get('_page_source_tier', 'unknown')}` | {conditions} | {source} |")
        lines += ["", "## Technical cards", ""]
        for row in selected:
            source = f"[source]({row['evidence_url']})" if row.get("evidence_url") else "source URL not captured"
            lines += ["<details>", f"<summary><strong>{row['paper_id']}</strong> — {row['title']}</summary>", "", f"- **Problem:** {clean(row.get('problem'))}", f"- **Mechanism / artifact:** {clean(row.get('method_or_artifact'))}", f"- **Conditions:** workload `{clean(row.get('workload_or_benchmark'), 260)}`; hardware `{clean(row.get('hardware_or_process_assumptions'), 260)}`", f"- **Metric:** {clean(row.get('metrics') or 'not reported', 300)}", f"- **Limit:** {clean(row.get('limits') or 'not recorded', 400)}", f"- **Source:** `{row.get('_page_source_tier', 'unknown')}`; {source}", "", "</details>", ""]
        direction_links = ", ".join(f"[{did}](../{direction_pages[did]})" for did in spec["direction_ids"])
        theme_links = ", ".join(f"[{tid}](../themes/{tid}.md)" for tid in spec["theme_ids"])
        lines += ["## Direction connection", "", f"This subtheme feeds the long-term directions {direction_links}. Its parent theme pages are {theme_links}.", "", "## Limits and next evidence", "", "- The record set is selected for recoverable evidence and mechanism diversity, not field prevalence.", "- Source tiers and condition presence do not establish correctness or independent reproduction.", "- The next comparison must hold workload/design population, hardware/process, baseline, metric, budget, and validity boundary constant.", ""]
        (OUT / f"{slug}.md").write_text("\n".join(subtheme_article(spec, items, selected)))
        pages.append({"subtheme_id": slug, "label": spec["label"], "page": f"reports/subthemes/{slug}.md", "record_count": len(items), "representative_record_count": len(selected), "direction_ids": spec["direction_ids"]})
    index = ["# Subtheme atlas", "", "These five subtheme pages are the high-value mechanism layer between the ten themes and the six long-term directions. They contain paper-level cards, conditions, source tiers, and explicit next comparisons.", "", "| Subtheme | Records | Representatives | Directions | Page |", "|---|---:|---:|---|---|"]
    for page in pages:
        index.append(f"| {page['label']} | {page['record_count']} | {page['representative_record_count']} | {', '.join(page['direction_ids'])} | [{page['label']}]({Path(page['page']).name}) |")
    index += ["", "The five pages above connect related subjects. For the complete set of 113 observed subthemes, use the [expanded taxonomy](../expanded-taxonomy-v1.md).", "", "## Reading rule", "", "Subtheme counts route technical reading. They do not imply prevalence, ranking, temporal growth, or comparable performance.", ""]
    (OUT / "README.md").write_text("\n".join(index))
    return {"schema": "subtheme-pages.v1", "status": "provisional_selected_sample", "pages": pages}


if __name__ == "__main__":
    print(json.dumps(build(), indent=2))
