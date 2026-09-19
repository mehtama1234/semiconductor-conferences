#!/usr/bin/env python3
"""Build canonical theme pages from the condition-aware coded evidence ledger."""
from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path
try:
    from scripts.research_articles import theme_article, build_observed, apply_editorial_corrections
except ModuleNotFoundError:
    from research_articles import theme_article, build_observed, apply_editorial_corrections


ROOT = Path(__file__).resolve().parents[1]
INPUT_GLOB = "**/data/adjudicated-*.jsonl"
TAXONOMY = ROOT / "data/taxonomy-v0.json"
OUT = ROOT / "reports/themes"

THEME_FRAMES = {
    "ai-assisted-eda": ("How can search, generation, and verification use tool feedback without confusing a proxy with a valid design?", "The design space is too large for exhaustive exploration, but an AI proposal is useful only when synthesis, simulation, formal checks, or measured constraints can reject or improve it."),
    "architecture-and-accelerators": ("How should computation be represented and executed when workload structure is too important to hide behind a general-purpose interface?", "Specialization exchanges flexibility for efficiency; the research question is whether the exposed structure survives workload, precision, and baseline changes."),
    "memory-interconnect-and-storage": ("When movement costs dominate arithmetic, what should the algorithm, architecture, and runtime agree to move, store, and reuse?", "Capacity, locality, bandwidth, contention, and topology become part of the algorithmic contract rather than late implementation details."),
    "chiplets-3d-and-packaging": ("How does physical partitioning change the feasible system, not merely its package diagram?", "Package boundaries, thermal coupling, power delivery, and die-to-die communication feed back into architecture and placement decisions."),
    "physical-design-and-manufacturing": ("How can design automation make process, geometry, timing, and power-delivery constraints executable early enough to change the design?", "A logically valid design is not physically realizable by default; the central mechanism is moving signoff-relevant information into search and construction."),
    "power-reliability-and-security": ("What happens when energy, faults, attacks, and recovery costs become first-class design objectives?", "Robustness is conditional on a threat or fault model, protection budget, and failure consequence; there is no universal robustness score."),
    "verification-and-validation": ("How do we know that a design, generated artifact, or optimization result is correct under the conditions that matter?", "Verification is not a final checkbox: its oracles, coverage, counterexamples, and cost shape which designs can be explored and trusted."),
    "design-methodology-and-tooling": ("Which abstractions, compilers, search procedures, and artifacts make a design decision repeatable and transferable?", "Tooling turns a design idea into an executable workflow; reproducibility and evaluator design determine whether claimed capability can be compared."),
    "systems-applications-and-workloads": ("Which real workloads and deployment environments create the constraints that specialized systems must satisfy?", "Workload and deployment context determine whether a mechanism is valuable; nominal application labels do not establish end-to-end benefit."),
    "analog-mixed-signal-and-emerging-devices": ("How can non-ideal, non-digital, or non-von-Neumann physics be used without hiding calibration, variation, and precision costs?", "Emerging devices change the feasible computation model, but device claims must remain coupled to modeling, calibration, workload, and physical evidence."),
}

