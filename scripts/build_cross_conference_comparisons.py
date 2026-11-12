#!/usr/bin/env python3
"""Build reader-facing cross-conference comparison dossiers."""
from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path

try:
    from scripts.build_theme_pages import read_current_sample
except ModuleNotFoundError:
    from build_theme_pages import read_current_sample


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "reports/comparisons"


def load_json(path: str):
    return json.loads((ROOT / path).read_text())


def load_jsonl(path: str):
    return [json.loads(line) for line in (ROOT / path).read_text().splitlines() if line.strip()]


def build() -> dict:
    atlas = load_json("data/long-term-direction-atlas-v1.json")
    current = {row['paper_id']: row for row in read_current_sample(ROOT)}
    cross = {row["direction_id"]: row for row in load_json("data/cross-conference-direction-atlas-v1.json")["directions"]}
    queue = {row["paper_id"]: row for row in load_jsonl("data/research-work-queue.jsonl")}
    gate = {row["direction_id"]: row for row in load_json("data/direction-review-gate-v1.json")["directions"]}
    OUT.mkdir(exist_ok=True)
    dossiers = []
    for direction in atlas["directions"]:
        direction_id = direction["direction_id"]
        comparison = cross[direction_id]
        refs = {row["paper_id"] for row in direction.get("evidence", [])}
        challenge_id = direction.get("challenge", {}).get("paper_id")
        if challenge_id:
            refs.add(challenge_id)
        grouped = defaultdict(list)
        corrected_ids = []
        for paper_id in sorted(refs):
            row = queue.get(paper_id, {})
            evidence = next((item for item in direction.get("evidence", []) if item["paper_id"] == paper_id), {})
            revised = current.get(paper_id, {})
            correction = revised.get('_editorial_correction')
            historical_condition = next((p["condition_status"] for p in gate[direction_id]["papers"] if p["paper_id"] == paper_id), "not_registered")
            if correction:
                corrected_ids.append(paper_id)
            grouped[row.get("conference_id") or evidence.get("conference_id") or "unknown"].append({
                "paper_id": paper_id,
                "title": row.get("title", "title not captured"),
                "edition": row.get("analysis_edition") or evidence.get("edition"),
                "evidence_tier": revised['_page_source_tier'] if correction else row.get("evidence_tier") or evidence.get("evidence_tier"),
                "evidence_url": revised['evidence_url'] if correction else row.get("evidence_url"),
                "condition_status": 'correction_pending_condition_review' if correction else historical_condition,
                "historical_condition_status": historical_condition,
                "correction_date": correction['review_date'] if correction else None,
                "reading_page": f"../observed-subthemes/{revised['subtheme_id']}.md#paper-{paper_id}" if correction else None,
                "source_direction_id": evidence.get("source_direction_id"),
            })
        filename = f"{direction_id}.md"
        lines = [
            f"# {direction['label']}: cross-conference comparison", "",
            "This dossier asks what the three venues contribute to the same conceptual pressure. It is a layer comparison, not a ranking, prevalence estimate, or temporal trend claim.", "",
            f"**Relation type:** `{comparison['relation_type']}`  ",
            f"**Current gate:** `{gate[direction_id]['promotion_gate']}`", "",
            "## Comparative proposition", "", comparison["interpretation"], "",
            "## Venue roles", "", "| Venue | Current role | Evidence references |", "|---|---|---:|",
        ]
        for venue in ("isca", "dac", "iccad"):
            lines.append(f"| {venue.upper()} | {comparison['venue_roles'][venue]} | {comparison['conference_reference_counts'].get(venue, 0)} |")
        lines += ["", "## Paper-level comparison set", "", "These are the source-backed references currently attached to the direction. Different source tiers and condition completeness are preserved rather than normalized away. Dated corrections use current source links, but do not inherit a historical complete-condition label. The direction promotion gate above is historical and is not newly satisfied by a correction.", ""]
        for venue in ("isca", "dac", "iccad", "unknown"):
            if not grouped.get(venue):
                continue
            lines += [f"### {venue.upper()}", "", "| Paper | Edition | Evidence tier | Conditions | Source |", "|---|---:|---|---|---|"]
            for paper in grouped[venue]:
                source = f"[source]({paper['evidence_url']})" if paper["evidence_url"] else "source URL not captured"
                lines.append(f"| `{paper['paper_id']}` — {paper['title']} | {paper['edition']} | `{paper['evidence_tier']}` | `{paper['condition_status']}` | {source} |")
            lines.append("")
            for paper in grouped[venue]:
                if paper['correction_date']:
                    lines += [f"- [{paper['paper_id']}: current correction and original evidence]({paper['reading_page']}) — corrected {paper['correction_date']}; historical condition status `{paper['historical_condition_status']}` is not carried forward as approval."]
            lines.append('')
        lines += [
            "## What is actually comparable", "",
            "The comparison should be made at the mechanism and constraint level first. A fair comparison holds six things fixed: the workload or design set, the hardware or simulator assumptions, the baseline, the metric, the test budget, and what counts as a failure.", "",
            "### Required matched fields", "",
            "| Field | Why it matters |", "|---|---|",
            "| Workload / design population | Determines whether the mechanism addresses the same pressure. |",
            "| Hardware / process / tool version | Separates a mechanism from a platform advantage. |",
            "| Baseline and budget | Prevents unequal search, retries, tuning, or evaluator effort. |",
            "| Metric and end-to-end boundary | Prevents proxy improvement from being reported as system benefit. |",
            "| Failure model and limits | Defines what counts as valid, safe, feasible, or transferable. |",
            "", "## Next matched comparison", "", comparison["next_comparison"], "",
            "## Current conclusion boundary", "",
            "The evidence supports a provisional cross-conference mechanism relation. It does not establish that the direction is increasing, dominant, superior, or independently validated. The [direction review gate](../direction-review-gate-v1.md) records the remaining promotion work.", "",
        ]
        (OUT / filename).write_text("\n".join(lines))
        dossiers.append({"direction_id": direction_id, "label": direction["label"], "page": f"reports/comparisons/{filename}", "reference_count": len(refs), "conference_reference_counts": comparison["conference_reference_counts"], "relation_type": comparison["relation_type"], "promotion_gate": gate[direction_id]["promotion_gate"], "corrected_reference_ids": corrected_ids, "correction_review_status": "pending_condition_and_independent_review" if corrected_ids else "no_registered_corrections"})
    index = ["# Cross-conference comparison dossiers", "", "These dossiers turn the cross-conference atlas into reader-facing comparisons. They preserve venue asymmetry and state the matched experiment needed before a long-term claim can be promoted.", "", "| Direction | Relation | References | Dossier |", "|---|---|---:|---|"]
    for item in dossiers:
        index.append(f"| {item['label']} | `{item['relation_type']}` | {item['reference_count']} | [{item['label']}]({Path(item['page']).name}) |")
    index += ["", "## Interpretation rule", "", "A shared pressure is not a shared result. Read the paper-level source tier and condition status before comparing mechanisms; then apply the longitudinal and independent-review gates.", ""]
    (OUT / "README.md").write_text("\n".join(index))
    result = {"schema": "cross-conference-comparison-dossiers.v1", "status": "provisional_cross_conference_synthesis", "dossiers": dossiers}
    (ROOT / "data/cross-conference-comparison-dossiers-v1.json").write_text(json.dumps(result, indent=2) + "\n")
    return result


if __name__ == "__main__":
    print(json.dumps(build(), indent=2))
