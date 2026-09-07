#!/usr/bin/env python3
"""Build a bounded, condition-aware profile of the coded description sample."""
from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path


def read(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def present(row: dict, field: str) -> bool:
    value = row.get(field)
    return bool(value) if field != "metrics" else bool(value)


def build(root: Path) -> dict:
    rows = read(root / "data/current-description-coding-v1.jsonl")
    groups: dict[str, list[dict]] = defaultdict(list)
    for row in rows:
        groups[row.get("theme_id") or "unassigned"].append(row)
    themes = []
    for theme, items in sorted(groups.items()):
        subthemes = Counter(item.get("subtheme_id") or "unassigned" for item in items)
        mechanisms = Counter(item.get("mechanism_label") or "unassigned" for item in items)
        themes.append({
            "theme_id": theme,
            "record_count": len(items),
            "subtheme_counts": dict(sorted(subthemes.items())),
            "top_mechanisms": [{"mechanism": name, "record_count": count} for name, count in mechanisms.most_common(12)],
            "source_tiers": dict(sorted(Counter(item.get("source_tier", "unknown") for item in items).items())),
            "condition_presence": {field: sum(present(item, field) for item in items) for field in ("workload_or_benchmark", "hardware_or_process_assumptions", "baselines", "metrics")},
        })
    result = {
        "schema": "deep-theme-profile.v1",
        "status": "provisional_selected_sample_profile",
        "record_count": len(rows),
        "source": "data/current-description-coding-v1.jsonl",
        "themes": themes,
        "limits": [
            "All source tiers in this input are official program descriptions; this is not full-paper evidence.",
            "Counts describe the selected coded sample and cannot estimate venue prevalence, field direction, adoption, or importance.",
            "Condition presence counts do not establish that a metric is comparable, correct, independently reproduced, or end-to-end.",
        ],
    }
    (root / "data/deep-theme-profile-v1.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    lines = [
        "# Deep theme profile v1",
        "",
        f"This profile summarizes {len(rows)} coded description records. It is a selected-sample mechanism map, not a prevalence or temporal trend estimate.",
        "",
        "| Theme | Records | Top subthemes | Conditions present (workload / hardware / baseline / metrics) |",
        "|---|---:|---|---|",
    ]
    for item in themes:
        top_sub = "; ".join(f"{name} ({count})" for name, count in sorted(item["subtheme_counts"].items(), key=lambda pair: (-pair[1], pair[0]))[:4])
        c = item["condition_presence"]
        lines.append(f"| {item['theme_id']} | {item['record_count']} | {top_sub} | {c['workload_or_benchmark']} / {c['hardware_or_process_assumptions']} / {c['baselines']} / {c['metrics']} |")
    lines += [
        "",
        "## How to read it",
        "",
        "Mechanism and subtheme counts route deeper reading. They do not mean that a topic is rising, that a method is important, or that records are comparable. Before promoting a quantitative or directional conclusion, recover primary text, preserve exact conditions and baselines, and obtain independent review.",
        "",
    ]
    (root / "reports/deep-theme-profile-v1.md").write_text("\n".join(lines), encoding="utf-8")
    return {"record_count": len(rows), "theme_count": len(themes), "status": result["status"]}


if __name__ == "__main__":
    root = Path(__file__).resolve().parents[1]
    print(json.dumps(build(root), indent=2, sort_keys=True))