THEME_EXPLANATIONS = {
    "ai-assisted-eda": {
        "problem": "Chip design has too many possible choices for a person or a simple search program to test one by one. The choices include circuit structure, layout, compiler settings, verification tests, and hardware mappings.",
        "change": "These papers use learned models or language models to propose, rank, repair, or generate design choices. The important technical question is whether the proposal is checked by a real design tool and whether failed proposals improve the next proposal.",
        "test": "A convincing result states the design set, tool version, search budget, correctness checks, comparison method, and the cost of failed attempts.",
    },
    "architecture-and-accelerators": {
        "problem": "A processor must execute a particular workload using limited compute units, memory, bandwidth, area, and power. A general processor hides useful workload structure, while a specialized design exposes it.",
        "change": "These papers change the organization of computation: which operations run together, where data is kept, how precision is represented, or how software controls the hardware.",
        "test": "The result must be checked on stated workloads against a clear hardware or software baseline, with the area, power, memory, and programming costs included.",
    },
    "memory-interconnect-and-storage": {
        "problem": "Computing an operation is often cheaper than fetching the data it needs. Delay, bandwidth, capacity, contention, and communication energy can determine total execution time.",
        "change": "These papers change where data is stored, when it moves, how it is shared, or which path carries it. The algorithm and the hardware must agree on reuse, placement, and movement.",
        "test": "The evaluation must state the data size, access pattern, topology, traffic, contention, capacity, and baseline. A bandwidth number alone does not establish end-to-end benefit.",
    },
    "chiplets-3d-and-packaging": {
        "problem": "A system built from several dies or stacked layers has physical connections, heat paths, power-delivery limits, and manufacturing constraints that affect its behavior.",
        "change": "These papers choose how functions are split across dies or layers and how those parts communicate, while accounting for heat, signal integrity, yield, and package limits.",
        "test": "The result must state the package or stack assumptions, die sizes, link properties, thermal model, power model, and which manufacturing effects are measured versus estimated.",
    },
    "physical-design-and-manufacturing": {
        "problem": "A design can be logically correct and still fail because wires are too long, timing is too slow, power delivery is insufficient, geometry violates a rule, or the process varies.",
        "change": "These papers change placement, routing, timing analysis, layout construction, process modeling, or manufacturing checks so that physical limits affect decisions earlier.",
        "test": "The evaluation must identify the design rules, technology data, tool settings, runtime, failure rate, and comparison flow. A proxy score is not the same as a valid manufactured design.",
    },
    "power-reliability-and-security": {
        "problem": "A system can be fast and still be unusable if it consumes too much power, fails under defects, leaks protected information, or cannot recover from an error.",
        "change": "These papers add protection, detection, correction, isolation, scheduling, or lower-power operation. Each choice trades hardware cost or performance against a stated failure or attack model.",
        "test": "The result must state the fault or threat, what is protected, how often failure occurs, recovery behavior, overhead, and what attacks or faults are outside the claim.",
    },
    "verification-and-validation": {
        "problem": "Design tools can produce an output without proving that the output is correct. Testing is limited by the number of cases, and formal methods are limited by model size and proof cost.",
        "change": "These papers create better tests, simulations, emulators, formal proofs, coverage measures, or security checks to find errors and establish what has been checked.",
        "test": "The evaluation must define the correctness rule, test population, coverage, false positives, false negatives, runtime, and remaining untested behavior.",
    },
    "design-methodology-and-tooling": {
        "problem": "A design idea is difficult to compare or reuse if the steps, inputs, tool versions, search choices, and output checks are not explicit.",
        "change": "These papers provide a compiler, synthesis method, optimizer, search method, benchmark, or artifact that turns design decisions into a repeatable process.",
        "test": "The result must show the inputs, transformations, resource budget, comparison tools, output quality, runtime, and whether another person can run the same process.",
    },
    "systems-applications-and-workloads": {
        "problem": "A hardware method is useful only when it meets the timing, quality, cost, energy, and reliability needs of a real workload and deployment setting.",
        "change": "These papers define the workload or service setting and change how computation is scheduled, placed, scaled, or supported by hardware.",
        "test": "The evaluation must state the input distribution, model or application, service target, hardware, scale, baseline, and quality constraint. A workload name alone is not a system evaluation.",
    },
    "analog-mixed-signal-and-emerging-devices": {
        "problem": "Non-digital devices can compute or communicate in ways that reduce a particular cost, but their output can vary with noise, temperature, manufacturing, calibration, and limited precision.",
        "change": "These papers use analog signals, optical paths, quantum states, new memory devices, or other physical behavior as part of computation or design automation.",
        "test": "The evaluation must connect device behavior to a workload and report variation, calibration, precision, energy, area, fabrication assumptions, and the digital work needed around the device.",
    },
}


def read_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]


def read_selected_sample(root: Path) -> list[dict]:
    """Load the deduplicated 3-venue selected sample, preserving record fields."""
    rows = []
    for path in sorted(root.glob(INPUT_GLOB)):
        rows.extend(read_jsonl(path))
    by_id = {}
    for row in rows:
        by_id[row["paper_id"]] = row
    for row in by_id.values():
        # Adjudicated ledgers use classification confidence and sub-subtheme;
        # normalize only for page rendering, without overwriting source data.
        row["_page_source_tier"] = row.get("source_tier") or row.get("evidence_tier") or row.get("classification_confidence", "unknown")
        row["_page_mechanism"] = row.get("mechanism_label") or row.get("subsubtheme_id") or "unassigned"
    return list(by_id.values())


def slug(value: str) -> str:
    return value.replace("/", "--")


def read_current_sample(root: Path) -> list[dict]:
    """Dated reading view; never rewrite ledgers or inherit acceptance for corrections."""
    rows = apply_editorial_corrections(root, read_selected_sample(root))
    for row in rows:
        row['_current_evidence_review_status'] = (
            'correction_pending_condition_and_independent_review'
            if row.get('_editorial_correction') else 'historical_record_no_editorial_correction'
        )
    return rows


def rank(row: dict) -> tuple:
    return (
        bool(row.get("metrics")),
        bool(row.get("baselines")),
        row.get("source_tier") in {"primary_or_author_copy", "author_artifact_source", "company_author_source"},
        row.get("paper_id", ""),
    )


