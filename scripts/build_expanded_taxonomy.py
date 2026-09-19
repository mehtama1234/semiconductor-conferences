#!/usr/bin/env python3
"""Build an evidence-derived expanded taxonomy from the deduplicated ledgers."""
from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path

try:
    from scripts.build_theme_pages import read_selected_sample, select_representatives
except ModuleNotFoundError:
    from build_theme_pages import read_selected_sample, select_representatives

ROOT = Path(__file__).resolve().parents[1]
OUT_JSON = ROOT / "data/taxonomy-expanded-v1.json"
OUT_MD = ROOT / "reports/expanded-taxonomy-v1.md"


def labelize(value: str) -> str:
    return value.replace("-", " ").capitalize()


def build(root: Path = ROOT) -> dict:
    rows = read_selected_sample(root)
    taxonomy = json.loads((root / "data/taxonomy-v0.json").read_text())
    theme_labels = {item["theme_id"]: item["label"] for item in taxonomy["themes"]}
    starter = {item["theme_id"]: set(item.get("subthemes", [])) for item in taxonomy["themes"]}
    groups = defaultdict(list)
    for row in rows:
        groups[row.get("theme_id", "unassigned")].append(row)

    themes = []
    for theme_id in sorted(groups, key=lambda x: theme_labels.get(x, x)):
        items = groups[theme_id]
        subgroups = defaultdict(list)
        for row in items:
            subgroups[row.get("subtheme_id") or "unassigned"].append(row)
        subthemes = []
        for subtheme_id in sorted(subgroups, key=lambda x: (-len(subgroups[x]), x)):
            subset = subgroups[subtheme_id]
            mechanisms = Counter(row.get("subsubtheme_id") or row.get("mechanism_label") or "unassigned" for row in subset)
            conferences = Counter(row.get("conference_id", "unknown") for row in subset)
            tiers = Counter(row.get("source_tier") or row.get("evidence_tier") or row.get("classification_confidence", "unknown") for row in subset)
            reps = select_representatives(subset, limit=3)
            subthemes.append({
                "subtheme_id": subtheme_id,
                "label": labelize(subtheme_id),
                "record_count": len(subset),
                "mechanism_count": len(mechanisms),
                "mechanisms": [{"id": key, "record_count": value} for key, value in mechanisms.most_common()],
                "conference_counts": dict(sorted(conferences.items())),
                "source_tier_counts": dict(sorted(tiers.items())),
                "representative_paper_ids": [row["paper_id"] for row in reps],
                "status": "starter_label" if subtheme_id in starter.get(theme_id, set()) else "observed_expansion",
            })
        themes.append({
            "theme_id": theme_id,
            "label": theme_labels.get(theme_id, labelize(theme_id)),
            "record_count": len(items),
            "subtheme_count": len(subthemes),
            "mechanism_count": len({row.get("subsubtheme_id") or row.get("mechanism_label") or "unassigned" for row in items}),
            "conference_counts": dict(sorted(Counter(row.get("conference_id", "unknown") for row in items).items())),
            "subthemes": subthemes,
        })

    observed_subthemes = {row.get("subtheme_id") or "unassigned" for row in rows}
    starter_ids = {s for values in starter.values() for s in values}
    result = {
        "schema": "taxonomy-expanded.v1",
        "status": "observed_selected_sample_taxonomy",
        "scope": "deduplicated adjudicated records across the selected ISCA, DAC, and ICCAD sample",
        "interpretation": "Observed labels are navigation and coding evidence, not prevalence, field ranking, or independent ontology proof.",
        "record_count": len(rows),
        "theme_count": len(themes),
        "observed_subtheme_count": len(observed_subthemes),
        "theme_subtheme_assignment_count": sum(theme["subtheme_count"] for theme in themes),
        "starter_subtheme_count": len(starter_ids),
        "expanded_subtheme_count": len(observed_subthemes - starter_ids),
        "mechanism_count": len({row.get("subsubtheme_id") or row.get("mechanism_label") or "unassigned" for row in rows}),
        "themes": themes,
    }
    OUT_JSON.write_text(json.dumps(result, indent=2) + "\n")

    lines = [
        "# Expanded taxonomy atlas v1", "",
        "The ten canonical themes remain the stable top-level spine. This atlas exposes the finer structure actually present in the coded corpus instead of treating the starter taxonomy as exhaustive.", "",
        f"The deduplicated selected sample contains **{len(rows)} records**, **{len(observed_subthemes)} observed subthemes**, and **{result['mechanism_count']} distinct mechanism labels**. The original starter taxonomy named only **{len(starter_ids)} subthemes**; **{result['expanded_subtheme_count']} additional observed labels** are now navigable here.", "",
        "## What these counts mean", "",
        "These are counts of coded records and labels in the selected ISCA, DAC, and ICCAD sample. They are not publication prevalence, venue importance, temporal growth, or proof that two similarly named labels are distinct research fields. A subtheme is an observed coding label; a mechanism is the paper-level technical differentiator. Read each record through its source tier, conditions, baselines, metrics, and limits.", "",
        "## Theme topology", "",
        "| Theme | Records | Observed subthemes | Mechanisms | Conference coverage |", "|---|---:|---:|---:|---|",
    ]
    for theme in themes:
        coverage = ", ".join(f"{key.upper()} {value}" for key, value in theme["conference_counts"].items())
        lines.append(f"| [{theme['label']}](themes/{theme['theme_id']}.md) | {theme['record_count']} | {theme['subtheme_count']} | {theme['mechanism_count']} | {coverage} |")
    lines += ["", "## Observed subtheme registry", "", "The registry below is intentionally exhaustive. Labels marked `expanded` were not in the starter taxonomy but recur in the adjudicated sample and therefore deserve direct navigation or future consolidation review.", ""]
    for theme in themes:
        lines += [f"### {theme['label']}", "", "| Subtheme | Status | Records | Mechanisms | Representative papers |", "|---|---|---:|---:|---|"]
        for subtheme in theme["subthemes"]:
            reps = ", ".join(f"`{paper}`" for paper in subtheme["representative_paper_ids"])
            lines.append(f"| [{subtheme['label']}](observed-subthemes/{subtheme['subtheme_id']}.md) | `{subtheme['status']}` | {subtheme['record_count']} | {subtheme['mechanism_count']} | {reps} |")
        lines.append("")
    lines += [
        "## How to use the expanded layer", "",
        "1. Start with a canonical theme to understand the first-principles boundary.",
        "2. Use this registry to find the observed subtheme and representative paper IDs.",
        "3. Open the theme page for source-backed paper cards and condition gaps.",
        "4. Move from the paper mechanism to the five high-value cross-cutting subtheme pages and six long-term direction pages only when the evidence supports that connection.", "",
        "## Taxonomy maintenance rule", "",
        "Do not split a label merely because titles differ, and do not merge labels merely because they share a workload. Promote an observed subtheme into a stable conceptual category only after at least two records expose the same mechanism boundary, or after a primary-source review demonstrates that the apparent distinction is real. Preserve aliases and uncertainty in the machine registry.", "",
    ]
    OUT_MD.write_text("\n".join(lines))
    return result


if __name__ == "__main__":
    print(json.dumps(build(), indent=2))