def clean(value, limit: int = 420) -> str:
    if isinstance(value, list):
        value = "; ".join(str(item) for item in value)
    elif isinstance(value, dict):
        value = json.dumps(value, ensure_ascii=False, sort_keys=True)
    else:
        value = str(value or "unknown")
    value = " ".join(value.split()).replace("|", "\\|")
    return value if len(value) <= limit else value[: limit - 1] + "…"


def select_representatives(items: list[dict], limit: int = 12) -> list[dict]:
    """Keep venue diversity, then prefer records with conditions and metrics."""
    selected = []
    for conference in ("isca", "dac", "iccad"):
        candidates = sorted((item for item in items if item.get("conference_id") == conference), key=rank, reverse=True)
        selected.extend(candidates[:4])
    selected_ids = {item["paper_id"] for item in selected}
    for item in sorted(items, key=rank, reverse=True):
        if item["paper_id"] not in selected_ids:
            selected.append(item)
            selected_ids.add(item["paper_id"])
        if len(selected) >= limit:
            break
    return selected[:limit]


def build(root: Path = ROOT) -> dict:
    rows = read_current_sample(root)
    build_observed(root, rows)
    taxonomy = json.loads((root / TAXONOMY.relative_to(ROOT)).read_text())
    labels = {item["theme_id"]: item["label"] for item in taxonomy["themes"]}
    groups: dict[str, list[dict]] = defaultdict(list)
    for row in rows:
        if row.get("theme_id"):
            groups[row["theme_id"]].append(row)
    OUT.mkdir(exist_ok=True)
    index = []
    for theme_id, items in sorted(groups.items(), key=lambda pair: labels.get(pair[0], pair[0])):
        label = labels.get(theme_id, theme_id)
        question, principle = THEME_FRAMES.get(theme_id, ("What constraint does this theme expose?", "The mechanism must be interpreted under its explicit conditions."))
        explanation = THEME_EXPLANATIONS.get(theme_id, {"problem": "What technical problem is present?", "change": "What does the method change?", "test": "What evidence would establish the result?"})
        subthemes = Counter(item.get("subtheme_id") or "unassigned" for item in items)
        mechanisms = Counter(item.get("_page_mechanism", "unassigned") for item in items)
        selected = select_representatives(items)
        missing = {field: sum(not item.get(field) for item in items) for field in ("workload_or_benchmark", "hardware_or_process_assumptions", "baselines", "metrics")}
        filename = f"{slug(theme_id)}.md"
        lines = [
            f"# {label}", "",
            "This is a canonical theme page generated from the condition-aware coded evidence ledger.",
            "It is a navigation and synthesis page for a selected sample, not a prevalence estimate or independent review.", "",
            "## First-principles question", "", question, "",
            "## Working principle", "", principle, "",
            "## In plain technical terms", "",
            f"**The problem.** {explanation['problem']}", "",
            f"**What the papers change.** {explanation['change']}", "",
            f"**What must be tested.** {explanation['test']}", "",
            "## How to read the page", "",
            "Read the mechanism map to see how the papers were grouped. Then read the representative records. For each record, ask: what input or workload was used, what design decision changed, what limit was assumed, what baseline was used, and what result was actually measured? A blank field means the current source did not establish it.", "",
            "## Contents", "",
            "- [Mechanism map](#mechanism-map)",
            "- [Representative source-backed records](#representative-source-backed-records)",
            "- [Paper cards](#paper-cards-what-changes-and-where-it-stops)",
            "- [What the evidence supports](#what-the-evidence-supports)",
            "- [Limits and next evidence](#limits-and-next-evidence)", "",
            "## Mechanism map", "",
            "| Subtheme | Records | Representative mechanisms |", "|---|---:|---|",
        ]
        by_sub: dict[str, list[str]] = defaultdict(list)
        for item in items:
            by_sub[item.get("subtheme_id") or "unassigned"].append(item.get("_page_mechanism", "unassigned"))
        for subtheme, count in sorted(subthemes.items(), key=lambda pair: (-pair[1], pair[0])):
            reps = "; ".join(name for name, _ in Counter(by_sub[subtheme]).most_common(4))
            lines.append(f"| `{subtheme}` | {count} | {reps} |")
        lines += ["", "## Representative source-backed records", "", "The records below are selected for mechanism and condition detail. Open the source URL and preserve the stated evidence tier; the project does not treat an official description as a full paper.", "", "| Paper | Conference / edition | Mechanism | Evidence tier | Workload | Hardware / process | Baseline / metric state | Source |", "|---|---|---|---|---|---|---|---|"]
        for item in selected:
            workload = "present" if item.get("workload_or_benchmark") else "missing"
            hardware = "present" if item.get("hardware_or_process_assumptions") else "missing"
            baseline = "present" if item.get("baselines") else "missing"
            metrics = "present" if item.get("metrics") else "missing"
            source = f"[source]({item['evidence_url']})" if item.get("evidence_url") else "source URL not captured"
            lines.append(f"| `{item['paper_id']}` — {item['title']} | {item['conference_id'].upper()} {item['analysis_edition']} | `{item.get('_page_mechanism', 'unassigned')}` | `{item.get('_page_source_tier', 'unknown')}` | {workload} | {hardware} | {baseline} / {metrics} | {source} |")
        lines += ["", "## Paper cards: what changes and where it stops", "", "These cards expose the coded problem, mechanism, conditions, reported metric, and limits for the same representative records. They are compact source-grounded summaries, not substitutes for the underlying paper or official record.", ""]
        for item in selected:
            metric = clean(item.get("metrics") or "not reported", 300)
            limits = clean(item.get("limits") or "not recorded", 420)
            locator = clean(item.get("evidence_locators") or item.get("evidence_locator") or item.get("source_locator") or "source locator not recorded", 260)
            lines += [
                "<details>",
                f"<summary><strong>{item['paper_id']}</strong> — {item['title']}</summary>",
                "",
                f"- **Problem:** {clean(item.get('problem'))}",
                f"- **Mechanism / artifact:** {clean(item.get('method_or_artifact'))}",
                f"- **Workload:** {clean(item.get('workload_or_benchmark'))}",
                f"- **Hardware / process:** {clean(item.get('hardware_or_process_assumptions'))}",
                f"- **Reported metric:** {metric}",
                f"- **Limits:** {limits}",
                f"- **Evidence:** `{item.get('_page_source_tier', 'unknown')}`; locator `{locator}`; [source]({item.get('evidence_url')})" if item.get("evidence_url") else f"- **Evidence:** `{item.get('_page_source_tier', 'unknown')}`; locator `{locator}`; source URL not captured",
                "",
                "</details>",
                "",
            ]
        lines += ["## What the evidence supports", "", f"The ledger contains **{len(items)}** coded records in this theme. The most common mechanism labels are " + ", ".join(f"`{name}` ({count})" for name, count in mechanisms.most_common(6)) + ". These counts route reading; they do not establish importance, field share, or temporal growth.", "", "The current source-condition boundary is: " + "; ".join(f"{field.replace('_or_benchmark', '').replace('_or_process_assumptions', '').replace('baselines', 'baseline').replace('metrics', 'metric')} missing in {count}/{len(items)}" for field, count in missing.items()) + ".", "", "## Cross-conference and long-term connection", "", "Use this theme as the mechanism layer between the [research atlas](../research-atlas-index-v1.md) and the canonical direction pages. A theme record becomes useful for a long-term direction only when its workload, hardware/process assumptions, baseline, metric, and limits can be compared with another venue or edition.", "", "## Limits and next evidence", "", "- This page is derived from selected coded records and is not a venue-wide count.", "- Source tier and condition presence do not establish correctness or independent reproduction.", "- Missing fields are evidence gaps, not negative results.", "- Next step: recover primary text or artifacts for the representative records, extract exact locators and budgets, and send the resulting packet through independent review.", ""]
        (root / "reports/themes" / filename).write_text("\n".join(theme_article(theme_id, label, items, selected, root=root)))
        index.append({"theme_id": theme_id, "label": label, "page": f"reports/themes/{filename}", "record_count": len(items), "subtheme_count": len(subthemes), "representative_record_count": len(selected)})
    index_lines = ["# Theme atlas", "", "The ten canonical theme pages are the mechanism-navigation layer of the research atlas. Each page moves from a first-principles question to subthemes, mechanisms, representative paper records, source URLs, and condition gaps.", "", "| Theme | Records | Subthemes | Page |", "|---|---:|---:|---|"]
    for item in index:
        index_lines.append(f"| {item['label']} | {item['record_count']} | {item['subtheme_count']} | [{item['label']}]({Path(item['page']).name}) |")
    index_lines += ["", "## Reading rule", "", "The record totals come from the deduplicated adjudicated ledgers under `*/data/adjudicated-*.jsonl`, a selected coded sample spanning three venues. They are not prevalence, ranking, or trend estimates. Follow every material claim to the linked source and then to the condition and review registers.", ""]
    (root / "reports/themes/README.md").write_text("\n".join(index_lines))
    return {"schema": "theme-pages.v1", "theme_count": len(index), "record_count": len(rows), "pages": index}


if __name__ == "__main__":
    print(json.dumps(build(), indent=2))
